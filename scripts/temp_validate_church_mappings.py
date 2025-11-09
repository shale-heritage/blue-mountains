#!/usr/bin/env python3
"""
Validate church disambiguation tag mappings.

Checks that all tags in the church disambiguation mappings exist in the taxonomy.
Reports any missing tags and suggests corrections.
"""

import csv
from pathlib import Path
from typing import List, Set, Dict
from difflib import get_close_matches

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"
MAPPING_CSV = BASE_DIR / "data" / "tag_application_mapping.csv"


def load_taxonomy() -> Set[str]:
    """Load all tags from taxonomy."""
    tags = set()
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Add both old_tag and new_tag (synonyms map to new_tag)
            tags.add(row['old_tag'])
            tags.add(row['new_tag'])
    return tags


def load_church_mappings() -> List[Dict[str, str]]:
    """Load church disambiguation mappings."""
    mappings = []
    with open(MAPPING_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['source'] == 'church_disambiguation_report':
                mappings.append(row)
    return mappings


def extract_tags_from_mappings(mappings: List[Dict[str, str]]) -> Set[str]:
    """Extract all unique tags from mappings."""
    tags = set()
    for mapping in mappings:
        # Extract tags from add_tags field (pipe-delimited)
        if mapping['add_tags']:
            tag_list = [t.strip() for t in mapping['add_tags'].split('|')]
            tags.update(tag_list)
    return tags


def validate_tags(tags_to_check: Set[str], taxonomy_tags: Set[str]) -> tuple[Set[str], Dict[str, List[str]]]:
    """
    Validate tags against taxonomy.

    Returns:
        Tuple of (missing_tags, suggestions)
        - missing_tags: Set of tags not found in taxonomy
        - suggestions: Dict mapping missing tag to list of similar tags
    """
    missing = set()
    suggestions = {}

    for tag in tags_to_check:
        if tag not in taxonomy_tags:
            missing.add(tag)
            # Find similar tags
            similar = get_close_matches(tag, taxonomy_tags, n=3, cutoff=0.6)
            if similar:
                suggestions[tag] = similar

    return missing, suggestions


def main():
    """Main validation."""
    print("Church Disambiguation - Tag Validation")
    print("=" * 60)
    print()

    # Load taxonomy
    print("Loading taxonomy...")
    taxonomy_tags = load_taxonomy()
    print(f"✓ Loaded {len(taxonomy_tags)} tags from taxonomy")
    print()

    # Load church mappings
    print("Loading church disambiguation mappings...")
    mappings = load_church_mappings()
    print(f"✓ Loaded {len(mappings)} church mappings")
    print()

    # Extract unique tags
    print("Extracting tags from mappings...")
    tags_to_check = extract_tags_from_mappings(mappings)
    print(f"✓ Found {len(tags_to_check)} unique tags to validate")
    print()

    # Validate
    print("Validating tags against taxonomy...")
    missing, suggestions = validate_tags(tags_to_check, taxonomy_tags)

    if not missing:
        print("✓ All tags exist in taxonomy!")
        print()
        print("=" * 60)
        print("✓ Validation passed - ready to apply mappings")
        return

    # Report missing tags
    print()
    print("=" * 60)
    print(f"⚠ VALIDATION FAILED: {len(missing)} tags not found in taxonomy")
    print("=" * 60)
    print()

    # Categorize missing tags
    clergy_tags = [t for t in missing if 'Rev' in t or 'Cardinal' in t or 'Archbishop' in t or 'Canon' in t or 'Father' in t]
    church_tags = [t for t in missing if 'Church' in t or 'Chapel' in t]
    other_tags = [t for t in missing if t not in clergy_tags and t not in church_tags]

    if clergy_tags:
        print("MISSING CLERGY TAGS:")
        print("-" * 60)
        for tag in sorted(clergy_tags):
            print(f"  • {tag}")
            if tag in suggestions:
                print(f"    Similar tags: {', '.join(suggestions[tag])}")
        print()

    if church_tags:
        print("MISSING CHURCH TAGS:")
        print("-" * 60)
        for tag in sorted(church_tags):
            print(f"  • {tag}")
            if tag in suggestions:
                print(f"    Similar tags: {', '.join(suggestions[tag])}")
        print()

    if other_tags:
        print("MISSING OTHER TAGS:")
        print("-" * 60)
        for tag in sorted(other_tags):
            print(f"  • {tag}")
            if tag in suggestions:
                print(f"    Similar tags: {', '.join(suggestions[tag])}")
        print()

    print("=" * 60)
    print("NEXT STEPS:")
    print("-" * 60)
    print("1. Add missing tags to taxonomy (especially clergy)")
    print("2. Fix any typos in tag names")
    print("3. Re-run validation to confirm all tags exist")


if __name__ == '__main__':
    main()
