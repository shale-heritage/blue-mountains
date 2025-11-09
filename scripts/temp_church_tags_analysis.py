#!/usr/bin/env python3
"""
Generate church building/organization disambiguation report.

This script:
1. Adds church (organization) tags to taxonomy
2. Fetches full text for all items tagged with church (building)
3. Analyzes context to suggest appropriate tags
4. Generates decision report for user review
"""

import csv
import json
import re
from datetime import datetime
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
TAXONOMY_CSV = BASE_DIR / "data" / "tag_map_consolidated.csv"
MAPPING_CSV = BASE_DIR / "data" / "tag_application_mapping.csv"
ZOTERO_JSON = BASE_DIR / "data" / "zotero_full_export.json"
REPORT_FILE = BASE_DIR / "reports" / "church_disambiguation_report.md"


def add_organization_tags():
    """Add church (organization) tags to taxonomy."""

    # Read existing taxonomy
    rows = []
    with open(TAXONOMY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Define organization tags to add
    org_tags = [
        {
            'old_tag': 'church (organization)',
            'new_tag': 'church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches (singular generic term)'
        },
        {
            'old_tag': 'Katoomba Congregational Church (organization)',
            'new_tag': 'Katoomba Congregational Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Methodist Church (organization)',
            'new_tag': 'Methodist Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Roman Catholic Church (organization)',
            'new_tag': 'Roman Catholic Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'St Hilda\'s Church (organization)',
            'new_tag': 'St Hilda\'s Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        },
        {
            'old_tag': 'Wesleyan Church (organization)',
            'new_tag': 'Wesleyan Church (organization)',
            'action': 'hierarchy',
            'notes': 'parent=churches'
        }
    ]

    # Check if already added
    existing_tags = {row['old_tag'] for row in rows}
    new_tags = [tag for tag in org_tags if tag['old_tag'] not in existing_tags]

    if new_tags:
        rows.extend(new_tags)

        # Write back
        with open(TAXONOMY_CSV, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Added {len(new_tags)} church (organization) tags to taxonomy")
    else:
        print("✓ Church (organization) tags already exist in taxonomy")

    return len(new_tags)


def get_church_items():
    """Get all items with church (building) tags."""

    church_items = []

    with open(MAPPING_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_tags = row.get('add_tags', '')
            if 'church (building)' in add_tags.lower():
                church_items.append(row)

    print(f"✓ Found {len(church_items)} items with church (building) tags")
    return church_items


def normalize_date(date_str):
    """Normalise date for comparison (handle different formats)."""
    try:
        # Try parsing as full date
        dt = datetime.strptime(date_str, "%d %B %Y")
        return dt.strftime("%Y-%m-%d")
    except:
        try:
            # Try ISO format
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except:
            # Try year only
            if date_str.isdigit() and len(date_str) == 4:
                return date_str
            return None


def normalize_title(title):
    """Normalise title for comparison."""
    return title.strip().rstrip('.').lower()


def get_article_text(title, date, publication, zotero_items):
    """Fetch article text and URL from Zotero export."""

    search_title_norm = normalize_title(title)
    search_date_norm = normalize_date(date)

    for item in zotero_items:
        item_title_norm = normalize_title(item.get('title', ''))
        item_date_norm = normalize_date(item.get('date', ''))

        # Match on title and date
        if item_title_norm == search_title_norm:
            if item_date_norm and search_date_norm:
                if item_date_norm == search_date_norm:
                    # Found match - extract text from notes
                    notes_text = ""
                    for note in item.get('notes', []):
                        note_content = note.get('note', '')
                        # Strip HTML tags
                        note_content = re.sub(r'<[^>]+>', ' ', note_content)
                        notes_text += note_content + " "

                    trove_url = item.get('url', '')
                    manual_tags = ', '.join(item.get('tags', []))

                    return notes_text.strip(), trove_url, manual_tags

    return None, None, None


def extract_sentences_around_match(text, match_pos, num_sentences=2):
    """Extract sentences around a match position."""
    # Split into sentences (rough approximation)
    sentences = re.split(r'[.!?]+\s+', text)

    # Find which sentence contains the match
    char_count = 0
    match_sentence_idx = 0
    for idx, sentence in enumerate(sentences):
        if char_count <= match_pos < char_count + len(sentence):
            match_sentence_idx = idx
            break
        char_count += len(sentence) + 2  # +2 for punctuation and space

    # Extract surrounding sentences
    start_idx = max(0, match_sentence_idx - num_sentences)
    end_idx = min(len(sentences), match_sentence_idx + num_sentences + 1)

    context = ' '.join(sentences[start_idx:end_idx])
    return context[:300]  # Cap at 300 chars


def analyze_church_context(title, article_text, current_tags, manual_tags):
    """
    Analyse article context and suggest appropriate church tag(s).

    Returns: (suggestion, reasoning, church_excerpts)
    """

    # Combine text for analysis
    full_text = f"{title} {article_text}".lower()

    # Find all church mentions with context
    church_patterns = [
        r'church\s+(?:building|structure|edifice)',
        r'(?:congregational|methodist|roman\s+catholic|wesleyan|st\s+hilda\'?s?)\s+church',
        r'church\s+(?:service|congregation|minister|pastor|reverend)',
        r'(?:built|erected|constructed|opened).*church',
        r'church.*(?:built|erected|constructed|opened)',
        r'foundation.*church',
        r'church.*foundation',
        r'the\s+church\s+',
    ]

    church_mentions = []
    for pattern in church_patterns:
        for match in re.finditer(pattern, full_text, re.IGNORECASE):
            context = extract_sentences_around_match(full_text, match.start())
            church_mentions.append(context)

    # Remove duplicates while preserving order
    seen = set()
    church_mentions = [x for x in church_mentions if not (x in seen or seen.add(x))]

    # Keywords for building-related content (must be near "church")
    building_keywords = [
        r'church.{0,100}(?:built|erected|construction|edifice|building|structure|foundation|brick|stone|opened|dedicated|consecrated|corner\s+stone)',
        r'(?:built|erected|construction|edifice|building|structure|foundation|brick|stone|opened|dedicated|consecrated|corner\s+stone).{0,100}church',
        r'new\s+church',
        r'church.{0,50}roof',
    ]

    # Keywords for organisation-related content (must be near "church")
    org_keywords = [
        r'church.{0,100}(?:congregation|minister|reverend|rev\.|service|sermon|sunday\s+school|members|meeting|worship|social|bazaar|anniversary)',
        r'(?:congregation|minister|reverend|rev\.|service|sermon|sunday\s+school|members|meeting|worship|social|bazaar|anniversary).{0,100}church',
    ]

    # Check for building vs organization context
    has_building = any(re.search(kw, full_text, re.IGNORECASE) for kw in building_keywords)
    has_org = any(re.search(kw, full_text, re.IGNORECASE) for kw in org_keywords)

    # Determine suggestion
    if has_building and has_org:
        return "BOTH", "Article discusses both physical structure and congregation/activities", church_mentions[:3]
    elif has_building:
        return "BUILDING", "Focus on physical church structure/construction", church_mentions[:3]
    elif has_org:
        return "ORGANIZATION", "Focus on congregation/religious activities", church_mentions[:3]
    else:
        # Default: provide context for manual review
        return "REVIEW", "Church mentioned but unclear context - manual review needed", church_mentions[:3]


def generate_report(church_items):
    """Generate decision report with context analysis."""

    # Load Zotero export
    with open(ZOTERO_JSON, 'r', encoding='utf-8') as f:
        zotero_data = json.load(f)
    zotero_items = zotero_data.get('items', [])

    report_lines = [
        "# Church Building/Organisation Disambiguation Report",
        "",
        "**Generated**: 2025-11-08",
        "**Items to Review**: " + str(len(church_items)),
        "",
        "---",
        "",
        "## Instructions",
        "",
        "For each item below, review the article text excerpt and suggested tag(s).",
        "Approve or modify the suggestion based on article context.",
        "",
        "**Tag Options:**",
        "- `BUILDING` - Physical church structure only → use `(building)` tag",
        "- `ORGANIZATION` - Religious congregation/denomination only → use `(organization)` tag",
        "- `BOTH` - Article discusses both aspects → use both tags (pipe-delimited)",
        "- `REVIEW` - Insufficient context → manual review needed",
        "",
        "---",
        ""
    ]

    not_found_count = 0

    for idx, item in enumerate(church_items, 1):
        title = item.get('title', '')
        date = item.get('date', '')
        publication = item.get('publication', '')
        current_tags = item.get('add_tags', '')

        # Get article text/tags
        article_text, trove_url, manual_tags = get_article_text(
            title, date, publication, zotero_items
        )

        if not article_text:
            not_found_count += 1

        # Analyse context
        suggestion, reasoning, church_excerpts = analyze_church_context(
            title, article_text or '', current_tags, manual_tags or ''
        )

        # Format report entry
        report_lines.extend([
            f"## Item {idx}: {title}",
            "",
            f"**Publication**: {publication} ({date})",
            f"**Current tags**: `{current_tags}`",
            f"**Original folksonomy**: `{manual_tags or 'N/A'}`",
            ""
        ])

        if trove_url:
            report_lines.append(f"**Trove URL**: {trove_url}")
            report_lines.append("")

        # Add church context excerpts
        if church_excerpts:
            report_lines.append("**Church mentions in context**:")
            for excerpt in church_excerpts:
                # Clean up and format excerpt
                excerpt = excerpt.strip()
                if len(excerpt) > 250:
                    excerpt = excerpt[:250] + "..."
                report_lines.append(f"> {excerpt}")
                report_lines.append("")
        else:
            report_lines.append("**Church mentions in context**: _(No church-specific context found)_")
            report_lines.append("")

        report_lines.extend([
            f"**SUGGESTION**: `{suggestion}`",
            f"**Reasoning**: {reasoning}",
            "",
            "**Decision**: _[APPROVE / MODIFY to: ________]_",
            "",
            "---",
            ""
        ])

    # Write report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"✓ Generated report: {REPORT_FILE}")
    print(f"  Total items: {len(church_items)}")
    if not_found_count > 0:
        print(f"  Warning: {not_found_count} items not found in Zotero export")

    # Summary statistics
    suggestions = {}
    for item in church_items:
        title = item.get('title', '')
        date = item.get('date', '')
        publication = item.get('publication', '')
        current_tags = item.get('add_tags', '')
        article_text, _, manual_tags = get_article_text(title, date, publication, zotero_items)
        suggestion, _, _ = analyze_church_context(
            title, article_text or '', current_tags, manual_tags or ''
        )
        suggestions[suggestion] = suggestions.get(suggestion, 0) + 1

    print("\nSuggestion Summary:")
    for suggestion, count in sorted(suggestions.items()):
        print(f"  {suggestion}: {count} items")


def main():
    """Main execution."""

    print("Church Building/Organization Disambiguation")
    print("=" * 60)
    print()

    # Step 1: Add organization tags
    print("Step 1: Adding organization tags to taxonomy...")
    added = add_organization_tags()
    print()

    # Step 2: Get church items
    print("Step 2: Fetching items with church (building) tags...")
    church_items = get_church_items()
    print()

    # Step 3: Generate report
    print("Step 3: Generating decision report...")
    generate_report(church_items)
    print()

    print("=" * 60)
    print("✓ Complete!")
    print()
    print(f"Next steps:")
    print(f"  1. Review: {REPORT_FILE}")
    print(f"  2. Approve/modify suggestions")
    print(f"  3. Apply decisions to tag_application_mapping.csv")


if __name__ == '__main__':
    main()
