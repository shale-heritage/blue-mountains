#!/usr/bin/env python3
"""
Fix Agents Facet Errors

This script corrects duplicate hierarchies and organizational errors in the Agents facet:

1. Animals duplication: Remove cattle, dogs, horses from top-level animals
   (keep only under domestic animals)

2. Families duplication: Remove duplicate families hierarchy under people
   (keep only under demographic groups)

3. Lodge terminology: Consolidate independent lodges → unaffiliated lodges
   - Make "independent lodges" a synonym of "unaffiliated lodges"
   - Move mountaineer lodge from independent lodges to unaffiliated lodges only

4. Sunday schools: Remove direct sunday school under religious education
   (keep only under sunday schools parent node)

All corrections improve hierarchy clarity and eliminate redundancy.
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
    print("FIX AGENTS FACET ERRORS")
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
    print("1. FIXING ANIMAL DUPLICATES")
    print("=" * 80)

    # Remove cattle, dogs, horses from top-level animals (keep under domestic animals)
    animals_to_fix = ['cattle', 'dogs', 'horses']

    for animal in animals_to_fix:
        mask = (df['old_tag'] == animal) & \
               (df['new_tag'] == animal) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=animals')
        removed = df[mask]
        if len(removed) > 0:
            removed_entries.append((animal, 'animals'))
            df = df[~mask]
            print(f"✓ Removed: {animal} -> animals (keeping under domestic animals)")
        else:
            print(f"⚠ Not found: {animal} -> animals")

    print("\n" + "=" * 80)
    print("2. FIXING FAMILIES DUPLICATION")
    print("=" * 80)

    # Remove families from direct people parent (keep under demographic groups)
    print("\n2a. Removing: families -> people")
    mask = (df['old_tag'] == 'families') & \
           (df['new_tag'] == 'families') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=people')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('families', 'people'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Get list of all family names
    families_list = [
        'Austin family',
        'Brydon family',
        'Delaney family',
        'Goyder family',
        'Greenbank family',
        'Peckman family',
        'Tabrett family',
        'davey family',
        'eaton family',
        'evans family',
        'family',
        'flynn family',
        'gordon family',
        'hartman family',
        'husband family',
        'meredith family',
        "miners' families",
        'penman family',
        'watkins family'
    ]

    # Remove all family entries with parent=families where families is under people
    print("\n2b. Removing duplicate family entries (keeping under demographic groups)")
    family_count = 0
    for family in families_list:
        # Find entries where this family has parent=families
        mask = (df['old_tag'] == family) & \
               (df['new_tag'] == family) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=families')

        # Check if there are duplicates (should be 2 if duplicated)
        matches = df[mask]
        if len(matches) > 1:
            # Remove one instance (the second one)
            df = df.drop(matches.index[-1])
            removed_entries.append((family, 'families (duplicate)'))
            family_count += 1

    print(f"   ✓ Removed {family_count} duplicate family entries")

    # Handle Goyder brothers special case
    mask = (df['old_tag'] == 'Goyder brothers') & \
           (df['new_tag'] == 'Goyder brothers') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=Goyder family')
    matches = df[mask]
    if len(matches) > 1:
        df = df.drop(matches.index[-1])
        removed_entries.append(('Goyder brothers', 'Goyder family (duplicate)'))
        family_count += 1
        print(f"   ✓ Removed duplicate Goyder brothers entry")

    print("\n" + "=" * 80)
    print("3. CONSOLIDATING LODGE TERMINOLOGY")
    print("=" * 80)

    # Make "independent lodges" a synonym of "unaffiliated lodges"
    print("\n3a. Adding synonym: independent lodges -> unaffiliated lodges")
    new_entry = pd.DataFrame([{
        'old_tag': 'independent lodges',
        'new_tag': 'unaffiliated lodges',
        'action': 'synonym',
        'notes': 'Terminology preference - use unaffiliated',
        'status': 'active'
    }])
    df = pd.concat([df, new_entry], ignore_index=True)
    added_entries.append(('independent lodges', 'unaffiliated lodges (synonym)'))
    print(f"   ✓ Added synonym")

    # Remove independent lodges hierarchy
    print("\n3b. Removing: independent lodges -> lodges")
    mask = (df['old_tag'] == 'independent lodges') & \
           (df['new_tag'] == 'independent lodges') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=lodges')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('independent lodges', 'lodges'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Remove mountaineer lodge -> independent lodges
    print("\n3c. Removing: mountaineer lodge -> independent lodges")
    mask = (df['old_tag'] == 'mountaineer lodge') & \
           (df['new_tag'] == 'mountaineer lodge') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=independent lodges')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('mountaineer lodge', 'independent lodges'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry (keeping under unaffiliated lodges)")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("4. FIXING SUNDAY SCHOOL STRUCTURE")
    print("=" * 80)

    # Remove direct sunday school -> religious education (keep under sunday schools)
    print("\n4. Removing: sunday school -> religious education")
    mask = (df['old_tag'] == 'sunday school') & \
           (df['new_tag'] == 'sunday school') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=religious education')
    removed = df[mask]
    if len(removed) > 0:
        removed_entries.append(('sunday school', 'religious education'))
        df = df[~mask]
        print(f"   ✓ Removed 1 entry (keeping under sunday schools)")
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
    print(f"  Removed:       {len(removed_entries)}")
    print(f"  Added:         {len(added_entries)}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\nFixed animal duplicates:")
    print("  • Removed cattle, dogs, horses from top-level animals")
    print("  • Now only under domestic animals")

    print("\nFixed families duplication:")
    print("  • Removed families hierarchy under people")
    print(f"  • Removed {family_count} duplicate family entries")
    print("  • Families now only under demographic groups")

    print("\nConsolidated lodge terminology:")
    print("  • Made 'independent lodges' a synonym of 'unaffiliated lodges'")
    print("  • Removed independent lodges hierarchy")
    print("  • Mountaineer lodge now only under unaffiliated lodges")

    print("\nFixed sunday school structure:")
    print("  • Removed direct sunday school under religious education")
    print("  • Sunday school now only under sunday schools parent")

    print("\n✓ Agents facet errors corrected!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
