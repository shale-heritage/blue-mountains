#!/usr/bin/env python3
"""
Analyse Zotero Library Data Counts

This script provides statistics on:
1. Primary sources with full text (items with PDF or note attachments)
2. Total archaeological records (items in the library)

The script reads from:
- data/raw_tags.json: Complete library metadata and statistics
- data/quality_no_attachments.csv: Items without PDF/note attachments
- data/quality_non_primary_sources.csv: Non-primary source items
"""

import json
import csv
from pathlib import Path


def load_raw_tags_metadata():
    """Load metadata from raw_tags.json."""
    data_dir = Path(__file__).parent.parent / "data"
    with open(data_dir / "raw_tags.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["metadata"]


def load_csv_keys(filename):
    """Load Zotero item keys from a CSV file."""
    data_dir = Path(__file__).parent.parent / "data"
    keys = set()
    with open(data_dir / filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            keys.add(row["key"])
    return keys


def main():
    """Analyse and report data counts."""

    # Load metadata from raw_tags.json
    metadata = load_raw_tags_metadata()
    stats = metadata["statistics"]

    print("=" * 70)
    print("BLUE MOUNTAINS ZOTERO LIBRARY DATA ANALYSIS")
    print("=" * 70)
    print()

    # Total archaeological records (all items in library)
    total_items = stats["total_items"]
    print(f"(b) TOTAL ARCHAEOLOGICAL RECORDS: {total_items:,}")
    print()
    print("    This is the total number of items (rows) in the Zotero library,")
    print("    excluding blank/empty records.")
    print()
    print("-" * 70)
    print()

    # Load quality check files
    no_attachments_keys = load_csv_keys("quality_no_attachments.csv")
    non_primary_keys = load_csv_keys("quality_non_primary_sources.csv")

    # Items without attachments
    items_without_attachments = len(no_attachments_keys)

    # Items with attachments (has PDF or note)
    items_with_attachments = total_items - items_without_attachments

    # Primary sources (exclude non-primary sources)
    non_primary_count = len(non_primary_keys)
    primary_sources_total = total_items - non_primary_count

    # Primary sources WITH full text (has attachment AND is primary source)
    # Calculate overlap: items that are BOTH non-primary AND have no attachments
    overlap = no_attachments_keys & non_primary_keys

    # Primary sources with full text = primary sources that have attachments
    # = (items with attachments) - (non-primary sources with attachments)
    # = (items with attachments) - (non-primary sources - overlap)
    non_primary_with_attachments = non_primary_count - len(overlap)
    primary_sources_with_full_text = items_with_attachments - non_primary_with_attachments

    print(f"(a) PRIMARY SOURCES WITH FULL TEXT: {primary_sources_with_full_text:,}")
    print()
    print("    These are items that:")
    print("    - Have attached PDF documents or notes containing full text")
    print("    - Are classified as primary sources (newspapers, archival documents,")
    print("      original correspondence, etc.)")
    print()
    print("-" * 70)
    print()

    # Additional breakdown
    print("DETAILED BREAKDOWN:")
    print()
    print(f"  Total items in library:              {total_items:,}")
    print(f"  Items with attachments (PDF/notes):  {items_with_attachments:,}")
    print(f"  Items without attachments:           {items_without_attachments:,}")
    print()
    print(f"  Primary sources (all):               {primary_sources_total:,}")
    print(f"  Non-primary sources:                 {non_primary_count:,}")
    print(f"    (overlap with no attachments):     {len(overlap):,}")
    print()
    print(f"  Primary sources with full text:      {primary_sources_with_full_text:,}")
    print(f"  Primary sources without full text:   {primary_sources_total - primary_sources_with_full_text:,}")
    print()

    # Tagged items statistics
    print("-" * 70)
    print()
    print("TAGGING STATISTICS:")
    print()
    print(f"  Items with tags:                     {stats['items_with_tags']:,}")
    print(f"  Items without tags:                  {stats['items_without_tags']:,}")
    print(f"  Unique tags:                         {stats['unique_tags']:,}")
    print(f"  Total tag applications:              {stats['total_tag_applications']:,}")
    print(f"  Average tags per tagged item:        {stats['avg_tags_per_item']:.1f}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
