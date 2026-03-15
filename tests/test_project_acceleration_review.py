"""Tests for the project acceleration review workflow."""

import json
import py_compile
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_project_acceleration_review_compiles():
    """project_acceleration_review.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "project_acceleration_review.py"), doraise=True)


def test_project_acceleration_review_outputs_current_signals(tmp_path):
    """The review should surface the live NI/I-PI-NA-MA decision state."""
    tool = TOOLS_DIR / "project_acceleration_review.py"
    json_out = tmp_path / "project_acceleration_review.json"
    markdown_out = tmp_path / "project_acceleration_review.md"

    result = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--output-json",
            str(json_out),
            "--markdown-out",
            str(markdown_out),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"project_acceleration_review failed (exit {result.returncode}):\n"
        f"STDOUT:\n{result.stdout[:1000]}\nSTDERR:\n{result.stderr[:1000]}"
    )
    assert json_out.exists(), "JSON review artifact was not written"
    assert markdown_out.exists(), "Markdown review artifact was not written"

    review = json.loads(json_out.read_text(encoding="utf-8"))
    assert review["project_snapshot"]["tool_inventory"]["python_tool_count"] >= 62
    assert review["execution_review"]["profile"]["mode"] == "balanced_split"
    assert review["execution_review"]["profile"]["capacity_split"]["ritual_register_pct"] == 35
    assert (
        review["execution_review"]["next_window"]["execution_slates"]["admin_primary"][0] == "HT2"
    )
    assert review["promotion_review"]["NI"]["decision"] == "APPROVE"
    assert review["promotion_review"]["NI"]["integrated_entry_source"] == "commodity_anchors"
    assert review["promotion_review"]["I-PI-NA-MA"]["decision"] == "HOLD"
    assert "cross_corpus_consistency" in review["promotion_review"]["I-PI-NA-MA"]["failed_required"]
    assert len(review["queue_review"]["top_ten"]) > 0, "queue_review.top_ten should not be empty"
    opportunity_ids = {item["id"] for item in review["opportunities"]}
    assert "ni_cascade_exploitation" in opportunity_ids
