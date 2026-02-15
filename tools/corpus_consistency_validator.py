#!/usr/bin/env python3
"""
Corpus Consistency Validator for Linear A

Automates First Principle #6 (Cross-Corpus Consistency):
"Every proposed reading must be tested across ALL occurrences in the corpus."

This tool validates that proposed readings work consistently across:
- All sites (HT, KH, ZA, PH, KN, etc.)
- All time periods (MMII, MMIII, LMI, LMIB)
- All scribal hands
- All contexts (administrative, religious, commodity)

Usage:
    python tools/corpus_consistency_validator.py --word KU-RO
    python tools/corpus_consistency_validator.py --word KU-RO --reading "total"
    python tools/corpus_consistency_validator.py --all --min-freq 5

Attribution:
    Part of Linear A Decipherment Project (OPERATION MINOS II)
"""

import json
import argparse
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from collections import Counter
from dataclasses import dataclass, asdict

from site_normalization import normalize_site


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
VALIDATION_RESULTS_FILE = DATA_DIR / "consistency_validation.json"


@dataclass
class Occurrence:
    """A single occurrence of a word in the corpus."""
    inscription_id: str
    site: str
    site_full: str
    site_raw: str
    period: str
    support: str
    position: int           # Position in inscription
    context_before: List[str]
    context_after: List[str]
    has_logogram: bool      # Is it followed by a logogram?
    has_number: bool        # Is it followed by a number?
    line_position: str      # start, middle, end, total_position


@dataclass
class ConsistencyReport:
    """Consistency validation results for a word."""
    word: str
    total_occurrences: int
    sites_found: List[str]
    sites_missing: List[str]
    periods_found: List[str]

    # Consistency metrics
    positional_consistency: float   # 0-1: how consistent is position?
    contextual_consistency: float   # 0-1: how consistent is context?
    functional_consistency: float   # 0-1: how consistent is function?

    # Breakdown
    position_distribution: Dict[str, int]
    context_distribution: Dict[str, int]
    site_distribution: Dict[str, int]

    # Issues detected
    anomalies: List[Dict]

    # Proposed reading validation
    reading_validated: bool
    reading_issues: List[str]

    generated: str


class CorpusConsistencyValidator:
    """
    Validates readings across the entire Linear A corpus.

    Implements First Principle #6: Cross-Corpus Consistency.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.corpus = None
        self.statistics = None
        self.major_sites = ['HT', 'KH', 'ZA', 'PH', 'KN', 'MA', 'TY', 'PK']
        self.site_name_map = {}

    def log(self, message: str):
        """Print if verbose mode."""
        if self.verbose:
            print(f"  {message}")

    def load_corpus(self) -> bool:
        """Load corpus data."""
        try:
            with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
                self.corpus = json.load(f)

            stats_file = DATA_DIR / "statistics.json"
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    self.statistics = json.load(f)
                    self.site_name_map = self.statistics.get('sites_full_names', {})

            self.log(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")
            return True
        except Exception as e:
            print(f"Error loading corpus: {e}")
            return False

    def find_occurrences(self, word: str) -> List[Occurrence]:
        """
        Find all occurrences of a word in the corpus.

        Returns detailed occurrence data including context.
        """
        word_upper = word.upper()
        occurrences = []

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            words = data.get('transliteratedWords', [])

            for i, w in enumerate(words):
                if not w:
                    continue

                # Match word (case-insensitive, handle subscripts)
                w_normalized = w.upper()
                if w_normalized == word_upper or w.upper() == word_upper:
                    # Extract context
                    context_before = [words[j] for j in range(max(0, i-3), i) if words[j]]
                    context_after = [words[j] for j in range(i+1, min(len(words), i+4)) if words[j]]

                    # Determine position characteristics
                    has_logogram = any(
                        re.match(r'^[A-Z]+$', w_after) and len(w_after) >= 2 and w_after not in ['VIR', 'MUL']
                        for w_after in context_after
                    )
                    has_number = any(
                        re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', w_after)
                        for w_after in context_after
                    )

                    # Determine line position
                    if i == 0:
                        line_pos = 'start'
                    elif i == len(words) - 1:
                        line_pos = 'end'
                    elif 'total' in str(context_before).lower() or has_number:
                        line_pos = 'total_position'
                    else:
                        line_pos = 'middle'

                    site_code, site_name = normalize_site(
                        site_value=data.get('site'),
                        inscription_id=insc_id,
                    )

                    occ = Occurrence(
                        inscription_id=insc_id,
                        site=site_code,
                        site_full=site_name,
                        site_raw=str(data.get('site', '') or ''),
                        period=data.get('context', 'UNKNOWN'),
                        support=data.get('support', 'UNKNOWN'),
                        position=i,
                        context_before=context_before,
                        context_after=context_after,
                        has_logogram=has_logogram,
                        has_number=has_number,
                        line_position=line_pos,
                    )
                    occurrences.append(occ)

        return occurrences

    def validate_word(self, word: str, proposed_reading: Optional[str] = None) -> ConsistencyReport:
        """
        Validate a word's consistency across the corpus.

        If a proposed_reading is provided, checks if the reading
        makes sense in all contexts where the word appears.
        """
        occurrences = self.find_occurrences(word)

        if not occurrences:
            return ConsistencyReport(
                word=word,
                total_occurrences=0,
                sites_found=[],
                sites_missing=self.major_sites,
                periods_found=[],
                positional_consistency=0.0,
                contextual_consistency=0.0,
                functional_consistency=0.0,
                position_distribution={},
                context_distribution={},
                site_distribution={},
                anomalies=[{'type': 'not_found', 'message': f'{word} not found in corpus'}],
                reading_validated=False,
                reading_issues=['Word not found in corpus'],
                generated=datetime.now().isoformat(),
            )

        # Analyze distributions
        sites_found = sorted(set(o.site for o in occurrences))
        sites_missing = [s for s in self.major_sites if s not in sites_found]
        periods_found = sorted(set(o.period for o in occurrences))

        # Position distribution
        position_dist = Counter(o.line_position for o in occurrences)

        # Context distribution (what follows the word)
        context_types = []
        for o in occurrences:
            if o.has_logogram and o.has_number:
                context_types.append('logogram+number')
            elif o.has_logogram:
                context_types.append('logogram')
            elif o.has_number:
                context_types.append('number')
            else:
                context_types.append('other')
        context_dist = Counter(context_types)

        # Site distribution
        site_dist = Counter(o.site for o in occurrences)

        # Calculate consistency metrics
        # Position consistency: high if word appears in same position most of the time
        most_common_pos = position_dist.most_common(1)[0][1] if position_dist else 0
        positional_consistency = most_common_pos / len(occurrences) if occurrences else 0

        # Context consistency: high if word appears in same context
        most_common_ctx = context_dist.most_common(1)[0][1] if context_dist else 0
        contextual_consistency = most_common_ctx / len(occurrences) if occurrences else 0

        # Functional consistency (combination of position + context)
        functional_consistency = (positional_consistency + contextual_consistency) / 2

        # Detect anomalies
        anomalies = []

        # Anomaly: appears at only one site when other sites have inscriptions
        if len(sites_found) == 1 and len(occurrences) > 5:
            concentration = len(occurrences) / len(self.corpus.get('inscriptions', {}))
            if concentration > 0.01:  # More than 1% of corpus
                anomalies.append({
                    'type': 'site_concentration',
                    'message': f'{word} appears at only {sites_found[0]} ({len(occurrences)} times)',
                    'severity': 'HIGH' if len(occurrences) > 20 else 'MEDIUM',
                    'implication': 'May be site-specific term or regional dialect',
                })

        # Anomaly: inconsistent contexts
        if len(context_dist) > 2 and max(context_dist.values()) < len(occurrences) * 0.5:
            anomalies.append({
                'type': 'context_inconsistency',
                'message': f'{word} appears in varied contexts: {dict(context_dist)}',
                'severity': 'MEDIUM',
                'implication': 'May have multiple functions or be a common word',
            })

        # Anomaly: appears with and without numbers
        if 'number' in context_dist and 'other' in context_dist:
            num_pct = context_dist.get('number', 0) / len(occurrences)
            if 0.2 < num_pct < 0.8:
                anomalies.append({
                    'type': 'mixed_numerical_context',
                    'message': f'{word} followed by number {num_pct*100:.1f}% of time',
                    'severity': 'LOW',
                    'implication': 'May have both administrative and non-administrative uses',
                })

        # Validate proposed reading
        reading_validated = True
        reading_issues = []

        if proposed_reading:
            reading_lower = proposed_reading.lower()

            # Total/sum reading should appear at totaling positions
            if 'total' in reading_lower or 'sum' in reading_lower or 'all' in reading_lower:
                total_positions = position_dist.get('total_position', 0) + position_dist.get('end', 0)
                if total_positions < len(occurrences) * 0.5:
                    reading_issues.append(
                        f"Reading '{proposed_reading}' expects totaling position, but "
                        f"only {total_positions}/{len(occurrences)} occurrences are at end/total position"
                    )
                    reading_validated = False

            # Deficit reading should have special marking or context
            if 'deficit' in reading_lower or 'lacking' in reading_lower:
                # Check if it co-occurs with KU-RO or similar
                has_kuro = any('KU-RO' in str(o.context_before + o.context_after).upper()
                               for o in occurrences)
                if not has_kuro and len(occurrences) > 3:
                    reading_issues.append(
                        f"Reading '{proposed_reading}' might expect co-occurrence with total term, "
                        f"but KU-RO not commonly found in context"
                    )

            # If reading implies commodity, should appear with logograms
            commodity_terms = ['wine', 'oil', 'grain', 'olive', 'fig']
            if any(term in reading_lower for term in commodity_terms):
                log_pct = (context_dist.get('logogram', 0) + context_dist.get('logogram+number', 0)) / len(occurrences)
                if log_pct < 0.3:
                    reading_issues.append(
                        f"Reading '{proposed_reading}' implies commodity, but only "
                        f"{log_pct*100:.1f}% of occurrences are followed by logograms"
                    )

        return ConsistencyReport(
            word=word,
            total_occurrences=len(occurrences),
            sites_found=sites_found,
            sites_missing=sites_missing,
            periods_found=periods_found,
            positional_consistency=positional_consistency,
            contextual_consistency=contextual_consistency,
            functional_consistency=functional_consistency,
            position_distribution=dict(position_dist),
            context_distribution=dict(context_dist),
            site_distribution=dict(site_dist),
            anomalies=anomalies,
            reading_validated=reading_validated,
            reading_issues=reading_issues,
            generated=datetime.now().isoformat(),
        )

    def validate_multiple_words(self, min_frequency: int = 5) -> Dict[str, ConsistencyReport]:
        """Validate all words above frequency threshold."""
        results = {}

        # Get word frequencies from statistics
        word_freqs = self.statistics.get('top_words', {}) if self.statistics else {}

        words_to_check = [w for w, f in word_freqs.items()
                         if f >= min_frequency and '-' in w]  # Only syllabic words

        self.log(f"Validating {len(words_to_check)} words with frequency >= {min_frequency}")

        for word in words_to_check:
            report = self.validate_word(word)
            results[word] = report

            if report.anomalies:
                self.log(f"{word}: {len(report.anomalies)} anomalies detected")

        return results

    def save_results(self, results: Dict[str, ConsistencyReport], output_path: Path = None):
        """Save validation results to JSON."""
        if output_path is None:
            output_path = VALIDATION_RESULTS_FILE

        data = {
            'generated': datetime.now().isoformat(),
            'total_words_validated': len(results),
            'words': {word: asdict(report) for word, report in results.items()},
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Results saved to: {output_path}")

    def print_report(self, report: ConsistencyReport):
        """Print a single validation report."""
        print("\n" + "=" * 70)
        print(f"CONSISTENCY VALIDATION: {report.word}")
        print("=" * 70)

        print(f"\nTotal occurrences: {report.total_occurrences}")
        print(f"Sites found: {', '.join(report.sites_found)}")
        if report.sites_missing:
            print(f"Sites missing: {', '.join(report.sites_missing)}")
        print(f"Periods: {', '.join(report.periods_found)}")

        print("\nConsistency Metrics:")
        print(f"  Positional: {report.positional_consistency:.1%}")
        print(f"  Contextual: {report.contextual_consistency:.1%}")
        print(f"  Functional: {report.functional_consistency:.1%}")

        print("\nPosition Distribution:")
        for pos, count in sorted(report.position_distribution.items(), key=lambda x: -x[1]):
            pct = count / report.total_occurrences * 100
            print(f"  {pos}: {count} ({pct:.1f}%)")

        print("\nContext Distribution:")
        for ctx, count in sorted(report.context_distribution.items(), key=lambda x: -x[1]):
            pct = count / report.total_occurrences * 100
            print(f"  {ctx}: {count} ({pct:.1f}%)")

        print("\nSite Distribution:")
        for site, count in sorted(report.site_distribution.items(), key=lambda x: -x[1]):
            pct = count / report.total_occurrences * 100
            print(f"  {site}: {count} ({pct:.1f}%)")

        if report.anomalies:
            print(f"\n⚠️  ANOMALIES DETECTED ({len(report.anomalies)}):")
            for a in report.anomalies:
                print(f"  [{a['severity']}] {a['type']}: {a['message']}")
                print(f"       → {a['implication']}")

        if report.reading_issues:
            print("\n⚠️  READING VALIDATION ISSUES:")
            for issue in report.reading_issues:
                print(f"  • {issue}")
        elif report.reading_validated:
            print("\n✓ Reading validation: PASSED")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Linear A readings across the entire corpus"
    )
    parser.add_argument(
        '--word', '-w',
        type=str,
        help='Validate a specific word'
    )
    parser.add_argument(
        '--reading', '-r',
        type=str,
        help='Proposed reading to validate (e.g., "total", "deficit")'
    )
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Validate all frequent words'
    )
    parser.add_argument(
        '--min-freq', '-m',
        type=int,
        default=5,
        help='Minimum frequency for --all mode (default: 5)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for results'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("LINEAR A CORPUS CONSISTENCY VALIDATOR")
    print("=" * 60)
    print("Enforcing First Principle #6: Cross-Corpus Consistency\n")

    validator = CorpusConsistencyValidator(verbose=args.verbose)

    if not validator.load_corpus():
        return 1

    if args.word:
        report = validator.validate_word(args.word, args.reading)
        validator.print_report(report)

        if args.output:
            validator.save_results({args.word: report}, Path(args.output))

    elif args.all:
        results = validator.validate_multiple_words(min_frequency=args.min_freq)

        # Print summary
        print(f"\nValidated {len(results)} words")

        # Find most concentrated words
        concentrated = [(w, r) for w, r in results.items()
                       if any(a['type'] == 'site_concentration' for a in r.anomalies)]
        if concentrated:
            print(f"\nSite-concentrated words ({len(concentrated)}):")
            for word, report in sorted(concentrated, key=lambda x: -x[1].total_occurrences)[:10]:
                sites = ', '.join(report.sites_found)
                print(f"  {word}: {report.total_occurrences} occurrences at {sites}")

        # Find words with reading issues
        inconsistent = [(w, r) for w, r in results.items() if r.functional_consistency < 0.5]
        if inconsistent:
            print(f"\nLow consistency words ({len(inconsistent)}):")
            for word, report in sorted(inconsistent, key=lambda x: x[1].functional_consistency)[:10]:
                print(f"  {word}: consistency={report.functional_consistency:.1%}")

        # Save all results
        output_path = Path(args.output) if args.output else None
        validator.save_results(results, output_path)

    else:
        print("Usage:")
        print("  --word WORD     Validate a specific word")
        print("  --all           Validate all frequent words")
        print("  --reading TEXT  Proposed reading to validate")
        print("\nExamples:")
        print('  python corpus_consistency_validator.py --word KU-RO --reading "total"')
        print("  python corpus_consistency_validator.py --all --min-freq 10")

    return 0


if __name__ == '__main__':
    sys.exit(main())
