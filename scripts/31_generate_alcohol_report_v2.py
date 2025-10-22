#!/usr/bin/env python3
"""
Script 31: Generate Improved Alcohol Tag Rationalisation Report

This script generates a detailed report for items tagged "Alcohol" with:
1. Excerpts that actually show alcohol-related content
2. Specific alcohol-related tag recommendations
3. Context about how alcohol is discussed in each item

The principle: If an item mentions alcohol/drinking/drunk/beer/wine/rum/grog/etc.,
it should have an alcohol-related tag - we're just making those tags more specific
than the generic "Alcohol" tag.

Outputs:
    - reports/alcohol_rationalisation_report.md: Detailed retagging guidance

Usage:
    python scripts/31_generate_alcohol_report_v2.py
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402

from pyzotero import zotero


class MLStripper(HTMLParser):
    """Simple HTML tag stripper."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)


def strip_html(html):
    """Remove HTML tags from text."""
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


def connect_to_zotero():
    """Connect to Zotero."""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def find_alcohol_snippet(text, max_words=150):
    """
    Find a snippet containing alcohol-related keywords.

    Returns snippet with alcohol context, or beginning of text if no keywords found.
    """
    # Alcohol-related keywords
    keywords = [
        r'\balcohol',
        r'\bdrink(?:ing|s|)',
        r'\bdrank',
        r'\bdrunk(?:en|enness|s|)',
        r'\bliquor',
        r'\bwhisk[ye]y',
        r'\bwine',
        r'\bbeer',
        r'\bgrog',
        r'\brum',
        r'\bbrandy',
        r'\bgin',
        r'\bpublican',
        r'\bhotel(?!keeper)',  # Hotel but not hotelkeeper
        r'\btemperance',
        r'\bteetotal',
        r'\binebriat',
        r'\bintoxicat',
        r'\blicen[cs]',
        r'\bsly-grog',
    ]

    # Search for first occurrence of any keyword
    for keyword_pattern in keywords:
        match = re.search(keyword_pattern, text, re.IGNORECASE)
        if match:
            # Found a keyword - extract context around it
            match_pos = match.start()

            # Find sentence boundaries before and after
            # Go back to find start (period, or start of text)
            start = max(0, match_pos - 400)
            # Find previous sentence end if we're not at start
            if start > 0:
                prev_period = text.rfind('.', start, match_pos)
                if prev_period != -1:
                    start = prev_period + 2  # Skip period and space

            # Go forward to find end
            end = min(len(text), match_pos + 400)
            next_period = text.find('.', match_pos, end)
            if next_period != -1:
                # Include the sentence that contains the match
                # Look for one more sentence
                second_period = text.find('.', next_period + 1, end)
                if second_period != -1:
                    end = second_period + 1
                else:
                    end = next_period + 1

            snippet = text[start:end].strip()

            # Limit to max_words
            words = snippet.split()
            if len(words) > max_words:
                snippet = ' '.join(words[:max_words]) + '...'

            return snippet

    # No alcohol keywords found - return beginning
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...'
    return text


def analyse_item(item):
    """Analyse a single item and return structured data."""
    result = {
        'title': item['data'].get('title', '[No Title]'),
        'date': item['data'].get('date', ''),
        'publication': item['data'].get('publicationTitle', ''),
        'tags': [],
        'hierarchy_paths': [],
        'snippet': '',
        'rationale': ''
    }

    return result


def main():
    """Generate improved alcohol rationalisation report."""
    print("=" * 70)
    print("ALCOHOL TAG RATIONALISATION - IMPROVED REPORT")
    print("=" * 70)
    print()

    zot = connect_to_zotero()
    items = zot.items(tag='Alcohol')

    print(f"Found {len(items)} items\n")

    # Manual analysis based on context analysis from script 30
    item_analyses = [
        {
            'num': 1,
            'title': 'A Charge of Rape.',
            'date': '6 September 1890',
            'publication': 'Nepean Times',
            'tags': ['Drinking', 'Rum', 'Sexual assault', 'Carrington Hotel'],
            'hierarchy': 'Activities > Lifestyle and leisure > Social activities > Drinking | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Rum | Events > Criminal events > Sexual assault | Built Environment > Buildings > Accommodation buildings > Hotels > Carrington Hotel',
            'rationale': 'Rape prosecution case where witnesses and accused had been drinking rum and "hot grog" before the assault. Multiple references to drinking: "they had a drink each", "had a drop of hot grog", "not the worse for liquor when I left". While primary subject is sexual assault, drinking/alcohol consumption is significant contextual element.',
        },
        {
            'num': 2,
            'title': 'Mountain Mixtures.',
            'date': '29 April 1892',
            'publication': 'Katoomba Times',
            'tags': ['Drunkenness', 'Drunkenness (intoxication)', 'Beer', 'Lithgow'],
            'hierarchy': 'Events > Criminal events > Drunkenness | Associated Concepts > Physical and health conditions > Drunkenness (intoxication) | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Beer | Places > Towns > Lithgow',
            'rationale': 'News snippets mentioning "Two drunks at Katoomba Court" (criminal prosecutions) and prediction that cheap "thripenny beers" at Lithgow will cause "double the amount of drunkenness at the black-diamond fields". Both criminal drunkenness and social commentary on intoxication levels.',
        },
        {
            'num': 3,
            'title': 'Mountain Mixtures',
            'date': '25 August 1893',
            'publication': 'Katoomba Times',
            'tags': ['Drinking', 'Whisky', 'Beer', 'Rum', 'Brandy', 'Liquor trade', 'Megalong Valley'],
            'hierarchy': 'Activities > Lifestyle and leisure > Social activities > Drinking | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Whisky | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Beer | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Rum | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Brandy | Activities > Commercial activities > Liquor trade | Places > Valleys > Megalong Valley',
            'rationale': 'Social commentary on Megalong Valley drinking culture: "Whisky at Megalong breeds imitation funerals, hangings", describes "grog shop", "beer and its whiskey, its rum and its brandy, re-tailed per case". About drinking as recreational activity and liquor retail trade.',
        },
        {
            'num': 4,
            'title': 'Mountain Mixtures.',
            'date': '10 February 1893',
            'publication': 'Katoomba Times',
            'tags': ['Beer', 'Liquor trade'],
            'hierarchy': 'Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Beer | Activities > Commercial activities > Liquor trade',
            'rationale': 'Satirical commentary on beer pricing: "talk of cheap beer at Katoomba... beer is awkwardly dear - high-priced... Sixpence a glass!" About beer as commodity and liquor pricing/trade.',
        },
        {
            'num': 5,
            'title': 'Found dead.',
            'date': '28 January 1893',
            'publication': 'Nepean Times',
            'tags': ['Drinking', 'Death', 'Inquests', 'Ruined Castle Shale Mine', 'South Katoomba'],
            'hierarchy': 'Activities > Lifestyle and leisure > Social activities > Drinking | Events > Death | Events > Legal proceedings > Inquests | Built Environment > Structures > Industrial structures > Mining sites > Ruined Castle Shale Mine | Places > Towns > Katoomba > South Katoomba',
            'rationale': 'Inquest into death of mine worker. Testimony notes deceased "was in the habit of taking a drink occasionally", "slightly under the influence of liquor" day before death. Death from natural causes (heart disease) but drinking mentioned as habitual behaviour.',
        },
        {
            'num': 6,
            'title': 'Mountain Mixtures.',
            'date': '3 March 1893',
            'publication': 'Katoomba Times',
            'tags': ['Liquor trade', 'Hotelliers', 'Fires', 'Megalong Valley', 'Oberon'],
            'hierarchy': 'Activities > Commercial activities > Liquor trade | Agents > People > Occupations > Hospitality workers > Hotelliers | Events > Disasters > Fires | Places > Valleys > Megalong Valley | Places > Towns > Oberon',
            'rationale': 'Multiple alcohol references: Megalong Valley needs "a grog shop to make it a red-hot hades", comment on "Mountain hotelkeepers" financial interests, fire at "Plummer\'s Club House Hotel, Oberon". Liquor trade, hotel keepers, and hotel building disaster.',
        },
        {
            'num': 7,
            'title': 'Katoomba Court.',
            'date': '14 October 1892',
            'publication': 'Katoomba Times',
            'tags': ['Liquor licensing', 'Illegal liquor sales', 'Whisky', 'Nellie\'s Glen'],
            'hierarchy': 'Activities > Commercial activities > Liquor trade > Liquor licensing | Events > Criminal events > Illegal liquor sales | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Whisky | Places > Natural features > Gullies > Nellie\'s Glen',
            'rationale': 'Court case: "Irwin charged with carrying about spirituous liquor for sale without a license". Witnesses testified defendant sold whisky at "6d. a drink" at Nellie\'s Glen without proper licensing. Illegal liquor sales prosecution.',
        },
        {
            'num': 8,
            'title': 'Katoomba Police Court.',
            'date': '21 March 1891',
            'publication': 'Katoomba Times',
            'tags': ['Liquor licensing', 'Illegal liquor sales', 'Whisky', 'Minors'],
            'hierarchy': 'Activities > Commercial activities > Liquor trade > Liquor licensing | Events > Criminal events > Illegal liquor sales | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Whisky | Associated Concepts > Age groups > Minors',
            'rationale': 'Prosecution of Joseph Nimmo for "supplying drink to Walter Meredith, a lad supposed to be under the age of 16". Supplied whisky to minor - liquor licensing violation.',
        },
        {
            'num': 9,
            'title': 'Katoomba Court.',
            'date': '17 March 1893',
            'publication': 'Katoomba Times',
            'tags': ['Drunkenness', 'Theft', 'Whisky', 'Rum', 'South Katoomba'],
            'hierarchy': 'Events > Criminal events > Drunkenness | Events > Criminal events > Theft | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Whisky | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Rum | Places > Towns > Katoomba > South Katoomba',
            'rationale': 'Court cases: Frank Kewell fined 5s "for his spree" (drunkenness), and Saunders/Brown/Prentice charged with "stealing whisky, &c. from Richard Allen, Katoomba South". Defendants "drank" the stolen rum. Criminal drunkenness and theft of alcoholic beverages.',
        },
        {
            'num': 10,
            'title': 'Megalong Matters.',
            'date': '9 September 1892',
            'publication': 'Katoomba Times',
            'tags': ['Drinking', 'Wine', 'Liquor trade', 'Indigenous Australians', 'Publicans', 'Megalong Valley'],
            'hierarchy': 'Activities > Lifestyle and leisure > Social activities > Drinking | Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Wine | Activities > Commercial activities > Liquor trade | Agents > People > Cultural groups > Indigenous Australians | Agents > People > Occupations > Hospitality workers > Publicans | Places > Valleys > Megalong Valley',
            'rationale': 'References to keeping Indigenous people from "looking on the wine when it is red" (Biblical reference to drinking), publican serving "liquor up" during cattle sale, people "gloriously drunk on a regular \'razzle dazzle\'". Social commentary on drinking and Indigenous people.',
        },
        {
            'num': 11,
            'title': 'Megalong Valley.',
            'date': '18 August 1893',
            'publication': 'Katoomba Times',
            'tags': ['Liquor trade', 'Mr Wilkinson', 'Megalong Valley'],
            'hierarchy': 'Activities > Commercial activities > Liquor trade | Agents > People > Occupations > Hospitality workers > Liquor merchants > Mr Wilkinson | Places > Valleys > Megalong Valley',
            'rationale': 'Specifically mentions "Mr. Wilkinson is doing a fair trade with his wholesale liquor business" at Megalong Valley. About liquor commerce and specific merchant.',
        },
        {
            'num': 12,
            'title': 'Megalong Valley.',
            'date': '23 June 1893',
            'publication': 'Katoomba Times',
            'tags': ['Liquor licensing', 'Hotels', 'Sly-grog shops', 'Gambling', 'Megalong Valley'],
            'hierarchy': 'Activities > Commercial activities > Liquor trade > Liquor licensing | Built Environment > Buildings > Accommodation buildings > Hotels | Events > Criminal events > Illegal liquor sales | Activities > Leisure activities > Gambling | Places > Valleys > Megalong Valley',
            'rationale': 'Debate over hotel licence application at Megalong: "a hotel would be preferable to the sly-grog and gambling shanties which are said to exist at the Mines". About liquor licensing, illegal sly-grog operations, and establishing legal hotel.',
        },
    ]

    # Fetch items and generate snippets
    print("Fetching full text and generating snippets...\n")

    for idx, item in enumerate(items, 1):
        # Get full text
        children = zot.children(item['key'])
        notes = [child for child in children if child['data'].get('itemType') == 'note']

        full_text = ''
        for note in notes:
            note_content = note['data'].get('note', '')
            full_text += strip_html(note_content) + '\n'

        # Find alcohol-relevant snippet
        snippet = find_alcohol_snippet(full_text)

        # Add snippet to corresponding analysis
        for analysis in item_analyses:
            if analysis['num'] == idx:
                analysis['snippet'] = snippet
                break

    # Generate report
    output_file = config.REPORTS_DIR / 'alcohol_rationalisation_report.md'
    print(f"Generating report at {output_file}...\n")

    report = f"""# Alcohol Tag Rationalisation Report

**Purpose:** Analyse items tagged "Alcohol" and propose specific replacement tags.

**Tag Analysis:**
- Total items: {len(items)}
- Items with full text: {len(items)}

**Current Issue:**
The "Alcohol" tag is too broad and encompasses multiple distinct concepts:
- Alcoholic beverages (material goods) - beer, wine, whisky, rum, brandy, grog
- Drinking/consumption (activities)
- Drunkenness (criminal offence vs. physical state)
- Liquor trade/licences (commercial activities)
- Temperance movement (social organisations)

**Goal:** Replace generic "Alcohol" tag with specific, contextually appropriate tags while maintaining alcohol-related tagging for all items that discuss alcohol/drinking/intoxication.

**Principle:** If an item mentions alcohol, drinking, drunk, drunkenness, or specific alcoholic beverages (beer, wine, rum, grog, whisky, etc.), it should have alcohol-related tags. We're making those tags more specific, not removing alcohol tagging.

**Instructions:**
1. Review each item below with its proposed tags
2. Verify proposed tags match article context
3. Apply approved tags manually in Zotero
4. Remove generic "Alcohol" tag after applying specific tags

---

## Items Requiring Retagging

"""

    for analysis in item_analyses:
        report += f"""### {analysis['num']}. {analysis['title']}

- **Date:** {analysis['date']}
- **Publication:** {analysis['publication']}
- **Proposed Tags:** {' | '.join(f'`{tag}`' for tag in analysis['tags'])}
- **Hierarchy Path:** {analysis['hierarchy']}

**Snippet (showing alcohol-related content):**
> {analysis['snippet']}

**Rationale:** {analysis['rationale']}

---

"""

    # Add guidance footer
    report += """## Retagging Guidance

### Alcohol-Related Tag Categories

**1. Drinking (Activity)**
- Use when: Article discusses drinking behaviour, pub culture, social drinking
- Hierarchy: `Activities > Lifestyle and leisure > Social activities > Drinking`

**2. Drunkenness (Criminal Event)**
- Use when: Court cases, charges, fines for public drunkenness
- Hierarchy: `Events > Criminal events > Drunkenness`

**3. Drunkenness (Physical Condition)**
- Use when: State of intoxication, not criminal prosecution
- Hierarchy: `Associated Concepts > Physical and health conditions > Drunkenness (intoxication)`

**4. Specific Alcoholic Beverages (Materials)**
- Beer: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Beer`
- Wine: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Wine`
- Whisky: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Whisky`
- Rum: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Rum`
- Brandy: `Associated Concepts > Materials > Consumable materials > Alcoholic beverages > Brandy`

**5. Liquor Trade (Commercial Activity)**
- Use when: Buying/selling alcohol, liquor business, alcohol commerce
- Hierarchy: `Activities > Commercial activities > Liquor trade`

**6. Liquor Licensing (Regulatory)**
- Use when: Liquor licences, licensing laws, licensed premises
- Hierarchy: `Activities > Commercial activities > Liquor trade > Liquor licensing`

**7. Illegal Liquor Sales (Criminal Event)**
- Use when: Sly-grog shops, unlicensed sales, selling to minors
- Hierarchy: `Events > Criminal events > Illegal liquor sales`

**8. Hospitality Workers (Occupations)**
- Publicans: `Agents > People > Occupations > Hospitality workers > Publicans`
- Hotelliers: `Agents > People > Occupations > Hospitality workers > Hotelliers`
- Liquor merchants: `Agents > People > Occupations > Hospitality workers > Liquor merchants`

### Multiple Tags

Most items warrant multiple tags. Examples:
- Article mentioning court case for drunk: `Drunkenness` (criminal event)
- Same article discussing amount of beer consumed: + `Beer` (material)
- Publican charged with serving minors: `Liquor licensing` + `Illegal liquor sales` + `Publicans` + `Minors`
- Hotel fire: `Hotels` + `Fires`

Use pipe separator (|) to denote multiple tags in this report.

---

**Next Steps:**
1. Review each item above
2. Verify proposed tags match context shown in snippet
3. Apply tags manually in Zotero
4. Remove generic "Alcohol" tag
5. Update `data/tag_consolidation_map.csv` with decisions
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Report saved to {output_file}")
    print(f"\n  Total items: {len(items)}")
    print(f"  All items have alcohol-related content and will receive specific alcohol tags")
    print(f"\nNext: Review report and apply tags in Zotero")


if __name__ == '__main__':
    main()
