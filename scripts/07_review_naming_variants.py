#!/usr/bin/env python3
"""
Review Naming Variants: Extract Zotero Items for Context

This script extracts the actual Zotero items that use each tag in the naming
variant pairs, allowing the historian to review usage context and determine
if they represent the same entity or are distinct.

Author: Claude Code
Date: 2025-10-19
"""

import json
from pathlib import Path
from typing import Dict, List, Set


def load_zotero_data() -> List[Dict]:
    """
    Load Zotero items from JSON file.

    Returns:
        List of Zotero item dictionaries
    """
    data_file = Path(__file__).parent.parent / "data/zotero_items.json"

    with open(data_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_items_with_tag(items: List[Dict], tag_name: str) -> List[Dict]:
    """
    Get all items that have a specific tag.

    Args:
        items: List of Zotero items
        tag_name: Tag to search for

    Returns:
        List of items with that tag
    """
    matching_items = []

    for item in items:
        tags = item.get('data', {}).get('tags', [])
        tag_names = [t.get('tag', '') for t in tags]

        if tag_name in tag_names:
            matching_items.append(item)

    return matching_items


def extract_item_info(item: Dict) -> Dict:
    """
    Extract relevant information from a Zotero item for display.

    Args:
        item: Zotero item dictionary

    Returns:
        Dictionary with title, date, creators, abstract snippet
    """
    data = item.get('data', {})

    # Get title
    title = data.get('title', 'No title')

    # Get date
    date = data.get('date', 'No date')

    # Get creators
    creators = data.get('creators', [])
    creator_str = '; '.join([
        f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
        for c in creators
    ])

    # Get abstract snippet (first 200 chars)
    abstract = data.get('abstractNote', '')
    abstract_snippet = (abstract[:200] + '...') if len(abstract) > 200 else abstract

    # Get all tags for context
    tags = data.get('tags', [])
    all_tags = [t.get('tag', '') for t in tags]

    return {
        'title': title,
        'date': date,
        'creators': creator_str if creator_str else 'No creators',
        'abstract': abstract_snippet,
        'all_tags': all_tags
    }


def analyze_naming_variant(
    items: List[Dict],
    tag1: str,
    tag2: str,
    output_lines: List[str]
) -> None:
    """
    Analyze a naming variant pair and add results to output.

    Args:
        items: All Zotero items
        tag1: First tag name
        tag2: Second tag name
        output_lines: List to append output lines to
    """
    items1 = get_items_with_tag(items, tag1)
    items2 = get_items_with_tag(items, tag2)

    output_lines.append(f"\n## Pair: '{tag1}' vs '{tag2}'")
    output_lines.append(f"\n**Usage:** {tag1} ({len(items1)} items) vs {tag2} ({len(items2)} items)")
    output_lines.append("")

    # Check for overlap
    keys1 = {item.get('key') for item in items1}
    keys2 = {item.get('key') for item in items2}
    overlap = keys1 & keys2

    if overlap:
        output_lines.append(f"⚠️  **OVERLAP:** {len(overlap)} items have BOTH tags")
        output_lines.append("")

    # Show items for tag1
    output_lines.append(f"### Items tagged '{tag1}' (showing up to 5):")
    output_lines.append("")

    for i, item in enumerate(items1[:5], 1):
        info = extract_item_info(item)
        output_lines.append(f"**{i}. {info['title']}**")
        output_lines.append(f"   - Date: {info['date']}")
        output_lines.append(f"   - Creators: {info['creators']}")
        if info['abstract']:
            output_lines.append(f"   - Abstract: {info['abstract']}")
        output_lines.append(f"   - Other tags: {', '.join([t for t in info['all_tags'] if t not in [tag1, tag2]][:5])}")
        output_lines.append("")

    if len(items1) > 5:
        output_lines.append(f"   *(... and {len(items1) - 5} more items)*")
        output_lines.append("")

    # Show items for tag2
    output_lines.append(f"### Items tagged '{tag2}' (showing up to 5):")
    output_lines.append("")

    for i, item in enumerate(items2[:5], 1):
        info = extract_item_info(item)
        output_lines.append(f"**{i}. {info['title']}**")
        output_lines.append(f"   - Date: {info['date']}")
        output_lines.append(f"   - Creators: {info['creators']}")
        if info['abstract']:
            output_lines.append(f"   - Abstract: {info['abstract']}")
        output_lines.append(f"   - Other tags: {', '.join([t for t in info['all_tags'] if t not in [tag1, tag2]][:5])}")
        output_lines.append("")

    if len(items2) > 5:
        output_lines.append(f"   *(... and {len(items2) - 5} more items)*")
        output_lines.append("")

    # Add decision framework
    output_lines.append("### Decision Framework:")
    output_lines.append("")
    output_lines.append("**Questions to consider:**")
    output_lines.append("1. Do items refer to the same geographic location/entity?")
    output_lines.append("2. Are the names used interchangeably in historical sources?")
    output_lines.append("3. Is one name a formal variant and the other informal?")
    output_lines.append("4. Should they be merged (same entity) or kept separate (distinct)?")
    output_lines.append("")
    output_lines.append("**Proposed decision:** _[MERGE / HIERARCHY / KEEP_SEPARATE]_")
    output_lines.append("")
    output_lines.append("**Rationale:** _[To be filled in]_")
    output_lines.append("")
    output_lines.append("---")


def main():
    """Main execution function."""
    base_dir = Path(__file__).parent.parent
    output_file = base_dir / "reports/naming_variants_review.md"

    print("Reviewing Naming Variants")
    print("=" * 60)
    print()

    # Load Zotero data
    print("Loading Zotero items...")
    items = load_zotero_data()
    print(f"✓ Loaded {len(items)} items")
    print()

    # Define naming variant pairs
    naming_variants = [
        ("Katoomba South", "South Katoomba"),
        ("Katoomba Superior Public School", "Katoomba Public School"),
        ("Katoomba Coal and Shale Mines", "Katoomba Coal and Shale Company"),
        ("Katoomba coal mines", "Katoomba Coal and Shale Company"),
        ("Katoomba Coal and Shale Mines", "Katoomba coal mines"),
        ("Druid's Lodge", "Lodges"),
    ]

    # Generate report
    output_lines = [
        "# Naming Variants Review",
        "",
        "**Generated:** 2025-10-19",
        "",
        "This report shows the actual Zotero items tagged with each naming variant pair",
        "to help determine if they represent the same entity or are distinct.",
        "",
        "---",
    ]

    print("Analyzing naming variant pairs...")
    for tag1, tag2 in naming_variants:
        print(f"  - Analyzing: '{tag1}' vs '{tag2}'")
        analyze_naming_variant(items, tag1, tag2, output_lines)

    # Write report
    print()
    print("Writing review report...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"✓ Report written to: {output_file}")
    print()
    print("=" * 60)
    print("Review the report to make decisions on each naming variant pair")
    print()


if __name__ == "__main__":
    main()
