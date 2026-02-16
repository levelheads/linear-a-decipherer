#!/usr/bin/env python3
"""
Regional Weighting System for Linear A

Adjusts confidence scores based on site concentration to address HT bias.
The corpus is 63.4% Hagia Triada, which means readings validated primarily
at HT may be over-confident.

Weighting Formula:
    weight = 1.0
    if num_sites >= 2: weight += log2(num_sites) * 0.1  # Diversity bonus
    if ht_concentration > 0.5: weight -= (ht_concentration - 0.5) * 0.5  # HT penalty
    weight = clip(weight, 0.3, 1.5)

Example:
    KU-RO at 39 HT tablets (high HT concentration) → ~0.75 weight (25% penalty)
    KU-RO confirmed at HT, ZA, PH → higher weight due to diversity

Usage:
    python tools/regional_weighting.py --word KU-RO
    python tools/regional_weighting.py --all --min-freq 3
    python tools/regional_weighting.py --site-stats
    python tools/regional_weighting.py --apply-weights --output data/weighted_readings.json

Attribution:
    Part of Linear A Decipherment Project
    Addresses regional bias critique in methodology review
"""

import json
import argparse
import sys
import re
import math
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
REGIONAL_ANALYSIS_FILE = DATA_DIR / "regional_analysis.json"
NEGATIVE_EVIDENCE_FILE = DATA_DIR / "negative_evidence_catalog.json"


# Site information
SITE_CODES = {
    "HT": {"name": "Hagia Triada", "region": "central", "dominant": True},
    "KH": {"name": "Khania", "region": "west", "dominant": False},
    "ZA": {"name": "Zakros", "region": "east", "dominant": False},
    "PH": {"name": "Phaistos", "region": "central", "dominant": False},
    "KN": {"name": "Knossos", "region": "central", "dominant": False},
    "MA": {"name": "Malia", "region": "east", "dominant": False},
    "TY": {"name": "Tylissos", "region": "central", "dominant": False},
    "PK": {"name": "Palaikastro", "region": "east", "dominant": False},
}


@dataclass
class SiteDistribution:
    """Distribution of a word across sites."""

    word: str
    total_occurrences: int
    site_counts: Dict[str, int]
    num_sites: int
    ht_concentration: float
    diversity_score: float


@dataclass
class WeightedReading:
    """A reading with regional weight applied."""

    word: str
    meaning: str
    raw_confidence: str
    site_distribution: SiteDistribution
    regional_weight: float
    negative_evidence_penalty: float
    adjusted_weight: float
    weight_rationale: List[str]


class RegionalWeighting:
    """
    Computes regional weights for Linear A readings.

    Addresses the critique that HT dominance (63.4% of corpus) may
    inflate confidence in readings that are actually site-specific.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = {}
        self.negative_evidence = []
        self.site_stats = {}

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_data(self) -> bool:
        """Load corpus and supporting data."""
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)

            if NEGATIVE_EVIDENCE_FILE.exists():
                with open(NEGATIVE_EVIDENCE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.negative_evidence = data.get("absences", [])

            # Calculate site statistics
            self._calculate_site_stats()

            print(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def _get_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        match = re.match(r"^([A-Z]+)", inscription_id)
        if match:
            code = match.group(1)
            # Normalize variants
            for canonical in SITE_CODES:
                if code.startswith(canonical):
                    return canonical
            return code
        return "UNKNOWN"

    def _calculate_site_stats(self):
        """Calculate inscription counts by site."""
        self.site_stats = Counter()

        for insc_id in self.corpus.get("inscriptions", {}):
            site = self._get_site_code(insc_id)
            self.site_stats[site] += 1

        total = sum(self.site_stats.values())
        self.log(f"Site distribution (total={total}):")
        for site, count in self.site_stats.most_common():
            pct = count / total * 100 if total > 0 else 0
            self.log(f"  {site}: {count} ({pct:.1f}%)")

    def _is_valid_word(self, word: str) -> bool:
        """Check if word is valid for analysis."""
        if not word or word in ["\n", "𐄁", "", "—", "≈"]:
            return False
        if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$", word):
            return False
        if word.startswith("𐝫") or word == "𐝫":
            return False
        return True

    def get_word_distribution(self, word: str) -> SiteDistribution:
        """
        Get the site distribution for a specific word.

        Args:
            word: The word to analyze

        Returns:
            SiteDistribution with counts and concentration metrics
        """
        site_counts = Counter()
        total = 0
        word_upper = word.upper()

        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue

            words = data.get("transliteratedWords", [])
            word_in_insc = any(w.upper() == word_upper for w in words if self._is_valid_word(w))

            if word_in_insc:
                site = self._get_site_code(insc_id)
                site_counts[site] += 1
                total += 1

        # Calculate HT concentration
        ht_count = site_counts.get("HT", 0)
        ht_concentration = ht_count / total if total > 0 else 0

        # Calculate diversity score (Shannon entropy normalized)
        num_sites = len([s for s in site_counts if site_counts[s] > 0])
        if num_sites > 0 and total > 0:
            probs = [count / total for count in site_counts.values() if count > 0]
            entropy = -sum(p * math.log2(p) for p in probs if p > 0)
            max_entropy = math.log2(num_sites) if num_sites > 1 else 1
            diversity_score = entropy / max_entropy if max_entropy > 0 else 0
        else:
            diversity_score = 0

        return SiteDistribution(
            word=word,
            total_occurrences=total,
            site_counts=dict(site_counts),
            num_sites=num_sites,
            ht_concentration=round(ht_concentration, 3),
            diversity_score=round(diversity_score, 3),
        )

    def calculate_regional_weight(self, distribution: SiteDistribution) -> Tuple[float, List[str]]:
        """
        Calculate regional weight based on site distribution.

        Formula:
            weight = 1.0
            if num_sites >= 2: weight += log2(num_sites) * 0.1  # Diversity bonus
            if ht_concentration > 0.5: weight -= (ht_concentration - 0.5) * 0.5  # HT penalty
            weight = clip(weight, 0.3, 1.5)

        Args:
            distribution: SiteDistribution for the word

        Returns:
            (weight, rationale) tuple
        """
        weight = 1.0
        rationale = []

        # Diversity bonus
        if distribution.num_sites >= 2:
            bonus = math.log2(distribution.num_sites) * 0.1
            weight += bonus
            rationale.append(f"Diversity bonus: +{bonus:.2f} ({distribution.num_sites} sites)")

        # HT concentration penalty
        if distribution.ht_concentration > 0.5:
            penalty = (distribution.ht_concentration - 0.5) * 0.5
            weight -= penalty
            rationale.append(
                f"HT concentration penalty: -{penalty:.2f} ({distribution.ht_concentration:.1%} at HT)"
            )

        # Single-site penalty
        if distribution.num_sites == 1:
            if distribution.total_occurrences > 5:
                weight *= 0.8
                rationale.append("Single-site penalty: ×0.8 (only found at one site)")

        # Low diversity penalty
        if distribution.diversity_score < 0.3 and distribution.num_sites > 1:
            weight *= 0.9
            rationale.append(
                f"Low diversity penalty: ×0.9 (entropy={distribution.diversity_score:.2f})"
            )

        # Cross-regional bonus (found in multiple regions)
        regions = set()
        for site in distribution.site_counts:
            if site in SITE_CODES:
                regions.add(SITE_CODES[site]["region"])
        if len(regions) >= 2:
            weight += 0.1
            rationale.append(f"Cross-regional bonus: +0.1 (found in {len(regions)} regions)")

        # Clip weight
        original_weight = weight
        weight = max(0.3, min(1.5, weight))
        if weight != original_weight:
            rationale.append(f"Clipped from {original_weight:.2f} to {weight:.2f}")

        return round(weight, 3), rationale

    def calculate_negative_evidence_penalty(
        self, word: str, hypothesis: str
    ) -> Tuple[float, List[str]]:
        """
        Calculate penalty based on negative evidence catalog.

        Args:
            word: The word being evaluated
            hypothesis: The hypothesis being tested

        Returns:
            (penalty, rationale) tuple where penalty is subtracted from weight
        """
        penalty = 0.0
        rationale = []

        for absence in self.negative_evidence:
            if absence.get("hypothesis", "").lower() != hypothesis.lower():
                continue

            # Check if this absence is relevant to the word
            if absence.get("falsifies", False) and absence.get("significance") == "CRITICAL":
                # Hypothesis is falsified - major penalty
                penalty += 0.3
                rationale.append(
                    f"Critical absence: {absence.get('pattern', 'Unknown')} ({absence.get('id')})"
                )

            elif absence.get("status") == "CERTAIN":
                penalty += 0.1
                rationale.append(f"Certain absence penalty: {absence.get('id')}")

            elif absence.get("status") == "PROBABLE":
                penalty += 0.05
                rationale.append(f"Probable absence penalty: {absence.get('id')}")

        return round(min(penalty, 0.5), 3), rationale  # Cap at 0.5

    def weight_reading(
        self,
        word: str,
        meaning: str = "",
        raw_confidence: str = "PROBABLE",
        hypothesis: str = "luwian",
    ) -> WeightedReading:
        """
        Apply regional weighting to a reading.

        Args:
            word: The Linear A word
            meaning: Proposed meaning
            raw_confidence: Original confidence level
            hypothesis: Primary hypothesis for negative evidence

        Returns:
            WeightedReading with all adjustments
        """
        distribution = self.get_word_distribution(word)
        regional_weight, weight_rationale = self.calculate_regional_weight(distribution)
        neg_penalty, neg_rationale = self.calculate_negative_evidence_penalty(word, hypothesis)

        adjusted_weight = max(0.3, regional_weight - neg_penalty)
        all_rationale = weight_rationale + neg_rationale

        return WeightedReading(
            word=word,
            meaning=meaning,
            raw_confidence=raw_confidence,
            site_distribution=distribution,
            regional_weight=regional_weight,
            negative_evidence_penalty=neg_penalty,
            adjusted_weight=round(adjusted_weight, 3),
            weight_rationale=all_rationale,
        )

    def weight_all_words(self, min_freq: int = 3) -> List[WeightedReading]:
        """
        Weight all words in corpus above frequency threshold.

        Args:
            min_freq: Minimum frequency to include

        Returns:
            List of WeightedReading objects
        """
        # Count word frequencies
        word_freq = Counter()
        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue
            for word in data.get("transliteratedWords", []):
                if self._is_valid_word(word) and "-" in word:
                    word_freq[word.upper()] += 1

        # Weight words above threshold
        results = []
        for word, freq in word_freq.most_common():
            if freq >= min_freq:
                weighted = self.weight_reading(word)
                results.append(weighted)
                self.log(
                    f"{word}: weight={weighted.adjusted_weight:.2f} ({weighted.site_distribution.num_sites} sites)"
                )

        return results

    def get_site_statistics(self) -> Dict:
        """Get comprehensive site statistics."""
        total = sum(self.site_stats.values())

        stats = {
            "total_inscriptions": total,
            "sites": {},
            "dominant_site": None,
            "dominant_concentration": 0,
            "regional_distribution": defaultdict(int),
        }

        max_count = 0
        for site, count in self.site_stats.items():
            pct = count / total * 100 if total > 0 else 0
            stats["sites"][site] = {
                "count": count,
                "percentage": round(pct, 1),
                "name": SITE_CODES.get(site, {}).get("name", site),
                "region": SITE_CODES.get(site, {}).get("region", "unknown"),
            }

            if count > max_count:
                max_count = count
                stats["dominant_site"] = site
                stats["dominant_concentration"] = round(pct, 1)

            if site in SITE_CODES:
                stats["regional_distribution"][SITE_CODES[site]["region"]] += count

        stats["regional_distribution"] = dict(stats["regional_distribution"])

        return stats

    def print_weighted_reading(self, weighted: WeightedReading):
        """Print formatted weighted reading."""
        print(f"\n{weighted.word}")
        print("─" * 50)
        print(f"  Meaning: {weighted.meaning or 'Unknown'}")
        print(f"  Raw Confidence: {weighted.raw_confidence}")
        print("\n  Site Distribution:")
        for site, count in sorted(
            weighted.site_distribution.site_counts.items(), key=lambda x: -x[1]
        ):
            name = SITE_CODES.get(site, {}).get("name", site)
            print(f"    {site} ({name}): {count}")
        print(f"\n  Sites: {weighted.site_distribution.num_sites}")
        print(f"  HT Concentration: {weighted.site_distribution.ht_concentration:.1%}")
        print(f"  Diversity Score: {weighted.site_distribution.diversity_score:.2f}")
        print("\n  Weights:")
        print(f"    Regional: {weighted.regional_weight:.3f}")
        print(f"    Neg. Evidence Penalty: -{weighted.negative_evidence_penalty:.3f}")
        print(f"    Adjusted: {weighted.adjusted_weight:.3f}")
        print("\n  Rationale:")
        for r in weighted.weight_rationale:
            print(f"    • {r}")

    def print_site_statistics(self):
        """Print site statistics summary."""
        stats = self.get_site_statistics()

        print("\n" + "=" * 70)
        print("SITE DISTRIBUTION STATISTICS")
        print("=" * 70)

        print(f"\nTotal Inscriptions: {stats['total_inscriptions']}")
        print(f"Dominant Site: {stats['dominant_site']} ({stats['dominant_concentration']}%)")

        print("\nBy Site:")
        for site, data in sorted(stats["sites"].items(), key=lambda x: -x[1]["count"]):
            bar = "█" * int(data["percentage"] / 2)
            print(
                f"  {site:4} {data['name'][:15]:15} {data['count']:4} ({data['percentage']:5.1f}%) {bar}"
            )

        print("\nBy Region:")
        for region, count in sorted(stats["regional_distribution"].items(), key=lambda x: -x[1]):
            pct = count / stats["total_inscriptions"] * 100
            print(f"  {region:8} {count:4} ({pct:.1f}%)")

        print("\n⚠ BIAS WARNING:")
        if stats["dominant_concentration"] > 50:
            print(
                f"  {stats['dominant_site']} accounts for {stats['dominant_concentration']}% of corpus"
            )
            print("  Readings validated primarily at this site may be over-confident")
            print("  Apply regional weighting to adjust confidence scores")

        print("\n" + "=" * 70)

    def generate_report(self, weighted_readings: List[WeightedReading]) -> Dict:
        """Generate comprehensive weighting report."""
        site_stats = self.get_site_statistics()

        # Categorize by weight
        high_weight = [w for w in weighted_readings if w.adjusted_weight >= 1.0]
        moderate_weight = [w for w in weighted_readings if 0.7 <= w.adjusted_weight < 1.0]
        low_weight = [w for w in weighted_readings if w.adjusted_weight < 0.7]

        # Words with HT penalty
        ht_penalized = [w for w in weighted_readings if w.site_distribution.ht_concentration > 0.5]

        # Cross-site validated
        cross_site = [w for w in weighted_readings if w.site_distribution.num_sites >= 3]

        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "method": "Regional Weighting with Negative Evidence",
                "formula": "weight = 1.0 + log2(sites)*0.1 - (ht_conc-0.5)*0.5 - neg_penalty",
                "total_words_analyzed": len(weighted_readings),
            },
            "site_statistics": site_stats,
            "weight_distribution": {
                "high_weight_1.0+": len(high_weight),
                "moderate_weight_0.7-1.0": len(moderate_weight),
                "low_weight_under_0.7": len(low_weight),
            },
            "ht_bias_analysis": {
                "words_with_ht_penalty": len(ht_penalized),
                "penalized_words": [asdict(w) for w in ht_penalized[:20]],
            },
            "cross_site_validated": {
                "count": len(cross_site),
                "words": [asdict(w) for w in cross_site[:20]],
            },
            "all_weights": [asdict(w) for w in weighted_readings],
        }

        return report


def main():
    parser = argparse.ArgumentParser(description="Calculate regional weights for Linear A readings")
    parser.add_argument("--word", "-w", type=str, help="Analyze a specific word")
    parser.add_argument("--all", "-a", action="store_true", help="Weight all words in corpus")
    parser.add_argument(
        "--min-freq", "-m", type=int, default=3, help="Minimum frequency for --all (default: 3)"
    )
    parser.add_argument(
        "--site-stats", "-s", action="store_true", help="Show site distribution statistics"
    )
    parser.add_argument("--output", "-o", type=str, help="Output path for JSON report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A REGIONAL WEIGHTING SYSTEM")
    print("=" * 70)

    system = RegionalWeighting(verbose=args.verbose)
    if not system.load_data():
        return 1

    if args.site_stats:
        system.print_site_statistics()
        return 0

    if args.word:
        weighted = system.weight_reading(args.word)
        system.print_weighted_reading(weighted)
        return 0

    if args.all:
        print(f"\nWeighting all words (min freq >= {args.min_freq})...")
        weighted_readings = system.weight_all_words(min_freq=args.min_freq)

        print(f"\nAnalyzed {len(weighted_readings)} words")

        # Summary
        high = sum(1 for w in weighted_readings if w.adjusted_weight >= 1.0)
        low = sum(1 for w in weighted_readings if w.adjusted_weight < 0.7)
        print(f"  High weight (≥1.0): {high}")
        print(f"  Low weight (<0.7): {low}")

        # Top penalized words
        penalized = sorted(weighted_readings, key=lambda w: w.adjusted_weight)[:10]
        print("\nMost Penalized Words:")
        for w in penalized:
            print(
                f"  {w.word}: {w.adjusted_weight:.2f} (HT={w.site_distribution.ht_concentration:.0%})"
            )

        # Top cross-site validated
        cross_site = sorted(weighted_readings, key=lambda w: -w.site_distribution.num_sites)[:10]
        print("\nBest Cross-Site Validation:")
        for w in cross_site:
            sites = ", ".join(w.site_distribution.site_counts.keys())
            print(
                f"  {w.word}: {w.adjusted_weight:.2f} ({w.site_distribution.num_sites} sites: {sites})"
            )

        if args.output:
            report = system.generate_report(weighted_readings)
            output_path = Path(args.output)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            print(f"\nReport saved to: {output_path}")

        return 0

    # Default: show site statistics
    system.print_site_statistics()
    print("\nUse --word WORD or --all for weighting analysis")

    return 0


if __name__ == "__main__":
    sys.exit(main())
