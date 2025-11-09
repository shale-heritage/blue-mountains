#!/usr/bin/env python3
"""
Generate tag application mappings from church disambiguation report.

Parses user decisions from church_disambiguation_report.md and generates
CSV mappings for tag_application_mapping.csv.

Handles:
- Abbreviated hierarchy notation (e.g., "Agents > ... > clergy > Name")
- Typos in church names
- Synonym mapping to preferred forms
- Multiple tags per item (AND-delimited)
"""

import csv
import re
from pathlib import Path
from typing import List, Tuple, Dict

# Paths
BASE_DIR = Path(__file__).parent.parent
REPORT_PATH = BASE_DIR / "reports" / "church_disambiguation_report.md"
MAPPING_CSV = BASE_DIR / "data" / "tag_application_mapping.csv"

# Typo corrections mapping
TYPO_CORRECTIONS = {
    'Chruch': 'Church',
    'Congragational': 'Congregational',
    'Congregatonal': 'Congregational',
    'Gongregational': 'Congregational',
    'Organiation': 'organization',  # Match taxonomy (TODO: convert to UK spelling later)
    'organisation': 'organization',  # Match taxonomy (TODO: convert to UK spelling later)
    'Rev Father ': 'Reverend Father ',  # More specific - process before 'Rev '
    'Rev ': 'Reverend ',  # Expand abbreviation to match taxonomy
    'Welseyan': 'Wesleyan',
    'Weslyan': 'Wesleyan',
    'eductation': 'education',
    'builidng': 'building',
    'Building': 'building',  # Fix capitalization
    'monastaries': 'monasteries',
    'Waverly': 'Waverley',
    'Mount Victory': 'Mount Victoria',
    'Parramata': 'Parramatta',
    'Hilds': 'Hilda\'s',
    'Hilda\'s\'s': 'Hilda\'s',  # Double possessive
    'Lapmpard': 'Lampard',
    'Lverty': 'Laverty',
    'katoomba': 'Katoomba',  # Fix capitalization
    'Church of England Church': 'Church of England',  # Double "Church"
    'Catholic Church Church': 'Catholic Church',  # Double "Church"
    'dancing': 'dance',
    'University of Sydney (organisation)': 'University of Sydney (institution)',
    'University of Sydney (organization)': 'University of Sydney (institution)',
    'Canon Kemmis': 'Reverend Canon Kemmis',
    'Archbishop of Sydney': 'Archbishop',  # Generic title
    'Coadjutor Archbishop Dr Kelly': 'Coadjutor Archbishop',  # Generic title for now
    # Note: Don't add 'Father ' → 'Reverend Father ' here as it causes double replacements
    'Presbyterian Church (organization)': 'Presbyterian church (organization)',  # Lowercase 'church'
    'Wesleyan Chapel (organization)': 'Wesleyan Chapel (building)',  # User meant building based on context
    'Leura Presbyterian church (organization)': 'Presbyterian Church Leura (organization)',
    'Wentworth Falls Presbyterian church (organization)': 'Presbyterian Church Wentworth Falls (organization)',
    'Father Hyland': 'Reverend Father Hyland',
    'Father Bridge': 'Reverend Father Bridge',
}

# Synonym mappings (variant form → preferred form)
SYNONYM_MAPPINGS = {
    'Leura Presbyterian Church': 'Presbyterian Church Leura',
    'Wentworth Falls Presbyterian Church': 'Presbyterian Church Wentworth Falls',
    'Katoomba Wesleyan Church': 'Wesleyan Church Katoomba',
    'Lawson Roman Catholic Church': 'Roman Catholic Church Lawson',
    'Mount Victoria Catholic Church': 'Roman Catholic Church Mount Victoria',
    'Blackheath Catholic Church': 'Roman Catholic Church Blackheath',
    'Katoomba Methodist Church': 'Methodist Church Katoomba',
    'Anglican Church Katoomba': 'Church of England Katoomba',
    'St Joseph\'s New Church Roman Catholic Church Megalong': 'Roman Catholic Church Megalong',
    'St Joseph\'s Roman Catholic Church Megalong': 'Roman Catholic Church Megalong',
    'St Hilda\'s Church Katoomba': 'St Hilda\'s Church of England',
}

# Parent nodes to filter out (only leaf tags should be applied)
PARENT_NODES = {
    'fraternal orders',
    'lodges',
    'religious organisations',
    'churches',
    'cultural',
    'clergy',
    'occupations',
    'people',
    'agents',
    'activities',
    'organisations',
    'religious education',
    'sunday schools',
    'performance groups',
    'choirs',
    'cultural societies',
    'recreational activities',
    'social behaviours',
    'health',
    'physical conditions',
    'monasteries',
    'friaries',
    'caves',  # Geographic features category
}


def correct_typos(text: str) -> str:
    """Apply typo corrections to text."""
    for typo, correction in TYPO_CORRECTIONS.items():
        text = text.replace(typo, correction)

    # Fix double "Reverend" caused by stacked corrections
    text = text.replace('Reverend Reverend', 'Reverend')

    return text


def apply_synonym_mapping(tag: str) -> str:
    """Map variant church names to preferred forms."""
    # Check exact match
    if tag in SYNONYM_MAPPINGS:
        return SYNONYM_MAPPINGS[tag]

    # Check with parenthetical removed for base matching
    base_tag = re.sub(r'\s*\([^)]+\)$', '', tag)
    if base_tag in SYNONYM_MAPPINGS:
        # Preserve the parenthetical qualifier
        qualifier_match = re.search(r'\(([^)]+)\)$', tag)
        if qualifier_match:
            return f"{SYNONYM_MAPPINGS[base_tag]} ({qualifier_match.group(1)})"
        return SYNONYM_MAPPINGS[base_tag]

    return tag


def extract_leaf_tag(hierarchy_notation: str) -> str:
    """
    Extract leaf tag from abbreviated hierarchy notation.

    Examples:
        "Agents > ... > clergy > Rev Canon Kemmis" → "Rev Canon Kemmis"
        "churches > Katoomba Congregational Church (organisation)" → "Katoomba Congregational Church (organisation)"
        "Agents > religious organisations > religious social movements > Methodist Band of Hope" → "Methodist Band of Hope"
    """
    # Split by > and take the last part
    parts = [p.strip() for p in hierarchy_notation.split('>')]
    leaf = parts[-1]

    # Apply typo corrections
    leaf = correct_typos(leaf)

    # Apply synonym mapping
    leaf = apply_synonym_mapping(leaf)

    return leaf


def parse_decision(decision_text: str) -> List[str]:
    """
    Parse user decision to extract leaf tags.

    Args:
        decision_text: Text from **Decision**: field

    Returns:
        List of leaf tags to add

    Examples:
        "_[MODIFY to: churches > Wesleyan Chapel (building) AND (organisation)]_"
        → ["Wesleyan Chapel (building)", "Wesleyan Chapel (organisation)"]

        "_[MODIFY to: REMOVE 'Church' tag]_"
        → []
    """
    # Extract content between [ and ]
    match = re.search(r'\[([^\]]+)\]', decision_text)
    if not match:
        return []

    content = match.group(1)

    # Handle REMOVE decisions
    if 'REMOVE' in content.upper():
        return []

    # Extract part after "MODIFY to:" or just use the whole content
    if 'MODIFY to:' in content:
        content = content.split('MODIFY to:', 1)[1].strip()

    # Split by AND (case-insensitive), but also handle missing ANDs
    # First normalize spacing around AND
    tags = re.split(r'\s+AND\s+', content, flags=re.IGNORECASE)

    # Further split tags that were concatenated without AND
    # Pattern: "building) Katoomba" or "organisation) St Hilda's"
    expanded_tags = []
    for tag in tags:
        # Split on pattern: ") [Capital Letter]" (indicates missing AND)
        subtags = re.split(r'\)\s+([A-Z])', tag)
        if len(subtags) > 1:
            # Reconstruct split tags
            for i in range(0, len(subtags), 2):
                if i == 0:
                    expanded_tags.append(subtags[i] + ')')
                elif i < len(subtags) - 1:
                    expanded_tags.append(subtags[i] + subtags[i + 1])
        else:
            expanded_tags.append(tag)

    # Extract leaf tags
    leaf_tags = []
    last_church_name = None

    for tag in expanded_tags:
        tag = tag.strip()
        if not tag:
            continue

        # Handle standalone parentheticals like "(organisation)"
        if re.match(r'^\([^)]+\)$', tag) and last_church_name:
            # Append to last church name
            qualifier = tag.strip('()')
            leaf = f"{last_church_name} ({qualifier})"
            leaf = correct_typos(leaf)
            leaf = apply_synonym_mapping(leaf)
            if leaf.lower() not in PARENT_NODES:
                leaf_tags.append(leaf)
            continue

        # Extract leaf from hierarchy notation
        leaf = extract_leaf_tag(tag)

        # Skip parent nodes
        if leaf.lower() in PARENT_NODES:
            continue

        # Remember church names for standalone parentheticals
        if 'Church' in leaf or 'Chapel' in leaf:
            # Extract church name without parenthetical
            base_name = re.sub(r'\s*\([^)]+\)$', '', leaf)
            last_church_name = base_name

        if leaf:
            leaf_tags.append(leaf)

    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in leaf_tags:
        if tag not in seen:
            seen.add(tag)
            unique_tags.append(tag)

    return unique_tags


def parse_report() -> List[Dict[str, any]]:
    """
    Parse church disambiguation report to extract item details and decisions.

    Returns:
        List of dictionaries with item details
    """
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into items (each starts with "## Item N:")
    items = re.split(r'\n## Item (\d+):', content)[1:]  # Skip preamble

    # Process pairs (item_num, item_content)
    parsed_items = []
    for i in range(0, len(items), 2):
        item_num = items[i].strip()
        item_content = items[i + 1] if i + 1 < len(items) else ""

        # Extract title (first line after item number)
        title_match = re.search(r'^([^\n]+)', item_content.strip())
        title = title_match.group(1).strip() if title_match else ""

        # Extract publication and date
        pub_match = re.search(r'\*\*Publication\*\*:\s*([^(]+)\(([^)]+)\)', item_content)
        publication = pub_match.group(1).strip() if pub_match else ""
        date = pub_match.group(2).strip() if pub_match else ""

        # Extract decision
        decision_match = re.search(r'\*\*Decision\*\*:\s*(.+?)(?=\n\n|\n---|\Z)', item_content, re.DOTALL)
        decision = decision_match.group(1).strip() if decision_match else ""

        # Parse decision to get tags to add
        tags_to_add = parse_decision(decision)

        parsed_items.append({
            'item_num': int(item_num),
            'title': title,
            'publication': publication,
            'date': date,
            'decision': decision,
            'tags_to_add': tags_to_add
        })

    return parsed_items


def generate_mappings():
    """Generate tag application mappings from parsed report."""

    print("Church Disambiguation - Tag Application Mappings")
    print("=" * 60)
    print()

    # Parse report
    print("Parsing church disambiguation report...")
    items = parse_report()
    print(f"✓ Parsed {len(items)} items")
    print()

    # Read existing mappings
    rows = []
    if MAPPING_CSV.exists():
        with open(MAPPING_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    # Generate new mappings
    new_mappings = []
    for item in items:
        # Skip Item 21 (needs manual review) and Item 5 (just remove tag)
        if item['item_num'] == 21:
            print(f"⚠ Skipping Item #{item['item_num']}: {item['title']} (needs manual review)")
            continue

        # Determine tags to remove and add
        remove_tags = "church (building)"
        add_tags = " | ".join(item['tags_to_add']) if item['tags_to_add'] else ""

        # Skip if no tags to add or remove
        if not add_tags and not remove_tags:
            print(f"⚠ Skipping Item #{item['item_num']}: {item['title']} (no changes)")
            continue

        mapping = {
            'title': item['title'],
            'date': item['date'],
            'publication': item['publication'],
            'remove_tags': remove_tags,
            'add_tags': add_tags,
            'source': 'church_disambiguation_report',
            'notes': f"Item #{item['item_num']}"
        }

        new_mappings.append(mapping)
        print(f"✓ Item #{item['item_num']}: {item['title']}")
        print(f"  Remove: {remove_tags}")
        print(f"  Add: {add_tags}")
        print()

    # Append to existing mappings
    rows.extend(new_mappings)

    # Write back to CSV
    with open(MAPPING_CSV, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['title', 'date', 'publication', 'remove_tags', 'add_tags', 'source', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print()
    print("=" * 60)
    print(f"✓ Generated {len(new_mappings)} new mappings")
    print(f"✓ Total mappings in CSV: {len(rows)}")
    print()
    print(f"Output: {MAPPING_CSV}")
    print()
    print("Next steps:")
    print("  1. Review generated mappings for accuracy")
    print("  2. Handle Item #21 manually (check Zotero annotation)")
    print("  3. Validate all tags exist in taxonomy")


def main():
    """Main execution."""
    generate_mappings()


if __name__ == '__main__':
    main()
