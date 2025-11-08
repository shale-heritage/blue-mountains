#!/usr/bin/env python3
"""
Extract contexts for specific orphaned tags to help determine their meaning.
"""

import csv
import sys

# Tags to check
TAGS_TO_CHECK = [
    "Carrington",
    "Katoomba South mines",
    "Katoomba Street",
    "Mining settlements"
]

def main():
    """Extract contexts for orphaned tags."""

    # This would need the actual Zotero export with full text
    # For now, let me check tag_frequency to see usage counts

    print("Orphaned Tag Usage Frequencies:\n")
    print("=" * 80)

    with open('data/tag_frequency.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row['tag']
            if tag in TAGS_TO_CHECK:
                count = row['count']
                pct = row['percentage']
                print(f"{tag}: {count} items ({pct}%)")

    print("\n" + "=" * 80)
    print("\nNote: Full text context analysis requires Zotero export data.")
    print("Recommend using web search for historical verification.")

if __name__ == '__main__':
    main()
