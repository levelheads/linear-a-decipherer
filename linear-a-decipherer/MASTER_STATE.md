# Master State

**Canonical operational source of truth for active status, metrics, campaigns, and release readiness.**

**Last Updated**: 2026-03-09
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
| Batch analysis coverage | 1,698/1,721 (98.66%) | `data/extended_corpus_analysis.json` |
| Hypothesis run word set | 160 words (freq >= 2) | `data/hypothesis_results.json` |
| Batch pipeline word set | 160 words | `data/batch_analysis_results.json` |
| High-confidence batch words | 28 | `data/batch_analysis_results.json` |
| Integrated validated words | 160 | `data/integrated_results.json` (run 2026-02-17) |
| Methodology compliance | 160/160 (100.0%) | `data/integrated_results.json` (run 2026-02-17) |
| Registered anchor types | 11 | `data/anchors.json` |
| Corpus validation status | PASS with 8 warnings, 0 critical errors | `data/validation_report.json` |
| Hypotheses tested | 7 | `data/hypothesis_results.json` |
| Grammatical categories identified | 27 (14 significant) | `data/ventris_grid.json` |
| Contextual formulas extracted | 87 | `data/contextual_analysis_full.json` |
| Morphological predictions tested | 481 (71 hits, 14.8%) | `data/morphological_predictions.json` |
| Infixes identified | 20 (1 known + 19 new) | `data/morphological_predictions.json` |
| Name candidates profiled | 111 (46 theophoric) | `data/onomastic_analysis.json` |
| Admin template comparisons | 36 (6x6 grid) | `data/admin_isomorphism.json` |
| Falsification: Active hypotheses | 2/7 (Luwian STRONG 35.0%, Semitic MODERATE 17.5%) | `data/falsification_report.json` |
| Falsification: Eliminated | 5/7 (Proto-Greek, Pre-Greek, Hurrian, Hattic, Etruscan) | `data/falsification_report.json` |
| Bayesian top posterior | Luwian 0.316, Isolate 0.299, Semitic 0.130 | `data/bayesian_corpus_results.json` |
| Negative evidence ranking | Luwian +3.5 > Hurrian +2.5 > Hattic/Etruscan +0.5 > Greek -15.0 | `data/negative_evidence_report.json` |
| Commodity functional anchors | 7 strong + 7 candidates | `data/commodity_anchors.json` |
| KU-RO arithmetic verified | 7/34 VERIFIED + 4 CONSTRAINED + 4 STRUCTURAL + 5 NEAR-MATCH | `data/arithmetic_verification.json` + mismatch_investigation.md |
| KU-RO mismatches investigated | 18/18 (all diagnosed) | `analysis/completed/thematic/mismatch_investigation.md` |
| Reading attempts completed | 55 tablets + 7 thematic | `analysis/completed/inscriptions/*_READING.md` |
| Cross-site readings | 30 (ZA×7, PEZ, IO, PH×6, SAMW, PK, KH×12, SY) | `analysis/completed/inscriptions/` |
| Sites with readings | 9 (HT, ZA, PEZ, IO, PH, SAMW, PK, KH, SY) | `analysis/completed/inscriptions/` |
| Cross-tablet name links | 13 confirmed | `analysis/completed/thematic/cross_tablet_network.md` |
| KU-RO scope typology | 3 types (grand, per-commodity, section) | `analysis/completed/thematic/mismatch_investigation.md` |
| PO-TO-KU-RO verified | 97 = 31+65+1 (HT122a+b) | First cross-tablet grand total |
| KH zero-K-R confirmed | p=0.004, n=226 | `analysis/completed/thematic/khania_expansion.md` |
| Domain layering confirmed | Religious=Luwian, Admin=Semitic | `analysis/completed/thematic/linguistic_deep_analysis.md` |
| Tool count (Python scripts) | 56 | `tools/*.py` |
| Current release version | v0.10.0 | `CITATION.cff`, local tags |

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
| Falsification thresholds | `python tools/falsification_system.py --all --output data/falsification_report.json` | `data/falsification_report.json` |
| Bayesian posteriors | `python tools/bayesian_hypothesis_tester.py --corpus --output data/bayesian_corpus_results.json` | `data/bayesian_corpus_results.json` |
| Negative evidence | `python tools/negative_evidence.py --hypothesis all --output data/negative_evidence_report.json` | `data/negative_evidence_report.json` |
| Ventris Grid | `python tools/structural_grid_builder.py --output data/ventris_grid.json` | `data/ventris_grid.json` |
| Admin isomorphism | `python tools/admin_isomorphism_scorer.py --output data/admin_isomorphism.json` | `data/admin_isomorphism.json` |
| Morphological predictions | `python tools/morphological_predictor.py --output data/morphological_predictions.json` | `data/morphological_predictions.json` |
| Onomastic comparison | `python tools/onomastic_comparator.py --output data/onomastic_analysis.json` | `data/onomastic_analysis.json` |
| Reading readiness | `python tools/reading_readiness_scorer.py --all --output data/reading_readiness.json` | `data/reading_readiness.json` |
| Arithmetic verification | `python tools/arithmetic_verifier.py --all --output data/arithmetic_verification.json` | `data/arithmetic_verification.json` |
| Commodity validation | `python tools/commodity_validator.py --all --output data/commodity_anchors.json` | `data/commodity_anchors.json` |

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

**Status**: MAINTENANCE (2026-02-17)
**Goal**: Refine base-language model through adversarial hypothesis testing.
**Note**: 5/7 hypotheses eliminated; focus on Luwian (STRONG) + Semitic (MODERATE) only. Reduced to maintenance — re-run validators only when new evidence surfaces.

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

### Lane G: Reading Attempts

**Status**: ACTIVE (2026-02-28)
**Goal**: Produce connected readings of specific tablets using accumulated evidence.

**Completed (v0.7.0)**:
1. HT 85a reading — VIR allocation, KU-RO=66 VERIFIED, 7 recipients (A-DU contributor)
2. HT 117a reading — Personnel list, KU-RO=10 VERIFIED, dual KI-RO+KU-RO, 3-section structure
3. HT 9b reading — Connected reading with arithmetic verification
4. Libation formula complete alignment — 34 inscriptions, 14 sites, Form A/B paradigm

**Completed (v0.8.0)**:
5. HT 92 reading — Minimal GRA distribution, A-DU 680 GRA + *304 12, NO_KURO, 100% identified
6. HT 86a reading — Two-section GRA distribution, 6 anchors, 87.5% coverage, dual commodity anchor validation
7. HT 7a reading — VIR allocation, NO_KURO, 5 recipients (QE-TI header), all Luwian-leaning
8. ZA 15b reading — Cross-site KU-RO (Zakros), VIN 78 + VIN+RA 17, first non-HT reading
9. HT 94b reading — KI-RO deficit list, KU-RO=5 VERIFIED (exact), dual KI-RO+KU-RO, post-total *86 section, Scribe 9
10. HT 102 reading — Large-scale GRA distribution, KU-RO=1060 MISMATCH (lacuna), SA-RA₂ 976 GRA (92%), two-tier grain, Scribe 5
11. HT 9a reading — VIN distribution (partner to HT 9b), KU-RO=31.75 MISMATCH (0.75=J+E), 7 recipients, 5 shared with side b, SA-RO S-R paradigm
12. HT 13 reading — Largest VIN distribution (130.5 units), KU-RO MISMATCH (-0.5), TE-TU 43%, Scribe 8, 2 hapax

**Completed (v0.9.0 — Operation MINOS III)**:
13. HT 122a reading — "Rosetta Tablet", KU-RO=31, PO-TO-KU-RO=97 VERIFIED (31+65+1), 8 cross-refs, Scribe 9
14. HT 11b reading — KA commodity, KU-RO=180 VERIFIED (Class A), DE-NU header, Scribe 24
15. HT 95a reading — GRA distribution, NO_KURO, KU-NI-SU+DA-ME anchors, 5/6 shared with HT86a
16. HT 95b reading — GRA distribution from A-DU, NO_KURO, 6/6 shared with HT95a (same grain cohort)
17. PEZg5 reading — First Petras reading, OLE *307 1.5, stone object
18. IOZa9 reading — Iouktas libation tablet, religious register
19. PH12a reading — Phaistos, VIR-*339-HIDE compound (leather workers?), 10 units
20. SAMWa1 reading — Only non-Cretan inscription (Samothrace), MMII, JA-SA SA-RA TE 10 1/16
21. PKZa27 reading — Palaikastro libation formula (JA-SA-SA-RA-ME / U-NA-KA-NA-SI)
22. KH22 reading — First Khania reading, CYP copper allocation, zero K-R confirmed
23. KH50 reading — Khania distribution record, zero K-R, distinctive admin vocabulary
24. ZA6a reading — Zakros mixed commodity (OLIV, GRA, *304), stone vessel
25. SYZa2 reading — Kato Symi religious variant, libation formula site
26. HT11a reading — Multi-section mixed distribution, KU-RO=10 CONSTRAINED, Scribe 24, paired with HT11b
27. ZA4a reading — Zakros, stone vessel
28. HT86b reading — GRA+K+L distribution partner to HT86a, A-KA-RU header, Scribe 6
29. HT106 reading — CYP copper account, MI-NU-TE CYP 6, Scribe 19
30. ZA11a reading — Zakros, 3 anchored
31. KH11 reading — Largest KH tablet, A-DU header (first KH occurrence!), mixed CYP+VIN, zero K-R
32. KH29 reading — Khania CYP allocation with fractions, RA header, KU-PA in non-GRA context
33. PH3a reading — Phaistos object inventory, 4 undeciphered logograms (*556, *557, *560, *563)
34. PH3b reading — Phaistos fractional commodity record, MI+JA compound, pair with PH3a
35. HT123+124a reading — Three-column OLIV/oil ledger, OLIV KU-RO=93.5 VERIFIED, *308=olive oil, Scribe 6
36. HT116a reading — Richest commodity variety (7 types), PU-RA₂ 40%, *304 column VERIFIED (15)
37. HT10a reading — KU-NI-SU role reversal (recipient→source), DA-RI-DA/DA-RE cross-refs
38. HT28a reading — SA-RA₂ allocation, 5 OLE variants (most ever), A-SI-JA-KA header
39. HT88 reading — KI-RO arithmetic proof (20-13-6=1), KU-RO=6 VERIFIED (section), A-DU VIR+KA, Scribe 7
40. HT104 reading — KU-RO=95 VERIFIED, -TI suffix pattern, complete vocabulary isolation
41. HT28b reading — Debt counterpart to HT28a, U-MI-NA-SI qualifier, proto-double-entry
42. HT1 reading — Largest-scale distribution (533+), QE-RA₂-U role reversal, KI-RO=197, Scribe 21
43. Thematic: Cross-tablet network analysis — 13+ confirmed cross-tablet name links, 3-tier admin hierarchy
44. Thematic: Mismatch investigation — 18/18 KU-RO mismatches diagnosed, 4 reclassified STRUCTURAL
45. Thematic: Khania expansion — 226 KH inscriptions scanned, zero-K-R confirmed (p=0.004), CYP grading system mapped
46. Thematic: Linguistic deep analysis — domain layering confirmed, Bayesian stable, *301=/kya/ maintained
47. Thematic: Anchor consolidation — KU-RO HIGH confirmed, SA-RA₂ PROBABLE, A-DU PROBABLE, NI held

**Completed (v0.10.0 — Operation MINOS IV)**:
48. KH5 reading — CYP grading + Luwian names, WI-SA-SA-NE Pre-Greek geminate, double-name header, zero K-R
49. KH6 reading — Pure CYP+D tablet, 5/5 fractional pattern, AU-RE-TE Luwian, zero K-R
50. KH7a reading — ONLY KH tablet with CYP+D+E together, CYP grading revision (quality not format), VIR+*313b labor
51. KH7b reading — CYP+K copper variant (3rd grade), Luwian names, companion to KH7a
52. KH8 reading — Most commodity-diverse KH tablet (7+ types), NI confirmed, GRA at Khania
53. KH9 reading — VIR+*307 labor + CYP three-tier grading, NI confirmed 3rd KH tablet
54. KH86 reading — Pure unqualified CYP (no grade), RE-ZA Luwian -ZA suffix
55. KH88 reading — NI 10 (largest KH wine), QA-NU-MA Luwian header, bulk allocation
56. PH1a reading — CYP at Phaistos, DI-RA-DI-NA reduplicated name, *316 Phaistos-specific
57. PH6 reading — Pure onomastic register (3 I-prefix names), A-RI recurring element, Luwian SUPPORTED
58. PH8a reading — Sectional accounting, Phaistos-unique logograms (*416+L2, *418+L2), zero syllabographic words
59. ZA10b reading — 13-entry ranked allocation (pan-Minoan template), 4 Luwian names at ZA
60. ZA1a reading — NI 42½ (LARGEST wine quantity in corpus), KI-RE-ZA institutional
61. ZA5b reading — Domain layering at name level (SI-PI-KI Semitic 4.15 + MA-KA-I-TA Luwian)
62. Thematic: Inflectional morphology — Suffix paradigms mapped, K-R/S-R transparent, suffixing language confirmed
63. Thematic: Khania administrative system — Distinct KH accounting tradition, CYP grading = quality, zero K-R explained

**Next priorities**:
1. Tier 3 HT readings (remaining high-readiness tablets)
2. NI promotion (packet prepared, awaiting formal registration)
3. Cross-site deepening (IO, PK, SY religious register analysis)
4. CYP grading system formalization across KH corpus

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
| HT concentration bias in core terms | Low | Regional weighting required in promotion packets; HT batch coverage rebalanced to 98.66% (v0.8.0, 2026-02-21) |
| Incomplete context metadata in corpus | Medium | Track warning deltas from `validate_corpus.py` each run |
| Legacy docs with stale metrics | Medium | Historical redirect banners + canonical state enforcement |
| Ambiguous sign functions with mixed roles | High | Maintain dual-role analyses with explicit falsification criteria |
| External release visibility gaps (API/network limits) | Low | Include manual GitHub release audit step when online |

---

## Release Readiness Snapshot

| Check | Status | Evidence |
|-------|--------|----------|
| Local tags align with CITATION version lineage | PASS | tags `v0.2.0`, `v0.3.0`, `v0.4.0`, `v0.4.1`, `v0.5.0`, `v0.6.0`, `v0.6.1`, `v0.7.0` |
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
