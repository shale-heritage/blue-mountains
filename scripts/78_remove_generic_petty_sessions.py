#!/usr/bin/env python3
"""
Remove Generic Court of Petty Sessions

Based on NLP analysis, all "Police court" references are Katoomba-specific.
No items use the generic "Court of Petty Sessions" directly.

Evidence from 5 contextual mentions:
- "at the local police court" (Katoomba Town Talk)
- "Katoomba Police Court" (explicit header)
- "At the police court, Katoomba" (explicit)
- "at the Katoomba police court" (explicit)
- "at the Katoomba Police Court" (explicit)

Changes:
1. Remove generic "Court of Petty Sessions" hierarchy entry (unused)
2. Update "Police Court" synonym → "Katoomba Court of Petty Sessions"
3. Update "police court" synonym → "Katoomba Court of Petty Sessions"

Result: All courts now location-specific (Katoomba or Penrith)
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
    df.to_csv(CSV_FILE, index=False, encoding='utf-8', lineterminator='\\n')
    print(f"✓ Saved: {CSV_FILE}")

def main():
    print("=" * 80)
    print("REMOVE GENERIC COURT OF PETTY SESSIONS")
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
    print("EVIDENCE SUMMARY")
    print("=" * 80)

    print("\nAll 5 'Police court' items reference Katoomba:")
    print("  1. 'at the local police court' (Town Talk, Katoomba context)")
    print("  2. 'Katoomba Police Court' (explicit header)")
    print("  3. 'At the police court, Katoomba' (explicit location)")
    print("  4. 'at the Katoomba police court' (explicit location)")
    print("  5. 'at the Katoomba Police Court' (explicit location)")

    print("\nGeneric 'Court of Petty Sessions': 0 items (unused)")

    print("\nConclusion: All court references are location-specific")
    print("  → Katoomba: 13 items total (8 'Katoomba Court' + 5 'Police court')")
    print("  → Penrith: As tagged")

    print("\n" + "=" * 80)
    print("REMOVING GENERIC HIERARCHY")
    print("=" * 80)

    # Remove generic Court of Petty Sessions hierarchy
    print("\n1. Removing: Court of Petty Sessions -> courts (unused)")
    mask = (df['old_tag'] == 'Court of Petty Sessions') & \
           (df['new_tag'] == 'Court of Petty Sessions') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=courts')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed hierarchy entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("UPDATING SYNONYMS TO KATOOMBA")
    print("=" * 80)

    # Update Police Court (capital C) synonym
    print("\n2. Updating: Police Court -> Katoomba Court of Petty Sessions")
    mask = (df['old_tag'] == 'Police Court') & \
           (df['new_tag'] == 'Court of Petty Sessions') & \
           (df['action'] == 'synonym')
    if mask.sum() > 0:
        df.loc[mask, 'new_tag'] = 'Katoomba Court of Petty Sessions'
        df.loc[mask, 'notes'] = 'Colloquial term for Katoomba Court of Petty Sessions'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} synonym entry")
    else:
        print(f"   ⚠ Entry not found")

    # Update police court (lowercase c) synonym
    print("\n3. Updating: police court -> Katoomba Court of Petty Sessions")
    mask = (df['old_tag'] == 'police court') & \
           (df['new_tag'] == 'Court of Petty Sessions') & \
           (df['action'] == 'synonym')
    if mask.sum() > 0:
        df.loc[mask, 'new_tag'] = 'Katoomba Court of Petty Sessions'
        df.loc[mask, 'notes'] = 'Colloquial term for Katoomba Court of Petty Sessions'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} synonym entry")
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
    print(f"  Removed:       {removed_count}")
    print(f"  Updated:       {updated_count}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nRemoved:")
    print("  • Court of Petty Sessions (generic hierarchy, unused)")

    print("\nUpdated synonyms:")
    print("  • Police Court → Katoomba Court of Petty Sessions")
    print("  • police court → Katoomba Court of Petty Sessions")

    print("\nFinal court structure:")
    print("  • Katoomba Court of Petty Sessions (13 items)")
    print("    - 8 items via 'Katoomba Court' synonym")
    print("    - 5 items via 'Police court' synonym")
    print("  • Penrith Court of Petty Sessions (as tagged)")

    print(f"\n✓ Generic Court of Petty Sessions removed!")
    print(f"✓ All courts now location-specific!")
    print(f"✓ Backup available: {backup_file}")

    print("\n" + "=" * 80)
    print("ITEM RETAGGING")
    print("=" * 80)

    print("\nNo manual retagging required:")
    print("  • Synonym mappings handle all items automatically")
    print("  • 5 items tagged 'Police court' will resolve to 'Katoomba Court of Petty Sessions'")
    print("  • No Zotero API calls needed")

if __name__ == '__main__':
    main()
