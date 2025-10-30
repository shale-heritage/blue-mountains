#!/usr/bin/env python3
"""
Create Tag Application Mapping File

Parse all approved tag decision documents and create a comprehensive
machine-readable mapping file for applying tag changes to Zotero items via API.

Sources:
- Hotel licensing action plan (13 items)
- Alcohol rationalisation report (12 items)
- Accommodation approval document (64 items with user decisions)
- Post tag action plan (TBD items)

Output: CSV file with columns:
- title: Item title
- date: Publication date
- publication: Publication name
- remove_tags: Tags to remove (pipe-separated)
- add_tags: Tags to add (pipe-separated)
- source: Which decision document this came from
- notes: Any special notes

Author: Claude Code
Date: 2025-10-30
"""

import csv
import re
from pathlib import Path
from typing import List, Dict, Any

# Input files
HOTEL_LICENSING_FILE = Path("reports/hotel_licensing_action_plan.md")
ALCOHOL_FILE = Path("reports/alcohol_rationalisation_report.md")
ACCOMMODATION_FILE = Path("reports/ACCOMMODATION_TAGS_APPROVAL.md")
POST_FILE = Path("reports/post_tag_action_plan.md")

# Output file
OUTPUT_FILE = Path("data/tag_application_mapping.csv")


def parse_hotel_licensing() -> List[Dict[str, Any]]:
    """Parse hotel licensing action plan."""
    mappings = []

    # The action plan has a table with the 13 items
    # Format: | Item # | Title | Date | Hotel Licensing | Publican's Licensing |
    with open(HOTEL_LICENSING_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the table
    table_match = re.search(
        r'\| Item # \| Title \| Date \| Hotel Licensing \| Publican\'s Licensing \|.*?\n\|[-|]+\|(.*?)(?:\n\*\*|\Z)',
        content,
        re.DOTALL
    )

    if table_match:
        rows = table_match.group(1).strip().split('\n')
        for row in rows:
            # Split by | and keep all parts including empty ones
            parts = row.split('|')
            if len(parts) >= 6:  # Should have | item | title | date | hotel | publican |
                item_num = parts[1].strip()
                title = parts[2].strip()
                date = parts[3].strip()
                hotel_lic = parts[4].strip()
                publican_lic = parts[5].strip()

                if not item_num or not title:
                    continue

                add_tags = []
                if '✓' in hotel_lic:
                    add_tags.append("Hotel licensing")
                if '✓' in publican_lic:
                    add_tags.append("Publican's licensing")

                if add_tags:
                    mappings.append({
                        'title': title,
                        'date': date,
                        'publication': '',  # Not in this report
                        'remove_tags': '',  # Not removing any tags
                        'add_tags': ' | '.join(add_tags),
                        'source': 'hotel_licensing_action_plan',
                        'notes': f'Item #{item_num}'
                    })

    print(f"Hotel licensing: Found {len(mappings)} items")
    return mappings


def parse_alcohol() -> List[Dict[str, Any]]:
    """Parse alcohol rationalisation report."""
    mappings = []

    with open(ALCOHOL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into items (each starts with ### followed by a number)
    items = re.split(r'\n### (\d+)\. ', content)[1:]

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            number = items[i]
            item_content = items[i + 1]

            # Extract fields
            title_match = re.search(r'^(.+?)\n', item_content)
            date_match = re.search(r'- \*\*Date:\*\* (.+?)\n', item_content)
            pub_match = re.search(r'- \*\*Publication:\*\* (.+?)\n', item_content)
            tags_match = re.search(r'- \*\*Proposed Tags:\*\* (.+?)(?:\n|$)', item_content)

            if title_match and date_match:
                title = title_match.group(1).strip()
                date = date_match.group(1).strip()
                publication = pub_match.group(1).strip() if pub_match else ''

                # Extract proposed tags
                add_tags = []
                if tags_match:
                    tags_text = tags_match.group(1)
                    # Tags are in backticks separated by |
                    add_tags = [t.strip().strip('`') for t in tags_text.split('|') if t.strip()]

                mappings.append({
                    'title': title,
                    'date': date,
                    'publication': publication,
                    'remove_tags': 'Alcohol',
                    'add_tags': ' | '.join(add_tags),
                    'source': 'alcohol_rationalisation_report',
                    'notes': f'Item #{number}'
                })

    print(f"Alcohol: Found {len(mappings)} items")
    return mappings


def parse_accommodation() -> List[Dict[str, Any]]:
    """Parse accommodation approval document with user decisions."""
    mappings = []

    with open(ACCOMMODATION_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into items (each starts with ### followed by a number)
    items = re.split(r'\n### (\d+)\. ', content)[1:]

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            number = items[i]
            item_content = items[i + 1]

            # Check user decision
            approved = '[X] **APPROVE**' in item_content or '[x] **APPROVE**' in item_content
            modified = '[X] **MODIFY**' in item_content or '[x] **MODIFY**' in item_content
            rejected = '[X] **REJECT**' in item_content or '[x] **REJECT**' in item_content

            # Skip if rejected or if no decision marked
            if rejected or (not approved and not modified):
                continue

            # Extract fields
            title_match = re.search(r'^(.+?)\n', item_content)
            date_match = re.search(r'\*\*Date:\*\* (.+?)(?:\n|  )', item_content)
            pub_match = re.search(r'\*\*Publication:\*\* (.+?)\n', item_content)

            if not title_match or not date_match:
                continue

            title = title_match.group(1).strip()
            date = date_match.group(1).strip()
            publication = pub_match.group(1).strip() if pub_match else ''

            # Extract proposed tags (between "Proposed new tags" and "Evidence")
            tags_section = re.search(
                r'\*\*Proposed new tags with full taxonomy:\*\*(.*?)\*\*Evidence',
                item_content,
                re.DOTALL
            )

            add_tags = []
            if tags_section:
                # Extract tag names (lines starting with - `)
                tag_lines = re.findall(r'-\s+`([^`]+)`', tags_section.group(1))
                add_tags = tag_lines

            # If MODIFY, check for additional tags in the modification text
            notes = ''
            if modified:
                modify_match = re.search(
                    r'\[X\] \*\*MODIFY\*\* - Write changes here:\s+(.+?)(?:\n\[ \]|\Z)',
                    item_content,
                    re.DOTALL
                )
                if modify_match:
                    notes = f"MODIFIED: {modify_match.group(1).strip()}"

            if add_tags or notes:
                mappings.append({
                    'title': title,
                    'date': date,
                    'publication': publication,
                    'remove_tags': 'Accommodation',
                    'add_tags': ' | '.join(add_tags) if add_tags else '',
                    'source': 'accommodation_approval',
                    'notes': notes or f'Item #{number}'
                })

    print(f"Accommodation: Found {len(mappings)} items")
    return mappings


def parse_post_tags() -> List[Dict[str, Any]]:
    """Parse post tag action plan."""
    if not POST_FILE.exists():
        print("Post tag file not found")
        return []

    mappings = []

    with open(POST_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into items (each starts with ### followed by a number)
    items = re.split(r'\n### (\d+)\. ', content)[1:]

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            number = items[i]
            item_content = items[i + 1]

            # Extract fields
            title_match = re.search(r'^(.+?)\s*\(Zotero Key:', item_content)
            date_match = re.search(r'\*\*Date:\*\* (.+?)\n', item_content)
            pub_match = re.search(r'\*\*Publication:\*\* (.+?)\n', item_content)

            # Extract add tags (lines starting with - ` after **Add:**)
            add_section = re.search(r'\*\*Add:\*\*(.*?)(?:\*\*|---|\Z)', item_content, re.DOTALL)

            if title_match and date_match:
                title = title_match.group(1).strip()
                date = date_match.group(1).strip()
                publication = pub_match.group(1).strip() if pub_match else ''

                add_tags = []
                if add_section:
                    # Extract tags from lines like: - `Tag name` (context)
                    tag_lines = re.findall(r'-\s+`([^`]+)`', add_section.group(1))
                    add_tags = tag_lines

                if add_tags:
                    mappings.append({
                        'title': title,
                        'date': date,
                        'publication': publication,
                        'remove_tags': 'Post',
                        'add_tags': ' | '.join(add_tags),
                        'source': 'post_tag_action_plan',
                        'notes': f'Item #{number}'
                    })

    print(f"Post tags: Found {len(mappings)} items")
    return mappings


def create_mapping_file():
    """Create comprehensive tag application mapping file."""
    print("Creating tag application mapping file...")
    print()

    # Parse all sources
    hotel_mappings = parse_hotel_licensing()
    alcohol_mappings = parse_alcohol()
    accommodation_mappings = parse_accommodation()
    post_mappings = parse_post_tags()

    # Combine all mappings
    all_mappings = (
        hotel_mappings +
        alcohol_mappings +
        accommodation_mappings +
        post_mappings
    )

    print()
    print(f"Total items to retag: {len(all_mappings)}")

    # Write to CSV
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as f:
        fieldnames = ['title', 'date', 'publication', 'remove_tags', 'add_tags', 'source', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_mappings)

    print(f"✓ Mapping file created: {OUTPUT_FILE}")
    print()
    print("Breakdown by source:")
    print(f"  Hotel licensing:  {len(hotel_mappings)} items")
    print(f"  Alcohol:          {len(alcohol_mappings)} items")
    print(f"  Accommodation:    {len(accommodation_mappings)} items")
    print(f"  Post tags:        {len(post_mappings)} items")
    print(f"  TOTAL:            {len(all_mappings)} items")


if __name__ == "__main__":
    create_mapping_file()
