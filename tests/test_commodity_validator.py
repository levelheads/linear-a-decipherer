"""Commodity validator regression tests: protect STRONG anchor mappings."""

import json
import py_compile
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANCHORS_FILE = DATA_DIR / "commodity_anchors.json"

sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

# Known STRONG word -> commodity mappings from v0.7.0
# ASCII words are matched by exact string; Unicode words use literal chars.
#   \u2248           = "approximately equal to" sign (approx-equal -> VIN)
#   \U00010749\U0001076B = two Linear A fraction signs (-> OLE)
#   \U00010747\U00010749 = two Linear A fraction signs (-> CYP)
EXPECTED_STRONG = {
    "\u2248": "VIN",
    "KU-NI-SU": "GRA",
    "DA-ME": "GRA",
    "KU-PA": "GRA",
}
# For the two Linear A fraction-sign words, we verify by checking
# that STRONG_ANCHOR entries exist mapping to OLE and CYP respectively.
EXPECTED_STRONG_COMMODITIES_FROM_UNICODE = {"OLE", "CYP"}


def test_commodity_validator_compiles():
    """commodity_validator.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "commodity_validator.py"), doraise=True)


def test_anchors_data_exists():
    """data/commodity_anchors.json must exist."""
    assert ANCHORS_FILE.exists(), f"Missing: {ANCHORS_FILE}"


def _load_anchors():
    with open(ANCHORS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def test_metadata_strong_anchors_count():
    """metadata.strong_anchors must be >= 6."""
    data = _load_anchors()
    strong = data.get("metadata", {}).get("strong_anchors", 0)
    assert strong >= 6, f"metadata.strong_anchors={strong}, expected >= 6"


def test_known_ascii_strong_mappings():
    """ASCII STRONG word->commodity mappings must be present and correct."""
    data = _load_anchors()
    mappings = data.get("mappings", [])

    # Build lookup: word -> entry
    lookup = {m["word"]: m for m in mappings}

    missing = []
    wrong_commodity = []
    not_strong = []

    for word, expected_commodity in EXPECTED_STRONG.items():
        if word not in lookup:
            missing.append(f"{repr(word)} -> {expected_commodity}")
        else:
            entry = lookup[word]
            if entry["primary_commodity"] != expected_commodity:
                wrong_commodity.append(
                    f"{repr(word)}: expected {expected_commodity}, got {entry['primary_commodity']}"
                )
            if entry.get("promotion_recommendation") != "STRONG_ANCHOR":
                not_strong.append(
                    f"{repr(word)}: recommendation={entry.get('promotion_recommendation')}"
                )

    failures = []
    if missing:
        failures.append(f"Missing words: {missing}")
    if wrong_commodity:
        failures.append(f"Wrong commodity: {wrong_commodity}")
    if not_strong:
        failures.append(f"Not STRONG_ANCHOR: {not_strong}")
    assert not failures, "STRONG anchor regression:\n  " + "\n  ".join(failures)


def test_unicode_strong_anchors_for_ole_and_cyp():
    """STRONG anchors must exist for OLE and CYP (Unicode fraction-sign words)."""
    data = _load_anchors()
    mappings = data.get("mappings", [])

    # Collect commodities that have at least one non-ASCII STRONG_ANCHOR word
    strong_unicode_commodities = set()
    for m in mappings:
        if m.get("promotion_recommendation") == "STRONG_ANCHOR":
            word = m["word"]
            if not word.isascii():
                strong_unicode_commodities.add(m["primary_commodity"])

    missing = EXPECTED_STRONG_COMMODITIES_FROM_UNICODE - strong_unicode_commodities
    assert not missing, (
        f"Missing Unicode STRONG anchors for commodities: {sorted(missing)}\n"
        f"  Found Unicode STRONG commodities: {sorted(strong_unicode_commodities)}"
    )


def test_strong_anchors_have_high_specificity():
    """All STRONG_ANCHOR mappings must have specificity >= 0.95."""
    data = _load_anchors()
    mappings = data.get("mappings", [])

    low_specificity = []
    for m in mappings:
        if m.get("promotion_recommendation") == "STRONG_ANCHOR":
            spec = m.get("specificity", 0)
            if spec < 0.95:
                low_specificity.append(f"{m['word']}: specificity={spec}")

    assert not low_specificity, "STRONG anchors with specificity < 0.95:\n  " + "\n  ".join(
        low_specificity
    )


def test_no_strong_anchor_has_zero_occurrences():
    """STRONG anchors must have total_occurrences > 0."""
    data = _load_anchors()
    mappings = data.get("mappings", [])

    zero_occ = []
    for m in mappings:
        if m.get("promotion_recommendation") == "STRONG_ANCHOR":
            if m.get("total_occurrences", 0) == 0:
                zero_occ.append(m["word"])

    assert not zero_occ, f"STRONG anchors with 0 occurrences: {zero_occ}"


def test_actual_strong_count_matches_metadata():
    """Number of STRONG_ANCHOR entries in mappings must match metadata."""
    data = _load_anchors()
    meta_count = data.get("metadata", {}).get("strong_anchors", -1)
    actual_count = sum(
        1 for m in data.get("mappings", []) if m.get("promotion_recommendation") == "STRONG_ANCHOR"
    )
    assert meta_count == actual_count, (
        f"metadata.strong_anchors={meta_count} but actual STRONG_ANCHOR count={actual_count}"
    )
