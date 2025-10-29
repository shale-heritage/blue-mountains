#!/usr/bin/env python3
"""
Count Archaeological Structures by Site

Separate counts for:
- Nellie's Glen (NG-Entity-Feature.csv)
- Ruined Castle (RC-Entity-Feature.csv)
"""

import csv
from pathlib import Path
from collections import defaultdict


def analyse_structures_by_site(filepath, site_name):
    """
    Analyse structures from a single site.

    Returns:
        dict: Structure information for the site
    """
    structures = []
    merged_groups = defaultdict(list)

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for record in reader:
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
                    'is_hearth': is_hearth,
                    'is_platform': is_platform,
                    'xref': xref
                })

                # Track merged groups
                if xref and '|' in xref:
                    merged_groups[xref].append(feature_id)

    # Filter to only groups with multiple features
    actual_merges = {k: v for k, v in merged_groups.items() if len(v) > 1}

    return {
        'site_name': site_name,
        'structures': structures,
        'merged_groups': actual_merges
    }


def main():
    """Generate site-specific structure counts."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    # Analyse each site
    ng_data = analyse_structures_by_site(ng_file, "Nellie's Glen (NG)")
    rc_data = analyse_structures_by_site(rc_file, "Ruined Castle (RC)")

    print("=" * 80)
    print("ARCHAEOLOGICAL STRUCTURES BY SITE")
    print("=" * 80)
    print()

    # Report for each site
    for site_data in [ng_data, rc_data]:
        structures = site_data['structures']
        merged_groups = site_data['merged_groups']

        print(f"{site_data['site_name']}")
        print("-" * 80)
        print()
        print(f"Total structure feature records: {len(structures)}")
        print()

        # Breakdown
        hearth_only = sum(1 for s in structures if s['is_hearth'] and not s['is_platform'])
        platform_only = sum(1 for s in structures if s['is_platform'] and not s['is_hearth'])
        both = sum(1 for s in structures if s['is_hearth'] and s['is_platform'])

        print("Breakdown:")
        print(f"  • Hearth only: {hearth_only}")
        print(f"  • Platform only: {platform_only}")
        print(f"  • Both hearth and platform: {both}")
        print()

        if merged_groups:
            print(f"Merged feature groups: {len(merged_groups)}")
            for xref, feature_ids in merged_groups.items():
                print(f"  • {xref}: Features {', '.join(feature_ids)}")
            print()

            total_merged_records = sum(len(v) for v in merged_groups.values())
            estimated_unique = len(structures) - total_merged_records + len(merged_groups)
            print(f"Estimated unique structures: {estimated_unique}")
            print(f"  ({len(structures)} records - {total_merged_records} merged + {len(merged_groups)} groups)")
        else:
            print("No merged groups")
            print(f"Estimated unique structures: {len(structures)}")

        print()
        print()

    # Summary table
    print("=" * 80)
    print()
    print("SUMMARY:")
    print()
    print(f"{'Site':<25} {'Records':<12} {'Merges':<12} {'Unique Structures (est.)':<25}")
    print("-" * 80)

    for site_data in [ng_data, rc_data]:
        structures = site_data['structures']
        merged_groups = site_data['merged_groups']
        total_merged_records = sum(len(v) for v in merged_groups.values()) if merged_groups else 0
        estimated_unique = len(structures) - total_merged_records + len(merged_groups) if merged_groups else len(structures)

        site_short = "Nellie's Glen" if "NG" in site_data['site_name'] else "Ruined Castle"
        print(f"{site_short:<25} {len(structures):<12} {len(merged_groups):<12} {estimated_unique:<25}")

    # Grand total
    ng_count = len(ng_data['structures'])
    rc_count = len(rc_data['structures'])
    ng_unique = len(ng_data['structures']) - sum(len(v) for v in ng_data['merged_groups'].values()) + len(ng_data['merged_groups']) if ng_data['merged_groups'] else len(ng_data['structures'])
    rc_unique = len(rc_data['structures']) - sum(len(v) for v in rc_data['merged_groups'].values()) + len(rc_data['merged_groups']) if rc_data['merged_groups'] else len(rc_data['structures'])

    print("-" * 80)
    print(f"{'TOTAL':<25} {ng_count + rc_count:<12} {len(ng_data['merged_groups']) + len(rc_data['merged_groups']):<12} {ng_unique + rc_unique:<25}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
