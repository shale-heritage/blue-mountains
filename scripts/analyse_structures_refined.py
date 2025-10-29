#!/usr/bin/env python3
"""
Refined Analysis of Archaeological Structures

This script provides detailed analysis of:
1. Structures (hearths and/or platforms), accounting for merged records
2. Prop holes (drilled holes in boulders) and their associations
"""

import csv
from pathlib import Path
from collections import defaultdict


def load_archaeology_data(filepath):
    """Load archaeology CSV data."""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def main():
    """Analyse structures and prop holes."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    ng_records = load_archaeology_data(ng_file)
    rc_records = load_archaeology_data(rc_file)
    all_records = ng_records + rc_records

    print("=" * 80)
    print("REFINED ARCHAEOLOGICAL STRUCTURES ANALYSIS")
    print("=" * 80)
    print()

    # Find all hearth/platform structures
    structures = []
    merged_info = defaultdict(list)

    for record in all_records:
        feature_id = record.get('FeatureID', '')
        feature_type = record.get('FeatureType', '').lower()
        revised_type = record.get('RevisedFeatureType', '').lower()
        tags = record.get('Tags', '').lower()

        is_hearth = 'hearth' in feature_type or 'hearth' in revised_type or 'hearth' in tags
        is_platform = 'platform' in feature_type or 'platform' in revised_type or 'platform' in tags

        if is_hearth or is_platform:
            xref = record.get('Xref', '') or record.get('x-ref', '')
            structures.append({
                'feature_id': feature_id,
                'feature_type': record.get('FeatureType', ''),
                'revised_type': record.get('RevisedFeatureType', ''),
                'tags': record.get('Tags', ''),
                'xref': xref,
                'notes': record.get('Notes', ''),
                'is_hearth': is_hearth,
                'is_platform': is_platform
            })

            if xref and '|' in xref:
                merged_info[xref].append(feature_id)

    print(f"1. STRUCTURES (Hearths and/or Platforms): {len(structures)} individual records")
    print()

    # Count types
    hearth_only = sum(1 for s in structures if s['is_hearth'] and not s['is_platform'])
    platform_only = sum(1 for s in structures if s['is_platform'] and not s['is_hearth'])
    both = sum(1 for s in structures if s['is_hearth'] and s['is_platform'])

    print("   Breakdown:")
    print(f"   - Hearth only: {hearth_only}")
    print(f"   - Platform only: {platform_only}")
    print(f"   - Hearth + Platform: {both}")
    print()

    # Report merged groups
    actual_merges = {k: v for k, v in merged_info.items() if len(v) > 1}
    if actual_merges:
        print("   Merged feature groups:")
        for xref, feature_ids in actual_merges.items():
            print(f"   - Features {', '.join(feature_ids)} merged as {xref}")
        print()
        print(f"   Note: {len(actual_merges)} merged groups representing")
        print(f"         {sum(len(v) for v in actual_merges.values())} individual records")
        print()

    print("-" * 80)
    print()

    # Find prop holes
    prop_holes = []
    structure_feature_ids = {s['feature_id'] for s in structures}

    for record in all_records:
        feature_id = record.get('FeatureID', '')
        feature_type = record.get('FeatureType', '').lower()
        revised_type = record.get('RevisedFeatureType', '').lower()
        description = record.get('Description', '').lower()
        notes = record.get('Notes', '').lower()
        tags = record.get('Tags', '').lower()

        # Identify drilled holes/prop holes
        is_drilled_hole = ('hole' in feature_type and 'drill' in feature_type) or \
                          'prop hole' in revised_type or \
                          'prop hole' in tags

        if is_drilled_hole:
            # Check if part of existing structure
            part_of_structure = feature_id in structure_feature_ids or \
                               'hearth' in revised_type or \
                               'platform' in revised_type or \
                               'part of same structure' in notes

            prop_holes.append({
                'feature_id': feature_id,
                'feature_type': record.get('FeatureType', ''),
                'revised_type': record.get('RevisedFeatureType', ''),
                'tags': record.get('Tags', ''),
                'description': record.get('Description', ''),
                'notes': record.get('Notes', ''),
                'part_of_structure': part_of_structure
            })

    print(f"2. PROP HOLES (Holes Drilled in Boulders): {len(prop_holes)} total")
    print()

    if prop_holes:
        standalone = [h for h in prop_holes if not h['part_of_structure']]
        associated = [h for h in prop_holes if h['part_of_structure']]

        print(f"   Associated with hearth/platform structures: {len(associated)}")
        if associated:
            for hole in associated:
                print(f"   - Feature {hole['feature_id']}: {hole['revised_type']}")
                if hole['notes']:
                    print(f"     Notes: {hole['notes']}")
        print()

        print(f"   Standalone (NOT associated with hearth/platform): {len(standalone)}")
        if standalone:
            print()
            print("   These may represent temporary shelter (tent/ridgepole supports):")
            for hole in standalone:
                print(f"   - Feature {hole['feature_id']}")
                print(f"     Type: {hole['feature_type']} → {hole['revised_type']}")
                print(f"     Tags: {hole['tags']}")
                if hole['description']:
                    desc = hole['description'][:120] + '...' if len(hole['description']) > 120 else hole['description']
                    print(f"     Description: {desc}")
                if hole['notes']:
                    print(f"     Notes: {hole['notes']}")
                print()

    print("=" * 80)
    print()
    print("SUMMARY:")
    print(f"  Hearth/Platform structures: {len(structures)} records")
    if actual_merges:
        print(f"  (includes {len(actual_merges)} merged groups)")
    print(f"  Prop holes (standalone): {len([h for h in prop_holes if not h['part_of_structure']])}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
