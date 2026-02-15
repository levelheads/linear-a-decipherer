#!/usr/bin/env python3
"""
Regional Variation Analyzer for Linear A

Compares vocabulary and patterns across major Linear A archives:
- HT (Hagia Triada): 199 tablets - central administration
- KH (Khania): 104 tablets - western Crete
- ZA (Zakros): 44 tablets - eastern port
- PH (Phaistos): 45 tablets - oldest corpus (MMIII)

This tool addresses key research questions:
1. Is Linear A vocabulary standardized across Crete?
2. Does ku-ro/ki-ro usage vary by site?
3. Are there regional administrative conventions?

Usage:
    python tools/regional_analyzer.py [--sites SITE1,SITE2] [--output FILE]

Examples:
    python tools/regional_analyzer.py --all
    python tools/regional_analyzer.py --sites HT,KH --verbose
    python tools/regional_analyzer.py --all --output data/regional_analysis.json

Attribution:
    Part of Linear A Decipherment Project
    Implements corpus-wide verification (First Principle #6)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List

from site_normalization import (
    CONTRACT_VERSION as SITE_CONTRACT_VERSION,
    build_site_totals,
    normalize_site,
)


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Major site codes and their variants
SITE_MAPPINGS = {
    'HT': ['HT', 'HTW', 'HTZ'],  # Hagia Triada
    'KH': ['KH', 'KHW', 'KHZ'],  # Khania
    'ZA': ['ZA', 'ZAW', 'ZAZ'],  # Zakros
    'PH': ['PH', 'PHW', 'PHZ'],  # Phaistos
    'KN': ['KN', 'KNW', 'KNZ'],  # Knossos
    'MA': ['MA', 'MAW', 'MAZ'],  # Malia
    'TY': ['TY', 'TYW', 'TYZ'],  # Tylissos
    'PK': ['PK', 'PKZ'],         # Palaikastro
}

SITE_FULL_NAMES = {
    'HT': 'Hagia Triada',
    'KH': 'Khania',
    'ZA': 'Zakros',
    'PH': 'Phaistos',
    'KN': 'Knossos',
    'MA': 'Malia',
    'TY': 'Tylissos',
    'PK': 'Palaikastro',
}


class RegionalAnalyzer:
    """
    Analyzes regional variation in Linear A vocabulary and patterns.

    For each site, extracts:
    - Unique vocabulary with frequencies
    - K-R paradigm usage (ku-ro, ki-ro variants)
    - Common formulaic patterns
    - Logograms in use
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.site_vocabularies = {}
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'Regional Variation Analysis',
                'principle': 'First Principle #6: Cross-Corpus Consistency',
                'site_normalization_contract': SITE_CONTRACT_VERSION,
            },
            'site_summaries': {},
            'vocabulary_comparisons': {},
            'kr_paradigm_by_site': {},
            'site_specific_words': {},
            'shared_vocabulary': {},
            'overall_findings': {},
        }
        self.corpus_site_totals = {}

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)
            self.corpus_site_totals = build_site_totals(self.corpus.get('inscriptions', {}))
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _get_site_code(self, inscription_id: str, data: dict) -> str:
        """Extract site code from inscription ID."""
        site_code, _ = normalize_site(
            site_value=data.get('site') if isinstance(data, dict) else None,
            inscription_id=inscription_id,
        )
        return site_code

    def _is_valid_word(self, word: str) -> bool:
        """Check if word is valid for analysis (not numeral, logogram-only, etc.)."""
        if not word or word in ['\n', '𐄁', '', '—', '≈']:
            return False
        # Skip pure numerals
        if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈₉○◎—|]+$', word):
            return False
        # Skip fractional markers
        if word.startswith('¹⁄') or word.startswith('³⁄') or word.startswith('≈'):
            return False
        # Skip damaged/unclear markers
        if word.startswith('𐝫') or word == '𐝫':
            return False
        return True

    def _is_syllabic_word(self, word: str) -> bool:
        """Check if word contains syllabic signs (has hyphens)."""
        return '-' in word and self._is_valid_word(word)

    def extract_site_vocabulary(self, site_code: str) -> tuple[Dict[str, int], int]:
        """
        Extract vocabulary for a specific site.

        Returns dict of word -> frequency for all inscriptions from the site.
        """
        word_freq = Counter()
        inscription_count = 0

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            # Check if inscription belongs to this site
            insc_site = self._get_site_code(insc_id, data)
            if insc_site != site_code:
                continue

            inscription_count += 1
            words = data.get('transliteratedWords', [])

            for word in words:
                if self._is_valid_word(word):
                    word_freq[word] += 1

        self.log(f"Site {site_code}: {inscription_count} inscriptions, {len(word_freq)} unique words")
        return dict(word_freq), inscription_count

    def extract_all_site_vocabularies(self, sites: List[str] = None):
        """Extract vocabulary for all specified sites."""
        if sites is None:
            sites = list(SITE_MAPPINGS.keys())

        print("\nExtracting site vocabularies...")
        for site in sites:
            vocab, inscription_count = self.extract_site_vocabulary(site)
            self.site_vocabularies[site] = vocab

            # Store summary
            site_total = int(self.corpus_site_totals.get(site, {}).get('inscriptions_total', 0) or 0)
            coverage_pct = round((inscription_count / site_total) * 100, 2) if site_total else 0.0
            site_name = self.corpus_site_totals.get(site, {}).get('site_name', SITE_FULL_NAMES.get(site, site))
            self.results['site_summaries'][site] = {
                'name': site_name,
                'unique_words': len(vocab),
                'total_tokens': sum(vocab.values()),
                'syllabic_words': len([w for w in vocab if '-' in w]),
                'inscriptions_analyzed': inscription_count,
                'inscriptions_total': site_total,
                'coverage_percent': coverage_pct,
                'top_words': dict(Counter(vocab).most_common(20)),
            }

    def calculate_vocabulary_overlap(self, site1: str, site2: str) -> dict:
        """
        Calculate vocabulary overlap between two sites.

        Returns Jaccard similarity and shared/unique word counts.
        """
        vocab1 = set(self.site_vocabularies.get(site1, {}).keys())
        vocab2 = set(self.site_vocabularies.get(site2, {}).keys())

        # Only consider syllabic words for meaningful comparison
        syllabic1 = {w for w in vocab1 if '-' in w}
        syllabic2 = {w for w in vocab2 if '-' in w}

        shared = syllabic1 & syllabic2
        only_in_1 = syllabic1 - syllabic2
        only_in_2 = syllabic2 - syllabic1

        # Jaccard similarity
        union = syllabic1 | syllabic2
        jaccard = len(shared) / len(union) if union else 0

        return {
            'site1': site1,
            'site2': site2,
            'shared_count': len(shared),
            'only_in_site1': len(only_in_1),
            'only_in_site2': len(only_in_2),
            'jaccard_similarity': round(jaccard, 4),
            'shared_words': sorted(list(shared))[:50],  # Top 50
            'unique_to_site1': sorted(list(only_in_1))[:20],
            'unique_to_site2': sorted(list(only_in_2))[:20],
        }

    def calculate_all_overlaps(self, sites: List[str] = None):
        """Calculate vocabulary overlap for all site pairs."""
        if sites is None:
            sites = list(self.site_vocabularies.keys())

        print("\nCalculating vocabulary overlaps...")
        for i, site1 in enumerate(sites):
            for site2 in sites[i+1:]:
                if site1 in self.site_vocabularies and site2 in self.site_vocabularies:
                    key = f"{site1}-{site2}"
                    overlap = self.calculate_vocabulary_overlap(site1, site2)
                    self.results['vocabulary_comparisons'][key] = overlap
                    self.log(f"{key}: Jaccard={overlap['jaccard_similarity']:.3f}, shared={overlap['shared_count']}")

    def identify_site_specific_words(self) -> dict:
        """
        Identify words that appear only at specific sites.

        These may indicate:
        - Regional administrative terms
        - Local commodity names
        - Site-specific personal names
        """
        site_specific = {}

        # Get all syllabic words from each site
        for site, vocab in self.site_vocabularies.items():
            syllabic_words = {w: c for w, c in vocab.items() if '-' in w}

            # Find words unique to this site
            unique = []
            for word, count in syllabic_words.items():
                is_unique = True
                for other_site, other_vocab in self.site_vocabularies.items():
                    if other_site != site and word in other_vocab:
                        is_unique = False
                        break

                if is_unique and count >= 2:  # At least 2 occurrences
                    unique.append({'word': word, 'count': count})

            unique.sort(key=lambda x: x['count'], reverse=True)
            site_specific[site] = {
                'count': len(unique),
                'words': unique[:30],  # Top 30
            }

        self.results['site_specific_words'] = site_specific
        return site_specific

    def identify_shared_vocabulary(self) -> dict:
        """
        Identify words shared across multiple sites.

        High-frequency shared words likely represent:
        - Core administrative vocabulary
        - Common commodity terms
        - Standardized formulas
        """
        # Count sites per word
        word_sites = defaultdict(list)

        for site, vocab in self.site_vocabularies.items():
            for word in vocab:
                if '-' in word:  # Syllabic only
                    word_sites[word].append(site)

        # Categorize by site count
        shared = {
            'all_sites': [],
            'most_sites': [],  # n-1 sites
            'multiple_sites': [],  # 2+ sites
        }

        num_sites = len(self.site_vocabularies)

        for word, sites in word_sites.items():
            site_count = len(sites)
            total_freq = sum(self.site_vocabularies[s].get(word, 0) for s in sites)

            entry = {
                'word': word,
                'sites': sites,
                'site_count': site_count,
                'total_frequency': total_freq,
            }

            if site_count == num_sites:
                shared['all_sites'].append(entry)
            elif site_count == num_sites - 1:
                shared['most_sites'].append(entry)
            elif site_count >= 2:
                shared['multiple_sites'].append(entry)

        # Sort by frequency
        for key in shared:
            shared[key].sort(key=lambda x: x['total_frequency'], reverse=True)
            shared[key] = shared[key][:30]  # Top 30

        self.results['shared_vocabulary'] = shared
        return shared

    def compare_kr_paradigm_by_site(self) -> dict:
        """
        Compare ku-ro / ki-ro usage across sites.

        Key questions:
        - Is ku-ro more common at some sites?
        - Does ki-ro have different distribution?
        - Are there site-specific K-R variants?
        """
        kr_by_site = {}

        # K-R pattern variants to search for
        kr_patterns = [
            'KU-RO', 'KI-RO',
            'KU-RA', 'KI-RA',
            'KU-RE', 'KI-RE',
            'KU-RI', 'KI-RI',
        ]

        for site, vocab in self.site_vocabularies.items():
            vocab_upper = {w.upper(): c for w, c in vocab.items()}

            site_kr = {
                'ku_ro': vocab_upper.get('KU-RO', 0),
                'ki_ro': vocab_upper.get('KI-RO', 0),
                'other_kr_forms': {},
                'kr_ratio': None,
                'total_kr': 0,
            }

            # Find other K-R forms
            for pattern in kr_patterns:
                if pattern not in ['KU-RO', 'KI-RO']:
                    count = vocab_upper.get(pattern, 0)
                    if count > 0:
                        site_kr['other_kr_forms'][pattern] = count

            site_kr['total_kr'] = site_kr['ku_ro'] + site_kr['ki_ro'] + sum(site_kr['other_kr_forms'].values())

            # Calculate ku/ki ratio
            if site_kr['ki_ro'] > 0:
                site_kr['kr_ratio'] = round(site_kr['ku_ro'] / site_kr['ki_ro'], 2)
            elif site_kr['ku_ro'] > 0:
                site_kr['kr_ratio'] = float('inf')  # Only ku-ro

            kr_by_site[site] = site_kr

        # Add comparative analysis
        analysis = {
            'by_site': kr_by_site,
            'observations': [],
        }

        # Analyze patterns
        total_ku_ro = sum(s['ku_ro'] for s in kr_by_site.values())
        total_ki_ro = sum(s['ki_ro'] for s in kr_by_site.values())

        analysis['totals'] = {
            'ku_ro': total_ku_ro,
            'ki_ro': total_ki_ro,
            'overall_ratio': round(total_ku_ro / total_ki_ro, 2) if total_ki_ro > 0 else None,
        }

        # Check for significant site variation
        for site, data in kr_by_site.items():
            if data['total_kr'] >= 5:
                if data['ki_ro'] > data['ku_ro']:
                    analysis['observations'].append({
                        'site': site,
                        'observation': f'ki-ro ({data["ki_ro"]}) more common than ku-ro ({data["ku_ro"]})',
                        'significance': 'May indicate different administrative function',
                    })
                elif data['ku_ro'] > 0 and data['ki_ro'] == 0:
                    analysis['observations'].append({
                        'site': site,
                        'observation': f'Only ku-ro found ({data["ku_ro"]}), no ki-ro',
                        'significance': 'Suggests site uses only totaling function',
                    })

        self.results['kr_paradigm_by_site'] = analysis
        return analysis

    def generate_overall_findings(self):
        """Generate summary findings from the analysis."""
        findings = {
            'standardization_level': None,
            'regional_variation': [],
            'kr_paradigm_consistency': None,
            'research_implications': [],
        }

        # Assess standardization
        overlaps = list(self.results['vocabulary_comparisons'].values())
        if overlaps:
            avg_jaccard = sum(o['jaccard_similarity'] for o in overlaps) / len(overlaps)
            if avg_jaccard > 0.3:
                findings['standardization_level'] = 'HIGH'
                findings['research_implications'].append(
                    'High vocabulary overlap suggests standardized administrative language'
                )
            elif avg_jaccard > 0.15:
                findings['standardization_level'] = 'MODERATE'
                findings['research_implications'].append(
                    'Moderate overlap indicates shared core vocabulary with regional variation'
                )
            else:
                findings['standardization_level'] = 'LOW'
                findings['research_implications'].append(
                    'Low overlap may indicate regional administrative independence or dialectal variation'
                )

        # Check K-R paradigm consistency
        kr_data = self.results.get('kr_paradigm_by_site', {}).get('by_site', {})
        if kr_data:
            ku_sites = [s for s, d in kr_data.items() if d['ku_ro'] > 0]
            ki_sites = [s for s, d in kr_data.items() if d['ki_ro'] > 0]

            if len(ku_sites) > len(ki_sites):
                findings['kr_paradigm_consistency'] = 'KU-RO dominant across sites'
            elif len(ki_sites) > len(ku_sites):
                findings['kr_paradigm_consistency'] = 'KI-RO more widespread'
            else:
                findings['kr_paradigm_consistency'] = 'KU-RO and KI-RO balanced distribution'

        # Regional variation notes
        site_specific = self.results.get('site_specific_words', {})
        for site, data in site_specific.items():
            if data['count'] > 10:
                findings['regional_variation'].append({
                    'site': site,
                    'unique_words': data['count'],
                    'note': f'{SITE_FULL_NAMES.get(site, site)} has {data["count"]} unique syllabic words',
                })

        self.results['overall_findings'] = findings

    def run_analysis(self, sites: List[str] = None):
        """Run complete regional analysis."""
        if sites is None:
            sites = ['HT', 'KH', 'ZA', 'PH', 'KN', 'MA', 'TY']

        self.extract_all_site_vocabularies(sites)
        self.calculate_all_overlaps(sites)
        self.identify_site_specific_words()
        self.identify_shared_vocabulary()
        self.compare_kr_paradigm_by_site()
        self.generate_overall_findings()

        self.results['metadata']['generated'] = datetime.now().isoformat()
        self.results['metadata']['sites_analyzed'] = sites

        return self.results

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        # Handle infinity values for JSON serialization
        def clean_for_json(obj):
            if isinstance(obj, dict):
                return {k: clean_for_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_for_json(v) for v in obj]
            elif isinstance(obj, float) and (obj == float('inf') or obj == float('-inf')):
                return "infinity"
            return obj

        clean_results = clean_for_json(self.results)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(clean_results, f, ensure_ascii=False, indent=2)

        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 70)
        print("REGIONAL VARIATION ANALYSIS SUMMARY")
        print("First Principle #6: Cross-Corpus Consistency")
        print("=" * 70)

        # Site summaries
        print("\nSite Vocabularies:")
        for site, summary in self.results['site_summaries'].items():
            name = summary['name']
            words = summary['unique_words']
            syllabic = summary['syllabic_words']
            print(f"  {site} ({name}): {words} unique words ({syllabic} syllabic)")

        # Vocabulary overlaps
        print("\nVocabulary Overlap (Jaccard similarity):")
        for key, data in sorted(self.results['vocabulary_comparisons'].items(),
                                key=lambda x: x[1]['jaccard_similarity'], reverse=True):
            print(f"  {key}: {data['jaccard_similarity']:.3f} ({data['shared_count']} shared words)")

        # K-R paradigm
        print("\nK-R Paradigm by Site:")
        kr_data = self.results.get('kr_paradigm_by_site', {}).get('by_site', {})
        for site, data in kr_data.items():
            if data['total_kr'] > 0:
                print(f"  {site}: ku-ro={data['ku_ro']}, ki-ro={data['ki_ro']}, ratio={data['kr_ratio']}")

        # Shared vocabulary
        shared = self.results.get('shared_vocabulary', {})
        all_sites = shared.get('all_sites', [])
        if all_sites:
            print(f"\nWords found at ALL sites ({len(all_sites)}):")
            for item in all_sites[:10]:
                print(f"  {item['word']} (freq={item['total_frequency']})")

        # Overall findings
        findings = self.results.get('overall_findings', {})
        print("\nOverall Findings:")
        print(f"  Standardization level: {findings.get('standardization_level', 'Unknown')}")
        print(f"  K-R paradigm: {findings.get('kr_paradigm_consistency', 'Unknown')}")

        for impl in findings.get('research_implications', []):
            print(f"  → {impl}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze regional variation in Linear A vocabulary"
    )
    parser.add_argument(
        '--sites', '-s',
        type=str,
        help='Comma-separated list of site codes (e.g., HT,KH,ZA)'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Analyze all major sites'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/regional_analysis.json',
        help='Output path for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A REGIONAL VARIATION ANALYZER")
    print("=" * 70)
    print("Implementing First Principle #6: Cross-Corpus Consistency")

    analyzer = RegionalAnalyzer(verbose=args.verbose)

    if not analyzer.load_corpus():
        return 1

    # Determine sites to analyze
    if args.sites:
        sites = [s.strip().upper() for s in args.sites.split(',')]
    elif args.all:
        sites = ['HT', 'KH', 'ZA', 'PH', 'KN', 'MA', 'TY', 'PK']
    else:
        sites = ['HT', 'KH', 'ZA', 'PH']  # Default: major 4

    # Run analysis
    analyzer.run_analysis(sites)

    # Save results
    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)

    # Print summary
    analyzer.print_summary()

    return 0


if __name__ == '__main__':
    sys.exit(main())
