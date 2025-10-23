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
    Analyse snippets to suggest specific tags.

    Parameters:
        snippets: List of KWIC snippets

    Returns:
        tuple: (suggested_tags list, rationale string)
    """
    combined_text = ' '.join(snippets).lower()

    suggested_tags = []
    rationale_parts = []

    # Check for postmaster/postmistress (occupation)
    if 'postmaster' in combined_text or 'postmistress' in combined_text:
        suggested_tags.append('Postmaster')
        rationale_parts.append('postmaster/postmistress mentioned')

    # Check for post office (building)
    if 'post office' in combined_text:
        # Check if it's about the building/location
        building_indicators = ['removed to', 'relocated', 'at the', 'building', 'site',
                               'painted', 'painting', 'erected', 'established']
        if any(term in combined_text for term in building_indicators):
            suggested_tags.append('Post office')
            rationale_parts.append('post office building/location')

    # Check for postal services/department
    service_indicators = ['postal authorities', 'postal department', 'postal service',
                         'mail', 'complaint against postal', 'letter']
    if any(term in combined_text for term in service_indicators):
        if 'postal authorities' in combined_text or 'postal department' in combined_text:
            suggested_tags.append('Postal Department')
            rationale_parts.append('postal authorities/department')
        else:
            suggested_tags.append('Postal services')
            rationale_parts.append('postal services/mail')

    # If no specific indicators found
    if not suggested_tags:
        suggested_tags.append('Post office')  # Default to building
        rationale_parts.append('mentions post office (default)')

    rationale = 'Context shows: ' + ', '.join(rationale_parts)

    return suggested_tags, rationale


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

        # Classify usage and suggest tags
        suggested_tags, rationale = classify_post_usage(snippets)

        analysed_items.append({
            'title': title,
            'date': date,
            'publication': pub,
            'key': item_key,
            'snippets': snippets,
            'suggested_tags': suggested_tags,
            'rationale': rationale,
            'full_text_length': len(full_text)
        })

    return analysed_items


def generate_report(items, output_path):
    """
    Generate markdown report for user review with pre-filled suggestions.

    Parameters:
        items: List of analysed items
        output_path: Path to write report
    """
    print(f"\nGenerating report: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Post Tag Analysis Report\n\n")
        f.write("**Generated:** 2025-10-22 (Updated)\n")
        f.write("**Purpose:** Disambiguate 'Post' tag usage\n\n")
        f.write("---\n\n")

        f.write("## Instructions\n\n")
        f.write("For each item below:\n\n")
        f.write("1. Review the suggested tags based on context analysis\n")
        f.write("2. **Answer YES/NO/OTHER** for the suggested tags\n")
        f.write("3. If OTHER, write your preferred tags in the field provided\n\n")
        f.write("**Available tags:**\n")
        f.write("- `Postmaster` (occupation) - Agents > People > Occupations > Public officials > Postmasters > Postmaster\n")
        f.write("- `Post office` (building) - Built Environment > Civic buildings > Postal facilities > Post office\n")
        f.write("- `Postal services` (activity) - Activities > Communication activities > Postal services\n")
        f.write("- `Postal Department` (government body) - Agents > Organizations > Government bodies > Postal authorities > Postal Department\n\n")
        f.write("---\n\n")

        for i, item in enumerate(items, 1):
            f.write(f"## {i}. {item['title']}\n\n")
            f.write(f"- **Date:** {item['date']}\n")
            f.write(f"- **Publication:** {item['publication']}\n")
            f.write(f"- **Zotero Key:** {item['key']}\n\n")

            # Format suggested tags
            tags_formatted = ' | '.join(f'`{tag}`' for tag in item['suggested_tags'])
            f.write(f"**Suggested Tags:** {tags_formatted}\n")
            f.write(f"**Rationale:** {item['rationale']}\n\n")

            f.write("**Snippets (showing post-related content):**\n\n")

            if item['snippets']:
                for snippet in item['snippets'][:3]:  # Limit to 3 most relevant
                    f.write(f"> {snippet}\n\n")
            else:
                f.write("> *No snippets found - limited full text available*\n\n")

            f.write("**DECISION:** ")
            f.write("YES / NO / OTHER: ________________\n\n")

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
