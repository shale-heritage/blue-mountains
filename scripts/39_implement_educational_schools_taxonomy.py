#!/usr/bin/env python3
"""
Implement educational schools dual-nature taxonomy with disambiguation qualifiers.

This script:
1. Removes obsolete unqualified school entries
2. Adds new disambiguated structure (building)/(organisation)
3. Creates synonym mappings for unqualified terms
4. Follows hotel/church model for consistency

Date: 2025-11-14
"""

import csv
from pathlib import Path
from typing import List, Tuple

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
CSV_PATH = DATA_DIR / "tag_map_consolidated.csv"

def read_csv(filepath: Path) -> List[Tuple[str, str, str, str]]:
    """Read CSV file and return as list of tuples."""
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 4:
                rows.append(tuple(row))
    return rows

def write_csv(filepath: Path, rows: List[Tuple[str, str, str, str]]) -> None:
    """Write list of tuples to CSV file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def remove_obsolete_entries(rows: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str, str, str]]:
    """Remove obsolete unqualified school entries."""

    # Entries to remove (exact matches)
    obsolete = {
        ('School', 'School', 'hierarchy', 'parent=Schools'),
        ('school', 'school', 'hierarchy', 'parent=schools'),
        ('School', 'school', 'synonym', 'Capitalized variant from original Zotero tags'),
        ('Katoomba Public School', 'Katoomba Public School', 'hierarchy', 'parent=schools'),
        ('Katoomba Public School', 'Katoomba Public School', 'hierarchy', 'parent=Schools'),
        ('Katoomba Superior Public School', 'Katoomba Superior Public School', 'hierarchy', 'parent=schools'),
        ('Katoomba Superior Public School', 'Katoomba Superior Public School', 'hierarchy', 'parent=Schools'),
        ('Megalong Valley School', 'Megalong Valley School', 'hierarchy', 'parent=schools'),
        ('Megalong Valley School', 'Megalong Valley School', 'hierarchy', 'parent=Schools'),
        ('Mount Victoria School', 'Mount Victoria School', 'hierarchy', 'parent=schools'),
        ('Mount Victoria School', 'Mount Victoria School', 'hierarchy', 'parent=Schools'),
        ('Schools', 'Schools', 'hierarchy', 'parent=Educational buildings'),
        ('schools', 'schools', 'hierarchy', 'parent=educational buildings'),
    }

    filtered = [row for row in rows if row not in obsolete]
    removed_count = len(rows) - len(filtered)
    print(f"✓ Removed {removed_count} obsolete entries")
    return filtered

def add_new_structure(rows: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str, str, str]]:
    """Add new disambiguated structure."""

    new_entries = [
        # Intermediate parents (NEW)
        ('schools (buildings)', 'schools (buildings)', 'hierarchy', 'parent=educational buildings'),
        ('schools (organisations)', 'schools (organisations)', 'hierarchy', 'parent=educational institutions'),

        # Plural parent category (polyhierarchical - for browsing)
        ('Schools', 'Schools', 'hierarchy', 'parent=educational institutions'),
        ('Schools', 'Schools', 'hierarchy', 'parent=educational buildings'),

        # Synonym mappings for unqualified generic terms
        ('School', 'School (organisation)', 'synonym', 'Unqualified variant - most usage is organisational (65.2%)'),
        ('school', 'school (organisation)', 'synonym', 'Lowercase variant - maps to organisation as primary'),

        # Singular generic leaves
        ('School (building)', 'School (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('School (organisation)', 'School (organisation)', 'hierarchy', 'parent=schools (organisations)'),
        ('school (building)', 'school (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('school (organisation)', 'school (organisation)', 'hierarchy', 'parent=schools (organisations)'),

        # Katoomba Public School
        ('Katoomba Public School (building)', 'Katoomba Public School (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('Katoomba Public School (organisation)', 'Katoomba Public School (organisation)', 'hierarchy', 'parent=schools (organisations)'),
        ('Katoomba Public School', 'Katoomba Public School (organisation)', 'synonym', 'Unqualified variant - to be applied based on context analysis'),

        # Katoomba Superior Public School
        ('Katoomba Superior Public School (building)', 'Katoomba Superior Public School (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('Katoomba Superior Public School (organisation)', 'Katoomba Superior Public School (organisation)', 'hierarchy', 'parent=schools (organisations)'),
        ('Katoomba Superior Public School', 'Katoomba Superior Public School (organisation)', 'synonym', 'Unqualified variant - to be applied based on context analysis'),

        # Megalong Valley School
        ('Megalong Valley School (building)', 'Megalong Valley School (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('Megalong Valley School (organisation)', 'Megalong Valley School (organisation)', 'hierarchy', 'parent=schools (organisations)'),
        ('Megalong Valley School', 'Megalong Valley School (organisation)', 'synonym', 'Unqualified variant - insufficient data for classification'),

        # Mount Victoria School
        ('Mount Victoria School (building)', 'Mount Victoria School (building)', 'hierarchy', 'parent=schools (buildings)'),
        ('Mount Victoria School (organisation)', 'Mount Victoria School (organisation)', 'hierarchy', 'parent=schools (organisations)'),
        ('Mount Victoria School', 'Mount Victoria School (organisation)', 'synonym', 'Unqualified variant - insufficient data for classification'),
    ]

    print(f"✓ Adding {len(new_entries)} new entries")
    return rows + new_entries

def main():
    """Main execution."""
    print("Educational Schools Taxonomy Implementation")
    print("=" * 60)

    # Read current CSV
    print(f"\n1. Reading CSV: {CSV_PATH}")
    rows = read_csv(CSV_PATH)
    print(f"   Initial row count: {len(rows)}")

    # Remove obsolete entries
    print("\n2. Removing obsolete unqualified entries...")
    rows = remove_obsolete_entries(rows)
    print(f"   Row count after removal: {len(rows)}")

    # Add new structure
    print("\n3. Adding new disambiguated structure...")
    rows = add_new_structure(rows)
    print(f"   Final row count: {len(rows)}")

    # Write updated CSV
    print(f"\n4. Writing updated CSV: {CSV_PATH}")
    write_csv(CSV_PATH, rows)

    print("\n✅ Taxonomy implementation complete!")
    print("\nNext steps:")
    print("  1. Verify changes: grep -E 'school|School' data/tag_map_consolidated.csv")
    print("  2. Generate item tag application CSV")
    print("  3. Update consolidation decisions log")

if __name__ == "__main__":
    main()
