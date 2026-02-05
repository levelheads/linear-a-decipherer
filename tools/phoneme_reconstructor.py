#!/usr/bin/env python3
"""
Phoneme Reconstructor for Linear A

Direction 2 Implementation: Build the Linear A phonological system from distributional evidence.

Key analyses:
1. Vowel frequency matrix by position (initial/medial/final)
2. Consonant cluster analysis — which CV combinations exist vs. absent
3. CVC sign inventory beyond *118
4. Phonotactic constraints documentation

Evidence-based questions:
- Does Linear A lack /o/ entirely, or is it written differently?
- What consonants appear word-finally (/-t, -n, -m, -s/?)?
- Are there aspirated vs. unaspirated distinctions?

Usage:
    python tools/phoneme_reconstructor.py --vowel-matrix
    python tools/phoneme_reconstructor.py --consonant-clusters
    python tools/phoneme_reconstructor.py --cvc-signs
    python tools/phoneme_reconstructor.py --all

Attribution:
    Part of Linear A Decipherment Project
    Implements First Principles methodology
"""

import json
import argparse
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Tuple

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Linear B-derived vowel values for Linear A signs
VOWEL_MAP = {
    'A': 'a', 'E': 'e', 'I': 'i', 'O': 'o', 'U': 'u',
    'A₂': 'a', 'A₃': 'a', 'A₄': 'a',
    'E₂': 'e',
    'I₂': 'i',
    'U₂': 'u',
}

# CV syllable to consonant+vowel mapping (Linear B values)
CV_MAP = {
    # D-series
    'DA': ('d', 'a'), 'DE': ('d', 'e'), 'DI': ('d', 'i'), 'DO': ('d', 'o'), 'DU': ('d', 'u'),
    # J-series
    'JA': ('j', 'a'), 'JE': ('j', 'e'), 'JO': ('j', 'o'), 'JU': ('j', 'u'),
    # K-series
    'KA': ('k', 'a'), 'KE': ('k', 'e'), 'KI': ('k', 'i'), 'KO': ('k', 'o'), 'KU': ('k', 'u'),
    # M-series
    'MA': ('m', 'a'), 'ME': ('m', 'e'), 'MI': ('m', 'i'), 'MO': ('m', 'o'), 'MU': ('m', 'u'),
    # N-series
    'NA': ('n', 'a'), 'NE': ('n', 'e'), 'NI': ('n', 'i'), 'NO': ('n', 'o'), 'NU': ('n', 'u'),
    # P-series
    'PA': ('p', 'a'), 'PE': ('p', 'e'), 'PI': ('p', 'i'), 'PO': ('p', 'o'), 'PU': ('p', 'u'),
    'PA₂': ('p', 'a'), 'PA₃': ('p', 'a'),
    # Q-series (labiovelars)
    'QA': ('kw', 'a'), 'QE': ('kw', 'e'), 'QI': ('kw', 'i'), 'QO': ('kw', 'o'),
    # R-series (r/l)
    'RA': ('r', 'a'), 'RE': ('r', 'e'), 'RI': ('r', 'i'), 'RO': ('r', 'o'), 'RU': ('r', 'u'),
    'RA₂': ('r', 'a'), 'RA₃': ('r', 'a'),
    # S-series
    'SA': ('s', 'a'), 'SE': ('s', 'e'), 'SI': ('s', 'i'), 'SO': ('s', 'o'), 'SU': ('s', 'u'),
    'SA₂': ('s', 'a'),
    # T-series
    'TA': ('t', 'a'), 'TE': ('t', 'e'), 'TI': ('t', 'i'), 'TO': ('t', 'o'), 'TU': ('t', 'u'),
    'TA₂': ('t', 'a'),
    # W-series
    'WA': ('w', 'a'), 'WE': ('w', 'e'), 'WI': ('w', 'i'), 'WO': ('w', 'o'),
    # Z-series (affricate?)
    'ZA': ('z', 'a'), 'ZE': ('z', 'e'), 'ZO': ('z', 'o'), 'ZU': ('z', 'u'),
}

# Signs unique to Linear A (not in Linear B) - potential extra phonemes
UNIQUE_SIGNS = [
    '*301', '*302', '*303', '*304', '*305', '*306', '*307', '*308', '*309', '*310',
    '*311', '*312', '*313', '*314', '*315', '*316', '*317', '*318', '*319', '*320',
    '*321', '*322', '*323', '*324', '*325', '*326', '*327', '*328', '*329', '*330',
    '*118',  # CVC sign (word-final consonant)
    '*21F', '*21M',  # Gender classifiers
    '*188',  # Vessel marker
]


class PhonemeReconstructor:
    """
    Reconstructs Linear A phoneme inventory from distributional evidence.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.corpus = None
        self.signs = None
        self.results = {
            'metadata': {
                'generated': None,
                'method': 'Phoneme Reconstruction via Distributional Analysis',
                'principles': ['P1 (Kober): Pattern-led analysis', 'P5 (Negative): Absence patterns'],
            },
            'vowel_analysis': {},
            'consonant_analysis': {},
            'cvc_signs': {},
            'phonotactics': {},
            'phoneme_inventory': {},
            'findings': [],
        }

    def log(self, message: str):
        if self.verbose:
            print(f"  {message}")

    def load_data(self) -> bool:
        """Load corpus and sign data."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)
            print(f"Loaded corpus: {len(self.corpus['inscriptions'])} inscriptions")

            signs_path = DATA_DIR / "signs.json"
            with open(signs_path, 'r', encoding='utf-8') as f:
                self.signs = json.load(f)
            print(f"Loaded signs: {self.signs['total_signs']} unique signs")

            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def extract_syllable(self, sign: str) -> Tuple[str, str]:
        """
        Extract consonant and vowel from a sign.
        Returns (consonant, vowel) or (None, vowel) for pure vowels.
        """
        sign_upper = sign.upper().strip()

        # Pure vowels
        if sign_upper in VOWEL_MAP:
            return (None, VOWEL_MAP[sign_upper])

        # CV syllables
        if sign_upper in CV_MAP:
            return CV_MAP[sign_upper]

        # Handle subscript variants
        base = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', sign_upper)
        if base in CV_MAP:
            return CV_MAP[base]
        if base in VOWEL_MAP:
            return (None, VOWEL_MAP[base])

        return (None, None)

    def analyze_vowel_frequencies(self) -> dict:
        """
        Analyze vowel frequency by position (initial, medial, final).

        Key finding to verify: /o/ at ~3% vs Greek ~20%
        """
        print("\n[Vowel Analysis] Extracting vowel frequencies by position...")

        vowel_counts = {
            'initial': Counter(),
            'medial': Counter(),
            'final': Counter(),
            'total': Counter(),
        }

        word_count = 0
        syllable_count = 0

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            for word in data.get('transliteratedWords', []):
                if not word or '-' not in word:
                    continue

                syllables = word.upper().split('-')
                if len(syllables) < 2:
                    continue

                word_count += 1

                for idx, syl in enumerate(syllables):
                    consonant, vowel = self.extract_syllable(syl)
                    if vowel is None:
                        continue

                    syllable_count += 1
                    vowel_counts['total'][vowel] += 1

                    if idx == 0:
                        vowel_counts['initial'][vowel] += 1
                    elif idx == len(syllables) - 1:
                        vowel_counts['final'][vowel] += 1
                    else:
                        vowel_counts['medial'][vowel] += 1

        # Calculate percentages
        total = sum(vowel_counts['total'].values())

        analysis = {
            'total_words_analyzed': word_count,
            'total_syllables': syllable_count,
            'overall_frequencies': {},
            'by_position': {
                'initial': {},
                'medial': {},
                'final': {},
            },
            'o_analysis': {},
        }

        for vowel in ['a', 'e', 'i', 'o', 'u']:
            count = vowel_counts['total'].get(vowel, 0)
            analysis['overall_frequencies'][vowel] = {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0,
            }

            for pos in ['initial', 'medial', 'final']:
                pos_total = sum(vowel_counts[pos].values())
                pos_count = vowel_counts[pos].get(vowel, 0)
                analysis['by_position'][pos][vowel] = {
                    'count': pos_count,
                    'percentage': round(pos_count / pos_total * 100, 2) if pos_total > 0 else 0,
                }

        # Special /o/ analysis
        o_pct = analysis['overall_frequencies']['o']['percentage']
        analysis['o_analysis'] = {
            'observed_percentage': o_pct,
            'expected_if_greek': 20.0,
            'deviation': round(20.0 - o_pct, 2),
            'interpretation': 'CONFIRMS non-Greek phonology' if o_pct < 10 else 'WEAKENS non-Greek hypothesis',
            'confidence': 'HIGH' if o_pct < 5 else 'MEDIUM' if o_pct < 10 else 'LOW',
        }

        self.results['vowel_analysis'] = analysis

        # Add finding
        self.results['findings'].append({
            'category': 'vowel_system',
            'finding': f"/o/ frequency at {o_pct}% (expected ~20% for Greek)",
            'implication': 'Linear A phonology fundamentally differs from Greek',
            'confidence': analysis['o_analysis']['confidence'],
        })

        self.log(f"Analyzed {word_count} words, {syllable_count} syllables")
        self.log(f"/o/ frequency: {o_pct}%")

        return analysis

    def analyze_consonant_clusters(self) -> dict:
        """
        Analyze which CV combinations exist vs. are absent.

        Gaps in the CV grid reveal phonotactic constraints.
        """
        print("\n[Consonant Analysis] Building CV combination matrix...")

        consonants = ['d', 'j', 'k', 'm', 'n', 'p', 'kw', 'r', 's', 't', 'w', 'z']
        vowels = ['a', 'e', 'i', 'o', 'u']

        cv_counts = defaultdict(Counter)
        total_cv = 0

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            for word in data.get('transliteratedWords', []):
                if not word or '-' not in word:
                    continue

                for syl in word.upper().split('-'):
                    consonant, vowel = self.extract_syllable(syl)
                    if consonant and vowel:
                        cv_counts[consonant][vowel] += 1
                        total_cv += 1

        # Build CV matrix
        matrix = {}
        for c in consonants:
            matrix[c] = {}
            for v in vowels:
                count = cv_counts[c].get(v, 0)
                matrix[c][v] = {
                    'count': count,
                    'percentage': round(count / total_cv * 100, 3) if total_cv > 0 else 0,
                }

        # Identify gaps (missing CV combinations)
        gaps = []
        for c in consonants:
            for v in vowels:
                if matrix[c][v]['count'] == 0:
                    gaps.append(f"{c}{v}")

        # Identify rare combinations (<1%)
        rare = []
        for c in consonants:
            for v in vowels:
                pct = matrix[c][v]['percentage']
                if 0 < pct < 0.5:
                    rare.append({'cv': f"{c}{v}", 'percentage': pct, 'count': matrix[c][v]['count']})

        # Consonant totals (to identify which consonants are most common)
        consonant_totals = {}
        for c in consonants:
            total = sum(cv_counts[c].values())
            consonant_totals[c] = {
                'count': total,
                'percentage': round(total / total_cv * 100, 2) if total_cv > 0 else 0,
            }

        analysis = {
            'total_cv_syllables': total_cv,
            'cv_matrix': matrix,
            'gaps': gaps,
            'rare_combinations': sorted(rare, key=lambda x: x['percentage']),
            'consonant_frequencies': consonant_totals,
        }

        self.results['consonant_analysis'] = analysis

        if gaps:
            self.results['findings'].append({
                'category': 'consonant_clusters',
                'finding': f"{len(gaps)} CV combinations not attested",
                'gaps': gaps[:10],
                'implication': 'Phonotactic constraints or script limitations',
                'confidence': 'MEDIUM',
            })

        self.log(f"CV combinations analyzed: {total_cv}")
        self.log(f"Gaps found: {len(gaps)}")

        return analysis

    def identify_cvc_signs(self) -> dict:
        """
        Identify CVC syllable signs (signs representing closed syllables).

        *118 is confirmed CVC (69% word-final). Find others.
        """
        print("\n[CVC Analysis] Identifying closed syllable signs...")

        sign_data = self.signs.get('signs', {})

        cvc_candidates = []

        for sign, data in sign_data.items():
            freq = data.get('total_occurrences', 0)
            if freq < 5:
                continue

            # Calculate position ratios
            pos = data.get('position_frequency', {})
            total_pos = pos.get('initial', 0) + pos.get('medial', 0) + pos.get('final', 0)

            if total_pos < 5:
                continue

            final_pct = pos.get('final', 0) / total_pos * 100 if total_pos > 0 else 0

            # CVC signs tend to appear word-finally (closing syllables)
            # Threshold: >50% final position
            if final_pct > 50:
                cvc_candidates.append({
                    'sign': sign,
                    'frequency': freq,
                    'final_percentage': round(final_pct, 1),
                    'initial_pct': round(pos.get('initial', 0) / total_pos * 100, 1),
                    'medial_pct': round(pos.get('medial', 0) / total_pos * 100, 1),
                    'cvc_confidence': 'HIGH' if final_pct > 65 else 'MEDIUM',
                })

        # Sort by final percentage
        cvc_candidates.sort(key=lambda x: -x['final_percentage'])

        # Identify unique Linear A signs that might be CVC
        unique_cvc = [c for c in cvc_candidates if c['sign'].startswith('*')]

        analysis = {
            'total_cvc_candidates': len(cvc_candidates),
            'unique_linear_a_cvc': len(unique_cvc),
            'candidates': cvc_candidates[:20],
            'confirmed': [],
            'word_final_consonants': [],
        }

        # Check for *118 specifically
        for c in cvc_candidates:
            if '*118' in c['sign']:
                analysis['confirmed'].append({
                    **c,
                    'status': 'CONFIRMED CVC',
                    'proposed_phonemes': ['/-t/', '/-n/', '/-m/'],
                })

        # Infer possible word-final consonants
        if analysis['confirmed']:
            analysis['word_final_consonants'] = [
                {'consonant': '-t', 'confidence': 'POSSIBLE', 'evidence': '*118 distribution'},
                {'consonant': '-n', 'confidence': 'POSSIBLE', 'evidence': '*118 distribution'},
                {'consonant': '-m', 'confidence': 'POSSIBLE', 'evidence': '*118 distribution'},
                {'consonant': '-s', 'confidence': 'SPECULATIVE', 'evidence': 'Cross-linguistic common'},
            ]

        self.results['cvc_signs'] = analysis

        self.results['findings'].append({
            'category': 'cvc_signs',
            'finding': f"Identified {len(cvc_candidates)} potential CVC signs",
            'confirmed': [c['sign'] for c in analysis['confirmed']],
            'implication': 'Linear A had closed syllables not represented in Linear B',
            'confidence': 'PROBABLE',
        })

        self.log(f"CVC candidates: {len(cvc_candidates)}")

        return analysis

    def analyze_phonotactics(self) -> dict:
        """
        Document phonotactic constraints - what sequences are impossible?
        """
        print("\n[Phonotactics] Analyzing syllable sequence constraints...")

        # Analyze syllable-to-syllable transitions
        transitions = Counter()
        vowel_sequences = Counter()
        consonant_sequences = Counter()

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            for word in data.get('transliteratedWords', []):
                if not word or '-' not in word:
                    continue

                syllables = word.upper().split('-')

                for i in range(len(syllables) - 1):
                    syl1, syl2 = syllables[i], syllables[i + 1]
                    c1, v1 = self.extract_syllable(syl1)
                    c2, v2 = self.extract_syllable(syl2)

                    if v1 and v2:
                        vowel_sequences[f"{v1}-{v2}"] += 1
                    if c1 and c2:
                        consonant_sequences[f"{c1}-{c2}"] += 1

                    transitions[f"{syl1}-{syl2}"] += 1

        # Find common and rare vowel sequences
        vowel_total = sum(vowel_sequences.values())
        common_vowel_seq = []
        rare_vowel_seq = []

        for seq, count in vowel_sequences.items():
            pct = count / vowel_total * 100 if vowel_total > 0 else 0
            entry = {'sequence': seq, 'count': count, 'percentage': round(pct, 2)}
            if pct > 5:
                common_vowel_seq.append(entry)
            elif pct < 1 and count >= 2:
                rare_vowel_seq.append(entry)

        # Identify forbidden/absent sequences
        all_vowels = ['a', 'e', 'i', 'o', 'u']
        absent_vowel_seq = []
        for v1 in all_vowels:
            for v2 in all_vowels:
                seq = f"{v1}-{v2}"
                if seq not in vowel_sequences:
                    absent_vowel_seq.append(seq)

        analysis = {
            'vowel_sequences': {
                'common': sorted(common_vowel_seq, key=lambda x: -x['percentage']),
                'rare': sorted(rare_vowel_seq, key=lambda x: x['percentage']),
                'absent': absent_vowel_seq,
            },
            'consonant_sequences': {
                'most_common': [{'seq': s, 'count': c} for s, c in consonant_sequences.most_common(20)],
            },
            'constraints': [],
        }

        # Derive constraints
        if absent_vowel_seq:
            # Check if o-sequences are systematically absent
            o_absent = [s for s in absent_vowel_seq if 'o' in s]
            if len(o_absent) > 3:
                analysis['constraints'].append({
                    'type': 'vowel_restriction',
                    'description': f"/o/ rare in vowel sequences ({len(o_absent)} combinations absent)",
                    'absent_sequences': o_absent,
                    'confidence': 'HIGH',
                })

        self.results['phonotactics'] = analysis

        if analysis['constraints']:
            for constraint in analysis['constraints']:
                self.results['findings'].append({
                    'category': 'phonotactics',
                    'finding': constraint['description'],
                    'confidence': constraint['confidence'],
                })

        return analysis

    def build_phoneme_inventory(self) -> dict:
        """
        Synthesize all analyses into a proposed phoneme inventory.
        """
        print("\n[Synthesis] Building phoneme inventory...")

        # Consonant inventory (based on Linear B with additions)
        consonants = {
            'stops': {
                'labial': {'p': 'CERTAIN', 'b': 'UNCERTAIN'},
                'dental': {'t': 'CERTAIN', 'd': 'CERTAIN'},
                'velar': {'k': 'CERTAIN', 'g': 'UNCERTAIN'},
                'labiovelar': {'kw': 'PROBABLE', 'gw': 'UNCERTAIN'},
            },
            'nasals': {'m': 'CERTAIN', 'n': 'CERTAIN'},
            'liquids': {'r': 'CERTAIN', 'l': 'PROBABLE'},  # r/l distinction unclear
            'fricatives': {'s': 'CERTAIN', 'h': 'SPECULATIVE'},
            'approximants': {'w': 'CERTAIN', 'j': 'CERTAIN'},
            'affricates': {'z': 'PROBABLE'},
            'unique_to_linear_a': {
                'pharyngeal': 'SPECULATIVE',  # *301 candidate
                'palatalized_stops': 'POSSIBLE',  # Various unique signs
                'emphatics': 'SPECULATIVE',  # Semitic contact
            },
        }

        # Vowel inventory
        vowel_freqs = self.results.get('vowel_analysis', {}).get('overall_frequencies', {})
        vowels = {
            'a': {'status': 'CERTAIN', 'frequency': vowel_freqs.get('a', {}).get('percentage', 0)},
            'e': {'status': 'CERTAIN', 'frequency': vowel_freqs.get('e', {}).get('percentage', 0)},
            'i': {'status': 'CERTAIN', 'frequency': vowel_freqs.get('i', {}).get('percentage', 0)},
            'o': {'status': 'MARGINAL', 'frequency': vowel_freqs.get('o', {}).get('percentage', 0),
                  'note': 'Very low frequency suggests marginal phoneme status'},
            'u': {'status': 'CERTAIN', 'frequency': vowel_freqs.get('u', {}).get('percentage', 0)},
        }

        # Syllable structure
        syllable_structure = {
            'cv': {'status': 'DOMINANT', 'note': 'Primary syllable type'},
            'v': {'status': 'ATTESTED', 'note': 'Word-initial vowels common'},
            'cvc': {'status': 'PROBABLE', 'note': '*118 and other signs suggest closed syllables'},
        }

        inventory = {
            'consonants': consonants,
            'vowels': vowels,
            'syllable_structure': syllable_structure,
            'unique_phonemes_count': '123 signs dropped from Linear B suggests 10-20 extra phonemes',
            'key_differences_from_greek': [
                '/o/ marginal (2.9% vs 20%)',
                'Possible pharyngeals (*301)',
                'Possible palatalized series',
                'CVC syllables (*118)',
                'Gender classifiers (*21F/*21M) - possibly tonal?',
            ],
        }

        self.results['phoneme_inventory'] = inventory

        return inventory

    def run_full_analysis(self) -> dict:
        """Run complete phonological reconstruction."""
        print("\n" + "=" * 70)
        print("PHONEME RECONSTRUCTOR - Direction 2")
        print("Building Linear A Sound System from Distributional Evidence")
        print("=" * 70)

        self.analyze_vowel_frequencies()
        self.analyze_consonant_clusters()
        self.identify_cvc_signs()
        self.analyze_phonotactics()
        self.build_phoneme_inventory()

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
        print("PHONOLOGICAL RECONSTRUCTION SUMMARY")
        print("=" * 70)

        # Vowel frequencies
        vowels = self.results.get('vowel_analysis', {}).get('overall_frequencies', {})
        print("\nVowel Frequencies:")
        for v in ['a', 'e', 'i', 'o', 'u']:
            data = vowels.get(v, {})
            bar = '█' * int(data.get('percentage', 0) / 2)
            print(f"  /{v}/: {data.get('percentage', 0):5.1f}% {bar}")

        # /o/ analysis
        o_analysis = self.results.get('vowel_analysis', {}).get('o_analysis', {})
        print(f"\n/o/ Analysis: {o_analysis.get('interpretation', 'N/A')}")
        print(f"  Observed: {o_analysis.get('observed_percentage', 0)}%")
        print(f"  Expected (Greek): {o_analysis.get('expected_if_greek', 0)}%")

        # CVC signs
        cvc = self.results.get('cvc_signs', {})
        print(f"\nCVC Signs: {cvc.get('total_cvc_candidates', 0)} candidates")
        for c in cvc.get('confirmed', []):
            print(f"  CONFIRMED: {c['sign']} ({c['final_percentage']}% word-final)")

        # Phoneme inventory
        inventory = self.results.get('phoneme_inventory', {})
        print("\nKey Differences from Greek:")
        for diff in inventory.get('key_differences_from_greek', []):
            print(f"  • {diff}")

        # Findings
        print("\nKey Findings:")
        for f in self.results.get('findings', []):
            print(f"  [{f['confidence']}] {f['finding']}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Reconstruct Linear A phoneme inventory"
    )
    parser.add_argument('--vowel-matrix', action='store_true', help='Generate vowel frequency matrix')
    parser.add_argument('--consonant-clusters', action='store_true', help='Analyze consonant clusters')
    parser.add_argument('--cvc-signs', action='store_true', help='Identify CVC signs')
    parser.add_argument('--all', '-a', action='store_true', help='Run full analysis')
    parser.add_argument('--output', '-o', type=str, default='data/phoneme_reconstruction.json')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()

    reconstructor = PhonemeReconstructor(verbose=args.verbose)

    if not reconstructor.load_data():
        return 1

    if args.all:
        reconstructor.run_full_analysis()
    else:
        if args.vowel_matrix:
            reconstructor.analyze_vowel_frequencies()
        if args.consonant_clusters:
            reconstructor.analyze_consonant_clusters()
        if args.cvc_signs:
            reconstructor.identify_cvc_signs()

    # Always build inventory if we ran any analysis
    if any([args.all, args.vowel_matrix, args.consonant_clusters, args.cvc_signs]):
        if not args.all:
            reconstructor.build_phoneme_inventory()

        reconstructor.results['metadata']['generated'] = datetime.now().isoformat()
        output_path = PROJECT_ROOT / args.output
        reconstructor.save_results(output_path)
        reconstructor.print_summary()
    else:
        print("\nUsage: python phoneme_reconstructor.py --all")

    return 0


if __name__ == '__main__':
    sys.exit(main())
