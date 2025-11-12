#!/usr/bin/env python3
"""
Add synonym mappings for unqualified variants of qualified taxonomy terms.

PROBLEM:
- 26 tags in Zotero lack parenthetical qualifiers (e.g., "Carrington Hotel")
- Taxonomy has qualified versions (e.g., "Carrington Hotel (building)")
- These tags will be lost when applying taxonomy

SOLUTION:
- Map unqualified → qualified for all specific entities
- Handle "Primary source" metadata tag separately (should probably be excluded from subject taxonomy)
"""

import json
import csv
import shutil
from datetime import datetime
from collections import defaultdict

# Load Zotero export
print("Loading Zotero export...")
with open('data/zotero_full_export.json', 'r') as f:
    zotero_data = json.load(f)

zotero_tags = set()
tag_frequency = defaultdict(int)

for item in zotero_data['items']:
    for tag in item.get('tags', []):
        zotero_tags.add(tag)
        tag_frequency[tag] += 1

# Load taxonomy
print("Loading taxonomy...")
rows = []
with open('data/tag_map_consolidated.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

existing_tags = {row['old_tag'] for row in rows}

# Create backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'data/tag_map_consolidated.csv.backup_{timestamp}'
shutil.copy2('data/tag_map_consolidated.csv', backup_file)
print(f"✓ Created backup: {backup_file}")

# Define mappings for unqualified → qualified
# These are based on the remaining 26 unmapped tags
unqualified_mappings = {
    # Specific named entities - all map to (building) qualified versions
    'Carrington Hotel': 'Carrington Hotel (building)',
    'Megalong Hotel': 'Megalong Hotel (building)',
    'Imperial Hotel': 'Imperial Hotel (building)',
    'Katoomba Hotel': 'Katoomba Hotel (building)',
    'Centennial Hotel': 'Centennial Hotel (building)',
    'Montrose House': 'Montrose House (building)',
    'Railway Hotel': 'Railway Hotel (building)',
    'Belgravia Hotel': 'Belgravia Hotel (building)',
    'Wentworth Falls Hotel': 'Wentworth Falls Hotel (building)',
    "Hoffman's House": "Hoffman's House (building)",
    'Katoomba Family Hotel': 'Katoomba Family Hotel (building)',

    # Churches - map to (organisation) for historical newspaper context
    'Church': 'church (organisation)',
    'Katoomba Congregational Church': 'Katoomba Congregational Church (organisation)',
    'Wesleyan Church': 'Wesleyan Church (organisation)',
    "St Hilda's Church": "St Hilda's Church of England (organisation)",
    'Methodist Church': 'Methodist Church (organisation)',
    'Roman Catholic Church': 'Roman Catholic Church (organisation)',

    # Mining - map to (facility) qualified versions
    'Megalong Shale Mines': 'Megalong Shale Mines (facility)',
    'Katoomba coal mines': 'Katoomba Coal Mines (facility)',
    'Coal mine': 'coal mine (facility)',
    "Nellie's Glen Shale Mine": "Nellie's Glen Shale Mine (facility)",
    'Katoomba Shale Mine': 'Katoomba Shale Mine (facility)',

    # Activities/substances
    'Alcohol': 'alcohol',  # Lowercase exists in taxonomy
}

# Find which of these are actually unmapped
new_mappings = []
for unqual, qual in unqualified_mappings.items():
    if unqual in zotero_tags and unqual not in existing_tags:
        # Verify target exists
        if qual in existing_tags:
            new_mappings.append({
                'old_tag': unqual,
                'new_tag': qual,
                'action': 'synonym',
                'notes': 'Unqualified variant from original Zotero tags',
                'parent_broader_category': '',
                'frequency': tag_frequency[unqual]
            })
        else:
            print(f"⚠️  Warning: Target '{qual}' not found for '{unqual}'")

# Sort by frequency
new_mappings.sort(key=lambda x: x['frequency'], reverse=True)

print(f"\nAdding {len(new_mappings)} unqualified → qualified mappings")

# Add to rows
new_rows = rows.copy()
for mapping in new_mappings:
    freq = mapping.pop('frequency')
    new_rows.append(mapping)

# Sort alphabetically
new_rows.sort(key=lambda x: x['old_tag'].lower())

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("UNQUALIFIED → QUALIFIED SYNONYM MAPPINGS")
print("="*80)

print(f"\nAdded {len(new_mappings)} synonym mappings:\n")

for i, mapping in enumerate(new_mappings, 1):
    freq = tag_frequency[mapping['old_tag']]
    print(f"{i:2d}. \"{mapping['old_tag']}\" → \"{mapping['new_tag']}\" ({freq} items)")

print(f"\nRows: {len(rows)} → {len(new_rows)} (added: {len(new_mappings)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

# Handle Primary source separately
if 'Primary source' in zotero_tags:
    freq = tag_frequency['Primary source']
    print("\n" + "="*80)
    print("SPECIAL CASE: Primary source")
    print("="*80)
    print(f"\n'Primary source' is used on {freq} items")
    print("This is a metadata flag, not a subject tag.")
    print("\nOptions:")
    print("1. Exclude from subject taxonomy (recommended)")
    print("2. Map to a metadata category if you create one")
    print("3. Remove from Zotero items (it's already tracked in item type)")
