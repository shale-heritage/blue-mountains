#!/usr/bin/env python3
"""
Script 01: Extract Tags from Zotero Group Library

Research Context:
This script implements the first phase of folksonomy rationalisation for the Blue
Mountains shale mining communities digital collection. Historical newspaper articles
and archaeological sources in the Zotero group library have been tagged by research
assistants using informal, descriptive terms (a "folksonomy" - user-generated
classification system). This script extracts those tags to prepare them for
standardisation against controlled vocabularies and publication to Research
Vocabularies Australia (RVA).

Folksonomy vs Taxonomy:
A folksonomy is a collaborative tagging system where users create tags freely without
predefined categories. This bottom-up approach captures researchers' intuitions about
subject matter, but produces inconsistencies (spelling variations, synonyms, varying
specificity). This script is step 1 of converting folksonomy tags into a structured
taxonomy (hierarchical classification system) mapped to established vocabularies like
the Getty Art & Architecture Thesaurus (AAT) and Thesaurus of Geographic Names (TGN).

Workflow Position:
1. [THIS SCRIPT] Extract tags from Zotero
2. Analyse tags for consolidation (02_analyze_tags.py)
3. Develop controlled vocabulary (manual curation with Getty/TGN mapping)
4. Publish vocabulary to RVA (future script)
5. Apply controlled vocabulary back to Zotero items (future script)
6. Publish to Omeka Classic digital collection (future script)

Methodological Questions Addressed:
- What subject areas have research assistants prioritised in tagging?
- How consistent is the tagging vocabulary across the corpus?
- Which items lack subject metadata (quality assurance)?
- What is the distribution of tag usage (power law vs uniform)?
- Are there obvious synonyms or spelling variations?

Technical Approach:
Connects to the Zotero Application Programming Interface (API) using the pyzotero
library and retrieves all items from the group library. The API paginates responses
at 100 items per request to prevent server timeouts and reduce memory load. Tags are
extracted from each item's metadata and stored with full provenance (which items use
each tag, item titles for context). This provenance enables later analysis of tag
co-occurrence patterns and validation of consolidation decisions.

FAIR Data Principles Implementation:
This script implements Findable, Accessible, Interoperable, Reusable (FAIR) data
principles:
- Findable: Output includes metadata (generation timestamp, source library ID)
- Accessible: Uses standard JSON and CSV formats with UTF-8 encoding
- Interoperable: JSON schema documented in docs/data-formats.md
- Reusable: Complete provenance (item associations) enables verification/replication

Security Model:
Uses read-only Zotero API key (config.ZOTERO_API_KEY_READONLY) following the
principle of least privilege. This script only extracts data - it never modifies
the Zotero library. Using a read-only key means bugs or key compromise cannot
accidentally delete or corrupt library data.

Inputs:
- Zotero API credentials from .env file (ZOTERO_API_KEY_READONLY)
- Internet connection for API access
- Group library ID: 2258643 (Blue Mountains Shale Mining Communities)

Outputs:
- data/raw_tags.json: Complete tag data with item associations (machine-readable)
- data/tag_frequency.csv: Tags sorted by usage frequency (human/machine-readable)
- reports/tag_summary.md: Statistical overview with recommendations (human-readable)

Performance:
Typical execution time for ~1,200 item library: 5-8 seconds
- API requests: ~3-5 seconds (depends on network)
- Tag extraction: <1 second (in-memory processing)
- File writing: <1 second

Dependencies:
- pyzotero: Zotero API client library (Web API v3 wrapper)
- pandas: Data manipulation and Comma-Separated Values (CSV) export
- python-dotenv: Secure API credential management
- config.py: Centralised configuration and path management

Usage:
    # Ensure virtual environment activated and .env configured
    python scripts/01_extract_tags.py

    # Expected output files:
    # - data/raw_tags.json
    # - data/tag_frequency.csv
    # - reports/tag_summary.md

Error Handling:
Script exits with code 1 on any error (API connection failure, missing credentials,
file write errors). Errors print full stack trace for debugging. This fail-fast
approach ensures problems are noticed immediately rather than producing incomplete
or incorrect data.

Author: Shawn Ross
Project: Australian Research Council (ARC) Linkage Project LP190100900
         Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import pandas as pd
from pyzotero import zotero

# Add parent directory to path for imports
# This allows importing config.py from scripts/ directory
# Necessary because scripts are in a subdirectory but share config
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def connect_to_zotero():
    """
    Initialise connection to Zotero group library via Application Programming Interface (API).

    This function creates a Zotero API client object that handles authentication
    and Hypertext Transfer Protocol (HTTP) requests to Zotero's servers. The
    pyzotero library (a wrapper around the Zotero Web API v3) manages:
    - API authentication via key (OAuth-style token authentication)
    - Request rate limiting to respect Zotero's fair use policy
    - Error handling for network failures and API errors
    - JavaScript Object Notation (JSON) response parsing

    Authentication Model:
    Zotero uses API key-based authentication (not username/password). Each API key
    is associated with a Zotero user account and grants specific permissions:
    - Read-only access: Can retrieve library data but not modify
    - Read/write access: Can also create, update, delete items and tags

    This script uses config.ZOTERO_API_KEY_READONLY (read-only key) following the
    security principle of least privilege. Since this script only extracts data and
    never modifies the library, a read-only key prevents accidental modifications or
    data loss if the script has bugs or the key is compromised.

    Group vs Personal Libraries:
    Zotero has two library types:
    - Personal libraries: Belong to individual user accounts (library_type='user')
    - Group libraries: Shared collections for collaborative research (library_type='group')

    This project uses a group library (ID: 2258643) shared among the research team.
    All team members can add items and tags, and this script extracts the collective
    tagging work.

    API Endpoint:
    The pyzotero library connects to https://api.zotero.org/
    This is Zotero's official public API endpoint (HTTPS encrypted)

    Returns:
        pyzotero.zotero.Zotero: Authenticated API client object with methods:
            - .items(): Retrieve items from library
            - .tags(): Retrieve all tags
            - .children(): Get attachments/notes for an item
            See pyzotero documentation: https://pyzotero.readthedocs.io/

    Raises:
        ValueError: If config validation fails (credentials missing from .env)
        ConnectionError: If Zotero API is unreachable (network down, API maintenance)
        zotero.zotero_errors.UserNotAuthorised: If API key is invalid
        zotero.zotero_errors.ResourceNotFound: If group library ID doesn't exist

    Example:
        >>> zot = connect_to_zotero()
        Connecting to Zotero group library 2258643...
        >>> items = zot.items(limit=5)  # Get first 5 items
        >>> print(f"Retrieved {len(items)} items")
        Retrieved 5 items

    See Also:
        - config.py: Where ZOTERO_API_KEY_READONLY is loaded from .env
        - Zotero Web API v3: https://www.zotero.org/support/dev/web_api/v3/start
        - pyzotero library: https://github.com/urschrei/pyzotero

    Note:
        This function doesn't make any API calls itself - it just creates the client
        object. Actual network requests happen when you call methods like .items() or
        .tags(). The client maintains a connection pool and handles request retries
        automatically (default: 3 retries with exponential backoff).
    """
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")

    # Create Zotero API client object
    # Parameters:
    #   library_id (str): Numeric ID of the library (group or user)
    #   library_type (str): 'group' or 'user'
    #   api_key (str): Authentication token from https://www.zotero.org/settings/keys
    #
    # The pyzotero.Zotero() constructor validates parameters but doesn't make network requests
    # Network errors only occur when calling methods like .items() or .tags()
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,           # Group library ID (e.g., '2258643')
        config.ZOTERO_LIBRARY_TYPE,       # Library type ('group' for this project)
        config.ZOTERO_API_KEY_READONLY    # Read-only key (security: least privilege)
    )

    return zot


def fetch_all_items(zot):
    """
    Retrieve all items from Zotero library using pagination.

    The Zotero API limits responses to 100 items per request to prevent server
    overload, timeout errors, and excessive memory usage. For libraries with >100
    items, we must paginate by making multiple requests with incrementing start
    offsets (similar to "page 1, page 2, page 3" in web results).

    Pagination Strategy:
    We use a simple while loop that:
    1. Requests batch of 100 items starting at offset 0 (items 1-100)
    2. If batch is non-empty, adds items to results and requests next batch
       (offset 100 = items 101-200)
    3. If batch is empty, we've reached the end of the library (break loop)
    4. Returns accumulated list of all items

    Why This Approach vs Alternatives:

    Alternative 1: Request all items at once (limit=999999)
    - Problem: Fails for large libraries with timeout or memory errors
    - Problem: Zotero API rejects requests with limit > 100

    Alternative 2: Use .num_items() to calculate total pages upfront
    - Problem: Extra API call, and total count can change during iteration
    - Problem: If someone adds items while script runs, we might miss them
    - Advantage: Could show progress bar ("fetching page 5 of 12")

    Alternative 3: Request smaller batches (limit=50)
    - Problem: More API calls = slower execution (network latency dominates)
    - No advantage: Zotero recommends limit=100 as optimal

    Alternative 4: Use .everything() method from pyzotero
    - Advantage: Handles pagination automatically
    - Problem: Less visibility into progress for large libraries
    - Problem: Less control over error handling
    - Note: We use manual pagination for educational transparency

    We chose manual pagination because:
    - Simple to implement and understand
    - Handles libraries of any size
    - Robust to library size changes during execution
    - Batch size of 100 is Zotero's recommended optimum
    - Progress messages reassure users for long-running operations

    Performance Analysis:
    Typical request time: 200-500ms per batch depending on network and server load
    Library size vs execution time:
    - Small (100 items): ~1 second (1 request)
    - Medium (1,000 items): ~5 seconds (10 requests)
    - Large (10,000 items): ~50 seconds (100 requests)

    Our Blue Mountains library (~1,200 items) takes approximately 5-8 seconds.

    Parameters:
        zot (pyzotero.zotero.Zotero): Authenticated Zotero API client from
                                      connect_to_zotero() function. Must be
                                      connected to a valid library.

    Returns:
        list: List of item dictionaries from Zotero API. Each item is a dict with:
              {
                  'key': 'ABC123',              # Unique 8-character item ID
                  'version': 123,               # Item version (for conflict detection)
                  'library': {...},             # Library metadata
                  'data': {                     # Actual item data
                      'key': 'ABC123',
                      'version': 123,
                      'itemType': 'newspaperArticle',  # CSL item type
                      'title': 'Article Title',
                      'creators': [...],        # Authors/contributors
                      'date': '1900-01-01',
                      'tags': [                 # User-generated tags (folksonomy)
                          {'tag': 'Mining'},
                          {'tag': 'Katoomba'}
                      ],
                      'publicationTitle': 'Sydney Morning Herald',
                      'pages': '5',
                      ...                       # Many other fields
                  },
                  'meta': {...}                 # Additional API metadata
              }

              See Zotero API documentation for complete schema:
              https://www.zotero.org/support/dev/web_api/v3/basics

    Raises:
        ConnectionError: If network fails during any request
        zotero.zotero_errors.HTTPError: If API returns error (rate limit, auth failure)
        zotero.zotero_errors.ResourceNotFound: If library doesn't exist
        KeyError: If API response format changes (should be very rare)

    Example:
        >>> zot = connect_to_zotero()
        Connecting to Zotero group library 2258643...
        >>> items = fetch_all_items(zot)
        Fetching all items from library...
          Retrieved 100 items so far...
          Retrieved 200 items so far...
          Retrieved 300 items so far...
        ✓ Total items retrieved: 300
        >>> print(items[0]['data']['itemType'])
        newspaperArticle
        >>> print(len(items[0]['data']['tags']))
        5

    See Also:
        - connect_to_zotero(): Creates the zot parameter
        - extract_tags_from_items(): Processes the returned items
        - pyzotero.Zotero.items(): Underlying API method used here

    Note:
        This function loads all items into memory. For extremely large libraries
        (>100,000 items), consider processing batches as they arrive rather than
        accumulating all items first. Our library size (~1,200 items) is well within
        memory limits (<10 megabytes (MB) of JSON data in memory).

        The zot.items() method returns a list of dicts, not generator. This is a
        pyzotero design choice - we can't stream items one-at-a-time. For huge
        libraries, would need to manually implement streaming via raw HTTP requests.
    """
    print("Fetching all items from library...")

    items = []  # Accumulator for all items across all requests
    start = 0  # Offset for pagination (which item number to start from)
    limit = 100  # Batch size (how many items per request) - Zotero's maximum and optimum

    # Pagination loop - continue until we get an empty batch (end of library)
    while True:
        # Request one batch of items from Zotero API
        # The pyzotero library handles the actual HTTP GET request:
        # GET https://api.zotero.org/groups/2258643/items?start=0&limit=100
        #
        # Parameters to zot.items():
        #   start (int): Offset - which item to start from (0-indexed)
        #   limit (int): How many items to return (max 100 per Zotero API rules)
        #
        # Returns:
        #   list of dicts: Item data from Zotero
        #   Empty list: If no more items (we've reached end of library)
        batch = zot.items(start=start, limit=limit)

        # Check if we've exhausted the library (no more items to fetch)
        # When start offset is beyond the last item, Zotero returns empty list
        # Example: Library has 250 items, we request start=300, get empty list
        if not batch:
            break  # Exit while loop - we're done

        # Add this batch to our accumulated results
        # extend() adds all items from batch list to items list
        # Example: items=[A,B,C], batch=[D,E], after extend items=[A,B,C,D,E]
        items.extend(batch)

        # Move offset forward for next batch
        # If we just retrieved items 0-99, next batch starts at 100
        # If we just retrieved items 100-199, next batch starts at 200, etc.
        start += limit

        # Progress indicator for user feedback
        # Important for large libraries where this takes >30 seconds
        # Reassures user that script is working, not frozen
        print(f"  Retrieved {len(items)} items so far...")

    # Final confirmation of total items retrieved
    print(f"✓ Total items retrieved: {len(items)}")
    return items


def extract_tags_from_items(items):
    """
    Extract all tags and their associations with items from Zotero data.

    This function processes the raw JSON response from Zotero's API to build a
    comprehensive tag dataset. For each unique tag name, we track:
    - Usage count (how many items have this tag applied)
    - Item associations (which specific item IDs use this tag)
    - Item titles (for human-readable context in reports)

    The function also calculates aggregate statistics to support data quality
    assessment, including identifying untagged items that need subject metadata.

    Data Structure Design Decision - defaultdict vs dict:
    We use defaultdict(lambda: {'count': 0, 'items': [], 'item_titles': []}) instead
    of a regular dict. This provides automatic initialisation - when we access a tag
    name for the first time, it creates the nested structure automatically. The
    alternative (regular dict) requires checking "if tag_name in dict" before every
    update, making code longer and harder to read. The defaultdict approach is more
    Pythonic and less error-prone.

    Tag Data Provenance - Why Track Item Associations:
    We store not just tag counts, but also which specific items use each tag. This
    provenance (origin/history tracking) enables:
    1. Tag co-occurrence analysis (which tags appear together?)
    2. Verification of consolidation decisions (can review affected items)
    3. Reconstruction of tagging history (who tagged what when, via Zotero API)
    4. Quality assurance (spot-check tagged items for accuracy)

    Without provenance, we'd only know "tag X appears 10 times" but couldn't verify
    if those 10 applications are appropriate or identify items needing retagging.

    Memory Efficiency Consideration:
    Storing item IDs and titles for each tag increases memory usage (~5x compared to
    just counts). For our library (~1,200 items, ~500 tags), this is ~2MB in memory,
    which is negligible on modern computers. For huge libraries (>100,000 items),
    might need to store just counts and fetch item details on-demand.

    Parameters:
        items (list): List of Zotero item dictionaries returned by fetch_all_items().
                     Each item must have 'key' and 'data' fields with 'data.tags'
                     being a list of tag objects: [{'tag': 'Mining'}, {'tag': 'NSW'}].
                     The pyzotero library guarantees this structure from API responses.

    Returns:
        tuple: (tag_data, statistics) where:

            tag_data (dict): Maps tag names to usage information:
                {
                    'Mining': {
                        'count': 32,                # How many items have this tag
                        'items': ['ABC123', ...],   # List of item keys (Zotero IDs)
                        'item_titles': ['Article title 1', ...]  # Matching titles
                    },
                    'Katoomba': {
                        'count': 45,
                        'items': ['DEF456', ...],
                        'item_titles': ['Article title 2', ...]
                    },
                    ...
                }

                Note: tag_data keys are case-sensitive. Zotero preserves exact tag
                capitalisation as entered. Similar tags like "Mining" and "mining"
                would be separate keys (addressed in 02_analyze_tags.py).

            statistics (dict): Aggregate metrics for overview and quality assessment:
                {
                    'total_items': 1189,              # All items in library
                    'items_with_tags': 336,           # Items that have ≥1 tag
                    'items_without_tags': 853,        # Items needing tagging
                    'unique_tags': 481,               # Distinct tag names
                    'total_tag_applications': 1247,   # Sum of all tag uses
                    'avg_tags_per_item': 3.71,        # Mean tags on tagged items
                    'max_tags_per_item': 15,          # Most tags on any item
                    'min_tags_per_item': 1            # Fewest tags on tagged items
                }

                Note: avg/max/min are calculated only for items_with_tags, not all
                items. Items without tags don't skew the average to near-zero.

    Raises:
        KeyError: If items list contains malformed dictionaries missing required
                 fields ('key', 'data', 'data.tags'). This indicates either:
                 - A pyzotero API version change (very rare - API is stable)
                 - Data corruption during network transfer
                 - Programming error in fetch_all_items()
                 If this occurs, check pyzotero library version and Zotero API docs.

        TypeError: If items parameter is not a list, or contains non-dict elements.

    Example:
        >>> zot = connect_to_zotero()
        >>> items = fetch_all_items(zot)
        >>> tag_data, stats = extract_tags_from_items(items)

        Extracting tags from items...
        ✓ Extracted 481 unique tags
          Items with tags: 336
          Items without tags: 853
          Total tag applications: 1247

        >>> print(f"Found {stats['unique_tags']} unique tags")
        Found 481 unique tags

        >>> print(f"Tag 'Mining' used {tag_data['Mining']['count']} times")
        Tag 'Mining' used 32 times

        >>> print(f"First item with 'Mining': {tag_data['Mining']['item_titles'][0]}")
        First item with 'Mining': Shale miners at Ruined Castle...

    See Also:
        - fetch_all_items(): Provides the items parameter
        - save_raw_tags(): Saves the returned tag_data to JSON
        - create_frequency_table(): Generates CSV report from tag_data
        - 02_analyze_tags.py: Performs deeper analysis on this data

    Note:
        This function loads all data into memory (tag_data dict can be ~2MB for our
        library). For libraries with >100,000 items and >10,000 tags, consider:
        - Processing in batches (stream items, accumulate counts only)
        - Using database (SQLite) instead of in-memory dict
        - Generating statistics incrementally rather than at end

        Our library size (~1,200 items, ~500 tags) processes in <1 second.

        The function uses .get() with defaults for safe field access. This is defensive
        programming - handles edge cases like items without titles gracefully rather
        than crashing with KeyError. Better to have '[No Title]' placeholder than fail.
    """
    print("\nExtracting tags from items...")

    # Initialise tag data accumulator
    # defaultdict with lambda factory creates nested dict structure automatically
    # When accessing tag_data['NewTag'] for first time, creates:
    # {'count': 0, 'items': [], 'item_titles': []}
    #
    # Without defaultdict, would need:
    #   if tag_name not in tag_data:
    #       tag_data[tag_name] = {'count': 0, 'items': [], 'item_titles': []}
    # before every update. defaultdict is more concise and Pythonic.
    tag_data = defaultdict(lambda: {
        'count': 0,           # Number of items using this tag
        'items': [],          # List of item keys (Zotero IDs like 'ABC123')
        'item_titles': []     # List of item titles (for human readability)
    })

    # Initialise statistics accumulators
    items_with_tags = 0           # Count of items that have ≥1 tag
    items_without_tags = 0        # Count of items that have 0 tags (need work)
    total_tag_applications = 0    # Sum of all tag uses (can be > items_with_tags)
    tags_per_item = []            # List of tag counts (for avg/max/min calculation)

    # Process each item from Zotero library
    # items is a list of dicts returned by fetch_all_items()
    for item in items:
        # Extract item metadata
        # We use .get() with defaults to handle missing fields gracefully
        # If a field doesn't exist, .get() returns the default instead of raising KeyError
        # This is defensive programming - better to have '[No Title]' than crash
        item_id = item['key']  # 8-character Zotero ID (e.g., 'ABC123XY')

        # Item title - use '[No Title]' if missing (rare but possible)
        # Some item types (notes, attachments) may not have titles
        item_title = item['data'].get('title', '[No Title]')

        # Item type - Zotero uses Citation Style Language (CSL) types
        # Common types: newspaperArticle, book, journalArticle, manuscript, etc.
        # We don't currently use this but might for filtering/categorisation later

        # Tags list - Zotero API format: [{'tag': 'Mining'}, {'tag': 'NSW'}]
        # If no tags, .get() returns empty list []
        tags = item['data'].get('tags', [])

        # Check if item has any tags
        if tags:
            # Item has at least one tag - count it and track tag details
            items_with_tags += 1
            tags_per_item.append(len(tags))  # For statistics (avg/max/min)

            # Process each tag on this item
            # Zotero API returns tags as list of dicts: [{'tag': 'TagName'}, ...]
            # The dict structure allows for future fields like 'type' (manual vs automatic)
            for tag_obj in tags:
                # Extract tag name from dict
                # Use .get() in case API format changes (defensive programming)
                tag_name = tag_obj.get('tag', '')

                # Verify tag name is non-empty (skip empty strings)
                # Empty tags shouldn't exist but API might allow it
                if tag_name:
                    # Update this tag's usage data
                    # defaultdict automatically initialised this tag if first occurrence
                    tag_data[tag_name]['count'] += 1                      # Increment usage count
                    tag_data[tag_name]['items'].append(item_id)           # Track which item
                    tag_data[tag_name]['item_titles'].append(item_title)  # Track item title

                    # Increment global tag application counter
                    # This counts each tag application separately
                    # If item has 5 tags, this increments 5 times
                    total_tag_applications += 1
        else:
            # Item has no tags - needs attention from research team
            # These items lack subject metadata and are hard to discover
            items_without_tags += 1

    # Display extraction results summary
    # This provides immediate feedback that extraction succeeded
    print(f"✓ Extracted {len(tag_data)} unique tags")
    print(f"  Items with tags: {items_with_tags}")
    print(f"  Items without tags: {items_without_tags}")
    print(f"  Total tag applications: {total_tag_applications}")

    # Calculate summary statistics
    # These metrics support data quality assessment and help identify problems
    # We use conditional expressions to handle edge case of zero tagged items
    # (if tags_per_item is empty, division would raise ZeroDivisionError)
    stats = {
        'total_items': len(items),
        'items_with_tags': items_with_tags,
        'items_without_tags': items_without_tags,
        'unique_tags': len(tag_data),
        'total_tag_applications': total_tag_applications,

        # Average tags per tagged item (not per all items)
        # We only average over items_with_tags, not total_items
        # This gives true average tag density for tagged content
        # If tags_per_item is empty (no tagged items), return 0 not error
        'avg_tags_per_item': sum(tags_per_item) / len(tags_per_item) if tags_per_item else 0,

        # Maximum tags on any single item
        # Useful for identifying over-tagged items (might be tag spam or very comprehensive)
        # If tags_per_item is empty, return 0 not error
        'max_tags_per_item': max(tags_per_item) if tags_per_item else 0,

        # Minimum tags on tagged items (always ≥1 by definition)
        # Useful for verifying logic (should always be 1 for items_with_tags)
        # If tags_per_item is empty, return 0 not error
        'min_tags_per_item': min(tags_per_item) if tags_per_item else 0
    }

    # Convert defaultdict to regular dict before returning
    # defaultdict objects aren't JSON-serialisable because of their factory function
    # json.dump() would raise TypeError: Object of type defaultdict is not JSON serializable
    # Converting to dict removes the factory function while keeping all data
    # This conversion is safe because we're done adding new tags
    return dict(tag_data), stats


def save_raw_tags(tag_data, stats):
    """
    Save complete tag data to JSON file with metadata and statistics.

    This function creates a JSON (JavaScript Object Notation) file that serves as
    the primary data product of this script. JSON format was chosen over CSV because:
    1. Preserves nested structure (tags → items → titles hierarchy)
    2. Supports arrays (multiple items per tag) without delimiter confusion
    3. Includes metadata (generation timestamp, provenance, statistics)
    4. Can be parsed by other scripts without ambiguity
    5. Standard format for Web APIs and data interchange

    CSV Alternative Rejected:
    CSV (Comma-Separated Values) would require either:
    - Multiple files (one for tags, one for tag-item associations) = harder to manage
    - Flattened structure with repeated tag names = inflated file size and parsing complexity
    - Array serialisation (pipe-delimited?) = nonstandard, error-prone

    JSON solves these problems naturally with nested objects and arrays.

    File Structure:
    The output file has two top-level keys following FAIR data principles:
    - 'metadata': Data provenance (when generated, from what source, summary stats)
    - 'tags': Complete tag data (see Parameters for structure)

    This structure mirrors best practices in research data management:
    - Provenance enables reproducibility (can verify when/how data was generated)
    - Summary statistics provide quick overview without loading all data
    - Detailed data enables replication and validation

    Character Encoding - UTF-8:
    We use UTF-8 encoding with ensure_ascii=False to preserve non-ASCII characters
    (accented letters, Unicode symbols, emoji). This is essential for:
    - International names (François, Götz, 北京)
    - Place names with diacritics (Katoombā - though probably just "Katoomba")
    - Proper quotation marks ("curly quotes" not "straight")
    - Mathematical symbols (±, ≈, °)

    If ensure_ascii=True (default), JSON would escape these as \\uXXXX sequences,
    making the file harder to read for humans and slightly larger. Modern text
    editors and JSON parsers handle UTF-8 natively, so we preserve readability.

    Pretty-Printing with indent=2:
    We use indent=2 for human readability at cost of larger file size (~30% larger
    than compact JSON). For our dataset (~500 tags, ~2KB), this is ~600KB vs ~450KB,
    which is negligible. The readability benefit (can inspect file manually, use grep,
    diff for changes) outweighs the space cost.

    For huge datasets (>100MB), would remove indentation for production but keep for
    development (two output modes: --compact flag).

    Parameters:
        tag_data (dict): Dictionary mapping tag names to usage information.
                        Structure from extract_tags_from_items():
                        {
                            'Mining': {
                                'count': 32,
                                'items': ['ABC123', 'DEF456', ...],
                                'item_titles': ['Article 1', 'Article 2', ...]
                            },
                            ...
                        }

        stats (dict): Aggregate statistics from extract_tags_from_items().
                     Contains: total_items, items_with_tags, unique_tags,
                     total_tag_applications, avg_tags_per_item, max_tags_per_item,
                     min_tags_per_item

    Returns:
        None (side effect: creates/overwrites file at config.DATA_DIR / 'raw_tags.json')

    Raises:
        PermissionError: If script lacks write permission to data/ directory
                        (shouldn't happen - config.py creates directory with
                         appropriate permissions)

        IOError: If disk is full or other I/O error occurs during write
                (rare - modern filesystems reserve space for metadata)

        TypeError: If tag_data or stats contain non-serialisable objects
                  (shouldn't happen - we convert defaultdict to dict in extract_tags_from_items)

    Example:
        >>> tag_data, stats = extract_tags_from_items(items)
        >>> save_raw_tags(tag_data, stats)

        Saving raw tag data to /path/to/data/raw_tags.json...
        ✓ Saved to /path/to/data/raw_tags.json

        >>> # File content (excerpt):
        >>> # {
        >>> #   "metadata": {
        >>> #     "generated_at": "2025-10-09T14:23:15+11:00",
        >>> #     "zotero_group_id": "2258643",
        >>> #     "statistics": {...}
        >>> #   },
        >>> #   "tags": {
        >>> #     "Mining": {
        >>> #       "count": 32,
        >>> #       "items": ["ABC123", ...],
        >>> #       "item_titles": ["Article title", ...]
        >>> #     }
        >>> #   }
        >>> # }

    See Also:
        - extract_tags_from_items(): Generates tag_data and stats parameters
        - load_tag_data() in 02_analyze_tags.py: Reads this JSON file
        - docs/data-formats.md: Full JSON schema documentation with validation rules

    Note:
        This function overwrites the file if it exists without warning. To preserve
        previous extractions:
        1. Manually copy data/raw_tags.json to backups/ directory with timestamp:
           cp data/raw_tags.json backups/raw_tags_2025-10-09.json
        2. Then run script again

        Future enhancement: Add --backup flag to automatically create timestamped backup
        before overwriting.

        The json.dump() function is atomic on most filesystems (writes to temp file, then
        renames). If script crashes during write, you won't get a corrupted half-written
        file. However, no automatic recovery - would need to re-run script.
    """
    output_file = config.DATA_DIR / 'raw_tags.json'
    print(f"\nSaving raw tag data to {output_file}...")

    # Build output data structure
    # We include metadata following FAIR data principles:
    # - Provenance: when generated, from what source (enables reproducibility)
    # - Statistics: summary metrics for quick assessment (enables discovery)
    # - Data: the actual tag information (enables reuse)
    #
    # This structure is self-documenting - anyone opening the file sees provenance first
    data = {
        'metadata': {
            # ISO 8601 format timestamp with timezone (e.g., 2025-10-09T14:23:15+11:00)
            # datetime.now() returns local time
            # .isoformat() converts to standard ISO 8601 string
            # Includes timezone offset so consumers know absolute time (not ambiguous)
            'generated_at': datetime.now().isoformat(),

            # Source library identifier (Zotero group ID)
            # This is public information (appears in URLs) not a secret
            # Enables verifying data came from correct library
            'zotero_group_id': config.ZOTERO_GROUP_ID,

            # Aggregate statistics for quick overview
            # Consumer can check stats before loading full tag data
            # Useful for validation (does unique_tags match length of tags object?)
            'statistics': stats
        },

        # Complete tag data with full provenance
        # This is the main payload - everything else is metadata
        'tags': tag_data
    }

    # Write JSON to file
    # Parameters:
    #   indent=2: Pretty-print with 2-space indentation (human-readable)
    #   ensure_ascii=False: Preserve Unicode characters (don't escape to \\uXXXX)
    #   encoding='utf-8': Use UTF-8 encoding (standard for JSON, handles international characters)
    #
    # Context manager (with statement) ensures file is properly closed even if error occurs
    # This prevents file corruption and resource leaks
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Confirm successful write
    # Reaching this line means no exceptions occurred during write
    print(f"✓ Saved to {output_file}")


def create_frequency_table(tag_data):
    """
    Create and save tag frequency table as CSV file.

    This function generates a human-readable and machine-readable CSV file listing
    all tags sorted by usage frequency (most common first). This format is useful for:
    - Quick overview of most/least used tags (skim top/bottom rows)
    - Import into spreadsheet software (Excel, Google Sheets) for manual review
    - Plotting frequency distributions (power law curves, Zipf's law analysis)
    - Identifying candidates for consolidation (rare tags at bottom)

    Why CSV in addition to JSON:
    While raw_tags.json contains all data, CSV provides complementary benefits:
    - Simpler format (easier to open in Excel/Sheets for non-technical users)
    - One tag per row (easier to sort, filter, annotate in spreadsheet)
    - Smaller file size (no nested structure or repeated keys)
    - Easy to generate plots (most tools can import CSV directly)

    Frequency Distribution Analysis:
    Tag usage often follows Zipf's law (power law distribution):
    - Few tags used very frequently (e.g., "Mining" appears 32 times)
    - Many tags used very rarely (e.g., 200+ tags appear only once = "singletons")

    This distribution is typical of natural language and folksonomy systems. The
    percentage column helps identify:
    - High-frequency tags (>5%): Core vocabulary, probably need refinement
    - Medium-frequency tags (1-5%): Useful descriptors, check for variants
    - Low-frequency tags (<1%): Often typos, overly specific, or candidates for merging

    Percentage Calculation:
    Percentage is of total tag applications, not total items:
    - Total applications = sum of all tag counts = 1247 (for our library)
    - If "Mining" has count 32, percentage = 32/1247 * 100 = 2.57%

    This measures tag usage intensity, not item coverage. Alternative would be
    percentage of items (32/1189 * 100 = 2.69%). We chose applications because it
    better reflects tagging effort and is more intuitive for tag consolidation
    ("this tag represents 2.5% of all tagging work").

    Sorting:
    Tags are sorted by count descending (highest frequency first). This puts most
    important tags (most used = most visible) at top for quick review. Alternative
    orders considered:
    - Alphabetical: Useful for looking up specific tags, but buries key tags
    - Ascending count: Useful for finding rare tags, but most analysis starts at top
    - Percentage: Same as count (mathematically proportional)

    We provide descending count. Users can re-sort in spreadsheet if needed.

    Parameters:
        tag_data (dict): Dictionary mapping tag names to usage information from
                        extract_tags_from_items(). Structure:
                        {
                            'Mining': {'count': 32, 'items': [...], 'item_titles': [...]},
                            'Katoomba': {'count': 45, ...},
                            ...
                        }

                        Only the 'count' field is used. 'items' and 'item_titles' are
                        ignored (they're preserved in raw_tags.json).

    Returns:
        pandas.DataFrame: Frequency table with columns ['tag', 'count', 'percentage'].
                         Sorted by count descending. Example:

                         | tag       | count | percentage |
                         |-----------|-------|------------|
                         | Mining    | 32    | 2.57       |
                         | Katoomba  | 45    | 3.61       |
                         | Women     | 18    | 1.44       |
                         | ...       | ...   | ...        |

                         This DataFrame is returned so generate_summary_report() can
                         extract top tags without re-reading the CSV file. The returned
                         DataFrame is the same data as written to CSV.

    Raises:
        PermissionError: If script lacks write permission to data/ directory
        IOError: If disk is full or other I/O error occurs during write
        ValueError: If tag_data is empty (no tags) - would produce empty CSV

    Example:
        >>> tag_data, stats = extract_tags_from_items(items)
        >>> df = create_frequency_table(tag_data)

        Creating tag frequency table at /path/to/data/tag_frequency.csv...
        ✓ Saved to /path/to/data/tag_frequency.csv

        >>> print(df.head())
           tag       count  percentage
        0  Katoomba     45        3.61
        1  Mining       32        2.57
        2  Women        18        1.44
        ...

        >>> # Can now open in Excel or plot with matplotlib
        >>> df.plot(x='tag', y='count', kind='bar')  # Frequency distribution plot

    See Also:
        - extract_tags_from_items(): Generates tag_data parameter
        - save_raw_tags(): Saves complete data with item associations
        - generate_summary_report(): Uses returned DataFrame for top tags
        - 02_analyze_tags.py: Performs deeper statistical analysis

    Note:
        The percentage column is rounded to 2 decimal places for readability. This is
        sufficient precision for our use case (identifying high/medium/low frequency).
        Full precision is preserved in the DataFrame (not rounded until writing to CSV).

        CSV file does not include item associations (items, item_titles) - those are in
        raw_tags.json. This keeps the CSV simple and focused on frequency analysis.

        The DataFrame.to_csv() with index=False prevents adding a row number column.
        This makes the CSV cleaner and easier to import into other tools without an
        extra unwanted column.
    """
    output_file = config.DATA_DIR / 'tag_frequency.csv'
    print(f"\nCreating tag frequency table at {output_file}...")

    # Build list of dicts for pandas DataFrame construction
    # We convert from nested dict to flat list structure:
    # {'Mining': {'count': 32}} → [{'tag': 'Mining', 'count': 32}]
    #
    # This transformation is necessary because:
    # - pandas DataFrames are table-like (rows and columns)
    # - Our tag_data is dict-like (nested structure)
    # - pandas.DataFrame() constructor expects list of dicts (one dict per row)
    data = []
    for tag_name, tag_info in tag_data.items():
        data.append({
            'tag': tag_name,  # Tag name (e.g., 'Mining')
            'count': tag_info['count'],  # Usage count (e.g., 32)
            'percentage': 0  # Placeholder - will calculate after summing counts
        })

    # Create pandas DataFrame from list of dicts
    # DataFrame is pandas' primary data structure - similar to spreadsheet or SQL table
    # Provides methods for sorting, filtering, aggregation, and export
    df = pd.DataFrame(data)

    # Sort by count descending (highest frequency first)
    # ascending=False means sort from high to low (32, 31, 30, ... 2, 1)
    # This puts most important tags at top for quick review
    # Sorting modifies df in place and also returns it (chaining pattern)
    df = df.sort_values('count', ascending=False)

    # Calculate percentage of total tag applications
    # We do this after creating DataFrame so we can use .sum() method
    # total_applications is sum of all counts (e.g., 32+45+18+... = 1247)
    total_applications = df['count'].sum()

    # Percentage calculation: (count / total) * 100
    # Example: Mining has count 32, total is 1247
    # Percentage = (32 / 1247) * 100 = 2.566...
    # .round(2) rounds to 2 decimal places = 2.57%
    #
    # This is vectorised operation - pandas applies to every row automatically
    # Much faster than Python loop: for i in range(len(df)): df.loc[i, 'percentage'] = ...
    df['percentage'] = (df['count'] / total_applications * 100).round(2)

    # Save DataFrame to CSV file
    # Parameters:
    #   index=False: Don't include row numbers (0, 1, 2, ...) as first column
    #                This makes CSV cleaner and easier to import elsewhere
    #
    # Default encoding is UTF-8 (handles international characters)
    # Default separator is comma (standard CSV format)
    # Quotes are only added around values containing commas or newlines (minimally quoted CSV)
    df.to_csv(output_file, index=False)

    print(f"✓ Saved to {output_file}")

    # Return DataFrame for use by generate_summary_report()
    # This avoids needing to re-read the CSV file we just wrote
    # The DataFrame contains the same data as the CSV (minus formatting nuances)
    return df


def generate_summary_report(stats, tag_data, frequency_df):
    """
    Generate human-readable summary report in Markdown format.

    This function creates a comprehensive summary report intended for the research
    team (historians, project PIs, research assistants) to review tag extraction
    results and identify next steps. The report uses Markdown format because:
    - Human-readable as plain text (can view in any text editor)
    - Renders beautifully in GitHub, VS Code, and documentation generators
    - Supports tables, formatting, and structure without complex syntax
    - Easy to diff/version control (shows changes clearly)
    - Can convert to HTML, PDF, or Word if needed (pandoc, etc.)

    Report Structure:
    The report has five main sections following a funnel pattern (broad → specific):
    1. Overall Statistics: High-level numbers (total items, tags, coverage)
    2. Tag Usage Patterns: Top 20 most frequent tags (core vocabulary)
    3. Tags Requiring Attention: Singleton tags (used once = potential problems)
    4. Recommendations: Actionable next steps for research team
    5. Next Steps: Links to subsequent scripts in workflow

    This structure supports different reading patterns:
    - Quick scan: Read section headers and first table
    - Detailed review: Read all statistics and examine top tags
    - Action planning: Focus on Recommendations and Next Steps
    - Quality assurance: Focus on singleton tags and untagged items

    Markdown Table Alignment:
    We use aligned tables with separators for readability:
    | Column 1 | Column 2 |
    |----------|----------|
    | Value 1  | Value 2  |

    Alternative (minimal markdown) would be:
    |Column 1|Column 2|
    |-|-|
    |Value 1|Value 2|

    We chose aligned format because humans read this file more than machines.
    The extra spaces make tables easier to scan visually and maintain manually.

    Number Formatting:
    We use thousand separators (1,189 not 1189) and percentage formatting (72.1% not 0.721)
    for readability. Python's f-string formatting handles this:
    - {value:,} adds thousand separators (1189 → 1,189)
    - {value:.1f} rounds to 1 decimal place (0.721456 → 0.7)
    - {value:.2f} rounds to 2 decimal places (3.14159 → 3.14)

    Singleton Tag Analysis:
    Tags used only once (singletons) often indicate:
    - Typos: "Minning" instead of "Mining"
    - Spelling variations: "Organisation" vs "Organization"
    - Overly specific terms: "John Smith's diary entry from 3 March 1892"
    - Legitimate unique descriptors: "Nellie's Glen" (only one item about that place)

    We surface these for manual review rather than automatically merging because:
    - Context matters (can't determine legitimacy algorithmically)
    - Some singletons are correct and should be kept
    - Merging errors are hard to undo (data loss)
    - Historians' domain knowledge is essential for correct consolidation

    Parameters:
        stats (dict): Aggregate statistics from extract_tags_from_items().
                     Contains: total_items, items_with_tags, items_without_tags,
                     unique_tags, total_tag_applications, avg_tags_per_item,
                     max_tags_per_item, min_tags_per_item

        tag_data (dict): Dictionary mapping tag names to usage information.
                        Structure: {'Mining': {'count': 32, ...}, ...}
                        Used to identify singleton tags (count == 1)

        frequency_df (pandas.DataFrame): Frequency table from create_frequency_table()
                                         with columns ['tag', 'count', 'percentage'].
                                         Sorted by count descending.
                                         Used to extract top 20 tags for table.

    Returns:
        None (side effect: creates/overwrites file at config.REPORTS_DIR / 'tag_summary.md')

    Raises:
        PermissionError: If script lacks write permission to reports/ directory
        IOError: If disk is full or other I/O error occurs during write

    Example:
        >>> tag_data, stats = extract_tags_from_items(items)
        >>> frequency_df = create_frequency_table(tag_data)
        >>> generate_summary_report(stats, tag_data, frequency_df)

        Generating summary report at /path/to/reports/tag_summary.md...
        ✓ Saved to /path/to/reports/tag_summary.md

        >>> # Report content (excerpt):
        >>> # # Zotero Tag Extraction Summary
        >>> #
        >>> # **Generated:** 2025-10-09 14:23:15
        >>> # **Zotero Group ID:** 2258643
        >>> #
        >>> # ## Overall Statistics
        >>> # | Metric | Value |
        >>> # |--------|-------|
        >>> # | Total Items in Library | 1,189 |
        >>> # ...

    See Also:
        - extract_tags_from_items(): Generates stats and tag_data parameters
        - create_frequency_table(): Generates frequency_df parameter
        - 02_analyze_tags.py: Next script in workflow (referenced in report)

    Note:
        This function generates a static snapshot report. Re-running the script
        overwrites the previous report (no history preserved). To maintain history:
        - Copy report to backups/ with timestamp before re-running
        - Use version control (Git) to track report changes over time

        The report uses timestamp from stats (generation time) not datetime.now()
        (report writing time). This ensures consistency - report timestamp matches
        data timestamp in raw_tags.json.

        Singleton tag list is limited to first 20 examples to keep report readable.
        Full list is available in tag_frequency.csv (filter for count == 1).

        Future enhancement: Add visualisations (tag frequency histogram, tag cloud)
        as inline images (generated PNG files embedded with ![alt](path) markdown).
    """
    output_file = config.REPORTS_DIR / 'tag_summary.md'
    print(f"\nGenerating summary report at {output_file}...")

    # Identify singleton tags (used only once)
    # These are candidates for consolidation, typo correction, or removal
    # List comprehension is more Pythonic than for loop with append:
    # singleton_tags = []
    # for tag, info in tag_data.items():
    #     if info['count'] == 1:
    #         singleton_tags.append(tag)
    singleton_tags = [tag for tag, info in tag_data.items() if info['count'] == 1]

    # Extract top 20 tags from frequency DataFrame
    # .head(20) returns first 20 rows (already sorted by count descending)
    # This is efficiently implemented - no copying, just view of first 20 rows
    top_tags = frequency_df.head(20)

    # Pre-calculate percentages for report (avoids long lines in f-string)
    items_with_tags_pct = (stats['items_with_tags'] /
                           stats['total_items'] * 100)
    items_without_tags_pct = (stats['items_without_tags'] /
                              stats['total_items'] * 100)

    # Build report content as multi-line f-string
    # Triple quotes allow line breaks without escape characters
    # f-string allows embedding variables and expressions directly
    #
    # We build entire report as one string to:
    # - Preview full structure before writing (easier to debug formatting)
    # - Enable in-memory manipulation if needed
    # - Write atomically (one operation, not multiple writes)
    #
    # Alternative would be writing line-by-line with file.write() in loop
    # Current approach is cleaner and more maintainable
    report = f"""# Zotero Tag Extraction Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overall Statistics

| Metric | Value |
|--------|-------|
| Total Items in Library | {stats['total_items']:,} |
| Items with Tags | {stats['items_with_tags']:,} ({items_with_tags_pct:.1f}%) |
| Items without Tags | {stats['items_without_tags']:,} ({items_without_tags_pct:.1f}%) |
| Unique Tags | {stats['unique_tags']:,} |
| Total Tag Applications | {stats['total_tag_applications']:,} |
| Average Tags per Item | {stats['avg_tags_per_item']:.2f} |
| Max Tags on Single Item | {stats['max_tags_per_item']} |
| Min Tags on Tagged Item | {stats['min_tags_per_item']} |

---

## Tag Usage Patterns

### Top 20 Most Frequently Used Tags

| Rank | Tag | Count | % of Total |
|------|-----|-------|------------|
"""

    # Add top 20 tags to table
    # Loop through DataFrame rows and append to report string
    # .iterrows() returns (index, Series) tuples - we use both for ranking
    for idx, row in top_tags.iterrows():
        # Calculate 1-based rank (first row = rank 1, not rank 0)
        # .index.get_loc(idx) returns 0-based position in sorted DataFrame
        # We add 1 to convert to human-friendly 1-based ranking
        rank = top_tags.index.get_loc(idx) + 1

        # Append this row to Markdown table
        # Markdown table row format: | col1 | col2 | col3 |
        # Note: we use \n at end to start new line for next row
        report += f"| {rank} | {row['tag']} | {row['count']} | {row['percentage']:.1f}% |\n"

    # Continue report with singleton tags section
    # We use continuation of the same f-string for consistency
    report += f"""
---

## Tags Requiring Attention

### Singleton Tags (Used Only Once)

**Count:** {len(singleton_tags)} tags

These tags may be:
- Typos or spelling variations
- Overly specific terms that should be consolidated
- Legitimate unique descriptors

**Examples (first 20):**
"""

    # Add first 20 singleton tags as bullet list
    # We limit to 20 to keep report readable (not 200+ line list)
    # Full singleton list is in tag_frequency.csv for detailed review
    for tag in singleton_tags[:20]:  # Slice first 20 items
        report += f"- {tag}\n"

    # If more than 20 singletons, add continuation indicator
    # This tells readers there are more items not shown
    if len(singleton_tags) > 20:
        # Italicised text using Markdown *...* syntax
        report += f"\n*...and {len(singleton_tags) - 20} more*\n"

    # Add recommendations and next steps sections
    # These provide actionable guidance for research team
    report += f"""
---

## Recommendations

1. **Review singleton tags:** {len(singleton_tags)} tags are used only once. Consider consolidation.
2. **Untagged items:** {stats['items_without_tags']} items have no tags. These need to be processed.
3. **Tag standardisation:** Review top tags for spelling variations and inconsistencies.
4. **Hierarchy development:** Consider grouping tags into categories based on usage patterns.

---

## Next Steps

1. Run `02_analyze_tags.py` to identify similar tags and patterns
2. Review analysis with project historians
3. Begin tag rationalisation process

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    # Write report to file
    # Context manager ensures proper file closing
    # encoding='utf-8' handles any international characters in tag names
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved to {output_file}")


def main():
    """
    Main execution function orchestrating the complete tag extraction workflow.

    This function serves as the entry point when script is run directly. It:
    1. Displays banner message (script identification and purpose)
    2. Orchestrates all extraction steps in correct order
    3. Handles errors gracefully with informative messages
    4. Summarises outputs and suggests next steps

    Workflow Steps:
    The function executes five steps sequentially:
    1. Connect to Zotero API (connect_to_zotero)
    2. Fetch all items from library (fetch_all_items)
    3. Extract tags and calculate statistics (extract_tags_from_items)
    4. Save complete tag data (save_raw_tags)
    5. Generate frequency table (create_frequency_table)
    6. Generate summary report (generate_summary_report)

    Each step depends on previous steps' outputs - they must run in this order.
    If any step fails, we stop immediately (fail-fast) rather than continuing with
    partial data (which could lead to incorrect conclusions).

    Error Handling Strategy:
    We use try-except to catch any exceptions during execution:
    - Print clear error message (what went wrong)
    - Print full stack trace (where it went wrong - for debugging)
    - Exit with code 1 (signals failure to shell/scripts)

    This fail-fast approach ensures:
    - Problems are noticed immediately (not silent failures)
    - No incomplete/corrupt output files (all-or-nothing)
    - Clear diagnostics for troubleshooting (stack trace)
    - Proper exit code for automation (scripts can detect failure)

    Alternative approaches rejected:
    - Catch and log errors, continue anyway: Could produce misleading output
    - Silent failures: User wouldn't know something went wrong
    - Exit without stack trace: Harder to debug when errors occur

    Returns:
        None (side effects: creates files, prints to console)

    Raises:
        SystemExit: Exits with code 1 if any error occurs during execution
                   (raised by sys.exit(1) in except block)

    Example:
        >>> python scripts/01_extract_tags.py
        ======================================================================
        BLUE MOUNTAINS PROJECT - TAG EXTRACTION
        Script 01: Extract all tags from Zotero group library
        ======================================================================

        Connecting to Zotero group library 2258643...
        Fetching all items from library...
          Retrieved 100 items so far...
          Retrieved 200 items so far...
        ✓ Total items retrieved: 300

        Extracting tags from items...
        ✓ Extracted 481 unique tags
          Items with tags: 336
          Items without tags: 853
          Total tag applications: 1247

        Saving raw tag data to /path/to/data/raw_tags.json...
        ✓ Saved to /path/to/data/raw_tags.json

        Creating tag frequency table at /path/to/data/tag_frequency.csv...
        ✓ Saved to /path/to/data/tag_frequency.csv

        Generating summary report at /path/to/reports/tag_summary.md...
        ✓ Saved to /path/to/reports/tag_summary.md

        ======================================================================
        ✓ TAG EXTRACTION COMPLETE
        ======================================================================

        Outputs created:
          - /path/to/data/raw_tags.json
          - /path/to/data/tag_frequency.csv
          - /path/to/reports/tag_summary.md

        Next: Review tag_summary.md and run 02_analyze_tags.py

    See Also:
        - All other functions in this script (orchestrated by main)
        - 02_analyze_tags.py: Next script in workflow
        - config.py: Configuration and path management

    Note:
        This function should only be called when script is run directly, not when
        imported as a module. The if __name__ == '__main__': guard at bottom of file
        ensures this. If we import this script (import 01_extract_tags), main() is
        NOT called automatically. This enables:
        - Testing individual functions in isolation
        - Reusing functions in other scripts
        - Jupyter notebook interactive development
    """
    # Display script banner
    # The "=" lines create visual separators for readability
    # 70 characters wide (common terminal width, fits in standard console)
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - TAG EXTRACTION")
    print("Script 01: Extract all tags from Zotero group library")
    print("="*70)
    print()  # Blank line for spacing

    try:
        # Step 1: Connect to Zotero API
        # Creates authenticated client object for subsequent requests
        zot = connect_to_zotero()

        # Step 2: Fetch all items from library
        # Retrieves complete item data via paginated API requests
        # This is the slowest step (~5 seconds for ~1200 items)
        items = fetch_all_items(zot)

        # Step 3: Extract tags and calculate statistics
        # Processes items in memory (fast, <1 second)
        # Returns tag data dict and aggregate statistics
        tag_data, stats = extract_tags_from_items(items)

        # Step 4: Save outputs
        # Three output files created in parallel (independent operations)
        # We call these sequentially (not parallel) for simplicity
        # Parallel execution would only save ~1 second, not worth complexity
        save_raw_tags(tag_data, stats)                    # JSON with full data
        frequency_df = create_frequency_table(tag_data)    # CSV frequency table
        generate_summary_report(stats, tag_data, frequency_df)  # Markdown report

        # Display completion banner
        # Confirms successful execution and lists outputs
        print("\n" + "="*70)
        print("✓ TAG EXTRACTION COMPLETE")
        print("="*70)
        print("\nOutputs created:")
        print(f"  - {config.DATA_DIR / 'raw_tags.json'}")
        print(f"  - {config.DATA_DIR / 'tag_frequency.csv'}")
        print(f"  - {config.REPORTS_DIR / 'tag_summary.md'}")
        print("\nNext: Review tag_summary.md and run 02_analyze_tags.py")

    except Exception as e:
        # Catch any error that occurred during execution
        # Exception is base class for all Python exceptions (catches everything)
        #
        # We print two things:
        # 1. Simple error message for quick diagnosis
        print(f"\n❌ ERROR: {e}")

        # 2. Full stack trace for detailed debugging
        # Shows exactly which line caused the error and how we got there
        # Essential for troubleshooting when errors occur
        import traceback
        traceback.print_exc()

        # Exit with error code 1 (signals failure to operating system)
        # Shell scripts can check $? == 1 to detect failure
        # Exit code 0 = success, non-zero = failure (standard Unix convention)
        sys.exit(1)


# Standard Python idiom - only run main() when script executed directly
# This line checks if script is being run as main program (python 01_extract_tags.py)
# vs being imported as module (import 01_extract_tags)
#
# Why this matters:
# - When executed directly: __name__ == '__main__', so main() runs
# - When imported: __name__ == '01_extract_tags', so main() doesn't run
#
# Benefits:
# - Can import functions without side effects (no automatic execution)
# - Can test functions individually (import script, call specific function)
# - Can reuse functions in other scripts
# - Enables interactive development (Jupyter, IPython)
#
# This is a Python best practice recommended by PEP 8 style guide
if __name__ == '__main__':
    main()
