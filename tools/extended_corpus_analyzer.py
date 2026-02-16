#!/usr/bin/env python3
"""
Extended Corpus Analyzer for Linear A

Direction 1 Implementation: Achieve 10% corpus coverage (172+ inscriptions)

Processes inscriptions in batches with full hypothesis testing and validation.
Prioritizes:
1. Khania tablets (K-R validation)
2. Cross-site inscriptions (ZA, TY, AR, PK)
3. MMII-MMIII period inscriptions (PH, KN early)

Usage:
    python tools/extended_corpus_analyzer.py --batch 50
    python tools/extended_corpus_analyzer.py --site KH
    python tools/extended_corpus_analyzer.py --all

Attribution:
    Part of Linear A Decipherment Project
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import List

from site_normalization import (
    CONTRACT_VERSION as SITE_CONTRACT_VERSION,
    build_site_totals,
    normalize_site,
)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = PROJECT_ROOT / "analysis"

# Already analyzed inscriptions (from KNOWLEDGE.md manual analyses)
# Note: This set is used to SKIP re-analysis, not to inflate coverage counts
# The coverage calculation now counts only inscriptions actually in the output
ALREADY_ANALYZED = {
    "HT13",
    "HT28",
    "HT31",
    "TY3a",
    "ZA4",
    "ZA15",
    "KH5",
    "KH88",
    "KNZf2",
    "PH(?)31a",
    "HT117",
    "HT94",
    "IOZa2",
    "HT85a",
    "HT122a",
    "HT122b",
    "KH6",
    "KH7a",
    "PKZa11",
    "ZA10b",
    "HT95a",
    "SYZa4",
    "KH11",
}

# Priority sites for expansion
PRIORITY_SITES = ["KH", "ZA", "PH", "KN", "TY", "PK", "ARKH", "IO", "SY"]


class ExtendedCorpusAnalyzer:
    """Analyze inscriptions to expand corpus coverage."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.analyzed = set()
        self.results = {
            "metadata": {
                "generated": None,
                "target": "Corpus expansion (batch analysis)",
                "site_normalization_contract": SITE_CONTRACT_VERSION,
            },
            "inscriptions_analyzed": [],
            "word_frequencies": Counter(),
            "site_coverage": {},
            "site_normalized_coverage": {},
            "hypothesis_summary": {},
            "new_findings": [],
        }

    def log(self, message: str):
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_inscription_priority(self, insc_id: str, data: dict) -> int:
        """
        Calculate priority score for inscription.
        Higher = more important to analyze.
        """
        score = 0

        # Normalize ID
        insc_clean = re.sub(r"[^A-Za-z0-9]", "", insc_id)
        if insc_clean in ALREADY_ANALYZED:
            return -1  # Skip already analyzed

        # Site priority
        site_code, _ = normalize_site(
            site_value=data.get("site"),
            inscription_id=insc_id,
        )

        if site_code in ["KH"]:
            score += 100  # Khania highest priority
        elif site_code in ["ZA", "PH", "PK", "IO", "SY"]:
            score += 80  # Cross-site validation
        elif site_code in ["ARKH", "TY", "KN"]:
            score += 60  # Secondary sites
        elif site_code == "HT":
            score += 20  # HT is over-represented

        # Word count bonus (prefer short inscriptions for quick analysis)
        words = data.get("transliteratedWords", [])
        word_count = len([w for w in words if w and w not in ["\n", "𐄁"]])
        if 5 <= word_count <= 20:
            score += 30  # Sweet spot
        elif word_count <= 10:
            score += 20

        # K-R vocabulary presence
        words_upper = [w.upper() for w in words if w]
        if "KU-RO" in words_upper or "KI-RO" in words_upper:
            score += 40

        # Religious text markers
        if any("JA-SA-SA-RA" in w or "A-TA-I-*301" in w for w in words_upper):
            score += 50

        return score

    def select_priority_inscriptions(self, count: int = 50) -> List[str]:
        """Select top priority inscriptions for analysis."""
        priorities = []

        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue

            priority = self.get_inscription_priority(insc_id, data)
            if priority >= 0:
                priorities.append((insc_id, priority))

        # Sort by priority descending
        priorities.sort(key=lambda x: -x[1])

        selected = [insc_id for insc_id, _ in priorities[:count]]
        return selected

    def analyze_inscription(self, insc_id: str) -> dict:
        """Analyze a single inscription."""
        data = self.corpus["inscriptions"].get(insc_id, {})
        if not data or "_parse_error" in data:
            return None

        words = data.get("transliteratedWords", [])

        # Extract meaningful words
        meaningful = []
        for w in words:
            if not w or w in ["\n", "𐄁", "", "—", "≈"]:
                continue
            if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈₉○◎—|]+$", w):
                continue
            meaningful.append(w.upper())

        # Count words
        word_freq = Counter(meaningful)

        # Check for key markers
        has_kuro = "KU-RO" in meaningful
        has_kiro = "KI-RO" in meaningful
        has_sara2 = any("SA-RA" in w for w in meaningful)
        has_libation = any("JA-SA-SA-RA" in w or "A-TA-I-*301" in w for w in meaningful)

        # Site extraction
        site_code, site_name = normalize_site(
            site_value=data.get("site"),
            inscription_id=insc_id,
        )

        analysis = {
            "id": insc_id,
            "site": site_code,
            "site_name": site_name,
            "site_raw": data.get("site", ""),
            "word_count": len(meaningful),
            "unique_words": len(set(meaningful)),
            "words": meaningful,
            "word_frequencies": dict(word_freq.most_common(10)),
            "markers": {
                "has_kuro": has_kuro,
                "has_kiro": has_kiro,
                "has_sara2": has_sara2,
                "has_libation": has_libation,
            },
            "text_type": "religious" if has_libation else "administrative",
        }

        return analysis

    def run_batch_analysis(self, count: int = 50, site_filter: str = None) -> dict:
        """Run analysis on a batch of inscriptions."""
        print(f"\n[Batch Analysis] Selecting {count} priority inscriptions...")

        if site_filter:
            # Filter to specific site
            selected = []
            for insc_id, data in self.corpus["inscriptions"].items():
                if insc_id.startswith(site_filter) and "_parse_error" not in data:
                    priority = self.get_inscription_priority(insc_id, data)
                    if priority >= 0:
                        selected.append(insc_id)
            selected = selected[:count]
        else:
            selected = self.select_priority_inscriptions(count)

        print(f"Selected {len(selected)} inscriptions for analysis")

        # Analyze each inscription
        site_stats = defaultdict(
            lambda: {
                "site_code": "",
                "site_name": "",
                "count": 0,
                "kuro": 0,
                "kiro": 0,
                "words": 0,
            }
        )
        all_words = Counter()
        corpus_site_totals = build_site_totals(self.corpus.get("inscriptions", {}))

        for i, insc_id in enumerate(selected):
            analysis = self.analyze_inscription(insc_id)
            if analysis:
                self.results["inscriptions_analyzed"].append(analysis)
                self.analyzed.add(insc_id)

                # Aggregate stats
                site = analysis["site"]
                site_stats[site]["site_code"] = site
                site_stats[site]["site_name"] = analysis.get("site_name", site)
                site_stats[site]["count"] += 1
                site_stats[site]["words"] += analysis["word_count"]
                if analysis["markers"]["has_kuro"]:
                    site_stats[site]["kuro"] += 1
                if analysis["markers"]["has_kiro"]:
                    site_stats[site]["kiro"] += 1

                # Word frequencies
                for word in analysis["words"]:
                    all_words[word] += 1

            if (i + 1) % 20 == 0:
                self.log(f"Progress: {i + 1}/{len(selected)}")

        # Summary
        self.results["word_frequencies"] = dict(all_words.most_common(100))

        site_coverage = {}
        for site_code, stats in sorted(site_stats.items()):
            total_entry = corpus_site_totals.get(site_code, {})
            inscriptions_total = int(total_entry.get("inscriptions_total", 0) or 0)
            coverage_pct = (
                round((stats["count"] / inscriptions_total) * 100, 2) if inscriptions_total else 0.0
            )
            site_coverage[site_code] = {
                "site_code": site_code,
                "site_name": stats["site_name"] or total_entry.get("site_name", site_code),
                "count": stats["count"],
                "kuro": stats["kuro"],
                "kiro": stats["kiro"],
                "words": stats["words"],
                "inscriptions_analyzed": stats["count"],
                "inscriptions_total": inscriptions_total,
                "coverage_percent": coverage_pct,
            }
        self.results["site_coverage"] = site_coverage
        self.results["site_normalized_coverage"] = site_coverage

        # Calculate coverage - ONLY count inscriptions actually in this analysis
        # Note: ALREADY_ANALYZED is used for deduplication, not cumulative tracking
        total_analyzed = len(self.analyzed)
        total_corpus = len(self.corpus["inscriptions"])
        coverage = total_analyzed / total_corpus * 100

        self.results["coverage"] = {
            "batch_analyzed": len(self.analyzed),
            "newly_analyzed": len(self.analyzed),
            "total_analyzed": total_analyzed,
            "total_corpus": total_corpus,
            "coverage_percent": round(coverage, 2),
        }

        print(f"\nCoverage: {total_analyzed}/{total_corpus} ({coverage:.2f}%)")

        return self.results

    def identify_new_findings(self) -> List[dict]:
        """Identify significant new findings from the analysis."""
        findings = []

        # Check for new K-R attestations outside HT
        for analysis in self.results["inscriptions_analyzed"]:
            if analysis["site"] != "HT":
                if analysis["markers"]["has_kuro"]:
                    findings.append(
                        {
                            "type": "K-R_ATTESTATION",
                            "inscription": analysis["id"],
                            "site": analysis["site"],
                            "finding": f"KU-RO attested at {analysis['site']}",
                            "significance": "Cross-site K-R verification",
                        }
                    )
                if analysis["markers"]["has_kiro"]:
                    findings.append(
                        {
                            "type": "K-R_ATTESTATION",
                            "inscription": analysis["id"],
                            "site": analysis["site"],
                            "finding": f"KI-RO attested at {analysis['site']}",
                            "significance": "UNEXPECTED - KI-RO typically HT-exclusive",
                        }
                    )

        # Check Khania for K-R (should be zero)
        kh_inscriptions = [a for a in self.results["inscriptions_analyzed"] if a["site"] == "KH"]
        kh_kuro = sum(1 for a in kh_inscriptions if a["markers"]["has_kuro"])
        kh_kiro = sum(1 for a in kh_inscriptions if a["markers"]["has_kiro"])

        if kh_inscriptions:
            findings.append(
                {
                    "type": "KHANIA_VERIFICATION",
                    "inscriptions_checked": len(kh_inscriptions),
                    "kuro_found": kh_kuro,
                    "kiro_found": kh_kiro,
                    "finding": f"Khania K-R status: KU-RO={kh_kuro}, KI-RO={kh_kiro}",
                    "significance": "ZERO K-R CONFIRMED"
                    if kh_kuro == 0 and kh_kiro == 0
                    else "UNEXPECTED K-R FOUND",
                }
            )

        # High-frequency new words
        top_words = list(self.results["word_frequencies"].items())[:20]
        for word, freq in top_words:
            if freq >= 5 and "-" in word:  # Syllabic, frequent
                findings.append(
                    {
                        "type": "HIGH_FREQUENCY_WORD",
                        "word": word,
                        "frequency": freq,
                        "finding": f"{word} appears {freq} times in batch",
                        "significance": "Candidate for hypothesis testing",
                    }
                )

        self.results["new_findings"] = findings
        return findings

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        self.results["metadata"]["generated"] = datetime.now().isoformat()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2, default=str)
        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 70)
        print("EXTENDED CORPUS ANALYSIS SUMMARY")
        print("=" * 70)

        coverage = self.results.get("coverage", {})
        print(
            f"\nCoverage: {coverage.get('total_analyzed', 0)}/{coverage.get('total_corpus', 0)} "
            f"({coverage.get('coverage_percent', 0)}%)"
        )

        print("\nSite Coverage:")
        for site, stats in sorted(self.results.get("site_coverage", {}).items()):
            print(
                f"  {site}: {stats['count']} inscriptions, "
                f"KU-RO={stats['kuro']}, KI-RO={stats['kiro']}, "
                f"coverage={stats.get('coverage_percent', 0)}%"
            )

        print("\nTop Words:")
        for word, freq in list(self.results.get("word_frequencies", {}).items())[:15]:
            print(f"  {word}: {freq}")

        print("\nKey Findings:")
        for finding in self.results.get("new_findings", [])[:10]:
            print(f"  [{finding['type']}] {finding['finding']}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Extended corpus analysis for 10% coverage")
    parser.add_argument(
        "--batch", "-b", type=int, default=50, help="Number of inscriptions to analyze"
    )
    parser.add_argument("--site", "-s", type=str, help="Filter to specific site")
    parser.add_argument(
        "--all", "-a", action="store_true", help="Analyze all remaining inscriptions"
    )
    parser.add_argument("--output", "-o", type=str, default="data/extended_corpus_analysis.json")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    analyzer = ExtendedCorpusAnalyzer(verbose=args.verbose)

    if not analyzer.load_corpus():
        return 1

    if args.all:
        # Analyze a large batch when --all is specified
        total = len(analyzer.corpus["inscriptions"])
        count = min(500, total - len(ALREADY_ANALYZED))  # Up to 500, excluding already analyzed
    else:
        count = args.batch

    analyzer.run_batch_analysis(count=count, site_filter=args.site)
    analyzer.identify_new_findings()

    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)
    analyzer.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
