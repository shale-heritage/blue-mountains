#!/usr/bin/env python3
"""
Implement dual-nature taxonomy structure for cottages.

Follows the same pattern as boarding houses and hotels:
- cottage (building) - Built Environment facet
- cottage (business) - Agents facet

Removes obsolete unqualified entries.
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR


def implement_cottages_taxonomy():
    """Implement cottages dual-nature taxonomy structure."""

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

    # Entries to remove (obsolete unqualified structure)
    obsolete_entries = {
        ('Cottage', 'Cottage', 'hierarchy', 'parent=Cottages'),
        ('Cottages', 'Cottages', 'hierarchy', 'parent=Accommodation and hospitality venues'),
        ('cottage', 'cottage', 'hierarchy', 'parent=cottages'),
        ('cottages', 'cottages', 'hierarchy', 'parent=accommodation buildings'),
    }

    print("\nRemoving obsolete entries:")
    initial_count = len(rows)
    rows = [row for row in rows if tuple(row) not in obsolete_entries]
    removed_count = initial_count - len(rows)
    print(f"  Removed {removed_count} obsolete entries")

    # New dual-nature structure
    new_entries = [
        # Built Environment facet
        ('cottages (buildings)', 'cottages (buildings)', 'hierarchy',
         'parent=accommodation buildings'),
        ('cottage (building)', 'cottage (building)', 'hierarchy',
         'parent=cottages (buildings)'),

        # Agents facet
        ('cottages (businesses)', 'cottages (businesses)', 'hierarchy',
         'parent=hospitality businesses'),
        ('cottage (business)', 'cottage (business)', 'hierarchy',
         'parent=cottages (businesses)'),
    ]

    print("\nAdding new dual-nature structure:")
    for entry in new_entries:
        print(f"  + {entry[0]}")

    # Add new entries
    rows.extend(new_entries)

    # Write updated taxonomy
    with open(TAXONOMY_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\n✓ Removed {removed_count} obsolete entries")
    print(f"✓ Added {len(new_entries)} new entries")
    print(f"✓ Net change: {len(new_entries) - removed_count:+d} entries")
    print(f"Final taxonomy size: {len(rows)} entries")
    print(f"Backup saved to: {backup_file}")


if __name__ == '__main__':
    implement_cottages_taxonomy()
