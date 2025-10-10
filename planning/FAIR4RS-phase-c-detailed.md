# Phase C Detailed: Folder-Specific README Documentation

**Status:** Ready for implementation
**Estimated Time:** 1.5-2 hours
**Dependencies:** Phase A completion (FAIR4RS compliance), Phase B completion (Code documentation)
**Last Updated:** 2025-10-10

---

## Overview

Phase C completes the documentation architecture by creating folder-specific README files that provide contextual guidance within each working directory. While the main README.md provides a comprehensive overview for GitHub visitors and new users, folder READMEs serve as quick-reference guides for researchers actively working with specific parts of the project.

### Relationship to Previous Phases

**Phase A (Completed)** established external FAIR4RS compliance:
- CITATION.cff and codemeta.json (Findable)
- Main README.md with comprehensive overview (Accessible)
- docs/data-formats.md and docs/vocabularies.md (Interoperable)
- CONTRIBUTING.md and licence clarity (Reusable)

**Phase B (Completed)** established internal code clarity:
- Comprehensive module and function docstrings in all Python scripts
- Educational inline comments explaining design decisions
- UK/Australian spelling throughout
- Quality assurance (linting, spelling, markdown validation)

**Phase C (This Phase)** establishes contextual documentation:
- Folder-specific READMEs for scripts/, data/, reports/, planning/
- Data dictionaries and file format quick references
- Script execution guides and workflow documentation
- Planning document navigation

### Three-Tier Documentation Architecture

The Blue Mountains project implements a three-tier README strategy:

1. **Main README** (Phase A, completed): High-level overview for discoverability
   - Research context and project goals
   - Installation and getting started
   - FAIR compliance overview
   - Citation and licensing
   - **Audience:** GitHub visitors, new users, researchers evaluating the software

2. **docs/ Folder** (Phase A, completed): Deep-dive technical specifications
   - Data format schemas (data-formats.md)
   - Vocabulary standards (vocabularies.md)
   - Gazetteer analysis (gazetteer-comparison.md)
   - **Audience:** Developers integrating with the software, data scientists

3. **Folder READMEs** (Phase C, this phase): Contextual quick-reference guides
   - scripts/README.md: Script execution guide
   - data/README.md: Data dictionary
   - reports/README.md: Report interpretation guide
   - planning/README.md: Planning documents index
   - **Audience:** Active users working within specific directories

### Why Phase C Matters

**Problem:** Researchers navigating to a specific folder (e.g., `data/` to check output files, or `scripts/` to run a script) must context-switch back to the main README or search through documentation to find relevant information.

**Solution:** Folder-specific READMEs provide "just-in-time" documentation at the point of need. When a researcher opens the `data/` folder and sees dozens of JSON/CSV files, a local README.md immediately explains what each file contains and how to use it.

**Benefits:**
- Reduced cognitive load (no need to remember file naming conventions)
- Faster troubleshooting (common issues documented where they occur)
- Better onboarding (new team members can navigate independently)
- Improved maintainability (documentation lives near the code/data it describes)

---

## C1. scripts/README.md

### Purpose

Provide a quick-reference guide for running scripts, including execution order, dependencies, configuration requirements, and common troubleshooting.

### File Location

`/home/shawn/Code/blue-mountains/scripts/README.md`

### Estimated Length

150-200 lines

### Required Content

#### Section 1: Overview

Brief explanation of what the scripts/ directory contains and how scripts relate to the research workflow.

```markdown
# Blue Mountains Scripts Directory

This directory contains Python scripts for processing Zotero library data, analysing tags, and preparing controlled vocabularies for publication.

## Workflow Overview

Scripts execute in sequence to transform folksonomy tags into FAIR-compliant controlled vocabularies:

1. **01_extract_tags.py** - Extract tags from Zotero API
2. **02_analyze_tags.py** - Analyse similarity, hierarchies, co-occurrence, quality
3. **03_inspect_multiple_attachments.py** - Detailed quality inspection

Each script reads from Zotero API and/or previous script outputs, generates data files (data/), and produces reports (reports/).
```

#### Section 2: Script Table

Comprehensive table showing all scripts with their purpose, inputs, outputs, and dependencies.

**Table Structure:**

| Script | Purpose | Inputs | Outputs | Runtime | Dependencies |
|--------|---------|--------|---------|---------|--------------|
| `config.py` | Configuration management | `.env` file | Configuration constants | Immediate | python-dotenv, pathlib |
| `01_extract_tags.py` | Extract tags from Zotero | Zotero API | `raw_tags.json`, `tag_frequency.csv`, `tag_summary.md` | 2-5 min | config.py, pyzotero, pandas |
| `02_analyze_tags.py` | Analyse tag patterns | `raw_tags.json`, Zotero API | `similar_tags.csv`, `tag_hierarchies.csv`, `tag_network.json`, `quality_*.csv`, reports | 5-10 min | config.py, fuzzywuzzy, networkx, matplotlib |
| `03_inspect_multiple_attachments.py` | Inspect attachment patterns | `quality_multiple_attachments.csv`, Zotero API | `multiple_attachments_inspection.md`, `multiple_attachments_details.json` | 1-3 min | config.py, pyzotero |

**Notes to Include:**
- Runtime estimates based on ~1,200 item library
- All scripts require .env configuration
- Network connection required for Zotero API access
- Scripts must run in order (02 depends on 01 outputs)

#### Section 3: Configuration Requirements

Step-by-step .env setup instructions with security reminders.

```markdown
## Configuration Setup

### Step 1: Create .env File

Copy the example configuration:

```bash
cp .env.example .env
```

### Step 2: Add Zotero Credentials

Edit `.env` and add your Zotero API credentials:

```bash
# Required for all scripts
ZOTERO_GROUP_ID=2258643
ZOTERO_API_KEY_READONLY=your_readonly_key_here

# Required for future vocabulary publishing scripts
ZOTERO_API_KEY_READWRITE=your_readwrite_key_here
```

### Step 3: Generate API Keys

Visit https://www.zotero.org/settings/keys

1. **Read-Only Key** (for scripts 01-03):
   - Name: "Blue Mountains - Read Only"
   - Permissions: "Allow library access" → Read Only
   - Select: Blue Mountains group library (2258643)

2. **Read-Write Key** (for future scripts):
   - Name: "Blue Mountains - Read Write"
   - Permissions: "Allow library access" → Read/Write
   - Select: Blue Mountains group library (2258643)

### Security Reminder

⚠️ **NEVER commit .env to Git** - This file contains secret API keys and is listed in .gitignore. If accidentally committed, regenerate keys immediately at https://www.zotero.org/settings/keys
```

#### Section 4: Execution Guide

Clear instructions for running scripts with examples.

```markdown
## Running Scripts

### Prerequisites

1. Virtual environment activated:
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. Dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

3. Configuration complete (see Configuration Setup above)

### Execution Order

**Always run scripts in numerical order:**

#### Step 1: Extract Tags (Script 01)

```bash
python scripts/01_extract_tags.py
```

**What it does:**
- Connects to Zotero API
- Retrieves all items from group library (pagination)
- Extracts tags with item associations
- Calculates tag frequency statistics
- Generates summary report

**Expected outputs:**
- `data/raw_tags.json` (481 tags, ~500KB)
- `data/tag_frequency.csv` (sorted by usage)
- `reports/tag_summary.md` (statistical overview)

**Runtime:** 2-5 minutes (depends on library size and network speed)

#### Step 2: Analyse Tags (Script 02)

```bash
python scripts/02_analyze_tags.py
```

**What it does:**
- Loads raw_tags.json from Script 01
- Finds similar tags using fuzzy string matching
- Detects hierarchical relationships (parent-child tags)
- Calculates tag co-occurrence patterns
- Identifies data quality issues
- Generates network visualisations
- Produces comprehensive analysis report

**Expected outputs:**
- `data/similar_tags.csv` (consolidation recommendations)
- `data/tag_hierarchies.csv` (parent-child relationships)
- `data/tag_network.json` (co-occurrence data)
- `data/quality_*.csv` (4 quality issue files)
- `visualizations/*.png` (network graphs, frequency charts)
- `reports/tag_analysis.md` (comprehensive analysis)
- `reports/data_quality_issues.md` (quality summary)

**Runtime:** 5-10 minutes (fuzzy matching is computationally intensive)

#### Step 3: Inspect Attachments (Script 03)

```bash
python scripts/03_inspect_multiple_attachments.py
```

**What it does:**
- Loads quality_multiple_attachments.csv from Script 02
- Retrieves detailed attachment metadata from Zotero API
- Categorises attachment patterns (multiple PDFs, PDF+notes, etc.)
- Assigns review priority (HIGH/MEDIUM/LOW)
- Generates detailed inspection report

**Expected outputs:**
- `reports/multiple_attachments_inspection.md` (categorised review guide)
- `data/multiple_attachments_details.json` (full attachment metadata)

**Runtime:** 1-3 minutes (depends on number of flagged items)

### Running All Scripts Sequentially

To run the complete workflow:

```bash
# Activate virtual environment
source venv/bin/activate

# Run all three scripts in order
python scripts/01_extract_tags.py
python scripts/02_analyze_tags.py
python scripts/03_inspect_multiple_attachments.py

echo "✓ Workflow complete. Check reports/ for analysis results."
```
```

#### Section 5: Common Troubleshooting

Address frequent errors with solutions.

```markdown
## Troubleshooting

### Error: "Zotero credentials not found in .env file"

**Cause:** .env file missing or incorrectly configured

**Solutions:**
1. Check that `.env` file exists in project root (not in scripts/ directory)
2. Verify .env contains `ZOTERO_GROUP_ID` and `ZOTERO_API_KEY_READONLY`
3. Ensure no extra spaces around `=` in .env: `KEY=value` not `KEY = value`
4. Test configuration: `python scripts/config.py`

---

### Error: "ModuleNotFoundError: No module named 'pyzotero'"

**Cause:** Dependencies not installed or wrong virtual environment

**Solutions:**
1. Activate virtual environment: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Verify installation: `pip list | grep pyzotero`

---

### Error: "ConnectionError: Failed to connect to Zotero API"

**Cause:** Network issue or Zotero API maintenance

**Solutions:**
1. Check internet connection: `ping api.zotero.org`
2. Verify API key is valid: https://www.zotero.org/settings/keys
3. Check Zotero status: https://status.zotero.org/
4. Wait 5 minutes and retry (temporary API issues)

---

### Error: "HTTPError 403: Forbidden"

**Cause:** API key lacks required permissions or is invalid

**Solutions:**
1. Regenerate API key at https://www.zotero.org/settings/keys
2. Ensure "Allow library access" is checked
3. Ensure correct group library is selected (Blue Mountains 2258643)
4. Update .env file with new key
5. Test: `python scripts/01_extract_tags.py`

---

### Error: "FileNotFoundError: raw_tags.json not found" (Script 02)

**Cause:** Script 02 requires Script 01 outputs

**Solution:**
1. Run Script 01 first: `python scripts/01_extract_tags.py`
2. Verify output exists: `ls -lh data/raw_tags.json`
3. Then run Script 02: `python scripts/02_analyze_tags.py`

---

### Warning: "python-Levenshtein not found, using slow implementation"

**Cause:** Optional C acceleration library not installed

**Impact:** Script 02 runs 10-30× slower (30 seconds vs 1 second for fuzzy matching)

**Solution:**
1. Install: `pip install python-Levenshtein`
2. On Windows, may need Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
3. Rerun Script 02 to see performance improvement

---

### Scripts Run But No Visualisations Generated

**Cause:** Matplotlib backend issue or missing display

**Solutions:**
1. Check if PNG files exist: `ls -lh visualizations/`
2. If missing, check matplotlib backend: `python -c "import matplotlib; print(matplotlib.get_backend())"`
3. On headless servers, ensure non-interactive backend: Add to script: `matplotlib.use('Agg')`
4. Already configured in scripts, but verify matplotlib installation: `pip install --upgrade matplotlib`
```

#### Section 6: Script-Specific Notes

Additional details for each script.

```markdown
## Script-Specific Notes

### config.py

**Not directly executable** - Imported by all other scripts for configuration management.

**Testing configuration:**
```bash
python scripts/config.py
# Expected output: "✓ Configuration loaded successfully"
```

**API Key Strategy:**
- Read-only key: Scripts 01-03 (cannot modify library data)
- Read-write key: Future vocabulary publishing scripts
- Implements principle of least privilege for security

---

### 01_extract_tags.py

**Data Provenance:**
- Includes generation timestamp in all outputs
- Records Zotero group ID and library statistics
- Preserves item associations (which items use each tag)

**Performance Notes:**
- Uses pagination (100 items per request) to avoid timeouts
- Typical library (~1,200 items): 12 API requests, ~2-5 minutes
- Progress indicators show retrieval status

**Output Format:**
- JSON: Machine-readable, preserves nested structures
- CSV: Human-readable, sortable in Excel/LibreOffice
- Markdown: Report for project team review

---

### 02_analyze_tags.py

**Algorithmic Complexity:**
- Fuzzy matching: O(n²) where n = number of tags
- For 481 tags: 115,440 comparisons
- With python-Levenshtein: <1 second
- Without: ~30 seconds (pure Python implementation)

**Similarity Threshold:**
- Default: 80% (catches variants like "Mine"/"Mining")
- Adjustable in code: `threshold=80` parameter
- Higher = fewer false positives, may miss variants
- Lower = more matches, requires more manual review

**Network Visualisation:**
- Uses Fruchterman-Reingold force-directed layout
- Node size = tag frequency
- Edge width = co-occurrence count
- Saves to visualizations/tag_network.png

**Quality Categories:**
- Duplicates: Likely same item entered twice
- Non-primary sources: Reference works, compilations
- Multiple attachments: May combine distinct sources
- No attachments: Missing PDF/source document

---

### 03_inspect_multiple_attachments.py

**Categorisation Logic:**
- Multiple PDFs → HIGH PRIORITY (likely distinct sources)
- PDF + Notes → LOW PRIORITY (likely text extraction)
- Multiple Notes → REVIEW (may need consolidation)
- Mixed → REVIEW (unusual pattern)

**Manual Review Required:**
- Script assists but cannot replace human judgment
- Categorisation based on metadata, not PDF content
- Researchers must decide if articles should be split

**Integration with Workflow:**
- Uses quality_multiple_attachments.csv from Script 02
- Provides detailed inspection for flagged items
- Generates actionable recommendations for curation
```

#### Section 7: See Also

Links to related documentation.

```markdown
## See Also

- **Main README:** Project overview, installation, usage examples
- **CONTRIBUTING.md:** Code standards, documentation requirements, contribution workflow
- **docs/data-formats.md:** JSON schema specifications, CSV column definitions
- **data/README.md:** Data dictionary and file format quick reference
- **reports/README.md:** Report interpretation guide

---

## Questions or Issues?

- **Script errors:** Check Troubleshooting section above
- **Zotero API issues:** https://forums.zotero.org/
- **Project questions:** Open issue on GitHub or email project team
- **Contributing:** See CONTRIBUTING.md for code standards and pull request process
```

---

## C2. data/README.md

### Purpose

Provide a data dictionary explaining all files generated by scripts, including JSON schemas, CSV column definitions, file naming conventions, and data provenance.

### File Location

`/home/shawn/Code/blue-mountains/data/README.md`

### Estimated Length

200-250 lines

### Required Content

#### Section 1: Overview

```markdown
# Blue Mountains Data Directory

This directory contains machine-readable data files generated by processing scripts. All files are excluded from Git (.gitignore) and regenerated from Zotero API when scripts run.

## Data Lifecycle

1. **Generation:** Scripts extract/analyse Zotero library data
2. **Storage:** Outputs saved to data/ directory
3. **Usage:** Consumed by subsequent scripts or external tools
4. **Archival:** Important datasets backed up to backups/ before major changes
5. **Regeneration:** Files can be regenerated at any time by rerunning scripts

**Note:** This directory should be empty in a fresh clone. Run `python scripts/01_extract_tags.py` to populate it.
```

#### Section 2: File Inventory

Complete list of data files with generation source.

```markdown
## File Inventory

### Tag Extraction Data (from 01_extract_tags.py)

| File | Format | Size | Generated By | Purpose |
|------|--------|------|--------------|---------|
| `raw_tags.json` | JSON | ~500KB | 01_extract_tags.py | Complete tag extraction with metadata, statistics, item associations |
| `tag_frequency.csv` | CSV | ~30KB | 01_extract_tags.py | Tag usage frequencies, sorted descending |

### Tag Analysis Data (from 02_analyze_tags.py)

| File | Format | Size | Generated By | Purpose |
|------|--------|------|--------------|---------|
| `similar_tags.csv` | CSV | ~20KB | 02_analyze_tags.py | Tag pairs with similarity scores, consolidation recommendations |
| `tag_hierarchies.csv` | CSV | ~15KB | 02_analyze_tags.py | Detected parent-child tag relationships |
| `tag_network.json` | JSON | ~100KB | 02_analyze_tags.py | Tag co-occurrence data for network analysis |
| `quality_duplicates.csv` | CSV | ~5KB | 02_analyze_tags.py | Potential duplicate items flagged for review |
| `quality_non_primary_sources.csv` | CSV | ~40KB | 02_analyze_tags.py | Non-primary sources to exclude from analysis |
| `quality_multiple_attachments.csv` | CSV | ~10KB | 02_analyze_tags.py | Items with multiple attachments needing inspection |
| `quality_no_attachments.csv` | CSV | ~8KB | 02_analyze_tags.py | Items missing PDF/source documents |

### Attachment Inspection Data (from 03_inspect_multiple_attachments.py)

| File | Format | Size | Generated By | Purpose |
|------|--------|------|--------------|---------|
| `multiple_attachments_details.json` | JSON | ~50KB | 03_inspect_multiple_attachments.py | Full attachment metadata for flagged items |
```

#### Section 3: JSON Schemas

Detailed specifications for JSON files (reference docs/data-formats.md for full schemas).

```markdown
## JSON File Specifications

### raw_tags.json

**Purpose:** Complete tag extraction from Zotero group library with full provenance

**Structure:**

```json
{
  "metadata": {
    "generated_at": "ISO-8601 timestamp",
    "zotero_group_id": "string",
    "statistics": {
      "total_items": "integer",
      "items_with_tags": "integer",
      "items_without_tags": "integer",
      "unique_tags": "integer",
      "total_tag_applications": "integer",
      "avg_tags_per_item": "float",
      "max_tags_per_item": "integer",
      "min_tags_per_item": "integer"
    }
  },
  "tags": {
    "tag_name": {
      "count": "integer - number of items using this tag",
      "items": ["array of Zotero item keys"],
      "item_titles": ["array of item titles"]
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
      "item_titles": ["Katoomba Daily article 1901", "Mining report 1905"]
    }
  }
}
```

**Usage:**
- Input for 02_analyze_tags.py
- Can be loaded by external tools for custom analysis
- Contains full provenance (which items use which tags)

**See also:** docs/data-formats.md for complete JSON schema specification

---

### tag_network.json

**Purpose:** Tag co-occurrence data for network analysis and visualisation

**Structure:**

```json
{
  "metadata": {
    "generated_at": "ISO-8601 timestamp",
    "source_file": "raw_tags.json",
    "total_items_analysed": "integer",
    "unique_tags": "integer",
    "total_cooccurrences": "integer"
  },
  "cooccurrences": [
    {
      "tag1": "string",
      "tag2": "string",
      "count": "integer - how many items have both tags",
      "tag1_total": "integer - total usage of tag1",
      "tag2_total": "integer - total usage of tag2",
      "jaccard": "float - Jaccard similarity coefficient (future)"
    }
  ]
}
```

**Sorting:** Cooccurrences sorted by count (descending)

**Usage:**
- Generate network graphs (networkx, Gephi, Cytoscape)
- Identify related concepts
- Inform hierarchical vocabulary structure

---

### multiple_attachments_details.json

**Purpose:** Detailed attachment metadata for items flagged in quality checks

**Structure:**

```json
{
  "metadata": {
    "generated_at": "ISO-8601 timestamp",
    "source_file": "quality_multiple_attachments.csv",
    "total_items": "integer"
  },
  "items": [
    {
      "key": "Zotero item key",
      "title": "Item title",
      "itemType": "Zotero item type",
      "children": [
        {
          "key": "Attachment key",
          "itemType": "attachment | note",
          "contentType": "application/pdf | text/html | etc",
          "filename": "PDF filename",
          "title": "Note title",
          "note": "Note content (HTML)"
        }
      ],
      "category": "multiple_pdfs | pdf_plus_notes | multiple_notes | mixed_content | uncertain",
      "reasoning": "Human-readable categorisation explanation",
      "action": "HIGH PRIORITY | REVIEW | LOW PRIORITY"
    }
  ]
}
```

**Usage:**
- Manual review of attachment patterns
- Identify items that may combine multiple sources
- Guide curation decisions (split vs keep together)
```

#### Section 4: CSV Column Definitions

Specifications for all CSV files.

```markdown
## CSV File Specifications

### tag_frequency.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tag` | string | Tag name | "Mining" |
| `count` | integer | Number of items using this tag | 32 |
| `percentage` | float | Percentage of tagged items using this tag | 9.52 |

**Sorting:** Descending by count (most frequent first)

**Usage:**
- Quick overview of tag usage
- Identify most/least common tags
- Import to Excel/LibreOffice for analysis
- Visualisation (bar charts, word clouds)

---

### similar_tags.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `tag1` | string | First tag name | "Mine" |
| `tag2` | string | Second tag name | "Mining" |
| `count1` | integer | Usage count of tag1 | 15 |
| `count2` | integer | Usage count of tag2 | 32 |
| `similarity` | float (0-100) | Similarity score (Levenshtein-based) | 83.3 |
| `ratio` | float (0-100) | Basic ratio similarity | 83.3 |
| `partial` | float (0-100) | Partial substring similarity | 100.0 |
| `token_sort` | float (0-100) | Token sort similarity | 83.3 |
| `suggested_merge` | string | Recommended tag to keep | "Mining" |

**Sorting:** Descending by similarity (most similar first)

**Usage:**
- Manual review for tag consolidation
- Merge suggested_merge recommendations
- Apply to Zotero library (manual or scripted)

**Note:** `suggested_merge` recommends keeping the tag with higher usage count

---

### tag_hierarchies.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `parent` | string | Parent (broader) tag | "Mining" |
| `child` | string | Child (narrower) tag | "Coal Mine" |
| `parent_count` | integer | Usage count of parent tag | 32 |
| `child_count` | integer | Usage count of child tag | 8 |
| `cooccurrence` | integer | Items with both tags | 6 |
| `relationship_type` | string | Detection method | "substring" or "cooccurrence" |

**Sorting:** By parent tag, then child tag (alphabetical)

**Usage:**
- Develop hierarchical taxonomy
- Inform SKOS broader/narrower relationships
- Guide controlled vocabulary structure

**Relationship Types:**
- **substring:** Child tag contains parent as substring ("Coal Mine" contains "Mine")
- **cooccurrence:** Tags frequently appear together (>50% of child tag usage)

---

### quality_duplicates.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `key` | string | Zotero item key | "ABC123XYZ" |
| `title` | string | Item title | "Mining accident at Katoomba" |
| `date` | string | Publication date | "1901-05-15" |
| `itemType` | string | Zotero item type | "newspaperArticle" |
| `numAttachments` | integer | Number of attachments | 1 |
| `numTags` | integer | Number of tags | 5 |

**Usage:**
- Manual review to identify true duplicates
- Check if items are identical or distinct
- Merge or delete as appropriate in Zotero

---

### quality_non_primary_sources.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `key` | string | Zotero item key | "DEF456UVW" |
| `title` | string | Item title | "Australian Dictionary of Biography" |
| `itemType` | string | Zotero item type | "encyclopediaArticle" |
| `creator` | string | Author/creator | "Smith, John" |
| `date` | string | Publication date | "1990" |
| `numTags` | integer | Number of tags | 0 |

**Usage:**
- Exclude from primary source analysis
- Separate reference works from archival sources
- Focus tagging efforts on primary sources

**Non-primary item types:**
- encyclopediaArticle, dictionaryEntry
- book (reference works, compilations)
- webpage (modern secondary sources)

---

### quality_multiple_attachments.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `key` | string | Zotero item key | "GHI789STU" |
| `title` | string | Item title | "Katoomba news collection" |
| `itemType` | string | Zotero item type | "newspaperArticle" |
| `numChildren` | integer | Total number of attachments/notes | 3 |
| `date` | string | Publication date | "1901" |
| `tags` | string | Comma-separated tag list | "Mining, Katoomba, Women" |

**Usage:**
- Input for 03_inspect_multiple_attachments.py
- Identify items that may combine multiple sources
- Flag for manual review and potential splitting

---

### quality_no_attachments.csv

**Columns:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `key` | string | Zotero item key | "JKL012MNO" |
| `title` | string | Item title | "Mining report 1905" |
| `itemType` | string | Zotero item type | "document" |
| `creator` | string | Author/creator | "NSW Mines Department" |
| `date` | string | Publication date | "1905" |
| `url` | string | External URL (if present) | "http://trove.nla.gov.au/..." |

**Usage:**
- Identify items missing source documents
- Add PDFs from archival sources
- Prioritise digitisation efforts
```

#### Section 5: File Naming Conventions

```markdown
## File Naming Conventions

### Patterns

- **Tag data:** `tag_*.{json,csv}` (e.g., tag_frequency.csv, tag_network.json)
- **Quality checks:** `quality_*.csv` (e.g., quality_duplicates.csv)
- **Attachment details:** `*_attachments_*.{json,md}` (e.g., multiple_attachments_details.json)

### Case and Separators

- All lowercase
- Underscores (`_`) for word separation (snake_case)
- Descriptive nouns (not verbs)
- No dates in filenames (use metadata.generated_at in JSON)

### Versioning

Data files do not include version numbers. To preserve historical snapshots:

1. **Manual backup:** Copy important files to backups/ before major changes
   ```bash
   cp data/raw_tags.json backups/raw_tags_2025-10-09.json
   ```

2. **Timestamped archives:** Use ISO 8601 dates (YYYY-MM-DD)

3. **Git tracking:** Consider tracking select data files if they represent stable milestones
```

#### Section 6: Data Provenance

```markdown
## Data Provenance and Reproducibility

### Generation Timestamps

All JSON files include `metadata.generated_at` with ISO 8601 timestamps:

```json
"metadata": {
  "generated_at": "2025-10-09T10:30:00+11:00"
}
```

**Time zone:** All timestamps use Australian Eastern Time (AEDT/AEST, UTC+10/+11)

### Source Attribution

Files document their source:

- **raw_tags.json:** Extracted from Zotero Group 2258643
- **tag_network.json:** Derived from raw_tags.json
- **multiple_attachments_details.json:** Derived from quality_multiple_attachments.csv + Zotero API

### Reproducibility

To reproduce data files:

1. Ensure .env configuration matches original (same Zotero library)
2. Run scripts in order: 01 → 02 → 03
3. Compare generated_at timestamps to verify freshness

**Note:** Results may differ if Zotero library has changed between runs (new items, modified tags)

### Zotero Library Version

To check current library state:

```bash
# Count items in library
python -c "from pyzotero import zotero; import config; \
           zot = zotero.Zotero(config.ZOTERO_GROUP_ID, 'group', config.ZOTERO_API_KEY_READONLY); \
           print(f'Total items: {len(zot.items())}')"
```

Compare with `metadata.statistics.total_items` in raw_tags.json to detect library changes.
```

#### Section 7: Usage Examples

```markdown
## Usage Examples

### Loading JSON Data in Python

```python
import json
from pathlib import Path

# Load raw tags
with open('data/raw_tags.json', 'r', encoding='utf-8') as f:
    tag_data = json.load(f)

# Access metadata
print(f"Generated: {tag_data['metadata']['generated_at']}")
print(f"Total tags: {tag_data['metadata']['statistics']['unique_tags']}")

# Access tag information
mining_tag = tag_data['tags']['Mining']
print(f"'Mining' used on {mining_tag['count']} items")
print(f"Example item: {mining_tag['item_titles'][0]}")
```

### Loading CSV Data in Python (pandas)

```python
import pandas as pd

# Load tag frequency
freq_df = pd.read_csv('data/tag_frequency.csv')
print(freq_df.head(10))  # Top 10 tags

# Load similar tags
similar_df = pd.read_csv('data/similar_tags.csv')
high_similarity = similar_df[similar_df['similarity'] >= 90]
print(f"Found {len(high_similarity)} very similar pairs")
```

### Loading CSV in R

```r
library(readr)

# Load tag frequency
tag_freq <- read_csv("data/tag_frequency.csv")
head(tag_freq, 10)

# Visualise top 20 tags
library(ggplot2)
top_tags <- head(tag_freq, 20)
ggplot(top_tags, aes(x = reorder(tag, count), y = count)) +
  geom_bar(stat = "identity") +
  coord_flip() +
  labs(title = "Top 20 Most Frequent Tags",
       x = "Tag", y = "Usage Count")
```

### Network Analysis (networkx)

```python
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load co-occurrence data
with open('data/tag_network.json', 'r') as f:
    network_data = json.load(f)

# Build graph
G = nx.Graph()
for pair in network_data['cooccurrences']:
    if pair['count'] >= 3:  # Filter weak connections
        G.add_edge(pair['tag1'], pair['tag2'], weight=pair['count'])

# Calculate centrality
centrality = nx.degree_centrality(G)
top_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]

print("Most central tags (hubiest):")
for tag, score in top_central:
    print(f"  {tag}: {score:.3f}")

# Visualise (small network)
if len(G.nodes()) <= 50:
    nx.draw_spring(G, with_labels=True, node_size=500)
    plt.savefig('tag_network_custom.png')
```
```

#### Section 8: Backup and Archival

```markdown
## Backup and Archival Strategy

### Why Backup Data?

Data files are regenerated from Zotero API, so they're technically reproducible. However, backup is valuable when:

1. **Library changes:** Zotero library may be modified between runs
2. **Milestone preservation:** Capture state at publication time
3. **Historical analysis:** Compare tag evolution over time
4. **Quality assurance:** Revert if regeneration produces unexpected results

### Backup Procedure

Before major changes (tag consolidation, library cleaning):

```bash
# Create timestamped backup directory
BACKUP_DATE=$(date +%Y-%m-%d)
mkdir -p backups/$BACKUP_DATE

# Copy important data files
cp data/raw_tags.json backups/$BACKUP_DATE/
cp data/tag_network.json backups/$BACKUP_DATE/
cp data/quality_*.csv backups/$BACKUP_DATE/

# Document backup
echo "Backup created: $(date)" > backups/$BACKUP_DATE/README.txt
echo "Purpose: Pre-tag consolidation snapshot" >> backups/$BACKUP_DATE/README.txt

echo "✓ Backup saved to backups/$BACKUP_DATE/"
```

### Retention Policy

- **Short-term backups:** Keep for 6 months (active development)
- **Milestone backups:** Keep indefinitely (publication, major releases)
- **Automated cleanup:** Remove backups older than 6 months (except milestones)

### Restoration

To restore from backup:

```bash
# List available backups
ls -l backups/

# Restore from specific date
cp backups/2025-10-09/raw_tags.json data/

# Verify restoration
python -c "import json; \
           data = json.load(open('data/raw_tags.json')); \
           print(f\"Restored data from: {data['metadata']['generated_at']}\")"
```
```

#### Section 9: See Also

```markdown
## See Also

- **docs/data-formats.md:** Complete JSON schema specifications
- **scripts/README.md:** Script execution guide and workflow
- **reports/README.md:** Report interpretation guide
- **CONTRIBUTING.md:** Data quality standards and validation procedures

---

## Questions?

- **Data format questions:** See docs/data-formats.md for detailed schemas
- **Missing files:** Run `python scripts/01_extract_tags.py` to generate
- **Corrupted files:** Delete and regenerate by rerunning scripts
- **Custom analysis:** Load JSON/CSV in your tool of choice (Python, R, Excel)
```

---

## C3. reports/README.md

### Purpose

Explain the types of reports generated, their purpose, intended audience, update frequency, and how to interpret findings.

### File Location

`/home/shawn/Code/blue-mountains/reports/README.md`

### Estimated Length

100-150 lines

### Required Content

#### Section 1: Overview

```markdown
# Blue Mountains Reports Directory

This directory contains human-readable reports generated by analysis scripts. Reports are written in Markdown format for readability and are excluded from Git (.gitignore).

## Report Philosophy

Reports are designed for **human review and decision-making**, not machine processing. They:

- Summarise key findings in plain language
- Highlight actionable recommendations
- Provide context for quantitative results
- Support manual curation workflows

**Note:** This directory should be empty in a fresh clone. Run scripts to generate reports.
```

#### Section 2: Report Inventory

```markdown
## Report Inventory

| Report | Generated By | Audience | Update Frequency |
|--------|--------------|----------|------------------|
| `tag_summary.md` | 01_extract_tags.py | Project team, historians | After each extraction |
| `tag_analysis.md` | 02_analyze_tags.py | Vocabulary developers | After tag analysis |
| `data_quality_issues.md` | 02_analyze_tags.py | Data curators | After quality checks |
| `multiple_attachments_inspection.md` | 03_inspect_multiple_attachments.py | Research assistants | After attachment inspection |
```

#### Section 3: Report Descriptions

Detailed explanation of each report type.

```markdown
## Report Descriptions

### tag_summary.md

**Purpose:** Overview statistics from tag extraction

**Generated by:** `python scripts/01_extract_tags.py`

**Contains:**
- Library statistics (total items, tagged items, unique tags)
- Tag frequency distribution (top 20 most/least common tags)
- Tagging coverage (percentage of items with tags)
- Tags per item statistics (average, min, max)
- Items without tags (flagged for review)

**Intended audience:**
- Project team: Quick health check of tagging progress
- Historians: Understand subject coverage
- Research assistants: Identify items needing tags

**How to interpret:**
- **High unique_tags count:** Rich subject coverage (good) or inconsistent terminology (needs consolidation)
- **Low items_with_tags percentage:** More tagging work needed
- **High avg_tags_per_item:** Detailed subject indexing (good) or over-tagging (review)

**Typical review frequency:** Weekly during active tagging, monthly during analysis phase

---

### tag_analysis.md

**Purpose:** Detailed tag pattern analysis with consolidation recommendations

**Generated by:** `python scripts/02_analyze_tags.py`

**Contains:**
- Similar tags (fuzzy matching results with similarity scores)
- Hierarchical relationships (detected parent-child tags)
- Co-occurrence patterns (tags frequently used together)
- Tag network metrics (centrality, clustering)
- Consolidation recommendations

**Intended audience:**
- Vocabulary developers: Make consolidation decisions
- Project PIs: Review subject taxonomy
- Data curators: Plan controlled vocabulary structure

**How to interpret:**
- **Similar tags section:** Review pairs with similarity ≥80% for potential merging
  - Consider: Are these true variants or distinct concepts?
  - Action: Merge in Zotero or keep separate with clear definitions
- **Hierarchies section:** Identify broader/narrower relationships for SKOS
  - Example: "Mining" (broader) → "Coal Mine" (narrower)
  - Action: Structure controlled vocabulary with skos:broader/narrower
- **Co-occurrence section:** Tags used together suggest related concepts
  - Example: "Mining" + "Katoomba" = geographic association
  - Action: Consider creating compound terms or cross-references

**Typical review frequency:** After major tagging milestones, before vocabulary publication

---

### data_quality_issues.md

**Purpose:** Flagged items requiring manual review and curation

**Generated by:** `python scripts/02_analyze_tags.py`

**Contains:**
- Potential duplicates (items with identical/similar titles)
- Non-primary sources (reference works to exclude from analysis)
- Items with multiple attachments (may combine distinct sources)
- Items without attachments (missing PDFs)
- Summary statistics for each category

**Intended audience:**
- Data curators: Prioritise cleanup tasks
- Research assistants: Address flagged items
- Project managers: Track data quality metrics

**How to interpret:**
- **Duplicates:** Check if items are truly identical
  - Action: Merge duplicates in Zotero, preserve metadata
- **Non-primary sources:** Verify categorisation
  - Action: Move to separate collection or delete if not needed
- **Multiple attachments:** See multiple_attachments_inspection.md for details
  - Action: Review attachment patterns, split if needed
- **No attachments:** Identify missing sources
  - Action: Locate PDFs, upload to Zotero

**Priority levels:**
- HIGH: Duplicates, multiple attachments with distinct sources
- MEDIUM: Non-primary sources review, missing attachments
- LOW: Items with PDF + notes (likely legitimate)

**Typical review frequency:** Monthly during curation, before publication

---

### multiple_attachments_inspection.md

**Purpose:** Detailed inspection of items with multiple attachments, categorised by pattern

**Generated by:** `python scripts/03_inspect_multiple_attachments.py`

**Contains:**
- Categorised items (multiple PDFs, PDF+notes, multiple notes, mixed, uncertain)
- Priority levels (HIGH/MEDIUM/LOW)
- Attachment details (filenames, types, counts)
- Recommended actions for each item

**Intended audience:**
- Research assistants: Conduct manual review
- Project PIs: Make splitting decisions
- Data curators: Implement changes

**How to interpret:**
- **HIGH PRIORITY - Multiple PDFs:** Likely distinct articles combined
  - Action: Open PDFs, check if separate sources, split into individual items
- **LOW PRIORITY - PDF + Notes:** Likely text extraction from PDF
  - Action: Verify notes match PDF content, keep together
- **REVIEW - Multiple Notes:** May be sections that should be consolidated
  - Action: Check if notes should merge into single note
- **REVIEW - Mixed Content:** Unusual pattern needs investigation
  - Action: Manual inspection to understand attachment purpose

**Decision framework:**
- If attachments are different sources → Split into separate items
- If attachments are related materials (notes, images) → Keep together
- If uncertain → Consult with project team

**Typical review frequency:** As needed when quality_multiple_attachments.csv has entries

```

#### Section 4: Report Format

```markdown
## Report Format

### Markdown Structure

All reports use Markdown with consistent formatting:

- **Headings:** `#` for title, `##` for sections, `###` for subsections
- **Lists:** Bulleted for qualitative points, numbered for procedures
- **Tables:** Pipe-delimited for structured data
- **Code blocks:** For data examples, commands
- **Emphasis:** *Italic* for terms, **bold** for important notes

### Reading in Different Tools

**GitHub/GitLab:**
- Markdown renders automatically in web interface
- Tables, lists, and formatting display correctly

**VS Code:**
- Install Markdown Preview extension
- Right-click file → "Open Preview" (Ctrl+Shift+V)

**Command line:**
- Use `less reports/tag_summary.md` for basic reading
- Install `mdcat` or `glow` for formatted terminal rendering:
  ```bash
  # Debian/Ubuntu
  sudo apt install glow
  glow reports/tag_summary.md
  ```

**Convert to other formats:**
- **PDF:** Use pandoc:
  ```bash
  pandoc reports/tag_analysis.md -o tag_analysis.pdf
  ```
- **HTML:** Use pandoc or markdown-to-html tools
- **Word:** Open in Typora, export as .docx

### Generation Timestamps

All reports include generation timestamp at top:

```markdown
# Tag Analysis Report

**Generated:** 2025-10-09 10:45:00 AEDT
**Source Data:** data/raw_tags.json (generated 2025-10-09 10:30:00)
```

Check timestamps to ensure reports are current with latest data.
```

#### Section 5: Interpretation Guidelines

```markdown
## Interpretation Guidelines

### Statistical Significance

**Tag frequencies:**
- Tags used <3 times: Likely too specific or errors (review for deletion)
- Tags used 3-10 times: Specific topics (keep if relevant)
- Tags used >20 times: Core subjects (high priority for vocabulary)

**Similarity scores (0-100):**
- 95-100: Almost certainly variants (merge unless intentional distinction)
- 85-94: Likely variants (review for merging)
- 80-84: Possibly related (manual judgment required)
- <80: Not reported (dissimilar)

**Co-occurrence counts:**
- Count ≥10: Strong association (consider related terms)
- Count 5-9: Moderate association (review context)
- Count 3-4: Weak association (may be coincidental)
- Count <3: Not reported (insufficient evidence)

### Context Matters

Numbers alone don't tell the full story. Consider:

1. **Domain knowledge:** Do similar tags represent distinct concepts in mining history?
2. **User intent:** Were tags meant to be hierarchical or flat?
3. **Workflow stage:** Early tagging may be exploratory, later tagging more systematic
4. **Team coordination:** Are multiple researchers using different terminology?

### When in Doubt

- **Consult project team:** Schedule review meeting with historians and PIs
- **Check item examples:** Read actual item titles/content to understand tag usage
- **Document decisions:** Add notes to planning/ folder explaining vocabulary choices
- **Iterate:** Controlled vocabulary development is iterative, not one-time
```

#### Section 6: Action Workflows

```markdown
## Action Workflows

### After Reviewing tag_summary.md

1. **If many untagged items:**
   - Schedule tagging sessions
   - Assign items to research assistants
   - Consider AI-assisted tagging (Phase 2)

2. **If tag diversity is high:**
   - Proceed to 02_analyze_tags.py for consolidation analysis
   - Plan vocabulary development workshop

### After Reviewing tag_analysis.md

1. **Similar tags identified:**
   - Export similar_tags.csv to Excel
   - Review each pair, mark "merge" or "keep separate"
   - Apply merges in Zotero manually or via script
   - Rerun 01_extract_tags.py to verify

2. **Hierarchies detected:**
   - Map to SKOS broader/narrower relationships
   - Begin controlled vocabulary structure development
   - Document hierarchy decisions

3. **Co-occurrences noted:**
   - Identify cross-disciplinary tags (mining + environment, mining + gender)
   - Consider creating faceted vocabulary
   - Plan compound term creation if needed

### After Reviewing data_quality_issues.md

1. **Duplicates flagged:**
   - Open each pair in Zotero
   - Merge if truly duplicate
   - Keep separate if distinct items with similar titles
   - Document merges in planning/data-quality-log.md

2. **Non-primary sources flagged:**
   - Verify categorisation correct
   - Move to "Reference Materials" collection in Zotero
   - Exclude from primary source analysis

3. **Multiple attachments flagged:**
   - Run 03_inspect_multiple_attachments.py for detailed review
   - Follow multiple_attachments_inspection.md recommendations

4. **Missing attachments flagged:**
   - Cross-reference with archival sources (Trove, NLA)
   - Prioritise digitisation of high-value items
   - Upload PDFs to Zotero when located

### After Reviewing multiple_attachments_inspection.md

1. **HIGH PRIORITY items:**
   - Review immediately (likely distinct sources combined)
   - Split into separate Zotero items if needed
   - Preserve metadata (tags, notes) on appropriate split item

2. **REVIEW items:**
   - Schedule for next curation session
   - Document decision (split or keep together)

3. **LOW PRIORITY items:**
   - Spot-check a few to verify categorisation correct
   - Can defer detailed review
```

#### Section 7: See Also

```markdown
## See Also

- **data/README.md:** Data files that feed into these reports
- **scripts/README.md:** How to regenerate reports
- **CONTRIBUTING.md:** Report quality standards
- **planning/:** Decision logs and vocabulary development notes

---

## Questions?

- **Report unclear:** Open GitHub issue with specific questions
- **Recommendations uncertain:** Schedule team review meeting
- **Technical issues:** Check scripts/README.md troubleshooting section
```

---

## C4. planning/README.md

### Purpose

Provide an index of planning documents, explain their purpose, and document the project evolution and decision-making process.

### File Location

`/home/shawn/Code/blue-mountains/planning/README.md`

### Estimated Length

80-120 lines

### Required Content

```markdown
# Blue Mountains Planning Directory

This directory contains project planning documents that guide software development, FAIR4RS compliance implementation, and research workflows.

## Purpose

Planning documents serve multiple functions:

1. **Project roadmap:** Break down complex work into phases and tasks
2. **Decision documentation:** Record rationale for technical and methodological choices
3. **Knowledge transfer:** Enable new team members to understand project evolution
4. **FAIR compliance:** Document software development process (Reusable principle)

---

## Document Index

### Project Planning

| Document | Purpose | Status | Last Updated |
|----------|---------|--------|--------------|
| `project-plan.md` | Overall 6-phase project plan | Active | 2025-10-09 |
| `phase1-detailed.md` | Tag rationalisation phase breakdown | Active | 2025-10-09 |

### FAIR4RS Implementation Plans

| Document | Purpose | Status | Last Updated |
|----------|---------|--------|--------------|
| `FAIR4RS-documentation-plan.md` | Master FAIR4RS compliance plan (Phases A-E) | Active | 2025-10-09 |
| `FAIR4RS-phase-a-detailed.md` | Phase A: Metadata and compliance files | Completed | 2025-10-09 |
| `FAIR4RS-phase-b-detailed.md` | Phase B: Enhanced code documentation | Completed | 2025-10-09 |
| `FAIR4RS-phase-c-detailed.md` | Phase C: Folder-specific READMEs | In Progress | 2025-10-10 |

### Future Planning Documents

As the project progresses, additional planning documents may be added:

- `phase2-ai-tagging-plan.md` - LLM-assisted tagging implementation
- `phase3-location-data-plan.md` - Gazetteer integration approach
- `phase4-omeka-publication-plan.md` - Omeka Classic workflow
- `vocabulary-development-plan.md` - Controlled vocabulary structure decisions
- `data-quality-log.md` - Record of curation decisions and merges

---

## Document Purposes

### project-plan.md

**High-level overview of the 6-phase project:**

1. Tag Rationalisation & Vocabulary Publishing
2. AI-Assisted Tagging
3. Location Data Enhancement
4. Omeka Classic Publication
5. CurateScape Mobile Tours
6. Archaeological Integration

Provides strategic context for all technical decisions.

### phase1-detailed.md

**Operational breakdown of Phase 1 (current focus):**

- Tag extraction workflow
- Analysis procedures
- Quality assurance steps
- Vocabulary development approach
- RVA publishing preparation

### FAIR4RS-documentation-plan.md

**Master plan for achieving FAIR4RS compliance:**

Maps FAIR principles (Findable, Accessible, Interoperable, Reusable) to concrete implementation tasks across 5 phases:

- Phase A: Metadata files (CITATION.cff, codemeta.json, enhanced README)
- Phase B: Code documentation (docstrings, comments, educational explanations)
- Phase C: Folder READMEs (this phase)
- Phase D: API documentation and testing
- Phase E: Quality assurance and final validation

### FAIR4RS Phase Detail Plans

**Implementation guides for each FAIR4RS phase:**

Each phase detail plan includes:
- Overview and rationale
- Task breakdowns with deliverables
- File locations and content specifications
- Quality assurance procedures
- Acceptance criteria
- Estimated time and dependencies

These plans guide Claude Code-assisted implementation while documenting the development process for reproducibility.

---

## How Planning Documents Relate to Implementation

### Planning → Code

1. **Planning documents** (this directory) describe **what** to build and **why**
2. **Scripts** (scripts/ directory) implement the planned functionality
3. **Documentation** (README.md, docs/, CONTRIBUTING.md) explain **how** to use and maintain

### Iterative Refinement

Planning is not linear:

- Initial plans are detailed but may evolve as implementation reveals new insights
- Completed phases inform future phase planning
- Decision logs capture changes and rationale

### Version Control

All planning documents are tracked in Git to preserve project history:

```bash
# View planning document history
git log --follow planning/FAIR4RS-documentation-plan.md

# Compare versions
git diff HEAD~5 HEAD planning/project-plan.md
```

---

## Project Evolution

### Timeline

**October 2025:** FAIR4RS compliance implementation

- ✅ Phase A: Metadata files and main README (Oct 9)
- ✅ Phase B: Enhanced code documentation (Oct 10)
- ⏳ Phase C: Folder-specific READMEs (Oct 10, in progress)
- 📅 Phase D: API documentation (planned)
- 📅 Phase E: Quality assurance (planned)

### Major Decisions

Key methodological and technical decisions are documented in planning files:

1. **Folksonomy → Controlled Vocabulary approach** (project-plan.md)
   - Rationale: Leverage team's informal tagging work rather than starting from scratch
   - Method: Fuzzy matching, hierarchy detection, manual curation

2. **Separate API keys for read-only vs read-write** (FAIR4RS-phase-b-detailed.md)
   - Rationale: Principle of least privilege for security
   - Implementation: config.py supports dual-key strategy

3. **UK/Australian spelling throughout** (FAIR4RS-phase-b-detailed.md, CLAUDE.md)
   - Rationale: Project based in Australia, aligns with funding body and partner expectations
   - Implementation: Comprehensive spelling audit, custom aspell dictionary

4. **Three-tier README architecture** (FAIR4RS-phase-c-detailed.md)
   - Rationale: Balance discoverability (main README), technical depth (docs/), and contextual guidance (folder READMEs)
   - Implementation: Main README complete, docs/ complete, folder READMEs in progress

---

## Contributing to Planning

Planning documents are living resources. To propose changes:

1. **Open an issue:** Describe what aspect of planning needs revision and why
2. **Submit PR:** Modify planning document with clear rationale
3. **Discuss with team:** Major strategic changes require PI approval
4. **Update related docs:** Keep implementation docs in sync with planning

---

## See Also

- **Main README:** Project overview and getting started
- **CONTRIBUTING.md:** Code standards and contribution process
- **docs/:** Technical specifications (data formats, vocabularies)
- **scripts/README.md:** Script execution guide

---

## Questions?

- **Planning unclear:** Open GitHub issue for discussion
- **Want to contribute:** See CONTRIBUTING.md for process
- **Historical context:** Check git log for document evolution
```

---

## Implementation Order

**Recommended sequence:**

1. **scripts/README.md** (most immediately useful for users)
2. **data/README.md** (helps users understand outputs)
3. **reports/README.md** (guides interpretation of analysis)
4. **planning/README.md** (meta-documentation, less urgent)

---

## Quality Assurance

### Checklist for Each README

- [ ] Markdown linting passes (markdownlint-cli2)
- [ ] UK/Australian spelling throughout
- [ ] Cross-references accurate (no broken links to other docs)
- [ ] Examples tested and accurate
- [ ] Appropriate length (not too brief, not overwhelming)
- [ ] Clear section structure with logical flow
- [ ] Actionable guidance (not just description)

### Linting Command

```bash
# Check all folder READMEs
markdownlint scripts/README.md data/README.md reports/README.md planning/README.md

# Fix common issues automatically (if tool supports)
markdownlint --fix scripts/README.md
```

### Cross-Reference Validation

Verify all links point to existing files/sections:

```bash
# Extract links from README
grep -o '\[.*\](.*\.md)' scripts/README.md

# Check if target files exist
ls -l CONTRIBUTING.md docs/data-formats.md  # etc.
```

---

## Success Criteria

Phase C is complete when:

- [ ] All four folder READMEs created
- [ ] Each README follows the detailed specifications above
- [ ] All READMEs pass markdownlint validation
- [ ] Cross-references between READMEs and main documentation are accurate
- [ ] UK/Australian spelling verified throughout
- [ ] Examples tested and working
- [ ] Clear, actionable guidance provided for target audiences
- [ ] Git commit includes all four files with descriptive message

---

## Estimated Implementation Time

- **scripts/README.md:** 30-40 minutes
- **data/README.md:** 40-50 minutes (most content, complex schemas)
- **reports/README.md:** 25-35 minutes
- **planning/README.md:** 20-30 minutes

**Total:** 1.5-2 hours for comprehensive implementation

---

**Status:** Ready for implementation
**Dependencies:** Phase A and Phase B complete (verified 2025-10-10)
**Last Updated:** 2025-10-10
