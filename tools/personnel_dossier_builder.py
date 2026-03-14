#!/usr/bin/env python3
"""
Personnel Dossier Builder — Cross-Tablet Name Intelligence

For each of 111 profiled personal names, builds a comprehensive administrative
dossier by cross-referencing the corpus, onomastic analysis, and name profiles.

Each dossier includes:
  {name, tablets, roles, commodities, quantities, co_occurring_names,
   sites, scribes, administrative_tier}

Usage:
    python3 tools/personnel_dossier_builder.py --all
    python3 tools/personnel_dossier_builder.py --name A-DU
    python3 tools/personnel_dossier_builder.py --top 20
    python3 tools/personnel_dossier_builder.py --cross-tablet
    python3 tools/personnel_dossier_builder.py --all --output data/personnel_dossiers.json

Attribution:
    Part of Linear A Decipherment Project
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
NAMES_FILE = DATA_DIR / "personal_names_comprehensive.json"
ONOMASTIC_FILE = DATA_DIR / "onomastic_analysis.json"
READINESS_FILE = DATA_DIR / "reading_readiness.json"


# ---------------------------------------------------------------------------
# Known commodity logograms (reused from reading_readiness_scorer.py)
# ---------------------------------------------------------------------------
COMMODITY_LOGOGRAMS: Set[str] = {
    "GRA",
    "VIN",
    "OLE",
    "OLIV",
    "FIC",
    "FAR",
    "CYP",
    "OVI",
    "CAP",
    "SUS",
    "BOS",
    "VIR",
    "MUL",
    "TELA",
    "OLE+U",
    "OLE+A",
    "OLE+E",
    "OLE+KI",
    "OLE+MI",
    "OLE+TU",
    "OLE+DI",
    "VIN+A",
    "VIN+DU",
    "GRA+PA",
    "GRA+A",
    "GRA+QE",
}

# Base commodity stems for matching compound logograms
COMMODITY_BASES: Set[str] = {
    "GRA",
    "VIN",
    "OLE",
    "OLIV",
    "FIC",
    "FAR",
    "CYP",
    "OVI",
    "CAP",
    "SUS",
    "BOS",
    "VIR",
    "MUL",
    "TELA",
}

FRACTION_TOKENS: Set[str] = {
    "J",
    "E",
    "F",
    "K",
    "L",
    "1/2",
    "½",
    "¹⁄₂",
    "1/4",
    "¼",
    "¹⁄₄",
    "3/4",
    "¾",
    "³⁄₄",
    "1/3",
    "⅓",
    "¹⁄₃",
    "2/3",
    "⅔",
    "²⁄₃",
    "1/8",
    "⅛",
    "¹⁄₈",
    "3/8",
    "⅜",
    "³⁄₈",
    "¹⁄₁₆",
    "~¹⁄₆",
    "¹⁄₆",
}

# Administrative / function words — not personal names but tracked as co-occurring
ADMIN_TERMS: Set[str] = {
    "KU-RO",
    "KI-RO",
    "TE",
    "SA-RA₂",
    "SA-RA2",
    "A-DU",
    "DA-RE",
    "SI-RU-TE",
    "PO-TO-KU-RO",
    "PA-I-TO",
    "KU-DO-NI-JA",
}

# Structural / separator tokens to skip
SKIP_TOKENS: Set[str] = {"\n", "𐄁", "", " ", "—", ",", ".", "[", "]", "*"}


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------
@dataclass
class PersonnelDossier:
    """Complete administrative dossier for one profiled name."""

    name: str
    tablets: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    commodities: List[str] = field(default_factory=list)
    quantities: Dict[str, float] = field(default_factory=dict)
    total_quantity: float = 0.0
    co_occurring_names: List[str] = field(default_factory=list)
    sites: List[str] = field(default_factory=list)
    scribes: List[str] = field(default_factory=list)
    administrative_tier: str = "unranked"
    # Metadata from names file
    occurrences_in_names_file: int = 0
    best_hypothesis: str = ""
    name_type: str = ""
    gender: str = ""
    confidence: str = ""
    detection_reason: str = ""


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def is_number(token: str) -> bool:
    """Check if a token is a numeric quantity."""
    if token in FRACTION_TOKENS:
        return True
    stripped = token.replace(".", "").replace(",", "")
    if stripped.isdigit():
        return True
    # Match fraction-like patterns
    if re.match(r"^\d+[/]\d+$", token):
        return True
    return False


def is_logogram(token: str) -> bool:
    """Check if a token is a commodity logogram."""
    if token in COMMODITY_LOGOGRAMS:
        return True
    if "+" in token:
        base = token.split("+")[0]
        return base in COMMODITY_BASES
    return token in COMMODITY_BASES


def extract_site(tablet_id: str) -> str:
    """Extract site code from tablet ID (e.g. HT85a -> HT)."""
    match = re.match(r"^([A-Z]+)", tablet_id)
    return match.group(1) if match else "UNKNOWN"


def parse_number(token: str) -> float:
    """Parse a numeric token to a float value."""
    if token in FRACTION_TOKENS:
        fraction_map = {
            "J": 0.25,
            "E": 0.5,
            "F": 0.5,
            "K": 0.25,
            "L": 0.125,
            "½": 0.5,
            "¹⁄₂": 0.5,
            "1/2": 0.5,
            "¼": 0.25,
            "¹⁄₄": 0.25,
            "1/4": 0.25,
            "¾": 0.75,
            "³⁄₄": 0.75,
            "3/4": 0.75,
            "⅓": 0.333,
            "¹⁄₃": 0.333,
            "1/3": 0.333,
            "⅔": 0.667,
            "²⁄₃": 0.667,
            "2/3": 0.667,
            "⅛": 0.125,
            "¹⁄₈": 0.125,
            "1/8": 0.125,
            "⅜": 0.375,
            "³⁄₈": 0.375,
            "3/8": 0.375,
            "¹⁄₁₆": 0.0625,
            "~¹⁄₆": 0.167,
            "¹⁄₆": 0.167,
        }
        return fraction_map.get(token, 0.0)
    try:
        return float(token)
    except (ValueError, TypeError):
        return 0.0


def is_syllabic_word(token: str) -> bool:
    """Check if a token is a syllabic word (not number, logogram, or structural)."""
    if token in SKIP_TOKENS:
        return False
    if is_number(token):
        return False
    if is_logogram(token):
        return False
    if token.startswith('"'):
        return False
    return True


def normalize_name(name: str) -> str:
    """Normalize name for matching — uppercase, canonical subscripts."""
    n = name.upper().strip()
    # Normalize subscript variants: RA2 -> RA₂, PA3 -> PA₃
    n = re.sub(r"([A-Z])2\b", r"\g<1>₂", n)
    n = re.sub(r"([A-Z])3\b", r"\g<1>₃", n)
    return n


# ---------------------------------------------------------------------------
# Main builder class
# ---------------------------------------------------------------------------
class PersonnelDossierBuilder:
    """Builds comprehensive cross-tablet dossiers for profiled personal names."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus: Dict = {}
        self.inscriptions: Dict = {}
        self.names_data: Dict = {}
        self.onomastic_data: Dict = {}
        self.readiness_data: Dict = {}

        # Derived data
        self.profiled_names: Dict[str, Dict] = {}  # normalized_name -> name entry
        self.name_variants: Dict[str, str] = {}  # variant -> canonical name
        self.dossiers: Dict[str, PersonnelDossier] = {}

        # Corpus index: tablet_id -> parsed token info
        self.tablet_words: Dict[str, List[str]] = {}
        self.tablet_scribes: Dict[str, str] = {}
        self.tablet_sites: Dict[str, str] = {}

    def log(self, msg: str):
        if self.verbose:
            print(f"  [debug] {msg}")

    # -----------------------------------------------------------------------
    # Data loading
    # -----------------------------------------------------------------------
    def load_data(self) -> bool:
        """Load all required and optional data files."""
        # Corpus (required)
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded corpus: {len(self.inscriptions)} inscriptions")
        except Exception as e:
            print(f"ERROR: Cannot load corpus — {e}")
            return False

        # Personal names (required)
        try:
            with open(NAMES_FILE, "r", encoding="utf-8") as f:
                self.names_data = json.load(f)
            names_dict = self.names_data.get("names", {})
            print(f"Loaded personal names: {len(names_dict)} profiles")
        except Exception as e:
            print(f"ERROR: Cannot load personal names — {e}")
            return False

        # Onomastic analysis (optional)
        try:
            with open(ONOMASTIC_FILE, "r", encoding="utf-8") as f:
                self.onomastic_data = json.load(f)
            self.log("Loaded onomastic analysis")
        except FileNotFoundError:
            print("  Warning: onomastic_analysis.json not found (non-fatal)")
        except Exception as e:
            print(f"  Warning: Error loading onomastic data — {e}")

        # Reading readiness (optional)
        try:
            with open(READINESS_FILE, "r", encoding="utf-8") as f:
                self.readiness_data = json.load(f)
            self.log("Loaded reading readiness data")
        except FileNotFoundError:
            pass  # Non-fatal
        except Exception as e:
            print(f"  Warning: Error loading readiness data — {e}")

        self._build_indexes()
        return True

    def _build_indexes(self):
        """Build lookup indexes from loaded data."""
        # Index profiled names with variant matching
        names_dict = self.names_data.get("names", {})
        for raw_key, entry in names_dict.items():
            canonical = normalize_name(raw_key)
            self.profiled_names[canonical] = entry
            # Also store the original key as a variant
            self.name_variants[raw_key.upper()] = canonical
            self.name_variants[canonical] = canonical
            # Store common variants (RA2 <-> RA₂, PA3 <-> PA₃)
            word_field = entry.get("word", raw_key)
            if word_field:
                self.name_variants[word_field.upper()] = canonical
                self.name_variants[normalize_name(word_field)] = canonical

        # Index corpus tablets
        for tablet_id, data in self.inscriptions.items():
            if "_parse_error" in data:
                continue
            words = data.get("transliteratedWords", [])
            self.tablet_words[tablet_id] = words
            self.tablet_scribes[tablet_id] = data.get("scribe", "")
            self.tablet_sites[tablet_id] = extract_site(tablet_id)

        print(
            f"  Indexed {len(self.profiled_names)} profiled names, "
            f"{len(self.tablet_words)} parseable tablets"
        )

    def _match_name_in_token(self, token: str) -> Optional[str]:
        """Check if a corpus token matches any profiled name. Returns canonical name or None."""
        token_upper = token.upper().strip()
        if token_upper in self.name_variants:
            return self.name_variants[token_upper]
        # Try normalized form
        token_norm = normalize_name(token)
        if token_norm in self.name_variants:
            return self.name_variants[token_norm]
        if token_norm in self.profiled_names:
            return token_norm
        return None

    # -----------------------------------------------------------------------
    # Role inference
    # -----------------------------------------------------------------------
    def _infer_roles(self, name: str, tablet_id: str, words: List[str]) -> List[str]:
        """
        Infer administrative roles from positional context on a tablet.

        Rules:
        - Position 0 or 1 (header/line-1): source / authority / header
        - Immediately before logogram+number: recipient
        - After KU-RO: totals-related
        - After KI-RO: deficit-related
        - After A-DU: contributor
        - After SA-RA₂: allocation recipient
        """
        roles = set()
        name_norm = normalize_name(name)

        # Find all positions where this name appears
        positions = []
        for i, token in enumerate(words):
            matched = self._match_name_in_token(token)
            if matched == name_norm:
                positions.append(i)

        if not positions:
            return list(roles)

        # Filter out structural tokens for position analysis
        meaningful_tokens = [(i, t) for i, t in enumerate(words) if t not in SKIP_TOKENS]

        for pos in positions:
            # Find rank among meaningful tokens
            rank = 0
            for mi, (idx, _) in enumerate(meaningful_tokens):
                if idx == pos:
                    rank = mi
                    break

            # Header / source if first or second meaningful token
            if rank <= 1:
                roles.add("header/source")

            # Check what comes before this name
            for prev_i in range(pos - 1, max(pos - 4, -1), -1):
                if prev_i < 0:
                    break
                prev_token = words[prev_i].upper().strip()
                if prev_token in SKIP_TOKENS:
                    continue
                if prev_token in ("KU-RO", "PO-TO-KU-RO"):
                    roles.add("totals-related")
                    break
                if prev_token == "KI-RO":
                    roles.add("deficit-related")
                    break
                if prev_token == "A-DU":
                    roles.add("contributor")
                    break
                if prev_token in ("SA-RA₂", "SA-RA2"):
                    roles.add("allocation-recipient")
                    break
                break  # Only check the nearest non-skip token

            # Check what comes after this name
            for next_i in range(pos + 1, min(pos + 4, len(words))):
                if next_i >= len(words):
                    break
                next_token = words[next_i]
                if next_token in SKIP_TOKENS:
                    continue
                if is_logogram(next_token) or is_number(next_token):
                    roles.add("recipient")
                    break
                break  # Only check the nearest non-skip token

        return sorted(roles)

    # -----------------------------------------------------------------------
    # Commodity & quantity extraction
    # -----------------------------------------------------------------------
    def _extract_commodities_and_quantities(
        self, name: str, tablet_id: str, words: List[str]
    ) -> Tuple[List[str], Dict[str, float]]:
        """
        Extract commodities on the tablet and quantities associated with this name.

        Strategy: collect all logograms on the tablet as commodities.
        For quantities, look for number tokens near (after) the name on the same line.
        """
        name_norm = normalize_name(name)

        # All commodities on the tablet
        tablet_commodities = set()
        for token in words:
            if is_logogram(token):
                tablet_commodities.add(token)

        # Quantities associated with this name: scan for name -> [logogram] -> number patterns
        name_quantities: Dict[str, float] = defaultdict(float)
        i = 0
        while i < len(words):
            matched = self._match_name_in_token(words[i])
            if matched == name_norm:
                # Scan forward on the same "line" for logogram + number
                current_commodity = None
                j = i + 1
                while j < len(words):
                    token = words[j]
                    if token == "\n":
                        break  # Stop at line boundary
                    if is_logogram(token):
                        current_commodity = token
                    elif is_number(token):
                        qty = parse_number(token)
                        if current_commodity:
                            name_quantities[current_commodity] += qty
                        else:
                            name_quantities["_unspecified"] += qty
                    j += 1
            i += 1

        return sorted(tablet_commodities), dict(name_quantities)

    # -----------------------------------------------------------------------
    # Co-occurring names
    # -----------------------------------------------------------------------
    def _find_co_occurring_names(self, name: str, tablet_id: str, words: List[str]) -> List[str]:
        """Find other profiled names that appear on the same tablet."""
        name_norm = normalize_name(name)
        co_names = set()
        for token in words:
            matched = self._match_name_in_token(token)
            if matched and matched != name_norm:
                co_names.add(matched)
        return sorted(co_names)

    # -----------------------------------------------------------------------
    # Administrative tier inference
    # -----------------------------------------------------------------------
    def _compute_admin_tier(self, dossier: PersonnelDossier) -> str:
        """
        Infer administrative tier based on:
        - tablet_count: number of tablets where name appears
        - site_count: number of distinct sites
        - total_quantity: sum of all associated quantities
        - role_diversity: number of distinct roles
        """
        tablet_count = len(dossier.tablets)
        site_count = len(dossier.sites)
        role_count = len(dossier.roles)
        total_qty = dossier.total_quantity

        score = 0.0
        # Tablet spread (0-30 points)
        score += min(tablet_count * 5, 30)
        # Site spread (0-30 points) — cross-site names are rare and important
        score += min(site_count * 15, 30)
        # Role diversity (0-20 points)
        score += min(role_count * 5, 20)
        # Quantity magnitude (0-20 points)
        if total_qty > 500:
            score += 20
        elif total_qty > 100:
            score += 15
        elif total_qty > 50:
            score += 10
        elif total_qty > 10:
            score += 5

        if score >= 60:
            return "TIER_1_ELITE"
        elif score >= 40:
            return "TIER_2_SENIOR"
        elif score >= 25:
            return "TIER_3_REGULAR"
        elif score >= 10:
            return "TIER_4_MINOR"
        else:
            return "TIER_5_MARGINAL"

    # -----------------------------------------------------------------------
    # Core dossier building
    # -----------------------------------------------------------------------
    def build_dossier(self, canonical_name: str) -> PersonnelDossier:
        """Build a complete dossier for one profiled name."""
        entry = self.profiled_names.get(canonical_name, {})
        dossier = PersonnelDossier(
            name=canonical_name,
            occurrences_in_names_file=entry.get("occurrences", 0),
            best_hypothesis=entry.get("best_hypothesis", ""),
            name_type=entry.get("name_type", ""),
            gender=entry.get("gender", ""),
            confidence=entry.get("confidence", ""),
            detection_reason=entry.get("detection_reason", ""),
        )

        all_commodities: Set[str] = set()
        all_quantities: Dict[str, float] = defaultdict(float)
        all_co_names: Set[str] = set()
        all_roles: Set[str] = set()
        all_sites: Set[str] = set()
        all_scribes: Set[str] = set()

        # Scan every tablet for this name
        for tablet_id, words in self.tablet_words.items():
            # Check if this name appears on this tablet
            found = False
            for token in words:
                matched = self._match_name_in_token(token)
                if matched == canonical_name:
                    found = True
                    break

            if not found:
                continue

            dossier.tablets.append(tablet_id)
            site = self.tablet_sites.get(tablet_id, "UNKNOWN")
            all_sites.add(site)

            scribe = self.tablet_scribes.get(tablet_id, "")
            if scribe:
                all_scribes.add(scribe)

            # Roles
            roles = self._infer_roles(canonical_name, tablet_id, words)
            all_roles.update(roles)

            # Commodities & quantities
            commodities, quantities = self._extract_commodities_and_quantities(
                canonical_name, tablet_id, words
            )
            all_commodities.update(commodities)
            for comm, qty in quantities.items():
                all_quantities[comm] += qty

            # Co-occurring names
            co_names = self._find_co_occurring_names(canonical_name, tablet_id, words)
            all_co_names.update(co_names)

        dossier.tablets.sort()
        dossier.roles = sorted(all_roles)
        dossier.commodities = sorted(all_commodities)
        dossier.quantities = {k: round(v, 3) for k, v in sorted(all_quantities.items())}
        dossier.total_quantity = round(sum(all_quantities.values()), 3)
        dossier.co_occurring_names = sorted(all_co_names)
        dossier.sites = sorted(all_sites)
        dossier.scribes = sorted(all_scribes)

        # Compute administrative tier
        dossier.administrative_tier = self._compute_admin_tier(dossier)

        return dossier

    def build_all_dossiers(self) -> Dict[str, PersonnelDossier]:
        """Build dossiers for all 111 profiled names."""
        print(f"\n[Phase 1] Building dossiers for {len(self.profiled_names)} profiled names...")
        for i, canonical_name in enumerate(sorted(self.profiled_names.keys())):
            dossier = self.build_dossier(canonical_name)
            self.dossiers[canonical_name] = dossier
            self.log(
                f"  {i + 1}/{len(self.profiled_names)}: {canonical_name} "
                f"({len(dossier.tablets)} tablets)"
            )

        # Statistics
        with_tablets = sum(1 for d in self.dossiers.values() if d.tablets)
        cross_tablet = sum(1 for d in self.dossiers.values() if len(d.tablets) >= 2)
        cross_site = sum(1 for d in self.dossiers.values() if len(d.sites) >= 2)
        tier_dist = Counter(d.administrative_tier for d in self.dossiers.values())

        print(f"  Dossiers built: {len(self.dossiers)}")
        print(f"  Names found in corpus: {with_tablets}")
        print(f"  Cross-tablet names (2+ tablets): {cross_tablet}")
        print(f"  Cross-site names (2+ sites): {cross_site}")
        print(f"  Tier distribution: {dict(sorted(tier_dist.items()))}")

        return self.dossiers

    # -----------------------------------------------------------------------
    # Cross-tablet link analysis
    # -----------------------------------------------------------------------
    def analyze_cross_tablet_links(self) -> Dict:
        """Analyze names that appear on multiple tablets — administrative network."""
        print("\n[Phase 2] Analyzing cross-tablet name links...")

        links = []
        for name, dossier in sorted(self.dossiers.items(), key=lambda x: -len(x[1].tablets)):
            if len(dossier.tablets) < 2:
                continue
            links.append(
                {
                    "name": name,
                    "tablet_count": len(dossier.tablets),
                    "tablets": dossier.tablets,
                    "site_count": len(dossier.sites),
                    "sites": dossier.sites,
                    "roles": dossier.roles,
                    "commodities": dossier.commodities,
                    "total_quantity": dossier.total_quantity,
                    "administrative_tier": dossier.administrative_tier,
                    "co_occurring_names_count": len(dossier.co_occurring_names),
                }
            )

        # Network edges: name pairs that co-occur on the same tablet
        name_pair_tablets: Dict[Tuple[str, str], List[str]] = defaultdict(list)
        for tablet_id, words in self.tablet_words.items():
            names_on_tablet = set()
            for token in words:
                matched = self._match_name_in_token(token)
                if matched:
                    names_on_tablet.add(matched)
            name_list = sorted(names_on_tablet)
            for i in range(len(name_list)):
                for j in range(i + 1, len(name_list)):
                    pair = (name_list[i], name_list[j])
                    name_pair_tablets[pair].append(tablet_id)

        # Find pairs that co-occur on 2+ tablets
        strong_connections = []
        for (n1, n2), tablets in sorted(name_pair_tablets.items(), key=lambda x: -len(x[1])):
            if len(tablets) >= 2:
                strong_connections.append(
                    {
                        "name_1": n1,
                        "name_2": n2,
                        "shared_tablets": len(tablets),
                        "tablets": tablets,
                    }
                )

        analysis = {
            "cross_tablet_names": links,
            "total_cross_tablet": len(links),
            "strong_connections": strong_connections,
            "total_strong_connections": len(strong_connections),
        }

        print(f"  Cross-tablet names: {len(links)}")
        print(f"  Strong name-pair connections (2+ shared tablets): {len(strong_connections)}")

        return analysis

    # -----------------------------------------------------------------------
    # Output methods
    # -----------------------------------------------------------------------
    def print_dossier(self, dossier: PersonnelDossier):
        """Print a single dossier in human-readable format."""
        print(f"\n{'=' * 70}")
        print(f"PERSONNEL DOSSIER: {dossier.name}")
        print(f"{'=' * 70}")
        print(f"  Administrative tier : {dossier.administrative_tier}")
        tabs_str = ", ".join(dossier.tablets) if dossier.tablets else "(none found in corpus)"
        print(f"  Tablets ({len(dossier.tablets):>3d})       : {tabs_str}")
        sites_str = ", ".join(dossier.sites) if dossier.sites else "—"
        print(f"  Sites   ({len(dossier.sites):>3d})       : {sites_str}")
        scribes_str = ", ".join(dossier.scribes) if dossier.scribes else "—"
        print(f"  Scribes ({len(dossier.scribes):>3d})       : {scribes_str}")
        print(f"  Roles               : {', '.join(dossier.roles) if dossier.roles else '—'}")
        commod_str = ", ".join(dossier.commodities) if dossier.commodities else "—"
        print(f"  Commodities         : {commod_str}")
        if dossier.quantities:
            print("  Quantities          :")
            for comm, qty in dossier.quantities.items():
                label = comm if comm != "_unspecified" else "(unspecified commodity)"
                print(f"    {label:20s}: {qty:>8.1f}")
            print(f"    {'TOTAL':20s}: {dossier.total_quantity:>8.1f}")
        else:
            print("  Total quantity      : 0")
        co_names_str = (
            ", ".join(dossier.co_occurring_names[:15]) if dossier.co_occurring_names else "—"
        )
        print(f"  Co-occurring names  : {co_names_str}")
        if len(dossier.co_occurring_names) > 15:
            print(f"                        ... and {len(dossier.co_occurring_names) - 15} more")

        # Metadata from names file
        print("  --- Profile metadata ---")
        print(f"  Occurrences (names file): {dossier.occurrences_in_names_file}")
        print(f"  Best hypothesis         : {dossier.best_hypothesis or '—'}")
        print(f"  Name type               : {dossier.name_type or '—'}")
        print(f"  Gender                  : {dossier.gender or '—'}")
        print(f"  Detection reason        : {dossier.detection_reason or '—'}")

    def print_ranking(self, dossiers: List[PersonnelDossier], top_n: int = 0):
        """Print dossiers ranked by administrative importance."""
        show = dossiers[:top_n] if top_n > 0 else dossiers
        print(f"\n{'=' * 90}")
        print("PERSONNEL RANKING BY ADMINISTRATIVE IMPORTANCE")
        print(f"{'=' * 90}")
        print(
            f"\n{'Rank':>4s}  {'Name':<20s} {'Tier':<16s} {'Tabs':>4s} "
            f"{'Sites':>5s} {'Roles':>5s} {'TotQty':>8s} {'Commodities'}"
        )
        print("-" * 90)

        for i, d in enumerate(show, 1):
            comms = ", ".join(d.commodities[:5])
            if len(d.commodities) > 5:
                comms += f" +{len(d.commodities) - 5}"
            print(
                f"{i:4d}  {d.name:<20s} {d.administrative_tier:<16s} "
                f"{len(d.tablets):4d} {len(d.sites):5d} {len(d.roles):5d} "
                f"{d.total_quantity:8.1f} {comms}"
            )

        print(f"\n  Total profiled: {len(dossiers)}")

    def print_cross_tablet_report(self, analysis: Dict):
        """Print cross-tablet link analysis."""
        print(f"\n{'=' * 70}")
        print("CROSS-TABLET NAME LINKS")
        print(f"{'=' * 70}")

        links = analysis.get("cross_tablet_names", [])
        print(f"\nNames appearing on 2+ tablets: {len(links)}\n")
        print(f"{'Name':<20s} {'Tabs':>4s} {'Sites':>5s} {'Tier':<16s} {'Tablets'}")
        print("-" * 80)
        for link in links[:30]:
            tablets_str = ", ".join(link["tablets"][:6])
            if len(link["tablets"]) > 6:
                tablets_str += f" +{len(link['tablets']) - 6}"
            print(
                f"{link['name']:<20s} {link['tablet_count']:4d} "
                f"{link['site_count']:5d} {link['administrative_tier']:<16s} {tablets_str}"
            )

        connections = analysis.get("strong_connections", [])
        if connections:
            print(f"\nStrong name-pair connections (co-occur on 2+ tablets): {len(connections)}\n")
            print(f"{'Name 1':<20s} {'Name 2':<20s} {'Shared':>6s} {'Tablets'}")
            print("-" * 75)
            for conn in connections[:20]:
                tablets_str = ", ".join(conn["tablets"][:5])
                print(
                    f"{conn['name_1']:<20s} {conn['name_2']:<20s} "
                    f"{conn['shared_tablets']:6d} {tablets_str}"
                )

    def save_results(self, output_path: str, cross_tablet: Optional[Dict] = None):
        """Save all dossiers to JSON."""
        ranked = sorted(self.dossiers.values(), key=lambda d: (-len(d.tablets), -d.total_quantity))

        output = {
            "metadata": {
                "tool": "personnel_dossier_builder.py",
                "generated": datetime.now().isoformat(),
                "total_profiles": len(self.profiled_names),
                "dossiers_built": len(self.dossiers),
                "names_found_in_corpus": sum(1 for d in self.dossiers.values() if d.tablets),
                "cross_tablet_names": sum(1 for d in self.dossiers.values() if len(d.tablets) >= 2),
                "cross_site_names": sum(1 for d in self.dossiers.values() if len(d.sites) >= 2),
                "tier_distribution": dict(
                    Counter(d.administrative_tier for d in self.dossiers.values())
                ),
            },
            "dossiers": {d.name: asdict(d) for d in ranked},
        }

        if cross_tablet:
            output["cross_tablet_analysis"] = cross_tablet

        out_path = Path(output_path)
        if not out_path.is_absolute():
            out_path = PROJECT_ROOT / output_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {out_path}")

    def print_summary(self):
        """Print overall summary statistics."""
        print(f"\n{'=' * 70}")
        print("PERSONNEL DOSSIER BUILDER — SUMMARY")
        print(f"{'=' * 70}")

        total = len(self.dossiers)
        with_tablets = sum(1 for d in self.dossiers.values() if d.tablets)
        cross_tablet = sum(1 for d in self.dossiers.values() if len(d.tablets) >= 2)
        cross_site = sum(1 for d in self.dossiers.values() if len(d.sites) >= 2)

        print(f"\n  Total profiled names  : {total}")
        print(f"  Found in corpus       : {with_tablets}")
        print(f"  Cross-tablet (2+ tabs): {cross_tablet}")
        print(f"  Cross-site (2+ sites) : {cross_site}")

        tier_dist = Counter(d.administrative_tier for d in self.dossiers.values())
        print("\n  Tier distribution:")
        for tier in sorted(tier_dist.keys()):
            bar = "#" * tier_dist[tier]
            print(f"    {tier:<20s}: {tier_dist[tier]:3d} {bar}")

        # Top 5 by tablet count
        top_by_tablets = sorted(self.dossiers.values(), key=lambda d: -len(d.tablets))[:5]
        print("\n  Top 5 by tablet count:")
        for d in top_by_tablets:
            print(
                f"    {d.name:<20s}: {len(d.tablets)} tablets, "
                f"{len(d.sites)} sites, tier={d.administrative_tier}"
            )

        # Top 5 by total quantity
        top_by_qty = sorted(self.dossiers.values(), key=lambda d: -d.total_quantity)[:5]
        print("\n  Top 5 by total quantity:")
        for d in top_by_qty:
            print(
                f"    {d.name:<20s}: {d.total_quantity:.1f} units across "
                f"{len(d.commodities)} commodity types"
            )

        print(f"\n{'=' * 70}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Personnel Dossier Builder — Cross-Tablet Name Intelligence"
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Build dossiers for all 111 profiled names"
    )
    parser.add_argument(
        "--name", "-n", type=str, help="Build dossier for a specific name (e.g. A-DU)"
    )
    parser.add_argument(
        "--top", type=int, default=0, help="Show top N names by administrative importance"
    )
    parser.add_argument("--cross-tablet", action="store_true", help="Show cross-tablet name links")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Save results to JSON file (e.g. data/personnel_dossiers.json)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug output")

    args = parser.parse_args()

    if not any([args.all, args.name, args.top, args.cross_tablet]):
        parser.print_help()
        return 1

    print("=" * 70)
    print("PERSONNEL DOSSIER BUILDER")
    print("Cross-Tablet Name Intelligence for Linear A")
    print("=" * 70)

    builder = PersonnelDossierBuilder(verbose=args.verbose)
    if not builder.load_data():
        return 1

    if args.name:
        # Build dossier for a single name
        target = normalize_name(args.name)
        # Try to find it even if not in profiled names (admin terms like A-DU)
        if target not in builder.profiled_names:
            # Check if it maps via variants
            if target in builder.name_variants:
                target = builder.name_variants[target]
            else:
                # Build an ad-hoc dossier by scanning corpus directly
                print(f"\n  Note: {args.name} is not in the 111 profiled names.")
                print("  Building ad-hoc dossier from corpus scan...")
                # Add it temporarily
                builder.profiled_names[target] = {
                    "word": args.name,
                    "occurrences": 0,
                    "sites": [],
                    "detection_reason": "ad-hoc query",
                }
                builder.name_variants[target] = target
                builder.name_variants[args.name.upper()] = target

        dossier = builder.build_dossier(target)
        builder.dossiers[target] = dossier
        builder.print_dossier(dossier)

        if args.output:
            builder.save_results(args.output)

    elif args.all or args.top or args.cross_tablet:
        builder.build_all_dossiers()

        cross_tablet_analysis = None
        if args.cross_tablet or args.all:
            cross_tablet_analysis = builder.analyze_cross_tablet_links()

        if args.all:
            # Print all dossiers ranked
            ranked = sorted(
                builder.dossiers.values(), key=lambda d: (-len(d.tablets), -d.total_quantity)
            )
            builder.print_ranking(ranked)
            if cross_tablet_analysis:
                builder.print_cross_tablet_report(cross_tablet_analysis)
            builder.print_summary()

        elif args.top:
            ranked = sorted(
                builder.dossiers.values(), key=lambda d: (-len(d.tablets), -d.total_quantity)
            )
            builder.print_ranking(ranked, top_n=args.top)

        elif args.cross_tablet:
            if cross_tablet_analysis:
                builder.print_cross_tablet_report(cross_tablet_analysis)

        if args.output:
            builder.save_results(args.output, cross_tablet=cross_tablet_analysis)

    return 0


if __name__ == "__main__":
    sys.exit(main())
