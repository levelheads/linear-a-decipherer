#!/usr/bin/env python3
"""
K-R Paradigm Validator for Linear A

Validates the K-R paradigm (ku-ro / ki-ro) corpus-wide, testing:
1. Distribution patterns of all K-V-R-V forms
2. Context mapping (what precedes/follows each form)
3. Complementary distribution hypothesis
4. Functional analysis (totaling vs. deficit)

Key research question: Are ku-ro and ki-ro complementary or synonymous?

Expected findings (based on prior analysis):
- KU-RO: ~37 occurrences, appears at totaling positions
- KI-RO: ~16 occurrences, may indicate deficit/subtraction

Usage:
    python tools/kr_paradigm_validator.py [--all] [--output FILE]

Examples:
    python tools/kr_paradigm_validator.py --all
    python tools/kr_paradigm_validator.py --verbose --output data/kr_paradigm_report.json

Attribution:
    Part of Linear A Decipherment Project
    Implements First Principle #6: Cross-Corpus Consistency
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Optional


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# All K-V-R-V patterns to analyze
KR_PATTERNS = {
    # Primary patterns (K-R core)
    'KU-RO': {'expected': 'total', 'confidence': 'HIGH'},
    'KI-RO': {'expected': 'deficit/subtraction', 'confidence': 'MEDIUM'},

    # Extended vowel patterns
    'KU-RA': {'expected': 'variant?', 'confidence': 'LOW'},
    'KI-RA': {'expected': 'variant?', 'confidence': 'LOW'},
    'KU-RE': {'expected': 'variant?', 'confidence': 'LOW'},
    'KI-RE': {'expected': 'variant?', 'confidence': 'LOW'},
    'KU-RI': {'expected': 'variant?', 'confidence': 'LOW'},
    'KI-RI': {'expected': 'variant?', 'confidence': 'LOW'},

    # Final vowel variants
    'KU-RU': {'expected': 'variant?', 'confidence': 'LOW'},
    'KI-RU': {'expected': 'variant?', 'confidence': 'LOW'},
}

# Context indicators
LOGOGRAMS = ['GRA', 'VIN', 'OLE', 'OLIV', 'CYP', 'AROM', 'TELA', 'LANA', 'BOS', 'OVIS', 'CAP', 'SUS']
NUMERALS = re.compile(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈₉]+$')
FRACTIONS = re.compile(r'^[¹²³⁴⁵⁶⁷⁸⁹⁰⁄₀₁₂₃₄₅₆₇₈₉]+$|^≈')


class KRParadigmValidator:
    """
    Validates K-R paradigm forms across the Linear A corpus.

    For each K-R form, maps:
    - All occurrences with inscription references
    - Preceding and following context
    - Position in inscription (initial, medial, final)
    - Associated logograms and numerals
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.kr_occurrences = []
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'K-R Paradigm Validation',
                'principle': 'First Principle #6: Cross-Corpus Consistency',
            },
            'summary': {},
            'form_counts': {},
            'occurrences': [],
            'context_analysis': {},
            'complementary_distribution': {},
            'functional_analysis': {},
            'paradigm_conclusions': {},
        }

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
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _is_kr_form(self, word: str) -> Optional[str]:
        """Check if word matches a K-R pattern. Returns matched pattern or None."""
        word_upper = word.upper()
        for pattern in KR_PATTERNS:
            if word_upper == pattern:
                return pattern
            # Also check with subscripts
            pattern_normalized = word_upper.replace('₂', '').replace('₃', '').replace('₄', '')
            if pattern_normalized == pattern:
                return pattern
        return None

    def _classify_word(self, word: str) -> str:
        """Classify a word by type."""
        if not word:
            return 'EMPTY'
        word_upper = word.upper()

        # Check for logograms
        for logo in LOGOGRAMS:
            if logo in word_upper:
                return 'LOGOGRAM'

        # Check for numerals
        if NUMERALS.match(word) or FRACTIONS.match(word):
            return 'NUMERAL'

        # Check for K-R form
        if self._is_kr_form(word):
            return 'KR_FORM'

        # Check for syllabic word
        if '-' in word:
            return 'SYLLABIC'

        return 'OTHER'

    def find_all_kr_forms(self) -> List[dict]:
        """
        Find all K-R forms in the corpus with full context.

        Returns list of occurrences with:
        - inscription_id
        - word (exact form)
        - pattern (matched K-R pattern)
        - position (index in inscription)
        - preceding_context (up to 3 words before)
        - following_context (up to 3 words after)
        - position_type (INITIAL, MEDIAL, FINAL)
        """
        occurrences = []

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            # Filter out empty/separator tokens but keep position info
            valid_words = [(i, w) for i, w in enumerate(words)
                           if w and w not in ['\n', '𐄁', '', '—', '≈', '𐝫']]

            for pos, (orig_idx, word) in enumerate(valid_words):
                pattern = self._is_kr_form(word)
                if pattern:
                    # Get context
                    context_before = []
                    context_after = []

                    for j in range(max(0, pos-3), pos):
                        context_before.append(valid_words[j][1])

                    for j in range(pos+1, min(len(valid_words), pos+4)):
                        context_after.append(valid_words[j][1])

                    # Determine position type
                    if pos == 0:
                        position_type = 'INITIAL'
                    elif pos == len(valid_words) - 1:
                        position_type = 'FINAL'
                    else:
                        position_type = 'MEDIAL'

                    # Classify immediate context
                    prev_type = self._classify_word(context_before[-1]) if context_before else 'NONE'
                    next_type = self._classify_word(context_after[0]) if context_after else 'NONE'

                    occurrence = {
                        'inscription_id': insc_id,
                        'word': word,
                        'pattern': pattern,
                        'position_in_inscription': pos,
                        'total_words_in_inscription': len(valid_words),
                        'position_type': position_type,
                        'preceding_context': context_before,
                        'following_context': context_after,
                        'prev_word_type': prev_type,
                        'next_word_type': next_type,
                    }

                    occurrences.append(occurrence)
                    self.log(f"Found {pattern} in {insc_id} at position {pos}")

        self.kr_occurrences = occurrences
        return occurrences

    def map_kr_contexts(self) -> dict:
        """
        Map all K-R contexts to identify patterns.

        Returns analysis of:
        - What typically precedes each K-R form
        - What typically follows each K-R form
        - Common sequences
        """
        context_analysis = {
            'by_pattern': {},
            'preceding_word_types': Counter(),
            'following_word_types': Counter(),
            'common_sequences': [],
        }

        pattern_contexts = defaultdict(lambda: {
            'preceding_types': Counter(),
            'following_types': Counter(),
            'preceding_words': Counter(),
            'following_words': Counter(),
            'position_types': Counter(),
        })

        for occ in self.kr_occurrences:
            pattern = occ['pattern']
            pc = pattern_contexts[pattern]

            pc['preceding_types'][occ['prev_word_type']] += 1
            pc['following_types'][occ['next_word_type']] += 1
            pc['position_types'][occ['position_type']] += 1

            # Track actual words
            if occ['preceding_context']:
                pc['preceding_words'][occ['preceding_context'][-1]] += 1
            if occ['following_context']:
                pc['following_words'][occ['following_context'][0]] += 1

            # Global tracking
            context_analysis['preceding_word_types'][occ['prev_word_type']] += 1
            context_analysis['following_word_types'][occ['next_word_type']] += 1

        # Summarize by pattern
        for pattern, pc in pattern_contexts.items():
            context_analysis['by_pattern'][pattern] = {
                'total_occurrences': sum(pc['position_types'].values()),
                'preceding_types': dict(pc['preceding_types'].most_common(5)),
                'following_types': dict(pc['following_types'].most_common(5)),
                'preceding_words': dict(pc['preceding_words'].most_common(10)),
                'following_words': dict(pc['following_words'].most_common(10)),
                'position_distribution': dict(pc['position_types']),
            }

        # Find common sequences
        sequence_counts = Counter()
        for occ in self.kr_occurrences:
            pattern = occ['pattern']
            if occ['preceding_context']:
                seq = f"{occ['preceding_context'][-1]} → {pattern}"
                sequence_counts[seq] += 1
            if occ['following_context']:
                seq = f"{pattern} → {occ['following_context'][0]}"
                sequence_counts[seq] += 1

        context_analysis['common_sequences'] = [
            {'sequence': seq, 'count': count}
            for seq, count in sequence_counts.most_common(20)
        ]

        self.results['context_analysis'] = context_analysis
        return context_analysis

    def test_complementary_distribution(self) -> dict:
        """
        Test whether ku-ro and ki-ro are in complementary distribution.

        Complementary distribution would mean:
        - They don't appear in the same contexts
        - Each has exclusive environments

        Returns analysis with:
        - Shared contexts (counter-evidence)
        - Exclusive contexts (supporting evidence)
        - Statistical test result
        """
        cd_analysis = {
            'hypothesis': 'KU-RO and KI-RO are in complementary distribution',
            'shared_contexts': [],
            'ku_ro_exclusive': [],
            'ki_ro_exclusive': [],
            'same_inscription_pairs': [],
            'verdict': None,
            'confidence': None,
        }

        # Group occurrences by pattern
        ku_ro_contexts = set()
        ki_ro_contexts = set()
        ku_ro_inscriptions = set()
        ki_ro_inscriptions = set()

        for occ in self.kr_occurrences:
            pattern = occ['pattern']
            # Context key: position type + prev type + next type
            context_key = f"{occ['position_type']}_{occ['prev_word_type']}_{occ['next_word_type']}"

            if pattern == 'KU-RO':
                ku_ro_contexts.add(context_key)
                ku_ro_inscriptions.add(occ['inscription_id'])
            elif pattern == 'KI-RO':
                ki_ro_contexts.add(context_key)
                ki_ro_inscriptions.add(occ['inscription_id'])

        # Find shared contexts
        shared = ku_ro_contexts & ki_ro_contexts
        cd_analysis['shared_contexts'] = list(shared)
        cd_analysis['ku_ro_exclusive'] = list(ku_ro_contexts - ki_ro_contexts)
        cd_analysis['ki_ro_exclusive'] = list(ki_ro_contexts - ku_ro_contexts)

        # Check for same-inscription co-occurrence
        same_insc = ku_ro_inscriptions & ki_ro_inscriptions
        if same_insc:
            for insc_id in same_insc:
                ku_pos = [o['position_in_inscription'] for o in self.kr_occurrences
                          if o['inscription_id'] == insc_id and o['pattern'] == 'KU-RO']
                ki_pos = [o['position_in_inscription'] for o in self.kr_occurrences
                          if o['inscription_id'] == insc_id and o['pattern'] == 'KI-RO']
                cd_analysis['same_inscription_pairs'].append({
                    'inscription_id': insc_id,
                    'ku_ro_positions': ku_pos,
                    'ki_ro_positions': ki_pos,
                })

        # Determine verdict
        if len(shared) == 0 and len(same_insc) == 0:
            cd_analysis['verdict'] = 'SUPPORTED'
            cd_analysis['confidence'] = 'HIGH'
            cd_analysis['interpretation'] = (
                'KU-RO and KI-RO appear in non-overlapping contexts, '
                'supporting complementary distribution hypothesis'
            )
        elif len(shared) <= 2 and len(same_insc) <= 2:
            cd_analysis['verdict'] = 'PARTIALLY SUPPORTED'
            cd_analysis['confidence'] = 'MEDIUM'
            cd_analysis['interpretation'] = (
                'Minimal context overlap exists, but patterns are largely distinct'
            )
        else:
            cd_analysis['verdict'] = 'NOT SUPPORTED'
            cd_analysis['confidence'] = 'HIGH'
            cd_analysis['interpretation'] = (
                'Significant context overlap suggests ku-ro and ki-ro may be synonymous '
                'or have overlapping functions'
            )

        self.results['complementary_distribution'] = cd_analysis
        return cd_analysis

    def analyze_functions(self) -> dict:
        """
        Analyze functional patterns of K-R forms.

        Tests:
        - Does KU-RO consistently appear at totaling positions?
        - Does KI-RO appear in deficit contexts?
        - Position relative to numerals and logograms
        """
        func_analysis = {
            'ku_ro': {
                'total_count': 0,
                'at_end_of_section': 0,
                'followed_by_numeral': 0,
                'preceded_by_logogram': 0,
                'function_hypothesis': 'TOTAL (sum of previous entries)',
                'evidence_strength': None,
            },
            'ki_ro': {
                'total_count': 0,
                'at_end_of_section': 0,
                'followed_by_numeral': 0,
                'preceded_by_logogram': 0,
                'function_hypothesis': 'DEFICIT (subtraction from total)',
                'evidence_strength': None,
            },
            'position_analysis': {},
            'conclusions': [],
        }

        for occ in self.kr_occurrences:
            pattern = occ['pattern']
            if pattern not in ['KU-RO', 'KI-RO']:
                continue

            key = 'ku_ro' if pattern == 'KU-RO' else 'ki_ro'
            func_analysis[key]['total_count'] += 1

            # Check if at end or near end
            if occ['position_type'] == 'FINAL':
                func_analysis[key]['at_end_of_section'] += 1
            elif occ['position_in_inscription'] >= occ['total_words_in_inscription'] - 3:
                func_analysis[key]['at_end_of_section'] += 1

            # Check context types
            if occ['next_word_type'] == 'NUMERAL':
                func_analysis[key]['followed_by_numeral'] += 1
            if occ['prev_word_type'] == 'LOGOGRAM':
                func_analysis[key]['preceded_by_logogram'] += 1

        # Calculate evidence strength
        for key in ['ku_ro', 'ki_ro']:
            data = func_analysis[key]
            if data['total_count'] > 0:
                end_ratio = data['at_end_of_section'] / data['total_count']
                numeral_ratio = data['followed_by_numeral'] / data['total_count']

                if end_ratio > 0.7:
                    data['evidence_strength'] = 'STRONG'
                elif end_ratio > 0.4:
                    data['evidence_strength'] = 'MODERATE'
                else:
                    data['evidence_strength'] = 'WEAK'

                data['end_ratio'] = round(end_ratio, 3)
                data['numeral_ratio'] = round(numeral_ratio, 3)

        # Generate conclusions
        ku = func_analysis['ku_ro']
        ki = func_analysis['ki_ro']

        if ku['total_count'] > ki['total_count'] * 2:
            func_analysis['conclusions'].append(
                f"KU-RO is dominant ({ku['total_count']} vs {ki['total_count']}), "
                "suggesting it's the primary administrative marker"
            )

        if ku.get('end_ratio', 0) > 0.5:
            func_analysis['conclusions'].append(
                f"KU-RO frequently appears at section end ({ku.get('end_ratio', 0)*100:.0f}%), "
                "consistent with 'total' function"
            )

        if ki['total_count'] > 0 and ki.get('numeral_ratio', 0) > ku.get('numeral_ratio', 0):
            func_analysis['conclusions'].append(
                "KI-RO more often followed by numerals, possibly indicating specific amounts"
            )

        self.results['functional_analysis'] = func_analysis
        return func_analysis

    def generate_paradigm_report(self) -> dict:
        """Generate comprehensive paradigm conclusions."""
        conclusions = {
            'primary_forms': {
                'KU-RO': {
                    'count': 0,
                    'function': 'TOTAL',
                    'confidence': 'HIGH',
                    'semitic_cognate': '*kull "all, totality"',
                    'greek_comparison': 'Not matching Greek τόσος (to-so)',
                },
                'KI-RO': {
                    'count': 0,
                    'function': 'DEFICIT',
                    'confidence': 'MEDIUM',
                    'semitic_cognate': '*gara "to diminish"',
                    'greek_comparison': 'Possibly related to χρέος (debt)?',
                },
            },
            'paradigm_structure': None,
            'morphological_analysis': {},
            'research_implications': [],
        }

        # Count forms
        form_counts = Counter()
        for occ in self.kr_occurrences:
            form_counts[occ['pattern']] += 1

        conclusions['primary_forms']['KU-RO']['count'] = form_counts.get('KU-RO', 0)
        conclusions['primary_forms']['KI-RO']['count'] = form_counts.get('KI-RO', 0)

        # Store all form counts
        self.results['form_counts'] = dict(form_counts)

        # Determine paradigm structure
        cd = self.results.get('complementary_distribution', {})
        if cd.get('verdict') == 'SUPPORTED':
            conclusions['paradigm_structure'] = 'COMPLEMENTARY'
            conclusions['research_implications'].append(
                'KU-RO and KI-RO form a complementary pair, likely with opposite functions'
            )
        elif cd.get('verdict') == 'PARTIALLY SUPPORTED':
            conclusions['paradigm_structure'] = 'MOSTLY_COMPLEMENTARY'
            conclusions['research_implications'].append(
                'KU-RO and KI-RO are largely complementary with some functional overlap'
            )
        else:
            conclusions['paradigm_structure'] = 'OVERLAPPING'
            conclusions['research_implications'].append(
                'KU-RO and KI-RO may share contexts, suggesting synonymy or gradation'
            )

        # Morphological analysis
        conclusions['morphological_analysis'] = {
            'initial_contrast': 'KU- vs KI- (back vowel vs front vowel)',
            'shared_element': '-RO (possibly noun-forming suffix)',
            'pattern': 'CV-CV (typical Linear A word structure)',
            'vowel_harmony': 'Not clear (mixed vowels common in corpus)',
        }

        # Add implications
        func = self.results.get('functional_analysis', {})
        if func.get('ku_ro', {}).get('evidence_strength') == 'STRONG':
            conclusions['research_implications'].append(
                'Strong evidence for KU-RO as totaling marker supports Semitic *kull cognate'
            )

        if len(cd.get('same_inscription_pairs', [])) > 0:
            conclusions['research_implications'].append(
                f'{len(cd["same_inscription_pairs"])} inscriptions contain both KU-RO and KI-RO, '
                'providing direct evidence of their functional relationship'
            )

        self.results['paradigm_conclusions'] = conclusions
        return conclusions

    def run_validation(self) -> dict:
        """Run complete K-R paradigm validation."""
        print("\nFinding all K-R forms...")
        self.find_all_kr_forms()

        # Summary
        self.results['summary'] = {
            'total_kr_occurrences': len(self.kr_occurrences),
            'unique_patterns_found': len(set(o['pattern'] for o in self.kr_occurrences)),
            'inscriptions_with_kr': len(set(o['inscription_id'] for o in self.kr_occurrences)),
        }
        print(f"Found {len(self.kr_occurrences)} K-R form occurrences")

        print("Mapping contexts...")
        self.map_kr_contexts()

        print("Testing complementary distribution...")
        self.test_complementary_distribution()

        print("Analyzing functions...")
        self.analyze_functions()

        print("Generating paradigm report...")
        self.generate_paradigm_report()

        # Store occurrences (simplified for JSON)
        self.results['occurrences'] = [
            {
                'inscription_id': o['inscription_id'],
                'pattern': o['pattern'],
                'position': o['position_in_inscription'],
                'position_type': o['position_type'],
                'prev_type': o['prev_word_type'],
                'next_type': o['next_word_type'],
                'preceding_words': o['preceding_context'],
                'following_words': o['following_context'],
            }
            for o in self.kr_occurrences
        ]

        self.results['metadata']['generated'] = datetime.now().isoformat()

        return self.results

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 70)
        print("K-R PARADIGM VALIDATION SUMMARY")
        print("First Principle #6: Cross-Corpus Consistency")
        print("=" * 70)

        # Form counts
        print("\nK-R Form Counts:")
        for pattern, count in sorted(self.results['form_counts'].items(),
                                     key=lambda x: x[1], reverse=True):
            print(f"  {pattern}: {count}")

        # Summary stats
        summary = self.results.get('summary', {})
        print(f"\nTotal K-R occurrences: {summary.get('total_kr_occurrences', 0)}")
        print(f"Inscriptions with K-R forms: {summary.get('inscriptions_with_kr', 0)}")

        # Complementary distribution
        cd = self.results.get('complementary_distribution', {})
        print("\nComplementary Distribution Test:")
        print(f"  Verdict: {cd.get('verdict', 'Unknown')}")
        print(f"  Confidence: {cd.get('confidence', 'Unknown')}")
        if cd.get('interpretation'):
            print(f"  → {cd['interpretation']}")

        # Same inscription pairs
        pairs = cd.get('same_inscription_pairs', [])
        if pairs:
            print(f"\nInscriptions with BOTH KU-RO and KI-RO ({len(pairs)}):")
            for pair in pairs[:5]:
                print(f"  {pair['inscription_id']}: "
                      f"KU-RO at {pair['ku_ro_positions']}, "
                      f"KI-RO at {pair['ki_ro_positions']}")

        # Functional analysis
        func = self.results.get('functional_analysis', {})
        print("\nFunctional Analysis:")
        for key in ['ku_ro', 'ki_ro']:
            data = func.get(key, {})
            if data.get('total_count', 0) > 0:
                pattern = 'KU-RO' if key == 'ku_ro' else 'KI-RO'
                print(f"  {pattern}:")
                print(f"    Function: {data.get('function_hypothesis', 'Unknown')}")
                print(f"    At section end: {data.get('end_ratio', 0)*100:.1f}%")
                print(f"    Evidence strength: {data.get('evidence_strength', 'Unknown')}")

        # Conclusions
        conclusions = self.results.get('paradigm_conclusions', {})
        print(f"\nParadigm Structure: {conclusions.get('paradigm_structure', 'Unknown')}")

        print("\nResearch Implications:")
        for impl in conclusions.get('research_implications', []):
            print(f"  → {impl}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate K-R paradigm across Linear A corpus"
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Run complete validation'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/kr_paradigm_report.json',
        help='Output path for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A K-R PARADIGM VALIDATOR")
    print("=" * 70)
    print("Validating KU-RO / KI-RO paradigm corpus-wide")

    validator = KRParadigmValidator(verbose=args.verbose)

    if not validator.load_corpus():
        return 1

    # Run validation
    validator.run_validation()

    # Save results
    output_path = PROJECT_ROOT / args.output
    validator.save_results(output_path)

    # Print summary
    validator.print_summary()

    return 0


if __name__ == '__main__':
    sys.exit(main())
