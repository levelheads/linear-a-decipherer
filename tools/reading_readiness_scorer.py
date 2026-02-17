#!/usr/bin/env python3
"""
Reading Readiness Scorer for Linear A

Given a tablet ID, scores how "readable" it is by combining all available evidence:
- Arithmetic verification status (corpus_auditor)
- Anchored/identified words (anchors, admin isomorphism)
- Named words (personal names, onomastic analysis)
- Formula words (contextual analysis)
- Morphological decomposition coverage
- Hypothesis result strength

Usage:
    python3 tools/reading_readiness_scorer.py --tablet HT9b
    python3 tools/reading_readiness_scorer.py --all
    python3 tools/reading_readiness_scorer.py --top 10
    python3 tools/reading_readiness_scorer.py --all --output data/reading_readiness.json

Attribution:
    Part of Linear A Decipherment Project
    Keystone tool: converts scattered evidence into actionable tablet rankings
"""

import json
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"


# Known commodity logograms (from corpus_auditor.py)
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
    "¹⁄₂",
    "½",
    "¹⁄₄",
    "¼",
    "³⁄₄",
    "¾",
    "¹⁄₃",
    "⅓",
    "²⁄₃",
    "⅔",
    "¹⁄₈",
    "⅛",
    "³⁄₈",
    "⅜",
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


@dataclass
class WordDetail:
    """Per-word readiness detail."""

    word: str
    position: int
    category: str  # 'anchored', 'named', 'formula', 'logogram', 'number', 'fraction', 'unknown', 'structural'
    identification: str  # What we know about it
    confidence: str  # CERTAIN, HIGH, PROBABLE, POSSIBLE, UNKNOWN
    hypothesis_support: Optional[str] = None  # Best hypothesis if any


@dataclass
class TabletReadiness:
    """Complete readiness assessment for a tablet."""

    tablet_id: str
    total_words: int  # Syllabic words only (excludes numbers, logograms, fractions)
    total_tokens: int  # All tokens including numbers, logograms
    anchored_words: int
    named_words: int
    formula_words: int
    logogram_count: int
    number_count: int
    unknown_words: int
    coverage_pct: float
    arithmetic_status: str  # VERIFIED, PARTIAL, MISMATCH, INCOMPLETE, NO_KURO
    document_type: str
    site: str
    readiness_score: float
    word_detail: List[Dict] = field(default_factory=list)


class ReadinessScorer:
    """
    Scores tablets by how readable they are using all accumulated evidence.
    """

    def __init__(self):
        self.corpus = {}
        self.inscriptions = {}
        self.anchors = {}
        self.hypothesis_results = {}
        self.admin_iso = {}
        self.morphological = {}
        self.contextual = {}
        self.personal_names = {}
        self.onomastic = {}
        self.audit_data = {}
        # Derived lookups
        self.known_names: Set[str] = set()
        self.formula_words: Set[str] = set()
        self.high_specificity_words: Dict[str, str] = {}  # word -> commodity
        self.morphological_words: Set[str] = set()
        self.positional_ids: Dict[str, str] = {}  # word -> identified role

    def load_data(self) -> bool:
        """Load all evidence data files."""
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

        # Load optional data files (non-fatal if missing)
        optional_files = {
            "anchors": DATA_DIR / "anchors.json",
            "hypothesis_results": DATA_DIR / "hypothesis_results.json",
            "admin_iso": DATA_DIR / "admin_isomorphism.json",
            "morphological": DATA_DIR / "morphological_predictions.json",
            "contextual": DATA_DIR / "contextual_analysis_full.json",
            "personal_names": DATA_DIR / "personal_names_comprehensive.json",
            "onomastic": DATA_DIR / "onomastic_analysis.json",
            "audit_data": DATA_DIR / "audit" / "corpus_audit.json",
        }

        for attr, path in optional_files.items():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    setattr(self, attr, json.load(f))
            except FileNotFoundError:
                pass  # Non-fatal
            except Exception as e:
                print(f"Warning: Error loading {path.name}: {e}")

        self._build_lookups()
        return True

    def _build_lookups(self):
        """Build derived lookup tables from loaded data."""
        # Extract known personal names
        if self.personal_names:
            names = self.personal_names.get("names", {})
            if isinstance(names, dict):
                self.known_names = set(names.keys())
            elif isinstance(names, list):
                self.known_names = {n.get("name", "") for n in names if isinstance(n, dict)}

        # Also get names from onomastic analysis
        if self.onomastic:
            profiles = self.onomastic.get("name_profiles", {})
            if isinstance(profiles, dict):
                self.known_names.update(profiles.keys())
            elif isinstance(profiles, list):
                for p in profiles:
                    if isinstance(p, dict) and "name" in p:
                        self.known_names.add(p["name"])

        # Extract formula words from contextual analysis
        if self.contextual:
            formulas = self.contextual.get("formulas", {})
            if isinstance(formulas, dict):
                for formula_name, formula_data in formulas.items():
                    if isinstance(formula_data, dict):
                        elements = formula_data.get("elements", [])
                        if isinstance(elements, list):
                            self.formula_words.update(elements)
                        # Also check for 'words' key
                        words = formula_data.get("words", [])
                        if isinstance(words, list):
                            self.formula_words.update(words)
            elif isinstance(formulas, list):
                for f in formulas:
                    if isinstance(f, dict):
                        elements = f.get("elements", f.get("words", []))
                        if isinstance(elements, list):
                            self.formula_words.update(elements)

        # Extract high-specificity co-occurrence from audit
        if self.audit_data:
            coocc = self.audit_data.get("cooccurrence_summary", {})
            for token, data in coocc.items():
                if isinstance(data, dict):
                    spec = data.get("specificity", 0)
                    if spec >= 0.8:
                        self.high_specificity_words[token] = data.get("primary", "UNKNOWN")

        # Extract morphological coverage
        if self.morphological:
            decomps = self.morphological.get("decompositions", {})
            if isinstance(decomps, dict):
                self.morphological_words = set(decomps.keys())
            elif isinstance(decomps, list):
                self.morphological_words = {
                    d.get("word", "") for d in decomps if isinstance(d, dict)
                }

        # Extract positional identifications from admin isomorphism
        if self.admin_iso:
            pos_ids = self.admin_iso.get("positional_identifications", {})
            if isinstance(pos_ids, dict):
                for word, data in pos_ids.items():
                    if isinstance(data, dict):
                        self.positional_ids[word] = data.get(
                            "role", data.get("identification", "identified")
                        )
                    elif isinstance(data, str):
                        self.positional_ids[word] = data
            elif isinstance(pos_ids, list):
                for item in pos_ids:
                    if isinstance(item, dict) and "word" in item:
                        self.positional_ids[item["word"]] = item.get("role", "identified")

        print(f"  Known names: {len(self.known_names)}")
        print(f"  Formula words: {len(self.formula_words)}")
        print(f"  High-specificity words: {len(self.high_specificity_words)}")
        print(f"  Morphological words: {len(self.morphological_words)}")
        print(f"  Positional IDs: {len(self.positional_ids)}")

    def _is_number(self, token: str) -> bool:
        """Check if token is a number."""
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

    def _is_logogram(self, token: str) -> bool:
        """Check if token is a commodity logogram."""
        if token in COMMODITY_LOGOGRAMS:
            return True
        if "+" in token:
            base = token.split("+")[0]
            return base in {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}
        return False

    def _is_word(self, token: str) -> bool:
        """Check if token is a syllabic word."""
        if token in {"\n", "𐄁", "", " ", "—", ",", ".", "[", "]"}:
            return False
        if self._is_number(token):
            return False
        if self._is_logogram(token):
            return False
        if token.startswith('"'):
            return False
        if token == "*":
            return False
        return True

    def _extract_site(self, tablet_id: str) -> str:
        """Extract site code from tablet ID."""
        match = re.match(r"^([A-Z]+)", tablet_id)
        return match.group(1) if match else "UNKNOWN"

    def _get_arithmetic_status(self, tablet_id: str) -> str:
        """Get arithmetic verification status for a tablet."""
        if not self.audit_data:
            return "NO_DATA"
        totals = self.audit_data.get("totals_validation", [])
        for t in totals:
            if t.get("tablet_id") == tablet_id:
                return t.get("confidence", "UNKNOWN")
        # Check if tablet has KU-RO at all
        tablet_data = self.inscriptions.get(tablet_id, {})
        words = tablet_data.get("transliteratedWords", [])
        if "KU-RO" in words:
            return "NOT_AUDITED"
        return "NO_KURO"

    def _get_document_type(self, tablet_id: str) -> str:
        """Infer document type from contextual analysis."""
        if not self.contextual:
            return "unknown"
        doc_structures = self.contextual.get("document_structures", {})
        if isinstance(doc_structures, dict) and tablet_id in doc_structures:
            return doc_structures[tablet_id].get("type", "administrative")

        # Infer from content
        tablet_data = self.inscriptions.get(tablet_id, {})
        words = tablet_data.get("transliteratedWords", [])
        word_set = set(words)

        # Check for libation formula elements
        libation_markers = {"JA-SA-SA-RA-ME", "A-TA-I-*301-WA-JA", "I-DA-MA-TE"}
        if word_set & libation_markers:
            return "religious/libation"

        # Check for KU-RO (administrative list)
        if "KU-RO" in word_set:
            return "administrative/list"

        # Check for commodity logograms
        has_commodities = any(self._is_logogram(w) for w in words)
        has_numbers = any(self._is_number(w) for w in words)
        if has_commodities and has_numbers:
            return "administrative/commodity"

        return "administrative"

    def _get_hypothesis_support(self, word: str) -> Optional[str]:
        """Get best hypothesis for a word from hypothesis_results."""
        if not self.hypothesis_results:
            return None
        analyses = self.hypothesis_results.get("word_analyses", {})
        # Try uppercase
        word_data = analyses.get(word.upper(), analyses.get(word, None))
        if not word_data:
            return None
        synthesis = word_data.get("synthesis", {})
        best_hyp = synthesis.get("best_hypothesis", "")
        max_conf = synthesis.get("max_confidence", "")
        if best_hyp and max_conf and max_conf not in ("UNKNOWN", "NONE", ""):
            return best_hyp
        return None

    def _classify_word(self, word: str, position: int, all_words: List[str]) -> WordDetail:
        """Classify a single word's identification status."""
        word_upper = word.upper()

        # Check known function words
        if word_upper in KNOWN_FUNCTION_WORDS or word in KNOWN_FUNCTION_WORDS:
            func = KNOWN_FUNCTION_WORDS.get(word_upper, KNOWN_FUNCTION_WORDS.get(word, "function"))
            return WordDetail(
                word=word,
                position=position,
                category="anchored",
                identification=func,
                confidence="HIGH",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check positional identifications from admin isomorphism
        if word_upper in self.positional_ids or word in self.positional_ids:
            role = self.positional_ids.get(word_upper, self.positional_ids.get(word, "identified"))
            return WordDetail(
                word=word,
                position=position,
                category="anchored",
                identification=f"positional: {role}",
                confidence="PROBABLE",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check high-specificity commodity words
        if word_upper in self.high_specificity_words or word in self.high_specificity_words:
            commodity = self.high_specificity_words.get(
                word_upper, self.high_specificity_words.get(word, "UNKNOWN")
            )
            return WordDetail(
                word=word,
                position=position,
                category="anchored",
                identification=f"commodity-specific ({commodity})",
                confidence="POSSIBLE",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check personal names
        if word_upper in self.known_names or word in self.known_names:
            return WordDetail(
                word=word,
                position=position,
                category="named",
                identification="personal name",
                confidence="PROBABLE",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check formula words
        if word_upper in self.formula_words or word in self.formula_words:
            return WordDetail(
                word=word,
                position=position,
                category="formula",
                identification="formula element",
                confidence="POSSIBLE",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check morphological decomposition
        if word_upper in self.morphological_words or word in self.morphological_words:
            return WordDetail(
                word=word,
                position=position,
                category="anchored",
                identification="morphologically decomposed",
                confidence="POSSIBLE",
                hypothesis_support=self._get_hypothesis_support(word),
            )

        # Check if hypothesis testing gives any support
        hyp = self._get_hypothesis_support(word)
        if hyp:
            return WordDetail(
                word=word,
                position=position,
                category="unknown",
                identification="hypothesis-tested only",
                confidence="SPECULATIVE",
                hypothesis_support=hyp,
            )

        # Truly unknown
        return WordDetail(
            word=word,
            position=position,
            category="unknown",
            identification="unidentified",
            confidence="UNKNOWN",
        )

    def score_tablet(self, tablet_id: str) -> Optional[TabletReadiness]:
        """Score a single tablet's reading readiness."""
        tablet_data = self.inscriptions.get(tablet_id)
        if not tablet_data:
            return None

        all_tokens = tablet_data.get("transliteratedWords", [])

        # Classify each token
        word_details = []
        syllabic_words = []
        logogram_count = 0
        number_count = 0
        pos = 0

        for token in all_tokens:
            if token in {"\n", "𐄁", "", " ", "—"}:
                continue

            if self._is_logogram(token):
                logogram_count += 1
                word_details.append(
                    WordDetail(
                        word=token,
                        position=pos,
                        category="logogram",
                        identification=token,
                        confidence="CERTAIN",
                    )
                )
            elif self._is_number(token):
                number_count += 1
                word_details.append(
                    WordDetail(
                        word=token,
                        position=pos,
                        category="number",
                        identification="quantity",
                        confidence="CERTAIN",
                    )
                )
            elif self._is_word(token):
                detail = self._classify_word(token, pos, all_tokens)
                word_details.append(detail)
                syllabic_words.append(detail)

            pos += 1

        total_words = len(syllabic_words)
        if total_words == 0:
            return None

        # Count categories
        anchored = sum(1 for d in syllabic_words if d.category == "anchored")
        named = sum(1 for d in syllabic_words if d.category == "named")
        formula = sum(1 for d in syllabic_words if d.category == "formula")
        unknown = sum(1 for d in syllabic_words if d.category == "unknown")

        identified = total_words - unknown
        coverage_pct = (identified / total_words * 100) if total_words > 0 else 0

        # Arithmetic status
        arith_status = self._get_arithmetic_status(tablet_id)

        # Document type
        doc_type = self._get_document_type(tablet_id)

        # Composite readiness score (0-1)
        score = self._compute_readiness_score(
            total_words=total_words,
            anchored=anchored,
            named=named,
            formula=formula,
            unknown=unknown,
            logogram_count=logogram_count,
            number_count=number_count,
            arith_status=arith_status,
        )

        return TabletReadiness(
            tablet_id=tablet_id,
            total_words=total_words,
            total_tokens=len(word_details),
            anchored_words=anchored,
            named_words=named,
            formula_words=formula,
            logogram_count=logogram_count,
            number_count=number_count,
            unknown_words=unknown,
            coverage_pct=round(coverage_pct, 1),
            arithmetic_status=arith_status,
            document_type=doc_type,
            site=self._extract_site(tablet_id),
            readiness_score=round(score, 3),
            word_detail=[asdict(d) for d in word_details],
        )

    def _compute_readiness_score(
        self,
        total_words: int,
        anchored: int,
        named: int,
        formula: int,
        unknown: int,
        logogram_count: int,
        number_count: int,
        arith_status: str,
    ) -> float:
        """
        Compute composite readiness score (0-1).

        Weights:
        - Word coverage (anchored + named + formula): 40%
        - Arithmetic verification: 25%
        - Structural richness (logograms + numbers): 15%
        - Tablet size bonus (more words = more context): 10%
        - Low unknown penalty: 10%
        """
        # Coverage component (0-1)
        identified = total_words - unknown
        coverage = identified / total_words if total_words > 0 else 0

        # Arithmetic component (0-1)
        arith_scores = {
            "VERIFIED": 1.0,
            "PARTIAL": 0.7,
            "MISMATCH": 0.3,
            "INCOMPLETE": 0.1,
            "NO_KURO": 0.2,
            "NOT_AUDITED": 0.15,
            "NO_DATA": 0.0,
        }
        arith = arith_scores.get(arith_status, 0.0)

        # Structural richness (0-1): tablets with logograms and numbers are more parseable
        total_structural = logogram_count + number_count
        total_all = total_words + total_structural
        structural = min(total_structural / max(total_all, 1), 1.0)

        # Size bonus: larger tablets provide more context (diminishing returns)
        import math

        size_bonus = min(math.log2(max(total_words, 1)) / 5.0, 1.0)  # cap at ~32 words

        # Unknown penalty
        unknown_ratio = unknown / total_words if total_words > 0 else 1.0
        unknown_penalty = 1.0 - unknown_ratio

        # Weighted composite
        score = (
            0.40 * coverage
            + 0.25 * arith
            + 0.15 * structural
            + 0.10 * size_bonus
            + 0.10 * unknown_penalty
        )

        return min(max(score, 0.0), 1.0)

    def score_all(self) -> List[TabletReadiness]:
        """Score all tablets and return sorted by readiness."""
        results = []
        for tablet_id in self.inscriptions:
            result = self.score_tablet(tablet_id)
            if result:
                results.append(result)
        results.sort(key=lambda r: r.readiness_score, reverse=True)
        return results

    def print_tablet_report(self, result: TabletReadiness):
        """Print detailed report for a single tablet."""
        print(f"\n{'=' * 70}")
        print(f"READING READINESS: {result.tablet_id}")
        print(f"{'=' * 70}")
        print(f"  Site: {result.site}")
        print(f"  Document type: {result.document_type}")
        print(f"  Arithmetic status: {result.arithmetic_status}")
        print(f"  Readiness score: {result.readiness_score:.3f}")
        print()
        print(f"  Syllabic words: {result.total_words}")
        print(f"    Anchored: {result.anchored_words}")
        print(f"    Named: {result.named_words}")
        print(f"    Formula: {result.formula_words}")
        print(f"    Unknown: {result.unknown_words}")
        print(f"  Logograms: {result.logogram_count}")
        print(f"  Numbers: {result.number_count}")
        print(f"  Coverage: {result.coverage_pct}%")

        print("\n  --- Word Details ---")
        for d in result.word_detail:
            cat = d["category"]
            marker = {
                "anchored": "A",
                "named": "N",
                "formula": "F",
                "logogram": "L",
                "number": "#",
                "unknown": "?",
            }.get(cat, ".")
            hyp = f" [{d['hypothesis_support']}]" if d.get("hypothesis_support") else ""
            print(f"    [{marker}] {d['word']:20s} → {d['identification']}{hyp}")

    def print_ranking(self, results: List[TabletReadiness], top_n: int = 0):
        """Print ranked tablet list."""
        print(f"\n{'=' * 70}")
        print("TABLET READING READINESS RANKING")
        print(f"{'=' * 70}")

        show = results[:top_n] if top_n > 0 else results
        print(
            f"\n{'Rank':>4s}  {'Tablet':<14s} {'Score':>6s} {'Words':>5s} "
            f"{'Anch':>4s} {'Name':>4s} {'Unkn':>4s} {'Cov%':>5s} {'Arith':<10s} {'Type'}"
        )
        print("-" * 85)

        for i, r in enumerate(show, 1):
            print(
                f"{i:4d}  {r.tablet_id:<14s} {r.readiness_score:6.3f} {r.total_words:5d} "
                f"{r.anchored_words:4d} {r.named_words:4d} {r.unknown_words:4d} "
                f"{r.coverage_pct:5.1f} {r.arithmetic_status:<10s} {r.document_type}"
            )

        # Summary statistics
        if results:
            avg_score = sum(r.readiness_score for r in results) / len(results)
            verified = sum(1 for r in results if r.arithmetic_status == "VERIFIED")
            zero_unknown = sum(1 for r in results if r.unknown_words == 0)
            print(f"\n  Total tablets scored: {len(results)}")
            print(f"  Average readiness: {avg_score:.3f}")
            print(f"  Arithmetically verified: {verified}")
            print(f"  Fully identified (0 unknown): {zero_unknown}")

    def save_results(self, results: List[TabletReadiness], output_path: str):
        """Save results to JSON."""
        output = {
            "metadata": {
                "tool": "reading_readiness_scorer.py",
                "tablets_scored": len(results),
                "data_sources": {
                    "corpus": str(CORPUS_FILE),
                    "known_names": len(self.known_names),
                    "formula_words": len(self.formula_words),
                    "high_specificity_words": len(self.high_specificity_words),
                    "morphological_words": len(self.morphological_words),
                    "positional_ids": len(self.positional_ids),
                },
            },
            "rankings": [
                {
                    "tablet_id": r.tablet_id,
                    "readiness_score": r.readiness_score,
                    "total_words": r.total_words,
                    "total_tokens": r.total_tokens,
                    "anchored_words": r.anchored_words,
                    "named_words": r.named_words,
                    "formula_words": r.formula_words,
                    "unknown_words": r.unknown_words,
                    "logogram_count": r.logogram_count,
                    "number_count": r.number_count,
                    "coverage_pct": r.coverage_pct,
                    "arithmetic_status": r.arithmetic_status,
                    "document_type": r.document_type,
                    "site": r.site,
                    "word_detail": r.word_detail,
                }
                for r in results
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Reading Readiness Scorer - rank tablets by readability"
    )
    parser.add_argument("--tablet", type=str, help="Score a single tablet")
    parser.add_argument("--all", action="store_true", help="Score all tablets")
    parser.add_argument("--top", type=int, default=0, help="Show top N most readable tablets")
    parser.add_argument("--output", type=str, help="Save results to JSON file")

    args = parser.parse_args()

    if not any([args.tablet, args.all, args.top]):
        args.top = 20  # Default: show top 20

    scorer = ReadinessScorer()
    if not scorer.load_data():
        sys.exit(1)

    if args.tablet:
        result = scorer.score_tablet(args.tablet)
        if result:
            scorer.print_tablet_report(result)
        else:
            print(f"Tablet {args.tablet} not found in corpus")
            sys.exit(1)
    else:
        results = scorer.score_all()
        top_n = args.top if args.top > 0 else 0
        scorer.print_ranking(results, top_n=top_n)

        if args.output:
            scorer.save_results(results, args.output)


if __name__ == "__main__":
    main()
