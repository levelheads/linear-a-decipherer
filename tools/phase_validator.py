#!/usr/bin/env python3
"""
Phase Validator for Linear A Analysis

Detects contradictions between analysis phases and tracks morphological claims
with their evidence basis. This tool enforces First Principle #2 (Ventris Lesson):
"Abandon hypotheses when evidence contradicts them."

Key features:
1. Register morphological claims with evidence basis
2. Detect logical contradictions between phases
3. Compare sample sizes and statistical significance
4. Track confidence evolution across phases

Usage:
    python tools/phase_validator.py --check-all
    python tools/phase_validator.py --claim "-U = Semitic nominative" --evidence "Phase 1 analysis"
    python tools/phase_validator.py --compare phase1 phase2

Attribution:
    Part of Linear A Decipherment Project (OPERATION MINOS II)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict
from enum import Enum


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ANALYSIS_DIR = PROJECT_ROOT / "analysis" / "sessions"
CLAIMS_FILE = DATA_DIR / "morphological_claims.json"


class ClaimType(str, Enum):
    MORPHOLOGICAL = "morphological"  # Suffix/ending function
    LEXICAL = "lexical"              # Word meaning
    PHONOLOGICAL = "phonological"    # Sound patterns
    SYNTACTIC = "syntactic"          # Word order/structure
    SEMANTIC = "semantic"            # Meaning relationships


class ConfidenceLevel(str, Enum):
    CERTAIN = "CERTAIN"
    PROBABLE = "PROBABLE"
    POSSIBLE = "POSSIBLE"
    SPECULATIVE = "SPECULATIVE"
    REJECTED = "REJECTED"


@dataclass
class MorphologicalClaim:
    """A registered claim about Linear A morphology."""
    claim_id: str
    claim_type: ClaimType
    element: str                    # The morpheme/word being claimed about
    assertion: str                  # What is being claimed
    hypothesis: str                 # Which linguistic hypothesis (luwian/semitic/pregreek/protogreek)
    confidence: ConfidenceLevel
    evidence: List[Dict]            # Supporting evidence
    phase: str                      # Which analysis phase
    sample_size: int                # Number of examples
    contradicting_evidence: List[Dict]  # Counter-evidence
    timestamp: str
    superseded_by: Optional[str] = None  # If later claim replaces this


@dataclass
class Contradiction:
    """A detected contradiction between claims."""
    contradiction_id: str
    claim_a: str                    # First claim ID
    claim_b: str                    # Second claim ID
    element: str                    # The element in conflict
    description: str                # What the contradiction is
    severity: str                   # HIGH/MEDIUM/LOW
    resolution_guidance: str        # How to resolve
    detected_at: str


class PhaseValidator:
    """
    Validates consistency across analysis phases.

    Tracks morphological claims and detects contradictions following
    First Principle #2: "If evidence contradicts your hypothesis,
    abandon the hypothesis, not the evidence."
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.claims: Dict[str, MorphologicalClaim] = {}
        self.contradictions: List[Contradiction] = []
        self.claim_index: Dict[str, List[str]] = defaultdict(list)  # element -> claim_ids
        self._load_claims()

    def log(self, message: str):
        """Print if verbose mode."""
        if self.verbose:
            print(f"  {message}")

    def _load_claims(self):
        """Load existing claims from file."""
        if CLAIMS_FILE.exists():
            try:
                with open(CLAIMS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for claim_data in data.get('claims', []):
                        claim = MorphologicalClaim(**claim_data)
                        self.claims[claim.claim_id] = claim
                        self.claim_index[claim.element].append(claim.claim_id)
                    for contra_data in data.get('contradictions', []):
                        self.contradictions.append(Contradiction(**contra_data))
                self.log(f"Loaded {len(self.claims)} claims, {len(self.contradictions)} contradictions")
            except Exception as e:
                self.log(f"Error loading claims: {e}")

    def _save_claims(self):
        """Save claims to file."""
        data = {
            'generated': datetime.now().isoformat(),
            'total_claims': len(self.claims),
            'total_contradictions': len(self.contradictions),
            'claims': [asdict(c) for c in self.claims.values()],
            'contradictions': [asdict(c) for c in self.contradictions],
        }
        CLAIMS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CLAIMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.log(f"Saved {len(self.claims)} claims")

    def _generate_claim_id(self) -> str:
        """Generate unique claim ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(self.claims) + 1
        return f"CLM-{timestamp}-{count:04d}"

    def _generate_contradiction_id(self) -> str:
        """Generate unique contradiction ID."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        count = len(self.contradictions) + 1
        return f"CTR-{timestamp}-{count:04d}"

    def register_claim(
        self,
        element: str,
        assertion: str,
        hypothesis: str,
        confidence: str,
        evidence: List[Dict],
        phase: str,
        sample_size: int,
        claim_type: str = "morphological"
    ) -> Tuple[MorphologicalClaim, Optional[Contradiction]]:
        """
        Register a new morphological claim and check for contradictions.

        Args:
            element: The morpheme being analyzed (e.g., "-U", "KU-RO")
            assertion: What is claimed (e.g., "nominative singular marker")
            hypothesis: Linguistic hypothesis (luwian/semitic/pregreek/protogreek)
            confidence: Confidence level
            evidence: List of evidence dictionaries
            phase: Which analysis phase (e.g., "Phase 1", "MINOS Phase 2")
            sample_size: Number of examples examined
            claim_type: Type of claim (morphological/lexical/etc.)

        Returns:
            Tuple of (new claim, contradiction if found)
        """
        claim_id = self._generate_claim_id()

        claim = MorphologicalClaim(
            claim_id=claim_id,
            claim_type=ClaimType(claim_type),
            element=element.upper(),
            assertion=assertion,
            hypothesis=hypothesis.lower(),
            confidence=ConfidenceLevel(confidence),
            evidence=evidence,
            phase=phase,
            sample_size=sample_size,
            contradicting_evidence=[],
            timestamp=datetime.now().isoformat(),
        )

        # Check for contradictions with existing claims
        contradiction = self._check_contradictions(claim)

        # Register the claim
        self.claims[claim_id] = claim
        self.claim_index[claim.element].append(claim_id)

        self._save_claims()

        return claim, contradiction

    def _check_contradictions(self, new_claim: MorphologicalClaim) -> Optional[Contradiction]:
        """
        Check if new claim contradicts existing claims.

        Contradiction types:
        1. Same element, different hypothesis, high confidence both
        2. Same element, same hypothesis, contradictory assertion
        3. Sample size disparity (large sample vs small sample)
        """
        element = new_claim.element
        existing_claims = [self.claims[cid] for cid in self.claim_index.get(element, [])]

        for existing in existing_claims:
            if existing.superseded_by:
                continue  # Skip superseded claims

            contradiction = None

            # Type 1: Different hypotheses with high confidence
            if (existing.hypothesis != new_claim.hypothesis and
                existing.confidence in [ConfidenceLevel.CERTAIN, ConfidenceLevel.PROBABLE] and
                new_claim.confidence in [ConfidenceLevel.CERTAIN, ConfidenceLevel.PROBABLE]):

                contradiction = Contradiction(
                    contradiction_id=self._generate_contradiction_id(),
                    claim_a=existing.claim_id,
                    claim_b=new_claim.claim_id,
                    element=element,
                    description=(
                        f"HIGH-CONFIDENCE CONFLICT: {element} claimed as "
                        f"{existing.hypothesis.upper()} ({existing.assertion}) in {existing.phase} "
                        f"vs {new_claim.hypothesis.upper()} ({new_claim.assertion}) in {new_claim.phase}"
                    ),
                    severity="HIGH",
                    resolution_guidance=(
                        f"Compare sample sizes: {existing.sample_size} vs {new_claim.sample_size}. "
                        f"Re-examine evidence. Consider whether {element} has multiple functions "
                        f"or if one analysis is incorrect. Per First Principle #2, follow evidence."
                    ),
                    detected_at=datetime.now().isoformat(),
                )

            # Type 2: Same hypothesis, contradictory assertion
            elif (existing.hypothesis == new_claim.hypothesis and
                  self._assertions_contradict(existing.assertion, new_claim.assertion)):

                contradiction = Contradiction(
                    contradiction_id=self._generate_contradiction_id(),
                    claim_a=existing.claim_id,
                    claim_b=new_claim.claim_id,
                    element=element,
                    description=(
                        f"ASSERTION CONFLICT within {existing.hypothesis.upper()}: "
                        f"'{existing.assertion}' ({existing.phase}) vs "
                        f"'{new_claim.assertion}' ({new_claim.phase})"
                    ),
                    severity="MEDIUM",
                    resolution_guidance=(
                        f"Same hypothesis, different functions. Check if context-dependent "
                        f"(e.g., different positions = different functions). "
                        f"Larger sample ({max(existing.sample_size, new_claim.sample_size)}) may be more reliable."
                    ),
                    detected_at=datetime.now().isoformat(),
                )

            # Type 3: Major sample size disparity
            elif (existing.sample_size > 0 and new_claim.sample_size > 0 and
                  max(existing.sample_size, new_claim.sample_size) /
                  min(existing.sample_size, new_claim.sample_size) > 10):

                smaller = existing if existing.sample_size < new_claim.sample_size else new_claim
                larger = new_claim if existing.sample_size < new_claim.sample_size else existing

                contradiction = Contradiction(
                    contradiction_id=self._generate_contradiction_id(),
                    claim_a=existing.claim_id,
                    claim_b=new_claim.claim_id,
                    element=element,
                    description=(
                        f"SAMPLE SIZE DISPARITY: {smaller.phase} used n={smaller.sample_size} "
                        f"vs {larger.phase} used n={larger.sample_size}"
                    ),
                    severity="LOW",
                    resolution_guidance=(
                        f"Larger sample ({larger.sample_size}) likely more representative. "
                        f"Consider if smaller sample captured edge cases or errors."
                    ),
                    detected_at=datetime.now().isoformat(),
                )

            if contradiction:
                self.contradictions.append(contradiction)
                return contradiction

        return None

    def _assertions_contradict(self, a1: str, a2: str) -> bool:
        """
        Determine if two assertions contradict each other.

        Simple heuristic: look for opposing terms.
        """
        a1_lower = a1.lower()
        a2_lower = a2.lower()

        # Direct opposites
        opposites = [
            ("nominative", "accusative"),
            ("nominative", "genitive"),
            ("nominative", "dative"),
            ("singular", "plural"),
            ("prefix", "suffix"),
            ("verbal", "nominal"),
            ("total", "deficit"),
            ("100%", "0%"),
        ]

        for term1, term2 in opposites:
            if (term1 in a1_lower and term2 in a2_lower) or \
               (term2 in a1_lower and term1 in a2_lower):
                return True

        # Percentage conflicts (e.g., "100% Semitic" vs "64% Luwian")
        pct_pattern = r'(\d+)%'
        matches_a1 = re.findall(pct_pattern, a1)
        matches_a2 = re.findall(pct_pattern, a2)

        if matches_a1 and matches_a2:
            # If both claim high percentages for different things
            if int(matches_a1[0]) > 80 and int(matches_a2[0]) > 80:
                # Check if they're about different hypotheses
                hyps = ['semitic', 'luwian', 'greek', 'pregreek']
                h1 = [h for h in hyps if h in a1_lower]
                h2 = [h for h in hyps if h in a2_lower]
                if h1 and h2 and h1[0] != h2[0]:
                    return True

        return False

    def supersede_claim(self, old_claim_id: str, new_claim_id: str, reason: str):
        """Mark an older claim as superseded by a newer one."""
        if old_claim_id in self.claims:
            self.claims[old_claim_id].superseded_by = new_claim_id
            self.claims[old_claim_id].contradicting_evidence.append({
                'reason': reason,
                'superseded_by': new_claim_id,
                'timestamp': datetime.now().isoformat(),
            })
            self._save_claims()

    def get_claims_for_element(self, element: str) -> List[MorphologicalClaim]:
        """Get all claims about a specific element."""
        element_upper = element.upper()
        claim_ids = self.claim_index.get(element_upper, [])
        return [self.claims[cid] for cid in claim_ids if cid in self.claims]

    def get_active_contradictions(self) -> List[Contradiction]:
        """Get all unresolved contradictions."""
        # A contradiction is resolved if one of its claims is superseded
        active = []
        for c in self.contradictions:
            claim_a = self.claims.get(c.claim_a)
            claim_b = self.claims.get(c.claim_b)
            if claim_a and claim_b:
                if not claim_a.superseded_by and not claim_b.superseded_by:
                    active.append(c)
        return active

    def validate_phase_files(self) -> Dict:
        """
        Scan analysis phase files and extract claims for validation.

        Looks for patterns like:
        - "-U ending: 64% Luwian"
        - "KU-RO = total (CERTAIN)"
        - "Semitic hypothesis: SUPPORTED"
        """
        results = {
            'phases_scanned': 0,
            'claims_extracted': 0,
            'contradictions_found': 0,
            'phase_summaries': {},
        }

        if not ANALYSIS_DIR.exists():
            self.log(f"Analysis directory not found: {ANALYSIS_DIR}")
            return results

        # Find all phase files
        phase_files = list(ANALYSIS_DIR.glob("PHASE*.md")) + \
                      list(ANALYSIS_DIR.glob("*phase*.md")) + \
                      list(ANALYSIS_DIR.glob("MINOS_*.md"))

        for pf in phase_files:
            results['phases_scanned'] += 1
            phase_name = pf.stem

            try:
                content = pf.read_text(encoding='utf-8')
                claims = self._extract_claims_from_text(content, phase_name)
                results['claims_extracted'] += len(claims)
                results['phase_summaries'][phase_name] = {
                    'claims_found': len(claims),
                    'file': str(pf),
                }
            except Exception as e:
                self.log(f"Error processing {pf}: {e}")

        results['contradictions_found'] = len(self.get_active_contradictions())
        return results

    def _extract_claims_from_text(self, text: str, phase: str) -> List[Dict]:
        """
        Extract morphological claims from analysis text.

        Patterns to detect:
        - "X = Y" (lexical claims)
        - "X ending: N% hypothesis" (morphological statistics)
        - "hypothesis: VERDICT" (hypothesis verdicts)
        """
        claims = []

        # Pattern 1: "-X ending: N% HYPOTHESIS"
        ending_pattern = r'(-\w+)\s+ending[s]?:?\s*(\d+)%\s*(\w+)'
        for match in re.finditer(ending_pattern, text, re.IGNORECASE):
            element, percentage, hypothesis = match.groups()
            claims.append({
                'element': element.upper(),
                'assertion': f"{percentage}% {hypothesis}",
                'hypothesis': hypothesis.lower(),
                'phase': phase,
            })

        # Pattern 2: "WORD = meaning (CONFIDENCE)"
        lexical_pattern = r'([A-Z]+-[A-Z]+(?:-[A-Z]+)*)\s*=\s*([^(]+)\((\w+)\)'
        for match in re.finditer(lexical_pattern, text):
            word, meaning, confidence = match.groups()
            claims.append({
                'element': word.upper(),
                'assertion': meaning.strip(),
                'confidence': confidence.upper(),
                'phase': phase,
            })

        # Pattern 3: "hypothesis: VERDICT"
        verdict_pattern = r'(luwian|semitic|pregreek|protogreek|proto-greek)[\s:]+(\w+)'
        for match in re.finditer(verdict_pattern, text, re.IGNORECASE):
            hypothesis, verdict = match.groups()
            if verdict.upper() in ['SUPPORTED', 'CONTRADICTED', 'NEUTRAL', 'POSSIBLE', 'PROBABLE']:
                claims.append({
                    'element': 'CORPUS',
                    'assertion': f"{hypothesis}: {verdict}",
                    'hypothesis': hypothesis.lower().replace('-', ''),
                    'phase': phase,
                })

        return claims

    def print_report(self):
        """Print validation report."""
        print("\n" + "=" * 70)
        print("PHASE VALIDATOR REPORT")
        print("=" * 70)
        print("First Principle #2: Abandon hypotheses when evidence contradicts\n")

        # Summary statistics
        print(f"Total claims registered: {len(self.claims)}")
        print(f"Active contradictions: {len(self.get_active_contradictions())}")

        # Claims by element
        print("\nClaims by Element:")
        element_counts = defaultdict(int)
        for claim in self.claims.values():
            element_counts[claim.element] += 1
        for element, count in sorted(element_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"  {element}: {count} claims")

        # Active contradictions
        active = self.get_active_contradictions()
        if active:
            print("\n" + "=" * 70)
            print("ACTIVE CONTRADICTIONS (require resolution)")
            print("=" * 70)
            for c in active:
                print(f"\n[{c.contradiction_id}] {c.severity} SEVERITY")
                print(f"  Element: {c.element}")
                print(f"  {c.description}")
                print(f"  Resolution: {c.resolution_guidance}")

        # High-confidence claims
        high_conf = [c for c in self.claims.values()
                     if c.confidence in [ConfidenceLevel.CERTAIN, ConfidenceLevel.PROBABLE]
                     and not c.superseded_by]
        if high_conf:
            print("\n" + "=" * 70)
            print("HIGH-CONFIDENCE CLAIMS (CERTAIN/PROBABLE)")
            print("=" * 70)
            for c in sorted(high_conf, key=lambda x: x.element)[:15]:
                print(f"  {c.element}: {c.assertion} [{c.hypothesis.upper()}] - {c.confidence.value}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate consistency across Linear A analysis phases"
    )
    parser.add_argument(
        '--check-all',
        action='store_true',
        help='Scan all phase files and check for contradictions'
    )
    parser.add_argument(
        '--claim',
        type=str,
        help='Register a new claim (format: "ELEMENT = assertion")'
    )
    parser.add_argument(
        '--hypothesis',
        type=str,
        default='unknown',
        help='Linguistic hypothesis for the claim'
    )
    parser.add_argument(
        '--confidence',
        type=str,
        default='POSSIBLE',
        choices=['CERTAIN', 'PROBABLE', 'POSSIBLE', 'SPECULATIVE'],
        help='Confidence level'
    )
    parser.add_argument(
        '--phase',
        type=str,
        default='manual',
        help='Analysis phase name'
    )
    parser.add_argument(
        '--sample-size',
        type=int,
        default=1,
        help='Number of examples examined'
    )
    parser.add_argument(
        '--element',
        type=str,
        help='Check claims for a specific element'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A PHASE VALIDATOR")
    print("=" * 60)
    print("Enforcing First Principle #2: Follow evidence, not theory\n")

    validator = PhaseValidator(verbose=args.verbose)

    if args.check_all:
        print("Scanning analysis phase files...")
        results = validator.validate_phase_files()
        print(f"  Phases scanned: {results['phases_scanned']}")
        print(f"  Claims extracted: {results['claims_extracted']}")
        print(f"  Contradictions found: {results['contradictions_found']}")
        validator.print_report()

    elif args.claim:
        # Parse claim format: "ELEMENT = assertion"
        if '=' in args.claim:
            parts = args.claim.split('=', 1)
            element = parts[0].strip()
            assertion = parts[1].strip()
        else:
            element = args.claim
            assertion = "unspecified"

        claim, contradiction = validator.register_claim(
            element=element,
            assertion=assertion,
            hypothesis=args.hypothesis,
            confidence=args.confidence,
            evidence=[{'source': 'CLI input', 'phase': args.phase}],
            phase=args.phase,
            sample_size=args.sample_size,
        )

        print(f"Registered claim: {claim.claim_id}")
        print(f"  Element: {claim.element}")
        print(f"  Assertion: {claim.assertion}")
        print(f"  Hypothesis: {claim.hypothesis}")
        print(f"  Confidence: {claim.confidence.value}")

        if contradiction:
            print(f"\n⚠️  CONTRADICTION DETECTED!")
            print(f"  {contradiction.description}")
            print(f"  Resolution: {contradiction.resolution_guidance}")

    elif args.element:
        claims = validator.get_claims_for_element(args.element)
        if claims:
            print(f"Claims for {args.element.upper()}:")
            for c in claims:
                status = "[SUPERSEDED]" if c.superseded_by else ""
                print(f"  [{c.claim_id}] {c.assertion} - {c.hypothesis} {c.confidence.value} {status}")
        else:
            print(f"No claims found for {args.element}")

    else:
        validator.print_report()

    return 0


if __name__ == '__main__':
    sys.exit(main())
