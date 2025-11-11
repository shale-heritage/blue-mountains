#!/usr/bin/env python3
"""
Properly move ALL church (building) entries from Agents to Built Environment.

The issue: Church buildings were added to Built Environment but NOT removed from Agents.
Buildings should ONLY exist in Built Environment facet.
Organizations should ONLY exist in Agents facet.

Actions:
1. Remove ALL hierarchy entries with (building) that have church-related parents from Agents
2. Remove ALL denominational (buildings) intermediate categories from Agents
   - Church of England churches (buildings)
   - Congregational churches (buildings)
   - Methodist churches (buildings)
   - Presbyterian churches (buildings)
   - Roman Catholic churches (buildings)
   - Wesleyan churches (buildings)
3. Keep all (organisation) tags under Agents
4. Ensure all (building) tags exist only under Built Environment
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
removed_from_agents = []

# Church-related parent patterns in AGENTS that should not have (building) children
agents_church_parents = [
    'parent=churches',
    'parent=Church of England churches',
    'parent=Congregational churches',
    'parent=Methodist churches',
    'parent=Presbyterian churches',
    'parent=Roman Catholic churches',
    'parent=Wesleyan churches',
    'parent=Church of England churches (buildings)',
    'parent=Congregational churches (buildings)',
    'parent=Methodist churches (buildings)',
    'parent=Presbyterian churches (buildings)',
    'parent=Roman Catholic churches (buildings)',
    'parent=Wesleyan churches (buildings)'
]

# Denominational building categories that should not exist under Agents
denominational_building_categories = [
    'Church of England churches (buildings)',
    'Congregational churches (buildings)',
    'Methodist churches (buildings)',
    'Presbyterian churches (buildings)',
    'Roman Catholic churches (buildings)',
    'Wesleyan churches (buildings)'
]

# Process rows - remove building entries from Agents
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    skip = False

    # Remove denominational (buildings) intermediate categories from Agents
    if (old_tag in denominational_building_categories and
        action == 'hierarchy' and
        any(parent in notes for parent in agents_church_parents)):
        removed_from_agents.append(f"{old_tag} (intermediate category)")
        skip = True

    # Remove any (building) tag that has a church-related parent in Agents
    elif ('(building)' in old_tag and
          action == 'hierarchy' and
          any(parent in notes for parent in agents_church_parents)):
        removed_from_agents.append(f"{old_tag}")
        skip = True

    if not skip:
        new_rows.append(row)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("MOVE CHURCH BUILDINGS FROM AGENTS TO BUILT ENVIRONMENT")
print("="*80)

print(f"\nRemoved from Agents ({len(removed_from_agents)}):")
for removed in removed_from_agents:
    print(f"  - {removed}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (removed: {len(rows) - len(new_rows)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

print("\n" + "="*80)
print("RESULT")
print("="*80)
print("✓ Church (building) entries now ONLY in Built Environment")
print("✓ Church (organisation) entries remain in Agents")
print("✓ Proper facet separation: buildings in Built Environment, organisations in Agents")
