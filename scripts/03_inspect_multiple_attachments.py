#!/usr/bin/env python3
"""
Script 03: Inspect Items with Multiple Attachments

This script examines items flagged as having multiple attachments to determine if:
1. They are multi-page articles (legitimate - keep together)
2. They contain multiple distinct primary sources (need splitting)
3. They have supplementary materials attached (may be OK)

The script retrieves full item details and all child attachments from Zotero,
then generates a detailed report for manual review.

Outputs:
- reports/multiple_attachments_inspection.md - Detailed report for review
- data/multiple_attachments_details.json - Full item data for reference
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd
from pyzotero import zotero

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config


def load_flagged_items():
    """Load list of items with multiple attachments"""
    print("Loading flagged items from quality analysis...")

    csv_file = config.DATA_DIR / 'quality_multiple_attachments.csv'
    df = pd.read_csv(csv_file)

    print(f"✓ Loaded {len(df)} items with multiple attachments")
    return df


def fetch_item_details(zot, item_key):
    """
    Fetch complete item details including all child attachments.

    Parameters:
        zot: Zotero API object
        item_key: Zotero item key/ID

    Returns:
        Dictionary with item data and children details
    """
    try:
        # Get the parent item
        item = zot.item(item_key)

        # Get all children (attachments, notes)
        children = zot.children(item_key)

        # Extract relevant information
        item_info = {
            'key': item_key,
            'title': item['data'].get('title', '[No Title]'),
            'itemType': item['data'].get('itemType', 'unknown'),
            'date': item['data'].get('date', ''),
            'publicationTitle': item['data'].get('publicationTitle', ''),
            'pages': item['data'].get('pages', ''),
            'url': item['data'].get('url', ''),
            'tags': [tag['tag'] for tag in item['data'].get('tags', [])],
            'num_children': len(children),
            'children': []
        }

        # Process each child
        for child in children:
            child_data = child['data']
            child_info = {
                'key': child['key'],
                'itemType': child_data.get('itemType', 'unknown'),
                'title': child_data.get('title', '[No Title]'),
                'filename': child_data.get('filename', ''),
                'contentType': child_data.get('contentType', ''),
                'linkMode': child_data.get('linkMode', ''),
                'note': child_data.get('note', '') if child_data.get('itemType') == 'note' else ''
            }
            item_info['children'].append(child_info)

        return item_info

    except Exception as e:
        print(f"  ⚠️  Error fetching item {item_key}: {e}")
        return None


def categorise_attachment_pattern(item_info):
    """
    Analyse attachment pattern to suggest category.

    Returns a category and reasoning:
    - 'multi_page': Likely same article across multiple pages
    - 'mixed_content': Has different types of attachments
    - 'multiple_pdfs': Multiple PDF files (may be distinct sources)
    - 'pdf_plus_notes': PDFs with text extraction notes
    - 'uncertain': Needs manual review
    """
    children = item_info['children']

    # Count by type
    pdfs = [c for c in children if c['contentType'] == 'application/pdf']
    notes = [c for c in children if c['itemType'] == 'note']
    attachments = [c for c in children if c['itemType'] == 'attachment']

    num_pdfs = len(pdfs)
    num_notes = len(notes)
    num_attachments = len(attachments)

    # Categorise
    if num_pdfs >= 2 and num_notes == 0:
        # Multiple PDFs, no notes - might be distinct sources
        category = 'multiple_pdfs'
        reasoning = f"Has {num_pdfs} PDF files with no notes. May be distinct sources combined."
        action = "HIGH PRIORITY - Review if these are separate articles"

    elif num_pdfs >= 1 and num_notes >= 1:
        # PDFs with notes - likely text extraction
        category = 'pdf_plus_notes'
        reasoning = f"Has {num_pdfs} PDF(s) and {num_notes} note(s). Likely text extraction."
        action = "LOW PRIORITY - Probably legitimate structure"

    elif num_pdfs == 0 and num_notes >= 2:
        # Multiple notes, no PDFs
        category = 'multiple_notes'
        reasoning = f"Has {num_notes} notes with no PDFs. May be transcribed text sections."
        action = "REVIEW - Check if notes should be consolidated"

    elif num_attachments > num_pdfs + num_notes:
        # Has other attachment types
        category = 'mixed_content'
        reasoning = f"Has mixed attachment types: {num_attachments} total attachments."
        action = "REVIEW - Check attachment types and purposes"

    else:
        category = 'uncertain'
        reasoning = "Pattern unclear from metadata alone."
        action = "REVIEW - Manual inspection required"

    return category, reasoning, action


def generate_inspection_report(items_details):
    """Generate detailed markdown report for manual review"""
    output_file = config.REPORTS_DIR / 'multiple_attachments_inspection.md'
    print(f"\nGenerating inspection report at {output_file}...")

    # Categorise all items
    categorised = {
        'multiple_pdfs': [],
        'pdf_plus_notes': [],
        'multiple_notes': [],
        'mixed_content': [],
        'uncertain': []
    }

    for item in items_details:
        if item:
            category, reasoning, action = categorise_attachment_pattern(item)
            item['category'] = category
            item['reasoning'] = reasoning
            item['action'] = action
            categorised[category].append(item)

    # Generate report
    report = f"""# Multiple Attachments Inspection Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overview

This report examines items with multiple attachments to identify:
- Items that may contain multiple distinct primary sources (need splitting)
- Items with legitimate multi-page or supplementary attachments (OK as-is)

**Total items inspected:** {len([i for i in items_details if i])}

---

## Summary by Category

| Category | Count | Priority | Description |
|----------|-------|----------|-------------|
| Multiple PDFs | {len(categorised['multiple_pdfs'])} | **HIGH** | Multiple PDF files - may be distinct sources |
| PDF + Notes | {len(categorised['pdf_plus_notes'])} | LOW | PDFs with text extraction notes |
| Multiple Notes | {len(categorised['multiple_notes'])} | MEDIUM | Multiple notes without PDFs |
| Mixed Content | {len(categorised['mixed_content'])} | MEDIUM | Various attachment types |
| Uncertain | {len(categorised['uncertain'])} | MEDIUM | Requires manual inspection |

---

## 1. HIGH PRIORITY: Multiple PDFs (Potential Split Candidates)

These items have multiple PDF attachments and may contain distinct primary sources
that should be separated into individual Zotero entries.

**Count:** {len(categorised['multiple_pdfs'])}

"""

    if categorised['multiple_pdfs']:
        for idx, item in enumerate(categorised['multiple_pdfs'][:20], 1):
            report += f"""### {idx}. "{item['title']}"

**Item Key:** `{item['key']}`
**Type:** {item['itemType']}
**Date:** {item['date']}
**Publication:** {item['publicationTitle']}
**Tags:** {', '.join(item['tags']) if item['tags'] else 'None'}

**Attachments ({len(item['children'])}):**

"""
            for child_idx, child in enumerate(item['children'], 1):
                report += f"{child_idx}. **{child['itemType']}:** {child['filename'] or child['title']}\n"
                if child['contentType']:
                    report += f"   - Content Type: {child['contentType']}\n"

            report += f"\n**Action Required:** {item['action']}\n"
            report += f"**Reasoning:** {item['reasoning']}\n\n"
            report += "---\n\n"

        if len(categorised['multiple_pdfs']) > 20:
            report += f"\n*Note: Showing first 20 of {len(categorised['multiple_pdfs'])} items. See JSON export for complete list.*\n\n"

    else:
        report += "*No items in this category.*\n\n"

    report += """---

## 2. PDF + Notes (Likely Text Extraction)

These items have PDFs with accompanying notes, which typically indicates
text extraction. These are usually fine as-is.

"""

    report += f"**Count:** {len(categorised['pdf_plus_notes'])}\n\n"

    if categorised['pdf_plus_notes']:
        report += "**Sample items (first 5):**\n\n"
        for idx, item in enumerate(categorised['pdf_plus_notes'][:5], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len([c for c in item['children'] if c['contentType'] == 'application/pdf'])} PDF(s), "
            report += f"{len([c for c in item['children'] if c['itemType'] == 'note'])} note(s)\n"
        report += "\n"

    report += """---

## 3. Multiple Notes (Transcribed Sections)

These items have multiple notes but no PDFs. May be transcribed text that
should be consolidated.

"""

    report += f"**Count:** {len(categorised['multiple_notes'])}\n\n"

    if categorised['multiple_notes']:
        report += "**Sample items (first 5):**\n\n"
        for idx, item in enumerate(categorised['multiple_notes'][:5], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len([c for c in item['children'] if c['itemType'] == 'note'])} note(s)\n"
        report += "\n"

    report += """---

## 4. Mixed Content

These items have various types of attachments and need individual review.

"""

    report += f"**Count:** {len(categorised['mixed_content'])}\n\n"

    if categorised['mixed_content']:
        report += "**Items requiring review:**\n\n"
        for idx, item in enumerate(categorised['mixed_content'][:10], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len(item['children'])} attachments of various types\n"
        report += "\n"

    report += """---

## 5. Uncertain Cases

These items require manual inspection to determine appropriate action.

"""

    report += f"**Count:** {len(categorised['uncertain'])}\n\n"

    if categorised['uncertain']:
        for idx, item in enumerate(categorised['uncertain'][:10], 1):
            report += f"{idx}. \"{item['title']}\" (Key: `{item['key']}`)\n"
            report += f"   - {len(item['children'])} attachments\n"
        report += "\n"

    report += f"""---

## Next Steps

### Immediate Actions

1. **Review HIGH PRIORITY items** (Multiple PDFs section)
   - Open each item in Zotero web interface: `https://www.zotero.org/groups/{config.ZOTERO_GROUP_ID}/items/ITEM_KEY`
   - Check if PDFs are: (a) same article split across pages, or (b) distinct sources
   - If distinct sources, plan to split into separate entries

2. **Spot-check other categories** to validate categorisation

3. **Document splitting workflow** if items need to be separated

### Reference

- Full item details exported to: `data/multiple_attachments_details.json`
- Use Zotero item keys to locate items in the web interface
- Take notes on which items need splitting for batch processing

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved inspection report")

    return categorised


def save_details_json(items_details):
    """Save complete item details to JSON for reference"""
    output_file = config.DATA_DIR / 'multiple_attachments_details.json'
    print(f"\nSaving detailed data to {output_file}...")

    data = {
        'generated_at': datetime.now().isoformat(),
        'zotero_group_id': config.ZOTERO_GROUP_ID,
        'total_items': len([i for i in items_details if i]),
        'items': [i for i in items_details if i]  # Filter out None values
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved details for {len(data['items'])} items")


def main():
    """Main execution function"""
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - MULTIPLE ATTACHMENTS INSPECTION")
    print("Script 03: Examine items with multiple attachments")
    print("="*70)
    print()

    try:
        # Load flagged items
        flagged_df = load_flagged_items()

        # Connect to Zotero
        print("\nConnecting to Zotero...")
        zot = zotero.Zotero(
            config.ZOTERO_GROUP_ID,
            config.ZOTERO_LIBRARY_TYPE,
            config.ZOTERO_API_KEY
        )
        print("✓ Connected")

        # Fetch details for each item
        print(f"\nFetching details for {len(flagged_df)} items...")
        print("(This may take a few minutes...)")

        items_details = []
        for idx, row in flagged_df.iterrows():
            item_key = row['key']
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(flagged_df)} items...")

            item_info = fetch_item_details(zot, item_key)
            items_details.append(item_info)

        print(f"✓ Retrieved details for {len([i for i in items_details if i])} items")

        # Generate reports
        categorised = generate_inspection_report(items_details)
        save_details_json(items_details)

        # Print summary
        print("\n" + "="*70)
        print("✓ INSPECTION COMPLETE")
        print("="*70)
        print("\nCategory Summary:")
        print(f"  HIGH PRIORITY - Multiple PDFs: {len(categorised['multiple_pdfs'])} items")
        print(f"  LOW PRIORITY - PDF + Notes: {len(categorised['pdf_plus_notes'])} items")
        print(f"  MEDIUM - Multiple Notes: {len(categorised['multiple_notes'])} items")
        print(f"  MEDIUM - Mixed Content: {len(categorised['mixed_content'])} items")
        print(f"  MEDIUM - Uncertain: {len(categorised['uncertain'])} items")
        print("\nOutputs created:")
        print(f"  - {config.REPORTS_DIR / 'multiple_attachments_inspection.md'}")
        print(f"  - {config.DATA_DIR / 'multiple_attachments_details.json'}")
        print("\nNext: Review the HIGH PRIORITY section in the report")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
