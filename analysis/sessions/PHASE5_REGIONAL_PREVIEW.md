# OPERATION MINOS Phase 5 Preview: Regional Vocabulary Analysis

**Date**: 2026-01-31
**Objective**: Investigate vocabulary standardization vs. regional variation across major Linear A sites
**Status**: COMPLETE

---

## Executive Summary

This analysis investigates the remarkably low vocabulary overlap (Jaccard < 0.03) found in Phase 1 between major Linear A sites. The key finding is a **two-tier vocabulary system**:

1. **Universal logograms** (commodities, measures) appear across all sites
2. **Administrative syllabic terms** (KU-RO, KI-RO, SA-RA2) are heavily concentrated at Hagia Triada

This pattern suggests either (a) HT served as a central administrative hub with specialized accounting terminology, or (b) the HT corpus size creates sampling artifacts.

---

## Site Overview

| Site | Code | Tablets | Unique Words | Syllabic Words | Top Administrative Terms |
|------|------|---------|--------------|----------------|-------------------------|
| Hagia Triada | HT | 147 | 633 | 458 | KU-RO (35), SA-RA2 (20), KI-RO (16) |
| Khania | KH | 99 | 202 | 97 | CYP (36), *411-VS (15), CYP+D (17) |
| Zakros | ZA | 31 | 163 | 117 | GRA+PA (9), VIN (6), OLIV (5) |
| Phaistos | PH | 26 | 108 | 56 | VIN (5), *21M (4), TE (3) |

---

## Finding 1: No Words Appear at ALL Four Sites

**Summary**: Zero syllabic words are attested across all four major sites (HT, KH, ZA, PH).

**Evidence**:
- The `shared_vocabulary.all_sites` array in regional_analysis.json is empty
- Only 2 words appear at 3 sites: KU-RO and KU-PA
- Maximum Jaccard similarity between any pair: 0.0231 (HT-ZA)
- Minimum: 0.0058 (ZA-PH)

**Confidence**: CERTAIN (direct corpus data)

**Implications**:
- Linear A administrative vocabulary was NOT fully standardized across Crete
- Each site may have developed independent scribal traditions
- Alternatively, corpus damage/preservation may skew results

---

## Finding 2: KU-RO Distribution is Highly Uneven

**Summary**: KU-RO (the "total" marker) appears 37 times in the corpus, but distribution is HT-dominated.

**Distribution by Site**:
| Site | KU-RO Count | Percentage |
|------|-------------|------------|
| HT | 35 | 94.6% |
| ZA | 1 | 2.7% |
| PH | 1 | 2.7% |
| KH | 0 | 0% |

**Evidence**:
- corpus_lookup.py "KU-RO" shows 35 of 37 occurrences at HT
- Attested tablets: HT9a, HT9b, HT11a, HT11b, HT13, HT25b (x2), HT27a, HT39, HT40, HT46a, HT67, HT74, HT85a, HT88, HT89, HT94a, HT94b, HT100, HT102, HT104, HT109, HT110a, HT116b, HT117a, HT118, HT119, HT122a, HT122b, HT123+124a, plus 7 more
- ZA and PH each have exactly 1 occurrence
- KH has ZERO occurrences

**Confidence**: HIGH

**Implications**:
1. Either KU-RO was an HT-specific accounting term
2. Or HT produced the most "total"-containing documents (summaries, archives)
3. KH may have used a different totaling system or word

---

## Finding 3: KI-RO is Exclusive to Hagia Triada

**Summary**: KI-RO (the "deficit/partial" marker) appears ONLY at Hagia Triada.

**Distribution**:
| Site | KI-RO Count |
|------|-------------|
| HT | 16 |
| ZA | 0 |
| PH | 0 |
| KH | 0 |

**Evidence**:
- All 16 occurrences are at HT
- Tablets: HT1, HT15, HT30, HT34, HT37, HT55a, HT88, HT93b, HT94b, HT117a, HT123+124a (x5), HT123+124b

**Confidence**: HIGH

**Implications**:
- KI-RO appears to be an HT-specific accounting term
- The KU-RO/KI-RO paradigm (total/deficit) may be unique to HT scribal practice
- Other sites may have expressed deficits differently or not tracked them

---

## Finding 4: SA-RA2 is Exclusive to Hagia Triada

**Summary**: SA-RA2 (proposed meaning: "allocation" from Akkadian *saraku*) appears ONLY at HT.

**Distribution**:
| Site | SA-RA2 Count |
|------|--------------|
| HT | 20 |
| ZA | 0 |
| PH | 0 |
| KH | 0 |

**Evidence**:
- All 20 occurrences at HT
- Tablets: HT18, HT28a, HT28b, HT30, HT32, HT33, HT34, HT90, HT93a, HT94a, HT97b, HT99a, HT100, HT101, HT102, HT105, HT114a, HT121, HT125a, HT130

**Confidence**: HIGH

**Implications**:
- SA-RA2 was either an HT-specific term or appears in document types preserved only at HT
- The Akkadian *saraku* ("to grant, allocate") hypothesis remains viable but limited to one site

---

## Finding 5: Logograms Show Wider Distribution

**Summary**: Commodity logograms (GRA, VIN, OLE, OLIV) appear across multiple sites, unlike syllabic terms.

**Logogram Distribution** (from regional_analysis.json top_words):

| Logogram | HT | KH | ZA | PH | Sites |
|----------|----|----|----|----|-------|
| GRA | 45 | 8 | 3 | - | 3 |
| VIN | 28 | 7 | 6 | 5 | 4 |
| OLIV | 17 | - | 5 | - | 2 |
| OLE+U | 19 | - | - | - | 1 |
| CYP | - | 36 | - | - | 1 |

**Evidence**:
- VIN (wine) appears at all 4 sites - the only consistent term
- GRA (grain) at 3 sites (HT, KH, ZA)
- CYP dominates at KH (36 occurrences) but rare elsewhere

**Confidence**: HIGH

**Implications**:
1. Commodity logograms were likely inherited from a common tradition (possibly Cretan Hieroglyphic)
2. Syllabic accounting terms developed regionally
3. KH specialization in CYP may indicate copper/bronze trade focus

---

## Finding 6: KU-PA Shows Cross-Site Use

**Summary**: KU-PA is one of only 2 words appearing at 3 sites.

**Distribution**:
| Site | Tablets |
|------|---------|
| HT | HT110a |
| KH | KH29 |
| ZA | ZA11a, ZA11b |

**Evidence**:
- 4 total occurrences across 3 sites
- Unlike KU-RO/KI-RO/SA-RA2, KU-PA has cross-site attestation
- Context appears administrative (numbers follow in all cases)

**Confidence**: HIGH

**Implications**:
- KU-PA may be a more standardized term than KU-RO
- Or may represent a personal name (distributed via trade networks)

---

## Finding 7: Site-Specific Vocabulary Clusters

**Summary**: Each site has distinctive vocabulary not found elsewhere.

### HT-Specific Terms (86 words)
| Term | Count | Notes |
|------|-------|-------|
| SA-RA2 | 20 | Allocation marker |
| KI-RO | 16 | Deficit marker |
| I-RA2 | 8 | Unknown function |
| KA-PA | 6 | Possibly toponym |
| SA-RU | 6 | Unknown |
| SI-KA | 6 | Unknown |
| DI-NA-U | 5 | Possibly anthroponym |
| KU-NI-SU | 5 | Possibly anthroponym |

### KH-Specific Terms (6 words)
| Term | Count | Notes |
|------|-------|-------|
| *411-VS | 15 | Ligature/unclear |
| *86-RO | 4 | Ligature/unclear |
| *409-VS | 4 | Ligature/unclear |
| *408-VS | 4 | Ligature/unclear |

### ZA-Specific Terms (10 words)
| Term | Count | Notes |
|------|-------|-------|
| *28B-NU-MA-RE | 3 | Ligature + syllabic |
| SI-PI-KI | 3 | Unknown |
| DU-RE-ZA-SE | 3 | Possibly toponym (ZA = site?) |
| QE-SI-ZU-E | 2 | Unknown |

### PH-Specific Terms (1 word)
| Term | Count | Notes |
|------|-------|-------|
| AU-SI-RE | 2 | Unknown |

**Confidence**: HIGH

---

## Key Comparisons: Pairwise Vocabulary Overlap

| Pair | Shared Words | Jaccard | Notable Shared Terms |
|------|--------------|---------|---------------------|
| HT-ZA | 13 | 0.0231 | KU-RO, KU-PA, A-RI-NI-TA, PA-JA-RE |
| HT-KH | 10 | 0.0183 | A-DU, DA-RE, QA-NU-MA |
| HT-PH | 6 | 0.0118 | KU-RO, KU-PA3-NU, MA-DI, A-RI |
| KH-ZA | 2 | 0.0094 | KU-PA, *21F-*118 |
| KH-PH | 1 | 0.0066 | A-MI |
| ZA-PH | 1 | 0.0058 | KU-RO |

---

## Research Questions Investigated

### Q1: Are administrative terms (KU-RO, KI-RO, SA-RA2) standardized across sites?

**Answer**: NO. These terms are overwhelmingly HT-specific.

| Term | HT | Other Sites | Standardized? |
|------|----|-----------|----|
| KU-RO | 35 | 2 | NO |
| KI-RO | 16 | 0 | NO |
| SA-RA2 | 20 | 0 | NO |

### Q2: Do different sites use different accounting terms?

**Answer**: PROBABLE.

- HT uses KU-RO/KI-RO paradigm for totals/deficits
- KH may use different terms (no KU-RO/KI-RO attestations despite 99 tablets)
- The absence at KH is especially striking given corpus size

### Q3: Is there evidence for scribal schools or regional dialects?

**Answer**: SUGGESTIVE but not conclusive.

**Evidence FOR regional variation**:
1. KU-RO/KI-RO exclusive to HT suggests HT scribal training
2. KH heavy use of CYP suggests different economic focus
3. Site-specific vocabulary clusters suggest local terminology

**Evidence AGAINST (or complicating)**:
1. HT corpus is 3-5x larger, potentially creating sampling artifacts
2. Commodity logograms (VIN, GRA) do cross sites
3. Low overlap could reflect functional specialization, not dialect

---

## Negative Evidence Analysis (First Principle #5)

### What is ABSENT that we might expect?

1. **No universal accounting terminology**: If Linear A had a "standard accounting vocabulary," we would expect core terms at all sites. KU-RO/KI-RO absence at KH (with 99 tablets) suggests:
   - Either KH used different terms for totaling
   - Or KH tablets are functional different (not summary documents)

2. **No shared personal names across sites**: The shared vocabulary lists contain no obvious anthroponyms appearing at multiple sites. This suggests:
   - Either scribal networks were local
   - Or personal names are not preserved/identifiable

3. **No SA-RA2 outside HT**: If SA-RA2 = "allocation" (a core economic concept), its absence elsewhere is puzzling unless:
   - HT had unique allocation practices
   - The term is more specialized than "allocation"

---

## Hypotheses for Low Standardization

### Hypothesis A: HT as Central Archive
HT may have functioned as a central administrative hub that collected summary documents from other sites. This would explain:
- Why KU-RO (totals) dominates at HT
- Why KI-RO (deficits) appears only at HT
- Why SA-RA2 (allocations) is HT-exclusive

### Hypothesis B: Functional Differentiation
Different sites produced different document types:
- HT: Summary accounts, allocations, balance sheets
- KH: Commodity transactions (CYP-heavy)
- ZA: Agricultural records (GRA+PA)
- PH: Earlier period, different practices

### Hypothesis C: Regional Dialects
Each site developed independent scribal traditions with local terminology. The Jaccard < 0.03 may reflect genuine dialectal variation in Minoan.

### Hypothesis D: Preservation Bias
The extremely low overlap may partly reflect:
- Random preservation (90%+ of tablets lost)
- Document type preservation bias
- Differential destruction patterns

---

## Implications for Linear A Decipherment

### Methodological Caution
1. **KU-RO readings may be HT-biased**: The understanding of KU-RO = "total" is based almost entirely on HT data
2. **KI-RO readings are entirely HT-based**: No external verification possible
3. **SA-RA2 interpretation limited**: Akkadian hypothesis cannot be tested cross-site

### Cross-Corpus Verification (First Principle #6)
When testing new readings:
- Check if term appears at multiple sites before claiming standardized meaning
- Note when readings are HT-only
- Consider site-specific interpretation for HT-exclusive terms

### Anchor Hierarchy Implications
- Level 2 anchors (KU-RO, KI-RO) may need site qualifiers
- Level 6 lexical matches (SA-RA2) limited to HT contexts

---

## Recommended Follow-Up Analyses

1. **KH Alternative Analysis**: What terms does KH use where HT uses KU-RO?
2. **Document Type Classification**: Are HT tablets functionally different (summaries vs. daily records)?
3. **Temporal Analysis**: Are there chronological patterns in site vocabulary?
4. **Logogram-Only Comparison**: Do logograms show higher standardization than syllabic terms?
5. **Anthroponym Analysis**: Do personal names cross site boundaries?

---

## First Principles Verification

| Principle | Status | Notes |
|-----------|--------|-------|
| P1 (Kober): Patterns before language | PASS | Analysis based on distribution patterns, not language assumptions |
| P2 (Ventris): Abandon contradicted hypotheses | PASS | No prior hypothesis forced |
| P3 (Anchors): Build from certain to speculative | PASS | Used Level 2-3 anchors (KU-RO, logograms) |
| P4 (Multi-Hyp): Test all four frameworks | N/A | Not proposing new readings |
| P5 (Negative): Consider absent patterns | PASS | Documented absences at KH, ZA, PH |
| P6 (Corpus): Verify across corpus | PASS | Core purpose of this analysis |

**Overall Compliance**: FULL PASS (for distributional analysis)

---

## Methods Used

### Tools
- [x] corpus_lookup.py (KU-RO, KI-RO, SA-RA2, KU-PA, A-DU distributions)
- [x] regional_analysis.json (pre-computed site comparisons)

### Data Sources
- [x] data/corpus.json (raw inscription data)
- [x] data/regional_analysis.json (site vocabulary analysis)

### Inscriptions Referenced
- HT corpus (147 tablets)
- KH corpus (99 tablets)
- ZA corpus (31 tablets)
- PH corpus (26 tablets)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Sites analyzed | 4 |
| Total unique words compared | 1,106 |
| Words at ALL sites | 0 |
| Words at 3 sites | 2 |
| Maximum Jaccard similarity | 0.0231 |
| Minimum Jaccard similarity | 0.0058 |
| KU-RO concentration at HT | 94.6% |
| KI-RO concentration at HT | 100% |
| SA-RA2 concentration at HT | 100% |

---

## Conclusion

The Linear A corpus shows remarkably low vocabulary standardization across major sites. Core administrative terms (KU-RO, KI-RO, SA-RA2) that underpin current decipherment hypotheses are almost exclusively attested at Hagia Triada. This raises important methodological questions:

1. Are HT-based readings applicable corpus-wide?
2. Should site-specific interpretations be developed?
3. What alternative systems did KH, ZA, and PH use?

The pattern suggests either strong regional scribal traditions, functional differentiation between sites, or significant preservation bias. Future decipherment work should explicitly note when readings are based on single-site evidence.

---

**Session Date**: 2026-01-31
**Status**: COMPLETE
**First Principles Compliance**: FULL PASS

---

*Session log for OPERATION MINOS Phase 5 Preview - Linear A Decipherment Project*
