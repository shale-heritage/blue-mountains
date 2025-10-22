#!/usr/bin/env python3
"""
Script 08: Check Full Text Availability in Zotero Notes

This script investigates whether newspaper article full text is stored in Zotero
notes as per Research Assistant (RA) protocol. If available, this full text can
be used for contextual analysis to disambiguate naming variants (e.g., is "south
katoomba" a distinct district name or just a directional descriptor?).

Research Question:
When RAs tagged articles, did they include full text in notes? If so, we can
analyse term usage in context rather than relying on tag names alone.

Usage:
    python scripts/08_check_full_text_availability.py

Outputs:
    - Console report on full text availability
    - Sample of full text if found
"""

import sys
from pathlib import Path
from pyzotero import zotero

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def connect_to_zotero():
    """Connect to Zotero group library via Application Programming Interface (API)."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def check_items_with_tags(zot, tag_names):
    """
    Fetch items with specific tags and check if they have notes with full text.

    Parameters:
        zot: Authenticated Zotero client
        tag_names: List of tag names to search for

    Returns:
        dict: Report on full text availability
    """
    print(f"\nChecking items tagged with: {', '.join(tag_names)}")

    results = {
        'items_checked': 0,
        'items_with_notes': 0,
        'notes_with_text': 0,
        'sample_texts': []
    }

    # Fetch items with any of the specified tags
    for tag in tag_names:
        print(f"\n  Fetching items with tag '{tag}'...")
        items = zot.items(tag=tag, limit=5)  # Limit to 5 items per tag for quick check

        for item in items:
            results['items_checked'] += 1
            item_key = item['key']
            item_title = item['data'].get('title', '[No Title]')

            print(f"    - {item_title[:60]}...")

            # Fetch child items (notes and attachments)
            children = zot.children(item_key)

            # Check for notes
            notes = [child for child in children if child['data'].get('itemType') == 'note']

            if notes:
                results['items_with_notes'] += 1
                print(f"      Found {len(notes)} note(s)")

                for note in notes:
                    note_content = note['data'].get('note', '')
                    if note_content and len(note_content) > 100:  # Substantive text
                        results['notes_with_text'] += 1

                        # Store sample (first 500 chars)
                        results['sample_texts'].append({
                            'item_title': item_title,
                            'tag': tag,
                            'text_length': len(note_content),
                            'sample': note_content[:500]
                        })

                        print(f"      Note has {len(note_content):,} characters")
            else:
                print(f"      No notes found")

    return results


def main():
    """Main execution function."""
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - FULL TEXT AVAILABILITY CHECK")
    print("Script 08: Check if full text is stored in Zotero notes")
    print("="*70)
    print()

    try:
        # Connect to Zotero
        zot = connect_to_zotero()

        # Check items with naming variant tags we want to analyse
        tags_to_check = [
            'south katoomba',
            'katoomba',
            'katoomba south coal mining company',
            'Druid\'s Lodge',
            'Druids Lodge'
        ]

        results = check_items_with_tags(zot, tags_to_check)

        # Print summary
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Items checked: {results['items_checked']}")
        print(f"Items with notes: {results['items_with_notes']}")
        print(f"Notes with substantial text: {results['notes_with_text']}")

        if results['sample_texts']:
            print("\n" + "="*70)
            print("SAMPLE TEXT (first sample)")
            print("="*70)
            sample = results['sample_texts'][0]
            print(f"Item: {sample['item_title']}")
            print(f"Tag: {sample['tag']}")
            print(f"Full text length: {sample['text_length']:,} characters")
            print(f"\nFirst 500 characters:")
            print("-"*70)
            print(sample['sample'])
            print("-"*70)

            print(f"\n✓ Full text IS available in Zotero notes!")
            print(f"  We can use this for contextual analysis of naming variants.")
        else:
            print(f"\n✗ No substantial text found in notes.")
            print(f"  Will need to fetch from Trove API instead.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
