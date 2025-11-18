#!/usr/bin/env python3
"""
Add Courts of Petty Sessions Intermediate Node

For consistency with taxonomy patterns, group location-specific Courts of Petty
Sessions under an intermediate organizational node.

Current structure:
    courts
    ├── Katoomba Court of Petty Sessions
    ├── Penrith Court of Petty Sessions
    └── ...

Desired structure:
    courts
    ├── Courts of Petty Sessions (organizational node)
    │   ├── Katoomba Court of Petty Sessions
    │   └── Penrith Court of Petty Sessions
    └── ...

Changes:
1. Add "Courts of Petty Sessions" → courts (intermediate node)
2. Update "Katoomba Court of Petty Sessions" parent → Courts of Petty Sessions
3. Update "Penrith Court of Petty Sessions" parent → Courts of Petty Sessions

Result: Consistent organizational hierarchy matching pattern used elsewhere
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
    print("ADD COURTS OF PETTY SESSIONS INTERMEDIATE NODE")
    print("=" * 80)

    # Create backup
    backup_file = create_backup()

    # Load data
    print("\nLoading CSV...")
    df = load_csv()
    initial_count = len(df)

    # Track changes
    added_count = 0
    updated_count = 0

    print("\n" + "=" * 80)
    print("RATIONALE")
    print("=" * 80)

    print("\nConsistency with taxonomy patterns:")
    print("  • Intermediate nodes organize similar leaf nodes")
    print("  • Specific courts group under court type")
    print("  • Example: hotels → Hotels (businesses) → specific hotel businesses")
    print("\nCurrent: courts → Katoomba/Penrith Court of Petty Sessions (direct)")
    print("Desired: courts → Courts of Petty Sessions → Katoomba/Penrith (grouped)")

    print("\n" + "=" * 80)
    print("ADDING INTERMEDIATE NODE")
    print("=" * 80)

    # Check if intermediate node already exists
    print("\n1. Adding: Courts of Petty Sessions → courts")
    intermediate_exists = (
        (df['old_tag'] == 'Courts of Petty Sessions') &
        (df['new_tag'] == 'Courts of Petty Sessions') &
        (df['action'] == 'hierarchy') &
        (df['notes'] == 'parent=courts')
    ).any()

    if not intermediate_exists:
        new_entry = pd.DataFrame([{
            'old_tag': 'Courts of Petty Sessions',
            'new_tag': 'Courts of Petty Sessions',
            'action': 'hierarchy',
            'notes': 'parent=courts',
            'status': 'active'
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        added_count += 1
        print(f"   ✓ Added intermediate node")
    else:
        print(f"   ⚠ Already exists")

    print("\n" + "=" * 80)
    print("UPDATING PARENT RELATIONSHIPS")
    print("=" * 80)

    # Update Katoomba Court of Petty Sessions parent
    print("\n2. Updating: Katoomba Court of Petty Sessions")
    print("   From: parent=courts")
    print("   To:   parent=Courts of Petty Sessions")

    mask = (df['old_tag'] == 'Katoomba Court of Petty Sessions') & \
           (df['new_tag'] == 'Katoomba Court of Petty Sessions') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=courts')

    matches = mask.sum()
    print(f"   Found {matches} matching entries")

    if matches > 0:
        df.loc[mask, 'notes'] = 'parent=Courts of Petty Sessions'
        updated_count += matches
        print(f"   ✓ Updated parent relationship")
    else:
        print(f"   ⚠ Entry not found")

    # Update Penrith Court of Petty Sessions parent
    print("\n3. Updating: Penrith Court of Petty Sessions")
    print("   From: parent=courts")
    print("   To:   parent=Courts of Petty Sessions")

    mask = (df['old_tag'] == 'Penrith Court of Petty Sessions') & \
           (df['new_tag'] == 'Penrith Court of Petty Sessions') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=courts')

    matches = mask.sum()
    print(f"   Found {matches} matching entries")

    if matches > 0:
        df.loc[mask, 'notes'] = 'parent=Courts of Petty Sessions'
        updated_count += matches
        print(f"   ✓ Updated parent relationship")
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
    print(f"  Added:         {added_count}")
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

    print("\nAdded intermediate node:")
    print("  • Courts of Petty Sessions → courts")

    print("\nUpdated parent relationships:")
    print("  • Katoomba Court of Petty Sessions → Courts of Petty Sessions")
    print("  • Penrith Court of Petty Sessions → Courts of Petty Sessions")

    print("\nFinal court structure:")
    print("  courts")
    print("  ├── Courts of Petty Sessions (organizational node)")
    print("  │   ├── Katoomba Court of Petty Sessions (13 items)")
    print("  │   └── Penrith Court of Petty Sessions (as tagged)")
    print("  ├── Licensing Court")
    print("  ├── Supreme Court")
    print("  └── court (generic singular)")

    print(f"\n✓ Courts of Petty Sessions intermediate node added!")
    print(f"✓ Consistent organizational hierarchy!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
