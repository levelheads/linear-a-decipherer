# Metadata Remediation Checklist

**Date**: 2026-02-15
**Primary ledger**: `analysis/active/2026-02-15_metadata_remediation_ledger.json`

Status legend: `todo`, `in_progress`, `done`, `blocked`

## Critical Site Assignment Tasks

| Inscription | Category | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `ANZb1` | missing_site | 6 | unassigned | todo | Verify site from primary publication/GORILA and backfill `site` field. |
| `DRAZg1` | missing_site | 6 | unassigned | todo | Verify site from primary publication/GORILA and backfill `site` field. |
| `INZb1` | missing_site | 6 | unassigned | todo | Verify site from primary publication/GORILA and backfill `site` field. |

## Critical Transliteration Recovery Tasks

| Inscription | Support | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `ZAZb39` | Stone vessel | 6 | unassigned | todo | Recover/confirm transliteration; add provenance note. |
| `ZOZa1` | Stone vessel | 6 | unassigned | todo | Recover/confirm transliteration; add provenance note. |
| `KNZg57b` | ivory object | 5 | unassigned | todo | Recover/confirm transliteration; add provenance note. |
| `HTWc3023` | Roundel | 3 | unassigned | todo | Recover/confirm transliteration; add provenance note. |
| `KE6` | Tablet | 3 | unassigned | todo | Recover/confirm transliteration; add provenance note. |

## High-Priority Context Backfill Tasks

| Inscription | Markers | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `IOZa2` | A-TA-I-*301-WA-JA, I-PI-NA-MA, JA-SA-SA-RA-ME, SI-RU-TE, U-NA-KA-NA-SI | 14 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa15` | I-PI-NA-MA, SI-RU-TE | 14 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `VRYZa1` | I-PI-NA-MA, SI-RU-TE | 14 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa14` | SI-RU-TE | 14 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `TLZa1` | A-TA-I-*301-WA-JA, I-PI-NA-MA, JA-SA-SA-RA-ME, SI-RU-TE, U-NA-KA-NA | 12 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `KOZa1` | A-TA-I-*301-WA-JA, I-PI-NA-MA, SI-RU-TE, U-NA-KA-NA-SI | 12 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `APZa2` | I-PI-NA-MA | 11 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa9` | JA-SA-SA-RA-ME, U-NA-KA-NA-SI | 9 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `PKZa27` | JA-SA-SA-RA-ME, U-NA-KA-NA-SI | 9 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa3` | A-TA-I-*301-WA-JA | 9 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `PKZa12` | A-TA-I-*301-WA-JA | 9 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `PSZa2` | JA-SA-SA-RA-ME | 9 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `APZa<3>` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa11` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa13` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |

## Execution Notes

1. Complete site assignments first (small set, high integrity impact).
2. Complete stone/ivory empty transliterations second.
3. Context backfill for ritual-critical entries third.
4. Re-run `bash tools/run_corpus_refresh_cycle.sh --skip-parse --date 2026-02-15` after updates.
