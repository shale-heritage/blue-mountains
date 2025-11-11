#!/usr/bin/env python3
"""
Fix US spelling violations in taxonomy.

Replaces "organization" with "organisation" (UK spelling) in tag_map_consolidated.csv
while validating that all parent-child relationships remain intact.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

# File paths
BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
BACKUP_FILE = TAG_MAP_FILE.with_suffix('.csv.backup-us-spelling')

def load_taxonomy():
    """Load the taxonomy CSV file."""
    rows = []
    with open(TAG_MAP_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def fix_us_spelling(text):
    """Replace US spelling with UK spelling."""
    if not text:
        return text
    return text.replace('organization', 'organisation').replace('Organization', 'Organisation')

def process_taxonomy(rows):
    """Process all rows and fix US spelling."""
    modified_count = 0
    modifications = []

    for row in rows:
        old_tag = row['old_tag']
        new_tag = row['new_tag']
        parent_value = row.get('parent_broader_category', '')

        # Fix old_tag
        fixed_old_tag = fix_us_spelling(old_tag)
        # Fix new_tag
        fixed_new_tag = fix_us_spelling(new_tag)
        # Fix parent reference
        fixed_parent = fix_us_spelling(parent_value)

        # Track modifications
        if old_tag != fixed_old_tag or new_tag != fixed_new_tag or parent_value != fixed_parent:
            modifications.append({
                'old': f"{old_tag} → {new_tag} (parent: {parent_value})",
                'new': f"{fixed_old_tag} → {fixed_new_tag} (parent: {fixed_parent})"
            })
            modified_count += 1

        # Update row
        row['old_tag'] = fixed_old_tag
        row['new_tag'] = fixed_new_tag
        row['parent_broader_category'] = fixed_parent

    return rows, modifications, modified_count

def validate_relationships(rows):
    """Validate that all parent references resolve correctly."""
    # Build a set of all tags that exist
    all_tags = set()
    for row in rows:
        if row['action'] in ['hierarchy', 'keep']:
            all_tags.add(row['new_tag'])

    # Check that all parent references exist
    broken_refs = []
    for row in rows:
        parent = row.get('parent_broader_category', '')
        if parent and not parent.startswith('parent='):
            continue

        if parent:
            parent_tag = parent.replace('parent=', '').strip()
            # Skip Getty AAT primary facet markers and thematic groupings
            if '(Getty AAT primary facet)' in parent_tag or '- THEMATIC' in parent_tag:
                continue
            # Check if parent exists
            if parent_tag and parent_tag not in all_tags:
                broken_refs.append({
                    'tag': row['new_tag'],
                    'missing_parent': parent_tag
                })

    return broken_refs

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
    print("US SPELLING FIX - organization → organisation")
    print("=" * 70)
    print()

    # Load taxonomy
    print("Loading taxonomy...")
    rows = load_taxonomy()
    print(f"✓ Loaded {len(rows)} rows")
    print()

    # Process and fix
    print("Processing US spelling corrections...")
    corrected_rows, modifications, modified_count = process_taxonomy(rows)
    print(f"✓ Modified {modified_count} rows")
    print()

    # Show modifications
    if modifications:
        print("Modifications made:")
        for i, mod in enumerate(modifications[:10], 1):
            print(f"  {i}. {mod['old']}")
            print(f"     → {mod['new']}")
        if len(modifications) > 10:
            print(f"     ... and {len(modifications) - 10} more")
        print()

    # Validate relationships
    print("Validating parent-child relationships...")
    broken_refs = validate_relationships(corrected_rows)

    if broken_refs:
        print(f"✗ Found {len(broken_refs)} broken references:")
        for ref in broken_refs[:10]:
            print(f"  - Tag '{ref['tag']}' references missing parent '{ref['missing_parent']}'")
        if len(broken_refs) > 10:
            print(f"    ... and {len(broken_refs) - 10} more")
        print()
        print("ERROR: Validation failed. Not saving changes.")
        sys.exit(1)
    else:
        print("✓ All parent-child relationships valid")
        print()

    # Verify no instances of "organization" remain
    check_count = 0
    for row in corrected_rows:
        for field in ['old_tag', 'new_tag', 'parent_broader_category']:
            if 'organization' in row.get(field, '').lower():
                check_count += 1

    if check_count > 0:
        print(f"✗ ERROR: Found {check_count} remaining instances of 'organization'")
        sys.exit(1)
    else:
        print("✓ Verification: Zero instances of 'organization' remain")
        print()

    # Save
    save_taxonomy(corrected_rows)

    print()
    print("=" * 70)
    print("COMPLETE: US spelling corrections applied successfully")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - Rows modified: {modified_count}")
    print(f"  - Relationships validated: PASS")
    print(f"  - Backup saved: {BACKUP_FILE.name}")
    print()

if __name__ == '__main__':
    main()
