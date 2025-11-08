#!/usr/bin/env python3
"""
Check if orphaned person names match existing names in taxonomy.

Compares orphaned person names against mapped names using various strategies
to identify potential matches.
"""

import csv
from pathlib import Path

# Orphaned person names from the analysis
ORPHANED_NAMES = [
    "Miss Bradley", "Miss Edwards", "Miss Eva Peckman", "Miss Levina Kitch",
    "Miss Nellie North", "Mr A J Parcell", "Mr A Thorneycroft", "Mr A W Stephen",
    "Mr Ah Narm", "Mr Allan West", "Mr Arthur L Morris", "Mr Arthur Wright",
    "Mr Banfield", "Mr C J Ellis", "Mr C W Craig", "Mr Charles E Hoffman",
    "Mr Charles George Gordon", "Mr Charles Pratt", "Mr Charles Wooller",
    "Mr Christopher Webb", "Mr Clydesdale", "Mr D J Dunbar", "Mr D Morsby",
    "Mr D O'Keefe", "Mr Dalwood", "Mr David Brown", "Mr David Hamilton",
    "Mr Douglass", "Mr E E Medlicott", "Mr E Jordan", "Mr Edward J Delaney",
    "Mr Edward Pearson", "Mr Frederick Charles Goyder", "Mr G Donald",
    "Mr G Griffiths", "Mr G R Dibbs", "Mr G W Spring", "Mr Gannon",
    "Mr George Bremmer Dunn", "Mr George Frederick Goyder", "Mr George H Cooper",
    "Mr George Susans", "Mr H Roberts", "Mr J Annesley", "Mr J B North",
    "Mr J H Humbley", "Mr J K Cleeve", "Mr J R Nash", "Mr John Duff",
    "Mr John Fitzpatrick", "Mr John Geggie", "Mr John Henry Mitchell",
    "Mr John Hurley", "Mr John Norton", "Mr John Still O'Hara",
    "Mr John W Fletcher", "Mr Jones", "Mr Joseph Cook", "Mr Joseph Edwards",
    "Mr Joseph Nimmo", "Mr Kitch", "Mr L H Howell", "Mr Lewis Duff",
    "Mr Louis Cohen", "Mr Mark Foy", "Mr Messitter", "Mr Neate",
    "Mr Nick Zimmo", "Mr O Purslow", "Mr O'Hare", "Mr O'Sullivan",
    "Mr Owen Owens", "Mr P McAviney", "Mr P Mullany", "Mr Parker",
    "Mr Penrose", "Mr Percy Hammond", "Mr Peter O'Donnell", "Mr Preston",
    "Mr R J Bronger", "Mr Ralph Hartman", "Mr Robert Brydon",
    "Mr Robert H Esgate", "Mr Robert Russell", "Mr Rodrigeuz",
    "Mr Rubina Fryer", "Mr S E Hewett", "Mr Samuel Austin", "Mr Sheard",
    "Mr Stanley Gayfer", "Mr T J Cale", "Mr T Tiernan", "Mr Thomas Austin",
    "Mr Thomas Cook", "Mr Thomas Hollins", "Mr W Hocking", "Mr W J Hart",
    "Mr W McMillan", "Mr Wilfred Moss", "Mr Wrench", "Mr Zack Nimmo",
    "Mrs Christina Brydon", "Mrs Elizabeth Nimmo", "Mrs Ellen Hoffman (nee Gavin)",
    "Mrs Emma Matilda Waudby (nee Phair)", "Mrs Evelyn Gordon (nee Günther)",
    "Mrs Grace Richmond Battram (nee Jones)", "Mrs Isabella Long (nee Clune)",
    "Mrs Mary Duff (nee Evans)", "Mrs Percy Fowles (nee Nimmo)",
    "Mrs Rose Anna (Fanny) Lynch (nee Fisher)", "Mrs S Hindman", "Ms May Porter"
]

def load_mapped_names():
    """Load all person names from taxonomy."""
    names = set()
    with open('data/tag_map_consolidated.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:
                continue
            new_tag = row[0].strip()
            # Include names that start with Mr, Mrs, Miss, Ms, Dr, Reverend, etc.
            if any(new_tag.startswith(prefix) for prefix in
                   ['Mr ', 'Mrs ', 'Miss ', 'Ms ', 'Dr ', 'Reverend ', 'Reverence ',
                    'Constable ', 'Senior-Constable ', 'Sergeant ', 'Coroner ',
                    'Cardinal ', 'Major ']):
                names.add(new_tag)
    return names

def normalize_name(name):
    """Normalize name for comparison."""
    # Remove periods after initials
    normalized = name.replace('.', '')
    # Normalize whitespace
    normalized = ' '.join(normalized.split())
    return normalized

def extract_surname(name):
    """Extract surname from name."""
    # Remove title
    for title in ['Mr ', 'Mrs ', 'Miss ', 'Ms ', 'Dr ']:
        if name.startswith(title):
            name = name[len(title):]
            break

    # Remove nee clause
    if '(nee ' in name:
        name = name.split('(nee')[0].strip()

    # Get last word as surname
    parts = name.split()
    return parts[-1] if parts else ''

def main():
    """Check for name matches."""
    print("Checking orphaned person names against taxonomy...\n")

    mapped_names = load_mapped_names()
    print(f"Found {len(mapped_names)} person names in taxonomy\n")

    # Check for matches
    exact_matches = []
    normalized_matches = []
    surname_matches = []
    no_matches = []

    for orphan in ORPHANED_NAMES:
        orphan_norm = normalize_name(orphan)
        orphan_surname = extract_surname(orphan)

        # Check exact match
        if orphan in mapped_names:
            exact_matches.append((orphan, orphan))
            continue

        # Check normalized match (periods removed)
        found = False
        for mapped in mapped_names:
            if normalize_name(mapped) == orphan_norm:
                normalized_matches.append((orphan, mapped))
                found = True
                break

        if found:
            continue

        # Check surname match
        surname_match_list = []
        for mapped in mapped_names:
            if orphan_surname and extract_surname(mapped) == orphan_surname:
                surname_match_list.append(mapped)

        if surname_match_list:
            surname_matches.append((orphan, surname_match_list))
        else:
            no_matches.append(orphan)

    # Report results
    if exact_matches:
        print(f"✓ Exact matches ({len(exact_matches)}):")
        print("  (These shouldn't be orphaned - may be a script error)")
        for orphan, mapped in exact_matches:
            print(f"  • {orphan!r} = {mapped!r}")
        print()

    if normalized_matches:
        print(f"✓ Normalized matches ({len(normalized_matches)}):")
        print("  (Same name with different punctuation)")
        for orphan, mapped in normalized_matches:
            print(f"  • {orphan!r} → {mapped!r}")
        print()

    if surname_matches:
        print(f"⚠ Possible surname matches ({len(surname_matches)}):")
        print("  (May be same person with different first names/initials)")
        for orphan, matches in surname_matches[:10]:
            print(f"  • {orphan!r} matches:")
            for match in matches:
                print(f"    - {match!r}")
        if len(surname_matches) > 10:
            print(f"  ... and {len(surname_matches) - 10} more")
        print()

    print(f"✗ No matches found ({len(no_matches)}):")
    print("  (Unique person names not in taxonomy)")
    for name in no_matches[:20]:
        print(f"  • {name}")
    if len(no_matches) > 20:
        print(f"  ... and {len(no_matches) - 20} more")

    print(f"\nSummary:")
    print(f"  Exact matches: {len(exact_matches)}")
    print(f"  Normalized matches: {len(normalized_matches)}")
    print(f"  Surname matches: {len(surname_matches)}")
    print(f"  No matches: {len(no_matches)}")

if __name__ == '__main__':
    main()
