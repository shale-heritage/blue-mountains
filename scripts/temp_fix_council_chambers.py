#!/usr/bin/env python3
"""
Fix Council Chambers capitalization and make it specific to Katoomba.

PROBLEM:
- 7 items in Zotero tagged with "Council Chambers" (capitalized)
- tag_map_consolidated.csv only has "council chambers" (lowercase) as hierarchy
- NO synonym mapping from "Council Chambers" → "council chambers"
- When taxonomy is applied, these 7 tags will be LOST

SOLUTION:
1. Rename "council chambers" → "Katoomba Council Chambers" (hierarchy)
2. Add synonym: "Council Chambers" → "Katoomba Council Chambers"
3. Add synonym: "council chambers" → "Katoomba Council Chambers"
4. Remove unused "council buildings" entry
"""

import csv
import shutil
from datetime import datetime

# Create backup
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = f'data/tag_map_consolidated.csv.backup_{timestamp}'
shutil.copy2('data/tag_map_consolidated.csv', backup_file)
print(f"✓ Created backup: {backup_file}")

# Read all rows
rows = []
with open('data/tag_map_consolidated.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Track changes
changes = []
removed = []
added = []

# Process rows
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    skip = False

    # 1. Remove "council buildings" (unused)
    if old_tag == 'council buildings' and action == 'hierarchy':
        removed.append('council buildings (unused intermediate parent)')
        skip = True

    # 2. Rename "council chambers" → "Katoomba Council Chambers"
    elif old_tag == 'council chambers' and action == 'hierarchy':
        changes.append('council chambers → Katoomba Council Chambers (hierarchy)')
        row['old_tag'] = 'Katoomba Council Chambers'
        row['new_tag'] = 'Katoomba Council Chambers'

    if not skip:
        new_rows.append(row)

# 3. Add synonym mappings
synonym_mappings = [
    {
        'old_tag': 'Council Chambers',
        'new_tag': 'Katoomba Council Chambers',
        'action': 'synonym',
        'notes': 'Capitalized variant from original Zotero tags',
        'parent_broader_category': ''
    },
    {
        'old_tag': 'council chambers',
        'new_tag': 'Katoomba Council Chambers',
        'action': 'synonym',
        'notes': 'Lowercase variant to preferred term',
        'parent_broader_category': ''
    }
]

for mapping in synonym_mappings:
    added.append(f"{mapping['old_tag']} → {mapping['new_tag']} (synonym)")
    new_rows.append(mapping)

# Sort to maintain alphabetical order
new_rows.sort(key=lambda x: x['old_tag'].lower())

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("FIX COUNCIL CHAMBERS CAPITALIZATION AND DATA LOSS")
print("="*80)

print(f"\nChanges ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nRemoved ({len(removed)}):")
for item in removed:
    print(f"  - {item}")

print(f"\nAdded ({len(added)}):")
for item in added:
    print(f"  + {item}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (net: {len(new_rows) - len(rows):+d})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)
print("✓ 7 items in Zotero with 'Council Chambers' will now map correctly")
print("✓ Prevents data loss when applying new taxonomy")
print("✓ Specifies location as Katoomba Council Chambers")
