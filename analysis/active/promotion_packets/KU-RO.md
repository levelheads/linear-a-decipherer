# Promotion Packet: KU-RO

Use this packet for any confidence promotion or demotion proposal.

---

## 1. Candidate

- Reading: KU-RO
- Current confidence: HIGH
- Proposed confidence: HIGH
- Meaning claim: total/sum
- Primary contexts: PH, ZA, HT

## 2. Evidence Artifacts

- Hypothesis results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/hypothesis_results.json`
- Consistency results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/consistency_validation.json`
- Integrated results: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/integrated_results.json`
- Dependencies: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/reading_dependencies.json`
- Anchors: `/Users/home/AI/Disciplines/Deciphering Ancient Languages/data/anchors.json`
- Optional supporting analysis: Provided via --regional-justification

## 3. Multi-Hypothesis Adjudication

- Luwian: score=1, verdict=POSSIBLE
- Semitic: score=4.35, verdict=SUPPORTED
- Pre-Greek: score=0, verdict=NEUTRAL
- Proto-Greek: score=4.0, verdict=SUPPORTED
- Isolate/null: See integrated Bayesian/isolate context in `data/bayesian_results.json` if needed.

## 4. Negative Evidence

- No explicit negative evidence penalties recorded.
- Contradictions detected: No
- Remaining uncertainty: threshold=MODERATE, final_confidence=PROBABLE

## 5. Cross-Corpus and Regional Behavior

- Sites attested: PH, ZA, HT
- Site concentration (HT): 0.941
- Period spread: ['', 'LMIB']
- Regional weighting impact: 0.944

## 6. Anchor and Dependency Check

- anchor_linear_b_comparison: level=2, confidence=HIGH
- anchor_kuro_total: level=2, confidence=HIGH
- Weakest dependency: HIGH
- Cascade risk if questioned: No cascade warnings

## 7. Gate Checklist

- [x] required_inputs_present (Missing: none)
- [x] no_direct_anchor_contradiction (dependency_warnings=0, threshold=MODERATE)
- [x] integrated_validation (entry=yes, final_confidence=PROBABLE, methodology_compliant=True)
- [x] dependency_trace (anchor_dependencies=2)

## 8. Decision

- Board decision: APPROVE
- Rationale: All required gates passed for requested confidence transition.
- Follow-up actions:
  - Re-run candidate through tool_parity_checker before final publication.; Attach packet and JSON decision record to lane B promotion board review.
