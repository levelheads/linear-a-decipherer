# v0.12.0 Release Notes

**Date**: 2026-03-15
**Release**: Operation VENTRIS Week 2

## Scope

This is a bounded research snapshot.

- Linear A remains undeciphered.
- This release does **not** claim full decipherment, full translation, or final language identification.
- It packages validated progress: stronger tooling, stronger governance, seven new bounded connected readings, repaired promotion flow for `NI`, and clearer handling of weak or unresolved cases.

## What Is New

- `NI` promotion flow repaired in `promotion_board_runner.py`; `NI` is now approved at `HIGH`.
- Two new execution/governance tools:
  - `tools/sprint_orchestrator.py`
  - `tools/project_acceleration_review.py`
- Seven new bounded connected readings:
  - `HT2`
  - `KNZb27`
  - `PH12c`
  - `KH15`
  - `KH54`
  - `KH25`
  - `ZA4b`
- New template and blocker-control documentation for admin, ritual, KH, and HTW workstreams.
- `PH25` explicitly documented as a reserve case rather than forced into a low-credibility reading.

## Metrics

- Tools: `62`
- Connected readings: `62 tablets + 14 thematic`
- Sites with connected readings: `10`
- Cross-site readings: `36`

## Prior-Art and Originality Guard

This release intentionally separates prior scholarship from project-native contributions.

Prior scholarship retained and credited:

- `ku-ro`, `ki-ro`, major toponyms, and established deity identifications
- libation-formula scholarship by Finkelberg, Davis, and Thomas
- corpus publication and sign references grounded in GORILA and linked corpus sources

Project-native contributions in this release:

- repo-native sprint/review workflow
- repaired `NI` promotion pipeline and approval packet handling
- new bounded connected readings and hold decisions
- subsystem/blocker formalization for KH and HTW materials
- release/governance framing that prevents overstated claims

## Boundaries

The following remain explicitly unresolved or bounded:

- `I-PI-NA-MA` remains `HOLD`
- `PH25` remains reserve-only
- `*188`, `*188-DU`, `*86-RO`, and related blocker families are structural/control results, not lexical promotions
- ritual translation remains template-level except where direct evidence supports more

## Verification

- `pytest -q`
- `python3 tools/master_state_guard.py`
- `python3 tools/release_gate.py --tag v0.12.0`

## Full Changelog

See [CHANGELOG.md](CHANGELOG.md).
