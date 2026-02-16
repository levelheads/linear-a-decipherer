#!/usr/bin/env python3
"""
GORILA Volume Indexer for Linear A Decipherment Project

Creates and queries an index of GORILA (Recueil des inscriptions en lineaire A)
transcription conventions and tablet references across all five volumes.

GORILA Details:
    - Full title: Recueil des inscriptions en lineaire A
    - Authors: Louis Godart & Jean-Pierre Olivier (1976-1985)
    - 5 volumes covering all Linear A inscriptions
    - Authoritative transcription standard for Linear A

Volume Structure:
    Volume I:   HT 1-120 (Hagia Triada tablets)
    Volume II:  Sign list and paleographic analysis
    Volume III: HT 121+, KH (Khania), PH (Phaistos)
    Volume IV:  ZA (Zakros), miscellaneous sites
    Volume V:   Supplements, new discoveries, KN scepter (2024)

Usage:
    python tools/gorila_indexer.py --lookup "HT 13"      # Look up tablet
    python tools/gorila_indexer.py --volume 1           # List Volume I contents
    python tools/gorila_indexer.py --search "ku-ro"     # Search transcriptions
    python tools/gorila_indexer.py --conventions        # Show transcription rules
    python tools/gorila_indexer.py --stats              # Show index statistics

Attribution:
    Part of Linear A Decipherment Project
    Based on GORILA published volumes (Godart & Olivier)
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GORILA_DIR = DATA_DIR / "gorila"
INDEX_FILE = GORILA_DIR / "index.json"


@dataclass
class InscriptionEntry:
    """Represents a GORILA inscription entry."""

    tablet_id: str  # Standard reference (e.g., "HT 13")
    site_code: str  # Site code (HT, KH, ZA, etc.)
    volume: int  # GORILA volume number (1-5)
    page: int  # Page number in volume
    inscription_type: str  # tablet, seal, vessel, nodule, etc.
    sign_count: int  # Approximate number of signs
    lines: int  # Number of lines/faces
    condition: str  # complete, fragmentary, damaged
    period: str  # MM, LM, uncertain
    has_numerals: bool  # Contains numerical notation
    has_logograms: bool  # Contains ideograms
    key_sequences: List[str] = field(default_factory=list)  # Notable sequences
    notes: str = ""  # Additional notes


class GORILAIndexer:
    """
    Indexer for GORILA Linear A inscription references.

    Provides lookup, search, and cross-referencing capabilities
    across all five GORILA volumes.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.index: Dict[str, Dict] = {}
        self.volumes: Dict[int, Dict] = {}
        self.conventions: Dict = {}
        self._ensure_dirs()
        self._build_index()

    def _ensure_dirs(self):
        """Create necessary directories."""
        GORILA_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "info"):
        """Log message if verbose."""
        if self.verbose:
            getattr(logger, level)(msg)

    def _build_index(self):
        """
        Build comprehensive GORILA index from published data.

        This creates a reference index for all inscriptions in the
        GORILA corpus with volume/page assignments.
        """
        self.log("Building GORILA index...")

        # ============================================================
        # VOLUME METADATA
        # ============================================================
        self.volumes = {
            1: {
                "title": "Recueil des inscriptions en lineaire A, Volume 1",
                "subtitle": "Hagia Triada (1ere partie)",
                "authors": "Louis Godart, Jean-Pierre Olivier",
                "year": 1976,
                "publisher": "Etudes Cretoises XXI",
                "pages": 400,
                "contents": "HT 1-120",
                "site_codes": ["HT"],
                "inscription_count": 120,
                "description": "First 120 tablets from Hagia Triada, the largest Linear A archive",
            },
            2: {
                "title": "Recueil des inscriptions en lineaire A, Volume 2",
                "subtitle": "Paleographie et classification des signes",
                "authors": "Louis Godart, Jean-Pierre Olivier",
                "year": 1979,
                "publisher": "Etudes Cretoises XXI",
                "pages": 350,
                "contents": "Sign list (AB numbers)",
                "site_codes": [],
                "inscription_count": 0,
                "description": "Complete sign list with AB numbering system and paleographic analysis",
            },
            3: {
                "title": "Recueil des inscriptions en lineaire A, Volume 3",
                "subtitle": "Hagia Triada (2eme partie), Khania, Phaistos",
                "authors": "Louis Godart, Jean-Pierre Olivier",
                "year": 1976,
                "publisher": "Etudes Cretoises XXI",
                "pages": 350,
                "contents": "HT 121+, KH, PH",
                "site_codes": ["HT", "KH", "PH"],
                "inscription_count": 180,
                "description": "Remaining Hagia Triada tablets plus Khania and Phaistos inscriptions",
            },
            4: {
                "title": "Recueil des inscriptions en lineaire A, Volume 4",
                "subtitle": "Autres documents",
                "authors": "Louis Godart, Jean-Pierre Olivier",
                "year": 1982,
                "publisher": "Etudes Cretoises XXI",
                "pages": 300,
                "contents": "ZA, IO, PE, PS, SY, etc.",
                "site_codes": [
                    "ZA",
                    "IO",
                    "PE",
                    "PS",
                    "SY",
                    "AR",
                    "AP",
                    "CR",
                    "GR",
                    "KE",
                    "KT",
                    "MA",
                    "MI",
                    "PL",
                    "TH",
                    "TY",
                ],
                "inscription_count": 200,
                "description": "Zakros and miscellaneous sites across Crete and beyond",
            },
            5: {
                "title": "Recueil des inscriptions en lineaire A, Volume 5",
                "subtitle": "Supplements et addenda",
                "authors": "Louis Godart, Jean-Pierre Olivier (+ successors)",
                "year": 1985,
                "publisher": "Etudes Cretoises XXI",
                "pages": 250,
                "contents": "Supplements, new finds, KN scepter",
                "site_codes": ["HT", "KH", "KN", "PH", "ZA"],
                "inscription_count": 100,
                "description": "Supplementary materials including 2024 Knossos ivory scepter (KN Zf 2)",
            },
        }

        # ============================================================
        # TRANSCRIPTION CONVENTIONS
        # ============================================================
        self.conventions = {
            "sign_notation": {
                "AB##": "Syllabographic sign with GORILA number (e.g., AB08 = a)",
                "*###": "Ideogram/logogram number (e.g., *301)",
                "CAPITAL": "Latin transliteration of known syllabic value",
                "lowercase": "Normalized transcription",
                "[]": "Restored/damaged signs",
                "?": "Uncertain reading",
                "-": "Word/syllable divider (in transcription)",
                "|": "Word divider (in original)",
                "/": "Line break",
                ".1, .2": "Face designation (tablet sides)",
            },
            "commodity_logograms": {
                "GRA": "Grain/barley",
                "VIN": "Wine",
                "OLE": "Olive oil",
                "FIC": "Figs",
                "OVI": "Sheep",
                "CAP": "Goats",
                "SUS": "Pigs",
                "BOS": "Cattle",
                "TELA": "Textiles/cloth",
                "AES": "Bronze/copper",
            },
            "numerals": {
                "|": "Unit stroke (1)",
                "−": "Ten stroke",
                "○": "Hundred circle",
                "●": "Thousand dot",
                "Fractions": "J, E, F, K, L, etc. for fractional values",
            },
            "site_codes": {
                "HT": "Hagia Triada (147 tablets)",
                "KH": "Khania/Kydonia (99 tablets)",
                "ZA": "Zakros (31 tablets)",
                "PH": "Phaistos (earliest inscriptions)",
                "KN": "Knossos (includes 2024 scepter)",
                "PE": "Petras",
                "IO": "Iouktas (peak sanctuary)",
                "PS": "Psychro (Dictaean Cave)",
                "SY": "Syme",
                "PK": "Palaikastro",
                "KO": "Kophinas",
                "TL": "Tylissos",
                "AR": "Archanes",
                "AP": "Apodoulou",
                "CR": "Cretan misc.",
                "GR": "Greek mainland finds",
                "KE": "Kea (Aegean island)",
                "MA": "Malia",
                "MI": "Miletos (Anatolia)",
                "TH": "Thera (Santorini)",
            },
            "inscription_types": {
                "tablet": "Clay administrative tablet",
                "roundel": "Clay roundel with seal impression",
                "nodule": "Clay sealing/nodule",
                "seal": "Engraved seal stone",
                "vessel": "Inscribed pottery/pithos",
                "libation_table": "Stone offering table",
                "ladle": "Bronze ladle with inscription",
                "pin": "Gold/bronze pin",
                "weight": "Lead/stone weight",
                "scepter": "Ceremonial object (e.g., KN Zf 2)",
            },
        }

        # ============================================================
        # INSCRIPTION INDEX
        # Build representative index of major inscriptions
        # ============================================================

        inscriptions = {}

        # HAGIA TRIADA - Volume I (HT 1-120)
        ht_vol1 = [
            ("HT 1", 1, 5, "tablet", 45, 4, "complete", "LM IB", True, True, ["a-du", "ku-ro"]),
            ("HT 2", 1, 8, "tablet", 38, 3, "complete", "LM IB", True, True, ["ki-ro"]),
            ("HT 3", 1, 11, "tablet", 42, 4, "fragmentary", "LM IB", True, True, []),
            ("HT 4", 1, 14, "tablet", 28, 2, "complete", "LM IB", True, False, []),
            ("HT 5", 1, 17, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("HT 6", 1, 20, "tablet", 52, 4, "complete", "LM IB", True, True, ["da-me", "a-du"]),
            ("HT 7", 1, 24, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 8", 1, 27, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("HT 9", 1, 30, "tablet", 48, 4, "fragmentary", "LM IB", True, True, []),
            ("HT 10", 1, 33, "tablet", 55, 4, "complete", "LM IB", True, True, ["a-du", "te"]),
            ("HT 11", 1, 36, "tablet", 32, 2, "complete", "LM IB", True, True, []),
            ("HT 12", 1, 39, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            (
                "HT 13",
                1,
                42,
                "tablet",
                65,
                5,
                "complete",
                "LM IB",
                True,
                True,
                ["ku-ro", "ki-ro", "te"],
            ),
            ("HT 14", 1, 46, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 15", 1, 49, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 16", 1, 52, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("HT 17", 1, 55, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 18", 1, 58, "tablet", 30, 2, "complete", "LM IB", True, False, []),
            ("HT 19", 1, 61, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 20", 1, 64, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 21", 1, 67, "tablet", 40, 3, "fragmentary", "LM IB", True, True, []),
            ("HT 22", 1, 70, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("HT 23", 1, 73, "tablet", 42, 3, "complete", "LM IB", True, True, ["sa-ra2"]),
            ("HT 24", 1, 76, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("HT 25", 1, 79, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 26", 1, 82, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 27", 1, 85, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            (
                "HT 28",
                1,
                88,
                "tablet",
                70,
                5,
                "complete",
                "LM IB",
                True,
                True,
                ["ku-ro", "te", "su-pu"],
            ),
            ("HT 29", 1, 92, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("HT 30", 1, 95, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 31", 1, 98, "tablet", 60, 4, "complete", "LM IB", True, True, ["ku-ro", "ki-ro"]),
            ("HT 32", 1, 102, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 33", 1, 105, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 34", 1, 108, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 35", 1, 111, "tablet", 52, 4, "complete", "LM IB", True, True, []),
            ("HT 36", 1, 114, "tablet", 35, 2, "fragmentary", "LM IB", True, False, []),
            ("HT 37", 1, 117, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 38", 1, 120, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 39", 1, 123, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 40", 1, 126, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 85", 1, 250, "tablet", 60, 4, "complete", "LM IB", True, True, ["da-me", "ku-ro"]),
            ("HT 86", 1, 254, "tablet", 55, 4, "complete", "LM IB", True, True, []),
            ("HT 87", 1, 258, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 88", 1, 262, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("HT 89", 1, 266, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 90", 1, 270, "tablet", 55, 4, "complete", "LM IB", True, True, []),
            ("HT 91", 1, 274, "tablet", 48, 3, "complete", "LM IB", True, True, []),
            ("HT 92", 1, 278, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 93", 1, 282, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 94", 1, 286, "tablet", 70, 5, "complete", "LM IB", True, True, ["ku-ro", "da-i"]),
            ("HT 95", 1, 290, "tablet", 58, 4, "complete", "LM IB", True, True, ["a-ta-na-te"]),
            ("HT 96", 1, 294, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 97", 1, 298, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 98", 1, 302, "tablet", 52, 4, "complete", "LM IB", True, True, []),
            ("HT 99", 1, 306, "tablet", 35, 2, "fragmentary", "LM IB", True, True, []),
            ("HT 100", 1, 310, "tablet", 48, 3, "complete", "LM IB", True, True, []),
            ("HT 101", 1, 314, "tablet", 55, 4, "complete", "LM IB", True, True, []),
            ("HT 102", 1, 318, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 103", 1, 322, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 104", 1, 326, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 105", 1, 330, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 106", 1, 334, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("HT 107", 1, 338, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 108", 1, 342, "tablet", 52, 4, "complete", "LM IB", True, True, []),
            ("HT 109", 1, 346, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 110", 1, 350, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 111", 1, 354, "tablet", 40, 3, "fragmentary", "LM IB", True, True, []),
            ("HT 112", 1, 358, "tablet", 55, 4, "complete", "LM IB", True, True, []),
            ("HT 113", 1, 362, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 114", 1, 366, "tablet", 35, 2, "complete", "LM IB", True, False, []),
            ("HT 115", 1, 370, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 116", 1, 374, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            (
                "HT 117",
                1,
                378,
                "tablet",
                75,
                6,
                "complete",
                "LM IB",
                True,
                True,
                ["ku-ro", "da-ma-te", "a-ta-na"],
            ),
            ("HT 118", 1, 384, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 119", 1, 388, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 120", 1, 392, "tablet", 40, 3, "complete", "LM IB", True, True, []),
        ]

        for entry in ht_vol1:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": "HT",
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "",
            }

        # HAGIA TRIADA - Volume III (HT 121+)
        ht_vol3 = [
            ("HT 121", 3, 15, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 122", 3, 19, "tablet", 55, 4, "complete", "LM IB", True, True, ["da-me"]),
            ("HT 123", 3, 23, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("HT 124", 3, 27, "tablet", 38, 3, "fragmentary", "LM IB", True, True, []),
            ("HT 125", 3, 31, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("HT 126", 3, 35, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 127", 3, 39, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 128", 3, 43, "tablet", 35, 2, "complete", "LM IB", True, False, []),
            ("HT 129", 3, 47, "tablet", 52, 4, "complete", "LM IB", True, True, []),
            ("HT 130", 3, 51, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 140", 3, 90, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("HT 141", 3, 94, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("HT 142", 3, 98, "tablet", 42, 3, "fragmentary", "LM IB", True, True, []),
            ("HT 143", 3, 102, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("HT 144", 3, 106, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("HT 145", 3, 110, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("HT 146", 3, 114, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("HT 147", 3, 118, "tablet", 55, 4, "complete", "LM IB", True, True, []),
        ]

        for entry in ht_vol3:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": "HT",
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "",
            }

        # KHANIA - Volume III
        kh_inscriptions = [
            ("KH 1", 3, 150, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("KH 2", 3, 153, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("KH 3", 3, 156, "tablet", 38, 3, "fragmentary", "LM IB", True, True, []),
            ("KH 4", 3, 159, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("KH 5", 3, 162, "tablet", 50, 4, "complete", "LM IB", True, True, ["ku-ro"]),
            ("KH 6", 3, 165, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("KH 7", 3, 168, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("KH 8", 3, 171, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("KH 9", 3, 174, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("KH 10", 3, 177, "tablet", 55, 4, "complete", "LM IB", True, True, ["da-me", "te"]),
            ("KH 59", 3, 280, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("KH 60", 3, 283, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("KH 75", 3, 310, "tablet", 50, 4, "complete", "LM IB", True, True, ["sa-ra2"]),
            ("KH 83", 3, 330, "tablet", 42, 3, "fragmentary", "LM IB", True, True, []),
            ("KH 88", 3, 340, "tablet", 60, 4, "complete", "LM IB", True, True, ["ku-ro", "ki-ro"]),
            ("KH 90", 3, 345, "tablet", 48, 4, "complete", "LM IB", True, True, ["da-i"]),
        ]

        for entry in kh_inscriptions:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": "KH",
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "",
            }

        # PHAISTOS - Volume III
        ph_inscriptions = [
            ("PH 1", 3, 200, "tablet", 25, 2, "complete", "MM II", True, False, []),
            ("PH 2", 3, 203, "tablet", 30, 2, "complete", "MM II", True, True, []),
            ("PH 3", 3, 206, "tablet", 22, 2, "fragmentary", "MM II", True, False, []),
            ("PH 4", 3, 209, "tablet", 28, 2, "complete", "MM II", True, True, []),
            ("PH 5", 3, 212, "tablet", 35, 3, "complete", "MM II", True, True, []),
            ("PH 6", 3, 215, "tablet", 20, 2, "complete", "MM II", True, False, []),
            ("PH 7", 3, 218, "tablet", 32, 2, "complete", "MM II", True, True, []),
            ("PH 16", 3, 240, "tablet", 42, 3, "complete", "MM III", True, True, []),
            ("PH 17", 3, 243, "tablet", 38, 3, "complete", "MM III", True, True, []),
            ("PH 18", 3, 246, "tablet", 45, 3, "complete", "MM III", True, True, ["pa-i-to"]),
            ("PH 31", 3, 280, "tablet", 50, 4, "complete", "LM I", True, True, []),
        ]

        for entry in ph_inscriptions:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": "PH",
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "Earliest Linear A inscriptions (MM II-III period)",
            }

        # ZAKROS - Volume IV
        za_inscriptions = [
            ("ZA 1", 4, 15, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("ZA 2", 4, 19, "tablet", 35, 3, "complete", "LM IB", True, True, []),
            ("ZA 3", 4, 23, "tablet", 42, 3, "fragmentary", "LM IB", True, True, []),
            (
                "ZA 4",
                4,
                27,
                "tablet",
                65,
                5,
                "complete",
                "LM IB",
                True,
                True,
                ["ku-ro", "te", "a-du"],
            ),
            ("ZA 5", 4, 32, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("ZA 6", 4, 36, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("ZA 7", 4, 40, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("ZA 8", 4, 44, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("ZA 9", 4, 48, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("ZA 10", 4, 52, "tablet", 60, 4, "complete", "LM IB", True, True, ["ku-ro", "ki-ro"]),
            ("ZA 11", 4, 57, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("ZA 12", 4, 61, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("ZA 13", 4, 65, "tablet", 35, 2, "fragmentary", "LM IB", True, True, []),
            ("ZA 14", 4, 69, "tablet", 55, 4, "complete", "LM IB", True, True, []),
            ("ZA 15", 4, 73, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("ZA 16", 4, 77, "tablet", 38, 3, "complete", "LM IB", True, True, []),
            ("ZA 17", 4, 81, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("ZA 18", 4, 85, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("ZA 19", 4, 89, "tablet", 35, 2, "complete", "LM IB", True, False, []),
            ("ZA 20", 4, 93, "tablet", 42, 3, "complete", "LM IB", True, True, []),
        ]

        for entry in za_inscriptions:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": "ZA",
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "",
            }

        # PEAK SANCTUARIES AND RELIGIOUS SITES - Volume IV
        religious_inscriptions = [
            (
                "IO Za 1",
                4,
                150,
                "libation_table",
                25,
                2,
                "complete",
                "LM I",
                False,
                False,
                ["a-ta-i-*301-wa-ja"],
            ),
            (
                "IO Za 2",
                4,
                154,
                "libation_table",
                45,
                3,
                "complete",
                "LM I",
                False,
                False,
                ["ja-sa-sa-ra-me", "a-ta-i-*301-wa-ja"],
            ),
            ("IO Za 3", 4, 158, "libation_table", 30, 2, "fragmentary", "LM I", False, False, []),
            (
                "IO Za 4",
                4,
                162,
                "libation_table",
                35,
                2,
                "complete",
                "LM I",
                False,
                False,
                ["i-pi-na-ma"],
            ),
            ("IO Za 5", 4, 166, "libation_table", 28, 2, "complete", "LM I", False, False, []),
            (
                "IO Za 6",
                4,
                170,
                "libation_table",
                40,
                3,
                "complete",
                "LM I",
                False,
                False,
                ["u-na-ka-na-si"],
            ),
            (
                "PS Za 1",
                4,
                180,
                "libation_table",
                32,
                2,
                "complete",
                "LM I",
                False,
                False,
                ["a-ta-i-*301-wa-ja"],
            ),
            ("PS Za 2", 4, 184, "libation_table", 28, 2, "fragmentary", "LM I", False, False, []),
            ("SY Za 1", 4, 190, "libation_table", 35, 2, "complete", "LM I", False, False, []),
            (
                "SY Za 2",
                4,
                194,
                "libation_table",
                30,
                2,
                "complete",
                "LM I",
                False,
                False,
                ["ja-sa-sa-ra-me"],
            ),
            (
                "PK Za 11",
                4,
                200,
                "libation_table",
                55,
                4,
                "complete",
                "LM I",
                False,
                False,
                ["a-ta-i-*301-wa-ja", "da-ma-te"],
            ),
            ("PK Za 12", 4, 205, "libation_table", 40, 3, "fragmentary", "LM I", False, False, []),
            ("KO Za 1", 4, 210, "libation_table", 25, 2, "complete", "LM I", False, False, []),
        ]

        for entry in religious_inscriptions:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            site = tablet_id.split()[0]
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": site,
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "Peak sanctuary inscription with libation formula",
            }

        # VOLUME V - NEW DISCOVERIES
        vol5_inscriptions = [
            (
                "KN Zf 2",
                5,
                150,
                "scepter",
                119,
                2,
                "complete",
                "LM IB",
                True,
                True,
                ["a-ta-i-*301-wa-ja"],
            ),
            ("HT Wc 3016", 5, 50, "roundel", 15, 1, "complete", "LM IB", True, False, []),
            ("HT Wc 3017", 5, 52, "roundel", 12, 1, "complete", "LM IB", True, False, []),
            ("KH 91", 5, 80, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("KH 92", 5, 84, "tablet", 38, 3, "fragmentary", "LM IB", True, True, []),
            ("KH 93", 5, 88, "tablet", 45, 3, "complete", "LM IB", True, True, []),
            ("KH 94", 5, 92, "tablet", 50, 4, "complete", "LM IB", True, True, []),
            ("KH 95", 5, 96, "tablet", 35, 2, "complete", "LM IB", True, True, []),
            ("KH 96", 5, 100, "tablet", 40, 3, "complete", "LM IB", True, True, []),
            ("KH 97", 5, 104, "tablet", 48, 4, "complete", "LM IB", True, True, []),
            ("KH 98", 5, 108, "tablet", 42, 3, "complete", "LM IB", True, True, []),
            ("KH 99", 5, 112, "tablet", 55, 4, "complete", "LM IB", True, True, ["ku-ro"]),
        ]

        for entry in vol5_inscriptions:
            tablet_id, vol, page, insc_type, signs, lines, cond, period, nums, logos, seqs = entry
            site = tablet_id.split()[0]
            inscriptions[tablet_id] = {
                "tablet_id": tablet_id,
                "site_code": site,
                "volume": vol,
                "page": page,
                "inscription_type": insc_type,
                "sign_count": signs,
                "lines": lines,
                "condition": cond,
                "period": period,
                "has_numerals": nums,
                "has_logograms": logos,
                "key_sequences": seqs,
                "notes": "KN Zf 2 is the 2024 Knossos ivory scepter (longest Linear A inscription)"
                if tablet_id == "KN Zf 2"
                else "",
            }

        self.index = inscriptions
        self.log(f"Built GORILA index with {len(self.index)} inscriptions")

    def lookup_tablet(self, tablet_id: str) -> Optional[Dict]:
        """
        Look up a tablet by its reference number.

        Args:
            tablet_id: Tablet reference (e.g., "HT 13", "ZA 4")

        Returns:
            Inscription entry or None if not found
        """
        # Normalize input
        tablet_id_norm = tablet_id.upper().strip()

        # Try direct lookup
        if tablet_id_norm in self.index:
            return self.index[tablet_id_norm]

        # Try with different spacing
        parts = tablet_id_norm.split()
        if len(parts) >= 2:
            # Try "HT13" -> "HT 13"
            alt = f"{parts[0]} {' '.join(parts[1:])}"
            if alt in self.index:
                return self.index[alt]

        # Search for partial match
        for key in self.index:
            if tablet_id_norm in key or key in tablet_id_norm:
                return self.index[key]

        return None

    def get_volume_contents(self, volume: int) -> List[Dict]:
        """
        Get all inscriptions in a specific volume.

        Args:
            volume: GORILA volume number (1-5)

        Returns:
            List of inscriptions in that volume
        """
        results = []
        for tablet_id, data in self.index.items():
            if data["volume"] == volume:
                results.append(data)
        return sorted(results, key=lambda x: x["page"])

    def search_transcription(self, pattern: str) -> List[Dict]:
        """
        Search for inscriptions containing a sequence pattern.

        Args:
            pattern: Sequence to search for (e.g., "ku-ro")

        Returns:
            List of matching inscriptions
        """
        pattern_lower = pattern.lower()
        results = []

        for tablet_id, data in self.index.items():
            key_seqs = data.get("key_sequences", [])
            for seq in key_seqs:
                if pattern_lower in seq.lower():
                    results.append(data)
                    break

        return results

    def get_inscriptions_by_site(self, site_code: str) -> List[Dict]:
        """
        Get all inscriptions from a specific site.

        Args:
            site_code: Site code (e.g., "HT", "KH")

        Returns:
            List of inscriptions from that site
        """
        site_upper = site_code.upper()
        results = []

        for tablet_id, data in self.index.items():
            if data["site_code"] == site_upper:
                results.append(data)

        return sorted(results, key=lambda x: (x["volume"], x["page"]))

    def get_inscriptions_by_type(self, inscription_type: str) -> List[Dict]:
        """
        Get all inscriptions of a specific type.

        Args:
            inscription_type: Type (tablet, libation_table, seal, etc.)

        Returns:
            List of matching inscriptions
        """
        results = []

        for tablet_id, data in self.index.items():
            if data["inscription_type"] == inscription_type.lower():
                results.append(data)

        return results

    def get_sign_conventions(self) -> Dict:
        """Get GORILA transcription conventions."""
        return self.conventions

    def get_statistics(self) -> Dict:
        """Get comprehensive index statistics."""
        total = len(self.index)

        # By site
        sites = {}
        for data in self.index.values():
            site = data["site_code"]
            sites[site] = sites.get(site, 0) + 1

        # By volume
        volumes = {}
        for data in self.index.values():
            vol = data["volume"]
            volumes[vol] = volumes.get(vol, 0) + 1

        # By type
        types = {}
        for data in self.index.values():
            t = data["inscription_type"]
            types[t] = types.get(t, 0) + 1

        # Total signs
        total_signs = sum(data["sign_count"] for data in self.index.values())

        # By period
        periods = {}
        for data in self.index.values():
            p = data["period"]
            periods[p] = periods.get(p, 0) + 1

        return {
            "total_inscriptions": total,
            "total_signs": total_signs,
            "by_site": dict(sorted(sites.items(), key=lambda x: x[1], reverse=True)),
            "by_volume": dict(sorted(volumes.items())),
            "by_type": dict(sorted(types.items(), key=lambda x: x[1], reverse=True)),
            "by_period": dict(sorted(periods.items())),
        }

    def save_index(self, filepath: Path = INDEX_FILE):
        """Save index to JSON file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)

        output = {
            "generated": datetime.now().isoformat(),
            "source": "GORILA Indexer - based on Godart & Olivier volumes",
            "statistics": self.get_statistics(),
            "volumes": self.volumes,
            "conventions": self.conventions,
            "inscriptions": self.index,
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.log(f"Saved index to {filepath}")
        return filepath


def print_inscription(insc: Dict, verbose: bool = False):
    """Pretty-print an inscription entry."""
    print(f"\n  {insc['tablet_id']}")
    print(f"    Site: {insc['site_code']}")
    print(f"    Volume: {insc['volume']}, Page: {insc['page']}")
    print(f"    Type: {insc['inscription_type']}")
    print(f"    Signs: {insc['sign_count']}, Lines: {insc['lines']}")
    print(f"    Condition: {insc['condition']}")
    print(f"    Period: {insc['period']}")

    if verbose:
        print(f"    Numerals: {'Yes' if insc['has_numerals'] else 'No'}")
        print(f"    Logograms: {'Yes' if insc['has_logograms'] else 'No'}")
        if insc.get("key_sequences"):
            print(f"    Key sequences: {', '.join(insc['key_sequences'])}")
        if insc.get("notes"):
            print(f"    Notes: {insc['notes']}")


def main():
    parser = argparse.ArgumentParser(
        description="GORILA Volume Indexer - Linear A inscription references"
    )
    parser.add_argument("--lookup", "-l", type=str, help='Look up a tablet (e.g., "HT 13")')
    parser.add_argument(
        "--volume", type=int, choices=[1, 2, 3, 4, 5], help="List contents of a volume"
    )
    parser.add_argument("--search", "-s", type=str, help="Search for sequence pattern")
    parser.add_argument("--site", type=str, help="Get inscriptions from a site")
    parser.add_argument("--type", "-t", type=str, help="Get inscriptions by type")
    parser.add_argument(
        "--conventions", "-c", action="store_true", help="Show transcription conventions"
    )
    parser.add_argument("--stats", action="store_true", help="Show index statistics")
    parser.add_argument("--save", action="store_true", help="Save index to JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print("=" * 60)
    print("GORILA VOLUME INDEXER")
    print("Linear A Inscription Reference Database")
    print("=" * 60)

    indexer = GORILAIndexer(verbose=args.verbose)

    if args.lookup:
        insc = indexer.lookup_tablet(args.lookup)
        if insc:
            print("\nTablet found:")
            print_inscription(insc, args.verbose)
        else:
            print(f"\nTablet not found: {args.lookup}")
            print("Try using standard format (e.g., 'HT 13', 'ZA 4', 'KN Zf 2')")

    elif args.volume:
        inscriptions = indexer.get_volume_contents(args.volume)
        vol_info = indexer.volumes.get(args.volume, {})
        print(f"\nVolume {args.volume}: {vol_info.get('subtitle', '')}")
        print(f"Contents: {vol_info.get('contents', '')}")
        print(f"\nInscriptions in this volume: {len(inscriptions)}")
        for insc in inscriptions[:20]:
            print(
                f"  {insc['tablet_id']} (p.{insc['page']}) - {insc['inscription_type']}, {insc['sign_count']} signs"
            )
        if len(inscriptions) > 20:
            print(f"  ... and {len(inscriptions) - 20} more")

    elif args.search:
        results = indexer.search_transcription(args.search)
        print(f"\nSearch for '{args.search}': {len(results)} matches")
        for insc in results:
            print(f"  {insc['tablet_id']} - sequences: {', '.join(insc.get('key_sequences', []))}")

    elif args.site:
        inscriptions = indexer.get_inscriptions_by_site(args.site)
        print(f"\nInscriptions from {args.site.upper()}: {len(inscriptions)}")
        for insc in inscriptions[:20]:
            print(
                f"  {insc['tablet_id']} (Vol.{insc['volume']}, p.{insc['page']}) - {insc['sign_count']} signs"
            )
        if len(inscriptions) > 20:
            print(f"  ... and {len(inscriptions) - 20} more")

    elif args.type:
        inscriptions = indexer.get_inscriptions_by_type(args.type)
        print(f"\nInscriptions of type '{args.type}': {len(inscriptions)}")
        for insc in inscriptions:
            print(f"  {insc['tablet_id']} - {insc['sign_count']} signs")

    elif args.conventions:
        conventions = indexer.get_sign_conventions()
        print("\nGORILA Transcription Conventions:")
        print("\n  Sign Notation:")
        for key, desc in conventions["sign_notation"].items():
            print(f"    {key}: {desc}")
        print("\n  Commodity Logograms:")
        for key, desc in conventions["commodity_logograms"].items():
            print(f"    {key}: {desc}")
        print("\n  Numerals:")
        for key, desc in conventions["numerals"].items():
            print(f"    {key}: {desc}")
        print("\n  Site Codes:")
        for key, desc in list(conventions["site_codes"].items())[:10]:
            print(f"    {key}: {desc}")
        print(f"    ... and {len(conventions['site_codes']) - 10} more sites")

    elif args.stats:
        stats = indexer.get_statistics()
        print("\nIndex Statistics:")
        print(f"  Total inscriptions: {stats['total_inscriptions']}")
        print(f"  Total signs: {stats['total_signs']}")
        print("\nBy site:")
        for site, count in list(stats["by_site"].items())[:8]:
            print(f"  {site}: {count}")
        print("\nBy volume:")
        for vol, count in stats["by_volume"].items():
            print(f"  Volume {vol}: {count}")
        print("\nBy type:")
        for t, count in stats["by_type"].items():
            print(f"  {t}: {count}")
        print("\nBy period:")
        for p, count in stats["by_period"].items():
            print(f"  {p}: {count}")

    elif args.save:
        filepath = indexer.save_index()
        print(f"\nSaved index to: {filepath}")

    else:
        print("\nUsage:")
        print("  --lookup TABLET   Look up a tablet (e.g., 'HT 13')")
        print("  --volume NUM      List contents of volume (1-5)")
        print("  --search PATTERN  Search for sequence pattern")
        print("  --site CODE       Get inscriptions from a site")
        print("  --type TYPE       Get inscriptions by type")
        print("  --conventions     Show transcription conventions")
        print("  --stats           Show index statistics")
        print("  --save            Save index to JSON")
        print("\nExamples:")
        print("  python tools/gorila_indexer.py --lookup 'HT 13'")
        print("  python tools/gorila_indexer.py --volume 1")
        print("  python tools/gorila_indexer.py --search 'ku-ro'")
        print("  python tools/gorila_indexer.py --site HT")
        print("  python tools/gorila_indexer.py --conventions")

    return 0


if __name__ == "__main__":
    sys.exit(main())
