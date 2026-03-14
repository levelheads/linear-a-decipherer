#!/usr/bin/env python3
"""
Reading Pipeline for Linear A

Automated reading workflow: SELECT -> PREPARE -> (READ) -> RECORD.
Replaces ~15 min of manual preparation per tablet with structured automation.

Stages:
    1. SELECT  - Score and rank unread tablets into a prioritized, site-balanced queue
    2. PREPARE - Gather all evidence into a structured "reading brief" for a tablet
    3. READ    - Human/Claude judgment (not automatable)
    4. RECORD  - Register new readings and update tracking files

Usage:
    python3 tools/reading_pipeline.py --select --top 20
    python3 tools/reading_pipeline.py --select --site-balanced --top 30
    python3 tools/reading_pipeline.py --prepare HT100
    python3 tools/reading_pipeline.py --queue --site-balanced
    python3 tools/reading_pipeline.py --output data/reading_queue.json
    python3 tools/reading_pipeline.py --record HT100 --meaning "commodity list" --confidence MEDIUM

Attribution:
    Part of Linear A Decipherment Project
    Automates the preparation workflow for tablet reading attempts
"""

import json
import argparse
import re
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
ANCHORS_FILE = DATA_DIR / "anchors.json"
DEPENDENCIES_FILE = DATA_DIR / "reading_dependencies.json"
HYPOTHESIS_FILE = DATA_DIR / "hypothesis_results.json"
ARITHMETIC_FILE = DATA_DIR / "arithmetic_verification.json"
NAMES_FILE = DATA_DIR / "personal_names_comprehensive.json"
READINESS_FILE = DATA_DIR / "reading_readiness.json"
CASCADE_FILE = DATA_DIR / "cascade_opportunities.json"
COMPLETED_DIR = PROJECT_ROOT / "analysis" / "completed" / "inscriptions"


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
    "\u00bd",
    "\u00bc",
    "\u00be",
    "\u2153",
    "\u2154",
    "\u215b",
    "\u215c",
    "\u00b9\u2044\u2082",
    "\u00b9\u2044\u2084",
    "\u00b3\u2044\u2084",
    "\u00b9\u2044\u2083",
    "\u00b2\u2044\u2083",
    "\u00b9\u2044\u2088",
    "\u00b3\u2044\u2088",
    "\u00b9\u2044\u2081\u2086",
    "~\u00b9\u2044\u2086",
    "\u00b9\u2044\u2086",
}

# Administrative function words with known/proposed functions
KNOWN_FUNCTION_WORDS = {
    "KU-RO": "total/summation",
    "KI-RO": "deficit/remainder",
    "TE": "header/topic marker",
    "SA-RA\u2082": "allocation marker",
    "A-DU": "contributor/sender",
    "DA-RE": "received/transaction verb",
}

# Commodity logogram base tokens for matching compound logograms
COMMODITY_BASES = {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}


# ─── Data classes ────────────────────────────────────────────────────────────


@dataclass
class QueueEntry:
    """A tablet in the reading queue with scoring metadata."""

    tablet_id: str
    site: str
    readiness_score: float
    total_words: int
    anchored_words: int
    named_words: int
    unknown_words: int
    coverage_pct: float
    arithmetic_status: str
    document_type: str
    cascade_boost: float = 0.0
    priority_score: float = 0.0


@dataclass
class ReadingBrief:
    """Structured evidence brief for a tablet reading attempt."""

    tablet_id: str
    site: str
    transliteration: List[str]
    raw_text: str
    total_tokens: int
    syllabic_words: int

    # Evidence layers
    arithmetic: Optional[Dict] = None
    word_analyses: Dict = field(default_factory=dict)
    anchored_words: List[Dict] = field(default_factory=list)
    named_words: List[Dict] = field(default_factory=list)
    formula_words: List[str] = field(default_factory=list)
    commodity_logograms: List[str] = field(default_factory=list)
    cross_tablet_links: List[Dict] = field(default_factory=list)
    hypothesis_summary: Dict = field(default_factory=dict)
    readiness_score: float = 0.0
    document_type: str = "unknown"


# ─── Helper functions ────────────────────────────────────────────────────────


def _load_json(path: Path) -> Optional[Dict]:
    """Load a JSON file, returning None if missing or invalid."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"  Warning: Error loading {path.name}: {e}")
        return None


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
        return base in COMMODITY_BASES
    return False


def _is_word(token: str) -> bool:
    """Check if token is a syllabic word (not separator, number, or logogram)."""
    if token in {"\n", "\U00010101", "", " ", "\u2014", ",", ".", "[", "]"}:
        return False
    if _is_number(token):
        return False
    if _is_logogram(token):
        return False
    if token.startswith('"'):
        return False
    if token == "*":
        return False
    return True


def _extract_site(tablet_id: str) -> str:
    """Extract site code from tablet ID (e.g., 'HT' from 'HT85a')."""
    match = re.match(r"^([A-Z]+)", tablet_id)
    return match.group(1) if match else "UNKNOWN"


# ─── Already-read detection ─────────────────────────────────────────────────


def get_already_read_tablets() -> Set[str]:
    """
    Scan analysis/completed/inscriptions/ for *_READING.md files
    and extract tablet IDs from filenames.

    Filename patterns:
        HT85a_READING.md        -> HT85a
        HT123_124a_READING.md   -> HT123+124a (join format)
        KH7b_READING.md         -> KH7b
        ZA15b_READING.md        -> ZA15b
    """
    read_tablets = set()

    if not COMPLETED_DIR.exists():
        return read_tablets

    for reading_file in COMPLETED_DIR.glob("*_READING.md"):
        filename = reading_file.stem  # e.g., "HT85a_READING"
        # Remove _READING suffix
        tablet_part = filename.replace("_READING", "")
        # Handle joined tablet IDs like HT123_124a -> HT123+124a
        # Store both the underscore and plus versions
        read_tablets.add(tablet_part)
        if "_" in tablet_part:
            read_tablets.add(tablet_part.replace("_", "+"))
        read_tablets.add(tablet_part.replace("+", "_"))

    return read_tablets


# ─── SELECT stage ────────────────────────────────────────────────────────────


class SelectStage:
    """
    Stage 1: SELECT - Score and rank unread tablets.

    Uses pre-computed readiness scores from data/reading_readiness.json
    when available, falls back to live scoring from corpus data.
    Optionally boosts scores using cascade opportunity data.
    Filters out already-read tablets.
    """

    def __init__(self):
        self.corpus = None
        self.inscriptions = {}
        self.readiness_data = None
        self.cascade_data = None
        self.already_read: Set[str] = set()
        self.anchors = {}
        self.dependencies = {}

    def load_data(self) -> bool:
        """Load required data sources."""
        # Corpus is required
        self.corpus = _load_json(CORPUS_FILE)
        if not self.corpus:
            print("Error: Cannot load corpus.json")
            return False
        self.inscriptions = self.corpus.get("inscriptions", {})
        print(f"Loaded {len(self.inscriptions)} inscriptions from corpus")

        # Pre-computed readiness scores (optional but preferred)
        self.readiness_data = _load_json(READINESS_FILE)
        if self.readiness_data:
            rankings = self.readiness_data.get("rankings", [])
            print(f"Loaded {len(rankings)} pre-computed readiness scores")
        else:
            print("  No pre-computed readiness scores; will compute from corpus")

        # Cascade opportunities (optional)
        self.cascade_data = _load_json(CASCADE_FILE)
        if self.cascade_data:
            print("Loaded cascade opportunity data")

        # Anchors and dependencies (for enrichment)
        anchors_data = _load_json(ANCHORS_FILE)
        if anchors_data:
            self.anchors = anchors_data.get("anchors", {})

        deps_data = _load_json(DEPENDENCIES_FILE)
        if deps_data:
            self.dependencies = deps_data.get("readings", {})

        # Already-read tablets
        self.already_read = get_already_read_tablets()
        print(f"Found {len(self.already_read)} already-read tablets to exclude")

        return True

    def _get_readiness_from_precomputed(self, tablet_id: str) -> Optional[Dict]:
        """Look up a tablet in pre-computed readiness data."""
        if not self.readiness_data:
            return None
        for entry in self.readiness_data.get("rankings", []):
            if entry.get("tablet_id") == tablet_id:
                return entry
        return None

    def _compute_readiness_live(self, tablet_id: str) -> Optional[Dict]:
        """
        Compute basic readiness metrics from corpus data directly.
        Lighter-weight than reading_readiness_scorer but sufficient for ranking.
        """
        tablet_data = self.inscriptions.get(tablet_id)
        if not tablet_data:
            return None

        all_tokens = tablet_data.get("transliteratedWords", [])

        syllabic_count = 0
        logogram_count = 0
        number_count = 0
        anchored_count = 0
        named_count = 0
        unknown_count = 0

        for token in all_tokens:
            if token in {"\n", "\U00010101", "", " ", "\u2014"}:
                continue
            if _is_logogram(token):
                logogram_count += 1
            elif _is_number(token):
                number_count += 1
            elif _is_word(token):
                syllabic_count += 1
                upper = token.upper()
                if upper in KNOWN_FUNCTION_WORDS or token in KNOWN_FUNCTION_WORDS:
                    anchored_count += 1
                elif upper in self.dependencies:
                    anchored_count += 1
                else:
                    unknown_count += 1

        if syllabic_count == 0:
            return None

        identified = syllabic_count - unknown_count
        coverage = (identified / syllabic_count * 100) if syllabic_count > 0 else 0

        # Check for KU-RO
        has_kuro = "KU-RO" in set(all_tokens)
        arith_status = "NO_KURO" if not has_kuro else "NOT_AUDITED"

        # Simple readiness score
        cov_score = identified / syllabic_count if syllabic_count > 0 else 0
        total_structural = logogram_count + number_count
        total_all = syllabic_count + total_structural
        structural = min(total_structural / max(total_all, 1), 1.0)
        size_bonus = min(math.log2(max(syllabic_count, 1)) / 5.0, 1.0)
        unknown_ratio = unknown_count / syllabic_count if syllabic_count > 0 else 1.0
        unknown_penalty = 1.0 - unknown_ratio

        score = (
            0.40 * cov_score
            + 0.25 * (1.0 if has_kuro else 0.2)
            + 0.15 * structural
            + 0.10 * size_bonus
            + 0.10 * unknown_penalty
        )

        return {
            "tablet_id": tablet_id,
            "readiness_score": round(min(max(score, 0.0), 1.0), 3),
            "total_words": syllabic_count,
            "anchored_words": anchored_count,
            "named_words": named_count,
            "unknown_words": unknown_count,
            "logogram_count": logogram_count,
            "number_count": number_count,
            "coverage_pct": round(coverage, 1),
            "arithmetic_status": arith_status,
            "document_type": "administrative",
            "site": _extract_site(tablet_id),
        }

    def _get_cascade_boost(self, tablet_id: str) -> float:
        """
        Get cascade opportunity boost for a tablet.
        Tablets that could unlock cascading insights get a score boost.
        """
        if not self.cascade_data:
            return 0.0

        opportunities = self.cascade_data.get("opportunities", [])
        if isinstance(opportunities, list):
            for opp in opportunities:
                if isinstance(opp, dict) and opp.get("tablet_id") == tablet_id:
                    return opp.get("cascade_score", 0.0) * 0.1  # Scale to ~0-0.1 range
        elif isinstance(opportunities, dict):
            opp = opportunities.get(tablet_id)
            if isinstance(opp, dict):
                return opp.get("cascade_score", 0.0) * 0.1

        return 0.0

    def _is_already_read(self, tablet_id: str) -> bool:
        """Check if a tablet has already been read."""
        if tablet_id in self.already_read:
            return True
        # Also check normalized forms
        normalized = tablet_id.replace("+", "_")
        if normalized in self.already_read:
            return True
        return False

    def build_queue(self, top_n: int = 0) -> List[QueueEntry]:
        """
        Build the prioritized reading queue.

        Returns tablets sorted by priority_score (readiness + cascade boost),
        excluding already-read tablets.
        """
        queue = []

        for tablet_id in self.inscriptions:
            if self._is_already_read(tablet_id):
                continue

            # Try pre-computed readiness first, fall back to live
            data = self._get_readiness_from_precomputed(tablet_id)
            if not data:
                data = self._compute_readiness_live(tablet_id)
            if not data:
                continue

            cascade_boost = self._get_cascade_boost(tablet_id)
            readiness = data.get("readiness_score", 0.0)
            priority = readiness + cascade_boost

            entry = QueueEntry(
                tablet_id=tablet_id,
                site=data.get("site", _extract_site(tablet_id)),
                readiness_score=readiness,
                total_words=data.get("total_words", 0),
                anchored_words=data.get("anchored_words", 0),
                named_words=data.get("named_words", 0),
                unknown_words=data.get("unknown_words", 0),
                coverage_pct=data.get("coverage_pct", 0.0),
                arithmetic_status=data.get("arithmetic_status", "NO_DATA"),
                document_type=data.get("document_type", "unknown"),
                cascade_boost=round(cascade_boost, 3),
                priority_score=round(priority, 3),
            )
            queue.append(entry)

        # Sort by priority score descending
        queue.sort(key=lambda e: e.priority_score, reverse=True)

        if top_n > 0:
            queue = queue[:top_n]

        return queue

    def site_balance(self, queue: List[QueueEntry]) -> List[QueueEntry]:
        """
        Interleave tablets from different sites so consecutive readings
        come from different sites where possible.

        Algorithm: Round-robin across site buckets, ordered by best score in each bucket.
        """
        if not queue:
            return queue

        # Group by site, preserving priority order within each group
        site_buckets: Dict[str, List[QueueEntry]] = defaultdict(list)
        for entry in queue:
            site_buckets[entry.site].append(entry)

        # Order site groups by best score in each
        site_order = sorted(
            site_buckets.keys(),
            key=lambda s: site_buckets[s][0].priority_score if site_buckets[s] else 0,
            reverse=True,
        )

        # Round-robin interleave
        balanced = []
        iterators = {site: iter(site_buckets[site]) for site in site_order}
        active_sites = list(site_order)

        while active_sites:
            exhausted = []
            for site in active_sites:
                try:
                    entry = next(iterators[site])
                    balanced.append(entry)
                except StopIteration:
                    exhausted.append(site)
            for site in exhausted:
                active_sites.remove(site)

        return balanced


# ─── PREPARE stage ───────────────────────────────────────────────────────────


class PrepareStage:
    """
    Stage 2: PREPARE - Gather all evidence into a structured reading brief.

    For a given tablet ID, collects:
    - Corpus transliteration
    - Arithmetic verification data (if KU-RO present)
    - Personnel dossiers (if exists) for names on the tablet
    - Hypothesis results for words on the tablet
    - Known anchors, named words, formula words
    - Cross-tablet name links
    - Commodity analysis
    """

    def __init__(self):
        self.corpus = None
        self.inscriptions = {}
        self.hypothesis_results = {}
        self.arithmetic_data = {}
        self.names_data = {}
        self.anchors = {}
        self.dependencies = {}
        self.readiness_data = None
        self.known_names: Set[str] = set()

    def load_data(self) -> bool:
        """Load all evidence data sources."""
        # Corpus is required
        self.corpus = _load_json(CORPUS_FILE)
        if not self.corpus:
            print("Error: Cannot load corpus.json")
            return False
        self.inscriptions = self.corpus.get("inscriptions", {})
        print(f"Loaded {len(self.inscriptions)} inscriptions")

        # Optional data files
        hyp_data = _load_json(HYPOTHESIS_FILE)
        if hyp_data:
            self.hypothesis_results = hyp_data.get("word_analyses", {})
            print(f"  Hypothesis results: {len(self.hypothesis_results)} words")

        arith_data = _load_json(ARITHMETIC_FILE)
        if arith_data:
            self.arithmetic_data = arith_data
            verifications = arith_data.get("verifications", [])
            print(f"  Arithmetic verifications: {len(verifications)} tablets")

        names_data = _load_json(NAMES_FILE)
        if names_data:
            self.names_data = names_data
            names_dict = names_data.get("names", {})
            if isinstance(names_dict, dict):
                self.known_names = set(names_dict.keys())
            elif isinstance(names_dict, list):
                self.known_names = {
                    n.get("name", n.get("word", "")) for n in names_dict if isinstance(n, dict)
                }
            print(f"  Known names: {len(self.known_names)}")

        anchors_data = _load_json(ANCHORS_FILE)
        if anchors_data:
            self.anchors = anchors_data.get("anchors", {})

        deps_data = _load_json(DEPENDENCIES_FILE)
        if deps_data:
            self.dependencies = deps_data.get("readings", {})
            print(f"  Reading dependencies: {len(self.dependencies)} readings")

        self.readiness_data = _load_json(READINESS_FILE)

        # Personnel dossiers (optional, may not exist yet)
        dossiers_file = DATA_DIR / "personnel_dossiers.json"
        self.personnel_dossiers = _load_json(dossiers_file) or {}

        return True

    def _get_arithmetic_for_tablet(self, tablet_id: str) -> Optional[Dict]:
        """Get arithmetic verification data for a specific tablet."""
        if not self.arithmetic_data:
            return None

        verifications = self.arithmetic_data.get("verifications", [])
        for v in verifications:
            if v.get("tablet_id") == tablet_id:
                return {
                    "has_kuro": v.get("has_kuro", False),
                    "has_kiro": v.get("has_kiro", False),
                    "kuro_status": v.get("kuro_status", "UNKNOWN"),
                    "kuro_value": v.get("kuro_value"),
                    "computed_sum": v.get("computed_sum"),
                    "difference": v.get("difference"),
                    "item_count": v.get("item_count", 0),
                    "diagnosis": v.get("diagnosis"),
                    "skeleton": v.get("skeleton", []),
                }
        return None

    def _get_hypothesis_for_word(self, word: str) -> Optional[Dict]:
        """Get hypothesis results for a word."""
        if not self.hypothesis_results:
            return None

        # Keys are UPPERCASE in hypothesis_results.json
        word_data = self.hypothesis_results.get(
            word.upper(), self.hypothesis_results.get(word, None)
        )
        if not word_data:
            return None

        synthesis = word_data.get("synthesis", {})
        hypotheses = word_data.get("hypotheses", {})

        summary = {
            "best_hypothesis": synthesis.get("best_hypothesis", "unknown"),
            "max_confidence": synthesis.get("max_confidence", "UNKNOWN"),
            "verdict": synthesis.get("verdict", "UNKNOWN"),
        }

        # Include per-hypothesis verdicts
        for hyp_name, hyp_data in hypotheses.items():
            if isinstance(hyp_data, dict):
                summary[f"{hyp_name}_verdict"] = hyp_data.get("verdict", "UNKNOWN")
                summary[f"{hyp_name}_score"] = hyp_data.get("score", 0)

        return summary

    def _get_name_info(self, word: str) -> Optional[Dict]:
        """Get personal name information for a word."""
        if not self.names_data:
            return None

        names_dict = self.names_data.get("names", {})
        if isinstance(names_dict, dict):
            # Try exact match then case variations
            name_entry = names_dict.get(word, names_dict.get(word.upper(), None))
            if name_entry and isinstance(name_entry, dict):
                return {
                    "word": name_entry.get("word", word),
                    "occurrences": name_entry.get("occurrences", 0),
                    "sites": name_entry.get("sites", []),
                    "gender": name_entry.get("gender", "unknown"),
                    "confidence": name_entry.get("confidence", "UNKNOWN"),
                    "best_hypothesis": name_entry.get("best_hypothesis", "unknown"),
                }
        return None

    def _get_dossier(self, word: str) -> Optional[Dict]:
        """Get personnel dossier for a name."""
        if not self.personnel_dossiers:
            return None

        dossiers = self.personnel_dossiers.get("dossiers", self.personnel_dossiers)
        if isinstance(dossiers, dict):
            return dossiers.get(word, dossiers.get(word.upper(), None))
        return None

    def _find_cross_tablet_links(self, words: List[str], tablet_id: str) -> List[Dict]:
        """
        Find other tablets that share names with this one.
        Only considers syllabic words that are identified as names or potential names.
        """
        links = []
        seen_pairs = set()

        for word in words:
            if not _is_word(word):
                continue
            word_upper = word.upper()

            # Check if this is a known name or appears in dependencies
            is_name = (
                word_upper in self.known_names
                or word in self.known_names
                or word_upper in KNOWN_FUNCTION_WORDS
                or word_upper in self.dependencies
            )

            if not is_name:
                continue

            # Search corpus for other tablets with this word
            for other_id, other_data in self.inscriptions.items():
                if other_id == tablet_id:
                    continue
                other_words = other_data.get("transliteratedWords", [])
                if word in other_words or word_upper in [
                    w.upper() for w in other_words if isinstance(w, str)
                ]:
                    pair_key = (word_upper, other_id)
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        links.append(
                            {
                                "shared_word": word,
                                "linked_tablet": other_id,
                                "linked_site": _extract_site(other_id),
                                "word_type": "function"
                                if word_upper in KNOWN_FUNCTION_WORDS
                                else "name/reading",
                            }
                        )

        # Sort by word then tablet
        links.sort(key=lambda x: (x["shared_word"], x["linked_tablet"]))
        return links

    def _classify_word(self, word: str) -> Dict:
        """Classify a word's status based on all available evidence."""
        word_upper = word.upper()

        # Check function words
        if word_upper in KNOWN_FUNCTION_WORDS or word in KNOWN_FUNCTION_WORDS:
            func = KNOWN_FUNCTION_WORDS.get(word_upper, KNOWN_FUNCTION_WORDS.get(word, ""))
            return {
                "word": word,
                "category": "anchored",
                "identification": func,
                "confidence": "HIGH",
            }

        # Check reading dependencies
        if word_upper in self.dependencies:
            dep = self.dependencies[word_upper]
            return {
                "word": word,
                "category": "reading",
                "identification": dep.get("meaning", "tracked reading"),
                "confidence": dep.get("confidence", "UNKNOWN"),
            }

        # Check personal names
        if word_upper in self.known_names or word in self.known_names:
            return {
                "word": word,
                "category": "named",
                "identification": "personal name",
                "confidence": "PROBABLE",
            }

        # Unknown
        return {
            "word": word,
            "category": "unknown",
            "identification": "unidentified",
            "confidence": "UNKNOWN",
        }

    def _get_readiness_score(self, tablet_id: str) -> float:
        """Get readiness score from pre-computed data."""
        if self.readiness_data:
            for entry in self.readiness_data.get("rankings", []):
                if entry.get("tablet_id") == tablet_id:
                    return entry.get("readiness_score", 0.0)
        return 0.0

    def _get_document_type(self, tablet_id: str) -> str:
        """Get document type from readiness data or infer from content."""
        if self.readiness_data:
            for entry in self.readiness_data.get("rankings", []):
                if entry.get("tablet_id") == tablet_id:
                    return entry.get("document_type", "unknown")

        # Basic inference from content
        tablet_data = self.inscriptions.get(tablet_id, {})
        words = set(tablet_data.get("transliteratedWords", []))

        libation_markers = {"JA-SA-SA-RA-ME", "A-TA-I-*301-WA-JA", "I-DA-MA-TE"}
        if words & libation_markers:
            return "religious/libation"
        if "KU-RO" in words:
            return "administrative/list"
        has_commodities = any(_is_logogram(w) for w in words)
        has_numbers = any(_is_number(w) for w in words)
        if has_commodities and has_numbers:
            return "administrative/commodity"
        return "administrative"

    def prepare_brief(self, tablet_id: str) -> Optional[ReadingBrief]:
        """
        Prepare a complete reading brief for a tablet.

        Gathers all available evidence into a structured format
        suitable for feeding into a reading attempt.
        """
        tablet_data = self.inscriptions.get(tablet_id)
        if not tablet_data:
            print(f"Error: Tablet {tablet_id} not found in corpus")
            return None

        transliteration = tablet_data.get("transliteratedWords", [])
        site = _extract_site(tablet_id)

        # Build raw text representation
        raw_parts = []
        for token in transliteration:
            if token == "\n":
                raw_parts.append(" | ")
            elif token == "\U00010101":
                raw_parts.append(" \u00b7 ")
            else:
                raw_parts.append(token + " ")
        raw_text = "".join(raw_parts).strip()

        # Count tokens
        syllabic_words = [t for t in transliteration if _is_word(t)]
        commodity_logs = [t for t in transliteration if _is_logogram(t)]

        brief = ReadingBrief(
            tablet_id=tablet_id,
            site=site,
            transliteration=transliteration,
            raw_text=raw_text,
            total_tokens=len([t for t in transliteration if t not in {"\n", "", " "}]),
            syllabic_words=len(syllabic_words),
            readiness_score=self._get_readiness_score(tablet_id),
            document_type=self._get_document_type(tablet_id),
            commodity_logograms=commodity_logs,
        )

        # Arithmetic verification
        brief.arithmetic = self._get_arithmetic_for_tablet(tablet_id)

        # Word-by-word analysis
        anchored = []
        named = []

        for word in syllabic_words:
            classification = self._classify_word(word)
            word_entry = dict(classification)

            # Add hypothesis data
            hyp = self._get_hypothesis_for_word(word)
            if hyp:
                word_entry["hypothesis"] = hyp

            # Add name info
            name_info = self._get_name_info(word)
            if name_info:
                word_entry["name_info"] = name_info

            # Add personnel dossier
            dossier = self._get_dossier(word)
            if dossier:
                word_entry["dossier"] = dossier

            brief.word_analyses[word] = word_entry

            cat = classification["category"]
            if cat in ("anchored", "reading"):
                anchored.append(word_entry)
            elif cat == "named":
                named.append(word_entry)

        brief.anchored_words = anchored
        brief.named_words = named

        # Cross-tablet links (limit search to meaningful words)
        meaningful_words = [
            w
            for w in syllabic_words
            if w.upper() in KNOWN_FUNCTION_WORDS
            or w.upper() in self.dependencies
            or w.upper() in self.known_names
            or w in self.known_names
        ]
        brief.cross_tablet_links = self._find_cross_tablet_links(meaningful_words, tablet_id)

        # Build hypothesis summary
        hyp_counts = defaultdict(int)
        for word, analysis in brief.word_analyses.items():
            hyp = analysis.get("hypothesis", {})
            best = hyp.get("best_hypothesis", "")
            if best and best != "unknown":
                hyp_counts[best] += 1
        brief.hypothesis_summary = dict(hyp_counts)

        return brief

    def print_brief(self, brief: ReadingBrief):
        """Print a human-readable reading brief."""
        print()
        print("=" * 72)
        print(f"READING BRIEF: {brief.tablet_id}")
        print("=" * 72)
        print()
        print(f"  Site: {brief.site}")
        print(f"  Document type: {brief.document_type}")
        print(f"  Readiness score: {brief.readiness_score:.3f}")
        print(f"  Total tokens: {brief.total_tokens}")
        print(f"  Syllabic words: {brief.syllabic_words}")
        comm_str = ", ".join(brief.commodity_logograms) if brief.commodity_logograms else "none"
        print(f"  Commodity logograms: {comm_str}")

        # Transliteration
        print()
        print("--- Transliteration ---")
        print(f"  {brief.raw_text}")

        # Arithmetic
        if brief.arithmetic:
            print()
            print("--- Arithmetic Verification ---")
            arith = brief.arithmetic
            print(f"  KU-RO present: {arith.get('has_kuro', False)}")
            print(f"  KI-RO present: {arith.get('has_kiro', False)}")
            print(f"  Status: {arith.get('kuro_status', 'N/A')}")
            if arith.get("kuro_value") is not None:
                print(f"  KU-RO value: {arith['kuro_value']}")
            if arith.get("computed_sum") is not None:
                print(f"  Computed sum: {arith['computed_sum']}")
            if arith.get("difference") is not None:
                print(f"  Difference: {arith['difference']}")
            if arith.get("diagnosis"):
                print(f"  Diagnosis: {arith['diagnosis']}")

        # Word analysis
        print()
        print("--- Word Analysis ---")
        for word, analysis in brief.word_analyses.items():
            cat = analysis.get("category", "?")
            marker = {
                "anchored": "A",
                "reading": "R",
                "named": "N",
                "formula": "F",
                "unknown": "?",
            }.get(cat, ".")
            ident = analysis.get("identification", "")
            conf = analysis.get("confidence", "")
            hyp = analysis.get("hypothesis", {})
            best_hyp = hyp.get("best_hypothesis", "")
            hyp_str = f" [{best_hyp}]" if best_hyp and best_hyp != "unknown" else ""

            print(f"  [{marker}] {word:20s} = {ident} ({conf}){hyp_str}")

            # Show dossier info if available
            if "dossier" in analysis:
                dos = analysis["dossier"]
                if isinstance(dos, dict):
                    role = dos.get("role", dos.get("summary", ""))
                    if role:
                        print(f"       Dossier: {role}")

            # Show name info if available
            if "name_info" in analysis:
                ni = analysis["name_info"]
                sites = ", ".join(ni.get("sites", []))
                occ = ni.get("occurrences", 0)
                if sites or occ:
                    print(
                        f"       Name: {occ} occ, sites=[{sites}], gender={ni.get('gender', '?')}"
                    )

        # Anchored words summary
        if brief.anchored_words:
            print()
            print(f"--- Anchored/Reading Words ({len(brief.anchored_words)}) ---")
            for aw in brief.anchored_words:
                print(f"  {aw['word']:20s} = {aw['identification']} ({aw['confidence']})")

        # Named words summary
        if brief.named_words:
            print()
            print(f"--- Named Words ({len(brief.named_words)}) ---")
            for nw in brief.named_words:
                print(f"  {nw['word']:20s} ({nw['confidence']})")

        # Commodity logograms
        if brief.commodity_logograms:
            print()
            print(f"--- Commodity Logograms ({len(brief.commodity_logograms)}) ---")
            for logo in brief.commodity_logograms:
                print(f"  {logo}")

        # Cross-tablet links
        if brief.cross_tablet_links:
            print()
            print(f"--- Cross-Tablet Links ({len(brief.cross_tablet_links)}) ---")
            for link in brief.cross_tablet_links[:20]:  # Limit display
                word_type = link.get("word_type", "")
                print(
                    f"  {link['shared_word']:20s} -> {link['linked_tablet']:12s} "
                    f"({link['linked_site']}) [{word_type}]"
                )
            if len(brief.cross_tablet_links) > 20:
                print(f"  ... and {len(brief.cross_tablet_links) - 20} more links")

        # Hypothesis summary
        if brief.hypothesis_summary:
            print()
            print("--- Hypothesis Summary ---")
            for hyp, count in sorted(
                brief.hypothesis_summary.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"  {hyp}: {count} word(s)")

        print()
        print("=" * 72)


# ─── RECORD stage ────────────────────────────────────────────────────────────


class RecordStage:
    """
    Stage 4: RECORD - Register new readings after a reading attempt.

    - Registers new readings via anchor_tracker logic
    - Reports what cascade opportunities the new reading unlocks
    - Suggests updates to analysis index
    """

    def __init__(self):
        self.dependencies = {}
        self.anchors = {}

    def load_data(self) -> bool:
        """Load tracking data."""
        deps_data = _load_json(DEPENDENCIES_FILE)
        if deps_data:
            self.dependencies = deps_data.get("readings", {})
            print(f"Loaded {len(self.dependencies)} existing readings")
        else:
            print("Warning: No reading_dependencies.json found")

        anchors_data = _load_json(ANCHORS_FILE)
        if anchors_data:
            self.anchors = anchors_data.get("anchors", {})
            print(f"Loaded {len(self.anchors)} anchors")

        return True

    def record_reading(
        self,
        tablet_id: str,
        meaning: str = "",
        confidence: str = "SPECULATIVE",
        depends_on: Optional[List[str]] = None,
    ) -> Dict:
        """
        Record a completed reading attempt.

        Returns a summary of what was recorded and what follow-up actions
        are recommended.
        """
        result = {
            "tablet_id": tablet_id,
            "meaning": meaning,
            "confidence": confidence,
            "depends_on": depends_on or [],
            "actions": [],
            "cascade_opportunities": [],
        }

        # Check if reading file exists
        reading_file = COMPLETED_DIR / f"{tablet_id}_READING.md"
        alt_file = COMPLETED_DIR / f"{tablet_id.replace('+', '_')}_READING.md"

        if reading_file.exists() or alt_file.exists():
            result["actions"].append(f"Reading file already exists for {tablet_id}")
        else:
            result["actions"].append(
                f"Create reading file: analysis/completed/inscriptions/{tablet_id}_READING.md"
            )

        # Check if tablet reading is already tracked
        if tablet_id in self.dependencies:
            result["actions"].append(
                f"Reading '{tablet_id}' already tracked in reading_dependencies.json"
            )
        else:
            result["actions"].append(
                f"Register reading in reading_dependencies.json via: "
                f"python3 tools/anchor_tracker.py --register {tablet_id} "
                f"--depends-on {' '.join(depends_on or ['anchor_linear_b_comparison'])}"
            )

        # Suggest analysis index update
        result["actions"].append(
            f"Update linear-a-decipherer/ANALYSIS_INDEX.md with new entry for {tablet_id}"
        )

        # Suggest cascade check
        result["actions"].append(
            f"Check cascading effects: python3 tools/anchor_tracker.py --reading {tablet_id}"
        )

        return result

    def print_record_summary(self, result: Dict):
        """Print the recording summary."""
        print()
        print("=" * 72)
        print(f"RECORD SUMMARY: {result['tablet_id']}")
        print("=" * 72)
        print(f"  Meaning: {result.get('meaning', 'N/A')}")
        print(f"  Confidence: {result.get('confidence', 'N/A')}")
        if result.get("depends_on"):
            print(f"  Depends on: {', '.join(result['depends_on'])}")
        print()
        print("--- Required Actions ---")
        for i, action in enumerate(result.get("actions", []), 1):
            print(f"  {i}. {action}")
        print()
        print("=" * 72)


# ─── Output helpers ──────────────────────────────────────────────────────────


def print_queue(queue: List[QueueEntry], site_balanced: bool = False):
    """Print the reading queue in human-readable format."""
    label = "SITE-BALANCED " if site_balanced else ""
    print()
    print("=" * 90)
    print(f"{label}READING QUEUE ({len(queue)} tablets)")
    print("=" * 90)

    print(
        f"\n{'Rank':>4s}  {'Tablet':<14s} {'Site':<5s} {'Prior':>6s} "
        f"{'Ready':>6s} {'Boost':>6s} {'Words':>5s} {'Anch':>4s} "
        f"{'Unkn':>4s} {'Cov%':>5s} {'Arith':<10s} {'Type'}"
    )
    print("-" * 100)

    for i, entry in enumerate(queue, 1):
        print(
            f"{i:4d}  {entry.tablet_id:<14s} {entry.site:<5s} "
            f"{entry.priority_score:6.3f} {entry.readiness_score:6.3f} "
            f"{entry.cascade_boost:6.3f} {entry.total_words:5d} "
            f"{entry.anchored_words:4d} {entry.unknown_words:4d} "
            f"{entry.coverage_pct:5.1f} {entry.arithmetic_status:<10s} "
            f"{entry.document_type}"
        )

    # Site distribution summary
    site_counts = defaultdict(int)
    for entry in queue:
        site_counts[entry.site] += 1
    print()
    print("--- Site Distribution ---")
    for site, count in sorted(site_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {site}: {count}")

    print()
    print("=" * 90)


def save_queue(queue: List[QueueEntry], output_path: str):
    """Save the reading queue to a JSON file."""
    output = {
        "metadata": {
            "tool": "reading_pipeline.py",
            "stage": "SELECT",
            "tablets_queued": len(queue),
            "already_read_excluded": len(get_already_read_tablets()),
        },
        "queue": [asdict(entry) for entry in queue],
    }

    path = Path(output_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nQueue saved to: {path}")


def save_brief(brief: ReadingBrief, output_path: str):
    """Save a reading brief to a JSON file."""
    output = {
        "metadata": {
            "tool": "reading_pipeline.py",
            "stage": "PREPARE",
            "tablet_id": brief.tablet_id,
        },
        "brief": {
            "tablet_id": brief.tablet_id,
            "site": brief.site,
            "raw_text": brief.raw_text,
            "total_tokens": brief.total_tokens,
            "syllabic_words": brief.syllabic_words,
            "readiness_score": brief.readiness_score,
            "document_type": brief.document_type,
            "commodity_logograms": brief.commodity_logograms,
            "arithmetic": brief.arithmetic,
            "word_analyses": brief.word_analyses,
            "anchored_words": brief.anchored_words,
            "named_words": brief.named_words,
            "cross_tablet_links": brief.cross_tablet_links,
            "hypothesis_summary": brief.hypothesis_summary,
        },
    }

    path = Path(output_path)
    if not path.is_absolute():
        path = PROJECT_ROOT / path

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nBrief saved to: {path}")


# ─── Main ────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Reading Pipeline - automated tablet reading workflow (SELECT/PREPARE/RECORD)"
    )

    # Stage selection
    parser.add_argument(
        "--select",
        action="store_true",
        help="Stage 1: Score and rank unread tablets",
    )
    parser.add_argument(
        "--prepare",
        type=str,
        metavar="TABLET_ID",
        help="Stage 2: Prepare a reading brief for a specific tablet",
    )
    parser.add_argument(
        "--record",
        type=str,
        metavar="TABLET_ID",
        help="Stage 4: Record a completed reading attempt",
    )

    # Queue options
    parser.add_argument(
        "--queue",
        action="store_true",
        help="Alias for --select (show the reading queue)",
    )
    parser.add_argument(
        "--site-balanced",
        action="store_true",
        help="Interleave sites in the queue for diversity",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=0,
        help="Show top N tablets (0 = all unread)",
    )

    # Record options
    parser.add_argument(
        "--meaning",
        type=str,
        default="",
        help="Meaning/interpretation for --record",
    )
    parser.add_argument(
        "--confidence",
        type=str,
        default="SPECULATIVE",
        help=(
            "Confidence level for --record (SPECULATIVE|POSSIBLE|LOW|MEDIUM|PROBABLE|HIGH|CERTAIN)"
        ),
    )
    parser.add_argument(
        "--depends-on",
        type=str,
        nargs="*",
        help="Anchor dependencies for --record",
    )

    # Output
    parser.add_argument(
        "--output",
        type=str,
        help="Save results to JSON file",
    )

    args = parser.parse_args()

    # Default to --select if no stage specified
    if not any([args.select, args.prepare, args.record, args.queue]):
        args.select = True
        if args.top == 0:
            args.top = 20

    # ── Stage 1: SELECT / QUEUE ──
    if args.select or args.queue:
        selector = SelectStage()
        if not selector.load_data():
            sys.exit(1)

        top_n = args.top if args.top > 0 else 0
        queue = selector.build_queue(top_n=0)  # Build full queue first

        if args.site_balanced:
            queue = selector.site_balance(queue)

        # Apply top_n after balancing
        if top_n > 0:
            queue = queue[:top_n]

        print_queue(queue, site_balanced=args.site_balanced)

        if args.output:
            save_queue(queue, args.output)

    # ── Stage 2: PREPARE ──
    elif args.prepare:
        preparer = PrepareStage()
        if not preparer.load_data():
            sys.exit(1)

        brief = preparer.prepare_brief(args.prepare)
        if brief:
            preparer.print_brief(brief)
            if args.output:
                save_brief(brief, args.output)
        else:
            print(f"Error: Could not prepare brief for tablet {args.prepare}")
            sys.exit(1)

    # ── Stage 4: RECORD ──
    elif args.record:
        recorder = RecordStage()
        if not recorder.load_data():
            sys.exit(1)

        result = recorder.record_reading(
            tablet_id=args.record,
            meaning=args.meaning,
            confidence=args.confidence,
            depends_on=args.depends_on,
        )
        recorder.print_record_summary(result)

        if args.output:
            path = Path(args.output)
            if not path.is_absolute():
                path = PROJECT_ROOT / path
            with open(path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Record saved to: {path}")


if __name__ == "__main__":
    main()
