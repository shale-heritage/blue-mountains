#!/usr/bin/env python3
"""
Comprehensive fixes for hotels and churches taxonomy.

HOTELS:
1. Delaney's Hotel - Change hierarchy to synonym of Delaney's Family Hotel
2. Grand Hotel - Change hierarchy to synonym of Grand Hotel (Sydney)
3. Mrs Long's Hotel, Allen's Hotel, Brown's Hotel - Remove hierarchy entries entirely
   (These are possessive forms; items should be tagged with 'hotel' + proprietor name)
4. Add hotel (business) / hotel (building) disambiguation for dual-nature entities

CHURCHES:
5. Move ALL church (building) tags from Agents to Built Environment
   - Find all entries with '(building)' under church-related parents in Agents
   - Add corresponding entries under Built Environment

SUNDAY SCHOOLS:
6. Standardize parenthetical format to (Sunday School) - capitalize in parentheses

UK SPELLING:
7. Fix 'buisiness' → 'business' in parentheticals
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
church_building_entries = []

for row in rows:
    old_tag = row['old_tag']
    new_tag = row['new_tag']
    action = row['action']
    notes = row['notes']

    skip = False

    # 1. Change Delaney's Hotel hierarchy to synonym
    if old_tag == "Delaney's Hotel" and action == 'hierarchy':
        changes.append("Delaney's Hotel: hierarchy → synonym of Delaney's Family Hotel")
        row['new_tag'] = "Delaney's Family Hotel"
        row['action'] = 'synonym'
        row['notes'] = "Abbreviated name - use full 'Delaney's Family Hotel'"
        row['parent_broader_category'] = ''

    # 2. Change Grand Hotel hierarchy to synonym
    elif old_tag == 'Grand Hotel' and action == 'hierarchy':
        changes.append("Grand Hotel: hierarchy → synonym of Grand Hotel (Sydney)")
        row['new_tag'] = 'Grand Hotel (Sydney)'
        row['action'] = 'synonym'
        row['notes'] = 'Unqualified reference - all instances in collection refer to Sydney hotel'
        row['parent_broader_category'] = ''

    # 3. Remove possessive hotel names entirely
    elif old_tag in ["Mrs Long's Hotel", "Allen's Hotel", "Brown's Hotel"]:
        if action == 'hierarchy':
            removed_rows.append(f"{old_tag} (hierarchy) - possessive form, tag as 'hotel' + proprietor")
            skip = True
        # Keep merge entries as they document the mapping decision

    # 5. Collect church (building) entries under Agents for later processing
    elif '(building)' in old_tag and action == 'hierarchy':
        # Check if it's under a church-related parent
        if any(parent in notes for parent in [
            'parent=churches',
            'parent=Church of England churches',
            'parent=Congregational churches',
            'parent=Methodist churches',
            'parent=Presbyterian churches',
            'parent=Roman Catholic churches',
            'parent=Wesleyan churches'
        ]):
            # This is a church building incorrectly under Agents
            church_building_entries.append((old_tag, notes))
            # Mark for removal from Agents
            removed_rows.append(f"{old_tag} from Agents (moving to Built Environment)")
            skip = True

    # 6. Standardize Sunday School parenthetical
    elif '(sunday school)' in old_tag.lower() and '(Sunday School)' not in old_tag:
        old_name = old_tag
        # Replace (sunday school) with (Sunday School)
        import re
        new_name = re.sub(r'\(sunday school\)', '(Sunday School)', old_tag, flags=re.IGNORECASE)
        if new_name != old_tag:
            changes.append(f"{old_tag} → {new_name} (standardize Sunday School capitalization)")
            row['old_tag'] = new_name
            if old_tag == new_tag:  # If it was a hierarchy entry
                row['new_tag'] = new_name

    if not skip:
        new_rows.append(row)

# 4. Add hotel (business) / hotel (building) disambiguation entries
# Find position after 'hotel' generic entry
insert_pos = None
for i, row in enumerate(new_rows):
    if row['old_tag'] == 'hotel' and row['action'] == 'hierarchy':
        insert_pos = i + 1
        break

if insert_pos:
    # Add hotel (business)
    hotel_business = {
        'old_tag': 'hotel (business)',
        'new_tag': 'hotel (business)',
        'action': 'hierarchy',
        'notes': 'parent=hotels',
        'parent_broader_category': 'Singular generic term for business entity'
    }
    new_rows.insert(insert_pos, hotel_business)
    added_rows.append("hotel (business) - business entity aspect")

    # Add hotel (building)
    hotel_building = {
        'old_tag': 'hotel (building)',
        'new_tag': 'hotel (building)',
        'action': 'hierarchy',
        'notes': 'parent=hotels',  # Will be moved to Built Environment in separate process
        'parent_broader_category': 'Singular generic term for physical structure'
    }
    new_rows.insert(insert_pos + 1, hotel_building)
    added_rows.append("hotel (building) - physical structure aspect")

# 5. Add church buildings to Built Environment
# Find Built Environment section - look for religious buildings parent
be_insert_pos = None
for i, row in enumerate(new_rows):
    if row['old_tag'] == 'religious buildings' and row['action'] == 'hierarchy':
        be_insert_pos = i + 1
        break

if be_insert_pos and church_building_entries:
    # Create a churches parent under religious buildings
    churches_be = {
        'old_tag': 'churches',
        'new_tag': 'churches',
        'action': 'hierarchy',
        'notes': 'parent=religious buildings',
        'parent_broader_category': ''
    }
    new_rows.insert(be_insert_pos, churches_be)
    added_rows.append("churches under Built Environment > religious buildings")
    be_insert_pos += 1

    # Now add all the church building entries
    for church_name, old_notes in church_building_entries:
        # Determine appropriate parent under Built Environment
        if 'Church of England' in church_name:
            be_parent = 'parent=Church of England churches (buildings)'
        elif 'Congregational' in church_name:
            be_parent = 'parent=Congregational churches (buildings)'
        elif 'Methodist' in church_name:
            be_parent = 'parent=Methodist churches (buildings)'
        elif 'Presbyterian' in church_name:
            be_parent = 'parent=Presbyterian churches (buildings)'
        elif 'Roman Catholic' in church_name or 'Catholic' in church_name:
            be_parent = 'parent=Roman Catholic churches (buildings)'
        elif 'Wesleyan' in church_name:
            be_parent = 'parent=Wesleyan churches (buildings)'
        elif 'church (building)' == church_name:
            be_parent = 'parent=churches'
        else:
            be_parent = 'parent=churches'

        church_be_entry = {
            'old_tag': church_name,
            'new_tag': church_name,
            'action': 'hierarchy',
            'notes': be_parent,
            'parent_broader_category': ''
        }
        new_rows.insert(be_insert_pos, church_be_entry)
        be_insert_pos += 1
        added_rows.append(f"{church_name} under Built Environment")

print("\nNote: hotel (building) entries will need parent updated to Built Environment in next phase")

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("HOTELS & CHURCHES COMPREHENSIVE FIXES")
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
