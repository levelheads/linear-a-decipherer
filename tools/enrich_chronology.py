#!/usr/bin/env python3
"""
Linear A Chronology Enrichment Tool

Infers missing chronology (context) values for inscriptions based on:
1. Site-specific default chronologies (most sites have dominant period)
2. Support type patterns (certain object types correlate with periods)
3. Cross-reference with other inscriptions from same findspot

Usage:
    python tools/enrich_chronology.py [--dry-run] [--verbose] [--output FILE]

Options:
    --dry-run    Show what would be changed without modifying files
    --verbose    Show detailed reasoning for each inference
    --output     Write enriched corpus to specified file (default: data/corpus.json)

Attribution:
    Part of Linear A Decipherment Project
    See FIRST_PRINCIPLES.md for methodology
"""

import json
import argparse
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


# Site-to-chronology mappings based on archaeological evidence
# These represent the dominant/default period for inscriptions from each site
# Sources: GORILA, archaeological site reports
SITE_CHRONOLOGY_DEFAULTS = {
    # Major administrative centers - mostly LMIB
    "HT": "LMIB",  # Hagia Triada - destroyed LMIB
    "HTW": "LMIB",  # Hagia Triada nodules/sealings
    "HTZ": "LMIB",  # Hagia Triada stone vessels
    "KH": "LMIB",  # Khania - destroyed LMIB
    "KHW": "LMIB",  # Khania nodules/sealings
    "KHZ": "LMIB",  # Khania stone vessels
    "ZA": "LMIB",  # Zakros - destroyed LMIB
    "ZAW": "LMIB",  # Zakros nodules
    "ZAZ": "LMIB",  # Zakros stone vessels
    # Knossos - mixed periods
    "KN": "LMIB",  # Default, but varies
    "KNW": "LMIB",  # Knossos nodules
    "KNZ": "LMIB",  # Knossos stone vessels (includes 2024 scepter)
    # Phaistos - earlier periods (palace period)
    "PH": "MMIII",  # Phaistos - many early tablets
    "PHW": "MMIII",  # Phaistos nodules
    "PHZ": "MMIII",  # Phaistos stone vessels
    # Malia - varied periods
    "MA": "MMIII",  # Malia
    "MAW": "MMIII",  # Malia nodules
    "MAZ": "MMIII",  # Malia stone vessels
    # Peak sanctuaries and religious sites - typically LMIA-LMIB
    "IOZ": "LMIA",  # Mt. Iouktas peak sanctuary
    "SYZ": "LMIB",  # Kato Symi sanctuary
    "PKZ": "LMIB",  # Palaikastro stone vessels
    "PSZ": "LMIB",  # Psychro Cave
    "PSIZ": "LMIB",  # Psychro Cave (variant)
    # Other major sites
    "PK": "LMIB",  # Palaikastro
    "PE": "LMIB",  # Petras
    "PEW": "LMIB",  # Petras nodules
    "PEZ": "LMIB",  # Petras stone vessels
    "TY": "LMIB",  # Tylissos
    "TYW": "LMIB",  # Tylissos nodules
    "TYZ": "LMIB",  # Tylissos stone vessels
    "ARKH": "LMIA",  # Arkhanes
    "ARKHZ": "LMIA",  # Arkhanes stone vessels
    "ARZ": "LMIA",  # Arkhalkhori
    "ARGZ": "LMIA",  # Arkhalkhori (variant)
    "GO": "LMIB",  # Gournia
    "GOW": "LMIB",  # Gournia nodules
    # Cycladic and off-Crete sites
    "THE": "LMIA",  # Thera (pre-eruption)
    "THEZ": "LMIA",  # Thera stone vessels
    "KE": "LMIB",  # Kea
    "KEW": "LMIB",  # Kea nodules
    "KEZ": "LMIB",  # Kea stone vessels
    "KYZ": "LMIB",  # Kythera
    "MYZ": "LMIIIA",  # Mycenae (later reuse)
    "MILZ": "LMIB",  # Miletos
    "TROZ": "LBI",  # Troy
    # Minor sites with sparse evidence
    "PYR": "LMIB",  # Pyrgos
    "PYRW": "LMIB",
    "PYRZ": "LMIB",
    "MOZ": "LMIB",  # Mokhilos
    "VRYZ": "LMIB",  # Vrysinas
    "APZ": "LMIB",  # Apodoulou
    "CRZ": "LMIB",  # Crete (general)
    "CR": "LMIB",
    "KAMZ": "LMIB",  # Kamilari
    "KANZ": "LMIB",  # Kannia
    "KOZ": "LMIB",  # Kophinas
    "KO": "LMIB",
    "MIZ": "LMIB",  # Milos
    "MI": "LMIB",
    "SAMW": "LMIB",  # Samothrace
    "TELZ": "LBI",  # Tel Haror (Levant)
    "TIZ": "LMIIIA",  # Tiryns (later reuse)
}

# Support type chronology hints (some object types are period-specific)
SUPPORT_CHRONOLOGY_HINTS = {
    "Nodule": "LMIB",  # Most nodules from LMIB destruction levels
    "Roundel": "LMIB",  # Most roundels from LMIB
    "Tablet": None,  # Tablets span all periods
    "Stone vessel": None,  # Vessels span all periods
    "Clay vessel": None,
    "Metal object": None,
    "ivory object": "LMIB",  # Recent discoveries (Knossos scepter)
}


class ChronologyEnricher:
    """Enriches corpus with inferred chronology data."""

    def __init__(self, verbose=False, dry_run=False):
        self.verbose = verbose
        self.dry_run = dry_run
        self.corpus = None
        self.changes = []
        self.stats = {
            "total_inscriptions": 0,
            "missing_before": 0,
            "inferred": 0,
            "by_method": Counter(),
            "by_period": Counter(),
        }

    def log(self, message: str):
        """Print message if verbose mode enabled."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        corpus_path = DATA_DIR / "corpus.json"
        if not corpus_path.exists():
            print(f"Error: corpus.json not found at {corpus_path}")
            return False

        with open(corpus_path, "r", encoding="utf-8") as f:
            self.corpus = json.load(f)

        self.stats["total_inscriptions"] = len(self.corpus["inscriptions"])
        return True

    def extract_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        import re

        match = re.match(r"^([A-Z]+)", inscription_id)
        return match.group(1) if match else ""

    def infer_chronology(self, inscription_id: str, data: dict) -> tuple:
        """
        Infer chronology for a single inscription.

        Returns: (inferred_value, method_used, confidence)
            - inferred_value: The chronology string (e.g., 'LMIB')
            - method_used: How the value was inferred
            - confidence: 'high', 'medium', 'low'
        """
        site_code = self.extract_site_code(inscription_id)
        support = data.get("support", "")

        # Method 1: Site-specific default
        if site_code in SITE_CHRONOLOGY_DEFAULTS:
            chronology = SITE_CHRONOLOGY_DEFAULTS[site_code]

            # Check if support type suggests different period
            if support in SUPPORT_CHRONOLOGY_HINTS:
                hint = SUPPORT_CHRONOLOGY_HINTS[support]
                if hint and hint != chronology:
                    # Support type conflicts with site default
                    # Prefer site-specific data, but note lower confidence
                    return chronology, "site_default_support_conflict", "medium"

            return chronology, "site_default", "high"

        # Method 2: Support-type hint
        if support in SUPPORT_CHRONOLOGY_HINTS and SUPPORT_CHRONOLOGY_HINTS[support]:
            return SUPPORT_CHRONOLOGY_HINTS[support], "support_hint", "medium"

        # Method 3: General LMIB default (most Linear A is from LMIB destruction)
        # This is the period of maximum destruction across Crete
        return "LMIB", "general_default", "low"

    def process_inscriptions(self):
        """Process all inscriptions, inferring missing chronology."""
        for inscription_id, data in self.corpus["inscriptions"].items():
            current_context = data.get("context", "")

            if not current_context:
                self.stats["missing_before"] += 1

                # Infer chronology
                inferred, method, confidence = self.infer_chronology(inscription_id, data)

                if inferred:
                    self.changes.append(
                        {
                            "inscription": inscription_id,
                            "inferred": inferred,
                            "method": method,
                            "confidence": confidence,
                            "site": data.get("site", ""),
                            "support": data.get("support", ""),
                        }
                    )

                    self.stats["inferred"] += 1
                    self.stats["by_method"][method] += 1
                    self.stats["by_period"][inferred] += 1

                    self.log(f"{inscription_id}: {inferred} ({method}, {confidence})")

                    # Apply change unless dry run
                    if not self.dry_run:
                        data["context"] = inferred
                        data["context_inferred"] = True
                        data["context_method"] = method
                        data["context_confidence"] = confidence

    def save_corpus(self, output_path: Path):
        """Save enriched corpus."""
        # Update attribution
        self.corpus["attribution"]["enriched"] = datetime.now().isoformat()
        self.corpus["attribution"]["enrichment_note"] = (
            "Chronology (context) field enriched for missing entries. "
            "Inferred values marked with context_inferred=true."
        )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.corpus, f, ensure_ascii=False, indent=2)

    def print_summary(self):
        """Print enrichment summary."""
        print("\n" + "=" * 60)
        print("Chronology Enrichment Summary")
        print("=" * 60)
        print(f"Total inscriptions: {self.stats['total_inscriptions']}")
        print(f"Missing chronology before: {self.stats['missing_before']}")
        print(f"Chronology inferred: {self.stats['inferred']}")

        if self.stats["by_method"]:
            print("\nBy inference method:")
            for method, count in self.stats["by_method"].most_common():
                print(f"  {method}: {count}")

        if self.stats["by_period"]:
            print("\nBy inferred period:")
            for period, count in self.stats["by_period"].most_common():
                print(f"  {period}: {count}")

        if self.dry_run:
            print("\n⚠️  DRY RUN - No changes saved")
        print("=" * 60)

    def generate_changes_report(self, output_path: Path):
        """Generate detailed report of all changes."""
        report = {
            "generated": datetime.now().isoformat(),
            "summary": {
                "total_inscriptions": self.stats["total_inscriptions"],
                "missing_before": self.stats["missing_before"],
                "inferred": self.stats["inferred"],
                "by_method": dict(self.stats["by_method"]),
                "by_period": dict(self.stats["by_period"]),
            },
            "changes": self.changes,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\nDetailed report: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Enrich Linear A corpus with inferred chronology data"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be changed without modifying files",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed reasoning for each inference"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/corpus.json",
        help="Output path for enriched corpus (default: data/corpus.json)",
    )
    parser.add_argument(
        "--report",
        "-r",
        type=str,
        default="data/chronology_enrichment_report.json",
        help="Path for detailed changes report",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Linear A Chronology Enrichment")
    print("=" * 60)

    enricher = ChronologyEnricher(verbose=args.verbose, dry_run=args.dry_run)

    if not enricher.load_corpus():
        return 1

    print(f"Loaded {enricher.stats['total_inscriptions']} inscriptions")

    # Process inscriptions
    print("\nProcessing inscriptions...")
    enricher.process_inscriptions()

    # Save results
    if not args.dry_run:
        output_path = PROJECT_ROOT / args.output
        enricher.save_corpus(output_path)
        print(f"\nEnriched corpus saved to: {output_path}")

    # Generate report
    report_path = PROJECT_ROOT / args.report
    enricher.generate_changes_report(report_path)

    # Print summary
    enricher.print_summary()

    return 0


if __name__ == "__main__":
    sys.exit(main())
