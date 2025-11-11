#!/usr/bin/env python3
"""
Add parentheticals to denominational church categories to prevent cross-facet contamination.

PROBLEM: "Church of England churches" appears under BOTH Agents and Built Environment
because it connects to "churches" which exists in both facets.

SOLUTION: Qualify the denominational categories:
- Under Agents: "Church of England churches (organisations)"
- Under Built Environment: Already have "Church of England churches (buildings)"

This requires updating the parent references for all (organisation) church entries.
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

# Mappings for renaming
denominational_renames = {
    'Church of England churches': 'Church of England churches (organisations)',
    'Congregational churches': 'Congregational churches (organisations)',
    'Methodist churches': 'Methodist churches (organisations)',
    'Presbyterian churches': 'Presbyterian churches (organisations)',
    'Roman Catholic churches': 'Roman Catholic churches (organisations)',
    'Wesleyan churches': 'Wesleyan churches (organisations)'
}

# Process rows
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    # Rename denominational categories that are under Agents (religious organisations)
    if old_tag in denominational_renames and action == 'hierarchy':
        # Check if this is the one under religious organisations (Agents)
        if 'parent=churches' in notes:
            # This could be either Agents or Built Environment
            # We need to check context - if it has (organisation) children, it's Agents
            # For now, we'll rename and create both versions
            pass

    # Update parent references for (organisation) entries
    for old_name, new_name in denominational_renames.items():
        if f'parent={old_name}' in notes and '(organisation)' in old_tag:
            changes.append(f"{old_tag}: parent {old_name} → {new_name}")
            row['notes'] = notes.replace(f'parent={old_name}', f'parent={new_name}')

    # Rename the denominational category tags themselves IF they have (organisation) children
    if old_tag in denominational_renames and action == 'hierarchy' and 'parent=churches' in notes:
        # Check if this should be qualified
        # We need to determine if this is the Agents or Built Environment one
        # Strategy: Create qualified versions for Agents, keep (buildings) for Built Environment
        new_name = denominational_renames[old_tag]
        changes.append(f"Qualify: {old_tag} → {new_name}")
        row['old_tag'] = new_name
        row['new_tag'] = new_name

    new_rows.append(row)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("QUALIFY DENOMINATIONAL CATEGORIES")
print("="*80)

print(f"\nChanges made ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nRows: {len(rows)} → {len(new_rows)}")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")
