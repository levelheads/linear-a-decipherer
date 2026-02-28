# HT 9a Connected Reading Report

**Date**: 2026-02-21
**Analyst**: Claude (Opus 4.6)
**Status**: COMPLETE
**Arithmetic**: MISMATCH (KU-RO = 31.75, computed = 31.0, difference = 0.75, 7 items)

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
| **Tablet ID** | HT 9a (side a of HT 9) |
| **Site** | Hagia Triada (Haghia Triada), Villa Magazine |
| **Museum** | Heraklion Museum (HM 13) |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Context** | LMIB |
| **Scribe** | Unavailable |
| **Support** | Clay tablet (page tablet, opisthograph) |
| **Reference** | GORILA Vol. I, pp. 18-19 (page 54 of PDF) |
| **Source URL** | https://lineara.xyz/items/HT9a.html |
| **Findspot** | Villa Magazine |
| **Partner** | HT 9b (other side of same physical tablet -- already read, v0.7.0) |

---

## Transliteration

### HT 9a (Side A)

```
Line 1:  SA-RO | TE | VIN |
Line 2:  PA-DE | 5 J E [= 5.75]
Line 2-3: *306-TU 10
Line 3:  DI-NA-U 4
Line 3-4: QE-PU 2
Line 4:  *324-DI-RA 2 J [= 2.5]
Line 4-5: TA-I-AROM 2 J [= 2.5]
Line 5-6: A-RU 4 E [= 4.25]
Line 6:  KU-RO 31 J E [= 31.75]
```

### HT 9b (Side B) -- for cross-reference (already read)

```
Line 1:  PA3 |
         WA-JA-PI
         ________________________
Line 2:  KA-*305 |
         PA-DE         3
Line 2-3: A-SI         3
Line 3:  *306-TU       8
Line 3:  *324-DI-RA    2
Line 4:  QE-PU         2
Line 4:  TA-I-AROM     2
Line 5:  DI-NA-U       4
Line 6:  KU-RO        24
```

### Sign Number Assignments

| Sign | AB Number | Confidence |
|------|-----------|------------|
| SA | AB 31 | CERTAIN |
| RO | AB 02 | CERTAIN |
| TE | AB 04 | CERTAIN |
| PA | AB 03 | CERTAIN |
| DE | AB 45 | CERTAIN |
| TU | AB 69 | CERTAIN |
| DI | AB 07 | CERTAIN |
| NA | AB 06 | CERTAIN |
| U | AB 10 | CERTAIN |
| QE | AB 78 | HIGH |
| PU | AB 18 | CERTAIN |
| RA | AB 60 | CERTAIN |
| TA | AB 59 | CERTAIN |
| I | AB 28 | CERTAIN |
| A | AB 08 | CERTAIN |
| RU | AB 26 | CERTAIN |
| KU | AB 81 | CERTAIN |

### Undeciphered Signs

| Sign | Status | Notes |
|------|--------|-------|
| *306 | No phonetic value assigned | Appears as *306-TU on both sides of HT 9; also on HT 119, HT 122a |
| *324 | No phonetic value assigned | Appears as *324-DI-RA on both sides of HT 9; also on HT 122a |
| *123/AROM | Dual interpretation | May equal Linear B AROM (herbs/spices) or have phonetic value (Younger 2023) |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None identified on this tablet.**

### Level 2: Linear B Cognates + Position (HIGH)

| Term | Interpretation | Evidence | Occurrences |
|------|----------------|----------|-------------|
| **KU-RO** | total/sum | List-final position; Semitic *kull* "all/total" (Gordon 1966); sum checked mathematically | 39 corpus-wide |

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **VIN** | Wine | Pictographic origin + Linear B cognate; standardized commodity logogram | Header position, commodity identifier |
| **AROM** (*123) | Herbs, condiments, spices | Linear B cognate; but here possibly given phonetic value (Younger 2023) | In TA-I-AROM |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| SA-RO \| TE \| VIN header | Heading line: qualifier + separator + commodity | Standard administrative header format |
| NAME + QUANTITY | Standard list entry format | 7 entries follow consistent pattern |
| KU-RO at end | Totaling line | Standard accounting closure |
| Separator marks (\|) | Section dividers | Physical word dividers on tablet |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Instances | Notes |
|---------|-----------|-------|
| -U ending | DI-NA-U, *306-TU | Possible Luwian nominal class marker (64% Luwian) |
| -RA ending | *324-DI-RA | May be adjectival suffix |
| -DE ending | PA-DE | Possible Luwian ablative/locative |
| Compound with AROM | TA-I-AROM | Two syllables + logogram/qualifier |
| -RU ending | A-RU | May be nominal (-RU/-RE paradigm) |

---

## Structural Analysis

### Document Type

**Single-commodity distribution list** -- records allocations of wine (VIN) to 7 named recipients, with arithmetic totaling.

### Document Structure (HT 9a)

```
[H] SA-RO |                Header qualifier
[S] TE |                   Separator/transaction marker
[C] VIN |                  Commodity: WINE
[R] PA-DE         5.75     Recipient 1 (5 J E)
[R] *306-TU      10        Recipient 2 (largest allocation)
[R] DI-NA-U       4        Recipient 3
[R] QE-PU         2        Recipient 4
[R] *324-DI-RA    2.5      Recipient 5 (2 J)
[R] TA-I-AROM     2.5      Recipient 6 (2 J)
[R] A-RU          4.25     Recipient 7 (4 E)
[T] KU-RO        31.75     Total (31 J E)
```

### Rosetta Skeleton

| Position | Term | Role | Quantity | Confidence |
|----------|------|------|----------|------------|
| Header | SA-RO | Heading qualifier or toponym | -- | POSSIBLE |
| Separator | TE | Structural marker | -- | PROBABLE |
| Commodity | VIN | Wine logogram | -- | **CERTAIN** |
| Entry 1 | PA-DE | Recipient (personal name or toponym) | 5.75 | PROBABLE (name) |
| Entry 2 | *306-TU | Recipient | 10 | PROBABLE (name) |
| Entry 3 | DI-NA-U | Recipient (toponym per Younger) | 4 | PROBABLE (toponym) |
| Entry 4 | QE-PU | Recipient (personal name or title) | 2 | POSSIBLE |
| Entry 5 | *324-DI-RA | Recipient | 2.5 | PROBABLE (name) |
| Entry 6 | TA-I-AROM | Recipient or qualified allocation | 2.5 | POSSIBLE |
| Entry 7 | A-RU | Recipient | 4.25 | PROBABLE (name) |
| Total | KU-RO | Sum | 31.75 | **HIGH** |

---

## Arithmetic Verification

### HT 9a Sum Check

| Recipient | Quantity |
|-----------|----------|
| PA-DE | 5 J E (= 5.75, if J = 1/2, E = 1/4) |
| *306-TU | 10 |
| DI-NA-U | 4 |
| QE-PU | 2 |
| *324-DI-RA | 2 J (= 2.5) |
| TA-I-AROM | 2 J (= 2.5) |
| A-RU | 4 E (= 4.25) |
| **Computed Sum** | **31.00** |
| **Stated KU-RO** | **31 J E (= 31.75)** |

**RESULT: MISMATCH** -- Computed 31.00, stated 31.75. Difference = 0.75 (= J + E).

**Diagnosis**: fraction_parsing (arithmetic_verifier). The discrepancy is exactly J + E (0.75). This is methodologically significant: HT 9b (the reverse side) verifies EXACTLY at 24, while side a shows a systematic 0.75 overshoot in the stated total.

**Younger's Commentary**: Younger (2023) discusses this discrepancy: "assuming KU-RO = total, J=1/2, & E=1/4: the total 29+3J+2E equals 31, not 31+J+E." He suggests PA3 on side b might denote a correction: "WA-JA-PI minus JE."

**Possible Explanations**:
1. An additional fraction was recorded but is now lost/damaged
2. The total includes an adjustment not captured in individual entries
3. Fraction values J and E are not exactly 1/2 and 1/4
4. A scribal correction was applied to the total

### HT 9b Sum Check (Cross-Reference -- already verified)

| **Computed Sum** | **24** |
| **Stated KU-RO** | **24** |
| **RESULT** | **VERIFIED** |

---

## The Opisthograph Relationship: HT 9a / HT 9b

### This is the most significant structural feature of this tablet.

HT 9a and HT 9b are two sides of the same physical clay tablet. The relationship between them is systematic and informative.

### Side-by-Side Comparison

| Recipient | HT 9a (Side A) | HT 9b (Side B) | Difference | Direction |
|-----------|-----------------|-----------------|------------|-----------|
| PA-DE | 5.75 | 3 | -2.75 | Decrease |
| *306-TU | 10 | 8 | -2 | Decrease |
| DI-NA-U | 4 | 4 | 0 | Same |
| QE-PU | 2 | 2 | 0 | Same |
| *324-DI-RA | 2.5 | 2 | -0.5 | Decrease |
| TA-I-AROM | 2.5 | 2 | -0.5 | Decrease |
| A-RU | 4.25 | (absent) | -4.25 | Absent |
| A-SI | (absent) | 3 | +3 | New on side b |
| **KU-RO** | **31.75** | **24** | **-7.75** | Decrease |

### Shared Recipients (5 of 7)

Five recipients appear on BOTH sides with the SAME or reduced quantities:

1. **PA-DE**: 5.75 (a) vs. 3 (b) -- appears first on both sides
2. ***306-TU**: 10 (a) vs. 8 (b) -- largest individual allocation on both sides
3. **DI-NA-U**: 4 (a) vs. 4 (b) -- identical on both sides
4. **QE-PU**: 2 (a) vs. 2 (b) -- identical on both sides
5. ***324-DI-RA**: 2.5 (a) vs. 2 (b) -- reduced
6. **TA-I-AROM**: 2.5 (a) vs. 2 (b) -- reduced

### Side-Specific Recipients

- **A-RU** appears only on side a (4.25 units) -- absent from side b
- **A-SI** appears only on side b (3 units) -- absent from side a
- **Younger (2023)** suggests A-SI on side b could alternatively be read as A-RU. If so, all recipients overlap.

### Key Structural Observations

1. **Side a has fractions; side b has only whole integers** -- different recording granularity
2. **Side a explicitly names the commodity (VIN)** -- side b omits it (implied)
3. **Side b quantities are always <= side a quantities** -- systematic decrease
4. **The net difference is 7.75 units** (31.75 - 24 = 7.75)
5. **Side b has additional header elements** (PA3, WA-JA-PI, KA-*305) not present on side a

### Structural Interpretation

**Hypothesis A: Double-Entry Accounting** -- Side a records the full allocation (what is owed), side b records what was actually disbursed. The difference represents outstanding balances.

**Hypothesis B: Two Periods** -- Side a records allocations from one period (with fractional adjustments), side b records allocations from a second period (round numbers only).

**Hypothesis C: Correction/Adjustment** -- Side b is a corrected or adjusted version of side a.

**Our Assessment**: Hypothesis A (double-entry accounting) best explains the data because:
- The quantities decrease uniformly (never increase, except for A-SI which may be A-RU)
- The whole-number nature of side b suggests it records actual physical disbursements
- The fractional nature of side a suggests it records calculated entitlements
- A-RU's absence from side b could mean this recipient received nothing in the actual disbursement

**Confidence**: POSSIBLE (structural pattern is clear, but functional interpretation remains uncertain)

---

## Multi-Hypothesis Testing

### Surviving Hypotheses Only (Luwian STRONG, Semitic MODERATE)

Per METHODOLOGY.md: All seven hypotheses must be tested for compliance, but analytical focus prioritizes the two surviving hypotheses.

### Key Term: SA-RO

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Semitic** | Akkadian *sharru* "king" (partial); biconsonantal S-R root | S-R paradigm documented in KNOWLEDGE.md (SA-RA2, SA-RU, SA-RO, SI-RU) | **POSSIBLE** |
| **Luwian** | *sa-* conjunction + *-ro* nominal | Morphological decomposition; but SA-RO belongs to S-R consonant skeleton | POSSIBLE |
| **Proto-Greek** | Contains /o/ (RO) -- slightly favors Greek | But /o/ at 3.9% in corpus argues against genetic Greek | WEAK |
| **Pre-Greek** | Vowel alternation a/o pattern | Characteristic Pre-Greek feature | WEAK |
| **Hurrian** | No parallel | -- | NEUTRAL |
| **Hattic** | SA- prefix matches causative | Single feature | NEUTRAL |
| **Etruscan** | No parallel | -- | NEUTRAL |

**Best fit**: Semitic (POSSIBLE)
**Project tools**: best=semitic, conf=POSSIBLE
**Corpus note**: SA-RO has 4 attestations (HT 9a, HT 17, HT 19, HT 42+59), all at HT. Part of S-R consonant skeleton (SA-RA2 20 occ, SA-RU 6, SA-RO 4, SI-RU 4). In this context, SA-RO precedes TE and VIN, functioning as a heading element -- possibly "allocation [of/from]" consistent with the S-R paradigm's proposed administrative function.
**Confidence**: POSSIBLE

### Key Term: PA-DE

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Proto-Greek** | *pater* "father" (truncated?); *pan* "all" | Phonological similarity; tool result best=protogreek | POSSIBLE |
| **Luwian** | *pata-* "foot" + locative -i > "at the foot of" | Morphological pattern; Luwian locative formations | POSSIBLE |
| **Semitic** | Akkadian *padu* "ransom, payment" | Administrative vocabulary fit | POSSIBLE |
| **Pre-Greek** | Substrate personal name | Position as recipient | POSSIBLE |
| **Hurrian** | No clear parallel | -- | NEUTRAL |
| **Hattic** | No parallel | -- | NEUTRAL |
| **Etruscan** | No parallel | -- | NEUTRAL |

**Best fit**: Multi-hypothesis (no decisive evidence)
**Project tools**: best=protogreek, conf=POSSIBLE (but Proto-Greek ELIMINATED; tool result reflects phonological similarity only)
**Corpus note**: PA-DE appears on HT 9a (5.75), HT 9b (3), and HT 122a (1). Consistent function as recipient across all three tablets. The HT 122a appearance is significant -- a different tablet with different header (RA-RI) but same function as recipient with quantity.
**Confidence**: POSSIBLE

### Key Term: DI-NA-U

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Luwian** | *Tina-* personal/divine name + *-u* nominal suffix | -U ending favors Luwian (64%); morphological fit | **PROBABLE** |
| **Proto-Greek** | *Dionysus* (initial match) | Phonological similarity only; Proto-Greek ELIMINATED | WEAK |
| **Semitic** | No clear root | -- | WEAK |
| **Pre-Greek** | Substrate toponym | Younger suggests toponym (place known for wine) | POSSIBLE |
| **Hurrian** | *tin-* root | Limited evidence | WEAK |
| **Hattic** | No parallel | -- | NEUTRAL |
| **Etruscan** | *tina* "day" (single lexical match) | Insufficient | WEAK |

**Best fit**: Luwian (PROBABLE)
**Project tools**: best=luwian, conf=PROBABLE
**Younger's commentary**: "DI-NA-U is a place known at least for its VIN" -- confirmed by KN Zb 27 (DI-NA-U VIN 17)
**Cross-corpus**: 5 attestations -- HT 9a (4), HT 9b (4), HT 16, HT 25a, KN Zb 27 (17). Cross-site attestation (HT + KN) strengthens toponym interpretation. Value of 4 on both sides of HT 9 is notable (same allocation regardless of side).
**Confidence**: PROBABLE

### Key Term: QE-PU

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Luwian** | Unknown | No clear Luwian parallel | POSSIBLE |
| **Semitic** | Akkadian *qepu* "entrusted, commissioner" | Administrative title; semantic fit | POSSIBLE |
| **Proto-Greek** | No cognate | -- | NEUTRAL |
| **Pre-Greek** | Substrate personal name | Position as recipient | POSSIBLE |
| **Hurrian** | No parallel | -- | NEUTRAL |
| **Hattic** | No parallel | -- | NEUTRAL |
| **Etruscan** | No parallel | -- | NEUTRAL |

**Best fit**: Luwian (tool result) or Semitic (multi-hypothesis)
**Project tools**: best=luwian, conf=POSSIBLE
**Corpus note**: QE-PU appears only on HT 9 (both sides), with identical quantity (2) on each. This fixed allocation is notable. Limited attestation (2 inscriptions, same tablet) prevents cross-corpus verification.
**Confidence**: POSSIBLE

### Key Term: TA-I-AROM

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Semitic** | *ta-* prefix + AROM (commodity determinative) | AROM = herbs/spices (Linear B cognate); *ta-* as demonstrative/article | **PROBABLE** |
| **Luwian** | TA-I compound + AROM qualifier | TA-I as possible name; AROM as category | POSSIBLE |
| **Proto-Greek** | No cognate | -- | WEAK |
| **Pre-Greek** | Substrate + logographic qualifier | Possible mixed notation | POSSIBLE |
| **Hurrian** | No parallel | -- | NEUTRAL |
| **Hattic** | No parallel | -- | NEUTRAL |
| **Etruscan** | No parallel | -- | NEUTRAL |

**Best fit**: Semitic (PROBABLE)
**Project tools**: best=semitic, conf=PROBABLE
**Critical note**: Younger (2023) identifies *123 as "the same as Linear B AROM (herbs, condiments, spices), but here given a phonetic value." If AROM is logographic, TA-I-AROM means "TA-I [recipient], [allocation of] aromatics." If phonetic, the entire sequence is a personal name.
**Cross-corpus**: 3 attestations -- HT 9a (2.5), HT 9b (2), HT 39 (TA-I-*123). The AROM/*123 notation varies between sources, confirming the logographic/phonetic ambiguity.
**Confidence**: POSSIBLE (AROM ambiguity limits certainty)

### Key Term: A-RU

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Semitic** | Multiple partial cognates including *arru* "wine" (Akkadian) | Extensive partial matches; administrative vocabulary | **PROBABLE** |
| **Luwian** | A- conjunction prefix + -RU nominal | Morphological decomposition | POSSIBLE |
| **Proto-Greek** | *Artemis*, *Amnisos* (initial matches) | Phonological similarity only | POSSIBLE |
| **Pre-Greek** | Prothetic vowel before consonant | Pre-Greek substrate feature | WEAK |
| **Hurrian** | No parallel | -- | NEUTRAL |
| **Hattic** | A- prefix (3sg subject) | Single feature | NEUTRAL |
| **Etruscan** | No parallel | -- | NEUTRAL |

**Best fit**: Semitic (PROBABLE)
**Project tools**: best=semitic, conf=PROBABLE, multi=True
**Corpus note**: A-RU appears on HT 9a (4.25) and HT 49a. Only 2 attestations. On HT 9a, A-RU is the ONLY recipient that does NOT appear on side b -- this is structurally significant. If A-SI on side b = A-RU (Younger's suggestion), then the discrepancy is resolved but quantities differ (4.25 vs. 3).
**Confidence**: POSSIBLE (limited attestation)

### Key Term: KU-RO

| Hypothesis | Proposed Etymology | Evidence | Rating |
|------------|-------------------|----------|--------|
| **Semitic** | Akkadian *kull* "totality, all" | Gordon (1966); 39 corpus-wide attestations; mathematical verification across multiple tablets | **CERTAIN** |
| **Luwian** | No Luwian parallel for this function | -- | WEAK |
| **Proto-Greek** | *kyrios* "lord, complete"? | Phonological similarity but semantic stretch | WEAK |
| **Pre-Greek** | Substrate administrative term | Possible but no etymology | POSSIBLE |
| **Hurrian** | No parallel | -- | WEAK |
| **Hattic** | No parallel | -- | WEAK |
| **Etruscan** | No parallel | -- | WEAK |

**Best fit**: Semitic (CERTAIN -- Level 2 anchor)
**Arithmetic**: MISMATCH on this tablet (31.00 computed vs. 31.75 stated), but VERIFIED on side b (24 = 24)
**Confidence**: CERTAIN (function), PROBABLE (etymology)

### Hypothesis Summary for HT 9a

| Term | Best Hypothesis | Confidence | Alternative |
|------|-----------------|------------|-------------|
| SA-RO | Semitic | POSSIBLE | S-R paradigm member |
| TE | Structural marker | PROBABLE | Separator/transaction |
| VIN | Logogram | **CERTAIN** | Wine |
| PA-DE | Multi-hypothesis | POSSIBLE | Name (3 tablets) |
| *306-TU | UNKNOWN | UNKNOWN | Name with undeciphered sign |
| DI-NA-U | Luwian | **PROBABLE** | Toponym (Younger, cross-site) |
| QE-PU | Luwian/Semitic | POSSIBLE | Name or title |
| *324-DI-RA | UNKNOWN | UNKNOWN | Name with undeciphered sign |
| TA-I-AROM | Semitic | PROBABLE | AROM ambiguity |
| A-RU | Semitic | PROBABLE | Name (limited attestation) |
| KU-RO | Semitic | **CERTAIN** | *kull* "total" |

**Dominant pattern**: Administrative vocabulary (KU-RO) is Semitic; names with syllabographic readings (DI-NA-U, QE-PU) lean Luwian in project tools. This is consistent with the established domain-specific layering pattern: Luwian morphological substrate + Semitic administrative loans.

---

## Connected Reading Attempt

### Interpretive Translation

```
SA-RO [heading qualifier/allocation term]            (POSSIBLE)
TE [separator/transaction marker]                     (PROBABLE)
VIN [WINE]                                            (CERTAIN)

PA-DE         5.75  [recipient: 5 3/4 units wine]     (name PROBABLE)
*306-TU      10     [recipient: 10 units wine]        (name PROBABLE)
DI-NA-U       4     [recipient/toponym: 4 units wine] (PROBABLE)
QE-PU         2     [recipient: 2 units wine]         (name POSSIBLE)
*324-DI-RA    2.5   [recipient: 2 1/2 units wine]     (name PROBABLE)
TA-I-AROM     2.5   [recipient: 2 1/2 units wine]     (POSSIBLE)
A-RU          4.25  [recipient: 4 1/4 units wine]     (name POSSIBLE)
KU-RO        31.75  [total: 31 3/4]                   (CERTAIN)
```

### Full Interpretive Translation (Speculative)

> **Wine Distribution Record** (Side A)
>
> [Allocation/From:] SA-RO
> [Transaction marker:] TE
> [Commodity:] Wine (VIN)
>
> To PA-DE: 5 3/4 [units of wine]
> To *306-TU: 10 [units of wine] (largest individual allocation)
> To DI-NA-U (locality?): 4 [units of wine]
> To QE-PU: 2 [units of wine]
> To *324-DI-RA: 2 1/2 [units of wine]
> To TA-I (of aromatics?): 2 1/2 [units of wine]
> To A-RU: 4 1/4 [units of wine]
>
> **Total: 31 3/4** [stated; computed entries sum to 31]

### Commodity Identification

The commodity is explicitly stated in the header: **VIN (wine)**. This is one of the clearest commodity identifications in the HT corpus. The VIN logogram is a Level 3 anchor (CERTAIN).

This explicit commodity identification distinguishes side a from side b, where no commodity logogram appears and the wine distribution is inferred from side a's header.

---

## What We Know for Certain

1. **The commodity is wine (VIN)**: Explicitly stated in the header -- Level 3 anchor
2. **KU-RO = 31.75 is the stated total**: Level 2 anchor; function as total marker is CERTAIN
3. **Seven named entries precede KU-RO**: Standard distribution list structure
4. **Five recipients appear on both sides of HT 9**: PA-DE, *306-TU, DI-NA-U, QE-PU, *324-DI-RA, TA-I-AROM (5 shared of 7 on each side)
5. **The computed sum is 31.00, not 31.75**: A discrepancy of exactly 0.75 (J + E)
6. **Side a uses fractions (J and E), side b uses only integers**: Different recording granularity
7. **The tablet is an opisthograph**: Both sides are parts of a coordinated accounting document
8. **DI-NA-U receives 4 on both sides**: Stable allocation regardless of side

## What We Hypothesize

1. **DI-NA-U is a toponym** (PROBABLE): Younger identifies it as "a place known at least for its VIN"; cross-site attestation at Knossos (KN Zb 27) supports this
2. **SA-RO is an S-R paradigm member** (POSSIBLE): Part of the SA-RA2/SA-RU/SA-RO/SI-RU pattern of administrative terms
3. **TA-I-AROM involves the AROM commodity determinative** (POSSIBLE): Dual interpretation (logographic vs. phonetic) unresolved
4. **A-RU's absence from side b is structurally significant** (POSSIBLE): May indicate zero disbursement if sides represent allocation vs. disbursement
5. **The 0.75 discrepancy is intentional or structural** (POSSIBLE): Exactly J + E; may represent an adjustment, additional entry, or different fraction system
6. **The a/b relationship is double-entry accounting** (POSSIBLE): Systematic decrease from side a to side b

---

## Cross-Corpus Verification

### DI-NA-U Occurrences

| Tablet | Context | Quantity | Consistent? |
|--------|---------|----------|-------------|
| HT 9a | Recipient in VIN distribution | 4 | Yes -- same value as HT 9b |
| HT 9b | Recipient in distribution | 4 | Yes -- same value as HT 9a |
| HT 16 | In heading position | -- | Yes -- heading function |
| HT 25a | Contributes personnel | -- | Yes -- administrative |
| KN Zb 27 | DI-NA-U VIN 17 | 17 | Yes -- wine context at Knossos |

**Verification**: DI-NA-U consistently appears in administrative contexts, frequently with wine (VIN). Cross-site attestation (HT + KN) is significant. Reading as toponym is **CORPUS-VERIFIED** (per Younger 2023).

### KU-RO Occurrences (Selective)

| Tablet | Value | Verified? |
|--------|-------|-----------|
| HT 9a | 31.75 | MISMATCH (31.00 computed) -- this analysis |
| HT 9b | 24 | **VERIFIED** |
| HT 85a | 66 | **VERIFIED** |
| HT 117a | 10 | **VERIFIED** |
| HT 122a/b | 97 (PO-TO-KU-RO) | VERIFIED |

### PA-DE Occurrences

| Tablet | Context | Quantity | Notes |
|--------|---------|----------|-------|
| HT 9a | Recipient in VIN distribution | 5.75 | First entry |
| HT 9b | Recipient in distribution | 3 | First entry (same position) |
| HT 122a | Recipient in RA-RI list | 1 | Different context, same function |

**Verification**: PA-DE consistently functions as a recipient across 3 tablets. Always appears with a quantity. Position as first entry on both sides of HT 9 suggests priority.

### *306-TU Occurrences

| Tablet | Context | Quantity | Notes |
|--------|---------|----------|-------|
| HT 9a | Recipient in VIN distribution | 10 | Largest allocation |
| HT 9b | Recipient in distribution | 8 | Largest allocation |
| HT 119 | Recipient | -- | Different context |
| HT 122a | Recipient in RA-RI list | 1 | Small allocation |

**Verification**: *306-TU consistently as recipient. Largest allocation on both HT 9 sides.

### *324-DI-RA Occurrences

| Tablet | Context | Quantity |
|--------|---------|----------|
| HT 9a | Recipient in VIN distribution | 2.5 |
| HT 9b | Recipient in distribution | 2 |
| HT 122a | Recipient in RA-RI list | 1 |

### TA-I-AROM / TA-I-*123 Occurrences

| Tablet | Context | Quantity |
|--------|---------|----------|
| HT 9a | Recipient: TA-I-AROM 2.5 | 2.5 |
| HT 9b | Recipient: TA-I-AROM 2 | 2 |
| HT 39 | TA-I-*123 | -- |

---

## First Principles Verification

### [1] KOBER: Was analysis data-led, not assumption-led?
**PASS**

Evidence: Started with transliteration verification, structural identification (header, commodity, entries, total), and arithmetic verification before proposing any linguistic interpretations. Cross-referenced with already-completed HT 9b reading to establish opisthograph relationship from data patterns.

### [2] VENTRIS: Was any evidence forced to fit?
**PASS**

Evidence:
- Acknowledged the 0.75 arithmetic discrepancy honestly rather than explaining it away
- Presented three competing hypotheses for the a/b relationship
- Noted that A-RU identification with A-SI is uncertain (per Younger)
- AROM logographic/phonetic ambiguity reported without resolution
- Three recipient names with undeciphered signs marked UNKNOWN

### [3] ANCHORS: Were readings built from confirmed anchors outward?
**PASS**

Anchors used (in order):
- Level 2: KU-RO as total (HIGH -- arithmetic MISMATCH but function clear)
- Level 3: VIN logogram (CERTAIN -- explicitly in header)
- Level 3: AROM logogram (if logographic reading accepted)
- Level 4: Header/entry structural patterns
- Level 5: Morphological patterns (-U, -DE, -RA, -RU endings)

No readings exceed anchor support.

### [4] MULTI-HYP: Were ALL seven hypotheses tested?
**PASS**

All seven hypotheses tested for key terms. Results:
- Luwian: Best fit for DI-NA-U (PROBABLE), QE-PU, -U endings
- Semitic: Best fit for KU-RO (CERTAIN), SA-RO, TA-I-AROM, A-RU
- Pre-Greek: POSSIBLE for substrate names -- ELIMINATED but tested
- Proto-Greek: WEAK across terms -- ELIMINATED
- Hurrian: NEUTRAL across terms -- ELIMINATED
- Hattic: NEUTRAL across terms -- ELIMINATED
- Etruscan: NEUTRAL across terms -- ELIMINATED

### [5] NEGATIVE: Was absence of patterns considered?
**PASS**

Absences noted:
- **No KI-RO**: No deficit notation on this tablet
- **No PO-TO-KU-RO**: No grand total -- single commodity list
- **No toponyms**: Cannot anchor to geographic confirmation (except DI-NA-U hypothesis)
- **Side b has no VIN**: Commodity implied, not stated
- **Side b has no fractions**: All whole integers
- **A-RU absent from side b**: Structurally significant omission
- **No SA-RA2**: Primary S-R term absent; SA-RO is the variant used

### [6] CORPUS: Were readings verified across all occurrences?
**PASS**

- KU-RO: Verified across 39+ corpus attestations (PASS)
- VIN: Standard logogram, universally recognized (PASS)
- DI-NA-U: Verified across HT 9a/b, HT 16, HT 25a, KN Zb 27 (PASS)
- PA-DE: Verified on HT 9a, HT 9b, HT 122a -- consistent function (PASS)
- *306-TU: Verified on HT 9a, HT 9b, HT 119, HT 122a (PASS)
- TA-I-AROM: Verified on HT 9 (both sides) and HT 39 (PASS)
- QE-PU: Limited to HT 9 (both sides) -- consistent function (PARTIAL)
- A-RU: Limited to HT 9a and HT 49a -- function consistent (PARTIAL)

**Limitation**: QE-PU and A-RU have limited attestation (2 inscriptions each). Full cross-corpus verification not possible for these terms.

---

## Novel Observations

### 1. SA-RO as S-R Paradigm Member in VIN Context

SA-RO appears in the header position immediately before TE and VIN. The S-R consonant skeleton (SA-RA2, SA-RU, SA-RO, SI-RU) documented in KNOWLEDGE.md suggests an administrative allocation paradigm. SA-RO's specific use with VIN (wine) may indicate a wine-specific allocation term, or SA-RO may function as a general "allocation from" term in the S-R system with vowel alternation conveying grammatical information.

### 2. Fraction Distribution as Evidence of Calculation

Side a's fractions (J = 1/2, E = 1/4) occur exclusively in PA-DE (J + E), *324-DI-RA (J), TA-I-AROM (J), and A-RU (E). The variety of fractional allocations (3/4, 1/2, 1/4) suggests these are CALCULATED amounts rather than measured ones -- consistent with our hypothesis that side a represents theoretical entitlements.

### 3. *306-TU as Persistent Largest Recipient

*306-TU receives the largest individual allocation on BOTH sides (10 on side a, 8 on side b). Combined with attestation on HT 119 and HT 122a, this name appears consistently across at least 4 tablets. The prominence suggests either a larger household, a more important official, or a production center.

### 4. Recipient Overlap with HT 122a

HT 122a (a different tablet with RA-RI header, Scribe 9) shares PA-DE, *306-TU, *324-DI-RA, and DA-SI-*118 with HT 9a/b. This cross-tablet overlap of 4+ recipient names strongly suggests these are actual individuals (or toponyms) that appear in multiple administrative records -- not ad hoc labels.

### 5. The 0.75 Discrepancy as Methodological Test Case

The exact J + E (0.75) discrepancy, combined with side b's exact verification, makes HT 9 a natural test case for fraction interpretation. If future work resolves the fraction values precisely, HT 9a provides a built-in verification tablet.

---

## Confidence Assessment

### Element-by-Element Confidence

| Element | Interpretation | Confidence | Rationale |
|---------|----------------|------------|-----------|
| Document type | Single-commodity distribution list | HIGH | KU-RO present; VIN stated; standard structure |
| VIN | Wine | **CERTAIN** | Level 3 anchor; explicitly in header |
| KU-RO = 31.75 | Total | **CERTAIN** (function) | Level 2 anchor; arithmetic MISMATCH but role clear |
| SA-RO | Header qualifier or allocation term | POSSIBLE | S-R paradigm member; 4 attestations, HT-only |
| TE | Separator/transaction marker | PROBABLE | Structural role consistent across corpus |
| PA-DE | Personal name or toponym (recipient) | PROBABLE | Consistent position across 3 tablets |
| *306-TU | Personal name (recipient) | PROBABLE | Position; undeciphered *306 prevents etymology |
| DI-NA-U | Toponym (locality known for wine) | **PROBABLE** | Cross-site (HT + KN); wine context; Younger |
| QE-PU | Personal name or title (recipient) | POSSIBLE | Position; limited attestation (HT 9 only) |
| *324-DI-RA | Personal name (recipient) | PROBABLE | Position; undeciphered *324 prevents etymology |
| TA-I-AROM | Recipient or qualified allocation | POSSIBLE | AROM ambiguity unresolved |
| A-RU | Personal name (recipient) | POSSIBLE | Limited attestation; absent from side b |
| Commodity = wine | Explicit | **CERTAIN** | VIN logogram in header |
| Opisthograph relationship | Coordinated accounting document | HIGH | Shared recipients, header system, systematic pattern |
| Double-entry pattern | Allocation vs. disbursement | POSSIBLE | Consistent decrease; structural logic; unproven |

### Overall Translation Confidence

| Aspect | Confidence |
|--------|------------|
| **Structure** | HIGH -- Clear distribution list with stated total |
| **Arithmetic** | MISMATCH -- 0.75 discrepancy (J + E) |
| **Commodity** | **CERTAIN** -- VIN explicitly stated |
| **Names** | PROBABLE -- Position patterns consistent; cross-tablet overlap |
| **Header terms** | POSSIBLE -- Function clear, meaning uncertain |
| **Side a/b relationship** | POSSIBLE -- Pattern clear, interpretation uncertain |

**OVERALL**: **PROBABLE** (Strong structural and commodity foundation; VIN CERTAIN; recipient names identified by position and cross-tablet verification; arithmetic discrepancy documented but does not undermine reading; opisthograph relationship with HT 9b established)

---

## Sources Consulted

1. **lineara.xyz** -- HT9a.html (transliteration, metadata, images)
2. **GORILA Vol. I** pp. 18-19 (referenced via lineara.xyz, page 54 of PDF)
3. **Younger, J. (2023)** -- Commentary on HT 9 (fraction discussion, DI-NA-U identification, AROM/*123 note)
4. **Gordon, C. H. (1966)** -- KU-RO = *kull* "total"
5. **METHODOLOGY.md** -- Seven hypotheses framework, First Principles
6. **KNOWLEDGE.md** -- Project knowledge base (K-R paradigm, S-R patterns, confirmed readings)
7. **HT9b_READING.md** -- Partner tablet reading (v0.7.0, 2026-02-17)
8. **HT85a_READING.md** -- Cross-reference (shared recipients)
9. **Ferrara (2020)** -- Fraction values (J, E system)
10. **arithmetic_verifier.py** -- Automated arithmetic verification (MISMATCH, fraction_parsing)
11. **reading_readiness_scorer.py** -- Readiness score: 0.629 (80% coverage)
12. **hypothesis_tester.py** -- All seven hypotheses tested for each word
13. **commodity_validator.py** -- SA-RO commodity mapping (VIN, SPECULATIVE)

---

## Appendix A: HT 9a / HT 9b Synoptic Comparison

```
SIDE A (HT 9a)                          SIDE B (HT 9b)
============================            ============================
SA-RO | TE | VIN |                      PA3 |
                                        WA-JA-PI
                                        ________________________

                                        KA-*305 |
PA-DE |     5 J E  [5.75]              PA-DE         3
*306-TU          10                     A-SI          3
DI-NA-U           4                     *306-TU       8
QE-PU             2                     *324-DI-RA    2
*324-DI-RA    2 J  [2.50]              QE-PU         2
TA-I-AROM     2 J  [2.50]              TA-I-AROM     2
A-RU          4 E  [4.25]              DI-NA-U       4
KU-RO        31 J E [31.75]            KU-RO        24

COMPUTED: 31.00                         COMPUTED: 24
STATED:   31.75                         STATED:   24
STATUS:   MISMATCH (-0.75)              STATUS:   VERIFIED
```

**Net difference**: 31.75 - 24 = 7.75 units (side a exceeds side b by 7.75)

---

## Appendix B: Recipient Order Comparison

| Side A Order | Side B Order | Notes |
|--------------|--------------|-------|
| 1. PA-DE | 1. PA-DE | Same position |
| 2. *306-TU | 2. A-SI | **Different**: A-SI absent from side a |
| 3. DI-NA-U | 3. *306-TU | Moved from position 2 to 3 |
| 4. QE-PU | 4. *324-DI-RA | Moved from position 5 to 4 |
| 5. *324-DI-RA | 5. QE-PU | Moved from position 4 to 5 |
| 6. TA-I-AROM | 6. TA-I-AROM | Same position |
| 7. A-RU | 7. DI-NA-U | DI-NA-U moved from 3 to 7; A-RU absent |

**Critical observation**: PA-DE leads both lists, but the subsequent order changes. This may indicate the lists were compiled independently.

**Alternative reading note**: Younger (2023) suggests A-SI on side b could alternatively be read as A-RU ("or: A-RU"). If A-SI = A-RU, then all side a recipients appear on side b.

---

## Appendix C: Cross-Tablet Recipient Network

```
         HT 9a    HT 9b    HT 122a   Other
PA-DE    5.75     3        1
*306-TU  10       8        1         HT 119
DI-NA-U  4        4        --        HT 16, HT 25a, KN Zb 27
QE-PU    2        2        --
*324-DI-RA 2.5    2        1
TA-I-AROM  2.5    2        --        HT 39
A-RU     4.25     --       --        HT 49a
A-SI     --       3        --
```

The overlap between HT 9 and HT 122a (PA-DE, *306-TU, *324-DI-RA) suggests a common pool of recipients across multiple wine distribution events. HT 122a totals 31 via KU-RO -- the same integer as HT 9a's computed sum (31.00), though HT 9a's stated KU-RO is 31.75.

---

## Morphological and Onomastic Constraints

### *306-TU (4 attestations)

- **Morphological decomposition**: 2-syllable word; *306 is an undeciphered sign + TU. Root skeleton *-T. Belongs to paradigm P-*T-6 (morphological predictor). Decomposition confidence: PROBABLE.
- **Paradigm membership**: P-*T-6 paradigm. The *306-TU base extends to *306-TU-JA (with -JA suffix) in the corpus, confirming -TU as an element that can take further suffixation.
- **Onomastic analysis**: Present in onomastic top 30 name candidates. Profile: CV-CV (short), HT site, final syllable TU (6 onomastic candidates end in -TU, including TE-TU). No theophoric element identified.
- **Constraint summary**: Paradigm P-*T-6 membership confirmed. The *306-TU / *306-TU-JA relationship demonstrates -JA suffixation on this base, consistent with Luwian -iya adjectival/ethnic derivation. Persistently largest recipient on both HT 9 sides.

### *324-DI-RA (3 attestations)

- **Morphological decomposition**: 3-syllable word with -RA suffix (37 corpus-wide attestations). *324 is an undeciphered sign. Root skeleton 3-D-R. Decomposition confidence: POSSIBLE.
- **Paradigm membership**: No specific paradigm match for the full word.
- **Onomastic analysis**: Present in onomastic top 30 name candidates. Profile: CV-CV-CV (medium), HT site, final syllable RA. Possible theophoric element: DI (shared with DI-KI-TE theophoric group).
- **Theophoric connection**: The DI element in *324-DI-RA is flagged as a possible theophoric component, which could link to divine naming conventions.
- **Constraint summary**: -RA suffix productive. Possible DI theophoric element detected. No full-word paradigm match.

### QE-PU (2 attestations, HT 9 only)

- **Morphological decomposition**: 2-syllable word with no recognized suffix (PU not in productive suffix list). Root skeleton Q-P. Decomposition confidence: SPECULATIVE.
- **Paradigm membership**: No paradigm match found.
- **Onomastic analysis**: Not in top name candidates. QE- initial appears in 4 name candidates (QE-RA2-U, QE-TI). CV-CV (short) pattern.
- **Constraint summary**: No paradigm match found. QE- prefix connects to a small but attested initial-syllable group. The fixed quantity (2) on both sides of HT 9 is the strongest constraint.

### TA-I-AROM (3 attestations)

- **Morphological decomposition**: 3-syllable word with TA- prefix (28 corpus attestations, 6th most common). Root skeleton T-Ø-Ø. Decomposition confidence: POSSIBLE. The AROM element is ambiguous (logographic = herbs/spices per Linear B, or phonetic per Younger 2023).
- **Paradigm membership**: No paradigm match found.
- **Onomastic analysis**: Present in onomastic top 30 name candidates. Profile: CV-CV-CV (medium), HT site, final syllable AROM. No theophoric element identified.
- **AROM constraint**: If AROM is logographic (Linear B cognate), then TA-I is the name/recipient and AROM is a commodity qualifier. If phonetic, the entire sequence is a personal name. The onomastic comparator treats it as a name candidate in either case.
- **Constraint summary**: TA- prefix productive. No paradigm match. The logographic vs. phonetic status of AROM remains the primary analytical constraint on this word.

---

*Reading completed 2026-02-21. Partner tablet to HT 9b (already read v0.7.0). VIN commodity CERTAIN (explicit). KU-RO = 31.75 arithmetic MISMATCH (0.75 = J+E discrepancy). Five of seven recipients shared with side b. DI-NA-U identified as probable toponym (cross-site verified at KN). Seven hypotheses tested; Luwian and Semitic dominant in domain-specific layering pattern. Overall confidence PROBABLE.*
