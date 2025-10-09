# Blue Mountains Shale Mining Communities Digital Collection Software

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Docs: CC-BY-4.0](https://img.shields.io/badge/Docs-CC--BY--4.0-green.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-compliant-brightgreen.svg)](https://www.rd-alliance.org/groups/fair-4-research-software-fair4rs-wg)

Research software for processing, analysing, and publishing historical newspaper sources and archaeological evidence from Blue Mountains shale mining communities (1880-1914).

**Project:** ARC Linkage Project LP190100900: *History, heritage and environmental change in a deindustrialised landscape*

**Institutions:** Macquarie University (lead), Deakin University, La Trobe University, MTS Heritage, Lantern Heritage, Concordia University (Canada)

**Keywords:** digital humanities · industrial archaeology · Zotero · Omeka Classic · FAIR data · controlled vocabularies · Getty vocabularies · Research Vocabularies Australia · Australian history · shale mining · Blue Mountains · heritage conservation

---

## Quick Links

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](docs/)
- [Contributing](CONTRIBUTING.md)
- [Citing This Software](#citing-this-software)
- [Licence](#licence)
- [Changelog](CHANGELOG.md)

---

## Project Overview

### Research Context

This software supports multidisciplinary research on shale mining settlements in the Jamison Valley, Blue Mountains, New South Wales. The project combines:

- **Historical archaeology:** Surface survey and material culture analysis
- **Archival research:** Newspaper articles, government records, maps
- **Oral history:** Community memories and family histories (via collaborators)
- **Digital methods:** FAIR data principles, controlled vocabularies, digital collections

**Research Questions:**

- How did working-class families live in isolated mining settlements?
- What were the social dynamics of gender, community, and transiency?
- How can digital methods enhance heritage conservation and public engagement?

**Study Site:** Ruined Castle shale mining village, Jamison Valley (operational 1880-1914)

**Primary Sources:** 417 newspaper articles and documents from Zotero group library (1,189 total items)

### Software Purpose

This software implements a FAIR-compliant workflow for managing historical sources:

```text
Zotero Library
    ↓
Tag Extraction & Analysis (folksonomy rationalisation)
    ↓
Controlled Vocabulary Development (hierarchical taxonomy)
    ↓
External Vocabulary Mapping (Getty AAT/TGN, Gazetteer of Australia)
    ↓
Research Vocabularies Australia Publishing (SKOS/RDF)
    ↓
Omeka Classic Publication (Dublin Core metadata)
    ↓
CurateScape Mobile Heritage Tours (public engagement)
```

**Intended Users:**

- Digital humanities researchers
- Archivists and data curators
- Heritage professionals
- Historical archaeologists
- Students learning research software development

---

## Features

### Current Features (v0.1.0)

- **Tag Management:**
  - Extract tags from Zotero group library via API
  - Analyse tag frequency and usage patterns
  - Identify similar tags using fuzzy string matching (Levenshtein Distance)
  - Detect hierarchical relationships (parent-child tags)
  - Generate tag co-occurrence networks

- **Data Quality:**
  - Identify potential duplicate items
  - Flag non-primary sources (attachments, notes, reference works)
  - Inspect items with multiple attachments
  - Generate quality assurance reports

- **Visualisation:**
  - Tag frequency bar charts
  - Tag co-occurrence network graphs
  - Similarity heatmaps

- **FAIR Compliance:**
  - Structured JSON data with provenance metadata
  - CSV exports for interoperability
  - Markdown reports for human readability
  - Software metadata (CITATION.cff, codemeta.json)

- **Geographic Integration:**
  - Composite Gazetteer of Australia (289,560 place names)
  - Coordinate lookup for Australian locations
  - GeoPackage spatial database queries

### Planned Features (Future Phases)

- **AI-Assisted Tagging:** LLM-based tag suggestions for untagged items
- **Vocabulary Publishing:** SKOS export to Research Vocabularies Australia
- **Getty Mapping:** Automated AAT/TGN URI resolution via SPARQL
- **Omeka Integration:** Batch publishing to Omeka Classic with Dublin Core metadata
- **CurateScape Tours:** Mobile heritage tour creation
- **Archaeological Data:** DNG photography workflow, site documentation

---

## Installation

### Prerequisites

- **Python 3.12 or higher**
- **Git** for version control
- **Zotero API credentials:**
  - Group library access to Blue Mountains collection (or your own library for testing)
  - API key with read/write permissions: https://www.zotero.org/settings/keys

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/shale-heritage/blue-mountains.git
cd blue-mountains
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

**Why a virtual environment?** Isolates project dependencies from system Python, preventing conflicts.

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Installed packages:**

- `pyzotero`: Zotero API client
- `pandas`: Data analysis and CSV export
- `fuzzywuzzy`, `python-Levenshtein`: Fuzzy string matching
- `networkx`: Network analysis
- `matplotlib`, `seaborn`: Visualisation
- `python-dotenv`: Environment variable management

See [requirements.txt](requirements.txt) for details and version constraints.

#### 4. Configure API Access

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your Zotero API key
# Use your preferred text editor
nano .env
```

**Required variables in `.env`:**

```bash
ZOTERO_GROUP_ID=2258643  # Or your own group/user library ID
ZOTERO_API_KEY=your_api_key_here
ZOTERO_LIBRARY_TYPE=group  # Or 'user' for personal library
```

**Security:** Never commit `.env` to version control! It's already in `.gitignore`.

#### 5. Verify Installation

```bash
# Test configuration loading
python scripts/config.py

# Expected output:
# ✓ Configuration loaded successfully
#   Zotero Group ID: 2258643
#   Library Type: group
```

### Troubleshooting

**Issue:** "Zotero credentials not found in .env file"

- **Solution:** Ensure `.env` file exists in project root and contains `ZOTERO_GROUP_ID` and `ZOTERO_API_KEY`

**Issue:** "ModuleNotFoundError: No module named 'pyzotero'"

- **Solution:** Activate virtual environment and reinstall: `pip install -r requirements.txt`

**Issue:** "Permission denied" when running scripts

- **Solution:** Make scripts executable: `chmod +x scripts/*.py` (Linux/macOS)

**Issue:** python-Levenshtein installation fails (Windows)

- **Solution:** Install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

---

## Usage

### Quick Start

Run scripts in order for the complete tag analysis workflow:

```bash
# 1. Extract tags from Zotero
python scripts/01_extract_tags.py

# 2. Analyse tag patterns
python scripts/02_analyze_tags.py

# 3. Inspect data quality
python scripts/03_inspect_multiple_attachments.py
```

### Script Details

#### Script 01: Extract Tags

**Purpose:** Fetch all items from Zotero and extract tag usage data

**Input:** Zotero group library (via API)

**Outputs:**

- `data/raw_tags.json`: Complete tag data with item associations
- `data/tag_frequency.csv`: Tag usage statistics (sorted by frequency)
- `reports/tag_summary.md`: Human-readable summary report

**Runtime:** ~2-5 minutes for 1,000+ items (depends on API response time)

**Example output:**

```text
======================================================================
BLUE MOUNTAINS PROJECT - TAG EXTRACTION
Script 01: Extract tags from Zotero group library
======================================================================

Connecting to Zotero...
✓ Connected

Fetching items from library (this may take a few minutes)...
  Retrieved batch 1: 100 items
  Retrieved batch 2: 100 items
  ...
  Retrieved batch 12: 89 items
✓ Retrieved 1189 total items

Extracting tags...
✓ Found 481 unique tags across 336 items

Statistics:
  Total items: 1189
  Items with tags: 336 (28.3%)
  Items without tags: 853 (71.7%)
  Unique tags: 481
  Most used tag: "Court" (45 items, 13.4%)

Saving data...
✓ Saved data/raw_tags.json
✓ Saved data/tag_frequency.csv
✓ Saved reports/tag_summary.md

✓ TAG EXTRACTION COMPLETE
```

#### Script 02: Analyse Tags

**Purpose:** Identify similar tags, hierarchical relationships, and co-occurrence patterns

**Input:** `data/raw_tags.json`

**Outputs:**

- `data/similar_tags.csv`: Tag pairs with similarity scores (>80%)
- `data/tag_network.json`: Co-occurrence network data
- `data/quality_*.csv`: Data quality issue lists
- `visualisations/tag_frequency_top20.png`: Bar chart
- `visualisations/tag_network.png`: Network graph
- `reports/tag_analysis.md`: Detailed analysis report

**Parameters:** Similarity threshold (default: 80%), minimum tag count (default: 1)

**Runtime:** ~1-3 minutes for 400+ tags

**Key findings (example):**

```text
Similar Tags Identified:
  "Court" vs "Court cases": 100% similarity, 45 items each
  "Katoomba" vs "Katoomba NSW": 85.7% similarity
  "Mining" vs "Mine": 83.3% similarity

Hierarchical Relationships:
  "Blue Mountains" contains "Katoomba" (18/45 items overlap)
  "Mining" contains "Mine" (all 8 "Mine" items also have "Mining")

Data Quality Issues:
  - 0 potential duplicates
  - 772 non-primary sources (attachments, notes)
  - 303 items with multiple attachments
```

#### Script 03: Inspect Multiple Attachments

**Purpose:** Review items with multiple attachments to ensure they don't combine distinct sources

**Input:** `data/quality_multiple_attachments.csv`

**Outputs:**

- `data/multiple_attachments_details.json`: Full item details
- `reports/multiple_attachments_inspection.md`: Categorised review report

**Categories:**

- **HIGH PRIORITY:** Multiple PDFs (may be distinct sources) - *Action: Split if needed*
- **PDF + Notes:** PDFs with text extraction notes - *Action: Usually OK*
- **Multiple Notes:** Multiple notes without PDFs - *Action: Review for consolidation*
- **Mixed Content:** Various attachment types - *Action: Case-by-case review*

**Findings (current dataset):**

- 0 high-priority items (no multiple PDFs needing splitting)
- 292 PDF+note pairs (legitimate structure for text extraction)
- 11 uncertain cases requiring manual inspection

---

## Documentation

### Project Documentation

- **[README.md](README.md)** (this file): Project overview and usage
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: Code standards, pull request process
- **[CHANGELOG.md](CHANGELOG.md)**: Version history and changes
- **[CITATION.cff](CITATION.cff)**: Software citation metadata
- **[codemeta.json](codemeta.json)**: Machine-readable software metadata

### Technical Documentation

- **[docs/data-formats.md](docs/data-formats.md)**: JSON schemas, CSV specifications
- **[docs/vocabularies.md](docs/vocabularies.md)**: Getty AAT/TGN, Gazetteer, RVA mappings
- **[docs/gazetteer-comparison.md](docs/gazetteer-comparison.md)**: Australian gazetteer evaluation

### Planning Documents

- **[planning/project-plan.md](planning/project-plan.md)**: 6-phase project roadmap
- **[planning/phase1-detailed.md](planning/phase1-detailed.md)**: Tag rationalisation phase
- **[planning/FAIR4RS-documentation-plan.md](planning/FAIR4RS-documentation-plan.md)**: FAIR compliance plan
- **[planning/FAIR4RS-phase-a-detailed.md](planning/FAIR4RS-phase-a-detailed.md)**: Implementation details

### Research Context

- **[project-info/summary.md](project-info/summary.md)**: ARC grant summary, investigators
- **[references/shale-heritage.bib](references/shale-heritage.bib)**: BibTeX citations

---

## FAIR4RS Compliance

This software implements FAIR4RS principles (Findable, Accessible, Interoperable, Reusable for Research Software):

### Findable (F)

- **Software Metadata:** CITATION.cff, codemeta.json
- **Persistent Identifier:** GitHub repository URL (Zenodo DOI planned)
- **Keywords:** 25+ searchable terms in metadata
- **Semantic Versioning:** v0.1.0 onwards
- **Detailed Documentation:** Comprehensive README, docs/ folder

### Accessible (A)

- **Open Source:** Apache 2.0 licence (code), CC-BY-4.0 (docs)
- **Public Repository:** https://github.com/shale-heritage/blue-mountains
- **Installation Guide:** Step-by-step instructions with troubleshooting
- **Dependencies:** All publicly available via PyPI
- **API Access:** Documented credentials process (.env.example)

### Interoperable (I)

- **Standard Formats:** JSON (RFC 8259), CSV (RFC 4180), Markdown (CommonMark)
- **Open APIs:** Zotero API (v3), Omeka Classic API
- **Vocabularies:** Getty AAT/TGN URIs, SKOS for RVA
- **Geospatial:** GeoPackage (OGC standard), GeoJSON (RFC 7946)
- **Metadata:** Dublin Core for Omeka, Schema.org for codemeta

### Reusable (R)

- **Clear Licence:** Apache 2.0 for code, CC-BY-4.0 for docs
- **Comprehensive Comments:** All functions documented with docstrings
- **Code Standards:** PEP 8 compliance, UK/Australian spelling
- **Contribution Guidelines:** CONTRIBUTING.md with PR process
- **Provenance:** All outputs include generation metadata

---

## Data Outputs

All data files are stored in the `data/` directory (gitignored for security):

### JSON Files

- **raw_tags.json:** Complete tag extraction from Zotero (metadata + tags dictionary)
- **tag_network.json:** Co-occurrence network data for visualisation
- **multiple_attachments_details.json:** Full item details for quality review

**Format:** UTF-8, 2-space indentation, ISO 8601 timestamps

**Schema:** See [docs/data-formats.md](docs/data-formats.md) for JSON schemas

### CSV Files

- **tag_frequency.csv:** Tag usage statistics (tag, count, percentage)
- **similar_tags.csv:** Tag similarity pairs (tag1, tag2, similarity, counts, suggested_merge)
- **quality_*.csv:** Data quality issue lists

**Format:** UTF-8, comma-delimited, header row, RFC 4180 compliant

### Reports (Markdown)

- **tag_summary.md:** Overview of tag extraction results
- **tag_analysis.md:** Detailed analysis of tag patterns
- **data_quality_issues.md:** Items flagged for review
- **multiple_attachments_inspection.md:** Attachment pattern review

**Format:** CommonMark, GitHub Flavoured Markdown, linted (MD022, MD031, MD032, MD040)

### Visualisations (PNG)

- **tag_frequency_top20.png:** Bar chart of most-used tags
- **tag_network.png:** Network graph of tag co-occurrences
- **tag_similarity_heatmap.png:** (future) Similarity matrix

**Format:** PNG, 300 DPI, 1920x1080px

---

## Citing This Software

If you use this software in your research, please cite it as:

### Recommended Citation

> Evans, T., Taksa, L., Ross, S., Lupack, S., Crook, P., Leslie, F., Parkes, R., & High, S. (2025).
> *Blue Mountains Shale Mining Communities Digital Collection Software* (Version 0.1.0) [Computer software].
> https://github.com/shale-heritage/blue-mountains

### BibTeX

```bibtex
@software{evans_blue_2025,
  title = {Blue Mountains Shale Mining Communities Digital Collection Software},
  author = {Evans, Tanya and Taksa, Lucy and Ross, Shawn and Lupack, Susan and
            Crook, Penelope and Leslie, Fiona and Parkes, Rebecca and High, Steven},
  year = {2025},
  version = {0.1.0},
  url = {https://github.com/shale-heritage/blue-mountains},
  note = {Software for managing historical sources from Blue Mountains shale mining settlements}
}
```

### Citation File Format

See [CITATION.cff](CITATION.cff) for machine-readable citation metadata (GitHub displays citation widget automatically).

---

## Licence

### Code Licence: Apache 2.0

All Python scripts, configuration files, and source code are licensed under the **Apache License 2.0**.

**You are free to:**

- Use the software for any purpose
- Modify the software to suit your needs
- Distribute the software
- Distribute your modified versions

**Under the following terms:**

- Include the original copyright notice and licence
- State significant changes made to the software
- Include the NOTICE file (if provided)
- Licence your modifications under Apache 2.0

See [LICENSE](LICENSE) for the full licence text.

### Documentation Licence: CC-BY-4.0

All documentation (Markdown files, planning documents, reports) is licensed under the **Creative Commons Attribution 4.0 International (CC-BY-4.0)**.

**You are free to:**

- Share: copy and redistribute the documentation
- Adapt: remix, transform, and build upon the documentation

**Under the following terms:**

- **Attribution:** You must give appropriate credit, provide a link to the licence, and indicate if changes were made

See [LICENSE-docs](LICENSE-docs) for details.

### Why Two Licences?

- **Apache 2.0 (code):** Provides patent protection and explicit terms for software distribution
- **CC-BY-4.0 (docs):** Standard for academic and educational content sharing

---

## Acknowledgements

This research is supported by the **Australian Research Council** Linkage Project scheme (grant **LP190100900**).

### Principal Investigators

- **A/Prof Tanya Evans** (Macquarie University) – Social history, public history
- **Prof Lucy Taksa** (Deakin University) – Labour history, industrial heritage
- **A/Prof Shawn Ross** (Macquarie University) – Digital archaeology, data management
- **Dr Susan Lupack** (Macquarie University) – Field archaeology, student training
- **Dr Penelope Crook** (Macquarie University) – Digital archaeology, artefact analysis

### Partner Investigators

- **Ms Fiona Leslie** (MTS Heritage) – Excavation direction, heritage management
- **Dr Rebecca Parkes** (Lantern Heritage Pty Ltd) – Archaeological surveys, heritage assessment
- **Prof Steven High** (Concordia University, Canada) – Deindustrialisation, oral history

### Partner Organisations

- Blue Mountains World Heritage Institute (BMWHI)
- National Parks and Wildlife Service (NPWS)
- Lantern Heritage Pty Ltd
- MTS Heritage
- Concordia University, Canada

### Related Publications

Parkes, R., Ross, S. A., Evans, T., Crook, P., Lupack, S., Karskens, G., Leslie, F., & Merson, J. (2018).
Ruined Castle Shale Mining Settlement, Katoomba NSW: Report on a Pilot Survey.
*Australasian Historical Archaeology*, 36, 86-92.
http://www.asha.org.au/journals/2010s/volume-36

---

## Contributing

We welcome contributions from the research community! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Code standards (PEP 8, UK/Australian spelling)
- Documentation requirements (comprehensive docstrings)
- Pull request process
- Issue reporting guidelines

**Key requirements:**

- All code uses UK/Australian English spelling
- Functions have detailed docstrings explaining purpose, parameters, and context
- Code passes linting (flake8 for Python, markdownlint for Markdown)
- Changes documented in CHANGELOG.md

---

## Contact

**Project Lead:** A/Prof Shawn Ross
**Email:** shawn@faims.edu.au
**Repository:** https://github.com/shale-heritage/blue-mountains

**For questions about:**

- **Software usage:** Open an issue on GitHub
- **Research collaboration:** Email shawn@faims.edu.au
- **Zotero library access:** Contact project team
- **Heritage site visits:** Contact NPWS or BMWHI

---

## Roadmap

### Phase 1: Tag Rationalisation & Vocabulary Publishing (Current)

- ✓ Tag extraction from Zotero
- ✓ Similarity analysis and consolidation recommendations
- ✓ Data quality assessment
- ⏳ Tag consolidation workflow (in progress)
- ⏳ Getty AAT/TGN mapping
- ⏳ Hierarchical vocabulary development
- ⏳ SKOS export to Research Vocabularies Australia

### Phase 2: AI-Assisted Tagging (Planned)

- LLM-based tag suggestions for 81 untagged primary sources
- Batch tagging workflow with human review
- Confidence scoring for automated suggestions

### Phase 3: Location Data Enhancement (Planned)

- Coordinate assignment using Composite Gazetteer of Australia
- Getty TGN URI mapping for international interoperability
- GeoJSON export for mapping applications

### Phase 4: Omeka Classic Publication (Planned)

- Dublin Core metadata mapping
- Batch item creation via Omeka API
- PDF attachment upload
- Collection organisation

### Phase 5: CurateScape Mobile Heritage Tours (Planned)

- Tour narrative development
- GPS-based location triggers
- Media integration (photos, audio, maps)

### Phase 6: Archaeological Integration (Future)

- DNG photography workflow
- Site documentation (surface survey data)
- 3D modelling integration
- Spatial analysis

---

## Project Status

**Current Version:** 0.1.0 (Initial Release)
**Development Status:** Active
**Last Updated:** 2025-10-09

---

*This software is part of the Blue Mountains Shale Mining Communities project, investigating industrial heritage and environmental change in the Jamison Valley, NSW, Australia.*
