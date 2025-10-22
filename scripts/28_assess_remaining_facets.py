#!/usr/bin/env python3
"""
Script 28: Assess Remaining Facets for Tag Cleaning Issues

Systematically analyzes the poly-hierarchical taxonomy to identify potential issues:
1. Potential synonyms/variants (similar names, abbreviations)
2. Singular/plural inconsistencies within categories
3. Missing intermediate facets (leaf nodes at wrong hierarchical level)
4. Potential buildings vs organizations issues
5. Company name standardization issues

Usage:
    python scripts/28_assess_remaining_facets.py

Outputs:
    - Console: Summary statistics and flagged issues
    - reports/facet_assessment_report.md: Detailed assessment with priorities

Author: Claude Code
Date: 2025-10-20
"""

import csv
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher


def load_hierarchy(csv_path):
    """
    Load poly-hierarchy CSV and parse into data structures.

    Returns:
        dict: Hierarchy data with parent-child relationships
    """
    hierarchies = defaultdict(list)
    all_tags = set()
    tag_parents = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row['old_tag']
            action = row['action']
            notes = row['notes']

            if action == 'hierarchy':
                all_tags.add(tag)
                # Extract parent from notes
                parent_match = re.search(r'parent=([^,\)]+)', notes)
                if parent_match:
                    parent = parent_match.group(1).strip()
                    if parent != '(new top-level facet)':
                        hierarchies[parent].append(tag)
                        tag_parents[tag] = parent

    return hierarchies, all_tags, tag_parents


def find_similar_tags(tags, threshold=0.85):
    """
    Find potentially similar tags that might be variants/synonyms.

    Args:
        tags: Set of tag names
        threshold: Similarity threshold (0-1)

    Returns:
        list: Tuples of (tag1, tag2, similarity_score)
    """
    similar_pairs = []
    tag_list = sorted(tags)

    for i, tag1 in enumerate(tag_list):
        for tag2 in tag_list[i+1:]:
            # Skip if already processed
            if tag1 == tag2:
                continue

            # Calculate similarity
            similarity = SequenceMatcher(None, tag1.lower(), tag2.lower()).ratio()

            if similarity >= threshold:
                similar_pairs.append((tag1, tag2, similarity))

            # Check for abbreviations
            if tag2.replace('.', '').replace(' ', '') in tag1.replace(' ', ''):
                similar_pairs.append((tag1, tag2, 0.9))  # High score for abbreviations

    return sorted(similar_pairs, key=lambda x: x[2], reverse=True)


def check_singular_plural(tags):
    """
    Check for potential singular/plural inconsistencies.

    Returns:
        list: Tuples of (singular_candidate, plural_candidate)
    """
    issues = []
    tag_list = sorted(tags)

    for tag in tag_list:
        # Common plural patterns
        if tag.endswith('s') and tag not in ['Headquarters', 'Thanks', 'News']:
            singular = tag[:-1]
            if singular in tags and singular != tag:
                issues.append((singular, tag))

        # -ies/-y pattern
        if tag.endswith('ies'):
            singular = tag[:-3] + 'y'
            if singular in tags:
                issues.append((singular, tag))

    return issues


def check_intermediate_facets(hierarchies, tag_parents):
    """
    Check for missing intermediate facets (too many children at one level).

    Returns:
        list: Parents with suspiciously many direct children
    """
    issues = []

    for parent, children in hierarchies.items():
        # Flag if parent has more than 10 direct children
        # This might indicate missing intermediate facet
        if len(children) > 10:
            issues.append((parent, len(children), children))

    return sorted(issues, key=lambda x: x[1], reverse=True)


def check_buildings_vs_orgs(tags):
    """
    Check for potential buildings that might be miscategorized as organizations.

    Returns:
        list: Tags that end in building-related terms
    """
    building_indicators = ['Hall', 'Building', 'House', 'Station', 'Office', 'Chambers']
    issues = []

    for tag in tags:
        for indicator in building_indicators:
            if tag.endswith(indicator) or f" {indicator}" in tag:
                issues.append((tag, indicator))
                break

    return issues


def check_company_names(tags):
    """
    Check for company names that need standardization.

    Returns:
        list: Tags with company name issues
    """
    issues = []

    for tag in tags:
        has_issue = False
        issue_types = []

        # Check for "Co." instead of "Company"
        if re.search(r'\bCo\.', tag):
            has_issue = True
            issue_types.append('Contains "Co." - should be "Company"')

        # Check for "&" instead of "and"
        if '&' in tag and 'Company' in tag:
            has_issue = True
            issue_types.append('Contains "&" - should be "and"')

        # Check for "Limited" or "Ltd."
        if re.search(r'\b(Limited|Ltd\.?)\b', tag):
            has_issue = True
            issue_types.append('Contains "Limited"/"Ltd." - consider dropping')

        if has_issue:
            issues.append((tag, '; '.join(issue_types)))

    return issues


def analyze_primary_facets(csv_path):
    """
    Analyze primary facets and generate comprehensive assessment report.

    Returns:
        dict: Assessment results by category
    """
    hierarchies, all_tags, tag_parents = load_hierarchy(csv_path)

    results = {
        'similar_tags': find_similar_tags(all_tags, threshold=0.85),
        'singular_plural': check_singular_plural(all_tags),
        'intermediate_facets': check_intermediate_facets(hierarchies, tag_parents),
        'buildings_vs_orgs': check_buildings_vs_orgs(all_tags),
        'company_names': check_company_names(all_tags),
        'hierarchies': hierarchies,
        'all_tags': all_tags,
        'tag_parents': tag_parents
    }

    return results


def generate_report(results, output_path):
    """Generate detailed assessment report in Markdown format."""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Facet Assessment Report - Tag Cleaning Issues\n\n")
        f.write("**Generated:** 2025-10-20\n")
        f.write("**Purpose:** Systematic assessment of remaining primary facets for cleaning\n\n")
        f.write("---\n\n")

        # Summary statistics
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Total tags analyzed:** {len(results['all_tags'])}\n")
        f.write(f"- **Similar tag pairs found:** {len(results['similar_tags'])}\n")
        f.write(f"- **Singular/plural inconsistencies:** {len(results['singular_plural'])}\n")
        f.write(f"- **Parents with many children (>10):** {len(results['intermediate_facets'])}\n")
        f.write(f"- **Potential building tags:** {len(results['buildings_vs_orgs'])}\n")
        f.write(f"- **Company name issues:** {len(results['company_names'])}\n\n")
        f.write("---\n\n")

        # Similar tags (potential synonyms/variants)
        f.write("## 1. Similar Tags (Potential Synonyms/Variants)\n\n")
        f.write("**Issue:** Tags with similar names may be variants, abbreviations, or synonyms.\n\n")
        f.write("**Action needed:** Review each pair to determine if MERGE or KEEP SEPARATE.\n\n")

        if results['similar_tags']:
            f.write("| Tag 1 | Tag 2 | Similarity | Notes |\n")
            f.write("|-------|-------|------------|-------|\n")
            for tag1, tag2, sim in results['similar_tags'][:30]:  # Top 30
                f.write(f"| {tag1} | {tag2} | {sim:.2f} | |\n")
            if len(results['similar_tags']) > 30:
                f.write(f"\n*...and {len(results['similar_tags']) - 30} more pairs*\n")
        else:
            f.write("✅ No similar tag pairs found.\n")

        f.write("\n---\n\n")

        # Singular/plural inconsistencies
        f.write("## 2. Singular/Plural Inconsistencies\n\n")
        f.write("**Issue:** Tags have both singular and plural forms.\n\n")
        f.write("**Action needed:** Determine if these should be merged or kept separate based on usage.\n\n")

        if results['singular_plural']:
            f.write("| Singular | Plural | Parent Context |\n")
            f.write("|----------|--------|----------------|\n")
            for singular, plural in results['singular_plural']:
                parent_s = results['tag_parents'].get(singular, 'N/A')
                parent_p = results['tag_parents'].get(plural, 'N/A')
                f.write(f"| {singular} | {plural} | S: {parent_s}<br>P: {parent_p} |\n")
        else:
            f.write("✅ No singular/plural inconsistencies found.\n")

        f.write("\n---\n\n")

        # Missing intermediate facets
        f.write("## 3. Potential Missing Intermediate Facets\n\n")
        f.write("**Issue:** Parents with >10 direct children may need intermediate facets.\n\n")
        f.write("**Action needed:** Review to determine if intermediate categorisation is needed.\n\n")

        if results['intermediate_facets']:
            f.write("| Parent Tag | # Children | Sample Children (first 5) |\n")
            f.write("|------------|------------|---------------------------|\n")
            for parent, count, children in results['intermediate_facets']:
                sample = ', '.join(children[:5])
                if len(children) > 5:
                    sample += f", ...and {len(children) - 5} more"
                f.write(f"| {parent} | {count} | {sample} |\n")
        else:
            f.write("✅ No parents with excessive children found.\n")

        f.write("\n---\n\n")

        # Buildings vs organizations
        f.write("## 4. Potential Buildings Miscategorized as Organizations\n\n")
        f.write("**Issue:** Tags ending in building-related terms may be physical structures.\n\n")
        f.write("**Action needed:** Verify if these should be in Built Environment facet.\n\n")

        if results['buildings_vs_orgs']:
            f.write("| Tag | Indicator | Current Parent | Notes |\n")
            f.write("|-----|-----------|----------------|-------|\n")
            for tag, indicator in results['buildings_vs_orgs']:
                parent = results['tag_parents'].get(tag, 'Top-level')
                f.write(f"| {tag} | {indicator} | {parent} | |\n")
        else:
            f.write("✅ No potential building tags found.\n")

        f.write("\n---\n\n")

        # Company name issues
        f.write("## 5. Company Name Standardization Issues\n\n")
        f.write("**Issue:** Company names need standardization (spell out Co./&, drop Ltd.).\n\n")
        f.write("**Action needed:** Apply standardization pattern established in Phase 1.\n\n")

        if results['company_names']:
            f.write("| Current Name | Issues | Suggested Change |\n")
            f.write("|--------------|--------|------------------|\n")
            for tag, issues in results['company_names']:
                suggested = tag
                suggested = re.sub(r'\bCo\.', 'Company', suggested)
                suggested = re.sub(r' & ', ' and ', suggested)
                suggested = re.sub(r'\b(Limited|Ltd\.?)\b', '', suggested).strip()
                f.write(f"| {tag} | {issues} | {suggested} |\n")
        else:
            f.write("✅ No company name issues found.\n")

        f.write("\n---\n\n")

        # Priority recommendations
        f.write("## Priority Recommendations\n\n")

        priority_high = []
        priority_med = []
        priority_low = []

        # Prioritize issues
        if len(results['company_names']) > 0:
            priority_high.append(f"**Fix {len(results['company_names'])} company name issues** (established pattern, automatic fix)")

        if len(results['singular_plural']) > 0:
            priority_high.append(f"**Review {len(results['singular_plural'])} singular/plural pairs** (may indicate inconsistency)")

        if len(results['buildings_vs_orgs']) > 5:
            priority_med.append(f"**Review {len(results['buildings_vs_orgs'])} potential building tags** (verify categorization)")

        if len(results['intermediate_facets']) > 0:
            priority_med.append(f"**Review {len(results['intermediate_facets'])} parents with many children** (consider intermediate facets)")

        if len(results['similar_tags']) > 0:
            priority_low.append(f"**Review {len(results['similar_tags'])} similar tag pairs** (may be legitimate distinct tags)")

        f.write("### HIGH Priority\n\n")
        if priority_high:
            for item in priority_high:
                f.write(f"- {item}\n")
        else:
            f.write("- ✅ No high-priority issues\n")

        f.write("\n### MEDIUM Priority\n\n")
        if priority_med:
            for item in priority_med:
                f.write(f"- {item}\n")
        else:
            f.write("- ✅ No medium-priority issues\n")

        f.write("\n### LOW Priority\n\n")
        if priority_low:
            for item in priority_low:
                f.write(f"- {item}\n")
        else:
            f.write("- ✅ No low-priority issues\n")

        f.write("\n---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Manual spot-check flagged tags with primary sources (scripts 24-27 pattern)\n")
        f.write("2. Apply batch corrections to `scripts/22_generate_poly_hierarchy.py`\n")
        f.write("3. Create variant merge CSVs for any new synonyms\n")
        f.write("4. Regenerate poly-hierarchy CSV and visualizations\n")
        f.write("5. Validate all corrections with validation report\n\n")
        f.write("---\n\n")
        f.write("**Assessment completed by:** Claude Code  \n")
        f.write("**Date:** 2025-10-20\n")


def main():
    """Run facet assessment analysis."""
    print("=" * 80)
    print("FACET ASSESSMENT - TAG CLEANING ANALYSIS")
    print("=" * 80)
    print()

    csv_path = Path('data/poly_hierarchy_additions.csv')

    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return

    print(f"Loading hierarchy from: {csv_path}")
    results = analyze_primary_facets(csv_path)

    print(f"✓ Analyzed {len(results['all_tags'])} tags\n")

    # Print console summary
    print("ISSUE SUMMARY:")
    print(f"  - Similar tag pairs: {len(results['similar_tags'])}")
    print(f"  - Singular/plural issues: {len(results['singular_plural'])}")
    print(f"  - Parents with >10 children: {len(results['intermediate_facets'])}")
    print(f"  - Potential building tags: {len(results['buildings_vs_orgs'])}")
    print(f"  - Company name issues: {len(results['company_names'])}")
    print()

    # Generate detailed report
    output_path = Path('reports/facet_assessment_report.md')
    print(f"Generating detailed report: {output_path}")
    generate_report(results, output_path)
    print(f"✓ Report generated successfully\n")

    print("=" * 80)
    print("ASSESSMENT COMPLETE")
    print("=" * 80)
    print()
    print(f"Review detailed report at: {output_path}")
    print()


if __name__ == '__main__':
    main()
