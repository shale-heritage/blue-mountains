#!/usr/bin/env python3
"""
Generate Accommodation Tag Approval Document

Parse the accommodation rationalization report and create a concise,
human-readable approval document with clear approval options.

Author: Claude Code
Date: 2025-10-30
"""

import re
from pathlib import Path

INPUT_FILE = Path("reports/accommodation_rationalization_report.md")
OUTPUT_FILE = Path("reports/ACCOMMODATION_TAGS_APPROVAL.md")


def parse_report():
    """Parse the accommodation rationalization report."""
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into items (each starts with ## followed by a number and title)
    items = re.split(r'\n## (\d+)\. ', content)[1:]  # Skip header before first item

    parsed_items = []
    for i in range(0, len(items), 2):
        if i + 1 < len(items):
            number = items[i]
            item_content = items[i + 1]

            # Extract fields
            title_match = re.search(r'^(.+?)\n', item_content)
            date_match = re.search(r'\*\*Date:\*\* (.+?)\n', item_content)
            pub_match = re.search(r'\*\*Publication:\*\* (.+?)\n', item_content)
            tags_match = re.search(r'\*\*Proposed Tag:\*\* (.+?)\n', item_content)
            hierarchy_match = re.search(r'\*\*Hierarchy Path:\*\* (.+?)\n', item_content)
            snippet_match = re.search(r'\*\*Snippet:\*\*\n\n> (.+?)\n\n', item_content, re.DOTALL)
            rationale_match = re.search(r'\*\*Rationale:\*\* (.+?)(?:\n|$)', item_content)

            title = title_match.group(1).strip() if title_match else "Unknown"
            date = date_match.group(1).strip() if date_match else "Unknown"
            publication = pub_match.group(1).strip() if pub_match else "Unknown"
            proposed_tags = tags_match.group(1).strip() if tags_match else "None"
            hierarchy_paths = hierarchy_match.group(1).strip() if hierarchy_match else "Unknown"
            snippet = snippet_match.group(1).strip() if snippet_match else "No snippet available"
            rationale = rationale_match.group(1).strip() if rationale_match else "No rationale"

            # Clean up proposed tags - split by | and clean
            tag_list = [t.strip().strip('`') for t in proposed_tags.split('|')]

            # Clean up hierarchy paths - split by | and clean
            hierarchy_list = [h.strip() for h in hierarchy_paths.split('|')]

            parsed_items.append({
                'number': number,
                'title': title,
                'date': date,
                'publication': publication,
                'tags': tag_list,
                'hierarchies': hierarchy_list,
                'snippet': snippet,
                'rationale': rationale
            })

    return parsed_items


def generate_approval_document(items):
    """Generate a clean approval document."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Accommodation Tags - Approval Document\n\n")
        f.write(f"**Generated:** 2025-10-30\n")
        f.write(f"**Items:** {len(items)} items requiring review\n")
        f.write(f"**Action:** Review each item and mark your decision\n\n")

        f.write("---\n\n")
        f.write("## Instructions\n\n")
        f.write("For each item below:\n\n")
        f.write("1. Review the proposed tags and rationale\n")
        f.write("2. Choose ONE of these actions:\n")
        f.write("   - **APPROVE** - Tags are correct, apply as proposed\n")
        f.write("   - **MODIFY** - Change tags (write your changes after the item)\n")
        f.write("   - **REJECT** - Don't change this item (explain why)\n\n")
        f.write("3. Mark your decision by replacing `[ ]` with:\n")
        f.write("   - `[A]` for APPROVE\n")
        f.write("   - `[M]` for MODIFY (and add your changes below)\n")
        f.write("   - `[R]` for REJECT (and explain why)\n\n")
        f.write("**Example:**\n")
        f.write("```\n")
        f.write("### 1. Some Article Title\n")
        f.write("**Proposed new tags with full taxonomy:**\n")
        f.write("- `Carrington Hotel`\n")
        f.write("  **Taxonomy:** Built Environment > Buildings > Hotels > Carrington Hotel\n")
        f.write("\n")
        f.write("**Evidence from source:**\n")
        f.write("> we then went to the Carrington Hotel; I called accused...\n")
        f.write("\n")
        f.write("[A] APPROVE  \n")
        f.write("[ ] MODIFY  \n")
        f.write("[ ] REJECT\n")
        f.write("```\n\n")

        f.write("---\n\n")
        f.write("## Items for Review\n\n")

        for item in items:
            f.write(f"### {item['number']}. {item['title']}\n\n")
            f.write(f"**Date:** {item['date']}  \n")
            f.write(f"**Publication:** {item['publication']}\n\n")

            f.write(f"**Current tags:** Remove `Accommodation`\n\n")
            f.write(f"**Proposed new tags with full taxonomy:**\n\n")

            # Write tags with their hierarchy paths
            for tag, hierarchy in zip(item['tags'], item['hierarchies']):
                f.write(f"- `{tag}`  \n")
                f.write(f"  **Taxonomy:** {hierarchy}\n\n")

            f.write(f"**Evidence from source:**\n\n")
            f.write(f"> {item['snippet']}\n\n")

            f.write(f"**Rationale:** {item['rationale']}\n\n")

            f.write(f"**Your decision:**\n\n")
            f.write(f"[ ] **APPROVE** - Apply tags as proposed  \n")
            f.write(f"[ ] **MODIFY** - Write changes here:  \n")
            f.write(f"[ ] **REJECT** - Explain reason:  \n\n")

            f.write("---\n\n")

        # Summary section
        f.write("## Approval Summary\n\n")
        f.write("After completing your review:\n\n")
        f.write("- [ ] All items reviewed\n")
        f.write(f"- [ ] Approved: ___ of {len(items)}\n")
        f.write(f"- [ ] Modified: ___ of {len(items)}\n")
        f.write(f"- [ ] Rejected: ___ of {len(items)}\n\n")

        f.write("**Next steps:**\n")
        f.write("1. Save this file with your decisions\n")
        f.write("2. Let Claude Code know you've completed the review\n")
        f.write("3. Claude Code will update the CSV based on your decisions\n")


def main():
    """Main execution."""
    print("Parsing accommodation rationalization report...")
    items = parse_report()
    print(f"Found {len(items)} items")

    print(f"Generating approval document: {OUTPUT_FILE}...")
    generate_approval_document(items)

    print(f"✓ Approval document created: {OUTPUT_FILE}")
    print(f"  Items: {len(items)}")
    print()
    print("Next steps:")
    print(f"1. Open: {OUTPUT_FILE}")
    print("2. Review each item and mark [A], [M], or [R]")
    print("3. Save the file when done")
    print("4. Let Claude Code know you've finished")


if __name__ == "__main__":
    main()
