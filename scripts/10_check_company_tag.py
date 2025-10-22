#!/usr/bin/env python3
"""
Script 10: Check Items with 'katoomba south coal mining company' Tag

Quick investigation of items tagged with this company name to understand
what it refers to and how it relates to other mining/company tags.
"""

import sys
from pathlib import Path
from pyzotero import zotero

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def connect_to_zotero():
    """Connect to Zotero group library via API."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def check_tag(zot, tag_name):
    """Check all items with a specific tag."""
    print(f"\nFetching items with tag '{tag_name}'...")
    items = zot.items(tag=tag_name)

    print(f"Found {len(items)} items\n")

    if len(items) == 0:
        print("No items found with this tag.")
        return

    for i, item in enumerate(items, 1):
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '[No Date]')
        item_type = item['data'].get('itemType', '[No Type]')

        # Get all tags for this item
        tags = [t['tag'] for t in item['data'].get('tags', [])]

        print(f"{i}. {item_title}")
        print(f"   Date: {item_date}")
        print(f"   Type: {item_type}")
        print(f"   Tags: {', '.join(tags[:10])}" + (" ..." if len(tags) > 10 else ""))
        print()


def main():
    """Main execution function."""
    print("="*70)
    print("CHECK COMPANY TAG")
    print("="*70)
    print()

    try:
        zot = connect_to_zotero()
        check_tag(zot, 'katoomba south coal mining company')

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
