# SI-RU-TE Terminal Model v2

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_terminal_model_v2.json`

## Summary

`SI-RU-TE` is best modeled as a terminal ritual marker with IOZ-conditioned extensions.

Global transition distribution (`n=7`):
- `<END>`: `5`
- `TA-NA-RA-TE-U-TI-NU`: `1`
- `I-DI`: `1`

Probabilities:
- Terminal end probability: `0.714`
- Extension probability: `0.286`

## Conditional Behavior

Conditioned on preceding token:
- Preceded by `I-PI-NA-MA` (`n=5`):
- `<END>`: `4`
- `TA-NA-RA-TE-U-TI-NU`: `1`
- Preceded by `SE-KA-NA-SI` (`n=1`):
- `<END>`: `1`
- Preceded by `<START>` (`n=1`):
- `I-DI`: `1`

Site-conditioned behavior:
- IOZ (`n=3`):
- Terminal end: `1` (`0.333`)
- Extensions: `TA-NA-RA-TE-U-TI-NU(1)`, `I-DI(1)`
- Non-IOZ (`n=4`):
- Terminal end: `4` (`1.000`)
- Extensions: none

## Constrained Grammar

Core:
- `[A-TA-I-*301-WA-JA]? [JA-SA-SA-RA-ME]? [U-NA-KA-NA-SI|U-NA-KA-NA]? [I-PI-NA-MA|SE-KA-NA-SI]? SI-RU-TE`

Extension:
- `<END> | TA-NA-RA-TE-U-TI-NU | I-DI`

Constraints:
- `TA-NA-RA-TE-U-TI-NU` and `I-DI` are currently attested only at IOZ.
- Outside IOZ, `SI-RU-TE` is always terminal.

## Decipherment Impact

1. Treat `SI-RU-TE` as the closure anchor of the ritual chain.
2. Model post-`SI-RU-TE` material as extension layer, not alternate closure heads.
