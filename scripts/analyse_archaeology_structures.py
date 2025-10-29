#!/usr/bin/env python3
"""
Analyse Archaeological Structures

This script analyses the archaeology CSV files to identify:
1. Structures (hearths and/or platforms), including merged records
2. Holes drilled in boulders associated with tents/ridgepoles (temporary shelter)
   but NOT already counted as part of hearth/platform structures

The script examines:
- FeatureType: Primary feature classification
- RevisedFeatureType: Updated classification after analysis
- Tags: Additional feature characteristics
- Xref/x-ref: Cross-references indicating merged features
- Notes: Additional context about feature associations
"""

import csv
from pathlib import Path
from collections import defaultdict


def load_archaeology_data(filepath):
    """
    Load archaeology CSV data.

    Returns:
        list: List of dictionaries, one per row
    """
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def analyse_structures(records):
    """
    Analyse records to identify structures (hearths/platforms).

    Returns:
        dict: Analysis results including structure count and details
    """
    structures = []
    merged_groups = defaultdict(list)

    for record in records:
        feature_id = record.get('FeatureID', '')
        feature_type = record.get('FeatureType', '').lower()
        revised_type = record.get('RevisedFeatureType', '').lower()
        tags = record.get('Tags', '').lower()
        xref = record.get('Xref', '') or record.get('x-ref', '')
        notes = record.get('Notes', '').lower()

        # Check if this is a hearth or platform
        is_hearth = 'hearth' in feature_type or 'hearth' in revised_type or 'hearth' in tags
        is_platform = 'platform' in feature_type or 'platform' in revised_type or 'platform' in tags

        if is_hearth or is_platform:
            structure_info = {
                'feature_id': feature_id,
                'feature_type': record.get('FeatureType', ''),
                'revised_type': record.get('RevisedFeatureType', ''),
                'tags': record.get('Tags', ''),
                'xref': xref,
                'notes': record.get('Notes', ''),
                'is_hearth': is_hearth,
                'is_platform': is_platform,
                'description': record.get('Description', '')
            }
            structures.append(structure_info)

            # Check for merged records indicated in xref or notes
            if xref:
                merged_groups[xref].append(feature_id)

    return {
        'structures': structures,
        'merged_groups': merged_groups
    }


def analyse_tent_holes(records, structure_feature_ids):
    """
    Analyse records to identify holes associated with tents/ridgepoles.

    Args:
        records: List of all records
        structure_feature_ids: Set of feature IDs already counted as structures

    Returns:
        list: Hole records associated with tents/temporary shelter
    """
    tent_holes = []

    for record in records:
        feature_id = record.get('FeatureID', '')
        feature_type = record.get('FeatureType', '').lower()
        revised_type = record.get('RevisedFeatureType', '').lower()
        tags = record.get('Tags', '').lower()
        interpretation = record.get('Interpretation', '').lower()
        description = record.get('Description', '').lower()
        notes = record.get('Notes', '').lower()

        # Check if this is a drilled hole
        is_hole = ('hole' in feature_type and 'drill' in feature_type) or \
                  ('hole' in revised_type and 'drill' in revised_type) or \
                  'prop hole' in tags or \
                  'drilled' in description

        # Skip if already counted as part of a structure
        if feature_id in structure_feature_ids:
            continue

        # Check if associated with tent/ridgepole/temporary shelter
        tent_keywords = ['tent', 'ridge pole', 'ridgepole', 'temporary', 'shelter',
                        'canvas', 'tarp', 'tarpaulin']
        has_tent_association = any(keyword in interpretation or
                                   keyword in description or
                                   keyword in notes
                                   for keyword in tent_keywords)

        if is_hole and has_tent_association:
            tent_holes.append({
                'feature_id': feature_id,
                'feature_type': record.get('FeatureType', ''),
                'revised_type': record.get('RevisedFeatureType', ''),
                'description': record.get('Description', ''),
                'interpretation': record.get('Interpretation', ''),
                'tags': record.get('Tags', ''),
                'notes': record.get('Notes', '')
            })

    return tent_holes


def main():
    """Analyse and report on archaeological structures."""

    base_dir = Path(__file__).parent.parent

    # Load data
    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    ng_records = load_archaeology_data(ng_file)
    rc_records = load_archaeology_data(rc_file)
    all_records = ng_records + rc_records

    print("=" * 80)
    print("ARCHAEOLOGICAL STRUCTURES ANALYSIS")
    print("=" * 80)
    print()

    # Analyse structures
    structure_analysis = analyse_structures(all_records)
    structures = structure_analysis['structures']
    merged_groups = structure_analysis['merged_groups']

    # Count unique structures (accounting for merged features)
    structure_feature_ids = {s['feature_id'] for s in structures}

    # Report structures
    print(f"STRUCTURES (Hearths and/or Platforms): {len(structures)}")
    print()
    print("Individual feature records with hearth/platform designation:")
    print(f"  Total records: {len(structures)}")
    print()

    # Categorise structures
    hearth_only = [s for s in structures if s['is_hearth'] and not s['is_platform']]
    platform_only = [s for s in structures if s['is_platform'] and not s['is_hearth']]
    both = [s for s in structures if s['is_hearth'] and s['is_platform']]

    print("Breakdown by type:")
    print(f"  Hearth only: {len(hearth_only)}")
    print(f"  Platform only: {len(platform_only)}")
    print(f"  Hearth + Platform (both designated): {len(both)}")
    print()

    # Report merged features
    if merged_groups:
        print("Merged feature groups (cross-referenced):")
        for xref, feature_ids in merged_groups.items():
            if len(feature_ids) > 1:
                print(f"  {xref}: Features {', '.join(feature_ids)} (merged)")
        print()

    print("-" * 80)
    print()

    # Analyse tent holes
    tent_holes = analyse_tent_holes(all_records, structure_feature_ids)

    print(f"HOLES DRILLED IN BOULDERS (Tent/Temporary Shelter Association): {len(tent_holes)}")
    print()
    if tent_holes:
        print("These holes are NOT already counted as part of hearth/platform structures")
        print("and are associated with tents, ridgepoles, or temporary shelter:")
        print()
        for hole in tent_holes:
            print(f"  Feature {hole['feature_id']}:")
            print(f"    Type: {hole['feature_type']}")
            if hole['revised_type']:
                print(f"    Revised: {hole['revised_type']}")
            if hole['interpretation']:
                print(f"    Interpretation: {hole['interpretation']}")
            if hole['description']:
                desc = hole['description'][:100] + '...' if len(hole['description']) > 100 else hole['description']
                print(f"    Description: {desc}")
            if hole['notes']:
                print(f"    Notes: {hole['notes']}")
            print()
    else:
        print("No drilled holes with tent/temporary shelter association found")
        print("(excluding those already counted as part of structures)")

    print("=" * 80)
    print()

    # Summary
    print("SUMMARY:")
    print(f"  Total structure features: {len(structures)}")
    print(f"  Tent-related holes (not in structures): {len(tent_holes)}")
    print(f"  Total shelter-related features: {len(structures) + len(tent_holes)}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
