#!/usr/bin/env python3
"""
Fix Capitalization and Punctuated Names in Agents

Multiple recurring issues to fix:

1. CAPITALIZATION FIXES:
   - 'Katoomba band' → 'Katoomba Band' (proper noun)
   - 'Police' → 'police' (generic)
   - 'Railway commission' → 'Railway Commission' (proper noun)
   - 'roman catholic church (organisation)' → 'Roman Catholic Church (organisation)'
   - 'roman catholic church lawson (organisation)' → 'Roman Catholic Church Lawson (organisation)'
   - 'roman catholic church (building)' → 'Roman Catholic Church (building)'
   - 'roman catholic church lawson (building)' → 'Roman Catholic Church Lawson (building)'
   - 'Archbishop' → 'archbishop' (generic occupation)
   - 'Coadjutor Archbishop' → 'coadjutor archbishop' (generic occupation)

2. PUNCTUATED NAMES (recurring issue):
   Remove punctuated duplicates, create synonym mappings:
   - 'Mr N. Delaney' → synonym of 'Mr N Delaney'
   - 'Mr P. G. Whittall' → synonym of 'Mr P G Whittall'

This keeps re-emerging because hierarchy entries aren't removed when
consolidating punctuated variants.
"""

import pandas as pd
import shutil
from datetime import datetime
from pathlib import Path

# File paths
DATA_DIR = Path(__file__).parent.parent / 'data'
CSV_FILE = DATA_DIR / 'tag_map_consolidated.csv'

def create_backup():
    """Create timestamped backup of the CSV file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = CSV_FILE.parent / f"{CSV_FILE.stem}.{timestamp}.bak"
    shutil.copy2(CSV_FILE, backup_file)
    print(f"✓ Backup created: {backup_file}")
    return backup_file

def load_csv():
    """Load the consolidated CSV file."""
    df = pd.read_csv(CSV_FILE, encoding='utf-8')
    print(f"✓ Loaded {len(df)} entries")
    return df

def save_csv(df):
    """Save the dataframe back to CSV with verification."""
    if len(df) == 0:
        raise ValueError("Cannot save empty dataframe!")

    temp_file = CSV_FILE.parent / f"{CSV_FILE.name}.tmp"
    df.to_csv(temp_file, index=False, encoding='utf-8', lineterminator='\n')

    temp_lines = sum(1 for _ in open(temp_file, 'r', encoding='utf-8'))
    print(f"✓ Wrote {temp_lines} lines to temp file")

    if temp_lines < 2:
        raise ValueError(f"Temp file only has {temp_lines} lines!")

    shutil.move(str(temp_file), str(CSV_FILE))
    print(f"✓ Saved: {CSV_FILE}")

def main():
    print("=" * 80)
    print("FIX CAPITALIZATION AND PUNCTUATED NAMES")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)

    # Track changes
    removed_count = 0
    updated_count = 0
    added_count = 0

    print("\n" + "=" * 80)
    print("1. CAPITALIZATION FIXES")
    print("=" * 80)

    # Define capitalization fixes
    cap_fixes = [
        ('Katoomba band', 'Katoomba Band', 'proper noun - band name'),
        ('Police', 'police', 'generic occupation'),
        ('Railway commission', 'Railway Commission', 'proper noun - government body'),
        ('roman catholic church (organisation)', 'Roman Catholic Church (organisation)', 'proper noun - church name'),
        ('roman catholic church (building)', 'Roman Catholic Church (building)', 'proper noun - church name'),
        ('roman catholic church lawson (organisation)', 'Roman Catholic Church Lawson (organisation)', 'proper noun - church name'),
        ('roman catholic church lawson (building)', 'Roman Catholic Church Lawson (building)', 'proper noun - church name'),
        ('Archbishop', 'archbishop', 'generic occupation'),
        ('Coadjutor Archbishop', 'coadjutor archbishop', 'generic occupation'),
    ]

    for old_cap, new_cap, reason in cap_fixes:
        print(f"\n  Fixing: {old_cap} → {new_cap}")
        print(f"  Reason: {reason}")

        # Update all occurrences (old_tag and new_tag)
        mask_old = df['old_tag'] == old_cap
        mask_new = df['new_tag'] == old_cap

        count_old = mask_old.sum()
        count_new = mask_new.sum()

        if count_old > 0:
            df.loc[mask_old, 'old_tag'] = new_cap
            updated_count += count_old

        if count_new > 0:
            df.loc[mask_new, 'new_tag'] = new_cap
            updated_count += count_new

        total_updated = count_old + count_new
        print(f"  ✓ Updated {total_updated} reference(s)")

    print("\n" + "=" * 80)
    print("2. PUNCTUATED NAMES (RECURRING ISSUE)")
    print("=" * 80)

    print("\nPattern: Minimal punctuation preferred (style guide)")
    print("  • 'Mr N. Delaney' → 'Mr N Delaney'")
    print("  • 'Mr P. G. Whittall' → 'Mr P G Whittall'")

    # Punctuated names to consolidate
    punctuated_names = [
        ('Mr N. Delaney', 'Mr N Delaney', 'parent=hotelliers'),
        ('Mr P. G. Whittall', 'Mr P G Whittall', 'parent=hotelliers'),
    ]

    for punctuated, minimal, parent_note in punctuated_names:
        print(f"\n  Processing: {punctuated}")

        # Remove punctuated hierarchy entry
        mask = (df['old_tag'] == punctuated) & \
               (df['new_tag'] == punctuated) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == parent_note)

        matches = mask.sum()
        if matches > 0:
            df = df[~mask].copy()
            removed_count += matches
            print(f"  ✓ Removed {matches} punctuated hierarchy entry(ies)")

        # Check if synonym already exists
        synonym_exists = (
            (df['old_tag'] == punctuated) &
            (df['new_tag'] == minimal) &
            (df['action'] == 'synonym')
        ).any()

        if not synonym_exists:
            # Add synonym mapping
            new_entry = pd.DataFrame([{
                'old_tag': punctuated,
                'new_tag': minimal,
                'action': 'synonym',
                'notes': 'Punctuated variant - use minimal punctuation per style guide',
                'status': 'active'
            }])
            df = pd.concat([df, new_entry], ignore_index=True)
            added_count += 1
            print(f"  ✓ Added synonym: {punctuated} → {minimal}")
        else:
            print(f"  ⚠ Synonym already exists")

    # Save changes
    print("\n" + "=" * 80)
    print("SAVING CHANGES")
    print("=" * 80)

    final_count = len(df)
    net_change = final_count - initial_count

    print(f"\nInitial entries: {initial_count}")
    print(f"Final entries:   {final_count}")
    print(f"Net change:      {net_change:+d}")
    print(f"  Removed:       {removed_count}")
    print(f"  Updated:       {updated_count}")
    print(f"  Added:         {added_count}")

    if final_count == 0:
        print("\n✗ ERROR: Dataframe is empty! Not saving.")
        return

    try:
        save_csv(df)
    except Exception as e:
        print(f"\n✗ ERROR saving CSV: {e}")
        return

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nCapitalization fixed:")
    print("  ✓ Katoomba Band (proper noun)")
    print("  ✓ police (generic)")
    print("  ✓ Railway Commission (proper noun)")
    print("  ✓ Roman Catholic Church variants (proper noun)")
    print("  ✓ archbishop, coadjutor archbishop (generic)")

    print("\nPunctuated names consolidated:")
    print("  ✓ Mr N Delaney (minimal punctuation)")
    print("  ✓ Mr P G Whittall (minimal punctuation)")
    print("  ✓ Punctuated variants now synonyms")

    print("\nWhy this won't re-emerge:")
    print("  • Hierarchy entries for punctuated names removed")
    print("  • Only synonym mappings remain")
    print("  • Script 22 won't regenerate removed hierarchies")

    print(f"\n✓ Capitalization and punctuated names fixed!")
    print(f"✓ Backup available: {backup_file}")

    print("\n" + "=" * 80)
    print("ITEM RETAGGING")
    print("=" * 80)

    print("\nNo manual retagging required:")
    print("  • Synonym mappings handle punctuated name variants")
    print("  • Capitalization changes apply to existing hierarchy")
    print("  • Items automatically resolve to correct forms")

if __name__ == '__main__':
    main()
