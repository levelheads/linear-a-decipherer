#!/usr/bin/env python3
"""
Tool Parity Checker for Linear A

Compares major analysis artifacts to detect metric drift and schema/logic
inconsistencies across the hypothesis, batch, and integrated pipelines.

Usage:
    python tools/tool_parity_checker.py
    python tools/tool_parity_checker.py --threshold-delta 12
    python tools/tool_parity_checker.py --output data/tool_parity_report.json
    python tools/tool_parity_checker.py --inputs a.json b.json c.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

DEFAULT_INPUTS = [
    str(DATA_DIR / "hypothesis_results.json"),
    str(DATA_DIR / "batch_analysis_results.json"),
    str(DATA_DIR / "integrated_results.json"),
]

HYPOTHESES = ("luwian", "semitic", "pregreek", "protogreek")


@dataclass
class ToolSummary:
    name: str
    path: str
    generated: str | None
    words_considered: int
    best_hypothesis_counts: dict[str, int]
    best_hypothesis_pct: dict[str, float]
    confidence_counts: dict[str, int]


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Missing input artifact: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc


def _round(value: float, digits: int = 2) -> float:
    return round(float(value), digits)


def _normalize_hypothesis(value: Any) -> str:
    if not isinstance(value, str):
        return "unknown"
    cleaned = value.strip().lower()
    mapping = {
        "luwian/anatolian": "luwian",
        "anatolian": "luwian",
        "semitic (west semitic/akkadian)": "semitic",
        "pre-greek": "pregreek",
        "proto-greek": "protogreek",
    }
    return mapping.get(cleaned, cleaned or "unknown")


def _pct(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return _round((count / total) * 100.0, 2)


def _as_confidence(value: Any) -> str:
    if not isinstance(value, str):
        return "UNKNOWN"
    return value.strip().upper() or "UNKNOWN"


def summarize_hypothesis_results(path: Path, payload: dict[str, Any]) -> ToolSummary:
    metadata = payload.get("metadata", {})
    word_analyses = payload.get("word_analyses", {})
    total_words = len(word_analyses) if isinstance(word_analyses, dict) else 0
    if total_words == 0:
        total_words = int(metadata.get("words_tested", 0) or 0)

    support_counts: dict[str, int] = {}
    summaries = payload.get("hypothesis_summaries", {})
    for hypothesis in HYPOTHESES:
        hypothesis_data = summaries.get(hypothesis, {})
        support_counts[hypothesis] = int(hypothesis_data.get("supported", 0) or 0)

    confidence_counts: dict[str, int] = {}
    if isinstance(word_analyses, dict):
        for row in word_analyses.values():
            synthesis = row.get("synthesis", {})
            confidence = _as_confidence(synthesis.get("max_confidence"))
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1

    best_pct = {h: _pct(support_counts.get(h, 0), total_words) for h in HYPOTHESES}
    return ToolSummary(
        name="hypothesis_results",
        path=str(path),
        generated=metadata.get("generated"),
        words_considered=total_words,
        best_hypothesis_counts=support_counts,
        best_hypothesis_pct=best_pct,
        confidence_counts=dict(sorted(confidence_counts.items())),
    )


def summarize_batch_results(path: Path, payload: dict[str, Any]) -> ToolSummary:
    summary = payload.get("summary", {})
    total_words = int(summary.get("total_words_analyzed", 0) or 0)

    rankings = payload.get("hypothesis_rankings", {})
    support_counts: dict[str, int] = {}
    for hypothesis in HYPOTHESES:
        row = rankings.get(hypothesis, {})
        support_counts[hypothesis] = int(row.get("words_supporting", 0) or 0)

    confidence_counts: dict[str, int] = {}
    for key in ("high_confidence_findings", "medium_confidence_findings", "needs_review"):
        rows = payload.get(key, [])
        if not isinstance(rows, list):
            continue
        for row in rows:
            confidence = _as_confidence(row.get("confidence"))
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1

    best_pct = {h: _pct(support_counts.get(h, 0), total_words) for h in HYPOTHESES}
    return ToolSummary(
        name="batch_analysis_results",
        path=str(path),
        generated=payload.get("generated"),
        words_considered=total_words,
        best_hypothesis_counts=support_counts,
        best_hypothesis_pct=best_pct,
        confidence_counts=dict(sorted(confidence_counts.items())),
    )


def summarize_integrated_results(path: Path, payload: dict[str, Any]) -> ToolSummary:
    metadata = payload.get("metadata", {})
    all_results = payload.get("all_results", [])
    total_words = int(metadata.get("words_validated", 0) or 0)
    if total_words == 0 and isinstance(all_results, list):
        total_words = len(all_results)

    support_counts = {h: 0 for h in HYPOTHESES}
    confidence_counts: dict[str, int] = {}

    if isinstance(all_results, list):
        for row in all_results:
            best = _normalize_hypothesis(row.get("raw_best_hypothesis"))
            if best in support_counts:
                support_counts[best] += 1
            confidence = _as_confidence(row.get("final_confidence"))
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1

    best_pct = {h: _pct(support_counts.get(h, 0), total_words) for h in HYPOTHESES}
    return ToolSummary(
        name="integrated_results",
        path=str(path),
        generated=metadata.get("generated"),
        words_considered=total_words,
        best_hypothesis_counts=support_counts,
        best_hypothesis_pct=best_pct,
        confidence_counts=dict(sorted(confidence_counts.items())),
    )


def build_word_best_map_hypothesis(payload: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    word_analyses = payload.get("word_analyses", {})
    if not isinstance(word_analyses, dict):
        return output
    for word, row in word_analyses.items():
        synthesis = row.get("synthesis", {})
        best = _normalize_hypothesis(synthesis.get("best_hypothesis"))
        output[str(word)] = best
    return output


def _merge_batch_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in ("high_confidence_findings", "medium_confidence_findings", "needs_review"):
        part = payload.get(key, [])
        if isinstance(part, list):
            rows.extend(part)
    return rows


def build_word_best_map_batch(payload: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for row in _merge_batch_rows(payload):
        word = row.get("word")
        if not word:
            continue
        best = _normalize_hypothesis(row.get("best_hypothesis"))
        output[str(word)] = best
    return output


def build_word_best_map_integrated(payload: dict[str, Any], field: str) -> dict[str, str]:
    output: dict[str, str] = {}
    rows = payload.get("all_results", [])
    if not isinstance(rows, list):
        return output
    for row in rows:
        word = row.get("word")
        if not word:
            continue
        best = _normalize_hypothesis(row.get(field))
        output[str(word)] = best
    return output


def compare_word_maps(
    source_a: str, map_a: dict[str, str], source_b: str, map_b: dict[str, str]
) -> dict[str, Any]:
    overlap = sorted(set(map_a).intersection(map_b))
    mismatches = []
    for word in overlap:
        best_a = map_a[word]
        best_b = map_b[word]
        if best_a != best_b:
            mismatches.append(
                {
                    "word": word,
                    f"{source_a}_best": best_a,
                    f"{source_b}_best": best_b,
                }
            )

    mismatch_rate = _round(len(mismatches) / len(overlap), 4) if overlap else 0.0
    return {
        "source_a": source_a,
        "source_b": source_b,
        "overlap_words": len(overlap),
        "mismatch_count": len(mismatches),
        "mismatch_rate": mismatch_rate,
        "sample_mismatches": mismatches[:25],
    }


def build_metric_deltas(summaries: list[ToolSummary]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for hypothesis in HYPOTHESES:
        for i in range(len(summaries)):
            for j in range(i + 1, len(summaries)):
                left = summaries[i]
                right = summaries[j]
                pct_left = left.best_hypothesis_pct.get(hypothesis, 0.0)
                pct_right = right.best_hypothesis_pct.get(hypothesis, 0.0)
                delta = _round(abs(pct_left - pct_right), 2)
                out.append(
                    {
                        "hypothesis": hypothesis,
                        "source_a": left.name,
                        "source_b": right.name,
                        "pct_a": pct_left,
                        "pct_b": pct_right,
                        "delta_pct": delta,
                    }
                )
    return sorted(out, key=lambda row: row["delta_pct"], reverse=True)


def classify_severity(
    deltas: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    threshold_delta: float,
) -> dict[str, Any]:
    max_delta = max((row["delta_pct"] for row in deltas), default=0.0)
    max_mismatch = max((row["mismatch_rate"] for row in comparisons), default=0.0)

    level = "LOW"
    rationale: list[str] = []

    if max_delta >= threshold_delta or max_mismatch >= 0.35:
        level = "HIGH"
    elif max_delta >= (threshold_delta / 2.0) or max_mismatch >= 0.2:
        level = "MEDIUM"

    if max_delta >= threshold_delta:
        rationale.append(
            f"At least one hypothesis support delta ({max_delta}%) exceeds threshold ({threshold_delta}%)."
        )
    elif max_delta > 0:
        rationale.append(f"Maximum support delta observed: {max_delta}%.")

    if max_mismatch >= 0.35:
        rationale.append(
            f"Word-level mismatch rate reached {max_mismatch:.2%}, indicating strong pipeline disagreement."
        )
    elif max_mismatch > 0:
        rationale.append(
            f"Maximum word-level mismatch rate observed: {max_mismatch:.2%}."
        )

    if not rationale:
        rationale.append("No significant parity drift detected.")

    recommended = [
        "Verify normalization/filtering rules across hypothesis, batch, and integrated pipelines.",
        "Re-run parity check after adjusting any shared preprocessing logic.",
    ]
    if level == "HIGH":
        recommended.insert(
            0,
            "Block confidence promotions until parity issues are resolved and validated.",
        )
    elif level == "MEDIUM":
        recommended.insert(
            0,
            "Treat promotion decisions as provisional until parity deltas are reduced.",
        )
    else:
        recommended.insert(0, "Proceed with normal promotion workflow.")

    return {
        "level": level,
        "max_support_delta_pct": _round(max_delta, 2),
        "max_word_mismatch_rate": _round(max_mismatch, 4),
        "thresholds": {
            "support_delta_pct": threshold_delta,
            "word_mismatch_warn": 0.20,
            "word_mismatch_fail": 0.35,
        },
        "rationale": rationale,
        "recommended_action": recommended,
    }


def summarize_sizes(summaries: list[ToolSummary]) -> dict[str, Any]:
    data = {row.name: row.words_considered for row in summaries}
    values = [v for v in data.values() if isinstance(v, int)]
    drift = max(values) - min(values) if values else 0
    return {
        "words_considered": data,
        "max_min_drift": drift,
    }


def load_and_summarize(inputs: list[str]) -> tuple[list[ToolSummary], dict[str, Any]]:
    if len(inputs) != 3:
        raise RuntimeError("--inputs requires exactly 3 files: hypothesis, batch, integrated")

    paths = [Path(item).expanduser().resolve() for item in inputs]
    payloads = [_load_json(path) for path in paths]
    summaries = [
        summarize_hypothesis_results(paths[0], payloads[0]),
        summarize_batch_results(paths[1], payloads[1]),
        summarize_integrated_results(paths[2], payloads[2]),
    ]
    return summaries, {
        "hypothesis": payloads[0],
        "batch": payloads[1],
        "integrated": payloads[2],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check parity across core analysis artifacts")
    parser.add_argument(
        "--inputs",
        nargs=3,
        metavar=("HYPOTHESIS_JSON", "BATCH_JSON", "INTEGRATED_JSON"),
        default=DEFAULT_INPUTS,
        help="Input artifacts in fixed order: hypothesis, batch, integrated",
    )
    parser.add_argument(
        "--threshold-delta",
        type=float,
        default=15.0,
        help="Maximum acceptable support-percentage delta between pipelines (default: 15.0)",
    )
    parser.add_argument(
        "--output",
        default=str(DATA_DIR / "tool_parity_report.json"),
        help="Output path for JSON report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress console summary and only write JSON",
    )
    args = parser.parse_args()

    if args.threshold_delta <= 0:
        print("Error: --threshold-delta must be > 0")
        return 2

    try:
        summaries, payloads = load_and_summarize(args.inputs)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        return 1

    word_maps = {
        "hypothesis_results": build_word_best_map_hypothesis(payloads["hypothesis"]),
        "batch_analysis_results": build_word_best_map_batch(payloads["batch"]),
        "integrated_raw_best": build_word_best_map_integrated(
            payloads["integrated"], "raw_best_hypothesis"
        ),
        "integrated_bayesian_best": build_word_best_map_integrated(
            payloads["integrated"], "bayesian_best"
        ),
    }

    pairwise = [
        compare_word_maps(
            "hypothesis_results",
            word_maps["hypothesis_results"],
            "batch_analysis_results",
            word_maps["batch_analysis_results"],
        ),
        compare_word_maps(
            "hypothesis_results",
            word_maps["hypothesis_results"],
            "integrated_raw_best",
            word_maps["integrated_raw_best"],
        ),
        compare_word_maps(
            "batch_analysis_results",
            word_maps["batch_analysis_results"],
            "integrated_raw_best",
            word_maps["integrated_raw_best"],
        ),
        compare_word_maps(
            "integrated_raw_best",
            word_maps["integrated_raw_best"],
            "integrated_bayesian_best",
            word_maps["integrated_bayesian_best"],
        ),
    ]

    deltas = build_metric_deltas(summaries)
    severity = classify_severity(deltas, pairwise, args.threshold_delta)

    report: dict[str, Any] = {
        "metadata": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "method": "Tool parity cross-artifact comparison",
            "inputs": [str(Path(p).resolve()) for p in args.inputs],
        },
        "summary": {
            "status": severity["level"],
            "dataset_sizes": summarize_sizes(summaries),
            "top_delta": deltas[0] if deltas else None,
            "top_word_mismatch": max(pairwise, key=lambda row: row["mismatch_rate"]) if pairwise else None,
        },
        "tool_summaries": [summary.__dict__ for summary in summaries],
        "metric_deltas": deltas,
        "word_level_disagreements": {
            "pairwise": pairwise,
        },
        "severity": severity,
        "recommended_action": severity["recommended_action"],
    }

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not args.quiet:
        print("=" * 60)
        print("TOOL PARITY CHECKER")
        print("=" * 60)
        print(f"Status: {severity['level']}")
        print(f"Max support delta: {severity['max_support_delta_pct']}%")
        print(f"Max word mismatch rate: {severity['max_word_mismatch_rate']:.2%}")
        print(f"Report: {output_path}")
        if severity["rationale"]:
            print("Rationale:")
            for item in severity["rationale"]:
                print(f"  - {item}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
