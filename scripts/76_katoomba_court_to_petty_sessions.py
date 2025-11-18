#!/usr/bin/env python3
"""
Convert Katoomba Court to Katoomba Court of Petty Sessions

Based on NLP analysis of Zotero items, "Katoomba Court" refers to the
Court of Petty Sessions held in Katoomba, not the courthouse building.

Evidence from 3 contextual mentions:
- Court sessions presided over by Police Magistrate and JPs
- Small Debts Court proceedings
- References to cases being heard at "Katoomba Court"

Changes:
1. Remove "Katoomba Court" hierarchy entries
2. Add "Katoomba Court of Petty Sessions" under courts
3. Make "Katoomba Court" a synonym of "Katoomba Court of Petty Sessions"

Note: This follows the same pattern as "Police Court" → "Court of Petty Sessions"
and "Penrith Police Court" → "Penrith Court of Petty Sessions"
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
    print("CONVERT KATOOMBA COURT TO KATOOMBA COURT OF PETTY SESSIONS")
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
    added_count = 0

    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)

    print("\nEvidence from Zotero context analysis (3 mentions):")
    print("  1. 'Katoomba Court. POLICE. Before Mr. J. K. Cleeve, P.M., and five JJ.P.'")
    print("     → P.M. = Police Magistrate, JJ.P. = Justices of the Peace")
    print("  2. 'Katoomba Court. SMALL DEBTS. Before Messrs... Js.P.'")
    print("     → Small Debts Court (part of Petty Sessions)")
    print("  3. 'No cases at Katoomba Court last Wednesday'")
    print("     → References to court proceedings/sessions")

    print("\nConclusion: 'Katoomba Court' = Court of Petty Sessions (institutional)")
    print("Pattern: Town name + 'Court' was common newspaper shorthand for local petty sessions")

    print("\n" + "=" * 80)
    print("REMOVING OLD ENTRIES")
    print("=" * 80)

    # Remove Katoomba Court hierarchy entries
    entries_to_remove = [
        ('Katoomba Court', 'Katoomba Court', 'hierarchy', 'parent=courts'),
        ('Katoomba Court', 'Katoomba Court', 'hierarchy', 'parent=court buildings'),
        ('Katoomba Court', 'Katoomba Court', 'hierarchy', 'parent=Court buildings'),
    ]

    for old_tag, new_tag, action, notes in entries_to_remove:
        mask = (df['old_tag'] == old_tag) & \
               (df['new_tag'] == new_tag) & \
               (df['action'] == action) & \
               (df['notes'] == notes)
        if mask.sum() > 0:
            df = df[~mask]
            removed_count += 1
            print(f"✓ Removed: {old_tag} ({notes})")

    print("\n" + "=" * 80)
    print("ADDING NEW ENTRIES")
    print("=" * 80)

    # Add Katoomba Court of Petty Sessions hierarchy
    new_entries = []

    # Check if hierarchy entry already exists
    hierarchy_exists = (
        (df['old_tag'] == 'Katoomba Court of Petty Sessions') &
        (df['new_tag'] == 'Katoomba Court of Petty Sessions') &
        (df['action'] == 'hierarchy') &
        (df['notes'] == 'parent=courts')
    ).any()

    if not hierarchy_exists:
        new_entries.append({
            'old_tag': 'Katoomba Court of Petty Sessions',
            'new_tag': 'Katoomba Court of Petty Sessions',
            'action': 'hierarchy',
            'notes': 'parent=courts',
            'status': 'active'
        })
        print("✓ Adding: Katoomba Court of Petty Sessions -> courts")

    # Add synonym mapping
    synonym_exists = (
        (df['old_tag'] == 'Katoomba Court') &
        (df['new_tag'] == 'Katoomba Court of Petty Sessions') &
        (df['action'] == 'synonym')
    ).any()

    if not synonym_exists:
        new_entries.append({
            'old_tag': 'Katoomba Court',
            'new_tag': 'Katoomba Court of Petty Sessions',
            'action': 'synonym',
            'notes': 'Newspaper shorthand for local Court of Petty Sessions',
            'status': 'active'
        })
        print("✓ Adding: Katoomba Court -> Katoomba Court of Petty Sessions (synonym)")

    if new_entries:
        new_df = pd.DataFrame(new_entries)
        df = pd.concat([df, new_df], ignore_index=True)
        added_count = len(new_entries)

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
    print(f"  Added:         {added_count}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nRemoved hierarchy entries:")
    print("  • Katoomba Court -> courts")
    print("  • Katoomba Court -> court buildings (2 variants)")

    print("\nAdded entries:")
    print("  • Katoomba Court of Petty Sessions -> courts (hierarchy)")
    print("  • Katoomba Court -> Katoomba Court of Petty Sessions (synonym)")

    print("\nResult:")
    print("  • 8 items tagged 'Katoomba Court' will map to 'Katoomba Court of Petty Sessions'")
    print("  • Consistent with 'Police Court' and 'Penrith Police Court' patterns")
    print("  • Institution (court sessions) not building (courthouse)")

    print(f"\n✓ Katoomba Court converted to Court of Petty Sessions!")
    print(f"✓ Backup available: {backup_file}")

    print("\n" + "=" * 80)
    print("ITEM RETAGGING")
    print("=" * 80)

    print("\nNo manual retagging required:")
    print("  • Synonym mapping handles all 8 items automatically")
    print("  • 'Katoomba Court' tag will resolve to 'Katoomba Court of Petty Sessions'")

if __name__ == '__main__':
    main()
