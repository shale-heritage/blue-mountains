#!/usr/bin/env python3
"""
Fix Hospitality Businesses Disambiguation

This script fixes inconsistent disambiguation in the hospitality businesses section
of the Agents facet. Within the Agents facet, all hospitality venues should use
(business) qualifiers to distinguish them from their building counterparts in the
Built Environment facet.

Issues fixed:
1. Remove 'hotels' from hospitality businesses (keep in Built Environment only)
2. Remove 'boarding houses' from hospitality businesses (keep in Built Environment only)
3. Ensure all hotel and boarding house children in Agents facet have (business) qualifiers

Following the principle: penultimate nodes and leaf nodes in Agents facet should
have (business) disambiguation for dual-nature entities.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path

# File paths
DATA_DIR = Path(__file__).parent.parent / 'data'
CSV_FILE = DATA_DIR / 'tag_map_consolidated.csv'

def create_backup():
    """Create timestamped backup of the CSV file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = CSV_FILE.parent / f"{CSV_FILE.stem}.{timestamp}.bak"
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Backup created: {backup_file}")
    return backup_file

def load_csv():
    """Load the consolidated CSV file."""
    return pd.read_csv(CSV_FILE, encoding='utf-8')

def save_csv(df):
    """Save the dataframe back to CSV."""
    df.to_csv(CSV_FILE, index=False, encoding='utf-8', lineterminator='\n')
    print(f"✓ Saved: {CSV_FILE}")

def main():
    print("=" * 80)
    print("FIX HOSPITALITY BUSINESSES DISAMBIGUATION")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)
    print(f"Initial entries: {initial_count}")

    # Track changes
    removed_count = 0
    updated_count = 0

    print("\n" + "=" * 80)
    print("1. REMOVING NON-DISAMBIGUATED PARENTS FROM AGENTS FACET")
    print("=" * 80)

    # Remove hotels -> hospitality businesses (keep in Built Environment)
    print("\n1a. Removing: hotels -> hospitality businesses")
    mask = (df['old_tag'] == 'hotels') & \
           (df['new_tag'] == 'hotels') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=hospitality businesses')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Remove boarding houses -> hospitality businesses (keep in Built Environment)
    print("\n1b. Removing: boarding houses -> hospitality businesses")
    mask = (df['old_tag'] == 'boarding houses') & \
           (df['new_tag'] == 'boarding houses') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=hospitality businesses')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("2. UPDATING CHILDREN TO USE (BUSINESS) QUALIFIER")
    print("=" * 80)

    # Update all hotel children with parent=hotels to parent=hotels (businesses)
    # and add (business) qualifier to the tag name
    print("\n2a. Updating hotel entries to have (business) qualifier")

    # Get all hotels with parent=hotels
    mask = (df['action'] == 'hierarchy') & (df['notes'] == 'parent=hotels')
    hotels_to_update = df[mask].copy()

    hotel_update_count = 0
    for idx, row in hotels_to_update.iterrows():
        hotel_name = row['old_tag']

        # Check if this hotel already has a (business) qualified version
        business_version = f"{hotel_name} (business)"

        # Check if business version already exists with parent=hotels (businesses)
        business_exists = (
            (df['old_tag'] == business_version) &
            (df['new_tag'] == business_version) &
            (df['action'] == 'hierarchy') &
            (df['notes'] == 'parent=hotels (businesses)')
        ).any()

        if business_exists:
            # Business version exists, remove the non-qualified one with parent=hotels
            df = df.drop(idx)
            removed_count += 1
            hotel_update_count += 1
        else:
            # No business version exists, update this one
            df.at[idx, 'old_tag'] = business_version
            df.at[idx, 'new_tag'] = business_version
            df.at[idx, 'notes'] = 'parent=hotels (businesses)'
            updated_count += 1
            hotel_update_count += 1

    print(f"   ✓ Updated {hotel_update_count} hotel entries")

    # Update all boarding house children similarly
    print("\n2b. Updating boarding house entries to have (business) qualifier")

    mask = (df['action'] == 'hierarchy') & (df['notes'] == 'parent=boarding houses')
    boarding_to_update = df[mask].copy()

    boarding_update_count = 0
    for idx, row in boarding_to_update.iterrows():
        boarding_name = row['old_tag']
        business_version = f"{boarding_name} (business)"

        # Check if business version already exists
        business_exists = (
            (df['old_tag'] == business_version) &
            (df['new_tag'] == business_version) &
            (df['action'] == 'hierarchy') &
            (df['notes'] == 'parent=boarding houses (businesses)')
        ).any()

        if business_exists:
            # Remove the non-qualified one
            df = df.drop(idx)
            removed_count += 1
            boarding_update_count += 1
        else:
            # Update this one
            df.at[idx, 'old_tag'] = business_version
            df.at[idx, 'new_tag'] = business_version
            df.at[idx, 'notes'] = 'parent=boarding houses (businesses)'
            updated_count += 1
            boarding_update_count += 1

    print(f"   ✓ Updated {boarding_update_count} boarding house entries")

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

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nRemoved from Agents facet:")
    print("  • hotels -> hospitality businesses")
    print("  • boarding houses -> hospitality businesses")

    print("\nUpdated to use (business) qualifiers:")
    print(f"  • {hotel_update_count} hotel entries")
    print(f"  • {boarding_update_count} boarding house entries")

    print("\nResult:")
    print("  • Agents facet: Only 'hotels (businesses)' and 'boarding houses (businesses)'")
    print("  • Built Environment facet: Retains 'hotels' and 'boarding houses'")
    print("  • All children in Agents facet now have (business) qualifiers")
    print("  • Consistent disambiguation throughout hospitality businesses")

    print("\n✓ Hospitality disambiguation fixed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
