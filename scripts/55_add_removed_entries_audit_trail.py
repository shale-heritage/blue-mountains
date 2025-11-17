#!/usr/bin/env python3
"""
Add Removed Entries Audit Trail

Add explicit entries for tags that were physically removed from the taxonomy,
marking them with status=removed to maintain complete audit trail.

Entries added:
- 5 Trucking hierarchy entries (removed by script 48)
- 3 Bankruptcy hierarchy entries (removed by script 51)
- 2 Cottage/Public house hierarchy entries (removed by script 52)

Total: 10 removed entries to document

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
    """Add removed entries to taxonomy CSV for audit trail."""
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

    # Removed entries to document (from scripts 48, 51, 52)
    removed_entries = [
        # Script 48 - Trucking regression removals
        ["Trucking", "Trucking", "hierarchy",
         "parent=transport & logistics businesses - REMOVED by script 48 (regression)",
         "removed"],
        ["Trucking", "Trucking", "hierarchy",
         "parent=transport - REMOVED by script 48 (regression)",
         "removed"],
        ["Trucking", "Trucking", "hierarchy",
         "parent=Commercial transport - THEMATIC - REMOVED by script 48 (regression)",
         "removed"],
        ["Trucking", "Trucking", "hierarchy",
         "parent=Transport & logistics businesses - REMOVED by script 48 (regression)",
         "removed"],
        ["Trucking", "Trucking", "hierarchy",
         "parent=Transport - REMOVED by script 48 (regression)",
         "removed"],

        # Script 51 - Bankruptcy incorrect capitalized hierarchies
        ["Bankruptcy", "Bankruptcy", "hierarchy",
         "parent=Legal outcomes - THEMATIC - REMOVED by script 51 (incorrect capitalization)",
         "removed"],
        ["Bankruptcy", "Bankruptcy", "hierarchy",
         "parent=Economic hardship - THEMATIC - REMOVED by script 51 (incorrect capitalization)",
         "removed"],
        ["Bankruptcy", "Bankruptcy", "hierarchy",
         "parent=Economic distress - THEMATIC - REMOVED by script 51 (incorrect capitalization)",
         "removed"],

        # Script 52 - Obsolete unqualified hierarchies
        ["Cottage", "Cottage", "hierarchy",
         "parent=Cottages - REMOVED by script 52 (obsolete unqualified form)",
         "removed"],
        ["Public house", "Public house", "hierarchy",
         "parent=Public houses - REMOVED by script 52 (obsolete unqualified form)",
         "removed"],
    ]

    # Add removed entries to the end
    added_count = 0
    for entry in removed_entries:
        entries.append(entry)
        added_count += 1
        print(f"Added removed entry: {entry[0]} (hierarchy, parent={entry[3].split(' - REMOVED')[0].replace('parent=', '')})")

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(entries)

    print(f"\nTotal entries after changes: {len(entries)}")
    print(f"Added: {added_count} removed entries for audit trail")

    # Count removed status entries
    removed_count = sum(1 for e in entries if len(e) == 5 and e[4] == 'removed')
    print(f"Total 'removed' status entries: {removed_count}")

    print("\n=== Audit Trail Complete ===")
    print("\nRemoved entries now documented:")
    print("  • 5 Trucking hierarchy entries (script 48 - regression fix)")
    print("  • 3 Bankruptcy hierarchy entries (script 51 - capitalization fix)")
    print("  • 2 Cottage/Public house hierarchies (script 52 - obsolete unqualified forms)")
    print("\n✓ Complete audit trail of removed tags established")


if __name__ == "__main__":
    main()
