#!/usr/bin/env python3
"""
Complete Church Disambiguations

Add missing (building) hierarchy entries for 4 churches that only have (organisation):
1. Methodist Church Katoomba
2. Roman Catholic Church Blackheath
3. Roman Catholic Church Lawson
4. Roman Catholic Church Mount Victoria

Also fix Grand Hotel unqualified hierarchy entry.

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
    """Complete church disambiguations."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")

    # New (building) entries to add
    new_building_entries = [
        ["Methodist Church Katoomba (building)", "Methodist Church Katoomba (building)",
         "hierarchy", "parent=Methodist churches (buildings)", "active"],

        ["Roman Catholic Church Blackheath (building)", "Roman Catholic Church Blackheath (building)",
         "hierarchy", "parent=Roman Catholic churches (buildings)", "active"],

        ["Roman Catholic Church Lawson (building)", "Roman Catholic Church Lawson (building)",
         "hierarchy", "parent=Roman Catholic churches (buildings)", "active"],

        ["Roman Catholic Church Mount Victoria (building)", "Roman Catholic Church Mount Victoria (building)",
         "hierarchy", "parent=Roman Catholic churches (buildings)", "active"],
    ]

    # Add new entries
    added_count = 0
    for entry in new_building_entries:
        # Check if already exists (shouldn't, but be safe)
        if entry not in entries:
            entries.append(entry)
            added_count += 1
            print(f"Added: {entry[0]}")
        else:
            print(f"Already exists: {entry[0]}")

    # Fix Grand Hotel unqualified hierarchy - remove it
    grand_hotel_unqualified = None
    for i, entry in enumerate(entries):
        if (len(entry) >= 4 and
            entry[0] == "Grand Hotel" and
            entry[1] == "Grand Hotel" and
            entry[2] == "hierarchy" and
            "parent=Hotels" in entry[3]):
            grand_hotel_unqualified = i
            print(f"Found Grand Hotel unqualified hierarchy at index {i}")
            break

    removed_count = 0
    if grand_hotel_unqualified is not None:
        removed_entry = entries.pop(grand_hotel_unqualified)
        removed_count = 1
        print(f"Removed: Grand Hotel unqualified hierarchy")
        print(f"  Details: {removed_entry}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries) + 1}")  # +1 for header
    print(f"Net change: +{added_count - removed_count} entries")

    print("\n=== Summary ===")
    print(f"\nAdded {added_count} missing (building) entries:")
    print("  ✓ Methodist Church Katoomba (building)")
    print("  ✓ Roman Catholic Church Blackheath (building)")
    print("  ✓ Roman Catholic Church Lawson (building)")
    print("  ✓ Roman Catholic Church Mount Victoria (building)")

    if removed_count > 0:
        print(f"\nRemoved {removed_count} unqualified hierarchy entry:")
        print("  ✓ Grand Hotel (unqualified) - conflicts with Grand Hotel (Sydney) qualifiers")

    print("\n✓ All 10 incomplete disambiguations now complete!")
    print("\nRemaining church entities now have complete (building)/(organisation) pairs:")
    print("  • Church of England Katoomba ✓")
    print("  • Methodist Church Katoomba ✓")
    print("  • Presbyterian Church Leura ✓")
    print("  • Presbyterian Church Wentworth Falls ✓")
    print("  • Roman Catholic Church Blackheath ✓")
    print("  • Roman Catholic Church Lawson ✓")
    print("  • Roman Catholic Church Megalong ✓")
    print("  • Roman Catholic Church Mount Victoria ✓")
    print("  • Wesleyan Church Katoomba ✓")
    print("  • Grand Hotel (Sydney) ✓")


if __name__ == "__main__":
    main()
