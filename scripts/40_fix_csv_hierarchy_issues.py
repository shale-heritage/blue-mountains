#!/usr/bin/env python3
"""
Fix CSV Hierarchy Issues

Removes duplicate and incorrect parent relationships identified in hierarchy visualization review.

Issues Fixed:
1. Demographic groups and Occupations incorrectly pointing directly to Agents (should only be under People)
2. Duplicate Police -> Law enforcement relationship with different annotations
3. Court/Courts confusion causing duplicate entries
4. Church/Churches confusion causing duplicate entries
5. Other poly-hierarchy issues within primary facets

Author: Claude Code
Date: 2025-10-30
"""

import csv
from pathlib import Path
from typing import List, Tuple

CSV_PATH = Path("data/tag_map_consolidated.csv")
BACKUP_PATH = Path("data/tag_map_consolidated.csv.backup-hierarchy-fixes")

# Define relationships to DELETE
RELATIONSHIPS_TO_DELETE = [
    # Issue 1: Demographic groups and Occupations should only be under People, not direct children of Agents
    ("Demographic groups", "Demographic groups", "hierarchy", "parent=Agents (new top-level facet)"),
    ("Occupations", "Occupations", "hierarchy", "parent=Agents (new top-level facet)"),

    # Issue 2: Duplicate Police entry with annotation difference (keep the one without annotation)
    ("Police", "Police", "hierarchy", "parent=Law enforcement (intermediate facet)"),

    # Issue 3: Court/Courts confusion - "Court" should not be a child of "Courts"
    # Instead, specific courts should be direct children of "Courts"
    ("Court", "Court", "hierarchy", "parent=Courts"),

    # Issue 3a: Specific courts should NOT also have "Court" as parent (causes duplication)
    ("Katoomba Court", "Katoomba Court", "hierarchy", "parent=Court"),
    ("Licensing Court", "Licensing Court", "hierarchy", "parent=Court"),
    ("Police court", "Police court", "hierarchy", "parent=Court"),
    ("Supreme Court", "Supreme Court", "hierarchy", "parent=Court"),

    # Issue 4: Church/Churches confusion - same pattern
    ("Church", "Church", "hierarchy", "parent=Churches"),

    # Issue 4a: Specific churches should NOT also have "Church" as parent
    ("Congregational Church", "Congregational Church", "hierarchy", "parent=Church"),
    ("Katoomba Congregational Church", "Katoomba Congregational Church", "hierarchy", "parent=Church"),
    ("Methodist Church", "Methodist Church", "hierarchy", "parent=Church"),
    ("Roman Catholic Church", "Roman Catholic Church", "hierarchy", "parent=Church"),
    ("St Hilda's Church", "St Hilda's Church", "hierarchy", "parent=Church"),
    ("Wesleyan Church", "Wesleyan Church", "hierarchy", "parent=Church"),

    # Issue 5: Remove remaining "Court" relationships (Court should not be a category)
    ("Court cases", "Court cases", "hierarchy", "parent=Court"),
    ("Courthouse", "Courthouse", "hierarchy", "parent=Court"),

    # Issue 6: Specific churches should only be under their denomination, not also under Churches
    ("Katoomba Congregational Church", "Katoomba Congregational Church", "hierarchy", "parent=Churches"),
]


def load_csv() -> List[dict]:
    """Load CSV data into memory."""
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(rows: List[dict]):
    """Save CSV data back to file."""
    if not rows:
        print("ERROR: No rows to save!")
        return

    fieldnames = ['new_tag', 'old_tag', 'action', 'notes']

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_backup():
    """Create backup of CSV before modifications."""
    import shutil
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Created backup: {BACKUP_PATH}")


def matches_relationship(row: dict, rel: Tuple[str, str, str, str]) -> bool:
    """Check if a CSV row matches a relationship to delete."""
    new_tag, old_tag, action, notes = rel
    return (
        row['new_tag'] == new_tag and
        row['old_tag'] == old_tag and
        row['action'] == action and
        row['notes'] == notes
    )


def fix_hierarchy_issues():
    """Main function to fix all hierarchy issues."""
    print("=" * 80)
    print("CSV HIERARCHY ISSUE FIXER")
    print("=" * 80)
    print()

    # Create backup
    create_backup()

    # Load data
    print(f"Loading CSV: {CSV_PATH}")
    rows = load_csv()
    original_count = len(rows)
    print(f"✓ Loaded {original_count} rows")
    print()

    # Filter out relationships to delete
    print("Removing problematic relationships:")
    print("-" * 80)

    deleted_count = 0
    filtered_rows = []

    for row in rows:
        should_delete = False

        for rel in RELATIONSHIPS_TO_DELETE:
            if matches_relationship(row, rel):
                new_tag, old_tag, action, notes = rel
                print(f"  ✗ {new_tag} -> {notes}")
                should_delete = True
                deleted_count += 1
                break

        if not should_delete:
            filtered_rows.append(row)

    print()
    print(f"Deleted {deleted_count} relationships")
    print(f"Remaining: {len(filtered_rows)} rows")
    print()

    # Save cleaned data
    save_csv(filtered_rows)
    print(f"✓ Saved cleaned CSV: {CSV_PATH}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original rows:     {original_count}")
    print(f"Deleted rows:      {deleted_count}")
    print(f"Remaining rows:    {len(filtered_rows)}")
    print(f"Backup location:   {BACKUP_PATH}")
    print()

    print("Issues Fixed:")
    print("  1. ✓ Removed Demographic groups -> Agents (should only be under People)")
    print("  2. ✓ Removed Occupations -> Agents (should only be under People)")
    print("  3. ✓ Removed duplicate Police -> Law enforcement entry")
    print("  4. ✓ Removed Court -> Courts relationship (Court is not a category)")
    print("  5. ✓ Removed specific courts -> Court relationships (prevents duplication)")
    print("  6. ✓ Removed Church -> Churches relationship (Church is not a category)")
    print("  7. ✓ Removed specific churches -> Church relationships (prevents duplication)")
    print()
    print("Next step: Regenerate hierarchy visualizations to verify fixes")
    print()


if __name__ == "__main__":
    fix_hierarchy_issues()
