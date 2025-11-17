#!/usr/bin/env python3
"""
Fix Bankruptcy Taxonomy Entries

Issue: "Bankruptcy" (capitalized) has hierarchy entries when it should only be a
synonym pointing to "bankruptcy" (lowercase).

Current state:
- bankruptcy,bankruptcy,hierarchy,parent=legal events ✓ CORRECT
- bankruptcy,bankruptcy,hierarchy,parent=Economic distress - THEMATIC ✓ CORRECT
- bankruptcy,bankruptcy,hierarchy,parent=Economic hardship - THEMATIC ✓ CORRECT
- bankruptcy,bankruptcy,hierarchy,parent=Legal outcomes - THEMATIC ✓ CORRECT
- Bankruptcy,bankruptcy,synonym,... ✓ CORRECT
- Bankruptcy,Bankruptcy,hierarchy,parent=Legal outcomes - THEMATIC ✗ REMOVE
- Bankruptcy,Bankruptcy,hierarchy,parent=Economic hardship - THEMATIC ✗ REMOVE
- Bankruptcy,Bankruptcy,hierarchy,parent=Economic distress - THEMATIC ✗ REMOVE

Fix: Remove the capitalized "Bankruptcy" hierarchy entries, keeping only the synonym.

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
    """Fix bankruptcy entries."""
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

    # Remove incorrect capitalized Bankruptcy hierarchy entries
    entries_to_remove = [
        ["Bankruptcy", "Bankruptcy", "hierarchy", "parent=Legal outcomes - THEMATIC"],
        ["Bankruptcy", "Bankruptcy", "hierarchy", "parent=Economic hardship - THEMATIC"],
        ["Bankruptcy", "Bankruptcy", "hierarchy", "parent=Economic distress - THEMATIC"],
    ]

    for entry in entries_to_remove:
        if entry in entries:
            entries.remove(entry)
            removed_entries.append(entry)
            print(f"Removed: {entry}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print(f"Net change: -{len(removed_entries)} entries")

    # Summary report
    print("\n=== Summary ===")
    print(f"\nRemoved {len(removed_entries)} incorrect capitalized Bankruptcy hierarchy entries")

    print("\nCorrect bankruptcy structure now:")
    print("  ✓ bankruptcy → bankruptcy (hierarchy under legal events)")
    print("  ✓ bankruptcy → bankruptcy (hierarchy under Economic distress - THEMATIC)")
    print("  ✓ bankruptcy → bankruptcy (hierarchy under Economic hardship - THEMATIC)")
    print("  ✓ bankruptcy → bankruptcy (hierarchy under Legal outcomes - THEMATIC)")
    print("  ✓ Bankruptcy → bankruptcy (synonym)")

    print("\n✓ Bankruptcy entries corrected")


if __name__ == "__main__":
    main()
