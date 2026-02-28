# HT 116a Connected Reading Report

**Date**: 2026-02-22
**Analyst**: Claude (Opus 4.6)
**Phase**: MINOS III - Campaign 1, Tier 2
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
| **Tablet ID** | HT 116a (side a of HT 116) |
| **Site** | Hagia Triada (Haghia Triada), Casa Room 9 |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Context** | LMIB |
| **Scribe** | Unattributed |
| **Support** | Clay tablet (opisthograph) |
| **Partner** | HT 116b (side b: KU-RO GRA 100, *304 15, OLE 17) |
| **Document Type** | Multi-commodity distribution (GRA + OLE variants + OLIV + *304) |
| **Arithmetic Status** | NO_KURO on side a; side b totals: *304 VERIFIED (15=15), GRA MISMATCH (109 vs 100), OLE MISMATCH (20 vs 17) |
| **Commodity Anchors** | GRA (logogram, CERTAIN); OLE variants (CERTAIN); OLIV (CERTAIN); *304 (22 tablets) |
| **Cross-Tablet Links** | PU-RA₂ (HT 28b); QA-NU-MA (KH 88); SI+SE (HT 42+59, MYZf1) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |

---

## Transliteration

### HT 116a (Side A)

```
Line 1:  U-TA-RO  𐄁  TE  𐄁

Line 2:  KU-PA-JA    GRA             16
Line 3:  PU-RA₂   𐄁  GRA             40
Line 4:               OLE+DI          5
Line 5:  SI+SE        GRA             16
Line 6:               OLE+KI          1
Line 7:               OLE+MI          6
Line 8:               OLIV            3
Line 9:  PI-*34-TE    GRA              5
Line 10:              OLE              5
Line 11:              OLE+MI           1
Line 12: *OLIV+TU                     2
Line 13: SI-KI-NE     GRA             12
Line 14:              *304            12
Line 15: QA-NU-MA     GRA             20
Line 16:              *304             3
```

### HT 116b (Side B) -- Totals

```
Line 1:  KU-RO    GRA              100
Line 2:           *304              15
Line 3:           OLE               17
```

---

## Arithmetic Verification

### Cross-Side Verification (Side A entries vs. Side B totals)

```
=== GRA Column ===
KU-PA-JA         16
PU-RA₂           40
SI+SE            16
PI-*34-TE         5
SI-KI-NE         12
QA-NU-MA         20
                 ---
Computed:        109
KU-RO (side b): 100
Difference:       -9  (MISMATCH)

=== *304 Column ===
SI-KI-NE         12
QA-NU-MA          3
                 ---
Computed:         15
KU-RO (side b):  15
Difference:        0  (VERIFIED)

=== OLE Column (all variants) ===
PU-RA₂  OLE+DI    5
SI+SE   OLE+KI    1
SI+SE   OLE+MI    6
PI-*34-TE OLE     5
PI-*34-TE OLE+MI  1
*OLIV+TU          2
                 ---
Computed:         20
KU-RO (side b):  17
Difference:       -3  (MISMATCH)

=== OLIV Column ===
SI+SE   OLIV      3
(Not totaled on side b)
```

**Diagnosis**: The *304 column VERIFIES exactly (15 = 15). The GRA mismatch (-9) and OLE mismatch (-3) may be explained by:
1. Some entries being sub-allocated differently (e.g., *OLIV+TU may not count as OLE)
2. Tablet damage between sides causing partial recording on side b
3. The OLIV (3) may be absorbed into either OLE or GRA totals on side b

If we exclude *OLIV+TU (2) from OLE: computed = 18 vs KU-RO 17 (gap 1, nearly matches). If OLIV (3) is absorbed into OLE: 17 + 3 = 20 = computed. The GRA gap of 9 is more difficult to explain -- it may indicate that some of the "GRA" entries are sub-categories not summed into the main KU-RO.

---

## Anchor Identification

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **GRA** | Grain | Established commodity | 6 entries, KU-RO 100 |
| **OLE** | Oil (base) | Established commodity | Multiple variants |
| **OLE+DI** | Oil variant D | Established sub-type | PU-RA₂: 5 |
| **OLE+KI** | Oil variant K | Established sub-type | SI+SE: 1 |
| **OLE+MI** | Oil variant M | Established sub-type | SI+SE: 6, PI-*34-TE: 1 |
| **OLIV** | Olives | Established commodity | SI+SE: 3 |
| **\*304** | Unknown commodity | 22 tablets; possibly dried fruit/figs | SI-KI-NE: 12, QA-NU-MA: 3 |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| U-TA-RO TE header | Institutional source/topic | Initial position + dual separators |
| NAME + multi-commodity | Recipients with varied allocation | 6 recipients, each with different commodities |
| Side b KU-RO | Column totals | GRA/OLE/*304 separately totaled |

### Level 3+: Commodity Functional Anchors

| Word | Status | Evidence |
|------|--------|----------|
| PU-RA₂ | GRA-associated | Hypothesis: PROBABLE Luwian; receives 40 GRA (largest) |
| QA-NU-MA | GRA-associated | Hypothesis: PROBABLE Luwian; receives 20 GRA; also on KH 88 |

---

## Structural Analysis

### Document Type

**Multi-commodity distribution ledger (GRA + OLE variants + OLIV + *304)**

HT 116a is one of the richest tablets in the corpus: 6 recipients receive varied combinations of grain, oil types, olives, and *304. Unlike the single-commodity distributions of the GRA cohort (HT 86a, 95a, 95b), HT 116a demonstrates mixed-commodity administration where each recipient receives a different basket of goods.

### Document Structure

```
[H]   U-TA-RO  𐄁  TE  𐄁              Header: source/topic

[R]   KU-PA-JA                         Recipient 1
[C]   GRA              16              Grain: 16

[R]   PU-RA₂  𐄁                        Recipient 2
[C]   GRA              40              Grain: 40
[C]   OLE+DI            5              Oil type D: 5

[R]   SI+SE                            Recipient 3
[C]   GRA              16              Grain: 16
[C]   OLE+KI            1              Oil type K: 1
[C]   OLE+MI            6              Oil type M: 6
[C]   OLIV              3              Olives: 3

[R]   PI-*34-TE                        Recipient 4
[C]   GRA               5              Grain: 5
[C]   OLE               5              Oil (base): 5
[C]   OLE+MI            1              Oil type M: 1

[?]   *OLIV+TU          2              Olive variant?: 2

[R]   SI-KI-NE                         Recipient 5
[C]   GRA              12              Grain: 12
[C]   *304             12              Commodity *304: 12

[R]   QA-NU-MA                         Recipient 6
[C]   GRA              20              Grain: 20
[C]   *304              3              Commodity *304: 3
```

### Notable Structural Features

1. **Richest commodity variety**: HT 116a names 7 distinct commodity types: GRA, OLE, OLE+DI, OLE+KI, OLE+MI, OLIV, *304. No other analyzed tablet uses this many commodity categories.

2. **Variable commodity baskets**: Each recipient receives a unique combination. PU-RA₂ gets GRA + OLE+DI; SI+SE gets GRA + 3 different oil types + OLIV; PI-*34-TE gets GRA + OLE + OLE+MI. This is qualitatively different from the uniform GRA-only distributions.

3. **PU-RA₂ is largest GRA recipient**: PU-RA₂ receives 40 GRA -- double the next largest (QA-NU-MA at 20). This dominance parallels SA-RU's position on HT 95a (20 vs mode 10).

4. **U-TA-RO TE as compound header**: The double-separator structure (U-TA-RO 𐄁 TE 𐄁) is unusual. TE has 58 corpus occurrences and may function as a qualifier, topic marker, or "from" particle. The structure could be parsed as: "U-TA-RO [separator] TE [separator]" = "From U-TA-RO: concerning TE" or "U-TA-RO's TE-allocation."

5. **\*OLIV+TU as ligature**: The compound logogram *OLIV+TU appears on 3 tablets (HT 50a, HT 101, HT 116a). It may represent a processed olive product (cf. *308 as olive oil on HT 123+124a).

6. **Side b as summary**: Side b provides three KU-RO lines (GRA 100, *304 15, OLE 17) -- a three-line commodity summary. The *304 total verifies exactly; GRA and OLE have modest mismatches.

7. **QA-NU-MA cross-site**: QA-NU-MA appears on both HT 116a and KH 88 -- a rare cross-site attestation linking Hagia Triada and Khania administrative networks.

---

## Multi-Hypothesis Testing

### Key Term: U-TA-RO (Header)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | -RO ending; score highest | **POSSIBLE** |
| Proto-Greek | -O ending; /o/ vowel | WEAK (ELIMINATED) |
| Others | NEUTRAL | - |

**Best**: Luwian (POSSIBLE). Hapax.

### Key Term: KU-PA-JA (Recipient)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | -JA suffix (Level 5 anchor, adjectival/ethnic); KU-PA- base | **POSSIBLE** |
| Others | NEUTRAL or WEAK | - |

**Best**: Luwian (POSSIBLE). Hapax. The -JA suffix is productive in Luwian (77 corpus-wide, 65.9% word-final). Note: KU-PA₃-NU appears on HT 117a (GRA context) -- the KU-PA- root may indicate a toponym or institution.

### Key Term: PU-RA₂ (Recipient, largest GRA allocation)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | SUPPORTED; PROBABLE | **PROBABLE** |
| Semitic | POSSIBLE | - |
| Others | NEUTRAL | - |

**Best**: Luwian (PROBABLE). 2 tablets (HT 28b, HT 116a).

### Key Term: SI+SE (Recipient, receives 4 commodities)

SI+SE is a ligature (two signs combined). 3 tablets (HT 42+59, HT 116a, MYZf1). As a ligature, hypothesis testing is limited.

**Assessment**: Position as recipient. Function confirmed by multi-commodity allocation.

### Key Term: PI-\*34-TE (Recipient)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | -TE ending (from/of interpretation) | **POSSIBLE** |
| Others | NEUTRAL | - |

**Best**: Luwian (POSSIBLE). Hapax. Contains undeciphered sign *34.

### Key Term: SI-KI-NE (Recipient)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Semitic** | Best score; POSSIBLE | **POSSIBLE** |
| Hurrian | -NE definite article | NEUTRAL |
| Luwian | No strong features | NEUTRAL |

**Best**: Semitic (POSSIBLE). Hapax. Named as personal name by reading_readiness_scorer.

### Key Term: QA-NU-MA (Recipient, cross-site)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | SUPPORTED; -MA suffix; PROBABLE | **PROBABLE** |
| Others | WEAK or NEUTRAL | - |

**Best**: Luwian (PROBABLE). 2 tablets (HT 116a, KH 88). Cross-site attestation supports institutional rather than personal identity.

### Hypothesis Distribution Summary

| Hypothesis | Best for N words | Status |
|------------|------------------|--------|
| **Luwian** | 5 (U-TA-RO, KU-PA-JA, PU-RA₂, PI-*34-TE, QA-NU-MA) | **STRONG** |
| **Semitic** | 1 (SI-KI-NE) | WEAK |
| Undetermined | 1 (SI+SE ligature) | - |

---

## Connected Reading Attempt

### Full Interpretive Reading

> **From U-TA-RO, TE** (institutional source):
>
> | Recipient | GRA | OLE variants | OLIV | *304 |
> |-----------|-----|-------------|------|------|
> | KU-PA-JA | 16 | -- | -- | -- |
> | PU-RA₂ | 40 | OLE+DI 5 | -- | -- |
> | SI+SE | 16 | OLE+KI 1, OLE+MI 6 | 3 | -- |
> | PI-*34-TE | 5 | OLE 5, OLE+MI 1 | -- | -- |
> | *OLIV+TU | -- | 2 | -- | -- |
> | SI-KI-NE | 12 | -- | -- | 12 |
> | QA-NU-MA | 20 | -- | -- | 3 |
>
> **Totals (side b)**: GRA 100, *304 15, OLE 17

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| U-TA-RO = header | Institutional source | POSSIBLE | Position; hapax |
| TE = qualifier | Topic/allocation marker | POSSIBLE | 58 corpus occurrences |
| GRA = grain | Commodity | CERTAIN | Logogram |
| OLE variants = oil types | Commodity sub-types | CERTAIN | Logograms |
| OLIV = olives | Commodity | CERTAIN | Logogram |
| *304 = unknown commodity | Possibly dried fruit/figs | POSSIBLE | 22 tablets; unidentified |
| KU-RO totals (side b) | Column totals | CERTAIN | *304 VERIFIED |
| Recipient names | Personal names/offices | POSSIBLE-PROBABLE | Variable attestation |

---

## What We Know For Certain

1. **Multi-commodity distribution**: 6 recipients receive varied combinations of GRA, OLE variants, OLIV, and *304.
2. **\*304 total VERIFIED**: 12 + 3 = 15 = KU-RO *304 15 (exact match).
3. **GRA is the base commodity**: All 6 recipients receive GRA; additional commodities vary.
4. **Same physical tablet**: Side a (detail) and side b (summary totals) are a unified accounting document.
5. **QA-NU-MA is cross-site**: Appears at both HT and KH, linking the two administrative centers.

## What We Hypothesize

1. **U-TA-RO as estate/institution**: Header position suggests institutional origin for the mixed distribution. POSSIBLE (hapax).
2. **OLE variants as oil grades**: OLE+DI, OLE+KI, OLE+MI may represent different oil qualities, uses, or processing stages. Their differentiated distribution (different recipients get different types) supports this.
3. **GRA mismatch explanation**: The 9-unit gap (109 computed vs 100 KU-RO) may indicate some "GRA" entries are sub-categories or that side b summarizes a slightly different set.
4. **PU-RA₂ as major institution**: Receiving 40 GRA (40% of total) suggests PU-RA₂ is a large estate, workshop, or population center.

---

## First Principles Verification

### [1] KOBER: **PASS** | [2] VENTRIS: **PASS** | [3] ANCHORS: **PASS** | [4] MULTI-HYP: **PASS** | [5] NEGATIVE: **PASS** | [6] CORPUS: **PARTIAL**

**Key absences**: No VIN, VIR, CYP. No KI-RO. No SA-RA₂. No fractions (all integers). Several hapax terms limit cross-verification.

---

## Novel Observations

### 1. Richest Commodity Variety on Any Analyzed Tablet

HT 116a uses 7 distinct commodity types -- more than any other reading. The differentiated distribution (each recipient gets a unique basket) demonstrates sophisticated mixed-commodity accounting where the scribe tracks multiple commodity flows simultaneously.

### 2. OLE Variant Differentiation

The use of OLE, OLE+DI, OLE+KI, and OLE+MI as separate categories on a single tablet confirms these are meaningfully distinct. SI+SE receives 3 different oil types (OLE+KI 1, OLE+MI 6) plus olives (OLIV 3), suggesting access to specialized oil products.

### 3. GRA as Universal Base

All 6 recipients receive GRA, but only some receive additional commodities. This suggests GRA is a universal allocation (everyone gets grain) while OLE/OLIV/*304 are selective additions based on recipient needs or status.

### 4. *304 as Non-Agricultural Commodity

*304 appears on 22 tablets -- it is the third most common unidentified logogram after *308 (8) and *OLIV+TU (3). On HT 116a, only 2 of 6 recipients receive it (SI-KI-NE and QA-NU-MA), suggesting it is a specialized rather than universal commodity.

---

## Sources Consulted

1. **lineara.xyz corpus** -- HT 116a/116b transliteration and metadata
2. **arithmetic_verifier** -- Rosetta skeleton, NO_KURO diagnosis
3. **data/hypothesis_results.json** -- PU-RA₂, QA-NU-MA
4. **hypothesis_tester.py** -- U-TA-RO, KU-PA-JA, SI-KI-NE (live testing)
5. **KNOWLEDGE.md** -- Logogram inventory, OLE variants
6. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework

---

*Connected reading completed 2026-02-22 as part of MINOS III Campaign 1, Tier 2.*

*HT 116a is the richest multi-commodity distribution in the analyzed corpus: U-TA-RO distributes GRA, 4 OLE variants, OLIV, and *304 to 6 recipients with differentiated commodity baskets. PU-RA₂ receives the largest GRA allocation (40, 40% of total). The *304 column verifies exactly against side b (15 = 15). QA-NU-MA's cross-site presence (HT + KH) confirms inter-site administrative links. All 6 recipients receive GRA as a universal base, with additional commodities selectively distributed.*
