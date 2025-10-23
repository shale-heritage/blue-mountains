#!/usr/bin/env python3
"""
Script 36: Fix Accommodation Report Tags from Hierarchy Paths

This script updates the "Proposed Tag" field in the accommodation rationalization
report by extracting leaf nodes from the hierarchy paths.

The user edited the hierarchy paths to show the correct tags (as leaf nodes at the
end of each path), but the "Proposed Tag" field wasn't updated to match. This script
extracts those leaf nodes and updates the proposed tag field accordingly.

Hierarchy path format:
    "Built Environment > Buildings > Hotels > Carrington Hotel | Places > Towns > Katoomba"

Leaf nodes (desired tags):
    "Carrington Hotel" and "Katoomba"

Usage:
    python scripts/36_fix_accommodation_tags.py
"""

import re
from pathlib import Path


def extract_leaf_nodes(hierarchy_path):
    """
    Extract leaf nodes (final terms) from a hierarchy path.

    Applies tagging guidelines:
    - Converts plural organizational categories to singular generic tags
    - Keeps specific named instances as-is

    Parameters:
        hierarchy_path (str): Full hierarchy path with | separating multiple paths

    Returns:
        list: Leaf nodes (final term in each path segment)

    Example:
        Input: "Built Environment > Buildings > Hotels > Carrington Hotel | Places > Towns > Katoomba"
        Output: ["Carrington Hotel", "Katoomba"]

        Input: "Built Environment > Buildings > Accommodation buildings > Hotels"
        Output: ["Hotel"]  (converted from plural to singular)
    """
    # Mapping of plural organizational categories to singular generic tags
    # Following leaf nodes only rule: never tag with plural categories
    plural_to_singular = {
        'Hotels': 'Hotel',
        'Boarding houses': 'Boarding house',
        'Cottages': 'Cottage',
        'Stables': 'Stable',
        'Churches': 'Church',
        'Hotelliers': 'Hotellier',
        'Publicans': 'Publican',
        'Liquor merchants': 'Liquor merchant',
        'Clergy': 'Clergyman',  # Note: Clergyman not yet in vocabulary, but planned
        'Medical professionals': 'Medical professional',  # Not yet in vocabulary
        'Schools': 'School',
        'Halls': 'Hall',
        'Mines': 'Mine',
        'Towns': 'Town',  # Usually shouldn't appear as leaf node
        'Reserves': 'Reserve',
        # Add more as needed
    }

    # Split by pipe to get individual hierarchy chains
    chains = hierarchy_path.split('|')

    leaf_nodes = []
    for chain in chains:
        # Split by > and get the last element (leaf node)
        parts = [part.strip() for part in chain.split('>')]
        if parts:
            leaf_node = parts[-1]

            # Convert plural organizational categories to singular generic
            if leaf_node in plural_to_singular:
                leaf_node = plural_to_singular[leaf_node]

            # Only add if not already in list (avoid duplicates)
            if leaf_node not in leaf_nodes:
                leaf_nodes.append(leaf_node)

    return leaf_nodes


def format_proposed_tags(leaf_nodes):
    """
    Format leaf nodes as proposed tags.

    Parameters:
        leaf_nodes (list): List of leaf node terms

    Returns:
        str: Formatted as backtick-quoted tags separated by pipes

    Example:
        Input: ["Carrington Hotel", "Katoomba"]
        Output: "`Carrington Hotel` | `Katoomba`"
    """
    return ' | '.join(f'`{node}`' for node in leaf_nodes)


def process_report(report_path):
    """
    Process accommodation report and update proposed tags from hierarchy paths.

    Parameters:
        report_path (Path): Path to accommodation rationalization report
    """
    print(f"Reading report: {report_path}")

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match items with Proposed Tag and Hierarchy Path
    # This regex captures:
    # - The full item block
    # - The current proposed tag (may include multiple tags separated by |)
    # - The hierarchy path
    pattern = re.compile(
        r'(- \*\*Proposed Tag:\*\* )((?:`[^`]+`(?:\s*\|\s*)?)+)'  # Proposed tag (one or more backtick-quoted terms)
        r'(\s+- \*\*Hierarchy Path:\*\* )([^\n]+)',  # Hierarchy path
        re.MULTILINE
    )

    updates = []

    def replacer(match):
        """Replace proposed tag with leaf nodes from hierarchy path."""
        prefix = match.group(1)  # "- **Proposed Tag:** "
        old_tag = match.group(2)  # Current tag like `Hotel`
        hierarchy_prefix = match.group(3)  # "\n- **Hierarchy Path:** "
        hierarchy_path = match.group(4)  # The actual hierarchy path

        # Extract leaf nodes from hierarchy path
        leaf_nodes = extract_leaf_nodes(hierarchy_path)

        # Format as proposed tags
        new_tag = format_proposed_tags(leaf_nodes)

        # Track update
        if old_tag != new_tag:
            updates.append({
                'old': old_tag,
                'new': new_tag,
                'leaf_nodes': leaf_nodes
            })

        # Return updated text
        return f"{prefix}{new_tag}{hierarchy_prefix}{hierarchy_path}"

    # Perform replacements
    updated_content = pattern.sub(replacer, content)

    # Write updated content
    print(f"Writing updated report...")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    # Report results
    print(f"\n✓ Updated {len(updates)} items")

    if updates:
        print("\nSample updates:")
        for update in updates[:5]:  # Show first 5
            print(f"  {update['old']} → {update['new']}")
            print(f"    Leaf nodes: {', '.join(update['leaf_nodes'])}")

    print(f"\n✓ Report updated: {report_path}")


def main():
    """Main entry point."""
    report_path = Path('reports/accommodation_rationalization_report.md')

    if not report_path.exists():
        print(f"ERROR: Report not found: {report_path}")
        return 1

    process_report(report_path)

    return 0


if __name__ == '__main__':
    exit(main())
