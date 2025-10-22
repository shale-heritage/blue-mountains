#!/usr/bin/env python3
"""
Script 16: Analyse Church Tag Usage for Dual-Nature Pattern

Determine if church tags refer to:
1. Denomination/congregation (organisation)
2. Physical building (venue)
3. Both (dual-nature)

Check for organisational language (congregation, denomination, members, minister) vs
venue language (at the church, in the church, church building, held at).

Author: Claude Code
Date: 2025-10-19
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from pyzotero import zotero
from collections import Counter

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


def find_contexts(text, search_terms, context_chars=120):
    """Find contexts for multiple search terms."""
    all_contexts = []

    for term in search_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for match in pattern.finditer(text):
            start = match.start()
            end = match.end()

            context_start = max(0, start - context_chars)
            context_end = min(len(text), end + context_chars)

            before = text[context_start:start]
            matched = text[start:end]
            after = text[end:context_end]

            # Clean up whitespace
            before = ' '.join(before.split())
            after = ' '.join(after.split())

            context = f"...{before} **{matched}** {after}..."
            all_contexts.append({
                'term': term,
                'context': context,
                'full_match': matched
            })

    return all_contexts


def analyse_church_usage(zot, tag_name, search_terms):
    """Analyse how a church tag is referenced in full text."""
    print(f"\nAnalysing tag: '{tag_name}'")

    items = zot.items(tag=tag_name)
    print(f"  Found {len(items)} items")

    all_contexts = []

    for item in items[:20]:  # Limit to first 20 items for performance
        item_key = item['key']

        # Fetch notes
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        if full_text.strip():
            contexts = find_contexts(full_text, search_terms)
            all_contexts.extend(contexts)

    return all_contexts


def categorise_usage(contexts):
    """
    Categorise contexts as organisation vs building references.

    Organisation keywords: denomination, congregation, members, minister, clergy,
                          parish, diocese, appointed, ministry, church decided

    Venue keywords: at the church, in the church, church building, held at,
                   meeting at, service at, building, premises, hall
    """
    org_keywords = [
        'congregation', 'denomination', 'member', 'minister', 'clergy',
        'parish', 'diocese', 'appointed', 'ministry', 'reverend',
        'church decided', 'church committee', 'church meeting',
        'pastor', 'priest', 'vicar'
    ]

    venue_keywords = [
        'at the', 'in the', 'held at', 'held in', 'meeting at',
        'service at', 'building', 'premises', 'hall', 'room',
        'at church', 'in church', 'church building', 'church hall'
    ]

    org_count = 0
    building_count = 0
    ambiguous_count = 0

    org_examples = []
    building_examples = []
    ambiguous_examples = []

    for ctx in contexts:
        context_lower = ctx['context'].lower()

        has_org = any(kw in context_lower for kw in org_keywords)
        has_building = any(kw in context_lower for kw in venue_keywords)

        if has_org and not has_building:
            org_count += 1
            if len(org_examples) < 5:
                org_examples.append(ctx['context'])
        elif has_building and not has_org:
            building_count += 1
            if len(building_examples) < 5:
                building_examples.append(ctx['context'])
        else:
            ambiguous_count += 1
            if len(ambiguous_examples) < 20:
                ambiguous_examples.append(ctx['context'])

    return {
        'org_count': org_count,
        'building_count': building_count,
        'ambiguous_count': ambiguous_count,
        'org_examples': org_examples,
        'building_examples': building_examples,
        'ambiguous_examples': ambiguous_examples,
        'total_contexts': len(contexts)
    }


def main():
    """Main execution."""
    print("=" * 70)
    print("CHURCH TAG USAGE ANALYSIS - DUAL-NATURE CHECK")
    print("=" * 70)
    print()

    try:
        zot = connect_to_zotero()

        # Get all church-related tags
        print("\nFetching all tags to identify church-related entries...")
        all_tags = zot.tags()

        # Tags are returned as list of strings
        church_tags = [
            tag for tag in all_tags
            if 'church' in tag.lower() and tag not in ['Church']
        ]

        # Add the parent 'Church' tag
        church_tags_to_analyse = ['Church'] + church_tags

        print(f"Found {len(church_tags_to_analyse)} church-related tags:")
        for tag in church_tags_to_analyse:
            print(f"  - {tag}")

        # Analyse each church tag
        results = {}

        for church_tag in church_tags_to_analyse[:10]:  # Limit to first 10 for performance
            print("\n" + "=" * 70)
            print(f"ANALYSING: {church_tag}")
            print("=" * 70)

            search_terms = [church_tag]

            # Add variations
            if church_tag != 'Church':
                # Extract church name for search variations
                church_name = church_tag
                search_terms.append(church_name)

            contexts = analyse_church_usage(zot, church_tag, search_terms)

            if len(contexts) == 0:
                print(f"  ⚠ No contexts found in full text")
                continue

            analysis = categorise_usage(contexts)
            results[church_tag] = analysis

            print(f"\n  Total contexts found: {analysis['total_contexts']}")
            print(f"  Organisation references: {analysis['org_count']}")
            print(f"  Building/venue references: {analysis['building_count']}")
            print(f"  Ambiguous: {analysis['ambiguous_count']}")

            if analysis['org_examples']:
                print("\n  Organisation usage examples:")
                for ex in analysis['org_examples'][:3]:
                    print(f"    • {ex}")

            if analysis['building_examples']:
                print("\n  Building/venue usage examples:")
                for ex in analysis['building_examples'][:3]:
                    print(f"    • {ex}")

            if analysis['ambiguous_examples']:
                print("\n  Ambiguous usage examples (ALL):")
                for i, ex in enumerate(analysis['ambiguous_examples'], 1):
                    print(f"    {i}. {ex}")

        # Summary recommendations
        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)

        for church_tag, analysis in results.items():
            print(f"\n{church_tag}:")

            if analysis['org_count'] > 0 and analysis['building_count'] > 0:
                print("  ✓ DUAL NATURE: Used for both organisation and building")
                print("    → Multi-tag under both 'Religious organisations' and 'Religious buildings'")
                print(f"    → Evidence: {analysis['org_count']} org refs, {analysis['building_count']} venue refs")
            elif analysis['org_count'] > 0:
                print("  ✓ ORGANISATION ONLY: Primarily organisational references")
                print("    → Tag under 'Religious organisations' (or keep under 'Religion')")
            elif analysis['building_count'] > 0:
                print("  ✓ BUILDING ONLY: Primarily venue references")
                print("    → Tag under 'Religious buildings'")
            else:
                print("  ? UNCLEAR: Insufficient evidence from contexts")
                print("    → Manual review recommended")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
