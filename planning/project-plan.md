# Zotero → Omeka Classic Publication Workflow

**Project:** Historical Newspaper Sources + Archaeological Evidence Digital Collection
**Date:** 2025-10-08
**Tools:** Zotero API, Omeka Classic API, Claude/Local LLM, CurateScape

---

## Phase 1: Tag Rationalization & Vocabulary Publishing

### 1.1 Folksonomy Analysis
- Extract all existing tags from Zotero group library
- Analyze tag usage patterns, frequencies, overlaps
- Interview/consult with historians who created tags
- Document current folksonomy logic and categories

### 1.2 Tag Schema Rationalization
- Consolidate similar/duplicate tags
- Standardize terminology and structure
- Create hierarchical organization if needed
- Document definitions and scope notes

### 1.3 Vocabulary Mapping & Publication
- Map rationalized tags → Getty vocabularies (AAT/TGN)
- Prepare metadata for Research Vocabularies Australia (RVA)
- Publish controlled vocabulary to RVA
- Document mappings for interoperability

### 1.4 Batch Update Zotero
- Apply rationalized tags to existing items via API
- Preserve original tags as backup (separate collection/export)
- Validate updates

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

## Key Scripts to Develop

1. **`zotero_folksonomy_analysis.py`** - Tag extraction and analysis
2. **`vocabulary_mapper.py`** - Getty/RVA mapping tools
3. **`ai_tagger_claude.py`** - Terminal-based tagging with Claude Code
4. **`ai_tagger_local.py`** - Alternative using local LLM
5. **`location_extractor.py`** - NER for place names + geocoding
6. **`license_handler.py`** - Trove license detection + CC-BY application
7. **`zotero_to_omeka.py`** - Main publication pipeline
8. **`fair_validator.py`** - Metadata quality checks

---

## Deliverables

**Academic:**
- Rationalized controlled vocabulary published to RVA
- Mappings to Getty vocabularies
- Fully-tagged Zotero group library (shareable)
- Reproducible scripts + documentation

**Public-Facing:**
- FAIR-compliant Omeka Classic collection
- CurateScape mobile tours
- Thematic exhibits

---

## Project Configuration

**Zotero:**
- Type: Group library
- API: Already enabled
- Focus: Primary sources (newspaper articles, late 19th/early 20th century)

**Omeka:**
- Version: Omeka Classic
- API: Already enabled
- Extensions: CurateScape for mobile tours

**Licensing:**
- Default: CC-BY
- Trove items: Inherit original licenses

**AI Tagging:**
- Primary: Claude Code (terminal-based)
- Alternative: Local LLM (up to 120B)
- Validation: 5-10% spot-checking after initial intensive review
