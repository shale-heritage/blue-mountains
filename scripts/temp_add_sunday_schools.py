#!/usr/bin/env python3
"""
Add Sunday schools hierarchy following Getty AAT institutional classification.

Changes:
1. Add intermediate "sunday schools" (plural parent) under religious education
2. Change "sunday school" from child of "religious education" to child of "sunday schools"
3. Add "Katoomba Congregational Church (Sunday school)" as specific named institution
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def update_sunday_schools():
    """Update Sunday schools hierarchy in taxonomy."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Track changes
    changes = []

    # Step 1: Add "sunday schools" (plural parent) under religious education
    sunday_schools_parent = {
        'old_tag': 'sunday schools',
        'new_tag': 'sunday schools',
        'action': 'hierarchy',
        'notes': 'parent=religious education'
    }

    # Check if already exists
    if not any(r['old_tag'] == 'sunday schools' and r['action'] == 'hierarchy' for r in rows):
        rows.append(sunday_schools_parent)
        changes.append("Added: sunday schools (plural parent) under religious education")
        print("✓ Added 'sunday schools' as child of religious education")
    else:
        print("✓ 'sunday schools' already exists")

    # Step 2: Update "sunday school" to be child of "sunday schools" instead of "religious education"
    for row in rows:
        if (row['old_tag'] == 'sunday school' and
            row['action'] == 'hierarchy' and
            row['notes'] == 'parent=religious education'):
            # Change parent
            row['notes'] = 'parent=sunday schools (singular generic term)'
            changes.append("Updated: sunday school parent from 'religious education' to 'sunday schools'")
            print("✓ Changed 'sunday school' to be child of 'sunday schools'")
            break

    # Step 3: Add "Katoomba Congregational Church (Sunday school)" as specific named institution
    katoomba_sunday_school = {
        'old_tag': 'Katoomba Congregational Church (Sunday school)',
        'new_tag': 'Katoomba Congregational Church (Sunday school)',
        'action': 'hierarchy',
        'notes': 'parent=sunday schools'
    }

    if not any(r['old_tag'] == 'Katoomba Congregational Church (Sunday school)' for r in rows):
        rows.append(katoomba_sunday_school)
        changes.append("Added: Katoomba Congregational Church (Sunday school) under sunday schools")
        print("✓ Added 'Katoomba Congregational Church (Sunday school)'")
    else:
        print("✓ 'Katoomba Congregational Church (Sunday school)' already exists")

    # Write back to CSV
    with open(TAXONOMY_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
        writer.writeheader()
        writer.writerows(rows)

    return changes


def main():
    """Main execution."""

    print("Sunday Schools Hierarchy Implementation")
    print("=" * 60)
    print()
    print("Following Getty AAT: Sunday schools (institutions)")
    print()

    changes = update_sunday_schools()

    print()
    print("=" * 60)
    print("Summary of changes:")
    for change in changes:
        print(f"  • {change}")
    print()
    print("New hierarchy:")
    print("  religious education")
    print("  └── sunday schools")
    print("      ├── sunday school (singular generic)")
    print("      └── Katoomba Congregational Church (Sunday school)")
    print()
    print("✓ Complete!")
    print()
    print("Next steps:")
    print("  1. Regenerate hierarchy visualizations")
    print("  2. Review items tagged with 'sunday school' to determine if specific named tag applies")


if __name__ == '__main__':
    main()
