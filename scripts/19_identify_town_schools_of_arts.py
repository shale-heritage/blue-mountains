#!/usr/bin/env python3
"""
Script 19: Identify Town-Specific Schools of Arts from Generic Tag

Analyse items tagged "School of Arts" (generic) to determine if they reference
specific town Schools of Arts based on:

1. Full text context (primary evidence)
2. Co-occurring location tags
3. Web search verification (if needed)

Goal: Create town-specific tags like:
- Blackheath School of Arts
- Leura School of Arts
- Mount Victoria School of Arts
- etc.

Following the pattern established for "Katoomba School of Arts".

Author: Claude Code
Date: 2025-10-19
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from pyzotero import zotero
from collections import Counter, defaultdict

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
    """Connect to Zotero API."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def find_town_references(text, towns):
    """
    Find which towns are mentioned in the text with School of Arts.

    Returns dict of {town: list of contexts}
    """
    results = defaultdict(list)

    # Look for "[Town] School of Arts" patterns
    for town in towns:
        # Pattern: Town name followed by "School of Arts"
        pattern = re.compile(
            rf'\b{re.escape(town)}\s+School\s+of\s+Arts\b',
            re.IGNORECASE
        )

        for match in pattern.finditer(text):
            start = max(0, match.start() - 120)
            end = min(len(text), match.end() + 120)

            context = text[start:end]
            context = ' '.join(context.split())

            results[town].append(context)

    return results


def analyse_school_of_arts_items(zot):
    """Analyse all items tagged 'School of Arts' for town associations."""

    print("\nAnalysing 'School of Arts' tag...")
    items = zot.items(tag='School of Arts')
    print(f"  Found {len(items)} items")

    # Blue Mountains towns to check
    towns = [
        'Blackheath',
        'Leura',
        'Mount Victoria',
        'Megalong',
        'Wentworth Falls',
        'Hartley',
        'Lithgow',
        'Katoomba'  # Include for completeness, though it has its own tag
    ]

    # Track evidence for each town
    town_evidence = defaultdict(lambda: {
        'item_count': 0,
        'context_count': 0,
        'contexts': [],
        'items': [],
        'location_tags': Counter()
    })

    generic_references = []

    for item in items:
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')

        # Get location tags
        item_tags = [t['tag'] for t in item['data'].get('tags', [])]
        location_tags = [t for t in item_tags if t in towns]

        # Get full text
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        if not full_text.strip():
            continue

        # Find town-specific references in text
        town_refs = find_town_references(full_text, towns)

        # Check for generic "the School of Arts" (not town-specific)
        generic_pattern = re.compile(
            r'\bthe\s+School\s+of\s+Arts\b',
            re.IGNORECASE
        )
        has_generic = bool(generic_pattern.search(full_text))

        # Categorise this item
        if town_refs:
            # Has explicit town-specific reference
            for town, contexts in town_refs.items():
                town_evidence[town]['item_count'] += 1
                town_evidence[town]['context_count'] += len(contexts)
                town_evidence[town]['contexts'].extend(contexts[:2])  # Max 2 per item
                town_evidence[town]['items'].append({
                    'title': item_title,
                    'key': item_key,
                    'location_tags': location_tags
                })
        elif location_tags and has_generic:
            # Has location tag and generic reference - infer association
            for loc_tag in location_tags:
                town_evidence[loc_tag]['item_count'] += 1
                town_evidence[loc_tag]['items'].append({
                    'title': item_title,
                    'key': item_key,
                    'location_tags': location_tags,
                    'inferred': True
                })
        else:
            # Truly generic - no town association
            generic_references.append({
                'title': item_title,
                'key': item_key,
                'location_tags': location_tags
            })

        # Track location tag co-occurrence
        for loc_tag in location_tags:
            town_evidence[loc_tag]['location_tags'][loc_tag] += 1

    return town_evidence, generic_references


def main():
    """Main execution."""
    print("=" * 70)
    print("TOWN-SPECIFIC SCHOOLS OF ARTS IDENTIFICATION")
    print("=" * 70)
    print()

    try:
        zot = connect_to_zotero()

        town_evidence, generic_refs = analyse_school_of_arts_items(zot)

        # Display results
        print("\n" + "=" * 70)
        print("RESULTS: TOWN ASSOCIATIONS FOUND")
        print("=" * 70)

        strong_associations = {}
        weak_associations = {}

        for town, evidence in sorted(town_evidence.items()):
            if evidence['item_count'] == 0:
                continue

            print(f"\n{town} School of Arts:")
            print(f"  Items: {evidence['item_count']}")
            print(f"  Explicit text references: {evidence['context_count']}")

            if evidence['contexts']:
                print(f"\n  Context examples:")
                for ctx in evidence['contexts'][:2]:
                    print(f"    • {ctx}")

            if evidence['items']:
                print(f"\n  Items:")
                for item_info in evidence['items'][:3]:
                    inferred = " (INFERRED from location tag)" if item_info.get('inferred') else ""
                    print(f"    - {item_info['title']}{inferred}")

                if len(evidence['items']) > 3:
                    print(f"    ... and {len(evidence['items']) - 3} more")

            # Classify strength of association
            if evidence['context_count'] >= 2:
                strong_associations[town] = evidence
                print(f"\n  ✓ STRONG ASSOCIATION - Create '{town} School of Arts' tag")
            elif evidence['context_count'] == 1:
                strong_associations[town] = evidence
                print(f"\n  ✓ MODERATE ASSOCIATION - Create '{town} School of Arts' tag")
            else:
                weak_associations[town] = evidence
                print(f"\n  ? WEAK ASSOCIATION - Inferred only from location tags")

        # Generic references
        print("\n" + "=" * 70)
        print("GENERIC REFERENCES (No town association)")
        print("=" * 70)
        print(f"\nFound {len(generic_refs)} items with generic 'School of Arts' references")
        if generic_refs:
            print("\nExamples:")
            for item_info in generic_refs[:3]:
                locs = f" (locations: {', '.join(item_info['location_tags'])})" if item_info['location_tags'] else ""
                print(f"  - {item_info['title']}{locs}")

        # Summary recommendations
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)
        print()

        print("** STRONG/MODERATE - Create these town-specific tags:")
        if strong_associations:
            for town in sorted(strong_associations.keys()):
                evidence = strong_associations[town]
                print(f"  ✓ {town} School of Arts ({evidence['item_count']} items, {evidence['context_count']} text refs)")
        else:
            print("  (none found)")

        print("\n** WEAK - Need manual review or web search verification:")
        if weak_associations:
            for town in sorted(weak_associations.keys()):
                evidence = weak_associations[town]
                print(f"  ? {town} School of Arts ({evidence['item_count']} items, inferred from location tags)")
                print(f"    → Web search: '{town} School of Arts Blue Mountains history'")
        else:
            print("  (none found)")

        print("\n** ACTION: Review weak associations and generic references")
        print("   Some may need context shown for manual categorization")
        print()

        # Return data for potential web search or further analysis
        return {
            'strong': strong_associations,
            'weak': weak_associations,
            'generic': generic_refs
        }

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
