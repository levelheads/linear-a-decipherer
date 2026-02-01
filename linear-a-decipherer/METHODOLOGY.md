# Linear A Decipherment Methodology

**Inviolable principles and operational procedures for Linear A analysis**

---

## Part 1: The Six Principles

These principles govern ALL operations. They derive from the methodology that successfully deciphered Linear B.

**Violating any principle invalidates the analysis.**

### Principle 1: THE KOBER PRINCIPLE

**Never start with a language assumption—let the data lead.**

> "Anyone who took a theory about the language as their starting point was doomed to failure. The single route to the finishing line was to find the patterns and deep symmetries inside the primary texts." — Alice Kober

Requirements:
- Analyze frequency distributions BEFORE hypothesizing language
- Map positional patterns (initial, medial, final) BEFORE semantic interpretation
- Language hypotheses are tested AGAINST patterns, never assumed

Self-check: *"Am I following the patterns in the data, or am I assuming a language?"*

### Principle 2: THE VENTRIS LESSON

**Be willing to abandon theories when evidence contradicts them.**

Michael Ventris believed Linear B encoded Etruscan until overwhelming evidence proved otherwise. He succeeded because he followed methodology over preconception.

Requirements:
- Hold ALL interpretations provisionally
- Treat contradicting evidence as MORE valuable than confirming evidence
- If a reading requires "exceptions," question the reading first
- Document what would falsify your current hypothesis

Self-check: *"Am I forcing evidence to fit my theory, or letting evidence shape my theory?"*

### Principle 3: ANCHOR-BASED EXPANSION

**Build outward from what's certain, not inward from speculation.**

Requirements:
- Identify ALL available anchors BEFORE novel readings
- Never skip anchor levels
- Never claim higher confidence than the anchor level supports
- Document which anchors support each reading

Self-check: *"Am I building from confirmed anchors outward, or from speculation inward?"*

### Principle 4: MULTI-HYPOTHESIS TESTING

**Always test Luwian, Semitic, Pre-Greek, AND Proto-Greek readings.**

No single hypothesis has achieved decipherment. Therefore:
- EVERY proposed reading must be tested against ALL four hypotheses
- Document which hypotheses the reading supports/contradicts
- If reading works under ONE hypothesis only → Max confidence: PROBABLE

Self-check: *"Have I tested this reading against ALL four major hypotheses?"*

### Principle 5: NEGATIVE EVIDENCE

**What the script DOESN'T show is also informative.**

Key observations for Linear A:
| Observation | Implication |
|-------------|-------------|
| Very few obvious Greek cognates | Probably not Greek |
| No clear Semitic triconsonantal patterns | Probably not Semitic |
| Limited visible inflection | Possibly isolating/agglutinative |
| Strong positional patterns | Sophisticated administrative system |

Self-check: *"What should I expect to see under this hypothesis that I'm NOT seeing?"*

### Principle 6: CROSS-CORPUS CONSISTENCY

**Readings must work across the entire corpus, not just one tablet.**

A reading is INVALID if:
- Works on one inscription but fails on others with same sequence
- Requires different values for same sign in different contexts
- Produces meaning on one tablet but gibberish on related tablets

Verification procedure:
1. Propose reading based on inscription X
2. Search corpus for ALL occurrences of sequence
3. Apply reading to EACH occurrence
4. IF consistent → Accept (with appropriate confidence)
5. IF inconsistent → REJECT or REVISE

Self-check: *"Does this reading hold across ALL occurrences in the corpus?"*

---

## Part 2: The Anchor Hierarchy

Build interpretations from established anchors outward. **Never skip levels.**

| Level | Type | Example | Max Confidence |
|-------|------|---------|----------------|
| 1 | Confirmed toponyms | pa-i-to = Phaistos | CERTAIN |
| 2 | Linear B cognates + position | ku-ro at totals | HIGH |
| 3 | Clear logograms | VIN, OLE, GRA | HIGH |
| 4 | Structural patterns | Transaction signs | MEDIUM |
| 5 | Morphological patterns | -jo genitive? | LOW-MEDIUM |
| 6 | Lexical matches | ki-ro = deficit | LOW |

### Anchor Re-evaluation Protocol

Anchors are provisional. Triggers for review:
- Anchor term appears in unexpected context
- Cross-corpus verification reveals inconsistency
- New archaeological/linguistic evidence challenges basis

Review outcome options: CONFIRMED, DEMOTED (update all dependent readings), REJECTED (remove from confirmed)

---

## Part 3: Four Hypotheses Framework

### 1. Luwian/Anatolian (Palmer, Finkelberg)

**Phonological mappings:**
- `a-` prefix ↔ Luwian conjunction
- `-wa-/-u-` ↔ quotative particle
- `ki-` ↔ `kui-` (relative pronoun)

**Morphological patterns:** `-ti`, `-nti` (verbal); `-ssa`, `-nda` (nominal)

### 2. Semitic - West Semitic/Akkadian (Gordon, Best)

**Method:** Extract consonants; compare to Semitic roots
- ku-ro → K-R → *kull* "total/all"
- ki-ro → K-R → "deficit/partial"
- SA-RA₂ → *šarāku* "allocate"

### 3. Pre-Greek Substrate (Beekes, Furnée)

**Phonological markers:** -nth-, -ss-, -mn- clusters; prothetic vowels

**Toponymic evidence:** Knossos, Amnissos, Tylissos (-ss-); Korinthos, Zakynthos (-nth-)

### 4. Proto-Greek (Georgiev, Mosenkis)

**Test administrative vocabulary:**
| Linear A | Greek candidate | Meaning |
|----------|-----------------|---------|
| ku-ro | kyrios | lord/complete |
| ma-te | mētēr | mother |

**Note:** Currently assessed as WEAKEST hypothesis (low /o/ frequency, absent Greek morphology)

---

## Part 4: Analysis Workflow

### Step 1: Source Acquisition

Primary databases:
1. **SigLA Database** - https://sigla.phis.me (palaeographical)
2. **University of Crete Ariadne** - https://ejournals.lib.uoc.gr/Ariadne/

Site codes: HT=Hagia Triada, KH=Khania, ZA=Zakros, PH=Phaistos, KN=Knossos

### Step 2: Sign Identification

For each sign:
1. Match against sign list (references/sign_list.md)
2. Assign AB number (GORILA classification)
3. Note variants; mark confidence (certain/probable/uncertain/illegible)

### Step 3: Phonetic Assignment

Apply Linear B values to homomorphic signs. Confidence levels:
- **High**: Identical to Linear B, confirmed by toponym matches
- **Medium**: Similar to Linear B, consistent with corpus
- **Low**: Differs from Linear B, value extrapolated
- **Unknown**: No Linear B cognate

### Step 4: Multi-Hypothesis Analysis

```
FOR each linguistic hypothesis H in {Luwian, Semitic, Pre-Greek, Proto-Greek}:
    1. Generate candidate reading using H's rules
    2. Search H's lexicon for matches
    3. Check morphological plausibility
    4. Assess semantic fit with context
    5. Score: P(reading | context, frequency, morphology)
OUTPUT: Ranked interpretations with reasoning chains
```

### Step 5: Corpus Verification

- Test proposed reading on ALL other occurrences
- Same sign = same value in all contexts
- Document corpus coverage

### Step 6: Documentation

For each interpretation document:
- Graphemic evidence (sign forms)
- Phonetic basis (Linear B cognate/extrapolation)
- Distributional evidence (frequency, positions)
- Morphological fit (which hypothesis)
- Semantic fit (archaeological context)
- Alternative interpretations
- Confidence level and novelty

---

## Part 5: Confidence Calibration

### Levels

| Level | Definition | Requirements |
|-------|------------|--------------|
| CERTAIN | Proven beyond reasonable doubt | Multiple independent anchors; cross-corpus consistency; no contradictions |
| HIGH | Very likely correct | Level 2-3 anchors; strong positional evidence |
| PROBABLE | Most likely correct | Good evidence; fits multiple hypotheses |
| POSSIBLE | Reasonable interpretation | Some evidence; alternatives exist |
| SPECULATIVE | Educated guess | Limited evidence; novel proposal |

### Automatic Downgrades

- Hapax legomenon (1 occurrence) → Max: POSSIBLE
- Damaged/uncertain signs → Reduce one level
- Single-hypothesis support → Max: PROBABLE
- Contradicts anchor → REJECT or flag for review

---

## Part 6: Pre/Post Flight Checklists

### Pre-Analysis Checklist (MANDATORY)

```
FIRST PRINCIPLES PRE-FLIGHT CHECK

[ ] I will analyze patterns BEFORE assuming a language [P1]
[ ] I am prepared to abandon my hypothesis if evidence contradicts [P2]
[ ] I have identified all available anchors [P3]
[ ] I will test against ALL four linguistic hypotheses [P4]
[ ] I will consider what the data DOESN'T show [P5]
[ ] I will verify readings across the ENTIRE corpus [P6]

If any box cannot be checked → DO NOT PROCEED
```

### Post-Analysis Verification (MANDATORY)

```
FIRST PRINCIPLES VERIFICATION

[1] KOBER: Was analysis data-led, not assumption-led?
    [PASS / FAIL / PARTIAL] Evidence: ___

[2] VENTRIS: Was any evidence forced to fit?
    [PASS / FAIL / PARTIAL] Evidence: ___

[3] ANCHORS: Were readings built from confirmed anchors outward?
    [PASS / FAIL / PARTIAL] Anchors used: ___

[4] MULTI-HYP: Were ALL four hypotheses tested?
    [PASS / FAIL / PARTIAL] Results: Luwian___ Semitic___ Pre-Greek___ Proto-Greek___

[5] NEGATIVE: Was absence of patterns considered?
    [PASS / FAIL / PARTIAL] Absences noted: ___

[6] CORPUS: Were readings verified across all occurrences?
    [PASS / FAIL / PARTIAL] Coverage: ___

ANY FAIL → Analysis is INVALID
ANY PARTIAL → Must document limitation explicitly
```

### Consequences of Violation

| Principle | Consequence |
|-----------|-------------|
| P1 (Kober) | Analysis invalidated; restart with pattern analysis |
| P2 (Ventris) | Hypothesis must be revised or rejected |
| P3 (Anchors) | Confidence capped at anchor level reached |
| P4 (Multi-Hyp) | Confidence capped at PROBABLE maximum |
| P5 (Negative) | Missing constraints flagged; analysis incomplete |
| P6 (Corpus) | Reading REJECTED until verified |

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

> "Linear A is undeciphered. Every claim requires evidence. Every interpretation requires humility. These principles exist because generations of scholars made the mistakes they prevent."

**When in doubt, return to the Six Principles.**

---

*Methodology document consolidating FIRST_PRINCIPLES.md, SKILL.md, and CLAUDE_REFERENCE.md*
