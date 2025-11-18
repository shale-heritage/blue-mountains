#!/usr/bin/env python3
"""
Move public houses (buildings) under public accommodations to align with Getty AAT.

Getty AAT guidance:
- Public accommodations (AAT 300164125) includes inns and related establishments
- Cauponae (AAT 300005208) - Roman taverns serving food/drink under public accommodations
- Pubs/public houses as drinking/dining establishments align with this category

Historical context:
While pubs' primary function is drinking/social venue, Getty AAT takes a broad
interpretation of "public accommodations" to include hospitality establishments
where the public gathers for refreshment and social purposes.

Changes:
- public houses (buildings): parent=accommodation buildings → parent=public accommodations

Stables remain under accommodation buildings (visitor horse accommodation, like hotel parking).
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

def move_public_houses_to_public_accommodations(csv_path):
    """Move public houses (buildings) to public accommodations."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    modified_count = 0

    # Update parent relationship
    for row in rows:
        # public houses (buildings): parent=accommodation buildings → parent=public accommodations
        if (row['old_tag'] == 'public houses (buildings)' and
            row['new_tag'] == 'public houses (buildings)' and
            row['action'] == 'hierarchy' and
            'parent=accommodation buildings' in row.get('notes', '')):
            row['notes'] = row['notes'].replace(
                'parent=accommodation buildings',
                'parent=public accommodations'
            )
            modified_count += 1
            print(f"Updated: public houses (buildings) → parent=public accommodations")

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return modified_count

def main():
    """Main execution function."""
    print("Move Public Houses to Public Accommodations (Getty AAT Alignment)")
    print("=" * 60)
    print("\nGgetty AAT guidance:")
    print("  - Public accommodations includes hospitality establishments")
    print("  - Pubs/public houses align with inns and drinking/dining venues")
    print("\nChanges:")
    print("  - public houses (buildings) → parent=public accommodations")
    print("\nStables remain under accommodation buildings (visitor horse")
    print("accommodation, analogous to hotel parking infrastructure)")

    # Create backup
    print("\n" + "=" * 60)
    create_backup(csv_path)

    # Apply changes
    print("\nApplying changes...")
    modified = move_public_houses_to_public_accommodations(csv_path)

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
