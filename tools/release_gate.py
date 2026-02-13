#!/usr/bin/env python3
"""
Release Gate for Linear A

Strict release checks:
1. Tag version matches CITATION.cff version
2. CITATION.cff date-released exists
3. MASTER_STATE exists and includes release readiness section
4. MASTER_STATE guard passes

Usage:
    python tools/release_gate.py --tag v0.4.1
    python tools/release_gate.py  # reads GITHUB_REF_NAME if available
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
CITATION = PROJECT_ROOT / "CITATION.cff"
MASTER_STATE = PROJECT_ROOT / "linear-a-decipherer" / "MASTER_STATE.md"
MASTER_GUARD = PROJECT_ROOT / "tools" / "master_state_guard.py"


def parse_citation() -> tuple[str | None, str | None]:
    if not CITATION.exists():
        return None, None
    content = CITATION.read_text(encoding="utf-8")
    version_match = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
    date_match = re.search(r'^date-released:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
    version = version_match.group(1).strip() if version_match else None
    date_released = date_match.group(1).strip() if date_match else None
    return version, date_released


def normalize_tag(tag: str | None) -> str | None:
    if not tag:
        return None
    return tag[1:] if tag.startswith("v") else tag


def run_master_guard() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(MASTER_GUARD)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    output = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Run strict release gate checks")
    parser.add_argument("--tag", help="Release tag (example: v0.4.1)")
    args = parser.parse_args()

    raw_tag = args.tag or os.environ.get("GITHUB_REF_NAME")
    tag_version = normalize_tag(raw_tag)

    print("=" * 60)
    print("RELEASE GATE")
    print("=" * 60)
    print(f"Tag input: {raw_tag or 'N/A'}")

    errors: list[str] = []

    citation_version, date_released = parse_citation()
    if citation_version is None:
        errors.append("CITATION.cff missing or version not found")
    if not date_released:
        errors.append("CITATION.cff missing date-released")

    if tag_version and citation_version and tag_version != citation_version:
        errors.append(
            f"Version mismatch: tag={tag_version} vs CITATION.cff={citation_version}"
        )

    if not MASTER_STATE.exists():
        errors.append(f"Missing MASTER_STATE: {MASTER_STATE}")
    else:
        master_content = MASTER_STATE.read_text(encoding="utf-8")
        if "## Release Readiness Snapshot" not in master_content:
            errors.append("MASTER_STATE missing 'Release Readiness Snapshot' section")
        if "Last Updated" not in master_content:
            errors.append("MASTER_STATE missing Last Updated field")

    guard_rc, guard_output = run_master_guard()
    if guard_rc != 0:
        errors.append("master_state_guard.py failed")
        print("master_state_guard output:")
        print(guard_output.rstrip())

    if errors:
        print("FAILED")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("PASS")
    print(f"  CITATION version: {citation_version}")
    print(f"  CITATION date-released: {date_released}")
    if tag_version:
        print(f"  Tag version validated: {tag_version}")
    print("  MASTER_STATE guard: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
