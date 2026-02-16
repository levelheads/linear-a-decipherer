# Metadata Remediation Checklist

**Date**: 2026-02-15
**Last Updated**: 2026-02-16 (Post-Sprint Phase 4)
**Primary ledger**: `analysis/active/2026-02-15_metadata_remediation_ledger.json`

Status legend: `todo`, `in_progress`, `done`, `blocked`

## Critical Site Assignment Tasks

| Inscription | Category | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `ANZb1` | missing_site | 6 | sprint | done | Site set to "Anemospilia" (near Archanes, Juktas region). |
| `DRAZg1` | missing_site | 6 | sprint | done | Site set to "Dreros" (east Crete; note: primarily Iron Age site, attribution uncertain). |
| `INZb1` | missing_site | 6 | sprint | done | Site set to "Inatos" (cave sanctuary, southern Crete; per Perna publication). |

## Critical Transliteration Recovery Tasks

| Inscription | Support | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `ZAZb39` | Stone vessel | 6 | sprint | blocked | Online sources insufficient; requires GORILA vol. IV consultation. Provenance note added. |
| `ZOZa1` | Stone vessel | 6 | sprint | blocked | Recent Zominthos excavation; publication access needed. Provenance note added. |
| `KNZg57b` | ivory object | 5 | sprint | done | Transliteration recovered from Unicode mapping: I KU WI NI KA DU [frag] GRA GRA OLIV. |
| `HTWc3023` | Roundel | 3 | sprint | blocked | Requires Hallager roundel corpus consultation. Provenance note added. |
| `KE6` | Tablet | 3 | sprint | blocked | Requires GORILA vol. V (extra-Cretan) consultation. Provenance note added. |

## High-Priority Context Backfill Tasks

| Inscription | Markers | Priority | Owner | Status | Next Action |
|---|---|---:|---|---|---|
| `IOZa2` | A-TA-I-*301-WA-JA, I-PI-NA-MA, JA-SA-SA-RA-ME, SI-RU-TE, U-NA-KA-NA-SI | 14 | sprint | done | Context=MMIII-LMI, confidence=HIGH. Iouktas peak sanctuary, Neopalatial. |
| `IOZa15` | I-PI-NA-MA, SI-RU-TE | 14 | sprint | done | Context=MMIII-LMI, confidence=HIGH. Iouktas peak sanctuary. |
| `VRYZa1` | I-PI-NA-MA, SI-RU-TE | 14 | sprint | done | Context=MMIII-LMI, confidence=HIGH. Vrysinas peak sanctuary. |
| `IOZa14` | SI-RU-TE | 14 | sprint | done | Context=MMIII-LMI, confidence=HIGH. Iouktas peak sanctuary. |
| `TLZa1` | A-TA-I-*301-WA-JA, I-PI-NA-MA, JA-SA-SA-RA-ME, SI-RU-TE, U-NA-KA-NA | 12 | sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Troullos peak sanctuary. |
| `KOZa1` | A-TA-I-*301-WA-JA, I-PI-NA-MA, SI-RU-TE, U-NA-KA-NA-SI | 12 | sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Kophinas peak sanctuary. |
| `APZa2` | I-PI-NA-MA | 11 | sprint | done | Already had context=MMIII-LMI. Verified. |
| `IOZa9` | JA-SA-SA-RA-ME, U-NA-KA-NA-SI | 9 | post-sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Iouktas peak sanctuary, Neopalatial stone vessel. |
| `PKZa27` | JA-SA-SA-RA-ME, U-NA-KA-NA-SI | 9 | post-sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Palaikastro sanctuary, Neopalatial stone vessel. |
| `IOZa3` | A-TA-I-*301-WA-JA | 9 | post-sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Iouktas peak sanctuary, Neopalatial stone vessel. |
| `PKZa12` | A-TA-I-*301-WA-JA | 9 | post-sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Palaikastro sanctuary, Neopalatial stone vessel. |
| `PSZa2` | JA-SA-SA-RA-ME | 9 | post-sprint | done | Context=MMIII-LMI, confidence=MEDIUM. Psykhro (Diktaean Cave), Neopalatial stone vessel. |
| `APZa<3>` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa11` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |
| `IOZa13` | none | 7 | unassigned | todo | Backfill `context` period with citation evidence; flag confidence. |

## Progress Summary (2026-02-16)

- Site assignments: **3/3 done**
- Transliteration recovery: **1/5 done, 4 blocked** (require physical GORILA volumes)
- Context backfill (priority 12+): **6/6 done**
- Context backfill (priority 9-11): **6/6 done** (post-sprint batch)
- Context backfill (priority <9): **0/3 remaining** (APZa<3>, IOZa11, IOZa13)
- **Total: 16/23 done, 4 blocked, 3 remaining**

## Execution Notes

1. Complete site assignments first (small set, high integrity impact).
2. Complete stone/ivory empty transliterations second.
3. Context backfill for ritual-critical entries third.
4. Re-run `bash tools/run_corpus_refresh_cycle.sh --skip-parse --date 2026-02-15` after updates.
