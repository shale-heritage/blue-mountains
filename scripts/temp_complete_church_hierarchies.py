#!/usr/bin/env python3
"""
Complete church hierarchies and fix duplicates.

Changes:
1. Add "Methodist churches" intermediate node
2. Add "Wesleyan churches" intermediate node
3. Convert duplicate "St Hilda's Church" to synonym of "St Hilda's Church of England"
4. Update all parent relationships
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def complete_church_hierarchies():
    """Add remaining intermediate hierarchies and fix duplicates."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    existing_tags = {row['old_tag'] for row in rows}

    # Tags to add
    new_tags = []

    # 1. Methodist churches intermediate hierarchy
    if 'Methodist churches' not in existing_tags:
        new_tags.append({
            'old_tag': 'Methodist churches',
            'new_tag': 'Methodist churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        })

    # 2. Wesleyan churches intermediate hierarchy
    if 'Wesleyan churches' not in existing_tags:
        new_tags.append({
            'old_tag': 'Wesleyan churches',
            'new_tag': 'Wesleyan churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        })

    # Methodist church tags to update
    methodist_tags = [
        'Methodist Church (building)',
        'Methodist Church (organization)',
        'Methodist Church Katoomba (organization)',
    ]

    # Wesleyan church tags to update
    wesleyan_tags = [
        'Wesleyan Chapel (building)',
        'Wesleyan Church (building)',
        'Wesleyan Church (organization)',
        'Wesleyan Church Katoomba (building)',
        'Wesleyan Church Katoomba (organization)',
    ]

    # Update parent relationships and convert St Hilda's duplicates to synonyms
    updated_count = 0
    synonym_count = 0

    for row in rows:
        tag = row['old_tag']

        # Update Methodist church tags
        if tag in methodist_tags:
            if 'parent=churches' in row['notes']:
                notes_parts = row['notes'].split('parent=churches', 1)
                if len(notes_parts) > 1 and notes_parts[1].strip():
                    additional = notes_parts[1].strip()
                    if additional.startswith('('):
                        row['notes'] = f"parent=Methodist churches {additional}"
                    else:
                        row['notes'] = f"parent=Methodist churches ({additional})"
                else:
                    row['notes'] = 'parent=Methodist churches'
                updated_count += 1

        # Update Wesleyan church tags
        elif tag in wesleyan_tags:
            if 'parent=churches' in row['notes']:
                notes_parts = row['notes'].split('parent=churches', 1)
                if len(notes_parts) > 1 and notes_parts[1].strip():
                    additional = notes_parts[1].strip()
                    if additional.startswith('('):
                        row['notes'] = f"parent=Wesleyan churches {additional}"
                    else:
                        row['notes'] = f"parent=Wesleyan churches ({additional})"
                else:
                    row['notes'] = 'parent=Wesleyan churches'
                updated_count += 1

        # Convert St Hilda's Church duplicates to synonyms
        elif tag == "St Hilda's Church (building)" and row['action'] == 'hierarchy':
            # Check if this is NOT the Church of England one
            if 'Church of England' not in row['notes']:
                row['action'] = 'synonym'
                row['new_tag'] = "St Hilda's Church of England (building)"
                row['notes'] = 'Duplicate - map to Church of England variant'
                synonym_count += 1

        elif tag == "St Hilda's Church (organization)" and row['action'] == 'hierarchy':
            # Check if this is NOT the Church of England one
            if 'Church of England' not in row['notes']:
                row['action'] = 'synonym'
                row['new_tag'] = "St Hilda's Church of England (organization)"
                row['notes'] = 'Duplicate - map to Church of England variant'
                synonym_count += 1

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
    print(f"✓ Converted {synonym_count} duplicate tags to synonyms")
    print()

    if new_tags:
        print("New hierarchies:")
        for tag in new_tags:
            print(f"  - {tag['old_tag']}")
        print()

    if synonym_count > 0:
        print("Fixed duplicates:")
        print("  - St Hilda's Church (building) → St Hilda's Church of England (building)")
        print("  - St Hilda's Church (organization) → St Hilda's Church of England (organization)")

    return len(new_tags), updated_count, synonym_count


def main():
    """Main execution."""

    print("Complete Church Hierarchies & Fix Duplicates")
    print("=" * 60)
    print()
    print("Changes:")
    print("  1. Add Methodist churches intermediate node")
    print("  2. Add Wesleyan churches intermediate node")
    print("  3. Fix St Hilda's Church duplicate (convert to synonym)")
    print()

    added, updated, synonyms = complete_church_hierarchies()

    print()
    print("=" * 60)
    print("Complete hierarchy structure:")
    print()
    print("churches")
    print("├── Church of England churches (17 instances)")
    print("│   ├── St Hilda's Church of England (building/organization)")
    print("│   └── ...")
    print("├── Congregational churches (7 instances)")
    print("├── Methodist churches (3 instances) [NEW]")
    print("│   ├── Methodist Church (building/organization) [generic]")
    print("│   └── Methodist Church Katoomba (organization)")
    print("├── Presbyterian churches (6 instances)")
    print("├── Roman Catholic churches (10 instances)")
    print("└── Wesleyan churches (5 instances) [NEW]")
    print("    ├── Wesleyan Chapel (building)")
    print("    ├── Wesleyan Church (building/organization) [generic]")
    print("    └── Wesleyan Church Katoomba (building/organization)")
    print()
    print("✓ Complete!")
    print()
    print("Next steps:")
    print("  1. Regenerate hierarchy visualisations")
    print("  2. Verify St Hilda's duplicate is resolved")


if __name__ == '__main__':
    main()
