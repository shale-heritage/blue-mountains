#!/usr/bin/env python3
"""
Script 26: Check Druid's Lodge Context - Building or Organization?

Usage:
    python scripts/26_check_druids_lodge_context.py

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


def check_tag_context(zot, tag_name):
    """Fetch all items and show full contexts."""
    print(f"\n{'='*80}")
    print(f"TAG: {tag_name}")
    print(f"{'='*80}\n")

    items = zot.items(tag=tag_name, limit=10)

    if not items:
        print(f"  No items found")
        return

    print(f"Found {len(items)} item(s)\n")

    for idx, item in enumerate(items, 1):
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '[No Date]')

        print(f"\n[{idx}] {item_title} ({item_date})")
        print("-" * 80)

        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        if notes:
            for note in notes:
                note_content = note['data'].get('note', '')
                if note_content:
                    clean_text = strip_html_tags(note_content)

                    # Find all occurrences
                    pattern = re.escape(tag_name)
                    matches = list(re.finditer(pattern, clean_text, re.IGNORECASE))

                    if matches:
                        print(f"\nFound {len(matches)} occurrence(s):\n")
                        for i, match in enumerate(matches, 1):
                            start = max(0, match.start() - 300)
                            end = min(len(clean_text), match.end() + 300)
                            context = clean_text[start:end]
                            print(f"  [{i}] ...{context}...\n")
                    else:
                        print(f"Tag not found in note text (might be in title/metadata)")
        else:
            print("  No notes available")


def main():
    """Check Druid's Lodge context."""
    print("=" * 80)
    print("DRUID'S LODGE CONTEXT ANALYSIS")
    print("=" * 80)

    zot = connect_to_zotero()
    check_tag_context(zot, "Druid's Lodge")

    print("\n" + "=" * 80)
    print("INDICATORS TO LOOK FOR:")
    print("=" * 80)
    print()
    print("BUILDING indicators:")
    print("  - 'in the Druid's Lodge', 'at the Druid's Lodge'")
    print("  - 'hall', 'building', 'premises', 'erected'")
    print("  - 'meeting was held in...'")
    print()
    print("ORGANIZATION indicators:")
    print("  - 'forming a Druid's Lodge', 'establishing'")
    print("  - 'members of the Druid's Lodge'")
    print("  - 'officers of the lodge'")
    print("  - 'Jersey Lodge' (proper name of local chapter)")
    print()


if __name__ == '__main__':
    main()
