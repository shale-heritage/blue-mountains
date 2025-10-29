#!/usr/bin/env python3
"""
Export Complete Zotero Library Data

This script exports ALL items from the Blue Mountains Zotero group library,
including complete bibliographic metadata, tags, attachments, and notes.
This export is needed for the library organisation project to classify all
items as primary or secondary sources and to tag them with file attachment
and transcription status.

Exports to: data/zotero_full_export.json

Data included for each item:
- Item key (unique identifier)
- Item type (newspaperArticle, book, webpage, etc.)
- Bibliographic metadata (title, creator, date, publication, etc.)
- Current tags
- Attachments (count and details)
- Notes (count and content)

Author: Claude Code
Date: 2025-10-29
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from pyzotero import zotero

# Load environment variables from .env file
load_dotenv()

# Zotero API configuration
GROUP_ID = os.getenv("ZOTERO_GROUP_ID")
API_KEY = os.getenv("ZOTERO_API_KEY_READONLY") or os.getenv("ZOTERO_API_KEY")
LIBRARY_TYPE = os.getenv("ZOTERO_LIBRARY_TYPE", "group")

# Validate configuration
if not GROUP_ID or not API_KEY:
    print("ERROR: Zotero credentials not found in .env file", file=sys.stderr)
    print("Required variables: ZOTERO_GROUP_ID, ZOTERO_API_KEY_READONLY", file=sys.stderr)
    sys.exit(1)

# Output file
OUTPUT_FILE = Path("data/zotero_full_export.json")


def get_all_items(zot: zotero.Zotero) -> List[Dict[str, Any]]:
    """
    Fetch all items from the Zotero library.

    The Zotero API returns items in batches (default 100 per request).
    This function handles pagination to retrieve all items.

    Args:
        zot: Zotero API client instance

    Returns:
        List of all items with complete metadata
    """
    print("Fetching all items from Zotero library...")

    # Use everything() method which handles pagination automatically
    # Returns ALL items including attachments and notes as child items
    all_items = zot.everything(zot.items())

    print(f"Retrieved {len(all_items)} total items (including attachments and notes)")

    return all_items


def get_item_children(zot: zotero.Zotero, item_key: str) -> Dict[str, Any]:
    """
    Fetch all child items (attachments and notes) for a parent item.

    Args:
        zot: Zotero API client instance
        item_key: Key of the parent item

    Returns:
        Dictionary with 'attachments' and 'notes' lists
    """
    try:
        # Get all children of this item
        children = zot.children(item_key)

        attachments = []
        notes = []

        for child in children:
            item_type = child.get("data", {}).get("itemType", "")

            if item_type == "attachment":
                attachments.append({
                    "key": child.get("key"),
                    "title": child.get("data", {}).get("title", ""),
                    "contentType": child.get("data", {}).get("contentType", ""),
                    "filename": child.get("data", {}).get("filename", ""),
                    "tags": child.get("data", {}).get("tags", [])
                })
            elif item_type == "note":
                notes.append({
                    "key": child.get("key"),
                    "note": child.get("data", {}).get("note", ""),
                    "tags": child.get("data", {}).get("tags", [])
                })

        return {
            "attachments": attachments,
            "notes": notes
        }
    except Exception as e:
        print(f"  Warning: Could not fetch children for item {item_key}: {e}")
        return {"attachments": [], "notes": []}


def extract_item_data(item: Dict[str, Any], zot: zotero.Zotero) -> Dict[str, Any]:
    """
    Extract relevant data from a Zotero item.

    Args:
        item: Raw item data from Zotero API
        zot: Zotero API client instance

    Returns:
        Dictionary with structured item data
    """
    data = item.get("data", {})
    item_key = item.get("key", "")

    # Skip child items (attachments and notes) - we'll get these via children API
    if data.get("parentItem"):
        return None

    # Extract basic metadata
    item_data = {
        "key": item_key,
        "itemType": data.get("itemType", ""),
        "title": data.get("title", ""),
        "creators": data.get("creators", []),
        "date": data.get("date", ""),
        "publicationTitle": data.get("publicationTitle", ""),
        "url": data.get("url", ""),
        "tags": [tag.get("tag", "") for tag in data.get("tags", [])],
        "dateAdded": data.get("dateAdded", ""),
        "dateModified": data.get("dateModified", "")
    }

    # Fetch child items (attachments and notes)
    children = get_item_children(zot, item_key)
    item_data["attachments"] = children["attachments"]
    item_data["notes"] = children["notes"]
    item_data["numAttachments"] = len(children["attachments"])
    item_data["numNotes"] = len(children["notes"])

    return item_data


def main():
    """Main execution function."""
    print("=" * 70)
    print("Blue Mountains Zotero Library Export")
    print("=" * 70)
    print()

    # Connect to Zotero
    print(f"Connecting to Zotero group library {GROUP_ID}...")
    zot = zotero.Zotero(GROUP_ID, LIBRARY_TYPE, API_KEY)
    print("Connected successfully")
    print()

    # Fetch all items
    all_items = get_all_items(zot)
    print()

    # Process items and extract relevant data
    print("Processing items and fetching attachments/notes...")
    processed_items = []
    parent_items_count = 0

    for i, item in enumerate(all_items, 1):
        # Show progress every 50 items
        if i % 50 == 0:
            print(f"  Processed {i}/{len(all_items)} items...")

        item_data = extract_item_data(item, zot)

        # Only include parent items (not standalone attachments/notes)
        if item_data:
            processed_items.append(item_data)
            parent_items_count += 1

    print(f"  Processed {len(all_items)}/{len(all_items)} items...")
    print(f"Found {parent_items_count} parent items (excluding standalone attachments/notes)")
    print()

    # Save to JSON file
    print(f"Saving export to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    export_data = {
        "exportDate": "2025-10-29",
        "totalItems": parent_items_count,
        "items": processed_items
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"Export complete: {OUTPUT_FILE}")
    print()

    # Print summary statistics
    print("=" * 70)
    print("Export Summary")
    print("=" * 70)
    print(f"Total parent items exported: {parent_items_count}")

    # Count items by type
    item_types = {}
    for item in processed_items:
        item_type = item["itemType"]
        item_types[item_type] = item_types.get(item_type, 0) + 1

    print()
    print("Items by type:")
    for item_type, count in sorted(item_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {item_type}: {count}")

    # Count tagged vs untagged
    tagged = sum(1 for item in processed_items if item["tags"])
    untagged = parent_items_count - tagged
    print()
    print(f"Items with tags: {tagged}")
    print(f"Items without tags: {untagged}")

    # Count items with attachments and notes
    with_attachments = sum(1 for item in processed_items if item["numAttachments"] > 0)
    with_notes = sum(1 for item in processed_items if item["numNotes"] > 0)
    print()
    print(f"Items with attachments: {with_attachments}")
    print(f"Items with notes: {with_notes}")

    print()
    print("✓ Export complete")


if __name__ == "__main__":
    main()
