# KH15 Connected Reading Report

**Date**: 2026-03-15
**Analyst**: Codex (GPT-5)
**Phase**: Month 1 Week 2 - KH Formalization Follow-On
**Status**: COMPLETE
**Confidence**: HIGH

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
| **Tablet ID** | KH15 |
| **Site** | Khania (Kydonia) |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Scribe** | KH Scribe 1 |
| **Support** | Tablet |
| **Document Type** | Mixed commodity fractional note (`CYP` + `NI`) |
| **Arithmetic Status** | NO_KURO (short transaction-level tablet) |
| **Corpus Source** | `data/corpus.json`, `data/arithmetic_verification.json` |
| **Reading Readiness** | Score 0.170 |
| **Cross-Site Significance** | Extends approved `NI` into a direct KH mixed-commodity tablet |

---

## Transliteration

```
Line 1:  CYP  ¹⁄₂
Line 2:  NI   ¹⁄₂
Line 3:  NI   ¹⁄₄
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| CYP | Logogram | CERTAIN | Khania-dominant |
| NI | AB 30 / registered reading | HIGH | 77+ occurrences project-wide; 26 at KH |
| ¹⁄₂ | Fraction | CERTAIN | Standard |
| ¹⁄₄ | Fraction | CERTAIN | Standard |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None.**

### Level 2: Linear B Cognates + Position (HIGH)

**None directly present.** No K-R vocabulary appears.

### Level 3: Logograms / Commodity Anchors (HIGH/CERTAIN)

| Term | Meaning | Evidence | On this tablet |
|------|---------|----------|----------------|
| **CYP** | Copper | Pictographic / cross-corpus commodity logogram | Line 1 |
| **NI** | Wine-associated commodity marker | Approved HIGH anchor; 100% VIN specificity in project dossier | Lines 2-3 |

### Level 4: Structural Patterns (HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| Commodity + fraction | Short transaction-level KH accounting | `CYP 1/2`, `NI 1/2`, `NI 1/4` |
| Repeated NI line items | Same commodity across multiple fractional entries | Lines 2-3 |
| No KU-RO / KI-RO | KH structural pattern | Consistent with KH transaction-level accounting |

---

## Structural Analysis

### Document Type

**Three-line mixed commodity micro-account at Khania**

KH15 is best read as a direct transaction-level note rather than a named-recipient list. The brief skeleton's header/recipient split for the two `NI` lines is less plausible than a plain commodity reading because:

1. `NI` is already operationally approved as a wine-associated commodity marker.
2. The inscription is only three lines long, each ending with a fraction.
3. Khania frequently records short commodity lines without HT-style recipient superstructure.

### Rosetta Skeleton

| Position | Term | Role | Quantity | Confidence |
|----------|------|------|----------|------------|
| 1 | CYP | Commodity | 1/2 | CERTAIN |
| 2 | NI | Commodity / wine marker | 1/2 | HIGH |
| 3 | NI | Commodity / wine marker | 1/4 | HIGH |

### Arithmetic Verification

```text
CYP   1/2
NI    1/2
NI    1/4
```

**Result**: `NO_KURO`. This is a short KH transaction note, not a balance-sheet tablet. There is no reason to expect KU-RO at this length and site.

### Notable Structural Features

1. **Direct CYP + NI coexistence**: KH15 places copper and NI on the same tablet without any K-R layer.
2. **NI repeats as two fractional entries**: this aligns KH15 with KH8's repeated NI behavior.
3. **KH transaction-level style remains intact**: three brief lines, all fractions, no recipients, no totals.
4. **KH Scribe 1 continuity**: the same scribal tradition appears in other KH administrative material and supports local system coherence.

---

## Connected Reading Attempt

### Element-by-Element Interpretation

```text
CYP   1/2        copper: 1/2 unit                  CERTAIN
NI    1/2        wine-associated commodity: 1/2    HIGH
NI    1/4        wine-associated commodity: 1/4    HIGH
```

### Full Interpretive Reading

> Copper: 1/2 unit  
> NI (wine-associated commodity): 1/2 unit  
> NI (wine-associated commodity): 1/4 unit

This is a **mixed commodity micro-account**, not a full sentence translation. The stable result is that `NI` is functioning as a commodity line at Khania alongside copper.

---

## What We Know For Certain

1. **KH15 is a three-line fractional account**.
2. **CYP is present with 1/2**.
3. **NI occurs twice**, with `1/2` and `1/4`.
4. **No K-R vocabulary appears**, consistent with KH structure.

## What We Hypothesize

1. **NI is functioning as the wine marker on both lines**, not as a personal name. HIGH.
2. **The two NI lines represent either two sub-allocations or two receipts of the same commodity class**. PROBABLE.
3. **KH15 is part of the same NI scaling continuum seen in KH8, KH11, and KH88**. HIGH.

---

## Cross-Corpus Verification

### NI at Khania

| Tablet | NI Quantity | Context |
|--------|-------------|---------|
| KH8 | 1/2, 1/4 | Fractional mixed micro-allocation |
| KH11 | 1 | Mixed commodity tablet with VIN also present |
| **KH15** | **1/2, 1/4** | Mixed `CYP` + `NI` micro-account |
| KH88 | 10 | Bulk allocation |

**Verification**: KH15 strengthens the existing NI range at Khania. NI now clearly spans:

- fractional micro-allocation (`KH8`, `KH15`)
- small integer use (`KH11`)
- bulk allocation (`KH88`)

### KH Structural Verification

| Feature | KH15 | Expected from KH model? |
|---------|------|-------------------------|
| Short tablet | Yes | Yes |
| Fractions | Yes | Yes |
| KU-RO absent | Yes | Yes |
| Mixed commodity possible | Yes | Yes |

**Verification**: KH15 fits the KH accounting philosophy model without needing any special exception.

---

## Promotion Recommendation

**Decision**: `MAINTAIN`

**Rationale**:
1. `NI` is already operationally approved at HIGH.
2. KH15 strengthens the NI-at-KH dossier but does not require a new promotion packet.
3. The reading's value is structural: it tightens the KH formalization stream and improves the cross-tablet translation floor.

---

## Final Assessment

KH15 is the cleanest current proof that approved `NI` belongs inside the **ordinary Khania administrative layer**, not just in exceptional or bulk texts. It connects the KH copper system to the NI dossier directly and strengthens the case that Khania administered wine across multiple scales without adopting the HT balance-sheet vocabulary.
