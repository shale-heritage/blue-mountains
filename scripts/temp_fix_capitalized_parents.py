#!/usr/bin/env python3
"""Fix capitalized parent references in CSV."""

replacements = [
    ('parent=Accident', 'parent=accidents'),
    ('parent=Animals', 'parent=animals'),
    ('parent=Organizations', 'parent=organisations'),
    ('parent=Criminal events', 'parent=criminal events'),
    ('parent=Historical events', 'parent=historical events'),
]

input_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated.csv'
output_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated_fixed.csv'

count_by_replacement = {old: 0 for old, _ in replacements}

with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            modified_line = line
            for old, new in replacements:
                if old in modified_line:
                    count_by_replacement[old] += 1
                    modified_line = modified_line.replace(old, new)
                    print(f"Replaced '{old}' with '{new}' in: {line.strip()}")
            outfile.write(modified_line)

print("\nSummary:")
for old, count in count_by_replacement.items():
    if count > 0:
        print(f"  {old}: {count} replacements")

print(f"\nOutput written to: {output_file}")
