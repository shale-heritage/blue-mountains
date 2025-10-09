#!/usr/bin/env python3
"""
Script 02: Analyze Tags and Data Quality

This script analyzes the extracted tags to:
1. Identify similar/duplicate tags (fuzzy matching)
2. Detect potential hierarchical relationships
3. Calculate tag co-occurrence patterns
4. Identify data quality issues:
   - Duplicate items
   - Non-primary source items
   - Items with multiple attachments (need splitting)
   - Items missing PDFs

Outputs:
- data/similar_tags.csv - Suggested tag merges
- data/tag_network.json - Co-occurrence patterns
- reports/tag_analysis.md - Detailed analysis
- reports/data_quality_issues.md - Items requiring attention
- visualizations/tag_cooccurrence.png - Network visualization
"""

import json
import sys
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
from itertools import combinations
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from pyzotero import zotero

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
import config

def load_tag_data():
    """Load previously extracted tag data"""
    print("Loading tag data from previous extraction...")
    with open(config.DATA_DIR / 'raw_tags.json', 'r') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data['tags'])} tags")
    return data['tags'], data['metadata']['statistics']

def find_similar_tags(tags, threshold=80):
    """Find similar tags using fuzzy string matching"""
    print(f"\nAnalyzing tag similarity (threshold: {threshold})...")

    tag_list = list(tags.keys())
    similar_pairs = []

    for i, tag1 in enumerate(tag_list):
        for tag2 in tag_list[i+1:]:
            # Calculate different similarity metrics
            ratio = fuzz.ratio(tag1.lower(), tag2.lower())
            partial = fuzz.partial_ratio(tag1.lower(), tag2.lower())
            token_sort = fuzz.token_sort_ratio(tag1.lower(), tag2.lower())

            max_similarity = max(ratio, partial, token_sort)

            if max_similarity >= threshold:
                similar_pairs.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count1': tags[tag1]['count'],
                    'count2': tags[tag2]['count'],
                    'similarity': max_similarity,
                    'ratio': ratio,
                    'partial': partial,
                    'token_sort': token_sort,
                    'suggested_merge': tag1 if tags[tag1]['count'] >= tags[tag2]['count'] else tag2
                })

    print(f"✓ Found {len(similar_pairs)} similar tag pairs")
    return similar_pairs

def detect_hierarchies(tags):
    """Detect potential hierarchical relationships"""
    print("\nDetecting potential hierarchies...")

    hierarchies = []
    tag_list = list(tags.keys())

    for tag in tag_list:
        tag_lower = tag.lower()

        # Check if this tag is contained in other tags
        for other_tag in tag_list:
            if tag == other_tag:
                continue

            other_lower = other_tag.lower()

            # Check if one tag is a substring of another
            if tag_lower in other_lower and tag_lower != other_lower:
                hierarchies.append({
                    'broader_term': other_tag,
                    'narrower_term': tag,
                    'broader_count': tags[other_tag]['count'],
                    'narrower_count': tags[tag]['count'],
                    'relationship': 'substring'
                })

    print(f"✓ Found {len(hierarchies)} potential hierarchical relationships")
    return hierarchies

def calculate_cooccurrence(tags):
    """Calculate tag co-occurrence patterns"""
    print("\nCalculating tag co-occurrence patterns...")

    # Build co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))

    # Get all items and their tags
    item_tags = defaultdict(set)
    for tag_name, tag_info in tags.items():
        for item_id in tag_info['items']:
            item_tags[item_id].add(tag_name)

    # Count co-occurrences
    total_pairs = 0
    for item_id, item_tag_set in item_tags.items():
        if len(item_tag_set) >= 2:
            for tag1, tag2 in combinations(sorted(item_tag_set), 2):
                cooccurrence[tag1][tag2] += 1
                cooccurrence[tag2][tag1] += 1
                total_pairs += 1

    print(f"✓ Calculated {total_pairs} tag pair co-occurrences")

    # Convert to list format
    cooccurrence_list = []
    processed = set()

    for tag1 in cooccurrence:
        for tag2, count in cooccurrence[tag1].items():
            pair = tuple(sorted([tag1, tag2]))
            if pair not in processed:
                cooccurrence_list.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count': count,
                    'tag1_total': tags[tag1]['count'],
                    'tag2_total': tags[tag2]['count']
                })
                processed.add(pair)

    # Sort by count
    cooccurrence_list.sort(key=lambda x: x['count'], reverse=True)

    return cooccurrence_list

def analyze_data_quality(zot):
    """Analyze data quality issues"""
    print("\nAnalyzing data quality issues...")

    # Fetch all items
    print("  Fetching items for quality analysis...")
    items = []
    start = 0
    limit = 100

    while True:
        batch = zot.items(start=start, limit=limit)
        if not batch:
            break
        items.extend(batch)
        start += limit

    print(f"  Analyzing {len(items)} items...")

    # Analyze items
    issues = {
        'duplicates': [],
        'non_primary_sources': [],
        'multiple_attachments': [],
        'no_attachments': [],
        'no_text_extraction': []
    }

    # Track for duplicate detection
    title_map = defaultdict(list)

    for item in items:
        item_data = item['data']
        item_key = item['key']
        item_type = item_data.get('itemType', 'unknown')
        title = item_data.get('title', '[No Title]')

        # Check for duplicates (same title)
        title_map[title.lower()].append({
            'key': item_key,
            'title': title,
            'itemType': item_type,
            'date': item_data.get('date', '')
        })

        # Check for non-primary sources
        if item_type in ['note', 'annotation', 'attachment']:
            issues['non_primary_sources'].append({
                'key': item_key,
                'title': title,
                'itemType': item_type
            })

        # Check attachments
        num_children = item.get('meta', {}).get('numChildren', 0)

        if num_children > 1:
            # Might have multiple PDFs
            issues['multiple_attachments'].append({
                'key': item_key,
                'title': title,
                'num_attachments': num_children
            })
        elif num_children == 0:
            # No attachments at all
            issues['no_attachments'].append({
                'key': item_key,
                'title': title
            })

    # Identify duplicates (titles appearing more than once)
    for title, item_list in title_map.items():
        if len(item_list) > 1:
            issues['duplicates'].extend(item_list)

    print(f"✓ Quality analysis complete")
    print(f"  Potential duplicates: {len(issues['duplicates'])} items")
    print(f"  Non-primary sources: {len(issues['non_primary_sources'])} items")
    print(f"  Multiple attachments: {len(issues['multiple_attachments'])} items")
    print(f"  No attachments: {len(issues['no_attachments'])} items")

    return issues

def save_similar_tags(similar_pairs):
    """Save similar tags analysis"""
    output_file = config.DATA_DIR / 'similar_tags.csv'
    print(f"\nSaving similar tags to {output_file}...")

    df = pd.DataFrame(similar_pairs)
    df = df.sort_values('similarity', ascending=False)
    df.to_csv(output_file, index=False)

    print(f"✓ Saved {len(similar_pairs)} similar tag pairs")

def save_cooccurrence(cooccurrence_list):
    """Save co-occurrence data"""
    output_file = config.DATA_DIR / 'tag_network.json'
    print(f"\nSaving tag co-occurrence network to {output_file}...")

    data = {
        'generated_at': datetime.now().isoformat(),
        'cooccurrences': cooccurrence_list
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(cooccurrence_list)} tag co-occurrence pairs")

def visualize_cooccurrence(cooccurrence_list, tags, top_n=30):
    """Create network visualization of tag co-occurrence"""
    output_file = config.VISUALIZATIONS_DIR / 'tag_cooccurrence.png'
    print(f"\nCreating co-occurrence visualization at {output_file}...")

    # Create graph
    G = nx.Graph()

    # Get top tags by frequency
    top_tags = sorted(tags.items(), key=lambda x: x[1]['count'], reverse=True)[:top_n]
    top_tag_names = {t[0] for t in top_tags}

    # Add edges for top tags only
    for co in cooccurrence_list:
        if co['tag1'] in top_tag_names and co['tag2'] in top_tag_names:
            if co['count'] >= 3:  # Only show significant co-occurrences
                G.add_edge(co['tag1'], co['tag2'], weight=co['count'])

    if len(G.nodes()) == 0:
        print("⚠ Not enough data for visualization")
        return

    # Create visualization
    plt.figure(figsize=(16, 12))

    # Use spring layout
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Node sizes based on tag frequency
    node_sizes = [tags[node]['count'] * 30 for node in G.nodes()]

    # Edge widths based on co-occurrence count
    edge_widths = [G[u][v]['weight'] * 0.3 for u, v in G.edges()]

    # Draw network
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                          node_color='lightblue', alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    plt.title('Tag Co-occurrence Network (Top 30 Tags)', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    print(f"✓ Saved visualization with {len(G.nodes())} nodes and {len(G.edges())} edges")

def generate_analysis_report(similar_pairs, hierarchies, cooccurrence_list, stats):
    """Generate comprehensive analysis report"""
    output_file = config.REPORTS_DIR / 'tag_analysis.md'
    print(f"\nGenerating analysis report at {output_file}...")

    report = f"""# Tag Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## 1. Similar Tags Analysis

### Overview

Found **{len(similar_pairs)}** pairs of similar tags that may need consolidation.

These represent potential duplicates, spelling variations, or related terms that should be standardized.

### Top 20 Most Similar Tag Pairs (Recommended for Review)

| Tag 1 | Tag 2 | Similarity | Count 1 | Count 2 | Suggested Merge To |
|-------|-------|------------|---------|---------|-------------------|
"""

    for pair in similar_pairs[:20]:
        report += f"| {pair['tag1']} | {pair['tag2']} | {pair['similarity']}% | {pair['count1']} | {pair['count2']} | **{pair['suggested_merge']}** |\n"

    report += f"""

### Similarity Metrics Explained

- **Ratio:** Overall string similarity
- **Partial:** Substring matching
- **Token Sort:** Word-order independent matching

All pairs shown have at least 80% similarity in one metric.

---

## 2. Hierarchical Relationships

### Overview

Found **{len(hierarchies)}** potential parent-child relationships between tags.

These suggest opportunities to create a hierarchical taxonomy.

"""

    if hierarchies:
        report += """### Detected Hierarchies (Top 20)

| Broader Term | Narrower Term | Broader Count | Narrower Count |
|--------------|---------------|---------------|----------------|
"""
        for h in hierarchies[:20]:
            report += f"| {h['broader_term']} | {h['narrower_term']} | {h['broader_count']} | {h['narrower_count']} |\n"
    else:
        report += "*No clear hierarchical relationships detected in tag names.*\n"

    report += """

**Note:** These are detected based on substring matching. Manual review recommended to determine true hierarchical relationships.

---

## 3. Tag Co-occurrence Patterns

### Overview

Analyzed how tags appear together on the same items.

This reveals thematic clusters and suggests potential tag categories.

### Top 30 Most Common Tag Pairs

| Tag 1 | Tag 2 | Co-occurrence Count | Tag 1 Total | Tag 2 Total |
|-------|-------|---------------------|-------------|-------------|
"""

    for co in cooccurrence_list[:30]:
        report += f"| {co['tag1']} | {co['tag2']} | {co['count']} | {co['tag1_total']} | {co['tag2_total']} |\n"

    report += f"""

### Insights from Co-occurrence

**Strong Thematic Clusters:** Tags that frequently appear together suggest content categories.

**Visualization:** See `visualizations/tag_cooccurrence.png` for network graph showing relationships between top tags.

---

## 4. Recommendations for Tag Rationalization

Based on this analysis, here are recommended next steps:

### A. Similar Tags to Consolidate

1. **Review high-similarity pairs** (>90% similarity) - likely duplicates or spelling variations
2. **Standardize singular/plural forms** - choose a convention (e.g., always plural)
3. **Resolve case inconsistencies** - establish capitalization rules

### B. Develop Hierarchical Taxonomy

Consider organizing tags into categories based on:

1. **Geographic hierarchy:** Region → Town → Specific location
2. **Thematic categories:** Industries, Social institutions, Events
3. **Temporal categories:** Time periods, specific dates
4. **Actor types:** People, Organizations, Government entities

### C. Tag Categories (Suggested from Top Tags)

Based on frequency and co-occurrence:

**Geographic:**
- Katoomba, Megalong, Lithgow, Hartley Vale, etc.

**Industry:**
- Shale mines, Mining, Miners, Coal, Railway

**Social:**
- Court, Court cases, Death, Church, Salvation Army
- Recreation for miners, Sports

**Infrastructure:**
- Hotels, Accommodation, Railway

**Organizations:**
- A.K.O. & M. Company

### D. Next Steps

1. **Collaborative review** with project historians
2. **Create controlled vocabulary** with definitions
3. **Map tags to standard vocabularies** (Getty, etc.)
4. **Develop tagging guidelines** for consistency

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved analysis report")

def generate_quality_report(issues):
    """Generate data quality report"""
    output_file = config.REPORTS_DIR / 'data_quality_issues.md'
    print(f"\nGenerating data quality report at {output_file}...")

    report = f"""# Data Quality Issues Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overview

This report identifies items requiring attention before proceeding with tagging and publication.

---

## 1. Duplicate Items

**Count:** {len(issues['duplicates'])} items with duplicate titles

These items have identical titles and may represent:
- Duplicate entries that should be merged
- Different articles with the same headline (legitimate)
- Different editions of the same article

### Action Required

Review these items to determine if they should be:
1. Merged (if truly duplicates)
2. Differentiated (add edition/date to title)
3. Kept separate (if genuinely different articles)

"""

    if issues['duplicates']:
        # Group duplicates by title
        dup_groups = defaultdict(list)
        for item in issues['duplicates']:
            dup_groups[item['title'].lower()].append(item)

        report += f"**Duplicate title groups:** {len(dup_groups)}\n\n"
        report += "### Examples (first 10 groups):\n\n"

        for idx, (title, items) in enumerate(list(dup_groups.items())[:10], 1):
            report += f"**{idx}. \"{items[0]['title']}\"** ({len(items)} items)\n"
            for item in items:
                report += f"   - Key: `{item['key']}`, Type: {item['itemType']}, Date: {item['date']}\n"
            report += "\n"

    report += """---

## 2. Non-Primary Source Items

**Count:** {0} items

These items are notes, attachments, or other non-article types that may need to be:
- Reclassified
- Removed from the primary source dataset
- Kept as supporting materials

""".format(len(issues['non_primary_sources']))

    if issues['non_primary_sources']:
        report += "### Items to Review:\n\n"
        for item in issues['non_primary_sources'][:20]:
            report += f"- Key: `{item['key']}`, Type: **{item['itemType']}**, Title: \"{item['title']}\"\n"

        if len(issues['non_primary_sources']) > 20:
            report += f"\n*...and {len(issues['non_primary_sources']) - 20} more*\n"

    report += """

---

## 3. Items with Multiple Attachments

**Count:** {0} items

These items have multiple child items (attachments). This may indicate:
- Multiple sources combined in one entry (need splitting)
- Multiple pages/images of same source (legitimate)
- Supplementary materials (legitimate)

### Action Required

**HIGH PRIORITY:** Review these items to determine if they contain multiple distinct primary sources that should be separated into individual entries.

""".format(len(issues['multiple_attachments']))

    if issues['multiple_attachments']:
        report += "### Items to Review:\n\n"
        report += "| Item Key | Title | # Attachments |\n"
        report += "|----------|-------|---------------|\n"

        for item in sorted(issues['multiple_attachments'], key=lambda x: x['num_attachments'], reverse=True)[:30]:
            report += f"| `{item['key']}` | {item['title'][:60]}{'...' if len(item['title']) > 60 else ''} | {item['num_attachments']} |\n"

        if len(issues['multiple_attachments']) > 30:
            report += f"\n*...and {len(issues['multiple_attachments']) - 30} more*\n"

    report += """

---

## 4. Items without Attachments

**Count:** {0} items

These items have no PDF or other attachments. This may indicate:
- Missing files that need to be uploaded
- Items created as placeholders
- Items where text was entered directly (check notes field)

### Action Required

Review these items to determine if:
1. PDFs need to be attached
2. Text was extracted to notes (if so, verify)
3. Items should be removed

""".format(len(issues['no_attachments']))

    if issues['no_attachments'] and len(issues['no_attachments']) <= 50:
        report += "### Items to Review:\n\n"
        for item in issues['no_attachments'][:50]:
            report += f"- Key: `{item['key']}`, Title: \"{item['title']}\"\n"
    elif issues['no_attachments']:
        report += f"**Note:** Too many items to list individually ({len(issues['no_attachments'])} items). See data export for full list.\n"

    report += """

---

## 5. Summary and Priorities

### Immediate Actions Required

1. **⚠️ HIGH:** Review items with multiple attachments - may need splitting
2. **⚠️ HIGH:** Check duplicate items - merge or differentiate
3. **MEDIUM:** Verify items without attachments have text in notes
4. **LOW:** Reclassify non-primary source items if needed

### Data Export

Detailed lists of all items with issues have been saved to:
- `data/quality_duplicates.csv`
- `data/quality_multiple_attachments.csv`
- `data/quality_no_attachments.csv`
- `data/quality_non_primary_sources.csv`

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Saved data quality report")

    # Save CSV exports
    for issue_type, items in issues.items():
        if items:
            df = pd.DataFrame(items)
            csv_file = config.DATA_DIR / f'quality_{issue_type}.csv'
            df.to_csv(csv_file, index=False)
            print(f"  Exported {len(items)} {issue_type} to CSV")

def main():
    """Main execution function"""
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - TAG ANALYSIS")
    print("Script 02: Analyze tags and identify data quality issues")
    print("="*70)
    print()

    try:
        # Load tag data
        tags, stats = load_tag_data()

        # Analyze tags
        similar_pairs = find_similar_tags(tags, threshold=80)
        hierarchies = detect_hierarchies(tags)
        cooccurrence_list = calculate_cooccurrence(tags)

        # Save tag analysis
        save_similar_tags(similar_pairs)
        save_cooccurrence(cooccurrence_list)
        visualize_cooccurrence(cooccurrence_list, tags, top_n=30)
        generate_analysis_report(similar_pairs, hierarchies, cooccurrence_list, stats)

        # Connect to Zotero for quality analysis
        print("\n" + "="*70)
        print("DATA QUALITY ANALYSIS")
        print("="*70)
        zot = zotero.Zotero(
            config.ZOTERO_GROUP_ID,
            config.ZOTERO_LIBRARY_TYPE,
            config.ZOTERO_API_KEY
        )

        # Analyze data quality
        issues = analyze_data_quality(zot)
        generate_quality_report(issues)

        print("\n" + "="*70)
        print("✓ ANALYSIS COMPLETE")
        print("="*70)
        print("\nOutputs created:")
        print(f"  - {config.DATA_DIR / 'similar_tags.csv'}")
        print(f"  - {config.DATA_DIR / 'tag_network.json'}")
        print(f"  - {config.VISUALIZATIONS_DIR / 'tag_cooccurrence.png'}")
        print(f"  - {config.REPORTS_DIR / 'tag_analysis.md'}")
        print(f"  - {config.REPORTS_DIR / 'data_quality_issues.md'}")
        print("\nNext: Review reports and begin tag rationalization planning")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
