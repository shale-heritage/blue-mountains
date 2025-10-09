# Phase 1: Tag Rationalization & Vocabulary Publishing (Detailed)

**Goal:** Transform the existing folksonomy into a rationalized controlled vocabulary, map it to standard vocabularies (Getty), publish to RVA, and apply it consistently across the Zotero library.

---

## 1.1 Folksonomy Analysis

### Objectives
- Understand the current tagging landscape
- Identify patterns, inconsistencies, and gaps
- Document the logic behind existing tags
- Establish baseline metrics

### Tasks

#### 1.1.1 Extract Tags from Zotero
**Script:** `scripts/01_extract_tags.py`

**Actions:**
- Connect to Zotero group library via API
- Retrieve all tags across all items
- Generate comprehensive tag inventory with:
  - Tag name
  - Number of items using tag
  - Items associated with each tag
  - Tag creation patterns (if available)

**Outputs:**
- `data/raw_tags.json` - Complete tag data
- `data/tag_frequency.csv` - Tags sorted by usage frequency
- `reports/tag_summary.md` - Overview statistics

**Key Metrics:**
- Total number of unique tags
- Total number of tagged items
- Average tags per item
- Tags used only once (candidates for consolidation)
- Most frequently used tags
- Untagged items count

#### 1.1.2 Analyze Tag Patterns
**Script:** `scripts/02_analyze_tags.py`

**Actions:**
- Identify similar tags (fuzzy matching):
  - Spelling variations
  - Singular/plural forms
  - Hyphenation differences
  - Case inconsistencies
- Detect potential hierarchies:
  - Broad vs. specific terms
  - Geographic hierarchies (e.g., "Blue Mountains" vs. "Katoomba")
  - Thematic categories
- Find orphaned/underused tags
- Map tag co-occurrence (which tags appear together)

**Outputs:**
- `reports/tag_analysis.md` - Detailed analysis
- `data/similar_tags.csv` - Suggested merges
- `data/tag_network.json` - Co-occurrence patterns
- `visualizations/tag_cloud.png` - Visual representation

#### 1.1.3 Document Folksonomy Logic
**Manual Process with Historian Input**

**Actions:**
- Review tag categories with project historians
- Document the reasoning behind tag choices
- Identify domain-specific terminology
- Understand regional/temporal specificity
- Clarify ambiguous tags

**Tool:** Interview template + collaborative document

**Outputs:**
- `planning/folksonomy_logic.md` - Documented rationale
- `planning/domain_terms.md` - Specialist vocabulary explanations
- `planning/tag_ambiguities.md` - Terms requiring clarification

---

## 1.2 Tag Schema Rationalization

### Objectives
- Create consistent, clearly-defined controlled vocabulary
- Eliminate redundancy
- Establish hierarchical structure where appropriate
- Prepare for external vocabulary mapping

### Tasks

#### 1.2.1 Consolidate Similar Tags
**Script:** `scripts/03_consolidate_tags.py`

**Actions:**
- Review similar tags from analysis (1.1.2)
- Create consolidation rules:
  - Merge spelling variants → canonical form
  - Standardize singular/plural (choose convention)
  - Resolve hyphenation (choose convention)
  - Normalize capitalization
- Generate mapping file: old_tag → new_tag

**Outputs:**
- `data/tag_consolidation_map.csv` - Transformation rules
- `reports/consolidation_preview.md` - Before/after comparison
- `data/tags_deduplicated.json` - Consolidated tag list

**Review Required:** Yes - historian approval before applying

#### 1.2.2 Standardize Terminology
**Collaborative Process**

**Actions:**
- Establish naming conventions:
  - Capitalization rules
  - Abbreviation standards
  - Hyphenation/spacing rules
  - Special character handling
- Identify preferred terms for concepts:
  - "Aboriginal" vs. "Indigenous" vs. "First Nations"
  - Historical vs. contemporary place names
  - Industry terminology standardization
- Create term preference guide

**Outputs:**
- `planning/naming_conventions.md` - Style guide
- `planning/preferred_terms.md` - Terminology choices
- `data/standardization_map.csv` - Old → standardized terms

#### 1.2.3 Create Hierarchical Structure
**Script:** `scripts/04_hierarchy_builder.py`

**Actions:**
- Identify broad categories (top-level):
  - Geographic (places)
  - Thematic (industries, social issues, events)
  - Temporal (periods, specific dates)
  - Actors (people, organizations)
  - Document types
- Nest specific tags under broader terms
- Create parent-child relationships
- Define facets for multi-dimensional classification

**Example Hierarchy:**
```
Geographic
├── Blue Mountains Region
│   ├── Katoomba
│   ├── Leura
│   └── Blackheath
├── Sydney
└── Regional NSW

Thematic
├── Tourism
│   ├── Hotels
│   ├── Railways
│   └── Scenic attractions
├── Mining
│   ├── Coal
│   └── Shale
└── Conservation
```

**Outputs:**
- `data/tag_hierarchy.json` - Structured taxonomy
- `visualizations/tag_tree.html` - Interactive visualization
- `planning/facet_design.md` - Multi-faceted classification scheme

#### 1.2.4 Document Definitions
**Manual/Collaborative Process**

**Actions:**
- Write scope notes for each tag:
  - Clear definition
  - Usage guidelines
  - Examples of when to apply
  - Exclusions (when NOT to apply)
- Establish relationships between tags:
  - Broader terms
  - Narrower terms
  - Related terms
  - Use instead of (deprecated tags)

**Outputs:**
- `data/tag_definitions.csv` - Tag dictionary
- `planning/tagging_guidelines.md` - Usage manual
- `data/tag_relationships.json` - SKOS-like structure

---

## 1.3 Vocabulary Mapping & Publication

### Objectives
- Map local vocabulary to established standards
- Enable interoperability with external systems
- Publish vocabulary to Research Vocabularies Australia
- Document mappings for FAIR compliance

### Tasks

#### 1.3.1 Map to Getty Vocabularies
**Script:** `scripts/05_getty_mapper.py`

**Primary Getty Vocabularies:**
- **AAT (Art & Architecture Thesaurus)** - Concepts, activities, materials, styles
- **TGN (Thesaurus of Geographic Names)** - Places, administrative entities
- **ULAN (Union List of Artist Names)** - People/organizations (if applicable)

**Actions:**
- Query Getty APIs for each rationalized tag
- Match local terms to Getty URIs:
  - Exact matches
  - Close matches
  - Broader/narrower matches
  - No match (local terms)
- Document match confidence levels
- Handle Australian-specific terms (may not be in Getty)

**Mapping Types:**
- `skos:exactMatch` - Identical concept
- `skos:closeMatch` - Very similar concept
- `skos:broadMatch` - Getty term is broader
- `skos:narrowMatch` - Getty term is narrower
- `skos:relatedMatch` - Related but not hierarchical

**Outputs:**
- `data/getty_mappings.csv` - Tag → Getty URI mapping
- `data/unmapped_terms.csv` - Terms without Getty equivalents
- `reports/getty_coverage.md` - Coverage statistics
- `data/vocabulary_skos.ttl` - SKOS-formatted vocabulary with mappings

#### 1.3.2 Prepare RVA Submission
**Manual/Script-Assisted Process**

**Actions:**
- Review RVA requirements and metadata schema
- Prepare vocabulary metadata:
  - Title, description, purpose
  - Creator/contributor information
  - Version, publication date
  - License (likely CC-BY)
  - Scope and coverage
- Format vocabulary according to RVA standards:
  - SKOS/RDF format
  - Include definitions, scope notes
  - Include Getty mappings
  - Include hierarchy
- Prepare documentation:
  - Vocabulary overview
  - Usage guidelines
  - Version history

**Outputs:**
- `rva_submission/vocabulary_metadata.json` - RVA-compliant metadata
- `rva_submission/vocabulary.ttl` - SKOS/RDF vocabulary file
- `rva_submission/documentation.pdf` - Human-readable guide
- `rva_submission/submission_notes.md` - Submission checklist

#### 1.3.3 Publish to RVA
**Manual Process**

**Actions:**
- Submit vocabulary to Research Vocabularies Australia
- Obtain persistent URI for vocabulary
- Record vocabulary identifier
- Document citation information

**Outputs:**
- `planning/rva_publication_record.md` - Publication details
- Persistent vocabulary URI (to be used in metadata)

#### 1.3.4 Document Mappings
**Script:** `scripts/06_mapping_documentation.py`

**Actions:**
- Create comprehensive mapping documentation
- Generate human-readable crosswalks
- Prepare machine-readable mapping files
- Document versioning and provenance

**Outputs:**
- `docs/vocabulary_crosswalk.md` - All mappings in readable format
- `data/mappings_complete.json` - Machine-readable mappings
- `docs/mapping_provenance.md` - Mapping methodology and decisions
- `docs/vocabulary_version_history.md` - Change log

---

## 1.4 Batch Update Zotero

### Objectives
- Apply rationalized vocabulary to Zotero library
- Preserve original data as backup
- Validate successful updates
- Minimize disruption to ongoing work

### Tasks

#### 1.4.1 Backup Original Tags
**Script:** `scripts/07_backup_tags.py`

**Actions:**
- Export complete Zotero library metadata
- Create timestamped backup:
  - All item metadata
  - All tag associations
  - Library structure
- Verify backup integrity
- Document backup location

**Outputs:**
- `backups/YYYY-MM-DD_zotero_full_export.json` - Complete backup
- `backups/YYYY-MM-DD_tag_snapshot.csv` - Tag relationships
- `backups/backup_manifest.md` - Backup documentation

#### 1.4.2 Apply Tag Updates
**Script:** `scripts/08_update_zotero_tags.py`

**Actions:**
- Load consolidation map + standardization map
- For each item with old tags:
  - Remove old tag
  - Add new (rationalized) tag
  - Preserve all other metadata
- Handle edge cases:
  - Items with multiple tags that consolidate to one
  - Tags that split into multiple (rare)
  - Tags with no mapping (preserve original?)
- Batch updates (e.g., 100 items at a time)
- Log all changes
- Rate limiting (respect Zotero API limits)

**Update Strategy:**
- Dry run first (preview changes without applying)
- Test with small subset (10-20 items)
- Validate test batch manually
- Proceed with full update
- Monitor for errors

**Outputs:**
- `logs/tag_update_YYYY-MM-DD.log` - Detailed change log
- `reports/update_summary.md` - Statistics and outcomes
- `data/failed_updates.csv` - Items that failed to update (if any)

#### 1.4.3 Validate Updates
**Script:** `scripts/09_validate_updates.py`

**Actions:**
- Re-query Zotero library post-update
- Compare against expected state:
  - All old tags removed?
  - All new tags applied correctly?
  - No unintended changes?
- Spot-check random sample (20-30 items)
- Verify tag counts match expectations
- Check for orphaned items (lost tags)

**Validation Checks:**
- Total tag count (should decrease after consolidation)
- Items per tag (should increase for consolidated tags)
- No items lost tags entirely (unless untagged initially)
- Tag names match controlled vocabulary exactly

**Outputs:**
- `reports/validation_report.md` - Validation results
- `data/discrepancies.csv` - Any unexpected outcomes
- `reports/final_tag_inventory.csv` - Post-update tag landscape

#### 1.4.4 Update Documentation
**Manual Process**

**Actions:**
- Update Zotero library description with:
  - Controlled vocabulary information
  - Link to RVA vocabulary
  - Tagging guidelines
- Create Zotero group note with vocabulary guide
- Share vocabulary documentation with collaborators
- Train RAs on new tagging standards

**Outputs:**
- `docs/zotero_library_guide.md` - Library documentation
- Zotero group note (created via web interface)
- `docs/ra_training_materials.md` - Training guide

---

## Phase 1 Scripts Summary

| Script | Purpose | Inputs | Outputs |
|--------|---------|--------|---------|
| `01_extract_tags.py` | Pull all tags from Zotero | Zotero API | `raw_tags.json`, `tag_frequency.csv` |
| `02_analyze_tags.py` | Identify patterns/issues | `raw_tags.json` | `tag_analysis.md`, `similar_tags.csv` |
| `03_consolidate_tags.py` | Merge similar tags | `similar_tags.csv` + manual review | `tag_consolidation_map.csv` |
| `04_hierarchy_builder.py` | Create taxonomy | Consolidated tags | `tag_hierarchy.json` |
| `05_getty_mapper.py` | Map to Getty vocabularies | Rationalized tags | `getty_mappings.csv`, `vocabulary_skos.ttl` |
| `06_mapping_documentation.py` | Document all mappings | All mapping files | `vocabulary_crosswalk.md` |
| `07_backup_tags.py` | Backup Zotero library | Zotero API | Timestamped backup files |
| `08_update_zotero_tags.py` | Apply new tags to Zotero | Mapping files | Updated Zotero library, logs |
| `09_validate_updates.py` | Verify updates | Zotero API + expected state | `validation_report.md` |

---

## Phase 1 Folder Structure

```
blue-mountains/
├── planning/
│   ├── project-plan.md
│   ├── phase1-detailed.md
│   ├── folksonomy_logic.md
│   ├── domain_terms.md
│   ├── tag_ambiguities.md
│   ├── naming_conventions.md
│   ├── preferred_terms.md
│   ├── facet_design.md
│   ├── tagging_guidelines.md
│   ├── rva_publication_record.md
│   └── vocabulary_version_history.md
├── scripts/
│   ├── 01_extract_tags.py
│   ├── 02_analyze_tags.py
│   ├── 03_consolidate_tags.py
│   ├── 04_hierarchy_builder.py
│   ├── 05_getty_mapper.py
│   ├── 06_mapping_documentation.py
│   ├── 07_backup_tags.py
│   ├── 08_update_zotero_tags.py
│   ├── 09_validate_updates.py
│   └── config.py (API keys, settings)
├── data/
│   ├── raw_tags.json
│   ├── tag_frequency.csv
│   ├── tag_network.json
│   ├── similar_tags.csv
│   ├── tags_deduplicated.json
│   ├── tag_consolidation_map.csv
│   ├── standardization_map.csv
│   ├── tag_hierarchy.json
│   ├── tag_definitions.csv
│   ├── tag_relationships.json
│   ├── getty_mappings.csv
│   ├── unmapped_terms.csv
│   ├── vocabulary_skos.ttl
│   ├── mappings_complete.json
│   └── final_tag_inventory.csv
├── reports/
│   ├── tag_summary.md
│   ├── tag_analysis.md
│   ├── consolidation_preview.md
│   ├── getty_coverage.md
│   ├── update_summary.md
│   └── validation_report.md
├── backups/
│   ├── YYYY-MM-DD_zotero_full_export.json
│   ├── YYYY-MM-DD_tag_snapshot.csv
│   └── backup_manifest.md
├── rva_submission/
│   ├── vocabulary_metadata.json
│   ├── vocabulary.ttl
│   ├── documentation.pdf
│   └── submission_notes.md
├── docs/
│   ├── vocabulary_crosswalk.md
│   ├── mapping_provenance.md
│   ├── zotero_library_guide.md
│   └── ra_training_materials.md
├── visualizations/
│   ├── tag_cloud.png
│   └── tag_tree.html
└── logs/
    └── tag_update_YYYY-MM-DD.log
```

---

## Getting Started - First Steps

1. **Set up environment:**
   - Create folder structure
   - Install Python dependencies (`pyzotero`, `requests`, `pandas`, etc.)
   - Configure Zotero API credentials

2. **Run initial extraction:**
   - Execute `01_extract_tags.py`
   - Review `tag_summary.md` for baseline understanding

3. **Begin analysis:**
   - Execute `02_analyze_tags.py`
   - Review outputs with project historians

4. **Schedule collaboration sessions:**
   - Folksonomy logic documentation (1.1.3)
   - Tag consolidation decisions (1.2.1)
   - Terminology standardization (1.2.2)

---

## Timeline Estimate

| Task | Estimated Time | Dependencies |
|------|---------------|--------------|
| 1.1 Folksonomy Analysis | 3-5 days | Zotero API access, historian availability |
| 1.2 Tag Rationalization | 1-2 weeks | Completed analysis, collaborative decision-making |
| 1.3 Vocabulary Mapping | 1 week | Rationalized tags, Getty API access |
| 1.4 Batch Update Zotero | 2-3 days | All mappings finalized, backup complete |
| **Total Phase 1** | **3-4 weeks** | Assumes part-time work, collaborative input |

---

## Next Steps

Ready to begin? Let's start with:
1. Setting up the project structure
2. Configuring Zotero API access
3. Running the first tag extraction script
