#!/usr/bin/env python3
"""
Script 44: Apply Leaf Node Assignments and Merges

Applies user-approved Getty facet assignments for leaf nodes and creates
merge operations for synonym standardisation.

ASSIGNMENTS (3):
- Greenbank family → Agents > People > Families
- Katoomba South → Places > Towns > Katoomba > Katoomba South
- Publican's License → Associated Concepts > Legal concepts > Licenses

MERGES (6):
- Minors → (context-dependent: child or adolescent)
- Mount Kembla Colliery Disaster → Mount Kembla Disaster
- Mt Victoria → Mount Victoria
- Post Office Department → Post Department
- Postman → Mailman
- Whiskey → Whisky

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path


def apply_assignments(csv_path: Path, backup_path: Path):
    """Apply hierarchy assignments and merge operations."""

    print("=" * 80)
    print("APPLYING LEAF NODE ASSIGNMENTS AND MERGES")
    print("=" * 80)
    print()

    # Create backup
    print(f"Creating backup: {backup_path}")
    import shutil
    shutil.copy2(csv_path, backup_path)
    print()

    # Load current CSV
    print(f"Loading {csv_path}...")
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for row in reader:
            rows.append(row)
    print(f"  Loaded {len(rows) - 1} data rows")
    print()

    # Prepare new entries
    new_entries = []

    # HIERARCHY ASSIGNMENTS
    print("Adding hierarchy assignments...")

    # 1. Greenbank family → Agents > People > Families
    new_entries.extend([
        ['Families', 'Families', 'hierarchy', 'parent=People'],
        ['Greenbank family', 'Greenbank family', 'hierarchy', 'parent=Families'],
    ])
    print("  + Greenbank family → Agents > People > Families")

    # 2. Katoomba South → Places > Towns > Katoomba > Katoomba South
    # (Katoomba already under Towns from script 41)
    new_entries.append(
        ['Katoomba South', 'Katoomba South', 'hierarchy', 'parent=Katoomba']
    )
    print("  + Katoomba South → Places > Towns > Katoomba")

    # 3. Publican's License → Associated Concepts > Legal concepts > Licenses
    new_entries.extend([
        ['Legal concepts', 'Legal concepts', 'hierarchy', 'parent=Associated Concepts'],
        ['Licenses', 'Licenses', 'hierarchy', 'parent=Legal concepts'],
        ['Publican\'s License', 'Publican\'s License', 'hierarchy', 'parent=Licenses'],
    ])
    print("  + Publican's License → Associated Concepts > Legal concepts > Licenses")
    print()

    # MERGE OPERATIONS
    print("Adding merge operations...")

    # 1. Minors → merge to child/adolescent (flagged for manual review)
    new_entries.append(
        ['Minors', 'Minors', 'merge', 'MANUAL REVIEW NEEDED: Merge to either Child or Adolescent based on context. Thesaurus entry: Minors = Child + Adolescent']
    )
    print("  + Minors → flagged for manual review (child/adolescent context-dependent)")

    # 2. Mount Kembla Colliery Disaster → Mount Kembla Disaster
    new_entries.append(
        ['Mount Kembla Colliery Disaster', 'Mount Kembla Disaster', 'merge', 'Synonym - standardise to Mount Kembla Disaster']
    )
    print("  + Mount Kembla Colliery Disaster → Mount Kembla Disaster")

    # 3. Mt Victoria → Mount Victoria
    new_entries.append(
        ['Mt Victoria', 'Mount Victoria', 'merge', 'Variant spelling - standardise to Mount Victoria']
    )
    print("  + Mt Victoria → Mount Victoria")

    # 4. Post Office Department → Post Department
    new_entries.append(
        ['Post Office Department', 'Post Department', 'merge', 'Synonym - standardise to Post Department']
    )
    print("  + Post Office Department → Post Department")

    # 5. Postman → Mailman
    new_entries.append(
        ['Postman', 'Mailman', 'merge', 'Synonym - standardise to Mailman']
    )
    print("  + Postman → Mailman")

    # 6. Whiskey → Whisky
    new_entries.append(
        ['Whiskey', 'Whisky', 'merge', 'Variant spelling - standardise to Whisky']
    )
    print("  + Whiskey → Whisky")
    print()

    # Check for duplicates before adding
    existing_set = {tuple(row) for row in rows[1:]}  # Skip header
    unique_new_entries = []

    for entry in new_entries:
        if tuple(entry) not in existing_set:
            unique_new_entries.append(entry)

    print(f"Adding {len(unique_new_entries)} unique new entries (filtered {len(new_entries) - len(unique_new_entries)} duplicates)")
    print()

    # Append new entries
    rows.extend(unique_new_entries)

    # Write updated CSV
    print(f"Writing updated CSV to {csv_path}...")
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"  ✓ Written {len(rows) - 1} data rows")
    print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"✓ Added 3 hierarchy assignments")
    print(f"✓ Added 6 merge operations")
    print(f"✓ Total new entries: {len(unique_new_entries)}")
    print()
    print("Deferred items (need hierarchy review after regeneration):")
    print("  - Mt Victoria Hotel")
    print("  - Reference to the Irish or Irish culture")
    print("  - Sly-grog operations")
    print()
    print("Next steps:")
    print("1. Regenerate visualizations")
    print("2. Review Agents and Activities hierarchies")
    print("3. Assign remaining 3 deferred items")
    print()


def main():
    """Main execution."""
    csv_path = Path('data/tag_map_consolidated.csv')
    backup_path = Path('data/tag_map_consolidated.csv.backup-2025-10-24-post-script44')

    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return 1

    apply_assignments(csv_path, backup_path)

    return 0


if __name__ == '__main__':
    exit(main())
