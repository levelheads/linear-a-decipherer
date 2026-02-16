#!/usr/bin/env python3
"""
Lane Orchestrator for Linear A

Runs lane-defined command bundles and emits a structured handoff report.

Manifest format:
- JSON-compatible YAML (JSON object saved as .yaml is supported).
- Root object must include `lanes` array.

Usage:
    python tools/lane_orchestrator.py --lane all --dry-run
    python tools/lane_orchestrator.py --lane A
    python tools/lane_orchestrator.py --lane C,D --date 2026-02-21
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).parent.parent
DEFAULT_MANIFEST = PROJECT_ROOT / "config" / "lane_manifest.yaml"


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"Manifest not found: {path}") from exc

    # The repository is stdlib-only, so we accept JSON-compatible YAML.
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Manifest must be JSON-compatible YAML (valid JSON content in .yaml file)."
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError("Manifest root must be an object")
    lanes = data.get("lanes")
    if not isinstance(lanes, list):
        raise RuntimeError("Manifest must include a 'lanes' array")
    return data


def get_git_status() -> set[str]:
    proc = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return set()
    files = set()
    for line in (proc.stdout or "").splitlines():
        if len(line) < 4:
            continue
        files.add(line[3:].strip())
    return files


def normalize_lane_ids(raw_lane: str) -> list[str]:
    if raw_lane.strip().lower() == "all":
        return ["all"]
    return [part.strip() for part in raw_lane.split(",") if part.strip()]


def run_command(command: str, cwd: Path, timeout_sec: int) -> dict[str, Any]:
    start = time.monotonic()
    try:
        proc = subprocess.run(
            command,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        duration = time.monotonic() - start
        return {
            "status": "PASS" if proc.returncode == 0 else "FAIL",
            "exit_code": proc.returncode,
            "duration_sec": round(duration, 3),
            "stdout_tail": (proc.stdout or "")[-2000:],
            "stderr_tail": (proc.stderr or "")[-2000:],
        }
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - start
        return {
            "status": "TIMEOUT",
            "exit_code": None,
            "duration_sec": round(duration, 3),
            "stdout_tail": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
        }


def evaluate_lane(
    lane: dict[str, Any],
    *,
    execution_date: str,
    dry_run: bool,
    fail_fast: bool,
) -> dict[str, Any]:
    lane_id = str(lane.get("lane_id", "")).strip()
    owner = str(lane.get("owner", "unassigned"))
    mission = str(lane.get("mission", ""))
    commands = lane.get("commands", [])
    required_artifacts = lane.get("required_artifacts", [])
    merge_gate = str(lane.get("merge_gate", ""))
    fallback = str(lane.get("fallback", ""))
    handoff_defaults = lane.get("handoff", {}) if isinstance(lane.get("handoff"), dict) else {}

    if not isinstance(commands, list):
        commands = []
    if not isinstance(required_artifacts, list):
        required_artifacts = []

    before_files = get_git_status()
    command_results: list[dict[str, Any]] = []
    lane_failed = False

    for command_spec in commands:
        if isinstance(command_spec, str):
            command = command_spec
            command_name = command_spec
            timeout_sec = 1800
            allow_failure = False
            command_cwd = PROJECT_ROOT
        elif isinstance(command_spec, dict):
            command = str(command_spec.get("cmd", "")).strip()
            command_name = str(command_spec.get("name", command)).strip() or command
            timeout_sec = int(command_spec.get("timeout_sec", 1800) or 1800)
            allow_failure = bool(command_spec.get("allow_failure", False))
            rel_cwd = str(command_spec.get("cwd", "")).strip()
            command_cwd = (PROJECT_ROOT / rel_cwd).resolve() if rel_cwd else PROJECT_ROOT
        else:
            continue

        if not command:
            continue

        result = {
            "name": command_name,
            "cmd": command,
            "cwd": str(command_cwd),
            "allow_failure": allow_failure,
        }

        if dry_run:
            result.update(
                {
                    "status": "DRY_RUN",
                    "exit_code": None,
                    "duration_sec": 0.0,
                    "stdout_tail": "",
                    "stderr_tail": "",
                }
            )
        else:
            command_result = run_command(command, command_cwd, timeout_sec)
            result.update(command_result)
            if command_result["status"] != "PASS" and not allow_failure:
                lane_failed = True

        command_results.append(result)

        if lane_failed and fail_fast and not dry_run:
            break

    artifact_checks: list[dict[str, Any]] = []
    for artifact in required_artifacts:
        rel = str(artifact).strip()
        if not rel:
            continue
        artifact_path = (PROJECT_ROOT / rel).resolve()
        artifact_checks.append(
            {
                "path": rel,
                "exists": artifact_path.exists(),
            }
        )

    missing_artifacts = [row["path"] for row in artifact_checks if not row["exists"]]
    after_files = get_git_status()
    changed_files = sorted(after_files - before_files)

    all_commands_passed = all(
        row["status"] in ("PASS", "DRY_RUN") or row.get("allow_failure", False)
        for row in command_results
    )
    artifacts_ok = len(missing_artifacts) == 0

    if dry_run:
        lane_status = "DRY_RUN"
    elif all_commands_passed and artifacts_ok:
        lane_status = "PASS"
    elif not all_commands_passed:
        lane_status = "FAIL"
    else:
        lane_status = "BLOCKED"

    evidence_artifacts = [row["path"] for row in artifact_checks if row["exists"]]
    if "evidence_artifacts" in handoff_defaults and isinstance(
        handoff_defaults["evidence_artifacts"], list
    ):
        evidence_artifacts = handoff_defaults["evidence_artifacts"]

    handoff = {
        "what_changed": (
            "Dry-run only; no commands executed."
            if dry_run
            else (
                ", ".join(changed_files)
                if changed_files
                else "No repository-tracked changes detected."
            )
        ),
        "evidence_artifacts": evidence_artifacts,
        "confidence_impact": handoff_defaults.get(
            "confidence_impact", "No confidence change recorded."
        ),
        "dependencies_affected": handoff_defaults.get("dependencies_affected", []),
        "open_risks": handoff_defaults.get("open_risks", []),
        "required_reviewer_lane": handoff_defaults.get("required_reviewer_lane", "A"),
    }

    return {
        "lane_id": lane_id,
        "owner": owner,
        "mission": mission,
        "execution_date": execution_date,
        "status": lane_status,
        "merge_gate": merge_gate,
        "fallback": fallback,
        "commands": command_results,
        "artifacts": artifact_checks,
        "missing_artifacts": missing_artifacts,
        "handoff": handoff,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lane orchestration workflow")
    parser.add_argument(
        "--lane",
        default="all",
        help="Lane id(s) to run: A, B, C ... or comma-separated list, or 'all'",
    )
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Path to JSON-compatible YAML lane manifest",
    )
    parser.add_argument(
        "--date",
        dest="execution_date",
        default=date.today().isoformat(),
        help="Execution date for report naming (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        help="Output path for handoff report JSON (default: data/lane_handoffs/<date>.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render execution plan without running commands",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop lane command sequence on first non-allowed failure",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    try:
        manifest = load_manifest(manifest_path)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1

    selected_ids = normalize_lane_ids(args.lane)
    all_lanes = manifest.get("lanes", [])
    selected_lanes: list[dict[str, Any]] = []
    if selected_ids == ["all"]:
        selected_lanes = [lane for lane in all_lanes if isinstance(lane, dict)]
    else:
        wanted = {item.upper() for item in selected_ids}
        for lane in all_lanes:
            if not isinstance(lane, dict):
                continue
            lane_id = str(lane.get("lane_id", "")).upper()
            if lane_id in wanted:
                selected_lanes.append(lane)

    if not selected_lanes:
        print("Error: no matching lanes found in manifest")
        return 1

    lane_reports = [
        evaluate_lane(
            lane,
            execution_date=args.execution_date,
            dry_run=args.dry_run,
            fail_fast=args.fail_fast,
        )
        for lane in selected_lanes
    ]

    status_counts: dict[str, int] = {}
    for lane_report in lane_reports:
        status = lane_report["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else (PROJECT_ROOT / "data" / "lane_handoffs" / f"{args.execution_date}.json").resolve()
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "metadata": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "manifest_path": str(manifest_path),
            "execution_date": args.execution_date,
            "dry_run": args.dry_run,
            "selected_lanes": [str(lane.get("lane_id", "")) for lane in selected_lanes],
        },
        "summary": {
            "total_lanes": len(lane_reports),
            "status_counts": status_counts,
        },
        "lanes": lane_reports,
    }
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("=" * 60)
    print("LANE ORCHESTRATOR")
    print("=" * 60)
    print(f"Manifest: {manifest_path}")
    print(f"Execution date: {args.execution_date}")
    print(f"Dry run: {'yes' if args.dry_run else 'no'}")
    print(f"Lanes: {', '.join(report['metadata']['selected_lanes'])}")
    print("Status counts:")
    for key in sorted(status_counts):
        print(f"  - {key}: {status_counts[key]}")
    print(f"Report: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
