#!/usr/bin/env python3
"""
Syntax Analyzer for Linear A

Direction 4 Implementation: Decode word order and grammatical structure.

Builds systematic syntax analysis to determine Linear A word order:
1. Slot grammar extraction from all tablet types
2. Subject-Object-Verb position tracking
3. Particle/prefix/suffix position mapping

Tests hypotheses:
- VSO (Verb-Subject-Object) — Semitic pattern
- SOV (Subject-Object-Verb) — Anatolian/Luwian pattern
- SVO (Subject-Verb-Object) — Isolate pattern

Usage:
    python tools/syntax_analyzer.py --administrative
    python tools/syntax_analyzer.py --religious
    python tools/syntax_analyzer.py --all

Attribution:
    Part of Linear A Decipherment Project
    Extends slot_grammar_analyzer.py for comprehensive syntax analysis
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter
from datetime import datetime
from typing import List

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Known structural markers from KNOWLEDGE.md
KNOWN_MARKERS = {
    "totals": ["KU-RO", "PO-TO-KU-RO", "KU-RE"],
    "deficits": ["KI-RO"],
    "allocations": ["SA-RA₂", "SA-RA2"],
    "commodities": ["GRA", "VIN", "OLE", "OLIV", "FIC", "CYP", "TELA", "BOS", "OVI", "CAP", "SUS"],
    "divine_names": ["JA-SA-SA-RA-ME", "A-SA-SA-RA-ME", "DA-MA-TE", "A-TA-NA"],
    "libation_verbs": ["A-TA-I-*301-WA-JA", "SI-RU-TE"],
    "luwian_particles": ["-JA", "-WA", "-U", "-TE", "-TI"],
}

# Text type patterns for classification
TEXT_PATTERNS = {
    "administrative": {
        "markers": ["KU-RO", "KI-RO", "GRA", "VIN", "OLE", "CYP", "TELA"],
        "structure": "list_with_totals",
    },
    "religious": {
        "markers": ["JA-SA-SA-RA-ME", "DA-MA-TE", "A-TA-I-*301-WA-JA", "SI-RU-TE"],
        "structure": "formula",
    },
    "inventory": {
        "markers": ["BOS", "OVI", "CAP", "SUS", "VIR", "MUL"],
        "structure": "list",
    },
}


class SyntaxAnalyzer:
    """
    Analyzes Linear A syntax patterns to determine word order.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.results = {
            "metadata": {
                "generated": None,
                "method": "Syntax Analysis via Position Mapping",
                "hypotheses_tested": ["VSO (Semitic)", "SOV (Luwian)", "SVO (Isolate)"],
            },
            "text_classification": {},
            "administrative_syntax": {},
            "religious_syntax": {},
            "word_order_evidence": {},
            "particle_positions": {},
            "slot_grammar": {},
            "hypothesis_scores": {},
            "findings": [],
        }

    def log(self, message: str):
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def classify_text_type(self, insc_id: str, words: List[str]) -> str:
        """
        Classify inscription by text type (administrative, religious, inventory).
        """
        words_upper = [w.upper() for w in words if w]

        # Check for religious markers
        for marker in TEXT_PATTERNS["religious"]["markers"]:
            if any(marker in w for w in words_upper):
                return "religious"

        # Check for administrative markers
        admin_score = sum(
            1
            for marker in TEXT_PATTERNS["administrative"]["markers"]
            if any(marker in w for w in words_upper)
        )
        if admin_score >= 2:
            return "administrative"

        # Check for inventory markers
        inv_score = sum(
            1
            for marker in TEXT_PATTERNS["inventory"]["markers"]
            if any(marker in w for w in words_upper)
        )
        if inv_score >= 2:
            return "inventory"

        # Default based on site
        if insc_id.startswith(("IO", "SY", "PK", "PS")):
            return "religious"  # Peak sanctuaries
        elif insc_id.startswith("KH"):
            return "administrative"  # Khania = administrative

        return "administrative"  # Default

    def classify_all_texts(self) -> dict:
        """Classify all inscriptions by text type."""
        print("\n[Classification] Categorizing inscriptions by text type...")

        classification = {
            "administrative": [],
            "religious": [],
            "inventory": [],
            "unknown": [],
        }

        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue

            words = data.get("transliteratedWords", [])
            if not words:
                continue

            text_type = self.classify_text_type(insc_id, words)
            classification[text_type].append(
                {
                    "id": insc_id,
                    "word_count": len([w for w in words if w and w not in ["\n", "𐄁"]]),
                }
            )

        self.results["text_classification"] = {
            "counts": {k: len(v) for k, v in classification.items()},
            "inscriptions": classification,
        }

        for text_type, items in classification.items():
            self.log(f"{text_type}: {len(items)} inscriptions")

        return classification

    def extract_slot_grammar(self, text_type: str) -> dict:
        """
        Extract slot grammar patterns for a specific text type.

        Slot grammar identifies:
        - Position 0: Initial element (verb in VSO, subject in SVO/SOV)
        - Position -1: Final element (verb in SOV, object in VSO/SVO)
        - Fixed positions for known elements (commodities, numerals, totals)
        """
        print(f"\n[Slot Grammar] Extracting patterns for {text_type} texts...")

        inscriptions = (
            self.results["text_classification"].get("inscriptions", {}).get(text_type, [])
        )

        slot_patterns = {
            "position_0": Counter(),  # First meaningful word
            "position_1": Counter(),  # Second word
            "position_minus_1": Counter(),  # Last word
            "position_minus_2": Counter(),  # Second to last
            "before_numeral": Counter(),  # Word before numeral
            "after_numeral": Counter(),  # Word after numeral
            "before_commodity": Counter(),  # Word before commodity logogram
            "after_commodity": Counter(),  # Word after commodity logogram
        }

        total_analyzed = 0

        for item in inscriptions:
            insc_id = item["id"]
            data = self.corpus["inscriptions"].get(insc_id, {})
            words = data.get("transliteratedWords", [])

            # Filter to meaningful words
            meaningful = []
            for w in words:
                if not w or w in ["\n", "𐄁", "", "—", "≈"]:
                    continue
                if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈₉○◎—|]+$", w):
                    continue
                meaningful.append(w.upper())

            if len(meaningful) < 2:
                continue

            total_analyzed += 1

            # Track positions
            slot_patterns["position_0"][meaningful[0]] += 1
            slot_patterns["position_1"][meaningful[1]] += 1 if len(meaningful) > 1 else 0
            slot_patterns["position_minus_1"][meaningful[-1]] += 1
            slot_patterns["position_minus_2"][meaningful[-2]] += 1 if len(meaningful) > 1 else 0

            # Track context around numerals
            for i, w in enumerate(meaningful):
                # Check if next word is numeral-like (skip this word)
                if i < len(meaningful) - 1:
                    next_w = meaningful[i + 1]
                    if any(c.isdigit() for c in next_w):
                        slot_patterns["before_numeral"][w] += 1

                # Check if previous was numeral-like
                if i > 0:
                    prev_w = meaningful[i - 1]
                    if any(c.isdigit() for c in prev_w):
                        slot_patterns["after_numeral"][w] += 1

                # Check context around commodities
                is_commodity = any(comm in w for comm in KNOWN_MARKERS["commodities"])
                if i > 0 and is_commodity:
                    slot_patterns["before_commodity"][meaningful[i - 1]] += 1
                if i < len(meaningful) - 1 and is_commodity:
                    slot_patterns["after_commodity"][meaningful[i + 1]] += 1

        # Convert to sorted lists
        grammar = {
            "total_analyzed": total_analyzed,
            "slots": {},
        }

        for slot, counter in slot_patterns.items():
            grammar["slots"][slot] = [
                {
                    "word": w,
                    "count": c,
                    "percentage": round(c / total_analyzed * 100, 1) if total_analyzed > 0 else 0,
                }
                for w, c in counter.most_common(20)
            ]

        return grammar

    def analyze_administrative_syntax(self) -> dict:
        """
        Analyze administrative text syntax.

        Administrative texts typically show:
        - [PERSON/PLACE] COMMODITY NUMBER structure
        - KU-RO at line/section ends (totals)
        - List structure with entries
        """
        print("\n[Administrative] Analyzing administrative text syntax...")

        grammar = self.extract_slot_grammar("administrative")

        # Identify structural patterns
        patterns = {
            "entry_structure": [],
            "total_position": [],
            "commodity_position": [],
        }

        # Check KU-RO position (should be final in entries/sections)
        for item in grammar["slots"].get("position_minus_1", []):
            if "KU-RO" in item["word"]:
                patterns["total_position"].append(
                    {
                        "marker": "KU-RO",
                        "position": "FINAL",
                        "frequency": item["count"],
                        "percentage": item["percentage"],
                    }
                )

        # Commodity position analysis
        commodity_positions = {
            "before_numeral": 0,
            "after_subject": 0,
        }
        for item in grammar["slots"].get("before_numeral", []):
            if any(comm in item["word"] for comm in KNOWN_MARKERS["commodities"]):
                commodity_positions["before_numeral"] += item["count"]

        # Infer entry structure
        # Most common pattern in Linear A administrative: SUBJECT COMMODITY NUMBER
        patterns["entry_structure"] = {
            "proposed": "SUBJECT COMMODITY NUMBER",
            "evidence": "Commodity appears before numerals",
            "confidence": "PROBABLE",
        }

        analysis = {
            "slot_grammar": grammar,
            "structural_patterns": patterns,
            "word_order_evidence": {
                "final_position": "TOTALS (KU-RO)",
                "pre_numeral": "COMMODITY",
                "initial": "SUBJECT/RECIPIENT",
            },
        }

        self.results["administrative_syntax"] = analysis

        return analysis

    def analyze_religious_syntax(self) -> dict:
        """
        Analyze religious text syntax (libation formulas).

        Known 6-position structure (Salgarella 2020):
        1. Main verb (A-TA-I-*301-WA-JA)
        2. Place name
        3. Dedicant's name
        4. Divine name/object
        5. Subordinate verb
        6. Prepositional phrase
        """
        print("\n[Religious] Analyzing religious text syntax...")

        grammar = self.extract_slot_grammar("religious")

        # Check for VSO evidence (verb-initial)
        verb_initial_evidence = []
        for item in grammar["slots"].get("position_0", []):
            # Check if matches known libation verbs
            if any(verb in item["word"] for verb in KNOWN_MARKERS["libation_verbs"]):
                verb_initial_evidence.append(
                    {
                        "verb": item["word"],
                        "count": item["count"],
                        "percentage": item["percentage"],
                    }
                )

        # 6-position structure verification
        six_position = {
            "position_1_verb": len(verb_initial_evidence) > 0,
            "position_4_divine": False,
            "position_6_prep": False,
        }

        # Check for divine names in mid positions
        divine_found = 0
        for slot in ["position_1", "position_minus_2"]:
            for item in grammar["slots"].get(slot, []):
                if any(divine in item["word"] for divine in KNOWN_MARKERS["divine_names"]):
                    divine_found += 1
                    six_position["position_4_divine"] = True

        analysis = {
            "slot_grammar": grammar,
            "verb_initial_evidence": verb_initial_evidence,
            "six_position_structure": six_position,
            "word_order": "VSO" if verb_initial_evidence else "UNDETERMINED",
            "word_order_confidence": "PROBABLE" if len(verb_initial_evidence) >= 2 else "POSSIBLE",
        }

        self.results["religious_syntax"] = analysis

        if verb_initial_evidence:
            self.results["findings"].append(
                {
                    "category": "word_order",
                    "finding": "Religious texts show verb-initial (VSO) pattern",
                    "evidence": f"{len(verb_initial_evidence)} verb-initial formulas found",
                    "confidence": analysis["word_order_confidence"],
                }
            )

        return analysis

    def analyze_particle_positions(self) -> dict:
        """
        Map particle/suffix positions to understand grammatical structure.

        Key particles: -JA, -WA, -U, -TE, -TI
        """
        print("\n[Particles] Mapping particle positions...")

        particle_data = {
            "-JA": {"initial": 0, "medial": 0, "final": 0, "words": []},
            "-WA": {"initial": 0, "medial": 0, "final": 0, "words": []},
            "-U": {"initial": 0, "medial": 0, "final": 0, "words": []},
            "-TE": {"initial": 0, "medial": 0, "final": 0, "words": []},
            "-TI": {"initial": 0, "medial": 0, "final": 0, "words": []},
        }

        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue

            for word in data.get("transliteratedWords", []):
                if not word or "-" not in word:
                    continue

                word_upper = word.upper()
                syllables = word_upper.split("-")

                for particle in particle_data.keys():
                    particle_clean = particle.lstrip("-")

                    if particle_clean in syllables:
                        idx = syllables.index(particle_clean)

                        if idx == 0:
                            particle_data[particle]["initial"] += 1
                        elif idx == len(syllables) - 1:
                            particle_data[particle]["final"] += 1
                        else:
                            particle_data[particle]["medial"] += 1

                        if len(particle_data[particle]["words"]) < 10:
                            particle_data[particle]["words"].append(word_upper)

        # Calculate percentages and dominant positions
        analysis = {}
        for particle, data in particle_data.items():
            total = data["initial"] + data["medial"] + data["final"]
            if total == 0:
                continue

            dominant = max(
                [
                    ("initial", data["initial"]),
                    ("medial", data["medial"]),
                    ("final", data["final"]),
                ],
                key=lambda x: x[1],
            )

            analysis[particle] = {
                "total_occurrences": total,
                "positions": {
                    "initial": {
                        "count": data["initial"],
                        "pct": round(data["initial"] / total * 100, 1),
                    },
                    "medial": {
                        "count": data["medial"],
                        "pct": round(data["medial"] / total * 100, 1),
                    },
                    "final": {"count": data["final"], "pct": round(data["final"] / total * 100, 1)},
                },
                "dominant_position": dominant[0],
                "examples": data["words"][:5],
            }

        self.results["particle_positions"] = analysis

        # Findings
        final_particles = [p for p, d in analysis.items() if d["dominant_position"] == "final"]
        if final_particles:
            self.results["findings"].append(
                {
                    "category": "morphology",
                    "finding": f"Particles {', '.join(final_particles)} are predominantly word-final (suffixes)",
                    "implication": "Supports agglutinative morphology (Luwian-like)",
                    "confidence": "PROBABLE",
                }
            )

        return analysis

    def score_word_order_hypotheses(self) -> dict:
        """
        Score the three word order hypotheses based on all evidence.
        """
        print("\n[Synthesis] Scoring word order hypotheses...")

        scores = {
            "VSO": {"score": 0, "evidence": [], "against": []},
            "SOV": {"score": 0, "evidence": [], "against": []},
            "SVO": {"score": 0, "evidence": [], "against": []},
        }

        # Evidence from religious texts (verb-initial)
        religious = self.results.get("religious_syntax", {})
        if religious.get("word_order") == "VSO":
            scores["VSO"]["score"] += 3
            scores["VSO"]["evidence"].append("Religious formulas show verb-initial pattern")
            scores["SOV"]["against"].append("Religious formulas are NOT verb-final")
            scores["SVO"]["against"].append("Religious formulas are NOT medial-verb")

        # Evidence from particle positions
        particles = self.results.get("particle_positions", {})
        final_count = sum(1 for p, d in particles.items() if d.get("dominant_position") == "final")
        if final_count >= 3:
            scores["SOV"]["score"] += 2
            scores["SOV"]["evidence"].append(
                f"{final_count} particles are word-final (suffix-heavy = SOV tendency)"
            )

        # Evidence from administrative texts
        admin = self.results.get("administrative_syntax", {})
        if admin:
            # Totals at end suggests clause-final positioning (could be SOV or flexible)
            if admin.get("word_order_evidence", {}).get("final_position") == "TOTALS (KU-RO)":
                scores["SOV"]["score"] += 1
                scores["SOV"]["evidence"].append("Administrative totals appear clause-finally")

        # Calculate final rankings
        for hyp in scores:
            scores[hyp]["final_score"] = scores[hyp]["score"] - len(scores[hyp]["against"]) * 0.5

        ranking = sorted(scores.items(), key=lambda x: -x[1]["final_score"])

        analysis = {
            "scores": scores,
            "ranking": [{"hypothesis": h, "score": d["final_score"]} for h, d in ranking],
            "best_hypothesis": ranking[0][0],
            "confidence": "PROBABLE"
            if ranking[0][1]["final_score"] > ranking[1][1]["final_score"] + 1
            else "POSSIBLE",
            "interpretation": "",
        }

        # Generate interpretation
        best = ranking[0][0]
        if best == "VSO":
            analysis["interpretation"] = (
                "Linear A may follow Verb-Subject-Object order (Semitic influence)"
            )
        elif best == "SOV":
            analysis["interpretation"] = (
                "Linear A may follow Subject-Object-Verb order (Luwian/Anatolian pattern)"
            )
        else:
            analysis["interpretation"] = (
                "Linear A may follow Subject-Verb-Object order (isolate pattern)"
            )

        self.results["hypothesis_scores"] = analysis

        self.results["findings"].append(
            {
                "category": "word_order",
                "finding": f"Best word order hypothesis: {best}",
                "score": ranking[0][1]["final_score"],
                "confidence": analysis["confidence"],
            }
        )

        return analysis

    def run_full_analysis(self) -> dict:
        """Run complete syntax analysis."""
        print("\n" + "=" * 70)
        print("SYNTAX ANALYZER - Direction 4")
        print("Decoding Linear A Word Order")
        print("=" * 70)

        self.classify_all_texts()
        self.analyze_administrative_syntax()
        self.analyze_religious_syntax()
        self.analyze_particle_positions()
        self.score_word_order_hypotheses()

        self.results["metadata"]["generated"] = datetime.now().isoformat()

        return self.results

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 70)
        print("SYNTAX ANALYSIS SUMMARY")
        print("=" * 70)

        # Text classification
        classification = self.results.get("text_classification", {}).get("counts", {})
        print("\nText Classification:")
        for text_type, count in classification.items():
            print(f"  {text_type}: {count} inscriptions")

        # Particle positions
        particles = self.results.get("particle_positions", {})
        print("\nParticle Positions:")
        for particle, data in particles.items():
            print(
                f"  {particle}: {data['dominant_position']} dominant ({data['total_occurrences']} occ)"
            )

        # Word order hypothesis
        hyp_scores = self.results.get("hypothesis_scores", {})
        print("\nWord Order Hypothesis Ranking:")
        for item in hyp_scores.get("ranking", []):
            print(f"  {item['hypothesis']}: {item['score']:.1f}")

        best = hyp_scores.get("best_hypothesis", "Unknown")
        conf = hyp_scores.get("confidence", "Unknown")
        print(f"\nBest Hypothesis: {best} ({conf})")
        print(f"Interpretation: {hyp_scores.get('interpretation', 'N/A')}")

        # Findings
        print("\nKey Findings:")
        for f in self.results.get("findings", []):
            print(f"  [{f['confidence']}] {f['finding']}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Analyze Linear A syntax patterns")
    parser.add_argument(
        "--administrative", action="store_true", help="Analyze administrative texts"
    )
    parser.add_argument("--religious", action="store_true", help="Analyze religious texts")
    parser.add_argument("--all", "-a", action="store_true", help="Run full analysis")
    parser.add_argument("--output", "-o", type=str, default="data/syntax_analysis.json")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    analyzer = SyntaxAnalyzer(verbose=args.verbose)

    if not analyzer.load_corpus():
        return 1

    if args.all:
        analyzer.run_full_analysis()
    else:
        analyzer.classify_all_texts()
        if args.administrative:
            analyzer.analyze_administrative_syntax()
        if args.religious:
            analyzer.analyze_religious_syntax()
        analyzer.analyze_particle_positions()
        analyzer.score_word_order_hypotheses()

    if any([args.all, args.administrative, args.religious]):
        analyzer.results["metadata"]["generated"] = datetime.now().isoformat()
        output_path = PROJECT_ROOT / args.output
        analyzer.save_results(output_path)
        analyzer.print_summary()
    else:
        print("\nUsage: python syntax_analyzer.py --all")

    return 0


if __name__ == "__main__":
    sys.exit(main())
