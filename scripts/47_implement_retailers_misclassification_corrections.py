#!/usr/bin/env python3
"""
Implement Retailers Misclassification Corrections

This script corrects misclassified "Retailers and stores" entries identified in
entity-tagging-system/outputs/retailers/misclassification-correction-report.md

Changes implemented:
1. Remove Nimmo's from "Retailers and stores"
2. Add Railway Hotel Katoomba (building) and (business) under Hotels
3. Remove Peckman Bros/Brothers from "Retailers and stores"
4. Add Peckman Brothers (business) under Transport & logistics businesses > Coach services

Evidence basis: Full-text context analysis from Zotero items (see report for details)

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
    """Implement retailers misclassification corrections."""
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

    # Remove misclassified entries
    entries_to_remove = [
        ["Nimmo's", "Nimmo's", "hierarchy", "parent=retailers and stores"],
        ["Nimmo's", "Nimmo's", "hierarchy", "parent=Retailers and stores"],
        ["Peckman Bros", "Peckman Bros", "hierarchy", "parent=Retailers and stores"],
        ["Peckman Brothers", "Peckman Brothers", "hierarchy", "parent=retailers and stores"],
    ]

    for entry in entries_to_remove:
        if entry in entries:
            entries.remove(entry)
            removed_entries.append(entry)
            print(f"Removed: {entry}")

    # Add correct entries for Railway Hotel Katoomba
    new_railway_hotel_entries = [
        ["Railway Hotel Katoomba (building)", "Railway Hotel Katoomba (building)",
         "hierarchy", "parent=hotels (buildings)"],
        ["Railway Hotel Katoomba (business)", "Railway Hotel Katoomba (business)",
         "hierarchy", "parent=hotels (businesses)"],
        ["Nimmo's Railway Hotel", "Railway Hotel Katoomba (building)",
         "synonym", "Full historical name - maps to building"],
        ["Nimmo's Railway Hotel", "Railway Hotel Katoomba (business)",
         "synonym", "Full historical name - maps to business"],
        ["Nimmo's", "Railway Hotel Katoomba (building)",
         "synonym", "Short form - maps to building"],
        ["Nimmo's", "Railway Hotel Katoomba (business)",
         "synonym", "Short form - maps to business"],
    ]

    # Add coach services category and Peckman Brothers
    new_transport_entries = [
        ["coach services", "coach services", "hierarchy",
         "parent=transport & logistics businesses"],
        ["coach service", "coach service", "hierarchy",
         "parent=coach services (singular generic term)"],
        ["Peckman Brothers (business)", "Peckman Brothers (business)",
         "hierarchy", "parent=coach services"],
        ["Peckman Bros", "Peckman Brothers (business)",
         "synonym", "Abbreviated form - use full Peckman Brothers"],
    ]

    # Add new entries
    added_entries = []
    for entry in new_railway_hotel_entries + new_transport_entries:
        if entry not in entries:
            entries.append(entry)
            added_entries.append(entry)
            print(f"Added: {entry}")
        else:
            print(f"Already exists: {entry}")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print(f"Net change: {len(entries) - (len(entries) - len(added_entries) + len(removed_entries))}")
    print(f"Removed: {len(removed_entries)} entries")
    print(f"Added: {len(added_entries)} entries")

    # Summary report
    print("\n=== Summary ===")
    print("\nRemoved (misclassified as retailers):")
    for entry in removed_entries:
        print(f"  - {entry[0]} → {entry[1]} ({entry[3]})")

    print("\nAdded (Railway Hotel Katoomba):")
    for entry in new_railway_hotel_entries:
        if entry in added_entries:
            print(f"  - {entry[0]} → {entry[1]} ({entry[2]})")

    print("\nAdded (Peckman Brothers - Transport):")
    for entry in new_transport_entries:
        if entry in added_entries:
            print(f"  - {entry[0]} → {entry[1]} ({entry[2]})")

    print("\n✓ Corrections implemented successfully")
    print("\nNext steps:")
    print("1. Review changes in data/tag_map_consolidated.csv")
    print("2. Apply item tags using entity-tagging-system/outputs/retailers/item_tag_application.csv")
    print("3. Document decision in planning/consolidation-decisions.md")


if __name__ == "__main__":
    main()
