#!/usr/bin/env python3
"""
Dependency Trace Resolver for Linear A promotion workflow.

Purpose:
1. Pre-check dependency-trace completeness before promotion runs.
2. Optionally write provisional dependency entries for resolvable gaps.

Usage:
    python3 tools/dependency_trace_resolver.py --top 25
    python3 tools/dependency_trace_resolver.py --candidates "KU-RO,*411-VS"
    python3 tools/dependency_trace_resolver.py --top 10 --write
    python3 tools/dependency_trace_resolver.py --top 25 --strict
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DEFAULT_INTEGRATED = DATA_DIR / "integrated_results.json"
DEFAULT_DEPENDENCIES = DATA_DIR / "reading_dependencies.json"
DEFAULT_ANCHORS = DATA_DIR / "anchors.json"
DEFAULT_OUTPUT = DATA_DIR / "dependency_trace_report.json"

HYPOTHESIS_TO_ANCHORS = {
    "luwian": ["anchor_luwian_morphology"],
    "semitic": ["anchor_semitic_loan_layer"],
    "pregreek": ["anchor_toponym_phaistos"],
    "protogreek": ["anchor_linear_b_comparison"],
}
PROVISIONAL_MARKER = "dependency_trace_resolver.py --write"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(f"Missing required file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON: {path}: {exc}") from exc


def normalize_hypothesis(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    cleaned = value.strip().lower()
    aliases = {
        "luwian/anatolian": "luwian",
        "semitic (west semitic/akkadian)": "semitic",
        "pre-greek": "pregreek",
        "proto-greek": "protogreek",
    }
    return aliases.get(cleaned, cleaned or "unknown")


def parse_candidate_list(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def pick_candidates(
    integrated_rows: list[dict[str, Any]],
    *,
    explicit: list[str] | None,
    top: int,
    non_compliant_only: bool,
) -> list[dict[str, Any]]:
    if explicit:
        wanted = {item.casefold() for item in explicit}
        selected = [
            row
            for row in integrated_rows
            if isinstance(row.get("word"), str) and row["word"].casefold() in wanted
        ]
        # Preserve explicit order
        by_word = {row["word"].casefold(): row for row in selected}
        ordered = []
        for word in explicit:
            row = by_word.get(word.casefold())
            if row:
                ordered.append(row)
        return ordered

    rows = integrated_rows
    if non_compliant_only:
        rows = [row for row in rows if not bool(row.get("methodology_compliant"))]

    rows = sorted(
        rows,
        key=lambda row: (
            -(int(row.get("frequency", 0) or 0)),
            str(row.get("word", "")),
        ),
    )
    return rows[:top]


def classify_candidate(
    row: dict[str, Any],
    readings: dict[str, Any],
    anchors: dict[str, Any],
) -> dict[str, Any]:
    word = str(row.get("word", ""))
    best_hypothesis = normalize_hypothesis(row.get("raw_best_hypothesis"))
    entry = readings.get(word)
    depends_on = []
    evidence_sources: list[str] = []
    if isinstance(entry, dict):
        depends_on = entry.get("depends_on", [])
        raw_sources = entry.get("evidence_sources", [])
        if isinstance(raw_sources, list):
            evidence_sources = [str(item) for item in raw_sources]
    if not isinstance(depends_on, list):
        depends_on = []

    missing_anchor_refs = [dep for dep in depends_on if dep not in anchors]
    has_valid_trace = bool(depends_on) and not missing_anchor_refs

    suggested = [dep for dep in HYPOTHESIS_TO_ANCHORS.get(best_hypothesis, []) if dep in anchors]
    resolvable = (not has_valid_trace) and bool(suggested)

    if has_valid_trace:
        status = "complete"
        trace_source = "provisional" if PROVISIONAL_MARKER in evidence_sources else "existing"
    elif resolvable:
        status = "resolvable"
        trace_source = "none"
    else:
        status = "unresolved"
        trace_source = "none"

    return {
        "word": word,
        "frequency": int(row.get("frequency", 0) or 0),
        "best_hypothesis": best_hypothesis,
        "existing_depends_on": depends_on,
        "missing_anchor_refs": missing_anchor_refs,
        "status": status,
        "trace_source": trace_source,
        "suggested_depends_on": suggested,
        "methodology_compliant": bool(row.get("methodology_compliant")),
        "threshold_category": row.get("threshold_category"),
        "final_confidence": row.get("final_confidence"),
    }


def apply_resolution(
    classification: dict[str, Any],
    readings: dict[str, Any],
) -> bool:
    if classification["status"] != "resolvable":
        return False
    word = classification["word"]
    suggested = classification["suggested_depends_on"]
    if not suggested:
        return False

    existing = readings.get(word)
    if not isinstance(existing, dict):
        existing = {
            "meaning": "provisional mapping from dependency resolver",
            "confidence": classification.get("final_confidence") or "SPECULATIVE",
            "max_confidence": "PROBABLE",
            "supports": [],
            "evidence_sources": [],
            "cascade_note": "",
        }

    existing["depends_on"] = suggested
    existing["cascade_note"] = (
        "Provisional dependency mapping auto-generated by dependency_trace_resolver.py"
    )
    sources = existing.get("evidence_sources", [])
    if not isinstance(sources, list):
        sources = []
    if PROVISIONAL_MARKER not in sources:
        sources.append(PROVISIONAL_MARKER)
    existing["evidence_sources"] = sources
    readings[word] = existing
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pre-check dependency-trace completeness for promotions"
    )
    parser.add_argument(
        "--candidates",
        help="Comma-separated word list to check (default: auto-pick from integrated results)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Number of auto-picked candidates (default: 20)",
    )
    parser.add_argument(
        "--include-compliant",
        action="store_true",
        help="Include methodology-compliant rows in auto-pick mode",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write provisional dependency mappings for resolvable candidates",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when unresolved candidates remain",
    )
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Exit non-zero unless every checked candidate has existing complete trace",
    )
    parser.add_argument(
        "--integrated",
        default=str(DEFAULT_INTEGRATED),
        help="Path to integrated results JSON",
    )
    parser.add_argument(
        "--dependencies",
        default=str(DEFAULT_DEPENDENCIES),
        help="Path to reading dependencies JSON",
    )
    parser.add_argument(
        "--anchors",
        default=str(DEFAULT_ANCHORS),
        help="Path to anchors JSON",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output report JSON path",
    )
    args = parser.parse_args()

    if args.top <= 0:
        print("Error: --top must be > 0")
        return 2

    integrated = load_json(Path(args.integrated).expanduser().resolve())
    dependency_obj = load_json(Path(args.dependencies).expanduser().resolve())
    anchor_obj = load_json(Path(args.anchors).expanduser().resolve())

    integrated_rows = integrated.get("all_results", [])
    if not isinstance(integrated_rows, list):
        raise RuntimeError("integrated_results.json missing all_results list")

    readings = dependency_obj.setdefault("readings", {})
    anchors = anchor_obj.get("anchors", {})
    if not isinstance(readings, dict) or not isinstance(anchors, dict):
        raise RuntimeError("Invalid readings/anchors schema")

    explicit = parse_candidate_list(args.candidates) if args.candidates else None
    candidates = pick_candidates(
        integrated_rows,
        explicit=explicit,
        top=args.top,
        non_compliant_only=not args.include_compliant,
    )

    checks = [classify_candidate(row, readings, anchors) for row in candidates]

    write_count = 0
    if args.write:
        for check in checks:
            if apply_resolution(check, readings):
                write_count += 1
        # Re-classify after writes for final status
        checks = [classify_candidate(row, readings, anchors) for row in candidates]
        dependency_obj.setdefault("metadata", {})
        dependency_obj["metadata"]["dependency_trace_resolver_last_run"] = datetime.now(
            timezone.utc
        ).isoformat()
        Path(args.dependencies).expanduser().resolve().write_text(
            json.dumps(dependency_obj, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    summary = {
        "total_checked": len(checks),
        "complete": sum(1 for c in checks if c["status"] == "complete"),
        "resolvable": sum(1 for c in checks if c["status"] == "resolvable"),
        "unresolved": sum(1 for c in checks if c["status"] == "unresolved"),
        "trace_sources": {
            "existing": sum(1 for c in checks if c.get("trace_source") == "existing"),
            "provisional": sum(1 for c in checks if c.get("trace_source") == "provisional"),
            "none": sum(1 for c in checks if c.get("trace_source") == "none"),
        },
        "write_count": write_count,
    }
    summary["incomplete"] = summary["total_checked"] - summary["complete"]

    report = {
        "metadata": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "method": "dependency trace pre-check",
            "write_mode": args.write,
            "strict_mode": args.strict,
            "require_complete": args.require_complete,
            "input_files": {
                "integrated": str(Path(args.integrated).expanduser().resolve()),
                "dependencies": str(Path(args.dependencies).expanduser().resolve()),
                "anchors": str(Path(args.anchors).expanduser().resolve()),
            },
        },
        "summary": summary,
        "checks": checks,
        "resolvable_candidates": [c for c in checks if c["status"] == "resolvable"],
        "unresolved_candidates": [c for c in checks if c["status"] == "unresolved"],
        "missing_trace_candidates": [c for c in checks if c.get("trace_source") == "none"],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("=" * 60)
    print("DEPENDENCY TRACE RESOLVER")
    print("=" * 60)
    print(f"Checked: {summary['total_checked']}")
    print(f"Complete: {summary['complete']}")
    print(f"Resolvable: {summary['resolvable']}")
    print(f"Unresolved: {summary['unresolved']}")
    print(f"Incomplete: {summary['incomplete']}")
    print(
        "Trace sources: "
        f"existing={summary['trace_sources']['existing']}, "
        f"provisional={summary['trace_sources']['provisional']}, "
        f"none={summary['trace_sources']['none']}"
    )
    if args.write:
        print(f"Writes applied: {summary['write_count']}")
        print(f"Updated dependencies: {Path(args.dependencies).expanduser().resolve()}")
    print(f"Report: {output_path}")

    if args.strict and summary["unresolved"] > 0:
        return 1
    if args.require_complete and (
        summary["incomplete"] > 0
        or summary["trace_sources"]["provisional"] > 0
        or summary["trace_sources"]["none"] > 0
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
