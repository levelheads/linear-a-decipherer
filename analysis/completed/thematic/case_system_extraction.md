# Case System Extraction from 55 Readings

**Date**: 2026-03-14
**Phase**: Operation VENTRIS Phase 1.3
**Status**: COMPLETED

---

## Methodology

Extracted all syllabic words across the full corpus (1,721 inscriptions) and tabulated their final-syllable distributions by grammatical position:

1. **RECIPIENT position**: Word immediately before LOGOGRAM + NUMBER sequence (e.g., `DA-SI-*118 VIR 24`)
2. **HEADER position**: First meaningful word on a tablet (source/authority role)
3. **TOTAL position**: Word immediately before KU-RO (totals context)

Tested the prediction from `administrative_grammar.md`: "If 30%+ of RECIPIENT-role words end in -SI, this strongly favors Luwian dative."

---

## Results: Final Syllable Distribution by Position

### Recipient Position (before LOGOGRAM + NUMBER)

| Suffix | Count | % of all | Interpretation |
|--------|-------|----------|----------------|
| -RA₂ | 17 | 40.5% | **Strongest recipient marker** (SA-RA₂ = allocation) |
| -TE | 11 | 9.6% | Moderate recipient presence |
| -NA | 7 | 10.4% | Moderate |
| -RO | 7 | 4.0% | Low (KU-RO in list-final, not recipient) |
| -SI | 5 | 3.2% | **Very low — NOT a dative marker** |
| -NI | 5 | 5.1% | NI = wine marker |
| -DI | 5 | 11.6% | Notable |
| -TA₂ | 6 | ? | Notable |
| -TU | 4 | ? | Moderate |
| -JA | 3 | 4.0% | Low |

### Header Position (first word on tablet)

| Suffix | Count | % of all | Interpretation |
|--------|-------|----------|----------------|
| -KA | 177 | 86.8% | **Dominant header suffix** |
| -KU | 161 | 87.5% | Very strong header suffix |
| -SI | 108 | 70.1% | **Strong header/verbal marker** |
| -RO | 103 | 59.5% | KU-RO in total/header positions |
| -TE | 51 | 44.7% | Strong header presence |
| -ZE | 46 | 97.9% | Nearly exclusively header |
| -JA | 37 | 49.3% | Strong header — adjectival/ethnic? |
| -VS | 26 | ? | Undeciphered sign sequences |
| -TA | 25 | 37.9% | Moderate header |
| -TI | 17 | 27.9% | Moderate |
| -NA | 18 | 26.9% | Moderate |

---

## Key Finding: -SI is NOT Dative

The central prediction of Luwian dative -SI was **DISCONFIRMED**:

- -SI appears in RECIPIENT position only **3.2%** of the time (5/154)
- -SI appears in HEADER position **70.1%** of the time (108/154)
- This is the **opposite** of what a dative marker would show

### Revised interpretation of -SI

-SI functions as a **verbal/agentive suffix** or **topic marker**, appearing predominantly in:
1. Header/authority positions (source, topic, authority)
2. The libation formula (U-NA-KA-NA-SI = verbal form)
3. Administrative verbs or agent nouns

This is consistent with:
- Luwian 3rd person singular verbal ending -si (verbal, not nominal dative)
- The TLZa1 evidence where U-NA-KA-NA (base) vs U-NA-KA-NA-SI (suffixed) in same formulaic position — suffix marks verbal inflection

---

## Emerging Case System

| Suffix | Primary Position | Proposed Function | Evidence Strength |
|--------|-----------------|-------------------|-------------------|
| -RA₂ | Recipient (40.5%) | **Allocation marker** | PROBABLE (SA-RA₂ confirmed) |
| -SI | Header (70.1%) | **Verbal/agentive** | PROBABLE (positional + morphological) |
| -TE | Mixed (header 44.7%, recip 9.6%) | **Ablative/source?** | POSSIBLE |
| -JA | Header (49.3%) | **Adjectival/ethnic** | PROBABLE (Palmer 1958) |
| -KA | Header (86.8%) | **Locative/institutional?** | POSSIBLE |
| -ZE | Header (97.9%) | **Site/context-specific** | SPECULATIVE |
| -TI | Mixed (27.9% header) | **Plural verbal?** | SPECULATIVE (Davis 2014) |
| -ME | Mixed (24.1% header) | **Nominal/divine** | PROBABLE (IOZa16 proof) |
| -DI | Recipient (11.6%) | **Object/accusative?** | SPECULATIVE |

---

## Implications

1. **Linear A is NOT a simple dative-marking language**: The recipient position is marked by allocation words (SA-RA₂) rather than case suffixes. The administrative register uses WORD ORDER + FUNCTION WORDS rather than inflectional case.

2. **-SI is verbal, not nominal**: This reinterprets many readings. Words ending in -SI (U-NA-KA-NA-SI, QE-SI-NE-SI, etc.) are likely verb forms, not dative nouns.

3. **Two-track grammar**: Administrative register uses function words (SA-RA₂, KU-RO) for grammatical roles, while religious register may use suffixal morphology (-SI verbal, -ME nominal). This supports domain-split grammar.

4. **-RA₂ as primary case marker**: SA-RA₂ may be the ONLY productive case-like marker, functioning as an allocation/dative function word rather than a bound morpheme.

---

## First Principles Verification

- [PASS] Kober: Data-led analysis of positional distributions
- [PASS] Ventris: Abandoned dative-SI hypothesis when data contradicted
- [PASS] Anchors: Built from SA-RA₂ (MEDIUM), -SI (PROBABLE), -ME (PROBABLE)
- [PASS] Multi-Hyp: Tested Luwian dative prediction explicitly
- [PASS] Negative: Documented absence of -SI in recipient position
- [PASS] Corpus: Analysis covers full corpus (1,721 inscriptions)
