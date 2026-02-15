# APZa2 Parity Test: I-PI-NA-MA

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_apza2_i_pi_na_ma_parity_test.json`

## Objective

Task 2: Determine whether `APZa2` uses `I-PI-NA-MA` as the same semantic class as ritual-chain attestations, or as a contextual outlier/homograph risk.

## Core Comparison

Ritual-group occurrences (`n=5`, excluding `APZa2`):
- Directly precedes `SI-RU-TE`: `5/5`
- Next-token distribution: `SI-RU-TE` only
- Marker bundle presence: ritual-chain markers present

APZa2 profile (`n=1`):
- Sequence: `NA-SI I-PI-NA-MA I-KU-PA₃-NA-TU-NA-TE PI-MI-NA-TE I-NA-JA-RE-TA`
- Directly precedes `SI-RU-TE`: `No`
- Ritual marker bundle count: `0`
- Immediate context: `NA-SI -> I-PI-NA-MA -> I-KU-PA₃-NA-TU-NA-TE`

Set-similarity against ritual inscriptions:
- Only shared token is `I-PI-NA-MA`
- Jaccard range: `0.091` to `0.167`

## Decision

- Classification: `contextual_outlier_vs_ritual_chain`
- Same lexical item confidence: `medium`
- Homograph risk: `medium`

## Interpretation

`APZa2` does not behave like ritual-slot usage and is the main source of context dilution in current consistency metrics. It should be tracked as a potential secondary usage class until additional APZ-adjacent evidence resolves it.
