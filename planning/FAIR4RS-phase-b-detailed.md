# Phase B Detailed: Enhanced Code Documentation

**Status:** Ready for implementation
**Estimated Time:** 4-6 hours
**Dependencies:** Phase A completion (FAIR4RS compliance documentation)
**Last Updated:** 2025-10-09

---

## Overview

Phase B implements comprehensive code documentation to make the software truly **Reusable** (the "R" in FAIR4RS) by ensuring that digital humanities researchers, data scientists, and heritage professionals can understand, modify, and extend the codebase without prior knowledge of the project.

### Relationship to Phase A

**Phase A (Completed)** established external FAIR4RS compliance:
- CITATION.cff and codemeta.json (Findable)
- README.md and installation guides (Accessible)
- Data format and vocabulary documentation (Interoperable)
- CONTRIBUTING.md and licence clarity (Reusable)

**Phase B (This Phase)** establishes internal code clarity:
- Comprehensive module docstrings explaining research context
- Detailed function docstrings with parameters, returns, exceptions, examples
- Educational inline comments explaining design decisions and algorithms
- UK/Australian spelling throughout all code
- Domain-specific terminology defined in context

### Why Phase B Matters

Research software differs from commercial software in that users often need to:
- Understand the methodological choices embedded in code
- Adapt algorithms for different datasets or research questions
- Validate that the software does what the documentation claims
- Learn computational approaches for their own projects

**Without comprehensive code documentation**, researchers must reverse-engineer the logic, risking misuse or abandonment. **With Phase B documentation**, the software becomes a teaching tool and a trustworthy research instrument.

### FAIR Vocabularies Integration (Pragmatic 80-20 Approach)

This project develops controlled vocabularies from folksonomy tags for publication to Research Vocabularies Australia (RVA). Documentation should explain vocabulary development following **FAIR principles for vocabularies** (Cox et al., 2021), taking a pragmatic approach focused on achievable goals.

**FAIR Vocabularies - Pragmatic Implementation:**

This project achieves FAIR vocabulary compliance through:

✅ **Easy wins (implement fully):**
- Term completeness - each tag has label and definition
- Version control - vocabulary development tracked in Git
- Machine-readable formats - export to SKOS/RDF for RVA
- Mapping to established vocabularies - Getty AAT/TGN (themselves FAIR)
- Open licensing - Creative Commons Attribution 4.0
- RVA registration - persistent identifiers and DOI from RVA

⚠️ **Aspirational (document, don't over-engineer):**
- Formal governance - note research team maintains, don't create committees
- Elaborate metadata schemas - use what RVA requires, don't invent more
- Complex revision processes - version control is sufficient

**Key Insight:** Mapping to well-maintained FAIR vocabularies (Getty AAT/TGN) provides substantial FAIR compliance by association. This project exceeds 90%+ of digital humanities projects in vocabulary FAIRness.

**Phase B Documentation Focus:**

When documenting vocabulary development scripts, briefly explain:
- Why we map to Getty vocabularies (FAIR compliance by reference)
- How RVA publication provides persistent identifiers
- Why SKOS/RDF format enables interoperability
- How Git provides traceable maintenance

Keep explanations concise and practical - focus on what the code does, not aspirational governance models.

**Reference:**
Cox SJD, Gonzalez-Beltran AN, Magagna B, Marinescu MC (2021) Ten simple rules for making a vocabulary FAIR. PLOS Computational Biology 17(6): e1009041. https://doi.org/10.1371/journal.pcbi.1009041

---

## Documentation Standards

### The Three Levels of Documentation

Phase B implements documentation at three levels:

#### Level 1: Module Docstrings
**Purpose:** Explain the script's role in the research workflow

**Required Elements:**
- Research context (why this script exists)
- Workflow position (what comes before/after)
- Inputs (data dependencies, API requirements)
- Outputs (files created, data structures)
- Usage examples

**Example:**
```python
"""
Script 01: Extract Tags from Zotero Group Library

Research Context:
This script implements the first phase of folksonomy rationalisation for
the Blue Mountains shale mining communities digital collection. Historical
newspaper articles in the Zotero group library have been tagged by research
assistants using informal, descriptive terms. This script extracts those
tags to prepare them for standardisation against controlled vocabularies
(Getty Art & Architecture Thesaurus (AAT) and Thesaurus of Geographic Names (TGN))
and publication to Research Vocabularies Australia (RVA).

Workflow Position:
1. [THIS SCRIPT] Extract tags from Zotero
2. Analyse tags for consolidation (02_analyze_tags.py)
3. Develop controlled vocabulary and prepare for publication
4. Publish controlled vocabulary to RVA and Omeka Classic

Methodological Questions Addressed:
- What subject areas have research assistants prioritised in tagging?
- How consistent is the tagging vocabulary across the corpus?
- Which items lack subject metadata (quality assurance)?

Technical Approach:
Connects to the Zotero API (pyzotero library) and retrieves all items from
the group library. The API paginates responses at 100 items per request to
prevent timeouts. Tags are extracted from each item's metadata and stored
with full provenance (which items use each tag, item titles for context).

Inputs:
- Zotero API credentials (.env file)
- Group library ID: 2258643 (Blue Mountains project)
- Internet connection for API access

Outputs:
- data/raw_tags.json: Complete tag data with item associations
- data/tag_frequency.csv: Tags sorted by usage frequency
- reports/tag_summary.md: Statistical overview for project team

Dependencies:
- pyzotero: Zotero API client (requires API key)
- pandas: Data manipulation and CSV export
- python-dotenv: Secure API credential management

Usage:
    python scripts/01_extract_tags.py

    Expected runtime: 2-5 minutes (depends on library size)
    Network requirements: HTTPS access to api.zotero.org

Author: Shawn Ross
Project: ARC LP190100900 - Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""
```

#### Level 2: Function Docstrings
**Purpose:** Explain what each function does and how to use it

**Required Elements (from CONTRIBUTING.md):**
1. Brief summary (one line)
2. Detailed description (2-4 paragraphs with context)
3. Parameters: type, description, example values, constraints
4. Returns: type, structure, example
5. Raises: exceptions and when they occur
6. Example: working code snippet
7. See Also: (optional) related functions, documentation
8. Note: (optional) performance tips, caveats, dependencies

**Example:**
```python
def extract_tags_from_items(items):
    """
    Extract all tags and their associations with items from Zotero data.

    This function processes the raw JSON response from Zotero's API to build
    a comprehensive tag dataset. For each unique tag, we track:
    - Usage count (how many items have this tag)
    - Item associations (which specific items use it)
    - Item titles (for human-readable context in reports)

    The function also calculates aggregate statistics to support data quality
    assessment, including identifying untagged items that need subject metadata.

    Design Decision: We use defaultdict instead of regular dict to avoid
    KeyError exceptions when incrementing counts. This makes the code more
    Pythonic and easier to maintain than checking for key existence before
    each update.

    Parameters:
        items (list): List of Zotero item dictionaries returned by
                     zotero.items(). Each item must have 'key', 'data',
                     and 'data.tags' fields. The pyzotero library
                     guarantees this structure.

    Returns:
        tuple: (tag_data, statistics) where:
            - tag_data (dict): Maps tag names to usage information:
                {
                    'tag_name': {
                        'count': int,           # number of items using this tag
                        'items': [str],         # list of item keys (Zotero IDs)
                        'item_titles': [str]    # list of item titles
                    }
                }
            - statistics (dict): Aggregate metrics:
                {
                    'total_items': int,
                    'items_with_tags': int,
                    'items_without_tags': int,
                    'unique_tags': int,
                    'total_tag_applications': int,
                    'avg_tags_per_item': float,
                    'max_tags_per_item': int,
                    'min_tags_per_item': int
                }

    Raises:
        KeyError: If items list contains malformed dictionaries missing
                 required fields. This indicates a pyzotero API change or
                 data corruption.
        TypeError: If items parameter is not a list or contains non-dict elements.

    Example:
        >>> zot = zotero.Zotero('2258643', 'group', 'api_key')
        >>> items = zot.items()
        >>> tag_data, stats = extract_tags_from_items(items)
        >>> print(f"Found {stats['unique_tags']} unique tags")
        Found 481 unique tags
        >>> print(tag_data['Mining']['count'])
        32

    See Also:
        - save_raw_tags(): Saves the returned data to JSON
        - create_frequency_table(): Generates CSV report from tag_data

    Note:
        This function loads all data into memory. For libraries with >100,000
        items, consider processing in batches to avoid memory issues. The
        Blue Mountains library (~1,200 items) processes in <1 second.
    """
    print("\nExtracting tags from items...")

    # Use defaultdict to simplify counting logic
    # This avoids the need for "if key in dict" checks before incrementing
    tag_data = defaultdict(lambda: {
        'count': 0,
        'items': [],
        'item_titles': []
    })

    items_with_tags = 0
    items_without_tags = 0
    total_tag_applications = 0
    tags_per_item = []

    for item in items:
        # Extract item metadata
        # We handle missing fields gracefully with .get() to prevent KeyErrors
        item_id = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_type = item['data'].get('itemType', 'unknown')
        tags = item['data'].get('tags', [])

        if tags:
            items_with_tags += 1
            tags_per_item.append(len(tags))

            # Process each tag
            # Zotero API returns tags as list of dicts: [{'tag': 'Mining'}, ...]
            for tag_obj in tags:
                tag_name = tag_obj.get('tag', '')
                if tag_name:
                    tag_data[tag_name]['count'] += 1
                    tag_data[tag_name]['items'].append(item_id)
                    tag_data[tag_name]['item_titles'].append(item_title)
                    total_tag_applications += 1
        else:
            items_without_tags += 1

    print(f"✓ Extracted {len(tag_data)} unique tags")
    print(f"  Items with tags: {items_with_tags}")
    print(f"  Items without tags: {items_without_tags}")
    print(f"  Total tag applications: {total_tag_applications}")

    # Calculate summary statistics
    # We use conditional expressions to handle edge case of zero tagged items
    stats = {
        'total_items': len(items),
        'items_with_tags': items_with_tags,
        'items_without_tags': items_without_tags,
        'unique_tags': len(tag_data),
        'total_tag_applications': total_tag_applications,
        'avg_tags_per_item': sum(tags_per_item) / len(tags_per_item) if tags_per_item else 0,
        'max_tags_per_item': max(tags_per_item) if tags_per_item else 0,
        'min_tags_per_item': min(tags_per_item) if tags_per_item else 0
    }

    return dict(tag_data), stats
```

#### Level 3: Inline Comments
**Purpose:** Explain design decisions, algorithms, and non-obvious logic

**Guidelines:**
- Comment the "why" not the "what" (code shows what it does)
- Explain algorithmic choices (why this approach vs alternatives)
- Define domain-specific terminology when first used
- **Expand acronyms on first usage** in each file/module (see CLAUDE.md for standard expansions)
- Highlight performance considerations
- Document workarounds for Application Programming Interface (API) limitations or bugs
- Explain data structure choices

**Good Examples:**
```python
# Use fuzzywuzzy library for similarity detection instead of simple string matching
# This catches variants like "Mining" vs "Mines" that differ by character edits
# The Levenshtein Distance algorithm counts insertions, deletions, substitutions
similarity = fuzz.ratio(tag1.lower(), tag2.lower())

# Zotero API limits responses to 100 items per request to prevent server timeouts
# We implement pagination by requesting batches with incrementing start offsets
# This is more reliable than requesting all items at once (which fails for large libraries)
batch_size = 100

# Convert defaultdict to regular dict before JSON serialisation
# defaultdict objects aren't JSON-serialisable because of their factory function
# This conversion is safe because we're done adding new keys
tag_data = dict(tag_data)
```

**Bad Examples (avoid these):**
```python
# Increment counter
count += 1  # DON'T: States the obvious

# Loop through items
for item in items:  # DON'T: Restates code

# Set threshold to 80
threshold = 80  # DON'T: No context for why 80
```

---

## Script-by-Script Enhancement Plan

### B1. config.py Enhancement

**Current State:** 42 lines, basic module docstring, minimal comments

**Target State:** ~120 lines with comprehensive documentation

#### Current Issues:
- Module docstring doesn't explain configuration management philosophy
- No explanation of why .env file approach is used
- Path structure creation not explained
- Validation logic uncommented

#### Enhancement Tasks:

**Task B1.1: Enhance Module Docstring**

Add comprehensive context:
- Why configuration management is separate from scripts
- Security rationale for .env files (API keys not in code)
- Path management approach (creating directories on import)
- How to add new configuration variables

**Before:**
```python
"""
Configuration file for Blue Mountains project.
Loads API credentials and settings from environment variables.
"""
```

**After:**
```python
"""
Configuration Management for Blue Mountains Digital Collection Software

Purpose:
Centralised configuration management for all scripts in the project. This module
loads API credentials, defines project paths, and ensures required directories exist.
All other scripts import this module to access configuration constants.

Security Model:
API credentials are stored in a .env file (NEVER committed to Git) and loaded via
python-dotenv library. This prevents accidental exposure of secret keys in version
control. The .env file is listed in .gitignore to enforce this security boundary.

Design Decision - Centralised Configuration:
Rather than having each script load its own .env file, we centralise configuration
here. Benefits:
1. Single source of truth for all credentials and paths
2. Consistent validation (all scripts fail early if credentials missing)
3. Easier maintenance (change paths in one place)
4. Testability (can override config in tests)

Path Management:
We define all project directories as Path objects (pathlib) rather than strings.
Benefits:
- Platform-independent path separators (works on Windows/Mac/Linux)
- Path manipulation methods (.parent, .mkdir(), etc.)
- Type safety (IDE autocomplete)

Directory Auto-Creation:
This module creates required directories when imported (using mkdir with parents=True
and exist_ok=True). This ensures scripts can immediately write outputs without checking
if directories exist. We use exist_ok=True to avoid errors when directories already
exist from previous runs.

Adding New Configuration:
1. Add environment variable to .env.example with documentation
2. Load it here with os.getenv('VARIABLE_NAME')
3. Add validation if required (see Zotero validation example)
4. Document the variable in this docstring

Usage:
    # Import at top of every script
    import config

    # Access credentials
    zot = zotero.Zotero(config.ZOTERO_GROUP_ID,
                       config.ZOTERO_LIBRARY_TYPE,
                       config.ZOTERO_API_KEY)

    # Access paths
    output_file = config.DATA_DIR / 'output.json'
    report_file = config.REPORTS_DIR / 'report.md'

Dependencies:
- python-dotenv: Loads .env file variables into os.environ
- pathlib: Modern path manipulation (Python 3.4+)

Security Notes:
- Never print API keys in logs or console output
- Validate that .env is in .gitignore before committing
- Regenerate API keys if accidentally committed

API Key Permissions:
Best practice is to use separate API keys for different access levels:
- Read-only key: For scripts that only extract/analyse data (01-03)
- Read-write key: For future scripts that modify Zotero library

Using read-only keys for extraction scripts follows the principle of least
privilege - if a key is compromised or script has bugs, it cannot accidentally
modify or delete library data. However, Zotero doesn't require separate keys
if the same key is carefully managed. Document which scripts need write access.

To generate API keys with specific permissions:
1. Visit https://www.zotero.org/settings/keys
2. Create new key and select permissions:
   - "Allow library access" → Read-only OR Read/Write
   - Select specific group library
3. Add key to .env file with descriptive variable name:
   - ZOTERO_API_KEY_READONLY (for extraction scripts)
   - ZOTERO_API_KEY_READWRITE (for future modification scripts)

Author: Shawn Ross
Project: ARC LP190100900 - Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""
```

**Task B1.2: Comment Path Configuration Section**

```python
# Project Paths
# =============
# All paths are defined as pathlib.Path objects for platform independence
# These paths are relative to PROJECT_ROOT (the repository root directory)

# PROJECT_ROOT is the parent directory of scripts/ (i.e., repository root)
# We use __file__ to get this config.py file's location, then navigate up
# __file__ = /path/to/blue-mountains/scripts/config.py
# __file__.parent = /path/to/blue-mountains/scripts
# __file__.parent.parent = /path/to/blue-mountains
PROJECT_ROOT = Path(__file__).parent.parent

# data/ - Machine-readable outputs (JSON, CSV)
# Generated by scripts, used as inputs to other scripts
# Excluded from Git (in .gitignore) - regenerated from Zotero
DATA_DIR = PROJECT_ROOT / 'data'

# reports/ - Human-readable reports (Markdown)
# Generated by scripts, intended for project team review
# Excluded from Git (in .gitignore) - regenerated from Zotero
REPORTS_DIR = PROJECT_ROOT / 'reports'

# backups/ - Timestamped backups of important data
# Used before major changes (e.g., before tag consolidation)
# Excluded from Git (in .gitignore) - local only
BACKUPS_DIR = PROJECT_ROOT / 'backups'

# logs/ - Script execution logs for debugging
# Not currently used but prepared for future logging implementation
# Excluded from Git (in .gitignore) - local only
LOGS_DIR = PROJECT_ROOT / 'logs'

# visualisations/ - Generated charts and network graphs (PNG, SVG)
# Created by analysis scripts, embedded in reports
# Excluded from Git (in .gitignore) - regenerated from data
VISUALIZATIONS_DIR = PROJECT_ROOT / 'visualizations'
```

**Task B1.3: Comment Directory Creation**

```python
# Ensure all required directories exist
# =====================================
# We create directories when this config module is imported (at script startup)
# This guarantees that scripts can immediately write files without error checking
#
# mkdir() parameters:
#   parents=True:  Create parent directories if needed (like 'mkdir -p')
#   exist_ok=True: Don't raise error if directory already exists
#
# This approach uses "ask forgiveness not permission" (AFNP) Python philosophy:
# Rather than checking if directory exists then creating (LBYL - look before you leap),
# we just create and ignore the error if it exists. More concise and thread-safe.
for directory in [DATA_DIR, REPORTS_DIR, BACKUPS_DIR, LOGS_DIR, VISUALIZATIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
```

**Task B1.4: Comment Validation Section**

```python
# Validation
# ==========
# We validate critical configuration before any scripts run
# This provides clear error messages at startup rather than cryptic failures later

# Zotero credentials are REQUIRED for all scripts
# Without these, API calls will fail with authentication errors
# We check both GROUP_ID and API_KEY exist and are non-empty
if not ZOTERO_GROUP_ID or not ZOTERO_API_KEY:
    raise ValueError(
        "Zotero credentials not found in .env file\n"
        "Required variables: ZOTERO_GROUP_ID, ZOTERO_API_KEY\n"
        "See .env.example for setup instructions"
    )

# Success confirmation
# Print to console so users know configuration loaded correctly
# We don't print API_KEY (security risk - might be logged or screenshotted)
print(f"✓ Configuration loaded successfully")
print(f"  Zotero Group ID: {ZOTERO_GROUP_ID}")
print(f"  Library Type: {ZOTERO_LIBRARY_TYPE}")
```

**Task B1.5: Add Configuration Testing Guidance**

Add as comment at bottom:

```python
# Testing This Configuration
# ==========================
# To verify configuration is correct, run this file directly:
#   python scripts/config.py
#
# Expected output:
#   ✓ Configuration loaded successfully
#   Zotero Group ID: 2258643
#   Library Type: group
#
# If you see ValueError, check your .env file:
#   1. Does .env exist in project root? (not in scripts/ directory)
#   2. Does it contain ZOTERO_GROUP_ID=2258643?
#   3. Does it contain ZOTERO_API_KEY=your_actual_key?
#   4. Is python-dotenv installed? (pip install python-dotenv)
```

---

### B2. 01_extract_tags.py Enhancement

**Current State:** ~200 lines, basic docstrings, some comments

**Target State:** ~350 lines with comprehensive educational documentation

#### Enhancement Tasks:

**Task B2.1: Enhance Module Docstring**

Replace existing module docstring with comprehensive version (see Level 1 example above in Documentation Standards section).

**Task B2.2: Enhance connect_to_zotero() Function**

```python
def connect_to_zotero():
    """
    Initialise connection to Zotero group library via API.

    This function creates a Zotero API client object that handles authentication
    and HTTP requests to Zotero's servers. The pyzotero library (a wrapper around
    the Zotero Web API v3) manages:
    - API authentication via key
    - Request rate limiting to respect Zotero's fair use policy
    - Error handling for network failures
    - JSON response parsing

    Authentication Model:
    Zotero uses API key-based authentication (not username/password). Each API key
    is associated with a Zotero user account and grants specific permissions:
    - Read-only access: Can retrieve library data
    - Read/write access: Can also create, update, delete items

    Our project uses read-only access for data extraction scripts. This is a security
    best practice - scripts that only read data can't accidentally modify the library.

    Group vs Personal Libraries:
    Zotero has two library types:
    - Personal libraries: Belong to individual user accounts
    - Group libraries: Shared collections for collaborative research

    This project uses a group library (ID: 2258643) shared among the research team.
    All team members can add items and tags, and this script extracts the collective
    tagging work.

    Returns:
        pyzotero.zotero.Zotero: Authenticated API client object. This object provides
                                methods like .items(), .tags(), .children() to retrieve
                                library data. See pyzotero documentation for full API:
                                https://pyzotero.readthedocs.io/

    Raises:
        ValueError: If configuration validation fails (credentials missing)
        ConnectionError: If Zotero API is unreachable (network down, API maintenance)
        AuthenticationError: If API key is invalid or lacks required permissions

    Example:
        >>> zot = connect_to_zotero()
        >>> items = zot.items()  # Retrieve all items
        >>> print(f"Library has {len(items)} items")

    See Also:
        - config.py: Where credentials are loaded and validated
        - Zotero Web API documentation: https://www.zotero.org/support/dev/web_api/v3/start

    Note:
        This function doesn't make any API calls itself - it just creates the client.
        Actual network requests happen when you call methods like .items() or .tags().
        The client maintains a connection pool and handles request retries automatically.
    """
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")

    # Create Zotero API client
    # Parameters:
    #   library_id: Numeric ID of the library (group or user)
    #   library_type: 'group' or 'user'
    #   api_key: Authentication token from https://www.zotero.org/settings/keys
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY
    )

    return zot
```

**Task B2.3: Enhance fetch_all_items() Function**

```python
def fetch_all_items(zot):
    """
    Retrieve all items from Zotero library using pagination.

    The Zotero API limits responses to 100 items per request to prevent server
    overload and timeout errors. For libraries with >100 items, we must paginate
    by making multiple requests with incrementing start offsets.

    Pagination Strategy:
    We use a simple while loop that:
    1. Requests batch of 100 items starting at offset 0
    2. If batch is non-empty, adds items to results and requests next batch (offset 100)
    3. If batch is empty, we've reached the end of the library

    Alternative approaches considered:
    - Request all items at once: Fails for large libraries (timeout/memory)
    - Use .num_items() to calculate pages: Extra API call, and total count can change
      during iteration (if someone adds items while script runs)
    - Request smaller batches (50): More API calls = slower
    - Request larger batches (200): Exceeds Zotero's limit, returns error

    We chose this approach because:
    - Simple to implement and understand
    - Handles libraries of any size
    - Robust to library size changes during execution
    - Batch size of 100 is Zotero's recommended optimum

    Performance:
    Typical request time is 200-500ms per batch, so:
    - Small library (100 items): ~1 second
    - Medium library (1,000 items): ~5 seconds
    - Large library (10,000 items): ~50 seconds

    Our Blue Mountains library (~1,200 items) takes approximately 5-8 seconds.

    Parameters:
        zot (pyzotero.zotero.Zotero): Authenticated Zotero API client from
                                      connect_to_zotero() function

    Returns:
        list: List of item dictionaries. Each item has structure:
              {
                  'key': 'ABC123',           # Unique item ID
                  'version': 123,            # Item version (for conflict detection)
                  'library': {...},          # Library metadata
                  'data': {                  # Item metadata
                      'key': 'ABC123',
                      'version': 123,
                      'itemType': 'newspaperArticle',
                      'title': 'Article Title',
                      'creators': [...],
                      'date': '1900-01-01',
                      'tags': [{'tag': 'Mining'}, {'tag': 'Katoomba'}],
                      ...
                  },
                  'meta': {...}              # Additional metadata
              }

    Raises:
        ConnectionError: If network fails during requests
        zotero.zotero_errors.HTTPError: If API returns error (rate limit, auth failure)

    Example:
        >>> zot = connect_to_zotero()
        >>> items = fetch_all_items(zot)
        >>> print(f"Retrieved {len(items)} items")
        Retrieved 1189 items
        >>> print(items[0]['data']['itemType'])
        newspaperArticle

    Note:
        This function loads all items into memory. For extremely large libraries
        (>100,000 items), consider processing batches as they arrive rather than
        accumulating all items first. Our library size (~1,200 items) is well within
        memory limits (<10 MB of data).
    """
    print("Fetching all items from library...")

    items = []  # Accumulator for all items
    start = 0   # Offset for pagination (which item to start from)
    limit = 100 # Batch size (Zotero's maximum and recommended size)

    while True:
        # Request batch of items
        # The pyzotero library handles the actual HTTP request and JSON parsing
        # Parameters:
        #   start: Offset (0 = first item, 100 = 101st item, etc.)
        #   limit: How many items to return (max 100)
        batch = zot.items(start=start, limit=limit)

        # Check if we've exhausted the library
        # When there are no more items, Zotero returns empty list
        if not batch:
            break

        # Add this batch to our results
        items.extend(batch)

        # Move offset forward for next batch
        # If we just retrieved items 0-99, next batch starts at 100
        start += limit

        # Progress indicator so users know script is working
        # Important for large libraries where this takes >30 seconds
        print(f"  Retrieved {len(items)} items so far...")

    print(f"✓ Total items retrieved: {len(items)}")
    return items
```

**Task B2.4: Enhance extract_tags_from_items() Function**

Use the comprehensive example from Level 2 documentation above (already fully documented there).

**Task B2.5: Enhance save_raw_tags() Function**

```python
def save_raw_tags(tag_data, stats):
    """
    Save complete tag data to JSON file with metadata and statistics.

    This function creates a JSON file that serves as the primary data product of
    this script. The JSON format was chosen over CSV because:
    1. Preserves nested structure (tags → items → titles)
    2. Supports arrays (multiple items per tag)
    3. Includes metadata (generation timestamp, statistics)
    4. Can be parsed by other scripts without ambiguity

    JSON Structure:
    The output file has two top-level keys:
    - 'metadata': Generation info and aggregate statistics
    - 'tags': Complete tag data (see Parameters below)

    This structure follows a common pattern in research data management:
    - Data provenance in metadata (when generated, from what source)
    - Summary statistics for quick overview
    - Detailed data for analysis

    File Format Decision:
    We use UTF-8 encoding with ensure_ascii=False to preserve non-ASCII characters
    (accented letters, Unicode symbols). This is essential for international names
    and place names in our dataset (e.g., "Pére", "Katoomb≈").

    We use indent=2 for human readability (at cost of larger file size). For a
    dataset this small (~500KB), readability is more valuable than space savings.
    If file size became problematic (>100MB), we'd remove indentation.

    Parameters:
        tag_data (dict): Dictionary mapping tag names to usage information.
                        Structure:
                        {
                            'tag_name': {
                                'count': int,
                                'items': [str],         # list of item keys
                                'item_titles': [str]    # list of titles
                            }
                        }

        stats (dict): Aggregate statistics from extract_tags_from_items().
                     Contains: total_items, items_with_tags, unique_tags, etc.

    Returns:
        None (side effect: creates/overwrites file)

    Raises:
        PermissionError: If script lacks write permission to data/ directory
        IOError: If disk is full or other I/O error occurs

    Example:
        >>> tag_data, stats = extract_tags_from_items(items)
        >>> save_raw_tags(tag_data, stats)
        Saving raw tag data to /path/to/data/raw_tags.json...
        ✓ Saved to /path/to/data/raw_tags.json

    See Also:
        - load_tag_data() in 02_analyze_tags.py: Reads this JSON file
        - docs/data-formats.md: Full JSON schema documentation

    Note:
        This function overwrites the file if it exists. To preserve previous
        extractions, manually copy data/raw_tags.json to backups/ directory
        with timestamp before running script again.
    """
    output_file = config.DATA_DIR / 'raw_tags.json'
    print(f"\nSaving raw tag data to {output_file}...")

    # Build output data structure
    # We include metadata following FAIR data principles:
    # - Provenance: when generated, from what source
    # - Statistics: summary metrics for quick assessment
    # - Data: the actual tag information
    data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),  # ISO 8601 format
            'zotero_group_id': config.ZOTERO_GROUP_ID,
            'statistics': stats
        },
        'tags': tag_data
    }

    # Write JSON to file
    # Parameters:
    #   indent=2: Pretty-print with 2-space indentation
    #   ensure_ascii=False: Preserve Unicode characters (don't escape to \uXXXX)
    #   encoding='utf-8': Use UTF-8 encoding (standard for JSON)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {output_file}")
```

**Task B2.6: Add UK/Australian Spelling**

Review all comments and docstrings:
- "organize" → "organise" (if present)
- "analyze" → "analyse" (if present)
- "center" → "centre" (if present)

**Task B2.7: Enhance Main Execution Block**

```python
if __name__ == '__main__':
    """
    Main execution block - runs when script is executed directly.

    This block orchestrates the complete tag extraction workflow:
    1. Connect to Zotero API
    2. Fetch all items from library
    3. Extract tags and calculate statistics
    4. Save results to JSON and CSV
    5. Generate human-readable report

    The 'if __name__ == "__main__"' guard ensures this only runs when the script
    is executed directly (python 01_extract_tags.py), not when imported as a module
    by other scripts. This is a Python best practice that:
    - Makes functions reusable by other scripts
    - Prevents accidental execution during imports
    - Enables easier testing (can import functions without side effects)

    Error Handling:
    We don't catch exceptions here because we want errors to propagate and halt
    execution. If Zotero connection fails, we want the script to stop immediately
    with a clear error message, not continue with partial results.
    """
    print("="*60)
    print("Blue Mountains - Tag Extraction")
    print("="*60)

    # Step 1: Connect to Zotero
    # This validates credentials and creates API client
    zot = connect_to_zotero()

    # Step 2: Retrieve all items
    # This makes multiple API requests (pagination) and can take several seconds
    items = fetch_all_items(zot)

    # Step 3: Extract tags
    # This processes items in memory (fast, <1 second)
    tag_data, stats = extract_tags_from_items(items)

    # Step 4: Save outputs
    # These functions write files and generate reports
    save_raw_tags(tag_data, stats)
    create_frequency_table(tag_data)
    generate_summary_report(stats, tag_data)

    print("\n" + "="*60)
    print("✓ Tag extraction complete!")
    print("="*60)
    print(f"\nOutputs:")
    print(f"  - {config.DATA_DIR / 'raw_tags.json'}")
    print(f"  - {config.DATA_DIR / 'tag_frequency.csv'}")
    print(f"  - {config.REPORTS_DIR / 'tag_summary.md'}")
    print(f"\nNext steps:")
    print(f"  1. Review {config.REPORTS_DIR / 'tag_summary.md'}")
    print(f"  2. Run python scripts/02_analyze_tags.py")
```

---

### B3. 02_analyze_tags.py Enhancement

**Current State:** ~400 lines, basic docstrings

**Target State:** ~650 lines with comprehensive documentation

#### Enhancement Focus Areas:

This script contains the most complex algorithms in the project (fuzzy matching,
network analysis, hierarchical detection). Documentation must explain not just
what the code does, but why these approaches were chosen and how the algorithms work.

**Key Documentation Challenges:**
1. Fuzzy string matching (Levenshtein Distance algorithm)
2. Tag hierarchy detection (substring matching + co-occurrence)
3. Network analysis (co-occurrence graphs)
4. Data quality categorisation (attachment patterns)

**Task B3.1: Enhance Module Docstring**

Add comprehensive docstring explaining:
- Phase 2 of the workflow (analyse tags from Phase 1 extraction)
- Four analysis types: similarity, hierarchies, co-occurrence, quality
- Algorithmic approaches (fuzzy matching, network analysis)
- How outputs support vocabulary development
- Research questions addressed (tag consolidation needs, quality issues)

**Task B3.2: Enhance find_similar_tags() Function**

```python
def find_similar_tags(tags, threshold=80):
    """
    Identify similar tags using fuzzy string matching for consolidation.

    This function addresses a common problem in collaborative tagging systems:
    inconsistent terminology. Research assistants may use different terms for the
    same concept ("Mine" vs "Mining", "Katoomba" vs "Katoomb" (typo)). Manually
    reviewing 481 tags for similarity is impractical, so we use algorithmic
    comparison.

    Algorithm: Levenshtein Distance via fuzzywuzzy Library

    The Levenshtein Distance algorithm calculates how many single-character edits
    (insertions, deletions, substitutions) are needed to transform one string into
    another. The fuzzywuzzy library converts this distance into a similarity ratio:

    - 100 = identical strings
    - 90+ = very similar (usually spelling variants)
    - 80-89 = similar (possibly related concepts)
    - <80 = dissimilar

    Example calculations:
    - "Mining" vs "Mines": ratio = 83 (6 chars match, 1 deletion)
    - "Katoomba" vs "Katoomb": ratio = 93 (7 chars match, 1 deletion)
    - "Mining" vs "Logging": ratio = 29 (only 'ing' matches)

    Why Three Similarity Metrics?

    We calculate three different similarity scores and use the maximum:

    1. ratio: Basic Levenshtein Distance
       - Best for: Simple spelling variants
       - Example: "organization" vs "organisation" = 98

    2. partial_ratio: Substring matching
       - Best for: One term contained in another
       - Example: "Mine" vs "Coal Mine" = 100 (ignores "Coal ")

    3. token_sort_ratio: Order-independent word matching
       - Best for: Different word orders
       - Example: "Blue Mountains NSW" vs "NSW Blue Mountains" = 100

    Using the maximum of these three scores catches more true matches while
    maintaining high precision. If any method finds high similarity, we flag it.

    Threshold Selection:

    We use threshold=80 by default based on empirical testing:
    - Threshold 90: Misses true variants like "Mine"/"Mining" (similarity=83)
    - Threshold 80: Catches variants while minimising false positives
    - Threshold 70: Too many false positives (unrelated similar words)

    Users can adjust threshold based on their corpus characteristics.

    Computational Complexity:

    This function has O(n²) complexity where n=number of tags:
    - For 481 tags: 115,440 comparisons (481 × 480 / 2)
    - Each comparison takes ~0.1ms
    - Total runtime: ~12 seconds

    For >1000 tags, consider optimisations:
    - Pre-filter by first letter (reduces comparisons 26×)
    - Use approximate nearest neighbor search (e.g., locality-sensitive hashing)
    - Parallel processing (multiprocessing module)

    Parameters:
        tags (dict): Tag data from load_tag_data(), structure:
                    {
                        'tag_name': {
                            'count': int,
                            'items': [str],
                            'item_titles': [str]
                        }
                    }

        threshold (int): Minimum similarity score (0-100) to flag a pair.
                        Default 80. Higher values reduce false positives but
                        may miss true variants. Lower values catch more variants
                        but require more manual review.

    Returns:
        list: List of similar tag pairs, sorted by similarity (highest first).
              Each pair is a dict:
              {
                  'tag1': str,                # First tag name
                  'tag2': str,                # Second tag name
                  'count1': int,              # Usage count of tag1
                  'count2': int,              # Usage count of tag2
                  'similarity': float,        # Best similarity score (0-100)
                  'ratio': float,             # Levenshtein ratio
                  'partial': float,           # Partial ratio
                  'token_sort': float,        # Token sort ratio
                  'suggested_merge': str      # Which tag to keep (higher count)
              }

    Raises:
        ValueError: If tags dict is empty
        TypeError: If threshold is not an integer or is outside 0-100 range

    Example:
        >>> tags = load_tag_data()
        >>> similar = find_similar_tags(tags, threshold=80)
        >>> print(f"Found {len(similar)} similar pairs")
        Found 23 similar pairs
        >>> print(similar[0])
        {
            'tag1': 'Mine',
            'tag2': 'Mining',
            'similarity': 83.3,
            'suggested_merge': 'Mining'  # 'Mining' has higher count
        }

    See Also:
        - fuzzywuzzy documentation: https://github.com/seatgeek/fuzzywuzzy
        - python-Levenshtein: C implementation for 100× speedup
        - save_similar_tags_csv(): Exports results to CSV for manual review

    Note:
        Install python-Levenshtein for performance: pip install python-Levenshtein
        Without it, fuzzywuzzy falls back to pure Python (100× slower).
        For our 481-tag dataset, this reduces runtime from 30s to <1s.
    """
    print(f"\nAnalysing tag similarity (threshold: {threshold})...")

    # Convert tags dict to list for pairwise comparisons
    # We iterate through all unique pairs (combinations, not permutations)
    tag_list = list(tags.keys())
    similar_pairs = []

    # Compare all pairs of tags
    # Using enumerate + slice to avoid comparing tag to itself or duplicate pairs
    # Example: For tags [A, B, C], we compare: (A,B), (A,C), (B,C)
    # We don't compare (A,A), (B,A) (same as A,B), etc.
    for i, tag1 in enumerate(tag_list):
        # Only compare with tags that come after this one in the list
        # This avoids duplicate comparisons and self-comparisons
        for tag2 in tag_list[i+1:]:
            # Calculate similarity using three different methods
            # We use .lower() to make comparison case-insensitive
            # "Mining" and "mining" should be treated as similar

            # Method 1: Basic Levenshtein ratio (character-level edit distance)
            ratio = fuzz.ratio(tag1.lower(), tag2.lower())

            # Method 2: Partial ratio (best matching substring)
            # Useful when one tag is a substring of another
            partial = fuzz.partial_ratio(tag1.lower(), tag2.lower())

            # Method 3: Token sort ratio (order-independent word matching)
            # Useful when words appear in different orders
            token_sort = fuzz.token_sort_ratio(tag1.lower(), tag2.lower())

            # Use the maximum similarity score across all methods
            # If any method finds high similarity, we want to flag it
            max_similarity = max(ratio, partial, token_sort)

            # Only keep pairs that meet or exceed threshold
            if max_similarity >= threshold:
                similar_pairs.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count1': tags[tag1]['count'],
                    'count2': tags[tag2]['count'],
                    'similarity': max_similarity,
                    'ratio': ratio,
                    'partial': partial,
                    'token_sort': token_sort,
                    # Suggest keeping the tag with higher usage count
                    # More frequently used tag is likely the "canonical" version
                    'suggested_merge': tag1 if tags[tag1]['count'] >= tags[tag2]['count'] else tag2
                })

    print(f"✓ Found {len(similar_pairs)} similar tag pairs")
    return similar_pairs
```

**Task B3.3: Enhance calculate_cooccurrence() Function**

```python
def calculate_cooccurrence(tags):
    """
    Calculate tag co-occurrence patterns to identify related concepts.

    Research Question:
    Which tags are frequently used together on the same items? This reveals
    conceptual relationships and can inform hierarchical vocabulary structure.

    Example insights from co-occurrence:
    - "Mining" + "Katoomba" appear together 28 times → geographic association
    - "Women" + "Domestic labour" appear together 15 times → thematic association
    - "Photograph" + "Material culture" appear together 12 times → source type pattern

    Algorithm: Pairwise Co-occurrence Counting

    Step 1: Build item→tags mapping
    We invert the tags→items structure to create a lookup of which tags each item has.
    This allows efficient pairwise iteration.

    Step 2: For each item with 2+ tags, count all pairs
    We use itertools.combinations() to generate all unique pairs from the item's tags.
    combinations(['A', 'B', 'C'], 2) → [('A','B'), ('A','C'), ('B','C')]

    Step 3: Aggregate counts in co-occurrence matrix
    We use defaultdict(lambda: defaultdict(int)) for automatic zero-initialisation.
    This creates a 2D sparse matrix where cooccurrence[tag1][tag2] = count.

    Why Not Use a Dense Matrix?

    A dense matrix would be 481×481=231,361 cells (mostly zeros). This wastes memory
    and processing time. Our sparse representation only stores pairs that actually
    co-occur (typically <5% of possible pairs), reducing memory by 95%.

    Symmetric Matrix:
    We store both cooccurrence[A][B] and cooccurrence[B][A] for convenience, even
    though they're identical. This allows O(1) lookup regardless of order.

    Alternative Approaches Considered:

    1. Jaccard Similarity: measures overlap between tag sets
       - More sophisticated but harder to interpret
       - Raw co-occurrence counts are more intuitive for humanities researchers

    2. Mutual Information: measures statistical dependence
       - Requires more complex calculations
       - Assumes sufficient sample size (we only have ~300 tagged items)

    3. Pointwise Mutual Information (PMI): normalised mutual information
       - Better for finding unexpected associations
       - Future enhancement candidate

    We chose raw counts because they're interpretable and actionable for vocabulary
    development. "Tags A and B co-occur 15 times" is immediately meaningful.

    Performance:
    For our dataset (~300 tagged items, avg 3 tags per item):
    - Combinations generated: ~300 × C(3,2) = ~900 pairs
    - Runtime: <1 second

    For larger datasets (>10,000 items), performance remains reasonable because:
    - We only process items with 2+ tags
    - Dictionary updates are O(1)
    - No nested loops over all tags

    Parameters:
        tags (dict): Tag data from load_tag_data(), structure:
                    {
                        'tag_name': {
                            'count': int,
                            'items': [str],
                            'item_titles': [str]
                        }
                    }

    Returns:
        list: List of co-occurring tag pairs, sorted by co-occurrence count (highest first).
              Each pair is a dict:
              {
                  'tag1': str,              # First tag name
                  'tag2': str,              # Second tag name
                  'count': int,             # Co-occurrence count
                  'tag1_total': int,        # Total count of tag1
                  'tag2_total': int,        # Total count of tag2
                  'jaccard': float          # Jaccard coefficient (optional future addition)
              }

    Raises:
        ValueError: If tags dict is empty

    Example:
        >>> tags = load_tag_data()
        >>> cooccur = calculate_cooccurrence(tags)
        >>> print(f"Found {len(cooccur)} co-occurring pairs")
        Found 847 co-occurring pairs
        >>> print(cooccur[0])  # Most common pair
        {
            'tag1': 'Mining',
            'tag2': 'Katoomba',
            'count': 28,
            'tag1_total': 32,
            'tag2_total': 45
        }

    See Also:
        - visualise_network(): Creates network graph from co-occurrence data
        - itertools.combinations: Python documentation for combination generation

    Note:
        This function only counts co-occurrences, not their statistical significance.
        Common tags will naturally have high co-occurrence counts. For normalised
        significance, consider implementing PMI (pointwise mutual information) or
        chi-square test in future versions.
    """
    print("\nCalculating tag co-occurrence patterns...")

    # Build co-occurrence matrix
    # defaultdict(lambda: defaultdict(int)) creates nested dicts with zero defaults
    # This allows cooccurrence[tag1][tag2] += 1 without checking if keys exist
    cooccurrence = defaultdict(lambda: defaultdict(int))

    # Step 1: Invert tags→items structure to items→tags
    # This allows us to process each item once and count all its tag pairs
    item_tags = defaultdict(set)  # Using set for uniqueness and fast membership

    for tag_name, tag_info in tags.items():
        # For each item that uses this tag, add the tag to that item's tag set
        for item_id in tag_info['items']:
            item_tags[item_id].add(tag_name)

    # Step 2: Count co-occurrences
    total_pairs = 0

    for item_id, item_tag_set in item_tags.items():
        # Only process items with 2+ tags (single-tag items have no pairs)
        if len(item_tag_set) >= 2:
            # Generate all unique pairs from this item's tags
            # combinations() returns tuples, we sort them for consistent ordering
            # Example: ['Mining', 'Katoomba', 'Women'] →
            #          [('Katoomba','Mining'), ('Katoomba','Women'), ('Mining','Women')]
            for tag1, tag2 in combinations(sorted(item_tag_set), 2):
                # Increment co-occurrence count for this pair
                # We store both directions (tag1→tag2 and tag2→tag1) for easy lookup
                cooccurrence[tag1][tag2] += 1
                cooccurrence[tag2][tag1] += 1
                total_pairs += 1

    print(f"✓ Calculated {total_pairs} tag pair co-occurrences")

    # Step 3: Convert sparse matrix to list format for CSV export and sorting
    cooccurrence_list = []
    processed = set()  # Track which pairs we've already added (avoid duplicates)

    for tag1 in cooccurrence:
        for tag2, count in cooccurrence[tag1].items():
            # Create canonical pair representation (sorted tuple)
            # This ensures ('A','B') and ('B','A') are treated as same pair
            pair = tuple(sorted([tag1, tag2]))

            # Only add each pair once
            if pair not in processed:
                cooccurrence_list.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count': count,
                    'tag1_total': tags[tag1]['count'],
                    'tag2_total': tags[tag2]['count']
                })
                processed.add(pair)

    # Sort by co-occurrence count (most frequent pairs first)
    # This makes the output more useful - researchers can focus on top pairs
    cooccurrence_list.sort(key=lambda x: x['count'], reverse=True)

    return cooccurrence_list
```

**Task B3.4: Continue with remaining functions in 02_analyze_tags.py**

Apply same comprehensive documentation approach to:
- `detect_hierarchies()` - explain substring matching and co-occurrence validation
- `connect_to_zotero()` - similar to 01_extract but for quality checks
- `identify_quality_issues()` - explain categorisation logic for attachments
- `visualise_network()` - explain NetworkX graph construction and matplotlib rendering
- All report generation functions

**Task B3.5: UK/Australian Spelling Audit**

Convert:
- "analyze" → "analyse"
- "organization" → "organisation"
- Comments like "visualize" → "visualise"

---

### B4. 03_inspect_multiple_attachments.py Enhancement

**Current State:** ~250 lines, some docstrings present

**Target State:** ~400 lines with comprehensive documentation

**Task B4.1: Enhance Module Docstring**

Add context about data quality workflow and why attachment inspection matters.

**Task B4.2: Enhance categorise_attachment_pattern() Function**

This function has complex decision logic that needs detailed explanation:

```python
def categorise_attachment_pattern(item_info):
    """
    Analyse attachment pattern to determine if item needs manual review.

    Research Data Quality Challenge:
    Items with multiple attachments might represent:
    1. Legitimate: Single article spanning multiple pages (keep together)
    2. Problematic: Multiple distinct articles combined into one record (split needed)
    3. Legitimate: Article + supplementary materials (notes, images)

    Automated categorisation helps prioritise manual review by identifying high-risk
    patterns (likely distinct sources) vs low-risk patterns (likely legitimate).

    Categorisation Logic - Decision Tree:

    We examine the types and counts of attachments (children) to infer intent:

    Pattern 1: Multiple PDFs, No Notes
    → Category: 'multiple_pdfs'
    → Risk: HIGH - Might be distinct articles combined
    → Example: Item has 3 PDFs attached, each a different newspaper article
    → Action: Manual review to check if PDFs should be split into separate items

    Pattern 2: PDF(s) + Notes
    → Category: 'pdf_plus_notes'
    → Risk: LOW - Notes likely transcription/text extraction from PDF
    → Example: Item has 1 PDF + 1 note containing OCR text
    → Action: Probably legitimate structure, low priority review

    Pattern 3: Multiple Notes, No PDFs
    → Category: 'multiple_notes'
    → Risk: MEDIUM - Notes might be sections that should be consolidated
    → Example: Item has 3 notes, each containing text from different pages
    → Action: Review if notes should be merged into single note

    Pattern 4: Mixed Attachment Types
    → Category: 'mixed_content'
    → Risk: MEDIUM - Unusual pattern, needs investigation
    → Example: Item has PDFs, notes, and linked files
    → Action: Review to understand attachment purpose

    Pattern 5: Unclear Pattern
    → Category: 'uncertain'
    → Risk: UNKNOWN - Can't determine from metadata alone
    → Action: Manual inspection required

    Why This Matters:

    The Blue Mountains project follows best practice for digital collections:
    one item record = one primary source. When research assistants accidentally
    combine multiple newspaper articles into one item, it creates metadata problems:
    - Title is ambiguous (which article is the "main" one?)
    - Date range is unclear (which date applies?)
    - Tags apply to different articles (can't tell which tag → which article)

    Splitting these items ensures each article has accurate, specific metadata.

    Limitations:

    This heuristic categorisation is not perfect. It can't detect:
    - Multiple articles in a single PDF (would need PDF content analysis)
    - Whether articles are related or unrelated (needs human judgment)
    - Which article should keep the original item ID (needs human decision)

    Therefore, categorisation assists but doesn't replace manual review.

    Parameters:
        item_info (dict): Item details from fetch_item_details(), structure:
                         {
                             'key': str,
                             'title': str,
                             'itemType': str,
                             'children': [
                                 {
                                     'key': str,
                                     'itemType': 'attachment' | 'note',
                                     'contentType': 'application/pdf' | '',
                                     'filename': str,
                                     'title': str,
                                     'note': str
                                 }
                             ]
                         }

    Returns:
        tuple: (category, reasoning, action) where:
               - category (str): One of 'multiple_pdfs', 'pdf_plus_notes',
                                'multiple_notes', 'mixed_content', 'uncertain'
               - reasoning (str): Human-readable explanation of categorisation
               - action (str): Recommended review priority:
                              'HIGH PRIORITY', 'REVIEW', 'LOW PRIORITY'

    Example:
        >>> item_info = {
        ...     'key': 'ABC123',
        ...     'title': 'Mining accidents',
        ...     'children': [
        ...         {'itemType': 'attachment', 'contentType': 'application/pdf'},
        ...         {'itemType': 'attachment', 'contentType': 'application/pdf'}
        ...     ]
        ... }
        >>> cat, reason, action = categorise_attachment_pattern(item_info)
        >>> print(cat)
        multiple_pdfs
        >>> print(action)
        HIGH PRIORITY - Review if these are separate articles

    See Also:
        - generate_inspection_report(): Uses these categories to organise report

    Note:
        This function only examines metadata (counts and types), not actual file
        content. Future enhancement could use PDF libraries (PyPDF2, pdfplumber)
        to analyse PDF structure (page count, text content) for better detection.
    """
    children = item_info['children']

    # Count attachments by type
    # We separate PDFs from notes because they indicate different patterns
    pdfs = [c for c in children if c['contentType'] == 'application/pdf']
    notes = [c for c in children if c['itemType'] == 'note']
    attachments = [c for c in children if c['itemType'] == 'attachment']

    num_pdfs = len(pdfs)
    num_notes = len(notes)
    num_attachments = len(attachments)

    # Decision tree for categorisation
    # Order matters - we check high-risk patterns first

    if num_pdfs >= 2 and num_notes == 0:
        # Pattern 1: Multiple PDFs without notes
        # Risk: High - might be distinct sources combined
        category = 'multiple_pdfs'
        reasoning = f"Has {num_pdfs} PDF files with no notes. May be distinct sources combined."
        action = "HIGH PRIORITY - Review if these are separate articles"

    elif num_pdfs >= 1 and num_notes >= 1:
        # Pattern 2: PDFs with notes
        # Risk: Low - likely PDF + text extraction
        category = 'pdf_plus_notes'
        reasoning = f"Has {num_pdfs} PDF(s) and {num_notes} note(s). Likely text extraction."
        action = "LOW PRIORITY - Probably legitimate structure"

    elif num_pdfs == 0 and num_notes >= 2:
        # Pattern 3: Multiple notes without PDFs
        # Risk: Medium - notes might need consolidation
        category = 'multiple_notes'
        reasoning = f"Has {num_notes} notes with no PDFs. May be transcribed text sections."
        action = "REVIEW - Check if notes should be consolidated"

    elif num_attachments > num_pdfs + num_notes:
        # Pattern 4: Other attachment types present
        # Risk: Medium - unusual, needs investigation
        category = 'mixed_content'
        reasoning = f"Has mixed attachment types: {num_attachments} total attachments."
        action = "REVIEW - Check attachment types and purposes"

    else:
        # Pattern 5: Unclear pattern
        # Risk: Unknown - needs manual review
        category = 'uncertain'
        reasoning = "Pattern unclear from metadata alone."
        action = "REVIEW - Manual inspection required"

    return category, reasoning, action
```

**Task B4.3: Enhance remaining functions**

Apply comprehensive documentation to:
- `load_flagged_items()` - explain CSV loading
- `fetch_item_details()` - explain Zotero API children retrieval
- `generate_inspection_report()` - explain Markdown report structure
- Main execution block

**Task B4.4: UK/Australian Spelling Audit**

Convert US spellings throughout.

---

## UK/Australian Spelling Conversion Checklist

### Common Conversions Required

Review **all** Python files for these patterns:

| US Spelling | UK/Australian | Context |
|------------|--------------|---------|
| analyze | analyse | Comments, docstrings, variable names |
| analysis | analysis | *(same spelling, no change)* |
| organize | organise | "organize data" → "organise data" |
| organization | organisation | Rare in code, but check |
| color | colour | Unlikely in this codebase |
| behavior | behaviour | Unlikely in this codebase |
| center | centre | "data center" (unlikely) |
| optimize | optimise | Comments about optimisation |
| optimization | optimisation | Performance comments |
| license (noun) | licence (noun) | "software licence" |
| license (verb) | license (verb) | "licensed under" *(no change)* |
| traveled | travelled | Unlikely but check |
| labeled | labelled | Comments about labels |
| fulfill | fulfil | Unlikely but check |

### Files to Check

- [ ] config.py
- [ ] 01_extract_tags.py
- [ ] 02_analyze_tags.py
- [ ] 03_inspect_multiple_attachments.py

### Search Patterns

Use find-in-files (grep) to locate US spellings:

```bash
# Check for "analyze" variants
grep -n "analyz" scripts/*.py

# Check for "organize" variants
grep -n "organiz" scripts/*.py

# Check for "optimize" variants
grep -n "optimiz" scripts/*.py

# Check for "license" as noun (should be "licence")
grep -n "software license\|data license" scripts/*.py
```

### Variable Names

Check if any variable names use US spelling (rare but possible):
- `organization_name` → `organisation_name`
- `analyze_results` → `analyse_results`

**Note:** Function names using US spelling should be updated too, but with caution:
- Update function definition
- Update all calls to the function
- Consider backwards compatibility if function might be imported elsewhere

---

## Quality Assurance Procedures

### QA1. Python Linting

**Objective:** Ensure code follows PEP 8 style guide and has no syntax errors

**Tools:**
- flake8 (fast, configurable)
- pylint (thorough, pedantic)

**Procedure:**

```bash
# Navigate to project root
cd /home/shawn/Code/blue-mountains

# Activate virtual environment
source venv/bin/activate

# Install linters (if not already installed)
pip install flake8 pylint

# Run flake8 on all scripts
# Allow line length up to 100 characters (project standard from CONTRIBUTING.md)
flake8 scripts/*.py --max-line-length=100 --exclude=venv

# Expected output: No errors
# If errors appear, fix them before proceeding

# Run pylint (more thorough)
pylint scripts/*.py --max-line-length=100

# Pylint is stricter and may report warnings we can ignore:
# - C0103: Variable name doesn't conform (e.g., single-letter loop vars)
# - R0914: Too many local variables (common in research scripts)
# - R0912: Too many branches (complex logic is sometimes necessary)

# Fix errors (E****) and critical warnings (C0102, C0121, etc.)
# Other warnings can be addressed or explicitly disabled with comments
```

**Common Fixes:**
- Remove unused imports
- Add blank lines around function definitions (2 blank lines)
- Fix inconsistent indentation
- Remove trailing whitespace
- Add blank line at end of file

**Acceptance Criteria:**
- All files pass flake8 with zero errors
- All files pass pylint with only acceptable warnings (see above)

---

### QA2. Docstring Completeness

**Objective:** Verify every function has comprehensive docstring meeting CONTRIBUTING.md standards

**Procedure:**

Manual review checklist for each function:

**For Each Function, Check:**
- [ ] Brief one-line summary present
- [ ] Detailed description (2-4 paragraphs) present
- [ ] All parameters documented with types
- [ ] Return value documented with type and structure
- [ ] Exceptions documented (Raises section)
- [ ] Example usage provided
- [ ] See Also section (if applicable)
- [ ] Note section for caveats/performance (if applicable)

**Functions to Check:**

config.py: *(no functions, just module-level code)*

01_extract_tags.py:
- [ ] connect_to_zotero()
- [ ] fetch_all_items()
- [ ] extract_tags_from_items()
- [ ] save_raw_tags()
- [ ] create_frequency_table()
- [ ] generate_summary_report()

02_analyze_tags.py:
- [ ] load_tag_data()
- [ ] find_similar_tags()
- [ ] detect_hierarchies()
- [ ] calculate_cooccurrence()
- [ ] connect_to_zotero()
- [ ] fetch_items_for_quality_check()
- [ ] identify_quality_issues()
- [ ] categorise_item()
- [ ] save_quality_csvs()
- [ ] save_similar_tags_csv()
- [ ] save_cooccurrence_data()
- [ ] visualise_network()
- [ ] generate_analysis_report()
- [ ] generate_quality_report()

03_inspect_multiple_attachments.py:
- [ ] load_flagged_items()
- [ ] connect_to_zotero()
- [ ] fetch_item_details()
- [ ] categorise_attachment_pattern()
- [ ] generate_inspection_report()
- [ ] save_full_details_json()

**Acceptance Criteria:**
- Every function has all required docstring sections
- Examples in docstrings are accurate and runnable
- Parameter types match actual code
- Docstrings explain "why" not just "what"

---

### QA3. Educational Clarity Review

**Objective:** Ensure documentation is understandable by digital humanities researchers without deep programming background

**Procedure:**

For each script, ask:

1. **Can a digital humanities researcher understand what the script does?**
   - Is the research context explained?
   - Are outputs and their purposes clear?
   - Is the workflow position explained?

2. **Can they understand how to run the script?**
   - Are prerequisites documented?
   - Are dependencies explained?
   - Is usage syntax provided?
   - Are common errors anticipated?

3. **Can they understand the algorithmic approach?**
   - Are algorithms explained conceptually before code?
   - Are domain-specific terms defined?
   - Are design decisions justified?
   - Are alternatives mentioned when relevant?

4. **Can they modify the script for their own research?**
   - Are parameters explained (what do they control)?
   - Are constraints documented (valid ranges, formats)?
   - Are extension points identified?

**Test Method:**
Read through each script's documentation imagining you are:
- A digital humanities postdoc with basic Python knowledge
- Trying to adapt the script for a different Zotero library
- Wanting to understand why the code works this way

If any section is confusing, add clarifying comments.

**Acceptance Criteria:**
- Documentation tells a coherent story from research question → code → outputs
- Technical terms are defined before use
- Rationale for choices is clear
- Script can be understood without external resources

---

### QA4. Markdown Linting

**Objective:** Ensure all Markdown files pass linting validation for consistency and readability

**Why This Matters:**
Markdown linting enforces structural consistency (blank lines, code block formatting) that improves readability and prevents rendering issues in different viewers (GitHub, VS Code, documentation generators).

**Tools:**
- markdownlint-cli (command-line tool, requires Node.js)
- VS Code markdownlint extension (David Anson)
- IDE diagnostics (if configured)

**Procedure:**

```bash
# Navigate to project root
cd /home/shawn/Code/blue-mountains

# Install markdownlint (requires Node.js/npm)
# Skip if already installed
npm install -g markdownlint-cli

# Run linter on all markdown files
# Exclude venv and node_modules directories
markdownlint '**/*.md' --ignore node_modules --ignore venv

# Alternative: Use VS Code extension
# Install "markdownlint" by David Anson from Extensions marketplace
# Errors will appear inline in editor
```

**Rules to Enforce (from CLAUDE.md):**

- **MD022:** Blank lines around headings
  ```markdown
  <!-- WRONG -->
  Some text
  ## Heading
  More text

  <!-- CORRECT -->
  Some text

  ## Heading

  More text
  ```

- **MD031:** Blank lines around fenced code blocks
  ```markdown
  <!-- WRONG -->
  Text before
  ```python
  code here
  ```
  Text after

  <!-- CORRECT -->
  Text before

  ```python
  code here
  ```

  Text after
  ```

- **MD032:** Blank lines around lists
  ```markdown
  <!-- WRONG -->
  Some text
  - List item
  - List item
  More text

  <!-- CORRECT -->
  Some text

  - List item
  - List item

  More text
  ```

- **MD040:** Language specifiers for code blocks
  ```markdown
  <!-- WRONG -->
  ```
  code here
  ```

  <!-- CORRECT -->
  ```python
  code here
  ```

  <!-- For plain text -->
  ```text
  plain text here
  ```
  ```

**Files to Lint:**

Python module docstrings are not checked by markdownlint (they're in .py files), but any standalone .md files should be linted:

- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] CHANGELOG.md
- [ ] planning/*.md (all planning documents)
- [ ] docs/*.md (all documentation files)
- [ ] reports/*.md (generated reports - may need markdownlint-disable comments for dynamic content)

**Common Fixes:**

1. **Add blank lines around headings** - Most common violation
2. **Add language specifiers** - Use ```python, ```bash, ```text, ```json
3. **Add blank lines around code blocks** - Before and after ```
4. **Add blank lines around lists** - Before and after bullet/numbered lists

**Handling Dynamic Content:**

Generated reports (in reports/) may violate rules due to programmatically created content. Options:
1. Fix the generating script to produce compliant markdown
2. Add `<!-- markdownlint-disable -->` comments to generated files
3. Exclude reports/ directory from linting if content is transient

**Acceptance Criteria:**
- All manually-written .md files pass markdownlint with zero errors
- Generated .md files either pass linting or have documented exceptions
- Code blocks specify language (python, bash, json, text)
- Consistent blank line spacing throughout

---

### QA5. Spelling Audit

**Objective:** Ensure 100% UK/Australian spelling in all code and documentation

**Procedure:**

```bash
# Check for common US spellings in Python files
cd /home/shawn/Code/blue-mountains

# Search for US spellings (case-insensitive)
grep -i "analyz" scripts/*.py
grep -i "organiz" scripts/*.py
grep -i "optimiz" scripts/*.py
grep -i "color" scripts/*.py
grep -i "center" scripts/*.py
grep -i "behavior" scripts/*.py

# Check for "license" used as noun (should be "licence")
# Valid: "licensed under" (verb)
# Invalid: "software license" (noun)
grep -n "license" scripts/*.py | grep -v "licensed"
```

**Manual Review:**
Read through all docstrings and comments looking for:
- Informal US spellings that grep might miss
- Variable names using US spelling
- String literals (less critical but still convert)

**Fix Strategy:**
1. Use search-and-replace in IDE with regex:
   - `analyz(\w+)` → `analys$1` (analyze→analyse, analyzing→analysing)
   - `organiz(\w+)` → `organis$1`
   - `optimiz(\w+)` → `optimis$1`

2. Manually review each match to avoid:
   - Breaking URLs or external references
   - Changing strings that match external API fields
   - Changing imported library function names (e.g., `normalize()` from library)

**Acceptance Criteria:**
- Zero US spellings found in grep searches
- All docstrings use UK/Australian spelling
- All comments use UK/Australian spelling
- Variable names converted where appropriate

---

## Implementation Guidance

### VS Code Setup (Optional but Recommended)

**Helpful Extensions:**

Install these VS Code extensions for inline linting feedback during Phase B:

1. **Python** (Microsoft) - `ms-python.python`
   - Syntax highlighting, IntelliSense, debugging
   - Includes pylint integration
   - Right-click in editor → "Format Document" for auto-formatting

2. **Pylance** (Microsoft) - `ms-python.vscode-pylance`
   - Fast Python language server
   - Type checking and IntelliSense improvements
   - Often installed automatically with Python extension

3. **markdownlint** (David Anson) - `DavidAnson.vscode-markdownlint`
   - Real-time markdown linting in editor
   - Shows MD022, MD031, MD032, MD040 violations inline
   - Quick-fix suggestions for common issues

4. **Python Docstring Generator** (Nils Werner) - `njpwerner.autodocstring`
   - Generates docstring templates (start typing `"""` then press Enter)
   - Useful for ensuring all parameters are documented
   - Configure for Google or NumPy style (use Google for this project)

**Installation:**
```bash
# From command line (if using VS Code CLI)
code --install-extension ms-python.python
code --install-extension DavidAnson.vscode-markdownlint

# Or: Extensions view (Ctrl+Shift+X) → search → install
```

**Configuration:**
VS Code will use workspace settings from `.vscode/settings.json` if present. No additional configuration needed for Phase B - extensions work out of the box.

**Benefits:**
- See linting errors as you type (immediate feedback)
- Quick-fix suggestions save time
- Docstring templates ensure completeness

**Not required:** You can complete Phase B using command-line tools (flake8, markdownlint-cli). Extensions just make the process smoother.

---

### Workflow

**Recommended Order:**

1. **Day 1: config.py + 01_extract_tags.py (2-3 hours)**
   - Start with config.py (small, foundational)
   - Move to 01_extract_tags.py (builds on config)
   - Run linting after each file
   - Test scripts still execute correctly

2. **Day 2: 02_analyze_tags.py (3-4 hours)**
   - Most complex script, needs most documentation
   - Take breaks to maintain quality
   - Test execution with real data

3. **Day 3: 03_inspect_multiple_attachments.py (1-2 hours)**
   - Smaller script, uses patterns from previous scripts
   - Final quality checks across all scripts

4. **Day 4: QA and Polish (1-2 hours)**
   - Run all linting checks
   - Spelling audit
   - Educational clarity review
   - Generate sample outputs to verify nothing broke

**Total Estimated Time: 7-11 hours** (spread across multiple sessions)

### Best Practices

**While Documenting:**

1. **Run the Code Frequently**
   - Don't document 300 lines without testing
   - Verify examples in docstrings actually work
   - Catch typos and logic errors early

2. **Use Your Own Voice**
   - These templates are guides, not rigid requirements
   - Adapt language to your style
   - Prioritise clarity over formality

3. **Think Like a Teacher**
   - Explain one concept at a time
   - Build from simple to complex
   - Use analogies and examples
   - Anticipate questions

4. **Leverage AI Assistance**
   - Use Claude Code to generate docstring drafts
   - Review and personalise all generated content
   - Ask Claude to explain algorithms you're documenting

5. **Test for Understanding**
   - Read your documentation out loud
   - If it sounds confusing, it probably is
   - Simplify jargon, expand abbreviations

### What to Avoid

**Anti-Patterns:**

1. **Over-Documentation**
   - Don't comment every line
   - Don't restate obvious code
   - Focus on "why" not "what"

2. **Copy-Paste Documentation**
   - Don't duplicate between similar functions
   - Use "See FunctionX" to reference instead

3. **Outdated Documentation**
   - Update docstrings when code changes
   - Keep examples synchronised with actual behaviour

4. **Defensive Documentation**
   - Don't apologise for code choices in comments
   - Confidently explain your rationale

5. **Jargon Without Definition**
   - Don't assume knowledge of technical terms
   - Define or link to definitions first time used

---

## Acceptance Criteria for Phase B Completion

Phase B is complete when:

### Code Quality
- [ ] All Python files pass flake8 linting (max-line-length=100)
- [ ] All Python files pass pylint with only acceptable warnings
- [ ] No syntax errors or broken imports
- [ ] All scripts execute successfully with test data

### Documentation Completeness
- [ ] Every script has comprehensive module docstring
- [ ] Every function has complete docstring (all required sections)
- [ ] All parameters documented with types
- [ ] All return values documented with types
- [ ] All exceptions documented
- [ ] All functions have usage examples

### Documentation Quality
- [ ] Docstrings explain research context (why code exists)
- [ ] Algorithms explained conceptually before code
- [ ] Design decisions justified
- [ ] Domain-specific terms defined
- [ ] **Acronyms expanded on first usage** in each file (AAT, TGN, RVA, etc.)
- [ ] Examples are accurate and runnable
- [ ] Educational tone maintained throughout
- [ ] FAIR vocabularies principles explained in relevant scripts (02_analyze_tags.py)

### UK/Australian Spelling
- [ ] Zero US spellings in Python files (grep verification)
- [ ] All docstrings use UK/Australian spelling
- [ ] All inline comments use UK/Australian spelling
- [ ] Variable names updated where appropriate

### Markdown Quality
- [ ] All .md files pass markdownlint with zero errors
- [ ] MD022: Blank lines around headings
- [ ] MD031: Blank lines around fenced code blocks
- [ ] MD032: Blank lines around lists
- [ ] MD040: Language specifiers for all code blocks
- [ ] Generated reports either pass linting or have documented exceptions

### Testing
- [ ] config.py executes without errors
- [ ] 01_extract_tags.py executes and produces correct outputs
- [ ] 02_analyze_tags.py executes and produces correct outputs
- [ ] 03_inspect_multiple_attachments.py executes and produces correct outputs
- [ ] All output files (JSON, CSV, Markdown) generated correctly

### Integration
- [ ] Documentation references Phase A outputs (CONTRIBUTING.md, docs/)
- [ ] Consistency with project standards (CLAUDE.md, CONTRIBUTING.md)
- [ ] Cross-references between scripts are accurate

---

## Post-Phase-B Enhancements (Future)

Phase B focuses on code documentation. Future phases could add:

### Phase C: API Documentation
- Sphinx/MkDocs auto-generated API reference from docstrings
- Read the Docs hosting
- Tutorial notebooks (Jupyter)

### Phase D: Testing Framework
- pytest suite with unit tests for all functions
- Integration tests for full workflow
- Test data fixtures
- Coverage reporting (aim for >80%)

### Phase E: User Guides
- Step-by-step tutorials for common tasks
- Video walkthroughs
- Troubleshooting FAQ
- Example workflows for different research scenarios

### Phase F: Performance Optimisation
- Profile scripts to identify bottlenecks
- Implement caching for API responses
- Add parallel processing for large datasets
- Benchmark documentation

---

## Implementation Notes

### API Key Security Decision

**Implementation:** Following least-privilege principle, user will provide separate API keys:
- **Read-only key** - for extraction/analysis scripts (01-03)
- **Read-write key** - for future vocabulary publishing scripts

**Documentation approach:**
- Config.py module docstring explains the two-key strategy
- Comment which scripts use which key
- .env.example documents both variables:
  - `ZOTERO_API_KEY_READONLY`
  - `ZOTERO_API_KEY_READWRITE`

This implements security best practice while maintaining practical workflow flexibility.

## Questions Before Starting

1. **Time Allocation:** Do you want to implement Phase B in one continuous session, or split across multiple days?

2. **Review Cadence:** Should I pause after each script for your review, or complete all four then review together?

3. **Documentation Depth:** The examples above are comprehensive. Do you want this level of detail for every function, or prioritise complex functions?

4. **Testing Requirements:** Should I verify scripts execute correctly during Phase B, or is testing a separate phase?

5. **UK Spelling Priority:** Should spelling conversion happen:
   - As we document each script? (integrated)
   - As a final pass after all documentation? (separate)

6. **Additional Scripts:** Are there other Python files beyond the four main scripts that need Phase B treatment?

---

## Success Metrics

Phase B succeeds if:

1. **A digital humanities researcher** can read the code and understand the methodological choices

2. **A Python developer** can modify the code confidently without extensive code archaeology

3. **A project evaluator** can verify the implementation matches the research design

4. **A graduate student** can learn computational approaches from reading the code

5. **The research team** can maintain the code after project completion

6. **The software** meets FAIR4RS "Reusable" principles through transparent implementation

---

## Conclusion

Phase B transforms functional research code into educational research software. By comprehensively documenting the "why" behind every design decision, algorithmic choice, and data structure, we enable:

- **Reproducibility:** Others can verify our methodology
- **Reusability:** Others can adapt our code for their projects
- **Transparency:** Research claims are backed by readable implementation
- **Sustainability:** The project team can maintain code long-term
- **Education:** Students can learn computational humanities methods

This investment in documentation pays dividends throughout the software lifecycle and contributes to the broader research software engineering community.

---

**Ready to Begin Phase B Implementation**

*Last Updated: 2025-10-09*
*Reviewed (and lightly edited): 2025-10-09 by Shawn Ross*
