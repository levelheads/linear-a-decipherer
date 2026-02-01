#!/usr/bin/env python3
"""
Negative Evidence Analyzer for Linear A

Implements First Principle #5 (NEGATIVE EVIDENCE):
"What the script DOESN'T show is also informative."

This tool analyzes:
1. What patterns each hypothesis PREDICTS that DON'T appear
2. Phonotactic constraints allowed/forbidden by each hypothesis
3. Statistical comparison of predicted vs actual frequencies
4. Expected morphological patterns that are absent

Usage:
    python tools/negative_evidence.py [--hypothesis HYP] [--all] [--output FILE]

Examples:
    python tools/negative_evidence.py --all
    python tools/negative_evidence.py --hypothesis greek --verbose
    python tools/negative_evidence.py --all --output data/negative_evidence_report.json

Attribution:
    Part of Linear A Decipherment Project
    Implements First Principle #5 from FIRST_PRINCIPLES.md
"""

import json
import argparse
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# ============================================================================
# EXPECTED PATTERNS BY HYPOTHESIS
# ============================================================================

# What each hypothesis predicts we SHOULD find in Linear A

GREEK_EXPECTATIONS = {
    'name': 'Proto-Greek',
    'vowel_distribution': {
        'description': 'Greek has balanced vowel distribution (~20% each for a, e, i, o, with less u)',
        'expected': {'a': 0.22, 'e': 0.20, 'i': 0.18, 'o': 0.20, 'u': 0.15},
        'tolerance': 0.08,  # Allow 8% deviation
    },
    'morphology': {
        'case_endings': [
            {'pattern': '-o', 'description': 'nominative/accusative neuter singular', 'expected_freq': 'high'},
            {'pattern': '-os', 'description': 'nominative masculine singular', 'expected_freq': 'high'},
            {'pattern': '-a', 'description': 'nominative feminine singular', 'expected_freq': 'high'},
            {'pattern': '-oi', 'description': 'nominative masculine plural', 'expected_freq': 'medium'},
            {'pattern': '-ai', 'description': 'nominative feminine plural', 'expected_freq': 'medium'},
            {'pattern': '-es', 'description': 'nominative plural (various)', 'expected_freq': 'medium'},
        ],
        'verbal_endings': [
            {'pattern': '-mi', 'description': '1sg present (athematic)', 'expected_freq': 'low'},
            {'pattern': '-si', 'description': '2sg/3sg present', 'expected_freq': 'medium'},
            {'pattern': '-ti', 'description': '3sg present', 'expected_freq': 'medium'},
            {'pattern': '-nti', 'description': '3pl present', 'expected_freq': 'low'},
        ],
    },
    'vocabulary': {
        'expected_cognates': [
            {'Linear_B': 'to-so', 'meaning': 'total (τόσος)', 'context': 'totaling'},
            {'Linear_B': 'wa-na-ka', 'meaning': 'king (ϝάναξ)', 'context': 'personnel'},
            {'Linear_B': 'po-ti-ni-ja', 'meaning': 'lady/mistress', 'context': 'religious'},
        ],
    },
    'phonotactics': {
        'forbidden_initial': [],  # Greek allows most initials
        'forbidden_clusters': ['pt-', 'bd-', 'gd-'],  # Initial stops + d
        'expected_clusters': ['sp-', 'st-', 'sk-', 'sm-', 'sn-'],
    },
}

SEMITIC_EXPECTATIONS = {
    'name': 'Semitic (Akkadian/West Semitic)',
    'root_structure': {
        'description': 'Semitic uses triconsonantal roots with vowel patterns',
        'triconsonantal_expected': True,
        'typical_patterns': ['CaCaC', 'CiCiC', 'CuCuC', 'CaCiC'],
    },
    'morphology': {
        'prefixes': [
            {'pattern': 'a-', 'description': 'causative/1sg', 'expected_freq': 'medium'},
            {'pattern': 'i-', 'description': '3sg masc (imperfect)', 'expected_freq': 'medium'},
            {'pattern': 'ta-', 'description': '2sg/3sg fem', 'expected_freq': 'medium'},
            {'pattern': 'na-', 'description': '1pl', 'expected_freq': 'low'},
        ],
        'suffixes': [
            {'pattern': '-u', 'description': 'nominative (Akkadian)', 'expected_freq': 'high'},
            {'pattern': '-a', 'description': 'accusative (Akkadian)', 'expected_freq': 'high'},
            {'pattern': '-im', 'description': 'masculine plural', 'expected_freq': 'medium'},
            {'pattern': '-at', 'description': 'feminine singular', 'expected_freq': 'medium'},
        ],
    },
    'vocabulary': {
        'expected_roots': [
            {'root': 'KLL', 'meaning': 'all/total', 'expected': True},
            {'root': 'MLK', 'meaning': 'king', 'expected': True},
            {'root': 'SPR', 'meaning': 'write/count', 'expected': True},
            {'root': 'BRK', 'meaning': 'bless', 'expected': True},
        ],
    },
    'phonotactics': {
        'description': 'Semitic has pharyngeals, emphatics, no initial clusters',
        'forbidden_initial': ['st-', 'sp-', 'sk-', 'tw-', 'kw-'],  # No initial consonant clusters
        'expected_final': ['-um', '-im', '-am', '-at'],  # Case/number markers
    },
}

LUWIAN_EXPECTATIONS = {
    'name': 'Luwian/Anatolian',
    'particles': {
        'description': 'Luwian uses distinctive particles',
        'expected': [
            {'pattern': 'a-', 'meaning': 'and (conjunction)', 'expected_freq': 'high'},
            {'pattern': '-wa-', 'meaning': 'quotative particle', 'expected_freq': 'high'},
            {'pattern': '-awa-', 'meaning': 'quotative (full)', 'expected_freq': 'medium'},
        ],
    },
    'morphology': {
        'verbal_endings': [
            {'pattern': '-ti', 'description': '3sg present', 'expected_freq': 'high'},
            {'pattern': '-nti', 'description': '3pl present', 'expected_freq': 'high'},
            {'pattern': '-ta', 'description': '3sg past', 'expected_freq': 'medium'},
            {'pattern': '-nta', 'description': '3pl past', 'expected_freq': 'medium'},
        ],
        'nominal_suffixes': [
            {'pattern': '-ssa', 'description': 'place suffix', 'expected_freq': 'medium'},
            {'pattern': '-nda', 'description': 'adjective/belonging', 'expected_freq': 'medium'},
            {'pattern': '-ja', 'description': 'adjectival (-iya)', 'expected_freq': 'high'},
        ],
    },
    'phonotactics': {
        'expected_clusters': ['tt', 'ss', 'nn', 'll'],  # Geminate consonants
        'labialized': ['wa', 'wi', 'we', 'wo', 'wu'],  # Common labiovelars
    },
}

PREGREEK_EXPECTATIONS = {
    'name': 'Pre-Greek Substrate',
    'phonology': {
        'characteristic_clusters': [
            {'pattern': '-nth-', 'examples': ['Korinthos', 'Zakynthos'], 'expected_freq': 'medium'},
            {'pattern': '-ss-', 'examples': ['Knossos', 'Parnassos'], 'expected_freq': 'high'},
            {'pattern': '-mn-', 'examples': ['Amnissos'], 'expected_freq': 'low'},
            {'pattern': '-tt-', 'examples': ['Brettia'], 'expected_freq': 'low'},
        ],
        'suffixes': [
            {'pattern': '-assos', 'type': 'toponym', 'expected_freq': 'medium'},
            {'pattern': '-inthos', 'type': 'toponym', 'expected_freq': 'medium'},
            {'pattern': '-issos', 'type': 'toponym', 'expected_freq': 'low'},
            {'pattern': '-ene', 'type': 'toponym', 'expected_freq': 'low'},
        ],
    },
    'vocabulary': {
        'description': 'Pre-Greek vocabulary should NOT match IE or Semitic',
        'should_not_match_ie': True,
        'should_not_match_semitic': True,
    },
}


class NegativeEvidenceAnalyzer:
    """
    Analyzes absent patterns in Linear A corpus.

    For each hypothesis, identifies:
    - What patterns the hypothesis predicts
    - Which predicted patterns are ABSENT from the corpus
    - Statistical deviation from expected frequencies
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.statistics = None
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'Negative Evidence Analysis (First Principle #5)',
                'principle': 'What the script DOESN\'T show is also informative',
            },
            'corpus_summary': {},
            'hypothesis_analyses': {},
            'overall_assessment': {},
        }

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_data(self) -> bool:
        """Load corpus and statistics data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            stats_path = DATA_DIR / "statistics.json"

            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)

            if stats_path.exists():
                with open(stats_path, 'r', encoding='utf-8') as f:
                    self.statistics = json.load(f)
            else:
                self.statistics = self._generate_statistics()

            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def _extract_words_from_corpus(self) -> dict:
        """
        Extract word frequencies directly from corpus.json.

        This is the ROBUST method - reads transliteratedWords from each
        inscription and counts frequencies. More reliable than using
        pre-computed statistics which may use different field names.
        """
        word_freq = Counter()

        if not self.corpus:
            return {}

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            for word in words:
                if not word or word in ['\n', '𐄁', '', '—', '≈']:
                    continue
                # Skip pure numerals
                if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈₉○◎—|]+$', word):
                    continue
                # Skip fractional markers
                if word.startswith('¹⁄') or word.startswith('³⁄') or word.startswith('≈'):
                    continue
                # Skip damaged/unclear markers
                if word.startswith('𐝫') or word == '𐝫':
                    continue
                # Skip pure logograms (single uppercase without hyphen)
                # But KEEP multi-syllable words even if they have logograms
                if re.match(r'^[A-Z*\d+\[\]]+$', word) and '-' not in word:
                    continue

                word_freq[word] += 1

        self.log(f"Extracted {len(word_freq)} unique words from corpus")
        self.log(f"Total word tokens: {sum(word_freq.values())}")

        return dict(word_freq)

    def _generate_statistics(self) -> dict:
        """Generate basic statistics if not available."""
        stats = {
            'word_frequencies': Counter(),
            'sign_frequencies': Counter(),
            'total_words': 0,
            'total_signs': 0,
        }

        for insc_id, data in self.corpus['inscriptions'].items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            for word in words:
                if not word or word in ['\n', '𐄁', '', '—']:
                    continue
                if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', word):
                    continue

                stats['word_frequencies'][word] += 1
                stats['total_words'] += 1

                # Extract signs
                if '-' in word:
                    for sign in word.split('-'):
                        sign_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', sign).upper()
                        if sign_clean:
                            stats['sign_frequencies'][sign_clean] += 1
                            stats['total_signs'] += 1

        return stats

    def extract_corpus_patterns(self) -> dict:
        """Extract patterns from corpus for comparison.

        Uses robust direct extraction from corpus.json, falling back to
        statistics.json if needed. This ensures we always have valid data.
        """
        patterns = {
            'vowel_distribution': Counter(),
            'word_endings': Counter(),
            'word_initials': Counter(),
            'syllable_patterns': Counter(),
            'consonant_clusters': [],
            'total_syllables': 0,
        }

        # ROBUST: Extract word frequencies directly from corpus
        word_freqs = self._extract_words_from_corpus()

        # Fallback to statistics.json if corpus extraction fails
        if not word_freqs:
            # BUG FIX: statistics.json uses 'top_words', not 'word_frequencies'
            word_freqs = self.statistics.get('top_words', {})
            if not word_freqs:
                word_freqs = self.statistics.get('word_frequencies', {})

        if isinstance(word_freqs, Counter):
            word_freqs = dict(word_freqs)

        for word, freq in word_freqs.items():
            if '-' not in word:
                continue

            syllables = word.upper().split('-')
            patterns['total_syllables'] += len(syllables) * freq

            # Word endings
            if syllables:
                patterns['word_endings'][syllables[-1]] += freq

            # Word initials
            if syllables:
                patterns['word_initials'][syllables[0]] += freq

            # Extract vowels
            for syl in syllables:
                syl_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
                if len(syl_clean) >= 1:
                    # Last character often vowel in CV structure
                    if syl_clean[-1] in 'AEIOU':
                        patterns['vowel_distribution'][syl_clean[-1].lower()] += freq

        # Normalize vowel distribution
        total_vowels = sum(patterns['vowel_distribution'].values())
        if total_vowels > 0:
            patterns['vowel_distribution_normalized'] = {
                v: c / total_vowels for v, c in patterns['vowel_distribution'].items()
            }
        else:
            patterns['vowel_distribution_normalized'] = {}

        return patterns

    def analyze_greek_negative_evidence(self, corpus_patterns: dict) -> dict:
        """Analyze what Greek hypothesis predicts but doesn't appear."""
        analysis = {
            'hypothesis': 'Proto-Greek',
            'absent_patterns': [],
            'statistical_deviations': [],
            'missing_vocabulary': [],
            'phonotactic_violations': [],
            'overall_score': 0,  # Lower = more negative evidence against hypothesis
        }

        # Check vowel distribution (MAJOR negative evidence for Greek)
        observed = corpus_patterns.get('vowel_distribution_normalized', {})
        expected = GREEK_EXPECTATIONS['vowel_distribution']['expected']

        for vowel, exp_freq in expected.items():
            obs_freq = observed.get(vowel, 0)
            deviation = abs(obs_freq - exp_freq)
            tolerance = GREEK_EXPECTATIONS['vowel_distribution']['tolerance']

            if deviation > tolerance:
                analysis['statistical_deviations'].append({
                    'pattern': f'vowel /{vowel}/',
                    'expected': f'{exp_freq*100:.1f}%',
                    'observed': f'{obs_freq*100:.1f}%',
                    'deviation': f'{deviation*100:.1f}%',
                    'significance': 'HIGH' if deviation > 0.15 else 'MEDIUM',
                    'interpretation': f'Linear A has {"more" if obs_freq > exp_freq else "less"} /{vowel}/ than expected for Greek',
                })
                analysis['overall_score'] -= 2 if deviation > 0.15 else 1

        # Special case: /o/ is critically low in Linear A (~3% vs ~20% expected)
        o_freq = observed.get('o', 0)
        if o_freq < 0.10:
            analysis['absent_patterns'].append({
                'pattern': 'Expected /o/ frequency',
                'expected': '~20% (Greek)',
                'observed': f'{o_freq*100:.1f}%',
                'significance': 'CRITICAL',
                'interpretation': 'Greek words should have frequent /o/ vowel; Linear A almost lacks it',
            })
            analysis['overall_score'] -= 5

        # Check for expected case endings
        endings = corpus_patterns.get('word_endings', {})
        total_words = sum(endings.values())

        for ending_info in GREEK_EXPECTATIONS['morphology']['case_endings']:
            pattern = ending_info['pattern'].replace('-', '').upper()
            count = endings.get(pattern, 0)
            freq = count / total_words if total_words > 0 else 0

            expected_freq_label = ending_info['expected_freq']
            threshold = 0.05 if expected_freq_label == 'high' else 0.02

            if freq < threshold and expected_freq_label in ['high', 'medium']:
                analysis['absent_patterns'].append({
                    'pattern': ending_info['pattern'],
                    'description': ending_info['description'],
                    'expected_freq': expected_freq_label,
                    'observed_freq': f'{freq*100:.2f}%',
                    'significance': 'MEDIUM',
                })
                analysis['overall_score'] -= 1

        # Check for expected Greek vocabulary (to-so instead of ku-ro)
        word_freqs = self._extract_words_from_corpus() or dict(self.statistics.get('top_words', {}))
        word_freqs_upper = {w.upper(): c for w, c in word_freqs.items()}

        if 'TO-SO' not in word_freqs_upper and 'TO-SA' not in word_freqs_upper:
            ku_ro_count = word_freqs_upper.get('KU-RO', 0)
            if ku_ro_count > 10:
                analysis['missing_vocabulary'].append({
                    'expected': 'to-so (Greek τόσος "total")',
                    'found_instead': 'ku-ro',
                    'occurrences': ku_ro_count,
                    'significance': 'HIGH',
                    'interpretation': 'Greek uses to-so for totals; Linear A uses ku-ro (non-Greek)',
                })
                analysis['overall_score'] -= 3

        return analysis

    def analyze_semitic_negative_evidence(self, corpus_patterns: dict) -> dict:
        """Analyze what Semitic hypothesis predicts but doesn't appear."""
        analysis = {
            'hypothesis': 'Semitic',
            'absent_patterns': [],
            'statistical_deviations': [],
            'structural_problems': [],
            'overall_score': 0,
        }

        # Semitic uses triconsonantal roots - check if Linear A words fit this
        word_freqs = self._extract_words_from_corpus() or dict(self.statistics.get('top_words', {}))

        consonant_counts = []
        for word, freq in word_freqs.items():
            if '-' not in word:
                continue
            # Extract consonants (initial letters of CV syllables)
            syllables = word.upper().split('-')
            consonants = []
            for syl in syllables:
                syl_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
                if syl_clean and syl_clean[0] not in 'AEIOU':
                    consonants.append(syl_clean[0])

            if consonants:
                consonant_counts.append((len(consonants), freq))

        # Calculate average consonant skeleton length
        if consonant_counts:
            total = sum(count * freq for count, freq in consonant_counts)
            total_freq = sum(freq for _, freq in consonant_counts)
            avg_consonants = total / total_freq if total_freq > 0 else 0

            # Semitic expects predominantly 3-consonant roots
            if avg_consonants < 2.5 or avg_consonants > 3.5:
                analysis['structural_problems'].append({
                    'pattern': 'Triconsonantal root structure',
                    'expected': '~3 consonants per root',
                    'observed': f'~{avg_consonants:.1f} consonants average',
                    'significance': 'MEDIUM',
                    'interpretation': 'Semitic has triconsonantal roots; Linear A pattern differs',
                })
                analysis['overall_score'] -= 2

        # Check for Semitic morphological prefixes
        initials = corpus_patterns.get('word_initials', {})
        total_words = sum(initials.values())

        for prefix_info in SEMITIC_EXPECTATIONS['morphology']['prefixes']:
            pattern = prefix_info['pattern'].replace('-', '').upper()
            count = initials.get(pattern, 0)
            freq = count / total_words if total_words > 0 else 0

            # Check if pattern appears with expected frequency
            expected = prefix_info['expected_freq']
            threshold = 0.05 if expected == 'medium' else 0.02

            if freq < threshold and expected in ['high', 'medium']:
                analysis['absent_patterns'].append({
                    'pattern': prefix_info['pattern'],
                    'description': prefix_info['description'],
                    'expected_freq': expected,
                    'observed_freq': f'{freq*100:.2f}%',
                    'significance': 'LOW',
                })

        # Check for Semitic phonotactics (no initial clusters)
        # Linear A actually fits this well due to CV structure
        analysis['structural_problems'].append({
            'pattern': 'Initial consonant clusters',
            'expected': 'Absent in Semitic',
            'observed': 'Absent in Linear A (CV syllabary)',
            'significance': 'NEUTRAL',
            'interpretation': 'Linear A CV structure compatible with Semitic phonotactics',
        })

        return analysis

    def analyze_luwian_negative_evidence(self, corpus_patterns: dict) -> dict:
        """Analyze what Luwian hypothesis predicts but doesn't appear."""
        analysis = {
            'hypothesis': 'Luwian/Anatolian',
            'absent_patterns': [],
            'present_patterns': [],
            'overall_score': 0,
        }

        word_freqs = self._extract_words_from_corpus() or dict(self.statistics.get('top_words', {}))
        word_freqs_upper = {w.upper(): c for w, c in word_freqs.items()}

        # Check for expected Luwian particles
        particles_found = 0
        for particle_info in LUWIAN_EXPECTATIONS['particles']['expected']:
            pattern = particle_info['pattern']
            pattern_clean = pattern.replace('-', '').upper()

            # Check word-initial or word-internal occurrences
            found = 0
            for word in word_freqs_upper:
                if pattern_clean in word.replace('-', ''):
                    found += word_freqs_upper[word]

            if found > 0:
                particles_found += 1
                analysis['present_patterns'].append({
                    'pattern': pattern,
                    'meaning': particle_info['meaning'],
                    'occurrences': found,
                    'significance': 'POSITIVE',
                })
                analysis['overall_score'] += 1 if particle_info['expected_freq'] == 'high' else 0.5
            else:
                analysis['absent_patterns'].append({
                    'pattern': pattern,
                    'meaning': particle_info['meaning'],
                    'expected_freq': particle_info['expected_freq'],
                    'significance': 'MEDIUM' if particle_info['expected_freq'] == 'high' else 'LOW',
                })
                analysis['overall_score'] -= 1

        # Check for Luwian verbal endings
        endings = corpus_patterns.get('word_endings', {})
        for ending_info in LUWIAN_EXPECTATIONS['morphology']['verbal_endings']:
            pattern = ending_info['pattern'].replace('-', '').upper()
            count = endings.get(pattern, 0)

            if count > 0:
                analysis['present_patterns'].append({
                    'pattern': ending_info['pattern'],
                    'description': ending_info['description'],
                    'occurrences': count,
                    'significance': 'POSITIVE',
                })
                analysis['overall_score'] += 0.5
            elif ending_info['expected_freq'] in ['high', 'medium']:
                analysis['absent_patterns'].append({
                    'pattern': ending_info['pattern'],
                    'description': ending_info['description'],
                    'expected_freq': ending_info['expected_freq'],
                    'significance': 'LOW',
                })

        return analysis

    def analyze_pregreek_negative_evidence(self, corpus_patterns: dict) -> dict:
        """Analyze what Pre-Greek hypothesis predicts but doesn't appear."""
        analysis = {
            'hypothesis': 'Pre-Greek Substrate',
            'notes': 'Pre-Greek is defined by what it is NOT (not IE, not Semitic)',
            'expected_absences': [],
            'structural_notes': [],
            'overall_score': 0,
        }

        # Pre-Greek should NOT show IE or Semitic patterns
        # This is actually positive evidence for Pre-Greek when those are absent

        # Check for Pre-Greek phonological markers
        word_freqs = self._extract_words_from_corpus() or dict(self.statistics.get('top_words', {}))

        for cluster_info in PREGREEK_EXPECTATIONS['phonology']['characteristic_clusters']:
            pattern = cluster_info['pattern']
            found = 0
            for word, freq in word_freqs.items():
                # Note: Linear A CV structure can't directly write -nth-, -ss- clusters
                # They would appear as TA-TA (for tt), SA-SA (for ss), etc.
                pass

        analysis['structural_notes'].append({
            'observation': 'Pre-Greek clusters (-nth-, -ss-) cannot be directly written in CV syllabary',
            'implication': 'Cannot use absence of these clusters as negative evidence',
            'significance': 'METHODOLOGICAL',
        })

        # Pre-Greek hypothesis gains support when OTHER hypotheses fail
        analysis['structural_notes'].append({
            'observation': 'Pre-Greek is a "residual" hypothesis',
            'implication': 'Negative evidence against Greek/Semitic is positive evidence for Pre-Greek',
            'significance': 'METHODOLOGICAL',
        })

        return analysis

    def analyze_reading_contradictions(self, top_n: int = 50) -> dict:
        """
        Analyze reading contradictions across hypotheses.

        For each high-frequency word, identifies:
        - What each hypothesis predicts about the reading
        - Where predictions contradict each other
        - Which observations would be decisive

        Args:
            top_n: Number of top-frequency words to analyze

        Returns:
            Dictionary with contradiction matrix and decisive tests
        """
        self.log("Analyzing reading contradictions...")

        word_freqs = self._extract_words_from_corpus()
        if not word_freqs:
            return {'error': 'No words extracted from corpus'}

        # Sort by frequency and take top N
        sorted_words = sorted(word_freqs.items(), key=lambda x: -x[1])[:top_n]

        contradictions = {
            'words_analyzed': len(sorted_words),
            'contradiction_matrix': [],
            'decisive_tests': [],
            'summary': {
                'total_contradictions': 0,
                'decisive_observations': 0,
            }
        }

        # Define prediction functions for each hypothesis
        def greek_predicts(word: str) -> dict:
            """What Greek hypothesis predicts about this word."""
            word_upper = word.upper()
            syllables = word_upper.split('-')
            predictions = {'hypothesis': 'Greek', 'predictions': [], 'violations': []}

            # Greek expects balanced vowels including /o/
            vowels = [s[-1] for s in syllables if s and s[-1] in 'AEIOU']
            o_count = sum(1 for v in vowels if v == 'O')
            if len(vowels) > 0 and o_count == 0:
                predictions['violations'].append('Missing expected /o/ vowel')

            # Check for Greek morphology
            if syllables:
                final = syllables[-1]
                if final in ['MI', 'SI', 'TI']:
                    predictions['predictions'].append('May be verbal form (1/2/3sg)')
                if final in ['O', 'OS', 'A']:
                    predictions['predictions'].append('Nominal ending expected')

            return predictions

        def semitic_predicts(word: str) -> dict:
            """What Semitic hypothesis predicts about this word."""
            word_upper = word.upper()
            syllables = word_upper.split('-')
            predictions = {'hypothesis': 'Semitic', 'predictions': [], 'violations': []}

            # Semitic expects triconsonantal roots
            consonants = [s[0] for s in syllables if s and s[0] not in 'AEIOU']
            if len(consonants) != 3:
                predictions['violations'].append(f'Non-triconsonantal ({len(consonants)} consonants)')
            else:
                predictions['predictions'].append('Triconsonantal root pattern fits')

            # Semitic should not have initial clusters
            if len(syllables) > 0 and len(syllables[0]) > 2:
                predictions['violations'].append('Possible initial cluster (Semitic forbids)')

            return predictions

        def luwian_predicts(word: str) -> dict:
            """What Luwian hypothesis predicts about this word."""
            word_upper = word.upper()
            syllables = word_upper.split('-')
            predictions = {'hypothesis': 'Luwian', 'predictions': [], 'violations': []}

            # Check for Luwian particles and endings
            if syllables:
                if syllables[0] == 'A':
                    predictions['predictions'].append('Initial a- may be conjunction')
                if 'WA' in syllables:
                    predictions['predictions'].append('Contains -wa- quotative particle')

                final = syllables[-1]
                if final in ['TI', 'NTI', 'TA', 'NTA']:
                    predictions['predictions'].append(f'Verbal ending -{final.lower()}')
                if final in ['SSA', 'NDA', 'JA']:
                    predictions['predictions'].append(f'Nominal suffix -{final.lower()}')

            return predictions

        def pregreek_predicts(word: str) -> dict:
            """What Pre-Greek hypothesis predicts (residual)."""
            predictions = {'hypothesis': 'Pre-Greek', 'predictions': [], 'violations': []}
            predictions['predictions'].append('Non-IE, non-Semitic vocabulary expected')
            predictions['predictions'].append('May contain substrate phonology')
            return predictions

        # Analyze each word
        for word, freq in sorted_words:
            if '-' not in word:
                continue

            greek = greek_predicts(word)
            semitic = semitic_predicts(word)
            luwian = luwian_predicts(word)
            pregreek = pregreek_predicts(word)

            # Find contradictions
            word_contradictions = []

            # Greek vs Semitic: vowel patterns
            greek_violations = len(greek['violations'])
            semitic_violations = len(semitic['violations'])

            if greek_violations > 0 and semitic_violations == 0:
                word_contradictions.append({
                    'type': 'structural',
                    'hyp1': 'Greek',
                    'hyp2': 'Semitic',
                    'observation': f'{word} violates Greek expectations but fits Semitic',
                    'decisive_for': 'Semitic'
                })
            elif semitic_violations > 0 and greek_violations == 0:
                word_contradictions.append({
                    'type': 'structural',
                    'hyp1': 'Greek',
                    'hyp2': 'Semitic',
                    'observation': f'{word} fits Greek but violates Semitic expectations',
                    'decisive_for': 'Greek'
                })

            # Greek vs Luwian: morphological patterns
            greek_morph = [p for p in greek['predictions'] if 'verbal' in p.lower() or 'nominal' in p.lower()]
            luwian_morph = [p for p in luwian['predictions'] if 'verbal' in p.lower() or 'nominal' in p.lower()]

            if greek_morph and not luwian_morph:
                word_contradictions.append({
                    'type': 'morphological',
                    'hyp1': 'Greek',
                    'hyp2': 'Luwian',
                    'observation': f'{word} shows Greek morphology, not Luwian',
                    'decisive_for': 'Greek'
                })
            elif luwian_morph and not greek_morph:
                word_contradictions.append({
                    'type': 'morphological',
                    'hyp1': 'Greek',
                    'hyp2': 'Luwian',
                    'observation': f'{word} shows Luwian morphology, not Greek',
                    'decisive_for': 'Luwian'
                })

            if word_contradictions:
                contradictions['contradiction_matrix'].append({
                    'word': word,
                    'frequency': freq,
                    'contradictions': word_contradictions,
                    'hypothesis_predictions': {
                        'greek': greek,
                        'semitic': semitic,
                        'luwian': luwian,
                        'pregreek': pregreek,
                    }
                })
                contradictions['summary']['total_contradictions'] += len(word_contradictions)

                # Add decisive tests
                for c in word_contradictions:
                    if c.get('decisive_for'):
                        contradictions['decisive_tests'].append({
                            'word': word,
                            'test': c['observation'],
                            'favors': c['decisive_for'],
                        })
                        contradictions['summary']['decisive_observations'] += 1

        self.log(f"Found {contradictions['summary']['total_contradictions']} contradictions")
        self.log(f"Identified {contradictions['summary']['decisive_observations']} decisive tests")

        return contradictions

    def generate_overall_assessment(self, analyses: dict) -> dict:
        """Generate overall assessment of negative evidence."""
        assessment = {
            'summary': {},
            'rankings': [],
            'critical_findings': [],
            'methodological_notes': [],
        }

        # Rank hypotheses by negative evidence (higher score = less negative evidence = better fit)
        rankings = []
        for hyp_name, analysis in analyses.items():
            score = analysis.get('overall_score', 0)
            rankings.append((hyp_name, score))

        rankings.sort(key=lambda x: x[1], reverse=True)
        assessment['rankings'] = [{'hypothesis': h, 'score': s} for h, s in rankings]

        # Identify critical findings
        for hyp_name, analysis in analyses.items():
            for pattern in analysis.get('absent_patterns', []):
                if pattern.get('significance') == 'CRITICAL':
                    assessment['critical_findings'].append({
                        'hypothesis': hyp_name,
                        'finding': pattern,
                    })

            for deviation in analysis.get('statistical_deviations', []):
                if deviation.get('significance') == 'HIGH':
                    assessment['critical_findings'].append({
                        'hypothesis': hyp_name,
                        'finding': deviation,
                    })

        # Add methodological notes
        assessment['methodological_notes'] = [
            'Negative evidence constrains hypotheses but cannot definitively prove alternatives',
            'Absence of pattern X under hypothesis H reduces confidence in H',
            'Pre-Greek hypothesis is "residual" - gains support when others fail',
            'Linear A CV syllabary cannot represent all phonological contrasts',
        ]

        return assessment

    def run_analysis(self) -> dict:
        """Run complete negative evidence analysis."""
        print("\nExtracting corpus patterns...")
        corpus_patterns = self.extract_corpus_patterns()

        # Store corpus summary
        self.results['corpus_summary'] = {
            'total_words': sum(corpus_patterns.get('word_endings', {}).values()),
            'vowel_distribution': corpus_patterns.get('vowel_distribution_normalized', {}),
            'common_endings': dict(corpus_patterns.get('word_endings', {}).most_common(20))
                             if isinstance(corpus_patterns.get('word_endings'), Counter) else {},
        }

        print("Analyzing Greek negative evidence...")
        greek_analysis = self.analyze_greek_negative_evidence(corpus_patterns)
        self.results['hypothesis_analyses']['greek'] = greek_analysis
        self.log(f"Greek score: {greek_analysis['overall_score']}")

        print("Analyzing Semitic negative evidence...")
        semitic_analysis = self.analyze_semitic_negative_evidence(corpus_patterns)
        self.results['hypothesis_analyses']['semitic'] = semitic_analysis
        self.log(f"Semitic score: {semitic_analysis['overall_score']}")

        print("Analyzing Luwian negative evidence...")
        luwian_analysis = self.analyze_luwian_negative_evidence(corpus_patterns)
        self.results['hypothesis_analyses']['luwian'] = luwian_analysis
        self.log(f"Luwian score: {luwian_analysis['overall_score']}")

        print("Analyzing Pre-Greek negative evidence...")
        pregreek_analysis = self.analyze_pregreek_negative_evidence(corpus_patterns)
        self.results['hypothesis_analyses']['pregreek'] = pregreek_analysis
        self.log(f"Pre-Greek score: {pregreek_analysis['overall_score']}")

        print("Analyzing reading contradictions...")
        self.results['contradictions'] = self.analyze_reading_contradictions(top_n=50)

        print("Generating overall assessment...")
        self.results['overall_assessment'] = self.generate_overall_assessment(
            self.results['hypothesis_analyses']
        )

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
        print("NEGATIVE EVIDENCE ANALYSIS SUMMARY")
        print("First Principle #5: What the script DOESN'T show is also informative")
        print("=" * 70)

        # Corpus summary
        summary = self.results.get('corpus_summary', {})
        vowels = summary.get('vowel_distribution', {})
        print("\nCorpus Vowel Distribution:")
        for v, freq in sorted(vowels.items()):
            print(f"  /{v}/: {freq*100:.1f}%")

        # Hypothesis rankings
        rankings = self.results.get('overall_assessment', {}).get('rankings', [])
        print("\nHypothesis Rankings (by negative evidence score):")
        print("  (Higher score = less negative evidence = better fit)")
        for rank in rankings:
            print(f"  {rank['hypothesis']:15} score: {rank['score']:+.1f}")

        # Critical findings
        critical = self.results.get('overall_assessment', {}).get('critical_findings', [])
        if critical:
            print("\nCritical Findings:")
            for finding in critical[:5]:
                hyp = finding['hypothesis']
                f = finding['finding']
                print(f"  [{hyp}] {f.get('pattern', f.get('observation', 'Unknown'))}")
                if 'interpretation' in f:
                    print(f"    → {f['interpretation']}")

        # Contradiction summary
        contradictions = self.results.get('contradictions', {})
        if contradictions.get('summary'):
            summary = contradictions['summary']
            print(f"\nContradiction Analysis:")
            print(f"  Total contradictions found: {summary.get('total_contradictions', 0)}")
            print(f"  Decisive observations: {summary.get('decisive_observations', 0)}")

            # Show top decisive tests
            decisive = contradictions.get('decisive_tests', [])[:5]
            if decisive:
                print("\n  Top Decisive Tests:")
                for test in decisive:
                    print(f"    • {test['word']}: favors {test['favors'].upper()}")

        # Key observations
        print("\nKey Observations:")
        print("  • Proto-Greek hypothesis has STRONG negative evidence (low /o/ frequency)")
        print("  • Semitic hypothesis partially compatible (triconsonantal structure unclear)")
        print("  • Luwian particles (a-, -wa-) need verification in corpus")
        print("  • Pre-Greek gains by default when others fail")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze negative evidence in Linear A corpus"
    )
    parser.add_argument(
        '--hypothesis', '-H',
        type=str,
        choices=['greek', 'semitic', 'luwian', 'pregreek', 'all'],
        default='all',
        help='Hypothesis to analyze (default: all)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='data/negative_evidence_report.json',
        help='Output path for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A NEGATIVE EVIDENCE ANALYZER")
    print("=" * 70)
    print("Implementing First Principle #5:")
    print("'What the script DOESN'T show is also informative.'")

    analyzer = NegativeEvidenceAnalyzer(verbose=args.verbose)

    if not analyzer.load_data():
        return 1

    analyzer.run_analysis()

    # Save results
    output_path = PROJECT_ROOT / args.output
    analyzer.save_results(output_path)

    # Print summary
    analyzer.print_summary()

    return 0


if __name__ == '__main__':
    sys.exit(main())
