#!/usr/bin/env python3
"""
Script 58: Detect Duplicate Leaf Nodes

Detects duplicate leaf node terms in the taxonomy hierarchy to identify potential
data quality issues.

A duplicate leaf node is a term that appears multiple times in the hierarchy with
different parent relationships. This could indicate:

1. Legitimate polyhierarchy (same entity in multiple facets)
2. Data quality issue (unintended duplication)
3. Disambiguation needed (different entities with same name)

The script distinguishes between:
- Expected duplicates (polyhierarchical relationships like Schools of Arts)
- Suspicious duplicates (likely data quality issues)

Author: Claude Code
Date: 2025-11-17
"""

import csv
from pathlib import Path
from collections import defaultdict


def extract_hierarchy_entries(csv_path: Path) -> dict:
    """
    Extract all hierarchy entries from CSV.

    Returns: dict mapping term -> list of parent relationships
    """
    hierarchy = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['action'] == 'hierarchy' and row['status'] == 'active':
                term = row['new_tag']
                # Extract parent from notes field
                notes = row['notes']
                if notes.startswith('parent='):
                    # Extract parent (before any THEMATIC marker or parentheticals)
                    parent_full = notes[7:]  # Strip 'parent='

                    # Parse parent (strip markers)
                    import re
                    match = re.search(r'(.+?)(?:\s*-\s*THEMATIC)?(?:\s*\([^)]*\))?$', parent_full)
                    if match:
                        parent = match.group(1).strip()
                        hierarchy[term].append(parent)

    return hierarchy


def categorize_duplicates(hierarchy: dict) -> dict:
    """
    Categorize duplicate leaf nodes.

    Returns: dict with categories:
    - expected: Known polyhierarchical relationships
    - suspicious: Likely data quality issues
    - single: No duplicates (single parent)
    """
    categories = {
        'expected': [],
        'suspicious': [],
        'single': []
    }

    # Expected polyhierarchical patterns (from CLAUDE.md)
    EXPECTED_POLYHIERARCHY = {
        # Dual-nature entities (building + organisation)
        '(building)', '(organisation)', '(business)', '(venue)',

        # Thematic vs structural facets
        'THEMATIC',
    }

    for term, parents in hierarchy.items():
        if len(parents) == 1:
            categories['single'].append((term, parents))
        elif len(parents) > 1:
            # Check if this is expected polyhierarchy
            is_expected = False

            # Check for disambiguation qualifiers in term
            if any(qualifier in term for qualifier in ['(building)', '(organisation)',
                                                        '(business)', '(venue)']):
                # Qualified terms should NOT have multiple parents
                # (each qualifier creates a separate entity)
                is_expected = False
                categories['suspicious'].append((term, parents))
                continue

            # Check if parents are in different facets (legitimate polyhierarchy)
            # Common polyhierarchical entities from project
            polyhierarchical_entities = [
                'school of arts',  # Can be both building and organisation
                'schools of arts',
                'church',  # Generic - can be both
                'churches',
                'hall',
                'halls',
                'lodge',
                'lodges',
            ]

            if term.lower() in polyhierarchical_entities:
                is_expected = True
                categories['expected'].append((term, parents))
            else:
                categories['suspicious'].append((term, parents))

    return categories


def main():
    """Detect duplicate leaf nodes in taxonomy."""
    csv_path = Path('data/tag_map_consolidated.csv')
    output_path = Path('reports/duplicate_leaf_nodes.md')

    print("="*80)
    print("DUPLICATE LEAF NODE DETECTION")
    print("="*80)
    print()

    # Extract hierarchy
    print("Extracting hierarchy entries...")
    hierarchy = extract_hierarchy_entries(csv_path)
    print(f"Found {len(hierarchy)} unique terms in hierarchy")
    print()

    # Categorize duplicates
    print("Categorizing duplicates...")
    categories = categorize_duplicates(hierarchy)
    print()

    # Count by category
    expected_count = len(categories['expected'])
    suspicious_count = len(categories['suspicious'])
    single_count = len(categories['single'])

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total terms: {len(hierarchy)}")
    print(f"Single parent (no duplicates): {single_count}")
    print(f"Expected polyhierarchy: {expected_count}")
    print(f"Suspicious duplicates: {suspicious_count}")
    print()

    # Write detailed report
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Duplicate Leaf Node Detection Report\n\n")
        f.write("**Generated:** 2025-11-17\n")
        f.write(f"**Source:** `{csv_path}`\n\n")
        f.write("---\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Total terms in hierarchy:** {len(hierarchy)}\n")
        f.write(f"- **Single parent (no duplicates):** {single_count}\n")
        f.write(f"- **Expected polyhierarchy:** {expected_count}\n")
        f.write(f"- **Suspicious duplicates:** {suspicious_count}\n\n")
        f.write("---\n\n")

        # Expected polyhierarchy section
        f.write("## Expected Polyhierarchy\n\n")
        f.write("Terms that legitimately appear in multiple facets:\n\n")

        if categories['expected']:
            for term, parents in sorted(categories['expected']):
                f.write(f"### {term}\n\n")
                f.write("Parents:\n")
                for parent in sorted(parents):
                    f.write(f"- {parent}\n")
                f.write("\n")
        else:
            f.write("*None found*\n\n")

        f.write("---\n\n")

        # Suspicious duplicates section
        f.write("## Suspicious Duplicates\n\n")
        f.write("Terms with multiple parents that may indicate data quality issues:\n\n")

        if categories['suspicious']:
            for term, parents in sorted(categories['suspicious']):
                f.write(f"### {term}\n\n")
                f.write("Parents:\n")
                for parent in sorted(parents):
                    f.write(f"- {parent}\n")
                f.write("\n**Action needed:** Review and determine if:\n")
                f.write("1. This is legitimate polyhierarchy (document in CLAUDE.md)\n")
                f.write("2. This is a data quality issue (consolidate or disambiguate)\n")
                f.write("3. This needs qualification (add parenthetical qualifiers)\n\n")
        else:
            f.write("✓ *No suspicious duplicates found!*\n\n")

        f.write("---\n\n")

        # Methodology section
        f.write("## Methodology\n\n")
        f.write("**Expected polyhierarchy:** Terms known to legitimately span multiple facets:\n")
        f.write("- Schools of Arts (building + organisation)\n")
        f.write("- Churches (building + organisation)\n")
        f.write("- Halls (building + organisation)\n")
        f.write("- Lodges (building + organisation)\n\n")

        f.write("**Suspicious duplicates:** All other terms with multiple parents\n\n")

        f.write("**Note:** Terms with disambiguation qualifiers (building), (organisation), ")
        f.write("(business), (venue) should NOT have multiple parents. Each qualifier creates ")
        f.write("a separate entity with a single parent.\n\n")

    print(f"Detailed report written to: {output_path}")
    print()

    # Show suspicious duplicates if any
    if categories['suspicious']:
        print("="*80)
        print("⚠ SUSPICIOUS DUPLICATES FOUND")
        print("="*80)
        print()
        print(f"Found {suspicious_count} terms with multiple parents that need review:")
        print()
        for term, parents in sorted(categories['suspicious'])[:10]:
            print(f"  • {term}")
            for parent in sorted(parents):
                print(f"    - parent: {parent}")
            print()

        if suspicious_count > 10:
            print(f"  ... and {suspicious_count - 10} more")
            print()

        print("See full report: reports/duplicate_leaf_nodes.md")
        print()
    else:
        print("="*80)
        print("✓ NO SUSPICIOUS DUPLICATES")
        print("="*80)
        print()
        print("All duplicate leaf nodes are expected polyhierarchical relationships.")
        print()

    # Show expected polyhierarchy
    if categories['expected']:
        print("Expected polyhierarchical terms:")
        for term, parents in sorted(categories['expected']):
            print(f"  ✓ {term} ({len(parents)} parents)")
        print()


if __name__ == '__main__':
    main()
