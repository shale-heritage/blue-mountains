#!/usr/bin/env python3
"""
Fix multiple taxonomy errors in Agents facet.

Issues to fix:
1. 'Peckman Bros' - should be synonym for 'Peckman Brothers', not separate hierarchy
2. 'Store' (capitalized singular) - remove; generic is 'retailer or store'
3. 'penrith rugby club' - capitalize to 'Penrith Rugby Club' (proper noun)
4. 'independent lodges' - remove; use 'unaffiliated lodges' as preferred term
5. 'police court' - change from hierarchy to synonym of 'Courts of Petty Sessions'
6. 'Postal Department' - remove duplicate under 'government bodies'
7. 'Aborigines' Protection Board' - remove duplicate under 'government bodies'
8. Add 'law enforcement' intermediate between 'government bodies' and 'New South Wales Police'
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
removed_rows = []
added_rows = []

# Process rows
new_rows = []
skip_next_mountaineer = False

for i, row in enumerate(rows):
    old_tag = row['old_tag']
    new_tag = row['new_tag']
    action = row['action']
    notes = row['notes']

    skip = False

    # 1. Fix Peckman Bros - change hierarchy to synonym
    if old_tag == 'Peckman Bros' and action == 'hierarchy':
        changes.append("Peckman Bros: hierarchy → synonym of Peckman Brothers")
        row['new_tag'] = 'Peckman Brothers'
        row['action'] = 'synonym'
        row['notes'] = 'Abbreviated form - use full name Peckman Brothers'
        row['parent_broader_category'] = ''

    # 2. Remove 'Store' capitalized singular under retailers
    elif old_tag == 'Store' and action == 'hierarchy' and 'parent=retailers and stores' in notes:
        removed_rows.append("Store (hierarchy under retailers) - generic is 'retailer or store'")
        skip = True

    # 3. Capitalize 'penrith rugby club' - update all variants
    elif 'penrith rugby club' in old_tag.lower():
        if old_tag != 'Penrith Rugby Club':
            changes.append(f"{old_tag} → Penrith Rugby Club (capitalize proper noun)")
            row['old_tag'] = 'Penrith Rugby Club'
            if action == 'hierarchy' and old_tag == new_tag:
                row['new_tag'] = 'Penrith Rugby Club'

    # 4. Remove 'independent lodges' hierarchy entries
    elif old_tag == 'independent lodges' and action == 'hierarchy':
        removed_rows.append("independent lodges (use 'unaffiliated lodges' instead)")
        skip = True

    # 5. Change 'police court' from hierarchy to synonym
    elif old_tag == 'police court' and action == 'hierarchy':
        changes.append("police court: hierarchy → synonym of Courts of Petty Sessions")
        row['new_tag'] = 'Courts of Petty Sessions'
        row['action'] = 'synonym'
        row['notes'] = 'Colloquial term for Courts of Petty Sessions in NSW ca. 1890-1900'
        row['parent_broader_category'] = ''

    # 6. Remove duplicate Postal Department under government bodies
    elif (old_tag == 'Postal Department' and action == 'hierarchy' and
          'parent=government bodies' in notes):
        removed_rows.append("Postal Department (duplicate under government bodies)")
        skip = True

    # 7. Remove duplicate Aborigines' Protection Board under government bodies
    elif (old_tag == "Aborigines' Protection Board" and action == 'hierarchy' and
          'parent=government bodies' in notes):
        removed_rows.append("Aborigines' Protection Board (duplicate under government bodies)")
        skip = True

    # 8. Change NSW Police parent from 'government bodies' to 'law enforcement'
    elif (old_tag == 'New South Wales Police' and action == 'hierarchy' and
          'parent=government bodies' in notes):
        changes.append("New South Wales Police: parent changed government bodies → law enforcement")
        row['notes'] = 'parent=law enforcement'

    if not skip:
        new_rows.append(row)

# 8. Add new 'law enforcement' intermediate hierarchy
# Find position after government bodies entries
insert_pos = None
for i, row in enumerate(new_rows):
    if row['old_tag'] == 'government bodies' and row['action'] == 'hierarchy':
        insert_pos = i + 1
        break

if insert_pos:
    law_enforcement_row = {
        'old_tag': 'law enforcement',
        'new_tag': 'law enforcement',
        'action': 'hierarchy',
        'notes': 'parent=government bodies',
        'parent_broader_category': ''
    }
    new_rows.insert(insert_pos, law_enforcement_row)
    added_rows.append("law enforcement (intermediate: government bodies → New South Wales Police)")

# Also need to add 'Mountaineer Lodge' under unaffiliated lodges if independent lodges referenced it
# Check if we need to update any references to independent lodges
for row in new_rows:
    if 'parent=independent lodges' in row['notes']:
        changes.append(f"{row['old_tag']}: parent changed independent lodges → unaffiliated lodges")
        row['notes'] = row['notes'].replace('parent=independent lodges', 'parent=unaffiliated lodges')

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("AGENTS TAXONOMY FIXES")
print("="*80)

print(f"\nChanges made ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nRows added ({len(added_rows)}):")
for added in added_rows:
    print(f"  + {added}")

print(f"\nRows removed ({len(removed_rows)}):")
for removed in removed_rows:
    print(f"  - {removed}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (net: {len(new_rows) - len(rows):+d})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")
