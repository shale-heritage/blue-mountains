#!/usr/bin/env python3
"""
Script 40: Analyze Primary Hierarchy Structure vs Archive

Comprehensive analysis comparing current consolidated CSV against archived
poly_hierarchy_additions.csv to identify:
1. Getty-aligned primary hierarchies (correctly connected to 7 facets)
2. Orphaned primary hierarchies (should be thematic-only)
3. Missing hierarchies (present in archive but not in current)
4. Unassigned tags (no primary parent)

APPROACH:
- Surgical: Keep what's correct, remove what's wrong, identify gaps
- Preserve thematic Towns hierarchies
- If significant discrepancies, recommend reverting to archive

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


# Getty AAT 7 Primary Facets
GETTY_FACETS = [
    'Agents',
    'Places',
    'Built Environment',
    'Activities',
    'Events',
    'Associated Concepts',
    'Materials',
]


def load_csv(path: Path) -> List[Dict]:
    """Load CSV into list of dicts."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_parent(notes: str) -> Tuple[str, bool, bool]:
    """
    Extract parent from notes.

    Returns:
        (parent_name, is_thematic, is_getty_root)
    """
    if not notes or 'parent=' not in notes:
        return None, False, False

    is_getty_root = '(Getty AAT primary facet)' in notes
    is_thematic = '- THEMATIC' in notes or 'thematic grouping' in notes.lower()

    if is_getty_root or 'parent=(thematic grouping)' in notes:
        return None, is_thematic, is_getty_root

    parent = notes.replace('parent=', '').split(' -')[0].split(' (')[0].strip()
    return parent, is_thematic, is_getty_root


def build_hierarchy_tree(rows: List[Dict]) -> Tuple[Dict, Dict, Set]:
    """
    Build parent-child maps.

    Returns:
        (primary_children, thematic_children, getty_roots)
    """
    primary_children = defaultdict(set)
    thematic_children = defaultdict(set)
    getty_roots = set()

    for row in rows:
        if row['action'] != 'hierarchy':
            continue

        tag = row['old_tag']
        parent, is_thematic, is_getty_root = parse_parent(row['notes'])

        if is_getty_root:
            getty_roots.add(tag)
        elif parent:
            if is_thematic:
                thematic_children[parent].add(tag)
            else:
                primary_children[parent].add(tag)

    return primary_children, thematic_children, getty_roots


def trace_to_getty_root(tag: str, primary_children: Dict, max_depth: int = 20) -> Tuple[bool, List[str]]:
    """
    Trace a tag upwards through primary hierarchy to see if it reaches a Getty root.

    Returns:
        (reaches_getty, path)
    """
    if tag in GETTY_FACETS:
        return True, [tag]

    # Find parents of this tag in primary hierarchy
    parents = []
    for parent, children in primary_children.items():
        if tag in children:
            parents.append(parent)

    if not parents:
        return False, [tag]

    # Recursively check each parent
    for parent in parents:
        if max_depth <= 0:
            return False, [tag]
        reaches, path = trace_to_getty_root(parent, primary_children, max_depth - 1)
        if reaches:
            return True, [tag] + path

    return False, [tag]


def analyze_hierarchies(current_path: Path, archive_path: Path, output_path: Path):
    """Generate comprehensive analysis report."""

    print("=" * 80)
    print("PRIMARY HIERARCHY STRUCTURE ANALYSIS")
    print("=" * 80)
    print()

    # Load data
    print("Loading current consolidated CSV...")
    current_rows = load_csv(current_path)
    print(f"  Loaded {len(current_rows)} rows")

    print("Loading archived poly hierarchy CSV...")
    archive_rows = load_csv(archive_path)
    print(f"  Loaded {len(archive_rows)} rows")
    print()

    # Build hierarchy maps
    print("Building hierarchy maps...")
    current_primary, current_thematic, current_getty = build_hierarchy_tree(current_rows)
    archive_primary, archive_thematic, archive_getty = build_hierarchy_tree(archive_rows)
    print(f"  Current: {len(current_primary)} primary parents, {len(current_getty)} Getty roots")
    print(f"  Archive: {len(archive_primary)} primary parents, {len(archive_getty)} Getty roots")
    print()

    # Identify Getty-connected vs orphaned
    print("Analyzing primary hierarchy connectivity...")
    getty_connected = set()
    orphaned_roots = set()

    for parent in current_primary.keys():
        reaches_getty, path = trace_to_getty_root(parent, current_primary)
        if reaches_getty:
            getty_connected.add(parent)
        else:
            orphaned_roots.add(parent)

    print(f"  Getty-connected primary parents: {len(getty_connected)}")
    print(f"  Orphaned primary roots: {len(orphaned_roots)}")
    print()

    # Compare archive vs current
    print("Comparing archive vs current...")

    # Build relationship sets for comparison
    current_primary_rels = {(row['old_tag'], row['notes']) for row in current_rows
                            if row['action'] == 'hierarchy' and '- THEMATIC' not in row['notes']}
    archive_primary_rels = {(row['old_tag'], row['notes']) for row in archive_rows
                           if row['action'] == 'hierarchy' and '- THEMATIC' not in row['notes']}

    missing_from_current = archive_primary_rels - current_primary_rels
    added_in_current = current_primary_rels - archive_primary_rels

    print(f"  Relationships in archive but missing from current: {len(missing_from_current)}")
    print(f"  Relationships added in current (not in archive): {len(added_in_current)}")
    print()

    # Find unassigned tags
    print("Identifying unassigned tags...")
    all_tags = {row['old_tag'] for row in current_rows}
    tags_with_primary_parent = set()

    for row in current_rows:
        if row['action'] == 'hierarchy':
            parent, is_thematic, is_getty_root = parse_parent(row['notes'])
            if parent and not is_thematic:
                tags_with_primary_parent.add(row['old_tag'])

    unassigned_tags = all_tags - tags_with_primary_parent - current_getty
    print(f"  Tags without primary parent: {len(unassigned_tags)}")
    print()

    # Write report
    print(f"Writing analysis report to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Primary Hierarchy Structure Analysis\n\n")
        f.write(f"**Generated:** 2025-10-24\n")
        f.write(f"**Current CSV:** {current_path}\n")
        f.write(f"**Archive CSV:** {archive_path}\n\n")

        f.write("## Executive Summary\n\n")
        f.write(f"- **Current Getty roots:** {len(current_getty)} (target: 7)\n")
        f.write(f"- **Getty-connected primary parents:** {len(getty_connected)}\n")
        f.write(f"- **Orphaned primary roots:** {len(orphaned_roots)}\n")
        f.write(f"- **Missing from current (vs archive):** {len(missing_from_current)}\n")
        f.write(f"- **Added in current (not in archive):** {len(added_in_current)}\n")
        f.write(f"- **Unassigned tags (no primary parent):** {len(unassigned_tags)}\n\n")

        # Decision recommendation
        if len(missing_from_current) > 50:
            f.write("## ⚠️ RECOMMENDATION: REVERT TO ARCHIVE\n\n")
            f.write(f"Found {len(missing_from_current)} missing relationships from archive. ")
            f.write("Recommend reverting to archived poly_hierarchy_additions.csv and ")
            f.write("working from there.\n\n")
        else:
            f.write("## ✓ RECOMMENDATION: FIX CURRENT\n\n")
            f.write(f"Found {len(missing_from_current)} missing relationships - manageable. ")
            f.write("Recommend surgical fixes to current structure.\n\n")

        f.write("---\n\n")

        # Section 1: Current Getty Roots
        f.write("## Section 1: Current Getty AAT Roots\n\n")
        if current_getty:
            for root in sorted(current_getty):
                f.write(f"- {root}\n")
        else:
            f.write("*No Getty roots found - need to add 7 Getty AAT root entries*\n")
        f.write("\n")

        # Section 2: Getty-Connected Primary Hierarchies
        f.write("## Section 2: Getty-Connected Primary Hierarchies (KEEP)\n\n")
        f.write("These primary hierarchies correctly connect to Getty AAT roots.\n\n")

        for getty_facet in GETTY_FACETS:
            connected_to_this_facet = []
            for parent in sorted(getty_connected):
                reaches_getty, path = trace_to_getty_root(parent, current_primary)
                if reaches_getty and getty_facet in path:
                    connected_to_this_facet.append((parent, path))

            if connected_to_this_facet:
                f.write(f"### {getty_facet}\n\n")
                for parent, path in connected_to_this_facet[:10]:  # Limit to 10 per facet for brevity
                    f.write(f"- `{parent}` (path: {' > '.join(reversed(path))})\n")
                if len(connected_to_this_facet) > 10:
                    f.write(f"- ... and {len(connected_to_this_facet) - 10} more\n")
                f.write("\n")

        # Section 3: Orphaned Primary Hierarchies
        f.write("## Section 3: Orphaned Primary Hierarchies (REMOVE)\n\n")
        f.write("These primary parents don't connect to any Getty root. ")
        f.write("**ACTION:** Remove these PRIMARY parent relationships ")
        f.write("(keep thematic if exists).\n\n")

        for root in sorted(orphaned_roots):
            children = current_primary[root]
            f.write(f"**{root}** ({len(children)} children)\n")
            sample = list(sorted(children))[:5]
            f.write(f"  Children: {', '.join(sample)}")
            if len(children) > 5:
                f.write(f" ... and {len(children) - 5} more")
            f.write("\n\n")

        # Section 4: Missing from Current
        f.write("## Section 4: Missing Hierarchies (in Archive, not in Current)\n\n")
        f.write("These relationships existed in archived poly_hierarchy_additions.csv ")
        f.write("but are missing from current consolidated CSV.\n\n")

        if len(missing_from_current) == 0:
            f.write("*No missing relationships - all archive content preserved!*\n\n")
        else:
            # Group by parent for readability
            missing_by_parent = defaultdict(list)
            for tag, notes in sorted(missing_from_current):
                parent = notes.replace('parent=', '').split(' -')[0].split(' (')[0].strip()
                missing_by_parent[parent].append((tag, notes))

            for parent in sorted(missing_by_parent.keys())[:20]:  # Show first 20 parents
                entries = missing_by_parent[parent]
                f.write(f"**Parent: {parent}** ({len(entries)} missing children)\n")
                for tag, notes in entries[:5]:  # Show first 5 children
                    f.write(f"  - {tag} → {notes}\n")
                if len(entries) > 5:
                    f.write(f"  - ... and {len(entries) - 5} more\n")
                f.write("\n")

            if len(missing_by_parent) > 20:
                f.write(f"*... and {len(missing_by_parent) - 20} more parents with missing children*\n\n")

        # Section 5: Unassigned Tags
        f.write("## Section 5: Unassigned Tags (No Primary Parent)\n\n")
        f.write("These tags have no primary hierarchy parent. ")
        f.write("Need manual assignment to Getty facets.\n\n")

        if len(unassigned_tags) == 0:
            f.write("*No unassigned tags - all tags have primary parents!*\n\n")
        else:
            for tag in sorted(unassigned_tags)[:50]:  # Show first 50
                # Check if has thematic parent
                thematic_parents = []
                for parent, children in current_thematic.items():
                    if tag in children:
                        thematic_parents.append(parent)

                f.write(f"**{tag}**\n")
                if thematic_parents:
                    f.write(f"  Thematic parents: {', '.join(thematic_parents)}\n")
                f.write("  **Assign to Getty facet:** _______________\n\n")

            if len(unassigned_tags) > 50:
                f.write(f"*... and {len(unassigned_tags) - 50} more unassigned tags*\n\n")

        f.write("---\n\n")
        f.write("## Next Steps\n\n")

        if len(missing_from_current) > 50:
            f.write("### Option A: REVERT TO ARCHIVE (Recommended)\n\n")
            f.write("1. Backup current tag_map_consolidated.csv\n")
            f.write("2. Replace with archived poly_hierarchy_additions.csv\n")
            f.write("3. Add Towns thematic hierarchies\n")
            f.write("4. Regenerate visualizations\n\n")

        f.write("### Option B: FIX CURRENT\n\n")
        f.write("1. Remove orphaned primary hierarchies (Section 3)\n")
        f.write("2. Add missing hierarchies from archive (Section 4)\n")
        f.write("3. Assign unassigned tags (Section 5)\n")
        f.write("4. Regenerate visualizations\n")

    print("✓ Analysis report generated")
    print()
    print("=" * 80)
    print("REVIEW THE REPORT")
    print("=" * 80)
    print()
    print(f"Report: {output_path}")
    print()
    print("Decision points:")
    print(f"1. If {len(missing_from_current)} missing relationships is too many → REVERT")
    print(f"2. If manageable → FIX current structure")
    print()


def main():
    """Main execution."""
    current_path = Path('data/tag_map_consolidated.csv')
    archive_path = Path('archive/csv-files/poly_hierarchy_additions.csv')
    output_path = Path('reports/primary_structure_analysis.md')

    if not current_path.exists():
        print(f"ERROR: {current_path} not found")
        return 1

    if not archive_path.exists():
        print(f"ERROR: {archive_path} not found")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    analyze_hierarchies(current_path, archive_path, output_path)

    return 0


if __name__ == '__main__':
    main()
