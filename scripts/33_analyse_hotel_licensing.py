#!/usr/bin/env python3
"""
Script 33: Analyse Hotel Licensing in Accommodation Items

This script analyses items from the accommodation rationalization (64 items)
to identify which contain hotel or boarding house licensing content.

Hotel/Boarding House Licensing includes:
1. License applications (hotel, boarding house, publican's licence)
2. License renewals and transfers
3. License refusals or violations
4. Licensing Court proceedings
5. Hotel Act or licensing regulations

Approach:
1. Fetch all items tagged "Accommodation" from Zotero
2. Search full text for hotel/boarding house licensing keywords
3. Extract Key Word In Context (KWIC) snippets around matches
4. Categorise by strength of licensing focus
5. Generate review report with yes/no checkboxes

Bonus: Flag any liquor licensing mentions separately (different tag)

Outputs:
    - reports/hotel_licensing_review.md: Review report with excerpts

Usage:
    python scripts/33_analyse_hotel_licensing.py
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402

from pyzotero import zotero


class MLStripper(HTMLParser):
    """
    Simple HTML tag stripper using Python's built-in HTML parser.

    Zotero notes are stored as HTML. We need plain text for analysis.
    This class removes all HTML tags while preserving text content.
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        """Accumulate text content (not tags)."""
        self.text.append(data)

    def get_data(self):
        """Return accumulated text."""
        return ''.join(self.text)


def strip_html(html):
    """
    Remove HTML tags from text.

    Parameters:
        html: HTML string

    Returns:
        Plain text string
    """
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


def connect_to_zotero():
    """Connect to Zotero group library via Application Programming Interface (API)."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def extract_kwic_snippets(full_text, pattern, context_sentences=2):
    """
    Extract Key Word In Context (KWIC) snippets for licensing keywords.

    Parameters:
        full_text: Complete text content
        pattern: Compiled regex pattern
        context_sentences: Number of sentences before/after to include

    Returns:
        list: Tuples of (keyword_found, snippet_text)
    """
    snippets = []

    # Split into sentences (basic sentence detection)
    sentences = re.split(r'(?<=[.!?])\s+', full_text)

    for sent_idx, sentence in enumerate(sentences):
        match = pattern.search(sentence)
        if match:
            # Extract context window
            start_idx = max(0, sent_idx - context_sentences)
            end_idx = min(len(sentences), sent_idx + context_sentences + 1)
            context = ' '.join(sentences[start_idx:end_idx])

            # Highlight the match
            keyword = match.group(0)
            highlighted = re.sub(
                re.escape(keyword),
                f"**{keyword}**",
                context,
                flags=re.IGNORECASE
            )

            snippets.append((keyword, highlighted))

    return snippets


def analyse_accommodation_items(zot):
    """
    Fetch and analyse all items tagged with "Accommodation".

    Parameters:
        zot: Authenticated Zotero client

    Returns:
        list: Dictionaries with item metadata, licensing mentions, and excerpts
    """
    print("\nFetching items tagged 'Accommodation'...")

    items = zot.items(tag='Accommodation')
    print(f"Found {len(items)} items")

    # Hotel/boarding house licensing patterns
    hotel_license_pattern = re.compile(
        r'\b(hotel\s+licen[cs]e|boarding\s+house\s+licen[cs]e|publican\'?s?\s+licen[cs]e|'
        r'conditional\s+licen[cs]e|renewal\s+of\s+licen[cs]e|transfer\s+of\s+licen[cs]e|'
        r'licen[cs]ing\s+court|licen[cs]ing\s+act|hotel\s+act|'
        r'licen[cs]ee\s+of|granted\s+a?\s+licen[cs]e|refused\s+a?\s+licen[cs]e|'
        r'application\s+for\s+a?\s+licen[cs]e|unlicensed\s+hotel|'
        r'infringing.*licen[cs]ing\s+act)',
        re.IGNORECASE
    )

    # Liquor licensing pattern (separate category)
    liquor_license_pattern = re.compile(
        r'\b(liquor\s+licen[cs]e|liquor\s+licen[cs]ing|sly-grog)',
        re.IGNORECASE
    )

    results = []

    for idx, item in enumerate(items, 1):
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '')
        item_publication = item['data'].get('publicationTitle', '')
        current_tags = [tag['tag'] for tag in item['data'].get('tags', [])]

        print(f"  Processing item {idx}/{len(items)}: {item_title[:50]}...")

        # Fetch child notes
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        # Extract text from notes
        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        # Search for hotel licensing mentions
        hotel_licensing_snippets = extract_kwic_snippets(
            full_text, hotel_license_pattern, context_sentences=2
        )

        # Search for liquor licensing mentions (bonus)
        liquor_licensing_snippets = extract_kwic_snippets(
            full_text, liquor_license_pattern, context_sentences=2
        )

        results.append({
            'number': idx,
            'key': item_key,
            'title': item_title,
            'date': item_date,
            'publication': item_publication,
            'current_tags': current_tags,
            'hotel_licensing_count': len(hotel_licensing_snippets),
            'liquor_licensing_count': len(liquor_licensing_snippets),
            'hotel_licensing_snippets': hotel_licensing_snippets,
            'liquor_licensing_snippets': liquor_licensing_snippets,
            'has_full_text': bool(full_text.strip())
        })

    return results


def categorise_by_strength(results):
    """
    Categorise items by strength of hotel licensing focus.

    Categories:
    - Strong: 3+ mentions or contains application/violation keywords
    - Moderate: 1-2 mentions
    - Weak/None: 0 mentions
    - No text: Full text unavailable

    Parameters:
        results: List of item dictionaries

    Returns:
        dict: Categorised results
    """
    categorised = {
        'strong': [],
        'moderate': [],
        'none': [],
        'no_text': [],
        'liquor_licensing': []
    }

    # Strong keywords that indicate licensing is central to the article
    strong_keywords = [
        'application for',
        'refused',
        'granted',
        'licensing court',
        'licensing act',
        'unlicensed',
        'transfer of license',
        'renewal of license',
        'conditional license'
    ]

    for item in results:
        if not item['has_full_text']:
            categorised['no_text'].append(item)
            continue

        hotel_count = item['hotel_licensing_count']
        liquor_count = item['liquor_licensing_count']

        # Check for strong keywords
        has_strong = any(
            any(kw in snippet[1].lower() for kw in strong_keywords)
            for snippet in item['hotel_licensing_snippets']
        )

        if hotel_count >= 3 or (hotel_count >= 1 and has_strong):
            categorised['strong'].append(item)
        elif hotel_count >= 1:
            categorised['moderate'].append(item)
        else:
            categorised['none'].append(item)

        # Bonus: flag liquor licensing
        if liquor_count > 0:
            categorised['liquor_licensing'].append(item)

    return categorised


def generate_review_report(categorised, output_file):
    """
    Generate markdown report for user review.

    Parameters:
        categorised: Categorised results dictionary
        output_file: Path to output file
    """
    print(f"\nGenerating review report: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Hotel Licensing Review Report\n\n")
        f.write("**Date:** 2025-10-22\n\n")
        f.write("**Purpose:** Identify which accommodation items should receive "
                "the new 'Hotel licensing' tag\n\n")
        f.write("---\n\n")

        # Calibration examples
        f.write("## Calibration Examples\n\n")
        f.write("Review these first to establish tagging criteria:\n\n")

        # Show 3 examples from different categories
        calibration_items = []
        if categorised['strong']:
            calibration_items.append(('STRONG', categorised['strong'][0]))
        if categorised['moderate']:
            calibration_items.append(('MODERATE', categorised['moderate'][0]))
        if categorised['none'] and any(i['has_full_text'] for i in categorised['none']):
            weak_item = next(i for i in categorised['none'] if i['has_full_text'])
            calibration_items.append(('WEAK/NONE', weak_item))

        for strength, item in calibration_items:
            f.write(f"### [{strength}] Item #{item['number']}: {item['title']}\n\n")
            f.write(f"**Date:** {item['date']}  \n")
            f.write(f"**Hotel licensing mentions:** {item['hotel_licensing_count']}\n\n")

            if item['hotel_licensing_snippets']:
                f.write("**Excerpt:**\n\n")
                snippet = item['hotel_licensing_snippets'][0]
                f.write(f"> {snippet[1]}\n\n")
            else:
                f.write("*No hotel licensing mentions found*\n\n")

            f.write("---\n\n")

        # Section A: Strong
        f.write("## Section A: Strong Hotel Licensing Focus\n\n")
        f.write(f"**Items:** {len(categorised['strong'])}  \n")
        f.write("Licensing is central to the article (applications, violations, court proceedings)\n\n")

        for item in categorised['strong']:
            write_item_section(f, item)

        # Section B: Moderate
        f.write("\n## Section B: Moderate Hotel Licensing Mentions\n\n")
        f.write(f"**Items:** {len(categorised['moderate'])}  \n")
        f.write("Substantive licensing content but not primary focus\n\n")

        for item in categorised['moderate']:
            write_item_section(f, item)

        # Section C: No mentions
        f.write("\n## Section C: No Hotel Licensing Mentions\n\n")
        f.write(f"**Items:** {len(categorised['none'])}  \n")
        f.write("No hotel licensing keywords found\n\n")

        # Just list titles, no excerpts needed
        for item in categorised['none']:
            f.write(f"- Item #{item['number']}: {item['title']}\n")

        # Section D: No text
        if categorised['no_text']:
            f.write("\n## Section D: Full Text Unavailable\n\n")
            f.write(f"**Items:** {len(categorised['no_text'])}  \n")
            f.write("Require manual review in Zotero\n\n")

            for item in categorised['no_text']:
                f.write(f"- Item #{item['number']}: {item['title']}\n")

        # Section E: Liquor licensing (bonus)
        if categorised['liquor_licensing']:
            f.write("\n## Section E: Bonus - Liquor Licensing Found\n\n")
            f.write(f"**Items:** {len(categorised['liquor_licensing'])}  \n")
            f.write("These items also contain liquor licensing mentions "
                    "(already handled in alcohol rationalization)\n\n")

            for item in categorised['liquor_licensing']:
                f.write(f"### Item #{item['number']}: {item['title']}\n\n")
                f.write(f"**Liquor licensing mentions:** {item['liquor_licensing_count']}\n\n")

                if item['liquor_licensing_snippets']:
                    f.write("**Liquor licensing excerpt:**\n\n")
                    snippet = item['liquor_licensing_snippets'][0]
                    f.write(f"> {snippet[1]}\n\n")

                f.write("---\n\n")

        # Summary statistics
        f.write("\n## Summary Statistics\n\n")
        total_hotel_mentions = sum(i['hotel_licensing_count'] for i in
                                   categorised['strong'] + categorised['moderate'])
        total_items_with_mentions = len(categorised['strong']) + len(categorised['moderate'])

        f.write(f"- **Total items analysed:** {len(categorised['strong']) + len(categorised['moderate']) + len(categorised['none']) + len(categorised['no_text'])}\n")
        f.write(f"- **Items with hotel licensing mentions:** {total_items_with_mentions}\n")
        f.write(f"- **Total hotel licensing mentions:** {total_hotel_mentions}\n")
        f.write(f"- **Items with strong focus:** {len(categorised['strong'])}\n")
        f.write(f"- **Items with moderate mentions:** {len(categorised['moderate'])}\n")
        f.write(f"- **Items with no mentions:** {len(categorised['none'])}\n")
        f.write(f"- **Items with no full text:** {len(categorised['no_text'])}\n")
        f.write(f"- **Bonus - Items with liquor licensing:** {len(categorised['liquor_licensing'])}\n")

    print(f"✓ Report saved: {output_file}")


def write_item_section(f, item):
    """
    Write a single item's section in the report.

    Parameters:
        f: File handle
        item: Item dictionary
    """
    f.write(f"### Item #{item['number']}: {item['title']}\n\n")
    f.write(f"**Date:** {item['date']}  \n")
    f.write(f"**Publication:** {item['publication']}  \n")
    f.write(f"**Current tags:** {', '.join(item['current_tags'])}  \n")
    f.write(f"**Hotel licensing mentions:** {item['hotel_licensing_count']}  \n")
    if item['liquor_licensing_count'] > 0:
        f.write(f"**Liquor licensing mentions:** {item['liquor_licensing_count']}  \n")
    f.write("\n")

    # Show all hotel licensing excerpts
    if item['hotel_licensing_snippets']:
        for idx, (keyword, snippet) in enumerate(item['hotel_licensing_snippets'], 1):
            f.write(f"#### Excerpt {idx}:\n\n")
            f.write(f"> {snippet}\n\n")

    # Decision checkboxes
    f.write("**Decision:**  \n")
    f.write("[ ] YES - Add 'Hotel licensing' tag  \n")
    f.write("[ ] NO - Merely contextual mention  \n")

    if item['liquor_licensing_count'] > 0:
        f.write("[ ] Also review for 'Liquor licensing' tag\n")

    f.write("\n---\n\n")


def main():
    """Main execution function."""
    print("=" * 80)
    print("HOTEL LICENSING ANALYSIS FOR ACCOMMODATION ITEMS")
    print("=" * 80)

    # Connect to Zotero
    zot = connect_to_zotero()

    # Analyse items
    results = analyse_accommodation_items(zot)

    # Categorise by strength
    categorised = categorise_by_strength(results)

    # Generate report
    output_file = Path('reports/hotel_licensing_review.md')
    generate_review_report(categorised, output_file)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nNext steps:")
    print(f"1. Review: {output_file}")
    print(f"2. Mark YES/NO decisions for each item")
    print(f"3. Run follow-up script to apply approved tags")
    print()


if __name__ == '__main__':
    main()
