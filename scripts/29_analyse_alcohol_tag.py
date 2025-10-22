#!/usr/bin/env python3
"""
Script 29: Analyse Alcohol Tag Usage

This script analyses items tagged with "Alcohol" to determine appropriate
reclassification. The "Alcohol" tag is too broad and may refer to:

1. Alcoholic beverages as material goods/substances
2. Alcohol consumption/drinking as an activity
3. Alcohol trade/sales as an occupation
4. Alcohol-related events (temperance, licensing)
5. Medical/chemical uses of alcohol

Approach:
1. Fetch all items tagged "Alcohol" from Zotero
2. Extract full text from notes
3. Analyse context of alcohol references
4. Generate detailed report with proposed replacement tags
5. Provide hierarchy paths for each proposed tag

The report will guide manual retagging in Zotero to replace the overly broad
"Alcohol" tag with specific, contextually appropriate tags.

Outputs:
    - reports/alcohol_rationalisation_report.md: Detailed retagging guidance

Usage:
    python scripts/29_analyse_alcohol_tag.py
"""

import sys
import json
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


def extract_snippet(full_text, max_words=150):
    """
    Extract a meaningful snippet from full text for context.

    Parameters:
        full_text: Complete text content
        max_words: Maximum words to include in snippet

    Returns:
        Text snippet with ellipsis if truncated
    """
    words = full_text.split()
    if len(words) <= max_words:
        return full_text
    return ' '.join(words[:max_words]) + '...'


def analyse_alcohol_items(zot):
    """
    Fetch and analyse all items tagged with "Alcohol".

    Parameters:
        zot: Authenticated Zotero client

    Returns:
        list: Dictionaries with item metadata and full text
    """
    print("\nFetching items tagged 'Alcohol'...")

    items = zot.items(tag='Alcohol')
    print(f"Found {len(items)} items")

    results = []

    for idx, item in enumerate(items, 1):
        item_key = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_date = item['data'].get('date', '')
        item_publication = item['data'].get('publicationTitle', '')

        print(f"  Processing item {idx}/{len(items)}: {item_title[:50]}...")

        # Fetch child notes
        children = zot.children(item_key)
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        # Extract text from notes
        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        results.append({
            'number': idx,
            'key': item_key,
            'title': item_title,
            'date': item_date,
            'publication': item_publication,
            'full_text': full_text.strip(),
            'has_text': bool(full_text.strip())
        })

    return results


def generate_report(items):
    """
    Generate detailed markdown report with retagging recommendations.

    Parameters:
        items: List of item dictionaries from analyse_alcohol_items()

    Returns:
        None (writes report file)
    """
    output_file = config.REPORTS_DIR / 'alcohol_rationalisation_report.md'
    print(f"\nGenerating report at {output_file}...")

    # Count items with/without full text
    with_text = sum(1 for item in items if item['has_text'])
    without_text = len(items) - with_text

    report = f"""# Alcohol Tag Rationalisation Report

**Purpose:** Analyse items tagged "Alcohol" and propose specific replacement tags.

**Tag Analysis:**
- Total items: {len(items)}
- Items with full text: {with_text}
- Items needing manual review: {without_text}

**Current Issue:**
The "Alcohol" tag is too broad and encompasses multiple distinct concepts:
- Alcoholic beverages (material goods)
- Drinking/consumption (activities)
- Liquor trade/licences (occupations/regulations)
- Temperance movement (social/religious organisations)
- Medical/chemical uses

**Goal:** Replace generic "Alcohol" tag with specific, contextually appropriate tags.

**Instructions:**
1. Review each item below with its proposed tags
2. Verify proposed tags match article context
3. Items marked "NEEDS REVIEW" require full-text examination
4. Apply approved tags manually in Zotero
5. Remove generic "Alcohol" tag after applying specific tags

---

## Items Requiring Retagging

"""

    for item in items:
        report += f"""### {item['number']}. {item['title']}

- **Date:** {item['date']}
- **Publication:** {item['publication']}
"""

        if item['has_text']:
            snippet = extract_snippet(item['full_text'], max_words=150)
            report += f"""- **Proposed Tag:** [TO BE DETERMINED - NEEDS MANUAL ANALYSIS]
- **Hierarchy Path:** [TO BE DETERMINED]

**Snippet:**
> {snippet}

**Rationale:** [TO BE DETERMINED - Please review context and assign appropriate tag]

"""
        else:
            report += """- **Proposed Tag:** NEEDS REVIEW (no full text available)
- **Hierarchy Path:** N/A

**Action Required:** Open item in Zotero, read article, determine appropriate tags based on actual content.

"""

        report += "---\n\n"

    # Add footer with guidance
    report += """## Retagging Guidance

Based on common alcohol-related content in Blue Mountains newspapers, consider these tags:

### Likely Tag Categories

**1. Activities > Drinking**
- Use when: Article discusses drinking behaviour, pub culture, social drinking
- Hierarchy: `Activities > Lifestyle and leisure > Social activities > Drinking`

**2. Events > Criminal events > Drunkenness**
- Use when: Court cases, charges, fines for public drunkenness
- Hierarchy: `Events > Criminal events > Drunkenness`

**3. Occupations > Hospitality workers > Publicans**
- Use when: Focus on hotel/pub keepers, liquor licence holders
- Hierarchy: `Agents > People > Occupations > Hospitality workers > Publicans`

**4. Organisations > Temperance societies**
- Use when: Temperance movement, abstinence campaigns, temperance halls
- Hierarchy: `Agents > Organisations > Social organisations > Temperance societies`

**5. Built Environment > Hotels/Pubs**
- Use when: Physical hotel/pub buildings, licensing of premises
- Hierarchy: `Built Environment > Buildings > Accommodation buildings > Hotels > [Specific hotel name]`
- Or: `Built Environment > Buildings > Hospitality venues > Pubs`

**6. Associated Concepts > Materials > Alcoholic beverages**
- Use when: Focus on alcohol as commodity/substance (not just drinking)
- Hierarchy: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages`

**7. Activities > Commercial activities > Liquor trade**
- Use when: Buying/selling alcohol, liquor licences, alcohol commerce
- Hierarchy: `Activities > Commercial activities > Liquor trade`

### Decision Framework

Ask yourself:
1. **What is the main subject?** The building, the activity, the person, the regulation?
2. **Is it about drinking or about alcohol?** Drinking = activity, alcohol = material
3. **Is it criminal or social?** Drunkenness charges vs pub culture
4. **Is it about trade/commerce?** Selling vs consuming
5. **Does it involve temperance?** Temperance societies have distinct tag

### Multiple Tags

Items may warrant multiple tags. For example:
- Article about publican charged with serving after hours → `Hospitality workers > Publicans` + `Criminal events`
- Temperance lecture at church → `Temperance societies` + `Religious organisations > Churches`
- Hotel fire → `Hotels > [Name]` + `Events > Disasters > Fires`

Use pipe separator (|) to denote multiple tags in this report.

---

**Next Steps:**
1. Review each item's full text in Zotero
2. Determine appropriate tag(s) based on context
3. Update this report with specific tag assignments
4. Apply tags in Zotero
5. Remove generic "Alcohol" tag
6. Update `data/tag_consolidation_map.csv` with decisions
"""

    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Report saved to {output_file}")
    print(f"\n  Items analysed: {len(items)}")
    print(f"  With full text: {with_text}")
    print(f"  Needing review: {without_text}")


def main():
    """Main execution function."""
    print("=" * 70)
    print("BLUE MOUNTAINS PROJECT - ALCOHOL TAG RATIONALISATION")
    print("Script 29: Analyse Alcohol tag usage and generate retagging report")
    print("=" * 70)
    print()

    try:
        # Connect to Zotero
        zot = connect_to_zotero()

        # Analyse items
        items = analyse_alcohol_items(zot)

        # Generate report
        generate_report(items)

        print("\n" + "=" * 70)
        print("✓ ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\nReport: {config.REPORTS_DIR / 'alcohol_rationalisation_report.md'}")
        print("\nNext steps:")
        print("1. Review report and analyse each item's context")
        print("2. Assign specific tags based on article content")
        print("3. Update report with tag assignments")
        print("4. Apply tags manually in Zotero")
        print("5. Remove generic 'Alcohol' tag")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
