# ZA6a Connected Reading Report

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
| **Tablet ID** | ZA6a |
| **Site** | Zakros |
| **Period** | Late Minoan I |
| **Scribe** | Unknown |
| **Support** | Stone vessel |
| **Document Type** | Mixed commodity distribution (OLIV, GRA, *304) |
| **Arithmetic Status** | NO_KURO (no KU-RO present) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |
| **Reading Readiness** | Score 0.388 |
| **Cross-Site Significance** | Zakros -- mixed commodity; large quantities; 3 anchored words |

---

## Transliteration

```
Line 1:   *305-WA-NA  *171  19
Line 2:   *34-JU-TE-MI
Line 3:   180
Line 4:   I-SE
Line 5:   OLIV  15
Line 6:   OLIV  10
Line 7:   I
Line 8:   2
Line 9:   PU₂-RA₂  GRA+PA
Line 10:  20
Line 11-14: (empty lines)
Line 15:  𐄁  OLIV  25  *304  20  I-SE
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| *305 | Unknown | UNCERTAIN | Low |
| WA | AB 54 | CERTAIN | High |
| NA | AB 06 | CERTAIN | High |
| *171 | Unknown | UNCERTAIN | Low |
| *34 | Unknown | UNCERTAIN | Low |
| JU | AB 65 | CERTAIN | Moderate |
| TE | AB 04 | CERTAIN | High |
| MI | AB 73 | CERTAIN | High |
| I | AB 28 | CERTAIN | High |
| SE | AB 09 | CERTAIN | High |
| PU₂ | AB 29b | CERTAIN | Moderate |
| RA₂ | AB 76 | CERTAIN | Moderate |
| OLIV | Logogram | CERTAIN | Pictographic |
| GRA+PA | Compound logogram | CERTAIN | GRA = grain |
| *304 | Unknown logogram | HIGH | Commodity logogram |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None confirmed.** *305-WA-NA could be a toponym but *305 is undeciphered.

### Level 2: Linear B Cognates + Position (HIGH)

**None.** No KU-RO or K-R terms, consistent with Zakros pattern (KU-RO present at ZA15b but KI-RO absent).

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **OLIV** | Olives | Pictographic origin; Linear B cognate | 3 occurrences (15, 10, 25) |
| **GRA+PA** | Grain variant (GRA with PA qualifier) | GRA = grain; +PA = variant marker | 1 occurrence (with PU₂-RA₂) |
| ***304** | Unknown commodity logogram | 93% word-initial/standalone; commodity position | 1 occurrence (20, after OLIV 25) |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| WORD + COMMODITY + QUANTITY | Standard distribution format | Multiple entries follow this pattern |
| Large quantities (19, 180, 15, 10, 20, 25, 20) | Major distribution | Larger scale than most analyzed tablets |
| Mixed commodities (OLIV, GRA+PA, *304) | Multi-commodity accounting | 3+ commodity types |
| I-SE repeated | Administrative term or category marker | Appears in lines 4 and 15 |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| *305-WA-NA | 3-syllable; -WA-NA ending | WA and NA are known syllables; *305 undeciphered |
| *34-JU-TE-MI | 4-syllable; -TE-MI ending | Possible personal name; -TE/-MI productive suffixes |
| I-SE | 2-syllable; hypothesis_tester best=semitic PROBABLE | Administrative term |
| PU₂-RA₂ | 2-syllable; uses variant signs PU₂, RA₂ | Personal name or toponym |

---

## Structural Analysis

### Document Type

**Mixed commodity distribution on stone vessel at Zakros (OLIV + GRA + *304)**

ZA6a is one of the more complex Zakros inscriptions, recording distributions of olives (OLIV), grain (GRA+PA), and an unknown commodity (*304) in substantial quantities. The stone vessel support suggests a semi-permanent or archival record.

### Document Structure

```
[H]  *305-WA-NA                Header: source / contributor
[?]  *171                      Unknown sign/qualifier
[#]  19                        Quantity: 19 units (commodity unspecified)
---
[R]  *34-JU-TE-MI              Recipient 1 (personal name?)
---
[#]  180                       Quantity: 180 units (largest on tablet)
---
[?]  I-SE                      Administrative term / category marker
---
[C]  OLIV                      Commodity: olives
[#]  15                        Quantity: 15 units
---
[C]  OLIV                      Commodity: olives
[#]  10                        Quantity: 10 units
---
[R]  I                         Recipient / marker (single syllable)
---
[#]  2                         Quantity: 2 units
---
[R]  PU₂-RA₂                   Recipient 2 (personal name?)
[C]  GRA+PA                    Commodity: grain variant
---
[#]  20                        Quantity: 20 units
---
(empty lines)
---
     𐄁                         Word divider / section marker
[C]  OLIV                      Commodity: olives
[#]  25                        Quantity: 25 units
[C]  *304                      Commodity: unknown
[#]  20                        Quantity: 20 units
[?]  I-SE                      Administrative term (repeated)
```

### Notable Structural Features

1. **Large quantities**: 180 units (the largest single allocation on any Zakros tablet analyzed). Total visible quantities: 19 + 180 + 15 + 10 + 2 + 20 + 25 + 20 = 291 units across multiple commodities.
2. **Mixed commodities**: OLIV (3 entries: 15, 10, 25 = 50 total), GRA+PA (1 entry: 20), *304 (1 entry: 20). The 180 and 19 quantities have no specified commodity.
3. **I-SE repeated**: Appears twice (lines 4 and 15), suggesting a structural/functional role rather than a personal name. hypothesis_tester: best=semitic, PROBABLE.
4. **Stone vessel**: Like ZA15, this is inscribed on stone rather than clay.
5. **\*304 as commodity logogram**: *304 is confirmed as a commodity logogram (93% initial/standalone, 42 corpus-wide, 5 sites). Its identity is SPECULATIVE but HIGH for commodity function.
6. **\*305-WA-NA as header**: Position-initial 3-syllable word with undeciphered *305. Could be a toponym.
7. **Empty lines**: Lines 11-14 are empty, suggesting a section break or end of one document/beginning of another.

---

## Word-by-Word Analysis

### *305-WA-NA

**Corpus frequency**: Limited. *305 is an undeciphered sign.
**Analysis**: 3-syllable word in header position. -WA-NA ending: WA (Luwian quotative particle?) + NA. Could be a toponym (place-name ending in -na is attested in Aegean onomastics).
**Hypothesis testing**: Cannot test due to undeciphered *305.
**Confidence**: UNKNOWN (sign undeciphered)

### *34-JU-TE-MI

**Corpus frequency**: Limited. *34 is an undeciphered sign.
**Analysis**: 4-syllable word in recipient position. -TE-MI ending has parallels with Luwian nominal morphology (-TE suffix + -MI locative/possessive?). Could be a personal name.
**Hypothesis testing**: Cannot fully test due to undeciphered *34.
**Confidence**: POSSIBLE (personal name by position)

### I-SE

**Hypothesis testing** (hypothesis_tester output):
- **Best**: Semitic (PROBABLE)
- **Analysis**: I-SE appears twice on this tablet, suggesting a functional/administrative role rather than a personal name. If Semitic, could relate to a root meaning "to give" or "to set." As an administrative term at Zakros, it may function as a category marker or transaction type.
**Cross-corpus**: I-SE attested at multiple sites.
**Confidence**: PROBABLE (administrative term)

### PU₂-RA₂

**Analysis**: 2-syllable word using variant signs PU₂ and RA₂ (not standard PU and RA). The use of variant signs may indicate different phonetic values from standard PU/RA, or scribal preference.
**Hypothesis testing**: Not in hypothesis_results as tested word.
**Cross-corpus**: PU₂-RA₂ appears in ZA context.
**Confidence**: POSSIBLE (personal name by position, before GRA+PA commodity)

---

## Multi-Hypothesis Testing

### Key Term: I-SE (Administrative Term)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Semitic** | Semitic root (give/set/place) | hypothesis_tester PROBABLE; admin context | **PROBABLE** | ACTIVE |
| Luwian | Possible Luwian form | I- prefix; -SE ending | POSSIBLE | ACTIVE |
| Pre-Greek | Substrate term | No diagnostic features | WEAK | ELIMINATED |
| Proto-Greek | No Greek parallel | No match | WEAK | ELIMINATED |
| Hurrian | No Hurrian parallel | No match | WEAK | ELIMINATED |
| Hattic | No Hattic parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No Etruscan parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Semitic (PROBABLE). Administrative vocabulary tendency.

### Other Terms

| Term | Best Hypothesis | Confidence | Note |
|------|-----------------|------------|------|
| *305-WA-NA | INDETERMINATE | UNKNOWN | Undeciphered *305 |
| *34-JU-TE-MI | INDETERMINATE | POSSIBLE (name) | Undeciphered *34 |
| PU₂-RA₂ | Not tested | POSSIBLE (name) | Position-based |
| OLIV | N/A (logogram) | CERTAIN | Level 3 anchor |
| GRA+PA | N/A (logogram) | HIGH | Grain variant |
| *304 | N/A (logogram) | HIGH (function) | Commodity logogram |

---

## Connected Reading Attempt

### Full Interpretive Reading (Speculative)

> **From *305-WA-NA** [source/contributor]:
> [*171 qualifier] -- 19 units [commodity unspecified]
>
> **To *34-JU-TE-MI** [recipient]:
> 180 units [commodity unspecified -- largest allocation]
>
> **I-SE** [category/transaction type]:
> Olives (OLIV): 15 units
> Olives (OLIV): 10 units
> I [marker?]: 2 units
>
> **PU₂-RA₂** [recipient]:
> Grain variant (GRA+PA): 20 units
>
> ---
>
> [Section break]
>
> Olives (OLIV): 25 units
> *304 [unknown commodity]: 20 units
> **I-SE** [repeated category marker]
>
> *A large-scale mixed commodity distribution at Zakros recording olives (50 total), grain (20), and *304 commodity (20), with 180 + 19 units of unspecified commodity. Total visible: ~291 units.*

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| *305-WA-NA = header | Source/contributor | POSSIBLE | Position-initial; undeciphered *305 |
| *34-JU-TE-MI = recipient | Personal name | POSSIBLE | Position before quantity |
| I-SE = admin term | Category/transaction | PROBABLE | Semitic; repeated on tablet |
| OLIV = olives | "Olives" | CERTAIN | Level 3 anchor |
| GRA+PA = grain variant | "Grain (PA type)" | HIGH | Compound logogram |
| *304 = commodity | Unknown commodity | HIGH (function) | Commodity logogram (93% initial) |
| PU₂-RA₂ = recipient | Personal name | POSSIBLE | Position before commodity |
| Quantities | Numerals | CERTAIN | Unambiguous |

---

## What We Know For Certain

1. **Commodities**: OLIV (olives, 3 entries totaling 50), GRA+PA (grain variant, 20), *304 (unknown, 20). CERTAIN.
2. **Large scale**: 291+ total visible units, including 180 in a single allocation. CERTAIN.
3. **Mixed commodity**: At least 3 commodity types in one document. CERTAIN.
4. **Stone vessel**: Semi-permanent record. CERTAIN.
5. **I-SE appears twice**: Structural/functional role, not a personal name. PROBABLE.
6. **No KU-RO/KI-RO**: No K-R paradigm terms at Zakros (KU-RO present on ZA15b but absent here). CERTAIN.

## What We Hypothesize

1. **I-SE as administrative separator**: The repeated I-SE may function as a category marker or transaction type, separating sections of the distribution. PROBABLE.
2. ***305-WA-NA as toponym**: Position-initial, 3-syllable word ending in -NA (common toponym suffix). Could designate the source/origin of goods. POSSIBLE.
3. **180 units as institutional allocation**: The single 180-unit allocation to *34-JU-TE-MI is by far the largest on any Zakros tablet. This suggests an institutional-scale recipient (temple, palace, workshop). POSSIBLE.
4. **Zakros mixed commodity economy**: Unlike the wine-focused ZA15, ZA6a shows olives and grain at Zakros, indicating a diversified economy. POSSIBLE.

---

## Cross-Corpus Verification

### I-SE Occurrences

I-SE is attested at multiple sites. Its repeated appearance on ZA6a (lines 4 and 15) confirms a functional role. **PARTIAL VERIFICATION**.

### OLIV Logogram

OLIV is CORPUS-VERIFIED across multiple sites. Its presence at Zakros alongside the well-documented wine focus (ZA15) shows commodity diversity.

### *304 as Commodity

*304 (42 corpus-wide, 5 sites: HT, KH, PH, PY, ZA) is confirmed as a commodity logogram by position and frequency. Its specific identity remains unknown. **PARTIAL VERIFICATION** (function confirmed; identity unknown).

### GRA+PA Compound

GRA+PA appears at ZA6a (this tablet) and ZA11a (below). The GRA base is CERTAIN; +PA qualifier function is consistent with compound logogram system (cf. OLE+U, CYP+D). **PARTIAL VERIFICATION**.

---

## First Principles Verification

### [1] KOBER: **PASS** -- Logograms and structural patterns identified before linguistic analysis.
### [2] VENTRIS: **PASS** -- Undeciphered signs (*305, *34, *304) left as UNKNOWN. I-SE repeated role noted without forcing specific meaning.
### [3] ANCHORS: **PASS** -- Level 3 (OLIV, GRA+PA) and Level 4 (structural patterns). Readings capped appropriately.
### [4] MULTI-HYP: **PASS** -- I-SE tested against all seven. Logograms agreed by all. Undeciphered signs INDETERMINATE.
### [5] NEGATIVE: **PASS** -- No KU-RO/KI-RO, no VIN (wine absent despite Zakros wine focus), no fractions, no A-DU.
### [6] CORPUS: **PASS** -- OLIV, *304 corpus-verified. I-SE partial.

---

## Novel Observations

### 1. Zakros Beyond Wine

ZA6a records olives (OLIV) and grain (GRA+PA), expanding Zakros's documented commodity portfolio beyond the wine (VIN) focus established by ZA15. Zakros was not a single-commodity site -- it administered multiple agricultural products.

### 2. 180-Unit Single Allocation

The 180-unit allocation to *34-JU-TE-MI is the largest single-recipient allocation at any non-HT site in the analyzed corpus. This suggests institutional-scale distribution (palace, temple, or major workshop), not personal allocations.

### 3. I-SE as Structural Marker

The doubled appearance of I-SE -- once mid-tablet (line 4) and once at the end (line 15) -- suggests it functions as a section-level marker or category label. This parallels how SA-RA₂ functions at HT, though I-SE's specific meaning differs. I-SE may be part of the Zakros administrative vocabulary that replaces or complements the HT SA-RA₂ system.

### 4. *304 at Zakros

*304's presence at Zakros (alongside HT, KH, PH, PY) confirms its cross-site distribution. On ZA6a, it appears after OLIV in the final section (OLIV 25, *304 20), suggesting a commodity related to or traded alongside olives.

---

## Sources Consulted

1. **lineara.xyz corpus** -- ZA6a transliteration and metadata
2. **arithmetic_verifier** -- Rosetta skeleton
3. **hypothesis_tester.py** -- I-SE, SI-PI-KI, *28B-NU-MA-RE
4. **KNOWLEDGE.md** -- *304 analysis, commodity anchors, Zakros wine focus
5. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework
6. **Salgarella, E. (2020)** -- GORILA compound logogram system

---

*Connected reading completed 2026-02-22. ZA6a is a complex mixed-commodity distribution at Zakros (OLIV 50 total, GRA+PA 20, *304 20, plus 199 unspecified). 180-unit single allocation is the largest at any non-HT site. I-SE repeated twice suggests administrative function (Semitic PROBABLE). Zakros commodity portfolio expanded beyond wine to include olives and grain. Overall reading confidence: HIGH for commodity identification; POSSIBLE-PROBABLE for word functions.*
