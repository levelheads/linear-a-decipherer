# Admin Template Induction Memo

**Date**: 2026-03-15
**Agents**: F, A1, B, Lead
**Lane**: G (reading attempts) + B (validation)
**Status**: DRAFT COMPLETE

---

## Purpose

Turn the current completed admin readings into reusable structural templates that can accelerate the next wave of connected readings without over-claiming translation.

Source readings:

- `analysis/completed/inscriptions/HT2_READING.md`
- `analysis/completed/inscriptions/KNZb27_READING.md`
- `analysis/completed/inscriptions/PH12c_READING.md`
- `analysis/completed/inscriptions/KH15_READING.md`
- `analysis/active/2026-03-15_KH_WEEK2_FORMALIZATION_MEMO.md`

Academic-overlap note:

This memo is repo-native synthesis work. It does **not** restate GORILA or Younger commentary. It generalizes templates from completed project readings and is therefore a new execution artifact rather than a literature summary.

---

## Executive Summary

The current admin reading floor supports four reusable templates:

1. **Standalone header/topic marker**
2. **Single-label commodity record**
3. **Header plus variant commodity block**
4. **KH zero-K-R micro-account**

These are not sentence translations. They are structural translation skeletons that can be applied to unread tablets with matching profiles.

The strongest immediate unlocks are:

- `KH54`
- `KH25`
- `ZA4b`
- `PH25`

`HT46b` remains staged but lower-yield until its unidentified signs gain better controls.

---

## Template Set

### Template A: Standalone Header/Topic Marker

**Core evidence**: `PH12c`

Canonical shape:

```text
TE
```

Interpretation:

- section opener
- entry/topic marker
- fragmentary header line

Why it matters:

- stabilizes segmentation on short admin fragments
- lets the project separate content words from structural openers

Current confidence:

- HIGH for function
- not a lexical translation claim

### Template B: Single-Label Commodity Record

**Core evidence**: `KNZb27`

Canonical shape:

```text
LABEL  divider  COMMODITY  QUANTITY
```

Example:

```text
DI-NA-U  𐄁  VIN  17
```

Interpretation:

- source/account/locality label
- one commodity
- one quantity

Why it matters:

- this is the cleanest short-record template in the current cross-site set
- suitable for vessel labels and short commodity notations

Current confidence:

- HIGH for structure
- PROBABLE for the label role

### Template C: Header Plus Variant Commodity Block

**Core evidence**: `HT2`

Canonical shape:

```text
HEADER  divider  COMMODITY-VARIANT + QUANTITY ...
[optional named sub-entry]
COMMODITY-VARIANT + QUANTITY ...
```

Example core:

```text
A-KA-RU  𐄁  OLE+U 20
OLE+A 17
OLE+E 3
KI-RE-TA-NA  OLE+U 54
OLE+A 47
```

Interpretation:

- institutional/section header
- grouped variant commodities
- optional named participant or sub-entry

Why it matters:

- it is the best current template for handling compact variant ledgers without KU-RO
- it proves that headers can span commodity classes and named sub-blocks

Current confidence:

- PROBABLE for header and sub-entry roles
- CERTAIN for commodity-logogram behavior

### Template D: KH Zero-K-R Micro-Account

**Core evidence**: `KH15`

Canonical shape:

```text
COMMODITY  FRACTION
COMMODITY  FRACTION
COMMODITY  FRACTION
```

Example:

```text
CYP  1/2
NI   1/2
NI   1/4
```

Interpretation:

- short transaction-level KH note
- mixed commodities allowed
- no KU-RO / KI-RO expected

Why it matters:

- this is the clearest reusable KH reading frame now in the repo
- it protects KH readings from being forced into HT-style balance-sheet expectations

Current confidence:

- HIGH for KH structural function
- HIGH for NI as commodity line in this setting

---

## Cross-Template Observations

### 1. Structural markers are now strong enough to drive segmentation

From `PH12c` and `HT2`, the project now has a cleaner split between:

- entry/header material
- commodity lines
- named/account labels

That reduces the number of unread tablets that have to be approached as unconstrained strings.

### 2. KH needs its own template family

The existing evidence confirms that KH cannot be read with HT expectations by default.

Working KH defaults:

- no K-R expectation
- short transaction notes are normal
- mixed commodities are normal
- grade or commodity lines may stand alone without recipient syntax

### 3. Variant-ledgers and single-line records are the fastest current translation route

The strongest readable structures are not long syntactic texts. They are:

- short label + commodity records
- variant-ledger blocks
- transaction-level micro-accounts

That is where the next connected readings should continue to concentrate.

---

## Target Unlock Map

### `KH54`

Current brief:

- `data/reading_briefs/week2/KH54.json`
- raw text: `CYP+E 1 | GRA 1 | 𐝫 | 𐝫`

Best template match:

- **Template D** with mixed KH commodity logic

Why it is high-yield:

- supports KH mixed-commodity formalization
- extends KH beyond copper-only interpretation

### `KH25`

Current brief:

- `data/reading_briefs/week2/KH25.json`
- raw text: `VIR+[?] 140 | VIR+[?] 10 | 𐝫`

Best template match:

- **Template D**, but in personnel-count mode rather than commodity-fraction mode

Why it is high-yield:

- tests high-scale KH recording without K-R
- strengthens KH transaction-level model with large counts

### `ZA4b`

Current brief:

- `data/reading_briefs/next_block/ZA4b.json`
- raw text: `𐝫 | VIN 104`

Best template match:

- **Template B**

Why it is high-yield:

- short Zakros wine record
- likely useful for label + commodity interpretation without arithmetic complexity

### `PH25`

Current brief:

- `data/reading_briefs/next_block/PH25.json`
- raw text: `VIN 2 | 𐝫 | 𐝫`

Best template match:

- weak **Template B** candidate

Why it is medium-yield:

- very short
- commodity anchor present
- but unidentified material remains thin

### `HT46b`

Current brief:

- `data/reading_briefs/next_block/HT46b.json`
- raw text: `𐝫 | 𐝫 | 16 1/2 | 6`

Best template match:

- none securely yet

Why it is lower-yield:

- no commodity anchor
- no clear structural marker
- likely needs another sign control before full reading effort

---

## Operational Recommendations

1. Read `KH54` next from the conservative stream.
2. Read `KH25` immediately after `KH54`.
3. Treat `ZA4b` as the best short non-KH follow-on.
4. Keep `PH25` in reserve behind `ZA4b`.
5. Hold `HT46b` until a stronger template or sign control appears.

---

## Determination

The admin reading program now has enough structure to move from tablet-by-tablet opportunism to template-guided execution.

Immediate result:

- `KH54`, `KH25`, and `ZA4b` are now the strongest next conservative reading targets.
