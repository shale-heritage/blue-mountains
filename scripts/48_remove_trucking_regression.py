#!/usr/bin/env python3
"""
Remove Trucking Regression Entries

This script removes the regressed "Trucking" hierarchy entries that refer to
commercial trucking/logistics. "Trucking" was previously corrected to refer
only to the "truck system" (historical exploitative labour practice).

Regression occurred when script 22 regenerated hierarchies and re-added these
entries from the primary facet generation logic.

Entries to remove:
1. Trucking,Trucking,hierarchy,parent=transport & logistics businesses
2. Trucking,Trucking,hierarchy,parent=transport
3. Trucking,Trucking,hierarchy,parent=Commercial transport - THEMATIC
4. Trucking,Trucking,hierarchy,parent=Transport & logistics businesses
5. Trucking,Trucking,hierarchy,parent=Transport

Entries to preserve:
- truck system,truck system,hierarchy,parent=economic activities
- trucking,truck system,synonym,... (historical term for truck system)

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
    """Remove Trucking regression entries."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")

    # Track changes
    removed_entries = []

    # Remove regression entries (all "Trucking" hierarchy entries)
    entries_to_remove = [
        ["Trucking", "Trucking", "hierarchy", "parent=transport & logistics businesses"],
        ["Trucking", "Trucking", "hierarchy", "parent=transport"],
        ["Trucking", "Trucking", "hierarchy", "parent=Commercial transport - THEMATIC"],
        ["Trucking", "Trucking", "hierarchy", "parent=Transport & logistics businesses"],
        ["Trucking", "Trucking", "hierarchy", "parent=Transport"],
    ]

    for entry in entries_to_remove:
        if entry in entries:
            entries.remove(entry)
            removed_entries.append(entry)
            print(f"Removed: {entry}")
        else:
            print(f"Not found (already removed?): {entry}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print(f"Net change: -{len(removed_entries)} entries")

    # Summary report
    print("\n=== Summary ===")
    print(f"\nRemoved {len(removed_entries)} Trucking regression entries:")
    for entry in removed_entries:
        print(f"  - {entry[0]} → {entry[1]} ({entry[3]})")

    print("\nPreserved correct entries:")
    print("  ✓ truck system,truck system,hierarchy,parent=economic activities")
    print("  ✓ trucking,truck system,synonym,... (historical term)")

    print("\n✓ Regression corrections complete")
    print("\nNext steps:")
    print("1. Regenerate visualisations to verify Trucking is gone")
    print("2. Update script 22 to prevent future regeneration of Trucking")


if __name__ == "__main__":
    main()
