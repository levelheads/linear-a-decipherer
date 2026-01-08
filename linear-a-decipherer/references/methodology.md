# Decipherment Methodology

Best practices from successful script decipherments, adapted for autonomous Linear A analysis.

---

## ⚠️ PREREQUISITE: FIRST_PRINCIPLES.md

**This document is subordinate to `FIRST_PRINCIPLES.md`.**

All methodology described here exists to SERVE the six First Principles. If any technique conflicts with a First Principle, the Principle takes precedence.

| # | Principle | This Document Serves It Via |
|---|-----------|----------------------------|
| 1 | Kober | Kober Method (frequency, triplets, bridging) |
| 2 | Ventris | Anchor system, verification loops |
| 3 | Anchors | Anchor Point Hierarchy, expansion procedure |
| 4 | Multi-Hyp | Four-hypothesis testing protocol |
| 5 | Negative | Negative evidence section |
| 6 | Corpus | Cross-corpus verification procedure |

**Before applying ANY technique below, ask: "Does this serve the First Principles?"**

---

## Lessons from Linear B Decipherment

### The Kober Method: Internal Evidence First

Alice Kober (1906-1950) established the foundational methodology:

**Core principle**: "Anyone who took a theory about the language as their starting point was doomed to failure. The single route to the finishing line was to find the patterns and deep symmetries inside the primary texts."

**Key techniques**:

1. **Statistical frequency analysis**
   - Track how often each sign appears
   - Track position of signs (initial, medial, final)
   - Signs appearing frequently at word-initial position → likely pure vowels
   - Signs appearing at word-final position → likely inflectional endings

2. **Kober's Triplets** - Detecting inflection
   ```
   Pattern: Same root + three different endings
   
   Example from Linear B:
   [root]-[X]     (nominative singular?)
   [root]-[Y]     (genitive singular?)
   [root]-[Z]     (dative singular?)
   ```
   
   **For Linear A**: Search for recurring roots with variable endings
   - If found → language is inflected (IE, Semitic, Anatolian likely)
   - If not found → language may be isolating or agglutinative

3. **Bridging syllables**
   - In CV syllabary: ending consonant of root + beginning vowel of suffix = bridging sign
   - Allows deduction of phonetic relationships WITHOUT knowing values

4. **The Grid Method**
   - Arrange signs where same consonant = same row, same vowel = same column
   - Build grid from distributional evidence, not phonetic guesses
   - Once a few values are known, grid fills in through interdependencies

### The Ventris Method: Toponymic Anchors

Michael Ventris (1922-1956) broke Linear B with place names:

**Principle**: Cretan place names survived into Greek. If tablets contain place names, they provide anchor points.

**Application to Linear A**:
- `pa-i-to` confirmed = Phaistos (known from Linear B)
- `su-ki-ri-ta` likely = toponym (survives in Greek sources?)
- `se-to-i-ja` likely = toponym
- Names on headings often = place names

**Toponymic test procedure**:
1. Identify words appearing in heading positions
2. Check if transliterated form matches known Cretan place names
3. If match, use confirmed values to test other readings
4. Cross-validate across multiple tablets

### The Chadwick Verification: Expert Review

John Chadwick provided linguistic verification:

**For autonomous operation**: Build in self-verification steps:
- Does proposed reading fit known Greek/Luwian/Semitic phonology?
- Do proposed meanings make archaeological sense?
- Are readings consistent across the corpus?

## The Anchor Point System

### Definition

An **anchor point** is a sign, word, or pattern whose value/meaning is established with high confidence.

### Hierarchy of Anchors (Most → Least Reliable)

| Level | Type | Example | Confidence |
|-------|------|---------|------------|
| 1 | Confirmed toponym | pa-i-to = Phaistos | Very High |
| 2 | Linear B cognate with matching context | ku-ro at list totals | High |
| 3 | Ideogram with clear pictorial origin | Sheep, grain, wine | High |
| 4 | Numeral system | Decimal notation | High |
| 5 | Positional pattern | Transaction signs at list heads | Medium |
| 6 | Morphological pattern | Recurring suffixes | Medium |
| 7 | Vocabulary match (single hypothesis) | ki-ro = "deficit" | Low |

### Building from Anchors

```
PROCEDURE: Anchor-based expansion

1. Start with highest-confidence anchors
2. For each anchor:
   - Identify signs with confirmed values
   - Look for those signs in other words
   - Tentatively extend readings
   - Cross-validate against other anchors
3. If extension produces contradictions → revise or reject
4. If extension is consistent → promote to higher confidence
```

## Autonomous Operation Protocols

### State Tracking

The agent should maintain running state:

```
ANALYSIS STATE:
├── Confirmed readings: [list with confidence levels]
├── Tentative readings: [list with evidence]
├── Rejected hypotheses: [list with reasons]
├── Unresolved questions: [list]
├── Sources consulted: [list with URLs]
└── Corpus coverage: [% of relevant inscriptions analyzed]
```

### Self-Verification Loops

Before finalizing any interpretation:

```
VERIFICATION CHECKLIST:
□ Does reading work in ALL occurrences of this word in corpus?
□ Do proposed phonetic values conflict with established anchors?
□ Does meaning fit archaeological context?
□ Is interpretation consistent across multiple hypotheses?
□ Have alternative readings been considered and documented?
□ Is confidence level appropriately calibrated?
```

### Error Recovery

When encountering problems:

| Problem | Recovery Action |
|---------|-----------------|
| Source unavailable | Try alternative sources; note gap in analysis |
| Conflicting readings | Document both; escalate uncertainty |
| No matches found | Explicitly state "no interpretation possible" |
| Sign unidentifiable | Mark with [?]; note damage/uncertainty |
| Corpus too small | Flag that conclusion is speculative |

### Confidence Calibration

**Automatic confidence downgrade triggers**:
- Hapax legomenon (appears only once) → Max confidence: POSSIBLE
- Damaged/uncertain signs → Reduce by one level
- Single-hypothesis support only → Max confidence: PROBABLE
- Contradicts established anchor → Flag for review

**Confidence levels**:
| Level | Meaning | Requirements |
|-------|---------|--------------|
| CERTAIN | Proven beyond reasonable doubt | Multiple independent anchors; cross-corpus consistency |
| PROBABLE | Most likely correct | Strong distributional evidence; fits multiple hypotheses |
| POSSIBLE | Reasonable interpretation | Some supporting evidence; alternatives exist |
| SPECULATIVE | Educated guess | Limited evidence; novel proposal |
| UNKNOWN | Cannot determine | Insufficient data |

### When to Escalate

Flag for human review when:
- Proposed reading contradicts established scholarship
- Novel interpretation with significant implications
- Multiple equally-plausible contradictory readings
- Potential breakthrough discovery
- Confidence consistently below POSSIBLE threshold

## Pattern Recognition Templates

### Administrative Tablet Patterns

```
TEMPLATE: Commodity List
[Transaction sign?]
.1  [Name/Toponym] [Logogram] [Number]
.2  [Name/Toponym] [Logogram] [Number]
...
.n  ku-ro [Total]

INDICATORS:
- Presence of numerals
- Presence of logograms (VIN, OLE, GRA, etc.)
- ku-ro in final position
- Multiple entries with similar structure
```

### Libation Formula Pattern

```
TEMPLATE: Religious Inscription
[Dedicatory phrase] [Divine name(s)] [Verb(s)] [Ritual terms]

KNOWN ELEMENTS:
- a-ta-i-*301-wa-ja (dedicatory?)
- ja-sa-sa-ra-me (deity name?)
- u-na-ka-na-si (verb?)

INDICATORS:
- Stone vessel (not clay)
- No numerals
- Formulaic repetition across sites
- Peak sanctuary or cave context
```

### Personal Name Pattern

```
INDICATORS:
- Appears with singular numeral or no numeral
- Different from toponyms (doesn't head lists)
- May show inflection (genitive -jo ending?)
- Varies between tablets (unlike toponyms)
```

## The Negative Evidence Principle

**What Linear A is NOT telling us is also informative:**

- Very few if any Greek-looking words → Probably not Greek
- No clear Semitic morphology → Probably not Semitic
- Limited inflection visible → Possibly isolating language
- Strong positional patterns → Sophisticated administrative system

## Iterative Refinement Cycle

```
CYCLE: Autonomous analysis loop

1. INGEST: Fetch inscription from sources
2. IDENTIFY: Transliterate signs using established values
3. SEGMENT: Identify word boundaries
4. ANCHOR: Match against known anchors
5. EXTEND: Tentatively extend from anchors
6. VERIFY: Run self-verification checks
7. HYPOTHESIZE: Generate readings under each hypothesis
8. COMPARE: Rank hypotheses by evidence fit
9. DOCUMENT: Record reasoning chains
10. ITERATE: If new insights, re-run on related inscriptions
```

## Red Flags for Autonomous Agent

Stop and reconsider if:
- You're forcing evidence to fit a preconceived theory
- Multiple "exceptions" are required to maintain a reading
- Semantic interpretations rely on stretching meanings
- You're citing sources you haven't actually fetched
- Confidence doesn't match evidence strength
- You haven't considered alternative hypotheses

Remember Kober's warning: "Mere lists of proposed phonetic values and derivations carry little conviction."

## The Ventris Lesson

Ventris himself believed Linear B encoded Etruscan until the very end. He was wrong about the language but right about the methodology. 

**Lesson for autonomous operation**: Follow the evidence even when it contradicts your working hypothesis. Be willing to abandon theories that don't fit the data.
