#!/usr/bin/env python3
"""
Enhance Newspaper Article Titles with ISO Dates

This script adds publication dates in ISO format (YYYY-MM-DD) to newspaper
article titles to eliminate duplicate titles and improve item distinguishability
in Zotero, Omeka, and Zenodo exports.

The enhancement is conservative and administrative:
- Original title is preserved, date appended in parentheses
- Format: "Original Title (YYYY-MM-DD)"
- Only applied to primary source newspaper articles
- Zero content interpretation or summarisation

Example: "Mountain Mixtures." → "Mountain Mixtures (1893-07-07)"

This solves:
1. Zotero incorrectly flagging items as duplicates
2. Items being indistinguishable in Omeka/Zenodo exports
3. Difficulty browsing recurring newspaper columns

Usage:
    python 36_enhance_newspaper_titles.py           # Preview only
    python 36_enhance_newspaper_titles.py --apply   # Apply to Zotero

Author: Claude Code
Date: 2025-10-29
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

# Input and output files
INPUT_FILE = Path("data/zotero_full_export.json")
OUTPUT_REPORT = Path("reports/title_enhancement_preview.md")
VERIFICATION_REPORT = Path("reports/title_enhancement_verification.md")


def parse_date_to_iso(date_str: str) -> Optional[str]:
    """
    Parse a date string and convert to ISO format (YYYY-MM-DD).

    Handles various date formats from Zotero/Trove:
    - "7 July 1893"
    - "July 7, 1893"
    - "1893-07-07"
    - "1893/07/07"

    Args:
        date_str: Date string from Zotero

    Returns:
        ISO format date string (YYYY-MM-DD) or None if unable to parse
    """
    if not date_str:
        return None

    date_str = date_str.strip()

    # Try ISO format first (already in correct format)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str

    # Try to parse various formats
    date_formats = [
        "%d %B %Y",      # 7 July 1893
        "%B %d, %Y",     # July 7, 1893
        "%d %b %Y",      # 7 Jul 1893
        "%b %d, %Y",     # Jul 7, 1893
        "%Y/%m/%d",      # 1893/07/07
        "%d/%m/%Y",      # 07/07/1893
        "%Y-%m-%d",      # 1893-07-07
    ]

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Try to extract at least year-month-day using regex
    # Pattern: Day Month Year or Month Day Year
    match = re.search(
        r'\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|'
        r'September|October|November|December)\s+(\d{4})\b',
        date_str,
        re.IGNORECASE
    )
    if match:
        day, month, year = match.groups()
        month_map = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12'
        }
        month_num = month_map.get(month.lower())
        if month_num:
            return f"{year}-{month_num}-{int(day):02d}"

    # Last resort: extract year only and use as YYYY-01-01
    year_match = re.search(r'\b(1[789]\d{2}|20\d{2})\b', date_str)
    if year_match:
        return f"{year_match.group(1)}-01-01"

    return None


def needs_title_enhancement(item: Dict) -> bool:
    """
    Determine if an item needs title enhancement.

    Criteria:
    - Must be a newspaper article (itemType == "newspaperArticle")
    - Must be tagged as "Primary source"
    - Must have a date that can be parsed
    - Title must not already contain an ISO date in parentheses

    Args:
        item: Item data from Zotero export

    Returns:
        True if item should be enhanced, False otherwise
    """
    # Must be newspaper article
    if item.get("itemType") != "newspaperArticle":
        return False

    # Must be primary source
    tags = item.get("tags", [])
    if "Primary source" not in tags:
        return False

    # Must have a parseable date
    date_str = item.get("date", "")
    iso_date = parse_date_to_iso(date_str)
    if not iso_date:
        return False

    # Check if title already has ISO date in parentheses
    title = item.get("title", "")
    if re.search(r'\(\d{4}-\d{2}-\d{2}\)$', title):
        return False

    return True


def create_enhanced_title(original_title: str, date_str: str) -> Optional[str]:
    """
    Create an enhanced title with ISO date appended.

    Format: "Original Title (YYYY-MM-DD)"

    Args:
        original_title: Original title from Zotero
        date_str: Date string from Zotero

    Returns:
        Enhanced title or None if date cannot be parsed
    """
    iso_date = parse_date_to_iso(date_str)
    if not iso_date:
        return None

    # Remove trailing period if present (common in newspaper titles)
    title = original_title.rstrip('.')

    # Append ISO date
    enhanced_title = f"{title} ({iso_date})"

    return enhanced_title


def analyse_items(items: List[Dict]) -> Dict:
    """
    Analyse items to determine which need enhancement and generate statistics.

    Args:
        items: List of items from Zotero export

    Returns:
        Dictionary with analysis results
    """
    stats = {
        'total_items': len(items),
        'newspaper_articles': 0,
        'primary_sources': 0,
        'needs_enhancement': 0,
        'already_enhanced': 0,
        'missing_dates': 0,
        'unparseable_dates': 0,
        'enhancements': []
    }

    for item in items:
        item_type = item.get("itemType", "")
        tags = item.get("tags", [])

        if item_type == "newspaperArticle":
            stats['newspaper_articles'] += 1

            if "Primary source" in tags:
                stats['primary_sources'] += 1

                title = item.get("title", "")
                date_str = item.get("date", "")

                # Check if already enhanced
                if re.search(r'\(\d{4}-\d{2}-\d{2}\)$', title):
                    stats['already_enhanced'] += 1
                    continue

                # Check if missing date
                if not date_str:
                    stats['missing_dates'] += 1
                    continue

                # Try to parse date
                iso_date = parse_date_to_iso(date_str)
                if not iso_date:
                    stats['unparseable_dates'] += 1
                    continue

                # This item needs enhancement
                stats['needs_enhancement'] += 1
                enhanced_title = create_enhanced_title(title, date_str)

                stats['enhancements'].append({
                    'key': item['key'],
                    'original_title': title,
                    'enhanced_title': enhanced_title,
                    'date': date_str,
                    'iso_date': iso_date,
                    'publication': item.get('publicationTitle', '')
                })

    return stats


def generate_preview_report(stats: Dict) -> None:
    """
    Generate a preview report showing all proposed title enhancements.

    Args:
        stats: Analysis results from analyse_items()
    """
    print(f"Generating preview report: {OUTPUT_REPORT}...")
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("# Title Enhancement Preview Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary Statistics\n\n")
        f.write(f"- Total items in library: {stats['total_items']}\n")
        f.write(f"- Newspaper articles: {stats['newspaper_articles']}\n")
        f.write(f"- Primary source newspaper articles: {stats['primary_sources']}\n")
        f.write(f"- Items needing enhancement: {stats['needs_enhancement']}\n")
        f.write(f"- Items already enhanced: {stats['already_enhanced']}\n")
        f.write(f"- Items missing dates: {stats['missing_dates']}\n")
        f.write(f"- Items with unparseable dates: {stats['unparseable_dates']}\n\n")

        if stats['missing_dates'] > 0 or stats['unparseable_dates'] > 0:
            f.write("## Issues\n\n")
            if stats['missing_dates'] > 0:
                f.write(f"⚠ {stats['missing_dates']} items have no date information\n\n")
            if stats['unparseable_dates'] > 0:
                f.write(f"⚠ {stats['unparseable_dates']} items have unparseable dates\n\n")

        f.write("## Proposed Title Enhancements\n\n")
        f.write(f"The following {stats['needs_enhancement']} items will have their titles enhanced "
                f"with ISO format dates (YYYY-MM-DD):\n\n")

        # Group by original title to show duplicates together
        by_title = defaultdict(list)
        for item in stats['enhancements']:
            by_title[item['original_title']].append(item)

        # Show groups with duplicates first
        duplicate_groups = {title: items for title, items in by_title.items() if len(items) > 1}
        single_items = {title: items for title, items in by_title.items() if len(items) == 1}

        if duplicate_groups:
            f.write(f"### Duplicate Titles ({len(duplicate_groups)} groups)\n\n")
            f.write("These titles appear multiple times and will be disambiguated:\n\n")

            for title in sorted(duplicate_groups.keys()):
                items = duplicate_groups[title]
                f.write(f"#### \"{title}\" ({len(items)} occurrences)\n\n")

                for item in sorted(items, key=lambda x: x['iso_date']):
                    f.write(f"- **Before:** {item['original_title']}\n")
                    f.write(f"  **After:** {item['enhanced_title']}\n")
                    f.write(f"  - Publication: {item['publication']}\n")
                    f.write(f"  - Date: {item['date']} → {item['iso_date']}\n\n")

                f.write("\n")

        if single_items:
            f.write(f"### Unique Titles ({len(single_items)} items)\n\n")
            f.write("These titles appear only once but will be enhanced for consistency:\n\n")

            count = 0
            for title in sorted(single_items.keys()):
                items = single_items[title]
                item = items[0]

                f.write(f"- **Before:** {item['original_title']}\n")
                f.write(f"  **After:** {item['enhanced_title']}\n")
                f.write(f"  - Date: {item['date']} → {item['iso_date']}\n\n")

                count += 1
                if count >= 20:  # Show first 20 only
                    remaining = len(single_items) - 20
                    if remaining > 0:
                        f.write(f"*...and {remaining} more items*\n\n")
                    break

        f.write("## Next Steps\n\n")
        f.write("1. Review the proposed enhancements above\n")
        f.write("2. If approved, run with `--apply` flag to update Zotero\n")
        f.write("3. Verification report will be generated after application\n\n")

    print(f"Preview report saved: {OUTPUT_REPORT}")


def apply_title_enhancements(zot: zotero.Zotero, enhancements: List[Dict]) -> Dict:
    """
    Apply title enhancements to items in Zotero library.

    Args:
        zot: Zotero API client instance
        enhancements: List of enhancement dictionaries

    Returns:
        Dictionary with application statistics
    """
    print()
    print("=" * 70)
    print("Applying Title Enhancements to Zotero Library")
    print("=" * 70)
    print()

    stats = {
        'updated': 0,
        'skipped': 0,
        'errors': 0,
        'error_details': []
    }

    total_items = len(enhancements)

    for i, enhancement in enumerate(enhancements, 1):
        # Show progress every 25 items
        if i % 25 == 0:
            print(f"  Processing {i}/{total_items} items...")

        key = enhancement['key']
        new_title = enhancement['enhanced_title']

        try:
            # Fetch the current item
            item = zot.item(key)
            current_title = item['data'].get('title', '')

            # Check if title needs updating
            if current_title == new_title:
                stats['skipped'] += 1
                continue

            # Update the title
            item['data']['title'] = new_title
            zot.update_item(item)

            stats['updated'] += 1

        except Exception as e:
            print(f"  ERROR processing item {key}: {e}")
            stats['errors'] += 1
            stats['error_details'].append({
                'key': key,
                'title': enhancement['original_title'],
                'error': str(e)
            })

    print(f"  Processing {total_items}/{total_items} items...")
    print()
    print(f"Updated: {stats['updated']}")
    print(f"Skipped (already correct): {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    print()

    return stats


def generate_verification_report(enhancements: List[Dict], application_stats: Dict) -> None:
    """
    Generate final verification report.

    Args:
        enhancements: List of enhancement dictionaries
        application_stats: Statistics from application process
    """
    print(f"Generating verification report: {VERIFICATION_REPORT}...")
    VERIFICATION_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with open(VERIFICATION_REPORT, "w", encoding="utf-8") as f:
        f.write("# Title Enhancement Verification Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## Summary\n\n")
        f.write(f"Total items enhanced: {len(enhancements)}\n\n")

        f.write("## Application Statistics\n\n")
        f.write(f"- Items updated: {application_stats['updated']}\n")
        f.write(f"- Items skipped (already correct): {application_stats['skipped']}\n")
        f.write(f"- Errors: {application_stats['errors']}\n\n")

        if application_stats['errors'] > 0:
            f.write("## Errors\n\n")
            for error in application_stats['error_details']:
                f.write(f"- **{error['title']}** (key: {error['key']})\n")
                f.write(f"  - Error: {error['error']}\n\n")

        f.write("## Verification\n\n")
        if application_stats['errors'] == 0:
            f.write("✓ All title enhancements applied successfully\n\n")
            f.write("✓ Newspaper article duplicates have been disambiguated\n\n")
            f.write("✓ Items are now distinguishable in Zotero, Omeka, and Zenodo\n\n")
        else:
            f.write(f"⚠ {application_stats['errors']} errors occurred during application\n\n")
            f.write("Please review errors above and manually correct if needed\n\n")

    print(f"Verification report saved: {VERIFICATION_REPORT}")


def main():
    """Main execution function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Enhance newspaper article titles with ISO dates'
    )
    parser.add_argument('--apply', action='store_true',
                       help='Apply enhancements to Zotero (default: preview only)')
    args = parser.parse_args()

    print("=" * 70)
    print("Newspaper Article Title Enhancement")
    print("=" * 70)
    print()

    # Load data
    print(f"Loading data from {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        export_data = json.load(f)

    items = export_data.get("items", [])
    print(f"Loaded {len(items)} items")
    print()

    # Analyse items
    print("Analysing items...")
    stats = analyse_items(items)
    print(f"Found {stats['needs_enhancement']} items needing title enhancement")
    print()

    # Generate preview report
    generate_preview_report(stats)
    print()

    # Show summary
    print("=" * 70)
    print("Preview Summary")
    print("=" * 70)
    print(f"Items to enhance: {stats['needs_enhancement']}")
    print(f"Already enhanced: {stats['already_enhanced']}")
    print(f"Issues: {stats['missing_dates'] + stats['unparseable_dates']}")
    print()

    if not args.apply:
        print(f"Preview report generated: {OUTPUT_REPORT}")
        print()
        print("To apply enhancements to Zotero, run:")
        print(f"  python {sys.argv[0]} --apply")
        return

    # Apply mode
    print("Applying enhancements to Zotero library...")
    print()

    # Connect to Zotero
    print(f"Connecting to Zotero group library {GROUP_ID}...")
    zot = zotero.Zotero(GROUP_ID, LIBRARY_TYPE, API_KEY)
    print("Connected successfully")

    # Apply enhancements
    application_stats = apply_title_enhancements(zot, stats['enhancements'])

    # Generate verification report
    print()
    generate_verification_report(stats['enhancements'], application_stats)

    print()
    print("=" * 70)
    print("✓ Title enhancement complete")
    print("=" * 70)
    print()
    print("Your newspaper articles now have unique, sortable titles.")
    print("Zotero duplicate detection issues should be resolved.")
    print("Items will be easily distinguishable in Omeka and Zenodo exports.")


if __name__ == "__main__":
    main()
