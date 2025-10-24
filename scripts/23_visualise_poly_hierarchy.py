#!/usr/bin/env python3
"""
Script 23: Visualise Poly-Hierarchical Taxonomy Structure

Generates ASCII tree diagrams for all primary facets and thematic groupings.

Reads from: data/tag_map_consolidated.csv (single source of truth)
Outputs to: visualizations/hierarchy_trees/

Author: Claude Code
Date: 2025-10-20 (Updated: 2025-10-24 to use consolidated CSV)
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def parse_parent_from_notes(notes: str) -> Tuple[str, bool]:
    """
    Extract parent tag name from notes field.

    Args:
        notes: Notes field from CSV (e.g., "parent=Agents (new top-level facet)")

    Returns:
        Tuple of (parent_name, is_thematic)

    Examples:
        "parent=Agents (new top-level facet)" -> ("Agents", False)
        "parent=Health & Medicine - THEMATIC" -> ("Health & Medicine", True)
        "parent=Occupations" -> ("Occupations", False)
    """
    # Extract parent name from notes field
    # Pattern: parent=NAME [- THEMATIC] [(additional info)]
    # We want to extract just NAME, stripping both the marker and any parenthetical

    # Special case: if parent is ONLY a parenthetical marker (e.g., "(thematic grouping)")
    # then there's no actual parent - this is a root node marker
    if re.match(r'parent=\([^)]+\)$', notes):
        return None, False

    # Extract parent name, stripping "- THEMATIC" suffix and any parenthetical notes
    match = re.search(r'parent=(.+?)(?:\s*-\s*THEMATIC)?(?:\s*\([^)]+\))?$', notes)
    if match:
        parent = match.group(1).strip()
        is_thematic = '- THEMATIC' in notes or 'thematic' in notes.lower()
        return parent, is_thematic

    return None, False


def build_hierarchy_tree(csv_path: Path) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Build parent-child mappings from CSV.

    Each relationship is evaluated individually based on its notes field:
    - THEMATIC: Has "- THEMATIC" marker or "parent=(thematic grouping)"
    - PRIMARY: All other hierarchy relationships

    This supports poly-hierarchies where tags can have both primary AND
    thematic parents (e.g., Halls → Community buildings [primary] AND
    Halls → Cultural venues - THEMATIC).

    Args:
        csv_path: Path to tag_map_consolidated.csv

    Returns:
        Tuple of (primary_hierarchies, thematic_hierarchies)
        Each is a dict mapping parent -> list of children
    """
    primary = defaultdict(list)
    thematic = defaultdict(list)

    # Single pass: classify each relationship individually
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['action'] == 'hierarchy':
                tag_name = row['new_tag']
                parent, is_thematic = parse_parent_from_notes(row['notes'])

                if parent:
                    if is_thematic:
                        thematic[parent].append(tag_name)
                    else:
                        primary[parent].append(tag_name)

    return primary, thematic


def identify_top_level_facets(hierarchies: Dict[str, List[str]]) -> List[str]:
    """
    Identify top-level facets (nodes that are parents but not children).

    Args:
        hierarchies: Parent -> children mapping

    Returns:
        List of top-level facet names
    """
    all_children = set()
    for children in hierarchies.values():
        all_children.update(children)

    all_parents = set(hierarchies.keys())

    # Top-level = parents that are never children
    top_level = all_parents - all_children

    return sorted(top_level)


def generate_tree_lines(
    node: str,
    hierarchies: Dict[str, List[str]],
    prefix: str = "",
    is_last: bool = True,
    visited: Set[str] = None
) -> List[str]:
    """
    Recursively generate ASCII tree lines for a node and its children.

    Args:
        node: Current node name
        hierarchies: Parent -> children mapping
        prefix: Current line prefix for indentation
        is_last: Whether this node is the last sibling
        visited: Set of already visited nodes (prevents infinite loops)

    Returns:
        List of formatted tree lines
    """
    if visited is None:
        visited = set()

    lines = []

    # Add current node
    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{node}")

    # Prevent infinite loops in poly-hierarchies
    if node in visited:
        return lines
    visited.add(node)

    # Get children
    children = hierarchies.get(node, [])
    if not children:
        return lines

    # Sort children alphabetically
    children = sorted(children)

    # Prepare prefix for children
    extension = "    " if is_last else "│   "
    child_prefix = prefix + extension

    # Process each child
    for i, child in enumerate(children):
        is_last_child = (i == len(children) - 1)
        child_lines = generate_tree_lines(
            child,
            hierarchies,
            child_prefix,
            is_last_child,
            visited.copy()  # Copy to allow multiple branches
        )
        lines.extend(child_lines)

    return lines


def generate_facet_tree(facet_name: str, hierarchies: Dict[str, List[str]]) -> str:
    """
    Generate complete ASCII tree for a facet.

    Args:
        facet_name: Name of the top-level facet
        hierarchies: Parent -> children mapping

    Returns:
        Formatted tree as string
    """
    lines = [facet_name]

    children = hierarchies.get(facet_name, [])
    if not children:
        return facet_name + "\n(No children)"

    children = sorted(children)

    for i, child in enumerate(children):
        is_last = (i == len(children) - 1)
        child_lines = generate_tree_lines(child, hierarchies, "", is_last)
        lines.extend(child_lines)

    return "\n".join(lines)


def count_hierarchy_stats(hierarchies: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Calculate statistics for a hierarchy.

    Args:
        hierarchies: Parent -> children mapping

    Returns:
        Dictionary of statistics
    """
    all_nodes = set(hierarchies.keys())
    for children in hierarchies.values():
        all_nodes.update(children)

    total_nodes = len(all_nodes)
    total_relationships = sum(len(children) for children in hierarchies.values())
    leaf_nodes = len(all_nodes - set(hierarchies.keys()))

    return {
        'total_nodes': total_nodes,
        'total_relationships': total_relationships,
        'leaf_nodes': leaf_nodes,
        'parent_nodes': len(hierarchies)
    }


def main():
    """Generate all hierarchy visualizations."""
    print("=" * 80)
    print("POLY-HIERARCHY VISUALIZATION GENERATOR")
    print("=" * 80)
    print()

    # Setup paths
    csv_path = Path('data/tag_map_consolidated.csv')
    output_dir = Path('visualizations/hierarchy_trees')
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Reading hierarchy data from: {csv_path}")
    primary, thematic = build_hierarchy_tree(csv_path)

    print(f"✓ Loaded {len(primary)} primary parent-child relationships")
    print(f"✓ Loaded {len(thematic)} thematic parent-child relationships")
    print()

    # ========================================================================
    # PRIMARY FACETS
    # ========================================================================

    print("=" * 80)
    print("PRIMARY FACETS (Form-Based, Getty AAT Compatible)")
    print("=" * 80)
    print()

    primary_facets = identify_top_level_facets(primary)
    print(f"Identified {len(primary_facets)} top-level primary facets:")
    for facet in primary_facets:
        print(f"  - {facet}")
    print()

    # Generate tree for each primary facet
    for facet in primary_facets:
        print(f"Generating tree for: {facet}")
        tree = generate_facet_tree(facet, primary)

        # Save to file
        safe_filename = re.sub(r'[^\w\s-]', '', facet).replace(' ', '_').lower()
        output_path = output_dir / f"primary_{safe_filename}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"PRIMARY FACET: {facet}\n")
            f.write("=" * 80 + "\n\n")
            f.write(tree)
            f.write("\n\n")

            # Add statistics - count nodes from tree lines
            tree_lines = tree.split('\n')
            node_count = len([line for line in tree_lines if line.strip() and not line.startswith('(')])
            f.write("\nSTATISTICS:\n")
            f.write(f"  Total nodes in facet: {node_count}\n")
            f.write(f"  Generated: 2025-10-20\n")
            f.write(f"  Source: data/tag_map_consolidated.csv\n")

        print(f"  ✓ Saved to: {output_path}")

    print()

    # ========================================================================
    # THEMATIC GROUPINGS
    # ========================================================================

    print("=" * 80)
    print("THEMATIC GROUPINGS (Domain-Based, Exhibition Optimised)")
    print("=" * 80)
    print()

    thematic_groupings = identify_top_level_facets(thematic)
    print(f"Identified {len(thematic_groupings)} thematic groupings:")
    for theme in thematic_groupings:
        print(f"  - {theme}")
    print()

    # Generate tree for each thematic grouping
    for theme in thematic_groupings:
        print(f"Generating tree for: {theme}")
        tree = generate_facet_tree(theme, thematic)

        # Save to file
        safe_filename = re.sub(r'[^\w\s-]', '', theme).replace(' ', '_').lower()
        output_path = output_dir / f"theme_{safe_filename}.txt"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"THEMATIC GROUPING: {theme}\n")
            f.write("=" * 80 + "\n\n")
            f.write(tree)
            f.write("\n\n")

            # Add note about poly-hierarchy
            f.write("\nNOTE: Tags in thematic groupings may also appear in primary facets.\n")
            f.write("This is intentional poly-hierarchy design for flexible querying.\n\n")

            # Add statistics - count nodes from tree lines
            tree_lines = tree.split('\n')
            node_count = len([line for line in tree_lines if line.strip() and not line.startswith('(')])
            f.write("\nSTATISTICS:\n")
            f.write(f"  Total nodes in theme: {node_count}\n")
            f.write(f"  Generated: 2025-10-20\n")
            f.write(f"  Source: data/tag_map_consolidated.csv\n")

        print(f"  ✓ Saved to: {output_path}")

    print()

    # ========================================================================
    # SUMMARY DOCUMENT
    # ========================================================================

    print("=" * 80)
    print("GENERATING SUMMARY DOCUMENT")
    print("=" * 80)
    print()

    summary_path = output_dir / "00_OVERVIEW.txt"

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("POLY-HIERARCHICAL TAXONOMY VISUALIZATION OVERVIEW\n")
        f.write("=" * 80 + "\n\n")

        f.write("This directory contains ASCII tree diagrams for the complete\n")
        f.write("poly-hierarchical taxonomy structure.\n\n")

        f.write("STRUCTURE:\n")
        f.write("-" * 80 + "\n\n")

        f.write("PRIMARY FACETS (Form-Based, Getty AAT Compatible):\n\n")
        for facet in primary_facets:
            safe_filename = re.sub(r'[^\w\s-]', '', facet).replace(' ', '_').lower()
            f.write(f"  - {facet}\n")
            f.write(f"    File: primary_{safe_filename}.txt\n\n")

        f.write("\nTHEMATIC GROUPINGS (Domain-Based, Exhibition Optimised):\n\n")
        for theme in thematic_groupings:
            safe_filename = re.sub(r'[^\w\s-]', '', theme).replace(' ', '_').lower()
            f.write(f"  - {theme}\n")
            f.write(f"    File: theme_{safe_filename}.txt\n\n")

        f.write("\n" + "=" * 80 + "\n\n")
        f.write("POLY-HIERARCHY EXPLANATION:\n\n")
        f.write("Tags may appear in MULTIPLE trees. This is intentional.\n\n")
        f.write("Example: 'Hotels' appears in:\n")
        f.write("  1. Agents > Organizations > Hospitality businesses > Hotels\n")
        f.write("  2. Built Environment > Accommodation buildings > Hotels\n")
        f.write("  3. Alcohol & Temperance > Alcohol-related venues > Hotels\n")
        f.write("  4. Tourism & Accommodation > Accommodation > Hotels\n\n")
        f.write("This enables:\n")
        f.write("  - Flexible querying from multiple perspectives\n")
        f.write("  - Getty AAT compatibility (primary facets)\n")
        f.write("  - Thematic exhibitions and tours (thematic groupings)\n\n")

        f.write("=" * 80 + "\n\n")
        f.write("OVERALL STATISTICS:\n\n")
        primary_stats = count_hierarchy_stats(primary)
        thematic_stats = count_hierarchy_stats(thematic)

        f.write(f"Primary Facets:\n")
        f.write(f"  - Top-level facets: {len(primary_facets)}\n")
        f.write(f"  - Total nodes: {primary_stats['total_nodes']}\n")
        f.write(f"  - Total relationships: {primary_stats['total_relationships']}\n")
        f.write(f"  - Parent nodes: {primary_stats['parent_nodes']}\n")
        f.write(f"  - Leaf nodes: {primary_stats['leaf_nodes']}\n\n")

        f.write(f"Thematic Groupings:\n")
        f.write(f"  - Top-level themes: {len(thematic_groupings)}\n")
        f.write(f"  - Total nodes: {thematic_stats['total_nodes']}\n")
        f.write(f"  - Total relationships: {thematic_stats['total_relationships']}\n")
        f.write(f"  - Parent nodes: {thematic_stats['parent_nodes']}\n")
        f.write(f"  - Leaf nodes: {thematic_stats['leaf_nodes']}\n\n")

        f.write(f"TOTAL HIERARCHY RELATIONSHIPS: {primary_stats['total_relationships'] + thematic_stats['total_relationships']}\n\n")

        f.write("=" * 80 + "\n")
        f.write("Generated: 2025-10-20\n")
        f.write("Script: scripts/23_visualise_poly_hierarchy.py\n")
        f.write("Source: data/tag_map_consolidated.csv\n")

    print(f"✓ Saved summary to: {summary_path}")
    print()

    # ========================================================================
    # COMPLETION SUMMARY
    # ========================================================================

    print("=" * 80)
    print("VISUALIZATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    print(f"Generated files:")
    print(f"  - {len(primary_facets)} primary facet trees")
    print(f"  - {len(thematic_groupings)} thematic grouping trees")
    print(f"  - 1 overview/summary document")
    print(f"  TOTAL: {len(primary_facets) + len(thematic_groupings) + 1} files")
    print()
    print(f"Output directory: {output_dir.absolute()}")
    print()
    print("Next steps:")
    print("  1. Review tree diagrams for accuracy")
    print("  2. Validate parent-child relationships")
    print("  3. Update folksonomy_logic.md with structure")
    print("  4. Proceed to Phase 1.3 (Getty AAT mapping)")
    print()


if __name__ == '__main__':
    main()
