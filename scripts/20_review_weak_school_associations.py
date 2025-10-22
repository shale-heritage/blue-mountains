#!/usr/bin/env python3
"""
Script 20: Review Weak School of Arts Town Associations

For towns with weak associations (inferred from location tags only),
extract full text to look for ANY mention of "School of Arts" in the
context of that town, even if not in the specific pattern "[Town] School of Arts".

This will help determine if the association is valid or if the generic
"School of Arts" tag was applied to an article that mentions multiple towns.

Author: Claude Code
Date: 2025-10-19
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from pyzotero import zotero

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


class MLStripper(HTMLParser):
    """Simple HTML tag stripper."""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)


def strip_html(html):
    """Remove HTML tags from text."""
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


def connect_to_zotero():
    """Connect to Zotero API."""
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def get_school_of_arts_context(zot, item_key, town_name):
    """
    Get all contexts where "School of Arts" appears in an item,
    showing which town (if any) it's associated with.
    """
    children = zot.children(item_key)
    notes = [child for child in children if child['data'].get('itemType') == 'note']

    full_text = ''
    for note in notes:
        note_content = note['data'].get('note', '')
        full_text += strip_html(note_content) + '\n'

    if not full_text.strip():
        return []

    # Find all "School of Arts" mentions
    pattern = re.compile(
        r'.{0,150}\bSchool\s+of\s+Arts\b.{0,150}',
        re.IGNORECASE
    )

    contexts = []
    for match in pattern.finditer(full_text):
        context = match.group(0)
        context = ' '.join(context.split())

        # Check if this town is mentioned near this School of Arts reference
        town_nearby = town_name.lower() in context.lower()

        contexts.append({
            'context': context,
            'town_nearby': town_nearby
        })

    return contexts


def main():
    """Main execution."""
    print("=" * 70)
    print("REVIEW WEAK SCHOOL OF ARTS ASSOCIATIONS")
    print("=" * 70)
    print()

    # Weak associations from previous analysis
    weak_associations = {
        'Blackheath': ['5JRZQCQK', 'DV7KQRCE'],  # Item keys will vary
        'Leura': [],
        'Megalong': [],
        'Mount Victoria': [],
        'Wentworth Falls': []
    }

    # Get actual items tagged with both "School of Arts" and each location
    zot = connect_to_zotero()

    towns = ['Blackheath', 'Leura', 'Megalong', 'Mount Victoria', 'Wentworth Falls']

    for town in towns:
        print(f"\n{'=' * 70}")
        print(f"{town} - CONTEXT REVIEW")
        print(f"{'=' * 70}")

        # Get items with both tags
        all_items = zot.items(tag='School of Arts')

        town_items = []
        for item in all_items:
            item_tags = [t['tag'] for t in item['data'].get('tags', [])]
            if town in item_tags:
                town_items.append(item)

        if not town_items:
            print(f"\nNo items found with both 'School of Arts' and '{town}' tags")
            continue

        print(f"\nFound {len(town_items)} items with both tags")

        for item in town_items:
            item_title = item['data'].get('title', '[No Title]')
            item_key = item['key']

            print(f"\n  Item: {item_title}")
            print(f"  Key: {item_key}")

            contexts = get_school_of_arts_context(zot, item_key, town)

            if not contexts:
                print(f"    ⚠ No 'School of Arts' found in full text")
                continue

            print(f"    Found {len(contexts)} School of Arts references:")

            for i, ctx_info in enumerate(contexts, 1):
                town_marker = " ✓ TOWN NAME NEARBY" if ctx_info['town_nearby'] else " ✗ Town not nearby"
                print(f"\n    Context {i}:{town_marker}")
                print(f"      ...{ctx_info['context']}...")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nReview the contexts above to determine:")
    print("  1. Does the School of Arts reference clearly relate to this town?")
    print("  2. Or is it a generic reference or refers to a different town?")
    print("\nMark for user review any ambiguous cases")
    print()


if __name__ == '__main__':
    main()
