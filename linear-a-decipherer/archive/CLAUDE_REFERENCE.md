# Claude Reference: Detailed Linear A Methodology

Read this file when performing actual analysis. This contains the full methodology details moved from CLAUDE.md to reduce context overhead.

---

## Core Design Pattern: Evidence-Based Reasoning Chain

The system does NOT function as a simple lookup tool. Instead, it:

1. **Acquires sources** - Fetches inscriptions from online databases (SigLA, academic repositories)
2. **Establishes anchors** - Identifies confirmed toponyms, Linear B cognates, logograms
3. **Analyzes patterns** - Uses Kober Method (frequency, position, inflection patterns)
4. **Tests hypotheses** - Generates readings under Luwian, Semitic, Pre-Greek, Proto-Greek frameworks
5. **Ranks interpretations** - Weights evidence chains and assigns calibrated confidence
6. **Verifies corpus-wide** - Tests proposed readings across all occurrences
7. **Documents reasoning** - Outputs complete evidence chains, not just conclusions

---

## The Anchor Hierarchy (STRICT ORDER)

| Level | Type | Example | Max Confidence |
|-------|------|---------|----------------|
| 1 | Confirmed toponyms | pa-i-to = Phaistos | CERTAIN |
| 2 | Linear B cognates + position | ku-ro at totals | HIGH |
| 3 | Clear logograms | VIN, OLE, GRA | HIGH |
| 4 | Structural patterns | Transaction signs | MEDIUM |
| 5 | Morphological patterns | -jo genitive? | LOW-MEDIUM |
| 6 | Lexical matches | ki-ro = deficit | LOW |

**Never skip anchor levels.** Confidence cannot exceed the anchor level reached.

---

## Four Mandatory Linguistic Hypotheses

EVERY proposed reading must be tested against:

1. **Luwian/Anatolian** (Palmer, Finkelberg)
2. **Semitic** - West Semitic/Akkadian (Gordon, Best)
3. **Pre-Greek Substrate** (Beekes, Furnée)
4. **Proto-Greek** (Georgiev, Mosenkis)

Single-hypothesis support caps confidence at PROBABLE. Multi-hypothesis convergence or overwhelming single-hypothesis evidence required for CERTAIN.

---

## Analyzing a Linear A Inscription

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

---

## Required Reading Order (for new sessions)

1. `linear-a-decipherer/FIRST_PRINCIPLES.md` (MANDATORY)
2. `linear-a-decipherer/SKILL.md` (operational procedures)
3. `linear-a-decipherer/references/methodology.md` (techniques)
4. `linear-a-decipherer/references/hypotheses.md` (linguistic frameworks)
5. `linear-a-decipherer/references/corpus.md` (inscription database)
6. `linear-a-decipherer/references/sign_list.md` (syllabary)

---

## Site Code Reference

| Code | Site | Key Information |
|------|------|----------------|
| HT | Hagia Triada | Largest corpus (147 tablets) |
| KH | Khania | 99 tablets |
| ZA | Zakros | 31 tablets |
| PH | Phaistos | Earliest inscriptions |
| KN | Knossos | Includes 2024 ivory scepter (119 signs) |

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

## Key Inscriptions to Reference

- **HT 13** - Classic commodity list with ku-ro total
- **KN Zf 2** - 2024 ivory scepter discovery (longest inscription ever found, 119 signs)
- **Libation formulas** - Religious texts from peak sanctuaries

---

## Knossos Ivory Scepter (2024)

- **119 signs** - longest Linear A inscription ever found
- Two separate inscriptions by different scribes
- Ring: ceremonial/religious style
- Handle: administrative style with numerals
- Published in Ariadne Supplement 5 (2025)
- URL: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841

---

## Historical Context

The First Principles derive from hard-won lessons:

- **Alice Kober (1906-1950)** established that pattern analysis must precede language assumptions. Her methodology enabled Linear B's decipherment.
- **Michael Ventris (1922-1956)** believed Linear B was Etruscan until overwhelming evidence proved otherwise. He succeeded because he followed methodology over preconception.

---

## Error Recovery

| Situation | Action |
|-----------|--------|
| Source unavailable | Try alternatives; document gap |
| Conflicting readings | Present both; flag uncertainty |
| Sign unidentifiable | Mark [?]; note damage |
| No interpretation possible | State explicitly; don't force a reading |
| Potential breakthrough | Flag for significance; document thoroughly |
