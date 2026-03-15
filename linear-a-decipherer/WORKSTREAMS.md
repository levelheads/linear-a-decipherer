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

## Sprint Execution

Month-scale research sprints should route through the sprint manifest and orchestrator:

```bash
python3 tools/sprint_orchestrator.py --week 1 --phase baseline --run-lanes --dry-run
python3 tools/sprint_orchestrator.py --week 1 --phase baseline --run-lanes
```

Default sprint manifest: `config/month1_decipherment_manifest.yaml`

Current Month 1 execution profile (2026-03-15):
- `55%` admin translation expansion
- `35%` ritual/register deepening
- `10%` bounded breakthrough hunting

Current week-2 slate:
- Admin primary: `HT2`, `KNZb<27>`, `HTWb229`, `PYR2`, `KHWa1013`, `PH12c`
- Admin reserve: `KH15`, `KH25`, `KH54`, `HT46b`, `ZA4b`, `PH25`
- Ritual primary: `IO formula set`, `PK formula set`, `SY formula set`, `I-PI-NA-MA evidence review`
- Breakthrough micro-study 1: `KA-NA` prefix alternations and formula reuse

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

### Lane G: Reading Attempts — ACTIVE (2026-03-14)

**Mission**: Produce connected readings of specific tablets using all accumulated evidence.

**Rationale**: The project has answered the language question as well as it can without a breakthrough: isolate substrate with Luwian morphological influence and Semitic administrative loans. The strategic pivot moves from "which language is it?" to "what do these texts say?"

**Current status (v0.12.0)**: 62 tablet readings + 14 thematic analyses completed across 10 sites (HT, ZA, PEZ, IO, PH, SAMW, PK, KH, SY, KN). First formal grammar sketch produced. Libation formula upgraded to POSSIBLE, `NI` is approved at HIGH, and the week-2 reading/template block is now repo-native.

**Week-2 progress (2026-03-15)**: `HT2`, `KNZb<27>`, `PH12c`, `KH15`, `KH54`, `KH25`, and `ZA4b` are now completed connected readings; KH formalization, blocker-routing, `KA-NA` micro-study, KH `*86-RO` subsystem work, KH control-object comparison, KH support-ecology checking, the `HTWb229` warehouse-classifier note, the HTW slot-order memo, the HTW `KA` vs `*188-DU` comparison, a week-2 credibility verification memo, a portfolio-based breakthrough brief, explicit admin and ritual template-induction memos, a `PH25` reserve note, and a staged conservative next-block reading queue all now have active outputs.

**Automated workflow** (4 new VENTRIS tools):
1. `reading_pipeline.py --select --top 20 --site-balanced` — SELECT candidates
2. `reading_pipeline.py --prepare TABLET_ID` — PREPARE reading brief
3. [Human analysis using the reading brief] — READ
4. `cascade_opportunity_detector.py --word NEW_WORD --confidence LEVEL` — RECORD + cascade

**Supporting tools**:
- `personnel_dossier_builder.py` — Cross-tablet name tracking (111 profiled names)
- `sign_value_extractor.py` — Arithmetic-driven sign value constraints from VERIFIED tablets

**Priority targets**:
- Tier 3 HT readings (remaining high-readiness tablets)
- NI cascade exploitation (APPROVED at HIGH; 535 threshold crossers queued for follow-on work)
- Cross-site deepening (IO, PK, SY religious register analysis)
- CYP grading system formalization across KH corpus

---

## Blocker Escalation

Escalate to SSOT owner when:

1. Two artifacts claim conflicting current metrics
2. A proposed promotion lacks required evidence packet
3. A lane cannot satisfy a hard gate due to tool/data failure
