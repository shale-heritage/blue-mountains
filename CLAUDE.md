# Blue Mountains Folksonomy Rationalization Project

## Project Purpose

Rationalize 1600+ folksonomy tags from the Blue Mountains Historical Society's Zotero library into a controlled vocabulary aligned with Getty Art & Architecture Thesaurus (AAT) structure. Transform user-generated tags into a hierarchical, polyhierarchical thesaurus suitable for cultural heritage research.

## Core Principles

### Getty AAT Alignment
- Follow Getty AAT hierarchy structure and relationships
- Use AAT preferred terms where they exist
- Reference vocab.getty.edu for authoritative terminology
- Document deviations from AAT with rationale
- Maintain semantic compatibility with broader GLAM vocabularies

### Vocabulary Structure
- **Polyhierarchical relationships** - Entities can have multiple broader terms
- **Faceted classification** - Seven primary facets organize all terms
- **Australian/regional terminology** - Preserve local usage where culturally significant
- **Disambiguation** - Use parenthetical qualifiers for homographs

### Leaf-Node Tagging Pattern

**CRITICAL**: This taxonomy follows a strict leaf-node tagging pattern where only leaf nodes are used to tag Zotero items. Parent nodes organise the hierarchy but are never directly applied.

**Pattern Structure:**
```
Plural Parent (organisational node - never tagged)
├── Singular Generic Leaf (tagged for unspecified items)
├── Specific Named Leaf 1 (tagged for specific entity)
├── Specific Named Leaf 2 (tagged for specific entity)
└── Specific Named Leaf N (tagged for specific entity)
```

**Examples:**

Hotels (parent - never tagged)
├── Hotel (generic leaf - for unspecified hotels)
├── Grand Hotel (specific leaf - for this hotel)
├── Imperial Hotel (specific leaf - for this hotel)
└── Railway Hotel (specific leaf - for this hotel)

Retailers and Stores (parent - never tagged)
├── Retailer or Store (generic leaf - for unspecified retailers)
├── Douglas and Company (specific leaf - for this business)
├── Nimmo's (specific leaf - for this business)
├── Peckman Brothers (specific leaf - for this business)
└── Tabrett and Company (specific leaf - for this business)

Schools (parent - never tagged)
├── School (generic leaf - for unspecified schools)
├── Katoomba Public School (specific leaf - for this school)
└── Mount Victoria School (specific leaf - for this school)

**Key Rules:**

1. **Plural parents are organisational only** - They structure the taxonomy but are never applied to items
2. **Singular generic leaves handle unspecified cases** - Use when source mentions "a hotel" or "a retailer" without naming it
3. **Specific named leaves for identified entities** - Use when source provides the actual name
4. **All tagging happens at leaf level** - Never tag with parent nodes
5. **Consistency across entire taxonomy** - This pattern applies to all categories (agents, buildings, events, etc.)

**Important Exception - When NOT to Include Singular Generics:**

Not every plural parent requires a singular generic leaf. Singular generics should only exist when there are realistic scenarios where source text would mention the category generically without naming the specific entity.

**Include singular generic when:**
- Source might say "stayed at a hotel" (without naming which) → Hotel
- Source might say "attended a school" (without naming which) → School
- Source might say "a mountain feature" (without specifying) → Mountain feature

**Do NOT include singular generic when:**
- Entities are always named/specific in sources (e.g., government authorities)
- Example: "Postal authorities" → only "Postal Department" (no generic "Postal authority")
- Example: "Railway authorities" → only "Railway commission" (no generic "Railway authority")
- Organisational entities, regulatory bodies, and official authorities are always named in historical sources

**Why This Pattern:**

- **Precision**: Clear distinction between category (parent), generic instance (singular leaf), and specific entity (named leaf)
- **Browsing**: Users can navigate hierarchies without being overwhelmed by generic "category" tags
- **Searchability**: Filtering by parent shows all children; filtering by leaf shows specific instances
- **Data quality**: Prevents mixing of organisational nodes with actual taggable terms
- **Getty AAT alignment**: Matches authoritative vocabulary structure patterns

**When Consolidating Tags:**

- Always check: is this a parent node or a leaf node?
- Parent nodes should be plural and have children
- Generic leaves should be singular ("Hotel" not "Hotels")
- Specific leaves use proper names or identifying phrases
- Never merge a parent into a leaf or vice versa

### Dual-Nature Entity Handling

**CURRENT APPROACH** (pending Getty AAT alignment review - see planning/TODO.md):

Some entities have both organisational and physical structure aspects (e.g., Schools of Arts, Churches, Fraternal halls). These dual-nature entities currently use **polyhierarchical relationships** (same tag appears in multiple facets without disambiguation).

**Current Implementation:**

```
Built Environment > Halls > Schools of Arts
    ├── Katoomba School of Arts
    └── School of Arts

Agents > Cultural societies > Schools of Arts
    ├── Katoomba School of Arts
    └── School of Arts
```

**Known Limitation:**

The CSV data structure doesn't support facet-specific display names. Any attempt to add parenthetical qualifiers (e.g., "Schools of Arts (venues)") renames the tag globally, breaking parent-child relationships across all facets.

**Strategic Decision Deferred:**

Two approaches under consideration:

1. **Polyhierarchy (current):** Same tag in multiple facets
   - ✅ Matches source terminology
   - ✅ Single tag application
   - ❌ Lacks visualization clarity

2. **Disambiguation (alternative):** Separate tags with parenthetical qualifiers
   - ✅ Explicit clarity (e.g., "Schools of Arts (organization)" vs "Schools of Arts (venue)")
   - ✅ Unique identifiers in primary taxonomies
   - ❌ Requires cataloguers to choose aspect
   - ❌ Departs from source terminology

See planning/TODO.md lines 42-140 for comprehensive analysis. Decision will be made during Phase 1.3 based on Getty AAT authoritative practice.

### Quality Standards
- Every consolidation decision must be evidence-based (context analysis from Zotero full text)
- Maintain audit trail in `planning/consolidation-decisions.md`
- Validate all changes before applying to master CSV
- Document ambiguous cases for review

## Project-Specific Acronyms

Expand on first usage in each file:
- **AAT**: Art & Architecture Thesaurus (Getty vocabulary)
- **TGN**: Thesaurus of Geographic Names (Getty vocabulary)  
- **ULAN**: Union List of Artist Names (Getty vocabulary)
- **RVA**: Research Vocabularies Australia
- **SKOS**: Simple Knowledge Organization System
- **GLAM**: Galleries, Libraries, Archives, Museums
- **KWIC**: Key Word In Context (concordance analysis method)

## Project Structure
```
data/
├── tag_consolidation_map.csv        # MASTER MAPPING (single source of truth)
├── full_dataset.csv                 # Complete Zotero export
└── *.md5                           # Checksums for data integrity

scripts/
├── 01-99_*.py                      # Numbered analysis/processing scripts
├── setup.sh                        # Virtual environment setup
└── run.sh                          # Script runner with auto venv activation

reports/
├── tag_analysis.md                 # Core tag usage statistics
├── *_context_analysis.md           # KWIC analysis for specific tags
├── *_corrections_validation.md     # Validation reports
└── *.png                          # Visualizations (network graphs, etc.)

planning/
├── consolidation-decisions.md      # Decision log (critical audit trail)
├── phase*.md                       # Phase planning documents
└── session_summary_*.md           # Session handover notes

docs/
├── folksonomy_logic.md            # Hierarchy design principles
└── thesaurus_structure.md         # Vocabulary organization
```

## Critical Files

### Master Data
- **`data/tag_consolidation_map.csv`** - Single source of truth for all tag mappings
  - Columns: original_tag, preferred_term, broader_term, facet, relationship_type
  - Never edit directly without validation
  - Always generate MD5 checksum after changes

### Decision Documentation  
- **`planning/consolidation-decisions.md`** - Complete decision log
  - Document rationale for every consolidation
  - Include evidence from context analysis
  - Note alternative options considered
  - Required for audit trail and reproducibility

### Validation Files
- **`reports/tag_analysis.md`** - Current tag statistics
- **`reports/data_quality_issues.md`** - Known issues and corrections needed

## Analysis Workflow

### Standard Process
1. **Context extraction** - Use scripts/08+ to extract full-text contexts from Zotero
2. **KWIC analysis** - Generate concordance reports for naming variants
3. **Pattern identification** - Identify consolidation opportunities
4. **Decision documentation** - Log decisions with evidence in planning/
5. **Validation** - Run validation scripts before applying changes
6. **Application** - Update tag_consolidation_map.csv
7. **Verification** - Generate post-change reports

### Script Numbering Convention
- **01-09**: Setup and data preparation
- **10-19**: Entity-specific analysis (churches, councils, schools)
- **20-29**: Cross-cutting analysis (dual-nature entities, facets)
- **30-39**: Specific tag investigations (e.g., alcohol, accommodation)
- **40+**: Application and validation scripts

## Domain Knowledge

### Blue Mountains Historical Context
- Region in NSW, Australia (west of Sydney)
- Gold rush era (1850s-1900s)
- Railway development significant (1860s-1900s)
- Tourism industry emergence (late 1800s)
- Mining (coal, shale) important to local economy

### Entity Types Common in Collection
- **Community institutions**: Schools of Arts, Mechanics' Institutes
- **Fraternal organizations**: Oddfellows, Druids, Freemasons
- **Religious organizations**: Denominational churches, church schools
- **Built environment**: Hotels, railway infrastructure, public buildings
- **Economic activities**: Mining, tourism, agriculture, retail

### Disambiguation Examples
- "Lodge" → Freemasons' lodge vs. tourist accommodation
- "School" → Educational institution vs. School of Arts (community hall)
- "Church" → Religious organization vs. church building
- "Hall" → Community hall vs. lodge meeting place vs. accommodation

## Validation Commands

### Check Data Integrity
```bash
# Verify CSV structure
python scripts/01_check_csv_structure.py

# Check for duplicate mappings
awk -F',' '{print $1}' data/tag_consolidation_map.csv | sort | uniq -d

# Validate MD5 checksums
md5sum -c data/tag_consolidation_map.csv.md5
```

### Regenerate Reports
```bash
# Run comprehensive analysis
python scripts/11_regenerate_reports.py

# Check specific entity contexts
python scripts/09_analyse_variants_in_context.py "School of Arts"
```

## Common Issues and Solutions

**Issue**: Tag appears in multiple contexts with different meanings  
**Solution**: Use KWIC analysis (scripts/09) to examine all contexts, create disambiguation entries

**Issue**: Unsure whether to use AAT term or local Australian term  
**Solution**: Use AAT term as preferred, add local term as alternate, document in decisions.md

**Issue**: Entity has both organizational and built environment aspects  
**Solution**: Create polyhierarchical relationships (both facets), document as dual-nature in reports/

**Issue**: Consolidation changes affect many items  
**Solution**: Run impact analysis, validate sample before full application, document in decisions.md

## Getty AAT Quick Reference

**Primary AAT Facets Used:**
- **Activities Facet** - Actions, processes, functions
- **Agents Facet** - People, organizations, groups  
- **Objects Facet** - Physical things, built environment
- **Associated Concepts** - Abstract ideas, events, processes
- **Physical Attributes** - Materials, colors, dimensions

**Check AAT at:** https://vocab.getty.edu/

## Session Continuity

For session handovers, check:
1. **SESSION_HANDOVER.md** - Latest session state
2. **planning/TODO.md** - Active tasks
3. **git log** - Recent commits and decisions
4. **reports/** - Latest analysis results