#!/usr/bin/env python3
"""
Comprehensive fix for all 28 orphaned tags in tag_application_mapping.csv
and corresponding taxonomy additions to tag_map_consolidated.csv.

Fixes:
1. All (organization) → (organisation) spelling
2. Whisky → whisky
3. Building tags → specific tags per user guidance
4. Police Court → Courts of Petty Sessions
5. Ruined Castle → Ruined Castle - rock formation (for unqualified usage)
6. sexual assault → sexual violence
7. inquest → inquest (add to taxonomy)
8. Person name consolidations and additions
9. Remove malformed entries
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path


def backup_file(filepath):
    """Create timestamped backup."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = f"{filepath}.backup-orphaned-fix-{timestamp}"
    shutil.copy2(filepath, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path


def add_taxonomy_entries(taxonomy_path):
    """Add new taxonomy entries."""

    # Read existing taxonomy
    with open(taxonomy_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    new_entries = [
        # Institutional buildings and healthcare facilities hierarchy
        ('institutional buildings', 'institutional buildings', 'hierarchy',
         'parent=Built Environment', ''),
        ('healthcare facilities', 'healthcare facilities', 'hierarchy',
         'parent=institutional buildings', ''),
        ('sanatoriums', 'sanatoriums', 'hierarchy',
         'parent=healthcare facilities', ''),
        ('sanatorium', 'sanatorium', 'hierarchy',
         'parent=sanatoriums', 'Singular generic term'),

        # Odd Fellows' Hall
        ("Odd Fellows' Hall", "Odd Fellows' Hall", 'hierarchy',
         'parent=halls', ''),

        # Courts of Petty Sessions
        ('Courts of Petty Sessions', 'Courts of Petty Sessions', 'hierarchy',
         'parent=courts', ''),
        ('Police Court', 'Courts of Petty Sessions', 'synonym',
         'Colloquial term for Courts of Petty Sessions in NSW ca. 1900', ''),

        # Inquests
        ('inquests', 'inquests', 'hierarchy',
         'parent=legal events', ''),
        ('inquests', 'inquests', 'hierarchy',
         'parent=legal proceedings', 'Polyhierarchical like court cases'),
        ('inquest', 'inquest', 'hierarchy',
         'parent=inquests', 'Singular generic term'),

        # Senior-Constable Tomkins
        ('Senior-Constable Tomkins', 'Senior-Constable Tomkins', 'hierarchy',
         'parent=senior-constable', ''),
        ('Senior-Constable Tomkins', 'Senior-Constable Tomkins', 'hierarchy',
         'parent=people - THEMATIC', ''),

        # Update Illingworth to include first name
        ('Senior-Constable John Illingworth', 'Senior-Constable John Illingworth',
         'hierarchy', 'parent=senior-constable', ''),
        ('Senior-Constable John Illingworth', 'Senior-Constable John Illingworth',
         'hierarchy', 'parent=people - THEMATIC', ''),
        ('Senior-Constable Illingworth', 'Senior-Constable John Illingworth',
         'synonym', 'Short form without first name', ''),
        ('Constable John Illingworth', 'Senior-Constable John Illingworth',
         'synonym', 'Incorrect rank - use Senior-Constable', ''),

        # Joseph Nimmo consolidation (already exists as Mr Joseph Nimmo under named persons)
        # Just add synonyms for variants
        ('Mr J Nimmo', 'Mr Joseph Nimmo', 'synonym',
         'Abbreviated first name variant', ''),
        ('Mr Joe Nimmo', 'Mr Joseph Nimmo', 'synonym',
         'Informal first name variant', ''),

        # Mr J. Hudson (with dot) synonym
        ('Mr J. Hudson', 'Mr J Hudson', 'synonym',
         'Punctuated form - use minimal punctuation', ''),

        # sexual assault synonym
        ('sexual assault', 'sexual violence', 'synonym',
         'Use sexual violence as preferred term', ''),

        # miners' dwelling singular
        ("miners' dwelling", "miners' dwelling", 'hierarchy',
         "parent=miners' dwellings", 'Singular generic term'),
    ]

    # Remove old Illingworth entries (will be replaced)
    rows = [r for r in rows if r['old_tag'] != 'Senior-Constable Illingworth']

    # Remove duplicate Joseph Nimmo entries under hotelliers (consolidating to named persons)
    nimmo_hotellier_variants = ['Mr J Nimmo', 'Mr J. Nimmo', 'Mr Joe Nimmo']
    rows = [r for r in rows if not (r['old_tag'] in nimmo_hotellier_variants
                                     and 'parent=hotelliers' in r.get('notes', ''))]

    # Add new entries
    for old_tag, new_tag, action, notes, parent in new_entries:
        rows.append({
            'old_tag': old_tag,
            'new_tag': new_tag,
            'action': action,
            'notes': notes,
            'parent_broader_category': parent
        })

    # Write back
    with open(taxonomy_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['old_tag', 'new_tag', 'action',
                                                 'notes', 'parent_broader_category'])
        writer.writeheader()
        writer.writerows(rows)

    return len(new_entries)


def fix_mapping_tags(mapping_path):
    """Fix all orphaned tags in mapping file."""

    # Read mapping
    with open(mapping_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    fixes_count = {
        'organization_spelling': 0,
        'whisky_case': 0,
        'building_tags': 0,
        'police_court': 0,
        'ruined_castle': 0,
        'sexual_assault': 0,
        'inquest_case': 0,
        'person_names': 0,
        'malformed_removed': 0,
    }

    # Define specific items for building tag fixes
    building_fixes = {
        ('Mountain Mixtures.', '21 October 1892'): {
            'remove': ['building'],
            'add': ['sanatorium']
        },
        ('Katoomba.', '7 January 1888'): {
            'remove': ['building'],
            'add': []
        },
        ('Katoomba.', '29 September 1888'): {
            'remove': ['building'],
            'add': ["Odd Fellows' Hall"]
        },
        ('Katoomba Athletic Sports.', '12 December 1885'): {
            'remove': ['building'],
            'add': []
        },
        ('Katoomba.', '14 July 1888'): {
            'remove': ['building'],
            'add': ['dwelling', "miners' dwelling", "Odd Fellows' Hall"]
        },
    }

    for row in rows:
        original_tags = row['add_tags']
        tags = [t.strip() for t in row['add_tags'].split('|')] if row['add_tags'] else []
        modified = False

        # Fix (organization) → (organisation)
        tags = [t.replace('(organization)', '(organisation)') for t in tags]
        if '(organization)' in original_tags:
            fixes_count['organization_spelling'] += 1
            modified = True

        # Fix Whisky → whisky
        tags = [t.replace('Whisky', 'whisky') if t == 'Whisky' else t for t in tags]
        if 'Whisky' in original_tags:
            fixes_count['whisky_case'] += 1
            modified = True

        # Fix Police Court → Courts of Petty Sessions
        tags = ['Courts of Petty Sessions' if t == 'Police Court' else t for t in tags]
        if 'Police Court' in original_tags:
            fixes_count['police_court'] += 1
            modified = True

        # Fix Ruined Castle → Ruined Castle - rock formation (unqualified only)
        tags = ['Ruined Castle - rock formation'
                if t == 'Ruined Castle'
                and 'Ruined Castle (settlement)' not in tags
                and 'Ruined Castle Shale Mine (site)' not in tags
                else t for t in tags]
        if 'Ruined Castle' in original_tags and 'Ruined Castle (settlement)' not in original_tags:
            fixes_count['ruined_castle'] += 1
            modified = True

        # Fix sexual assault → sexual violence
        tags = ['sexual violence' if t == 'sexual assault' else t for t in tags]
        if 'sexual assault' in original_tags:
            fixes_count['sexual_assault'] += 1
            modified = True

        # Fix inquest (lowercase) - keep lowercase, it's now in taxonomy
        # No change needed, just note it
        if 'inquest' in tags:
            fixes_count['inquest_case'] += 1

        # Fix person names
        nimmo_variants = ['Mr J Nimmo', 'Mr J. Nimmo', 'Mr Joe Nimmo']
        for variant in nimmo_variants:
            if variant in tags:
                tags = ['Mr Joseph Nimmo' if t == variant else t for t in tags]
                fixes_count['person_names'] += 1
                modified = True

        tags = ['Senior-Constable John Illingworth'
                if t in ['Senior-Constable Illingworth', 'Constable John Illingworth']
                else t for t in tags]
        if any(x in original_tags for x in ['Senior-Constable Illingworth', 'Constable John Illingworth']):
            fixes_count['person_names'] += 1
            modified = True

        # Fix Mr J. Hudson → Mr J Hudson
        tags = ['Mr J Hudson' if t == 'Mr J. Hudson' else t for t in tags]
        if 'Mr J. Hudson' in original_tags:
            fixes_count['person_names'] += 1
            modified = True

        # Remove malformed entries
        malformed = [
            'Hotel licensing Please',
            '[name of hotellier]',
            'Hotel (not only here but in all instances)',
        ]
        original_len = len(tags)
        tags = [t for t in tags if t not in malformed]
        if len(tags) < original_len:
            fixes_count['malformed_removed'] += original_len - len(tags)
            modified = True

        # Handle specific building tag fixes
        item_key = (row['title'], row['date'])
        if item_key in building_fixes:
            fix_spec = building_fixes[item_key]
            # Remove specified tags
            for tag_to_remove in fix_spec['remove']:
                if tag_to_remove in tags:
                    tags.remove(tag_to_remove)
                    fixes_count['building_tags'] += 1
                    modified = True
            # Add specified tags
            for tag_to_add in fix_spec['add']:
                if tag_to_add not in tags:
                    tags.append(tag_to_add)
                    modified = True

        # Update row if modified
        if modified:
            row['add_tags'] = ' | '.join(tags) if tags else ''

    # Write back
    with open(mapping_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return fixes_count


def main():
    taxonomy_path = Path('data/tag_map_consolidated.csv')
    mapping_path = Path('data/tag_application_mapping.csv')

    print("="*80)
    print("COMPREHENSIVE ORPHANED TAGS FIX")
    print("="*80)
    print()

    # Backup files
    print("Creating backups...")
    backup_file(taxonomy_path)
    backup_file(mapping_path)
    print()

    # Add taxonomy entries
    print("Adding taxonomy entries...")
    entries_added = add_taxonomy_entries(taxonomy_path)
    print(f"✓ Added {entries_added} new taxonomy entries")
    print()

    # Fix mapping tags
    print("Fixing mapping tags...")
    fixes = fix_mapping_tags(mapping_path)
    print(f"✓ Fixed {fixes['organization_spelling']} (organization) → (organisation)")
    print(f"✓ Fixed {fixes['whisky_case']} Whisky → whisky")
    print(f"✓ Fixed {fixes['building_tags']} building tags")
    print(f"✓ Fixed {fixes['police_court']} Police Court → Courts of Petty Sessions")
    print(f"✓ Fixed {fixes['ruined_castle']} Ruined Castle → rock formation")
    print(f"✓ Fixed {fixes['sexual_assault']} sexual assault → sexual violence")
    print(f"✓ Noted {fixes['inquest_case']} inquest tags (now in taxonomy)")
    print(f"✓ Fixed {fixes['person_names']} person name variations")
    print(f"✓ Removed {fixes['malformed_removed']} malformed entries")
    print()

    total_fixes = sum(fixes.values())
    print(f"Total fixes applied: {total_fixes}")
    print()
    print("✓ All orphaned tags fixed!")


if __name__ == '__main__':
    main()
