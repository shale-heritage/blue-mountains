#!/usr/bin/env python3
"""
Script 01: Extract Tags from Zotero Group Library

This script:
1. Connects to the Zotero group library
2. Retrieves all items and their associated tags
3. Analyzes tag usage patterns
4. Generates comprehensive reports and datasets

Outputs:
- data/raw_tags.json - Complete tag data with item associations
- data/tag_frequency.csv - Tags sorted by usage frequency
- reports/tag_summary.md - Overview statistics and insights
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import pandas as pd
from pyzotero import zotero

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config

def connect_to_zotero():
    """Initialize Zotero connection"""
    print(f"Connecting to Zotero group library {config.ZOTERO_GROUP_ID}...")
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY
    )
    return zot

def fetch_all_items(zot):
    """Fetch all items from the library"""
    print("Fetching all items from library...")
    items = []
    start = 0
    limit = 100

    while True:
        batch = zot.items(start=start, limit=limit)
        if not batch:
            break
        items.extend(batch)
        start += limit
        print(f"  Retrieved {len(items)} items so far...")

    print(f"✓ Total items retrieved: {len(items)}")
    return items

def extract_tags_from_items(items):
    """Extract all tags and their associations with items"""
    print("\nExtracting tags from items...")

    tag_data = defaultdict(lambda: {
        'count': 0,
        'items': [],
        'item_titles': []
    })

    items_with_tags = 0
    items_without_tags = 0
    total_tag_applications = 0
    tags_per_item = []

    for item in items:
        item_id = item['key']
        item_title = item['data'].get('title', '[No Title]')
        item_type = item['data'].get('itemType', 'unknown')
        tags = item['data'].get('tags', [])

        if tags:
            items_with_tags += 1
            tags_per_item.append(len(tags))

            for tag_obj in tags:
                tag_name = tag_obj.get('tag', '')
                if tag_name:
                    tag_data[tag_name]['count'] += 1
                    tag_data[tag_name]['items'].append(item_id)
                    tag_data[tag_name]['item_titles'].append(item_title)
                    total_tag_applications += 1
        else:
            items_without_tags += 1

    print(f"✓ Extracted {len(tag_data)} unique tags")
    print(f"  Items with tags: {items_with_tags}")
    print(f"  Items without tags: {items_without_tags}")
    print(f"  Total tag applications: {total_tag_applications}")

    stats = {
        'total_items': len(items),
        'items_with_tags': items_with_tags,
        'items_without_tags': items_without_tags,
        'unique_tags': len(tag_data),
        'total_tag_applications': total_tag_applications,
        'avg_tags_per_item': sum(tags_per_item) / len(tags_per_item) if tags_per_item else 0,
        'max_tags_per_item': max(tags_per_item) if tags_per_item else 0,
        'min_tags_per_item': min(tags_per_item) if tags_per_item else 0
    }

    return dict(tag_data), stats

def save_raw_tags(tag_data, stats):
    """Save complete tag data to JSON"""
    output_file = config.DATA_DIR / 'raw_tags.json'
    print(f"\nSaving raw tag data to {output_file}...")

    data = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'zotero_group_id': config.ZOTERO_GROUP_ID,
            'statistics': stats
        },
        'tags': tag_data
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved to {output_file}")

def create_frequency_table(tag_data):
    """Create and save tag frequency table"""
    output_file = config.DATA_DIR / 'tag_frequency.csv'
    print(f"\nCreating tag frequency table at {output_file}...")

    # Create DataFrame
    data = []
    for tag_name, tag_info in tag_data.items():
        data.append({
            'tag': tag_name,
            'count': tag_info['count'],
            'percentage': 0  # Will calculate after
        })

    df = pd.DataFrame(data)
    df = df.sort_values('count', ascending=False)

    # Calculate percentage
    total_applications = df['count'].sum()
    df['percentage'] = (df['count'] / total_applications * 100).round(2)

    # Save
    df.to_csv(output_file, index=False)
    print(f"✓ Saved to {output_file}")

    return df

def generate_summary_report(stats, tag_data, frequency_df):
    """Generate human-readable summary report"""
    output_file = config.REPORTS_DIR / 'tag_summary.md'
    print(f"\nGenerating summary report at {output_file}...")

    # Identify tags used only once
    singleton_tags = [tag for tag, info in tag_data.items() if info['count'] == 1]

    # Get top tags
    top_tags = frequency_df.head(20)

    # Generate report content
    report = f"""# Zotero Tag Extraction Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overall Statistics

| Metric | Value |
|--------|-------|
| Total Items in Library | {stats['total_items']:,} |
| Items with Tags | {stats['items_with_tags']:,} ({stats['items_with_tags']/stats['total_items']*100:.1f}%) |
| Items without Tags | {stats['items_without_tags']:,} ({stats['items_without_tags']/stats['total_items']*100:.1f}%) |
| Unique Tags | {stats['unique_tags']:,} |
| Total Tag Applications | {stats['total_tag_applications']:,} |
| Average Tags per Item | {stats['avg_tags_per_item']:.2f} |
| Max Tags on Single Item | {stats['max_tags_per_item']} |
| Min Tags on Tagged Item | {stats['min_tags_per_item']} |

---

## Tag Usage Patterns

### Top 20 Most Frequently Used Tags

| Rank | Tag | Count | % of Total |
|------|-----|-------|------------|
"""

    for idx, row in top_tags.iterrows():
        rank = top_tags.index.get_loc(idx) + 1
        report += f"| {rank} | {row['tag']} | {row['count']} | {row['percentage']:.1f}% |\n"

    report += f"""
---

## Tags Requiring Attention

### Singleton Tags (Used Only Once)

**Count:** {len(singleton_tags)} tags

These tags may be:
- Typos or spelling variations
- Overly specific terms that should be consolidated
- Legitimate unique descriptors

**Examples (first 20):**
"""

    for tag in singleton_tags[:20]:
        report += f"- {tag}\n"

    if len(singleton_tags) > 20:
        report += f"\n*...and {len(singleton_tags) - 20} more*\n"

    report += f"""
---

## Recommendations

1. **Review singleton tags:** {len(singleton_tags)} tags are used only once. Consider consolidation.
2. **Untagged items:** {stats['items_without_tags']} items have no tags. These need to be processed.
3. **Tag standardization:** Review top tags for spelling variations and inconsistencies.
4. **Hierarchy development:** Consider grouping tags into categories based on usage patterns.

---

## Next Steps

1. Run `02_analyze_tags.py` to identify similar tags and patterns
2. Review analysis with project historians
3. Begin tag rationalization process

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved to {output_file}")

def main():
    """Main execution function"""
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - TAG EXTRACTION")
    print("Script 01: Extract all tags from Zotero group library")
    print("="*70)
    print()

    try:
        # Connect to Zotero
        zot = connect_to_zotero()

        # Fetch all items
        items = fetch_all_items(zot)

        # Extract tags
        tag_data, stats = extract_tags_from_items(items)

        # Save outputs
        save_raw_tags(tag_data, stats)
        frequency_df = create_frequency_table(tag_data)
        generate_summary_report(stats, tag_data, frequency_df)

        print("\n" + "="*70)
        print("✓ TAG EXTRACTION COMPLETE")
        print("="*70)
        print("\nOutputs created:")
        print(f"  - {config.DATA_DIR / 'raw_tags.json'}")
        print(f"  - {config.DATA_DIR / 'tag_frequency.csv'}")
        print(f"  - {config.REPORTS_DIR / 'tag_summary.md'}")
        print("\nNext: Review tag_summary.md and run 02_analyze_tags.py")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
