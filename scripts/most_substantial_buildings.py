#!/usr/bin/env python3
"""
Identify Most Substantial Buildings

Focus on structures with multiple strong indicators of substantial construction,
such as:
- Brick construction + other indicators
- Apsidal/complex architecture
- Multiple hearths
- Brick paving/flooring
- Masonry walls (not just simple hearth)
- Very large dimensions (>5m) + dwelling designation
- Evidence of mortar, mud render, or other finishing
"""

import csv
import re
from pathlib import Path


def extract_dimensions(description):
    """Extract platform dimensions from description."""
    if not description:
        return []

    dimension_patterns = [
        r'(\d+\.?\d*)\s*[xX×]\s*(\d+\.?\d*)\s*m',
        r'(\d+\.?\d*)\s*m\s*[xX×]\s*(\d+\.?\d*)\s*m',
        r'(\d+\.?\d*)\s*m',
        r'width[:\s]+(\d+\.?\d*)',
        r'length[:\s]+(\d+\.?\d*)',
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


def assess_substantial(record):
    """
    Assess whether structure is truly substantial.

    Returns score and list of strong indicators.
    """
    feature_id = record.get('FeatureID', '')
    description = record.get('Description', '')
    material = record.get('Material', '')
    revised_type = record.get('RevisedFeatureType', '')
    tags = record.get('Tags', '')
    comments = record.get('Comments', '')
    interpretation = record.get('Interpretation', '')

    all_text = ' '.join([description, material, revised_type, tags,
                         comments, interpretation]).lower()

    score = 0
    indicators = []

    # Strong indicators (worth more points)

    # Brick paving/flooring (very strong indicator)
    if 'brick pav' in all_text or 'brick' in all_text and 'floor' in all_text:
        score += 3
        indicators.append('Brick paved floor')

    # Mortar/render (indicates permanence)
    if 'mortar' in all_text or 'render' in all_text:
        score += 2
        indicators.append('Mortar or mud render')

    # Apsidal construction (complex architecture)
    if 'apsidal' in all_text or 'horseshoe' in all_text:
        score += 2
        indicators.append('Apsidal/horseshoe construction (complex form)')

    # Multiple hearths or double hearth
    if 'double hearth' in all_text or re.search(r'(two|2)\s+hearth', all_text):
        score += 2
        indicators.append('Multiple/double hearths')

    # Multiple courses (7+ courses indicates substantial walls)
    courses_match = re.search(r'(\d+)\s+course', all_text)
    if courses_match:
        num_courses = int(courses_match.group(1))
        if num_courses >= 7:
            score += 2
            indicators.append(f'{num_courses} courses high (substantial walls)')
        elif num_courses >= 5:
            score += 1
            indicators.append(f'{num_courses} courses high')

    # Brick construction (moderate indicator)
    if 'brick' in all_text and 'brick pav' not in all_text:
        score += 1
        indicators.append('Brick construction')

    # Large dimensions
    dimensions = extract_dimensions(description)
    if dimensions:
        max_dim = max(dimensions)
        if max_dim >= 6.0:
            score += 2
            indicators.append(f'Very large (up to {max_dim}m)')
        elif max_dim >= 5.0:
            score += 1
            indicators.append(f'Large dimensions ({max_dim}m)')

    # Dwelling designation (with other indicators)
    if 'dwelling' in all_text and score > 0:
        score += 1
        indicators.append('Designated as dwelling')

    # Rectangular/rectilinear with planned layout
    if 'rectangular' in all_text and dimensions and max(dimensions) >= 4.0:
        score += 1
        indicators.append('Rectangular planned layout')

    # Retaining walls or terracing
    if 'retaining wall' in all_text or 'terrac' in all_text:
        score += 1
        indicators.append('Retaining walls/terracing')

    # Masonry (not just hearth)
    if 'masonry' in revised_type.lower():
        score += 1
        indicators.append('Masonry structure')

    return {
        'feature_id': feature_id,
        'score': score,
        'indicators': indicators,
        'description': description,
        'revised_type': revised_type
    }


def main():
    """Identify most substantial buildings."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    print("=" * 80)
    print("MOST SUBSTANTIAL BUILDINGS")
    print("=" * 80)
    print()
    print("Structures with multiple strong indicators of substantial construction")
    print("(Score threshold: ≥3 points)")
    print()

    ng_substantial = []
    rc_substantial = []

    # Analyse Nellie's Glen
    with open(ng_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for record in reader:
            feature_type = record.get('FeatureType', '').lower()
            revised_type = record.get('RevisedFeatureType', '').lower()
            tags = record.get('Tags', '').lower()

            is_structure = ('hearth' in feature_type or 'hearth' in revised_type or
                          'hearth' in tags or 'platform' in feature_type or
                          'platform' in revised_type or 'platform' in tags or
                          'masonry' in feature_type or 'masonry' in revised_type)

            if is_structure:
                assessment = assess_substantial(record)
                if assessment['score'] >= 3:
                    ng_substantial.append(assessment)

    # Analyse Ruined Castle
    with open(rc_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for record in reader:
            feature_type = record.get('FeatureType', '').lower()
            revised_type = record.get('RevisedFeatureType', '').lower()
            tags = record.get('Tags', '').lower()

            is_structure = ('hearth' in feature_type or 'hearth' in revised_type or
                          'hearth' in tags or 'platform' in feature_type or
                          'platform' in revised_type or 'platform' in tags or
                          'masonry' in feature_type or 'masonry' in revised_type)

            if is_structure:
                assessment = assess_substantial(record)
                if assessment['score'] >= 3:
                    rc_substantial.append(assessment)

    # Report Nellie's Glen
    print("=" * 80)
    print("NELLIE'S GLEN")
    print("=" * 80)
    print()

    if ng_substantial:
        # Sort by score
        ng_substantial.sort(key=lambda x: x['score'], reverse=True)

        print(f"Found {len(ng_substantial)} substantial building(s):")
        print()

        for building in ng_substantial:
            print(f"Feature {building['feature_id']} (Score: {building['score']})")
            print(f"  Type: {building['revised_type']}")
            print(f"  Strong indicators:")
            for indicator in building['indicators']:
                print(f"    • {indicator}")
            if building['description']:
                desc = building['description']
                if len(desc) > 180:
                    desc = desc[:180] + '...'
                print(f"  Description: {desc}")
            print()
    else:
        print("No structures meet the threshold for substantial buildings")
        print()

    # Report Ruined Castle
    print("=" * 80)
    print("RUINED CASTLE")
    print("=" * 80)
    print()

    if rc_substantial:
        rc_substantial.sort(key=lambda x: x['score'], reverse=True)

        print(f"Found {len(rc_substantial)} substantial building(s):")
        print()

        for building in rc_substantial:
            print(f"Feature {building['feature_id']} (Score: {building['score']})")
            print(f"  Type: {building['revised_type']}")
            print(f"  Strong indicators:")
            for indicator in building['indicators']:
                print(f"    • {indicator}")
            if building['description']:
                desc = building['description']
                if len(desc) > 180:
                    desc = desc[:180] + '...'
                print(f"  Description: {desc}")
            print()
    else:
        print("No structures meet the threshold for substantial buildings")
        print()

    # Summary
    print("=" * 80)
    print()
    print("SUMMARY:")
    print()
    print(f"  Nellie's Glen: {len(ng_substantial)} substantial buildings")
    print(f"  Ruined Castle: {len(rc_substantial)} substantial buildings")
    print(f"  TOTAL: {len(ng_substantial) + len(rc_substantial)} substantial buildings")
    print()
    print("These represent structures that were likely more permanent dwellings")
    print("with features beyond simple temporary huts (brick construction, mortar,")
    print("complex architecture, substantial walls, or large dimensions).")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
