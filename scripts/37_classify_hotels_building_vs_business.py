#!/usr/bin/env python3
"""
Classify hotel mentions as building, business, or both using linguistic heuristic.

Applies entity-classification-heuristic.md decision framework to all hotel mentions
in the Zotero library to determine appropriate facet classification.

Output: Report with context, classification recommendation, and approval workflow.
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
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
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


# Linguistic patterns for classification
BUILDING_PATTERNS = {
    'locational_prep': r'\b(at|in|within|inside|outside|near|opposite|adjacent to|on)\s+(?:the\s+)?{hotel}',
    'movement_to': r'\b(go(?:ing)?|come|coming|came|went|arrive|arriving|arrived|leave|leaving|left|depart|walk|travel)(?:ing)?\s+(?:to|from|at)\s+(?:the\s+)?{hotel}',
    'events_at': r'\b(meeting|concert|ball|dinner|auction|court|session|gathering|function|held|took place|occurred|picnic|race meeting|entertainment)\s+(?:at|in|near)\s+(?:the\s+)?{hotel}',
    'staying_at': r'\b(stay(?:ing)?|stayed|lodg(?:ing)?|lodged|resid(?:ing)?|resided|accommodated|stopping)\s+(?:at|in)\s+(?:the\s+)?{hotel}',
    'physical_features': r'{hotel}(?:\'?s)?\s+(building|structure|premises|rooms?|bar|verandah?|dining room|bedroom|parlou?r|stable)',
    'construction': r'{hotel}\s+(?:was\s+)?(?:being\s+)?(built|erected|demolished|burned|destroyed|burnt|damaged)',
    'venue_usage': r'(?:at|in)\s+(?:the\s+)?{hotel}\s+(?:yard|grounds|paddock|garden)',
}

BUSINESS_PATTERNS = {
    'agency_verbs': r'{hotel}\s+(?:has\s+)?(?:is\s+)?(?:are\s+)?(?:being\s+)?(expand(?:ing|ed)?|refurbish(?:ing|ed)?|open(?:ing|ed)?|clos(?:ing|ed)?|advertis(?:ing|ed)?|announc(?:ing|ed)?)',
    'ownership': r'{hotel}\s+(?:proprietor|owner|manager|keeper|lessee)',
    'proprietor_subject': r'\b(?:proprietor|owner|manager|keeper|landlord|landlady)\s+(?:of|at)\s+(?:the\s+)?{hotel}',
    'business_ops': r'{hotel}\s+(?:has\s+)?(?:been\s+)?(?:is\s+)?(licensed|opened for|closed for|commenced|trading|operating|conducting)',
    'financial': r'{hotel}\s+(?:has\s+)?(?:been\s+)?(sell(?:ing)?|purchas(?:ing)?|bought|sold|revenue|profit|rent(?:ing)?)',
    'services': r'{hotel}\s+(?:will\s+)?(?:has\s+)?(?:can\s+)?(offer(?:ing|s|ed)?|provid(?:ing|es|ed)?|cater(?:ing|s|ed)?|serv(?:ing|es|ed)?|supply|supplies|supplied)',
    'legal_agent': r'{hotel}\s+(?:is\s+)?(?:was\s+)?(appl(?:ying|ied)|fined|prosecuted|charged|sued|summoned)',
    'competition': r'{hotel}\s+(?:is\s+)?(?:competing|rival(?:ling)?|undercutting)',
}

METONYMY_PATTERNS = {
    'hotel_as_agent': r'(?:the\s+)?{hotel}\s+(denies|claims|states|argues|contests|appeals|refuses|accepts)',
}


def extract_context(text: str, match_pos: Tuple[int, int], context_chars: int = 300) -> str:
    """Extract surrounding text for context."""
    start, end = match_pos

    # Get characters around the match
    context_start = max(0, start - context_chars)
    context_end = min(len(text), end + context_chars)

    context = text[context_start:context_end]

    # Try to start/end at sentence boundaries
    # Find first sentence start after context_start
    if context_start > 0:
        first_period = context.find('. ')
        if 0 < first_period < 50:  # Don't skip too much
            context = context[first_period + 2:]

    # Find last complete sentence before context_end
    last_period = context.rfind('. ')
    if last_period > len(context) - 50:  # Don't trim too much
        context = context[:last_period + 1]

    return context.strip()


def classify_mention(hotel_name: str, context: str) -> Tuple[str, str, int, List[str]]:
    """
    Classify hotel mention using heuristic.

    Returns:
        classification: 'building', 'business', 'both', 'unclear'
        reasoning: explanation of decision
        confidence: 1-3 (1=low, 2=medium, 3=high)
        matched_patterns: list of pattern types that matched
    """
    # Escape hotel name for regex, but handle apostrophes specially
    hotel_escaped = re.escape(hotel_name).replace(r"\'", r"'?")

    building_matches = []
    business_matches = []

    # Check building patterns
    for pattern_name, pattern_template in BUILDING_PATTERNS.items():
        pattern = pattern_template.format(hotel=hotel_escaped)
        if re.search(pattern, context, re.IGNORECASE):
            building_matches.append(pattern_name)

    # Check business patterns
    for pattern_name, pattern_template in BUSINESS_PATTERNS.items():
        pattern = pattern_template.format(hotel=hotel_escaped)
        if re.search(pattern, context, re.IGNORECASE):
            business_matches.append(pattern_name)

    # Check metonymy patterns (count as business)
    for pattern_name, pattern_template in METONYMY_PATTERNS.items():
        pattern = pattern_template.format(hotel=hotel_escaped)
        if re.search(pattern, context, re.IGNORECASE):
            business_matches.append(pattern_name)

    # Determine classification
    building_score = len(building_matches)
    business_score = len(business_matches)

    matched_patterns = building_matches + business_matches

    if building_score > 0 and business_score > 0:
        classification = 'both'
        confidence = 3
        reasoning = f"Text contains both spatial indicators ({', '.join(building_matches)}) and agency indicators ({', '.join(business_matches)})"
    elif building_score > business_score:
        classification = 'building'
        confidence = 3 if building_score >= 2 else 2
        reasoning = f"Spatial/locational indicators: {', '.join(building_matches)}"
    elif business_score > building_score:
        classification = 'business'
        confidence = 3 if business_score >= 2 else 2
        reasoning = f"Agency/operational indicators: {', '.join(business_matches)}"
    else:
        # Default to building if hotel is mentioned but no strong signals
        # Most newspaper mentions use hotels as locations
        classification = 'building'
        confidence = 1
        reasoning = "No strong indicators detected; defaulting to building (typical usage)"

    return classification, reasoning, confidence, matched_patterns


def main():
    """Analyse hotel mentions and generate classification report."""
    print("=" * 80)
    print("HOTEL CLASSIFICATION: Building vs Business")
    print("=" * 80)
    print()

    zot = connect_to_zotero()

    # Get list of specific hotel names from taxonomy
    print("Loading hotel names from taxonomy...")
    hotel_names = set()

    # We'll look for items with hotel tags and extract hotel names from them
    # For now, focus on the major hotels mentioned in previous work
    specific_hotels = [
        'Carrington Hotel',
        'Imperial Hotel',
        'Katoomba Hotel',
        'Megalong Hotel',
        'Centennial Hotel',
        'Belgravia Hotel',
        'Railway Hotel',
        'Wentworth Falls Hotel',
        'Mount Victoria Hotel',
        'Katoomba Family Hotel',
        'Grand Hotel',
        "Hoffman's House",
        'Montrose House',
        'Leura Hotel',
        'Falls Hotel',
        'Great Western Hotel',
        'Hotel Wentworth',
        'Hydora House Hotel',
        'Comet Hotel',
        "Delaney's Family Hotel",
        "Fryer's Family Hotel",
    ]

    print(f"Analysing {len(specific_hotels)} specific hotels...")

    results = []

    for hotel_name in specific_hotels:
        print(f"\nSearching for items tagged '{hotel_name}'...")

        # Try to find items with this hotel tag
        try:
            items = zot.items(tag=hotel_name)
        except Exception as e:
            print(f"  Could not fetch items for '{hotel_name}': {e}")
            continue

        if not items:
            print(f"  No items found")
            continue

        print(f"  Found {len(items)} items")

        for item in items:
            title = item['data'].get('title', '[No Title]')
            date = item['data'].get('date', '')
            url = item['data'].get('url', '')

            # Get full text from notes
            try:
                children = zot.children(item['key'])
                notes = [child for child in children if child['data'].get('itemType') == 'note']

                full_text = ''
                for note in notes:
                    note_content = note['data'].get('note', '')
                    full_text += strip_html(note_content) + '\n'

                if not full_text.strip() or len(full_text) < 100:
                    print(f"    Skipping '{title}' (insufficient text)")
                    continue

                # Find hotel mentions in text
                pattern = re.compile(re.escape(hotel_name).replace(r"\'", r"'?"), re.IGNORECASE)
                matches = list(pattern.finditer(full_text))

                if not matches:
                    print(f"    Skipping '{title}' (hotel not mentioned in text)")
                    continue

                # Use first substantive mention
                match = matches[0]
                context = extract_context(full_text, match.span(), context_chars=250)

                if len(context) < 100:
                    continue

                # Classify
                classification, reasoning, confidence, patterns = classify_mention(hotel_name, context)

                results.append({
                    'hotel_name': hotel_name,
                    'item_title': title,
                    'item_date': date,
                    'context': context,
                    'classification': classification,
                    'reasoning': reasoning,
                    'confidence': confidence,
                    'matched_patterns': patterns,
                    'url': url,
                })

                print(f"    ✓ Analysed '{title}': {classification} (confidence: {confidence}/3)")

            except Exception as e:
                print(f"    Error processing '{title}': {e}")
                continue

    print(f"\n\n{'=' * 80}")
    print(f"Processed {len(results)} hotel mentions")
    print('=' * 80)

    # Generate report
    report_path = config.REPORTS_DIR / 'hotel_classification_review.md'

    with open(report_path, 'w') as f:
        f.write("# Hotel Classification Review: Building vs Business\n\n")
        f.write("Classification of hotel mentions using linguistic heuristic from ")
        f.write("`docs/entity-classification-heuristic.md`\n\n")
        f.write("## Instructions\n\n")
        f.write("For each hotel mention below:\n\n")
        f.write("1. Read the context and my recommendation\n")
        f.write("2. Modify the `APPROVED_CLASSIFICATION` if needed\n")
        f.write("3. Valid values: `building`, `business`, `both`\n")
        f.write("4. Add notes in `REVIEW_NOTES` if helpful\n\n")
        f.write("## Classification Key\n\n")
        f.write("- **building**: Tag as `[Hotel Name] (building)` in Built Environment only\n")
        f.write("- **business**: Tag as `[Hotel Name] (business)` in Agents > Organisations only\n")
        f.write("- **both**: Create polyhierarchical tags appearing in both facets\n\n")
        f.write("## Decision Heuristic Summary\n\n")
        f.write("**Building indicators:**\n")
        f.write("- Locational: at/in/near the hotel\n")
        f.write("- Movement: going to/from, arriving at\n")
        f.write("- Events: meeting held at, concert at\n")
        f.write("- Accommodation: staying at, lodging at\n\n")
        f.write("**Business indicators:**\n")
        f.write("- Agency: hotel expanding, refurbishing, opening\n")
        f.write("- Ownership: hotel proprietor, owner, manager\n")
        f.write("- Operations: licensed, trading, providing services\n")
        f.write("- Financial: selling, purchasing, revenue\n\n")
        f.write("---\n\n")

        # Group by hotel name
        by_hotel = defaultdict(list)
        for result in results:
            by_hotel[result['hotel_name']].append(result)

        # Sort by frequency
        sorted_hotels = sorted(by_hotel.items(), key=lambda x: len(x[1]), reverse=True)

        entry_num = 1
        for hotel_name, mentions in sorted_hotels:
            f.write(f"## {hotel_name}\n\n")
            f.write(f"**Total mentions analysed:** {len(mentions)}\n\n")

            for mention in mentions:
                f.write(f"### Entry {entry_num}\n\n")

                f.write(f"**Item:** {mention['item_title']}")
                if mention['item_date']:
                    f.write(f" ({mention['item_date']})")
                f.write("\n\n")

                f.write("**Context:**\n\n")
                f.write(f"> {mention['context']}\n\n")

                f.write(f"**Recommended classification:** `{mention['classification']}` ")
                f.write(f"(confidence: {mention['confidence']}/3)\n\n")

                f.write(f"**Reasoning:** {mention['reasoning']}\n\n")

                if mention['matched_patterns']:
                    f.write(f"**Matched patterns:** {', '.join(mention['matched_patterns'])}\n\n")

                if mention['url']:
                    f.write(f"**Trove source:** <{mention['url']}>\n\n")

                f.write("**APPROVED_CLASSIFICATION:** `")
                f.write(mention['classification'])
                f.write("`\n\n")

                f.write("**REVIEW_NOTES:**\n\n")
                f.write("---\n\n")

                entry_num += 1

    print(f"\n✓ Generated classification review report: {report_path}")
    print(f"\n📋 Summary:")
    print(f"   Total entries: {len(results)}")
    print(f"   Unique hotels: {len(by_hotel)}")

    # Summary statistics
    classifications = defaultdict(int)
    confidences = defaultdict(int)
    for r in results:
        classifications[r['classification']] += 1
        confidences[r['confidence']] += 1

    print(f"\n   Initial classifications:")
    for cls, count in sorted(classifications.items(), key=lambda x: x[1], reverse=True):
        pct = count / len(results) * 100
        print(f"     {cls}: {count} ({pct:.1f}%)")

    print(f"\n   Confidence distribution:")
    for conf, count in sorted(confidences.items(), reverse=True):
        pct = count / len(results) * 100
        print(f"     {conf}/3: {count} ({pct:.1f}%)")

    print(f"\n📝 Next steps:")
    print(f"   1. Review {report_path}")
    print(f"   2. Adjust APPROVED_CLASSIFICATION values as needed")
    print(f"   3. Add REVIEW_NOTES for ambiguous cases")
    print(f"   4. Run follow-up script to apply approved classifications")


if __name__ == '__main__':
    main()
