#!/usr/bin/env python3
"""
Release Audit Tool for Linear A

Compares local git tags to published GitHub releases when network/API access
is available.

Usage:
    python tools/release_audit.py
    python tools/release_audit.py --strict-network
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent


def run_cmd(cmd: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def get_local_tags() -> list[str]:
    rc, out, err = run_cmd(["git", "tag", "--list", "--sort=creatordate"])
    if rc != 0:
        raise RuntimeError(f"Failed to list local tags: {err}")
    return [line.strip() for line in out.splitlines() if line.strip()]


def get_github_releases() -> list[str]:
    rc, out, err = run_cmd(["gh", "release", "list", "--limit", "100", "--json", "tagName"])
    if rc != 0:
        raise RuntimeError(err or "Failed to fetch GitHub releases")
    data = json.loads(out or "[]")
    return [item.get("tagName", "").strip() for item in data if item.get("tagName")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local tags vs GitHub releases")
    parser.add_argument(
        "--strict-network",
        action="store_true",
        help="Fail if GitHub release API is unavailable",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("RELEASE AUDIT")
    print("=" * 60)

    try:
        local_tags = get_local_tags()
    except Exception as exc:
        print(f"FAILED: {exc}")
        return 1

    print(f"Local tags: {len(local_tags)}")
    for tag in local_tags:
        print(f"  - {tag}")

    try:
        release_tags = get_github_releases()
    except Exception as exc:
        msg = f"GitHub release API unavailable: {exc}"
        if args.strict_network:
            print(f"FAILED: {msg}")
            return 1
        print(f"WARNING: {msg}")
        print("Audit result: PARTIAL (local-only)")
        return 0

    release_set = set(release_tags)
    local_set = set(local_tags)
    missing_on_github = sorted(local_set - release_set)
    missing_locally = sorted(release_set - local_set)

    print(f"GitHub releases: {len(release_tags)}")
    for tag in release_tags:
        print(f"  - {tag}")

    if missing_on_github:
        print("Tags present locally but missing on GitHub releases:")
        for tag in missing_on_github:
            print(f"  - {tag}")

    if missing_locally:
        print("Tags present on GitHub releases but missing locally:")
        for tag in missing_locally:
            print(f"  - {tag}")

    if missing_on_github or missing_locally:
        print("FAILED: release/tag mismatch detected")
        return 1

    print("PASS: local tags and GitHub releases are aligned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
