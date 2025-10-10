# API Integration Guide

**Project:** Blue Mountains Shale Mining Communities Digital Collection Software
**Purpose:** Guide to using Zotero and Omeka Classic APIs
**Last Updated:** 2025-10-10

---

## Overview

This guide documents how the Blue Mountains Digital Collection Software integrates with the Zotero API for bibliographic data management and the Omeka Classic API for digital collection publishing.

### APIs Used

1. **Zotero Web API** (v3) - *Currently implemented*
   - Tag extraction from group library
   - Item metadata retrieval
   - Attachment inspection
   - Authentication: API key
   - Documentation: <https://www.zotero.org/support/dev/web_api/v3/start>

2. **Omeka Classic API** - *Implementation in progress (Phase 4)*
   - Item publishing to digital collection
   - Metadata mapping from Zotero
   - Authentication: API key
   - Documentation: <https://omeka.org/classic/docs/Reference/api/>

### Design Philosophy

This project uses read-only API access for data extraction (scripts 01-03) following the **principle of least privilege** for security. Future vocabulary publishing scripts will use read-write access to both Zotero and Omeka.

---

## Zotero API Authentication

### Generating API Keys

1. **Navigate to:** <https://www.zotero.org/settings/keys>
2. **Click:** "Create new private key"

3. **For read-only scripts (01-03):**
   - Name: "Blue Mountains - Read Only"
   - Permissions:
     - Allow library access: **Read Only**
     - Allow notes access: **No**
     - Allow write access: **No**
   - Library access: Select "Blue Mountains" group library (ID: 2258643)
   - Click "Save Key"
   - **Copy key immediately** (shown only once)

4. **For future read-write scripts (vocabulary publishing):**
   - Name: "Blue Mountains - Read Write"
   - Permissions:
     - Allow library access: **Read/Write**
     - Allow notes access: **No**
   - Library access: Select "Blue Mountains" group library (ID: 2258643)
   - Click "Save Key"
   - **Copy key immediately**

### Configuring Zotero API Keys

Add keys to `.env` file in project root (never commit this file):

```bash
# Required for all scripts
ZOTERO_GROUP_ID=2258643
ZOTERO_LIBRARY_TYPE=group

# Read-only key (scripts 01-03)
ZOTERO_API_KEY_READONLY=your_readonly_key_here

# Read-write key (future scripts)
ZOTERO_API_KEY_READWRITE=your_readwrite_key_here
```

### Security Best Practices

1. **Never commit `.env` file** - Listed in .gitignore, contains secrets
2. **Use separate keys for read/write** - Limits damage if key compromised
3. **Regenerate compromised keys immediately** - At <https://www.zotero.org/settings/keys>
4. **Rotate keys periodically** - Consider annual rotation for long-running projects
5. **Don't print keys in logs** - config.py only confirms "Available", never shows key

---

## Zotero API Usage Patterns

### Initialising the Zotero Client

All scripts use the pyzotero library via config.py:

```python
from pyzotero import zotero
import config

# For read-only scripts (01-03)
zot = zotero.Zotero(
    config.ZOTERO_GROUP_ID,
    config.ZOTERO_LIBRARY_TYPE,
    config.ZOTERO_API_KEY_READONLY
)

# For future read-write scripts
zot = zotero.Zotero(
    config.ZOTERO_GROUP_ID,
    config.ZOTERO_LIBRARY_TYPE,
    config.ZOTERO_API_KEY_READWRITE
)
```

### Pagination Pattern

Zotero API limits responses to 100 items maximum. Always implement pagination for retrieving all items:

```python
def fetch_all_items(zot):
    """
    Retrieve all items from Zotero library using pagination.

    The Zotero API returns maximum 100 items per request. This function
    implements pagination to retrieve complete library contents regardless
    of size.

    Parameters:
        zot: Authenticated Zotero client instance

    Returns:
        list: All items from library, combining paginated responses

    Performance:
        ~1,200 item library = 12 API requests = ~2-5 minutes
        Network latency is primary factor, not computation
    """
    items = []
    start = 0
    limit = 100  # Zotero API maximum

    print(f"Fetching items from Zotero (group {zot.library_id})...")

    while True:
        # Retrieve batch starting at 'start' index
        batch = zot.items(start=start, limit=limit)

        # Empty batch indicates we've retrieved all items
        if not batch:
            break

        items.extend(batch)
        print(f"  Retrieved {len(items)} items so far...")

        # Move to next batch
        start += limit

    print(f"✓ Retrieved {len(items)} total items")
    return items
```

**Why pagination matters:**

- Prevents timeout on large libraries (>100 items)
- Reduces memory usage (process in batches if needed)
- Provides progress feedback for long operations
- Matches Zotero API's design (batch retrieval)

### Tag Extraction Pattern

Extract tags with item associations for folksonomy analysis:

```python
def extract_tags_with_items(zot):
    """
    Extract all tags from library with full item associations.

    Returns:
        dict: {
            'tag_name': {
                'count': int,
                'items': [item_keys],
                'item_titles': [titles]
            }
        }
    """
    from collections import defaultdict

    # defaultdict avoids KeyError when first encountering a tag
    # Initialises to empty dict with count/items/item_titles structure
    tags = defaultdict(lambda: {'count': 0, 'items': [], 'item_titles': []})

    # Get all items (using pagination pattern above)
    items = fetch_all_items(zot)

    for item in items:
        # Skip items without tags (not all items are tagged)
        if 'data' not in item or 'tags' not in item['data']:
            continue

        item_key = item['key']
        item_title = item['data'].get('title', 'Untitled')

        # Each item can have multiple tags
        for tag_obj in item['data']['tags']:
            tag_name = tag_obj['tag']

            # Record this item uses this tag
            tags[tag_name]['count'] += 1
            tags[tag_name]['items'].append(item_key)
            tags[tag_name]['item_titles'].append(item_title)

    # Convert defaultdict to regular dict for JSON serialisation
    return dict(tags)
```

### Retrieving Item Children (Attachments/Notes)

For quality inspection (Script 03):

```python
def get_item_with_children(zot, item_key):
    """
    Retrieve item with all children (attachments, notes).

    Parameters:
        zot: Authenticated Zotero client
        item_key (str): Zotero item key (8-character alphanumeric)

    Returns:
        dict: Item with 'children' key containing attachments/notes

    Note:
        Separate API call required for children - not included in
        standard item retrieval for performance reasons
    """
    # Get parent item
    item = zot.item(item_key)

    # Get children (attachments, notes)
    # This is a separate API call - only retrieve when needed
    children = zot.children(item_key)

    # Combine for analysis
    item['children'] = children

    return item
```

---

## Error Handling and Rate Limiting

### Common API Errors

#### 1. Authentication Failures (403 Forbidden)

```python
from pyzotero.zotero_errors import UserNotAuthorised

try:
    items = zot.items()
except UserNotAuthorised:
    print("ERROR: Zotero API key is invalid or lacks required permissions")
    print("Solutions:")
    print("  1. Regenerate key at https://www.zotero.org/settings/keys")
    print("  2. Ensure 'Allow library access' permission is checked")
    print("  3. Ensure correct group library is selected")
    print("  4. Update .env file with new key")
    sys.exit(1)
```

#### 2. Network Errors (Connection Failures)

```python
from requests.exceptions import ConnectionError, Timeout

try:
    items = zot.items()
except ConnectionError:
    print("ERROR: Cannot connect to Zotero API")
    print("Solutions:")
    print("  1. Check internet connection: ping api.zotero.org")
    print("  2. Check firewall/proxy settings")
    print("  3. Verify Zotero API status: https://status.zotero.org/")
    print("  4. Wait 5 minutes and retry (temporary API issues)")
    sys.exit(1)
except Timeout:
    print("WARNING: Zotero API request timed out")
    print("  Retrying with longer timeout...")
    # Implement retry with exponential backoff
```

#### 3. Rate Limiting (429 Too Many Requests)

Zotero API rate limits (as of 2025):

- Unauthenticated: 5 requests per second
- Authenticated: 10 requests per second per key

**Best practices:**

1. Batch requests where possible (items in groups of 100)
2. Add delays between large batches
3. Implement exponential backoff on 429 errors

```python
import time
from requests.exceptions import HTTPError

def fetch_with_retry(zot, max_retries=3):
    """
    Fetch items with automatic retry on rate limiting.

    Implements exponential backoff: wait 1s, 2s, 4s between retries
    """
    for attempt in range(max_retries):
        try:
            return zot.items()
        except HTTPError as e:
            if e.response.status_code == 429:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential: 1, 2, 4 seconds
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("ERROR: Rate limit exceeded after retries")
                    raise
            else:
                raise
```

### Handling Deleted Items

Zotero API may return deleted items in some queries:

```python
def filter_active_items(items):
    """
    Remove deleted items from results.

    Deleted items have 'deleted': 1 in metadata but may still
    appear in API responses for syncing purposes.
    """
    return [item for item in items if item['data'].get('deleted', 0) != 1]
```

---

## Data Provenance and Timestamps

### Recording API Retrieval Metadata

All generated files include provenance metadata:

```python
import datetime

def create_metadata():
    """
    Generate metadata block for JSON outputs.

    Provides data provenance for reproducibility and citation.
    """
    return {
        "generated_at": datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=11))
        ).isoformat(),  # Australian Eastern Time (UTC+11 for AEDT)
        "zotero_group_id": config.ZOTERO_GROUP_ID,
        "zotero_library_type": config.ZOTERO_LIBRARY_TYPE,
        "script_version": "0.1.0",  # From CHANGELOG.md
        "api_version": "Zotero API v3"
    }

# Include in all JSON outputs
output_data = {
    "metadata": create_metadata(),
    "tags": extracted_tags,
    # ... rest of data
}
```

### Library Version Detection

Detect if library has changed since last extraction:

```python
def check_library_version(zot, previous_metadata):
    """
    Compare current library state to previous extraction.

    Returns:
        tuple: (bool changed, str message)
    """
    # Count current items
    current_count = zot.num_items()

    # Get previous count from metadata
    previous_count = previous_metadata.get('statistics', {}).get('total_items', 0)

    if current_count != previous_count:
        return (True, f"Library changed: {previous_count} → {current_count} items")
    else:
        return (False, f"Library unchanged: {current_count} items")
```

---

## Omeka Classic API Integration

### Overview

Omeka Classic provides a REST API for managing digital collection items, files, and metadata. This project uses Omeka Classic to publish controlled vocabulary-tagged items from Zotero.

**Implementation Status:** Phase 4 (planned)

**Site Details:**

- **Production site:** <https://shaleheritage.au/>
- **API endpoint:** <https://shaleheritage.au/api>
- **Maximum results per page:** 50 (configured in Omeka settings)
- **Authentication:** API key (all permissions - Omeka doesn't support read-only keys)

### Authentication Setup

Omeka Classic uses API keys generated in the admin panel:

1. **Navigate to:** Omeka admin panel → Users → API Keys
2. **Generate key:** Associated with your user account
3. **Copy key:** Save to `.env` file immediately

**Add to `.env`:**

```bash
# Omeka Classic API configuration
OMEKA_API_URL=https://shaleheritage.au/api
OMEKA_API_KEY=your_omeka_key_here
```

**Security note:** Omeka Classic API keys inherit all user permissions. There is no read-only key option, so protect this key carefully. Consider creating a dedicated user account with minimal permissions for API access.

### Pagination Pattern

Omeka Classic API uses `page` parameter for pagination (unlike Zotero's `start` parameter):

```python
import requests

def fetch_all_omeka_items(api_url, api_key, per_page=50):
    """
    Retrieve all items from Omeka Classic using pagination.

    Parameters:
        api_url (str): Omeka API endpoint (e.g., https://shaleheritage.au/api)
        api_key (str): Omeka API key
        per_page (int): Results per page (max 50 for this site)

    Returns:
        list: All items from Omeka collection
    """
    items = []
    page = 1

    while True:
        # Construct request
        response = requests.get(
            f"{api_url}/items",
            params={'key': api_key, 'page': page, 'per_page': per_page}
        )

        # Check for errors
        response.raise_for_status()

        # Parse JSON response
        batch = response.json()

        # Empty batch indicates we've retrieved all items
        if not batch:
            break

        items.extend(batch)
        print(f"  Retrieved {len(items)} items so far...")

        page += 1

    print(f"✓ Retrieved {len(items)} total items from Omeka")
    return items
```

### Publishing Items to Omeka

**Planned implementation for Phase 4:**

```python
def publish_to_omeka(zotero_item, omeka_url, omeka_key):
    """
    Publish Zotero item to Omeka Classic collection.

    Maps Zotero metadata fields to Omeka Dublin Core elements.

    Parameters:
        zotero_item (dict): Zotero item with controlled vocabulary tags
        omeka_url (str): Omeka API endpoint
        omeka_key (str): Omeka API key

    Returns:
        dict: Created Omeka item response

    Note:
        Implementation planned for Phase 4 (Omeka Classic Publication)
    """
    # Map Zotero → Dublin Core
    # See docs/vocabularies.md for complete Dublin Core mapping
    dc_metadata = {
        'Dublin Core': {
            'Title': [{
                'text': zotero_item['data'].get('title', 'Untitled'),
                'html': False
            }],
            'Date': [{
                'text': zotero_item['data'].get('date', ''),
                'html': False
            }],
            'Subject': [
                {'text': tag['tag'], 'html': False}
                for tag in zotero_item['data'].get('tags', [])
            ],
            'Description': [{
                'text': zotero_item['data'].get('abstractNote', ''),
                'html': True
            }],
            'Creator': [{
                'text': format_creator(creator),
                'html': False
            } for creator in zotero_item['data'].get('creators', [])],
            'Source': [{
                'text': zotero_item['data'].get('publicationTitle', ''),
                'html': False
            }],
            'Type': [{
                'text': zotero_item['data'].get('itemType', ''),
                'html': False
            }],
            'Identifier': [{
                'text': zotero_item['key'],
                'html': False
            }]
        }
    }

    # POST to Omeka API
    response = requests.post(
        f"{omeka_url}/items",
        headers={'X-Omeka-Key': omeka_key},
        json={'element_texts': dc_metadata, 'public': True, 'featured': False}
    )

    response.raise_for_status()
    return response.json()


def format_creator(creator):
    """
    Format Zotero creator as string for Dublin Core.

    Parameters:
        creator (dict): Zotero creator object

    Returns:
        str: Formatted creator name
    """
    if 'name' in creator:
        return creator['name']
    else:
        return f"{creator.get('lastName', '')}, {creator.get('firstName', '')}"
```

### Omeka API Error Handling

```python
def omeka_request_with_retry(url, api_key, method='GET', data=None, max_retries=3):
    """
    Make Omeka API request with automatic retry.

    Parameters:
        url (str): Full API endpoint URL
        api_key (str): Omeka API key
        method (str): HTTP method (GET, POST, PUT, DELETE)
        data (dict): Request payload for POST/PUT
        max_retries (int): Maximum retry attempts

    Returns:
        dict: JSON response from Omeka

    Raises:
        requests.HTTPError: After max retries exceeded
    """
    import time

    for attempt in range(max_retries):
        try:
            if method == 'GET':
                response = requests.get(url, params={'key': api_key})
            elif method == 'POST':
                response = requests.post(
                    url,
                    headers={'X-Omeka-Key': api_key},
                    json=data
                )
            elif method == 'PUT':
                response = requests.put(
                    url,
                    headers={'X-Omeka-Key': api_key},
                    json=data
                )
            elif method == 'DELETE':
                response = requests.delete(url, params={'key': api_key})

            response.raise_for_status()
            return response.json() if response.content else {}

        except requests.HTTPError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Omeka API error {e.response.status_code}. "
                      f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                print(f"ERROR: Omeka API request failed after {max_retries} attempts")
                raise
```

### Reference Documentation

- **Omeka Classic API:** <https://omeka.org/classic/docs/Reference/api/>
- **Dublin Core Mapping:** docs/vocabularies.md (completed in Phase A)
- **Shale Heritage site:** <https://shaleheritage.au/>

---

## Testing API Integration

### Zotero Connection Test

Test Zotero API connection without retrieving data:

```bash
python scripts/config.py
```

Expected output:

```text
✓ Configuration loaded successfully
  Zotero Group ID: 2258643
  Library Type: group
  Read-only API key: Available
  Read-write API key: Available
```

### Zotero Item Count Test

```python
# Quick test script (can add to config.py)
if __name__ == "__main__":
    from pyzotero import zotero

    print("\nTesting Zotero API connection...")

    try:
        zot = zotero.Zotero(
            ZOTERO_GROUP_ID,
            ZOTERO_LIBRARY_TYPE,
            ZOTERO_API_KEY_READONLY
        )

        count = zot.num_items()
        print(f"✓ Connected successfully")
        print(f"  Library contains {count} items")

    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)
```

### Zotero Full Extraction Test

```bash
# Full test of extraction workflow
python scripts/01_extract_tags.py
```

Verify outputs:

- data/raw_tags.json created (~500KB)
- data/tag_frequency.csv created (~30KB)
- reports/tag_summary.md created
- No errors in console output

### Omeka Connection Test (Future)

```python
# Test Omeka API connection (Phase 4)
import requests

def test_omeka_connection(api_url, api_key):
    """
    Test Omeka Classic API connection.

    Returns:
        bool: True if connection successful
    """
    try:
        response = requests.get(
            f"{api_url}/items",
            params={'key': api_key, 'per_page': 1}
        )
        response.raise_for_status()

        print(f"✓ Connected to Omeka at {api_url}")
        items = response.json()
        print(f"  Sample item retrieved: {len(items)} item(s)")
        return True

    except requests.HTTPError as e:
        print(f"✗ Omeka connection failed: {e}")
        print(f"  Status code: {e.response.status_code}")
        return False
    except Exception as e:
        print(f"✗ Omeka connection failed: {e}")
        return False


# Run test
if __name__ == "__main__":
    import config
    test_omeka_connection(config.OMEKA_API_URL, config.OMEKA_API_KEY)
```

---

## Performance Considerations

### Zotero API Performance

**Typical timings for ~1,200 item library:**

- Tag extraction (script 01): 2-5 minutes
  - 12 API requests (100 items each)
  - Network latency dominant factor
  - Progress indicators every 100 items

- Tag analysis (script 02): 5-10 minutes
  - Initial extraction: same as above
  - Fuzzy matching: <1 second (with python-Levenshtein)
  - Network analysis: ~2 seconds
  - Visualisation generation: ~1 second

- Attachment inspection (script 03): 1-3 minutes
  - Depends on number of flagged items
  - One API call per flagged item
  - Typically 20-50 items flagged

**Optimisation strategies:**

1. **Cache Zotero data locally** - Scripts 02-03 can reuse data from script 01 without re-fetching
2. **Use python-Levenshtein** - 10-30× faster fuzzy matching than pure Python
3. **Batch operations** - Retrieve 100 items per request rather than one-by-one
4. **Progress indicators** - Inform user of long-running operations

### Omeka API Performance (Future)

**Expected timings:**

- Publishing 1,000 items to Omeka: ~30-60 minutes
  - One POST request per item
  - Includes file upload for PDFs
  - Rate limiting depends on server configuration

**Optimisation strategies:**

1. **Batch metadata updates** - Use Omeka API batch operations where available
2. **Parallel uploads** - Consider threading for file uploads (with rate limiting)
3. **Incremental publishing** - Only publish changed items, not entire library
4. **Progress tracking** - Save publish state to resume interrupted operations

---

## See Also

- **scripts/README.md:** Script execution guide and workflow
- **docs/data-formats.md:** JSON schemas for API response storage
- **docs/vocabularies.md:** Controlled vocabulary development and mappings
- **CONTRIBUTING.md:** Code standards for API integration code

---

## Questions?

- **Zotero API issues:** <https://forums.zotero.org/>
- **Omeka API issues:** <https://forum.omeka.org/>
- **API key problems (Zotero):** Regenerate at <https://www.zotero.org/settings/keys>
- **API key problems (Omeka):** Regenerate in Omeka admin panel → Users → API Keys
- **Connection errors:** Check scripts/README.md troubleshooting section
