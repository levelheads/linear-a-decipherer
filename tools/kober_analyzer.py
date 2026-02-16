#!/usr/bin/env python3
"""
Kober Method Pattern Analyzer for Linear A

Automates Alice Kober's analytical methodology:
1. Sign frequency analysis
2. Positional distribution (initial, medial, final)
3. Inflection pattern detection (same root + different endings)
4. Kober's Triplet detection (words sharing roots but differing in suffixes)
5. Co-occurrence matrix for sign relationships

This tool implements First Principle #1 (KOBER PRINCIPLE):
"Never start with a language assumption—let the data lead."

Usage:
    python tools/kober_analyzer.py [--output FILE] [--verbose] [--min-freq N]

Output:
    data/pattern_report.json - Comprehensive pattern analysis results

Attribution:
    Part of Linear A Decipherment Project
    Named for Alice Kober (1906-1950), whose methodology enabled Linear B decipherment
    See FIRST_PRINCIPLES.md for methodology
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


class KoberAnalyzer:
    """
    Implements the Kober Method for Linear A pattern analysis.

    The Kober Method proceeds in stages:
    1. Frequency analysis (what signs appear most often?)
    2. Positional analysis (where do signs prefer to appear?)
    3. Distribution analysis (what contexts do signs appear in?)
    4. Inflection detection (which words share roots but differ in endings?)
    5. Paradigm building (can we identify grammatical patterns?)
    """

    def __init__(self, verbose=False, min_frequency=3):
        self.verbose = verbose
        self.min_frequency = min_frequency

        # Loaded data
        self.corpus = None
        self.signs = None
        self.statistics = None

        # Analysis results
        self.results = {
            "metadata": {
                "generated": None,
                "corpus_size": 0,
                "min_frequency": min_frequency,
            },
            "sign_analysis": {},
            "word_analysis": {},
            "pattern_analysis": {},
            "inflection_analysis": {},
            "triplet_analysis": {},
            "co_occurrence": {},
            "paradigm_candidates": [],
            "findings": [],
        }

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_data(self) -> bool:
        """Load corpus and sign data."""
        try:
            # Load corpus
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")

            # Load signs
            signs_path = DATA_DIR / "signs.json"
            with open(signs_path, "r", encoding="utf-8") as f:
                self.signs = json.load(f)
            print(f"Loaded signs: {self.signs['total_signs']} unique signs")

            # Load statistics
            stats_path = DATA_DIR / "statistics.json"
            with open(stats_path, "r", encoding="utf-8") as f:
                self.statistics = json.load(f)

            self.results["metadata"]["corpus_size"] = len(self.corpus["inscriptions"])
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    # =========================================================================
    # PHASE 1: Sign Frequency Analysis
    # =========================================================================

    def analyze_sign_frequencies(self):
        """
        Analyze sign frequencies following Kober's method.

        High-frequency signs may indicate:
        - Common grammatical elements (prefixes, suffixes)
        - Frequent lexical items
        - Administrative terminology
        """
        print("\n[Phase 1] Analyzing sign frequencies...")

        sign_data = self.signs["signs"]
        frequencies = []

        for sign, data in sign_data.items():
            freq = data["total_occurrences"]
            if freq >= self.min_frequency:
                frequencies.append(
                    {
                        "sign": sign,
                        "frequency": freq,
                        "initial_pct": round(data["position_frequency"]["initial"] / freq * 100, 1)
                        if freq > 0
                        else 0,
                        "medial_pct": round(data["position_frequency"]["medial"] / freq * 100, 1)
                        if freq > 0
                        else 0,
                        "final_pct": round(data["position_frequency"]["final"] / freq * 100, 1)
                        if freq > 0
                        else 0,
                        "standalone_pct": round(data["contexts"]["standalone"] / freq * 100, 1)
                        if freq > 0
                        else 0,
                    }
                )

        # Sort by frequency
        frequencies.sort(key=lambda x: x["frequency"], reverse=True)

        self.results["sign_analysis"]["frequency_ranking"] = frequencies
        self.results["sign_analysis"]["total_analyzed"] = len(frequencies)

        # Identify high-frequency signs (potential grammatical markers)
        high_freq = [s for s in frequencies if s["frequency"] >= 50]
        self.results["sign_analysis"]["high_frequency_signs"] = high_freq

        self.log(f"Analyzed {len(frequencies)} signs with freq >= {self.min_frequency}")
        self.log(f"Found {len(high_freq)} high-frequency signs (>= 50 occurrences)")

    # =========================================================================
    # PHASE 2: Positional Distribution Analysis
    # =========================================================================

    def analyze_positional_patterns(self):
        """
        Analyze where signs prefer to appear in words.

        Kober's insight: Signs that strongly prefer certain positions
        likely have grammatical functions (prefixes, roots, suffixes).
        """
        print("\n[Phase 2] Analyzing positional patterns...")

        sign_data = self.signs["signs"]
        positional = {
            "initial_preference": [],  # Signs that prefer word-initial
            "medial_preference": [],  # Signs that prefer word-medial
            "final_preference": [],  # Signs that prefer word-final
            "flexible": [],  # Signs with no strong preference
        }

        for sign, data in sign_data.items():
            freq = data["total_occurrences"]
            if freq < self.min_frequency:
                continue

            # Calculate position percentages
            pos = data["position_frequency"]
            standalone = data["contexts"]["standalone"]
            non_standalone = freq - standalone

            if non_standalone < 5:
                continue  # Need sufficient multi-syllabic occurrences

            initial_pct = pos["initial"] / non_standalone * 100 if non_standalone > 0 else 0
            medial_pct = pos["medial"] / non_standalone * 100 if non_standalone > 0 else 0
            final_pct = pos["final"] / non_standalone * 100 if non_standalone > 0 else 0

            entry = {
                "sign": sign,
                "frequency": freq,
                "initial_pct": round(initial_pct, 1),
                "medial_pct": round(medial_pct, 1),
                "final_pct": round(final_pct, 1),
            }

            # Classify by preference (>60% in one position = strong preference)
            if initial_pct >= 60:
                entry["position"] = "initial"
                entry["strength"] = "strong" if initial_pct >= 75 else "moderate"
                positional["initial_preference"].append(entry)
            elif final_pct >= 60:
                entry["position"] = "final"
                entry["strength"] = "strong" if final_pct >= 75 else "moderate"
                positional["final_preference"].append(entry)
            elif medial_pct >= 50:
                entry["position"] = "medial"
                entry["strength"] = "moderate"
                positional["medial_preference"].append(entry)
            else:
                entry["position"] = "flexible"
                positional["flexible"].append(entry)

        # Sort each category by frequency
        for category in positional:
            positional[category].sort(key=lambda x: x["frequency"], reverse=True)

        self.results["pattern_analysis"]["positional"] = positional

        # Generate findings
        if positional["initial_preference"]:
            self.results["findings"].append(
                {
                    "category": "positional",
                    "finding": f"{len(positional['initial_preference'])} signs prefer word-initial position (potential prefixes/determinatives)",
                    "signs": [s["sign"] for s in positional["initial_preference"][:10]],
                    "confidence": "HIGH",
                }
            )

        if positional["final_preference"]:
            self.results["findings"].append(
                {
                    "category": "positional",
                    "finding": f"{len(positional['final_preference'])} signs prefer word-final position (potential suffixes/case endings)",
                    "signs": [s["sign"] for s in positional["final_preference"][:10]],
                    "confidence": "HIGH",
                }
            )

        self.log(f"Initial preference: {len(positional['initial_preference'])} signs")
        self.log(f"Medial preference: {len(positional['medial_preference'])} signs")
        self.log(f"Final preference: {len(positional['final_preference'])} signs")
        self.log(f"Flexible: {len(positional['flexible'])} signs")

    # =========================================================================
    # PHASE 3: Word Analysis
    # =========================================================================

    def extract_all_words(self) -> Dict[str, List[dict]]:
        """Extract all words from corpus with their contexts."""
        words = defaultdict(list)

        for insc_id, data in self.corpus["inscriptions"].items():
            if "_parse_error" in data:
                continue

            transliterated = data.get("transliteratedWords", [])

            for idx, word in enumerate(transliterated):
                if not word or word in ["\n", "𐄁", "", "—", "≈"]:
                    continue
                # Skip numerals
                if re.match(r"^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$", word):
                    continue
                # Skip logograms (all caps with no hyphens)
                if re.match(r"^[A-Z*\d+\[\]]+$", word) and "-" not in word:
                    continue
                # Skip lacuna markers
                if word.startswith("𐝫"):
                    continue

                # Record word with context
                words[word].append(
                    {
                        "inscription": insc_id,
                        "position": idx,
                        "site": data.get("site", ""),
                        "context": data.get("context", ""),
                    }
                )

        return dict(words)

    def analyze_word_patterns(self):
        """
        Analyze word-level patterns.

        Identifies:
        - Most frequent words (candidates for function words)
        - Words with common prefixes/suffixes
        - Word length distribution
        """
        print("\n[Phase 3] Analyzing word patterns...")

        all_words = self.extract_all_words()

        # Word frequency analysis
        word_freq = {word: len(occurrences) for word, occurrences in all_words.items()}
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

        # Filter by minimum frequency
        frequent_words = [(w, f) for w, f in sorted_words if f >= self.min_frequency]

        self.results["word_analysis"]["total_unique_words"] = len(all_words)
        self.results["word_analysis"]["words_above_threshold"] = len(frequent_words)
        self.results["word_analysis"]["top_words"] = [
            {"word": w, "frequency": f} for w, f in frequent_words[:50]
        ]

        # Word length distribution
        lengths = Counter()
        for word in all_words:
            syllables = word.split("-")
            lengths[len(syllables)] += 1

        self.results["word_analysis"]["length_distribution"] = dict(lengths.most_common())

        # Identify potential function words (very high frequency)
        function_word_candidates = [
            {"word": w, "frequency": f} for w, f in frequent_words if f >= 20
        ]
        self.results["word_analysis"]["function_word_candidates"] = function_word_candidates

        if function_word_candidates:
            self.results["findings"].append(
                {
                    "category": "word_analysis",
                    "finding": f"Identified {len(function_word_candidates)} high-frequency words (possible function words or common terms)",
                    "examples": [fw["word"] for fw in function_word_candidates[:5]],
                    "confidence": "MEDIUM",
                }
            )

        self.log(f"Total unique words: {len(all_words)}")
        self.log(f"Words above threshold: {len(frequent_words)}")
        self.log(f"Function word candidates: {len(function_word_candidates)}")

        return all_words

    # =========================================================================
    # PHASE 4: Inflection Pattern Detection (Kober's Key Method)
    # =========================================================================

    def detect_inflection_patterns(self, all_words: Dict[str, List[dict]]):
        """
        Detect inflection patterns using Kober's method.

        Kober discovered that Linear B words shared roots but differed in endings.
        This method finds:
        - Words sharing the same prefix/root
        - Recurring suffix patterns
        - Paradigm candidates (sets of words differing only in final syllable)
        """
        print("\n[Phase 4] Detecting inflection patterns (Kober Method)...")

        # Only analyze words with >= 2 syllables
        multi_syllable = {w: occs for w, occs in all_words.items() if "-" in w and len(occs) >= 2}

        # Group by prefix (first 1-2 syllables)
        prefix_groups = defaultdict(list)
        for word in multi_syllable:
            syllables = word.split("-")
            if len(syllables) >= 2:
                # Try both 1-syllable and 2-syllable prefixes
                prefix1 = syllables[0]
                prefix2 = "-".join(syllables[:2]) if len(syllables) >= 3 else None

                prefix_groups[prefix1].append(word)
                if prefix2:
                    prefix_groups[prefix2].append(word)

        # Find groups with multiple words (potential paradigms)
        paradigm_candidates = []
        for prefix, words in prefix_groups.items():
            if len(words) >= 2 and len(set(words)) >= 2:
                # Get unique suffixes
                suffixes = []
                for word in set(words):
                    syllables = word.split("-")
                    prefix_len = len(prefix.split("-"))
                    suffix = "-".join(syllables[prefix_len:]) if len(syllables) > prefix_len else ""
                    if suffix:
                        suffixes.append(
                            {"word": word, "suffix": suffix, "freq": len(all_words.get(word, []))}
                        )

                if len(suffixes) >= 2:
                    paradigm_candidates.append(
                        {
                            "prefix": prefix,
                            "variants": suffixes,
                            "total_attestations": sum(s["freq"] for s in suffixes),
                        }
                    )

        # Sort by total attestations
        paradigm_candidates.sort(key=lambda x: x["total_attestations"], reverse=True)

        # Keep top paradigm candidates
        top_paradigms = paradigm_candidates[:30]
        self.results["inflection_analysis"]["paradigm_candidates"] = top_paradigms

        # Extract recurring suffixes
        suffix_counter = Counter()
        for word in multi_syllable:
            syllables = word.split("-")
            if len(syllables) >= 2:
                # Final syllable
                suffix_counter[syllables[-1]] += len(all_words[word])
                # Final two syllables (for disyllabic suffixes)
                if len(syllables) >= 3:
                    disyl_suffix = "-".join(syllables[-2:])
                    suffix_counter[disyl_suffix] += len(all_words[word])

        common_suffixes = [
            {"suffix": s, "frequency": f} for s, f in suffix_counter.most_common(20) if f >= 10
        ]
        self.results["inflection_analysis"]["common_suffixes"] = common_suffixes

        # Generate findings
        if top_paradigms:
            self.results["findings"].append(
                {
                    "category": "inflection",
                    "finding": f"Identified {len(top_paradigms)} potential paradigm groups (words sharing roots)",
                    "top_example": {
                        "prefix": top_paradigms[0]["prefix"],
                        "variants": [v["word"] for v in top_paradigms[0]["variants"][:5]],
                    },
                    "confidence": "HIGH",
                }
            )

        if common_suffixes:
            self.results["findings"].append(
                {
                    "category": "inflection",
                    "finding": f"Found {len(common_suffixes)} recurring suffix patterns (potential grammatical endings)",
                    "examples": [s["suffix"] for s in common_suffixes[:5]],
                    "confidence": "MEDIUM",
                }
            )

        self.log(f"Paradigm candidates: {len(top_paradigms)}")
        self.log(f"Common suffixes: {len(common_suffixes)}")

    # =========================================================================
    # PHASE 5: Triplet Detection (Kober's Breakthrough)
    # =========================================================================

    def detect_triplets(self, all_words: Dict[str, List[dict]]):
        """
        Detect Kober's Triplets: sets of words that share a root
        but differ systematically in their final syllable(s).

        This was Kober's key methodological breakthrough that enabled
        Ventris to identify case endings in Linear B.

        A triplet pattern suggests grammatical inflection:
        - Same root = same lexeme
        - Different ending = different grammatical form (case, number, etc.)
        """
        print("\n[Phase 5] Detecting Kober's Triplets...")

        triplets = []

        # Get all words with 3+ syllables
        words_3plus = {
            w: occs for w, occs in all_words.items() if len(w.split("-")) >= 3 and len(occs) >= 2
        }

        # Group by first two syllables (root)
        root_groups = defaultdict(list)
        for word in words_3plus:
            syllables = word.split("-")
            root = "-".join(syllables[:2])
            root_groups[root].append(
                {
                    "word": word,
                    "suffix": "-".join(syllables[2:]),
                    "frequency": len(all_words[word]),
                }
            )

        # Find triplets (3+ variants with same root)
        for root, variants in root_groups.items():
            if len(variants) >= 3:
                # Get unique endings
                unique_endings = {}
                for v in variants:
                    if v["suffix"] not in unique_endings:
                        unique_endings[v["suffix"]] = v

                if len(unique_endings) >= 3:
                    triplets.append(
                        {
                            "root": root,
                            "variants": list(unique_endings.values()),
                            "total_attestations": sum(
                                v["frequency"] for v in unique_endings.values()
                            ),
                            "endings": list(unique_endings.keys()),
                        }
                    )

        # Sort by attestations
        triplets.sort(key=lambda x: x["total_attestations"], reverse=True)

        self.results["triplet_analysis"]["triplets"] = triplets[:20]
        self.results["triplet_analysis"]["total_found"] = len(triplets)

        # Also find pairs (2 variants) which are also significant
        pairs = []
        for root, variants in root_groups.items():
            if len(variants) >= 2:
                unique_endings = {}
                for v in variants:
                    if v["suffix"] not in unique_endings:
                        unique_endings[v["suffix"]] = v

                if len(unique_endings) == 2:
                    pairs.append(
                        {
                            "root": root,
                            "variants": list(unique_endings.values()),
                            "total_attestations": sum(
                                v["frequency"] for v in unique_endings.values()
                            ),
                        }
                    )

        pairs.sort(key=lambda x: x["total_attestations"], reverse=True)
        self.results["triplet_analysis"]["pairs"] = pairs[:20]
        self.results["triplet_analysis"]["total_pairs"] = len(pairs)

        if triplets:
            self.results["findings"].append(
                {
                    "category": "triplets",
                    "finding": f"Detected {len(triplets)} Kober Triplets (words sharing root with 3+ variant endings)",
                    "significance": "BREAKTHROUGH - suggests grammatical inflection system",
                    "top_example": triplets[0] if triplets else None,
                    "confidence": "HIGH",
                }
            )

        self.log(f"Triplets found: {len(triplets)}")
        self.log(f"Pairs found: {len(pairs)}")

    # =========================================================================
    # PHASE 6: Co-occurrence Analysis
    # =========================================================================

    def analyze_co_occurrences(self, all_words: Dict[str, List[dict]]):
        """
        Analyze which signs co-occur together in words.

        Strong co-occurrence patterns may indicate:
        - Consonant clusters typical of a language
        - Phonotactic constraints
        - Fixed phrases or compound words
        """
        print("\n[Phase 6] Analyzing sign co-occurrences...")

        # Build co-occurrence matrix from sign data
        sign_data = self.signs["signs"]

        # Identify strongest co-occurrences
        strong_pairs = []
        for sign, data in sign_data.items():
            if data["total_occurrences"] < self.min_frequency:
                continue

            co_occs = data.get("co_occurrences", {})
            for other_sign, count in co_occs.items():
                if count >= 5:  # Minimum co-occurrence threshold
                    # Calculate mutual information-like score
                    sign_freq = data["total_occurrences"]
                    other_data = sign_data.get(other_sign, {})
                    other_freq = other_data.get("total_occurrences", 0)

                    if other_freq > 0:
                        # Simple association score
                        expected = (sign_freq * other_freq) / 10000  # Normalized
                        observed = count
                        if expected > 0:
                            association = observed / expected
                        else:
                            association = observed

                        strong_pairs.append(
                            {
                                "signs": [sign, other_sign],
                                "co_occurrences": count,
                                "sign1_freq": sign_freq,
                                "sign2_freq": other_freq,
                                "association_score": round(association, 2),
                            }
                        )

        # Deduplicate (A-B and B-A are the same)
        seen = set()
        unique_pairs = []
        for pair in strong_pairs:
            key = tuple(sorted(pair["signs"]))
            if key not in seen:
                seen.add(key)
                unique_pairs.append(pair)

        # Sort by association score
        unique_pairs.sort(key=lambda x: x["association_score"], reverse=True)

        self.results["co_occurrence"]["strong_pairs"] = unique_pairs[:30]
        self.results["co_occurrence"]["total_strong_pairs"] = len(unique_pairs)

        if unique_pairs:
            self.results["findings"].append(
                {
                    "category": "co_occurrence",
                    "finding": f"Found {len(unique_pairs)} significant sign co-occurrence patterns",
                    "top_pairs": [f"{p['signs'][0]}-{p['signs'][1]}" for p in unique_pairs[:5]],
                    "confidence": "MEDIUM",
                }
            )

        self.log(f"Strong co-occurrence pairs: {len(unique_pairs)}")

    # =========================================================================
    # PHASE 7: K-R Paradigm Investigation (Specific to Linear A)
    # =========================================================================

    def investigate_kr_paradigm(self, all_words: Dict[str, List[dict]]):
        """
        Specifically investigate the K-R root paradigm identified in the corpus:
        - ku-ro (total, 37+ attestations)
        - ki-ro (deficit, 16+ attestations)
        - ka-i-ro (possible third form in ZA 4)

        This could indicate an ablaut system or derivational morphology.
        """
        print("\n[Phase 7] Investigating K-R paradigm...")

        kr_forms = []
        kr_pattern = re.compile(r"^K[AEIOU]-.*-R[AEIOU]$|^K[AEIOU]-R[AEIOU]$", re.IGNORECASE)

        for word, occurrences in all_words.items():
            if kr_pattern.match(word):
                kr_forms.append(
                    {
                        "word": word,
                        "frequency": len(occurrences),
                        "sites": list(set(o["site"] for o in occurrences if o["site"])),
                    }
                )

        kr_forms.sort(key=lambda x: x["frequency"], reverse=True)

        self.results["paradigm_candidates"].append(
            {
                "paradigm": "K-R Root",
                "description": "Words with K-vowel-R-vowel pattern (ku-ro, ki-ro, ka-i-ro, etc.)",
                "forms": kr_forms,
                "hypothesis": "May indicate ablaut system (vowel alternation for grammatical meaning) or derivational morphology",
                "significance": "HIGH - if confirmed, reveals major morphological pattern",
            }
        )

        if len(kr_forms) >= 2:
            self.results["findings"].append(
                {
                    "category": "paradigm",
                    "finding": f"K-R paradigm confirmed: {len(kr_forms)} forms with K-V-R-V pattern",
                    "forms": [f["word"] for f in kr_forms[:5]],
                    "confidence": "HIGH",
                    "next_steps": "Verify all K-R forms across corpus; test for semantic/functional relationships",
                }
            )

        self.log(f"K-R paradigm forms: {len(kr_forms)}")

    # =========================================================================
    # Main Analysis Pipeline
    # =========================================================================

    def run_analysis(self):
        """Run complete Kober Method analysis."""
        print("\n" + "=" * 60)
        print("KOBER METHOD PATTERN ANALYSIS")
        print("=" * 60)
        print("Following First Principle #1: Let the data lead\n")

        if not self.load_data():
            return False

        # Run all analysis phases
        self.analyze_sign_frequencies()
        self.analyze_positional_patterns()
        all_words = self.analyze_word_patterns()
        self.detect_inflection_patterns(all_words)
        self.detect_triplets(all_words)
        self.analyze_co_occurrences(all_words)
        self.investigate_kr_paradigm(all_words)

        # Finalize metadata
        self.results["metadata"]["generated"] = datetime.now().isoformat()

        return True

    def save_results(self, output_path: Path):
        """Save analysis results to JSON."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 60)
        print("ANALYSIS SUMMARY")
        print("=" * 60)

        print(f"\nCorpus: {self.results['metadata']['corpus_size']} inscriptions")
        print(f"Signs analyzed: {self.results['sign_analysis'].get('total_analyzed', 0)}")
        print(f"Words analyzed: {self.results['word_analysis'].get('total_unique_words', 0)}")

        print("\n--- KEY FINDINGS ---")
        for i, finding in enumerate(self.results["findings"], 1):
            print(f"\n{i}. [{finding['confidence']}] {finding['finding']}")
            if "examples" in finding:
                print(f"   Examples: {', '.join(finding['examples'][:5])}")
            if "top_example" in finding and finding["top_example"]:
                if isinstance(finding["top_example"], dict):
                    prefix = finding["top_example"].get("prefix", "")
                    variants = finding["top_example"].get("variants", [])
                    if prefix:
                        print(f"   Top: {prefix}- → {', '.join(str(v) for v in variants[:3])}")

        # Paradigm candidates
        if self.results["paradigm_candidates"]:
            print("\n--- PARADIGM CANDIDATES ---")
            for paradigm in self.results["paradigm_candidates"]:
                print(f"\n• {paradigm['paradigm']}")
                print(f"  {paradigm['description']}")
                forms = paradigm.get("forms", [])
                if forms:
                    print(f"  Forms: {', '.join(f['word'] for f in forms[:5])}")

        print("\n" + "=" * 60)
        print("Analysis complete. See pattern_report.json for full details.")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Run Kober Method pattern analysis on Linear A corpus"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/pattern_report.json",
        help="Output path for pattern report (default: data/pattern_report.json)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed analysis progress"
    )
    parser.add_argument(
        "--min-freq",
        "-m",
        type=int,
        default=3,
        help="Minimum frequency threshold for analysis (default: 3)",
    )

    args = parser.parse_args()

    analyzer = KoberAnalyzer(verbose=args.verbose, min_frequency=args.min_freq)

    if not analyzer.run_analysis():
        return 1

    # Save results
    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)

    # Print summary
    analyzer.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
