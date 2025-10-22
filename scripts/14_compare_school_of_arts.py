#!/usr/bin/env python3
"""
Script 14: Compare 'School of Arts' vs 'Katoomba School of Arts'

Determine if these are:
1. The same entity (generic vs specific naming)
2. Different entities (multiple Schools of Arts in region)

Check for geographic qualifiers and whether items are about the same institution.
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
    """Remove HTML tags."""
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


def connect_to_zotero():
    """Connect to Zotero."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def analyse_tag_items(zot, tag_name):
    """Get items and geographic context for a tag."""
    print(f"\nAnalysing tag: '{tag_name}'")

    items = zot.items(tag=tag_name)
    print(f"  Found {len(items)} items")

    results = {
        'tag': tag_name,
        'item_count': len(items),
        'locations': [],
        'contexts': []
    }

    # Check for geographic qualifiers in contexts
    for item in items:
        item_title = item['data'].get('title', '[No Title]')
        item_tags = [t['tag'] for t in item['data'].get('tags', [])]

        # Check other location tags
        location_tags = [t for t in item_tags if t in [
            'Katoomba', 'Megalong', 'Lithgow', 'Wentworth Falls',
            'Leura', 'Mount Victoria', 'Blackheath', 'Hartley',
            'South Katoomba', 'Katoomba South'
        ]]

        if location_tags:
            results['locations'].extend(location_tags)

        # Get full text contexts
        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        for note in notes:
            note_content = note['data'].get('note', '')
            text = strip_html(note_content)

            # Look for "the School of Arts" vs "Katoomba School of Arts"
            # Also look for other location qualifiers
            if re.search(r'(Megalong|Lithgow|Wentworth Falls|Leura|Mount Victoria|Hartley)\s+School of Arts', text, re.IGNORECASE):
                match = re.search(r'(Megalong|Lithgow|Wentworth Falls|Leura|Mount Victoria|Hartley)\s+School of Arts', text, re.IGNORECASE)
                results['contexts'].append({
                    'item': item_title,
                    'type': 'other_location',
                    'location': match.group(1)
                })

            # Check for "the local School of Arts" (implies Katoomba context)
            if re.search(r'(the local|Katoomba)\s+School of Arts', text, re.IGNORECASE):
                results['contexts'].append({
                    'item': item_title,
                    'type': 'katoomba_qualified'
                })

    return results


def main():
    """Main execution."""
    print("="*70)
    print("SCHOOL OF ARTS TAG COMPARISON")
    print("="*70)
    print()

    try:
        zot = connect_to_zotero()

        # Analyse both tags
        generic = analyse_tag_items(zot, 'School of Arts')
        specific = analyse_tag_items(zot, 'Katoomba School of Arts')

        print("\n" + "="*70)
        print("ANALYSIS")
        print("="*70)

        # Count location tags
        from collections import Counter

        generic_locs = Counter(generic['locations'])
        specific_locs = Counter(specific['locations'])

        print(f"\n'School of Arts' ({generic['item_count']} items):")
        print(f"  Most common location tags:")
        for loc, count in generic_locs.most_common(5):
            print(f"    - {loc}: {count} items")

        # Check for non-Katoomba Schools of Arts
        other_locations = [ctx for ctx in generic['contexts'] if ctx['type'] == 'other_location']
        if other_locations:
            print(f"\n  ⚠ Found references to other Schools of Arts:")
            for ctx in other_locations:
                print(f"    - {ctx['location']} School of Arts in: {ctx['item']}")

        print(f"\n'Katoomba School of Arts' ({specific['item_count']} items):")
        print(f"  Most common location tags:")
        for loc, count in specific_locs.most_common(5):
            print(f"    - {loc}: {count} items")

        # Check for overlap
        print("\n" + "="*70)
        print("RECOMMENDATION")
        print("="*70)

        # Get item keys for overlap check
        generic_items = set(item['key'] for item in zot.items(tag='School of Arts'))
        specific_items = set(item['key'] for item in zot.items(tag='Katoomba School of Arts'))

        overlap = generic_items & specific_items

        print(f"\nItem overlap: {len(overlap)} items have BOTH tags")
        print(f"Generic only: {len(generic_items - specific_items)} items")
        print(f"Specific only: {len(specific_items - generic_items)} items")

        if other_locations:
            print("\n✗ KEEP SEPARATE")
            print("  'School of Arts' is used for multiple locations")
            print("  'Katoomba School of Arts' is specific to Katoomba")
            print("\n  However, items tagged 'School of Arts' in Katoomba context")
            print("  should ALSO be tagged 'Katoomba School of Arts'")
        elif len(generic_items - specific_items) > 0 and generic_locs.get('Katoomba', 0) > 5:
            print("\n✓ LIKELY SAME ENTITY")
            print("  'School of Arts' appears to refer to Katoomba School of Arts")
            print("  Consider: MERGE or establish HIERARCHY")
            print("    - Option A: MERGE 'School of Arts' → 'Katoomba School of Arts'")
            print("    - Option B: HIERARCHY with Katoomba School of Arts parent")
        else:
            print("\n? UNCLEAR - needs manual review of specific items")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
