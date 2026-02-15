# Ritual Chain Decision Summary

**Date**: 2026-02-15
**Scope**: Execute analysis tasks focused on decipherment outcomes (not tooling polish)

## Decisions Locked

1. `SI-RU-TE` stays `PROBABLE` and is treated as terminal chain anchor with IOZ-only extension layer.
2. `I-PI-NA-MA` stays `HOLD` for promotion despite strong slot evidence, because cross-corpus consistency gate still fails.
3. `SE-KA-NA-SI` is accepted as a real but singleton slot substitution candidate.
4. `U-NA-KA-NA(-SI)` remains upstream chain anchor, not direct slot filler.
5. Administrative token `A-DU` remains separate from ritual register (no overlap in attestations).

## What This Changes Immediately

1. The ritual chain should now be analyzed as a constrained sequence with one dominant slot and one rare variant.
2. IOZ extensions after `SI-RU-TE` should be handled as conditioned branch behavior, not baseline grammar.
3. Promotion effort should focus on resolving `I-PI-NA-MA` semantics, not revisiting already stable register splits.

## Next High-Impact Tasks

1. Run targeted wildcard search for additional slot substitutions:
- Pattern frame: `* SI-RU-TE` in ritual-like inscriptions
- Priority sites: non-SYZ stone-vessel corpus first

2. Perform APZa2 parity test for `I-PI-NA-MA`:
- Compare left/right context class against ritual-chain `I-PI-NA-MA` attestations
- Decide whether APZa2 is same lexical item or homograph

3. Build micro-promotion packet for `I-PI-NA-MA`:
- Include new slot-fit v3 scorecard
- Include adjudication posterior and explicit HOLD-clearing criteria
- Define minimum evidence threshold for moving from HOLD to APPROVE
