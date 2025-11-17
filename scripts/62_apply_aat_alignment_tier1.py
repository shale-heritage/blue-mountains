#!/usr/bin/env python3
"""
Script 62: Apply Getty AAT Alignment Changes (Tier 1)

Implements low-cost structural changes to improve alignment with Getty AAT
before crosswalk mapping phase.

Changes:
1. Add "financial institutions (buildings)" intermediate node
   - Insert between commercial buildings > banks (buildings)
   - Update banks (buildings) parent reference

2. Add "public accommodations" intermediate node
   - Insert between accommodation buildings > hotels (buildings)
   - Update hotels (buildings) parent reference

3. Verify/add "commercial buildings" intermediate node
   - Ensure proper parent for financial/mercantile building types

Impact:
- Improved AAT alignment for banks and hotels hierarchies
- Cleaner crosswalk mapping
- Foundation for future expansion

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


def check_term_exists(rows: list, term: str) -> bool:
    """Check if a term already exists in active hierarchy."""
    for row in rows:
        if row['new_tag'] == term and row['status'] == 'active':
            return True
    return False


def apply_tier1_changes(rows: list, fieldnames: list) -> tuple[list, dict]:
    """Apply Tier 1 AAT alignment changes."""
    stats = {
        'added': [],
        'updated': [],
        'skipped': [],
    }

    # Change 1: Add "financial institutions (buildings)"
    # Check if it already exists
    if not check_term_exists(rows, 'financial institutions (buildings)'):
        new_entry = {
            'old_tag': 'financial institutions (buildings)',
            'new_tag': 'financial institutions (buildings)',
            'action': 'hierarchy',
            'notes': 'parent=commercial buildings',
            'status': 'active'
        }
        rows.append(new_entry)
        stats['added'].append('financial institutions (buildings)')
        print("✓ Added: financial institutions (buildings)")
    else:
        stats['skipped'].append('financial institutions (buildings) - already exists')
        print("⊙ Skipped: financial institutions (buildings) - already exists")

    # Update banks (buildings) parent reference
    updated_banks = False
    for row in rows:
        if (row['new_tag'] == 'banks (buildings)' and
            row['action'] == 'hierarchy' and
            row['status'] == 'active'):

            old_notes = row['notes']
            # Check if parent is already correct
            if 'parent=financial institutions (buildings)' in old_notes:
                stats['skipped'].append('banks (buildings) parent - already correct')
                print("⊙ Skipped: banks (buildings) parent - already correct")
            else:
                row['notes'] = 'parent=financial institutions (buildings)'
                stats['updated'].append(f'banks (buildings): {old_notes} → {row["notes"]}')
                print(f"✓ Updated: banks (buildings) parent reference")
                updated_banks = True

    if not updated_banks:
        print("⊙ Note: banks (buildings) not found or parent already correct")

    # Change 2: Add "public accommodations"
    if not check_term_exists(rows, 'public accommodations'):
        new_entry = {
            'old_tag': 'public accommodations',
            'new_tag': 'public accommodations',
            'action': 'hierarchy',
            'notes': 'parent=accommodation buildings',
            'status': 'active'
        }
        rows.append(new_entry)
        stats['added'].append('public accommodations')
        print("✓ Added: public accommodations")
    else:
        stats['skipped'].append('public accommodations - already exists')
        print("⊙ Skipped: public accommodations - already exists")

    # Update hotels (buildings) parent reference
    updated_hotels = False
    for row in rows:
        if (row['new_tag'] == 'hotels (buildings)' and
            row['action'] == 'hierarchy' and
            row['status'] == 'active'):

            old_notes = row['notes']
            # Check if parent is already correct
            if 'parent=public accommodations' in old_notes:
                stats['skipped'].append('hotels (buildings) parent - already correct')
                print("⊙ Skipped: hotels (buildings) parent - already correct")
            else:
                row['notes'] = 'parent=public accommodations'
                stats['updated'].append(f'hotels (buildings): {old_notes} → {row["notes"]}')
                print(f"✓ Updated: hotels (buildings) parent reference")
                updated_hotels = True

    if not updated_hotels:
        print("⊙ Note: hotels (buildings) not found or parent already correct")

    # Change 3: Verify "commercial buildings" exists
    if not check_term_exists(rows, 'commercial buildings'):
        print("⚠ WARNING: commercial buildings not found - adding it")
        new_entry = {
            'old_tag': 'commercial buildings',
            'new_tag': 'commercial buildings',
            'action': 'hierarchy',
            'notes': 'parent=Built Environment',
            'status': 'active'
        }
        rows.append(new_entry)
        stats['added'].append('commercial buildings')
        print("✓ Added: commercial buildings")
    else:
        print("✓ Verified: commercial buildings exists")

    # Change 4: Verify "accommodation buildings" exists
    if not check_term_exists(rows, 'accommodation buildings'):
        print("⚠ WARNING: accommodation buildings not found - adding it")
        new_entry = {
            'old_tag': 'accommodation buildings',
            'new_tag': 'accommodation buildings',
            'action': 'hierarchy',
            'notes': 'parent=Built Environment',
            'status': 'active'
        }
        rows.append(new_entry)
        stats['added'].append('accommodation buildings')
        print("✓ Added: accommodation buildings")
    else:
        print("✓ Verified: accommodation buildings exists")

    return rows, stats


def main():
    """Apply Tier 1 AAT alignment changes."""
    csv_path = Path('data/tag_map_consolidated.csv')

    print("=" * 80)
    print("GETTY AAT ALIGNMENT - TIER 1 CHANGES")
    print("=" * 80)
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

    # Apply changes
    print("Applying Tier 1 changes...")
    print()
    rows, stats = apply_tier1_changes(rows, fieldnames)
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

    print(f"Added terms: {len(stats['added'])}")
    for term in stats['added']:
        print(f"  + {term}")
    print()

    print(f"Updated references: {len(stats['updated'])}")
    for update in stats['updated']:
        print(f"  → {update}")
    print()

    if stats['skipped']:
        print(f"Skipped (already correct): {len(stats['skipped'])}")
        for item in stats['skipped']:
            print(f"  ⊙ {item}")
        print()

    print("=" * 80)
    print("CHANGES APPLIED")
    print("=" * 80)
    print()
    print("Hierarchy changes:")
    print("  1. financial institutions (buildings) → commercial buildings")
    print("     banks (buildings) → financial institutions (buildings)")
    print()
    print("  2. public accommodations → accommodation buildings")
    print("     hotels (buildings) → public accommodations")
    print()
    print("Next steps:")
    print("  1. Run script 61 (final QA validation)")
    print("  2. Review validation report")
    print("  3. Update documentation")
    print()


if __name__ == '__main__':
    main()
