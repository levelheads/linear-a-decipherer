# Promotion Packet: A-DU

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: A-DU
- Current confidence: SPECULATIVE
- Proposed confidence: PROBABLE
- Meaning claim: Not specified
- Primary contexts: HT, KH, TY

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: Provided via --regional-justification

## 3. Multi-Hypothesis Adjudication

- Luwian: score=3, verdict=SUPPORTED
- Semitic: score=3.15, verdict=SUPPORTED
- Pre-Greek: score=0.5, verdict=WEAK
- Proto-Greek: score=2.0, verdict=POSSIBLE
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=MODERATE, final_confidence=SPECULATIVE

## 5. Cross-Corpus and Regional Behavior

- Sites attested: HT, KH, TY
- Site concentration (HT): 0.700
- Period spread: ['', 'LMIB']
- Regional weighting impact: 1.158

## 6. Anchor and Dependency Check

- No anchor dependencies found
- Weakest dependency: SPECULATIVE
- Cascade risk if questioned: No registered dependencies

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [x] no_direct_anchor_contradiction (dependency_warnings=1, threshold=MODERATE)
- [x] multi_hypothesis_run (All four hypotheses present in hypothesis_results)
- [ ] cross_corpus_consistency (validated=True, positional=0.700, functional=0.550, sites=3)
- [x] integrated_validation (entry=yes, final_confidence=SPECULATIVE, methodology_compliant=False)
- [ ] dependency_trace (anchor_dependencies=0)
- [x] negative_evidence_statement (negative_evidence_items=0)

## 8. Decision

- Board decision: HOLD
- Rationale: One or more non-critical required gates failed. Failed gates: cross_corpus_consistency, dependency_trace
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
