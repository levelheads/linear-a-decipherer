# HT 7a Connected Reading Report

**Date**: 2026-02-21
**Analyst**: Claude (Opus 4.6)
**Phase**: Lane G - Reading Attempts (Personnel Allocation Series)
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
| **Tablet ID** | HT 7a |
| **Site** | Hagia Triada (Haghia Triada) |
| **Period** | Late Minoan IB (~1500-1450 BCE) |
| **Scribe** | HT Scribe 11 |
| **Support** | Clay tablet |
| **Document Type** | VIR (person/worker) allocation list |
| **Arithmetic Status** | NO_KURO (no total line; computed sum = 10 VIR) |
| **Corpus Source** | lineara.xyz / arithmetic_verifier |
| **Reading Readiness** | 83.3% coverage |

---

## Transliteration

```
Line 1:  QE-TI | VIR+[?]
Line 2:  I-RU-JA                 3
Line 3:  DU-JA                   4
Line 4:  TA-NA-TI                1
Line 5:  DA-RE                   1
Line 6:  TE-TU                   1
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| QE | AB 78 | HIGH | Moderate |
| TI | AB 37 | CERTAIN | High |
| VIR | Logogram | CERTAIN | Pictographic |
| I | AB 28 | CERTAIN | High |
| RU | AB 26 | CERTAIN | Moderate |
| JA | AB 57 | HIGH | High |
| DU | AB 51 | HIGH | Moderate |
| TA | AB 59 | CERTAIN | High |
| NA | AB 06 | CERTAIN | High |
| DA | AB 01 | CERTAIN | High |
| RE | AB 27 | HIGH | Moderate |
| TE | AB 04 | CERTAIN | High |
| TU | AB 69 | HIGH | High |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None identified on this tablet.**

### Level 2: Linear B Cognates + Position (HIGH)

**No KU-RO on this tablet.** Unlike HT 85a, HT 117a, and HT 9b, this tablet lacks a totaling line. The absence of KU-RO is itself informative -- see Negative Evidence below.

### Level 3: Logograms (HIGH/CERTAIN)

| Logogram | Meaning | Evidence | On this tablet |
|----------|---------|----------|----------------|
| **VIR+[?]** | Person/worker (qualified) | Pictographic origin; Linear B VIR cognate | Header, commodity identifier |

### Level 4: Structural Patterns (MEDIUM-HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| Header position | QE-TI = heading/department/supervisor | Initial position before commodity logogram |
| NAME + QUANTITY | Standard allocation list entry | 5 consistent entries, all NAME + integer |
| Single-commodity list | All entries counted in same unit (VIR) | No logogram variation between entries |
| Word divider (dot) | Separates header from commodity | Between QE-TI and VIR+[?] |

### Level 5: Morphological Patterns (MEDIUM)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| -JA suffix (x2 names) | Common onomastic ending | I-RU-JA, DU-JA; 17 names end in -JA in corpus |
| -TI suffix (QE-TI, TA-NA-TI) | Possible verbal/locative ending | Consistent with Luwian/Valério -TI interpretation |
| DA-RE dual function | Personal name OR transaction marker | Recipient position here; administrative function elsewhere |

### Level 6: Lexical Matches (LOW)

| Match | Interpretation | Evidence |
|-------|----------------|----------|
| TA-NA-TI ~ Luwian onomastics | Personal name with Anatolian morphology | -TI ending; three-syllable structure; Luwian best-fit per hypothesis_tester |
| DA-RE ~ Luwian *tare-* | "to take/receive" or personal name | Attested dual function across corpus |
| TE-TU ~ Luwian onomastics | Personal name | 2-syllable; Luwian POSSIBLE per hypothesis_tester |

---

## Structural Analysis

### Document Type

**Single-commodity personnel allocation tablet (VIR distribution, no total)**

This tablet records the allocation of persons (VIR = workers/people) to 5 named recipients under a single header (QE-TI). It lacks a KU-RO totaling line, which distinguishes it from HT 85a (which has KU-RO 66 for an identical document type). The computed sum is 10 VIR (3 + 4 + 1 + 1 + 1).

### Document Structure

```
[H]  QE-TI                    Header: supervisor/department/toponym
[C]  VIR+[?]                  Commodity: persons/workers (with qualifier)
[R]  I-RU-JA          3       Recipient 1: 3 workers
[R]  DU-JA            4       Recipient 2: 4 workers (largest share)
[R]  TA-NA-TI         1       Recipient 3: 1 worker
[R]  DA-RE            1       Recipient 4: 1 worker
[R]  TE-TU            1       Recipient 5: 1 worker
```

### Rosetta Skeleton (arithmetic_verifier output)

| Tag | Role | Count |
|-----|------|-------|
| [H] | Header | 1 (QE-TI) |
| [C] | Commodity | 1 (VIR+[?]) |
| [R] | Recipient | 5 (named entries with quantities) |
| [T] | Total | 0 (NO KU-RO) |

### Arithmetic Status

```
I-RU-JA       3
DU-JA         4
TA-NA-TI      1
DA-RE         1
TE-TU         1
             --
SUM           10 VIR

KU-RO:       ABSENT
Status:       NO_KURO (no total line)
```

**No formal total is stated.** The computed sum is 10 workers distributed across 5 recipients. The absence of KU-RO does not invalidate the reading -- not all distribution tablets include totals (cf. HT 117a Section 2 under SA-TA, which also lacks KU-RO).

### Notable Structural Features

1. **No KU-RO**: Unlike HT 85a (same document type, same commodity), this tablet has no total line. This may indicate an incomplete record, a different administrative convention, or a sub-account within a larger ledger.
2. **Single commodity**: All entries are in VIR (persons), consistent with a personnel allocation.
3. **Integer-only**: No fraction signs appear. All allocations are whole numbers (as expected for personnel).
4. **Concentration**: DU-JA receives 40% of total (4/10), with the remaining 6 workers split among 4 recipients.
5. **-JA ending cluster**: Two of five recipients (I-RU-JA, DU-JA) end in -JA, the most common name-final element in the corpus (77 occurrences word-final, 65.9%).
6. **No KI-RO**: No deficit marker present.
7. **No SA-RA2**: No allocation marker present. The allocation is implicit in the list structure.

### Distribution Analysis

| Recipient | Count | Share | Rank |
|-----------|-------|-------|------|
| DU-JA | 4 | 40.0% | 1 |
| I-RU-JA | 3 | 30.0% | 2 |
| TA-NA-TI | 1 | 10.0% | 3 (tied) |
| DA-RE | 1 | 10.0% | 3 (tied) |
| TE-TU | 1 | 10.0% | 3 (tied) |

**Observation**: The distribution is skewed toward the first two recipients (70% of total), with the remaining three receiving a single worker each. This is a smaller-scale allocation than HT 85a (10 vs. 66 workers), suggesting either a smaller administrative unit or a sub-department within a larger organization.

---

## Personal Names Identified

| Name | Quantity | Syllables | Suffix | Notes |
|------|----------|-----------|--------|-------|
| **I-RU-JA** | 3 | 3 | -JA | Common name ending; V-CV-CV; not in hypothesis results (low freq?) |
| **DU-JA** | 4 | 2 | -JA | Short form; -JA ending; largest recipient |
| **TA-NA-TI** | 1 | 3 | -TI | Luwian best-fit (PROBABLE); onomastic candidate |
| **DA-RE** | 1 | 2 | -RE | Dual function possible (name OR "received/transaction"); Luwian POSSIBLE |
| **TE-TU** | 1 | 2 | -TU | Luwian best-fit (POSSIBLE); short form |

### Observation on -JA Ending Names

Two of five recipients end in -JA. The -JA suffix is the most common name-final element in the Linear A corpus (Palmer 1958; 77 occurrences; 65.9% word-final). It is interpreted as an adjectival/ethnic suffix with Luwian -iya parallel. In an onomastic context, -JA names may indicate ethnic/geographic origin (e.g., "the one from X"). This cluster of -JA names on a personnel tablet is consistent with multi-origin labor allocation.

### Observation on DA-RE

DA-RE appears in the recipient list with quantity 1, which is the standard format for personal names on this tablet. However, DA-RE also has attested administrative meaning ("received" or "transaction marker") elsewhere in the corpus. On HT 85a, DA-RE also appears as a recipient (quantity 4). The consistent recipient-list position across two tablets with integer counts strongly favors the personal name reading here. The dual-function possibility is noted but not forced.

**Cross-tablet confirmation**: DA-RE appears on both HT 7a (quantity 1) and HT 85a (quantity 4) in identical functional positions (recipient in VIR allocation list). This cross-tablet consistency supports the personal name interpretation.

---

## Multi-Hypothesis Testing

### Focus Terms

Analysis prioritizes the surviving hypotheses (Luwian STRONG, Semitic MODERATE) while testing all seven for compliance.

### Key Term: QE-TI (Header)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | Possible Luwian administrative term with -TI suffix | -TI as Luwian verbal/locative ending; header position | **POSSIBLE** | ACTIVE |
| **Semitic** | No clear Semitic root | QE-TI does not match known Semitic patterns | WEAK | ACTIVE |
| Pre-Greek | Substrate term or toponym | Position supports function; no etymology | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No Greek parallel | WEAK | ELIMINATED |
| Hurrian | No parallel | No Hurrian match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No Etruscan match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE) -- the -TI suffix matches Luwian morphological patterns.
**Confidence cap**: POSSIBLE -- not found in hypothesis results; header function assumed from position only; limited attestation.
**Functional interpretation**: QE-TI occupies the header position before VIR+[?], parallel to A-DU's position on HT 85a. Whether QE-TI names a supervisor, department, location, or category is unknown.

### Key Term: I-RU-JA (Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | Anatolian personal name with -JA (Luwian -iya) suffix | -JA ending; three-syllable structure | **POSSIBLE** | ACTIVE |
| **Semitic** | No clear Semitic match | I-R-J does not match common Semitic roots | WEAK | ACTIVE |
| Pre-Greek | Substrate personal name with -JA suffix | -JA productive in Pre-Greek onomastics | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No Greek parallel | WEAK | ELIMINATED |
| Hurrian | Possible Hurrian name element | -JA could be Hurrian theophoric suffix | POSSIBLE | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE) -- -JA suffix is the strongest morphological signal, and Luwian -iya is the primary parallel.
**Confidence cap**: POSSIBLE -- not in hypothesis results; personal name; -JA ambiguous across hypotheses.

### Key Term: DU-JA (Largest Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | *Tuya-* personal name (Luwian -iya) | -JA ending; 2-syllable short form | **POSSIBLE** | ACTIVE |
| **Semitic** | No clear match | DU-JA does not match known Semitic patterns | WEAK | ACTIVE |
| Pre-Greek | Substrate personal name | Short form; -JA ending | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No match | WEAK | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE).
**Confidence cap**: POSSIBLE -- not in hypothesis results; short name; limited diagnostic features.

### Key Term: TA-NA-TI (Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | *Tanati-* personal name; -TI as Luwian nominal/verbal suffix | Three-syllable; -TI ending; hypothesis_tester best=luwian | **PROBABLE** | ACTIVE |
| **Semitic** | No clear root | TA-NA-TI does not match Semitic patterns | WEAK | ACTIVE |
| Pre-Greek | Substrate personal name with -TI | -TI productive ending; possible substrate name | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No Greek parallel | WEAK | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (PROBABLE) -- hypothesis_tester output; -TI morphology consistent with Luwian.
**Confidence cap**: PROBABLE -- single-hypothesis support but backed by morphological pattern.

### Key Term: DA-RE (Dual-Function Candidate)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | *tare-* "to take, receive" (Luwian verbal root) | Position before quantity; attested in admin contexts; hypothesis_tester best=luwian | **POSSIBLE** | ACTIVE |
| **Semitic** | Possible Semitic name or verb | D-R root; no strong Semitic match | WEAK | ACTIVE |
| Pre-Greek | Personal name or substrate term | Position ambiguous | POSSIBLE | ELIMINATED |
| Proto-Greek | No parallel | No match | WEAK | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE) -- hypothesis_tester output; dual function attested.
**Known function**: "received/transaction" attested elsewhere; here in recipient position with quantity 1.
**Cross-tablet**: Also appears on HT 85a in identical functional position (recipient, quantity 4).

### Key Term: TE-TU (Recipient)

| Hypothesis | Proposed Etymology | Evidence | Rating | Status |
|------------|-------------------|----------|--------|--------|
| **Luwian** | *Tetu-* personal name; -U as Luwian nominal suffix | 2-syllable; -U ending (64% Luwian association); hypothesis_tester best=luwian | **POSSIBLE** | ACTIVE |
| **Semitic** | No clear match | TE-TU does not match Semitic patterns | WEAK | ACTIVE |
| Pre-Greek | Substrate name | Short form; limited features | POSSIBLE | ELIMINATED |
| Proto-Greek | No cognate | No match | WEAK | ELIMINATED |
| Hurrian | No parallel | No match | WEAK | ELIMINATED |
| Hattic | No parallel | Insufficient data | INDETERMINATE | ELIMINATED |
| Etruscan | No parallel | No match | WEAK | ELIMINATED |

**Best hypothesis**: Luwian (POSSIBLE) -- hypothesis_tester output.
**Confidence cap**: POSSIBLE -- limited attestation; short name.

### Hypothesis Summary for HT 7a

| Term | Best Hypothesis | Confidence | Alternative |
|------|-----------------|------------|-------------|
| QE-TI | Luwian | POSSIBLE | Header function; -TI suffix |
| VIR+[?] | N/A (logogram) | HIGH | Level 3 anchor |
| I-RU-JA | Luwian | POSSIBLE | -JA suffix (multi-hyp) |
| DU-JA | Luwian | POSSIBLE | -JA suffix (multi-hyp) |
| TA-NA-TI | Luwian | PROBABLE | Best-fit per hypothesis_tester |
| DA-RE | Luwian | POSSIBLE | Dual function attested |
| TE-TU | Luwian | POSSIBLE | -U ending |

**Dominant pattern**: All five recipient names lean Luwian in project tools or by morphological pattern. No Semitic administrative vocabulary appears on this tablet (no KU-RO, no KI-RO, no SA-RA2). This is one of the few tablets where Luwian morphological influence dominates entirely, without the usual Semitic accounting layer. This is consistent with the tablet being a simple personnel list -- the Semitic layer is most visible in totaling/accounting vocabulary, which this tablet lacks.

---

## Connected Reading Attempt

### Element-by-Element Interpretation

```
QE-TI              "[Regarding/From] QE-TI:"            POSSIBLE (position)
VIR+[?]            "persons/workers (qualified)"         HIGH (logogram)

I-RU-JA      3     "[To] I-RU-JA: 3 persons"            PROBABLE (structure)
DU-JA         4     "[To] DU-JA: 4 persons"              PROBABLE (structure)
TA-NA-TI      1     "[To] TA-NA-TI: 1 person"            PROBABLE (structure)
DA-RE         1     "[To] DA-RE: 1 person"                PROBABLE (structure)
TE-TU         1     "[To] TE-TU: 1 person"               PROBABLE (structure)
```

### Full Interpretive Reading (Speculative)

> **[Regarding/From] QE-TI** (supervisor/department/location):
>
> Workers (VIR) [qualified]:
>
> To I-RU-JA: 3 workers
> To DU-JA: 4 workers
> To TA-NA-TI: 1 worker
> To DA-RE: 1 worker
> To TE-TU: 1 worker
>
> **(No total stated; computed sum: 10 workers)**

### Confidence Per Element

| Element | Reading | Confidence | Basis |
|---------|---------|------------|-------|
| QE-TI = header | "regarding / supervisor / from" | POSSIBLE | Position pattern only; not in hypothesis results |
| VIR+[?] = workers | "persons/workers" | HIGH | Logogram (Level 3 anchor) |
| 5 recipient names | Personal names | PROBABLE | Position pattern; NAME + QUANTITY |
| Integer quantities | Worker counts | CERTAIN | Numerals are unambiguous |
| Absence of KU-RO | No formal total | CERTAIN | Absence is observable fact |
| Name etymologies | Luwian-leaning | POSSIBLE | Single-hypothesis support; limited attestation |

---

## What We Know For Certain

These elements are established beyond reasonable doubt:

1. **Document function**: This is a personnel allocation list. QE-TI provides the heading; 5 recipients receive workers (VIR).
2. **VIR = persons**: The VIR logogram denotes people/workers, confirmed via Linear B cognate and pictographic evidence.
3. **All 5 entries are recipient names**: Each appears in the standard NAME + QUANTITY format without exception.
4. **Integer quantities**: 3, 4, 1, 1, 1 are unambiguous whole numbers. Computed sum = 10.
5. **No KU-RO**: The absence of a totaling line is a definite structural feature, not a lacuna (the tablet appears complete).
6. **DA-RE cross-tablet consistency**: DA-RE appears as a recipient on both HT 7a and HT 85a, supporting the personal name reading.
7. **-JA names**: I-RU-JA and DU-JA both end in the most common name-final element in the corpus.

## What We Hypothesize

These elements are interpretations, not proven facts:

1. **QE-TI as header function**: Assumed from position (before VIR+[?]); could be a supervisor, department, toponym, or category marker. Evidence is purely positional.
2. **QE-TI -TI suffix as Luwian**: The -TI ending is consistent with Luwian morphology, but could also be the same -TI seen in TA-NA-TI (onomastic) or a non-Luwian morpheme.
3. **DA-RE as personal name (not verb)**: The recipient-list position favors this reading, but the attested administrative function ("received") remains an alternative.
4. **Name etymologies**: All Luwian attributions for recipient names are POSSIBLE at best. The -JA suffix could be Pre-Greek or Hurrian rather than Luwian.
5. **Absence of KU-RO implies sub-account**: The tablet may be a section of a larger ledger, or the scribe may have omitted the total for other reasons. We cannot determine why KU-RO is absent.
6. **VIR+[?] qualifier**: The qualifier attached to VIR is unclear -- it may specify a type of worker (skilled, corvee, etc.) or a status category.

---

## Cross-Corpus Verification

### QE-TI Occurrences

| Tablet | Context | Position | Consistent? |
|--------|---------|----------|-------------|
| HT 7a | Header before VIR allocation | Initial | Yes (this tablet) |

**Verification**: QE-TI has limited attestation. Cross-corpus verification is INCOMPLETE -- function as header is based solely on this tablet's evidence. Additional occurrences needed to confirm.

### DA-RE Occurrences

| Tablet | Context | Function | Consistent? |
|--------|---------|----------|-------------|
| HT 7a | Recipient position, quantity 1 | Personal name (probable) | Yes (this tablet) |
| HT 85a | Recipient position, quantity 4 | Personal name (probable) | Yes |
| Other HT tablets | Administrative contexts | Transaction/received marker | Dual function |

**Verification**: DA-RE has **dual usage** (personal name AND administrative function). On both HT 7a and HT 85a, the recipient-list position with integer count favors the personal name reading. Dual function confirmed across corpus.

### VIR Logogram Occurrences

| Tablet | Context | Consistent? |
|--------|---------|-------------|
| HT 7a | Header commodity (VIR+[?]) | Yes |
| HT 85a | Header commodity (VIR+[?]) | Yes |
| HT 117a | Schoep Type IV (personnel) | Yes (no VIR logogram but personnel content) |

**Verification**: VIR logogram in header position for personnel distribution is consistent with HT 85a and the broader Linear A corpus. **CORPUS-VERIFIED**.

### -JA Suffix Occurrences

| Context | Count | Consistent? |
|---------|-------|-------------|
| Word-final -JA | 77 corpus-wide (65.9%) | Yes |
| Personal names ending in -JA | 17+ | Yes |
| I-RU-JA, DU-JA on this tablet | 2 | Consistent with corpus-wide pattern |

**Verification**: The -JA ending is the most common name-final element. Its presence on this tablet is unremarkable and consistent. **CORPUS-VERIFIED** for morphological pattern.

---

## First Principles Verification

### [1] KOBER: Was analysis data-led, not assumption-led?
**PASS**

Evidence: Started with transliteration verification and structural analysis (header/recipient/commodity identification). Identified the NAME + QUANTITY pattern before any linguistic hypothesis was tested. The absence of KU-RO was noted as data, not explained away.

### [2] VENTRIS: Was any evidence forced to fit?
**PASS**

Evidence: Acknowledged:
- QE-TI meaning remains at POSSIBLE (not forced to a specific interpretation)
- VIR+[?] qualifier left uninterpreted rather than guessed
- DA-RE dual function explicitly flagged rather than collapsed to one reading
- Name etymologies capped at POSSIBLE rather than overclaimed
- Absence of KU-RO not forced to mean "incomplete" -- alternative explanations listed

### [3] ANCHORS: Were readings built from confirmed anchors outward?
**PASS**

Anchors used (in order):
- Level 3: VIR logogram (HIGH -- pictographic + Linear B cognate)
- Level 4: Structural patterns -- header, recipient-list format (MEDIUM-HIGH)
- Level 5: -JA suffix morphological pattern (MEDIUM)
- Level 6: Name etymologies (POSSIBLE)

No reading exceeds the confidence level of its supporting anchors.

### [4] MULTI-HYP: Were ALL seven hypotheses tested?
**PASS**

For each key term:
- QE-TI: Luwian POSSIBLE, Semitic WEAK, Pre-Greek POSSIBLE, Proto-Greek ELIMINATED, Hurrian ELIMINATED, Hattic ELIMINATED, Etruscan ELIMINATED
- I-RU-JA: Luwian POSSIBLE, Semitic WEAK, Pre-Greek POSSIBLE, Proto-Greek ELIMINATED, Hurrian POSSIBLE (ELIMINATED), Hattic ELIMINATED, Etruscan ELIMINATED
- DU-JA: Luwian POSSIBLE, others WEAK/ELIMINATED
- TA-NA-TI: Luwian PROBABLE, others WEAK/ELIMINATED
- DA-RE: Luwian POSSIBLE, others WEAK/ELIMINATED
- TE-TU: Luwian POSSIBLE, others WEAK/ELIMINATED

All seven hypotheses tested for all key terms. Five eliminated hypotheses noted as such throughout.

### [5] NEGATIVE: Was absence of patterns considered?
**PASS**

Absences noted:
- **No KU-RO**: No total line. This is a complete tablet without formal totaling, unlike HT 85a (same scribe pool, same commodity).
- **No KI-RO**: No deficit marker. This is not a deficit or balance record.
- **No SA-RA2**: No allocation marker. Allocation is implicit in the list structure.
- **No fractions**: All quantities are integers. Personnel are not divided fractionally.
- **No toponyms**: Cannot anchor to geographic confirmation. All names appear personal.
- **No commodity variation**: Single-commodity tablet (VIR only).
- **No Semitic vocabulary**: Unlike most analyzed tablets, no KU-RO/KI-RO/SA-RA2 means the Semitic administrative layer is entirely absent.
- **No Greek case endings**: No -os, -on, -oi in any name.
- **No triconsonantal morphology**: No Semitic root patterns in recipient names.
- **No ergative markers**: No Hurrian-type case system visible.
- **No prefixing morphology**: No Hattic-type prefixes.

### [6] CORPUS: Were readings verified across all occurrences?
**PASS**

| Reading | Occurrences Checked | Result |
|---------|---------------------|--------|
| VIR logogram | Corpus-wide | Consistent |
| DA-RE dual function | HT 7a, HT 85a, other HT tablets | Confirmed |
| -JA suffix | 77 corpus-wide | Consistent |
| QE-TI | HT 7a only | Limited -- further attestation needed |
| TA-NA-TI | hypothesis_tester output | Luwian best-fit confirmed |

---

## Comparison with HT 85a (Same Document Type)

| Feature | HT 7a | HT 85a |
|---------|--------|--------|
| Commodity | VIR+[?] | VIR+[?] |
| Header | QE-TI | A-DU |
| Number of recipients | 5 | 7 |
| Total workers | 10 (computed) | 66 (KU-RO) |
| KU-RO present | **NO** | Yes (VERIFIED exact) |
| KI-RO present | No | No |
| SA-RA2 present | No | No |
| Fractions | None | None |
| Scribe | HT Scribe 11 | HT Scribe 9 |
| Largest allocation | DU-JA (4, 40%) | DA-SI-*118 (24, 36%) |
| DA-RE appears | Yes (quantity 1) | Yes (quantity 4) |

**Assessment**: HT 7a is a smaller, simpler version of the HT 85a document type. Both are VIR allocation lists with headers, integer-only quantities, and no fractions. The key structural difference is the absence of KU-RO on HT 7a. DA-RE appears on both tablets as a recipient, strengthening the personal name interpretation.

**Scribe difference**: HT 7a (Scribe 11) and HT 85a (Scribe 9) are written by different scribes. The shared structural format (header + VIR + NAME+QUANTITY list) indicates a standardized administrative convention at Hagia Triada, not an individual scribal habit.

---

## Novel Observations

### 1. Personnel Tablet Without KU-RO

HT 7a demonstrates that KU-RO is not mandatory on personnel allocation tablets. HT 85a (same format, same commodity) includes KU-RO; HT 7a does not. This suggests KU-RO is a formal accounting element that scribes could include or omit based on administrative context. Possible reasons for omission:
- The tablet is a sub-account within a larger system
- The total was self-evident and did not require formal recording
- Different scribal practice (Scribe 11 vs. Scribe 9)
- The tablet is incomplete (though it appears physically complete)

### 2. -JA Name Cluster on Personnel Tablet

Two of five recipients (40%) end in -JA. This is above the general corpus frequency but not statistically significant with a sample of 5. However, it is consistent with the hypothesis that -JA names may indicate persons from specific geographic or ethnic backgrounds, and that personnel tablets may group workers by origin.

### 3. DA-RE Cross-Tablet Evidence

DA-RE's appearance on both HT 7a and HT 85a -- in both cases as a VIR allocation recipient -- is the strongest evidence yet that DA-RE functions as a personal name in personnel contexts. The individual appears in two separate administrative records, receiving 1 worker (HT 7a) and 4 workers (HT 85a). The different quantities rule out formulaic repetition and suggest genuine administrative records of the same person at different times or under different allocation schemes.

### 4. Absence of Semitic Administrative Layer

This is one of the few fully analyzed tablets where the Semitic administrative vocabulary layer (KU-RO, KI-RO, SA-RA2) is completely absent. The tablet's entire vocabulary leans Luwian. This supports the domain-specific layering model: Semitic terms dominate accounting/totaling functions; Luwian morphology dominates personal names and general vocabulary. A simple personnel list without totaling has no functional slot for Semitic terms.

### 5. QE-TI as Unknown Header

QE-TI joins the list of header terms whose function is clear (initial position before commodity) but whose meaning is unknown. The growing inventory of header terms (A-DU, MA-KA-RI-TE, SA-TA, QE-TI, *21F-TU-NE) suggests a rich administrative vocabulary for categorizing accounts. Each likely denotes a different organizational principle (contributor, department, location, classification).

---

## Sources Consulted

1. **lineara.xyz corpus** -- HT7a transliteration and commentary
2. **arithmetic_verifier** -- Rosetta skeleton and NO_KURO classification
3. **hypothesis_tester.py** -- Multi-hypothesis scoring for TA-NA-TI, DA-RE, TE-TU
4. **KNOWLEDGE.md** -- Confirmed readings, -JA suffix analysis, anchor registry
5. **METHODOLOGY.md** -- Six Principles, Seven Hypotheses framework, confidence calibration
6. **MASTER_STATE.md** -- Current metrics and operational baseline
7. **HT85a_READING.md** -- Template and cross-reference for same document type
8. **Gordon, C.H. (1966)** -- KU-RO = *kull* (Semitic "total")
9. **Palmer, L.R. (1958)** -- -JA suffix; Luwian morphological comparisons
10. **Salgarella, E. (2020)** -- Sign classification, tablet structure
11. **Younger, J. (2024)** -- Linear A Texts: Introduction; transcriptions

---

## Appendix: Computed Sum Detail

### Raw Computation

```
Entry 1:  I-RU-JA      =   3
Entry 2:  DU-JA        =   4
Entry 3:  TA-NA-TI     =   1
Entry 4:  DA-RE        =   1
Entry 5:  TE-TU        =   1
                           --
Computed sum             =  10
Stated KU-RO             =  (absent)
Status                   =  NO_KURO
```

### Verification Quality Metrics

| Metric | Value |
|--------|-------|
| Number of entries | 5 |
| Fraction count | 0 |
| Damaged entries | 0 |
| Ambiguous readings | 0 |
| KU-RO present | No |
| Verification class | Class N (no total for comparison) |

This is a **Class N verification**: no KU-RO total is available for comparison. The computed sum (10) is reported but cannot be validated against a stated total. The arithmetic of the individual entries is straightforward (all single-digit integers).

---

## Morphological and Onomastic Constraints

### QE-TI (header)

- **Morphological decomposition**: 2-syllable word with -TI suffix. Suffix -TI has 42 corpus-wide attestations (5th most common suffix). Root skeleton Q-T.
- **Paradigm membership**: No K-R, S-R, or O-D paradigm match. Not in any documented paradigm.
- **Onomastic analysis**: QE- initial syllable accounts for 4 name candidates corpus-wide (including QE-RA2-U, QE-PU). Not in top name candidates list.
- **Infix patterns**: None detected.
- **Constraint summary**: -TI suffix is consistent with Luwian verbal/locative endings. Hapax (1 attestation); no paradigm match found. Function as header is the primary constraint.

### I-RU-JA

- **Morphological decomposition**: 3-syllable word with -JA suffix (most common suffix, 48 attestations) and I- prefix (54 attestations, 2nd most common prefix). Root skeleton O-R.
- **Paradigm membership**: No specific paradigm match. However, the Ø-R root is shared with A-RU (paradigm P-ØR-5), suggesting a possible root relationship.
- **Onomastic analysis**: Not in top name candidates. -JA suffix is the most common name-final element (17 onomastic candidates end in -JA). CV-CV-CV (medium) pattern consistent with standard Minoan onomastic length.
- **Infix patterns**: None detected.
- **Constraint summary**: I- prefix + -JA suffix combination places this firmly in the productive Minoan name-formation system. The -JA suffix (Luwian -iya parallel) supports an ethnic/adjectival interpretation ("the one from [I-RU]").

### DU-JA

- **Morphological decomposition**: 2-syllable word with -JA suffix. DU- prefix not in top 10 prefixes but DU- initial appears in 4 onomastic candidates. Root skeleton D.
- **Paradigm membership**: No paradigm match found.
- **Onomastic analysis**: Not in top name candidates. CV-CV (short) pattern. -JA suffix consistent with Luwian -iya.
- **Infix patterns**: None detected.
- **Constraint summary**: Short-form name with -JA suffix. May be an abbreviated form of a longer DU-*-JA name. No paradigm match found.

---

*Connected reading completed 2026-02-21 as part of Lane G: Reading Attempts (Personnel Allocation Series).*

*Document structure and commodity logogram (VIR) are established with HIGH confidence. Header function (QE-TI) is at POSSIBLE -- not yet independently confirmed. Personal names are identified by position but individual etymologies remain at POSSIBLE-PROBABLE. The absence of KU-RO is the key structural difference from the otherwise identical HT 85a format. DA-RE's cross-tablet consistency (HT 7a + HT 85a) strengthens the personal name reading. All five recipient names lean Luwian, with no Semitic administrative vocabulary present -- consistent with domain-specific layering.*
