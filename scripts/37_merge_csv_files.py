#!/usr/bin/env python3
"""
Script 37: Merge Tag Consolidation CSV Files

Merges tag_consolidation_map.csv and poly_hierarchy_additions.csv into unified
tag_map_consolidated.csv (single source of truth).

MERGE STRATEGY (approved 2025-10-24):
1. Remove exact duplicates from each file (126 in map, 2 in poly)
2. Poly version takes precedence for primary facet conflicts (has corrections)
3. Preserve ALL poly-hierarchical relationships (same tag, different parents)
4. Preserve ALL 37 town-based thematic groupings from map file
5. Output: tag_map_consolidated.csv with ~1100-1200 unique rows

CONFLICT RESOLUTION:
- Primary facet conflicts (91 cases): Keep poly version (corrected intermediate facets)
- Poly-hierarchy (intentional): Keep BOTH parent relationships
- Unique to map (392 relationships): Keep all (includes town groupings)
- Unique to poly: Keep all (includes new thematic groupings)

VALIDATION CHECKS:
- Exact duplicate removal
- Poly-hierarchy preservation (tags with multiple parents)
- Town groupings preserved (37 entries with parent=Katoomba, etc.)
- Primary facet corrections applied
- THEMATIC marker count >= 183

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict


def load_csv_rows(filepath):
    """
    Load CSV file into list of row dictionaries.

    Args:
        filepath: Path to CSV file

    Returns:
        list: List of dicts with keys: old_tag, new_tag, action, notes
    """
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'old_tag': row['old_tag'],
                'new_tag': row['new_tag'],
                'action': row['action'],
                'notes': row['notes']
            })
    return rows


def deduplicate_rows(rows):
    """
    Remove exact duplicate rows (same values in all fields).

    Args:
        rows: List of row dictionaries

    Returns:
        tuple: (unique_rows list, duplicate_count int)
    """
    seen = set()
    unique_rows = []
    duplicate_count = 0

    for row in rows:
        # Create hashable key from all fields
        key = (row['old_tag'], row['new_tag'], row['action'], row['notes'])

        if key not in seen:
            seen.add(key)
            unique_rows.append(row)
        else:
            duplicate_count += 1

    return unique_rows, duplicate_count


def create_relationship_index(rows):
    """
    Create index of relationships: (old_tag, notes) -> row.

    This allows us to identify unique relationships and detect conflicts.
    Each (old_tag, parent) pair is a unique relationship in poly-hierarchy.

    Args:
        rows: List of row dictionaries

    Returns:
        dict: {(old_tag, notes): row_dict}
    """
    index = {}
    for row in rows:
        key = (row['old_tag'], row['notes'])
        index[key] = row
    return index


def merge_csvs(map_file, poly_file, output_file):
    """
    Merge two CSV files with approved conflict resolution strategy.

    Strategy:
    1. Load and deduplicate both files
    2. Create relationship indices
    3. Merge: Start with map, update/add from poly (poly takes precedence)
    4. Write unified output

    Args:
        map_file: Path to tag_consolidation_map.csv
        poly_file: Path to poly_hierarchy_additions.csv
        output_file: Path to tag_map_consolidated.csv

    Returns:
        dict: Validation statistics
    """
    print("=" * 80)
    print("CSV MERGE OPERATION: Creating Single Source of Truth")
    print("=" * 80)
    print()

    # Phase 1: Load and deduplicate
    print("Phase 1: Loading and deduplicating files...")
    print()

    map_rows = load_csv_rows(map_file)
    poly_rows = load_csv_rows(poly_file)

    print(f"tag_consolidation_map.csv: {len(map_rows)} rows loaded")
    print(f"poly_hierarchy_additions.csv: {len(poly_rows)} rows loaded")
    print()

    map_unique, map_dupes = deduplicate_rows(map_rows)
    poly_unique, poly_dupes = deduplicate_rows(poly_rows)

    print(f"Deduplication results:")
    print(f"  map:  {len(map_unique)} unique rows ({map_dupes} duplicates removed)")
    print(f"  poly: {len(poly_unique)} unique rows ({poly_dupes} duplicates removed)")
    print()

    # Phase 2: Create relationship indices
    print("Phase 2: Creating relationship indices...")
    map_index = create_relationship_index(map_unique)
    poly_index = create_relationship_index(poly_unique)

    print(f"  map:  {len(map_index)} unique relationships")
    print(f"  poly: {len(poly_index)} unique relationships")
    print()

    # Phase 3: Merge with poly taking precedence
    print("Phase 3: Merging with conflict resolution...")
    print("  Strategy: poly version takes precedence for conflicts")
    print()

    # Start with map relationships, then update/add from poly
    merged_index = map_index.copy()
    merged_index.update(poly_index)  # poly overwrites conflicts

    # Calculate statistics
    map_keys = set(map_index.keys())
    poly_keys = set(poly_index.keys())
    merged_keys = set(merged_index.keys())

    common_keys = map_keys & poly_keys
    unique_to_map = map_keys - poly_keys
    unique_to_poly = poly_keys - map_keys

    # Count conflicts (same key, different values)
    conflicts = []
    for key in common_keys:
        if map_index[key] != poly_index[key]:
            conflicts.append(key)

    print(f"Merge statistics:")
    print(f"  Overlap: {len(common_keys)} relationships in both files")
    print(f"  Conflicts: {len(conflicts)} relationships with different values")
    print(f"  Unique to map: {len(unique_to_map)} relationships")
    print(f"  Unique to poly: {len(unique_to_poly)} relationships")
    print(f"  Merged total: {len(merged_keys)} unique relationships")
    print()

    # Phase 4: Write output
    print(f"Phase 4: Writing merged output to {output_file}...")

    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['old_tag', 'new_tag', 'action', 'notes'])

        # Sort by old_tag for consistent output
        for key in sorted(merged_index.keys()):
            row = merged_index[key]
            writer.writerow([
                row['old_tag'],
                row['new_tag'],
                row['action'],
                row['notes']
            ])

    print(f"✓ Wrote {len(merged_index)} rows to {output_file}")
    print()

    # Phase 5: Validation
    print("Phase 5: Validation checks...")
    print()

    # Count THEMATIC markers
    thematic_count = sum(1 for row in merged_index.values()
                         if '- THEMATIC' in row['notes'])
    print(f"  THEMATIC markers: {thematic_count} (expected >= 183)")

    # Count town groupings
    town_names = ['Katoomba', 'Blackheath', 'Leura', 'Wentworth Falls', 'Mount Victoria']
    town_groupings = []
    for key, row in merged_index.items():
        for town in town_names:
            if row['notes'] == f'parent={town}':
                town_groupings.append(key)
                break

    print(f"  Town groupings: {len(town_groupings)} (expected 37)")

    # Count poly-hierarchical tags (tags with multiple parents)
    tag_counts = defaultdict(int)
    for old_tag, _ in merged_index.keys():
        tag_counts[old_tag] += 1

    poly_tags = {tag: count for tag, count in tag_counts.items() if count > 1}
    print(f"  Poly-hierarchical tags: {len(poly_tags)} tags with multiple parents")

    # Sample validation: Check corrected intermediate facets
    test_cases = [
        ('Senior-Constable Illingworth', 'parent=Police'),
        ('Demographic groups', 'parent=People'),
    ]

    print()
    print("  Sample validation (corrected intermediate facets):")
    for tag, expected_notes in test_cases:
        key = (tag, expected_notes)
        if key in merged_index:
            print(f"    ✓ {tag} → {expected_notes}")
        else:
            print(f"    ✗ {tag} → {expected_notes} NOT FOUND")

    print()

    # Return statistics
    stats = {
        'map_rows': len(map_rows),
        'poly_rows': len(poly_rows),
        'map_unique': len(map_unique),
        'poly_unique': len(poly_unique),
        'map_duplicates': map_dupes,
        'poly_duplicates': poly_dupes,
        'merged_total': len(merged_index),
        'overlap': len(common_keys),
        'conflicts': len(conflicts),
        'unique_to_map': len(unique_to_map),
        'unique_to_poly': len(unique_to_poly),
        'thematic_count': thematic_count,
        'town_groupings': len(town_groupings),
        'poly_tags': len(poly_tags),
    }

    return stats


def main():
    """Main execution function."""
    # File paths
    data_dir = Path(__file__).parent.parent / 'data'
    map_file = data_dir / 'tag_consolidation_map.csv'
    poly_file = data_dir / 'poly_hierarchy_additions.csv'
    output_file = data_dir / 'tag_map_consolidated.csv'

    # Check input files exist
    if not map_file.exists():
        print(f"ERROR: {map_file} not found")
        return 1

    if not poly_file.exists():
        print(f"ERROR: {poly_file} not found")
        return 1

    # Perform merge
    stats = merge_csvs(map_file, poly_file, output_file)

    # Report summary
    print("=" * 80)
    print("MERGE COMPLETE - SUMMARY")
    print("=" * 80)
    print()
    print(f"Input files:")
    print(f"  tag_consolidation_map.csv:      {stats['map_rows']:4d} rows → {stats['map_unique']:4d} unique ({stats['map_duplicates']} dupes removed)")
    print(f"  poly_hierarchy_additions.csv:   {stats['poly_rows']:4d} rows → {stats['poly_unique']:4d} unique ({stats['poly_duplicates']} dupes removed)")
    print()
    print(f"Merge results:")
    print(f"  Overlap (in both files):        {stats['overlap']:4d} relationships")
    print(f"  Conflicts resolved (poly kept): {stats['conflicts']:4d} relationships")
    print(f"  Unique to map (kept):           {stats['unique_to_map']:4d} relationships")
    print(f"  Unique to poly (kept):          {stats['unique_to_poly']:4d} relationships")
    print()
    print(f"Output file:")
    print(f"  tag_map_consolidated.csv:       {stats['merged_total']:4d} unique relationships")
    print()
    print(f"Validation:")
    print(f"  THEMATIC markers:               {stats['thematic_count']:4d} (expected >= 183) {'✓' if stats['thematic_count'] >= 183 else '✗'}")
    print(f"  Town groupings:                 {stats['town_groupings']:4d} (expected 37) {'✓' if stats['town_groupings'] == 37 else '✗'}")
    print(f"  Poly-hierarchical tags:         {stats['poly_tags']:4d} tags with multiple parents")
    print()
    print("Next steps:")
    print("1. Review validation results above")
    print("2. Spot check sample entries in tag_map_consolidated.csv")
    print("3. If approved, archive old CSV files")
    print("4. Update script 22 to append to consolidated file")
    print()


if __name__ == '__main__':
    main()
