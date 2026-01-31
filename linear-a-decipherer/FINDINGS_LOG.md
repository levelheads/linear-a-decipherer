# Findings Journal

**Chronological record of discoveries and interpretation changes**

---

## 2026-01-31

### Script Adaptation Analysis: 123 Unique Linear A Signs

**Scope**: Systematic analysis of signs that exist in Linear A but have no Linear B equivalent

**Key Finding**: When Greeks adapted Linear A to write Mycenaean Greek (~1450 BCE), they dropped 123 signs representing sounds that Greek did not have.

**Quantitative Results**:
- **123 unique signs** identified (GORILA *XXX series)
- **874 total attestations** across corpus
- **30+ sites** attest unique signs
- ***301** is most frequent (290 occurrences, 23 sites)

**Top Unique Signs**:

| Sign | Attestations | Primary Position | Key Context |
|------|-------------|------------------|-------------|
| *301 | 290 | Initial (88%) | A-TA-I-*301-WA-JA (libation formula) |
| *304 | 42 | Initial (88%) | Standalone; commodity contexts |
| *188 | 32 | Mixed | With SU-PU₂, PA₃ |
| *21 | 30 | Initial (70%) | *21F, *21M (gender markers) |
| *118 | 26 | Final (69%) | DA-SI-*118 (word-final) |

**Phonological Inferences**:

| Feature | Evidence | Confidence |
|---------|----------|------------|
| **More consonants than Greek** | 123 unique signs dropped | HIGH |
| **Possible pharyngeals** | *301 distribution matches Semitic pattern | MEDIUM |
| **Possible palatalized series** | Luwian parallels; position constraints | MEDIUM |
| **/l/ vs. /r/ distinction** | Separate sign series retained | HIGH |
| **Grammatical classifiers** | F/M marked signs (*21F, *21M, etc.) | MEDIUM |

**Hypothesis Scores**:
- Luwian/Anatolian: +3 (palatalized consonants explain many unique signs)
- Semitic: +2 (pharyngeals explain *301)
- Pre-Greek: +1 (unique inventory consistent with isolate)
- Proto-Greek: **-2** (Greek has FEWER phonemes, not more)

**Implications**:
1. Linear A language had richer consonant inventory than Greek
2. Dropped signs reveal "negative space" of Greek phonology
3. *301 is critical — appears in religious vocabulary with Luwian-like morphology
4. Script adaptation is a methodological tool for phoneme reconstruction

**Confidence**: HIGH (systematic corpus-wide analysis)

**File**: [../analysis/sessions/LINEAR_A_UNIQUE_SIGNS_ANALYSIS.md](../analysis/sessions/LINEAR_A_UNIQUE_SIGNS_ANALYSIS.md)

---

### Corpus Structural Audit: Function Words and Arithmetic

**Scope**: Automated structural analysis of entire corpus (1,722 inscriptions)

**Tool**: `tools/corpus_auditor.py` (new)

**Key Findings**:

#### 1. TE is a Header/Topic Marker (HIGH confidence)
- **Position**: 67% line-initial, 31% medial, 2% final
- **Entropy**: 0.637 (moderately fixed position)
- **Distribution**: 58 occurrences across 12 sites
- **Hypothesis**: Functions as topic/header marker, not conjunction
- **Note**: Different from -TE suffix (verbal ending)

#### 2. KI-RO Commodity Association Pattern (CLARIFIED)
- **Finding**: When KI-RO appears ON SAME LINE as a commodity, it's always CYP (copper)
- **Note**: KI-RO often appears as standalone (no commodity on line) - these cases not counted
- **Implication**: KI-RO + CYP is a fixed phrase for "copper deficit"; standalone KI-RO is generic
- **Contrast with KU-RO**: KU-RO appears with multiple commodities (GRA, OLIV, VIN) = generic "total"

#### 3. KU-RO Arithmetic Validation (Mixed Results)
- **Verified**: 11.4% (exact match)
- **Close match** (≤0.5 diff): HT13 differs by only 0.5 (likely fraction parsing)
- **Large mismatches**: Many tablets show significant differences
- **Interpretation**: Mismatches likely due to:
  - Multi-section tablets (KU-RO totals only current section)
  - Damaged/missing lines
  - Unparsed fraction signs

#### 4. Token-Commodity Associations
**High-specificity tokens** (100% one commodity):
- KA → CYP (copper): 169 associations
- SI → VIN (wine): 118 associations
- NI → VIN (wine): 76 associations
- TA → OLE (oil): 29 associations
- KI-RO → CYP (copper): 16 associations

**Low-specificity tokens** (function words):
- KU-RO: Appears with GRA, OLIV, VIN (confirms generic "total" function)
- A-DU: Appears with VIR, GRA, CYP (generic administrative term)

**Confidence**: HIGH (automated corpus-wide analysis)

**File**: data/audit/corpus_audit.json

---

### Phase 10: Khania Operates Parallel Administrative System

**Scope**: Complete vocabulary analysis of Khania (KH) corpus (227 inscriptions)

**Key Finding**: KH uses a **DIFFERENT** administrative system from Hagia Triada.

**Evidence**:
1. **ZERO** KU-RO occurrences (vs. 35 at HT)
2. **ZERO** KI-RO occurrences (vs. 16 at HT)
3. **ZERO** SA-RA₂ occurrences (vs. 20 at HT)
4. Only 1.8% vocabulary overlap with HT

**KH-Specific Signs Identified**:
- `*164` = textile marker (13 occ)
- `*306` = commodity qualifier (7 occ)
- `*401+RU` = liquid measure (7 occ)
- `CYP+D/CYP+E` = copper grades (parallel to HT OLE variants)
- `*411-VS/*409-VS/*408-VS` = vessel content sealings

**Implications**:
- Semitic administrative vocabulary (KU-RO, SA-RA₂) may be HT-specific
- KH may preserve older/indigenous vocabulary
- Regional variation is REAL - cannot assume HT readings apply corpus-wide

**Confidence**: HIGH (complete corpus analysis)

**File**: [../analysis/sessions/PHASE10_KH_VOCABULARY_COMPLETE.md](../analysis/sessions/PHASE10_KH_VOCABULARY_COMPLETE.md)

---

### Semitic Vessel Vocabulary Confirmed (HT 31)

**Finding**: Three vessel terms show strong Akkadian cognates

| Linear A | Akkadian | Meaning | Confidence |
|----------|----------|---------|------------|
| **SU-PU** | *suppu* | bowl | PROBABLE |
| **KA-RO-PA₃** | *karpu* | vessel | PROBABLE |
| **QA-PA₃** | *qappu* | measure | POSSIBLE |

**Context**: HT 31 vessel inventory (3,775 vessels calculated)

**Implications**:
- Semitic vocabulary extends to THREE domains: accounting (KU-RO), allocation (SA-RA₂), vessels (SU-PU)
- Strengthens loanword layer hypothesis
- Vessel inventories use different conventions (no KU-RO total)

**Confidence**: PROBABLE (phonological fit + contextual match)

**File**: [../analysis/completed/inscriptions/HT31_TRANSLATION.md](../analysis/completed/inscriptions/HT31_TRANSLATION.md)

---

### Personal Names: 127 Identified with Theophoric Patterns

**Finding**: Comprehensive extraction identifies 127 personal names (140% increase)

**Linguistic Distribution**:
- Unknown: 48 (37.8%)
- Semitic: 28 (22.0%)
- Pre-Greek: 25 (19.7%)
- Luwian: 21 (16.5%)
- Greek: 5 (3.9%)

**High-Confidence Deity Names**:
| Linear A | Linear B | Deity | Confidence |
|----------|----------|-------|------------|
| **DA-MA-TE** | *da-ma-te* | Demeter | HIGH |
| **A-TA-NA** | *a-ta-na* | Athena | HIGH |

**Suffix Patterns**: -JA (26, theophoric), -NA (18, feminine), -NE (14, feminine), -SI (10, origin)

**Implications**:
- Demeter and Athena worship may have Minoan origins
- 48% of names contain theophoric elements
- Pre-Greek substrate best explains religious naming

**Confidence**: HIGH (systematic corpus-wide analysis)

**File**: [../data/personal_names_comprehensive.json](../data/personal_names_comprehensive.json)

---

### HT 28: 5 Oil Types and U-MI-NA-SI Dual Usage

**Finding**: HT 28 documents 5 distinct oil types on single tablet

**Oil Types**: OLE+U, OLE+KI, OLE+MI, OLE+TU, OLE+DI

**U-MI-NA-SI Discovery**: This term appears in BOTH:
- Administrative context (HT 28 header)
- Religious context (peak sanctuary libations)

**Implications**:
- Oil economy was highly differentiated
- Some vocabulary crosses administrative/religious boundary
- SA-RA₂ functions as section marker within accounts

**Confidence**: PROBABLE (structural analysis)

**File**: [../analysis/completed/inscriptions/HT28_TRANSLATION.md](../analysis/completed/inscriptions/HT28_TRANSLATION.md)

---

### Commodity Logogram Analysis Complete - 11 Oil Types Identified

**Scope**: Systematic corpus survey of commodity logograms and modifiers

**Key Findings**:

1. **OLE (Olive Oil) Has Most Complex Modifier System**
   - 11+ distinct forms: OLE, OLE+U (22), OLE+KI (21), OLE+MI (19), OLE+DI (12), OLE+NE (5), OLE+E (4), OLE+A (2), OLE+QE+DI, OLE+KI+U, OLE+KI+ME, OLE+TU
   - TY 3a tablet records 8+ distinct oil types in single document
   - Complex compounds (OLE+KI+U, OLE+KI+ME) suggest subcategories

2. **VIN (Wine) Shows Minimal Modification**
   - Only VIN+KA (1 occurrence) and PU-VIN (2 occurrences)
   - Either wine was more homogeneous commodity OR marked differently

3. **GRA (Grain) Has 7+ Variants**
   - GRA+PA (19 - most common), GRA+KU (7), GRA+QE (4), GRA+K+L (3), GRA+B (2), GRA+DA (1), GRA+H (1), GRA+E (1)

4. **CYP+E Shows Geographic Concentration**
   - 11 of 13 CYP+E occurrences are from Khania (KH)
   - Suggests regional scribal practice or metal quality distinction

5. **SA-RA2 Confirmed as Multi-Commodity Term**
   - Appears with GRA (5x), CYP (5x+), OLE (2x)
   - Supports interpretation as administrative "allocation" term

6. **Modifiers Likely Acrophonic** (like Linear B)
   - Linear B uses OLE+WO (rose oil), OLE+RI (linseed oil), OLE+PA (palm oil)
   - Linear A modifiers may use different phonetic values for same concept
   - Cannot verify without knowing Minoan vocabulary

**Attestation Counts**:
- VIN: 53 occurrences
- GRA: 62+ (with variants)
- CYP: 52+ (13 CYP+E)
- OLIV: 24 occurrences
- OLE: 22+ (with 100+ including variants)
- FAR, FIC: Not attested (may use different notation)

**Implications**:
- Oil economy was highly differentiated (8+ types vs. 1 wine type)
- Modifier system parallels but differs from Linear B
- Quality/processing grades most likely interpretation
- Regional variation exists (CYP+E at Khania)

**Confidence**: HIGH for pattern identification; UNDETERMINED for specific modifier meanings

**File**: [../analysis/sessions/COMMODITY_ANALYSIS.md](../analysis/sessions/COMMODITY_ANALYSIS.md)

---

### Phase 2: -U Endings Pattern Re-evaluated - "100% Semitic Discrimination" NOT Confirmed

**Previous claim**: Phase 1 reconnaissance reported that -U endings discriminate 100% for Semitic hypothesis (39 words)

**New finding**: -U endings actually favor Luwian hypothesis (64%) over Semitic (24%)

**Evidence**:
1. 25 -U words with freq >= 2 systematically tested against all 4 hypotheses
2. Hypothesis support distribution:
   - Luwian: 16 words (64%)
   - Semitic: 6 words (24%)
   - Proto-Greek: 2 words (8%)
   - Pre-Greek: 1 word (4%)
3. The -U ending more likely represents Luwian quotative particle than Semitic nominative case
4. K-R skeleton words (A-KA-RU, KA-RU, KO-RU) DO support Semitic, but this is due to consonant pattern, not -U ending
5. Multi-hypothesis support common for A-...-U pattern words

**Words that DO support Semitic**:
- A-DU (10 occ): Semitic 3.15, Luwian 3.0 - narrow margin
- A-KA-RU (3 occ): Semitic 5.35 - strong K-R skeleton match
- KA-RU (2 occ): Semitic 5.35 - K-R skeleton
- KO-RU (1 occ): Semitic 5.35 - K-R skeleton
- A-RU (2 occ): Semitic 7.7 - multiple root matches
- KU-NI-SU (5 occ): Semitic 1.95 - KNS "gather" match

**Words that support Luwian instead**:
- KU-PA3-NU (8 occ): Luwian 2.0, Semitic 0.75
- DI-NA-U (6 occ): Luwian 3.0, Semitic 0.25
- SA-RU (6 occ): Luwian 2.0, Semitic 1.3
- *306-TU (4 occ): Luwian 1.0, Semitic 0.25
- TE-TU (3 occ): Luwian 1.0, Semitic 0.25
- QA-QA-RU (3 occ): Luwian 2.0, Semitic 0.75
- And 10 more...

**Implications**:
1. Slot grammar analysis prediction was based on theoretical morphology, not tested readings
2. -U as Luwian quotative particle is a better explanation than Semitic nominative
3. Focus Semitic investigation on K-R consonant skeleton, not vowel endings
4. Multi-hypothesis support suggests possible loanword layer

**Methodological Note**: This follows First Principle #2 (Ventris Lesson) - abandoned the "100% Semitic" claim when evidence contradicted it

**Confidence**: HIGH (systematic 4-hypothesis testing completed)

**File**: [analysis/sessions/PHASE2_U_ENDINGS_ANALYSIS.md](../analysis/sessions/PHASE2_U_ENDINGS_ANALYSIS.md)

---

### OPERATION MINOS Phase 7: Translation Attempts Preview Complete

**Scope**: Attempted full translations of 4 well-structured HT tablets

**Tablets Analyzed**:
1. **HT 13** - Wine distribution list (6 recipients, KU-RO 130.5)
2. **HT 9a** - Wine list (7 recipients, KU-RO 31.75)
3. **HT 9b** - Commodity list (same names as 9a, KU-RO 24)
4. **HT 88** - Personnel/commodity assessment (A-DU header, KI-RO/KU-RO sections)

**Key Findings**:

1. **Numerical Verification Works**
   - HT 13: Calculated sum = 131, stated KU-RO = 130.5 (0.5 discrepancy)
   - HT 9a: Calculated sum = 31, stated KU-RO = 31.75 (0.75 discrepancy)
   - HT 9b: Calculated sum = 24, stated KU-RO = 24 (EXACT MATCH)
   - HT 88: Deficit section sum = 6, stated KU-RO = 6 (EXACT MATCH)

2. **Cross-Referencing Tablets Is Productive**
   - HT 9a and HT 9b share 6 of 7 recipient names
   - Different quantities suggest different time periods or allocation types
   - Demonstrates consistent personnel/name tracking across documents

3. **Document Structure Template Confirmed**
   ```
   HEADER (title/heading) + COMMODITY LOGOGRAM + TE (transaction)
   BODY (names + quantities)
   [KI-RO section if deficit]
   KU-RO (TOTAL) + sum
   ```

4. **What We CAN Translate**
   - Commodity logograms (VIN, NI, OLE, VIR) - CERTAIN
   - Numerical system (base-10, fractions) - CERTAIN
   - Totaling term (KU-RO) - HIGH
   - Deficit term (KI-RO) - HIGH
   - Document structure - HIGH

5. **What We CANNOT Translate**
   - Personal names (20+ sequences remain opaque)
   - Heading terms (KA-U-DE-TA, SA-RO, PA3)
   - Exact semantics of A-DU (probable but not certain)
   - Commodity units (liters? kilograms?)

**Implications**:
- Administrative Linear A tablets are ~60% readable (structure + commodities + numerals)
- Personal names represent the largest gap in understanding
- Semitic administrative vocabulary hypothesis continues to gain support
- Translation viability rated PROBABLE for structurally clear tablets

**Confidence**: PROBABLE (First Principles: 6/6 PASS or PARTIAL)

**File**: [analysis/sessions/PHASE7_TRANSLATIONS.md](../analysis/sessions/PHASE7_TRANSLATIONS.md)

---

### OPERATION MINOS Phase 6: Suffix and Ending Analysis Complete

**Scope**: Analyzed 20 most frequent word endings in Linear A corpus

**Key Findings**:

1. **-JA is Adjectival/Derivational Suffix (PROBABLE)**
   - 65 occurrences, 66% word-final
   - Matches Luwian -iya pattern (adjectival/ethnic suffix)
   - -WA-JA combination (43 occurrences) strongly supports Luwian connection
   - Appears on place names, ethnics, and derived forms

2. **-TE/-TI May Be Verbal Endings (POSSIBLE)**
   - -TE: 56 occurrences, 79% final (possible 3sg past, cf. Luwian -ta)
   - -TI: 49 occurrences, 53% final (possible 3sg present, cf. Luwian -ti)
   - SI-RU-TE consistently appears in ritual contexts

3. **Vowel Ablaut System Confirmed**
   - K-R paradigm: KU-RO / KI-RO / KU-RE / KI-RA / KU-RA (67 attestations of -RO)
   - Vowel alternation carries grammatical meaning
   - KU-RE appears immediately before KU-RO in HT39 (subtotal + grand total?)

4. **-RO is Lexical Element, Not Productive Suffix**
   - 78 occurrences dominated by KU-RO (37) and KI-RO (16)
   - Part of K-R root paradigm, not separable suffix

5. **Negative Evidence: No Greek Case Endings**
   - Expected -os, -ou, -oi, -ai, -es: 0% observed
   - Further weakens Proto-Greek hypothesis

**Hypothesis Rankings for Suffix System**:
- Luwian: STRONGEST (matches -iya, -ti, -ta patterns)
- Pre-Greek: MEDIUM (substrate elements possible)
- Semitic: LOW (some lexical items only)
- Proto-Greek: WEAKEST (morphology absent)

**Confidence**: HIGH for patterns; POSSIBLE-PROBABLE for interpretations

**File**: [analysis/sessions/PHASE6_SUFFIXES.md](../analysis/sessions/PHASE6_SUFFIXES.md)

---

### OPERATION MINOS Phase 3: Hagia Triada Administrative Conquest Complete

**Scope**: Systematic analysis of HT corpus (1,110 tablets, 34% of Linear A)

**Key Findings**:

1. **8 Core Administrative Terms Mapped**
   - KU-RO (total), KI-RO (deficit/header), SA-RA2 (allocation)
   - A-DU (assessment), KA-PA (summary), SA-TA (section)
   - RE-ZA (recipient?), TE (qualifier)

2. **Commodity Frequency Hierarchy Established**
   - NI (figs): 188+ occurrences - most common
   - OLE (oil variants): 138+ occurrences
   - GRA (grain): 128+ occurrences
   - CYP (copper): 105+ occurrences
   - VIN (wine): 83+ occurrences

3. **Oil Variant Typology Discovered**
   - 6+ distinct oil types: OLE+U, OLE+A, OLE+E, OLE+MI, OLE+KI, OLE+DI
   - Likely reflect processing stages, origins, or purposes
   - OLE+U most common (Semitic -U ending?)

4. **HT Document Structure Template Defined**
   ```
   HEADER → [A-DU/KA-PA] → BODY (names+quantities)
      → [KI-RO section] → KU-RO TOTAL → [SA-RA2 allocation]
   ```

5. **SA-RA2 Exclusively at HT**
   - All 20 occurrences at Hagia Triada
   - Confirms site-specific administrative vocabulary
   - Supports redistribution center function

**Implications**:
- HT administrative system now well-documented
- Oil economy more sophisticated than previously understood
- Regional vocabulary variation confirmed (SA-RA2 = HT only)
- Ready for Phase 4 cross-site comparison

**Confidence**: HIGH (First Principles: 6/6 PASS)

**File**: [analysis/sessions/PHASE3_HT_ADMIN.md](../analysis/sessions/PHASE3_HT_ADMIN.md)

---

### OPERATION MINOS Phase 1: Full Spectrum Reconnaissance Complete

**Scope**: Deployed all 14 analysis tools across 1,721-inscription corpus

**Key Findings**:

1. **Proto-Greek Hypothesis WEAK (score: -15.0)**
   - /o/ frequency: 3.9% (expected ~20% for Greek)
   - /a/ frequency: 41.7% (expected ~22% for Greek)
   - Greek case endings (-os, -on, -oi, -ai, -es): 0% observed
   - Luwian now ranks HIGHEST (+3.5); Semitic neutral (0.0)

2. **K-R Paradigm Expanded: 21 Forms Found**
   - KU-RO (37), KI-RO (16), KU-RE (2), KI-RA (2), KU-RA (2), KI-RU (1)
   - Includes rare variants for extended paradigm investigation

3. **30 Kober Paradigm Candidates Identified**
   - KU- root: 4 variants
   - SA- root: 5 variants
   - Multiple other roots with 2-3 suffixed forms

4. **Discriminating Vowel Patterns Confirmed**
   - -U ending: 39 words → favors SEMITIC (100% discrimination)
   - -E/-O endings: 65 words → favors PROTOGREEK (but hypothesis weak overall)
   - -DU ending: 8 words → favors SEMITIC

5. **Regional Standardization: LOW**
   - HT-KH overlap: 1.8% Jaccard similarity
   - HT-ZA overlap: 2.3% Jaccard similarity
   - K-R forms concentrated at HT (51/60 occurrences)

6. **207 Slot Words Identified**
   - SA-RA₂ (18), KU-RO (12), KU-PA (5), SA-RO (4), PU-RA₂ (4)
   - All appear in commodity contexts for Phase 2 investigation

**Implications**:
- Proto-Greek should be deprioritized in future analyses
- Semitic administrative vocabulary is the most accessible layer
- Regional independence requires cross-site validation
- 21 K-R forms provide expanded paradigm investigation material

**Confidence**: HIGH (First Principles: 6/6 PASS)

**File**: [analysis/completed/thematic/PHASE1_RECONNAISSANCE_REPORT.md](../analysis/completed/thematic/PHASE1_RECONNAISSANCE_REPORT.md)

---

### JA-SA-SA-RA-ME = Divine Name (PROBABLE)

**Previous interpretation**: Unknown sequence

**New interpretation**: Divine name or major deity in Minoan religion

**Evidence**:
1. All 7 occurrences at peak sanctuary sites (IOZ=Mt Iouktas, PKZ=Petsofa, PSZ=Psychro, PLZ=Palaikastro, TLZ=Traostalos)
2. Pre-Greek phonological features: gemination SA-SA, vowel alternation
3. Often followed by U-NA-KA-NA-SI (possible epithet)
4. Context: exclusively religious/votive inscriptions
5. Hypothesis scores: Pre-Greek 2.5, Semitic 0.7, Proto-Greek 0.25

**Implications**:
- First PROBABLE reading of a divine name in Linear A
- Confirms religious register distinct from administrative
- Pre-Greek substrate strongest for religious vocabulary
- U-NA-KA-NA-SI may be an epithet or title for this deity

**Confidence**: PROBABLE (Pre-Greek best fit; exclusive religious context)

**File**: [analysis/sessions/SESSION_LOG_2026-01-31_PHASE2.md](../analysis/sessions/SESSION_LOG_2026-01-31_PHASE2.md)

---

### I-PI-NA-MA + SI-RU-TE = Fixed Ritual Formula

**Finding**: These two words form a fixed formula in libation/votive contexts

**Evidence**:
- Co-occur in 4/6 I-PI-NA-MA contexts
- Co-occur in 4/7 SI-RU-TE contexts
- PMI = 7.36 (highest pair in corpus)
- Both appear exclusively at peak sanctuaries

**Interpretation**: Likely a ritual formula or invocation phrase, similar to "pray to [deity]" or "offer to [deity]"

**Confidence**: POSSIBLE (formulaic pairing confirmed; semantics uncertain)

---

### KU-RE Appears Before KU-RO in HT39

**Finding**: In HT39, the sequence is "10 | KU-RE | KU-RO"

**Interpretation**:
- KU-RE may be a subtotal or running total
- KU-RO = grand total
- Vowel alternation (U→E) may indicate different total types

**Confidence**: SPECULATIVE (only 2 occurrences of KU-RE)

---

### SA-RA₂ = Akkadian šarāku (PROBABLE)

**Previous interpretation**: Possibly *še'u* "barley" (Semitic)

**New interpretation**: *šarāku* "to allocate, grant" (Akkadian)

**Evidence**:
1. Multi-commodity distribution (GRA, CYP, OLE) rules out commodity name
2. Always precedes logogram, never follows
3. Positional pattern matches allocation terminology
4. Phonological fit: šarāku → SA-RA₂ (with final syllable loss)
5. Gordon precedent: if KU-RO = *kull*, other Semitic terms plausible
6. Archaeological context: Hagia Triada was redistribution center

**Implications**:
- Confirms Semitic (specifically Akkadian) vocabulary in Linear A administrative texts
- Supports "loanword layer" interpretation (borrowed terms, not genetic relationship)
- Explains why SA-RA₂ appears with multiple commodity types

**First Principles Verification**: All 6 PASS

**File**: [analysis/completed/thematic/SA-RA2_akkadian_deep_investigation.md](../analysis/completed/thematic/SA-RA2_akkadian_deep_investigation.md)

---

### KU-RO / KI-RO Relationship Clarified

**Previous assumption**: Complementary distribution (one or the other, never both)

**New finding**: Overlapping distribution; different accounting functions

**Evidence**:
- 5 inscriptions contain BOTH forms: HT 88, HT 94b, HT 117a, HT 123+124a, HT 123+124b
- KU-RO consistently = grand total (sum of entries)
- KI-RO serves multiple functions:
  - Header/category marker
  - Fractional/partial amounts
  - Deficit/remainder after total

**Functions identified**:
```
KU-RO = Σ (all entries) = GRAND TOTAL
KI-RO = partial amount OR amount outstanding

When both appear:
- KI-RO before list = "owed/outstanding category"
- KI-RO after KU-RO = "remaining/deficit from total"
- KI-RO within blocks = "partial/fractional allocation"
```

**Implications**:
- KU-RO and KI-RO are NOT in complementary distribution
- They serve different accounting functions within same document
- Vowel alternation (U/I) may signal different roots, not inflection

**Confidence**: HIGH (Level 2 anchor - Linear B cognate + consistent position)

**File**: [analysis/sessions/analysis_session_2026-01-31.md](../analysis/sessions/analysis_session_2026-01-31.md)

---

### Vowel-Based Hypothesis Discrimination Pattern

**Finding**: Final vowel of Linear A words correlates with linguistic hypothesis support

| Final Vowel | Favors | Word Count | Example Suffixes |
|-------------|--------|------------|------------------|
| **-U** | Semitic | 39 | -U, -DU, -RU, -SU, -NU, -JU, -TU |
| **-E/-O** | Proto-Greek | 65+ | -E, -O, -RO, -RE, -SE, -NE, -ME, -TO |
| -A | Neutral | Many | -RA, -NA, -TA (both hypotheses) |
| -I | Luwian (weak) | Some | -RI, -TI, -DI |

**Possible explanations**:
1. **Language Mixture**: U-words = Semitic loans; E/O-words = Aegean substrate
2. **Morphological Differentiation**: Vowel quality marks grammatical distinctions

**Status**: Insufficient evidence to distinguish between explanations

**Confidence**: LOW-MEDIUM

**File**: [analysis/sessions/analysis_session_2026-01-31.md](../analysis/sessions/analysis_session_2026-01-31.md)

---

## 2026-01-09

### Knossos Ivory Scepter (KN Zf 2) Analyzed

**Discovery**: 119 signs - longest Linear A inscription ever found

**Key findings**:
- Two separate inscriptions by different scribes
- Ring: ceremonial/religious style (no numerals)
- Handle: administrative style with numerals and fractions
- Mixed scripts: Linear A + Cretan Hieroglyphic signs (*180, *181)

**Significance**:
- 1.6% of entire Linear A corpus in single object
- First Linear A economic document from cult context (handle)
- Dual register (sacred + secular) on same object

**Status**: Framework complete; awaiting full transliteration from Anetaki II publication

**File**: [analysis/completed/inscriptions/KNOSSOS_SCEPTER_COMPLETE.md](../analysis/completed/inscriptions/KNOSSOS_SCEPTER_COMPLETE.md)

---

### TY 3a Oil Distribution Analysis

**Finding**: Sophisticated oil accounting at Tylissos

**Details**:
- 68 entries, second longest tablet
- 8 distinct oil types (OLE+KI, OLE+U, OLE+MI, OLE+QIf, etc.)
- Mixed linguistic elements:
  - Semitic: A-DU (50%), A-DA
  - Luwian: KO-A-DU-WA (33%)
  - Pre-Greek: NE-KI (17%)

**Implications**:
- Regional administration as sophisticated as Hagia Triada
- Contact language hypothesis supported (Semitic + Luwian + Pre-Greek)
- No KU-RO totaling = distribution record, not inventory

**File**: [analysis/completed/inscriptions/TY3a_COMPLETE_ANALYSIS.md](../analysis/completed/inscriptions/TY3a_COMPLETE_ANALYSIS.md)

---

## 2026-01-05

### Contact Language Model Proposed

**Finding**: Linear A likely NOT simple monolingual system

**Proposed structure**:
- **Base**: Pre-Greek substrate (indigenous Aegean)
- **Administrative layer**: Semitic loan words (Near Eastern trade contact)
- **Religious layer**: Possible Luwian grammatical influence

**Evidence**:
- KU-RO = Semitic *kull* "all/total" (PROBABLE)
- KI-RO = Semitic "deficit" (PROBABLE)
- Low /o/ frequency (2.9%) argues against Proto-Greek
- Libation formulas show Luwian particles

**File**: [analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md](../analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md)

---

### Proto-Greek Hypothesis Downgraded to WEAK

**Previous status**: Neutral/open

**New status**: WEAK

**Evidence against**:
1. Low /o/ frequency (2.9% vs. Greek higher)
2. KU-RO ≠ Linear B *to-so* for "total"
3. Absence of clear Greek morphology (-os, -on, -ōn)
4. Only pa-i-to confirmed (likely Pre-Greek substrate origin)

**Methodological note**: This follows P2 (Ventris Lesson) - abandon hypotheses when evidence contradicts

**File**: [analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md](../analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md)

---

### Only One Level 1 Anchor Confirmed

**Finding**: pa-i-to = Phaistos is the ONLY confirmed Level 1 (toponym) anchor

**Implications**:
- All other readings are Level 2-6 (HIGH to SPECULATIVE)
- Anchor hierarchy essential to prevent overinterpretation
- Building systematically from this single certain point

**File**: [analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md](../analysis/completed/thematic/LINEAR_A_COMPREHENSIVE_ANALYSIS.md)

---

## How to Use This Log

1. **Add entries chronologically** (newest at top of each date section)
2. **Include**: Previous interpretation, new interpretation, evidence, implications
3. **Cross-reference**: Link to analysis files
4. **Note confidence levels**: CERTAIN, PROBABLE, POSSIBLE, SPECULATIVE
5. **Document reversals**: When abandoning a hypothesis, explain why

---

## Related Documents

- [ANALYSIS_INDEX.md](ANALYSIS_INDEX.md) - Central registry
- [CONFIRMED_READINGS.md](CONFIRMED_READINGS.md) - Secure interpretations
- [STATE_OF_KNOWLEDGE.md](STATE_OF_KNOWLEDGE.md) - Current synthesis
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Methodology refinements

---

*Journal maintained as part of the Linear A Decipherment Project knowledge management system.*
