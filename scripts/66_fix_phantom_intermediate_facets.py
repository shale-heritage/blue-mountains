#!/usr/bin/env python3
"""
Fix phantom intermediate facet parent references.

Issues found:
1. Police → parent="law enforcement (intermediate facet)" should be "law enforcement"
2. coroners → has duplicate entry with phantom parent (line 184) - should be removed

These phantom parents cause the visualization to show incorrect top-level facets.
"""

import csv
from pathlib import Path
from datetime import datetime

def main():
    csv_file = Path('data/tag_map_consolidated.csv')

    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = csv_file.parent / f'tag_map_consolidated.{timestamp}.bak'

    print('='*80)
    print('FIX PHANTOM INTERMEDIATE FACET REFERENCES')
    print('='*80)
    print()

    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f'Current total rows: {len(rows)}')
    print()

    # Create backup before modification
    print(f'Creating backup: {backup_file.name}')
    with open(csv_file, 'r', encoding='utf-8') as f:
        with open(backup_file, 'w', encoding='utf-8') as bak:
            bak.write(f.read())
    print()

    # Track changes
    fixed_count = 0
    removed_count = 0

    # Fix entries
    cleaned_rows = []
    for row in rows:
        # Fix 1: Police parent reference
        if (row['old_tag'] == 'Police' and
            row['new_tag'] == 'Police' and
            row['action'] == 'hierarchy' and
            'law enforcement (intermediate facet)' in row['notes']):
            print(f'Fixing: Police parent reference')
            print(f'  Old: {row["notes"]}')
            row['notes'] = 'parent=law enforcement'
            print(f'  New: {row["notes"]}')
            fixed_count += 1
            cleaned_rows.append(row)

        # Fix 2: Remove duplicate coroners entry with phantom parent
        elif (row['old_tag'] == 'coroners' and
              row['new_tag'] == 'coroners' and
              row['action'] == 'hierarchy' and
              'legal officials (intermediate facet)' in row['notes']):
            print(f'Removing: coroners duplicate with phantom parent')
            print(f'  Entry: {row["old_tag"]} → {row["new_tag"]} ({row["notes"]})')
            removed_count += 1
            # Don't append - skip this row

        else:
            cleaned_rows.append(row)

    print()

    # Write cleaned CSV
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f'✓ Fixed {fixed_count} parent references')
    print(f'✓ Removed {removed_count} duplicate entries')
    print(f'✓ New total rows: {len(cleaned_rows)}')
    print()

    # Verify phantom parents are gone
    print('Verifying phantom intermediate facets removed:')
    phantom_parents = set()
    for row in cleaned_rows:
        notes = row.get('notes', '')
        if '(intermediate facet)' in notes:
            # Extract parent names that still reference intermediate facet
            import re
            matches = re.findall(r'parent=([^,;]+)', notes)
            for match in matches:
                if '(intermediate facet)' in match:
                    phantom_parents.add(match.strip())

    if phantom_parents:
        print(f'⚠ WARNING: Still {len(phantom_parents)} phantom intermediate facet references:')
        for parent in phantom_parents:
            print(f'  • "{parent}"')
    else:
        print('✓ No phantom intermediate facet references remaining')
    print()

    print('='*80)
    print('COMPLETE')
    print('='*80)
    print(f'Backup: {backup_file}')
    print(f'Fixed: {fixed_count} entries')
    print(f'Removed: {removed_count} duplicate entries')
    print(f'Remaining: {len(cleaned_rows)} active entries')
    print()
    print('Next steps:')
    print('  1. Regenerate hierarchy visualizations (script 23)')
    print('  2. Verify only 8 primary facets appear')
    print('='*80)

if __name__ == '__main__':
    main()
