# Ritual Template Induction Memo

**Date**: 2026-03-15
**Agents**: G, G1, B1, Lead
**Lane**: G (reading attempts) + B (validation)
**Status**: DRAFT COMPLETE

---

## Purpose

Convert the current ritual/libation evidence into reusable formula templates that can guide further decipherment without overstating translation confidence.

Source analyses:

- `analysis/completed/inscriptions/IOZa9_READING.md`
- `analysis/completed/inscriptions/PKZa27_READING.md`
- `analysis/completed/inscriptions/SYZa2_READING.md`
- `analysis/completed/thematic/libation_formula_complete_reading.md`
- `analysis/active/2026-02-16_libation_formula_inflectional_paradigm.md`
- `analysis/active/2026-03-15_KA_NA_MICROSTUDY_1.md`
- `analysis/active/promotion_packets/I-PI-NA-MA.md`

Academic-overlap note:

The libation formula has substantial prior scholarship. This memo follows the repo’s existing practice: it treats Finkelberg, Davis, Thomas, and related work as prior art, and only advances template-level synthesis that the local project evidence supports.

---

## Executive Summary

The current ritual floor supports three operational templates:

1. **Abbreviated Form A libation core**
2. **Commodity-marked offering formula**
3. **Full-formula qualifier/closing frame**

The strongest stable facts are structural:

- `JA-SA-SA-RA-ME` and `U-NA-KA-NA-SI` form a reusable ritual core
- `SYZa2` proves the formula can absorb commodity logograms directly
- `I-PI-NA-MA` remains a HOLD-grade qualifier because cross-corpus consistency still fails

This means the ritual lane can scale by template induction now, but only if it keeps `I-PI-NA-MA` below promotion and distinguishes stable formula structure from weaker lexical interpretation.

---

## Template Set

### Template R1: Abbreviated Form A Libation Core

**Core evidence**:

- `IOZa9`
- `PKZa27`

Canonical shape:

```text
JA-SA-SA-RA-ME
U-NA-KA-NA-SI
```

Stable interpretation:

- formula position 2/4 sacred-name or sacred-object slot
- formula position 3/5 ritual action slot

Why it matters:

- this is the cleanest cross-site ritual frame in the active reading set
- it lets the project recognize partial libation texts even when the invocation and closing are absent

Current confidence:

- HIGH for formula membership
- PROBABLE for the action-family role of `U-NA-KA-NA-SI`

### Template R2: Commodity-Marked Offering Formula

**Core evidence**:

- `SYZa2`

Canonical shape:

```text
A-TA-I-*301-WA-JA
[word]-OLIV  quantity
U-NA-KA-NA-SI-OLE
[closing]
```

Stable interpretation:

- formula verb can carry offering commodities directly
- ritual and commodity notation are not fully segregated

Why it matters:

- this is the best current bridge between ritual language and administrative commodity logic
- it narrows the semantic field of the ritual action toward offering/provision behavior without forcing a full translation

Current confidence:

- HIGH for structure
- PROBABLE for offering-related action

### Template R3: Full Formula with Qualifier and Closing

**Core evidence**:

- `libation_formula_complete_reading.md`
- `2026-02-16_libation_formula_inflectional_paradigm.md`

Canonical shape:

```text
Position 1  invocation
Position 2  sacred/deity element
Position 3  ritual action family
Position 4  qualifier
Position 5  closing
```

Working position map:

- invocation: `A-TA-I-*301-WA-JA` / variant
- sacred element: `JA-SA-SA-RA-ME` / variant
- ritual action: `U-NA-KA-NA-SI` and related forms
- qualifier: `I-PI-NA-MA` / `I-PI-NA-MI-NA`
- closing: `SI-RU-TE` / `SI-RU`

Why it matters:

- it organizes partial inscriptions against a known full frame
- it gives the ritual lane a reusable segmentation model

Current confidence:

- HIGH for the existence of the frame
- mixed by position for lexical interpretation

---

## Position Assessments

### Stable positions

#### Ritual action family

Strongest stable claim:

- `KA-NA` is a real root family
- ritual branch is much stronger than the administrative standalone branch

This comes from:

- `U-NA-KA-NA-SI`
- `U-NA-KA-NA`
- `U-NA-RU-KA-NA-SI`
- `U-NA-RU-KA-NA-TI`
- `SE-KA-NA-SI`
- `U-NA-KA-NA-SI-OLE`

#### Sacred element

Strongest stable claim:

- `JA-SA-SA-RA-ME` is a formula-stable sacred element
- function is stronger than dictionary meaning

### Bounded positions

#### Qualifier: `I-PI-NA-MA`

Current state:

- board decision remains HOLD
- cross-corpus consistency still fails

Critical limits from the packet:

- positional consistency: `0.333`
- functional consistency: `0.417`
- gate required: `min >= 0.55 and max >= 0.70`

Operational consequence:

- keep `I-PI-NA-MA` in the formula map
- do not let it drive translation claims

#### Closing slot

Current stable claim:

- `SI-RU-TE` / `SI-RU` belongs to the formula closing layer

Current unstable claim:

- precise lexical meaning remains open

---

## Cross-Template Observations

### 1. The ritual lane now has a usable core without needing the full formula every time

`IOZa9` and `PKZa27` prove that the sacred element plus action family is enough to identify a ritual formula fragment.

### 2. `SYZa2` is the current bridge tablet

This remains the most important ritual control for translation work because it binds:

- formula action
- commodity logograms
- quantity

That is the cleanest current path from ritual structure toward semantic narrowing.

### 3. The project should separate formula stability from qualifier instability

The full formula frame is real. Not every position inside it is equally solved.

Most important distinction:

- `U-NA-KA-NA-SI` family = usable structural anchor
- `I-PI-NA-MA` = still bounded and weak

### 4. Register bridges should remain root-level unless the data genuinely improve

The best current bridge is still:

- root-level `KA-NA`

Not:

- full equivalence between standalone admin `KA-NA` and ritual derivatives

This is exactly where the ritual lane can go wrong if it starts translating ahead of the evidence.

---

## Operational Recommendations

1. Use Template R1 to identify and cluster partial libation fragments first.
2. Use Template R2 as the main semantic narrowing control for ritual translation.
3. Keep Template R3 as the segmentation frame for longer formula analysis.
4. Keep `I-PI-NA-MA` in evidence-review mode only.
5. Route any new ritual claim through the existing credibility boundary before updating confidence.

---

## Determination

The ritual lane is ready for template-guided expansion, but not for a broad qualifier breakthrough.

Immediate result:

- the formula core is stable enough to accelerate ritual analysis
- `SYZa2` remains the key bridge text
- `I-PI-NA-MA` stays HOLD
