#!/usr/bin/env python3
"""
Paradigm Discoverer for Linear A

Discovers morphological paradigms by:
1. Extracting candidate roots from words
2. Detecting systematic vowel alternations (U→I, U→E, U→A)
3. Clustering words sharing the same root
4. Validating paradigms corpus-wide

Currently only the K-R paradigm (KU-RO, KI-RO) has been systematically analyzed.
This tool aims to discover 5+ additional paradigms.

Target paradigms from MINOS analysis:
- SA- paradigm: SA-RA₂, SA-RU, SA-MA, SA-RI
- TA- paradigm: TA-I, TA-JA, TA-NA, TA-RA
- DA- paradigm: DA-I, DA-JA, DA-RE, DA-ME
- -JA suffix distribution: Across all roots
- -TE/-TI endings: Possible verbal system

Usage:
    python tools/paradigm_discoverer.py --discover
    python tools/paradigm_discoverer.py --root SA
    python tools/paradigm_discoverer.py --suffix JA

Attribution:
    Part of Linear A Decipherment Project (OPERATION MINOS II)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
PARADIGMS_FILE = DATA_DIR / "discovered_paradigms.json"


# Vowel classes for alternation detection
VOWELS = ['A', 'E', 'I', 'O', 'U']
VOWEL_ALTERNATIONS = [
    ('U', 'I'),   # Most common in K-R paradigm
    ('U', 'A'),   # Possible ablaut
    ('U', 'E'),   # Possible ablaut
    ('I', 'A'),   # Possible case marker
    ('I', 'E'),   # Possible case marker
    ('A', 'E'),   # Common Semitic pattern
    ('A', 'I'),   # Common pattern
]


@dataclass
class ParadigmMember:
    """A word that is a member of a paradigm."""
    word: str
    frequency: int
    vowel_pattern: str      # e.g., "U-O" for KU-RO
    final_syllable: str
    sites: List[str]
    contexts: List[str]     # Context types: administrative, religious, etc.


@dataclass
class Paradigm:
    """A discovered morphological paradigm."""
    paradigm_id: str
    root: str               # Consonantal root (e.g., "K-R")
    root_pattern: str       # Pattern (e.g., "CV-CV")
    members: List[ParadigmMember]
    total_occurrences: int

    # Alternation analysis
    vowel_alternations: List[Dict]
    final_alternations: List[Dict]

    # Functional analysis
    functional_differentiation: bool
    function_mapping: Dict[str, str]  # word -> proposed function

    # Confidence
    confidence: str         # HIGH, MEDIUM, LOW
    evidence_notes: List[str]

    # Comparison to K-R
    kr_similarity: float    # 0-1: how similar to known K-R paradigm


class ParadigmDiscoverer:
    """
    Discovers morphological paradigms in Linear A.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = None
        self.word_data: Dict[str, Dict] = {}  # word -> {freq, sites, contexts}
        self.discovered_paradigms: Dict[str, Paradigm] = {}

    def log(self, message: str):
        """Print if verbose mode."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        try:
            with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)

            self._extract_word_data()
            self.log(f"Loaded {len(self.word_data)} unique syllabic words")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _extract_word_data(self):
        """Extract word frequencies and contexts."""
        word_freq = Counter()
        word_sites = defaultdict(set)
        word_contexts = defaultdict(list)

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])
            site_match = re.match(r'^([A-Z]+)', insc_id)
            site = site_match.group(1) if site_match else 'UNKNOWN'

            for i, word in enumerate(words):
                if not word or '-' not in word:
                    continue

                # Skip numerals
                if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', word):
                    continue

                word_upper = word.upper()
                word_freq[word_upper] += 1
                word_sites[word_upper].add(site)

                # Determine context type
                after = words[i+1:i+3] if i < len(words) - 1 else []
                if any(w in ['GRA', 'VIN', 'OLE', 'OLIV', 'CYP'] for w in after):
                    word_contexts[word_upper].append('administrative')
                elif any(re.match(r'^[\d]+$', w) for w in after):
                    word_contexts[word_upper].append('counted')
                else:
                    word_contexts[word_upper].append('other')

        for word, freq in word_freq.items():
            self.word_data[word] = {
                'frequency': freq,
                'sites': list(word_sites[word]),
                'contexts': word_contexts[word],
            }

    def extract_consonant_skeleton(self, word: str) -> str:
        """
        Extract consonant skeleton from a word.

        KU-RO -> K-R
        SA-RA₂ -> S-R
        """
        syllables = word.upper().split('-')
        consonants = []

        for syl in syllables:
            # Remove subscripts
            syl_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
            if syl_clean and syl_clean[0] not in VOWELS:
                consonants.append(syl_clean[0])
            elif syl_clean and syl_clean[0] in VOWELS:
                # Pure vowel syllable
                consonants.append('Ø')

        return '-'.join(consonants)

    def extract_vowel_pattern(self, word: str) -> str:
        """
        Extract vowel pattern from a word.

        KU-RO -> U-O
        SA-RA₂ -> A-A
        """
        syllables = word.upper().split('-')
        vowels = []

        for syl in syllables:
            syl_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
            # Find vowel in syllable
            for char in syl_clean:
                if char in VOWELS:
                    vowels.append(char)
                    break
            else:
                vowels.append('?')

        return '-'.join(vowels)

    def find_paradigm_candidates(self, min_members: int = 2) -> Dict[str, List[str]]:
        """
        Find words that might belong to the same paradigm.

        Groups words by consonant skeleton.
        """
        skeleton_groups = defaultdict(list)

        for word in self.word_data:
            skeleton = self.extract_consonant_skeleton(word)
            if len(skeleton) >= 3:  # At least C-C pattern
                skeleton_groups[skeleton].append(word)

        # Filter to groups with enough members
        candidates = {
            skel: words for skel, words in skeleton_groups.items()
            if len(words) >= min_members
        }

        return candidates

    def analyze_paradigm(self, root: str, words: List[str]) -> Optional[Paradigm]:
        """
        Analyze a group of words as a potential paradigm.
        """
        if len(words) < 2:
            return None

        paradigm_id = f"P-{root.replace('-', '')}-{len(words)}"

        # Build member list
        members = []
        total_occ = 0

        for word in words:
            data = self.word_data.get(word, {})
            freq = data.get('frequency', 0)
            total_occ += freq

            members.append(ParadigmMember(
                word=word,
                frequency=freq,
                vowel_pattern=self.extract_vowel_pattern(word),
                final_syllable=word.split('-')[-1],
                sites=data.get('sites', []),
                contexts=data.get('contexts', []),
            ))

        # Sort by frequency
        members.sort(key=lambda m: -m.frequency)

        # Analyze vowel alternations
        vowel_alternations = self._detect_vowel_alternations(members)

        # Analyze final syllable alternations
        final_alternations = self._detect_final_alternations(members)

        # Check for functional differentiation
        func_diff, func_map = self._analyze_functional_differentiation(members)

        # Calculate confidence
        confidence, notes = self._calculate_confidence(
            members, vowel_alternations, final_alternations, func_diff
        )

        # Compare to K-R paradigm
        kr_sim = self._compare_to_kr(members, vowel_alternations)

        return Paradigm(
            paradigm_id=paradigm_id,
            root=root,
            root_pattern=self._get_root_pattern(words[0]),
            members=members,
            total_occurrences=total_occ,
            vowel_alternations=vowel_alternations,
            final_alternations=final_alternations,
            functional_differentiation=func_diff,
            function_mapping=func_map,
            confidence=confidence,
            evidence_notes=notes,
            kr_similarity=kr_sim,
        )

    def _get_root_pattern(self, word: str) -> str:
        """Get structural pattern (CV-CV, CV-CVC, etc.)."""
        syllables = word.upper().split('-')
        pattern = []

        for syl in syllables:
            syl_clean = re.sub(r'[₀₁₂₃₄₅₆₇₈₉]', '', syl)
            p = ''
            for char in syl_clean:
                if char in VOWELS:
                    p += 'V'
                else:
                    p += 'C'
            pattern.append(p)

        return '-'.join(pattern)

    def _detect_vowel_alternations(self, members: List[ParadigmMember]) -> List[Dict]:
        """Detect systematic vowel alternations."""
        alternations = []

        vowel_patterns = [m.vowel_pattern for m in members]
        unique_patterns = set(vowel_patterns)

        if len(unique_patterns) < 2:
            return alternations

        # Check each vowel position
        for i in range(len(vowel_patterns[0].split('-'))):
            vowels_at_pos = []
            for pattern in vowel_patterns:
                parts = pattern.split('-')
                if i < len(parts):
                    vowels_at_pos.append(parts[i])

            unique_vowels = set(vowels_at_pos)
            if len(unique_vowels) >= 2:
                # Check for known alternation patterns
                for v1, v2 in VOWEL_ALTERNATIONS:
                    if v1 in unique_vowels and v2 in unique_vowels:
                        # Find words with each variant
                        v1_words = [m.word for m in members
                                   if m.vowel_pattern.split('-')[i] == v1]
                        v2_words = [m.word for m in members
                                   if m.vowel_pattern.split('-')[i] == v2]

                        alternations.append({
                            'position': i,
                            'alternation': f'{v1}/{v2}',
                            f'{v1}_forms': v1_words,
                            f'{v2}_forms': v2_words,
                        })

        return alternations

    def _detect_final_alternations(self, members: List[ParadigmMember]) -> List[Dict]:
        """Detect final syllable alternations (possible case markers)."""
        alternations = []

        finals = Counter(m.final_syllable for m in members)

        if len(finals) >= 2:
            for final, count in finals.most_common():
                words = [m.word for m in members if m.final_syllable == final]
                alternations.append({
                    'final': final,
                    'count': count,
                    'words': words,
                })

        return alternations

    def _analyze_functional_differentiation(self, members: List[ParadigmMember]) -> Tuple[bool, Dict]:
        """Check if different forms have different functions."""
        func_map = {}

        for m in members:
            contexts = m.contexts
            if contexts:
                # Most common context
                common_ctx = Counter(contexts).most_common(1)[0][0]
                func_map[m.word] = common_ctx

        # Check if there's differentiation
        unique_funcs = set(func_map.values())
        has_differentiation = len(unique_funcs) >= 2

        return has_differentiation, func_map

    def _calculate_confidence(
        self,
        members: List[ParadigmMember],
        vowel_alt: List[Dict],
        final_alt: List[Dict],
        func_diff: bool
    ) -> Tuple[str, List[str]]:
        """Calculate confidence level for the paradigm."""
        notes = []
        score = 0

        # Number of members
        if len(members) >= 4:
            score += 2
            notes.append(f"Strong: {len(members)} members")
        elif len(members) >= 3:
            score += 1
            notes.append(f"Moderate: {len(members)} members")

        # Total occurrences
        total_occ = sum(m.frequency for m in members)
        if total_occ >= 20:
            score += 2
            notes.append(f"High frequency: {total_occ} total occurrences")
        elif total_occ >= 10:
            score += 1
            notes.append(f"Moderate frequency: {total_occ} occurrences")

        # Vowel alternations
        if vowel_alt:
            score += 1
            notes.append(f"Vowel alternation detected: {vowel_alt[0]['alternation']}")

        # Functional differentiation
        if func_diff:
            score += 1
            notes.append("Functional differentiation observed")

        # Site distribution (appears at multiple sites)
        all_sites = set()
        for m in members:
            all_sites.update(m.sites)
        if len(all_sites) >= 3:
            score += 1
            notes.append(f"Multi-site distribution: {len(all_sites)} sites")

        if score >= 5:
            return 'HIGH', notes
        elif score >= 3:
            return 'MEDIUM', notes
        else:
            return 'LOW', notes

    def _compare_to_kr(self, members: List[ParadigmMember], vowel_alt: List[Dict]) -> float:
        """
        Compare paradigm to the known K-R paradigm (KU-RO, KI-RO).

        Returns similarity score 0-1.
        """
        sim = 0.0

        # K-R has U/I alternation in first syllable
        for alt in vowel_alt:
            if alt['alternation'] == 'U/I' and alt['position'] == 0:
                sim += 0.4
                break

        # K-R has 2 main members with high frequency
        high_freq = [m for m in members if m.frequency >= 10]
        if len(high_freq) >= 2:
            sim += 0.2

        # K-R appears in administrative context
        admin_count = sum(1 for m in members
                         if 'administrative' in m.contexts or 'counted' in m.contexts)
        if admin_count >= len(members) * 0.5:
            sim += 0.2

        # K-R has CV-CV structure
        for m in members:
            if len(m.word.split('-')) == 2:
                sim += 0.1
                break

        # K-R appears at multiple sites
        all_sites = set()
        for m in members:
            all_sites.update(m.sites)
        if len(all_sites) >= 2:
            sim += 0.1

        return min(1.0, sim)

    def discover_paradigms(self, min_members: int = 2, min_occurrences: int = 5) -> Dict[str, Paradigm]:
        """Discover all paradigms in the corpus."""
        candidates = self.find_paradigm_candidates(min_members)

        self.log(f"Found {len(candidates)} candidate paradigm groups")

        for root, words in candidates.items():
            paradigm = self.analyze_paradigm(root, words)

            if paradigm and paradigm.total_occurrences >= min_occurrences:
                self.discovered_paradigms[paradigm.paradigm_id] = paradigm
                self.log(f"Discovered paradigm: {root} ({len(words)} members, {paradigm.confidence})")

        return self.discovered_paradigms

    def analyze_root(self, root: str) -> Optional[Paradigm]:
        """Analyze a specific root."""
        root_upper = root.upper()

        # Find all words with this consonant skeleton
        matching_words = []
        for word in self.word_data:
            skeleton = self.extract_consonant_skeleton(word)
            if skeleton == root_upper or skeleton.startswith(root_upper):
                matching_words.append(word)

        if not matching_words:
            print(f"No words found with root pattern: {root}")
            return None

        return self.analyze_paradigm(root_upper, matching_words)

    def analyze_suffix(self, suffix: str) -> Dict[str, List[str]]:
        """Analyze distribution of a suffix across words."""
        suffix_upper = suffix.upper()

        suffix_words = defaultdict(list)

        for word in self.word_data:
            if word.endswith(f'-{suffix_upper}'):
                root = self.extract_consonant_skeleton(word)
                suffix_words[root].append(word)

        return dict(suffix_words)

    def save_results(self, output_path: Path = None):
        """Save discovered paradigms to JSON."""
        if output_path is None:
            output_path = PARADIGMS_FILE

        # Convert paradigms for JSON serialization
        paradigms_data = {}
        for pid, p in self.discovered_paradigms.items():
            paradigms_data[pid] = {
                'paradigm_id': p.paradigm_id,
                'root': p.root,
                'root_pattern': p.root_pattern,
                'members': [asdict(m) for m in p.members],
                'total_occurrences': p.total_occurrences,
                'vowel_alternations': p.vowel_alternations,
                'final_alternations': p.final_alternations,
                'functional_differentiation': p.functional_differentiation,
                'function_mapping': p.function_mapping,
                'confidence': p.confidence,
                'evidence_notes': p.evidence_notes,
                'kr_similarity': p.kr_similarity,
            }

        data = {
            'generated': datetime.now().isoformat(),
            'total_paradigms': len(self.discovered_paradigms),
            'paradigms': paradigms_data,
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Results saved to: {output_path}")

    def print_paradigm_report(self, paradigm: Paradigm):
        """Print detailed paradigm report."""
        print("\n" + "=" * 70)
        print(f"PARADIGM: {paradigm.root}")
        print("=" * 70)

        print(f"\nID: {paradigm.paradigm_id}")
        print(f"Root pattern: {paradigm.root_pattern}")
        print(f"Confidence: {paradigm.confidence}")
        print(f"K-R similarity: {paradigm.kr_similarity:.1%}")

        print(f"\nMembers ({len(paradigm.members)}):")
        for m in paradigm.members:
            print(f"  {m.word:15} freq={m.frequency:3} vowels={m.vowel_pattern:5} sites={','.join(m.sites[:3])}")

        print(f"\nTotal occurrences: {paradigm.total_occurrences}")

        if paradigm.vowel_alternations:
            print(f"\nVowel Alternations:")
            for alt in paradigm.vowel_alternations:
                print(f"  Position {alt['position']}: {alt['alternation']}")
                for key, val in alt.items():
                    if key.endswith('_forms'):
                        print(f"    {key}: {', '.join(val)}")

        if paradigm.final_alternations:
            print(f"\nFinal Syllable Alternations:")
            for alt in paradigm.final_alternations:
                print(f"  -{alt['final']}: {', '.join(alt['words'])}")

        if paradigm.functional_differentiation:
            print(f"\nFunctional Differentiation:")
            for word, func in paradigm.function_mapping.items():
                print(f"  {word}: {func}")

        print(f"\nEvidence Notes:")
        for note in paradigm.evidence_notes:
            print(f"  • {note}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Discover morphological paradigms in Linear A"
    )
    parser.add_argument(
        '--discover',
        action='store_true',
        help='Discover all paradigms in corpus'
    )
    parser.add_argument(
        '--root', '-r',
        type=str,
        help='Analyze a specific root (e.g., K-R, S-R, T-N)'
    )
    parser.add_argument(
        '--suffix', '-s',
        type=str,
        help='Analyze distribution of a suffix (e.g., JA, TE, TI)'
    )
    parser.add_argument(
        '--min-members',
        type=int,
        default=2,
        help='Minimum members for paradigm (default: 2)'
    )
    parser.add_argument(
        '--min-occurrences',
        type=int,
        default=5,
        help='Minimum total occurrences (default: 5)'
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
    print("LINEAR A PARADIGM DISCOVERER")
    print("=" * 60)
    print("Discovering morphological patterns beyond K-R\n")

    discoverer = ParadigmDiscoverer(verbose=args.verbose)

    if not discoverer.load_corpus():
        return 1

    if args.discover:
        paradigms = discoverer.discover_paradigms(
            min_members=args.min_members,
            min_occurrences=args.min_occurrences
        )

        print(f"\nDiscovered {len(paradigms)} paradigms")

        # Sort by confidence and occurrence
        sorted_paradigms = sorted(
            paradigms.values(),
            key=lambda p: (p.confidence == 'HIGH', p.confidence == 'MEDIUM', p.total_occurrences),
            reverse=True
        )

        print("\nTop paradigms:")
        for p in sorted_paradigms[:10]:
            members = ', '.join(m.word for m in p.members[:4])
            print(f"  {p.root}: {p.confidence} ({p.total_occurrences} occ) - {members}")

        # Save results
        output_path = Path(args.output) if args.output else None
        discoverer.save_results(output_path)

    elif args.root:
        paradigm = discoverer.analyze_root(args.root)
        if paradigm:
            discoverer.print_paradigm_report(paradigm)

    elif args.suffix:
        suffix_dist = discoverer.analyze_suffix(args.suffix)
        print(f"\nSuffix -{args.suffix.upper()} distribution:")
        for root, words in sorted(suffix_dist.items(), key=lambda x: -len(x[1])):
            print(f"  {root}: {', '.join(words)}")

    else:
        print("Usage:")
        print("  --discover      Discover all paradigms")
        print("  --root ROOT     Analyze specific root (e.g., K-R)")
        print("  --suffix SUFFIX Analyze suffix distribution (e.g., JA)")
        print("\nExamples:")
        print("  python paradigm_discoverer.py --discover --min-members 3")
        print("  python paradigm_discoverer.py --root S-R")
        print("  python paradigm_discoverer.py --suffix JA")

    return 0


if __name__ == '__main__':
    sys.exit(main())
