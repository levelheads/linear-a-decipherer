# Master State

**Canonical operational source of truth for active status, metrics, campaigns, and release readiness.**

**Last Updated**: 2026-02-13
**Scope**: Current state only (not full historical narrative)
**Historical log**: `linear-a-decipherer/CHANGELOG.md`

---

## Canonical Rule

This file is the authoritative current-state view for:

1. Program metrics and baselines
2. Active decipherment campaigns and priorities
3. Promotion gates for readings
4. Risks, blockers, and dependency-critical constraints
5. Release readiness

If any other file conflicts with this one, this file wins.

---

## Metrics Snapshot

| Metric | Current Value | Source |
|--------|---------------|--------|
| Total corpus inscriptions | 1,721 | `data/corpus.json` |
| Batch analysis coverage | 300/1,721 (17.43%) | `data/extended_corpus_analysis.json` |
| Hypothesis run word set | 198 words (freq >= 2) | `data/hypothesis_results.json` |
| Batch pipeline word set | 248 words | `data/batch_analysis_results.json` |
| High-confidence batch words | 42 | `data/batch_analysis_results.json` |
| Integrated validated words | 160 | `data/integrated_results.json` (run 2026-02-13) |
| Methodology compliance | 6/160 (3.8%) | `data/integrated_results.json` (run 2026-02-13) |
| Corpus validation status | PASS with 8 warnings, 0 critical errors | `data/validation_report.json` |
| Tool count (Python scripts) | 41 | `tools/*.py` |
| Current release version | v0.4.1 | `CITATION.cff`, local tags |

---

## Metric Source Map

| Domain | Command | Output Artifact |
|--------|---------|-----------------|
| Corpus parse | `python tools/parse_lineara_corpus.py` | `data/corpus.json`, `data/statistics.json` |
| Corpus quality | `python tools/validate_corpus.py` | `data/validation_report.json` |
| Hypothesis discrimination | `python tools/hypothesis_tester.py --all --min-freq 2` | `data/hypothesis_results.json` |
| Batch throughput | `python tools/batch_pipeline.py --full` | `data/batch_analysis_results.json` |
| Coverage extension | `python tools/extended_corpus_analyzer.py --all` | `data/extended_corpus_analysis.json` |
| Cross-corpus consistency | `python tools/corpus_consistency_validator.py --all --min-freq 5 --output data/consistency_validation.json` | `data/consistency_validation.json` |
| Integrated compliance | `python tools/integrated_validator.py --all --output data/integrated_results.json` | `data/integrated_results.json` |
| Index refresh | `python tools/update_index.py --write` | `linear-a-decipherer/ANALYSIS_INDEX.md` |

---

## Active Campaigns

### Lane A: SSOT + Governance

**Status**: IN PROGRESS
**Goal**: Eliminate conflicting operational truth and metric drift.

Current focus:

1. Canonical file in place (`MASTER_STATE.md`)
2. Legacy status docs marked historical and redirected
3. CI drift checks for canonical governance

### Lane B: Validation and Quality Gates

**Status**: IN PROGRESS
**Goal**: Prevent promotion of claims without full methodology checks.

Current focus:

1. CI runs consistency/integrated validators with explicit execution flags
2. Drift/health script verifies SSOT structure and redirect banners
3. Promotion packet template enforced before upgrades

### Lane C: Script Asymmetry Campaign

**Status**: ACTIVE
**Goal**: Decode high-leverage signs/functions using structure-first evidence.

Priority sequence:

1. *304
2. *21F/*21M
3. *118 extensions
4. *188 and *86 compounds

### Lane D: Language Asymmetry Campaign

**Status**: ACTIVE
**Goal**: Refine base-language model through adversarial hypothesis testing.

Priority sequence:

1. High-frequency administrative terms under regional penalties
2. Religious register terms (cross-site sanctuaries)
3. Contact-layer chronology stress tests

### Lane E: Corpus Throughput Engine

**Status**: ACTIVE
**Goal**: Increase coverage with site diversification while preserving quality gates.

Current throughput target:

1. Weekly mixed batch + deep-dive cadence
2. Non-HT site balancing in queue selection
3. Coverage and site-bias report each cycle

### Lane F: Release and Process Excellence

**Status**: IN PROGRESS
**Goal**: Make releases impossible to publish with state/version inconsistencies.

Current focus:

1. Strict CI release checks
2. CITATION/tag alignment
3. Canonical-state required for release readiness

---

## Promotion Board

No reading may be promoted without a complete evidence packet.

### Required Promotion Inputs

1. Hypothesis result (`data/hypothesis_results.json`)
2. Cross-corpus consistency report (`data/consistency_validation.json`)
3. Integrated validation report (`data/integrated_results.json`)
4. Anchor/dependency review (`data/reading_dependencies.json`, `data/anchors.json`)
5. Negative-evidence statement (explicit)
6. Regional concentration statement (explicit, if applicable)

### Promotion Gates

| Target Tier | Minimum Gate |
|-------------|--------------|
| SPECULATIVE -> POSSIBLE | Multi-hypothesis run + no direct anchor contradiction |
| POSSIBLE -> PROBABLE | Cross-corpus consistency + integrated validation + dependency trace |
| PROBABLE -> HIGH | Strong cross-site behavior or justified regional constraint + integrated pass + no unresolved critical contradiction |
| HIGH -> CERTAIN | Multiple independent anchors + broad corpus consistency + zero unresolved critical contradictions |

---

## Current Risks and Blockers

| Risk | Severity | Mitigation |
|------|----------|------------|
| HT concentration bias in core terms | High | Regional weighting required in promotion packets |
| Incomplete context metadata in corpus | Medium | Track warning deltas from `validate_corpus.py` each run |
| Legacy docs with stale metrics | Medium | Historical redirect banners + canonical state enforcement |
| Ambiguous sign functions with mixed roles | High | Maintain dual-role analyses with explicit falsification criteria |
| External release visibility gaps (API/network limits) | Low | Include manual GitHub release audit step when online |

---

## Release Readiness Snapshot

| Check | Status | Evidence |
|-------|--------|----------|
| Local tags align with CITATION version lineage | PASS | tags `v0.2.0`, `v0.3.0`, `v0.4.0`, `v0.4.1` |
| CITATION version/date present | PASS | `CITATION.cff` |
| Validator commands in CI use execution flags | TARGETED | `.github/workflows/validate.yml` |
| Canonical-state guard enabled in CI | TARGETED | `.github/workflows/validate.yml` |
| Legacy status docs redirected | TARGETED | top-banner checks in guard script |

---

## Online Release Audit

Latest local check date: 2026-02-13
Status: GitHub API not reachable from local environment during planning run.

When network is available:

1. Run `gh release list --limit 20`
2. Compare published releases vs local tags
3. Confirm release notes reflect canonical metrics
4. Record result in this section

---

## Update Protocol

1. Refresh metric artifacts via toolchain.
2. Update this file in one commit with clear date.
3. If promoting/demoting readings, include promotion packet reference.
4. Add historical detail to `CHANGELOG.md` (not here).
5. Keep this file concise and decision-oriented.
