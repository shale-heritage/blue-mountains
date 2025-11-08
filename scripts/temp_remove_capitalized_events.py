#!/usr/bin/env python3
"""Temporary script to remove capitalized event entries from CSV."""

import csv

# Entries to remove (exact matches)
entries_to_remove = [
    "Assault,Assault,hierarchy,parent=Criminal events",
    "Bigamy,Bigamy,hierarchy,parent=Criminal events",
    "Desertion,Desertion,hierarchy,parent=Criminal events",
    "Fighting,Fighting,hierarchy,parent=Criminal events",
    "Rape,Rape,hierarchy,parent=Criminal events",
    "Sexual violence,Sexual violence,hierarchy,parent=Criminal events",
    "Theft,Theft,hierarchy,parent=Criminal events",
    "Concert,Concert,hierarchy,parent=Cultural events",
    "Corroboree,Corroboree,hierarchy,parent=Cultural events",
    "Debate,Debate,hierarchy,parent=Cultural events",
    "Bankruptcy,Bankruptcy,hierarchy,parent=legal events",
    "Court cases,Court cases,hierarchy,parent=legal events",
    "Divorce,Divorce,hierarchy,parent=legal events",
    "Death,Death,hierarchy,parent=life events",
    "Death notice,Death notice,hierarchy,parent=Death",
    "Funeral,Funeral,hierarchy,parent=life events",
    "Marriage,Marriage,hierarchy,parent=life events",
    "Election,Election,hierarchy,parent=political events",
    "Petition,Petition,hierarchy,parent=political events",
    "Public meeting,Public meeting,hierarchy,parent=political events",
    "Strike,Strike,hierarchy,parent=economic events",
    "Mine closure,Mine closure,hierarchy,parent=Economic events",
    "Ball,Ball,hierarchy,parent=social events",
    "Dance,Dance,hierarchy,parent=social events",
    "Flower show,Flower show,hierarchy,parent=social events",
    "Athletics,Athletics,hierarchy,parent=sporting events",
    "Billiards,Billiards,hierarchy,parent=sporting events",
    "Cricket,Cricket,hierarchy,parent=sporting events",
    "Football,Football,hierarchy,parent=sporting events",
    "Rugby,Rugby,hierarchy,parent=sporting events",
    "Shooting,Shooting,hierarchy,parent=sporting events",
    "Tennis,Tennis,hierarchy,parent=sporting events",
    "Drunkenness (crime),Drunkenness (crime),hierarchy,parent=alcohol-related",
    "Serving alcohol to minors,Serving alcohol to minors,hierarchy,parent=alcohol-related",
    "Unlicensed sales,Unlicensed sales,hierarchy,parent=alcohol-related",
]

# Read and filter
input_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated.csv'
output_file = '/home/shawn/Code/blue-mountains/data/tag_map_consolidated_filtered.csv'

removed_count = 0
with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Check if this line matches any entry to remove
            line_stripped = line.strip()
            if line_stripped in entries_to_remove:
                removed_count += 1
                print(f"Removing: {line_stripped}")
            else:
                outfile.write(line)

print(f"\nTotal entries removed: {removed_count}")
print(f"Output written to: {output_file}")
