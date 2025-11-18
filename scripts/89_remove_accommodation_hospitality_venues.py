#!/usr/bin/env python3
"""
Remove redundant "accommodation and hospitality venues" category.

Issue:
The taxonomy has both:
- accommodation and hospitality venues (with unqualified plural parents)
- accommodation buildings (with qualified (buildings) versions)

This creates unnecessary duplication. Built Environment should only contain
the (buildings) aspect of dual-nature entities.

Changes:
1. Delete "accommodation and hospitality venues" category
2. Remove hierarchy relationships for plural parents under that category
3. Add synonym relationships mapping unqualified to qualified versions

Dual-nature entities (both building & business aspects):
- hotels, public houses, boarding houses, cottages

Building-only entities:
- stables (only has buildings aspect)
- dwellings (already has correct hierarchy under accommodation buildings)
"""

import csv
from datetime import datetime
from pathlib import Path

# Paths
project_root = Path(__file__).parent.parent
csv_path = project_root / "data" / "tag_map_consolidated.csv"

def create_backup(file_path):
    """Create timestamped backup of the CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    backup_path.write_text(file_path.read_text())
    print(f"Backup created: {backup_path}")
    return backup_path

def remove_accommodation_venues(csv_path):
    """Remove accommodation and hospitality venues category and update synonyms."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    original_count = len(rows)
    deleted_count = 0
    added_count = 0

    # Entries to delete
    delete_entries = [
        ('accommodation and hospitality venues', 'accommodation and hospitality venues',
         'hierarchy', 'parent=Built Environment'),
        ('boarding houses', 'boarding houses',
         'hierarchy', 'parent=accommodation and hospitality venues'),
        ('cottages', 'cottages',
         'hierarchy', 'parent=accommodation and hospitality venues'),
        ('dwellings', 'dwellings',
         'hierarchy', 'parent=accommodation and hospitality venues'),
        ('hotels', 'hotels',
         'hierarchy', 'parent=accommodation and hospitality venues'),
        ('public houses', 'public houses',
         'hierarchy', 'parent=accommodation and hospitality venues'),
        ('stables', 'stables',
         'hierarchy', 'parent=accommodation and hospitality venues'),
    ]

    # Synonym entries to add
    new_synonyms = [
        # Dual-nature: hotels
        ('hotels', 'hotels (buildings)', 'synonym',
         'Unqualified form - maps to buildings aspect'),
        ('hotels', 'hotels (businesses)', 'synonym',
         'Unqualified form - maps to businesses aspect'),

        # Dual-nature: public houses
        ('public houses', 'public houses (buildings)', 'synonym',
         'Unqualified form - maps to buildings aspect'),
        ('public houses', 'public houses (businesses)', 'synonym',
         'Unqualified form - maps to businesses aspect'),

        # Dual-nature: boarding houses
        ('boarding houses', 'boarding houses (buildings)', 'synonym',
         'Unqualified form - maps to buildings aspect'),
        ('boarding houses', 'boarding houses (businesses)', 'synonym',
         'Unqualified form - maps to businesses aspect'),

        # Dual-nature: cottages
        ('cottages', 'cottages (buildings)', 'synonym',
         'Unqualified form - maps to buildings aspect'),
        ('cottages', 'cottages (businesses)', 'synonym',
         'Unqualified form - maps to businesses aspect'),

        # Building-only: stables
        ('stables', 'stables (buildings)', 'synonym',
         'Unqualified form - maps to buildings aspect'),
    ]

    # Filter rows - remove deletions
    filtered_rows = []
    for row in rows:
        should_delete = False

        for del_old, del_new, del_action, del_parent in delete_entries:
            if (row['old_tag'] == del_old and
                row['new_tag'] == del_new and
                row['action'] == del_action and
                del_parent in row.get('notes', '')):
                print(f"Deleting: {row['old_tag']},{row['new_tag']},{row['action']},{row['notes']}")
                deleted_count += 1
                should_delete = True
                break

        if not should_delete:
            filtered_rows.append(row)

    # Add new synonym entries
    print("\nAdding synonym entries:")
    for old_tag, new_tag, action, notes in new_synonyms:
        # Check if synonym already exists
        exists = False
        for row in filtered_rows:
            if (row['old_tag'] == old_tag and
                row['new_tag'] == new_tag and
                row['action'] == 'synonym'):
                exists = True
                break

        if not exists:
            new_row = {
                'old_tag': old_tag,
                'new_tag': new_tag,
                'action': action,
                'notes': notes,
                'status': 'active'
            }
            filtered_rows.append(new_row)
            added_count += 1
            print(f"Adding: {old_tag} → {new_tag} (synonym)")

    # Sort rows to maintain some order (optional, keeps old_tag alphabetical)
    filtered_rows.sort(key=lambda x: (x['old_tag'].lower(), x['action'], x['new_tag']))

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    return deleted_count, added_count, original_count, len(filtered_rows)

def main():
    """Main execution function."""
    print("Remove Accommodation and Hospitality Venues Category")
    print("=" * 60)
    print("\nIssue: Redundant category creates duplication with")
    print("       'accommodation buildings'")
    print("\nActions:")
    print("  1. Delete 'accommodation and hospitality venues' category")
    print("  2. Delete 6 plural parent hierarchy relationships")
    print("  3. Add synonym mappings to qualified versions")

    # Create backup
    print("\n" + "=" * 60)
    create_backup(csv_path)

    # Apply changes
    print("\nApplying changes...")
    print("=" * 60)
    deleted, added, original, final = remove_accommodation_venues(csv_path)

    print("\n" + "=" * 60)
    print("Results:")
    print(f"  Original entries: {original}")
    print(f"  Deleted entries:  {deleted}")
    print(f"  Added entries:    {added}")
    print(f"  Final entries:    {final}")
    print(f"  Net change:       {added - deleted:+d} entries")

    print("\n" + "=" * 60)
    print("Changes applied successfully!")
    print("\nNext steps:")
    print("1. Regenerate visualisations: python3 scripts/23_visualise_poly_hierarchy.py")
    print("2. Verify Built Environment structure")
    print("3. Review changes: git diff data/tag_map_consolidated.csv")

if __name__ == "__main__":
    main()
