#!/usr/bin/env python3
"""
Arithmetic Verifier for Linear A

Extends corpus_auditor.py --totals with:
1. Mismatch diagnosis: Why do 25 tablets fail? (lacuna, multi-commodity, fractions)
2. Sub-total detection: Commodity-specific KU-RO lines
3. Rosetta skeleton output: Structural position tagging for VERIFIED tablets
4. KI-RO verification: Test (sum - KI-RO) = KU-RO hypothesis

Usage:
    python3 tools/arithmetic_verifier.py --all
    python3 tools/arithmetic_verifier.py --tablet HT9b
    python3 tools/arithmetic_verifier.py --diagnose
    python3 tools/arithmetic_verifier.py --skeleton HT117a
    python3 tools/arithmetic_verifier.py --output data/arithmetic_verification.json

Attribution:
    Part of Linear A Decipherment Project
    Builds on corpus_auditor.py arithmetic validation
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import Counter
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from fractions import Fraction


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"

# Known commodity logograms
COMMODITY_LOGOGRAMS = {
    "GRA",
    "VIN",
    "OLE",
    "OLIV",
    "FIC",
    "FAR",
    "CYP",
    "OVI",
    "CAP",
    "SUS",
    "BOS",
    "VIR",
    "MUL",
    "TELA",
}

COMMODITY_LIGATURE_BASES = {"OLE", "VIN", "GRA", "FIC", "CYP", "VIR", "TELA"}

# Fraction mappings
FRACTION_MAP = {
    "¹⁄₂": Fraction(1, 2),
    "½": Fraction(1, 2),
    "¹⁄₄": Fraction(1, 4),
    "¼": Fraction(1, 4),
    "³⁄₄": Fraction(3, 4),
    "¾": Fraction(3, 4),
    "¹⁄₃": Fraction(1, 3),
    "⅓": Fraction(1, 3),
    "²⁄₃": Fraction(2, 3),
    "⅔": Fraction(2, 3),
    "¹⁄₈": Fraction(1, 8),
    "⅛": Fraction(1, 8),
    "³⁄₈": Fraction(3, 8),
    "⅜": Fraction(3, 8),
    "¹⁄₁₆": Fraction(1, 16),
    "~¹⁄₆": Fraction(1, 6),
    "¹⁄₆": Fraction(1, 6),
    "J": Fraction(1, 4),  # AB 164
    "E": Fraction(1, 2),  # AB 162
    "F": Fraction(1, 3),  # AB 163
    "K": Fraction(1, 8),  # AB 165
    "L": Fraction(1, 16),  # AB 166
}


@dataclass
class StructuralPosition:
    """A word's structural role within a tablet."""

    word: str
    position_idx: int
    role: str  # 'header', 'recipient', 'commodity', 'quantity', 'total', 'deficit', 'unknown'
    commodity_context: Optional[str] = None
    quantity: Optional[float] = None
    confidence: str = "INFERRED"
    notes: str = ""


@dataclass
class MismatchDiagnosis:
    """Diagnosis of why a KU-RO mismatch occurs."""

    tablet_id: str
    kuro_value: float
    computed_sum: float
    difference: float
    diagnosis: (
        str  # 'lacuna', 'multi_commodity', 'fraction_parsing', 'multi_kuro', 'damaged', 'unknown'
    )
    explanation: str
    confidence: str  # 'CERTAIN', 'PROBABLE', 'POSSIBLE'


@dataclass
class TabletVerification:
    """Complete verification result for a tablet."""

    tablet_id: str
    site: str
    has_kuro: bool
    has_kiro: bool
    kuro_status: str  # VERIFIED, PARTIAL, MISMATCH, INCOMPLETE, NO_KURO
    kuro_value: Optional[float] = None
    computed_sum: Optional[float] = None
    difference: Optional[float] = None
    item_count: int = 0
    diagnosis: Optional[MismatchDiagnosis] = None
    skeleton: List[StructuralPosition] = field(default_factory=list)
    kiro_verification: Optional[Dict] = None


class ArithmeticVerifier:
    """Arithmetic verification and structural position tagging for Linear A tablets."""

    def __init__(self):
        self.corpus = {}
        self.inscriptions = {}

    def load_corpus(self) -> bool:
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def _parse_number(self, token: str) -> Optional[Fraction]:
        """Parse a token as a number (integer or fraction)."""
        if token in FRACTION_MAP:
            return FRACTION_MAP[token]
        try:
            return Fraction(int(token))
        except ValueError:
            pass
        match = re.match(r"^(\d+)\s+(\d+)/(\d+)$", token)
        if match:
            whole, num, denom = int(match.group(1)), int(match.group(2)), int(match.group(3))
            return Fraction(whole * denom + num, denom)
        match = re.match(r"^(\d+)/(\d+)$", token)
        if match:
            return Fraction(int(match.group(1)), int(match.group(2)))
        return None

    def _is_logogram(self, token: str) -> bool:
        if token in COMMODITY_LOGOGRAMS:
            return True
        if "+" in token:
            base = token.split("+")[0]
            return base in COMMODITY_LIGATURE_BASES
        return False

    def _get_base_commodity(self, token: str) -> str:
        """Get base commodity from logogram (handles ligatures)."""
        if "+" in token:
            return token.split("+")[0]
        return token

    def _is_word(self, token: str) -> bool:
        if token in {"\n", "𐄁", "", " ", "—", ","}:
            return False
        if self._parse_number(token) is not None:
            return False
        if self._is_logogram(token):
            return False
        if token.startswith('"'):
            return False
        if token == "*":
            return False
        return True

    def _extract_site(self, tablet_id: str) -> str:
        match = re.match(r"^([A-Z]+)", tablet_id)
        return match.group(1) if match else "UNKNOWN"

    def _has_lacuna_markers(self, words: List[str]) -> bool:
        """Check if tablet has lacuna/damage indicators."""
        for w in words:
            if any(c in w for c in ["[", "]", "?", "…", "vacat"]):
                return True
        return False

    def _count_commodities(self, words: List[str]) -> Set[str]:
        """Count distinct commodity types on a tablet."""
        commodities = set()
        for w in words:
            if self._is_logogram(w):
                commodities.add(self._get_base_commodity(w))
        return commodities

    def _count_kuro_instances(self, words: List[str]) -> int:
        """Count KU-RO instances."""
        return words.count("KU-RO")

    def verify_tablet(self, tablet_id: str) -> Optional[TabletVerification]:
        """Full verification of a single tablet."""
        tablet_data = self.inscriptions.get(tablet_id)
        if not tablet_data:
            return None

        words = tablet_data.get("transliteratedWords", [])
        has_kuro = "KU-RO" in words
        has_kiro = "KI-RO" in words
        site = self._extract_site(tablet_id)

        if not has_kuro:
            skeleton = self._build_skeleton(tablet_id, words) if len(words) > 0 else []
            return TabletVerification(
                tablet_id=tablet_id,
                site=site,
                has_kuro=False,
                has_kiro=has_kiro,
                kuro_status="NO_KURO",
                skeleton=skeleton,
            )

        # Perform arithmetic verification
        kuro_indices = [i for i, w in enumerate(words) if w == "KU-RO"]

        # Use the LAST KU-RO (often the grand total)
        kuro_idx = kuro_indices[-1]

        # Get KU-RO value
        kuro_value = Fraction(0)
        for i in range(kuro_idx + 1, min(kuro_idx + 4, len(words))):
            if words[i] == "\n":
                break
            num = self._parse_number(words[i])
            if num is not None:
                kuro_value += num

        if kuro_value == 0:
            return TabletVerification(
                tablet_id=tablet_id,
                site=site,
                has_kuro=True,
                has_kiro=has_kiro,
                kuro_status="INCOMPLETE",
                skeleton=self._build_skeleton(tablet_id, words),
            )

        # Sum preceding amounts
        items = []
        computed_sum = Fraction(0)
        current_entity = None
        current_amount = Fraction(0)

        for i in range(kuro_idx):
            token = words[i]
            if token == "\n":
                if current_entity and current_amount > 0:
                    items.append((current_entity, current_amount))
                    computed_sum += current_amount
                current_entity = None
                current_amount = Fraction(0)
            elif self._is_word(token) and not self._is_logogram(token):
                if current_entity is None:
                    current_entity = token
            else:
                num = self._parse_number(token)
                if num is not None:
                    current_amount += num

        if current_entity and current_amount > 0:
            items.append((current_entity, current_amount))
            computed_sum += current_amount

        difference = abs(kuro_value - computed_sum)
        if difference == 0:
            status = "VERIFIED"
        elif difference <= Fraction(1, 4):
            status = "PARTIAL"
        elif len(items) == 0:
            status = "INCOMPLETE"
        else:
            status = "MISMATCH"

        # Diagnose mismatches
        diagnosis = None
        if status == "MISMATCH":
            diagnosis = self._diagnose_mismatch(tablet_id, words, kuro_value, computed_sum, items)

        # Build skeleton
        skeleton = self._build_skeleton(tablet_id, words)

        # KI-RO verification
        kiro_check = None
        if has_kiro:
            kiro_check = self._verify_kiro(words, kuro_value, computed_sum)

        return TabletVerification(
            tablet_id=tablet_id,
            site=site,
            has_kuro=True,
            has_kiro=has_kiro,
            kuro_status=status,
            kuro_value=float(kuro_value),
            computed_sum=float(computed_sum),
            difference=float(difference),
            item_count=len(items),
            diagnosis=diagnosis,
            skeleton=skeleton,
            kiro_verification=kiro_check,
        )

    def _diagnose_mismatch(
        self,
        tablet_id: str,
        words: List[str],
        kuro_value: Fraction,
        computed_sum: Fraction,
        items: List,
    ) -> MismatchDiagnosis:
        """Diagnose why a KU-RO mismatch occurs."""
        diff = float(abs(kuro_value - computed_sum))

        # Check for lacunae
        has_lacuna = self._has_lacuna_markers(words)
        if has_lacuna:
            return MismatchDiagnosis(
                tablet_id=tablet_id,
                kuro_value=float(kuro_value),
                computed_sum=float(computed_sum),
                difference=diff,
                diagnosis="lacuna",
                explanation="Tablet has damaged/missing sections; some entries may be unreadable",
                confidence="PROBABLE",
            )

        # Check for multiple commodities (might have sub-totals)
        commodities = self._count_commodities(words)
        if len(commodities) > 1:
            return MismatchDiagnosis(
                tablet_id=tablet_id,
                kuro_value=float(kuro_value),
                computed_sum=float(computed_sum),
                difference=diff,
                diagnosis="multi_commodity",
                explanation=f"Multiple commodities ({', '.join(sorted(commodities))}); "
                f"KU-RO may total one commodity type only, or parser "
                f"conflates quantities across commodity boundaries",
                confidence="POSSIBLE",
            )

        # Check for multiple KU-RO (sub-totals)
        kuro_count = self._count_kuro_instances(words)
        if kuro_count > 1:
            return MismatchDiagnosis(
                tablet_id=tablet_id,
                kuro_value=float(kuro_value),
                computed_sum=float(computed_sum),
                difference=diff,
                diagnosis="multi_kuro",
                explanation=f"Multiple KU-RO instances ({kuro_count}); "
                f"may represent sub-totals for different sections",
                confidence="PROBABLE",
            )

        # Check if difference is a round number (suggests missing entries)
        if diff == int(diff) and diff > 0:
            missing_entries = int(diff)
            return MismatchDiagnosis(
                tablet_id=tablet_id,
                kuro_value=float(kuro_value),
                computed_sum=float(computed_sum),
                difference=diff,
                diagnosis="missing_entries",
                explanation=f"Difference is round ({int(diff)}); likely {missing_entries} "
                f"unit(s) in entries not captured by parser (e.g., entries without "
                f"named recipients, or on damaged/missing lines)",
                confidence="POSSIBLE",
            )

        # Check if difference suggests fraction parsing issue
        frac_diff = Fraction(kuro_value - computed_sum)
        if frac_diff.denominator > 1:
            return MismatchDiagnosis(
                tablet_id=tablet_id,
                kuro_value=float(kuro_value),
                computed_sum=float(computed_sum),
                difference=diff,
                diagnosis="fraction_parsing",
                explanation=f"Fractional difference ({float(frac_diff):.4f}); "
                f"may indicate unparsed fraction signs",
                confidence="POSSIBLE",
            )

        return MismatchDiagnosis(
            tablet_id=tablet_id,
            kuro_value=float(kuro_value),
            computed_sum=float(computed_sum),
            difference=diff,
            diagnosis="unknown",
            explanation="Mismatch cause not automatically diagnosed; "
            "requires manual tablet inspection",
            confidence="UNKNOWN",
        )

    def _build_skeleton(self, tablet_id: str, words: List[str]) -> List[StructuralPosition]:
        """
        Build a Rosetta skeleton: tag each word with its structural position.

        Positions: header, recipient, commodity, quantity, total, deficit, separator, unknown
        """
        skeleton = []
        state = "start"
        line_start = True
        current_commodity = None

        for i, token in enumerate(words):
            if token == "\n":
                line_start = True
                skeleton.append(StructuralPosition(word=token, position_idx=i, role="separator"))
                continue

            if token in {"𐄁", "—", ""}:
                skeleton.append(StructuralPosition(word=token, position_idx=i, role="separator"))
                continue

            # Number
            num = self._parse_number(token)
            if num is not None:
                skeleton.append(
                    StructuralPosition(
                        word=token,
                        position_idx=i,
                        role="quantity",
                        commodity_context=current_commodity,
                        quantity=float(num),
                        confidence="CERTAIN",
                    )
                )
                line_start = False
                continue

            # KU-RO
            if token == "KU-RO":
                skeleton.append(
                    StructuralPosition(
                        word=token,
                        position_idx=i,
                        role="total",
                        confidence="CERTAIN",
                        notes="Summation marker",
                    )
                )
                line_start = False
                continue

            # KI-RO
            if token == "KI-RO":
                skeleton.append(
                    StructuralPosition(
                        word=token,
                        position_idx=i,
                        role="deficit",
                        confidence="HIGH",
                        notes="Deficit/remainder marker",
                    )
                )
                line_start = False
                continue

            # Logogram
            if self._is_logogram(token):
                current_commodity = self._get_base_commodity(token)
                skeleton.append(
                    StructuralPosition(
                        word=token,
                        position_idx=i,
                        role="commodity",
                        commodity_context=current_commodity,
                        confidence="CERTAIN",
                    )
                )
                line_start = False
                continue

            # Syllabic word
            if self._is_word(token):
                # First word of tablet or after separator at position 0
                if i == 0 or (line_start and state == "start"):
                    role = "header"
                    state = "body"
                    confidence = "PROBABLE"
                elif line_start:
                    # Word at start of a line is likely a recipient/entity
                    role = "recipient"
                    confidence = "INFERRED"
                else:
                    role = "unknown"
                    confidence = "INFERRED"

                skeleton.append(
                    StructuralPosition(word=token, position_idx=i, role=role, confidence=confidence)
                )
                line_start = False

        return skeleton

    def _verify_kiro(self, words: List[str], kuro_value: Fraction, computed_sum: Fraction) -> Dict:
        """Test whether (sum - KI-RO_value) = KU-RO on tablets with both."""
        kiro_indices = [i for i, w in enumerate(words) if w == "KI-RO"]
        results = []

        for kiro_idx in kiro_indices:
            # Get KI-RO value
            kiro_value = Fraction(0)
            for j in range(kiro_idx + 1, min(kiro_idx + 4, len(words))):
                if words[j] == "\n":
                    break
                num = self._parse_number(words[j])
                if num is not None:
                    kiro_value += num

            if kiro_value > 0 and kuro_value > 0:
                # Test: sum - KI-RO = KU-RO?
                predicted_kuro = computed_sum - kiro_value
                matches = abs(predicted_kuro - kuro_value) == 0
                results.append(
                    {
                        "kiro_value": float(kiro_value),
                        "predicted_kuro": float(predicted_kuro),
                        "actual_kuro": float(kuro_value),
                        "matches": matches,
                        "interpretation": "deficit hypothesis confirmed"
                        if matches
                        else "deficit hypothesis not confirmed",
                    }
                )

        return (
            {
                "has_both": True,
                "tests": results,
                "summary": "CONFIRMED" if any(r["matches"] for r in results) else "NOT_CONFIRMED",
            }
            if results
            else {"has_both": True, "tests": [], "summary": "INCONCLUSIVE"}
        )

    def verify_all(self) -> List[TabletVerification]:
        """Verify all tablets."""
        results = []
        for tablet_id in self.inscriptions:
            result = self.verify_tablet(tablet_id)
            if result:
                results.append(result)
        return results

    def print_tablet_report(self, result: TabletVerification):
        """Print detailed report for a single tablet."""
        print(f"\n{'=' * 70}")
        print(f"ARITHMETIC VERIFICATION: {result.tablet_id}")
        print(f"{'=' * 70}")
        print(f"  Site: {result.site}")
        print(f"  KU-RO present: {result.has_kuro}")
        print(f"  KI-RO present: {result.has_kiro}")
        print(f"  Status: {result.kuro_status}")

        if result.kuro_value is not None:
            print(f"  KU-RO value: {result.kuro_value}")
            print(f"  Computed sum: {result.computed_sum}")
            print(f"  Difference: {result.difference}")
            print(f"  Items parsed: {result.item_count}")

        if result.diagnosis:
            d = result.diagnosis
            print("\n  --- Mismatch Diagnosis ---")
            print(f"  Diagnosis: {d.diagnosis}")
            print(f"  Explanation: {d.explanation}")
            print(f"  Confidence: {d.confidence}")

        if result.kiro_verification:
            kv = result.kiro_verification
            print("\n  --- KI-RO Verification ---")
            print(f"  Summary: {kv['summary']}")
            for t in kv.get("tests", []):
                print(
                    f"    KI-RO={t['kiro_value']}, predicted KU-RO={t['predicted_kuro']}, "
                    f"actual KU-RO={t['actual_kuro']}, matches={t['matches']}"
                )

        if result.skeleton:
            print("\n  --- Rosetta Skeleton ---")
            for sp in result.skeleton:
                if sp.role == "separator":
                    if sp.word == "\n":
                        print("    ---")
                    continue
                marker = {
                    "header": "H",
                    "recipient": "R",
                    "commodity": "C",
                    "quantity": "#",
                    "total": "T",
                    "deficit": "D",
                    "unknown": "?",
                }.get(sp.role, ".")
                qty = f" = {sp.quantity}" if sp.quantity is not None else ""
                comm = f" ({sp.commodity_context})" if sp.commodity_context else ""
                print(f"    [{marker}] {sp.word:25s} {sp.role:12s}{comm}{qty}")

    def print_summary(self, results: List[TabletVerification]):
        """Print summary of all verifications."""
        print(f"\n{'=' * 70}")
        print("ARITHMETIC VERIFICATION SUMMARY")
        print(f"{'=' * 70}")

        kuro_tablets = [r for r in results if r.has_kuro]
        kiro_tablets = [r for r in results if r.has_kiro]

        statuses = Counter(r.kuro_status for r in results)
        print(f"\n  Total tablets: {len(results)}")
        print(f"  With KU-RO: {len(kuro_tablets)}")
        print(f"  With KI-RO: {len(kiro_tablets)}")
        print(f"  With both: {sum(1 for r in results if r.has_kuro and r.has_kiro)}")
        print("\n  Status distribution:")
        for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
            print(f"    {status:12s}: {count:4d}")

        # Diagnosis distribution
        diagnosed = [r for r in results if r.diagnosis]
        if diagnosed:
            diag_counts = Counter(r.diagnosis.diagnosis for r in diagnosed)
            print(f"\n  Mismatch diagnoses ({len(diagnosed)} total):")
            for diag, count in sorted(diag_counts.items(), key=lambda x: -x[1]):
                print(f"    {diag:20s}: {count}")

        # KI-RO deficit hypothesis
        kiro_results = [
            r for r in results if r.kiro_verification and r.kiro_verification.get("tests")
        ]
        if kiro_results:
            confirmed = sum(
                1 for r in kiro_results if r.kiro_verification["summary"] == "CONFIRMED"
            )
            print(f"\n  KI-RO deficit hypothesis: {confirmed}/{len(kiro_results)} confirmed")

    def save_results(self, results: List[TabletVerification], output_path: str):
        """Save results to JSON."""
        output = {
            "metadata": {
                "tool": "arithmetic_verifier.py",
                "tablets_analyzed": len(results),
                "with_kuro": sum(1 for r in results if r.has_kuro),
                "verified": sum(1 for r in results if r.kuro_status == "VERIFIED"),
                "mismatched": sum(1 for r in results if r.kuro_status == "MISMATCH"),
            },
            "verifications": [
                {
                    "tablet_id": r.tablet_id,
                    "site": r.site,
                    "has_kuro": r.has_kuro,
                    "has_kiro": r.has_kiro,
                    "kuro_status": r.kuro_status,
                    "kuro_value": r.kuro_value,
                    "computed_sum": r.computed_sum,
                    "difference": r.difference,
                    "item_count": r.item_count,
                    "diagnosis": asdict(r.diagnosis) if r.diagnosis else None,
                    "skeleton": [asdict(sp) for sp in r.skeleton],
                    "kiro_verification": r.kiro_verification,
                }
                for r in results
            ],
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Arithmetic Verifier - diagnose mismatches and build Rosetta skeletons"
    )
    parser.add_argument("--tablet", type=str, help="Verify a single tablet")
    parser.add_argument("--all", action="store_true", help="Verify all tablets")
    parser.add_argument("--diagnose", action="store_true", help="Show mismatch diagnoses only")
    parser.add_argument("--skeleton", type=str, help="Show Rosetta skeleton for a tablet")
    parser.add_argument("--output", type=str, help="Save results to JSON file")

    args = parser.parse_args()

    if not any([args.tablet, args.all, args.diagnose, args.skeleton]):
        args.all = True

    verifier = ArithmeticVerifier()
    if not verifier.load_corpus():
        sys.exit(1)

    if args.tablet:
        result = verifier.verify_tablet(args.tablet)
        if result:
            verifier.print_tablet_report(result)
        else:
            print(f"Tablet {args.tablet} not found")
            sys.exit(1)
    elif args.skeleton:
        result = verifier.verify_tablet(args.skeleton)
        if result:
            verifier.print_tablet_report(result)
        else:
            print(f"Tablet {args.skeleton} not found")
            sys.exit(1)
    elif args.diagnose:
        results = verifier.verify_all()
        mismatches = [r for r in results if r.kuro_status == "MISMATCH"]
        for r in mismatches:
            verifier.print_tablet_report(r)
        print(f"\n{len(mismatches)} mismatches diagnosed")
    else:
        results = verifier.verify_all()
        verifier.print_summary(results)

        if args.output:
            verifier.save_results(results, args.output)


if __name__ == "__main__":
    main()
