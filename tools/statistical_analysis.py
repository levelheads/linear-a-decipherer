#!/usr/bin/env python3
"""
Statistical Analysis Suite for Linear A Corpus

Provides quantitative analysis for decipherment research:
1. Chronological stratification (MMII vs LMIB)
2. Regional variation (HT vs KH vs ZA vocabularies)
3. Register comparison (administrative vs religious texts)
4. Chi-squared tests for positional preferences
5. Entropy measures for sign distribution

Usage:
    python tools/statistical_analysis.py [command] [options]

Commands:
    chronology      Compare vocabulary across time periods
    regional        Compare vocabulary across sites
    register        Compare administrative vs religious texts
    positions       Chi-squared tests for sign positions
    entropy         Calculate entropy measures
    summary         Generate full statistical summary

Examples:
    python tools/statistical_analysis.py summary
    python tools/statistical_analysis.py chronology --compare MMIII LMIB
    python tools/statistical_analysis.py regional --sites HT KH ZA

Attribution:
    Part of Linear A Decipherment Project
    See FIRST_PRINCIPLES.md for methodology
"""

import json
import argparse
import sys
import re
import math
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Set


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


class StatisticalAnalyzer:
    """
    Statistical analysis tools for Linear A corpus.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.signs = None
        self.statistics = None
        self.results = {
            "metadata": {
                "generated": None,
            }
        }

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_data(self) -> bool:
        """Load corpus and sign data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)

            signs_path = DATA_DIR / "signs.json"
            with open(signs_path, "r", encoding="utf-8") as f:
                self.signs = json.load(f)

            stats_path = DATA_DIR / "statistics.json"
            with open(stats_path, "r", encoding="utf-8") as f:
                self.statistics = json.load(f)

            print(f"Loaded {len(self.corpus['inscriptions'])} inscriptions")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def _extract_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        match = re.match(r"^([A-Z]+)", inscription_id)
        return match.group(1) if match else ""

    def _extract_words(self, inscriptions: Dict) -> Counter:
        """Extract word frequencies from a set of inscriptions."""
        word_freq = Counter()

        for insc_id, data in inscriptions.items():
            if "_parse_error" in data:
                continue

            transliterated = data.get("transliteratedWords", [])
            for word in transliterated:
                if not word or word in ["\n", "𐄁", "", "—", "≈"]:
                    continue
                if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$", word):
                    continue
                if word.startswith("𐝫"):
                    continue
                word_freq[word] += 1

        return word_freq

    def _chi_squared(self, observed: List[int], expected: List[float]) -> Tuple[float, int]:
        """
        Calculate chi-squared statistic.
        Returns (chi_squared, degrees_of_freedom).
        """
        if len(observed) != len(expected):
            raise ValueError("Observed and expected must have same length")

        chi_sq = 0
        df = len(observed) - 1

        for obs, exp in zip(observed, expected):
            if exp > 0:
                chi_sq += (obs - exp) ** 2 / exp

        return chi_sq, df

    def _entropy(self, frequencies: List[int]) -> float:
        """
        Calculate Shannon entropy from frequency distribution.
        Returns entropy in bits.
        """
        total = sum(frequencies)
        if total == 0:
            return 0

        entropy = 0
        for freq in frequencies:
            if freq > 0:
                p = freq / total
                entropy -= p * math.log2(p)

        return entropy

    def _jaccard_similarity(self, set1: Set, set2: Set) -> float:
        """Calculate Jaccard similarity between two sets."""
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0

    # =========================================================================
    # CHRONOLOGICAL STRATIFICATION
    # =========================================================================

    def analyze_chronology(self) -> dict:
        """
        Compare vocabulary across time periods.

        Tests whether vocabulary changes significantly between MMII/MMIII and LMIB.
        """
        print("\n[Chronology] Analyzing temporal vocabulary distribution...")

        # Group inscriptions by period
        periods = defaultdict(dict)
        for insc_id, data in self.corpus["inscriptions"].items():
            period = data.get("context", "")
            if period:
                periods[period][insc_id] = data

        # Extract word frequencies for each period
        period_words = {}
        for period, inscriptions in periods.items():
            period_words[period] = self._extract_words(inscriptions)

        results = {
            "periods_analyzed": list(periods.keys()),
            "inscription_counts": {p: len(inscriptions) for p, inscriptions in periods.items()},
            "word_counts": {p: sum(wf.values()) for p, wf in period_words.items()},
            "unique_words": {p: len(wf) for p, wf in period_words.items()},
            "comparisons": [],
        }

        # Compare major periods
        major_periods = ["MMII", "MMIII", "LMIA", "LMIB"]
        available = [p for p in major_periods if p in period_words]

        for i, p1 in enumerate(available):
            for p2 in available[i + 1 :]:
                words1 = set(period_words[p1].keys())
                words2 = set(period_words[p2].keys())

                shared = words1 & words2
                unique_to_p1 = words1 - words2
                unique_to_p2 = words2 - words1

                results["comparisons"].append(
                    {
                        "period1": p1,
                        "period2": p2,
                        "jaccard_similarity": round(self._jaccard_similarity(words1, words2), 3),
                        "shared_words": len(shared),
                        "unique_to_p1": len(unique_to_p1),
                        "unique_to_p2": len(unique_to_p2),
                        "top_shared": [
                            w
                            for w in shared
                            if period_words[p1][w] >= 2 and period_words[p2][w] >= 2
                        ][:10],
                    }
                )

        self.results["chronology"] = results
        return results

    # =========================================================================
    # REGIONAL VARIATION
    # =========================================================================

    def analyze_regional(self, sites: List[str] = None) -> dict:
        """
        Compare vocabulary across sites.

        Tests whether vocabulary differs significantly between major sites.
        """
        print("\n[Regional] Analyzing geographic vocabulary distribution...")

        # Default to major sites
        if sites is None:
            sites = ["HT", "KH", "ZA", "PH", "KN", "MA"]

        # Group inscriptions by site
        site_inscriptions = defaultdict(dict)
        for insc_id, data in self.corpus["inscriptions"].items():
            site_code = self._extract_site_code(insc_id)
            # Normalize site codes (e.g., HTW -> HT)
            base_site = re.match(r"^([A-Z]{2,3})", site_code)
            if base_site:
                base = base_site.group(1)
                for target in sites:
                    if base.startswith(target) or target.startswith(base):
                        site_inscriptions[target][insc_id] = data
                        break

        # Extract word frequencies for each site
        site_words = {}
        for site, inscriptions in site_inscriptions.items():
            if inscriptions:
                site_words[site] = self._extract_words(inscriptions)

        results = {
            "sites_analyzed": list(site_words.keys()),
            "inscription_counts": {s: len(site_inscriptions[s]) for s in site_words},
            "word_counts": {s: sum(wf.values()) for s, wf in site_words.items()},
            "unique_words": {s: len(wf) for s, wf in site_words.items()},
            "comparisons": [],
            "site_specific_words": {},
        }

        # Compare sites
        available_sites = list(site_words.keys())
        for i, s1 in enumerate(available_sites):
            for s2 in available_sites[i + 1 :]:
                words1 = set(site_words[s1].keys())
                words2 = set(site_words[s2].keys())

                results["comparisons"].append(
                    {
                        "site1": s1,
                        "site2": s2,
                        "jaccard_similarity": round(self._jaccard_similarity(words1, words2), 3),
                        "shared_words": len(words1 & words2),
                        "unique_to_s1": len(words1 - words2),
                        "unique_to_s2": len(words2 - words1),
                    }
                )

        # Find site-specific words (appear at one site but not others)
        for site in available_sites:
            site_vocab = set(site_words[site].keys())
            other_vocab = set()
            for other in available_sites:
                if other != site:
                    other_vocab.update(site_words[other].keys())

            unique = site_vocab - other_vocab
            # Filter to words with frequency >= 2
            unique_freq = [(w, site_words[site][w]) for w in unique if site_words[site][w] >= 2]
            unique_freq.sort(key=lambda x: x[1], reverse=True)

            results["site_specific_words"][site] = unique_freq[:10]

        self.results["regional"] = results
        return results

    # =========================================================================
    # REGISTER COMPARISON
    # =========================================================================

    def analyze_register(self) -> dict:
        """
        Compare administrative vs religious texts.

        Based on support type: Tablets = administrative, Stone vessels = religious
        """
        print("\n[Register] Analyzing administrative vs religious vocabulary...")

        # Classify by support type
        administrative = {}
        religious = {}

        for insc_id, data in self.corpus["inscriptions"].items():
            support = data.get("support", "").lower()

            if "tablet" in support or "nodule" in support or "roundel" in support:
                administrative[insc_id] = data
            elif "stone" in support or "metal" in support:
                religious[insc_id] = data

        # Extract word frequencies
        admin_words = self._extract_words(administrative)
        relig_words = self._extract_words(religious)

        admin_vocab = set(admin_words.keys())
        relig_vocab = set(relig_words.keys())

        results = {
            "administrative": {
                "inscriptions": len(administrative),
                "total_words": sum(admin_words.values()),
                "unique_words": len(admin_words),
            },
            "religious": {
                "inscriptions": len(religious),
                "total_words": sum(relig_words.values()),
                "unique_words": len(relig_words),
            },
            "jaccard_similarity": round(self._jaccard_similarity(admin_vocab, relig_vocab), 3),
            "shared_words": len(admin_vocab & relig_vocab),
            "admin_only": len(admin_vocab - relig_vocab),
            "religious_only": len(relig_vocab - admin_vocab),
            "top_admin_only": [
                (w, admin_words[w]) for w in (admin_vocab - relig_vocab) if admin_words[w] >= 3
            ][:10],
            "top_religious_only": [
                (w, relig_words[w]) for w in (relig_vocab - admin_vocab) if relig_words[w] >= 2
            ][:10],
        }

        # Sort by frequency
        results["top_admin_only"].sort(key=lambda x: x[1], reverse=True)
        results["top_religious_only"].sort(key=lambda x: x[1], reverse=True)

        self.results["register"] = results
        return results

    # =========================================================================
    # SIGN POSITION ANALYSIS
    # =========================================================================

    def analyze_positions(self) -> dict:
        """
        Chi-squared tests for sign positional preferences.

        Tests whether signs have significant positional preferences.
        """
        print("\n[Positions] Analyzing sign positional distributions...")

        sign_data = self.signs["signs"]
        results = {
            "signs_analyzed": 0,
            "significant_preferences": [],
            "random_distribution": [],
        }

        for sign, data in sign_data.items():
            total = data["total_occurrences"]
            if total < 20:  # Need sufficient data
                continue

            results["signs_analyzed"] += 1

            pos = data["position_frequency"]
            standalone = data["contexts"]["standalone"]

            # Observed frequencies
            observed = [pos["initial"], pos["medial"], pos["final"]]
            total_pos = sum(observed)

            if total_pos < 10:
                continue

            # Expected (uniform distribution)
            expected = [total_pos / 3] * 3

            # Calculate chi-squared
            chi_sq, df = self._chi_squared(observed, expected)

            # Chi-squared critical value at p=0.05, df=2 is 5.99
            significant = chi_sq > 5.99

            position_pcts = {
                "initial": round(pos["initial"] / total_pos * 100, 1) if total_pos > 0 else 0,
                "medial": round(pos["medial"] / total_pos * 100, 1) if total_pos > 0 else 0,
                "final": round(pos["final"] / total_pos * 100, 1) if total_pos > 0 else 0,
            }

            # Determine dominant position
            dominant = max(position_pcts, key=position_pcts.get)

            entry = {
                "sign": sign,
                "total": total,
                "chi_squared": round(chi_sq, 2),
                "significant": significant,
                "dominant_position": dominant,
                "dominant_pct": position_pcts[dominant],
                "positions": position_pcts,
            }

            if significant:
                results["significant_preferences"].append(entry)
            else:
                results["random_distribution"].append(entry)

        # Sort by chi-squared
        results["significant_preferences"].sort(key=lambda x: x["chi_squared"], reverse=True)

        self.results["positions"] = results
        return results

    # =========================================================================
    # ENTROPY ANALYSIS
    # =========================================================================

    def analyze_entropy(self) -> dict:
        """
        Calculate entropy measures for sign and word distributions.

        Higher entropy = more uniform distribution
        Lower entropy = more concentrated distribution
        """
        print("\n[Entropy] Calculating distribution entropy...")

        # Sign frequency entropy
        sign_freqs = [data["total_occurrences"] for data in self.signs["signs"].values()]
        sign_entropy = self._entropy(sign_freqs)

        # Word frequency entropy
        word_freqs = list(self.statistics["top_words"].values())
        word_entropy = self._entropy(word_freqs)

        # Position entropy for each sign
        position_entropies = []
        for sign, data in self.signs["signs"].items():
            pos = data["position_frequency"]
            pos_freqs = [pos["initial"], pos["medial"], pos["final"]]
            if sum(pos_freqs) >= 10:
                position_entropies.append(
                    {
                        "sign": sign,
                        "entropy": round(self._entropy(pos_freqs), 3),
                        "max_entropy": round(math.log2(3), 3),  # Max entropy for 3 categories
                    }
                )

        # Sort by entropy (low entropy = strong preference)
        position_entropies.sort(key=lambda x: x["entropy"])

        results = {
            "sign_frequency_entropy": round(sign_entropy, 3),
            "max_sign_entropy": round(math.log2(len(sign_freqs)), 3),
            "word_frequency_entropy": round(word_entropy, 3),
            "max_word_entropy": round(math.log2(len(word_freqs)), 3),
            "low_position_entropy_signs": position_entropies[:15],  # Strong positional preference
            "high_position_entropy_signs": position_entropies[-10:],  # Flexible position
        }

        self.results["entropy"] = results
        return results

    # =========================================================================
    # SUMMARY REPORT
    # =========================================================================

    def generate_summary(self) -> dict:
        """Generate full statistical summary."""
        print("\n" + "=" * 60)
        print("STATISTICAL ANALYSIS SUMMARY")
        print("=" * 60)

        # Run all analyses
        self.analyze_chronology()
        self.analyze_regional()
        self.analyze_register()
        self.analyze_positions()
        self.analyze_entropy()

        self.results["metadata"]["generated"] = datetime.now().isoformat()

        return self.results

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print human-readable summary."""
        print("\n" + "=" * 60)
        print("KEY FINDINGS")
        print("=" * 60)

        # Chronology
        if "chronology" in self.results:
            print("\n[CHRONOLOGY]")
            chr = self.results["chronology"]
            for comp in chr["comparisons"][:3]:
                print(
                    f"  {comp['period1']} vs {comp['period2']}: Jaccard={comp['jaccard_similarity']:.3f}"
                )

        # Regional
        if "regional" in self.results:
            print("\n[REGIONAL]")
            reg = self.results["regional"]
            for comp in reg["comparisons"][:3]:
                print(
                    f"  {comp['site1']} vs {comp['site2']}: Jaccard={comp['jaccard_similarity']:.3f}"
                )

            if reg.get("site_specific_words"):
                print("\n  Site-specific words:")
                for site, words in reg["site_specific_words"].items():
                    if words:
                        print(f"    {site}: {', '.join(w[0] for w in words[:5])}")

        # Register
        if "register" in self.results:
            print("\n[REGISTER]")
            reg = self.results["register"]
            print(f"  Admin vs Religious Jaccard: {reg['jaccard_similarity']:.3f}")
            print(f"  Admin-only words: {reg['admin_only']}")
            print(f"  Religious-only words: {reg['religious_only']}")

        # Positions
        if "positions" in self.results:
            print("\n[POSITIONS]")
            pos = self.results["positions"]
            print(f"  Signs with significant preference: {len(pos['significant_preferences'])}")
            top_prefs = pos["significant_preferences"][:5]
            for p in top_prefs:
                print(f"    {p['sign']}: {p['dominant_position']} ({p['dominant_pct']}%)")

        # Entropy
        if "entropy" in self.results:
            print("\n[ENTROPY]")
            ent = self.results["entropy"]
            print(
                f"  Sign distribution entropy: {ent['sign_frequency_entropy']:.3f} / {ent['max_sign_entropy']:.3f}"
            )
            print(
                f"  Word distribution entropy: {ent['word_frequency_entropy']:.3f} / {ent['max_word_entropy']:.3f}"
            )

        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Statistical analysis of Linear A corpus")
    parser.add_argument(
        "command",
        nargs="?",
        default="summary",
        choices=["chronology", "regional", "register", "positions", "entropy", "summary"],
        help="Analysis to run (default: summary)",
    )
    parser.add_argument(
        "--sites", type=str, nargs="+", help="Sites for regional comparison (e.g., HT KH ZA)"
    )
    parser.add_argument(
        "--compare", type=str, nargs=2, help="Periods for chronology comparison (e.g., MMIII LMIB)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/statistical_report.json",
        help="Output path for results",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed progress")

    args = parser.parse_args()

    analyzer = StatisticalAnalyzer(verbose=args.verbose)

    if not analyzer.load_data():
        return 1

    # Run requested analysis
    if args.command == "chronology":
        analyzer.analyze_chronology()
    elif args.command == "regional":
        analyzer.analyze_regional(sites=args.sites)
    elif args.command == "register":
        analyzer.analyze_register()
    elif args.command == "positions":
        analyzer.analyze_positions()
    elif args.command == "entropy":
        analyzer.analyze_entropy()
    else:  # summary
        analyzer.generate_summary()

    # Save and display results
    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)
    analyzer.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
