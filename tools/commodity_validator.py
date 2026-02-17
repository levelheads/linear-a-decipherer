#!/usr/bin/env python3
"""
Commodity Validator for Linear A

Promotes co-occurrence observations to validated functional anchors.

For each high-specificity word-commodity mapping:
1. Full corpus verification: Does the word EVER appear without the commodity?
2. Falsifiability test: Exclusive → anchor. 95%+ → strong anchor with exceptions
3. Contextual position: Where does the word appear relative to the logogram?
4. Cross-site: Does the mapping hold at multiple sites?

Usage:
    python3 tools/commodity_validator.py --all
    python3 tools/commodity_validator.py --word SI
    python3 tools/commodity_validator.py --threshold 0.8
    python3 tools/commodity_validator.py --output data/commodity_anchors.json

Attribution:
    Part of Linear A Decipherment Project
    Promotes co-occurrence data to functional anchors
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"

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


@dataclass
class CommodityMapping:
    """A validated word→commodity functional mapping."""

    word: str
    primary_commodity: str
    total_occurrences: int
    with_primary: int  # Times appearing with primary commodity
    with_other: int  # Times appearing with other commodities
    without_any: int  # Times appearing with no commodity
    specificity: float  # 0-1
    exclusivity: float  # 0-1 (with_primary / total_occurrences)
    sites: List[str]
    site_count: int
    position_relative: str  # 'before', 'after', 'mixed', 'same_line'
    exceptions: List[Dict]  # List of exception contexts
    promotion_recommendation: str  # 'FUNCTIONAL_ANCHOR', 'STRONG_ANCHOR', 'CANDIDATE', 'REJECTED'
    confidence: str  # CERTAIN, HIGH, PROBABLE, POSSIBLE
    notes: str = ""


class CommodityValidator:
    """Validates word-commodity co-occurrences into functional anchors."""

    def __init__(self, threshold: float = 0.8):
        self.corpus = {}
        self.inscriptions = {}
        self.threshold = threshold

    def load_corpus(self) -> bool:
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _is_number(self, token: str) -> bool:
        if token in FRACTION_TOKENS:
            return True
        try:
            int(token)
            return True
        except ValueError:
            return False

    def _is_logogram(self, token: str) -> bool:
        if token in COMMODITY_LOGOGRAMS:
            return True
        if "+" in token:
            base = token.split("+")[0]
            return base in COMMODITY_LIGATURE_BASES
        return False

    def _get_base_commodity(self, token: str) -> str:
        if "+" in token:
            return token.split("+")[0]
        return token

    def _is_word(self, token: str) -> bool:
        if token in {"\n", "𐄁", "", " ", "—", ","}:
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
        match = re.match(r"^([A-Z]+)", tablet_id)
        return match.group(1) if match else "UNKNOWN"

    def _build_line_index(self, words: List[str]) -> List[List[str]]:
        """Split words into lines."""
        lines = []
        current = []
        for w in words:
            if w == "\n":
                if current:
                    lines.append(current)
                current = []
            else:
                current.append(w)
        if current:
            lines.append(current)
        return lines

    def validate_word(self, target_word: str) -> Optional[CommodityMapping]:
        """Exhaustively validate a single word's commodity association."""
        # Collect all occurrences
        word_tablets = set()
        commodity_counter = Counter()
        site_counter = Counter()
        position_counts = Counter()  # 'before', 'after', 'same_position'
        exceptions = []

        for tablet_id, data in self.inscriptions.items():
            words = data.get("transliteratedWords", [])
            if target_word not in words:
                continue

            word_tablets.add(tablet_id)
            site = self._extract_site(tablet_id)
            site_counter[site] += 1

            lines = self._build_line_index(words)

            for line in lines:
                if target_word not in line:
                    continue

                word_positions = [i for i, w in enumerate(line) if w == target_word]
                commodities_on_line = []
                for i, w in enumerate(line):
                    if self._is_logogram(w):
                        commodities_on_line.append((i, self._get_base_commodity(w), w))

                for wp in word_positions:
                    if commodities_on_line:
                        for cp, base_comm, full_comm in commodities_on_line:
                            commodity_counter[base_comm] += 1
                            if wp < cp:
                                position_counts["before"] += 1
                            elif wp > cp:
                                position_counts["after"] += 1
                            else:
                                position_counts["same"] += 1
                    else:
                        commodity_counter["NONE"] += 1
                        exceptions.append(
                            {
                                "tablet_id": tablet_id,
                                "context": " ".join(line[:10]),
                                "note": "No commodity on line",
                            }
                        )

        total_occurrences = sum(commodity_counter.values())
        if total_occurrences < 2:
            return None

        # Find primary commodity (excluding NONE)
        real_commodities = {k: v for k, v in commodity_counter.items() if k != "NONE"}
        if not real_commodities:
            return None

        primary = max(real_commodities, key=lambda k: real_commodities[k])
        with_primary = real_commodities[primary]
        with_other = sum(v for k, v in real_commodities.items() if k != primary)
        without_any = commodity_counter.get("NONE", 0)

        # Calculate specificity (among commodities only)
        total_with_commodity = sum(real_commodities.values())
        specificity = with_primary / total_with_commodity if total_with_commodity > 0 else 0

        # Exclusivity (how often word appears with primary vs total appearances)
        exclusivity = with_primary / total_occurrences if total_occurrences > 0 else 0

        # Position relative to commodity
        if position_counts:
            dominant_pos = max(position_counts, key=lambda k: position_counts[k])
            pos_pct = position_counts[dominant_pos] / sum(position_counts.values())
            if pos_pct > 0.7:
                position_relative = dominant_pos
            else:
                position_relative = "mixed"
        else:
            position_relative = "unknown"

        # Promotion decision
        sites = sorted(site_counter.keys())
        site_count = len(sites)

        if specificity >= 0.95 and total_occurrences >= 3 and without_any == 0:
            promotion = "FUNCTIONAL_ANCHOR"
            confidence = "HIGH"
        elif specificity >= 0.80 and total_occurrences >= 3:
            promotion = "STRONG_ANCHOR"
            confidence = "PROBABLE"
        elif specificity >= self.threshold and total_occurrences >= 2:
            promotion = "CANDIDATE"
            confidence = "POSSIBLE"
        else:
            promotion = "REJECTED"
            confidence = "SPECULATIVE"

        # Cross-site bonus
        if site_count >= 2 and promotion != "REJECTED":
            confidence_upgrade = {
                "POSSIBLE": "PROBABLE",
                "PROBABLE": "HIGH",
            }
            confidence = confidence_upgrade.get(confidence, confidence)

        return CommodityMapping(
            word=target_word,
            primary_commodity=primary,
            total_occurrences=total_occurrences,
            with_primary=with_primary,
            with_other=with_other,
            without_any=without_any,
            specificity=round(specificity, 3),
            exclusivity=round(exclusivity, 3),
            sites=sites,
            site_count=site_count,
            position_relative=position_relative,
            exceptions=exceptions[:5],  # Limit stored exceptions
            promotion_recommendation=promotion,
            confidence=confidence,
            notes=f"Primary {primary}: {with_primary}/{total_occurrences}, "
            f"{'pan-Minoan' if site_count >= 2 else f'{sites[0]}-only' if sites else 'unknown'}",
        )

    def validate_all(self) -> List[CommodityMapping]:
        """Validate all words with commodity co-occurrence."""
        # First, find all words that co-occur with commodities
        word_commodity_counts = defaultdict(lambda: defaultdict(int))
        word_total_counts = Counter()

        for tablet_id, data in self.inscriptions.items():
            words = data.get("transliteratedWords", [])
            lines = self._build_line_index(words)

            for line in lines:
                commodities = [self._get_base_commodity(w) for w in line if self._is_logogram(w)]
                word_tokens = [w for w in line if self._is_word(w)]

                for word in word_tokens:
                    word_total_counts[word] += 1
                    for comm in commodities:
                        word_commodity_counts[word][comm] += 1

        # Find high-specificity candidates
        candidates = []
        for word, commodities in word_commodity_counts.items():
            if word_total_counts[word] < 2:
                continue
            total = sum(commodities.values())
            if total < 2:
                continue
            primary = max(commodities, key=lambda k: commodities[k])
            specificity = commodities[primary] / total
            if specificity >= self.threshold:
                candidates.append(word)

        print(f"Found {len(candidates)} candidate words (specificity >= {self.threshold})")

        # Validate each candidate
        results = []
        for word in sorted(candidates):
            mapping = self.validate_word(word)
            if mapping:
                results.append(mapping)

        results.sort(key=lambda m: (-m.specificity, -m.total_occurrences))
        return results

    def print_mapping_report(self, mapping: CommodityMapping):
        """Print detailed report for a single mapping."""
        print(f"\n{'=' * 60}")
        print(f"COMMODITY MAPPING: {mapping.word} → {mapping.primary_commodity}")
        print(f"{'=' * 60}")
        print(f"  Occurrences: {mapping.total_occurrences}")
        print(
            f"  With {mapping.primary_commodity}: {mapping.with_primary} ({mapping.specificity:.0%})"
        )
        print(f"  With other: {mapping.with_other}")
        print(f"  Without any: {mapping.without_any}")
        print(f"  Exclusivity: {mapping.exclusivity:.0%}")
        print(f"  Position: {mapping.position_relative}")
        print(f"  Sites: {', '.join(mapping.sites)} ({mapping.site_count})")
        print(f"  Promotion: {mapping.promotion_recommendation}")
        print(f"  Confidence: {mapping.confidence}")
        if mapping.exceptions:
            print("  Exceptions:")
            for ex in mapping.exceptions[:3]:
                print(f"    {ex['tablet_id']}: {ex['note']}")

    def print_summary(self, results: List[CommodityMapping]):
        """Print summary of all validations."""
        print(f"\n{'=' * 70}")
        print("COMMODITY VALIDATION SUMMARY")
        print(f"{'=' * 70}")

        promo_counts = Counter(m.promotion_recommendation for m in results)
        print(f"\n  Total mappings validated: {len(results)}")
        for promo, count in sorted(promo_counts.items()):
            print(f"    {promo:20s}: {count}")

        # List functional anchors
        anchors = [
            m
            for m in results
            if m.promotion_recommendation in ("FUNCTIONAL_ANCHOR", "STRONG_ANCHOR")
        ]
        if anchors:
            print(f"\n  --- Promoted Anchors ({len(anchors)}) ---")
            print(
                f"  {'Word':<20s} {'Commodity':<8s} {'Spec':>5s} {'N':>4s} {'Sites':>5s} {'Level'}"
            )
            print(f"  {'-' * 60}")
            for m in anchors:
                print(
                    f"  {m.word:<20s} {m.primary_commodity:<8s} "
                    f"{m.specificity:5.1%} {m.total_occurrences:4d} "
                    f"{m.site_count:5d} {m.promotion_recommendation}"
                )

        # List by commodity
        comm_groups = defaultdict(list)
        for m in results:
            if m.promotion_recommendation != "REJECTED":
                comm_groups[m.primary_commodity].append(m)

        if comm_groups:
            print("\n  --- By Commodity ---")
            for comm in sorted(comm_groups.keys()):
                words = comm_groups[comm]
                word_list = ", ".join(f"{m.word}({m.specificity:.0%})" for m in words[:5])
                print(f"  {comm:8s}: {word_list}")

    def save_results(self, results: List[CommodityMapping], output_path: str):
        """Save results to JSON."""
        output = {
            "metadata": {
                "tool": "commodity_validator.py",
                "threshold": self.threshold,
                "total_validated": len(results),
                "functional_anchors": sum(
                    1 for m in results if m.promotion_recommendation == "FUNCTIONAL_ANCHOR"
                ),
                "strong_anchors": sum(
                    1 for m in results if m.promotion_recommendation == "STRONG_ANCHOR"
                ),
                "candidates": sum(1 for m in results if m.promotion_recommendation == "CANDIDATE"),
            },
            "mappings": [asdict(m) for m in results],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Commodity Validator - promote co-occurrence to functional anchors"
    )
    parser.add_argument("--word", type=str, help="Validate a single word")
    parser.add_argument("--all", action="store_true", help="Validate all high-specificity words")
    parser.add_argument(
        "--threshold", type=float, default=0.8, help="Minimum specificity threshold (default: 0.8)"
    )
    parser.add_argument("--output", type=str, help="Save results to JSON file")

    args = parser.parse_args()

    if not any([args.word, args.all]):
        args.all = True

    validator = CommodityValidator(threshold=args.threshold)
    if not validator.load_corpus():
        sys.exit(1)

    if args.word:
        mapping = validator.validate_word(args.word)
        if mapping:
            validator.print_mapping_report(mapping)
        else:
            print(f"Word '{args.word}' has insufficient data for validation")
    else:
        results = validator.validate_all()
        validator.print_summary(results)

        if args.output:
            validator.save_results(results, args.output)


if __name__ == "__main__":
    main()
