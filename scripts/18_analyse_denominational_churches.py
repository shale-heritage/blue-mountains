#!/usr/bin/env python3
"""
Script 18: Analyse Individual Denominational Churches for Dual-Nature Pattern

Analyse each specific denominational church to determine if it shows dual-nature usage:
1. Organisation/congregation (religious services, leadership, church decisions)
2. Physical venue (events held at the church, concerts, lectures)

Churches to analyse:
- Wesleyan Church
- Methodist Church
- Congregational Church
- Katoomba Congregational Church
- Roman Catholic Church (already done - venue only)
- St Hilda's Church

Pattern identified from generic "Church" analysis:
- Events at churches (lectures, concerts, meetings) = VENUE
- Religious services & leadership (sermons, deacon, minister, services) = ORGANISATION

Author: Claude Code
Date: 2025-10-19
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

    if len(items) == 0:
        return []

    all_contexts = []

    # Analyse all items for smaller collections, limit to 30 for larger
    items_to_check = min(len(items), 30)

    for item in items[:items_to_check]:
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
    Categorise contexts using the pattern identified from user training:

    ORGANISATION indicators:
    - Religious services: sermon, service, preach, worship, mass
    - Leadership: minister, deacon, elder, pastor, priest, reverend
    - Church activities: church decided, church donated, church committee
    - Attendance/membership: go to church, church member

    VENUE indicators:
    - Events held: concert in/at, lecture at, meeting at, held in
    - Physical references: church building, at the church (for non-religious events)
    - Directions: drive to the church, at the church (as location)

    BOTH indicators:
    - Dedication/opening of new church
    - Church decorated for service
    """
    org_keywords = [
        'sermon', 'service', 'preach', 'worship', 'mass',
        'minister', 'deacon', 'elder', 'pastor', 'priest', 'reverend',
        'church decided', 'church donated', 'church committee',
        'go to church', 'church member', 'congregation', 'parish',
        'officiate', 'services conducted', 'services will be'
    ]

    venue_keywords = [
        'concert in', 'concert at', 'lecture at', 'lecture in',
        'meeting at', 'meeting in', 'held at', 'held in',
        'drive to', 'at the church', 'in the church',
        'church hall', 'available for'
    ]

    both_keywords = [
        'dedication', 'opening', 'decorated', 'new church'
    ]

    org_count = 0
    venue_count = 0
    both_count = 0
    unclear_count = 0

    org_examples = []
    venue_examples = []
    both_examples = []
    unclear_examples = []

    for ctx in contexts:
        context_lower = ctx['context'].lower()

        has_org = any(kw in context_lower for kw in org_keywords)
        has_venue = any(kw in context_lower for kw in venue_keywords)
        has_both = any(kw in context_lower for kw in both_keywords)

        if has_both:
            both_count += 1
            if len(both_examples) < 3:
                both_examples.append(ctx['context'])
        elif has_org and not has_venue:
            org_count += 1
            if len(org_examples) < 5:
                org_examples.append(ctx['context'])
        elif has_venue and not has_org:
            venue_count += 1
            if len(venue_examples) < 5:
                venue_examples.append(ctx['context'])
        else:
            unclear_count += 1
            if len(unclear_examples) < 5:
                unclear_examples.append(ctx['context'])

    return {
        'org_count': org_count,
        'venue_count': venue_count,
        'both_count': both_count,
        'unclear_count': unclear_count,
        'org_examples': org_examples,
        'venue_examples': venue_examples,
        'both_examples': both_examples,
        'unclear_examples': unclear_examples,
        'total_contexts': len(contexts)
    }


def main():
    """Main execution."""
    print("=" * 70)
    print("DENOMINATIONAL CHURCH ANALYSIS - DUAL-NATURE CHECK")
    print("=" * 70)
    print()

    try:
        zot = connect_to_zotero()

        # Churches to analyse individually
        churches_to_analyse = [
            'Wesleyan Church',
            'Methodist Church',
            'Congregational Church',
            'Katoomba Congregational Church',
            'St Hilda\'s Church'
        ]

        print(f"\nAnalysing {len(churches_to_analyse)} denominational churches:")
        for church in churches_to_analyse:
            print(f"  - {church}")

        # Results storage
        results = {}

        # Analyse each church
        for church_tag in churches_to_analyse:
            print("\n" + "=" * 70)
            print(f"ANALYSING: {church_tag}")
            print("=" * 70)

            search_terms = [church_tag]

            contexts = analyse_church_usage(zot, church_tag, search_terms)

            if len(contexts) == 0:
                print(f"  ⚠ No contexts found in full text")
                results[church_tag] = None
                continue

            analysis = categorise_usage(contexts)
            results[church_tag] = analysis

            print(f"\n  Total contexts found: {analysis['total_contexts']}")
            print(f"  Organisation references: {analysis['org_count']}")
            print(f"  Venue references: {analysis['venue_count']}")
            print(f"  Both (dedication/ceremony): {analysis['both_count']}")
            print(f"  Unclear: {analysis['unclear_count']}")

            if analysis['org_examples']:
                print("\n  Organisation usage examples:")
                for ex in analysis['org_examples'][:3]:
                    print(f"    • {ex}")

            if analysis['venue_examples']:
                print("\n  Venue usage examples:")
                for ex in analysis['venue_examples'][:3]:
                    print(f"    • {ex}")

            if analysis['both_examples']:
                print("\n  Both (dedication/ceremony) examples:")
                for ex in analysis['both_examples'][:2]:
                    print(f"    • {ex}")

            if analysis['unclear_examples']:
                print("\n  Unclear examples (need manual review):")
                for ex in analysis['unclear_examples'][:3]:
                    print(f"    • {ex}")

        # Summary recommendations
        print("\n" + "=" * 70)
        print("SUMMARY RECOMMENDATIONS")
        print("=" * 70)
        print()

        dual_nature_churches = []
        org_only_churches = []
        venue_only_churches = []
        insufficient_data_churches = []

        for church_tag, analysis in results.items():
            if analysis is None:
                insufficient_data_churches.append(church_tag)
                continue

            total_clear = analysis['org_count'] + analysis['venue_count']

            if total_clear == 0:
                insufficient_data_churches.append(church_tag)
            elif analysis['org_count'] > 0 and analysis['venue_count'] > 0:
                dual_nature_churches.append(church_tag)
            elif analysis['org_count'] > 0:
                org_only_churches.append(church_tag)
            elif analysis['venue_count'] > 0:
                venue_only_churches.append(church_tag)

        print("\n** DUAL NATURE (multi-tag under Religious organisations + Religious buildings):")
        if dual_nature_churches:
            for church in dual_nature_churches:
                print(f"  ✓ {church}")
                print(f"    Org: {results[church]['org_count']}, Venue: {results[church]['venue_count']}")
        else:
            print("  (none found)")

        print("\n** ORGANISATION ONLY (tag under Religious organisations):")
        if org_only_churches:
            for church in org_only_churches:
                print(f"  ✓ {church}")
                print(f"    Org: {results[church]['org_count']}, Venue: 0")
        else:
            print("  (none found)")

        print("\n** VENUE ONLY (tag under Religious buildings):")
        if venue_only_churches:
            for church in venue_only_churches:
                print(f"  ✓ {church}")
                print(f"    Org: 0, Venue: {results[church]['venue_count']}")
        else:
            print("  (none found)")

        print("\n** INSUFFICIENT DATA:")
        if insufficient_data_churches:
            for church in insufficient_data_churches:
                print(f"  ? {church} - no clear contexts found, default to dual-nature")
        else:
            print("  (all churches have sufficient data)")

        print("\n" + "=" * 70)
        print("NEXT STEPS")
        print("=" * 70)
        print()
        print("1. Review unclear examples above and categorise manually if needed")
        print("2. Update taxonomy CSV with dual-nature multi-tagging for identified churches")
        print("3. Create 'Religious organisations' and 'Religious buildings' subcategories under Religion")
        print()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
