#!/usr/bin/env python3
"""
Blue Mountains Project - Automated Tag Categorization
======================================================

Purpose:
    Semi-automated tool to categorize 332 similar tag pairs into decision
    categories (MERGE, HIERARCHY, KEEP SEPARATE, FLAG FOR REVIEW).

    Uses pattern matching to automatically handle 60-70% of clear-cut cases,
    leaving only ambiguous cases for human review. Implements the 80% solution
    approach for efficient tag rationalization.

Input:
    - data/similar_tags.csv (332 pairs from 02_analyze_tags.py)
    - docs/folksonomy_logic.md (decision framework and principles)

Outputs:
    - planning/phase1.2.1-consolidation-decisions.md (decision log with rationale)
    - data/tag_consolidation_map.csv (machine-readable transformation rules)
    - reports/consolidation_preview.md (before/after comparison)

Decision Categories:
    - MERGE: Typos, spelling, capitalization variants
    - HIERARCHY: Geographic/institution parent-child relationships
    - KEEP_SEPARATE: Distinct concepts (especially person names)
    - FLAG_REVIEW: Ambiguous cases requiring historian input

Pattern-Based Detection:
    - Typos: Levenshtein distance < 2, length difference <= 1
    - Geographic: "Place → Place + Institution" pattern
    - Institution: "Type → Type + Modifier" pattern
    - Person names: Contains Mr/Mrs/Miss/Dr → default keep separate
    - Court hierarchy: Pre-decided in folksonomy_logic.md

Author: Shawn Ross (with Claude Code assistance)
Project: ARC Linkage Project LP190100900
Created: 2025-10-19
"""

import csv
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add project root to path for config import
import sys
sys.path.append(str(Path(__file__).parent))
import config

# ==============================================================================
# Pattern Recognition Functions
# ==============================================================================

def is_typo_variant(tag1: str, tag2: str, count1: int, count2: int) -> bool:
    """
    Detect if tag2 is a typo of tag1 based on similarity and usage.

    Criteria:
    - Very similar strings (differ by 1-2 characters)
    - Length difference <= 1
    - One tag used much more frequently (suggests typo)
    - NOT person names (preserve all person names separately)

    Args:
        tag1: First tag name
        tag2: Second tag name
        count1: Usage count of tag1
        count2: Usage count of tag2

    Returns:
        True if likely a typo relationship
    """
    from Levenshtein import distance

    # NEVER merge person names - they could be different people (brothers, father-son, etc.)
    if is_person_name(tag1) or is_person_name(tag2):
        return False

    # Calculate edit distance
    lev_dist = distance(tag1.lower(), tag2.lower())

    # Length difference
    len_diff = abs(len(tag1) - len(tag2))

    # Usage ratio (tag with higher count is likely correct)
    if count1 == 0 or count2 == 0:
        return False

    usage_ratio = max(count1, count2) / min(count1, count2)

    # Typo if: very close strings, small length diff, and one much more common
    return lev_dist <= 2 and len_diff <= 1 and usage_ratio >= 3


def is_capitalization_variant(tag1: str, tag2: str) -> bool:
    """
    Check if tags differ only in capitalization.

    Examples: "Bottle" vs "bottle", "Building material" vs "Building Material"
    """
    return tag1.lower() == tag2.lower() and tag1 != tag2


def is_hyphenation_variant(tag1: str, tag2: str) -> bool:
    """
    Check if tags differ only in hyphenation.

    Examples: "Building-material" vs "Building material"
    """
    # Remove hyphens and compare
    tag1_normalized = tag1.replace('-', ' ').replace('_', ' ')
    tag2_normalized = tag2.replace('-', ' ').replace('_', ' ')

    return tag1_normalized.lower() == tag2_normalized.lower() and tag1 != tag2


def is_geographic_hierarchy(tag1: str, tag2: str) -> bool:
    """
    Detect geographic hierarchy: "Place → Place + Specific Location".

    Examples:
    - "Katoomba" → "Katoomba Hotel"
    - "Megalong Valley" → "Megalong Valley School"
    - "Nellie's Glen" → "Nellie's Glen Shale Mine"

    Pattern: tag2 starts with tag1 and adds a specific location/institution
    """
    # Case-insensitive containment check
    return tag2.lower().startswith(tag1.lower() + ' ') and tag1.lower() != tag2.lower()


def is_institution_hierarchy(tag1: str, tag2: str) -> bool:
    """
    Detect institution hierarchy: "Type → Specific Instance".

    Examples:
    - "Church" → "Congregational Church"
    - "Hotel" → "Imperial Hotel"
    - "School" → "Katoomba Public School"

    Pattern: tag2 ends with tag1 (institution type is suffix)
    """
    # Institution type usually appears as suffix
    return tag2.lower().endswith(' ' + tag1.lower()) and tag1.lower() != tag2.lower()


def is_person_name(tag: str) -> bool:
    """
    Detect if tag is a person name (contains honorific).

    Honorifics: Mr, Mrs, Miss, Ms, Dr, Reverend, Rev, Professor, Prof

    Person names should default to KEEP SEPARATE unless verified as same person.
    """
    honorifics = ['mr ', 'mrs ', 'miss ', 'ms ', 'dr ', 'reverend ', 'rev ',
                  'professor ', 'prof ']

    tag_lower = tag.lower()

    # Check for honorific at start or after space (for "The Reverend X" patterns)
    for honorific in honorifics:
        if tag_lower.startswith(honorific) or f' {honorific}' in tag_lower:
            return True

    return False


def is_court_tag(tag: str) -> bool:
    """
    Check if tag is part of the court hierarchy (pre-decided).

    Court hierarchy (from folksonomy_logic.md:458-493):
    - Court (parent)
    - Court cases, Courthouse (sub-tags)
    - Supreme Court, Police court, Licensing Court (court types)
    - Katoomba Court (specific building)
    """
    court_tags = ['court', 'court cases', 'courthouse', 'supreme court',
                  'police court', 'licensing court', 'katoomba court']

    return tag.lower() in court_tags


# ==============================================================================
# Tag Pair Categorization
# ==============================================================================

def categorize_tag_pair(tag1: str, tag2: str, count1: int, count2: int,
                        similarity: float) -> Tuple[str, str, str]:
    """
    Categorize a tag pair into decision category with rationale.

    Args:
        tag1: First tag name
        tag2: Second tag name
        count1: Usage count of tag1
        count2: Usage count of tag2
        similarity: Similarity score (0-100)

    Returns:
        Tuple of (decision, canonical_tag, rationale)

    Decision types:
        - MERGE: Consolidate to single tag
        - HIERARCHY: Parent-child relationship (keep both, apply multi-tagging)
        - KEEP_SEPARATE: Distinct concepts
        - FLAG_REVIEW: Uncertain, needs historian input
    """
    # Court hierarchy (pre-decided in folksonomy_logic.md)
    if is_court_tag(tag1) or is_court_tag(tag2):
        # All court tags maintain hierarchy
        if 'court' in tag1.lower() and 'court' in tag2.lower():
            parent = 'Court' if tag1.lower() == 'court' else tag1
            return ('HIERARCHY', parent, 'Court hierarchy (pre-decided in folksonomy_logic.md lines 458-493)')

    # MERGE Category: Typos and variants
    if is_typo_variant(tag1, tag2, count1, count2):
        canonical = tag1 if count1 >= count2 else tag2
        return ('MERGE', canonical, f'Typo variant (edit distance ≤2, usage ratio {max(count1,count2)}/{min(count1,count2)})')

    if is_capitalization_variant(tag1, tag2):
        # Prefer more frequent capitalization, or sentence case if tied
        if count1 > count2:
            return ('MERGE', tag1, 'Capitalization variant (using more frequent form)')
        elif count2 > count1:
            return ('MERGE', tag2, 'Capitalization variant (using more frequent form)')
        else:
            # Prefer sentence case (first letter capital, rest lowercase unless proper noun)
            canonical = tag1 if tag1[0].isupper() and not tag1.isupper() else tag2
            return ('MERGE', canonical, 'Capitalization variant (standardizing to sentence case)')

    if is_hyphenation_variant(tag1, tag2):
        canonical = tag1 if count1 >= count2 else tag2
        return ('MERGE', canonical, 'Hyphenation variant (using more frequent form)')

    # KEEP_SEPARATE Category: Person names (default)
    if is_person_name(tag1) and is_person_name(tag2):
        return ('KEEP_SEPARATE', '',
                'Person names - likely different individuals (preserve granularity per folksonomy_logic.md:517-522)')

    # HIERARCHY Category: Geographic relationships
    if is_geographic_hierarchy(tag1, tag2):
        return ('HIERARCHY', tag1,
                f'Geographic hierarchy: "{tag1}" (parent) → "{tag2}" (specific location)')

    if is_geographic_hierarchy(tag2, tag1):
        return ('HIERARCHY', tag2,
                f'Geographic hierarchy: "{tag2}" (parent) → "{tag1}" (specific location)')

    # HIERARCHY Category: Institution relationships
    if is_institution_hierarchy(tag1, tag2):
        return ('HIERARCHY', tag1,
                f'Institution hierarchy: "{tag1}" (type) → "{tag2}" (specific instance)')

    if is_institution_hierarchy(tag2, tag1):
        return ('HIERARCHY', tag2,
                f'Institution hierarchy: "{tag2}" (type) → "{tag1}" (specific instance)')

    # FLAG_REVIEW: Ambiguous cases
    # High similarity but doesn't match clear patterns
    if similarity >= 95:
        return ('FLAG_REVIEW', '',
                f'High similarity ({similarity}%) but unclear relationship - requires historian review')

    # Related but distinct concepts
    if similarity >= 80 and similarity < 95:
        return ('FLAG_REVIEW', '',
                f'Moderate similarity ({similarity}%) - may be related concepts or false positive')

    # Default: Flag for review
    return ('FLAG_REVIEW', '',
            'Uncertain relationship - manual review recommended')


# ==============================================================================
# Main Processing
# ==============================================================================

def main():
    """
    Main workflow:
    1. Load similar_tags.csv
    2. Categorize each pair using pattern matching
    3. Generate decision log (Markdown)
    4. Generate consolidation map (CSV)
    5. Generate preview report (Markdown)
    """
    print('=' * 70)
    print('BLUE MOUNTAINS PROJECT - AUTOMATED TAG CATEGORIZATION')
    print('Script 04: Semi-automated tag pair decision making')
    print('=' * 70)
    print()

    # Load similar tags CSV
    similar_tags_path = config.DATA_DIR / 'similar_tags.csv'

    print(f'Loading similar tags from {similar_tags_path}...')

    tag_pairs = []
    with open(similar_tags_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag_pairs.append(row)

    print(f'✓ Loaded {len(tag_pairs)} tag pairs')
    print()

    # Categorize all pairs
    print('Categorizing tag pairs using pattern matching...')

    decisions = {
        'MERGE': [],
        'HIERARCHY': [],
        'KEEP_SEPARATE': [],
        'FLAG_REVIEW': []
    }

    for row in tag_pairs:
        tag1 = row['tag1']
        tag2 = row['tag2']
        count1 = int(row['count1'])
        count2 = int(row['count2'])
        similarity = float(row['similarity'])

        decision, canonical, rationale = categorize_tag_pair(
            tag1, tag2, count1, count2, similarity
        )

        decisions[decision].append({
            'tag1': tag1,
            'tag2': tag2,
            'count1': count1,
            'count2': count2,
            'similarity': similarity,
            'canonical': canonical,
            'rationale': rationale
        })

    # Print summary
    print(f'✓ Categorization complete')
    print()
    print('Decision Summary:')
    print(f'  MERGE: {len(decisions["MERGE"])} pairs (typos, variants)')
    print(f'  HIERARCHY: {len(decisions["HIERARCHY"])} pairs (parent-child)')
    print(f'  KEEP_SEPARATE: {len(decisions["KEEP_SEPARATE"])} pairs (distinct concepts)')
    print(f'  FLAG_REVIEW: {len(decisions["FLAG_REVIEW"])} pairs (needs historian review)')
    print()

    auto_decided = len(decisions['MERGE']) + len(decisions['HIERARCHY']) + len(decisions['KEEP_SEPARATE'])
    manual_review = len(decisions['FLAG_REVIEW'])

    print(f'Automated decisions: {auto_decided} ({auto_decided/len(tag_pairs)*100:.1f}%)')
    print(f'Manual review needed: {manual_review} ({manual_review/len(tag_pairs)*100:.1f}%)')
    print()

    # Generate outputs
    generate_decision_log(decisions)
    generate_consolidation_map(decisions)
    generate_preview_report(decisions)

    print('=' * 70)
    print('✓ AUTOMATED CATEGORIZATION COMPLETE')
    print('=' * 70)
    print()
    print('Next steps:')
    print('  1. Review planning/phase1.2.1-consolidation-decisions.md')
    print('  2. Review flagged cases requiring historian input')
    print('  3. Apply consolidation map to Zotero (Phase 1.4)')
    print()


def generate_decision_log(decisions: Dict[str, List[Dict]]):
    """Generate Markdown decision log with rationale."""
    output_path = config.PROJECT_ROOT / 'planning' / 'phase1.2.1-consolidation-decisions.md'

    print(f'Generating decision log at {output_path}...')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('# Phase 1.2.1: Tag Consolidation Decisions\n\n')
        f.write(f'**Date generated:** {timestamp}\n')
        f.write(f'**Total pairs reviewed:** {sum(len(v) for v in decisions.values())}\n')
        f.write('**Method:** Semi-automated pattern matching + manual review\n\n')
        f.write('---\n\n')

        # Merge decisions
        f.write('## MERGE Decisions (Typos and Variants)\n\n')
        f.write(f'**Count:** {len(decisions["MERGE"])} pairs\n\n')
        f.write('| Tag 1 | Tag 2 | Count 1 | Count 2 | Canonical Form | Rationale |\n')
        f.write('|-------|-------|---------|---------|----------------|-----------||\n')

        for d in sorted(decisions['MERGE'], key=lambda x: -x['count1']):
            f.write(f"| {d['tag1']} | {d['tag2']} | {d['count1']} | {d['count2']} | "
                   f"**{d['canonical']}** | {d['rationale']} |\n")

        f.write('\n---\n\n')

        # Hierarchy decisions
        f.write('## HIERARCHY Decisions (Parent-Child Relationships)\n\n')
        f.write(f'**Count:** {len(decisions["HIERARCHY"])} pairs\n\n')
        f.write('Apply multi-tagging: items get BOTH parent and child tags.\n\n')
        f.write('| Parent Tag | Child Tag | Count 1 | Count 2 | Rationale |\n')
        f.write('|------------|-----------|---------|---------|-----------||\n')

        for d in sorted(decisions['HIERARCHY'], key=lambda x: -x['count1']):
            f.write(f"| **{d['canonical']}** | {d['tag2'] if d['tag1'] == d['canonical'] else d['tag1']} | "
                   f"{d['count1']} | {d['count2']} | {d['rationale']} |\n")

        f.write('\n---\n\n')

        # Keep separate decisions
        f.write('## KEEP SEPARATE Decisions (Distinct Concepts)\n\n')
        f.write(f'**Count:** {len(decisions["KEEP_SEPARATE"])} pairs\n\n')
        f.write('No action required - tags remain distinct.\n\n')
        f.write('| Tag 1 | Tag 2 | Count 1 | Count 2 | Rationale |\n')
        f.write('|-------|-------|---------|---------|-----------||\n')

        for d in sorted(decisions['KEEP_SEPARATE'], key=lambda x: -x['count1']):
            f.write(f"| {d['tag1']} | {d['tag2']} | {d['count1']} | {d['count2']} | {d['rationale']} |\n")

        f.write('\n---\n\n')

        # Flagged for review
        f.write('## FLAGGED FOR REVIEW (Manual Decision Required)\n\n')
        f.write(f'**Count:** {len(decisions["FLAG_REVIEW"])} pairs\n\n')
        f.write('**ACTION REQUIRED:** Historian review needed for these ambiguous cases.\n\n')
        f.write('| Tag 1 | Tag 2 | Count 1 | Count 2 | Similarity | Reason |\n')
        f.write('|-------|-------|---------|---------|------------|--------||\n')

        for d in sorted(decisions['FLAG_REVIEW'], key=lambda x: -x['similarity']):
            f.write(f"| {d['tag1']} | {d['tag2']} | {d['count1']} | {d['count2']} | "
                   f"{d['similarity']:.1f}% | {d['rationale']} |\n")

    print(f'✓ Saved decision log')


def generate_consolidation_map(decisions: Dict[str, List[Dict]]):
    """Generate CSV consolidation map for batch processing."""
    output_path = config.DATA_DIR / 'tag_consolidation_map.csv'

    print(f'Generating consolidation map at {output_path}...')

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['old_tag', 'new_tag', 'action', 'notes'])

        # Merge actions
        for d in decisions['MERGE']:
            # Merge tag with lower count into tag with higher count
            old_tag = d['tag2'] if d['tag1'] == d['canonical'] else d['tag1']
            new_tag = d['canonical']
            writer.writerow([old_tag, new_tag, 'merge', d['rationale']])

        # Hierarchy actions
        for d in decisions['HIERARCHY']:
            # Record parent-child relationship
            parent = d['canonical']
            child = d['tag2'] if d['tag1'] == parent else d['tag1']
            writer.writerow([child, parent, 'hierarchy', f'parent={parent}'])

        # Keep separate (for completeness)
        for d in decisions['KEEP_SEPARATE']:
            writer.writerow([d['tag1'], d['tag1'], 'keep', d['rationale']])
            writer.writerow([d['tag2'], d['tag2'], 'keep', d['rationale']])

        # Flagged (no action yet)
        for d in decisions['FLAG_REVIEW']:
            writer.writerow([d['tag1'], '', 'review', d['rationale']])
            writer.writerow([d['tag2'], '', 'review', d['rationale']])

    print(f'✓ Saved consolidation map')


def generate_preview_report(decisions: Dict[str, List[Dict]]):
    """Generate Markdown preview of before/after tag changes."""
    output_path = config.REPORTS_DIR / 'consolidation_preview.md'

    print(f'Generating preview report at {output_path}...')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('# Tag Consolidation Preview\n\n')
        f.write(f'**Generated:** {timestamp}\n\n')
        f.write('---\n\n')

        f.write('## Impact Summary\n\n')

        # Calculate statistics
        merge_count = len(decisions['MERGE'])
        hierarchy_count = len(decisions['HIERARCHY'])

        f.write(f'- **Tags to be merged:** {merge_count} pairs\n')
        f.write(f'- **Hierarchies to establish:** {hierarchy_count} pairs\n')
        f.write(f'- **Tags requiring review:** {len(decisions["FLAG_REVIEW"])} pairs\n')
        f.write('\n---\n\n')

        f.write('## Example Transformations\n\n')

        f.write('### Merge Examples\n\n')
        for i, d in enumerate(decisions['MERGE'][:10], 1):
            old = d['tag2'] if d['tag1'] == d['canonical'] else d['tag1']
            new = d['canonical']
            f.write(f"{i}. `{old}` → `{new}` (usage: {d['count2'] if d['tag1'] == d['canonical'] else d['count1']} → {d['count1'] if d['tag1'] == d['canonical'] else d['count2']})\n")

        if len(decisions['MERGE']) > 10:
            f.write(f'\n...and {len(decisions["MERGE"]) - 10} more\n')

        f.write('\n### Hierarchy Examples\n\n')
        for i, d in enumerate(decisions['HIERARCHY'][:10], 1):
            parent = d['canonical']
            child = d['tag2'] if d['tag1'] == parent else d['tag1']
            f.write(f"{i}. `{parent}` ← `{child}` (multi-tag: both applied)\n")

        if len(decisions['HIERARCHY']) > 10:
            f.write(f'\n...and {len(decisions["HIERARCHY"]) - 10} more\n')

    print(f'✓ Saved preview report')


if __name__ == '__main__':
    main()
