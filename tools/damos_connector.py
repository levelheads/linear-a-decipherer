#!/usr/bin/env python3
"""
DĀMOS Connector for Linear A Decipherment Project

Connects to DĀMOS (Database of Mycenaean at Oslo) for Linear B verification.
Provides comprehensive reference data for validating Linear A cognate claims.

Since DĀMOS is a web application without a public API, this connector:
1. Maintains a comprehensive static dictionary of Linear B vocabulary
2. Cross-references against the existing cognates.json from lineara.xyz
3. Provides theophoric name verification data
4. Supports onomastic pattern analysis

Sources:
- DĀMOS (damos.hf.uio.no) - 6,000+ Linear B tablets
- Aura Jorro, Diccionario Micénico (1985-1993)
- Ventris & Chadwick, Documents in Mycenaean Greek (1973)
- Palmer, The Interpretation of Mycenaean Greek Texts (1963)
- Killen, Linear B Tablets and Mycenaean Economy (2008)

Usage:
    python tools/damos_connector.py --verify da-ma-te     # Verify theophoric name
    python tools/damos_connector.py --theophoric         # List all theophoric names
    python tools/damos_connector.py --cognates           # Cross-check cognates
    python tools/damos_connector.py --stats              # Show vocabulary stats

Attribution:
    Part of Linear A Decipherment Project (Phase 6-7)
    Linear B data from published academic sources
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LINEAR_B_DIR = DATA_DIR / "linear_b"
COGNATES_FILE = DATA_DIR / "cognates.json"
OUTPUT_FILE = LINEAR_B_DIR / "cognate_verification.json"


@dataclass
class LinearBEntry:
    """Represents a Linear B word with full attestation data."""
    word: str                              # The Linear B word
    meaning: str                           # Primary meaning/translation
    greek: str = ""                        # Greek equivalent if known
    tablets: List[str] = field(default_factory=list)  # Tablet attestations
    sites: List[str] = field(default_factory=list)    # Sites (KN, PY, MY, TH)
    category: str = ""                     # Semantic category
    divine_element: str = ""               # Divine element if theophoric
    is_theophoric: bool = False            # Is this a theophoric name?
    is_toponym: bool = False               # Is this a place name?
    linear_a_cognate: str = ""             # Corresponding Linear A form
    notes: str = ""                        # Additional notes
    confidence: str = "HIGH"               # Confidence level
    source: str = ""                       # Primary reference


class DAMOSConnector:
    """
    Connector for Linear B verification data.

    Provides comprehensive vocabulary for validating Linear A cognate claims,
    with special focus on theophoric names and administrative vocabulary.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.vocabulary: Dict[str, Dict] = {}
        self.cognates: Dict = {}
        self._ensure_dirs()
        self._build_vocabulary()
        self._load_cognates()

    def _ensure_dirs(self):
        """Create necessary directories."""
        LINEAR_B_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "info"):
        """Log message if verbose."""
        if self.verbose:
            getattr(logger, level)(msg)

    def _load_cognates(self):
        """Load existing cognates from cognates.json."""
        try:
            if COGNATES_FILE.exists():
                with open(COGNATES_FILE, 'r', encoding='utf-8') as f:
                    self.cognates = json.load(f)
                self.log(f"Loaded {len(self.cognates.get('identicalWords', {}))} cognates")
        except Exception as e:
            self.log(f"Error loading cognates: {e}", "warning")

    def _build_vocabulary(self):
        """
        Build comprehensive Linear B vocabulary from published sources.

        Focus areas for Linear A verification:
        1. Theophoric names (divine elements)
        2. Administrative vocabulary
        3. Toponyms
        4. Commodity terms
        5. Personnel/occupational terms
        """

        self.log("Building Linear B vocabulary...")

        # ============================================================
        # THEOPHORIC NAMES AND DIVINE VOCABULARY
        # Critical for verifying Linear A religious readings
        # ============================================================

        theophoric = {
            'da-ma-te': {
                'word': 'da-ma-te',
                'meaning': 'Demeter (goddess of grain/harvest)',
                'greek': 'Δημήτηρ (Dēmētēr)',
                'tablets': ['PY En 609', 'PY Eo 224'],
                'sites': ['PY'],
                'category': 'divine_name',
                'divine_element': 'da-ma-te',
                'is_theophoric': True,
                'linear_a_cognate': 'DA-MA-TE',
                'notes': 'Appears as da-ma-te at Pylos. The Linear A DA-MA-TE at peak sanctuary PKZ may be the earliest attestation of Demeter worship. Etymology disputed: either "grain mother" (*dā- + mātēr) or Pre-Greek.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I pp.153-154; Ventris-Chadwick p.126'
            },
            'a-ta-na-po-ti-ni-ja': {
                'word': 'a-ta-na-po-ti-ni-ja',
                'meaning': 'Athena Potnia (Lady Athena)',
                'greek': 'Ἀθηνᾶ Πότνια',
                'tablets': ['KN V 52'],
                'sites': ['KN'],
                'category': 'divine_name',
                'divine_element': 'a-ta-na',
                'is_theophoric': True,
                'linear_a_cognate': 'A-TA-NA',
                'notes': 'Full divine title at Knossos. The element a-ta-na appears independently and in compounds. Linear A A-TA-NA and A-TA-NA-TE at Hagia Triada suggest Athena worship in Minoan period.',
                'confidence': 'HIGH',
                'source': 'KT5; Ventris-Chadwick p.126'
            },
            'po-ti-ni-ja': {
                'word': 'po-ti-ni-ja',
                'meaning': 'Potnia (Lady, Mistress) - divine title',
                'greek': 'πότνια (potnia)',
                'tablets': ['KN Gg 702', 'PY Tn 316', 'PY Fr 1206', 'MY Oi 701'],
                'sites': ['KN', 'PY', 'MY'],
                'category': 'divine_title',
                'divine_element': 'po-ti-ni-ja',
                'is_theophoric': False,
                'notes': 'Common divine title; appears alone and with qualifiers (a-ta-na-po-ti-ni-ja, da-pu-ri-to-jo-po-ti-ni-ja). May correspond to Linear A goddess titles.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic II pp.141-142'
            },
            'di-we': {
                'word': 'di-we',
                'meaning': 'Zeus (dative: "to Zeus")',
                'greek': 'Διί (dat. of Ζεύς)',
                'tablets': ['KN Fp 1', 'PY Tn 316', 'PY Un 718'],
                'sites': ['KN', 'PY'],
                'category': 'divine_name',
                'divine_element': 'di-we/di-wo',
                'is_theophoric': True,
                'notes': 'Zeus appears frequently in offerings tablets. The di- element appears in theophoric names.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I pp.178-179'
            },
            'di-wo-nu-so': {
                'word': 'di-wo-nu-so',
                'meaning': 'Dionysus (god of wine)',
                'greek': 'Διόνυσος',
                'tablets': ['PY Xa 102', 'KN Xb 1419'],
                'sites': ['PY', 'KN'],
                'category': 'divine_name',
                'divine_element': 'di-wo-nu-so',
                'is_theophoric': True,
                'notes': 'Attested at both Pylos and Knossos. Important for wine-related vocabulary comparison with Linear A.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I pp.181-182'
            },
            'e-ra': {
                'word': 'e-ra',
                'meaning': 'Hera (goddess)',
                'greek': 'Ἥρα',
                'tablets': ['PY Tn 316', 'TH Of 36'],
                'sites': ['PY', 'TH'],
                'category': 'divine_name',
                'divine_element': 'e-ra',
                'is_theophoric': True,
                'notes': 'Appears in offerings contexts. May have Pre-Greek etymology.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.232'
            },
            'a-re': {
                'word': 'a-re',
                'meaning': 'Ares (god of war)',
                'greek': 'Ἄρης',
                'tablets': ['KN Fp 14', 'KN V 52'],
                'sites': ['KN'],
                'category': 'divine_name',
                'divine_element': 'a-re',
                'is_theophoric': True,
                'notes': 'War god. Element appears in theophoric names.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.93'
            },
            'po-se-da-o': {
                'word': 'po-se-da-o',
                'meaning': 'Poseidon (god of sea/earthquakes)',
                'greek': 'Ποσειδῶν',
                'tablets': ['PY Tn 316', 'KN M 719', 'PY Es 650'],
                'sites': ['PY', 'KN'],
                'category': 'divine_name',
                'divine_element': 'po-se-da-o',
                'is_theophoric': True,
                'notes': 'Major deity at Pylos. Etymology may be Pre-Greek (*potis + *da "lord of earth").',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic II pp.139-140'
            },
            'pa-ja-wo': {
                'word': 'pa-ja-wo',
                'meaning': 'Paean/Apollo (healer god)',
                'greek': 'Παιάων',
                'tablets': ['KN V 52'],
                'sites': ['KN'],
                'category': 'divine_name',
                'divine_element': 'pa-ja-wo',
                'is_theophoric': True,
                'notes': 'Early form of Apollo as healer. Pre-Greek name.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic II p.16'
            },
            'e-nu-wa-ri-jo': {
                'word': 'e-nu-wa-ri-jo',
                'meaning': 'Enyalios (war god)',
                'greek': 'Ἐνυάλιος',
                'tablets': ['KN V 52'],
                'sites': ['KN'],
                'category': 'divine_name',
                'divine_element': 'e-nu-wa-ri-jo',
                'is_theophoric': True,
                'notes': 'War deity, sometimes identified with Ares.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.227'
            },
            'ma-na-sa': {
                'word': 'ma-na-sa',
                'meaning': 'possibly a goddess (Manasa?)',
                'greek': 'uncertain',
                'tablets': ['PY Fr 1225'],
                'sites': ['PY'],
                'category': 'divine_name',
                'divine_element': 'ma-na-sa',
                'is_theophoric': True,
                'notes': 'Receives oil offerings. Possibly Pre-Greek divinity.',
                'confidence': 'MEDIUM',
                'source': 'Aura Jorro DMic II p.20'
            },
            'i-pe-me-de-ja': {
                'word': 'i-pe-me-de-ja',
                'meaning': 'Iphimedeia (goddess/heroine)',
                'greek': 'Ἰφιμέδεια',
                'tablets': ['PY Tn 316'],
                'sites': ['PY'],
                'category': 'divine_name',
                'divine_element': 'i-pe-me-de-ja',
                'is_theophoric': True,
                'notes': 'Receives gold offerings at Pylos. Later known as mother of Otus and Ephialtes.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.312'
            },
            'di-u-ja': {
                'word': 'di-u-ja',
                'meaning': 'Diwia (female counterpart of Zeus)',
                'greek': 'Διϝία',
                'tablets': ['PY Tn 316', 'KN F 51'],
                'sites': ['PY', 'KN'],
                'category': 'divine_name',
                'divine_element': 'di-u-ja',
                'is_theophoric': True,
                'notes': 'Female Zeus. Important for -JA suffix analysis in Linear A.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.179'
            },
        }

        # ============================================================
        # ADMINISTRATIVE VOCABULARY
        # For validating Linear A ku-ro, ki-ro, etc.
        # ============================================================

        administrative = {
            'to-so': {
                'word': 'to-so',
                'meaning': 'so much, total (masculine)',
                'greek': 'τόσος (tosos)',
                'tablets': ['PY An 1', 'KN As 1517', 'MY Ge 602'],
                'sites': ['PY', 'KN', 'MY'],
                'category': 'totaling',
                'is_theophoric': False,
                'linear_a_cognate': 'KU-RO (functional)',
                'notes': 'Greek totaling term. Linear A uses KU-RO in same position but different form, suggesting non-Greek origin for Linear A.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.560'
            },
            'to-sa': {
                'word': 'to-sa',
                'meaning': 'so much (feminine/neuter plural)',
                'greek': 'τόσα',
                'tablets': ['PY Jn 389', 'KN L 695'],
                'sites': ['PY', 'KN'],
                'category': 'totaling',
                'is_theophoric': False,
                'notes': 'Feminine/neuter form of to-so.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.560'
            },
            'o-pe-ro': {
                'word': 'o-pe-ro',
                'meaning': 'deficit, debt, owed',
                'greek': 'ὄφελος (ophelos)',
                'tablets': ['PY Ma 365', 'PY Un 718', 'KN E 846'],
                'sites': ['PY', 'KN'],
                'category': 'deficit',
                'is_theophoric': False,
                'linear_a_cognate': 'KI-RO (functional)',
                'notes': 'Greek deficit term. Compare with Linear A KI-RO which may serve similar function but has different form.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.504'
            },
            'a-pu-do-si': {
                'word': 'a-pu-do-si',
                'meaning': 'delivery, payment, contribution',
                'greek': 'ἀπόδοσις (apodosis)',
                'tablets': ['PY Ma 90', 'KN C 914'],
                'sites': ['PY', 'KN'],
                'category': 'allocation',
                'is_theophoric': False,
                'notes': 'Technical term for required contributions.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.89'
            },
            'do-so-mo': {
                'word': 'do-so-mo',
                'meaning': 'contribution, offering',
                'greek': 'δοσμός',
                'tablets': ['PY Un 718', 'PY Es 644'],
                'sites': ['PY'],
                'category': 'allocation',
                'is_theophoric': False,
                'notes': 'Technical term for contributions to palace/sanctuary.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.189'
            },
            'wo-ze': {
                'word': 'wo-ze',
                'meaning': 'he works, produces',
                'greek': 'ϝέργει (*werzei > ἔρδει)',
                'tablets': ['PY An 18', 'PY Jn 829'],
                'sites': ['PY'],
                'category': 'work',
                'is_theophoric': False,
                'notes': 'Work/production term. Compare Linear A A-DU contexts.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.592'
            },
            'e-ke': {
                'word': 'e-ke',
                'meaning': 'holds, possesses',
                'greek': 'ἔχει (ekhei)',
                'tablets': ['PY Eb 294', 'PY Ep 704', 'KN Am 821'],
                'sites': ['PY', 'KN'],
                'category': 'possession',
                'is_theophoric': False,
                'notes': 'Common land-holding term.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.438'
            },
            'pa-ro': {
                'word': 'pa-ro',
                'meaning': 'from, beside, with',
                'greek': 'παρά (para)',
                'tablets': ['PY Eb 297', 'KN As 1516'],
                'sites': ['PY', 'KN'],
                'category': 'preposition',
                'is_theophoric': False,
                'notes': 'Indicates source/origin in transactions.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.517'
            },
        }

        # ============================================================
        # TOPONYMS
        # For cross-referencing place names
        # ============================================================

        toponyms = {
            'pa-i-to': {
                'word': 'pa-i-to',
                'meaning': 'Phaistos (city in Crete)',
                'greek': 'Φαιστός',
                'tablets': ['KN Db 1159', 'KN Da 1164', 'KN Sd 4413'],
                'sites': ['KN'],
                'category': 'toponym',
                'is_toponym': True,
                'linear_a_cognate': 'PA-I-TO',
                'notes': 'Major Minoan/Mycenaean site. CERTAIN anchor reading. Identical in Linear A and B.',
                'confidence': 'CERTAIN',
                'source': 'Ventris-Chadwick p.410'
            },
            'ku-do-ni-ja': {
                'word': 'ku-do-ni-ja',
                'meaning': 'Kydonia (Chania, western Crete)',
                'greek': 'Κυδωνία',
                'tablets': ['KN C 902', 'KN Db 1186'],
                'sites': ['KN'],
                'category': 'toponym',
                'is_toponym': True,
                'linear_a_cognate': 'KU-DO-NI-JA',
                'notes': 'Major Minoan/Mycenaean city. CERTAIN anchor reading. Identical in Linear A and B.',
                'confidence': 'CERTAIN',
                'source': 'Ventris-Chadwick p.400'
            },
            'ko-no-so': {
                'word': 'ko-no-so',
                'meaning': 'Knossos (palace city)',
                'greek': 'Κνωσός',
                'tablets': ['KN As 1516', 'KN Dv 1295'],
                'sites': ['KN'],
                'category': 'toponym',
                'is_toponym': True,
                'notes': 'Principal Minoan palace. Pre-Greek name.',
                'confidence': 'CERTAIN',
                'source': 'Ventris-Chadwick p.393'
            },
            'a-mi-ni-so': {
                'word': 'a-mi-ni-so',
                'meaning': 'Amnisos (port of Knossos)',
                'greek': 'Ἀμνισός',
                'tablets': ['KN Gg 5 702', 'KN M 719'],
                'sites': ['KN'],
                'category': 'toponym',
                'is_toponym': True,
                'notes': 'Harbor town. Important port for Knossos.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.143'
            },
            'tu-ri-so': {
                'word': 'tu-ri-so',
                'meaning': 'Tylissos (Cretan city)',
                'greek': 'Τύλισος',
                'tablets': ['KN C 902', 'KN Dv 1325'],
                'sites': ['KN'],
                'category': 'toponym',
                'is_toponym': True,
                'notes': 'Major Minoan site west of Knossos.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.552'
            },
            'pu-ro': {
                'word': 'pu-ro',
                'meaning': 'Pylos (Mycenaean palace)',
                'greek': 'Πύλος',
                'tablets': ['PY An 1', 'PY Eb 294'],
                'sites': ['PY'],
                'category': 'toponym',
                'is_toponym': True,
                'notes': 'Major Mycenaean palace on mainland Greece. Largest Linear B archive.',
                'confidence': 'CERTAIN',
                'source': 'Ventris-Chadwick p.421'
            },
        }

        # ============================================================
        # COMMODITIES AND MEASURES
        # ============================================================

        commodities = {
            'wo-no': {
                'word': 'wo-no',
                'meaning': 'wine',
                'greek': 'ϝοῖνος (woinos > οἶνος)',
                'tablets': ['PY Un 718', 'KN Uc 160'],
                'sites': ['PY', 'KN'],
                'category': 'commodity',
                'is_theophoric': False,
                'linear_a_cognate': 'YA-NE (speculative)',
                'notes': 'Greek wine term. Compare Linear A ya-ne (possible Semitic loan).',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.592'
            },
            'e-ra-wo': {
                'word': 'e-ra-wo',
                'meaning': 'olive oil, fat',
                'greek': 'ἔλαιϝον (elaiwon > ἔλαιον)',
                'tablets': ['PY Fr 1184', 'KN Fh 347'],
                'sites': ['PY', 'KN'],
                'category': 'commodity',
                'is_theophoric': False,
                'notes': 'Olive oil. Most common commodity in Linear B tablets.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.441'
            },
            'me-ri': {
                'word': 'me-ri',
                'meaning': 'honey',
                'greek': 'μέλι (meli)',
                'tablets': ['KN Gg 702', 'PY Un 718'],
                'sites': ['KN', 'PY'],
                'category': 'commodity',
                'is_theophoric': False,
                'notes': 'Honey offerings common in religious contexts.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.477'
            },
            'si-to': {
                'word': 'si-to',
                'meaning': 'grain, wheat',
                'greek': 'σῖτος (sitos)',
                'tablets': ['PY An 724', 'KN F 841'],
                'sites': ['PY', 'KN'],
                'category': 'commodity',
                'is_theophoric': False,
                'notes': 'Grain/cereal. Related to GRA logogram.',
                'confidence': 'HIGH',
                'source': 'Ventris-Chadwick p.543'
            },
        }

        # ============================================================
        # PERSONAL NAMES WITH THEOPHORIC ELEMENTS
        # ============================================================

        theophoric_names = {
            'di-wi-je-u': {
                'word': 'di-wi-je-u',
                'meaning': 'Zeus-devotee (personal name)',
                'greek': 'Διϝιεύς',
                'tablets': ['PY An 654'],
                'sites': ['PY'],
                'category': 'personal_name',
                'divine_element': 'di-wi/di-we',
                'is_theophoric': True,
                'notes': 'Name containing Zeus element. Pattern for identifying theophoric names.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.179'
            },
            'po-se-da-wo-ne': {
                'word': 'po-se-da-wo-ne',
                'meaning': 'Poseidon-related (personal name)',
                'greek': 'Ποσειδάϝωνος related',
                'tablets': ['PY Tn 316'],
                'sites': ['PY'],
                'category': 'personal_name',
                'divine_element': 'po-se-da-o',
                'is_theophoric': True,
                'notes': 'Name with Poseidon element.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic II p.140'
            },
            'a-ta-na-to': {
                'word': 'a-ta-na-to',
                'meaning': 'Athena-related (personal name?)',
                'tablets': ['KN V 280'],
                'sites': ['KN'],
                'category': 'personal_name',
                'divine_element': 'a-ta-na',
                'is_theophoric': True,
                'linear_a_cognate': 'A-TA-NA-TE',
                'notes': 'Contains Athena element. Compare Linear A A-TA-NA-TE.',
                'confidence': 'MEDIUM',
                'source': 'Aura Jorro DMic I p.120'
            },
            'a-re-i-me-ne': {
                'word': 'a-re-i-me-ne',
                'meaning': 'Ares-minded (personal name)',
                'greek': 'Ἀρηΐμενης',
                'tablets': ['PY An 39'],
                'sites': ['PY'],
                'category': 'personal_name',
                'divine_element': 'a-re',
                'is_theophoric': True,
                'notes': 'Theophoric with Ares element.',
                'confidence': 'HIGH',
                'source': 'Aura Jorro DMic I p.93'
            },
        }

        # Combine all categories
        all_vocab = {}
        all_vocab.update(theophoric)
        all_vocab.update(administrative)
        all_vocab.update(toponyms)
        all_vocab.update(commodities)
        all_vocab.update(theophoric_names)

        self.vocabulary = all_vocab
        self.log(f"Built vocabulary with {len(self.vocabulary)} entries")

    def verify_cognate(self, linear_a_word: str) -> Dict:
        """
        Verify a Linear A reading against Linear B data.

        Returns verification result with confidence and evidence.
        """
        word_upper = linear_a_word.upper().replace('_', '-')
        word_lower = linear_a_word.lower().replace('_', '-')

        result = {
            'linear_a_word': linear_a_word,
            'verified': False,
            'linear_b_matches': [],
            'cognates_json_matches': [],
            'confidence': 'NOT_FOUND',
            'evidence': [],
            'notes': ''
        }

        # Check vocabulary for direct matches
        for word, data in self.vocabulary.items():
            # Check if this Linear B word has this Linear A as cognate
            if data.get('linear_a_cognate', '').upper() == word_upper:
                result['verified'] = True
                result['linear_b_matches'].append({
                    'word': word,
                    'meaning': data['meaning'],
                    'tablets': data.get('tablets', []),
                    'sites': data.get('sites', []),
                    'source': data.get('source', ''),
                    'notes': data.get('notes', '')
                })
                result['confidence'] = data.get('confidence', 'MEDIUM')

        # Check cognates.json for identical words
        identical = self.cognates.get('identicalWords', {})
        if word_upper in identical or word_lower in identical:
            key = word_upper if word_upper in identical else word_lower
            tablets = identical[key]
            result['cognates_json_matches'] = tablets
            if not result['verified']:
                result['verified'] = True
                result['confidence'] = 'HIGH' if len(tablets) > 3 else 'MEDIUM'
            result['evidence'].append(f"Found in cognates.json with {len(tablets)} Linear B attestations")

        # Add notes
        if result['verified']:
            result['notes'] = f"Linear B verification successful with {len(result['linear_b_matches'])} vocabulary matches and {len(result['cognates_json_matches'])} corpus attestations."
        else:
            result['notes'] = "No direct Linear B cognate found. This does not invalidate the reading but limits anchoring."

        return result

    def get_theophoric_names(self) -> List[Dict]:
        """Get all theophoric names and divine vocabulary."""
        return [
            {
                'word': word,
                'meaning': data['meaning'],
                'divine_element': data.get('divine_element', ''),
                'linear_a_cognate': data.get('linear_a_cognate', ''),
                'sites': data.get('sites', []),
                'confidence': data.get('confidence', 'MEDIUM')
            }
            for word, data in self.vocabulary.items()
            if data.get('is_theophoric', False) or data.get('category') == 'divine_name'
        ]

    def get_toponyms(self) -> List[Dict]:
        """Get all verified toponyms."""
        return [
            {
                'word': word,
                'meaning': data['meaning'],
                'linear_a_cognate': data.get('linear_a_cognate', ''),
                'sites': data.get('sites', []),
                'confidence': data.get('confidence', 'MEDIUM')
            }
            for word, data in self.vocabulary.items()
            if data.get('is_toponym', False)
        ]

    def get_administrative_vocabulary(self) -> List[Dict]:
        """Get administrative vocabulary for comparing with Linear A."""
        return [
            {
                'word': word,
                'meaning': data['meaning'],
                'greek': data.get('greek', ''),
                'linear_a_cognate': data.get('linear_a_cognate', ''),
                'category': data.get('category', ''),
                'notes': data.get('notes', '')
            }
            for word, data in self.vocabulary.items()
            if data.get('category') in ['totaling', 'deficit', 'allocation', 'work', 'possession', 'preposition']
        ]

    def verify_all_phase4_names(self, names_file: Path = None) -> Dict:
        """
        Verify Phase 4 personal names against Linear B data.

        Returns verification report for the 127 identified names.
        """
        if names_file is None:
            names_file = DATA_DIR / "personal_names_comprehensive.json"

        try:
            with open(names_file, 'r', encoding='utf-8') as f:
                names_data = json.load(f)
        except Exception as e:
            return {'error': f"Could not load names file: {e}"}

        names = names_data.get('names', {})

        results = {
            'total_names': len(names),
            'verified_with_lb': [],
            'no_lb_match': [],
            'theophoric_matches': [],
            'summary': {}
        }

        for name, data in names.items():
            verification = self.verify_cognate(name)

            if verification['verified']:
                results['verified_with_lb'].append({
                    'linear_a': name,
                    'linear_b_attestations': verification['cognates_json_matches'],
                    'hypothesis': data.get('best_hypothesis', 'unknown'),
                    'occurrences': data.get('occurrences', 0)
                })
            else:
                results['no_lb_match'].append(name)

            # Check for theophoric elements
            if data.get('name_type') == 'theophoric':
                results['theophoric_matches'].append({
                    'name': name,
                    'divine_element': data.get('morphology', {}).get('root', ''),
                    'lb_verified': verification['verified']
                })

        results['summary'] = {
            'total': len(names),
            'lb_verified': len(results['verified_with_lb']),
            'verification_rate': f"{len(results['verified_with_lb'])/len(names)*100:.1f}%",
            'theophoric_count': len(results['theophoric_matches'])
        }

        return results

    def generate_verification_report(self) -> Dict:
        """Generate comprehensive verification report."""
        report = {
            'generated': datetime.now().isoformat(),
            'source': 'DĀMOS Connector (compiled from published sources)',
            'vocabulary_stats': {
                'total_entries': len(self.vocabulary),
                'theophoric': len(self.get_theophoric_names()),
                'toponyms': len(self.get_toponyms()),
                'administrative': len(self.get_administrative_vocabulary())
            },
            'cognates_stats': {
                'identical_words': len(self.cognates.get('identicalWords', {}))
            },
            'theophoric_vocabulary': self.get_theophoric_names(),
            'toponyms': self.get_toponyms(),
            'administrative_vocabulary': self.get_administrative_vocabulary()
        }

        return report

    def save_verification_data(self):
        """Save verification data to JSON."""
        report = self.generate_verification_report()

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"Saved verification data to {OUTPUT_FILE}")
        return report


def main():
    parser = argparse.ArgumentParser(
        description='DĀMOS Connector - Linear B verification for Linear A research'
    )
    parser.add_argument('--verify', '-v', type=str, help='Verify a Linear A word against Linear B')
    parser.add_argument('--theophoric', '-t', action='store_true', help='List theophoric names')
    parser.add_argument('--toponyms', action='store_true', help='List verified toponyms')
    parser.add_argument('--admin', '-a', action='store_true', help='List administrative vocabulary')
    parser.add_argument('--cognates', '-c', action='store_true', help='Verify all Phase 4 names')
    parser.add_argument('--stats', '-s', action='store_true', help='Show vocabulary statistics')
    parser.add_argument('--save', action='store_true', help='Save verification data to JSON')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    connector = DAMOSConnector(verbose=args.verbose)

    if args.verify:
        result = connector.verify_cognate(args.verify)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.theophoric:
        names = connector.get_theophoric_names()
        print(f"\n{'='*60}")
        print("THEOPHORIC NAMES AND DIVINE VOCABULARY")
        print(f"{'='*60}\n")
        for name in names:
            print(f"  {name['word']}: {name['meaning']}")
            if name.get('linear_a_cognate'):
                print(f"    → Linear A: {name['linear_a_cognate']}")
            print()

    elif args.toponyms:
        toponyms = connector.get_toponyms()
        print(f"\n{'='*60}")
        print("VERIFIED TOPONYMS")
        print(f"{'='*60}\n")
        for t in toponyms:
            print(f"  {t['word']}: {t['meaning']} [{t['confidence']}]")
            if t.get('linear_a_cognate'):
                print(f"    → Linear A: {t['linear_a_cognate']}")
            print()

    elif args.admin:
        vocab = connector.get_administrative_vocabulary()
        print(f"\n{'='*60}")
        print("ADMINISTRATIVE VOCABULARY")
        print(f"{'='*60}\n")
        for v in vocab:
            print(f"  {v['word']}: {v['meaning']}")
            if v.get('greek'):
                print(f"    Greek: {v['greek']}")
            if v.get('linear_a_cognate'):
                print(f"    → Linear A comparison: {v['linear_a_cognate']}")
            print()

    elif args.cognates:
        results = connector.verify_all_phase4_names()
        print(f"\n{'='*60}")
        print("PHASE 4 PERSONAL NAMES VERIFICATION")
        print(f"{'='*60}\n")
        print(f"Total names: {results['summary']['total']}")
        print(f"Verified with Linear B: {results['summary']['lb_verified']}")
        print(f"Verification rate: {results['summary']['verification_rate']}")
        print(f"Theophoric names: {results['summary']['theophoric_count']}")
        print(f"\nVerified names:")
        for v in results['verified_with_lb'][:10]:
            print(f"  {v['linear_a']}: {len(v['linear_b_attestations'])} LB attestations")

    elif args.stats:
        report = connector.generate_verification_report()
        print(f"\n{'='*60}")
        print("DĀMOS CONNECTOR STATISTICS")
        print(f"{'='*60}\n")
        print(f"Total vocabulary entries: {report['vocabulary_stats']['total_entries']}")
        print(f"  - Theophoric: {report['vocabulary_stats']['theophoric']}")
        print(f"  - Toponyms: {report['vocabulary_stats']['toponyms']}")
        print(f"  - Administrative: {report['vocabulary_stats']['administrative']}")
        print(f"\nCognates from lineara.xyz: {report['cognates_stats']['identical_words']}")

    elif args.save:
        connector.save_verification_data()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
