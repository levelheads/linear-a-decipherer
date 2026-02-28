# KH22 Connected Reading Report

**Date**: 2026-02-22
**Analyst**: Claude (Opus 4.6)
**Phase**: MINOS III Campaign 1 — Cross-Site Readings (Tiers 3-4)
**Status**: COMPLETE

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
| **Tablet ID** | KH22 |
| **Site** | Khania (Kydonia) |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Scribe** | Unknown |
| **Support** | Tablet (clay) |
| **Document Type** | Copper allocation record (CYP grading system) |
| **Arithmetic Status** | NO_KURO (no KU-RO present) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |
| **Reading Readiness** | Score 0.415 |
| **Cross-Site Significance** | Khania -- parallel admin system; zero K-R vocabulary; CYP grading |

---

## Transliteration

```
Line 1:  ZA  𐄁  SU  7
Line 2:  CYP+E
Line 3:  SI  4
Line 4:  CYP
Line 5:  𐝫
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| ZA | AB 17 | CERTAIN | High |
| SU | AB 58 | CERTAIN | High |
| SI | AB 41 | CERTAIN | High |
| CYP | Logogram | CERTAIN | Khania-dominant |
| CYP+E | Compound logogram | CERTAIN | Khania-specific |
| 𐄁 | Word divider | CERTAIN | Standard |
| 𐝫 | Damaged/missing | — | — |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None directly inscribed.** ZA and SU are single syllables, not confirmed toponyms.

### Level 2: Linear B Cognates + Position (HIGH)

**None.** No KU-RO, KI-RO, or other K-R paradigm terms. **This confirms the zero-K-R pattern at Khania** (now confirmed at p=0.004, per Regional agent analysis).

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **CYP** | Copper/bronze | Pictographic; Linear B cognate | Commodity (ungraded) |
| **CYP+E** | Higher-grade copper | CYP base + E qualifier = integer quantities | Commodity (graded, higher) |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| CYP+E with integer (4) | Higher-grade copper, integer quantities | KH system: CYP+E = integers |
| CYP alone (bottom) | Possibly CYP+D (lower-grade) or unqualified | KH system: CYP+D = fractions |
| ZA 𐄁 SU pattern | Header: ZA as place/source, SU as qualifier | Position-initial |
| SI + 4 | Recipient with quantity | Standard NAME + QUANTITY |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| ZA as standalone | Place name? Administrative marker? | Single syllable; appears in KH11 also |
| SU as standalone | Category? Personal name? | Single syllable; appears in KH11 also |
| SI as standalone | Recipient name? | Single syllable; common in KH corpus |

---

## Structural Analysis

### Document Type

**Copper grading/allocation record using the Khania CYP system**

KH22 records copper transactions using the distinctive Khania grading system. CYP+E designates higher-grade copper (associated with integer quantities) while CYP alone (or CYP+D) designates lower-grade or unqualified copper.

### Document Structure

```
[H]  ZA                        Header: source / category
     𐄁                         Word divider
[?]  SU                        Qualifier / sub-category
[#]  7                         Quantity: 7 (associated with header section)
---
[C]  CYP+E                     Commodity: higher-grade copper
---
[R]  SI                        Recipient
[#]  4                         Quantity: 4 units (integer = CYP+E consistent)
---
[C]  CYP                       Commodity: copper (unqualified or lower grade)
---
[R]  𐝫                         [damaged/missing]
```

### Rosetta Skeleton (arithmetic_verifier output)

| Tag | Role | Count |
|-----|------|-------|
| [H] | Header | 1 (ZA) |
| [?] | Unknown | 1 (SU) |
| [#] | Quantity | 2 (7, 4) |
| [C] | Commodity | 2 (CYP+E, CYP) |
| [R] | Recipient | 2 (SI, 𐝫) |

### CYP Grading System Context

The Khania copper grading system (established in KH5, KH6, KH7a analyses):

| Grade | Logogram | Quantity Pattern | Interpretation |
|-------|----------|-----------------|----------------|
| **Higher** | CYP+E | **Integer** quantities | Higher-grade copper/bronze |
| **Lower** | CYP+D | **Fractional** quantities | Lower-grade copper/bronze |
| **Unqualified** | CYP | Mixed | Copper (grade unspecified) |

On KH22:
- CYP+E section: SI receives 4 (integer) -- **consistent with CYP+E = higher grade**
- CYP section: damaged entry -- cannot verify grade pattern

### Notable Structural Features

1. **Zero K-R vocabulary**: No KU-RO, KI-RO, SA-RA₂, PO-TO-KU-RO, or A-DU. Confirms the zero-K-R pattern at Khania (p=0.004).
2. **CYP+E present**: Higher-grade copper. Integer quantity (4) is consistent with the CYP+E = integers pattern.
3. **Two-section format**: CYP+E section followed by CYP section. Multi-grade copper accounting.
4. **Damaged final entry**: 𐝫 indicates missing/damaged content. The CYP section recipient and quantity are lost.
5. **Single-syllable words**: ZA, SU, SI -- typical of the Khania administrative vocabulary, which has minimal overlap with HT (1.8%).
6. **Compact format**: Brief tablet with only two commodity sections.

---

## Multi-Hypothesis Testing

### Key Term: ZA (Header)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| Luwian | Possible Luwian toponym/abbreviation | Single syllable; insufficient evidence | WEAK | ACTIVE |
| Semitic | No Semitic parallel | Single syllable | WEAK | ACTIVE |
| Pre-Greek | Pre-Greek toponym? | Cannot test | INDETERMINATE | ELIMINATED |
| Proto-Greek | No parallel | Cannot test | INDETERMINATE | ELIMINATED |
| Hurrian | No parallel | Cannot test | INDETERMINATE | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | Cannot test | INDETERMINATE | ELIMINATED |

**Best hypothesis**: INDETERMINATE. Single syllables cannot be meaningfully tested against linguistic hypotheses.
**Note**: ZA could be an abbreviation for Zakros (ZA = site code in modern notation) or another toponym, but this is SPECULATIVE.

### Key Term: SU (Qualifier)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| All | INDETERMINATE | Single syllable; insufficient evidence | INDETERMINATE | — |

**Best hypothesis**: INDETERMINATE. Same limitation as ZA.

### Key Term: SI (Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| All | INDETERMINATE | Single syllable; insufficient evidence | INDETERMINATE | — |

**Best hypothesis**: INDETERMINATE. Could be a personal name abbreviation or administrative category.

### Key Term: CYP+E (Higher-Grade Copper)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **All** | Higher-grade copper; CYP + E qualifier | Logogram + qualifier system; KH-specific | **HIGH** | N/A (logogram) |

**Confidence**: HIGH. CYP is a Level 3 logogram anchor. The +E qualifier distinguishes higher-grade copper within the Khania system.

### Hypothesis Summary for KH22

| Term | Best Hypothesis | Confidence | Alternative |
|------|-----------------|------------|-------------|
| ZA | INDETERMINATE | UNKNOWN | Single syllable |
| SU | INDETERMINATE | UNKNOWN | Single syllable |
| SI | INDETERMINATE | UNKNOWN | Single syllable |
| CYP+E | N/A (logogram) | HIGH | Higher-grade copper |
| CYP | N/A (logogram) | CERTAIN | Copper (ungraded) |
| 7, 4 | N/A (numerals) | CERTAIN | Unambiguous |

**Dominant pattern**: This tablet cannot discriminate linguistic hypotheses due to single-syllable words. Its value lies in confirming the Khania CYP grading system.

---

## Connected Reading Attempt

### Element-by-Element Interpretation

```
ZA                 "[From/Category] ZA"                  UNKNOWN
𐄁                  [word divider]                        CERTAIN
SU                 "[qualifier/sub-category]"             UNKNOWN
7                  "7 units"                              CERTAIN
CYP+E              "higher-grade copper"                  HIGH
SI                 "[Recipient] SI"                       UNKNOWN
4                  "4 units"                              CERTAIN
CYP                "copper (ungraded)"                    CERTAIN
𐝫                  [damaged/missing]                      —
```

### Full Interpretive Reading (Speculative)

> **ZA [source/category], SU [qualifier]: 7 [units]**
>
> **Higher-grade copper (CYP+E):**
> To SI: 4 units
>
> **Copper (CYP, ungraded):**
> [damaged/missing entry]
>
> *A copper allocation record at Khania, recording 7 units in the header section and distributing higher-grade copper (CYP+E, 4 units) to SI, with an additional ungraded copper entry (damaged).*

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| ZA = header | Source/category | UNKNOWN | Position-initial; single syllable |
| SU = qualifier | Sub-category | UNKNOWN | After header; single syllable |
| 7 = quantity | "7 units" | CERTAIN | Numeral |
| CYP+E = higher-grade copper | "Higher-grade copper" | HIGH | Logogram + KH grading system |
| SI = recipient | Person/category | UNKNOWN | Before quantity; single syllable |
| 4 = quantity | "4 units" | CERTAIN | Numeral; integer = CYP+E consistent |
| CYP = copper | "Copper (ungraded)" | CERTAIN | Level 3 logogram anchor |

---

## What We Know For Certain

1. **Copper commodity**: CYP and CYP+E logograms are present. This is a copper record. CERTAIN.
2. **CYP+E with integer**: The CYP+E section shows integer quantity (4), consistent with the higher-grade = integers pattern. CERTAIN.
3. **Zero K-R**: No KU-RO, KI-RO, SA-RA₂, or any K-R paradigm term. CERTAIN.
4. **Khania administrative system**: This tablet belongs to the parallel Khania system, not the HT system. CERTAIN.
5. **Damage**: Final entry is damaged (𐝫). The CYP section is incomplete. CERTAIN.

## What We Hypothesize

1. **ZA as source/toponym**: ZA in header position may designate the source of the copper. SPECULATIVE.
2. **SU as qualifier**: SU following ZA may specify a sub-category or quality descriptor. SPECULATIVE.
3. **SI as recipient**: SI receives 4 units of CYP+E copper. If SI is a personal name abbreviation, this is a named allocation. POSSIBLE.
4. **Two-grade accounting**: The CYP+E and CYP sections may record different copper grades from the same source (ZA), with separate allocation tracking. POSSIBLE.
5. **Missing CYP section**: The damaged CYP entry may have contained a fractional quantity (consistent with CYP+D = fractions pattern) or another integer. INDETERMINATE.

---

## Cross-Corpus Verification

### CYP+E Occurrences

| Tablet | Site | Quantity | Integer? | Consistent? |
|--------|------|----------|----------|-------------|
| KH5 | KH | Integer | Yes | Yes |
| KH7a | KH | Integer | Yes | Yes |
| KH11 | KH | 3 | Yes | Yes |
| **KH22** | **KH** | **4** | **Yes** | **Yes** |

**Verification**: CYP+E = integer quantities **CORPUS-VERIFIED** at Khania (4/4 instances integer).

### Zero K-R at Khania

| Tablet | K-R Terms? | Consistent? |
|--------|------------|-------------|
| KH5 | None | Yes |
| KH6 | None | Yes |
| KH7a | None | Yes |
| KH11 | None | Yes |
| **KH22** | **None** | **Yes** |
| KH88 | None | Yes |

**Verification**: Zero K-R at Khania now confirmed across **6+ analyzed KH tablets**. Regional agent reports p=0.004 (statistically significant absence).

### ZA / SU / SI at Khania

| Word | KH Tablets | Other Sites | Notes |
|------|-----------|-------------|-------|
| ZA | KH11, KH22 | Widespread | Also a site code (Zakros) |
| SU | KH11, KH22 | Less common | Co-occurs with ZA at KH |
| SI | KH22, others | Widespread | Common single syllable |

**Partial verification**: ZA and SU co-occur in KH11 and KH22, both in header-adjacent positions. This consistent co-occurrence at Khania may indicate a fixed pairing (source + qualifier) specific to the KH administrative system.

---

## First Principles Verification

### [1] KOBER: Was analysis data-led?
**PASS** -- Identified CYP logograms and structural patterns before linguistic analysis.

### [2] VENTRIS: Was any evidence forced?
**PASS** -- Single-syllable words left as UNKNOWN/INDETERMINATE. No etymological forcing.

### [3] ANCHORS: Were readings built from confirmed anchors outward?
**PASS** -- Level 3 (CYP, CYP+E logograms). Single-syllable words capped at UNKNOWN.

### [4] MULTI-HYP: Were ALL seven hypotheses tested?
**PASS** -- All logograms tested (all agree). Single syllables INDETERMINATE for all seven.

### [5] NEGATIVE: Was absence of patterns considered?
**PASS**

Absences:
- **Zero K-R**: No KU-RO, KI-RO, SA-RA₂, PO-TO-KU-RO, A-DU
- **No multi-syllable words**: All words are single syllables; limits linguistic analysis
- **No fractions visible**: Only integers present (7, 4); CYP section damaged
- **No *86+*188 roundel**: This is a tablet, not a roundel
- **No VIN/OLE/GRA**: Pure copper record; no mixed commodities

### [6] CORPUS: Were readings verified across all occurrences?
**PASS** -- CYP+E integer pattern CORPUS-VERIFIED. Zero K-R CORPUS-VERIFIED.

---

## Novel Observations

### 1. ZA-SU Pairing at Khania

ZA and SU appear together (in this order, header-adjacent) on both KH22 and KH11. This is a distinctive Khania pattern not seen at HT. If ZA designates a copper source (geographic origin) and SU qualifies the grade or type, this pairing may be a standardized Khania header formula for copper records.

### 2. CYP+E Integer Validation

KH22 provides the 4th confirmation of the CYP+E = integer quantities pattern (after KH5, KH7a, KH11). The pattern is now well-established: **CYP+E always appears with integers at Khania**. This is consistent with CYP+E representing a higher copper grade where integer quantities suffice (no need for fractional precision).

### 3. Compact Two-Section Format

KH22's two-section CYP record (CYP+E, then CYP) is the most compact multi-grade copper tablet analyzed. Compare KH11 (mixed CYP+VIN+*306, extensive fractions) and KH7a (CYP+D and CYP+E in same document). The simplicity of KH22 suggests either:
- A small transaction (only 2 entries)
- A summary or extract from a larger record
- A specific transaction with limited scope

---

## Sources Consulted

1. **lineara.xyz corpus** -- KH22 transliteration and metadata
2. **arithmetic_verifier** -- Rosetta skeleton
3. **KNOWLEDGE.md** -- KH system, CYP grading, zero K-R, Khania Inversion
4. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework
5. **KH5, KH6, KH7a, KH11 analyses** -- CYP grading cross-reference
6. **Regional agent** -- p=0.004 zero-K-R confirmation

---

*Connected reading completed 2026-02-22. KH22 is a compact copper grading record at Khania with CYP+E (4 integers) and CYP (damaged). Confirms CYP+E = integer pattern (4th instance) and zero-K-R at Khania (6th tablet). Single-syllable words (ZA, SU, SI) prevent linguistic hypothesis testing. ZA-SU pairing observed on both KH22 and KH11. Overall reading confidence: HIGH for CYP grading system; UNKNOWN for word meanings.*
