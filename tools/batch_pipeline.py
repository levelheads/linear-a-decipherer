#!/usr/bin/env python3
"""
Linear A Batch Processing Pipeline

Enables systematic analysis of the entire corpus by chaining tools together.
This addresses the critical gap: only 0.81% of corpus analyzed.

Pipeline stages:
1. DISCOVER: Extract all words meeting frequency threshold
2. HYPOTHESIZE: Test each word against four linguistic hypotheses
3. VALIDATE: Check corpus-wide consistency
4. SYNTHESIZE: Aggregate findings and update knowledge base

Usage:
    python tools/batch_pipeline.py --full              # Full pipeline on entire corpus
    python tools/batch_pipeline.py --stage discover    # Run single stage
    python tools/batch_pipeline.py --site HT           # Filter by site
    python tools/batch_pipeline.py --min-freq 5        # Minimum frequency threshold
    python tools/batch_pipeline.py --resume            # Resume from last checkpoint

First Principles Compliance:
    - P1 (Kober): Patterns analyzed before language assumption
    - P4 (Multi-Hypothesis): All four hypotheses tested automatically
    - P6 (Cross-Corpus): Every reading verified corpus-wide

Attribution:
    Part of Linear A Decipherment Project
    Designed to scale analysis from 0.81% to comprehensive corpus coverage
"""

import json
import argparse
import sys
import re
import os
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
import subprocess


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
TOOLS_DIR = PROJECT_ROOT / "tools"
ANALYSIS_DIR = PROJECT_ROOT / "analysis"
CHECKPOINT_DIR = DATA_DIR / "pipeline_checkpoints"


class BatchPipeline:
    """
    Orchestrates multi-stage corpus analysis pipeline.

    Maintains checkpoints for resumption and generates
    comprehensive analysis reports.
    """

    def __init__(self, verbose=False, dry_run=False):
        self.verbose = verbose
        self.dry_run = dry_run
        self.corpus = None
        self.checkpoint = {}

        # Pipeline state
        self.words_discovered = {}
        self.hypotheses_tested = {}
        self.validations = {}
        self.synthesis = {}

        # Statistics
        self.stats = {
            'inscriptions_total': 0,
            'inscriptions_processed': 0,
            'words_total': 0,
            'words_analyzed': 0,
            'high_confidence_findings': 0,
            'coverage_percent': 0.0,
        }

        # Ensure checkpoint directory exists
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    def log(self, message: str, level: str = 'INFO'):
        """Print message with timestamp if verbose mode enabled."""
        if self.verbose or level in ['ERROR', 'WARNING']:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] [{level}] {message}")

    def load_corpus(self, site_filter: Optional[str] = None) -> bool:
        """Load corpus data with optional site filtering."""
        try:
            corpus_path = DATA_DIR / "corpus.json"
            with open(corpus_path, 'r', encoding='utf-8') as f:
                full_corpus = json.load(f)

            # Apply site filter if specified
            if site_filter:
                filtered = {}
                for insc_id, data in full_corpus.get('inscriptions', {}).items():
                    if insc_id.startswith(site_filter):
                        filtered[insc_id] = data
                self.corpus = {'inscriptions': filtered, 'attribution': full_corpus.get('attribution', {})}
                self.log(f"Loaded {len(filtered)} inscriptions from site {site_filter}")
            else:
                self.corpus = full_corpus
                self.log(f"Loaded {len(full_corpus.get('inscriptions', {}))} inscriptions")

            self.stats['inscriptions_total'] = len(self.corpus.get('inscriptions', {}))
            return True

        except Exception as e:
            self.log(f"Error loading corpus: {e}", 'ERROR')
            return False

    def save_checkpoint(self, stage: str):
        """Save pipeline state for resumption."""
        checkpoint_path = CHECKPOINT_DIR / f"checkpoint_{stage}.json"

        checkpoint = {
            'stage': stage,
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'words_discovered': self.words_discovered,
            'hypotheses_tested': self.hypotheses_tested,  # Full data for proper resume
            'validations': self.validations,  # Required for synthesize stage
            'progress': {
                'total_words': len(self.words_discovered),
                'tested_words': len(self.hypotheses_tested),
                'validated_words': len(self.validations),
            }
        }

        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, ensure_ascii=False, indent=2)

        self.log(f"Checkpoint saved: {checkpoint_path}")

    def load_checkpoint(self, stage: str) -> bool:
        """Load checkpoint to resume pipeline."""
        checkpoint_path = CHECKPOINT_DIR / f"checkpoint_{stage}.json"

        if not checkpoint_path.exists():
            return False

        try:
            with open(checkpoint_path, 'r', encoding='utf-8') as f:
                self.checkpoint = json.load(f)
            self.stats = self.checkpoint.get('stats', self.stats)
            self.words_discovered = self.checkpoint.get('words_discovered', {})
            self.hypotheses_tested = self.checkpoint.get('hypotheses_tested', {})
            self.validations = self.checkpoint.get('validations', {})
            self.log(f"Resumed from checkpoint: {stage}")
            self.log(f"  Words discovered: {len(self.words_discovered)}")
            self.log(f"  Hypotheses tested: {len(self.hypotheses_tested)}")
            self.log(f"  Validations: {len(self.validations)}")
            return True
        except Exception as e:
            self.log(f"Could not load checkpoint: {e}", 'WARNING')
            return False

    # =========================================================================
    # STAGE 1: DISCOVER - Extract words from corpus
    # =========================================================================

    def stage_discover(self, min_frequency: int = 2) -> dict:
        """
        Extract all words from corpus with frequency counts.

        Returns:
            Dictionary of words with frequency, sites, positions
        """
        self.log("=" * 50)
        self.log("STAGE 1: DISCOVER - Extracting words from corpus")
        self.log("=" * 50)

        if self.dry_run:
            self.log("DRY RUN: Would extract words from corpus")
            return {}

        word_data = defaultdict(lambda: {
            'frequency': 0,
            'sites': set(),
            'inscriptions': [],
            'positions': defaultdict(int),  # initial/medial/final
            'contexts': [],  # Sample contexts
        })

        processed = 0
        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            site = self._extract_site_code(insc_id)
            words = data.get('transliteratedWords', [])

            for idx, word in enumerate(words):
                if not self._is_valid_word(word):
                    continue

                word_upper = word.upper()
                word_data[word_upper]['frequency'] += 1
                word_data[word_upper]['sites'].add(site)

                # Track position (simplified)
                if idx == 0 or (idx > 0 and words[idx-1] == '\n'):
                    word_data[word_upper]['positions']['initial'] += 1
                elif idx == len(words) - 1 or (idx < len(words) - 1 and words[idx+1] == '\n'):
                    word_data[word_upper]['positions']['final'] += 1
                else:
                    word_data[word_upper]['positions']['medial'] += 1

                # Store sample inscriptions (max 10)
                if len(word_data[word_upper]['inscriptions']) < 10:
                    word_data[word_upper]['inscriptions'].append(insc_id)

            processed += 1

        # Convert sets to lists for JSON serialization
        self.words_discovered = {}
        for word, data in word_data.items():
            if data['frequency'] >= min_frequency:
                self.words_discovered[word] = {
                    'frequency': data['frequency'],
                    'sites': list(data['sites']),
                    'inscriptions': data['inscriptions'],
                    'positions': dict(data['positions']),
                    'site_count': len(data['sites']),
                }

        self.stats['inscriptions_processed'] = processed
        self.stats['words_total'] = len(word_data)
        self.stats['words_above_threshold'] = len(self.words_discovered)

        # Count logograms for transparency (these are in word_data but excluded from words_discovered)
        logogram_count = sum(1 for w in word_data if self._is_logogram(w))
        single_syllable_count = sum(1 for w in word_data
                                     if re.match(r'^[A-Z*\d\[\]]+$', w) and '-' not in w and not self._is_logogram(w))

        self.log(f"Discovered {len(self.words_discovered)} words with freq >= {min_frequency}")
        self.log(f"Total unique words: {len(word_data)}")
        self.log(f"Inscriptions processed: {processed}")
        self.log(f"Logograms excluded from hypothesis testing: {logogram_count}")
        self.log(f"Single-syllables excluded (insufficient data): {single_syllable_count}")

        self.save_checkpoint('discover')
        return self.words_discovered

    def _extract_site_code(self, inscription_id: str) -> str:
        """Extract site code from inscription ID."""
        match = re.match(r'^([A-Z]+)', inscription_id)
        return match.group(1) if match else 'UNKNOWN'

    # Commodity logograms (not linguistic data - represent concepts, not sounds)
    COMMODITY_LOGOGRAMS = {
        'GRA', 'VIN', 'OLE', 'OLIV', 'FIC', 'FAR', 'CYP',
        'OVI', 'CAP', 'SUS', 'BOS', 'VIR', 'MUL', 'TELA'
    }

    def _is_valid_word(self, word: str) -> bool:
        """Check if word is valid for hypothesis analysis.

        Filters out:
        - Punctuation and empty strings
        - Pure numerals and fractions
        - Pure logograms (uppercase-only without hyphens: OLIV, GRA, VIN)
        - Single-syllables without hyphens (KU, KA, SI) - too short to discriminate
        - Damaged/uncertain markers (𐝫)

        Keeps:
        - Multi-syllable words with hyphens (KU-RO, SA-RA₂)
        - Ligatures with phonetic complements (OLE+KI)
        """
        if not word or word in ['\n', '|', '—', '𐄁', '']:
            return False

        # Skip numerals
        if re.match(r'^[\d\s.¹²³⁴⁵⁶⁷⁸⁹⁰/₀₁₂₃₄₅₆₇₈○◎—|]+$', word):
            return False

        # Skip pure logograms (uppercase-only without hyphens)
        # This matches: OLIV, GRA, VIN, KU, KA, SI, etc.
        # But keeps: KU-RO, OLE+KI (has special chars)
        if re.match(r'^[A-Z*\d\[\]]+$', word) and '-' not in word:
            return False

        # Skip damaged/uncertain markers
        if word.startswith('𐝫'):
            return False

        return True

    def _is_logogram(self, word: str) -> bool:
        """Check if word is a commodity logogram."""
        base = word.split('+')[0] if '+' in word else word
        return base.upper() in self.COMMODITY_LOGOGRAMS

    def calculate_corpus_coverage(self) -> dict:
        """
        Calculate corpus coverage statistics by site, frequency tier, and overall.

        Returns:
            Dictionary with coverage metrics and recommendations for next analysis.
        """
        if not self.corpus:
            return {'error': 'Corpus not loaded'}

        # Count inscriptions and words by site
        site_stats = defaultdict(lambda: {
            'inscriptions': 0,
            'words': 0,
            'unique_words': set(),
            'has_kuro': 0,
        })

        total_inscriptions = 0
        total_words = 0
        kuro_tablets = 0

        for insc_id, data in self.corpus.get('inscriptions', {}).items():
            if '_parse_error' in data:
                continue

            site = self._extract_site_code(insc_id)
            site_stats[site]['inscriptions'] += 1
            total_inscriptions += 1

            words = data.get('transliteratedWords', [])
            valid_words = [w for w in words if self._is_valid_word(w)]
            site_stats[site]['words'] += len(valid_words)
            site_stats[site]['unique_words'].update(w.upper() for w in valid_words)
            total_words += len(valid_words)

            if 'KU-RO' in words:
                site_stats[site]['has_kuro'] += 1
                kuro_tablets += 1

        # Calculate analyzed coverage
        analyzed_words = len(self.hypotheses_tested) if self.hypotheses_tested else 0

        # Build coverage report
        coverage = {
            'total_inscriptions': total_inscriptions,
            'total_words': total_words,
            'words_analyzed': analyzed_words,
            'overall_coverage_percent': round(analyzed_words / total_words * 100, 2) if total_words > 0 else 0,
            'kuro_tablets': kuro_tablets,
            'by_site': {},
            'recommendations': [],
        }

        # Per-site statistics
        for site, stats in sorted(site_stats.items(), key=lambda x: -x[1]['inscriptions']):
            unique_count = len(stats['unique_words'])
            # Estimate analyzed (intersection with hypotheses_tested)
            analyzed_at_site = sum(1 for w in stats['unique_words']
                                   if w in (self.hypotheses_tested or {}))

            coverage['by_site'][site] = {
                'inscriptions': stats['inscriptions'],
                'words': stats['words'],
                'unique_words': unique_count,
                'analyzed': analyzed_at_site,
                'coverage_percent': round(analyzed_at_site / unique_count * 100, 2) if unique_count > 0 else 0,
                'kuro_tablets': stats['has_kuro'],
            }

        # Generate recommendations (priority sites with low coverage)
        priority_sites = []
        for site, stats in coverage['by_site'].items():
            if stats['inscriptions'] >= 10 and stats['coverage_percent'] < 50:
                priority_sites.append({
                    'site': site,
                    'inscriptions': stats['inscriptions'],
                    'coverage': stats['coverage_percent'],
                    'reason': 'Low coverage, significant corpus'
                })

        priority_sites.sort(key=lambda x: (-x['inscriptions'], x['coverage']))

        coverage['recommendations'] = [
            f"Priority: {s['site']} ({s['inscriptions']} inscriptions, {s['coverage']}% coverage)"
            for s in priority_sites[:5]
        ]

        if not coverage['recommendations']:
            coverage['recommendations'] = ['All major sites have adequate coverage']

        return coverage

    # =========================================================================
    # STAGE 2: HYPOTHESIZE - Test against four hypotheses
    # =========================================================================

    def stage_hypothesize(self, max_words: Optional[int] = None) -> dict:
        """
        Test each discovered word against all four linguistic hypotheses.

        Uses hypothesis_tester.py for each word.
        """
        self.log("=" * 50)
        self.log("STAGE 2: HYPOTHESIZE - Testing against four hypotheses")
        self.log("=" * 50)

        if self.dry_run:
            self.log("DRY RUN: Would test words against hypotheses")
            return {}

        if not self.words_discovered:
            self.log("No words discovered. Run stage_discover first.", 'ERROR')
            return {}

        # Import hypothesis tester inline to avoid circular imports
        sys.path.insert(0, str(TOOLS_DIR))
        try:
            from hypothesis_tester import HypothesisTester
        except ImportError as e:
            self.log(f"Could not import hypothesis_tester: {e}", 'ERROR')
            return {}

        tester = HypothesisTester(verbose=False)

        # Sort by frequency (most frequent first)
        words_sorted = sorted(
            self.words_discovered.items(),
            key=lambda x: -x[1]['frequency']
        )

        if max_words:
            words_sorted = words_sorted[:max_words]

        total = len(words_sorted)
        self.log(f"Testing {total} words...")

        for idx, (word, data) in enumerate(words_sorted):
            if (idx + 1) % 50 == 0:
                self.log(f"Progress: {idx + 1}/{total} words tested")

            try:
                result = tester.test_word(word, frequency=data['frequency'])
                self.hypotheses_tested[word] = {
                    'word': word,
                    'frequency': data['frequency'],
                    'sites': data['sites'],
                    'best_hypothesis': result['synthesis']['best_hypothesis'],
                    'best_score': result['synthesis']['best_score'],
                    'max_confidence': result['synthesis']['max_confidence'],
                    'multi_hypothesis_support': result['synthesis']['multi_hypothesis_support'],
                    'supported_hypotheses': result['synthesis']['supported_hypotheses'],
                    'hypothesis_scores': {
                        h: result['hypotheses'][h]['score']
                        for h in result['hypotheses']
                    },
                }
            except Exception as e:
                self.log(f"Error testing {word}: {e}", 'WARNING')

        self.stats['words_analyzed'] = len(self.hypotheses_tested)
        self.stats['coverage_percent'] = (
            len(self.hypotheses_tested) / len(self.words_discovered) * 100
            if self.words_discovered else 0
        )

        # Count high-confidence findings
        high_conf = sum(1 for w, d in self.hypotheses_tested.items()
                        if d['max_confidence'] in ['CERTAIN', 'PROBABLE', 'HIGH'])
        self.stats['high_confidence_findings'] = high_conf

        self.log(f"Hypothesis testing complete: {len(self.hypotheses_tested)} words")
        self.log(f"High-confidence findings: {high_conf}")

        self.save_checkpoint('hypothesize')
        return self.hypotheses_tested

    # =========================================================================
    # STAGE 3: VALIDATE - Cross-corpus consistency check
    # =========================================================================

    def stage_validate(self) -> dict:
        """
        Validate findings for cross-corpus consistency (First Principle #6).

        Checks:
        - Does reading work across all sites?
        - Are there contradicting occurrences?
        - Is the pattern consistent?
        """
        self.log("=" * 50)
        self.log("STAGE 3: VALIDATE - Cross-corpus consistency")
        self.log("=" * 50)

        if self.dry_run:
            self.log("DRY RUN: Would validate corpus consistency")
            return {}

        if not self.hypotheses_tested:
            self.log("No hypotheses tested. Run stage_hypothesize first.", 'ERROR')
            return {}

        validations = {}

        for word, data in self.hypotheses_tested.items():
            sites = data.get('sites', [])
            freq = data.get('frequency', 0)

            # Cross-site consistency
            site_count = len(sites)
            is_cross_site = site_count > 1

            # Position consistency (from discover stage)
            word_data = self.words_discovered.get(word, {})
            positions = word_data.get('positions', {})

            # Determine dominant position
            if positions:
                dominant_pos = max(positions.items(), key=lambda x: x[1])
                position_consistency = dominant_pos[1] / sum(positions.values())
            else:
                dominant_pos = ('unknown', 0)
                position_consistency = 0

            # Validation verdict
            if is_cross_site and position_consistency > 0.7:
                verdict = 'CONSISTENT'
            elif is_cross_site or position_consistency > 0.7:
                verdict = 'PARTIAL'
            else:
                verdict = 'WEAK'

            validations[word] = {
                'word': word,
                'frequency': freq,
                'site_count': site_count,
                'sites': sites,
                'cross_site': is_cross_site,
                'dominant_position': dominant_pos[0],
                'position_consistency': round(position_consistency, 2),
                'verdict': verdict,
                'best_hypothesis': data.get('best_hypothesis'),
                'max_confidence': data.get('max_confidence'),
            }

        self.validations = validations

        # Statistics
        consistent = sum(1 for v in validations.values() if v['verdict'] == 'CONSISTENT')
        partial = sum(1 for v in validations.values() if v['verdict'] == 'PARTIAL')
        weak = sum(1 for v in validations.values() if v['verdict'] == 'WEAK')

        self.log(f"Validation complete:")
        self.log(f"  CONSISTENT: {consistent}")
        self.log(f"  PARTIAL: {partial}")
        self.log(f"  WEAK: {weak}")

        self.save_checkpoint('validate')
        return validations

    # =========================================================================
    # STAGE 4: SYNTHESIZE - Aggregate findings
    # =========================================================================

    def stage_synthesize(self) -> dict:
        """
        Synthesize findings into actionable knowledge base updates.

        Generates:
        - Ranked word list by confidence
        - Hypothesis support summary
        - Recommendations for KNOWLEDGE.md updates
        - Flagged items requiring manual review
        """
        self.log("=" * 50)
        self.log("STAGE 4: SYNTHESIZE - Aggregating findings")
        self.log("=" * 50)

        if self.dry_run:
            self.log("DRY RUN: Would synthesize findings")
            return {}

        if not self.validations:
            self.log("No validations available. Run stage_validate first.", 'ERROR')
            return {}

        # Hypothesis support aggregation
        hypothesis_support = {
            'luwian': {'total_score': 0, 'word_count': 0, 'best_words': []},
            'semitic': {'total_score': 0, 'word_count': 0, 'best_words': []},
            'pregreek': {'total_score': 0, 'word_count': 0, 'best_words': []},
            'protogreek': {'total_score': 0, 'word_count': 0, 'best_words': []},
        }

        # Categorize findings
        high_confidence = []
        medium_confidence = []
        needs_review = []

        for word, validation in self.validations.items():
            hyp_data = self.hypotheses_tested.get(word, {})
            scores = hyp_data.get('hypothesis_scores', {})

            # Aggregate hypothesis scores
            for hyp, score in scores.items():
                if hyp in hypothesis_support:
                    hypothesis_support[hyp]['total_score'] += score
                    if score > 1.5:
                        hypothesis_support[hyp]['word_count'] += 1

            # Categorize by confidence
            confidence = validation.get('max_confidence', 'SPECULATIVE')
            verdict = validation.get('verdict', 'WEAK')

            entry = {
                'word': word,
                'frequency': validation.get('frequency', 0),
                'best_hypothesis': validation.get('best_hypothesis'),
                'confidence': confidence,
                'consistency': verdict,
                'sites': validation.get('sites', []),
            }

            if confidence in ['CERTAIN', 'PROBABLE'] and verdict == 'CONSISTENT':
                high_confidence.append(entry)
            elif confidence in ['PROBABLE', 'POSSIBLE'] or verdict == 'PARTIAL':
                medium_confidence.append(entry)
            else:
                needs_review.append(entry)

        # Sort by frequency
        high_confidence.sort(key=lambda x: -x['frequency'])
        medium_confidence.sort(key=lambda x: -x['frequency'])
        needs_review.sort(key=lambda x: -x['frequency'])

        # Calculate hypothesis rankings
        hypothesis_rankings = sorted(
            hypothesis_support.items(),
            key=lambda x: -x[1]['total_score']
        )

        self.synthesis = {
            'generated': datetime.now().isoformat(),
            'pipeline_stats': self.stats,
            'summary': {
                'total_words_analyzed': len(self.validations),
                'high_confidence': len(high_confidence),
                'medium_confidence': len(medium_confidence),
                'needs_review': len(needs_review),
            },
            'hypothesis_rankings': {
                hyp: {
                    'rank': idx + 1,
                    'total_score': round(data['total_score'], 2),
                    'words_supporting': data['word_count'],
                }
                for idx, (hyp, data) in enumerate(hypothesis_rankings)
            },
            'high_confidence_findings': high_confidence[:50],  # Top 50
            'medium_confidence_findings': medium_confidence[:50],
            'needs_review': needs_review[:30],
            'recommendations': self._generate_recommendations(high_confidence),
        }

        self.log(f"\nSynthesis complete:")
        self.log(f"  High confidence: {len(high_confidence)}")
        self.log(f"  Medium confidence: {len(medium_confidence)}")
        self.log(f"  Needs review: {len(needs_review)}")
        self.log(f"\nHypothesis rankings:")
        for hyp, data in hypothesis_rankings:
            self.log(f"  {hyp.upper()}: score={data['total_score']:.1f}, words={data['word_count']}")

        return self.synthesis

    def _generate_recommendations(self, high_confidence: List[dict]) -> List[str]:
        """Generate recommendations for knowledge base updates."""
        recommendations = []

        if high_confidence:
            recommendations.append(
                f"Consider adding {len(high_confidence)} high-confidence readings to KNOWLEDGE.md"
            )

            # Group by hypothesis
            by_hyp = defaultdict(list)
            for item in high_confidence[:20]:
                by_hyp[item['best_hypothesis']].append(item['word'])

            for hyp, words in by_hyp.items():
                if words:
                    recommendations.append(
                        f"{hyp.upper()} hypothesis supported by: {', '.join(words[:5])}..."
                    )

        return recommendations

    # =========================================================================
    # MAIN PIPELINE RUNNER
    # =========================================================================

    def run_full_pipeline(
        self,
        min_frequency: int = 2,
        max_words: Optional[int] = None,
        site_filter: Optional[str] = None,
        resume: bool = False
    ) -> dict:
        """
        Run complete analysis pipeline.

        Args:
            min_frequency: Minimum word frequency to analyze
            max_words: Maximum words to test (None = all)
            site_filter: Filter to specific site (e.g., 'HT')
            resume: Resume from last checkpoint

        Returns:
            Complete synthesis results
        """
        self.log("=" * 60)
        self.log("LINEAR A BATCH PROCESSING PIPELINE")
        self.log("=" * 60)
        self.log(f"Min frequency: {min_frequency}")
        self.log(f"Max words: {max_words or 'ALL'}")
        self.log(f"Site filter: {site_filter or 'ALL'}")
        self.log("")

        # Load corpus
        if not self.load_corpus(site_filter):
            return {'error': 'Failed to load corpus'}

        # Stage 1: Discover
        if resume and self.load_checkpoint('discover'):
            self.log("Resumed discovery from checkpoint")
        else:
            self.stage_discover(min_frequency)

        # Stage 2: Hypothesize
        if resume and self.load_checkpoint('hypothesize'):
            self.log("Resumed hypothesis testing from checkpoint")
        else:
            self.stage_hypothesize(max_words)

        # Stage 3: Validate
        self.stage_validate()

        # Stage 4: Synthesize
        self.stage_synthesize()

        # Save final results
        output_path = DATA_DIR / "batch_analysis_results.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.synthesis, f, ensure_ascii=False, indent=2)

        self.log("")
        self.log("=" * 60)
        self.log(f"Pipeline complete. Results saved to: {output_path}")
        self.log("=" * 60)

        # Print summary
        self.print_summary()

        return self.synthesis

    def print_summary(self):
        """Print human-readable summary of pipeline results."""
        if not self.synthesis:
            return

        print("\n" + "=" * 60)
        print("BATCH ANALYSIS SUMMARY")
        print("=" * 60)

        summary = self.synthesis.get('summary', {})
        print(f"\nWords Analyzed: {summary.get('total_words_analyzed', 0)}")
        print(f"  High Confidence: {summary.get('high_confidence', 0)}")
        print(f"  Medium Confidence: {summary.get('medium_confidence', 0)}")
        print(f"  Needs Review: {summary.get('needs_review', 0)}")

        print("\nHypothesis Rankings:")
        rankings = self.synthesis.get('hypothesis_rankings', {})
        for hyp, data in sorted(rankings.items(), key=lambda x: x[1]['rank']):
            print(f"  {data['rank']}. {hyp.upper()}: score={data['total_score']}, words={data['words_supporting']}")

        print("\nTop High-Confidence Findings:")
        for item in self.synthesis.get('high_confidence_findings', [])[:10]:
            print(f"  {item['word']} (freq={item['frequency']}): {item['best_hypothesis'].upper()} [{item['confidence']}]")

        print("\nRecommendations:")
        for rec in self.synthesis.get('recommendations', []):
            print(f"  - {rec}")

        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Linear A Batch Processing Pipeline"
    )
    parser.add_argument(
        '--full', '-f',
        action='store_true',
        help='Run full pipeline on entire corpus'
    )
    parser.add_argument(
        '--stage', '-s',
        choices=['discover', 'hypothesize', 'validate', 'synthesize'],
        help='Run single stage only'
    )
    parser.add_argument(
        '--site',
        type=str,
        help='Filter by site code (e.g., HT, KH, ZA)'
    )
    parser.add_argument(
        '--min-freq', '-m',
        type=int,
        default=2,
        help='Minimum word frequency threshold (default: 2)'
    )
    parser.add_argument(
        '--max-words',
        type=int,
        help='Maximum words to test (default: all)'
    )
    parser.add_argument(
        '--resume', '-r',
        action='store_true',
        help='Resume from last checkpoint'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without executing'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Calculate and display corpus coverage statistics'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed progress'
    )

    args = parser.parse_args()

    pipeline = BatchPipeline(verbose=args.verbose, dry_run=args.dry_run)

    if args.coverage:
        # Just show coverage statistics
        if not pipeline.load_corpus(args.site):
            return 1
        if args.resume:
            pipeline.load_checkpoint('hypothesize')
        coverage = pipeline.calculate_corpus_coverage()
        print("\n" + "=" * 60)
        print("CORPUS COVERAGE ANALYSIS")
        print("=" * 60)
        print(f"\nTotal inscriptions: {coverage.get('total_inscriptions', 0)}")
        print(f"Total words: {coverage.get('total_words', 0)}")
        print(f"Words analyzed: {coverage.get('words_analyzed', 0)}")
        print(f"Overall coverage: {coverage.get('overall_coverage_percent', 0)}%")
        print(f"KU-RO tablets: {coverage.get('kuro_tablets', 0)}")
        print("\nCoverage by Site:")
        for site, stats in coverage.get('by_site', {}).items():
            print(f"  {site:4s}: {stats['inscriptions']:4d} inscriptions, "
                  f"{stats['unique_words']:4d} unique words, "
                  f"{stats['coverage_percent']:5.1f}% analyzed")
        print("\nRecommendations:")
        for rec in coverage.get('recommendations', []):
            print(f"  • {rec}")
        print("=" * 60)
        return 0

    if args.full:
        pipeline.run_full_pipeline(
            min_frequency=args.min_freq,
            max_words=args.max_words,
            site_filter=args.site,
            resume=args.resume
        )
    elif args.stage:
        # Load corpus first
        if not pipeline.load_corpus(args.site):
            return 1

        if args.stage == 'discover':
            pipeline.stage_discover(args.min_freq)
        elif args.stage == 'hypothesize':
            if args.resume:
                pipeline.load_checkpoint('discover')
            else:
                pipeline.stage_discover(args.min_freq)
            pipeline.stage_hypothesize(args.max_words)
        elif args.stage == 'validate':
            if args.resume:
                pipeline.load_checkpoint('hypothesize')
            pipeline.stage_validate()
        elif args.stage == 'synthesize':
            if args.resume:
                pipeline.load_checkpoint('validate')
            pipeline.stage_synthesize()
    else:
        print("Linear A Batch Processing Pipeline")
        print("-" * 40)
        print("Usage:")
        print("  --full          Run complete pipeline")
        print("  --stage STAGE   Run single stage")
        print("  --site SITE     Filter by site code")
        print("  --min-freq N    Minimum frequency threshold")
        print("  --resume        Resume from checkpoint")
        print("")
        print("Example:")
        print("  python batch_pipeline.py --full --min-freq 3 --verbose")
        print("  python batch_pipeline.py --stage discover --site HT")

    return 0


if __name__ == '__main__':
    sys.exit(main())
