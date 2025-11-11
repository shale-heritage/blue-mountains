#!/usr/bin/env python3
"""
Fix family hotel hierarchy issues.

Problems identified:
1. "family hotel" (singular generic) has parent=hotels (should be parent=family hotels)
2. "Fryer's Family Hotel" has parent=hotels (should be parent=family hotels)
3. "Katoomba Family Hotel" has duplicate hierarchy entry (one parent=hotels, one parent=family hotels)
   - Need to remove the parent=hotels entry

Expected result:
- family hotels (parent) → under hotels
  ├── family hotel (singular generic)
  ├── Delaney's Family Hotel (specific)
  ├── Fryer's Family Hotel (specific - though also has synonym mapping)
  └── Katoomba Family Hotel (specific)
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

# Process rows
new_rows = []
for row in rows:
    old_tag = row['old_tag']
    action = row['action']
    notes = row['notes']

    # Skip the duplicate Katoomba Family Hotel entry (parent=hotels)
    if (old_tag == 'Katoomba Family Hotel' and
        action == 'hierarchy' and
        notes == 'parent=hotels'):
        removed_rows.append(f"Katoomba Family Hotel,hierarchy,parent=hotels (duplicate)")
        continue

    # Fix "family hotel" singular generic parent
    if (old_tag == 'family hotel' and
        action == 'hierarchy' and
        notes == 'parent=hotels'):
        changes.append("family hotel: parent=hotels → parent=family hotels")
        row['notes'] = 'parent=family hotels,Singular generic term'

    # Fix Fryer's Family Hotel parent
    elif (old_tag == "Fryer's Family Hotel" and
          action == 'hierarchy' and
          notes == 'parent=hotels'):
        changes.append("Fryer's Family Hotel: parent=hotels → parent=family hotels")
        row['notes'] = 'parent=family hotels'

    new_rows.append(row)

# Write updated CSV
with open('data/tag_map_consolidated.csv', 'w', newline='') as f:
    fieldnames = ['old_tag', 'new_tag', 'action', 'notes', 'parent_broader_category']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_rows)

# Report results
print("\n" + "="*80)
print("FAMILY HOTEL HIERARCHY FIXES")
print("="*80)

print(f"\nChanges made ({len(changes)}):")
for change in changes:
    print(f"  ✓ {change}")

print(f"\nDuplicate entries removed ({len(removed_rows)}):")
for removed in removed_rows:
    print(f"  ✗ {removed}")

print(f"\nRows: {len(rows)} → {len(new_rows)} (removed {len(rows) - len(new_rows)})")
print(f"\n✓ Updated: data/tag_map_consolidated.csv")
print(f"✓ Backup: {backup_file}")
