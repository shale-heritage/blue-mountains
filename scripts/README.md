# Blue Mountains Scripts Directory

This directory contains Python scripts for processing Zotero library data, analysing tags, and preparing controlled vocabularies for publication.

## Workflow Overview

Scripts execute in sequence to transform folksonomy tags into FAIR-compliant controlled vocabularies:

1. **01_extract_tags.py** - Extract tags from Zotero API
2. **02_analyze_tags.py** - Analyse similarity, hierarchies, co-occurrence, quality
3. **03_inspect_multiple_attachments.py** - Detailed quality inspection

Each script reads from Zotero API and/or previous script outputs, generates data files (data/), and produces reports (reports/).

## Script Reference Table

| Script | Purpose | Inputs | Outputs | Runtime | Dependencies |
|--------|---------|--------|---------|---------|--------------|
| `config.py` | Configuration management | `.env` file | Configuration constants | Immediate | python-dotenv, pathlib |
| `01_extract_tags.py` | Extract tags from Zotero | Zotero API | `raw_tags.json`, `tag_frequency.csv`, `tag_summary.md` | 2-5 min | config.py, pyzotero, pandas |
| `02_analyze_tags.py` | Analyse tag patterns | `raw_tags.json`, Zotero API | `similar_tags.csv`, `tag_hierarchies.csv`, `tag_network.json`, `quality_*.csv`, reports | 5-10 min | config.py, fuzzywuzzy, networkx, matplotlib |
| `03_inspect_multiple_attachments.py` | Inspect attachment patterns | `quality_multiple_attachments.csv`, Zotero API | `multiple_attachments_inspection.md`, `multiple_attachments_details.json` | 1-3 min | config.py, pyzotero |

**Notes:**

- Runtime estimates based on ~1,200 item library
- All scripts require .env configuration
- Network connection required for Zotero API access
- Scripts must run in order (02 depends on 01 outputs)

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

Visit <https://www.zotero.org/settings/keys>

1. **Read-Only Key** (for scripts 01-03):
   - Name: "Blue Mountains - Read Only"
   - Permissions: "Allow library access" → Read Only
   - Select: Blue Mountains group library (2258643)

2. **Read-Write Key** (for future scripts):
   - Name: "Blue Mountains - Read Write"
   - Permissions: "Allow library access" → Read/Write
   - Select: Blue Mountains group library (2258643)

### Security Reminder

⚠️ **NEVER commit .env to Git** - This file contains secret API keys and is listed in .gitignore. If accidentally committed, regenerate keys immediately at <https://www.zotero.org/settings/keys>

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
2. Verify API key is valid: <https://www.zotero.org/settings/keys>
3. Check Zotero status: <https://status.zotero.org/>
4. Wait 5 minutes and retry (temporary API issues)

---

### Error: "HTTPError 403: Forbidden"

**Cause:** API key lacks required permissions or is invalid

**Solutions:**

1. Regenerate API key at <https://www.zotero.org/settings/keys>
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
2. On Windows, may need Microsoft C++ Build Tools: <https://visualstudio.microsoft.com/visual-cpp-build-tools/>
3. Rerun Script 02 to see performance improvement

---

### Scripts Run But No Visualisations Generated

**Cause:** Matplotlib backend issue or missing display

**Solutions:**

1. Check if PNG files exist: `ls -lh visualizations/`
2. If missing, check matplotlib backend: `python -c "import matplotlib; print(matplotlib.get_backend())"`
3. On headless servers, ensure non-interactive backend: Add to script: `matplotlib.use('Agg')`
4. Already configured in scripts, but verify matplotlib installation: `pip install --upgrade matplotlib`

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

## See Also

- **Main README:** Project overview, installation, usage examples
- **CONTRIBUTING.md:** Code standards, documentation requirements, contribution workflow
- **docs/data-formats.md:** JSON schema specifications, CSV column definitions
- **data/README.md:** Data dictionary and file format quick reference
- **reports/README.md:** Report interpretation guide

---

## Questions or Issues?

- **Script errors:** Check Troubleshooting section above
- **Zotero API issues:** <https://forums.zotero.org/>
- **Project questions:** Open issue on GitHub or email project team
- **Contributing:** See CONTRIBUTING.md for code standards and pull request process
