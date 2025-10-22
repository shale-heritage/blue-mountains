#!/usr/bin/env python3
"""
Apply Automated Tag Consolidation Decisions

This script applies the 47 high-confidence automated decisions from the triage
analysis to the consolidation decisions file and regenerates all outputs.

Decisions applied:
- 13 false positives → KEEP_SEPARATE
- 34 generic→specific hierarchies → HIERARCHY

Author: Claude Code
Date: 2025-10-19
"""

import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set


def load_triage_decisions() -> Dict[str, List[Dict]]:
    """
    Load the automated decisions from triage report.

    Returns:
        Dictionary with 'false_positives' and 'hierarchies' lists
    """
    decisions = {
        'false_positives': [
            {'tag1': 'Pub', 'tag2': 'Public meeting', 'count1': '3', 'count2': '1'},
            {'tag1': 'Pub', 'tag2': 'Publican', 'count1': '3', 'count2': '1'},
            {'tag1': 'Bank', 'tag2': 'Greenbank family', 'count1': '2', 'count2': '4'},
            {'tag1': 'Band', 'tag2': 'Mr William Husband', 'count1': '8', 'count2': '2'},
            {'tag1': 'Band', 'tag2': 'Mr Robert J Husband', 'count1': '8', 'count2': '4'},
            {'tag1': 'Football', 'tag2': 'Ball', 'count1': '6', 'count2': '4'},
            {'tag1': 'Mining', 'tag2': 'Drinking', 'count1': '32', 'count2': '2'},
            {'tag1': 'Horses', 'tag2': 'Boarding houses', 'count1': '19', 'count2': '8'},
            {'tag1': 'Death', 'tag2': 'Debating', 'count1': '53', 'count2': '2'},
            {'tag1': 'Theft', 'tag2': 'Athletics', 'count1': '11', 'count2': '2'},
            {'tag1': 'Weather', 'tag2': 'Death', 'count1': '49', 'count2': '53'},
            {'tag1': 'Dogs', 'tag2': 'Gas', 'count1': '8', 'count2': '2'},
            {'tag1': 'Blackheath', 'tag2': 'Death', 'count1': '22', 'count2': '53'},
        ],
        'hierarchies': [
            {'parent': 'Coal', 'child': 'Gladstone Coal Company', 'count1': '18', 'count2': '2'},
            {'parent': 'Coal', 'child': 'Katoomba Coal and Shale Mines', 'count1': '18', 'count2': '2'},
            {'parent': 'Coal', 'child': 'Katoomba coal mines', 'count1': '18', 'count2': '9'},
            {'parent': 'Coal', 'child': 'Katoomba Coal and Shale Company', 'count1': '18', 'count2': '7'},
            {'parent': 'Cricket', 'child': 'Katoomba Cricket Club', 'count1': '14', 'count2': '2'},
            {'parent': 'Cricket', 'child': 'Megalong Cricket Club', 'count1': '14', 'count2': '2'},
            {'parent': 'Football', 'child': 'Katoomba Football Club', 'count1': '6', 'count2': '3'},
            {'parent': 'Accident', 'child': 'Mining accidents', 'count1': '16', 'count2': '16'},
            {'parent': 'Tennis', 'child': 'Katoomba Tennis Club', 'count1': '3', 'count2': '2'},
            {'parent': 'Mining', 'child': 'Sunny Corner Mining Company', 'count1': '32', 'count2': '2'},
            {'parent': 'Shale mines', 'child': "Nellie's Glen Shale Mine", 'count1': '48', 'count2': '6'},
            {'parent': 'Shale mines', 'child': 'Ruined Castle Shale Mine', 'count1': '48', 'count2': '26'},
            {'parent': 'Shale mines', 'child': 'Katoomba Shale Mine', 'count1': '48', 'count2': '4'},
            {'parent': 'Reserves', 'child': 'South Katoomba Reserve', 'count1': '11', 'count2': '1'},
            {'parent': 'Reserves', 'child': 'Leura Reserve', 'count1': '11', 'count2': '2'},
            {'parent': 'Councils', 'child': 'Lithgow Council', 'count1': '27', 'count2': '2'},
            {'parent': 'Councils', 'child': 'Katoomba Council', 'count1': '27', 'count2': '22'},
            {'parent': 'Hotels', 'child': 'Megalong Hotel', 'count1': '62', 'count2': '9'},
            {'parent': 'Hotels', 'child': 'Mount Victoria Hotel', 'count1': '62', 'count2': '2'},
            {'parent': 'Hotels', 'child': "Mrs Long's Hotel", 'count1': '62', 'count2': '5'},
            {'parent': 'Hotels', 'child': 'Family Hotel', 'count1': '62', 'count2': '3'},
            {'parent': 'Hotels', 'child': 'Belgravia Hotel', 'count1': '62', 'count2': '3'},
            {'parent': 'Hotels', 'child': 'Railway Hotel', 'count1': '62', 'count2': '3'},
            {'parent': 'Hotels', 'child': 'Grand Hotel', 'count1': '62', 'count2': '3'},
            {'parent': 'Hotels', 'child': "Allen's Hotel", 'count1': '62', 'count2': '2'},
            {'parent': 'Hotels', 'child': 'Centennial Hotel', 'count1': '62', 'count2': '5'},
            {'parent': 'Hotels', 'child': "Brown's Hotel", 'count1': '62', 'count2': '2'},
            {'parent': 'Hotels', 'child': 'Katoomba Hotel', 'count1': '62', 'count2': '5'},
            {'parent': 'Hotels', 'child': 'Wentworth Falls Hotel', 'count1': '62', 'count2': '3'},
            {'parent': 'Hotels', 'child': 'Imperial Hotel', 'count1': '62', 'count2': '5'},
            {'parent': 'Hotels', 'child': 'Katoomba Family Hotel', 'count1': '62', 'count2': '2'},
            {'parent': 'Hotels', 'child': "Delaney's Hotel", 'count1': '62', 'count2': '5'},
            {'parent': 'Roads', 'child': "Nellie's Glen Road", 'count1': '15', 'count2': '3'},
            {'parent': 'Roads', 'child': 'Jenolan Caves road', 'count1': '15', 'count2': '2'},
        ]
    }

    return decisions


def generate_updated_decisions(
    existing_merge: List[Dict],
    existing_hierarchy: List[Dict],
    existing_keep: List[Dict],
    new_false_positives: List[Dict],
    new_hierarchies: List[Dict],
    remaining_flagged: List[Dict]
) -> str:
    """
    Generate updated consolidation decisions file content.

    Args:
        existing_merge: Current MERGE decisions
        existing_hierarchy: Current HIERARCHY decisions
        existing_keep: Current KEEP_SEPARATE decisions
        new_false_positives: New false positives to add to KEEP_SEPARATE
        new_hierarchies: New hierarchies to add
        remaining_flagged: Remaining flagged pairs

    Returns:
        Markdown content for updated decisions file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Combine keep separate lists
    all_keep = existing_keep + new_false_positives
    all_hierarchy = existing_hierarchy + new_hierarchies

    # Calculate totals
    total_pairs = len(existing_merge) + len(all_hierarchy) + len(all_keep) + len(remaining_flagged)

    content = f"""# Phase 1.2.1: Tag Consolidation Decisions

**Date generated:** {timestamp}
**Total pairs reviewed:** {total_pairs}
**Method:** Semi-automated pattern matching + manual review

---

## MERGE Decisions (Typos and Variants)

**Count:** {len(existing_merge)} pairs

| Tag 1 | Tag 2 | Count 1 | Count 2 | Canonical Form | Rationale |
|-------|-------|---------|---------|----------------|-----------|
"""

    for pair in existing_merge:
        content += f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | **{pair['canonical']}** | {pair['rationale']} |\n"

    content += f"""
---

## HIERARCHY Decisions (Parent-Child Relationships)

**Count:** {len(all_hierarchy)} pairs

Apply multi-tagging: items get BOTH parent and child tags.

| Parent Tag | Child Tag | Count 1 | Count 2 | Rationale |
|------------|-----------|---------|---------|-----------|
"""

    for pair in all_hierarchy:
        content += f"| **{pair['parent']}** | {pair['child']} | {pair['count1']} | {pair['count2']} | {pair['rationale']} |\n"

    content += f"""
---

## KEEP SEPARATE Decisions (Distinct Concepts)

**Count:** {len(all_keep)} pairs

No action required - tags remain distinct.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Rationale |
|-------|-------|---------|---------|-----------|
"""

    for pair in all_keep:
        content += f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {pair['rationale']} |\n"

    content += f"""
---

## FLAGGED FOR REVIEW (Manual Decision Required)

**Count:** {len(remaining_flagged)} pairs

**ACTION REQUIRED:** Historian review needed for these ambiguous cases.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Similarity | Reason |
|-------|-------|---------|---------|------------|--------|
"""

    for pair in remaining_flagged:
        content += f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {pair['similarity']} | {pair['reason']} |\n"

    content += "\n"

    return content


def generate_consolidation_map(
    merge_pairs: List[Dict],
    hierarchy_pairs: List[Dict],
    keep_pairs: List[Dict]
) -> List[Dict]:
    """
    Generate consolidation map CSV data.

    Args:
        merge_pairs: MERGE decisions
        hierarchy_pairs: HIERARCHY decisions
        keep_pairs: KEEP_SEPARATE decisions

    Returns:
        List of dictionaries for CSV writing
    """
    rows = []

    # Add merge rows
    for pair in merge_pairs:
        rows.append({
            'old_tag': pair['tag2'],
            'new_tag': pair['canonical'],
            'action': 'merge',
            'notes': pair['rationale']
        })

    # Add hierarchy rows (child tag gets parent added)
    for pair in hierarchy_pairs:
        rows.append({
            'old_tag': pair['child'],
            'new_tag': pair['child'],
            'action': 'hierarchy',
            'notes': f"parent={pair['parent']}"
        })

    # Add keep separate rows
    for pair in keep_pairs:
        rows.append({
            'old_tag': pair['tag1'],
            'new_tag': pair['tag1'],
            'action': 'keep',
            'notes': pair['rationale']
        })
        # Add second tag if different
        if pair['tag1'] != pair['tag2']:
            rows.append({
                'old_tag': pair['tag2'],
                'new_tag': pair['tag2'],
                'action': 'keep',
                'notes': pair['rationale']
            })

    return rows


def main():
    """Main execution function."""
    base_dir = Path(__file__).parent.parent
    decisions_file = base_dir / "planning/phase1.2.1-consolidation-decisions.md"
    map_file = base_dir / "data/tag_consolidation_map.csv"
    preview_file = base_dir / "reports/consolidation_preview.md"

    print("Applying Automated Tag Consolidation Decisions")
    print("=" * 60)
    print()

    # Load triage decisions
    print("Loading automated decisions from triage analysis...")
    triage = load_triage_decisions()
    print(f"✓ Loaded {len(triage['false_positives'])} false positive decisions")
    print(f"✓ Loaded {len(triage['hierarchies'])} hierarchy decisions")
    print()

    # Read existing decisions file to extract current decisions
    print("Reading existing consolidation decisions...")

    existing_merge = []
    existing_hierarchy = []
    existing_keep = []
    remaining_flagged = []

    # Create sets of pairs we're applying decisions for
    false_positive_pairs = {(p['tag1'], p['tag2']) for p in triage['false_positives']}
    false_positive_pairs.update({(p['tag2'], p['tag1']) for p in triage['false_positives']})

    hierarchy_pairs = {(p['parent'], p['child']) for p in triage['hierarchies']}
    hierarchy_pairs.update({(p['child'], p['parent']) for p in triage['hierarchies']})

    with open(decisions_file, 'r', encoding='utf-8') as f:
        current_section = None
        for line in f:
            if '## MERGE Decisions' in line:
                current_section = 'merge'
                continue
            elif '## HIERARCHY Decisions' in line:
                current_section = 'hierarchy'
                continue
            elif '## KEEP SEPARATE Decisions' in line:
                current_section = 'keep'
                continue
            elif '## FLAGGED FOR REVIEW' in line:
                current_section = 'flagged'
                continue

            # Parse table rows
            if current_section and line.startswith('| ') and not line.startswith('| Tag') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]

                if current_section == 'merge' and len(parts) >= 5:
                    existing_merge.append({
                        'tag1': parts[0],
                        'tag2': parts[1],
                        'count1': parts[2],
                        'count2': parts[3],
                        'canonical': parts[4].replace('**', ''),
                        'rationale': parts[5] if len(parts) > 5 else ''
                    })

                elif current_section == 'hierarchy' and len(parts) >= 4:
                    existing_hierarchy.append({
                        'parent': parts[0].replace('**', ''),
                        'child': parts[1],
                        'count1': parts[2],
                        'count2': parts[3],
                        'rationale': parts[4] if len(parts) > 4 else ''
                    })

                elif current_section == 'keep' and len(parts) >= 4:
                    existing_keep.append({
                        'tag1': parts[0],
                        'tag2': parts[1],
                        'count1': parts[2],
                        'count2': parts[3],
                        'rationale': parts[4] if len(parts) > 4 else ''
                    })

                elif current_section == 'flagged' and len(parts) >= 5:
                    pair_key = (parts[0], parts[1])
                    # Only keep if NOT in our automated decisions
                    if pair_key not in false_positive_pairs and pair_key not in hierarchy_pairs:
                        remaining_flagged.append({
                            'tag1': parts[0],
                            'tag2': parts[1],
                            'count1': parts[2],
                            'count2': parts[3],
                            'similarity': parts[4] if len(parts) > 4 else '',
                            'reason': parts[5] if len(parts) > 5 else 'Requires manual review'
                        })

    print(f"✓ Existing MERGE: {len(existing_merge)} pairs")
    print(f"✓ Existing HIERARCHY: {len(existing_hierarchy)} pairs")
    print(f"✓ Existing KEEP_SEPARATE: {len(existing_keep)} pairs")
    print(f"✓ Remaining FLAGGED: {len(remaining_flagged)} pairs (97 expected)")
    print()

    # Convert triage decisions to proper format
    print("Formatting new decisions...")

    new_false_positives = []
    for fp in triage['false_positives']:
        new_false_positives.append({
            'tag1': fp['tag1'],
            'tag2': fp['tag2'],
            'count1': fp['count1'],
            'count2': fp['count2'],
            'rationale': 'Substring coincidence - semantically unrelated concepts (automated triage)'
        })

    new_hierarchies = []
    for hier in triage['hierarchies']:
        # Determine rationale based on parent type
        if hier['parent'] in ['Hotels', 'Councils', 'Reserves', 'Roads']:
            rationale = f"Generic type '{hier['parent']}' → specific instance '{hier['child']}' (automated triage)"
        elif hier['parent'] in ['Cricket', 'Football', 'Tennis', 'Athletics', 'Mining', 'Tourism']:
            rationale = f"Generic activity '{hier['parent']}' → specific instance '{hier['child']}' (automated triage)"
        elif hier['parent'] in ['Coal', 'Shale mines']:
            rationale = f"Generic resource '{hier['parent']}' → specific instance '{hier['child']}' (automated triage)"
        else:
            rationale = f"Generic concept '{hier['parent']}' → specific instance '{hier['child']}' (automated triage)"

        new_hierarchies.append({
            'parent': hier['parent'],
            'child': hier['child'],
            'count1': hier['count1'],
            'count2': hier['count2'],
            'rationale': rationale
        })

    print(f"✓ Formatted {len(new_false_positives)} false positive decisions")
    print(f"✓ Formatted {len(new_hierarchies)} hierarchy decisions")
    print()

    # Generate updated decisions file
    print("Generating updated consolidation decisions file...")
    updated_content = generate_updated_decisions(
        existing_merge,
        existing_hierarchy,
        existing_keep,
        new_false_positives,
        new_hierarchies,
        remaining_flagged
    )

    with open(decisions_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"✓ Updated: {decisions_file}")
    print()

    # Generate consolidation map
    print("Generating consolidation map CSV...")
    map_data = generate_consolidation_map(
        existing_merge,
        existing_hierarchy + new_hierarchies,
        existing_keep + new_false_positives
    )

    with open(map_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action', 'notes'])
        writer.writeheader()
        writer.writerows(map_data)

    print(f"✓ Updated: {map_file} ({len(map_data)} rows)")
    print()

    # Generate preview
    print("Generating consolidation preview...")

    total_merges = len(existing_merge)
    total_hierarchies = len(existing_hierarchy) + len(new_hierarchies)
    total_flagged = len(remaining_flagged)

    preview_content = f"""# Tag Consolidation Preview

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Impact Summary

- **Tags to be merged:** {total_merges} pairs
- **Hierarchies to establish:** {total_hierarchies} pairs
- **Tags requiring review:** {total_flagged} pairs

---

## Recent Additions (Automated Triage)

### New False Positives (KEEP_SEPARATE)

Count: {len(new_false_positives)}

"""

    for fp in new_false_positives[:5]:
        preview_content += f"- `{fp['tag1']}` vs `{fp['tag2']}` (usage: {fp['count1']} vs {fp['count2']}) - Substring coincidence\n"

    if len(new_false_positives) > 5:
        preview_content += f"\n...and {len(new_false_positives) - 5} more\n"

    preview_content += f"""
### New Hierarchies

Count: {len(new_hierarchies)}

"""

    for hier in new_hierarchies[:10]:
        preview_content += f"- `{hier['parent']}` ← `{hier['child']}` (usage: {hier['count1']} vs {hier['count2']})\n"

    if len(new_hierarchies) > 10:
        preview_content += f"\n...and {len(new_hierarchies) - 10} more\n"

    preview_content += f"""
---

## Example Transformations

### Merge Examples

"""
    for merge in existing_merge:
        preview_content += f"1. `{merge['tag2']}` → `{merge['canonical']}` (usage: {merge['count2']} → {merge['count1']})\n"

    preview_content += f"""
### Hierarchy Examples

"""
    # Show first 10 hierarchies
    for i, hier in enumerate((existing_hierarchy + new_hierarchies)[:10], 1):
        preview_content += f"{i}. `{hier['parent']}` ← `{hier['child']}` (multi-tag: both applied)\n"

    if total_hierarchies > 10:
        preview_content += f"\n...and {total_hierarchies - 10} more\n"

    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(preview_content)

    print(f"✓ Updated: {preview_file}")
    print()

    # Summary
    print("=" * 60)
    print("Summary of Changes")
    print("=" * 60)
    print()
    print(f"Applied decisions:        47 pairs")
    print(f"  - False positives:      {len(new_false_positives)}")
    print(f"  - Hierarchies:          {len(new_hierarchies)}")
    print()
    print(f"Current status:")
    print(f"  - MERGE:                {total_merges} pairs")
    print(f"  - HIERARCHY:            {total_hierarchies} pairs")
    print(f"  - KEEP_SEPARATE:        {len(existing_keep) + len(new_false_positives)} pairs")
    print(f"  - FLAGGED (remaining):  {total_flagged} pairs")
    print()
    print("Next step: Review remaining flagged pairs with historian expertise")
    print()


if __name__ == "__main__":
    main()
