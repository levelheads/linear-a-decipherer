#!/usr/bin/env python3
"""
Linear A Corpus Cross-Reference Tool

Fast indexed search for corpus-wide pattern verification:
- Exact word search
- Wildcard patterns (ku-*-ro, *-ja, etc.)
- Regex patterns
- Context-aware results (site, line, adjacent words, logograms, numerals)

This tool implements First Principle #6 (CROSS-CORPUS CONSISTENCY):
"Readings must work across the entire corpus, not just one tablet."

Usage:
    python tools/corpus_lookup.py [options] PATTERN

Examples:
    python tools/corpus_lookup.py ku-ro           # Exact match
    python tools/corpus_lookup.py "ku-*"          # Wildcard (starts with ku-)
    python tools/corpus_lookup.py --regex "K[UI]-RO"  # Regex pattern
    python tools/corpus_lookup.py --context 3 ku-ro   # Show 3 words context

Options:
    --exact, -e       Exact match only (default)
    --wildcard, -w    Wildcard match (* = any, ? = single char)
    --regex, -r       Regular expression match
    --context, -c N   Show N words of context on each side
    --site SITE       Filter by site code (e.g., HT, KH, ZA)
    --period PERIOD   Filter by chronological period (e.g., LMIB)
    --output, -o FILE Write results to JSON file
    --verbose, -v     Show detailed output

Attribution:
    Part of Linear A Decipherment Project
    Enables First Principle #6 verification
"""

import json
import argparse
import sys
import re
import fnmatch
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


class CorpusLookup:
    """
    Fast corpus lookup for cross-reference verification.

    Supports:
    - Exact matching
    - Wildcard patterns (*, ?)
    - Regular expressions
    - Context extraction
    - Filtering by site/period
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.word_index = {}  # word -> [(inscription_id, position, context)]
        self.sign_index = {}  # sign -> [(inscription_id, position)]

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load and index corpus data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)

            self._build_index()
            return True

        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _build_index(self):
        """Build search indexes for fast lookup."""
        print("Building search index...")

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            transliterated = data.get('transliteratedWords', [])

            for idx, word in enumerate(transliterated):
                if not word or word == '\n':
                    continue

                # Index the word
                if word not in self.word_index:
                    self.word_index[word] = []

                self.word_index[word].append({
                    'inscription': insc_id,
                    'position': idx,
                    'site': data.get('site', ''),
                    'site_code': self._extract_site_code(insc_id),
                    'period': data.get('context', ''),
                    'support': data.get('support', ''),
                })

                # Index individual signs
                if '-' in word:
                    for sign in word.split('-'):
                        sign_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', sign).upper()
                        if sign_clean and len(sign_clean) <= 6:
                            if sign_clean not in self.sign_index:
                                self.sign_index[sign_clean] = []
                            self.sign_index[sign_clean].append({
                                'inscription': insc_id,
                                'position': idx,
                                'word': word,
                            })

        print(f"Indexed {len(self.word_index)} unique words, {len(self.sign_index)} unique signs")

    def _extract_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        match = re.match(r'^([A-Z]+)', inscription_id)
        return match.group(1) if match else ''

    def _get_context(self, inscription_id: str, position: int, context_size: int) -> dict:
        """Get surrounding words for context."""
        data = self.corpus['inscriptions'].get(inscription_id, {})
        words = data.get('transliteratedWords', [])

        start = max(0, position - context_size)
        end = min(len(words), position + context_size + 1)

        context_words = []
        for i in range(start, end):
            w = words[i] if i < len(words) else ''
            if w == '\n':
                w = '|'  # Line break marker
            context_words.append(w)

        # Calculate relative position
        relative_pos = position - start

        return {
            'words': context_words,
            'target_position': relative_pos,
            'before': context_words[:relative_pos],
            'after': context_words[relative_pos + 1:] if relative_pos + 1 < len(context_words) else [],
        }

    def _identify_adjacent_elements(self, inscription_id: str, position: int) -> dict:
        """Identify logograms, numerals, and other elements near the word."""
        data = self.corpus['inscriptions'].get(inscription_id, {})
        words = data.get('transliteratedWords', [])

        result = {
            'preceding_logogram': None,
            'following_logogram': None,
            'following_numeral': None,
            'line_number': 0,
        }

        # Count newlines to determine line number
        line_num = 1
        for i in range(position):
            if i < len(words) and words[i] == '\n':
                line_num += 1
        result['line_number'] = line_num

        # Check preceding word
        if position > 0:
            prev = words[position - 1] if position - 1 < len(words) else ''
            if prev and re.match(r'^[A-Z*\d+\[\]]+$', prev) and '-' not in prev:
                result['preceding_logogram'] = prev

        # Check following words
        for i in range(position + 1, min(position + 3, len(words))):
            w = words[i] if i < len(words) else ''
            if w == '\n':
                break
            # Check if logogram
            if w and re.match(r'^[A-Z*\d+\[\]]+$', w) and '-' not in w:
                if not result['following_logogram']:
                    result['following_logogram'] = w
            # Check if numeral
            if w and re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|≈]+$', w):
                if not result['following_numeral']:
                    result['following_numeral'] = w

        return result

    def search_exact(self, query: str, site_filter: str = None,
                     period_filter: str = None, context_size: int = 0) -> List[dict]:
        """Search for exact word match."""
        results = []

        matches = self.word_index.get(query, [])

        for match in matches:
            # Apply filters
            if site_filter and not match['site_code'].startswith(site_filter.upper()):
                continue
            if period_filter and match['period'] != period_filter:
                continue

            result = {
                'word': query,
                'inscription': match['inscription'],
                'position': match['position'],
                'site': match['site'],
                'site_code': match['site_code'],
                'period': match['period'],
                'support': match['support'],
            }

            # Add context if requested
            if context_size > 0:
                result['context'] = self._get_context(
                    match['inscription'], match['position'], context_size
                )

            # Add adjacent element info
            result['adjacent'] = self._identify_adjacent_elements(
                match['inscription'], match['position']
            )

            results.append(result)

        return results

    def search_wildcard(self, pattern: str, site_filter: str = None,
                        period_filter: str = None, context_size: int = 0) -> List[dict]:
        """Search using wildcard pattern (* = any, ? = single char)."""
        results = []

        # Convert wildcard to regex
        pattern_upper = pattern.upper()

        for word in self.word_index:
            word_upper = word.upper()
            if fnmatch.fnmatch(word_upper, pattern_upper):
                word_results = self.search_exact(word, site_filter, period_filter, context_size)
                results.extend(word_results)

        return results

    def search_regex(self, pattern: str, site_filter: str = None,
                     period_filter: str = None, context_size: int = 0) -> List[dict]:
        """Search using regular expression."""
        results = []

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
            return results

        for word in self.word_index:
            if regex.search(word):
                word_results = self.search_exact(word, site_filter, period_filter, context_size)
                results.extend(word_results)

        return results

    def search_sign(self, sign: str, site_filter: str = None,
                    period_filter: str = None) -> List[dict]:
        """Search for a specific sign (syllabogram) in any word."""
        results = []

        sign_upper = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', sign).upper()
        matches = self.sign_index.get(sign_upper, [])

        for match in matches:
            insc_id = match['inscription']
            data = self.corpus['inscriptions'].get(insc_id, {})

            # Apply filters
            site_code = self._extract_site_code(insc_id)
            if site_filter and not site_code.startswith(site_filter.upper()):
                continue
            period = data.get('context', '')
            if period_filter and period != period_filter:
                continue

            results.append({
                'sign': sign_upper,
                'word': match['word'],
                'inscription': insc_id,
                'position': match['position'],
                'site': data.get('site', ''),
                'period': period,
            })

        return results

    def verify_reading_consistency(self, word: str) -> dict:
        """
        Verify that a proposed reading is consistent across all occurrences.

        This is the core function for First Principle #6 verification.
        """
        results = self.search_exact(word, context_size=2)

        if not results:
            return {
                'word': word,
                'total_occurrences': 0,
                'verified': False,
                'message': 'Word not found in corpus',
                'sites': {},
                'periods': {},
                'contexts': {},
                'consistency_score': 0,
                'verdict': 'NOT_FOUND',
                'first_principle_6': 'FAIL',
            }

        # Analyze distribution
        sites = defaultdict(int)
        periods = defaultdict(int)
        contexts = defaultdict(int)

        for r in results:
            sites[r['site_code']] += 1
            if r['period']:
                periods[r['period']] += 1

            # Categorize by context
            adj = r['adjacent']
            if adj['following_logogram']:
                contexts['pre_logogram'] += 1
            elif adj['following_numeral']:
                contexts['pre_numeral'] += 1
            else:
                contexts['other'] += 1

        # Determine consistency
        consistency_score = 0

        # Multi-site attestation is good
        if len(sites) >= 2:
            consistency_score += 1

        # Consistent context is good
        if len(contexts) == 1 or max(contexts.values()) / len(results) >= 0.7:
            consistency_score += 1

        # Multi-period attestation suggests stability
        if len(periods) >= 2:
            consistency_score += 1

        verification = {
            'word': word,
            'total_occurrences': len(results),
            'sites': dict(sites),
            'periods': dict(periods),
            'contexts': dict(contexts),
            'consistency_score': consistency_score,
            'verified': consistency_score >= 2,
            'verdict': 'CONSISTENT' if consistency_score >= 2 else 'NEEDS_REVIEW',
            'first_principle_6': 'PASS' if consistency_score >= 2 else 'PARTIAL',
        }

        return verification

    def generate_attestation_report(self, word: str) -> str:
        """Generate a human-readable attestation report for a word."""
        results = self.search_exact(word, context_size=2)
        verification = self.verify_reading_consistency(word)

        report = []
        report.append(f"{'='*60}")
        report.append(f"ATTESTATION REPORT: {word}")
        report.append(f"{'='*60}")
        report.append(f"Total occurrences: {verification['total_occurrences']}")
        report.append(f"Sites: {', '.join(f'{k}({v})' for k, v in verification['sites'].items())}")
        report.append(f"Periods: {', '.join(f'{k}({v})' for k, v in verification['periods'].items())}")
        report.append(f"Contexts: {', '.join(f'{k}({v})' for k, v in verification['contexts'].items())}")
        report.append(f"\nFirst Principle #6 Verification: {verification['first_principle_6']}")
        report.append(f"Verdict: {verification['verdict']}")
        report.append(f"\n{'='*60}")
        report.append("ATTESTATIONS:")
        report.append(f"{'='*60}")

        for i, r in enumerate(results[:20], 1):  # Limit to 20 for display
            ctx = r.get('context', {})
            before = ' '.join(ctx.get('before', []))
            after = ' '.join(ctx.get('after', []))
            adj = r.get('adjacent', {})

            report.append(f"\n{i}. {r['inscription']} (Line {adj.get('line_number', '?')})")
            report.append(f"   Site: {r['site']} | Period: {r['period']}")
            report.append(f"   Context: {before} [{word}] {after}")
            if adj.get('following_logogram'):
                report.append(f"   Following logogram: {adj['following_logogram']}")
            if adj.get('following_numeral'):
                report.append(f"   Following numeral: {adj['following_numeral']}")

        if len(results) > 20:
            report.append(f"\n... and {len(results) - 20} more occurrences")

        report.append(f"\n{'='*60}")

        return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Search Linear A corpus for cross-reference verification"
    )
    parser.add_argument(
        'pattern',
        nargs='?',
        help='Search pattern (word, wildcard, or regex)'
    )
    parser.add_argument(
        '--exact', '-e',
        action='store_true',
        help='Exact match (default)'
    )
    parser.add_argument(
        '--wildcard', '-w',
        action='store_true',
        help='Wildcard match (* = any, ? = single char)'
    )
    parser.add_argument(
        '--regex', '-r',
        action='store_true',
        help='Regular expression match'
    )
    parser.add_argument(
        '--sign', '-s',
        action='store_true',
        help='Search for sign (syllabogram) in any word'
    )
    parser.add_argument(
        '--context', '-c',
        type=int,
        default=2,
        help='Number of words context on each side (default: 2)'
    )
    parser.add_argument(
        '--site',
        type=str,
        help='Filter by site code (e.g., HT, KH, ZA)'
    )
    parser.add_argument(
        '--period',
        type=str,
        help='Filter by period (e.g., LMIB, MMIII)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Run First Principle #6 consistency verification'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate detailed attestation report'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Write results to JSON file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    if not args.pattern:
        parser.print_help()
        return 0

    lookup = CorpusLookup(verbose=args.verbose)

    if not lookup.load_corpus():
        return 1

    # Perform search
    if args.report:
        # Generate detailed report
        report = lookup.generate_attestation_report(args.pattern)
        print(report)
        return 0

    if args.verify:
        # Run consistency verification
        verification = lookup.verify_reading_consistency(args.pattern)
        print(f"\n{'='*60}")
        print(f"FIRST PRINCIPLE #6 VERIFICATION: {args.pattern}")
        print(f"{'='*60}")
        print(f"Total occurrences: {verification['total_occurrences']}")
        print(f"Sites: {verification['sites']}")
        print(f"Periods: {verification['periods']}")
        print(f"Contexts: {verification['contexts']}")
        print(f"Consistency score: {verification['consistency_score']}/3")
        print(f"Verdict: {verification['verdict']}")
        print(f"First Principle #6: {verification['first_principle_6']}")
        print(f"{'='*60}")
        return 0

    # Regular search
    if args.regex:
        results = lookup.search_regex(args.pattern, args.site, args.period, args.context)
    elif args.wildcard:
        results = lookup.search_wildcard(args.pattern, args.site, args.period, args.context)
    elif args.sign:
        results = lookup.search_sign(args.pattern, args.site, args.period)
    else:
        results = lookup.search_exact(args.pattern, args.site, args.period, args.context)

    # Output results
    print(f"\nFound {len(results)} occurrences of '{args.pattern}'")

    if args.output:
        output_path = PROJECT_ROOT / args.output
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'query': args.pattern,
                'total_results': len(results),
                'results': results,
            }, f, ensure_ascii=False, indent=2)
        print(f"Results saved to: {output_path}")
    else:
        # Print to console
        print(f"\n{'='*60}")
        for i, r in enumerate(results[:30], 1):  # Limit display to 30
            print(f"{i}. {r['inscription']} ({r['site_code']}, {r.get('period', 'N/A')})")
            if 'context' in r:
                ctx = r['context']
                before = ' '.join(ctx.get('before', []))
                after = ' '.join(ctx.get('after', []))
                print(f"   {before} [{r['word']}] {after}")

        if len(results) > 30:
            print(f"\n... and {len(results) - 30} more results")

        print(f"{'='*60}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
