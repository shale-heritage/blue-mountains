#!/usr/bin/env python3
"""
Script 30: Detailed Alcohol Context Analysis

This script provides detailed analysis of each item tagged "Alcohol" by
searching for alcohol-related keywords in the full text and extracting
relevant context. This helps determine appropriate replacement tags.

Outputs:
    - Console output with keyword-in-context analysis
    - Updated alcohol_rationalisation_report.md with specific recommendations

Usage:
    python scripts/30_analyse_alcohol_contexts.py
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402

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


def find_alcohol_contexts(text):
    """
    Search for alcohol-related keywords in text and extract context.

    Returns:
        list: Tuples of (keyword, context_string)
    """
    # Alcohol-related keywords
    keywords = [
        'alcohol', 'drink', 'drank', 'drunk', 'drunkenness', 'drunkeness',
        'liquor', 'whisky', 'whiskey', 'wine', 'beer', 'grog',
        'publican', 'hotel', 'pub', 'inn', 'tavern',
        'temperance', 'teetotal', 'abstinence',
        'licence', 'license', 'licensing',
        'intoxicat', 'inebriat', 'tipsy', 'sober'
    ]

    contexts = []
    for keyword in keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\w*', re.IGNORECASE)
        for match in pattern.finditer(text):
            start = match.start()
            end = match.end()

            # Extract 80 chars before and after
            context_start = max(0, start - 80)
            context_end = min(len(text), end + 80)

            before = text[context_start:start]
            term = text[start:end]
            after = text[end:context_end]

            # Clean whitespace
            before = ' '.join(before.split())
            after = ' '.join(after.split())

            context_str = f"...{before} **{term}** {after}..."
            contexts.append((term, context_str))

    return contexts


def main():
    """Analyse each Alcohol-tagged item in detail."""
    print("=" * 70)
    print("ALCOHOL TAG - DETAILED CONTEXT ANALYSIS")
    print("=" * 70)
    print()

    zot = connect_to_zotero()

    items = zot.items(tag='Alcohol')
    print(f"Analysing {len(items)} items...\n")

    for idx, item in enumerate(items, 1):
        title = item['data'].get('title', '[No Title]')
        date = item['data'].get('date', '')

        print(f"\n{'=' * 70}")
        print(f"{idx}. {title}")
        print(f"Date: {date}")
        print('=' * 70)

        # Get full text
        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        if not full_text.strip():
            print("NO FULL TEXT AVAILABLE")
            continue

        # Find alcohol contexts
        contexts = find_alcohol_contexts(full_text)

        if contexts:
            print(f"\nFound {len(contexts)} alcohol-related references:")
            for keyword, context in contexts[:5]:  # Show first 5
                print(f"\n  Keyword: {keyword}")
                print(f"  {context}")
        else:
            print("\nNO ALCOHOL KEYWORDS FOUND IN TEXT")
            print("(Tag may be incorrect or keyword list incomplete)")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == '__main__':
    main()
