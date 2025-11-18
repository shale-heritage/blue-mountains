#!/usr/bin/env python3
"""
Comprehensive Agents Facet Corrections

This script implements multiple corrections to the Agents facet:

1. Courts corrections:
   - Change "Courts of Petty Sessions" to singular "Court of Petty Sessions"
   - Remove "Police court" hierarchy, keep as synonym
   - Rename "Penrith Police Court" to "Penrith Court of Petty Sessions"

2. Military capitalisation:
   - Mountain Rifle Reserves (capitalize)

3. Churches corrections:
   - Remove unqualified "church" hierarchy entry
   - Capitalize denomination names (Congregational, Methodist, Presbyterian, Wesleyan)
   - Capitalize specific church names (roman catholic church lawson)

4. Religious organisations capitalisation:
   - Waverley Friary
   - Methodist Band of Hope

5. Family names capitalisation:
   - Davey, Eaton, Evans, Flynn, Gordon, Hartman, Husband, Meredith, Penman, Watkins

6. Hotelliers consolidation:
   - Merge punctuated names into minimal-punctuation versions
   - Make punctuated versions synonyms

7. Postmasters consolidation:
   - Merge punctuated names into minimal-punctuation versions
   - Make punctuated versions synonyms

8. Occupations cleanup:
   - Remove "other goods and services" intermediate
   - Move "coach and buggy business" directly under occupations

Evidence: Manual review and user instructions
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
    print("COMPREHENSIVE AGENTS FACET CORRECTIONS")
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
    added_count = 0

    print("\n" + "=" * 80)
    print("1. COURTS CORRECTIONS")
    print("=" * 80)

    # Change Courts of Petty Sessions to singular
    print("\n1a. Changing 'Courts of Petty Sessions' to singular")
    mask = df['new_tag'] == 'Courts of Petty Sessions'
    if mask.sum() > 0:
        df.loc[mask, 'new_tag'] = 'Court of Petty Sessions'
        # Also update old_tag for hierarchy entries
        mask2 = df['old_tag'] == 'Courts of Petty Sessions'
        df.loc[mask2, 'old_tag'] = 'Court of Petty Sessions'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    # Remove Police court hierarchy, keep as synonym
    print("\n1b. Removing: Police court -> courts")
    mask = (df['old_tag'] == 'Police court') & \
           (df['new_tag'] == 'Police court') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=courts')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry (keeping synonym mappings)")
    else:
        print(f"   ⚠ Entry not found")

    # Rename Penrith Police Court
    print("\n1c. Renaming: Penrith Police Court -> Penrith Court of Petty Sessions")
    mask = df['old_tag'] == 'Penrith Police Court'
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Penrith Court of Petty Sessions'
        df.loc[mask, 'new_tag'] = 'Penrith Court of Petty Sessions'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")

        # Add synonym for old name
        new_entry = pd.DataFrame([{
            'old_tag': 'Penrith Police Court',
            'new_tag': 'Penrith Court of Petty Sessions',
            'action': 'synonym',
            'notes': 'Colloquial term - use Court of Petty Sessions',
            'status': 'active'
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        added_count += 1
        print(f"   ✓ Added synonym mapping")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("2. MILITARY CAPITALISATION")
    print("=" * 80)

    # Mountain Rifle Reserves
    print("\n2. Capitalizing: mountain rifle reserves")
    mask = df['old_tag'] == 'mountain rifle reserves'
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Mountain Rifle Reserves'
        df.loc[mask, 'new_tag'] = 'Mountain Rifle Reserves'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("3. CHURCHES CORRECTIONS")
    print("=" * 80)

    # Remove unqualified church hierarchy
    print("\n3a. Removing: church -> churches (unqualified)")
    mask = (df['old_tag'] == 'church') & \
           (df['new_tag'] == 'church') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=churches')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry (keeping qualified versions)")
    else:
        print(f"   ⚠ Entry not found")

    # Capitalize denominations
    print("\n3b. Capitalizing denomination names")

    denominations = [
        ('congregational', 'Congregational'),
        ('methodist', 'Methodist'),
        ('presbyterian', 'Presbyterian'),
        ('wesleyan', 'Wesleyan')
    ]

    for old_denom, new_denom in denominations:
        # Update all entries containing the lowercase denomination
        mask = df['old_tag'].str.contains(f'^{old_denom}', case=False, regex=True, na=False)
        count_before = mask.sum()
        if count_before > 0:
            # Replace at start of string
            df.loc[mask, 'old_tag'] = df.loc[mask, 'old_tag'].str.replace(
                f'^{old_denom}', new_denom, regex=True
            )
            df.loc[mask, 'new_tag'] = df.loc[mask, 'new_tag'].str.replace(
                f'^{old_denom}', new_denom, regex=True
            )
            # Also update in notes
            notes_mask = df['notes'].str.contains(f'{old_denom}', case=False, na=False)
            df.loc[notes_mask, 'notes'] = df.loc[notes_mask, 'notes'].str.replace(
                f'{old_denom}', new_denom, case=False, regex=False
            )
            updated_count += count_before
            print(f"   ✓ {new_denom}: Updated {count_before} entry(ies)")

    # Fix specific lowercase church names
    print("\n3c. Capitalizing specific church names")

    specific_churches = [
        ('roman catholic church lawson', 'Roman Catholic Church Lawson')
    ]

    for old_name, new_name in specific_churches:
        mask = df['old_tag'] == old_name
        if mask.sum() > 0:
            df.loc[mask, 'old_tag'] = new_name
            df.loc[mask, 'new_tag'] = new_name
            updated_count += mask.sum()
            print(f"   ✓ {new_name}: Updated {mask.sum()} entry(ies)")

    print("\n" + "=" * 80)
    print("4. RELIGIOUS ORGANISATIONS CAPITALISATION")
    print("=" * 80)

    # Waverley Friary
    print("\n4a. Capitalizing: waverley friary")
    mask = df['old_tag'].str.contains('waverley friary', case=False, na=False)
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = df.loc[mask, 'old_tag'].str.replace(
            'waverley friary', 'Waverley Friary', case=False, regex=False
        )
        df.loc[mask, 'new_tag'] = df.loc[mask, 'new_tag'].str.replace(
            'waverley friary', 'Waverley Friary', case=False, regex=False
        )
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    # Methodist Band of Hope
    print("\n4b. Capitalizing: methodist band of hope")
    mask = df['old_tag'] == 'methodist band of hope'
    if mask.sum() > 0:
        df.loc[mask, 'old_tag'] = 'Methodist Band of Hope'
        df.loc[mask, 'new_tag'] = 'Methodist Band of Hope'
        updated_count += mask.sum()
        print(f"   ✓ Updated {mask.sum()} entry(ies)")
    else:
        print(f"   ⚠ Entry not found")

    print("\n" + "=" * 80)
    print("5. FAMILY NAMES CAPITALISATION")
    print("=" * 80)

    # Capitalize family surnames
    families_to_capitalize = [
        ('davey family', 'Davey family'),
        ('eaton family', 'Eaton family'),
        ('evans family', 'Evans family'),
        ('flynn family', 'Flynn family'),
        ('gordon family', 'Gordon family'),
        ('hartman family', 'Hartman family'),
        ('husband family', 'Husband family'),
        ('meredith family', 'Meredith family'),
        ('penman family', 'Penman family'),
        ('watkins family', 'Watkins family')
    ]

    for old_name, new_name in families_to_capitalize:
        mask = df['old_tag'] == old_name
        if mask.sum() > 0:
            df.loc[mask, 'old_tag'] = new_name
            df.loc[mask, 'new_tag'] = new_name
            updated_count += mask.sum()
            print(f"   ✓ {new_name}: Updated {mask.sum()} entry(ies)")

    print("\n" + "=" * 80)
    print("6. HOTELLIERS CONSOLIDATION (remove punctuation)")
    print("=" * 80)

    # Hotelliers with punctuation to consolidate
    hotelliers_consolidations = [
        ('F. C. Goyder', 'F C Goyder'),
        ('Isabellea J. Long', 'Isabellea J Long'),
        ('Mr A. G. Rowell', 'Mr A G Rowell'),
        ('Mr Alf. Goodare', 'Mr Alf Goodare'),
        ('Mr D. Brown', 'Mr D Brown'),
        ('Mr D. Thompson', 'Mr D Thompson'),
    ]

    for punctuated, minimal in hotelliers_consolidations:
        # Remove punctuated hierarchy entry
        mask = (df['old_tag'] == punctuated) & \
               (df['new_tag'] == punctuated) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=hotelliers')
        if mask.sum() > 0:
            df = df[~mask]
            removed_count += 1
            print(f"   ✓ Removed: {punctuated}")

            # Add synonym mapping if it doesn't exist
            synonym_exists = (
                (df['old_tag'] == punctuated) &
                (df['new_tag'] == minimal) &
                (df['action'] == 'synonym')
            ).any()

            if not synonym_exists:
                new_entry = pd.DataFrame([{
                    'old_tag': punctuated,
                    'new_tag': minimal,
                    'action': 'synonym',
                    'notes': 'Punctuated variant - use minimal punctuation',
                    'status': 'active'
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                added_count += 1
                print(f"   ✓ Added synonym: {punctuated} → {minimal}")

    print("\n" + "=" * 80)
    print("7. POSTMASTERS CONSOLIDATION (remove punctuation)")
    print("=" * 80)

    # Postmasters with punctuation to consolidate
    postmasters_consolidations = [
        ('Mrs. A. Smith', 'Mrs A Smith'),
        ('Mrs. England', 'Mrs England'),
        ('Mrs. H. Corston', 'Mrs H Corston'),
        ('Mrs. James', 'Mrs James'),
    ]

    for punctuated, minimal in postmasters_consolidations:
        # Remove punctuated hierarchy entry
        mask = (df['old_tag'] == punctuated) & \
               (df['new_tag'] == punctuated) & \
               (df['action'] == 'hierarchy') & \
               (df['notes'] == 'parent=postmasters')
        if mask.sum() > 0:
            df = df[~mask]
            removed_count += 1
            print(f"   ✓ Removed: {punctuated}")

            # Add synonym mapping if it doesn't exist
            synonym_exists = (
                (df['old_tag'] == punctuated) &
                (df['new_tag'] == minimal) &
                (df['action'] == 'synonym')
            ).any()

            if not synonym_exists:
                new_entry = pd.DataFrame([{
                    'old_tag': punctuated,
                    'new_tag': minimal,
                    'action': 'synonym',
                    'notes': 'Punctuated variant - use minimal punctuation',
                    'status': 'active'
                }])
                df = pd.concat([df, new_entry], ignore_index=True)
                added_count += 1
                print(f"   ✓ Added synonym: {punctuated} → {minimal}")

    print("\n" + "=" * 80)
    print("8. OCCUPATIONS CLEANUP")
    print("=" * 80)

    # Remove "other goods and services" intermediate
    print("\n8a. Removing: other goods and services -> occupations")
    mask = (df['old_tag'] == 'other goods and services') & \
           (df['new_tag'] == 'other goods and services') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=occupations')
    if mask.sum() > 0:
        df = df[~mask]
        removed_count += 1
        print(f"   ✓ Removed 1 entry")
    else:
        print(f"   ⚠ Entry not found")

    # Move coach and buggy business to occupations
    print("\n8b. Moving: coach and buggy business -> occupations")
    mask = (df['old_tag'] == 'coach and buggy business') & \
           (df['new_tag'] == 'coach and buggy business') & \
           (df['action'] == 'hierarchy') & \
           (df['notes'] == 'parent=other goods and services')
    if mask.sum() > 0:
        df.loc[mask, 'notes'] = 'parent=occupations'
        updated_count += 1
        print(f"   ✓ Updated parent to occupations")
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
    print(f"  Added:         {added_count}")

    save_csv(df)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("\n1. Courts corrections:")
    print("  • Changed 'Courts of Petty Sessions' to singular")
    print("  • Removed 'Police court' hierarchy (kept synonyms)")
    print("  • Renamed 'Penrith Police Court' to 'Penrith Court of Petty Sessions'")

    print("\n2. Capitalisation:")
    print("  • Mountain Rifle Reserves")
    print("  • Denominations: Congregational, Methodist, Presbyterian, Wesleyan")
    print("  • Roman Catholic Church Lawson")
    print("  • Waverley Friary")
    print("  • Methodist Band of Hope")
    print("  • Family surnames: Davey, Eaton, Evans, Flynn, Gordon, Hartman,")
    print("                     Husband, Meredith, Penman, Watkins")

    print("\n3. Churches:")
    print("  • Removed unqualified 'church' hierarchy entry")
    print("  • All churches now use qualified (building)/(organisation) versions")

    print("\n4. Name consolidations:")
    print(f"  • Hotelliers: {len(hotelliers_consolidations)} punctuated entries → minimal punctuation")
    print(f"  • Postmasters: {len(postmasters_consolidations)} punctuated entries → minimal punctuation")

    print("\n5. Occupations cleanup:")
    print("  • Removed 'other goods and services' intermediate")
    print("  • 'coach and buggy business' now directly under occupations")

    print(f"\n✓ Comprehensive agents corrections applied!")
    print(f"✓ Backup available: {backup_file}")

if __name__ == '__main__':
    main()
