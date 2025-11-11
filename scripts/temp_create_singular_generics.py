#!/usr/bin/env python3
"""
Create singular generic leaf nodes for parent nodes used in tag_application_mapping.csv.

Analyzes which parent nodes are incorrectly used in mappings and creates
appropriate singular generic leaves under those parents.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict

# File paths
BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
TAG_APP_FILE = BASE_DIR / 'data' / 'tag_application_mapping.csv'
BACKUP_TAG_MAP = TAG_MAP_FILE.with_suffix('.csv.backup-add-singular-generics')

# Manual mapping for parent → singular generic leaf
# These define what singular generic to create for each parent node
SINGULAR_GENERIC_MAPPINGS = {
    'death': ('death', 'deaths'),
    'court cases': ('court case', 'court cases'),
    'railway': ('railway facility', 'railway'),
    'mining': ('mine', 'mining'),
    'towns': ('town', 'towns'),
    'licensing': ('licensing case', 'licensing'),
    'retailers and stores': ('retailer or store', 'retailers and stores'),
    'liquor trade': ('liquor trade activity', 'liquor trade'),
    'hotels & hospitality': ('hotel or hospitality venue', 'hotels & hospitality'),
    'postal services': ('postal service', 'postal services'),
    'military': ('military activity', 'military'),
    'accommodation': ('accommodation venue', 'accommodation'),
    'drunkenness': ('drunkenness incident', 'drunkenness'),
    'local councils': ('local council', 'local councils'),
    'swimming': ('swimming activity', 'swimming'),
    'racing': ('race event', 'racing'),
    'sport': ('sporting activity', 'sport'),
    # Place names are special - we'll handle them differently
    'Katoomba': None,  # Place names shouldn't have singular generics
    'Megalong': None,
    'Ruined Castle mining district': None,
}

def load_csv(filepath):
    """Load a CSV file and return rows as list of dicts."""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def get_parent_nodes_used_in_mappings(tag_map_rows, tag_app_rows):
    """
    Identify parent nodes that are incorrectly used in tag_application_mapping.csv.

    Returns dict of {parent_name: {usage_count, children}}
    """
    # First, identify all parent nodes from tag_map
    parent_nodes = {}
    tag_children = defaultdict(list)

    for row in tag_map_rows:
        if row['action'] != 'hierarchy':
            continue

        tag_name = row['new_tag']
        parent = row.get('parent_broader_category', '')

        if parent.startswith('parent='):
            parent_name = parent.replace('parent=', '').strip()
            # Skip thematic groupings and Getty facets
            if ' - THEMATIC' in parent_name or '(Getty AAT primary facet)' in parent_name:
                continue
            tag_children[parent_name].append(tag_name)

    # Identify which are parents (have children)
    for parent, children in tag_children.items():
        if len(children) > 0:
            parent_nodes[parent] = {
                'children': children,
                'usage_count': 0
            }

    # Now count how many times each parent is used in mappings
    for row in tag_app_rows:
        add_tags = row.get('add_tags', '')
        if not add_tags:
            continue

        # Split by comma (tags can be comma-separated)
        for tag in add_tags.split(','):
            tag = tag.strip()
            if tag in parent_nodes:
                parent_nodes[tag]['usage_count'] += 1

    # Filter to only those actually used in mappings
    return {k: v for k, v in parent_nodes.items() if v['usage_count'] > 0}

def create_singular_generic_entries(parent_nodes):
    """
    Create CSV rows for new singular generic leaf nodes.

    Returns list of new rows to add to tag_map_consolidated.csv
    """
    new_rows = []

    for parent_name, data in sorted(parent_nodes.items()):
        if parent_name not in SINGULAR_GENERIC_MAPPINGS:
            print(f"  ⚠ No mapping defined for parent '{parent_name}' - skipping")
            continue

        mapping = SINGULAR_GENERIC_MAPPINGS[parent_name]
        if mapping is None:
            print(f"  ℹ Skipping '{parent_name}' (place name - no singular generic needed)")
            continue

        singular, parent_ref = mapping
        print(f"  + Creating '{singular}' under parent '{parent_ref}'")

        # Check if singular generic already exists
        # (We'll do this check in the main function)

        new_row = {
            'old_tag': singular,
            'new_tag': singular,
            'action': 'hierarchy',
            'parent_broader_category': f'parent={parent_ref}',
            'notes': f'Singular generic term (added for leaf-node tagging pattern compliance)'
        }
        new_rows.append(new_row)

    return new_rows

def check_existing_tags(tag_map_rows, new_rows):
    """Check if any of the new tags already exist."""
    existing_tags = {row['new_tag'] for row in tag_map_rows}
    conflicts = []

    for row in new_rows:
        if row['new_tag'] in existing_tags:
            conflicts.append(row['new_tag'])

    return conflicts

def save_taxonomy(rows, fieldnames):
    """Save the updated taxonomy."""
    # Create backup
    import shutil
    shutil.copy2(TAG_MAP_FILE, BACKUP_TAG_MAP)
    print(f"✓ Backup created: {BACKUP_TAG_MAP}")

    # Write updated data
    with open(TAG_MAP_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated taxonomy saved: {TAG_MAP_FILE}")

def main():
    print("=" * 70)
    print("CREATE SINGULAR GENERIC LEAF NODES")
    print("=" * 70)
    print()

    # Load data
    print("Loading data files...")
    tag_map_rows = load_csv(TAG_MAP_FILE)
    tag_app_rows = load_csv(TAG_APP_FILE)
    print(f"✓ Loaded {len(tag_map_rows)} taxonomy rows")
    print(f"✓ Loaded {len(tag_app_rows)} mapping rows")
    print()

    # Analyze parent node usage
    print("Analyzing parent nodes used in mappings...")
    parent_nodes = get_parent_nodes_used_in_mappings(tag_map_rows, tag_app_rows)
    print(f"✓ Found {len(parent_nodes)} parent nodes used in mappings")
    print()

    # Show analysis
    print("Parent nodes usage breakdown:")
    for parent, data in sorted(parent_nodes.items(), key=lambda x: x[1]['usage_count'], reverse=True):
        print(f"  - '{parent}': {data['usage_count']} uses, {len(data['children'])} children")
    print()

    # Create singular generic entries
    print("Creating singular generic leaf nodes...")
    new_rows = create_singular_generic_entries(parent_nodes)
    print(f"✓ Created {len(new_rows)} new singular generic entries")
    print()

    # Check for conflicts
    print("Checking for existing tags...")
    conflicts = check_existing_tags(tag_map_rows, new_rows)
    if conflicts:
        print(f"✗ Found {len(conflicts)} conflicting tags that already exist:")
        for tag in conflicts:
            print(f"  - {tag}")
        print()
        print("ERROR: Cannot proceed - conflicts found")
        print("These tags already exist. Review manually.")
        sys.exit(1)
    else:
        print("✓ No conflicts - all new tags are unique")
        print()

    # Add new rows to taxonomy
    fieldnames = tag_map_rows[0].keys()
    updated_rows = tag_map_rows + new_rows
    print(f"Adding {len(new_rows)} rows to taxonomy...")
    print(f"  Original rows: {len(tag_map_rows)}")
    print(f"  New rows: {len(new_rows)}")
    print(f"  Total rows: {len(updated_rows)}")
    print()

    # Save
    save_taxonomy(updated_rows, fieldnames)

    print()
    print("=" * 70)
    print("COMPLETE: Singular generic leaf nodes created")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  - Singular generics created: {len(new_rows)}")
    print(f"  - Parent nodes handled: {len([m for m in SINGULAR_GENERIC_MAPPINGS.values() if m is not None])}")
    print(f"  - Place names skipped: {len([m for m in SINGULAR_GENERIC_MAPPINGS.values() if m is None])}")
    print(f"  - Backup saved: {BACKUP_TAG_MAP.name}")
    print()
    print("⚠ NEXT STEP: Run update script to replace parent nodes in tag_application_mapping.csv")
    print()

if __name__ == '__main__':
    main()
