#!/usr/bin/env python3
"""
Script 37: Apply Capitalization Changes for Getty AAT Compliance

Applies the capitalization changes identified by script 36_analyse_capitalization.py.

IMPORTANT: This script modifies data/tag_map_consolidated.csv
Make sure you have reviewed reports/capitalization_preview.txt and approved the changes.

Safety features:
- Updates ALL occurrences consistently (tag names AND parent references)
- Preserves CSV structure
- Creates backup before changes
- Validates changes after application

Usage:
    python scripts/37_apply_capitalization.py

The script will:
1. Re-generate the capitalization mapping (using same logic as script 36)
2. Show summary of changes
3. Ask for confirmation
4. Apply changes atomically
5. Validate results
"""

import csv
import re
import sys
from pathlib import Path
from collections import defaultdict

# Import the same functions from script 36
import sys
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module

# Load the analysis script's functions
spec = import_module('36_analyse_capitalization')
should_be_lowercase = spec.should_be_lowercase
extract_all_terms = spec.extract_all_terms
generate_capitalization_mapping = spec.generate_capitalization_mapping


def apply_capitalization_to_csv(csv_path: Path, mapping: dict) -> None:
    """
    Apply capitalization changes to CSV file.

    Updates ALL occurrences: both in tag names and in parent= references.
    """
    # Read all rows
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Apply mapping to all fields
    updated_rows = []
    for row in rows:
        new_row = row.copy()

        # Update tag names
        if row['new_tag'] in mapping:
            new_row['new_tag'] = mapping[row['new_tag']]

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

                # Parse parent (same logic as in script 23)
                match = re.search(r'(.+?)(?:\s*-\s*THEMATIC)?(?:\s*\([^)]*\))?$', parent_full)
                if match:
                    parent = match.group(1).strip()

                    # Check if parent needs updating
                    if parent in mapping:
                        # Replace parent in the full parent string
                        new_parent_full = parent_full.replace(parent, mapping[parent], 1)
                        new_row['notes'] = notes.replace(parent_full, new_parent_full, 1)

        updated_rows.append(new_row)

    # Write updated CSV
    backup_path = csv_path.parent / (csv_path.name + '.pre-capitalization-backup')
    csv_path.rename(backup_path)
    print(f"✓ Created backup: {backup_path}")

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print(f"✓ Applied changes to: {csv_path}")


def validate_changes(csv_path: Path, mapping: dict) -> bool:
    """Validate that changes were applied correctly."""
    print("\nValidating changes...")

    # Read CSV and check that mapped terms were updated in tag columns and parent references
    errors = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, 2):  # Start at 2 (header is 1)
            # Check new_tag field
            if row['new_tag'] in mapping:
                errors.append(
                    f"  - Line {row_num}: new_tag '{row['new_tag']}' should be "
                    f"'{mapping[row['new_tag']]}'"
                )

            # Check old_tag field
            if row['old_tag'] in mapping:
                errors.append(
                    f"  - Line {row_num}: old_tag '{row['old_tag']}' should be "
                    f"'{mapping[row['old_tag']]}'"
                )

            # Check parent references in hierarchy rows
            if row['action'] == 'hierarchy':
                parent_match = re.search(r'parent=(.+?)(?:\s*-\s*THEMATIC)?(?:\s*\([^)]*\))?$',
                                        row['notes'])
                if parent_match:
                    parent = parent_match.group(1).strip()
                    if parent in mapping:
                        errors.append(
                            f"  - Line {row_num}: parent '{parent}' should be "
                            f"'{mapping[parent]}'"
                        )

    if errors:
        print("❌ Validation FAILED:")
        for error in errors[:10]:  # Show first 10 errors
            print(error)
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
        return False
    else:
        print("✓ Validation PASSED: All changes applied correctly")
        return True


def main():
    csv_path = Path('data/tag_map_consolidated.csv')

    print("="*80)
    print("APPLY CAPITALIZATION CHANGES - Getty AAT Standard")
    print("="*80)
    print()

    # Extract terms and generate mapping
    print("Analysing current state...")
    terms = extract_all_terms(csv_path)
    mapping = generate_capitalization_mapping(terms)

    if not mapping:
        print("✓ No changes needed - all terms already comply with Getty AAT standard!")
        return

    print(f"Found {len(mapping)} terms requiring capitalization changes")
    print()

    # Show sample
    print("Sample changes (first 10):")
    print("-"*80)
    for i, (old_term, new_term) in enumerate(sorted(mapping.items())[:10], 1):
        print(f"  {i}. {old_term}")
        print(f"     → {new_term}")
    if len(mapping) > 10:
        print(f"  ... and {len(mapping) - 10} more")
    print()

    # Confirm
    print("="*80)
    print("IMPORTANT:")
    print("  - This will modify data/tag_map_consolidated.csv")
    print("  - A backup will be created automatically")
    print("  - You are on branch 'capitalization-getty-standard'")
    print("  - Changes can be rolled back with git")
    print("="*80)
    print()

    response = input("Apply these changes? [yes/no]: ").strip().lower()
    if response != 'yes':
        print("\n❌ Cancelled - no changes made")
        return

    print()
    print("Applying changes...")

    # Apply changes
    apply_capitalization_to_csv(csv_path, mapping)

    # Validate
    if validate_changes(csv_path, mapping):
        print()
        print("="*80)
        print("✓ SUCCESS!")
        print("="*80)
        print()
        print("Next steps:")
        print("  1. Regenerate visualizations: python scripts/23_visualise_poly_hierarchy.py")
        print("  2. Review changes: git diff data/tag_map_consolidated.csv")
        print("  3. Test the taxonomy")
        print("  4. If satisfied: git commit -am 'style: apply Getty AAT capitalization standard'")
        print("  5. If problems: git checkout data/tag_map_consolidated.csv")
        print()
    else:
        print()
        print("="*80)
        print("❌ VALIDATION FAILED")
        print("="*80)
        print()
        print("Rolling back changes...")
        backup_path = csv_path.parent / (csv_path.name + '.pre-capitalization-backup')
        if backup_path.exists():
            backup_path.rename(csv_path)
            print(f"✓ Restored from backup: {csv_path}")
        print()
        print("Please review the errors above and report the issue.")


if __name__ == '__main__':
    main()
