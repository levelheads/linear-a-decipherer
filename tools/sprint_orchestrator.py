#!/usr/bin/env python3
"""
Sprint Orchestrator for Linear A.

Wraps the existing lane orchestration workflow with sprint metadata:
agents, weekly objectives, cadence phases, and month-end deliverables.

Manifest format:
- JSON-compatible YAML (valid JSON content saved as .yaml is supported)
- Root object must include:
  - sprint_id
  - title
  - agents (array)
  - weeks (array)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = PROJECT_ROOT / "config" / "month1_decipherment_manifest.yaml"
DEFAULT_LANE_MANIFEST = PROJECT_ROOT / "config" / "lane_manifest.yaml"
LANE_ORCHESTRATOR = PROJECT_ROOT / "tools" / "lane_orchestrator.py"
WEEK_OPTIONAL_FIELDS = (
    "execution_slates",
    "weekly_output_targets",
    "acceptance_checks",
)


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"Manifest not found: {path}") from exc

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Manifest must be JSON-compatible YAML (valid JSON content in .yaml file)."
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError("Manifest root must be an object")
    if not isinstance(data.get("agents"), list):
        raise RuntimeError("Manifest must include an 'agents' array")
    if not isinstance(data.get("weeks"), list):
        raise RuntimeError("Manifest must include a 'weeks' array")
    sprint_id = str(data.get("sprint_id", "")).strip()
    title = str(data.get("title", "")).strip()
    if not sprint_id or not title:
        raise RuntimeError("Manifest must include non-empty sprint_id and title")
    return data


def parse_selector(raw: str) -> set[str] | None:
    if raw.strip().lower() == "all":
        return None
    values = {part.strip().lower() for part in raw.split(",") if part.strip()}
    return values or None


def normalize_week_id(value: Any) -> str:
    return str(value).strip()


def sanitize_token(value: str) -> str:
    chars = []
    for char in value.lower():
        if char.isalnum() or char in ("-", "_"):
            chars.append(char)
        else:
            chars.append("-")
    sanitized = "".join(chars).strip("-")
    return sanitized or "selection"


def select_weeks(
    manifest: dict[str, Any],
    week_filter: set[str] | None,
    phase_filter: set[str] | None,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for week in manifest.get("weeks", []):
        if not isinstance(week, dict):
            continue
        week_id = normalize_week_id(week.get("week_id", ""))
        if week_filter is not None and week_id.lower() not in week_filter:
            continue

        phase_rows = []
        for phase in week.get("phases", []):
            if not isinstance(phase, dict):
                continue
            phase_id = str(phase.get("phase_id", "")).strip()
            if not phase_id:
                continue
            if phase_filter is not None and phase_id.lower() not in phase_filter:
                continue
            phase_rows.append(
                {
                    "phase_id": phase_id,
                    "cadence": str(phase.get("cadence", "")).strip(),
                    "summary": str(phase.get("summary", "")).strip(),
                    "lanes": [
                        str(lane).strip().upper()
                        for lane in phase.get("lanes", [])
                        if str(lane).strip()
                    ],
                }
            )

        if phase_filter is not None and not phase_rows:
            continue

        week_record = {
            "week_id": week_id,
            "label": str(week.get("label", "")).strip(),
            "objective": str(week.get("objective", "")).strip(),
            "primary_lanes": [
                str(lane).strip().upper()
                for lane in week.get("primary_lanes", [])
                if str(lane).strip()
            ],
            "priority_targets": [
                str(item).strip() for item in week.get("priority_targets", []) if str(item).strip()
            ],
            "deliverables": [
                str(item).strip() for item in week.get("deliverables", []) if str(item).strip()
            ],
            "phases": phase_rows,
        }
        for field in WEEK_OPTIONAL_FIELDS:
            value = week.get(field)
            if isinstance(value, (dict, list)):
                week_record[field] = value
        selected.append(week_record)
    return selected


def collect_lanes(selected_weeks: list[dict[str, Any]]) -> list[str]:
    lanes: list[str] = []
    seen: set[str] = set()
    for week in selected_weeks:
        for lane in week.get("primary_lanes", []):
            if lane not in seen:
                seen.add(lane)
                lanes.append(lane)
        for phase in week.get("phases", []):
            for lane in phase.get("lanes", []):
                if lane not in seen:
                    seen.add(lane)
                    lanes.append(lane)
    return lanes


def select_agents(manifest: dict[str, Any], selected_lanes: list[str]) -> list[dict[str, Any]]:
    lane_set = set(selected_lanes)
    selected: list[dict[str, Any]] = []
    for agent in manifest.get("agents", []):
        if not isinstance(agent, dict):
            continue
        primary_lanes = {
            str(lane).strip().upper()
            for lane in agent.get("primary_lanes", [])
            if str(lane).strip()
        }
        if primary_lanes & lane_set:
            selected.append(
                {
                    "agent_id": str(agent.get("agent_id", "")).strip(),
                    "name": str(agent.get("name", "")).strip(),
                    "primary_lanes": sorted(primary_lanes),
                    "mission": str(agent.get("mission", "")).strip(),
                    "standing_deliverables": [
                        str(item).strip()
                        for item in agent.get("standing_deliverables", [])
                        if str(item).strip()
                    ],
                }
            )
    return selected


def ensure_project_path(path: Path) -> None:
    if not str(path.resolve()).startswith(str(PROJECT_ROOT)):
        raise RuntimeError(f"Path must be within project root: {path}")


def default_output_path(execution_date: str, sprint_id: str, weeks: list[dict[str, Any]]) -> Path:
    suffix = "all" if not weeks else "-".join(sanitize_token(week["week_id"]) for week in weeks)
    filename = f"{execution_date}_{sanitize_token(sprint_id)}_{suffix}.json"
    return PROJECT_ROOT / "data" / "sprint_reports" / filename


def default_lane_output_path(
    execution_date: str, sprint_id: str, weeks: list[dict[str, Any]]
) -> Path:
    suffix = "all" if not weeks else "-".join(sanitize_token(week["week_id"]) for week in weeks)
    filename = f"{execution_date}_{sanitize_token(sprint_id)}_{suffix}.json"
    return PROJECT_ROOT / "data" / "lane_handoffs" / filename


def run_lanes(
    *,
    lanes: list[str],
    lane_manifest: Path,
    execution_date: str,
    dry_run: bool,
    fail_fast: bool,
    lane_output: Path,
) -> dict[str, Any]:
    ensure_project_path(lane_output)
    cmd = [
        sys.executable,
        str(LANE_ORCHESTRATOR),
        "--lane",
        ",".join(lanes),
        "--manifest",
        str(lane_manifest),
        "--date",
        execution_date,
        "--output",
        str(lane_output),
    ]
    if dry_run:
        cmd.append("--dry-run")
    if fail_fast:
        cmd.append("--fail-fast")

    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    nested_status = "PASS" if proc.returncode == 0 else "FAIL"
    status_counts: dict[str, int] = {}
    if lane_output.exists():
        try:
            lane_report = json.loads(lane_output.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            lane_report = {}
        summary = lane_report.get("summary", {}) if isinstance(lane_report, dict) else {}
        if isinstance(summary, dict):
            raw_counts = summary.get("status_counts", {})
            if isinstance(raw_counts, dict):
                status_counts = {
                    str(key): int(value)
                    for key, value in raw_counts.items()
                    if isinstance(key, str)
                }
        if status_counts.get("FAIL", 0) or status_counts.get("BLOCKED", 0):
            nested_status = "FAIL"

    return {
        "requested": True,
        "status": nested_status,
        "exit_code": proc.returncode,
        "lane_ids": lanes,
        "lane_manifest": str(lane_manifest),
        "report_path": str(lane_output),
        "status_counts": status_counts,
        "stdout_tail": (proc.stdout or "")[-4000:],
        "stderr_tail": (proc.stderr or "")[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run sprint-level orchestration workflow")
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Path to JSON-compatible YAML sprint manifest",
    )
    parser.add_argument(
        "--week",
        default="all",
        help="Week id(s) to run: 1,2,3,4 or comma-separated list, or 'all'",
    )
    parser.add_argument(
        "--phase",
        default="all",
        help="Phase id(s) to run: baseline,sync,promotion or comma-separated list, or 'all'",
    )
    parser.add_argument(
        "--date",
        dest="execution_date",
        default=date.today().isoformat(),
        help="Execution date for report naming (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        help="Output path for sprint report JSON (default: data/sprint_reports/<date>_<sprint>.json)",
    )
    parser.add_argument(
        "--run-lanes",
        action="store_true",
        help="Invoke lane_orchestrator.py for the selected weeks/phases",
    )
    parser.add_argument(
        "--lane-output",
        help="Output path for nested lane handoff JSON (default: data/lane_handoffs/<date>_<sprint>.json)",
    )
    parser.add_argument(
        "--lane-manifest",
        default=str(DEFAULT_LANE_MANIFEST),
        help="Path to JSON-compatible YAML lane manifest",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render the sprint plan without executing lane commands",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop nested lane execution on first non-allowed failure",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    lane_manifest_path = Path(args.lane_manifest).expanduser().resolve()
    try:
        manifest = load_manifest(manifest_path)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1

    week_filter = parse_selector(args.week)
    phase_filter = parse_selector(args.phase)
    selected_weeks = select_weeks(manifest, week_filter, phase_filter)
    if not selected_weeks:
        print("Error: no matching weeks/phases found in manifest")
        return 1

    selected_lanes = collect_lanes(selected_weeks)
    selected_agents = select_agents(manifest, selected_lanes)

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else default_output_path(
            args.execution_date, manifest["sprint_id"], selected_weeks
        ).resolve()
    )
    ensure_project_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lane_execution: dict[str, Any] = {
        "requested": False,
        "status": "NOT_RUN",
        "lane_ids": selected_lanes,
    }
    if args.run_lanes:
        lane_output_path = (
            Path(args.lane_output).expanduser().resolve()
            if args.lane_output
            else default_lane_output_path(
                args.execution_date, manifest["sprint_id"], selected_weeks
            ).resolve()
        )
        lane_output_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            lane_execution = run_lanes(
                lanes=selected_lanes,
                lane_manifest=lane_manifest_path,
                execution_date=args.execution_date,
                dry_run=args.dry_run,
                fail_fast=args.fail_fast,
                lane_output=lane_output_path,
            )
        except RuntimeError as exc:
            print(f"Error: {exc}")
            return 1
        if lane_execution["status"] != "PASS":
            print(lane_execution.get("stderr_tail", "").strip())

    report = {
        "metadata": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "manifest_path": str(manifest_path),
            "lane_manifest_path": str(lane_manifest_path),
            "execution_date": args.execution_date,
            "dry_run": args.dry_run,
        },
        "sprint": {
            "sprint_id": manifest["sprint_id"],
            "title": manifest["title"],
            "summary": manifest.get("summary", ""),
            "success_criteria": manifest.get("success_criteria", []),
            "month_end_deliverables": manifest.get("month_end_deliverables", []),
            "critical_risks": manifest.get("critical_risks", []),
            "execution_profile": manifest.get("execution_profile", {}),
            "workstreams": manifest.get("workstreams", []),
        },
        "selected": {
            "weeks": selected_weeks,
            "lanes": selected_lanes,
            "agents": selected_agents,
        },
        "lane_execution": lane_execution,
    }
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("=" * 60)
    print("SPRINT ORCHESTRATOR")
    print("=" * 60)
    print(f"Sprint: {manifest['sprint_id']} — {manifest['title']}")
    print(f"Execution date: {args.execution_date}")
    print(f"Dry run: {'yes' if args.dry_run else 'no'}")
    execution_profile = manifest.get("execution_profile", {})
    if isinstance(execution_profile, dict) and execution_profile:
        mode = str(execution_profile.get("mode", "")).strip() or "unspecified"
        split = execution_profile.get("capacity_split", {})
        if isinstance(split, dict) and split:
            split_summary = "/".join(
                str(split.get(key, ""))
                for key in (
                    "admin_translation_pct",
                    "ritual_register_pct",
                    "breakthrough_hunting_pct",
                )
            )
            print(f"Execution profile: {mode} ({split_summary})")
        else:
            print(f"Execution profile: {mode}")
    print("Weeks:")
    for week in selected_weeks:
        phase_ids = ", ".join(phase["phase_id"] for phase in week.get("phases", [])) or "all"
        print(f"  - {week['week_id']}: {week['label']} [{phase_ids}]")
    print(f"Lanes: {', '.join(selected_lanes)}")
    print(f"Agents: {', '.join(agent['agent_id'] for agent in selected_agents)}")
    print(f"Report: {output_path}")
    if args.run_lanes:
        print(f"Lane execution: {lane_execution['status']}")
        print(f"Lane report: {lane_execution.get('report_path', 'n/a')}")

    return 0 if lane_execution.get("status", "PASS") != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
