#!/usr/bin/env python3
"""
Shared site normalization contract for corpus-facing tools.

This module provides a single way to normalize site values from:
- inscription IDs (e.g., HT13, HTWa1, KNZb4)
- corpus site names (e.g., Haghia Triada, Khania)
- statistics aliases (e.g., HTW, KHZ)
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any


CONTRACT_VERSION = "2026-02-15.v1"

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
STATISTICS_FILE = DATA_DIR / "statistics.json"


# Preferred canonical codes for major sites and known high-frequency archives.
PREFERRED_FULL_NAME_TO_CODE = {
    "HAGHIA TRIADA": "HT",
    "KHANIA": "KH",
    "ZAKROS": "ZA",
    "PHAISTOS": "PH",
    "KNOSSOS": "KN",
    "MALIA": "MA",
    "TYLISSOS": "TY",
    "PALAIKASTRO": "PK",
    "ARKHALKHORI": "ARKH",
    "PETRAS": "PE",
    "THERA": "THE",
    "IOUKTAS": "IOZ",
    "KEA": "KE",
    "GOURNIA": "GO",
    "PYRGOS": "PYR",
}


DEFAULT_CODE_TO_NAME = {
    "HT": "Haghia Triada",
    "KH": "Khania",
    "ZA": "Zakros",
    "PH": "Phaistos",
    "KN": "Knossos",
    "MA": "Malia",
    "TY": "Tylissos",
    "PK": "Palaikastro",
}


def _normalize_key(value: str) -> str:
    cleaned = re.sub(r"[^A-Z0-9]+", "", value.upper())
    return cleaned


def extract_site_code(inscription_id: Any) -> str:
    """
    Extract site-like alphabetic prefix from inscription ID.

    Examples:
    - HT13 -> HT
    - HTWa1 -> HTW
    - KNZb4 -> KNZ
    """
    if inscription_id is None:
        return ""
    text = str(inscription_id).strip().upper()
    if not text:
        return ""
    match = re.match(r"^([A-Z]+)", text)
    return match.group(1) if match else ""


def _choose_canonical_code(aliases: list[str], full_name: str) -> str:
    preferred = PREFERRED_FULL_NAME_TO_CODE.get(full_name.upper())
    if preferred:
        return preferred

    # Prefer aliases that are not variant suffixes (W/Z endings), then shorter aliases.
    ordered = sorted(
        aliases,
        key=lambda alias: (
            alias.endswith(("W", "Z")),
            len(alias),
            alias,
        ),
    )
    return ordered[0]


def _load_statistics_sites() -> dict[str, str]:
    if not STATISTICS_FILE.exists():
        return {}
    try:
        payload = json.loads(STATISTICS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    raw = payload.get("sites_full_names", {})
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for alias, name in raw.items():
        if not isinstance(alias, str) or not isinstance(name, str):
            continue
        alias_norm = alias.strip().upper()
        if not alias_norm:
            continue
        out[alias_norm] = name.strip() or alias_norm
    return out


@lru_cache(maxsize=1)
def _site_index() -> tuple[dict[str, str], dict[str, str]]:
    """
    Build lookup indices:
    - alias/name key -> canonical code
    - canonical code -> full name
    """
    alias_to_name = _load_statistics_sites()

    # Ensure defaults exist even when statistics file is missing/stale.
    for code, name in DEFAULT_CODE_TO_NAME.items():
        alias_to_name.setdefault(code, name)

    by_name: dict[str, set[str]] = defaultdict(set)
    for alias, full_name in alias_to_name.items():
        by_name[full_name].add(alias)

    alias_to_code: dict[str, str] = {}
    code_to_name: dict[str, str] = {}

    for full_name, aliases in by_name.items():
        alias_list = sorted(aliases)
        canonical = _choose_canonical_code(alias_list, full_name)
        code_to_name[canonical] = full_name
        alias_to_code[canonical] = canonical
        alias_to_code[_normalize_key(canonical)] = canonical
        alias_to_code[_normalize_key(full_name)] = canonical
        for alias in alias_list:
            alias_to_code[alias] = canonical
            alias_to_code[_normalize_key(alias)] = canonical

    return alias_to_code, code_to_name


def normalize_site(
    *,
    site_value: Any | None = None,
    inscription_id: Any | None = None,
) -> tuple[str, str]:
    """
    Normalize site to canonical code and full name.

    Returns:
        (site_code, site_name)
    """
    alias_to_code, code_to_name = _site_index()

    candidates: list[str] = []
    if site_value is not None:
        raw_site = str(site_value).strip()
        if raw_site:
            candidates.append(raw_site)
    code_from_id = extract_site_code(inscription_id)
    if code_from_id:
        candidates.append(code_from_id)

    for candidate in candidates:
        upper = candidate.upper()
        canonical = alias_to_code.get(upper) or alias_to_code.get(_normalize_key(upper))
        if canonical:
            return canonical, code_to_name.get(canonical, canonical)

    if code_from_id:
        return code_from_id, code_from_id
    return "UNKNOWN", "Unknown"


def build_site_totals(inscriptions: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Count corpus inscriptions by normalized site.

    Returns map:
      site_code -> {"site_code", "site_name", "inscriptions_total"}
    """
    totals: dict[str, dict[str, Any]] = {}
    for inscription_id, row in inscriptions.items():
        if not isinstance(row, dict):
            continue
        if "_parse_error" in row:
            continue
        code, name = normalize_site(
            site_value=row.get("site"),
            inscription_id=inscription_id,
        )
        entry = totals.setdefault(
            code,
            {
                "site_code": code,
                "site_name": name,
                "inscriptions_total": 0,
            },
        )
        entry["inscriptions_total"] += 1
    return totals
