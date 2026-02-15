# Promotion Packet: I-RA₂

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: I-RA₂
- Current confidence: SPECULATIVE
- Proposed confidence: PROBABLE
- Meaning claim: Not specified
- Primary contexts: HTW

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: Provided via --regional-justification

## 3. Multi-Hypothesis Adjudication

- Luwian: score=1, verdict=POSSIBLE
- Semitic: score=7.699999999999998, verdict=SUPPORTED
- Pre-Greek: score=0, verdict=NEUTRAL
- Proto-Greek: score=0.5, verdict=WEAK
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=WEAK, final_confidence=SPECULATIVE

## 5. Cross-Corpus and Regional Behavior

- Sites attested: HTW
- Site concentration (HT): 1.000
- Period spread: ['LMIB']
- Regional weighting impact: 0.6

## 6. Anchor and Dependency Check

- No anchor dependencies found
- Weakest dependency: SPECULATIVE
- Cascade risk if questioned: No registered dependencies

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [x] no_direct_anchor_contradiction (dependency_warnings=1, threshold=WEAK)
- [x] multi_hypothesis_run (All four hypotheses present in hypothesis_results)
- [x] cross_corpus_consistency (validated=True, positional=1.000, functional=1.000, sites=1)
- [x] integrated_validation (entry=yes, final_confidence=SPECULATIVE, methodology_compliant=False)
- [ ] dependency_trace (anchor_dependencies=0)
- [x] negative_evidence_statement (negative_evidence_items=0)

## 8. Decision

- Board decision: HOLD
- Rationale: One or more non-critical required gates failed. Failed gates: dependency_trace
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
