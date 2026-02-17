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
- See `analysis/KNOSSOS_SCEPTER_DATA_2026-01-09.md` for detailed extraction

---

### GORILA - Recueil des inscriptions en linéaire A

- **Full Citation**: Godart, L. & Olivier, J.-P. (1976-1985). *Recueil des inscriptions en linéaire A* (GORILA). Études Crétoises, vols. 21.1-5. Paris: Geuthner.
- **Type**: Book (5 volumes) - **NOW DIGITIZED ONLINE**
- **Local Path**: Available in `external/lineara/papers/` (PDF copies)
- **Relevance**: Authoritative corpus; AB numbering system; sign classification standard
- **Inscriptions**: 1,427 documents; 7,362-7,396 signs

**Online Access** (École française d'Athènes - cefael.efa.gr):

| Volume | Contents | URL |
|--------|----------|-----|
| **Vol. 1** | Tablets published before 1970 | http://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=1&sp=5 |
| **Vol. 2** | Nodules, roundels before 1970 | http://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=2&sp=5 |
| **Vol. 3** | 1975-1976 publications | http://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=3&sp=5 |
| **Vol. 4** | Vases, jewelry, misc. | http://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=4&sp=5 |
| **Vol. 5** | Indices, concordances, sign tables | http://cefael.efa.gr/detail.php?site_id=1&actionID=page&serie_id=EtCret&volume_number=21&issue_number=5&sp=5 |

**Notes**:
- Definitive reference for Linear A inscriptions
- Establishes AB### sign numbering convention
- **OPEN ACCESS** via École française d'Athènes digital library
- Photos, drawings, and transcriptions for each document
- Volume 5 contains the authoritative sign classification

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

- **Full Citation**: Younger, J.G. (ongoing, last updated 2024-04-23). *Linear A Texts & Inscriptions in phonetic transcription*.
- **Type**: Online compilation (Academia.edu)
- **Primary URL**: https://www.academia.edu/117949876/Linear_A_Texts_and_Inscriptions_in_phonetic_transcription
- **Introduction**: https://www.academia.edu/117949722/Younger_JG_Linear_A_folder_introduction
- **Lexicon**: http://www.people.ku.edu/~jyounger/LinearA/lexicon.html (may be deprecated)
- **Accessed**: 2026-01-31
- **Relevance**: Comprehensive phonetic transcriptions of all GORILA tablets; ~1,500 documents, ~7,500 signs

**URL Migration Notice (February 2024)**:
> The original Kansas University server (people.ku.edu/~jyounger/LinearA/) was **shut down in February 2024**. Younger migrated materials to Academia.edu in April 2024. Some old links in lineara.xyz commentary may be broken.

**Available Files on Academia.edu**:
- Introduction and overview of Linear A
- Linear AB syllabary
- Haghia Triada texts (transliteration)
- Texts from other sites
- Lexicon (planned)
- Chronological updates list (planned)

**Notes**:
- Primary reference for tablet transcriptions
- Uses Linear B phonetic values with systematic conventions
- Includes administrative vocabulary analysis and libation formula documentation
- Does NOT yet include Knossos scepter (last updated before 2025 publication)
- Covers sites: HT, KH, ZA, PH, AR, KN, MA, TY, PE, and others
- Younger has worked on Linear A for 20+ years; contextual/archaeological approach

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

---

## Additional Online Resources

### Mnamon Portal (Meta-Resource)

- **Full Citation**: Del Freo, M. (ed.). *Mnamon: Ancient Writing Systems in the Mediterranean*. Scuola Normale Superiore di Pisa.
- **Type**: Portal / Meta-resource
- **URL**: https://mnamon.sns.it/index.php?page=Scrittura&id=19&lang=en
- **Resources Page**: https://mnamon.sns.it/index.php?page=Risorse&id=19&lang=en
- **DOI**: 10.25429/sns.it/lettere/mnamon000
- **ISBN**: 978-88-7642-719-0
- **Last Updated**: April 2022 (Linear A section by Maurizio Del Freo)
- **Accessed**: 2026-01-31
- **Relevance**: Curated index of 37+ Linear A resources; research centers; bibliographies

**Sections Available**:
- Linear A overview and script description
- Examples of writing (sample inscriptions)
- List of symbols (sign inventory)
- Online resources (comprehensive link collection)

**Notes**:
- Best single starting point for discovering Linear A resources
- Critically reviewed by specialists
- Covers research centers, databases, bibliographies, fonts, archives

---

### DĀMOS - Database of Mycenaean at Oslo

- **Full Citation**: Piquero Rodríguez, J. et al. *DĀMOS: Database of Mycenaean at Oslo*. University of Oslo.
- **Type**: Database (URL)
- **URL**: https://damos.hf.uio.no/
- **Texts**: https://damos.hf.uio.no/about/texts/
- **Accessed**: 2026-01-31
- **Relevance**: Complete Linear B corpus for cognate verification; 6,000+ tablets

**Statistics**:
- Knossos: 3,369 tablets by ~100 scribes
- Pylos: 1,107 tablets by 32 scribes
- Other sites: Mycenae, Thebes, Tiryns, Midea, Dimini

**Features**:
- Full corpus in transcription
- Word search tool
- Updated with new joins and readings
- Scribal hand identification

**Notes**:
- Essential for Linear B cognate verification
- Cross-reference Linear A readings against Linear B vocabulary
- Maintained with ongoing updates from new archaeological finds

---

### INSCRIBE Project (ERC)

- **Full Citation**: Ferrara, S. (PI). *INSCRIBE: Invention of Scripts and their Beginnings*. ERC Consolidator Grant, University of Bologna.
- **Type**: Research Project + Database
- **URL**: https://site.unibo.it/inscribe/en/about-1
- **SigLA Integration**: https://site.unibo.it/inscribe/en/linear-a-sigla
- **Accessed**: 2026-01-31
- **Relevance**: Comparative study of writing invention; computational approaches

**Key Outputs**:
- SigLA paleographic database (see separate entry)
- LAIF (Linear A Inscription Finder) - in development
- Fraction sign analysis (computational)
- Sign evolution studies

**Notes**:
- Ongoing ERC-funded project
- Focus on script invention and early development
- May produce additional digital resources

---

### Linear A Digital Corpus (TEI-EpiDoc)

- **Full Citation**: Petrolito, T., Petrolito, R., Cacciafoco, F.P., & Winterstein, G. (2015). "Minoan Linguistic Resources: The Linear A Digital Corpus." *Proceedings of LaTeCH 2015*.
- **Type**: Digital Corpus (TEI-XML)
- **URL**: https://aclanthology.org/W15-3715/
- **PDF**: https://aclanthology.org/W15-3715.pdf
- **Accessed**: 2026-01-31
- **Relevance**: Structured XML corpus; Unicode standardization; NLP-ready format

**Technical Details**:
- TEI-EpiDoc XML encoding
- Custom Linear A Unicode font
- Standardized character mapping
- Designed for computational analysis

**Notes**:
- Useful for NLP/computational approaches
- Addresses Unicode visualization issues
- May be outdated compared to SigLA/lineara.xyz

---

### CREWS Project (Cambridge)

- **Full Citation**: Steele, P.M. (PI). *CREWS: Contexts of and Relations between Early Writing Systems*. ERC, University of Cambridge.
- **Type**: Research Project
- **URL**: https://crewsproject.wordpress.com/
- **Accessed**: 2026-01-31
- **Relevance**: Writing systems methodology; Bronze Age Aegean scripts context

**Key Publications**:
- Blog posts on Linear A methodology
- Comparative script analysis
- Replica tablet creation guides

**Notes**:
- Valuable for methodological context
- Cross-script comparisons (Cypriot, Anatolian, etc.)

---

### PASP - Program in Aegean Scripts and Prehistory

- **Full Citation**: Palaima, T.G. (Director). *Program in Aegean Scripts and Prehistory*. University of Texas at Austin.
- **Type**: Research Center + Archive
- **URL**: https://sites.utexas.edu/scripts/
- **Accessed**: 2026-01-31
- **Relevance**: Primary US center for Aegean script studies; archives

**Archives Held**:
- Elizabeth Wayland Barber Collection
- William Brice Collection (includes Ventris correspondence)
- Pylos tablet documentation project

**Notes**:
- Major scholarly archive for Linear A/B research history
- Pylos tablets digitization with RTI/3D scanning
- Annual research programs on decipherment

---

### CaLiBRA - Cambridge Linear B Research Archive

- **Full Citation**: University of Cambridge. *CaLiBRA: Cambridge Archive of Linear B Research*.
- **Type**: Database / Image Archive
- **URL**: https://calibra.classics.cam.ac.uk/
- **Accessed**: 2026-01-31
- **Relevance**: Searchable photographs of Linear B tablets; cognate verification

**Notes**:
- High-quality tablet photographs
- Useful for comparing Linear A/B sign forms
- Focus on Pylos archive

---

### Computational Approaches Review (2024)

- **Full Citation**: Ferrara, S. et al. (2024). "A Systematic Review of Computational Approaches to Deciphering Bronze Age Aegean and Cypriot Scripts." *Computational Linguistics*, 50(2), 725-773.
- **Type**: Review Article
- **URL**: https://direct.mit.edu/coli/article/50/2/725/119990/
- **PDF**: https://aclanthology.org/2024.cl-2.7.pdf
- **Accessed**: 2026-01-31
- **Relevance**: State-of-the-art computational methods; machine learning approaches

**Coverage**:
- Traditional and deep learning decipherment approaches
- Archanes script, Cretan Hieroglyphic, Phaistos Disc
- Linear A computational analysis methods
- Cypro-Minoan and Cypriot syllabary

**Notes**:
- Essential reading for computational methodology
- Identifies gaps and opportunities in automated analysis
- Published 2024 - most current review available

---

### Salgarella Publications (2024)

- **Full Citation**: Salgarella, E. & Judson, A. (2024). "Signs of the time? Testing the chronological significance of Linear A and B palaeography." In *Ko-ro-na-we-sa: Proceedings of the 15th International Colloquium on Mycenaean Studies*. Crete University Press.
- **Type**: Conference Proceedings
- **URL**: https://www.academia.edu/127103477/
- **Accessed**: 2026-01-31
- **Relevance**: Chronological analysis via paleography; tablet dating methodology

**Also see**:
- Meissner, T. & Salgarella, E. (2024). "The Relationship Between Cretan Hieroglyphic and the Other Cretan Scripts." In Civitillo et al. (eds.), *Cretan Hieroglyphic*. Cambridge University Press, pp. 134-164.
- Salgarella, Bellinato & Ferrara (2025, forthcoming). "On Aegean Spices: Decipherment prospects on Linear A and B spice-related signs."

---

## Fonts and Technical Resources

### Noto Sans Linear A

- **Type**: Unicode Font
- **URL**: https://fonts.google.com/noto/specimen/Noto+Sans+Linear+A
- **License**: SIL Open Font License
- **Relevance**: Complete Linear A Unicode character set

**Notes**:
- Google's comprehensive ancient script font
- Recommended for document preparation
- Full Unicode Block U+10600-U+1077F

---

### Aegean Font (George Douros)

- **Type**: Unicode Font
- **URL**: https://localfonts.eu/freefonts/greek-free-fonts/unicode-fonts-for-ancient-scripts/aegean/
- **Relevance**: Cretan Hieroglyphic, Linear A, Linear B, Cypriot

**Notes**:
- Covers multiple Aegean scripts in one font
- Used by lineara.xyz project
- Includes sign variants

---

### Linear A LaTeX Package

- **Type**: LaTeX Package + Fonts
- **URL**: https://ctan.org/pkg/lineara
- **Author**: Apostolos Syropoulos
- **Relevance**: Academic document preparation with Linear A signs

---

## Research Centers and Archaeological Schools

| Institution | URL | Focus |
|-------------|-----|-------|
| **SAIA** (Italian School at Athens) | http://www.scuoladiatene.it/ | Cretan excavations |
| **INSTAP** | http://www.instapstudycenter.org/ | Aegean prehistory (US) |
| **EfA** (French School at Athens) | http://www.efa.gr/ | Malia excavations |
| **BSA** (British School at Athens) | http://www.bsa.ac.uk/ | Knossos, Palekastro |
| **ASCSA** (American School) | http://www.ascsa.edu.gr/ | Research library |
| **Heraklion Museum** | https://heraklionmuseum.gr/language/en/home/ | 75% of Linear A inscriptions |

---

## Bibliographies

| Resource | URL | Coverage |
|----------|-----|----------|
| **Younger Bibliography** | http://www.people.ku.edu/~jyounger/LinearA/biblio.html | 1980-present |
| **NESTOR** | https://classics.uc.edu/nestor | Aegean prehistory to 2006 |
| **SMID** | https://repositories.lib.utexas.edu/handle/2152/16096 | Linear A/B (1979-1999) |

---

## URL Verification Log

| URL | Last Verified | Status |
|-----|---------------|--------|
| https://sigla.phis.me | 2026-01-31 | Active |
| https://lineara.xyz | 2026-01-31 | Active |
| https://www.paitoproject.it/linear-a/ | 2026-01-31 | Active |
| https://ejournals.lib.uoc.gr/Ariadne/article/view/1841 | 2026-01-31 | Active |
| https://mnamon.sns.it/index.php?page=Risorse&id=19&lang=en | 2026-01-31 | Active |
| https://damos.hf.uio.no/ | 2026-01-31 | Active |
| http://cefael.efa.gr/ (GORILA) | 2026-01-31 | Active |
| https://site.unibo.it/inscribe/en/ | 2026-01-31 | Active |
| https://sites.utexas.edu/scripts/ | 2026-01-31 | Active |
| https://calibra.classics.cam.ac.uk/ | 2026-01-31 | Active |

---

## Integration Status

| Resource | Programmatic Integration | Notes |
|----------|--------------------------|-------|
| **lineara.xyz** | FULL | Primary corpus via parse_lineara_corpus.py |
| **ORACC/Akkadian** | FULL | Via oracc_connector.py |
| **SigLA** | Reference only | No API; would require scraping |
| **GORILA** | Via lineara.xyz | Direct PDFs now linked |
| **DĀMOS** | Reference only | Potential for Linear B cross-ref |
| **PAITO** | Reference only | Chronology metadata source |
| **John Younger** | Via lineara.xyz | Original KU URL deprecated Feb 2024 |
