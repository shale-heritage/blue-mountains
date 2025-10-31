#!/usr/bin/env python3
"""
Fix Awkward Singular Forms

Remove duplicate/awkward singular forms created by simple pluralization rules
when proper forms already exist in the taxonomy.

Author: Claude Code
Date: 2025-10-30
"""

import csv
from pathlib import Path

CSV_PATH = Path("data/tag_map_consolidated.csv")
BACKUP_PATH = Path("data/tag_map_consolidated.csv.backup-before-awkward-fix")

# Awkward forms to delete (proper form already exists)
DELETE_AWKWARD = [
    "Boarding hous",
    "Public hous",
    "Tenni",
    "Coach and buggy busines",
]

# Awkward forms to rename
RENAME_AWKWARD = {
    "Licens": "License",
}


def fix_awkward_singulars():
    """Remove awkward singular forms and rename others."""
    print("=" * 80)
    print("FIX AWKWARD SINGULAR FORMS")
    print("=" * 80)
    print()

    # Create backup
    import shutil
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Created backup: {BACKUP_PATH}")
    print()

    # Load data
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    original_count = len(rows)
    print(f"✓ Loaded {original_count} rows")
    print()

    # Filter and rename
    print("Removing awkward duplicate forms:")
    print("-" * 80)

    deleted_count = 0
    renamed_count = 0
    filtered_rows = []

    for row in rows:
        # Check if should delete
        if row['new_tag'] in DELETE_AWKWARD:
            print(f"  ✗ Deleted: '{row['new_tag']}' (proper form already exists)")
            deleted_count += 1
            continue

        # Check if should rename
        if row['new_tag'] in RENAME_AWKWARD:
            old_name = row['new_tag']
            new_name = RENAME_AWKWARD[old_name]
            print(f"  ✓ Renamed: '{old_name}' → '{new_name}'")
            row['new_tag'] = new_name
            row['old_tag'] = new_name
            renamed_count += 1

        filtered_rows.append(row)

    print()
    print(f"Deleted: {deleted_count} rows")
    print(f"Renamed: {renamed_count} rows")
    print()

    # Save
    fieldnames = ['new_tag', 'old_tag', 'action', 'notes']
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"✓ Saved updated CSV: {CSV_PATH}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original rows:    {original_count}")
    print(f"Deleted:          {deleted_count}")
    print(f"Renamed:          {renamed_count}")
    print(f"Final rows:       {len(filtered_rows)}")
    print()


if __name__ == "__main__":
    fix_awkward_singulars()
