#!/usr/bin/env python3
"""
Fix Railway Commission Duplicate

Issue: Two hierarchy entries exist:
- Railway Commission (correct - Title Case proper noun)
- railway commission (incorrect - lowercase duplicate)

And a backwards synonym:
- Railway Commission → railway commission (should be reversed)

Fix:
1. Remove lowercase "railway commission" hierarchy entry
2. Reverse synonym to: railway commission → Railway Commission
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
    print("FIX RAILWAY COMMISSION DUPLICATE")
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

    print("\n" + "=" * 80)
    print("ISSUE")
    print("=" * 80)

    print("\nCurrent state:")
    print("  • Railway Commission → Railway Commission (hierarchy) ✓ Correct")
    print("  • railway commission → railway commission (hierarchy) ✗ Duplicate")
    print("  • Railway Commission → railway commission (synonym) ✗ Backwards")

    print("\nDesired state:")
    print("  • Railway Commission → Railway Commission (hierarchy) ✓ Keep")
    print("  • railway commission → Railway Commission (synonym) ✓ Correct direction")

    print("\n" + "=" * 80)
    print("FIXING")
    print("=" * 80)

    # 1. Remove lowercase hierarchy entry
    print("\n1. Removing: railway commission hierarchy entry")
    mask = (df['old_tag'] == 'railway commission') & \
           (df['new_tag'] == 'railway commission') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=railway authorities')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"   ✓ Removed {matches} entry(ies)")
    else:
        print(f"   ⚠ Not found")

    # 2. Fix the backwards synonym
    print("\n2. Fixing: Railway Commission synonym (reverse direction)")
    mask = (df['old_tag'] == 'Railway Commission') & \
           (df['new_tag'] == 'railway commission') & \
           (df['action'] == 'synonym')

    matches = mask.sum()
    if matches > 0:
        # Swap old_tag and new_tag
        df.loc[mask, 'old_tag'] = 'railway commission'
        df.loc[mask, 'new_tag'] = 'Railway Commission'
        df.loc[mask, 'notes'] = 'Lowercase variant - use Title Case for proper noun'
        updated_count += matches
        print(f"   ✓ Reversed {matches} synonym entry(ies)")
        print(f"   Now: railway commission → Railway Commission")
    else:
        print(f"   ⚠ Not found")

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

    print("\nFixed Railway Commission:")
    print("  ✓ Removed lowercase duplicate hierarchy entry")
    print("  ✓ Reversed synonym to correct direction")
    print("  ✓ Railway Commission (Title Case) is now the canonical form")

    print(f"\n✓ Railway Commission duplicate fixed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
