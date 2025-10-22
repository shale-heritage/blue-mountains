#!/usr/bin/env python3
"""
Script 24: Check Mining Entity Context in Primary Sources

Investigates whether mining-related tags refer to:
- Corporate entities (companies)
- Physical sites (mines/collieries)

Checks primary source text in Zotero notes to determine correct classification.

Usage:
    python scripts/24_check_mining_entity_context.py

Author: Claude Code
Date: 2025-10-20
"""

import sys
from pathlib import Path
from pyzotero import zotero
import re

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


def strip_html_tags(html_text):
    """Remove HTML tags from text."""
    clean = re.sub('<.*?>', '', html_text)
    return clean


def check_tag_context(zot, tag_name, max_items=10):
    """
    Fetch items with specific tag and extract context from notes.

    Args:
        zot: Authenticated Zotero client
        tag_name: Tag name to search for
        max_items: Maximum items to check

    Returns:
        list: Context samples showing how tag is used
    """
    print(f"\n{'='*80}")
    print(f"TAG: {tag_name}")
    print(f"{'='*80}\n")

    contexts = []

    # Fetch items with this tag
    items = zot.items(tag=tag_name, limit=max_items)

    if not items:
        print(f"  No items found with tag '{tag_name}'")
        return contexts

    print(f"Found {len(items)} item(s) with tag '{tag_name}'\n")

    for idx, item in enumerate(items, 1):
        item_key = item['key']
        item_data = item['data']
        item_title = item_data.get('title', '[No Title]')
        item_date = item_data.get('date', '[No Date]')

        print(f"[{idx}] {item_title}")
        print(f"    Date: {item_date}")

        # Fetch child items (notes and attachments)
        children = zot.children(item_key)

        # Check for notes
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        if notes:
            print(f"    Notes: {len(notes)} found")

            for note_idx, note in enumerate(notes, 1):
                note_content = note['data'].get('note', '')

                if note_content:
                    # Strip HTML
                    clean_text = strip_html_tags(note_content)

                    # Extract context around the tag term
                    # Look for the tag name (case-insensitive)
                    tag_pattern = re.escape(tag_name)
                    matches = list(re.finditer(tag_pattern, clean_text, re.IGNORECASE))

                    if matches:
                        print(f"    Note {note_idx}: Found '{tag_name}' {len(matches)} time(s)")

                        # Show first occurrence with context
                        match = matches[0]
                        start = max(0, match.start() - 150)
                        end = min(len(clean_text), match.end() + 150)
                        context = clean_text[start:end]

                        print(f"    Context: ...{context}...")
                        print()

                        contexts.append({
                            'item_title': item_title,
                            'item_date': item_date,
                            'tag': tag_name,
                            'context': context,
                            'full_text_length': len(clean_text)
                        })
                    else:
                        # Tag not found in note text - might be applied based on article content
                        print(f"    Note {note_idx}: Tag '{tag_name}' not found in note text")
                        print(f"    Note excerpt: {clean_text[:200]}...")
                        print()
        else:
            print(f"    Notes: None found")
            print()

    return contexts


def main():
    """Check context for mining-related entity tags."""
    print("=" * 80)
    print("MINING ENTITY CONTEXT CHECK")
    print("=" * 80)
    print()
    print("Checking whether tags refer to corporate entities or physical sites...")
    print()

    # Connect to Zotero
    zot = connect_to_zotero()

    # Tags to check
    tags_to_check = [
        'Colliery',
        'Katoomba Coal and Shale Mines',
        'South Clifton Tunnel Mine',
        'New South Wales Shale and Oil Co.',
        'A.K.O. & M. Company',
    ]

    all_contexts = []

    for tag in tags_to_check:
        contexts = check_tag_context(zot, tag, max_items=5)
        all_contexts.extend(contexts)

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nTotal contexts extracted: {len(all_contexts)}")

    if all_contexts:
        print("\nContext samples collected. Review output above to determine:")
        print("  1. Does 'Colliery' refer to a specific entity or generic term?")
        print("  2. Do tags without 'Company'/'Co.' refer to mines (sites) or companies?")
        print("  3. Should these be classified as Organizations or Places?")
    else:
        print("\nNo note text available for these tags.")
        print("Recommendation: Check PDF attachments or newspaper metadata.")


if __name__ == '__main__':
    main()
