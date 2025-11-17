#!/usr/bin/env python3
"""
Deduplicate Taxonomy Entries

Remove exact duplicate rows from tag_map_consolidated.csv while preserving order.
This handles duplicates created when multiple scripts add the same entries.

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
    """Deduplicate taxonomy entries."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        entries = list(reader)

    print(f"Total entries before deduplication: {len(entries)}")

    # Deduplicate while preserving order
    seen = set()
    unique_entries = []
    duplicates = []

    for entry in entries:
        entry_tuple = tuple(entry)
        if entry_tuple not in seen:
            seen.add(entry_tuple)
            unique_entries.append(entry)
        else:
            duplicates.append(entry)

    # Write deduplicated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(unique_entries)

    print(f"Total entries after deduplication: {len(unique_entries)}")
    print(f"Duplicates removed: {len(duplicates)}")

    if duplicates:
        print("\nDuplicate entries removed:")
        # Group duplicates by entry for cleaner output
        from collections import Counter
        duplicate_counts = Counter(tuple(d) for d in duplicates)
        for entry, count in duplicate_counts.most_common(10):
            print(f"  {count}x: {list(entry)[:2]}...")  # Show first 2 fields

    print("\n✓ Deduplication complete")


if __name__ == "__main__":
    main()
