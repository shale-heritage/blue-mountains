#!/usr/bin/env python3
"""
Final Activities Facet Cleanup

This script makes final refinements to the Activities facet:
1. Removes orphaned 'commercial activities' intermediate node (no children)
2. Removes unnecessary 'postal services' intermediate node
3. Moves 'postal service' to 'societal activities' (more appropriate context)
4. Renames 'military' to 'military activity' (follows singular generic pattern)

These changes improve consistency and remove unnecessary hierarchy depth.
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
    print("FINAL ACTIVITIES FACET CLEANUP")
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
    modified_entries = []

    print("\n" + "=" * 80)
    print("1. REMOVING ORPHANED 'COMMERCIAL ACTIVITIES' NODE")
    print("=" * 80)

    # Remove commercial activities (no children after liquor trade was moved)
    mask = (df['old_tag'] == 'commercial activities') & \
           (df['new_tag'] == 'commercial activities') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=Activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('commercial activities', 'Activities'))
        df = df[~mask]
        print(f"✓ Removed orphaned 'commercial activities' node")
    else:
        print(f"⚠ Entry not found")

    print("\n" + "=" * 80)
    print("2. REMOVING 'POSTAL SERVICES' INTERMEDIATE NODE")
    print("=" * 80)

    # Remove postal services intermediate node
    print("\n2a. Removing: postal services -> communication activities")
    mask = (df['old_tag'] == 'postal services') & \
           (df['new_tag'] == 'postal services') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=communication activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('postal services', 'communication activities'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Remove postal service -> postal services relationship
    print("\n2b. Removing: postal service -> postal services")
    mask = (df['old_tag'] == 'postal service') & \
           (df['new_tag'] == 'postal service') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=postal services')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('postal service', 'postal services'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("3. MOVING 'POSTAL SERVICE' TO 'SOCIETAL ACTIVITIES'")
    print("=" * 80)

    # Add postal service -> societal activities
    new_entry = pd.DataFrame([{
        'old_tag': 'postal service',
        'new_tag': 'postal service',
        'action': 'hierarchy',
        'notes': 'parent=societal activities',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('postal service', 'societal activities'))
    print(f"✓ Added: postal service -> societal activities")

    print("\n" + "=" * 80)
    print("4. RENAMING 'MILITARY' TO 'MILITARY ACTIVITY'")
    print("=" * 80)

    # Update synonym: military -> military activity
    print("\n4a. Updating synonym: military (capitalized) -> military activity")
    mask = (df['old_tag'] == 'military') & \
           (df['new_tag'] == 'military') & \
           (df['action'] == 'synonym')
    if mask.sum() > 0:
        df.loc[mask, 'new_tag'] = 'military activity'
        modified_entries.append(('synonym: military -> military activity'))
        print(f"   ✓ Updated synonym mapping")
    else:
        print(f"   ⚠ Synonym not found")

    # Remove old hierarchy: military -> military activities
    print("\n4b. Removing: military -> military activities")
    mask = (df['old_tag'] == 'military') & \
           (df['new_tag'] == 'military') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=military activities')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('military', 'military activities'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Add new hierarchy: military activity -> military activities
    print("\n4c. Adding: military activity -> military activities")
    new_entry = pd.DataFrame([{
        'old_tag': 'military activity',
        'new_tag': 'military activity',
        'action': 'hierarchy',
        'notes': 'parent=military activities (singular generic term)',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('military activity', 'military activities'))
    print(f"   ✓ Added 1 entry")

    # Update thematic relationship: military -> military activity
    print("\n4d. Updating thematic relationship: military -> military activity")
    mask = (df['old_tag'] == 'military') & \
           (df['new_tag'] == 'military') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=military organisations - THEMATIC')
    if mask.sum() > 0:
        df.loc[mask, 'new_tag'] = 'military activity'
        modified_entries.append(('thematic: military -> military activity'))
        print(f"   ✓ Updated thematic relationship")
    else:
        print(f"   ⚠ Thematic relationship not found")

    # Remove merge entries for military and military activity
    print("\n4e. Cleaning up old merge entries")
    mask = ((df['old_tag'] == 'military') | (df['old_tag'] == 'military activity')) & \
           (df['action'] == 'merge')
    removed_merge = df[mask]
    if len(removed_merge) > 0:
        df = df[~mask]
        print(f"   ✓ Removed {len(removed_merge)} obsolete merge entries")
    else:
        print(f"   ⚠ No merge entries found")

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
    print(f"  Modified:      {len(modified_entries)}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nOrphaned nodes removed:")
    print("  • commercial activities (no children)")

    print("\nUnnecessary intermediate nodes removed:")
    print("  • postal services (only had one child)")

    print("\nRestructured:")
    print("  • postal service moved from communication activities to societal activities")

    print("\nRenamed for consistency:")
    print("  • military → military activity (follows singular generic pattern)")

    print("\n✓ Final Activities facet cleanup complete!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
