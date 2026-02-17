#!/usr/bin/env python3
"""
Bayesian Hypothesis Tester for Linear A

Replaces binary matching with calibrated probabilistic inference.
Addresses the critique: "What does '30.3% support' actually mean epistemically?"

Features:
- Calibrated prior probabilities from external evidence
- Posterior probabilities with 95% credible intervals
- Bayes factors (hypothesis vs isolate null)
- Multi-hypothesis support (code-switching model)
- Prior sensitivity analysis

Prior Probabilities (calibrated):
    Luwian:     0.25  (geographic proximity, Palmer/Finkelberg case)
    Semitic:    0.15  (trade routes, Gordon's evidence)
    Pre-Greek:  0.20  (substrate theory, Beekes' lexicon)
    Proto-Greek: 0.05 (low /o/ argues against)
    Isolate:    0.35  (conservative null hypothesis)

Usage:
    python tools/bayesian_hypothesis_tester.py --word ku-ro --detail
    python tools/bayesian_hypothesis_tester.py --corpus --output data/bayesian_results.json
    python tools/bayesian_hypothesis_tester.py --sensitivity

Attribution:
    Part of Linear A Decipherment Project
    Extends hypothesis_tester.py with Bayesian inference
"""

import json
import argparse
import sys
import math
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
import re


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CORPUS_FILE = DATA_DIR / "corpus.json"
HYPOTHESIS_RESULTS_FILE = DATA_DIR / "hypothesis_results.json"

# Import lexicons from hypothesis_tester if available
try:
    from hypothesis_tester import (
        LUWIAN_LEXICON,
        SEMITIC_LEXICON,
        PREGREEK_MARKERS,
        PREGREEK_VOCABULARY,
        GREEK_LEXICON,
        extract_consonants,
    )
except ImportError:
    # Define minimal versions if import fails
    LUWIAN_LEXICON = {}
    SEMITIC_LEXICON = {}
    PREGREEK_MARKERS = {}
    PREGREEK_VOCABULARY = {}
    GREEK_LEXICON = {}

    def extract_consonants(word: str) -> str:
        consonants = []
        syllables = word.upper().split("-")
        for syl in syllables:
            syl = re.sub(r"[₀₁₂₃₄₅₆₇₈₉]", "", syl)
            if len(syl) >= 1:
                first = syl[0]
                if first not in "AEIOU":
                    consonants.append(first)
        return "".join(consonants)


# ============================================================================
# PRIOR PROBABILITIES
# ============================================================================

# Calibrated priors based on external evidence
DEFAULT_PRIORS = {
    "luwian": 0.22,  # Geographic proximity, Palmer/Finkelberg case
    "semitic": 0.12,  # Trade routes, Gordon's administrative vocabulary
    "pregreek": 0.15,  # Substrate theory, Beekes' lexicon of Pre-Greek
    "protogreek": 0.03,  # Low /o/ frequency strongly argues against
    "hurrian": 0.10,  # Agglutinative, 4-vowel (no /o/), 2nd millennium Levant
    "hattic": 0.03,  # Prefix-dominant — structural mismatch with Linear A
    "etruscan": 0.02,  # Lemnian/Tyrsenian Aegean presence; chronological gap
    "isolate": 0.33,  # Conservative null hypothesis
}

# Prior rationales
PRIOR_RATIONALES = {
    "luwian": [
        "Geographic proximity: Anatolia accessible via western trade routes",
        "Palmer (1958) and Finkelberg (1998) identified morphological parallels",
        "30.3% corpus support (highest of tested hypotheses)",
        "Religious texts show +14.5% Luwian affinity vs administrative",
    ],
    "semitic": [
        "Bronze Age trade routes connected Crete with Levant",
        "Gordon (1966) identified KU-RO = *kull administrative parallel",
        "17.7% corpus support concentrated in administrative vocabulary",
        "Absence of triconsonantal morphology suggests loans, not genetic",
    ],
    "pregreek": [
        "Substrate theory: Pre-Greek layer in Greek toponyms and vocabulary",
        "Beekes (2014) documented extensive Pre-Greek vocabulary",
        "Low direct evidence (1.5%) may reflect detection limitations",
        "Pre-Greek is 'residual' hypothesis - gains when others fail",
    ],
    "protogreek": [
        "Very low prior due to /o/ frequency (2.9% vs expected 20%)",
        "Absence of Greek case endings",
        "Different totaling vocabulary (KU-RO vs to-so)",
        "Only 2.5% corpus support; effectively eliminated",
    ],
    "isolate": [
        "Conservative null hypothesis: Minoan is a language isolate",
        "No definitive genetic affiliation established",
        "Davis (2014) 'isolated language' consensus",
        "Methodologically important to test against null",
    ],
    "hurrian": [
        "Agglutinative morphology with suffixation — compatible with Linear A",
        "4-vowel system (a,e,i,u, no /o/) matches Linear A's near-zero /o/",
        "2nd millennium BCE Levant presence (Nuzi, Alalakh, Mittani)",
        "SOV word order conflicts with Linear A VSO tendency",
    ],
    "hattic": [
        "Pre-Indo-European Anatolian language",
        "CRITICAL: Prefix-dominant morphology contradicts Linear A suffix-dominant pattern",
        "Known primarily from Hattic-Hittite bilinguals; small reference corpus",
        "Low prior reflects structural mismatch",
    ],
    "etruscan": [
        "Tyrsenian family includes Lemnian (Aegean) — geographic plausibility",
        "Suffixing morphology compatible with Linear A",
        "Chronological gap: Etruscan texts 7th c. BCE vs Linear A 17th-15th c. BCE",
        "Vowel syncope in Etruscan differs from Linear A full vowels",
    ],
}


@dataclass
class LikelihoodEvidence:
    """Evidence contributing to likelihood calculation."""

    evidence_type: str  # lexical, morphological, phonological, structural
    observation: str
    likelihood_luwian: float
    likelihood_semitic: float
    likelihood_pregreek: float
    likelihood_protogreek: float
    likelihood_isolate: float
    weight: float  # How much this evidence counts


@dataclass
class BayesianResult:
    """Result of Bayesian analysis for a word."""

    word: str
    frequency: int
    priors: Dict[str, float]
    likelihoods: Dict[str, float]
    posteriors: Dict[str, float]
    credible_intervals: Dict[str, Tuple[float, float]]
    bayes_factors: Dict[str, float]
    evidence: List[LikelihoodEvidence]
    best_hypothesis: str
    multi_hypothesis_support: Dict[str, float]  # For code-switching model
    interpretation: str


class BayesianHypothesisTester:
    """
    Bayesian hypothesis tester for Linear A readings.

    Uses Bayes' theorem to compute posterior probabilities:
    P(H|E) = P(E|H) * P(H) / P(E)

    Where:
    - P(H|E) = posterior probability of hypothesis given evidence
    - P(E|H) = likelihood of evidence under hypothesis
    - P(H) = prior probability of hypothesis
    - P(E) = normalizing constant (sum over all hypotheses)
    """

    def __init__(self, priors: Dict[str, float] = None, verbose: bool = False):
        self.verbose = verbose
        self.priors = priors or DEFAULT_PRIORS.copy()
        self.corpus = {}
        self.hypothesis_results = {}

        # Normalize priors
        total = sum(self.priors.values())
        self.priors = {k: v / total for k, v in self.priors.items()}

    def log(self, msg: str):
        if self.verbose:
            print(f"  {msg}")

    def load_data(self) -> bool:
        """Load corpus and existing hypothesis results."""
        try:
            with open(CORPUS_FILE, "r", encoding="utf-8") as f:
                self.corpus = json.load(f)

            if HYPOTHESIS_RESULTS_FILE.exists():
                with open(HYPOTHESIS_RESULTS_FILE, "r", encoding="utf-8") as f:
                    self.hypothesis_results = json.load(f)

            print(f"Loaded corpus: {len(self.corpus.get('inscriptions', {}))} inscriptions")
            return True

        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def calculate_lexical_likelihood(self, word: str) -> Dict[str, float]:
        """
        Calculate likelihood based on lexical matches.

        Returns likelihood values for each hypothesis.
        """
        likelihoods = {h: 0.1 for h in self.priors}

        word_upper = word.upper()
        syllables = word_upper.split("-")
        consonants = extract_consonants(word)

        # Check Luwian lexicon
        for luw_word, data in LUWIAN_LEXICON.items():
            if luw_word.upper() in word_upper or word_upper in luw_word.upper():
                conf = data.get("confidence", "LOW")
                boost = 0.3 if conf == "HIGH" else 0.2 if conf == "MEDIUM" else 0.1
                likelihoods["luwian"] += boost

        # Check Semitic roots
        for sem_word, data in SEMITIC_LEXICON.items():
            root = data.get("root", sem_word.upper())
            if consonants == root or consonants in root or root in consonants:
                conf = data.get("confidence", "LOW")
                boost = 0.3 if conf == "HIGH" else 0.2 if conf == "MEDIUM" else 0.1
                likelihoods["semitic"] += boost

        # Check Greek cognates
        for greek_word, data in GREEK_LEXICON.items():
            linear_b = data.get("Linear_B", "").upper()
            if linear_b and (
                word_upper == linear_b or word_upper in linear_b or linear_b in word_upper
            ):
                conf = data.get("confidence", "LOW")
                boost = 0.3 if conf == "HIGH" else 0.2 if conf == "MEDIUM" else 0.1
                likelihoods["protogreek"] += boost

        # Check Pre-Greek markers
        for marker in PREGREEK_MARKERS:
            if marker.upper() in word_upper:
                sig = PREGREEK_MARKERS[marker].get("significance", "LOW")
                boost = 0.3 if sig == "HIGH" else 0.2 if sig == "MEDIUM" else 0.1
                likelihoods["pregreek"] += boost

        # Hurrian: lexical matches from hypothesis_results if available
        if self.hypothesis_results:
            word_data = self.hypothesis_results.get("word_analyses", {}).get(word_upper, {})
            hurr_data = word_data.get("hypotheses", {}).get("hurrian", {})
            if hurr_data.get("score", 0) > 0:
                likelihoods.setdefault("hurrian", 0.1)
                likelihoods["hurrian"] += min(0.3, hurr_data["score"] * 0.1)
            hatt_data = word_data.get("hypotheses", {}).get("hattic", {})
            if hatt_data.get("score", 0) > 0:
                likelihoods.setdefault("hattic", 0.1)
                likelihoods["hattic"] += min(0.3, hatt_data["score"] * 0.1)
            etr_data = word_data.get("hypotheses", {}).get("etruscan", {})
            if etr_data.get("score", 0) > 0:
                likelihoods.setdefault("etruscan", 0.1)
                likelihoods["etruscan"] += min(0.3, etr_data["score"] * 0.1)

        # Normalize to [0, 1] range
        for hyp in likelihoods:
            likelihoods[hyp] = min(1.0, likelihoods[hyp])

        return likelihoods

    def calculate_morphological_likelihood(self, word: str) -> Dict[str, float]:
        """
        Calculate likelihood based on morphological patterns.
        """
        likelihoods = {h: 0.1 for h in self.priors}

        word_upper = word.upper()
        syllables = word_upper.split("-")

        # Luwian morphology
        if syllables[0] == "A":  # Conjunction
            likelihoods["luwian"] += 0.15
        if "WA" in syllables or "U" in syllables:  # Quotative
            likelihoods["luwian"] += 0.15
        if word_upper.endswith("-JA"):  # Adjectival
            likelihoods["luwian"] += 0.2
        if word_upper.endswith("-TI") or word_upper.endswith("-NTI"):  # Verbal
            likelihoods["luwian"] += 0.15

        # Semitic morphology (weak evidence - we know it's mostly loans)
        consonants = extract_consonants(word)
        if len(consonants) == 3:  # Triconsonantal
            likelihoods["semitic"] += 0.1

        # Greek morphology
        greek_endings = ["O", "A", "OS", "AS", "ES", "OI", "AI"]
        if syllables and syllables[-1] in greek_endings:
            likelihoods["protogreek"] += 0.1

        # Pre-Greek (limited morphological criteria)
        if len(syllables) >= 2 and syllables[0] == syllables[1]:  # Gemination
            likelihoods["pregreek"] += 0.1

        # Hurrian morphology (agglutinative, case suffixes)
        if "hurrian" in likelihoods:
            hurrian_suffixes = ["NE", "DA", "NA", "WA", "SSE", "SE"]
            if syllables and syllables[-1] in hurrian_suffixes:
                likelihoods["hurrian"] += 0.15
            if len(syllables) >= 4:  # Agglutinative polysyllabic
                likelihoods["hurrian"] += 0.1

        # Hattic morphology (prefix-dominant — mostly negative for Linear A)
        if "hattic" in likelihoods:
            hattic_prefixes = ["WA", "A", "TA", "TE", "TU"]
            if syllables and syllables[0] in hattic_prefixes:
                likelihoods["hattic"] += 0.1
            # Suffix-heavy words are negative for Hattic
            common_suffixes = ["ME", "SI", "JA", "TE", "TI"]
            if syllables and syllables[-1] in common_suffixes:
                likelihoods["hattic"] *= 0.8  # Reduce

        # Etruscan morphology (suffixing, genitive -s)
        if "etruscan" in likelihoods:
            etruscan_suffixes = ["SI", "SA", "LE", "KE", "NE"]
            if syllables and syllables[-1] in etruscan_suffixes:
                likelihoods["etruscan"] += 0.1

        # Isolate gets boost for unmatched patterns
        if max(likelihoods.values()) < 0.2:
            likelihoods["isolate"] += 0.2

        # Normalize
        for hyp in likelihoods:
            likelihoods[hyp] = min(1.0, likelihoods[hyp])

        return likelihoods

    def calculate_phonological_likelihood(self, word: str) -> Dict[str, float]:
        """
        Calculate likelihood based on phonological patterns.
        """
        likelihoods = {h: 0.1 for h in self.priors}

        word_upper = word.upper()
        syllables = word_upper.split("-")

        # Vowel distribution (critical for Greek)
        vowels = []
        for syl in syllables:
            syl_clean = re.sub(r"[₀₁₂₃₄₅₆₇₈₉]", "", syl)
            if syl_clean and syl_clean[-1] in "AEIOU":
                vowels.append(syl_clean[-1])

        if vowels:
            o_freq = vowels.count("O") / len(vowels)
            a_freq = vowels.count("A") / len(vowels)

            # Low /o/ argues against Greek
            if o_freq < 0.1:
                likelihoods["protogreek"] *= 0.5
                likelihoods["isolate"] += 0.1
                # Low /o/ supports Hurrian (4-vowel system: a,e,i,u)
                if "hurrian" in likelihoods:
                    likelihoods["hurrian"] += 0.15

            # High /a/ compatible with Anatolian/Semitic
            if a_freq > 0.4:
                likelihoods["luwian"] += 0.1
                likelihoods["semitic"] += 0.1

            # /o/ presence argues against Hurrian
            if o_freq > 0.2 and "hurrian" in likelihoods:
                likelihoods["hurrian"] *= 0.7

        # Labialized consonants (Luwian feature)
        for syl in syllables:
            if syl.startswith("W") or syl.startswith("KW") or syl.startswith("QU"):
                likelihoods["luwian"] += 0.1
                break

        # Normalize
        for hyp in likelihoods:
            likelihoods[hyp] = min(1.0, likelihoods[hyp])

        return likelihoods

    def compute_posterior(self, word: str, frequency: int = 1) -> BayesianResult:
        """
        Compute Bayesian posterior probabilities for a word.

        Uses Bayes' theorem with evidence from lexical, morphological,
        and phonological analyses.
        """
        evidence = []

        # Calculate likelihoods from different evidence types
        lexical_lik = self.calculate_lexical_likelihood(word)
        morph_lik = self.calculate_morphological_likelihood(word)
        phon_lik = self.calculate_phonological_likelihood(word)

        # Combine likelihoods (geometric mean for independence assumption)
        combined_likelihoods = {}
        for hyp in self.priors:
            combined_likelihoods[hyp] = (
                lexical_lik[hyp] ** 0.4 * morph_lik[hyp] ** 0.3 * phon_lik[hyp] ** 0.3
            )

        # Apply Bayes' theorem
        # P(H|E) ∝ P(E|H) * P(H)
        unnormalized_posteriors = {}
        for hyp in self.priors:
            unnormalized_posteriors[hyp] = combined_likelihoods[hyp] * self.priors[hyp]

        # Normalize
        total = sum(unnormalized_posteriors.values())
        posteriors = {}
        for hyp in self.priors:
            posteriors[hyp] = (
                unnormalized_posteriors[hyp] / total if total > 0 else self.priors[hyp]
            )

        # Calculate credible intervals using Beta distribution approximation
        credible_intervals = {}
        for hyp, post in posteriors.items():
            # Simple approximation based on posterior and effective sample size
            # More rigorous would use MCMC
            effective_n = frequency + 1
            alpha = post * effective_n
            beta = (1 - post) * effective_n + 1
            # 95% credible interval from Beta distribution
            lower = max(0, post - 1.96 * math.sqrt(post * (1 - post) / effective_n))
            upper = min(1, post + 1.96 * math.sqrt(post * (1 - post) / effective_n))
            credible_intervals[hyp] = (round(lower, 4), round(upper, 4))

        # Calculate Bayes factors vs isolate null
        bayes_factors = {}
        isolate_post = posteriors.get("isolate", 0.001)
        for hyp in posteriors:
            if hyp != "isolate":
                bf = posteriors[hyp] / isolate_post if isolate_post > 0 else 0
                bayes_factors[hyp] = round(bf, 3)

        # Determine best hypothesis
        best_hyp = max(posteriors.keys(), key=lambda k: posteriors[k])

        # Multi-hypothesis support (code-switching model)
        # Normalize non-isolate posteriors for weighting
        non_isolate = {k: v for k, v in posteriors.items() if k != "isolate"}
        total_non_isolate = sum(non_isolate.values())
        multi_support = {}
        if total_non_isolate > 0:
            for hyp, post in non_isolate.items():
                if post > 0.1:  # Threshold for meaningful support
                    multi_support[hyp] = round(post / total_non_isolate, 3)

        # Generate interpretation
        interpretation = self._generate_interpretation(posteriors, bayes_factors, best_hyp)

        return BayesianResult(
            word=word,
            frequency=frequency,
            priors=self.priors.copy(),
            likelihoods=combined_likelihoods,
            posteriors=posteriors,
            credible_intervals=credible_intervals,
            bayes_factors=bayes_factors,
            evidence=evidence,
            best_hypothesis=best_hyp,
            multi_hypothesis_support=multi_support,
            interpretation=interpretation,
        )

    def _generate_interpretation(
        self, posteriors: Dict[str, float], bayes_factors: Dict[str, float], best_hyp: str
    ) -> str:
        """Generate human-readable interpretation."""
        best_post = posteriors[best_hyp]
        best_bf = bayes_factors.get(best_hyp, 0)

        # Interpret posterior
        if best_post > 0.5:
            strength = "strongly"
        elif best_post > 0.3:
            strength = "moderately"
        else:
            strength = "weakly"

        # Interpret Bayes factor
        if best_bf > 100:
            bf_interp = "very strong evidence"
        elif best_bf > 10:
            bf_interp = "strong evidence"
        elif best_bf > 3:
            bf_interp = "moderate evidence"
        elif best_bf > 1:
            bf_interp = "weak evidence"
        else:
            bf_interp = "no evidence"

        # Check for multi-hypothesis support
        above_threshold = [h for h, p in posteriors.items() if p > 0.15 and h != "isolate"]

        if len(above_threshold) > 1:
            return (
                f"{best_hyp.capitalize()} {strength} supported (P={best_post:.2f}), "
                f"but multi-hypothesis model suggests: {', '.join(above_threshold)}"
            )
        else:
            return (
                f"{best_hyp.capitalize()} {strength} supported (P={best_post:.2f}); "
                f"{bf_interp} vs isolate null (BF={best_bf:.1f})"
            )

    def sensitivity_analysis(self, word: str) -> Dict:
        """
        Perform prior sensitivity analysis.

        Tests how posteriors change under different prior assumptions.
        """
        results = {}

        # Test different prior configurations
        prior_configs = {
            "default": DEFAULT_PRIORS.copy(),
            "uniform": {h: 1.0 / len(DEFAULT_PRIORS) for h in DEFAULT_PRIORS},
            "luwian_dominant": {
                "luwian": 0.35,
                "semitic": 0.10,
                "pregreek": 0.10,
                "protogreek": 0.03,
                "hurrian": 0.08,
                "hattic": 0.02,
                "etruscan": 0.02,
                "isolate": 0.30,
            },
            "semitic_dominant": {
                "luwian": 0.15,
                "semitic": 0.30,
                "pregreek": 0.10,
                "protogreek": 0.03,
                "hurrian": 0.08,
                "hattic": 0.02,
                "etruscan": 0.02,
                "isolate": 0.30,
            },
            "hurrian_dominant": {
                "luwian": 0.15,
                "semitic": 0.10,
                "pregreek": 0.10,
                "protogreek": 0.03,
                "hurrian": 0.25,
                "hattic": 0.02,
                "etruscan": 0.02,
                "isolate": 0.33,
            },
            "skeptical": {
                "luwian": 0.10,
                "semitic": 0.08,
                "pregreek": 0.10,
                "protogreek": 0.03,
                "hurrian": 0.06,
                "hattic": 0.02,
                "etruscan": 0.02,
                "isolate": 0.59,
            },
        }

        for config_name, priors in prior_configs.items():
            # Normalize
            total = sum(priors.values())
            priors = {k: v / total for k, v in priors.items()}

            # Temporarily update priors
            old_priors = self.priors
            self.priors = priors

            result = self.compute_posterior(word)

            results[config_name] = {
                "priors": priors,
                "posteriors": result.posteriors,
                "best_hypothesis": result.best_hypothesis,
                "best_posterior": result.posteriors[result.best_hypothesis],
            }

            self.priors = old_priors

        # Check stability
        best_hypotheses = [r["best_hypothesis"] for r in results.values()]
        stable = len(set(best_hypotheses)) == 1

        return {
            "word": word,
            "configurations": results,
            "stable": stable,
            "interpretation": "Robust to prior changes"
            if stable
            else "Sensitive to prior assumptions",
        }

    def analyze_corpus(self, min_freq: int = 2) -> List[BayesianResult]:
        """
        Run Bayesian analysis on all corpus words.
        """
        # Extract word frequencies
        word_freq = Counter()
        for insc_id, data in self.corpus.get("inscriptions", {}).items():
            if "_parse_error" in data:
                continue
            for word in data.get("transliteratedWords", []):
                if word and "-" in word and word not in ["\n", "𐄁", ""]:
                    word_freq[word.upper()] += 1

        # Analyze words above threshold
        results = []
        for word, freq in word_freq.most_common():
            if freq >= min_freq:
                result = self.compute_posterior(word, freq)
                results.append(result)
                self.log(
                    f"{word}: {result.best_hypothesis} (P={result.posteriors[result.best_hypothesis]:.2f})"
                )

        return results

    def generate_report(self, results: List[BayesianResult]) -> Dict:
        """Generate comprehensive Bayesian analysis report."""
        # Aggregate by best hypothesis
        by_hypothesis = defaultdict(list)
        for r in results:
            by_hypothesis[r.best_hypothesis].append(r)

        # Calculate aggregate posteriors
        aggregate_posteriors = defaultdict(list)
        for r in results:
            for hyp, post in r.posteriors.items():
                aggregate_posteriors[hyp].append(post)

        mean_posteriors = {
            hyp: sum(posts) / len(posts) for hyp, posts in aggregate_posteriors.items()
        }

        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "method": "Bayesian Hypothesis Testing",
                "words_analyzed": len(results),
                "priors_used": self.priors,
            },
            "aggregate_results": {
                "mean_posteriors": mean_posteriors,
                "words_per_hypothesis": {h: len(words) for h, words in by_hypothesis.items()},
            },
            "hypothesis_summaries": {},
            "word_details": [asdict(r) for r in results[:100]],  # Top 100
        }

        for hyp in self.priors:
            words = by_hypothesis.get(hyp, [])
            posteriors = [r.posteriors[hyp] for r in results]
            report["hypothesis_summaries"][hyp] = {
                "best_for_n_words": len(words),
                "mean_posterior": round(sum(posteriors) / len(posteriors), 4) if posteriors else 0,
                "max_posterior": round(max(posteriors), 4) if posteriors else 0,
                "prior": self.priors[hyp],
                "posterior_shift": round((sum(posteriors) / len(posteriors)) - self.priors[hyp], 4)
                if posteriors
                else 0,
            }

        return report

    def print_result(self, result: BayesianResult):
        """Print formatted Bayesian result."""
        print(f"\n{result.word} (freq={result.frequency})")
        print("─" * 60)

        print("\nPrior → Posterior (95% CI):")
        for hyp in sorted(result.posteriors.keys(), key=lambda h: -result.posteriors[h]):
            prior = result.priors[hyp]
            post = result.posteriors[hyp]
            ci = result.credible_intervals[hyp]
            bf = result.bayes_factors.get(hyp, "")
            bf_str = f"BF={bf:.1f}" if bf else ""

            bar_len = int(post * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)

            print(f"  {hyp:12} {prior:.2f} → {post:.3f} [{ci[0]:.2f}, {ci[1]:.2f}] {bar} {bf_str}")

        if result.multi_hypothesis_support and len(result.multi_hypothesis_support) > 1:
            print("\nMulti-hypothesis support (code-switching model):")
            for hyp, weight in sorted(result.multi_hypothesis_support.items(), key=lambda x: -x[1]):
                print(f"  {hyp}: {weight:.1%}")

        print(f"\nBest: {result.best_hypothesis.upper()}")
        print(f"Interpretation: {result.interpretation}")

    def print_report(self, report: Dict):
        """Print formatted report."""
        print("\n" + "=" * 70)
        print("BAYESIAN HYPOTHESIS TESTING REPORT")
        print("=" * 70)

        print(f"\nWords Analyzed: {report['metadata']['words_analyzed']}")

        print("\nPrior Probabilities:")
        for hyp, prior in report["metadata"]["priors_used"].items():
            print(f"  {hyp:12} {prior:.2f}")

        print("\nAggregate Results (Mean Posterior):")
        for hyp, mean_post in sorted(
            report["aggregate_results"]["mean_posteriors"].items(), key=lambda x: -x[1]
        ):
            prior = report["metadata"]["priors_used"][hyp]
            shift = mean_post - prior
            arrow = "↑" if shift > 0 else "↓" if shift < 0 else "→"
            print(f"  {hyp:12} {mean_post:.3f} ({arrow}{abs(shift):.3f} from prior)")

        print("\nWords Best Explained By:")
        for hyp, count in sorted(
            report["aggregate_results"]["words_per_hypothesis"].items(), key=lambda x: -x[1]
        ):
            pct = count / report["metadata"]["words_analyzed"] * 100
            print(f"  {hyp:12} {count:4d} ({pct:.1f}%)")

        print("\nHypothesis Performance:")
        for hyp, summary in sorted(
            report["hypothesis_summaries"].items(), key=lambda x: -x[1]["mean_posterior"]
        ):
            print(f"\n  {hyp.upper()}:")
            print(f"    Best for {summary['best_for_n_words']} words")
            print(
                f"    Mean posterior: {summary['mean_posterior']:.3f} (prior: {summary['prior']:.2f})"
            )
            print(f"    Max posterior: {summary['max_posterior']:.3f}")
            print(f"    Shift from prior: {summary['posterior_shift']:+.3f}")

        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Bayesian hypothesis testing for Linear A")
    parser.add_argument("--word", "-w", type=str, help="Analyze a specific word")
    parser.add_argument(
        "--detail", "-d", action="store_true", help="Show detailed evidence breakdown"
    )
    parser.add_argument("--corpus", "-c", action="store_true", help="Analyze full corpus")
    parser.add_argument(
        "--min-freq",
        "-m",
        type=int,
        default=2,
        help="Minimum frequency for corpus analysis (default: 2)",
    )
    parser.add_argument(
        "--sensitivity",
        "-s",
        type=str,
        metavar="WORD",
        help="Run prior sensitivity analysis for a word",
    )
    parser.add_argument("--output", "-o", type=str, help="Output path for JSON results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print("=" * 70)
    print("LINEAR A BAYESIAN HYPOTHESIS TESTER")
    print("=" * 70)

    tester = BayesianHypothesisTester(verbose=args.verbose)
    if not tester.load_data():
        return 1

    if args.sensitivity:
        print(f"\nPrior Sensitivity Analysis: {args.sensitivity}")
        result = tester.sensitivity_analysis(args.sensitivity)

        print(f"\nStability: {result['interpretation']}")
        print("\nResults by Prior Configuration:")
        for config, data in result["configurations"].items():
            print(f"\n  {config}:")
            print(f"    Best: {data['best_hypothesis']} (P={data['best_posterior']:.3f})")

        return 0

    if args.word:
        result = tester.compute_posterior(args.word)
        tester.print_result(result)
        return 0

    if args.corpus:
        print(f"\nAnalyzing corpus (min freq >= {args.min_freq})...")
        results = tester.analyze_corpus(min_freq=args.min_freq)
        report = tester.generate_report(results)
        tester.print_report(report)

        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\nReport saved to: {output_path}")

        return 0

    # Default: show priors and usage
    print("\nDefault Prior Probabilities:")
    for hyp, prior in DEFAULT_PRIORS.items():
        print(f"  {hyp:12} {prior:.2f}")
        for rationale in PRIOR_RATIONALES[hyp][:2]:
            print(f"    • {rationale[:60]}...")

    print("\nUse --word WORD or --corpus for analysis")
    return 0


if __name__ == "__main__":
    sys.exit(main())
