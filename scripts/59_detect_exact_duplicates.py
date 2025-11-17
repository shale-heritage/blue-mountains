#!/usr/bin/env python3
"""
Script 59: Detect and Remove Exact Duplicate Entries

Detects exact duplicate rows in the taxonomy CSV and removes them.

An exact duplicate is a row where ALL fields are identical to another row.
This is different from polyhierarchical relationships where the same term
appears with different parents.

This script:
1. Detects exact duplicates (same old_tag, new_tag, action, notes, status)
2. Reports duplicates found
3. Creates backup
4. Removes duplicates (keeping first occurrence)
5. Validates results

Author: Claude Code
Date: 2025-11-17
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def backup_file(file_path: Path) -> Path:
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def detect_exact_duplicates(csv_path: Path) -> tuple[list, dict]:
    """
    Detect exact duplicate rows.

    Returns: (all_rows, duplicates_dict)
    - all_rows: list of all rows from CSV
    - duplicates_dict: dict mapping row_tuple -> list of row indices
    """
    rows = []
    duplicates = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for idx, row in enumerate(reader):
            rows.append(row)

            # Create tuple of all field values for duplicate detection
            row_tuple = tuple(row[field] for field in fieldnames)
            duplicates[row_tuple].append(idx)

    # Filter to only actual duplicates (appearing more than once)
    duplicates_dict = {k: v for k, v in duplicates.items() if len(v) > 1}

    return rows, duplicates_dict, fieldnames


def remove_duplicates(rows: list, duplicates_dict: dict, fieldnames: list) -> list:
    """
    Remove duplicate rows, keeping first occurrence.

    Returns: list of deduplicated rows
    """
    # Track which row indices to keep
    rows_to_keep = set(range(len(rows)))

    for row_tuple, indices in duplicates_dict.items():
        # Keep first occurrence, remove the rest
        for idx in indices[1:]:
            rows_to_keep.discard(idx)

    # Return deduplicated rows
    deduplicated = [rows[i] for i in sorted(rows_to_keep)]
    return deduplicated


def main():
    """Detect and remove exact duplicate entries."""
    csv_path = Path('data/tag_map_consolidated.csv')

    print("="*80)
    print("EXACT DUPLICATE DETECTION AND REMOVAL")
    print("="*80)
    print()

    # Detect duplicates
    print("Scanning for exact duplicates...")
    rows, duplicates_dict, fieldnames = detect_exact_duplicates(csv_path)
    print(f"Total rows: {len(rows)}")
    print(f"Exact duplicates found: {len(duplicates_dict)}")
    print()

    if not duplicates_dict:
        print("="*80)
        print("✓ NO EXACT DUPLICATES FOUND")
        print("="*80)
        print()
        print("All entries in the taxonomy are unique.")
        return

    # Calculate total duplicate rows to remove
    total_duplicates = sum(len(indices) - 1 for indices in duplicates_dict.values())
    print(f"Duplicate rows to remove: {total_duplicates}")
    print()

    # Show sample duplicates
    print("="*80)
    print("SAMPLE DUPLICATES (first 10):")
    print("="*80)
    print()

    for i, (row_tuple, indices) in enumerate(sorted(duplicates_dict.items())[:10], 1):
        # Reconstruct row dict from tuple
        row_dict = dict(zip(fieldnames, row_tuple))
        print(f"{i}. {row_dict['new_tag']}")
        print(f"   Action: {row_dict['action']}")
        print(f"   Notes: {row_dict['notes']}")
        print(f"   Occurrences: {len(indices)}")
        print()

    if len(duplicates_dict) > 10:
        print(f"... and {len(duplicates_dict) - 10} more duplicate patterns")
        print()

    # Create backup
    print("Creating backup...")
    backup_file(csv_path)
    print()

    # Remove duplicates
    print("Removing duplicates...")
    deduplicated_rows = remove_duplicates(rows, duplicates_dict, fieldnames)
    print(f"Rows after deduplication: {len(deduplicated_rows)}")
    print()

    # Write deduplicated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduplicated_rows)

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Original rows: {len(rows)}")
    print(f"Duplicate patterns found: {len(duplicates_dict)}")
    print(f"Duplicate rows removed: {total_duplicates}")
    print(f"Final rows: {len(deduplicated_rows)}")
    print(f"Net change: -{total_duplicates} rows")
    print()

    # Show breakdown by type
    hierarchy_dupes = sum(1 for row_tuple, _ in duplicates_dict.items()
                          if dict(zip(fieldnames, row_tuple))['action'] == 'hierarchy')
    synonym_dupes = sum(1 for row_tuple, _ in duplicates_dict.items()
                        if dict(zip(fieldnames, row_tuple))['action'] == 'synonym')

    print("Breakdown by action:")
    print(f"  Hierarchy duplicates: {hierarchy_dupes}")
    print(f"  Synonym duplicates: {synonym_dupes}")
    print(f"  Other: {len(duplicates_dict) - hierarchy_dupes - synonym_dupes}")
    print()

    print("="*80)
    print("✓ DEDUPLICATION COMPLETE")
    print("="*80)
    print()
    print("Next steps:")
    print("  1. Review changes: git diff data/tag_map_consolidated.csv")
    print("  2. Verify key entries are correct")
    print("  3. Re-run duplicate detection: python scripts/58_detect_duplicate_leaf_nodes.py")
    print()


if __name__ == '__main__':
    main()
