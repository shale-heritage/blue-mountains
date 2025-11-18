#!/usr/bin/env python3
"""
Fix Agents Facet Capitalisation and Duplicates

This script corrects several issues in cultural & recreational organisations
and educational institutions:

1. Chess and draughts club: Consolidate to lowercase (generic reference)
   - Remove capital version hierarchy entry
   - Keep synonym mapping and lowercase hierarchy

2. Schools of arts: Remove non-qualified duplicate
   - Remove "schools of arts" hierarchy entries (without qualifier)
   - Keep only "schools of arts (organisations)" under cultural societies

3. Proper names capitalisation:
   - Congregational Church Choir
   - Nepean Football Club
   - Mountaineer Lodge

4. Schools consolidation: Remove non-qualified duplicates
   - Remove "schools" parent node entries
   - Keep only "schools (organisations)" entries with qualifiers
   - Synonym mappings already handle unqualified variants

Evidence: Manual review of visualizations/hierarchy_trees/primary_agents.txt
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
    print("FIX AGENTS CAPITALISATION AND DUPLICATES")
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
    print("1. CONSOLIDATE CHESS AND DRAUGHTS CLUB TO LOWERCASE")
    print("=" * 80)

    # Remove capital version hierarchy (keep synonym mapping and lowercase hierarchy)
    print("\n1. Removing: Chess and Draughts Club -> cultural societies")
    mask = (df['old_tag'] == 'Chess and Draughts Club') & \
           (df['new_tag'] == 'Chess and Draughts Club') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=cultural societies')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry (keeping lowercase version)")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("2. REMOVE SCHOOLS OF ARTS DUPLICATE (without qualifier)")
    print("=" * 80)

    # Remove schools of arts from cultural societies (keep qualified version)
    print("\n2a. Removing: schools of arts -> cultural societies")
    mask = (df['old_tag'] == 'schools of arts') & \
           (df['new_tag'] == 'schools of arts') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=cultural societies')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Remove schools of arts from halls (keep qualified version)
    print("\n2b. Removing: schools of arts -> halls")
    mask = (df['old_tag'] == 'schools of arts') & \
           (df['new_tag'] == 'schools of arts') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=halls')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("3. CAPITALIZE PROPER NAMES")
    print("=" * 80)

    # Congregational Church Choir
    print("\n3a. Capitalizing: congregational church choir")
    mask = (df['old_tag'] == 'congregational church choir')
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Congregational Church Choir'
        df.loc[mask, 'new_tag'] = 'Congregational Church Choir'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    # Nepean Football Club
    print("\n3b. Capitalizing: nepean football club")
    mask = (df['old_tag'] == 'nepean football club')
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Nepean Football Club'
        df.loc[mask, 'new_tag'] = 'Nepean Football Club'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    # Mountaineer Lodge
    print("\n3c. Capitalizing: mountaineer lodge")
    mask = (df['old_tag'] == 'mountaineer lodge')
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Mountaineer Lodge'
        df.loc[mask, 'new_tag'] = 'Mountaineer Lodge'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("4. CONSOLIDATE SCHOOLS (remove non-qualified duplicates)")
    print("=" * 80)

    # Remove non-qualified school hierarchy entries
    schools_to_remove = [
        ('Katoomba Public School', 'parent=schools'),
        ('Katoomba Superior Public School', 'parent=schools'),
        ('Megalong Valley School', 'parent=schools'),
        ('Mount Victoria School', 'parent=schools'),
        ('school', 'parent=schools')
    ]

    for school, parent_note in schools_to_remove:
        print(f"\n4. Removing: {school} -> schools")
        mask = (df['old_tag'] == school) & \
               (df['new_tag'] == school) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == parent_note)
        if mask.sum() > 0:
            df = df[~mask]
            removed_count += 1
            print(f"   ✓ Removed 1 entry (keeping qualified version with (organisation))")
        else:
            print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("5. REMOVE NON-QUALIFIED SCHOOLS OF ARTS ENTRIES")
    print("=" * 80)

    # Remove non-qualified schools of arts entries
    schools_of_arts_to_remove = [
        ('Katoomba School of Arts', 'parent=schools of arts'),
        ('school of arts', 'parent=schools of arts')
    ]

    for school, parent_note in schools_of_arts_to_remove:
        print(f"\n5. Removing: {school} -> schools of arts")
        mask = (df['old_tag'] == school) & \
               (df['new_tag'] == school) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == parent_note)
        if mask.sum() > 0:
            df = df[~mask]
            removed_count += 1
            print(f"   ✓ Removed 1 entry (keeping qualified version)")
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

    print("\nConsolidated to lowercase (generic):")
    print("  • chess and draughts club")

    print("\nRemoved duplicate schools of arts:")
    print("  • schools of arts -> cultural societies (keeping qualified version)")
    print("  • schools of arts -> halls (keeping qualified version)")
    print("  • Katoomba School of Arts (unqualified)")
    print("  • school of arts (unqualified)")

    print("\nCapitalized proper names:")
    print("  • Congregational Church Choir")
    print("  • Nepean Football Club")
    print("  • Mountaineer Lodge")

    print("\nConsolidated schools (removed unqualified duplicates):")
    print("  • Katoomba Public School")
    print("  • Katoomba Superior Public School")
    print("  • Megalong Valley School")
    print("  • Mount Victoria School")
    print("  • school (generic)")
    print("\n  All now use only (organisation) qualified versions in Agents facet")

    print(f"\n✓ Agents capitalisation and duplicates fixed!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
