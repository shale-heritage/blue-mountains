#!/usr/bin/env python3
"""
Reorganize Mining Taxonomy

Comprehensive reorganization of mining-related tags to correct facet placement:
- Move mines (buildings) to Built Environment
- Move mining companies to Agents with name standardization
- Move mining settlements and districts to Places
- Move mining events to Events facet
- Add Coal and Shale to Materials facet
- Merge Commercial activities into Economic activities
- Remove "Colliery" tag (becomes synonym for "Coal mine")

Author: Claude Code
Date: 2025-10-30
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# File paths
CSV_PATH = Path('data/tag_map_consolidated.csv')
BACKUP_PATH = Path('data/tag_map_consolidated.csv.backup-before-mining-reorg')


def read_csv() -> List[Dict[str, str]]:
    """Read CSV into list of dicts."""
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=['tag_name', 'new_tag', 'action', 'notes'])
        for row in reader:
            rows.append(row)
    return rows


def write_csv(rows: List[Dict[str, str]]) -> None:
    """Write list of dicts to CSV."""
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tag_name', 'new_tag', 'action', 'notes'])
        for row in rows:
            writer.writerow(row)


def main():
    print("=" * 80)
    print("MINING TAXONOMY REORGANIZATION")
    print("=" * 80)
    print()

    # Backup original
    import shutil
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Backup created: {BACKUP_PATH}")
    print()

    rows = read_csv()
    original_count = len(rows)
    print(f"Original CSV: {original_count} rows")
    print()

    # Track changes
    changes = {
        'deleted': 0,
        'added': 0,
        'company_merges': 0,
        'mines_moved': 0,
        'settlements_moved': 0,
        'events_moved': 0,
        'materials_added': 0,
        'commercial_merged': 0,
    }

    filtered_rows = []
    rows_to_add = []

    # Process each row
    for row in rows:
        tag = row['tag_name']
        action = row['action']
        notes = row['notes']

        if action != 'hierarchy':
            filtered_rows.append(row)
            continue

        # ================================================================
        # 1. DELETE: Remove deprecated/incorrect relationships
        # ================================================================

        # Delete Colliery (becomes synonym only)
        if tag == 'Colliery' and action == 'hierarchy':
            print(f"  ✗ Deleted: {tag} (becomes synonym for Coal mine)")
            changes['deleted'] += 1
            continue

        # Delete redundant company names (being merged)
        if (tag, notes) in [
            ('A.K.O. & M. Company', 'parent=Mining companies'),
            ('Australian Kerosene Shale and Oil Company', 'parent=Mining companies'),
            ('Katoomba Coal and Shale Mines', 'parent=Mining companies'),
            ('New South Wales Shale and Oil Co.', 'parent=Mining companies'),
            ('South Clifton Mine Co.', 'parent=Mining companies'),
            ('Waudby & Co.', 'parent=Mining companies'),
        ]:
            print(f"  ✗ Deleted: {tag} (merged into standardized name)")
            changes['company_merges'] += 1
            continue

        # Delete old mining company placements under Economic activities
        if tag in ['Gladstone Coal Company', 'Katoomba Coal and Shale Company',
                   'Katoomba Coal and Shale Mines', 'Sunny Corner Mining Company'] and \
           ('parent=Coal' in notes or 'parent=Mining' in notes):
            print(f"  ✗ Deleted: {tag} from Economic activities (moving to Agents)")
            changes['deleted'] += 1
            continue

        # Delete Coal intermediate tag under Coal mining
        if tag == 'Coal' and 'parent=Coal mining' in notes:
            print(f"  ✗ Deleted: {tag} from Coal mining (moving to Materials)")
            changes['deleted'] += 1
            continue

        # Delete mines from Economic activities (moving to Built Environment)
        if action == 'hierarchy' and ('parent=Coal' in notes or 'parent=Shale mines' in notes or
                                      'parent=Coal mines' in notes):
            if 'mine' in tag.lower() or 'mines' in tag.lower():
                print(f"  ✗ Deleted: {tag} from Economic activities (moving to Built Environment)")
                changes['deleted'] += 1
                continue

        # Delete mining settlements from Economic activities (moving to Places)
        if 'parent=Mining settlements' in notes and 'THEMATIC' not in notes:
            print(f"  ✗ Deleted: {tag} from Economic activities > Mining settlements")
            changes['deleted'] += 1
            continue

        # Delete Mining settlements category from Economic activities
        if tag == 'Mining settlements' and 'parent=Mining' in notes and 'THEMATIC' not in notes:
            print(f"  ✗ Deleted: {tag} category from Economic activities")
            changes['deleted'] += 1
            continue

        # Delete mining accidents from Economic activities (moving to Events)
        if 'parent=Mining accidents' in notes and 'THEMATIC' not in notes:
            print(f"  ✗ Deleted: {tag} from Economic activities > Mining accidents")
            changes['deleted'] += 1
            continue

        # Delete Mining accidents category from Economic activities
        if tag == 'Mining accidents' and 'parent=Mining' in notes and 'THEMATIC' not in notes:
            print(f"  ✗ Deleted: {tag} category from Economic activities")
            changes['deleted'] += 1
            continue

        # Delete South Clifton Tunnel Mine from companies
        if tag == 'South Clifton Tunnel Mine' and 'parent=Mining companies' in notes:
            print(f"  ✗ Deleted: {tag} from Mining companies (it's a physical mine)")
            changes['deleted'] += 1
            continue

        # Delete Commercial activities category
        if tag == 'Commercial activities' and action == 'hierarchy':
            print(f"  ✗ Deleted: {tag} category (merging into Economic activities)")
            changes['commercial_merged'] += 1
            continue

        # Update Liquor trade parent from Commercial activities to Economic activities
        if tag == 'Liquor trade' and 'parent=Commercial activities' in notes:
            row['notes'] = 'parent=Economic activities'
            print(f"  ✓ Updated: {tag} → parent=Economic activities")
            changes['commercial_merged'] += 1

        # Keep row
        filtered_rows.append(row)

    print()
    print("=" * 80)
    print("ADDING NEW RELATIONSHIPS")
    print("=" * 80)
    print()

    # ================================================================
    # 2. ADD: New categories and hierarchies
    # ================================================================

    # Add Materials facet entries
    materials_to_add = [
        ('Coal', 'Coal', 'hierarchy', 'parent=Materials'),
        ('Shale', 'Shale', 'hierarchy', 'parent=Materials'),
    ]

    for tag_name, new_tag, action, notes in materials_to_add:
        rows_to_add.append({
            'tag_name': tag_name,
            'new_tag': new_tag,
            'action': action,
            'notes': notes
        })
        print(f"  + Added: {tag_name} → {notes}")
        changes['materials_added'] += 1

    # Add Built Environment > Industrial buildings > Mines hierarchy
    mines_to_add = [
        ('Industrial buildings', 'Industrial buildings', 'hierarchy', 'parent=Built Environment'),
        ('Mines', 'Mines', 'hierarchy', 'parent=Industrial buildings'),
        ('Mine', 'Mine', 'hierarchy', 'parent=Mines (singular generic term)'),
        ('Coal mines', 'Coal mines', 'hierarchy', 'parent=Mines'),
        ('Coal mine', 'Coal mine', 'hierarchy', 'parent=Coal mines (singular generic term)'),
        ('Katoomba coal mines', 'Katoomba coal mines', 'hierarchy', 'parent=Coal mines'),
        ('South Clifton Tunnel Mine', 'South Clifton Tunnel Mine', 'hierarchy', 'parent=Coal mines'),
        ('Shale mines', 'Shale mines', 'hierarchy', 'parent=Mines'),
        ('Shale mine', 'Shale mine', 'hierarchy', 'parent=Shale mines (singular generic term)'),
        ('Katoomba Shale Mine', 'Katoomba Shale Mine', 'hierarchy', 'parent=Shale mines'),
        ('Megalong Shale Mines', 'Megalong Shale Mines', 'hierarchy', 'parent=Shale mines'),
        ("Nellie's Glen Shale Mine", "Nellie's Glen Shale Mine", 'hierarchy', 'parent=Shale mines'),
        ('Ruined Castle Shale Mine', 'Ruined Castle Shale Mine', 'hierarchy', 'parent=Shale mines'),
    ]

    for tag_name, new_tag, action, notes in mines_to_add:
        rows_to_add.append({
            'tag_name': tag_name,
            'new_tag': new_tag,
            'action': action,
            'notes': notes
        })
        print(f"  + Added: {tag_name} → {notes}")
        changes['mines_moved'] += 1

    # Add Places > Mining districts and Mining settlements
    places_to_add = [
        ('Mining districts', 'Mining districts', 'hierarchy', 'parent=Places'),
        ('Mining district', 'Mining district', 'hierarchy', 'parent=Mining districts (singular generic term)'),
        ("Nellie's Glen", "Nellie's Glen", 'hierarchy', 'parent=Mining districts'),
        ('Ruined Castle', 'Ruined Castle', 'hierarchy', 'parent=Mining districts'),
        ('South Clifton', 'South Clifton', 'hierarchy', 'parent=Mining districts'),
        ('Mining settlements', 'Mining settlements', 'hierarchy', 'parent=Settlements'),
        ('Mining settlement', 'Mining settlement', 'hierarchy', 'parent=Mining settlements (singular generic term)'),
        ('Middle camp', 'Middle camp', 'hierarchy', 'parent=Mining settlements'),
        ("Nellie's Glen", "Nellie's Glen", 'hierarchy', 'parent=Mining settlements (poly-hierarchy with districts)'),
        ('Ruined Castle', 'Ruined Castle', 'hierarchy', 'parent=Mining settlements (poly-hierarchy with districts)'),
    ]

    for tag_name, new_tag, action, notes in places_to_add:
        rows_to_add.append({
            'tag_name': tag_name,
            'new_tag': new_tag,
            'action': action,
            'notes': notes
        })
        print(f"  + Added: {tag_name} → {notes}")
        changes['settlements_moved'] += 1

    # Add Events > Mining events
    events_to_add = [
        ('Mining events', 'Mining events', 'hierarchy', 'parent=Events'),
        ('Mining accidents', 'Mining accidents', 'hierarchy', 'parent=Mining events'),
        ('Mining accident', 'Mining accident', 'hierarchy', 'parent=Mining accidents (singular generic term)'),
        ('Mount Kembla Disaster', 'Mount Kembla Disaster', 'hierarchy', 'parent=Mining accidents'),
        ('Mine closure', 'Mine closure', 'hierarchy', 'parent=Mining events'),
    ]

    for tag_name, new_tag, action, notes in events_to_add:
        rows_to_add.append({
            'tag_name': tag_name,
            'new_tag': new_tag,
            'action': action,
            'notes': notes
        })
        print(f"  + Added: {tag_name} → {notes}")
        changes['events_moved'] += 1

    # Add standardized company names to Agents > Mining companies
    companies_to_add = [
        ('Australian Kerosene Oil and Mineral Company', 'Australian Kerosene Oil and Mineral Company',
         'hierarchy', 'parent=Mining companies (primary: absorbs A.K.O. & M. Company, Australian Kerosene Shale and Oil Company)'),
        ('Katoomba Coal and Shale Company', 'Katoomba Coal and Shale Company',
         'hierarchy', 'parent=Mining companies (primary: absorbs Katoomba Coal and Shale Mines)'),
        ('New South Wales Shale and Oil Company', 'New South Wales Shale and Oil Company',
         'hierarchy', 'parent=Mining companies (primary: absorbs New South Wales Shale and Oil Co.)'),
        ('South Clifton Mine Company', 'South Clifton Mine Company',
         'hierarchy', 'parent=Mining companies (primary: absorbs South Clifton Mine Co.)'),
        ('Waudby and Company', 'Waudby and Company',
         'hierarchy', 'parent=Mining companies (primary: absorbs Waudby & Co.)'),
    ]

    for tag_name, new_tag, action, notes in companies_to_add:
        rows_to_add.append({
            'tag_name': tag_name,
            'new_tag': new_tag,
            'action': action,
            'notes': notes
        })
        print(f"  + Added: {tag_name} → {notes}")

    print()

    # Combine filtered rows with new rows
    final_rows = filtered_rows + rows_to_add

    # Write back to CSV
    write_csv(final_rows)

    final_count = len(final_rows)

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original rows:        {original_count}")
    print(f"Deleted rows:         {changes['deleted']}")
    print(f"Added rows:           {len(rows_to_add)}")
    print(f"Final rows:           {final_count}")
    print(f"Net change:           {final_count - original_count:+d}")
    print()
    print("Changes by category:")
    print(f"  Company merges:        {changes['company_merges']}")
    print(f"  Mines moved:           {changes['mines_moved']}")
    print(f"  Settlements moved:     {changes['settlements_moved']}")
    print(f"  Events moved:          {changes['events_moved']}")
    print(f"  Materials added:       {changes['materials_added']}")
    print(f"  Commercial merged:     {changes['commercial_merged']}")
    print()
    print(f"✓ Updated: {CSV_PATH}")
    print(f"✓ Backup: {BACKUP_PATH}")
    print()


if __name__ == '__main__':
    main()
