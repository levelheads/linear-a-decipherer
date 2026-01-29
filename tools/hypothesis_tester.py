#!/usr/bin/env python3
"""
Multi-Hypothesis Tester for Linear A

Tests proposed Linear A readings against four mandatory linguistic hypotheses:
1. Luwian/Anatolian (Palmer, Finkelberg)
2. Semitic - West Semitic/Akkadian (Gordon, Best)
3. Pre-Greek Substrate (Beekes, Furnée)
4. Proto-Greek (Georgiev, Mosenkis)

This tool implements First Principle #4 (MULTI-HYPOTHESIS TESTING):
"Always test Luwian, Semitic, Pre-Greek, AND Proto-Greek readings."

Usage:
    python tools/hypothesis_tester.py [--word WORD] [--all] [--output FILE]

Examples:
    python tools/hypothesis_tester.py --word ku-ro
    python tools/hypothesis_tester.py --all --output data/hypothesis_results.json

Attribution:
    Part of Linear A Decipherment Project
    See FIRST_PRINCIPLES.md and references/hypotheses.md for methodology
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# ============================================================================
# LINGUISTIC REFERENCE DATA
# ============================================================================

# Luwian/Anatolian reference data
LUWIAN_LEXICON = {
    # Particles and grammatical elements
    'a': {'meaning': 'and/coordinative conjunction', 'confidence': 'HIGH'},
    'wa': {'meaning': 'quotative particle', 'confidence': 'HIGH'},
    'u': {'meaning': 'quotative particle variant', 'confidence': 'MEDIUM'},
    'ki': {'meaning': 'relative pronoun stem (kui-)', 'confidence': 'MEDIUM'},
    # Possible cognates
    'adi': {'meaning': 'to make/do', 'confidence': 'LOW'},
    'padi': {'meaning': 'into/to', 'confidence': 'LOW'},
    # Suffixes
    '-ja': {'meaning': 'adjectival suffix (-iya)', 'confidence': 'MEDIUM'},
    '-ti': {'meaning': 'verbal 3sg ending', 'confidence': 'LOW'},
    '-nti': {'meaning': 'verbal 3pl ending', 'confidence': 'LOW'},
    '-ssa': {'meaning': 'nominal suffix', 'confidence': 'MEDIUM'},
}

LUWIAN_PHONOLOGICAL_MARKERS = [
    # Luwian phonological features
    'wa', 'wi', 'wu',  # Labialized consonants
    'ssa', 'nda',      # Characteristic clusters
]

# Semitic reference data (Akkadian, Hebrew, West Semitic)
SEMITIC_LEXICON = {
    # Administrative terms
    'kull': {'meaning': 'all, total (Akkadian)', 'confidence': 'HIGH', 'root': 'KLL'},
    'kol': {'meaning': 'all (Hebrew)', 'confidence': 'HIGH', 'root': 'KL'},
    'gara': {'meaning': 'to diminish, deficit (Hebrew)', 'confidence': 'MEDIUM', 'root': 'GR'},
    'asap': {'meaning': 'to gather (Semitic *sp)', 'confidence': 'LOW', 'root': 'SP'},
    'sakar': {'meaning': 'to hire/reward', 'confidence': 'LOW', 'root': 'SKR'},
    # Common Semitic roots for administrative contexts
    'mlk': {'meaning': 'king, rule', 'confidence': 'LOW', 'root': 'MLK'},
    'spr': {'meaning': 'to count, scribe', 'confidence': 'LOW', 'root': 'SPR'},
}

# Extract consonant skeleton for Semitic comparison
def extract_consonants(word: str) -> str:
    """Extract consonant skeleton from Linear A transliteration."""
    consonants = []
    syllables = word.upper().split('-')
    for syl in syllables:
        # Remove subscripts
        syl = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
        if len(syl) >= 1:
            # First character is usually consonant (CV structure)
            first = syl[0]
            if first not in 'AEIOU':
                consonants.append(first)
    return ''.join(consonants)

# Pre-Greek substrate markers
PREGREEK_MARKERS = {
    # Characteristic phonological patterns
    'nth': {'type': 'cluster', 'significance': 'HIGH', 'examples': ['Korinthos', 'labyrinth']},
    'ss': {'type': 'cluster', 'significance': 'HIGH', 'examples': ['Knossos', 'Parnassos']},
    'mn': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': ['Amnissos']},
    'nd': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': []},
    'assos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Parnassos']},
    'inthos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Korinthos', 'Zakynthos']},
    'issos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Tylissos']},
}

# Proto-Greek/Greek reference data
GREEK_LEXICON = {
    # Possible cognates
    'kyrios': {'meaning': 'lord, master → total', 'Linear_B': 'ku-ro', 'confidence': 'MEDIUM'},
    'chreos': {'meaning': 'debt', 'Linear_B': 'ki-re-o', 'confidence': 'LOW'},
    'meter': {'meaning': 'mother', 'Linear_B': 'ma-te', 'confidence': 'LOW'},
    'demos': {'meaning': 'people, district', 'Linear_B': 'da-mo', 'confidence': 'LOW'},
    'wanax': {'meaning': 'king', 'Linear_B': 'wa-na-ka', 'confidence': 'HIGH'},
    'woinos': {'meaning': 'wine', 'Linear_B': 'wo-no', 'confidence': 'HIGH'},
    # Administrative terms
    'kolos': {'meaning': 'total (unattested but plausible)', 'confidence': 'SPECULATIVE'},
}


class HypothesisTester:
    """
    Tests Linear A words against four linguistic hypotheses.

    For each word, generates:
    - Luwian analysis (particles, morphology, cognates)
    - Semitic analysis (consonant skeleton matching)
    - Pre-Greek analysis (phonological markers)
    - Proto-Greek analysis (Greek cognate comparison)
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'Four-Hypothesis Testing (First Principle #4)',
            },
            'word_analyses': {},
            'corpus_statistics': {},
            'hypothesis_summaries': {
                'luwian': {'supported': 0, 'contradicted': 0, 'neutral': 0},
                'semitic': {'supported': 0, 'contradicted': 0, 'neutral': 0},
                'pregreek': {'supported': 0, 'contradicted': 0, 'neutral': 0},
                'protogreek': {'supported': 0, 'contradicted': 0, 'neutral': 0},
            }
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

    def extract_words(self) -> Dict[str, int]:
        """Extract all words with frequencies from corpus."""
        word_freq = Counter()

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            transliterated = data.get('transliteratedWords', [])
            for word in transliterated:
                if not word or word in ['\n', '𐄁', '', '—', '≈']:
                    continue
                # Skip numerals
                if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', word):
                    continue
                # Skip pure logograms
                if re.match(r'^[A-Z*\d+\[\]]+$', word) and '-' not in word:
                    continue
                if word.startswith('𐝫'):
                    continue

                word_freq[word] += 1

        return dict(word_freq)

    # =========================================================================
    # HYPOTHESIS 1: LUWIAN/ANATOLIAN
    # =========================================================================

    def test_luwian(self, word: str) -> dict:
        """
        Test word against Luwian/Anatolian hypothesis.

        Checks for:
        - Luwian particles (a-, wa-, u-)
        - Luwian morphological patterns
        - Luwian lexical cognates
        """
        result = {
            'hypothesis': 'Luwian/Anatolian',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'cognates_found': [],
        }

        word_upper = word.upper()
        syllables = word_upper.split('-')

        # Check for Luwian particles
        if syllables[0] == 'A':
            result['evidence'].append({
                'type': 'particle',
                'element': 'A-',
                'interpretation': 'Possible Luwian coordinative conjunction',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        if 'WA' in syllables or 'U' in syllables:
            result['evidence'].append({
                'type': 'particle',
                'element': 'WA/U',
                'interpretation': 'Possible Luwian quotative particle',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # Check for Luwian suffixes
        if word_upper.endswith('-JA'):
            result['evidence'].append({
                'type': 'morphology',
                'element': '-JA',
                'interpretation': 'Possible Luwian adjectival suffix (-iya)',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        if word_upper.endswith('-TI') or word_upper.endswith('-NTI'):
            result['evidence'].append({
                'type': 'morphology',
                'element': '-TI/-NTI',
                'interpretation': 'Possible Luwian verbal ending (3sg/3pl)',
                'confidence': 'LOW',
            })
            result['score'] += 0.5

        # Check Luwian lexicon
        for luw_word, data in LUWIAN_LEXICON.items():
            if luw_word.upper() in word_upper or word_upper in luw_word.upper():
                result['cognates_found'].append({
                    'luwian': luw_word,
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                })
                result['score'] += 1 if data['confidence'] == 'HIGH' else 0.5

        # Determine verdict
        if result['score'] >= 2:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1:
            result['verdict'] = 'POSSIBLE'
        else:
            result['verdict'] = 'NEUTRAL'

        return result

    # =========================================================================
    # HYPOTHESIS 2: SEMITIC
    # =========================================================================

    def test_semitic(self, word: str) -> dict:
        """
        Test word against Semitic hypothesis.

        Uses consonant extraction method:
        1. Strip vowels to get consonant skeleton
        2. Compare against known Semitic roots
        3. Check for triconsonantal patterns
        """
        result = {
            'hypothesis': 'Semitic (West Semitic/Akkadian)',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'consonant_skeleton': '',
            'root_matches': [],
        }

        # Extract consonant skeleton
        consonants = extract_consonants(word)
        result['consonant_skeleton'] = consonants

        # Check against Semitic lexicon
        for sem_word, data in SEMITIC_LEXICON.items():
            root = data.get('root', sem_word.upper())
            if consonants == root or consonants in root or root in consonants:
                result['root_matches'].append({
                    'semitic_root': root,
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                })
                if data['confidence'] == 'HIGH':
                    result['score'] += 2
                elif data['confidence'] == 'MEDIUM':
                    result['score'] += 1
                else:
                    result['score'] += 0.5

        # Check for triconsonantal structure (characteristic of Semitic)
        if len(consonants) == 3:
            result['evidence'].append({
                'type': 'structure',
                'observation': f'Triconsonantal skeleton: {consonants}',
                'interpretation': 'Potentially compatible with Semitic root structure',
                'confidence': 'LOW',
            })
            result['score'] += 0.5

        # K-R pattern special case (ku-ro = *kull "all")
        if consonants in ['KR', 'KL', 'KLL']:
            result['evidence'].append({
                'type': 'cognate',
                'observation': 'K-R/K-L skeleton',
                'interpretation': 'Matches Semitic *kull/*kol "all, total"',
                'confidence': 'HIGH',
            })
            result['score'] += 2

        # Determine verdict
        if result['score'] >= 2:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1:
            result['verdict'] = 'POSSIBLE'
        else:
            result['verdict'] = 'NEUTRAL'

        return result

    # =========================================================================
    # HYPOTHESIS 3: PRE-GREEK SUBSTRATE
    # =========================================================================

    def test_pregreek(self, word: str) -> dict:
        """
        Test word against Pre-Greek substrate hypothesis.

        Checks for:
        - Characteristic consonant clusters (-nth-, -ss-, -mn-)
        - Pre-Greek suffix patterns (-assos, -inthos)
        - Non-IE phonological features
        """
        result = {
            'hypothesis': 'Pre-Greek Substrate',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'markers_found': [],
        }

        word_upper = word.upper()

        # Check for Pre-Greek markers
        for marker, data in PREGREEK_MARKERS.items():
            if marker.upper() in word_upper:
                result['markers_found'].append({
                    'marker': marker,
                    'type': data['type'],
                    'significance': data['significance'],
                    'examples': data['examples'],
                })
                if data['significance'] == 'HIGH':
                    result['score'] += 2
                else:
                    result['score'] += 1

        # Check for vowel alternations (a/e, i/e) characteristic of Pre-Greek
        syllables = word_upper.split('-')
        vowel_alternation = False
        for i, syl in enumerate(syllables[:-1]):
            if len(syl) >= 2 and len(syllables[i+1]) >= 2:
                v1 = syl[-1] if syl[-1] in 'AEIOU' else ''
                v2 = syllables[i+1][-1] if syllables[i+1][-1] in 'AEIOU' else ''
                if (v1 == 'A' and v2 == 'E') or (v1 == 'E' and v2 == 'A'):
                    vowel_alternation = True

        if vowel_alternation:
            result['evidence'].append({
                'type': 'phonology',
                'observation': 'A/E vowel alternation',
                'interpretation': 'Characteristic of Pre-Greek words',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # Determine verdict
        if result['score'] >= 2:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1:
            result['verdict'] = 'POSSIBLE'
        else:
            result['verdict'] = 'NEUTRAL'

        return result

    # =========================================================================
    # HYPOTHESIS 4: PROTO-GREEK
    # =========================================================================

    def test_protogreek(self, word: str) -> dict:
        """
        Test word against Proto-Greek hypothesis.

        Checks for:
        - Linear B cognates
        - Greek lexical matches
        - Greek morphological patterns
        """
        result = {
            'hypothesis': 'Proto-Greek',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'greek_cognates': [],
        }

        word_upper = word.upper()
        syllables = word_upper.split('-')

        # Check Greek lexicon
        for greek_word, data in GREEK_LEXICON.items():
            linear_b = data.get('Linear_B', '').upper()
            if word_upper == linear_b or word_upper in linear_b:
                result['greek_cognates'].append({
                    'greek': greek_word,
                    'linear_b': data.get('Linear_B'),
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                })
                if data['confidence'] == 'HIGH':
                    result['score'] += 2
                elif data['confidence'] == 'MEDIUM':
                    result['score'] += 1
                else:
                    result['score'] += 0.5

        # Check for Greek-like case endings
        greek_endings = ['-O', '-A', '-AS', '-OS', '-E', '-I']
        for ending in greek_endings:
            if word_upper.endswith(ending.replace('-', '')):
                result['evidence'].append({
                    'type': 'morphology',
                    'observation': f'Ending {ending}',
                    'interpretation': 'Potentially compatible with Greek case system',
                    'confidence': 'LOW',
                })
                result['score'] += 0.25

        # Special case: ku-ro
        if word_upper == 'KU-RO':
            result['evidence'].append({
                'type': 'functional',
                'observation': 'ku-ro totaling function',
                'interpretation': 'Parallels Linear B ku-ro usage; may relate to Greek kyrios',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # Determine verdict
        if result['score'] >= 2:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1:
            result['verdict'] = 'POSSIBLE'
        else:
            result['verdict'] = 'NEUTRAL'

        return result

    # =========================================================================
    # MAIN TESTING FUNCTIONS
    # =========================================================================

    def test_word(self, word: str, frequency: int = 1) -> dict:
        """
        Test a single word against all four hypotheses.

        Returns complete multi-hypothesis analysis.
        """
        analysis = {
            'word': word,
            'frequency': frequency,
            'hypotheses': {
                'luwian': self.test_luwian(word),
                'semitic': self.test_semitic(word),
                'pregreek': self.test_pregreek(word),
                'protogreek': self.test_protogreek(word),
            },
            'synthesis': {},
        }

        # Synthesize results
        verdicts = {h: analysis['hypotheses'][h]['verdict']
                    for h in analysis['hypotheses']}
        scores = {h: analysis['hypotheses'][h]['score']
                  for h in analysis['hypotheses']}

        # Find best-supported hypothesis
        best_hyp = max(scores.keys(), key=lambda k: scores[k])
        best_score = scores[best_hyp]

        # Count supported hypotheses
        supported = [h for h, v in verdicts.items() if v == 'SUPPORTED']

        analysis['synthesis'] = {
            'best_hypothesis': best_hyp if best_score > 0 else 'NONE',
            'best_score': best_score,
            'supported_count': len(supported),
            'supported_hypotheses': supported,
            'multi_hypothesis_support': len(supported) > 1,
            'max_confidence': self._determine_confidence(supported, best_score),
        }

        return analysis

    def _determine_confidence(self, supported: List[str], best_score: float) -> str:
        """
        Determine maximum confidence based on First Principles.

        - Single-hypothesis support → Max: PROBABLE
        - Multi-hypothesis support → Can be CERTAIN
        - No support → SPECULATIVE
        """
        if len(supported) >= 2:
            return 'CERTAIN' if best_score >= 3 else 'PROBABLE'
        elif len(supported) == 1:
            return 'PROBABLE'  # Single-hypothesis cap
        elif best_score >= 1:
            return 'POSSIBLE'
        else:
            return 'SPECULATIVE'

    def test_corpus(self, min_frequency: int = 3):
        """
        Test all words in corpus above frequency threshold.
        """
        print("\nExtracting words from corpus...")
        word_freqs = self.extract_words()

        words_to_test = {w: f for w, f in word_freqs.items() if f >= min_frequency}
        print(f"Testing {len(words_to_test)} words (freq >= {min_frequency})...")

        for word, freq in words_to_test.items():
            analysis = self.test_word(word, freq)
            self.results['word_analyses'][word] = analysis

            # Update hypothesis summaries
            for hyp, data in analysis['hypotheses'].items():
                verdict = data['verdict']
                if verdict == 'SUPPORTED':
                    self.results['hypothesis_summaries'][hyp]['supported'] += 1
                elif verdict == 'NEUTRAL':
                    self.results['hypothesis_summaries'][hyp]['neutral'] += 1
                else:
                    self.results['hypothesis_summaries'][hyp]['contradicted'] += 1

            self.log(f"{word}: {analysis['synthesis']['best_hypothesis']} ({analysis['synthesis']['max_confidence']})")

        self.results['metadata']['words_tested'] = len(words_to_test)
        self.results['metadata']['min_frequency'] = min_frequency

    def save_results(self, output_path: Path):
        """Save results to JSON."""
        self.results['metadata']['generated'] = datetime.now().isoformat()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

        print(f"\nResults saved to: {output_path}")

    def print_summary(self):
        """Print analysis summary."""
        print("\n" + "=" * 60)
        print("MULTI-HYPOTHESIS TEST SUMMARY")
        print("=" * 60)
        print(f"Following First Principle #4: Test ALL hypotheses\n")

        print("Hypothesis Support Summary:")
        for hyp, stats in self.results['hypothesis_summaries'].items():
            total = stats['supported'] + stats['neutral'] + stats['contradicted']
            if total > 0:
                pct = stats['supported'] / total * 100
                print(f"  {hyp.upper():12} - Supported: {stats['supported']:3} ({pct:.1f}%)")

        # Find words with multi-hypothesis support
        multi_support = [
            w for w, a in self.results['word_analyses'].items()
            if a['synthesis']['multi_hypothesis_support']
        ]

        if multi_support:
            print(f"\nWords with multi-hypothesis support ({len(multi_support)}):")
            for word in multi_support[:10]:
                analysis = self.results['word_analyses'][word]
                supported = analysis['synthesis']['supported_hypotheses']
                print(f"  {word}: {', '.join(supported)}")

        # High-confidence words
        high_conf = [
            (w, a) for w, a in self.results['word_analyses'].items()
            if a['synthesis']['max_confidence'] in ['CERTAIN', 'PROBABLE']
        ]
        high_conf.sort(key=lambda x: x[1]['frequency'], reverse=True)

        if high_conf:
            print(f"\nHigh-confidence interpretations ({len(high_conf)}):")
            for word, analysis in high_conf[:10]:
                conf = analysis['synthesis']['max_confidence']
                best = analysis['synthesis']['best_hypothesis']
                freq = analysis['frequency']
                print(f"  {word} (freq={freq}): {best.upper()} [{conf}]")

        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Test Linear A readings against four linguistic hypotheses"
    )
    parser.add_argument(
        '--word', '-w',
        type=str,
        help='Test a specific word (e.g., ku-ro)'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Test all words in corpus'
    )
    parser.add_argument(
        '--min-freq', '-m',
        type=int,
        default=3,
        help='Minimum frequency for corpus-wide testing (default: 3)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/hypothesis_results.json',
        help='Output path for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A MULTI-HYPOTHESIS TESTER")
    print("=" * 60)
    print("Enforcing First Principle #4: Test ALL hypotheses")

    tester = HypothesisTester(verbose=args.verbose)

    if args.word:
        # Test single word
        print(f"\nTesting word: {args.word}")
        analysis = tester.test_word(args.word)

        print(f"\n{'='*60}")
        print(f"ANALYSIS: {args.word}")
        print(f"{'='*60}")

        for hyp, data in analysis['hypotheses'].items():
            print(f"\n{hyp.upper()}: {data['verdict']} (score: {data['score']})")
            if data.get('evidence'):
                for ev in data['evidence']:
                    print(f"  - {ev['observation']}: {ev['interpretation']}")
            if data.get('cognates_found') or data.get('root_matches') or data.get('greek_cognates'):
                cognates = data.get('cognates_found') or data.get('root_matches') or data.get('greek_cognates')
                for cog in cognates:
                    meaning = cog.get('meaning', cog.get('interpretation', ''))
                    print(f"  - Cognate: {meaning}")

        print(f"\nSYNTHESIS:")
        print(f"  Best hypothesis: {analysis['synthesis']['best_hypothesis']}")
        print(f"  Max confidence: {analysis['synthesis']['max_confidence']}")
        if analysis['synthesis']['multi_hypothesis_support']:
            print(f"  Multi-hypothesis support: {', '.join(analysis['synthesis']['supported_hypotheses'])}")

    elif args.all:
        # Test all corpus words
        if not tester.load_corpus():
            return 1

        tester.test_corpus(min_frequency=args.min_freq)

        # Save results
        output_path = PROJECT_ROOT / args.output
        tester.save_results(output_path)

        # Print summary
        tester.print_summary()

    else:
        print("\nUsage:")
        print("  --word WORD    Test a specific word")
        print("  --all          Test all corpus words")
        print("\nExamples:")
        print("  python hypothesis_tester.py --word ku-ro")
        print("  python hypothesis_tester.py --all --min-freq 5")

    return 0


if __name__ == '__main__':
    sys.exit(main())
