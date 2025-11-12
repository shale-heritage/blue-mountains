#!/usr/bin/env python3
"""
Add synonym mappings for all case sensitivity variations.

PROBLEM:
- 99 tags in Zotero have capitalization (e.g., "Hotels", "Death", "Court")
- Taxonomy only has lowercase versions (e.g., "hotels", "death", "court")
- When applying taxonomy, 99 tags affecting hundreds of items will be lost

SOLUTION:
- Create synonym mappings: "Hotels" → "hotels (businesses)", "Death" → "death", etc.
- Handle special cases where capitalized form should map to specific qualified term
"""

import json
import csv
import shutil
from datetime import datetime
from collections import defaultdict

# Load Zotero export to get exact case
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

# Build mapping of what exists
existing_tags = {row['old_tag'] for row in rows}
hierarchy_tags = {row['old_tag']: row for row in rows if row['action'] == 'hierarchy'}

# Create backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'data/tag_map_consolidated.csv.backup_{timestamp}'
shutil.copy2('data/tag_map_consolidated.csv', backup_file)
print(f"✓ Created backup: {backup_file}")

# Find case sensitivity issues
case_mappings = []
special_cases = {
    # Capitalized tags that should map to qualified terms
    'Hotels': 'hotels (businesses)',
    'Church': 'church (organisation)',
    'Carrington Hotel': 'Carrington Hotel (building)',
    'Megalong Hotel': 'Megalong Hotel (building)',
    'Wesleyan Church': 'Wesleyan Church (organisation)',
    'Katoomba Congregational Church': 'Katoomba Congregational Church (organisation)',
    'School of Arts': 'school of arts',  # Generic
    'School': 'school',  # Generic
}

for ztag in zotero_tags:
    if ztag not in existing_tags:
        ztag_lower = ztag.lower()

        # Check if lowercase version exists
        if ztag_lower in existing_tags:
            # Determine target based on special cases or lowercase default
            target = special_cases.get(ztag, ztag_lower)

            case_mappings.append({
                'old_tag': ztag,
                'new_tag': target,
                'action': 'synonym',
                'notes': 'Capitalized variant from original Zotero tags',
                'parent_broader_category': '',
                'frequency': tag_frequency[ztag]
            })

# Sort by frequency for review
case_mappings.sort(key=lambda x: x['frequency'], reverse=True)

print(f"\nFound {len(case_mappings)} case sensitivity mappings to add")

# Add to rows
new_rows = rows.copy()
for mapping in case_mappings:
    # Remove frequency before adding to CSV
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
print("CASE SENSITIVITY SYNONYM MAPPINGS")
print("="*80)

print(f"\nAdded {len(case_mappings)} synonym mappings:\n")

for i, mapping in enumerate(case_mappings[:30], 1):
    freq = tag_frequency[mapping['old_tag']]
    print(f"{i:2d}. \"{mapping['old_tag']}\" → \"{mapping['new_tag']}\" ({freq} items)")

if len(case_mappings) > 30:
    print(f"\n... and {len(case_mappings) - 30} more")

print(f"\nRows: {len(rows)} → {len(new_rows)} (added: {len(case_mappings)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

# Calculate remaining unmapped
unmapped_count = len([t for t in zotero_tags if t not in existing_tags and t.lower() not in existing_tags])

print("\n" + "="*80)
print("REMAINING UNMAPPED TAGS")
print("="*80)
print(f"\nAfter adding case sensitivity synonyms:")
print(f"  Unmapped tags remaining: {unmapped_count}")
print(f"  (These need manual review - likely truly missing from taxonomy)")
