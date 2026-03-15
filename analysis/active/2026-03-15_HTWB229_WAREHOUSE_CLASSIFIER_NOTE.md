# HTWb229 Warehouse-Classifier Note

**Date**: 2026-03-15
**Agents**: C, C2, Lead
**Lane**: C (script asymmetry) with warehouse support
**Status**: DRAFT COMPLETE

---

## Executive Summary

`HTWb229` is now best treated as part of the HTW warehouse classifier chain rather than as a standalone translation problem.

The current evidence cluster is coherent:

1. `HTWb229` reads `*188 CYP+D`.
2. `CYP+D` is directly attested in HTW warehouse context in only two places: `HTWb229` and `HTWc<3018>`.
3. The stronger chain signal comes from `HTWeWc3020`, where `*188-DU` directly precedes `*304+PA-CYP+D`.

That pattern makes `HTWb229` useful as a structural control for the warehouse-grade system, but it does not yet justify a connected reading or lexical promotion of `*188`.

---

## Evidence Base

### Live corpus checks

- `python3 tools/corpus_lookup.py '*188' --exact`
- `python3 tools/corpus_lookup.py '*188-DU' --exact`
- `python3 tools/corpus_lookup.py 'CYP+D' --exact --site HTW`
- `python3 tools/corpus_lookup.py '*304+PA-CYP+D' --exact`

### Prior analysis

- `analysis/active/2026-03-15_WEEK2_BLOCKER_ROUTING_MEMO.md`
- `analysis/active/2026-02-17_star304_morphological_analysis.md`

---

## Attestation Summary

### `HTWb229`

Raw text:

```text
*188  CYP+D
```

### Wider `*188` family

Standalone `*188` occurs nine times:

- `HT15`
- `HT56a`
- `HT98b`
- `HT103`
- `HT123+124b`
- `HTW231b`
- `HTWb229`
- `HTWc3009`
- `HTWc3013`

Distribution is HT + HTW, with a strong administrative profile and no stable lexical reading.

### `*188-DU` chain

`*188-DU` occurs three times:

- `HT123+124b`
- `HTWa1021`
- `HTWeWc3020`

The most informative case is:

```text
HTWeWc3020: *188-DU  *304+PA-CYP+D
```

This shows the `*188` family directly adjacent to a warehouse commodity-grade compound.

### HTW `CYP+D` controls

Within HTW, `CYP+D` appears only in:

- `HTWb229`: `*188 CYP+D`
- `HTWc<3018>`: `KA CYP+D`

And the expanded HTW warehouse compound appears in:

- `HTWa1021bis`: `*304+PA-CYP+D`
- `HTWc3016`: `KA-KU-PA *304+PA-CYP+D`
- `HTWeWc3020`: `*188-DU *304+PA-CYP+D`

---

## Findings

### 1. `HTWb229` belongs inside the HTW warehouse-grade system

The key observation is not just that `HTWb229` contains `CYP+D`, but that the same grade marker reappears inside the tighter HTW chain:

- bare grade with sign prefix: `*188 CYP+D`
- bare grade with syllabic prefix: `KA CYP+D`
- extended commodity-grade compound: `*304+PA-CYP+D`

This is typical of a warehouse sublanguage where short labels and fuller compounds coexist.

### 2. `*188` most likely occupies a classifier or transaction-label slot

The best current reading of the evidence is functional, not lexical:

- `*188` is not behaving like a clear commodity name
- `*188` is not behaving like a solved grammatical particle
- `*188` repeatedly sits in administrative positions before or around categorized goods

The strongest working options are:

- classifier/category marker
- warehouse transaction label
- document- or operation-type marker

The evidence does not yet let us choose among those with promotion-level confidence.

### 3. `HTWb229` should constrain later readings, not consume them

The value of `HTWb229` is that it anchors the family in a small, interpretable warehouse frame:

- one unresolved administrative marker
- one already-modeled copper grade

That makes it a useful blocker note and a bad candidate for forced translation.

### 4. The `*188` family connects HT and HTW, but the HTW warehouse branch is narrower

`*188` is broader than `HTWb229`, but the warehouse branch is especially clear where it meets copper-grade notation:

- `HTWb229`
- `HTWeWc3020`
- nearby HTW `CYP+D` controls

This suggests the next progress on `*188` is more likely to come from warehouse subsystem comparison than from language-hypothesis testing.

---

## Determination

`HTWb229` should remain in **lane-C blocker status** as part of the HTW warehouse-classifier chain.

Current best statement:

**`*188` is an unresolved administrative/classifier-family sign that can precede warehouse copper-grade notation, including `CYP+D`.**

That is stronger than "unknown sign," but still below any lexical promotion threshold.

---

## Operational Consequences

1. Do not open a full connected reading for `HTWb229` yet.
2. Use `HTWb229`, `HTWeWc3020`, and `HTWc<3018>` as the core HTW comparator set.
3. Keep `*188` work tied to warehouse structure and classifier behavior.
4. Do not treat `HTWb229` as evidence for a translation breakthrough by itself.

---

## Next Test

The next high-yield comparison is:

- `HTWb229` = `*188 CYP+D`
- `HTWeWc3020` = `*188-DU *304+PA-CYP+D`
- `HTWc<3018>` = `KA CYP+D`

If a stable slot order emerges across that trio, the project can upgrade the `*188` family from a generic blocker to a narrower warehouse classifier/control function.
