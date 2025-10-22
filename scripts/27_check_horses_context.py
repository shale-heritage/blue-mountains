#!/usr/bin/env python3
"""
Script 27: Check Horses Tag Context - Recreation or Mining Transport?

Usage:
    python scripts/27_check_horses_context.py

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
    """Fetch items and show contexts."""
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

                    # Find occurrences
                    pattern = re.compile(r'\bhorse\w*\b', re.IGNORECASE)
                    matches = list(pattern.finditer(clean_text))

                    if matches:
                        print(f"\nFound {len(matches)} horse-related reference(s):\n")
                        for i, match in enumerate(matches[:3], 1):  # Show first 3
                            start = max(0, match.start() - 200)
                            end = min(len(clean_text), match.end() + 200)
                            context = clean_text[start:end]
                            print(f"  [{i}] ...{context}...\n")
                    else:
                        print(f"Tag not found in note text")
        else:
            print("  No notes available")


def main():
    """Check Horses tag context."""
    print("=" * 80)
    print("HORSES TAG CONTEXT ANALYSIS")
    print("=" * 80)

    zot = connect_to_zotero()
    check_tag_context(zot, "Horses")

    print("\n" + "=" * 80)
    print("CLASSIFICATION INDICATORS:")
    print("=" * 80)
    print()
    print("RECREATION indicators:")
    print("  - 'horseback riding', 'riding for pleasure'")
    print("  - 'horse racing', 'equestrian events'")
    print("  - 'picnic', 'outing', 'excursion'")
    print()
    print("TRANSPORT/MINING indicators:")
    print("  - 'cart', 'dray', 'wagon', 'haulage'")
    print("  - 'teams of horses', 'working horses'")
    print("  - 'transport', 'carrying', 'hauling'")
    print()


if __name__ == '__main__':
    main()
