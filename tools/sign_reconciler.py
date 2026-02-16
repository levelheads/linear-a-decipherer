#!/usr/bin/env python3
"""
Linear A Sign System Reconciler

Creates a unified mapping between the two sign classification systems:
1. signs.json - Mixed phonetic notation (A, RA, KU, *301, OLE)
2. sign_database.json - GORILA AB-numbered system (AB08, AB28, AB81)

This tool ensures cross-referencing is possible between paleographic data
(AB-numbered) and corpus analysis data (phonetic notation).

Usage:
    python tools/sign_reconciler.py --build       # Build mapping table
    python tools/sign_reconciler.py --lookup KU   # Look up sign by phonetic value
    python tools/sign_reconciler.py --ab AB81    # Look up by AB number
    python tools/sign_reconciler.py --validate    # Validate corpus against sign database
    python tools/sign_reconciler.py --report      # Generate reconciliation report

Attribution:
    Part of Linear A Decipherment Project
    Enables cross-system sign verification for First Principle #6
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import List, Optional


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SIGLA_DIR = DATA_DIR / "sigla"


class SignReconciler:
    """
    Reconciles sign classification systems for unified lookup.

    Creates bidirectional mapping:
    - phonetic_to_ab: "ku" -> "AB81"
    - ab_to_phonetic: "AB81" -> "ku"

    Also tracks:
    - Signs unique to each system
    - Confidence levels from sign_database.json
    - Frequency data from signs.json
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.signs_data = None  # From signs.json (phonetic notation)
        self.sigla_data = None  # From sign_database.json (AB numbers)

        # Mapping tables
        self.phonetic_to_ab = {}  # "ku" -> {"ab": "AB81", "confidence": "CERTAIN"}
        self.ab_to_phonetic = {}  # "AB81" -> {"phonetic": "ku", "confidence": "CERTAIN"}
        self.logograms = {}  # "OLE" -> {"type": "logogram", "meaning": "olive oil"}
        self.unmapped_signs = []  # Signs without AB equivalents (*301, etc.)
        self.unmapped_ab = []  # AB numbers without phonetic equivalents

        # Combined data
        self.unified_signs = {}  # Complete sign inventory

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_data(self) -> bool:
        """Load both sign data sources."""
        success = True

        # Load signs.json (phonetic notation with frequencies)
        signs_path = DATA_DIR / "signs.json"
        try:
            with open(signs_path, "r", encoding="utf-8") as f:
                self.signs_data = json.load(f)
            self.log(f"Loaded signs.json: {self.signs_data.get('total_signs', 0)} signs")
        except Exception as e:
            print(f"Error loading signs.json: {e}")
            success = False

        # Load sign_database.json (AB numbers with confidence)
        sigla_path = SIGLA_DIR / "sign_database.json"
        try:
            with open(sigla_path, "r", encoding="utf-8") as f:
                self.sigla_data = json.load(f)
            self.log(
                f"Loaded sign_database.json: {self.sigla_data['statistics']['total_signs']} signs"
            )
        except Exception as e:
            print(f"Error loading sign_database.json: {e}")
            success = False

        return success

    def build_mapping(self) -> dict:
        """
        Build bidirectional mapping between sign systems.

        Returns summary statistics.
        """
        print("Building sign system mapping...")

        # Build mapping from sign_database.json (AB -> phonetic)
        # This is the authoritative source for AB numbers
        for ab_num, data in self.sigla_data.get("signs", {}).items():
            phonetic = data.get("phonetic_value", "").lower()
            sign_type = data.get("sign_type", "syllabogram")
            confidence = data.get("confidence", "UNKNOWN")

            if sign_type == "logogram":
                # Logograms like VIN, OLE, GRA, FIC, OVI, *301
                self.logograms[ab_num] = {
                    "ab_number": ab_num,
                    "type": "logogram",
                    "meaning": data.get("description", ""),
                    "frequency": data.get("frequency", 0),
                    "confidence": confidence,
                    "linear_b_cognate": data.get("linear_b_cognate", ""),
                }
                # Also map for lookup
                self.phonetic_to_ab[ab_num.lower()] = {
                    "ab": ab_num,
                    "confidence": confidence,
                    "type": "logogram",
                }
                self.ab_to_phonetic[ab_num] = {
                    "phonetic": ab_num.lower(),
                    "confidence": confidence,
                    "type": "logogram",
                }
            elif phonetic:
                # Syllabograms with phonetic values
                self.phonetic_to_ab[phonetic] = {
                    "ab": ab_num,
                    "confidence": confidence,
                    "type": "syllabogram",
                    "linear_b_cognate": data.get("linear_b_cognate", ""),
                }
                self.ab_to_phonetic[ab_num] = {
                    "phonetic": phonetic,
                    "confidence": confidence,
                    "type": "syllabogram",
                    "linear_b_cognate": data.get("linear_b_cognate", ""),
                }

                # Also map uppercase version for corpus matching
                self.phonetic_to_ab[phonetic.upper()] = self.phonetic_to_ab[phonetic]

        # Now process signs.json to find unmapped signs
        if self.signs_data:
            for sign_key, sign_data in self.signs_data.get("signs", {}).items():
                sign_upper = sign_key.upper()
                sign_lower = sign_key.lower()

                # Check if this sign is mapped
                if sign_lower not in self.phonetic_to_ab and sign_upper not in self.phonetic_to_ab:
                    # Check if it's a logogram
                    if sign_upper in self.logograms:
                        continue

                    # Unmapped sign (e.g., *301, composite signs)
                    self.unmapped_signs.append(
                        {
                            "sign": sign_key,
                            "occurrences": sign_data.get("total_occurrences", 0),
                            "positions": sign_data.get("position_frequency", {}),
                            "note": "No AB number mapping - possibly Linear A unique sign",
                        }
                    )

        # Build unified sign inventory
        self._build_unified_inventory()

        # Generate statistics
        stats = {
            "syllabograms_mapped": len(
                [k for k, v in self.phonetic_to_ab.items() if v.get("type") == "syllabogram"]
            ),
            "logograms_mapped": len(self.logograms),
            "unmapped_signs": len(self.unmapped_signs),
            "total_ab_signs": len(self.ab_to_phonetic),
            "total_unified": len(self.unified_signs),
        }

        print("Mapping complete:")
        print(f"  Syllabograms mapped: {stats['syllabograms_mapped']}")
        print(f"  Logograms: {stats['logograms_mapped']}")
        print(f"  Unmapped signs: {stats['unmapped_signs']}")

        return stats

    def _build_unified_inventory(self):
        """Build unified sign inventory combining both sources."""

        # Start with AB-numbered signs (authoritative)
        for ab_num, data in self.sigla_data.get("signs", {}).items():
            phonetic = data.get("phonetic_value", "").upper()
            if not phonetic:
                phonetic = ab_num  # Use AB number for logograms

            self.unified_signs[phonetic] = {
                "canonical": phonetic,
                "ab_number": ab_num,
                "phonetic_value": data.get("phonetic_value", ""),
                "sign_type": data.get("sign_type", "unknown"),
                "confidence": data.get("confidence", "UNKNOWN"),
                "frequency_sigla": data.get("frequency", 0),
                "frequency_corpus": 0,  # Will be filled from signs.json
                "sites": data.get("sites", []),
                "linear_b_cognate": data.get("linear_b_cognate", ""),
                "description": data.get("description", ""),
            }

        # Enrich with frequency data from signs.json
        if self.signs_data:
            for sign_key, sign_data in self.signs_data.get("signs", {}).items():
                # Try to match with unified inventory
                sign_upper = sign_key.upper()

                if sign_upper in self.unified_signs:
                    self.unified_signs[sign_upper]["frequency_corpus"] = sign_data.get(
                        "total_occurrences", 0
                    )
                    self.unified_signs[sign_upper]["position_frequency"] = sign_data.get(
                        "position_frequency", {}
                    )
                    self.unified_signs[sign_upper]["contexts"] = sign_data.get("contexts", {})
                elif sign_upper in self.logograms:
                    # It's a logogram
                    if sign_upper not in self.unified_signs:
                        self.unified_signs[sign_upper] = {
                            "canonical": sign_upper,
                            "ab_number": sign_upper,
                            "sign_type": "logogram",
                            "frequency_corpus": sign_data.get("total_occurrences", 0),
                            "position_frequency": sign_data.get("position_frequency", {}),
                        }
                else:
                    # Unmapped sign - add to unified with note
                    self.unified_signs[sign_upper] = {
                        "canonical": sign_upper,
                        "ab_number": None,
                        "sign_type": "unknown",
                        "note": "No AB mapping - Linear A unique or special sign",
                        "frequency_corpus": sign_data.get("total_occurrences", 0),
                        "position_frequency": sign_data.get("position_frequency", {}),
                    }

    def lookup_phonetic(self, phonetic: str) -> Optional[dict]:
        """Look up a sign by phonetic value."""
        key = phonetic.lower()
        if key in self.phonetic_to_ab:
            result = self.phonetic_to_ab[key].copy()
            result["input"] = phonetic

            # Get full data from unified inventory
            canonical = phonetic.upper()
            if canonical in self.unified_signs:
                result["full_data"] = self.unified_signs[canonical]

            return result

        # Try uppercase (for logograms)
        key_upper = phonetic.upper()
        if key_upper in self.phonetic_to_ab:
            result = self.phonetic_to_ab[key_upper].copy()
            result["input"] = phonetic
            if key_upper in self.unified_signs:
                result["full_data"] = self.unified_signs[key_upper]
            return result

        return None

    def lookup_ab(self, ab_number: str) -> Optional[dict]:
        """Look up a sign by AB number."""
        key = ab_number.upper()
        if key in self.ab_to_phonetic:
            result = self.ab_to_phonetic[key].copy()
            result["input"] = ab_number

            # Get full data
            phonetic = result.get("phonetic", "").upper()
            if phonetic in self.unified_signs:
                result["full_data"] = self.unified_signs[phonetic]
            elif key in self.unified_signs:
                result["full_data"] = self.unified_signs[key]

            return result
        return None

    def normalize_word(self, word: str) -> List[dict]:
        """
        Normalize a word, returning sign-by-sign breakdown with AB mappings.

        Example: "KU-RO" -> [
            {"sign": "KU", "ab": "AB81", "confidence": "CERTAIN"},
            {"sign": "RO", "ab": "AB02", "confidence": "CERTAIN"}
        ]
        """
        if not word or word in ["\n", "|", "—"]:
            return []

        # Handle logograms (no hyphens, uppercase)
        if "-" not in word and word.upper() in self.logograms:
            return [
                {
                    "sign": word.upper(),
                    "ab": word.upper(),
                    "type": "logogram",
                    "confidence": self.logograms[word.upper()].get("confidence", "UNKNOWN"),
                }
            ]

        # Split syllabic word
        signs = word.upper().split("-")
        result = []

        for sign in signs:
            # Clean subscripts
            sign_clean = re.sub(r"[₀₁₂₃₄₅₆₇₈₉]", "", sign)

            lookup = self.lookup_phonetic(sign_clean)
            if lookup:
                result.append(
                    {
                        "sign": sign,
                        "sign_clean": sign_clean,
                        "ab": lookup.get("ab"),
                        "type": lookup.get("type", "syllabogram"),
                        "confidence": lookup.get("confidence", "UNKNOWN"),
                    }
                )
            else:
                result.append(
                    {
                        "sign": sign,
                        "sign_clean": sign_clean,
                        "ab": None,
                        "type": "unknown",
                        "confidence": "UNKNOWN",
                        "note": "No AB mapping found",
                    }
                )

        return result

    def validate_corpus_signs(self) -> dict:
        """
        Validate all signs in corpus against sign database.

        Returns report of:
        - Signs in corpus with AB mappings
        - Signs in corpus without mappings
        - Frequency of each category
        """
        print("Validating corpus signs against sign database...")

        corpus_path = DATA_DIR / "corpus.json"
        try:
            with open(corpus_path, "r", encoding="utf-8") as f:
                corpus = json.load(f)
        except Exception as e:
            return {"error": f"Could not load corpus: {e}"}

        # Track sign usage
        mapped_signs = defaultdict(int)
        unmapped_signs = defaultdict(int)
        sign_contexts = defaultdict(list)

        for insc_id, data in corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue

            words = data.get("transliteratedWords", [])
            for word in words:
                if not word or word in ["\n", "|", "—", "𐄁"]:
                    continue

                # Skip numerals
                if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈]+$", word):
                    continue

                normalized = self.normalize_word(word)
                for sign_info in normalized:
                    sign = sign_info["sign"]
                    if sign_info["ab"]:
                        mapped_signs[sign] += 1
                    else:
                        unmapped_signs[sign] += 1
                        if len(sign_contexts[sign]) < 5:
                            sign_contexts[sign].append(insc_id)

        # Calculate statistics
        total_mapped = sum(mapped_signs.values())
        total_unmapped = sum(unmapped_signs.values())
        total = total_mapped + total_unmapped

        report = {
            "summary": {
                "total_sign_occurrences": total,
                "mapped_occurrences": total_mapped,
                "unmapped_occurrences": total_unmapped,
                "mapping_rate": f"{total_mapped / total * 100:.1f}%" if total > 0 else "N/A",
                "unique_mapped_signs": len(mapped_signs),
                "unique_unmapped_signs": len(unmapped_signs),
            },
            "mapped_signs": dict(mapped_signs),
            "unmapped_signs": {
                sign: {
                    "count": count,
                    "examples": sign_contexts.get(sign, []),
                }
                for sign, count in sorted(unmapped_signs.items(), key=lambda x: -x[1])
            },
        }

        print("\nValidation Summary:")
        print(f"  Total sign occurrences: {total}")
        print(
            f"  Mapped: {total_mapped} ({total_mapped / total * 100:.1f}%)"
            if total > 0
            else "  Mapped: 0"
        )
        print(
            f"  Unmapped: {total_unmapped} ({total_unmapped / total * 100:.1f}%)"
            if total > 0
            else "  Unmapped: 0"
        )
        print(f"  Unique mapped signs: {len(mapped_signs)}")
        print(f"  Unique unmapped signs: {len(unmapped_signs)}")

        return report

    def save_mapping(self, output_path: Path = None):
        """Save the complete mapping to JSON."""
        if output_path is None:
            output_path = DATA_DIR / "sign_mapping.json"

        output = {
            "generated": datetime.now().isoformat(),
            "description": "Unified sign mapping between phonetic notation and AB numbers",
            "sources": {
                "phonetic": "signs.json (lineara.xyz corpus analysis)",
                "ab_numbers": "sign_database.json (SigLA/GORILA)",
            },
            "statistics": {
                "syllabograms": len(
                    [k for k, v in self.phonetic_to_ab.items() if v.get("type") == "syllabogram"]
                ),
                "logograms": len(self.logograms),
                "unmapped": len(self.unmapped_signs),
                "total_unified": len(self.unified_signs),
            },
            "phonetic_to_ab": self.phonetic_to_ab,
            "ab_to_phonetic": self.ab_to_phonetic,
            "logograms": self.logograms,
            "unmapped_signs": self.unmapped_signs,
            "unified_inventory": self.unified_signs,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\nMapping saved to: {output_path}")
        return output_path

    def generate_report(self) -> str:
        """Generate human-readable reconciliation report."""
        lines = []
        lines.append("=" * 70)
        lines.append("LINEAR A SIGN SYSTEM RECONCILIATION REPORT")
        lines.append("=" * 70)
        lines.append(f"Generated: {datetime.now().isoformat()}")
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(
            f"Syllabograms with AB mapping: {len([k for k, v in self.phonetic_to_ab.items() if v.get('type') == 'syllabogram'])}"
        )
        lines.append(f"Logograms: {len(self.logograms)}")
        lines.append(f"Signs without AB mapping: {len(self.unmapped_signs)}")
        lines.append(f"Total unified inventory: {len(self.unified_signs)}")
        lines.append("")

        # Mapping table (syllabograms)
        lines.append("SYLLABOGRAM MAPPING (Phonetic -> AB Number)")
        lines.append("-" * 40)
        lines.append(f"{'Phonetic':<10} {'AB#':<8} {'Confidence':<12} {'Linear B'}")
        lines.append("-" * 60)

        for phonetic, data in sorted(self.phonetic_to_ab.items()):
            if data.get("type") == "syllabogram":
                cognate = data.get("linear_b_cognate", "")[:20]
                lines.append(f"{phonetic:<10} {data['ab']:<8} {data['confidence']:<12} {cognate}")

        lines.append("")

        # Logograms
        lines.append("LOGOGRAMS")
        lines.append("-" * 40)
        lines.append(f"{'Sign':<10} {'Confidence':<12} {'Description'}")
        lines.append("-" * 60)

        for logo, data in sorted(self.logograms.items()):
            desc = data.get("meaning", "")[:40]
            lines.append(f"{logo:<10} {data['confidence']:<12} {desc}")

        lines.append("")

        # Unmapped signs
        if self.unmapped_signs:
            lines.append("UNMAPPED SIGNS (Linear A unique)")
            lines.append("-" * 40)
            lines.append(f"{'Sign':<15} {'Occurrences':<12} {'Note'}")
            lines.append("-" * 60)

            for sign_info in sorted(self.unmapped_signs, key=lambda x: -x.get("occurrences", 0)):
                lines.append(
                    f"{sign_info['sign']:<15} {sign_info.get('occurrences', 0):<12} {sign_info.get('note', '')[:40]}"
                )

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Reconcile Linear A sign classification systems")
    parser.add_argument(
        "--build",
        "-b",
        action="store_true",
        help="Build mapping table and save to data/sign_mapping.json",
    )
    parser.add_argument(
        "--lookup", "-l", type=str, help="Look up sign by phonetic value (e.g., KU, RA, OLE)"
    )
    parser.add_argument("--ab", type=str, help="Look up sign by AB number (e.g., AB81, AB02)")
    parser.add_argument(
        "--word", "-w", type=str, help="Normalize a word showing AB mappings (e.g., KU-RO)"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate all corpus signs against sign database"
    )
    parser.add_argument(
        "--report", "-r", action="store_true", help="Generate human-readable reconciliation report"
    )
    parser.add_argument("--output", "-o", type=str, help="Output file path for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A SIGN SYSTEM RECONCILER")
    print("=" * 60)

    reconciler = SignReconciler(verbose=args.verbose)

    if not reconciler.load_data():
        print("Failed to load sign data. Exiting.")
        return 1

    reconciler.build_mapping()

    if args.build:
        output_path = Path(args.output) if args.output else None
        reconciler.save_mapping(output_path)

    if args.lookup:
        result = reconciler.lookup_phonetic(args.lookup)
        if result:
            print(f"\nLookup: {args.lookup}")
            print(f"  AB Number: {result.get('ab')}")
            print(f"  Type: {result.get('type')}")
            print(f"  Confidence: {result.get('confidence')}")
            if result.get("full_data"):
                fd = result["full_data"]
                print(f"  Frequency (corpus): {fd.get('frequency_corpus', 'N/A')}")
                print(f"  Linear B cognate: {fd.get('linear_b_cognate', 'N/A')}")
        else:
            print(f"\nNo mapping found for: {args.lookup}")

    if args.ab:
        result = reconciler.lookup_ab(args.ab)
        if result:
            print(f"\nLookup: {args.ab}")
            print(f"  Phonetic value: {result.get('phonetic')}")
            print(f"  Type: {result.get('type')}")
            print(f"  Confidence: {result.get('confidence')}")
        else:
            print(f"\nNo mapping found for: {args.ab}")

    if args.word:
        normalized = reconciler.normalize_word(args.word)
        print(f"\nWord: {args.word}")
        print("-" * 40)
        for sign_info in normalized:
            ab = sign_info.get("ab") or "UNMAPPED"
            conf = sign_info.get("confidence") or "N/A"
            print(f"  {sign_info['sign']:<10} -> {ab:<8} ({conf})")

    if args.validate:
        report = reconciler.validate_corpus_signs()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\nValidation report saved to: {args.output}")

    if args.report:
        report_text = reconciler.generate_report()
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report_text)
            print(f"\nReport saved to: {args.output}")
        else:
            print(report_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
