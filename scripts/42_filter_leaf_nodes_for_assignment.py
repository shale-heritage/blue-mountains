#!/usr/bin/env python3
"""
Script 42: Filter Leaf Nodes for Assignment

Filters the 157 unassigned tags to identify actual leaf nodes (tags applied to items)
vs intermediate organizational groups. Separates individual people for People thematic
hierarchy and provides focused list of remaining tags for manual Getty facet assignment.

Strategy:
1. Load CSV and identify which tags are actually used on items (action != 'hierarchy')
2. From unassigned list, filter to only leaf nodes
3. Identify people (Mr/Mrs/Miss names) → prepare for People thematic hierarchy
4. Exclude thematic grouping roots (keep as thematic-only)
5. Output focused assignment list for remaining leaf nodes

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import List, Set, Dict, Tuple


def load_csv(path: Path) -> List[Dict]:
    """Load CSV into list of dicts."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def is_person_name(tag: str) -> bool:
    """Check if tag is an individual person name."""
    prefixes = ['Mr ', 'Mrs ', 'Miss ', 'Ms ']
    return any(tag.startswith(prefix) for prefix in prefixes)


def is_thematic_root(tag: str) -> bool:
    """Check if tag is a thematic grouping root that should remain thematic-only."""
    thematic_roots = {
        'Alcohol & Temperance',
        'Arts & Culture',
        'Communications & Postal Services',
        'Community institutions',
        'Economy & Labour',
        'Environment & Weather',
        'Family & Domestic Life',
        'Health & Medicine',
        'Justice & Crime',
        'Military & War',
        'Mining & Industry',
        'Politics & Governance',
        'Race & Ethnicity',
        'Religion',
        'Social issues',
        'Sport & Recreation',
        'Tourism & Accommodation',
        'Transport & Infrastructure',
        'Women & Gender',
    }
    return tag in thematic_roots


def analyze_and_filter(csv_path: Path, unassigned_report_path: Path, output_report_path: Path):
    """Analyze unassigned tags and generate filtered assignment list."""

    print("=" * 80)
    print("LEAF NODE FILTERING FOR ASSIGNMENT")
    print("=" * 80)
    print()

    # Load CSV
    print(f"Loading {csv_path}...")
    rows = load_csv(csv_path)
    print(f"  Loaded {len(rows)} rows")
    print()

    # Identify tags used on items (leaf nodes)
    print("Identifying leaf nodes (tags applied to items)...")
    leaf_nodes = set()
    hierarchy_only_tags = set()

    for row in rows:
        tag = row['old_tag']
        action = row['action']

        if action == 'hierarchy':
            hierarchy_only_tags.add(tag)
        else:
            # Any non-hierarchy action means this tag is applied to items
            leaf_nodes.add(tag)

    print(f"  Tags used on items (leaf nodes): {len(leaf_nodes)}")
    print(f"  Tags only used in hierarchy: {len(hierarchy_only_tags)}")
    print()

    # Load unassigned tags from report
    print(f"Loading unassigned tags from {unassigned_report_path}...")
    unassigned_tags = set()
    with open(unassigned_report_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('**') and not line.startswith('**Generated'):
                # Extract tag name between ** markers
                tag = line.strip().replace('**', '').split('\n')[0]
                if tag and tag != 'Assign to Getty facet path:':
                    unassigned_tags.add(tag)

    print(f"  Found {len(unassigned_tags)} unassigned tags")
    print()

    # Categorize unassigned tags
    print("Categorizing unassigned tags...")

    people = []
    thematic_roots = []
    leaf_unassigned = []
    intermediate_only = []

    for tag in sorted(unassigned_tags):
        if is_person_name(tag):
            people.append(tag)
        elif is_thematic_root(tag):
            thematic_roots.append(tag)
        elif tag in leaf_nodes:
            # This tag is actually applied to items
            leaf_unassigned.append(tag)
        else:
            # Only used as intermediate hierarchy node
            intermediate_only.append(tag)

    print(f"  People (Mr/Mrs/Miss names): {len(people)}")
    print(f"  Thematic roots (keep thematic-only): {len(thematic_roots)}")
    print(f"  Leaf nodes needing assignment: {len(leaf_unassigned)}")
    print(f"  Intermediate-only (skip assignment): {len(intermediate_only)}")
    print()

    # Build thematic parent map for context
    print("Building thematic parent map...")
    thematic_parents = defaultdict(set)
    for row in rows:
        if row['action'] == 'hierarchy' and '- THEMATIC' in row.get('notes', ''):
            tag = row['old_tag']
            notes = row['notes']
            if 'parent=' in notes:
                parent = notes.replace('parent=', '').split(' -')[0].strip()
                thematic_parents[tag].add(parent)
    print(f"  Mapped {len(thematic_parents)} tags to thematic parents")
    print()

    # Generate output report
    print(f"Writing filtered assignment report to {output_report_path}...")
    with open(output_report_path, 'w', encoding='utf-8') as f:
        f.write("# Filtered Leaf Nodes for Getty Facet Assignment\n\n")
        f.write("**Generated:** 2025-10-24\n")
        f.write(f"**Original unassigned:** 157\n")
        f.write(f"**Leaf nodes needing assignment:** {len(leaf_unassigned)}\n\n")
        f.write("This filtered list contains only tags that are actually applied to items\n")
        f.write("and need primary Getty facet assignment.\n\n")
        f.write("---\n\n")

        # Section 1: People (for thematic hierarchy)
        f.write("## Section 1: Individual People\n\n")
        f.write(f"**Count:** {len(people)} individual people\n\n")
        f.write("These should be added to the **People thematic hierarchy**:\n")
        f.write("- People → parent=(thematic grouping)\n")
        f.write("- [Each person] → parent=People - THEMATIC\n\n")
        f.write("These individuals should remain under their occupations in the PRIMARY hierarchy\n")
        f.write("(e.g., Agents > Occupations > Miners > Mr John Smith).\n\n")

        if len(people) > 0:
            f.write("**People to add to thematic hierarchy:**\n")
            for person in people[:20]:  # Show first 20
                f.write(f"- {person}\n")
            if len(people) > 20:
                f.write(f"- ... and {len(people) - 20} more\n")
        f.write("\n---\n\n")

        # Section 2: Thematic roots (keep as-is)
        f.write("## Section 2: Thematic Grouping Roots\n\n")
        f.write(f"**Count:** {len(thematic_roots)}\n\n")
        f.write("These are top-level thematic groupings and should remain **thematic-only**.\n")
        f.write("No primary parent assignment needed.\n\n")
        if len(thematic_roots) > 0:
            for root in thematic_roots:
                f.write(f"- {root}\n")
        f.write("\n---\n\n")

        # Section 3: Intermediate-only tags (skip)
        f.write("## Section 3: Intermediate Organizational Groups\n\n")
        f.write(f"**Count:** {len(intermediate_only)}\n\n")
        f.write("These are only used as intermediate hierarchy nodes, not applied to items.\n")
        f.write("They will inherit primary parents from their children - no assignment needed.\n\n")
        if len(intermediate_only) > 0:
            for tag in intermediate_only[:20]:  # Show first 20
                f.write(f"- {tag}\n")
            if len(intermediate_only) > 20:
                f.write(f"- ... and {len(intermediate_only) - 20} more\n")
        f.write("\n---\n\n")

        # Section 4: Leaf nodes needing assignment
        f.write("## Section 4: Leaf Nodes Needing Getty Facet Assignment\n\n")
        f.write(f"**Count:** {len(leaf_unassigned)}\n\n")
        f.write("These tags are applied to items and need primary Getty facet assignment.\n\n")
        f.write("**Getty AAT Primary Facets:**\n")
        f.write("1. Agents\n")
        f.write("2. Places\n")
        f.write("3. Built Environment\n")
        f.write("4. Activities\n")
        f.write("5. Events\n")
        f.write("6. Associated Concepts\n")
        f.write("7. Materials\n\n")
        f.write("---\n\n")

        for tag in leaf_unassigned:
            f.write(f"**{tag}**\n")

            # Show thematic parents for context
            if tag in thematic_parents and thematic_parents[tag]:
                parents = sorted(thematic_parents[tag])
                f.write(f"  Thematic context: {', '.join(parents)}\n")

            # Check if used on items
            if tag in leaf_nodes:
                f.write("  Status: ✓ Applied to items (leaf node)\n")

            f.write("  **Assign to Getty facet path:** _______________\n\n")

    print(f"  ✓ Filtered report written")
    print()

    # Generate People thematic hierarchy CSV entries
    people_csv_path = Path('data/people_thematic_hierarchy.csv')
    print(f"Generating People thematic hierarchy CSV: {people_csv_path}...")

    with open(people_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['old_tag', 'new_tag', 'action', 'notes'])

        # Add People thematic root
        writer.writerow(['People', 'People', 'hierarchy', 'parent=(thematic grouping)'])

        # Add each person under People - THEMATIC
        for person in sorted(people):
            writer.writerow([person, person, 'hierarchy', f'parent=People - THEMATIC'])

    print(f"  ✓ Written {len(people) + 1} entries (1 root + {len(people)} people)")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Original unassigned tags: 157")
    print()
    print(f"✓ {len(people)} people → Add to People thematic hierarchy")
    print(f"✓ {len(thematic_roots)} thematic roots → Keep thematic-only (no action needed)")
    print(f"✓ {len(intermediate_only)} intermediate groups → Skip (inherit from children)")
    print(f"✓ {len(leaf_unassigned)} leaf nodes → Manual Getty facet assignment needed")
    print()
    print(f"Focused assignment list: {output_report_path}")
    print(f"People thematic CSV: {people_csv_path}")
    print()
    print("Next steps:")
    print(f"1. Review and append {people_csv_path} to tag_map_consolidated.csv")
    print(f"2. Manually assign {len(leaf_unassigned)} leaf nodes to Getty facets")
    print(f"3. Regenerate visualizations")
    print()


def main():
    """Main execution."""
    csv_path = Path('data/tag_map_consolidated.csv')
    unassigned_report_path = Path('reports/unassigned_tags_for_manual_assignment.md')
    output_report_path = Path('reports/leaf_nodes_for_assignment.md')

    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return 1

    if not unassigned_report_path.exists():
        print(f"ERROR: {unassigned_report_path} not found")
        return 1

    output_report_path.parent.mkdir(parents=True, exist_ok=True)

    analyze_and_filter(csv_path, unassigned_report_path, output_report_path)

    return 0


if __name__ == '__main__':
    exit(main())
