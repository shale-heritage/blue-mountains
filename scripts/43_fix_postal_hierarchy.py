#!/usr/bin/env python3
"""
Fix Postal Hierarchy

Changes:
1. Remove "Post" tag entirely (deprecated, being replaced)
2. Remove "Postal service" singular generic (redundant - only child of Postal services)
3. Move "Post office" from Activities to Built Environment > Postal facilities
4. Keep "Postal services" as leaf node under Communication activities

Author: Claude Code
Date: 2025-10-30
"""

import csv
from pathlib import Path

CSV_PATH = Path("data/tag_map_consolidated.csv")
BACKUP_PATH = Path("data/tag_map_consolidated.csv.backup-before-postal-fix")


def fix_postal_hierarchy():
    """Fix postal-related hierarchy issues."""
    print("=" * 80)
    print("FIX POSTAL HIERARCHY")
    print("=" * 80)
    print()

    # Create backup
    import shutil
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Created backup: {BACKUP_PATH}")
    print()

    # Load data
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    original_count = len(rows)
    print(f"✓ Loaded {original_count} rows")
    print()

    # Apply changes
    print("Applying changes:")
    print("-" * 80)

    filtered_rows = []
    changes = {
        'deleted_post': 0,
        'deleted_postal_service': 0,
        'updated_post_office': 0
    }

    for row in rows:
        # 1. Delete "Post" tag entirely (all relationships)
        if row['new_tag'] == 'Post' and row['action'] == 'hierarchy':
            print(f"  ✗ Deleted: Post -> {row['notes']}")
            changes['deleted_post'] += 1
            continue

        # 2. Delete "Postal service" singular generic (redundant)
        if (row['new_tag'] == 'Postal service' and
            row['action'] == 'hierarchy' and
            'parent=Postal services' in row['notes']):
            print(f"  ✗ Deleted: Postal service (redundant singular generic)")
            changes['deleted_postal_service'] += 1
            continue

        # 3. Update "Post office" - remove from Activities/Postal services only
        if (row['new_tag'] == 'Post office' and
            row['action'] == 'hierarchy' and
            ('parent=Post' in row['notes'] or 'THEMATIC' in row['notes'])):
            # Only delete if it's the wrong parent (Post) or a thematic relationship
            # Keep the one with parent=Postal facilities
            if 'parent=Postal facilities' not in row['notes']:
                print(f"  ✗ Deleted: Post office -> {row['notes']}")
                changes['updated_post_office'] += 1
                continue

        filtered_rows.append(row)

    # Verify Post office still has correct parent
    post_office_parents = [r for r in filtered_rows
                          if r['new_tag'] == 'Post office' and r['action'] == 'hierarchy']

    print()
    print("Post office remaining relationships:")
    for r in post_office_parents:
        print(f"  ✓ Post office -> {r['notes']}")

    print()
    print(f"Deleted {changes['deleted_post']} 'Post' relationships")
    print(f"Deleted {changes['deleted_postal_service']} 'Postal service' relationship")
    print(f"Updated 'Post office' location (removed {changes['updated_post_office']} old relationship)")
    print()

    # Save
    fieldnames = ['new_tag', 'old_tag', 'action', 'notes']
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered_rows)

    print(f"✓ Saved updated CSV: {CSV_PATH}")
    print()

    # Summary
    total_deleted = sum(changes.values())
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original rows:    {original_count}")
    print(f"Deleted rows:     {total_deleted}")
    print(f"Final rows:       {len(filtered_rows)}")
    print()
    print("Changes made:")
    print("  1. ✓ Removed 'Post' tag entirely (deprecated)")
    print("  2. ✓ Removed 'Postal service' singular generic (redundant)")
    print("  3. ✓ 'Post office' now only under Built Environment > Postal facilities")
    print("  4. ✓ 'Postal services' remains as leaf under Communication activities")
    print()


if __name__ == "__main__":
    fix_postal_hierarchy()
