#!/usr/bin/env python3
"""
Script 25: Check Hall/Lodge Context in Primary Sources

Determines whether tags refer to buildings or organizations.

Usage:
    python scripts/25_check_hall_lodge_context.py

Author: Claude Code
Date: 2025-10-20
"""

import sys
from pathlib import Path
from pyzotero import zotero
import re

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def connect_to_zotero():
    """Connect to Zotero group library via Application Programming Interface (API)."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def strip_html_tags(html_text):
    """Remove HTML tags from text."""
    clean = re.sub('<.*?>', '', html_text)
    return clean


def check_tag_context(zot, tag_name, max_items=5):
    """Fetch items and extract context."""
    print(f"\n{'='*80}")
    print(f"TAG: {tag_name}")
    print(f"{'='*80}\n")

    items = zot.items(tag=tag_name, limit=max_items)

    if not items:
        print(f"  No items found with tag '{tag_name}'")
        return []

    print(f"Found {len(items)} item(s)\n")

    contexts = []

    for idx, item in enumerate(items, 1):
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '[No Date]')

        print(f"[{idx}] {item_title}")
        print(f"    Date: {item_date}")

        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        if notes:
            for note in notes:
                note_content = note['data'].get('note', '')
                if note_content:
                    clean_text = strip_html_tags(note_content)

                    # Extract context
                    tag_pattern = re.escape(tag_name)
                    matches = list(re.finditer(tag_pattern, clean_text, re.IGNORECASE))

                    if matches:
                        match = matches[0]
                        start = max(0, match.start() - 200)
                        end = min(len(clean_text), match.end() + 200)
                        context = clean_text[start:end]

                        print(f"    Context: ...{context}...")
                        print()

                        contexts.append(context)
        else:
            print(f"    No notes")
            print()

    return contexts


def main():
    """Check hall/lodge contexts."""
    print("=" * 80)
    print("HALL/LODGE CONTEXT CHECK")
    print("=" * 80)
    print()

    zot = connect_to_zotero()

    tags_to_check = [
        'Odd Fellows\' Hall',
        'Masonic Hall',
        'Druid\'s Lodge',
        'U.A.O.D.',
    ]

    for tag in tags_to_check:
        check_tag_context(zot, tag, max_items=3)

    print("\n" + "=" * 80)
    print("ANALYSIS GUIDE")
    print("=" * 80)
    print()
    print("Building indicators:")
    print("  - 'in the [name]', 'at the [name]'")
    print("  - 'opened the [name]', 'building', 'premises'")
    print()
    print("Organization indicators:")
    print("  - 'members of the [name]'")
    print("  - 'lodge meeting', 'society', 'order'")
    print()


if __name__ == '__main__':
    main()
