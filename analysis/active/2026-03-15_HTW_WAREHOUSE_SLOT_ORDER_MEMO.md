# HTW Warehouse Slot-Order Memo

**Date**: 2026-03-15
**Agents**: C, C2, C2a, Lead
**Lane**: C (script asymmetry) with warehouse support
**Status**: DRAFT COMPLETE

---

## Executive Summary

The HTW comparator set now supports a tighter structural claim than the earlier `HTWb229` note.

Across sealing, roundel, nodule, and tablet supports, the same warehouse branch keeps reappearing:

- `*188`
- `*188-DU`
- `CYP+D`
- `*304+PA-CYP+D`

The strongest result is this:

**The `*188` family occupies a recurrent control/classifier slot upstream of copper-grade notation, while the grade and full commodity-grade compound can appear with different prefixes depending on support and document compression.**

That is not yet a translation, but it is a credible subsystem result and a real narrowing of the warehouse problem.

---

## Evidence Base

### Live checks

- `python3 tools/corpus_lookup.py '*188' --exact`
- `python3 tools/corpus_lookup.py '*188-DU' --exact`
- `python3 tools/corpus_lookup.py 'CYP+D' --exact --site HTW`
- `python3 tools/corpus_lookup.py '*304+PA-CYP+D' --exact`
- object metadata extracted from `external/lineara/items_analysis/inscriptions.json`
- validator checks:
  - `python3 tools/corpus_consistency_validator.py --word '*188'`
  - `python3 tools/integrated_validator.py --word '*188'`
  - `python3 tools/corpus_consistency_validator.py --word '*188-DU'`
  - `python3 tools/integrated_validator.py --word '*188-DU'`

### Comparator set

| Item | Support | Context | Content |
|------|---------|---------|---------|
| `HTWb229` | Sealing | LMIB | `*188 CYP+D` |
| `HTWc3013` | Roundel | LMIB | `*188` |
| `HTWc3009` | Roundel | LMIB | `*333-DI-SU-KA *188` |
| `HTWc<3018>` | Roundel | LMIB | `KA CYP+D` |
| `HTWc3016` | Roundel | LMIB | `KA-KU-PA *304+PA-CYP+D` |
| `HTWeWc3020` | Roundel | LMIB | `*188-DU *304+PA-CYP+D` |
| `HTWa1021` | Nodule | LMIB | `*188-DU ...` |
| `HTWa1021bis` | Nodule | LMIB | `*304+PA-CYP+D 3` |
| `HT123+124b` | Tablet | LMIB | `*188`, `*188-DU`, numerals and totals |

---

## Findings

### 1. The HTW branch is not a single inscription type; it spans multiple supports

This is the biggest improvement over the prior note.

The relevant family is now visible on:

- sealing: `HTWb229`
- roundels: `HTWc3013`, `HTWc3009`, `HTWc<3018>`, `HTWc3016`, `HTWeWc3020`
- nodules: `HTWa1021`, `HTWa1021bis`
- tablets: `HT123+124b`

That distribution is exactly what we would expect from an administrative subsystem rather than an isolated lexical item.

### 2. A compressed-to-expanded scale is starting to emerge

The data align naturally on a compression scale:

- minimal sign only: `*188`
- sign plus grade: `*188 CYP+D`
- sign-family plus full commodity-grade compound: `*188-DU *304+PA-CYP+D`
- alternate prefix plus grade: `KA CYP+D`
- alternate prefix plus full compound: `KA-KU-PA *304+PA-CYP+D`

This suggests that the subsystem permits abbreviated and expanded labels rather than using one rigid written formula.

### 3. `*188` and `*188-DU` are not equivalent, but they occupy related slots

The validator evidence helps here:

- bare `*188` is structurally mixed and lexically weak
- `*188-DU` is more patterned than bare `*188`

The practical reading is:

- `*188` is the broader family marker
- `*188-DU` is a narrower warehouse branch or expanded variant

That is more credible than forcing both forms into the same translation.

### 4. Copper-grade notation is the stable downstream anchor

The most stable part of the subsystem remains the grade side:

- `CYP+D`
- `*304+PA-CYP+D`

Those are already bounded by earlier warehouse work. The new point is that the `*188` family reliably appears **before** or **upstream of** that material, which supports a classifier/control interpretation rather than a commodity identity.

### 5. The HTW subsystem is now falsifiable at slot level

The slot-order model predicts:

- future `*188`-family warehouse items should continue to appear upstream of grade or commodity-grade material
- future counterexamples where `*188` behaves like an ordinary commodity name would weaken the model
- if `*188-DU` regularly patterns with the expanded warehouse compound while bare `*188` does not, the family split becomes stronger

This is a useful research position because it creates a clear next test instead of an unbounded guess.

---

## Validation Snapshot

### `*188`

- corpus consistency: positional `44.4%`, contextual `44.4%`, functional `44.4%`
- integrated validation: methodology non-compliant as lexical item; regionally penalized and threshold-eliminated

Interpretation:

Bare `*188` is too mixed for a strong lexical claim. It should stay at subsystem/function level only.

### `*188-DU`

- corpus consistency: positional `66.7%`, contextual `66.7%`, functional `66.7%`
- integrated validation: stronger patterned behavior than bare `*188`, but still not enough to justify promotion of a translation for the family

Interpretation:

`*188-DU` is the more structured warehouse branch and should be prioritized over bare `*188` for future slot testing.

---

## Determination

The HTW warehouse family should now be modeled as a **slot-order subsystem**:

- upstream control/classifier slot: `*188`, `*188-DU`, possibly syllabic alternatives like `KA`
- downstream grade slot: `CYP+D`
- downstream expanded commodity-grade slot: `*304+PA-CYP+D`

This is a credible structural gain, but it remains below translation/promotion threshold.

---

## Operational Consequences

1. Keep `HTWb229` out of the connected-reading queue.
2. Use `HTWeWc3020` as the primary warehouse control comparator.
3. Treat `*188-DU` as the sharper comparator form for future warehouse work.
4. Use support variation to study subsystem compression rather than lexical meaning first.
