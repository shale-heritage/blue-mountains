#!/usr/bin/env python3
"""
Script 43: Comprehensive Archive Comparison

Compare current tag_map_consolidated.csv against archived poly_hierarchy_additions.csv
to identify any valuable content that may have been lost during cleanup.

Focus on:
1. Primary hierarchy relationships (non-thematic)
2. Merge operations
3. Tags that existed in archive but missing from current

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set, Tuple


def load_csv_as_set(path: Path) -> Set[Tuple]:
    """Load CSV rows as set of tuples for comparison."""
    rows = set()
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                rows.add(tuple(row[:4]))  # old_tag, new_tag, action, notes
    return rows


def compare_csvs(current_path: Path, archive_path: Path, output_path: Path):
    """Generate comprehensive comparison report."""

    print("=" * 80)
    print("COMPREHENSIVE ARCHIVE COMPARISON")
    print("=" * 80)
    print()

    # Load CSVs
    print(f"Loading current CSV: {current_path}...")
    current_rows = load_csv_as_set(current_path)
    print(f"  Loaded {len(current_rows)} unique rows")

    print(f"Loading archive CSV: {archive_path}...")
    archive_rows = load_csv_as_set(archive_path)
    print(f"  Loaded {len(archive_rows)} unique rows")
    print()

    # Find differences
    print("Comparing...")
    missing_from_current = archive_rows - current_rows
    added_in_current = current_rows - archive_rows

    print(f"  Rows in archive but missing from current: {len(missing_from_current)}")
    print(f"  Rows added in current (not in archive): {len(added_in_current)}")
    print()

    # Categorize missing rows
    print("Categorizing missing rows...")
    missing_primary = []
    missing_thematic = []
    missing_merges = []
    missing_other = []

    for row in missing_from_current:
        old_tag, new_tag, action, notes = row

        if action == 'merge':
            missing_merges.append(row)
        elif action == 'hierarchy':
            if '- THEMATIC' in notes or 'thematic grouping' in notes.lower():
                missing_thematic.append(row)
            else:
                missing_primary.append(row)
        else:
            missing_other.append(row)

    print(f"  Missing primary hierarchies: {len(missing_primary)}")
    print(f"  Missing thematic hierarchies: {len(missing_thematic)}")
    print(f"  Missing merges: {len(missing_merges)}")
    print(f"  Missing other actions: {len(missing_other)}")
    print()

    # Write report
    print(f"Writing comparison report to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Comprehensive Archive Comparison\n\n")
        f.write(f"**Generated:** 2025-10-24\n")
        f.write(f"**Current CSV:** {current_path}\n")
        f.write(f"**Archive CSV:** {archive_path}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Current rows: {len(current_rows)}\n")
        f.write(f"- Archive rows: {len(archive_rows)}\n")
        f.write(f"- Missing from current: {len(missing_from_current)}\n")
        f.write(f"- Added in current: {len(added_in_current)}\n\n")

        f.write("### Missing Content Breakdown\n\n")
        f.write(f"- Missing primary hierarchies: {len(missing_primary)}\n")
        f.write(f"- Missing thematic hierarchies: {len(missing_thematic)}\n")
        f.write(f"- Missing merges: {len(missing_merges)}\n")
        f.write(f"- Missing other actions: {len(missing_other)}\n\n")

        f.write("---\n\n")

        # Section 1: Missing Primary Hierarchies
        f.write("## Section 1: Missing Primary Hierarchies\n\n")
        f.write(f"**Count:** {len(missing_primary)}\n\n")
        f.write("These primary hierarchy relationships existed in archive but are missing from current.\n\n")

        if len(missing_primary) == 0:
            f.write("*No missing primary hierarchies - all preserved!*\n\n")
        else:
            # Group by parent
            by_parent = defaultdict(list)
            for row in missing_primary:
                old_tag, new_tag, action, notes = row
                parent = notes.replace('parent=', '').split(' -')[0].split(' (')[0].strip() if 'parent=' in notes else 'UNKNOWN'
                by_parent[parent].append((old_tag, notes))

            for parent in sorted(by_parent.keys())[:50]:  # Show first 50
                entries = by_parent[parent]
                f.write(f"### Parent: {parent} ({len(entries)} missing)\n\n")
                for tag, notes in entries[:10]:  # Show first 10 per parent
                    f.write(f"- `{tag}` → {notes}\n")
                if len(entries) > 10:
                    f.write(f"- ... and {len(entries) - 10} more\n")
                f.write("\n")

            if len(by_parent) > 50:
                f.write(f"*... and {len(by_parent) - 50} more parents*\n\n")

        f.write("---\n\n")

        # Section 2: Missing Thematic Hierarchies
        f.write("## Section 2: Missing Thematic Hierarchies\n\n")
        f.write(f"**Count:** {len(missing_thematic)}\n\n")

        if len(missing_thematic) == 0:
            f.write("*No missing thematic hierarchies!*\n\n")
        else:
            for row in sorted(missing_thematic)[:20]:
                old_tag, new_tag, action, notes = row
                f.write(f"- `{old_tag}` → {notes}\n")
            if len(missing_thematic) > 20:
                f.write(f"- ... and {len(missing_thematic) - 20} more\n")
            f.write("\n")

        f.write("---\n\n")

        # Section 3: Missing Merges
        f.write("## Section 3: Missing Merge Operations\n\n")
        f.write(f"**Count:** {len(missing_merges)}\n\n")

        if len(missing_merges) == 0:
            f.write("*No missing merges!*\n\n")
        else:
            for row in sorted(missing_merges)[:20]:
                old_tag, new_tag, action, notes = row
                f.write(f"- `{old_tag}` → `{new_tag}` ({notes})\n")
            if len(missing_merges) > 20:
                f.write(f"- ... and {len(missing_merges) - 20} more\n")
            f.write("\n")

        f.write("---\n\n")

        # Section 4: Added Content
        f.write("## Section 4: Content Added in Current (Not in Archive)\n\n")
        f.write(f"**Count:** {len(added_in_current)}\n\n")
        f.write("Sample of new content:\n\n")

        for row in sorted(added_in_current)[:30]:
            old_tag, new_tag, action, notes = row
            f.write(f"- `{old_tag}` ({action}) → {notes}\n")
        if len(added_in_current) > 30:
            f.write(f"- ... and {len(added_in_current) - 30} more\n")
        f.write("\n")

    print(f"  ✓ Report written")
    print()

    # Print critical findings
    print("=" * 80)
    print("CRITICAL FINDINGS")
    print("=" * 80)
    print()

    if len(missing_primary) > 0:
        print(f"⚠️  WARNING: {len(missing_primary)} primary hierarchy relationships lost")
        print(f"   Review report Section 1 carefully")
        print()

    if len(missing_merges) > 0:
        print(f"⚠️  WARNING: {len(missing_merges)} merge operations lost")
        print(f"   Review report Section 3 carefully")
        print()

    if len(missing_primary) == 0 and len(missing_merges) == 0:
        print("✓ No critical content lost - all primary hierarchies and merges preserved")
        print()

    print(f"Full report: {output_path}")
    print()


def main():
    """Main execution."""
    current_path = Path('data/tag_map_consolidated.csv')
    archive_path = Path('archive/csv-files/poly_hierarchy_additions.csv')
    output_path = Path('reports/archive_comparison_comprehensive.md')

    if not current_path.exists():
        print(f"ERROR: {current_path} not found")
        return 1

    if not archive_path.exists():
        print(f"ERROR: {archive_path} not found")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)

    compare_csvs(current_path, archive_path, output_path)

    return 0


if __name__ == '__main__':
    exit(main())
