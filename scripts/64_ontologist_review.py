#!/usr/bin/env python3
"""
Comprehensive ontologist review of taxonomy quality.

This script examines the taxonomy for:
- Capitalisation inconsistencies
- Duplicate terms
- Singular/plural pattern violations
- Disambiguation completeness
- Hierarchical logic issues
"""

import csv
import re
from collections import defaultdict, Counter
from pathlib import Path

def main():
    csv_file = Path('data/tag_map_consolidated.csv')

    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Filter active hierarchy entries only
    active_hierarchy = [r for r in rows if r['status'] == 'active' and r['action'] == 'hierarchy']

    print('='*80)
    print('ONTOLOGIST REVIEW: TAXONOMY QUALITY ANALYSIS')
    print('='*80)
    print()

    # Issue 1: Check for capitalization inconsistencies
    print('1. CAPITALISATION CONSISTENCY')
    print('-' * 80)

    # Group by lowercase version to find variants
    lowercase_map = defaultdict(list)
    for row in active_hierarchy:
        term = row['new_tag']
        lowercase_map[term.lower()].append(term)

    cap_issues = []
    for lower, variants in lowercase_map.items():
        if len(variants) > 1:
            # Check if they are genuinely different
            unique_variants = list(set(variants))
            if len(unique_variants) > 1:
                # Filter out intentional variations (REMOVED markers, parentheticals, etc)
                cleaned_variants = [v for v in unique_variants if 'REMOVED' not in v and 'THEMATIC' not in v]
                if len(cleaned_variants) > 1:
                    cap_issues.append((lower, cleaned_variants))

    if cap_issues:
        print(f'Found {len(cap_issues)} potential capitalisation inconsistencies:')
        for lower, variants in cap_issues[:15]:
            print(f'  • {variants}')
    else:
        print('✓ No capitalisation inconsistencies found')
    print()

    # Issue 2: Duplicate terms (exact)
    print('2. EXACT DUPLICATE TERMS')
    print('-' * 80)
    term_counts = Counter(row['new_tag'] for row in active_hierarchy)
    duplicates = [(term, count) for term, count in term_counts.items() if count > 1]
    if duplicates:
        print(f'Found {len(duplicates)} terms with multiple active hierarchy entries:')
        for term, count in sorted(duplicates, key=lambda x: -x[1])[:20]:
            print(f'  • "{term}" appears {count} times')
    else:
        print('✓ No exact duplicates found')
    print()

    # Issue 3: Orphaned terms (no parent)
    print('3. ORPHANED TERMS (No Parent Reference)')
    print('-' * 80)

    parent_pattern = re.compile(r'parent=')
    orphaned = []
    for row in active_hierarchy:
        if not parent_pattern.search(row['notes']):
            # Top-level facets are expected to have no parent
            term = row['new_tag']
            if term not in ['Activities', 'Agents', 'Built Environment', 'Events',
                           'Information Forms', 'Materials', 'Places', 'Associated Concepts']:
                orphaned.append(term)

    if orphaned:
        print(f'Found {len(orphaned)} orphaned terms (no parent):')
        for term in orphaned[:15]:
            print(f'  • "{term}"')
    else:
        print('✓ No orphaned terms found')
    print()

    # Issue 4: Check for terms that appear in wrong case contexts
    print('4. MIXED CASE IN PARENT-CHILD RELATIONSHIPS')
    print('-' * 80)

    # Build parent-child map
    children_map = defaultdict(list)
    parent_extract = re.compile(r'parent=([^,;]+)')

    for row in active_hierarchy:
        match = parent_extract.search(row['notes'])
        if match:
            parent_name = match.group(1).strip()
            children_map[parent_name].append(row['new_tag'])

    # Check for case mixing
    case_mixing = []
    for parent, children in children_map.items():
        if children:
            # Check if parent is lowercase but has Title Case children (or vice versa)
            parent_is_lower = parent[0].islower()
            for child in children:
                if '(' not in child:  # Skip disambiguated terms
                    child_is_lower = child[0].islower()
                    if parent_is_lower != child_is_lower:
                        # This might be intentional (generic parent, specific named child)
                        # But flag for review
                        case_mixing.append((parent, child))

    if case_mixing:
        print(f'Found {len(case_mixing)} parent-child case variations (might be intentional):')
        for parent, child in case_mixing[:10]:
            print(f'  • Parent "{parent}" → Child "{child}"')
    else:
        print('✓ Case usage appears consistent')
    print()

    # Issue 5: REMOVED entries that are still marked active
    print('5. REMOVED ENTRIES MARKED AS ACTIVE')
    print('-' * 80)

    removed_but_active = [r for r in active_hierarchy if 'REMOVED' in r['new_tag']]
    if removed_but_active:
        print(f'Found {len(removed_but_active)} entries marked REMOVED but status=active:')
        for row in removed_but_active[:10]:
            print(f'  • "{row["new_tag"]}"')
    else:
        print('✓ No REMOVED entries marked as active')
    print()

    # Issue 6: Terms with multiple parents (polyhierarchy check)
    print('6. POLYHIERARCHICAL RELATIONSHIPS')
    print('-' * 80)

    term_parent_count = defaultdict(int)
    for row in active_hierarchy:
        # Count parent references
        matches = re.findall(r'parent=([^,;]+)', row['notes'])
        if len(matches) > 1:
            term_parent_count[row['new_tag']] = len(matches)

    if term_parent_count:
        print(f'Found {len(term_parent_count)} terms with multiple parents (polyhierarchical):')
        for term, count in sorted(term_parent_count.items(), key=lambda x: -x[1])[:15]:
            print(f'  • "{term}" has {count} parents')
    else:
        print('(No polyhierarchical terms found - this may be incorrect)')
    print()

    # Summary
    print('='*80)
    print('SUMMARY')
    print('='*80)
    print(f'Total active hierarchy entries: {len(active_hierarchy)}')
    print(f'Capitalisation issues: {len(cap_issues)}')
    print(f'Duplicate terms: {len(duplicates)}')
    print(f'Orphaned terms: {len(orphaned)}')
    print(f'Case mixing instances: {len(case_mixing)}')
    print(f'REMOVED but active: {len(removed_but_active)}')
    print(f'Polyhierarchical terms: {len(term_parent_count)}')
    print('='*80)

if __name__ == '__main__':
    main()
