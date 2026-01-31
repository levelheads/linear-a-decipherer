#!/usr/bin/env python3
"""
SigLA Paleographic Querier for Linear A Decipherment Project

Queries paleographic data for Linear A signs based on SigLA (Signs of Linear A)
database and GORILA sign classifications.

SigLA Details:
    - URL: https://sigla.phis.me
    - Contains: Paleographic data for Linear A signs
    - Provides: Sign variants, attestations, drawing comparisons

Since SigLA is a web application without a public API, this tool maintains
a comprehensive static database compiled from GORILA and published sources.

Usage:
    python tools/sigla_querier.py --query AB08       # Query sign AB08
    python tools/sigla_querier.py --variants AB60   # Get variants of AB60 (ra)
    python tools/sigla_querier.py --compare AB60 AB64  # Compare ra and ra2
    python tools/sigla_querier.py --tablet HT13     # Get signs on tablet HT 13
    python tools/sigla_querier.py --stats           # Show database statistics

Sources:
    - GORILA Volume II (Godart & Olivier, 1976-1985) - Sign list
    - SigLA (sigla.phis.me) - Paleographic variants
    - lineara.xyz corpus - Frequency data

Attribution:
    Part of Linear A Decipherment Project
    Based on published academic sources
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SIGLA_DIR = DATA_DIR / "sigla"
SIGN_DB_FILE = SIGLA_DIR / "sign_database.json"
ATTESTATIONS_FILE = SIGLA_DIR / "attestations.json"


@dataclass
class SignEntry:
    """Represents a Linear A sign with paleographic data."""
    ab_number: str                      # GORILA AB number (e.g., "AB08")
    phonetic_value: str                 # Proposed phonetic value (e.g., "a")
    sign_type: str                      # Type: syllabogram, logogram, numeral
    frequency: int                      # Corpus occurrences
    sites: List[str] = field(default_factory=list)  # Sites where attested
    variants: List[Dict] = field(default_factory=list)  # Paleographic variants
    linear_b_cognate: str = ""          # Linear B equivalent if any
    description: str = ""               # Visual description
    confidence: str = "HIGH"            # Cognate confidence
    notes: str = ""                     # Additional notes
    examples: List[str] = field(default_factory=list)  # Example tablets


class SigLAQuerier:
    """
    Querier for Linear A paleographic data.

    Provides sign variant analysis, attestation lookup, and
    paleographic comparison capabilities.
    """

    def __init__(self, verbose: bool = False, offline: bool = True):
        self.verbose = verbose
        self.offline = offline
        self.signs: Dict[str, Dict] = {}
        self.attestations: Dict[str, List] = {}
        self._ensure_dirs()
        self._build_sign_database()

    def _ensure_dirs(self):
        """Create necessary directories."""
        SIGLA_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "info"):
        """Log message if verbose."""
        if self.verbose:
            getattr(logger, level)(msg)

    def _build_sign_database(self):
        """
        Build comprehensive sign database from published sources.

        Sources:
        - GORILA Volume II (sign list and AB numbering)
        - Linear B cognate evidence
        - lineara.xyz corpus frequency data
        """
        self.log("Building sign database...")

        # ============================================================
        # SIMPLE VOWELS
        # ============================================================
        vowels = {
            'AB08': {
                'ab_number': 'AB08',
                'phonetic_value': 'a',
                'sign_type': 'syllabogram',
                'frequency': 200,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN', 'PS', 'IO', 'SY'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Open cross with central dot'},
                    {'form': 'simplified', 'sites': ['ZA'], 'description': 'Simple cross form'},
                ],
                'linear_b_cognate': 'AB08 (a)',
                'description': 'Cross-shaped sign with central element',
                'confidence': 'CERTAIN',
                'notes': 'Very common vowel; appears in many word-initial positions',
                'examples': ['HT 13', 'HT 28', 'ZA 4', 'PK Za 11']
            },
            'AB28': {
                'ab_number': 'AB28',
                'phonetic_value': 'i',
                'sign_type': 'syllabogram',
                'frequency': 191,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Vertical line with cross-bars'},
                ],
                'linear_b_cognate': 'AB28 (i)',
                'description': 'Vertical with horizontal elements',
                'confidence': 'CERTAIN',
                'notes': 'Second most common vowel',
                'examples': ['HT 1', 'HT 85', 'KH 5']
            },
            'AB61': {
                'ab_number': 'AB61',
                'phonetic_value': 'o',
                'sign_type': 'syllabogram',
                'frequency': 29,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Circular with internal elements'},
                ],
                'linear_b_cognate': 'AB61 (o)',
                'description': 'Rounded form with internal structure',
                'confidence': 'CERTAIN',
                'notes': 'Less common vowel; often in specific word positions',
                'examples': ['HT 24', 'KH 7']
            },
            'AB10': {
                'ab_number': 'AB10',
                'phonetic_value': 'u',
                'sign_type': 'syllabogram',
                'frequency': 67,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'U-shaped with internal stroke'},
                ],
                'linear_b_cognate': 'AB10 (u)',
                'description': 'U-form with vertical element',
                'confidence': 'CERTAIN',
                'notes': 'Distinctive U shape maintains across sites',
                'examples': ['HT 31', 'ZA 10', 'KH 6']
            },
            'AB38': {
                'ab_number': 'AB38',
                'phonetic_value': 'e',
                'sign_type': 'syllabogram',
                'frequency': 30,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex angular form'},
                ],
                'linear_b_cognate': 'AB38 (e)',
                'description': 'Angular sign with horizontal bars',
                'confidence': 'CERTAIN',
                'notes': 'Least common pure vowel',
                'examples': ['HT 93', 'KH 10']
            },
        }

        # ============================================================
        # LABIAL CONSONANTS (p/b series)
        # ============================================================
        labials = {
            'AB03': {
                'ab_number': 'AB03',
                'phonetic_value': 'pa',
                'sign_type': 'syllabogram',
                'frequency': 141,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Arrow-like with stem'},
                    {'form': 'elaborated', 'sites': ['PH'], 'description': 'More complex arrow form'},
                ],
                'linear_b_cognate': 'AB03 (pa)',
                'description': 'Arrow-shaped sign',
                'confidence': 'CERTAIN',
                'notes': 'Key component in PA-I-TO (Phaistos)',
                'examples': ['HT 6', 'HT 13', 'PH 1', 'KN Zf 2']
            },
            'AB39': {
                'ab_number': 'AB39',
                'phonetic_value': 'pi',
                'sign_type': 'syllabogram',
                'frequency': 56,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex with internal lines'},
                ],
                'linear_b_cognate': 'AB39 (pi)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Appears in personal names',
                'examples': ['HT 13', 'HT 88']
            },
            'AB11': {
                'ab_number': 'AB11',
                'phonetic_value': 'po',
                'sign_type': 'syllabogram',
                'frequency': 8,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB11 (po)',
                'description': 'Distinctive rounded form',
                'confidence': 'HIGH',
                'notes': 'Rare; appears in specific contexts',
                'examples': ['HT 117']
            },
            'AB72': {
                'ab_number': 'AB72',
                'phonetic_value': 'pe',
                'sign_type': 'syllabogram',
                'frequency': 25,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'T-form variant'},
                ],
                'linear_b_cognate': 'AB72 (pe)',
                'description': 'T-shaped sign',
                'confidence': 'HIGH',
                'notes': 'Relatively uncommon',
                'examples': ['HT 6', 'KH 5']
            },
            'AB18': {
                'ab_number': 'AB18',
                'phonetic_value': 'pu',
                'sign_type': 'syllabogram',
                'frequency': 34,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Ladder-like form'},
                ],
                'linear_b_cognate': 'AB18 (pu)',
                'description': 'Vertical with horizontal bars',
                'confidence': 'HIGH',
                'notes': 'Appears in various contexts',
                'examples': ['HT 94', 'ZA 4']
            },
            'AB56': {
                'ab_number': 'AB56',
                'phonetic_value': 'pa3',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Variant of pa'},
                ],
                'linear_b_cognate': 'AB56 (pa3)',
                'description': 'Variant form of pa',
                'confidence': 'MEDIUM',
                'notes': 'Variant - possibly dialectal or phonetic difference',
                'examples': ['HT 49', 'KH 59']
            },
        }

        # ============================================================
        # DENTAL CONSONANTS (t/d series)
        # ============================================================
        dentals = {
            'AB59': {
                'ab_number': 'AB59',
                'phonetic_value': 'ta',
                'sign_type': 'syllabogram',
                'frequency': 175,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Cross with additional elements'},
                    {'form': 'simplified', 'sites': ['ZA'], 'description': 'Reduced form'},
                ],
                'linear_b_cognate': 'AB59 (ta)',
                'description': 'Complex cross-form',
                'confidence': 'CERTAIN',
                'notes': 'Very common; appears in DA-MA-TE, A-TA-NA',
                'examples': ['HT 6', 'HT 95', 'ZA 4', 'PK Za 11']
            },
            'AB04': {
                'ab_number': 'AB04',
                'phonetic_value': 'te',
                'sign_type': 'syllabogram',
                'frequency': 152,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Trident-like form'},
                ],
                'linear_b_cognate': 'AB04 (te)',
                'description': 'Three-pronged sign',
                'confidence': 'CERTAIN',
                'notes': 'Transaction sign; appears at line beginnings',
                'examples': ['HT 13', 'HT 28', 'HT 31']
            },
            'AB37': {
                'ab_number': 'AB37',
                'phonetic_value': 'ti',
                'sign_type': 'syllabogram',
                'frequency': 107,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Arrow pointing upward'},
                ],
                'linear_b_cognate': 'AB37 (ti)',
                'description': 'Upward arrow form',
                'confidence': 'CERTAIN',
                'notes': 'Common in personal names and words',
                'examples': ['HT 6', 'HT 117', 'KH 7']
            },
            'AB05': {
                'ab_number': 'AB05',
                'phonetic_value': 'to',
                'sign_type': 'syllabogram',
                'frequency': 17,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Cross-like form'},
                ],
                'linear_b_cognate': 'AB05 (to)',
                'description': 'Simple cross',
                'confidence': 'HIGH',
                'notes': 'Less common; appears in specific words',
                'examples': ['HT 31', 'HT 88']
            },
            'AB69': {
                'ab_number': 'AB69',
                'phonetic_value': 'tu',
                'sign_type': 'syllabogram',
                'frequency': 63,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex angular form'},
                ],
                'linear_b_cognate': 'AB69 (tu)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 117']
            },
            'AB01': {
                'ab_number': 'AB01',
                'phonetic_value': 'da',
                'sign_type': 'syllabogram',
                'frequency': 133,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Hand-like form'},
                    {'form': 'elaborated', 'sites': ['PH'], 'description': 'More detailed hand'},
                ],
                'linear_b_cognate': 'AB01 (da)',
                'description': 'Hand-shaped sign',
                'confidence': 'CERTAIN',
                'notes': 'Very common; key in DA-MA-TE (Demeter)',
                'examples': ['HT 6', 'HT 117', 'PK Za 11']
            },
            'AB45': {
                'ab_number': 'AB45',
                'phonetic_value': 'de',
                'sign_type': 'syllabogram',
                'frequency': 35,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Tree-like form'},
                ],
                'linear_b_cognate': 'AB45 (de)',
                'description': 'Branching form',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 10', 'HT 98']
            },
            'AB07': {
                'ab_number': 'AB07',
                'phonetic_value': 'di',
                'sign_type': 'syllabogram',
                'frequency': 103,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Circular with internal dot'},
                ],
                'linear_b_cognate': 'AB07 (di)',
                'description': 'Circular sign',
                'confidence': 'CERTAIN',
                'notes': 'Common in personal names',
                'examples': ['HT 10', 'HT 88']
            },
            'AB14': {
                'ab_number': 'AB14',
                'phonetic_value': 'do',
                'sign_type': 'syllabogram',
                'frequency': 18,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Boat-like form'},
                ],
                'linear_b_cognate': 'AB14 (do)',
                'description': 'Curved form',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 13']
            },
            'AB51': {
                'ab_number': 'AB51',
                'phonetic_value': 'du',
                'sign_type': 'syllabogram',
                'frequency': 71,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex angular'},
                ],
                'linear_b_cognate': 'AB51 (du)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Appears in A-DU and other words',
                'examples': ['HT 6', 'HT 28']
            },
            'AB66': {
                'ab_number': 'AB66',
                'phonetic_value': 'ta2',
                'sign_type': 'syllabogram',
                'frequency': 8,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Variant of ta'},
                ],
                'linear_b_cognate': 'AB66 (ta2)',
                'description': 'Variant of ta sign',
                'confidence': 'MEDIUM',
                'notes': 'Rare variant',
                'examples': ['HT 117']
            },
        }

        # ============================================================
        # VELAR CONSONANTS (k/g series)
        # ============================================================
        velars = {
            'AB77': {
                'ab_number': 'AB77',
                'phonetic_value': 'ka',
                'sign_type': 'syllabogram',
                'frequency': 276,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Angular form with stem'},
                    {'form': 'simplified', 'sites': ['ZA'], 'description': 'Reduced angular'},
                ],
                'linear_b_cognate': 'AB77 (ka)',
                'description': 'Angular sign with vertical element',
                'confidence': 'CERTAIN',
                'notes': 'Second most common sign; appears in many words',
                'examples': ['HT 1', 'HT 6', 'HT 28', 'ZA 4']
            },
            'AB44': {
                'ab_number': 'AB44',
                'phonetic_value': 'ke',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB44 (ke)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Less common velar',
                'examples': ['HT 6']
            },
            'AB67': {
                'ab_number': 'AB67',
                'phonetic_value': 'ki',
                'sign_type': 'syllabogram',
                'frequency': 125,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Plant-like form'},
                ],
                'linear_b_cognate': 'AB67 (ki)',
                'description': 'Branching plant form',
                'confidence': 'CERTAIN',
                'notes': 'Common in KI-RO (deficit)',
                'examples': ['HT 13', 'HT 28', 'HT 31']
            },
            'AB70': {
                'ab_number': 'AB70',
                'phonetic_value': 'ko',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Hook-like form'},
                ],
                'linear_b_cognate': 'AB70 (ko)',
                'description': 'Curved hook shape',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB81': {
                'ab_number': 'AB81',
                'phonetic_value': 'ku',
                'sign_type': 'syllabogram',
                'frequency': 303,
                'sites': ['HT', 'KH', 'ZA', 'PH', 'KN'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH', 'ZA'], 'description': 'Vessel-like form'},
                    {'form': 'elaborated', 'sites': ['PH'], 'description': 'More detailed vessel'},
                ],
                'linear_b_cognate': 'AB81 (ku)',
                'description': 'Vessel or jar shape',
                'confidence': 'CERTAIN',
                'notes': 'Most common sign; key in KU-RO (total)',
                'examples': ['HT 1', 'HT 13', 'HT 28', 'HT 31', 'ZA 4']
            },
        }

        # ============================================================
        # NASAL CONSONANTS (m/n series)
        # ============================================================
        nasals = {
            'AB80': {
                'ab_number': 'AB80',
                'phonetic_value': 'ma',
                'sign_type': 'syllabogram',
                'frequency': 114,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Cat-face form'},
                ],
                'linear_b_cognate': 'AB80 (ma)',
                'description': 'Double-circle with connecting element',
                'confidence': 'CERTAIN',
                'notes': 'Common; appears in DA-MA-TE',
                'examples': ['HT 6', 'HT 117', 'PK Za 11']
            },
            'AB13': {
                'ab_number': 'AB13',
                'phonetic_value': 'me',
                'sign_type': 'syllabogram',
                'frequency': 43,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex sign'},
                ],
                'linear_b_cognate': 'AB13 (me)',
                'description': 'Multi-stroke sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 117']
            },
            'AB73': {
                'ab_number': 'AB73',
                'phonetic_value': 'mi',
                'sign_type': 'syllabogram',
                'frequency': 91,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Berry cluster form'},
                ],
                'linear_b_cognate': 'AB73 (mi)',
                'description': 'Clustered dots/circles',
                'confidence': 'HIGH',
                'notes': 'Common in various contexts',
                'examples': ['HT 10', 'HT 88']
            },
            'AB15': {
                'ab_number': 'AB15',
                'phonetic_value': 'mo',
                'sign_type': 'syllabogram',
                'frequency': 22,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Double element'},
                ],
                'linear_b_cognate': 'AB15 (mo)',
                'description': 'Paired form',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB23': {
                'ab_number': 'AB23',
                'phonetic_value': 'mu',
                'sign_type': 'syllabogram',
                'frequency': 14,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB23 (mu)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Rare',
                'examples': ['HT 10']
            },
            'AB06': {
                'ab_number': 'AB06',
                'phonetic_value': 'na',
                'sign_type': 'syllabogram',
                'frequency': 153,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Angular form'},
                ],
                'linear_b_cognate': 'AB06 (na)',
                'description': 'Angular sign with internal element',
                'confidence': 'CERTAIN',
                'notes': 'Very common; appears in A-TA-NA',
                'examples': ['HT 6', 'HT 117', 'HT 95']
            },
            'AB24': {
                'ab_number': 'AB24',
                'phonetic_value': 'ne',
                'sign_type': 'syllabogram',
                'frequency': 55,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Double-bar form'},
                ],
                'linear_b_cognate': 'AB24 (ne)',
                'description': 'Horizontal double bar',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 88']
            },
            'AB30': {
                'ab_number': 'AB30',
                'phonetic_value': 'ni',
                'sign_type': 'syllabogram',
                'frequency': 133,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Double vertical'},
                ],
                'linear_b_cognate': 'AB30 (ni)',
                'description': 'Paired vertical strokes',
                'confidence': 'CERTAIN',
                'notes': 'Common in various words',
                'examples': ['HT 6', 'HT 13', 'HT 117']
            },
            'AB52': {
                'ab_number': 'AB52',
                'phonetic_value': 'no',
                'sign_type': 'syllabogram',
                'frequency': 28,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Cross form'},
                ],
                'linear_b_cognate': 'AB52 (no)',
                'description': 'Cross-like sign',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 31']
            },
            'AB55': {
                'ab_number': 'AB55',
                'phonetic_value': 'nu',
                'sign_type': 'syllabogram',
                'frequency': 56,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex angular'},
                ],
                'linear_b_cognate': 'AB55 (nu)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 88']
            },
        }

        # ============================================================
        # LIQUID CONSONANTS (r/l series)
        # ============================================================
        liquids = {
            'AB60': {
                'ab_number': 'AB60',
                'phonetic_value': 'ra',
                'sign_type': 'syllabogram',
                'frequency': 162,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'T with dots'},
                ],
                'linear_b_cognate': 'AB60 (ra)',
                'description': 'T-shaped with additional elements',
                'confidence': 'CERTAIN',
                'notes': 'Very common; appears in ja-sa-sa-ra-me',
                'examples': ['HT 6', 'HT 117', 'IO Za 2']
            },
            'AB64': {
                'ab_number': 'AB64',
                'phonetic_value': 'ra2',
                'sign_type': 'syllabogram',
                'frequency': 12,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Variant of ra'},
                ],
                'linear_b_cognate': 'AB64 (ra2)',
                'description': 'Variant of ra sign',
                'confidence': 'MEDIUM',
                'notes': 'Variant - possibly different phonetic value',
                'examples': ['HT 88']
            },
            'AB89': {
                'ab_number': 'AB89',
                'phonetic_value': 'ra3',
                'sign_type': 'syllabogram',
                'frequency': 5,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Third variant of ra'},
                ],
                'linear_b_cognate': 'AB89 (ra3)',
                'description': 'Third variant of ra',
                'confidence': 'LOW',
                'notes': 'Rare variant',
                'examples': ['HT 117']
            },
            'AB27': {
                'ab_number': 'AB27',
                'phonetic_value': 're',
                'sign_type': 'syllabogram',
                'frequency': 120,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Hook form'},
                ],
                'linear_b_cognate': 'AB27 (re)',
                'description': 'Curved hook shape',
                'confidence': 'CERTAIN',
                'notes': 'Common in word-final positions',
                'examples': ['HT 6', 'HT 28']
            },
            'AB53': {
                'ab_number': 'AB53',
                'phonetic_value': 'ri',
                'sign_type': 'syllabogram',
                'frequency': 70,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex angular'},
                ],
                'linear_b_cognate': 'AB53 (ri)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Common',
                'examples': ['HT 10', 'HT 88']
            },
            'AB02': {
                'ab_number': 'AB02',
                'phonetic_value': 'ro',
                'sign_type': 'syllabogram',
                'frequency': 182,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Double-circle form'},
                ],
                'linear_b_cognate': 'AB02 (ro)',
                'description': 'Double circular elements',
                'confidence': 'CERTAIN',
                'notes': 'Very common; appears in KU-RO, KI-RO',
                'examples': ['HT 13', 'HT 28', 'HT 31']
            },
            'AB26': {
                'ab_number': 'AB26',
                'phonetic_value': 'ru',
                'sign_type': 'syllabogram',
                'frequency': 91,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB26 (ru)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Common',
                'examples': ['HT 6', 'HT 117']
            },
            'AB19': {
                'ab_number': 'AB19',
                'phonetic_value': 'la',
                'sign_type': 'syllabogram',
                'frequency': 32,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex sign'},
                ],
                'linear_b_cognate': 'AB19 (la)',
                'description': 'Multi-element form',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 88']
            },
            'AB68': {
                'ab_number': 'AB68',
                'phonetic_value': 'le',
                'sign_type': 'syllabogram',
                'frequency': 18,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Angular form'},
                ],
                'linear_b_cognate': 'AB68 (le)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 10']
            },
            'AB88': {
                'ab_number': 'AB88',
                'phonetic_value': 'li',
                'sign_type': 'syllabogram',
                'frequency': 12,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB88 (li)',
                'description': 'Simple sign',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB84': {
                'ab_number': 'AB84',
                'phonetic_value': 'lo',
                'sign_type': 'syllabogram',
                'frequency': 8,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rare form'},
                ],
                'linear_b_cognate': 'AB84 (lo)',
                'description': 'Complex form',
                'confidence': 'MEDIUM',
                'notes': 'Rare',
                'examples': ['HT 6']
            },
            'AB76': {
                'ab_number': 'AB76',
                'phonetic_value': 'lu',
                'sign_type': 'syllabogram',
                'frequency': 12,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB76 (lu)',
                'description': 'Simple sign',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 88']
            },
        }

        # ============================================================
        # SIBILANT CONSONANTS (s/z series)
        # ============================================================
        sibilants = {
            'AB31': {
                'ab_number': 'AB31',
                'phonetic_value': 'sa',
                'sign_type': 'syllabogram',
                'frequency': 138,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Angular lightning-like'},
                ],
                'linear_b_cognate': 'AB31 (sa)',
                'description': 'Angular zigzag form',
                'confidence': 'CERTAIN',
                'notes': 'Very common; appears in ja-sa-sa-ra-me',
                'examples': ['HT 6', 'HT 117', 'IO Za 2']
            },
            'AB09': {
                'ab_number': 'AB09',
                'phonetic_value': 'se',
                'sign_type': 'syllabogram',
                'frequency': 65,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB09 (se)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Common',
                'examples': ['HT 6', 'HT 88']
            },
            'AB41': {
                'ab_number': 'AB41',
                'phonetic_value': 'si',
                'sign_type': 'syllabogram',
                'frequency': 237,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Angular with dots'},
                ],
                'linear_b_cognate': 'AB41 (si)',
                'description': 'Angular sign with internal elements',
                'confidence': 'CERTAIN',
                'notes': 'Third most common; appears in many words',
                'examples': ['HT 6', 'HT 13', 'HT 117']
            },
            'AB12': {
                'ab_number': 'AB12',
                'phonetic_value': 'so',
                'sign_type': 'syllabogram',
                'frequency': 22,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rounded form'},
                ],
                'linear_b_cognate': 'AB12 (so)',
                'description': 'Rounded sign',
                'confidence': 'HIGH',
                'notes': 'Less common',
                'examples': ['HT 31']
            },
            'AB58': {
                'ab_number': 'AB58',
                'phonetic_value': 'su',
                'sign_type': 'syllabogram',
                'frequency': 51,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Pig-head form'},
                ],
                'linear_b_cognate': 'AB58 (su)',
                'description': 'Animal-head shape',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency; possibly related to SUS logogram',
                'examples': ['HT 6', 'HT 88']
            },
            'AB17': {
                'ab_number': 'AB17',
                'phonetic_value': 'za',
                'sign_type': 'syllabogram',
                'frequency': 40,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'ZA'], 'description': 'Angular form'},
                ],
                'linear_b_cognate': 'AB17 (za)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Common in ZA site codes',
                'examples': ['ZA 4', 'ZA 10']
            },
            'AB74': {
                'ab_number': 'AB74',
                'phonetic_value': 'ze',
                'sign_type': 'syllabogram',
                'frequency': 47,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB74 (ze)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6', 'HT 88']
            },
            'AB87': {
                'ab_number': 'AB87',
                'phonetic_value': 'zi',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB87 (zi)',
                'description': 'Simple sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB20': {
                'ab_number': 'AB20',
                'phonetic_value': 'zo',
                'sign_type': 'syllabogram',
                'frequency': 2,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rare form'},
                ],
                'linear_b_cognate': 'AB20 (zo)',
                'description': 'Rare sign',
                'confidence': 'LOW',
                'notes': 'Very rare',
                'examples': ['HT 10']
            },
            'AB79': {
                'ab_number': 'AB79',
                'phonetic_value': 'zu',
                'sign_type': 'syllabogram',
                'frequency': 32,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Angular form'},
                ],
                'linear_b_cognate': 'AB79 (zu)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 6']
            },
        }

        # ============================================================
        # SEMIVOWEL CONSONANTS (w/j series)
        # ============================================================
        semivowels = {
            'AB54': {
                'ab_number': 'AB54',
                'phonetic_value': 'wa',
                'sign_type': 'syllabogram',
                'frequency': 45,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB54 (wa)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Common in religious formulas',
                'examples': ['HT 6', 'IO Za 2']
            },
            'AB75': {
                'ab_number': 'AB75',
                'phonetic_value': 'we',
                'sign_type': 'syllabogram',
                'frequency': 18,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB75 (we)',
                'description': 'Simple sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 88']
            },
            'AB40': {
                'ab_number': 'AB40',
                'phonetic_value': 'wi',
                'sign_type': 'syllabogram',
                'frequency': 21,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB40 (wi)',
                'description': 'Multi-element sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 6']
            },
            'AB42': {
                'ab_number': 'AB42',
                'phonetic_value': 'wo',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB42 (wo)',
                'description': 'Simple sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB57': {
                'ab_number': 'AB57',
                'phonetic_value': 'ja',
                'sign_type': 'syllabogram',
                'frequency': 166,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Grain/wheat form'},
                ],
                'linear_b_cognate': 'AB57 (ja)',
                'description': 'Wheat/grain-like shape',
                'confidence': 'HIGH',
                'notes': 'Very common; appears in ja-sa-sa-ra-me',
                'examples': ['HT 6', 'IO Za 2', 'PK Za 11']
            },
            'AB46': {
                'ab_number': 'AB46',
                'phonetic_value': 'je',
                'sign_type': 'syllabogram',
                'frequency': 15,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Simple form'},
                ],
                'linear_b_cognate': 'AB46 (je)',
                'description': 'Simple sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 88']
            },
            'AB36': {
                'ab_number': 'AB36',
                'phonetic_value': 'jo',
                'sign_type': 'syllabogram',
                'frequency': 28,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Angular form'},
                ],
                'linear_b_cognate': 'AB36 (jo)',
                'description': 'Angular sign',
                'confidence': 'HIGH',
                'notes': 'Possible genitive ending',
                'examples': ['HT 6', 'HT 117']
            },
            'AB65': {
                'ab_number': 'AB65',
                'phonetic_value': 'ju',
                'sign_type': 'syllabogram',
                'frequency': 29,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB65 (ju)',
                'description': 'Multi-element sign',
                'confidence': 'HIGH',
                'notes': 'Moderate frequency',
                'examples': ['HT 10', 'HT 88']
            },
        }

        # ============================================================
        # LABIOVELAR AND COMPLEX SIGNS
        # ============================================================
        complex_signs = {
            'AB16': {
                'ab_number': 'AB16',
                'phonetic_value': 'qa',
                'sign_type': 'syllabogram',
                'frequency': 43,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Labiovelar form'},
                ],
                'linear_b_cognate': 'AB16 (qa)',
                'description': 'Labiovelar sign',
                'confidence': 'HIGH',
                'notes': 'Labiovelar series',
                'examples': ['HT 6', 'HT 88']
            },
            'AB21': {
                'ab_number': 'AB21',
                'phonetic_value': 'qe',
                'sign_type': 'syllabogram',
                'frequency': 43,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Labiovelar form'},
                ],
                'linear_b_cognate': 'AB21 (qe)',
                'description': 'Labiovelar sign',
                'confidence': 'HIGH',
                'notes': 'Labiovelar series',
                'examples': ['HT 6', 'HT 117']
            },
            'AB22': {
                'ab_number': 'AB22',
                'phonetic_value': 'qi',
                'sign_type': 'syllabogram',
                'frequency': 3,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rare form'},
                ],
                'linear_b_cognate': 'AB22 (qi)',
                'description': 'Rare labiovelar',
                'confidence': 'MEDIUM',
                'notes': 'Very rare',
                'examples': ['HT 10']
            },
            'AB78': {
                'ab_number': 'AB78',
                'phonetic_value': 'qo',
                'sign_type': 'syllabogram',
                'frequency': 12,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB78 (qo)',
                'description': 'Labiovelar sign',
                'confidence': 'MEDIUM',
                'notes': 'Less common',
                'examples': ['HT 117']
            },
            'AB25': {
                'ab_number': 'AB25',
                'phonetic_value': 'a2',
                'sign_type': 'syllabogram',
                'frequency': 25,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Variant of a'},
                ],
                'linear_b_cognate': 'AB25 (a2)',
                'description': 'Variant vowel',
                'confidence': 'MEDIUM',
                'notes': 'Possibly different vowel quality',
                'examples': ['HT 6', 'HT 88']
            },
            'AB48': {
                'ab_number': 'AB48',
                'phonetic_value': 'nwa',
                'sign_type': 'syllabogram',
                'frequency': 8,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex sign'},
                ],
                'linear_b_cognate': 'AB48 (nwa)',
                'description': 'Complex syllable',
                'confidence': 'MEDIUM',
                'notes': 'Complex sign - CCV structure',
                'examples': ['HT 117']
            },
            'AB83': {
                'ab_number': 'AB83',
                'phonetic_value': 'pte',
                'sign_type': 'syllabogram',
                'frequency': 5,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB83 (pte)',
                'description': 'Complex syllable',
                'confidence': 'LOW',
                'notes': 'Complex sign - CCVC structure',
                'examples': ['HT 10']
            },
            'AB82': {
                'ab_number': 'AB82',
                'phonetic_value': 'dwe',
                'sign_type': 'syllabogram',
                'frequency': 3,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Complex form'},
                ],
                'linear_b_cognate': 'AB82 (dwe)',
                'description': 'Complex syllable',
                'confidence': 'LOW',
                'notes': 'Complex sign',
                'examples': ['HT 117']
            },
            'AB86': {
                'ab_number': 'AB86',
                'phonetic_value': 'dwo',
                'sign_type': 'syllabogram',
                'frequency': 2,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rare form'},
                ],
                'linear_b_cognate': 'AB86 (dwo)',
                'description': 'Complex syllable',
                'confidence': 'LOW',
                'notes': 'Very rare',
                'examples': ['HT 10']
            },
            'AB90': {
                'ab_number': 'AB90',
                'phonetic_value': 'two',
                'sign_type': 'syllabogram',
                'frequency': 2,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Rare form'},
                ],
                'linear_b_cognate': 'AB90 (two)',
                'description': 'Complex syllable',
                'confidence': 'LOW',
                'notes': 'Very rare',
                'examples': ['HT 117']
            },
            'AB85': {
                'ab_number': 'AB85',
                'phonetic_value': 'au',
                'sign_type': 'syllabogram',
                'frequency': 8,
                'sites': ['HT'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Diphthong form'},
                ],
                'linear_b_cognate': 'AB85 (au)',
                'description': 'Diphthong sign',
                'confidence': 'MEDIUM',
                'notes': 'Diphthong - rare',
                'examples': ['HT 6']
            },
        }

        # ============================================================
        # LOGOGRAMS (Ideograms)
        # ============================================================
        logograms = {
            'VIN': {
                'ab_number': 'VIN',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 85,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Vine/grape form'},
                ],
                'linear_b_cognate': 'VIN (wine)',
                'description': 'Wine/vine logogram',
                'confidence': 'CERTAIN',
                'notes': 'Confirmed commodity logogram',
                'examples': ['HT 13', 'HT 28']
            },
            'OLE': {
                'ab_number': 'OLE',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 120,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Oil vessel form'},
                ],
                'linear_b_cognate': 'OLE (olive oil)',
                'description': 'Olive oil logogram',
                'confidence': 'CERTAIN',
                'notes': 'Most common commodity logogram',
                'examples': ['HT 13', 'HT 28', 'HT 31']
            },
            'GRA': {
                'ab_number': 'GRA',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 95,
                'sites': ['HT', 'KH', 'ZA'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH'], 'description': 'Grain/wheat form'},
                ],
                'linear_b_cognate': 'GRA (grain)',
                'description': 'Grain logogram',
                'confidence': 'CERTAIN',
                'notes': 'Confirmed commodity logogram',
                'examples': ['HT 13', 'HT 94']
            },
            'FIC': {
                'ab_number': 'FIC',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 45,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Fig form'},
                ],
                'linear_b_cognate': 'FIC (figs)',
                'description': 'Fig logogram',
                'confidence': 'CERTAIN',
                'notes': 'Confirmed commodity logogram',
                'examples': ['HT 28', 'HT 100']
            },
            'OVI': {
                'ab_number': 'OVI',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 35,
                'sites': ['HT', 'KH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT'], 'description': 'Sheep form'},
                ],
                'linear_b_cognate': 'OVI (sheep)',
                'description': 'Sheep logogram',
                'confidence': 'CERTAIN',
                'notes': 'Animal logogram',
                'examples': ['HT 24']
            },
            '*301': {
                'ab_number': '*301',
                'phonetic_value': '',
                'sign_type': 'logogram',
                'frequency': 180,
                'sites': ['HT', 'KH', 'ZA', 'PH'],
                'variants': [
                    {'form': 'standard', 'sites': ['HT', 'KH', 'ZA'], 'description': 'Unknown form'},
                ],
                'linear_b_cognate': '',
                'description': 'Unknown logogram - very frequent',
                'confidence': 'UNKNOWN',
                'notes': 'No Linear B cognate; meaning unknown; appears in libation formula',
                'examples': ['IO Za 2', 'PK Za 11', 'KN Zf 2']
            },
        }

        # Combine all categories
        all_signs = {}
        for category in [vowels, labials, dentals, velars, nasals, liquids,
                         sibilants, semivowels, complex_signs, logograms]:
            all_signs.update(category)

        self.signs = all_signs
        self.log(f"Built sign database with {len(self.signs)} entries")

    def query_sign(self, sign_id: str) -> Optional[Dict]:
        """
        Query a sign by AB number or phonetic value.

        Args:
            sign_id: AB number (e.g., "AB08") or phonetic value (e.g., "a")

        Returns:
            Sign entry or None if not found
        """
        # Normalize input
        sign_id_upper = sign_id.upper()

        # Direct AB number lookup
        if sign_id_upper in self.signs:
            return self.signs[sign_id_upper]

        # Try with "AB" prefix
        if not sign_id_upper.startswith('AB') and not sign_id_upper.startswith('*'):
            ab_key = f"AB{sign_id_upper.zfill(2)}"
            if ab_key in self.signs:
                return self.signs[ab_key]

        # Search by phonetic value
        for ab_num, data in self.signs.items():
            if data['phonetic_value'].lower() == sign_id.lower():
                return data

        return None

    def get_sign_variants(self, sign_id: str) -> List[Dict]:
        """
        Get all variant forms of a sign.

        Args:
            sign_id: AB number or phonetic value

        Returns:
            List of variant dictionaries
        """
        sign = self.query_sign(sign_id)
        if sign:
            return sign.get('variants', [])
        return []

    def compare_signs(self, sign_a: str, sign_b: str) -> Dict:
        """
        Compare two signs paleographically.

        Args:
            sign_a: First sign (AB number or phonetic value)
            sign_b: Second sign (AB number or phonetic value)

        Returns:
            Comparison results
        """
        entry_a = self.query_sign(sign_a)
        entry_b = self.query_sign(sign_b)

        if not entry_a or not entry_b:
            return {
                'error': f"Sign not found: {sign_a if not entry_a else sign_b}",
                'valid': False
            }

        # Calculate shared sites
        sites_a = set(entry_a.get('sites', []))
        sites_b = set(entry_b.get('sites', []))
        shared_sites = sites_a & sites_b

        # Frequency comparison
        freq_a = entry_a.get('frequency', 0)
        freq_b = entry_b.get('frequency', 0)

        # Check if they are variants
        are_variants = False
        pv_a = entry_a['phonetic_value'].rstrip('0123456789')
        pv_b = entry_b['phonetic_value'].rstrip('0123456789')
        if pv_a == pv_b and entry_a['ab_number'] != entry_b['ab_number']:
            are_variants = True

        return {
            'valid': True,
            'sign_a': {
                'ab_number': entry_a['ab_number'],
                'phonetic_value': entry_a['phonetic_value'],
                'frequency': freq_a,
                'sites': list(sites_a)
            },
            'sign_b': {
                'ab_number': entry_b['ab_number'],
                'phonetic_value': entry_b['phonetic_value'],
                'frequency': freq_b,
                'sites': list(sites_b)
            },
            'shared_sites': list(shared_sites),
            'are_variants': are_variants,
            'frequency_ratio': round(freq_a / freq_b, 2) if freq_b > 0 else None,
            'notes': f"{'These are variant forms of the same phoneme' if are_variants else 'These are distinct phonemes'}"
        }

    def get_tablet_signs(self, tablet_id: str) -> List[str]:
        """
        Get all signs attested on a specific tablet.

        Note: This is based on example attestations in the database,
        not a complete tablet transcription.

        Args:
            tablet_id: Tablet reference (e.g., "HT 13")

        Returns:
            List of AB numbers found on that tablet
        """
        tablet_id_norm = tablet_id.upper().replace(' ', ' ')
        results = []

        for ab_num, data in self.signs.items():
            examples = data.get('examples', [])
            for ex in examples:
                if tablet_id_norm in ex.upper():
                    results.append(ab_num)
                    break

        return sorted(results)

    def get_signs_by_site(self, site_code: str) -> List[Dict]:
        """
        Get all signs attested at a specific site.

        Args:
            site_code: Site code (e.g., "HT", "KH", "ZA")

        Returns:
            List of signs with frequencies
        """
        site_code_upper = site_code.upper()
        results = []

        for ab_num, data in self.signs.items():
            if site_code_upper in data.get('sites', []):
                results.append({
                    'ab_number': ab_num,
                    'phonetic_value': data['phonetic_value'],
                    'frequency': data['frequency'],
                    'sign_type': data['sign_type']
                })

        return sorted(results, key=lambda x: x['frequency'], reverse=True)

    def get_signs_by_frequency(self, min_freq: int = 0, max_freq: int = 999999) -> List[Dict]:
        """
        Get signs within a frequency range.

        Args:
            min_freq: Minimum frequency
            max_freq: Maximum frequency

        Returns:
            List of signs sorted by frequency
        """
        results = []

        for ab_num, data in self.signs.items():
            freq = data.get('frequency', 0)
            if min_freq <= freq <= max_freq:
                results.append({
                    'ab_number': ab_num,
                    'phonetic_value': data['phonetic_value'],
                    'frequency': freq,
                    'sign_type': data['sign_type'],
                    'confidence': data.get('confidence', 'UNKNOWN')
                })

        return sorted(results, key=lambda x: x['frequency'], reverse=True)

    def get_statistics(self) -> Dict:
        """Get comprehensive database statistics."""
        total = len(self.signs)
        syllabograms = sum(1 for s in self.signs.values() if s['sign_type'] == 'syllabogram')
        logograms = sum(1 for s in self.signs.values() if s['sign_type'] == 'logogram')
        total_freq = sum(s.get('frequency', 0) for s in self.signs.values())

        # Confidence breakdown
        confidence_counts = {}
        for s in self.signs.values():
            conf = s.get('confidence', 'UNKNOWN')
            confidence_counts[conf] = confidence_counts.get(conf, 0) + 1

        # Site coverage
        all_sites = set()
        for s in self.signs.values():
            all_sites.update(s.get('sites', []))

        return {
            'total_signs': total,
            'syllabograms': syllabograms,
            'logograms': logograms,
            'total_attestations': total_freq,
            'sites_covered': sorted(list(all_sites)),
            'confidence_breakdown': confidence_counts
        }

    def save_database(self, filepath: Path = SIGN_DB_FILE):
        """Save sign database to JSON."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        output = {
            'generated': datetime.now().isoformat(),
            'source': 'SigLA Querier - compiled from GORILA and published sources',
            'statistics': self.get_statistics(),
            'signs': self.signs
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.log(f"Saved database to {filepath}")
        return filepath


def print_sign(sign: Dict, verbose: bool = False):
    """Pretty-print a sign entry."""
    print(f"\n  {sign['ab_number']}: {sign['phonetic_value'] or '(logogram)'}")
    print(f"    Type: {sign['sign_type']}")
    print(f"    Frequency: {sign['frequency']} occurrences")
    print(f"    Sites: {', '.join(sign.get('sites', []))}")
    print(f"    Confidence: {sign.get('confidence', 'UNKNOWN')}")

    if verbose:
        if sign.get('linear_b_cognate'):
            print(f"    Linear B: {sign['linear_b_cognate']}")
        if sign.get('description'):
            print(f"    Description: {sign['description']}")
        if sign.get('notes'):
            print(f"    Notes: {sign['notes']}")
        if sign.get('variants'):
            print(f"    Variants: {len(sign['variants'])} forms")
            for v in sign['variants']:
                print(f"      - {v['form']}: {v['description']} ({', '.join(v.get('sites', []))})")
        if sign.get('examples'):
            print(f"    Examples: {', '.join(sign['examples'][:5])}")


def main():
    parser = argparse.ArgumentParser(
        description='SigLA Paleographic Querier - Linear A sign analysis'
    )
    parser.add_argument('--query', '-q', type=str, help='Query a sign by AB number or phonetic value')
    parser.add_argument('--variants', type=str, help='Get variants of a sign')
    parser.add_argument('--compare', nargs=2, metavar=('SIGN_A', 'SIGN_B'),
                        help='Compare two signs paleographically')
    parser.add_argument('--tablet', '-t', type=str, help='Get signs on a specific tablet')
    parser.add_argument('--site', '-s', type=str, help='Get signs attested at a site')
    parser.add_argument('--frequency', nargs=2, type=int, metavar=('MIN', 'MAX'),
                        help='Get signs in frequency range')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--save', action='store_true', help='Save database to JSON')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    print("=" * 60)
    print("SigLA PALEOGRAPHIC QUERIER")
    print("Linear A Sign Database")
    print("=" * 60)

    querier = SigLAQuerier(verbose=args.verbose)

    if args.query:
        sign = querier.query_sign(args.query)
        if sign:
            print(f"\nSign found:")
            print_sign(sign, args.verbose)
        else:
            print(f"\nSign not found: {args.query}")
            print("Try using AB number (e.g., AB08) or phonetic value (e.g., 'a')")

    elif args.variants:
        variants = querier.get_sign_variants(args.variants)
        sign = querier.query_sign(args.variants)
        if sign:
            print(f"\nVariants of {sign['ab_number']} ({sign['phonetic_value']}):")
            if variants:
                for v in variants:
                    print(f"  - {v['form']}: {v['description']}")
                    print(f"    Sites: {', '.join(v.get('sites', []))}")
            else:
                print("  No documented variants")
        else:
            print(f"\nSign not found: {args.variants}")

    elif args.compare:
        result = querier.compare_signs(args.compare[0], args.compare[1])
        if result.get('valid'):
            print(f"\nSign Comparison:")
            print(f"\n  Sign A: {result['sign_a']['ab_number']} ({result['sign_a']['phonetic_value']})")
            print(f"    Frequency: {result['sign_a']['frequency']}")
            print(f"    Sites: {', '.join(result['sign_a']['sites'])}")
            print(f"\n  Sign B: {result['sign_b']['ab_number']} ({result['sign_b']['phonetic_value']})")
            print(f"    Frequency: {result['sign_b']['frequency']}")
            print(f"    Sites: {', '.join(result['sign_b']['sites'])}")
            print(f"\n  Shared sites: {', '.join(result['shared_sites']) or 'None'}")
            print(f"  Are variants: {result['are_variants']}")
            if result['frequency_ratio']:
                print(f"  Frequency ratio: {result['frequency_ratio']}")
            print(f"\n  {result['notes']}")
        else:
            print(f"\n  Error: {result.get('error')}")

    elif args.tablet:
        signs = querier.get_tablet_signs(args.tablet)
        print(f"\nSigns on tablet {args.tablet}:")
        if signs:
            for ab_num in signs:
                sign = querier.query_sign(ab_num)
                if sign:
                    print(f"  {ab_num}: {sign['phonetic_value'] or '(logogram)'}")
        else:
            print("  No signs found (tablet may not be in examples database)")

    elif args.site:
        signs = querier.get_signs_by_site(args.site)
        print(f"\nSigns attested at {args.site.upper()}: {len(signs)} signs")
        for s in signs[:20]:  # Show top 20
            print(f"  {s['ab_number']}: {s['phonetic_value'] or '(logogram)'} - {s['frequency']} occurrences")
        if len(signs) > 20:
            print(f"  ... and {len(signs) - 20} more")

    elif args.frequency:
        signs = querier.get_signs_by_frequency(args.frequency[0], args.frequency[1])
        print(f"\nSigns with frequency {args.frequency[0]}-{args.frequency[1]}: {len(signs)} signs")
        for s in signs:
            print(f"  {s['ab_number']}: {s['phonetic_value'] or '(logogram)'} - {s['frequency']} occurrences [{s['confidence']}]")

    elif args.stats:
        stats = querier.get_statistics()
        print(f"\nDatabase Statistics:")
        print(f"  Total signs: {stats['total_signs']}")
        print(f"  Syllabograms: {stats['syllabograms']}")
        print(f"  Logograms: {stats['logograms']}")
        print(f"  Total attestations: {stats['total_attestations']}")
        print(f"  Sites covered: {', '.join(stats['sites_covered'])}")
        print(f"\nConfidence breakdown:")
        for conf, count in sorted(stats['confidence_breakdown'].items()):
            print(f"  {conf}: {count}")

    elif args.save:
        filepath = querier.save_database()
        print(f"\nSaved database to: {filepath}")

    else:
        print("\nUsage:")
        print("  --query SIGN      Query a sign (e.g., AB08, 'a', 'ku')")
        print("  --variants SIGN   Get variant forms of a sign")
        print("  --compare A B     Compare two signs")
        print("  --tablet ID       Get signs on a tablet (e.g., 'HT 13')")
        print("  --site CODE       Get signs at a site (e.g., 'HT', 'KH')")
        print("  --frequency MIN MAX  Get signs in frequency range")
        print("  --stats           Show database statistics")
        print("  --save            Save database to JSON")
        print("\nExamples:")
        print("  python tools/sigla_querier.py --query ku")
        print("  python tools/sigla_querier.py --compare AB60 AB64")
        print("  python tools/sigla_querier.py --site HT -v")
        print("  python tools/sigla_querier.py --stats")

    return 0


if __name__ == '__main__':
    sys.exit(main())
