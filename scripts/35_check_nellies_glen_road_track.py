#!/usr/bin/env python3
"""
Script 35: Check Nellie's Glen Road vs Track Context

Investigates whether "Nellie's Glen Road" and "Nellie's Glen Track" refer to:
- The same infrastructure (synonyms - different names for same road)
- Different infrastructure (road vs walking track)

Checks primary source text in Zotero notes to determine correct classification.

Usage:
    python scripts/35_check_nellies_glen_road_track.py
"""

import json
import sys
from pathlib import Path

# Add scripts directory to path for config import
sys.path.insert(0, str(Path(__file__).parent))
import config

def extract_context(text, search_term, context_chars=200):
    """Extract context around search term from text."""
    if not text:
        return []

    text_lower = text.lower()
    search_lower = search_term.lower()
    contexts = []

    start = 0
    while True:
        pos = text_lower.find(search_lower, start)
        if pos == -1:
            break

        # Extract context
        ctx_start = max(0, pos - context_chars)
        ctx_end = min(len(text), pos + len(search_term) + context_chars)
        context = text[ctx_start:ctx_end]

        # Clean up
        context = context.replace('\n', ' ').replace('\r', '')
        contexts.append(context)

        start = pos + 1

    return contexts

def main():
    print("=" * 80)
    print("NELLIE'S GLEN ROAD vs TRACK CONTEXT ANALYSIS")
    print("=" * 80)

    # Load Zotero data
    zotero_file = Path("data/zotero_full_export.json")
    print(f"\nLoading: {zotero_file}")

    with open(zotero_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get('items', [])
    print(f"Total items: {len(items)}")

    # Search terms
    search_terms = {
        'road': "Nellie's Glen Road",
        'track': "Nellie's Glen track"
    }

    results = {
        'road': [],
        'track': []
    }

    # Search through items
    for item in items:
        # Check tags - they're stored as simple strings in an array
        tags = item.get('tags', [])

        # Get all note text
        note_text = ""
        for note in item.get('notes', []):
            note_text += note.get('note', '') + " "

        # Check for road
        if "Nellie's Glen Road" in tags:
            results['road'].append({
                'title': item.get('title', 'Untitled'),
                'date': item.get('date', 'No date'),
                'tags': tags,
                'contexts': extract_context(note_text, "Nellie's Glen Road")
            })

        # Check for track
        if "Nellie's Glen track" in tags:
            results['track'].append({
                'title': item.get('title', 'Untitled'),
                'date': item.get('date', 'No date'),
                'tags': tags,
                'contexts': extract_context(note_text, "Nellie's Glen")
            })

    # Print results
    print("\n" + "=" * 80)
    print("NELLIE'S GLEN ROAD - Tagged Items Analysis")
    print("=" * 80)
    print(f"Items tagged: {len(results['road'])}")

    for idx, item in enumerate(results['road'], 1):
        print(f"\n[{idx}] {item['title']} ({item['date']})")
        print(f"    Other tags: {', '.join([t for t in item['tags'] if 'Nellie' not in t][:5])}")
        if item['contexts']:
            print(f"    Contexts found: {len(item['contexts'])}")
            for ctx in item['contexts'][:2]:  # Show first 2 contexts
                print(f"      ...{ctx}...")
        else:
            print("    No context text found in notes")

    print("\n" + "=" * 80)
    print("NELLIE'S GLEN TRACK - Tagged Items Analysis")
    print("=" * 80)
    print(f"Items tagged: {len(results['track'])}")

    for idx, item in enumerate(results['track'], 1):
        print(f"\n[{idx}] {item['title']} ({item['date']})")
        print(f"    Other tags: {', '.join([t for t in item['tags'] if 'Nellie' not in t][:5])}")
        if item['contexts']:
            print(f"    Contexts found: {len(item['contexts'])}")
            for ctx in item['contexts'][:2]:  # Show first 2 contexts
                print(f"      ...{ctx}...")
        else:
            print("    No context text found in notes")

    # Summary
    print("\n" + "=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    print(f"Road: {len(results['road'])} items")
    print(f"Track: {len(results['track'])} items")
    print("\nRecommendation:")
    print("- If contexts show same infrastructure → merge to synonym")
    print("- If contexts show different uses → keep separate (road vs walking track)")

if __name__ == '__main__':
    main()
