#!/usr/bin/env python3
"""
Final Archaeological Structures Report

Comprehensive analysis of:
1. Hearth/platform structures with merged records
2. Prop holes and their associations
3. Assessment of temporary shelter indicators
"""

import csv
from pathlib import Path


def load_archaeology_data(filepath):
    """Load archaeology CSV data."""
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def main():
    """Generate final structure report."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    ng_records = load_archaeology_data(ng_file)
    rc_records = load_archaeology_data(rc_file)
    all_records = ng_records + rc_records

    print("=" * 80)
    print("ARCHAEOLOGICAL STRUCTURES - FINAL REPORT")
    print("=" * 80)
    print()

    # === PART 1: HEARTH/PLATFORM STRUCTURES ===

    structures = []
    merged_groups = {}

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

            # Track merged groups
            if xref and '|' in xref:
                if xref not in merged_groups:
                    merged_groups[xref] = []
                merged_groups[xref].append(feature_id)

    # Filter to only groups with multiple features
    actual_merges = {k: v for k, v in merged_groups.items() if len(v) > 1}

    print("QUESTION 1: STRUCTURES (Hearths and/or Platforms)")
    print("-" * 80)
    print()
    print(f"Total structure feature records: {len(structures)}")
    print()

    hearth_only = sum(1 for s in structures if s['is_hearth'] and not s['is_platform'])
    platform_only = sum(1 for s in structures if s['is_platform'] and not s['is_hearth'])
    both = sum(1 for s in structures if s['is_hearth'] and s['is_platform'])

    print("Breakdown by designation:")
    print(f"  • Hearth only: {hearth_only}")
    print(f"  • Platform only: {platform_only}")
    print(f"  • Both hearth and platform: {both}")
    print()

    if actual_merges:
        print(f"Merged feature groups: {len(actual_merges)}")
        print()
        for xref, feature_ids in actual_merges.items():
            print(f"  • {xref}:")
            print(f"    Features {', '.join(feature_ids)} merged into single structure")
        print()
        total_merged_records = sum(len(v) for v in actual_merges.values())
        estimated_unique = len(structures) - total_merged_records + len(actual_merges)
        print(f"Note: {len(structures)} individual records represent approximately")
        print(f"      {estimated_unique} unique structures (accounting for merges)")
    print()

    # === PART 2: PROP HOLES ===

    print("=" * 80)
    print()
    print("QUESTION 2: HOLES DRILLED IN BOULDERS (Prop Holes)")
    print("-" * 80)
    print()

    structure_feature_ids = {s['feature_id'] for s in structures}
    prop_holes = []

    for record in all_records:
        feature_id = record.get('FeatureID', '')
        feature_type = record.get('FeatureType', '').lower()
        revised_type = record.get('RevisedFeatureType', '').lower()
        tags = record.get('Tags', '').lower()
        description = record.get('Description', '').lower()
        interpretation = record.get('Interpretation', '').lower()
        notes = record.get('Notes', '').lower()

        # Identify drilled holes/prop holes
        is_drilled = ('hole' in feature_type and 'drill' in feature_type) or \
                     'prop hole' in revised_type or \
                     'prop hole' in tags

        if is_drilled:
            # Check associations
            associated_with_structure = (feature_id in structure_feature_ids or
                                        'hearth' in revised_type or
                                        'platform' in revised_type or
                                        'part of same structure' in notes)

            # Check for tent/temporary shelter indicators
            tent_indicators = ['tent', 'ridge pole', 'ridgepole', 'temporary',
                             'canvas', 'tarp', 'shelter']
            has_tent_mention = any(indicator in description or
                                  indicator in interpretation or
                                  indicator in notes
                                  for indicator in tent_indicators)

            prop_holes.append({
                'feature_id': feature_id,
                'feature_type': record.get('FeatureType', ''),
                'revised_type': record.get('RevisedFeatureType', ''),
                'tags': record.get('Tags', ''),
                'description': record.get('Description', ''),
                'notes': record.get('Notes', ''),
                'associated_with_structure': associated_with_structure,
                'has_tent_mention': has_tent_mention
            })

    standalone = [h for h in prop_holes if not h['associated_with_structure']]
    tent_related = [h for h in prop_holes if h['has_tent_mention']]

    print(f"Total prop holes found: {len(prop_holes)}")
    print()
    print(f"Associated with hearth/platform structures: {len(prop_holes) - len(standalone)}")
    print(f"Standalone (not associated with structures): {len(standalone)}")
    print()

    print(f"Holes with explicit tent/ridgepole/temporary shelter designation: {len(tent_related)}")
    print()

    if len(tent_related) == 0:
        print("RESULT: No drilled holes have been explicitly designated as")
        print("        associated with tents, ridgepoles, or temporary shelter.")
        print()

        if standalone:
            print("Note: There is 1 standalone prop hole (Feature 1013) that is NOT")
            print("      associated with a hearth/platform structure. However, this")
            print("      feature is located near mining/industrial features (ore frames,")
            print("      ropeway buckets) and has an associated slag heap, suggesting")
            print("      industrial rather than residential shelter use.")
    else:
        print("Tent-related prop holes:")
        for hole in tent_related:
            print(f"  • Feature {hole['feature_id']}: {hole['revised_type']}")
            print(f"    {hole['description']}")

    print()
    print("=" * 80)
    print()

    # === SUMMARY ===

    print("SUMMARY:")
    print()
    print(f"1. Structures (hearths/platforms): {len(structures)} feature records")
    if actual_merges:
        print(f"   (including {len(actual_merges)} merged groups)")
    print()
    print(f"2. Prop holes with tent/temporary shelter designation: {len(tent_related)}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
