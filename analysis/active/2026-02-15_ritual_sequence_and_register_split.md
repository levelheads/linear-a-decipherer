# Targeted Results Analysis: Ritual Sequence Cluster and Register Split

**Date**: 2026-02-15
**Scope**: `A-DU`, `SI-RU-TE`, `I-PI-NA-MA` and adjacent ritual-sequence terms
**Goal**: Produce decipherment-facing results (not tooling work) from current corpus evidence.

---

## Methods Run

```bash
python3 tools/corpus_lookup.py "A-DU" --report
python3 tools/corpus_lookup.py "SI-RU-TE" --report
python3 tools/corpus_lookup.py "I-PI-NA-MA" --report
python3 tools/corpus_lookup.py "U-NA-KA-NA-SI" --report
python3 tools/corpus_lookup.py "JA-SA-SA-RA-ME" --report
python3 tools/hypothesis_tester.py --word "A-DU"
python3 tools/hypothesis_tester.py --word "SI-RU-TE"
python3 tools/hypothesis_tester.py --word "I-PI-NA-MA"
python3 tools/contextual_analyzer.py --analyze formulas --min-formula-length 2 --min-formula-occurrences 2 --output data/contextual_formulas_min2.json
python3 tools/analyze_inscription.py IOZa2
python3 tools/analyze_inscription.py KOZa1
python3 tools/analyze_inscription.py TLZa1
python3 tools/corpus_auditor.py --function-word "*304"
python3 tools/corpus_auditor.py --function-word "*21F"
python3 tools/corpus_auditor.py --function-word "*118"
```

---

## Result 1: Strong Ritual Sequence Cluster

### Core sequence evidence

From formula mining (`data/contextual_formulas_min2.json`):

- `I-PI-NA-MA SI-RU-TE`: **5** occurrences, flagged `is_libation_related=True`
- `U-NA-KA-NA-SI I-PI-NA-MA`: **2** occurrences, `is_libation_related=True`
- `U-NA-KA-NA-SI I-PI-NA-MA SI-RU-TE`: **2** occurrences, `is_libation_related=True`
- `JA-SA-SA-RA-ME U-NA-KA-NA-SI`: **3** occurrences, `is_libation_related=True`

### Co-occurrence and ordering

Inscription-level counts:

- `I-PI-NA-MA` and `SI-RU-TE` co-occur in **5** inscriptions.
- In all **5/5**, `I-PI-NA-MA` precedes `SI-RU-TE`.
- In all **5/5**, they appear as direct adjacency after separator removal.

### Cross-site distribution

- `I-PI-NA-MA`: IOZ, KOZ, TLZ, VRYZ, APZ (5 sites)
- `SI-RU-TE`: IOZ, KOZ, TLZ, SYZ, VRYZ (5 sites)
- Shared ritual-set inscriptions include IOZa2, IOZa15, KOZa1, TLZa1, VRYZa1.

### Interpretation

This is not random co-occurrence. The sequence behavior is formulaic and stable enough to treat as a **ritual register unit**:

`JA-SA-SA-RA-ME -> U-NA-KA-NA(-SI) -> I-PI-NA-MA -> SI-RU-TE`

Working interpretation:

- `SI-RU-TE`: likely a terminal formula element (line-final/closure behavior).
- `I-PI-NA-MA`: likely the directly bound element before `SI-RU-TE` (candidate name/title/epithet slot).

---

## Result 2: `A-DU` Belongs to a Different Register

### Distribution/profile

- Total occurrences: **10**
- Sites: HT (7), KH (2), TY (1)
- Positional behavior (content tokens): **7/10 initial**, 0 final
- Following-token profile: **7 logogram/symbol**, 3 syllabic, 0 direct numeric after separator removal

### Separation from ritual cluster

Inscription-level overlap with ritual cluster terms (`A-TA-I-*301-WA-JA`, `JA-SA-SA-RA-ME`, `U-NA-KA-NA-SI`, `I-PI-NA-MA`, `SI-RU-TE`):

- `A-DU` co-occurrence with all listed ritual terms: **0**

### Interpretation

`A-DU` behaves like an **administrative line-initial operator/header token**, not a ritual sequence token.
The data supports a register split:

- Ritual cluster: IOZ/KOZ/TLZ/VRYZ/SYZ style formula texts
- Administrative cluster: HT/KH/TY commodity/logogram contexts

---

## Result 3: Sign-Asymmetry Checks (Lane C Priority Signs)

From `corpus_auditor.py --function-word`:

- `*304`: 25 occurrences, **84.0% initial**, entropy 0.400, numeric neighbors frequent
  -> strong header/topic marker behavior
- `*21F`: 4 occurrences, **75.0% initial**
  -> same direction, low sample
- `*118`: 3 occurrences, **66.7% initial**
  -> same direction, low sample

Interpretation: `*304` is currently the strongest sign-level structural result in this set.

---

## Result 4: Terminal-Marker Behavior Around `SI-RU-TE`

Targeted lookup for possible terminal alternatives:

- `TA-NA-RA-TE-U-TI-NU`: 1 occurrence (IOZa2), directly after `SI-RU-TE`
- `I-DI`: 1 occurrence (IOZa14), directly after `SI-RU-TE`

`SI-RU-TE` next-token distribution (content tokens):

- `<END>`: **5**
- `TA-NA-RA-TE-U-TI-NU`: **1**
- `I-DI`: **1**

Interpretation:

- `SI-RU-TE` is primarily terminal, but in IOZ it can introduce a second terminal segment.
- `TA-NA-RA-TE-U-TI-NU` and `I-DI` behave as likely **post-`SI-RU-TE` supplements** rather than independent openers.

---

## Confidence Impact

1. `SI-RU-TE`: keep at **PROBABLE** with explicit note that it is a ritual terminal formula component.
2. `A-DU`: keep at **PROBABLE** with explicit note of administrative/header behavior and mixed context risk.
3. `I-PI-NA-MA`: keep **HOLD** for promotion pending stronger functional-consistency evidence, but treat as a high-priority ritual slot candidate due deterministic pairing with `SI-RU-TE`.

---

## Immediate Next Decipherment Experiments

1. **Ritual-slot test**: classify whether `I-PI-NA-MA` is name/title by comparing suffix behavior against high-probability anthroponyms at the same sites.
2. **Terminal-marker test**: evaluate `SI-RU-TE` against other line-final ritual forms (`TA-NA-RA-TE-U-TI-NU`, `I-DI`) for substitution/complementarity.
3. **Register contrast test**: formal A/B comparison of `A-DU` vs `SA-RA₂` and `KU-RO` in immediate-right context class (logogram, numeric, syllabic) to refine administrative function.
