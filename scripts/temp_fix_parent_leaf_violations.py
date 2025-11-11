#!/usr/bin/env python3
"""
Fix parent-leaf violations in taxonomy.

Creates plural parents and restructures hierarchies for tags that currently
act as both leaf nodes (used in mappings) and parent nodes (have children).

Handles specific known cases:
- death → deaths
- court cases (already plural, check structure)
- hotel licensing
- liquor trade
"""

import csv
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
BACKUP_FILE = TAG_MAP_FILE.with_suffix('.csv.backup-fix-parent-leaf')

# Manual fixes for known problematic structures
# Format: {current_parent_tag: (new_plural_parent, note)}
RESTRUCTURING = {
    'death': ('deaths', 'Create plural parent, make death/death notice/suicide siblings'),
    'hotel licensing': ('hotel licensing cases', 'Create specific plural parent'),
    'liquor trade': ('liquor trade activities', 'Create plural parent for trade activities'),
}

def load_taxonomy():
    """Load taxonomy with proper handling of line endings."""
    rows = []
    with open(TAG_MAP_FILE, 'r', encoding='utf-8', newline='') as f:
        # Read and normalize line endings
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')

    import io
    f = io.StringIO(content)
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)
    return rows

def create_new_parents():
    """Create new plural parent entries."""
    new_parents = []
    for old_tag, (new_parent, note) in RESTRUCTURING.items():
        # Create hierarchy entry for new parent under appropriate broader category
        entry = {
            'old_tag': new_parent,
            'new_tag': new_parent,
            'action': 'hierarchy',
            'notes': f'Plural parent node (leaf-node pattern compliance fix) - {note}',
            'parent_broader_category': 'parent=life events',  # Will need to determine correct parent
        }
        new_parents.append(entry)
    return new_parents

def update_children_parents(rows):
    """Update parent references for children of restructured tags."""
    modified = []
    for row in rows:
        parent = row.get('parent_broader_category', '')
        updated = False

        for old_tag, (new_parent, _) in RESTRUCTURING.items():
            if parent == f'parent={old_tag}':
                row['parent_broader_category'] = f'parent={new_parent}'
                row['notes'] = row.get('notes', '') + f' | Parent updated from {old_tag} to {new_parent}'
                updated = True
                modified.append((row['new_tag'], old_tag, new_parent))

        # Also update the problematic tag itself to point to new parent
        if row['new_tag'] in RESTRUCTURING:
            new_parent, _ = RESTRUCTURING[row['new_tag']]
            if row['action'] == 'hierarchy':
                # Keep existing parents but also add new parent
                # Actually, this is complex with polyhierarchy
                # Let's just document for now
                pass

    return rows, modified

def save_taxonomy(rows):
    """Save updated taxonomy."""
    import shutil
    shutil.copy2(TAG_MAP_FILE, BACKUP_FILE)
    print(f"✓ Backup created: {BACKUP_FILE}")

    fieldnames = rows[0].keys() if rows else []
    with open(TAG_MAP_FILE, 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Updated taxonomy saved: {TAG_MAP_FILE}")

def main():
    print("=" * 70)
    print("FIX PARENT-LEAF VIOLATIONS")
    print("=" * 70)
    print()
    print("This script is PAUSED for user review.")
    print()
    print("The issue is complex - tags like 'death' are:")
    print("  1. Valid leaf nodes (used in mappings - which is correct)")
    print("  2. Also act as parents (have children - which violates pattern)")
    print()
    print("Recommended approach:")
    print("  - Manually review the taxonomy structure")
    print("  - User consultation on how to handle polyhierarchical cases")
    print("  - Targeted fixes for highest-impact cases only")
    print()
    print("SKIPPING automatic fixes for now.")
    print("Please review and provide guidance.")

    return

if __name__ == '__main__':
    main()
