# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

This repository contains a Linear A decipherment skill system designed to analyze undeciphered Minoan Bronze Age inscriptions (c.1800-1450 BCE) from Crete. The project uses a rigorous methodology derived from the successful Linear B decipherment to systematically analyze patterns, test competing linguistic hypotheses, and generate novel interpretations with calibrated confidence levels.

**Linear A remains undeciphered.** This system approaches it as an active research problem, not a solved puzzle.

---

## Critical First Steps

### MANDATORY: Read First Principles Before ANY Analysis

**Location**: `linear-a-decipherer/FIRST_PRINCIPLES.md`

This document contains six inviolable principles that govern all decipherment operations:

1. **KOBER PRINCIPLE** - Never start with language assumptions; let data lead
2. **VENTRIS LESSON** - Abandon theories when evidence contradicts
3. **ANCHOR-BASED EXPANSION** - Build from certain to speculative
4. **MULTI-HYPOTHESIS TESTING** - Test ALL four linguistic hypotheses (Luwian, Semitic, Pre-Greek, Proto-Greek)
5. **NEGATIVE EVIDENCE** - Consider what's absent, not just present
6. **CROSS-CORPUS CONSISTENCY** - Readings must work across entire corpus

**Violating any principle invalidates the analysis.** The First Principles document includes pre-flight checklists and post-analysis verification procedures that must be followed.

### Required Reading Order

1. `linear-a-decipherer/FIRST_PRINCIPLES.md` (MANDATORY)
2. `linear-a-decipherer/SKILL.md` (operational procedures)
3. `linear-a-decipherer/references/methodology.md` (techniques)
4. `linear-a-decipherer/references/hypotheses.md` (linguistic frameworks)
5. `linear-a-decipherer/references/corpus.md` (inscription database)
6. `linear-a-decipherer/references/sign_list.md` (syllabary)

---

## Architecture

### Core Design Pattern: Evidence-Based Reasoning Chain

The system does NOT function as a simple lookup tool. Instead, it:

1. **Acquires sources** - Fetches inscriptions from online databases (SigLA, academic repositories)
2. **Establishes anchors** - Identifies confirmed toponyms, Linear B cognates, logograms
3. **Analyzes patterns** - Uses Kober Method (frequency, position, inflection patterns)
4. **Tests hypotheses** - Generates readings under Luwian, Semitic, Pre-Greek, Proto-Greek frameworks
5. **Ranks interpretations** - Weights evidence chains and assigns calibrated confidence
6. **Verifies corpus-wide** - Tests proposed readings across all occurrences
7. **Documents reasoning** - Outputs complete evidence chains, not just conclusions

### The Anchor Hierarchy (STRICT ORDER)

| Level | Type | Example | Max Confidence |
|-------|------|---------|----------------|
| 1 | Confirmed toponyms | pa-i-to = Phaistos | CERTAIN |
| 2 | Linear B cognates + position | ku-ro at totals | HIGH |
| 3 | Clear logograms | VIN, OLE, GRA | HIGH |
| 4 | Structural patterns | Transaction signs | MEDIUM |
| 5 | Morphological patterns | -jo genitive? | LOW-MEDIUM |
| 6 | Lexical matches | ki-ro = deficit | LOW |

**Never skip anchor levels.** Confidence cannot exceed the anchor level reached.

### Four Mandatory Linguistic Hypotheses

EVERY proposed reading must be tested against:

1. **Luwian/Anatolian** (Palmer, Finkelberg)
2. **Semitic** - West Semitic/Akkadian (Gordon, Best)
3. **Pre-Greek Substrate** (Beekes, Furnée)
4. **Proto-Greek** (Georgiev, Mosenkis)

Single-hypothesis support caps confidence at PROBABLE. Multi-hypothesis convergence or overwhelming single-hypothesis evidence required for CERTAIN.

---

## Common Operations

### Analyzing a Linear A Inscription

**From tablet reference** (e.g., "HT 13", "ZA 4"):
1. Run pre-flight checklist (FIRST_PRINCIPLES.md)
2. Fetch inscription from SigLA database (https://sigla.phis.me)
3. Identify all available anchors before novel readings
4. Apply Kober Method: frequency → position → inflection patterns
5. Test against all four hypotheses with explicit reasoning chains
6. Verify readings across entire corpus
7. Generate structured report with confidence calibration
8. Run post-analysis verification (FIRST_PRINCIPLES.md)

**From image**:
1. Extract signs visually
2. Match against sign list (references/sign_list.md)
3. Assign AB numbers (GORILA classification)
4. Proceed as above

### Site Code Reference

| Code | Site | Key Information |
|------|------|----------------|
| HT | Hagia Triada | Largest corpus (147 tablets) |
| KH | Khania | 99 tablets |
| ZA | Zakros | 31 tablets |
| PH | Phaistos | Earliest inscriptions |
| KN | Knossos | Includes 2024 ivory scepter (119 signs) |

### Key Inscriptions to Reference

- **HT 13** - Classic commodity list with ku-ro total
- **KN Zf 2** - 2024 ivory scepter discovery (longest inscription ever found)
- **Libation formulas** - Religious texts from peak sanctuaries

---

## Methodological Constraints

### What to ALWAYS Do

- Start with frequency/positional analysis before language assumptions
- Document complete evidence chains for every claim
- Test alternative hypotheses explicitly
- Verify readings across all corpus occurrences
- Calibrate confidence to anchor level reached
- Acknowledge when no interpretation is possible

### What to NEVER Do

- Start by assuming a language ("what would this mean in Greek?")
- Ignore contradicting evidence to preserve a hypothesis
- Skip anchor levels (e.g., jump to lexical match without structural context)
- Claim CERTAIN confidence based on single-hypothesis fit
- Force evidence to fit preconceived theories
- Accumulate "special cases" or "exceptions" to save a reading
- Present only one linguistic analysis without testing others

### Red Flags (Stop and Reconsider)

- Requiring multiple exceptions to maintain a reading
- Semantic stretching to achieve desired meaning
- Citing sources not actually fetched
- Emotional attachment to particular interpretation
- Ignoring that expected patterns are missing
- Confidence claims exceeding evidence strength

---

## Confidence Calibration

### Automatic Downgrades

- Hapax legomenon (1 occurrence) → Max: POSSIBLE
- Damaged/uncertain signs → Reduce one level
- Single-hypothesis support → Max: PROBABLE
- Contradicts anchor → REJECT or flag for review

### Levels and Requirements

| Level | Requirements |
|-------|-------------|
| CERTAIN | Multiple independent anchors; cross-corpus consistency; no contradictions |
| PROBABLE | Strong distributional evidence; fits multiple hypotheses |
| POSSIBLE | Some supporting evidence; alternatives exist |
| SPECULATIVE | Limited evidence; novel proposal |
| UNKNOWN | Insufficient data |

---

## Output Format

All analyses should follow the structured report template in SKILL.md:

- Source information (site, reference, URL)
- Transliteration with sign numbers
- Linear B cognates
- Multi-hypothesis analysis (all four frameworks)
- Synthesis with novel interpretations
- Confidence assessment
- **First Principles verification** (PASS/FAIL/PARTIAL for each principle)
- Sources consulted

---

## Recent Developments

### Knossos Ivory Scepter (2024)

- **119 signs** - longest Linear A inscription ever found
- Two separate inscriptions by different scribes
- Ring: ceremonial/religious style
- Handle: administrative style with numerals
- Published in Ariadne Supplement 5 (2025)
- URL: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841

This discovery provides new sign sequences for pattern analysis and confirms dual use of Linear A (administrative + religious).

---

## Key Historical Context

### Why These Principles Exist

The First Principles derive from hard-won lessons:

- **Alice Kober (1906-1950)** established that pattern analysis must precede language assumptions. Her methodology enabled Linear B's decipherment.
- **Michael Ventris (1922-1956)** believed Linear B was Etruscan until overwhelming evidence proved otherwise. He succeeded because he followed methodology over preconception.

Linear A has resisted decipherment for over a century. Every previous attempt that violated these principles failed.

---

## Working Philosophy

**Epistemic Humility**: Linear A is undeciphered. All claims require evidence. All interpretations require calibrated confidence. The goal is not to "solve" Linear A in one session, but to incrementally build understanding through rigorous methodology.

**Active Reasoning**: Don't just look up—reason through the evidence. Generate novel interpretations, but ground them in explicit evidence chains.

**Multi-Hypothesis Thinking**: Competing linguistic theories each have partial successes and failures. Testing all four prevents premature convergence on wrong answers.

**Negative Evidence**: What's absent matters as much as what's present. If a hypothesis predicts patterns not found in the corpus, that's evidence against it.

---

## Error Recovery

| Situation | Action |
|-----------|--------|
| Source unavailable | Try alternatives; document gap |
| Conflicting readings | Present both; flag uncertainty |
| Sign unidentifiable | Mark [?]; note damage |
| No interpretation possible | State explicitly; don't force a reading |
| Potential breakthrough | Flag for significance; document thoroughly |

---

## Final Reminder

From FIRST_PRINCIPLES.md:

> "Linear A is undeciphered. Every claim requires evidence. Every interpretation requires humility. These principles exist because generations of scholars made the mistakes they prevent."

**When in doubt, return to the First Principles.**
