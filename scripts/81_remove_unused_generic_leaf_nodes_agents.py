#!/usr/bin/env python3
"""
Remove Unused Generic Leaf Nodes from Agents Facet

Removes 17 generic singular leaf nodes that are:
1. Not used in Zotero (0 items)
2. Not mentioned in consolidation decisions
3. Not serving any documented purpose

These are organizational placeholders that were created but never utilized.

KEPT (26 generics):
- 8 currently used in Zotero
- 18 mentioned in consolidation decisions (may have pending retagging)

REMOVED (17 unused):
- coach service, demographic group, ethnic group, financial institution,
  hospitality worker, hotellier, labour organisation, liquor merchant,
  maritime worker, medical professional, minstrel troupe, monastery or friary,
  outdoor recreation club, postmaster, progress committee,
  religious social movement, school teacher
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
    print("REMOVE UNUSED GENERIC LEAF NODES FROM AGENTS FACET")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)

    # Track changes
    removed_count = 0

    print("\n" + "=" * 80)
    print("RATIONALE")
    print("=" * 80)

    print("\nThese 17 generic leaf nodes are:")
    print("  • Not used in Zotero (0 items)")
    print("  • Not mentioned in consolidation decisions")
    print("  • Unnecessary organizational placeholders")
    print("\nRemoving them cleans up the taxonomy without loss of functionality.")

    print("\n" + "=" * 80)
    print("REMOVING UNUSED GENERIC LEAF NODES")
    print("=" * 80)

    # List of terms to remove with their parents
    terms_to_remove = [
        ('coach service', 'coach services'),
        ('demographic group', 'demographic groups'),
        ('ethnic group', 'ethnic groups'),
        ('financial institution', 'financial institutions'),
        ('hospitality worker', 'hospitality workers'),
        ('hotellier', 'hotelliers'),
        ('labour organisation', 'labour organisations'),
        ('liquor merchant', 'liquor merchants'),
        ('maritime worker', 'maritime workers'),
        ('medical professional', 'medical professionals'),
        ('minstrel troupe', 'minstrel troupes'),
        ('monastery or friary', 'monasteries and friaries'),
        ('outdoor recreation club', 'outdoor recreation clubs'),
        ('postmaster', 'postmasters'),
        ('progress committee', 'progress committees'),
        ('religious social movement', 'religious social movements'),
        ('school teacher', 'school teachers'),
    ]

    for i, (tag, parent) in enumerate(terms_to_remove, 1):
        print(f"\n{i}. Removing: {tag}")
        print(f"   Parent: {parent}")

        # Find and remove hierarchy entry
        # Note: Some parents have "(singular generic term)" in notes
        mask = (df['old_tag'] == tag) & \
               (df['new_tag'] == tag) & \
               (df['action'] == 'hierarchy')

        # Also check for entries where parent is explicitly stated
        mask = mask & (
            (df['notes'] == f'parent={parent}') |
            (df['notes'] == f'parent={parent} (singular generic term)')
        )

        matches = mask.sum()
        print(f"   Found: {matches} matching entries")

        if matches > 0:
            df = df[~mask].copy()
            removed_count += matches
            print(f"   ✓ Removed {matches} entry(ies)")
        else:
            print(f"   ⚠ Not found (may have been removed already)")

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

    print("\nRemoved 17 unused generic leaf nodes:")
    print("  • coach service")
    print("  • demographic group, ethnic group")
    print("  • financial institution")
    print("  • hospitality worker, hotellier")
    print("  • labour organisation, liquor merchant")
    print("  • maritime worker, medical professional")
    print("  • minstrel troupe, monastery or friary")
    print("  • outdoor recreation club")
    print("  • postmaster, progress committee")
    print("  • religious social movement, school teacher")

    print("\nKept 26 generic leaf nodes:")
    print("  • 8 currently used in Zotero")
    print("    - band, choir, coroner, court, publican, rifle club,")
    print("      sunday school, retailer or store")
    print("  • 18 mentioned in consolidation decisions")
    print("    - animal, athletic club, bicycle club, cattle trucking yard,")
    print("      constable, council, coursing club, cricket club, football club,")
    print("      legal official, lodge, miner, miners' dwelling, police officer,")
    print("      public official, rugby club, tennis club, unaffiliated lodge")

    print(f"\n✓ Removed {removed_count} unused generic leaf nodes!")
    print(f"✓ Agents facet cleaned up!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
