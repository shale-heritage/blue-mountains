#!/usr/bin/env python3
"""
Script 11: Regenerate Consolidation Reports from CSV

Reads the tag_consolidation_map.csv and regenerates the human-readable
Markdown reports WITHOUT modifying the CSV itself.
"""

import sys
import pandas as pd
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def load_consolidation_map():
    """Load the consolidation map CSV."""
    csv_path = config.DATA_DIR / 'tag_consolidation_map.csv'
    print(f"Loading consolidation map from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} consolidation decisions")
    return df


def generate_summary(df):
    """Generate summary statistics from consolidation map."""
    # Count actions
    action_counts = df['action'].value_counts()

    summary = {
        'total_decisions': len(df),
        'merge_count': action_counts.get('merge', 0),
        'hierarchy_count': action_counts.get('hierarchy', 0),
        'keep_count': action_counts.get('keep', 0),
        'flag_count': action_counts.get('flag', 0)
    }

    return summary


def generate_decisions_markdown(df, summary):
    """Generate the phase1.2.1-consolidation-decisions.md file."""
    from datetime import datetime

    output_file = Path('planning/phase1.2.1-consolidation-decisions.md')
    print(f"\nGenerating decisions markdown at {output_file}...")

    # Separate by action
    merges = df[df['action'] == 'merge']
    hierarchies = df[df['action'] == 'hierarchy']
    keeps = df[df['action'] == 'keep']
    flags = df[df['action'] == 'flag']

    # Build markdown content
    content = f"""# Phase 1.2.1: Tag Consolidation Decisions

**Date generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total decisions:** {summary['total_decisions']}
**Method:** Semi-automated pattern matching + contextual analysis + manual review

---

## MERGE Decisions (Naming Variants)

**Count:** {summary['merge_count']} pairs

"""

    if len(merges) > 0:
        content += "| Old Tag | New Tag | Notes |\n"
        content += "|---------|---------|-------|\n"
        for _, row in merges.iterrows():
            notes = row['notes'] if pd.notna(row['notes']) else ''
            content += f"| {row['old_tag']} | {row['new_tag']} | {notes} |\n"
    else:
        content += "No naming variant merges currently approved.\n\n"
        content += "**Principle:** No family names or person names will be merged without reviewing primary sources.\n"

    content += "\n---\n\n## HIERARCHY Decisions (Parent-Child Relationships)\n\n"
    content += f"**Count:** {summary['hierarchy_count']} pairs\n\n"
    content += "Apply multi-tagging: items get BOTH parent and child tags.\n\n"

    if len(hierarchies) > 0:
        # Group by parent
        hierarchies_with_parent = hierarchies[hierarchies['notes'].str.contains('parent=', na=False)]

        # Extract parent from notes
        parents_dict = {}
        for _, row in hierarchies_with_parent.iterrows():
            notes = row['notes']
            if pd.notna(notes) and 'parent=' in notes:
                parent = notes.split('parent=')[1].split(',')[0].split(';')[0].strip()
                if parent not in parents_dict:
                    parents_dict[parent] = []
                parents_dict[parent].append(row)

        # Sort parents by number of children (descending)
        sorted_parents = sorted(parents_dict.items(), key=lambda x: len(x[1]), reverse=True)

        content += "| Parent Tag | Child Tag | Notes |\n"
        content += "|------------|-----------|-------|\n"

        for parent, rows in sorted_parents:
            for row in rows:
                notes = row['notes'] if pd.notna(row['notes']) else ''
                content += f"| **{parent}** | {row['old_tag']} | {notes} |\n"

    content += "\n---\n\n## KEEP_SEPARATE Decisions\n\n"
    content += f"**Count:** {summary['keep_count']} pairs\n\n"

    if len(keeps) > 0:
        content += "| Tag | Notes |\n"
        content += "|-----|-------|\n"
        for _, row in keeps.iterrows():
            notes = row['notes'] if pd.notna(row['notes']) else ''
            content += f"| {row['old_tag']} | {notes} |\n"

    content += "\n---\n\n## FLAGGED for Manual Review\n\n"
    content += f"**Count:** {summary['flag_count']} pairs\n\n"

    if len(flags) > 0:
        content += "| Tag | Notes |\n"
        content += "|-----|-------|\n"
        for _, row in flags.iterrows():
            notes = row['notes'] if pd.notna(row['notes']) else ''
            content += f"| {row['old_tag']} | {notes} |\n"
    else:
        content += "All pairs have been triaged.\n"

    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Saved to {output_file}")


def main():
    """Main execution."""
    print("="*70)
    print("REGENERATE CONSOLIDATION REPORTS")
    print("="*70)
    print()

    try:
        # Load consolidation map
        df = load_consolidation_map()

        # Generate summary
        summary = generate_summary(df)

        print("\nSummary:")
        print(f"  MERGE:         {summary['merge_count']} pairs")
        print(f"  HIERARCHY:     {summary['hierarchy_count']} pairs")
        print(f"  KEEP_SEPARATE: {summary['keep_count']} pairs")
        print(f"  FLAGGED:       {summary['flag_count']} pairs")
        print(f"  TOTAL:         {summary['total_decisions']} decisions")

        # Generate markdown report
        generate_decisions_markdown(df, summary)

        print("\n" + "="*70)
        print("✓ REPORTS REGENERATED")
        print("="*70)

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
