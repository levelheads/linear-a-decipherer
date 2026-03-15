#!/usr/bin/env python3
"""
Project-wide Linear A acceleration review.

Aggregates the current platform state, research outputs, promotion outcomes,
queue signals, and cascade opportunities into one machine-readable review that
can drive the next sprint decision.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = PROJECT_ROOT / "analysis" / "active"
TOOLS_DIR = PROJECT_ROOT / "tools"
DOCS_DIR = PROJECT_ROOT / "linear-a-decipherer"
LANE_MANIFEST = PROJECT_ROOT / "config" / "lane_manifest.yaml"
SPRINT_MANIFEST = PROJECT_ROOT / "config" / "month1_decipherment_manifest.yaml"
DEFAULT_JSON_OUTPUT = DATA_DIR / "project_acceleration_review.json"

STATUS_ROW_RE = re.compile(r"^\|\s*(?P<label>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|$")
LAST_UPDATED_RE = re.compile(
    r"^\*\*Last Updated\*\*:\s*(?P<date>\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE
)

CORE_TOOLCHAINS = {
    "orchestration": [
        "lane_orchestrator.py",
        "sprint_orchestrator.py",
    ],
    "governance": [
        "master_state_guard.py",
        "refresh_master_state.py",
        "update_index.py",
        "project_acceleration_review.py",
    ],
    "validation": [
        "corpus_consistency_validator.py",
        "integrated_validator.py",
        "tool_parity_checker.py",
        "promotion_board_runner.py",
        "dependency_trace_resolver.py",
    ],
    "throughput": [
        "reading_readiness_scorer.py",
        "reading_pipeline.py",
        "cascade_opportunity_detector.py",
    ],
    "reading_support": [
        "personnel_dossier_builder.py",
        "sign_value_extractor.py",
        "arithmetic_verifier.py",
    ],
}


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def parse_last_updated(text: str) -> str | None:
    match = LAST_UPDATED_RE.search(text)
    return match.group("date") if match else None


def parse_markdown_table(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = STATUS_ROW_RE.match(line.strip())
        if not match:
            continue
        label = match.group("label").strip()
        value = match.group("value").strip()
        if label.startswith("-") or label.lower() == "metric":
            continue
        rows[label] = value
    return rows


def parse_ints_from_text(value: str) -> list[int]:
    return [int(token.replace(",", "")) for token in re.findall(r"\d[\d,]*", value)]


def extract_connected_reading_snapshot(knowledge_rows: dict[str, str]) -> dict[str, Any]:
    raw = knowledge_rows.get("Connected Readings", "")
    numbers = parse_ints_from_text(raw)
    return {
        "raw": raw,
        "tablet_readings": numbers[0] if len(numbers) >= 1 else 0,
        "thematic_analyses": numbers[1] if len(numbers) >= 2 else 0,
        "sites": numbers[2] if len(numbers) >= 3 else 0,
    }


def extract_tool_count(knowledge_rows: dict[str, str]) -> int:
    raw = knowledge_rows.get("Tool Count", "")
    numbers = parse_ints_from_text(raw)
    return numbers[0] if numbers else len(list(TOOLS_DIR.glob("*.py")))


def load_manifest(path: Path) -> dict[str, Any]:
    data = load_json(path)
    return data if isinstance(data, dict) else {}


def summarize_execution_review(manifest: dict[str, Any]) -> dict[str, Any]:
    execution_profile = manifest.get("execution_profile", {})
    weeks = manifest.get("weeks", []) if isinstance(manifest.get("weeks"), list) else []
    next_week = next(
        (
            week
            for week in weeks
            if isinstance(week, dict) and str(week.get("week_id", "")).strip() == "2"
        ),
        weeks[0] if weeks and isinstance(weeks[0], dict) else {},
    )
    return {
        "profile": execution_profile if isinstance(execution_profile, dict) else {},
        "workstreams": manifest.get("workstreams", [])
        if isinstance(manifest.get("workstreams"), list)
        else [],
        "next_window": {
            "week_id": str(next_week.get("week_id", "")).strip(),
            "label": str(next_week.get("label", "")).strip(),
            "execution_slates": next_week.get("execution_slates", {}),
            "weekly_output_targets": next_week.get("weekly_output_targets", {}),
            "acceptance_checks": next_week.get("acceptance_checks", []),
        },
    }


def latest_sprint_report() -> dict[str, Any] | None:
    report_dir = DATA_DIR / "sprint_reports"
    reports = sorted(report_dir.glob("*.json"))
    if not reports:
        return None
    data = load_json(reports[-1])
    if not isinstance(data, dict):
        return None
    return {
        "path": str(reports[-1]),
        "generated": data.get("metadata", {}).get("generated"),
        "execution_date": data.get("metadata", {}).get("execution_date"),
        "lane_status": data.get("lane_execution", {}).get("status"),
        "lane_ids": data.get("lane_execution", {}).get("lane_ids", []),
        "status_counts": data.get("lane_execution", {}).get("status_counts", {}),
    }


def extract_toolchains() -> dict[str, Any]:
    categories: dict[str, Any] = {}
    for name, filenames in CORE_TOOLCHAINS.items():
        statuses = []
        for filename in filenames:
            path = TOOLS_DIR / filename
            statuses.append(
                {
                    "tool": filename,
                    "present": path.exists(),
                    "path": str(path),
                }
            )
        categories[name] = {
            "present": sum(1 for item in statuses if item["present"]),
            "expected": len(statuses),
            "tools": statuses,
        }
    return categories


def latest_decision(decisions: list[dict[str, Any]], candidate: str) -> dict[str, Any] | None:
    candidates = [row for row in decisions if row.get("candidate") == candidate]
    if not candidates:
        return None
    return max(candidates, key=lambda row: str(row.get("generated", "")))


def summarize_decision(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    gates = row.get("gate_results", {})
    required_gate_ids = set(row.get("required_gate_ids", []))
    failed_gates = sorted(
        gate_id
        for gate_id, gate in gates.items()
        if gate_id in required_gate_ids and not gate.get("passed")
    )
    evidence = row.get("evidence", {})
    return {
        "candidate": row.get("candidate"),
        "generated": row.get("generated"),
        "decision": row.get("decision"),
        "target_confidence": row.get("target_confidence"),
        "failed_required": failed_gates,
        "sites_found": evidence.get("sites_found", []),
        "threshold_category": evidence.get("threshold_category"),
        "final_confidence": evidence.get("final_confidence"),
        "commodity_entry_found": evidence.get("commodity_entry_found"),
        "integrated_entry_source": evidence.get("integrated_entry_source"),
        "anchor_dependencies": evidence.get("effective_anchor_dependencies")
        or evidence.get("anchor_dependencies", []),
        "cross_corpus_evidence": gates.get("cross_corpus_consistency", {}).get("evidence"),
        "integrated_validation_evidence": gates.get("integrated_validation", {}).get("evidence"),
    }


def summarize_queue(data: dict[str, Any] | None) -> dict[str, Any]:
    queue = data.get("queue", []) if isinstance(data, dict) else []
    top_ten = queue[:10]
    site_counts = Counter(item.get("site", "UNK") for item in top_ten if item.get("site"))
    return {
        "queue_size": len(queue),
        "top_ten": [
            {
                "tablet_id": item.get("tablet_id"),
                "site": item.get("site"),
                "readiness_score": item.get("readiness_score"),
                "coverage_pct": item.get("coverage_pct"),
                "document_type": item.get("document_type"),
                "cascade_boost": item.get("cascade_boost"),
            }
            for item in top_ten
        ],
        "top_ten_site_counts": dict(site_counts),
        "ht_share_top_ten": round(
            sum(count for site, count in site_counts.items() if site.startswith("HT"))
            / max(len(top_ten), 1),
            3,
        )
        if top_ten
        else 0.0,
    }


def summarize_cascade(data: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(data, dict):
        return {
            "trigger": None,
            "summary": {},
            "top_threshold_crossers": [],
        }
    opportunities = data.get("opportunities", [])
    threshold_crossers = [
        item
        for item in opportunities
        if (item.get("current_readiness", 0) < 0.5 <= item.get("new_readiness", 0))
    ]
    return {
        "trigger": data.get("trigger"),
        "summary": data.get("summary", {}),
        "top_threshold_crossers": [
            {
                "tablet_id": item.get("tablet_id"),
                "site": item.get("site"),
                "current_readiness": item.get("current_readiness"),
                "new_readiness": item.get("new_readiness"),
                "readiness_delta": item.get("readiness_delta"),
            }
            for item in threshold_crossers[:10]
        ],
    }


def build_opportunities(
    *,
    queue_summary: dict[str, Any],
    cascade_summary: dict[str, Any],
    ni_decision: dict[str, Any] | None,
    i_pi_na_ma_decision: dict[str, Any] | None,
    sprint_summary: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    opportunities: list[dict[str, Any]] = []
    ni_summary = cascade_summary.get("summary", {})
    if ni_decision and ni_decision.get("decision") == "APPROVE":
        opportunities.append(
            {
                "id": "ni_cascade_exploitation",
                "priority": "immediate",
                "summary": "Exploit the now-approved NI anchor across the queue and cascade threshold crossers.",
                "evidence": {
                    "decision": ni_decision.get("decision"),
                    "target_confidence": ni_decision.get("target_confidence"),
                    "threshold_crossers": ni_summary.get("threshold_crossers"),
                    "direct_tablets": ni_summary.get("direct_tablets"),
                    "cascade_tablets": ni_summary.get("cascade_tablets"),
                },
                "next_actions": [
                    "Refresh the admin queue against the NI threshold crossers and lock the week-2 admin slate.",
                    "Prefer KH/HT/ZA/PH crossers that convert directly into connected administrative readings.",
                ],
            }
        )

    if queue_summary.get("queue_size", 0) > 0:
        opportunities.append(
            {
                "id": "queue_driven_admin_burst",
                "priority": "immediate",
                "summary": "Use the existing queue as the primary admin throughput engine instead of reopening broad hypothesis work.",
                "evidence": {
                    "queue_size": queue_summary.get("queue_size"),
                    "top_ten_site_counts": queue_summary.get("top_ten_site_counts"),
                    "ht_share_top_ten": queue_summary.get("ht_share_top_ten"),
                    "top_targets": [
                        item.get("tablet_id") for item in queue_summary.get("top_ten", [])[:5]
                    ],
                },
                "next_actions": [
                    "Split the top queue into fast structural wins and NI-enabled cascade wins.",
                    "Keep at least four of the next admin readings outside the HT cluster.",
                ],
            }
        )

    if i_pi_na_ma_decision and i_pi_na_ma_decision.get("decision") == "HOLD":
        opportunities.append(
            {
                "id": "ritual_hold_discipline",
                "priority": "medium",
                "summary": "Keep I-PI-NA-MA in a bounded evidence hunt rather than broad ritual promotion work.",
                "evidence": {
                    "decision": i_pi_na_ma_decision.get("decision"),
                    "failed_required": i_pi_na_ma_decision.get("failed_required"),
                    "cross_corpus_evidence": i_pi_na_ma_decision.get("cross_corpus_evidence"),
                },
                "next_actions": [
                    "Limit ritual work to formula-rich contexts and template-level sentence claims.",
                    "Only reopen promotion if new non-outlier evidence improves cross-corpus consistency.",
                ],
            }
        )

    if sprint_summary is not None:
        opportunities.append(
            {
                "id": "orchestrated_execution_ready",
                "priority": "supporting",
                "summary": "The repo already has an executable sprint platform; keep the next cycle inside that workflow.",
                "evidence": {
                    "latest_sprint_lane_status": sprint_summary.get("lane_status"),
                    "latest_sprint_lanes": sprint_summary.get("lane_ids"),
                    "status_counts": sprint_summary.get("status_counts"),
                },
                "next_actions": [
                    "Run the project review in lane A before each weekly queue lock.",
                    "Keep promotion, queue, and canonical docs attached to the sprint cadence rather than ad hoc notes.",
                ],
            }
        )

    return opportunities


def build_streams(
    *,
    execution_review: dict[str, Any],
    queue_summary: dict[str, Any],
    cascade_summary: dict[str, Any],
    ni_decision: dict[str, Any] | None,
    i_pi_na_ma_decision: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    top_queue = [item.get("tablet_id") for item in queue_summary.get("top_ten", [])[:10]]
    threshold_crossers = [
        item.get("tablet_id") for item in cascade_summary.get("top_threshold_crossers", [])[:10]
    ]
    next_window = execution_review.get("next_window", {})
    execution_slates = (
        next_window.get("execution_slates", {}) if isinstance(next_window, dict) else {}
    )
    admin_primary = (
        execution_slates.get("admin_primary", []) if isinstance(execution_slates, dict) else []
    )
    admin_reserve = (
        execution_slates.get("admin_reserve", []) if isinstance(execution_slates, dict) else []
    )
    ritual_primary = (
        execution_slates.get("ritual_primary", []) if isinstance(execution_slates, dict) else []
    )
    breakthrough_targets = (
        execution_slates.get("breakthrough_micro_studies", [])
        if isinstance(execution_slates, dict)
        else []
    )
    kh_targets = [
        tablet
        for tablet in admin_primary + admin_reserve
        if isinstance(tablet, str) and tablet.startswith("KH")
    ]
    return [
        {
            "stream_id": "S1",
            "name": "Administrative Cascade Exploitation",
            "priority": "immediate",
            "owners": ["E", "F", "LEAD"],
            "objective": "Convert the approved NI anchor into new connected administrative readings.",
            "targets": admin_primary or (top_queue[:5] + threshold_crossers[:5]),
            "dependencies": [
                "NI promotion decision",
                "reading_queue.json",
                "ni_cascade_report.json",
            ],
            "guardrails": [
                "Maintain site balancing.",
                "Attach arithmetic and dependency notes to each reading.",
            ],
            "evidence": {
                "ni_decision": ni_decision.get("decision") if ni_decision else None,
                "threshold_crossers": cascade_summary.get("summary", {}).get("threshold_crossers"),
            },
        },
        {
            "stream_id": "S2",
            "name": "KH Administrative Formalization",
            "priority": "high",
            "owners": ["C", "F"],
            "objective": "Turn KH versus HT accounting differences into a reusable admin model.",
            "targets": kh_targets
            or [tablet for tablet in top_queue if tablet and tablet.startswith("KH")]
            or ["KH15", "KH25", "KH54"],
            "dependencies": ["KH readings", "sign-function blockers", "CYP grading memo"],
            "guardrails": [
                "Resolve only those sign issues that block active KH readings.",
                "Do not reopen general sign campaigns without queue pressure.",
            ],
            "evidence": {
                "kh_queue_items": [
                    tablet for tablet in top_queue if tablet and tablet.startswith("KH")
                ],
                "focus": "CYP grading, zero-K-R structure, KH/HT contrasts",
            },
        },
        {
            "stream_id": "S3",
            "name": "Ritual Register Evidence Hunt",
            "priority": "medium",
            "owners": ["B", "D", "G"],
            "objective": "Deepen ritual/template understanding without overrunning the evidence floor.",
            "targets": ritual_primary or ["IO", "PK", "SY", "I-PI-NA-MA evidence review"],
            "dependencies": [
                "promotion_board_runner.py",
                "negative_evidence.py",
                "contextual ritual readings",
            ],
            "guardrails": [
                "Keep I-PI-NA-MA on HOLD until cross-corpus consistency improves.",
                "Publish ritual outputs as template-level unless promotion gates change.",
            ],
            "evidence": {
                "i_pi_na_ma_decision": i_pi_na_ma_decision.get("decision")
                if i_pi_na_ma_decision
                else None,
                "failed_required": i_pi_na_ma_decision.get("failed_required")
                if i_pi_na_ma_decision
                else [],
            },
        },
        {
            "stream_id": "S4",
            "name": "Bounded Breakthrough Hunting",
            "priority": "medium",
            "owners": ["C", "D", "G"],
            "objective": "Run tightly bounded micro-studies for breakthrough candidates without derailing core work.",
            "targets": breakthrough_targets
            or ["KA-NA prefix alternations", "*304 or *21F/*21M blocker"],
            "dependencies": [
                "active ritual/admin slate",
                "sign-function blockers",
                "lane B validation",
            ],
            "guardrails": [
                "Maximum two micro-studies for the remainder of Month 1.",
                "Conclude each study with strengthen/hold/discard output.",
            ],
            "evidence": {
                "micro_studies_planned": len(breakthrough_targets) if breakthrough_targets else 2,
                "speculation_mode": execution_review.get("profile", {}).get("speculation_policy"),
            },
        },
        {
            "stream_id": "S5",
            "name": "Governance and Promotion Discipline",
            "priority": "high",
            "owners": ["A", "B", "LEAD"],
            "objective": "Keep sprint decisions bound to current artifacts, validators, and canonical docs.",
            "targets": [
                "MASTER_STATE.md",
                "KNOWLEDGE.md",
                "ANALYSIS_INDEX.md",
                "promotion packets",
            ],
            "dependencies": [
                "sprint_orchestrator.py",
                "lane_orchestrator.py",
                "project_acceleration_review.py",
            ],
            "guardrails": [
                "No promotion without a packet-backed decision.",
                "Canonical docs must reflect the latest lane-B outcomes.",
            ],
            "evidence": {
                "review_tooling": "present",
                "latest_queue_size": queue_summary.get("queue_size"),
            },
        },
    ]


def render_markdown(report: dict[str, Any], json_path: Path) -> str:
    snapshot = report["project_snapshot"]
    platform = report["platform_review"]
    execution = report["execution_review"]
    queue = report["queue_review"]
    cascade = report["cascade_review"]
    promotions = report["promotion_review"]
    opportunities = report["opportunities"]
    streams = report["streams"]
    capacity_split = execution.get("profile", {}).get("capacity_split", {})
    next_window = execution.get("next_window", {})
    next_slates = next_window.get("execution_slates", {}) if isinstance(next_window, dict) else {}

    lines = [
        "# Project Acceleration Review",
        "",
        f"**Date**: {report['metadata']['generated_utc'][:10]}  ",
        f"**Artifact**: `{json_path}`",
        "",
        "## Snapshot",
        "",
        f"- Python tools: `{snapshot['tool_inventory']['python_tool_count']}`",
        f"- Connected readings: `{snapshot['connected_readings']['tablet_readings']}` tablets + `{snapshot['connected_readings']['thematic_analyses']}` thematic across `{snapshot['connected_readings']['sites']}` sites",
        f"- Active lanes in manifest: `{platform['lane_count']}`",
        f"- Sprint agents in manifest: `{platform['agent_count']}`",
        f"- Latest sprint lane status: `{platform['latest_sprint']['lane_status'] if platform['latest_sprint'] else 'unknown'}`",
        "",
        "## Execution Profile",
        "",
        f"- Mode: `{execution.get('profile', {}).get('mode', 'unknown')}`",
        f"- Capacity split: `{capacity_split.get('admin_translation_pct', 0)}/{capacity_split.get('ritual_register_pct', 0)}/{capacity_split.get('breakthrough_hunting_pct', 0)}`",
        f"- Speculation policy: `{execution.get('profile', {}).get('speculation_policy', 'unknown')}`",
        f"- Next window: `{next_window.get('label', 'unknown')}`",
        f"- Admin primary slate: `{', '.join(next_slates.get('admin_primary', [])[:6])}`",
        f"- Ritual primary slate: `{', '.join(next_slates.get('ritual_primary', [])[:4])}`",
        "",
        "## Current Signals",
        "",
        f"- `NI`: `{promotions['NI']['decision'] if promotions['NI'] else 'unknown'}` ({promotions['NI']['target_confidence'] if promotions['NI'] else 'n/a'})",
        f"- `I-PI-NA-MA`: `{promotions['I-PI-NA-MA']['decision'] if promotions['I-PI-NA-MA'] else 'unknown'}`",
        f"- Queue top 5: `{', '.join(item['tablet_id'] for item in queue['top_ten'][:5] if item.get('tablet_id'))}`",
        f"- NI cascade: `{cascade['summary'].get('direct_tablets', 0)}` direct, `{cascade['summary'].get('cascade_tablets', 0)}` transitive, `{cascade['summary'].get('threshold_crossers', 0)}` threshold crossers",
        "",
        "## Opportunity Areas",
        "",
    ]
    for idx, item in enumerate(opportunities, start=1):
        lines.append(f"{idx}. **{item['id']}** — {item['summary']}")

    lines.extend(
        [
            "",
            "## Multi-Stream Plan",
            "",
        ]
    )
    for stream in streams:
        lines.append(f"### {stream['stream_id']} — {stream['name']}")
        lines.append("")
        lines.append(f"- Owners: `{', '.join(stream['owners'])}`")
        lines.append(f"- Objective: {stream['objective']}")
        lines.append(f"- Targets: `{', '.join(stream['targets'])}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def build_report() -> dict[str, Any]:
    knowledge_text = load_text(DOCS_DIR / "KNOWLEDGE.md")
    master_state_text = load_text(DOCS_DIR / "MASTER_STATE.md")
    analysis_index_text = load_text(DOCS_DIR / "ANALYSIS_INDEX.md")
    knowledge_rows = parse_markdown_table(knowledge_text)
    lane_manifest = load_manifest(LANE_MANIFEST)
    sprint_manifest = load_manifest(SPRINT_MANIFEST)
    execution_review = summarize_execution_review(sprint_manifest)

    queue_summary = summarize_queue(load_json(DATA_DIR / "reading_queue.json"))
    cascade_summary = summarize_cascade(load_json(DATA_DIR / "ni_cascade_report.json"))
    promotion_data = load_json(DATA_DIR / "promotion_decisions.json") or {}
    decision_rows = promotion_data.get("decisions", []) if isinstance(promotion_data, dict) else []

    ni_decision = summarize_decision(latest_decision(decision_rows, "NI"))
    i_pi_na_ma_decision = summarize_decision(latest_decision(decision_rows, "I-PI-NA-MA"))
    sprint_summary = latest_sprint_report()

    report = {
        "metadata": {
            "generated_utc": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat()
            .replace("+00:00", "Z"),
            "tool": "project_acceleration_review.py",
            "purpose": "Whole-project review for data-informed decipherment planning",
        },
        "sources": {
            "knowledge": str(DOCS_DIR / "KNOWLEDGE.md"),
            "master_state": str(DOCS_DIR / "MASTER_STATE.md"),
            "analysis_index": str(DOCS_DIR / "ANALYSIS_INDEX.md"),
            "lane_manifest": str(LANE_MANIFEST),
            "sprint_manifest": str(SPRINT_MANIFEST),
            "reading_queue": str(DATA_DIR / "reading_queue.json"),
            "ni_cascade_report": str(DATA_DIR / "ni_cascade_report.json"),
            "promotion_decisions": str(DATA_DIR / "promotion_decisions.json"),
        },
        "project_snapshot": {
            "knowledge_last_updated": parse_last_updated(knowledge_text),
            "master_state_last_updated": parse_last_updated(master_state_text),
            "analysis_index_last_updated": parse_last_updated(analysis_index_text),
            "connected_readings": extract_connected_reading_snapshot(knowledge_rows),
            "tool_inventory": {
                "python_tool_count": len(list(TOOLS_DIR.glob("*.py"))),
                "knowledge_declared_tool_count": extract_tool_count(knowledge_rows),
                "core_toolchains": extract_toolchains(),
            },
        },
        "platform_review": {
            "lane_count": len(lane_manifest.get("lanes", [])),
            "lane_ids": [
                lane.get("lane_id")
                for lane in lane_manifest.get("lanes", [])
                if isinstance(lane, dict)
            ],
            "agent_count": len(sprint_manifest.get("agents", [])),
            "latest_sprint": sprint_summary,
        },
        "execution_review": execution_review,
        "queue_review": queue_summary,
        "cascade_review": cascade_summary,
        "promotion_review": {
            "NI": ni_decision,
            "I-PI-NA-MA": i_pi_na_ma_decision,
        },
    }
    report["opportunities"] = build_opportunities(
        queue_summary=queue_summary,
        cascade_summary=cascade_summary,
        ni_decision=ni_decision,
        i_pi_na_ma_decision=i_pi_na_ma_decision,
        sprint_summary=sprint_summary,
    )
    report["streams"] = build_streams(
        execution_review=execution_review,
        queue_summary=queue_summary,
        cascade_summary=cascade_summary,
        ni_decision=ni_decision,
        i_pi_na_ma_decision=i_pi_na_ma_decision,
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a data-informed project acceleration review."
    )
    parser.add_argument(
        "--output-json",
        default=str(DEFAULT_JSON_OUTPUT),
        help="Path for the machine-readable JSON review output.",
    )
    parser.add_argument(
        "--markdown-out",
        help="Optional path for a Markdown summary.",
    )
    args = parser.parse_args()

    json_path = Path(args.output_json).resolve()
    report = build_report()
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.markdown_out:
        markdown_path = Path(args.markdown_out).resolve()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(render_markdown(report, json_path), encoding="utf-8")

    print(f"Project acceleration review written to {json_path}")
    if args.markdown_out:
        print(f"Markdown summary written to {Path(args.markdown_out).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
