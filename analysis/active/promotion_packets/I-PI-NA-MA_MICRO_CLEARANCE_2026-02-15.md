# Promotion Packet: I-PI-NA-MA (Micro Clearance)

**Date**: 2026-02-15
**Primary threshold artifact**: `analysis/active/2026-02-15_i_pi_na_ma_promotion_thresholds.json`

## 1. Current Gate State

- Board status: `HOLD`
- Failed required gate: `cross_corpus_consistency`
- Cross-corpus rule: `min(positional,functional)>=0.55 and max(positional,functional)>=0.70`
- Current metrics:
- Positional consistency: `0.333`
- Contextual consistency: `0.500`
- Functional consistency: `0.417`

## 2. New Supporting Evidence (This Sprint)

- Slot fit v3 (`analysis/active/2026-02-15_slot_fit_candidates_v3.json`):
- `I-PI-NA-MA` score `0.880`
- Direct pre-`SI-RU-TE`: `5/7`
- APZa2 parity test (`analysis/active/2026-02-15_apza2_i_pi_na_ma_parity_test.json`):
- Classified as contextual outlier vs ritual chain
- Homograph risk: `medium`
- Non-SYZ substitution hunt (`analysis/active/2026-02-15_non_syz_slot_substitution_hunt.json`):
- No additional non-SYZ substitution filler found

## 3. Clearance Scenarios

Scenario A: Keep all attestations as one lexical class
- Minimum new aligned ritual attestations required to pass gate: `6`

Scenario B: Split APZa2 as contextual homograph, then retest ritual class
- Minimum new aligned ritual attestations required to pass gate: `4`

## 4. Board Resubmission Criteria

Required before re-running promotion:
1. Meet one of the two quantitative thresholds above (`6` or `4`, depending on APZa2 handling).
2. Add at least one new non-SYZ substitution candidate before `SI-RU-TE` with `X != I-PI-NA-MA`.
3. Re-run `corpus_consistency_validator` and `promotion_board_runner` and attach updated gate evidence line.

## 5. Recommendation

Do not re-open promotion now. Prioritize corpus expansion and ritual-slot discovery, then re-submit with the threshold checklist satisfied.
