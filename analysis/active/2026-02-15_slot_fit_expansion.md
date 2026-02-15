# Expanded Substitution Search: Pre-`SI-RU-TE` Slot

**Date**: 2026-02-15
**Objective**: Broaden the pre-`SI-RU-TE` substitution search and rank ritual candidates by slot-fit.

---

## Method

We ran a constrained slot-fit model over ritual inscriptions only.

Ritual set definition:

- Inscriptions containing `SI-RU-TE`, or
- Inscriptions containing at least two markers from:
  - `A-TA-I-*301-WA-JA`
  - `JA-SA-SA-RA-ME`
  - `U-NA-KA-NA-SI` / `U-NA-KA-NA`
  - `SI-RU-TE`

Features used in score:

1. Direct pre-`SI-RU-TE` occupancy
2. Occurrence after `U-NA-KA-NA(-SI)`
3. Chain participation after `JA-SA-SA-RA-ME`
4. Ritual ratio (ritual-occurrence / total-occurrence)
5. Site spread
6. Administrative contamination penalty

Machine output: `analysis/active/2026-02-15_slot_fit_candidates.json`

---

## Core Slot Facts

`SI-RU-TE` predecessor distribution:

- `I-PI-NA-MA`: **5**
- `SE-KA-NA-SI`: **1**
- `<START>`: **1**

`SI-RU-TE` successor distribution:

- `<END>`: **5**
- `TA-NA-RA-TE-U-TI-NU`: **1**
- `I-DI`: **1**

---

## Ranked Candidates (v2)

1. `I-PI-NA-MA`
- slot-fit score: **0.975**
- pre-`SI-RU-TE`: **5**
- after `U-NA-KA-NA(-SI)`: **3**
- ritual ratio: **0.83**
- sites: **5**

2. `SE-KA-NA-SI`
- slot-fit score: **0.250**
- pre-`SI-RU-TE`: **1**
- ritual ratio: **1.00**
- sites: **1**

3. `U-NA-KA-NA-SI`
- slot-fit score: **0.330** (chain anchor, not direct slot filler)
- pre-`SI-RU-TE`: **0**
- after `JA-SA-SA-RA-ME`: **3**
- ritual ratio: **1.00**

Interpretation:

- `I-PI-NA-MA` remains the dominant slot occupant by a large margin.
- `SE-KA-NA-SI` is the only attested direct substitution candidate so far.
- `U-NA-KA-NA-SI` is structurally upstream in the ritual chain, not a direct replacement.

---

## Candidate Diagnostics

### `SE-KA-NA-SI`

Attestation:

- `SYZa3`: `A-TA-I-*301-WA-JA SE-KA-NA-SI SI-RU-TE`

Name-analyzer signal:

- Name probability: 50%
- Suffix `-SI` and theophoric-like pattern

Status: **valid substitution candidate (singleton evidence)**.

### `I-PI-NA-MA`

Attestations:

- 6 total, 5 directly before `SI-RU-TE`

Name-analyzer signal:

- Name probability: 45%

Status: **primary slot anchor candidate**.

---

## Decipherment Consequence

The pre-`SI-RU-TE` slot now has a defensible two-candidate model:

1. Primary filler: `I-PI-NA-MA`
2. Rare variant filler: `SE-KA-NA-SI`

This supports a slot semantics of **ritual participant/designation** rather than commodity/accounting term.

---

## Next Evidence Tasks

1. Target low-frequency ritual inscriptions for additional `... X SI-RU-TE` instances to test whether `SE-KA-NA-SI` expands beyond SYZ.
2. Compare suffix morphology in slot fillers (`-MA`, `-SI`) against broader anthroponym inventories by site.
3. Build a strict finite-state sequence test for:
   `A-TA-I-*301-WA-JA -> JA-SA-SA-RA-ME -> U-NA-KA-NA(-SI) -> SLOT -> SI-RU-TE -> EXTENSION?`
