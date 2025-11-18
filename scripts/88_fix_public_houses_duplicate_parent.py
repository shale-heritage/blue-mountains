#!/usr/bin/env python3
"""
Fix duplicate parent relationship for public houses (buildings).

Issue:
- Line 1559: public houses (buildings) has parent=accommodation and hospitality venues
- This creates incorrect sibling relationship with "public houses" plural parent
- Should only have parent=accommodation buildings (line 1558)

Correct structure should mirror hotels pattern:
- public houses → parent=accommodation and hospitality venues (organisational)
- public houses (buildings) → parent=accommodation buildings ONLY
- public houses (businesses) → parent=hospitality businesses ONLY

Changes:
- Delete line with: public houses (buildings),parent=accommodation and hospitality venues
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

def fix_public_houses(csv_path):
    """Remove duplicate parent relationship for public houses (buildings)."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    original_count = len(rows)
    deleted_count = 0

    # Filter rows - remove the duplicate parent relationship
    filtered_rows = []
    for row in rows:
        # Delete: public houses (buildings),parent=accommodation and hospitality venues
        if (row['old_tag'] == 'public houses (buildings)' and
            row['new_tag'] == 'public houses (buildings)' and
            row['action'] == 'hierarchy' and
            'parent=accommodation and hospitality venues' in row.get('notes', '')):
            deleted_count += 1
            print(f"Deleting: {row['old_tag']},{row['new_tag']},{row['action']},{row['notes']}")
            continue

        filtered_rows.append(row)

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    return deleted_count, original_count, len(filtered_rows)

def main():
    """Main execution function."""
    print("Public Houses Duplicate Parent Relationship Fix")
    print("=" * 60)
    print("\nIssue: public houses (buildings) has duplicate parent relationship")
    print("  - Should only be child of 'accommodation buildings'")
    print("  - Currently also child of 'accommodation and hospitality venues'")
    print("  - This makes it sibling of 'public houses' instead of child")

    # Create backup
    print("\n" + "=" * 60)
    create_backup(csv_path)

    # Apply fix
    print("\nApplying fix...")
    deleted, original, final = fix_public_houses(csv_path)

    print("\n" + "=" * 60)
    print("Results:")
    print(f"  Original entries: {original}")
    print(f"  Deleted entries:  {deleted}")
    print(f"  Final entries:    {final}")
    print(f"  Net change:       -{deleted} entries")

    print("\n" + "=" * 60)
    print("Fix applied successfully!")
    print("\nNext steps:")
    print("1. Regenerate visualisations: python3 scripts/23_visualise_poly_hierarchy.py")
    print("2. Verify structure: check primary_built_environment.txt")
    print("3. Review changes: git diff data/tag_map_consolidated.csv")

if __name__ == "__main__":
    main()
