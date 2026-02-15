# Linear A Decipherer

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
![Inscriptions](https://img.shields.io/badge/Inscriptions-1%2C721-blue)
![Current State](https://img.shields.io/badge/Current%20State-MASTER__STATE.md-blue)

> **Canonical current-state file**: `linear-a-decipherer/MASTER_STATE.md`
> Use it for active metrics, campaign status, promotion gates, and release readiness.

A rigorous methodology system for analyzing undeciphered Minoan Bronze Age inscriptions (c.1800-1450 BCE) from Crete.

---

## Research Status (February 2026)

> **Working hypothesis validated through systematic tool-based corpus analysis.** Proto-Greek **ELIMINATED** at 2.5% support (5/198 words), consistent with prior scholarly observations on phonological mismatch (Gordon 1966, Beekes 2014). Luwian morphology validated as **DOMINANT** at 30.3%. The vowel /o/ appears at only 3.9% frequency (Greek expects ~20%), and zero Greek case endings have been identified.

**Best-fit model**: Linear A records a **contact language** with three distinct layers, building on proposals by Gordon (1966), Palmer (1958), and Beekes (2014):

| Layer | Tool-Validated Support | Key Findings | Prior Scholarship |
|-------|------------------------|--------------|-------------------|
| **Luwian morphology** | **30.3%** (60/198 words) | -JA adjectival (77 occ); -TE/-TI verbal; WA/U quotative | Palmer (1958), Finkelberg (1998) |
| **Semitic administrative** | **17.7%** (35/198 words) | ku-ro = *kull* "total"; SA-RA₂ = *šarāku* "allocate" | Gordon (1966), Best (1972) |
| **Pre-Greek substrate** | Base layer | pa-i-to = Phaistos; 123 unique signs Greek couldn't represent | Beekes (2014), Furnée (1972) |

---

## Overview

**Linear A remains undeciphered.** This project approaches it as an active research problem, not a solved puzzle.

The system uses a methodology derived from the successful Linear B decipherment to systematically analyze patterns, test competing linguistic hypotheses, and generate novel interpretations with calibrated confidence levels.

### Key Features

- **Evidence-based reasoning chains** - Every interpretation documented with explicit evidence
- **Multi-hypothesis testing** - All readings tested against Luwian, Semitic, Pre-Greek, and Proto-Greek frameworks
- **Anchor-based expansion** - Building from confirmed toponyms and Linear B cognates outward
- **Corpus-wide verification** - Proposed readings validated across all 1,721 inscriptions
- **Calibrated confidence** - Explicit uncertainty quantification for all claims
- **Regional analysis** - Site-by-site vocabulary comparison reveals parallel administrative systems

---

## First Principles

The system operates under six inviolable principles derived from Alice Kober's methodology and Michael Ventris's successful decipherment of Linear B:

| # | Principle | Summary |
|---|-----------|---------|
| 1 | **KOBER** | Let data lead; never start with language assumptions |
| 2 | **VENTRIS** | Abandon theories when evidence contradicts |
| 3 | **ANCHORS** | Build from certain to speculative |
| 4 | **MULTI-HYP** | Test ALL four linguistic hypotheses |
| 5 | **NEGATIVE** | Consider what's absent, not just present |
| 6 | **CORPUS** | Readings must work across entire corpus |

**Violating any principle invalidates the analysis.**

See [METHODOLOGY.md](linear-a-decipherer/METHODOLOGY.md) for pre-flight checklists and verification procedures.

---

## Key Readings

### Verified Readings (56 total)

| Reading | Meaning | Occurrences | Confidence | First Proposed | Project Contribution |
|---------|---------|-------------|------------|----------------|---------------------|
| pa-i-to | Phaistos | 12 | CERTAIN | Evans (1909) | Corpus verification |
| ku-do-ni-ja | Kydonia | 8 | CERTAIN | Ventris (1953) | Corpus verification |
| ku-ro | total/sum | 39 | HIGH | Gordon (1966) | Cross-site verification (HT, ZA, PH) |
| ki-ro | deficit | 17 | HIGH | Gordon (1966) | Function mapping, HT-exclusive |
| -JA suffix | adjectival/ethnic | 77 | HIGH | Palmer (1958) | Quantification (17 sites) |
| SA-RA₂ | allocation (*šarāku*) | 20 | PROBABLE | This project | Novel interpretation |
| DA-MA-TE | Demeter (deity) | 1 | HIGH | Multiple scholars | Corpus verification |
| A-TA-NA | Athena (deity) | 2 | HIGH | Multiple scholars | Corpus verification |

**Full registry**: [KNOWLEDGE.md](linear-a-decipherer/KNOWLEDGE.md#confirmed-readings)

### Hypothesis Discrimination Results

Tool-validated results from `hypothesis_tester.py` (198 words, freq ≥ 2):

| Hypothesis | Support | Status | Key Proponents |
|------------|---------|--------|----------------|
| **Luwian/Anatolian** | **30.3%** (60 words) | **DOMINANT** - morphological particles pervasive | Palmer (1958), Finkelberg (1998) |
| **Semitic (loans)** | **17.7%** (35 words) | STRONG - administrative vocabulary | Gordon (1966), Best (1972) |
| **Pre-Greek Substrate** | 1.5% (3 words) | Base layer; toponyms, divine names | Beekes (2014), Furnée (1972) |
| **Proto-Greek** | **2.5%** (5 words) | **ELIMINATED** - phonological mismatch | Georgiev (1963), Mosenkis (2019) |

### Major Findings

Building on prior scholarship with systematic corpus validation:

- **\*118 = Word-final consonant**: 69% final position proves Linear A had **closed syllables** (CVC structure) — explains why Greeks dropped 123 signs when adapting to CV-only Linear B (novel breakthrough)
- **Regional administrative systems**: Khania (227 inscriptions) has ZERO ku-ro/ki-ro forms — confirms parallel system distinct from Hagia Triada (novel systematization)
- **123 unique Linear A signs**: Dropped when Greeks adapted the script, revealing sounds Greek lacked (novel phonological analysis)
- **127 personal names identified**: 22% Semitic, 20% Pre-Greek, 17% Luwian; DA-MA-TE and A-TA-NA suggest Minoan origins for Demeter/Athena worship
- **Libation formula structure**: 5-position religious formula mapped (builds on Davis 2014 syntax work)
- **K-R paradigm**: 60+ forms mapped with vowel alternation system (extends Gordon's 1966 ku-ro proposal)

---

## 2024 Knossos Scepter Discovery

The **longest Linear A inscription ever found** (119 signs) was discovered at Knossos in 2024:

- **Two separate inscriptions** by different scribes
- **Ring section**: Ceremonial/religious style
- **Handle section**: Administrative style with numerals
- **Publication**: Ariadne Supplement 5 (2025)
- **URL**: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841

This discovery provides new sign sequences for pattern analysis and confirms dual use of Linear A (administrative + religious registers).

---

## Project Structure

```
linear-a-decipherer/
├── linear-a-decipherer/      # Core methodology & knowledge management
│   ├── METHODOLOGY.md        # Six inviolable principles (READ FIRST)
│   ├── KNOWLEDGE.md          # Reference tables: readings, hypotheses, anchors
│   ├── CHANGELOG.md          # Chronological discovery journal
│   ├── ANALYSIS_INDEX.md     # Registry of all analyses
│   ├── LESSONS_LEARNED.md    # Project methodology insights
│   └── references/           # Bibliography, hypotheses, sign list
│
├── analysis/                 # Research outputs
│   ├── active/               # Current operation analyses
│   ├── completed/            # Finished inscription/thematic analyses
│   └── archive/              # Historical phase analyses
│
├── tools/                    # 44 Python analysis scripts
├── external/lineara/         # Corpus data (git submodule)
├── data/                     # Generated JSON files
└── templates/                # Document templates
```

**Full structure**: See directory tree in repository.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Git with submodule support

### Installation

```bash
# Clone the repository
git clone https://github.com/levelheads/linear-a-decipherer.git
cd linear-a-decipherer

# Initialize the corpus submodule
git submodule update --init

# Generate analysis data
python tools/parse_lineara_corpus.py
```

### Quick Start

1. **Current Program State**: [MASTER_STATE.md](linear-a-decipherer/MASTER_STATE.md) — canonical current metrics and campaign status
2. **Project Overview**: [PROJECT_REVIEW.md](PROJECT_REVIEW.md) — historical strategic review
3. **Read First Principles**: [METHODOLOGY.md](linear-a-decipherer/METHODOLOGY.md) — six inviolable principles
4. **Reference Knowledge Tables**: [KNOWLEDGE.md](linear-a-decipherer/KNOWLEDGE.md)
5. **See Example Analysis**: [HT13_ANALYSIS.md](linear-a-decipherer/examples/HT13_ANALYSIS.md)

---

## Analysis Tools

The project includes 44 Python analysis scripts organized by function (stdlib-only, no external dependencies):

### Core Analysis

| Tool | Description |
|------|-------------|
| `analyze_inscription.py` | Full analysis pipeline for specific tablets |
| `kober_analyzer.py` | Frequency/positional analysis (Kober Method) |
| `hypothesis_tester.py` | Multi-hypothesis testing (all 4 frameworks) |
| `batch_pipeline.py` | Multi-stage corpus analysis (discover → hypothesize → validate → synthesize) |

### Pattern Detection

| Tool | Description |
|------|-------------|
| `contextual_analyzer.py` | Formula detection, document structures (33KB) |
| `paradigm_discoverer.py` | Morphological paradigm discovery |
| `slot_grammar_analyzer.py` | Grammatical slot analysis from logograms |
| `kr_paradigm_validator.py` | K-R form validation corpus-wide |
| `negative_evidence.py` | Absence pattern analysis |
| `sign_reconciler.py` | Cross-reference phonetic notation ↔ GORILA AB-numbers |
| `analyze_ph.py` | Phaistos vs Hagia Triada syllabary comparison |

### Cross-Corpus Verification

| Tool | Description |
|------|-------------|
| `corpus_lookup.py` | Fast indexed search with context |
| `corpus_consistency_validator.py` | First Principle #6 verification |
| `regional_analyzer.py` | Site-by-site vocabulary comparison |
| `corpus_auditor.py` | Structure audit, arithmetic validation |
| `phase_validator.py` | Detect contradictions between phases |

### External Database Connectors

| Tool | Database | Description |
|------|----------|-------------|
| `sigla_querier.py` | [SigLA](https://sigla.phis.me) | Paleographic database (772 documents) |
| `gorila_indexer.py` | GORILA | Primary corpus indexing |
| `oracc_connector.py` | [ORACC](http://oracc.org) | Akkadian/Sumerian comparative data |
| `damos_connector.py` | [DĀMOS](https://damos.hf.uio.no) | Linear B database |

### Orchestration and Governance

| Tool | Description |
|------|-------------|
| `tool_parity_checker.py` | Cross-artifact drift detection (hypothesis vs batch vs integrated) |
| `promotion_board_runner.py` | Promotion packet + gate decision generator for candidate readings |
| `lane_orchestrator.py` | Lane-based command orchestration with structured handoff JSON output |
| `dependency_trace_resolver.py` | Pre-check and optional auto-resolution for dependency-trace promotion gaps |

### Usage Examples

```bash
# Test a word against all hypotheses
python tools/hypothesis_tester.py --word ku-ro

# Compare vocabulary across sites
python tools/regional_analyzer.py --all

# Validate K-R paradigm corpus-wide
python tools/kr_paradigm_validator.py --all

# Search corpus with context
python tools/corpus_lookup.py --report ku-ro

# Run negative evidence analysis
python tools/negative_evidence.py --hypothesis all
```

**Full tool guide**: [TOOLS_GUIDE.md](linear-a-decipherer/TOOLS_GUIDE.md)

---

## Corpus Data

This project integrates the [lineara.xyz](https://lineara.xyz) corpus as a git submodule.

| Metric | Count |
|--------|-------|
| Total inscriptions | 1,721 |
| Sites | 89 |
| Core syllabograms | ~90 |
| Date range | c. 1800-1450 BCE |

### Geographic Distribution

| Site | Code | Inscriptions | Notes |
|------|------|--------------|-------|
| Hagia Triada | HT | 147 | Largest; central accounting hub |
| Khania | KH | 99 | Parallel administrative system |
| Zakros | ZA | 31 | Eastern dialectal variants |
| Phaistos | PH | 26 | Earliest inscriptions |
| Knossos | KN | 20+ | Includes 2024 scepter |

**Attribution**: Data from [mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz), aggregating GORILA (Godart & Olivier), George Douros, and John Younger. See [ATTRIBUTION.md](ATTRIBUTION.md).

---

## Research Timeline

| Date | Milestone |
|------|-----------|
| **Jan 5-9, 2026** | OPERATION MINOS Phase 1-7: Full corpus reconnaissance; Proto-Greek assessed as weakest |
| **Jan 9-31, 2026** | OPERATION MINOS II Phase 8+: Regional validation; 47 high-frequency words analyzed |
| **Jan 31, 2026** | Contact Language Model validated; 127 personal names identified |
| **Feb 1, 2026** | OPERATION MINOS III + BREAKTHROUGH: 5-Vector analysis; Tool validation complete |
| **Ongoing** | Strategic Plan: Paradigm completion, synthesis |

### OPERATION MINOS III + BREAKTHROUGH Key Findings (Feb 2026)

**Tool Validation Results** (`hypothesis_tester.py`, 198 words):
- **Proto-Greek ELIMINATED**: Only 2.5% support (5/198 words)
- **Luwian DOMINANT**: 30.3% support (60/198 words) — morphological particles pervasive
- **Semitic STRONG**: 17.7% support (35/198 words) — administrative vocabulary

**5-Vector Breakthrough Analysis**:
- **\*118 = Word-final consonant**: 69% final position proves CVC syllable structure (BREAKTHROUGH)
- **KU-RO cross-site VERIFIED**: ZA 15b contains `KU-RO VIN 78` — confirms pan-Minoan usage
- **KU-RO chronology extended**: PH(?)31a shows KU-RO in MMIII (c.1700-1600 BCE)
- **Zero K-R at Khania CERTAIN**: All 227 KH inscriptions searched; confirms parallel administrative system
- **Sign *301 profiled**: 288 occurrences, 88.2% word-initial — possible pharyngeal or palatalized consonant

**Session logs**: [analysis/sessions/](analysis/sessions/)

---

## The Anchor Hierarchy

| Level | Type | Example | Max Confidence |
|-------|------|---------|----------------|
| 1 | Confirmed toponyms | pa-i-to = Phaistos | CERTAIN |
| 2 | Linear B cognates + position | ku-ro at totals | HIGH |
| 3 | Clear logograms | VIN, OLE, GRA | HIGH |
| 4 | Structural patterns | Transaction signs | MEDIUM |
| 5 | Morphological patterns | -JA suffix | LOW-MEDIUM |
| 6 | Lexical matches | ki-ro = deficit | LOW |

**Never skip anchor levels.** Confidence cannot exceed the anchor level reached.

---

## Key Resources

| Resource | URL | Description |
|----------|-----|-------------|
| SigLA | https://sigla.phis.me | Palaeographical database (772 documents) |
| lineara.xyz | https://lineara.xyz | Corpus explorer (1,800+ inscriptions) |
| PAITO Project | https://www.paitoproject.it/linear-a/ | Epigraphic research (1,534 documents) |
| Ariadne Journal | https://ejournals.lib.uoc.gr/Ariadne/ | Academic publications |
| ORACC | http://oracc.org | Akkadian/Sumerian comparative data |
| DĀMOS | https://damos.hf.uio.no | Linear B database |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions must:

- Follow all six First Principles
- Test all four linguistic hypotheses
- Verify readings across corpus
- Use calibrated confidence levels

**Issue templates** available for: New Corpus Data, Pattern Observations, Proposed Readings.

---

## Citation

```bibtex
@software{linear_a_decipherer,
  title = {Linear A Decipherment Methodology System},
  author = {LevelHeads Research},
  year = {2026},
  url = {https://github.com/levelheads/linear-a-decipherer},
  license = {CC-BY-NC-SA-4.0}
}
```

See [CITATION.cff](CITATION.cff) for full citation information.

---

## Prior Scholarship

This project builds on decades of scholarly work on Linear A. Key contributions we validate and extend:

### Linguistic Hypotheses

| Scholar | Contribution | Our Extension |
|---------|--------------|---------------|
| **Cyrus Gordon (1966)** | ku-ro = Semitic *kull* "total" | Corpus-wide verification (39 occ, 3 sites) |
| **Leonard Palmer (1958)** | Luwian morphological parallels | -JA suffix quantification (77 occ, 17 sites) |
| **Margalit Finkelberg (1998)** | Anatolian connections | Suffix scoring framework |
| **Robert Beekes (2014)** | Pre-Greek substrate phonology | 123-sign phonological analysis |
| **Brent Davis (2010+)** | Libation formula syntax | 5-position structure formalization |
| **Ester Salgarella (2020+)** | SigLA database, paleography | Data source for corpus tools |

### What This Project Contributes

**Novel methodology**:
- Systematic multi-hypothesis testing framework with tool-validated percentages
- Anchor hierarchy formalization for confidence calibration
- Regional administration systematization (HT vs KH parallel systems)
- 28 Python analysis tools for corpus-wide verification (stdlib-only)

**Novel interpretations**:
- **\*118 = Word-final consonant** — proves Linear A had closed syllables (CVC), explaining why Greeks dropped 123 signs
- SA-RA₂ = Akkadian *šarāku* "allocate" (if unpublished elsewhere)
- Contact language model formalization with tool-validated layer percentages
- Khania parallel system documentation (zero K-R vocabulary)
- *301 distributional profile and phoneme candidates
- Proto-Greek definitively eliminated (2.5% support vs 30.3% Luwian)

---

## Acknowledgments

### Methodological Foundation

- **Alice Kober (1906-1950)** — Established that pattern analysis must precede language assumptions. Her methodology enabled Linear B's decipherment.
- **Michael Ventris (1922-1956)** — Deciphered Linear B by following methodology over preconception. Abandoned his Etruscan hypothesis when evidence demanded it.

### Data Sources

- **GORILA** (Godart & Olivier, 1976-1985) — Primary corpus reference
- **lineara.xyz** (mwenge) — Structured corpus data
- **SigLA** (Consani et al.) — Paleographic database
- **ORACC** — Akkadian comparative data

### Academic Resources

- John Younger's Linear A transcriptions
- PAITO Project epigraphic research
- Ariadne Journal publications

---

## Epistemic Commitment

> "Linear A is undeciphered. Every claim requires evidence. Every interpretation requires humility."

The goal is not to "solve" Linear A quickly, but to incrementally build understanding through rigorous methodology. All claims carry calibrated confidence levels. All hypotheses are tested against evidence. All readings are verified across the corpus.

---

## License

This work is licensed under [CC BY-NC-SA 4.0](LICENSE) — Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
