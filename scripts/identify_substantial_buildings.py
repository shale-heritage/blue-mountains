#!/usr/bin/env python3
"""
Identify Substantial Buildings

Analyse structure records to identify those that may represent more substantial
buildings rather than simple huts or temporary shelters.

Indicators of substantial buildings:
- Larger platform dimensions (>4m in any dimension)
- Brick construction (indicates more permanent structure)
- Multiple rooms or complex features
- Stone masonry (more elaborate than simple hearth)
- Descriptors like "dwelling", "house", "building" vs "hut"
- Multiple hearths or substantial structural features
- Evidence of foundations, flooring, or other substantial construction
"""

import csv
import re
from pathlib import Path


def extract_dimensions(description):
    """
    Extract platform dimensions from description.

    Returns:
        list: List of dimension values in metres
    """
    if not description:
        return []

    # Pattern to match dimensions like "3m", "3.5m", "3 m", etc.
    # Common patterns: "3m long", "width 3m", "3.5 X 4m", etc.
    dimension_patterns = [
        r'(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)\s*m',  # "3 x 4m" or "3.5 X 4.2m"
        r'(\d+\.?\d*)\s*m\s*[xX×]\s*(\d+\.?\d*)\s*m',  # "3m x 4m"
        r'(\d+\.?\d*)\s*m',  # Any "Nm" pattern
        r'width[:\s]+(\d+\.?\d*)',  # "width 3" or "width: 3"
        r'length[:\s]+(\d+\.?\d*)',  # "length 4"
    ]

    dimensions = []
    for pattern in dimension_patterns:
        matches = re.findall(pattern, description.lower())
        for match in matches:
            if isinstance(match, tuple):
                dimensions.extend([float(d) for d in match if d])
            else:
                try:
                    dimensions.append(float(match))
                except ValueError:
                    pass

    return dimensions


def assess_building_scale(record):
    """
    Assess whether a structure represents a substantial building.

    Returns:
        dict: Assessment results
    """
    feature_id = record.get('FeatureID', '')
    description = record.get('Description', '')
    material = record.get('Material', '')
    revised_type = record.get('RevisedFeatureType', '')
    tags = record.get('Tags', '')
    comments = record.get('Comments', '')
    interpretation = record.get('Interpretation', '')

    # Combine all text fields for analysis
    all_text = ' '.join([description, material, revised_type, tags,
                         comments, interpretation]).lower()

    indicators = {
        'feature_id': feature_id,
        'is_substantial': False,
        'reasons': [],
        'description': description,
        'material': material,
        'revised_type': revised_type,
        'interpretation': interpretation
    }

    # Check for brick construction
    if 'brick' in all_text:
        indicators['reasons'].append('Brick construction')
        indicators['is_substantial'] = True

    # Check for masonry
    if 'masonry' in all_text and 'hearth' not in all_text:
        indicators['reasons'].append('Masonry structure (not just hearth)')
        indicators['is_substantial'] = True

    # Check dimensions
    dimensions = extract_dimensions(description)
    if dimensions:
        max_dim = max(dimensions)
        if max_dim >= 5.0:
            indicators['reasons'].append(f'Large dimensions (up to {max_dim}m)')
            indicators['is_substantial'] = True
        elif max_dim >= 4.0:
            indicators['reasons'].append(f'Moderate-large dimensions (up to {max_dim}m)')

    # Check for dwelling terminology
    if 'dwelling' in all_text:
        indicators['reasons'].append('Designated as "dwelling"')
        indicators['is_substantial'] = True

    if 'house' in all_text:
        indicators['reasons'].append('Designated as "house"')
        indicators['is_substantial'] = True

    # Check for multiple hearths
    if re.search(r'(two|2|multiple|several)\s+(hearth|fireplace)', all_text):
        indicators['reasons'].append('Multiple hearths')
        indicators['is_substantial'] = True

    # Check for apsidal construction (more elaborate)
    if 'apsidal' in all_text:
        indicators['reasons'].append('Apsidal construction (complex form)')
        indicators['is_substantial'] = True

    # Check for flooring/foundations
    if 'floor' in all_text or 'foundation' in all_text:
        indicators['reasons'].append('Evidence of flooring/foundations')
        indicators['is_substantial'] = True

    # Check for multiple rooms or partitions
    if 'room' in all_text or 'partition' in all_text:
        indicators['reasons'].append('Multiple rooms/partitions')
        indicators['is_substantial'] = True

    # Check for "built up" platforms (suggests more effort/permanence)
    if 'built up' in all_text:
        # Only count if substantial dimensions too
        if dimensions and max(dimensions) >= 4.0:
            indicators['reasons'].append('Built-up platform (artificial leveling)')

    # Check for rectangular/rectilinear construction
    if 'rectangular' in all_text and dimensions and max(dimensions) >= 4.0:
        indicators['reasons'].append('Rectangular construction (planned layout)')

    return indicators


def main():
    """Identify and report substantial buildings."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    print("=" * 80)
    print("SUBSTANTIAL BUILDINGS ANALYSIS")
    print("=" * 80)
    print()
    print("Identifying structures that may represent more substantial buildings")
    print("rather than simple huts or temporary shelters.")
    print()

    # Analyse each site
    for site_name, filepath in [("Nellie's Glen (NG)", ng_file),
                                 ("Ruined Castle (RC)", rc_file)]:

        substantial_buildings = []

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for record in reader:
                feature_type = record.get('FeatureType', '').lower()
                revised_type = record.get('RevisedFeatureType', '').lower()
                tags = record.get('Tags', '').lower()

                # Check if it's a structure
                is_structure = ('hearth' in feature_type or 'hearth' in revised_type or
                              'hearth' in tags or 'platform' in feature_type or
                              'platform' in revised_type or 'platform' in tags or
                              'masonry' in feature_type or 'masonry' in revised_type)

                if is_structure:
                    assessment = assess_building_scale(record)
                    if assessment['is_substantial']:
                        substantial_buildings.append(assessment)

        # Report findings
        print("=" * 80)
        print(f"{site_name}")
        print("=" * 80)
        print()

        if substantial_buildings:
            print(f"Found {len(substantial_buildings)} potentially substantial building(s):")
            print()

            for building in substantial_buildings:
                print(f"Feature {building['feature_id']}")
                print(f"  Revised Type: {building['revised_type']}")
                print(f"  Indicators of substantial construction:")
                for reason in building['reasons']:
                    print(f"    • {reason}")
                if building['description']:
                    desc = building['description']
                    if len(desc) > 200:
                        desc = desc[:200] + '...'
                    print(f"  Description: {desc}")
                if building['interpretation']:
                    print(f"  Interpretation: {building['interpretation']}")
                print()
        else:
            print("No structures identified as potentially substantial buildings")
            print("(all appear to be simple huts or temporary shelters)")
            print()

    print("=" * 80)
    print()
    print("METHODOLOGY:")
    print()
    print("Indicators of substantial buildings include:")
    print("  • Brick construction (vs simple stone hearths)")
    print("  • Large dimensions (≥5m) or moderate-large (≥4m)")
    print("  • Masonry structures (beyond simple hearth)")
    print("  • Designated as 'dwelling' or 'house' (vs 'hut')")
    print("  • Multiple hearths")
    print("  • Apsidal or complex construction")
    print("  • Evidence of flooring, foundations")
    print("  • Multiple rooms or partitions")
    print("  • Built-up platforms with substantial dimensions")
    print("  • Rectangular/planned layouts with substantial dimensions")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
