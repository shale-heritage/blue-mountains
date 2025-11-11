#!/usr/bin/env python3
"""
Fix orphaned tags in tag_application_mapping.csv.

Corrects tags that don't exist in taxonomy:
1. US spelling: organization → organisation
2. Typos: Grant Hotel → Grand Hotel, Wentwork → Wentworth
3. Malformed entries with newlines
4. Case variants: Drunkenness → drunkenness
5. Remove invalid placeholders
"""

import csv
import io
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TAG_APP_FILE = BASE_DIR / 'data' / 'tag_application_mapping.csv'
BACKUP_FILE = TAG_APP_FILE.with_suffix('.csv.backup-fix-orphaned')

# Mapping of incorrect → correct tag names
TAG_CORRECTIONS = {
    # US spelling fixes
    'Church of England Katoomba (organization)': 'Church of England Katoomba (organisation)',
    'Congregational Church (organization)': 'Congregational Church (organisation)',
    'Congregational Church Katoomba South (organization)': 'Congregational Church Katoomba South (organisation)',
    'Methodist Church Katoomba (organization)': 'Methodist Church Katoomba (organisation)',
    'Presbyterian Church Leura (organization)': 'Presbyterian Church Leura (organisation)',
    'Presbyterian Church Wentworth Falls (organization)': 'Presbyterian Church Wentworth Falls (organisation)',
    'Roman Catholic Church Blackheath (organization)': 'Roman Catholic Church Blackheath (organisation)',
    'Roman Catholic Church Lawson (organization)': 'Roman Catholic Church Lawson (organisation)',
    'Roman Catholic Church Megalong (organization)': 'Roman Catholic Church Megalong (organisation)',
    'Wesleyan Church Katoomba (organization)': 'Wesleyan Church Katoomba (organisation)',

    # Typos
    'Grant Hotel': 'Grand Hotel',
    'Wentwork Falls Hotel': 'Wentworth Falls Hotel',
    'hartley Vale': 'Hartley Vale',
    'Hatley Vale': 'Hartley Vale',

    # Case variants
    'Drunkenness': 'drunkenness (intoxication)',
    'Inquests': 'inquest',
    'Buildings': 'building',  # or remove - too generic
    'Sexual assault': 'sexual assault',
    'Indigenous Australians': 'Aboriginal people',  # or appropriate variant
    'TBD': '',  # Remove placeholder

    # Truncated/malformed
    'Accommodation and': '',  # Remove
    'Hotel\n (not only here but in all instances)': 'hotel',  # Fix newline
}

def load_mappings():
    """Load mappings with normalized line endings."""
    with open(TAG_APP_FILE, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
    reader = csv.DictReader(io.StringIO(content))
    return list(reader), reader.fieldnames

def fix_tag_list(tag_string):
    """Fix a pipe-separated list of tags."""
    if not tag_string:
        return tag_string

    tags = [t.strip() for t in tag_string.split(' | ')]
    fixed_tags = []

    for tag in tags:
        # Remove newlines and extra whitespace
        tag = tag.replace('\n', '').replace('\r', '').strip()
        if not tag:
            continue

        # Apply corrections
        if tag in TAG_CORRECTIONS:
            corrected = TAG_CORRECTIONS[tag]
            if corrected:  # Only add if replacement isn't empty
                fixed_tags.append(corrected)
        else:
            fixed_tags.append(tag)

    return ' | '.join(fixed_tags)

def process_mappings(rows):
    """Process all mapping rows and fix orphaned tags."""
    modified_count = 0
    modifications = []

    for row in rows:
        old_add_tags = row.get('add_tags', '')
        fixed_add_tags = fix_tag_list(old_add_tags)

        if old_add_tags != fixed_add_tags:
            modifications.append({
                'title': row.get('title', 'Unknown'),
                'old': old_add_tags,
                'new': fixed_add_tags
            })
            row['add_tags'] = fixed_add_tags
            modified_count += 1

    return rows, modifications, modified_count

def save_mappings(rows, fieldnames):
    """Save corrected mappings."""
    import shutil
    shutil.copy2(TAG_APP_FILE, BACKUP_FILE)
    print(f"✓ Backup created: {BACKUP_FILE}")

    with open(TAG_APP_FILE, 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated mappings saved: {TAG_APP_FILE}")

def main():
    print("=" * 70)
    print("FIX ORPHANED TAGS IN MAPPINGS")
    print("=" * 70)
    print()

    # Load
    print("Loading mappings...")
    rows, fieldnames = load_mappings()
    print(f"✓ Loaded {len(rows)} mapping rows")
    print()

    # Process
    print("Fixing orphaned tags...")
    corrected_rows, modifications, modified_count = process_mappings(rows)
    print(f"✓ Modified {modified_count} rows")
    print()

    # Show sample modifications
    if modifications:
        print(f"Sample modifications ({min(10, len(modifications))}):")
        for mod in modifications[:10]:
            print(f"  {mod['title'][:50]:50}")
            print(f"    Old: {mod['old'][:60]}")
            print(f"    New: {mod['new'][:60]}")
        if len(modifications) > 10:
            print(f"    ... and {len(modifications) - 10} more")
        print()

    # Save
    save_mappings(corrected_rows, fieldnames)

    print()
    print("=" * 70)
    print("COMPLETE: Orphaned tags fixed")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - Rows modified: {modified_count}")
    print(f"  - Backup saved: {BACKUP_FILE.name}")
    print()

if __name__ == '__main__':
    main()
