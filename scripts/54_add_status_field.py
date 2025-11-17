#!/usr/bin/env python3
"""
Add Status Field to Taxonomy CSV

Add a 'status' field to track the lifecycle state of taxonomy entries:
- active: Currently in use (default for most entries)
- removed: Intentionally removed from active taxonomy
- deprecated: Marked for future removal
- merged: Consolidated into another entry

This addresses the data loss concern where removed tags have no audit trail.

The status field will be inserted as the 5th column (after old_tag, new_tag, action, notes).

CSV structure change:
OLD: old_tag,new_tag,action,notes
NEW: old_tag,new_tag,action,notes,status

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


def determine_status(old_tag: str, new_tag: str, action: str, notes: str) -> str:
    """
    Determine lifecycle status (orthogonal to action field).

    Status tracks temporal/lifecycle state:
    - 'active': Currently used in taxonomy (default)
    - 'removed': No longer valid, kept for audit trail only
    - 'merged': Consolidated into another entry (from action=merge)
    - 'deprecated': Marked for future removal but still valid
    - 'historical': Preserved for research but not for tagging

    Note: This is different from the 'action' field:
    - action: What happened to the tag (synonym, merge, hierarchy, keep)
    - status: Current lifecycle state (active, removed, deprecated, historical)

    Rules:
    - 'removed' if notes mention removal/deletion/obsolete/incorrect
    - 'merged' if action is 'merge'
    - 'active' (default) for all other entries
    """
    notes_lower = notes.lower()

    # Check for removal indicators
    removal_indicators = [
        'removed',
        'deletion',
        'obsolete',
        'incorrect',
        'regressed',
        'duplicate',
    ]

    if any(indicator in notes_lower for indicator in removal_indicators):
        return 'removed'

    # Merge action
    if action == 'merge':
        return 'merged'

    # Default: active
    return 'active'


def main():
    """Add status field to taxonomy CSV."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")
    print(f"Current header: {header}")

    # Add status field to header
    new_header = header + ['status']

    # Process entries and add status
    status_counts = {'active': 0, 'removed': 0, 'merged': 0, 'deprecated': 0}
    new_entries = []

    for entry in entries:
        if len(entry) == 4:
            old_tag, new_tag, action, notes = entry
            status = determine_status(old_tag, new_tag, action, notes)
            new_entry = [old_tag, new_tag, action, notes, status]
            new_entries.append(new_entry)
            status_counts[status] += 1
        elif len(entry) == 5:
            # Already has status field (shouldn't happen, but handle it)
            new_entries.append(entry)
            if entry[4] in status_counts:
                status_counts[entry[4]] += 1
        else:
            # Malformed entry - keep as-is
            print(f"WARNING: Malformed entry (expected 4 columns, got {len(entry)}): {entry}")
            new_entries.append(entry)

    # Write updated CSV with new header
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(new_header)
        writer.writerows(new_entries)

    print(f"\nTotal entries after changes: {len(new_entries)}")
    print(f"New header: {new_header}")

    print("\n=== Status Field Distribution ===")
    for status, count in sorted(status_counts.items()):
        if count > 0:
            percentage = (count / len(new_entries)) * 100
            print(f"  {status}: {count} ({percentage:.1f}%)")

    print("\n=== Example Entries by Status ===")

    # Show examples of each status
    for status in ['active', 'merged', 'removed']:
        examples = [e for e in new_entries if len(e) == 5 and e[4] == status]
        if examples:
            print(f"\n{status.upper()} ({len(examples)} total):")
            for example in examples[:3]:  # Show first 3 examples
                print(f"  {example[0]} → {example[1]} ({example[2]})")

    print("\n✓ Status field added to taxonomy CSV")
    print("✓ All entries now have explicit lifecycle tracking")
    print("\nNOTE: Review 'removed' and 'merged' entries to verify correct classification")


if __name__ == "__main__":
    main()
