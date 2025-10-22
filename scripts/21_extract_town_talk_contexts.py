#!/usr/bin/env python3
"""
Script 21: Extract Full Town Talk Contexts for School of Arts

For the "Town Talk" items that mention School of Arts, extract large context
windows to show:
1. How the town is introduced/referenced
2. How "the local School of Arts" is mentioned

This will help determine if the School of Arts reference clearly belongs to
the town indicated by the location tag.

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


def extract_full_context(text, item_title):
    """
    Extract large contexts around School of Arts mentions,
    including town name references.
    """
    # Find all School of Arts mentions
    soa_pattern = re.compile(
        r'School\s+of\s+Arts',
        re.IGNORECASE
    )

    contexts = []

    for match in soa_pattern.finditer(text):
        # Get very large context - 800 chars before and after
        start = max(0, match.start() - 800)
        end = min(len(text), match.end() + 800)

        context = text[start:end]

        # Clean up whitespace but preserve paragraph structure
        context = re.sub(r'\s+', ' ', context)

        # Find the School of Arts mention within this context
        match_in_context = re.search(r'School\s+of\s+Arts', context, re.IGNORECASE)
        if match_in_context:
            # Mark the match
            before = context[:match_in_context.start()]
            matched = context[match_in_context.start():match_in_context.end()]
            after = context[match_in_context.end():]

            marked_context = f"{before}**{matched}**{after}"
            contexts.append(marked_context)

    return contexts


def main():
    """Main execution."""
    print("=" * 70)
    print("TOWN TALK CONTEXTS - SCHOOL OF ARTS MENTIONS")
    print("=" * 70)
    print()

    zot = connect_to_zotero()

    # Get the specific "Town Talk" items
    items = zot.items(tag='School of Arts')

    # Focus on Town Talk items
    town_talk_items = [item for item in items if 'Town Talk' in item['data'].get('title', '')]

    print(f"Found {len(town_talk_items)} 'Town Talk' items with School of Arts tag\n")

    for item in town_talk_items:
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', 'Unknown date')
        item_tags = [t['tag'] for t in item['data'].get('tags', [])]

        # Filter for location tags
        towns = ['Blackheath', 'Leura', 'Megalong', 'Mount Victoria', 'Wentworth Falls', 'Katoomba']
        location_tags = [t for t in item_tags if t in towns]

        print("=" * 70)
        print(f"ITEM: {item_title}")
        print(f"Date: {item_date}")
        print(f"Key: {item_key}")
        print(f"Location tags: {', '.join(location_tags) if location_tags else 'None'}")
        print("=" * 70)

        # Get full text
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        if not full_text.strip():
            print("⚠ No full text available\n")
            continue

        # Extract contexts
        contexts = extract_full_context(full_text, item_title)

        if not contexts:
            print("⚠ No School of Arts mentions found\n")
            continue

        print(f"\nFound {len(contexts)} School of Arts mention(s):\n")

        for i, context in enumerate(contexts, 1):
            print(f"--- Context {i} ---")
            print(f"{context}")
            print()

        print("\n")


if __name__ == '__main__':
    main()
