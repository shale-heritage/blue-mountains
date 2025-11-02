#!/usr/bin/env python3
"""
Check full text of specific item for club mentions.

Retrieves full text of "At Katoomba (1893-11-10)" to determine whether
Katoomba Cricket Club and/or Megalong Cricket Club are actually mentioned.
"""

import sys
from pathlib import Path
from html.parser import HTMLParser

sys.path.append(str(Path(__file__).parent))
import config

from pyzotero import zotero


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


def main():
    """Main execution."""
    print("=" * 80)
    print("CHECKING FULL TEXT: At Katoomba (1893-11-10)")
    print("=" * 80)
    print()

    # Connect to Zotero
    print("Connecting to Zotero API...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )

    # Search for the item by tag (more efficient)
    print("Searching for items tagged 'Katoomba Cricket Club'...")
    items = zot.items(tag='Katoomba Cricket Club')

    target_item = None
    for item in items:
        title = item['data'].get('title', '')
        date = item['data'].get('date', '')

        if 'At Katoomba' in title and ('1893-11-10' in date or '10 November 1893' in date or '1893' in date):
            target_item = item
            print(f"  Candidate: {title} ({date})")
            break

    # Also try Megalong Cricket Club tag if not found
    if not target_item:
        print("Searching for items tagged 'Megalong Cricket Club'...")
        items = zot.items(tag='Megalong Cricket Club')

        for item in items:
            title = item['data'].get('title', '')
            date = item['data'].get('date', '')

            if 'At Katoomba' in title and ('1893-11-10' in date or '10 November 1893' in date or '1893' in date):
                target_item = item
                print(f"  Candidate: {title} ({date})")
                break

    if not target_item:
        print("✗ Item not found")
        return

    print(f"✓ Found item: {target_item['data']['title']}")
    print(f"  Date: {target_item['data']['date']}")
    print(f"  Item key: {target_item['key']}")

    # Get current tags
    tags = target_item['data'].get('tags', [])
    print(f"\n  Current tags ({len(tags)}):")
    for tag in tags:
        tag_name = tag.get('tag', '')
        if 'cricket' in tag_name.lower() or 'sport' in tag_name.lower():
            print(f"    - {tag_name}")

    # Get full text from children
    print("\nRetrieving full text from attachments/notes...")
    children = zot.children(target_item['key'])
    notes = [child for child in children if child['data'].get('itemType') == 'note']

    full_text = ''
    for note in notes:
        note_content = note['data'].get('note', '')
        full_text += strip_html(note_content) + '\n'

    if not full_text.strip():
        print("✗ No full text available")
        return

    print(f"✓ Retrieved {len(full_text)} characters of text")

    # Search for club mentions
    print("\n" + "=" * 80)
    print("SEARCHING FOR CLUB MENTIONS")
    print("=" * 80)
    print()

    search_terms = {
        'Katoomba Cricket Club': 'Katoomba Cricket Club',
        'Megalong Cricket Club': 'Megalong Cricket Club',
        'cricket club': 'cricket club (generic)',
        'Cricket Club': 'Cricket Club (capitalized)',
        'Kelly Gang': 'Kelly Gang (team name)',
        'town v. mines': 'town v. mines (match)',
        'town versus mines': 'town versus mines (match)',
    }

    found_any = False
    for term, description in search_terms.items():
        if term.lower() in full_text.lower():
            print(f"✓ FOUND: {description}")
            found_any = True

            # Find context
            term_lower = term.lower()
            text_lower = full_text.lower()
            pos = text_lower.find(term_lower)

            while pos != -1:
                start = max(0, pos - 150)
                end = min(len(full_text), pos + len(term) + 150)

                before = full_text[start:pos]
                match = full_text[pos:pos + len(term)]
                after = full_text[pos + len(term):end]

                # Clean whitespace
                before = ' '.join(before.split())
                after = ' '.join(after.split())

                print(f"  Context: ...{before} **{match}** {after}...")
                print()

                # Find next occurrence
                pos = text_lower.find(term_lower, pos + 1)

    if not found_any:
        print("✗ No club-specific mentions found")
        print("\nThis item appears to be tagged with club names incorrectly.")
        print("The excerpt shows a cricket match ('town v. mines') but no club references.")

    print("\n" + "=" * 80)
    print("FULL TEXT")
    print("=" * 80)
    print()
    print(full_text)


if __name__ == '__main__':
    main()
