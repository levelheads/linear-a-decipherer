# Non-SYZ Slot Substitution Hunt

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_non_syz_slot_substitution_hunt.json`

## Objective

Task 1: Find additional non-SYZ direct fillers for the pre-`SI-RU-TE` slot.

## Method

- Re-scanned all `SI-RU-TE` attestations with content-token normalization.
- Extracted predecessor token for each `SI-RU-TE` occurrence.
- Split predecessor distributions into `SYZ` vs non-`SYZ`.
- Ran near-miss scan for `*-RU-TE` variants excluding `SI-RU-TE`.

## Results

`SI-RU-TE` total occurrences: `7`

Predecessor distribution (all):
- `I-PI-NA-MA`: `5`
- `SE-KA-NA-SI`: `1`
- `<START>`: `1`

Predecessor distribution (non-SYZ):
- `I-PI-NA-MA`: `5`
- `<START>`: `1`

Predecessor distribution (SYZ):
- `SE-KA-NA-SI`: `1`

Variant scan:
- `*-RU-TE` hits excluding `SI-RU-TE`: `0`

## Decision

- No new non-SYZ substitution filler was found.
- Current substitution model is unchanged:
1. Primary: `I-PI-NA-MA`
2. Singleton variant: `SE-KA-NA-SI` (SYZ only)

## Immediate Implication

The promotion blocker for `I-PI-NA-MA` cannot be solved by existing corpus substitution evidence alone; new attestations are required.
