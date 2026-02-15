# Metadata Remediation Ledger

**Date**: 2026-02-15
**Artifact**: `analysis/active/2026-02-15_metadata_remediation_ledger.json`

## Purpose

Track and prioritize data-quality gaps that directly slow decipherment testing.

## Snapshot

- Missing context records: `331`
- Missing site records: `3`
- Empty transliteration records: `9`
- Current validation warnings: `8`

## High-Priority Context Backfill Targets

Top ritual-relevant records (score-driven):
1. `IOZa2`
2. `IOZa15`
3. `VRYZa1`
4. `IOZa14`
5. `TLZa1`
6. `KOZa1`
7. `APZa2`
8. `IOZa9`
9. `PKZa27`

These are prioritized because they intersect ritual markers and active slot/terminal hypotheses.

## Missing Site Records

Records requiring source-level site verification:
1. `ANZb1`
2. `DRAZg1`
3. `INZb1`

## Empty Transliteration Records (Highest Priority)

1. `ZAZb39` (Stone vessel)
2. `ZOZa1` (Stone vessel)
3. `KNZg57b` (ivory object)

## Remediation Protocol

1. Resolve all missing-site records first (low count, high integrity impact).
2. Recover transliterations for high-value empty records (stone/ivory/metal supports).
3. Backfill context periods for ritual-critical inscriptions (priority score `>=8`).
4. Bulk backfill remaining context entries with citation provenance.

## Validator Policy (Until Fully Remediated)

Chronology-conditioned analyses should either:
1. Exclude empty-context records, or
2. Flag outputs as context-incomplete.
