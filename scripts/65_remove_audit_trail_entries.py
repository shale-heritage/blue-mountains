#!/usr/bin/env python3
"""
Remove audit trail entries that are causing phantom facets in visualizations.

These entries (status=removed) were useful for documenting corrections,
but now cause confusion by creating phantom parent references in hierarchy trees.

Affected entries:
- trucking (8 removed entries referencing phantom Transport/Commercial transport parents)
- bankruptcy (3 removed entries referencing phantom Economic distress parents)
- Cottage, public house (2 removed entries referencing phantom Cottages/Public houses parents)
- 3 synonym corrections (Constable, St Hilda's Church variants)

Total: 13 removed entries to be deleted
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
    print('REMOVE AUDIT TRAIL ENTRIES (status=removed)')
    print('='*80)
    print()

    # Read CSV
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f'Current total rows: {len(rows)}')
    print()

    # Find removed entries
    removed_entries = [r for r in rows if r.get('status') == 'removed']
    active_entries = [r for r in rows if r.get('status') != 'removed']

    print(f'Found {len(removed_entries)} entries with status=removed:')
    for entry in removed_entries:
        print(f'  • {entry["old_tag"]} → {entry["new_tag"]} ({entry["action"]})')
    print()

    # Create backup before modification
    print(f'Creating backup: {backup_file.name}')
    with open(csv_file, 'r', encoding='utf-8') as f:
        with open(backup_file, 'w', encoding='utf-8') as bak:
            bak.write(f.read())
    print()

    # Write cleaned CSV (only active entries)
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(active_entries)

    print(f'✓ Removed {len(removed_entries)} audit trail entries')
    print(f'✓ New total rows: {len(active_entries)}')
    print()

    # Verify phantom parents are gone
    print('Verifying phantom parent references removed:')
    phantom_parents = set()
    for entry in active_entries:
        notes = entry.get('notes', '')
        if 'REMOVED by script' in notes:
            # Extract parent names that still reference removed nodes
            import re
            matches = re.findall(r'parent=([^,;]+)', notes)
            for match in matches:
                if 'REMOVED' in match:
                    phantom_parents.add(match.strip())

    if phantom_parents:
        print(f'⚠ WARNING: Still {len(phantom_parents)} phantom parent references found:')
        for parent in phantom_parents:
            print(f'  • "{parent}"')
    else:
        print('✓ No phantom parent references remaining')
    print()

    print('='*80)
    print('COMPLETE')
    print('='*80)
    print(f'Backup: {backup_file}')
    print(f'Removed: {len(removed_entries)} audit trail entries')
    print(f'Remaining: {len(active_entries)} active entries')
    print()
    print('Next steps:')
    print('  1. Regenerate hierarchy visualizations (script 23)')
    print('  2. Verify phantom facets are gone')
    print('='*80)

if __name__ == '__main__':
    main()
