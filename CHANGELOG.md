# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned

- Zenodo integration for DOI assignment on releases
- Additional publication references
- Dataset linking after data cleaning
- AI-assisted tagging for untagged primary sources
- Location data enhancement with coordinates
- Omeka Classic publication workflow
- CurateScape mobile heritage tour integration
- Tag consolidation and batch updates
- Getty vocabulary mapping (AAT, TGN)
- Research Vocabularies Australia publication
- DNG high-resolution photography workflow

## [0.1.0] - 2025-10-09

### Added

- Initial project structure and folder organisation
- FAIR4RS compliance documentation
  - CITATION.cff with complete investigator metadata and ORCIDs
  - codemeta.json with Schema.org software metadata
  - CHANGELOG.md for version tracking
  - CONTRIBUTING.md with code standards
  - LICENSE-docs (CC-BY-4.0) for documentation
- Core Python scripts for tag management
  - `scripts/config.py`: Configuration management with environment variables
  - `scripts/01_extract_tags.py`: Tag extraction from Zotero group library
  - `scripts/02_analyze_tags.py`: Tag similarity analysis and pattern detection
  - `scripts/03_inspect_multiple_attachments.py`: Data quality assessment
- Data analysis capabilities
  - Tag frequency analysis
  - Fuzzy string matching for tag similarity (80% threshold)
  - Hierarchical taxonomy detection
  - Tag co-occurrence network analysis
  - Data quality categorisation
- Documentation
  - Project planning documents in `planning/`
  - Gazetteer comparison and recommendation
  - Data formats and schemas documentation
  - Vocabulary standards and mappings (Getty AAT/TGN, Gazetteer of Australia, RVA)
  - API integration guides for Zotero and Omeka Classic
  - Comprehensive README with installation guide
- Integration with external resources
  - Zotero API for group library access (Group ID: 2258643)
  - Composite Gazetteer of Australia (GeoPackage format)
  - Gazetteer of Australia 2012 (reference)
  - Getty Vocabularies (AAT, TGN) URIs
  - Research Vocabularies Australia mapping
- Project context
  - ARC Linkage Project LP190100900 metadata
  - Investigator biographies with ORCIDs
  - Organisation RORs (Macquarie, Deakin, Concordia)
  - Partner organisation details
  - Publication references (Parkes et al. 2018)
- Quality assurance
  - UK/Australian spelling standards
  - Markdown linting compliance (MD022, MD031, MD032, MD040)
  - Python code standards and docstrings
  - Git commit message templates
- Development environment
  - Python 3.12 virtual environment setup
  - Requirements specification with dependencies
  - Environment variable management (.env, .env.example)
  - .gitignore for security and clean repository

### Changed

- Repository migrated to shale-heritage organisation
- Repository URL: `https://github.com/shale-heritage/blue-mountains`
- Penny Crook affiliation updated to Macquarie University (from La Trobe University)
- Lucy Taksa affiliation updated to Deakin University (from Macquarie University)

### Analysis Results

- **Total Zotero items:** 1,189
- **Unique tags:** 481
- **Items with tags:** 336 (28.3%)
- **Items without tags:** 853 (71.7%)
  - Actual primary sources without tags: 81 (after filtering attachments/notes)
- **Similar tag pairs identified:** 332 at 80% similarity threshold
- **Data quality issues:**
  - Potential duplicate items
  - Non-primary sources flagged
  - Multiple attachment patterns documented
  - 0 high-priority splitting candidates (all PDF+note pairs legitimate)

### Infrastructure

- Virtual environment: Python 3.12
- Dependencies: pyzotero, pandas, networkx, fuzzywuzzy, matplotlib, seaborn
- API integration: Zotero v3 API
- Data formats: JSON, CSV, Markdown, PNG
- Spatial data: GeoPackage (Gazetteer)
- Version control: Git with GitHub

## Guidelines for This Changelog

### Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

### Version Numbering (Semantic Versioning)

Given a version number MAJOR.MINOR.PATCH, increment:

1. **MAJOR** version when you make incompatible API changes
2. **MINOR** version when you add functionality in a backwards compatible manner
3. **PATCH** version when you make backwards compatible bug fixes

### Change Documentation

- Keep an Unreleased section at the top for tracking upcoming changes
- Document all notable changes (not every single commit)
- Group changes by type (Added, Changed, Fixed, etc.)
- Include dates in YYYY-MM-DD format
- Reference issue/PR numbers when applicable
- Write entries from user perspective, not developer jargon
- Link version tags to GitHub releases

### Example Entry

```markdown
## [1.2.0] - 2025-11-15

### Added

- Getty AAT vocabulary mapping with SKOS relationships (#42)
- Batch tag update script for Zotero items (#45)

### Changed

- Improved fuzzy matching algorithm for better accuracy (#43)
- Updated pandas dependency to 2.1.0 for performance gains

### Fixed

- Resolved Unicode encoding error in tag export (#44)
```

---

[Unreleased]: https://github.com/shale-heritage/blue-mountains/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/shale-heritage/blue-mountains/releases/tag/v0.1.0
