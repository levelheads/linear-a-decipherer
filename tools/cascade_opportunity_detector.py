#!/usr/bin/env python3
"""
Cascade Opportunity Detector for Linear A

When a new reading is confirmed (e.g., a word's meaning or a sign's value),
this tool computes what other tablets become newly readable as a result.

It works in the forward direction: confirming word X means tablets containing X
gain readiness. If those tablets cross readability thresholds, they may yield
new name links or word identifications that unlock still more tablets —
a transitive cascade of readability gains.

Usage:
    python3 tools/cascade_opportunity_detector.py --word KU-RO --confidence HIGH
    python3 tools/cascade_opportunity_detector.py --word NI --confidence HIGH --threshold 0.5
    python3 tools/cascade_opportunity_detector.py --all-anchors
    python3 tools/cascade_opportunity_detector.py --all-anchors --threshold 0.6
    python3 tools/cascade_opportunity_detector.py --output data/cascade_opportunities.json

Attribution:
    Part of Linear A Decipherment Project
    Highest-leverage planning tool: identifies where confirming one reading
    unlocks the most downstream readability gains.
"""

import json
import argparse
import math
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
from datetime import datetime


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
READINESS_FILE = DATA_DIR / "reading_readiness.json"
DEPENDENCIES_FILE = DATA_DIR / "reading_dependencies.json"
ANCHORS_FILE = DATA_DIR / "anchors.json"
NAMES_FILE = DATA_DIR / "personal_names_comprehensive.json"


# Known commodity logograms (from reading_readiness_scorer.py)
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
    "GRA+QE",
}

FRACTION_TOKENS = {
    "J",
    "E",
    "F",
    "K",
    "L",
    "½",
    "¹⁄₂",
    "¼",
    "¹⁄₄",
    "¾",
    "³⁄₄",
    "⅓",
    "¹⁄₃",
    "⅔",
    "²⁄₃",
    "⅛",
    "¹⁄₈",
    "⅜",
    "³⁄₈",
    "¹⁄₁₆",
    "~¹⁄₆",
    "¹⁄₆",
}

# Administrative function words with known/proposed functions
KNOWN_FUNCTION_WORDS = {
    "KU-RO": "total/summation",
    "KI-RO": "deficit/remainder",
    "TE": "header/topic marker",
    "SA-RA₂": "allocation marker",
    "A-DU": "contributor/sender",
    "DA-RE": "received/transaction verb",
}

# Confidence levels (ordered from lowest to highest)
CONFIDENCE_LEVELS = ["SPECULATIVE", "POSSIBLE", "LOW", "MEDIUM", "PROBABLE", "HIGH", "CERTAIN"]
CONFIDENCE_RANK = {level: i for i, level in enumerate(CONFIDENCE_LEVELS)}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class CascadeOpportunity:
    """A single tablet that gains readability from a confirmed reading."""

    tablet_id: str
    current_readiness: float
    new_readiness: float
    readiness_delta: float
    newly_identified_words: List[str]
    remaining_unknowns: int
    site: str
    cascade_depth: int  # 0 = directly contains word, 1+ = transitive


@dataclass
class CascadeReport:
    """Full report for a single trigger word's cascade effects."""

    trigger_word: str
    trigger_confidence: str
    direct_tablets: int  # tablets directly containing the word
    cascade_tablets: int  # tablets unlocked transitively
    opportunities: List[CascadeOpportunity]
    transitive_chains: List[Dict]  # word -> tablets -> new words -> tablets


# ---------------------------------------------------------------------------
# Token classification helpers (mirrors reading_readiness_scorer.py)
# ---------------------------------------------------------------------------


def _is_number(token: str) -> bool:
    """Check if token is a number or fraction."""
    if token in FRACTION_TOKENS:
        return True
    try:
        int(token)
        return True
    except ValueError:
        pass
    if re.match(r"^\d+$", token):
        return True
    return False


def _is_logogram(token: str) -> bool:
    """Check if token is a commodity logogram."""
    if token in COMMODITY_LOGOGRAMS:
        return True
    if "+" in token:
        base = token.split("+")[0]
        return base in {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}
    return False


def _is_structural(token: str) -> bool:
    """Check if token is a separator or structural element."""
    return token in {"\n", "𐄁", "", " ", "—", ",", ".", "[", "]", "*"}


def _is_syllabic_word(token: str) -> bool:
    """Check if token is a syllabic word (not number, logogram, or structural)."""
    if _is_structural(token):
        return False
    if _is_number(token):
        return False
    if _is_logogram(token):
        return False
    if token.startswith('"'):
        return False
    return True


def _extract_site(tablet_id: str) -> str:
    """Extract site code from tablet ID."""
    match = re.match(r"^([A-Z]+)", tablet_id)
    return match.group(1) if match else "UNKNOWN"


# ---------------------------------------------------------------------------
# Main detector class
# ---------------------------------------------------------------------------


class CascadeOpportunityDetector:
    """
    Detects cascade opportunities: when confirming one reading unlocks
    readability on other tablets.

    Works in the forward direction of the anchor dependency DAG.
    """

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold  # Readiness threshold for "crossable"

        # Data stores
        self.inscriptions: Dict = {}
        self.readiness_cache: Dict[str, float] = {}  # tablet_id -> readiness score
        self.readiness_details: Dict[str, Dict] = {}  # tablet_id -> full ranking entry
        self.readings: Dict = {}  # from reading_dependencies.json
        self.anchors: Dict = {}  # from anchors.json
        self.known_names: Set[str] = set()

        # Derived indexes
        self.word_to_tablets: Dict[str, Set[str]] = defaultdict(set)
        self.tablet_syllabic_words: Dict[str, List[str]] = {}  # tablet_id -> list of syllabic words
        self.identified_words: Set[str] = set()  # all words with some identification

    def load_data(self) -> bool:
        """Load all required data files."""
        # --- Corpus (required) ---
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                corpus = json.load(f)
            self.inscriptions = corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions from corpus")
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

        # --- Build word-to-tablet index ---
        for tablet_id, tablet_data in self.inscriptions.items():
            tokens = tablet_data.get("transliteratedWords", [])
            syllabic = [t for t in tokens if _is_syllabic_word(t)]
            self.tablet_syllabic_words[tablet_id] = syllabic
            for word in set(syllabic):
                self.word_to_tablets[word].add(tablet_id)

        # --- Reading readiness (optional but strongly desired) ---
        try:
            with open(READINESS_FILE, "r", encoding="utf-8") as f:
                readiness_data = json.load(f)
            rankings = readiness_data.get("rankings", [])
            for entry in rankings:
                tid = entry.get("tablet_id", "")
                self.readiness_cache[tid] = entry.get("readiness_score", 0.0)
                self.readiness_details[tid] = entry
            print(f"Loaded readiness scores for {len(self.readiness_cache)} tablets")
        except FileNotFoundError:
            print("Warning: reading_readiness.json not found — will compute scores inline")
        except Exception as e:
            print(f"Warning: Error loading readiness data: {e}")

        # --- Reading dependencies (optional) ---
        try:
            with open(DEPENDENCIES_FILE, "r", encoding="utf-8") as f:
                dep_data = json.load(f)
            self.readings = dep_data.get("readings", {})
            print(f"Loaded {len(self.readings)} reading dependencies")
        except FileNotFoundError:
            print("Warning: reading_dependencies.json not found")
        except Exception as e:
            print(f"Warning: Error loading dependencies: {e}")

        # --- Anchors (optional) ---
        try:
            with open(ANCHORS_FILE, "r", encoding="utf-8") as f:
                anchor_data = json.load(f)
            self.anchors = anchor_data.get("anchors", {})
            print(f"Loaded {len(self.anchors)} anchors")
        except FileNotFoundError:
            print("Warning: anchors.json not found")
        except Exception as e:
            print(f"Warning: Error loading anchors: {e}")

        # --- Personal names (optional) ---
        try:
            with open(NAMES_FILE, "r", encoding="utf-8") as f:
                names_data = json.load(f)
            names = names_data.get("names", {})
            if isinstance(names, dict):
                self.known_names = set(names.keys())
            elif isinstance(names, list):
                self.known_names = {
                    n.get("name", n.get("word", "")) for n in names if isinstance(n, dict)
                }
            print(f"Loaded {len(self.known_names)} personal names")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Warning: Error loading personal names: {e}")

        # --- Build identified-words set ---
        self._build_identified_words()

        return True

    def _build_identified_words(self):
        """Build the set of all words that have some identification."""
        # Function words
        self.identified_words.update(KNOWN_FUNCTION_WORDS.keys())

        # Reading dependencies (words with readings)
        for reading_id in self.readings:
            self.identified_words.add(reading_id)

        # Known personal names
        self.identified_words.update(self.known_names)

        # Words from readiness details with non-unknown categories
        for tablet_id, details in self.readiness_details.items():
            for wd in details.get("word_detail", []):
                if wd.get("category") not in ("unknown",):
                    self.identified_words.add(wd.get("word", ""))

        print(f"Total identified words: {len(self.identified_words)}")

    def _is_word_identified(self, word: str) -> bool:
        """Check if a word is currently identified (anchored, named, formula, etc.)."""
        if word in self.identified_words:
            return True
        # Also check case-insensitive
        if word.upper() in self.identified_words:
            return True
        return False

    def _compute_readiness_inline(
        self, tablet_id: str, extra_identified: Optional[Set[str]] = None
    ) -> Tuple[float, int, int, List[str]]:
        """
        Compute readiness score for a tablet inline.

        Returns (score, total_syllabic, unknown_count, unknown_words).

        This mirrors the logic in reading_readiness_scorer.py but is
        self-contained to avoid import issues.
        """
        syllabic = self.tablet_syllabic_words.get(tablet_id, [])
        if not syllabic:
            return (0.0, 0, 0, [])

        tokens = self.inscriptions.get(tablet_id, {}).get("transliteratedWords", [])
        logogram_count = sum(1 for t in tokens if _is_logogram(t))
        number_count = sum(1 for t in tokens if _is_number(t))

        total_words = len(syllabic)
        unknown_words = []
        for w in syllabic:
            is_known = self._is_word_identified(w)
            if extra_identified and not is_known:
                is_known = w in extra_identified or w.upper() in extra_identified
            if not is_known:
                unknown_words.append(w)

        unknown = len(unknown_words)
        identified = total_words - unknown

        # Coverage component (0-1)
        coverage = identified / total_words if total_words > 0 else 0

        # Arithmetic component — check for KU-RO
        has_kuro = "KU-RO" in set(syllabic)
        arith = 0.2 if has_kuro else 0.0
        # Use cached status if available
        details = self.readiness_details.get(tablet_id, {})
        arith_status = details.get("arithmetic_status", "")
        arith_scores = {
            "VERIFIED": 1.0,
            "PARTIAL": 0.7,
            "MISMATCH": 0.3,
            "INCOMPLETE": 0.1,
            "NO_KURO": 0.2,
            "NOT_AUDITED": 0.15,
            "NO_DATA": 0.0,
        }
        if arith_status in arith_scores:
            arith = arith_scores[arith_status]

        # Structural richness
        total_structural = logogram_count + number_count
        total_all = total_words + total_structural
        structural = min(total_structural / max(total_all, 1), 1.0)

        # Size bonus
        size_bonus = min(math.log2(max(total_words, 1)) / 5.0, 1.0)

        # Unknown penalty
        unknown_ratio = unknown / total_words if total_words > 0 else 1.0
        unknown_penalty = 1.0 - unknown_ratio

        # Weighted composite (same weights as reading_readiness_scorer.py)
        score = (
            0.40 * coverage
            + 0.25 * arith
            + 0.15 * structural
            + 0.10 * size_bonus
            + 0.10 * unknown_penalty
        )
        score = min(max(score, 0.0), 1.0)

        return (round(score, 3), total_words, unknown, unknown_words)

    def get_current_readiness(self, tablet_id: str) -> float:
        """Get the current readiness score for a tablet."""
        if tablet_id in self.readiness_cache:
            return self.readiness_cache[tablet_id]
        # Compute inline
        score, _, _, _ = self._compute_readiness_inline(tablet_id)
        return score

    def find_tablets_with_word(self, word: str) -> Set[str]:
        """Find all tablets containing a given word."""
        tablets = set()
        tablets.update(self.word_to_tablets.get(word, set()))
        # Also try uppercase variant
        tablets.update(self.word_to_tablets.get(word.upper(), set()))
        return tablets

    def compute_cascade_from_word(self, word: str, new_confidence: str) -> CascadeReport:
        """
        Compute cascade effects of confirming a word.

        1. Find all tablets containing the word
        2. Recompute readiness with the word now identified
        3. Identify tablets crossing the readability threshold
        4. Trace transitive cascades through newly-readable names
        5. Return ranked opportunities

        Args:
            word: The word being confirmed (e.g., "KU-RO", "NI")
            new_confidence: Confidence level of the confirmation

        Returns:
            CascadeReport with all opportunities ranked by delta
        """
        # Track what we're adding as newly identified
        newly_confirmed = {word, word.upper()}

        # --- Phase 1: Direct tablets ---
        direct_tablet_ids = self.find_tablets_with_word(word)
        direct_opportunities = []
        transitive_chains = []

        # Track new name links discovered from newly-readable tablets
        new_name_links: Dict[str, Set[str]] = defaultdict(set)  # name -> tablets it appears on

        for tablet_id in sorted(direct_tablet_ids):
            current_score = self.get_current_readiness(tablet_id)
            new_score, total_words, new_unknown, unknown_words = self._compute_readiness_inline(
                tablet_id, extra_identified=newly_confirmed
            )

            delta = round(new_score - current_score, 3)

            # What words did we newly identify on this tablet?
            syllabic = self.tablet_syllabic_words.get(tablet_id, [])
            newly_id = [
                w
                for w in set(syllabic)
                if (w in newly_confirmed or w.upper() in newly_confirmed)
                and not self._is_word_identified(w)
            ]

            site = _extract_site(tablet_id)

            opp = CascadeOpportunity(
                tablet_id=tablet_id,
                current_readiness=current_score,
                new_readiness=new_score,
                readiness_delta=delta,
                newly_identified_words=newly_id,
                remaining_unknowns=new_unknown,
                site=site,
                cascade_depth=0,
            )
            direct_opportunities.append(opp)

            # If tablet crosses threshold, check for transitive effects
            if new_score >= self.threshold and current_score < self.threshold:
                # This tablet is newly "readable" — check for name links
                for unk_word in unknown_words:
                    if unk_word in newly_confirmed:
                        continue
                    # Check if this unknown word appears on other tablets
                    other_tablets = self.find_tablets_with_word(unk_word)
                    other_tablets.discard(tablet_id)
                    if other_tablets:
                        new_name_links[unk_word] = other_tablets

        # --- Phase 2: Transitive cascades ---
        transitive_opportunities = []
        visited_tablets = set(direct_tablet_ids)
        cascade_queue: List[Tuple[str, Set[str], int]] = []  # (word, tablets, depth)

        # Seed with name links from Phase 1
        for name_word, linked_tablets in new_name_links.items():
            cascade_queue.append((name_word, linked_tablets, 1))
            transitive_chains.append(
                {
                    "source_word": word,
                    "link_word": name_word,
                    "linked_tablets": sorted(linked_tablets),
                    "depth": 1,
                }
            )

        # BFS through transitive cascades (limit depth to prevent runaway)
        max_cascade_depth = 3
        while cascade_queue:
            link_word, link_tablets, depth = cascade_queue.pop(0)
            if depth > max_cascade_depth:
                continue

            # Add link_word as a "contextually identified" word
            transitive_identified = newly_confirmed | {link_word, link_word.upper()}

            for tablet_id in sorted(link_tablets):
                if tablet_id in visited_tablets:
                    continue
                visited_tablets.add(tablet_id)

                current_score = self.get_current_readiness(tablet_id)
                (new_score, total_words, new_unknown, unknown_words) = (
                    self._compute_readiness_inline(
                        tablet_id,
                        extra_identified=transitive_identified,
                    )
                )
                delta = round(new_score - current_score, 3)

                if delta <= 0:
                    continue

                syllabic = self.tablet_syllabic_words.get(tablet_id, [])
                newly_id = [
                    w
                    for w in set(syllabic)
                    if (w in transitive_identified or w.upper() in transitive_identified)
                    and not self._is_word_identified(w)
                ]

                site = _extract_site(tablet_id)

                opp = CascadeOpportunity(
                    tablet_id=tablet_id,
                    current_readiness=current_score,
                    new_readiness=new_score,
                    readiness_delta=delta,
                    newly_identified_words=newly_id,
                    remaining_unknowns=new_unknown,
                    site=site,
                    cascade_depth=depth,
                )
                transitive_opportunities.append(opp)

                # Check for further transitive effects
                if depth < max_cascade_depth and new_score >= self.threshold:
                    for unk_word in unknown_words:
                        if unk_word in transitive_identified:
                            continue
                        further_tablets = self.find_tablets_with_word(unk_word)
                        further_tablets -= visited_tablets
                        if further_tablets:
                            cascade_queue.append((unk_word, further_tablets, depth + 1))
                            transitive_chains.append(
                                {
                                    "source_word": link_word,
                                    "link_word": unk_word,
                                    "linked_tablets": sorted(further_tablets),
                                    "depth": depth + 1,
                                }
                            )

        # --- Combine and rank ---
        all_opportunities = direct_opportunities + transitive_opportunities
        # Sort by readiness delta (descending), then by new readiness (descending)
        all_opportunities.sort(key=lambda o: (-o.readiness_delta, -o.new_readiness))

        return CascadeReport(
            trigger_word=word,
            trigger_confidence=new_confidence,
            direct_tablets=len(direct_tablet_ids),
            cascade_tablets=len(transitive_opportunities),
            opportunities=all_opportunities,
            transitive_chains=transitive_chains,
        )

    def compute_all_anchors(self) -> List[CascadeReport]:
        """
        Compute cascade reports for all anchor words in reading_dependencies.

        Returns reports sorted by total opportunity count (most impactful first).
        """
        reports = []
        seen_words = set()

        # Process all readings that have a known meaning
        for reading_id, reading_data in self.readings.items():
            word = reading_id
            if word in seen_words:
                continue
            seen_words.add(word)

            confidence = reading_data.get("confidence", "SPECULATIVE")

            # Only process words that actually appear in the corpus
            tablets = self.find_tablets_with_word(word)
            if not tablets:
                continue

            report = self.compute_cascade_from_word(word, confidence)
            reports.append(report)

        # Also process known function words not in readings
        for word in KNOWN_FUNCTION_WORDS:
            if word in seen_words:
                continue
            seen_words.add(word)
            tablets = self.find_tablets_with_word(word)
            if not tablets:
                continue
            report = self.compute_cascade_from_word(word, "HIGH")
            reports.append(report)

        # Sort by total cascade impact (direct + transitive tablets with positive delta)
        reports.sort(
            key=lambda r: sum(1 for o in r.opportunities if o.readiness_delta > 0),
            reverse=True,
        )

        return reports

    # ------------------------------------------------------------------
    # Output formatting
    # ------------------------------------------------------------------

    def print_report(self, report: CascadeReport, verbose: bool = False):
        """Print a human-readable cascade report."""
        print(f"\n{'=' * 70}")
        print("CASCADE OPPORTUNITY REPORT")
        print(f"{'=' * 70}")
        print(f"  Trigger word: {report.trigger_word}")
        print(f"  Confidence:   {report.trigger_confidence}")
        print(f"  Direct tablets: {report.direct_tablets}")
        print(f"  Transitive cascade tablets: {report.cascade_tablets}")
        print(f"  Readiness threshold: {self.threshold}")

        # Summarize opportunities
        positive = [o for o in report.opportunities if o.readiness_delta > 0]
        threshold_crossers = [
            o
            for o in report.opportunities
            if o.current_readiness < self.threshold and o.new_readiness >= self.threshold
        ]

        print(f"\n  Tablets with readiness gain: {len(positive)}")
        print(f"  Tablets crossing threshold ({self.threshold}): {len(threshold_crossers)}")

        if positive:
            # Show top opportunities
            print(f"\n{'─' * 70}")
            print("  TOP CASCADE OPPORTUNITIES (by readiness gain)")
            print(f"{'─' * 70}")
            print(
                f"  {'Tablet':<14s} {'Current':>7s} {'New':>7s} {'Delta':>7s} "
                f"{'Unkn':>4s} {'Depth':>5s} {'Site':<6s} Newly Identified"
            )
            print(f"  {'-' * 66}")

            show = positive[:20] if not verbose else positive
            for opp in show:
                newly = ", ".join(opp.newly_identified_words[:3])
                if len(opp.newly_identified_words) > 3:
                    newly += f" (+{len(opp.newly_identified_words) - 3})"
                marker = (
                    " ***"
                    if (
                        opp.current_readiness < self.threshold
                        and opp.new_readiness >= self.threshold
                    )
                    else ""
                )
                print(
                    f"  {opp.tablet_id:<14s} {opp.current_readiness:7.3f} "
                    f"{opp.new_readiness:7.3f} {opp.readiness_delta:+7.3f} "
                    f"{opp.remaining_unknowns:4d} {opp.cascade_depth:5d} "
                    f"{opp.site:<6s} {newly}{marker}"
                )

            if len(positive) > 20 and not verbose:
                print(f"  ... and {len(positive) - 20} more (use --verbose to see all)")

        # Threshold crossers
        if threshold_crossers:
            print(f"\n{'─' * 70}")
            print("  THRESHOLD CROSSERS (newly readable)")
            print(f"{'─' * 70}")
            for opp in threshold_crossers:
                print(
                    f"  {opp.tablet_id:<14s} "
                    f"{opp.current_readiness:.3f} -> {opp.new_readiness:.3f} "
                    f"(depth {opp.cascade_depth})"
                )

        # Transitive chains
        if report.transitive_chains:
            print(f"\n{'─' * 70}")
            print("  TRANSITIVE CHAINS")
            print(f"{'─' * 70}")
            for chain in report.transitive_chains[:10]:
                tablet_list = ", ".join(chain["linked_tablets"][:5])
                if len(chain["linked_tablets"]) > 5:
                    tablet_list += f" (+{len(chain['linked_tablets']) - 5})"
                print(
                    f"  [{chain['depth']}] {chain['source_word']} -> "
                    f"{chain['link_word']} -> {tablet_list}"
                )
            if len(report.transitive_chains) > 10:
                print(f"  ... and {len(report.transitive_chains) - 10} more chains")

        print(f"\n{'=' * 70}")

    def print_all_anchors_summary(self, reports: List[CascadeReport]):
        """Print summary of cascade potential across all anchor words."""
        print(f"\n{'=' * 70}")
        print("CASCADE OPPORTUNITY SUMMARY — ALL ANCHORS")
        print(f"{'=' * 70}")
        print(f"  Threshold: {self.threshold}")
        print(f"  Anchor words analyzed: {len(reports)}")

        # Filter to only reports with positive impact
        impactful = [r for r in reports if any(o.readiness_delta > 0 for o in r.opportunities)]

        print(f"  Anchors with cascade potential: {len(impactful)}")

        if impactful:
            print(
                f"\n  {'Word':<20s} {'Conf':<10s} {'Direct':>6s} {'Trans':>5s} "
                f"{'Gains':>5s} {'Cross':>5s} {'Max Δ':>7s}"
            )
            print(f"  {'-' * 62}")

            for r in impactful[:30]:
                positive = [o for o in r.opportunities if o.readiness_delta > 0]
                crossers = [
                    o
                    for o in r.opportunities
                    if o.current_readiness < self.threshold and o.new_readiness >= self.threshold
                ]
                max_delta = max(
                    (o.readiness_delta for o in r.opportunities),
                    default=0.0,
                )
                print(
                    f"  {r.trigger_word:<20s} {r.trigger_confidence:<10s} "
                    f"{r.direct_tablets:6d} {r.cascade_tablets:5d} "
                    f"{len(positive):5d} {len(crossers):5d} {max_delta:+7.3f}"
                )

            if len(impactful) > 30:
                print(f"\n  ... and {len(impactful) - 30} more")

        # Most efficient next readings
        print(f"\n{'─' * 70}")
        print("  MOST EFFICIENT NEXT READINGS")
        print("  (Words whose confirmation unlocks the most downstream readability)")
        print(f"{'─' * 70}")

        # Score each word by total readiness delta it produces
        word_scores = []
        for r in reports:
            total_delta = sum(o.readiness_delta for o in r.opportunities if o.readiness_delta > 0)
            crosser_count = sum(
                1
                for o in r.opportunities
                if o.current_readiness < self.threshold and o.new_readiness >= self.threshold
            )
            if total_delta > 0:
                word_scores.append(
                    {
                        "word": r.trigger_word,
                        "confidence": r.trigger_confidence,
                        "total_delta": round(total_delta, 3),
                        "tablets_improved": sum(
                            1 for o in r.opportunities if o.readiness_delta > 0
                        ),
                        "threshold_crossers": crosser_count,
                        "direct_tablets": r.direct_tablets,
                        # Efficiency = delta per tablet affected
                        "efficiency": round(total_delta / max(r.direct_tablets, 1), 3),
                    }
                )

        # Sort by total delta (most impact first)
        word_scores.sort(key=lambda w: -w["total_delta"])

        if word_scores:
            print(
                f"\n  {'Rank':>4s}  {'Word':<20s} {'Total Δ':>8s} {'Tablets':>7s} "
                f"{'Cross':>5s} {'Effic':>7s} {'Conf':<10s}"
            )
            print(f"  {'-' * 66}")

            for i, ws in enumerate(word_scores[:15], 1):
                print(
                    f"  {i:4d}  {ws['word']:<20s} {ws['total_delta']:+8.3f} "
                    f"{ws['tablets_improved']:7d} {ws['threshold_crossers']:5d} "
                    f"{ws['efficiency']:7.3f} {ws['confidence']:<10s}"
                )

        print(f"\n{'=' * 70}")

    def save_results(
        self,
        reports: List[CascadeReport],
        output_path: str,
        single_word: bool = False,
    ):
        """Save results to JSON."""
        if single_word and len(reports) == 1:
            report = reports[0]
            output = {
                "metadata": {
                    "tool": "cascade_opportunity_detector.py",
                    "generated": datetime.now().isoformat(),
                    "threshold": self.threshold,
                },
                "trigger": {
                    "word": report.trigger_word,
                    "confidence": report.trigger_confidence,
                },
                "summary": {
                    "direct_tablets": report.direct_tablets,
                    "cascade_tablets": report.cascade_tablets,
                    "total_opportunities": len(report.opportunities),
                    "positive_delta_count": sum(
                        1 for o in report.opportunities if o.readiness_delta > 0
                    ),
                    "threshold_crossers": sum(
                        1
                        for o in report.opportunities
                        if o.current_readiness < self.threshold
                        and o.new_readiness >= self.threshold
                    ),
                },
                "opportunities": [asdict(o) for o in report.opportunities],
                "transitive_chains": report.transitive_chains,
            }
        else:
            # Multi-word summary
            word_summaries = []
            for r in reports:
                positive = [o for o in r.opportunities if o.readiness_delta > 0]
                total_delta = sum(o.readiness_delta for o in positive)
                crossers = sum(
                    1
                    for o in r.opportunities
                    if o.current_readiness < self.threshold and o.new_readiness >= self.threshold
                )
                word_summaries.append(
                    {
                        "word": r.trigger_word,
                        "confidence": r.trigger_confidence,
                        "direct_tablets": r.direct_tablets,
                        "cascade_tablets": r.cascade_tablets,
                        "tablets_improved": len(positive),
                        "threshold_crossers": crossers,
                        "total_readiness_delta": round(total_delta, 3),
                        "efficiency": round(total_delta / max(r.direct_tablets, 1), 3),
                    }
                )

            # Sort by total delta
            word_summaries.sort(key=lambda w: -w["total_readiness_delta"])

            output = {
                "metadata": {
                    "tool": "cascade_opportunity_detector.py",
                    "generated": datetime.now().isoformat(),
                    "threshold": self.threshold,
                    "words_analyzed": len(reports),
                },
                "word_rankings": word_summaries,
            }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Cascade Opportunity Detector — find highest-leverage next readings"
    )
    parser.add_argument(
        "--word", type=str, help="Trigger word to test cascade from (e.g., KU-RO, NI)"
    )
    parser.add_argument(
        "--confidence",
        type=str,
        default="HIGH",
        choices=CONFIDENCE_LEVELS,
        help="Confidence level of the confirmed reading (default: HIGH)",
    )
    parser.add_argument(
        "--all-anchors", action="store_true", help="Compute cascade potential for all anchor words"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Readiness threshold for 'readable' (default: 0.5)",
    )
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    parser.add_argument(
        "--verbose", action="store_true", help="Show all opportunities (not just top 20)"
    )

    args = parser.parse_args()

    if not args.word and not args.all_anchors:
        parser.print_help()
        print("\nError: Must specify --word or --all-anchors")
        sys.exit(1)

    print("=" * 70)
    print("LINEAR A CASCADE OPPORTUNITY DETECTOR")
    print("=" * 70)

    detector = CascadeOpportunityDetector(threshold=args.threshold)
    if not detector.load_data():
        sys.exit(1)

    if args.word:
        report = detector.compute_cascade_from_word(args.word, args.confidence)
        detector.print_report(report, verbose=args.verbose)

        if args.output:
            detector.save_results([report], args.output, single_word=True)

    elif args.all_anchors:
        reports = detector.compute_all_anchors()
        detector.print_all_anchors_summary(reports)

        if args.output:
            detector.save_results(reports, args.output, single_word=False)


if __name__ == "__main__":
    main()
