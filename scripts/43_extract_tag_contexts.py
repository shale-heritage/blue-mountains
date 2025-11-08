#!/usr/bin/env python3
"""
Extract items and contexts for specific tags to aid in tagging decisions.

Reads from zotero_full_export.json and extracts items tagged with specific
orphaned tags, showing title, date, publication, and other metadata.
"""

import json
import sys
from collections import defaultdict

TAGS_TO_EXTRACT = [
    "Alcohol",
    "Mining settlements",
    "Rifle reserves"
]

def load_zotero_export():
    """Load Zotero export JSON."""
    with open('data/zotero_full_export.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Handle both list and dict formats
        if isinstance(data, dict) and 'items' in data:
            return data['items']
        return data

def extract_text_from_notes(notes):
    """Extract text content from Zotero notes (HTML format)."""
    if not notes:
        return ""

    # Concatenate all notes
    full_text = []
    for note in notes:
        if isinstance(note, dict) and 'note' in note:
            html = note['note']
            # Simple HTML tag removal
            import re
            text = re.sub('<[^<]+?>', '', html)
            text = text.replace('&nbsp;', ' ')
            text = re.sub(r'\s+', ' ', text)
            full_text.append(text.strip())

    return '\n\n'.join(full_text)

def extract_tagged_items(data, target_tags):
    """Extract items with specific tags."""
    results = defaultdict(list)

    for item in data:
        # Get item tags
        item_tags = item.get('tags', [])
        # Handle both string arrays and dict arrays
        if item_tags and isinstance(item_tags[0], str):
            tag_names = item_tags
        else:
            tag_names = [tag.get('tag', '') for tag in item_tags if isinstance(tag, dict)]

        # Check if any target tags are present
        for target_tag in target_tags:
            if target_tag in tag_names:
                # Extract notes/annotations
                notes = item.get('notes', [])
                primary_text = extract_text_from_notes(notes)

                # Extract relevant fields
                item_info = {
                    'title': item.get('title', 'No title'),
                    'date': item.get('date', 'No date'),
                    'publicationTitle': item.get('publicationTitle', ''),
                    'itemType': item.get('itemType', ''),
                    'tags': tag_names,
                    'url': item.get('url', ''),
                    'primary_text': primary_text[:1500] if primary_text else 'No text available'  # Limit length
                }
                results[target_tag].append(item_info)

    return results

def format_item_report(tag, items):
    """Format items for human review with decision options."""
    report = []
    report.append(f"\n## Tag: {tag}")
    report.append(f"\n**Total occurrences**: {len(items)}\n")

    for i, item in enumerate(items, 1):
        report.append(f"### Occurrence {i}")
        report.append("")
        report.append(f"**Item**: {item['title']}")
        report.append(f"**Date**: {item['date']}")
        if item['publicationTitle']:
            report.append(f"**Publication**: {item['publicationTitle']}")
        if item['url']:
            report.append(f"**URL**: {item['url']}")
        report.append("")

        # Show other relevant tags
        other_tags = [t for t in item['tags'] if t != tag]
        if other_tags:
            report.append(f"**Other tags**: {', '.join(other_tags)}")
            report.append("")

        # Show primary text excerpt
        report.append("**Primary text excerpt**:")
        report.append("")
        report.append("```text")
        text = item.get('primary_text', 'No text available')
        # Clean up text for display
        if len(text) > 800:
            text = text[:800] + "..."
        report.append(text)
        report.append("```")
        report.append("")

        # Decision section
        report.append("**Recommended new tag(s)**:")
        report.append("")
        report.append("- [ ] APPROVE: (specify replacement tags)")
        report.append("- [ ] REJECT: Keep original tag")
        report.append("- [ ] CHANGE: (specify alternative)")
        report.append("")
        report.append("**Notes**: ")
        report.append("")
        report.append("---")
        report.append("")

    return '\n'.join(report)

def main():
    """Extract and display tagged items."""
    print("Extracting items for orphaned tags...\n")

    data = load_zotero_export()
    print(f"Loaded {len(data)} items from Zotero export")

    results = extract_tagged_items(data, TAGS_TO_EXTRACT)

    # Generate report header
    full_report = []
    full_report.append("# Orphaned Tags - Retagging Decisions")
    full_report.append("")
    full_report.append("**Date**: 2025-11-04")
    full_report.append("**Purpose**: Review and approve replacement tags for orphaned folksonomy tags")
    full_report.append("**Status**: PENDING APPROVAL")
    full_report.append("")
    full_report.append("## Instructions")
    full_report.append("")
    full_report.append("For each occurrence below:")
    full_report.append("")
    full_report.append("1. Review the primary text excerpt")
    full_report.append("2. Review the existing co-tags")
    full_report.append("3. Mark your decision: APPROVE / REJECT / CHANGE")
    full_report.append("4. Specify the replacement tag(s) if APPROVE or CHANGE")
    full_report.append("5. Add any notes about the decision")
    full_report.append("")
    full_report.append("---")
    full_report.append("")

    # Generate report for each tag
    for tag in TAGS_TO_EXTRACT:
        items = results.get(tag, [])
        if items:
            full_report.append(format_item_report(tag, items))
        else:
            full_report.append(f"\n## Tag: {tag}")
            full_report.append(f"\n**No items found for this tag**\n")
            full_report.append("---")
            full_report.append("")

    # Save to file
    output_file = 'reports/orphaned_tags_RETAGGING_DECISIONS.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(full_report))

    print(f"\nReport saved to: {output_file}")
    print(f"Total items to review: {sum(len(items) for items in results.values())}")

if __name__ == '__main__':
    main()
