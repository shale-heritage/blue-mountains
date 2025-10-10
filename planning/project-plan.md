# Zotero → Omeka Classic Publication Workflow

**Project:** Historical Newspaper Sources + Archaeological Evidence Digital Collection
**Date Created:** 2025-10-08
**Last Updated:** 2025-10-10
**Tools:** Zotero API, Omeka Classic API, Claude/Local LLM, CurateScape

---

## Current Status (2025-10-10)

**Phase 1:** 🔄 In Progress - Tag rationalisation infrastructure complete, analysis ongoing

**Recent Achievements:**
- ✅ Complete FAIR4RS documentation implementation (Phases A-E, Oct 9-10, 2025)
- ✅ Core analysis scripts developed and documented (01_extract_tags.py, 02_analyze_tags.py, 03_inspect_multiple_attachments.py)
- ✅ Comprehensive code documentation (~4,100 lines)
- ✅ Project metadata and compliance files (CITATION.cff, codemeta.json, CONTRIBUTING.md)
- ✅ Technical documentation (API integration, data formats, vocabularies, gazetteers)
- ✅ Folder-specific READMEs for all major directories
- ✅ Quality assurance complete (Python linting, markdown linting, UK/Australian spelling)
- ✅ Configuration updated for Omeka Classic integration (shaleheritage.au)

**Documentation Statistics:**
- 29 markdown files
- ~16,200 lines of documentation
- 16:1 documentation-to-code ratio
- 0 linting errors across all files
- Publication-ready research software

**Next Steps:**
- Complete Phase 1.1: Historian consultation on tag folksonomy
- Begin Phase 1.2: Tag schema rationalisation
- Develop Phase 1.3: Getty and RVA vocabulary mapping

---

## Phase 1: Tag Rationalization & Vocabulary Publishing 🔄 IN PROGRESS

### 1.1 Folksonomy Analysis ✅ INFRASTRUCTURE COMPLETE

**Completed:**
- ✅ Extract all existing tags from Zotero group library (01_extract_tags.py)
- ✅ Analyse tag usage patterns, frequencies, overlaps (02_analyze_tags.py)
  - Fuzzy matching for similar tags (80% similarity threshold)
  - Hierarchical relationship detection (substring analysis)
  - Co-occurrence network analysis
  - Data quality categorisation
- ✅ Generate comprehensive analysis reports:
  - tag_summary.md - Overview statistics
  - tag_analysis.md - Detailed pattern analysis
  - similar_tags.csv - Consolidation suggestions
  - tag_hierarchy.csv - Parent/child relationships
  - tag_cooccurrence.csv - Network relationships

**Remaining:**
- 🔄 Interview/consult with historians who created tags
- 🔄 Document current folksonomy logic and categories

**Scripts:** 01_extract_tags.py (1,420 lines), 02_analyze_tags.py (2,164 lines)

### 1.2 Tag Schema Rationalization 📋 PLANNED

**Tasks:**
- Consolidate similar/duplicate tags (using similar_tags.csv recommendations)
- Standardise terminology and structure
- Create hierarchical organisation if needed (using tag_hierarchy.csv)
- Document definitions and scope notes

**Dependencies:** Requires historian consultation (Phase 1.1)

### 1.3 Vocabulary Mapping & Publication 📋 PLANNED

**Tasks:**
- Map rationalised tags → Getty vocabularies (AAT/TGN)
- Prepare metadata for Research Vocabularies Australia (RVA)
- Publish controlled vocabulary to RVA
- Document mappings for interoperability

**Documentation Available:**
- docs/vocabularies.md - Getty AAT, TGN, and RVA standards
- docs/gazetteer-comparison.md - Geographic vocabulary options

**Dependencies:** Requires Phase 1.2 completion

### 1.4 Batch Update Zotero 📋 PLANNED

**Tasks:**
- Apply rationalised tags to existing items via API
- Preserve original tags as backup (separate collection/export)
- Validate updates

**Documentation Available:** docs/api-integration.md - Zotero API patterns

**Dependencies:** Requires Phase 1.3 completion

## Phase 2: AI-Assisted Tagging (Terminal-Based)

### 2.1 Content Extraction
- Pull untagged primary sources from Zotero API
- Extract text from PDFs/notes field
- Prepare batches for analysis

### 2.2 AI Tagging Options
**Option A: Claude Code in terminal (this session)**
- Process PDFs/text directly here
- Apply controlled vocabulary interactively
- Update Zotero via API in batches

**Option B: Local LLM (120B)**
- Script to feed content to local model
- Prompt engineering with controlled vocabulary
- Batch processing for efficiency

### 2.3 Validation Workflow
- Intensive manual review of first 5-10 PDFs
- Refine prompts/model based on results
- Spot-check 5-10% of remaining items
- Statistical validation across corpus

## Phase 3: Location Data Enhancement

### 3.1 Location Extraction
- Parse articles for place names
- Match to existing location metadata
- Geocode locations (use Getty TGN where mapped)
- Handle imprecise locations ("near X", "region of Y")

### 3.2 CurateScape Location Setup
- Add lat/long to Omeka items
- Group items by geographic proximity
- Link newspaper sources to archaeological sites
- Create location clusters for tours

## Phase 4: Omeka Classic Publication (FAIR-Compliant)

### 4.1 Metadata Transformation
- Map Zotero fields → Dublin Core
- Include:
  - Controlled vocabulary tags
  - Getty mappings
  - RVA vocabulary URIs
  - Location coordinates
  - Trove source URLs (persistent IDs)

### 4.2 License Management
- Apply CC-BY by default
- Inherit/respect Trove licenses per item
- Document license in metadata
- Include rights statements in exhibits

### 4.3 Automated Publishing Pipeline
- `zotero_to_omeka.py` script:
  - Pull tagged items from Zotero group
  - Transform metadata + PDFs
  - POST to Omeka Classic API
  - Assign to Collections (by theme/tag)
  - Set geographic data for CurateScape

### 4.4 Collections & Exhibits
- Create Collections based on tag groupings
- Build Exhibits combining sources + context
- Prepare for CurateScape tour integration

## Phase 5: CurateScape Tours

### 5.1 Tour Design
- Group items by location + theme
- Combine newspaper articles + archaeological evidence
- Create narrative structures
- Test mobile functionality

### 5.2 Integration
- Configure CurateScape with published items
- Set up location-based triggers
- Build interpretive content
- QA on iOS/Android apps

## Phase 6: Archaeological Integration (Future)

- Match DSLR images to records
- Apply compatible tag schema
- Import to Omeka via API
- Link to newspaper sources via tags + locations
- Expand tours with material evidence

---

## Key Scripts: Development Status

### Core Infrastructure ✅ COMPLETE

1. **`config.py`** ✅ - Configuration management (296 lines)
   - Environment variable handling
   - Zotero and Omeka API configuration
   - Path management and validation
   - Security-focused design

2. **`01_extract_tags.py`** ✅ - Tag extraction from Zotero (1,420 lines)
   - Complete Zotero API integration
   - Tag frequency analysis
   - Item association tracking
   - Comprehensive reporting

3. **`02_analyze_tags.py`** ✅ - Tag pattern analysis (2,164 lines)
   - Fuzzy matching for similarity detection
   - Hierarchical relationship detection
   - Co-occurrence network analysis
   - Data quality categorisation
   - Network visualisation

4. **`03_inspect_multiple_attachments.py`** ✅ - Data quality checks (1,243 lines)
   - Multiple attachment detection and categorisation
   - Priority-based flagging system
   - Detailed inspection reports

### Phase 1 Scripts 📋 PLANNED

5. **`vocabulary_mapper.py`** 📋 - Getty/RVA mapping tools
   - Map tags to Getty AAT (Art & Architecture Thesaurus)
   - Map locations to Getty TGN (Thesaurus of Geographic Names)
   - Prepare SKOS format for RVA publication
   - Validate mappings

### Phase 2-3 Scripts 📋 PLANNED

6. **`ai_tagger_claude.py`** 📋 - Terminal-based tagging with Claude Code
   - Content extraction from PDFs
   - LLM-based tag suggestion
   - Interactive validation workflow

7. **`ai_tagger_local.py`** 📋 - Alternative using local LLM
   - Batch processing for untagged items
   - Local model integration (up to 120B)

8. **`location_extractor.py`** 📋 - NER for place names + geocoding
   - Named entity recognition for locations
   - Getty TGN mapping
   - Coordinate assignment

### Phase 4 Scripts 📋 PLANNED

9. **`license_handler.py`** 📋 - Trove licence detection + CC-BY application
    - Parse Trove licence metadata
    - Apply CC-BY as default
    - Document licence provenance

10. **`zotero_to_omeka.py`** 📋 - Main publication pipeline
    - Metadata transformation (Zotero → Dublin Core)
    - Item creation via Omeka Classic API
    - Collection assignment
    - Geographic data integration for CurateScape

11. **`fair_validator.py`** 📋 - Metadata quality checks
    - Validate FAIR4RS compliance
    - Check required metadata fields
    - Verify controlled vocabulary usage
    - Generate quality reports

---

## Deliverables

**Academic:**
- ✅ Reproducible scripts + comprehensive documentation (FAIR4RS compliant, Oct 2025)
- 📋 Rationalised controlled vocabulary published to RVA
- 📋 Mappings to Getty vocabularies
- 📋 Fully-tagged Zotero group library (shareable)

**Public-Facing:**
- 📋 FAIR-compliant Omeka Classic collection
- 📋 CurateScape mobile tours
- 📋 Thematic exhibits

**Documentation (Completed Oct 2025):**
- ✅ CITATION.cff, codemeta.json for software citation
- ✅ Comprehensive README.md (667 lines)
- ✅ API integration guide (docs/api-integration.md, 800 lines)
- ✅ Data format specifications (docs/data-formats.md)
- ✅ Vocabulary standards documentation (docs/vocabularies.md)
- ✅ Gazetteer comparison (docs/gazetteer-comparison.md)
- ✅ Folder-specific READMEs (scripts, data, reports, planning)
- ✅ Code documentation (~4,100 lines of docstrings and comments)
- ✅ CONTRIBUTING.md, CHANGELOG.md, CLAUDE.md

---

## Project Configuration

**Zotero:**
- Type: Group library (ID: 2258643)
- API: Enabled and documented (docs/api-integration.md)
- Focus: Primary sources (newspaper articles, late 19th/early 20th century)
- Status: ✅ Configured in scripts/config.py

**Omeka:**
- Version: Omeka Classic
- Site: <https://shaleheritage.au/>
- API Endpoint: <https://shaleheritage.au/api>
- Maximum results per page: 50
- API: Enabled and documented (docs/api-integration.md)
- Extensions: CurateScape for mobile tours
- Status: ✅ Configured in scripts/config.py and .env.example

**Licensing:**
- Default: CC-BY
- Trove items: Inherit original licences
- Documentation: README.md, CONTRIBUTING.md

**AI Tagging:**
- Primary: Claude Code (terminal-based)
- Alternative: Local LLM (up to 120B)
- Validation: 5-10% spot-checking after initial intensive review

---

## Optional Future Enhancements

Beyond the core 6-phase workflow, optional enhancements could improve software sustainability and reach:

### High Priority (Low Effort)

1. **Zenodo DOI Integration** (2-3 hours) - Persistent identifiers for software releases
2. **GitHub Actions CI** (3-5 hours) - Automated testing and quality checks
3. **Docker Container** (4-6 hours) - Simplified installation and deployment

### Medium Priority (Medium Effort)

4. **Example Jupyter Notebooks** (6-8 hours) - Interactive tutorials for researchers
5. **Command-Line Interface** (6-10 hours) - Unified CLI for all scripts
6. **Automated Testing Suite** (10-15 hours) - pytest framework with >80% coverage

### Lower Priority (Higher Effort)

7. **Read the Docs Hosting** (8-12 hours) - Professional documentation with versioning
8. **Data Quality Dashboard** (12-18 hours) - Visual analytics using Dash or Streamlit
9. **Video Tutorials** (10-15 hours) - Installation and usage screencasts
10. **RVA Publishing Automation** (15-20 hours) - Direct vocabulary publishing to RVA

**Detailed specifications** for all enhancements available in `planning/FAIR4RS-documentation-plan.md` (Optional Future Enhancements section).

**Note:** These are optional quality-of-life improvements. The core software is already FAIR4RS compliant and publication-ready as of October 2025.
