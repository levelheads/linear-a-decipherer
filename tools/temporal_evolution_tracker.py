#!/usr/bin/env python3
"""
Temporal Evolution Tracker for Linear A

Tracks how Linear A administrative writing evolved across archaeological
periods by analyzing:
1. Word frequency distributions per period (using word_filter_contract)
2. Logogram usage patterns per period
3. Administrative structure markers (KU-RO, KI-RO, SA-RA₂) per period
4. Site distribution per period
5. Vocabulary changes across periods (appearance/disappearance)
6. Document complexity evolution over time

Usage:
    python3 tools/temporal_evolution_tracker.py --all
    python3 tools/temporal_evolution_tracker.py --period LMIB
    python3 tools/temporal_evolution_tracker.py --vocabulary
    python3 tools/temporal_evolution_tracker.py --structure
    python3 tools/temporal_evolution_tracker.py --output data/temporal_evolution.json

Attribution:
    Part of Linear A Decipherment Project
    Builds on word_filter_contract for lexical eligibility
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field

# Local imports
sys.path.insert(0, str(Path(__file__).parent))
from word_filter_contract import is_hypothesis_eligible_word, normalize_word_token

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
DEFAULT_OUTPUT = DATA_DIR / "temporal_evolution.json"

# Chronological period ordering
PERIOD_ORDER = [
    "MMII",
    "MMIIIA",
    "MMIIIB",
    "MMIII",
    "LMIA",
    "LMI",
    "LMIB",
    "LMIIIA",
    "Geometric",
    "LBI",
]

# Administrative markers to track
ADMIN_MARKERS = ["KU-RO", "KI-RO", "SA-RA\u2082"]

# Known commodity logograms
COMMODITY_LOGOGRAMS = {
    "GRA",
    "VIN",
    "OLE",
    "OLIV",
    "FIC",
    "FAR",
    "CYP",
    "OVI",
    "CAP",
    "SUS",
    "BOS",
    "VIR",
    "MUL",
    "TELA",
}

COMMODITY_LIGATURE_BASES = {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}

# Numeric/fraction pattern for token classification
NUMERIC_RE = re.compile(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|½¼¾⅓⅔⅛⅜~≈]+$")


def _is_logogram(token: str) -> bool:
    """Check if a token is a commodity logogram or ligature."""
    if token in COMMODITY_LOGOGRAMS:
        return True
    if "+" in token:
        base = token.split("+")[0]
        return base in COMMODITY_LIGATURE_BASES
    return False


def _get_logogram_base(token: str) -> str:
    """Get the base commodity from a logogram (handles ligatures)."""
    if "+" in token:
        return token.split("+")[0]
    return token


def _is_numeric(token: str) -> bool:
    """Check if a token is purely numeric/fractional."""
    if not token:
        return False
    return bool(NUMERIC_RE.match(token))


def _is_separator(token: str) -> bool:
    """Check if a token is a structural separator."""
    return token in {"", "\n", "|", "\u2014", "\u10101", "\u2248"}


@dataclass
class PeriodProfile:
    """Statistical profile for a single archaeological period."""

    period: str
    inscription_count: int = 0
    sites: Dict[str, int] = field(default_factory=dict)
    word_frequencies: Dict[str, int] = field(default_factory=dict)
    logogram_frequencies: Dict[str, int] = field(default_factory=dict)
    admin_marker_counts: Dict[str, int] = field(default_factory=dict)
    admin_marker_tablets: Dict[str, List[str]] = field(default_factory=dict)
    total_tokens: int = 0
    total_words: int = 0
    total_logograms: int = 0
    avg_document_length: float = 0.0
    document_lengths: List[int] = field(default_factory=list)
    unique_words: int = 0
    hapax_count: int = 0  # Words appearing exactly once in this period


@dataclass
class VocabularyTransition:
    """Vocabulary changes between two adjacent periods."""

    from_period: str
    to_period: str
    words_appearing: List[str] = field(default_factory=list)
    words_disappearing: List[str] = field(default_factory=list)
    words_shared: List[str] = field(default_factory=list)
    appearing_count: int = 0
    disappearing_count: int = 0
    shared_count: int = 0
    continuity_ratio: float = 0.0  # shared / union


@dataclass
class StructuralEvolution:
    """Track how administrative structure changes over time."""

    period: str
    kuro_rate: float = 0.0  # Fraction of tablets with KU-RO
    kiro_rate: float = 0.0  # Fraction of tablets with KI-RO
    sara2_rate: float = 0.0  # Fraction of tablets with SA-RA₂
    avg_complexity: float = 0.0  # Average tokens per tablet
    logogram_diversity: int = 0  # Distinct logograms used
    word_diversity: int = 0  # Distinct eligible words used
    type_token_ratio: float = 0.0  # Unique words / total words


class TemporalEvolutionTracker:
    """Tracks evolution of Linear A administrative writing across periods."""

    def __init__(self):
        self.corpus: Dict = {}
        self.inscriptions: Dict = {}
        self.period_profiles: Dict[str, PeriodProfile] = {}
        self.vocabulary_transitions: List[VocabularyTransition] = []
        self.structural_evolution: List[StructuralEvolution] = []

    def load_corpus(self) -> bool:
        """Load corpus data from JSON."""
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _get_period(self, tablet_data: Dict) -> str:
        """Extract period from tablet data, returning empty string if absent."""
        ctx = tablet_data.get("context", "")
        if isinstance(ctx, str):
            return ctx.strip()
        if isinstance(ctx, dict):
            return ctx.get("period", "").strip()
        return ""

    def _get_site(self, tablet_data: Dict) -> str:
        """Extract site from tablet data."""
        return tablet_data.get("site", "UNKNOWN")

    def _classify_tokens(self, words: List[str]) -> Dict[str, List[str]]:
        """Classify tokens into categories."""
        result: Dict[str, List[str]] = {
            "eligible_words": [],
            "logograms": [],
            "numbers": [],
            "separators": [],
            "other": [],
        }
        for token in words:
            if _is_separator(token):
                result["separators"].append(token)
            elif _is_numeric(token):
                result["numbers"].append(token)
            elif _is_logogram(token):
                result["logograms"].append(token)
            elif is_hypothesis_eligible_word(token):
                result["eligible_words"].append(normalize_word_token(token))
            else:
                result["other"].append(token)
        return result

    def build_period_profiles(self) -> Dict[str, PeriodProfile]:
        """Build statistical profiles for each period."""
        period_inscriptions: Dict[str, List[tuple]] = defaultdict(list)

        # Group inscriptions by period
        for tablet_id, tablet_data in self.inscriptions.items():
            period = self._get_period(tablet_data)
            if not period:
                period = "UNKNOWN"
            period_inscriptions[period].append((tablet_id, tablet_data))

        # Build profile for each period
        for period, tablets in period_inscriptions.items():
            profile = PeriodProfile(period=period)
            profile.inscription_count = len(tablets)

            site_counter: Counter = Counter()
            word_counter: Counter = Counter()
            logogram_counter: Counter = Counter()
            admin_counts: Dict[str, int] = {m: 0 for m in ADMIN_MARKERS}
            admin_tablets: Dict[str, List[str]] = {m: [] for m in ADMIN_MARKERS}

            for tablet_id, tablet_data in tablets:
                site = self._get_site(tablet_data)
                site_counter[site] += 1

                words = tablet_data.get("transliteratedWords", [])
                classified = self._classify_tokens(words)

                # Document length = non-separator tokens
                doc_length = len(words) - len(classified["separators"])
                profile.document_lengths.append(doc_length)
                profile.total_tokens += len(words)

                # Word frequencies
                for w in classified["eligible_words"]:
                    word_counter[w] += 1
                    profile.total_words += 1

                # Logogram frequencies
                for lg in classified["logograms"]:
                    base = _get_logogram_base(lg)
                    logogram_counter[base] += 1
                    profile.total_logograms += 1

                # Administrative markers
                for marker in ADMIN_MARKERS:
                    if marker in words:
                        admin_counts[marker] += 1
                        admin_tablets[marker].append(tablet_id)

            profile.sites = dict(site_counter.most_common())
            profile.word_frequencies = dict(word_counter.most_common())
            profile.logogram_frequencies = dict(logogram_counter.most_common())
            profile.admin_marker_counts = admin_counts
            profile.admin_marker_tablets = admin_tablets
            profile.unique_words = len(word_counter)
            profile.hapax_count = sum(1 for c in word_counter.values() if c == 1)

            if profile.document_lengths:
                profile.avg_document_length = sum(profile.document_lengths) / len(
                    profile.document_lengths
                )

            self.period_profiles[period] = profile

        return self.period_profiles

    def compute_vocabulary_transitions(self) -> List[VocabularyTransition]:
        """Compute vocabulary changes between adjacent periods."""
        self.vocabulary_transitions = []

        # Get ordered periods that actually have data
        ordered = [p for p in PERIOD_ORDER if p in self.period_profiles]

        for i in range(len(ordered) - 1):
            from_period = ordered[i]
            to_period = ordered[i + 1]

            from_vocab = set(self.period_profiles[from_period].word_frequencies.keys())
            to_vocab = set(self.period_profiles[to_period].word_frequencies.keys())

            shared = from_vocab & to_vocab
            appearing = to_vocab - from_vocab
            disappearing = from_vocab - to_vocab
            union = from_vocab | to_vocab

            transition = VocabularyTransition(
                from_period=from_period,
                to_period=to_period,
                words_appearing=sorted(appearing),
                words_disappearing=sorted(disappearing),
                words_shared=sorted(shared),
                appearing_count=len(appearing),
                disappearing_count=len(disappearing),
                shared_count=len(shared),
                continuity_ratio=len(shared) / len(union) if union else 0.0,
            )
            self.vocabulary_transitions.append(transition)

        return self.vocabulary_transitions

    def compute_structural_evolution(self) -> List[StructuralEvolution]:
        """Compute how administrative structure evolves across periods."""
        self.structural_evolution = []

        ordered = [p for p in PERIOD_ORDER if p in self.period_profiles]

        for period in ordered:
            profile = self.period_profiles[period]
            n = profile.inscription_count

            if n == 0:
                continue

            evo = StructuralEvolution(
                period=period,
                kuro_rate=profile.admin_marker_counts.get("KU-RO", 0) / n,
                kiro_rate=profile.admin_marker_counts.get("KI-RO", 0) / n,
                sara2_rate=profile.admin_marker_counts.get("SA-RA\u2082", 0) / n,
                avg_complexity=profile.avg_document_length,
                logogram_diversity=len(profile.logogram_frequencies),
                word_diversity=profile.unique_words,
                type_token_ratio=(
                    profile.unique_words / profile.total_words if profile.total_words > 0 else 0.0
                ),
            )
            self.structural_evolution.append(evo)

        return self.structural_evolution

    def analyze_all(self) -> Dict[str, Any]:
        """Run full temporal evolution analysis."""
        self.build_period_profiles()
        self.compute_vocabulary_transitions()
        self.compute_structural_evolution()

        return {
            "profiles": self.period_profiles,
            "transitions": self.vocabulary_transitions,
            "evolution": self.structural_evolution,
        }

    def analyze_period(self, period: str) -> Optional[PeriodProfile]:
        """Analyze a single period in detail."""
        if not self.period_profiles:
            self.build_period_profiles()

        return self.period_profiles.get(period)

    # --- Printing ---

    def print_period_summary(self, profile: PeriodProfile):
        """Print detailed summary for a single period."""
        print(f"\n{'=' * 70}")
        print(f"PERIOD: {profile.period}")
        print(f"{'=' * 70}")
        print(f"  Inscriptions: {profile.inscription_count}")
        print(f"  Total tokens: {profile.total_tokens}")
        print(f"  Eligible words (tokens): {profile.total_words}")
        print(f"  Unique words (types): {profile.unique_words}")
        print(f"  Hapax legomena: {profile.hapax_count}")
        print(f"  Avg document length: {profile.avg_document_length:.1f} tokens")

        if profile.total_words > 0:
            ttr = profile.unique_words / profile.total_words
            print(f"  Type-token ratio: {ttr:.3f}")

        print(f"\n  Sites ({len(profile.sites)}):")
        for site, count in profile.sites.items():
            print(f"    {site}: {count}")

        print("\n  Administrative markers:")
        for marker in ADMIN_MARKERS:
            count = profile.admin_marker_counts.get(marker, 0)
            rate = count / profile.inscription_count if profile.inscription_count > 0 else 0
            tablets = profile.admin_marker_tablets.get(marker, [])
            tablet_str = (
                f" [{', '.join(tablets[:5])}{'...' if len(tablets) > 5 else ''}]" if tablets else ""
            )
            print(f"    {marker}: {count} ({rate:.1%}){tablet_str}")

        print(f"\n  Top logograms ({len(profile.logogram_frequencies)}):")
        for lg, count in list(profile.logogram_frequencies.items())[:10]:
            print(f"    {lg}: {count}")

        print(f"\n  Top words ({profile.unique_words} unique):")
        for word, count in list(profile.word_frequencies.items())[:15]:
            print(f"    {word}: {count}")

    def print_full_summary(self):
        """Print summary across all periods."""
        print(f"\n{'=' * 70}")
        print("TEMPORAL EVOLUTION SUMMARY")
        print(f"{'=' * 70}")

        # Period counts and site distributions
        ordered = [p for p in PERIOD_ORDER if p in self.period_profiles]
        unknown = self.period_profiles.get("UNKNOWN")

        print(f"\n  Periods with data: {len(ordered)}")
        if unknown:
            print(f"  Inscriptions without period: {unknown.inscription_count}")

        print("\n  --- Period Counts & Sites ---")
        for period in ordered:
            profile = self.period_profiles[period]
            sites = ", ".join(f"{s}({c})" for s, c in list(profile.sites.items())[:5])
            more = f" +{len(profile.sites) - 5} more" if len(profile.sites) > 5 else ""
            n = profile.inscription_count
            print(f"  {period:12s}: {n:5d} inscriptions | sites: {sites}{more}")

        # Vocabulary unique to each period
        print("\n  --- Vocabulary Unique to Each Period ---")
        all_words_by_period: Dict[str, Set[str]] = {}
        for period in ordered:
            all_words_by_period[period] = set(self.period_profiles[period].word_frequencies.keys())

        for period in ordered:
            others = set()
            for p2 in ordered:
                if p2 != period:
                    others |= all_words_by_period[p2]
            unique = all_words_by_period[period] - others
            if unique:
                unique_sorted = sorted(unique)
                display = ", ".join(unique_sorted[:10])
                more = f" +{len(unique_sorted) - 10} more" if len(unique_sorted) > 10 else ""
                print(f"  {period:12s}: {len(unique):3d} unique | {display}{more}")
            else:
                print(f"  {period:12s}:   0 unique")

        # Vocabulary shared across all periods
        print("\n  --- Vocabulary Shared Across Periods ---")
        if len(ordered) >= 2:
            universal = all_words_by_period[ordered[0]].copy()
            for period in ordered[1:]:
                universal &= all_words_by_period[period]
            if universal:
                print(f"  Shared across all {len(ordered)} periods ({len(universal)} words):")
                for w in sorted(universal):
                    print(f"    {w}")
            else:
                print(f"  No words shared across all {len(ordered)} periods")

            # Pairwise shared
            for i in range(len(ordered) - 1):
                p1, p2 = ordered[i], ordered[i + 1]
                shared = all_words_by_period[p1] & all_words_by_period[p2]
                print(f"  {p1} -> {p2}: {len(shared)} shared words")

        # Administrative marker evolution
        print("\n  --- Administrative Marker Evolution ---")
        sara2 = "SA-RA\u2082"
        header = f"  {'Period':12s} | {'KU-RO':>10s} | {'KI-RO':>10s} | {sara2:>10s} | {'N':>5s}"
        print(header)
        print(f"  {'-' * len(header.strip())}")
        for period in ordered:
            profile = self.period_profiles[period]
            n = profile.inscription_count
            kuro = profile.admin_marker_counts.get("KU-RO", 0)
            kiro = profile.admin_marker_counts.get("KI-RO", 0)
            sara = profile.admin_marker_counts.get("SA-RA\u2082", 0)
            kuro_pct = f"{kuro}({kuro / n:.0%})" if n > 0 else "0"
            kiro_pct = f"{kiro}({kiro / n:.0%})" if n > 0 else "0"
            sara_pct = f"{sara}({sara / n:.0%})" if n > 0 else "0"
            print(f"  {period:12s} | {kuro_pct:>10s} | {kiro_pct:>10s} | {sara_pct:>10s} | {n:5d}")

        # Statistical summary
        print("\n  --- Statistical Summary ---")
        total_inscriptions = sum(self.period_profiles[p].inscription_count for p in ordered)
        total_words = sum(self.period_profiles[p].total_words for p in ordered)
        total_unique = len(set().union(*(all_words_by_period[p] for p in ordered)))
        print(f"  Total inscriptions (with period): {total_inscriptions}")
        print(f"  Total word tokens: {total_words}")
        print(f"  Total unique words: {total_unique}")

        if self.structural_evolution:
            print("\n  --- Complexity Evolution ---")
            for evo in self.structural_evolution:
                print(
                    f"  {evo.period:12s}: "
                    f"avg_len={evo.avg_complexity:6.1f} | "
                    f"word_types={evo.word_diversity:4d} | "
                    f"logo_types={evo.logogram_diversity:3d} | "
                    f"TTR={evo.type_token_ratio:.3f}"
                )

    def print_vocabulary_transitions(self):
        """Print vocabulary transition details."""
        print(f"\n{'=' * 70}")
        print("VOCABULARY TRANSITIONS")
        print(f"{'=' * 70}")

        if not self.vocabulary_transitions:
            print("  No transitions computed (need >= 2 periods with data)")
            return

        for trans in self.vocabulary_transitions:
            print(f"\n  {trans.from_period} -> {trans.to_period}:")
            print(f"    Continuity ratio: {trans.continuity_ratio:.3f}")
            print(f"    Shared: {trans.shared_count}")
            print(f"    Appearing: {trans.appearing_count}")
            print(f"    Disappearing: {trans.disappearing_count}")

            if trans.words_appearing:
                display = ", ".join(trans.words_appearing[:15])
                more = (
                    f" +{len(trans.words_appearing) - 15} more"
                    if len(trans.words_appearing) > 15
                    else ""
                )
                print(f"    New words: {display}{more}")

            if trans.words_disappearing:
                display = ", ".join(trans.words_disappearing[:15])
                more = (
                    f" +{len(trans.words_disappearing) - 15} more"
                    if len(trans.words_disappearing) > 15
                    else ""
                )
                print(f"    Lost words: {display}{more}")

    def print_structural_evolution(self):
        """Print administrative structure evolution."""
        print(f"\n{'=' * 70}")
        print("STRUCTURAL EVOLUTION")
        print(f"{'=' * 70}")

        if not self.structural_evolution:
            print("  No structural evolution data computed")
            return

        sara2_pct = "SA-RA\u2082%"
        print(
            f"\n  {'Period':12s} | {'KU-RO%':>7s} | {'KI-RO%':>7s} | {sara2_pct:>8s} | "
            f"{'AvgLen':>7s} | {'Words':>6s} | {'Logos':>6s} | {'TTR':>6s}"
        )
        print(f"  {'-' * 80}")
        for evo in self.structural_evolution:
            print(
                f"  {evo.period:12s} | {evo.kuro_rate:6.1%} | {evo.kiro_rate:6.1%} | "
                f"{evo.sara2_rate:7.1%} | {evo.avg_complexity:7.1f} | "
                f"{evo.word_diversity:6d} | {evo.logogram_diversity:6d} | "
                f"{evo.type_token_ratio:6.3f}"
            )

    # --- JSON Output ---

    def save_results(self, output_path: str):
        """Save full results to JSON."""
        ordered = [p for p in PERIOD_ORDER if p in self.period_profiles]

        # Build serializable profiles
        profiles_out = {}
        for period in ordered:
            profile = self.period_profiles[period]
            profiles_out[period] = {
                "period": profile.period,
                "inscription_count": profile.inscription_count,
                "sites": profile.sites,
                "word_frequencies": profile.word_frequencies,
                "logogram_frequencies": profile.logogram_frequencies,
                "admin_marker_counts": profile.admin_marker_counts,
                "admin_marker_tablets": profile.admin_marker_tablets,
                "total_tokens": profile.total_tokens,
                "total_words": profile.total_words,
                "total_logograms": profile.total_logograms,
                "avg_document_length": round(profile.avg_document_length, 2),
                "unique_words": profile.unique_words,
                "hapax_count": profile.hapax_count,
            }

        # Include UNKNOWN if present
        if "UNKNOWN" in self.period_profiles:
            profile = self.period_profiles["UNKNOWN"]
            profiles_out["UNKNOWN"] = {
                "period": "UNKNOWN",
                "inscription_count": profile.inscription_count,
                "sites": profile.sites,
                "total_tokens": profile.total_tokens,
                "total_words": profile.total_words,
                "unique_words": profile.unique_words,
                "admin_marker_counts": profile.admin_marker_counts,
            }

        # Build serializable transitions
        transitions_out = [
            {
                "from_period": t.from_period,
                "to_period": t.to_period,
                "appearing_count": t.appearing_count,
                "disappearing_count": t.disappearing_count,
                "shared_count": t.shared_count,
                "continuity_ratio": round(t.continuity_ratio, 4),
                "words_appearing": t.words_appearing,
                "words_disappearing": t.words_disappearing,
                "words_shared": t.words_shared,
            }
            for t in self.vocabulary_transitions
        ]

        # Build serializable evolution
        evolution_out = [
            {
                "period": e.period,
                "kuro_rate": round(e.kuro_rate, 4),
                "kiro_rate": round(e.kiro_rate, 4),
                "sara2_rate": round(e.sara2_rate, 4),
                "avg_complexity": round(e.avg_complexity, 2),
                "logogram_diversity": e.logogram_diversity,
                "word_diversity": e.word_diversity,
                "type_token_ratio": round(e.type_token_ratio, 4),
            }
            for e in self.structural_evolution
        ]

        # Compute cross-period vocabulary sets for JSON
        all_words_by_period: Dict[str, Set[str]] = {}
        for period in ordered:
            all_words_by_period[period] = set(self.period_profiles[period].word_frequencies.keys())

        unique_per_period = {}
        for period in ordered:
            others = set()
            for p2 in ordered:
                if p2 != period:
                    others |= all_words_by_period.get(p2, set())
            unique = all_words_by_period[period] - others
            unique_per_period[period] = sorted(unique)

        # Universal vocabulary
        universal: Set[str] = set()
        if ordered:
            universal = all_words_by_period[ordered[0]].copy()
            for period in ordered[1:]:
                universal &= all_words_by_period[period]

        output = {
            "metadata": {
                "tool": "temporal_evolution_tracker.py",
                "periods_analyzed": len(ordered),
                "total_inscriptions": sum(
                    self.period_profiles[p].inscription_count for p in ordered
                ),
                "period_order": ordered,
            },
            "period_profiles": profiles_out,
            "vocabulary_transitions": transitions_out,
            "structural_evolution": evolution_out,
            "vocabulary_unique_per_period": unique_per_period,
            "vocabulary_universal": sorted(universal),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Temporal Evolution Tracker - analyze Linear A across archaeological periods"
    )
    parser.add_argument("--all", action="store_true", help="Full analysis across all periods")
    parser.add_argument("--period", type=str, help="Analyze a specific period (e.g., LMIB, MMIII)")
    parser.add_argument(
        "--vocabulary", action="store_true", help="Focus on vocabulary changes between periods"
    )
    parser.add_argument(
        "--structure", action="store_true", help="Focus on administrative structure changes"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help=f"Output JSON path (default: {DEFAULT_OUTPUT})",
    )

    args = parser.parse_args()

    # Default to --all if no mode specified
    if not any([args.all, args.period, args.vocabulary, args.structure]):
        args.all = True

    tracker = TemporalEvolutionTracker()
    if not tracker.load_corpus():
        sys.exit(1)

    if args.period:
        # Single period analysis
        tracker.build_period_profiles()
        profile = tracker.analyze_period(args.period)
        if profile:
            tracker.print_period_summary(profile)
        else:
            available = [p for p in PERIOD_ORDER if p in tracker.period_profiles]
            print(f"Period '{args.period}' not found. Available: {', '.join(available)}")
            sys.exit(1)

    elif args.vocabulary:
        # Vocabulary transition focus
        tracker.build_period_profiles()
        tracker.compute_vocabulary_transitions()
        tracker.print_vocabulary_transitions()

    elif args.structure:
        # Structural evolution focus
        tracker.build_period_profiles()
        tracker.compute_structural_evolution()
        tracker.print_structural_evolution()

    else:
        # Full analysis
        tracker.analyze_all()
        tracker.print_full_summary()

    # Save results (always run full analysis for JSON)
    if args.output:
        if not tracker.vocabulary_transitions:
            tracker.build_period_profiles()
            tracker.compute_vocabulary_transitions()
            tracker.compute_structural_evolution()
        tracker.save_results(args.output)


if __name__ == "__main__":
    main()
