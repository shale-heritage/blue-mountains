#!/usr/bin/env python3
"""
Script 41: Fix Primary Structure - Automated Corrections

Applies surgical fixes to align primary hierarchy with Getty Art & Architecture
Thesaurus (AAT) structure:

Phase 1: Add 7 Getty AAT root entries
Phase 2: Remove orphaned primary parent relationships (preserve thematic)
Phase 3: Restore 4 missing Town → parent=Towns relationships
Phase 4: Generate formatted list of unassigned tags for manual assignment

PRESERVATION RULES:
- Keep ALL thematic relationships (parent contains "- THEMATIC")
- Remove ONLY primary parent relationships from orphaned roots
- Never remove tags themselves
- Preserve Towns thematic structure: Towns > [Town] > [intermediates] > [entities]

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple


# Getty AAT 7 Primary Facets
GETTY_ROOTS = [
    ['Agents', 'Agents', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Places', 'Places', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Built Environment', 'Built Environment', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Activities', 'Activities', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Events', 'Events', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Associated Concepts', 'Associated Concepts', 'hierarchy', 'parent=(Getty AAT primary facet)'],
    ['Materials', 'Materials', 'hierarchy', 'parent=(Getty AAT primary facet)'],
]

# 60 Orphaned Primary Roots identified by script 40
ORPHANED_ROOTS = {
    '(conceptual facet)',
    '(new top-level facet)',
    '(place type)',
    '(thematic facet)',
    'Alcohol & Temperance',
    'Alcohol consumption & behaviour',
    'Arts & Culture',
    'Carrington',
    'Chinese community',
    'Civic organisations',
    'Communications & Postal Services',
    'Community institutions',
    'Crimes',
    'Cultural identity & heritage',
    'Economy & Labour',
    'Environment & Weather',
    'Environmental conditions',
    'Family & Domestic Life',
    'Health & Medicine',
    'Health conditions',
    'Historical periods & events',
    'Indigenous peoples',
    'Information Forms',
    'Information objects',
    'Justice & Crime',
    'Katoomba',
    'Katoomba South',
    'Legal & regulatory frameworks',
    'Legal documents',
    'Legal outcomes',
    'Legislation',
    'Leura',
    'Licenses',
    'Marginalised groups',
    'Megalong',
    'Military & War',
    'Military events',
    'Mining & Industry',
    'Mining activities',
    'Mining workforce',
    'Mount Victoria',
    'Other crimes',
    'Parent Tag',
    'Port Kembla',
    'Property crimes',
    'Race & Ethnicity',
    'Racial stereotyping & performance',
    'Religion',
    'Religious organisations',
    'Social issues',
    'Social order offences',
    'South Katoomba',
    'Sport & Recreation',
    'Sunny Corner',
    'Tourism & Accommodation',
    'Transport & Infrastructure',
    'Violent crimes',
    'Weather & climate',
    'Wentworth Falls',
    'Women & Gender',
}

# 4 Missing Town relationships from archive
MISSING_TOWN_RELATIONSHIPS = [
    ['Katoomba', 'Katoomba', 'hierarchy', 'parent=Towns'],
    ['Leura', 'Leura', 'hierarchy', 'parent=Towns'],
    ['Megalong', 'Megalong', 'hierarchy', 'parent=Towns'],
    ['Mount Victoria', 'Mount Victoria', 'hierarchy', 'parent=Towns'],
]


def load_csv(path: Path) -> List[List[str]]:
    """Load CSV into list of lists."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        for row in reader:
            rows.append(row)
    return rows


def is_thematic_relationship(notes: str) -> bool:
    """Check if this is a thematic relationship that should be preserved."""
    if not notes:
        return False
    return '- THEMATIC' in notes or 'thematic grouping' in notes.lower()


def parse_parent_from_notes(notes: str) -> str:
    """Extract parent name from notes field."""
    if not notes or 'parent=' not in notes:
        return None

    parent = notes.replace('parent=', '').split(' -')[0].split(' (')[0].strip()
    return parent


def apply_fixes(input_path: Path, output_path: Path, unassigned_report_path: Path):
    """Apply all automated fixes to CSV."""

    print("=" * 80)
    print("PRIMARY STRUCTURE FIX - AUTOMATED CORRECTIONS")
    print("=" * 80)
    print()

    # Load current CSV
    print(f"Loading {input_path}...")
    rows = load_csv(input_path)
    header = rows[0]
    data_rows = rows[1:]
    print(f"  Loaded {len(data_rows)} data rows")
    print()

    # Phase 1: Check if Getty roots already exist
    print("Phase 1: Adding Getty AAT root entries...")
    existing_getty_roots = set()
    for row in data_rows:
        if len(row) >= 4 and row[3] == 'parent=(Getty AAT primary facet)':
            existing_getty_roots.add(row[0])

    new_getty_roots = []
    for getty_root in GETTY_ROOTS:
        if getty_root[0] not in existing_getty_roots:
            new_getty_roots.append(getty_root)

    print(f"  Existing Getty roots: {len(existing_getty_roots)}")
    print(f"  Adding new Getty roots: {len(new_getty_roots)}")
    for root in new_getty_roots:
        print(f"    + {root[0]}")
    print()

    # Phase 2: Remove orphaned primary parents
    print("Phase 2: Removing orphaned primary parent relationships...")
    print(f"  Checking {len(ORPHANED_ROOTS)} orphaned roots...")

    rows_to_keep = []
    rows_removed = 0

    for row in data_rows:
        if len(row) < 4 or row[2] != 'hierarchy':
            rows_to_keep.append(row)
            continue

        notes = row[3] if len(row) > 3 else ''
        parent = parse_parent_from_notes(notes)

        # Keep row if:
        # 1. Not a hierarchy entry, OR
        # 2. Parent is not an orphaned root, OR
        # 3. It's a thematic relationship (preserve these)
        if not parent:
            rows_to_keep.append(row)
        elif parent not in ORPHANED_ROOTS:
            rows_to_keep.append(row)
        elif is_thematic_relationship(notes):
            rows_to_keep.append(row)
            # print(f"    ✓ Preserved thematic: {row[0]} → {parent} - THEMATIC")
        else:
            rows_removed += 1
            print(f"    - Removed: {row[0]} → parent={parent}")

    print(f"  Removed {rows_removed} orphaned primary parent relationships")
    print(f"  Kept {len(rows_to_keep)} rows (including preserved thematic)")
    print()

    # Phase 3: Restore missing Town relationships
    print("Phase 3: Restoring missing Town → parent=Towns relationships...")

    existing_town_primary = set()
    for row in rows_to_keep:
        if len(row) >= 4 and row[2] == 'hierarchy':
            notes = row[3] if len(row) > 3 else ''
            parent = parse_parent_from_notes(notes)
            if parent == 'Towns' and '- THEMATIC' not in notes:
                existing_town_primary.add(row[0])

    missing_to_add = []
    for town_rel in MISSING_TOWN_RELATIONSHIPS:
        if town_rel[0] not in existing_town_primary:
            missing_to_add.append(town_rel)

    print(f"  Existing town primary relationships: {len(existing_town_primary)}")
    print(f"  Adding missing relationships: {len(missing_to_add)}")
    for rel in missing_to_add:
        print(f"    + {rel[0]} → parent=Towns")
    print()

    # Combine all rows
    final_rows = [header] + new_getty_roots + rows_to_keep + missing_to_add

    # Write output CSV
    print(f"Writing updated CSV to {output_path}...")
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(final_rows)
    print(f"  ✓ Written {len(final_rows) - 1} data rows")
    print()

    # Phase 4: Generate unassigned tags report
    print("Phase 4: Generating unassigned tags report...")

    # Build maps
    all_tags = set()
    tags_with_primary_parent = set()
    thematic_children = defaultdict(set)

    for row in final_rows[1:]:  # Skip header
        if len(row) < 3:
            continue

        tag = row[0]
        all_tags.add(tag)

        if row[2] == 'hierarchy' and len(row) >= 4:
            notes = row[3]
            parent = parse_parent_from_notes(notes)

            if parent:
                if is_thematic_relationship(notes):
                    thematic_children[tag].add(parent)
                else:
                    tags_with_primary_parent.add(tag)

    # Getty roots have implicit primary parent
    getty_facet_names = {root[0] for root in GETTY_ROOTS}
    tags_with_primary_parent.update(getty_facet_names)

    # Find unassigned
    unassigned_tags = sorted(all_tags - tags_with_primary_parent)

    print(f"  Total tags: {len(all_tags)}")
    print(f"  Tags with primary parent: {len(tags_with_primary_parent)}")
    print(f"  Unassigned tags: {len(unassigned_tags)}")
    print()

    # Write unassigned tags report
    print(f"Writing unassigned tags report to {unassigned_report_path}...")
    with open(unassigned_report_path, 'w', encoding='utf-8') as f:
        f.write("# Unassigned Tags - Manual Getty Facet Assignment Needed\n\n")
        f.write(f"**Generated:** 2025-10-24\n")
        f.write(f"**Total unassigned:** {len(unassigned_tags)}\n\n")
        f.write("These tags have no primary hierarchy parent after automated cleanup.\n")
        f.write("Each needs manual assignment to one of the 7 Getty AAT facets:\n\n")
        f.write("1. Agents\n")
        f.write("2. Places\n")
        f.write("3. Built Environment\n")
        f.write("4. Activities\n")
        f.write("5. Events\n")
        f.write("6. Associated Concepts\n")
        f.write("7. Materials\n\n")
        f.write("---\n\n")

        for tag in unassigned_tags:
            f.write(f"**{tag}**\n")

            # Show thematic parents if any
            if tag in thematic_children and thematic_children[tag]:
                parents = sorted(thematic_children[tag])
                f.write(f"  Thematic parents: {', '.join(parents)}\n")

            f.write("  **Assign to Getty facet path:** _______________\n\n")

    print(f"  ✓ Unassigned tags report written")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY OF CHANGES")
    print("=" * 80)
    print()
    print(f"✓ Added {len(new_getty_roots)} Getty AAT root entries")
    print(f"✓ Removed {rows_removed} orphaned primary parent relationships")
    print(f"✓ Restored {len(missing_to_add)} missing Town relationships")
    print(f"✓ Generated report for {len(unassigned_tags)} unassigned tags")
    print()
    print(f"Input:  {input_path} ({len(data_rows)} rows)")
    print(f"Output: {output_path} ({len(final_rows) - 1} rows)")
    print(f"Report: {unassigned_report_path}")
    print()
    print("Next steps:")
    print("1. Review unassigned tags report")
    print("2. Assign each tag to appropriate Getty facet path")
    print("3. Regenerate visualizations to verify 7 primary trees")
    print()


def main():
    """Main execution."""
    input_path = Path('data/tag_map_consolidated.csv')
    output_path = Path('data/tag_map_consolidated.csv')  # Overwrite in place
    backup_path = Path('data/tag_map_consolidated.csv.backup')
    unassigned_report_path = Path('reports/unassigned_tags_for_manual_assignment.md')

    if not input_path.exists():
        print(f"ERROR: {input_path} not found")
        return 1

    # Create backup
    print(f"Creating backup: {backup_path}")
    import shutil
    shutil.copy2(input_path, backup_path)
    print()

    # Ensure reports directory exists
    unassigned_report_path.parent.mkdir(parents=True, exist_ok=True)

    # Apply fixes
    apply_fixes(input_path, output_path, unassigned_report_path)

    return 0


if __name__ == '__main__':
    exit(main())
