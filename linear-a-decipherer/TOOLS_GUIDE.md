# Analysis Tools Guide

**Task-based tool selection for Linear A research**

---

## Quick Reference

| Task | Primary Tool | Supporting Tools |
|------|-------------|------------------|
| Analyze specific inscription | analyze_inscription.py | corpus_lookup.py |
| Investigate specific word | hypothesis_tester.py | corpus_lookup.py |
| Find patterns | kober_analyzer.py | slot_grammar_analyzer.py |
| Verify reading across corpus | kr_paradigm_validator.py | corpus_lookup.py |
| Check commodity correlations | contextual_analyzer.py | — |
| Validate reading corpus-wide | corpus_consistency_validator.py | — |
| Find external linguistic parallels | comparative_integrator.py | — |
| Discover new paradigms | paradigm_discoverer.py | — |
| Analyze personal names | personal_name_analyzer.py | — |
| Check for contradictions | phase_validator.py | — |

---

## Task-Based Workflows

### "I want to analyze a specific inscription"

**Example**: Analyze HT 13

**Steps**:
1. **Get transliteration**
   ```bash
   python tools/corpus_lookup.py HT13
   ```

2. **Run full analysis pipeline**
   ```bash
   python tools/analyze_inscription.py HT13
   ```

3. **Update knowledge management**
   - Add entry to ANALYSIS_INDEX.md
   - If findings significant, add to FINDINGS_LOG.md

**Output location**: analysis/completed/inscriptions/[ID]_analysis.md

---

### "I want to investigate a specific word"

**Example**: Investigate SA-RA₂

**Steps**:
1. **Find all occurrences**
   ```bash
   python tools/corpus_lookup.py "SA-RA₂"
   ```

2. **Test all hypotheses**
   ```bash
   python tools/hypothesis_tester.py --word "SA-RA₂"
   ```

3. **Check commodity correlations** (if administrative term)
   ```bash
   python tools/contextual_analyzer.py --word "SA-RA₂"
   ```

4. **Update knowledge management**
   - Add to ANALYSIS_INDEX.md (Words section)
   - If reaches HIGH+, add to CONFIRMED_READINGS.md
   - Document in FINDINGS_LOG.md

**Output location**: analysis/completed/thematic/[WORD]_investigation.md

---

### "I want to find patterns"

**Example**: Find morphological patterns in administrative tablets

**Steps**:
1. **Run frequency analysis**
   ```bash
   python tools/kober_analyzer.py --corpus HT
   ```

2. **Analyze positional distribution**
   ```bash
   python tools/slot_grammar_analyzer.py --site HT
   ```

3. **Identify inflection candidates**
   - Look for triplets (same word, different endings)
   - Check position patterns (initial/medial/final)

4. **Update knowledge management**
   - Add to ANALYSIS_INDEX.md (Thematic section)
   - Document in LESSONS_LEARNED.md if methodology refined

**Output location**: analysis/completed/thematic/[PATTERN]_analysis.md

---

### "I want to verify a reading across corpus"

**Example**: Verify KU-RO = "total"

**Steps**:
1. **Find all occurrences**
   ```bash
   python tools/corpus_lookup.py "KU-RO"
   ```

2. **Check position consistency**
   - Should be list-final
   - Should precede sum of preceding entries

3. **Run K-R paradigm validator** (for K-R words)
   ```bash
   python tools/kr_paradigm_validator.py
   ```

4. **Check for contradicting evidence**
   - Counter-examples
   - Unexpected positions
   - Numerical mismatches

5. **Update confidence in CONFIRMED_READINGS.md**

---

### "I want to compare regional variation"

**Example**: Compare HT vs. KH scribal practices

**Steps**:
1. **Run regional analyzer**
   ```bash
   python tools/regional_analyzer.py --sites HT KH
   ```

2. **Compare vocabularies**
   - Administrative terms
   - Oil/commodity logograms
   - Numerical patterns

3. **Document differences in STATE_OF_KNOWLEDGE.md**

---

## Tool Details

### corpus_lookup.py

**Purpose**: Query corpus for inscriptions or words

**Input**:
- Inscription ID (e.g., "HT 13")
- Word/sequence (e.g., "KU-RO")

**Output**:
- Transliteration
- Occurrence count
- Context for each occurrence

**Flags**:
- `--site [HT|KH|ZA|etc]` - Filter by site
- `--format [text|json]` - Output format

---

### analyze_inscription.py

**Purpose**: Full analysis pipeline for single inscription

**Input**: Inscription ID

**Output**:
- Transliteration with AB numbers
- Anchor identification
- Multi-hypothesis analysis
- First Principles verification

**Generates**: Markdown report following SKILL.md template

---

### hypothesis_tester.py

**Purpose**: Test word against all four linguistic hypotheses

**Input**:
- Word/sequence
- `--word [WORD]` flag

**Output**:
- Luwian score and analysis
- Semitic score and analysis
- Pre-Greek score and analysis
- Proto-Greek score and analysis
- Ranked results

**Interpretation**:
- Score > 3.0 = Strong support
- Score 1.5-3.0 = Moderate support
- Score < 1.5 = Weak support

---

### kober_analyzer.py

**Purpose**: Apply Kober Method (frequency, position, patterns)

**Input**:
- Corpus or subset
- `--corpus [site]` flag

**Output**:
- Sign frequencies
- Positional distributions
- Triplet candidates (potential paradigms)

---

### slot_grammar_analyzer.py

**Purpose**: Analyze grammatical slots (pre-logogram, post-logogram, etc.)

**Input**: Corpus or subset

**Output**:
- Slot distributions
- Words by grammatical position
- Pattern candidates

---

### kr_paradigm_validator.py

**Purpose**: Validate K-R paradigm (KU-RO, KI-RO, etc.)

**Input**: None (runs on full corpus)

**Output**:
- All K-R forms with frequencies
- Co-occurrence analysis
- Function assignments

**Key check**: Are forms complementary or do they co-occur?

---

### contextual_analyzer.py

**Purpose**: Analyze word-commodity correlations

**Input**: Word to analyze

**Output**:
- Commodities appearing with word
- Frequency by commodity type
- Distribution analysis

**Critical for**: Determining if word is commodity name vs. transaction term

---

### regional_analyzer.py

**Purpose**: Compare regional scribal practices

**Input**: Two or more site codes

**Output**:
- Vocabulary overlap/differences
- Script variations
- Administrative practice comparisons

---

### "I want to validate a proposed reading"

**Example**: Validate KU-RO = "total"

**Steps**:
1. **Check corpus-wide consistency**
   ```bash
   python tools/corpus_consistency_validator.py --word KU-RO --reading "total"
   ```

2. **Find external linguistic parallels**
   ```bash
   python tools/comparative_integrator.py --validate "KU-RO = total" --hypothesis semitic
   ```

3. **Check for contradicting claims**
   ```bash
   python tools/phase_validator.py --check-all
   ```

4. **Update knowledge management**
   - If validated, update CONFIRMED_READINGS.md
   - If contradictions found, document in LESSONS_LEARNED.md

**Output location**: data/consistency_validation.json

---

### "I want to discover new paradigms"

**Example**: Find morphological patterns beyond K-R

**Steps**:
1. **Run paradigm discovery**
   ```bash
   python tools/paradigm_discoverer.py --discover
   ```

2. **Investigate specific root**
   ```bash
   python tools/paradigm_discoverer.py --root SA
   ```

3. **Check suffix distributions**
   ```bash
   python tools/paradigm_discoverer.py --suffix JA
   ```

4. **Validate candidates corpus-wide**
   ```bash
   python tools/corpus_consistency_validator.py --word [CANDIDATE]
   ```

**Output location**: data/discovered_paradigms.json

---

### "I want to analyze personal names"

**Example**: Extract and classify anthroponyms

**Steps**:
1. **Extract potential names from corpus**
   ```bash
   python tools/personal_name_analyzer.py --extract
   ```

2. **Analyze specific name candidate**
   ```bash
   python tools/personal_name_analyzer.py --analyze DA-MA-TE
   ```

3. **Run full analysis on all candidates**
   ```bash
   python tools/personal_name_analyzer.py --all
   ```

**Output location**: data/personal_names.json

---

## New Tools (OPERATION MINOS II)

Five new tools were added to enforce First Principles automatically:

### corpus_consistency_validator.py

**Purpose**: Enforce First Principle #6 (Cross-Corpus Consistency)

**Input**:
- `--word [WORD]` - Word to validate
- `--reading [MEANING]` - Proposed meaning (optional)
- `--all --min-freq [N]` - Validate all words with N+ occurrences

**Output**:
- Site distribution analysis
- Period distribution analysis
- Positional consistency score (0-1)
- Contextual consistency score (0-1)
- Anomalies detected

**Critical check**: Readings must work across ALL sites, not just HT

---

### comparative_integrator.py

**Purpose**: Validate readings against external Bronze Age corpora

**Input**:
- `--query [TERM]` - Query Akkadian/Luwian vocabulary
- `--validate "[READING]" --hypothesis [TYPE]` - Validate against specific hypothesis
- `--update-cache` - Refresh external data cache

**Output**:
- Akkadian parallels (from ORACC)
- Luwian parallels (from Hethitologie)
- Ugaritic parallels (for trade terms)
- Confidence assessment

**Sources integrated**:
- ORACC (Open Richly Annotated Cuneiform Corpus)
- Hethitologie Portal (Luwian/Hittite)
- CDLI (Cuneiform Digital Library Initiative)

---

### paradigm_discoverer.py

**Purpose**: Discover morphological paradigms beyond K-R

**Input**:
- `--discover` - Run full paradigm discovery
- `--root [ROOT]` - Investigate specific consonantal root
- `--suffix [SUFFIX]` - Analyze suffix distribution

**Output**:
- Paradigm candidates with members
- Vowel alternation patterns
- Frequency and site distribution
- Confidence scoring

**Target paradigms**:
- SA- paradigm: SA-RA₂, SA-RU, SA-MA, SA-RI
- TA- paradigm: TA-I, TA-JA, TA-NA, TA-RA
- DA- paradigm: DA-I, DA-JA, DA-RE, DA-ME
- -JA suffix distribution across all roots

---

### personal_name_analyzer.py

**Purpose**: Extract and analyze anthroponyms (personal names)

**Input**:
- `--extract` - Extract potential names from corpus
- `--analyze [NAME]` - Analyze specific name candidate
- `--all` - Run full analysis on all candidates

**Output**:
- Candidate classification (likely name vs. not)
- Morphological pattern analysis
- Theophoric element detection
- Comparison to Bronze Age naming conventions

**Detection heuristics**:
- Words in "recipient" slot before logograms
- Theophoric elements (deity name + suffix)
- Known Near Eastern naming patterns
- High-frequency words not fitting administrative vocabulary

**Note**: Personal names estimated at 50%+ of Linear A vocabulary but currently 0% deciphered

---

### phase_validator.py

**Purpose**: Enforce First Principle #2 (Ventris Lesson) - track contradictions

**Input**:
- `--check-all` - Check for contradictions across all phases
- `--claim "[CLAIM]" --evidence "[SOURCE]"` - Register a morphological claim
- `--compare phase1 phase2` - Compare claims between phases

**Output**:
- Registered claims with evidence basis
- Detected contradictions
- Sample size comparisons
- Confidence evolution tracking

**Key function**: Prevents accumulating contradicting claims across analysis sessions

---

## External Resources

### external/lineara Integration

**Location**: `external/lineara/`

**Contents**:
- Full corpus images (1,600+ tablets)
- John Younger commentary (1,700 files)
- Network analysis views

**Use for**: Visual verification of discovered patterns, cross-referencing transliterations

---

## Database Reference

### Online Databases

| Database | URL | Best For |
|----------|-----|----------|
| SigLA | https://sigla.phis.me | Palaeographic details, sign variants |
| lineara.xyz | https://lineara.xyz | Quick corpus search, 1,800+ inscriptions |
| PAITO | https://www.paitoproject.it/linear-a/ | 1,534 documents, sign frequencies |
| SigLA GitHub | https://github.com/mwenge/lineara.xyz | Raw data access |

### Local Data

| File | Location | Content |
|------|----------|---------|
| statistics.json | data/corpus/ | Sign frequencies, word counts |
| inscriptions.json | data/corpus/ | Full inscription database |
| sign_values.json | data/reference/ | AB number to phonetic value |

---

## Workflow Integration

### Before Starting Analysis

1. Check ANALYSIS_INDEX.md - Has this been analyzed?
2. Read FIRST_PRINCIPLES.md - Pre-flight checklist
3. Review STATE_OF_KNOWLEDGE.md - Current understanding

### During Analysis

1. Use appropriate tool for task
2. Document all commands run
3. Test ALL four hypotheses (P4)
4. Check for negative evidence (P5)

### After Analysis

1. Update ANALYSIS_INDEX.md
2. Add discoveries to FINDINGS_LOG.md
3. If HIGH+ confidence, update CONFIRMED_READINGS.md
4. If methodology refined, update LESSONS_LEARNED.md
5. If major finding, update STATE_OF_KNOWLEDGE.md

---

## Common Pitfalls

### Tool Misuse

| Wrong | Right | Why |
|-------|-------|-----|
| hypothesis_tester without corpus_lookup | corpus_lookup THEN hypothesis_tester | Need occurrence data first |
| Single-hypothesis testing | All four hypotheses | P4 requires multi-hypothesis |
| Trust high scores blindly | Check evidence quality | Score is heuristic, not proof |

### Data Issues

| Issue | Solution |
|-------|----------|
| Missing transliteration | Try multiple databases (SigLA, lineara.xyz) |
| Conflicting readings | Document both; flag uncertainty |
| Damaged signs | Mark [?]; reduce confidence |

---

## Related Documents

- [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) - Methodology
- [SKILL.md](SKILL.md) - Operational procedures
- [ANALYSIS_INDEX.md](ANALYSIS_INDEX.md) - What's been done
- [LESSONS_LEARNED.md](LESSONS_LEARNED.md) - Tool-specific lessons

---

*Guide maintained as part of the Linear A Decipherment Project knowledge management system.*
