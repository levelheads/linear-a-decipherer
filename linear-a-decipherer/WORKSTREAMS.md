# Workstreams

This document defines parallel execution contracts for accelerated decipherment work.

All workstreams must follow:

1. `linear-a-decipherer/METHODOLOGY.md`
2. `linear-a-decipherer/MASTER_STATE.md`
3. Promotion gates in `templates/PROMOTION_PACKET_TEMPLATE.md`

---

## Workstream Matrix

| Lane | Mission | Inputs | Outputs | Gate to Merge |
|------|---------|--------|---------|---------------|
| A | SSOT + governance | Current docs, metrics artifacts | Canonical status updates, redirect hygiene | SSOT guard checks pass |
| B | Validation + quality | Hypothesis, consistency, integrated results | Promotion packet decisions | All required reports present and coherent |
| C | Script asymmetry | Corpus structure/sign distributions | Sign function hypotheses | Cross-corpus + anchor checks |
| D | Language asymmetry (MAINTENANCE) | Hypothesis and Bayesian outputs | Language-layer updates | Integrated validator + negative evidence |
| E | Throughput engine | Corpus queue + site balancing rules | Expanded coverage and deep-dives | Coverage report and site-bias note |
| F | Release/process | Tags, CITATION, changelog, SSOT | Release candidate package | Strict CI + release gate pass |
| G | Reading attempts | Anchored words, admin isomorphism, morphological predictions | Connected tablet readings, Rosetta skeletons | Arithmetic verification + cross-site consistency |

---

## Operating Rhythm (Weekly)

1. Monday: baseline refresh and queue lock
2. Midweek: lane sync with blocker escalation
3. Friday: promotion board + release readiness snapshot

---

## Handoff Contract (Required in every lane update)

1. What changed
2. Evidence artifact paths
3. Confidence impact (if any)
4. Dependencies affected
5. Open risks
6. Required reviewer lane

---

## Lane Notes

### Lane D: Language Asymmetry — MAINTENANCE MODE (2026-02-17)

Mission accomplished: 5/7 hypotheses ELIMINATED. Focus on Luwian (STRONG 35.0%) and Semitic (MODERATE 17.5%) only. Further refinement of Bayesian posteriors and falsification thresholds produces diminishing returns. Lane D reduced to maintenance — re-run validators only when new evidence surfaces.

### Lane G: Reading Attempts — NEW (2026-02-17)

**Mission**: Produce connected readings of specific tablets using all accumulated evidence.

**Rationale**: The project has answered the language question as well as it can without a breakthrough: isolate substrate with Luwian morphological influence and Semitic administrative loans. The strategic pivot moves from "which language is it?" to "what do these texts say?"

**Workflow**:
1. Select tablets with highest density of anchored/identified words
2. List every word on the tablet with known values
3. Mark positional identifications from admin_isomorphism (46 identifications)
4. Mark paradigm memberships from morphological_predictor
5. Apply arithmetic verification where possible
6. Attempt connected reading (even with 50%+ unknown)
7. Identify which unknown words are most constrained by context → next analysis targets

**Priority targets**:
- KU-RO tablets (39 occurrences) — arithmetic verification possible
- Libation formula texts (11 occurrences across 5 sites) — best candidate for complete reading
- Commodity co-occurrence exploitation (43 POSSIBLE-confidence identifications)

---

## Blocker Escalation

Escalate to SSOT owner when:

1. Two artifacts claim conflicting current metrics
2. A proposed promotion lacks required evidence packet
3. A lane cannot satisfy a hard gate due to tool/data failure
