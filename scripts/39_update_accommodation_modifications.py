#!/usr/bin/env python3
"""
Update Accommodation Modifications in Mapping File

Parse the user's MODIFY instructions from the accommodation approval document
and update the mapping file with the additional tags specified.

Author: Claude Code
Date: 2025-10-30
"""

import csv
import re
from pathlib import Path
from typing import Dict, List

APPROVAL_FILE = Path("reports/ACCOMMODATION_TAGS_APPROVAL.md")
MAPPING_FILE = Path("data/tag_application_mapping.csv")


def parse_modify_instructions() -> Dict[str, List[str]]:
    """Parse MODIFY instructions from approval document.

    Returns dict of {title+date: [list of additional tags]}
    """
    modifications = {}

    with open(APPROVAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into items
    items = re.split(r'\n### (\d+)\. ', content)[1:]

    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            number = items[i]
            item_content = items[i + 1]

            # Check if modified
            if '[X] **MODIFY**' not in item_content and '[x] **MODIFY**' not in item_content:
                continue

            # Extract title and date
            title_match = re.search(r'^(.+?)\n', item_content)
            date_match = re.search(r'\*\*Date:\*\* (.+?)(?:\n|  )', item_content)

            if not title_match or not date_match:
                continue

            title = title_match.group(1).strip()
            date = date_match.group(1).strip()
            key = f"{title}|{date}"

            # Extract MODIFY instructions
            modify_match = re.search(
                r'\[X\] \*\*MODIFY\*\* - Write changes here:\s+(.+?)(?:\n\[ \]|\Z)',
                item_content,
                re.DOTALL | re.IGNORECASE
            )

            if not modify_match:
                continue

            modify_text = modify_match.group(1).strip()

            # Parse additional tags from modify text
            additional_tags = []

            # Pattern 1: "Hierarchy > Path > Leaf Node" - extract the LAST element (leaf node)
            # Match lines with hierarchy paths - split on AND as separator between multiple paths
            modify_lines = modify_text.split(' AND')

            for line in modify_lines:
                line = line.strip()
                # Check if this is a hierarchy path
                if '>' in line:
                    # Extract the leaf node (last element after final >)
                    parts = [p.strip() for p in line.split('>')]
                    if parts:
                        leaf = parts[-1].strip()
                        # Clean up leaf node
                        leaf = re.sub(r'\s*(EXCEPT|correct|also|add|Add|Note).*$', '', leaf, flags=re.IGNORECASE).strip()
                        if leaf and len(leaf) > 1:
                            additional_tags.append(leaf)

            # Clean up tags
            additional_tags = [
                t.strip() for t in additional_tags
                if t.strip() and
                'EXCEPT' not in t and
                'AND' not in t and
                'correct' not in t.lower() and
                'above' not in t.lower() and
                'taxonomy' not in t.lower()
            ]

            if additional_tags:
                modifications[key] = additional_tags
                print(f"Item #{number}: {title} ({date})")
                print(f"  Additional tags: {', '.join(additional_tags)}")
                print()

    return modifications


def update_mapping_file(modifications: Dict[str, List[str]]):
    """Update mapping file with additional tags from modifications."""
    # Read existing mapping
    rows = []
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Update rows with modifications
    updated_count = 0
    for row in rows:
        if row['source'] == 'accommodation_approval':
            key = f"{row['title']}|{row['date']}"
            if key in modifications:
                # Add additional tags
                existing_tags = [t.strip() for t in row['add_tags'].split('|') if t.strip()]
                additional_tags = modifications[key]

                # Combine and deduplicate
                all_tags = existing_tags + additional_tags
                all_tags = list(dict.fromkeys(all_tags))  # Preserve order, remove duplicates

                row['add_tags'] = ' | '.join(all_tags)
                row['notes'] = f"Item (modified with {len(additional_tags)} additional tags)"
                updated_count += 1

    # Write back
    with open(MAPPING_FILE, "w", encoding="utf-8", newline='') as f:
        fieldnames = ['title', 'date', 'publication', 'remove_tags', 'add_tags', 'source', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated {updated_count} accommodation items with additional tags")


def main():
    """Main execution."""
    print("Parsing MODIFY instructions from accommodation approval document...")
    print()

    modifications = parse_modify_instructions()

    print(f"Found {len(modifications)} items with modifications")
    print()

    if modifications:
        print("Updating mapping file...")
        update_mapping_file(modifications)
    else:
        print("No modifications to apply")


if __name__ == "__main__":
    main()
