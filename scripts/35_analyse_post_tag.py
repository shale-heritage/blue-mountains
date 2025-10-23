#!/usr/bin/env python3
"""
Script 35: Analyse Post Tag Usage

This script analyses items tagged with "Post" to determine whether they refer to:
1. Post office (building) - should be tagged under Built Environment
2. Postal services (activity) - should be tagged under Activities
3. Both
4. Something else

Approach:
1. Fetch all items tagged "Post" from Zotero
2. Search full text for post-related keywords
3. Extract Key Word In Context (KWIC) snippets
4. Generate review report with context and suggested classifications

Outputs:
    - reports/post_tag_analysis.md: Review report with excerpts and recommendations

Usage:
    python scripts/35_analyse_post_tag.py
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


def extract_kwic_snippets(full_text, keywords, context_chars=150):
    """
    Extract Key Word In Context (KWIC) snippets for post-related keywords.

    Parameters:
        full_text: Complete text content
        keywords: List of keywords to search for
        context_chars: Number of characters to show on each side of match

    Returns:
        list: KWIC snippets with keyword highlighted
    """
    snippets = []

    for keyword in keywords:
        # Case-insensitive search
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)

        for match in pattern.finditer(full_text):
            start = max(0, match.start() - context_chars)
            end = min(len(full_text), match.end() + context_chars)

            snippet = full_text[start:end]

            # Clean up whitespace
            snippet = ' '.join(snippet.split())

            # Highlight the keyword
            snippet = re.sub(
                f'({re.escape(keyword)})',
                r'**\1**',
                snippet,
                flags=re.IGNORECASE
            )

            snippets.append(snippet)

    # Remove duplicates while preserving order
    seen = set()
    unique_snippets = []
    for snippet in snippets:
        if snippet not in seen:
            seen.add(snippet)
            unique_snippets.append(snippet)

    return unique_snippets[:5]  # Limit to 5 snippets per item


def classify_post_usage(snippets):
    """
    Analyse snippets to suggest classification.

    Parameters:
        snippets: List of KWIC snippets

    Returns:
        str: Suggested classification with rationale
    """
    combined_text = ' '.join(snippets).lower()

    # Building indicators
    building_terms = ['post office building', 'post office site', 'erected', 'constructed',
                      'building', 'site', 'location', 'premises']

    # Service indicators
    service_terms = ['postal service', 'mail', 'letter', 'delivery', 'postmaster',
                     'postage', 'correspondence', 'telegraph', 'sent', 'received']

    # Official indicators
    official_terms = ['postmaster', 'post office inspector', 'postal official',
                      'postal department']

    building_score = sum(1 for term in building_terms if term in combined_text)
    service_score = sum(1 for term in service_terms if term in combined_text)
    official_score = sum(1 for term in official_terms if term in combined_text)

    if building_score > service_score and building_score > 0:
        return "Post office (building)", "Mentions physical building/site"
    elif service_score > building_score and service_score > 0:
        return "Postal services (activity)", "Mentions postal/mail services"
    elif official_score > 0:
        return "Public officials (postmaster)", "Mentions postal officials"
    elif building_score > 0 and service_score > 0:
        return "Both building and services", "Mentions both aspects"
    else:
        return "Unclear - manual review needed", "Insufficient context"


def analyse_post_items(zot):
    """
    Analyse all items tagged with "Post".

    Parameters:
        zot: Authenticated Zotero client

    Returns:
        list: Items with post tag analysis
    """
    print("Fetching items tagged 'Post'...")

    # Fetch items tagged with "Post"
    items = zot.items(tag='Post')

    print(f"Found {len(items)} items tagged 'Post'")

    analysed_items = []

    for item in items:
        if 'data' not in item:
            continue

        item_data = item['data']

        # Extract basic metadata
        title = item_data.get('title', 'Untitled')
        date = item_data.get('date', 'No date')
        pub = item_data.get('publicationTitle', 'Unknown publication')
        item_key = item['key']

        print(f"  Analysing: {title[:60]}...")

        # Get children (attachments with full text)
        children = zot.children(item_key)

        full_text = ""
        for child in children:
            if child['data'].get('itemType') == 'note':
                note_html = child['data'].get('note', '')
                full_text += strip_html(note_html) + " "

        if not full_text.strip():
            full_text = item_data.get('abstractNote', '')

        # Extract KWIC snippets for post-related terms
        keywords = ['post office', 'post', 'postal', 'postmaster', 'mail', 'letter']
        snippets = extract_kwic_snippets(full_text, keywords)

        # Classify usage
        classification, rationale = classify_post_usage(snippets)

        analysed_items.append({
            'title': title,
            'date': date,
            'publication': pub,
            'key': item_key,
            'snippets': snippets,
            'classification': classification,
            'rationale': rationale,
            'full_text_length': len(full_text)
        })

    return analysed_items


def generate_report(items, output_path):
    """
    Generate markdown report for user review.

    Parameters:
        items: List of analysed items
        output_path: Path to write report
    """
    print(f"\nGenerating report: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Post Tag Analysis Report\n\n")
        f.write("**Generated:** 2025-10-22\n")
        f.write("**Purpose:** Disambiguate 'Post' tag usage\n\n")
        f.write("---\n\n")

        f.write("## Instructions\n\n")
        f.write("For each item below:\n\n")
        f.write("1. Review the snippets showing 'Post' usage in context\n")
        f.write("2. Determine the correct classification:\n")
        f.write("   - **Post office** (building) → Tag with building tag\n")
        f.write("   - **Postal services** (activity) → Tag with activity tag\n")
        f.write("   - **Postmaster** (occupation) → Tag with occupation tag\n")
        f.write("   - **Multiple** → Tag with multiple appropriate tags\n")
        f.write("3. Write the desired tag(s) in the 'DECISION' field\n\n")
        f.write("---\n\n")

        for i, item in enumerate(items, 1):
            f.write(f"## {i}. {item['title']}\n\n")
            f.write(f"- **Date:** {item['date']}\n")
            f.write(f"- **Publication:** {item['publication']}\n")
            f.write(f"- **Zotero Key:** {item['key']}\n")
            f.write(f"- **Full Text Available:** {'Yes' if item['full_text_length'] > 100 else 'No (limited context)'}\n\n")

            f.write(f"**Suggested Classification:** {item['classification']}\n")
            f.write(f"**Rationale:** {item['rationale']}\n\n")

            f.write("**Snippets (showing post-related content):**\n\n")

            if item['snippets']:
                for snippet in item['snippets']:
                    f.write(f"> {snippet}\n\n")
            else:
                f.write("> *No snippets found - limited full text available*\n\n")

            f.write("**DECISION:**\n\n")
            f.write("- [ ] Post office (building)\n")
            f.write("- [ ] Postal services (activity)\n")
            f.write("- [ ] Postmaster (occupation)\n")
            f.write("- [ ] Multiple (specify): ________________\n")
            f.write("- [ ] Remove 'Post' tag (not relevant)\n\n")
            f.write("**Proposed Tags:** ________________\n\n")
            f.write("---\n\n")

    print(f"✓ Report generated: {output_path}")
    print(f"\n{len(items)} items analysed")


def main():
    """Main entry point."""
    # Connect to Zotero
    zot = connect_to_zotero()

    # Analyse items
    items = analyse_post_items(zot)

    if not items:
        print("\nNo items found with 'Post' tag")
        return 1

    # Generate report
    output_path = Path('reports/post_tag_analysis.md')
    generate_report(items, output_path)

    print("\n✓ Analysis complete")
    print(f"\nNext steps:")
    print(f"1. Review report: {output_path}")
    print(f"2. Make decisions on each item's classification")
    print(f"3. Apply tags manually in Zotero")

    return 0


if __name__ == '__main__':
    exit(main())
