#!/usr/bin/env python3
"""
Qualify all accommodation/hospitality intermediate categories to prevent facet contamination.

PROBLEM: Same as churches - "hotels" and "boarding houses" exist in BOTH Agents and Built Environment

SOLUTION:
Agents > hospitality businesses:
- hotels → hotels (businesses)
- boarding houses → boarding houses (businesses)
- Add business qualifiers to all specific entities

Built Environment > accommodation buildings:
- hotels → hotels (buildings) [keep structure, already has (building) children]
- boarding houses → boarding houses (buildings)
- public houses → public houses (buildings)
- stables → stables (buildings)
- Already qualified: all children have (building)
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
added_rows = []

# Process rows
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    # 1. Rename intermediate categories under Agents > hospitality businesses
    if old_tag == 'hotels' and action == 'hierarchy' and 'parent=hospitality businesses' in notes:
        changes.append("hotels → hotels (businesses) under Agents")
        row['old_tag'] = 'hotels (businesses)'
        row['new_tag'] = 'hotels (businesses)'

    elif old_tag == 'boarding houses' and action == 'hierarchy' and 'parent=hospitality businesses' in notes:
        changes.append("boarding houses → boarding houses (businesses) under Agents")
        row['old_tag'] = 'boarding houses (businesses)'
        row['new_tag'] = 'boarding houses (businesses)'

    # 2. Rename intermediate categories under Built Environment > accommodation buildings
    elif old_tag == 'hotels' and action == 'hierarchy' and 'parent=accommodation buildings' in notes:
        changes.append("hotels → hotels (buildings) under Built Environment")
        row['old_tag'] = 'hotels (buildings)'
        row['new_tag'] = 'hotels (buildings)'

    elif old_tag == 'boarding houses' and action == 'hierarchy' and 'parent=accommodation buildings' in notes:
        changes.append("boarding houses → boarding houses (buildings) under Built Environment")
        row['old_tag'] = 'boarding houses (buildings)'
        row['new_tag'] = 'boarding houses (buildings)'

    elif old_tag == 'public houses' and action == 'hierarchy' and 'parent=accommodation buildings' in notes:
        changes.append("public houses → public houses (buildings) under Built Environment")
        row['old_tag'] = 'public houses (buildings)'
        row['new_tag'] = 'public houses (buildings)'

    elif old_tag == 'stables' and action == 'hierarchy' and 'parent=accommodation buildings' in notes:
        changes.append("stables → stables (buildings) under Built Environment")
        row['old_tag'] = 'stables (buildings)'
        row['new_tag'] = 'stables (buildings)'

    # 3. Update parent references: children under hotels → hotels (businesses) in Agents
    elif 'parent=hotels' in notes and '(building)' not in old_tag and '(business)' not in old_tag:
        # This is tricky - need to determine if it should be (buildings) or (businesses)
        # Default: if no qualifier, assume it's under Built Environment (already has buildings)
        # We'll update Agents references separately
        pass

    # 4. Update parent references: hotels (building) children → hotels (buildings)
    elif 'parent=hotels' in notes and '(building)' in old_tag:
        changes.append(f"{old_tag}: parent hotels → hotels (buildings)")
        row['notes'] = notes.replace('parent=hotels', 'parent=hotels (buildings)')

    # 5. Update parent references: boarding house children
    elif 'parent=boarding houses' in notes and '(building)' not in old_tag and '(business)' not in old_tag:
        # Need to qualify boarding house entries in Agents vs Built Environment
        # For now, assume unqualified boarding house is business (in Agents)
        if old_tag in ['Orama Boarding House', 'boarding house']:
            # These need to be businesses in Agents
            new_name = f"{old_tag} (business)"
            changes.append(f"{old_tag} → {new_name}")
            row['old_tag'] = new_name
            row['new_tag'] = new_name
            row['notes'] = notes.replace('parent=boarding houses', 'parent=boarding houses (businesses)')

    # 6. Update public house and stable children
    elif old_tag == 'public house' and 'parent=public houses' in notes:
        changes.append("public house → public house (building)")
        row['old_tag'] = 'public house (building)'
        row['new_tag'] = 'public house (building)'
        row['notes'] = 'parent=public houses (buildings)'

    elif old_tag == 'stable' and 'parent=stables' in notes:
        changes.append("stable → stable (building)")
        row['old_tag'] = 'stable (building)'
        row['new_tag'] = 'stable (building)'
        row['notes'] = 'parent=stables (buildings)'

    # 7. Update family hotels parent reference
    elif old_tag == 'family hotels' and 'parent=hotels' in notes:
        changes.append("family hotels: parent hotels → hotels (buildings)")
        row['notes'] = 'parent=hotels (buildings)'

    new_rows.append(row)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("QUALIFY ACCOMMODATION & HOSPITALITY CATEGORIES")
print("="*80)

print(f"\nChanges made ({len(changes)}):")
for change in changes[:20]:
    print(f"  ✓ {change}")
if len(changes) > 20:
    print(f"  ... and {len(changes) - 20} more")

print(f"\nRows: {len(rows)} → {len(new_rows)}")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")
