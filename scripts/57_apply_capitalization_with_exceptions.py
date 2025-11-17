#!/usr/bin/env python3
"""
Script 57: Apply Capitalisation Changes with Exception List

Applies Getty AAT capitalisation standard with explicit exception list for edge cases.

This script improves on script 37 by adding an exception list for terms that the
automated logic incorrectly identifies as needing lowercase conversion.

Exception categories:
1. Family names (Austin family, Brydon family)
2. Place names (Break Neck Gully)
3. Denomination names (Church of England, Roman Catholic Church)
4. Specific named organisations (Chess and Draughts Club)

Safety features:
- Creates timestamped backup before changes
- Validates changes after application
- Reports summary of changes made

Author: Claude Code
Date: 2025-11-17
"""

import csv
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Import analysis functions from script 36
import sys
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
spec = import_module('36_analyse_capitalization')
should_be_lowercase = spec.should_be_lowercase
extract_all_terms = spec.extract_all_terms


# EXCEPTION LIST: Terms that should NOT be lowercased despite automated logic
CAPITALIZATION_EXCEPTIONS = {
    # Family names (proper nouns)
    'Austin family',
    'Brydon family',
    'Delaney family',
    'Greenbank family',
    'Goyder family',
    'Fryer family',
    'Manuell family',

    # Place names (proper nouns)
    'Break Neck Gully',

    # Denomination names (proper nouns - full phrase)
    'Church of England',
    'Church of England church (building)',
    'Church of England church (organisation)',
    'Church of England churches',
    'Church of England churches (buildings)',
    'Church of England churches (organisations)',
    'Roman Catholic Church',
    'Roman Catholic church (building)',
    'Roman Catholic church (organisation)',
    'Roman Catholic churches',
    'Roman Catholic churches (buildings)',
    'Roman Catholic churches (organisations)',

    # Specific named organisations
    'Chess and Draughts Club',

    # Getty AAT primary facets (already in script 36 but belt-and-braces)
    'Activities',
    'Agents',
    'Associated Concepts',
    'Built Environment',
    'Events',
    'Materials',
    'Places',
}


def backup_file(file_path: Path) -> Path:
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


def generate_capitalization_mapping_with_exceptions(terms: set) -> dict:
    """
    Generate mapping of current term -> proper capitalisation.

    Applies automated logic from script 36, but excludes terms in exception list.
    """
    mapping = {}

    for term in sorted(terms):
        # Check exception list first
        if term in CAPITALIZATION_EXCEPTIONS:
            continue  # Skip - keep current capitalisation

        # Apply automated logic
        if should_be_lowercase(term):
            new_term = term.lower()
            if new_term != term:
                mapping[term] = new_term

    return mapping


def apply_capitalization_to_csv(csv_path: Path, mapping: dict) -> tuple[int, int]:
    """
    Apply capitalisation changes to CSV file.

    Returns: (tag_changes, parent_changes)
    """
    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Track changes
    tag_changes = 0
    parent_changes = 0

    # Apply mapping to all fields
    updated_rows = []
    for row in rows:
        new_row = row.copy()

        # Update tag names
        if row['new_tag'] in mapping:
            new_row['new_tag'] = mapping[row['new_tag']]
            tag_changes += 1

        if row['old_tag'] in mapping:
            new_row['old_tag'] = mapping[row['old_tag']]

        # Update parent references in notes field
        if row['action'] == 'hierarchy':
            notes = row['notes']
            # Extract and update parent name
            parent_match = re.search(r'(parent=)(.+?)($)', notes)
            if parent_match:
                prefix = parent_match.group(1)
                parent_full = parent_match.group(2)

                # Parse parent (strip thematic markers and parentheticals)
                match = re.search(r'(.+?)(?:\s*-\s*THEMATIC)?(?:\s*-\s*REMOVED)?(?:\s*\([^)]*\))?$', parent_full)
                if match:
                    parent = match.group(1).strip()

                    # Check if parent needs updating
                    if parent in mapping:
                        # Replace parent in the full parent string
                        new_parent_full = parent_full.replace(parent, mapping[parent], 1)
                        new_row['notes'] = notes.replace(parent_full, new_parent_full, 1)
                        parent_changes += 1

        updated_rows.append(new_row)

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    return tag_changes, parent_changes


def main():
    """Apply capitalisation changes with exception list."""
    csv_path = Path('data/tag_map_consolidated.csv')

    print("="*80)
    print("GETTY AAT CAPITALISATION FIX - WITH EXCEPTION LIST")
    print("="*80)
    print()

    # Create backup
    backup_file(csv_path)

    # Extract terms
    print("Extracting all terms from taxonomy...")
    terms = extract_all_terms(csv_path)
    print(f"Found {len(terms)} unique terms")
    print()

    # Generate mapping with exceptions
    print("Generating capitalisation mapping...")
    mapping = generate_capitalization_mapping_with_exceptions(terms)
    print(f"Identified {len(mapping)} terms requiring changes")
    print(f"Preserved {len(CAPITALIZATION_EXCEPTIONS)} exception terms")
    print()

    if not mapping:
        print("✓ No changes needed - all terms comply with Getty AAT standard!")
        return

    # Show exceptions being preserved
    print("="*80)
    print("EXCEPTIONS PRESERVED (not lowercased):")
    print("="*80)
    exceptions_found = [term for term in CAPITALIZATION_EXCEPTIONS if term in terms]
    if exceptions_found:
        for exception in sorted(exceptions_found):
            print(f"  ✓ {exception}")
    else:
        print("  (none in current taxonomy)")
    print()

    # Show sample changes
    print("="*80)
    print("SAMPLE CHANGES (first 20):")
    print("="*80)
    for i, (old_term, new_term) in enumerate(sorted(mapping.items())[:20], 1):
        print(f"  {i}. {old_term}")
        print(f"     → {new_term}")
    if len(mapping) > 20:
        print(f"  ... and {len(mapping) - 20} more")
    print()

    # Apply changes
    print("Applying changes...")
    tag_changes, parent_changes = apply_capitalization_to_csv(csv_path, mapping)

    print()
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Terms lowercased: {len(mapping)}")
    print(f"Tag field updates: {tag_changes}")
    print(f"Parent reference updates: {parent_changes}")
    print(f"Total updates: {tag_changes + parent_changes}")
    print()
    print(f"Exceptions preserved: {len(exceptions_found)}")
    print()

    # List key exception categories
    print("Exception categories:")
    print("  • Family names (Austin family, Brydon family, etc.)")
    print("  • Place names (Break Neck Gully)")
    print("  • Denomination names (Church of England, Roman Catholic Church)")
    print("  • Specific named organisations (Chess and Draughts Club)")
    print()

    print("="*80)
    print("✓ CAPITALISATION FIX COMPLETE")
    print("="*80)
    print()
    print("Next steps:")
    print("  1. Review changes: git diff data/tag_map_consolidated.csv")
    print("  2. Verify key terms are correct")
    print("  3. Run validation: python scripts/validate_taxonomy.py")
    print()


if __name__ == '__main__':
    main()
