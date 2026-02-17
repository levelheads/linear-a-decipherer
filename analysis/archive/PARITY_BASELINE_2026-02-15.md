# Parity Baseline (2026-02-15)

## Scope
Cross-pipeline parity snapshot for:
- `tools/hypothesis_tester.py`
- `tools/batch_pipeline.py`
- `tools/integrated_validator.py`
- evaluated via `tools/tool_parity_checker.py`

## Baseline History (same day)

| Snapshot | Status | Max Support Delta | Max Word Mismatch | Notes |
|---|---|---:|---:|---|
| Pre-contract (earlier run) | HIGH | 25.85% | 66.87% | Divergent token filters and mixed ranking semantics |
| Mid-fix (contract only) | HIGH | 20.63% | 66.87% | Shared eligibility applied; ranking semantics still inconsistent |
| Post-contract + parity fix | LOW | 0.00% | 0.00%* | Shared eligibility + aligned best-assignment metrics |

\* Internal `integrated_raw_best` vs `integrated_bayesian_best` contrast remains analytically useful but is excluded from parity severity because it is not inter-tool drift.

## Key Changes That Produced Reduction
1. Added shared word filter contract in `tools/word_filter_contract.py` and wired it into all hypothesis pipelines.
2. Aligned batch hypothesis support counting with `hypothesis_tester` synthesis thresholds.
3. Added `best_assignments` to batch synthesis output so parity comparisons use equivalent semantics.
4. Updated parity severity to focus on cross-pipeline mismatches only.

## Current Gate Status
- `tool_parity_checker.py --fail-on-high`: PASS
- Lane B parity guard can now be used as a blocking condition for promotions.

## Follow-up
1. Keep parity checker in lane B as required gate.
2. Re-run parity check after any change to token eligibility or hypothesis ranking logic.
