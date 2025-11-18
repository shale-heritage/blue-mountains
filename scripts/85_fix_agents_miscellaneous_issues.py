#!/usr/bin/env python3
"""
Fix Miscellaneous Agents Issues

Multiple issues to fix:

1. CAPITALIZATION:
   - orama boarding house → Orama Boarding House (both building and business)
   - mines school of arts → Mines School of Arts (both building and organisation)

2. FAMILY HOTEL DUPLICATE:
   - Remove: family hotel (business) → hotels (businesses)
   - Keep: family hotel (business) → family hotels (businesses) (correct generic location)

3. RETAILER OR STORE:
   - Remove: retailer or store hierarchy
   - Add: retailer or store → store (synonym)

4. TRANSPORT & LOGISTICS BUSINESS:
   - Unused (0 items in Zotero)
   - Remove singular generic

5. SCHOOLS CONSOLIDATION:
   - Remove: schools → educational institutions
   - Remove: schools → educational buildings
   - Add: schools → schools (organisations) (synonym)
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
    print("FIX MISCELLANEOUS AGENTS ISSUES")
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

    # Orama Boarding House
    print("\nFixing: orama boarding house → Orama Boarding House")

    cap_fixes = [
        ('orama boarding house (building)', 'Orama Boarding House (building)'),
        ('orama boarding house (business)', 'Orama Boarding House (business)'),
        ('mines school of arts (building)', 'Mines School of Arts (building)'),
        ('mines school of arts (organisation)', 'Mines School of Arts (organisation)'),
    ]

    for old_cap, new_cap in cap_fixes:
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

        total = count_old + count_new
        if total > 0:
            print(f"  ✓ {old_cap} → {new_cap} ({total} references)")

    print("\n" + "=" * 80)
    print("2. FAMILY HOTEL DUPLICATE")
    print("=" * 80)

    print("\nRemoving: family hotel (business) → hotels (businesses)")
    print("  (Keep generic under family hotels (businesses) only)")

    mask = (df['old_tag'] == 'family hotel (business)') & \
           (df['new_tag'] == 'family hotel (business)') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=hotels (businesses)')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"  ✓ Removed {matches} duplicate entry(ies)")
    else:
        print(f"  ⚠ Not found")

    print("\n" + "=" * 80)
    print("3. RETAILER OR STORE")
    print("=" * 80)

    print("\nConsolidating: retailer or store → store")

    # Remove retailer or store hierarchy
    mask = (df['old_tag'] == 'retailer or store') & \
           (df['new_tag'] == 'retailer or store') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=retailers and stores')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"  ✓ Removed hierarchy entry")

    # Check if synonym already exists
    synonym_exists = (
        (df['old_tag'] == 'retailer or store') &
        (df['new_tag'] == 'store') &
        (df['action'] == 'synonym')
    ).any()

    if not synonym_exists:
        new_entry = pd.DataFrame([{
            'old_tag': 'retailer or store',
            'new_tag': 'store',
            'action': 'synonym',
            'notes': 'Use simpler generic term',
            'status': 'active'
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        added_count += 1
        print(f"  ✓ Added synonym: retailer or store → store")
    else:
        print(f"  ⚠ Synonym already exists")

    print("\n" + "=" * 80)
    print("4. TRANSPORT & LOGISTICS BUSINESS")
    print("=" * 80)

    print("\nRemoving: transport & logistics business (unused)")
    print("  Evidence: 0 items in Zotero")

    mask = (df['old_tag'] == 'transport & logistics business') & \
           (df['new_tag'] == 'transport & logistics business') & \
           (df['action'] == 'hierarchy')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"  ✓ Removed {matches} unused singular generic")
    else:
        print(f"  ⚠ Not found")

    print("\n" + "=" * 80)
    print("5. SCHOOLS CONSOLIDATION")
    print("=" * 80)

    print("\nConsolidating: schools → schools (organisations)")

    # Remove schools → educational institutions
    mask1 = (df['old_tag'] == 'schools') & \
            (df['new_tag'] == 'schools') & \
            (df['action'] == 'hierarchy') & \
            (df['notes'] == 'parent=educational institutions')

    matches1 = mask1.sum()
    if matches1 > 0:
        df = df[~mask1].copy()
        removed_count += matches1
        print(f"  ✓ Removed schools → educational institutions")

    # Remove schools → educational buildings
    mask2 = (df['old_tag'] == 'schools') & \
            (df['new_tag'] == 'schools') & \
            (df['action'] == 'hierarchy') & \
            (df['notes'] == 'parent=educational buildings')

    matches2 = mask2.sum()
    if matches2 > 0:
        df = df[~mask2].copy()
        removed_count += matches2
        print(f"  ✓ Removed schools → educational buildings")

    # Check if synonym already exists
    synonym_exists = (
        (df['old_tag'] == 'schools') &
        (df['new_tag'] == 'schools (organisations)') &
        (df['action'] == 'synonym')
    ).any()

    if not synonym_exists:
        new_entry = pd.DataFrame([{
            'old_tag': 'schools',
            'new_tag': 'schools (organisations)',
            'action': 'synonym',
            'notes': 'Unqualified reference maps to organisational aspect',
            'status': 'active'
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        added_count += 1
        print(f"  ✓ Added synonym: schools → schools (organisations)")
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
    print("  ✓ Orama Boarding House (building & business)")
    print("  ✓ Mines School of Arts (building & organisation)")

    print("\nDuplicates removed:")
    print("  ✓ family hotel (business) - now only under family hotels (businesses)")
    print("  ✓ retailer or store - now synonym of store")
    print("  ✓ schools - now synonym of schools (organisations)")

    print("\nUnused generics removed:")
    print("  ✓ transport & logistics business (0 items)")

    print(f"\n✓ All miscellaneous agents issues fixed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
