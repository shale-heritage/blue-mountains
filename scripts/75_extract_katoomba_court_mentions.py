#!/usr/bin/env python3
"""
Extract Katoomba Court mentions from Zotero

Quick extraction to determine if "Katoomba Court" refers to Court of Petty Sessions
or something else (building, etc.).
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


def extract_context(text: str, entity_name: str, context_chars: int = 400) -> str:
    """Extract context around first mention of entity."""
    import re

    # Create flexible pattern for "Katoomba Court"
    pattern = re.compile(r'\bKatoomba\s+Court\b', re.IGNORECASE)

    match = pattern.search(text)
    if not match:
        return None

    # Extract context
    start = max(0, match.start() - context_chars)
    end = min(len(text), match.end() + context_chars)
    context = text[start:end]

    # Clean up
    context = ' '.join(context.split())

    return context


def main():
    print("=" * 80)
    print("EXTRACT KATOOMBA COURT MENTIONS")
    print("=" * 80)

    # Connect to Zotero
    print("\nConnecting to Zotero...")
    zot = connect_to_zotero()

    # Get all items tagged with "Katoomba Court"
    print("Searching for items tagged 'Katoomba Court'...")
    items = zot.everything(zot.items(tag='Katoomba Court'))
    print(f"Found {len(items)} items")

    # Extract mentions
    mentions = []

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

        # Extract context
        if full_text.strip():
            context = extract_context(full_text, "Katoomba Court")
            if context:
                mentions.append({
                    'title': title,
                    'date': date,
                    'context': context,
                    'item_key': item['key']
                })

    # Display results
    print(f"\nFound {len(mentions)} mentions with context\n")
    print("=" * 80)

    for i, mention in enumerate(mentions, 1):
        print(f"\nMention {i}")
        print(f"Title: {mention['title']}")
        print(f"Date: {mention['date']}")
        print(f"Context: ...{mention['context']}...")
        print("-" * 80)

    # Save to JSON
    output_file = Path('data/entity_classification/katoomba_court_mentions.json')
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mentions, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Saved to: {output_file}")

    # Quick analysis summary
    print("\n" + "=" * 80)
    print("QUICK ANALYSIS")
    print("=" * 80)

    # Check for keywords
    petty_sessions_count = 0
    courthouse_count = 0
    building_count = 0

    for mention in mentions:
        context_lower = mention['context'].lower()
        if 'petty session' in context_lower:
            petty_sessions_count += 1
        if 'courthouse' in context_lower or 'court house' in context_lower:
            courthouse_count += 1
        if 'building' in context_lower or 'premises' in context_lower:
            building_count += 1

    print(f"\nKeyword analysis:")
    print(f"  Mentions with 'petty session': {petty_sessions_count}/{len(mentions)}")
    print(f"  Mentions with 'courthouse/court house': {courthouse_count}/{len(mentions)}")
    print(f"  Mentions with 'building/premises': {building_count}/{len(mentions)}")

    if petty_sessions_count > len(mentions) * 0.5:
        print("\n✓ Likely refers to Court of Petty Sessions (institution)")
    elif courthouse_count > 0:
        print("\n⚠ May have dual nature (institution + building)")
    else:
        print("\n? Unclear - needs manual review")


if __name__ == '__main__':
    main()
