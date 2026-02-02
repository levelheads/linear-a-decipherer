#!/usr/bin/env python3
"""
Falsification Threshold System for Linear A

Defines explicit rejection/acceptance thresholds for hypothesis testing.
Addresses the methodological critique: "At what point is a hypothesis rejected?
The methodology eliminated Proto-Greek at 2.5%, but what made 2.5% the threshold?"

Thresholds:
    ELIMINATED  <5%    Statistically indistinguishable from noise
    WEAK        5-15%  Possible contact layer, not substrate
    MODERATE    15-25% Possible genetic affiliation
    STRONG      >25%   Likely genetic relationship

Usage:
    python tools/falsification_system.py --classify luwian
    python tools/falsification_system.py --all --output data/falsification_report.json
    python tools/falsification_system.py --threshold-history
    python tools/falsification_system.py --test-significance luwian 30.3

Attribution:
    Part of Linear A Decipherment Project
    Implements explicit falsification criteria per METHODOLOGY.md
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
HYPOTHESIS_RESULTS_FILE = DATA_DIR / "hypothesis_results.json"
HISTORY_FILE = DATA_DIR / "threshold_history.json"


# ============================================================================
# FALSIFICATION THRESHOLDS
# ============================================================================

@dataclass
class ThresholdCategory:
    """Definition of a hypothesis classification category."""
    name: str
    min_pct: float
    max_pct: float
    interpretation: str
    action: str
    color: str  # For visualization


THRESHOLDS = {
    'ELIMINATED': ThresholdCategory(
        name='ELIMINATED',
        min_pct=0.0,
        max_pct=5.0,
        interpretation='Statistically indistinguishable from noise/chance matches',
        action='Hypothesis rejected; no further testing unless new evidence',
        color='red'
    ),
    'WEAK': ThresholdCategory(
        name='WEAK',
        min_pct=5.0,
        max_pct=15.0,
        interpretation='Possible contact layer (loanwords) but not substrate/genetic',
        action='Hypothesis retained as secondary; test for specific borrowing patterns',
        color='orange'
    ),
    'MODERATE': ThresholdCategory(
        name='MODERATE',
        min_pct=15.0,
        max_pct=25.0,
        interpretation='Possible genetic affiliation; warrants detailed investigation',
        action='Hypothesis prioritized; seek morphological/syntactic corroboration',
        color='yellow'
    ),
    'STRONG': ThresholdCategory(
        name='STRONG',
        min_pct=25.0,
        max_pct=100.0,
        interpretation='Likely genetic relationship or deep contact',
        action='Hypothesis primary focus; build comprehensive reading framework',
        color='green'
    ),
}

# Bayes factor interpretation (Kass & Raftery 1995)
BAYES_FACTOR_INTERPRETATION = {
    (0, 1): 'Negative (supports null)',
    (1, 3): 'Not worth more than a bare mention',
    (3, 20): 'Positive',
    (20, 150): 'Strong',
    (150, float('inf')): 'Very strong',
}


@dataclass
class ClassificationResult:
    """Result of classifying a hypothesis against thresholds."""
    hypothesis: str
    support_pct: float
    word_count: int
    total_words: int
    category: str
    interpretation: str
    action: str
    confidence_interval: Tuple[float, float]
    bayes_factor_vs_null: float
    bayes_interpretation: str
    threshold_crossed_from: Optional[str]
    notes: List[str]


@dataclass
class ThresholdCrossing:
    """Record of a hypothesis crossing a threshold."""
    hypothesis: str
    old_category: str
    new_category: str
    old_pct: float
    new_pct: float
    timestamp: str
    trigger: str


class FalsificationSystem:
    """
    Classifies hypotheses against explicit falsification thresholds.

    Provides:
    - Classification of current hypothesis scores
    - Confidence intervals for percentages
    - Bayes factor calculation vs null hypothesis
    - Tracking of threshold crossings over time
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.hypothesis_results = {}
        self.threshold_history = []

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_data(self) -> bool:
        """Load hypothesis testing results."""
        try:
            if HYPOTHESIS_RESULTS_FILE.exists():
                with open(HYPOTHESIS_RESULTS_FILE, 'r', encoding='utf-8') as f:
                    self.hypothesis_results = json.load(f)
                print(f"Loaded hypothesis results: {self.hypothesis_results.get('metadata', {}).get('words_tested', 0)} words")

            if HISTORY_FILE.exists():
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.threshold_history = json.load(f).get('crossings', [])

            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def save_history(self):
        """Save threshold crossing history."""
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'description': 'Historical record of hypothesis threshold crossings',
                        'last_updated': datetime.now().isoformat()
                    },
                    'crossings': self.threshold_history
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")

    def calculate_confidence_interval(self, successes: int, total: int,
                                      confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calculate Wilson score confidence interval for a proportion.

        More accurate than normal approximation for small samples.

        Args:
            successes: Number of words supporting hypothesis
            total: Total words tested
            confidence: Confidence level (default 95%)

        Returns:
            (lower_bound, upper_bound) as percentages
        """
        if total == 0:
            return (0.0, 100.0)

        from math import sqrt

        # Wilson score interval
        z = 1.96 if confidence == 0.95 else 2.576  # 95% or 99%
        p_hat = successes / total
        n = total

        denominator = 1 + z*z/n
        center = (p_hat + z*z/(2*n)) / denominator
        margin = (z / denominator) * sqrt((p_hat*(1-p_hat) + z*z/(4*n)) / n)

        lower = max(0, (center - margin) * 100)
        upper = min(100, (center + margin) * 100)

        return (round(lower, 2), round(upper, 2))

    def calculate_bayes_factor(self, successes: int, total: int,
                               null_rate: float = 0.05) -> float:
        """
        Calculate Bayes factor for hypothesis vs null (chance matches).

        Uses a simple binomial model where:
        - H0: Match rate = null_rate (e.g., 5% by chance)
        - H1: Match rate = observed rate

        Returns:
            Bayes factor (>1 supports hypothesis, <1 supports null)
        """
        if total == 0 or successes == 0:
            return 0.0

        observed_rate = successes / total

        # Simple likelihood ratio (approximation)
        # P(data|H1) / P(data|H0)
        try:
            # Binomial likelihood ratio
            from math import log, exp

            log_h1 = successes * log(observed_rate) + (total - successes) * log(1 - observed_rate)
            log_h0 = successes * log(null_rate) + (total - successes) * log(1 - null_rate)

            bayes_factor = exp(log_h1 - log_h0)

            # Cap to avoid infinity
            return min(bayes_factor, 10000.0)

        except (ValueError, ZeroDivisionError):
            return 1.0

    def interpret_bayes_factor(self, bf: float) -> str:
        """Interpret Bayes factor according to Kass & Raftery (1995)."""
        for (low, high), interpretation in BAYES_FACTOR_INTERPRETATION.items():
            if low <= bf < high:
                return interpretation
        return 'Very strong'

    def get_category(self, pct: float) -> str:
        """Get threshold category for a percentage."""
        for category, threshold in THRESHOLDS.items():
            if threshold.min_pct <= pct < threshold.max_pct:
                return category
        return 'STRONG' if pct >= 25 else 'ELIMINATED'

    def classify_hypothesis(self, hypothesis: str,
                           support_pct: Optional[float] = None,
                           word_count: Optional[int] = None,
                           total_words: Optional[int] = None) -> ClassificationResult:
        """
        Classify a hypothesis against falsification thresholds.

        Args:
            hypothesis: Hypothesis name (luwian, semitic, pregreek, protogreek)
            support_pct: Override support percentage (otherwise load from results)
            word_count: Override word count
            total_words: Override total words

        Returns:
            ClassificationResult with full analysis
        """
        # Get data from results or use overrides
        if support_pct is None or word_count is None:
            summaries = self.hypothesis_results.get('hypothesis_summaries', {})
            hyp_data = summaries.get(hypothesis, {})
            supported = hyp_data.get('supported', 0)
            total = sum(hyp_data.get(k, 0) for k in ['supported', 'neutral', 'contradicted'])

            if total == 0:
                total = self.hypothesis_results.get('metadata', {}).get('words_tested', 0)

            word_count = supported
            total_words = total
            support_pct = (supported / total * 100) if total > 0 else 0.0

        # Determine category
        category = self.get_category(support_pct)
        threshold = THRESHOLDS[category]

        # Calculate confidence interval
        ci = self.calculate_confidence_interval(word_count, total_words)

        # Calculate Bayes factor vs null (5% chance)
        bf = self.calculate_bayes_factor(word_count, total_words, null_rate=0.05)
        bf_interpretation = self.interpret_bayes_factor(bf)

        # Check for threshold crossings
        threshold_crossed_from = None
        for crossing in self.threshold_history:
            if crossing['hypothesis'] == hypothesis:
                if crossing['new_category'] == category and crossing['old_category'] != category:
                    threshold_crossed_from = crossing['old_category']
                    break

        # Generate notes
        notes = []
        if ci[0] < 5:
            notes.append("Lower CI bound below ELIMINATED threshold - hypothesis uncertain")
        if ci[1] > 25 and category in ['WEAK', 'MODERATE']:
            notes.append("Upper CI bound in STRONG range - more data could change classification")
        if bf < 1:
            notes.append("Bayes factor <1 suggests results could be chance")
        if word_count < 20:
            notes.append(f"Small sample size ({word_count} words) - interpret with caution")

        return ClassificationResult(
            hypothesis=hypothesis,
            support_pct=round(support_pct, 2),
            word_count=word_count,
            total_words=total_words,
            category=category,
            interpretation=threshold.interpretation,
            action=threshold.action,
            confidence_interval=ci,
            bayes_factor_vs_null=round(bf, 2),
            bayes_interpretation=bf_interpretation,
            threshold_crossed_from=threshold_crossed_from,
            notes=notes
        )

    def classify_all(self) -> Dict[str, ClassificationResult]:
        """Classify all hypotheses."""
        results = {}

        hypotheses = ['luwian', 'semitic', 'pregreek', 'protogreek']

        for hyp in hypotheses:
            results[hyp] = self.classify_hypothesis(hyp)

        return results

    def record_threshold_crossing(self, hypothesis: str, old_pct: float,
                                  new_pct: float, trigger: str):
        """Record a hypothesis crossing a threshold."""
        old_category = self.get_category(old_pct)
        new_category = self.get_category(new_pct)

        if old_category != new_category:
            crossing = ThresholdCrossing(
                hypothesis=hypothesis,
                old_category=old_category,
                new_category=new_category,
                old_pct=round(old_pct, 2),
                new_pct=round(new_pct, 2),
                timestamp=datetime.now().isoformat(),
                trigger=trigger
            )
            self.threshold_history.append(asdict(crossing))
            self.save_history()
            return crossing

        return None

    def test_significance(self, hypothesis: str, observed_pct: float,
                         sample_size: int = 198) -> Dict:
        """
        Test if observed support is significantly different from chance.

        Uses binomial test against null hypothesis of 5% chance matches.

        Args:
            hypothesis: Hypothesis name
            observed_pct: Observed support percentage
            sample_size: Number of words tested

        Returns:
            Significance analysis
        """
        null_rate = 0.05  # 5% chance matches
        observed_count = int(observed_pct / 100 * sample_size)

        # Calculate p-value (one-sided, greater than null)
        from math import comb, pow as mpow

        def binomial_pmf(k, n, p):
            return comb(n, k) * mpow(p, k) * mpow(1-p, n-k)

        # P(X >= observed | H0)
        p_value = sum(binomial_pmf(k, sample_size, null_rate)
                     for k in range(observed_count, sample_size + 1))

        significant = p_value < 0.05

        return {
            'hypothesis': hypothesis,
            'observed_pct': observed_pct,
            'observed_count': observed_count,
            'sample_size': sample_size,
            'null_rate': null_rate * 100,
            'p_value': round(p_value, 6),
            'significant_at_05': significant,
            'interpretation': 'Significantly above chance' if significant else 'Not significantly different from chance',
            'effect_size': round((observed_pct - null_rate * 100) / 100, 3)
        }

    def generate_report(self) -> Dict:
        """Generate full falsification report."""
        results = self.classify_all()

        # Sort by support percentage
        ranked = sorted(results.items(), key=lambda x: x[1].support_pct, reverse=True)

        report = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'method': 'Explicit Falsification Thresholds',
                'thresholds': {k: {'min': v.min_pct, 'max': v.max_pct, 'interpretation': v.interpretation}
                              for k, v in THRESHOLDS.items()},
                'total_words_tested': self.hypothesis_results.get('metadata', {}).get('words_tested', 0)
            },
            'classifications': {hyp: asdict(result) for hyp, result in results.items()},
            'ranking': [
                {
                    'rank': i + 1,
                    'hypothesis': hyp,
                    'support_pct': result.support_pct,
                    'category': result.category,
                    'ci_95': result.confidence_interval
                }
                for i, (hyp, result) in enumerate(ranked)
            ],
            'eliminated_hypotheses': [
                hyp for hyp, result in results.items()
                if result.category == 'ELIMINATED'
            ],
            'active_hypotheses': [
                hyp for hyp, result in results.items()
                if result.category != 'ELIMINATED'
            ],
            'threshold_history': self.threshold_history
        }

        return report

    def print_classification(self, result: ClassificationResult):
        """Print formatted classification result."""
        print(f"\n{result.hypothesis.upper()}")
        print("─" * 50)
        print(f"  Support: {result.support_pct}% ({result.word_count}/{result.total_words} words)")
        print(f"  95% CI:  [{result.confidence_interval[0]}%, {result.confidence_interval[1]}%]")
        print(f"  Category: {result.category}")
        print(f"  Interpretation: {result.interpretation}")
        print(f"  Action: {result.action}")
        print(f"  Bayes Factor: {result.bayes_factor_vs_null} ({result.bayes_interpretation})")

        if result.threshold_crossed_from:
            print(f"  ⚠ Crossed from {result.threshold_crossed_from}")

        if result.notes:
            print("  Notes:")
            for note in result.notes:
                print(f"    • {note}")

    def print_report(self, report: Dict):
        """Print formatted full report."""
        print("\n" + "=" * 70)
        print("FALSIFICATION THRESHOLD REPORT")
        print("=" * 70)

        print("\nTHRESHOLD DEFINITIONS:")
        for category, threshold in THRESHOLDS.items():
            print(f"  {category:12} {threshold.min_pct:>5.1f}% - {threshold.max_pct:>5.1f}%  {threshold.interpretation[:40]}...")

        print("\n" + "─" * 70)
        print("HYPOTHESIS RANKINGS")
        print("─" * 70)

        for item in report['ranking']:
            category = item['category']
            symbol = {'ELIMINATED': '✗', 'WEAK': '○', 'MODERATE': '◐', 'STRONG': '●'}[category]
            ci = item['ci_95']
            print(f"  {item['rank']}. {symbol} {item['hypothesis']:12} {item['support_pct']:5.1f}% [{category:10}] CI: [{ci[0]:.1f}%, {ci[1]:.1f}%]")

        print("\n" + "─" * 70)
        print("SUMMARY")
        print("─" * 70)

        eliminated = report['eliminated_hypotheses']
        active = report['active_hypotheses']

        if eliminated:
            print(f"\n  ELIMINATED ({len(eliminated)}): {', '.join(eliminated)}")

        if active:
            print(f"\n  ACTIVE ({len(active)}):")
            for hyp in active:
                result = report['classifications'][hyp]
                print(f"    • {hyp}: {result['category']} - {result['interpretation'][:50]}...")

        # Threshold history
        if report['threshold_history']:
            print("\n  Recent Threshold Crossings:")
            for crossing in report['threshold_history'][-5:]:
                print(f"    • {crossing['hypothesis']}: {crossing['old_category']} → {crossing['new_category']} ({crossing['timestamp'][:10]})")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Classify hypotheses against explicit falsification thresholds"
    )
    parser.add_argument(
        '--classify', '-c',
        type=str,
        metavar='HYPOTHESIS',
        help='Classify a specific hypothesis (luwian, semitic, pregreek, protogreek)'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Classify all hypotheses and generate report'
    )
    parser.add_argument(
        '--test-significance', '-t',
        nargs=2,
        metavar=('HYPOTHESIS', 'PCT'),
        help='Test if observed percentage is significantly above chance'
    )
    parser.add_argument(
        '--threshold-history',
        action='store_true',
        help='Show threshold crossing history'
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
    print("LINEAR A FALSIFICATION THRESHOLD SYSTEM")
    print("=" * 70)

    system = FalsificationSystem(verbose=args.verbose)
    if not system.load_data():
        print("Warning: No hypothesis results found. Using test mode.")

    if args.classify:
        result = system.classify_hypothesis(args.classify)
        system.print_classification(result)
        return 0

    if args.test_significance:
        hyp, pct = args.test_significance
        result = system.test_significance(hyp, float(pct))
        print(f"\nSignificance Test: {hyp}")
        print("─" * 50)
        for key, value in result.items():
            print(f"  {key}: {value}")
        return 0

    if args.threshold_history:
        if not system.threshold_history:
            print("\nNo threshold crossings recorded.")
        else:
            print("\nThreshold Crossing History:")
            for crossing in system.threshold_history:
                print(f"\n  {crossing['timestamp'][:10]}: {crossing['hypothesis']}")
                print(f"    {crossing['old_category']} ({crossing['old_pct']}%) → {crossing['new_category']} ({crossing['new_pct']}%)")
                print(f"    Trigger: {crossing['trigger']}")
        return 0

    if args.all or not any([args.classify, args.test_significance, args.threshold_history]):
        report = system.generate_report()
        system.print_report(report)

        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\nReport saved to: {output_path}")

        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
