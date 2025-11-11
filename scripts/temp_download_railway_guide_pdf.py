#!/usr/bin/env python3
"""
Download the Blue Mountains Railway Tourist Guide PDF from Zotero.

This script uses the Zotero API to download the PDF attachment for analysis.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pyzotero import zotero

# Load environment variables
load_dotenv()

# Zotero API configuration
GROUP_ID = os.getenv("ZOTERO_GROUP_ID")
API_KEY = os.getenv("ZOTERO_API_KEY_READONLY") or os.getenv("ZOTERO_API_KEY")
LIBRARY_TYPE = os.getenv("ZOTERO_LIBRARY_TYPE", "group")

# Validate configuration
if not GROUP_ID or not API_KEY:
    print("ERROR: Zotero credentials not found in .env file", file=sys.stderr)
    sys.exit(1)

# Item and attachment keys
ITEM_KEY = "V7623AF9"  # Blue Mountains Railway Tourist Guide
ATTACHMENT_KEY = "FK8EMV8L"  # PDF attachment

# Output directory
OUTPUT_DIR = Path("data/pdfs")
OUTPUT_FILE = OUTPUT_DIR / "blue-mountains-railway-guide-1894.pdf"


def main():
    """Download the PDF attachment."""
    print("="*80)
    print("DOWNLOAD BLUE MOUNTAINS RAILWAY TOURIST GUIDE PDF")
    print("="*80)
    print()

    # Connect to Zotero
    print(f"Connecting to Zotero group library {GROUP_ID}...")
    zot = zotero.Zotero(GROUP_ID, LIBRARY_TYPE, API_KEY)
    print("✓ Connected successfully")
    print()

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Download attachment
    print(f"Downloading attachment {ATTACHMENT_KEY}...")
    try:
        # Get attachment file
        file_data = zot.file(ATTACHMENT_KEY)

        # Save to disk
        with open(OUTPUT_FILE, 'wb') as f:
            f.write(file_data)

        file_size = OUTPUT_FILE.stat().st_size
        print(f"✓ Downloaded successfully: {OUTPUT_FILE}")
        print(f"  File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        print()

        return True

    except Exception as e:
        print(f"✗ Error downloading attachment: {e}", file=sys.stderr)
        print()

        # Try alternative method - get item and check attachment details
        print("Attempting to get attachment metadata...")
        try:
            item = zot.item(ATTACHMENT_KEY)
            print(f"Attachment metadata:")
            print(f"  Title: {item.get('data', {}).get('title', 'N/A')}")
            print(f"  Content type: {item.get('data', {}).get('contentType', 'N/A')}")
            print(f"  Filename: {item.get('data', {}).get('filename', 'N/A')}")
            print(f"  Link mode: {item.get('data', {}).get('linkMode', 'N/A')}")
            print()

            # Check if it's a linked file vs stored file
            link_mode = item.get('data', {}).get('linkMode', '')
            if link_mode == 'linked_file':
                print("⚠️  This is a linked file (not stored in Zotero cloud)")
                print("    Cannot download via API - file is stored locally on your machine")
                print()
                print("    Possible local path:")
                print(f"    ~/Zotero/storage/{ATTACHMENT_KEY}/1894 - Blue Mountains Railway Tourist Guide.pdf")
                return False
            else:
                print(f"⚠️  Link mode: {link_mode}")
                print("    This may not be accessible via API")
                return False

        except Exception as e2:
            print(f"✗ Could not get attachment metadata: {e2}")
            return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
