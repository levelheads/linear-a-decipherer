# HT 94b Connected Reading Report

**Date**: 2026-02-21
**Analyst**: Claude (Opus 4.6)
**Phase**: Lane G - Reading Attempts (KU-RO Arithmetic Verification Series)
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
| **Tablet ID** | HT 94b (side b of HT 94) |
| **Site** | Hagia Triada (Haghia Triada) |
| **Findspot** | Casa Room 7 |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Scribe** | HT Scribe 9 |
| **Support** | Clay tablet (page tablet, opisthograph) |
| **Document Type** | KI-RO deficit list with KU-RO total + supplementary section |
| **Arithmetic Status** | VERIFIED (KU-RO = 5, computed sum = 5, 5 items) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |
| **Same Scribe As** | HT 85a, HT 117a (HT Scribe 9) -- significant for scribal convention comparison |
| **Reference** | GORILA Vol. I, p. 186 |

---

## Transliteration

```
SECTION 1 — Deficit Header + Personnel List + Total

b.1     KI-RO | 𐄁                               [DEFICIT MARKER]
b.1     TU-MA                               1
b.2     PA-TA-NE                             1
b.2     DE-DI                                1
b.3     KE-KI-RU                             1
b.3     SA-RU                                1
b.4     KU-RO                                5    [TOTAL]

SECTION 2 — Supplementary Entries (Post-Total)

b.4     *86 | 𐄁                                   [SECTION MARKER]
b.5     RA | 𐄁 | DE-ME-TE                    1
b.5     *21F-TU | 𐄁                          1
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| KI | AB 67 | CERTAIN | High |
| RO | AB 02 | CERTAIN | High |
| TU | AB 69 | HIGH | High |
| MA | AB 80 | CERTAIN | High |
| PA | AB 03 | CERTAIN | High |
| TA | AB 59 | CERTAIN | High |
| NE | AB 24 | HIGH | Moderate |
| DE | AB 45 | CERTAIN | High |
| DI | AB 07 | CERTAIN | High |
| KE | AB 44 | HIGH | Moderate |
| RU | AB 26 | CERTAIN | Moderate |
| SA | AB 31 | CERTAIN | High |
| KU | AB 81 | CERTAIN | High |
| RA | AB 60 | CERTAIN | High |
| ME | AB 13 | CERTAIN | High |
| TE | AB 04 | CERTAIN | High |
| *86 | Unique | HIGH | 24 corpus occurrences |
| *21F | Unique | HIGH | 22 corpus occurrences |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None identified on this tablet.**

### Level 2: Linear B Cognates + Position (HIGH)

| Term | Interpretation | Evidence | Corpus Attestations |
|------|----------------|----------|---------------------|
| **KU-RO** | "total/sum" | List-final position; sum = 5 verified; Gordon (1966) | 37 corpus-wide |
| **KI-RO** | "deficit/category marker" | Tablet-initial position; 16 corpus-wide | 16 |

### Level 3: Logograms (HIGH/CERTAIN)

**No commodity logograms on this tablet.** This is a pure deficit list with no GRA, OLE, VIN, FIC, or any commodity sign. All entries are NAME + numeral 1. The commodity is unstated -- it may be implicit from side a (HT 94a records personnel/commodity distributions with KU-RO 110).

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| KI-RO at opening | Deficit/outstanding category marker | Cross-corpus verified (HT 117a header, HT 123a deficit) |
| NAME + 1 format | Personnel counting or individual allocations | 5 consistent entries in Section 1 |
| KU-RO at section end | Total for preceding entries | Arithmetic VERIFIED |
| Post-KU-RO section | Supplementary entries or different category | *86 introduces new section after total |
| Word divider 𐄁 | Separates functional elements | Between KI-RO and list; between RA and DE-ME-TE |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| -RU suffix (x2) | SA-RU, KE-KI-RU | Possible S-R paradigm member (SA-RU); name ending (KE-KI-RU) |
| -NE suffix | PA-TA-NE | 3-syllable name with -NE ending |
| -DI suffix | DE-DI | Short 2-syllable name |
| *21F classifier | Feminine gender classifier | Established function (KNOWLEDGE.md); precedes -TU |

### Level 6: Lexical Matches (LOW)

| Match | Interpretation | Evidence |
|-------|----------------|----------|
| SA-RU ~ S-R paradigm | S-R variant (A-U vowel pattern) | 6 attestations; all HT; part of S-R root system |
| DE-ME-TE ~ Linear B *da-ma-te* | Possible Demeter cognate | Phonological similarity; but must not assume |

---

## Structural Analysis

### Document Type

**Deficit (KI-RO) list with KU-RO total and supplementary section**

This tablet records 5 individuals or items marked as deficient/outstanding (KI-RO), each allocated quantity 1, totaling KU-RO 5. After the total, a second section introduced by *86 lists 2 additional entries. The dual KI-RO + KU-RO structure parallels HT 117a (same scribe, HT Scribe 9).

### Document Structure

```
[D]  KI-RO                    Deficit/outstanding marker
[H]  TU-MA            1       Header or first entry
[R]  PA-TA-NE         1       Recipient 1
[R]  DE-DI            1       Recipient 2
[R]  KE-KI-RU         1       Recipient 3
[R]  SA-RU            1       Recipient 4
[T]  KU-RO            5       Total: 5 units

─── Section break ───

[R]  *86                       Section marker (no quantity)
[R]  RA | DE-ME-TE    1       Recipient 5 (with qualifier?)
[R]  *21F-TU          1       Recipient 6 (feminine classifier + TU)
```

### Rosetta Skeleton (arithmetic_verifier output)

| Tag | Role | Count |
|-----|------|-------|
| [D] | Deficit marker | 1 (KI-RO) |
| [H] | Header | 1 (TU-MA) |
| [R] | Recipient | 7 (PA-TA-NE, DE-DI, KE-KI-RU, SA-RU, *86, RA/DE-ME-TE, *21F-TU) |
| [T] | Total | 1 (KU-RO 5) |
| [?] | Unknown | 1 (DE-ME-TE classified as unknown by skeleton) |

### Arithmetic Verification

```
TU-MA        1
PA-TA-NE     1
DE-DI        1
KE-KI-RU     1
SA-RU        1
             --
SUM          5  =  KU-RO 5  VERIFIED
```

**All 5 entries sum exactly to the stated KU-RO total.** Uniform quantity (all 1's) -- the simplest possible arithmetic verification. No fractions, no damage, no discrepancies.

### KI-RO Verification

**Status: INCONCLUSIVE** -- The arithmetic_verifier classifies KI-RO verification as INCONCLUSIVE because KI-RO's precise function (deficit amount vs. category marker) remains debated. The tablet's arithmetic is internally consistent regardless.

### Notable Structural Features

1. **Dual KI-RO + KU-RO**: Both K-R paradigm terms co-occur, confirming they serve different functions (marker vs. total). Parallels HT 117a (same scribe).
2. **Uniform quantity**: All 5 entries = 1. Same pattern as HT 117a (10 entries of 1). This is a headcount or per-person deficit, not a variable commodity distribution.
3. **Post-total section**: After KU-RO 5, the tablet continues with *86 and 2 more entries. This supplementary section is NOT included in the KU-RO total.
4. **Same scribe as HT 85a and HT 117a**: HT Scribe 9 consistently uses KU-RO with exact arithmetic and section structure.
5. **Opisthograph**: HT 94a (side a) records a larger document with KU-RO 110 (personnel grand total). Side b (this reading) is a separate but related deficit account.
6. **Word dividers**: 𐄁 used to separate KI-RO from the list, and to separate elements in the post-total section.

---

## Personal Names Identified

### Section 1 (Under KI-RO Deficit)

| Name | Syllables | Suffix | Cross-Tablet | Notes |
|------|-----------|--------|--------------|-------|
| **TU-MA** | 2 | -MA | HT 94b only (hapax) | Header position or first entry; function unclear |
| **PA-TA-NE** | 3 | -NE | HT 122a, HTWa1019 (3 total) | Cross-tablet name; -NE ending |
| **DE-DI** | 2 | -DI | HT 94b only (hapax) | Short 2-syllable form |
| **KE-KI-RU** | 3 | -RU | HT 94b only (hapax) | Reduplicated KE-KI element + -RU |
| **SA-RU** | 2 | -RU | 6 tablets (HT86a/b, HT94b, HT95a/b, HT123+124a) | S-R paradigm member; well-attested at HT |

### Section 2 (Post-KU-RO, under *86)

| Name | Syllables | Notes |
|------|-----------|-------|
| **RA** | 1 | Single syllable; unclear if name or function word; precedes DE-ME-TE |
| **DE-ME-TE** | 3 | Hapax in corpus (1 attestation); phonological similarity to Linear B *da-ma-te* (Demeter) |
| ***21F-TU** | 2 | Feminine classifier *21F + TU; possibly a gendered name or title |

### Note on SA-RU

SA-RU has 6 corpus-wide attestations, all at Hagia Triada. It belongs to the S-R paradigm (vowel pattern A-U), alongside SA-RA₂ (A-A), SA-RO (A-O), and SI-RU (I-U). In this tablet, SA-RU appears in recipient position with quantity 1 -- consistent with a personal name reading. However, SA-RU's membership in the S-R administrative paradigm means it could alternatively function as an administrative term. Position evidence (recipient + integer) favors the personal name reading here.

### Note on DE-ME-TE

DE-ME-TE appears only on HT 94b in the entire corpus (hapax legomenon). Its phonological similarity to Linear B *da-ma-te* (Demeter, the grain deity) is noteworthy but must not be assumed as proof of identity. The word appears in the post-total supplementary section, not in the main deficit list. If DE-ME-TE is indeed a Demeter cognate, this would be significant evidence for Minoan religious naming; however, hapax status limits confidence to SPECULATIVE. The KNOWLEDGE.md entry for DA-MA-TE (Level 2, HIGH) refers to a different attestation at a peak sanctuary; DE-ME-TE here has a different spelling pattern (E vowels vs. A vowels).

### Note on *21F-TU

The *21F sign is a feminine gender classifier (KNOWLEDGE.md: 22 occurrences, 63.6% at HT). Combined with TU, this may represent a gendered personal name, a feminine title, or a classifier + name combination. Compare *21F-TU-NE on HT 117b (same scribe, used as section header for a female-associated personnel list). The -TU element may be the same base name, with -NE added as an additional suffix on HT 117b.

---

## Multi-Hypothesis Testing

### Focus Terms

Analysis prioritizes the surviving hypotheses (Luwian STRONG, Semitic MODERATE) while testing all seven for compliance.

### Key Term: KI-RO (Deficit/Category Marker)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Semitic** | *kirru/girru* "deficit/remainder" (extended K-R root) | 16 corpus-wide; standard admin term; HERE at tablet-initial position | **PROBABLE** | ACTIVE |
| **Luwian** | Possible adopted admin loan | K-R paradigm may be Semitic-origin in Luwian admin framework | POSSIBLE | ACTIVE |
| Pre-Greek | Unknown substrate admin term | Position consistent but no etymology | POSSIBLE | ELIMINATED |
| Proto-Greek | *kyrios*-related? | Phonologically improbable; /o/ frequency argues against | WEAK | ELIMINATED |
| Hurrian | No parallel | No Hurrian admin cognate | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No Etruscan admin cognate | WEAK | ELIMINATED |

**Best hypothesis**: Semitic (PROBABLE) -- consistent with K-R paradigm.
**Key finding**: KI-RO at tablet-initial position, functioning as deficit marker introducing a list of outstanding items/persons. This contrasts with KI-RO's header function on HT 117a (same scribe), demonstrating multi-functional usage.

### Key Term: KU-RO (Total)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Semitic** | *kull* "total/all" (Akkadian/West Semitic) | 37 corpus-wide; list-final; sums verified; cross-site (HT, ZA, PH) | **CERTAIN** | ACTIVE |
| **Luwian** | Adopted into Minoan admin system | Not originally Luwian but used in Luwian-influenced framework | HIGH (function) | ACTIVE |
| Pre-Greek | -- | -- | -- | ELIMINATED |
| Proto-Greek | *kyrios* "lord/complete" | Chronologically and phonologically problematic | WEAK | ELIMINATED |
| Hurrian | -- | -- | -- | ELIMINATED |
| Hattic | -- | -- | -- | ELIMINATED |
| Etruscan | -- | -- | -- | ELIMINATED |

**Best hypothesis**: Semitic (CERTAIN for function; PROBABLE for specific etymology).
**Arithmetic verification**: 5 entries x 1 = 5 = KU-RO. EXACT MATCH.

### Key Term: SA-RU (Recipient / S-R Paradigm Member)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | Possible Luwian personal name or S-R admin variant | S-R paradigm member (A-U vowel); -RU ending favors Luwian (64%); hypothesis_tester best=luwian | **POSSIBLE** | ACTIVE |
| **Semitic** | S-R root: *šarāku*-related variant | Biconsonantal SR skeleton; related to SA-RA₂ paradigm | POSSIBLE | ACTIVE |
| Pre-Greek | Substrate personal name | Possible | WEAK | ELIMINATED |
| Proto-Greek | No cognate | No match | WEAK | ELIMINATED |
| Hurrian | Partial cognate (*šarr-* "king"?) | Limited evidence | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE) per hypothesis_tester.
**Dual interpretation**: SA-RU is BOTH a personal name candidate (recipient position) AND an S-R paradigm member (administrative term candidate). Position evidence on this tablet (recipient + integer 1) favors the personal name reading.
**Confidence**: POSSIBLE (multi-hypothesis; S-R paradigm complicates interpretation).

### Key Term: PA-TA-NE (Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Proto-Greek** | *panta* "all" or *pater* "father" + nominative | Cognate scoring from hypothesis_tester; best=protogreek | **POSSIBLE** | ELIMINATED |
| **Luwian** | Luwian personal name with -NE suffix | -NE matches Luwian nominal patterns | POSSIBLE | ACTIVE |
| Semitic | Possible PTN triconsonantal root | Biconsonantal fit; fig (Hebrew *te'ena*) partial match | WEAK | ACTIVE |
| Pre-Greek | Substrate personal name with vowel alternation | Pre-Greek a/e alternation pattern | WEAK | ELIMINATED |
| Hurrian | -NE matches Hurrian definite article | Grammatical parallel; no lexical match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Proto-Greek scored highest (POSSIBLE) but Proto-Greek is ELIMINATED as a genetic hypothesis. Within surviving hypotheses, Luwian (POSSIBLE) is the best active candidate.
**Cross-corpus**: PA-TA-NE appears on 3 tablets (HT 94b, HT 122a, HTWa1019) -- sufficient for cross-tablet verification but all HT-only.
**Confidence cap**: POSSIBLE (ELIMINATED hypothesis scored highest; single-hypothesis support among active candidates).

### Key Term: DE-ME-TE (Post-Total Entry)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Proto-Greek** | *Demeter* (deity name) | Phonological similarity to Linear B *da-ma-te* | **POSSIBLE** | ELIMINATED |
| **Luwian** | Possible Anatolian compound name | DE-ME + -TE suffix (ablative/locative) | POSSIBLE | ACTIVE |
| **Semitic** | No clear root | D-M-T does not match standard Semitic patterns | WEAK | ACTIVE |
| Pre-Greek | Substrate deity name or personal name | Pre-Greek divine names often preserved across languages | POSSIBLE | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Multi-hypothesis (Proto-Greek and Pre-Greek POSSIBLE but ELIMINATED; Luwian POSSIBLE and ACTIVE).
**Critical caveat**: Hapax legomenon (1 occurrence). Max confidence: POSSIBLE per automatic downgrade rules.
**Note**: The spelling DE-ME-TE differs from DA-MA-TE (the KNOWLEDGE.md Level 2 entry). If both refer to the same deity, the vowel variation (E vs. A) may indicate dialectal difference, inflectional change, or that these are in fact different words. Must not conflate without evidence.
**Confidence**: SPECULATIVE (hapax; phonological similarity is suggestive but not probative).

### Key Term: *86 (Section Marker)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| All | UNKNOWN | Undeciphered sign; 24 corpus occurrences; 92% initial position | UNKNOWN | -- |

**Function**: *86 introduces the post-total supplementary section. It receives no quantity and appears to function as a section boundary marker or category classifier. Per KNOWLEDGE.md: 24 occurrences, dominant at Khania (where *86+*188 functions as roundel stamp). Here at HT, it appears to have a different sectional function.
**Confidence**: UNKNOWN (undeciphered sign).

### Key Term: *21F-TU (Post-Total Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | Gendered personal name with classifier | *21F as feminine classifier (PROBABLE); -TU as name element | **POSSIBLE** | ACTIVE |
| **Semitic** | No clear match | No Semitic parallel for classifier + name | WEAK | ACTIVE |
| Pre-Greek | Substrate gendered name | Possible | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No match | WEAK | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE).
**Cross-reference**: *21F-TU-NE appears on HT 117b (same scribe) as a section header for a female-associated list. The -TU element is shared; -NE is additional on HT 117b.
**Confidence**: POSSIBLE.

### Hypothesis Summary for HT 94b

| Term | Best Hypothesis | Confidence | Alternative |
|------|-----------------|------------|-------------|
| KI-RO | Semitic | PROBABLE | K-R paradigm (Luwian admin adoption) |
| KU-RO | Semitic | CERTAIN | *kull* "total" (Level 2 anchor) |
| TU-MA | UNKNOWN | UNKNOWN | Hapax; no analysis possible |
| PA-TA-NE | Luwian (active) | POSSIBLE | Proto-Greek scored highest but ELIMINATED |
| DE-DI | UNKNOWN | UNKNOWN | Hapax; no etymology |
| KE-KI-RU | UNKNOWN | UNKNOWN | Hapax; reduplicated initial |
| SA-RU | Luwian | POSSIBLE | S-R paradigm member; dual name/admin function |
| *86 | UNKNOWN | UNKNOWN | Section marker function |
| RA | UNKNOWN | UNKNOWN | Single syllable; function unclear |
| DE-ME-TE | Multi-hypothesis | SPECULATIVE | Hapax; *Demeter* similarity noted but not claimed |
| *21F-TU | Luwian | POSSIBLE | Feminine classifier + name |

**Dominant pattern**: The K-R vocabulary (KI-RO, KU-RO) is Semitic; personal name morphology (-RU, -NE suffixes) leans Luwian. This is consistent with the project's established domain-specific layering: Semitic administrative loans in a Luwian-influenced morphological framework.

---

## Connected Reading Attempt

### Element-by-Element Interpretation

```
KI-RO               "Outstanding/deficit [items]:"       PROBABLE (Level 2 anchor)
TU-MA          1     "[Entry] TU-MA: 1 [unit]"          POSSIBLE (structure)
PA-TA-NE       1     "[Entry] PA-TA-NE: 1 [unit]"       PROBABLE (cross-tablet name)
DE-DI          1     "[Entry] DE-DI: 1 [unit]"           POSSIBLE (structure)
KE-KI-RU       1     "[Entry] KE-KI-RU: 1 [unit]"       POSSIBLE (structure)
SA-RU          1     "[Entry] SA-RU: 1 [unit]"           PROBABLE (attested name)

KU-RO          5     "Total: 5"                          CERTAIN (arithmetic proof)

*86                  [Section break / new category]       UNKNOWN
RA | DE-ME-TE  1     "[Entry] RA / DE-ME-TE: 1 [unit]"  SPECULATIVE
*21F-TU        1     "[Entry] *21F-TU: 1 [unit]"         POSSIBLE
```

### Full Interpretive Reading (Speculative)

> **Deficit account (KI-RO):**
>
> TU-MA: 1 [unit outstanding]
> PA-TA-NE: 1 [unit outstanding]
> DE-DI: 1 [unit outstanding]
> KE-KI-RU: 1 [unit outstanding]
> SA-RU: 1 [unit outstanding]
>
> **Total outstanding (KU-RO): 5**
>
> ---
>
> **[Supplementary section under *86:]**
>
> RA / DE-ME-TE: 1
> *21F-TU: 1

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| KI-RO = deficit/outstanding | "deficit account" | PROBABLE | Level 2 anchor; 16 corpus attestations; K-R paradigm |
| 5 recipients x 1 each | Personal names with equal allocation | PROBABLE | Position pattern; NAME + 1 format |
| KU-RO = total | "total: 5" | CERTAIN | Level 2 anchor; arithmetic VERIFIED |
| *86 = section break | New category or supplementary | POSSIBLE | Position after KU-RO; 24 corpus attestations in initial position |
| Post-total entries | Additional items not in deficit total | POSSIBLE | Structure evidence only |
| DE-ME-TE = Demeter? | Deity name | SPECULATIVE | Hapax; phonological similarity; not proven |
| *21F-TU = gendered name | Female-associated entry | POSSIBLE | *21F feminine classifier established |
| Name etymologies | Various (see multi-hyp above) | POSSIBLE-SPECULATIVE | Limited attestation |

---

## What We Know for Certain

These elements are established beyond reasonable doubt:

1. **Arithmetic integrity**: 1 + 1 + 1 + 1 + 1 = 5 = KU-RO. The tablet's mathematics are internally consistent and undamaged.
2. **KU-RO function**: KU-RO marks the total. Confirmed at CERTAIN confidence with arithmetic proof on this tablet and 37+ other corpus attestations.
3. **KI-RO function**: KI-RO is a K-R paradigm term functioning as deficit/category marker. Confirmed at PROBABLE confidence with 16 corpus attestations.
4. **Dual KI-RO + KU-RO co-occurrence**: Both terms appear on this tablet in distinct structural positions (initial vs. total line), proving they are not alternative forms for the same function.
5. **Two-section structure**: Section 1 (KI-RO through KU-RO 5) is a complete deficit account. Section 2 (*86 through *21F-TU) is a supplementary section not included in the total.
6. **All Section 1 entries are personal names or headed items**: Each appears in standard NAME + 1 format.
7. **Same scribe (HT Scribe 9)**: Third verified tablet from this scribe (with HT 85a and HT 117a).

## What We Hypothesize

These elements are interpretations, not proven facts:

1. **KI-RO as deficit marker here**: KI-RO's tablet-initial position is consistent with a "deficit/outstanding" reading (items owed), but it could also function as a category marker (as on HT 117a). The KI-RO function on this specific tablet is PROBABLE but not CERTAIN.
2. **Uniform quantity = headcount**: Each entry = 1. This may mean each person owes 1 unit of something, or each person is counted as 1 outstanding allocation. The commodity is unstated.
3. **Post-total section function**: The *86-introduced section may record corrections, additions, or a different category of outstanding items. Its relationship to the main deficit list is unclear.
4. **DE-ME-TE as Demeter**: Phonological similarity exists but is not proof. The hapax status and spelling difference from DA-MA-TE prevent promotion.
5. **RA as qualifier for DE-ME-TE**: RA appears before DE-ME-TE with word divider separation. It may be an abbreviated personal name, a classifier, or a separate entry.
6. ***21F-TU as feminine name**: The *21F classifier suggests a female-associated entry, consistent with *21F-TU-NE on HT 117b (same scribe).
7. **Relation to HT 94a**: Side a has KU-RO 110 (large personnel total). Side b's deficit list of 5 may represent outstanding items from the larger account -- but this connection is SPECULATIVE.

---

## Cross-Corpus Verification

### KI-RO Occurrences (Function Comparison)

| Tablet | Position | Function | Consistent with HT 94b? |
|--------|----------|----------|---------------------------|
| **HT 94b** | b.1 (initial) | Deficit marker | **THIS TABLET** |
| HT 117a | a.1 (header) | Category marker in tripartite header | Partially (initial position; different function) |
| HT 88 | Header | Section marker | Yes (initial position) |
| HT 123a | a.9 | Deficit marker (after total) | Partially (deficit function; different position) |

**Verdict**: KI-RO's multi-functional usage is confirmed. On HT 94b it functions as a deficit/outstanding marker at tablet-initial position, consistent with one of its two established functions.

### KU-RO Occurrences (Verified Subset)

| Tablet | KU-RO Value | Arithmetic Status | Scribe |
|--------|-------------|-------------------|--------|
| HT 85a | 66 | VERIFIED (exact) | HT Scribe 9 |
| HT 117a | 10 | VERIFIED (exact) | HT Scribe 9 |
| **HT 94b** | **5** | **VERIFIED (exact)** | **HT Scribe 9** |
| HT 9b | 24 | VERIFIED (exact) | Unknown |
| HT 13 | 130.5 | Near-match | Unknown |
| HT 122a/b | 97 (PO-TO-KU-RO) | VERIFIED | Unknown |

**HT Scribe 9 track record**: All three verified tablets from this scribe show exact arithmetic matches (66, 10, 5). This scribal consistency reinforces confidence in KU-RO as a formal totaling convention.

### SA-RU Occurrences

| Tablet | Context | Consistent? |
|--------|---------|-------------|
| HT 86a | Administrative list | Yes |
| HT 86b | Administrative list | Yes |
| **HT 94b** | Recipient with quantity 1 | **THIS TABLET** |
| HT 95a | GRA distribution | Yes (commodity context) |
| HT 95b | Administrative list | Yes |
| HT 123+124a | Administrative list | Yes |

**Verification**: SA-RU consistently appears in administrative recipient/entry contexts. All 6 attestations are HT-only. Reading as personal name or S-R admin term is CORPUS-CONSISTENT.

### PA-TA-NE Occurrences

| Tablet | Context | Consistent? |
|--------|---------|-------------|
| **HT 94b** | Recipient with quantity 1 | **THIS TABLET** |
| HT 122a | Recipient in multi-section tablet | Yes (recipient position) |
| HTWa1019 | Administrative context | Yes |

**Verification**: PA-TA-NE appears on 3 tablets, always in recipient/entry position. Reading as personal name is CORPUS-CONSISTENT.

### DE-ME-TE Cross-Reference

**Hapax legomenon** -- appears only on HT 94b. No cross-corpus verification possible. Compare:
- DA-MA-TE (KNOWLEDGE.md Level 2): Appears at peak sanctuary (different context, different vowel pattern)
- DA-MA-TE on HT 94b side a: NOT present (no DA-MA-TE on this tablet)

The DE-ME-TE / DA-MA-TE relationship remains UNCONFIRMED.

---

## First Principles Verification

### [1] KOBER: Was analysis data-led, not assumption-led?
**PASS**

Evidence: Started with arithmetic verification (data), then structural pattern analysis (KI-RO/KU-RO framework, post-total section), then anchor identification by level. Language hypotheses tested AFTER structural reading was established. DE-ME-TE similarity to Demeter noted but NOT assumed or forced.

### [2] VENTRIS: Was any evidence forced to fit?
**PASS**

Evidence: Acknowledged:
- TU-MA, DE-DI, KE-KI-RU left as UNKNOWN (hapax; not forced to etymologies)
- DE-ME-TE = Demeter noted as SPECULATIVE, not asserted
- RA function left uninterpreted rather than guessed
- *86 function noted as UNKNOWN rather than forced to a reading
- SA-RU dual function (name vs. admin term) explicitly flagged
- Post-total section relationship to main list left as POSSIBLE

### [3] ANCHORS: Were readings built from confirmed anchors outward?
**PASS**

Anchors used (in order of confidence):
1. Level 2: KU-RO = total (CERTAIN -- arithmetic proof)
2. Level 2: KI-RO = deficit/category (PROBABLE -- K-R paradigm)
3. Level 4: Structural patterns -- deficit marker, list, total, supplementary section (MEDIUM-HIGH)
4. Level 5: *21F classifier function (MEDIUM)
5. Level 6: Name etymologies, DE-ME-TE similarity (LOW-SPECULATIVE)

No reading exceeds anchor support level.

### [4] MULTI-HYP: Were ALL seven hypotheses tested?
**PASS**

For each key term:
- KI-RO: Semitic **PROBABLE**, Luwian POSSIBLE, Pre-Greek POSSIBLE, Proto-Greek WEAK/ELIMINATED, Hurrian WEAK/ELIMINATED, Hattic INDETERMINATE/ELIMINATED, Etruscan WEAK/ELIMINATED
- KU-RO: Semitic **CERTAIN**, Luwian HIGH (function), others WEAK/ELIMINATED
- SA-RU: Luwian **POSSIBLE**, Semitic POSSIBLE, others WEAK/ELIMINATED
- PA-TA-NE: Luwian POSSIBLE (active), Proto-Greek POSSIBLE (ELIMINATED), others WEAK/ELIMINATED
- DE-ME-TE: Multi-hypothesis (Luwian POSSIBLE active; Proto-Greek and Pre-Greek POSSIBLE but ELIMINATED)
- *21F-TU: Luwian POSSIBLE, others WEAK/ELIMINATED

All seven hypotheses tested for all key terms. Five eliminated hypotheses noted as such throughout.

### [5] NEGATIVE: Was absence of patterns considered?
**PASS**

Absences noted:
- **No commodity logograms**: Pure deficit list with no GRA, OLE, VIN, FIC, CYP. The outstanding commodity is unstated.
- **No SA-RA₂**: Unlike HT 28 and HT 94a, no "allocation" marker. The deficit account uses KI-RO instead.
- **No fractions**: All quantities are integers (1). Consistent with personnel/headcount rather than commodity measurement.
- **No toponyms**: Cannot anchor to geographic confirmation.
- **No Greek case endings**: No -os, -on, -oi in any name.
- **No triconsonantal Semitic morphology**: Names do not exhibit Semitic root patterns.
- **No ergative markers**: No Hurrian-type case system.
- **No prefixing morphology**: No Hattic-type prefixes.
- **No PO-TO-KU-RO**: No grand total -- this is a section-level deficit only.

### [6] CORPUS: Were readings verified across all occurrences?
**PASS**

| Reading | Occurrences Checked | Result |
|---------|---------------------|--------|
| KU-RO = total | 37 corpus-wide | Consistent |
| KI-RO multi-function | 16 corpus-wide | Confirmed (header + deficit) |
| SA-RU attestation | 6 HT tablets | Consistent |
| PA-TA-NE attestation | 3 HT tablets | Consistent |
| DE-ME-TE | 1 (hapax) | Cannot verify cross-corpus |

**ALL PASS: Analysis VALID** (DE-ME-TE limitation documented per hapax downgrade rule)

---

## Comparison: HT 94b vs. HT 117a vs. HT 85a (Same Scribe)

| Feature | HT 94b | HT 117a | HT 85a |
|---------|--------|---------|--------|
| Scribe | HT Scribe 9 | HT Scribe 9 | HT Scribe 9 |
| KU-RO Value | 5 | 10 | 66 |
| Arithmetic | VERIFIED (exact) | VERIFIED (exact) | VERIFIED (exact) |
| KI-RO | Present (initial) | Present (header) | Absent |
| Content Type | Deficit list (NAME + 1) | Personnel roster (NAME + 1) | Commodity distribution |
| Section Count | 2 | 3 | 1 |
| Commodity Logograms | NONE | NONE | VIR+[?] |
| Post-Total Section | Yes (*86) | Yes (SA-TA, *21F-TU-NE) | No |
| Fractions | No | No | No |

**Scribe 9 profile (expanded)**: Produces deficit lists, personnel rosters, and commodity records. Uses KU-RO totals with exact arithmetic (3/3 verified). Employs multi-section structure with section markers. Uses KI-RO in both deficit and header functions. A meticulous, consistent administrator.

---

## Novel Observations

### 1. Third Consecutive Exact KU-RO from Scribe 9

HT 94b is the third tablet from HT Scribe 9 with exact KU-RO arithmetic (5=5, joining 10=10 on HT 117a and 66=66 on HT 85a). This is not coincidental -- Scribe 9 demonstrates consistent computational accuracy. The probability of three consecutive exact matches by chance (given that some tablets show mismatches due to lacunae or damage) further validates both the KU-RO = total reading and the scribal identification.

### 2. KI-RO + KU-RO Co-Occurrence Pattern

HT 94b joins HT 117a as a dual KI-RO + KU-RO tablet from the same scribe. The structural parallel is striking:
- HT 117a: KI-RO in tripartite header, KU-RO as total (10)
- HT 94b: KI-RO as initial deficit marker, KU-RO as total (5)

Both tablets have uniform allocation (all 1's) and lack commodity logograms. The K-R paradigm's multi-functional nature is confirmed by a single scribe using both terms in different structural positions across tablets.

### 3. Post-Total Supplementary Sections

HT 94b and HT 117a both have entries AFTER the KU-RO total, introduced by section markers (*86 on HT 94b; SA-TA and *21F-TU-NE on HT 117a). HT 85a does NOT have a post-total section. This suggests Scribe 9 uses post-total sections for addenda or secondary categories, but only when the document requires them.

### 4. The *86 Section as Administrative Addendum

The post-total section (*86, RA/DE-ME-TE, *21F-TU) adds 2 entries with quantity 1 each. These are NOT included in the KU-RO total. This deliberate exclusion has several possible interpretations:
- The addendum records a different category of deficit
- These entries were added after the main account was totaled
- The *86 section is a note or cross-reference, not part of the deficit tally

### 5. Uniform Allocation Pattern

Like HT 117a, every entry on HT 94b has quantity 1. This eliminates the possibility of differential commodity distribution and strongly suggests headcount or per-person allocation. The deficit of 5 individuals (or 5 units per individual) is the simplest possible deficit account.

### 6. DE-ME-TE Spelling Variant

If DE-ME-TE (this tablet) and DA-MA-TE (Level 2 entry, peak sanctuary) refer to the same word/deity, the E/A vowel variation is significant. Possible explanations:
- Dialectal variation within Minoan (e.g., site-specific or period-specific)
- Inflectional change (different grammatical case or form)
- Two genuinely different words with coincidental phonological similarity
- Scribal variation (though Scribe 9 is demonstrably consistent)

This observation is recorded for future investigation but NOT promoted as a finding.

---

## Sources Consulted

1. **lineara.xyz corpus** -- HT94b transliteration and metadata
2. **arithmetic_verifier** -- Rosetta skeleton and sum verification
3. **hypothesis_tester.py** -- Multi-hypothesis scoring for KI-RO, KU-RO, SA-RU, PA-TA-NE
4. **reading_readiness_scorer.py** -- Coverage assessment (45.5%, score 0.610)
5. **KNOWLEDGE.md** -- K-R paradigm, S-R paradigm, *86 analysis, *21F classifier, confirmed readings
6. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework, confidence calibration
7. **MASTER_STATE.md** -- Current metrics and operational baseline
8. **Gordon, C.H. (1966)** -- KU-RO = *kull* (Semitic "total")
9. **Salgarella, E. (2020)** -- Sign classification, tablet structure
10. **Younger, J. (2024)** -- Linear A Texts: Introduction; transcriptions
11. **Schoep, I. (2002)** -- Transaction term analysis; tablet classification

---

## Appendix: Arithmetic Verification Detail

### Raw Computation

```
Entry 1:  TU-MA        =   1
Entry 2:  PA-TA-NE     =   1
Entry 3:  DE-DI        =   1
Entry 4:  KE-KI-RU     =   1
Entry 5:  SA-RU        =   1
                           ---
Computed sum             =   5
Stated KU-RO             =   5
Difference               =   0
Status                   =  VERIFIED (exact match)
```

### Verification Quality Metrics

| Metric | Value |
|--------|-------|
| Number of entries | 5 |
| Fraction count | 0 |
| Damaged entries | 0 |
| Ambiguous readings | 0 |
| Sum accuracy | 100% (exact) |
| Verification class | Class A (no caveats) |

This is a **Class A verification**: no fractions, no damage, no ambiguity. The arithmetic proof is as strong as it can be for any Linear A document.

### Post-Total Entries (NOT Included in KU-RO)

```
Post-total 1:  DE-ME-TE  =  1
Post-total 2:  *21F-TU   =  1
                             ---
Post-total sum            =  2   (NOT included in KU-RO 5)
```

---

## Morphological and Onomastic Constraints

### TU-MA (hapax)

- **Morphological decomposition**: 2-syllable word with -MA suffix (20 corpus-wide attestations). Root skeleton T-M. CV-CV (short) pattern.
- **Paradigm membership**: No paradigm match found.
- **Onomastic analysis**: Not in onomastic top candidates. -MA suffix appears in 2 onomastic candidates (SA-MA at HT).
- **Constraint summary**: No paradigm match found. Hapax; insufficient data for morphological exploitation.

### DE-DI (hapax)

- **Morphological decomposition**: 2-syllable word with -DI suffix (17 attestations). Root skeleton D-D. CV-CV (short) pattern.
- **Paradigm membership**: No paradigm match found. The D-D root (possible reduplication) is not part of any known paradigm.
- **Onomastic analysis**: Not in onomastic top candidates. The DE- initial element appears in compound names (DE-ME-TE on this tablet; DI-DE-RU on HT 86a).
- **Constraint summary**: No paradigm match found. The reduplicated D-D pattern is unusual and may indicate a shortened or hypocoristic name form.

### KE-KI-RU (hapax)

- **Morphological decomposition**: 3-syllable word with -RU suffix (21 attestations). Root skeleton K-K-R. KE-KI- shows possible reduplication of velar initial.
- **Paradigm membership**: No specific paradigm match. However, -RU suffix is shared with SA-RU (S-R paradigm, P-SR-9) and A-KA-RU (paradigm P-ØKR-4), placing KE-KI-RU in the productive -RU name class.
- **Onomastic analysis**: Not in top name candidates. CV-CV-CV (medium) pattern standard for 3-syllable names.
- **Constraint summary**: -RU suffix membership confirmed (productive suffix class). Reduplicated KE-KI- element is distinctive. No paradigm match found for the full word.

### DE-ME-TE (hapax)

- **Morphological decomposition**: 3-syllable word with -TE suffix (44 attestations, 4th most common). Root skeleton D-M-T. DE- prefix not in top 10 prefixes.
- **Paradigm membership**: No K-R, S-R, or O-D paradigm match.
- **Onomastic analysis**: Not in top name candidates. However, decoded name DA-MA-TE = "Mother Earth / Earth Mother (deity name)" is listed at POSSIBLE confidence. DE-ME-TE differs in vowel pattern (E-E-E vs. A-A-E for DA-MA-TE). The onomastic comparator identifies DA-MA-TE as the sole POSSIBLE-level decoded name.
- **Theophoric connection**: The DA-MA-TE theophoric link suggests DE-ME-TE may be a vowel variant of the same deity name, but the E/A variation is unexplained and may indicate different words.
- **Constraint summary**: -TE suffix productive. Possible connection to DA-MA-TE deity name (SPECULATIVE). Hapax; vowel variation from DA-MA-TE unresolved.

### *86 and RA

- **Morphological decomposition**: *86 is an undeciphered sign (24 corpus occurrences, 92% initial position). RA is a single syllable -- too short for morphological decomposition.
- **Paradigm membership**: None for either.
- **Onomastic analysis**: Neither appears in onomastic candidates.
- **Constraint summary**: No paradigm match found. *86 functions as a section marker/classifier; RA may be an abbreviated name or qualifier.

---

*Connected reading completed 2026-02-21 as part of Lane G: Reading Attempts (KU-RO Arithmetic Verification Series).*

*Document structure, deficit marker (KI-RO), and total function (KU-RO) are established with PROBABLE-CERTAIN confidence. The dual KI-RO + KU-RO co-occurrence from HT Scribe 9 (third verified tablet) strengthens both K-R paradigm readings. Post-total supplementary section noted but not fully interpreted. Personal names identified by position; individual etymologies remain at POSSIBLE-SPECULATIVE. The arithmetic verification is exact and undamaged -- a Class A verification.*
