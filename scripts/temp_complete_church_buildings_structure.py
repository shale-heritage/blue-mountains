#!/usr/bin/env python3
"""
Complete the church buildings structure in Built Environment.

1. Add denominational intermediate categories under churches (buildings):
   - Church of England churches (buildings)
   - Congregational churches (buildings)
   - Methodist churches (buildings)
   - Presbyterian churches (buildings)
   - Roman Catholic churches (buildings)
   - Wesleyan churches (buildings)

2. Move hotel (building) from hotels to accommodation buildings
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
added_rows = []
changes = []

# Process rows
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    # Fix hotel (building) parent
    if old_tag == 'hotel (building)' and action == 'hierarchy' and 'parent=hotels' in notes:
        changes.append("hotel (building): parent hotels → accommodation buildings")
        row['notes'] = 'parent=accommodation buildings'

    # Update church building parents to use new intermediate categories
    if action == 'hierarchy' and '(building)' in old_tag:
        if notes == 'parent=Church of England churches (buildings)':
            # Already correct
            pass
        elif 'Church of England' in old_tag and notes == 'parent=churches':
            row['notes'] = 'parent=Church of England churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Church of England churches (buildings)")
        elif 'Congregational' in old_tag and notes == 'parent=churches':
            row['notes'] = 'parent=Congregational churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Congregational churches (buildings)")
        elif 'Methodist' in old_tag and notes == 'parent=churches':
            row['notes'] = 'parent=Methodist churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Methodist churches (buildings)")
        elif 'Presbyterian' in old_tag and notes == 'parent=churches':
            row['notes'] = 'parent=Presbyterian churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Presbyterian churches (buildings)")
        elif ('Roman Catholic' in old_tag or 'Catholic' in old_tag) and notes == 'parent=churches':
            row['notes'] = 'parent=Roman Catholic churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Roman Catholic churches (buildings)")
        elif 'Wesleyan' in old_tag and notes == 'parent=churches':
            row['notes'] = 'parent=Wesleyan churches (buildings)'
            changes.append(f"{old_tag}: parent churches → Wesleyan churches (buildings)")

    new_rows.append(row)

# Add denominational intermediate categories
# Find position after 'churches' under religious buildings
insert_pos = None
for i, row in enumerate(new_rows):
    if row['old_tag'] == 'churches' and 'parent=religious buildings' in row['notes']:
        insert_pos = i + 1
        break

if insert_pos:
    denominations = [
        'Church of England churches (buildings)',
        'Congregational churches (buildings)',
        'Methodist churches (buildings)',
        'Presbyterian churches (buildings)',
        'Roman Catholic churches (buildings)',
        'Wesleyan churches (buildings)'
    ]

    for denom in denominations:
        denom_entry = {
            'old_tag': denom,
            'new_tag': denom,
            'action': 'hierarchy',
            'notes': 'parent=churches',
            'parent_broader_category': ''
        }
        new_rows.insert(insert_pos, denom_entry)
        insert_pos += 1
        added_rows.append(denom)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("COMPLETE CHURCH BUILDINGS STRUCTURE")
print("="*80)

print(f"\nDenominational categories added ({len(added_rows)}):")
for added in added_rows:
    print(f"  + {added}")

print(f"\nParent updates ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (net: {len(new_rows) - len(rows):+d})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")
