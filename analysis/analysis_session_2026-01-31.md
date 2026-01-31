# Linear A Analysis Session: 2026-01-31

## Overview

Three focused investigations completed following Challenge 3 (Slot Grammar Analysis):

1. **SA-RA₂ Deep-Dive** - Most frequent pre-logogram word
2. **KU-RO / KI-RO Co-occurrence Analysis** - 5 inscriptions with both forms
3. **Semitic -U Ending Signal** - Vowel-based hypothesis discrimination

---

## 1. SA-RA₂ Analysis

### Distribution (20 occurrences)

All occurrences are at Hagia Triada (HT), LMIB period.

| Inscription | Context | Commodity | Quantity |
|-------------|---------|-----------|----------|
| HT18 | *304 3 → **SA-RA₂** GRA 10 | Grain | 10 |
| HT28a | OLE+TU → **SA-RA₂** OLE+DI 1 | Oil | 1 |
| HT28b | U-MI-NA-SI → **SA-RA₂** GRA 20 | Grain | 20 |
| HT30 | SI 4 → **SA-RA₂** CYP 14 | Copper? | 14 |
| HT90 | I-KU-RI-NA → **SA-RA₂** GRA 20 | Grain | 20 |
| HT93a | 26¾ → **SA-RA₂** 20 → QA-QA-RU | - | 20 |
| HT94a | KU-RO 110 → **SA-RA₂** CYP 5 | Copper? | 5 |
| HT99a | A-DU → **SA-RA₂** CYP 4 | Copper? | 4 |
| HT100 | KU-RO 97 → **SA-RA₂** CYP 5¼ | Copper? | 5¼ |
| HT101 | OLE+KI 2 → **SA-RA₂** GRA 41 | Grain | 41 |
| HT102 | KA-PA → **SA-RA₂** GRA 976 | Grain | 976 |
| HT114a | KI-RI-TA₂ → **SA-RA₂** GRA 10 | Grain | 10 |
| HT121 | OLE+QE+DI 10 → **SA-RA₂** GRA 5 | Grain | 5 |
| HT125a | 1½ → **SA-RA₂** GRA 2 | Grain | 2 |
| HT130 | SI 3 → **SA-RA₂** CYP | Copper? | - |

### Pattern Analysis

1. **Position**: Always immediately precedes commodity logogram
2. **Commodities**: Appears with GRA (grain, 9x), CYP (copper?, 5x), OLE (oil, 2x)
3. **Context**: Often follows totals (KU-RO) or other commodity entries
4. **Numerals**: Associated quantities range from 1 to 976

### Hypothesis Testing

| Hypothesis | Score | Interpretation |
|------------|-------|----------------|
| **Semitic** | 1.3 (best) | Cognate with Akkadian *še'u* "barley" or *šarru* "king" |
| Luwian | 1.0 | Possible coordinative conjunction |
| Pre-Greek | 1.0 | No specific match |
| Proto-Greek | 0 | No match |

### Functional Hypothesis

SA-RA₂ appears to function as a **transaction category marker** or **commodity type qualifier**:

- **Option A**: "Allocation/portion of [commodity]" (administrative term)
- **Option B**: "Barley-type" classifier (if Semitic *še'u* cognate)
- **Option C**: "Royal/palace [commodity]" (if Semitic *šarru* cognate)

**Confidence**: POSSIBLE (Level 4-5 anchor, structural position known, semantics uncertain)

---

## 2. KU-RO / KI-RO Co-occurrence Analysis

### The 5 Key Inscriptions

#### HT123+124a (Most Complex)
```
KI-TA-I OLIV 31 → *308 8¼ → KI-RO 1.3
PU-VIN OLIV 31½ → *308 8¾ → KI-RO .3
SA-RU OLIV 16 → *308 4≈⅙ → KI-RO ¾
DA-TU OLIV 15 → *308 4¼ → KI-RO ¾
KU-RO OLIV 93½ → *308 → KU-RO 25≈⅙ → KI-RO 6
```
**Structure**: Entry blocks each ending with KI-RO (fractional amounts), grand total with KU-RO

#### HT117a
```
MA-KA-RI-TE → KI-RO → U-MI-NA-SI
[10 names, each "1"]
KU-RO 10
```
**Structure**: KI-RO as header/category marker, KU-RO sums the list (10 = sum of 10×1)

#### HT88
```
A-DU VIR+KA 20 → RE-ZA 6 → NI KI-KI-NA 7
KI-RO
[6 names, each "1"]
KU-RO 6
```
**Structure**: Commodity entries → KI-RO (break marker) → Name list → KU-RO (sum)

#### HT94b
```
KI-RO
[5 names, each "1"]
KU-RO 5
```
**Structure**: KI-RO as header, KU-RO sums the list (5 = sum of 5×1)

#### HT123+124b
```
[Various entries]
KU-RO 20
KI-RO 5
```
**Structure**: KU-RO (total), KI-RO (remainder/deficit)

### Functional Synthesis

| Form | Function | Evidence |
|------|----------|----------|
| **KU-RO** | TOTAL/SUM | Numerical values consistently equal sum of preceding entries |
| **KI-RO** | DEFICIT/REMAINDER/SUBTOTAL | Appears as fractional amounts, header markers, or post-total remainders |

### Relationship Model

```
KU-RO = Σ (all entries) = GRAND TOTAL
KI-RO = partial amount OR amount outstanding

When both appear:
- KI-RO before list = "owed/outstanding category"
- KI-RO after KU-RO = "remaining/deficit from total"
- KI-RO within blocks = "partial/fractional allocation"
```

**Key Insight**: KI-RO and KU-RO are NOT in complementary distribution (they co-occur), but they serve different accounting functions within the same document.

**Confidence**: HIGH (Level 2 anchor - Linear B cognate + consistent position)

---

## 3. Semitic -U Ending Signal

### Vowel-Based Discrimination Pattern

The slot grammar analysis revealed a striking pattern:

| Final Vowel | Favors | Word Count | Example Suffixes |
|-------------|--------|------------|------------------|
| **-U** | Semitic | 39 | -U, -DU, -RU, -SU, -NU, -JU, -TU |
| **-E/-O** | Proto-Greek | 65+ | -E, -O, -RO, -RE, -SE, -NE, -ME, -TO |
| -A | Neutral | Many | -RA, -NA, -TA (both hypotheses) |
| -I | Luwian (weak) | Some | -RI, -TI, -DI |

### Interpretation

This pattern has two possible explanations:

**Explanation A: Language Mixture**
Linear A may encode a **mixed linguistic substrate** where:
- U-final words derive from Semitic loanwords or a Semitic administrative vocabulary
- E/O-final words derive from an Aegean (Proto-Greek or Pre-Greek) substrate
- A-final words are shared or neutral

**Explanation B: Morphological Differentiation**
In a single language, vowel quality may mark **grammatical distinctions**:
- -U: nominative/agentive (Semitic pattern)
- -O: genitive/possessive (Greek pattern)
- -E: dative/locative (Greek pattern)

### Evidence for Explanation A (Mixture)

1. Administrative texts worldwide show loanword adoption
2. Minoan trade contacts with Levant documented archaeologically
3. Some words (like KU-RO, KI-RO) may be Semitic accounting terms adopted into Minoan

### Evidence for Explanation B (Single Language)

1. Consistent morphological patterns across corpus
2. No clear geographic/temporal split between U-words and E/O-words
3. Both types appear in same inscriptions

**Current Assessment**: Insufficient evidence to distinguish. Both remain viable.

**Confidence**: LOW-MEDIUM (interesting pattern, interpretation uncertain)

---

## Cross-Analysis Synthesis

### Converging Evidence

1. **SA-RA₂** (Semitic-leaning) appears in administrative commodity contexts
2. **KU-RO** contains -U ending, functions as "total" (possibly Semitic *kull-* "all"?)
3. **KI-RO** contains -O ending, functions differently (partial/deficit)

### Provocative Observation

If KU-RO derives from Semitic *kull-u* "totality/all" and KI-RO from a different root, the vowel alternation U→O might signal:
- Different etymologies (two distinct words)
- OR grammatical alternation within one paradigm

The K-R paradigm shows:
- KU-RO (37x): totaling
- KI-RO (16x): deficit/partial
- KU-RE, KI-RA, KU-RA, KI-RU: rare variants (1-2x each)

This suggests **vowel gradation** (U/I alternation in first syllable, O/A/E/U in second) rather than simple inflection.

---

## First Principles Verification

| Principle | Status | Notes |
|-----------|--------|-------|
| P1 (Kober) | PASS | Analysis followed pattern → hypothesis, not reverse |
| P2 (Ventris) | PASS | Multiple interpretations considered |
| P3 (Anchors) | PASS | Built from KU-RO/KI-RO (L2) and logograms (L3) |
| P4 (Multi-Hyp) | PASS | All four hypotheses tested |
| P5 (Negative) | PASS | Noted absence of clear KI-RO "deficit" marking in some contexts |
| P6 (Corpus) | PASS | Patterns verified across multiple inscriptions |

---

## Recommended Next Steps

### Immediate
1. **Test SA-RA₂ Semitic hypothesis** against Akkadian administrative vocabulary
2. **Map KI-RO positions** more precisely (header vs. line-final vs. post-total)
3. **Correlate -U words with specific commodity types**

### Medium-Term
4. **Challenge 4: Libation Formula Analysis** - Apply same methodology to religious texts
5. **Chronological analysis** - Check if vowel patterns change over MMII→LMIB span

### Data Collection
6. Fetch comparative Akkadian/Ugaritic administrative terminology
7. Compile all K-R paradigm forms with full contexts

---

## Session Metadata

- **Date**: 2026-01-31
- **Tools Used**: hypothesis_tester.py, corpus_lookup.py, analyze_inscription.py, kr_paradigm_validator.py, slot_grammar_analyzer.py
- **Inscriptions Analyzed**: HT123+124a, HT123+124b, HT117a, HT88, HT94b, plus 20 SA-RA₂ occurrences
- **Commit**: 9d44771 (Challenge 3 implementation)
