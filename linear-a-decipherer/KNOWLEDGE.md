# Current State of Knowledge

**Essential lookup tables and project status for Linear A research**

**Last Updated**: 2026-02-01

---

## Quick Status

| Metric | Value |
|--------|-------|
| Corpus Processed | 1,722 inscriptions (100%) |
| Words Tested | 198 words (freq >= 2) via hypothesis_tester.py |
| High-Confidence Words | 86 (CERTAIN or PROBABLE) |
| KU-RO Totals Verified | 4/35 (11.4%) via corpus_auditor.py |
| Personal Names | 127 identified |
| Best-Fit Model | **Undetermined substrate** with contact features (Luwian morphological influence + Semitic admin loans) |
| Active Vectors | 5 (OPERATION BREAKTHROUGH) |

**Tool Validation**: 2026-02-01 - All analyses re-run with proper tooling

**See**: `CHANGELOG.md` for full discovery chronology

---

## Confirmed Readings

### Level 1: CERTAIN (Toponyms)

| Word | Meaning | Occurrences | Evidence |
|------|---------|-------------|----------|
| **pa-i-to** | Phaistos | 12 | Geographic + Linear B cognate |
| **ku-do-ni-ja** | Kydonia (Chania) | 8 | Geographic + Linear B cognate |

### Level 2: HIGH (Linear B Cognates + Position)

| Word | Meaning | Occurrences | Evidence | First Proposed |
|------|---------|-------------|----------|----------------|
| **ku-ro** | total/sum | 39 | List-final; sums verified mathematically | Gordon (1966) |
| **ki-ro** | deficit/category marker | 17 | Multi-function: deficit OR header | Gordon (1966) |
| **MA-RU (A 559)** | wool (*maru*) | — | Complex sign; Linear B *145/LANA retained from Minoan; Greek μαλλός /mallós/ "wool/fleece" | Salgarella (2020) |
| **-JA suffix** | adjectival/ethnic | 77 | Word-final 65.9%; Luwian -iya parallel | Palmer (1958) |
| **DA-MA-TE** | Demeter (deity) | 1 | Linear B cognate *da-ma-te*; peak sanctuary | — |
| **A-TA-NA** | Athena (deity) | 2 | Linear B cognate *a-ta-na* | — |
| **A-TA-NA-TE** | Athena derivative | 2 | -TE suffix on A-TA-NA | — |

### Level 3: HIGH (Logograms)

| Logogram | Meaning | Evidence |
|----------|---------|----------|
| GRA, VIN, OLE, OLIV, FIC | Commodities | Pictographic + Linear B |
| OVI, CAP, SUS, BOS, VIR | Animals/Personnel | Pictographic + Linear B |
| TELA, CYP | Materials | Linear B + context |

#### OLE Variant Codes (GORILA Classification)

| Logogram | Code | Likely Meaning |
|----------|------|----------------|
| OLE+U | *610 | Oil variant (most common) |
| OLE+KI | *618 | Oil variant |
| OLE+MI | *622 | Oil variant |
| OLE+TU | *621 | Oil variant |
| OLE+DI | *608 | Oil variant |

**Source**: Salgarella (2020), citing GORILA classification

### Level 4-5: PROBABLE

| Word | Meaning | Confidence | Best Hypothesis | First Proposed |
|------|---------|------------|-----------------|----------------|
| **SA-RA₂** | allocation (*šarāku*) | PROBABLE | Akkadian | This project |
| **A-DU** | administrative term | PROBABLE | Semitic | Multiple |
| **U-MI-NA-SI** | debt / '[s/he] owes' | POSSIBLE | Unknown | Younger (2024) |
| **PO-TO-KU-RO** | grand total | PROBABLE | Multi-hypothesis | Extends Gordon |
| **JA-SA-SA-RA-ME** | divine name | PROBABLE | Pre-Greek | This project |
| **SU-PU** | bowl (*suppu*) | PROBABLE | Akkadian | This project |
| **KA-RO-PA₃** | vessel (*karpu*) | PROBABLE | Akkadian | This project |
| **-TE/-TI** | verbal endings | POSSIBLE | Luwian | Palmer (1958) |
| **-U** | noun class marker | PROBABLE | Luwian (64%) | This project |

### K-R Paradigm (3-Tier Accounting)

| Word | Meaning | Occurrences | Regional Scope |
|------|---------|-------------|----------------|
| PO-TO-KU-RO | Grand total | 5 | HT-only |
| KU-RO | Section total | 37 | Cross-site (HT, ZA, PH) |
| KU-RE | Subtotal | 2 | HT-only |
| KI-RO | Deficit/owed | 16 | **HT-EXCLUSIVE** |

### Transaction Terms (Administrative Vocabulary)

| Term | Proposed Meaning | Confidence | Source |
|------|------------------|------------|--------|
| KU-RO | total/sum | HIGH | Gordon (1966) |
| KI-RO | deficit/category | HIGH | Gordon (1966) |
| SA-RA₂ | allocation (*šarāku*) | PROBABLE | This project |
| U-MI-NA-SI | debt / '[s/he] owes' | POSSIBLE | Younger (2024) |
| A-DU | administrative term | PROBABLE | Multiple |

---

## Hypothesis Scorecard

### Tool-Validated Results (2026-02-01)

**Method**: `hypothesis_tester.py` on 198 words (freq >= 2), 1,722 inscriptions

| Hypothesis | Support % | Words | Rank | Key Proponents |
|------------|-----------|-------|------|----------------|
| **Luwian/Anatolian** | **30.3%** | 60 | **1** | Palmer (1958), Finkelberg (1998) |
| Semitic (loans) | 17.7% | 35 | 2 | Gordon (1966), Best (1972) |
| Proto-Greek | 2.5% | 5 | 3 | Georgiev (1963), Mosenkis (2019) |
| Pre-Greek Substrate | 1.5% | 3 | 4 | Beekes (2014), Furnée (1972) |

**Critical Findings**:
1. **Luwian DOMINANT** (30.3%) - morphological particles (-JA, WA, U) more pervasive than recognized
2. **Proto-Greek ELIMINATED** (2.5% support; only 5 words) - phonological incompatibility confirmed
3. **Pre-Greek low** - may reflect detection limitations rather than actual absence

### Legacy Scores (Manual Analysis)

| Hypothesis | Score | Notes |
|------------|-------|-------|
| Semitic | +61.4 | Administrative vocabulary strong |
| Luwian | +50.0 | Morphological particles dominant |
| Pre-Greek | +34.5 | Substrate in toponyms, divine names |
| Proto-Greek | -2.75 | ELIMINATED |

**Proto-Greek evidence against**: /o/ frequency 2.9% (expected ~20%); no Greek case endings; 123 unique signs dropped when Greeks adapted script; tool validation shows only 2.5% word-level support.

---

## Regional Administrative Systems

```
                    CRETE
    ┌─────────────────────────────────────────┐
    │    KH (Khania) - 227 inscriptions       │
    │    ZERO K-R vocabulary; CYP dominant    │
    │                                         │
    │    HT (Hagia Triada) - 1,092 inscriptions │
    │    KU-RO/KI-RO/SA-RA₂ ACCOUNTING CENTER  │
    │                                         │
    │    ZA (Zakros) - 31 tablets             │
    │    KU-RO present; KI-RO/SA-RA₂ absent   │
    │                                         │
    │    PH (Phaistos) - 66 inscriptions      │
    │    KU-RO in MMIII = EARLIEST K-R        │
    └─────────────────────────────────────────┘
```

**Key finding**: HT vocabulary (KU-RO/KI-RO/SA-RA₂) is a specialized palatial system, NOT universal Minoan.

---

## Analysis Registry

### Inscriptions Fully Analyzed

| ID | Site | Confidence | Key Finding |
|----|------|------------|-------------|
| HT 13 | Hagia Triada | HIGH | ku-ro = total; wine distribution |
| HT 28 | Hagia Triada | HIGH | 5 oil types (*608-*622); SA-RA₂; JA-QI recurrent; U-MI-NA-SI |
| HT 31 | Hagia Triada | POSSIBLE | Vessel inventory; Semitic vocabulary |
| TY 3a | Tylissos | HIGH | 8 oil types; Semitic/Luwian mixed |
| ZA 4, ZA 15 | Zakros | HIGH | KU-RO cross-site verified |
| KH 5, KH 88 | Khania | MEDIUM | Zero K-R; CYP+E copper grades |
| KN Zf 2 | Knossos | MEDIUM | 119 signs; longest inscription |
| PH(?)31a | Phaistos | HIGH | KU-RO in MMIII (earliest) |
| HT 117 | Hagia Triada | HIGH | KI-RO header function; KU-RO 10 verified |
| HT 94 | Hagia Triada | HIGH | KU-RO+KI-RO co-occur; SA-RA₂ commodities |

### Recurrent Personal Names (Cross-Tablet)

| Name | Tablets | Interpretation |
|------|---------|----------------|
| JA-QI | HT 28a, HT 28b | Appears on both sides; official or recipient |
| KU-PA₃-NU | PH, HT | Cross-site attestation |

**Note**: See `data/personal_names_comprehensive.json` for full list of 127 identified names

### Major Thematic Investigations

| Topic | Status | Key Finding |
|-------|--------|-------------|
| K-R Paradigm | Complete | U/I vowel polarity = total/deficit |
| SA-RA₂ = *šarāku* | Complete | Akkadian "allocate"; HT-exclusive |
| Libation Formulas | Complete | **6-position structure** (Salgarella 2020); JA-SA-SA-RA-ME divine |
| Khania System | Complete | Parallel copper trade admin; zero K-R |
| Unique Signs | Complete | 123 signs dropped; pharyngeal/palatalized candidates |
| Personal Names | Complete | 127 names; Demeter/Athena Minoan origins |

### Libation Formula Structure (Salgarella Table 5)

| Position | Function | Example |
|----------|----------|---------|
| First | Verb (main) | A-TA-I-*301-WA-JA |
| Second | Place name | DA-MA-TE |
| Third | Dedicant's name | (varies) |
| Fourth | Object | A-SA-SA-RA-ME |
| Fifth | Verb (subordinate) | — |
| Sixth | Prepositional phrase | -TE "from" |

**Note**: Two versions exist — "principal" (6 sequences) and "secondary" (3 sequences). Both share A/JA-SA-SA-RA-ME.

---

## Key Negative Evidence

| Observation | Implication |
|-------------|-------------|
| /o/ frequency 2.9% | Argues against Proto-Greek |
| Zero Greek case endings | Argues against Proto-Greek |
| No Semitic triconsonantal morphology | Semitic = loans, not genetic |
| KU-RO ≠ Linear B *to-so* | Different administrative vocabulary |
| 123 unique signs | More phonemes than Greek |

---

## Unique Sign Analysis: *301

**Status**: Phase B2 COMPLETE (phoneme candidates generated)

| Metric | Value |
|--------|-------|
| Occurrences | 288 |
| Word-initial | 88.2% |
| Standalone + numeral | 82.6% |
| Sites | 10 (HT dominant at 82.6%) |

**Hybrid Sign Model**: *301 functions as BOTH logogram (commodity marker) AND syllabogram

| Rank | Phoneme | IPA | Confidence | Linguistic Source |
|------|---------|-----|------------|-------------------|
| 1 | ḥa | [ħa] | PROBABLE | Semitic pharyngeal |
| 2 | kya | [kʲa] | PROBABLE | Luwian palatalized |
| 3 | ʿa | [ʕa] | POSSIBLE | West Semitic |
| 4 | xa | [xa] | POSSIBLE | Multi-source |

**Key Context**: A-TA-I-*301-WA-JA (libation formula, 11 occurrences)

**Why Dropped in Linear B**: Represented phoneme(s) absent in Greek; logographic function obsolete

---

## Open Questions

### High Priority
1. **Is Semitic layer loanwords or genetic?** Current: Probably loanwords
2. **What language family is substrate?** Current: Unknown (possibly isolate)
3. **Can religious texts provide different vocabulary?** Current: Yes - distinct register

### Medium Priority
4. **Regional scribal traditions?** ANSWERED: HT = hub; KH = parallel system
5. **Vowel ending patterns?** PARTIAL: -U favors Luwian (64%), not Semitic

---

## Corpus Statistics

| Metric | Count |
|--------|-------|
| Total inscriptions | ~1,721 |
| Total signs | ~7,400 |
| Core syllabograms | ~90 |
| Date range | c. 1800-1450 BCE |

### Vowel Frequencies

| Vowel | Frequency | Note |
|-------|-----------|------|
| a | 39.3% | High (Anatolian/Semitic pattern) |
| i | 25.7% | Moderate |
| u | 18.1% | Moderate |
| e | 14.0% | Moderate |
| **o** | **2.9%** | **Low (argues against Greek)** |

---

## Critical Dependencies

If these anchors change, dependent readings must be re-evaluated:

| Reading | Depends On | If Anchor Changes |
|---------|------------|-------------------|
| SA-RA₂ | Semitic loanword layer | Demote to SPECULATIVE |
| KU-RO family | Linear B cognate validity | Demote to POSSIBLE |
| -JA suffix | Luwian morphology layer | Demote to POSSIBLE |
| Vessel vocabulary | Semitic loan layer | Demote if rejected |

---

## Quick Reference: Site Codes

| Code | Site | Key Info |
|------|------|----------|
| HT | Hagia Triada | Largest corpus (147 tablets); K-R vocabulary hub |
| KH | Khania | 99 tablets; copper focus; zero K-R |
| ZA | Zakros | 31 tablets; wine focus; KU-RO present |
| PH | Phaistos | 26 tablets; earliest (MMII-III) |
| KN | Knossos | Includes 2024 scepter (119 signs) |

---

## Related Documents

- **METHODOLOGY.md** - Analysis principles and procedures
- **CHANGELOG.md** - Chronological discovery record
- **LESSONS_LEARNED.md** - Methodology refinements
- **references/** - Sign lists, corpus data, hypotheses frameworks

### Archived Originals (Full Detail)

- `archive/STATE_OF_KNOWLEDGE.md` - Full synthesis with all details
- `archive/CONFIRMED_READINGS.md` - Complete readings with all annotations
- `archive/ANALYSIS_INDEX.md` - Full analysis registry with file links

---

---

## OPERATION BREAKTHROUGH: 5-Vector Synthesis

### Vector 1: Dropped Sign Phonology

**123 unique signs** dropped when Greeks adapted Linear A. Key findings:

| Sign | Occurrences | Position | Phoneme Candidate | Function |
|------|-------------|----------|-------------------|----------|
| *301 | 288 | 88% initial | /ħa/ or /kʲa/ | Hybrid (logogram + syllable) |
| *304 | 42 | 93% initial | Emphatic? | Pure logogram |
| *188 | 32 | 94% initial | Unknown | Vessel-related |
| **\*118** | **26** | **69% FINAL** | Word-final consonant | CVC marker |
| *86 | 24 | 92% initial | Unknown | Khania-dominant |
| *21F/*21M | 30 | 70% initial | — | Gender classifier |

**Key Discovery**: *118's 69% FINAL position proves Linear A had **closed syllables** (CVC structure) — explains why Greeks dropped final consonant signs.

### Vector 2: Libation Formula Structure

6-position religious formula decoded:

| Position | Function | Example |
|----------|----------|---------|
| 1 | Main verb | A-TA-I-*301-WA-JA |
| 2 | Dedicant name | JA-DI-KI-TU |
| 3 | Divine name | JA-SA-SA-RA-ME |
| 4 | Epithet/verb | U-NA-KA-NA-SI |
| 5 | Offering term | I-PI-NA-MA |
| 6 | Prepositional | SI-RU-TE |

**Key Discovery**: Religious vocabulary favors **Luwian/Pre-Greek** (+14.5/+13.0), NOT Semitic (+4.5) — two distinct linguistic layers.

### Vector 3: Khania Inversion

| Feature | Hagia Triada | Khania |
|---------|--------------|--------|
| K-R vocabulary | Full system | **ZERO** |
| Commodity focus | Oil/grain/wine | **Copper (CYP)** |
| CYP grading | — | CYP+D (fractions), CYP+E (integers) |
| Vocabulary overlap | — | 1.8% |

**Key Discovery**: KH operates **PARALLEL** administrative system. CYP+D = lower grade (fractions), CYP+E = higher grade (integers).

### Vector 4: Knossos Scepter

119 signs = 1.6% of corpus. MA-RU precedent validates:
- Ligatured signs spell words phonetically
- Amphora ligatures (PA, RU, RA, I, NE, SE) = content labels
- 6-fraction sequence may calibrate ALL fraction values

**Status**: Awaiting Anetaki II publication for full analysis.

### Vector 5: Chronological Wedge

| Period | K-R Status | Vocabulary Type |
|--------|------------|-----------------|
| **MMII** (1800-1700) | **ZERO** | Pure name lists, Pre-Greek |
| **MMIII** (1700-1600) | **KU-RO only** | Innovation horizon |
| **LMIB** (1500-1450) | **Full system** | Complete K-R |

**Key Discovery**: K-R Innovation Horizon = **MMIII Phaistos** (PH(?)31a). Full system develops over ~200 years.

---

## Key References

| Author | Year | Work | Contribution |
|--------|------|------|--------------|
| Gordon | 1966 | *Evidence for the Minoan Language* | KU-RO = *kull* (Semitic "total") |
| Palmer | 1958 | — | -JA suffix; Luwian morphology |
| Beekes | 2014 | *Pre-Greek* | Substrate phonology |
| Salgarella | 2020 | *Aegean Scripts* | HT 28 structure; 6-position libation formula; MA-RU = wool; sign classification |
| Younger | 2024 | *Linear A Texts: Introduction* | U-MI-NA-SI = 'debt/owes'; transcriptions |

---

*Knowledge base consolidating STATE_OF_KNOWLEDGE.md, CONFIRMED_READINGS.md, and ANALYSIS_INDEX.md*
*Full discovery chronology in CHANGELOG.md*
