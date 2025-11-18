#!/usr/bin/env python3
"""
Fix capitalisation issues in Associated Concepts facet.

Changes:
- Maps → maps (generic document type should be lowercase)

Aligns with style-guide.md capitalisation rules:
- Lowercase for generic terms
- Title Case only for proper nouns
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

def fix_capitalisation(csv_path):
    """Fix capitalisation in Associated Concepts facet."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    changes_made = 0

    # Process rows
    for row in rows:
        # Fix: Maps → maps
        if row['old_tag'] == 'Maps':
            row['old_tag'] = 'maps'
            changes_made += 1

        if row['new_tag'] == 'Maps':
            row['new_tag'] = 'maps'
            changes_made += 1

        # Update notes that reference Maps
        if 'Maps' in row.get('notes', ''):
            row['notes'] = row['notes'].replace('Maps', 'maps')
            changes_made += 1

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return changes_made

def main():
    """Main execution function."""
    print("Associated Concepts Capitalisation Corrections")
    print("=" * 60)

    # Create backup
    create_backup(csv_path)

    # Apply corrections
    print("\nApplying corrections...")
    changes = fix_capitalisation(csv_path)

    print(f"\nChanges made: {changes}")
    print("\nCorrections applied successfully!")
    print("\nNext steps:")
    print("1. Run visualisation regeneration script")
    print("2. Review changes with: git diff data/tag_map_consolidated.csv")

if __name__ == "__main__":
    main()
