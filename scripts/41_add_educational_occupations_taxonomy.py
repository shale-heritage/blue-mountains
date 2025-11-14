#!/usr/bin/env python3
"""
Add educational occupations hierarchy to taxonomy.

This script adds:
- Educational occupations (intermediate parent under Occupations)
- School teachers (intermediate parent under Educational occupations)
- School teacher (singular generic leaf)

Date: 2025-11-14
Context: Identified during manual review of educational schools items
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

def add_educational_occupations(rows: List[Tuple[str, str, str, str]]) -> List[Tuple[str, str, str, str]]:
    """Add educational occupations hierarchy."""

    new_entries = [
        # Educational occupations (intermediate parent)
        ('Educational occupations', 'Educational occupations', 'hierarchy', 'parent=Occupations'),
        ('educational occupations', 'educational occupations', 'hierarchy', 'parent=occupations'),

        # School teachers (intermediate parent)
        ('School teachers', 'School teachers', 'hierarchy', 'parent=Educational occupations'),
        ('school teachers', 'school teachers', 'hierarchy', 'parent=educational occupations'),

        # School teacher (singular generic leaf)
        ('School teacher', 'School teacher', 'hierarchy', 'parent=School teachers'),
        ('school teacher', 'school teacher', 'hierarchy', 'parent=school teachers'),

        # Specific named school teacher
        ('Mr W Chapman', 'Mr W Chapman', 'hierarchy', 'parent=School teachers'),
    ]

    print(f"✓ Adding {len(new_entries)} new entries for educational occupations")

    for entry in new_entries:
        print(f"  + {entry[0]} → {entry[3]}")

    return rows + new_entries

def main():
    """Main execution."""
    print("Educational Occupations Taxonomy Addition")
    print("=" * 60)

    # Read current CSV
    print(f"\n1. Reading CSV: {CSV_PATH}")
    rows = read_csv(CSV_PATH)
    print(f"   Initial row count: {len(rows)}")

    # Add educational occupations hierarchy
    print("\n2. Adding educational occupations hierarchy...")
    rows = add_educational_occupations(rows)
    print(f"   Final row count: {len(rows)}")

    # Write updated CSV
    print(f"\n3. Writing updated CSV: {CSV_PATH}")
    write_csv(CSV_PATH, rows)

    print("\n✅ Taxonomy addition complete!")
    print("\nNew hierarchy structure:")
    print("  Agents > People > Occupations")
    print("    └── Educational occupations")
    print("        └── School teachers")
    print("            ├── School teacher (singular generic)")
    print("            └── Mr W Chapman (specific person)")
    print("\nNext steps:")
    print("  1. Verify structure: grep -E 'educational occupation|school teacher|Chapman' data/tag_map_consolidated.csv")
    print("  2. Apply 'Mr W Chapman' tag to Megalong Matters (1892-09-09)")
    print("  3. Remove 'Megalong Valley School' tag from that item (it's about the teacher, not the school)")

if __name__ == "__main__":
    main()
