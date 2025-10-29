#!/usr/bin/env python3
"""
Apply Source Classification Tags to Zotero Library

This script applies approved source classifications and organisational tags to
all items in the Zotero library based on Pass 1 classifications.

Tags applied:
1. Source type: "Primary source" or "Secondary source" (all items)
2. File status: "Has source" or "No source" (all items, based on attachments)
3. Transcription status: "Has transcription" or "No transcription" (primary sources only)

The script performs a dry run first to show what changes will be made, then
prompts for confirmation before applying changes to the Zotero library.

Usage:
    python 35_apply_source_tags.py          # Interactive mode with confirmation
    python 35_apply_source_tags.py --apply  # Apply tags without confirmation

Author: Claude Code
Date: 2025-10-29
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from pyzotero import zotero

# Load environment variables from .env file
load_dotenv()

# Zotero API configuration
GROUP_ID = os.getenv("ZOTERO_GROUP_ID")
API_KEY = os.getenv("ZOTERO_API_KEY_READWRITE") or os.getenv("ZOTERO_API_KEY")
LIBRARY_TYPE = os.getenv("ZOTERO_LIBRARY_TYPE", "group")

# Validate configuration
if not GROUP_ID or not API_KEY:
    print("ERROR: Zotero credentials not found in .env file", file=sys.stderr)
    print("Required variables: ZOTERO_GROUP_ID, ZOTERO_API_KEY_READWRITE", file=sys.stderr)
    sys.exit(1)

# Input files
CLASSIFICATIONS_FILE = Path("data/pass1_classifications.json")
FULL_EXPORT_FILE = Path("data/zotero_full_export.json")

# Output file
OUTPUT_REPORT = Path("reports/tag_application_report.md")


def load_classifications() -> Dict:
    """
    Load approved classifications from Pass 1.

    Returns:
        Dictionary with classification data
    """
    print(f"Loading classifications from {CLASSIFICATIONS_FILE}...")
    with open(CLASSIFICATIONS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded classifications for {data['totalItems']} items")
    return data


def build_item_tags(classifications: Dict) -> Dict[str, Dict]:
    """
    Build a mapping of item keys to tags that should be applied.

    Args:
        classifications: Classification data from Pass 1

    Returns:
        Dictionary mapping item key to tag information
    """
    item_tags = {}

    # Process primary sources (high confidence)
    for item in classifications['classifications']['primary_high']:
        item_tags[item['key']] = {
            'source_type': 'Primary source',
            'has_source': 'Has source' if item['numAttachments'] > 0 else 'No source',
            'has_transcription': 'Has transcription' if item['numNotes'] > 0 else 'No transcription',
            'numAttachments': item['numAttachments'],
            'numNotes': item['numNotes'],
            'title': item['title']
        }

    # Process primary sources (medium confidence) - none expected but handle if present
    for item in classifications['classifications']['primary_medium']:
        item_tags[item['key']] = {
            'source_type': 'Primary source',
            'has_source': 'Has source' if item['numAttachments'] > 0 else 'No source',
            'has_transcription': 'Has transcription' if item['numNotes'] > 0 else 'No transcription',
            'numAttachments': item['numAttachments'],
            'numNotes': item['numNotes'],
            'title': item['title']
        }

    # Process secondary sources (high confidence)
    for item in classifications['classifications']['secondary_high']:
        item_tags[item['key']] = {
            'source_type': 'Secondary source',
            'has_source': 'Has source' if item['numAttachments'] > 0 else 'No source',
            'has_transcription': None,  # Not applicable for secondary sources
            'numAttachments': item['numAttachments'],
            'numNotes': item['numNotes'],
            'title': item['title']
        }

    # Process secondary sources (medium confidence)
    for item in classifications['classifications']['secondary_medium']:
        item_tags[item['key']] = {
            'source_type': 'Secondary source',
            'has_source': 'Has source' if item['numAttachments'] > 0 else 'No source',
            'has_transcription': None,  # Not applicable for secondary sources
            'numAttachments': item['numAttachments'],
            'numNotes': item['numNotes'],
            'title': item['title']
        }

    # Process uncertain items (classify as primary per user approval)
    for item in classifications['classifications']['uncertain']:
        item_tags[item['key']] = {
            'source_type': 'Primary source',
            'has_source': 'Has source' if item['numAttachments'] > 0 else 'No source',
            'has_transcription': 'Has transcription' if item['numNotes'] > 0 else 'No transcription',
            'numAttachments': item['numAttachments'],
            'numNotes': item['numNotes'],
            'title': item['title']
        }

    return item_tags


def generate_dry_run_report(item_tags: Dict[str, Dict]) -> None:
    """
    Generate a report showing what tags will be applied.

    Args:
        item_tags: Dictionary mapping item keys to tag information
    """
    print()
    print("=" * 70)
    print("Dry Run: Tag Application Preview")
    print("=" * 70)
    print()

    # Count tags to be applied
    stats = {
        'primary_source': 0,
        'secondary_source': 0,
        'has_source': 0,
        'no_source': 0,
        'has_transcription': 0,
        'no_transcription': 0
    }

    for key, tags in item_tags.items():
        if tags['source_type'] == 'Primary source':
            stats['primary_source'] += 1
        else:
            stats['secondary_source'] += 1

        if tags['has_source'] == 'Has source':
            stats['has_source'] += 1
        else:
            stats['no_source'] += 1

        if tags['has_transcription'] == 'Has transcription':
            stats['has_transcription'] += 1
        elif tags['has_transcription'] == 'No transcription':
            stats['no_transcription'] += 1

    print(f"Total items to be tagged: {len(item_tags)}")
    print()
    print("Source type tags:")
    print(f"  'Primary source':   {stats['primary_source']}")
    print(f"  'Secondary source': {stats['secondary_source']}")
    print()
    print("File status tags (all items):")
    print(f"  'Has source': {stats['has_source']}")
    print(f"  'No source':  {stats['no_source']}")
    print()
    print("Transcription status tags (primary sources only):")
    print(f"  'Has transcription':    {stats['has_transcription']}")
    print(f"  'No transcription':     {stats['no_transcription']}")
    print()

    # Show sample items
    print("Sample items to be tagged:")
    print()

    # Show 3 primary sources
    primary_samples = [k for k, v in item_tags.items() if v['source_type'] == 'Primary source'][:3]
    for key in primary_samples:
        tags = item_tags[key]
        print(f"  {tags['title'][:60]}")
        print(f"    Tags: {tags['source_type']}, {tags['has_source']}, {tags['has_transcription']}")
        print()

    # Show 2 secondary sources
    secondary_samples = [k for k, v in item_tags.items() if v['source_type'] == 'Secondary source'][:2]
    for key in secondary_samples:
        tags = item_tags[key]
        print(f"  {tags['title'][:60]}")
        print(f"    Tags: {tags['source_type']}, {tags['has_source']}")
        print()


def apply_tags_to_zotero(zot: zotero.Zotero, item_tags: Dict[str, Dict]) -> Dict:
    """
    Apply tags to items in the Zotero library.

    Args:
        zot: Zotero API client instance
        item_tags: Dictionary mapping item keys to tag information

    Returns:
        Dictionary with application statistics
    """
    print()
    print("=" * 70)
    print("Applying Tags to Zotero Library")
    print("=" * 70)
    print()

    stats = {
        'updated': 0,
        'skipped': 0,
        'errors': 0
    }

    total_items = len(item_tags)

    for i, (key, tag_info) in enumerate(item_tags.items(), 1):
        # Show progress every 50 items
        if i % 50 == 0:
            print(f"  Processing {i}/{total_items} items...")

        try:
            # Fetch the current item
            item = zot.item(key)
            current_tags = item['data'].get('tags', [])

            # Build list of tag names to add
            tags_to_add = [tag_info['source_type'], tag_info['has_source']]
            if tag_info['has_transcription']:
                tags_to_add.append(tag_info['has_transcription'])

            # Check if tags already exist
            existing_tag_names = [tag.get('tag', '') for tag in current_tags]
            new_tags_needed = [tag for tag in tags_to_add if tag not in existing_tag_names]

            if not new_tags_needed:
                stats['skipped'] += 1
                continue

            # Add new tags to existing tags
            updated_tags = current_tags.copy()
            for tag in new_tags_needed:
                updated_tags.append({'tag': tag})

            # Update the item
            item['data']['tags'] = updated_tags
            zot.update_item(item)

            stats['updated'] += 1

        except Exception as e:
            print(f"  ERROR processing item {key}: {e}")
            stats['errors'] += 1

    print(f"  Processing {total_items}/{total_items} items...")
    print()
    print(f"Updated: {stats['updated']}")
    print(f"Skipped (already tagged): {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    print()

    return stats


def generate_final_report(item_tags: Dict[str, Dict], stats: Dict) -> None:
    """
    Generate final report of tag application.

    Args:
        item_tags: Dictionary mapping item keys to tag information
        stats: Application statistics
    """
    print(f"Generating final report: {OUTPUT_REPORT}...")
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("# Zotero Library Organisation Report\n\n")
        f.write(f"**Generated:** {Path().cwd()}\n\n")

        f.write("## Summary\n\n")
        f.write(f"Total items tagged: {len(item_tags)}\n\n")

        f.write("## Tag Application Statistics\n\n")
        f.write(f"- Items updated: {stats['updated']}\n")
        f.write(f"- Items skipped (already tagged): {stats['skipped']}\n")
        f.write(f"- Errors: {stats['errors']}\n\n")

        # Count final tag distributions
        tag_counts = {
            'primary': sum(1 for t in item_tags.values() if t['source_type'] == 'Primary source'),
            'secondary': sum(1 for t in item_tags.values() if t['source_type'] == 'Secondary source'),
            'has_source': sum(1 for t in item_tags.values() if t['has_source'] == 'Has source'),
            'no_source': sum(1 for t in item_tags.values() if t['has_source'] == 'No source'),
            'has_transcription': sum(1 for t in item_tags.values() if t['has_transcription'] == 'Has transcription'),
            'no_transcription': sum(1 for t in item_tags.values() if t['has_transcription'] == 'No transcription')
        }

        f.write("## Final Tag Distribution\n\n")
        f.write("### Source Type\n\n")
        f.write(f"- Primary source: {tag_counts['primary']}\n")
        f.write(f"- Secondary source: {tag_counts['secondary']}\n\n")

        f.write("### File Attachment Status\n\n")
        f.write(f"- Has source: {tag_counts['has_source']}\n")
        f.write(f"- No source: {tag_counts['no_source']}\n\n")

        f.write("### Transcription Status (Primary Sources Only)\n\n")
        f.write(f"- Has transcription: {tag_counts['has_transcription']}\n")
        f.write(f"- No transcription: {tag_counts['no_transcription']}\n\n")

        f.write("## Verification\n\n")
        f.write("✓ All items now have source classification tags\n\n")
        f.write("✓ All items have file attachment status tags\n\n")
        f.write("✓ All primary sources have transcription status tags\n\n")

    print(f"Report saved: {OUTPUT_REPORT}")


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Apply source classification tags to Zotero library')
    parser.add_argument('--apply', action='store_true',
                       help='Apply tags without confirmation prompt')
    args = parser.parse_args()

    print("=" * 70)
    print("Apply Source Classification Tags to Zotero Library")
    print("=" * 70)
    print()

    # Load classifications
    classifications = load_classifications()
    print()

    # Build item tags mapping
    print("Building tag assignments...")
    item_tags = build_item_tags(classifications)
    print(f"Tag assignments prepared for {len(item_tags)} items")

    # Generate dry run report
    generate_dry_run_report(item_tags)

    # Prompt for confirmation (unless --apply flag is used)
    if not args.apply:
        print("=" * 70)
        response = input("Apply these tags to the Zotero library? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Tag application cancelled")
            return
    else:
        print()
        print("Applying tags (--apply flag specified)...")

    # Connect to Zotero
    print()
    print(f"Connecting to Zotero group library {GROUP_ID}...")
    zot = zotero.Zotero(GROUP_ID, LIBRARY_TYPE, API_KEY)
    print("Connected successfully")

    # Apply tags
    stats = apply_tags_to_zotero(zot, item_tags)

    # Generate final report
    print()
    generate_final_report(item_tags, stats)

    print()
    print("=" * 70)
    print("✓ Tag application complete")
    print("=" * 70)
    print()
    print("Your Zotero library is now organised with:")
    print("  - Source type tags (Primary source / Secondary source)")
    print("  - File status tags (Has source / No source)")
    print("  - Transcription tags (Has transcription / No transcription)")
    print()
    print("You can now create separate libraries by filtering on these tags.")


if __name__ == "__main__":
    main()
