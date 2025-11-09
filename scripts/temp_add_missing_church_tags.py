#!/usr/bin/env python3
"""
Add missing tags from church disambiguation validation.

Adds clergy names and other tags identified as missing during validation.
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def add_missing_tags():
    """Add all missing tags to taxonomy."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    existing_tags = {row['old_tag'] for row in rows}

    # Define missing tags to add
    new_tags = []

    # Clergy tags (all under Agents > people > occupations > clergy)
    clergy_members = [
        'Reverend E A Ferguson',
        'Reverend E Lampard',
        'Reverend F Bevan',
        'Reverend Father Bridge',
        'Reverend J F Russel',
        'Reverend J Hargreaves',
        'Reverend R W Orton',
        'Reverend Robertson',
        'Reverend T K Abbot',
        'Reverend W Lampard',
        'Reverend W R Orton',
        'Reverend W Tollis',
        'Archbishop',
        'Coadjutor Archbishop',
        'Mr van Someren',  # Clergy or church figure
    ]

    for clergy in clergy_members:
        new_tags.append({
            'old_tag': clergy,
            'new_tag': clergy,
            'action': 'hierarchy',
            'notes': 'parent=clergy'
        })

    # Sunday School tag (under religious education > sunday schools)
    new_tags.append({
        'old_tag': 'St Aidan\'s Church Blackheath Sunday School',
        'new_tag': 'St Aidan\'s Church Blackheath Sunday School',
        'action': 'hierarchy',
        'notes': 'parent=sunday schools'
    })

    # Geographic feature
    new_tags.append({
        'old_tag': 'Yarrangobilly Caves',
        'new_tag': 'Yarrangobilly Caves',
        'action': 'hierarchy',
        'notes': 'parent=caves'
    })

    # Filter out tags that already exist
    tags_to_add = [tag for tag in new_tags if tag['old_tag'] not in existing_tags]

    if tags_to_add:
        rows.extend(tags_to_add)

        # Write back to CSV
        with open(TAXONOMY_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Added {len(tags_to_add)} new tags to taxonomy:")
        for tag in tags_to_add:
            print(f"  - {tag['old_tag']}")
    else:
        print("✓ All tags already exist in taxonomy")

    return len(tags_to_add)


def main():
    """Main execution."""

    print("Adding Missing Church Disambiguation Tags")
    print("=" * 60)
    print()

    added_count = add_missing_tags()

    print()
    print("=" * 60)
    print(f"✓ Complete: {added_count} tags added")
    print()

    if added_count > 0:
        print("Next steps:")
        print("  1. Re-run validation to confirm all tags exist")
        print("  2. Regenerate hierarchy visualizations")


if __name__ == '__main__':
    main()
