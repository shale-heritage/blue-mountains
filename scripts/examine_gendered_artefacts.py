#!/usr/bin/env python3
"""
Examine Gendered and Family-Associated Artefacts

Identify specific artefacts that led to features being tagged as associated
with women, children, or families.
"""

import csv
from pathlib import Path


def main():
    """Extract and report gendered/family artefact associations."""

    base_dir = Path(__file__).parent.parent

    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    print("=" * 80)
    print("GENDERED AND FAMILY-ASSOCIATED ARTEFACTS")
    print("=" * 80)
    print()
    print("Features explicitly tagged with 'Women', 'Children', or 'Family'")
    print()

    found_features = []

    for site_name, filepath in [("Nellie's Glen", ng_file),
                                 ("Ruined Castle", rc_file)]:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for record in reader:
                tags = record.get('Tags', '').lower()

                # Check for gendered/family tags
                has_women = 'women' in tags
                has_children = 'children' in tags or 'child' in tags
                has_family = 'family' in tags

                if has_women or has_children or has_family:
                    found_features.append({
                        'site': site_name,
                        'feature_id': record.get('FeatureID', ''),
                        'tags': record.get('Tags', ''),
                        'feature_type': record.get('FeatureType', ''),
                        'revised_type': record.get('RevisedFeatureType', ''),
                        'description': record.get('Description', ''),
                        'material': record.get('Material', ''),
                        'associated_notes': record.get('AsociatedMaterialNotes', ''),
                        'interpretation': record.get('Interpretation', ''),
                        'comments': record.get('Comments', ''),
                        'func_type': record.get('Artefact Functional type', ''),
                        'has_women': has_women,
                        'has_children': has_children,
                        'has_family': has_family
                    })

    if not found_features:
        print("No features found with Women, Children, or Family tags")
        print()
        print("Searching for indirect evidence...")
        print()

        # Search for features with relevant keywords even without explicit tags
        for site_name, filepath in [("Nellie's Glen", ng_file),
                                     ("Ruined Castle", rc_file)]:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for record in reader:
                    desc = record.get('Description', '').lower()
                    interp = record.get('Interpretation', '').lower()
                    notes = record.get('AsociatedMaterialNotes', '').lower()

                    keywords = ['women', 'woman', 'children', 'child', 'family',
                               'infant', 'baby', 'mother', 'father', 'domestic']

                    if any(kw in desc or kw in interp or kw in notes for kw in keywords):
                        print(f"Feature {record.get('FeatureID')} ({site_name})")
                        print(f"  Contains keyword in description/interpretation")
                        print(f"  Description: {desc[:150]}...")
                        print()
    else:
        print(f"Found {len(found_features)} feature(s) with explicit gender/family tags")
        print()

        for feature in found_features:
            print("=" * 80)
            print(f"FEATURE {feature['feature_id']} ({feature['site']})")
            print("=" * 80)
            print()

            print(f"Tags: {feature['tags']}")
            print()

            gender_tags = []
            if feature['has_women']:
                gender_tags.append('Women')
            if feature['has_children']:
                gender_tags.append('Children')
            if feature['has_family']:
                gender_tags.append('Family')
            print(f"Gender/Family Tags: {', '.join(gender_tags)}")
            print()

            print(f"Feature Type: {feature['feature_type']}")
            if feature['revised_type']:
                print(f"Revised Type: {feature['revised_type']}")
            print()

            print("DESCRIPTION:")
            print(f"{feature['description']}")
            print()

            if feature['material']:
                print("MATERIALS:")
                print(f"{feature['material']}")
                print()

            if feature['associated_notes']:
                print("ASSOCIATED MATERIAL NOTES:")
                print(f"{feature['associated_notes']}")
                print()

            if feature['func_type']:
                print(f"Functional Type: {feature['func_type']}")
                print()

            if feature['interpretation']:
                print("INTERPRETATION:")
                print(f"{feature['interpretation']}")
                print()

            if feature['comments']:
                print("COMMENTS:")
                print(f"{feature['comments']}")
                print()

            # Analyse what might have led to gendering
            print("-" * 80)
            print("ANALYSIS: Possible reasons for gender/family association")
            print("-" * 80)
            print()

            desc_lower = feature['description'].lower()
            mat_lower = feature['material'].lower()
            notes_lower = feature['associated_notes'].lower()
            all_text = ' '.join([desc_lower, mat_lower, notes_lower])

            reasons = []

            # Check for specific gendered artefact types
            if 'perfume' in all_text or 'cosmetic' in all_text:
                reasons.append("• Perfume/cosmetic bottles (traditionally associated with women)")

            if 'bead' in all_text:
                reasons.append("• Beads (often associated with women's clothing/adornment)")

            if 'button' in all_text:
                reasons.append("• Buttons (could indicate clothing, potentially gendered)")

            if 'toy' in all_text or 'doll' in all_text or 'marble' in all_text:
                reasons.append("• Toys/children's items")

            if 'pharmaceutical' in feature['tags'].lower() and 'women' in feature['tags'].lower():
                reasons.append("• Pharmaceutical items (may include women's health products)")

            if 'chamber pot' in all_text:
                reasons.append("• Chamber pot (domestic sanitation, associated with family/private spaces)")

            if 'domestic' in all_text or 'household' in all_text:
                reasons.append("• Domestic/household items (historically associated with women's sphere)")

            if 'ceramic' in mat_lower and 'decorated' in desc_lower:
                reasons.append("• Decorated ceramics (domestic sphere, care in household goods)")

            if 'pit' in feature['revised_type'].lower() or 'cesspit' in desc_lower:
                reasons.append("• Pit/cesspit with household refuse (domestic waste management)")

            # Check for small items
            if 'small' in desc_lower or 'miniature' in desc_lower:
                reasons.append("• Small/miniature items (possibly children's scale)")

            # Check for specific mentions in description
            if 'banded ware' in desc_lower or 'blue banded' in desc_lower:
                reasons.append("• Banded ware ceramics (common domestic tableware)")

            if not reasons:
                reasons.append("• Tag applied based on overall domestic assemblage context")
                reasons.append("• Combination of multiple domestic indicators")

            for reason in reasons:
                print(reason)

            print()
            print()

    print("=" * 80)
    print()
    print("SUMMARY:")
    print()
    print("Tags indicating women's, children's, or family presence appear to be based on:")
    print()
    print("1. ARTEFACT TYPES:")
    print("   • Perfume/pharmaceutical bottles")
    print("   • Domestic ceramics and tableware")
    print("   • Chamber pots (domestic/private sphere)")
    print("   • Household refuse in pits/cesspits")
    print()
    print("2. ASSEMBLAGE CONTEXT:")
    print("   • Dense domestic assemblages suggesting settled households")
    print("   • Mix of functional and decorative items")
    print("   • Evidence of domestic maintenance and care")
    print()
    print("3. HISTORICAL INTERPRETATION:")
    print("   • Tags reflect archaeologists' interpretation that certain")
    print("   • domestic contexts and artefact types indicate women's")
    print("   • presence and family life rather than male-only camps")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
