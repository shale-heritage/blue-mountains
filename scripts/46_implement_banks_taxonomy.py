#!/usr/bin/env python3
"""
Implement (building)/(business) disambiguation for Banks.

Replaces polyhierarchical structure with explicit qualifiers following
the same pattern as hotels, public houses, schools of arts, churches, and
boarding houses.

Changes:
- Remove unqualified polyhierarchical entries
- Add banks (buildings) hierarchy under Commercial buildings
- Add banks (businesses) hierarchy under Financial institutions
- Add specific establishments with both qualifiers:
  - Commercial Bank of Australia (building) / (business)
- Update synonyms to point to both qualified forms
- Maintain proper leaf-node pattern with plural parents
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR


def implement_banks_taxonomy():
    """Implement Banks disambiguation taxonomy structure."""

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
        # Unqualified Bank polyhierarchy (capitalized)
        ('Bank', 'Bank', 'hierarchy', 'parent=Financial institutions'),
        ('Bank', 'Bank', 'hierarchy', 'parent=Commercial buildings'),

        # Unqualified bank polyhierarchy (lowercase)
        ('bank', 'bank', 'hierarchy', 'parent=commercial buildings'),
        ('bank', 'bank', 'hierarchy', 'parent=financial institutions'),

        # Capitalization synonym (will be recreated to point to qualified terms)
        ('Bank', 'bank', 'synonym', 'Capitalized variant from original Zotero tags'),
    }

    print("\nRemoving obsolete entries:")
    initial_count = len(rows)
    rows = [row for row in rows if tuple(row) not in obsolete_entries]
    removed_count = initial_count - len(rows)
    print(f"  Removed {removed_count} obsolete entries")

    # New disambiguation structure
    new_entries = [
        # Built Environment facet - Buildings
        ('banks (buildings)', 'banks (buildings)', 'hierarchy',
         'parent=commercial buildings'),
        ('bank (building)', 'bank (building)', 'hierarchy',
         'parent=banks (buildings)'),
        ('Commercial Bank of Australia (building)', 'Commercial Bank of Australia (building)', 'hierarchy',
         'parent=banks (buildings)'),

        # Agents facet - Businesses (Financial institutions)
        ('banks (businesses)', 'banks (businesses)', 'hierarchy',
         'parent=financial institutions'),
        ('bank (business)', 'bank (business)', 'hierarchy',
         'parent=banks (businesses)'),
        ('Commercial Bank of Australia (business)', 'Commercial Bank of Australia (business)', 'hierarchy',
         'parent=banks (businesses)'),

        # Synonyms pointing to BOTH qualified forms
        # "Bank" (capitalized) → both aspects
        ('Bank', 'bank (building)', 'synonym',
         'Capitalized variant - maps to building aspect'),
        ('Bank', 'bank (business)', 'synonym',
         'Capitalized variant - maps to business aspect'),

        # "bank" (lowercase) already exists - no synonym needed (it's the canonical form)
        # This maintains "bank" as base term for both qualified forms

        # Specific establishments - synonyms
        ('Commercial Bank', 'Commercial Bank of Australia (building)', 'synonym',
         'Short form - maps to building aspect'),
        ('Commercial Bank', 'Commercial Bank of Australia (business)', 'synonym',
         'Short form - maps to business aspect'),
    ]

    print("\nImplementing disambiguation structure:")
    print("\n  Built Environment facet:")
    print("    banks (buildings)")
    print("      ├── bank (building)")
    print("      └── Commercial Bank of Australia (building)")

    print("\n  Agents facet:")
    print("    banks (businesses)")
    print("      ├── bank (business)")
    print("      └── Commercial Bank of Australia (business)")

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
    print("Banks now uses (building)/(business) qualifiers")
    print("This aligns with hotels, public houses, schools of arts, churches, and boarding houses")
    print("\nNote: Sample size was small (1 valid item) but domain knowledge and project")
    print("      consistency support this structure. As more bank items are tagged, specific")
    print("      establishments can be added following the same pattern.")
    print("\nNext steps:")
    print("1. Apply qualified tags to Zotero items using item_tag_application.csv")
    print("2. Remove false match tags from bankruptcy item")
    print("3. Consider expanded search for bank mentions in full text")


if __name__ == '__main__':
    implement_banks_taxonomy()
