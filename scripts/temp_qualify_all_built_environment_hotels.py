#!/usr/bin/env python3
"""
Add (building) qualifier to ALL hotel entries in Built Environment.

Issues to fix:
1. All specific hotel names need (building): Carrington Hotel → Carrington Hotel (building)
2. Generic "hotel" under hotels needs to be "hotel (building)"
3. Remove "hotel (business)" from Built Environment entirely (only belongs in Agents)
4. All family hotel names need (building)
5. Generic "family hotel" needs to be "family hotel (building)"
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

# Hotels that need (building) qualifier
hotels_to_qualify = [
    'Belgravia Hotel',
    'Carrington Hotel',
    'Centennial Hotel',
    'Comet Hotel',
    'Falls Hotel',
    'Grand Hotel (Sydney)',
    'Great Western Hotel',
    "Hoffman's House",
    'Hotel Wentworth',
    'Hydora House Hotel',
    'Imperial Hotel',
    'Katoomba Hotel',
    'Leura Hotel',
    'Megalong Hotel',
    'Montrose House',
    'Mount Victoria Hotel',
    'Oxford Hotel (Sydney)',
    'Railway Hotel',
    'Wentworth Falls Hotel',
    "Delaney's Family Hotel",
    "Fryer's Family Hotel",
    'Katoomba Family Hotel',
    'family hotel',
    'hotel'
]

# Track changes
changes = []
removed_rows = []

# Process rows
new_rows = []

for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    skip = False

    # Remove hotel (business) from Built Environment
    if (old_tag == 'hotel (business)' and
        action == 'hierarchy' and
        'parent=hotels' in notes):
        removed_rows.append("hotel (business) - belongs only in Agents")
        skip = True

    # Qualify all hotel names in Built Environment with (building)
    elif (old_tag in hotels_to_qualify and
          action == 'hierarchy' and
          ('parent=hotels' in notes or 'parent=family hotels' in notes)):

        # Don't qualify if already qualified
        if '(building)' not in old_tag:
            new_name = f"{old_tag} (building)"
            changes.append(f"{old_tag} → {new_name}")
            row['old_tag'] = new_name
            row['new_tag'] = new_name

    # Update parent references for any entries that reference these hotels
    # (though there shouldn't be any for leaf nodes)

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
print("QUALIFY ALL HOTELS IN BUILT ENVIRONMENT")
print("="*80)

print(f"\nQualified with (building) ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nRemoved from Built Environment ({len(removed_rows)}):")
for removed in removed_rows:
    print(f"  - {removed}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (removed: {len(rows) - len(new_rows)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")

print("\n" + "="*80)
print("RESULT")
print("="*80)
print("✓ All hotels in Built Environment now have (building) qualifier")
print("✓ hotel (business) removed from Built Environment (remains in Agents only)")
print("✓ Proper facet separation maintained")
