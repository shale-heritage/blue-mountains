#!/usr/bin/env python3
"""
Remove duplicate organisation tag entries.

Removes capitalised duplicates of:
- Cultural organisations
- Military organisations
- Temperance organisations & movements

Keeps the lowercase versions.
"""

import csv
import sys
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
BACKUP_FILE = TAG_MAP_FILE.with_suffix('.csv.backup-remove-org-duplicates')

# Duplicates to remove (keep lowercase, remove title case)
DUPLICATES_TO_REMOVE = {
    'Cultural organisations',
    'Military organisations',
    'Temperance organisations & movements',
}

def load_taxonomy():
    """Load the taxonomy CSV file."""
    rows = []
    with open(TAG_MAP_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def remove_duplicates(rows):
    """Remove specified duplicate entries."""
    cleaned_rows = []
    removed_count = 0
    removed_items = []

    for row in rows:
        tag_name = row['new_tag']
        if tag_name in DUPLICATES_TO_REMOVE:
            removed_items.append(f"{tag_name} (parent: {row.get('parent_broader_category', '')})")
            removed_count += 1
            print(f"  Removing: {tag_name}")
            continue
        cleaned_rows.append(row)

    return cleaned_rows, removed_count, removed_items

def save_taxonomy(rows):
    """Save the cleaned taxonomy."""
    # Create backup
    if TAG_MAP_FILE.exists():
        import shutil
        shutil.copy2(TAG_MAP_FILE, BACKUP_FILE)
        print(f"✓ Backup created: {BACKUP_FILE}")

    # Write cleaned data
    fieldnames = rows[0].keys()
    with open(TAG_MAP_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Cleaned taxonomy saved: {TAG_MAP_FILE}")

def main():
    print("=" * 70)
    print("REMOVE DUPLICATE ORGANISATION ENTRIES")
    print("=" * 70)
    print()

    # Load taxonomy
    print("Loading taxonomy...")
    rows = load_taxonomy()
    print(f"✓ Loaded {len(rows)} rows")
    print()

    # Remove duplicates
    print("Removing duplicate entries...")
    cleaned_rows, removed_count, removed_items = remove_duplicates(rows)
    print(f"✓ Removed {removed_count} duplicate rows")
    print()

    if removed_items:
        print("Removed entries:")
        for item in removed_items:
            print(f"  - {item}")
        print()

    # Save
    save_taxonomy(cleaned_rows)

    print()
    print("=" * 70)
    print("COMPLETE: Duplicate organisation entries removed")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - Original rows: {len(rows)}")
    print(f"  - Removed: {removed_count}")
    print(f"  - Final rows: {len(cleaned_rows)}")
    print(f"  - Backup saved: {BACKUP_FILE.name}")
    print()

if __name__ == '__main__':
    main()
