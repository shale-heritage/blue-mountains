#!/usr/bin/env python3
"""
Script 12: Analyse 'School of Arts' Usage in Full Text

Investigate how "School of Arts" is used in newspaper sources to determine
correct hierarchical classification - educational institution vs community hall.
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
    """Connect to Zotero group library."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def find_contexts(text, search_term, context_chars=100):
    """Find all occurrences of a term with surrounding context."""
    contexts = []
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)

    for match in pattern.finditer(text):
        start = match.start()
        end = match.end()

        context_start = max(0, start - context_chars)
        context_end = min(len(text), end + context_chars)

        before = text[context_start:start]
        term = text[start:end]
        after = text[end:context_end]

        before = ' '.join(before.split())
        after = ' '.join(after.split())

        context = f"...{before} **{term}** {after}..."
        contexts.append(context)

    return contexts


def analyse_school_of_arts(zot):
    """Analyse School of Arts usage."""
    print("\nFetching items with 'School of Arts' tags...")

    # Try different variations
    tags = ['School of Arts', 'Katoomba School of Arts', 'school of arts']

    all_contexts = []
    all_items = []

    for tag in tags:
        items = zot.items(tag=tag)
        if items:
            print(f"  Found {len(items)} items with tag '{tag}'")

            for item in items:
                item_key = item['key']
                item_title = item['data'].get('title', '[No Title]')

                # Fetch notes
                children = zot.children(item_key)
                notes = [child for child in children if child['data'].get('itemType') == 'note']

                full_text = ''
                for note in notes:
                    note_content = note['data'].get('note', '')
                    full_text += strip_html(note_content) + '\n'

                if full_text.strip():
                    all_items.append({
                        'title': item_title,
                        'tag': tag,
                        'text': full_text
                    })

                    # Find contexts
                    contexts = find_contexts(full_text, 'School of Arts')
                    all_contexts.extend(contexts)

    return all_items, all_contexts


def main():
    """Main execution."""
    print("="*70)
    print("SCHOOL OF ARTS CONTEXTUAL ANALYSIS")
    print("="*70)
    print()

    try:
        zot = connect_to_zotero()
        items, contexts = analyse_school_of_arts(zot)

        print(f"\nTotal items with full text: {len(items)}")
        print(f"Total contextual references: {len(contexts)}")

        print("\n" + "="*70)
        print("CONTEXTUAL EXAMPLES (showing all)")
        print("="*70)

        for i, context in enumerate(contexts, 1):
            print(f"\n{i}. {context}")

        print("\n" + "="*70)
        print("ANALYSIS")
        print("="*70)

        # Analyse contexts for keywords
        all_text = ' '.join(contexts).lower()

        educational_keywords = ['class', 'student', 'teacher', 'lesson', 'examination', 'study', 'pupil']
        community_keywords = ['meeting', 'hall', 'concert', 'entertainment', 'lecture', 'dance', 'social', 'function', 'gathering']

        educational_count = sum(all_text.count(kw) for kw in educational_keywords)
        community_count = sum(all_text.count(kw) for kw in community_keywords)

        print(f"\nKeyword analysis:")
        print(f"  Educational keywords: {educational_count}")
        print(f"  Community/hall keywords: {community_count}")

        print(f"\nRecommendation:")
        if community_count > educational_count * 2:
            print("  STRONG: School of Arts appears to be a COMMUNITY HALL/INSTITUTION")
            print("  Suggested parent: 'Community institutions' or 'Public halls'")
        elif community_count > educational_count:
            print("  MODERATE: School of Arts leans toward COMMUNITY HALL")
            print("  Suggested parent: 'Community institutions'")
        else:
            print("  UNCERTAIN: Mixed usage between educational and community functions")
            print("  Current parent 'School' may be appropriate, or create 'Halls' category")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
