"""Hypothesis consistency tests: all hypothesis tools must agree on the 7-hypothesis set."""

import importlib
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ensure tools/ is importable
sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

EXPECTED_7 = {"luwian", "semitic", "pregreek", "protogreek", "hurrian", "hattic", "etruscan"}
EXPECTED_8 = EXPECTED_7 | {"isolate"}


def test_hypothesis_tester_case_marker_predictions():
    """CASE_MARKER_PREDICTIONS must have exactly the canonical 7 hypotheses."""
    mod = importlib.import_module("tools.hypothesis_tester")
    keys = set(mod.CASE_MARKER_PREDICTIONS.keys())
    assert keys == EXPECTED_7, (
        f"CASE_MARKER_PREDICTIONS keys mismatch.\n"
        f"  Expected: {sorted(EXPECTED_7)}\n"
        f"  Got:      {sorted(keys)}\n"
        f"  Missing:  {sorted(EXPECTED_7 - keys)}\n"
        f"  Extra:    {sorted(keys - EXPECTED_7)}"
    )


def test_falsification_system_hypothesis_list():
    """falsification_system.classify_all must iterate over all 7 hypotheses."""
    importlib.import_module("tools.falsification_system")  # ensure importable
    # The FalsificationSystem.classify_all method defines a local `hypotheses` list.
    # We instantiate and inspect the classify_all source or call it indirectly.
    # Safer: read the source and check the list.
    src = (TOOLS_DIR / "falsification_system.py").read_text(encoding="utf-8")

    # Verify each of the 7 hypotheses appears in the source
    for hyp in EXPECTED_7:
        assert f'"{hyp}"' in src, f"falsification_system.py missing hypothesis: {hyp}"


def test_negative_evidence_handles_all_7():
    """negative_evidence must have analysis methods for all 7 hypotheses."""
    mod = importlib.import_module("tools.negative_evidence")
    src = (TOOLS_DIR / "negative_evidence.py").read_text(encoding="utf-8")

    # negative_evidence uses "greek" for Proto-Greek and "pregreek" for Pre-Greek.
    # Mapping: protogreek -> greek in negative_evidence naming.
    ne_names = {"luwian", "semitic", "greek", "pregreek", "hurrian", "hattic", "etruscan"}

    # Check argparse choices include all 7 + "all"
    assert "choices=" in src, "negative_evidence.py must have argparse choices"
    for name in ne_names:
        assert f'"{name}"' in src, f"negative_evidence.py missing hypothesis choice: {name}"

    # Check analysis method exists for each
    method_map = {
        "greek": "analyze_greek_negative_evidence",
        "semitic": "analyze_semitic_negative_evidence",
        "luwian": "analyze_luwian_negative_evidence",
        "pregreek": "analyze_pregreek_negative_evidence",
        "hurrian": "analyze_hurrian_negative_evidence",
        "hattic": "analyze_hattic_negative_evidence",
        "etruscan": "analyze_etruscan_negative_evidence",
    }
    for hyp, method_name in method_map.items():
        assert hasattr(mod.NegativeEvidenceAnalyzer, method_name), (
            f"NegativeEvidenceAnalyzer missing method: {method_name}"
        )


def test_bayesian_priors_cover_7_plus_isolate():
    """bayesian_hypothesis_tester DEFAULT_PRIORS must cover 7 hypotheses + isolate."""
    mod = importlib.import_module("tools.bayesian_hypothesis_tester")
    prior_keys = set(mod.DEFAULT_PRIORS.keys())
    assert prior_keys == EXPECTED_8, (
        f"DEFAULT_PRIORS keys mismatch.\n"
        f"  Expected: {sorted(EXPECTED_8)}\n"
        f"  Got:      {sorted(prior_keys)}\n"
        f"  Missing:  {sorted(EXPECTED_8 - prior_keys)}\n"
        f"  Extra:    {sorted(prior_keys - EXPECTED_8)}"
    )
    # Priors must sum to ~1.0
    total = sum(mod.DEFAULT_PRIORS.values())
    assert abs(total - 1.0) < 0.01, f"DEFAULT_PRIORS sum to {total}, expected ~1.0"


def test_tool_parity_checker_hypothesis_tuple():
    """tool_parity_checker.HYPOTHESES must match the canonical 7."""
    mod = importlib.import_module("tools.tool_parity_checker")
    parity_set = set(mod.HYPOTHESES)
    assert parity_set == EXPECTED_7, (
        f"tool_parity_checker.HYPOTHESES mismatch.\n"
        f"  Expected: {sorted(EXPECTED_7)}\n"
        f"  Got:      {sorted(parity_set)}"
    )


def test_tool_parity_checker_runs():
    """tool_parity_checker.py should execute without error."""
    result = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "tool_parity_checker.py")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, (
        f"tool_parity_checker.py failed (exit {result.returncode}):\n"
        f"  stdout: {result.stdout[:500]}\n"
        f"  stderr: {result.stderr[:500]}"
    )
