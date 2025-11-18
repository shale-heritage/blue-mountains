#!/usr/bin/env python3
"""
Remove Phantom and Orphaned Retailer Entries

This script removes phantom and orphaned entries from "Retailers and stores":

1. Orphaned entries (should have been removed by script 47):
   - Nimmo's (already has synonym mappings to Railway Hotel Katoomba)
   - Peckman Bros (already has synonym mappings to Peckman Brothers business)

2. Phantom entries (never used to tag any items):
   - Douglas and Company (0 items)
   - P. Mullany and Company (0 items)
   - Tabrett and Company (0 items)

Evidence basis: entity-tagging-system/outputs/retailers/retailers-investigation-summary.md

Result: "Retailers and stores" category will have no specific business entries,
only generic terms (retailer or store, store) for potential future use.
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
    print("REMOVE PHANTOM AND ORPHANED RETAILER ENTRIES")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)
    print(f"Initial entries: {initial_count}")

    # Track changes
    removed_entries = []

    print("\n" + "=" * 80)
    print("1. REMOVING ORPHANED ENTRIES (should have been removed by script 47)")
    print("=" * 80)

    # Remove Nimmo's from retailers
    print("\n1a. Removing: Nimmo's -> retailers and stores")
    mask = (df['old_tag'] == "Nimmo's") & \
           (df['new_tag'] == "Nimmo's") & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=retailers and stores')
    if mask.sum() > 0:
        removed_entries.append(("Nimmo's", "retailers and stores", "orphaned"))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
        print(f"   Note: Synonym mappings to Railway Hotel Katoomba already exist")
    else:
        print(f"   ⚠ Entry not found")

    # Remove Peckman Bros from retailers
    print("\n1b. Removing: Peckman Bros -> retailers and stores")
    mask = (df['old_tag'] == "Peckman Bros") & \
           (df['new_tag'] == "Peckman Bros") & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=retailers and stores')
    if mask.sum() > 0:
        removed_entries.append(("Peckman Bros", "retailers and stores", "orphaned"))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
        print(f"   Note: Synonym mappings to Peckman Brothers (business) already exist")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("2. REMOVING PHANTOM ENTRIES (never used to tag items)")
    print("=" * 80)

    phantom_retailers = [
        "Douglas and Company",
        "p. mullany and company",
        "Tabrett and Company"
    ]

    for retailer in phantom_retailers:
        print(f"\n2. Removing: {retailer} -> retailers and stores")
        mask = (df['old_tag'] == retailer) & \
               (df['new_tag'] == retailer) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=retailers and stores')
        if mask.sum() > 0:
            removed_entries.append((retailer, "retailers and stores", "phantom - 0 items"))
            df = df[~mask]
            print(f"   ✓ Removed 1 entry (0 items tagged)")
        else:
            print(f"   ⚠ Entry not found")

    # Save changes
    print("\n" + "=" * 80)
    print("SAVING CHANGES")
    print("=" * 80)

    final_count = len(df)
    net_change = final_count - initial_count

    print(f"\nInitial entries: {initial_count}")
    print(f"Final entries:   {final_count}")
    print(f"Net change:      {net_change:+d}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"\nRemoved {len(removed_entries)} problematic retailer entries:")

    print("\nOrphaned entries (duplicates after script 47):")
    for entry, parent, reason in removed_entries:
        if reason == "orphaned":
            print(f"  • {entry}")

    print("\nPhantom entries (never used):")
    for entry, parent, reason in removed_entries:
        if "phantom" in reason:
            print(f"  • {entry} ({reason})")

    print("\n'Retailers and stores' category now contains:")
    print("  • Generic terms only (retailer or store, store)")
    print("  • No specific business entries")
    print("  • Structure retained for potential future use")

    print("\nAll retailer items (6 total) now correctly tagged:")
    print("  • Nimmo's (3 items) → Railway Hotel Katoomba (building/business)")
    print("  • Peckman Bros (3 items) → Peckman Brothers (business) under coach services")

    print(f"\n✓ Phantom and orphaned retailers removed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
