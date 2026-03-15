# HTW `KA` vs `*188-DU` Comparison

**Date**: 2026-03-15
**Agents**: C, C2, C2b, Lead
**Lane**: C (script asymmetry) with warehouse support
**Status**: DRAFT COMPLETE

---

## Executive Summary

The next HTW comparison resolves one important ambiguity from the prior slot-order memo.

Question:

**Is the upstream warehouse slot varying because of support class, or because multiple classifier/control families feed the same downstream grade system?**

Current answer:

**Classifier-family variation is the better fit.**

Why:

1. `*188-DU` appears on both a nodule (`HTWa1021`) and a roundel (`HTWeWc3020`), so it is not support-locked.
2. `KA-KU-PA` appears on a tablet (`HT16`) and on roundels (`HTWc3015`, `HTWc3016`), so it is not support-locked either.
3. Both families can sit upstream of copper or copper-graded warehouse material.

This does not solve the labels, but it does show that the warehouse branch contains at least two upstream control families, not one support-conditioned alternation.

---

## Evidence Base

### Live corpus checks

- `python3 tools/corpus_lookup.py 'KA-KU-PA' --exact`
- `python3 tools/corpus_lookup.py 'KA' --exact --site HTW`
- `python3 tools/corpus_lookup.py '*188-DU' --exact`
- `python3 tools/corpus_lookup.py '*304+PA-CYP+D' --exact`
- `python3 tools/corpus_consistency_validator.py --word 'KA-KU-PA'`
- `python3 tools/integrated_validator.py --word 'KA-KU-PA'`

### Prior project analyses

- `analysis/active/2026-03-15_HTWB229_WAREHOUSE_CLASSIFIER_NOTE.md`
- `analysis/active/2026-03-15_HTW_WAREHOUSE_SLOT_ORDER_MEMO.md`

### Academic-overlap note

The local commentary files describe object types and transcriptions for `HTWe1021` and `HTWc3016`, but they do not make the cross-support classifier comparison documented here.

---

## Comparator Set

### `*188-DU` branch

| Item | Support | Content |
|------|---------|---------|
| `HTWa1021` | Nodule | `*188-DU ...` |
| `HTWeWc3020` | Roundel | `*188-DU *304+PA-CYP+D` |
| `HT123+124b` | Tablet | `*188-DU 𐄁 10` |

### `KA` / `KA-KU-PA` branch

| Item | Support | Content |
|------|---------|---------|
| `HT16` | Tablet | `KA-KU-PA 𐄁` |
| `HTWc3015` | Roundel | `KA-KU-PA CYP` |
| `HTWc3016` | Roundel | `KA-KU-PA *304+PA-CYP+D` |
| `HTWc<3018>` | Roundel | `KA CYP+D` |

---

## Findings

### 1. Support class alone cannot explain the upstream variation

If the alternation were support-driven, we would expect one family to stay on nodules and another to stay on roundels or tablets.

But the evidence shows:

- `*188-DU` spans nodule, roundel, and tablet
- `KA-KU-PA` spans tablet and roundel

That breaks the simple support-conditioned explanation.

### 2. Multiple upstream control families are feeding the same warehouse chain

The downstream side is comparatively stable:

- `CYP`
- `CYP+D`
- `*304+PA-CYP+D`

The upstream side varies:

- `*188`
- `*188-DU`
- `KA`
- `KA-KU-PA`

This is better explained by multiple control/classifier families interacting with one warehouse-grade vocabulary than by a single label changing solely by support.

### 3. `KA-KU-PA` is patterned enough to matter, but too mixed to solve

`KA-KU-PA` has:

- 3 occurrences
- support spread across tablet and roundel
- corpus-consistency pass but contextual inconsistency
- integrated validation that allows bounded linguistic interest but does not force a warehouse translation

So it is a legitimate comparator, but not a clean lexical anchor.

### 4. Bare `KA` is too broad to anchor the subsystem by itself

There are many HTW nodules with bare `KA`. That means:

- `KA` cannot be treated as a narrow warehouse label by default
- only the warehouse-grade contexts (`HTWc<3018>`, `HTWc3015`, `HTWc3016`) are relevant to this branch

This protects the analysis from collapsing the whole `KA` inventory into one explanation.

### 5. The HTW subsystem is more structurally differentiated than the earlier note implied

The earlier memo established an upstream slot before warehouse grade notation.

This memo refines that:

- the slot is real
- it is not explained by support class alone
- it likely hosts more than one classifier/control family

That is a better and more falsifiable model.

---

## Determination

The HTW warehouse subsystem should now be modeled with **multiple upstream control families**:

- `*188` / `*188-DU` family
- `KA` / `KA-KU-PA` family

Both can feed into the same downstream grade and commodity-grade slots.

This is a structural gain only. No translation promotion is justified.

---

## Operational Consequences

1. Keep `*188-DU` as the sharper warehouse comparator.
2. Track `KA-KU-PA` as a secondary upstream comparator, not as a solved item.
3. Do not explain HTW slot variation purely by support class.
4. Restrict `KA` claims to the warehouse-grade subset, not the full HTW `KA` mass.
