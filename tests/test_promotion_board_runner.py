"""Promotion board runner regressions."""

import json
import py_compile
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_promotion_board_runner_compiles():
    """promotion_board_runner.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "promotion_board_runner.py"), doraise=True)


def test_promotion_board_runner_ni_uses_commodity_anchor(tmp_path):
    """NI should use commodity-anchor evidence instead of failing integrated validation."""
    tool = TOOLS_DIR / "promotion_board_runner.py"
    packet = tmp_path / "NI.md"
    decisions = tmp_path / "promotion_decisions.json"

    result = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--candidate",
            "NI",
            "--target-confidence",
            "HIGH",
            "--packet-out",
            str(packet),
            "--json-out",
            str(decisions),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"promotion_board_runner NI failed (exit {result.returncode}):\n"
        f"STDOUT:\n{result.stdout[:1000]}\nSTDERR:\n{result.stderr[:1000]}"
    )

    data = json.loads(decisions.read_text(encoding="utf-8"))
    row = next(item for item in data["decisions"] if item["candidate"] == "NI")
    assert row["decision"] == "APPROVE"
    assert row["evidence"]["commodity_entry_found"] is True
    assert row["evidence"]["integrated_entry_source"] == "commodity_anchors"
    assert row["gate_results"]["integrated_validation"]["passed"] is True
    assert row["gate_results"]["cross_corpus_consistency"]["required"] is False
    assert row["gate_results"]["multi_hypothesis_run"]["required"] is False


def test_promotion_board_runner_i_pi_na_ma_still_hold(tmp_path):
    """I-PI-NA-MA should remain HOLD until cross-corpus consistency improves."""
    tool = TOOLS_DIR / "promotion_board_runner.py"
    packet = tmp_path / "I-PI-NA-MA.md"
    decisions = tmp_path / "promotion_decisions.json"

    result = subprocess.run(
        [
            sys.executable,
            str(tool),
            "--candidate",
            "I-PI-NA-MA",
            "--target-confidence",
            "PROBABLE",
            "--packet-out",
            str(packet),
            "--json-out",
            str(decisions),
        ],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(PROJECT_ROOT),
    )
    assert result.returncode == 0, (
        f"promotion_board_runner I-PI-NA-MA failed (exit {result.returncode}):\n"
        f"STDOUT:\n{result.stdout[:1000]}\nSTDERR:\n{result.stderr[:1000]}"
    )

    data = json.loads(decisions.read_text(encoding="utf-8"))
    row = next(item for item in data["decisions"] if item["candidate"] == "I-PI-NA-MA")
    assert row["decision"] == "HOLD"
    assert row["gate_results"]["cross_corpus_consistency"]["passed"] is False
