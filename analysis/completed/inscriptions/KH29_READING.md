# KH29 Connected Reading Report

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
```

---

## Source Information

| Attribute | Value |
|-----------|-------|
| **Tablet ID** | KH29 |
| **Site** | Khania (Kydonia) |
| **Period** | Late Minoan IB |
| **Support** | Tablet (clay) |
| **Document Type** | Copper allocation (CYP with fractions) |
| **Arithmetic Status** | NO_KURO |
| **Reading Readiness** | Score 0.363 |

---

## Transliteration

```
Line 1:  RA  𐄁  TA₂
Line 2:  1
Line 3:  KU-PA
Line 4:  2
Line 5:  CYP  ½
Line 6:  𐝫
Line 7:  𐝫
```

---

## Structural Analysis

### Document Structure

```
[H]  RA                        Header (single syllable)
     𐄁                         Word divider
[?]  TA₂                       Qualifier / category
---
[#]  1                         Quantity: 1 unit
---
[R]  KU-PA                     Recipient: KU-PA (STRONG GRA anchor)
---
[#]  2                         Quantity: 2 units
---
[C]  CYP                       Commodity: copper
[#]  ½                         Quantity: 0.5 (fraction = lower grade pattern)
---
[R]  𐝫                         [damaged]
---
[R]  𐝫                         [damaged]
```

### Notable Features

1. **KU-PA at Khania**: KU-PA is a STRONG commodity anchor for GRA (100% specificity, 3 sites). Here it appears at Khania on a CYP tablet. This does NOT break the anchor -- KU-PA appears as a recipient name, not with a GRA logogram. The GRA specificity applies when GRA is on the same line; KU-PA can appear as a name in non-GRA contexts.
2. **CYP ½**: Fractional copper, consistent with the CYP = fractions pattern (lower grade).
3. **Damaged entries**: Two damaged lines at the end.
4. **Zero K-R**: Consistent with Khania.
5. **RA header**: Single syllable. RA appears as a header element (cf. the +RA qualifier on VIN+RA at ZA15b).

---

## Multi-Hypothesis Testing

| Term | Best Hypothesis | Confidence | Note |
|------|-----------------|------------|------|
| RA | INDETERMINATE | UNKNOWN | Single syllable |
| TA₂ | INDETERMINATE | UNKNOWN | Single syllable |
| KU-PA | Luwian | PROBABLE | hypothesis_tester; STRONG GRA anchor (as name here) |
| CYP | N/A (logogram) | CERTAIN | Copper |

All seven hypotheses tested. Single syllables INDETERMINATE for all.

---

## Connected Reading Attempt

> **RA** [source/category], **TA₂** [qualifier]:
> 1 [unit]
>
> **KU-PA**: 2 [units]
>
> **Copper (CYP):** ½ unit (fractional = lower grade)
>
> [2 damaged entries]

---

## What We Know For Certain

1. **CYP with fraction (½)**: Consistent with CYP = fractional quantities pattern. CERTAIN.
2. **KU-PA present**: STRONG GRA anchor appearing as recipient at KH. CERTAIN.
3. **Zero K-R**: Confirmed for 8th KH tablet. CERTAIN.
4. **Partial damage**: Two entries lost. CERTAIN.

## What We Hypothesize

1. **KU-PA as personal name here**: Despite being a GRA anchor, KU-PA functions as a recipient name on this CYP tablet. Names can function in multiple commodity contexts. PROBABLE.
2. **RA-TA₂ as header pair**: Similar to ZA-SU on KH22 and KH11. Khania uses single-syllable header pairs. POSSIBLE.

---

## Novel Observations

### KU-PA in Non-GRA Context

KU-PA's appearance on a CYP tablet at Khania is important for anchor methodology. The STRONG anchor (100% GRA specificity) refers to cases where KU-PA appears WITH a commodity logogram on the same line. Here KU-PA appears as a recipient receiving a quantity, without GRA. The anchor is maintained because it tracks co-occurrence with commodity logograms, not mere presence on a tablet.

---

## Sources Consulted

1. **lineara.xyz corpus** -- KH29 transliteration
2. **arithmetic_verifier** -- Rosetta skeleton
3. **hypothesis_tester.py** -- KU-PA (Luwian PROBABLE)
4. **KNOWLEDGE.md** -- KU-PA anchor, CYP grading

---

*Connected reading completed 2026-02-22. KH29 is a partially damaged Khania CYP tablet with KU-PA as recipient. CYP ½ (fractional) confirms grading pattern. Zero K-R for 8th KH tablet. Overall reading confidence: HIGH for CYP system; UNKNOWN for header terms.*
