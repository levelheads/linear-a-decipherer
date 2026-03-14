#!/usr/bin/env python3
"""
Sign Value Extractor for Linear A

Arithmetic-driven sign value discovery. For each VERIFIED KU-RO tablet:
1. Extract the arithmetic skeleton (entries with quantities, totals)
2. For each entry with unknown word/sign, compute numerical constraints
3. Cross-reference: same unknown sign in multiple arithmetic contexts
   -> intersection of constraints
4. Connect to structural grid categories from ventris_grid.json

Analyses:
- Quantity ratio analysis: If sign X always appears with ~10% of CYP quantities,
  X may be tin (bronze = 90% Cu + 10% Sn)
- Position analysis: Signs in total position vs entry position vs qualifier position
- Cross-tablet constraints: Same sign on multiple tablets must have consistent
  interpretation

Usage:
    python3 tools/sign_value_extractor.py --all
    python3 tools/sign_value_extractor.py --tablet HT85a
    python3 tools/sign_value_extractor.py --sign '*304'
    python3 tools/sign_value_extractor.py --ratios
    python3 tools/sign_value_extractor.py --output data/sign_value_constraints.json

Attribution:
    Part of Linear A Decipherment Project
    Builds on arithmetic_verifier.py skeleton analysis
"""

import json
import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from fractions import Fraction


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
ARITHMETIC_FILE = DATA_DIR / "arithmetic_verification.json"
VENTRIS_GRID_FILE = DATA_DIR / "ventris_grid.json"
HYPOTHESIS_FILE = DATA_DIR / "hypothesis_results.json"

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

# Fraction mappings (from arithmetic_verifier.py)
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
    "≈ ¹⁄₆": Fraction(1, 6),
}

FRACTION_TOKENS = set(FRACTION_MAP.keys())

# Known function words (not unknown signs)
KNOWN_FUNCTION_WORDS = {
    "KU-RO",
    "KI-RO",
    "TE",
    "SA-RA₂",
    "A-DU",
    "DA-RE",
}

# Status levels to include in analysis
ARITHMETIC_STATUSES = {"VERIFIED", "CONSTRAINED"}


@dataclass
class ArithmeticEntry:
    """A single entry in a tablet's arithmetic structure."""

    word: str
    quantity: float
    commodity_context: Optional[str]
    position_role: str  # 'recipient', 'header', 'unknown', 'commodity', etc.
    line_index: int
    has_unknown_sign: bool = False
    unknown_signs: List[str] = field(default_factory=list)


@dataclass
class ArithmeticSkeleton:
    """Complete arithmetic structure of a tablet."""

    tablet_id: str
    site: str
    kuro_status: str
    kuro_value: float
    computed_sum: float
    entries: List[ArithmeticEntry] = field(default_factory=list)
    commodities: List[str] = field(default_factory=list)
    header_word: Optional[str] = None
    unknown_signs_present: List[str] = field(default_factory=list)


@dataclass
class SignConstraint:
    """Numerical constraint for an unknown sign from one tablet."""

    tablet_id: str
    sign: str
    quantity: Optional[float]
    ratio_to_total: Optional[float]
    commodity_context: Optional[str]
    position_role: str
    co_occurring_signs: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class SignProfile:
    """Cross-tablet profile for an unknown sign."""

    sign: str
    total_occurrences: int
    arithmetic_occurrences: int
    tablets: List[str] = field(default_factory=list)
    constraints: List[SignConstraint] = field(default_factory=list)
    quantity_range: Optional[Tuple[float, float]] = None
    ratio_range: Optional[Tuple[float, float]] = None
    consistent_commodity: Optional[str] = None
    position_distribution: Dict[str, int] = field(default_factory=dict)
    grid_roles: List[str] = field(default_factory=list)
    hypothesis_support: Optional[str] = None
    interpretation_candidates: List[str] = field(default_factory=list)
    confidence: str = "SPECULATIVE"


@dataclass
class RatioAnalysis:
    """Quantity ratio analysis between signs/commodities."""

    sign_a: str
    sign_b: str
    tablets: List[str] = field(default_factory=list)
    ratios: List[float] = field(default_factory=list)
    mean_ratio: Optional[float] = None
    std_ratio: Optional[float] = None
    interpretation: str = ""
    confidence: str = "SPECULATIVE"


class SignValueExtractor:
    """Arithmetic-driven sign value discovery for Linear A."""

    def __init__(self):
        self.corpus = {}
        self.inscriptions = {}
        self.arithmetic_data = {}
        self.ventris_grid = {}
        self.hypothesis_results = {}
        # Derived
        self.verified_tablets: Dict[str, Dict] = {}
        self.sign_profiles: Dict[str, SignProfile] = {}
        self.skeletons: Dict[str, ArithmeticSkeleton] = {}

    def load_data(self) -> bool:
        """Load all required data files."""
        # corpus.json — required
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)
            self.inscriptions = self.corpus.get("inscriptions", {})
            print(f"Loaded {len(self.inscriptions)} inscriptions")
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

        # arithmetic_verification.json — required
        try:
            with open(ARITHMETIC_FILE, "r", encoding="utf-8") as f:
                self.arithmetic_data = json.load(f)
            verifications = self.arithmetic_data.get("verifications", [])
            for v in verifications:
                if v.get("kuro_status") in ARITHMETIC_STATUSES:
                    self.verified_tablets[v["tablet_id"]] = v
            print(
                f"Loaded {len(verifications)} verifications, "
                f"{len(self.verified_tablets)} VERIFIED/CONSTRAINED"
            )
        except Exception as e:
            print(f"Error loading arithmetic verification: {e}")
            return False

        # ventris_grid.json — optional
        try:
            with open(VENTRIS_GRID_FILE, "r", encoding="utf-8") as f:
                self.ventris_grid = json.load(f)
            print(f"Loaded ventris grid ({len(self.ventris_grid.get('grid', {}))} paradigms)")
        except FileNotFoundError:
            print("Warning: ventris_grid.json not found (optional)")
        except Exception as e:
            print(f"Warning: Error loading ventris grid: {e}")

        # hypothesis_results.json — optional
        try:
            with open(HYPOTHESIS_FILE, "r", encoding="utf-8") as f:
                self.hypothesis_results = json.load(f)
            print(
                f"Loaded hypothesis results "
                f"({len(self.hypothesis_results.get('word_analyses', {}))} words)"
            )
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Warning: Error loading hypothesis results: {e}")

        return True

    # ── Token classification ───────────────────────────────────────────

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
            whole = int(match.group(1))
            num = int(match.group(2))
            denom = int(match.group(3))
            return Fraction(whole * denom + num, denom)
        match = re.match(r"^(\d+)/(\d+)$", token)
        if match:
            return Fraction(int(match.group(1)), int(match.group(2)))
        return None

    def _is_logogram(self, token: str) -> bool:
        """Check if token is a commodity logogram."""
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
        """Check if token is a syllabic word (not number, logogram, separator)."""
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

    def _contains_unknown_sign(self, token: str) -> bool:
        """Check if a token contains an undeciphered sign number (e.g., *304, *118)."""
        return bool(re.search(r"\*\d{2,3}", token))

    def _extract_unknown_signs(self, token: str) -> List[str]:
        """Extract all unknown sign numbers from a token."""
        return re.findall(r"\*\d{2,3}[a-z]?", token)

    def _extract_site(self, tablet_id: str) -> str:
        """Extract site code from tablet ID."""
        match = re.match(r"^([A-Z]+)", tablet_id)
        return match.group(1) if match else "UNKNOWN"

    # ── Skeleton building ──────────────────────────────────────────────

    def _build_arithmetic_skeleton(self, tablet_id: str) -> Optional[ArithmeticSkeleton]:
        """Build arithmetic skeleton for a single tablet from corpus data."""
        verification = self.verified_tablets.get(tablet_id)
        if not verification:
            return None

        tablet_data = self.inscriptions.get(tablet_id)
        if not tablet_data:
            return None

        words = tablet_data.get("transliteratedWords", [])
        if not words:
            return None

        site = self._extract_site(tablet_id)
        kuro_status = verification.get("kuro_status", "UNKNOWN")
        kuro_value = verification.get("kuro_value", 0.0) or 0.0
        computed_sum = verification.get("computed_sum", 0.0) or 0.0

        # Find KU-RO position(s)
        kuro_indices = [i for i, w in enumerate(words) if w == "KU-RO"]
        if not kuro_indices:
            return None
        kuro_idx = kuro_indices[-1]

        # Parse entries before KU-RO
        entries = []
        commodities_found = set()
        header_word = None
        all_unknown_signs = []

        current_entity = None
        current_amount = Fraction(0)
        current_commodity = None
        current_role = "unknown"
        current_unknown_signs = []
        line_idx = 0
        is_first_word = True

        for i in range(kuro_idx):
            token = words[i]

            if token == "\n":
                # End of line — flush current entry
                if current_entity is not None and current_amount > 0:
                    has_unknown = len(current_unknown_signs) > 0
                    entries.append(
                        ArithmeticEntry(
                            word=current_entity,
                            quantity=float(current_amount),
                            commodity_context=current_commodity,
                            position_role=current_role,
                            line_index=line_idx,
                            has_unknown_sign=has_unknown,
                            unknown_signs=list(current_unknown_signs),
                        )
                    )
                    all_unknown_signs.extend(current_unknown_signs)
                current_entity = None
                current_amount = Fraction(0)
                current_commodity = None
                current_role = "unknown"
                current_unknown_signs = []
                line_idx += 1
                continue

            if token in {"𐄁", "—", "", " ", ","}:
                continue

            # Number
            num = self._parse_number(token)
            if num is not None:
                current_amount += num
                continue

            # Logogram
            if self._is_logogram(token):
                base = self._get_base_commodity(token)
                commodities_found.add(base)
                current_commodity = base
                # If no entity yet, logogram IS the entity
                if current_entity is None:
                    current_entity = token
                    current_role = "commodity"
                continue

            # Word
            if self._is_word(token):
                # Check for unknown signs in the token
                if self._contains_unknown_sign(token):
                    signs = self._extract_unknown_signs(token)
                    current_unknown_signs.extend(signs)

                if is_first_word and current_entity is None:
                    header_word = token
                    current_entity = token
                    current_role = "header"
                    is_first_word = False
                elif current_entity is None:
                    current_entity = token
                    current_role = "recipient"
                else:
                    # Additional word on same line — check if it has unknown signs
                    if self._contains_unknown_sign(token):
                        current_unknown_signs.extend(
                            s
                            for s in self._extract_unknown_signs(token)
                            if s not in current_unknown_signs
                        )
                is_first_word = False

        # Flush final entry
        if current_entity is not None and current_amount > 0:
            has_unknown = len(current_unknown_signs) > 0
            entries.append(
                ArithmeticEntry(
                    word=current_entity,
                    quantity=float(current_amount),
                    commodity_context=current_commodity,
                    position_role=current_role,
                    line_index=line_idx,
                    has_unknown_sign=has_unknown,
                    unknown_signs=list(current_unknown_signs),
                )
            )
            all_unknown_signs.extend(current_unknown_signs)

        # Also scan entire tablet for unknown signs (including after KU-RO)
        all_signs_on_tablet = []
        for token in words:
            if self._contains_unknown_sign(token):
                all_signs_on_tablet.extend(self._extract_unknown_signs(token))

        skeleton = ArithmeticSkeleton(
            tablet_id=tablet_id,
            site=site,
            kuro_status=kuro_status,
            kuro_value=kuro_value,
            computed_sum=computed_sum,
            entries=entries,
            commodities=sorted(commodities_found),
            header_word=header_word,
            unknown_signs_present=sorted(set(all_signs_on_tablet)),
        )

        return skeleton

    # ── Sign constraint extraction ─────────────────────────────────────

    def _extract_sign_constraints(self, skeleton: ArithmeticSkeleton) -> List[SignConstraint]:
        """Extract numerical constraints for unknown signs from a skeleton."""
        constraints = []

        for entry in skeleton.entries:
            if not entry.has_unknown_sign:
                continue

            for sign in entry.unknown_signs:
                # Compute ratio to total
                ratio = None
                if skeleton.kuro_value > 0:
                    ratio = entry.quantity / skeleton.kuro_value

                # Find co-occurring signs on same tablet
                co_occurring = [s for s in skeleton.unknown_signs_present if s != sign]

                notes_parts = []
                if entry.position_role == "header":
                    notes_parts.append("appears in header position")
                if entry.commodity_context:
                    notes_parts.append(f"commodity context: {entry.commodity_context}")

                constraint = SignConstraint(
                    tablet_id=skeleton.tablet_id,
                    sign=sign,
                    quantity=entry.quantity,
                    ratio_to_total=round(ratio, 4) if ratio is not None else None,
                    commodity_context=entry.commodity_context,
                    position_role=entry.position_role,
                    co_occurring_signs=co_occurring,
                    notes="; ".join(notes_parts) if notes_parts else "",
                )
                constraints.append(constraint)

        # Also check for signs that appear on the tablet but NOT in quantity entries
        # (qualifiers, markers, etc.)
        signs_with_quantities = set()
        for entry in skeleton.entries:
            signs_with_quantities.update(entry.unknown_signs)

        for sign in skeleton.unknown_signs_present:
            if sign not in signs_with_quantities:
                co_occurring = [s for s in skeleton.unknown_signs_present if s != sign]
                constraint = SignConstraint(
                    tablet_id=skeleton.tablet_id,
                    sign=sign,
                    quantity=None,
                    ratio_to_total=None,
                    commodity_context=None,
                    position_role="non-quantity",
                    co_occurring_signs=co_occurring,
                    notes="appears on tablet but not in quantity-bearing entry",
                )
                constraints.append(constraint)

        return constraints

    # ── Cross-tablet sign profiling ────────────────────────────────────

    def _build_sign_profiles(self) -> Dict[str, SignProfile]:
        """Build cross-tablet profiles for all unknown signs."""
        # Gather all constraints across tablets
        sign_constraints: Dict[str, List[SignConstraint]] = defaultdict(list)

        for tablet_id, skeleton in self.skeletons.items():
            constraints = self._extract_sign_constraints(skeleton)
            for c in constraints:
                sign_constraints[c.sign].append(c)

        # Count total corpus occurrences of each sign
        sign_corpus_count: Dict[str, int] = Counter()
        sign_corpus_tablets: Dict[str, Set[str]] = defaultdict(set)
        for tablet_id, tdata in self.inscriptions.items():
            words = tdata.get("transliteratedWords", [])
            for w in words:
                if self._contains_unknown_sign(w):
                    for sign in self._extract_unknown_signs(w):
                        sign_corpus_count[sign] += 1
                        sign_corpus_tablets[sign].add(tablet_id)

        # Build profiles
        profiles = {}
        all_signs = set(sign_constraints.keys()) | set(sign_corpus_count.keys())

        for sign in sorted(all_signs):
            constraints = sign_constraints.get(sign, [])

            # Quantity range
            quantities = [c.quantity for c in constraints if c.quantity is not None]
            qty_range = (min(quantities), max(quantities)) if quantities else None

            # Ratio range
            ratios = [c.ratio_to_total for c in constraints if c.ratio_to_total is not None]
            ratio_range = (min(ratios), max(ratios)) if ratios else None

            # Consistent commodity
            commodity_counts = Counter(
                c.commodity_context for c in constraints if c.commodity_context is not None
            )
            consistent_commodity = None
            if commodity_counts:
                top_comm, top_count = commodity_counts.most_common(1)[0]
                if top_count == len([c for c in constraints if c.commodity_context]):
                    consistent_commodity = top_comm

            # Position distribution
            pos_dist = Counter(c.position_role for c in constraints)

            # Grid roles from ventris_grid
            grid_roles = self._lookup_grid_roles(sign)

            # Hypothesis support
            hyp_support = self._lookup_hypothesis(sign)

            # Interpretation candidates
            candidates = self._generate_interpretation_candidates(
                sign,
                constraints,
                qty_range,
                ratio_range,
                consistent_commodity,
                pos_dist,
                grid_roles,
            )

            # Confidence assessment
            confidence = self._assess_confidence(constraints, candidates)

            profile = SignProfile(
                sign=sign,
                total_occurrences=sign_corpus_count.get(sign, 0),
                arithmetic_occurrences=len(constraints),
                tablets=sorted(sign_corpus_tablets.get(sign, set())),
                constraints=constraints,
                quantity_range=qty_range,
                ratio_range=ratio_range,
                consistent_commodity=consistent_commodity,
                position_distribution=dict(pos_dist),
                grid_roles=grid_roles,
                hypothesis_support=hyp_support,
                interpretation_candidates=candidates,
                confidence=confidence,
            )
            profiles[sign] = profile

        return profiles

    def _lookup_grid_roles(self, sign: str) -> List[str]:
        """Look up structural grid roles for a sign from ventris_grid.json."""
        roles = []
        if not self.ventris_grid:
            return roles

        word_profiles = self.ventris_grid.get("word_profiles", {})
        top_profiles = word_profiles.get("top_200", {})

        # Check if sign appears in any word profile
        for word, profile in top_profiles.items():
            if sign in word:
                gram_roles = profile.get("grammatical_roles", [])
                roles.extend(gram_roles)

        # Check grid paradigms
        grid = self.ventris_grid.get("grid", {})
        for paradigm_id, paradigm_data in grid.items():
            if not isinstance(paradigm_data, dict):
                continue
            for role_name, role_data in paradigm_data.items():
                if not isinstance(role_data, dict):
                    continue
                role_words = role_data.get("words", [])
                for w in role_words:
                    if sign in w:
                        roles.append(f"{paradigm_id}:{role_name}")

        return sorted(set(roles))

    def _lookup_hypothesis(self, sign: str) -> Optional[str]:
        """Look up hypothesis support for a sign."""
        if not self.hypothesis_results:
            return None
        analyses = self.hypothesis_results.get("word_analyses", {})

        # Try the sign itself and common word forms containing it
        for word, data in analyses.items():
            if sign in word:
                synthesis = data.get("synthesis", {})
                best = synthesis.get("best_hypothesis", "")
                conf = synthesis.get("max_confidence", "")
                if best and conf and conf not in ("UNKNOWN", "NONE", ""):
                    return f"{word}: {best} ({conf})"

        return None

    def _generate_interpretation_candidates(
        self,
        sign: str,
        constraints: List[SignConstraint],
        qty_range: Optional[Tuple[float, float]],
        ratio_range: Optional[Tuple[float, float]],
        consistent_commodity: Optional[str],
        pos_dist: Dict[str, int],
        grid_roles: List[str],
    ) -> List[str]:
        """Generate possible interpretation candidates based on constraints."""
        candidates = []

        if not constraints:
            return candidates

        # Ratio-based candidates
        if ratio_range:
            lo, hi = ratio_range
            # Check for ~10% ratio (tin in bronze)
            if 0.05 <= lo <= 0.15 and 0.05 <= hi <= 0.15:
                if consistent_commodity == "CYP":
                    candidates.append(
                        f"Possible tin indicator (ratio {lo:.1%}-{hi:.1%} of CYP, "
                        f"consistent with bronze = 90% Cu + 10% Sn)"
                    )

            # Check for high ratio (>50%) — might be primary commodity
            if lo > 0.4:
                candidates.append(
                    f"High ratio to total ({lo:.1%}-{hi:.1%}): "
                    f"likely primary commodity or large allocation"
                )

            # Check for very low ratio (<5%) — might be additive/tax
            if hi < 0.05 and hi > 0:
                candidates.append(
                    f"Low ratio to total ({lo:.1%}-{hi:.1%}): possible tax, fee, or additive"
                )

        # Position-based candidates
        if pos_dist.get("header", 0) > 0:
            total_positioned = sum(pos_dist.values())
            header_pct = pos_dist["header"] / total_positioned
            if header_pct > 0.5:
                candidates.append(
                    "Frequently in header position: likely a transaction type or place name"
                )

        if pos_dist.get("non-quantity", 0) > 0 and pos_dist.get("recipient", 0) == 0:
            candidates.append(
                "Appears without quantities: possible qualifier,"
                " determinative, or administrative marker"
            )

        # Commodity context candidates
        if consistent_commodity:
            candidates.append(
                f"Consistently associated with {consistent_commodity}: "
                f"possible sub-type, grade, or related term"
            )

        # Cross-tablet consistency
        arith_tablets = set(c.tablet_id for c in constraints)
        if len(arith_tablets) >= 2:
            quantities = [c.quantity for c in constraints if c.quantity is not None]
            if quantities and len(set(quantities)) == 1:
                candidates.append(
                    f"Same quantity ({quantities[0]}) across {len(arith_tablets)} tablets: "
                    f"possible fixed allocation or standard unit"
                )

        # Grid role candidates
        if grid_roles:
            candidates.append(f"Structural grid roles: {', '.join(grid_roles)}")

        return candidates

    def _assess_confidence(
        self,
        constraints: List[SignConstraint],
        candidates: List[str],
    ) -> str:
        """Assess confidence level of sign value extraction."""
        if not constraints:
            return "NO_DATA"

        arith_count = len([c for c in constraints if c.quantity is not None])
        tablet_count = len(set(c.tablet_id for c in constraints))

        if arith_count >= 3 and tablet_count >= 2 and candidates:
            return "PROBABLE"
        if arith_count >= 2 and candidates:
            return "POSSIBLE"
        if arith_count >= 1:
            return "SPECULATIVE"
        return "INSUFFICIENT"

    # ── Ratio analysis ────────────────────────────────────────────────

    def compute_ratio_analysis(self) -> List[RatioAnalysis]:
        """Compute quantity ratios between unknown signs and commodities across tablets."""
        ratio_analyses = []

        # Collect (sign, commodity) -> [(tablet, sign_qty, commodity_total)] tuples
        sign_commodity_pairs: Dict[Tuple[str, str], List[Tuple[str, float, float]]] = defaultdict(
            list
        )

        for tablet_id, skeleton in self.skeletons.items():
            # Get commodity totals from the skeleton
            commodity_totals: Dict[str, float] = defaultdict(float)
            for entry in skeleton.entries:
                if entry.commodity_context and not entry.has_unknown_sign:
                    commodity_totals[entry.commodity_context] += entry.quantity

            # For entries with unknown signs, compute ratios to commodity totals
            for entry in skeleton.entries:
                if entry.has_unknown_sign and entry.quantity:
                    for sign in entry.unknown_signs:
                        # Ratio to overall KU-RO total
                        if skeleton.kuro_value > 0:
                            key = (sign, "KU-RO_TOTAL")
                            sign_commodity_pairs[key].append(
                                (tablet_id, entry.quantity, skeleton.kuro_value)
                            )
                        # Ratio to specific commodity totals on same tablet
                        for comm, comm_total in commodity_totals.items():
                            if comm_total > 0:
                                key = (sign, comm)
                                sign_commodity_pairs[key].append(
                                    (tablet_id, entry.quantity, comm_total)
                                )

        # Build ratio analyses
        for (sign, commodity), data_points in sign_commodity_pairs.items():
            if len(data_points) < 1:
                continue

            tablets = [d[0] for d in data_points]
            ratios = [d[1] / d[2] for d in data_points if d[2] > 0]

            if not ratios:
                continue

            mean_ratio = sum(ratios) / len(ratios)
            if len(ratios) > 1:
                variance = sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios)
                std_ratio = variance**0.5
            else:
                std_ratio = None

            # Generate interpretation
            interpretation = self._interpret_ratio(
                sign, commodity, mean_ratio, std_ratio, len(ratios)
            )

            confidence = "SPECULATIVE"
            if len(ratios) >= 3 and std_ratio is not None and std_ratio < 0.1:
                confidence = "PROBABLE"
            elif len(ratios) >= 2 and std_ratio is not None and std_ratio < 0.15:
                confidence = "POSSIBLE"

            analysis = RatioAnalysis(
                sign_a=sign,
                sign_b=commodity,
                tablets=tablets,
                ratios=[round(r, 4) for r in ratios],
                mean_ratio=round(mean_ratio, 4),
                std_ratio=round(std_ratio, 4) if std_ratio is not None else None,
                interpretation=interpretation,
                confidence=confidence,
            )
            ratio_analyses.append(analysis)

        # Sort by confidence then number of data points
        confidence_order = {"PROBABLE": 0, "POSSIBLE": 1, "SPECULATIVE": 2}
        ratio_analyses.sort(
            key=lambda a: (
                confidence_order.get(a.confidence, 3),
                -len(a.ratios),
            )
        )

        return ratio_analyses

    def _interpret_ratio(
        self,
        sign: str,
        commodity: str,
        mean_ratio: float,
        std_ratio: Optional[float],
        n_points: int,
    ) -> str:
        """Interpret a sign-commodity ratio."""
        parts = []

        if commodity == "KU-RO_TOTAL":
            parts.append(f"{sign} averages {mean_ratio:.1%} of tablet total")
        else:
            parts.append(f"{sign} averages {mean_ratio:.1%} of {commodity} quantities")

        # Bronze ratio check
        if commodity == "CYP" and 0.08 <= mean_ratio <= 0.12:
            parts.append("NOTABLE: ratio consistent with tin proportion in bronze (10%)")

        # High/low ratio signals
        if mean_ratio > 0.5:
            parts.append("high ratio suggests primary allocation or major commodity")
        elif mean_ratio < 0.05 and mean_ratio > 0:
            parts.append("low ratio suggests tax, tithe, or secondary additive")

        if std_ratio is not None:
            if std_ratio < 0.05:
                parts.append("very consistent across tablets")
            elif std_ratio < 0.15:
                parts.append("moderately consistent")
            else:
                parts.append("high variance — ratio may not be meaningful")

        if n_points == 1:
            parts.append("(single data point — needs more evidence)")

        return "; ".join(parts)

    # ── Main analysis pipeline ─────────────────────────────────────────

    def analyze_all(self):
        """Run full analysis: build skeletons, extract constraints, build profiles."""
        # Build skeletons for all VERIFIED/CONSTRAINED tablets
        for tablet_id in self.verified_tablets:
            skeleton = self._build_arithmetic_skeleton(tablet_id)
            if skeleton:
                self.skeletons[tablet_id] = skeleton

        # Build sign profiles
        self.sign_profiles = self._build_sign_profiles()

    def analyze_tablet(self, tablet_id: str) -> Optional[ArithmeticSkeleton]:
        """Analyze a single tablet."""
        if tablet_id not in self.verified_tablets:
            # Try to build skeleton anyway from corpus
            tablet_data = self.inscriptions.get(tablet_id)
            if not tablet_data:
                return None
            # Create a minimal verification entry
            words = tablet_data.get("transliteratedWords", [])
            has_kuro = "KU-RO" in words
            if not has_kuro:
                print(f"  {tablet_id}: No KU-RO found, cannot build arithmetic skeleton")
                return None
            self.verified_tablets[tablet_id] = {
                "tablet_id": tablet_id,
                "kuro_status": "UNVERIFIED",
                "kuro_value": 0.0,
                "computed_sum": 0.0,
            }

        skeleton = self._build_arithmetic_skeleton(tablet_id)
        if skeleton:
            self.skeletons[tablet_id] = skeleton
            # Build profiles for signs on this tablet
            self.sign_profiles = self._build_sign_profiles()
        return skeleton

    # ── Display ────────────────────────────────────────────────────────

    def print_tablet_report(self, skeleton: ArithmeticSkeleton):
        """Print detailed report for a single tablet's arithmetic skeleton."""
        print(f"\n{'=' * 70}")
        print(f"ARITHMETIC SKELETON: {skeleton.tablet_id}")
        print(f"{'=' * 70}")
        print(f"  Site: {skeleton.site}")
        print(f"  Status: {skeleton.kuro_status}")
        print(f"  KU-RO value: {skeleton.kuro_value}")
        print(f"  Computed sum: {skeleton.computed_sum}")
        commod_str = ", ".join(skeleton.commodities) if skeleton.commodities else "none explicit"
        print(f"  Commodities: {commod_str}")
        print(f"  Header: {skeleton.header_word or '(none)'}")
        unk_str = (
            ", ".join(skeleton.unknown_signs_present) if skeleton.unknown_signs_present else "none"
        )
        print(f"  Unknown signs: {unk_str}")

        print(f"\n  --- Entries ({len(skeleton.entries)}) ---")
        for entry in skeleton.entries:
            sign_flag = " [*]" if entry.has_unknown_sign else ""
            comm = f" ({entry.commodity_context})" if entry.commodity_context else ""
            ratio = ""
            if skeleton.kuro_value > 0:
                r = entry.quantity / skeleton.kuro_value
                ratio = f" = {r:.1%} of total"
            print(
                f"    L{entry.line_index}: {entry.word:25s} "
                f"{entry.quantity:8.2f}{comm}{ratio} [{entry.position_role}]{sign_flag}"
            )
            if entry.unknown_signs:
                print(f"         unknown signs: {', '.join(entry.unknown_signs)}")

        # Print sign constraints for this tablet
        constraints = self._extract_sign_constraints(skeleton)
        if constraints:
            print(f"\n  --- Sign Constraints ({len(constraints)}) ---")
            for c in constraints:
                qty = f"{c.quantity:.2f}" if c.quantity is not None else "N/A"
                ratio = f"{c.ratio_to_total:.1%}" if c.ratio_to_total is not None else "N/A"
                print(
                    f"    {c.sign:12s} qty={qty:>8s}  ratio={ratio:>6s}  "
                    f"role={c.position_role}  {c.notes}"
                )

    def print_sign_report(self, sign: str):
        """Print detailed report for a single sign's cross-tablet profile."""
        profile = self.sign_profiles.get(sign)
        if not profile:
            print(f"Sign {sign} not found in any VERIFIED/CONSTRAINED arithmetic tablet")
            # Check corpus
            count = 0
            tablets = []
            for tid, tdata in self.inscriptions.items():
                words = tdata.get("transliteratedWords", [])
                for w in words:
                    if sign in w:
                        count += 1
                        tablets.append(tid)
                        break
            if count:
                print(f"  (found on {count} tablets in corpus: {', '.join(tablets[:10])})")
            return

        print(f"\n{'=' * 70}")
        print(f"SIGN VALUE PROFILE: {profile.sign}")
        print(f"{'=' * 70}")
        print(f"  Total corpus occurrences: {profile.total_occurrences}")
        print(f"  Arithmetic occurrences: {profile.arithmetic_occurrences}")
        print(
            f"  Tablets (all): {', '.join(profile.tablets[:15])}"
            f"{'...' if len(profile.tablets) > 15 else ''}"
        )
        print(f"  Confidence: {profile.confidence}")

        if profile.quantity_range:
            lo, hi = profile.quantity_range
            print(f"  Quantity range: {lo:.2f} - {hi:.2f}")
        if profile.ratio_range:
            lo, hi = profile.ratio_range
            print(f"  Ratio-to-total range: {lo:.1%} - {hi:.1%}")
        if profile.consistent_commodity:
            print(f"  Consistent commodity: {profile.consistent_commodity}")
        if profile.position_distribution:
            pos_str = ", ".join(
                f"{k}={v}" for k, v in sorted(profile.position_distribution.items())
            )
            print(f"  Position distribution: {pos_str}")
        if profile.grid_roles:
            print(f"  Grid roles: {', '.join(profile.grid_roles)}")
        if profile.hypothesis_support:
            print(f"  Hypothesis support: {profile.hypothesis_support}")

        if profile.constraints:
            print(f"\n  --- Per-tablet constraints ({len(profile.constraints)}) ---")
            for c in profile.constraints:
                qty = f"{c.quantity:.2f}" if c.quantity is not None else "N/A"
                ratio = f"{c.ratio_to_total:.1%}" if c.ratio_to_total is not None else "N/A"
                print(
                    f"    {c.tablet_id:12s} qty={qty:>8s}  ratio={ratio:>6s}  "
                    f"role={c.position_role}"
                )
                if c.co_occurring_signs:
                    print(f"                 co-occurring: {', '.join(c.co_occurring_signs)}")
                if c.notes:
                    print(f"                 {c.notes}")

        if profile.interpretation_candidates:
            print("\n  --- Interpretation candidates ---")
            for i, cand in enumerate(profile.interpretation_candidates, 1):
                print(f"    {i}. {cand}")

    def print_summary(self):
        """Print overall summary of all sign value extractions."""
        print(f"\n{'=' * 70}")
        print("SIGN VALUE EXTRACTION SUMMARY")
        print(f"{'=' * 70}")

        print(f"\n  Tablets analyzed: {len(self.skeletons)}")
        verified = sum(1 for s in self.skeletons.values() if s.kuro_status == "VERIFIED")
        constrained = sum(1 for s in self.skeletons.values() if s.kuro_status == "CONSTRAINED")
        print(f"    VERIFIED: {verified}")
        print(f"    CONSTRAINED: {constrained}")

        # Signs summary
        signs_with_arith = {
            sign: p for sign, p in self.sign_profiles.items() if p.arithmetic_occurrences > 0
        }
        all_signs = self.sign_profiles

        print(f"\n  Unknown signs in corpus: {len(all_signs)}")
        print(f"  Unknown signs in arithmetic contexts: {len(signs_with_arith)}")

        # Confidence distribution
        conf_dist = Counter(p.confidence for p in signs_with_arith.values())
        if conf_dist:
            print("\n  Confidence distribution (arithmetic signs):")
            for conf in ["PROBABLE", "POSSIBLE", "SPECULATIVE", "INSUFFICIENT", "NO_DATA"]:
                if conf in conf_dist:
                    print(f"    {conf:15s}: {conf_dist[conf]}")

        # Top constrained signs
        constrained_signs = sorted(
            signs_with_arith.values(),
            key=lambda p: (
                {"PROBABLE": 0, "POSSIBLE": 1, "SPECULATIVE": 2}.get(p.confidence, 3),
                -p.arithmetic_occurrences,
            ),
        )

        if constrained_signs:
            print("\n  --- Top constrained signs ---")
            print(
                f"  {'Sign':12s} {'Arith':>5s} {'Corpus':>6s} {'Qty Range':>12s} "
                f"{'Ratio Range':>14s} {'Conf':12s}"
            )
            print(f"  {'-' * 65}")
            for p in constrained_signs[:20]:
                qty = (
                    f"{p.quantity_range[0]:.1f}-{p.quantity_range[1]:.1f}"
                    if p.quantity_range
                    else "N/A"
                )
                ratio = f"{p.ratio_range[0]:.1%}-{p.ratio_range[1]:.1%}" if p.ratio_range else "N/A"
                print(
                    f"  {p.sign:12s} {p.arithmetic_occurrences:5d} {p.total_occurrences:6d} "
                    f"{qty:>12s} {ratio:>14s} {p.confidence:12s}"
                )

        # Per-tablet skeleton summaries
        print("\n  --- Tablet skeletons ---")
        for tid in sorted(self.skeletons.keys()):
            s = self.skeletons[tid]
            n_entries = len(s.entries)
            n_unknown = len(s.unknown_signs_present)
            comm = ", ".join(s.commodities) if s.commodities else "none"
            print(
                f"    {tid:12s} [{s.kuro_status:11s}] "
                f"KU-RO={s.kuro_value:>6.1f}  entries={n_entries:2d}  "
                f"unknown_signs={n_unknown}  commodities={comm}"
            )

    def print_ratio_analysis(self, ratio_analyses: List[RatioAnalysis]):
        """Print ratio analysis results."""
        print(f"\n{'=' * 70}")
        print("QUANTITY RATIO ANALYSIS")
        print(f"{'=' * 70}")

        if not ratio_analyses:
            print("\n  No ratio data available (no unknown signs with quantities found)")
            return

        print(f"\n  Total sign-commodity pairs analyzed: {len(ratio_analyses)}")

        notable = [a for a in ratio_analyses if a.confidence in ("PROBABLE", "POSSIBLE")]
        if notable:
            print(f"  Notable (PROBABLE/POSSIBLE): {len(notable)}")

        for a in ratio_analyses:
            print(f"\n  {a.sign_a} / {a.sign_b}:")
            print(f"    Tablets: {', '.join(a.tablets)}")
            print(f"    Ratios: {', '.join(f'{r:.1%}' for r in a.ratios)}")
            print(
                f"    Mean ratio: {a.mean_ratio:.1%}"
                f"{f'  (std: {a.std_ratio:.4f})' if a.std_ratio is not None else ''}"
            )
            print(f"    Confidence: {a.confidence}")
            print(f"    Interpretation: {a.interpretation}")

    # ── JSON output ────────────────────────────────────────────────────

    def save_results(self, output_path: str):
        """Save all results to JSON."""
        # Filter to signs with arithmetic data for the main output
        arith_profiles = {
            sign: p for sign, p in self.sign_profiles.items() if p.arithmetic_occurrences > 0
        }

        output = {
            "metadata": {
                "tool": "sign_value_extractor.py",
                "tablets_analyzed": len(self.skeletons),
                "verified_tablets": sum(
                    1 for s in self.skeletons.values() if s.kuro_status == "VERIFIED"
                ),
                "constrained_tablets": sum(
                    1 for s in self.skeletons.values() if s.kuro_status == "CONSTRAINED"
                ),
                "unknown_signs_in_corpus": len(self.sign_profiles),
                "unknown_signs_in_arithmetic": len(arith_profiles),
            },
            "skeletons": {
                tid: {
                    "tablet_id": s.tablet_id,
                    "site": s.site,
                    "kuro_status": s.kuro_status,
                    "kuro_value": s.kuro_value,
                    "computed_sum": s.computed_sum,
                    "commodities": s.commodities,
                    "header_word": s.header_word,
                    "unknown_signs_present": s.unknown_signs_present,
                    "entries": [
                        {
                            "word": e.word,
                            "quantity": e.quantity,
                            "commodity_context": e.commodity_context,
                            "position_role": e.position_role,
                            "line_index": e.line_index,
                            "has_unknown_sign": e.has_unknown_sign,
                            "unknown_signs": e.unknown_signs,
                        }
                        for e in s.entries
                    ],
                }
                for tid, s in sorted(self.skeletons.items())
            },
            "sign_profiles": {
                sign: {
                    "sign": p.sign,
                    "total_occurrences": p.total_occurrences,
                    "arithmetic_occurrences": p.arithmetic_occurrences,
                    "tablets": p.tablets,
                    "quantity_range": list(p.quantity_range) if p.quantity_range else None,
                    "ratio_range": list(p.ratio_range) if p.ratio_range else None,
                    "consistent_commodity": p.consistent_commodity,
                    "position_distribution": p.position_distribution,
                    "grid_roles": p.grid_roles,
                    "hypothesis_support": p.hypothesis_support,
                    "interpretation_candidates": p.interpretation_candidates,
                    "confidence": p.confidence,
                    "constraints": [
                        {
                            "tablet_id": c.tablet_id,
                            "quantity": c.quantity,
                            "ratio_to_total": c.ratio_to_total,
                            "commodity_context": c.commodity_context,
                            "position_role": c.position_role,
                            "co_occurring_signs": c.co_occurring_signs,
                            "notes": c.notes,
                        }
                        for c in p.constraints
                    ],
                }
                for sign, p in sorted(arith_profiles.items())
            },
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Sign Value Extractor - arithmetic-driven sign value discovery"
    )
    parser.add_argument("--tablet", type=str, help="Analyze a single tablet")
    parser.add_argument(
        "--all", action="store_true", help="Analyze all VERIFIED/CONSTRAINED tablets"
    )
    parser.add_argument("--sign", type=str, help="Show profile for a specific sign (e.g., '*304')")
    parser.add_argument("--ratios", action="store_true", help="Show quantity ratio analysis")
    parser.add_argument("--output", type=str, help="Save results to JSON file")

    args = parser.parse_args()

    if not any([args.tablet, args.all, args.sign, args.ratios]):
        args.all = True

    extractor = SignValueExtractor()
    if not extractor.load_data():
        sys.exit(1)

    if args.tablet:
        skeleton = extractor.analyze_tablet(args.tablet)
        if skeleton:
            extractor.print_tablet_report(skeleton)
            # Also show sign profiles for signs on this tablet
            for sign in skeleton.unknown_signs_present:
                extractor.print_sign_report(sign)
        else:
            print(f"Tablet {args.tablet} not found or has no KU-RO")
            sys.exit(1)

    elif args.sign:
        # Need to run full analysis first to build cross-tablet profiles
        extractor.analyze_all()
        extractor.print_sign_report(args.sign)

    elif args.ratios:
        extractor.analyze_all()
        ratio_analyses = extractor.compute_ratio_analysis()
        extractor.print_ratio_analysis(ratio_analyses)

    else:
        # --all
        extractor.analyze_all()
        extractor.print_summary()

        # Always include ratio analysis in --all mode
        ratio_analyses = extractor.compute_ratio_analysis()
        if ratio_analyses:
            extractor.print_ratio_analysis(ratio_analyses)

    if args.output:
        if not extractor.skeletons:
            extractor.analyze_all()
        extractor.save_results(args.output)


if __name__ == "__main__":
    main()
