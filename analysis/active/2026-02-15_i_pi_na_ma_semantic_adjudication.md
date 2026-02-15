# I-PI-NA-MA Semantic Adjudication

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_i_pi_na_ma_semantic_adjudication.json`

## Question

What semantic class is best supported for `I-PI-NA-MA` in the ritual chain?

## Key Evidence

Slot binding:
- Directly before `SI-RU-TE`: `5/7` (`0.714`)
- Attested substitution (`SE-KA-NA-SI`): `1` case

Distribution:
- Total occurrences: `6`
- Ritual ratio: `0.833`
- Site spread: `5` sites (`APZ, IOZ, KOZ, TLZ, VRYZ`)
- Administrative share: `0.000`

Onomastic signal (`tools/personal_name_analyzer.py --analyze I-PI-NA-MA`):
- Name probability: `0.45`
- Detection reason: `4 syllables; frequency 6; theophoric element MA`

Consistency and promotion:
- Positional consistency: `0.333`
- Functional consistency: `0.417`
- Promotion board status: `HOLD`
- Failed required gate: `cross_corpus_consistency`

## Posterior Ranking (Model Blend)

- `ritual_title_or_epithet`: `0.383`
- `personal_name`: `0.359`
- `verbal_predicate`: `0.171`
- `administrative_or_commodity_operator`: `0.087`

## Decision

- Best single model: `ritual_title_or_epithet`
- Resolution class: `unresolved_between_name_and_title`
- Working gloss: `ritual participant designation immediately before SI-RU-TE (name/title unresolved)`
- Recommendation: `retain_hold`

## Conditions To Clear HOLD

1. Add at least one more non-SYZ substitution in `SLOT -> SI-RU-TE`.
2. Raise functional consistency above the promotion gate threshold.
3. Test whether `APZa2` usage belongs to the same semantic class as ritual-chain usages.
