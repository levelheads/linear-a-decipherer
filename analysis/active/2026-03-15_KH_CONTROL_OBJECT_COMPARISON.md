# KH Control Object Comparison

**Date**: 2026-03-15
**Agents**: C, C1, C1a, Lead
**Lane**: C (script asymmetry)
**Status**: DRAFT COMPLETE

---

## Executive Summary

The KH `*86` family now has a clearer structural shape than it did in the earlier blocker memo.

The comparison between `KHWa1013-1016` and `KHWc2058-2109` shows:

1. `*86-RO` is carried on **nodules**.
2. `*86+*188` is carried on **roundels**.
3. Both families are KH-only, highly formulaic, and LMIB-centered.

That combination supports a narrower and more credible claim:

**`*86-RO` and `*86+*188` are parallel control labels used on different administrative object classes inside the same KH apparatus.**

This is a structural breakthrough, not a lexical one. It improves subsystem mapping and reduces the chance of forcing false translations onto the `*86` family.

---

## Evidence Base

### Live checks

- `python3 tools/corpus_lookup.py '*86-RO' --exact`
- `python3 tools/corpus_lookup.py '*86+*188' --exact`
- object metadata extracted from `external/lineara/items_analysis/inscriptions.json`
- validator checks:
  - `python3 tools/corpus_consistency_validator.py --word '*86-RO'`
  - `python3 tools/corpus_consistency_validator.py --word '*86+*188'`
  - `python3 tools/integrated_validator.py --word '*86-RO'`
  - `python3 tools/integrated_validator.py --word '*86+*188'`

### Prior analysis

- `analysis/active/2026-02-17_khania_star86_star188_system.md`
- `analysis/active/2026-03-15_KH_STAR86_RO_SUBSYSTEM_MEMO.md`

---

## Comparator Set

### Family A: `*86-RO`

| Item | Support | Context | Content |
|------|---------|---------|---------|
| `KHWa1013` | Nodule | LMIB | `*86-RO` |
| `KHWa1014` | Nodule | LMIB | `*86-RO` |
| `KHWa1015` | Nodule | — | `*86-RO` |
| `KHWa1016` | Nodule | LMIB | `*86-RO` |

### Family B: `*86+*188`

| Item | Support | Context | Content |
|------|---------|---------|---------|
| `KHWc2058` | Roundel | LMIB | `*86+*188` |
| `KHWc2092` | Roundel | — | `*86+*188` |
| `KHWc2091` | Roundel | — | `*86+*188` |
| `KHWc2059` | Roundel | — | `*86+*188` |
| `KHWc2060` | Roundel | LMIB | `*86+*188` |
| `KHWc2061` | Roundel | LMIB | `*86+*188` |
| `KHWc2062` | Roundel | LMIB | `*86+*188` |
| `KHWc2109` | Roundel | LMIB | `*86+*188` |

---

## Findings

### 1. The two KH families are separated by support class, not just by sign sequence

This is the strongest new result.

- `*86-RO` is attached to `KHWa` nodules
- `*86+*188` is attached to `KHWc` roundels

That means the split is not accidental sign variation on the same kind of object. The KH administration is using related `*86` labels on two different physical support classes.

### 2. The common denominator is control function, not commodity content

Both families share the same structural profile:

- sole-content inscriptions
- no numerals
- tight site concentration at KH
- minimal internal variation

Those are the wrong conditions for an ordinary commodity line and the right conditions for control marks, receipt marks, or object-class labels.

### 3. `*86-RO` is best read as the nodule-side branch of the KH control system

The earlier memo already treated `*86-RO` as administrative. The support comparison sharpens that claim:

- `*86+*188` marks roundels
- `*86-RO` marks nodules

The best current model is that the two branches label different administrative objects within the same system rather than different lexical meanings of `*86`.

### 4. The `-RO` element still does not justify a solved translation

It remains reasonable to compare `-RO` to closure or summary behavior, but the object-class evidence actually strengthens the case for caution.

If `*86-RO` is a nodule-side control label, then the `-RO` sequence may be functioning inside an administrative formula rather than transparently carrying a recoverable spoken word.

### 5. The project now has a falsifiable KH subsystem model

The claim can now be stated in a way that can fail:

- if future `*86-RO` tokens appear on roundels or tablets with numerals, the object-class split weakens
- if future `*86+*188` tokens appear on nodules, the branch distinction weakens
- if either family gains ordinary commodity syntax, the control-label model weakens

That makes this a stronger research position than the earlier generic blocker label.

---

## Validation Snapshot

### `*86-RO`

- corpus consistency: positional `100%`, contextual `100%`, functional `100%`
- integrated validation: language-hypothesis tier `ELIMINATED`; anchor floor keeps it bounded above pure noise

Interpretation:

`*86-RO` is highly consistent as a narrow family, but not as a language decipherment item.

### `*86+*188`

- corpus consistency: positional `100%`, contextual `100%`, functional `100%`
- integrated validation: language-hypothesis tier `ELIMINATED`; no basis for lexical promotion

Interpretation:

`*86+*188` is likewise highly consistent structurally and weak lexically, which is exactly what a control-object marker should look like.

---

## Determination

The KH `*86` system should now be modeled as an **object-class split inside one control apparatus**:

- `*86-RO` = nodule-side control family
- `*86+*188` = roundel-side control family

This is a stronger administrative model and a more credible one than any current lexical translation attempt.

---

## Operational Consequences

1. Treat `KHWa1013-1016` and `KHWc2058-2109` as one coordinated KH subsystem dossier.
2. Keep the entire `*86` family in lane-C structural analysis.
3. Do not open promotion work for a spoken-value reading of `*86-RO`.
4. Use this object-class split as a control when evaluating future KH nodules and roundels.
