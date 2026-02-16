# Promotion Packet: JA-SA-SA-RA-ME

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: JA-SA-SA-RA-ME
- Current confidence: PROBABLE
- Proposed confidence: PROBABLE
- Meaning claim: divine name (religious formula)
- Primary contexts: IOZ, PK, PLZ, PSZ, TLZ

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: None

## 3. Multi-Hypothesis Adjudication

- Luwian: score=1, verdict=POSSIBLE
- Semitic: score=0.7, verdict=WEAK
- Pre-Greek: score=2.5, verdict=SUPPORTED
- Proto-Greek: score=0.25, verdict=NEUTRAL
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=ELIMINATED, final_confidence=SPECULATIVE

## 5. Cross-Corpus and Regional Behavior

- Sites attested: IOZ, PK, PLZ, PSZ, TLZ
- Site concentration (HT): 0.000
- Period spread: ['', 'LMIA']
- Regional weighting impact: 1.232
- Parity status: LOW

## 6. Anchor and Dependency Check

- anchor_linear_b_comparison: level=2, confidence=HIGH
- Weakest dependency: PROBABLE
- Cascade risk if questioned: No cascade warnings
- Dependency trace source: existing (status: complete)

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [ ] no_direct_anchor_contradiction (dependency_warnings=0, threshold=ELIMINATED)
- [x] parity_guard (parity_level=LOW)
- [x] integrated_validation (entry=yes, final_confidence=SPECULATIVE, methodology_compliant=True)
- [x] dependency_trace (anchor_dependencies=1, trace_source=existing)

## 8. Decision

- Board decision: REJECT
- Rationale: Critical gate failure detected (missing artifacts or direct contradiction). Failed gates: no_direct_anchor_contradiction
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
