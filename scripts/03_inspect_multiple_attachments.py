#!/usr/bin/env python3
"""
Script 03: Inspect Items with Multiple Attachments for Quality Control

Research Context:
This script implements Phase 3 of data quality control for the Blue Mountains
shale mining communities digital collection. Following the quality analysis in
Script 02, this script provides deep inspection of items flagged as having
multiple attachments.

The goal is to identify items where multiple distinct primary sources have been
incorrectly combined into a single Zotero entry. This is a common data entry
error that occurs when:
1. Research assistants encounter multiple articles from the same newspaper issue
2. Multi-page articles are scanned as separate images
3. Supplementary materials (transcriptions, notes) are attached to items

Distinguishing these cases requires examining actual attachment details (filenames,
content types, notes) and providing curators with enough context to make informed
decisions about whether to split items or keep them consolidated.

Workflow Position:
This is the third of four planned scripts in the vocabulary development pipeline:

- Script 01 (COMPLETE): Extract raw tags from Zotero → raw_tags.json
- Script 02 (COMPLETE): Analyze tags and quality → similar_tags.csv, quality reports
- **Script 03 (THIS SCRIPT)**: Inspect multiple-attachment items → detailed inspection report
- Script 04 (PLANNED): Map tags to Getty AAT/TGN → controlled vocabulary for Research
  Vocabularies Australia (RVA)

This script depends on Script 02 having identified items with multiple attachments
and exported them to data/quality_multiple_attachments.csv. It fetches full details
for each flagged item (including all child attachments) and categorises them by
attachment pattern to prioritise manual review.

Technical Approach - Attachment Pattern Categorisation:
We categorise items based on the types and quantities of child items:

1. **multiple_pdfs** (HIGH PRIORITY):
   - Multiple Portable Document Format (PDF) files, no notes
   - Most likely to contain distinct sources that should be split
   - Example: Two newspaper articles from different dates incorrectly combined

2. **pdf_plus_notes** (LOW PRIORITY):
   - PDFs with accompanying notes
   - Usually indicates text extraction (research assistant transcribed PDF content)
   - Legitimate structure - text extraction aids searchability and accessibility

3. **multiple_notes** (MEDIUM PRIORITY):
   - Multiple notes, no PDFs
   - May be transcribed text sections that could be consolidated
   - Less urgent than multiple PDFs

4. **mixed_content** (MEDIUM PRIORITY):
   - Various attachment types (PDFs, notes, linked files, etc.)
   - Needs case-by-case review to understand attachment purposes

5. **uncertain** (MEDIUM PRIORITY):
   - Pattern doesn't match known categories
   - Requires manual inspection to understand structure

This categorisation is heuristic (rule-based pattern matching) rather than
algorithmic analysis. It provides a starting point for human review, not
definitive classification. Domain experts (project historians) must make
final decisions based on attachment content.

Why Manual Review is Required:
Automated splitting is too risky for scholarly research collections:

1. **Context Loss**: Multiple PDFs might be pages of one article, not separate articles
2. **Relationship Preservation**: Supplementary materials may need to stay with primary source
3. **Citation Integrity**: Incorrect splitting affects citations and provenance
4. **Domain Knowledge**: Historians can assess content relevance; algorithms cannot

Our approach: Surface patterns, provide context, let experts decide.

Alternative Approaches Considered:
1. **Optical Character Recognition (OCR) + Natural Language Processing (NLP)**:
   Extract text from PDFs, detect article boundaries automatically
   Rejected: High complexity, error-prone, still requires validation
2. **Filename pattern analysis**:
   Parse filenames for dates, page numbers, article markers
   Rejected: Filename conventions inconsistent across collection
3. **Automated splitting**:
   Automatically separate all items with multiple PDFs
   Rejected: Too risky - would create incorrect splits, lose relationships

FAIR Principles Implementation:
This script supports Findable, Accessible, Interoperable, Reusable (FAIR) principles:

**Findable:**
- Report includes Zotero item keys for direct lookup
- Items are categorised by priority for efficient curation workflow
- JSON export preserves complete item metadata for future reference

**Accessible:**
- Report in Markdown (readable as text, beautiful in rendered view)
- Clear explanations of each category with action recommendations
- Direct links to Zotero web interface for item inspection

**Interoperable:**
- JSON export uses standard format for programmatic access
- Comma-Separated Values (CSV) input from Script 02 enables spreadsheet workflow
- Compatible with Zotero Application Programming Interface (API) for automation

**Reusable:**
- Categorisation logic is modular (categorise_attachment_pattern function)
- Heuristics are documented and can be refined based on review outcomes
- Report template can be adapted for other quality control tasks

Security Model:
This script uses read-only Zotero API key (config.ZOTERO_API_KEY_READONLY)
following the principle of least privilege. The script only reads item and
attachment metadata - it never modifies the Zotero library, downloads files,
or writes data back to Zotero. All changes (item splitting, consolidation)
must be performed manually by curators in the Zotero interface.

Performance Considerations:
For each flagged item, we make two API requests:
1. zot.item(key) - Fetch parent item metadata
2. zot.children(key) - Fetch all child items (attachments, notes)

For 303 flagged items (from Script 02), this means 606 HyperText Transfer
Protocol (HTTP) requests. With network latency, this takes 5-10 minutes.

To improve performance:
- Progress indicators show processing status every 50 items
- Errors on individual items are logged but don't stop entire process
- Results are saved incrementally (if script crashes, restart from CSV)

For very large datasets (>1000 items), consider:
- Batch API requests (Zotero API supports some batch operations)
- Parallel processing (multiple threads fetching items concurrently)
- Caching (save fetched items to avoid re-fetching on script re-run)

Output Files Generated:
1. **reports/multiple_attachments_inspection.md**:
   Human-readable report organised by priority
   - HIGH PRIORITY section: Multiple PDFs (detailed listings)
   - Other sections: Summaries with sample items
   - Action recommendations for each category

2. **data/multiple_attachments_details.json**:
   Complete item metadata and attachment details
   - Includes all fetched data for programmatic access
   - Can be used by other scripts or imported to analysis tools
   - Preserves raw data for future re-categorisation if heuristics change

Dependencies:
- json, sys, pathlib, datetime: Python standard library
- pandas: Load CSV input from Script 02
- pyzotero: Fetch item and attachment details from Zotero Web API
- config: Project configuration module (loads .env credentials and paths)

Installation:
  pip install pandas pyzotero

Usage:
  # Ensure Script 02 has been run first to generate quality_multiple_attachments.csv
  python scripts/03_inspect_multiple_attachments.py

  # Review outputs:
  - Read reports/multiple_attachments_inspection.md (start with HIGH PRIORITY section)
  - For each HIGH PRIORITY item, open in Zotero web interface to view attachments
  - Decide if items need splitting (document decisions for batch processing)
  - Use data/multiple_attachments_details.json for detailed reference if needed

Curation Workflow After Running This Script:
1. Review HIGH PRIORITY section in Markdown report
2. For each item, open in Zotero web interface:
   https://www.zotero.org/groups/2258643/items/ITEM_KEY
3. Examine each PDF attachment to determine if distinct sources
4. Document splitting decisions (create a curation log)
5. Perform item splitting in batches (Zotero interface or API)
6. Re-run Script 02 to verify quality improvements
7. Re-run this script to check for any remaining issues

Author: Shawn Ross
Project: Australian Research Council (ARC) Linkage Project LP190100900
         Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
from pyzotero import zotero

# Add parent directory to path for imports
# This allows importing config.py when running from project root or scripts/ directory
# __file__ = /path/to/blue-mountains/scripts/03_inspect_multiple_attachments.py
# __file__.parent = /path/to/blue-mountains/scripts/
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def load_flagged_items():
    """
    Load list of items with multiple attachments from Script 02 output.

    This function reads the CSV file generated by Script 02's quality analysis,
    which contains items flagged as having >1 child item (attachments, notes).

    CSV Structure Expected:
    The quality_multiple_attachments.csv file has these columns:
    - key: Zotero item key (8-character identifier)
    - title: Item title
    - num_attachments: Number of child items

    This script depends on Script 02 having been run successfully. If the CSV
    file doesn't exist, pandas raises FileNotFoundError with helpful message.

    Why Load from CSV Instead of Re-querying Zotero:
    We could fetch all items from Zotero and re-check for multiple attachments,
    but loading from CSV is:
    1. Faster (no API calls required)
    2. Reproducible (same input for testing/debugging)
    3. Consistent with Script 02 results (no library changes between runs)

    This follows the workflow design principle: each script consumes outputs
    from previous scripts rather than re-computing everything from scratch.

    Returns:
        pandas.DataFrame: DataFrame with columns [key, title, num_attachments]
            Each row represents one item flagged for inspection

    Side Effects:
        Reads data/quality_multiple_attachments.csv file

    Error Handling:
        If file doesn't exist, pandas raises FileNotFoundError
        If CSV is malformed, pandas raises parsing error
        Both errors are caught by main() and reported with full traceback

    Example:
        df = load_flagged_items()
        print(f"Found {len(df)} items with multiple attachments")
        for idx, row in df.iterrows():
            print(f"Item {row['key']}: {row['title']} ({row['num_attachments']} attachments)")

    See Also:
        Script 02 (02_analyze_tags.py): Generates the input CSV file
    """
    # Print progress message (reassures user script is running)
    print("Loading flagged items from quality analysis...")

    # Construct path to CSV file using config.DATA_DIR
    # This ensures we look in the correct directory regardless of where script is run from
    csv_file = config.DATA_DIR / 'quality_multiple_attachments.csv'

    # Load CSV into pandas DataFrame
    # pandas automatically handles:
    # - Header row parsing (first row becomes column names)
    # - Data type inference (strings for key/title, int for num_attachments)
    # - Encoding detection (handles UTF-8 international characters)
    df = pd.read_csv(csv_file)

    # Confirm successful load with count
    # This helps users verify they're inspecting the expected number of items
    print(f"✓ Loaded {len(df)} items with multiple attachments")

    return df


def fetch_item_details(zot, item_key):
    """
    Fetch complete item details including all child attachments from Zotero.

    This function makes two API calls to retrieve:
    1. Parent item metadata (title, type, date, tags, etc.)
    2. All child items (attachments, notes)

    We need full details because the quality analysis CSV only contains item
    keys and counts. To categorise attachment patterns, we need to know:
    - How many PDFs vs notes vs other attachment types
    - Attachment filenames and content types
    - Whether notes contain transcribed text

    Zotero Data Model - Parent/Child Relationships:
    Zotero organises items hierarchically:
    - **Parent items**: Top-level entries (newspaper articles, reports, books)
    - **Child items**: Attachments and notes belonging to parent
      - Attachments: PDF files, images, linked files, web snapshots
      - Notes: Rich text notes with transcriptions, annotations, etc.

    Each parent can have 0-N children. Children cannot have their own children
    (no nested hierarchies beyond one level).

    API Request Details:
    1. zot.item(key): Returns full item object with metadata
       Response includes item['data'] (metadata fields) and item['meta'] (Zotero metadata)
    2. zot.children(key): Returns list of all child items
       Each child has same structure as parent (data, meta fields)

    Network Performance:
    Each function call makes 2 HTTP requests. For 303 items, that's 606 requests.
    At ~1 request per second (network latency), this takes ~10 minutes total.

    We could optimise with batch requests, but:
    - Zotero API has limited batch support for item+children retrieval
    - Individual requests are simpler and more reliable
    - 10 minutes is acceptable for a quality control task

    Error Handling:
    If API request fails (network error, invalid key, permission denied), we:
    - Print warning with item key and error message
    - Return None (caller filters out None values later)
    - Continue processing other items (one failure doesn't stop entire script)

    This is defensive error handling appropriate for quality control workflow.

    Args:
        zot: Authenticated pyzotero.Zotero instance (from config.ZOTERO_API_KEY_READONLY)
        item_key (str): Zotero item key (8-character identifier like "ABCD1234")

    Returns:
        dict or None: Dictionary with item metadata and children, or None if error
            {
                'key': str,                    # Item key
                'title': str,                  # Item title
                'itemType': str,               # Type (newspaperArticle, report, etc.)
                'date': str,                   # Publication date
                'publicationTitle': str,       # Newspaper/journal name
                'pages': str,                  # Page numbers
                'url': str,                    # URL if applicable
                'tags': [str, ...],            # List of tag names
                'num_children': int,           # Count of child items
                'children': [                  # List of child details
                    {
                        'key': str,            # Child key
                        'itemType': str,       # attachment, note
                        'title': str,          # Child title
                        'filename': str,       # Filename for attachments
                        'contentType': str,    # MIME type (application/pdf, etc.)
                        'linkMode': str,       # Storage mode
                        'note': str            # Note content (if note item)
                    },
                    ...
                ]
            }

    Example:
        zot = zotero.Zotero(config.ZOTERO_GROUP_ID, config.ZOTERO_LIBRARY_TYPE,
                           config.ZOTERO_API_KEY_READONLY)
        item_info = fetch_item_details(zot, "ABCD1234")
        if item_info:
            print(f"Item: {item_info['title']}")
            print(f"Children: {item_info['num_children']}")
            for child in item_info['children']:
                print(f"  - {child['itemType']}: {child['filename'] or child['title']}")

    See Also:
        - Zotero API documentation: https://www.zotero.org/support/dev/web_api/v3/basics
        - pyzotero documentation: https://pyzotero.readthedocs.io/
    """
    # Wrap API calls in try/except to handle network errors gracefully
    try:
        # API Call 1: Fetch parent item metadata
        # zot.item() returns full item object including all metadata fields
        # This is a synchronous call that blocks until response received
        item = zot.item(item_key)

        # API Call 2: Fetch all children (attachments, notes)
        # zot.children() returns list of child items for this parent
        # Returns empty list if no children (not an error)
        children = zot.children(item_key)

        # Extract relevant information from parent item
        # We select a subset of fields that are useful for categorisation
        # Using .get() with default values ensures script doesn't crash on missing fields
        item_info = {
            # Item identification
            'key': item_key,
            'title': item['data'].get('title', '[No Title]'),
            'itemType': item['data'].get('itemType', 'unknown'),

            # Publication metadata (helps identify articles)
            'date': item['data'].get('date', ''),
            'publicationTitle': item['data'].get('publicationTitle', ''),
            'pages': item['data'].get('pages', ''),

            # Additional fields
            'url': item['data'].get('url', ''),

            # Tags (list comprehension extracts tag names from tag objects)
            # Zotero stores tags as [{'tag': 'name'}, {'tag': 'name2'}]
            # We extract just the names: ['name', 'name2']
            'tags': [tag['tag'] for tag in item['data'].get('tags', [])],

            # Children count (calculated from fetched children list)
            'num_children': len(children),

            # Children details (populated in loop below)
            'children': []
        }

        # Process each child item to extract relevant details
        for child in children:
            # Access child metadata
            child_data = child['data']

            # Extract relevant child information
            child_info = {
                # Child identification
                'key': child['key'],
                'itemType': child_data.get('itemType', 'unknown'),  # attachment, note
                'title': child_data.get('title', '[No Title]'),

                # Attachment-specific fields
                # Only populated for attachment items, empty for notes
                'filename': child_data.get('filename', ''),          # Original filename
                'contentType': child_data.get('contentType', ''),    # MIME type (application/pdf, image/png)  # noqa: E501
                'linkMode': child_data.get('linkMode', ''),          # imported_file, linked_file, imported_url  # noqa: E501

                # Note-specific field
                # Only extract note content if this is a note item
                # Notes contain rich text (HTML) with transcriptions, annotations
                # We include this to help curators understand note purposes
                'note': child_data.get('note', '') if child_data.get('itemType') == 'note' else ''
            }

            # Add this child to parent's children list
            item_info['children'].append(child_info)

        # Return successfully fetched item info
        return item_info

    except Exception as e:
        # Catch any error (network error, invalid key, permission denied, etc.)
        # Print warning with item key and error message for debugging
        print(f"  ⚠️  Error fetching item {item_key}: {e}")

        # Return None to indicate failure
        # Caller will filter out None values when generating report
        return None


def categorise_attachment_pattern(item_info):
    """
    Analyse attachment pattern to categorise item for prioritised review.

    This function implements heuristic rules to classify items based on the
    types and quantities of child attachments. The goal is to identify patterns
    that suggest items may need splitting (HIGH PRIORITY) vs patterns that are
    typically legitimate (LOW PRIORITY).

    Categorisation Algorithm - Rule-Based Heuristics:

    **Rule 1: Multiple PDFs (HIGH PRIORITY)**
    If item has 2+ PDF attachments and no notes:
    - Category: 'multiple_pdfs'
    - Reasoning: Multiple PDFs with no accompanying text extraction suggests
      distinct sources incorrectly combined
    - Action: HIGH PRIORITY review to determine if PDFs are:
      (a) Pages of same article (legitimate) or
      (b) Separate articles (need splitting)

    **Rule 2: PDFs with Notes (LOW PRIORITY)**
    If item has 1+ PDFs and 1+ notes:
    - Category: 'pdf_plus_notes'
    - Reasoning: Notes typically indicate text extraction by research assistants
      This is legitimate structure - notes aid searchability and accessibility
    - Action: LOW PRIORITY - spot-check a few to validate categorisation

    **Rule 3: Multiple Notes, No PDFs (MEDIUM PRIORITY)**
    If item has 2+ notes and no PDFs:
    - Category: 'multiple_notes'
    - Reasoning: Multiple notes might be transcribed text sections that could
      be consolidated for easier reading
    - Action: MEDIUM PRIORITY - review if notes should be combined

    **Rule 4: Mixed Attachment Types (MEDIUM PRIORITY)**
    If item has more total attachments than PDFs+notes:
    - Category: 'mixed_content'
    - Reasoning: Has other attachment types (images, web snapshots, linked files)
      Needs case-by-case review to understand attachment purposes
    - Action: MEDIUM PRIORITY - individual inspection required

    **Rule 5: Uncertain (MEDIUM PRIORITY)**
    If pattern doesn't match any of the above:
    - Category: 'uncertain'
    - Reasoning: Attachment pattern is unusual or ambiguous
    - Action: MEDIUM PRIORITY - manual inspection required

    Why Heuristics Instead of Machine Learning:
    We use rule-based heuristics rather than trained models because:
    1. Small dataset (303 items) - insufficient for ML training
    2. Clear patterns - rules capture most cases accurately
    3. Interpretability - curators can understand and validate rules
    4. Maintainability - rules can be refined based on review outcomes

    If dataset grows significantly (>10,000 items) and patterns become complex,
    consider ML approaches:
    - Train classifier on manually-reviewed examples
    - Features: attachment counts, filename patterns, content types
    - Model: Decision tree, random forest, or gradient boosting

    Limitations:
    These heuristics have false positives and false negatives:
    - **False Positive**: Item categorised as 'multiple_pdfs' (HIGH PRIORITY)
      but PDFs are actually pages of one article
    - **False Negative**: Item categorised as 'pdf_plus_notes' (LOW PRIORITY)
      but PDFs are actually distinct sources

    This is acceptable because:
    1. All categories require human review (we're prioritising, not deciding)
    2. HIGH PRIORITY items get thorough review (catches false positives)
    3. Sample items from other categories get spot-checked (catches false negatives)

    Args:
        item_info (dict): Item details from fetch_item_details()
            Must contain 'children' list with child metadata

    Returns:
        tuple: (category, reasoning, action)
            - category (str): One of the category codes
              ('multiple_pdfs', 'pdf_plus_notes', 'multiple_notes',
               'mixed_content', 'uncertain')
            - reasoning (str): Human-readable explanation of categorisation
              Describes what pattern was detected and what it might indicate
            - action (str): Priority level and recommended action
              Guides curator workflow (what to review first)

    Example:
        item_info = fetch_item_details(zot, "ABCD1234")
        category, reasoning, action = categorise_attachment_pattern(item_info)
        print(f"Category: {category}")
        print(f"Reasoning: {reasoning}")
        print(f"Action: {action}")

    Output Example:
        Category: multiple_pdfs
        Reasoning: Has 3 PDF files with no notes. May be distinct sources combined.
        Action: HIGH PRIORITY - Review if these are separate articles

    See Also:
        generate_inspection_report(): Uses these categories to organise report sections
    """
    # Extract children list from item info
    children = item_info['children']

    # Filter children by type using list comprehensions
    # This separates PDFs, notes, and other attachments for counting

    # PDFs: Filter for attachment items with PDF content type
    # contentType = 'application/pdf' is standard MIME type for PDFs
    pdfs = [c for c in children if c['contentType'] == 'application/pdf']

    # Notes: Filter for note items
    # itemType = 'note' identifies rich text note items
    notes = [c for c in children if c['itemType'] == 'note']

    # All attachments: Filter for attachment items (excludes notes)
    # itemType = 'attachment' includes PDFs, images, web snapshots, linked files
    attachments = [c for c in children if c['itemType'] == 'attachment']

    # Count each type for rule evaluation
    num_pdfs = len(pdfs)
    num_notes = len(notes)
    num_attachments = len(attachments)

    # Apply categorisation rules in priority order
    # Rules are ordered by specificity (most specific first)

    # Rule 1: Multiple PDFs without notes - HIGHEST PRIORITY
    if num_pdfs >= 2 and num_notes == 0:
        # This pattern suggests multiple distinct sources
        # No notes = no text extraction = research assistant likely combined sources
        category = 'multiple_pdfs'
        reasoning = f"Has {num_pdfs} PDF files with no notes. May be distinct sources combined."
        action = "HIGH PRIORITY - Review if these are separate articles"

    # Rule 2: PDFs with notes - LOWEST PRIORITY
    elif num_pdfs >= 1 and num_notes >= 1:
        # This pattern suggests text extraction workflow
        # Research assistant scanned PDF then transcribed content to note
        # This is legitimate structure that aids searchability
        category = 'pdf_plus_notes'
        reasoning = f"Has {num_pdfs} PDF(s) and {num_notes} note(s). Likely text extraction."
        action = "LOW PRIORITY - Probably legitimate structure"

    # Rule 3: Multiple notes without PDFs - MEDIUM PRIORITY
    elif num_pdfs == 0 and num_notes >= 2:
        # This pattern suggests transcribed text sections
        # Multiple notes might be easier to use if consolidated into one note
        # Less urgent than multiple PDFs (no risk of combined sources)
        category = 'multiple_notes'
        reasoning = f"Has {num_notes} notes with no PDFs. May be transcribed text sections."
        action = "REVIEW - Check if notes should be consolidated"

    # Rule 4: Mixed attachment types - MEDIUM PRIORITY
    elif num_attachments > num_pdfs + num_notes:
        # This pattern indicates other attachment types present
        # Could be images, web snapshots, linked files, etc.
        # Needs individual review to understand each attachment's purpose
        category = 'mixed_content'
        reasoning = f"Has mixed attachment types: {num_attachments} total attachments."
        action = "REVIEW - Check attachment types and purposes"

    # Rule 5: Uncertain pattern - MEDIUM PRIORITY
    else:
        # Pattern doesn't match any of the above rules
        # This is the catch-all category for unusual cases
        category = 'uncertain'
        reasoning = "Pattern unclear from metadata alone."
        action = "REVIEW - Manual inspection required"

    # Return tuple with categorisation results
    return category, reasoning, action


def generate_inspection_report(items_details):
    """
    Generate detailed Markdown report for manual review of multiple-attachment items.

    This function creates a comprehensive, human-readable report organised by
    priority level. The report helps curators efficiently review items by:
    1. Grouping items into categories based on attachment patterns
    2. Prioritising HIGH PRIORITY items (most likely to need splitting)
    3. Providing detailed information for top-priority items
    4. Summarising lower-priority categories
    5. Including direct links to Zotero web interface for item inspection

    Report Structure:

    **Overview Section**:
    - Total items inspected
    - Purpose of inspection (identify items needing splitting)

    **Summary Table**:
    - Counts for each category
    - Priority levels (HIGH/MEDIUM/LOW)
    - Brief descriptions

    **Section 1: HIGH PRIORITY - Multiple PDFs**:
    - Detailed listings for first 20 items
    - Each item shows: title, key, metadata, all attachments, action required
    - These are most likely to contain distinct sources that need splitting

    **Sections 2-5: Other Categories**:
    - Summary counts
    - Sample items (first 5-10)
    - Brief descriptions
    - Less detail than HIGH PRIORITY section (can investigate if needed)

    **Next Steps Section**:
    - Workflow guidance for curators
    - Links to Zotero web interface format
    - Documentation recommendations

    Markdown Format Benefits:
    Same benefits as previous report functions - readable as text, beautiful
    when rendered, version controllable, platform independent.

    Categorisation Process:
    For each item:
    1. Call categorise_attachment_pattern() to classify
    2. Add category, reasoning, and action to item dict
    3. Append to appropriate category list

    This prepares data for report sections organised by category.

    Args:
        items_details (list): List of item detail dicts from fetch_item_details()
            May contain None values (items that failed to fetch)

    Returns:
        dict: Dictionary mapping category names to lists of categorised items
            {
                'multiple_pdfs': [item1, item2, ...],
                'pdf_plus_notes': [item3, item4, ...],
                ...
            }
        This is returned so main() can print summary statistics.

    Side Effects:
        Writes reports/multiple_attachments_inspection.md file

    Report Organisation Philosophy:
    We organise by priority (not alphabetically or by item key) because:
    1. Curators have limited time - focus on highest-risk items first
    2. HIGH PRIORITY items are most likely to need action
    3. Lower-priority items can be spot-checked rather than exhaustively reviewed

    This prioritised workflow maximises curation efficiency.

    Example Report Section:
        ### 1. "Katoomba Shale Mine Closure"

        **Item Key:** `ABCD1234`
        **Type:** newspaperArticle
        **Date:** 1927-08-15
        **Publication:** Blue Mountains Echo
        **Tags:** Katoomba, shale mines, closure

        **Attachments (3):**

        1. **attachment:** article_1927_08_15_page1.pdf
           - Content Type: application/pdf
        2. **attachment:** article_1927_08_15_page2.pdf
           - Content Type: application/pdf
        3. **attachment:** article_1927_08_20_closure.pdf
           - Content Type: application/pdf

        **Action Required:** HIGH PRIORITY - Review if these are separate articles
        **Reasoning:** Has 3 PDF files with no notes. May be distinct sources combined.

    See Also:
        categorise_attachment_pattern(): Performs the categorisation
        save_details_json(): Exports complete data for reference
    """
    # Construct output file path
    output_file = config.REPORTS_DIR / 'multiple_attachments_inspection.md'
    print(f"\nGenerating inspection report at {output_file}...")

    # Initialise category dictionaries
    # Each category maps to a list of items in that category
    categorised = {
        'multiple_pdfs': [],      # HIGH PRIORITY - multiple PDFs without notes
        'pdf_plus_notes': [],     # LOW PRIORITY - PDFs with text extraction notes
        'multiple_notes': [],     # MEDIUM - multiple notes without PDFs
        'mixed_content': [],      # MEDIUM - various attachment types
        'uncertain': []           # MEDIUM - unclear pattern
    }

    # Categorise all items
    # Iterate through all fetched items and classify each one
    for item in items_details:
        # Skip None values (items that failed to fetch due to API errors)
        if item:
            # Categorise this item using heuristic rules
            category, reasoning, action = categorise_attachment_pattern(item)

            # Add categorisation results to item dict
            # This augments the item with categorisation metadata
            item['category'] = category
            item['reasoning'] = reasoning
            item['action'] = action

            # Add item to appropriate category list
            categorised[category].append(item)

    # Build report as multi-line string
    # Using f-string for embedded expressions
    report = f"""# Multiple Attachments Inspection Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overview

This report examines items with multiple attachments to identify:
- Items that may contain multiple distinct primary sources (need splitting)
- Items with legitimate multi-page or supplementary attachments (OK as-is)

**Total items inspected:** {len([i for i in items_details if i])}

---

## Summary by Category

| Category | Count | Priority | Description |
|----------|-------|----------|-------------|
| Multiple PDFs | {len(categorised['multiple_pdfs'])} | **HIGH** | Multiple PDF files - may be distinct sources |  # noqa: E501
| PDF + Notes | {len(categorised['pdf_plus_notes'])} | LOW | PDFs with text extraction notes |
| Multiple Notes | {len(categorised['multiple_notes'])} | MEDIUM | Multiple notes without PDFs |
| Mixed Content | {len(categorised['mixed_content'])} | MEDIUM | Various attachment types |
| Uncertain | {len(categorised['uncertain'])} | MEDIUM | Requires manual inspection |

---

## 1. HIGH PRIORITY: Multiple PDFs (Potential Split Candidates)

These items have multiple PDF attachments and may contain distinct primary sources
that should be separated into individual Zotero entries.

**Count:** {len(categorised['multiple_pdfs'])}

"""

    # Section 1: HIGH PRIORITY - Multiple PDFs
    # Show detailed information for first 20 items
    # These are most important to review, so we provide complete details
    if categorised['multiple_pdfs']:
        # Iterate through first 20 items in this category
        for idx, item in enumerate(categorised['multiple_pdfs'][:20], 1):
            # Item header with title
            report += f"""### {idx}. "{item['title']}"

**Item Key:** `{item['key']}`
**Type:** {item['itemType']}
**Date:** {item['date']}
**Publication:** {item['publicationTitle']}
**Tags:** {', '.join(item['tags']) if item['tags'] else 'None'}

**Attachments ({len(item['children'])}):**

"""
            # List each attachment with details
            # Numbered list helps curators refer to specific attachments
            for child_idx, child in enumerate(item['children'], 1):
                # Show attachment type and filename/title
                report += f"{child_idx}. **{child['itemType']}:** {child['filename'] or child['title']}\n"  # noqa: E501

                # Show content type if present (helps identify PDFs vs images vs other)
                if child['contentType']:
                    report += f"   - Content Type: {child['contentType']}\n"

            # Show action and reasoning for this item
            report += f"\n**Action Required:** {item['action']}\n"
            report += f"**Reasoning:** {item['reasoning']}\n\n"

            # Horizontal rule separates items visually
            report += "---\n\n"

        # If more than 20 items, note that full list is in JSON export
        if len(categorised['multiple_pdfs']) > 20:
            report += f"\n*Note: Showing first 20 of {len(categorised['multiple_pdfs'])} items. See JSON export for complete list.*\n\n"  # noqa: E501

    else:
        # No items in this category
        report += "*No items in this category.*\n\n"

    # Section 2: PDF + Notes (LOW PRIORITY)
    # Show summary only - these are typically legitimate structure
    report += """---

## 2. PDF + Notes (Likely Text Extraction)

These items have PDFs with accompanying notes, which typically indicates
text extraction. These are usually fine as-is.

"""

    report += f"**Count:** {len(categorised['pdf_plus_notes'])}\n\n"

    # Show sample items (first 5) for spot-checking
    if categorised['pdf_plus_notes']:
        report += "**Sample items (first 5):**\n\n"
        for idx, item in enumerate(categorised['pdf_plus_notes'][:5], 1):
            # Brief summary: title, key, attachment counts
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            # Count PDFs and notes separately
            report += f"   - {len([c for c in item['children'] if c['contentType'] == 'application/pdf'])} PDF(s), "  # noqa: E501
            report += f"{len([c for c in item['children'] if c['itemType'] == 'note'])} note(s)\n"
        report += "\n"

    # Section 3: Multiple Notes (MEDIUM PRIORITY)
    report += """---

## 3. Multiple Notes (Transcribed Sections)

These items have multiple notes but no PDFs. May be transcribed text that
should be consolidated.

"""

    report += f"**Count:** {len(categorised['multiple_notes'])}\n\n"

    # Show sample items (first 5)
    if categorised['multiple_notes']:
        report += "**Sample items (first 5):**\n\n"
        for idx, item in enumerate(categorised['multiple_notes'][:5], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len([c for c in item['children'] if c['itemType'] == 'note'])} note(s)\n"  # noqa: E501
        report += "\n"

    # Section 4: Mixed Content (MEDIUM PRIORITY)
    report += """---

## 4. Mixed Content

These items have various types of attachments and need individual review.

"""

    report += f"**Count:** {len(categorised['mixed_content'])}\n\n"

    # Show sample items (first 10)
    if categorised['mixed_content']:
        report += "**Items requiring review:**\n\n"
        for idx, item in enumerate(categorised['mixed_content'][:10], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len(item['children'])} attachments of various types\n"
        report += "\n"

    # Section 5: Uncertain Cases (MEDIUM PRIORITY)
    report += """---

## 5. Uncertain Cases

These items require manual inspection to determine appropriate action.

"""

    report += f"**Count:** {len(categorised['uncertain'])}\n\n"

    # Show sample items (first 10)
    if categorised['uncertain']:
        for idx, item in enumerate(categorised['uncertain'][:10], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len(item['children'])} attachments\n"
        report += "\n"

    # Next Steps Section
    # Provide workflow guidance for curators
    report += f"""---

## Next Steps

### Immediate Actions

1. **Review HIGH PRIORITY items** (Multiple PDFs section)
   - Open each item in Zotero web interface: `https://www.zotero.org/groups/{config.ZOTERO_GROUP_ID}/items/ITEM_KEY`  # noqa: E501
   - Check if PDFs are: (a) same article split across pages, or (b) distinct sources
   - If distinct sources, plan to split into separate entries

2. **Spot-check other categories** to validate categorisation

3. **Document splitting workflow** if items need to be separated

### Reference

- Full item details exported to: `data/multiple_attachments_details.json`
- Use Zotero item keys to locate items in the web interface
- Take notes on which items need splitting for batch processing

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    # Write report to file
    # UTF-8 encoding handles any international characters in titles
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Confirm save
    print("✓ Saved inspection report")

    # Return categorised items dict so main() can print summary
    return categorised


def save_details_json(items_details):
    """
    Save complete item details to JSON for programmatic access and reference.

    This function exports all fetched item metadata and attachment details to
    a JSON file. This serves multiple purposes:

    1. **Reference**: Curators can consult detailed data when reviewing items
    2. **Programmatic access**: Other scripts can load this data for analysis
    3. **Reproducibility**: Preserves exact data used to generate report
    4. **Re-categorisation**: If heuristics change, can re-run categorisation
       without re-fetching from Zotero API

    JSON Format:
    {
      "generated_at": "2025-10-09T14:30:00",
      "zotero_group_id": "2258643",
      "total_items": 303,
      "items": [
        {
          "key": "ABCD1234",
          "title": "Article Title",
          "itemType": "newspaperArticle",
          "date": "1927-08-15",
          "publicationTitle": "Blue Mountains Echo",
          "pages": "1-2",
          "url": "",
          "tags": ["Katoomba", "shale mines"],
          "num_children": 3,
          "children": [
            {
              "key": "EFGH5678",
              "itemType": "attachment",
              "title": "Article PDF",
              "filename": "article_1927_08_15.pdf",
              "contentType": "application/pdf",
              "linkMode": "imported_file",
              "note": ""
            },
            ...
          ],
          "category": "multiple_pdfs",
          "reasoning": "Has 3 PDF files with no notes...",
          "action": "HIGH PRIORITY - Review if these are separate articles"
        },
        ...
      ]
    }

    Why Include Categorisation Results:
    We augment the raw item data with categorisation results (category, reasoning,
    action) so the JSON contains both original data and analysis results. This
    makes the JSON self-documenting - users can see both what the data is and
    how we categorised it.

    File Size Considerations:
    For 303 items with ~5 children each, JSON file is typically ~500KB.
    With pretty-printing (indent=2), it might be ~750KB. This is small enough
    to commit to Git if needed, though typically we .gitignore it since it's
    regenerated from Zotero.

    Args:
        items_details (list): List of item detail dicts from fetch_item_details()
            May contain None values (items that failed to fetch)

    Side Effects:
        Writes data/multiple_attachments_details.json file

    Example Usage:
        # Load data in another script
        import json
        with open('data/multiple_attachments_details.json', 'r') as f:
            data = json.load(f)

        print(f"Inspected {data['total_items']} items")
        for item in data['items']:
            if item['category'] == 'multiple_pdfs':
                print(f"HIGH PRIORITY: {item['title']}")

    See Also:
        generate_inspection_report(): Creates human-readable Markdown report
    """
    # Construct output file path
    output_file = config.DATA_DIR / 'multiple_attachments_details.json'
    print(f"\nSaving detailed data to {output_file}...")

    # Create data structure with metadata
    data = {
        # ISO 8601 timestamp format: YYYY-MM-DDTHH:MM:SS
        # isoformat() generates standard timestamp
        'generated_at': datetime.now().isoformat(),

        # Zotero library identifier for reference
        'zotero_group_id': config.ZOTERO_GROUP_ID,

        # Count of successfully fetched items (excludes None values)
        # List comprehension filters out None values then len() counts remainder
        'total_items': len([i for i in items_details if i]),

        # List of item details (filtered to remove None values)
        # None values are items that failed to fetch due to API errors
        'items': [i for i in items_details if i]
    }

    # Write JSON to file
    # Open with UTF-8 encoding (handles international characters in titles)
    with open(output_file, 'w', encoding='utf-8') as f:
        # json.dump() serializes Python dict to JSON text
        # Parameters:
        #   indent=2: Pretty-print with 2-space indentation (human-readable)
        #   ensure_ascii=False: Preserve Unicode characters (don't escape to \\uXXXX)
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Confirm save with count
    print(f"✓ Saved details for {len(data['items'])} items")


def main():
    """
    Main execution function orchestrating the complete inspection workflow.

    This function coordinates all steps in the multiple-attachment inspection process:
    1. Load flagged items from Script 02 output (CSV)
    2. Connect to Zotero with read-only API key
    3. Fetch full details for each flagged item (item + children)
    4. Categorise items by attachment pattern
    5. Generate prioritised inspection report (Markdown)
    6. Export complete details (JSON)
    7. Print summary statistics

    Workflow Design:
    Each step builds on previous step's output:
    - Step 1 provides list of item keys to fetch
    - Step 3 fetches full details for each key
    - Step 4 categorises based on fetched details
    - Step 5 generates report from categorised items
    - Step 6 exports all data for reference

    Progress Reporting:
    We print progress messages at each major step and periodically during long
    operations (fetching items). This keeps users informed that script is working
    and not hung. For 303 items taking ~10 minutes, progress updates are essential.

    Error Handling:
    The entire workflow is wrapped in try/except to catch any errors and provide
    helpful debugging information. Individual item fetch errors are handled gracefully
    (return None, continue processing), but fatal errors (missing CSV, network failure)
    stop the entire script.

    Output Files Summary:
    After successful completion, these files will have been created/updated:
    - reports/multiple_attachments_inspection.md (human-readable prioritised report)
    - data/multiple_attachments_details.json (complete item data for reference)

    Performance:
    For typical dataset (303 flagged items):
    - Loading CSV: <1 second
    - Fetching items: 5-10 minutes (2 API requests per item)
    - Categorisation: <1 second
    - Report generation: <1 second
    - Total time: ~5-10 minutes (dominated by API requests)

    Returns:
        None (main is called for side effects - file generation)

    Exit Codes:
        0: Success (all items inspected and reports generated)
        1: Failure (error occurred, see traceback for details)

    Side Effects:
        - Writes multiple files to reports/ and data/ directories
        - Makes HTTP requests to Zotero API (2 per flagged item)
        - Prints progress messages to console
        - May take 5-10 minutes to complete

    Dependencies:
        - Requires data/quality_multiple_attachments.csv (from Script 02)
        - Requires Zotero API credentials in .env file
        - Requires required directories to exist (created by config module)

    Example Usage:
        if __name__ == '__main__':
            main()

    See Also:
        - Script 02 (02_analyze_tags.py): Generates input CSV file
        - Zotero web interface: https://www.zotero.org/groups/2258643/ (for manual review)
    """
    # Print header banner for visual separation in console output
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - MULTIPLE ATTACHMENTS INSPECTION")
    print("Script 03: Examine items with multiple attachments")
    print("="*70)
    print()

    # Wrap entire workflow in try/except for centralized error handling
    try:
        # Step 1: Load flagged items from Script 02 output
        # This CSV contains item keys and attachment counts
        flagged_df = load_flagged_items()

        # Step 2: Connect to Zotero
        # Use read-only API key (principle of least privilege)
        # This script only reads data - never modifies the library
        print("\nConnecting to Zotero...")
        zot = zotero.Zotero(
            config.ZOTERO_GROUP_ID,
            config.ZOTERO_LIBRARY_TYPE,
            config.ZOTERO_API_KEY_READONLY  # Read-only key (security: prevents accidental modification)  # noqa: E501
        )
        print("✓ Connected")

        # Step 3: Fetch details for each flagged item
        # This is the slow step (2 API requests per item)
        # For 303 items, this takes ~10 minutes
        print(f"\nFetching details for {len(flagged_df)} items...")
        print("(This may take a few minutes...)")

        # Initialize list to store fetched item details
        items_details = []

        # Iterate through DataFrame rows
        # iterrows() returns (index, row) tuples
        for idx, row in flagged_df.iterrows():
            # Extract item key from this row
            item_key = row['key']

            # Print progress every 50 items
            # This reassures users that script is still running
            # Using (idx + 1) because idx is 0-based but we want 1-based count
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(flagged_df)} items...")

            # Fetch full details for this item
            # Returns dict with item metadata and children, or None if error
            item_info = fetch_item_details(zot, item_key)

            # Append to list (including None values for failed fetches)
            # We filter out None values later when generating reports
            items_details.append(item_info)

        # Confirm completion with count of successful fetches
        # List comprehension filters None values then counts remainder
        print(f"✓ Retrieved details for {len([i for i in items_details if i])} items")

        # Step 4 & 5: Categorise items and generate report
        # categorise_attachment_pattern() is called internally by generate_inspection_report()
        # Returns categorised dict for summary statistics
        categorised = generate_inspection_report(items_details)

        # Step 6: Export complete details to JSON
        # Provides reference data for curators and programmatic access
        save_details_json(items_details)

        # Print summary statistics
        # This gives curators quick overview before diving into report
        print("\n" + "="*70)
        print("✓ INSPECTION COMPLETE")
        print("="*70)

        # Category summary with counts
        print("\nCategory Summary:")
        print(f"  HIGH PRIORITY - Multiple PDFs: {len(categorised['multiple_pdfs'])} items")
        print(f"  LOW PRIORITY - PDF + Notes: {len(categorised['pdf_plus_notes'])} items")
        print(f"  MEDIUM - Multiple Notes: {len(categorised['multiple_notes'])} items")
        print(f"  MEDIUM - Mixed Content: {len(categorised['mixed_content'])} items")
        print(f"  MEDIUM - Uncertain: {len(categorised['uncertain'])} items")

        # List output files
        print("\nOutputs created:")
        print(f"  - {config.REPORTS_DIR / 'multiple_attachments_inspection.md'}")
        print(f"  - {config.DATA_DIR / 'multiple_attachments_details.json'}")

        # Suggest next steps in workflow
        print("\nNext: Review the HIGH PRIORITY section in the report")

    except Exception as e:
        # Catch any error that occurred during execution
        # Print error message and full traceback for debugging
        print(f"\n❌ ERROR: {e}")

        # import traceback here (not at top) because it's only needed for error handling
        import traceback
        traceback.print_exc()  # Print full stack trace showing where error occurred

        # Exit with status code 1 to signal failure
        # This allows shell scripts to detect failure with $? or "if command; then"
        sys.exit(1)


# Standard Python idiom: Only run main() if this file is executed directly
# (not if it's imported as a module by another script)
if __name__ == '__main__':
    main()
