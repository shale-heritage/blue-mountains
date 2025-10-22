#!/usr/bin/env python3
"""
Script 13: Check Lodge vs Hall Usage

Determine if "Odd Fellows" and "Masons/Masonic" are used to refer to:
1. The organisation (lodge/society)
2. The building (hall)
3. Both

This determines whether we need separate tags or multi-tagging.
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

            before = ' '.join(before.split())
            after = ' '.join(after.split())

            context = f"...{before} **{matched}** {after}..."
            all_contexts.append({
                'term': term,
                'context': context,
                'full_match': matched
            })

    return all_contexts


def analyse_lodge_usage(zot, tag_name, search_terms):
    """Analyse how a lodge/hall is referenced."""
    print(f"\nAnalysing tag: '{tag_name}'")

    items = zot.items(tag=tag_name)
    print(f"  Found {len(items)} items")

    all_contexts = []

    for item in items:
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
    """Categorise contexts as organisation vs building references."""
    org_keywords = ['member', 'society', 'lodge', 'order', 'brother', 'grand master',
                    'meeting of', 'initiation', 'ceremony']
    building_keywords = ['hall', 'building', 'room', 'held at', 'held in',
                         'at the', 'in the', 'premises']

    org_count = 0
    building_count = 0
    ambiguous_count = 0

    org_examples = []
    building_examples = []

    for ctx in contexts:
        context_lower = ctx['context'].lower()

        has_org = any(kw in context_lower for kw in org_keywords)
        has_building = any(kw in context_lower for kw in building_keywords)

        if has_org and not has_building:
            org_count += 1
            if len(org_examples) < 3:
                org_examples.append(ctx['context'])
        elif has_building and not has_org:
            building_count += 1
            if len(building_examples) < 3:
                building_examples.append(ctx['context'])
        else:
            ambiguous_count += 1

    return {
        'org_count': org_count,
        'building_count': building_count,
        'ambiguous_count': ambiguous_count,
        'org_examples': org_examples,
        'building_examples': building_examples
    }


def main():
    """Main execution."""
    print("="*70)
    print("LODGE VS HALL USAGE ANALYSIS")
    print("="*70)
    print()

    try:
        zot = connect_to_zotero()

        # Analyse Odd Fellows' Hall
        print("\n" + "="*70)
        print("1. ODD FELLOWS' HALL")
        print("="*70)

        oddfellows_contexts = analyse_lodge_usage(
            zot,
            "Odd Fellows' Hall",
            ["Odd Fellows' Hall", "Odd Fellows", "Oddfellows", "IOOF", "I.O.O.F."]
        )

        oddfellows_analysis = categorise_usage(oddfellows_contexts)

        print(f"\n  Organisation references: {oddfellows_analysis['org_count']}")
        print(f"  Building references: {oddfellows_analysis['building_count']}")
        print(f"  Ambiguous: {oddfellows_analysis['ambiguous_count']}")

        if oddfellows_analysis['org_examples']:
            print("\n  Organisation usage examples:")
            for ex in oddfellows_analysis['org_examples']:
                print(f"    - {ex}")

        if oddfellows_analysis['building_examples']:
            print("\n  Building usage examples:")
            for ex in oddfellows_analysis['building_examples']:
                print(f"    - {ex}")

        # Analyse I.O.O.F. Hall
        print("\n" + "="*70)
        print("2. I.O.O.F. HALL")
        print("="*70)

        ioof_contexts = analyse_lodge_usage(
            zot,
            "I.O.O.F. Hall",
            ["I.O.O.F. Hall", "IOOF Hall", "Odd Fellows' Hall", "Odd Fellows"]
        )

        ioof_analysis = categorise_usage(ioof_contexts)

        print(f"\n  Organisation references: {ioof_analysis['org_count']}")
        print(f"  Building references: {ioof_analysis['building_count']}")
        print(f"  Ambiguous: {ioof_analysis['ambiguous_count']}")

        # Analyse Masonic Hall
        print("\n" + "="*70)
        print("3. MASONIC HALL")
        print("="*70)

        masonic_contexts = analyse_lodge_usage(
            zot,
            "Masonic Hall",
            ["Masonic Hall", "Masons", "Freemasons", "Masonic"]
        )

        masonic_analysis = categorise_usage(masonic_contexts)

        print(f"\n  Organisation references: {masonic_analysis['org_count']}")
        print(f"  Building references: {masonic_analysis['building_count']}")
        print(f"  Ambiguous: {masonic_analysis['ambiguous_count']}")

        if masonic_analysis['org_examples']:
            print("\n  Organisation usage examples:")
            for ex in masonic_analysis['org_examples']:
                print(f"    - {ex}")

        if masonic_analysis['building_examples']:
            print("\n  Building usage examples:")
            for ex in masonic_analysis['building_examples']:
                print(f"    - {ex}")

        # Summary recommendations
        print("\n" + "="*70)
        print("RECOMMENDATIONS")
        print("="*70)

        print("\nOdd Fellows' Hall:")
        if oddfellows_analysis['org_count'] > 0:
            print("  ✓ DUAL NATURE: Used for both organisation and building")
            print("    → Multi-tag: Lodges + Halls")
        else:
            print("  ✓ BUILDING ONLY: Only building references found")
            print("    → Single tag: Halls only")

        print("\nI.O.O.F. Hall:")
        print(f"  → MERGE to 'Odd Fellows' Hall' (same organisation/building)")

        print("\nMasonic Hall:")
        if masonic_analysis['org_count'] > 0:
            print("  ✓ DUAL NATURE: Used for both organisation and building")
            print("    → Multi-tag: Lodges + Halls")
        else:
            print("  ✓ BUILDING ONLY: Only building references found")
            print("    → Single tag: Halls only")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
