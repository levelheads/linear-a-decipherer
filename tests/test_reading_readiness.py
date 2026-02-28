"""Reading readiness scorer tests: score ranges and known high-scorers."""

import json
import py_compile
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
READINESS_FILE = DATA_DIR / "reading_readiness.json"

sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

# Tablets known to score well (VERIFIED arithmetic + good coverage)
KNOWN_HIGH_SCORERS = {"ZA15b", "HT92", "HT86a"}


def test_reading_readiness_scorer_compiles():
    """reading_readiness_scorer.py must compile without syntax errors."""
    py_compile.compile(str(TOOLS_DIR / "reading_readiness_scorer.py"), doraise=True)


def _ensure_readiness_data() -> dict:
    """Load readiness data, generating it if missing."""
    if READINESS_FILE.exists():
        with open(READINESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    # Generate the data file
    result = subprocess.run(
        [
            sys.executable,
            str(TOOLS_DIR / "reading_readiness_scorer.py"),
            "--all",
            "--output",
            str(READINESS_FILE),
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"reading_readiness_scorer.py --all failed (exit {result.returncode}):\n"
        f"  stderr: {result.stderr[:500]}"
    )
    assert READINESS_FILE.exists(), f"Scorer ran but {READINESS_FILE} was not created"
    with open(READINESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def test_all_scores_in_valid_range():
    """Every readiness_score must be in [0.0, 1.0]."""
    data = _ensure_readiness_data()
    rankings = data.get("rankings", [])
    assert len(rankings) > 0, "No rankings in readiness data"

    out_of_range = []
    for r in rankings:
        score = r.get("readiness_score", -1)
        if score < 0.0 or score > 1.0:
            out_of_range.append(f"{r['tablet_id']}: {score}")

    assert not out_of_range, "Scores outside [0.0, 1.0]:\n  " + "\n  ".join(out_of_range)


def test_all_coverages_in_valid_range():
    """Every coverage_pct must be in [0.0, 100.0] (percentage)."""
    data = _ensure_readiness_data()
    rankings = data.get("rankings", [])
    assert len(rankings) > 0, "No rankings in readiness data"

    out_of_range = []
    for r in rankings:
        cov = r.get("coverage_pct", -1)
        if cov < 0.0 or cov > 100.0:
            out_of_range.append(f"{r['tablet_id']}: {cov}%")

    assert not out_of_range, "Coverages outside [0.0, 100.0]:\n  " + "\n  ".join(out_of_range)


def test_known_high_scorers_above_threshold():
    """Known high-scoring tablets must have score > 0.5."""
    data = _ensure_readiness_data()
    rankings = data.get("rankings", [])

    score_by_id = {r["tablet_id"]: r["readiness_score"] for r in rankings}

    failures = []
    for tid in sorted(KNOWN_HIGH_SCORERS):
        if tid not in score_by_id:
            failures.append(f"{tid}: not found in rankings")
        elif score_by_id[tid] <= 0.5:
            failures.append(f"{tid}: score={score_by_id[tid]:.3f} (expected > 0.5)")

    assert not failures, "High-scorer regression:\n  " + "\n  ".join(failures)


def test_rankings_sorted_descending():
    """Rankings should be sorted by readiness_score descending."""
    data = _ensure_readiness_data()
    rankings = data.get("rankings", [])
    if len(rankings) < 2:
        return  # Nothing to check

    scores = [r["readiness_score"] for r in rankings]
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i + 1], (
            f"Rankings not sorted: index {i} ({scores[i]}) < index {i + 1} ({scores[i + 1]})"
        )


def test_no_negative_word_counts():
    """Word counts (total, anchored, named, unknown) must never be negative."""
    data = _ensure_readiness_data()
    rankings = data.get("rankings", [])

    negatives = []
    count_fields = ["total_words", "anchored_words", "named_words", "unknown_words"]
    for r in rankings:
        for field in count_fields:
            val = r.get(field, 0)
            if val < 0:
                negatives.append(f"{r['tablet_id']}.{field}={val}")

    assert not negatives, "Negative word counts:\n  " + "\n  ".join(negatives)
