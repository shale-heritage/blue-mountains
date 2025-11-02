#!/usr/bin/env python3
"""
Script 34: Check Possessive Hotel Name Contexts

Investigates whether possessive hotel names (e.g., "Brown's Hotel", "Mrs Long's Hotel")
are official trading names or informal references to hotels run by specific proprietors.

If informal references, items should be tagged:
- Hotel (generic)
- Person's name (under Hotelliers)

If official trading names, keep as named hotel entities.

Usage:
    python scripts/34_check_possessive_hotel_names.py

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


def analyse_hotel_tag(zot, hotel_name, max_items=10):
    """
    Analyse contexts to determine if hotel name is official trading name or informal reference.

    Args:
        zot: Authenticated Zotero client
        hotel_name: Hotel tag name to analyse
        max_items: Maximum items to check
    """
    print(f"\n{'='*80}")
    print(f"HOTEL: {hotel_name}")
    print(f"{'='*80}\n")

    # Fetch items with this hotel tag
    items = zot.items(tag=hotel_name, limit=max_items)

    if not items:
        print(f"  No items found with tag '{hotel_name}'")
        return

    print(f"Found {len(items)} item(s) with tag '{hotel_name}'\n")

    # Track patterns found
    patterns = {
        'official_name': [],      # "Allen's Hotel" (capitalised, proper noun usage)
        'informal_reference': [], # "at Allen's hotel", "Brown's hotel"
        'proprietor_mention': [], # "Mr Allen", "Mrs Long"
        'licensee': [],          # "licensee", "proprietress", "landlord"
    }

    for idx, item in enumerate(items, 1):
        item_data = item['data']
        title = item_data.get('title', '[No Title]')
        date = item_data.get('date', '[No Date]')

        print(f"[{idx}] {title}")
        print(f"    Date: {date}")

        # Get notes
        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        if notes:
            for note_idx, note in enumerate(notes, 1):
                content = strip_html_tags(note['data'].get('note', ''))

                # Look for hotel name variations
                # Official trading name: usually capitalised "Allen's Hotel"
                # Informal: often lowercase "allen's hotel" or "at Brown's hotel"

                base_name = hotel_name.replace("'s Hotel", "").replace("'s House", "")

                # Search patterns
                official_pattern = re.compile(
                    rf'\b{re.escape(hotel_name)}\b',
                    re.IGNORECASE
                )

                proprietor_patterns = [
                    re.compile(rf'\b(Mr|Mrs|Miss)\.?\s+{re.escape(base_name)}\b', re.IGNORECASE),
                    re.compile(rf'\b{re.escape(base_name)}[,\s]+(landlord|landlady|licensee|proprietor|proprietress|hotellier)\b', re.IGNORECASE),
                    re.compile(rf'\b(licensee|proprietress|landlord|landlady)[,\s]+{re.escape(base_name)}\b', re.IGNORECASE),
                ]

                # Find contexts
                matches = list(official_pattern.finditer(content))

                if matches:
                    for match in matches[:3]:  # Show up to 3 examples
                        start = max(0, match.start() - 150)
                        end = min(len(content), match.end() + 150)
                        context = content[start:end]

                        print(f"    Context: ...{context}...")

                        # Analyse context for clues
                        context_lower = context.lower()

                        # Check for proprietor mentions
                        for prop_pattern in proprietor_patterns:
                            if prop_pattern.search(context):
                                patterns['proprietor_mention'].append(context)
                                print(f"      → Proprietor mention found")
                                break

                        # Check for licensee/business role mentions
                        if re.search(r'\b(licensee|proprietress|landlord|landlady|hotellier)\b',
                                    context_lower):
                            patterns['licensee'].append(context)
                            print(f"      → Business role mention found")

                        # Check capitalisation pattern
                        if hotel_name in context:  # Exact match with capitalisation
                            patterns['official_name'].append(context)
                            print(f"      → Official capitalisation used")
                        else:
                            patterns['informal_reference'].append(context)
                            print(f"      → Lowercase/informal usage")

                        print()
        else:
            print(f"    No notes found\n")

    # Summary for this hotel
    print(f"\n  PATTERN ANALYSIS:")
    print(f"    Official name usage: {len(patterns['official_name'])} contexts")
    print(f"    Informal references: {len(patterns['informal_reference'])} contexts")
    print(f"    Proprietor mentions: {len(patterns['proprietor_mention'])} contexts")
    print(f"    Licensee/role mentions: {len(patterns['licensee'])} contexts")

    # Recommendation
    print(f"\n  RECOMMENDATION:")
    if patterns['proprietor_mention'] or patterns['licensee']:
        print(f"    → Likely INFORMAL reference (proprietor's hotel)")
        print(f"    → Consider tagging as: Hotel + {base_name} (under Hotelliers)")
    else:
        print(f"    → Likely OFFICIAL trading name")
        print(f"    → Keep as named hotel entity: {hotel_name}")


def main():
    """Check contexts for possessive hotel names."""
    print("=" * 80)
    print("POSSESSIVE HOTEL NAME CONTEXT ANALYSIS")
    print("=" * 80)
    print()
    print("Determining whether possessive names are official trading names or")
    print("informal references to proprietors' hotels...")
    print()

    # Connect to Zotero
    zot = connect_to_zotero()

    # Hotels to check
    hotels_to_check = [
        "Allen's Hotel",
        "Brown's Hotel",
        "Mrs Long's Hotel",
        "Hoffman's House",
    ]

    for hotel in hotels_to_check:
        analyse_hotel_tag(zot, hotel, max_items=10)

    # Overall summary
    print("\n" + "=" * 80)
    print("OVERALL GUIDANCE")
    print("=" * 80)
    print()
    print("Official trading names:")
    print("  - Consistently capitalised in sources")
    print("  - Used as proper nouns")
    print("  - May appear in advertisements, legal notices")
    print()
    print("Informal references:")
    print("  - Sources mention proprietor by name and role")
    print("  - References like 'at Brown's hotel' (lowercase)")
    print("  - Text discusses landlord/licensee/proprietress by name")
    print()
    print("If informal, retag as:")
    print("  - Hotel (generic) for the establishment")
    print("  - Person's name under Hotelliers for the proprietor")
    print()


if __name__ == '__main__':
    main()
