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
