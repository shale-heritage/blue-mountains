#!/usr/bin/env python3
"""
Remove Unused Activity Singular Generics

This script removes orphaned singular generic leaf nodes from the Activities facet.
These are abstract categories that are unlikely to appear as generic mentions in
historical newspaper text:

- charitable and welfare activity
- communication activity
- economic activity
- recreation activity
- social behaviour

These tags have no children, no synonym mappings, and are not used elsewhere in
the taxonomy. They violate the principle that singular generics should only exist
when there are realistic scenarios for generic mentions in source text.
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
    print("REMOVE UNUSED ACTIVITY SINGULAR GENERICS")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)
    print(f"Initial entries: {initial_count}")

    # List of orphaned singular generics to remove
    unused_generics = [
        'charitable and welfare activity',
        'communication activity',
        'economic activity',
        'recreation activity',
        'social behaviour'
    ]

    print("\n" + "=" * 80)
    print("REMOVING ORPHANED SINGULAR GENERIC LEAF NODES")
    print("=" * 80)

    removed_count = 0
    for tag in unused_generics:
        mask = (df['old_tag'] == tag) & \
               (df['new_tag'] == tag) & \
               (df['action'] == 'hierarchy')

        removed = df[mask]
        if len(removed) > 0:
            parent = removed.iloc[0]['notes'].replace('parent=', '')
            df = df[~mask]
            removed_count += 1
            print(f"✓ Removed: '{tag}' (was under {parent})")
        else:
            print(f"⚠ Not found: '{tag}'")

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

    print(f"\nRemoved {removed_count} orphaned singular generic leaf nodes:")
    for tag in unused_generics:
        print(f"  • {tag}")

    print("\nRationale:")
    print("  These abstract activity categories are unlikely to appear as generic")
    print("  mentions in historical source text. Historical newspapers would specify")
    print("  the actual activity rather than using these broad generic terms.")
    print("\n  Singular generics should only exist when sources realistically mention")
    print("  the category without naming the specific instance.")

    print("\n✓ Unused activity generics removed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
