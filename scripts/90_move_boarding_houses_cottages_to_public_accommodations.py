#!/usr/bin/env python3
"""
Move boarding houses (buildings) and cottages (buildings) under public accommodations.

Issue:
boarding houses (buildings) and cottages (buildings) are direct children of
"accommodation buildings", but they should be grouped with hotels (buildings)
under "public accommodations" since all three are commercial/paid accommodation.

Current structure:
  accommodation buildings
  ├── boarding houses (buildings)
  ├── cottages (buildings)
  └── public accommodations
      └── hotels (buildings)

Correct structure:
  accommodation buildings
  └── public accommodations
      ├── hotels (buildings)
      ├── boarding houses (buildings)
      └── cottages (buildings)

Changes:
- boarding houses (buildings): parent=accommodation buildings → parent=public accommodations
- cottages (buildings): parent=accommodation buildings → parent=public accommodations
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

def move_to_public_accommodations(csv_path):
    """Move boarding houses and cottages buildings to public accommodations."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    modified_count = 0

    # Update parent relationships
    for row in rows:
        # boarding houses (buildings): parent=accommodation buildings → parent=public accommodations
        if (row['old_tag'] == 'boarding houses (buildings)' and
            row['new_tag'] == 'boarding houses (buildings)' and
            row['action'] == 'hierarchy' and
            'parent=accommodation buildings' in row.get('notes', '')):
            row['notes'] = row['notes'].replace(
                'parent=accommodation buildings',
                'parent=public accommodations'
            )
            modified_count += 1
            print(f"Updated: boarding houses (buildings) → parent=public accommodations")

        # cottages (buildings): parent=accommodation buildings → parent=public accommodations
        if (row['old_tag'] == 'cottages (buildings)' and
            row['new_tag'] == 'cottages (buildings)' and
            row['action'] == 'hierarchy' and
            'parent=accommodation buildings' in row.get('notes', '')):
            row['notes'] = row['notes'].replace(
                'parent=accommodation buildings',
                'parent=public accommodations'
            )
            modified_count += 1
            print(f"Updated: cottages (buildings) → parent=public accommodations")

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return modified_count

def main():
    """Main execution function."""
    print("Move Boarding Houses and Cottages to Public Accommodations")
    print("=" * 60)
    print("\nRationale: All three types (hotels, boarding houses, cottages)")
    print("           are commercial/paid accommodation establishments")
    print("\nChanges:")
    print("  - boarding houses (buildings) → parent=public accommodations")
    print("  - cottages (buildings) → parent=public accommodations")

    # Create backup
    print("\n" + "=" * 60)
    create_backup(csv_path)

    # Apply changes
    print("\nApplying changes...")
    modified = move_to_public_accommodations(csv_path)

    print("\n" + "=" * 60)
    print("Results:")
    print(f"  Modified entries: {modified}")

    print("\n" + "=" * 60)
    print("Changes applied successfully!")
    print("\nNext steps:")
    print("1. Regenerate visualisations: python3 scripts/23_visualise_poly_hierarchy.py")
    print("2. Verify public accommodations structure")
    print("3. Review changes: git diff data/tag_map_consolidated.csv")

if __name__ == "__main__":
    main()
