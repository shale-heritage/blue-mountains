#!/usr/bin/env python3
"""
Tag Consolidation Triage: Review Flagged Pairs

This script categorizes the 144 flagged tag pairs from automated analysis into
decision groups, making it easier to batch-review and approve similar patterns.

Categories:
- FALSE_POSITIVE: Substring coincidence, semantically unrelated
- HIERARCHY: Generic → Specific instance (should multi-tag)
- NAMING_VARIANT: Likely same entity with different names (needs investigation)
- CONTEXTUAL: Requires examining actual Zotero items to decide

Author: Claude Code
Date: 2025-10-19
"""

import csv
import re
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime


def is_substring_coincidence(tag1: str, tag2: str) -> bool:
    """
    Detect if similarity is just substring coincidence, not semantic relationship.

    Examples of false positives:
    - "Bank" vs "Greenbank family" (surname contains "bank")
    - "Band" vs "Husband family" (surname contains "band")
    - "Pub" vs "Public meeting" (different concepts despite substring)

    Args:
        tag1: First tag
        tag2: Second tag

    Returns:
        True if likely a false positive substring match
    """
    # Convert to lowercase for comparison
    t1_lower = tag1.lower()
    t2_lower = tag2.lower()

    # Pattern: One is a person/family name containing the other word
    # e.g., "Band" in "Husband family", "Bank" in "Greenbank family"
    person_indicators = ['mr ', 'mrs ', 'miss ', 'dr ', 'family']
    if any(ind in t2_lower for ind in person_indicators):
        # If tag1 is a short word that appears in a person/family name
        if len(tag1) <= 5 and tag1.lower() in tag2.lower():
            return True

    # Pattern: Completely different semantic domains
    semantic_pairs = [
        ('pub', 'public meeting'),  # Pub vs public meeting
        ('pub', 'publican'),  # Related but distinct
        ('death', 'debating'),  # Totally different
        ('horses', 'boarding houses'),  # house substring coincidence
        ('miners', 'minister'),  # Different concepts
        ('mining', 'drinking'),  # Different concepts
        ('theft', 'athletics'),  # Different concepts
        ('dogs', 'gas'),  # Different concepts
        ('weather', 'death'),  # Different concepts
        ('blackheath', 'death'),  # Place name contains "heath"
        ('ball', 'football'),  # Ball as event vs football (different)
    ]

    for pair in semantic_pairs:
        if (t1_lower == pair[0] and t2_lower == pair[1]) or \
           (t1_lower == pair[1] and t2_lower == pair[0]):
            return True

    return False


def is_generic_to_specific_hierarchy(tag1: str, tag2: str) -> Tuple[bool, str]:
    """
    Detect if this is a generic → specific instance hierarchy.

    Examples:
    - "Hotels" → "Imperial Hotel" (type → instance)
    - "Councils" → "Katoomba Council" (type → instance)
    - "Cricket clubs" → "Megalong Cricket Club" (type → instance)

    Args:
        tag1: First tag (potentially generic)
        tag2: Second tag (potentially specific)

    Returns:
        Tuple of (is_hierarchy, rationale)
    """
    # Convert to lowercase for comparison
    t1_lower = tag1.lower()
    t2_lower = tag2.lower()

    # Pattern 1: Plural generic → specific instance
    # "Hotels" → "Carrington Hotel"
    # "Councils" → "Katoomba Council"
    # "Reserves" → "Leura Reserve"

    # Check if tag1 is plural and tag2 contains singular form
    plural_to_singular = {
        'hotels': 'hotel',
        'councils': 'council',
        'reserves': 'reserve',
        'clubs': 'club',
        'committees': 'committee',
        'lodges': 'lodge',
        'roads': 'road',
        'mines': 'mine',
    }

    for plural, singular in plural_to_singular.items():
        if t1_lower == plural and singular in t2_lower:
            return (True, f"Generic type '{tag1}' → specific instance '{tag2}'")

    # Pattern 2: Generic activity/concept → specific instance
    # "Cricket" → "Katoomba Cricket Club"
    # "Football" → "Katoomba Football Club"
    # "Tennis" → "Katoomba Tennis Club"
    # "Mining" → "Sunny Corner Mining Company"

    generic_activities = ['cricket', 'football', 'tennis', 'athletics',
                         'mining', 'tourism']

    for activity in generic_activities:
        if t1_lower == activity and activity in t2_lower:
            return (True, f"Generic activity '{tag1}' → specific instance '{tag2}'")

    # Pattern 3: Generic resource → specific type
    # "Shale mines" → "Nellie's Glen Shale Mine"
    # "Coal" → "Coal mine"

    if 'shale mine' in t1_lower and 'shale mine' in t2_lower:
        return (True, f"Generic type '{tag1}' → specific instance '{tag2}'")

    if t1_lower == 'coal' and 'coal' in t2_lower:
        return (True, f"Generic resource '{tag1}' → specific instance '{tag2}'")

    # Pattern 4: Generic role/position → specific instance
    # "Accident" → "Mining accidents"
    # "Miners" → "Miners' families" (related concept)

    if t1_lower == 'accident' and 'accident' in t2_lower:
        return (True, f"Generic concept '{tag1}' → specific type '{tag2}'")

    return (False, "")


def is_naming_variant(tag1: str, tag2: str) -> bool:
    """
    Detect if tags might be naming variants of the same entity.

    Examples that need investigation:
    - "Katoomba South" vs "South Katoomba"
    - "Katoomba coal mines" vs "Katoomba Coal and Shale Company"
    - "Katoomba Superior Public School" vs "Katoomba Public School"

    Args:
        tag1: First tag
        tag2: Second tag

    Returns:
        True if likely naming variants requiring investigation
    """
    t1_lower = tag1.lower()
    t2_lower = tag2.lower()

    # Pattern: Place + cardinal direction variants
    # "Katoomba South" vs "South Katoomba"
    if 'south' in t1_lower and 'south' in t2_lower:
        place1 = t1_lower.replace('south', '').strip()
        place2 = t2_lower.replace('south', '').strip()
        if place1 == place2:
            return True

    # Pattern: Similar organization names (company/mine variants)
    # "Katoomba coal mines" vs "Katoomba Coal and Shale Company"
    # "Katoomba Coal and Shale Mines" vs "Katoomba Coal and Shale Company"
    if 'katoomba' in t1_lower and 'katoomba' in t2_lower:
        if ('coal' in t1_lower and 'coal' in t2_lower) or \
           ('shale' in t1_lower and 'shale' in t2_lower):
            if ('mine' in t1_lower or 'company' in t2_lower) or \
               ('mine' in t2_lower or 'company' in t1_lower):
                return True

    # Pattern: School name variants
    # "Katoomba Superior Public School" vs "Katoomba Public School"
    if 'school' in t1_lower and 'school' in t2_lower:
        # Extract base name
        base1 = t1_lower.replace('superior', '').replace('public', '').replace('school', '').strip()
        base2 = t2_lower.replace('superior', '').replace('public', '').replace('school', '').strip()
        if base1 == base2 and base1:  # Same base location
            return True

    # Pattern: Lodge/organization variants
    # "Druid's Lodge" vs "Lodges", "Odd Fellows' Hall" vs "Oddfellows"
    if ('lodge' in t1_lower or 'lodge' in t2_lower) and \
       ('druid' in t1_lower or 'druid' in t2_lower or \
        'oddfellow' in t1_lower or 'oddfellow' in t2_lower):
        return True

    return False


def categorize_flagged_pairs(flagged_pairs: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize flagged pairs into decision groups.

    Args:
        flagged_pairs: List of flagged pair dictionaries

    Returns:
        Dictionary mapping category to list of pairs
    """
    categories = {
        'FALSE_POSITIVE': [],
        'HIERARCHY': [],
        'NAMING_VARIANT': [],
        'MINERS_RELATED': [],  # Special category for miners/mines relationships
        'CONTEXTUAL': [],
    }

    for pair in flagged_pairs:
        tag1 = pair['tag1']
        tag2 = pair['tag2']

        # Check for false positives first
        if is_substring_coincidence(tag1, tag2):
            categories['FALSE_POSITIVE'].append({
                **pair,
                'proposed_action': 'KEEP_SEPARATE',
                'rationale': 'Substring coincidence - semantically unrelated concepts'
            })
            continue

        # Check for generic → specific hierarchies
        is_hierarchy, hierarchy_rationale = is_generic_to_specific_hierarchy(tag1, tag2)
        if is_hierarchy:
            # Determine parent/child based on which is more generic
            # If tag1 is plural or shorter, it's usually the parent
            if len(tag1) < len(tag2) or tag1.endswith('s'):
                parent, child = tag1, tag2
            else:
                parent, child = tag2, tag1

            categories['HIERARCHY'].append({
                **pair,
                'proposed_action': 'HIERARCHY',
                'parent': parent,
                'child': child,
                'rationale': hierarchy_rationale
            })
            continue

        # Check for naming variants
        if is_naming_variant(tag1, tag2):
            categories['NAMING_VARIANT'].append({
                **pair,
                'proposed_action': 'INVESTIGATE',
                'rationale': 'Possible naming variant - examine Zotero items to determine if same entity'
            })
            continue

        # Special category: Miners/mines relationships (complex domain logic)
        if ('miner' in tag1.lower() or 'mine' in tag1.lower()) and \
           ('miner' in tag2.lower() or 'mine' in tag2.lower()):
            categories['MINERS_RELATED'].append({
                **pair,
                'proposed_action': 'REVIEW',
                'rationale': 'Mining domain - requires understanding of miner/mine/dwelling relationships'
            })
            continue

        # Everything else needs contextual review
        categories['CONTEXTUAL'].append({
            **pair,
            'proposed_action': 'REVIEW',
            'rationale': 'Requires examining actual Zotero item context to determine relationship'
        })

    return categories


def generate_triage_report(categories: Dict[str, List[Dict]], output_path: Path):
    """
    Generate human-readable markdown triage report.

    Args:
        categories: Categorized pairs
        output_path: Path to write report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Count statistics
    total = sum(len(pairs) for pairs in categories.values())
    false_pos = len(categories['FALSE_POSITIVE'])
    hierarchy = len(categories['HIERARCHY'])
    naming = len(categories['NAMING_VARIANT'])
    miners = len(categories['MINERS_RELATED'])
    contextual = len(categories['CONTEXTUAL'])

    # Calculate automated decisions
    automated = false_pos + hierarchy
    manual = naming + miners + contextual

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Tag Consolidation Triage Report

**Generated:** {timestamp}
**Total flagged pairs reviewed:** {total}

---

## Executive Summary

This report categorizes the 144 flagged pairs from automated analysis into decision groups for efficient batch review.

### Decision Statistics

- **Automated decisions proposed:** {automated} pairs ({automated/total*100:.1f}%)
  - False positives (keep separate): {false_pos}
  - Hierarchies (multi-tag): {hierarchy}

- **Manual review required:** {manual} pairs ({manual/total*100:.1f}%)
  - Naming variants (investigate): {naming}
  - Mining domain (domain expertise): {miners}
  - Contextual review: {contextual}

---

## Category 1: False Positives (KEEP_SEPARATE)

**Count:** {false_pos} pairs
**Proposed action:** Mark as KEEP_SEPARATE (distinct concepts)

These pairs matched due to substring coincidence but are semantically unrelated.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Rationale |
|-------|-------|---------|---------|-----------|
""")

        for pair in categories['FALSE_POSITIVE']:
            f.write(f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {pair['rationale']} |\n")

        f.write(f"""
---

## Category 2: Generic → Specific Hierarchies (HIERARCHY)

**Count:** {hierarchy} pairs
**Proposed action:** Establish parent-child hierarchy with multi-tagging

These follow the same pattern as the 104 hierarchies already approved (e.g., Church → Methodist Church).

| Parent Tag | Child Tag | Count 1 | Count 2 | Rationale |
|------------|-----------|---------|---------|-----------|
""")

        for pair in categories['HIERARCHY']:
            f.write(f"| **{pair['parent']}** | {pair['child']} | {pair['count1']} | {pair['count2']} | {pair['rationale']} |\n")

        f.write(f"""
---

## Category 3: Naming Variants (INVESTIGATE)

**Count:** {naming} pairs
**Proposed action:** Examine actual Zotero items to determine if same entity

These pairs may represent the same entity with different naming conventions. Requires checking bibliographic items.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Question to Answer |
|-------|-------|---------|---------|-------------------|
""")

        for pair in categories['NAMING_VARIANT']:
            # Generate specific question for each pair
            question = f"Are these the same entity?"
            if 'south' in pair['tag1'].lower() and 'south' in pair['tag2'].lower():
                question = "Same location, different naming convention?"
            elif 'school' in pair['tag1'].lower():
                question = "Same school (renamed/reclassified)?"
            elif 'coal' in pair['tag1'].lower() or 'mine' in pair['tag1'].lower():
                question = "Same company/mine (different official names)?"

            f.write(f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {question} |\n")

        f.write(f"""
---

## Category 4: Mining Domain Relationships (REVIEW)

**Count:** {miners} pairs
**Proposed action:** Apply domain expertise for miners/mines/dwellings relationships

These involve complex relationships between miners, mines, mine infrastructure, and related concepts.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Domain Consideration |
|-------|-------|---------|---------|---------------------|
""")

        for pair in categories['MINERS_RELATED']:
            consideration = "Relationship between concept and instance?"
            if 'dwelling' in pair['tag1'].lower() or 'dwelling' in pair['tag2'].lower():
                consideration = "Are miners' dwellings a subset/aspect of miners generally?"
            elif 'families' in pair['tag1'].lower() or 'families' in pair['tag2'].lower():
                consideration = "Are miners' families a related but distinct concept?"

            f.write(f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {consideration} |\n")

        f.write(f"""
---

## Category 5: Contextual Review Required (REVIEW)

**Count:** {contextual} pairs
**Proposed action:** Examine Zotero items to understand semantic relationship

These pairs require looking at actual bibliographic context to determine appropriate action.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Similarity |
|-------|-------|---------|---------|-----------|
""")

        for pair in categories['CONTEXTUAL']:
            f.write(f"| {pair['tag1']} | {pair['tag2']} | {pair['count1']} | {pair['count2']} | {pair.get('similarity', 'N/A')} |\n")

        f.write(f"""
---

## Recommended Next Steps

### Immediate Batch Decisions (Can approve without further review)

1. **Accept all {false_pos} FALSE_POSITIVE pairs** → Mark as KEEP_SEPARATE
2. **Accept all {hierarchy} HIERARCHY pairs** → Establish parent-child relationships

This resolves {automated} of {total} pairs ({automated/total*100:.1f}%) with high confidence.

### Requires Investigation ({naming} pairs)

For naming variants, check Zotero items to determine:
- Are they the same entity? → MERGE (with canonical form decision)
- Are they related but distinct? → HIERARCHY or KEEP_SEPARATE

### Requires Domain Expertise ({miners + contextual} pairs)

The mining domain relationships and contextual pairs require historian review:
- Understanding of historical mining industry structure
- Knowledge of local institutions and relationships
- Examination of actual bibliographic context

---

## Approval Workflow

**Option A (Fast):** Approve Categories 1-2 as batch, review Categories 3-5 individually

**Option B (Careful):** Review sample from each category before batch approval

**Recommended:** Option A - batch approve obvious patterns, focus time on genuinely ambiguous cases

""")

    print(f"✓ Triage report written to: {output_path}")


def main():
    """Main execution function."""
    # Paths
    base_dir = Path(__file__).parent.parent
    decisions_file = base_dir / "planning/phase1.2.1-consolidation-decisions.md"
    output_file = base_dir / "reports/triage_report.md"

    print("Tag Consolidation Triage Analysis")
    print("=" * 60)
    print()

    # Read flagged pairs from decisions file
    print("Reading flagged pairs from consolidation decisions...")
    flagged_pairs = []

    with open(decisions_file, 'r', encoding='utf-8') as f:
        in_flagged_section = False
        for line in f:
            if '## FLAGGED FOR REVIEW' in line:
                in_flagged_section = True
                continue

            if in_flagged_section and line.startswith('| ') and not line.startswith('| Tag 1'):
                parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
                if len(parts) >= 5 and parts[0] not in ['----', 'Tag 1']:
                    flagged_pairs.append({
                        'tag1': parts[0],
                        'tag2': parts[1],
                        'count1': parts[2],
                        'count2': parts[3],
                        'similarity': parts[4]
                    })

    print(f"✓ Found {len(flagged_pairs)} flagged pairs")
    print()

    # Categorize pairs
    print("Categorizing pairs by pattern...")
    categories = categorize_flagged_pairs(flagged_pairs)

    print(f"✓ False positives: {len(categories['FALSE_POSITIVE'])}")
    print(f"✓ Hierarchies: {len(categories['HIERARCHY'])}")
    print(f"✓ Naming variants: {len(categories['NAMING_VARIANT'])}")
    print(f"✓ Mining domain: {len(categories['MINERS_RELATED'])}")
    print(f"✓ Contextual review: {len(categories['CONTEXTUAL'])}")
    print()

    # Generate report
    print("Generating triage report...")
    generate_triage_report(categories, output_file)
    print()

    print("=" * 60)
    print(f"Triage complete! Review the report at:")
    print(f"  {output_file}")
    print()
    print("Next: Review the report and approve/modify proposed decisions")


if __name__ == "__main__":
    main()
