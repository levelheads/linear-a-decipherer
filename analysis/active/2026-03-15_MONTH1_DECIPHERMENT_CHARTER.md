# Month 1 Decipherment Charter

**Date**: 2026-03-15  
**Sprint Manifest**: `config/month1_decipherment_manifest.yaml`  
**Execution Tool**: `tools/sprint_orchestrator.py`  
**Canonical state**: `linear-a-decipherer/MASTER_STATE.md`

## Objective

Implement the first month of the current decipherment push as an evidence-first multi-agent sprint. The target is not a publicity-grade "Linear A solved" claim. The target is a defensible decipherment candidate for the administrative core plus ritual/libation register, with explicit unresolved areas and promotion-board-backed confidence discipline.

## Evidence Floor

The sprint starts from the current validated project state:

- 1,721 inscriptions processed with 98.66% batch analysis coverage
- 55 connected readings plus 14 thematic analyses
- Active lanes already established for governance, validation, script asymmetry, throughput, and reading attempts
- NI promotion path repaired and approved at HIGH via lane B on 2026-03-15
- Reading queue and cascade tooling already available and now elevated to sprint-critical artifacts

## Agent Team

- **Agent A, Corpus/Governance**: SSOT integrity, index refresh, sprint reporting
- **Agent B, Validation/Promotion**: validator runs, packet review, promotion holds
- **Agent C, Script Asymmetry**: unblock `*304`, `*21F/*21M`, `*118`, `*188`, `*86`
- **Agent D, Language Layering**: maintenance-only stress tests when new evidence demands it
- **Agent E, Throughput/Queue**: coverage, site balancing, cascade routing
- **Agent F, Administrative Reading Team**: connected admin readings
- **Agent G, Ritual Reading Team**: libation/ritual sequence deepening
- **Lead Synthesizer**: weekly synthesis and month-end decipherment dossier

## Week 1 Lock

Week 1 is for queue lock, NI adjudication, and baseline hardening. The sprint should open with:

1. `python3 tools/sprint_orchestrator.py --week 1 --phase baseline --run-lanes`
2. `python3 tools/sprint_orchestrator.py --week 1 --phase sync --dry-run`
3. `python3 tools/sprint_orchestrator.py --week 1 --phase promotion --dry-run`

### Locked queue seed

The current site-balanced queue seed is:

1. `HT2`
2. `KNZb<27>`
3. `HTWb229`
4. `PYR2`
5. `KHWa1013`
6. `KNWc48`
7. `KYZa2`
8. `MAZb8`
9. `NEZa1`
10. `PH12c`

These targets come from the current `reading_pipeline.py --select --top 20 --site-balanced` output and should remain the default week-1 slate unless lane B blocks one for evidence reasons.

### NI leverage

The current NI cascade snapshot is the strongest immediate leverage move in the repo:

- 67 direct tablets
- 727 transitive cascade tablets
- 794 tablets with readiness gain
- 535 tablets crossing the 0.5 readability threshold

Top immediate threshold crossers include `KH15`, `KH25`, `KH54`, `HT46b`, `HT50b`, `HT154g`, `ZA4b`, `PH25`, and `ZA28`. This is why NI promotion or formal hold was the first sprint decision.

### Status update (2026-03-15)

Lane B has now approved `NI` at `HIGH` using commodity-anchor evidence. The week-1 bottleneck shifts from packet repair to exploiting the `535` threshold crossers and routing the strongest administrative tablets into week-2 reading throughput.

## Weekly Cadence

- **Monday**: baseline refresh and queue lock
- **Wednesday**: blocker sync and lane rerouting
- **Friday**: promotion board and week close-out

Every weekly update should use `templates/SPRINT_WEEKLY_UPDATE_TEMPLATE.md` and attach:

- queue artifact
- cascade artifact
- validation artifact set
- lane handoff JSON

## Month-End Deliverables

- Month-end decipherment dossier in `analysis/completed/thematic/`
- Updated `MASTER_STATE.md`, `KNOWLEDGE.md`, and `ANALYSIS_INDEX.md`
- Promotion packet decisions for month-critical candidates
- Resolved / partially resolved / unresolved map for the administrative and ritual registers

## Guardrails

- No claim bypasses `METHODOLOGY.md`
- No promotion proceeds without lane B artifacts
- Lane D remains maintenance-only unless new evidence creates a contradiction
- Ritual sentence claims stay below the evidence floor if week-3 work does not improve them enough
- Site balancing remains mandatory; do not drift back into HT-only convenience work
