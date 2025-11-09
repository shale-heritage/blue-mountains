#!/usr/bin/env python3
"""
Extract Trove URLs for items needing source links in ambiguous tags decision report.
"""

import json
from datetime import datetime
from pathlib import Path

# Items needing Trove links (title, date, item_id in report)
ITEMS_NEEDED = [
    # Nellie's Glen
    ("Mountain Mixtures.", "9 September 1892", "2.2"),
    ("Town Talk.", "13 March 1903", "2.3"),
    ("A Public Meeting.", "13 January 1905", "2.9"),
    ("St Joseph's New Church, Megalong", "17 March 1905", "2.10"),
    ("Work at the Mines.", "17 April 1903", "2.11"),
    ("The Katoomba Mines.", "20 March 1903", "2.12"),
    ("Narrow Neck.", "27 December 1901", "2.13"),
    ("Brevities.", "6 April 1894", "2.14"),
    ("Katoomba Court.", "14 October 1892", "2.18"),
    ("Megalong Valley.", "1 September 1893", "2.23"),
    # Hartley Vale
    ("Town Talk.", "13 May 1904", "3.1"),
    ("Mountain Mixtures.", "4 May 1894", "3.9"),
    ("Mountain Mixtures.", "10 February 1893", "3.16"),
    ("Mountain Mixtures.", "17 June 1892", "3.17"),
    ("Hartley Vale.", "2 February 1900", "3.19"),
    # Ruined Castle
    ("Katoomba Court.", "17 March 1893", "4.11"),
]

def normalize_date(date_str):
    """Normalize date for comparison (handle different formats)."""
    try:
        # Try parsing as full date
        dt = datetime.strptime(date_str, "%d %B %Y")
        return dt.strftime("%Y-%m-%d")
    except:
        try:
            # Try ISO format
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except:
            # Try year only
            if date_str.isdigit() and len(date_str) == 4:
                return date_str
            return None

def normalize_title(title):
    """Normalize title for comparison."""
    return title.strip().rstrip('.').lower()

def main():
    # Load Zotero export
    json_path = Path('data/zotero_full_export.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data['items']
    print(f"Loaded {len(items)} items from Zotero export\n")

    # Search for each item
    results = []
    for search_title, search_date, item_id in ITEMS_NEEDED:
        search_date_norm = normalize_date(search_date)
        search_title_norm = normalize_title(search_title)

        matches = []
        for item in items:
            item_title_norm = normalize_title(item.get('title', ''))
            item_date_norm = normalize_date(item.get('date', ''))

            if item_title_norm == search_title_norm:
                if item_date_norm and search_date_norm:
                    if item_date_norm == search_date_norm:
                        matches.append(item)
                    elif search_date_norm in item_date_norm or item_date_norm in search_date_norm:
                        # Partial date match
                        matches.append(item)

        if len(matches) == 1:
            url = matches[0].get('url', 'NO URL')
            results.append((item_id, search_title, search_date, url, 'FOUND'))
            print(f"✓ Item {item_id}: {search_title} ({search_date})")
            print(f"  URL: {url}\n")
        elif len(matches) > 1:
            results.append((item_id, search_title, search_date, "MULTIPLE MATCHES", 'AMBIGUOUS'))
            print(f"⚠ Item {item_id}: {search_title} ({search_date}) - {len(matches)} matches")
            for m in matches:
                print(f"  - {m.get('date')} / {m.get('url', 'NO URL')}")
            print()
        else:
            results.append((item_id, search_title, search_date, "NOT FOUND", 'MISSING'))
            print(f"✗ Item {item_id}: {search_title} ({search_date}) - NOT FOUND\n")

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    found = sum(1 for r in results if r[4] == 'FOUND')
    ambiguous = sum(1 for r in results if r[4] == 'AMBIGUOUS')
    missing = sum(1 for r in results if r[4] == 'MISSING')

    print(f"Found: {found}/{len(ITEMS_NEEDED)}")
    print(f"Ambiguous: {ambiguous}/{len(ITEMS_NEEDED)}")
    print(f"Missing: {missing}/{len(ITEMS_NEEDED)}")

    # Write results to file
    output_path = Path('reports/trove_links_extracted.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("TROVE LINKS FOR AMBIGUOUS TAGS DECISION REPORT\n")
        f.write("="*80 + "\n\n")
        for item_id, title, date, url, status in results:
            f.write(f"Item {item_id}: {title} ({date})\n")
            f.write(f"Status: {status}\n")
            f.write(f"URL: {url}\n\n")

    print(f"\nResults written to: {output_path}")

    return results

if __name__ == '__main__':
    main()
