# Corpus Access Readiness Audit

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_corpus_access_readiness_audit.json`

## Verdict

Readiness status: **sufficient for the next local analysis cycle, with known gaps**.

## Corpus Access Snapshot

- Core corpus inscriptions: `1,721`
- Submodule status: `external/lineara` present and pinned (`eb9afc7...`)
- Parse health: `0` parse-error flags
- Unique site codes: `89`
- Support types: `19`

Top concentration:
- `HTW`: `893`
- `HT`: `199`
- `KHW`: `121`
- `KH`: `104`

HT-cluster share (`HTW+HT+HTZ`): `~64.5%` of corpus.

## Comparative Data Access

Local comparative corpora are available without network:
- SigLA static sign DB: `84` signs (`data/sigla/sign_database.json`)
- DĀMOS verification DB: `35` vocabulary entries, `231` cognate words (`data/linear_b/cognate_verification.json`)
- ORACC comparative DB: `104` terms (`data/comparative/akkadian_oracc.json`)
- GORILA local index: `166` indexed inscriptions (`data/gorila/index.json`)

## Quality and Coverage Gaps

Validation summary (`data/validation_report.json`):
- Critical errors: `0`
- Warnings: `8`

Key data-quality gaps:
- Missing context metadata: `331` inscriptions
- Missing site metadata: `3` inscriptions
- Empty transliteration records: `9` inscriptions

Coverage state:
- Extended analysis coverage: `500/1721` (`29.05%`)
- HT site deep-coverage remains low in extended queue (`~3.96%` in that workflow), despite large corpus share.

## Impact on Decipherment Velocity

1. We can continue serious local analysis immediately.
2. New ritual-slot discoveries are now corpus-limited, not tooling-limited.
3. Missing context metadata reduces confidence in chronology-conditioned tests.
4. HT-heavy concentration still risks overfitting unless queue diversification is enforced.

## Setup Tasks To Execute Next

1. Add a repeatable refresh runbook:
- `git submodule update --init --remote`
- `python tools/parse_lineara_corpus.py`
- `python tools/validate_corpus.py`

2. Add a metadata remediation ledger:
- Track and triage `missing context/site/empty transliteration` records
- Define explicit exclusion rules for validators

3. Rebalance corpus queue for decipherment gain:
- Prioritize non-HT ritual-support inscriptions for substitution discovery
- Keep HT throughput for administrative baselines only

4. Version comparative snapshots:
- Rebuild and stamp ORACC/SigLA/DĀMOS artifacts each cycle
- Preserve previous snapshot hashes for drift detection
