#!/usr/bin/env python3
"""
Fix thematic facet capitalisation inconsistencies.

Standardises all thematic grouping names to use title case consistently.
Example: "alcohol & temperance - THEMATIC" → "Alcohol & Temperance - THEMATIC"
"""

import csv
import sys
from pathlib import Path
import re

# File paths
BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
BACKUP_FILE = TAG_MAP_FILE.with_suffix('.csv.backup-thematic-case')

def to_title_case_thematic(text):
    """
    Convert thematic facet names to title case.

    Handles special cases like '&' and preserves ' - THEMATIC' suffix.
    Example: "alcohol & temperance - THEMATIC" → "Alcohol & Temperance - THEMATIC"
    """
    if not text or ' - THEMATIC' not in text:
        return text

    # Split off the THEMATIC suffix
    base_text = text.replace(' - THEMATIC', '')

    # Title case the base, handling '&' properly
    words = base_text.split()
    titled_words = []
    for word in words:
        if word == '&':
            titled_words.append('&')
        else:
            # Title case: capitalize first letter, lowercase rest
            titled_words.append(word[0].upper() + word[1:].lower() if len(word) > 0 else word)

    return ' '.join(titled_words) + ' - THEMATIC'

def load_taxonomy():
    """Load the taxonomy CSV file."""
    rows = []
    with open(TAG_MAP_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def process_taxonomy(rows):
    """Process all rows and fix thematic facet capitalisation."""
    modified_count = 0
    modifications = []
    thematic_changes = {}  # Track old → new thematic names

    for row in rows:
        old_tag = row['old_tag']
        new_tag = row['new_tag']
        parent_value = row.get('parent_broader_category', '')

        # Fix tags that are themselves thematic facets
        fixed_old_tag = to_title_case_thematic(old_tag)
        fixed_new_tag = to_title_case_thematic(new_tag)

        # Fix parent references to thematic facets
        fixed_parent = parent_value
        if parent_value and ' - THEMATIC' in parent_value:
            if parent_value.startswith('parent='):
                parent_tag = parent_value.replace('parent=', '').strip()
                fixed_parent_tag = to_title_case_thematic(parent_tag)
                if parent_tag != fixed_parent_tag:
                    fixed_parent = f"parent={fixed_parent_tag}"
                    thematic_changes[parent_tag] = fixed_parent_tag
            else:
                # Direct parent reference without 'parent=' prefix
                fixed_parent = to_title_case_thematic(parent_value)
                if parent_value != fixed_parent:
                    thematic_changes[parent_value] = fixed_parent

        # Track modifications
        if (old_tag != fixed_old_tag or new_tag != fixed_new_tag or
            parent_value != fixed_parent):
            modifications.append({
                'old': f"{old_tag} → {new_tag} (parent: {parent_value})",
                'new': f"{fixed_old_tag} → {fixed_new_tag} (parent: {fixed_parent})"
            })
            modified_count += 1

        # Update row
        row['old_tag'] = fixed_old_tag
        row['new_tag'] = fixed_new_tag
        row['parent_broader_category'] = fixed_parent

    return rows, modifications, modified_count, thematic_changes

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

def verify_consistency(rows):
    """Verify all thematic facets now have consistent capitalisation."""
    thematic_variations = {}

    for row in rows:
        for field in ['old_tag', 'new_tag', 'parent_broader_category']:
            value = row.get(field, '')
            if ' - THEMATIC' in value:
                # Normalize by removing parent= prefix
                normalized = value.replace('parent=', '').strip()
                # Group by lowercase version
                key = normalized.lower()
                if key not in thematic_variations:
                    thematic_variations[key] = set()
                thematic_variations[key].add(normalized)

    # Find any that still have variations
    inconsistent = []
    for key, variations in thematic_variations.items():
        if len(variations) > 1:
            inconsistent.append({
                'key': key,
                'variations': list(variations)
            })

    return inconsistent

def main():
    print("=" * 70)
    print("THEMATIC FACET CAPITALISATION FIX - Standardising to title case")
    print("=" * 70)
    print()

    # Load taxonomy
    print("Loading taxonomy...")
    rows = load_taxonomy()
    print(f"✓ Loaded {len(rows)} rows")
    print()

    # Process and fix
    print("Processing thematic facet capitalisation...")
    corrected_rows, modifications, modified_count, thematic_changes = process_taxonomy(rows)
    print(f"✓ Modified {modified_count} rows")
    print()

    # Show thematic name changes
    if thematic_changes:
        print(f"Thematic facet names standardised ({len(set(thematic_changes.values()))} unique):")
        seen = set()
        for old, new in thematic_changes.items():
            if new not in seen:
                print(f"  '{old}' → '{new}'")
                seen.add(new)
        print()

    # Show some modifications
    if modifications:
        print(f"Sample modifications ({min(10, len(modifications))} of {len(modifications)}):")
        for i, mod in enumerate(modifications[:10], 1):
            print(f"  {i}. {mod['old']}")
            print(f"     → {mod['new']}")
        if len(modifications) > 10:
            print(f"     ... and {len(modifications) - 10} more")
        print()

    # Verify consistency
    print("Verifying thematic facet consistency...")
    inconsistent = verify_consistency(corrected_rows)

    if inconsistent:
        print(f"⚠ Found {len(inconsistent)} thematic facets with remaining inconsistencies:")
        for item in inconsistent:
            print(f"  - {item['key']}: {', '.join(item['variations'])}")
        print()
    else:
        print("✓ All thematic facets have consistent capitalisation")
        print()

    # Save
    save_taxonomy(corrected_rows)

    print()
    print("=" * 70)
    print("COMPLETE: Thematic facet capitalisation standardised")
    print("=" * 70)
    print()
    print(f"Summary:")
    print(f"  - Rows modified: {modified_count}")
    print(f"  - Thematic facets standardised: {len(set(thematic_changes.values()))}")
    print(f"  - Backup saved: {BACKUP_FILE.name}")
    print()

if __name__ == '__main__':
    main()
