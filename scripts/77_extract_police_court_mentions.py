#!/usr/bin/env python3
"""
Extract Police court mentions from Zotero

Quick extraction to determine if "Police court" references are all Katoomba-specific
or refer to generic/multiple courts.
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
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


def connect_to_zotero():
    """Connect to Zotero."""
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def extract_context(text: str, entity_name: str, context_chars: int = 400) -> list:
    """Extract context around ALL mentions of entity."""
    import re

    # Create flexible pattern for court references
    patterns = [
        re.compile(r'\bPolice\s+[Cc]ourt\b', re.IGNORECASE),
        re.compile(r'\b[Cc]ourt\s+of\s+Petty\s+Sessions?\b', re.IGNORECASE),
        re.compile(r'\bPetty\s+Sessions?\b', re.IGNORECASE)
    ]

    contexts = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            # Extract context
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            context = text[start:end]

            # Clean up
            context = ' '.join(context.split())

            contexts.append({
                'match': match.group(),
                'context': context
            })

    return contexts


def main():
    print("=" * 80)
    print("EXTRACT POLICE COURT MENTIONS")
    print("=" * 80)

    # Connect to Zotero
    print("\nConnecting to Zotero...")
    zot = connect_to_zotero()

    # Get all items tagged with "Police court"
    print("Searching for items tagged 'Police court'...")
    items = zot.everything(zot.items(tag='Police court'))
    print(f"Found {len(items)} items")

    # Extract mentions
    all_mentions = []

    for item in items:
        item_data = item.get('data', {})
        title = item_data.get('title', 'Untitled')
        date = item_data.get('date', 'No date')

        # Get full text from notes
        full_text = ""

        # Check if item has attachment with note
        children = zot.children(item['key'])
        for child in children:
            if child['data'].get('itemType') == 'note':
                note_html = child['data'].get('note', '')
                full_text += strip_html(note_html) + " "

        # Extract all contexts
        if full_text.strip():
            contexts = extract_context(full_text, "Police court")
            if contexts:
                for ctx in contexts:
                    all_mentions.append({
                        'title': title,
                        'date': date,
                        'match': ctx['match'],
                        'context': ctx['context'],
                        'item_key': item['key']
                    })

    # Display results
    print(f"\nFound {len(all_mentions)} mentions across {len(items)} items\n")
    print("=" * 80)

    for i, mention in enumerate(all_mentions, 1):
        print(f"\nMention {i}")
        print(f"Title: {mention['title']}")
        print(f"Date: {mention['date']}")
        print(f"Match: {mention['match']}")
        print(f"Context: ...{mention['context']}...")
        print("-" * 80)

    # Save to JSON
    output_file = Path('data/entity_classification/police_court_mentions.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_mentions, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved to: {output_file}")

    # Quick analysis summary
    print("\n" + "=" * 80)
    print("QUICK ANALYSIS")
    print("=" * 80)

    # Check for location keywords
    katoomba_count = 0
    penrith_count = 0
    blackheath_count = 0
    other_location = 0

    for mention in all_mentions:
        context_lower = mention['context'].lower()
        if 'katoomba' in context_lower:
            katoomba_count += 1
        elif 'penrith' in context_lower:
            penrith_count += 1
        elif 'blackheath' in context_lower:
            blackheath_count += 1
        else:
            # Look for other location indicators
            if any(loc in context_lower for loc in ['mount victoria', 'springwood',
                                                     'lawson', 'leura', 'wentworth']):
                other_location += 1

    print(f"\nLocation analysis:")
    print(f"  Mentions with 'Katoomba': {katoomba_count}/{len(all_mentions)}")
    print(f"  Mentions with 'Penrith': {penrith_count}/{len(all_mentions)}")
    print(f"  Mentions with 'Blackheath': {blackheath_count}/{len(all_mentions)}")
    print(f"  Mentions with other Blue Mountains locations: {other_location}/{len(all_mentions)}")
    print(f"  Mentions with no clear location: {len(all_mentions) - katoomba_count - penrith_count - blackheath_count - other_location}/{len(all_mentions)}")

    if katoomba_count > len(all_mentions) * 0.8:
        print("\n✓ Strong evidence: Most references are Katoomba-specific")
        print("   → Recommend: 'Police Court' → 'Katoomba Court of Petty Sessions'")
    elif katoomba_count > len(all_mentions) * 0.5:
        print("\n⚠ Mixed evidence: Majority Katoomba but some ambiguity")
        print("   → Recommend: Manual review of non-Katoomba contexts")
    else:
        print("\n⚠ Generic usage: References span multiple locations")
        print("   → Recommend: Keep generic 'Court of Petty Sessions'")


if __name__ == '__main__':
    main()
