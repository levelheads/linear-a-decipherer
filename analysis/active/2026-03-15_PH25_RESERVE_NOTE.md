# PH25 Reserve Note

**Date**: 2026-03-15
**Agents**: F, B, A2
**Lane**: G (reading attempts) + B (validation)
**Status**: ACTIVE HOLD

---

## Purpose

Document why `PH25` should remain in the conservative queue as a bounded reserve case rather than being forced into a completed connected reading.

---

## Evidence Reviewed

- `data/reading_briefs/next_block/PH25.json`
- `data/corpus.json`
- `external/lineara/items_analysis/inscriptions.json`
- `tools/analyze_inscription.py PH25 --json`
- local project search for prior `PH25` analysis and Phaistos `VIN` comparators

---

## Secure Floor

`PH25` securely preserves:

```text
Line 1:  VIN  2
Line 2:  𐝫
Line 3:  𐝫
```

What is secure:

1. `VIN` is certain.
2. The quantity `2` is certain.
3. The text is administrative, short, and non-totaled.
4. The support is a Phaistos label, which makes compressed notation plausible.

---

## Why It Stays On Hold

The two following lines are both unresolved single-sign lines. At current evidence level, the project cannot tell whether they are:

- label/control marks
- recipient marks
- repeated section or object markers
- an incomplete label sequence on a multi-face object

That uncertainty is too central to the document to justify a completed connected reading. Unlike `ZA4b`, where the secure `VIN 104` line can stand on its own as the main content, `PH25` is dominated by unresolved trailing material.

---

## Credibility Check

The reserve decision is evidence-driven:

- the reading brief classified `PH25` as a weak Template B candidate
- the automated inscription analysis confirmed only one anchor (`VIN`)
- local project search found no prior completed `PH25` reading to inherit or contradict
- no internal evidence surfaced that would justify turning the repeated `𐝫` lines into a named person, place, or function word

This is the correct methodological outcome: bounded interpretation, not forced completion.

---

## Determination

`PH25` remains:

- `HOLD` for a completed connected reading
- `ACTIVE` as a reserve comparator for short Phaistos wine labels

Secure working gloss:

> Wine: 2 units  
> [two unresolved control/label lines]

This gloss is operational only and should not be indexed as a completed canonical reading.

---

## Re-entry Conditions

Promote `PH25` back into active reading work only if one of these happens:

1. a Phaistos label comparator clarifies the repeated single-sign lines
2. the unresolved sign gains a stable function from lane-C distribution work
3. image-level review or support-layout analysis shows a clearer line order/function split

Until then, `PH25` is better used as a cautionary reserve tablet than as a breakthrough target.
