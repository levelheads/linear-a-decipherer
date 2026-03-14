"""Tests for the four VENTRIS-release tools (v0.11.0).

Covers:
  - cascade_opportunity_detector.py
  - personnel_dossier_builder.py
  - sign_value_extractor.py
  - reading_pipeline.py
"""

import importlib
import py_compile
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

VENTRIS_TOOLS = [
    "cascade_opportunity_detector",
    "personnel_dossier_builder",
    "sign_value_extractor",
    "reading_pipeline",
]


# ── Compilation ──────────────────────────────────────────────────────


def test_ventris_tools_compile():
    """All four VENTRIS tools must compile without syntax errors."""
    failures = []
    for name in VENTRIS_TOOLS:
        py_file = TOOLS_DIR / f"{name}.py"
        assert py_file.exists(), f"Missing tool: {py_file}"
        try:
            py_compile.compile(str(py_file), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append(str(e))
    assert not failures, "Compilation failures:\n" + "\n".join(failures)


# ── Import ───────────────────────────────────────────────────────────


def test_ventris_tools_import():
    """All four VENTRIS tools should be importable."""
    failures = []
    for name in VENTRIS_TOOLS:
        mod = f"tools.{name}"
        try:
            importlib.import_module(mod)
        except Exception as e:
            failures.append(f"{mod}: {e}")
    assert not failures, "Import failures:\n" + "\n".join(failures)


# ── --help smoke tests ───────────────────────────────────────────────


def test_cascade_opportunity_detector_help():
    """cascade_opportunity_detector.py --help must exit 0."""
    tool = TOOLS_DIR / "cascade_opportunity_detector.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"--help failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_personnel_dossier_builder_help():
    """personnel_dossier_builder.py --help must exit 0."""
    tool = TOOLS_DIR / "personnel_dossier_builder.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"--help failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_sign_value_extractor_help():
    """sign_value_extractor.py --help must exit 0."""
    tool = TOOLS_DIR / "sign_value_extractor.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"--help failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_reading_pipeline_help():
    """reading_pipeline.py --help must exit 0."""
    tool = TOOLS_DIR / "reading_pipeline.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--help"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"--help failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


# ── Basic invocation tests ───────────────────────────────────────────


def test_cascade_all_anchors_runs():
    """cascade_opportunity_detector.py --all-anchors should complete."""
    tool = TOOLS_DIR / "cascade_opportunity_detector.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--all-anchors"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"--all-anchors failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_personnel_dossier_top_runs():
    """personnel_dossier_builder.py --top 5 should complete."""
    tool = TOOLS_DIR / "personnel_dossier_builder.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--top", "5"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"--top 5 failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_sign_value_extractor_ratios_runs():
    """sign_value_extractor.py --ratios should complete."""
    tool = TOOLS_DIR / "sign_value_extractor.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--ratios"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"--ratios failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )


def test_reading_pipeline_select_runs():
    """reading_pipeline.py --select --top 5 should complete."""
    tool = TOOLS_DIR / "reading_pipeline.py"
    result = subprocess.run(
        [sys.executable, str(tool), "--select", "--top", "5"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"--select --top 5 failed (exit {result.returncode}):\n{result.stderr[:500]}"
    )
