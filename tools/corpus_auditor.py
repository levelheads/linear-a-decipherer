#!/usr/bin/env python3
"""
Corpus Auditor for Linear A

Implements three audit functions suggested by quantitative corpus linguistics:
1. Arithmetic validation: Verify KU-RO totals match preceding amounts
2. Token-commodity co-occurrence: Build bipartite graph of words and logograms
3. Function word analysis: Positional study of candidates like TE

These analyses work WITHOUT language assumptions - pure structural/mathematical.

Usage:
    python tools/corpus_auditor.py --totals          # Arithmetic validation
    python tools/corpus_auditor.py --cooccurrence    # Token-commodity matrix
    python tools/corpus_auditor.py --function-word TE  # Positional analysis
    python tools/corpus_auditor.py --all             # Full audit report

Attribution:
    Part of Linear A Decipherment Project
    Implements First Principles methodology (structure before language)
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from fractions import Fraction


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
OUTPUT_DIR = DATA_DIR / "audit"


# ============================================================================
# CONSTANTS
# ============================================================================

# Known commodity logograms
COMMODITY_LOGOGRAMS = {
    "GRA",
    "VIN",
    "OLE",
    "OLIV",
    "FIC",
    "FAR",
    "CYP",  # goods
    "OVI",
    "CAP",
    "SUS",
    "BOS",  # animals
    "VIR",
    "MUL",  # people
    "TELA",  # textiles
    # Ligature variants
    "OLE+U",
    "OLE+A",
    "OLE+E",
    "OLE+KI",
    "OLE+MI",
    "OLE+TU",
    "OLE+DI",
    "VIN+A",
    "VIN+DU",
    "GRA+PA",
    "GRA+A",
}

# Administrative function words (candidates for positional analysis)
FUNCTION_WORD_CANDIDATES = {"TE", "KU-RO", "KI-RO", "SA-RA₂", "A-DU", "DA-RE"}

# Fraction mappings (Unicode superscript → Fraction object)
FRACTION_MAP = {
    "¹⁄₂": Fraction(1, 2),
    "½": Fraction(1, 2),
    "¹⁄₄": Fraction(1, 4),
    "¼": Fraction(1, 4),
    "³⁄₄": Fraction(3, 4),
    "¾": Fraction(3, 4),
    "¹⁄₃": Fraction(1, 3),
    "⅓": Fraction(1, 3),
    "²⁄₃": Fraction(2, 3),
    "⅔": Fraction(2, 3),
    "¹⁄₈": Fraction(1, 8),
    "⅛": Fraction(1, 8),
    "³⁄₈": Fraction(3, 8),
    "⅜": Fraction(3, 8),
    "¹⁄₁₆": Fraction(1, 16),
    "~¹⁄₆": Fraction(1, 6),  # approximate
    "¹⁄₆": Fraction(1, 6),
    "J": Fraction(1, 4),  # AB 164
    "E": Fraction(1, 2),  # AB 162
    "F": Fraction(1, 3),  # AB 163
    "K": Fraction(1, 8),  # AB 165
    "L": Fraction(1, 16),  # AB 166
}


# ============================================================================
# DATA CLASSES
# ============================================================================


@dataclass
class TotalValidation:
    """Result of validating a KU-RO total."""

    tablet_id: str
    kuro_value: Fraction
    computed_sum: Fraction
    items: List[Tuple[str, Fraction]]  # (entity, amount)
    matches: bool
    difference: Fraction
    confidence: str  # VERIFIED, PARTIAL, INCOMPLETE, MISMATCH
    notes: str = ""


@dataclass
class CooccurrenceData:
    """Token-commodity co-occurrence statistics."""

    token: str
    commodities: Dict[str, int]  # commodity → count
    total_occurrences: int
    primary_commodity: str
    specificity: float  # 0-1, how focused on one commodity


@dataclass
class PositionalAnalysis:
    """Positional analysis for a function word candidate."""

    word: str
    total_occurrences: int
    position_distribution: Dict[str, int]  # INITIAL, MEDIAL, FINAL
    line_position_entropy: float
    left_neighbors: Counter
    right_neighbors: Counter
    scribe_distribution: Dict[str, int]
    site_distribution: Dict[str, int]
    role_hypothesis: str


# ============================================================================
# CORPUS AUDITOR
# ============================================================================


class CorpusAuditor:
    """
    Audits Linear A corpus for structural patterns and arithmetic consistency.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = None
        self.inscriptions = {}

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_corpus(self) -> bool:
        """Load the corpus data."""
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _parse_number(self, token: str) -> Optional[Fraction]:
        """Parse a token as a number (integer or fraction)."""
        # Check fraction map first
        if token in FRACTION_MAP:
            return FRACTION_MAP[token]

        # Try integer
        try:
            return Fraction(int(token))
        except ValueError:
            pass

        # Try parsing "X Y/Z" format
        match = re.match(r"^(\d+)\s+(\d+)/(\d+)$", token)
        if match:
            whole, num, denom = int(match.group(1)), int(match.group(2)), int(match.group(3))
            return Fraction(whole * denom + num, denom)

        # Try parsing "X/Y" format
        match = re.match(r"^(\d+)/(\d+)$", token)
        if match:
            return Fraction(int(match.group(1)), int(match.group(2)))

        return None

    def _is_logogram(self, token: str) -> bool:
        """Check if token is a commodity logogram."""
        # Direct match
        if token in COMMODITY_LOGOGRAMS:
            return True
        # Check for ligature (contains +)
        if "+" in token:
            base = token.split("+")[0]
            return base in {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}
        return False

    def _is_word(self, token: str) -> bool:
        """Check if token is a syllabic word (not number, divider, newline, logogram)."""
        if token in {"\n", "𐄁", "", " "}:
            return False
        if self._parse_number(token) is not None:
            return False
        if self._is_logogram(token):
            return False
        if token.startswith('"'):
            return False
        if token == "*":  # Reject bare asterisk only
            return False
        # *NNN-XX patterns are valid entity names (undeciphered sign codes) - allow them
        return True

    def _extract_site(self, tablet_id: str) -> str:
        """Extract site code from tablet ID."""
        match = re.match(r"^([A-Z]+)", tablet_id)
        return match.group(1) if match else "UNKNOWN"

    # ========================================================================
    # 1. ARITHMETIC VALIDATION
    # ========================================================================

    def validate_totals(self) -> List[TotalValidation]:
        """
        Validate all tablets with KU-RO totals.

        For each tablet containing KU-RO:
        1. Find position of KU-RO
        2. Sum all preceding amounts
        3. Compare to KU-RO value
        4. Report match/mismatch
        """
        results = []

        for tablet_id, data in self.inscriptions.items():
            words = data.get("transliteratedWords", [])
            if "KU-RO" not in words:
                continue

            self.log(f"Validating {tablet_id}...")

            # Find KU-RO position(s)
            kuro_indices = [i for i, w in enumerate(words) if w == "KU-RO"]

            for kuro_idx in kuro_indices:
                # Get KU-RO value (next numeric tokens)
                kuro_value = Fraction(0)
                for i in range(kuro_idx + 1, min(kuro_idx + 4, len(words))):
                    if words[i] == "\n":
                        break
                    num = self._parse_number(words[i])
                    if num is not None:
                        kuro_value += num

                if kuro_value == 0:
                    continue  # No value found

                # Sum preceding amounts
                items = []
                computed_sum = Fraction(0)
                current_entity = None
                current_amount = Fraction(0)

                for i in range(kuro_idx):
                    token = words[i]

                    if token == "\n":
                        if current_entity and current_amount > 0:
                            items.append((current_entity, current_amount))
                            computed_sum += current_amount
                        current_entity = None
                        current_amount = Fraction(0)
                    elif self._is_word(token) and not self._is_logogram(token):
                        # This might be an entity name
                        if current_entity is None:
                            current_entity = token
                    else:
                        num = self._parse_number(token)
                        if num is not None:
                            current_amount += num

                # Don't forget last item before KU-RO
                if current_entity and current_amount > 0:
                    items.append((current_entity, current_amount))
                    computed_sum += current_amount

                # Determine status
                difference = abs(kuro_value - computed_sum)
                if difference == 0:
                    matches = True
                    confidence = "VERIFIED"
                elif difference <= Fraction(1, 4):
                    matches = False
                    confidence = "PARTIAL"  # Small discrepancy (rounding?)
                elif len(items) == 0:
                    matches = False
                    confidence = "INCOMPLETE"  # Can't verify without items
                else:
                    matches = False
                    confidence = "MISMATCH"

                results.append(
                    TotalValidation(
                        tablet_id=tablet_id,
                        kuro_value=kuro_value,
                        computed_sum=computed_sum,
                        items=items,
                        matches=matches,
                        difference=difference,
                        confidence=confidence,
                        notes=f"{len(items)} items parsed",
                    )
                )

        return results

    def print_totals_report(self, results: List[TotalValidation]):
        """Print arithmetic validation report."""
        print("\n" + "=" * 70)
        print("ARITHMETIC VALIDATION REPORT")
        print("=" * 70)

        # Summary
        verified = sum(1 for r in results if r.confidence == "VERIFIED")
        partial = sum(1 for r in results if r.confidence == "PARTIAL")
        mismatch = sum(1 for r in results if r.confidence == "MISMATCH")
        incomplete = sum(1 for r in results if r.confidence == "INCOMPLETE")

        print(f"\nSummary: {len(results)} KU-RO instances analyzed")
        print(
            f"  VERIFIED:   {verified:3d} ({100 * verified / len(results):.1f}%)" if results else ""
        )
        print(
            f"  PARTIAL:    {partial:3d} ({100 * partial / len(results):.1f}%)" if results else ""
        )
        print(
            f"  MISMATCH:   {mismatch:3d} ({100 * mismatch / len(results):.1f}%)" if results else ""
        )
        print(
            f"  INCOMPLETE: {incomplete:3d} ({100 * incomplete / len(results):.1f}%)"
            if results
            else ""
        )

        # Detail on mismatches (most interesting for research)
        if mismatch > 0:
            print("\n--- MISMATCHES (require investigation) ---")
            for r in results:
                if r.confidence == "MISMATCH":
                    print(f"\n{r.tablet_id}:")
                    print(f"  KU-RO value:  {float(r.kuro_value):.4f}")
                    print(f"  Computed sum: {float(r.computed_sum):.4f}")
                    print(f"  Difference:   {float(r.difference):.4f}")
                    print(
                        f"  Items: {r.items[:5]}..." if len(r.items) > 5 else f"  Items: {r.items}"
                    )

        # Fraction value inference
        print("\n--- FRACTION CONSISTENCY CHECK ---")
        fraction_tablets = [
            r
            for r in results
            if r.kuro_value != int(r.kuro_value) or r.computed_sum != int(r.computed_sum)
        ]
        print(f"Tablets with fractions: {len(fraction_tablets)}")
        if fraction_tablets:
            verified_fracs = [r for r in fraction_tablets if r.confidence == "VERIFIED"]
            print(f"  Verified with fractions: {len(verified_fracs)}")
            print("  (These constrain fraction sign values)")

    # ========================================================================
    # 2. TOKEN-COMMODITY CO-OCCURRENCE
    # ========================================================================

    def build_cooccurrence(self) -> Dict[str, CooccurrenceData]:
        """
        Build token-commodity co-occurrence matrix.

        For each word, count how often it appears with each commodity logogram.
        High specificity = word strongly associated with one commodity.
        """
        # token -> commodity -> count
        cooccurrence = defaultdict(lambda: defaultdict(int))
        token_counts = Counter()

        for tablet_id, data in self.inscriptions.items():
            words = data.get("transliteratedWords", [])

            # Process line by line
            lines = []
            current_line = []
            for w in words:
                if w == "\n":
                    if current_line:
                        lines.append(current_line)
                    current_line = []
                else:
                    current_line.append(w)
            if current_line:
                lines.append(current_line)

            # For each line, find commodities and tokens
            for line in lines:
                commodities_in_line = [w for w in line if self._is_logogram(w)]
                tokens_in_line = [w for w in line if self._is_word(w)]

                for token in tokens_in_line:
                    token_counts[token] += 1
                    for commodity in commodities_in_line:
                        # Normalize ligatures to base
                        base_commodity = commodity.split("+")[0] if "+" in commodity else commodity
                        cooccurrence[token][base_commodity] += 1

        # Build results
        results = {}
        for token, commodities in cooccurrence.items():
            total = token_counts[token]
            if total < 2:  # Skip hapax
                continue

            primary = max(commodities.keys(), key=lambda c: commodities[c]) if commodities else ""
            primary_count = commodities.get(primary, 0)
            specificity = primary_count / sum(commodities.values()) if commodities else 0

            results[token] = CooccurrenceData(
                token=token,
                commodities=dict(commodities),
                total_occurrences=total,
                primary_commodity=primary,
                specificity=specificity,
            )

        return results

    def print_cooccurrence_report(self, data: Dict[str, CooccurrenceData]):
        """Print token-commodity co-occurrence analysis."""
        print("\n" + "=" * 70)
        print("TOKEN-COMMODITY CO-OCCURRENCE ANALYSIS")
        print("=" * 70)

        # Sort by total occurrences
        sorted_tokens = sorted(data.values(), key=lambda x: x.total_occurrences, reverse=True)

        print(f"\nTokens analyzed: {len(sorted_tokens)}")

        # High specificity tokens (likely commodity-specific terms)
        print("\n--- HIGH SPECIFICITY (>80% one commodity) ---")
        print("These tokens strongly associate with one commodity type:\n")
        high_spec = [t for t in sorted_tokens if t.specificity > 0.8 and t.total_occurrences >= 3]
        for t in high_spec[:20]:
            print(
                f"  {t.token:20s} → {t.primary_commodity:6s} "
                f"({t.specificity:.0%}, n={t.total_occurrences})"
            )

        # Low specificity tokens (likely function words or general terms)
        print("\n--- LOW SPECIFICITY (<40% any commodity) ---")
        print("These tokens appear across multiple commodity types:\n")
        low_spec = [
            t for t in sorted_tokens if t.specificity < 0.4 and sum(t.commodities.values()) >= 3
        ]
        for t in low_spec[:15]:
            comm_str = ", ".join(
                f"{c}:{n}" for c, n in sorted(t.commodities.items(), key=lambda x: -x[1])[:3]
            )
            print(f"  {t.token:20s} → [{comm_str}] (n={t.total_occurrences})")

        # Commodity distribution summary
        print("\n--- COMMODITY FREQUENCY ---")
        commodity_totals = defaultdict(int)
        for t in data.values():
            for c, n in t.commodities.items():
                commodity_totals[c] += n
        for c, n in sorted(commodity_totals.items(), key=lambda x: -x[1]):
            print(f"  {c:8s}: {n:4d} associations")

    # ========================================================================
    # 3. FUNCTION WORD ANALYSIS
    # ========================================================================

    def analyze_function_word(self, word: str) -> PositionalAnalysis:
        """
        Analyze positional distribution and context of a function word candidate.

        Measures:
        - Position in line (INITIAL, MEDIAL, FINAL)
        - Left/right neighbors
        - Distribution by scribe and site
        """
        position_dist = Counter()
        left_neighbors = Counter()
        right_neighbors = Counter()
        scribe_dist = Counter()
        site_dist = Counter()
        total = 0

        for tablet_id, data in self.inscriptions.items():
            words = data.get("transliteratedWords", [])
            scribe = data.get("scribe", "Unknown")
            site = self._extract_site(tablet_id)

            # Find word occurrences
            indices = [i for i, w in enumerate(words) if w == word]

            for idx in indices:
                total += 1
                scribe_dist[scribe] += 1
                site_dist[site] += 1

                # Determine line position
                # Find line boundaries
                line_start = idx
                while line_start > 0 and words[line_start - 1] != "\n":
                    line_start -= 1
                line_end = idx
                while line_end < len(words) - 1 and words[line_end + 1] != "\n":
                    line_end += 1

                line_len = line_end - line_start + 1
                pos_in_line = idx - line_start

                if pos_in_line == 0:
                    position_dist["INITIAL"] += 1
                elif pos_in_line == line_len - 1:
                    position_dist["FINAL"] += 1
                else:
                    position_dist["MEDIAL"] += 1

                # Get neighbors (skip newlines)
                left_idx = idx - 1
                while left_idx >= 0 and words[left_idx] == "\n":
                    left_idx -= 1
                if left_idx >= 0:
                    left_neighbors[words[left_idx]] += 1

                right_idx = idx + 1
                while right_idx < len(words) and words[right_idx] == "\n":
                    right_idx += 1
                if right_idx < len(words):
                    right_neighbors[words[right_idx]] += 1

        # Calculate position entropy
        if total > 0:
            import math

            probs = [c / total for c in position_dist.values()]
            entropy = -sum(p * math.log2(p) for p in probs if p > 0)
            max_entropy = math.log2(3)  # 3 positions
            normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        else:
            normalized_entropy = 0

        # Infer role hypothesis
        if position_dist.get("INITIAL", 0) / total > 0.6 if total > 0 else False:
            role = "Header/Topic marker (line-initial)"
        elif position_dist.get("FINAL", 0) / total > 0.6 if total > 0 else False:
            role = "Total/Summary marker (line-final)"
        elif normalized_entropy < 0.5:
            role = "Fixed position function word"
        else:
            role = "Variable position (connector? modifier?)"

        return PositionalAnalysis(
            word=word,
            total_occurrences=total,
            position_distribution=dict(position_dist),
            line_position_entropy=normalized_entropy,
            left_neighbors=left_neighbors,
            right_neighbors=right_neighbors,
            scribe_distribution=dict(scribe_dist),
            site_distribution=dict(site_dist),
            role_hypothesis=role,
        )

    def print_function_word_report(self, analysis: PositionalAnalysis):
        """Print function word positional analysis."""
        print("\n" + "=" * 70)
        print(f"FUNCTION WORD ANALYSIS: {analysis.word}")
        print("=" * 70)

        print(f"\nTotal occurrences: {analysis.total_occurrences}")

        print("\n--- POSITION DISTRIBUTION ---")
        total = analysis.total_occurrences or 1
        for pos in ["INITIAL", "MEDIAL", "FINAL"]:
            count = analysis.position_distribution.get(pos, 0)
            bar = "█" * int(50 * count / total)
            print(f"  {pos:8s}: {count:3d} ({100 * count / total:5.1f}%) {bar}")

        print(f"\nPosition entropy: {analysis.line_position_entropy:.3f} (0=fixed, 1=uniform)")
        print(f"Role hypothesis: {analysis.role_hypothesis}")

        print("\n--- TOP LEFT NEIGHBORS ---")
        for token, count in analysis.left_neighbors.most_common(10):
            if token not in {"\n", "𐄁"}:
                print(f"  {token:20s}: {count}")

        print("\n--- TOP RIGHT NEIGHBORS ---")
        for token, count in analysis.right_neighbors.most_common(10):
            if token not in {"\n", "𐄁"}:
                print(f"  {token:20s}: {count}")

        print("\n--- SITE DISTRIBUTION ---")
        for site, count in sorted(analysis.site_distribution.items(), key=lambda x: -x[1]):
            print(f"  {site:4s}: {count:3d}")

        if len(analysis.scribe_distribution) > 1:
            print("\n--- SCRIBE DISTRIBUTION ---")
            for scribe, count in sorted(analysis.scribe_distribution.items(), key=lambda x: -x[1])[
                :5
            ]:
                if scribe:
                    print(f"  {scribe[:25]:25s}: {count:3d}")

    # ========================================================================
    # MAIN INTERFACE
    # ========================================================================

    def run_full_audit(self) -> Dict:
        """Run all audits and return combined results."""
        print("\n" + "=" * 70)
        print("LINEAR A CORPUS AUDIT")
        print("=" * 70)

        results = {"totals": None, "cooccurrence": None, "function_words": {}}

        # 1. Arithmetic validation
        print("\n[1/3] Running arithmetic validation...")
        totals = self.validate_totals()
        results["totals"] = totals
        self.print_totals_report(totals)

        # 2. Co-occurrence analysis
        print("\n[2/3] Building co-occurrence matrix...")
        coocc = self.build_cooccurrence()
        results["cooccurrence"] = coocc
        self.print_cooccurrence_report(coocc)

        # 3. Function word analysis for key candidates
        print("\n[3/3] Analyzing function words...")
        for word in ["TE", "KU-RO", "KI-RO"]:
            analysis = self.analyze_function_word(word)
            results["function_words"][word] = analysis
            self.print_function_word_report(analysis)

        return results

    def save_results(self, results: Dict, output_path: Path = None):
        """Save audit results to JSON."""
        if output_path is None:
            OUTPUT_DIR.mkdir(exist_ok=True)
            output_path = OUTPUT_DIR / "corpus_audit.json"

        # Convert to serializable format
        output = {
            "metadata": {
                "generated": str(Path(__file__).name),
                "inscriptions_analyzed": len(self.inscriptions),
            },
            "totals_validation": [
                {
                    "tablet_id": r.tablet_id,
                    "kuro_value": float(r.kuro_value),
                    "computed_sum": float(r.computed_sum),
                    "matches": r.matches,
                    "difference": float(r.difference),
                    "confidence": r.confidence,
                    "item_count": len(r.items),
                }
                for r in (results.get("totals") or [])
            ],
            "cooccurrence_summary": {
                token: {
                    "commodities": data.commodities,
                    "total": data.total_occurrences,
                    "primary": data.primary_commodity,
                    "specificity": data.specificity,
                }
                for token, data in list((results.get("cooccurrence") or {}).items())[:100]
            },
            "function_word_analysis": {
                word: {
                    "occurrences": a.total_occurrences,
                    "position_distribution": a.position_distribution,
                    "entropy": a.line_position_entropy,
                    "role_hypothesis": a.role_hypothesis,
                    "top_left_neighbors": dict(a.left_neighbors.most_common(10)),
                    "top_right_neighbors": dict(a.right_neighbors.most_common(10)),
                    "site_distribution": a.site_distribution,
                }
                for word, a in (results.get("function_words") or {}).items()
            },
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Corpus Auditor for Linear A - structural analysis without language assumptions"
    )
    parser.add_argument("--totals", action="store_true", help="Validate KU-RO arithmetic totals")
    parser.add_argument(
        "--cooccurrence", action="store_true", help="Build token-commodity co-occurrence matrix"
    )
    parser.add_argument(
        "--function-word",
        type=str,
        metavar="WORD",
        help="Analyze positional distribution of a function word",
    )
    parser.add_argument(
        "--all", action="store_true", help="Run full audit (totals + cooccurrence + function words)"
    )
    parser.add_argument("--save", action="store_true", help="Save results to JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Default to --all if no specific option given
    if not any([args.totals, args.cooccurrence, args.function_word, args.all]):
        args.all = True

    auditor = CorpusAuditor(verbose=args.verbose)
    if not auditor.load_corpus():
        sys.exit(1)

    results = {}

    if args.all:
        results = auditor.run_full_audit()
    else:
        if args.totals:
            totals = auditor.validate_totals()
            results["totals"] = totals
            auditor.print_totals_report(totals)

        if args.cooccurrence:
            coocc = auditor.build_cooccurrence()
            results["cooccurrence"] = coocc
            auditor.print_cooccurrence_report(coocc)

        if args.function_word:
            analysis = auditor.analyze_function_word(args.function_word)
            results["function_words"] = {args.function_word: analysis}
            auditor.print_function_word_report(analysis)

    if args.save and results:
        auditor.save_results(results)


if __name__ == "__main__":
    main()
