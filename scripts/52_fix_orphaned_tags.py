#!/usr/bin/env python3
"""
Fix Orphaned Tags

The validation report identified 2 orphaned tags that appear in mappings but don't
have proper synonym relationships to the new qualified forms:

1. "cottage" → needs synonyms to cottage (building) and cottage (business)
2. "public house" → needs synonyms to public house (building) and public house (business)

The issue is capitalization: old tags use Title Case ("Cottage", "Public house")
but the new taxonomy uses lowercase with qualifiers.

This script adds the missing synonym mappings.

Author: Claude Code
Date: 2025-11-16
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime


def backup_file(file_path: Path) -> Path:
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def main():
    """Fix orphaned tags."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")

    # New synonym entries to fix orphaned tags
    new_entries = [
        # Cottage synonyms (lowercase variant)
        ["cottage", "cottage (building)", "synonym",
         "Lowercase variant - maps to building aspect"],
        ["cottage", "cottage (business)", "synonym",
         "Lowercase variant - maps to business aspect"],

        # Cottage synonyms (Title Case variant)
        ["Cottage", "cottage (building)", "synonym",
         "Capitalized variant - maps to building aspect"],
        ["Cottage", "cottage (business)", "synonym",
         "Capitalized variant - maps to business aspect"],

        # Public house synonyms (lowercase variant)
        ["public house", "public house (building)", "synonym",
         "Unqualified form - maps to building aspect"],
        ["public house", "public house (business)", "synonym",
         "Unqualified form - maps to business aspect"],

        # Public house synonyms (Title Case variant)
        ["Public house", "public house (building)", "synonym",
         "Title Case variant - maps to building aspect"],
        ["Public house", "public house (business)", "synonym",
         "Title Case variant - maps to business aspect"],
    ]

    # Add new entries (check for duplicates first)
    added_count = 0
    for entry in new_entries:
        if entry not in entries:
            entries.append(entry)
            added_count += 1
            print(f"Added: {entry[:2]}")
        else:
            print(f"Already exists: {entry[:2]}")

    # Remove old unqualified hierarchy entries that should now be synonyms
    entries_to_remove = [
        ["Cottage", "Cottage", "hierarchy", "parent=Cottages"],
        ["Public house", "Public house", "hierarchy", "parent=Public houses"],
    ]

    removed_count = 0
    for entry in entries_to_remove:
        if entry in entries:
            entries.remove(entry)
            removed_count += 1
            print(f"Removed obsolete: {entry[:2]}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print(f"Added: {added_count} synonym entries")
    print(f"Removed: {removed_count} obsolete hierarchy entries")
    print(f"Net change: {added_count - removed_count:+d}")

    print("\n=== Summary ===")
    print("\nFixed orphaned tags:")
    print("  ✓ cottage → cottage (building) + cottage (business)")
    print("  ✓ Cottage → cottage (building) + cottage (business)")
    print("  ✓ public house → public house (building) + public house (business)")
    print("  ✓ Public house → public house (building) + public house (business)")

    print("\n✓ Orphaned tags fixed - all variants now map to qualified forms")


if __name__ == "__main__":
    main()
