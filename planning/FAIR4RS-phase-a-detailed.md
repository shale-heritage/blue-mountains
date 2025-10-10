# Phase A Detailed: FAIR4RS Compliance Implementation

**Status:** Ready for review and execution
**Estimated Time:** 2-3 hours
**Dependencies:** Project information from `project-info/`

---

## Overview

Phase A establishes the foundational FAIR4RS compliance for the software project, making it Findable, Accessible, Interoperable, and Reusable. This phase creates metadata files, enhances discoverability, clarifies licensing, and documents standards.

---

## A1. Findable (F) - Detailed Tasks

### Task A1.1: Create CITATION.cff

**Purpose:** Enable automatic software citation in GitHub and research platforms

**File Location:** `/home/shawn/Code/blue-mountains/CITATION.cff`

**Content Structure:**
```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "Blue Mountains Shale Mining Communities Digital Collection Software"
version: 0.1.0
date-released: "2025-10-09"

# Principal Investigators
authors:
  - family-names: "Evans"
    given-names: "Tanya"
    affiliation: "Macquarie University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

  - family-names: "Taksa"
    given-names: "Lucy"
    affiliation: "Deakin University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

  - family-names: "Ross"
    given-names: "Shawn"
    affiliation: "Macquarie University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

  - family-names: "Cassidy"
    given-names: "Steve"
    affiliation: "Macquarie University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

  - family-names: "Lupack"
    given-names: "Susan"
    affiliation: "Macquarie University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

  - family-names: "Crook"
    given-names: "Penelope"
    affiliation: "La Trobe University"
    orcid: "https://orcid.org/[TO_BE_PROVIDED]"

# Keywords for discoverability
keywords:
  - "digital humanities"
  - "archaeology"
  - "industrial archaeology"
  - "historical archaeology"
  - "shale mining"
  - "Blue Mountains"
  - "Jamison Valley"
  - "Zotero"
  - "Omeka Classic"
  - "CurateScape"
  - "FAIR data"
  - "controlled vocabularies"
  - "Getty vocabularies"
  - "Research Vocabularies Australia"
  - "deindustrialisation"
  - "industrial heritage"
  - "Australian history"
  - "heritage conservation"

license: "GPL-3.0-or-later"
repository-code: "https://github.com/[ORG]/blue-mountains"
type: software

abstract: >
  Research software for processing, analysing, and publishing historical
  newspaper sources and archaeological evidence from Blue Mountains shale
  mining communities (1880-1914). Part of ARC Linkage Project LP190100900:
  "History, heritage and environmental change in a deindustrialised landscape".

  The software implements FAIR principles for research data, integrating
  Zotero bibliography management for controlled vocabulary development,
  mapping to Getty vocabularies (AAT, TGN) and Research Vocabularies Australia,
  and publishing to Omeka Classic digital collections with CurateScape mobile
  heritage tours.

  Key features: tag extraction and rationalisation, similarity analysis,
  hierarchical taxonomy development, data quality assessment, FAIR-compliant
  metadata generation, and API integration with Zotero and Omeka Classic.

references:
  - type: grant
    title: "History, heritage and environmental change in a deindustrialised landscape"
    institution:
      name: "Australian Research Council"
    number: "LP190100900"
    start-date: "2020-07-01"
    end-date: "2024-12-31"
    authors:
      - family-names: "Evans"
        given-names: "Tanya"
      - family-names: "Taksa"
        given-names: "Lucy"
      - family-names: "Ross"
        given-names: "Shawn"
      - family-names: "Lupack"
        given-names: "Susan"
      - family-names: "Crook"
        given-names: "Penelope"
```

**Questions Needed:**
- ORCID IDs for all 6 CIs (or leave placeholders?)
- GitHub organisation name
- Confirm GPL-3.0-or-later is correct licence

**Validation:**
- Use https://citation-file-format.github.io/cff-initializer-javascript/ to validate
- GitHub will automatically display citation widget

---

### Task A1.2: Create codemeta.json

**Purpose:** Provide machine-readable software metadata in Schema.org format

**File Location:** `/home/shawn/Code/blue-mountains/codemeta.json`

**Key Sections:**

1. **Basic Metadata**
```json
{
  "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
  "@type": "SoftwareSourceCode",
  "name": "Blue Mountains Shale Mining Communities Digital Collection Software",
  "description": "Research software for processing historical sources from Blue Mountains shale mining settlements...",
  "version": "0.1.0",
  "dateCreated": "2025-10-09",
  "dateModified": "2025-10-09"
}
```

2. **Technical Details**
```json
{
  "programmingLanguage": {
    "@type": "ComputerLanguage",
    "name": "Python",
    "version": "3.12",
    "url": "https://www.python.org/"
  },
  "runtimePlatform": "Python 3.12+",
  "operatingSystem": ["Linux", "macOS", "Windows"]
}
```

3. **Research Context**
```json
{
  "applicationCategory": "Research Software",
  "applicationSubCategory": [
    "Digital Humanities",
    "Historical Archaeology",
    "Heritage Management",
    "Data Management"
  ],
  "keywords": [/* same as CITATION.cff */]
}
```

4. **Funding**
```json
{
  "funder": {
    "@type": "Organization",
    "name": "Australian Research Council",
    "url": "https://www.arc.gov.au/",
    "identifier": "https://doi.org/10.13039/501100000923"
  },
  "funding": "LP190100900"
}
```

5. **Software Requirements**
```json
{
  "softwareRequirements": [
    {
      "@type": "SoftwareApplication",
      "name": "pyzotero",
      "version": ">=1.6.17"
    },
    {
      "@type": "SoftwareApplication",
      "name": "pandas",
      "version": ">=2.0"
    },
    {
      "@type": "SoftwareApplication",
      "name": "networkx",
      "version": ">=3.0"
    },
    {
      "@type": "SoftwareApplication",
      "name": "fuzzywuzzy",
      "version": ">=0.18"
    }
  ]
}
```

**Validation:**
- Use https://codemeta.github.io/codemeta-generator/ to validate
- Ensure valid JSON structure

---

### Task A1.3: Create CHANGELOG.md

**Purpose:** Track software versions and changes

**File Location:** `/home/shawn/Code/blue-mountains/CHANGELOG.md`

**Format:** Keep a Changelog standard

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Tag extraction script (01_extract_tags.py)
- Tag analysis script (02_analyse_tags.py)
- Multiple attachments inspection script (03_inspect_multiple_attachments.py)
- FAIR4RS compliance documentation

## [0.1.0] - 2025-10-09

### Added
- Initial release
- Zotero API integration for tag management
- Data quality analysis tools
- Project planning and documentation
- FAIR data principles implementation

[Unreleased]: https://github.com/[ORG]/blue-mountains/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/[ORG]/blue-mountains/releases/tag/v0.1.0
```

**Maintenance:**
- Update with each significant change
- Tag releases in Git when versioning

---

### Task A1.4: Enhance README.md with Findability Elements

**Current State:** Minimal README ("Work on the Blue Mountains Shale Mining Communities project")

**Enhanced Version:** Add to top of README

```markdown
# Blue Mountains Shale Mining Communities Digital Collection Software

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/[TO_BE_ASSIGNED].svg)](https://doi.org/[TO_BE_ASSIGNED])

Research software for processing, analysing, and publishing historical newspaper sources and archaeological evidence from Blue Mountains shale mining communities (1880-1914).

**Project:** ARC Linkage Project LP190100900: *History, heritage and environmental change in a deindustrialised landscape*

**Institutions:** Macquarie University (lead), Deakin University, La Trobe University

**Keywords:** digital humanities · industrial archaeology · Zotero · Omeka Classic · FAIR data · controlled vocabularies · Australian history

---

## Quick Links

- [Installation](#installation)
- [Usage](#usage)
- [Documentation](docs/)
- [Contributing](CONTRIBUTING.md)
- [Citing](#citing-this-software)
- [License](#licence)

---
```

**Findability Features Added:**
- Badges for quick status checks
- Clear project title and description
- Keywords for search engines
- Links to key resources
- Professional formatting

---

## A2. Accessible (A) - Detailed Tasks

### Task A2.1: Create .env.example

**Purpose:** Document required environment variables without exposing secrets

**File Location:** `/home/shawn/Code/blue-mountains/.env.example`

```bash
# Zotero API Configuration
# Generate your API key at: https://www.zotero.org/settings/keys
# Permissions needed: Read/Write access to the group library

ZOTERO_GROUP_ID=2258643
ZOTERO_API_KEY=your_api_key_here
ZOTERO_LIBRARY_TYPE=group

# Omeka Classic Configuration (for future use)
# OMEKA_API_URL=https://your-omeka-site.org/api
# OMEKA_API_KEY=your_omeka_api_key_here
```

**Update .gitignore** to ensure `.env` is never committed:

```gitignore
# Environment variables (contains API keys)
.env
.env.local
.env.*.local
```

**Documentation in README:**

```markdown
## Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API credentials:
   - **Zotero API Key:** Generate at https://www.zotero.org/settings/keys
     - Select "Allow library access"
     - Select your group library
     - Copy the generated key

3. **Security:** Never commit `.env` to version control!
```

---

### Task A2.2: Installation Guide in README

**Add to README.md:**

```markdown
## Installation

### Prerequisites

- Python 3.12 or higher
- Git
- Zotero group library access
- Zotero API key (read/write permissions)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/[ORG]/blue-mountains.git
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

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure API Access

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your Zotero API key
# Use your preferred text editor
nano .env
```

#### 5. Verify Installation

```bash
# Test configuration
python scripts/config.py

# Expected output:
# ✓ Configuration loaded successfully
#   Zotero Group ID: 2258643
#   Library Type: group
```

### Troubleshooting

**Issue:** "Zotero credentials not found in .env file"
- **Solution:** Ensure `.env` file exists and contains `ZOTERO_GROUP_ID` and `ZOTERO_API_KEY`

**Issue:** "ModuleNotFoundError: No module named 'pyzotero'"
- **Solution:** Activate virtual environment and reinstall: `pip install -r requirements.txt`

**Issue:** "Permission denied" when running scripts
- **Solution:** Make scripts executable: `chmod +x scripts/*.py`
```

---

### Task A2.3: Enhanced requirements.txt with Comments

**Current:** Simple list of packages

**Enhanced:** Annotated with purpose and version constraints

```text
# Core Dependencies
# =================

# Zotero API client for bibliography management
# https://github.com/urschrei/pyzotero
pyzotero>=1.6.17

# HTTP requests for API interactions
# https://requests.readthedocs.io/
requests>=2.32.0

# Data analysis and manipulation
# https://pandas.pydata.org/
pandas>=2.3.0

# Environment variable management (secure API key storage)
# https://github.com/theskumar/python-dotenv
python-dotenv>=1.1.0


# Analysis Dependencies
# ====================

# Data visualisation
# https://matplotlib.org/
matplotlib>=3.10.0
seaborn>=0.13.0

# Fuzzy string matching for tag similarity analysis
# https://github.com/seatgeek/fuzzywuzzy
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.27.0

# Network analysis for tag co-occurrence
# https://networkx.org/
networkx>=3.5


# Development Dependencies (optional)
# ===================================

# Code linting and style checking
# flake8>=7.0.0
# pylint>=3.0.0

# Markdown linting
# markdownlint-cli>=0.37.0
```

---

## A3. Interoperable (I) - Detailed Tasks

### Task A3.1: Create docs/data-formats.md

**Purpose:** Document all data formats for interoperability

**File Location:** `/home/shawn/Code/blue-mountains/docs/data-formats.md`

**Content Structure:**

```markdown
# Data Formats

All data produced by this software uses standard, open formats to ensure interoperability and long-term accessibility.

## File Formats Overview

| Format | Purpose | Standard | Tools |
|--------|---------|----------|-------|
| JSON | Structured data storage | RFC 8259 | Python json module, jq |
| CSV | Tabular data | RFC 4180 | pandas, Excel, R |
| Markdown | Documentation, reports | CommonMark | Any text editor |
| PNG | Visualisations | ISO/IEC 15948 | Image viewers |

## JSON Schemas

### raw_tags.json

**Purpose:** Complete export of tags from Zotero group library

**Schema:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "tags"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "generated_at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp of generation"
        },
        "zotero_group_id": {
          "type": "string",
          "description": "Zotero group library ID"
        },
        "statistics": {
          "type": "object",
          "properties": {
            "total_items": {"type": "integer"},
            "items_with_tags": {"type": "integer"},
            "items_without_tags": {"type": "integer"},
            "unique_tags": {"type": "integer"}
          }
        }
      }
    },
    "tags": {
      "type": "object",
      "patternProperties": {
        ".*": {
          "type": "object",
          "properties": {
            "count": {"type": "integer"},
            "items": {
              "type": "array",
              "items": {"type": "string"}
            },
            "item_titles": {
              "type": "array",
              "items": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

**Example:**
```json
{
  "metadata": {
    "generated_at": "2025-10-09T10:30:00+11:00",
    "zotero_group_id": "2258643",
    "statistics": {
      "total_items": 1189,
      "items_with_tags": 336,
      "unique_tags": 481
    }
  },
  "tags": {
    "Mining": {
      "count": 32,
      "items": ["ABC123XYZ", "DEF456UVW"],
      "item_titles": ["Article Title 1", "Article Title 2"]
    }
  }
}
```

[Continue with other formats...]
```

---

### Task A3.2: Create docs/vocabularies.md

**Purpose:** Document vocabulary standards used

**Content:**

```markdown
# Vocabulary Standards and Mappings

## Overview

This project uses controlled vocabularies following FAIR principles for research data. Tags are mapped to international standards to enable interoperability and discovery.

## Getty Vocabularies

### Art & Architecture Thesaurus (AAT)

**Purpose:** Concepts, activities, materials, styles, genres

**Example Mappings:**
- Local: "Mining" → AAT: http://vocab.getty.edu/aat/300053857
- Local: "Shale" → AAT: http://vocab.getty.edu/aat/300011791

**Access:** http://www.getty.edu/research/tools/vocabularies/aat/

### Thesaurus of Geographic Names (TGN)

**Purpose:** Places, administrative entities

**Example Mappings:**
- Local: "Katoomba" → TGN: http://vocab.getty.edu/tgn/7001924
- Local: "Jamison Valley" → TGN: [to be mapped]
- Local: "Blue Mountains" → TGN: http://vocab.getty.edu/tgn/7001926

**Access:** http://www.getty.edu/research/tools/vocabularies/tgn/

## Research Vocabularies Australia (RVA)

**Purpose:** Australian research vocabularies discovery and reuse

**Project Vocabulary:** [To be published to RVA]

**SKOS Format:** Project vocabulary will be published in Simple Knowledge Organisation System (SKOS) format

## Dublin Core Metadata

**Purpose:** Item-level metadata for Omeka publications

**Elements Used:**
- dcterms:title
- dcterms:creator
- dcterms:date
- dcterms:description
- dcterms:subject (tags)
- dcterms:spatial (geographic locations)
- dcterms:type
- dcterms:rights

**Namespace:** http://purl.org/dc/terms/

## Mapping Relationships (SKOS)

**Relationship Types:**
- `skos:exactMatch` - Identical concepts
- `skos:closeMatch` - Very similar concepts
- `skos:broadMatch` - Broader concept
- `skos:narrowMatch` - Narrower concept
- `skos:relatedMatch` - Related but not hierarchical
```

---

## A4. Reusable (R) - Detailed Tasks

### Task A4.1: Add Licence Section to README

```markdown
## Licence

This software is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

You are free to:
- Use this software for any purpose
- Change the software to suit your needs
- Share the software with others
- Share your changes with others

Under the following terms:
- You must include the original copyright and licence notice
- If you modify and distribute the software, you must release it under the same licence
- You must state significant changes made to the software
- You must make your source code available

See [LICENSE](LICENSE) for full licence text.

### Citation

If you use this software in your research, please cite it using the information in [CITATION.cff](CITATION.cff) or:

> Evans, T., Taksa, L., Ross, S., Cassidy, S., Lupack, S., & Crook, P. (2025).
> Blue Mountains Shale Mining Communities Digital Collection Software (Version 0.1.0)
> [Computer software]. https://github.com/[ORG]/blue-mountains

### Acknowledgements

This research is supported by the Australian Research Council Linkage Project scheme (grant LP190100900).

**Partner Organisations:**
- Blue Mountains World Heritage Institute
- National Parks and Wildlife Service (NPWS)
- Lantern Heritage Pty Ltd
- MTS Heritage
- Concordia University (Canada)
```

---

### Task A4.2: Create CONTRIBUTING.md

*(Full file content as specified in main plan)*

---

## Questions Before Proceeding

1. **ORCID IDs:** Do you have ORCID IDs for the 6 Chief Investigators? If not, should we leave placeholders?

2. **GitHub Repository:** What is the GitHub organisation or username? (for repository URLs in citations)

3. **Zenodo DOI:** Would you like to set up Zenodo integration for automatic DOI assignment on releases?

4. **Contact Email:** What email address should be listed for project contact in CONTRIBUTING.md?

5. **Publications:** Are there any publications from LP190100900 that should be listed as references?

6. **Related Datasets:** Any published datasets to cross-reference?

7. **Licence Confirmation:** GPL-3.0-or-later is appropriate for this project?

---

## Execution Checklist

- [ ] Create CITATION.cff with complete metadata
- [ ] Create codemeta.json with software metadata
- [ ] Create CHANGELOG.md with versioning
- [ ] Create .env.example with documented variables
- [ ] Verify .env is in .gitignore
- [ ] Create comprehensive installation guide in README
- [ ] Add troubleshooting section to README
- [ ] Annotate requirements.txt with comments
- [ ] Create docs/data-formats.md with JSON schemas
- [ ] Create docs/vocabularies.md with mappings
- [ ] Add Licence section to README
- [ ] Create CONTRIBUTING.md
- [ ] Create docs/ directory structure
- [ ] Test all documentation for clarity
- [ ] Verify all files use UK/Australian spelling

---

*Ready for review and execution*
*Close manual review 2025-10-09 by Shawn Ross*