# Engineering Practices

Project management lessons for the Linear A Decipherment Project.

**Last Updated**: 2026-02-17

---

## Release Management Lessons

### CITATION.cff Synchronization (2026-02-02)

**Lesson**: Update CITATION.cff BEFORE creating release tags

**Problem**: Created v0.3.0 tag with CITATION.cff still showing v0.2.0.

**Fix**: CITATION.cff update must be part of the release commit, not a follow-up.

### Pre-commit Hook Versions (2026-02-02)

**Lesson**: Run `pre-commit autoupdate` before releases

**Problem**: Hardcoded v4.5.0 when v6.0.0 was available.

**Fix**: Quarterly or before each release, run autoupdate.

### Configuration Hygiene (2026-02-02)

**Lesson**: Review configs for duplicate blocks

**Problem**: Duplicate repo entries in .pre-commit-config.yaml.

**Fix**: Scan config files before committing changes.

---

## Plan Verification Lessons

### File-by-File Verification (2026-02-02)

**Lesson**: Explicitly verify every file mentioned in implementation plans

**Problem**: Plan mentioned CITATION.cff but verification was incomplete.

**Fix**: After implementation, check each file against plan.

---

## Checklists

See GIT_WORKFLOW.md for:
- Release Checklist
- Pre-commit Hygiene Checklist
- Plan Verification Checklist

## Canonical State Practice

Current operational truth (metrics, active campaigns, release readiness) must be
maintained in `linear-a-decipherer/MASTER_STATE.md`.

Historical detail belongs in `linear-a-decipherer/CHANGELOG.md`.

---

## BREAKTHROUGH Sprint Lessons (2026-02-17)

### Hypothesis List Maintenance

**Lesson**: When extending hypothesis tools, check ALL companion tools for hardcoded hypothesis lists

**Problem**: Extended `hypothesis_tester.py` from 4→7 hypotheses, but `falsification_system.py`, `negative_evidence.py`, and `bayesian_hypothesis_tester.py` still had hardcoded 4-hypothesis lists.

**Fix**: Grep for hypothesis name strings across all `tools/*.py` files before declaring extension complete. All hypothesis-facing tools must share the same hypothesis enum.

### POSSIBLE Verdict Semantics

**Lesson**: POSSIBLE = neutral, not contradicted

**Problem**: Verdict aggregation in `hypothesis_tester.py` counted POSSIBLE as "contradicted," causing systematic under-scoring and incorrect rankings.

**Fix**: POSSIBLE verdicts contribute zero to contradiction count. Only explicit CONTRADICTED counts against. This single bug fix changed the entire hypothesis ranking landscape.

### Archive Discipline

**Lesson**: `_pre_sprint` naming convention works well; use consistently for before/after snapshots

**Problem**: Stale `*_pre_sprint.json` and `*_prefix.json` files accumulated in `data/`, causing confusion about which files were current.

**Fix**: Archive superseded data files to `data/archive/` promptly. Name convention: `{name}_pre_{event}.json` for snapshots.

### Data File Lifecycle

**Lesson**: Superseded JSON files must be archived promptly to prevent stale-data bugs

**Problem**: Multiple tools could read the wrong version of a data file (e.g., `bayesian_results.json` vs `bayesian_corpus_results.json`).

**Fix**: When a new output supersedes an old one, archive the old file in the same commit.

---

## Tool Development Lessons (Consolidated from LESSONS_LEARNED.md)

### Commodity Distribution Before Semantics (2026-01-31)

**Lesson**: Check commodity distribution BEFORE proposing word meanings

If a word appears with multiple commodity types, it's NOT a commodity name — it must be a transaction category, qualifier, or administrative term.

### Complementary Distribution Verification (2026-01-31)

**Lesson**: Don't assume complementary distribution — actively search for co-occurrence counter-examples

Found 5 inscriptions with BOTH KU-RO and KI-RO, disproving initial complementary distribution assumption.

### Tool Parity (2026-02-01)

**Lesson**: All tools analyzing the same corpus must use identical filtering logic

75% discrepancy between `batch_pipeline.py` and `hypothesis_tester.py` rankings was caused by different word filtering (single-syllables inflating scores). Use `word_filter_contract.py` for consistency.

### Score Inflation via Noise (2026-02-01)

**Lesson**: Exclude single-syllable tokens and logograms from hypothesis testing

Single syllables (KU, KA, SI) match multiple hypothesis patterns by chance, completely inverting rankings.

### Evidence Level Discipline (2026-02-01)

**Lesson**: A claim cannot be more certain than its weakest dependency

Track dependency chains explicitly. If Claim A depends on Claim B, and B is SPECULATIVE, then A cannot exceed SPECULATIVE.

### Internal Contradiction Detection (2026-02-01)

**Lesson**: Check scholarly literature for internal contradictions before adopting claims

Example: Cambridge publication claims both "-RU/-RE = Greek -os ending" AND "Minoan is isolated" — mutually contradictory.

---

## Reading Attempt Lessons (2026-02-17)

### Arithmetic Verification as Foundation

**Lesson**: Always start reading attempts with arithmetic verification before attempting semantic interpretation

Tablets with VERIFIED KU-RO arithmetic (exact match) provide a structural skeleton that constrains all subsequent interpretation. HT 85a (66=66) and HT 117a (10=10) were the most productive reading attempts precisely because their arithmetic was provably correct.

### Reading Readiness Scoring

**Lesson**: Score tablets before attempting readings — readability varies enormously

Most tablets in the corpus score below 0.3 readiness due to missing evidence. The top 10 tablets (0.7+) yield productive readings; attempting readings on low-score tablets wastes effort.

### Commodity Anchors Are Language-Independent

**Lesson**: Commodity-word co-occurrence provides functional identification regardless of language hypothesis

The 6 strong anchors (100% specificity) tell us WHAT a word does (e.g., KU-NI-SU = grain-associated term) without requiring any language assumption. These are the most robust type of evidence after arithmetic proof.

### Scribe Identification Enables Cross-Tablet Validation

**Lesson**: When the same scribe writes multiple tablets, arithmetic precision and structural conventions cross-validate

HT Scribe 9 produced both HT 85a and HT 117a; both verify exactly. This provides evidence that the scribal system maintained arithmetic integrity as a convention, not just on individual tablets.
