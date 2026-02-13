# Contributing to Linear A Decipherment Research

Thank you for your interest in contributing to this research project. Linear A remains one of the last undeciphered scripts of the ancient Mediterranean, and collaborative effort following rigorous methodology is essential.

## First Principles Requirement

**All contributions MUST comply with the Six First Principles.**

Before contributing, read and understand:
- `linear-a-decipherer/METHODOLOGY.md` (MANDATORY - six principles, checklists)
- `linear-a-decipherer/MASTER_STATE.md` (canonical current operational status)
- `linear-a-decipherer/KNOWLEDGE.md` (reference tables and synthesis details)

### The Six First Principles

| # | Principle | Requirement |
|---|-----------|-------------|
| 1 | **KOBER** | Let data lead; never start with language assumptions |
| 2 | **VENTRIS** | Abandon theories when evidence contradicts |
| 3 | **ANCHORS** | Build from certain to speculative (follow hierarchy) |
| 4 | **MULTI-HYP** | Test ALL four linguistic hypotheses |
| 5 | **NEGATIVE** | Consider what's absent, not just present |
| 6 | **CORPUS** | Verify readings across entire corpus |

**Contributions violating any principle will be rejected.**

---

## Types of Contributions

### 1. New Corpus Data

Adding transliterations, images, or references for inscriptions.

**Requirements**:
- Cite primary source (GORILA reference, publication, database URL)
- Use standard AB# notation for sign numbers
- Note any damage or uncertainty
- Place in `analyses/` with date-stamped filename

**Issue Template**: Use "New Corpus Data" template

### 2. Pattern Observations

Proposing new distributional patterns (frequency, position, co-occurrence).

**Requirements**:
- Document corpus coverage (which tablets examined)
- Provide statistical evidence where possible
- Follow Kober Method (frequency → position → distribution)
- Do NOT claim linguistic interpretation without multi-hypothesis testing

**Issue Template**: Use "Pattern Observation" template

### 3. Proposed Readings

Suggesting interpretations for sign sequences.

**Requirements**:
- Start with anchor verification (what level?)
- Test against ALL FOUR hypotheses (Luwian, Semitic, Pre-Greek, Proto-Greek)
- Document complete evidence chain
- Calibrate confidence appropriately
- Verify across ALL corpus occurrences
- Complete First Principles verification checklist

**Issue Template**: Use "Proposed Reading" template

### 4. Source Additions

Adding academic papers, database links, or reference materials.

**Requirements**:
- Verify source accessibility
- Summarize relevance to decipherment
- Note any methodological concerns
- Add to appropriate reference file

---

## Contribution Process

### Step 1: Open an Issue First

Before any pull request, open an issue using the appropriate template:
- Describe what you're proposing
- Wait for maintainer feedback
- Discuss methodology concerns

### Step 2: Fork and Branch

```bash
git clone https://github.com/levelheads/linear-a-decipherer.git
git checkout -b your-contribution-name
```

### Step 3: Make Changes

- Follow existing file formats
- Include First Principles verification in any analysis
- Date-stamp new analysis files (YYYY-MM-DD)

### Step 4: Submit Pull Request

- Reference the issue number
- Complete the PR checklist
- Await review

---

## Code of Conduct

### Epistemic Standards

1. **Humility**: Linear A is undeciphered. No one has "the answer."
2. **Evidence-based**: All claims require explicit evidence chains.
3. **Falsifiability**: State what would disprove your hypothesis.
4. **Revision**: Be willing to abandon contradicted theories.

### Interaction Standards

1. Critique ideas, not people
2. Assume good faith
3. Acknowledge uncertainty
4. Credit prior work appropriately

---

## What NOT to Contribute

The following will be rejected:

- Claims of "definitive" decipherment
- Single-hypothesis analyses (must test all four)
- Readings without corpus verification
- Speculation without evidence chains
- Commercial or promotional content
- AI-generated content without human verification

---

## Confidence Calibration

All proposed readings must include calibrated confidence:

| Level | Requirements |
|-------|-------------|
| CERTAIN | Multiple independent anchors; cross-corpus consistency; no contradictions |
| PROBABLE | Strong distributional evidence; fits multiple hypotheses |
| POSSIBLE | Some supporting evidence; alternatives exist |
| SPECULATIVE | Limited evidence; novel proposal |
| UNKNOWN | Insufficient data |

**Automatic Downgrades**:
- Hapax legomenon → Max: POSSIBLE
- Single-hypothesis support → Max: PROBABLE
- Damaged signs → Reduce one level

---

## Questions?

Open a Discussion or Issue with the "Question" label.

Remember: Every contribution should move us closer to understanding, not further into speculation.

---

*"Anyone who took a theory about the language as their starting point was doomed to failure."* — Alice Kober
