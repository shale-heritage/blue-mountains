#!/usr/bin/env python3
"""
Add Singular Generic Terms to Taxonomy

For plural categories that have specific named instances as direct children,
add a singular generic term as a sibling. This follows the pattern:

    Hotels (plural category)
    ├── Hotel (singular generic)
    ├── Carrington Hotel (specific instance)
    └── Katoomba Hotel (specific instance)

The singular generic should be a sibling to the specific instances, not their parent.

Author: Claude Code
Date: 2025-10-30
"""

import csv
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

CSV_PATH = Path("data/tag_map_consolidated.csv")
BACKUP_PATH = Path("data/tag_map_consolidated.csv.backup-before-singular-generics")


def load_csv() -> List[dict]:
    """Load CSV data into memory."""
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(rows: List[dict]):
    """Save CSV data back to file."""
    fieldnames = ['new_tag', 'old_tag', 'action', 'notes']
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_hierarchy_map(rows: List[dict]) -> Tuple[Dict[str, List[str]], Set[str]]:
    """
    Build parent->children mapping and identify leaf nodes.

    Returns:
        Tuple of (hierarchies dict, set of leaf nodes)
    """
    hierarchies = defaultdict(list)
    all_parents = set()

    for row in rows:
        if row['action'] == 'hierarchy' and 'THEMATIC' not in row['notes']:
            if 'parent=' in row['notes']:
                # Extract parent name
                parent_part = row['notes'].split('parent=')[1]
                parent = parent_part.split('(')[0].strip()
                parent = parent.replace(' - THEMATIC', '').strip()

                hierarchies[parent].append(row['new_tag'])
                all_parents.add(parent)

    # Identify leaf nodes
    all_children = set()
    for children in hierarchies.values():
        all_children.update(children)

    leaf_nodes = all_children - all_parents

    return hierarchies, leaf_nodes


def calculate_singular(plural: str) -> str:
    """Calculate singular form from plural."""
    if plural.endswith('ies'):
        return plural[:-3] + 'y'
    elif plural.endswith('ches'):
        return plural[:-2]
    elif plural.endswith('ses'):
        return plural[:-2]
    elif plural.endswith('s'):
        return plural[:-1]
    else:
        return plural


def identify_missing_generics(hierarchies: Dict[str, List[str]],
                              leaf_nodes: Set[str]) -> List[Tuple[str, str, List[str]]]:
    """
    Identify plural categories that need singular generics.

    Returns:
        List of (plural_name, singular_name, leaf_children)
    """
    missing = []

    for parent, children in sorted(hierarchies.items()):
        # Check if parent is plural
        if not parent.endswith('s') or len(parent) <= 3:
            continue

        # Calculate singular form
        singular = calculate_singular(parent)

        # Check if ANY direct children are leaf nodes
        leaf_children = [c for c in children if c in leaf_nodes]

        # If has leaf children AND doesn't already have singular generic
        if len(leaf_children) > 0 and singular not in children:
            missing.append((parent, singular, leaf_children))

    return missing


def add_singular_generics():
    """Main function to add all missing singular generics."""
    print("=" * 80)
    print("ADD SINGULAR GENERIC TERMS")
    print("=" * 80)
    print()

    # Create backup
    import shutil
    shutil.copy2(CSV_PATH, BACKUP_PATH)
    print(f"✓ Created backup: {BACKUP_PATH}")
    print()

    # Load data
    print(f"Loading CSV: {CSV_PATH}")
    rows = load_csv()
    original_count = len(rows)
    print(f"✓ Loaded {original_count} rows")
    print()

    # Build hierarchy
    hierarchies, leaf_nodes = build_hierarchy_map(rows)

    # Identify missing generics
    missing = identify_missing_generics(hierarchies, leaf_nodes)

    print(f"Found {len(missing)} categories needing singular generics")
    print("-" * 80)
    print()

    # Create new rows for singular generics
    new_rows = []

    for plural, singular, leaf_children in sorted(missing):
        # Create new CSV row for singular generic
        new_row = {
            'new_tag': singular,
            'old_tag': singular,
            'action': 'hierarchy',
            'notes': f'parent={plural} (singular generic term)'
        }

        new_rows.append(new_row)

        print(f"  + {singular}")
        print(f"    Parent: {plural}")
        print(f"    Siblings: {', '.join(leaf_children[:3])}{' ...' if len(leaf_children) > 3 else ''}")
        print()

    print()
    print(f"Adding {len(new_rows)} singular generic terms...")

    # Add new rows to existing data
    updated_rows = rows + new_rows

    # Save
    save_csv(updated_rows)

    print(f"✓ Saved updated CSV: {CSV_PATH}")
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Original rows:        {original_count}")
    print(f"Singular generics added: {len(new_rows)}")
    print(f"Final rows:           {len(updated_rows)}")
    print(f"Backup location:      {BACKUP_PATH}")
    print()

    print("Examples of additions:")
    print("-" * 80)
    for plural, singular, _ in sorted(missing)[:10]:
        print(f"  {plural} → {singular}")
    print()

    if len(missing) > 10:
        print(f"  ... and {len(missing) - 10} more")
        print()

    print("Next step: Regenerate hierarchy visualizations")
    print()


if __name__ == "__main__":
    add_singular_generics()
