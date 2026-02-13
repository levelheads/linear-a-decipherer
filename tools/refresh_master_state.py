#!/usr/bin/env python3
"""
Refresh MASTER_STATE.md metrics from generated artifacts.

Usage:
    python tools/refresh_master_state.py --check
    python tools/refresh_master_state.py --write
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TOOLS_DIR = PROJECT_ROOT / "tools"
MASTER_STATE = PROJECT_ROOT / "linear-a-decipherer" / "MASTER_STATE.md"
CITATION = PROJECT_ROOT / "CITATION.cff"


ROW_RE = re.compile(
    r"^\|\s*(?P<metric>[^|]+?)\s*\|\s*(?P<value>.*?)\s*\|\s*(?P<source>.*?)\s*\|$"
)


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def to_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if cleaned.isdigit():
            return int(cleaned)
    return default


def to_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip().replace("%", "").replace(",", "")
        try:
            return float(cleaned)
        except ValueError:
            return default
    return default


def format_pct(value: float) -> str:
    return f"{value:.2f}%"


def parse_citation_version() -> str | None:
    if not CITATION.exists():
        return None
    content = CITATION.read_text(encoding="utf-8")
    match = re.search(r'^version:\s*"?([^"\n]+)"?\s*$', content, re.MULTILINE)
    if not match:
        return None
    version = match.group(1).strip()
    return f"v{version}" if not version.startswith("v") else version


def parse_generated_date(data: dict[str, Any] | None) -> str | None:
    if not data:
        return None
    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        return None
    generated = metadata.get("generated")
    if not isinstance(generated, str):
        return None
    return generated.split("T", 1)[0]


def corpus_inscription_count(corpus_data: dict[str, Any] | None) -> int | None:
    if not corpus_data:
        return None
    inscriptions = corpus_data.get("inscriptions")
    if isinstance(inscriptions, dict):
        return len(inscriptions)
    if isinstance(inscriptions, list):
        return len(inscriptions)
    if isinstance(corpus_data, dict):
        return len(corpus_data)
    return None


def build_metric_updates() -> dict[str, tuple[str, str | None]]:
    updates: dict[str, tuple[str, str | None]] = {}

    corpus = load_json(DATA_DIR / "corpus.json")
    corpus_total = corpus_inscription_count(corpus)
    if corpus_total is not None:
        updates["Total corpus inscriptions"] = (f"{corpus_total:,}", None)

    extended = load_json(DATA_DIR / "extended_corpus_analysis.json")
    if extended:
        coverage = extended.get("coverage", {})
        analyzed = to_int(coverage.get("batch_analyzed"), 0)
        total = to_int(coverage.get("total_corpus"), corpus_total or 0)
        if analyzed <= 0:
            analyzed = len(extended.get("inscriptions_analyzed", []))
        if total <= 0 and corpus_total:
            total = corpus_total
        percent = to_float(coverage.get("coverage_percent"), 0.0)
        if percent <= 0 and total > 0:
            percent = (analyzed / total) * 100
        if analyzed > 0 and total > 0:
            updates["Batch analysis coverage"] = (
                f"{analyzed:,}/{total:,} ({format_pct(percent)})",
                None,
            )

    hypothesis = load_json(DATA_DIR / "hypothesis_results.json")
    if hypothesis:
        word_analyses = hypothesis.get("word_analyses", {})
        word_count = len(word_analyses) if isinstance(word_analyses, dict) else 0
        metadata = hypothesis.get("metadata", {})
        if word_count == 0:
            word_count = to_int(metadata.get("words_tested"), 0)
        min_freq = metadata.get("min_frequency")
        if word_count > 0:
            if isinstance(min_freq, int):
                value = f"{word_count} words (freq >= {min_freq})"
            else:
                value = f"{word_count} words"
            updates["Hypothesis run word set"] = (value, None)

    batch = load_json(DATA_DIR / "batch_analysis_results.json")
    if batch:
        summary = batch.get("summary", {})
        words_analyzed = to_int(summary.get("total_words_analyzed"), 0)
        high_conf = to_int(summary.get("high_confidence"), 0)
        if words_analyzed <= 0:
            pipeline_stats = batch.get("pipeline_stats", {})
            words_analyzed = to_int(pipeline_stats.get("words_analyzed"), 0)
        if high_conf <= 0:
            high_conf = len(batch.get("high_confidence_findings", []))
        if words_analyzed > 0:
            updates["Batch pipeline word set"] = (f"{words_analyzed:,} words", None)
        if high_conf > 0:
            updates["High-confidence batch words"] = (f"{high_conf:,}", None)

    integrated_path = DATA_DIR / "integrated_results.json"
    integrated = load_json(integrated_path)
    if integrated is None:
        integrated_path = DATA_DIR / "integrated_results_current.json"
        integrated = load_json(integrated_path)
    if integrated:
        summary = integrated.get("summary", {})
        all_results = integrated.get("all_results", [])
        total_validated = len(all_results) if isinstance(all_results, list) else 0
        if total_validated == 0:
            total_validated = to_int(summary.get("methodology_compliant"), 0) + to_int(
                summary.get("non_compliant"), 0
            )
        compliant = to_int(summary.get("methodology_compliant"), 0)
        compliance_rate = to_float(summary.get("compliance_rate"), -1.0)
        if compliance_rate < 0 and total_validated > 0:
            compliance_rate = (compliant / total_validated) * 100
        source_run_date = parse_generated_date(integrated)
        source = f"`data/{integrated_path.name}`"
        if source_run_date:
            source += f" (run {source_run_date})"
        if total_validated > 0:
            updates["Integrated validated words"] = (f"{total_validated:,}", source)
            updates["Methodology compliance"] = (
                f"{compliant:,}/{total_validated:,} ({compliance_rate:.1f}%)",
                source,
            )

    validation = load_json(DATA_DIR / "validation_report.json")
    if validation:
        summary = validation.get("summary", {})
        critical = to_int(summary.get("critical_errors"), 0)
        warnings = to_int(summary.get("warnings"), 0)
        if critical == 0:
            status = f"PASS with {warnings} warnings, {critical} critical errors"
        else:
            status = f"FAIL with {warnings} warnings, {critical} critical errors"
        updates["Corpus validation status"] = (status, None)

    updates["Tool count (Python scripts)"] = (
        f"{len(list(TOOLS_DIR.glob('*.py'))):,}",
        None,
    )

    citation_version = parse_citation_version()
    if citation_version:
        updates["Current release version"] = (citation_version, None)

    return updates


def update_last_updated(content: str) -> tuple[str, bool]:
    replacement = f"**Last Updated**: {date.today().isoformat()}"
    updated = re.sub(
        r"^\*\*Last Updated\*\*:\s*.*$",
        replacement,
        content,
        count=1,
        flags=re.MULTILINE,
    )
    return updated, updated != content


def apply_metric_updates(
    content: str, updates: dict[str, tuple[str, str | None]]
) -> tuple[str, list[str]]:
    lines = content.splitlines()
    in_metrics = False
    changed_metrics: list[str] = []

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "## Metrics Snapshot":
            in_metrics = True
            continue
        if in_metrics and stripped == "---":
            in_metrics = False
            continue
        if not in_metrics:
            continue

        match = ROW_RE.match(line)
        if not match:
            continue
        metric = match.group("metric").strip()
        if metric not in updates:
            continue

        new_value, new_source = updates[metric]
        existing_source = match.group("source").strip()
        final_source = new_source if new_source is not None else existing_source
        new_line = f"| {metric} | {new_value} | {final_source} |"
        if new_line != line:
            lines[idx] = new_line
            changed_metrics.append(metric)

    rendered = "\n".join(lines)
    if content.endswith("\n"):
        rendered += "\n"
    return rendered, changed_metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh metrics in MASTER_STATE.md")
    parser.add_argument("--write", action="store_true", help="Write updates to disk")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if MASTER_STATE.md is out of date",
    )
    args = parser.parse_args()

    if not MASTER_STATE.exists():
        print(f"FAILED: missing {MASTER_STATE}")
        return 1

    content = MASTER_STATE.read_text(encoding="utf-8")
    updates = build_metric_updates()
    content2, changed_metrics = apply_metric_updates(content, updates)
    content3, changed_date = update_last_updated(content2)

    changed = (content3 != content)

    print("=" * 60)
    print("MASTER STATE REFRESH")
    print("=" * 60)
    if changed_metrics:
        print("Metrics updated:")
        for metric in changed_metrics:
            print(f"  - {metric}")
    if changed_date and not changed_metrics:
        print("Only Last Updated date changed.")
    if not changed:
        print("No changes required.")

    if args.write and changed:
        MASTER_STATE.write_text(content3, encoding="utf-8")
        print(f"Wrote updates to {MASTER_STATE}")

    if args.check and changed:
        print("CHECK FAILED: MASTER_STATE.md is out of date.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
