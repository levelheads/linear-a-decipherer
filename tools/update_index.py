#!/usr/bin/env python3
"""
Analysis Index Auto-Updater for Linear A

Scans analysis/active/ and analysis/completed/ directories for analysis markdown
files, extracts metadata, and generates/updates ANALYSIS_INDEX.md entries.

Extracted metadata:
- Inscription ID (patterns: HT 85, IO Za 2, KH 11, PH(?)31, ZA 4a/4b)
- Site (from ID or explicit mention)
- Status (COMPLETE, PENDING, IN_PROGRESS, etc.)
- Key findings from "Key Finding" or "Key Findings" sections

Usage:
    python tools/update_index.py                    # Preview changes
    python tools/update_index.py --write            # Update ANALYSIS_INDEX.md
    python tools/update_index.py --verbose          # Show detailed parsing
    python tools/update_index.py --json             # Output as JSON

First Principles Compliance:
    - P1 (Kober): Automated pattern extraction, no assumptions
    - P6 (Cross-Corpus): Enables systematic corpus coverage tracking

Attribution:
    Part of Linear A Decipherment Project
    Automated index maintenance for analysis tracking
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, field, asdict


# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
ACTIVE_DIR = ANALYSIS_DIR / "active"
COMPLETED_DIR = ANALYSIS_DIR / "completed"
INDEX_PATH = PROJECT_ROOT / "linear-a-decipherer" / "ANALYSIS_INDEX.md"


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class AnalysisEntry:
    """Represents a single inscription analysis entry."""

    inscription_id: str
    site: str
    status: str
    confidence: str
    key_finding: str
    analysis_file: str
    date: str
    file_path: Path = field(repr=False, default=None)

    def to_table_row(self) -> str:
        """Format as markdown table row."""
        # Truncate key finding if too long
        finding = self.key_finding
        if len(finding) > 100:
            finding = finding[:97] + "..."
        return f"| {self.inscription_id} | {self.site} | {self.status} | {self.confidence} | {finding} | {self.analysis_file} | {self.date} |"


# ============================================================================
# SITE MAPPING
# ============================================================================

SITE_CODES = {
    "HT": "Hagia Triada",
    "KH": "Khania",
    "ZA": "Zakros",
    "PH": "Phaistos",
    "KN": "Knossos",
    "IO": "Iouktas",
    "TY": "Tylissos",
    "MA": "Malia",
    "PL": "Platanos",
    "PS": "Psychro",
    "TL": "Troullos",
    "PK": "Palaikastro",
    "AP": "Apodoulou",
    "AR": "Archanes",
    "KA": "Kato Syme",
    "MY": "Mykenaean",
    "PE": "Petsophas",
    "PR": "Prasa",
    "SY": "Syme",
    "VR": "Vrysinas",
}


# ============================================================================
# REGEX PATTERNS
# ============================================================================

# Inscription ID patterns - ORDER MATTERS (more specific patterns first)
INSCRIPTION_ID_PATTERNS = [
    # Peak sanctuary format: IO Za 2, PS Za 2 (must come before standard format)
    (r"\b([A-Z]{2})\s+Za\s+(\d+)\b", "za"),
    # Scepter format: KN Zf 2
    (r"\b([A-Z]{2})\s+Zf\s+(\d+)\b", "zf"),
    # With parenthetical: PH(?)31a/b
    (r"\b([A-Z]{2})\(\?\)(\d+[a-z]?(?:/[a-z])?)\b", "standard"),
    # Combined format in titles: HT 94 / HT 117
    (r"\b([A-Z]{2})\s+(\d+)\s*/\s*[A-Z]{2}\s+\d+", "standard"),
    # Range format: KH 5 and KH 88
    (r"\b([A-Z]{2})\s+(\d+)\s+and\s+[A-Z]{2}\s+\d+", "standard"),
    # Standard format: HT 85, KH 11, ZA 4 (comes last as fallback)
    # Exclude Za/Zf/Zg patterns to avoid false matches
    (r"\b([A-Z]{2})\s+(\d+[a-z]?(?:/[a-z])?)\b", "standard"),
]

# Status patterns
STATUS_PATTERNS = [
    r"\*\*Status\*\*:\s*([A-Z_]+)",
    r"Status:\s*([A-Z_]+)",
    r"\bStatus\b[:\s]+([A-Z_]+)",
]

# Confidence patterns
CONFIDENCE_PATTERNS = [
    r"\*\*Confidence\*\*:\s*([A-Z]+)",
    r"Confidence:\s*([A-Z]+)",
    r"\bConfidence\b[:\s]+([A-Z]+)",
]

# Date patterns
DATE_PATTERNS = [
    r"\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})",
    r"Date:\s*(\d{4}-\d{2}-\d{2})",
]


# ============================================================================
# PARSER
# ============================================================================


class AnalysisFileParser:
    """
    Parses markdown analysis files to extract metadata.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def log(self, msg: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  [PARSE] {msg}")

    def parse_file(self, file_path: Path) -> List[AnalysisEntry]:
        """
        Parse a single analysis file and extract entries.

        Returns list of entries (one file may contain multiple inscriptions).
        """
        self.log(f"Parsing: {file_path.name}")

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            self.log(f"Error reading file: {e}")
            return []

        entries = []

        # Extract inscription IDs from the file
        inscription_ids = self._extract_inscription_ids(content, file_path.name)

        if not inscription_ids:
            self.log(f"No inscription IDs found in {file_path.name}")
            return []

        # Extract common metadata
        status = self._extract_status(content)
        confidence = self._extract_confidence(content)
        date = self._extract_date(content, file_path)
        key_findings = self._extract_key_findings(content)

        # Create relative path for analysis file link
        try:
            rel_path = file_path.relative_to(PROJECT_ROOT)
        except ValueError:
            rel_path = file_path.name

        for insc_id in inscription_ids:
            site = self._extract_site(insc_id, content)

            # Find key finding specific to this inscription if possible
            finding = self._find_inscription_specific_finding(insc_id, key_findings, content)

            entry = AnalysisEntry(
                inscription_id=insc_id,
                site=site,
                status=status,
                confidence=confidence,
                key_finding=finding,
                analysis_file=f"[{file_path.stem}]({rel_path})",
                date=date,
                file_path=file_path,
            )
            entries.append(entry)
            self.log(f"  Found: {insc_id} at {site} ({status})")

        return entries

    def _extract_inscription_ids(self, content: str, filename: str) -> List[str]:
        """Extract all inscription IDs from file content."""
        ids = set()

        # Skip tracking/overview files that list many inscriptions
        skip_patterns = ["TRACKING", "OVERVIEW", "INDEX", "AUDIT", "SYNTHESIS"]
        if any(pat in filename.upper() for pat in skip_patterns):
            self.log(f"Skipping tracking/overview file: {filename}")
            return []

        # Check filename first for primary inscription
        for pattern, pattern_type in INSCRIPTION_ID_PATTERNS:
            for match in re.finditer(pattern, filename, re.IGNORECASE):
                # Normalize the ID
                site_code = match.group(1).upper()
                number = match.group(2)

                # Skip if this looks like a Za/Zf prefix that should be handled specially
                if pattern_type == "standard" and site_code in ["ZA", "ZF", "ZG"]:
                    # Check if this is actually part of a Za/Zf pattern
                    continue

                if pattern_type == "za":
                    insc_id = f"{site_code} Za {number}"
                elif pattern_type == "zf":
                    insc_id = f"{site_code} Zf {number}"
                else:
                    insc_id = f"{site_code} {number}"

                ids.add(insc_id)

        # Check title/header (first few lines)
        header_lines = "\n".join(content.split("\n")[:20])

        for pattern, pattern_type in INSCRIPTION_ID_PATTERNS:
            for match in re.finditer(pattern, header_lines, re.IGNORECASE):
                site_code = match.group(1).upper()
                number = match.group(2)

                # Handle special cases
                if pattern_type == "za":
                    insc_id = f"{site_code} Za {number}"
                elif pattern_type == "zf":
                    insc_id = f"{site_code} Zf {number}"
                else:
                    # Skip standalone ZA/ZF/ZG if they should be prefixes
                    if site_code in ["ZA", "ZF", "ZG"] and pattern_type == "standard":
                        continue
                    insc_id = f"{site_code} {number}"

                ids.add(insc_id)

        # Special handling for combined analyses (multiple tablets)
        combined_patterns = [
            r"([A-Z]{2})\s+(\d+[a-z]?)\s+and\s+([A-Z]{2})\s+(\d+[a-z]?)",
            r"([A-Z]{2})\s+(\d+[a-z]?),\s*([A-Z]{2})\s+(\d+[a-z]?)",
        ]
        for pattern in combined_patterns:
            for match in re.finditer(pattern, header_lines, re.IGNORECASE):
                ids.add(f"{match.group(1).upper()} {match.group(2)}")
                ids.add(f"{match.group(3).upper()} {match.group(4)}")

        # Handle a/b sides
        processed_ids = set()
        for insc_id in ids:
            # If we have "HT 94" but content mentions "HT 94a" and "HT 94b"
            base = insc_id.rstrip("ab/")
            if base != insc_id:
                processed_ids.add(insc_id)
            elif re.search(rf"{re.escape(base)}[ab]", content):
                # Check if explicit a/b sides are discussed
                if f"{base}a" in content and f"{base}b" in content:
                    processed_ids.add(f"{base}a/b")
                else:
                    processed_ids.add(insc_id)
            else:
                processed_ids.add(insc_id)

        return sorted(processed_ids)

    def _extract_status(self, content: str) -> str:
        """Extract analysis status from content."""
        for pattern in STATUS_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                status = match.group(1).upper()
                # Normalize status values
                if status in ["COMPLETE", "COMPLETED", "DONE"]:
                    return "Complete"
                elif status in ["PARTIAL", "IN_PROGRESS", "WIP", "IN", "PROGRESS"]:
                    return "Partial"
                elif status in ["PENDING", "TODO"]:
                    return "Pending"
                elif status in ["ACTIVE"]:
                    return "Active"
                return status.capitalize()

        # Check for status-like keywords in content
        if "Status: COMPLETE" in content or "**Status**: COMPLETE" in content:
            return "Complete"
        if "IN PROGRESS" in content.upper() or "IN_PROGRESS" in content.upper():
            return "Partial"

        # Default
        return "Unknown"

    def _extract_confidence(self, content: str) -> str:
        """Extract confidence level from content."""
        for pattern in CONFIDENCE_PATTERNS:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                conf = match.group(1).upper()
                # Validate it's a real confidence level
                valid_levels = [
                    "CERTAIN",
                    "HIGH",
                    "PROBABLE",
                    "MEDIUM",
                    "POSSIBLE",
                    "LOW",
                    "SPECULATIVE",
                ]
                if conf in valid_levels:
                    return conf

        # Try to infer from content (look for explicit mentions)
        content_upper = content.upper()
        if "CONFIDENCE**: HIGH" in content or "CONFIDENCE: HIGH" in content_upper:
            return "HIGH"
        elif "CONFIDENCE**: CERTAIN" in content or "CONFIDENCE: CERTAIN" in content_upper:
            return "CERTAIN"
        elif "VERIFIED" in content_upper or "EXACT MATCH" in content_upper:
            return "HIGH"
        elif "PROBABLE" in content_upper and "CONFIDENCE" in content_upper:
            return "PROBABLE"
        elif "POSSIBLE" in content_upper and "CONFIDENCE" in content_upper:
            return "POSSIBLE"
        elif "SPECULATIVE" in content_upper:
            return "SPECULATIVE"

        return "MEDIUM"

    def _extract_date(self, content: str, file_path: Path) -> str:
        """Extract analysis date from content or file modification time."""
        for pattern in DATE_PATTERNS:
            match = re.search(pattern, content)
            if match:
                return match.group(1)

        # Fallback to file modification date
        try:
            mtime = file_path.stat().st_mtime
            return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except Exception:
            return datetime.now().strftime("%Y-%m-%d")

    def _extract_site(self, inscription_id: str, content: str) -> str:
        """Extract site name from inscription ID or content."""
        # Parse site code from inscription ID
        match = re.match(r"([A-Z]{2})", inscription_id)
        if match:
            code = match.group(1)
            if code in SITE_CODES:
                return SITE_CODES[code]

        # Try to find explicit site mention in content
        site_pattern = r"\|\s*Site\s*\|\s*([^|]+)\s*\|"
        match = re.search(site_pattern, content, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return "Unknown"

    def _extract_key_findings(self, content: str) -> List[str]:
        """Extract key findings section from content."""
        findings = []

        # Look for Key Finding(s) section
        key_finding_patterns = [
            r"##\s*\d*\.?\s*Key\s+Findings?\s*\n(.*?)(?=\n##|\n---|\Z)",
            r"\*\*Key\s+Findings?\*\*:?\s*(.*?)(?=\n\n|\n##|\Z)",
            r"###\s*\d*\.?\s*Key\s+Findings?\s*\n(.*?)(?=\n##|\n---|\Z)",
        ]

        for pattern in key_finding_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                section = match.group(1).strip()
                # Extract bullet points or numbered items
                items = re.findall(r"^\s*[-*\d.]+\s*\*?\*?(.+?)(?:\*\*)?$", section, re.MULTILINE)
                if items:
                    # Clean up the items
                    cleaned = []
                    for item in items:
                        # Remove markdown formatting and leading colons
                        clean = re.sub(r"\*\*", "", item).strip()
                        clean = re.sub(r"^[:\s]+", "", clean)
                        if clean and len(clean) > 10:
                            cleaned.append(clean)
                    findings.extend(cleaned[:5])
                elif section:
                    # Take first sentence if no bullets
                    first_sentence = section.split(".")[0].strip()
                    first_sentence = re.sub(r"\*\*", "", first_sentence)
                    if first_sentence and len(first_sentence) > 10:
                        findings.append(first_sentence)
                break

        # Also check Executive Summary
        exec_summary_match = re.search(
            r"##\s*Executive\s+Summary\s*\n(.*?)(?=\n##|\n---|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        if exec_summary_match and not findings:
            summary = exec_summary_match.group(1).strip()
            items = re.findall(r"^\s*[-*\d.]+\s*\*?\*?(.+?)(?:\*\*)?$", summary, re.MULTILINE)
            if items:
                cleaned = []
                for item in items:
                    clean = re.sub(r"\*\*", "", item).strip()
                    clean = re.sub(r"^[:\s]+", "", clean)
                    if clean and len(clean) > 10:
                        cleaned.append(clean)
                findings.extend(cleaned[:3])

        return findings

    def _find_inscription_specific_finding(
        self, inscription_id: str, findings: List[str], content: str
    ) -> str:
        """Find key finding specific to an inscription."""
        # First check if any finding mentions this specific inscription
        insc_base = inscription_id.replace(" ", r"[\s-]?")
        for finding in findings:
            if re.search(insc_base, finding, re.IGNORECASE):
                return finding.strip()

        # Otherwise return first finding
        if findings:
            return findings[0].strip()

        # Try to extract from Analysis Registry if present
        registry_pattern = rf"\|\s*{re.escape(inscription_id)}\s*\|[^|]*\|[^|]*\|([^|]+)\|"
        match = re.search(registry_pattern, content)
        if match:
            finding = match.group(1).strip()
            finding = re.sub(r"\*\*", "", finding)
            return finding

        # Look for verification/confirmation patterns
        verify_patterns = [
            r"VERIFIED[:\s]+(.{20,100})",
            r"CONFIRMED[:\s]+(.{20,100})",
            r"confirms?[:\s]+(.{20,100})",
        ]
        for pattern in verify_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                finding = match.group(1).strip()
                finding = re.sub(r"\*\*", "", finding)
                return finding.split(".")[0] + "."

        # Fallback to first meaningful sentence after the header
        lines = content.split("\n")
        for line in lines[3:30]:  # Skip title, look in early content
            line = line.strip()
            # Skip headers, tables, metadata
            if (
                len(line) > 40
                and not line.startswith("#")
                and not line.startswith("|")
                and not line.startswith("**")
                and not line.startswith("---")
            ):
                # Clean up
                clean = re.sub(r"\*\*", "", line)
                clean = re.sub(r"\[.*?\]\(.*?\)", "", clean)  # Remove links
                clean = clean.strip()
                if len(clean) > 30:
                    return clean[:100] + ("..." if len(clean) > 100 else "")

        return "Analysis documented"


# ============================================================================
# INDEX GENERATOR
# ============================================================================


class IndexGenerator:
    """
    Generates ANALYSIS_INDEX.md content from parsed entries.
    """

    def __init__(self):
        self.entries: List[AnalysisEntry] = []

    def add_entries(self, entries: List[AnalysisEntry]):
        """Add entries, avoiding duplicates."""
        existing_ids = {e.inscription_id for e in self.entries}
        for entry in entries:
            if entry.inscription_id not in existing_ids:
                self.entries.append(entry)
                existing_ids.add(entry.inscription_id)

    def generate_table(self) -> str:
        """Generate markdown table of inscriptions."""
        if not self.entries:
            return "No entries found."

        # Sort by site, then by inscription number
        def sort_key(e):
            match = re.match(r"([A-Z]+)\s*(.+)", e.inscription_id)
            if match:
                site = match.group(1)
                num_part = match.group(2)
                # Extract leading number for sorting
                num_match = re.match(r"(\d+)", num_part)
                num = int(num_match.group(1)) if num_match else 999
                return (site, num, num_part)
            return (e.inscription_id, 0, "")

        sorted_entries = sorted(self.entries, key=sort_key)

        lines = [
            "| ID | Site | Status | Confidence | Key Finding | Analysis File | Date |",
            "|----|------|--------|------------|-------------|---------------|------|",
        ]

        for entry in sorted_entries:
            lines.append(entry.to_table_row())

        return "\n".join(lines)

    def generate_full_index(self) -> str:
        """Generate complete ANALYSIS_INDEX.md content."""
        now = datetime.now().strftime("%Y-%m-%d")

        content = f"""# Analysis Index

> **Index role**: This file is an analysis registry, not the canonical live status board.
> For current operational truth, use `linear-a-decipherer/MASTER_STATE.md`.

**Central registry of all Linear A analyses conducted in this project**

**Last Updated**: {now}

**Auto-generated by**: `tools/update_index.py`

---

## Inscriptions Analyzed

{self.generate_table()}

---

## Statistics

| Metric | Count |
|--------|-------|
| Total inscriptions analyzed | {len(self.entries)} |
| Complete analyses | {sum(1 for e in self.entries if e.status == "Complete")} |
| Partial analyses | {sum(1 for e in self.entries if e.status == "Partial")} |
| Pending analyses | {sum(1 for e in self.entries if e.status == "Pending")} |

### By Site

{self._generate_site_stats()}

### By Confidence Level

{self._generate_confidence_stats()}

---

## How to Use This Index

1. **Before starting new analysis**: Check if inscription already analyzed
2. **After completing analysis**: Run `python tools/update_index.py --write`
3. **Link format**: Analysis files should be in `analysis/active/` or `analysis/completed/`

---

*Index auto-generated by update_index.py*
"""
        return content

    def _generate_site_stats(self) -> str:
        """Generate site distribution statistics."""
        site_counts: Dict[str, int] = {}
        for entry in self.entries:
            site_counts[entry.site] = site_counts.get(entry.site, 0) + 1

        lines = ["| Site | Count |", "|------|-------|"]
        for site, count in sorted(site_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {site} | {count} |")

        return "\n".join(lines)

    def _generate_confidence_stats(self) -> str:
        """Generate confidence level statistics."""
        conf_counts: Dict[str, int] = {}
        for entry in self.entries:
            conf_counts[entry.confidence] = conf_counts.get(entry.confidence, 0) + 1

        lines = ["| Confidence | Count |", "|------------|-------|"]
        order = ["CERTAIN", "HIGH", "PROBABLE", "POSSIBLE", "MEDIUM", "SPECULATIVE", "Unknown"]
        for conf in order:
            if conf in conf_counts:
                lines.append(f"| {conf} | {conf_counts[conf]} |")

        return "\n".join(lines)


# ============================================================================
# MAIN SCANNER
# ============================================================================


class IndexScanner:
    """
    Main scanner that coordinates file discovery and parsing.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.parser = AnalysisFileParser(verbose=verbose)
        self.generator = IndexGenerator()

    def log(self, msg: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"[SCAN] {msg}")

    def scan_directories(self) -> List[AnalysisEntry]:
        """Scan analysis directories for markdown files."""
        all_entries = []

        directories = [ACTIVE_DIR, COMPLETED_DIR]

        for directory in directories:
            if not directory.exists():
                self.log(f"Directory not found: {directory}")
                continue

            self.log(f"Scanning: {directory}")

            # Find all markdown files recursively
            md_files = list(directory.glob("**/*.md"))
            self.log(f"Found {len(md_files)} markdown files")

            for md_file in md_files:
                # Skip index files themselves
                if "INDEX" in md_file.name.upper():
                    continue

                entries = self.parser.parse_file(md_file)
                all_entries.extend(entries)

        return all_entries

    def run(self, write: bool = False, json_output: bool = False) -> int:
        """
        Run the scanner and optionally update the index.

        Args:
            write: If True, write changes to ANALYSIS_INDEX.md
            json_output: If True, output as JSON instead of markdown

        Returns:
            Exit code (0 for success)
        """
        if not json_output:
            print("=" * 60)
            print("LINEAR A ANALYSIS INDEX UPDATER")
            print("=" * 60)

        # Scan directories
        entries = self.scan_directories()
        if not json_output:
            print(f"\nFound {len(entries)} inscription entries")

        if not entries:
            print("No analysis entries found.")
            return 1

        # Add to generator
        self.generator.add_entries(entries)

        # Output
        if json_output:
            output = {
                "generated": datetime.now().isoformat(),
                "entries": [asdict(e) for e in self.generator.entries],
                "statistics": {
                    "total": len(self.generator.entries),
                    "complete": sum(1 for e in self.generator.entries if e.status == "Complete"),
                },
            }
            # Remove file_path from JSON output (not serializable)
            for entry in output["entries"]:
                entry.pop("file_path", None)
            print(json.dumps(output, indent=2, ensure_ascii=False))
            return 0
        else:
            # Generate markdown
            content = self.generator.generate_full_index()

            if write:
                # Ensure parent directory exists
                INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

                # Write to file
                INDEX_PATH.write_text(content, encoding="utf-8")
                print(f"\nIndex written to: {INDEX_PATH}")
            else:
                # Preview mode
                print("\n" + "=" * 60)
                print("PREVIEW (use --write to save)")
                print("=" * 60)
                print(content)

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total inscriptions: {len(self.generator.entries)}")
        print(f"Complete: {sum(1 for e in self.generator.entries if e.status == 'Complete')}")
        print(f"Partial: {sum(1 for e in self.generator.entries if e.status == 'Partial')}")

        # Site breakdown
        sites = {}
        for e in self.generator.entries:
            sites[e.site] = sites.get(e.site, 0) + 1
        print("\nBy site:")
        for site, count in sorted(sites.items(), key=lambda x: -x[1]):
            print(f"  {site}: {count}")

        return 0


# ============================================================================
# CLI
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Auto-update ANALYSIS_INDEX.md from analysis files"
    )
    parser.add_argument(
        "--write",
        "-w",
        action="store_true",
        help="Write changes to ANALYSIS_INDEX.md (default: preview only)",
    )
    parser.add_argument(
        "--json", "-j", action="store_true", help="Output as JSON instead of markdown"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed parsing information"
    )

    args = parser.parse_args()

    scanner = IndexScanner(verbose=args.verbose)
    return scanner.run(write=args.write, json_output=args.json)


if __name__ == "__main__":
    sys.exit(main())
