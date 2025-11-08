#!/usr/bin/env python3
"""Remove ALL capitalized event entries from CSV, regardless of parent capitalization."""

import re

# Event terms that should only appear in lowercase (except proper nouns)
capitalized_event_terms = [
    'Assault', 'Bigamy', 'Desertion', 'Fighting', 'Rape', 'Sexual violence', 'Theft',
    'Concert', 'Corroboree', 'Debate',
    'Bankruptcy', 'Court cases', 'Divorce',
    'Death', 'Death notice', 'Funeral', 'Marriage',
    'Election', 'Petition', 'Public meeting',
    'Strike', 'Mine closure',
    'Ball', 'Dance', 'Flower show',
    'Athletics', 'Billiards', 'Cricket', 'Football', 'Rugby', 'Shooting', 'Tennis',
    'Drunkenness (crime)', 'Serving alcohol to minors', 'Unlicensed sales',
]

# Read and filter - remove any line where first field matches capitalized term
input_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated.csv'
output_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated_filtered.csv'

removed_count = 0
with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Extract first field
            fields = line.strip().split(',')
            if len(fields) >= 3:
                first_field = fields[0]
                third_field = fields[2]

                # Remove if it's a capitalized event term with hierarchy action
                if first_field in capitalized_event_terms and third_field == 'hierarchy':
                    removed_count += 1
                    print(f"Removing: {line.strip()}")
                else:
                    outfile.write(line)
            else:
                outfile.write(line)

print(f"\nTotal entries removed: {removed_count}")
print(f"Output written to: {output_file}")
