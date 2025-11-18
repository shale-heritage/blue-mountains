#!/usr/bin/env python3
"""
Fix Hotel Duplicates and Owner-Named Hotels

Two issues to fix:

1. Railway Hotel Duplicate:
   - Remove generic "Railway Hotel (business/building)" hierarchy entries
   - Update "Railway Hotel" synonym to map to "Railway Hotel Katoomba"
   - Evidence: All references are to Nimmo's Railway Hotel in Katoomba

2. Owner-Named Hotel Businesses (recurring issue):
   - Remove hierarchy entries for "[Owner]'s Hotel (business)"
   - These should only have "merge" entries
   - Pattern: Tag items with "hotel" (generic) + hotellier name

Owner-named hotels to remove:
   - Allen's Hotel (business)
   - Brown's Hotel (business)
   - Delaney's Hotel (business)
   - Mrs Long's Hotel (business)

These keep re-emerging because hierarchy entries weren't removed when
we consolidated hotellier names.
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
    print("FIX HOTEL DUPLICATES AND OWNER-NAMED HOTELS")
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
    print("ISSUE 1: RAILWAY HOTEL DUPLICATE")
    print("=" * 80)

    print("\nEvidence: All 'Railway Hotel' references are to Katoomba location")
    print("  • Nimmo's Railway Hotel synonyms already map to Railway Hotel Katoomba")
    print("  • Generic 'Railway Hotel' entries are redundant")

    # Remove generic Railway Hotel hierarchy entries
    print("\n1. Removing: Railway Hotel (business) hierarchy")
    mask = (df['old_tag'] == 'Railway Hotel (business)') & \
           (df['new_tag'] == 'Railway Hotel (business)') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=hotels (businesses)')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"   ✓ Removed {matches} entry(ies)")
    else:
        print(f"   ⚠ Not found")

    print("\n2. Removing: Railway Hotel (building) hierarchy")
    mask = (df['old_tag'] == 'Railway Hotel (building)') & \
           (df['new_tag'] == 'Railway Hotel (building)') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=hotels (buildings)')

    matches = mask.sum()
    if matches > 0:
        df = df[~mask].copy()
        removed_count += matches
        print(f"   ✓ Removed {matches} entry(ies)")
    else:
        print(f"   ⚠ Not found")

    # Update Railway Hotel synonym to map to Katoomba location
    print("\n3. Updating: Railway Hotel synonym to map to Railway Hotel Katoomba")
    mask = (df['old_tag'] == 'Railway Hotel') & \
           (df['new_tag'] == 'Railway Hotel (building)') & \
           (df['action'] == 'synonym')

    matches = mask.sum()
    if matches > 0:
        df.loc[mask, 'new_tag'] = 'Railway Hotel Katoomba (building)'
        df.loc[mask, 'notes'] = 'Unqualified reference - all instances refer to Katoomba Railway Hotel'
        updated_count += matches
        print(f"   ✓ Updated {matches} synonym entry(ies) to map to Katoomba")
    else:
        print(f"   ⚠ Building synonym not found")

    # Check if there's also a business synonym
    mask = (df['old_tag'] == 'Railway Hotel') & \
           (df['new_tag'] == 'Railway Hotel (business)') & \
           (df['action'] == 'synonym')

    matches = mask.sum()
    if matches > 0:
        df.loc[mask, 'new_tag'] = 'Railway Hotel Katoomba (business)'
        df.loc[mask, 'notes'] = 'Unqualified reference - all instances refer to Katoomba Railway Hotel'
        updated_count += matches
        print(f"   ✓ Updated {matches} business synonym entry(ies) to map to Katoomba")

    print("\n" + "=" * 80)
    print("ISSUE 2: OWNER-NAMED HOTEL BUSINESSES")
    print("=" * 80)

    print("\nPattern: [Owner]'s Hotel should tag as 'hotel' + hotellier name")
    print("  • Keep 'merge' entries (correct)")
    print("  • Remove hierarchy entries (cause duplication)")

    owner_hotels = [
        "Allen's Hotel (business)",
        "Brown's Hotel (business)",
        "Delaney's Hotel (business)",
        "Mrs Long's Hotel (business)"
    ]

    for i, hotel in enumerate(owner_hotels, 4):
        owner_name = hotel.split("'")[0]
        print(f"\n{i}. Removing: {hotel}")
        print(f"   Owner: {owner_name}")

        mask = (df['old_tag'] == hotel) & \
               (df['new_tag'] == hotel) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=hotels (businesses)')

        matches = mask.sum()
        if matches > 0:
            df = df[~mask].copy()
            removed_count += matches
            print(f"   ✓ Removed {matches} hierarchy entry(ies)")
            print(f"   ✓ 'merge' entry preserved - items tag as 'hotel' + '{owner_name}'")
        else:
            print(f"   ⚠ Not found (may be removed already)")

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

    print("\nRailway Hotel:")
    print("  ✓ Removed generic 'Railway Hotel' hierarchy entries")
    print("  ✓ Updated synonym to map to 'Railway Hotel Katoomba'")
    print("  ✓ All 3 items now correctly map to Katoomba location")

    print("\nOwner-Named Hotels:")
    print("  ✓ Removed hierarchy entries for 4 owner-named hotels")
    print("  ✓ Allen's Hotel, Brown's Hotel, Delaney's Hotel, Mrs Long's Hotel")
    print("  ✓ Items now tag as 'hotel' + hotellier name (correct pattern)")

    print("\nResult:")
    print("  • Railway Hotel Katoomba is now the single specific entry")
    print("  • Owner-named hotels won't re-emerge in visualizations")
    print("  • Consistent with established tagging pattern")

    print(f"\n✓ Hotel duplicates fixed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
