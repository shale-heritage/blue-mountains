#!/usr/bin/env python3
"""
Examine All Hole Features

This script examines all features with "hole" in the type or description
to understand their characteristics and associations.
"""

import csv
from pathlib import Path


def load_and_filter_holes(filepath):
    """Load records and filter for any with 'hole' mentions."""
    holes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check multiple fields for 'hole' keyword
            feature_type = row.get('FeatureType', '').lower()
            revised_type = row.get('RevisedFeatureType', '').lower()
            tags = row.get('Tags', '').lower()
            description = row.get('Description', '').lower()

            if ('hole' in feature_type or 'hole' in revised_type or
                'hole' in tags or 'hole' in description):
                holes.append(row)
    return holes


def main():
    """Examine all hole features."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    ng_holes = load_and_filter_holes(ng_file)
    rc_holes = load_and_filter_holes(rc_file)
    all_holes = ng_holes + rc_holes

    print("=" * 80)
    print(f"FEATURES WITH 'HOLE' KEYWORD: {len(all_holes)}")
    print("=" * 80)
    print()

    for hole in all_holes:
        print(f"Feature ID: {hole.get('FeatureID', 'N/A')}")
        print(f"  Type: {hole.get('FeatureType', 'N/A')}")
        if hole.get('RevisedFeatureType'):
            print(f"  Revised Type: {hole.get('RevisedFeatureType')}")
        if hole.get('Tags'):
            print(f"  Tags: {hole.get('Tags')}")
        if hole.get('Description'):
            desc = hole.get('Description', '')
            if len(desc) > 150:
                desc = desc[:150] + '...'
            print(f"  Description: {desc}")
        if hole.get('Interpretation'):
            print(f"  Interpretation: {hole.get('Interpretation')}")
        if hole.get('Notes'):
            print(f"  Notes: {hole.get('Notes')}")
        print()

    print("=" * 80)


if __name__ == "__main__":
    main()
