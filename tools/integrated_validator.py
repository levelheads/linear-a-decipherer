#!/usr/bin/env python3
"""
Integrated Validator for Linear A

Combines all four methodological improvement systems into a unified pipeline:

1. Raw hypothesis score (from hypothesis_tester.py)
   → 2. Apply regional weight (from regional_weighting.py)
   → 3. Apply negative evidence penalty (from negative_evidence_catalog.json)
   → 4. Classify via falsification thresholds (from falsification_system.py)
   → 5. Calculate Bayesian posterior with credible interval (from bayesian_hypothesis_tester.py)
   → 6. Check anchor dependencies (from anchor_tracker.py)

Output: Unified, methodology-compliant assessment

Usage:
    python tools/integrated_validator.py --word KU-RO --detail
    python tools/integrated_validator.py --all --output data/integrated_results.json
    python tools/integrated_validator.py --summary
    python tools/integrated_validator.py --validate-methodology

Attribution:
    Part of Linear A Decipherment Project
    Unified implementation of methodology improvements
"""

import json
import argparse
import sys
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import re
import math


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Import components (with fallbacks)
try:
    from anchor_tracker import AnchorTracker, CascadeResult
except ImportError:
    AnchorTracker = None

try:
    from falsification_system import FalsificationSystem, THRESHOLDS
except ImportError:
    FalsificationSystem = None
    THRESHOLDS = {
        'ELIMINATED': type('T', (), {'min_pct': 0, 'max_pct': 5})(),
        'WEAK': type('T', (), {'min_pct': 5, 'max_pct': 15})(),
        'MODERATE': type('T', (), {'min_pct': 15, 'max_pct': 25})(),
        'STRONG': type('T', (), {'min_pct': 25, 'max_pct': 100})(),
    }

try:
    from regional_weighting import RegionalWeighting
except ImportError:
    RegionalWeighting = None

try:
    from bayesian_hypothesis_tester import BayesianHypothesisTester, DEFAULT_PRIORS
except ImportError:
    BayesianHypothesisTester = None
    DEFAULT_PRIORS = {
        'luwian': 0.25, 'semitic': 0.15, 'pregreek': 0.20,
        'protogreek': 0.05, 'isolate': 0.35
    }


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class IntegratedAssessment:
    """Complete assessment of a word through all validation stages."""
    word: str
    frequency: int

    # Stage 1: Raw hypothesis testing
    raw_scores: Dict[str, float]
    raw_best_hypothesis: str
    raw_support_pct: float

    # Stage 2: Regional weighting
    site_distribution: Dict[str, int]
    num_sites: int
    ht_concentration: float
    regional_weight: float
    regional_rationale: List[str]

    # Stage 3: Negative evidence
    negative_evidence_penalty: float
    negative_evidence_items: List[str]

    # Stage 4: Falsification threshold
    adjusted_pct: float
    threshold_category: str
    threshold_interpretation: str

    # Stage 5: Bayesian posterior
    bayesian_posteriors: Dict[str, float]
    credible_interval_95: Tuple[float, float]
    bayes_factor: float
    bayesian_best: str

    # Stage 6: Anchor dependencies
    anchor_dependencies: List[str]
    max_confidence_from_anchors: str
    dependency_warnings: List[str]

    # Final synthesis
    final_assessment: str
    final_confidence: str
    methodology_compliant: bool
    compliance_notes: List[str]


class IntegratedValidator:
    """
    Unified validator combining all methodological improvements.

    Pipeline:
    1. Get raw hypothesis scores
    2. Apply regional weighting
    3. Apply negative evidence penalty
    4. Classify against falsification thresholds
    5. Calculate Bayesian posteriors
    6. Check anchor dependencies
    7. Generate final methodology-compliant assessment
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = {}
        self.hypothesis_results = {}
        self.negative_evidence = []
        self.anchors = {}
        self.reading_dependencies = {}

        # Component instances
        self.regional_weighting = None
        self.bayesian_tester = None
        self.anchor_tracker = None
        self.falsification_system = None

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_all_data(self) -> bool:
        """Load all required data and initialize components."""
        try:
            # Load corpus
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)
            print(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")

            # Load hypothesis results
            hyp_path = DATA_DIR / "hypothesis_results.json"
            if hyp_path.exists():
                with open(hyp_path, 'r', encoding='utf-8') as f:
                    self.hypothesis_results = json.load(f)

            # Load negative evidence catalog
            neg_path = DATA_DIR / "negative_evidence_catalog.json"
            if neg_path.exists():
                with open(neg_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.negative_evidence = data.get('absences', [])

            # Load anchors
            anchor_path = DATA_DIR / "anchors.json"
            if anchor_path.exists():
                with open(anchor_path, 'r', encoding='utf-8') as f:
                    self.anchors = json.load(f).get('anchors', {})

            # Load reading dependencies
            dep_path = DATA_DIR / "reading_dependencies.json"
            if dep_path.exists():
                with open(dep_path, 'r', encoding='utf-8') as f:
                    self.reading_dependencies = json.load(f).get('readings', {})

            # Initialize components
            if RegionalWeighting:
                self.regional_weighting = RegionalWeighting(verbose=self.verbose)
                self.regional_weighting.load_data()

            if BayesianHypothesisTester:
                self.bayesian_tester = BayesianHypothesisTester(verbose=self.verbose)
                self.bayesian_tester.load_data()

            if AnchorTracker:
                self.anchor_tracker = AnchorTracker(verbose=self.verbose)
                self.anchor_tracker.load_data()

            if FalsificationSystem:
                self.falsification_system = FalsificationSystem(verbose=self.verbose)
                self.falsification_system.load_data()

            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _get_raw_scores(self, word: str) -> Tuple[Dict[str, float], str, float]:
        """Get raw hypothesis scores for a word."""
        word_analyses = self.hypothesis_results.get('word_analyses', {})

        # Try exact match then case-insensitive
        word_data = word_analyses.get(word) or word_analyses.get(word.upper())

        if word_data:
            hypotheses = word_data.get('hypotheses', {})
            scores = {
                'luwian': hypotheses.get('luwian', {}).get('score', 0),
                'semitic': hypotheses.get('semitic', {}).get('score', 0),
                'pregreek': hypotheses.get('pregreek', {}).get('score', 0),
                'protogreek': hypotheses.get('protogreek', {}).get('score', 0),
            }
            synthesis = word_data.get('synthesis', {})
            best = synthesis.get('best_hypothesis', 'unknown')

            # Calculate support percentage from summaries
            summaries = self.hypothesis_results.get('hypothesis_summaries', {})
            total = self.hypothesis_results.get('metadata', {}).get('words_tested', 198)
            supported = summaries.get(best, {}).get('supported', 0)
            pct = supported / total * 100 if total > 0 else 0

            return scores, best, pct

        # Default if not found
        return {'luwian': 0, 'semitic': 0, 'pregreek': 0, 'protogreek': 0}, 'unknown', 0

    def _get_regional_weight(self, word: str) -> Tuple[Dict, int, float, float, List[str]]:
        """Get regional weighting for a word."""
        if self.regional_weighting:
            weighted = self.regional_weighting.weight_reading(word)
            return (
                weighted.site_distribution.site_counts,
                weighted.site_distribution.num_sites,
                weighted.site_distribution.ht_concentration,
                weighted.regional_weight,
                weighted.weight_rationale
            )

        # Fallback: calculate manually from corpus
        site_counts = Counter()
        word_upper = word.upper()

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue
            words = data.get('transliteratedWords', [])
            if any(w.upper() == word_upper for w in words):
                match = re.match(r'^([A-Z]+)', insc_id)
                if match:
                    site = match.group(1)[:2]
                    site_counts[site] += 1

        total = sum(site_counts.values())
        ht_count = site_counts.get('HT', 0)
        ht_conc = ht_count / total if total > 0 else 0

        # Calculate weight
        weight = 1.0
        rationale = []
        num_sites = len([s for s in site_counts if site_counts[s] > 0])

        if num_sites >= 2:
            bonus = math.log2(num_sites) * 0.1
            weight += bonus
            rationale.append(f"Diversity bonus: +{bonus:.2f}")

        if ht_conc > 0.5:
            penalty = (ht_conc - 0.5) * 0.5
            weight -= penalty
            rationale.append(f"HT penalty: -{penalty:.2f}")

        weight = max(0.3, min(1.5, weight))

        return dict(site_counts), num_sites, round(ht_conc, 3), round(weight, 3), rationale

    def _get_negative_penalty(self, hypothesis: str) -> Tuple[float, List[str]]:
        """Get negative evidence penalty for a hypothesis."""
        penalty = 0.0
        items = []

        for absence in self.negative_evidence:
            if absence.get('hypothesis', '').lower() == hypothesis.lower():
                if absence.get('falsifies', False):
                    penalty += 0.3
                    items.append(f"CRITICAL: {absence.get('pattern', 'Unknown')}")
                elif absence.get('status') == 'CERTAIN':
                    penalty += 0.1
                    items.append(f"Certain: {absence.get('id', 'Unknown')}")
                elif absence.get('status') == 'PROBABLE':
                    penalty += 0.05
                    items.append(f"Probable: {absence.get('id', 'Unknown')}")

        return min(penalty, 0.5), items

    def _get_threshold_category(self, pct: float) -> Tuple[str, str]:
        """Get falsification threshold category."""
        for category, threshold in THRESHOLDS.items():
            if hasattr(threshold, 'min_pct'):
                if threshold.min_pct <= pct < threshold.max_pct:
                    return category, getattr(threshold, 'interpretation', category)
        return 'STRONG' if pct >= 25 else 'ELIMINATED', 'Unknown category'

    def _get_bayesian_posteriors(self, word: str, frequency: int) -> Tuple[Dict, Tuple, float, str]:
        """Get Bayesian posteriors for a word."""
        if self.bayesian_tester:
            result = self.bayesian_tester.compute_posterior(word, frequency)
            best_hyp = result.best_hypothesis
            ci = result.credible_intervals.get(best_hyp, (0, 1))
            bf = result.bayes_factors.get(best_hyp, 1.0)
            return result.posteriors, ci, bf, best_hyp

        # Fallback: simple estimate based on priors
        posteriors = DEFAULT_PRIORS.copy()
        return posteriors, (0.0, 1.0), 1.0, max(posteriors.keys(), key=lambda k: posteriors[k])

    def _get_anchor_dependencies(self, word: str) -> Tuple[List[str], str, List[str]]:
        """Get anchor dependencies and constraints for a reading."""
        reading_data = self.reading_dependencies.get(word) or self.reading_dependencies.get(word.upper())

        if reading_data:
            deps = reading_data.get('depends_on', [])
            max_conf = reading_data.get('max_confidence', 'SPECULATIVE')

            # Check for warnings
            warnings = []
            for dep in deps:
                anchor = self.anchors.get(dep, {})
                if anchor.get('confidence') in ['LOW', 'SPECULATIVE']:
                    warnings.append(f"Low-confidence anchor: {dep}")

            return deps, max_conf, warnings

        return [], 'SPECULATIVE', ['No registered dependencies']

    def _synthesize_assessment(self, stages: dict) -> Tuple[str, str, bool, List[str]]:
        """
        Synthesize final assessment from all stages.

        Returns:
            (assessment_text, final_confidence, is_compliant, compliance_notes)
        """
        compliance_notes = []
        is_compliant = True

        # Check methodology compliance
        # Rule 1: Confidence cannot exceed anchor max
        anchor_max = stages['anchor_max']
        bayesian_best = stages['bayesian_best']
        bayes_factor = stages['bayes_factor']

        # Determine base confidence from Bayesian analysis
        best_posterior = stages['posteriors'].get(bayesian_best, 0)
        if best_posterior > 0.5:
            base_conf = 'HIGH'
        elif best_posterior > 0.3:
            base_conf = 'PROBABLE'
        elif best_posterior > 0.15:
            base_conf = 'POSSIBLE'
        else:
            base_conf = 'SPECULATIVE'

        # Apply threshold classification
        threshold_cat = stages['threshold_category']
        if threshold_cat == 'ELIMINATED':
            base_conf = 'SPECULATIVE'
            compliance_notes.append("Hypothesis eliminated by threshold (<5%)")

        # Apply anchor cap
        conf_order = ['SPECULATIVE', 'POSSIBLE', 'LOW', 'MEDIUM', 'PROBABLE', 'HIGH', 'CERTAIN']
        base_rank = conf_order.index(base_conf) if base_conf in conf_order else 0
        anchor_rank = conf_order.index(anchor_max) if anchor_max in conf_order else 0

        if base_rank > anchor_rank:
            compliance_notes.append(f"Confidence capped at {anchor_max} by anchor constraints")
            base_conf = anchor_max

        # Apply regional weight penalty
        regional_weight = stages['regional_weight']
        if regional_weight < 0.7:
            compliance_notes.append(f"Regional weight penalty applied ({regional_weight:.2f})")
            if base_conf in ['HIGH', 'CERTAIN']:
                base_conf = 'PROBABLE'
                compliance_notes.append("Demoted due to low regional diversity")

        # Apply negative evidence
        neg_penalty = stages['neg_penalty']
        if neg_penalty > 0.2:
            compliance_notes.append(f"Significant negative evidence penalty ({neg_penalty:.2f})")
            if base_conf in ['HIGH', 'CERTAIN', 'PROBABLE']:
                base_conf = 'POSSIBLE'
                compliance_notes.append("Demoted due to negative evidence")

        # Check for single-hypothesis support
        supported_hyps = [h for h, p in stages['posteriors'].items()
                        if p > 0.15 and h != 'isolate']
        if len(supported_hyps) == 1 and base_conf in ['HIGH', 'CERTAIN']:
            base_conf = 'PROBABLE'
            compliance_notes.append("Capped at PROBABLE (single-hypothesis support)")

        # Generate assessment text
        best_hyp = stages['bayesian_best']
        assessment = (
            f"{best_hyp.upper()} supported | "
            f"Threshold: {threshold_cat} | "
            f"Bayesian P={best_posterior:.2f} (BF={bayes_factor:.1f}) | "
            f"Regional weight: {regional_weight:.2f}"
        )

        # Check overall compliance
        if not stages['anchor_deps']:
            is_compliant = False
            compliance_notes.append("WARNING: No anchor dependencies registered")

        if stages['dependency_warnings']:
            compliance_notes.extend(stages['dependency_warnings'])

        return assessment, base_conf, is_compliant, compliance_notes

    def validate_word(self, word: str, frequency: int = 1) -> IntegratedAssessment:
        """
        Run full integrated validation pipeline for a word.
        """
        # Stage 1: Raw hypothesis scores
        raw_scores, raw_best, raw_pct = self._get_raw_scores(word)

        # Stage 2: Regional weighting
        site_dist, num_sites, ht_conc, regional_weight, regional_rationale = self._get_regional_weight(word)

        # Stage 3: Negative evidence
        neg_penalty, neg_items = self._get_negative_penalty(raw_best)

        # Stage 4: Adjusted percentage and threshold
        adjusted_pct = raw_pct * regional_weight * (1 - neg_penalty)
        threshold_cat, threshold_interp = self._get_threshold_category(adjusted_pct)

        # Stage 5: Bayesian posteriors
        posteriors, ci, bf, bayes_best = self._get_bayesian_posteriors(word, frequency)

        # Stage 6: Anchor dependencies
        anchor_deps, anchor_max, dep_warnings = self._get_anchor_dependencies(word)

        # Synthesize final assessment
        stages = {
            'threshold_category': threshold_cat,
            'posteriors': posteriors,
            'bayesian_best': bayes_best,
            'bayes_factor': bf,
            'regional_weight': regional_weight,
            'neg_penalty': neg_penalty,
            'anchor_max': anchor_max,
            'anchor_deps': anchor_deps,
            'dependency_warnings': dep_warnings,
        }

        assessment, confidence, compliant, notes = self._synthesize_assessment(stages)

        return IntegratedAssessment(
            word=word,
            frequency=frequency,
            raw_scores=raw_scores,
            raw_best_hypothesis=raw_best,
            raw_support_pct=round(raw_pct, 2),
            site_distribution=site_dist,
            num_sites=num_sites,
            ht_concentration=round(ht_conc, 3),
            regional_weight=regional_weight,
            regional_rationale=regional_rationale,
            negative_evidence_penalty=neg_penalty,
            negative_evidence_items=neg_items,
            adjusted_pct=round(adjusted_pct, 2),
            threshold_category=threshold_cat,
            threshold_interpretation=threshold_interp,
            bayesian_posteriors=posteriors,
            credible_interval_95=ci,
            bayes_factor=bf,
            bayesian_best=bayes_best,
            anchor_dependencies=anchor_deps,
            max_confidence_from_anchors=anchor_max,
            dependency_warnings=dep_warnings,
            final_assessment=assessment,
            final_confidence=confidence,
            methodology_compliant=compliant,
            compliance_notes=notes
        )

    def validate_all(self, min_freq: int = 2) -> List[IntegratedAssessment]:
        """Validate all words in corpus above frequency threshold."""
        # Get word frequencies
        word_freq = Counter()
        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue
            for word in data.get('transliteratedWords', []):
                if word and '-' in word and word not in ['\n', '𐄁', '']:
                    word_freq[word.upper()] += 1

        results = []
        for word, freq in word_freq.most_common():
            if freq >= min_freq:
                result = self.validate_word(word, freq)
                results.append(result)
                self.log(f"{word}: {result.final_confidence} ({result.final_assessment[:40]}...)")

        return results

    def generate_report(self, results: List[IntegratedAssessment]) -> Dict:
        """Generate comprehensive integrated validation report."""
        # Group by confidence
        by_confidence = defaultdict(list)
        for r in results:
            by_confidence[r.final_confidence].append(r)

        # Group by threshold category
        by_threshold = defaultdict(list)
        for r in results:
            by_threshold[r.threshold_category].append(r)

        # Compliance statistics
        compliant = [r for r in results if r.methodology_compliant]
        non_compliant = [r for r in results if not r.methodology_compliant]

        report = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'method': 'Integrated Validation Pipeline',
                'stages': [
                    '1. Raw hypothesis scores',
                    '2. Regional weighting',
                    '3. Negative evidence penalty',
                    '4. Falsification threshold',
                    '5. Bayesian posterior',
                    '6. Anchor dependency check',
                    '7. Final synthesis'
                ],
                'words_validated': len(results)
            },
            'summary': {
                'by_confidence': {k: len(v) for k, v in by_confidence.items()},
                'by_threshold': {k: len(v) for k, v in by_threshold.items()},
                'methodology_compliant': len(compliant),
                'non_compliant': len(non_compliant),
                'compliance_rate': round(len(compliant) / len(results) * 100, 1) if results else 0
            },
            'high_confidence_readings': [
                asdict(r) for r in results
                if r.final_confidence in ['HIGH', 'CERTAIN', 'PROBABLE']
            ][:50],
            'non_compliant_readings': [
                {
                    'word': r.word,
                    'confidence': r.final_confidence,
                    'issues': r.compliance_notes
                }
                for r in non_compliant[:20]
            ],
            'all_results': [asdict(r) for r in results]
        }

        return report

    def print_assessment(self, result: IntegratedAssessment):
        """Print formatted integrated assessment."""
        print(f"\n{'='*70}")
        print(f"INTEGRATED VALIDATION: {result.word}")
        print(f"{'='*70}")

        print("\n[1] RAW HYPOTHESIS SCORES")
        print(f"    Best: {result.raw_best_hypothesis} ({result.raw_support_pct}%)")
        for hyp, score in sorted(result.raw_scores.items(), key=lambda x: -x[1]):
            print(f"    {hyp:12} score: {score:.1f}")

        print("\n[2] REGIONAL WEIGHTING")
        print(f"    Sites: {result.num_sites} | HT concentration: {result.ht_concentration:.0%}")
        print(f"    Weight: {result.regional_weight:.3f}")
        for r in result.regional_rationale[:3]:
            print(f"    • {r}")

        print("\n[3] NEGATIVE EVIDENCE")
        print(f"    Penalty: {result.negative_evidence_penalty:.3f}")
        for item in result.negative_evidence_items[:3]:
            print(f"    • {item}")

        print("\n[4] FALSIFICATION THRESHOLD")
        print(f"    Adjusted %: {result.adjusted_pct:.1f}%")
        print(f"    Category: {result.threshold_category}")
        print(f"    → {result.threshold_interpretation[:60]}...")

        print("\n[5] BAYESIAN ANALYSIS")
        print(f"    Best: {result.bayesian_best} (P={result.bayesian_posteriors.get(result.bayesian_best, 0):.3f})")
        print(f"    95% CI: [{result.credible_interval_95[0]:.2f}, {result.credible_interval_95[1]:.2f}]")
        print(f"    Bayes Factor vs Isolate: {result.bayes_factor:.1f}")
        for hyp, post in sorted(result.bayesian_posteriors.items(), key=lambda x: -x[1])[:4]:
            print(f"    {hyp:12} P={post:.3f}")

        print("\n[6] ANCHOR DEPENDENCIES")
        print(f"    Max confidence: {result.max_confidence_from_anchors}")
        if result.anchor_dependencies:
            print(f"    Depends on: {', '.join(result.anchor_dependencies[:3])}")
        for w in result.dependency_warnings[:2]:
            print(f"    ⚠ {w}")

        print(f"\n{'─'*70}")
        print("FINAL ASSESSMENT")
        print(f"{'─'*70}")
        print(f"    {result.final_assessment}")
        print(f"    Confidence: {result.final_confidence}")
        compliant_str = "✓ YES" if result.methodology_compliant else "✗ NO"
        print(f"    Methodology Compliant: {compliant_str}")
        if result.compliance_notes:
            print("    Notes:")
            for note in result.compliance_notes:
                print(f"      • {note}")

        print(f"\n{'='*70}")

    def print_summary(self, report: Dict):
        """Print summary of integrated validation."""
        print("\n" + "=" * 70)
        print("INTEGRATED VALIDATION SUMMARY")
        print("=" * 70)

        summary = report['summary']

        print(f"\nWords Validated: {report['metadata']['words_validated']}")

        print("\nBy Final Confidence:")
        conf_order = ['CERTAIN', 'HIGH', 'PROBABLE', 'POSSIBLE', 'SPECULATIVE']
        for conf in conf_order:
            count = summary['by_confidence'].get(conf, 0)
            if count > 0:
                print(f"  {conf:12} {count:4d}")

        print("\nBy Threshold Category:")
        for cat in ['STRONG', 'MODERATE', 'WEAK', 'ELIMINATED']:
            count = summary['by_threshold'].get(cat, 0)
            if count > 0:
                print(f"  {cat:12} {count:4d}")

        print("\nMethodology Compliance:")
        print(f"  Compliant:     {summary['methodology_compliant']:4d} ({summary['compliance_rate']}%)")
        print(f"  Non-compliant: {summary['non_compliant']:4d}")

        if report['non_compliant_readings']:
            print("\nTop Non-Compliant Issues:")
            for item in report['non_compliant_readings'][:5]:
                print(f"  {item['word']}: {item['issues'][0] if item['issues'] else 'Unknown'}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Integrated validation combining all methodological improvements"
    )
    parser.add_argument(
        '--word', '-w',
        type=str,
        help='Validate a specific word'
    )
    parser.add_argument(
        '--detail', '-d',
        action='store_true',
        help='Show detailed stage breakdown'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Validate all words in corpus'
    )
    parser.add_argument(
        '--min-freq', '-m',
        type=int,
        default=2,
        help='Minimum frequency for --all (default: 2)'
    )
    parser.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Show methodology summary'
    )
    parser.add_argument(
        '--validate-methodology',
        action='store_true',
        help='Validate methodology compliance'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output path for JSON report'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A INTEGRATED VALIDATOR")
    print("=" * 70)
    print("Combining: Hypothesis Testing → Regional Weighting → Negative Evidence")
    print("         → Falsification Thresholds → Bayesian Analysis → Anchor Dependencies")

    validator = IntegratedValidator(verbose=args.verbose)
    if not validator.load_all_data():
        return 1

    if args.summary:
        print("\nMethodology Pipeline:")
        print("  1. Raw hypothesis scores from hypothesis_tester.py")
        print("  2. Regional weight adjustment for site concentration")
        print("  3. Negative evidence penalty from canonical absences")
        print("  4. Classification against falsification thresholds")
        print("  5. Bayesian posterior with credible intervals")
        print("  6. Anchor dependency constraint checking")
        print("  7. Final methodology-compliant synthesis")
        return 0

    if args.word:
        result = validator.validate_word(args.word)
        validator.print_assessment(result)
        return 0

    if args.all or args.validate_methodology:
        print(f"\nValidating all words (min freq >= {args.min_freq})...")
        results = validator.validate_all(min_freq=args.min_freq)
        report = validator.generate_report(results)
        validator.print_summary(report)

        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\nReport saved to: {output_path}")

        return 0

    # Default: show usage
    print("\nUsage:")
    print("  --word WORD    Validate a specific word")
    print("  --all          Validate all words")
    print("  --summary      Show methodology summary")

    return 0


if __name__ == '__main__':
    sys.exit(main())
