#!/usr/bin/env python3
"""
Promotion Board Runner for Linear A

Generates promotion packets and decision records for candidate readings using
the required evidence artifacts and gate rules from MASTER_STATE.md.

Usage:
    python tools/promotion_board_runner.py --candidate KU-RO
    python tools/promotion_board_runner.py --candidate SA-RA₂ --target-confidence PROBABLE
    python tools/promotion_board_runner.py --candidate A-TA-I-*301-WA-JA --regional-justification "Religious register expected to be concentrated"
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
PACKET_DIR = PROJECT_ROOT / "analysis" / "active" / "promotion_packets"

REQUIRED_ARTIFACTS = {
    "hypothesis_results": DATA_DIR / "hypothesis_results.json",
    "consistency_results": DATA_DIR / "consistency_validation.json",
    "integrated_results": DATA_DIR / "integrated_results.json",
    "reading_dependencies": DATA_DIR / "reading_dependencies.json",
    "anchors": DATA_DIR / "anchors.json",
}
PARITY_REPORT = DATA_DIR / "tool_parity_report.json"
DEPENDENCY_TRACE_REPORT = DATA_DIR / "dependency_trace_report.json"

CONFIDENCE_ORDER = [
    "SPECULATIVE",
    "POSSIBLE",
    "MEDIUM",
    "PROBABLE",
    "HIGH",
    "CERTAIN",
]


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _normalize_confidence(value: Any) -> str:
    if not isinstance(value, str):
        return "SPECULATIVE"
    cleaned = value.strip().upper()
    if cleaned in CONFIDENCE_ORDER:
        return cleaned
    aliases = {
        "LOW": "SPECULATIVE",
        "LOW-MEDIUM": "POSSIBLE",
        "MEDIUM-LOW": "POSSIBLE",
        "LIKELY": "PROBABLE",
    }
    return aliases.get(cleaned, "SPECULATIVE")


def _next_confidence(current: str) -> str:
    current = _normalize_confidence(current)
    idx = CONFIDENCE_ORDER.index(current)
    if idx >= len(CONFIDENCE_ORDER) - 1:
        return current
    return CONFIDENCE_ORDER[idx + 1]


def _find_dict_entry_casefold(mapping: dict[str, Any], key: str) -> Any:
    if key in mapping:
        return mapping[key]
    upper = key.upper()
    if upper in mapping:
        return mapping[upper]
    key_cf = key.casefold()
    for k, v in mapping.items():
        if str(k).casefold() == key_cf:
            return v
    return None


def _find_word_in_list(rows: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
    key_cf = key.casefold()
    for row in rows:
        word = row.get("word")
        if isinstance(word, str) and word.casefold() == key_cf:
            return row
    return None


def _confidence_rank(value: str) -> int:
    value = _normalize_confidence(value)
    return CONFIDENCE_ORDER.index(value)


def _sanitize_word_for_filename(word: str) -> str:
    chars = []
    for ch in word:
        if ch.isalnum():
            chars.append(ch)
        elif ch in ("-", "_"):
            chars.append(ch)
        else:
            chars.append("_")
    cleaned = "".join(chars).strip("_")
    return cleaned or "candidate"


def _gate(required: bool, passed: bool, evidence: str, notes: str = "") -> dict[str, Any]:
    return {
        "required": required,
        "passed": passed,
        "evidence": evidence,
        "notes": notes,
    }


def _contains_provisional_marker(entry: dict[str, Any] | None) -> bool:
    if not isinstance(entry, dict):
        return False

    sources = entry.get("evidence_sources", [])
    if isinstance(sources, list):
        for item in sources:
            if isinstance(item, str) and "provisional" in item.lower():
                return True

    for field in ("cascade_note", "meaning"):
        value = entry.get(field)
        if isinstance(value, str) and "provisional" in value.lower():
            return True
    return False


def _cross_corpus_pass(
    *,
    target_confidence: str,
    consistency_validated: bool,
    positional_consistency: float,
    functional_consistency: float,
) -> tuple[bool, str]:
    if not consistency_validated:
        return False, "reading_validated=False"

    # PROBABLE gate allows one dimension to be strong and the other to be moderate.
    # HIGH/CERTAIN remain stricter.
    if target_confidence == "PROBABLE":
        passed = (
            min(positional_consistency, functional_consistency) >= 0.55
            and max(positional_consistency, functional_consistency) >= 0.70
        )
        rule = "min>=0.55 and max>=0.70"
    elif target_confidence in ("HIGH", "CERTAIN"):
        passed = positional_consistency >= 0.60 and functional_consistency >= 0.60
        rule = "positional>=0.60 and functional>=0.60"
    else:
        passed = positional_consistency >= 0.60 and functional_consistency >= 0.60
        rule = "positional>=0.60 and functional>=0.60"

    return passed, rule


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate promotion packet and board decision")
    parser.add_argument("--candidate", required=True, help="Candidate reading word")
    parser.add_argument(
        "--target-confidence",
        help="Target confidence tier (SPECULATIVE, POSSIBLE, MEDIUM, PROBABLE, HIGH, CERTAIN)",
    )
    parser.add_argument(
        "--regional-justification",
        help="Explicit justification when concentration is high but behavior is expected",
    )
    parser.add_argument(
        "--packet-out",
        help="Output path for markdown packet (default: analysis/active/promotion_packets/<candidate>.md)",
    )
    parser.add_argument(
        "--json-out",
        default=str(DATA_DIR / "promotion_decisions.json"),
        help="Output path for machine-readable board decisions",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail immediately if required artifacts are missing",
    )
    parser.add_argument(
        "--allow-provisional-trace",
        action="store_true",
        help="Allow PROBABLE+ promotions when dependency trace source is provisional",
    )
    args = parser.parse_args()

    candidate = args.candidate.strip()
    if not candidate:
        print("Error: --candidate cannot be empty")
        return 2

    artifact_presence = {name: path.exists() for name, path in REQUIRED_ARTIFACTS.items()}
    missing_required = [name for name, present in artifact_presence.items() if not present]
    if missing_required and args.strict:
        print("Error: missing required artifacts:")
        for name in missing_required:
            print(f"  - {name}: {REQUIRED_ARTIFACTS[name]}")
        return 1

    hypothesis_data = _load_json(REQUIRED_ARTIFACTS["hypothesis_results"]) or {}
    consistency_data = _load_json(REQUIRED_ARTIFACTS["consistency_results"]) or {}
    integrated_data = _load_json(REQUIRED_ARTIFACTS["integrated_results"]) or {}
    dependency_data = _load_json(REQUIRED_ARTIFACTS["reading_dependencies"]) or {}
    anchor_data = _load_json(REQUIRED_ARTIFACTS["anchors"]) or {}
    parity_data = _load_json(PARITY_REPORT) or {}
    dependency_trace_data = _load_json(DEPENDENCY_TRACE_REPORT) or {}

    hypothesis_entry = _find_dict_entry_casefold(
        hypothesis_data.get("word_analyses", {}), candidate
    )
    consistency_entry = _find_dict_entry_casefold(consistency_data.get("words", {}), candidate)
    integrated_entry = _find_word_in_list(integrated_data.get("all_results", []), candidate)
    dependency_entry = _find_dict_entry_casefold(dependency_data.get("readings", {}), candidate)
    dependency_trace_entry = _find_word_in_list(dependency_trace_data.get("checks", []), candidate)
    anchors = anchor_data.get("anchors", {})

    current_confidence = "SPECULATIVE"
    if dependency_entry and isinstance(dependency_entry, dict):
        current_confidence = _normalize_confidence(dependency_entry.get("confidence"))
    elif integrated_entry:
        current_confidence = _normalize_confidence(integrated_entry.get("final_confidence"))
    elif hypothesis_entry:
        synthesis = hypothesis_entry.get("synthesis", {})
        current_confidence = _normalize_confidence(synthesis.get("max_confidence"))

    target_confidence = (
        _normalize_confidence(args.target_confidence)
        if args.target_confidence
        else _next_confidence(current_confidence)
    )

    increasing = _confidence_rank(target_confidence) > _confidence_rank(current_confidence)

    # Pull shared evidence values
    dependency_warnings = []
    anchor_dependencies = []
    if integrated_entry:
        dependency_warnings = integrated_entry.get("dependency_warnings", []) or []
        anchor_dependencies = integrated_entry.get("anchor_dependencies", []) or []
    if not anchor_dependencies and dependency_entry:
        anchor_dependencies = dependency_entry.get("depends_on", []) or []

    dependency_trace_source = "none"
    dependency_trace_status = "unknown"
    if dependency_trace_entry:
        dependency_trace_source = str(dependency_trace_entry.get("trace_source", "none")).lower()
        dependency_trace_status = str(dependency_trace_entry.get("status", "unknown")).lower()
    elif dependency_entry and anchor_dependencies:
        sources = (
            dependency_entry.get("evidence_sources", [])
            if isinstance(dependency_entry, dict)
            else []
        )
        if (
            isinstance(sources, list) and "dependency_trace_resolver.py --write" in sources
        ) or _contains_provisional_marker(dependency_entry):
            dependency_trace_source = "provisional"
        else:
            dependency_trace_source = "existing"
        dependency_trace_status = "complete"

    parity_level = str(
        parity_data.get("severity", {}).get(
            "level",
            parity_data.get("summary", {}).get("status", "UNKNOWN"),
        )
    ).upper()

    threshold_category = (
        str(integrated_entry.get("threshold_category", "")) if integrated_entry else ""
    )
    methodology_compliant = (
        bool(integrated_entry.get("methodology_compliant")) if integrated_entry else False
    )
    final_confidence = (
        _normalize_confidence(integrated_entry.get("final_confidence"))
        if integrated_entry
        else "SPECULATIVE"
    )
    ht_concentration = (
        float(integrated_entry.get("ht_concentration", 0.0)) if integrated_entry else 0.0
    )
    num_sites = int(integrated_entry.get("num_sites", 0) or 0) if integrated_entry else 0
    negative_items = integrated_entry.get("negative_evidence_items", []) if integrated_entry else []

    consistency_validated = (
        bool(consistency_entry.get("reading_validated")) if consistency_entry else False
    )
    positional_consistency = (
        float(consistency_entry.get("positional_consistency", 0.0)) if consistency_entry else 0.0
    )
    functional_consistency = (
        float(consistency_entry.get("functional_consistency", 0.0)) if consistency_entry else 0.0
    )
    sites_found = consistency_entry.get("sites_found", []) if consistency_entry else []
    cross_corpus_passed, cross_corpus_rule = _cross_corpus_pass(
        target_confidence=target_confidence,
        consistency_validated=consistency_validated,
        positional_consistency=positional_consistency,
        functional_consistency=functional_consistency,
    )

    anchors_with_falsification = 0
    for dep in anchor_dependencies:
        anchor = anchors.get(dep, {})
        if isinstance(anchor, dict) and str(anchor.get("falsification_condition", "")).strip():
            anchors_with_falsification += 1

    all_hypotheses_present = False
    if hypothesis_entry:
        hypotheses = hypothesis_entry.get("hypotheses", {})
        all_hypotheses_present = all(
            k in hypotheses
            for k in (
                "luwian",
                "semitic",
                "pregreek",
                "protogreek",
                "hurrian",
                "hattic",
                "etruscan",
            )
        )

    direct_anchor_contradiction = any(
        isinstance(item, str) and ("contradict" in item.lower() or "conflict" in item.lower())
        for item in dependency_warnings
    )
    eliminated_flag = threshold_category.upper() == "ELIMINATED"

    gate_results: dict[str, dict[str, Any]] = {}
    gate_results["required_inputs_present"] = _gate(
        required=True,
        passed=(len(missing_required) == 0),
        evidence=f"Missing: {', '.join(missing_required) if missing_required else 'none'}",
    )
    gate_results["no_direct_anchor_contradiction"] = _gate(
        required=True,
        passed=(not direct_anchor_contradiction and not eliminated_flag),
        evidence=f"dependency_warnings={len(dependency_warnings)}, threshold={threshold_category or 'unknown'}",
    )
    gate_results["parity_guard"] = _gate(
        required=True,
        passed=(parity_level != "HIGH"),
        evidence=f"parity_level={parity_level}",
    )
    gate_results["multi_hypothesis_run"] = _gate(
        required=True,
        passed=all_hypotheses_present,
        evidence="All seven hypotheses present in hypothesis_results",
    )
    gate_results["cross_corpus_consistency"] = _gate(
        required=True,
        passed=cross_corpus_passed,
        evidence=(
            f"validated={consistency_validated}, positional={positional_consistency:.3f}, "
            f"functional={functional_consistency:.3f}, sites={len(sites_found)}, rule={cross_corpus_rule}"
        ),
    )
    gate_results["integrated_validation"] = _gate(
        required=True,
        passed=bool(integrated_entry),
        evidence=(
            f"entry={'yes' if integrated_entry else 'no'}, "
            f"final_confidence={final_confidence}, methodology_compliant={methodology_compliant}"
        ),
    )
    gate_results["dependency_trace"] = _gate(
        required=True,
        passed=bool(anchor_dependencies) and dependency_trace_source in {"existing", "provisional"},
        evidence=f"anchor_dependencies={len(anchor_dependencies)}, trace_source={dependency_trace_source}",
        notes=f"trace_source={dependency_trace_source}, trace_status={dependency_trace_status}",
    )
    gate_results["provisional_trace_review"] = _gate(
        required=target_confidence in ("PROBABLE", "HIGH", "CERTAIN"),
        passed=(dependency_trace_source != "provisional" or args.allow_provisional_trace),
        evidence=f"trace_source={dependency_trace_source}, allow_override={args.allow_provisional_trace}",
    )
    gate_results["negative_evidence_statement"] = _gate(
        required=True,
        passed=isinstance(negative_items, list),
        evidence=f"negative_evidence_items={len(negative_items) if isinstance(negative_items, list) else 'missing'}",
    )
    regional_note = (
        args.regional_justification
        if args.regional_justification
        else (
            "High concentration noted without explicit justification."
            if ht_concentration > 0.8
            else "Balanced distribution."
        )
    )
    gate_results["regional_concentration_addressed"] = _gate(
        required=True,
        passed=(
            ht_concentration <= 0.8
            or bool(args.regional_justification)
            or target_confidence in ("POSSIBLE", "MEDIUM")
        ),
        evidence=f"ht_concentration={ht_concentration:.3f}, num_sites={num_sites}",
        notes=regional_note,
    )
    gate_results["falsification_documented"] = _gate(
        required=True,
        passed=(anchors_with_falsification > 0),
        evidence=f"anchors_with_falsification={anchors_with_falsification}/{len(anchor_dependencies)}",
    )
    gate_results["multi_anchor_support"] = _gate(
        required=target_confidence in ("HIGH", "CERTAIN"),
        passed=(len(anchor_dependencies) >= 2),
        evidence=f"anchor_dependencies={len(anchor_dependencies)}",
    )
    gate_results["broad_corpus_behavior"] = _gate(
        required=target_confidence == "CERTAIN",
        passed=(
            len(sites_found) >= 3
            and positional_consistency >= 0.8
            and functional_consistency >= 0.8
        ),
        evidence=f"sites={len(sites_found)}, positional={positional_consistency:.3f}, functional={functional_consistency:.3f}",
    )
    gate_results["methodology_compliant_for_high"] = _gate(
        required=target_confidence in ("HIGH", "CERTAIN"),
        passed=methodology_compliant,
        evidence=f"methodology_compliant={methodology_compliant}",
    )

    required_gate_ids = [
        "required_inputs_present",
        "no_direct_anchor_contradiction",
        "parity_guard",
    ]
    if increasing:
        if target_confidence in ("POSSIBLE", "MEDIUM"):
            required_gate_ids.extend(["multi_hypothesis_run"])
        elif target_confidence == "PROBABLE":
            required_gate_ids.extend(
                [
                    "multi_hypothesis_run",
                    "cross_corpus_consistency",
                    "integrated_validation",
                    "dependency_trace",
                    "provisional_trace_review",
                    "negative_evidence_statement",
                ]
            )
        elif target_confidence == "HIGH":
            required_gate_ids.extend(
                [
                    "multi_hypothesis_run",
                    "cross_corpus_consistency",
                    "integrated_validation",
                    "dependency_trace",
                    "provisional_trace_review",
                    "negative_evidence_statement",
                    "regional_concentration_addressed",
                    "multi_anchor_support",
                    "methodology_compliant_for_high",
                    "falsification_documented",
                ]
            )
        elif target_confidence == "CERTAIN":
            required_gate_ids.extend(
                [
                    "multi_hypothesis_run",
                    "cross_corpus_consistency",
                    "integrated_validation",
                    "dependency_trace",
                    "provisional_trace_review",
                    "negative_evidence_statement",
                    "regional_concentration_addressed",
                    "multi_anchor_support",
                    "broad_corpus_behavior",
                    "methodology_compliant_for_high",
                    "falsification_documented",
                ]
            )
    else:
        required_gate_ids.extend(["integrated_validation", "dependency_trace"])

    failed_required = [
        gate for gate in required_gate_ids if not gate_results.get(gate, {}).get("passed", False)
    ]
    critical_fail = any(
        not gate_results[name]["passed"]
        for name in ("required_inputs_present", "no_direct_anchor_contradiction")
    )

    if critical_fail:
        board_decision = "REJECT"
    elif failed_required:
        board_decision = "HOLD"
    else:
        board_decision = "APPROVE"

    rationale = []
    if board_decision == "APPROVE":
        rationale.append("All required gates passed for requested confidence transition.")
    elif board_decision == "HOLD":
        rationale.append("One or more non-critical required gates failed.")
    else:
        rationale.append(
            "Critical gate failure detected (missing artifacts or direct contradiction)."
        )

    if failed_required:
        rationale.append(f"Failed gates: {', '.join(failed_required)}")

    evidence_artifacts = {
        "hypothesis_results": str(REQUIRED_ARTIFACTS["hypothesis_results"]),
        "consistency_results": str(REQUIRED_ARTIFACTS["consistency_results"]),
        "integrated_results": str(REQUIRED_ARTIFACTS["integrated_results"]),
        "reading_dependencies": str(REQUIRED_ARTIFACTS["reading_dependencies"]),
        "anchors": str(REQUIRED_ARTIFACTS["anchors"]),
    }

    decision_record: dict[str, Any] = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "candidate": candidate,
        "current_confidence": current_confidence,
        "target_confidence": target_confidence,
        "direction": "promotion" if increasing else "non-promotion",
        "decision": board_decision,
        "required_gate_ids": required_gate_ids,
        "failed_required": failed_required,
        "gate_results": gate_results,
        "evidence": {
            "artifact_presence": artifact_presence,
            "hypothesis_entry_found": bool(hypothesis_entry),
            "consistency_entry_found": bool(consistency_entry),
            "integrated_entry_found": bool(integrated_entry),
            "dependency_entry_found": bool(dependency_entry),
            "anchor_dependencies": anchor_dependencies,
            "dependency_trace_source": dependency_trace_source,
            "dependency_trace_status": dependency_trace_status,
            "threshold_category": threshold_category,
            "final_confidence": final_confidence,
            "methodology_compliant": methodology_compliant,
            "parity_level": parity_level,
            "cross_corpus_metrics": {
                "validated": consistency_validated,
                "positional_consistency": positional_consistency,
                "functional_consistency": functional_consistency,
                "rule": cross_corpus_rule,
                "passed": cross_corpus_passed,
            },
            "ht_concentration": ht_concentration,
            "num_sites": num_sites,
            "sites_found": sites_found,
        },
        "rationale": rationale,
        "follow_up_actions": [
            "Re-run candidate through tool_parity_checker before final publication.",
            "Attach packet and JSON decision record to lane B promotion board review.",
        ],
    }

    packet_path = (
        Path(args.packet_out).expanduser().resolve()
        if args.packet_out
        else (PACKET_DIR / f"{_sanitize_word_for_filename(candidate)}.md").resolve()
    )
    packet_path.parent.mkdir(parents=True, exist_ok=True)

    # Packet fields
    hypothesis_text = "Not available"
    if hypothesis_entry:
        hyp = hypothesis_entry.get("hypotheses", {})

        def _hv(name: str) -> str:
            row = hyp.get(name, {})
            return f"score={row.get('score', 'n/a')}, verdict={row.get('verdict', 'n/a')}"

        hypothesis_text = "\n".join(
            [
                f"- Luwian: {_hv('luwian')}",
                f"- Semitic: {_hv('semitic')}",
                f"- Pre-Greek: {_hv('pregreek')}",
                f"- Proto-Greek: {_hv('protogreek')}",
            ]
        )

    negative_text = "No integrated negative evidence entry."
    if isinstance(negative_items, list):
        if negative_items:
            negative_text = "\n".join(f"- {item}" for item in negative_items[:12])
        else:
            negative_text = "- No explicit negative evidence penalties recorded."

    sites_attested = sites_found if isinstance(sites_found, list) else []
    anchor_lines = []
    for dep in anchor_dependencies:
        anchor = anchors.get(dep, {})
        if isinstance(anchor, dict):
            anchor_lines.append(
                f"- {dep}: level={anchor.get('level', 'n/a')}, confidence={anchor.get('confidence', 'n/a')}"
            )
        else:
            anchor_lines.append(f"- {dep}: metadata unavailable")
    if not anchor_lines:
        anchor_lines.append("- No anchor dependencies found")

    gate_lines = []
    for gate in required_gate_ids:
        row = gate_results[gate]
        mark = "x" if row["passed"] else " "
        gate_lines.append(f"- [{mark}] {gate} ({row['evidence']})")

    packet_body = f"""# Promotion Packet: {candidate}

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: {candidate}
- Current confidence: {current_confidence}
- Proposed confidence: {target_confidence}
- Meaning claim: {(dependency_entry or {}).get("meaning", "Not specified")}
- Primary contexts: {", ".join(sites_attested) if sites_attested else "Not available"}

## 2. Evidence Artifacts

- Hypothesis results: `{evidence_artifacts["hypothesis_results"]}`
- Consistency results: `{evidence_artifacts["consistency_results"]}`
- Integrated results: `{evidence_artifacts["integrated_results"]}`
- Dependencies: `{evidence_artifacts["reading_dependencies"]}`
- Anchors: `{evidence_artifacts["anchors"]}`
- Optional supporting analysis: {"Provided via --regional-justification" if args.regional_justification else "None"}

## 3. Multi-Hypothesis Adjudication

{hypothesis_text}
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

{negative_text}
- Contradictions detected: {"Yes" if direct_anchor_contradiction else "No"}
- Remaining uncertainty: threshold={threshold_category or "unknown"}, final_confidence={final_confidence}

## 5. Cross-Corpus and Regional Behavior

- Sites attested: {", ".join(sites_attested) if sites_attested else "Not available"}
- Site concentration (HT): {ht_concentration:.3f}
- Period spread: {(consistency_entry or {}).get("periods_found", []) if consistency_entry else "Not available"}
- Regional weighting impact: {(integrated_entry or {}).get("regional_weight", "Not available")}
- Parity status: {parity_level}

## 6. Anchor and Dependency Check

{chr(10).join(anchor_lines)}
- Weakest dependency: {(integrated_entry or {}).get("max_confidence_from_anchors", "Unknown")}
- Cascade risk if questioned: {"; ".join(dependency_warnings) if dependency_warnings else "No cascade warnings"}
- Dependency trace source: {dependency_trace_source} (status: {dependency_trace_status})

## 7. Gate Checklist

{chr(10).join(gate_lines)}

## 8. Decision

- Board decision: {board_decision}
- Rationale: {" ".join(rationale)}
- Follow-up actions:
  - {"; ".join(decision_record["follow_up_actions"])}
"""
    packet_path.write_text(packet_body, encoding="utf-8")

    json_out_path = Path(args.json_out).expanduser().resolve()
    json_out_path.parent.mkdir(parents=True, exist_ok=True)

    existing = _load_json(json_out_path) or {}
    decisions = existing.get("decisions", [])
    if not isinstance(decisions, list):
        decisions = []

    # Replace previous record for same candidate to keep output deterministic.
    candidate_cf = candidate.casefold()
    decisions = [
        row for row in decisions if str(row.get("candidate", "")).casefold() != candidate_cf
    ]
    decisions.append(decision_record)

    merged = {
        "metadata": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "method": "Promotion board runner",
            "artifacts": evidence_artifacts,
        },
        "decisions": decisions,
    }
    json_out_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("=" * 60)
    print("PROMOTION BOARD RUNNER")
    print("=" * 60)
    print(f"Candidate: {candidate}")
    print(f"Current -> Target: {current_confidence} -> {target_confidence}")
    print(f"Decision: {board_decision}")
    if failed_required:
        print(f"Failed required gates: {', '.join(failed_required)}")
    print(f"Packet: {packet_path}")
    print(f"Decision JSON: {json_out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
