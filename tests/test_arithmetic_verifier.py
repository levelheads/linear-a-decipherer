"""Arithmetic verifier regression tests: protect 6 VERIFIED KU-RO tablets."""

import json
import py_compile
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VERIFICATION_FILE = DATA_DIR / "arithmetic_verification.json"

sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

# The 6 tablets confirmed as VERIFIED in v0.7.0
MUST_BE_VERIFIED = {"HT9b", "HT11b", "HT85a", "HT94b", "HT104", "HT117a"}


def test_arithmetic_verifier_compiles():
    """arithmetic_verifier.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "arithmetic_verifier.py"), doraise=True)


def test_verification_data_exists():
    """data/arithmetic_verification.json must exist."""
    assert VERIFICATION_FILE.exists(), f"Missing: {VERIFICATION_FILE}"


def _load_verification_data():
    with open(VERIFICATION_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def test_exactly_34_kuro_tablets():
    """Exactly 34 tablets must have has_kuro=True."""
    data = _load_verification_data()
    kuro_tablets = [v for v in data["verifications"] if v.get("has_kuro")]
    assert len(kuro_tablets) == 34, f"Expected 34 has_kuro=True tablets, got {len(kuro_tablets)}"


def test_at_least_6_verified():
    """At least 6 tablets must have kuro_status=='VERIFIED'."""
    data = _load_verification_data()
    verified = [v for v in data["verifications"] if v.get("kuro_status") == "VERIFIED"]
    assert len(verified) >= 6, f"Expected >= 6 VERIFIED tablets, got {len(verified)}"


def test_specific_tablets_verified():
    """The 6 known-good tablets must each be VERIFIED."""
    data = _load_verification_data()
    status_by_id = {v["tablet_id"]: v["kuro_status"] for v in data["verifications"]}
    missing = []
    not_verified = []
    for tid in sorted(MUST_BE_VERIFIED):
        if tid not in status_by_id:
            missing.append(tid)
        elif status_by_id[tid] != "VERIFIED":
            not_verified.append(f"{tid}: {status_by_id[tid]}")

    failures = []
    if missing:
        failures.append(f"Missing tablets: {missing}")
    if not_verified:
        failures.append(f"Not VERIFIED: {not_verified}")
    assert not failures, "Regression in VERIFIED tablets:\n  " + "\n  ".join(failures)


def test_verified_tablets_have_zero_difference():
    """Every VERIFIED tablet must have difference == 0."""
    data = _load_verification_data()
    verified = [v for v in data["verifications"] if v.get("kuro_status") == "VERIFIED"]
    nonzero = []
    for v in verified:
        diff = v.get("difference")
        if diff is not None and diff != 0 and diff != 0.0:
            nonzero.append(f"{v['tablet_id']}: difference={diff}")
    assert not nonzero, "VERIFIED tablets with nonzero difference:\n  " + "\n  ".join(nonzero)


def test_metadata_counts_match():
    """Metadata with_kuro and verified counts must match actual data."""
    data = _load_verification_data()
    meta = data.get("metadata", {})

    actual_kuro = sum(1 for v in data["verifications"] if v.get("has_kuro"))
    actual_verified = sum(1 for v in data["verifications"] if v.get("kuro_status") == "VERIFIED")

    assert meta.get("with_kuro") == actual_kuro, (
        f"metadata.with_kuro={meta.get('with_kuro')} but actual={actual_kuro}"
    )
    assert meta.get("verified") == actual_verified, (
        f"metadata.verified={meta.get('verified')} but actual={actual_verified}"
    )
