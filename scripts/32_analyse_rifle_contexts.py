#!/usr/bin/env python3
"""
Script 32: Analyse Rifle-Related Tags in Primary Source Context

Investigates whether rifle-related tags refer to:
- Organisations (rifle clubs - voluntary associations)
- Places (rifle reserves - parcels of Crown land set aside for rifle practice)
- Built facilities (rifle ranges - physical shooting infrastructure)

Checks primary source text in Zotero notes to determine correct classification
and rationalise the current confusion where "Katoomba Rifle Reserves" appears
in multiple facets.

Usage:
    python scripts/32_analyse_rifle_contexts.py

Outputs:
    - Console report with context samples
    - Analysis for consolidation decisions

Author: Claude Code
Date: 2025-11-02
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
    """Remove HyperText Markup Language (HTML) tags from text."""
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

                    # Look for rifle-related terms to understand context
                    rifle_terms = [
                        'rifle club', 'rifle association', 'rifle reserves',
                        'rifle reserve', 'rifle range', 'shooting', 'marksman',
                        'volunteer', 'military', 'practice', 'competition',
                        'crown land', 'gazetted', 'reserve'
                    ]

                    # Find all rifle-related terms in the text
                    found_terms = []
                    for term in rifle_terms:
                        if re.search(re.escape(term), clean_text, re.IGNORECASE):
                            found_terms.append(term)

                    if found_terms:
                        print(f"    Note {note_idx}: Found rifle-related terms: {', '.join(found_terms)}")

                        # Extract a larger context window to understand meaning
                        # Look for the main tag name or related terms
                        search_terms = [tag_name] + ['rifle']
                        match = None

                        for search_term in search_terms:
                            pattern = re.escape(search_term)
                            matches = list(re.finditer(pattern, clean_text, re.IGNORECASE))
                            if matches:
                                match = matches[0]
                                break

                        if match:
                            # Show larger context window (300 chars before/after)
                            start = max(0, match.start() - 300)
                            end = min(len(clean_text), match.end() + 300)
                            context = clean_text[start:end]

                            print(f"    Context: ...{context}...")
                            print()

                            contexts.append({
                                'item_title': item_title,
                                'item_date': item_date,
                                'tag': tag_name,
                                'found_terms': found_terms,
                                'context': context,
                                'full_text_length': len(clean_text)
                            })
                    else:
                        # Tag applied but no rifle terms in note
                        print(f"    Note {note_idx}: No rifle terms found in note text")
                        print(f"    Note excerpt: {clean_text[:200]}...")
                        print()
        else:
            print(f"    Notes: None found")
            print()

    return contexts


def main():
    """Check context for rifle-related tags."""
    print("=" * 80)
    print("RIFLE-RELATED TAG CONTEXT ANALYSIS")
    print("=" * 80)
    print()
    print("Investigating whether tags refer to:")
    print("  1. Organisations (rifle clubs - voluntary associations)")
    print("  2. Places (rifle reserves - Crown land parcels)")
    print("  3. Built facilities (rifle ranges - physical infrastructure)")
    print()

    # Connect to Zotero
    zot = connect_to_zotero()

    # Tags to check (in order of frequency/importance)
    tags_to_check = [
        'Katoomba Rifle Reserves',  # 5 items - appears in 3 different places in taxonomy
        'Rifle reserves',            # 2 items - generic term
        'Rifle club',                # 1 item
        'Mountain Rifle Reserves',   # Unknown frequency
        'Western Rifle Association', # Listed in taxonomy
    ]

    all_contexts = []

    for tag in tags_to_check:
        contexts = check_tag_context(zot, tag, max_items=10)
        all_contexts.extend(contexts)

    # Summary and Analysis
    print("\n" + "=" * 80)
    print("SUMMARY AND ANALYSIS")
    print("=" * 80)
    print(f"\nTotal contexts extracted: {len(all_contexts)}")

    if all_contexts:
        print("\nKey terms found across all contexts:")
        all_terms = set()
        for ctx in all_contexts:
            all_terms.update(ctx['found_terms'])
        for term in sorted(all_terms):
            print(f"  - {term}")

        print("\nNext steps:")
        print("  1. Review contexts above to determine entity type for each tag")
        print("  2. Check if 'Katoomba Rifle Reserves' refers to:")
        print("     a) An organisation (club/association) → Agents facet")
        print("     b) A place (land reserve) → Places facet")
        print("     c) A built facility (range) → Built Environment facet")
        print("  3. Determine if singular/plural variants are used consistently")
        print("  4. Update tag_map_consolidated.csv to remove duplications")
        print("  5. Document decisions in planning/consolidation-decisions.md")
    else:
        print("\nNo note text available for these tags.")
        print("Recommendation:")
        print("  1. Check Portable Document Format (PDF) attachments manually")
        print("  2. Search newspaper text for rifle-related content")
        print("  3. Consult tag_frequency.csv for item counts")


if __name__ == '__main__':
    main()
