"""Tests for update_index.py parsing behavior."""

import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR.parent))
sys.path.insert(0, str(TOOLS_DIR))

from tools.update_index import AnalysisFileParser  # noqa: E402


def test_update_index_parses_zb_siglum(tmp_path):
    """The index parser should recognize KN Zb style sigla from report headers."""
    report = tmp_path / "KNZb27_READING.md"
    report.write_text(
        "\n".join(
            [
                "# KN Zb 27 Connected Reading Report",
                "",
                "**Date**: 2026-03-15",
                "**Status**: COMPLETE",
                "**Confidence**: HIGH",
                "",
                "## Source Information",
                "",
                "| Attribute | Value |",
                "|-----------|-------|",
                "| **Tablet ID** | KN Zb 27 |",
                "| **Site** | Knossos |",
            ]
        ),
        encoding="utf-8",
    )

    parser = AnalysisFileParser()
    entries = parser.parse_file(report)

    assert entries, "Expected at least one parsed entry"
    assert entries[0].inscription_id == "KN Zb 27"
    assert entries[0].site == "Knossos"
    assert entries[0].status == "Complete"
    assert entries[0].confidence == "HIGH"
