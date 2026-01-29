#!/usr/bin/env python3
"""
Contextual Analyzer for Linear A

Advanced pattern detection through contextual analysis:
1. Conditional frequencies: P(word | context type)
2. Formulaic sequence detection
3. Document structure mapping (headers, entries, totals)
4. Co-occurrence statistics

This tool extends corpus_lookup.py with statistical context analysis.

Usage:
    python tools/contextual_analyzer.py [--analyze TYPE] [--output FILE]

Examples:
    python tools/contextual_analyzer.py --analyze formulas
    python tools/contextual_analyzer.py --analyze structure
    python tools/contextual_analyzer.py --all --output data/contextual_analysis.json

Attribution:
    Part of Linear A Decipherment Project
    Supports First Principle #6 (Cross-Corpus Consistency)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from itertools import combinations

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


class ContextualAnalyzer:
    """
    Contextual analysis of Linear A corpus patterns.

    Provides:
    - Conditional frequency analysis (word given context)
    - Formulaic sequence detection
    - Document structure templates
    - Co-occurrence statistics
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'Contextual Pattern Analysis',
            },
            'conditional_frequencies': {},
            'formulas': {},
            'document_structures': {},
            'cooccurrence': {},
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

    def _is_numeral(self, word: str) -> bool:
        """Check if word is a numeral."""
        if not word:
            return False
        return bool(re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|≈J]+$', word))

    def _is_logogram(self, word: str) -> bool:
        """Check if word is a logogram (all caps, no hyphens)."""
        if not word or '-' in word:
            return False
        return bool(re.match(r'^[A-Z*\d\[\]]+$', word))

    def _is_syllabic(self, word: str) -> bool:
        """Check if word is syllabic (contains hyphens)."""
        return '-' in word and not self._is_numeral(word)

    def _extract_document_elements(self, inscription_id: str) -> dict:
        """Extract structural elements from an inscription."""
        data = self.corpus['inscriptions'].get(inscription_id, {})
        if '_parse_error' in data:
            return None

        words = data.get('transliteratedWords', [])
        if not words:
            return None

        elements = {
            'inscription_id': inscription_id,
            'site': data.get('site', ''),
            'lines': [],
            'syllabic_words': [],
            'logograms': [],
            'numerals': [],
            'has_total': False,
            'total_word': None,
            'structure_type': 'unknown',
        }

        current_line = []
        line_num = 1

        for word in words:
            if word == '\n':
                if current_line:
                    elements['lines'].append({
                        'line_num': line_num,
                        'words': current_line,
                    })
                    current_line = []
                    line_num += 1
                continue

            if not word or word in ['𐄁', '', '—', '≈']:
                continue

            current_line.append(word)

            if self._is_numeral(word):
                elements['numerals'].append({'word': word, 'line': line_num})
            elif self._is_logogram(word):
                elements['logograms'].append({'word': word, 'line': line_num})
            elif self._is_syllabic(word):
                elements['syllabic_words'].append({'word': word, 'line': line_num})

                # Check for totaling words
                word_upper = word.upper()
                if word_upper in ['KU-RO', 'PO-TO-KU-RO', 'KI-RO']:
                    elements['has_total'] = True
                    elements['total_word'] = word

        # Add final line
        if current_line:
            elements['lines'].append({
                'line_num': line_num,
                'words': current_line,
            })

        # Determine structure type
        if elements['has_total']:
            elements['structure_type'] = 'commodity_list'
        elif len(elements['logograms']) > 5:
            elements['structure_type'] = 'logographic_heavy'
        elif len(elements['numerals']) > 3:
            elements['structure_type'] = 'administrative'
        else:
            elements['structure_type'] = 'mixed'

        return elements

    # =========================================================================
    # CONDITIONAL FREQUENCY ANALYSIS
    # =========================================================================

    def analyze_conditional_frequencies(self) -> dict:
        """
        Calculate P(word | context) for various contexts.

        Contexts include:
        - Before logogram
        - After logogram
        - Before numeral
        - Line-initial
        - Line-final
        - Before ku-ro (total)
        """
        print("Analyzing conditional frequencies...")

        contexts = {
            'before_logogram': Counter(),
            'after_logogram': Counter(),
            'before_numeral': Counter(),
            'after_numeral': Counter(),
            'line_initial': Counter(),
            'line_final': Counter(),
            'before_total': Counter(),  # Words appearing before ku-ro
            'after_total': Counter(),   # Words appearing after ku-ro
            'pre_logogram_pairs': Counter(),  # (word, logogram) pairs
        }

        total_counts = Counter()

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            line_words = []

            for i, word in enumerate(words):
                if word == '\n':
                    # Process line
                    if line_words:
                        # Line initial
                        if self._is_syllabic(line_words[0]):
                            contexts['line_initial'][line_words[0].upper()] += 1

                        # Line final (before newline, excluding numerals)
                        for w in reversed(line_words):
                            if self._is_syllabic(w):
                                contexts['line_final'][w.upper()] += 1
                                break
                    line_words = []
                    continue

                if not word or word in ['𐄁', '', '—', '≈']:
                    continue

                line_words.append(word)
                word_upper = word.upper()

                if self._is_syllabic(word):
                    total_counts[word_upper] += 1

                # Check context relationships
                if i > 0:
                    prev = words[i-1]
                    if self._is_logogram(prev) and self._is_syllabic(word):
                        contexts['after_logogram'][word_upper] += 1
                    if self._is_numeral(prev) and self._is_syllabic(word):
                        contexts['after_numeral'][word_upper] += 1
                    if prev.upper() in ['KU-RO', 'PO-TO-KU-RO'] and self._is_syllabic(word):
                        contexts['after_total'][word_upper] += 1

                if i < len(words) - 1:
                    next_word = words[i+1]
                    if self._is_logogram(next_word) and self._is_syllabic(word):
                        contexts['before_logogram'][word_upper] += 1
                        # Track the pair
                        contexts['pre_logogram_pairs'][(word_upper, next_word)] += 1
                    if self._is_numeral(next_word) and self._is_syllabic(word):
                        contexts['before_numeral'][word_upper] += 1
                    if next_word.upper() in ['KU-RO', 'PO-TO-KU-RO'] and self._is_syllabic(word):
                        contexts['before_total'][word_upper] += 1

        # Calculate conditional probabilities
        results = {}
        for context_name, counter in contexts.items():
            total = sum(counter.values())
            if total == 0:
                continue

            top_items = counter.most_common(30)

            if context_name == 'pre_logogram_pairs':
                # Format pairs nicely
                results[context_name] = {
                    'total_count': total,
                    'top_pairs': [
                        {
                            'word': pair[0],
                            'logogram': pair[1],
                            'count': count,
                            'frequency': count / total,
                        }
                        for pair, count in top_items
                    ]
                }
            else:
                results[context_name] = {
                    'total_count': total,
                    'top_words': [
                        {
                            'word': word,
                            'count': count,
                            'frequency': count / total,
                            'overall_frequency': total_counts.get(word, 0) / sum(total_counts.values())
                                                 if total_counts else 0,
                        }
                        for word, count in top_items
                    ]
                }

        self.results['conditional_frequencies'] = results
        return results

    # =========================================================================
    # FORMULAIC SEQUENCE DETECTION
    # =========================================================================

    def detect_formulas(self, min_length: int = 2, min_occurrences: int = 3) -> dict:
        """
        Detect recurring multi-word sequences (formulas).

        Parameters:
            min_length: Minimum number of words in sequence
            min_occurrences: Minimum times sequence must appear
        """
        print(f"Detecting formulas (min_length={min_length}, min_occurrences={min_occurrences})...")

        # Extract all sequences
        sequence_counts = defaultdict(lambda: {'count': 0, 'locations': []})

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])

            # Filter to syllabic words and logograms
            filtered_words = []
            positions = []
            for i, word in enumerate(words):
                if word == '\n' or not word or word in ['𐄁', '', '—', '≈']:
                    continue
                if self._is_numeral(word):
                    continue
                filtered_words.append(word.upper())
                positions.append(i)

            # Generate all subsequences
            for length in range(min_length, min(len(filtered_words) + 1, 7)):  # Max 6 words
                for start in range(len(filtered_words) - length + 1):
                    seq = tuple(filtered_words[start:start + length])
                    sequence_counts[seq]['count'] += 1
                    sequence_counts[seq]['locations'].append({
                        'inscription': insc_id,
                        'position': positions[start] if start < len(positions) else 0,
                    })

        # Filter by minimum occurrences
        formulas = {}
        for seq, data in sequence_counts.items():
            if data['count'] >= min_occurrences:
                seq_str = ' '.join(seq)
                formulas[seq_str] = {
                    'sequence': list(seq),
                    'length': len(seq),
                    'occurrences': data['count'],
                    'locations': data['locations'][:10],  # Limit for output size
                    'is_libation_related': self._is_libation_formula(seq),
                }

        # Sort by occurrences
        sorted_formulas = dict(
            sorted(formulas.items(), key=lambda x: (-x[1]['occurrences'], -x[1]['length']))
        )

        # Group by length
        by_length = defaultdict(list)
        for formula, data in sorted_formulas.items():
            by_length[data['length']].append({
                'formula': formula,
                **data
            })

        results = {
            'total_formulas_found': len(sorted_formulas),
            'by_length': {str(k): v for k, v in sorted(by_length.items())},
            'top_formulas': [
                {'formula': k, **v}
                for k, v in list(sorted_formulas.items())[:30]
            ],
        }

        self.results['formulas'] = results
        return results

    def _is_libation_formula(self, sequence: tuple) -> bool:
        """Check if sequence matches known libation formula patterns."""
        libation_words = {'A-TA-I', 'JA-SA-SA-RA-ME', 'U-NA-KA-NA-SI',
                         'I-PI-NA-MA', 'SI-RU-TE', '*301', 'WA-JA'}
        return any(word in libation_words for word in sequence)

    # =========================================================================
    # DOCUMENT STRUCTURE ANALYSIS
    # =========================================================================

    def analyze_document_structures(self) -> dict:
        """
        Map document structure templates.

        Identifies common document patterns:
        - Commodity lists (header + entries + total)
        - Personnel lists
        - Religious texts
        """
        print("Analyzing document structures...")

        structures = {
            'commodity_list': [],
            'personnel_list': [],
            'religious': [],
            'administrative': [],
            'fragment': [],
            'unknown': [],
        }

        structure_stats = Counter()

        for insc_id in self.corpus['inscriptions']:
            elements = self._extract_document_elements(insc_id)
            if not elements:
                continue

            structure_type = elements['structure_type']
            structure_stats[structure_type] += 1

            # Classify more specifically
            if elements['has_total']:
                structures['commodity_list'].append({
                    'inscription': insc_id,
                    'total_word': elements['total_word'],
                    'line_count': len(elements['lines']),
                    'logogram_count': len(elements['logograms']),
                    'numeral_count': len(elements['numerals']),
                })
            elif self._is_religious_text(elements):
                structures['religious'].append({
                    'inscription': insc_id,
                    'line_count': len(elements['lines']),
                    'syllabic_count': len(elements['syllabic_words']),
                })
            elif len(elements['lines']) <= 2 and len(elements['syllabic_words']) < 5:
                structures['fragment'].append({
                    'inscription': insc_id,
                    'word_count': len(elements['syllabic_words']) + len(elements['logograms']),
                })
            else:
                structures['administrative'].append({
                    'inscription': insc_id,
                    'structure': structure_type,
                })

        # Calculate template patterns for commodity lists
        commodity_templates = self._extract_commodity_templates(structures['commodity_list'])

        results = {
            'structure_counts': dict(structure_stats),
            'commodity_lists': {
                'count': len(structures['commodity_list']),
                'templates': commodity_templates,
                'examples': structures['commodity_list'][:10],
            },
            'religious_texts': {
                'count': len(structures['religious']),
                'examples': structures['religious'][:10],
            },
            'fragments': {
                'count': len(structures['fragment']),
            },
            'administrative': {
                'count': len(structures['administrative']),
                'examples': structures['administrative'][:10],
            },
        }

        self.results['document_structures'] = results
        return results

    def _is_religious_text(self, elements: dict) -> bool:
        """Check if document appears to be religious text."""
        # Check for libation formula words
        libation_markers = {'A-TA-I', 'JA-SA-SA-RA-ME', 'U-NA-KA-NA-SI'}
        syllabic_upper = [w['word'].upper() for w in elements['syllabic_words']]

        if any(marker in syllabic_upper for marker in libation_markers):
            return True

        # Check site (peak sanctuaries, caves)
        religious_sites = {'IO', 'PS', 'SY', 'PK'}
        site_code = self._extract_site_code(elements['inscription_id'])
        if site_code in religious_sites:
            return True

        # Check support type (Za = stone vessels)
        if 'Za' in elements['inscription_id']:
            return True

        return False

    def _extract_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        match = re.match(r'^([A-Z]+)', inscription_id)
        return match.group(1) if match else ''

    def _extract_commodity_templates(self, commodity_docs: list) -> list:
        """Extract common templates from commodity lists."""
        templates = []

        # Template 1: Header + Entries + ku-ro Total
        header_entry_total = []
        for doc in commodity_docs:
            if doc['total_word'] and doc['total_word'].upper() == 'KU-RO':
                header_entry_total.append(doc['inscription'])

        if header_entry_total:
            templates.append({
                'name': 'Standard Commodity List (ku-ro)',
                'pattern': '[Header?] → [Entry + Logogram + Numeral]* → ku-ro + Total',
                'count': len(header_entry_total),
                'examples': header_entry_total[:5],
            })

        # Template 2: ki-ro deficit lists
        deficit_lists = [
            doc['inscription'] for doc in commodity_docs
            if doc['total_word'] and 'KI-RO' in doc['total_word'].upper()
        ]
        if deficit_lists:
            templates.append({
                'name': 'Deficit List (ki-ro)',
                'pattern': '[Entries] → ki-ro + Deficit Amount',
                'count': len(deficit_lists),
                'examples': deficit_lists[:5],
            })

        return templates

    # =========================================================================
    # CO-OCCURRENCE ANALYSIS
    # =========================================================================

    def analyze_cooccurrence(self, window_size: int = 3) -> dict:
        """
        Calculate co-occurrence statistics for words.

        Parameters:
            window_size: Number of words to consider as context
        """
        print(f"Analyzing co-occurrence (window_size={window_size})...")

        cooccurrence_matrix = defaultdict(Counter)
        word_counts = Counter()

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])

            # Filter to syllabic words only
            syllabic = []
            for word in words:
                if self._is_syllabic(word):
                    syllabic.append(word.upper())
                    word_counts[word.upper()] += 1

            # Calculate co-occurrence within window
            for i, word1 in enumerate(syllabic):
                for j in range(max(0, i - window_size), min(len(syllabic), i + window_size + 1)):
                    if i != j:
                        word2 = syllabic[j]
                        cooccurrence_matrix[word1][word2] += 1

        # Calculate PMI (Pointwise Mutual Information) for top pairs
        total_words = sum(word_counts.values())
        pmi_scores = []

        for word1, cooccur in cooccurrence_matrix.items():
            if word_counts[word1] < 5:  # Skip rare words
                continue

            for word2, count in cooccur.items():
                if word_counts[word2] < 5:
                    continue

                # PMI = log(P(x,y) / (P(x) * P(y)))
                p_xy = count / total_words
                p_x = word_counts[word1] / total_words
                p_y = word_counts[word2] / total_words

                if p_x * p_y > 0:
                    import math
                    pmi = math.log2(p_xy / (p_x * p_y)) if p_xy > 0 else 0

                    if pmi > 1:  # Only keep high PMI pairs
                        pmi_scores.append({
                            'word1': word1,
                            'word2': word2,
                            'cooccurrence_count': count,
                            'pmi': round(pmi, 3),
                        })

        # Sort by PMI
        pmi_scores.sort(key=lambda x: -x['pmi'])

        # Build word association lists
        associations = {}
        for word, cooccur in cooccurrence_matrix.items():
            if word_counts[word] >= 5:
                top_assoc = cooccur.most_common(10)
                associations[word] = [
                    {'word': w, 'count': c}
                    for w, c in top_assoc
                ]

        results = {
            'window_size': window_size,
            'total_words_analyzed': len(word_counts),
            'high_pmi_pairs': pmi_scores[:50],
            'top_word_associations': dict(list(associations.items())[:30]),
        }

        self.results['cooccurrence'] = results
        return results

    # =========================================================================
    # MAIN ANALYSIS
    # =========================================================================

    def run_full_analysis(self) -> dict:
        """Run all contextual analyses."""
        print("\n" + "=" * 60)
        print("RUNNING FULL CONTEXTUAL ANALYSIS")
        print("=" * 60)

        self.analyze_conditional_frequencies()
        self.detect_formulas()
        self.analyze_document_structures()
        self.analyze_cooccurrence()

        self.results['metadata']['generated'] = datetime.now().isoformat()

        return self.results

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 70)
        print("CONTEXTUAL ANALYSIS SUMMARY")
        print("=" * 70)

        # Conditional frequencies
        cond_freq = self.results.get('conditional_frequencies', {})
        print("\nConditional Frequency Highlights:")
        if 'before_total' in cond_freq:
            before_total = cond_freq['before_total'].get('top_words', [])[:5]
            print("  Words most likely to appear before ku-ro (total):")
            for item in before_total:
                print(f"    {item['word']}: {item['count']} times ({item['frequency']*100:.1f}%)")

        # Formulas
        formulas = self.results.get('formulas', {})
        print(f"\nFormulas Detected: {formulas.get('total_formulas_found', 0)}")
        top = formulas.get('top_formulas', [])[:5]
        for f in top:
            print(f"  '{f['formula']}' - {f['occurrences']} occurrences")

        # Document structures
        structures = self.results.get('document_structures', {})
        print("\nDocument Structure Types:")
        for struct_type, count in structures.get('structure_counts', {}).items():
            print(f"  {struct_type}: {count}")

        # Co-occurrence
        cooccur = self.results.get('cooccurrence', {})
        print("\nHigh PMI Word Pairs (strong associations):")
        high_pmi = cooccur.get('high_pmi_pairs', [])[:5]
        for pair in high_pmi:
            print(f"  {pair['word1']} + {pair['word2']}: PMI={pair['pmi']:.2f}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze contextual patterns in Linear A corpus"
    )
    parser.add_argument(
        '--analyze', '-a',
        type=str,
        choices=['frequencies', 'formulas', 'structure', 'cooccurrence', 'all'],
        default='all',
        help='Analysis type to run (default: all)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/contextual_analysis.json',
        help='Output path for results'
    )
    parser.add_argument(
        '--min-formula-length',
        type=int,
        default=2,
        help='Minimum words in formula (default: 2)'
    )
    parser.add_argument(
        '--min-formula-occurrences',
        type=int,
        default=3,
        help='Minimum formula occurrences (default: 3)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A CONTEXTUAL ANALYZER")
    print("=" * 60)

    analyzer = ContextualAnalyzer(verbose=args.verbose)

    if not analyzer.load_corpus():
        return 1

    # Run requested analyses
    if args.analyze == 'all':
        analyzer.run_full_analysis()
    elif args.analyze == 'frequencies':
        analyzer.analyze_conditional_frequencies()
    elif args.analyze == 'formulas':
        analyzer.detect_formulas(args.min_formula_length, args.min_formula_occurrences)
    elif args.analyze == 'structure':
        analyzer.analyze_document_structures()
    elif args.analyze == 'cooccurrence':
        analyzer.analyze_cooccurrence()

    analyzer.results['metadata']['generated'] = datetime.now().isoformat()

    # Save results
    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)

    # Print summary
    analyzer.print_summary()

    return 0


if __name__ == '__main__':
    sys.exit(main())
