# Promotion Packet: SA-RA₂

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: SA-RA₂
- Current confidence: MEDIUM
- Proposed confidence: PROBABLE
- Meaning claim: allocation (*šarāku)
- Primary contexts: HT

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: Provided via --regional-justification

## 3. Multi-Hypothesis Adjudication

- Luwian: score=1, verdict=POSSIBLE
- Semitic: score=1.2999999999999998, verdict=WEAK
- Pre-Greek: score=1, verdict=WEAK
- Proto-Greek: score=0, verdict=NEUTRAL
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=WEAK, final_confidence=MEDIUM

## 5. Cross-Corpus and Regional Behavior

- Sites attested: HT
- Site concentration (HT): 1.000
- Period spread: ['LMIB']
- Regional weighting impact: 0.6
- Parity status: LOW

## 6. Anchor and Dependency Check

- anchor_linear_b_comparison: level=2, confidence=HIGH
- anchor_semitic_loan_layer: level=4, confidence=MEDIUM
- Weakest dependency: MEDIUM
- Cascade risk if questioned: No cascade warnings
- Dependency trace source: existing (status: complete)

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [x] no_direct_anchor_contradiction (dependency_warnings=0, threshold=WEAK)
- [x] parity_guard (parity_level=LOW)
- [x] multi_hypothesis_run (All four hypotheses present in hypothesis_results)
- [x] cross_corpus_consistency (validated=True, positional=0.850, functional=0.750, sites=1, rule=min>=0.55 and max>=0.70)
- [x] integrated_validation (entry=yes, final_confidence=MEDIUM, methodology_compliant=True)
- [x] dependency_trace (anchor_dependencies=2, trace_source=existing)
- [x] provisional_trace_review (trace_source=existing, allow_override=False)
- [x] negative_evidence_statement (negative_evidence_items=0)

## 8. Decision

- Board decision: APPROVE
- Rationale: All required gates passed for requested confidence transition.
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
