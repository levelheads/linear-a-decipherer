# Attribution and Data Sources

This document provides comprehensive attribution for all external data sources, code, and scholarly works integrated into or referenced by this project.

---

## External Repositories

### lineara.xyz Corpus Explorer

**Location**: `external/lineara/` (git submodule)

**Repository**: https://github.com/mwenge/lineara.xyz

**Author**: mwenge (GitHub)

**Description**: A web-based tool for exploring the Linear A corpus, providing structured access to inscription data, images, and scholarly commentary.

**License Status**: No explicit license specified in the repository as of 2026-01-09. This project links to the repository via git submodule (equivalent to citation) rather than copying or redistributing its contents.

**How We Use It**: Reference data for corpus analysis; not redistributed.

#### Upstream Data Sources (as documented by lineara.xyz)

The lineara.xyz project aggregates data from three primary scholarly sources:

1. **GORILA (Recueil des Inscriptions en Linéaire A)**
   - **Citation**: Godart, L. & Olivier, J.-P. (1976-1985). *Recueil des inscriptions en linéaire A*. Études Crétoises, vols. 21.1-5. Paris: Geuthner.
   - **Digitization Source**: Centre d'Études de l'Antiquité (cefael.efa.gr)
   - **Content**: Tablet images and transcriptions
   - **Copyright**: Original publication copyright held by publishers; digitization by EFA

2. **George Douros Spreadsheet**
   - **Contributor**: George Douros
   - **Content**: Tabulated document data with word breaks, ideograms, and numerals
   - **Format**: Spreadsheet parsed into JSON by lineara.xyz

3. **John Younger Commentaries**
   - **Contributor**: John G. Younger (University of Kansas)
   - **Source**: Originally hosted at ku.edu
   - **Content**: Scholarly commentaries on individual Linear A inscriptions
   - **Format**: HTML extracted and integrated into lineara.xyz

#### Attribution Chain

When citing data accessed through this integration:

```
Data accessed via lineara.xyz (mwenge, https://github.com/mwenge/lineara.xyz),
which aggregates: GORILA (Godart & Olivier, 1976-1985), George Douros spreadsheet,
and John Younger commentaries.
```

---

## Academic Sources

### Primary Corpus References

| Source | Citation | Use in Project |
|--------|----------|----------------|
| GORILA | Godart & Olivier (1976-1985) | Authoritative corpus; AB numbering |
| SigLA | Salgarella (ongoing) | Sign verification; online queries |
| PAITO | Del Freo & Ferro (ongoing) | Cross-reference; scholarly curation |

### Methodological Sources

| Source | Citation | Use in Project |
|--------|----------|----------------|
| Kober Method | Kober, A. (1945-1950) | Pattern analysis methodology |
| Ventris Grid | Ventris, M. (1952) | Decipherment approach |
| Documents in Mycenaean Greek | Ventris & Chadwick (1956) | Linear B reference |

### Linguistic Hypothesis Sources

| Hypothesis | Key Proponents | Key Works |
|------------|---------------|-----------|
| Luwian/Anatolian | Palmer, Finkelberg | Finkelberg (1998) |
| Semitic | Gordon, Best | Gordon (1966) |
| Pre-Greek Substrate | Beekes, Furnée | Beekes (2014) |
| Proto-Greek | Georgiev, Mosenkis | Various |

---

## License Compatibility

### This Project

This project is licensed under **CC BY-NC-SA 4.0** (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International).

### External Dependencies

| Dependency | License | Compatibility |
|------------|---------|---------------|
| lineara.xyz | Not specified | Linked via submodule; not redistributed |
| GORILA | Academic publication | Fair use for research |
| SigLA | Academic database | Reference only |

### Fair Use Statement

This project uses external data sources for **non-commercial academic research** into undeciphered ancient scripts. Data is accessed via linking (git submodules) or citation rather than redistribution. All uses fall within fair use provisions for scholarly research and commentary.

---

## How to Cite This Project

If you use this project or its analyses in academic work:

```bibtex
@software{linear_a_decipherer,
  title = {Linear A Decipherment Methodology System},
  author = {{Contributors}},
  year = {2026},
  url = {https://github.com/levelheads/linear-a-decipherer},
  note = {Incorporates data from lineara.xyz, GORILA, and other sources as documented in ATTRIBUTION.md}
}
```

---

## Acknowledgments

This project builds upon decades of scholarly work on Linear A and Aegean scripts. We acknowledge:

- **Louis Godart and Jean-Pierre Olivier** for GORILA, the foundational corpus
- **Alice Kober** (1906-1950) for the methodological framework
- **Michael Ventris** (1922-1956) for demonstrating rigorous decipherment
- **John Chadwick** (1920-1998) for verification methodology
- **George Douros** for corpus digitization work
- **John Younger** for comprehensive inscription commentaries
- **mwenge** for the lineara.xyz explorer and data aggregation
- **Ester Salgarella** for SigLA and ongoing Linear A scholarship
- **The PAITO Project team** for corpus curation

---

## Reporting Attribution Issues

If you believe any attribution in this project is incomplete or incorrect, please open an issue at the project repository or contact the maintainers directly.
