# Ritual Chain Master Snapshot (v2)

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_ritual_chain_master_snapshot.json`

## Scope

This snapshot consolidates corpus-level evidence for the ritual chain:

`JA-SA-SA-RA-ME -> U-NA-KA-NA(-SI) -> [I-PI-NA-MA | SE-KA-NA-SI] -> SI-RU-TE -> [extension?]`

Normalization rule used in this snapshot:
- Content tokens are hyphenated transliterations only.
- Line breaks, logograms, and numerals are removed for sequence modeling.

## Core Results

`SI-RU-TE` profile:
- Total occurrences: `7`
- Sites: `IOZ(3), KOZ(1), SYZ(1), TLZ(1), VRYZ(1)`
- Supports: `Stone vessel` only
- Preceding token distribution:
- `I-PI-NA-MA`: `5`
- `SE-KA-NA-SI`: `1`
- `<START>`: `1`
- Following token distribution:
- `<END>`: `5`
- `TA-NA-RA-TE-U-TI-NU`: `1`
- `I-DI`: `1`
- Terminal ratio: `5/7 = 0.714`
- Extension ratio: `2/7 = 0.286`

Ritual-chain inscription states (`n=9`):
- `full_chain`: `2`
- `slot_plus_terminal`: `4`
- `pre_terminal_chain`: `2`
- `terminal_only`: `1`

Formula evidence from `data/contextual_formulas_min2.json`:
- `I-PI-NA-MA SI-RU-TE`: `5` (libation-related)
- `JA-SA-SA-RA-ME U-NA-KA-NA-SI`: `3` (libation-related)
- `U-NA-KA-NA-SI I-PI-NA-MA`: `2` (libation-related)
- `U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE`: `2` (libation-related)

## Register Split Check

Administrative contrast token `A-DU`:
- Occurrences: `10`
- Sites: `HT(7), KH(2), TY(1)`
- Overlap with ritual-term set inscriptions: `0`

Result:
- Register separation remains supported (`A-DU` administrative; ritual chain non-administrative).

## Decipherment Impact

1. The ritual chain is now structurally stable enough to treat as a reusable sequence model, not isolated tablet-specific text.
2. The primary unresolved variable remains slot semantics for `I-PI-NA-MA`.
3. The `SI-RU-TE` terminal behavior is robust outside IOZ and conditionally extended inside IOZ.
