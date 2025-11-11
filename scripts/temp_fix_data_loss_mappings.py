#!/usr/bin/env python3
"""
Fix 5 data loss mappings (items with remove_tags but no add_tags).

Changes:
1. Blue Mountains Railway Tourist Guide - deferred (return to user)
2. A Public Meeting - add Carrington Hotel and bushfire tags
3. Licensing - add publican's licensing tag
4. Megalong Valley - removal confirmed (no Nellie's Glen mention)
5. Megalong Matters - removal confirmed (no church mention)

Also restructures disasters hierarchy in taxonomy:
- Create disasters (plural parent)
- Move disaster to be child of disasters
- Add bushfire under disasters
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path


def backup_file(filepath):
    """Create timestamped backup."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = f"{filepath}.backup-data-loss-fix-{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path


def restructure_disasters_hierarchy(taxonomy_path):
    """Restructure disaster/disasters hierarchy and add bushfire."""

    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Remove existing disaster entry (will be recreated under disasters)
    rows = [r for r in rows if not (r['old_tag'] == 'disaster'
                                     and r['action'] == 'hierarchy'
                                     and 'parent=accidents' in r.get('notes', ''))]

    # Add new hierarchy entries
    new_entries = [
        # disasters plural parent
        ('disasters', 'disasters', 'hierarchy',
         'parent=accidents', ''),

        # disaster singular generic leaf
        ('disaster', 'disaster', 'hierarchy',
         'parent=disasters', 'Singular generic term'),

        # bushfire
        ('bushfire', 'bushfire', 'hierarchy',
         'parent=disasters', ''),
    ]

    for old_tag, new_tag, action, notes, parent in new_entries:
        rows.append({
            'old_tag': old_tag,
            'new_tag': new_tag,
            'action': action,
            'notes': notes,
            'parent_broader_category': parent
        })

    # Write back
    with open(taxonomy_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action',
                                                 'notes', 'parent_broader_category'])
        writer.writeheader()
        writer.writerows(rows)

    return len(new_entries)


def fix_data_loss_mappings(mapping_path):
    """Fix the data loss mappings by adding appropriate tags."""

    with open(mapping_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    fixes_applied = 0

    for row in rows:
        title = row['title']
        date = row['date']
        remove_tags = row.get('remove_tags', '').strip()
        add_tags = row.get('add_tags', '').strip()

        # Item 2: A Public Meeting - add Carrington Hotel and bushfire
        if (title == 'A Public Meeting.'
            and date == '13 January 1905'
            and remove_tags == 'Accommodation'
            and not add_tags):
            row['add_tags'] = 'Carrington Hotel | bushfire'
            row['notes'] = 'Added hotel and disaster tags based on content review'
            fixes_applied += 1

        # Item 3: Licensing - add publican's licensing
        elif (title == 'Licensing.'
              and date == '1 October 1892'
              and remove_tags == 'Accommodation'
              and not add_tags):
            row['add_tags'] = "publican's licensing"
            row['notes'] = 'Added licensing tag based on content review'
            fixes_applied += 1

        # Items 4 and 5 - removals confirmed as correct, update notes
        elif (title == 'Megalong Valley.'
              and date == '1 September 1893'
              and remove_tags == "Nellie's Glen"):
            row['notes'] = "Confirmed: Nellie's Glen not mentioned in source - removal correct"
            fixes_applied += 1

        elif (title == 'Megalong Matters.'
              and date == '5 August 1892'
              and remove_tags == 'church (building)'):
            row['notes'] = 'Confirmed: no church mention in source - removal correct'
            fixes_applied += 1

    # Write back
    with open(mapping_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return fixes_applied


def main():
    taxonomy_path = Path('data/tag_map_consolidated.csv')
    mapping_path = Path('data/tag_application_mapping.csv')

    print("="*80)
    print("FIX DATA LOSS MAPPINGS")
    print("="*80)
    print()

    # Backup files
    print("Creating backups...")
    backup_file(taxonomy_path)
    backup_file(mapping_path)
    print()

    # Restructure disasters hierarchy
    print("Restructuring disasters hierarchy in taxonomy...")
    entries_added = restructure_disasters_hierarchy(taxonomy_path)
    print(f"✓ Added {entries_added} entries (disasters parent, disaster leaf, bushfire)")
    print()

    # Fix mappings
    print("Fixing data loss mappings...")
    fixes = fix_data_loss_mappings(mapping_path)
    print(f"✓ Fixed {fixes} mapping entries:")
    print("  - Item 2: Added Carrington Hotel and bushfire")
    print("  - Item 3: Added publican's licensing")
    print("  - Item 4: Confirmed Nellie's Glen removal")
    print("  - Item 5: Confirmed church removal")
    print()

    print("✓ Data loss mappings resolved!")
    print()
    print("Remaining: Item 1 (Blue Mountains Railway Tourist Guide) - deferred")


if __name__ == '__main__':
    main()
