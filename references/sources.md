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

- **Full Citation**: Kanta, A., Nakassis, D., Palaima, T.G., & Perna, M. (2025). "An archaeological and epigraphical overview of some inscriptions found in the Cult Center of the city of Knossos (Anetaki plot)." *Ariadne*, Supplement 5, pp. 27-43.
- **Type**: Article (Open Access PDF)
- **License**: CC BY-NC-SA 4.0
- **Local Path**: `references/pdfs/Kanta_et_al_2025_Knossos_Scepter.pdf` (acquired 2026-01-09)
- **Article URL**: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841
- **PDF URL**: https://ejournals.lib.uoc.gr/Ariadne/article/view/1841/1751
- **DOI**: 10.26248/ariadne.vi.1841
- **Accessed**: 2026-01-09
- **Relevance**: Longest Linear A inscription (119 signs); dual register analysis; 2024 discovery

**Sign Count** (confirmed):
- 84 signs completely or partially preserved
- 35 signs in small traces or probably present
- **Total: 119 signs** (longest Linear A inscription ever found)

**Key Excerpts**:
> "The ivory ring is inscribed on all four of its faces with a text in Linear A that represents the longest Linear A inscription ever discovered." (p. 35)

> "The ring inscription shows a refined, calligraphic hand with stylistic affinity to Cretan Hieroglyphic." (paraphrased from p. 36)

**Official Designations**:
- **KN Zg 57** - Ivory ring (ceremonial/religious inscription)
- **KN Zg 58** - Ivory handle (administrative inscription)

**Notes**:
- **OPEN ACCESS** - PDF freely downloadable for non-commercial use
- This paper is an "overview" - full transliteration forthcoming in "Anetaki II"
- Two inscriptions by different scribes (ring + handle)
- Ring: 84 preserved + 35 partial signs, ceremonial/religious style, no numerals
- Handle: administrative style with numerals and 6 fraction signs
- Found in "Fetish Shrine" at Anetaki plot, Knossos (Neopalatial, 1700-1450 BCE)
- First confirmed Linear A at Knossos cult center
- See `analyses/KNOSSOS_SCEPTER_DATA_2026-01-09.md` for detailed extraction

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

- **Full Citation**: Greco, A., Flouda, G., & Notti, E. (ongoing). *PA-I-TO: Linear A and Linear B Epigraphic Project*. Sapienza Università di Roma / Heraklion Archaeological Museum / IULM University.
- **Type**: Database (URL)
- **URL**: https://www.paitoproject.it/linear-a/
- **Project Overview**: https://www.paitoproject.it/en/pa-i-to-project-2/
- **Accessed**: 2026-01-09
- **Contact**: Prof. Alessandro Greco (a.greco@uniroma1.it)
- **License**: Scientific non-profit use; permission required for reproduction
- **Relevance**: 1,534 Linear A documents; 7,574 signs; RTI/3D imaging methodology

**Corpus Statistics**:
- 1,534 Linear A documents (as of 2023)
- 7,574 total signs
- ~90% administrative documents, ~10% non-administrative
- Sites: Hagia Triada, Phaistos, Knossos, plus Aegean islands and Asia Minor

**Methodology** (valuable for our approach):
- **RTI (Reflectance Transformation Imaging)**: 48-60 photos at varying light angles
- **3D Laser Scanning**: 0.01mm resolution for curvature analysis
- Captures sign details invisible in standard examination
- Emphasizes "materiality" - physical tablet formation and scribe hand

**Key Insight - Phaistos Chronology**:
- Room 25 tablets (PH 1-30) are the **oldest Linear A corpus** (MM IIB, 1800-1680 BCE)
- Predates most Hagia Triada tablets by 200+ years
- Early tablets may show archaic features vs. later standardization

**Notes**:
- Multi-institutional collaboration (Sapienza, IULM, Heraklion Museum)
- 2D+ and 3D-models available for scholarly use with permission
- Participated in 2024 Knossos ivory scepter documentation
- Focus on paleographic documentation over linguistic interpretation

---

### Younger - Linear A Texts & Inscriptions

- **Full Citation**: Younger, J.G. (ongoing, last updated 2024-04-08). *Linear A Texts & Inscriptions in phonetic transcription*.
- **Type**: Online compilation (Academia.edu)
- **URL**: https://www.academia.edu/117949876/Linear_A_Texts_and_Inscriptions_in_phonetic_transcription
- **Accessed**: 2026-01-09
- **Relevance**: Comprehensive phonetic transcriptions of all GORILA tablets; ~1,500 documents, ~7,500 signs

**Notes**:
- Primary reference for tablet transcriptions
- Uses Linear B phonetic values with systematic conventions
- Includes administrative vocabulary analysis and libation formula documentation
- Does NOT yet include Knossos scepter (last updated before 2025 publication)
- Covers sites: HT, KH, ZA, PH, AR, KN, MA, TY, PE, and others

---

## Sources To Acquire

Priority sources not yet obtained:

| Source | Priority | Type | Status |
|--------|----------|------|--------|
| Anetaki II (full scepter transliteration) | **Critical** | Publication | Forthcoming |
| GORILA volumes | High | Book | Institutional access needed |
| Finkelberg 1998 (Luwian hypothesis) | Medium | Article | To acquire |
| Gordon 1966 (Semitic hypothesis) | Medium | Book | To acquire |
| Beekes 2014 (Pre-Greek) | Medium | Book | To acquire |

**Completed**: Kanta et al. 2025 acquired 2026-01-09 (see above)

---

## URL Verification Log

| URL | Last Verified | Status |
|-----|---------------|--------|
| https://sigla.phis.me | 2026-01-09 | Active |
| https://lineara.xyz | 2026-01-09 | Active |
| https://www.paitoproject.it/linear-a/ | 2026-01-09 | Active |
| https://ejournals.lib.uoc.gr/Ariadne/article/view/1841 | 2026-01-09 | Active |
