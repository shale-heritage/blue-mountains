#!/usr/bin/env python3
"""
Add universities hierarchy following Getty AAT institutional classification.

Changes:
1. Add "educational institutions" under organisations
2. Add "universities" under educational institutions
3. Add "university (institution)" as singular generic
4. Add "University of Sydney (institution)" as specific named entity
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def add_universities():
    """Add universities hierarchy to taxonomy."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Define tags to add
    new_tags = [
        {
            'old_tag': 'educational institutions',
            'new_tag': 'educational institutions',
            'action': 'hierarchy',
            'notes': 'parent=organisations'
        },
        {
            'old_tag': 'universities',
            'new_tag': 'universities',
            'action': 'hierarchy',
            'notes': 'parent=educational institutions'
        },
        {
            'old_tag': 'university (institution)',
            'new_tag': 'university (institution)',
            'action': 'hierarchy',
            'notes': 'parent=universities (singular generic term)'
        },
        {
            'old_tag': 'University of Sydney (institution)',
            'new_tag': 'University of Sydney (institution)',
            'action': 'hierarchy',
            'notes': 'parent=universities'
        }
    ]

    # Check what already exists
    existing_tags = {row['old_tag'] for row in rows}
    tags_to_add = [tag for tag in new_tags if tag['old_tag'] not in existing_tags]

    if tags_to_add:
        rows.extend(tags_to_add)

        # Write back
        with open(TAXONOMY_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Added {len(tags_to_add)} new tags to taxonomy:")
        for tag in tags_to_add:
            print(f"  - {tag['old_tag']}")
    else:
        print("✓ All universities tags already exist in taxonomy")

    return len(tags_to_add)


def main():
    """Main execution."""

    print("Universities Hierarchy Implementation")
    print("=" * 60)
    print()
    print("Following Getty AAT: universities (institutions)")
    print()

    added_count = add_universities()

    print()
    print("=" * 60)
    print("New hierarchy:")
    print("  organisations")
    print("  └── educational institutions")
    print("      └── universities")
    print("          ├── university (institution)")
    print("          └── University of Sydney (institution)")
    print()
    print("✓ Complete!")
    print()
    if added_count > 0:
        print("Next steps:")
        print("  1. Regenerate hierarchy visualisations")
        print("  2. Tag items mentioning University of Sydney appropriately")


if __name__ == '__main__':
    main()
