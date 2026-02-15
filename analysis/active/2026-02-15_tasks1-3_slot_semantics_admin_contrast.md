# Results Sprint: Tasks (1) to (3)

**Date**: 2026-02-15
**Focus**: Decipherment results only (ritual slot substitution, SI-RU-TE semantic model, administrative contrast)

---

## Task 1: Ritual-Slot Substitution Test (`I-PI-NA-MA`)

### Question

Does `I-PI-NA-MA` occupy a stable ritual slot that can be substituted by other candidate name/title tokens?

### Evidence

For all `SI-RU-TE` occurrences (content-token normalized):

- Total `SI-RU-TE`: **7**
- Preceding token distribution:
  - `I-PI-NA-MA`: **5**
  - `SE-KA-NA-SI`: **1**
  - `<START>`: **1**

Detailed rows:

- IOZa2: `U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE TA-NA-RA-TE-U-TI-NU`
- IOZa15: `I-PI-NA-MA SI-RU-TE`
- KOZa1: `U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE`
- TLZa1: `U-NA-KA-NA I-PI-NA-MA SI-RU-TE`
- VRYZa1: `I-PI-NA-MA SI-RU-TE`
- SYZa3: `A-TA-I-*301-WA-JA SE-KA-NA-SI SI-RU-TE`
- IOZa14: `SI-RU-TE I-DI`

Formula mining (`data/contextual_formulas_min2.json`) confirms:

- `I-PI-NA-MA SI-RU-TE`: **5** occurrences (`is_libation_related=True`)
- `U-NA-KA-NA-SI I-PI-NA-MA`: **2**
- `U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE`: **2**

### Interpretation

- `I-PI-NA-MA` is the dominant occupant of the pre-`SI-RU-TE` slot.
- `SE-KA-NA-SI` is a plausible substitution candidate in the same slot (currently singleton evidence).
- This supports a **name/title slot hypothesis** for `I-PI-NA-MA`, but with unresolved ambiguity between anthroponym vs epithet/function.

### Confidence move

- Keep `I-PI-NA-MA` as **high-priority HOLD** (evidence-rich but function still mixed in validators).

---

## Task 2: Constrained Semantic Model for `SI-RU-TE`

### Question

Can `SI-RU-TE` be modeled as a terminal ritual marker with optional IOZ-specific extension terms?

### Evidence

`SI-RU-TE` next-token distribution:

- `<END>`: **5**
- `TA-NA-RA-TE-U-TI-NU`: **1** (IOZa2)
- `I-DI`: **1** (IOZa14)

Site spread of `SI-RU-TE`: IOZ, KOZ, SYZ, TLZ, VRYZ (5 sites).
Direct attestations show terminal behavior outside IOZ and extension behavior inside IOZ.

### Constrained model

```text
RitualCore := [A-TA-I-*301-WA-JA] [JA-SA-SA-RA-ME] [U-NA-KA-NA(-SI)] [I-PI-NA-MA|SE-KA-NA-SI] SI-RU-TE [Extension]
Extension := <END> | TA-NA-RA-TE-U-TI-NU | I-DI
Constraint: TA-NA-RA-TE-U-TI-NU and I-DI are currently IOZ-only after SI-RU-TE.
```

### Interpretation

- `SI-RU-TE` is best treated as a **terminal marker** with optional, low-frequency post-terminal supplements.
- Current evidence does not support reading `TA-NA-RA-TE-U-TI-NU` or `I-DI` as independent primary closures.

### Confidence move

- Keep `SI-RU-TE` at **PROBABLE**, add explicit note: “terminal ritual component with IOZ extension variants.”

---

## Task 3: Administrative Contrast (`A-DU` vs `SA-RA₂` vs `KU-RO`)

### Question

Do immediate-right contexts distinguish administrative functions for `A-DU`, `SA-RA₂`, and `KU-RO`?

### Evidence summary

#### `A-DU` (10 occurrences)

- Position: initial 7, medial 3, final 0
- Right-class distribution:
  - logogram/symbol: **70.0%**
  - syllabic: **30.0%**
  - number: **0%**

#### `SA-RA₂` (20 occurrences)

- Position: medial 18, initial 2
- Right-class distribution:
  - logogram/symbol: **90.0%**
  - number: **5.0%**
  - end: **5.0%**
  - syllabic: **0%**

#### `KU-RO` (37 occurrences)

- Position: medial 36, initial 1
- Right-class distribution:
  - number: **78.4%**
  - logogram/symbol: **18.9%**
  - syllabic: **2.7%**

Pairwise right-class deltas (percentage points):

- `A-DU` vs `KU-RO`: logogram/symbol **+51.1**, number **-78.4**
- `KU-RO` vs `SA-RA₂`: number **+73.4**, logogram/symbol **-71.1**
- `A-DU` vs `SA-RA₂`: syllabic **+30.0**

### Interpretation

- `KU-RO` is quantitatively a **numeric-total operator** (strong number-right profile).
- `SA-RA₂` is a **commodity-linking administrative term** (dominant logogram-right profile, HT-specific).
- `A-DU` patterns with administrative starts and mixed right neighbors, indicating a likely **header/operator role** rather than totaling role.

---

## Net Decipherment Conclusions

1. Ritual register chain is structurally robust across multiple non-HT sites.
2. `I-PI-NA-MA` is strongly slot-bound before `SI-RU-TE` and remains the key unresolved lexical target.
3. `SI-RU-TE` is best modeled as terminal ritual marker with rare IOZ-specific extensions.
4. `A-DU` belongs to the administrative register and should not be merged semantically with ritual-slot terms.

---

## Immediate Result-Driven Next Steps

1. Expand substitution search for pre-`SI-RU-TE` slot candidates beyond `SE-KA-NA-SI` (site-filtered ritual corpus only).
2. Build a dedicated IOZ extension inventory after `SI-RU-TE` to test whether extension terms correlate with support type or line position.
3. Run a controlled comparison of `A-DU` against additional administrative tokens (`I-DA`, `DA-KA`, `SA-RU`) using the same right-class protocol.
