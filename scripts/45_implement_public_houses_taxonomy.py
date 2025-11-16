#!/usr/bin/env python3
"""
Complete (building)/(business) disambiguation for Public houses.

The taxonomy currently has partial structure (building facet exists) but lacks
the business facet. This script completes the disambiguation following the same
pattern as hotels, schools of arts, churches, and boarding houses.

Changes:
- Remove incomplete polyhierarchical entries (unqualified "Public house")
- Keep existing public houses (buildings) structure
- Add public houses (businesses) hierarchy under Agents
- Update synonyms to point to both qualified forms
- Maintain "Pubs" synonym mapping to plural forms
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR


def implement_public_houses_taxonomy():
    """Complete Public houses disambiguation taxonomy structure."""

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

    # Entries to remove (unqualified polyhierarchical structure)
    obsolete_entries = {
        # Unqualified Public house (polyhierarchical - inconsistent with project pattern)
        ('Public house', 'Public house', 'hierarchy', 'parent=Public houses'),

        # Unqualified Public houses polyhierarchy (partial - only one parent listed)
        ('Public houses', 'Public houses', 'hierarchy', 'parent=Accommodation and hospitality venues'),
        ('Public houses', 'Public houses', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'),

        # Old synonyms pointing to unqualified terms (will be recreated to point to qualified terms)
        ('Pub', 'public house', 'synonym', 'Colloquial term for public house'),
        ('pub', 'public house', 'synonym', 'Short form (UK/Australian) - lowercase variant'),
        ('Pubs', 'public houses', 'synonym', 'Colloquial short form - prefer full form public houses'),

        # Lowercase variants (partial implementation)
        ('public houses', 'public houses', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'),
    }

    print("\nRemoving obsolete entries:")
    initial_count = len(rows)
    rows = [row for row in rows if tuple(row) not in obsolete_entries]
    removed_count = initial_count - len(rows)
    print(f"  Removed {removed_count} obsolete entries")

    # New disambiguation structure
    new_entries = [
        # Built Environment facet - Buildings (keep existing, add parent plural)
        ('public houses (buildings)', 'public houses (buildings)', 'hierarchy',
         'parent=accommodation buildings'),
        # Note: 'public house (building)' already exists under 'public houses (buildings)'

        # Agents facet - Businesses (NEW)
        ('public houses (businesses)', 'public houses (businesses)', 'hierarchy',
         'parent=hospitality businesses'),
        ('public house (business)', 'public house (business)', 'hierarchy',
         'parent=public houses (businesses)'),

        # Thematic cross-references (maintain existing themes with qualified targets)
        ('public houses (buildings)', 'public houses (buildings)', 'hierarchy',
         'parent=Accommodation and hospitality venues'),
        ('public houses (businesses)', 'public houses (businesses)', 'hierarchy',
         'parent=Alcohol-related venues - THEMATIC'),

        # Synonyms pointing to BOTH qualified forms
        # "Pub" (capitalized) → both aspects
        ('Pub', 'public house (building)', 'synonym',
         'Colloquial term - maps to building aspect'),
        ('Pub', 'public house (business)', 'synonym',
         'Colloquial term - maps to business aspect'),

        # "pub" (lowercase) → both aspects
        ('pub', 'public house (building)', 'synonym',
         'Short form (UK/Australian) - maps to building aspect'),
        ('pub', 'public house (business)', 'synonym',
         'Short form (UK/Australian) - maps to business aspect'),

        # "Pubs" (capitalized plural) → both plural forms
        ('Pubs', 'public houses (buildings)', 'synonym',
         'Colloquial plural - maps to building aspect'),
        ('Pubs', 'public houses (businesses)', 'synonym',
         'Colloquial plural - maps to business aspect'),

        # "pubs" (lowercase plural) → both plural forms
        ('pubs', 'public houses (buildings)', 'synonym',
         'Colloquial plural (lowercase) - maps to building aspect'),
        ('pubs', 'public houses (businesses)', 'synonym',
         'Colloquial plural (lowercase) - maps to business aspect'),
    ]

    print("\nCompleting disambiguation structure:")
    print("\n  Built Environment facet:")
    print("    public houses (buildings)  [parent already exists]")
    print("      └── public house (building)  [already exists]")

    print("\n  Agents facet (NEW):")
    print("    public houses (businesses)")
    print("      └── public house (business)")

    print(f"\n  Total new entries: {len(new_entries)}")

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

    print("\n" + "=" * 80)
    print("COMPLETION: Public Houses Disambiguation")
    print("=" * 80)
    print("Public houses now uses complete (building)/(business) qualifiers")
    print("This aligns with hotels, schools of arts, churches, and boarding houses")
    print("\nNext step: Apply qualified tags to Zotero items using item_tag_application.csv")


if __name__ == '__main__':
    implement_public_houses_taxonomy()
