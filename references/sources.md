# Reference Sources Index

This file indexes all reference materials used in the Linear A decipherment project. Large files (PDFs, documents) are stored locally and excluded from version control. This index provides citations, URLs, and key notes for reproducibility.

---

## How to Use This Index

1. **Adding a new source**: Copy the template below and fill in all fields
2. **Local files**: Store in `references/pdfs/` or `references/local/` (gitignored)
3. **URLs**: Prefer DOI links or stable institutional URLs
4. **Key excerpts**: Include relevant quotes that inform analysis (with page numbers)

---

## Source Template

```markdown
### [Short Title]

- **Full Citation**: Author(s). (Year). Title. Journal/Publisher. DOI/URL
- **Type**: PDF | URL | Book | Article | Database
- **Local Path**: `references/pdfs/filename.pdf` (if applicable)
- **URL**: https://...
- **DOI**: 10.xxxx/xxxxx
- **Accessed**: YYYY-MM-DD
- **Relevance**: [Which aspect of Linear A research this informs]

**Key Excerpts**:
> "Quoted text with page number" (p. XX)

**Notes**:
- Bullet points summarizing key contributions
```

---

## Indexed Sources

---

### Salgarella - Drawing Lines

- **Full Citation**: Salgarella, E. (2020). "Drawing Lines: A Study of the Relationship between Cretan Hieroglyphic and Linear A Scripts." *Kadmos*, 59(1-2), 1-44.
- **Type**: Article (PDF/DOCX)
- **Local Path**: `reference texts/Drawing Lines_E Salgarella_Kadmos.docx`
- **DOI**: 10.1515/kadmos-2020-0001
- **Accessed**: 2026-01-09
- **Relevance**: Script evolution; relationship between Cretan Hieroglyphic and Linear A; sign correspondences

**Key Excerpts**:
> [Add relevant quotes after reading]

**Notes**:
- Examines continuity and divergence between Cretan Hieroglyphic and Linear A
- Important for understanding sign origins and paleographic evolution

---

### Kanta et al. - Knossos Ivory Scepter

- **Full Citation**: Kanta, A., et al. (2025). "The Knossos Ivory Scepter: A New Linear A Inscription." *Ariadne*, Supplement 5.
- **Type**: Article (URL)
- **Local Path**: (not yet acquired)
- **URL**: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841
- **Accessed**: 2026-01-09
- **Relevance**: Longest Linear A inscription (119 signs); dual register analysis; 2024 discovery

**Key Excerpts**:
> [Awaiting full transliteration]

**Notes**:
- Critical source for complete scepter transliteration
- Two inscriptions by different scribes (ring + handle)
- Ring: ceremonial/religious style
- Handle: administrative style with numerals

---

### GORILA - Recueil des inscriptions en linéaire A

- **Full Citation**: Godart, L. & Olivier, J.-P. (1976-1985). *Recueil des inscriptions en linéaire A* (GORILA). Études Crétoises, vols. 21.1-5. Paris: Geuthner.
- **Type**: Book (5 volumes)
- **Local Path**: (not held locally)
- **URL**: (institutional access required)
- **Relevance**: Authoritative corpus; AB numbering system; sign classification standard

**Notes**:
- Definitive reference for Linear A inscriptions
- Establishes AB### sign numbering convention
- Five volumes covering all known inscriptions through 1985

---

### SigLA Database

- **Full Citation**: Salgarella, E. (ongoing). *SigLA: The Signs of Linear A*. Online database.
- **Type**: Database (URL)
- **URL**: https://sigla.phis.me
- **Accessed**: 2026-01-09
- **Relevance**: Sign list; inscription search; 772 documents indexed

**Notes**:
- Primary online resource for sign verification
- Searchable by sign, inscription, or site
- Includes paleographic variants

---

### lineara.xyz (Git Submodule)

- **Full Citation**: mwenge. (ongoing). *lineara.xyz: A tool for exploring the Linear A corpus*. GitHub repository.
- **Type**: Database + Code Repository (Git Submodule)
- **Local Path**: `external/lineara/` (git submodule)
- **Repository**: https://github.com/mwenge/lineara.xyz
- **Website**: https://lineara.xyz
- **Commit**: eb9afc70104aed41dc740ebd05bf7e677fb48ffe
- **Accessed**: 2026-01-09
- **License**: Not specified (see ATTRIBUTION.md for details)
- **Relevance**: Comprehensive inscription database; 1,800+ inscriptions; structured data

**Key Data Files**:
- `LinearAInscriptions.js` - Full corpus as JSON objects
- `words_in_linearb.js` - Linear B cognates (29 words, 141 roots, 600+ variants)
- `ideograms.js` - Logogram catalog
- `annotations.js` - Scholarly annotations
- `commentary/` - HTML commentary files (from John Younger)

**Upstream Sources** (as documented by repository):
- GORILA (Godart & Olivier, 1976-1985) - tablet images and transcriptions
- George Douros - spreadsheet with word breaks, ideograms, numerals
- John Younger - inscription commentaries (originally from ku.edu)

**Notes**:
- Most comprehensive online corpus with structured data access
- Integrated as git submodule for data reference without redistribution
- See ATTRIBUTION.md for full attribution chain and license considerations
- To initialize: `git submodule update --init`

---

### PAITO Project

- **Full Citation**: Del Freo, M. & Ferro, L. (ongoing). *PAITO: Corpus of Mycenaean and Linear A Inscriptions*. CNR-ISPC.
- **Type**: Database (URL)
- **URL**: https://www.paitoproject.it/linear-a/
- **Accessed**: 2026-01-09
- **Relevance**: 1,534 Linear A documents; scholarly curation

**Notes**:
- Italian CNR project
- Cross-references with Linear B corpus
- Academic quality control

---

## Sources To Acquire

Priority sources not yet obtained:

| Source | Priority | Type | Status |
|--------|----------|------|--------|
| Kanta et al. 2025 (full text) | Critical | PDF | Awaiting |
| GORILA volumes | High | Book | Institutional access needed |
| Younger's Linear A Texts | Medium | URL | To index |
| Finkelberg 1998 (Luwian hypothesis) | Medium | Article | To acquire |
| Gordon 1966 (Semitic hypothesis) | Medium | Book | To acquire |
| Beekes 2014 (Pre-Greek) | Medium | Book | To acquire |

---

## URL Verification Log

| URL | Last Verified | Status |
|-----|---------------|--------|
| https://sigla.phis.me | 2026-01-09 | Active |
| https://lineara.xyz | 2026-01-09 | Active |
| https://www.paitoproject.it/linear-a/ | 2026-01-09 | Active |
| https://ejournals.lib.uoc.gr/Ariadne/article/view/1841 | 2026-01-09 | Active |
