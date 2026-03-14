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
| **Audit corpus structure** | **corpus_auditor.py** | — |
| **Audit corpus readiness** | **corpus_readiness_auditor.py** | run_corpus_refresh_cycle.sh |
| **Verify KU-RO totals** | **corpus_auditor.py --totals** | — |
| **Find function words** | **corpus_auditor.py --function-word** | — |
| **Check tool drift/parity** | **tool_parity_checker.py** | integrated_validator.py |
| **Generate promotion packet** | **promotion_board_runner.py** | integrated_validator.py, corpus_consistency_validator.py |
| **Run lane orchestration** | **lane_orchestrator.py** | config/lane_manifest.yaml |
| **Pre-check dependency trace** | **dependency_trace_resolver.py** | promotion_board_runner.py |
| **Normalize site names/codes** | **site_normalization.py** | extended_corpus_analyzer.py, regional_analyzer.py |
| **Find cascade opportunities** | **cascade_opportunity_detector.py** | reading_readiness_scorer.py |
| **Build personnel dossiers** | **personnel_dossier_builder.py** | onomastic_comparator.py |
| **Extract sign value constraints** | **sign_value_extractor.py** | arithmetic_verifier.py |
| **Automate reading workflow** | **reading_pipeline.py** | All evidence-gathering tools |

---

## Task-Based Workflows

### Shared Word Filter Contract

Hypothesis-facing pipelines now share one eligibility contract (`tools/word_filter_contract.py`):
- include only hypothesis-eligible hyphenated lexical tokens
- exclude numerals/fractions, non-word separators, and damaged markers
- exclude non-hyphen logogram/symbol tokens

This contract is applied by:
- `hypothesis_tester.py`
- `batch_pipeline.py`
- `integrated_validator.py`

### Shared Site Normalization Contract

Corpus-facing pipelines now share one site normalization contract (`tools/site_normalization.py`):
- normalize inscription ID site prefixes and full site names to canonical site codes
- provide canonical code + full-name pairing for reporting artifacts
- prevent mismatches between corpus full names and analysis short codes

This contract is applied by:
- `extended_corpus_analyzer.py`
- `regional_analyzer.py`
- `corpus_consistency_validator.py`

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
   - If findings significant, add to CHANGELOG.md

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
   - If reaches HIGH+, add to KNOWLEDGE.md
   - Document in CHANGELOG.md

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
   - Document in ENGINEERING_PRACTICES.md if methodology refined

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

5. **Update confidence in KNOWLEDGE.md**

---

### "I want to audit corpus structure (no language assumptions)"

**Example**: Find function words, verify totals, check commodity associations

**Steps**:
1. **Run full structural audit**
   ```bash
   python tools/corpus_auditor.py --all --save
   ```

2. **Investigate specific function word candidate**
   ```bash
   python tools/corpus_auditor.py --function-word TE
   ```

3. **Check arithmetic consistency**
   ```bash
   python tools/corpus_auditor.py --totals
   ```

4. **Update knowledge management**
   - Mismatches may indicate parsing errors or undocumented fractions
   - High-specificity tokens are commodity-specific terms
   - Low-specificity tokens are function words or general terms

**Output location**: data/audit/corpus_audit.json

**Key insight**: This works WITHOUT language assumptions - pure structural/mathematical analysis

---

### "I want to refresh corpus and emit a readiness snapshot"

**Example**: Run a sprint-start refresh with parse, validation, and readiness output

**Steps**:
1. **Dry run**
   ```bash
   bash tools/run_corpus_refresh_cycle.sh --dry-run
   ```

2. **Execute refresh cycle**
   ```bash
   bash tools/run_corpus_refresh_cycle.sh --date 2026-02-15
   ```

3. **Generate readiness snapshot directly (optional)**
   ```bash
   python3 tools/corpus_readiness_auditor.py --markdown
   ```

**Output location**:
- `analysis/active/YYYY-MM-DD_corpus_access_readiness_audit.json`
- `analysis/active/YYYY-MM-DD_corpus_access_readiness_audit.md`

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

3. **Document differences in KNOWLEDGE.md**

---

### "I want to run multi-lane execution with handoff artifacts"

**Example**: Run lanes A, B, and F for governance + validation checks

**Steps**:
1. **Preview lane execution plan**
   ```bash
   python3 tools/lane_orchestrator.py --lane A,B,F --dry-run
   ```

2. **Run selected lanes**
   ```bash
   python3 tools/lane_orchestrator.py --lane A,B,F
   ```

3. **Review handoff report**
   - Output: `data/lane_handoffs/YYYY-MM-DD.json`
   - Confirm command status, artifact presence, and required reviewer lane

4. **Run parity check before promotion decisions**
   ```bash
   python3 tools/tool_parity_checker.py --output data/tool_parity_report.json
   ```

5. **Pre-check dependency trace completeness**
   ```bash
   python3 tools/dependency_trace_resolver.py --top 25 --output data/dependency_trace_report.json
   ```

6. **Generate promotion packet for candidate**
   ```bash
   python3 tools/promotion_board_runner.py --candidate KU-RO --target-confidence HIGH
   ```

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

**Generates**: Markdown report following METHODOLOGY.md template

---

### hypothesis_tester.py

**Purpose**: Test word against all seven linguistic hypotheses

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

---

## BREAKTHROUGH Tools (2026-02-17)

Four new tools were added as part of the BREAKTHROUGH sub-projects, extending hypothesis testing from 4 to 7 hypotheses:

### structural_grid_builder.py

**Purpose**: Build a "Ventris Grid" — grammatical category identification from structural patterns

**Input**:
- `--all` - Run full grid analysis
- `--build` - Build category grid
- `--constraints` - Show constraint analysis
- `--entropy` - Show entropy calculations

**Output**: `data/ventris_grid.json` — 27 grammatical categories (14 significant)

### admin_isomorphism_scorer.py

**Purpose**: Score administrative template isomorphisms across 6 Bronze Age writing systems

**Input**:
- `--all` - Run full analysis
- `--score` - Score isomorphisms
- `--identify` - Identify template matches
- `--khania` - Khania-specific analysis

**Output**: `data/admin_isomorphism.json` — 36 template comparisons, 46 positional identifications

### morphological_predictor.py

**Purpose**: Generate and test morphological predictions from hypothesis frameworks

**Input**:
- `--all` - Run full analysis
- `--decompose` - Decompose words morphologically
- `--predict` - Generate predictions
- `--infix-hunt` - Search for infixes
- `--typology` - Typological comparison

**Output**: `data/morphological_predictions.json` — 481 predictions (71 hits, 14.8%), 20 infixes

### onomastic_comparator.py

**Purpose**: Compare Linear A names against Bronze Age onomastic traditions

**Input**:
- `--all` - Run full analysis
- `--compare` - Cross-tradition comparison
- `--theophoric` - Theophoric element analysis
- `--regional` - Regional name distribution

**Output**: `data/onomastic_analysis.json` — 111 name profiles, 46 theophoric elements

---

## Reading Attempt Tools (2026-02-17)

Three new tools for transitioning from evidence accumulation to tablet reading:

### reading_readiness_scorer.py

**Purpose**: Score all tablets by how "readable" they are, combining all available evidence

**Input**:
- `--tablet [ID]` - Score single tablet
- `--all` - Score all tablets, rank by readiness
- `--top N` - Show top N most readable tablets
- `--output FILE` - Save to JSON

**Output**: `data/reading_readiness.json` — per-tablet composite scores (coverage, arithmetic, structure, size)

**Key metrics**: Weights — 40% coverage, 25% arithmetic, 15% structural, 10% size, 10% unknown penalty

### arithmetic_verifier.py

**Purpose**: Diagnose KU-RO arithmetic mismatches and produce Rosetta skeletons

**Input**:
- `--tablet [ID]` - Verify single tablet
- `--all` - Verify all KU-RO tablets
- `--diagnose` - Diagnose mismatches
- `--skeleton [ID]` - Output Rosetta skeleton
- `--output FILE` - Save to JSON

**Output**: `data/arithmetic_verification.json` — 6 VERIFIED, 23 MISMATCH (diagnosed), 5 INCOMPLETE

**Mismatch categories**: lacuna (8), missing_entries (7), fraction_parsing (4), multi_commodity (2), multi_kuro (2)

### commodity_validator.py

**Purpose**: Promote co-occurrence observations to validated functional anchors

**Input**:
- `--word [WORD]` - Validate single word
- `--all` - Validate all high-specificity words
- `--threshold [FLOAT]` - Minimum specificity (default: 0.8)
- `--output FILE` - Save to JSON

**Output**: `data/commodity_anchors.json` — 15 validated mappings (6 STRONG_ANCHOR, 9 CANDIDATE)

**Promotion levels**: FUNCTIONAL_ANCHOR (≥95%, no exceptions), STRONG_ANCHOR (≥80%), CANDIDATE (≥threshold)

---

### Extended Tools (4→7 hypotheses)

The following existing tools were extended to support all 7 hypotheses (luwian, semitic, pregreek, protogreek, hurrian, hattic, etruscan):

- `hypothesis_tester.py` — per-word hypothesis testing
- `falsification_system.py` — falsification threshold classification
- `negative_evidence.py` — absence pattern analysis
- `bayesian_hypothesis_tester.py` — Bayesian posterior calculation (7 + isolate)

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
   - If validated, update KNOWLEDGE.md
   - If contradictions found, document in ENGINEERING_PRACTICES.md

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

### corpus_auditor.py (NEW)

**Purpose**: Structural corpus analysis WITHOUT language assumptions

Implements three audit functions from quantitative corpus linguistics:

1. **Arithmetic validation** (`--totals`): Verify KU-RO totals match preceding amounts
2. **Token-commodity co-occurrence** (`--cooccurrence`): Build bipartite graph of words and logograms
3. **Function word analysis** (`--function-word WORD`): Positional study of candidates like TE

**Input**:
- `--totals` - Validate arithmetic consistency of KU-RO totals
- `--cooccurrence` - Build token-commodity matrix
- `--function-word [WORD]` - Analyze positional distribution
- `--all` - Run full audit
- `--save` - Export results to JSON

**Output**:
- **Totals**: VERIFIED/PARTIAL/MISMATCH/INCOMPLETE status for each KU-RO
- **Co-occurrence**: High-specificity tokens (commodity-specific) vs low-specificity (function words)
- **Function words**: Position entropy, neighbors, scribe/site distribution, role hypothesis

**Key metrics**:
- Position entropy: 0 = fixed position, 1 = uniform distribution
- Specificity: 0 = appears with all commodities, 1 = one commodity only

**Example findings** (2026-01-31 audit):
- TE: 67% line-initial, entropy 0.64 → "Header/Topic marker"
- KU-RO: 100% line-initial (on its own line), always followed by number
- KI-RO: 100% specificity with CYP (copper) — previously undocumented!

**Critical insight**: Can discover function word roles purely from position, no translation needed

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
2. Read METHODOLOGY.md - Pre-flight checklist
3. Review KNOWLEDGE.md - Current understanding

### During Analysis

1. Use appropriate tool for task
2. Document all commands run
3. Test ALL seven hypotheses (P4)
4. Check for negative evidence (P5)

### After Analysis

1. Update ANALYSIS_INDEX.md
2. Add discoveries to CHANGELOG.md
3. If HIGH+ confidence, update KNOWLEDGE.md
4. If methodology refined, update ENGINEERING_PRACTICES.md
5. If major finding, update KNOWLEDGE.md

---

## Common Pitfalls

### Tool Misuse

| Wrong | Right | Why |
|-------|-------|-----|
| hypothesis_tester without corpus_lookup | corpus_lookup THEN hypothesis_tester | Need occurrence data first |
| Single-hypothesis testing | All seven hypotheses | P4 requires multi-hypothesis |
| Trust high scores blindly | Check evidence quality | Score is heuristic, not proof |

### Data Issues

| Issue | Solution |
|-------|----------|
| Missing transliteration | Try multiple databases (SigLA, lineara.xyz) |
| Conflicting readings | Document both; flag uncertainty |
| Damaged signs | Mark [?]; reduce confidence |

---

## New Tools (2026-02 Audit)

Two new tools were added to address critical gaps identified in the 2026-02 comprehensive audit:

### sign_reconciler.py

**Purpose**: Reconcile the two sign classification systems (phonetic notation vs AB numbers)

This tool addresses the critical issue that `signs.json` (mixed notation) and `sign_database.json` (AB numbers) had only 2 signs in common with no explicit mapping.

**Input**:
- `--build` - Build unified mapping table and save to `data/sign_mapping.json`
- `--lookup [SIGN]` - Look up sign by phonetic value (e.g., KU, RA)
- `--ab [AB#]` - Look up by AB number (e.g., AB81, AB02)
- `--word [WORD]` - Normalize a word showing AB mappings (e.g., KU-RO)
- `--validate` - Validate all corpus signs against sign database
- `--report` - Generate human-readable reconciliation report

**Output**:
- Bidirectional mapping: phonetic ↔ AB numbers
- Unified sign inventory with frequency data from both sources
- Corpus validation report showing mapped vs unmapped signs

**Example**:
```bash
python tools/sign_reconciler.py --word KU-RO
# Output:
#   KU -> AB81 (CERTAIN)
#   RO -> AB02 (CERTAIN)
```

**Key insight**: Enables cross-referencing between paleographic data and corpus analysis

---

### batch_pipeline.py

**Purpose**: Systematic analysis of the entire corpus (addresses 0.81% coverage gap)

This tool chains together discovery, hypothesis testing, validation, and synthesis into a single pipeline, enabling analysis at scale.

**Stages**:
1. **DISCOVER**: Extract all words with frequency counts
2. **HYPOTHESIZE**: Test each word against seven linguistic hypotheses
3. **VALIDATE**: Check cross-corpus consistency (First Principle #6)
4. **SYNTHESIZE**: Aggregate findings and generate recommendations

**Input**:
- `--full` - Run complete pipeline on entire corpus
- `--stage [STAGE]` - Run single stage (discover/hypothesize/validate/synthesize)
- `--site [SITE]` - Filter by site code (e.g., HT, KH, ZA)
- `--min-freq [N]` - Minimum frequency threshold (default: 2)
- `--max-words [N]` - Maximum words to test (for quick runs)
- `--resume` - Resume from last checkpoint

**Output**:
- `data/batch_analysis_results.json` - Complete synthesis with:
  - Hypothesis rankings across corpus
  - High/medium confidence findings
  - Cross-corpus validation verdicts
  - Recommendations for KNOWLEDGE.md updates
- `data/pipeline_checkpoints/` - Stage checkpoints for resumption

**Example**:
```bash
# Full pipeline with minimum frequency 3
python tools/batch_pipeline.py --full --min-freq 3 --verbose

# Resume after interruption
python tools/batch_pipeline.py --full --resume

# Analyze only Hagia Triada tablets
python tools/batch_pipeline.py --full --site HT --min-freq 5
```

**First Principles Compliance**:
- P1 (Kober): Patterns analyzed before language assumption
- P4 (Multi-Hypothesis): All seven hypotheses tested automatically
- P6 (Cross-Corpus): Every reading verified corpus-wide

**Critical impact**: Scales analysis from 14 inscriptions (0.81%) to full corpus (1,722 inscriptions)

---

## Operation VENTRIS Tools (2026-03-14)

Four new tools for strategic depth — transitioning from evidence accumulation to language understanding:

### cascade_opportunity_detector.py

**Purpose**: Detect which tablets become readable when new evidence confirms a word/sign value

**Input**:
- `--word [WORD]` - Trigger word to test
- `--confidence [LEVEL]` - Confidence level (HIGH, PROBABLE, POSSIBLE)
- `--all-anchors` - Test all current anchors
- `--threshold [FLOAT]` - Minimum readiness delta (default: 0.1)
- `--output FILE` - Save to JSON

**Output**: Per-tablet readiness deltas, transitive cascade chains, priority queue for next readings

**Key insight**: Answers "if we confirm X, which tablets become readable?" — guides research priorities

---

### personnel_dossier_builder.py

**Purpose**: Build cross-tablet name intelligence for profiled individuals

**Input**:
- `--all` - Build dossiers for all 111 profiled names
- `--name [NAME]` - Build dossier for specific name
- `--top N` - Show top N most-connected names
- `--cross-tablet` - Focus on names appearing on multiple tablets
- `--output FILE` - Save to JSON

**Output**: `data/personnel_dossiers.json` — per-name dossier with tablets, roles, commodities, quantities, co-occurring names, sites, admin tier

**Key insight**: Tracks individual "careers" across the archive — reveals administrative hierarchy

---

### sign_value_extractor.py

**Purpose**: Arithmetic-driven sign value discovery from VERIFIED tablets

**Input**:
- `--all` - Extract from all VERIFIED tablets
- `--tablet [ID]` - Extract from specific tablet
- `--sign '*NNN'` - Constrain specific sign (quote the asterisk!)
- `--ratios` - Show quantity ratio analysis
- `--output FILE` - Save to JSON

**Output**: `data/sign_value_constraints.json` — arithmetic skeletons with unknown sign value constraints

**Key insight**: Uses arithmetic proof (not linguistic guess) to constrain sign values

---

### reading_pipeline.py

**Purpose**: Automated reading workflow (SELECT → PREPARE → READ → RECORD)

**Input**:
- `--select` - Generate prioritized, site-balanced reading queue
- `--prepare [TABLET]` - Generate reading brief for specific tablet
- `--queue` - Show current reading queue
- `--top N` - Limit queue to top N tablets
- `--site-balanced` - Enforce site diversification
- `--output FILE` - Save to JSON

**Output**: `data/reading_queue.json` — prioritized tablet queue excluding already-read tablets

**Key workflow**: SELECT → PREPARE → [Human analysis] → RECORD

---

### "I want to read a new tablet"

**Example**: Systematic tablet reading from selection to recording

**Steps**:
1. **Select best candidates**
   ```bash
   python3 tools/reading_pipeline.py --select --top 20 --site-balanced
   ```

2. **Prepare reading brief**
   ```bash
   python3 tools/reading_pipeline.py --prepare TABLET_ID
   ```

3. **[Human analysis using the reading brief]**

4. **Check cascade opportunities from new findings**
   ```bash
   python3 tools/cascade_opportunity_detector.py --word NEW_WORD --confidence LEVEL
   ```

---

## Governance & Utility Tools

Supporting tools for data management, release governance, and linguistic utilities.

### Data Management

#### validate_corpus.py

**Purpose**: Validate Linear A corpus data integrity

**Flags**: `--verbose`, `--quiet`, `--report FILE` (default: `data/validation_report.json`), `--report-only`

---

#### update_index.py

**Purpose**: Auto-update ANALYSIS_INDEX.md from analysis files

**Flags**: `--write` (default: preview only), `--json`, `--verbose`

---

#### compare_results.py

**Purpose**: Compare hypothesis/batch results before and after a fix

**Flags**: `--hypo-pre FILE`, `--hypo-post FILE`, `--batch-pre FILE`, `--batch-post FILE`

---

#### enrich_chronology.py

**Purpose**: Enrich Linear A corpus with inferred chronology data

**Flags**: `--dry-run`, `--verbose`, `--output FILE` (default: `data/corpus.json`), `--report FILE`

---

### Governance

#### master_state_guard.py

**Purpose**: Validate canonical-state governance (ensures MASTER_STATE.md is well-formed)

**Flags**: `--strict` (fail on warnings as errors)

---

#### refresh_master_state.py

**Purpose**: Refresh metrics in MASTER_STATE.md from live data sources

**Flags**: `--write` (write updates to disk), `--check` (exit non-zero if out of date)

---

#### release_gate.py

**Purpose**: Run strict release gate checks before tagging a version

**Flags**: `--tag TAG` (e.g., `v0.4.1`)

---

#### release_audit.py

**Purpose**: Audit local tags vs GitHub releases for consistency

**Flags**: `--strict-network` (fail if GitHub release API is unavailable)

---

#### git_manager.py

**Purpose**: Git workflow helper for Linear A Decipherer

**Subcommands**: `status`, `pre-commit`, `summary`, `sync`, `release`

---

### Linguistic Utilities

#### phoneme_reconstructor.py

**Purpose**: Reconstruct Linear A phoneme inventory

**Flags**: `--all`, `--vowel-matrix`, `--consonant-clusters`, `--cvc-signs`, `--output FILE`, `--verbose`

---

#### regional_weighting.py

**Purpose**: Calculate regional weights for Linear A readings

**Flags**: `--word WORD`, `--all`, `--min-freq N` (default: 3), `--site-stats`, `--output FILE`, `--verbose`

---

#### statistical_analysis.py

**Purpose**: Statistical analysis of Linear A corpus (chronology, regional, register, positions, entropy)

**Subcommands**: `chronology`, `regional`, `register`, `positions`, `entropy`, `summary` (default)

**Flags**: `--sites SITES`, `--compare PERIOD1 PERIOD2`, `--output FILE`, `--verbose`

---

#### temporal_evolution_tracker.py

**Purpose**: Analyze Linear A across archaeological periods

**Flags**: `--all`, `--period PERIOD` (e.g., LMIB, MMIII), `--vocabulary`, `--structure`, `--output FILE`

---

## Related Documents

- [METHODOLOGY.md](METHODOLOGY.md) - First principles and methodology
- [MASTER_STATE.md](MASTER_STATE.md) - Current operational state
- [ANALYSIS_INDEX.md](ANALYSIS_INDEX.md) - What's been done
- [ENGINEERING_PRACTICES.md](ENGINEERING_PRACTICES.md) - Tool-specific lessons

---

*Guide maintained as part of the Linear A Decipherment Project knowledge management system. 60 tools as of v0.11.0.*
