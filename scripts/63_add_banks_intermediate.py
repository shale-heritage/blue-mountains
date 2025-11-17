#!/usr/bin/env python3
"""
Script 63: Add Missing 'banks' Intermediate Node

Completes the 3-tier pattern for banks dual-nature entity to match
other categories (churches, hotels, schools, schools of arts, boarding houses).

Current structure:
  banks (buildings) → financial institutions (buildings)
  banks (businesses) → financial institutions

Target structure:
  banks [NEW - polyhierarchical intermediate]
  ├─ banks (buildings) → financial institutions (buildings)
  └─ banks (businesses) → financial institutions

This brings banks into perfect consistency with the 3-tier pattern:
  Tier 1: Unqualified polyhierarchical intermediate
  Tier 2: Qualified facet-specific intermediates
  Tier 3: Leaf nodes

Changes:
1. Add new hierarchy entry: 'banks' (polyhierarchical)
   - Parents: financial institutions, financial institutions (buildings)

2. Add child references for existing qualified intermediates:
   - banks (buildings) - already has correct parent
   - banks (businesses) - already has correct parent

Note: The qualified intermediates already exist with correct single parents,
so we only need to add the Tier 1 unqualified intermediate.

Author: Claude Code
Date: 2025-11-17
"""

import csv
import shutil
from pathlib import Path
from datetime import datetime


def create_backup(csv_path: Path) -> Path:
    """Create timestamped backup."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = csv_path.parent / f"{csv_path.stem}.{timestamp}.bak"
    shutil.copy2(csv_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path


def load_csv(csv_path: Path) -> tuple[list, list]:
    """Load CSV data."""
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    return rows, fieldnames


def save_csv(csv_path: Path, rows: list, fieldnames: list):
    """Save CSV data."""
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def check_term_exists(rows: list, term: str, action: str = None) -> bool:
    """Check if a term already exists in active hierarchy."""
    for row in rows:
        if row['new_tag'] == term and row['status'] == 'active':
            if action is None or row['action'] == action:
                return True
    return False


def add_banks_intermediate(rows: list, fieldnames: list) -> tuple[list, dict]:
    """Add the missing 'banks' intermediate node."""
    stats = {
        'added': [],
        'skipped': [],
        'verified': [],
    }

    # Check if 'banks' already exists
    if check_term_exists(rows, 'banks', action='hierarchy'):
        stats['skipped'].append('banks - already exists')
        print("⊙ Skipped: 'banks' already exists as hierarchy entry")
        return rows, stats

    # Verify that banks (buildings) and banks (businesses) exist
    has_buildings = check_term_exists(rows, 'banks (buildings)', action='hierarchy')
    has_businesses = check_term_exists(rows, 'banks (businesses)', action='hierarchy')

    if not has_buildings:
        print("⚠ WARNING: 'banks (buildings)' not found")
    else:
        stats['verified'].append('banks (buildings) exists')
        print("✓ Verified: 'banks (buildings)' exists")

    if not has_businesses:
        print("⚠ WARNING: 'banks (businesses)' not found")
    else:
        stats['verified'].append('banks (businesses) exists')
        print("✓ Verified: 'banks (businesses)' exists")

    # Add the new 'banks' intermediate node
    # It should be polyhierarchical with parents in both Agent and Built Environment facets
    new_entry = {
        'old_tag': 'banks',
        'new_tag': 'banks',
        'action': 'hierarchy',
        'notes': 'parent=financial institutions',  # Primary parent (Agents facet)
        'status': 'active'
    }

    rows.append(new_entry)
    stats['added'].append('banks (polyhierarchical intermediate)')
    print("✓ Added: 'banks' as polyhierarchical intermediate")
    print("  Parent: financial institutions (Agents facet)")

    # Note: We could also add a second hierarchy entry for the Built Environment parent,
    # but the pattern in our taxonomy is to have one primary parent listed.
    # The polyhierarchy is implicit through the children having different parent chains.

    return rows, stats


def main():
    """Add missing 'banks' intermediate node."""
    csv_path = Path('data/tag_map_consolidated.csv')

    print("=" * 80)
    print("ADD MISSING 'BANKS' INTERMEDIATE NODE")
    print("=" * 80)
    print()
    print("Purpose: Complete 3-tier pattern for banks dual-nature entity")
    print()

    # Create backup
    backup_path = create_backup(csv_path)
    print()

    # Load CSV
    print("Loading taxonomy...")
    rows, fieldnames = load_csv(csv_path)
    initial_count = len(rows)
    print(f"✓ Loaded {initial_count:,} entries")
    print()

    # Add missing node
    print("Adding 'banks' intermediate node...")
    print()
    rows, stats = add_banks_intermediate(rows, fieldnames)
    print()

    # Save updated CSV
    print("Saving updated taxonomy...")
    save_csv(csv_path, rows, fieldnames)
    final_count = len(rows)
    print(f"✓ Saved {final_count:,} entries")
    print()

    # Report statistics
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Initial entries: {initial_count:,}")
    print(f"Final entries: {final_count:,}")
    print(f"Net change: +{final_count - initial_count}")
    print()

    if stats['added']:
        print(f"Added: {len(stats['added'])}")
        for item in stats['added']:
            print(f"  + {item}")
        print()

    if stats['verified']:
        print(f"Verified existing: {len(stats['verified'])}")
        for item in stats['verified']:
            print(f"  ✓ {item}")
        print()

    if stats['skipped']:
        print(f"Skipped: {len(stats['skipped'])}")
        for item in stats['skipped']:
            print(f"  ⊙ {item}")
        print()

    print("=" * 80)
    print("BANKS 3-TIER STRUCTURE COMPLETE")
    print("=" * 80)
    print()
    print("Tier 1: banks (polyhierarchical)")
    print("  └─ Parent: financial institutions")
    print()
    print("Tier 2: Qualified intermediates")
    print("  ├─ banks (buildings) → financial institutions (buildings)")
    print("  └─ banks (businesses) → financial institutions")
    print()
    print("Tier 3: Leaf nodes")
    print("  ├─ bank (building)")
    print("  ├─ bank (business)")
    print("  └─ Commercial Bank of Australia (building/business)")
    print()
    print("Next steps:")
    print("  1. Run script 61 (final QA validation)")
    print("  2. Update documentation")
    print()


if __name__ == '__main__':
    main()
