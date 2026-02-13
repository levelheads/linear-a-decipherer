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
| D | Language asymmetry | Hypothesis and Bayesian outputs | Language-layer updates | Integrated validator + negative evidence |
| E | Throughput engine | Corpus queue + site balancing rules | Expanded coverage and deep-dives | Coverage report and site-bias note |
| F | Release/process | Tags, CITATION, changelog, SSOT | Release candidate package | Strict CI + release gate pass |

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

## Blocker Escalation

Escalate to SSOT owner when:

1. Two artifacts claim conflicting current metrics
2. A proposed promotion lacks required evidence packet
3. A lane cannot satisfy a hard gate due to tool/data failure
