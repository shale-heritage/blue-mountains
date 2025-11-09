#!/usr/bin/env python3
"""
Add church disambiguation taxonomy entries.

Implements Phase 1 of church disambiguation plan:
- Adds new church hierarchies (Presbyterian, Church of England, etc.)
- Creates synonym mappings for variant naming patterns
- Follows standardized "[church name] [place]" naming convention
"""

import csv
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"


def add_church_taxonomy():
    """Add all new church-related taxonomy entries."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    existing_tags = {row['old_tag'] for row in rows}

    # Define all new tags to add
    new_tags = []

    # 1.1 Loyal Orange Order
    new_tags.append({
        'old_tag': 'Loyal Orange Order',
        'new_tag': 'Loyal Orange Order',
        'action': 'hierarchy',
        'notes': 'parent=lodges'
    })

    # 1.2 Monasteries and friaries
    new_tags.extend([
        {
            'old_tag': 'monasteries and friaries',
            'new_tag': 'monasteries and friaries',
            'action': 'hierarchy',
            'notes': 'parent=religious organisations'
        },
        {
            'old_tag': 'monastery or friary',
            'new_tag': 'monastery or friary',
            'action': 'hierarchy',
            'notes': 'parent=monasteries and friaries (singular generic term)'
        },
        {
            'old_tag': 'Waverley Friary (organization)',
            'new_tag': 'Waverley Friary (organization)',
            'action': 'hierarchy',
            'notes': 'parent=monasteries and friaries'
        }
    ])

    # 1.3 Presbyterian churches
    new_tags.extend([
        {
            'old_tag': 'Presbyterian churches',
            'new_tag': 'Presbyterian churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Presbyterian church (organization)',
            'new_tag': 'Presbyterian church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches (singular generic term)'
        },
        {
            'old_tag': 'Presbyterian church (building)',
            'new_tag': 'Presbyterian church (building)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches (singular generic term)'
        },
        {
            'old_tag': 'Presbyterian Church Leura (organization)',
            'new_tag': 'Presbyterian Church Leura (organization)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches'
        },
        {
            'old_tag': 'Presbyterian Church Leura (building)',
            'new_tag': 'Presbyterian Church Leura (building)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches'
        },
        {
            'old_tag': 'Presbyterian Church Wentworth Falls (organization)',
            'new_tag': 'Presbyterian Church Wentworth Falls (organization)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches'
        },
        {
            'old_tag': 'Presbyterian Church Wentworth Falls (building)',
            'new_tag': 'Presbyterian Church Wentworth Falls (building)',
            'action': 'hierarchy',
            'notes': 'parent=Presbyterian churches'
        },
        # Synonyms for variant naming
        {
            'old_tag': 'Leura Presbyterian Church',
            'new_tag': 'Presbyterian Church Leura',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        },
        {
            'old_tag': 'Wentworth Falls Presbyterian Church',
            'new_tag': 'Presbyterian Church Wentworth Falls',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        }
    ])

    # 1.4 Church of England
    new_tags.extend([
        {
            'old_tag': 'Church of England churches',
            'new_tag': 'Church of England churches',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Church of England church (organization)',
            'new_tag': 'Church of England church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches (singular generic term)'
        },
        {
            'old_tag': 'Church of England church (building)',
            'new_tag': 'Church of England church (building)',
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches (singular generic term)'
        },
        {
            'old_tag': 'Church of England Katoomba (organization)',
            'new_tag': 'Church of England Katoomba (organization)',
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': 'Church of England Katoomba (building)',
            'new_tag': 'Church of England Katoomba (building)',
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Hilda's Church of England (organization)",
            'new_tag': "St Hilda's Church of England (organization)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Hilda's Church of England (building)",
            'new_tag': "St Hilda's Church of England (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Aidan's Church Blackheath (organization)",
            'new_tag': "St Aidan's Church Blackheath (organization)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Clement's Church of England Yass (organization)",
            'new_tag': "St Clement's Church of England Yass (organization)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Mark's Church of England Darling Point (organization)",
            'new_tag': "St Mark's Church of England Darling Point (organization)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Mark's Church of England (building)",
            'new_tag': "St Mark's Church of England (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Andrew's Cathedral Church of England Sydney (organization)",
            'new_tag': "St Andrew's Cathedral Church of England Sydney (organization)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Andrew's Cathedral Church of England Sydney (building)",
            'new_tag': "St Andrew's Cathedral Church of England Sydney (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St John's Church Parramatta (building)",
            'new_tag': "St John's Church Parramatta (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St David's Church Surry Hills (building)",
            'new_tag': "St David's Church Surry Hills (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Paul's Church of England (building)",
            'new_tag': "St Paul's Church of England (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        {
            'old_tag': "St Mary's Church of England Greta (building)",
            'new_tag': "St Mary's Church of England Greta (building)",
            'action': 'hierarchy',
            'notes': 'parent=Church of England churches'
        },
        # Synonym for Anglican
        {
            'old_tag': 'Anglican',
            'new_tag': 'Church of England',
            'action': 'synonym',
            'notes': 'UK/Australian terminology preference - use Church of England'
        },
        {
            'old_tag': 'Anglican Church Katoomba',
            'new_tag': 'Church of England Katoomba',
            'action': 'synonym',
            'notes': 'UK/Australian terminology preference - use Church of England'
        }
    ])

    # 1.5 Additional Roman Catholic churches
    new_tags.extend([
        {
            'old_tag': 'Roman Catholic Church Lawson (organization)',
            'new_tag': 'Roman Catholic Church Lawson (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church Katoomba (building)',
            'new_tag': 'Roman Catholic Church Katoomba (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church Megalong (organization)',
            'new_tag': 'Roman Catholic Church Megalong (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church Megalong (building)',
            'new_tag': 'Roman Catholic Church Megalong (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church Mount Victoria (organization)',
            'new_tag': 'Roman Catholic Church Mount Victoria (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church Blackheath (organization)',
            'new_tag': 'Roman Catholic Church Blackheath (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': "St Canice's Catholic Church Katoomba (organization)",
            'new_tag': "St Canice's Catholic Church Katoomba (organization)",
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': "St Canice's Catholic Church Katoomba (building)",
            'new_tag': "St Canice's Catholic Church Katoomba (building)",
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        # Synonyms
        {
            'old_tag': 'Lawson Roman Catholic Church',
            'new_tag': 'Roman Catholic Church Lawson',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        },
        {
            'old_tag': 'Mount Victoria Catholic Church',
            'new_tag': 'Roman Catholic Church Mount Victoria',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        },
        {
            'old_tag': 'Blackheath Catholic Church',
            'new_tag': 'Roman Catholic Church Blackheath',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        },
        {
            'old_tag': "St Joseph's New Church Roman Catholic Church Megalong",
            'new_tag': 'Roman Catholic Church Megalong',
            'action': 'synonym',
            'notes': 'Full description variant - use standard form'
        },
        {
            'old_tag': "St Joseph's Roman Catholic Church Megalong",
            'new_tag': 'Roman Catholic Church Megalong',
            'action': 'synonym',
            'notes': 'Saint name variant - use standard location form'
        }
    ])

    # 1.6 Congregational churches
    new_tags.extend([
        {
            'old_tag': 'Congregational Church (organization)',
            'new_tag': 'Congregational Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches (singular generic term)'
        },
        {
            'old_tag': 'Congregational Church (building)',
            'new_tag': 'Congregational Church (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches (singular generic term)'
        },
        {
            'old_tag': 'Congregational Church Katoomba (building)',
            'new_tag': 'Congregational Church Katoomba (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Congregational Church Katoomba South (organization)',
            'new_tag': 'Congregational Church Katoomba South (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Congregational Church Katoomba South (building)',
            'new_tag': 'Congregational Church Katoomba South (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        }
    ])

    # 1.7 Methodist churches
    new_tags.extend([
        {
            'old_tag': 'Methodist Church Katoomba (organization)',
            'new_tag': 'Methodist Church Katoomba (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        # Synonym
        {
            'old_tag': 'Katoomba Methodist Church',
            'new_tag': 'Methodist Church Katoomba',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        }
    ])

    # 1.8 Wesleyan churches
    new_tags.extend([
        {
            'old_tag': 'Wesleyan Chapel (building)',
            'new_tag': 'Wesleyan Chapel (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Wesleyan Church Katoomba (organization)',
            'new_tag': 'Wesleyan Church Katoomba (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Wesleyan Church Katoomba (building)',
            'new_tag': 'Wesleyan Church Katoomba (building)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        # Synonym
        {
            'old_tag': 'Katoomba Wesleyan Church',
            'new_tag': 'Wesleyan Church Katoomba',
            'action': 'synonym',
            'notes': 'Variant naming pattern - standardized to [church name] [place]'
        }
    ])

    # 1.9 Methodist Band of Hope
    new_tags.append({
        'old_tag': 'Methodist Band of Hope',
        'new_tag': 'Methodist Band of Hope',
        'action': 'hierarchy',
        'notes': 'parent=religious social movements'
    })

    # 1.10 Congregational Church Choir
    new_tags.append({
        'old_tag': 'Congregational Church Choir',
        'new_tag': 'Congregational Church Choir',
        'action': 'hierarchy',
        'notes': 'parent=choirs'
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

        print(f"✓ Added {len(tags_to_add)} new tags to taxonomy")

        # Show breakdown
        hierarchies = [t for t in tags_to_add if t['action'] == 'hierarchy']
        synonyms = [t for t in tags_to_add if t['action'] == 'synonym']
        print(f"  - Hierarchies: {len(hierarchies)}")
        print(f"  - Synonyms: {len(synonyms)}")

        return len(tags_to_add)
    else:
        print("✓ All tags already exist in taxonomy")
        return 0


def main():
    """Main execution."""

    print("Church Disambiguation - Taxonomy Update")
    print("=" * 60)
    print()

    added_count = add_church_taxonomy()

    print()
    print("=" * 60)
    print(f"✓ Phase 1 Complete: {added_count} tags added")
    print()
    print("Next steps:")
    print("  1. Regenerate hierarchy visualizations")
    print("  2. Create tag application mappings from disambiguation report")


if __name__ == '__main__':
    main()
