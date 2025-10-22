#!/usr/bin/env python3
"""
Script 09: Analyse Naming Variants in Full Text Context

This script analyses tag naming variants by examining how terms are actually used
in the full text of newspaper articles. This provides evidence-based disambiguation:
- Is "south katoomba" a distinct district/suburb name, or just "katoomba" with a directional qualifier?
- Is "Katoomba South Coal Mining Company" the company's official name, or informal reference?
- Are school name variations referring to different schools, or the same school at different times?

Approach:
1. Load naming variant pairs from consolidation decisions
2. Fetch items tagged with each variant
3. Extract full text from Zotero notes
4. Analyse term usage in context using KWIC (Key Word In Context) analysis
5. Generate evidence report with recommendations

KWIC Analysis:
Shows each term usage with surrounding context (50 characters before/after):
"...the committee of the **Katoomba South** Distress Fund met on..."
"...established at **South Katoomba** to assist miners..."

This reveals whether terms are used as:
- Proper nouns (capitalised, official names) → likely distinct entities → keep separate
- Common descriptors (lowercase, directional) → likely same entity → merge or hierarchy

Outputs:
    - reports/naming_variants_context_analysis.md: Evidence report

Usage:
    python scripts/09_analyse_variants_in_context.py
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
import pandas as pd
from pyzotero import zotero

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


class MLStripper(HTMLParser):
    """
    Simple HTML tag stripper using Python's built-in HTML parser.

    Zotero notes are stored as HTML. We need plain text for KWIC analysis.
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


def get_full_text_for_tag(zot, tag_name):
    """
    Fetch full text for all items with a specific tag.

    Parameters:
        zot: Authenticated Zotero client
        tag_name: Tag to search for

    Returns:
        list: Dictionaries with item metadata and full text
    """
    print(f"  Fetching items with tag '{tag_name}'...")

    items = zot.items(tag=tag_name)
    results = []

    for item in items:
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '')

        # Fetch child notes
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        # Extract text from notes
        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        if full_text.strip():
            results.append({
                'key': item_key,
                'title': item_title,
                'date': item_date,
                'full_text': full_text.strip()
            })

    print(f"    Found {len(results)} items with full text")
    return results


def find_contexts(text, search_term, context_chars=80):
    """
    Find all occurrences of a term and extract surrounding context.

    Uses KWIC (Key Word In Context) analysis - shows term with surrounding text.

    Parameters:
        text: Full text to search
        search_term: Term to find (case-insensitive)
        context_chars: Number of characters to show before/after term

    Returns:
        list: Context strings showing term usage
    """
    contexts = []

    # Case-insensitive search
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)

    for match in pattern.finditer(text):
        start = match.start()
        end = match.end()

        # Extract context
        context_start = max(0, start - context_chars)
        context_end = min(len(text), end + context_chars)

        before = text[context_start:start]
        term = text[start:end]
        after = text[end:context_end]

        # Clean up whitespace
        before = ' '.join(before.split())
        after = ' '.join(after.split())

        context = f"...{before} **{term}** {after}..."
        contexts.append(context)

    return contexts


def analyse_variant_pair(zot, tag1, tag2):
    """
    Analyse a pair of naming variants by examining their usage in context.

    Parameters:
        zot: Authenticated Zotero client
        tag1: First tag variant
        tag2: Second tag variant

    Returns:
        dict: Analysis results
    """
    print(f"\nAnalysing pair: '{tag1}' vs '{tag2}'")

    # Fetch full text for both tags
    items1 = get_full_text_for_tag(zot, tag1)
    items2 = get_full_text_for_tag(zot, tag2)

    # Find contexts for each tag
    contexts1 = []
    contexts2 = []

    for item in items1:
        contexts1.extend(find_contexts(item['full_text'], tag1))

    for item in items2:
        contexts2.extend(find_contexts(item['full_text'], tag2))

    return {
        'tag1': tag1,
        'tag2': tag2,
        'items_count1': len(items1),
        'items_count2': len(items2),
        'contexts1': contexts1[:10],  # Limit to first 10 for readability
        'contexts2': contexts2[:10],
        'total_contexts1': len(contexts1),
        'total_contexts2': len(contexts2)
    }


def generate_context_report(analyses):
    """
    Generate Markdown report with contextual analysis of naming variants.

    Parameters:
        analyses: List of analysis results from analyse_variant_pair()

    Returns:
        None (writes report file)
    """
    output_file = config.REPORTS_DIR / 'naming_variants_context_analysis.md'
    print(f"\nGenerating context analysis report at {output_file}...")

    report = """# Naming Variants Context Analysis

**Purpose:** Analyse tag naming variants by examining actual usage in newspaper article full text.

**Method:** KWIC (Key Word In Context) analysis - shows how terms are used in their original context.

**Goal:** Determine whether variants refer to distinct entities (keep separate) or same entity (merge/hierarchy).

---

"""

    for analysis in analyses:
        report += f"""## Pair: '{analysis['tag1']}' vs '{analysis['tag2']}'

### Summary

- **{analysis['tag1']}**: {analysis['items_count1']} items, {analysis['total_contexts1']} occurrences
- **{analysis['tag2']}**: {analysis['items_count2']} items, {analysis['total_contexts2']} occurrences

### Context Examples for '{analysis['tag1']}'

"""
        if analysis['contexts1']:
            for i, context in enumerate(analysis['contexts1'], 1):
                report += f"{i}. {context}\n\n"
        else:
            report += "*No contexts found (term may not appear in full text)*\n\n"

        report += f"""### Context Examples for '{analysis['tag2']}'

"""
        if analysis['contexts2']:
            for i, context in enumerate(analysis['contexts2'], 1):
                report += f"{i}. {context}\n\n"
        else:
            report += "*No contexts found (term may not appear in full text)*\n\n"

        report += "---\n\n"

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved to {output_file}")


def main():
    """Main execution function."""
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - NAMING VARIANTS CONTEXT ANALYSIS")
    print("Script 09: Analyse naming variants using full text context")
    print("="*70)
    print()

    try:
        # Connect to Zotero
        zot = connect_to_zotero()

        # Define naming variant pairs to analyse
        # These come from reports/naming_variants_review.md
        variant_pairs = [
            ('Druid\'s Lodge', 'Druids Lodge'),
            ('south katoomba', 'katoomba'),
            ('katoomba south coal mining company', 'katoomba'),
            ('Katoomba Public School', 'Katoomba Public School (1883-1890)'),
            ('Lithgow Public School', 'Lithgow Public School (1878-1906)')
        ]

        # Analyse each pair
        analyses = []
        for tag1, tag2 in variant_pairs:
            analysis = analyse_variant_pair(zot, tag1, tag2)
            analyses.append(analysis)

        # Generate report
        generate_context_report(analyses)

        print("\n" + "="*70)
        print("✓ CONTEXT ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nReport: {config.REPORTS_DIR / 'naming_variants_context_analysis.md'}")
        print("\nNext: Review context evidence and update consolidation decisions")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
