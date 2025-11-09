#!/usr/bin/env python3
"""
Add intermediate hierarchies for Congregational and Roman Catholic churches.

Following the pattern established for Presbyterian churches and Church of England churches,
this adds intermediate parent nodes for denominations with multiple instances.

Changes:
1. Add "Congregational churches" intermediate node under churches
2. Add "Roman Catholic churches" intermediate node under churches
3. Update parent relationships for all Congregational church tags
4. Update parent relationships for all Roman Catholic church tags
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def add_intermediate_hierarchies():
    """Add intermediate church hierarchies and update parent relationships."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    existing_tags = {row['old_tag'] for row in rows}

    # Tags to add
    new_tags = []

    # 1. Congregational churches intermediate hierarchy
    if 'Congregational churches' not in existing_tags:
        new_tags.append({
            'old_tag': 'Congregational churches',
            'new_tag': 'Congregational churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        })

    # 2. Roman Catholic churches intermediate hierarchy
    if 'Roman Catholic churches' not in existing_tags:
        new_tags.append({
            'old_tag': 'Roman Catholic churches',
            'new_tag': 'Roman Catholic churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        })

    # Congregational church tags to update parent relationships
    congregational_tags = [
        'Congregational Church (building)',
        'Congregational Church (organization)',
        'Congregational Church Katoomba (building)',
        'Congregational Church Katoomba South (building)',
        'Congregational Church Katoomba South (organization)',
        'Katoomba Congregational Church (building)',
        'Katoomba Congregational Church (organization)',
        'Katoomba Congregational Church (Sunday school)',
    ]

    # Roman Catholic church tags to update parent relationships
    roman_catholic_tags = [
        'Roman Catholic Church (building)',
        'Roman Catholic Church (organization)',
        'Roman Catholic Church Blackheath (organization)',
        'Roman Catholic Church Katoomba (building)',
        'Roman Catholic Church Lawson (organization)',
        'Roman Catholic Church Megalong (building)',
        'Roman Catholic Church Megalong (organization)',
        'Roman Catholic Church Mount Victoria (organization)',
        'St Canice\'s Catholic Church Katoomba (building)',
        'St Canice\'s Catholic Church Katoomba (organization)',
    ]

    # Update parent relationships for existing tags
    updated_count = 0
    for row in rows:
        tag = row['old_tag']

        # Update Congregational church tags
        if tag in congregational_tags:
            # Check if parent is currently "churches"
            if 'parent=churches' in row['notes']:
                # Preserve any additional notes after parent specification
                notes_parts = row['notes'].split('parent=churches', 1)
                if len(notes_parts) > 1 and notes_parts[1].strip():
                    # Has additional notes like "(singular generic term)"
                    additional = notes_parts[1].strip()
                    if additional.startswith('('):
                        row['notes'] = f"parent=Congregational churches {additional}"
                    else:
                        row['notes'] = f"parent=Congregational churches ({additional})"
                else:
                    row['notes'] = 'parent=Congregational churches'
                updated_count += 1

        # Update Roman Catholic church tags
        elif tag in roman_catholic_tags:
            # Check if parent is currently "churches"
            if 'parent=churches' in row['notes']:
                # Preserve any additional notes
                notes_parts = row['notes'].split('parent=churches', 1)
                if len(notes_parts) > 1 and notes_parts[1].strip():
                    additional = notes_parts[1].strip()
                    if additional.startswith('('):
                        row['notes'] = f"parent=Roman Catholic churches {additional}"
                    else:
                        row['notes'] = f"parent=Roman Catholic churches ({additional})"
                else:
                    row['notes'] = 'parent=Roman Catholic churches'
                updated_count += 1

    # Add new intermediate nodes
    if new_tags:
        rows.extend(new_tags)

    # Write back to CSV
    with open(TAXONOMY_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Added {len(new_tags)} intermediate hierarchy nodes")
    print(f"✓ Updated parent relationships for {updated_count} existing tags")
    print()

    if new_tags:
        print("New hierarchies:")
        for tag in new_tags:
            print(f"  - {tag['old_tag']}")

    return len(new_tags), updated_count


def main():
    """Main execution."""

    print("Add Intermediate Church Hierarchies")
    print("=" * 60)
    print()
    print("Adding intermediate nodes for:")
    print("  - Congregational churches")
    print("  - Roman Catholic churches")
    print()

    added, updated = add_intermediate_hierarchies()

    print()
    print("=" * 60)
    print("New hierarchy structure:")
    print()
    print("churches")
    print("├── Congregational churches")
    print("│   ├── Congregational Church (building)")
    print("│   ├── Congregational Church (organization)")
    print("│   ├── Congregational Church Katoomba (building)")
    print("│   ├── Congregational Church Katoomba South (...)")
    print("│   ├── Katoomba Congregational Church (...)")
    print("│   └── ...")
    print("├── Roman Catholic churches")
    print("│   ├── Roman Catholic Church (building)")
    print("│   ├── Roman Catholic Church (organization)")
    print("│   ├── Roman Catholic Church Blackheath (organization)")
    print("│   ├── Roman Catholic Church Katoomba (building)")
    print("│   ├── Roman Catholic Church Lawson (organization)")
    print("│   ├── St Canice's Catholic Church Katoomba (...)")
    print("│   └── ...")
    print("├── Church of England churches")
    print("│   └── ...")
    print("└── Presbyterian churches")
    print("    └── ...")
    print()
    print("✓ Complete!")
    print()
    print("Next steps:")
    print("  1. Regenerate hierarchy visualizations")
    print("  2. Review Religion theme to verify structure")


if __name__ == '__main__':
    main()
