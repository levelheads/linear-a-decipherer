"""Tests for the month sprint orchestration workflow."""

import importlib
import json
import py_compile
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))


def test_sprint_orchestrator_compiles():
    """sprint_orchestrator.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "sprint_orchestrator.py"), doraise=True)


def test_sprint_orchestrator_import():
    """sprint_orchestrator.py should be importable."""
    importlib.import_module("tools.sprint_orchestrator")


def test_lane_manifest_includes_reading_lane():
    """The lane manifest should define lane G for reading attempts."""
    manifest = json.loads((PROJECT_ROOT / "config" / "lane_manifest.yaml").read_text())
    lane_ids = {str(lane.get("lane_id", "")).upper() for lane in manifest.get("lanes", [])}
    assert "G" in lane_ids, "Lane G missing from config/lane_manifest.yaml"


def test_sprint_orchestrator_dry_run_with_lane_execution():
    """A week-1 dry run should emit sprint and lane reports."""
    tool = TOOLS_DIR / "sprint_orchestrator.py"
    sprint_report = PROJECT_ROOT / "data" / "test_sprint_report.json"
    lane_report = PROJECT_ROOT / "data" / "test_lane_report.json"

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(tool),
                "--week",
                "1",
                "--phase",
                "baseline",
                "--run-lanes",
                "--dry-run",
                "--output",
                str(sprint_report),
                "--lane-output",
                str(lane_report),
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        assert result.returncode == 0, (
            f"sprint dry-run failed (exit {result.returncode}):\n"
            f"STDOUT:\n{result.stdout[:1000]}\nSTDERR:\n{result.stderr[:1000]}"
        )
        assert sprint_report.exists(), "Sprint report was not written"
        assert lane_report.exists(), "Lane report was not written"

        report = json.loads(sprint_report.read_text())
        assert report["metadata"]["dry_run"] is True
        assert report["sprint"]["sprint_id"] == "month1-decipherment-2026-03"
        assert report["lane_execution"]["requested"] is True
        assert report["lane_execution"]["status"] == "PASS"
        assert "G" in report["selected"]["lanes"]
        week_ids = {entry["week_id"] for entry in report["selected"]["weeks"]}
        assert "1" in week_ids
    finally:
        sprint_report.unlink(missing_ok=True)
        lane_report.unlink(missing_ok=True)


def test_sprint_orchestrator_week2_includes_execution_profile():
    """Week-2 reports should carry the balanced-split execution metadata."""
    tool = TOOLS_DIR / "sprint_orchestrator.py"
    sprint_report = PROJECT_ROOT / "data" / "test_week2_sprint_report.json"

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(tool),
                "--week",
                "2",
                "--phase",
                "baseline",
                "--dry-run",
                "--output",
                str(sprint_report),
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        assert result.returncode == 0, (
            f"week-2 sprint dry-run failed (exit {result.returncode}):\n"
            f"STDOUT:\n{result.stdout[:1000]}\nSTDERR:\n{result.stderr[:1000]}"
        )
        report = json.loads(sprint_report.read_text())
        assert report["sprint"]["execution_profile"]["mode"] == "balanced_split"
        assert (
            report["sprint"]["execution_profile"]["capacity_split"]["admin_translation_pct"] == 55
        )
        week = report["selected"]["weeks"][0]
        assert week["execution_slates"]["admin_primary"][0] == "HT2"
        assert week["weekly_output_targets"]["admin_readings"] == 3
    finally:
        sprint_report.unlink(missing_ok=True)
