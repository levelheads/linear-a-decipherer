#!/usr/bin/env python3
"""
Personal Name Analyzer for Linear A

Analyzes Linear A anthroponyms (personal names) to:
1. Detect words likely to be personal names based on context
2. Classify names by morphological patterns
3. Compare to known Bronze Age naming conventions
4. Test name morphology against linguistic hypotheses

Personal names are estimated to constitute 50%+ of Linear A vocabulary
but are currently 0% deciphered. This tool addresses that gap.

Detection heuristics:
- Words in "recipient" slot before logograms
- Theophoric elements (deity name + suffix)
- Known Near Eastern naming patterns
- High-frequency words not fitting administrative vocabulary

Usage:
    python tools/personal_name_analyzer.py --extract
    python tools/personal_name_analyzer.py --analyze DA-MA-TE
    python tools/personal_name_analyzer.py --all

Attribution:
    Part of Linear A Decipherment Project (OPERATION MINOS II)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
NAMES_FILE = DATA_DIR / "personal_names.json"


# Known administrative terms (NOT personal names)
ADMINISTRATIVE_TERMS = {
    'KU-RO', 'KI-RO', 'SA-RA₂', 'DA-RE', 'TE', 'PO-TO-KU-RO',
    'A-DU', 'KU-PA₃-NU', 'SI-RU-TE', 'I-PI-NA-MA',
}

# Known toponyms (NOT personal names)
TOPONYMS = {
    'PA-I-TO',  # Phaistos
    'KU-DO-NI-JA',  # Kydonia
    'SU-KI-RI-TA',  # Sybrita
    'SE-TO-I-JA',
}

# Likely theophoric elements (deity name components)
THEOPHORIC_ELEMENTS = {
    'A-TA-NA': 'Athena-related',
    'A-SI': 'Possibly Asiatic deity',
    'DI': 'Possibly Zeus (Di-/Diwos)',
    'JA': 'Divine suffix?',
    'MA': 'Mother-related',
    'DA': 'Possibly Dameter/Demeter',
    'PO': 'Possibly Poseidon',
}

# Suffix patterns by linguistic hypothesis
NAME_SUFFIX_PATTERNS = {
    'luwian': {
        '-WA': {'meaning': 'Agent/possessive suffix', 'examples': ['Tarḫunawa', 'Muwawa']},
        '-MU-WA': {'meaning': 'Name-forming suffix', 'examples': ['Arnumawa', 'Šuppiluliumaš']},
        '-ZI-TI': {'meaning': 'Living/belonging to', 'examples': ['Muwaziti', 'Piyamaziti']},
        '-A-TA': {'meaning': 'Affiliation suffix', 'examples': []},
        '-SA': {'meaning': 'Possessive', 'examples': []},
    },
    'semitic': {
        '-U': {'meaning': 'Nominative masculine', 'examples': ['Ḫammurabi', 'Zimri-Lim']},
        '-A': {'meaning': 'Feminine/status', 'examples': []},
        '-I': {'meaning': 'Nisbe adjective/origin', 'examples': ['Ṣidqi', 'Abdi']},
        '-EL': {'meaning': 'Theophoric (God)', 'examples': ['Israel', 'Gabriel']},
        '-BA-AL': {'meaning': 'Theophoric (Baal)', 'examples': []},
        '-YA': {'meaning': 'Theophoric (Yahweh)', 'examples': []},
    },
    'pregreek': {
        '-NTH': {'meaning': 'Pre-Greek suffix', 'examples': ['Korinth-', 'Amarynth-']},
        '-SS': {'meaning': 'Pre-Greek suffix', 'examples': ['Odyss-', 'Parnass-']},
        '-NA': {'meaning': 'Feminine/place suffix', 'examples': ['Athena', 'Mykena']},
        '-NE': {'meaning': 'Variant of -NA', 'examples': []},
    },
    'greek': {
        '-OS': {'meaning': 'Masculine nominative', 'examples': ['Odysseus', 'Menelaos']},
        '-ES': {'meaning': 'Masculine nominative', 'examples': ['Achilles', 'Herakles']},
        '-AS': {'meaning': 'Masculine nominative', 'examples': ['Aeneas', 'Anchises']},
        '-E': {'meaning': 'Vocative/feminine', 'examples': ['Penelope', 'Hekabe']},
        '-A': {'meaning': 'Feminine nominative', 'examples': ['Helena', 'Elektra']},
    },
}


@dataclass
class PersonalName:
    """A word identified as a likely personal name."""
    word: str
    occurrences: int
    sites: List[str]
    contexts: List[Dict]

    # Detection metrics
    name_probability: float  # 0-1: likelihood this is a personal name
    detection_reason: str

    # Morphological analysis
    root: str
    suffixes: List[str]
    prefixes: List[str]

    # Hypothesis fit
    luwian_fit: Dict
    semitic_fit: Dict
    pregreek_fit: Dict
    greek_fit: Dict
    best_hypothesis: str

    # Classification
    name_type: str  # theophoric, patronymic, occupational, descriptive, unknown
    gender_guess: str  # masculine, feminine, unknown

    # Related names
    possible_variants: List[str]
    similar_names: List[str]


class PersonalNameAnalyzer:
    """
    Analyzes Linear A corpus for personal names.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = None
        self.word_contexts: Dict[str, List[Dict]] = defaultdict(list)
        self.word_frequencies: Dict[str, int] = {}
        self.detected_names: Dict[str, PersonalName] = {}

    def log(self, message: str):
        """Print if verbose mode."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        try:
            with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)

            self._extract_word_contexts()
            self.log(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _extract_word_contexts(self):
        """Extract all words with their contexts."""
        word_freq = Counter()

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            site_match = re.match(r'^([A-Z]+)', insc_id)
            site = site_match.group(1) if site_match else 'UNKNOWN'

            for i, word in enumerate(words):
                if not word or '-' not in word:
                    continue

                # Skip numerals and pure logograms
                if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', word):
                    continue
                if re.match(r'^[A-Z*\d+\[\]]+$', word) and '-' not in word:
                    continue

                word_upper = word.upper()
                word_freq[word_upper] += 1

                # Extract context
                before = [words[j] for j in range(max(0, i-2), i) if words[j]]
                after = [words[j] for j in range(i+1, min(len(words), i+3)) if words[j]]

                # Determine if followed by logogram or number
                followed_by_logogram = any(
                    re.match(r'^[A-Z]+$', w) and len(w) >= 2
                    for w in after
                )
                followed_by_number = any(
                    re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/]+$', w)
                    for w in after
                )

                self.word_contexts[word_upper].append({
                    'inscription': insc_id,
                    'site': site,
                    'position': i,
                    'before': before,
                    'after': after,
                    'followed_by_logogram': followed_by_logogram,
                    'followed_by_number': followed_by_number,
                })

        self.word_frequencies = dict(word_freq)

    def detect_personal_names(self, min_frequency: int = 2) -> Dict[str, PersonalName]:
        """
        Detect words likely to be personal names.

        Detection criteria:
        1. Appears before logogram + number (recipient pattern)
        2. Multi-syllable (names tend to be 2-4 syllables)
        3. Not a known administrative term or toponym
        4. Consistent context across occurrences
        """
        candidates = {}

        for word, contexts in self.word_contexts.items():
            freq = self.word_frequencies.get(word, 0)
            if freq < min_frequency:
                continue

            # Skip known non-names
            if word in ADMINISTRATIVE_TERMS or word in TOPONYMS:
                continue

            # Skip single syllables
            syllables = word.split('-')
            if len(syllables) < 2:
                continue

            # Calculate name probability
            name_prob, reason = self._calculate_name_probability(word, contexts)

            if name_prob >= 0.3:  # Threshold for likely name
                sites = list(set(c['site'] for c in contexts))

                # Morphological analysis
                root, prefixes, suffixes = self._analyze_morphology(word)

                # Hypothesis testing
                luwian_fit = self._test_luwian_name(word, suffixes)
                semitic_fit = self._test_semitic_name(word, suffixes)
                pregreek_fit = self._test_pregreek_name(word, suffixes)
                greek_fit = self._test_greek_name(word, suffixes)

                # Find best hypothesis
                fits = {
                    'luwian': luwian_fit.get('score', 0),
                    'semitic': semitic_fit.get('score', 0),
                    'pregreek': pregreek_fit.get('score', 0),
                    'greek': greek_fit.get('score', 0),
                }
                best_hyp = max(fits.keys(), key=lambda k: fits[k])

                # Determine name type
                name_type = self._classify_name_type(word, syllables)

                # Guess gender
                gender = self._guess_gender(word, suffixes)

                # Find variants
                variants = self._find_variants(word)
                similar = self._find_similar_names(word, list(self.word_frequencies.keys()))

                name = PersonalName(
                    word=word,
                    occurrences=freq,
                    sites=sites,
                    contexts=contexts[:5],  # Limit for storage
                    name_probability=name_prob,
                    detection_reason=reason,
                    root=root,
                    suffixes=suffixes,
                    prefixes=prefixes,
                    luwian_fit=luwian_fit,
                    semitic_fit=semitic_fit,
                    pregreek_fit=pregreek_fit,
                    greek_fit=greek_fit,
                    best_hypothesis=best_hyp if fits[best_hyp] > 0 else 'unknown',
                    name_type=name_type,
                    gender_guess=gender,
                    possible_variants=variants,
                    similar_names=similar,
                )

                candidates[word] = name
                self.log(f"Detected name: {word} (prob={name_prob:.2f}, {reason})")

        self.detected_names = candidates
        return candidates

    def _calculate_name_probability(self, word: str, contexts: List[Dict]) -> Tuple[float, str]:
        """
        Calculate probability that a word is a personal name.

        Returns (probability, reason).
        """
        prob = 0.0
        reasons = []

        # Factor 1: Appears before logogram + number (recipient pattern)
        recipient_count = sum(1 for c in contexts
                            if c['followed_by_logogram'] and c['followed_by_number'])
        if recipient_count > 0:
            recipient_ratio = recipient_count / len(contexts)
            prob += min(0.4, recipient_ratio * 0.5)
            if recipient_ratio > 0.3:
                reasons.append(f"recipient pattern ({recipient_count}/{len(contexts)})")

        # Factor 2: Multi-syllable (names tend to be 2-4 syllables)
        syllables = word.split('-')
        if 2 <= len(syllables) <= 5:
            prob += 0.15
            reasons.append(f"{len(syllables)} syllables")

        # Factor 3: Low frequency (rare names) or moderate frequency (common names)
        freq = self.word_frequencies.get(word, 0)
        if 2 <= freq <= 10:
            prob += 0.1
            reasons.append(f"frequency {freq}")

        # Factor 4: Contains theophoric element
        for elem in THEOPHORIC_ELEMENTS:
            if elem in word:
                prob += 0.2
                reasons.append(f"theophoric element {elem}")
                break

        # Factor 5: Consistent site pattern (names may be site-specific)
        sites = set(c['site'] for c in contexts)
        if len(sites) == 1 and len(contexts) >= 2:
            prob += 0.1
            reasons.append(f"site-specific ({list(sites)[0]})")

        # Factor 6: Name-like suffixes
        if word.endswith(('-JA', '-WA', '-TI', '-SI', '-TE', '-NE', '-RI')):
            prob += 0.15
            reasons.append("name-like suffix")

        reason = "; ".join(reasons) if reasons else "no strong indicators"
        return min(1.0, prob), reason

    def _analyze_morphology(self, word: str) -> Tuple[str, List[str], List[str]]:
        """
        Analyze morphological structure of a name.

        Returns (root, prefixes, suffixes).
        """
        syllables = word.split('-')

        if len(syllables) < 2:
            return word, [], []

        # Common prefix patterns
        prefixes = []
        if syllables[0] in ['A', 'I', 'U', 'E']:
            prefixes.append(syllables[0])
            syllables = syllables[1:]

        # Common suffix patterns
        suffixes = []
        suffix_candidates = ['-JA', '-WA', '-TI', '-SI', '-TE', '-NE', '-RI', '-U', '-A', '-I']

        for suffix in suffix_candidates:
            if word.endswith(suffix):
                suffixes.append(suffix[1:])  # Remove leading dash
                break

        # Root is what remains
        if suffixes:
            root_end = len(syllables) - 1
            root = '-'.join(syllables[:root_end])
        else:
            root = '-'.join(syllables)

        return root, prefixes, suffixes

    def _test_luwian_name(self, word: str, suffixes: List[str]) -> Dict:
        """Test if name follows Luwian naming patterns."""
        result = {'score': 0, 'matches': [], 'notes': []}

        for suffix in suffixes:
            suffix_upper = suffix.upper()
            for pattern, data in NAME_SUFFIX_PATTERNS['luwian'].items():
                pattern_clean = pattern.replace('-', '')
                if suffix_upper == pattern_clean or word.upper().endswith(pattern.replace('-', '')):
                    result['score'] += 1
                    result['matches'].append({
                        'suffix': pattern,
                        'meaning': data['meaning'],
                    })

        # Check for Luwian-like initial elements
        if word.upper().startswith(('TA-', 'MA-', 'PA-', 'PI-')):
            result['score'] += 0.5
            result['notes'].append('Luwian-like initial syllable')

        return result

    def _test_semitic_name(self, word: str, suffixes: List[str]) -> Dict:
        """Test if name follows Semitic naming patterns."""
        result = {'score': 0, 'matches': [], 'notes': []}

        for suffix in suffixes:
            suffix_upper = suffix.upper()
            for pattern, data in NAME_SUFFIX_PATTERNS['semitic'].items():
                pattern_clean = pattern.replace('-', '')
                if suffix_upper == pattern_clean:
                    result['score'] += 1
                    result['matches'].append({
                        'suffix': pattern,
                        'meaning': data['meaning'],
                    })

        # Check for triconsonantal structure (characteristic of Semitic)
        syllables = word.split('-')
        consonants = [s[0] for s in syllables if s and s[0] not in 'AEIOU']
        if len(consonants) == 3:
            result['score'] += 0.5
            result['notes'].append('Triconsonantal structure')

        return result

    def _test_pregreek_name(self, word: str, suffixes: List[str]) -> Dict:
        """Test if name follows Pre-Greek naming patterns."""
        result = {'score': 0, 'matches': [], 'notes': []}

        for suffix in suffixes:
            suffix_upper = suffix.upper()
            for pattern, data in NAME_SUFFIX_PATTERNS['pregreek'].items():
                pattern_clean = pattern.replace('-', '')
                if suffix_upper == pattern_clean:
                    result['score'] += 1
                    result['matches'].append({
                        'suffix': pattern,
                        'meaning': data['meaning'],
                    })

        # Check for Pre-Greek phonological markers
        word_concat = word.replace('-', '').upper()
        if 'SS' in word_concat or 'NTH' in word_concat or 'MN' in word_concat:
            result['score'] += 1
            result['notes'].append('Pre-Greek phonological marker')

        return result

    def _test_greek_name(self, word: str, suffixes: List[str]) -> Dict:
        """Test if name follows Greek naming patterns."""
        result = {'score': 0, 'matches': [], 'notes': []}

        for suffix in suffixes:
            suffix_upper = suffix.upper()
            for pattern, data in NAME_SUFFIX_PATTERNS['greek'].items():
                pattern_clean = pattern.replace('-', '')
                if suffix_upper == pattern_clean:
                    result['score'] += 1
                    result['matches'].append({
                        'suffix': pattern,
                        'meaning': data['meaning'],
                    })

        return result

    def _classify_name_type(self, word: str, syllables: List[str]) -> str:
        """Classify the type of personal name."""
        word_upper = word.upper()

        # Theophoric (contains divine element)
        for elem in THEOPHORIC_ELEMENTS:
            if elem in word_upper:
                return 'theophoric'

        # Patronymic indicators
        if word_upper.endswith(('-I-DA', '-I-DO')):
            return 'patronymic'

        # Occupational (usually short, ends in certain suffixes)
        if len(syllables) == 2 and word_upper.endswith(('-TE', '-KE', '-ME')):
            return 'occupational'

        return 'unknown'

    def _guess_gender(self, word: str, suffixes: List[str]) -> str:
        """Guess gender based on suffix patterns."""
        word_upper = word.upper()

        # Feminine indicators
        if word_upper.endswith(('-A', '-NA', '-NE', '-E')) and not word_upper.endswith(('-TA', '-DA')):
            return 'feminine'

        # Masculine indicators
        if word_upper.endswith(('-OS', '-U', '-AS', '-WA')):
            return 'masculine'

        return 'unknown'

    def _find_variants(self, word: str) -> List[str]:
        """Find possible spelling variants of a name."""
        variants = []
        word_upper = word.upper()

        for other in self.word_frequencies:
            if other == word_upper:
                continue

            # Check for vowel alternation variants
            # (e.g., KU-RO vs KI-RO, SA-RA vs SA-RI)
            if len(other.split('-')) == len(word_upper.split('-')):
                diff_count = sum(1 for a, b in zip(word_upper.split('-'), other.split('-')) if a != b)
                if diff_count == 1:
                    # Check if difference is just vowel
                    for s1, s2 in zip(word_upper.split('-'), other.split('-')):
                        if s1 != s2 and len(s1) == len(s2):
                            if s1[0] == s2[0]:  # Same consonant
                                variants.append(other)
                                break

        return variants[:5]  # Limit

    def _find_similar_names(self, word: str, all_words: List[str]) -> List[str]:
        """Find names with similar structure."""
        similar = []
        word_upper = word.upper()
        syllables = word_upper.split('-')

        for other in all_words:
            if other == word_upper:
                continue

            other_syls = other.split('-')

            # Same length and same initial syllable
            if len(other_syls) == len(syllables) and other_syls[0] == syllables[0]:
                similar.append(other)

            # Same suffix
            elif other_syls[-1] == syllables[-1] and len(other_syls) >= 2:
                similar.append(other)

        return similar[:5]  # Limit

    def analyze_single_name(self, word: str) -> Optional[PersonalName]:
        """Analyze a single word as potential name."""
        word_upper = word.upper()

        contexts = self.word_contexts.get(word_upper, [])
        if not contexts:
            # Create minimal context
            contexts = [{'followed_by_logogram': False, 'followed_by_number': False, 'site': 'UNKNOWN'}]

        name_prob, reason = self._calculate_name_probability(word_upper, contexts)

        syllables = word_upper.split('-')
        root, prefixes, suffixes = self._analyze_morphology(word_upper)

        luwian_fit = self._test_luwian_name(word_upper, suffixes)
        semitic_fit = self._test_semitic_name(word_upper, suffixes)
        pregreek_fit = self._test_pregreek_name(word_upper, suffixes)
        greek_fit = self._test_greek_name(word_upper, suffixes)

        fits = {
            'luwian': luwian_fit.get('score', 0),
            'semitic': semitic_fit.get('score', 0),
            'pregreek': pregreek_fit.get('score', 0),
            'greek': greek_fit.get('score', 0),
        }
        best_hyp = max(fits.keys(), key=lambda k: fits[k])

        return PersonalName(
            word=word_upper,
            occurrences=self.word_frequencies.get(word_upper, 0),
            sites=list(set(c.get('site', 'UNKNOWN') for c in contexts)),
            contexts=contexts[:5],
            name_probability=name_prob,
            detection_reason=reason,
            root=root,
            suffixes=suffixes,
            prefixes=prefixes,
            luwian_fit=luwian_fit,
            semitic_fit=semitic_fit,
            pregreek_fit=pregreek_fit,
            greek_fit=greek_fit,
            best_hypothesis=best_hyp if fits[best_hyp] > 0 else 'unknown',
            name_type=self._classify_name_type(word_upper, syllables),
            gender_guess=self._guess_gender(word_upper, suffixes),
            possible_variants=self._find_variants(word_upper),
            similar_names=self._find_similar_names(word_upper, list(self.word_frequencies.keys())),
        )

    def save_results(self, output_path: Path = None):
        """Save detected names to JSON."""
        if output_path is None:
            output_path = NAMES_FILE

        data = {
            'generated': datetime.now().isoformat(),
            'total_names_detected': len(self.detected_names),
            'methodology': 'Personal name detection based on context and morphology',
            'names': {word: asdict(name) for word, name in self.detected_names.items()},
            'summary': {
                'by_hypothesis': Counter(n.best_hypothesis for n in self.detected_names.values()),
                'by_type': Counter(n.name_type for n in self.detected_names.values()),
                'by_gender': Counter(n.gender_guess for n in self.detected_names.values()),
            },
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Results saved to: {output_path}")

    def print_name_report(self, name: PersonalName):
        """Print detailed report for a single name."""
        print("\n" + "=" * 70)
        print(f"PERSONAL NAME ANALYSIS: {name.word}")
        print("=" * 70)

        print(f"\nOccurrences: {name.occurrences}")
        print(f"Sites: {', '.join(name.sites)}")
        print(f"Name probability: {name.name_probability:.1%}")
        print(f"Detection reason: {name.detection_reason}")

        print("\nMorphology:")
        print(f"  Root: {name.root}")
        print(f"  Prefixes: {name.prefixes or 'none'}")
        print(f"  Suffixes: {name.suffixes or 'none'}")

        print("\nClassification:")
        print(f"  Name type: {name.name_type}")
        print(f"  Gender guess: {name.gender_guess}")

        print("\nHypothesis Testing:")
        for hyp in ['luwian', 'semitic', 'pregreek', 'greek']:
            fit = getattr(name, f'{hyp}_fit')
            score = fit.get('score', 0)
            indicator = "★" if hyp == name.best_hypothesis and score > 0 else " "
            print(f"  {indicator} {hyp.upper()}: score={score}")
            if fit.get('matches'):
                for m in fit['matches']:
                    print(f"      • {m['suffix']}: {m['meaning']}")
            if fit.get('notes'):
                for n in fit['notes']:
                    print(f"      • {n}")

        if name.possible_variants:
            print(f"\nPossible variants: {', '.join(name.possible_variants)}")

        if name.similar_names:
            print(f"Similar names: {', '.join(name.similar_names)}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Linear A personal names"
    )
    parser.add_argument(
        '--extract',
        action='store_true',
        help='Extract all likely personal names from corpus'
    )
    parser.add_argument(
        '--analyze', '-a',
        type=str,
        help='Analyze a specific word as potential name'
    )
    parser.add_argument(
        '--min-freq', '-m',
        type=int,
        default=2,
        help='Minimum frequency for name detection (default: 2)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A PERSONAL NAME ANALYZER")
    print("=" * 60)
    print("Analyzing anthroponyms to unlock 50%+ of vocabulary\n")

    analyzer = PersonalNameAnalyzer(verbose=args.verbose)

    if not analyzer.load_corpus():
        return 1

    if args.extract:
        names = analyzer.detect_personal_names(min_frequency=args.min_freq)

        print(f"\nDetected {len(names)} likely personal names")

        # Summary by hypothesis
        by_hyp = Counter(n.best_hypothesis for n in names.values())
        print("\nBy hypothesis:")
        for hyp, count in by_hyp.most_common():
            print(f"  {hyp}: {count}")

        # Top names
        print("\nTop names by probability:")
        sorted_names = sorted(names.values(), key=lambda n: -n.name_probability)
        for name in sorted_names[:15]:
            print(f"  {name.word}: prob={name.name_probability:.2f}, {name.best_hypothesis}, {name.name_type}")

        # Save results
        output_path = Path(args.output) if args.output else None
        analyzer.save_results(output_path)

    elif args.analyze:
        name = analyzer.analyze_single_name(args.analyze)
        if name:
            analyzer.print_name_report(name)

    else:
        print("Usage:")
        print("  --extract       Extract all likely personal names")
        print("  --analyze WORD  Analyze a specific word as name")
        print("\nExamples:")
        print("  python personal_name_analyzer.py --extract --min-freq 3")
        print("  python personal_name_analyzer.py --analyze DA-MA-TE")

    return 0


if __name__ == '__main__':
    sys.exit(main())
