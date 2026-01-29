#!/usr/bin/env python3
"""
Git Manager for Linear A Decipherment Project

Provides consistent git workflow management:
- Status checks before/after work sessions
- Pre-commit validation
- Commit message formatting
- Push verification

Usage:
    python tools/git_manager.py status      # Check current state
    python tools/git_manager.py pre-commit  # Validate before committing
    python tools/git_manager.py summary     # Generate commit summary
    python tools/git_manager.py sync        # Full sync check

This script ensures project success by maintaining consistent version control.
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Dict

PROJECT_ROOT = Path(__file__).parent.parent


def run_git(args: List[str], capture=True) -> Tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ['git'] + args,
        cwd=PROJECT_ROOT,
        capture_output=capture,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def get_status() -> Dict:
    """Get comprehensive git status."""
    status = {
        'branch': '',
        'remote_status': '',
        'staged': [],
        'modified': [],
        'untracked': [],
        'has_uncommitted': False,
        'needs_push': False,
    }

    # Get current branch
    code, out, _ = run_git(['branch', '--show-current'])
    status['branch'] = out.strip()

    # Get status
    code, out, _ = run_git(['status', '--porcelain'])
    for line in out.strip().split('\n'):
        if not line:
            continue
        state = line[:2]
        filepath = line[3:]

        if state[0] in 'MADRC':
            status['staged'].append(filepath)
        if state[1] in 'MADRC':
            status['modified'].append(filepath)
        if state == '??':
            # Filter out ignored patterns
            if not any(p in filepath for p in ['__pycache__', '.DS_Store']):
                status['untracked'].append(filepath)

    status['has_uncommitted'] = bool(status['staged'] or status['modified'] or status['untracked'])

    # Check if ahead of remote
    code, out, _ = run_git(['rev-list', '--count', '@{u}..HEAD'])
    if code == 0 and out.strip():
        ahead = int(out.strip())
        status['needs_push'] = ahead > 0
        if ahead > 0:
            status['remote_status'] = f'{ahead} commit(s) ahead of origin'

    # Check if behind remote
    code, out, _ = run_git(['rev-list', '--count', 'HEAD..@{u}'])
    if code == 0 and out.strip():
        behind = int(out.strip())
        if behind > 0:
            status['remote_status'] = f'{behind} commit(s) behind origin'

    if not status['remote_status']:
        status['remote_status'] = 'Up to date with origin'

    return status


def print_status():
    """Print formatted git status."""
    status = get_status()

    print("=" * 60)
    print("LINEAR A DECIPHERER - GIT STATUS")
    print("=" * 60)
    print(f"Branch: {status['branch']}")
    print(f"Remote: {status['remote_status']}")
    print()

    if status['staged']:
        print(f"STAGED ({len(status['staged'])}):")
        for f in status['staged'][:10]:
            print(f"  + {f}")
        if len(status['staged']) > 10:
            print(f"  ... and {len(status['staged']) - 10} more")
        print()

    if status['modified']:
        print(f"MODIFIED ({len(status['modified'])}):")
        for f in status['modified'][:10]:
            print(f"  M {f}")
        if len(status['modified']) > 10:
            print(f"  ... and {len(status['modified']) - 10} more")
        print()

    if status['untracked']:
        print(f"UNTRACKED ({len(status['untracked'])}):")
        for f in status['untracked'][:10]:
            print(f"  ? {f}")
        if len(status['untracked']) > 10:
            print(f"  ... and {len(status['untracked']) - 10} more")
        print()

    if not status['has_uncommitted']:
        print("✓ Working directory clean")

    if status['needs_push']:
        print(f"⚠ {status['remote_status']} - push recommended")

    print("=" * 60)
    return status


def pre_commit_check() -> bool:
    """Run pre-commit validation checks."""
    print("=" * 60)
    print("PRE-COMMIT CHECKLIST")
    print("=" * 60)

    checks_passed = True

    # Check 1: No data/ files staged (should be gitignored)
    code, out, _ = run_git(['diff', '--cached', '--name-only'])
    staged_files = out.strip().split('\n') if out.strip() else []
    data_files = [f for f in staged_files if f.startswith('data/')]
    if data_files:
        print("✗ ERROR: data/ files staged (should be gitignored)")
        for f in data_files:
            print(f"    {f}")
        checks_passed = False
    else:
        print("✓ No data/ files staged")

    # Check 2: No __pycache__ staged
    pycache_files = [f for f in staged_files if '__pycache__' in f]
    if pycache_files:
        print("✗ ERROR: __pycache__ files staged")
        checks_passed = False
    else:
        print("✓ No __pycache__ files staged")

    # Check 3: Python files have no syntax errors
    py_files = [f for f in staged_files if f.endswith('.py')]
    for py_file in py_files:
        filepath = PROJECT_ROOT / py_file
        if filepath.exists():
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', str(filepath)],
                capture_output=True
            )
            if result.returncode != 0:
                print(f"✗ Syntax error in {py_file}")
                checks_passed = False
    if py_files and checks_passed:
        print(f"✓ Python syntax valid ({len(py_files)} files)")

    # Check 4: README.md updated if tools/ changed
    tools_changed = any(f.startswith('tools/') and f.endswith('.py') for f in staged_files)
    readme_changed = 'README.md' in staged_files
    if tools_changed and not readme_changed:
        print("⚠ WARNING: tools/ changed but README.md not updated")
    elif tools_changed and readme_changed:
        print("✓ README.md updated with tools/ changes")

    # Check 5: Analyses have proper structure
    analysis_files = [f for f in staged_files if f.startswith('analyses/') and f.endswith('.md')]
    for af in analysis_files:
        filepath = PROJECT_ROOT / af
        if filepath.exists():
            content = filepath.read_text()
            if '## EXECUTIVE SUMMARY' not in content and '## Overview' not in content:
                print(f"⚠ WARNING: {af} may be missing summary section")

    print()
    if checks_passed:
        print("✓ All pre-commit checks passed")
    else:
        print("✗ Some checks failed - review before committing")

    print("=" * 60)
    return checks_passed


def generate_commit_summary() -> str:
    """Generate a commit message summary based on staged changes."""
    code, out, _ = run_git(['diff', '--cached', '--stat'])
    if not out.strip():
        print("No staged changes to summarize")
        return ""

    code, files_out, _ = run_git(['diff', '--cached', '--name-only'])
    files = files_out.strip().split('\n') if files_out.strip() else []

    # Categorize changes
    categories = {
        'tools': [],
        'analyses': [],
        'docs': [],
        'data': [],
        'other': [],
    }

    for f in files:
        if f.startswith('tools/'):
            categories['tools'].append(f)
        elif f.startswith('analyses/'):
            categories['analyses'].append(f)
        elif f.endswith('.md'):
            categories['docs'].append(f)
        elif f.startswith('data/'):
            categories['data'].append(f)
        else:
            categories['other'].append(f)

    # Generate summary
    parts = []

    if categories['tools']:
        new_tools = [f for f in categories['tools'] if 'new file' in out]
        if new_tools:
            parts.append(f"Add {len(new_tools)} new tool(s)")
        else:
            parts.append(f"Update {len(categories['tools'])} tool(s)")

    if categories['analyses']:
        parts.append(f"Add/update {len(categories['analyses'])} analysis document(s)")

    if categories['docs']:
        parts.append(f"Update documentation")

    summary = "; ".join(parts) if parts else "Update project files"

    print("=" * 60)
    print("SUGGESTED COMMIT MESSAGE")
    print("=" * 60)
    print()
    print(f"Subject: {summary}")
    print()
    print("Files changed:")
    for f in files[:15]:
        print(f"  - {f}")
    if len(files) > 15:
        print(f"  ... and {len(files) - 15} more")
    print()
    print("=" * 60)

    return summary


def sync_check():
    """Full synchronization check."""
    print("=" * 60)
    print("FULL SYNC CHECK")
    print("=" * 60)
    print()

    # Fetch latest from remote
    print("Fetching from remote...")
    run_git(['fetch'])

    # Show status
    status = get_status()

    issues = []

    if status['has_uncommitted']:
        issues.append(f"Uncommitted changes: {len(status['modified'])} modified, {len(status['untracked'])} untracked")

    if status['needs_push']:
        issues.append(f"Unpushed commits: {status['remote_status']}")

    if 'behind' in status['remote_status']:
        issues.append(f"Need to pull: {status['remote_status']}")

    if issues:
        print("⚠ ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("RECOMMENDED ACTIONS:")
        if status['has_uncommitted']:
            print("  1. Stage changes: git add <files>")
            print("  2. Commit: git commit -m 'message'")
        if status['needs_push']:
            print("  3. Push: git push")
        if 'behind' in status['remote_status']:
            print("  - Pull first: git pull")
    else:
        print("✓ Repository fully synchronized")
        print("  - Working directory clean")
        print("  - Up to date with origin")
        print("  - No unpushed commits")

    print()
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/git_manager.py <command>")
        print()
        print("Commands:")
        print("  status      - Show current git status")
        print("  pre-commit  - Run pre-commit checks")
        print("  summary     - Generate commit message summary")
        print("  sync        - Full synchronization check")
        return 1

    command = sys.argv[1]

    if command == 'status':
        print_status()
    elif command == 'pre-commit':
        success = pre_commit_check()
        return 0 if success else 1
    elif command == 'summary':
        generate_commit_summary()
    elif command == 'sync':
        sync_check()
    else:
        print(f"Unknown command: {command}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
