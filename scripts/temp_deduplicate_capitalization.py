#!/usr/bin/env python3
"""
Deduplication Script: Remove Capitalized Category Duplicates

Problem: Case-sensitive taxonomy has duplicate entries where both "Term" and "term"
exist, creating false top-level facets in hierarchy visualizations.

Solution: Keep lowercase versions (Getty AAT standard), remove capitalized duplicates,
update all parent references to lowercase.

Usage: python3 scripts/temp_deduplicate_capitalization.py
"""

import csv
import shutil
from collections import defaultdict
from pathlib import Path

# File paths
CSV_PATH = Path('data/tag_map_consolidated.csv')
BACKUP_PATH = Path('data/tag_map_consolidated.csv.pre-dedup-backup')

# Primary facets and proper nouns that SHOULD be capitalized
PRESERVE_CAPITALIZATION = {
    'Activities', 'Agents', 'Associated Concepts', 'Built Environment',
    'Events', 'Information Forms', 'Materials', 'Places',
    'Law enforcement (intermediate facet)', 'Legal officials (intermediate facet)',
    # Add more proper nouns as needed
}

def is_proper_noun_or_primary_facet(term):
    """Check if term should preserve capitalization."""
    if term in PRESERVE_CAPITALIZATION:
        return True
    # Check if it's a proper noun (contains specific patterns)
    # Proper nouns have capital letters mid-word like "Mount Victoria"
    # Category terms like "Commercial businesses" should be lowercase
    words = term.split()
    if len(words) > 1:
        # Multi-word terms - check if it's a place name, person name, etc.
        # For now, use simple heuristic: if ALL words capitalized, might be category
        all_cap = all(w[0].isupper() for w in words if w)
        # If it's something like "Commercial businesses" (category pattern), return False
        # If it's "Mount Victoria" (proper noun pattern), return True
        # This is imperfect but we'll rely on the duplicates check
        pass
    return False

def analyze_duplicates(rows):
    """Find case-insensitive duplicates in hierarchy entries."""
    # Group by lowercase new_tag for hierarchy entries
    hierarchy_entries = defaultdict(list)

    for i, row in enumerate(rows):
        if row['action'] == 'hierarchy':
            key = row['new_tag'].lower()
            hierarchy_entries[key].append((i, row))

    # Find duplicates
    duplicates = {}
    for key, entries in hierarchy_entries.items():
        if len(entries) > 1:
            # Check if there are capitalization variations
            tags = [row['new_tag'] for _, row in entries]
            unique_tags = set(tags)
            if len(unique_tags) > 1:
                # We have capitalization duplicates
                duplicates[key] = entries

    return duplicates

def main():
    print("="*80)
    print("DEDUPLICATION SCRIPT: Remove Capitalized Category Duplicates")
    print("="*80)

    # Step 1: Create backup
    print(f"\n[1/5] Creating backup...")
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Backup created: {BACKUP_PATH}")

    # Step 2: Read CSV
    print(f"\n[2/5] Reading CSV...")
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"✓ Loaded {len(rows)} rows")

    # Step 3: Analyze duplicates
    print(f"\n[3/5] Analyzing case-insensitive duplicates...")
    duplicates = analyze_duplicates(rows)
    print(f"✓ Found {len(duplicates)} terms with capitalization duplicates")

    if not duplicates:
        print("\n✓ No duplicates found! CSV is clean.")
        return

    # Show duplicates
    print("\nDuplicates found:")
    for key, entries in sorted(duplicates.items())[:10]:  # Show first 10
        tags = [row['new_tag'] for _, row in entries]
        print(f"  • {key}: {tags}")
    if len(duplicates) > 10:
        print(f"  ... and {len(duplicates) - 10} more")

    # Step 4: Determine which to keep/remove
    print(f"\n[4/5] Planning deduplication...")
    to_remove = []
    canonical_mapping = {}  # Maps capitalized → lowercase canonical form

    for key, entries in duplicates.items():
        # Find lowercase version
        lowercase_entries = [(i, row) for i, row in entries if row['new_tag'] == row['new_tag'].lower()]
        capitalized_entries = [(i, row) for i, row in entries if row['new_tag'] != row['new_tag'].lower()]

        if lowercase_entries:
            # Keep lowercase, remove capitalized
            canonical = lowercase_entries[0][1]['new_tag']
            for i, row in capitalized_entries:
                to_remove.append(i)
                canonical_mapping[row['new_tag']] = canonical
        else:
            # No lowercase version exists, keep the first one and lowercase it
            # This shouldn't happen often
            keep_idx, keep_row = entries[0]
            canonical = keep_row['new_tag'].lower()
            rows[keep_idx]['new_tag'] = canonical
            rows[keep_idx]['old_tag'] = canonical
            canonical_mapping[keep_row['new_tag']] = canonical

            for i, row in entries[1:]:
                to_remove.append(i)
                canonical_mapping[row['new_tag']] = canonical

    print(f"✓ Will remove {len(to_remove)} duplicate rows")
    print(f"✓ Will update {len(canonical_mapping)} parent references")

    # Show what will be removed
    print("\nRemoving capitalized duplicates:")
    for idx in sorted(to_remove)[:10]:
        row = rows[idx]
        canonical = canonical_mapping.get(row['new_tag'], '?')
        print(f"  - Line {idx+2}: {row['new_tag']} → keeping {canonical}")
    if len(to_remove) > 10:
        print(f"  ... and {len(to_remove) - 10} more")

    # Step 5: Apply changes
    print(f"\n[5/5] Applying changes...")

    # Remove duplicates (in reverse order to preserve indices)
    for idx in sorted(to_remove, reverse=True):
        del rows[idx]
    print(f"✓ Removed {len(to_remove)} duplicate rows")

    # Update parent references
    parent_updates = 0
    for row in rows:
        if 'parent=' in row['notes']:
            # Extract parent value
            notes = row['notes']
            if notes.startswith('parent='):
                parent_val = notes[7:]  # Everything after "parent="
                # Check if this parent needs updating
                if parent_val in canonical_mapping:
                    new_parent = canonical_mapping[parent_val]
                    row['notes'] = f'parent={new_parent}'
                    parent_updates += 1

    print(f"✓ Updated {parent_updates} parent references to lowercase")

    # Write updated CSV
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✓ Updated CSV written: {CSV_PATH}")
    print(f"\n{'='*80}")
    print("DEDUPLICATION COMPLETE")
    print("="*80)
    print(f"Summary:")
    print(f"  • Rows removed: {len(to_remove)}")
    print(f"  • Parent refs updated: {parent_updates}")
    print(f"  • Final row count: {len(rows)}")
    print(f"  • Backup saved to: {BACKUP_PATH}")
    print(f"\nNext step: Regenerate visualizations to verify 10 primary facets")

if __name__ == '__main__':
    main()
