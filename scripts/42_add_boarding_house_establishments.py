#!/usr/bin/env python3
"""
Add Mrs Gillen's and Miss Kelly's boarding houses to taxonomy.

Follows project capitalisation guidelines:
- Proper nouns capitalised
- Generic terms in entity names capitalised (Boarding House)
- Parenthetical qualifiers lowercase (building), (business)
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR


def add_boarding_house_establishments():
    """Add specific boarding house establishments to taxonomy."""

    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_file = BACKUP_DIR / f'tag_map_consolidated.csv.backup-{timestamp}'

    print(f"Creating backup: {backup_file}")
    with open(TAXONOMY_FILE, 'r') as src, open(backup_file, 'w') as dst:
        dst.write(src.read())

    # Read existing taxonomy
    with open(TAXONOMY_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    print(f"Current taxonomy size: {len(rows)} entries")

    # New entries - following capitalisation guidelines
    new_entries = [
        ("Mrs Gillen's Boarding House (building)",
         "Mrs Gillen's Boarding House (building)",
         "hierarchy",
         "parent=boarding houses (buildings)"),
        ("Miss Kelly's Boarding House (building)",
         "Miss Kelly's Boarding House (building)",
         "hierarchy",
         "parent=boarding houses (buildings)"),
        ("Miss Kelly's Boarding House (business)",
         "Miss Kelly's Boarding House (business)",
         "hierarchy",
         "parent=boarding houses (businesses)"),
    ]

    # Check for duplicates
    existing_tags = {row[0] for row in rows}
    to_add = []

    for entry in new_entries:
        if entry[0] in existing_tags:
            print(f"⚠ Already exists: {entry[0]}")
        else:
            to_add.append(entry)
            print(f"✓ Will add: {entry[0]}")

    if not to_add:
        print("\nNo new entries to add (all already exist)")
        return

    # Add new entries
    rows.extend(to_add)

    # Write updated taxonomy
    with open(TAXONOMY_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\n✓ Added {len(to_add)} new entries")
    print(f"Final taxonomy size: {len(rows)} entries")
    print(f"Backup saved to: {backup_file}")


if __name__ == '__main__':
    add_boarding_house_establishments()
