#!/usr/bin/env python3
"""
Add Trucking Synonym Mapping

This script adds a synonym mapping for "Trucking" (capitalized) to redirect to
"truck system". Currently 8 items are tagged with "Trucking" but there's no
mapping for them.

Current state:
- "trucking" (lowercase) → "truck system" (synonym exists)
- "Trucking" (capitalized) → NO MAPPING (8 items orphaned)

This adds:
- "Trucking" (capitalized) → "truck system" (synonym)

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
    """Add Trucking synonym mapping."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")

    # Check if entry already exists
    new_entry = ["Trucking", "truck system", "synonym",
                 "Capitalized variant - historical term for the truck system (19th century exploitative labour practice)"]

    if new_entry in entries:
        print("Entry already exists, no changes needed")
        return

    # Add new entry
    entries.append(new_entry)
    print(f"Added: {new_entry}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print("Net change: +1 entry")

    # Summary report
    print("\n=== Summary ===")
    print("\nTruck system mappings now complete:")
    print("  ✓ truck system → truck system (hierarchy under economic activities)")
    print("  ✓ trucking (lowercase) → truck system (synonym)")
    print("  ✓ Trucking (capitalized) → truck system (synonym) [NEW]")

    print("\n✓ 8 items tagged with 'Trucking' will now map to 'truck system'")


if __name__ == "__main__":
    main()
