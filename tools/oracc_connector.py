#!/usr/bin/env python3
"""
ORACC Connector for Linear A Decipherment Project

Connects to ORACC (Open Richly Annotated Cuneiform Corpus) to fetch Akkadian
administrative vocabulary for comparative analysis with Linear A.

ORACC API Structure:
    - Main portal: https://oracc.museum.upenn.edu/
    - Build server: https://build-oracc.museum.upenn.edu/
    - JSON endpoint: http://build-oracc.museum.upenn.edu/json/[PROJECT]
    - Glossary pattern: http://oracc.museum.upenn.edu/[PROJECT]/[LANG]

Key Projects:
    - SAA (State Archives of Assyria): Neo-Assyrian administrative texts
    - RINAP (Royal Inscriptions of the Neo-Assyrian Period)
    - CDLI (Cuneiform Digital Library Initiative)
    - epsd2 (Electronic Pennsylvania Sumerian Dictionary v2)
    - ribo (Royal Inscriptions of Babylonia Online)

Fallback:
    If live API is inaccessible, uses comprehensive static dictionary
    compiled from CAD (Chicago Assyrian Dictionary) and CDA (Concise
    Dictionary of Akkadian).

Usage:
    python tools/oracc_connector.py --fetch          # Fetch from ORACC
    python tools/oracc_connector.py --build-static   # Build static dictionary
    python tools/oracc_connector.py --query nadānu   # Query a term
    python tools/oracc_connector.py --category totaling  # Get category terms
    python tools/oracc_connector.py --stats          # Show vocabulary stats

Attribution:
    Part of Linear A Decipherment Project (OPERATION MINOS III)
    ORACC data licensed CC0 (public domain)
"""

import json
import argparse
import sys
import os
import ssl
import urllib.request
import urllib.error
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
COMPARATIVE_DIR = DATA_DIR / "comparative"
OUTPUT_FILE = COMPARATIVE_DIR / "akkadian_oracc.json"
CACHE_DIR = COMPARATIVE_DIR / "cache"

# ORACC API endpoints
ORACC_BASE = "https://oracc.museum.upenn.edu"
ORACC_BUILD = "http://build-oracc.museum.upenn.edu"
ORACC_PROJECTS_URL = f"{ORACC_BASE}/projects.json"

# Relevant ORACC projects for administrative vocabulary
RELEVANT_PROJECTS = [
    "saao/saa01",      # State Archives of Assyria Volume 1
    "saao/saa05",      # State Archives - Treaties and Loyalty Oaths
    "saao/saa10",      # Letters from Assyrian scholars
    "saao/saa13",      # Letters from Priests
    "saao/saa15",      # Babylonian Letters from Archives
    "ribo",            # Royal Inscriptions of Babylonia
    "cams/gkab",       # Corpus of Ancient Mesopotamian Scholarship
    "epsd2-admin-ur3", # Ur III Administrative corpus
    "cdli",            # Cuneiform Digital Library
]


@dataclass
class AkkadianTerm:
    """Represents an Akkadian term with full metadata."""
    term: str                          # The Akkadian word
    meaning: str                       # Primary meaning/translation
    root: str                          # Root consonants (e.g., KLL, ŠRK)
    usage: str                         # How it's used administratively
    context: str                       # Typical context of appearance
    examples: List[str] = field(default_factory=list)  # Example sentences
    source: str = ""                   # Primary reference (CAD, CDA, etc.)
    secondary_sources: List[str] = field(default_factory=list)  # Additional refs
    oracc_refs: List[str] = field(default_factory=list)  # ORACC text references
    category: str = ""                 # Semantic category
    confidence: str = "HIGH"           # Confidence level
    cognates: Dict[str, str] = field(default_factory=dict)  # Related languages
    notes: str = ""                    # Additional notes


class ORACCConnector:
    """
    Connector to ORACC for Akkadian vocabulary.

    Attempts live API access; falls back to comprehensive static dictionary
    based on CAD, CDA, and published Assyriology literature.
    """

    def __init__(self, verbose: bool = False, offline: bool = False):
        self.verbose = verbose
        self.offline = offline
        self.vocabulary: Dict[str, Dict] = {}
        self._ensure_dirs()

    def _ensure_dirs(self):
        """Create necessary directories."""
        COMPARATIVE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, msg: str, level: str = "info"):
        """Log message if verbose."""
        if self.verbose:
            getattr(logger, level)(msg)

    def _fetch_url(self, url: str, timeout: int = 30) -> Optional[Dict]:
        """Fetch JSON from URL with error handling."""
        if self.offline:
            self.log(f"Offline mode: skipping {url}")
            return None

        try:
            # Create SSL context that doesn't verify certificates
            # (ORACC sometimes has certificate issues)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'LinearA-Decipherment/1.0'}
            )

            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data

        except urllib.error.HTTPError as e:
            self.log(f"HTTP Error {e.code}: {url}", "warning")
            return None
        except urllib.error.URLError as e:
            self.log(f"URL Error: {e.reason}", "warning")
            return None
        except Exception as e:
            self.log(f"Error fetching {url}: {e}", "warning")
            return None

    def fetch_oracc_projects(self) -> Optional[List[str]]:
        """Fetch list of available ORACC projects."""
        self.log("Fetching ORACC project list...")
        data = self._fetch_url(ORACC_PROJECTS_URL)
        if data and 'public' in data:
            return data['public']
        return None

    def fetch_project_glossary(self, project: str, lang: str = "akk") -> Optional[Dict]:
        """
        Fetch glossary for a specific project and language.

        Args:
            project: ORACC project name (e.g., "saao/saa01")
            lang: Language code (akk = Akkadian)
        """
        # Try glossary JSON endpoint
        url = f"{ORACC_BUILD}/json/{project}"
        self.log(f"Fetching glossary: {url}")

        data = self._fetch_url(url)
        if data:
            # Cache the result
            cache_file = CACHE_DIR / f"{project.replace('/', '_')}_{lang}.json"
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                self.log(f"Cached: {cache_file}")
            except Exception as e:
                self.log(f"Cache write error: {e}", "warning")

        return data

    def parse_glossary_entries(self, glossary_data: Dict) -> List[AkkadianTerm]:
        """Parse ORACC glossary format into AkkadianTerm objects."""
        terms = []

        if not glossary_data:
            return terms

        # ORACC glossary structure has 'entries' with lemma data
        entries = glossary_data.get('entries', glossary_data.get('terms', []))

        for entry in entries:
            if isinstance(entry, dict):
                cf = entry.get('cf', '')  # Citation form
                gw = entry.get('gw', '')  # Guide word (meaning)
                pos = entry.get('pos', '')  # Part of speech

                if cf and gw:
                    term = AkkadianTerm(
                        term=cf,
                        meaning=gw,
                        root=self._extract_root(cf),
                        usage=pos,
                        context="ORACC corpus",
                        source="ORACC",
                    )
                    terms.append(term)

        return terms

    def _extract_root(self, term: str) -> str:
        """Extract consonantal root from Akkadian term."""
        # Remove vowels and common endings to approximate root
        consonants = ''.join(c for c in term.upper()
                           if c in 'BCDFGHJKLMNPQRSTVWXYZḪŠṢṬ')
        return consonants[:4] if len(consonants) > 4 else consonants

    def fetch_all_glossaries(self) -> int:
        """
        Attempt to fetch glossaries from all relevant projects.
        Returns count of terms found.
        """
        total_terms = 0

        for project in RELEVANT_PROJECTS:
            self.log(f"Fetching {project}...")
            data = self.fetch_project_glossary(project)
            if data:
                terms = self.parse_glossary_entries(data)
                for t in terms:
                    if t.term not in self.vocabulary:
                        self.vocabulary[t.term] = asdict(t)
                        total_terms += 1

        return total_terms

    def build_static_dictionary(self) -> int:
        """
        Build comprehensive static dictionary from published sources.

        Sources:
        - CAD (Chicago Assyrian Dictionary) - 21 volumes
        - CDA (Concise Dictionary of Akkadian) - Black et al.
        - SAAo (State Archives of Assyria Online)
        - Published Assyriology literature

        Categories focus on Linear A comparative analysis needs:
        - Totaling/quantities
        - Deficit/shortage
        - Allocation/distribution
        - Commodities
        - Counting/recording
        - Personnel/occupations
        - Temple/religious
        - Trade/commerce
        """

        self.log("Building comprehensive static dictionary...")

        # Vocabulary organized by semantic category
        vocabulary = {}

        # ============================================================
        # CATEGORY 1: TOTALING AND QUANTITIES
        # ============================================================
        totaling_terms = {
            'napḫaru': {
                'term': 'napḫaru',
                'meaning': 'total, sum, entirety, aggregate',
                'root': 'PḪR',
                'usage': 'Administrative totaling at end of commodity lists',
                'context': 'Most common term for "total" in Neo-Assyrian/Babylonian texts; appears at list endings',
                'examples': [
                    'PAP 3 MA.NA napḫar - "total: 3 minas altogether"',
                    'napḫar nikkassī - "sum total of accounts"',
                    'napḫar ša UD.x.KAM - "total for day x"'
                ],
                'source': 'CAD N/1 pp.296-302',
                'secondary_sources': ['CDA p.232', 'SAA glossaries'],
                'category': 'totaling',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'פחד (related root)'},
                'notes': 'Primary totaling term in Neo-Assyrian administrative texts'
            },
            'kullatu': {
                'term': 'kullatu',
                'meaning': 'totality, all, entirety, whole amount',
                'root': 'KLL',
                'usage': 'Indicates completeness of a set or collection',
                'context': 'Abstract noun for "the whole"; emphatic totaling',
                'examples': [
                    'kul-la-at šīmātim - "the totality of the prices"',
                    'kullat nišī - "all the people"',
                    'kullat māt Aššur - "all of Assyria"'
                ],
                'source': 'CAD K pp.505-507',
                'secondary_sources': ['CDA p.165'],
                'category': 'totaling',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'כֹּל kōl', 'Ugaritic': 'kl', 'Arabic': 'كُلّ kull'},
                'notes': 'Strong Semitic etymology; potential cognate for Linear A ku-ro'
            },
            'kalû': {
                'term': 'kalû',
                'meaning': 'all, every, the whole of, entire',
                'root': 'KL',
                'usage': 'Adjective/determiner for totality',
                'context': 'Modifies nouns to indicate completeness',
                'examples': [
                    'kalu awīlū - "all the men"',
                    'ana kali šattim - "for the whole year"',
                    'kalu ūmī - "every day, always"'
                ],
                'source': 'CAD K pp.89-99',
                'secondary_sources': ['CDA p.142'],
                'category': 'totaling',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'כֹּל kōl', 'Aramaic': 'כֹּל'},
                'notes': 'Basic Semitic root for "all/every"'
            },
            'gimru': {
                'term': 'gimru',
                'meaning': 'totality, entirety, complete amount, all',
                'root': 'GMR',
                'usage': 'Alternative totaling term in lists',
                'context': 'Often interchangeable with kullatu',
                'examples': [
                    'gimri - "in total"',
                    'ana gimrišu - "in its entirety"',
                    'gimrat eqlī - "the total of the fields"'
                ],
                'source': 'CAD G pp.75-78',
                'secondary_sources': ['CDA p.93'],
                'category': 'totaling',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'גמר gāmar (to complete)'},
                'notes': 'Emphasizes completion/finality'
            },
            'gabbû': {
                'term': 'gabbû',
                'meaning': 'all, totality, the whole, every',
                'root': 'GB',
                'usage': 'Inclusive totality marker',
                'context': 'Often in contracts and legal texts',
                'examples': [
                    'gabbî - "all of it"',
                    'ana gabbi - "to/for all"',
                    'gabbu u mimmû - "all and everything"'
                ],
                'source': 'CAD G pp.1-4',
                'secondary_sources': ['CDA p.88'],
                'category': 'totaling',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Possibly West Semitic origin'
            },
            'pāḫiru': {
                'term': 'pāḫiru',
                'meaning': 'gatherer, one who collects, assembler',
                'root': 'PḪR',
                'usage': 'Agent noun from napḫaru root',
                'context': 'Person who totals/collects items',
                'examples': [
                    'pāḫir nikkassī - "collector of accounts"'
                ],
                'source': 'CAD P pp.9-10',
                'secondary_sources': ['CDA p.255'],
                'category': 'totaling',
                'confidence': 'MEDIUM',
                'cognates': {},
                'notes': 'Related to napḫaru totaling function'
            },
        }

        # ============================================================
        # CATEGORY 2: DEFICIT AND SHORTAGE
        # ============================================================
        deficit_terms = {
            'ḫurrāqu': {
                'term': 'ḫurrāqu',
                'meaning': 'deficit, shortage, missing amount',
                'root': 'ḪRQ',
                'usage': 'Marks shortfall in accounts',
                'context': 'Administrative notation for quantities owing or missing',
                'examples': [
                    'ḫurrāq ša PN - "deficit of PN"',
                    '1 GUR ḫurrāqu - "1 gur deficit"'
                ],
                'source': 'CAD Ḫ pp.252-253',
                'secondary_sources': ['CDA p.125'],
                'category': 'deficit',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Technical accounting term for shortfall'
            },
            'matû': {
                'term': 'matû',
                'meaning': 'to decrease, diminish, be less, fall short',
                'root': 'MTʾ',
                'usage': 'Verb indicating reduction or insufficiency',
                'context': 'When quantities do not meet expected amounts',
                'examples': [
                    'imtūt - "it decreased"',
                    'ul imaṭṭi - "it shall not decrease"',
                    'ša imtutu - "what has diminished"'
                ],
                'source': 'CAD M/1 pp.413-418',
                'secondary_sources': ['CDA p.199'],
                'category': 'deficit',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'מָעַט māʿaṭ (to be few)'},
                'notes': 'Common verb for shortage/decrease'
            },
            'zittu': {
                'term': 'zittu',
                'meaning': 'share, portion, allotment, part',
                'root': 'ZZ',
                'usage': 'Division or portion of total',
                'context': 'What each person receives from distribution',
                'examples': [
                    'zitti palê - "share of the reign"',
                    'zittašu - "his share"',
                    'zittī lā iltaqi - "he did not receive my share"'
                ],
                'source': 'CAD Z pp.143-149',
                'secondary_sources': ['CDA p.450'],
                'category': 'deficit',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Can indicate what is missing from full allocation'
            },
            'māḫiru': {
                'term': 'māḫiru',
                'meaning': 'exchange rate, price, equivalent value',
                'root': 'MḪR',
                'usage': 'Value calculation in trade',
                'context': 'Determines shortage when values do not match',
                'examples': [
                    'māḫir kaspi - "exchange rate of silver"',
                    'māḫir še ī - "price of barley"'
                ],
                'source': 'CAD M/1 pp.86-91',
                'secondary_sources': ['CDA p.186'],
                'category': 'deficit',
                'confidence': 'MEDIUM',
                'cognates': {},
                'notes': 'Used in balance calculations'
            },
            'ḫalāqu': {
                'term': 'ḫalāqu',
                'meaning': 'to disappear, be lost, perish, go missing',
                'root': 'ḪLQ',
                'usage': 'Recording losses in inventory',
                'context': 'Items that cannot be accounted for',
                'examples': [
                    'iḫtaliq - "it was lost"',
                    'ša iḫliqu - "that which is lost"',
                    'lā iḫalliq - "it shall not be lost"'
                ],
                'source': 'CAD Ḫ pp.35-42',
                'secondary_sources': ['CDA p.101'],
                'category': 'deficit',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חלק (different meaning)'},
                'notes': 'Used for unrecoverable losses'
            },
            'waṣû': {
                'term': 'waṣû',
                'meaning': 'to go out, exit, be expended, depart',
                'root': 'WṢ',
                'usage': 'Expenditure from stores',
                'context': 'Items leaving inventory (outflow)',
                'examples': [
                    'ittaṣi - "it went out"',
                    'muṣû - "expenditure, outgoing"',
                    'ša uṣṣû - "that which went out"'
                ],
                'source': 'CAD A/2 pp.399-418 (as aṣû)',
                'secondary_sources': ['CDA p.28'],
                'category': 'deficit',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'יצא yāṣāʾ'},
                'notes': 'Opposite of erēbu (income/entry)'
            },
            'riāqu': {
                'term': 'riāqu',
                'meaning': 'to be empty, remain over, be left vacant',
                'root': 'RYQ',
                'usage': 'Indicating empty or unfilled allocation',
                'context': 'When expected quantity is not filled',
                'examples': [
                    'rīqu - "empty, vacant"',
                    'rīqūtu - "emptiness"'
                ],
                'source': 'CAD R pp.365-368',
                'secondary_sources': ['CDA p.304'],
                'category': 'deficit',
                'confidence': 'MEDIUM',
                'cognates': {'Hebrew': 'ריק rêq (empty)'},
                'notes': 'Describes unfilled slots/allocations'
            },
        }

        # ============================================================
        # CATEGORY 3: ALLOCATION AND DISTRIBUTION
        # ============================================================
        allocation_terms = {
            'zīzu': {
                'term': 'zīzu',
                'meaning': 'to divide, distribute, share, allocate',
                'root': 'ZZ',
                'usage': 'Division and distribution of goods/labor',
                'context': 'Primary verb for administrative allocation',
                'examples': [
                    'uzazzû eqlam - "they divided the field"',
                    'ziztu - "division, distribution"',
                    'uzuzzu - "to be shared"'
                ],
                'source': 'CAD Z pp.150-153',
                'secondary_sources': ['CDA p.450'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Core distribution terminology'
            },
            'qâpu': {
                'term': 'qâpu',
                'meaning': 'to entrust, commit, confide, hand over',
                'root': 'QP',
                'usage': 'Entrusting goods to responsible party',
                'context': 'Transfer of responsibility for items',
                'examples': [
                    'ana PN iqīp - "he entrusted to PN"',
                    'qīpu - "trustee, commissioner"'
                ],
                'source': 'CAD Q pp.173-177',
                'secondary_sources': ['CDA p.284'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Implies responsibility for allocated goods'
            },
            'nadānu': {
                'term': 'nadānu',
                'meaning': 'to give, grant, deliver, pay, sell',
                'root': 'NDN',
                'usage': 'Basic giving/transfer verb',
                'context': 'Universal for transfers of any kind',
                'examples': [
                    'iddin - "he gave"',
                    'ana PN nadnu - "given to PN"',
                    'nidintum - "gift, grant"'
                ],
                'source': 'CAD N/1 pp.38-86',
                'secondary_sources': ['CDA p.227'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'נתן nātan'},
                'notes': 'Most common transfer verb in Akkadian'
            },
            'šarāku': {
                'term': 'šarāku',
                'meaning': 'to give, grant, present, donate',
                'root': 'ŠRK',
                'usage': 'Formal giving, especially by royalty/temples',
                'context': 'Used for grants and distributions from authority',
                'examples': [
                    'ana PN išruk - "he granted to PN"',
                    'šarku - "given, granted"',
                    'širktu - "grant, donation"'
                ],
                'source': 'CAD Š/2 pp.34-41',
                'secondary_sources': ['CDA p.359'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Potential cognate for Linear A SA-RA - see hypothesis testing'
            },
            'paqādu': {
                'term': 'paqādu',
                'meaning': 'to entrust, hand over, assign, commission',
                'root': 'PQD',
                'usage': 'Official assignment of tasks/goods',
                'context': 'Administrative delegation',
                'examples': [
                    'ipqid - "he entrusted"',
                    'piqdatu - "commission, assignment"',
                    'paqdu - "entrusted property"'
                ],
                'source': 'CAD P pp.123-141',
                'secondary_sources': ['CDA p.262'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'פקד pāqad (to visit, assign)'},
                'notes': 'Used for official assignments'
            },
            'našû': {
                'term': 'našû',
                'meaning': 'to carry, transport, bring, bear',
                'root': 'NŠ',
                'usage': 'Physical transport of allocated goods',
                'context': 'Moving commodities to recipients',
                'examples': [
                    'iššû - "they carried"',
                    'našû - "porter, carrier"',
                    'našâku - "my transport"'
                ],
                'source': 'CAD N/2 pp.86-107',
                'secondary_sources': ['CDA p.246'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'נשא nāśāʾ'},
                'notes': 'Logistics of distribution'
            },
            'erēbu': {
                'term': 'erēbu',
                'meaning': 'to enter, arrive, come in, be received',
                'root': 'ʾRB',
                'usage': 'Income, receipt of goods',
                'context': 'Items entering inventory (inflow)',
                'examples': [
                    'īrub - "it entered"',
                    'erbu - "income, revenue"',
                    'mērēbu - "entrance, entry"'
                ],
                'source': 'CAD E pp.260-282',
                'secondary_sources': ['CDA p.75'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'ערב ʿereb (evening - entering)'},
                'notes': 'Opposite of waṣû (expenditure)'
            },
            'šūṣû': {
                'term': 'šūṣû',
                'meaning': 'to bring out, remove, expend, withdraw',
                'root': 'WṢ (causative)',
                'usage': 'Authorized expenditure',
                'context': 'Official withdrawal from stores',
                'examples': [
                    'ušēṣi - "he brought out"',
                    'šūṣû - "withdrawal"'
                ],
                'source': 'CAD Š/3 pp.375-384',
                'secondary_sources': ['CDA p.388'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Causative of waṣû'
            },
            'maḫāru': {
                'term': 'maḫāru',
                'meaning': 'to receive, accept, confront, face',
                'root': 'MḪR',
                'usage': 'Receiving allocated goods',
                'context': 'Acknowledgment of receipt',
                'examples': [
                    'imḫur - "he received"',
                    'maḫīru - "receiver"',
                    'maḫirtu - "receipt"'
                ],
                'source': 'CAD M/1 pp.55-86',
                'secondary_sources': ['CDA p.185'],
                'category': 'allocation',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Confirms transfer of goods'
            },
            'rakāsu': {
                'term': 'rakāsu',
                'meaning': 'to bind, tie, collect together, organize',
                'root': 'RKS',
                'usage': 'Binding/organizing allocations',
                'context': 'Bundling goods for distribution',
                'examples': [
                    'riksu - "binding, contract"',
                    'rikis - "bale, bundle"',
                    'raksu - "bound together"'
                ],
                'source': 'CAD R pp.109-122',
                'secondary_sources': ['CDA p.296'],
                'category': 'allocation',
                'confidence': 'MEDIUM',
                'cognates': {},
                'notes': 'Physical bundling of distributed items'
            },
        }

        # ============================================================
        # CATEGORY 4: COMMODITIES
        # ============================================================
        commodity_terms = {
            'šamnu': {
                'term': 'šamnu',
                'meaning': 'oil, fat, grease, sesame oil',
                'root': 'ŠMN',
                'usage': 'Primary commodity in ration texts',
                'context': 'Temple offerings, rations, trade',
                'examples': [
                    'šaman erēni - "cedar oil"',
                    '1 SÌLA šamni - "1 sila of oil"',
                    'šamnu ellu - "pure oil"'
                ],
                'source': 'CAD Š/1 pp.322-330',
                'secondary_sources': ['CDA p.352'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שֶׁמֶן šemen', 'Ugaritic': 'šmn', 'Arabic': 'سمن samn'},
                'notes': 'Common Semitic; compare Linear A OLE+commodity lists'
            },
            'karānu': {
                'term': 'karānu',
                'meaning': 'wine, grape, vine',
                'root': 'KRN',
                'usage': 'Wine commodity in offerings and rations',
                'context': 'Luxury/elite rations, offerings',
                'examples': [
                    '1 DUG karāni - "1 vessel of wine"',
                    'karān māti - "domestic wine"',
                    'karānu ṭābu - "fine wine"'
                ],
                'source': 'CAD K pp.206-210',
                'secondary_sources': ['CDA p.145'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'כֶּרֶם kerem (vineyard)', 'Ugaritic': 'krm'},
                'notes': 'Compare Linear A VIN ideogram contexts'
            },
            'ṭābtu': {
                'term': 'ṭābtu',
                'meaning': 'salt',
                'root': 'ṬB',
                'usage': 'Salt commodity in trade',
                'context': 'Preservation, trade, offerings',
                'examples': [
                    '1 SÌLA ṭābti - "1 sila of salt"',
                    'ṭābat tāmti - "sea salt"'
                ],
                'source': 'CAD Ṭ pp.23-26',
                'secondary_sources': ['CDA p.396'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Related to ṭābu (good, sweet)'
            },
            'šeʾu': {
                'term': 'šeʾu',
                'meaning': 'barley, grain',
                'root': 'Šʾ',
                'usage': 'Most common ration commodity',
                'context': 'Basic ration, offerings, trade',
                'examples': [
                    'ŠE.BA - "barley ration"',
                    '1 GUR še ī - "1 gur of barley"',
                    'ša še ī - "of barley"'
                ],
                'source': 'CAD Š/2 pp.338-347',
                'secondary_sources': ['CDA p.369'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שְׂעֹרָה śeʿōrāh'},
                'notes': 'Compare Linear A GRA ideogram'
            },
            'dišpu': {
                'term': 'dišpu',
                'meaning': 'honey',
                'root': 'DŠP',
                'usage': 'Luxury commodity',
                'context': 'Temple offerings, elite goods',
                'examples': [
                    '1 SÌLA dišpi - "1 sila of honey"',
                    'dišip šadî - "mountain honey"'
                ],
                'source': 'CAD D pp.168-169',
                'secondary_sources': ['CDA p.63'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'דְּבַשׁ debaš'},
                'notes': 'High-value offering item'
            },
            'samīdu': {
                'term': 'samīdu',
                'meaning': 'semolina, coarse flour, groats',
                'root': 'SMD',
                'usage': 'Flour commodity',
                'context': 'Food preparation, offerings',
                'examples': [
                    'samīd našqi - "fine semolina"',
                    '1 BÁN samīdi - "1 ban of semolina"'
                ],
                'source': 'CAD S pp.112-115',
                'secondary_sources': ['CDA p.315'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'סֹלֶת sōlet (fine flour)'},
                'notes': 'Processed grain product'
            },
            'ṣipātu': {
                'term': 'ṣipātu',
                'meaning': 'wool',
                'root': 'ṢPT',
                'usage': 'Textile commodity',
                'context': 'Trade, rations, manufacturing',
                'examples': [
                    'ṣipātu peṣītu - "white wool"',
                    '1 MA.NA ṣipāti - "1 mina of wool"'
                ],
                'source': 'CAD Ṣ pp.200-203',
                'secondary_sources': ['CDA p.329'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Major trade commodity'
            },
            'lubuštu': {
                'term': 'lubuštu',
                'meaning': 'clothing, garment, textile',
                'root': 'LBŠ',
                'usage': 'Textile commodity and ration',
                'context': 'Worker rations, temple garments',
                'examples': [
                    'lubušti ilāni - "garments of the gods"',
                    'lubuštu ša šatti - "yearly clothing ration"'
                ],
                'source': 'CAD L pp.222-228',
                'secondary_sources': ['CDA p.180'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'לָבַשׁ lābaš (to wear)'},
                'notes': 'See Linear A TELA ideogram'
            },
            'qēmu': {
                'term': 'qēmu',
                'meaning': 'flour, meal',
                'root': 'QM',
                'usage': 'Basic food commodity',
                'context': 'Daily rations, offerings',
                'examples': [
                    'qēm našqi - "fine flour"',
                    '1 BÁN qēmi - "1 ban of flour"'
                ],
                'source': 'CAD Q pp.213-218',
                'secondary_sources': ['CDA p.286'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'קֶמַח qemaḥ'},
                'notes': 'Basic grain-derived product'
            },
            'ḫimētu': {
                'term': 'ḫimētu',
                'meaning': 'butter, ghee, clarified butter',
                'root': 'ḪMT',
                'usage': 'Dairy product commodity',
                'context': 'Offerings, elite rations',
                'examples': [
                    '1 SÌLA ḫimēti - "1 sila of butter"',
                    'ḫimētu ṭābtu - "fine butter"'
                ],
                'source': 'CAD Ḫ pp.188-190',
                'secondary_sources': ['CDA p.111'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חֶמְאָה ḥemʾâ'},
                'notes': 'High-value dairy product'
            },
            'šikaru': {
                'term': 'šikaru',
                'meaning': 'beer, alcoholic beverage',
                'root': 'ŠKR',
                'usage': 'Primary beverage ration',
                'context': 'Daily rations, offerings, trade',
                'examples': [
                    '1 DUG šikari - "1 vessel of beer"',
                    'šikar šadî - "mountain beer"',
                    'šikaru dannu - "strong beer"'
                ],
                'source': 'CAD Š/2 pp.414-420',
                'secondary_sources': ['CDA p.376'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שֵׁכָר šēkār'},
                'notes': 'Staple beverage in ration texts'
            },
            'kaspu': {
                'term': 'kaspu',
                'meaning': 'silver, money',
                'root': 'KSP',
                'usage': 'Currency and value measure',
                'context': 'Payment, value notation, trade',
                'examples': [
                    '1 MA.NA kaspim - "1 mina of silver"',
                    'kasap šīmim - "purchase silver"',
                    'ana kaspim - "for money"'
                ],
                'source': 'CAD K pp.250-260',
                'secondary_sources': ['CDA p.148'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'כֶּסֶף kesep'},
                'notes': 'Primary currency/value measure'
            },
            'ḫurāṣu': {
                'term': 'ḫurāṣu',
                'meaning': 'gold',
                'root': 'ḪRṢ',
                'usage': 'Precious metal',
                'context': 'High-value items, temple treasures',
                'examples': [
                    'ḫurāṣ ebbu - "pure gold"',
                    '1 GÍN ḫurāṣi - "1 shekel of gold"'
                ],
                'source': 'CAD Ḫ pp.248-251',
                'secondary_sources': ['CDA p.125'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חָרוּץ ḥārûṣ'},
                'notes': 'Elite/temple commodity'
            },
            'siparru': {
                'term': 'siparru',
                'meaning': 'bronze, copper',
                'root': 'SPR',
                'usage': 'Metal commodity',
                'context': 'Tools, weapons, vessels',
                'examples': [
                    'siparru ellu - "pure bronze"',
                    'kalû siparri - "bronze vessel"'
                ],
                'source': 'CAD S pp.299-303',
                'secondary_sources': ['CDA p.325'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Important Bronze Age metal'
            },
            'lipi': {
                'term': 'lipi',
                'meaning': 'fat, tallow, suet',
                'root': 'LP',
                'usage': 'Animal fat commodity',
                'context': 'Offerings, food preparation',
                'examples': [
                    'lipi alpi - "beef fat"',
                    'lipi immeri - "sheep fat"'
                ],
                'source': 'CAD L pp.199-202',
                'secondary_sources': ['CDA p.178'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Animal-derived product'
            },
        }

        # ============================================================
        # CATEGORY 5: COUNTING AND RECORDING
        # ============================================================
        counting_terms = {
            'manû': {
                'term': 'manû',
                'meaning': 'to count, reckon, calculate, assign number',
                'root': 'MN',
                'usage': 'Basic counting operation',
                'context': 'Inventory, census, accounting',
                'examples': [
                    'imnû - "they counted"',
                    'minûtu - "counting, calculation"',
                    'manû - "counted, reckoned"'
                ],
                'source': 'CAD M/1 pp.221-226',
                'secondary_sources': ['CDA p.195'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'מנה mānâ'},
                'notes': 'Core counting terminology'
            },
            'šapāru': {
                'term': 'šapāru',
                'meaning': 'to send, write, dispatch, order',
                'root': 'ŠPR',
                'usage': 'Recording and sending documents',
                'context': 'Scribal activity, communication',
                'examples': [
                    'ṭuppam išpur - "he sent a tablet"',
                    'šipru - "message, work"',
                    'šāpiru - "sender, overseer"'
                ],
                'source': 'CAD Š/1 pp.415-430',
                'secondary_sources': ['CDA p.355'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'ספר spr (to count, write)'},
                'notes': 'Connects counting to writing'
            },
            'nikassu': {
                'term': 'nikassu',
                'meaning': 'property, capital, assets, account',
                'root': 'NKS',
                'usage': 'Accounting term for assets',
                'context': 'Financial accounting',
                'examples': [
                    'nikassī - "accounts"',
                    'napḫar nikassī - "total of accounts"',
                    'rab nikassī - "chief accountant"'
                ],
                'source': 'CAD N/2 pp.220-225',
                'secondary_sources': ['CDA p.249'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Technical accounting term'
            },
            'šatāru': {
                'term': 'šatāru',
                'meaning': 'to write, inscribe, record',
                'root': 'ŠṬR',
                'usage': 'Scribal recording',
                'context': 'Document creation',
                'examples': [
                    'šaṭir - "it is written"',
                    'šaṭāru - "document"',
                    'šāṭiru - "writer, scribe"'
                ],
                'source': 'CAD Š/2 pp.196-206',
                'secondary_sources': ['CDA p.366'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שׁטר šṭr (document)'},
                'notes': 'Writing/documentation'
            },
            'limu': {
                'term': 'limu',
                'meaning': 'thousand, eponym (year official)',
                'root': 'LM',
                'usage': 'Large quantity notation',
                'context': 'Large numbers, dating',
                'examples': [
                    '1 li-mu - "1000"',
                    'lim alpi - "1000 oxen"'
                ],
                'source': 'CAD L pp.205-208',
                'secondary_sources': ['CDA p.179'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Large quantity designation'
            },
            'mēat': {
                'term': 'mēat',
                'meaning': 'hundred',
                'root': 'M T',
                'usage': 'Numerical notation',
                'context': 'Medium-large quantities',
                'examples': [
                    '1 me-at - "100"',
                    '2 mēat - "200"'
                ],
                'source': 'CAD M/1 pp.135-137',
                'secondary_sources': ['CDA p.201'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Standard hundred notation'
            },
            'išten': {
                'term': 'išten',
                'meaning': 'one, single, same, first',
                'root': 'ʾḤD (Semitic)',
                'usage': 'Basic numeral',
                'context': 'Counting, singular items',
                'examples': [
                    'ištēn awīlu - "one man"',
                    'ina ištēn - "together, at once"'
                ],
                'source': 'CAD I/J pp.271-280',
                'secondary_sources': ['CDA p.134'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אֶחָד ʾeḥād'},
                'notes': 'Basic counting unit'
            },
            'šina': {
                'term': 'šina',
                'meaning': 'two',
                'root': 'ŠN',
                'usage': 'Basic numeral',
                'context': 'Counting, pairs',
                'examples': [
                    'šinā GÚ - "two talents"',
                    'šanîš - "secondly"'
                ],
                'source': 'CAD Š/3 pp.23-30',
                'secondary_sources': ['CDA p.375'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שְׁנַיִם šenayim'},
                'notes': 'Dual/pair designation'
            },
        }

        # ============================================================
        # CATEGORY 6: PERSONNEL AND OCCUPATIONS
        # ============================================================
        personnel_terms = {
            'ṭupšarru': {
                'term': 'ṭupšarru',
                'meaning': 'scribe, tablet-writer',
                'root': 'ṬPP + ŠṬR',
                'usage': 'Occupation designation',
                'context': 'Administrative personnel',
                'examples': [
                    'ṭupšarru ša ēkalli - "palace scribe"',
                    'mār ṭupšarri - "scribe\'s apprentice"'
                ],
                'source': 'CAD Ṭ pp.148-151',
                'secondary_sources': ['CDA p.405'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Compound: tablet + writing'
            },
            'šaknu': {
                'term': 'šaknu',
                'meaning': 'governor, prefect, overseer',
                'root': 'ŠKN',
                'usage': 'Administrative title',
                'context': 'Regional administration',
                'examples': [
                    'šakin māti - "governor of the land"',
                    'bēl pīḫāti - "district governor"'
                ],
                'source': 'CAD Š/1 pp.156-165',
                'secondary_sources': ['CDA p.346'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'High administrative office'
            },
            'awīlu': {
                'term': 'awīlu',
                'meaning': 'man, person, gentleman, free citizen',
                'root': 'WL',
                'usage': 'Personnel designation',
                'context': 'Worker lists, legal texts',
                'examples': [
                    'awīlum šū - "that man"',
                    'awīlī - "men, people"'
                ],
                'source': 'CAD A/2 pp.48-57',
                'secondary_sources': ['CDA p.29'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Basic personnel term'
            },
            'amtu': {
                'term': 'amtu',
                'meaning': 'female slave, maidservant',
                'root': 'ʾM',
                'usage': 'Personnel designation',
                'context': 'Worker lists, household texts',
                'examples': [
                    'amtum ša bītim - "maidservant of the house"',
                    'amāti - "female servants"'
                ],
                'source': 'CAD A/2 pp.79-83',
                'secondary_sources': ['CDA p.16'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אָמָה ʾāmâ'},
                'notes': 'Female workforce designation'
            },
            'wardu': {
                'term': 'wardu',
                'meaning': 'male slave, servant, subject',
                'root': 'WRD',
                'usage': 'Personnel designation',
                'context': 'Worker lists, legal texts',
                'examples': [
                    'warad šarri - "servant of the king"',
                    'wardī - "my servants"'
                ],
                'source': 'CAD A/2 pp.250-260 (as ardu)',
                'secondary_sources': ['CDA p.26'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Male workforce designation'
            },
            'nuḫatimmu': {
                'term': 'nuḫatimmu',
                'meaning': 'cook, baker',
                'root': 'NḪT',
                'usage': 'Occupation designation',
                'context': 'Temple/palace personnel',
                'examples': [
                    'bēl nuḫatimmī - "chief baker"',
                    'nuḫatimmūtu - "bakery"'
                ],
                'source': 'CAD N/2 pp.318-321',
                'secondary_sources': ['CDA p.253'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Food preparation specialist'
            },
            'nappāḫu': {
                'term': 'nappāḫu',
                'meaning': 'smith, metalworker',
                'root': 'NPḪ',
                'usage': 'Occupation designation',
                'context': 'Craft specialists',
                'examples': [
                    'nappāḫ siparri - "bronze smith"',
                    'bīt nappāḫi - "smithy"'
                ],
                'source': 'CAD N/1 pp.302-306',
                'secondary_sources': ['CDA p.234'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Metal craftsman'
            },
            'išparu': {
                'term': 'išparu',
                'meaning': 'weaver',
                'root': 'SPR',
                'usage': 'Occupation designation',
                'context': 'Textile production',
                'examples': [
                    'išpar birmi - "multicolored weaver"',
                    'bīt išpari - "weaving house"'
                ],
                'source': 'CAD I/J pp.257-260',
                'secondary_sources': ['CDA p.134'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Textile specialist'
            },
            'māru': {
                'term': 'māru',
                'meaning': 'son, child, member of group',
                'root': 'MR',
                'usage': 'Kinship/group designation',
                'context': 'Personnel lists, guilds',
                'examples': [
                    'mārē āli - "citizens (sons of the city)"',
                    'mār ummâni - "craftsman (son of expert)"'
                ],
                'source': 'CAD M/1 pp.294-317',
                'secondary_sources': ['CDA p.198'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'בֵּן bēn (different root)'},
                'notes': 'Extended kinship/guild term'
            },
            'ummânu': {
                'term': 'ummânu',
                'meaning': 'craftsman, expert, artisan, scholar',
                'root': 'ʾMN',
                'usage': 'Skilled worker designation',
                'context': 'Craft specialists, scholars',
                'examples': [
                    'ummân ṭupšarrūti - "scribal expert"',
                    'ummānū - "craftsmen, experts"'
                ],
                'source': 'CAD U pp.102-107',
                'secondary_sources': ['CDA p.418'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אֻמָּן ʾummān'},
                'notes': 'Skilled labor designation'
            },
            'rab': {
                'term': 'rab',
                'meaning': 'chief, head, overseer, great one',
                'root': 'RB',
                'usage': 'Title prefix for supervisors',
                'context': 'Administrative hierarchy',
                'examples': [
                    'rab nuḫatimmī - "chief baker"',
                    'rab māḫiṣi - "chief brewer"',
                    'rabûtu - "officials"'
                ],
                'source': 'CAD R pp.22-36',
                'secondary_sources': ['CDA p.288'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'רַב rab'},
                'notes': 'Common supervisor title prefix'
            },
        }

        # ============================================================
        # CATEGORY 7: TEMPLE AND RELIGIOUS
        # ============================================================
        temple_terms = {
            'ilu': {
                'term': 'ilu',
                'meaning': 'god, deity',
                'root': 'ʾL',
                'usage': 'Divine reference',
                'context': 'Temple texts, offerings',
                'examples': [
                    'ilāni rabûti - "great gods"',
                    'ana ili - "to the god"'
                ],
                'source': 'CAD I/J pp.91-105',
                'secondary_sources': ['CDA p.126'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אֵל ʾēl', 'Ugaritic': 'il'},
                'notes': 'Common Semitic god term'
            },
            'ēkallu': {
                'term': 'ēkallu',
                'meaning': 'palace, temple-palace complex',
                'root': 'HKL',
                'usage': 'Administrative center reference',
                'context': 'Palace administration',
                'examples': [
                    'ša ēkalli - "of the palace"',
                    'ana ēkalli - "to the palace"'
                ],
                'source': 'CAD E pp.52-62',
                'secondary_sources': ['CDA p.67'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'הֵיכָל hêkāl', 'Sumerian': 'é-gal'},
                'notes': 'Administrative center'
            },
            'bītu': {
                'term': 'bītu',
                'meaning': 'house, temple, household, estate',
                'root': 'BT',
                'usage': 'Temple/estate designation',
                'context': 'Temple administration',
                'examples': [
                    'bīt ili - "temple (house of god)"',
                    'ša bīti - "of the household"'
                ],
                'source': 'CAD B pp.282-298',
                'secondary_sources': ['CDA p.42'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'בַּיִת bayit'},
                'notes': 'Administrative unit'
            },
            'niqû': {
                'term': 'niqû',
                'meaning': 'offering, sacrifice',
                'root': 'NQ',
                'usage': 'Sacrificial offering',
                'context': 'Temple ritual',
                'examples': [
                    'niqê ilāni - "offerings to the gods"',
                    'ana niqê - "for sacrifice"'
                ],
                'source': 'CAD N/2 pp.249-257',
                'secondary_sources': ['CDA p.250'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Temple offering term'
            },
            'sattukku': {
                'term': 'sattukku',
                'meaning': 'regular offering, food offering',
                'root': 'STK',
                'usage': 'Regular temple offerings',
                'context': 'Temple supply lists',
                'examples': [
                    'sattukki ilāni - "regular offerings of the gods"',
                    'sattuk ūmi - "daily offering"'
                ],
                'source': 'CAD S pp.198-204',
                'secondary_sources': ['CDA p.321'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Regular/periodic offering'
            },
            'šangû': {
                'term': 'šangû',
                'meaning': 'chief priest, temple administrator',
                'root': 'ŠNG',
                'usage': 'Temple administrator title',
                'context': 'Temple hierarchy',
                'examples': [
                    'šangû ša Marduk - "priest of Marduk"',
                    'šangûtu - "priesthood"'
                ],
                'source': 'CAD Š/1 pp.375-381',
                'secondary_sources': ['CDA p.353'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'High temple official'
            },
            'gināʾu': {
                'term': 'gināʾu',
                'meaning': 'regular offering, customary delivery',
                'root': 'GN',
                'usage': 'Periodic temple deliveries',
                'context': 'Temple supply schedules',
                'examples': [
                    'ginâ ša šatti - "annual regular delivery"',
                    'ginê ilāni - "regular offerings of the gods"'
                ],
                'source': 'CAD G pp.72-75',
                'secondary_sources': ['CDA p.92'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Scheduled/recurring delivery'
            },
            'kurummatu': {
                'term': 'kurummatu',
                'meaning': 'food ration, sustenance allocation',
                'root': 'KRM',
                'usage': 'Temple/palace rations',
                'context': 'Personnel feeding',
                'examples': [
                    'kurummat ṣābī - "rations of the workers"',
                    'kurummat ilāni - "food offerings to gods"'
                ],
                'source': 'CAD K pp.567-573',
                'secondary_sources': ['CDA p.169'],
                'category': 'temple',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Sustenance allocation term'
            },
        }

        # ============================================================
        # CATEGORY 8: TRADE AND COMMERCE
        # ============================================================
        trade_terms = {
            'tamkāru': {
                'term': 'tamkāru',
                'meaning': 'merchant, trader, commercial agent',
                'root': 'MKR',
                'usage': 'Commercial occupation',
                'context': 'Trade texts, merchant records',
                'examples': [
                    'tamkār āli - "city merchant"',
                    'tamkārūtu - "trade, commerce"'
                ],
                'source': 'CAD T pp.125-130',
                'secondary_sources': ['CDA p.393'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'סֹחֵר sōḥēr (different root)'},
                'notes': 'Primary merchant term'
            },
            'šīmu': {
                'term': 'šīmu',
                'meaning': 'price, purchase price, value',
                'root': 'ŠM',
                'usage': 'Commercial value notation',
                'context': 'Trade, sale records',
                'examples': [
                    'šīm eqli - "price of the field"',
                    'ana šīmim - "for purchase"'
                ],
                'source': 'CAD Š/3 pp.8-16',
                'secondary_sources': ['CDA p.374'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Price/value term'
            },
            'šāmu': {
                'term': 'šāmu',
                'meaning': 'to buy, purchase',
                'root': 'ŠM',
                'usage': 'Commercial transaction',
                'context': 'Sale documents',
                'examples': [
                    'išāmu - "he bought"',
                    'šīmum - "purchase"'
                ],
                'source': 'CAD Š/1 pp.297-307',
                'secondary_sources': ['CDA p.350'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Purchase verb'
            },
            'hubullu': {
                'term': 'hubullu',
                'meaning': 'debt, obligation, loan',
                'root': 'ḪBL',
                'usage': 'Commercial debt notation',
                'context': 'Loan documents',
                'examples': [
                    'hubullum ša PN - "debt of PN"',
                    'hubulla - "debts"'
                ],
                'source': 'CAD Ḫ pp.219-222',
                'secondary_sources': ['CDA p.116'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חֹבֶל ḥōbel'},
                'notes': 'Debt/loan terminology'
            },
            'šūkulu': {
                'term': 'šūkulu',
                'meaning': 'to supply food, deliver, feed',
                'root': 'ʾKL (causative)',
                'usage': 'Supply/delivery',
                'context': 'Commodity distribution',
                'examples': [
                    'ušākil - "he supplied"',
                    'šūkultu - "supply, food delivery"'
                ],
                'source': 'CAD Š/3 pp.209-212',
                'secondary_sources': ['CDA p.381'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Supply/delivery verb'
            },
            'elēpu': {
                'term': 'elēpu',
                'meaning': 'ship, boat',
                'root': 'ʾLP',
                'usage': 'Transport vessel',
                'context': 'Maritime trade',
                'examples': [
                    'elep tamkāri - "merchant ship"',
                    'eleppu - "boat, ship"'
                ],
                'source': 'CAD E pp.93-101',
                'secondary_sources': ['CDA p.68'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Maritime transport - relevant to Aegean trade'
            },
            'kāru': {
                'term': 'kāru',
                'meaning': 'harbor, quay, trading station',
                'root': 'KR',
                'usage': 'Trade location',
                'context': 'Maritime commerce',
                'examples': [
                    'kār Telmun - "harbor of Dilmun"',
                    'bīt kāri - "harbor facility"'
                ],
                'source': 'CAD K pp.235-241',
                'secondary_sources': ['CDA p.147'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Harbor/trading post'
            },
            'ṣibtu': {
                'term': 'ṣibtu',
                'meaning': 'interest (on loan), increase',
                'root': 'ṢBT',
                'usage': 'Loan interest',
                'context': 'Financial texts',
                'examples': [
                    'ana ṣibtim - "at interest"',
                    'ṣibit kaspim - "interest on silver"'
                ],
                'source': 'CAD Ṣ pp.154-158',
                'secondary_sources': ['CDA p.327'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Financial term for interest'
            },
        }

        # ============================================================
        # CATEGORY 9: MEASUREMENTS AND UNITS
        # ============================================================
        measurement_terms = {
            'biltu': {
                'term': 'biltu',
                'meaning': 'talent (unit of weight ~30kg), load, tribute',
                'root': 'BL (to carry)',
                'usage': 'Large weight measure',
                'context': 'Commodity weights, tribute',
                'examples': [
                    '1 GÚ kaspim - "1 talent of silver"',
                    'bilat šadî - "mountain tribute"'
                ],
                'source': 'CAD B pp.229-235',
                'secondary_sources': ['CDA p.40'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Standard large weight unit'
            },
            'mana': {
                'term': 'mana',
                'meaning': 'mina (weight unit ~500g)',
                'root': 'MN',
                'usage': 'Standard weight measure',
                'context': 'Metal weights, commodities',
                'examples': [
                    '1 MA.NA kaspim - "1 mina of silver"',
                    '60 šiqil = 1 manû'
                ],
                'source': 'CAD M/1 pp.196-200',
                'secondary_sources': ['CDA p.193'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'מָנֶה māneh'},
                'notes': '1/60 of talent'
            },
            'šiqlu': {
                'term': 'šiqlu',
                'meaning': 'shekel (weight unit ~8g)',
                'root': 'ŠQL',
                'usage': 'Small weight measure',
                'context': 'Precious metals, small quantities',
                'examples': [
                    '1 GÍN kaspim - "1 shekel of silver"',
                    '60 šiqil = 1 manû'
                ],
                'source': 'CAD Š/2 pp.440-448',
                'secondary_sources': ['CDA p.377'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שֶׁקֶל šeqel'},
                'notes': 'Standard small weight'
            },
            'kurru': {
                'term': 'kurru',
                'meaning': 'gur/kor (capacity ~300L), large measure',
                'root': 'KR',
                'usage': 'Grain capacity measure',
                'context': 'Grain quantities',
                'examples': [
                    '1 GUR še ī - "1 kor of barley"',
                    '5 BÁN = 1 kurru'
                ],
                'source': 'CAD K pp.563-567',
                'secondary_sources': ['CDA p.169'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'כֹּר kōr'},
                'notes': 'Large capacity unit'
            },
            'qû': {
                'term': 'qû',
                'meaning': 'qa (capacity ~1L), small measure',
                'root': 'Q',
                'usage': 'Small capacity measure',
                'context': 'Small liquid/grain quantities',
                'examples': [
                    '1 SÌLA šamni - "1 qa of oil"',
                    '10 qû = 1 sūtu'
                ],
                'source': 'CAD Q pp.276-282',
                'secondary_sources': ['CDA p.288'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Basic small capacity'
            },
            'sūtu': {
                'term': 'sūtu',
                'meaning': 'seah (capacity ~10L)',
                'root': 'ST',
                'usage': 'Medium capacity measure',
                'context': 'Grain, liquids',
                'examples': [
                    '1 BÁN še ī - "1 seah of barley"',
                    '6 sūtu = 1 kurru'
                ],
                'source': 'CAD S pp.418-424',
                'secondary_sources': ['CDA p.339'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'סְאָה seʾâ'},
                'notes': 'Intermediate capacity'
            },
            'ammatu': {
                'term': 'ammatu',
                'meaning': 'cubit (length ~50cm), forearm',
                'root': 'ʾM',
                'usage': 'Length measure',
                'context': 'Construction, textiles',
                'examples': [
                    '10 KÙŠ - "10 cubits"',
                    'ammatum rabītu - "large cubit"'
                ],
                'source': 'CAD A/2 pp.72-76',
                'secondary_sources': ['CDA p.16'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אַמָּה ʾammâ'},
                'notes': 'Standard length unit'
            },
            'imēru': {
                'term': 'imēru',
                'meaning': 'homer (capacity ~100L), donkey-load',
                'root': 'ḪMR',
                'usage': 'Large capacity/transport unit',
                'context': 'Transport quantities',
                'examples': [
                    'imēr še ī - "donkey-load of barley"',
                    '1 ANŠE = 1 imēru'
                ],
                'source': 'CAD I/J pp.118-121',
                'secondary_sources': ['CDA p.128'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חֹמֶר ḥōmer'},
                'notes': 'Based on donkey transport capacity'
            },
        }

        # ============================================================
        # CATEGORY 10: TIME AND CALENDRICAL
        # ============================================================
        time_terms = {
            'ūmu': {
                'term': 'ūmu',
                'meaning': 'day, time',
                'root': 'WM',
                'usage': 'Date notation',
                'context': 'Administrative dating',
                'examples': [
                    'UD.1.KAM - "day 1"',
                    'ūm išten - "first day"'
                ],
                'source': 'CAD U pp.135-156',
                'secondary_sources': ['CDA p.422'],
                'category': 'time',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'יוֹם yôm'},
                'notes': 'Basic time unit'
            },
            'arḫu': {
                'term': 'arḫu',
                'meaning': 'month',
                'root': 'WRḪ',
                'usage': 'Calendar notation',
                'context': 'Dating, schedules',
                'examples': [
                    'ITI.1.KAM - "month 1"',
                    'arḫu Nisannu - "month of Nisan"'
                ],
                'source': 'CAD A/2 pp.264-269',
                'secondary_sources': ['CDA p.26'],
                'category': 'time',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'יֶרַח yeraḥ'},
                'notes': 'Monthly calendar unit'
            },
            'šattu': {
                'term': 'šattu',
                'meaning': 'year',
                'root': 'ŠT',
                'usage': 'Annual dating, schedules',
                'context': 'Dating, annual accounts',
                'examples': [
                    'šatti 1.KAM - "year 1"',
                    'ša šattim - "of the year"',
                    'šattišam - "yearly, annually"'
                ],
                'source': 'CAD Š/2 pp.206-224',
                'secondary_sources': ['CDA p.366'],
                'category': 'time',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Annual accounting period'
            },
            'palû': {
                'term': 'palû',
                'meaning': 'reign, regnal year, turn',
                'root': 'PL',
                'usage': 'Royal dating formula',
                'context': 'Historical dating',
                'examples': [
                    'palê šarri - "reign of the king"',
                    'ina palêšu - "during his reign"'
                ],
                'source': 'CAD P pp.71-78',
                'secondary_sources': ['CDA p.257'],
                'category': 'time',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Royal chronological term'
            },
        }

        # ============================================================
        # CATEGORY 11: ADDITIONAL ADMINISTRATIVE TERMS
        # ============================================================
        additional_terms = {
            'šulpu': {
                'term': 'šulpu',
                'meaning': 'ear of grain, grain spike',
                'root': 'ŠLP',
                'usage': 'Agricultural commodity',
                'context': 'Harvest accounting',
                'examples': [
                    'šulpī ša eqlim - "grain ears of the field"'
                ],
                'source': 'CAD Š/3 pp.252-254',
                'secondary_sources': ['CDA p.384'],
                'category': 'commodity',
                'confidence': 'MEDIUM',
                'cognates': {},
                'notes': 'Agricultural produce term'
            },
            'riksu': {
                'term': 'riksu',
                'meaning': 'binding, agreement, contract, treaty',
                'root': 'RKS',
                'usage': 'Legal/administrative binding',
                'context': 'Contracts, obligations',
                'examples': [
                    'riksu ša ilāni - "treaty of the gods"',
                    'rikis libbi - "agreement"'
                ],
                'source': 'CAD R pp.353-361',
                'secondary_sources': ['CDA p.302'],
                'category': 'trade',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Legal document term'
            },
            'ṣuḫāru': {
                'term': 'ṣuḫāru',
                'meaning': 'young man, servant boy, assistant',
                'root': 'ṢḪR',
                'usage': 'Personnel designation',
                'context': 'Junior workforce',
                'examples': [
                    'ṣuḫārē - "servants, assistants"',
                    'ṣuḫār ēkalli - "palace servants"'
                ],
                'source': 'CAD Ṣ pp.235-240',
                'secondary_sources': ['CDA p.332'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Junior personnel term'
            },
            'alpum': {
                'term': 'alpum',
                'meaning': 'ox, cattle, bovine',
                'root': 'ʾLP',
                'usage': 'Livestock commodity',
                'context': 'Animal husbandry, offerings',
                'examples': [
                    '1 GU₄ - "1 ox"',
                    'alpū ša naškutim - "cattle of the herd"'
                ],
                'source': 'CAD A/1 pp.355-366',
                'secondary_sources': ['CDA p.14'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אֶלֶף ʾelep'},
                'notes': 'Major livestock; compare Linear A cattle ideogram'
            },
            'immeru': {
                'term': 'immeru',
                'meaning': 'sheep, ram',
                'root': 'MR',
                'usage': 'Livestock commodity',
                'context': 'Animal husbandry, offerings',
                'examples': [
                    '1 UDU - "1 sheep"',
                    'immerū rabûtum - "large sheep"'
                ],
                'source': 'CAD I/J pp.121-128',
                'secondary_sources': ['CDA p.128'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Major livestock; compare Linear A sheep ideogram'
            },
            'enzu': {
                'term': 'enzu',
                'meaning': 'goat, she-goat',
                'root': 'NZ',
                'usage': 'Livestock commodity',
                'context': 'Animal husbandry',
                'examples': [
                    '1 ÙZ - "1 goat"',
                    'enzū - "goats"'
                ],
                'source': 'CAD E pp.172-175',
                'secondary_sources': ['CDA p.73'],
                'category': 'commodity',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'עֵז ʿēz'},
                'notes': 'Goat herd management'
            },
            'šahû': {
                'term': 'šahû',
                'meaning': 'pig, swine',
                'root': 'ŠH',
                'usage': 'Livestock (less common)',
                'context': 'Animal husbandry',
                'examples': [
                    'šahû - "pig"',
                    'šahû šamnu - "fattened pig"'
                ],
                'source': 'CAD Š/1 pp.100-103',
                'secondary_sources': ['CDA p.344'],
                'category': 'commodity',
                'confidence': 'MEDIUM',
                'cognates': {},
                'notes': 'Less common livestock'
            },
            'eqlu': {
                'term': 'eqlu',
                'meaning': 'field, arable land, plot',
                'root': 'QLL',
                'usage': 'Land measurement/allocation',
                'context': 'Agricultural administration',
                'examples': [
                    'eqel PN - "field of PN"',
                    '1 IKU eqlim - "1 iku of field"'
                ],
                'source': 'CAD E pp.251-260',
                'secondary_sources': ['CDA p.74'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Land allocation term'
            },
            'iku': {
                'term': 'iku',
                'meaning': 'iku (area ~3600 sq m), field unit',
                'root': 'K',
                'usage': 'Land area measure',
                'context': 'Field allocation',
                'examples': [
                    '1 IKU A.ŠÀ - "1 iku of field"',
                    '100 iku = 1 būru'
                ],
                'source': 'CAD I/J pp.69-74',
                'secondary_sources': ['CDA p.125'],
                'category': 'measurement',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Standard area unit'
            },
            'bēlu': {
                'term': 'bēlu',
                'meaning': 'lord, master, owner, proprietor',
                'root': 'BʾL',
                'usage': 'Title/ownership designation',
                'context': 'Hierarchy, ownership',
                'examples': [
                    'bēl bīti - "master of the house"',
                    'bēl pīḫāti - "district governor"'
                ],
                'source': 'CAD B pp.191-206',
                'secondary_sources': ['CDA p.36'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'בַּעַל baʿal', 'Ugaritic': 'bʿl'},
                'notes': 'Common Semitic lord/owner title'
            },
            'šarru': {
                'term': 'šarru',
                'meaning': 'king, ruler',
                'root': 'ŠR',
                'usage': 'Royal title',
                'context': 'Royal administration',
                'examples': [
                    'šar māt Aššur - "king of Assyria"',
                    'ana šarri - "to the king"'
                ],
                'source': 'CAD Š/2 pp.68-93',
                'secondary_sources': ['CDA p.360'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Royal designation'
            },
            'šarratu': {
                'term': 'šarratu',
                'meaning': 'queen',
                'root': 'ŠR',
                'usage': 'Royal title (feminine)',
                'context': 'Royal administration',
                'examples': [
                    'šarratum - "the queen"',
                    'bīt šarrāti - "queen\'s household"'
                ],
                'source': 'CAD Š/2 pp.93-97',
                'secondary_sources': ['CDA p.360'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {},
                'notes': 'Royal female title'
            },
            'ummum': {
                'term': 'ummum',
                'meaning': 'mother',
                'root': 'ʾM',
                'usage': 'Kinship term',
                'context': 'Personnel, genealogy',
                'examples': [
                    'ummi - "my mother"',
                    'ummum rabītum - "the great mother"'
                ],
                'source': 'CAD U pp.107-115',
                'secondary_sources': ['CDA p.419'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אֵם ʾēm'},
                'notes': 'Basic kinship term'
            },
            'abum': {
                'term': 'abum',
                'meaning': 'father',
                'root': 'ʾB',
                'usage': 'Kinship term',
                'context': 'Personnel, genealogy',
                'examples': [
                    'abī - "my father"',
                    'bīt abi - "father\'s house"'
                ],
                'source': 'CAD A/1 pp.67-77',
                'secondary_sources': ['CDA p.3'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אָב ʾāb'},
                'notes': 'Basic kinship term'
            },
            'aḫum': {
                'term': 'aḫum',
                'meaning': 'brother',
                'root': 'ʾḪ',
                'usage': 'Kinship term',
                'context': 'Personnel, genealogy',
                'examples': [
                    'aḫī - "my brother"',
                    'aḫḫū - "brothers"'
                ],
                'source': 'CAD A/1 pp.193-205',
                'secondary_sources': ['CDA p.8'],
                'category': 'personnel',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אָח ʾāḥ'},
                'notes': 'Kinship; also metaphoric for allies'
            },
            'selāšu': {
                'term': 'selāšu',
                'meaning': 'three',
                'root': 'ŠLŠ',
                'usage': 'Basic numeral',
                'context': 'Counting',
                'examples': [
                    'šalāš - "three"',
                    'šalšī - "third"'
                ],
                'source': 'CAD Š/1 pp.252-260',
                'secondary_sources': ['CDA p.349'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'שָׁלֹשׁ šālōš'},
                'notes': 'Numeral three'
            },
            'erbe': {
                'term': 'erbe',
                'meaning': 'four',
                'root': 'RBʾ',
                'usage': 'Basic numeral',
                'context': 'Counting',
                'examples': [
                    'erbe - "four"',
                    'rebû - "fourth"'
                ],
                'source': 'CAD E pp.259-262',
                'secondary_sources': ['CDA p.75'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'אַרְבַּע ʾarbaʿ'},
                'notes': 'Numeral four'
            },
            'ḫamšu': {
                'term': 'ḫamšu',
                'meaning': 'five',
                'root': 'ḪMŠ',
                'usage': 'Basic numeral',
                'context': 'Counting',
                'examples': [
                    'ḫamšu - "five"',
                    'ḫamšī - "fifth"'
                ],
                'source': 'CAD Ḫ pp.67-70',
                'secondary_sources': ['CDA p.103'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'חָמֵשׁ ḥāmēš'},
                'notes': 'Numeral five'
            },
            'ešru': {
                'term': 'ešru',
                'meaning': 'ten',
                'root': 'ʾŠR',
                'usage': 'Basic numeral',
                'context': 'Counting',
                'examples': [
                    'ešer - "ten"',
                    'ešrū - "tens, decades"'
                ],
                'source': 'CAD E pp.364-369',
                'secondary_sources': ['CDA p.81'],
                'category': 'counting',
                'confidence': 'HIGH',
                'cognates': {'Hebrew': 'עֶשֶׂר ʿeśer'},
                'notes': 'Numeral ten'
            },
        }

        # Combine all categories
        all_terms = {}
        all_terms.update(totaling_terms)
        all_terms.update(deficit_terms)
        all_terms.update(allocation_terms)
        all_terms.update(commodity_terms)
        all_terms.update(counting_terms)
        all_terms.update(personnel_terms)
        all_terms.update(temple_terms)
        all_terms.update(trade_terms)
        all_terms.update(measurement_terms)
        all_terms.update(time_terms)
        all_terms.update(additional_terms)

        self.vocabulary = all_terms
        return len(all_terms)

    def save_vocabulary(self, filepath: Optional[Path] = None) -> Path:
        """Save vocabulary to JSON file."""
        if filepath is None:
            filepath = OUTPUT_FILE

        output = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'generator': 'ORACC Connector (Linear A Decipherment Project)',
                'version': '1.0.0',
                'total_terms': len(self.vocabulary),
                'sources': [
                    'CAD (Chicago Assyrian Dictionary)',
                    'CDA (Concise Dictionary of Akkadian)',
                    'ORACC (Open Richly Annotated Cuneiform Corpus)',
                    'SAA (State Archives of Assyria)',
                ],
                'categories': {
                    'totaling': 'Terms for totals, sums, quantities',
                    'deficit': 'Terms for shortages, losses, deficits',
                    'allocation': 'Terms for distribution, giving, receiving',
                    'commodity': 'Goods: oil, wine, grain, metals, textiles',
                    'counting': 'Counting, recording, numerals',
                    'personnel': 'Occupations, workers, titles',
                    'temple': 'Religious and temple administration',
                    'trade': 'Commerce, merchants, prices',
                    'measurement': 'Units of weight, capacity, length',
                    'time': 'Days, months, years, dating',
                },
                'usage_note': 'For comparative analysis with Linear A administrative texts',
                'linear_a_relevance': 'Terms selected for parallels with Bronze Age Aegean administration',
            },
            'terms': self.vocabulary,
        }

        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        self.log(f"Saved {len(self.vocabulary)} terms to {filepath}")
        return filepath

    def load_vocabulary(self, filepath: Optional[Path] = None) -> int:
        """Load vocabulary from JSON file."""
        if filepath is None:
            filepath = OUTPUT_FILE

        if not filepath.exists():
            self.log(f"File not found: {filepath}", "warning")
            return 0

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.vocabulary = data.get('terms', {})
        return len(self.vocabulary)

    def query(self, term: str, exact: bool = False) -> List[Dict]:
        """Query vocabulary for a term."""
        results = []
        term_lower = term.lower()

        for akk_term, data in self.vocabulary.items():
            # Exact match
            if exact and term_lower == akk_term.lower():
                results.append(data)
                continue

            # Fuzzy matching
            if not exact:
                # Term match
                if term_lower in akk_term.lower():
                    results.append(data)
                    continue

                # Root match
                root = data.get('root', '').upper()
                if term.upper() in root:
                    results.append(data)
                    continue

                # Meaning match
                meaning = data.get('meaning', '').lower()
                if term_lower in meaning:
                    results.append(data)
                    continue

        return results

    def get_category(self, category: str) -> List[Dict]:
        """Get all terms in a category."""
        return [
            data for data in self.vocabulary.values()
            if data.get('category', '').lower() == category.lower()
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """Get vocabulary statistics."""
        categories = {}
        confidence_levels = {}
        sources = set()

        for term, data in self.vocabulary.items():
            # Count categories
            cat = data.get('category', 'unknown')
            categories[cat] = categories.get(cat, 0) + 1

            # Count confidence levels
            conf = data.get('confidence', 'unknown')
            confidence_levels[conf] = confidence_levels.get(conf, 0) + 1

            # Collect sources
            sources.add(data.get('source', ''))
            for s in data.get('secondary_sources', []):
                sources.add(s)

        return {
            'total_terms': len(self.vocabulary),
            'categories': categories,
            'confidence_levels': confidence_levels,
            'unique_sources': len(sources) - 1,  # Subtract empty string
        }


def print_term(term_data: Dict, verbose: bool = False):
    """Pretty print a term."""
    print(f"\n  {term_data['term']}")
    print(f"    Meaning: {term_data['meaning']}")
    print(f"    Root: {term_data['root']}")
    print(f"    Category: {term_data.get('category', 'N/A')}")
    print(f"    Confidence: {term_data.get('confidence', 'N/A')}")

    if verbose:
        print(f"    Usage: {term_data.get('usage', 'N/A')}")
        print(f"    Context: {term_data.get('context', 'N/A')}")
        if term_data.get('examples'):
            print(f"    Examples:")
            for ex in term_data['examples'][:3]:
                print(f"      - {ex}")
        print(f"    Source: {term_data.get('source', 'N/A')}")
        if term_data.get('cognates'):
            print(f"    Cognates: {term_data['cognates']}")


def main():
    parser = argparse.ArgumentParser(
        description="ORACC Connector for Akkadian administrative vocabulary"
    )
    parser.add_argument(
        '--fetch',
        action='store_true',
        help='Attempt to fetch vocabulary from ORACC (requires network)'
    )
    parser.add_argument(
        '--build-static',
        action='store_true',
        help='Build comprehensive static dictionary from published sources'
    )
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Query vocabulary for a term'
    )
    parser.add_argument(
        '--exact',
        action='store_true',
        help='Use exact matching for queries'
    )
    parser.add_argument(
        '--category', '-c',
        type=str,
        help='Get all terms in a category'
    )
    parser.add_argument(
        '--list-categories',
        action='store_true',
        help='List available categories'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show vocabulary statistics'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Skip network operations'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: data/comparative/akkadian_oracc.json)'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("ORACC CONNECTOR - Akkadian Administrative Vocabulary")
    print("Linear A Decipherment Project (OPERATION MINOS III)")
    print("=" * 70)

    connector = ORACCConnector(verbose=args.verbose, offline=args.offline)
    output_path = Path(args.output) if args.output else OUTPUT_FILE

    if args.build_static:
        print("\nBuilding static dictionary from CAD/CDA sources...")
        count = connector.build_static_dictionary()
        filepath = connector.save_vocabulary(output_path)
        print(f"\nBuilt {count} terms")
        print(f"Saved to: {filepath}")

        # Show stats
        stats = connector.get_statistics()
        print(f"\nCategories: {len(stats['categories'])}")
        for cat, n in sorted(stats['categories'].items()):
            print(f"  {cat}: {n}")

    elif args.fetch:
        print("\nAttempting to fetch from ORACC...")
        print("(Note: Falls back to static dictionary if network unavailable)")

        # Try ORACC fetch
        count = connector.fetch_all_glossaries()

        if count == 0:
            print("ORACC unavailable, building static dictionary...")
            count = connector.build_static_dictionary()

        filepath = connector.save_vocabulary(output_path)
        print(f"\nFetched/built {count} terms")
        print(f"Saved to: {filepath}")

    elif args.query:
        # Load existing vocabulary
        loaded = connector.load_vocabulary(output_path)
        if loaded == 0:
            print("No vocabulary file found. Run --build-static first.")
            return 1

        results = connector.query(args.query, exact=args.exact)
        print(f"\nQuery: '{args.query}' ({len(results)} matches)")

        for r in results:
            print_term(r, args.verbose)

    elif args.category:
        loaded = connector.load_vocabulary(output_path)
        if loaded == 0:
            print("No vocabulary file found. Run --build-static first.")
            return 1

        results = connector.get_category(args.category)
        print(f"\nCategory: {args.category} ({len(results)} terms)")

        for r in results:
            print_term(r, args.verbose)

    elif args.list_categories:
        loaded = connector.load_vocabulary(output_path)
        if loaded == 0:
            print("No vocabulary file found. Run --build-static first.")
            return 1

        stats = connector.get_statistics()
        print("\nAvailable categories:")
        for cat, n in sorted(stats['categories'].items()):
            print(f"  {cat}: {n} terms")

    elif args.stats:
        loaded = connector.load_vocabulary(output_path)
        if loaded == 0:
            print("No vocabulary file found. Run --build-static first.")
            return 1

        stats = connector.get_statistics()
        print(f"\nVocabulary Statistics:")
        print(f"  Total terms: {stats['total_terms']}")
        print(f"  Categories: {len(stats['categories'])}")
        print(f"  Unique sources: {stats['unique_sources']}")
        print(f"\nBy category:")
        for cat, n in sorted(stats['categories'].items()):
            print(f"  {cat}: {n}")
        print(f"\nBy confidence:")
        for conf, n in sorted(stats['confidence_levels'].items()):
            print(f"  {conf}: {n}")

    else:
        print("\nUsage:")
        print("  --build-static    Build vocabulary from CAD/CDA sources")
        print("  --fetch           Attempt ORACC fetch (with static fallback)")
        print("  --query TERM      Search for a term")
        print("  --category CAT    Get terms in a category")
        print("  --stats           Show vocabulary statistics")
        print("\nExamples:")
        print("  python tools/oracc_connector.py --build-static")
        print("  python tools/oracc_connector.py --query kull")
        print("  python tools/oracc_connector.py --category totaling -v")
        print("  python tools/oracc_connector.py --stats")

    return 0


if __name__ == '__main__':
    sys.exit(main())
