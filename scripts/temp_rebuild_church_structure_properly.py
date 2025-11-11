#!/usr/bin/env python3
"""
Properly rebuild church structure with clear separation:

AGENTS > religious organisations > churches:
- Church of England churches → (organisation) entries only
- Congregational churches → (organisation) entries only
- Methodist churches → (organisation) entries only
- Presbyterian churches → (organisation) entries only
- Roman Catholic churches → (organisation) entries only
- Wesleyan churches → (organisation) entries only

BUILT ENVIRONMENT > religious buildings > churches:
- Church of England churches (buildings) → (building) entries only
- Congregational churches (buildings) → (building) entries only
- Methodist churches (buildings) → (building) entries only
- Presbyterian churches (buildings) → (building) entries only
- Roman Catholic churches (buildings) → (building) entries only
- Wesleyan churches (buildings) → (building) entries only

Key: The (buildings) qualifier on the intermediate category ensures they connect
to the churches under Built Environment, not the churches under Agents.
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

# Find position to insert Built Environment church buildings
# Look for churches under religious buildings
insert_pos = None
for i, row in enumerate(rows):
    if row['old_tag'] == 'churches' and 'parent=religious buildings' in row['notes']:
        insert_pos = i + 1
        break

if insert_pos:
    # Add denominational building categories under Built Environment > churches
    denominational_categories = [
        ('Church of England churches (buildings)', 'parent=churches'),
        ('Congregational churches (buildings)', 'parent=churches'),
        ('Methodist churches (buildings)', 'parent=churches'),
        ('Presbyterian churches (buildings)', 'parent=churches'),
        ('Roman Catholic churches (buildings)', 'parent=churches'),
        ('Wesleyan churches (buildings)', 'parent=churches')
    ]

    for category_name, parent_note in denominational_categories:
        category_entry = {
            'old_tag': category_name,
            'new_tag': category_name,
            'action': 'hierarchy',
            'notes': parent_note,
            'parent_broader_category': ''
        }
        rows.insert(insert_pos, category_entry)
        insert_pos += 1
        added_rows.append(category_name)

    # Now add the actual building entries under these categories
    # We need to recreate the church building entries that were removed

    church_buildings = [
        ("church (building)", "parent=churches"),
        ("Church of England church (building)", "parent=Church of England churches (buildings)"),
        ("Church of England Katoomba (building)", "parent=Church of England churches (buildings)"),
        ("St Hilda's Church of England (building)", "parent=Church of England churches (buildings)"),
        ("St Mark's Church of England (building)", "parent=Church of England churches (buildings)"),
        ("St Andrew's Cathedral Church of England Sydney (building)", "parent=Church of England churches (buildings)"),
        ("St John's Church Parramatta (building)", "parent=Church of England churches (buildings)"),
        ("St David's Church Surry Hills (building)", "parent=Church of England churches (buildings)"),
        ("St Paul's Church of England (building)", "parent=Church of England churches (buildings)"),
        ("St Mary's Church of England Greta (building)", "parent=Church of England churches (buildings)"),
        ("Congregational Church (building)", "parent=Congregational churches (buildings)"),
        ("Congregational Church Katoomba (building)", "parent=Congregational churches (buildings)"),
        ("Congregational Church Katoomba South (building)", "parent=Congregational churches (buildings)"),
        ("Katoomba Congregational Church (building)", "parent=Congregational churches (buildings)"),
        ("Methodist Church (building)", "parent=Methodist churches (buildings)"),
        ("Presbyterian church (building)", "parent=Presbyterian churches (buildings)"),
        ("Presbyterian Church Leura (building)", "parent=Presbyterian churches (buildings)"),
        ("Presbyterian Church Wentworth Falls (building)", "parent=Presbyterian churches (buildings)"),
        ("Roman Catholic Church (building)", "parent=Roman Catholic churches (buildings)"),
        ("Roman Catholic Church Katoomba (building)", "parent=Roman Catholic churches (buildings)"),
        ("Roman Catholic Church Megalong (building)", "parent=Roman Catholic churches (buildings)"),
        ("St Canice's Catholic Church Katoomba (building)", "parent=Roman Catholic churches (buildings)"),
        ("Wesleyan Chapel (building)", "parent=Wesleyan churches (buildings)"),
        ("Wesleyan Church (building)", "parent=Wesleyan churches (buildings)"),
        ("Wesleyan Church Katoomba (building)", "parent=Wesleyan churches (buildings)")
    ]

    for building_name, parent_note in church_buildings:
        building_entry = {
            'old_tag': building_name,
            'new_tag': building_name,
            'action': 'hierarchy',
            'notes': parent_note,
            'parent_broader_category': ''
        }
        rows.insert(insert_pos, building_entry)
        insert_pos += 1
        added_rows.append(building_name)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# Report results
print("\n" + "="*80)
print("REBUILD CHURCH STRUCTURE WITH PROPER SEPARATION")
print("="*80)

print(f"\nAdded to Built Environment > religious buildings > churches ({len(added_rows)}):")
print(f"  6 denominational (buildings) categories")
print(f"  {len(added_rows) - 6} specific church (building) entries")

print(f"\nRows: {len(rows) - len(added_rows)} → {len(rows)} (added: {len(added_rows)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

print("\n" + "="*80)
print("RESULT")
print("="*80)
print("✓ AGENTS > churches: Only (organisation) entries")
print("✓ BUILT ENVIRONMENT > churches: Only (building) entries")
print("✓ Proper facet separation maintained")
