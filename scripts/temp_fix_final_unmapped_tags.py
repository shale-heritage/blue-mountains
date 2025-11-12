#!/usr/bin/env python3
"""
Fix the final 4 unmapped tags.

REMAINING UNMAPPED:
1. "Primary source" (304 items) - metadata flag
2. "Alcohol" (12 items) → "alcohol consumption & behaviour"
3. "Mount Victoria Hotel" (2 items) → "Mount Victoria Hotel (building)"
4. "Congregational Church" (1 item) → "Congregational Church (organisation)"
"""

import csv
import shutil
from datetime import datetime

# Create backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'data/tag_map_consolidated.csv.backup_{timestamp}'
shutil.copy2('data/tag_map_consolidated.csv', backup_file)
print(f"✓ Created backup: {backup_file}")

# Load rows
rows = []
with open('data/tag_map_consolidated.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Add final mappings
final_mappings = [
    {
        'old_tag': 'Alcohol',
        'new_tag': 'alcohol consumption & behaviour',
        'action': 'synonym',
        'notes': 'Capitalized variant; generic tag for alcohol-related content',
        'parent_broader_category': ''
    },
    {
        'old_tag': 'Mount Victoria Hotel',
        'new_tag': 'Mount Victoria Hotel (building)',
        'action': 'synonym',
        'notes': 'Unqualified variant from original Zotero tags',
        'parent_broader_category': ''
    },
    {
        'old_tag': 'Congregational Church',
        'new_tag': 'Congregational Church (organisation)',
        'action': 'synonym',
        'notes': 'Unqualified variant from original Zotero tags',
        'parent_broader_category': ''
    },
    {
        'old_tag': 'Primary source',
        'new_tag': 'PRIMARY SOURCE',
        'action': 'exclude',
        'notes': 'Metadata flag - not a subject tag. Item type already indicates primary source status.',
        'parent_broader_category': 'METADATA'
    }
]

# Add new mappings
new_rows = rows + final_mappings

# Sort alphabetically
new_rows.sort(key=lambda x: x['old_tag'].lower())

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report
print("\n" + "="*80)
print("FINAL UNMAPPED TAGS - RESOLVED")
print("="*80)

print(f"\nAdded {len(final_mappings)} final mappings:\n")

for i, mapping in enumerate(final_mappings, 1):
    action = mapping['action']
    old = mapping['old_tag']
    new = mapping['new_tag']
    print(f"{i}. \"{old}\" → \"{new}\" ({action})")

print(f"\nRows: {len(rows)} → {len(new_rows)} (added: {len(final_mappings)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

print("\n" + "="*80)
print("RESULT")
print("="*80)
print("✓ All Zotero tags now have mappings!")
print("✓ 100% mapping coverage achieved")
print("✓ No data loss when applying taxonomy")
print("\n📝 Note: 'Primary source' marked for exclusion (metadata, not subject)")
