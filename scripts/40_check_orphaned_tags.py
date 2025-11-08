#!/usr/bin/env python3
"""
Check for orphaned tags in Zotero library.

Identifies tags currently applied to items that have no mapping in
tag_map_consolidated.csv. This ensures no tags will be lost when applying
the consolidated taxonomy.
"""

import csv
from pathlib import Path
from collections import defaultdict

def load_current_tags():
    """Load all tags currently applied to Zotero items from tag_frequency.csv."""
    tags = set()
    with open('data/tag_frequency.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags.add(row['tag'])
    return tags

def load_mapped_tags():
    """
    Load all tags that have mappings in tag_map_consolidated.csv.

    Returns:
        mapped_tags: Set of all tags that appear in either new_tag or old_tag columns
        mapping_info: Dict mapping each tag to its mapping type(s) and target(s)
    """
    mapped_tags = set()
    mapping_info = defaultdict(list)

    with open('data/tag_map_consolidated.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue

            new_tag = row[0].strip()
            old_tag = row[1].strip()
            action = row[2].strip()
            notes = row[3].strip() if len(row) > 3 else ''

            # Add both new_tag and old_tag to mapped set
            if new_tag:
                mapped_tags.add(new_tag)
            if old_tag:
                mapped_tags.add(old_tag)

            # Track mapping information for old_tag
            if old_tag and action:
                mapping_info[old_tag].append({
                    'action': action,
                    'target': new_tag,
                    'notes': notes
                })

    return mapped_tags, mapping_info

def main():
    """Identify and report orphaned tags."""
    print("Checking for orphaned tags...\n")

    # Load data
    print("Loading current tags from tag_frequency.csv...")
    current_tags = load_current_tags()
    print(f"Found {len(current_tags)} unique tags currently applied to items\n")

    print("Loading mapped tags from tag_map_consolidated.csv...")
    mapped_tags, mapping_info = load_mapped_tags()
    print(f"Found {len(mapped_tags)} unique tags with mappings\n")

    # Find orphans - first exact match, then case-insensitive
    exact_orphaned = current_tags - mapped_tags

    # Create lowercase lookup for mapped tags
    mapped_lower = {tag.lower(): tag for tag in mapped_tags}

    # Separate into true orphans vs capitalization differences
    true_orphans = []
    capitalization_only = []

    for tag in exact_orphaned:
        if tag.lower() in mapped_lower:
            capitalization_only.append((tag, mapped_lower[tag.lower()]))
        else:
            true_orphans.append(tag)

    # Report capitalization differences
    if capitalization_only:
        print(f"📝 Found {len(capitalization_only)} tags with capitalization differences:")
        print("(These will be automatically fixed during tag rewrite)")
        print("=" * 80)
        for old, new in sorted(capitalization_only)[:10]:
            print(f"  • {old!r} → {new!r}")
        if len(capitalization_only) > 10:
            print(f"  ... and {len(capitalization_only) - 10} more")
        print()

    # Report true orphans
    if not true_orphans:
        print("✓ SUCCESS: No truly orphaned tags found!")
        print("All tags currently on items have mappings (accounting for capitalization)")
        return 0

    print(f"⚠ WARNING: Found {len(true_orphans)} truly orphaned tags:\n")
    print("These tags have no mapping (even case-insensitive):")
    print("=" * 80)

    for tag in sorted(true_orphans):
        print(f"  • {tag}")

    print("\n" + "=" * 80)
    print(f"\nTotal orphaned tags: {len(true_orphans)}")
    print("\nNext steps:")
    print("1. Review these tags against planning/consolidation-decisions.md")
    print("2. For intentionally removed tags, document the decision")
    print("3. For unintentionally missed tags, add mappings to tag_map_consolidated.csv")

    return 1

if __name__ == '__main__':
    exit(main())
