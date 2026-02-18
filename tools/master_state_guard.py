#!/usr/bin/env python3
"""
Master State Guard for Linear A

Validates canonical-state governance expectations:
1. MASTER_STATE.md exists with required sections
2. Legacy status files include redirect banners to MASTER_STATE.md
3. Tool count metric in MASTER_STATE matches actual tools/*.py count

Usage:
    python tools/master_state_guard.py
    python tools/master_state_guard.py --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
MASTER_STATE = PROJECT_ROOT / "linear-a-decipherer" / "MASTER_STATE.md"
README = PROJECT_ROOT / "README.md"

LEGACY_REDIRECT_FILES = [
    PROJECT_ROOT / "analysis" / "archive" / "PROJECT_REVIEW.md",
    PROJECT_ROOT / "linear-a-decipherer" / "KNOWLEDGE.md",
    PROJECT_ROOT / "analysis" / "archive" / "OPERATION_MINOS_III_TRACKING.md",
    PROJECT_ROOT / "linear-a-decipherer" / "ANALYSIS_INDEX.md",
]

REQUIRED_MASTER_HEADINGS = [
    "## Canonical Rule",
    "## Metrics Snapshot",
    "## Metric Source Map",
    "## Active Campaigns",
    "## Promotion Board",
    "## Current Risks and Blockers",
    "## Release Readiness Snapshot",
    "## Update Protocol",
]


def extract_master_tool_count(content: str) -> int | None:
    """
    Extract tool count metric from MASTER_STATE metrics table.
    Expected row format:
    | Tool count (Python scripts) | <number> | `tools/*.py` |
    """
    match = re.search(
        r"^\|\s*Tool count \(Python scripts\)\s*\|\s*(\d+)\s*\|",
        content,
        flags=re.MULTILINE,
    )
    if not match:
        return None
    return int(match.group(1))


def count_python_tools() -> int:
    return len(list((PROJECT_ROOT / "tools").glob("*.py")))


def validate_master_state(errors: list[str]) -> str:
    if not MASTER_STATE.exists():
        errors.append(f"Missing canonical file: {MASTER_STATE}")
        return ""

    content = MASTER_STATE.read_text(encoding="utf-8")

    for heading in REQUIRED_MASTER_HEADINGS:
        if heading not in content:
            errors.append(f"MASTER_STATE missing required section: {heading}")

    if "Last Updated" not in content:
        errors.append("MASTER_STATE missing Last Updated field")

    declared_tools = extract_master_tool_count(content)
    if declared_tools is None:
        errors.append("MASTER_STATE missing tool count metric row")
    else:
        actual_tools = count_python_tools()
        if declared_tools != actual_tools:
            errors.append(
                f"Tool count drift: MASTER_STATE={declared_tools}, tools/*.py={actual_tools}"
            )

    return content


def validate_redirect_banners(errors: list[str]) -> None:
    for path in LEGACY_REDIRECT_FILES:
        if not path.exists():
            errors.append(f"Missing legacy file for redirect validation: {path}")
            continue
        content = path.read_text(encoding="utf-8")
        if "MASTER_STATE.md" not in content:
            errors.append(f"Legacy file missing MASTER_STATE redirect: {path}")


def validate_readme(errors: list[str]) -> None:
    if not README.exists():
        errors.append(f"Missing README: {README}")
        return
    content = README.read_text(encoding="utf-8")
    if "MASTER_STATE.md" not in content:
        errors.append("README missing canonical MASTER_STATE pointer")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate canonical-state governance")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on warnings as errors (reserved for future use)",
    )
    args = parser.parse_args()

    _ = args  # reserved for future extension
    errors: list[str] = []

    print("=" * 60)
    print("MASTER STATE GUARD")
    print("=" * 60)

    validate_master_state(errors)
    validate_redirect_banners(errors)
    validate_readme(errors)

    if errors:
        print("FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("PASS")
    print(f"  MASTER_STATE: {MASTER_STATE}")
    print(f"  tools/*.py count: {count_python_tools()}")
    print(f"  legacy redirects checked: {len(LEGACY_REDIRECT_FILES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
