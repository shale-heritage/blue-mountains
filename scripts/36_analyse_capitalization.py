#!/usr/bin/env python3
"""
Script 36: Analyse and Preview Capitalization Changes for Getty AAT Compliance

Analyses current capitalization in taxonomy and generates a preview of changes
needed to comply with Getty AAT standard (lowercase for generic terms,
capitalize proper nouns).

Getty AAT Standard:
- Generic terms: lowercase (e.g., "hotel", "church", "miner")
- Proper nouns: capitalize (e.g., "Katoomba", "Grand Hotel")
- Proper adjectives: capitalize (e.g., "Aboriginal", "Chinese", "Australian")

This script ONLY analyses and previews - it does NOT make changes.

Usage:
    python scripts/36_analyse_capitalization.py

Output:
    reports/capitalization_preview.txt - detailed preview of changes
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

# Getty AAT-compliant capitalization rules
PROPER_NOUN_INDICATORS = [
    # Place names (specific locations)
    'Katoomba', 'Sydney', 'Blackheath', 'Leura', 'Lithgow', 'Megalong',
    'Mount Victoria', 'Mt Victoria', 'Mt', 'Victoria', 'Medlow', 'Clarence',
    'Hartley Vale', "Nellie's Glen",
    'Ruined Castle', 'South Clifton', 'Illawarra', 'Jenolan', 'Middle camp',
    'Wentworth Falls', 'Burragorang', 'Kanimbla', 'Jamieson', 'Wallerawang',
    'N.S.W.', 'New South Wales', 'Australia', 'Australian', 'Queensland',
    'Blue Mountains', 'Great Western', 'Western', 'Zig Zag', 'Eskbank',
    'Penrith', 'Nepean',

    # Ethnic/cultural proper adjectives
    'Aboriginal', 'Chinese', 'Irish', 'Inuit', 'German', 'English',

    # Specific organizations (must check context)
    'Independent Order of Odd Fellows', 'United Ancient Order of Druids',
    'Good Templars', 'Freemasons',

    # Named entities (hotels, buildings with proper names)
    'Grand Hotel', 'Imperial Hotel', 'Carrington Hotel', 'Railway Hotel',
    'Belgravia', 'Centennial', 'Comet', 'Falls', 'Hoffman', 'Hydora',
    'Leura', 'Megalong', 'Montrose', 'Oxford', 'Wentworth',

    # Government bodies (official names)
    'Railway Commission', 'Postal Department', 'Post Department', 'Post Office Department',
    "Aborigines' Protection Board",

    # Specific families and people
    'Delaney', 'Greenbank', 'Goyder', 'Fryer', 'Manuell',
    'Bashford', 'Biles', 'Rowell', 'Goodare', 'Thomson', 'Thompson',
    'Edwards', 'Ellis', 'Hudson', 'Nimmo', 'Lindeman', 'Manuel',
    'Whittall', 'Wilson', 'Peckman', 'Tabrett',

    # Organizations (only when standalone, not part of compound phrases)
    # Note: "Police" as organization is handled separately below
    'Court', 'Council',  # When standalone as proper body
    'Douglas and Company', 'Nimmo\'s', 'Peckman Brothers', 'Tabrett and Company',
    'Waudby and Company',

    # Specific historical events/legislation (proper nouns)
    'Licensing Act', 'Mount Kembla', 'Kembla',

    # People and saints (for possessive buildings/institutions)
    'Clarke', 'Waudby', 'Allen', 'Brown', 'Long', 'St Hilda', 'Hilda', 'St',

    # Time periods/styles (if any)
    'Victorian', 'Georgian',
]

GENERIC_CATEGORIES = [
    # Generic category terms that should be lowercase
    'hotels', 'hotel', 'churches', 'church', 'schools', 'school',
    'miners', 'miner', 'mining', 'mines', 'mine',
    'houses', 'house', 'buildings', 'building',
    'lodges', 'lodge', 'halls', 'hall',
    'clubs', 'club', 'organisations', 'organisation',
    'workers', 'worker', 'employees', 'employee',
    'activities', 'activity', 'events', 'event',
    'facilities', 'facility', 'infrastructure',
    'districts', 'district', 'settlements', 'settlement',
    'features', 'feature', 'phenomena',
    'concepts', 'conditions', 'condition',
    'groups', 'group', 'families', 'family',
    'crimes', 'crime', 'violence',
    'reserves', 'reserve', 'towns', 'town',
    'gullies', 'gully', 'valleys', 'valley', 'waterfalls', 'waterfall',
    'accidents', 'accident', 'disaster', 'disasters',
    'disease', 'diseases', 'illness', 'illnesses', 'injury', 'injuries',
    'weather', 'unemployment', 'insurance', 'relief',
    'laws', 'law', 'licences', 'licence', 'attractions', 'attraction',
    'drunkenness', 'intoxication',

    # Social activities
    'behaviours', 'behaviour', 'drinking', 'drink', 'gambling', 'gamble',
    'temperance', 'charity', 'charitable', 'welfare',

    # Communication activities
    'advertising', 'fundraising', 'postal', 'services', 'service',
    'communication',

    # Economic activities
    'agriculture', 'agricultural', 'husbandry', 'breeding', 'breed',
    'hunting', 'hunt', 'tourism', 'tourist', 'transport', 'transportation',
    'trucking', 'trade', 'sales', 'sale', 'business', 'businesses',
    'liquor', 'wholesale', 'financial', 'operations', 'operation',
    'horseborne', 'railway', 'trains', 'train',

    # Recreation activities
    'athletics', 'athletic', 'billiards', 'billiard', 'riding', 'ride',
    'sports', 'sport', 'cricket', 'football', 'rugby', 'tennis',
    'shooting', 'shoot', 'spectator', 'team', 'horseback',
    'military', 'recreation', 'recreational',

    # Societal activities
    'regulatory', 'regulation', 'processes', 'process', 'licensing',
    'policing', 'control', 'culling', 'cull',
    'enforcement', 'public', 'health', 'safety', 'societal',
    'animal', 'feral', 'wild', 'dog', 'horse',

    # Organizations and bodies
    'organizations', 'organisation', 'organisations', 'bodies', 'body',
    'government', 'councils', 'council', 'courts', 'court',
    'committees', 'committee', 'unions', 'union',
    'societies', 'society', 'movements', 'movement',
    'bands', 'band', 'choirs', 'choir', 'troupes', 'troupe',
    'retailers', 'retailer', 'stores', 'store', 'merchants', 'merchant',
    'companies', 'company', 'businesses', 'business',
    'institutions', 'institution', 'bank', 'banks',
    'education', 'educational',

    # People and occupations
    'people', 'person', 'occupations', 'occupation',
    'clergy', 'officials', 'official', 'professionals', 'professional',
    'officers', 'officer', 'personnel', 'employees', 'employee',
    'constable', 'constables', 'sergeant', 'sergeants',
    'coroners', 'coroner', 'shipwright', 'shipwrights',
    'soldiers', 'soldier', 'aldermen', 'alderman',
    'stationmaster', 'stationmasters', 'mailmen', 'mailman',
    'postboy', 'postboys', 'postmasters', 'postmaster',
    'publican', 'publicans', 'hotellier', 'hotelliers',
    'breeder', 'breeders',

    # Demographic groups
    'adolescents', 'adolescent', 'children', 'child',
    'men', 'man', 'widows', 'widow', 'women', 'woman',
    'adults', 'adult', 'youth', 'youths',

    # Animals (generic)
    'animals', 'cattle', 'dogs', 'horses',
]


def should_be_lowercase(term: str) -> bool:
    """
    Determine if a term should be lowercase per Getty AAT standard.

    Returns True if term is generic (should be lowercase)
    Returns False if term is proper noun (should keep capitals)
    """
    # Already all lowercase - no change needed
    if term == term.lower():
        return False  # No change

    # Special cases - keep as-is
    # Getty AAT primary facet names should remain capitalized
    if term in ['THEMATIC', 'Getty AAT', 'Activities', 'Events', 'Associated Concepts',
                'Agents', 'Places', 'Built Environment', 'Materials']:
        return False

    # Title + Name patterns - preserve capitalization
    # e.g., "Constable John Hamilton", "Mr Harry Peckman", "Dr Morgan", "Reverend Smith"
    title_patterns = [
        'Mr ', 'Mrs ', 'Mrs. ', 'Ms ', 'Miss ', 'Dr ', 'Dr. ',
        'Reverend ', 'Reverence ', 'Cardinal ', 'Major ', 'Sir ',
        'Constable ', 'Sergeant ', 'Senior-Constable ',
        'Coroner ', 'Minister ', 'Alderman '
    ]
    for title in title_patterns:
        if term.startswith(title):
            # Check if followed by capitalized name
            remainder = term[len(title):].strip()
            if remainder and remainder[0].isupper():
                return False  # Title + proper name - keep capitalized

    # Special case: "Police" standalone (organization) vs "Police" in compounds (generic)
    if term == 'Police':
        return False  # Standalone "Police" is the organization - keep capitalized

    # Possessive forms - distinguish between proper names and generic descriptives
    if "'" in term or "'" in term:
        # Extract the possessive part (word before apostrophe)
        possessive_word = term.split("'")[0].strip().split()[-1]

        # If the possessive is a known proper noun, keep capitalized
        # e.g., "Allen's Hotel", "Mrs Long's Hotel", "Odd Fellows' Hall"
        for proper in PROPER_NOUN_INDICATORS:
            # Check if possessive word appears in the proper noun indicator
            # OR if proper noun indicator matches the possessive word
            if (possessive_word.lower() in proper.lower() or
                proper.lower() in possessive_word.lower()):
                return False  # Keep capitalization (proper possessive)

        # Otherwise, it's a generic possessive like "publican's licence"
        # Let it fall through to normal processing

    # Check if contains capital letter in middle (not just first letter)
    # This indicates a proper noun within the term
    words = term.split()
    for word in words:
        if len(word) > 1 and any(c.isupper() for c in word[1:]):
            # Capital in middle of word = proper noun
            return False

    # Denomination patterns (Religious Adjective + Church)
    if term.endswith(' Church') and len(words) == 2:
        # Patterns like "Congregational Church", "Methodist Church", "Roman Catholic Church"
        first_word = words[0]
        if first_word[0].isupper() and first_word not in ['The', 'A', 'An']:
            return False  # Keep denomination names capitalized

    # Check if this is a PURE generic category (no proper nouns mixed in)
    term_lower = term.lower()

    # Pure generic categories - just the category word(s) alone
    if term_lower in GENERIC_CATEGORIES:
        return True  # Pure generic - lowercase

    # Category + modifier patterns (e.g., "Coal mining", "Recreation activities")
    # These should be lowercase UNLESS they contain proper nouns
    for generic in GENERIC_CATEGORIES:
        if generic in term_lower:
            # Contains generic term - check if it ONLY contains generics
            # Use sophisticated matching to avoid false positives like "St" matching "postal"
            term_words = set(term_lower.split())
            has_proper = False

            for proper in PROPER_NOUN_INDICATORS:
                proper_lower = proper.lower()

                # Multi-word proper nouns - check if they appear in the term
                # (either exact match or as part of a longer name)
                if ' ' in proper_lower:
                    if proper_lower in term_lower:
                        has_proper = True
                        break
                # Single-word proper nouns
                else:
                    # Short words (<=3 chars) like "St" need exact word match to avoid false positives
                    if len(proper) <= 3:
                        if proper_lower in term_words:
                            has_proper = True
                            break
                    # Longer proper nouns can match as substring
                    else:
                        if proper_lower in term_lower:
                            # But check it's not a substring of a different word
                            # e.g., "Police" shouldn't match "policing"
                            if (proper_lower in term_words or
                                any(word.startswith(proper_lower) or word.endswith(proper_lower)
                                    for word in term_words)):
                                has_proper = True
                                break

            if not has_proper:
                # Pure generic construction - lowercase
                return True

    # Conservative default: if we're not sure, keep current capitalization
    return False


def extract_all_terms(csv_path: Path) -> set:
    """Extract all unique terms from CSV (both tag names and parent references)."""
    terms = set()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Add tag names
            terms.add(row['new_tag'])
            terms.add(row['old_tag'])

            # Extract parent names from notes field
            if row['action'] == 'hierarchy':
                parent_match = re.search(r'parent=(.+?)(?:\s*-\s*THEMATIC)?(?:\s*\([^)]*\))?$',
                                        row['notes'])
                if parent_match:
                    parent = parent_match.group(1).strip()
                    # Strip explanatory parentheticals
                    parent = re.sub(r'\s*\(new top-level facet\)$', '', parent)
                    parent = re.sub(r'\s*\(singular generic term\)$', '', parent)
                    parent = re.sub(r'\s*\(existing facet\)$', '', parent)
                    parent = re.sub(r'\s*\(Getty AAT primary facet\)$', '', parent)
                    terms.add(parent)

    return terms


def generate_capitalization_mapping(terms: set) -> dict:
    """Generate mapping of current term -> proper capitalization."""
    mapping = {}

    for term in sorted(terms):
        if should_be_lowercase(term):
            new_term = term.lower()
            if new_term != term:
                mapping[term] = new_term

    return mapping


def main():
    csv_path = Path('data/tag_map_consolidated.csv')
    output_path = Path('reports/capitalization_preview.txt')

    print("="*80)
    print("GETTY AAT CAPITALIZATION ANALYSIS")
    print("="*80)
    print()

    # Extract all terms
    print("Extracting all terms from taxonomy...")
    terms = extract_all_terms(csv_path)
    print(f"Found {len(terms)} unique terms")
    print()

    # Generate mapping
    print("Analysing capitalization...")
    mapping = generate_capitalization_mapping(terms)
    print(f"Identified {len(mapping)} terms requiring capitalization changes")
    print()

    # Write preview
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CAPITALIZATION CHANGES PREVIEW - Getty AAT Standard\n")
        f.write("="*80 + "\n\n")

        f.write("Getty AAT Standard:\n")
        f.write("- Generic terms: lowercase (e.g., 'hotel', 'church', 'miner')\n")
        f.write("- Proper nouns: capitalize (e.g., 'Katoomba', 'Grand Hotel')\n")
        f.write("- Proper adjectives: capitalize (e.g., 'Aboriginal', 'Chinese')\n\n")

        f.write(f"Total terms requiring changes: {len(mapping)}\n")
        f.write("="*80 + "\n\n")

        if mapping:
            f.write("PROPOSED CHANGES:\n")
            f.write("-"*80 + "\n\n")

            for old_term, new_term in sorted(mapping.items()):
                f.write(f"  {old_term}\n")
                f.write(f"  → {new_term}\n\n")
        else:
            f.write("No changes needed - all terms already comply with Getty AAT standard!\n")

    print(f"Preview written to: {output_path}")
    print()

    if mapping:
        print("SAMPLE CHANGES (first 20):")
        print("-"*80)
        for i, (old_term, new_term) in enumerate(sorted(mapping.items())[:20], 1):
            print(f"  {i}. {old_term} → {new_term}")

        if len(mapping) > 20:
            print(f"  ... and {len(mapping) - 20} more")

        print()
        print("="*80)
        print("NEXT STEPS:")
        print("="*80)
        print("1. Review the full preview: reports/capitalization_preview.txt")
        print("2. If approved, run: python scripts/37_apply_capitalization.py")
        print("3. The application script will update ALL occurrences consistently")
        print()
    else:
        print("✓ All terms already comply with Getty AAT capitalization standard!")


if __name__ == '__main__':
    main()
