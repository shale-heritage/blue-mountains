#!/usr/bin/env python3
"""
Fix Built Environment facet style guide compliance issues.

Addresses 52 distinct violations across four categories:
1. Capitalisation issues (21 instances)
2. Duplicate entries (12 pairs)
3. Unqualified church tags (5 instances)
4. Structural issues (14 instances)

Based on analysis in reports/built-environment-style-compliance-review.md

Changes:
- Remove 25 duplicate/conflicting entries
- Modify 16 entries for capitalisation and parent references
- Align with style guide: generic terms lowercase, proper nouns Title Case
"""

import csv
from datetime import datetime
from pathlib import Path

# Paths
project_root = Path(__file__).parent.parent
csv_path = project_root / "data" / "tag_map_consolidated.csv"

def create_backup(file_path):
    """Create timestamped backup of the CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    backup_path.write_text(file_path.read_text())
    print(f"Backup created: {backup_path}")
    return backup_path

def should_delete_row(row):
    """Determine if a row should be deleted."""
    old_tag = row['old_tag']
    new_tag = row['new_tag']
    action = row['action']
    notes = row.get('notes', '')

    # Delete capitalized duplicates that have lowercase equivalents
    delete_entries = [
        # Capitalized category duplicates
        ('Accommodation and hospitality venues', 'Accommodation and hospitality venues', 'hierarchy', 'parent=Built Environment'),
        ('Gas', 'Gas', 'hierarchy', 'parent=Utilities'),
        ('Roads', 'Roads', 'hierarchy', 'parent=transport infrastructure'),
        ('Roads', 'Roads', 'hierarchy', 'parent=transport & infrastructure - THEMATIC'),
        ('Sewerage', 'Sewerage', 'hierarchy', 'parent=Utilities'),
        ('Tramway', 'Tramway', 'hierarchy', 'parent=mining infrastructure'),
        ('Tramway', 'Tramway', 'hierarchy', 'parent=mining transport - THEMATIC'),
        ('Utilities', 'Utilities', 'hierarchy', 'parent=infrastructure'),
        ('Utilities', 'Utilities', 'hierarchy', 'parent=transport & infrastructure - THEMATIC'),
        ('Police station', 'Police station', 'hierarchy', 'parent=police facilities'),
        ('Police station', 'Police station', 'hierarchy', 'parent=justice & crime - THEMATIC'),
        ('Post office', 'Post office', 'hierarchy', 'parent=postal facilities'),
        ('Post office', 'Post office', 'hierarchy', 'parent=postal services - THEMATIC'),

        # Duplicate Court buildings (keep lowercase version)
        ('Court buildings', 'Court buildings', 'hierarchy', 'parent=civic buildings'),
        ('Court buildings', 'Court buildings', 'hierarchy', 'parent=justice & crime - THEMATIC'),

        # Structural issues - hotel (building) duplicate parent
        ('hotel (building)', 'hotel (building)', 'hierarchy', 'parent=accommodation buildings'),

        # Structural issues - plural parents in thematic facets
        ('hotels', 'hotels', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'),
        ('hotels', 'hotels', 'hierarchy', 'parent=Domestic accommodation - THEMATIC (residential aspect)'),
        ('boarding houses', 'boarding houses', 'hierarchy', 'parent=Domestic accommodation - THEMATIC'),
        ('public houses', 'public houses', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'),

        # Unqualified church hierarchy relationships (keep only synonyms)
        ('Congregational Church', 'Congregational Church', 'hierarchy', 'parent=churches'),
        ('Methodist Church', 'Methodist Church', 'hierarchy', 'parent=churches'),
        ('Roman Catholic Church', 'Roman Catholic Church', 'hierarchy', 'parent=churches'),
        ('Wesleyan Church', 'Wesleyan Church', 'hierarchy', 'parent=churches'),
        ("St Hilda's Church", "St Hilda's Church", 'hierarchy', 'parent=churches'),
    ]

    for del_old, del_new, del_action, del_parent in delete_entries:
        if (old_tag == del_old and new_tag == del_new and
            action == del_action and del_parent in notes):
            return True

    return False

def fix_row(row):
    """Apply capitalisation and parent reference fixes to a row."""
    old_tag = row['old_tag']
    new_tag = row['new_tag']
    action = row['action']
    notes = row.get('notes', '')

    # Capitalisation fixes - change tag to lowercase
    capitalisation_fixes = {
        'Cottages': 'cottages',
        'Council buildings': 'council buildings',
        'Courthouse': 'courthouse',
        'Council Chambers': 'council chambers',
        'Dwellings': 'dwellings',
        'Stable': 'stable',
        'Stables': 'stables',
    }

    if old_tag in capitalisation_fixes:
        row['old_tag'] = capitalisation_fixes[old_tag]

    if new_tag in capitalisation_fixes:
        row['new_tag'] = capitalisation_fixes[new_tag]

    # Parent reference fixes - change from capitalized to lowercase parents
    parent_fixes = {
        'parent=Accommodation and hospitality venues': 'parent=accommodation and hospitality venues',
        'parent=Court buildings': 'parent=court buildings',
        'parent=Council buildings': 'parent=council buildings',
        'parent=Stables': 'parent=stables',
        'parent=Roads': 'parent=roads',
        'parent=Utilities': 'parent=utilities',
    }

    for old_parent, new_parent in parent_fixes.items():
        if old_parent in notes:
            row['notes'] = notes.replace(old_parent, new_parent)

    return row

def apply_corrections(csv_path):
    """Apply all corrections to the CSV file."""

    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    original_count = len(rows)
    deleted_count = 0
    modified_count = 0

    # Process rows
    filtered_rows = []
    for row in rows:
        if should_delete_row(row):
            deleted_count += 1
            continue

        # Check if row will be modified
        original_row = row.copy()
        row = fix_row(row)

        if row != original_row:
            modified_count += 1

        filtered_rows.append(row)

    # Write back
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    return deleted_count, modified_count, original_count, len(filtered_rows)

def main():
    """Main execution function."""
    print("Built Environment Style Guide Compliance Corrections")
    print("=" * 60)
    print("\nBased on: reports/built-environment-style-compliance-review.md")
    print("\nAddressing:")
    print("  - Capitalisation issues (21 instances)")
    print("  - Duplicate entries (12 pairs)")
    print("  - Unqualified church tags (5 instances)")
    print("  - Structural issues (14 instances)")

    # Create backup
    print("\n" + "=" * 60)
    create_backup(csv_path)

    # Apply corrections
    print("\nApplying corrections...")
    deleted, modified, original, final = apply_corrections(csv_path)

    print("\n" + "=" * 60)
    print("Results:")
    print(f"  Original entries: {original}")
    print(f"  Deleted entries:  {deleted}")
    print(f"  Modified entries: {modified}")
    print(f"  Final entries:    {final}")
    print(f"  Net change:       -{deleted} entries")

    print("\n" + "=" * 60)
    print("Corrections applied successfully!")
    print("\nNext steps:")
    print("1. Run validation queries from the report")
    print("2. Regenerate visualisations: python3 scripts/23_visualise_poly_hierarchy.py")
    print("3. Review changes: git diff data/tag_map_consolidated.csv")

if __name__ == "__main__":
    main()
