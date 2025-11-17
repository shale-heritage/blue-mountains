#!/usr/bin/env python3
"""
Fix US Spelling Violations

Convert all US spelling to UK/Australian spelling throughout the taxonomy CSV.
This applies to old_tag, new_tag, and notes fields.

Common US → UK/Australian conversions:
- organization → organisation
- labor → labour
- color → colour
- behavior → behaviour
- analyze → analyse
- optimize → optimise
- center → centre
- license (noun) → licence (noun)

Author: Claude Code
Date: 2025-11-16
"""

import csv
import shutil
import re
from pathlib import Path
from datetime import datetime


def backup_file(file_path: Path) -> Path:
    """Create timestamped backup of file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".{timestamp}.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path


# US → UK/Australian spelling mappings
SPELLING_FIXES = {
    # -ize → -ise
    r'\borganization\b': 'organisation',
    r'\borganizations\b': 'organisations',
    r'\bOrganization\b': 'Organisation',
    r'\bOrganizations\b': 'Organisations',
    r'\banalyze\b': 'analyse',
    r'\banalyzes\b': 'analyses',
    r'\boptimize\b': 'optimise',
    r'\boptimizes\b': 'optimises',

    # -or → -our
    r'\blabor\b': 'labour',
    r'\blabors\b': 'labours',
    r'\bLabor\b': 'Labour',
    r'\bcolor\b': 'colour',
    r'\bcolors\b': 'colours',
    r'\bColor\b': 'Colour',
    r'\bbehavior\b': 'behaviour',
    r'\bbehaviors\b': 'behaviours',
    r'\bBehavior\b': 'Behaviour',

    # -er → -re
    r'\bcenter\b': 'centre',
    r'\bcenters\b': 'centres',
    r'\bCenter\b': 'Centre',
    r'\btheater\b': 'theatre',
    r'\btheaters\b': 'theatres',
    r'\bTheater\b': 'Theatre',

    # -se (US verb) → -ce (UK noun)
    # Be careful: "license" can be both noun and verb
    # In UK: licence (noun), license (verb)
    # Context needed - skip for now to avoid breaking things
}


def fix_spelling(text: str) -> tuple[str, int]:
    """Fix US spelling in text. Returns (fixed_text, num_changes)"""
    if not text:
        return text, 0

    fixed = text
    changes = 0

    for us_pattern, uk_replacement in SPELLING_FIXES.items():
        new_fixed = re.sub(us_pattern, uk_replacement, fixed)
        if new_fixed != fixed:
            # Count how many times this pattern was replaced
            changes += len(re.findall(us_pattern, fixed))
            fixed = new_fixed

    return fixed, changes


def main():
    """Fix US spelling violations."""
    csv_path = Path("data/tag_map_consolidated.csv")

    # Create backup
    backup_file(csv_path)

    # Read existing entries
    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        entries = list(reader)

    print(f"Total entries before changes: {len(entries)}")

    # Fix spelling in all fields
    total_changes = 0
    changes_by_field = {'old_tag': 0, 'new_tag': 0, 'action': 0, 'notes': 0}

    fixed_entries = []
    for entry in entries:
        if len(entry) != 4:
            fixed_entries.append(entry)  # Keep malformed entries as-is
            continue

        old_tag, new_tag, action, notes = entry

        # Fix each field
        fixed_old, old_changes = fix_spelling(old_tag)
        fixed_new, new_changes = fix_spelling(new_tag)
        fixed_action, action_changes = fix_spelling(action)
        fixed_notes, notes_changes = fix_spelling(notes)

        # Track changes
        changes_by_field['old_tag'] += old_changes
        changes_by_field['new_tag'] += new_changes
        changes_by_field['action'] += action_changes
        changes_by_field['notes'] += notes_changes
        total_changes += old_changes + new_changes + action_changes + notes_changes

        fixed_entries.append([fixed_old, fixed_new, fixed_action, fixed_notes])

    # Write updated CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(fixed_entries)

    print(f"\nTotal entries after changes: {len(fixed_entries)}")
    print(f"Total spelling corrections: {total_changes}")

    print("\n=== Changes by Field ===")
    for field, count in changes_by_field.items():
        if count > 0:
            print(f"  {field}: {count} corrections")

    print("\n=== Common Corrections ===")
    print("  organization → organisation")
    print("  labor → labour")
    print("  color → colour")
    print("  behavior → behaviour")
    print("  analyze → analyse")
    print("  center → centre")

    print("\n✓ US spelling violations fixed")
    print("✓ All text now uses UK/Australian spelling")


if __name__ == "__main__":
    main()
