#!/usr/bin/env python3
"""
Implement (building)/(organisation) disambiguation for Schools of Arts.

Replaces polyhierarchical structure with explicit qualifiers following
the same pattern as educational schools, churches, hotels, and boarding houses.

Changes:
- Remove unqualified polyhierarchical entries
- Add schools of arts (buildings) hierarchy under halls
- Add schools of arts (organisations) hierarchy under cultural societies
- Add specific establishments with both qualifiers:
  - Katoomba School of Arts (building) / (organisation)
  - Mines School of Arts (building) / (organisation)
  - Generic School of Arts (building) / (organisation)
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR


def implement_schools_of_arts_taxonomy():
    """Implement Schools of Arts disambiguation taxonomy structure."""

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
        # Unqualified Schools of Arts polyhierarchy
        ('Schools of Arts', 'Schools of Arts', 'hierarchy', 'parent=Cultural societies'),
        ('Schools of Arts', 'Schools of Arts', 'hierarchy', 'parent=Halls'),
        ('schools of arts', 'schools of arts', 'hierarchy', 'parent=cultural societies'),
        ('schools of arts', 'schools of arts', 'hierarchy', 'parent=halls'),

        # Unqualified School of Arts (singular)
        ('School of Arts', 'School of Arts', 'hierarchy', 'parent=Schools of Arts'),
        ('school of arts', 'school of arts', 'hierarchy', 'parent=schools of arts'),

        # Unqualified Katoomba School of Arts polyhierarchy
        ('Katoomba School of Arts', 'Katoomba School of Arts', 'hierarchy', 'parent=schools of arts'),
        ('Katoomba School of Arts', 'Katoomba School of Arts', 'hierarchy', 'parent=Schools of Arts'),

        # Synonyms to unqualified terms (will be recreated to point to qualified terms)
        ('School of Arts', 'school of arts', 'synonym', 'Capitalized variant from original Zotero tags'),
        ('school of art', 'school of arts', 'synonym', 'Variant spelling - standardised to School of Arts'),
        ('schools of art', 'schools of arts', 'synonym', 'Variant spelling - standardised to Schools of Arts'),
    }

    print("\nRemoving obsolete entries:")
    initial_count = len(rows)
    rows = [row for row in rows if tuple(row) not in obsolete_entries]
    removed_count = initial_count - len(rows)
    print(f"  Removed {removed_count} obsolete entries")

    # New disambiguation structure
    new_entries = [
        # Built Environment facet - Buildings
        ('schools of arts (buildings)', 'schools of arts (buildings)', 'hierarchy',
         'parent=halls'),
        ('school of arts (building)', 'school of arts (building)', 'hierarchy',
         'parent=schools of arts (buildings)'),
        ('Katoomba School of Arts (building)', 'Katoomba School of Arts (building)', 'hierarchy',
         'parent=schools of arts (buildings)'),
        ('Mines School of Arts (building)', 'Mines School of Arts (building)', 'hierarchy',
         'parent=schools of arts (buildings)'),

        # Agents facet - Organisations
        ('schools of arts (organisations)', 'schools of arts (organisations)', 'hierarchy',
         'parent=cultural societies'),
        ('school of arts (organisation)', 'school of arts (organisation)', 'hierarchy',
         'parent=schools of arts (organisations)'),
        ('Katoomba School of Arts (organisation)', 'Katoomba School of Arts (organisation)', 'hierarchy',
         'parent=schools of arts (organisations)'),
        ('Mines School of Arts (organisation)', 'Mines School of Arts (organisation)', 'hierarchy',
         'parent=schools of arts (organisations)'),

        # Synonyms pointing to BOTH qualified forms
        # Note: Zotero tag application CSV will specify which qualifier(s) to use per item
        ('School of Arts', 'school of arts (building)', 'synonym',
         'Capitalised variant - maps to building aspect'),
        ('School of Arts', 'school of arts (organisation)', 'synonym',
         'Capitalised variant - maps to organisation aspect'),
        ('school of art', 'school of arts (building)', 'synonym',
         'Singular variant - maps to building aspect'),
        ('school of art', 'school of arts (organisation)', 'synonym',
         'Singular variant - maps to organisation aspect'),
        ('schools of art', 'schools of arts (buildings)', 'synonym',
         'Plural variant - maps to building aspect'),
        ('schools of art', 'schools of arts (organisations)', 'synonym',
         'Plural variant - maps to organisation aspect'),
    ]

    print("\nAdding new disambiguation structure:")
    print("\n  Built Environment facet:")
    print("    schools of arts (buildings)")
    print("      ├── school of arts (building)")
    print("      ├── Katoomba School of Arts (building)")
    print("      └── Mines School of Arts (building)")

    print("\n  Agents facet:")
    print("    schools of arts (organisations)")
    print("      ├── school of arts (organisation)")
    print("      ├── Katoomba School of Arts (organisation)")
    print("      └── Mines School of Arts (organisation)")

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
    print("STRATEGIC CHANGE: Polyhierarchy → Disambiguation")
    print("=" * 80)
    print("Schools of Arts now uses (building)/(organisation) qualifiers")
    print("This aligns with educational schools, churches, hotels, and boarding houses")
    print("\nNext step: Apply qualified tags to Zotero items using item_tag_application.csv")


if __name__ == '__main__':
    implement_schools_of_arts_taxonomy()
