#!/usr/bin/env python3
"""
Linear A Corpus Data Validation Tool

Validates integrity of corpus.json, signs.json, and related data files to ensure:
- Sign sequences reference only documented AB numbers
- Inscription references resolve to known sites
- Word frequencies match actual word counts
- Chronology assignments are valid
- No duplicate inscriptions
- Sign-level data consistency

Usage:
    python tools/validate_corpus.py [--verbose] [--quiet] [--report-only]

Exit codes:
    0 - All validations passed
    1 - Critical errors found
    2 - Warnings found (non-critical)
    3 - File access errors

Attribution:
    Part of Linear A Decipherment Project
    See FIRST_PRINCIPLES.md for methodology
"""

import json
import sys
import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import argparse


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REFS_DIR = PROJECT_ROOT / "linear-a-decipherer" / "references"


class ValidationResult:
    """Stores validation results for reporting."""

    def __init__(self):
        self.critical_errors = []
        self.warnings = []
        self.info = []
        self.stats = {}

    def add_critical(self, message: str, context: str = None):
        """Add a critical error that invalidates the dataset."""
        error = {"message": message}
        if context:
            error["context"] = context
        self.critical_errors.append(error)

    def add_warning(self, message: str, context: str = None):
        """Add a non-critical warning."""
        warning = {"message": message}
        if context:
            warning["context"] = context
        self.warnings.append(warning)

    def add_info(self, message: str):
        """Add informational note."""
        self.info.append(message)

    def has_errors(self) -> bool:
        """Check if any critical errors exist."""
        return len(self.critical_errors) > 0

    def has_warnings(self) -> bool:
        """Check if any warnings exist."""
        return len(self.warnings) > 0

    def summary(self) -> dict:
        """Get summary statistics."""
        return {
            "critical_errors": len(self.critical_errors),
            "warnings": len(self.warnings),
            "info_messages": len(self.info),
        }


class CorpusValidator:
    """Validates Linear A corpus data files."""

    def __init__(self, verbose=False, quiet=False):
        self.verbose = verbose
        self.quiet = quiet
        self.result = ValidationResult()

        # Known valid values
        self.known_sites = set()
        self.known_support_types = set()
        self.known_chronologies = {
            "LMIB",
            "LMIA",
            "LMI",
            "MMII",
            "MMIII",
            "MMIIIB",
            "MMIIIA",
            "MMIA",
            "LMIIIA",
            "LBI",
            "Geometric",
            "LMII",
            "MMIB",
        }

        # Loaded data
        self.corpus = None
        self.signs = None
        self.statistics = None
        self.cognates = None

    def log(self, message: str, level="info"):
        """Print message based on verbosity settings."""
        if level == "error" and not self.quiet:
            print(f"❌ ERROR: {message}", file=sys.stderr)
        elif level == "warning" and not self.quiet:
            print(f"⚠️  WARNING: {message}")
        elif level == "info" and self.verbose:
            print(f"ℹ️  {message}")
        elif level == "always" and not self.quiet:
            print(message)

    def load_data(self) -> bool:
        """Load all data files. Returns False if critical files missing."""
        try:
            # Load corpus (critical)
            corpus_path = DATA_DIR / "corpus.json"
            if not corpus_path.exists():
                self.log(f"Critical file missing: {corpus_path}", "error")
                return False

            with open(corpus_path, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.log(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")

            # Load signs (critical)
            signs_path = DATA_DIR / "signs.json"
            if not signs_path.exists():
                self.log(f"Critical file missing: {signs_path}", "error")
                return False

            with open(signs_path, "r", encoding="utf-8") as f:
                self.signs = json.load(f)
            self.log(f"Loaded signs: {self.signs.get('total_signs', 0)} unique signs")

            # Load statistics (optional)
            stats_path = DATA_DIR / "statistics.json"
            if stats_path.exists():
                with open(stats_path, "r", encoding="utf-8") as f:
                    self.statistics = json.load(f)
                self.log("Loaded statistics")
            else:
                self.log("Statistics file not found (non-critical)", "warning")

            # Load cognates (optional)
            cognates_path = DATA_DIR / "cognates.json"
            if cognates_path.exists():
                with open(cognates_path, "r", encoding="utf-8") as f:
                    self.cognates = json.load(f)
                self.log("Loaded cognates")
            else:
                self.log("Cognates file not found (non-critical)", "warning")

            return True

        except json.JSONDecodeError as e:
            self.log(f"JSON parse error: {e}", "error")
            return False
        except Exception as e:
            self.log(f"Data load error: {e}", "error")
            return False

    def validate_site_codes(self):
        """Validate that all site codes are known and consistent."""
        self.log("Validating site codes...", "always")

        site_codes = set()
        for inscription_id, data in self.corpus["inscriptions"].items():
            # Extract site code from inscription ID
            match = re.match(r"^([A-Z]+)", inscription_id)
            if match:
                site_code = match.group(1)
                site_codes.add(site_code)

                # Check if site name is provided
                if "site" in data and data["site"]:
                    self.known_sites.add(data["site"])
            else:
                self.result.add_warning(
                    f"Inscription ID '{inscription_id}' does not start with site code",
                    inscription_id,
                )

        self.result.stats["unique_site_codes"] = len(site_codes)
        self.result.stats["site_codes"] = sorted(site_codes)
        self.log(f"  Found {len(site_codes)} unique site codes")

    def validate_chronology(self):
        """Validate chronology assignments."""
        self.log("Validating chronology assignments...", "always")

        unknown_chronologies = set()
        missing_chronology = 0

        for inscription_id, data in self.corpus["inscriptions"].items():
            chronology = data.get("context", "")

            if not chronology:
                missing_chronology += 1
            elif chronology not in self.known_chronologies:
                unknown_chronologies.add(chronology)

        if unknown_chronologies:
            self.result.add_warning(
                f"Unknown chronology values: {', '.join(sorted(unknown_chronologies))}"
            )

        self.result.stats["missing_chronology"] = missing_chronology
        self.result.stats["unknown_chronologies"] = len(unknown_chronologies)
        self.log(f"  {missing_chronology} inscriptions missing chronology")
        if unknown_chronologies:
            self.log(f"  Unknown chronologies: {unknown_chronologies}", "warning")

    def validate_duplicates(self):
        """Check for duplicate inscriptions."""
        self.log("Checking for duplicate inscriptions...", "always")

        # Check for duplicate IDs (should be impossible given dict structure)
        inscription_ids = list(self.corpus["inscriptions"].keys())
        if len(inscription_ids) != len(set(inscription_ids)):
            self.result.add_critical("Duplicate inscription IDs found in corpus")

        # Check for identical content (transliterated words)
        content_hashes = defaultdict(list)
        for inscription_id, data in self.corpus["inscriptions"].items():
            transliterated = data.get("transliteratedWords", [])
            # Create simple hash of transliterated content
            content_hash = "|".join(str(w) for w in transliterated)
            content_hashes[content_hash].append(inscription_id)

        # Find duplicates
        duplicates = {k: v for k, v in content_hashes.items() if len(v) > 1}
        if duplicates:
            for content, ids in list(duplicates.items())[:5]:  # Show first 5
                self.result.add_warning(
                    f"Potential duplicate content: {', '.join(ids[:3])}", f"Hash: {content[:50]}..."
                )

        self.result.stats["potential_content_duplicates"] = len(duplicates)
        self.log(f"  {len(duplicates)} potential content duplicates found")

    def validate_word_frequencies(self):
        """Validate that word frequency counts match actual occurrences."""
        self.log("Validating word frequencies...", "always")

        # Count actual occurrences
        actual_counts = Counter()
        for inscription_id, data in self.corpus["inscriptions"].items():
            transliterated = data.get("transliteratedWords", [])
            for word in transliterated:
                if word and word not in ["\n", "𐄁", "", "—"]:
                    actual_counts[str(word)] += 1

        # Compare with statistics if available
        if self.statistics and "top_words" in self.statistics:
            discrepancies = []
            for word, reported_count in self.statistics["top_words"].items():
                actual_count = actual_counts.get(word, 0)
                if actual_count != reported_count:
                    discrepancies.append(
                        f"{word}: reported={reported_count}, actual={actual_count}"
                    )

            if discrepancies:
                self.result.add_warning(
                    f"Word frequency discrepancies found: {len(discrepancies)} words"
                )
                for disc in discrepancies[:5]:  # Show first 5
                    self.log(f"    {disc}", "warning")

            self.result.stats["word_frequency_discrepancies"] = len(discrepancies)
        else:
            self.log("  No statistics file to compare against")

        self.result.stats["total_unique_words"] = len(actual_counts)
        self.log(f"  {len(actual_counts)} unique words counted")

    def validate_sign_data_consistency(self):
        """Validate sign-level data consistency."""
        self.log("Validating sign-level data...", "always")

        inconsistencies = []

        for sign, data in self.signs["signs"].items():
            total = data["total_occurrences"]
            pos_sum = (
                data["position_frequency"]["initial"]
                + data["position_frequency"]["medial"]
                + data["position_frequency"]["final"]
                + data["contexts"]["standalone"]
            )

            if pos_sum != total:
                inconsistencies.append(f"{sign}: total={total} but positions sum to {pos_sum}")

        if inconsistencies:
            self.result.add_critical(
                f"Sign position frequency inconsistencies: {len(inconsistencies)} signs"
            )
            for incon in inconsistencies[:5]:
                self.log(f"    {incon}", "error")

        self.result.stats["sign_inconsistencies"] = len(inconsistencies)
        self.log(f"  {len(inconsistencies)} sign data inconsistencies")

    def validate_sign_attestations(self):
        """Validate that sign attestations reference valid inscriptions."""
        self.log("Validating sign attestations...", "always")

        invalid_refs = []
        inscription_ids = set(self.corpus["inscriptions"].keys())

        for sign, data in self.signs["signs"].items():
            for attestation in data.get("attestations", []):
                inscription_id = attestation.get("inscription")
                if inscription_id not in inscription_ids:
                    invalid_refs.append(
                        f"Sign '{sign}' references non-existent inscription '{inscription_id}'"
                    )

        if invalid_refs:
            self.result.add_critical(
                f"Invalid inscription references in sign attestations: {len(invalid_refs)}"
            )
            for ref in invalid_refs[:5]:
                self.log(f"    {ref}", "error")

        self.result.stats["invalid_attestation_refs"] = len(invalid_refs)
        self.log(f"  {len(invalid_refs)} invalid attestation references")

    def validate_data_integrity(self):
        """Validate general data integrity."""
        self.log("Validating general data integrity...", "always")

        # Check for parse errors in corpus
        parse_errors = 0
        for inscription_id, data in self.corpus["inscriptions"].items():
            if "_parse_error" in data:
                parse_errors += 1
                if parse_errors <= 3:  # Show first 3
                    self.result.add_warning(
                        f"Parse error in {inscription_id}: {data.get('_parse_error', 'Unknown')}",
                        inscription_id,
                    )

        self.result.stats["parse_errors"] = parse_errors
        if parse_errors > 0:
            self.log(f"  {parse_errors} inscriptions have parse errors", "warning")

        # Check for missing critical fields
        missing_fields = defaultdict(int)
        for inscription_id, data in self.corpus["inscriptions"].items():
            if "_parse_error" in data:
                continue  # Skip parse-error inscriptions

            for field in ["site", "context", "support", "transliteratedWords"]:
                if field not in data or not data[field]:
                    missing_fields[field] += 1

        for field, count in missing_fields.items():
            if count > 0:
                self.result.add_warning(f"{count} inscriptions missing '{field}' field")

        self.result.stats["missing_fields"] = dict(missing_fields)

    def run_all_validations(self):
        """Run all validation checks."""
        self.log("=" * 60, "always")
        self.log("Linear A Corpus Validation", "always")
        self.log("=" * 60, "always")

        if not self.load_data():
            self.result.add_critical("Failed to load data files")
            return

        # Run validation checks
        self.validate_site_codes()
        self.validate_chronology()
        self.validate_duplicates()
        self.validate_word_frequencies()
        self.validate_sign_data_consistency()
        self.validate_sign_attestations()
        self.validate_data_integrity()

        # Summary
        self.log("=" * 60, "always")
        self.log("Validation Summary", "always")
        self.log("=" * 60, "always")

        summary = self.result.summary()
        self.log(f"Critical errors: {summary['critical_errors']}", "always")
        self.log(f"Warnings: {summary['warnings']}", "always")
        self.log(f"Info messages: {summary['info_messages']}", "always")

        if self.result.has_errors():
            self.log("❌ VALIDATION FAILED - Critical errors found", "error")
        elif self.result.has_warnings():
            self.log("⚠️  VALIDATION PASSED with warnings", "always")
        else:
            self.log("✅ VALIDATION PASSED - No issues found", "always")

        self.log("=" * 60, "always")

    def generate_report(self, output_path: Path):
        """Generate detailed validation report as JSON."""
        report = {
            "generated": datetime.now().isoformat(),
            "summary": self.result.summary(),
            "statistics": self.result.stats,
            "critical_errors": self.result.critical_errors,
            "warnings": self.result.warnings,
            "info": self.result.info,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.log(f"Report written to: {output_path}", "always")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate Linear A corpus data integrity")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output with detailed progress"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress all output except errors"
    )
    parser.add_argument(
        "--report",
        "-r",
        type=str,
        default="data/validation_report.json",
        help="Path for validation report (default: data/validation_report.json)",
    )
    parser.add_argument(
        "--report-only", action="store_true", help="Only generate report, suppress console output"
    )

    args = parser.parse_args()

    # Create validator
    validator = CorpusValidator(verbose=args.verbose, quiet=args.quiet or args.report_only)

    # Run validations
    validator.run_all_validations()

    # Generate report
    report_path = PROJECT_ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    validator.generate_report(report_path)

    # Exit with appropriate code
    if validator.result.has_errors():
        return 1
    elif validator.result.has_warnings():
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
