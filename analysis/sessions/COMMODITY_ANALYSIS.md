# Commodity Logogram Analysis

**Session Date**: 2026-01-31
**Analysis Type**: Systematic commodity and modifier survey
**Corpus Coverage**: Full corpus scan for OLE, VIN, GRA, CYP, OLIV, FAR, FIC

---

## Pre-Flight Check (FIRST_PRINCIPLES.md)

- [x] Analyzing patterns BEFORE assuming language [P1]
- [x] Prepared to abandon hypothesis if contradicted [P2]
- [x] All available anchors identified [P3]
- [x] Testing against all four hypotheses [P4]
- [x] Considering negative evidence [P5]
- [x] Verifying across corpus [P6]

---

## Executive Summary

Linear A commodity logograms show a sophisticated classification system using syllabic modifiers that appear to indicate **commodity subtypes**. The evidence suggests these modifiers represent:

1. **Processing state** (raw vs. refined)
2. **Quality grades** (primary, secondary)
3. **Source/origin** (geographic or botanical)
4. **Purpose/destination** (ritual, storage, distribution)

The modifier system parallels Linear B's acrophonic abbreviations but uses different phonetic values, suggesting either:
- Different terminology for the same concepts
- Different commodity classification priorities
- An underlying non-Greek vocabulary

---

## 1. OLE (Olive Oil) - Most Complex Modifier System

### Attestations

| Modifier | Occurrences | Notes |
|----------|-------------|-------|
| **OLE** (plain) | 22 | Base logogram |
| **OLE+U** | 22 | Most common variant |
| **OLE+KI** | 21 | Common variant |
| **OLE+MI** | 19 | Common variant |
| **OLE+DI** | 12 | Medium frequency |
| **OLE+NE** | 5 | Lower frequency |
| **OLE+E** | 4 | Rare variant |
| **OLE+A** | 2 | Rare variant |
| **OLE+QE+DI** | 1 | Complex modifier (hapax) |
| **OLE+KI+U** | 1 | Complex modifier (TY3a) |
| **OLE+KI+ME** | 1 | Complex modifier (TY3a) |
| **OLE+TU** | 1 | Rare (TY3a) |

### TY 3a Oil Tablet - Special Analysis

The TY 3a tablet from Tylissos lists at least **8 distinct oil types** in a single document:

```
ZA-*321    OLE+KI      15 1/4
           OLE+U       22
NE-KI                  5
           OLE+QIf     3 1/2
           OLE+MI      (quantity lost)
           OLE+U       7 1/2
---
A-DU       OLE+KI      51
           OLE+KI+U    2 1/5
           OLE+KI+ME   1
           OLE+QIf     4 1/2
           OLIV        4
---
A-DA       OLE+U       21
           OLE+MI      2
KO-A-DU-WA OLE         7 1/5
---
A-KU-TU-*361
           KI          5
           OLE+TU      1
```

**Key Observations (TY 3a)**:
1. Multiple oil types appear in **same accounting entry** - suggests quality/type differentiation
2. **OLE+KI+U** and **OLE+KI+ME** are complex compounds - possible subtypes of OLE+KI
3. Personal names (A-DA, KO-A-DU-WA, A-KU-TU-*361) receive different oil allocations
4. OLIV (whole olives) appears alongside OLE variants - confirming distinct commodities

### Slot Grammar Analysis - Pre-OLE Words

Words appearing BEFORE OLE modifiers (from slot_grammar_analysis.json):

| Word | Frequency | Likely Function |
|------|-----------|-----------------|
| **SA-RA2** | 2 | Administrative term (allocation?) |
| **JE-DI** | 2 | Personal name? |
| **SA-RO** | 2 | Personal name/title? |
| **A-DA** | 2 | Personal name |
| **KO-A-DU-WA** | 2 | Personal name |
| **A-KA-RU** | 1 | Personal name? |
| **ZA-*321** | 1 | Personal name? |
| **KI-RE-TA-NA** | 3 | Toponym or title |

**Pattern**: Personal names and administrative terms precede OLE variants, suggesting **allocation records**.

### Modifier Hypothesis Analysis

#### Hypothesis 1: Quality Grades

| Modifier | Proposed Meaning | Evidence |
|----------|------------------|----------|
| OLE+U | Primary/finest oil | Highest quantities; premium allocation |
| OLE+MI | Secondary grade | Lower quantities per entry |
| OLE+KI | Filtered/processed | Complex compounds (OLE+KI+U, OLE+KI+ME) |
| OLE+DI | Aged/stored | Different distribution pattern |
| OLE+NE | Fresh-pressed? | Limited attestation |

#### Hypothesis 2: Processing State (Linear B Parallel)

In Linear B (Melena 1983), oil modifiers use acrophonic abbreviations:
- OLE+WO = *wo-do-we* (rose-scented)
- OLE+RI = *ri-no* (linseed oil)
- OLE+PA = palm oil variant

**If Linear A follows similar pattern**:
| Modifier | Possible Acrophony | Reconstructed Word |
|----------|-------------------|-------------------|
| OLE+U | u-? | Unknown |
| OLE+KI | ki-? | *ki-ta* (garden/cultivation)? |
| OLE+MI | mi-? | *mi-tu* (mint)? *mi-ta* (aromatics)? |
| OLE+DI | di-? | Unknown |

**Critical Problem**: We cannot verify acrophonies without knowing the Minoan vocabulary.

#### Hypothesis 3: Geographic Origin

| Modifier | Possible Origin |
|----------|-----------------|
| OLE+KI | ki-ta, ki-ro region? |
| OLE+U | Unknown region |
| OLE+MI | Unknown region |

**Weakness**: No toponym evidence supports this interpretation.

### Multi-Hypothesis Testing

| Hypothesis | Luwian | Semitic | Pre-Greek | Proto-Greek |
|------------|--------|---------|-----------|-------------|
| Acrophonic system | POSSIBLE | POSSIBLE | POSSIBLE | POSSIBLE |
| Quality grades | POSSIBLE | POSSIBLE | POSSIBLE | POSSIBLE |
| Processing terms | NEUTRAL | NEUTRAL | NEUTRAL | NEUTRAL |
| Geographic origin | WEAK | WEAK | WEAK | WEAK |

**Result**: No hypothesis discriminates - modifier meanings remain UNDETERMINED.

---

## 2. VIN (Wine)

### Attestations

| Form | Occurrences | Notes |
|------|-------------|-------|
| **VIN** (plain) | 53 | Standard wine logogram |
| **VIN+KA** | 1 | Single attestation (ZA 6b) |
| **PU-VIN** | 2 | Compound with syllabic prefix |
| **VIR+KA-VIN** | 1 | Complex compound |

### Transaction Patterns

VIN frequently appears with **TE** transaction marker:
```
HT 9a:   SA-RO TE VIN
HT 13:   VIN TE (quantities follow)
HT 17:   RA-*164-TI TE VIN 37
HT 19:   RA-*164-TI TE VIN 30
```

**Pattern**: TE + VIN + NUMBER is a standard wine allocation formula.

### Pre-VIN Words (Slot Grammar)

| Word | Frequency | Likely Function |
|------|-----------|-----------------|
| **JA-*21F** | 2 | Administrative term? |
| **SA-RO** | 1 | Personal name/title |
| **PU-RA2** | 1 | Personal name? |
| **KU-RO** | 1 | Total marker |
| **KA-DI** | 1 | Unknown |

### Modifier Analysis

VIN shows **minimal modification** compared to OLE:
- Only 1 attestation of VIN+KA
- 2 attestations of PU-VIN (prefix, not suffix)

**Interpretation**: Wine was treated as a **more homogeneous commodity** than oil in Minoan accounting. Alternatively, wine quality distinctions existed but were marked differently (perhaps in preceding text, not ligatures).

### Semitic Parallel

The word **ya-ne** (appearing in wine contexts) may be cognate with Semitic *yayin* "wine":
- Hebrew: *yayin*
- Ugaritic: *yn*
- Akkadian: *inu*

**Confidence**: SPECULATIVE (limited attestation; could be loanword if valid)

---

## 3. GRA (Grain/Cereals)

### Attestations

| Form | Occurrences | Notes |
|------|-------------|-------|
| **GRA** (plain) | 62 | Base logogram |
| **GRA+PA** | 19 | Most common variant |
| **GRA+KU** | 7 | Medium frequency |
| **GRA+QE** | 4 | Lower frequency |
| **GRA+K+L** | 3 | Compound with fractions |
| **GRA+B** | 2 | Rare variant |
| **GRA+DA** | 1 | Single attestation |
| **GRA+H** | 1 | Single attestation |
| **GRA+E** | 1 | Single attestation |

### GRA+PA Analysis

GRA+PA appears in multiple contexts:
```
HT 102:   PA3-NI GRA+PA 33
HT 120:   GRA+PA 62 (after GRA+K+L 74)
HT 125b:  RE-TA2 GRA+PA 20
ZA 6a:    PU2-RA2 GRA+PA 20
ZA 11a:   KU-PA GRA+PA 1
```

**Possible Interpretations**:
1. **Processed grain** (flour?) - PA could be acrophonic for processing term
2. **Grain type** - specific variety (emmer, barley)
3. **Portion/ration** - administrative designation

### GRA+KU Analysis (HT 128 Focus)

HT 128a-b contains concentrated GRA+KU entries:
```
MI-TI      GRA+KU 6
WA-TU-MA-RE GRA+KU 12
(fragment) GRA+KU 6
VIR+[?]-*329 GRA+KU 1
(fragment) GRA+KU 6
```

**Observation**: GRA+KU appears with VIR (person ideogram) modifier, suggesting **ration allocation per person**.

### Pre-GRA Words (Slot Grammar - Top 10)

| Word | Frequency | Function |
|------|-----------|----------|
| **SA-RA2** | 5 | Allocation/grant |
| **KU-RO** | 3 | Total |
| **PI-*34-TE** | 2 | Unknown |
| **A-PU2-NA-DU** | 2 | Personal name |
| **KI-DA-TA** | 2 | Toponym? |
| **A-DU** | 2 | Administrative term |
| **SI-RU-MA-RI-TA2** | 2 | Personal name |
| **WA-TU-MA-RE** | 2 | Personal name |
| **TU-*21F-RI-NA** | 2 | Personal name |
| **PI-*314** | 2 | Unknown |

**Pattern**: SA-RA2 appears with GRA, OLE, and CYP - a **multi-commodity administrative term**.

---

## 4. CYP (Copper/Bronze)

### Attestations

| Form | Occurrences | Notes |
|------|-------------|-------|
| **CYP** (plain) | 52 | Standard metal logogram |
| **CYP+E** | 13 | Only common modifier |

### CYP+E Analysis

CYP+E appears predominantly at **Khania (KH)** site:
```
KH 5:   WI-SA-SA-NE CYP+E 2
KH 7a:  I CYP+E 1/16
KH 11:  A-TO-*349-TO-I CYP+E 3
KH 20:  A-SI-KI-RA CYP+E 1/3
KH 20:  DU-RE-ZA CYP+E 1/2
KH 34:  CYP+E 2
KH 54:  CYP+E 1
KH 58:  NI CYP+E 1 1/4
        A CYP+E 4
```

**Geographic Pattern**: 11 of 13 CYP+E occurrences are from Khania.

**Possible Interpretations**:
1. **Metal quality/purity** - +E indicates refined bronze?
2. **Regional preference** - Khania scribes used this distinction
3. **Time period** - Later convention?

### SA-RA2 with CYP

SA-RA2 + CYP appears multiple times:
```
HT 30:   SA-RA2 CYP 14
HT 94a:  SA-RA2 CYP 5
HT 99a:  SA-RA2 CYP 4
HT 100:  SA-RA2 CYP 5 1/4
HT 130:  SA-RA2 CYP (damaged)
```

**Confirms**: SA-RA2 is a **transaction term** not limited to agricultural products.

---

## 5. OLIV (Whole Olives)

### Attestations: 24 occurrences

### Distinction from OLE

OLIV clearly represents **whole olives** (fruit) vs. OLE (pressed oil):
- Appears alongside OLE in same tablets (TY 3a)
- Different quantities and allocation patterns
- Pictographic origin distinct

### HT 123+124a - Olive Distribution

```
KI-TA-I    OLIV 31
PU-VIN     OLIV 31 1/2
SA-RU      OLIV 16
DA-TU      OLIV 15
KU-RO      OLIV 93 1/2
```

**Key Insight**: KU-RO + OLIV confirms **totaling function** - the quantities sum to 93.5 units.

---

## 6. FAR and FIC

### FAR (Flour/Barley)

**No attestations found** in corpus search.

**Possible explanations**:
1. FAR may be a Linear B-specific logogram
2. May appear under different abbreviation in Linear A
3. May be subsumed under GRA variants

### FIC (Figs)

**No attestations found** in corpus search.

**Similar situation to FAR** - may use different notation in Linear A.

---

## 7. Slot Grammar Summary

### Top 20 Pre-Commodity Words

From slot_grammar_analysis.json (words appearing before logograms):

| Rank | Word | Frequency | Proposed Function |
|------|------|-----------|-------------------|
| 1 | **SA-RA2** | 18 | Allocation/grant (Akkadian *saraku*?) |
| 2 | **KU-RO** | 12 | Total/sum |
| 3 | **KU-PA** | 5 | Personal name? |
| 4 | **SA-RO** | 4 | Personal name/title |
| 5 | **PU-RA2** | 4 | Personal name? |
| 6 | **KI-RE-TA-NA** | 3 | Toponym or title |
| 7 | **JA-*21F** | 3 | Administrative term |
| 8 | **KI-RO** | 3 | Deficit/owed |
| 9 | **KU-PA3-NU** | 3 | Personal name? |
| 10 | **MA-DI** | 3 | Unknown |
| 11 | **SA-RU** | 3 | Personal name? |
| 12 | **TE-RI** | 3 | Unknown |
| 13 | **DA-RE** | 3 | Personal name? |
| 14 | **JE-DI** | 2 | Personal name? |
| 15 | **RU-ZU-NA** | 2 | Personal name? |
| 16 | **A-PU2-NA-DU** | 2 | Personal name |
| 17 | **WI-DI-NA** | 2 | Personal name? |
| 18 | **KI-DA-TA** | 2 | Toponym? |
| 19 | **DA-ME** | 2 | Community/people? |
| 20 | **MI-NU-TE** | 2 | Personal name/title |

### Suffix Frequency in Slot Words

| Suffix | Frequency | Possible Meaning |
|--------|-----------|------------------|
| **-RA** | 30 | ? |
| **-RO** | 23 | Masculine ending? |
| **-NA** | 19 | Feminine/locative? |
| **-TA** | 16 | ? |
| **-TI** | 12 | ? |
| **-RI** | 10 | ? |
| **-DI** | 9 | ? |
| **-TE** | 9 | ? |
| **-JA** | 8 | Religious/possessive? |
| **-DU** | 8 | Semitic influence? |

---

## 8. Transaction Signs

### TE Pattern

TE appears as a **transaction marker** before commodities:
```
Pattern: [header] TE COMMODITY NUMBER
```

Examples:
- HT 14: PU-VIN TE GRA 30
- HT 21: PI-TA-KA-SE TE GRA 161
- HT 40: NU-DU-*331 TE GRA 207
- HT 42+59: SI+SE TE OLE+KI 8

**Function**: TE likely marks **incoming** or **issued** transactions.

---

## 9. Synthesis and Conclusions

### Confirmed Patterns (HIGH confidence)

1. **Logograms are Level 3 anchors** - pictographic origin confirmed
2. **Modifiers indicate commodity subtypes** - not random variation
3. **SA-RA2 is multi-commodity administrative term** - appears with GRA, CYP, OLE
4. **KU-RO functions as total marker** - mathematical verification possible
5. **TY 3a demonstrates 8+ oil types** - sophisticated classification

### Probable Patterns (MEDIUM confidence)

1. **Modifiers use acrophonic abbreviation** - like Linear B but different values
2. **Quality/processing grades** - OLE+U, OLE+MI may indicate grades
3. **Regional scribal preferences** - CYP+E concentrated at Khania
4. **Personal names precede allocations** - slot grammar pattern

### Speculative Patterns (LOW confidence)

1. **Semitic administrative vocabulary** - SA-RA2 = *saraku*, KU-RO = *kull*
2. **Oil modifier meanings** - cannot verify without vocabulary
3. **Wine less differentiated than oil** - or differently marked

### Negative Evidence

1. **No FAR or FIC attestations** - may use different notation
2. **Wine modifiers rare** - only VIN+KA (1x), PU-VIN (2x)
3. **No clear geographic origins in modifiers** - hypothesis unsupported
4. **No verbal morphology visible** - consistent with isolating/agglutinative structure

---

## First Principles Verification

| Principle | Status | Evidence |
|-----------|--------|----------|
| [1] KOBER | PASS | Analysis led by frequency/distribution data |
| [2] VENTRIS | PASS | Geographic origin hypothesis abandoned for lack of evidence |
| [3] ANCHORS | PASS | Building from Level 3 logograms outward |
| [4] MULTI-HYP | PASS | All four hypotheses tested on modifier meanings |
| [5] NEGATIVE | PASS | FAR/FIC absence noted; wine modifier rarity noted |
| [6] CORPUS | PASS | Full corpus scan for each commodity |

---

## Sources Consulted

- Corpus data: lineara.xyz via tools/corpus_lookup.py
- Slot grammar: data/slot_grammar_analysis.json
- Linear B parallels: [Melena 1983 "Olive Oil and Other Sorts of Oil"](https://gredos.usal.es/bitstream/handle/10366/73447/Olive_Oil_and_Other_Sorts_of_Oil_in_the_.pdf)
- Methodology: FIRST_PRINCIPLES.md, methodology.md

---

## Recommendations for Further Analysis

1. **Complete TY 3 translation** - Most comprehensive oil type tablet
2. **Compare HT 128a/b with Linear B grain tablets** - GRA+KU pattern
3. **Map CYP+E geographic distribution** - Khania regional practice?
4. **Investigate GRA+PA function** - Most common grain modifier
5. **Search for FAR/FIC under alternate notation** - May be in corpus differently

---

*Analysis completed 2026-01-31 as part of OPERATION MINOS Phase 2*
