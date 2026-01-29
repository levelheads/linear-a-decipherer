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

# ===========================================================================
# LUWIAN/ANATOLIAN REFERENCE DATA
# Sources: Melchert (2003) Luwian Dictionary, Yakubovich (2010), Finkelberg (1998)
# ===========================================================================

LUWIAN_LEXICON = {
    # Particles and grammatical elements (HIGH confidence)
    'a': {'meaning': 'and/coordinative conjunction', 'confidence': 'HIGH', 'source': 'Melchert'},
    'wa': {'meaning': 'quotative particle', 'confidence': 'HIGH', 'source': 'Melchert'},
    'u': {'meaning': 'quotative particle variant', 'confidence': 'HIGH', 'source': 'Melchert'},
    'awa': {'meaning': 'quotative (full form)', 'confidence': 'HIGH', 'source': 'Melchert'},

    # Pronouns and determiners (MEDIUM-HIGH confidence)
    'ki': {'meaning': 'relative pronoun stem (kui-)', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'apa': {'meaning': 'demonstrative "that"', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'za': {'meaning': 'demonstrative "this"', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'kwi': {'meaning': 'interrogative/relative', 'confidence': 'MEDIUM', 'source': 'Melchert'},

    # Verbal roots (MEDIUM confidence)
    'adi': {'meaning': 'to make/do (a- + -ti)', 'confidence': 'MEDIUM', 'source': 'Yakubovich'},
    'tati': {'meaning': 'father', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'anni': {'meaning': 'mother', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'wawa': {'meaning': 'cow', 'confidence': 'MEDIUM', 'source': 'Melchert'},

    # Nouns (MEDIUM confidence)
    'padi': {'meaning': 'into/to (place)', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'taru': {'meaning': 'tree, wood', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'watu': {'meaning': 'water', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'hanti': {'meaning': 'front, forehead', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'ura': {'meaning': 'great', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    'massana': {'meaning': 'god', 'confidence': 'MEDIUM', 'source': 'Melchert'},

    # Divine names (LOW-MEDIUM confidence for Linear A)
    'tarhunt': {'meaning': 'Storm God (Tarḫunt-)', 'confidence': 'LOW', 'source': 'Yakubovich'},
    'santa': {'meaning': 'deity name', 'confidence': 'LOW', 'source': 'Melchert'},
    'arma': {'meaning': 'Moon God', 'confidence': 'LOW', 'source': 'Melchert'},

    # Suffixes
    '-ja': {'meaning': 'adjectival suffix (-iya)', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-ti': {'meaning': 'verbal 3sg ending', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-nti': {'meaning': 'verbal 3pl ending', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-ssa': {'meaning': 'nominal suffix (place)', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-nda': {'meaning': 'suffix (characteristic)', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-si': {'meaning': 'dative-locative', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-za': {'meaning': 'ablative suffix', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-ta': {'meaning': 'agentive suffix', 'confidence': 'MEDIUM', 'source': 'Melchert'},
    '-ri': {'meaning': 'nominal suffix', 'confidence': 'LOW', 'source': 'Yakubovich'},
}

LUWIAN_PHONOLOGICAL_MARKERS = [
    # Labialized consonants
    'wa', 'wi', 'wu', 'we', 'wo',
    # Characteristic clusters
    'ssa', 'nda', 'nti', 'tti',
    # Initial patterns
    'ta', 'pa', 'ma', 'ha',
]

# Sound correspondence rules: Luwian -> Linear A (speculative)
LUWIAN_SOUND_RULES = {
    'ḫ': 'a',  # Laryngeal often lost or vowel
    'tt': 'ta',  # Geminate simplified
    'ss': 'sa',  # Geminate simplified
}

# ===========================================================================
# SEMITIC REFERENCE DATA (Akkadian, Hebrew, Ugaritic, West Semitic)
# Sources: CAD (Chicago Akkadian Dictionary), BDB Hebrew Lexicon,
# Huehnergard (2011), Gordon (1966)
# ===========================================================================

SEMITIC_LEXICON = {
    # ---- ADMINISTRATIVE VOCABULARY (HIGH confidence) ----

    # Totals and quantities
    'kull': {'meaning': 'all, totality (Akkadian kullatu)', 'confidence': 'HIGH', 'root': 'KLL', 'source': 'CAD'},
    'kol': {'meaning': 'all, every (Hebrew kōl)', 'confidence': 'HIGH', 'root': 'KL', 'source': 'BDB'},
    'kala': {'meaning': 'to complete, finish (Akkadian kalû)', 'confidence': 'HIGH', 'root': 'KL', 'source': 'CAD'},

    # Deficit/diminish
    'gara': {'meaning': 'to diminish, deduct (Hebrew gāraʿ)', 'confidence': 'HIGH', 'root': 'GR', 'source': 'BDB'},
    'giru': {'meaning': 'to be wanting, lack', 'confidence': 'MEDIUM', 'root': 'GR', 'source': 'Ugaritic'},

    # Counting and recording
    'spr': {'meaning': 'to count, write (Hebrew sāpar)', 'confidence': 'MEDIUM', 'root': 'SPR', 'source': 'BDB'},
    'sapru': {'meaning': 'scribe, official', 'confidence': 'MEDIUM', 'root': 'SPR', 'source': 'CAD'},
    'mana': {'meaning': 'to count, assign (Akkadian manû)', 'confidence': 'MEDIUM', 'root': 'MN', 'source': 'CAD'},

    # Gathering and collecting
    'asap': {'meaning': 'to gather, collect (Hebrew ʾāsap)', 'confidence': 'MEDIUM', 'root': 'SP', 'source': 'BDB'},
    'qbs': {'meaning': 'to gather (Hebrew qābaṣ)', 'confidence': 'MEDIUM', 'root': 'QBS', 'source': 'BDB'},
    'kns': {'meaning': 'to gather, assemble', 'confidence': 'LOW', 'root': 'KNS', 'source': 'BDB'},

    # Payment and wages
    'sakar': {'meaning': 'wage, hire (Hebrew śākār)', 'confidence': 'MEDIUM', 'root': 'SKR', 'source': 'BDB'},
    'sakaru': {'meaning': 'to hire, pay wages (Akkadian)', 'confidence': 'MEDIUM', 'root': 'SKR', 'source': 'CAD'},

    # ---- COMMODITIES (MEDIUM confidence) ----

    # Wine
    'yayin': {'meaning': 'wine (Hebrew yayin)', 'confidence': 'MEDIUM', 'root': 'YN', 'source': 'BDB'},
    'karanu': {'meaning': 'wine (Akkadian)', 'confidence': 'MEDIUM', 'root': 'KRN', 'source': 'CAD'},

    # Oil
    'samnu': {'meaning': 'oil, fat (Akkadian šamnu)', 'confidence': 'MEDIUM', 'root': 'SMN', 'source': 'CAD'},
    'semen': {'meaning': 'oil (Hebrew šemen)', 'confidence': 'MEDIUM', 'root': 'SMN', 'source': 'BDB'},

    # Grain
    'se': {'meaning': 'barley (Akkadian sheu)', 'confidence': 'MEDIUM', 'root': 'S', 'source': 'CAD'},
    'dagan': {'meaning': 'grain (Hebrew dāgān)', 'confidence': 'MEDIUM', 'root': 'DGN', 'source': 'BDB'},
    'kibtu': {'meaning': 'wheat (Akkadian)', 'confidence': 'LOW', 'root': 'KBT', 'source': 'CAD'},

    # Honey
    'dabas': {'meaning': 'honey (Hebrew dĕbaš)', 'confidence': 'MEDIUM', 'root': 'DBS', 'source': 'BDB'},
    'dispu': {'meaning': 'honey (Akkadian)', 'confidence': 'MEDIUM', 'root': 'DSP', 'source': 'CAD'},

    # Figs
    'tina': {'meaning': 'fig (Hebrew tĕʾēnā)', 'confidence': 'MEDIUM', 'root': 'TN', 'source': 'BDB'},

    # ---- SOCIAL/POLITICAL VOCABULARY (LOW-MEDIUM confidence) ----

    # Ruler terms
    'mlk': {'meaning': 'king, rule (Hebrew melek)', 'confidence': 'LOW', 'root': 'MLK', 'source': 'BDB'},
    'sarru': {'meaning': 'king (Akkadian)', 'confidence': 'LOW', 'root': 'SRR', 'source': 'CAD'},
    'rb': {'meaning': 'great, chief (Hebrew rab)', 'confidence': 'LOW', 'root': 'RB', 'source': 'BDB'},

    # People terms
    'amm': {'meaning': 'people, kinship group (Hebrew ʿam)', 'confidence': 'LOW', 'root': 'MM', 'source': 'BDB'},
    'goy': {'meaning': 'nation (Hebrew gôy)', 'confidence': 'LOW', 'root': 'GY', 'source': 'BDB'},

    # House/temple
    'bitu': {'meaning': 'house, temple (Akkadian bītu)', 'confidence': 'MEDIUM', 'root': 'BT', 'source': 'CAD'},
    'bayit': {'meaning': 'house (Hebrew bayit)', 'confidence': 'MEDIUM', 'root': 'BT', 'source': 'BDB'},

    # ---- RELIGIOUS VOCABULARY (LOW-MEDIUM confidence) ----

    # God terms
    'ilu': {'meaning': 'god (Akkadian, Ugaritic)', 'confidence': 'MEDIUM', 'root': 'L', 'source': 'CAD'},
    'el': {'meaning': 'god (Hebrew ʾēl)', 'confidence': 'MEDIUM', 'root': 'L', 'source': 'BDB'},

    # Offering terms
    'ndr': {'meaning': 'vow, votive offering', 'confidence': 'LOW', 'root': 'NDR', 'source': 'BDB'},
    'qrb': {'meaning': 'to offer, bring near', 'confidence': 'LOW', 'root': 'QRB', 'source': 'BDB'},
    'zbh': {'meaning': 'sacrifice (Hebrew zebaḥ)', 'confidence': 'LOW', 'root': 'ZBH', 'source': 'BDB'},

    # Blessing
    'brk': {'meaning': 'to bless (Hebrew bārak)', 'confidence': 'LOW', 'root': 'BRK', 'source': 'BDB'},
    'slm': {'meaning': 'peace, wellbeing (Hebrew šālôm)', 'confidence': 'LOW', 'root': 'SLM', 'source': 'BDB'},

    # ---- NUMBERS (LOW confidence - different system) ----

    'wahid': {'meaning': 'one', 'confidence': 'LOW', 'root': 'WHD', 'source': 'BDB'},
    'sana': {'meaning': 'two', 'confidence': 'LOW', 'root': 'SN', 'source': 'BDB'},
    'salasa': {'meaning': 'three', 'confidence': 'LOW', 'root': 'SLS', 'source': 'BDB'},

    # ---- VERBS (LOW confidence - morphology differences) ----

    'ntn': {'meaning': 'to give (Hebrew nātan)', 'confidence': 'LOW', 'root': 'NTN', 'source': 'BDB'},
    'lqh': {'meaning': 'to take (Hebrew lāqaḥ)', 'confidence': 'LOW', 'root': 'LQH', 'source': 'BDB'},
    'bw': {'meaning': 'to come (Hebrew bôʾ)', 'confidence': 'LOW', 'root': 'BW', 'source': 'BDB'},
    'yṣ': {'meaning': 'to go out (Hebrew yāṣāʾ)', 'confidence': 'LOW', 'root': 'YS', 'source': 'BDB'},
    'ʿbd': {'meaning': 'to work, serve (Hebrew ʿābad)', 'confidence': 'LOW', 'root': 'BD', 'source': 'BDB'},
    'šmr': {'meaning': 'to guard, keep (Hebrew šāmar)', 'confidence': 'LOW', 'root': 'SMR', 'source': 'BDB'},
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

# ===========================================================================
# PRE-GREEK SUBSTRATE REFERENCE DATA
# Sources: Beekes (2014) Pre-Greek, Furnée (1972), Kretschmer
# ===========================================================================

PREGREEK_MARKERS = {
    # Characteristic consonant clusters (cannot occur in PIE)
    'nth': {'type': 'cluster', 'significance': 'HIGH', 'examples': ['Korinthos', 'labyrinth', 'Zakynthos']},
    'ss': {'type': 'cluster', 'significance': 'HIGH', 'examples': ['Knossos', 'Parnassos', 'Tylissos']},
    'mn': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': ['Amnissos', 'Hymettus']},
    'nd': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': []},
    'tt': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': ['Brettia']},
    'mb': {'type': 'cluster', 'significance': 'MEDIUM', 'examples': []},
    'gd': {'type': 'cluster', 'significance': 'LOW', 'examples': []},

    # Characteristic suffixes
    'assos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Parnassos', 'Halicarnassos']},
    'inthos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Korinthos', 'Zakynthos', 'labyrinth']},
    'issos': {'type': 'suffix', 'significance': 'HIGH', 'examples': ['Tylissos', 'Knossos']},
    'ene': {'type': 'suffix', 'significance': 'MEDIUM', 'examples': ['Athene', 'Mykene']},
    'ene': {'type': 'suffix', 'significance': 'MEDIUM', 'examples': ['Peirene']},

    # Toponymic suffixes
    'ara': {'type': 'toponym_suffix', 'significance': 'MEDIUM', 'examples': []},
    'ssa': {'type': 'toponym_suffix', 'significance': 'HIGH', 'examples': ['Larissa', 'Mykalessos']},
    'na': {'type': 'toponym_suffix', 'significance': 'MEDIUM', 'examples': ['Athena', 'Mykena']},
}

PREGREEK_VOCABULARY = {
    # Plants and agriculture (HIGH - borrowed into Greek)
    'elaia': {'meaning': 'olive', 'confidence': 'MEDIUM', 'source': 'Beekes'},
    'ampelos': {'meaning': 'vine', 'confidence': 'MEDIUM', 'source': 'Beekes'},
    'kitharos': {'meaning': 'lyre', 'confidence': 'MEDIUM', 'source': 'Beekes'},
    'labyrinthos': {'meaning': 'labyrinth', 'confidence': 'HIGH', 'source': 'Beekes'},
    'thalassa': {'meaning': 'sea', 'confidence': 'HIGH', 'source': 'Beekes'},
    'kolossos': {'meaning': 'statue', 'confidence': 'MEDIUM', 'source': 'Beekes'},

    # Metals and crafts
    'kassiteros': {'meaning': 'tin', 'confidence': 'MEDIUM', 'source': 'Furnée'},
    'khalybos': {'meaning': 'steel/iron', 'confidence': 'LOW', 'source': 'Furnée'},

    # Religious/ritual
    'thymos': {'meaning': 'spirit, soul (possibly)', 'confidence': 'LOW', 'source': 'Beekes'},
    'daphnē': {'meaning': 'laurel', 'confidence': 'MEDIUM', 'source': 'Beekes'},

    # Personal names/theonyms
    'Ariadne': {'meaning': 'personal name (Pre-Greek)', 'confidence': 'MEDIUM', 'source': 'Beekes'},
    'Athene': {'meaning': 'goddess name (Pre-Greek)', 'confidence': 'HIGH', 'source': 'Beekes'},
}

# Pre-Greek phonological rules (characteristics that distinguish from IE)
PREGREEK_PHONOLOGY = {
    # Vowel alternations (a/e, i/e)
    'vowel_alternation': ['a/e', 'i/e', 'o/a'],
    # Initial clusters forbidden in PIE
    'initial_clusters': ['gd-', 'bd-', 'ks-', 'ps-'],
    # Prenasalization
    'prenasalization': ['mb', 'nd', 'ng'],
}

# ===========================================================================
# PROTO-GREEK / MYCENAEAN REFERENCE DATA
# Sources: Ventris & Chadwick (1973) Documents in Mycenaean Greek,
# Aura Jorro (1985-1993) DMic, Palmer (1963)
# ===========================================================================

GREEK_LEXICON = {
    # ---- ADMINISTRATIVE VOCABULARY (HIGH confidence) ----

    # Totals and quantities
    'toso': {'meaning': 'so much, total (τόσος)', 'Linear_B': 'to-so', 'confidence': 'HIGH', 'source': 'Ventris'},
    'tosa': {'meaning': 'so many (fem.)', 'Linear_B': 'to-sa', 'confidence': 'HIGH', 'source': 'Ventris'},
    'panta': {'meaning': 'all (πάντα)', 'Linear_B': 'pa-ta', 'confidence': 'MEDIUM', 'source': 'Ventris'},

    # Personnel/titles
    'wanax': {'meaning': 'king (ϝάναξ)', 'Linear_B': 'wa-na-ka', 'confidence': 'HIGH', 'source': 'Ventris'},
    'lawagetas': {'meaning': 'army leader (λαγέτας)', 'Linear_B': 'ra-wa-ke-ta', 'confidence': 'HIGH', 'source': 'Ventris'},
    'basileus': {'meaning': 'chief, king (βασιλεύς)', 'Linear_B': 'qa-si-re-u', 'confidence': 'HIGH', 'source': 'Ventris'},
    'korete': {'meaning': 'mayor, governor', 'Linear_B': 'ko-re-te', 'confidence': 'HIGH', 'source': 'Ventris'},
    'doero': {'meaning': 'servant/slave (δοῦλος)', 'Linear_B': 'do-e-ro', 'confidence': 'HIGH', 'source': 'Ventris'},
    'doera': {'meaning': 'female servant', 'Linear_B': 'do-e-ra', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Professions
    'tekton': {'meaning': 'craftsman (τέκτων)', 'Linear_B': 'te-ko-to', 'confidence': 'HIGH', 'source': 'Ventris'},
    'khalkeus': {'meaning': 'bronzesmith (χαλκεύς)', 'Linear_B': 'ka-ke-u', 'confidence': 'HIGH', 'source': 'Ventris'},
    'kerameus': {'meaning': 'potter (κεραμεύς)', 'Linear_B': 'ke-ra-me-u', 'confidence': 'HIGH', 'source': 'Ventris'},

    # ---- COMMODITIES (HIGH confidence) ----

    # Wine
    'woinos': {'meaning': 'wine (ϝοῖνος)', 'Linear_B': 'wo-no', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Oil
    'elaiwon': {'meaning': 'olive oil (ἔλαιϝον)', 'Linear_B': 'e-ra-wo', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Grain
    'sitos': {'meaning': 'grain, food (σῖτος)', 'Linear_B': 'si-to', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Honey
    'meli': {'meaning': 'honey (μέλι)', 'Linear_B': 'me-ri', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Figs
    'sukon': {'meaning': 'fig (σῦκον)', 'Linear_B': 'su-ko', 'confidence': 'HIGH', 'source': 'Ventris'},

    # Wool/textiles
    'mallos': {'meaning': 'wool', 'Linear_B': 'ma-ro', 'confidence': 'MEDIUM', 'source': 'Ventris'},

    # Metals
    'khalkos': {'meaning': 'bronze (χαλκός)', 'Linear_B': 'ka-ko', 'confidence': 'HIGH', 'source': 'Ventris'},
    'khrusos': {'meaning': 'gold (χρυσός)', 'Linear_B': 'ku-ru-so', 'confidence': 'HIGH', 'source': 'Ventris'},

    # ---- ANIMALS (HIGH confidence) ----

    'bous': {'meaning': 'ox, cattle (βοῦς)', 'Linear_B': 'qo-u', 'confidence': 'HIGH', 'source': 'Ventris'},
    'oïs': {'meaning': 'sheep (ὄϊς)', 'Linear_B': 'o-wi', 'confidence': 'HIGH', 'source': 'Ventris'},
    'aix': {'meaning': 'goat (αἴξ)', 'Linear_B': 'a-i-ka', 'confidence': 'HIGH', 'source': 'Ventris'},
    'sus': {'meaning': 'pig (σῦς)', 'Linear_B': 'su-we', 'confidence': 'HIGH', 'source': 'Ventris'},
    'hippos': {'meaning': 'horse (ἵππος)', 'Linear_B': 'i-qo', 'confidence': 'HIGH', 'source': 'Ventris'},

    # ---- DIVINE NAMES (HIGH confidence for Linear B) ----

    'Zeus': {'meaning': 'Zeus (Ζεύς)', 'Linear_B': 'di-we', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Hera': {'meaning': 'Hera (Ἥρα)', 'Linear_B': 'e-ra', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Poseidon': {'meaning': 'Poseidon (Ποσειδῶν)', 'Linear_B': 'po-se-da-o', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Athena': {'meaning': 'Athena (Ἀθήνη)', 'Linear_B': 'a-ta-na', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'Artemis': {'meaning': 'Artemis (Ἄρτεμις)', 'Linear_B': 'a-te-mi-to', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'Hermes': {'meaning': 'Hermes (Ἑρμῆς)', 'Linear_B': 'e-ma-a', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'Dionysos': {'meaning': 'Dionysus (Διόνυσος)', 'Linear_B': 'di-wo-nu-so', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'Potnia': {'meaning': 'Lady, Mistress (Πότνια)', 'Linear_B': 'po-ti-ni-ja', 'confidence': 'HIGH', 'source': 'Ventris'},

    # ---- KINSHIP TERMS (HIGH confidence) ----

    'meter': {'meaning': 'mother (μήτηρ)', 'Linear_B': 'ma-te', 'confidence': 'HIGH', 'source': 'Ventris'},
    'pater': {'meaning': 'father (πατήρ)', 'Linear_B': 'pa-te', 'confidence': 'HIGH', 'source': 'Ventris'},
    'huios': {'meaning': 'son (υἱός)', 'Linear_B': 'u-jo', 'confidence': 'HIGH', 'source': 'Ventris'},
    'korwos': {'meaning': 'boy (κόρϝος)', 'Linear_B': 'ko-wo', 'confidence': 'HIGH', 'source': 'Ventris'},
    'korwa': {'meaning': 'girl (κόρϝα)', 'Linear_B': 'ko-wa', 'confidence': 'HIGH', 'source': 'Ventris'},
    'gune': {'meaning': 'woman (γυνή)', 'Linear_B': 'ku-na', 'confidence': 'MEDIUM', 'source': 'Ventris'},

    # ---- PLACES (HIGH confidence - includes confirmed Linear A toponym) ----

    'Phaistos': {'meaning': 'Phaistos', 'Linear_B': 'pa-i-to', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Knossos': {'meaning': 'Knossos', 'Linear_B': 'ko-no-so', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Amnisos': {'meaning': 'Amnisos', 'Linear_B': 'a-mi-ni-so', 'confidence': 'HIGH', 'source': 'Ventris'},
    'Tylissos': {'meaning': 'Tylissos', 'Linear_B': 'tu-ri-so', 'confidence': 'MEDIUM', 'source': 'Ventris'},

    # ---- POSSIBLE LINEAR A COGNATES (MEDIUM-LOW confidence) ----

    'kyrios': {'meaning': 'lord, master → total?', 'Linear_B': 'ku-ro', 'confidence': 'MEDIUM', 'source': 'Gordon'},
    'chreos': {'meaning': 'debt (χρέος)', 'Linear_B': 'ki-re-o', 'confidence': 'LOW', 'source': 'Gordon'},
    'demos': {'meaning': 'people, district (δῆμος)', 'Linear_B': 'da-mo', 'confidence': 'MEDIUM', 'source': 'Ventris'},

    # ---- VERBS (MEDIUM confidence) ----

    'didonai': {'meaning': 'to give (δίδωμι)', 'Linear_B': 'di-do-si', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'ekhein': {'meaning': 'to have (ἔχω)', 'Linear_B': 'e-ke', 'confidence': 'MEDIUM', 'source': 'Ventris'},
    'ophellein': {'meaning': 'to owe (ὀφείλω)', 'Linear_B': 'o-pe-ro', 'confidence': 'MEDIUM', 'source': 'Ventris'},
}

# Greek phonetic patterns expected in Linear A (if Greek)
GREEK_PHONOLOGY_EXPECTATIONS = {
    # Expected vowel distribution
    'vowel_distribution': {'a': 0.25, 'e': 0.20, 'i': 0.20, 'o': 0.20, 'u': 0.15},
    # Linear A actual: a ~39%, i ~26%, u ~18%, e ~14%, o ~3% (strongly differs!)

    # Expected case endings (if Greek)
    'case_endings': ['-o', '-a', '-i', '-e', '-os', '-as', '-es', '-oi', '-ai'],

    # Diphthongs expected
    'diphthongs': ['ai', 'ei', 'oi', 'au', 'eu', 'ou'],
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
        self.contextual_data = None
        self.formulaic_words = set()
        self.high_pmi_pairs = {}
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
            },
            'contextual_analysis': {},
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

    def load_contextual_data(self) -> bool:
        """
        Load contextual analysis data including formulaic sequences and PMI pairs.

        This data enhances hypothesis testing by considering:
        - Words that appear in fixed formulas (likely religious/ritual terms)
        - Words with high co-occurrence (likely semantically related)
        """
        try:
            context_path = DATA_DIR / "contextual_analysis.json"
            if not context_path.exists():
                self.log("No contextual analysis data found - skipping")
                return False

            with open(context_path, 'r', encoding='utf-8') as f:
                self.contextual_data = json.load(f)

            # Extract formulaic words (appear in fixed sequences)
            formulas = self.contextual_data.get('formulas', {})
            for length_group in formulas.get('by_length', {}).values():
                for formula in length_group:
                    sequence = formula.get('sequence', [])
                    occurrences = formula.get('occurrences', 0)
                    is_libation = formula.get('is_libation_related', False)

                    for word in sequence:
                        if '-' in word:  # Syllabic words only
                            if word not in self.formulaic_words:
                                self.formulaic_words.add(word)

            # Extract high-PMI pairs (semantically related words)
            cooc = self.contextual_data.get('cooccurrence', {})
            for pair in cooc.get('high_pmi_pairs', []):
                w1 = pair.get('word1', '')
                w2 = pair.get('word2', '')
                pmi = pair.get('pmi', 0)
                count = pair.get('cooccurrence_count', 0)

                if '-' in w1 and '-' in w2 and w1 != w2:
                    if w1 not in self.high_pmi_pairs:
                        self.high_pmi_pairs[w1] = []
                    self.high_pmi_pairs[w1].append({
                        'related_word': w2,
                        'pmi': pmi,
                        'count': count,
                    })

            self.log(f"Loaded {len(self.formulaic_words)} formulaic words")
            self.log(f"Loaded {len(self.high_pmi_pairs)} words with PMI associations")
            return True

        except Exception as e:
            self.log(f"Error loading contextual data: {e}")
            return False

    def test_formula_against_hypotheses(self, formula_words: List[str]) -> dict:
        """
        Test a formulaic sequence against all four hypotheses.

        Formulas are significant because:
        - They may preserve archaic language forms
        - They often appear in religious/ritual contexts
        - Their meaning may be fixed and conventional
        """
        analysis = {
            'formula': ' '.join(formula_words),
            'words_count': len(formula_words),
            'hypotheses': {},
            'overall_interpretation': None,
        }

        # Test each word and aggregate
        word_results = []
        for word in formula_words:
            if '-' in word:
                result = self.test_word(word)
                word_results.append(result)

        if not word_results:
            return analysis

        # Aggregate hypothesis scores
        for hyp in ['luwian', 'semitic', 'pregreek', 'protogreek']:
            total_score = sum(r['hypotheses'][hyp]['score'] for r in word_results)
            supported_count = sum(1 for r in word_results
                                  if r['hypotheses'][hyp]['verdict'] == 'SUPPORTED')
            analysis['hypotheses'][hyp] = {
                'total_score': total_score,
                'supported_words': supported_count,
                'avg_score': total_score / len(word_results),
            }

        # Determine best fit
        best = max(analysis['hypotheses'].items(), key=lambda x: x[1]['total_score'])
        analysis['overall_interpretation'] = {
            'best_hypothesis': best[0],
            'confidence': 'HIGH' if best[1]['supported_words'] > len(word_results) // 2 else 'MEDIUM',
        }

        return analysis

    def identify_semantic_fields(self) -> dict:
        """
        Identify semantic fields using PMI associations.

        High-PMI word pairs likely belong to the same semantic field.
        This can help interpret unknown words by their company.
        """
        semantic_fields = {
            'administrative': [],
            'religious': [],
            'commodity': [],
            'personnel': [],
            'uncertain': [],
        }

        # Known markers for each field
        admin_markers = ['KU-RO', 'KI-RO', 'SA-RA₂', 'DA-RE']
        religious_markers = ['JA-SA-SA-RA-ME', 'A-TA-I-*301-WA-JA', 'I-PI-NA-MA', 'SI-RU-TE']
        commodity_markers = ['GRA', 'VIN', 'OLE', 'OLIV', 'CYP']

        # Classify words by their associations
        for word, associations in self.high_pmi_pairs.items():
            field = 'uncertain'

            for assoc in associations:
                related = assoc['related_word']

                if any(m in word.upper() or m in related.upper() for m in admin_markers):
                    field = 'administrative'
                    break
                elif any(m in word.upper() or m in related.upper() for m in religious_markers):
                    field = 'religious'
                    break
                elif any(m in related.upper() for m in commodity_markers):
                    field = 'commodity'
                    break

            entry = {
                'word': word,
                'top_associations': associations[:3],
                'in_formula': word in self.formulaic_words,
            }
            semantic_fields[field].append(entry)

        # Sort by number of associations
        for field in semantic_fields:
            semantic_fields[field].sort(
                key=lambda x: len(x['top_associations']),
                reverse=True
            )

        return semantic_fields

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
        4. Check for typical Semitic morphological patterns
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
            # Flexible matching: exact, contains, or partial overlap
            if consonants == root:
                match_type = 'exact'
                score_mult = 1.0
            elif consonants in root or root in consonants:
                match_type = 'partial'
                score_mult = 0.7
            elif len(consonants) >= 2 and len(root) >= 2:
                # Check for 2-consonant overlap
                if consonants[:2] == root[:2]:
                    match_type = 'initial_match'
                    score_mult = 0.5
                else:
                    continue
            else:
                continue

            result['root_matches'].append({
                'semitic_root': root,
                'semitic_word': sem_word,
                'meaning': data['meaning'],
                'confidence': data['confidence'],
                'match_type': match_type,
                'source': data.get('source', 'Unknown'),
            })

            base_score = 2 if data['confidence'] == 'HIGH' else (1 if data['confidence'] == 'MEDIUM' else 0.5)
            result['score'] += base_score * score_mult

        # Check for triconsonantal structure (characteristic of Semitic)
        if len(consonants) == 3:
            result['evidence'].append({
                'type': 'structure',
                'observation': f'Triconsonantal skeleton: {consonants}',
                'interpretation': 'Compatible with Semitic triliteral root structure',
                'confidence': 'MEDIUM',
            })
            result['score'] += 0.75

        # Check for biconsonantal (common in early Semitic administrative terms)
        elif len(consonants) == 2:
            result['evidence'].append({
                'type': 'structure',
                'observation': f'Biconsonantal skeleton: {consonants}',
                'interpretation': 'Compatible with biconsonantal Semitic roots (KL, QR, etc.)',
                'confidence': 'LOW',
            })
            result['score'] += 0.25

        # K-R pattern special case (ku-ro = *kull "all")
        if consonants in ['KR', 'KL', 'KLL']:
            result['evidence'].append({
                'type': 'cognate',
                'observation': 'K-R/K-L skeleton',
                'interpretation': 'Matches Semitic *kull/*kol "all, total" (HIGH evidence)',
                'confidence': 'HIGH',
            })
            result['score'] += 2

        # G-R pattern (ki-ro possibly *gara "diminish")
        if consonants in ['KR', 'GR']:
            result['evidence'].append({
                'type': 'cognate',
                'observation': 'G-R skeleton',
                'interpretation': 'Matches Semitic *gara "to diminish, deficit"',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # S-P pattern (collecting/gathering verbs)
        if 'SP' in consonants or consonants == 'SP':
            result['evidence'].append({
                'type': 'cognate',
                'observation': 'S-P skeleton',
                'interpretation': 'Matches Semitic *ʾsp "to gather, collect"',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # Determine verdict with more nuanced thresholds
        if result['score'] >= 2.5:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1.5:
            result['verdict'] = 'POSSIBLE'
        elif result['score'] >= 0.5:
            result['verdict'] = 'WEAK'
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
        - Pre-Greek vocabulary matches (Beekes, Furnée)
        """
        result = {
            'hypothesis': 'Pre-Greek Substrate',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'markers_found': [],
            'vocabulary_matches': [],
        }

        word_upper = word.upper()
        word_lower = word.lower()
        syllables = word_upper.split('-')
        reconstructed = ''.join(syllables).lower()

        # Check for Pre-Greek phonological markers
        for marker, data in PREGREEK_MARKERS.items():
            marker_upper = marker.upper()
            # Check in concatenated form or original
            if marker_upper in word_upper or marker.lower() in reconstructed:
                result['markers_found'].append({
                    'marker': marker,
                    'type': data['type'],
                    'significance': data['significance'],
                    'examples': data['examples'],
                })
                if data['significance'] == 'HIGH':
                    result['score'] += 2
                elif data['significance'] == 'MEDIUM':
                    result['score'] += 1
                else:
                    result['score'] += 0.5

        # Check for Pre-Greek vocabulary matches
        for vocab, data in PREGREEK_VOCABULARY.items():
            # Normalize for comparison
            vocab_norm = vocab.lower().replace('-', '')
            if vocab_norm in reconstructed or reconstructed in vocab_norm:
                result['vocabulary_matches'].append({
                    'vocabulary': vocab,
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                    'source': data.get('source', 'Beekes'),
                })
                base_score = 1.5 if data['confidence'] == 'HIGH' else (1 if data['confidence'] == 'MEDIUM' else 0.5)
                result['score'] += base_score

        # Check for vowel alternations (a/e, i/e) characteristic of Pre-Greek
        vowel_alternation = False
        for i, syl in enumerate(syllables[:-1]):
            if len(syl) >= 1 and len(syllables[i+1]) >= 1:
                # Get final vowel of each syllable
                v1 = syl[-1] if syl[-1] in 'AEIOU' else ''
                v2 = syllables[i+1][-1] if syllables[i+1][-1] in 'AEIOU' else ''
                # Check for Pre-Greek alternation patterns
                for alt in PREGREEK_PHONOLOGY.get('vowel_alternation', []):
                    parts = alt.split('/')
                    if len(parts) == 2:
                        if (v1.lower() == parts[0] and v2.lower() == parts[1]) or \
                           (v1.lower() == parts[1] and v2.lower() == parts[0]):
                            vowel_alternation = True
                            break

        if vowel_alternation:
            result['evidence'].append({
                'type': 'phonology',
                'observation': 'Vowel alternation pattern',
                'interpretation': 'Characteristic of Pre-Greek words (a/e, i/e alternation)',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # Check for prothetic vowels (word-initial a-, e- before consonant cluster)
        if len(syllables) >= 2:
            first = syllables[0]
            if first in ['A', 'E'] and len(syllables[1]) >= 2:
                result['evidence'].append({
                    'type': 'phonology',
                    'observation': 'Possible prothetic vowel',
                    'interpretation': 'Word-initial vowel before consonant cluster (Pre-Greek feature)',
                    'confidence': 'LOW',
                })
                result['score'] += 0.5

        # Check for double consonants in syllable structure (written as ta-ta, sa-sa, etc.)
        for i in range(len(syllables) - 1):
            if syllables[i] == syllables[i+1]:
                result['evidence'].append({
                    'type': 'phonology',
                    'observation': f'Gemination: {syllables[i]}-{syllables[i+1]}',
                    'interpretation': 'Possible geminate consonant (Pre-Greek feature)',
                    'confidence': 'LOW',
                })
                result['score'] += 0.5
                break

        # Determine verdict with calibrated thresholds
        if result['score'] >= 2.5:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1.5:
            result['verdict'] = 'POSSIBLE'
        elif result['score'] >= 0.5:
            result['verdict'] = 'WEAK'
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
        - Linear B cognates (exact and partial matches)
        - Greek lexical matches
        - Greek morphological patterns
        - Vowel distribution consistency with Greek
        """
        result = {
            'hypothesis': 'Proto-Greek',
            'score': 0,
            'verdict': 'NEUTRAL',
            'evidence': [],
            'greek_cognates': [],
            'negative_evidence': [],
        }

        word_upper = word.upper()
        syllables = word_upper.split('-')

        # Check Greek lexicon for Linear B cognates
        for greek_word, data in GREEK_LEXICON.items():
            linear_b = data.get('Linear_B', '').upper()
            if not linear_b:
                continue

            linear_b_norm = linear_b.replace('-', '')
            word_norm = word_upper.replace('-', '')

            # Exact match
            if word_upper == linear_b:
                result['greek_cognates'].append({
                    'greek': greek_word,
                    'linear_b': data.get('Linear_B'),
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                    'match_type': 'exact',
                    'source': data.get('source', 'Unknown'),
                })
                base_score = 2.5 if data['confidence'] == 'HIGH' else (1.5 if data['confidence'] == 'MEDIUM' else 0.75)
                result['score'] += base_score

            # Partial match (word is substring or Linear B is substring)
            elif word_norm in linear_b_norm or linear_b_norm in word_norm:
                result['greek_cognates'].append({
                    'greek': greek_word,
                    'linear_b': data.get('Linear_B'),
                    'meaning': data['meaning'],
                    'confidence': data['confidence'],
                    'match_type': 'partial',
                    'source': data.get('source', 'Unknown'),
                })
                base_score = 1.5 if data['confidence'] == 'HIGH' else (1 if data['confidence'] == 'MEDIUM' else 0.5)
                result['score'] += base_score

            # Initial syllable match (for word roots)
            elif len(syllables) >= 1 and len(linear_b.split('-')) >= 1:
                if syllables[0] == linear_b.split('-')[0]:
                    result['greek_cognates'].append({
                        'greek': greek_word,
                        'linear_b': data.get('Linear_B'),
                        'meaning': data['meaning'],
                        'confidence': data['confidence'],
                        'match_type': 'initial',
                        'source': data.get('source', 'Unknown'),
                    })
                    result['score'] += 0.5

        # Check for Greek-like case endings
        greek_endings = {
            '-o': ('nominative/accusative neuter', 'LOW'),
            '-a': ('nominative feminine', 'LOW'),
            '-as': ('genitive masculine', 'MEDIUM'),
            '-os': ('nominative masculine', 'LOW'),
            '-e': ('vocative/dative', 'LOW'),
            '-i': ('dative', 'LOW'),
            '-oi': ('nominative plural masculine', 'MEDIUM'),
            '-ai': ('nominative plural feminine', 'MEDIUM'),
            '-es': ('nominative plural', 'MEDIUM'),
        }

        word_lower = word.lower()
        for ending, (meaning, conf) in greek_endings.items():
            ending_check = ending.replace('-', '')
            if word_lower.endswith(ending_check):
                result['evidence'].append({
                    'type': 'morphology',
                    'observation': f'Ending {ending}',
                    'interpretation': f'Potentially Greek {meaning}',
                    'confidence': conf,
                })
                score_add = 0.5 if conf == 'MEDIUM' else 0.25
                result['score'] += score_add
                break  # Only count one ending

        # Special case: ku-ro
        if word_upper == 'KU-RO':
            result['evidence'].append({
                'type': 'functional',
                'observation': 'ku-ro totaling function',
                'interpretation': 'Parallels Linear B administrative ku-ro; may relate to Greek kyrios or *kolos',
                'confidence': 'MEDIUM',
            })
            result['score'] += 1

        # NEGATIVE EVIDENCE: Low /o/ frequency problem
        # If word contains O, check pattern (Linear A has very low /o/)
        syllables_with_o = [s for s in syllables if 'O' in s]
        # This is actually positive for Greek if /o/ appears
        if syllables_with_o:
            result['evidence'].append({
                'type': 'phonology',
                'observation': f'Contains /o/ syllable(s): {syllables_with_o}',
                'interpretation': 'Presence of /o/ slightly favors Greek (expected ~20% in Greek vs ~3% in Linear A overall)',
                'confidence': 'LOW',
            })
            result['score'] += 0.25

        # Check for expected Greek vocabulary not found
        # (This is for negative evidence tracking)
        if word_upper in ['MA-TE', 'PA-TE', 'WA-NA-KA']:
            # These would be very strong Greek evidence
            pass  # Already matched above

        # Determine verdict with calibrated thresholds
        if result['score'] >= 2.5:
            result['verdict'] = 'SUPPORTED'
        elif result['score'] >= 1.5:
            result['verdict'] = 'POSSIBLE'
        elif result['score'] >= 0.5:
            result['verdict'] = 'WEAK'
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
            'contextual_info': {},
        }

        # Add contextual data if available
        if self.formulaic_words or self.high_pmi_pairs:
            word_upper = word.upper()
            analysis['contextual_info'] = {
                'in_formula': word in self.formulaic_words or word_upper in self.formulaic_words,
                'related_words': [],
            }

            # Check for PMI associations
            if word in self.high_pmi_pairs:
                analysis['contextual_info']['related_words'] = self.high_pmi_pairs[word][:3]
            elif word_upper in self.high_pmi_pairs:
                analysis['contextual_info']['related_words'] = self.high_pmi_pairs[word_upper][:3]

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
        # Load contextual data for enhanced analysis
        self.load_contextual_data()

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

        # Add contextual analysis results
        if self.formulaic_words or self.high_pmi_pairs:
            self.results['contextual_analysis'] = {
                'formulaic_words_count': len(self.formulaic_words),
                'pmi_pairs_count': len(self.high_pmi_pairs),
                'semantic_fields': self.identify_semantic_fields(),
            }

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
