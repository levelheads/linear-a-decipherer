# HT 2 Connected Reading Report

**Date**: 2026-03-15
**Analyst**: Codex (GPT-5)
**Phase**: Month 1 Week 2 - Balanced Admin Push
**Status**: COMPLETE
**Confidence**: PROBABLE

---

## Pre-Flight Checklist (First Principles)

```
FIRST PRINCIPLES PRE-FLIGHT CHECK

[x] I will analyze patterns BEFORE assuming a language [P1]
[x] I am prepared to abandon my hypothesis if evidence contradicts it [P2]
[x] I have identified all available anchors [P3]
[x] I will test against ALL seven linguistic hypotheses [P4]
[x] I will consider what the data DOESN'T show [P5]
[x] I will verify readings across the ENTIRE corpus [P6]

Seven hypotheses: Luwian, Semitic, Pre-Greek, Proto-Greek, Hurrian, Hattic, Etruscan
Surviving: Luwian (STRONG, 35.0%), Semitic (MODERATE, 17.5%)
Eliminated: Proto-Greek, Pre-Greek, Hurrian, Hattic, Etruscan (all <5%)
```

---

## Source Information

| Attribute | Value |
|-----------|-------|
| **Tablet ID** | HT 2 |
| **Site** | Hagia Triada (Haghia Triada) |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Findspot** | Portico 11 and Room 13 |
| **Scribe** | Unknown |
| **Support** | Tablet |
| **Document Type** | Compact oil account with qualified OLE variants |
| **Arithmetic Status** | NO_KURO (no total line present) |
| **Corpus Source** | `data/corpus.json`, `data/arithmetic_verification.json` |
| **Reading Readiness** | Score 0.697 |
| **Cross-Tablet Significance** | Links A-KA-RU and KI-RE-TA-NA inside a single oil-variant account |

---

## Transliteration

```
Line 1:  A-KA-RU  𐄁  OLE+U  20
Line 2:  OLE+A  17
Line 3:  OLE+E  3
Line 4:  KI-RE-TA-NA  OLE+U  54
Line 5:  OLE+A  47
Line 6:  1
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| A | AB 08 | CERTAIN | High |
| KA | AB 77 | CERTAIN | High |
| RU | AB 26 | CERTAIN | High |
| KI | AB 67 | CERTAIN | High |
| RE | AB 27 | CERTAIN | High |
| TA | AB 59 | CERTAIN | High |
| NA | AB 06 | CERTAIN | High |
| OLE+U | Logogram compound | CERTAIN | 22 occurrences |
| OLE+A | Logogram compound | CERTAIN | 2 occurrences |
| OLE+E | Logogram compound | CERTAIN | 4 occurrences |
| 𐄁 | Divider | CERTAIN | Standard |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None directly confirmed on this tablet.**

### Level 2: Linear B Cognates + Position (HIGH)

**None directly confirmed.** No KU-RO / KI-RO vocabulary is present.

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **OLE+U** | Olive oil, qualified variant U | Pictographic OLE base; cross-corpus compound logogram system | Lines 1, 4 |
| **OLE+A** | Olive oil, qualified variant A | Same compound-logogram system | Lines 2, 5 |
| **OLE+E** | Olive oil, qualified variant E | Same compound-logogram system | Line 3 |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| Header + divider + commodity sequence | Standard administrative opening | `A-KA-RU 𐄁 ...` |
| Repeated logogram + number | Commodity accounting | Five explicit OLE variant quantities |
| Named entry followed by commodity + quantity | Recipient/source sub-entry | `KI-RE-TA-NA OLE+U 54` |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| **A-KA-RU** | Section header / institutional source | Header-initial here and in HT 86a/b |
| **KI-RE-TA-NA** | Named participant (recipient, locality, or institution) | Cross-tablet recurrence with OLE, GRA, and VIR contexts |

---

## Structural Analysis

### Document Type

**Compact oil account with three qualified oil variants and one named downstream entry**

HT 2 is not a full recipient list and not a fully totaled ledger. Instead, it records a short oil account under the header **A-KA-RU**, then switches into a named entry for **KI-RE-TA-NA** with two larger OLE allocations. The tablet is structurally valuable because it shows the rare variants **OLE+A** and **OLE+E** on the same document as the common **OLE+U**.

### Rosetta Skeleton

| Position | Term | Role | Quantity | Confidence |
|----------|------|------|----------|------------|
| 1 | A-KA-RU | Header | -- | PROBABLE |
| 2 | 𐄁 | Divider | -- | CERTAIN |
| 3 | OLE+U | Commodity | 20 | CERTAIN |
| 4 | OLE+A | Commodity | 17 | CERTAIN |
| 5 | OLE+E | Commodity | 3 | CERTAIN |
| 6 | KI-RE-TA-NA | Named entry | -- | PROBABLE |
| 7 | OLE+U | Commodity | 54 | CERTAIN |
| 8 | OLE+A | Commodity | 47 | CERTAIN |
| 9 | 1 | Isolated numeral / residual notation | 1 | POSSIBLE |

### Arithmetic Verification

```
Visible explicit quantities:
  OLE+U    20
  OLE+A    17
  OLE+E     3
  OLE+U    54
  OLE+A    47
  1         [isolated terminal numeral]
```

**Result**: `NO_KURO`. There is no totaling line and no reliable way to assign the final isolated `1` to a specific commodity class. The visible account therefore supports structural reading but not a verified subtotal/grand-total claim.

### Notable Structural Features

1. **Three oil variants on a single short tablet**: `OLE+U`, `OLE+A`, and `OLE+E` appear together. `OLE+A` is otherwise only attested on HT 2.
2. **A-KA-RU is header-like, not a commodity word**: on HT 86a/b the same form opens grain sections; on HT 2 it opens an oil account. This cross-commodity behavior argues for an institutional/header role.
3. **KI-RE-TA-NA is commodity-flexible**: the same word appears with oil here, with fractions on HT 8a, with `VIR+[?]` on HT 108, and with `GRA+B 60` on HT 120.
4. **Terminal `1` remains unresolved**: it may be an omitted continuation of the previous OLE line or a damaged residual numeral, but the tablet does not prove which.

---

## Connected Reading Attempt

### Element-by-Element Interpretation

```
A-KA-RU               [institutional / section header]          PROBABLE
OLE+U 20              oil variant U: 20                        CERTAIN
OLE+A 17              oil variant A: 17                        CERTAIN
OLE+E 3               oil variant E: 3                         CERTAIN
KI-RE-TA-NA           named recipient/source/locality          PROBABLE
OLE+U 54              oil variant U: 54                        CERTAIN
OLE+A 47              oil variant A: 47                        CERTAIN
1                     unresolved residual numeral              POSSIBLE
```

### Full Interpretive Reading (Conservative)

> **A-KA-RU account**
>
> Olive oil variant U: 20  
> Olive oil variant A: 17  
> Olive oil variant E: 3
>
> **KI-RE-TA-NA**:
>
> Olive oil variant U: 54  
> Olive oil variant A: 47  
> `1` [unresolved terminal numeral]

This is best treated as a **compact oil ledger** rather than a sentence translation. The stable result is the structure: one header, three oil-grade quantities, then a named sub-entry with two larger oil allocations.

---

## What We Know For Certain

1. **HT 2 is an oil tablet**: all explicit commodity logograms are OLE variants.
2. **Three qualified oil variants occur**: `OLE+U`, `OLE+A`, `OLE+E`.
3. **A-KA-RU is header-initial**: same positional behavior as on HT 86a/b.
4. **KI-RE-TA-NA is a reusable administrative word**: it recurs on four HT tablets in multiple commodity contexts.
5. **No verified total is present**: the tablet is `NO_KURO`.

## What We Hypothesize

1. **A-KA-RU is an institutional or personal header**, not a commodity label. PROBABLE.
2. **KI-RE-TA-NA is a named recipient, locality, or institution** participating in multiple commodity streams. PROBABLE.
3. **The final `1` is an omitted continuation marker or residual quantity** rather than a standalone total. POSSIBLE.

---

## Cross-Corpus Verification

### A-KA-RU Distribution

| Tablet | Context | Role |
|--------|---------|------|
| HT 2 | Oil account | Header |
| HT 86a | Grain distribution | Header |
| HT 86b | Grain distribution | Header |

**Verification**: A-KA-RU is always initial and never directly followed by a numeral. This supports a header/source interpretation.

### KI-RE-TA-NA Distribution

| Tablet | Context | Quantity Pattern |
|--------|---------|------------------|
| HT 2 | OLE account | `OLE+U 54`, `OLE+A 47` |
| HT 8a | Fractional account | `1/4`, `1/2` |
| HT 108 | Personnel context | `VIR+[?] 1` |
| HT 120 | Grain context | `GRA+B 60` |

**Verification**: KI-RE-TA-NA is commodity-flexible and therefore unlikely to be a commodity name.

### OLE Variant Context

| Variant | Corpus Count | Notes |
|---------|--------------|-------|
| OLE+U | 22 | Standard/common oil qualifier |
| OLE+A | 2 | HT 2 only |
| OLE+E | 4 | Rare but cross-tablet attested |

**Verification**: HT 2 is the key tablet for `OLE+A`, making it disproportionately important for the OLE variant system.

---

## Promotion Recommendation

**Decision**: `NO-PROMOTION`

**Rationale**:
1. HT 2 strengthens existing dossiers for **A-KA-RU** and **KI-RE-TA-NA**.
2. The unresolved terminal `1` prevents a tighter interpretive upgrade.
3. The tablet is still valuable as a high-signal structural reading for the OLE variant system.

---

## Final Assessment

HT 2 advances the decipherment by tightening the **oil qualifier system** and by showing that **A-KA-RU** behaves as a reusable administrative header across commodities. The tablet does **not** yet justify a lexical promotion, but it materially improves the admin reading floor for OLE accounts and makes **KI-RE-TA-NA** more defensible as a cross-commodity named entity.
