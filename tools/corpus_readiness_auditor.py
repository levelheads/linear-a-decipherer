#!/usr/bin/env python3
"""
Corpus readiness auditor for sprint setup checks.

Generates a JSON snapshot (and optional Markdown summary) describing whether
the local project has enough corpus/comparative access to run further tests.
"""

import argparse
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = PROJECT_ROOT / "analysis" / "active"


def load_json(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def site_code(inscription_id: str) -> str:
    match = re.match(r"^([A-Z]+)", inscription_id)
    return match.group(1) if match else "UNK"


def _safe_get(obj: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = obj
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _submodule_status() -> str:
    try:
        lines = (
            subprocess.check_output(
                ["git", "submodule", "status"],
                cwd=PROJECT_ROOT,
                text=True,
            )
            .strip()
            .splitlines()
        )
        return lines[0].strip() if lines else "none"
    except Exception:
        return "unknown"


def build_report() -> dict[str, Any]:
    corpus = load_json(DATA_DIR / "corpus.json")
    validation = load_json(DATA_DIR / "validation_report.json")
    extended = load_json(DATA_DIR / "extended_corpus_analysis.json")

    sigla = load_json(DATA_DIR / "sigla" / "sign_database.json")
    damos = load_json(DATA_DIR / "linear_b" / "cognate_verification.json")
    oracc = load_json(DATA_DIR / "comparative" / "akkadian_oracc.json")
    gorila = load_json(DATA_DIR / "gorila" / "index.json")

    inscriptions = corpus.get("inscriptions", {})
    site_counts: Counter[str] = Counter()
    support_counts: Counter[str] = Counter()
    period_counts: Counter[str] = Counter()
    parse_error_count = 0
    empty_transliterated: list[str] = []

    for insc_id, data in inscriptions.items():
        site_counts[site_code(insc_id)] += 1
        support_counts[str(data.get("support", "UNKNOWN"))] += 1
        period_counts[str(data.get("context", ""))] += 1
        if "_parse_error" in data:
            parse_error_count += 1
        if not data.get("transliteratedWords"):
            empty_transliterated.append(insc_id)

    missing_context_count = sum(1 for data in inscriptions.values() if not data.get("context", ""))
    missing_site_count = sum(1 for data in inscriptions.values() if not data.get("site", ""))

    coverage = extended.get("coverage", {})
    site_cov = extended.get("site_coverage", {})

    total_inscriptions = len(inscriptions)
    ht_total = site_counts.get("HT", 0) + site_counts.get("HTW", 0) + site_counts.get("HTZ", 0)
    ht_share = (ht_total / total_inscriptions) if total_inscriptions else 0.0

    critical_errors = _safe_get(validation, "summary", "critical_errors", default=1)
    if critical_errors is None:
        critical_errors = 1

    ready = (
        total_inscriptions >= 1700
        and float(coverage.get("coverage_percent", 0) or 0) >= 25.0
        and int(critical_errors) == 0
    )

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    return {
        "metadata": {
            "generated_utc": generated,
            "purpose": "Project setup / corpus access readiness for further decipherment tests",
        },
        "core_corpus_access": {
            "inscriptions_total": total_inscriptions,
            "submodule_status": _submodule_status(),
            "source": _safe_get(corpus, "attribution", "source", default=""),
            "upstream": _safe_get(corpus, "attribution", "upstream", default=[]),
            "parse_errors_flagged": parse_error_count,
            "empty_transliterated_records": len(empty_transliterated),
            "empty_transliterated_ids": empty_transliterated,
            "unique_site_codes": len(site_counts),
            "top_site_codes": site_counts.most_common(12),
            "supports": dict(support_counts),
            "period_top": period_counts.most_common(12),
        },
        "analysis_coverage": {
            "extended_coverage_percent": coverage.get("coverage_percent"),
            "extended_total_analyzed": coverage.get("total_analyzed"),
            "extended_total_corpus": coverage.get("total_corpus"),
            "ht_cluster_share_of_corpus": round(ht_share, 3),
            "ht_site_coverage": site_cov.get("HT", {}),
            "kh_site_coverage": site_cov.get("KH", {}),
            "ioz_site_coverage": site_cov.get("IOZ", {}),
        },
        "comparative_access": {
            "sigla_static_signs": _safe_get(sigla, "statistics", "total_signs", default=None),
            "sigla_sites_covered": _safe_get(sigla, "statistics", "sites_covered", default=[]),
            "damos_vocab_total": _safe_get(
                damos, "vocabulary_stats", "total_entries", default=None
            ),
            "damos_cognate_words": _safe_get(
                damos, "cognates_stats", "identical_words", default=None
            ),
            "oracc_terms_total": _safe_get(oracc, "metadata", "total_terms", default=None),
            "oracc_generated": _safe_get(oracc, "metadata", "generated", default=None),
            "gorila_index_inscriptions": _safe_get(
                gorila, "statistics", "total_inscriptions", default=None
            ),
        },
        "data_quality": {
            "validation_critical_errors": _safe_get(
                validation, "summary", "critical_errors", default=None
            ),
            "validation_warnings": _safe_get(validation, "summary", "warnings", default=None),
            "warning_sample": validation.get("warnings", [])[:8],
            "missing_context_count": missing_context_count,
            "missing_site_count": missing_site_count,
        },
        "readiness_assessment": {
            "ready_for_further_local_testing": ready,
            "verdict": (
                "sufficient_for_next_analysis_cycle_with_known_gaps"
                if ready
                else "insufficient_without_data_remediation"
            ),
            "blocking_gaps": [
                "No new non-SYZ ritual-slot substitutions in current corpus; acceleration depends on new attestations or alternate targets.",
                "Context metadata gaps weaken chronology-conditioned tests.",
                "HT-cluster dominance remains high; queue diversification is still needed for robust cross-site inference.",
                "Comparative connectors rely on static dictionaries or optional network fetches; live refresh paths are limited offline.",
            ],
            "recommended_actions": [
                "Run a scheduled corpus refresh workflow (submodule update -> parse_lineara_corpus -> validate_corpus).",
                "Maintain a remediation ledger for missing context/site/empty transliteration records and explicit validator exclusions.",
                "Prioritize non-HT ritual-support inscriptions in expansion queues.",
                "Version comparative snapshots (ORACC/SigLA/DAMOS) each cycle for drift tracking.",
            ],
        },
    }


def render_markdown(report: dict[str, Any], json_path: Path) -> str:
    core = report["core_corpus_access"]
    quality = report["data_quality"]
    coverage = report["analysis_coverage"]
    comp = report["comparative_access"]
    ready = report["readiness_assessment"]

    return "\n".join(
        [
            "# Corpus Access Readiness Audit",
            "",
            f"**Date**: {report['metadata']['generated_utc'][:10]}  ",
            f"**Artifact**: `{json_path}`",
            "",
            "## Verdict",
            "",
            f"Readiness status: **{ready['verdict']}**.",
            "",
            "## Snapshot",
            "",
            f"- Core corpus inscriptions: `{core['inscriptions_total']}`",
            f"- Parse error flags: `{core['parse_errors_flagged']}`",
            f"- Empty transliteration records: `{core['empty_transliterated_records']}`",
            f"- Unique site codes: `{core['unique_site_codes']}`",
            f"- Extended coverage: `{coverage['extended_coverage_percent']}%`",
            f"- HT-cluster share: `{coverage['ht_cluster_share_of_corpus']}`",
            "",
            "## Comparative Access",
            "",
            f"- SigLA static signs: `{comp['sigla_static_signs']}`",
            f"- DĀMOS vocabulary entries: `{comp['damos_vocab_total']}`",
            f"- ORACC comparative terms: `{comp['oracc_terms_total']}`",
            f"- GORILA indexed inscriptions: `{comp['gorila_index_inscriptions']}`",
            "",
            "## Quality Gaps",
            "",
            f"- Validation critical errors: `{quality['validation_critical_errors']}`",
            f"- Validation warnings: `{quality['validation_warnings']}`",
            f"- Missing context count: `{quality['missing_context_count']}`",
            f"- Missing site count: `{quality['missing_site_count']}`",
            "",
            "## Recommended Actions",
            "",
            "1. Run refresh workflow at sprint start (`submodule -> parse -> validate`).",
            "2. Maintain remediation ledger for metadata/transliteration gaps.",
            "3. Keep non-HT ritual inscriptions at top of expansion queue.",
            "4. Version comparative snapshots for drift detection.",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a corpus access readiness audit snapshot."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="JSON output path (default: analysis/active/YYYY-MM-DD_corpus_access_readiness_audit.json)",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Also write a Markdown summary next to JSON output",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress console output")
    args = parser.parse_args()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    output_path = (
        Path(args.output)
        if args.output
        else ANALYSIS_DIR / f"{today}_corpus_access_readiness_audit.json"
    )
    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    report = build_report()
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    if args.markdown:
        md_path = output_path.with_suffix(".md")
        md_path.write_text(render_markdown(report, output_path), encoding="utf-8")

    if not args.quiet:
        print(f"Wrote readiness audit JSON: {output_path}")
        if args.markdown:
            print(f"Wrote readiness audit Markdown: {output_path.with_suffix('.md')}")
        print(
            "Readiness verdict:",
            report["readiness_assessment"]["verdict"],
            "| ready_for_further_local_testing:",
            report["readiness_assessment"]["ready_for_further_local_testing"],
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
