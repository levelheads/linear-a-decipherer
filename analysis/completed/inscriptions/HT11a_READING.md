# HT 11a Connected Reading Report

**Date**: 2026-02-22
**Analyst**: Claude (Opus 4.6)
**Phase**: MINOS III - Campaign 1, Tier 1
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
| **Tablet ID** | HT 11a (side a of HT 11) |
| **Site** | Hagia Triada (Haghia Triada), Villa Magazine |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Context** | LMIB |
| **Scribe** | HT Scribe 24 |
| **Support** | Clay tablet (page tablet, opisthograph) |
| **Partner** | HT 11b (side b, KA distribution, 180 KU-RO VERIFIED) |
| **Document Type** | Multi-section mixed distribution (unnamed commodity + VIR) |
| **Arithmetic Status** | CONSTRAINED (KU-RO = 10, computed = 6, lacuna budget = 4) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |

---

## Transliteration

### HT 11a (Side A)

```
Line 1:  A-RU-RA  𐄁                  3
Line 2:  KA-RO-NA                    2
Line 3:  *322-RI                     1
Line 4:  KU-RO                      10
Line 5:  A-SU-JA                     1
Line 6:  VIR+[?]-I                   3
Line 7:  TA₂                        15
```

### HT 11b (Side B) -- for cross-reference (partner)

```
Line 1:  𐝫DE-NU
Line 2:  RU-RA₂
Line 3:  *86-KA         40
Line 4:  KA             30
Line 5:  KA             50
Line 6:  RU-ZU-NA KA    30
Line 7:  SA-QE-RI 𐄁 KA  30
Line 8:  KU-RO         180
```

---

## Arithmetic Verification

### Section 1 (Lines 1-4)

```
A-RU-RA (header?)   3  (or unnamed entry?)
KA-RO-NA            2
*322-RI              1
                    ---
Computed sum         6
Stated KU-RO        10
Difference           4
Status              CONSTRAINED (lacuna budget 4 = plausible missing entries)
```

**Diagnosis**: The arithmetic verifier classifies the 3 on Line 1 as a quantity associated with the header A-RU-RA. If A-RU-RA is a header (not a recipient), then the 3 may be assigned to a damaged or omitted entry. The 4-unit gap could be explained by 1-2 damaged entries in the opening. Alternatively, A-RU-RA may be both a header and have an associated quantity (like DA-DU-MA-TA 𐄁 GRA on HT 95a, where GRA is the commodity, not a quantity).

**Re-reading**: The separator (𐄁) after A-RU-RA suggests it is a header. The 3 on the same line may be:
1. A quantity for an unnamed entry (damaged name)
2. A commodity count associated with the header
3. An error in line-break parsing (quantity belongs to A-RU-RA)

### Post-KU-RO Section (Lines 5-7)

```
A-SU-JA              1   (recipient or category?)
VIR+[?]-I            3   (commodity logogram + qualifier + quantity)
TA₂                  15  (recipient or standalone entry)
```

These entries appear AFTER the KU-RO total and are therefore not included in the section 1 sum. This parallels HT 122a (KU-DA 1 after KU-RO 31) and is a recognized structural pattern for addenda or secondary sections.

---

## Anchor Identification

### Level 2: Linear B Cognates + Position (HIGH)

| Term | Interpretation | Evidence | Occurrences |
|------|----------------|----------|-------------|
| **KU-RO** | Total/summation | List-position; 37 corpus-wide; Gordon 1966 | 37 |

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **VIR+[?]-I** | Person/worker (qualified + I) | Pictographic; VIR cognate | Line 6 (post-total) |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| A-RU-RA header | Institutional source | Initial position + separator |
| NAME + QUANTITY | Distribution entries | Lines 2-3 |
| KU-RO total | Section total | Line 4 (10) |
| Post-total entries | Secondary section/addenda | Lines 5-7 |

---

## Structural Analysis

### Document Type

**Multi-section mixed-commodity distribution tablet**

HT 11a has two distinct sections:
1. **Section 1** (Lines 1-4): Distribution under A-RU-RA header, KU-RO = 10 (commodity unspecified)
2. **Post-total section** (Lines 5-7): A-SU-JA 1, VIR+[?]-I 3, TA₂ 15 (different commodity/category)

### Document Structure

```
=== Section 1 ===
[H]   A-RU-RA  𐄁           Header: institutional source
[#]   3                     Quantity (for damaged entry? or header attribute?)
[R]   KA-RO-NA        2    Recipient 1: 2 units
[R]   *322-RI          1    Recipient 2: 1 unit
[T]   KU-RO           10    Section total (CONSTRAINED)

=== Section 2 (post-total) ===
[R?]  A-SU-JA          1    Entry/recipient
[C]   VIR+[?]-I        3    Commodity: 3 workers (qualified)
[R?]  TA₂             15    Entry: 15 units (largest number on tablet)
```

### Notable Structural Features

1. **CONSTRAINED arithmetic**: KU-RO = 10, computed = 6, gap = 4. The gap is within plausible range for 1-2 damaged entries.

2. **Two sections**: Pre-KU-RO (unspecified commodity, 10 total) and post-KU-RO (VIR+[?]-I and TA₂). This parallels HT 122a (KU-DA 1 after KU-RO 31).

3. **VIR+[?]-I logogram**: The -I suffix on VIR+[?] is unusual. This may indicate a specific worker type or a scribal notation. Compare VIR+[?] on HT 122b and HT 85a (no -I suffix).

4. **TA₂ = 15**: The largest quantity on the tablet. TA₂ appears on only 3 tablets (HT 11a, HT 137, KH 29). As a single syllable, it may be an abbreviation, a commodity unit, or a category marker.

5. **Scale contrast with partner**: Side a totals ~29 (10 + 1 + 3 + 15); side b totals 180. The two sides operate at very different scales.

6. **No shared vocabulary with partner**: HT 11a and HT 11b share no words (except potential implicit KA on both, but this is unconfirmed). The same scribe records two completely independent accounts.

---

## Multi-Hypothesis Testing

### Key Term: A-RU-RA (Header)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | -RA nominal suffix; A- prefix parallels Anatolian | **POSSIBLE** |
| Proto-Greek | A-RU- ~ *arotron* "plow"; -RA ending | WEAK |
| Semitic | No clear root | NEUTRAL |
| Pre-Greek | No diagnostic features | NEUTRAL |
| Hurrian | -RA comitative suffix | WEAK |
| Hattic | A- prefix 3sg | WEAK |
| Etruscan | No parallel | NEUTRAL |

**Best**: Luwian (POSSIBLE). Hapax. Confidence capped.

### Key Term: KA-RO-NA (Recipient)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Pre-Greek** | Vowel alternation (a/o/a); -NA ending | **POSSIBLE** |
| Proto-Greek | Contains /o/ syllable; bronze cognate (initial) | POSSIBLE (ELIMINATED) |
| Luwian | -NA ending | WEAK |
| Semitic | No clear root | NEUTRAL |
| Hurrian | -NA definite/plural | WEAK |
| Hattic | No parallel | NEUTRAL |
| Etruscan | No parallel | NEUTRAL |

**Best**: Pre-Greek (POSSIBLE, but ELIMINATED hypothesis). Active best: Luwian/undetermined. Hapax.
**Note**: Contains /o/ (RO syllable), which is rare in Linear A (3.92%). This slightly favors Greek-influenced onomastics, but Proto-Greek is ELIMINATED as a genetic hypothesis.

### Key Term: A-SU-JA (Post-Total Entry)

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| **Luwian** | -JA suffix (Level 5 anchor, MEDIUM confidence); Luwian adjectival/ethnic | **POSSIBLE** |
| Proto-Greek | -JA ~ Greek -ia; Athena/Artemis initial | WEAK |
| Semitic | No clear root | NEUTRAL |
| Pre-Greek | No diagnostic features | NEUTRAL |
| Hurrian | No parallel | NEUTRAL |
| Hattic | A- prefix | WEAK |
| Etruscan | No parallel | NEUTRAL |

**Best**: Luwian (POSSIBLE). Hapax. The -JA suffix is a productive Luwian adjectival/ethnic marker (77 corpus-wide, 65.9% word-final).

### Key Term: TA₂ (Post-Total, 15 units)

TA₂ is a single sign (not a multi-syllable word). As such, hypothesis testing is limited:

| Hypothesis | Evidence | Rating |
|------------|----------|--------|
| Multiple | Single syllable; could be abbreviation, logogram, or unit marker | **UNKNOWN** |

**Assessment**: TA₂ with the very large quantity 15 (largest on tablet) and its post-total position suggests it may be a commodity unit or category marker rather than a personal name. Its 3 corpus occurrences (HT 11a, HT 137, KH 29) include cross-site attestation, but the small sample prevents meaningful hypothesis testing.

---

## Connected Reading Attempt

### Full Interpretive Reading

> **Section 1 -- From A-RU-RA** (institutional source):
>
> [3 units (entry/name lost or attached to header)]
> To KA-RO-NA: 2 units
> To *322-RI: 1 unit
>
> **Section Total: 10 units** (4 unaccounted, likely damaged entries)
>
> **Section 2 (post-total):**
>
> A-SU-JA: 1 [unit or entry marker]
> VIR+[?]-I: 3 workers (qualified type)
> TA₂: 15 [units of unnamed commodity]

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| A-RU-RA = header | Institutional source | POSSIBLE | Position; hapax |
| KU-RO = total | Section total: 10 | CERTAIN | Corpus-verified |
| VIR+[?]-I = workers | Workers (qualified) | HIGH | Logogram |
| KA-RO-NA, *322-RI = names | Recipients | POSSIBLE | Position; hapax |
| Post-total entries = Section 2 | Separate accounting section | PROBABLE | Structural pattern |
| TA₂ function | Unknown (commodity? category?) | UNKNOWN | 3 corpus occurrences |

---

## What We Know For Certain

1. **KU-RO = 10**: Section total. CERTAIN.
2. **VIR+[?]-I = workers**: Commodity logogram in post-total section. HIGH.
3. **Same scribe and findspot as HT 11b**: HT Scribe 24, Villa Magazine. Both sides by the same hand.
4. **Two-section structure**: Pre-KU-RO distribution + post-KU-RO addendum. Established pattern.

## What We Hypothesize

1. **A-RU-RA as header**: Position + separator support this, but the 3 on the same line is ambiguous. Could be recipient with quantity 3.
2. **Section 1 commodity**: Not explicitly stated. The unspecified commodity for the KU-RO = 10 section may be KA (paralleling side b) or another commodity.
3. **TA₂ = 15 as independent accounting**: The largest quantity (15) appears after VIR+[?]-I, suggesting a different commodity/category from the VIR workers.
4. **Gap of 4**: Likely 1-2 damaged entries before Line 2.

---

## First Principles Verification

### [1] KOBER: Data-led? **PASS**
### [2] VENTRIS: Evidence not forced? **PASS**
- A-RU-RA's header vs. recipient ambiguity acknowledged; TA₂ function left as UNKNOWN; gap diagnosed as lacuna, not forced
### [3] ANCHORS: Built outward? **PASS**
- KU-RO (CERTAIN), VIR logogram (HIGH), structural patterns (MEDIUM-HIGH)
### [4] MULTI-HYP: All seven tested? **PASS**
- Tested for A-RU-RA, KA-RO-NA, A-SU-JA, KU-RO
### [5] NEGATIVE: Absences noted? **PASS**
- No commodity logogram in Section 1; no KI-RO; no SA-RA₂; no fractions; all hapax vocabulary
- TA₂ function unknown -- not forced to an interpretation
### [6] CORPUS: Verified? **PARTIAL**
- KU-RO verified (37 occ); VIR verified. All other terms hapax -- cannot verify cross-corpus.

---

## Novel Observations

### 1. HT Scribe 24's Two-Sided Accounting

HT 11a (mixed, small-scale: ~29 units) and HT 11b (KA commodity, large-scale: 180 units) represent dramatically different administrative domains recorded by the same scribe on the same tablet. This parallels HT Scribe 9's pattern (HT 85a VIR 66 + HT 122 VIR 97), but Scribe 24 works across different commodity types rather than a single commodity.

### 2. Post-Total Section as Standard Feature

The post-KU-RO entries (A-SU-JA 1, VIR+[?]-I 3, TA₂ 15) echo HT 122a (KU-DA 1 after KU-RO 31) and suggest that post-total sections are a regular scribal practice, not anomalies. They may represent different commodity categories, addenda, or corrections.

### 3. VIR+[?]-I as Worker Category Variant

The -I suffix on VIR+[?] is unusual. If -I represents an additional qualifier, this may distinguish a specific sub-category of worker (e.g., VIR+[?]-I = "workers of type I" vs. VIR+[?] = "workers, general"). The 3 workers of this type are separate from the Section 1 accounting.

---

## Sources Consulted

1. **lineara.xyz corpus** -- HT 11a transliteration and metadata
2. **arithmetic_verifier** -- Rosetta skeleton, CONSTRAINED diagnosis
3. **hypothesis_tester.py** -- A-RU-RA, KA-RO-NA, A-SU-JA
4. **data/hypothesis_results.json** -- KU-RO
5. **HT 11b reading** -- Partner tablet comparison
6. **KNOWLEDGE.md** -- -JA suffix, VIR logogram
7. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework

---

*Connected reading completed 2026-02-22 as part of MINOS III Campaign 1, Tier 1.*

*HT 11a is a compact multi-section tablet by HT Scribe 24 (same scribe as partner HT 11b). Section 1 distributes 10 units from A-RU-RA to at least 2-4 recipients (CONSTRAINED arithmetic, gap 4). Post-total entries introduce VIR+[?]-I workers (3) and the enigmatic TA₂ (15). No vocabulary is shared with partner tablet HT 11b, confirming the two sides record independent accounts.*
