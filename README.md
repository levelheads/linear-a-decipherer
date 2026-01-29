# Linear A Decipherer

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

A rigorous methodology system for analyzing undeciphered Minoan Bronze Age inscriptions (c.1800-1450 BCE) from Crete.

## Overview

**Linear A remains undeciphered.** This project approaches it as an active research problem, not a solved puzzle.

The system uses a methodology derived from the successful Linear B decipherment to systematically analyze patterns, test competing linguistic hypotheses, and generate novel interpretations with calibrated confidence levels.

## Key Features

- **Evidence-based reasoning chains** - Every interpretation documented with explicit evidence
- **Multi-hypothesis testing** - All readings tested against Luwian, Semitic, Pre-Greek, and Proto-Greek frameworks
- **Anchor-based expansion** - Building from confirmed toponyms and Linear B cognates outward
- **Corpus-wide verification** - Proposed readings validated across all occurrences
- **Calibrated confidence** - Explicit uncertainty quantification for all claims

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

## Project Structure

```
linear-a-decipherer/
├── README.md                 # This file
├── LICENSE                   # CC BY-NC-SA 4.0
├── CONTRIBUTING.md           # Contribution guidelines (First Principles required)
├── CITATION.cff              # Academic citation format
├── CLAUDE.md                 # AI assistant guidance
│
├── linear-a-decipherer/      # Core methodology
│   ├── FIRST_PRINCIPLES.md   # Six inviolable principles (READ FIRST)
│   ├── SKILL.md              # Operational procedures
│   ├── references/
│   │   ├── methodology.md    # Analytical techniques (Kober Method)
│   │   ├── hypotheses.md     # Four linguistic frameworks
│   │   ├── corpus.md         # Inscription database
│   │   └── sign_list.md      # Linear A syllabary
│   └── examples/
│       ├── HT13_COMPLETE_ANALYSIS.md
│       └── HT13_QUICK_START.md
│
├── analyses/                 # Research outputs
│   ├── LINEAR_A_COMPREHENSIVE_ANALYSIS.md
│   ├── KNOSSOS_SCEPTER_ANALYSIS.md
│   ├── KOBER_METHOD_ANALYSIS_2026-01-09.md
│   └── CORPUS_DATA_2026-01-09.md
│
├── external/                 # External data (git submodules)
│   └── lineara/              # lineara.xyz corpus data
│
├── tools/                    # Analysis scripts
│   ├── analyze_inscription.py    # Full analysis pipeline
│   ├── corpus_lookup.py          # Query inscriptions
│   ├── enrich_chronology.py      # Chronological context
│   ├── hypothesis_tester.py      # Multi-hypothesis testing
│   ├── kober_analyzer.py         # Frequency/positional analysis
│   ├── parse_lineara_corpus.py   # Corpus data generator
│   ├── statistical_analysis.py   # Pattern detection
│   └── validate_corpus.py        # Corpus integrity checks
│
├── data/                     # Generated data (gitignored)
│   ├── corpus.json           # Parsed inscription data (1,721 entries)
│   ├── cognates.json         # Linear B cognate mappings
│   ├── signs.json            # Sign inventory
│   ├── statistics.json       # Corpus statistics
│   ├── chronology_enrichment_report.json
│   ├── hypothesis_results.json
│   ├── pattern_report.json
│   ├── statistical_report.json
│   └── validation_report.json
│
├── sessions/                 # Session logs
│   ├── SESSION_LOG_2026-01-05.md
│   └── SESSION_LOG_2026-01-09.md
│
└── .github/
    └── ISSUE_TEMPLATE/       # Templates for contributions
        ├── proposed-reading.md
        ├── pattern-observation.md
        └── new-corpus-data.md
```

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

# Generate analysis data (outputs to data/, ~2MB)
python tools/parse_lineara_corpus.py
```

### Verify Setup

After running the commands above, you should have:

| Directory/File | Contents |
|----------------|----------|
| `external/lineara/` | Corpus data from lineara.xyz |
| `data/corpus.json` | Parsed inscriptions (1,721 entries) |
| `data/cognates.json` | Linear B cognate mappings |
| `data/signs.json` | Sign inventory |

## Quick Start

1. **Read First Principles**: `linear-a-decipherer/FIRST_PRINCIPLES.md`
2. **Review Methodology**: `linear-a-decipherer/references/methodology.md`
3. **See Example Analysis**: `linear-a-decipherer/examples/HT13_QUICK_START.md`
4. **Explore Corpus Data**: `analyses/CORPUS_DATA_2026-01-09.md`
5. **See Pattern Analysis**: `analyses/KOBER_METHOD_ANALYSIS_2026-01-09.md`

## Corpus Data

This project integrates the [lineara.xyz](https://lineara.xyz) corpus as a git submodule, providing structured access to 1,700+ inscriptions.

**Generated Files** (in `data/`, gitignored - regenerate with `python tools/parse_lineara_corpus.py`):

| File | Description |
|------|-------------|
| `corpus.json` | Full inscription data (1,721 inscriptions, 89 sites) |
| `cognates.json` | Linear B cognate mappings (231 words, 191 roots) |
| `signs.json` | Sign inventory with frequencies |
| `statistics.json` | Corpus statistics and word frequencies |
| `hypothesis_results.json` | Multi-hypothesis test results |
| `pattern_report.json` | Kober Method pattern analysis |
| `chronology_enrichment_report.json` | Temporal context data |
| `statistical_report.json` | Statistical analysis output |
| `validation_report.json` | Corpus integrity checks |

**Attribution**: Data from [mwenge/lineara.xyz](https://github.com/mwenge/lineara.xyz), which aggregates GORILA (Godart & Olivier), George Douros, and John Younger. See [ATTRIBUTION.md](ATTRIBUTION.md).

## The Anchor Hierarchy

| Level | Type | Example | Max Confidence |
|-------|------|---------|----------------|
| 1 | Confirmed toponyms | pa-i-to = Phaistos | CERTAIN |
| 2 | Linear B cognates + position | ku-ro at totals | HIGH |
| 3 | Clear logograms | VIN, OLE, GRA | HIGH |
| 4 | Structural patterns | Transaction signs | MEDIUM |
| 5 | Morphological patterns | -jo genitive? | LOW-MEDIUM |
| 6 | Lexical matches | ki-ro = deficit | LOW |

## Key Resources

| Resource | URL | Description |
|----------|-----|-------------|
| SigLA | https://sigla.phis.me | Palaeographical database (772 documents) |
| lineara.xyz | https://lineara.xyz | Corpus explorer (1,800+ inscriptions) |
| PAITO Project | https://www.paitoproject.it/linear-a/ | Epigraphic research (1,534 documents) |
| Ariadne Journal | https://ejournals.lib.uoc.gr/Ariadne/ | Academic publications |

## Current Research Status

**Verified Anchors**:
- pa-i-to = Phaistos (Level 1, CERTAIN)
- ku-ro = "total" (Level 2, HIGH, 50+ occurrences)
- ki-ro = "deficit" (Level 2, HIGH, 30+ occurrences)

**Pattern Findings**:
- K-R root paradigm (ku-ro, ki-ro, ka-i-ro) suggests morphological system
- -SI/-TI alternation in libation formulas may indicate verbal conjugation
- Proto-Greek hypothesis remains WEAK (negative evidence)

**Best-Fit Model**: Contact language (Pre-Greek base + Semitic administrative loans)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. All contributions must:
- Follow First Principles
- Test all four linguistic hypotheses
- Verify readings across corpus
- Use calibrated confidence levels

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

## Historical Context

- **Alice Kober (1906-1950)** - Established that pattern analysis must precede language assumptions
- **Michael Ventris (1922-1956)** - Deciphered Linear B by following methodology over preconception

Their methodology succeeded where decades of speculation failed. This project applies those lessons to Linear A.

## Epistemic Commitment

> "Linear A is undeciphered. Every claim requires evidence. Every interpretation requires humility."

The goal is not to "solve" Linear A quickly, but to incrementally build understanding through rigorous methodology.

## License

This work is licensed under [CC BY-NC-SA 4.0](LICENSE) - Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International.
