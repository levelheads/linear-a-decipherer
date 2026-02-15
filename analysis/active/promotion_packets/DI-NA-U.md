# Promotion Packet: DI-NA-U

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: DI-NA-U
- Current confidence: SPECULATIVE
- Proposed confidence: PROBABLE
- Meaning claim: Not specified
- Primary contexts: HT, KNZ

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: Provided via --regional-justification

## 3. Multi-Hypothesis Adjudication

- Luwian: score=3, verdict=SUPPORTED
- Semitic: score=0.25, verdict=NEUTRAL
- Pre-Greek: score=1, verdict=WEAK
- Proto-Greek: score=1.5, verdict=POSSIBLE
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=STRONG, final_confidence=SPECULATIVE

## 5. Cross-Corpus and Regional Behavior

- Sites attested: HT, KNZ
- Site concentration (HT): 0.800
- Period spread: ['MMIIIB', 'LMIB']
- Regional weighting impact: 0.95

## 6. Anchor and Dependency Check

- No anchor dependencies found
- Weakest dependency: SPECULATIVE
- Cascade risk if questioned: No registered dependencies

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [x] no_direct_anchor_contradiction (dependency_warnings=1, threshold=STRONG)
- [x] multi_hypothesis_run (All four hypotheses present in hypothesis_results)
- [x] cross_corpus_consistency (validated=True, positional=0.833, functional=0.833, sites=2)
- [x] integrated_validation (entry=yes, final_confidence=SPECULATIVE, methodology_compliant=False)
- [ ] dependency_trace (anchor_dependencies=0)
- [x] negative_evidence_statement (negative_evidence_items=0)

## 8. Decision

- Board decision: HOLD
- Rationale: One or more non-critical required gates failed. Failed gates: dependency_trace
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
