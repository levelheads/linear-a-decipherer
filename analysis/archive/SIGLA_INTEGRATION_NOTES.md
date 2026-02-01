# SigLA Integration Notes

**Date**: 2026-01-31
**Status**: Assessment Complete

---

## Current Data Sources

### Already Integrated: lineara.xyz
- **Location**: `external/lineara/`
- **Format**: JavaScript (LinearAInscriptions.js, annotations.js)
- **Coverage**: 1,721 inscriptions
- **Content**: Full transliterations, parsed inscriptions, site data, scribe data
- **Already parsed into**: `data/corpus.json`

### SigLA Database (sigla.phis.me)
- **Created by**: Ester Salgarella & Simon Castellan (2020-)
- **License**: CC BY-NC-SA 4.0
- **Focus**: Paleographical analysis of signs
- **Unique value**: 3,000+ individual sign attestations with drawings

## Assessment

### What We Have (lineara.xyz)
- Complete transliterations for all 1,721 inscriptions
- Word-level parsing with numerals separated
- Site, scribe, period (context), and support metadata
- Already integrated into our corpus.json

### What SigLA Adds
- **Sign-level paleographical data** (not currently needed for lexical analysis)
- **Sign drawings and variants** (useful for disputed readings)
- **Sign attestation frequencies** (partially duplicated in our tools)

### Recommendation

**SigLA integration is LOW PRIORITY** for OPERATION MINOS II because:
1. Our current corpus already has full transliterations
2. SigLA's value is paleographical (sign shapes), not lexical
3. We already have word/sign frequency data from our tools

**Future integration value**:
- Useful when resolving disputed sign readings
- Valuable for sign variant analysis (e.g., *301 variants)
- May help with chronological paleography studies

## Action

- [x] Verify lineara.xyz data is current
- [ ] Monitor SigLA for updates that add new inscriptions
- [ ] Consider paleographical integration for Phase 10+

---

*Assessment by OPERATION MINOS II infrastructure review*
