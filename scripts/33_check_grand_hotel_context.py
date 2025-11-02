#!/usr/bin/env python3
"""
Script 33: Check Grand Hotel Tag Context

Investigates whether items tagged with "Grand Hotel" refer to a Sydney hotel
or a Blue Mountains hotel, to determine if it should be merged with
"Grand Hotel (Sydney)" or kept as a separate entity.

Usage:
    python scripts/33_check_grand_hotel_context.py

Author: Claude Code
Date: 2025-11-02
"""

import sys
from pathlib import Path
from pyzotero import zotero
import re

# Add parent directory to path for imports
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
    """Remove HyperText Markup Language (HTML) tags from text."""
    clean = re.sub('<.*?>', '', html_text)
    return clean


def main():
    """Check context for Grand Hotel tag."""
    print("=" * 80)
    print("GRAND HOTEL TAG CONTEXT ANALYSIS")
    print("=" * 80)
    print()
    print("Checking whether 'Grand Hotel' refers to Sydney or Blue Mountains location...")
    print()

    # Connect to Zotero
    zot = connect_to_zotero()

    # Fetch items with "Grand Hotel" tag
    items = zot.items(tag='Grand Hotel', limit=10)

    print(f"\nFound {len(items)} item(s) tagged with 'Grand Hotel'\n")
    print("=" * 80)

    for idx, item in enumerate(items, 1):
        item_data = item['data']
        title = item_data.get('title', '[No Title]')
        date = item_data.get('date', '[No Date]')

        print(f"\n[{idx}] {title}")
        print(f"    Date: {date}")

        # Get notes
        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        if notes:
            for note_idx, note in enumerate(notes, 1):
                content = strip_html_tags(note['data'].get('note', ''))

                # Look for location indicators
                location_terms = {
                    'Sydney': ['Sydney', 'George Street', 'Pitt Street', 'Market Street',
                              'Clarence Street', 'York Street'],
                    'Blue Mountains': ['Katoomba', 'Blue Mountains', 'Leura', 'Wentworth Falls',
                                      'Mount Victoria', 'Blackheath']
                }

                found_locations = {'Sydney': [], 'Blue Mountains': []}

                for region, terms in location_terms.items():
                    for term in terms:
                        if re.search(re.escape(term), content, re.IGNORECASE):
                            found_locations[region].append(term)

                # Report findings
                if found_locations['Sydney'] or found_locations['Blue Mountains']:
                    print(f"    Note {note_idx} - Location indicators:")
                    if found_locations['Sydney']:
                        print(f"      Sydney: {', '.join(set(found_locations['Sydney']))}")
                    if found_locations['Blue Mountains']:
                        print(f"      Blue Mountains: {', '.join(set(found_locations['Blue Mountains']))}")

                # Find context around "Grand Hotel"
                pattern = re.compile(r'Grand Hotel', re.IGNORECASE)
                matches = list(pattern.finditer(content))

                if matches:
                    print(f"    Note {note_idx} - Found 'Grand Hotel' {len(matches)} time(s)")
                    # Show first mention with context
                    match = matches[0]
                    start = max(0, match.start() - 200)
                    end = min(len(content), match.end() + 200)
                    context = content[start:end]
                    print(f"    Context: ...{context}...")
                    print()
        else:
            print(f"    No notes found")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("Review contexts above to determine:")
    print("  1. Do all items refer to the Sydney Grand Hotel?")
    print("  2. Or is there a separate Grand Hotel in the Blue Mountains?")
    print("  3. Should 'Grand Hotel' be merged with 'Grand Hotel (Sydney)'?")
    print()


if __name__ == '__main__':
    main()
