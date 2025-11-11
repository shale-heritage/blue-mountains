#!/usr/bin/env python3
"""
Fix case variation duplicates in taxonomy.

Standardises capitalisation for terms that appear with multiple case variations.
Uses lowercase for generic terms, preserves capitalisation for proper names.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

# File paths
BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
BACKUP_FILE = TAG_MAP_FILE.with_suffix('.csv.backup-case-variations')

# Standardisation rules: {incorrect: correct}
CASE_FIXES = {
    'Children': 'children',
    'Drinking (alcohol)': 'drinking (alcohol)',
    'Family Hotel': 'family hotel',
    'Mailman': 'mailman',
    'Postal service': 'postal service',
    'Public house': 'public house',
    "Publican's licensing": "publican's licensing",
    'Unlicensed sales': 'unlicensed sales',
    'Whisky': 'whisky',
}

def load_taxonomy():
    """Load the taxonomy CSV file."""
    rows = []
    with open(TAG_MAP_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def fix_case(text):
    """Fix case variations according to standardisation rules."""
    if not text:
        return text
    # Check for exact matches in case fix dictionary
    if text in CASE_FIXES:
        return CASE_FIXES[text]
    return text

def process_taxonomy(rows):
    """Process all rows and fix case variations."""
    modified_count = 0
    modifications = []

    for row in rows:
        old_tag = row['old_tag']
        new_tag = row['new_tag']
        parent_value = row.get('parent_broader_category', '')
        notes = row.get('notes', '')

        # Fix old_tag
        fixed_old_tag = fix_case(old_tag)
        # Fix new_tag
        fixed_new_tag = fix_case(new_tag)
        # Fix parent reference (extract tag name from parent=X format)
        fixed_parent = parent_value
        if parent_value.startswith('parent='):
            parent_tag = parent_value.replace('parent=', '').strip()
            fixed_parent_tag = fix_case(parent_tag)
            if parent_tag != fixed_parent_tag:
                fixed_parent = f"parent={fixed_parent_tag}"

        # Fix notes field (may contain case variations in descriptions)
        fixed_notes = notes
        for incorrect, correct in CASE_FIXES.items():
            fixed_notes = fixed_notes.replace(incorrect, correct)

        # Track modifications
        if (old_tag != fixed_old_tag or new_tag != fixed_new_tag or
            parent_value != fixed_parent or notes != fixed_notes):
            modifications.append({
                'old': f"{old_tag} → {new_tag} (parent: {parent_value})",
                'new': f"{fixed_old_tag} → {fixed_new_tag} (parent: {fixed_parent})"
            })
            modified_count += 1

        # Update row
        row['old_tag'] = fixed_old_tag
        row['new_tag'] = fixed_new_tag
        row['parent_broader_category'] = fixed_parent
        row['notes'] = fixed_notes

    return rows, modifications, modified_count

def check_duplicates(rows):
    """Check for duplicate tag names (case-insensitive) within same facet."""
    # Group tags by primary facet and name (case-insensitive)
    facet_tags = defaultdict(lambda: defaultdict(list))

    for row in rows:
        if row['action'] not in ['hierarchy', 'keep']:
            continue

        tag_name = row['new_tag']
        # Try to determine primary facet by tracing parents
        # For now, just collect all tags and check for case-insensitive duplicates
        key = tag_name.lower()
        facet_tags['all'][key].append(tag_name)

    # Find duplicates
    duplicates = []
    for facet, tags in facet_tags.items():
        for key, tag_list in tags.items():
            # Get unique case variations
            unique_variations = list(set(tag_list))
            if len(unique_variations) > 1:
                duplicates.append({
                    'key': key,
                    'variations': unique_variations,
                    'count': len(tag_list)
                })

    return duplicates

def save_taxonomy(rows):
    """Save the corrected taxonomy."""
    # Create backup
    if TAG_MAP_FILE.exists():
        import shutil
        shutil.copy2(TAG_MAP_FILE, BACKUP_FILE)
        print(f"✓ Backup created: {BACKUP_FILE}")

    # Write corrected data
    fieldnames = rows[0].keys()
    with open(TAG_MAP_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Corrected taxonomy saved: {TAG_MAP_FILE}")

def main():
    print("=" * 70)
    print("CASE VARIATION FIX - Standardising capitalisation")
    print("=" * 70)
    print()
    print("Standardisation rules:")
    for incorrect, correct in CASE_FIXES.items():
        print(f"  '{incorrect}' → '{correct}'")
    print()

    # Load taxonomy
    print("Loading taxonomy...")
    rows = load_taxonomy()
    print(f"✓ Loaded {len(rows)} rows")
    print()

    # Process and fix
    print("Processing case variations...")
    corrected_rows, modifications, modified_count = process_taxonomy(rows)
    print(f"✓ Modified {modified_count} rows")
    print()

    # Show modifications
    if modifications:
        print("Modifications made:")
        for i, mod in enumerate(modifications[:15], 1):
            print(f"  {i}. {mod['old']}")
            print(f"     → {mod['new']}")
        if len(modifications) > 15:
            print(f"     ... and {len(modifications) - 15} more")
        print()

    # Check for remaining duplicates
    print("Checking for remaining case-insensitive duplicates...")
    duplicates = check_duplicates(corrected_rows)

    if duplicates:
        print(f"⚠ Found {len(duplicates)} case-insensitive duplicates (may be expected for polyhierarchy):")
        for dup in duplicates[:10]:
            print(f"  - '{dup['key']}' appears as: {', '.join(dup['variations'])} ({dup['count']} times)")
        if len(duplicates) > 10:
            print(f"    ... and {len(duplicates) - 10} more")
        print()
    else:
        print("✓ No case-insensitive duplicates found")
        print()

    # Save
    save_taxonomy(corrected_rows)

    print()
    print("=" * 70)
    print("COMPLETE: Case variation corrections applied successfully")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - Rows modified: {modified_count}")
    print(f"  - Backup saved: {BACKUP_FILE.name}")
    print()

if __name__ == '__main__':
    main()
