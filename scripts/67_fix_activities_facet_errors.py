#!/usr/bin/env python3
"""
Fix Activities Facet Errors

This script corrects major structural errors in the Activities facet:
1. Removes duplicate hierarchies (liquor trade, military activities, regulatory processes)
2. Removes misplaced buildings/facilities (coal mines, shale mines)
3. Removes misplaced materials (Coal)
4. Removes misplaced agents (police organizations and officers)
5. Creates proper law enforcement agencies intermediate node in Agents facet

Errors found:
- Liquor trade appears under both commercial activities and economic activities
- Military activities appears at top level and under societal activities
- Regulatory processes appears at top level and under societal activities
- Coal mines/shale mines facilities appear under Activities instead of Built Environment
- Coal material appears under Activities instead of Materials
- Police organizations and officers appear under Activities via law enforcement cascade
- law enforcement incorrectly appears under government bodies and occupations

All corrections preserve synonym mappings and thematic relationships.
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
    print("FIX ACTIVITIES FACET ERRORS")
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
    added_entries = []

    print("\n" + "=" * 80)
    print("REMOVING DUPLICATE HIERARCHIES")
    print("=" * 80)

    # 1. Remove liquor trade from commercial activities (keep under economic activities)
    print("\n1. Removing: liquor trade -> commercial activities")
    mask = (df['old_tag'] == 'liquor trade') & \
           (df['new_tag'] == 'liquor trade') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=commercial activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('liquor trade', 'commercial activities', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 2. Remove military activities from top-level Activities (keep under societal activities)
    print("\n2. Removing: military activities -> Activities")
    mask = (df['old_tag'] == 'military activities') & \
           (df['new_tag'] == 'military activities') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=Activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('military activities', 'Activities', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 3. Remove regulatory processes from top-level Activities (keep under societal activities)
    print("\n3. Removing: regulatory processes -> Activities")
    mask = (df['old_tag'] == 'regulatory processes') & \
           (df['new_tag'] == 'regulatory processes') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=Activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('regulatory processes', 'Activities', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("REMOVING MISPLACED MATERIALS")
    print("=" * 80)

    # 4. Remove Coal from coal mining (material already in Materials facet)
    print("\n4. Removing: Coal -> coal mining")
    mask = (df['old_tag'] == 'Coal') & \
           (df['new_tag'] == 'Coal') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=coal mining')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('Coal', 'coal mining', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("REMOVING MISPLACED FACILITIES")
    print("=" * 80)

    # 5. Remove coal mines from coal mining activity (facilities already in Built Environment)
    print("\n5. Removing: coal mines -> coal mining")
    mask = (df['old_tag'] == 'coal mines') & \
           (df['new_tag'] == 'coal mines') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=coal mining')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('coal mines', 'coal mining', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 6. Remove shale mines from shale mining activity (facilities already in Built Environment)
    print("\n6. Removing: shale mines -> shale mining")
    mask = (df['old_tag'] == 'shale mines') & \
           (df['new_tag'] == 'shale mines') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=shale mining')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('shale mines', 'shale mining', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("REMOVING MISPLACED AGENTS (LAW ENFORCEMENT)")
    print("=" * 80)

    # 7. Remove law enforcement from government bodies
    print("\n7. Removing: law enforcement -> government bodies")
    mask = (df['old_tag'] == 'law enforcement') & \
           (df['new_tag'] == 'law enforcement') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=government bodies')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('law enforcement', 'government bodies', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 8. Remove law enforcement from occupations
    print("\n8. Removing: law enforcement -> occupations")
    mask = (df['old_tag'] == 'law enforcement') & \
           (df['new_tag'] == 'law enforcement') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=occupations')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('law enforcement', 'occupations', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 9. Remove New South Wales Police -> law enforcement
    print("\n9. Removing: New South Wales Police -> law enforcement")
    mask = (df['old_tag'] == 'New South Wales Police') & \
           (df['new_tag'] == 'New South Wales Police') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=law enforcement')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('New South Wales Police', 'law enforcement', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 10. Remove Police -> law enforcement
    print("\n10. Removing: Police -> law enforcement")
    mask = (df['old_tag'] == 'Police') & \
           (df['new_tag'] == 'Police') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=law enforcement')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('Police', 'law enforcement', removed.iloc[0]))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # 11. Remove all officer -> Police relationships
    print("\n11. Removing: [officers] -> Police")
    officers = [
        'Constable John Hamilton',
        'Constable O\'Reilly',
        'Constable Orr',
        'Constable White',
        'Senior-Constable Illingworth',
        'Senior-Constable Thorncroft',
        'Sergeant Thorndyke'
    ]
    officer_count = 0
    for officer in officers:
        mask = (df['old_tag'] == officer) & \
               (df['new_tag'] == officer) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=Police')
        removed = df[mask]
        if len(removed) > 0:
            removed_entries.append((officer, 'Police', removed.iloc[0]))
            df = df[~mask]
            officer_count += 1
    print(f"   ✓ Removed {officer_count} officer entries")

    print("\n" + "=" * 80)
    print("ADDING LAW ENFORCEMENT AGENCIES NODE")
    print("=" * 80)

    # 12. Add law enforcement agencies intermediate node
    print("\n12. Adding: law enforcement agencies -> government bodies")
    new_entry = pd.DataFrame([{
        'old_tag': 'law enforcement agencies',
        'new_tag': 'law enforcement agencies',
        'action': 'hierarchy',
        'notes': 'parent=government bodies',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('law enforcement agencies', 'government bodies'))
    print(f"   ✓ Added 1 entry")

    # 13. Add New South Wales Police -> law enforcement agencies
    print("\n13. Adding: New South Wales Police -> law enforcement agencies")
    new_entry = pd.DataFrame([{
        'old_tag': 'New South Wales Police',
        'new_tag': 'New South Wales Police',
        'action': 'hierarchy',
        'notes': 'parent=law enforcement agencies',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('New South Wales Police', 'law enforcement agencies'))
    print(f"   ✓ Added 1 entry")

    # 14. Add Police -> law enforcement agencies
    print("\n14. Adding: Police -> law enforcement agencies")
    new_entry = pd.DataFrame([{
        'old_tag': 'Police',
        'new_tag': 'Police',
        'action': 'hierarchy',
        'notes': 'parent=law enforcement agencies',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('Police', 'law enforcement agencies'))
    print(f"   ✓ Added 1 entry")

    # Save changes
    print("\n" + "=" * 80)
    print("SAVING CHANGES")
    print("=" * 80)

    final_count = len(df)
    net_change = final_count - initial_count

    print(f"\nInitial entries: {initial_count}")
    print(f"Final entries:   {final_count}")
    print(f"Net change:      {net_change:+d}")
    print(f"  Removed:       {len(removed_entries)}")
    print(f"  Added:         {len(added_entries)}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nRemoved duplicate hierarchies:")
    print("  • liquor trade from commercial activities")
    print("  • military activities from top-level Activities")
    print("  • regulatory processes from top-level Activities")

    print("\nRemoved misplaced materials:")
    print("  • Coal from coal mining activity")

    print("\nRemoved misplaced facilities:")
    print("  • coal mines from coal mining activity")
    print("  • shale mines from shale mining activity")

    print("\nRemoved misplaced agents:")
    print("  • law enforcement from government bodies")
    print("  • law enforcement from occupations")
    print("  • New South Wales Police from law enforcement")
    print("  • Police from law enforcement")
    print(f"  • {officer_count} officers from Police")

    print("\nAdded proper structure:")
    print("  • law enforcement agencies under government bodies")
    print("  • New South Wales Police under law enforcement agencies")
    print("  • Police under law enforcement agencies")

    print("\n✓ Activities facet errors corrected!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
