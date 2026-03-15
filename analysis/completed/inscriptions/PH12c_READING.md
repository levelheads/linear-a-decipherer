# PH 12c Connected Reading Report

**Date**: 2026-03-15
**Analyst**: Codex (GPT-5)
**Phase**: Month 1 Week 2 - Balanced Admin Push
**Status**: COMPLETE
**Confidence**: HIGH

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
| **Tablet ID** | PH 12c |
| **Site** | Phaistos |
| **Period** | Unspecified in corpus metadata |
| **Scribe** | Unknown |
| **Support** | Lames (short thin tablet) |
| **Document Type** | Administrative header fragment |
| **Arithmetic Status** | NO_KURO |
| **Corpus Source** | `data/corpus.json`, `tools/corpus_auditor.py --function-word TE` |
| **Reading Readiness** | Score 0.550 |
| **Cross-Site Significance** | Confirms TE as a standalone line-initial header/topic marker at Phaistos |

---

## Transliteration

```
TE
```

### Sign Number Assignments

| Sign | AB Number | Confidence | Corpus Frequency |
|------|-----------|------------|------------------|
| TE | AB 04 | CERTAIN | High |

---

## Anchor Identification

### Level 1: Toponyms (CERTAIN)

**None.**

### Level 2: Linear B Cognates + Position (HIGH)

**None directly.** The value of PH 12c is structural rather than lexical-comparative.

### Level 4: Structural Patterns (HIGH)

| Pattern | Interpretation | Evidence |
|---------|----------------|----------|
| Standalone line-initial `TE` | Header/topic marker | Corpus auditor: 58 occurrences, 67.2% initial |
| PH parallels | Same function at Phaistos | `PH27` has `TE` followed by `A`; `PHWb36` has standalone `TE` |

---

## Structural Analysis

### Document Type

**Single-sign administrative header fragment**

PH 12c does not offer a sentence translation. Its importance is that it preserves **only** the sign **TE**, in exactly the position where the wider corpus predicts a header/topic marker. This makes PH 12c a useful control tablet for the function of TE.

### Rosetta Skeleton

| Position | Term | Role | Confidence |
|----------|------|------|------------|
| 1 | TE | Header/topic marker | HIGH |

### Arithmetic Verification

Not applicable beyond confirming `NO_KURO`. There are no numerals and no totaling logic.

### Notable Structural Features

1. **Minimal but clean**: PH 12c contains only `TE`, so the tablet isolates the function word without interference from surrounding content.
2. **Cross-site support is strong**: TE occurs across HT, HTW, KN, PH, ZA, AN, ARKH, and other corpora.
3. **Phaistos-local confirmation**: PH 27 (`TE | A`) and PHWb36 (`TE`) show the same line-initial behavior.

---

## Connected Reading Attempt

### Conservative Interpretation

```
TE      [header / topic marker / entry introducer]      HIGH
```

### Full Interpretive Reading

> **[Header / entry marker]**

PH 12c is best translated functionally, not lexically. The tablet likely marks the beginning of an entry, topic, or section.

---

## What We Know For Certain

1. **TE is the entire inscription**.
2. **TE is overwhelmingly line-initial in the corpus**: 39 of 58 occurrences (67.2%).
3. **The corpus auditor's role hypothesis is header/topic marker**.
4. **Phaistos has parallel TE usage** in PH 27 and PHWb36.

## What We Hypothesize

1. **TE is a structural marker equivalent to "entry/header/topic"**, not a content word. HIGH.
2. **PH 12c is a fragment from a larger administrative sequence** rather than a complete self-standing message. PROBABLE.

---

## Cross-Corpus Verification

### TE Function-Word Audit

| Metric | Value |
|--------|-------|
| Total occurrences | 58 |
| Initial position | 39 (67.2%) |
| Medial position | 18 (31.0%) |
| Final position | 1 (1.7%) |
| Position entropy | 0.637 |
| Role hypothesis | Header/Topic marker (line-initial) |

### Phaistos Parallels

| Tablet | Pattern |
|--------|---------|
| PH 12c | `TE` |
| PH 27 | `TE | A` |
| PHWb36 | `TE` |

### Broader Structural Parallels

| Tablet | Pattern |
|--------|---------|
| HT 9a | `SA-RO | TE | VIN` |
| HT 92 | `TE` header on short admin tablet |
| Multiple HTW tablets | line-initial `TE` series |

**Verification**: PH 12c is a clean confirmation tablet for the current TE model. It does not invent a new interpretation; it validates the existing one in a minimal context.

---

## Promotion Recommendation

**Decision**: `MAINTAIN`

**Rationale**:
1. TE is already at **HIGH** as a header/topic marker.
2. PH 12c provides confirmatory evidence, not a new semantic leap.
3. No further promotion is warranted from a one-sign tablet.

---

## Final Assessment

PH 12c is a small but useful control reading. It confirms that **TE functions as a structural header/topic marker even when no following commodity or recipient survives**, which helps stabilize sentence segmentation across the administrative corpus.
