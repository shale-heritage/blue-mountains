#!/usr/bin/env python3
"""
Count Archaeological Records

This script counts non-empty data rows in the archaeology CSV files:
- archaeology/data/input/NG-Entity-Feature.csv
- archaeology/data/input/RC-Entity-Feature.csv

A row is considered non-empty if it contains data beyond just the header.
"""

import csv
from pathlib import Path


def count_csv_rows(filepath):
    """
    Count non-empty data rows in a CSV file.

    Returns:
        tuple: (total_rows, header)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header row

        # Count rows with at least one non-empty field
        count = 0
        for row in reader:
            # Check if row has any non-empty values
            if any(cell.strip() for cell in row):
                count += 1

    return count, header


def main():
    """Count and report archaeology records."""

    base_dir = Path(__file__).parent.parent

    # Define file paths
    ng_file = base_dir / "archaeology" / "data" / "input" / "NG-Entity-Feature.csv"
    rc_file = base_dir / "archaeology" / "data" / "input" / "RC-Entity-Feature.csv"

    print("=" * 70)
    print("ARCHAEOLOGY DATA RECORD COUNT")
    print("=" * 70)
    print()

    # Count NG records
    ng_count, ng_header = count_csv_rows(ng_file)
    print(f"NG-Entity-Feature.csv:")
    print(f"  Data rows (non-empty): {ng_count:,}")
    print(f"  Columns: {len(ng_header)}")
    print()

    # Count RC records
    rc_count, rc_header = count_csv_rows(rc_file)
    print(f"RC-Entity-Feature.csv:")
    print(f"  Data rows (non-empty): {rc_count:,}")
    print(f"  Columns: {len(rc_header)}")
    print()

    print("-" * 70)
    print()

    # Total
    total_count = ng_count + rc_count
    print(f"TOTAL ARCHAEOLOGICAL RECORDS: {total_count:,}")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
