# Current State of Knowledge

> **Operational note**: This file is now a reference knowledge base (readings, hypotheses, and supporting tables).
> Canonical current operations and metrics live in `linear-a-decipherer/MASTER_STATE.md`.

**Essential lookup tables and project status for Linear A research**

**Last Updated**: 2026-02-16

> **Refresh policy**: KNOWLEDGE.md updates when readings, hypotheses, or reference tables change.
> MASTER_STATE.md updates for any operational metric or status change (and is canonical when they diverge).

---

## Quick Status

| Metric | Value |
|--------|-------|
| Corpus Processed | 1,721 inscriptions (100%) |
| Detailed Analyses | **300/1,721 inscriptions (17.43% coverage)** |
| Words Tested | **248 words** (freq >= 2) via batch_pipeline.py |
| High-Confidence Words | **42** (CERTAIN/PROBABLE + CONSISTENT via batch_pipeline.py) |
| KU-RO Totals Verified | 7/35 (20%) via corpus_auditor.py |
| Personal Names | 127 identified |
| Best-Fit Model | **Undetermined substrate** with contact features (Luwian morphological influence + Semitic admin loans) |
| Active Operation | **CORPUS EXPANSION — 17% achieved** |

**Corpus Expansion Progress**: 2026-02-05 — 17.43% coverage
- Phase 1: ✅ Site Diversification — KH (9), ZA (28), PH (35) analyzed
- Phase 2: ✅ Hypothesis Validation — 248 words tested, 42 high-confidence
- Phase 3: ✅ Comprehensive Sweep — **17.43% coverage (300/1,721)**
- **21 sites** now represented in batch analysis
- **K-R absent** in 9 analyzed KH inscriptions (sample too small for confirmation)

**Previous 5-Direction Progress** (2026-02-05 — ALL COMPLETE):
- Direction 2: ✅ Phonological Reconstruction — /o/ at 3.92%, 15 CV gaps, *118 CVC confirmed
- Direction 3: ✅ Khania K-R absence — observed in 9 KH inscriptions (requires larger sample)
- Direction 4: ✅ Syntax Analysis — VSO word order suggested (limited evidence)
- Direction 5: ✅ Sign Campaign — 21 K-R forms, 30 paradigm groups, 9 final-preference signs

**See**: `CHANGELOG.md` for full discovery chronology

---

## Confirmed Readings

### Level 1: CERTAIN (Toponyms)

| Word | Meaning | Occurrences | Evidence |
|------|---------|-------------|----------|
| **pa-i-to** | Phaistos | 12 | Geographic + Linear B cognate |
| **ku-do-ni-ja** | Kydonia (Chania) | 8 | Geographic + Linear B cognate |
| **di-ki-te** | Mount Dikte | — | PK Za 11a; Linear B *di-ka-ta-de* |
| **tu-ru-sa** | Tylissos | — | KO Za 1b; Linear B *tu-ri-so* |
| **i-da** | Mount Ida | — | PK Za 18; Linear B *i-da-i-jo* |

**Note**: SE-TO-I-JA (PR Za1.b) proposed as "Arkhanes or Mallia" but location unconfirmed — SPECULATIVE.

### Level 2: HIGH (Linear B Cognates + Position)

| Word | Meaning | Occurrences | Evidence | First Proposed |
|------|---------|-------------|----------|----------------|
| **ku-ro** | total/sum | 39 | List-final; sums verified mathematically | Gordon (1966) |
| **ki-ro** | deficit/category marker | 17 | Multi-function: deficit OR header | Gordon (1966) |
| **MA-RU (A 559)** | wool (*maru*) | — | Complex sign; Linear B *145/LANA retained from Minoan; Greek μαλλός /mallós/ "wool/fleece"; Hesychius glosses Cretan μάλλυκες = τρίχες "hair" | Salgarella (2020) |
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
| **-TE/-TI** | verbal endings OR 'from/of' | POSSIBLE | Luwian (Palmer 1958) OR locative (Valério 2007) | Dual interpretation |
| **-U** | noun class marker | PROBABLE | Luwian (64%) | This project |
| **I-/J- prefix** | 'to' or 'at' | SPECULATIVE | Duhoux 1997 interpretation | Single scholar |
| **-RU/-RE** | = Greek -os? | SPECULATIVE | Steele & Meissner 2017 | See note below |

**Critical Note on -RU/-RE**: If Minoan -RU/-RE corresponds to Greek -os masculine ending (DI-DE-RU → di-de-ro), this implies either genetic relationship or borrowing — which contradicts "isolated language" claims. Treat with caution.

### Level 6: SPECULATIVE (Single Scholar Interpretations)

| Word | Proposed Meaning | Source | Problem |
|------|------------------|--------|---------|
| **NI (AB 30)** | 'fig' (acrophonic of νικύλεον) | Neumann 1958 | Assumes acrophonic principle + Greek etymology. Circular if Minoan is "isolated." |
| **KI-KI-NA** | 'figs of sycamore' | HT 88.2; cf. Greek κεικύνη | Depends on NI = 'fig' being correct. Building speculation on speculation. |

**Methodology Note**: These etymologies use Greek to decode Minoan, then claim Minoan is unrelated to Greek. This internal contradiction should prevent automatic acceptance.

### K-R Paradigm (3-Tier Accounting) — Table updated 2026-02-02

**Note**: paradigm_discoverer.py extracted 9 K-R related forms (64 total occurrences). K-R paradigm was already established; this adds variant forms.

| Word | Meaning | Occurrences | Vowel Pattern | Regional Scope |
|------|---------|-------------|---------------|----------------|
| PO-TO-KU-RO | Grand total | 5 | O-O-U-O | HT-only |
| **KU-RO** | **Section total** | **37** | **U-O** | **Cross-site (HT, ZA, PH)** |
| **KI-RO** | **Deficit/owed** | **16** | **I-O** | **HT-EXCLUSIVE** |
| KU-RE | Subtotal | 2 | U-E | HT-only |
| KA-RU | K-R variant | 2 | A-U | HT |
| KI-RA | K-R variant | 2 | I-A | HT |
| KU-RA | K-R variant | 2 | U-A | HT |
| KI-DA-RO | Extended form | 1 | I-A-O | HT |
| KI-RU | K-R variant | 1 | I-U | HT |

**Vowel Alternation Pattern**:
- Position 0: U/I semantic opposition (total/deficit)
- Position 1: O/E/A possible grammatical function

### S-R Pattern Candidates (2026-02-02)

**Status**: Consonant skeleton extraction; requires validation. 38 total occurrences.

| Word | Meaning | Occurrences | Vowel Pattern | Sites |
|------|---------|-------------|---------------|-------|
| **SA-RA₂** | allocation (*šarāku*) | 20 | A-A | HT |
| SA-RU | S-R variant | 6 | A-U | HT, ZA |
| SA-RO | S-R variant | 4 | A-O | HT |
| SI-RU | S-R variant | 4 | I-U | HT, TY |
| SI-RU-TE | Religious term | 3 | I-U-E | Peak sanctuaries |

**Hypothesis**: If validated, SA-RA₂ may be part of a larger S-R root system with vowel alternation similar to K-R. Requires independent verification.

### Ø-D Pattern Candidates (2026-02-02)

**Status**: Consonant skeleton extraction; requires validation. 20 total occurrences.

| Word | Meaning | Occurrences | Pattern |
|------|---------|-------------|---------|
| **A-DU** | administrative term | 8 | Ø-DU |
| I-DA | Mount Ida/Ø-D variant | 4 | Ø-DA |
| I-DI | Ø-D variant | 3 | Ø-DI |
| O-DA | Ø-D variant | 3 | Ø-DA |
| U-DA | Ø-D variant | 2 | Ø-DA |

**Hypothesis**: If validated, vowel-initial words with D-final syllable may form a paradigm, suggesting vowel-prefix system. Pattern co-occurrence ≠ morphological relationship.

### Transaction Terms (Administrative Vocabulary)

| Term | Proposed Meaning | Confidence | Source |
|------|------------------|------------|--------|
| KU-RO | total/sum | HIGH | Gordon (1966); HT 9a.6, 9b.6 |
| KI-RO | deficit/category | HIGH | Gordon (1966); HT 123a.9 |
| PO-TO-KU-RO | grand total | PROBABLE | HT 122b.6 |
| KU-RA | total (variant?) | POSSIBLE | ZA 20.4 — needs verification |
| DA-I | total (alternative?) | POSSIBLE | HT 12.6 — needs verification |
| SA-RA₂ | allocation (*šarāku*) | PROBABLE | This project |
| U-MI-NA-SI | debt / '[s/he] owes' | POSSIBLE | Younger (2024); HT 28b.1-2 |
| A-DU | administrative term | PROBABLE | HT 95b.1; compounds: A-DU-RE-ZA, A-DU-KU-MI-NA |
| KA-I-RO | balance? | SPECULATIVE | ZA 8.6 — single scholar interpretation |
| KI-RA | balance? | SPECULATIVE | HT 103.5 — single scholar interpretation |

**Caution**: KU-RA, DA-I, KA-I-RO, KI-RA are proposed by Schoep 2002 / Younger 2024 but have limited attestation. "Balance" meanings especially speculative.

---

## Hypothesis Scorecard

### Bayesian Results (2026-02-02)

**Method**: `bayesian_hypothesis_tester.py` on 160 words (freq >= 2), Bayesian inference with calibrated priors

| Hypothesis | Mean Posterior | Prior | Shift | Words Best | Verdict |
|------------|----------------|-------|-------|------------|---------|
| **Luwian/Anatolian** | **35.1%** | 25% | **+10.1%** | **87** | **DOMINANT** |
| Isolate (null) | 32.8% | 35% | -2.2% | 73 | Active null |
| Semitic (loans) | 15.8% | 15% | +0.8% | 0 | LOANS |
| Pre-Greek Substrate | 13.5% | 20% | -6.5% | 0 | SUBSTRATE |
| **Proto-Greek** | **2.8%** | 5% | **-2.2%** | **0** | **ELIMINATED** |

**95% Credible Intervals**:
- Luwian: [14.2%, 42.9%]
- Proto-Greek: [2.4%, 7.8%] (below 5% threshold; confirms 2026-02-01 elimination)

### Negative Evidence Summary (2026-02-02)

| Hypothesis | Score | Critical Absences |
|------------|-------|-------------------|
| **Proto-Greek** | **-15.0** | /o/ at 3.9% (expected 20%); Greek case endings absent |
| Luwian | +3.5 | None critical |
| Semitic | 0.0 | Triconsonantal morphology absent |
| Pre-Greek | 0.0 | Methodology limitations (no Level 1/2 anchors; phonological matching only) |

### Legacy Results (Validated 2026-02-09)

**Method**: `hypothesis_tester.py` on 198 words (freq >= 2), 1,721 inscriptions
**Validated**: Full re-run after K-R double-matching fix, Pre-Greek expansion, frequency gating

| Hypothesis | Support % | Words | Rank |
|------------|-----------|-------|------|
| **Luwian/Anatolian** | **30.3%** | 60 | **1** |
| Semitic (loans) | 17.7% | 35 | 2 |
| Proto-Greek | 2.5% | 5 | 3 |
| Pre-Greek Substrate | 2.0% | 4 | 4 |

**Critical Findings**:
1. **Luwian DOMINANT** (35.1% Bayesian posterior) - morphological particles (-JA, WA, U) more pervasive than recognized
2. **Proto-Greek ELIMINATED** (2.8% posterior, max 6.4%) - below 5% falsification threshold
3. **Domain-specific layering**: Admin vocabulary favors Semitic; overall corpus favors Luwian
4. **Pre-Greek expanded** (2.0%, up from 1.5%) - marker/vocabulary expansion detected 1 additional word
5. **Confidence recalibration** (2026-02-09): 10 words demoted CERTAIN→PROBABLE after K-R fix + frequency gating

**Note on Scoring Methods**: Bayesian posterior (35.1% Luwian) and batch_pipeline raw scores (Semitic 687.7 vs Luwian 278.5) are NOT directly comparable. Bayesian uses calibrated priors and word-count support; batch_pipeline sums per-word evidence scores where Semitic tests have higher maximum scores per word. Both confirm the domain-specific layering pattern. Batch scores validated 2026-02-09 after K-R fix; unchanged from pre-fix (fix affected per-word scores but not tier classifications).

### Untested Hypotheses (Proposed in Literature)

| Hypothesis | Proponents | Status | Why Not Prioritized |
|------------|------------|--------|---------------------|
| **Hurrian** | Monti 2002, 2005, 2006; van Soesbergen 2017 | NOT TESTED | Methodological criticisms; Hurrian corpus limited |
| **Etruscan** | Facchetti 2001; Facchetti & Negri 2003 | NOT TESTED | Facchetti has retreated from strong claims; Etruscan itself poorly understood |
| **Hattic/Hatto-Sumerian** | Schrijver 2018 | NOT TESTED | Highly speculative; Hattic corpus too small for comparison |

**Methodological Note**: The "isolated language" designation (Davis 2014) is essentially an admission that affiliation cannot be determined — NOT a positive finding that Minoan has no relatives. Our multi-hypothesis testing with percentages is more epistemically honest than declaring isolation.

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
                    CRETE (17.43% Batch Coverage)
    ┌─────────────────────────────────────────┐
    │    KH (Khania) - 227 inscriptions       │
    │    BATCH ANALYZED: 9 (4.0%)             │
    │    K-R absent in sample; CYP dominant   │
    │                                         │
    │    HT (Hagia Triada) - 1,110 inscriptions│
    │    BATCH ANALYZED: 172 (15.5%)          │
    │    KU-RO=29, KI-RO=12 in batch          │
    │                                         │
    │    ZA (Zakros) - 53 inscriptions        │
    │    BATCH ANALYZED: 28 (52.8%)           │
    │    KU-RO present; KI-RO absent          │
    │                                         │
    │    PH (Phaistos) - 66 inscriptions      │
    │    BATCH ANALYZED: 35 (53.0%)           │
    │    KU-RO in MMIII = EARLIEST K-R        │
    │                                         │
    │    OTHER SITES (17 additional):         │
    │    ARKH=10, KN=13, MA=6, PK=2, TY=2     │
    │    IOZ=5, SYZ=4, KNZ=4, others          │
    └─────────────────────────────────────────┘
```

**Observed pattern**: K-R vocabulary (KU-RO/KI-RO/SA-RA₂) concentrated at HT. Absence at other sites may reflect site function, chronology, or regional variation. **Insufficient coverage to determine universality.**

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
| **IO Za 2** | Iouktas | **HIGH** | 6-position libation formula; JA-SA-SA-RA-ME divine name |
| **HT 85a** | Hagia Triada | **HIGH** | KU-RO 66 VERIFIED (exact arithmetic match) |
| **HT 122a/b** | Hagia Triada | **HIGH** | PO-TO-KU-RO 97 grand total; dual KU-RO sections |
| **KH 6** | Khania | **MEDIUM** | CYP+D fractional copper; zero K-R confirmed |
| **KH 7a** | Khania | **MEDIUM** | CYP+D and CYP+E in same document; VIR+*313b |
| **PK Za 11** | Palaikastro | **MEDIUM** | Libation formula; DI-KI-TE toponym; SA-SA-RA-ME |
| **ZA 10b** | Zakros | **MEDIUM** | 12 entries; no KU-RO (distribution record) |
| **HT 95a** | Hagia Triada | **MEDIUM** | GRA distribution; DA-DU-MA-TA header |
| **SY Za 4** | Kato Symi | **MEDIUM** | A-TA-I-*301-WA-JA libation verb cross-site |
| **KH 11** | Khania | **MEDIUM** | Mixed CYP+VIN; extensive fractions (¹⁄₁₆, ¹⁄₆, ¹⁄₃); *301+1 logographic |

**Detailed Manual Analysis**: 24 inscriptions (above)
**Automated Batch Analysis**: 300/1,721 inscriptions (17.43% coverage)
**See**: `data/extended_corpus_analysis.json` for full batch results

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

**Status**: Phase B3 COMPLETE (validation testing done)

| Metric | Value |
|--------|-------|
| Occurrences | 561 |
| Logographic contexts | 32 (5.7%) - with numerals |
| Syllabographic contexts | 53 (9.4%) - in word sequences |
| Standalone (requires context) | 476 (84.8%) |
| Sites | 17 (HT 42.4%, 238 occ) |

**DUAL-USE SIGN CONFIRMED**: *301 functions as BOTH logogram (commodity/measurement) AND syllabogram

| Pattern | Occurrences | Context | Sites |
|---------|-------------|---------|-------|
| *301+*311 | 20 | Measurement compound | Khania (primary) |
| A-TA-I-*301-WA-JA | 11 | Libation formula verb | IO, SY, KO, PK, TL |
| *301-*301 | 8 | Reduplicated logogram | HT |
| TE-*301 | 4 | Syllabographic sequence | HT |

**Phase B3 Validation Results**:

| Rank | Phoneme | IPA | Confidence | Evidence |
|------|---------|-----|------------|----------|
| 1 | **kya** | [kʲa] | **PROBABLE** | Syllabographic patterns + -WA-JA Luwian morphology |
| 2 | ḥa | [ħa] | POSSIBLE | Logographic use only; contradicted by syllabographic contexts |
| 3 | ʿa | [ʕa] | WEAK | Limited evidence |

**Key Finding**: Luwian /kya/ MORE PLAUSIBLE than Semitic /ħa/ — syllabographic patterns (word-medial *301-U-RA, word-final E-*301) contradict pure logographic Semitic hypothesis
| 4 | xa | [xa] | POSSIBLE | Multi-source |

**Key Context**: A-TA-I-*301-WA-JA (libation formula, 11 occurrences)

**Why Dropped in Linear B**: Represented phoneme(s) absent in Greek; logographic function obsolete

---

## Additional Undeciphered Signs (Phase 3 Complete)

### Sign *118: CVC Syllable with Final Consonant

| Metric | Value |
|--------|-------|
| Occurrences | 26 |
| Word-final | **69.2%** (CONFIRMED) |
| Word-initial | 19.2% |
| Word-medial | 11.5% |
| Primary site | HT (53.8%) |

**Key Patterns**:
- DA-SI-*118 (4 occ) — most stable form
- *21F-*118 (3 occ) — classifier + final marker
- I-QA-*118 (2 occ) — second most stable

**Phonetic Hypothesis**: CVC syllable with final consonant /-t, -n, or -m/
**Confidence**: PROBABLE

### Sign *304: Suffix/Postposition (REVISED)

| Metric | Value |
|--------|-------|
| Occurrences | 42 |
| Word-medial | **66.7%** |
| Word-final | 21.4% |
| Word-initial | 11.9% |
| Primary site | HT (66.7%) |

**REVISION**: Expected 93% initial, observed 11.9% — NOT emphatic/logographic
**Actual Function**: Suffix or postposition marker (medial dominant)
**Key Compound**: *304+PA (3 occ)
**Confidence**: POSSIBLE (function revised)

### Signs *21F/*21M: Gender Classifiers

| Sign | Occurrences | Primary Site | Medial % |
|------|-------------|--------------|----------|
| *21F | 22 | HT (63.6%) | 59.1% |
| *21M | 8 | PH (50.0%) | 87.5% |

**Function**: Paired gender classifier system
- *21F = Feminine classifier (more frequent, wider distribution)
- *21M = Masculine classifier (Phaistos cluster, rarer)
- Both appear word-internally, often with word-final marker following

**Key Pattern**: *21F-*118 (2 occ) — feminine + final consonant
**Confidence**: PROBABLE

### Sign *188: Vessel/Administrative Marker

| Metric | Value |
|--------|-------|
| Occurrences | 32 |
| Word-initial | **62.5%** |
| On roundels | **46.9%** (administrative seals) |
| Primary site | HT (59.4%) |

**Key Compound**: *86+*188 (11 occ, 34%) — dominant pattern at Khania
**Vessel Context**: Confirmed (PSIZa1 stone vessel)
**Administrative Use**: High roundel frequency supports seal/marking function
**Confidence**: PROBABLE

---

## Open Questions

### High Priority
1. **Is Semitic layer loanwords or genetic?** Current: Probably loanwords (no triconsonantal morphology)
2. **What language family is substrate?** Current: Unknown — "isolated" designation reflects inability to determine, not positive finding
3. **Can religious texts provide different vocabulary?** Current: Yes - distinct register (Luwian/Pre-Greek dominant)
4. **Why do -RU/-RE match Greek -os if Minoan is "isolated"?** Unresolved contradiction in scholarship

### Medium Priority
5. **Regional scribal traditions?** ANSWERED: HT = hub; KH = parallel system
6. **Vowel ending patterns?** PARTIAL: -U favors Luwian (64%), not Semitic
7. **Should we test Hurrian hypothesis?** Current: Low priority due to methodological criticisms

---

## Corpus Statistics

| Metric | Count |
|--------|-------|
| Total inscriptions | 1,721 |
| **Batch analyses** | **300 (17.43%)** |
| Total signs | ~7,400 |
| Core syllabograms | ~90 |
| Date range | c. 1800-1450 BCE |
| Sites in batch | 21 |

### Vowel Frequencies (Updated 2026-02-05)

| Vowel | Frequency | By Position (I/M/F) | Note |
|-------|-----------|---------------------|------|
| a | **41.67%** | 46.96% / 42.07% / 36.05% | Dominant — Anatolian/Semitic pattern |
| i | **24.06%** | 23.56% / 28.05% / 20.67% | Second most common |
| u | **17.20%** | 18.97% / 17.03% / 15.62% | Moderate |
| e | **13.14%** | 8.21% / 10.52% / 20.59% | Higher word-finally |
| **o** | **3.92%** | 2.30% / 2.34% / 7.08% | **CONFIRMS non-Greek** (expected ~20%) |

**Key Finding**: /o/ is marginal (3.92%) with 16% deviation from Greek expectation. Higher word-finally (7%) suggests possible epenthetic or borrowed function.

### CV Combination Gaps (15 Not Attested)

```
do, ji, jo, mo, no, pe, kwo, kwu, so, we, wo, wu, ze, zi, zo
```

**Pattern**: /o/ systematically rare; w-series restricted; z-series limited to /za/, /zu/

### Consonantal Series (Consensus View via Linear B Comparison)

| Category | Series | Notes |
|----------|--------|-------|
| Stops | /p/, /t/, /k/ | Voicing and aspiration unclear |
| Nasals | /m/, /n/ | — |
| Liquids | /l/, /r/ | Both represented by r-series |
| Fricative | /s/ | — |
| Approximants | /w/, /j/ | — |
| Affricates | z-series | Phonetic value debated |
| Labio-velars | q-series | Interpretation much-debated |

**Sources**: Duhoux 1992: 74-9, Davis 2014: 192-278, Consani 2021: 50-3

**Critical Caveat**: This 12-series inventory assumes Linear A phonemes map 1:1 to Linear B. Our dropped-sign analysis (123 unique signs) suggests Linear A had ADDITIONAL phonemes not captured here — pharyngeals, palatalized stops, possibly emphatics.

---

## Syntax (2026-02-05 Analysis)

| Feature | Status | Evidence | Caution Level |
|---------|--------|----------|---------------|
| Word Order | **VSO PROBABLE** | Verb-initial in religious texts (score 3.0) | PROBABLE |
| Syntactical Complexity | Very limited | Formulaic, cultic/ritual inscriptions | ESTABLISHED |
| Longest Syntactic Texts | Libation formulas | 6-position structure (Salgarella 2020) | ESTABLISHED |

**Word Order Hypothesis Scores** (`syntax_analyzer.py`):
| Hypothesis | Score | Evidence |
|------------|-------|----------|
| **VSO** | **3.0** | A-TA-I-*301-WA-JA verb-initial in religious formulas |
| SOV | 0.5 | Suffixes word-final (-TE, -TI) |
| SVO | -0.5 | No supporting evidence |

**Particle Positions** (150+ occurrences mapped):
- **-JA**: Initial dominant (150 occ) — verb morphology or prefix
- **-TE/-TI**: Final dominant (93/91 occ) — clear suffixes
- **-WA**: Medial dominant (42 occ) — clitic particle

**Our Position**: VSO now **PROBABLE** based on systematic analysis. Religious texts show clear verb-initial pattern; administrative texts show suffix-heavy morphology consistent with Luwian influence.

---

## Critical Dependencies

If these anchors change, dependent readings must be re-evaluated.

**Tools**: `tools/anchor_tracker.py --cascade ANCHOR_ID --to QUESTIONED`

### Anchor Registry

| Anchor ID | Name | Level | Confidence |
|-----------|------|-------|------------|
| anchor_linear_b_comparison | Linear B Phonetic Comparison | 2 | HIGH |
| anchor_semitic_loan_layer | Semitic Loanword Layer | 4 | MEDIUM |
| anchor_luwian_morphology | Luwian Morphological Layer | 4 | MEDIUM |
| anchor_toponym_phaistos | PA-I-TO = Phaistos | 1 | CERTAIN |
| anchor_toponym_kydonia | KU-DO-NI-JA = Kydonia | 1 | CERTAIN |
| anchor_commodity_logograms | Commodity Logograms | 3 | HIGH |
| anchor_kuro_total | KU-RO = Total/Sum | 2 | HIGH |
| anchor_kiro_deficit | KI-RO = Deficit/Category | 4 | MEDIUM |
| anchor_ja_suffix | -JA Adjectival Suffix | 5 | MEDIUM |

### Reading Dependencies

| Reading | Depends On | Max Confidence | Cascade Risk |
|---------|------------|----------------|--------------|
| KU-RO | Linear B + kuro_total | HIGH | Foundation of K-R paradigm |
| KI-RO | Linear B + kiro_deficit + semitic | MEDIUM | Dependent on KU-RO |
| SA-RA₂ | Linear B + semitic | PROBABLE | Semitic layer dependent |
| PO-TO-KU-RO | Linear B + kuro_total | PROBABLE | Derived from KU-RO |
| -JA suffix | Linear B + luwian + ja_suffix | PROBABLE | Single-hypothesis cap |
| PA-I-TO | toponym_phaistos | CERTAIN | Primary anchor |
| SU-PU, KA-RO-PA₃ | Linear B + semitic | PROBABLE | Vessel vocabulary |

### Cascade Warnings

When reviewing an anchor, run: `python tools/anchor_tracker.py --cascade ANCHOR_ID --to QUESTIONED`

Example cascade from `anchor_semitic_loan_layer`:
- SA-RA₂ → demote to SPECULATIVE
- SU-PU → demote to SPECULATIVE
- KA-RO-PA₃ → demote to SPECULATIVE
- Affects 35 words (17.7% of corpus)

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
| *301 | 561 | dual-use | /kʲa/ (PROBABLE) or /ħa/ (POSSIBLE) | Hybrid (logogram + syllable) |
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

### Vector 5: Chronological Wedge (EXPANDED 2026-02-05)

#### Contact Language Layer Timeline

| Layer | First Appearance | Peak Period | Key Evidence |
|-------|------------------|-------------|--------------|
| **Luwian (morphology)** | **MMII** | LMIB | -JA suffix (PHWc39), -WA (PH6) |
| **Pre-Greek (substrate)** | **MMII** | LMIA | Long compounds, archaic signs (*314, *320) |
| **Semitic (loans)** | **MMIII** | LMIB | KU-RO (PH(?)31a), full K-R in LMIB |

#### Period-by-Period Distribution

| Period | K-R Status | Luwian Features | Pre-Greek Features |
|--------|------------|-----------------|-------------------|
| **MMII** (1800-1700) | ZERO | -JA, -WA present | Archaic signs (*314, *320), long compounds |
| **MMIII** (1700-1600) | KU-RO x1 | -JA continuing | Long compounds |
| **LMIA** (1600-1500) | ZERO | A-TA-I-*301-WA-JA emerges | JA-SA-SA-RA-ME emerges |
| **LMIB** (1500-1450) | Full system | Complete morphology | Religious vocabulary |

#### Key Inscription References

| Inscription | Period | Features Present |
|-------------|--------|------------------|
| PHWc39 | MMII | JA-DI (earliest -JA suffix) |
| PH6 | MMII | I-NA-WA (earliest -WA), I-DA-PA3-I-SA-RI (6-syllable compound) |
| PHWc37 | MMII | KA-*314-SI *320 (archaic signs, MMII-exclusive) |
| PH(?)31a | MMIII | KU-RO (earliest Semitic admin term) |
| IO Za 6 | LMIA | JA-SA-SA-RA-ME (earliest gemination), libation formula |
| SY Za 3-4 | LMIA | A-TA-I-*301-WA-JA, SI-RU-TE |
| HT series | LMIB | Full K-R paradigm (KU-RO 33, KI-RO 12, SA-RA2 20) |

**Key Discovery**: K-R Innovation Horizon = **MMIII Phaistos** (PH(?)31a). Full system develops over ~200 years. Luwian morphology is the OLDEST contact layer, present from earliest texts.

---

## Key References

| Author | Year | Work | Contribution |
|--------|------|------|--------------|
| Gordon | 1966 | *Evidence for the Minoan Language* | KU-RO = *kull* (Semitic "total") |
| Palmer | 1958 | — | -JA suffix; Luwian morphology |
| Beekes | 2014 | *Pre-Greek* | Substrate phonology |
| Salgarella | 2020 | *Aegean Linear Scripts* | HT 28 structure; 6-position libation formula; MA-RU = wool; sign classification |
| Younger | 2024 | *Linear A Texts: Introduction* | U-MI-NA-SI = 'debt/owes'; transcriptions |
| Schoep | 2002 | — pp. 159-66 | Transaction terms (KU-RO, KI-RO context) |
| Valério | 2007 | — | -TE/-TI = 'from/of' interpretation |
| Steele & Meissner | 2017 | — | -RU/-RE morphology; word endings |
| Duhoux | 1978, 1992, 1997 | — | Affixes; phonology; I-/J- prefix |
| Davis | 2013, 2014 | — | VSO hypothesis; "isolated language" consensus |
| Consani | 2021 | — pp. 50-53 | Recent phonological overview |

### Critical Gaps in Our Bibliography

| Citation | Why Critical | Priority |
|----------|--------------|----------|
| **Davis 2014** (full) | Comprehensive synthesis: phonology (192-278), affiliation (156-278) | URGENT |
| **Duhoux 1992** | Phonology + libation formula primary analysis | URGENT |
| **Duhoux 2020** | Current "isolated language" position | HIGH |
| **Consani 2021** | Most recent phonological analysis | HIGH |

**Note**: We frequently cite secondary sources (Salgarella 2020) but lack primary methodological works (Davis, Duhoux). Acquiring these is essential for rigorous scholarship.

---

*Knowledge base consolidating STATE_OF_KNOWLEDGE.md, CONFIRMED_READINGS.md, and ANALYSIS_INDEX.md*
*Full discovery chronology in CHANGELOG.md*
