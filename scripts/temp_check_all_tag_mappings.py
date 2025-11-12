#!/usr/bin/env python3
"""
Check ALL original Zotero tags to ensure they have mappings in the new taxonomy.

Identifies potential data loss where tags in Zotero don't have corresponding
hierarchy entries or synonym mappings in tag_map_consolidated.csv.

This addresses the critical concern: when applying the new taxonomy, any Zotero
tags without mappings will be LOST.
"""

import json
import csv
from collections import defaultdict

# Load Zotero export
print("Loading Zotero export...")
with open('data/zotero_full_export.json', 'r') as f:
    zotero_data = json.load(f)

# Extract all unique tags from Zotero
zotero_tags = set()
tag_frequency = defaultdict(int)

for item in zotero_data['items']:
    for tag in item.get('tags', []):
        zotero_tags.add(tag)
        tag_frequency[tag] += 1

print(f"Found {len(zotero_tags)} unique tags in Zotero")

# Load taxonomy mappings
print("Loading taxonomy mappings...")
with open('data/tag_map_consolidated.csv', 'r') as f:
    reader = csv.DictReader(f)

    # Collect all tags that have mappings (hierarchy or synonym)
    mapped_tags = set()
    hierarchy_tags = set()
    synonym_sources = set()

    for row in reader:
        old_tag = row['old_tag']
        action = row['action']

        mapped_tags.add(old_tag)

        if action == 'hierarchy':
            hierarchy_tags.add(old_tag)
        elif action == 'synonym':
            synonym_sources.add(old_tag)

print(f"Found {len(mapped_tags)} tags in taxonomy mapping")
print(f"  - {len(hierarchy_tags)} hierarchy entries")
print(f"  - {len(synonym_sources)} synonym mappings")

# Find unmapped tags (potential data loss)
unmapped = zotero_tags - mapped_tags

print("\n" + "="*80)
print("POTENTIAL DATA LOSS ANALYSIS")
print("="*80)

if unmapped:
    print(f"\n⚠️  Found {len(unmapped)} tags in Zotero WITHOUT mappings:")
    print(f"\nThese tags will be LOST when applying the new taxonomy!\n")

    # Sort by frequency (most used first)
    unmapped_sorted = sorted(unmapped, key=lambda x: tag_frequency[x], reverse=True)

    for i, tag in enumerate(unmapped_sorted, 1):
        count = tag_frequency[tag]
        print(f"{i:3d}. \"{tag}\" ({count} items)")

        if i == 50:
            print(f"\n... and {len(unmapped) - 50} more")
            break
else:
    print("\n✓ All Zotero tags have mappings in the taxonomy!")
    print("✓ No data loss expected when applying new taxonomy")

# Additional analysis: Case sensitivity issues
print("\n" + "="*80)
print("CASE SENSITIVITY CHECK")
print("="*80)

case_issues = []
for ztag in zotero_tags:
    # Check if lowercase version exists in mappings but not exact case
    if ztag not in mapped_tags:
        ztag_lower = ztag.lower()
        # See if any mapped tag matches when lowercased
        for mtag in mapped_tags:
            if mtag.lower() == ztag_lower and mtag != ztag:
                case_issues.append((ztag, mtag, tag_frequency[ztag]))
                break

if case_issues:
    print(f"\n⚠️  Found {len(case_issues)} case sensitivity issues:")
    print("These tags exist in Zotero but only lowercase versions are mapped:\n")

    case_issues_sorted = sorted(case_issues, key=lambda x: x[2], reverse=True)
    for ztag, mtag, count in case_issues_sorted[:20]:
        print(f'  Zotero: "{ztag}" ({count} items)')
        print(f'  Mapped: "{mtag}"')
        print()
else:
    print("\n✓ No case sensitivity issues found")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total Zotero tags:     {len(zotero_tags):4d}")
print(f"Mapped tags:           {len(zotero_tags & mapped_tags):4d}")
print(f"Unmapped tags:         {len(unmapped):4d}")
print(f"Case sensitivity issues: {len(case_issues):4d}")

coverage = len(zotero_tags & mapped_tags) / len(zotero_tags) * 100
print(f"\nMapping coverage:      {coverage:.1f}%")

if unmapped or case_issues:
    print("\n⚠️  ACTION REQUIRED: Fix unmapped tags and case sensitivity issues")
    print("   to prevent data loss when applying taxonomy")
else:
    print("\n✓ Ready to apply new taxonomy - all tags have mappings!")
