#!/usr/bin/env python3
"""
Generate tag application mapping entries for all 83 items in ambiguous tags decision report.
Based on user's decisions and Trove context analysis.
"""

import csv
from pathlib import Path

# Tag mappings for all 83 items
# Format: (item_id, title, date, publication, remove_tags, add_tags, notes)

POLICE_ITEMS = [
    ("1.1", "A Charge of Rape.", "6 September 1890", "Nepean Times", "Police", "Penrith Police Court", "Item 1.1 - Police Court"),
    ("1.2", "News in Brief", "9 October 1903", "Mountaineer", "Police", "police officer", "Item 1.2 - generic police officer"),
    ("1.3", "Jottings.", "23 May 1891", "Katoomba Times", "Police", "police officer", "Item 1.3 - generic police officer"),
    ("1.4", "Mountain Mixtures.", "23 June 1893", "Katoomba Times", "Police", "police officer | New South Wales Police", "Item 1.4 - both generic and organization"),
    ("1.5", "Local Jottings.", "21 September 1889", "Katoomba Times", "Police", "police officer | New South Wales Police", "Item 1.5 - both generic and organization"),
    ("1.6", "To-Day's Further Court Proceedings", "1 December 1932", "Lithgow Mercury", "Police", "police officer | New South Wales Police", "Item 1.6 - both generic and organization"),
    ("1.7", "Bigamy.", "4 August 1909", "New South Wales Police Gazette and Weekly Record of Crime", "Police", "Senior-constable Tomkins | New South Wales Police | Helensburgh", "Item 1.7 - named officer, organization, and town"),
    ("1.8", "Missing Friends.", "9 June 1909", "New South Wales Police Gazette and Weekly Record of Crime", "Police", "New South Wales Police", "Item 1.8 - organization"),
    ("1.9", "Town Talk.", "2 October 1903", "Blue Mountain Gazette", "Police", "Police Court", "Item 1.9 - Police Court"),
    ("1.10", "Katoomba Police Court", "13 December 1895", "Mountaineer", "Police", "Senior-Constable Illingworth | police officer | New South Wales Police | Police Court", "Item 1.10 - named officer, generic, organization, and court"),
    ("1.11", "Megalong Valley.", "15 September 1893", "Katoomba Times", "Police", "police officer", "Item 1.11 - generic police officer"),
    ("1.12", "Katoomba Court.", "16 June 1893", "Katoomba Times", "Police", "Constable John Illingworth | New South Wales Police", "Item 1.12 - named officer and organization"),
    ("1.13", "Mountain Mixtures.", "14 April 1893", "Katoomba Times", "Police", "police officer | Megalong", "Item 1.13 - generic officer and town"),
    ("1.14", "Mountain Mixtures.", "3 March 1893", "Katoomba Times", "Police", "police officer | Megalong", "Item 1.14 - generic officer and town"),
    ("1.15", "Mountain Mixtures.", "25 November 1892", "Katoomba Times", "Police", "police quarters | Katoomba", "Item 1.15 - police quarters building and town"),
    ("1.16", "Katoomba Police Court.", "5 November 1892", "Nepean Times", "Police", "Police Court", "Item 1.16 - Police Court"),
    ("1.17", "Katoomba Court.", "14 October 1892", "Katoomba Times", "Police", "New South Wales Police", "Item 1.17 - organization"),
    ("1.18", "Katoomba Police Court.", "26 March 1892", "Nepean Times", "Police", "police officer | New South Wales Police", "Item 1.18 - generic and organization"),
    ("1.19", "Mountain Mixtures.", "11 March 1892", "Katoomba Times", "Police", "police officer | Blackheath", "Item 1.19 - generic officer and town"),
    ("1.20", "Katoomba Miners' Strike.", "3 August 1887", "Evening News", "Police", "police officer | New South Wales Police", "Item 1.20 - generic and organization"),
    ("1.21", "Katoomba Miners' Strike.", "1 August 1887", "Evening News", "Police", "New South Wales Police | Penrith", "Item 1.21 - organization and town"),
    ("1.22", "Katoomba Court.", "17 March 1893", "Katoomba Times", "Police", "Constable John Illingworth", "Item 1.22 - named officer"),
    ("1.23", "Katoomba Court.", "2 June 1893", "Katoomba Times", "Police", "police officer", "Item 1.23 - generic police officer"),
    ("1.24", "Katoomba News.", "29 June 1895", "Nepean Times", "Police", "Police Court", "Item 1.24 - Police Court"),
    ("1.25", "Notice of Application for a Conditional Publican's Licence", "9 June 1893", "Katoomba Times", "Police", "police station | Katoomba", "Item 1.25 - police station and town"),
    ("1.26", "Megalong Valley.", "23 June 1893", "", "Police", "police officer | New South Wales Police", "Item 1.26 - generic and organization"),
    ("1.27", "Megalong Notes.", "2 May 1902", "Mountaineer", "Police", "police officer | Katoomba", "Item 1.27 - generic officer and town"),
]

NELLIES_GLEN_ITEMS = [
    ("2.1", "NARROW ESCAPE OF SHALE STACK.", "6 January 1905", "Daily Telegraph", "Nellie's Glen", "Nellie's Glen Shale Mine | mining accident", "Item 2.1 - shale mine and accident"),
    ("2.2", "Mountain Mixtures.", "9 September 1892", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (settlement)", "Item 2.2 - settlement (mining township)"),
    ("2.3", "Town Talk.", "13 March 1903", "Blue Mountain Gazette", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen Road", "Item 2.3 - gully/road travel"),
    ("2.4", "The Rockley Game.", "7 February 1896", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen (settlement)", "Item 2.4 - both gully and settlement"),
    ("2.5", "Mountain Mixtures.", "4 December 1891", "Katoomba Times", "Nellie's Glen", "Nellie's Glen Shale Mine", "Item 2.5 - shale mine"),
    ("2.6", "Megalong Matters.", "5 June 1896", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully)", "Item 2.6 - gully (approach for stock)"),
    ("2.7", "Local Jottings.", "25 May 1889", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen Road | Nellie's Glen Shale Mine", "Item 2.7 - gully, road, and mine"),
    ("2.8", "John Britty North.", "6 March 1909", "Blue Mountain Echo", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen Shale Mine | Nellie's Glen (settlement) | Nellie's Glen Road", "Item 2.8 - comprehensive (gully named after daughter, mines, settlement, roads)"),
    ("2.9", "A Public Meeting.", "13 January 1905", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully)", "Item 2.9 - gully (geographic area affected by bushfire)"),
    ("2.10", "St Joseph's New Church, Megalong", "17 March 1905", "Mountaineer", "Nellie's Glen", "Nellie's Glen (settlement) | Nellie's Glen (gully)", "Item 2.10 - settlement and gully (foot of glen near hotel)"),
    ("2.11", "Work at the Mines.", "17 April 1903", "Blue Mountain Gazette", "Nellie's Glen", "Nellie's Glen Shale Mine", "Item 2.11 - the Glen = Nellie's Glen Shale Mine"),
    ("2.12", "The Katoomba Mines.", "20 March 1903", "Blue Mountain Gazette", "Nellie's Glen", "Nellie's Glen Shale Mine", "Item 2.12 - the Glen = Nellie's Glen Shale Mine"),
    ("2.13", "Narrow Neck.", "27 December 1901", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully)", "Item 2.13 - gully (creek/watercourse)"),
    ("2.14", "Brevities.", "6 April 1894", "Evening News", "Nellie's Glen", "Nellie's Glen (settlement)", "Item 2.14 - settlement (mining township with unemployment)"),
    ("2.15", "Mountain Mixtures.", "29 December 1893", "Katoomba Times", "Nellie's Glen", "Nellie's Glen Shale Mine", "Item 2.15 - shale mine"),
    ("2.16", "Megalong Mines.", "1 September 1893", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (settlement) | Nellie's Glen (gully)", "Item 2.16 - settlement and gully"),
    ("2.17", "Mountain Mixtures.", "25 November 1892", "Katoomba Times", "Nellie's Glen", "Nellie's Glen Shale Mine", "Item 2.17 - shale mine (accident at)"),
    ("2.18", "Katoomba Court.", "14 October 1892", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (settlement)", "Item 2.18 - settlement (sly grog shop, residents)"),
    ("2.19", "Accident in Nellie's Glen.", "27 July 1889", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (settlement)", "Item 2.19 - settlement (resident's home)"),
    ("2.20", "Katoomba Court.", "4 November 1892", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (settlement)", "Item 2.20 - settlement (multiple residents)"),
    ("2.21", "Megalong Matters.", "9 September 1892", "Katoomba Times", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen Road", "Item 2.21 - gully and road (trip via)"),
    ("2.22", "Megalong Matters.", "10 January 1896", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen Road", "Item 2.22 - gully and road (horsemen via)"),
    ("2.23", "Megalong Valley.", "1 September 1893", "Katoomba Times", "Nellie's Glen", "", "Item 2.23 - REMOVE TAG (no mention found)"),
    ("2.24", "The Megalong Hotel", "21 September 1894", "Mountaineer", "Nellie's Glen", "Nellie's Glen (gully) | Nellie's Glen (settlement)", "Item 2.24 - gully and settlement (hotel at foot of)"),
    ("2.25", "Tourist Sketch Map showing pathways at Nelly's Glen or Megalong Pass", "1909", "", "Nellie's Glen", "Nellie's Glen (gully)", "Item 2.25 - gully (map feature)"),
]

HARTLEY_VALE_ITEMS = [
    ("3.1", "Town Talk.", "13 May 1904", "Blue Mountain Gazette", "Hartley Vale", "", "Item 3.1 - REMOVE TAG (only Hartley electoral, not Hartley Vale)"),
    ("3.2", "Social at Hartley Vale.", "23 September 1898", "Lithgow Mercury", "Hartley Vale", "Hartley Vale | Hartley Vale Natives Football Club", "Item 3.2 - settlement and football club"),
    ("3.3", "Mountain Mixtures.", "4 December 1891", "Katoomba Times", "Hartley Vale", "Hartley Vale | Hartley Vale mines", "Item 3.3 - settlement and mines"),
    ("3.4", "Hartley Vale.", "13 February 1911", "Lithgow Mercury", "Hartley Vale", "Hartley Vale Cricket Club", "Item 3.4 - cricket club"),
    ("3.5", "Mountain Mixtures.", "22 January 1892", "Katoomba Times", "Hartley Vale", "Hartley Vale mines", "Item 3.5 - mines"),
    ("3.6", "Footballers' Social at Hartley Vale.", "20 October 1899", "Lithgow Mercury", "Hartley Vale", "Hartley Vale | Hartley Vale Natives Football Club", "Item 3.6 - settlement and football club"),
    ("3.7", "Mountain Mixtures.", "29 April 1892", "Katoomba Times", "Hartley Vale", "Hartley Vale | police station", "Item 3.7 - settlement and police station"),
    ("3.8", "The Passing of a Mountaineer. Vale! Joseph Nimmo.", "23 March 1917", "Blue Mountain Echo", "Hartley Vale", "Hartley Vale", "Item 3.8 - town (revised per user's earlier decision)"),
    ("3.9", "Mountain Mixtures.", "4 May 1894", "Katoomba Times", "Hartley Vale", "", "Item 3.9 - REMOVE TAG (only Hartley electoral, not Hartley Vale)"),
    ("3.10", "Kembla Disaster Survivor: Death of Mr. J. J. Meredith", "25 November 1940", "Lithgow Mercury", "Hartley Vale", "Hartley Vale Shale Mine | Hermitage Coal Mine", "Item 3.10 - Hartley Vale Shale Mine (Hermitage already exists)"),
    ("3.11", "West Wallsend.", "10 October 1911", "Newcastle Morning Herald and Miners' Advocate", "Hartley Vale", "Hartley Vale", "Item 3.11 - town (birthplace)"),
    ("3.12", "Mining.", "15 June 1897", "Evening News", "Hartley Vale", "Hartley Vale Shale Mine", "Item 3.12 - shale mine"),
    ("3.13", "Mining.", "25 August 1896", "Evening News", "Hartley Vale", "Hartley Vale Shale Mine", "Item 3.13 - shale mine"),
    ("3.14", "Mining.", "19 May 1896", "Evening News", "Hartley Vale", "Hartley Vale mines | Hartley Vale Shale Mine", "Item 3.14 - both mines (generic) and specific mine"),
    ("3.15", "The Gold Fields.", "21 April 1896", "Evening News", "Hartley Vale", "Hartley Vale Shale Mine | Hartley Vale mines | Hartley Vale", "Item 3.15 - shale mine, mines, and town"),
    ("3.16", "Mountain Mixtures.", "10 February 1893", "Katoomba Times", "Hartley Vale", "", "Item 3.16 - REMOVE TAG (only Hartley electoral, not Hartley Vale)"),
    ("3.17", "Mountain Mixtures.", "17 June 1892", "Katoomba Times", "Hartley Vale", "", "Item 3.17 - REMOVE TAG (only Hartley's Members, not Hartley Vale)"),
    ("3.18", "Hartley Vale.", "16 October 1891", "Katoomba Times", "Hartley Vale", "Hartley Vale Natives Football Club | Hartley Vale", "Item 3.18 - football club and town"),
    ("3.19", "Hartley Vale.", "2 February 1900", "Lithgow Mercury", "Hartley Vale", "Hartley Vale", "Item 3.19 - town (confirmed via Trove)"),
    ("3.20", "Notice of Application for a Conditional Publican's Licence", "9 June 1893", "Katoomba Times", "Hartley Vale", "Hartley Vale", "Item 3.20 - town"),
]

RUINED_CASTLE_ITEMS = [
    ("4.1", "Mountain Mixtures.", "21 October 1892", "Katoomba Times", "Ruined Castle", "Ruined Castle", "Item 4.1 - rock formation"),
    ("4.2", "Mountain Mixtures.", "9 September 1892", "Katoomba Times", "Ruined Castle", "Ruined Castle Shale Mine", "Item 4.2 - shale mine"),
    ("4.3", "Megalong Matters.", "5 June 1896", "Mountaineer", "Ruined Castle", "recreation for miners | cricket match | Ruined Castle (settlement)", "Item 4.3 - recreation, cricket match, and settlement"),
    ("4.4", "The Katoomba Mines.", "20 March 1903", "Blue Mountain Gazette", "Ruined Castle", "Ruined Castle Shale Mine", "Item 4.4 - shale mine"),
    ("4.5", "Current Events.", "26 October 1896", "Newcastle Morning Herald and Miners' Advocate", "Ruined Castle", "tramway | Ruined Castle Shale Mine", "Item 4.5 - tramway and shale mine"),
    ("4.6", "The Megalong Shale Mines.", "21 December 1893", "National Advocate", "Ruined Castle", "Ruined Castle Shale Mine", "Item 4.6 - shale mine and site"),
    ("4.7", "Katoomba Court.", "16 June 1893", "Katoomba Times", "Ruined Castle", "Ruined Castle (settlement)", "Item 4.7 - settlement (residence)"),
    ("4.8", "Mountain Mixtures.", "2 June 1893", "Katoomba Times", "Ruined Castle", "Ruined Castle (settlement) | miner | miners' families | women", "Item 4.8 - settlement, miners, families, women"),
    ("4.9", "Mountain Mixtures.", "2 December 1892", "Katoomba Times", "Ruined Castle", "Ruined Castle Shale Mine | mining accident", "Item 4.9 - shale mine and accident"),
    ("4.10", "To the Editor of The Times.", "8 September 1893", "Katoomba Times", "Ruined Castle", "Ruined Castle Shale Mine | miner | Ruined Castle (settlement)", "Item 4.10 - shale mine, miner, settlement"),
    ("4.11", "Katoomba Court.", "17 March 1893", "Katoomba Times", "Ruined Castle", "Ruined Castle (settlement) | miner", "Item 4.11 - settlement and miner (confirmed via Trove)"),
]

def main():
    # Combine all items
    all_items = POLICE_ITEMS + NELLIES_GLEN_ITEMS + HARTLEY_VALE_ITEMS + RUINED_CASTLE_ITEMS

    # Read existing mapping file
    mapping_path = Path('data/tag_application_mapping.csv')
    with open(mapping_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing_rows = list(reader)
        fieldnames = reader.fieldnames

    # Create new rows
    new_rows = []
    skipped = []

    for item_id, title, date, publication, remove_tags, add_tags, notes in all_items:
        if not add_tags:  # Skip items where tag should be removed entirely
            skipped.append((item_id, title, notes))
            continue

        row = {
            'title': title,
            'date': date,
            'publication': publication,
            'remove_tags': remove_tags,
            'add_tags': add_tags,
            'source': 'ambiguous_tags_decision_report',
            'notes': notes
        }
        new_rows.append(row)

    # Append new rows
    all_rows = existing_rows + new_rows

    # Write back to file
    with open(mapping_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"✓ Added {len(new_rows)} new tag application mappings")
    print(f"✓ Total mappings: {len(all_rows)}")
    print(f"\nSkipped {len(skipped)} items (tag to be removed entirely):")
    for item_id, title, notes in skipped:
        print(f"  - {item_id}: {title} ({notes})")

    # Write summary report
    summary_path = Path('reports/ambiguous_tags_mapping_summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("AMBIGUOUS TAGS DECISION IMPLEMENTATION SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total items processed: {len(all_items)}\n")
        f.write(f"Mappings created: {len(new_rows)}\n")
        f.write(f"Tags removed (no replacement): {len(skipped)}\n\n")

        f.write("ITEMS WHERE TAG REMOVED ENTIRELY:\n")
        f.write("-"*80 + "\n")
        for item_id, title, notes in skipped:
            f.write(f"{item_id}: {title}\n")
            f.write(f"  {notes}\n\n")

        f.write("\nNEW TAGS CREATED IN TAXONOMY:\n")
        f.write("-"*80 + "\n")
        f.write("1. police officer (singular generic under police officers)\n")
        f.write("2. police quarters (building under police facilities)\n")
        f.write("3. Helensburgh (town)\n")
        f.write("4. mining accident (singular generic under mining accidents)\n")
        f.write("5. Hartley Vale Cricket Club (organization under cricket clubs)\n")

    print(f"\n✓ Summary report written to: {summary_path}")

if __name__ == '__main__':
    main()
