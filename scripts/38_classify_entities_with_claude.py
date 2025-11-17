#!/usr/bin/env python3
"""
Classify entity mentions using Claude Sonnet 4.5 via entity-classifier skill.

This script demonstrates using Claude's natural language understanding to classify
dual-nature entities (hotels, churches, schools, etc.) as building-only,
business/organisation-only, or both (polyhierarchical).

Alternative to deterministic regex-based classification (script 37).

Usage:
    python scripts/38_classify_entities_with_claude.py --entity-type hotels
    python scripts/38_classify_entities_with_claude.py --entity-type churches
    python scripts/38_classify_entities_with_claude.py --interactive

The actual classification is performed by invoking the entity-classifier Claude Skill,
which uses Claude Sonnet 4.5's natural language understanding.
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
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


def extract_context(text: str, entity_name: str, context_chars: int = 400) -> str:
    """
    Extract context around first mention of entity.

    Handles orthographic variants:
    - Space/hyphen interchange: "boarding houses" matches "boarding-houses"
    - Optional plural: "boarding house" matches "boarding houses"
    - Apostrophe variants: handles both straight and curly quotes

    Returns:
        Context string, or None if entity not found
    """
    import re

    # Build flexible pattern from entity name
    pattern_str = re.escape(entity_name)

    # Space/hyphen interchange: space → space or hyphen, hyphen → space or hyphen
    pattern_str = pattern_str.replace(r"\ ", r"[\s-]")
    pattern_str = pattern_str.replace(r"\-", r"[\s-]")

    # Optional plural: make trailing 's' optional
    # Match 's' followed by word boundary or end of string
    pattern_str = re.sub(r's(\\b|\$)', r's?\\1', pattern_str, flags=re.IGNORECASE)

    # Apostrophe variants (handle straight and curly quotes)
    pattern_str = pattern_str.replace(r"\'", r"'?")

    pattern = re.compile(pattern_str, re.IGNORECASE)
    match = pattern.search(text)

    if not match:
        return None

    start, end = match.span()

    # Extract surrounding text
    context_start = max(0, start - context_chars)
    context_end = min(len(text), end + context_chars)

    context = text[context_start:context_end]

    # Try to clip at sentence boundaries
    if context_start > 0:
        first_period = context.find('. ')
        if 0 < first_period < 50:
            context = context[first_period + 2:]

    last_period = context.rfind('. ')
    if last_period > len(context) - 50:
        context = context[:last_period + 1]

    return context.strip()


def collect_entity_mentions(entity_type: str, entity_names: list) -> list:
    """
    Collect mentions of entities from Zotero with full text context.

    Returns:
        List of dicts with: entity_name, item_title, item_date, url, context
    """
    print(f"Connecting to Zotero...")
    zot = connect_to_zotero()

    mentions = []

    for entity_name in entity_names:
        print(f"\nSearching for items tagged '{entity_name}'...")

        try:
            items = zot.items(tag=entity_name)
        except Exception as e:
            print(f"  Error fetching items: {e}")
            continue

        if not items:
            print(f"  No items found")
            continue

        print(f"  Found {len(items)} items")

        for item in items:
            title = item['data'].get('title', '[No Title]')
            date = item['data'].get('date', '')
            url = item['data'].get('url', '')

            try:
                # Get full text from notes
                children = zot.children(item['key'])
                notes = [child for child in children if child['data'].get('itemType') == 'note']

                full_text = ''
                for note in notes:
                    note_content = note['data'].get('note', '')
                    full_text += strip_html(note_content) + '\n'

                if not full_text.strip() or len(full_text) < 100:
                    continue

                # Extract context around entity mention
                context = extract_context(full_text, entity_name, context_chars=350)

                if not context or len(context) < 100:
                    continue

                mentions.append({
                    'entity_name': entity_name,
                    'entity_type': entity_type,
                    'item_title': title,
                    'item_date': date,
                    'url': url,
                    'context': context
                })

                print(f"    ✓ Collected context from '{title}'")

            except Exception as e:
                print(f"    Error processing '{title}': {e}")
                continue

    return mentions


def format_mentions_for_claude(mentions: list, entity_type: str) -> str:
    """
    Format collected mentions into a prompt for Claude entity-classifier skill.

    Returns:
        Formatted prompt string
    """
    entity_type_formal = {
        'hotels': 'hotel',
        'churches': 'church',
        'schools': 'school of arts',
        'halls': 'hall',
    }.get(entity_type, entity_type)

    prompt = f"""I need you to classify {len(mentions)} mentions of {entity_type} in historical newspaper text.

For each mention below, determine whether the {entity_type_formal} should be classified as:
- **building** (Built Environment facet only)
- **business/organisation** (Agents facet only)
- **both** (polyhierarchical - appears in both facets)

Apply the entity classification heuristic, looking for spatial indicators (at/in/near, events occurring, accommodation) vs agency indicators (ownership, operations, services, financial actions).

Please analyse each mention independently and provide the structured output format specified in the skill.

---

"""

    for i, mention in enumerate(mentions, 1):
        prompt += f"""## Mention {i}

**Entity:** {mention['entity_name']}
**Item:** {mention['item_title']}"""

        if mention['item_date']:
            prompt += f" ({mention['item_date']})"

        prompt += f"""
**Trove URL:** {mention['url']}

**Context:**
> {mention['context']}

---

"""

    return prompt


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(
        description='Classify entity mentions using Claude entity-classifier skill'
    )
    parser.add_argument(
        '--entity-type',
        choices=['hotels', 'churches', 'schools', 'halls', 'boarding-houses', 'educational-schools', 'public-houses', 'banks', 'retailers'],
        help='Type of entity to classify'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of mentions to process (for testing)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: reports/claude_entity_classification_{type}.json)'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Generate prompt but require manual Claude interaction'
    )

    args = parser.parse_args()

    if not args.entity_type:
        print("Error: --entity-type is required")
        parser.print_help()
        return

    # Define entities to search for
    entity_names = {
        'hotels': [
            'Carrington Hotel', 'Imperial Hotel', 'Katoomba Hotel', 'Megalong Hotel',
            'Centennial Hotel', 'Belgravia Hotel', 'Railway Hotel', 'Wentworth Falls Hotel',
            'Mount Victoria Hotel', 'Katoomba Family Hotel', 'Grand Hotel',
            "Hoffman's House", 'Montrose House',
        ],
        'churches': [
            'Church of England', 'Methodist Church', 'Roman Catholic Church',
            'Presbyterian Church', 'Wesleyan Church', 'Congregational Church',
            'St Hilda\'s Church', 'Katoomba Congregational Church',
        ],
        'schools': [
            'Katoomba School of Arts', 'School of Arts',
        ],
        'halls': [
            'Masonic Hall', 'Odd Fellows\' Hall', 'Clarke\'s Hall',
            'Waudby\'s Hall', 'Mount Victoria Hall',
        ],
        'boarding-houses': [
            'Orama Boarding House', 'boarding house', 'Boarding house',
            'boarding houses', 'Boarding houses',
        ],
        'educational-schools': [
            'Katoomba Public School', 'Katoomba Superior Public School',
            'Megalong Valley School', 'Mount Victoria School',
            'School', 'school',
        ],
        'public-houses': [
            'Public house', 'public house', 'Pub', 'pub', 'Pubs', 'pubs',
        ],
        'banks': [
            'Bank', 'bank',
        ],
        'retailers': [
            'Store', 'store', 'Retailers and stores', 'retailers and stores',
            'retailer or store',
            'Douglas and Company', 'Nimmo\'s', "Nimmo's",
            'P. Mullany and Company', 'Peckman Bros', 'Peckman Brothers',
            'Tabrett and Company',
        ],
    }

    names = entity_names.get(args.entity_type, [])

    print("=" * 80)
    print(f"ENTITY CLASSIFICATION: {args.entity_type.upper()}")
    print("Using Claude Sonnet 4.5 via entity-classifier skill")
    print("=" * 80)
    print()

    # Collect mentions from Zotero
    mentions = collect_entity_mentions(args.entity_type, names)

    if not mentions:
        print("\nNo mentions found. Exiting.")
        return

    if args.limit:
        mentions = mentions[:args.limit]

    print(f"\n{'=' * 80}")
    print(f"Collected {len(mentions)} mentions for classification")
    print('=' * 80)
    print()

    # Format prompt for Claude
    prompt = format_mentions_for_claude(mentions, args.entity_type)

    # Save mentions and prompt
    output_dir = config.DATA_DIR / 'entity_classification'
    output_dir.mkdir(exist_ok=True)

    mentions_file = output_dir / f'{args.entity_type}_mentions.json'
    with open(mentions_file, 'w') as f:
        json.dump(mentions, f, indent=2)
    print(f"✓ Saved mentions to: {mentions_file}")

    prompt_file = output_dir / f'{args.entity_type}_classification_prompt.txt'
    with open(prompt_file, 'w') as f:
        f.write(prompt)
    print(f"✓ Saved prompt to: {prompt_file}")

    if args.interactive:
        print("\n" + "=" * 80)
        print("INTERACTIVE MODE")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Invoke the entity-classifier skill:")
        print("   `/skill entity-classifier`")
        print(f"\n2. Paste the prompt from: {prompt_file}")
        print("\n3. Save Claude's structured output")
        print(f"   Default location: reports/claude_entity_classification_{args.entity_type}.md")
        print("\n4. Use script 39 to parse Claude's output and apply classifications")
    else:
        print("\n" + "=" * 80)
        print("PROMPT READY FOR CLAUDE")
        print("=" * 80)
        print("\nTo classify these entities:")
        print("1. Copy the prompt below")
        print("2. Invoke entity-classifier skill in Claude Code")
        print("3. Paste the prompt")
        print("4. Save the structured output\n")
        print("=" * 80)
        print("\nPROMPT:\n")
        print(prompt)


if __name__ == '__main__':
    main()
