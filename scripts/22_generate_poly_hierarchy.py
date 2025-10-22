#!/usr/bin/env python3
"""
Script 22: Generate Poly-Hierarchical Taxonomy Structure (CORRECTED VERSION)

Creates comprehensive poly-hierarchical CSV rows for both:
1. Primary Facets (form-based, Getty AAT compatible)
2. Thematic Groupings (domain-based, exhibition/tour optimized)

Outputs CSV format ready to append to tag_consolidation_map.csv

CORRECTIONS APPLIED (2025-10-20):
- Added intermediate facets consistently throughout:
  * Law enforcement > Police > [individual officers]
  * Legal officials > Coroners > [Coroner, Coroner Lethbridge]
  * Government bodies > Courts > [Court, specific courts]
  * Religious organizations > Churches > [Church, specific churches]
  * Performance groups > Bands > [Band, specific bands]
  * Performance groups > Choirs > [Choir]
  * Sports clubs > Rifle clubs > [Rifle club]
  * Economic activities > Transport > [Horses, Trucking]
- Standardised company names: spelled out "Co." as "Company", "&" as "and"
- Used preferred terms for mining companies and fraternal organizations
- Removed "Colliery" (ambiguous/generic tag)
- Moved "South Clifton Tunnel Mine" from mining companies to Places > Mining districts
- Moved halls from Organizations to Built Environment:
  * Masonic Hall and Odd Fellows' Hall → Built Environment > Halls (buildings, not orgs)
- Standardised fraternal organization names:
  * United Ancient Order of Druids (preferred), U.A.O.D. (variant)
  * Independent Order of Odd Fellows (preferred), Oddfellows (variant)
  * Freemasons (preferred), Masons/U.A.O.D./Druids (variants - see variant_merges_fraternal_orgs.csv)
- Fixed hotel/church duplication (category appears in both facets, individuals only once)
- Dropped "Limited"/"Ltd." from company names for brevity
- Fixed singular/plural consistency: "Coal mine" → "Coal mines"
- Reclassified "Horses" from Recreation to Transport (based on primary source analysis)
- Added "Horseback riding" under Recreation activities (specific recreation activity)

Author: Claude Code
Date: 2025-10-20 (v2 - corrected)
"""

import csv
from pathlib import Path


def generate_primary_facets():
    """
    Generate all primary facet hierarchies (form-based).

    Returns:
        list: CSV rows in format [old_tag, new_tag, action, notes]
    """
    rows = []

    # ========================================================================
    # FACET 1: AGENTS
    # ========================================================================

    # --- 1.1 People ---
    rows.extend([
        ['People', 'People', 'hierarchy', 'parent=Agents (new top-level facet)'],
    ])

    # --- 1.2 Demographic Groups ---
    rows.extend([
        ['Demographic groups', 'Demographic groups', 'hierarchy', 'parent=People'],
        ['Women', 'Women', 'hierarchy', 'parent=Demographic groups'],
        ['Men', 'Men', 'hierarchy', 'parent=Demographic groups'],
        ['Children', 'Children', 'hierarchy', 'parent=Demographic groups'],
        ['Adolescents', 'Adolescents', 'hierarchy', 'parent=Demographic groups'],
        ['Widows', 'Widows', 'hierarchy', 'parent=Demographic groups'],

        # Families
        ['Families', 'Families', 'hierarchy', 'parent=Demographic groups'],
        ['Miners\' families', 'Miners\' families', 'hierarchy', 'parent=Families'],
    ])

    # --- 1.3 Ethnic Groups ---
    rows.extend([
        ['Ethnic groups', 'Ethnic groups', 'hierarchy', 'parent=People'],
        ['Aboriginal people', 'Aboriginal people', 'hierarchy', 'parent=Ethnic groups'],
        ['Chinese people', 'Chinese people', 'hierarchy', 'parent=Ethnic groups'],
        ['Irish culture', 'Irish culture', 'hierarchy', 'parent=Ethnic groups'],

        # Synonym for Irish culture tag
        ['Reference to the Irish or Irish culture', 'Irish culture', 'synonym', 'Renamed to emphasize cultural references rather than demographic group'],

        # Broader term for minors (covers both Children and Adolescents)
        ['Minors', 'Children', 'broader', 'Broader term covering both Children and Adolescents (ages <18)'],
    ])

    # --- 1.4 Occupations ---
    rows.extend([
        ['Occupations', 'Occupations', 'hierarchy', 'parent=People'],

        # Miners
        ['Miners', 'Miners', 'hierarchy', 'parent=Occupations'],

        # Medical professionals
        ['Medical professionals', 'Medical professionals', 'hierarchy', 'parent=Occupations'],
        ['Dr Spark', 'Dr Spark', 'hierarchy', 'parent=Medical professionals'],
        ['Dr Prangley', 'Dr Prangley', 'hierarchy', 'parent=Medical professionals'],
        ['Dr Watkins', 'Dr Watkins', 'hierarchy', 'parent=Medical professionals'],
        ['Dr Morgan', 'Dr Morgan', 'hierarchy', 'parent=Medical professionals'],

        # Clergy
        ['Clergy', 'Clergy', 'hierarchy', 'parent=Occupations'],
        ['Reverend F V Pratt', 'Reverend F V Pratt', 'hierarchy', 'parent=Clergy'],
        ['Reverend Canon Kemmis', 'Reverend Canon Kemmis', 'hierarchy', 'parent=Clergy'],
        ['Reverend M S Fletcher', 'Reverend M S Fletcher', 'hierarchy', 'parent=Clergy'],
        ['Reverend J H Maclean', 'Reverend J H Maclean', 'hierarchy', 'parent=Clergy'],
        ['Reverend A Sutherland', 'Reverend A Sutherland', 'hierarchy', 'parent=Clergy'],
        ['Reverence M C Brown', 'Reverence M C Brown', 'hierarchy', 'parent=Clergy'],
        ['Reverend R M Laverty', 'Reverend R M Laverty', 'hierarchy', 'parent=Clergy'],
        ['Cardinal Moran', 'Cardinal Moran', 'hierarchy', 'parent=Clergy'],

        # Law enforcement
        ['Law enforcement', 'Law enforcement', 'hierarchy', 'parent=Occupations'],
        ['Police', 'Police', 'hierarchy', 'parent=Law enforcement (intermediate facet)'],
        ['Senior-Constable Illingworth', 'Senior-Constable Illingworth', 'hierarchy', 'parent=Police'],
        ['Senior-Constable Thorncroft', 'Senior-Constable Thorncroft', 'hierarchy', 'parent=Police'],
        ['Constable Orr', 'Constable Orr', 'hierarchy', 'parent=Police'],
        ['Constable John Hamilton', 'Constable John Hamilton', 'hierarchy', 'parent=Police'],
        ['Constable O\'Reilly', 'Constable O\'Reilly', 'hierarchy', 'parent=Police'],
        ['Constable White', 'Constable White', 'hierarchy', 'parent=Police'],
        ['Sergeant Thorndyke', 'Sergeant Thorndyke', 'hierarchy', 'parent=Police'],

        # Legal officials
        ['Legal officials', 'Legal officials', 'hierarchy', 'parent=Occupations'],
        ['Coroners', 'Coroners', 'hierarchy', 'parent=Legal officials (intermediate facet)'],
        ['Coroner', 'Coroner', 'hierarchy', 'parent=Coroners'],
        ['Coroner Lethbridge', 'Coroner Lethbridge', 'hierarchy', 'parent=Coroners'],

        # Public officials
        ['Public officials', 'Public officials', 'hierarchy', 'parent=Occupations'],
        ['Aldermen', 'Aldermen', 'hierarchy', 'parent=Public officials'],
        ['Licensing inspector', 'Licensing inspector', 'hierarchy', 'parent=Public officials'],
        ['Stationmaster', 'Stationmaster', 'hierarchy', 'parent=Public officials'],
        ['Minister for Mines', 'Minister for Mines', 'hierarchy', 'parent=Public officials'],

        # Hospitality workers
        ['Hospitality workers', 'Hospitality workers', 'hierarchy', 'parent=Occupations'],
        ['Publican', 'Publican', 'hierarchy', 'parent=Hospitality workers'],

        # Liquor merchants
        ['Liquor merchants', 'Liquor merchants', 'hierarchy', 'parent=Hospitality workers'],
        ['Mr Wilkinson', 'Mr Wilkinson', 'hierarchy', 'parent=Liquor merchants'],

        # Hotelliers - Pattern A (Churches model): Hotelliers > Hotellier > specific people
        ['Hotelliers', 'Hotelliers', 'hierarchy', 'parent=Hospitality workers'],
        ['Hotellier', 'Hotellier', 'hierarchy', 'parent=Hotelliers'],  # Generic/unnamed hotellier
        ['Mrs Long', 'Mrs Long', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Wilson', 'Mr Wilson', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Manuel', 'Mr Manuel', 'hierarchy', 'parent=Hotelliers'],
        ['F. C. Goyder', 'F. C. Goyder', 'hierarchy', 'parent=Hotelliers'],
        ['Rubina Fryer', 'Rubina Fryer', 'hierarchy', 'parent=Hotelliers'],
        ['Isabellea J. Long', 'Isabellea J. Long', 'hierarchy', 'parent=Hotelliers'],
        ['Mr N. Delaney', 'Mr N. Delaney', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Ellis', 'Mr Ellis', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Joe Nimmo', 'Mr Joe Nimmo', 'hierarchy', 'parent=Hotelliers'],
        ['Mrs (Joe) Nimmo', 'Mrs (Joe) Nimmo', 'hierarchy', 'parent=Hotelliers'],
        ['Manuell', 'Manuell', 'hierarchy', 'parent=Hotelliers'],
        ['Mrs Brown', 'Mrs Brown', 'hierarchy', 'parent=Hotelliers'],
        ['W. Green', 'W. Green', 'hierarchy', 'parent=Hotelliers'],
        ['Richard Allen', 'Richard Allen', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Alf. Goodare', 'Mr Alf. Goodare', 'hierarchy', 'parent=Hotelliers'],
        ['Mr R. Fryer', 'Mr R. Fryer', 'hierarchy', 'parent=Hotelliers'],
        ['Mrs (R.) Fryer', 'Mrs (R.) Fryer', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Edwards', 'Mr Edwards', 'hierarchy', 'parent=Hotelliers'],
        ['Biles', 'Biles', 'hierarchy', 'parent=Hotelliers'],
        ['Mr J. Nimmo', 'Mr J. Nimmo', 'hierarchy', 'parent=Hotelliers'],
        ['Mr D. Thompson', 'Mr D. Thompson', 'hierarchy', 'parent=Hotelliers'],
        ['Mr D. Brown', 'Mr D. Brown', 'hierarchy', 'parent=Hotelliers'],
        ['Mr P. G. Whittall', 'Mr P. G. Whittall', 'hierarchy', 'parent=Hotelliers'],
        ['Allen', 'Allen', 'hierarchy', 'parent=Hotelliers'],
        ['Mr Delaney', 'Mr Delaney', 'hierarchy', 'parent=Hotelliers'],
        ['Mr A. G. Rowell', 'Mr A. G. Rowell', 'hierarchy', 'parent=Hotelliers'],
        ['Mr D Thomson', 'Mr D Thomson', 'hierarchy', 'parent=Hotelliers'],
        ['Brown', 'Brown', 'hierarchy', 'parent=Hotelliers'],

        # Military
        ['Military personnel', 'Military personnel', 'hierarchy', 'parent=Occupations'],
        ['Soldiers', 'Soldiers', 'hierarchy', 'parent=Military personnel'],

        # Maritime workers
        ['Maritime workers', 'Maritime workers', 'hierarchy', 'parent=Occupations'],
        ['Shipwright', 'Shipwright', 'hierarchy', 'parent=Maritime workers'],

        # Other goods and services (NEW category)
        ['Other goods and services', 'Other goods and services', 'hierarchy', 'parent=Occupations'],
        ['Coach and buggy business', 'Coach and buggy business', 'hierarchy', 'parent=Other goods and services'],
        ['Mr Thomas Cale', 'Mr Thomas Cale', 'hierarchy', 'parent=Coach and buggy business'],
    ])

    # --- 1.5 Organizations ---
    rows.extend([
        ['Organizations', 'Organizations', 'hierarchy', 'parent=Agents (new top-level facet)'],
        ['Commercial businesses', 'Commercial businesses', 'hierarchy', 'parent=Organizations'],

        # Mining companies
        ['Mining companies', 'Mining companies', 'hierarchy', 'parent=Commercial businesses'],
        ['Australian Kerosene Oil and Mineral Company', 'Australian Kerosene Oil and Mineral Company', 'hierarchy', 'parent=Mining companies'],
        ['Katoomba Coal and Shale Company', 'Katoomba Coal and Shale Company', 'hierarchy', 'parent=Mining companies'],
        ['Gladstone Coal Company', 'Gladstone Coal Company', 'hierarchy', 'parent=Mining companies'],
        ['Sunny Corner Mining Company', 'Sunny Corner Mining Company', 'hierarchy', 'parent=Mining companies'],
        ['South Clifton Mine Company', 'South Clifton Mine Company', 'hierarchy', 'parent=Mining companies'],
        ['New South Wales Shale and Oil Company', 'New South Wales Shale and Oil Company', 'hierarchy', 'parent=Mining companies'],
        ['Waudby and Company', 'Waudby and Company', 'hierarchy', 'parent=Mining companies'],

        # Retailers and stores
        ['Retailers and stores', 'Retailers and stores', 'hierarchy', 'parent=Commercial businesses'],
        ['Store', 'Store', 'hierarchy', 'parent=Retailers and stores'],
        ['Peckman Bros', 'Peckman Bros', 'hierarchy', 'parent=Retailers and stores'],
        ['Nimmo\'s', 'Nimmo\'s', 'hierarchy', 'parent=Retailers and stores'],
        ['Tabrett and Company', 'Tabrett and Company', 'hierarchy', 'parent=Retailers and stores'],
        ['Douglas and Company', 'Douglas and Company', 'hierarchy', 'parent=Retailers and stores'],

        # Financial institutions
        ['Financial institutions', 'Financial institutions', 'hierarchy', 'parent=Commercial businesses'],
        ['Bank', 'Bank', 'hierarchy', 'parent=Financial institutions'],

        # Hospitality businesses
        ['Hospitality businesses', 'Hospitality businesses', 'hierarchy', 'parent=Commercial businesses'],
        ['Hotels', 'Hotels', 'hierarchy', 'parent=Hospitality businesses'],
        # All individual hotels - organisation aspect (also appear under Built Environment)
        ['Megalong Hotel', 'Megalong Hotel', 'hierarchy', 'parent=Hotels'],
        ['Mount Victoria Hotel', 'Mount Victoria Hotel', 'hierarchy', 'parent=Hotels'],
        ['Mrs Long\'s Hotel', 'Mrs Long\'s Hotel', 'hierarchy', 'parent=Hotels'],
        ['Family Hotel', 'Family Hotel', 'hierarchy', 'parent=Hotels'],
        ['Belgravia Hotel', 'Belgravia Hotel', 'hierarchy', 'parent=Hotels'],
        ['Railway Hotel', 'Railway Hotel', 'hierarchy', 'parent=Hotels'],
        ['Grand Hotel', 'Grand Hotel', 'hierarchy', 'parent=Hotels'],
        ['Allen\'s Hotel', 'Allen\'s Hotel', 'hierarchy', 'parent=Hotels'],
        ['Centennial Hotel', 'Centennial Hotel', 'hierarchy', 'parent=Hotels'],
        ['Brown\'s Hotel', 'Brown\'s Hotel', 'hierarchy', 'parent=Hotels'],
        ['Katoomba Hotel', 'Katoomba Hotel', 'hierarchy', 'parent=Hotels'],
        ['Wentworth Falls Hotel', 'Wentworth Falls Hotel', 'hierarchy', 'parent=Hotels'],
        ['Imperial Hotel', 'Imperial Hotel', 'hierarchy', 'parent=Hotels'],
        ['Katoomba Family Hotel', 'Katoomba Family Hotel', 'hierarchy', 'parent=Hotels'],
        ['Delaney\'s Hotel', 'Delaney\'s Hotel', 'hierarchy', 'parent=Hotels'],
        ['Carrington Hotel', 'Carrington Hotel', 'hierarchy', 'parent=Hotels'],
        ['Hoffman\'s House', 'Hoffman\'s House', 'hierarchy', 'parent=Hotels'],
        ['Montrose House', 'Montrose House', 'hierarchy', 'parent=Hotels'],
        ['Boarding houses', 'Boarding houses', 'hierarchy', 'parent=Hospitality businesses'],

        # Transport & logistics businesses
        ['Transport & logistics businesses', 'Transport & logistics businesses', 'hierarchy', 'parent=Commercial businesses'],
        ['Trucking', 'Trucking', 'hierarchy', 'parent=Transport & logistics businesses'],

        # Religious organizations
        ['Religious organizations', 'Religious organizations', 'hierarchy', 'parent=Organizations'],
        ['Churches', 'Churches', 'hierarchy', 'parent=Religious organizations'],
        ['Church', 'Church', 'hierarchy', 'parent=Churches'],
        ['Wesleyan Church', 'Wesleyan Church', 'hierarchy', 'parent=Churches'],
        ['Congregational Church', 'Congregational Church', 'hierarchy', 'parent=Churches'],
        ['Methodist Church', 'Methodist Church', 'hierarchy', 'parent=Churches'],
        ['Katoomba Congregational Church', 'Katoomba Congregational Church', 'hierarchy', 'parent=Churches'],
        ['St Hilda\'s Church', 'St Hilda\'s Church', 'hierarchy', 'parent=Churches'],
        ['Roman Catholic Church', 'Roman Catholic Church', 'hierarchy', 'parent=Churches'],
        ['Religious social movements', 'Religious social movements', 'hierarchy', 'parent=Religious organizations'],
        ['Salvation Army', 'Salvation Army', 'hierarchy', 'parent=Religious social movements'],
        ['Good Templars', 'Good Templars', 'hierarchy', 'parent=Religious social movements'],
        ['Religious education', 'Religious education', 'hierarchy', 'parent=Religious organizations'],
        ['Sunday school', 'Sunday school', 'hierarchy', 'parent=Religious education'],

        # Fraternal orders & lodges
        ['Fraternal orders & lodges', 'Fraternal orders & lodges', 'hierarchy', 'parent=Organizations'],
        ['Lodges', 'Lodges', 'hierarchy', 'parent=Fraternal orders & lodges'],
        # Preferred terms only - variants will be merged via tag_consolidation_map.csv
        ['Freemasons', 'Freemasons', 'hierarchy', 'parent=Lodges'],
        # NOTE: Masons → Freemasons (merge variant)
        # NOTE: Masonic Hall moved to Built Environment > Halls (building, not organization)
        ['Independent Order of Odd Fellows', 'Independent Order of Odd Fellows', 'hierarchy', 'parent=Lodges'],
        # NOTE: Oddfellows → Independent Order of Odd Fellows (merge variant)
        # NOTE: Odd Fellows' Hall moved to Built Environment > Halls (building, not organization)
        ['United Ancient Order of Druids', 'United Ancient Order of Druids', 'hierarchy', 'parent=Lodges'],
        ['Druid\'s Lodge (local lodge)', 'Druid\'s Lodge (local lodge)', 'hierarchy', 'parent=United Ancient Order of Druids'],
        # NOTE: U.A.O.D. → United Ancient Order of Druids (merge acronym variant)
        # NOTE: Druids → United Ancient Order of Druids (merge informal variant)
        ['Independent lodges', 'Independent lodges', 'hierarchy', 'parent=Lodges'],
        ['Mountaineer Lodge', 'Mountaineer Lodge', 'hierarchy', 'parent=Independent lodges'],

        # Cultural & recreational organizations
        ['Cultural & recreational organizations', 'Cultural & recreational organizations', 'hierarchy', 'parent=Organizations'],

        # Sports clubs
        ['Sports clubs', 'Sports clubs', 'hierarchy', 'parent=Cultural & recreational organizations'],
        ['Cricket clubs', 'Cricket clubs', 'hierarchy', 'parent=Sports clubs'],
        ['Katoomba Cricket Club', 'Katoomba Cricket Club', 'hierarchy', 'parent=Cricket clubs'],
        ['Megalong Cricket Club', 'Megalong Cricket Club', 'hierarchy', 'parent=Cricket clubs'],
        ['Football clubs', 'Football clubs', 'hierarchy', 'parent=Sports clubs'],
        ['Katoomba Football Club', 'Katoomba Football Club', 'hierarchy', 'parent=Football clubs'],
        ['Tennis clubs', 'Tennis clubs', 'hierarchy', 'parent=Sports clubs'],
        ['Katoomba Tennis Club', 'Katoomba Tennis Club', 'hierarchy', 'parent=Tennis clubs'],
        ['Lawn Tennis Club', 'Lawn Tennis Club', 'hierarchy', 'parent=Tennis clubs'],
        ['Athletic clubs', 'Athletic clubs', 'hierarchy', 'parent=Sports clubs'],
        ['Katoomba Athletic Club', 'Katoomba Athletic Club', 'hierarchy', 'parent=Athletic clubs'],
        ['Rifle clubs', 'Rifle clubs', 'hierarchy', 'parent=Sports clubs'],
        ['Rifle club', 'Rifle club', 'hierarchy', 'parent=Rifle clubs'],

        # Performance groups
        ['Performance groups', 'Performance groups', 'hierarchy', 'parent=Cultural & recreational organizations'],
        ['Choirs', 'Choirs', 'hierarchy', 'parent=Performance groups'],
        ['Choir', 'Choir', 'hierarchy', 'parent=Choirs'],
        ['Bands', 'Bands', 'hierarchy', 'parent=Performance groups'],
        ['Band', 'Band', 'hierarchy', 'parent=Bands'],
        ['Katoomba band', 'Katoomba band', 'hierarchy', 'parent=Bands'],
        ['Minstrel troupes', 'Minstrel troupes', 'hierarchy', 'parent=Performance groups'],
        ['Katoomba Amateur Minstrels', 'Katoomba Amateur Minstrels', 'hierarchy', 'parent=Minstrel troupes'],

        # Cultural societies
        ['Cultural societies', 'Cultural societies', 'hierarchy', 'parent=Cultural & recreational organizations'],
        ['Schools of Arts', 'Schools of Arts', 'hierarchy', 'parent=Cultural societies'],
        ['School of Arts', 'School of Arts', 'hierarchy', 'parent=Schools of Arts'],
        ['Katoomba School of Arts', 'Katoomba School of Arts', 'hierarchy', 'parent=Schools of Arts'],
        ['Horticulture society', 'Horticulture society', 'hierarchy', 'parent=Cultural societies'],
        ['Katoomba Amateur Dramatic Club', 'Katoomba Amateur Dramatic Club', 'hierarchy', 'parent=Cultural societies'],
        ['Chess and Draughts Club', 'Chess and Draughts Club', 'hierarchy', 'parent=Cultural societies'],

        # Civic organizations
        ['Civic organizations', 'Civic organizations', 'hierarchy', 'parent=Organizations'],
        ['Progress committees', 'Progress committees', 'hierarchy', 'parent=Civic organizations'],
        ['Katoomba Progress Association', 'Katoomba Progress Association', 'hierarchy', 'parent=Progress committees'],
        ['Leura Progress Association', 'Leura Progress Association', 'hierarchy', 'parent=Progress committees'],
        ['Wentworth Falls Progress Association', 'Wentworth Falls Progress Association', 'hierarchy', 'parent=Progress committees'],
        ['Mount Victoria Progress Committee', 'Mount Victoria Progress Committee', 'hierarchy', 'parent=Progress committees'],
        ['Megalong Progress Committee', 'Megalong Progress Committee', 'hierarchy', 'parent=Progress committees'],
        ['Labour organizations', 'Labour organizations', 'hierarchy', 'parent=Civic organizations'],
        ['Unions', 'Unions', 'hierarchy', 'parent=Labour organizations'],

        # Government bodies
        ['Government bodies', 'Government bodies', 'hierarchy', 'parent=Organizations'],
        ['Courts', 'Courts', 'hierarchy', 'parent=Government bodies'],
        ['Court', 'Court', 'hierarchy', 'parent=Courts'],
        ['Supreme Court', 'Supreme Court', 'hierarchy', 'parent=Courts'],
        ['Police court', 'Police court', 'hierarchy', 'parent=Courts'],
        ['Licensing Court', 'Licensing Court', 'hierarchy', 'parent=Courts'],
        ['Katoomba Court', 'Katoomba Court', 'hierarchy', 'parent=Courts'],
        ['Councils', 'Councils', 'hierarchy', 'parent=Government bodies'],
        ['Katoomba Council', 'Katoomba Council', 'hierarchy', 'parent=Councils'],
        ['Lithgow Council', 'Lithgow Council', 'hierarchy', 'parent=Councils'],
        ['Railway authorities', 'Railway authorities', 'hierarchy', 'parent=Government bodies'],
        ['Railway commission', 'Railway commission', 'hierarchy', 'parent=Railway authorities'],
        ['Other government bodies', 'Other government bodies', 'hierarchy', 'parent=Government bodies'],
        ['Aborigines\' Protection Board', 'Aborigines\' Protection Board', 'hierarchy', 'parent=Other government bodies'],
    ])

    # --- 1.7 Animals (Living Organisms) ---
    rows.extend([
        ['Animals', 'Animals', 'hierarchy', 'parent=Agents (new top-level facet)'],
        ['Horses', 'Horses', 'hierarchy', 'parent=Animals'],
        ['Dogs', 'Dogs', 'hierarchy', 'parent=Animals'],
        ['Cattle', 'Cattle', 'hierarchy', 'parent=Animals'],
    ])

    # ========================================================================
    # FACET 2: PLACES
    # ========================================================================

    rows.extend([
        # Mining districts
        ['Mining districts', 'Mining districts', 'hierarchy', 'parent=Places (existing facet)'],
        ['Ruined Castle', 'Ruined Castle', 'hierarchy', 'parent=Mining districts'],
        ['Ruined Castle Shale Mine', 'Ruined Castle Shale Mine', 'hierarchy', 'parent=Ruined Castle'],
        ['Nellie\'s Glen', 'Nellie\'s Glen', 'hierarchy', 'parent=Mining districts'],
        ['Nellie\'s Glen Track', 'Nellie\'s Glen Track', 'hierarchy', 'parent=Nellie\'s Glen'],
        ['Nellie\'s Glen Road', 'Nellie\'s Glen Road', 'hierarchy', 'parent=Nellie\'s Glen'],
        ['Nellie\'s Glen Shale Mine', 'Nellie\'s Glen Shale Mine', 'hierarchy', 'parent=Nellie\'s Glen'],
        ['South Clifton', 'South Clifton', 'hierarchy', 'parent=Mining districts'],
        ['South Clifton Tunnel Mine', 'South Clifton Tunnel Mine', 'hierarchy', 'parent=South Clifton'],

        # Natural features
        ['Natural features', 'Natural features', 'hierarchy', 'parent=Places (existing facet)'],
        ['Waterfalls', 'Waterfalls', 'hierarchy', 'parent=Natural features'],
        ['Katoomba Falls', 'Katoomba Falls', 'hierarchy', 'parent=Waterfalls'],
        ['Leura Falls', 'Leura Falls', 'hierarchy', 'parent=Waterfalls'],
        ['Minnehaha', 'Minnehaha', 'hierarchy', 'parent=Waterfalls'],
        ['Valleys', 'Valleys', 'hierarchy', 'parent=Natural features'],
        ['Megalong Valley', 'Megalong Valley', 'hierarchy', 'parent=Valleys'],
        ['Kanimbla Valley', 'Kanimbla Valley', 'hierarchy', 'parent=Valleys'],
        ['Jamieson Valley', 'Jamieson Valley', 'hierarchy', 'parent=Valleys'],
        ['Mountain features', 'Mountain features', 'hierarchy', 'parent=Natural features'],
        ['Narrow Neck', 'Narrow Neck', 'hierarchy', 'parent=Mountain features'],
        # TODO: Verify if 'Ruined Castle' is used for topographic feature independently of mining district
        # Currently removed to prevent 'Ruined Castle Shale Mine' appearing under Mountain features
        # ['Ruined Castle', 'Ruined Castle', 'hierarchy', 'parent=Mountain features'],
        ['Caves & geological features', 'Caves & geological features', 'hierarchy', 'parent=Natural features'],
        ['Jenolan Caves', 'Jenolan Caves', 'hierarchy', 'parent=Caves & geological features'],
        ['Jenolan Caves Road', 'Jenolan Caves Road', 'hierarchy', 'parent=Jenolan Caves'],
        ['Gullies', 'Gullies', 'hierarchy', 'parent=Natural features'],
        ['Nellie\'s Glen', 'Nellie\'s Glen', 'hierarchy', 'parent=Gullies'],

        # Mining settlements
        ['Mining settlements', 'Mining settlements', 'hierarchy', 'parent=Places (existing facet)'],
        ['Middle camp', 'Middle camp', 'hierarchy', 'parent=Mining settlements'],

        # Towns (settlements with places/localities within them)
        ['Towns', 'Towns', 'hierarchy', 'parent=Places (existing facet)'],
        ['Katoomba', 'Katoomba', 'hierarchy', 'parent=Towns'],
        ['Carrington', 'Carrington', 'hierarchy', 'parent=Katoomba'],
        ['South Katoomba', 'South Katoomba', 'hierarchy', 'parent=Katoomba'],
        ['Leura', 'Leura', 'hierarchy', 'parent=Towns'],
        ['Medlow', 'Medlow', 'hierarchy', 'parent=Towns'],
        ['Mount Victoria', 'Mount Victoria', 'hierarchy', 'parent=Towns'],
        ['Hartley Vale', 'Hartley Vale', 'hierarchy', 'parent=Towns'],
        ['Clarence', 'Clarence', 'hierarchy', 'parent=Towns'],
        ['Lithgow', 'Lithgow', 'hierarchy', 'parent=Towns'],
        ['Sydney', 'Sydney', 'hierarchy', 'parent=Towns'],
        ['Blackheath', 'Blackheath', 'hierarchy', 'parent=Towns'],
        ['Megalong', 'Megalong', 'hierarchy', 'parent=Towns'],
        ['Middle camp', 'Middle camp', 'hierarchy', 'parent=Megalong'],

        # Reserves (recreational lands)
        ['Reserves', 'Reserves', 'hierarchy', 'parent=Places (existing facet)'],
        ['Rifle reserves', 'Rifle reserves', 'hierarchy', 'parent=Reserves'],
        ['Katoomba Rifle Reserve', 'Katoomba Rifle Reserve', 'hierarchy', 'parent=Rifle reserves'],
        ['Wentworth Falls Reserve', 'Wentworth Falls Reserve', 'hierarchy', 'parent=Reserves'],
        ['Leura Reserve', 'Leura Reserve', 'hierarchy', 'parent=Reserves'],
        ['South Katoomba Reserve', 'South Katoomba Reserve', 'hierarchy', 'parent=Reserves'],

        # Place name variants/synonyms
        ['Wentworth Falls Reserves', 'Wentworth Falls Reserve', 'synonym', 'Plural variant - standardised to singular'],
        ['Katoomba Rifle Reserves', 'Katoomba Rifle Reserve', 'synonym', 'Plural variant - standardised to singular'],
        ['Mt Victoria', 'Mount Victoria', 'synonym', 'Abbreviation of Mount Victoria (town)'],
        ['Mt Victoria Hotel', 'Mount Victoria Hotel', 'synonym', 'Abbreviation of Mount Victoria Hotel'],
    ])

    # ========================================================================
    # FACET 3: BUILT ENVIRONMENT
    # ========================================================================

    rows.extend([
        ['Built Environment', 'Built Environment', 'hierarchy', 'parent=(new top-level facet)'],

        # Accommodation buildings
        ['Accommodation buildings', 'Accommodation buildings', 'hierarchy', 'parent=Built Environment'],

        # Hotels - Pattern A (Churches model): Hotels > Hotel > specific hotels
        ['Hotels', 'Hotels', 'hierarchy', 'parent=Accommodation buildings'],
        ['Hotel', 'Hotel', 'hierarchy', 'parent=Hotels'],  # Generic/unnamed hotel
        # NOTE: Individual hotels also appear under Organizations > Hospitality businesses (business aspect)
        # This creates poly-hierarchy: hotels as buildings (here) AND hotels as businesses (Organizations)
        # New hotels from accommodation rationalization:
        ['Comet Hotel', 'Comet Hotel', 'hierarchy', 'parent=Hotels'],
        ['Falls Hotel', 'Falls Hotel', 'hierarchy', 'parent=Hotels'],
        ['Fryer\'s Family Hotel', 'Fryer\'s Family Hotel', 'hierarchy', 'parent=Hotels'],
        ['Grand Hotel (Sydney)', 'Grand Hotel (Sydney)', 'hierarchy', 'parent=Hotels'],
        ['Great Western Hotel', 'Great Western Hotel', 'hierarchy', 'parent=Hotels'],
        ['Hotel Wentworth', 'Hotel Wentworth', 'hierarchy', 'parent=Hotels'],
        ['Hydora House Hotel', 'Hydora House Hotel', 'hierarchy', 'parent=Hotels'],
        ['Leura Hotel', 'Leura Hotel', 'hierarchy', 'parent=Hotels'],
        ['Oxford Hotel (Sydney)', 'Oxford Hotel (Sydney)', 'hierarchy', 'parent=Hotels'],

        # Boarding houses - Pattern A
        ['Boarding houses', 'Boarding houses', 'hierarchy', 'parent=Accommodation buildings'],
        ['Boarding house', 'Boarding house', 'hierarchy', 'parent=Boarding houses'],  # Generic/unnamed
        ['Orama Boarding House', 'Orama Boarding House', 'hierarchy', 'parent=Boarding houses'],

        # Cottages - Pattern A (NEW category)
        ['Cottages', 'Cottages', 'hierarchy', 'parent=Accommodation buildings'],
        ['Cottage', 'Cottage', 'hierarchy', 'parent=Cottages'],  # Generic/unnamed cottage

        # Stables - Pattern A (NEW category)
        ['Stables', 'Stables', 'hierarchy', 'parent=Accommodation buildings'],
        ['Stable', 'Stable', 'hierarchy', 'parent=Stables'],  # Generic/unnamed stable

        # Dwellings
        ['Dwellings', 'Dwellings', 'hierarchy', 'parent=Accommodation buildings'],
        ['Miners\' dwellings', 'Miners\' dwellings', 'hierarchy', 'parent=Dwellings'],

        # Hospitality venues
        ['Hospitality venues', 'Hospitality venues', 'hierarchy', 'parent=Built Environment'],
        ['Public house', 'Public house', 'hierarchy', 'parent=Hospitality venues'],
        ['Pub', 'Public house', 'synonym', 'Colloquial term for public house'],
        ['Pubs', 'Pubs', 'hierarchy', 'parent=Hospitality venues'],

        # Civic buildings
        ['Civic buildings', 'Civic buildings', 'hierarchy', 'parent=Built Environment'],
        ['Court buildings', 'Court buildings', 'hierarchy', 'parent=Civic buildings'],
        ['Courthouse', 'Courthouse', 'hierarchy', 'parent=Court buildings'],
        ['Katoomba Court', 'Katoomba Court', 'hierarchy', 'parent=Court buildings'],
        ['Council buildings', 'Council buildings', 'hierarchy', 'parent=Civic buildings'],
        ['Council Chambers', 'Council Chambers', 'hierarchy', 'parent=Council buildings'],
        ['Police facilities', 'Police facilities', 'hierarchy', 'parent=Civic buildings'],
        ['Police station', 'Police station', 'hierarchy', 'parent=Police facilities'],
        ['Postal facilities', 'Postal facilities', 'hierarchy', 'parent=Civic buildings'],
        ['Post office', 'Post office', 'hierarchy', 'parent=Postal facilities'],

        # Educational buildings
        ['Educational buildings', 'Educational buildings', 'hierarchy', 'parent=Built Environment'],
        ['Schools', 'Schools', 'hierarchy', 'parent=Educational buildings'],
        ['School', 'School', 'hierarchy', 'parent=Schools'],
        ['Mount Victoria School', 'Mount Victoria School', 'hierarchy', 'parent=Schools'],
        ['Katoomba Public School', 'Katoomba Public School', 'hierarchy', 'parent=Schools'],
        ['Katoomba Superior Public School', 'Katoomba Superior Public School', 'hierarchy', 'parent=Schools'],
        ['Megalong Valley School', 'Megalong Valley School', 'hierarchy', 'parent=Schools'],

        # Religious buildings
        ['Religious buildings', 'Religious buildings', 'hierarchy', 'parent=Built Environment'],
        ['Churches', 'Churches', 'hierarchy', 'parent=Religious buildings'],
        # NOTE: Individual churches listed under Organizations > Religious organizations > Churches
        # Churches category appears here for poly-hierarchy (building aspect), but individual churches not duplicated

        # Community buildings
        ['Community buildings', 'Community buildings', 'hierarchy', 'parent=Built Environment'],
        ['Halls', 'Halls', 'hierarchy', 'parent=Community buildings'],
        ['Schools of Arts', 'Schools of Arts', 'hierarchy', 'parent=Halls'],
        ['School of Arts', 'School of Arts', 'hierarchy', 'parent=Schools of Arts'],
        ['Katoomba School of Arts', 'Katoomba School of Arts', 'hierarchy', 'parent=Schools of Arts'],
        ['Clarke\'s Hall', 'Clarke\'s Hall', 'hierarchy', 'parent=Halls'],
        ['Waudby\'s Hall', 'Waudby\'s Hall', 'hierarchy', 'parent=Halls'],
        ['Mount Victoria Hall', 'Mount Victoria Hall', 'hierarchy', 'parent=Halls'],
        ['Odd Fellows\' Hall', 'Odd Fellows\' Hall', 'hierarchy', 'parent=Halls'],
        ['Masonic Hall', 'Masonic Hall', 'hierarchy', 'parent=Halls'],

        # Commercial buildings
        ['Commercial buildings', 'Commercial buildings', 'hierarchy', 'parent=Built Environment'],
        ['Store', 'Store', 'hierarchy', 'parent=Commercial buildings'],
        ['Bank', 'Bank', 'hierarchy', 'parent=Commercial buildings'],

        # Infrastructure
        ['Infrastructure', 'Infrastructure', 'hierarchy', 'parent=Built Environment'],
        ['Transport infrastructure', 'Transport infrastructure', 'hierarchy', 'parent=Infrastructure'],

        # Railway
        ['Railway', 'Railway', 'hierarchy', 'parent=Transport infrastructure'],
        ['Great Western Railway', 'Great Western Railway', 'hierarchy', 'parent=Railway'],
        ['Railway infrastructure', 'Railway infrastructure', 'hierarchy', 'parent=Railway'],
        ['Katoomba station', 'Katoomba station', 'hierarchy', 'parent=Railway infrastructure'],
        ['Zig Zag', 'Zig Zag', 'hierarchy', 'parent=Railway infrastructure'],
        ['Railway operations', 'Railway operations', 'hierarchy', 'parent=Railway'],
        ['Tourist trains', 'Tourist trains', 'hierarchy', 'parent=Railway operations'],

        # Roads
        ['Roads', 'Roads', 'hierarchy', 'parent=Transport infrastructure'],
        ['Jenolan Caves Road', 'Jenolan Caves Road', 'hierarchy', 'parent=Roads'],
        ['Nellie\'s Glen Road', 'Nellie\'s Glen Road', 'hierarchy', 'parent=Roads'],
        ['Nellie\'s Glen Track', 'Nellie\'s Glen Track', 'hierarchy', 'parent=Roads'],

        # Mining infrastructure
        ['Mining infrastructure', 'Mining infrastructure', 'hierarchy', 'parent=Infrastructure'],
        ['Tramway', 'Tramway', 'hierarchy', 'parent=Mining infrastructure'],

        # Utilities
        ['Utilities', 'Utilities', 'hierarchy', 'parent=Infrastructure'],
        ['Sewerage', 'Sewerage', 'hierarchy', 'parent=Utilities'],
        ['Gas', 'Gas', 'hierarchy', 'parent=Utilities'],
    ])

    # ========================================================================
    # FACET 4: ACTIVITIES & EVENTS
    # ========================================================================

    rows.extend([
        ['Events', 'Events', 'hierarchy', 'parent=(new top-level facet)'],

        # Life events
        ['Life events', 'Life events', 'hierarchy', 'parent=Events'],
        ['Death', 'Death', 'hierarchy', 'parent=Life events'],
        ['Death notice', 'Death notice', 'hierarchy', 'parent=Death'],
        ['Marriage', 'Marriage', 'hierarchy', 'parent=Life events'],
        ['Funeral', 'Funeral', 'hierarchy', 'parent=Life events'],

        # Social events
        ['Social events', 'Social events', 'hierarchy', 'parent=Events'],
        ['Dance', 'Dance', 'hierarchy', 'parent=Social events'],
        ['Ball', 'Ball', 'hierarchy', 'parent=Social events'],
        ['Flower show', 'Flower show', 'hierarchy', 'parent=Social events'],

        # Sporting events
        ['Sporting events', 'Sporting events', 'hierarchy', 'parent=Events'],
        ['Cricket', 'Cricket', 'hierarchy', 'parent=Sporting events'],
        ['Girls\' cricket', 'Girls\' cricket', 'hierarchy', 'parent=Cricket'],
        ['Football', 'Football', 'hierarchy', 'parent=Sporting events'],
        ['Tennis', 'Tennis', 'hierarchy', 'parent=Sporting events'],
        ['Athletics', 'Athletics', 'hierarchy', 'parent=Sporting events'],
        ['Rugby', 'Rugby', 'hierarchy', 'parent=Sporting events'],
        ['Shooting', 'Shooting', 'hierarchy', 'parent=Sporting events'],
        ['Billiards', 'Billiards', 'hierarchy', 'parent=Sporting events'],

        # Cultural events
        ['Cultural events', 'Cultural events', 'hierarchy', 'parent=Events'],
        ['Concert', 'Concert', 'hierarchy', 'parent=Cultural events'],
        ['Debate', 'Debate', 'hierarchy', 'parent=Cultural events'],
        ['Corroboree', 'Corroboree', 'hierarchy', 'parent=Cultural events'],

        # Legal events
        ['Legal events', 'Legal events', 'hierarchy', 'parent=Events'],
        ['Court cases', 'Court cases', 'hierarchy', 'parent=Legal events'],
        ['Bankruptcy', 'Bankruptcy', 'hierarchy', 'parent=Legal events'],
        ['Divorce', 'Divorce', 'hierarchy', 'parent=Legal events'],

        # Criminal events
        ['Criminal events', 'Criminal events', 'hierarchy', 'parent=Events'],
        ['Theft', 'Theft', 'hierarchy', 'parent=Criminal events'],
        ['Rape', 'Rape', 'hierarchy', 'parent=Criminal events'],
        ['Fighting', 'Fighting', 'hierarchy', 'parent=Criminal events'],
        ['Assault', 'Assault', 'hierarchy', 'parent=Criminal events'],
        ['Bigamy', 'Bigamy', 'hierarchy', 'parent=Criminal events'],
        ['Sexual violence', 'Sexual violence', 'hierarchy', 'parent=Criminal events'],
        ['Desertion', 'Desertion', 'hierarchy', 'parent=Criminal events'],

        # Alcohol-related criminal events
        ['Alcohol-related', 'Alcohol-related', 'hierarchy', 'parent=Criminal events'],
        ['Drunkenness', 'Drunkenness', 'hierarchy', 'parent=Alcohol-related'],
        ['Unlicensed sales', 'Unlicensed sales', 'hierarchy', 'parent=Alcohol-related'],
        ['Sly-grog operations', 'Unlicensed sales', 'synonym', 'Australian colonial term for unlicensed liquor sales'],
        ['Serving alcohol to minors', 'Serving alcohol to minors', 'hierarchy', 'parent=Alcohol-related'],

        # Political events
        ['Political events', 'Political events', 'hierarchy', 'parent=Events'],
        ['Election', 'Election', 'hierarchy', 'parent=Political events'],
        ['Public meeting', 'Public meeting', 'hierarchy', 'parent=Political events'],
        ['Petition', 'Petition', 'hierarchy', 'parent=Political events'],

        # Economic events
        ['Economic events', 'Economic events', 'hierarchy', 'parent=Events'],
        ['Strike', 'Strike', 'hierarchy', 'parent=Economic events'],
        ['Mine closure', 'Mine closure', 'hierarchy', 'parent=Economic events'],

        # Disasters & accidents
        ['Disasters & accidents', 'Disasters & accidents', 'hierarchy', 'parent=Events'],
        ['Accident', 'Accident', 'hierarchy', 'parent=Disasters & accidents'],
        ['Mining accidents', 'Mining accidents', 'hierarchy', 'parent=Accident'],
        ['Mount Kembla Disaster', 'Mount Kembla Disaster', 'hierarchy', 'parent=Mining accidents'],
        ['Fire', 'Fire', 'hierarchy', 'parent=Disasters & accidents'],

        # Historical events
        ['Historical events', 'Historical events', 'hierarchy', 'parent=Events'],
        ['World War I', 'World War I', 'hierarchy', 'parent=Historical events'],

        # Synonyms for Mount Kembla Disaster
        ['Port Kembla disaster', 'Mount Kembla Disaster', 'synonym', 'Historical misnomer - actually Mount Kembla (not Port Kembla)'],
        ['Mount Kembla Colliery Disaster', 'Mount Kembla Disaster', 'synonym', 'Alternative name for 1902 mining disaster'],

        # Activities (ongoing processes)
        ['Activities', 'Activities', 'hierarchy', 'parent=(new top-level facet)'],

        # Economic activities
        ['Economic activities', 'Economic activities', 'hierarchy', 'parent=Activities'],
        ['Mining', 'Mining', 'hierarchy', 'parent=Economic activities'],
        ['Shale mining', 'Shale mining', 'hierarchy', 'parent=Mining'],
        ['Shale mines', 'Shale mines', 'hierarchy', 'parent=Shale mining'],
        ['Coal mining', 'Coal mining', 'hierarchy', 'parent=Mining'],
        ['Coal', 'Coal', 'hierarchy', 'parent=Coal mining'],
        ['Coal mines', 'Coal mines', 'hierarchy', 'parent=Coal mining'],
        ['Gold mining', 'Gold mining', 'hierarchy', 'parent=Mining'],
        ['Tourism', 'Tourism', 'hierarchy', 'parent=Economic activities'],
        ['Transport', 'Transport', 'hierarchy', 'parent=Economic activities'],
        ['Trucking', 'Trucking', 'hierarchy', 'parent=Transport'],
        ['Horses', 'Horses', 'hierarchy', 'parent=Transport'],

        # Commercial activities
        ['Commercial activities', 'Commercial activities', 'hierarchy', 'parent=Activities'],
        ['Liquor trade', 'Liquor trade', 'hierarchy', 'parent=Commercial activities'],
        ['Liquor sales', 'Liquor sales', 'hierarchy', 'parent=Liquor trade'],
        ['Wholesale liquor business', 'Wholesale liquor business', 'hierarchy', 'parent=Liquor trade'],

        # Recreation activities
        ['Recreation activities', 'Recreation activities', 'hierarchy', 'parent=Activities'],
        ['Recreation for miners', 'Recreation for miners', 'hierarchy', 'parent=Recreation activities'],
        ['Sports', 'Sports', 'hierarchy', 'parent=Recreation activities'],
        ['Horseback riding', 'Horseback riding', 'hierarchy', 'parent=Recreation activities'],

        # Social behaviours
        ['Social behaviours', 'Social behaviours', 'hierarchy', 'parent=Activities'],
        ['Drinking (alcohol)', 'Drinking (alcohol)', 'hierarchy', 'parent=Social behaviours'],
        ['Drinking', 'Drinking (alcohol)', 'synonym', 'Renamed for clarity - refers specifically to alcohol consumption'],
        ['Gambling', 'Gambling', 'hierarchy', 'parent=Social behaviours'],
        ['Temperance', 'Temperance', 'hierarchy', 'parent=Social behaviours'],

        # Communication activities
        ['Communication activities', 'Communication activities', 'hierarchy', 'parent=Activities'],
        ['Advertising', 'Advertising', 'hierarchy', 'parent=Communication activities'],
        ['Fundraising', 'Fundraising', 'hierarchy', 'parent=Communication activities'],

        # Postal services
        # TODO: Review source text to disambiguate post office (building) vs postal service (activity)
        ['Postal services', 'Postal services', 'hierarchy', 'parent=Communication activities'],
        ['Post', 'Post', 'hierarchy', 'parent=Postal services'],

        # Military activities
        ['Military activities', 'Military activities', 'hierarchy', 'parent=Activities'],
        ['Military', 'Military', 'hierarchy', 'parent=Military activities'],

        # Regulatory processes
        ['Regulatory processes', 'Regulatory processes', 'hierarchy', 'parent=Activities'],
        ['Licensing', 'Licensing', 'hierarchy', 'parent=Regulatory processes'],
        ['Liquor licensing', 'Liquor licensing', 'hierarchy', 'parent=Licensing'],

        # Charitable and welfare activities
        ['Charitable and welfare activities', 'Charitable and welfare activities', 'hierarchy', 'parent=Activities'],
        ['Charity', 'Charity', 'hierarchy', 'parent=Charitable and welfare activities'],
        ['Unemployment relief', 'Unemployment relief', 'hierarchy', 'parent=Charitable and welfare activities'],
    ])

    # ========================================================================
    # FACET 5: CONCEPTS & THEMES
    # ========================================================================

    rows.extend([
        # Information Forms (Getty AAT-aligned terminology)
        ['Information Forms', 'Information Forms', 'hierarchy', 'parent=(conceptual facet)'],
        ['Legal documents', 'Legal documents', 'hierarchy', 'parent=Information Forms'],
        ['Legislation', 'Legislation', 'hierarchy', 'parent=Legal documents'],
        ['Licensing Act', 'Licensing Act', 'hierarchy', 'parent=Legislation'],
        ['Licenses', 'Licenses', 'hierarchy', 'parent=Legal documents'],
        ['Publican\'s License', 'Publican\'s License', 'hierarchy', 'parent=Licenses'],
        ['Maps', 'Maps', 'hierarchy', 'parent=Information Forms'],

        # Associated Concepts (Getty AAT-aligned: abstract concepts and phenomena)
        ['Associated Concepts', 'Associated Concepts', 'hierarchy', 'parent=(conceptual facet)'],

        # Physical phenomena
        ['Physical phenomena', 'Physical phenomena', 'hierarchy', 'parent=Associated Concepts'],
        ['Weather', 'Weather', 'hierarchy', 'parent=Physical phenomena'],

        # Social & economic concepts
        ['Social & economic concepts', 'Social & economic concepts', 'hierarchy', 'parent=Associated Concepts'],
        ['Unemployment', 'Unemployment', 'hierarchy', 'parent=Social & economic concepts'],

        # Physical and health conditions
        ['Physical and health conditions', 'Physical and health conditions', 'hierarchy', 'parent=Associated Concepts'],
        ['Injury', 'Injury', 'hierarchy', 'parent=Physical and health conditions'],
        ['Illness', 'Illness', 'hierarchy', 'parent=Physical and health conditions'],
        ['Disease', 'Disease', 'hierarchy', 'parent=Physical and health conditions'],
        ['Drunkenness (intoxication)', 'Drunkenness (intoxication)', 'hierarchy', 'parent=Physical and health conditions'],
    ])

    # ========================================================================
    # FACET 7: MATERIALS
    # ========================================================================
    # New facet added 2025-10-22 for consumable materials (alcohol rationalization)

    rows.extend([
        ['Materials', 'Materials', 'hierarchy', 'parent=(new top-level facet)'],

        # Consumable materials
        ['Consumable materials', 'Consumable materials', 'hierarchy', 'parent=Materials'],

        # Alcoholic beverages
        ['Alcoholic beverages', 'Alcoholic beverages', 'hierarchy', 'parent=Consumable materials'],
        ['Beer', 'Beer', 'hierarchy', 'parent=Alcoholic beverages'],
        ['Wine', 'Wine', 'hierarchy', 'parent=Alcoholic beverages'],

        # Spirits
        ['Spirits', 'Spirits', 'hierarchy', 'parent=Alcoholic beverages'],
        ['Whisky', 'Whisky', 'hierarchy', 'parent=Spirits'],
        ['Whiskey', 'Whisky', 'synonym', 'Alternative spelling of whisky (both spellings valid)'],
        ['Rum', 'Rum', 'hierarchy', 'parent=Spirits'],
        ['Brandy', 'Brandy', 'hierarchy', 'parent=Spirits'],
        ['Gin', 'Gin', 'hierarchy', 'parent=Spirits'],

        # Mixed alcoholic beverages
        ['Mixed alcoholic beverages', 'Mixed alcoholic beverages', 'hierarchy', 'parent=Alcoholic beverages'],
        ['Grog', 'Grog', 'hierarchy', 'parent=Mixed alcoholic beverages'],
    ])

    # ========================================================================
    # DEFERRED TAGS - REQUIRE SOURCE TEXT REVIEW OR RATIONALIZATION
    # ========================================================================
    # The following tags need further analysis before primary facet assignment:
    #
    # 1. Drunkeness (16 uses) - ✅ COMPLETED - TAG SPLIT REQUIRED - Manual re-tagging needed in Zotero
    #    The original "Drunkeness" tag has been split into two concepts:
    #
    #    A) "Drunkenness" → Events > Criminal events (10 instances)
    #       Court cases where people were charged/fined for public drunkenness:
    #       - "Jottings" (1891): "drunk cases at Katoomba Court"
    #       - "Moutains Mixtures" (1893): "drunk, disorderly... paid over 17s. 6d."
    #       - "Mountain Mixtures" (1894): "drunk and disorderly, paid 10s."
    #       - "Mountain Mixtures" (1893): "charge of drunkenness... fined"
    #       - "Katoomba Police Court" (1892): "fined the minimum for drunkenness"
    #       - "Newsettes" (1891): "drunkenness and disorderly conduct, fined 7s 6d"
    #       - "Newsettes" (1891): William Fell fined 12s 6d
    #       - "Mountain Mixtures" (1892): "Two drunks at Katoomba Court"
    #       - "Katoomba Court" (1893): "One drunk... paid 5s."
    #       - "Mountain Mixtures" (1891): "drunk cases at Katoomba Court"
    #
    #    B) "Drunkenness (intoxication)" → Associated Concepts > Physical and health conditions (6 instances)
    #       References to state of being intoxicated (not criminal proceedings):
    #       - "Police Court" (1904): "told Susan to go to bed as he was drunk"
    #       - "Katoomba Court" (1893): "they were drunk when they went to bed"
    #       - "Megalong Matters" (1892): "found them all gloriously drunk"
    #       - "Katoomba Court" (1893): testimony "I was drunk"
    #       - "Mountain Mixtures" (1893): "going down the pass... in a drunken coalition"
    #       - "Mountain Mixtures" (1892): "double the amount of drunkenness at black-diamond fields"
    #       - "Katoomba Municipal Elections" (1890): "No drunkenness or rowdyism was observable"
    #
    #    TODO: Manually re-tag these 16 Zotero items based on context above.
    #
    # 2. Accommodation (64 uses) - ✅ COMPLETED - DEPRECATED & RATIONALIZED
    #    Resolution: "Accommodation" tag deprecated and replaced with specific building types
    #    using Pattern A (Churches model) hierarchy structure:
    #
    #    New hierarchies created:
    #    - Built Environment > Accommodation buildings > Hotels > Hotel > [15+ specific hotels]
    #    - Built Environment > Accommodation buildings > Boarding houses > Boarding house > [specific]
    #    - Built Environment > Accommodation buildings > Cottages > Cottage (NEW category)
    #    - Built Environment > Accommodation buildings > Stables > Stable (NEW category)
    #
    #    Related additions:
    #    - Agents > People > Occupations > Hospitality workers > Hotelliers > Hotellier > [30+ individuals]
    #    - Agents > People > Occupations > Other goods and services > Coach and buggy business
    #    - Places > Towns: Added 9 new towns (Leura, Medlow, Mount Victoria, Hartley Vale, etc.)
    #    - Places > Towns > Katoomba > South Katoomba (sub-locality)
    #    - Places > Natural features > Gullies > Nellie's Glen
    #    - Agents > Animals > Cattle
    #
    #    Detailed retagging guidance: reports/accommodation_rationalization_report.md
    #    TODO: Manually re-tag 64 Zotero items using report as guide (3 items need full-text review)
    #
    # 3. Alcohol (12 uses) - Too broad. Appears in various contexts (legal
    #    testimony, inquests). May overlap with "Drinking" (activity). Needs
    #    context review to determine if should be: substance/material, activity,
    #    or merged with existing tags.
    #
    # 4. Post (9 uses) - Added to Activities > Communication activities > Postal
    #    services, but needs review to disambiguate post office (building) from
    #    postal service (activity). May need separate built environment entry.
    #
    # ========================================================================

    # ========================================================================
    # TODO: HIERARCHY STANDARDIZATION (Deferred to separate pass - Phase 2)
    # ========================================================================
    # ISSUE: Inconsistent intermediate hierarchy patterns across vocabulary
    #
    # PATTERN A (Churches model - CORRECT, adopted for new additions):
    #   Structure: Plural Parent (category) > Singular Generic > Specific Instances
    #   Purpose: Separates category navigation from taggable entities
    #   Example: Churches > Church > St Hilda's Church
    #            Hotels > Hotel > Carrington Hotel
    #            Hotelliers > Hotellier > Mrs Long
    #
    # PATTERN B (Flat model - INCONSISTENT, needs retrofit):
    #   Structure: Plural Parent (both category AND taggable) > Specific Instances
    #   Problem: Category serves dual purpose (navigation + tagging generic items)
    #   Examples: Clergy > Cardinal Moran (missing "Clergyman" intermediate)
    #             Medical professionals > Dr Spark (missing "Medical professional" intermediate)
    #
    # Categories already using Pattern A (✓ correct):
    #   - Churches > Church > [specific churches]
    #   - Hotels > Hotel > [specific hotels] (THIS implementation)
    #   - Hotelliers > Hotellier > [specific people] (THIS implementation)
    #   - Boarding houses > Boarding house > [specific] (THIS implementation)
    #   - Cottages > Cottage > [specific] (THIS implementation)
    #   - Stables > Stable > [specific] (THIS implementation)
    #   - Courts > Court > [specific courts]
    #   - Pubs > Pub (has generic intermediate)
    #   - Schools > School > [specific schools]
    #
    # Categories needing retrofit to Pattern A (⚠ inconsistent):
    #   - Clergy > [ADD: Clergyman] > Cardinal Moran, etc.
    #   - Medical professionals > [ADD: Medical professional] > Dr Spark, etc.
    #   - Law enforcement > [ADD: Police officer] > Constable Hamilton, etc.
    #   - Other occupation categories (audit needed)
    #
    # Rationale for Pattern A:
    #   1. Semantic clarity: Category vs instance vs generic concept are distinct
    #   2. Getty AAT alignment: Matches formal thesaurus structure
    #   3. Tagging clarity: Tag generic items with singular intermediate, not plural parent
    #   4. Poly-hierarchy support: Cleaner relationships when items appear in multiple hierarchies
    #   5. Future-proofing: Standard pattern for adding new categories
    #
    # Implementation plan:
    #   1. Create planning/hierarchy_standardization_plan.md
    #   2. Audit all plural parent categories across 7 primary facets
    #   3. Identify categories using Pattern B
    #   4. Add singular intermediates where missing
    #   5. Update visualizations and documentation
    #   6. Test and validate changes
    #
    # Estimated scope: ~5-6 categories, potentially ~200+ existing tags affected
    # Priority: Medium (cosmetic consistency, not breaking functionality)
    # Timeline: Separate focused pass after completing deferred items (Alcohol, Post)
    #
    # ========================================================================

    return rows


def generate_thematic_groupings():
    """
    Generate all thematic grouping hierarchies (domain-based).
    Tags appear here AS WELL AS in primary facets (poly-hierarchy).

    Returns:
        list: CSV rows for thematic parent relationships
    """
    rows = []

    # Note: These are SECONDARY parents - tags already have primary facet parents
    # Use format with "THEMATIC:" prefix in notes to distinguish

    # ========================================================================
    # THEME 1: HEALTH & MEDICINE
    # ========================================================================

    rows.extend([
        ['Health & Medicine', 'Health & Medicine', 'hierarchy', 'parent=(thematic grouping)'],
        ['Medical professionals', 'Medical professionals', 'hierarchy', 'parent=Health & Medicine - THEMATIC'],
        ['Health conditions', 'Health conditions', 'hierarchy', 'parent=Health & Medicine - THEMATIC'],
        ['Illness', 'Illness', 'hierarchy', 'parent=Health conditions - THEMATIC'],
        ['Disease', 'Disease', 'hierarchy', 'parent=Health conditions - THEMATIC'],
        ['Injury', 'Injury', 'hierarchy', 'parent=Health conditions - THEMATIC'],
        ['Death', 'Death', 'hierarchy', 'parent=Health conditions - THEMATIC'],
        ['Health-related events', 'Health-related events', 'hierarchy', 'parent=Health & Medicine - THEMATIC'],
        ['Accident', 'Accident', 'hierarchy', 'parent=Health-related events - THEMATIC'],
        ['Mining accidents', 'Mining accidents', 'hierarchy', 'parent=Health-related events - THEMATIC'],
    ])

    # ========================================================================
    # THEME 2: EDUCATION
    # ========================================================================

    rows.extend([
        ['Education', 'Education', 'hierarchy', 'parent=(thematic grouping)'],
        ['Educational buildings', 'Educational buildings', 'hierarchy', 'parent=Education - THEMATIC'],
        ['Sunday school', 'Sunday school', 'hierarchy', 'parent=Education - THEMATIC (religious education)'],
    ])

    # ========================================================================
    # THEME 3: RELIGION
    # ========================================================================

    rows.extend([
        ['Religion', 'Religion', 'hierarchy', 'parent=(thematic grouping)'],
        ['Religious organizations', 'Religious organizations', 'hierarchy', 'parent=Religion - THEMATIC'],
        ['Religious buildings', 'Religious buildings', 'hierarchy', 'parent=Religion - THEMATIC'],
        ['Clergy', 'Clergy', 'hierarchy', 'parent=Religion - THEMATIC'],
        ['Cardinal Moran', 'Cardinal Moran', 'hierarchy', 'parent=Religion - THEMATIC (religious figure)'],
    ])

    # ========================================================================
    # THEME 4: JUSTICE & CRIME
    # ========================================================================

    rows.extend([
        ['Justice & Crime', 'Justice & Crime', 'hierarchy', 'parent=(thematic grouping)'],
        ['Courts', 'Courts', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Court buildings', 'Court buildings', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Legal events', 'Legal events', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Law enforcement', 'Law enforcement', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Police station', 'Police station', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Legal officials', 'Legal officials', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],

        # Crimes
        ['Crimes', 'Crimes', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Violent crimes', 'Violent crimes', 'hierarchy', 'parent=Crimes - THEMATIC'],
        ['Assault', 'Assault', 'hierarchy', 'parent=Violent crimes - THEMATIC'],
        ['Fighting', 'Fighting', 'hierarchy', 'parent=Violent crimes - THEMATIC'],
        ['Rape', 'Rape', 'hierarchy', 'parent=Violent crimes - THEMATIC'],
        ['Sexual violence', 'Sexual violence', 'hierarchy', 'parent=Violent crimes - THEMATIC'],
        ['Property crimes', 'Property crimes', 'hierarchy', 'parent=Crimes - THEMATIC'],
        ['Theft', 'Theft', 'hierarchy', 'parent=Property crimes - THEMATIC'],
        ['Social order offences', 'Social order offences', 'hierarchy', 'parent=Crimes - THEMATIC'],
        ['Drunkenness', 'Drunkenness', 'hierarchy', 'parent=Social order offences - THEMATIC'],
        ['Gambling', 'Gambling', 'hierarchy', 'parent=Social order offences - THEMATIC'],
        ['Desertion', 'Desertion', 'hierarchy', 'parent=Social order offences - THEMATIC'],
        ['Other crimes', 'Other crimes', 'hierarchy', 'parent=Crimes - THEMATIC'],
        ['Bigamy', 'Bigamy', 'hierarchy', 'parent=Other crimes - THEMATIC'],

        # Victims (thematic grouping - virtual)
        ['Victims of crime & violence', 'Victims of crime & violence', 'hierarchy', 'parent=Justice & Crime - THEMATIC (virtual grouping)'],
        ['Widows', 'Widows', 'hierarchy', 'parent=Victims of crime & violence - THEMATIC'],

        # Legal outcomes
        ['Legal outcomes', 'Legal outcomes', 'hierarchy', 'parent=Justice & Crime - THEMATIC'],
        ['Divorce', 'Divorce', 'hierarchy', 'parent=Legal outcomes - THEMATIC'],
        ['Bankruptcy', 'Bankruptcy', 'hierarchy', 'parent=Legal outcomes - THEMATIC'],
    ])

    # ========================================================================
    # THEME 5: MINING & INDUSTRY
    # ========================================================================

    rows.extend([
        ['Mining & Industry', 'Mining & Industry', 'hierarchy', 'parent=(thematic grouping)'],
        ['Mining companies', 'Mining companies', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Mines & mining districts', 'Mines & mining districts', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Shale mines', 'Shale mines', 'hierarchy', 'parent=Mines & mining districts - THEMATIC'],
        ['Coal mining', 'Coal mining', 'hierarchy', 'parent=Mines & mining districts - THEMATIC'],
        ['Mining workforce', 'Mining workforce', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Miners', 'Miners', 'hierarchy', 'parent=Mining workforce - THEMATIC'],
        ['Miners\' families', 'Miners\' families', 'hierarchy', 'parent=Mining workforce - THEMATIC'],
        ['Miners\' dwellings', 'Miners\' dwellings', 'hierarchy', 'parent=Mining workforce - THEMATIC'],
        ['Mining activities', 'Mining activities', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Mining', 'Mining', 'hierarchy', 'parent=Mining activities - THEMATIC'],
        ['Mine closure', 'Mine closure', 'hierarchy', 'parent=Mining activities - THEMATIC'],
        ['Recreation for miners', 'Recreation for miners', 'hierarchy', 'parent=Mining activities - THEMATIC'],
        ['Mining infrastructure', 'Mining infrastructure', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Mining settlements', 'Mining settlements', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Mining incidents', 'Mining incidents', 'hierarchy', 'parent=Mining & Industry - THEMATIC'],
        ['Mining accidents', 'Mining accidents', 'hierarchy', 'parent=Mining incidents - THEMATIC'],
        ['Accident', 'Accident', 'hierarchy', 'parent=Mining incidents - THEMATIC'],
    ])

    # ========================================================================
    # THEME 6: ALCOHOL & TEMPERANCE
    # ========================================================================

    rows.extend([
        ['Alcohol & Temperance', 'Alcohol & Temperance', 'hierarchy', 'parent=(thematic grouping)'],
        ['Alcohol-related venues', 'Alcohol-related venues', 'hierarchy', 'parent=Alcohol & Temperance - THEMATIC'],
        ['Hotels', 'Hotels', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'],
        ['Pubs', 'Pubs', 'hierarchy', 'parent=Alcohol-related venues - THEMATIC'],
        ['Temperance organizations & movements', 'Temperance organizations & movements', 'hierarchy', 'parent=Alcohol & Temperance - THEMATIC'],
        ['Good Templars', 'Good Templars', 'hierarchy', 'parent=Temperance organizations & movements - THEMATIC'],
        ['Temperance', 'Temperance', 'hierarchy', 'parent=Temperance organizations & movements - THEMATIC'],
        ['Alcohol consumption & behaviour', 'Alcohol consumption & behaviour', 'hierarchy', 'parent=Alcohol & Temperance - THEMATIC'],
        ['Alcoholic beverages', 'Alcoholic beverages', 'hierarchy', 'parent=Alcohol consumption & behaviour - THEMATIC'],
        ['Drinking (alcohol)', 'Drinking (alcohol)', 'hierarchy', 'parent=Alcohol consumption & behaviour - THEMATIC'],
        ['Drunkenness', 'Drunkenness', 'hierarchy', 'parent=Alcohol consumption & behaviour - THEMATIC'],
        ['Drunkenness (intoxication)', 'Drunkenness (intoxication)', 'hierarchy', 'parent=Alcohol consumption & behaviour - THEMATIC'],
        ['Licensing & regulation', 'Licensing & regulation', 'hierarchy', 'parent=Alcohol & Temperance - THEMATIC'],
        ['Licensing', 'Licensing', 'hierarchy', 'parent=Licensing & regulation - THEMATIC'],
        ['Licensing Act', 'Licensing Act', 'hierarchy', 'parent=Licensing & regulation - THEMATIC'],
        ['Licensing Court', 'Licensing Court', 'hierarchy', 'parent=Licensing & regulation - THEMATIC'],
        ['Licensing inspector', 'Licensing inspector', 'hierarchy', 'parent=Licensing & regulation - THEMATIC'],
        ['Publican\'s License', 'Publican\'s License', 'hierarchy', 'parent=Licensing & regulation - THEMATIC'],
        ['Hospitality workers', 'Hospitality workers', 'hierarchy', 'parent=Alcohol & Temperance - THEMATIC'],
    ])

    # ========================================================================
    # THEME 7: SPORT & RECREATION
    # ========================================================================

    rows.extend([
        ['Sport & Recreation', 'Sport & Recreation', 'hierarchy', 'parent=(thematic grouping)'],
        ['Sporting events', 'Sporting events', 'hierarchy', 'parent=Sport & Recreation - THEMATIC'],
        ['Sports clubs', 'Sports clubs', 'hierarchy', 'parent=Sport & Recreation - THEMATIC'],
        ['Recreation themes', 'Recreation themes', 'hierarchy', 'parent=Sport & Recreation - THEMATIC'],
        ['Recreation for miners', 'Recreation for miners', 'hierarchy', 'parent=Recreation themes - THEMATIC'],
        ['Sports', 'Sports', 'hierarchy', 'parent=Recreation themes - THEMATIC'],
        ['Reserves', 'Reserves', 'hierarchy', 'parent=Recreation themes - THEMATIC (recreational lands)'],
    ])

    # ========================================================================
    # THEME 8: ARTS & CULTURE
    # ========================================================================

    rows.extend([
        ['Arts & Culture', 'Arts & Culture', 'hierarchy', 'parent=(thematic grouping)'],
        ['Cultural organizations', 'Cultural organizations', 'hierarchy', 'parent=Arts & Culture - THEMATIC'],
        ['Cultural venues', 'Cultural venues', 'hierarchy', 'parent=Arts & Culture - THEMATIC'],
        ['Halls', 'Halls', 'hierarchy', 'parent=Cultural venues - THEMATIC'],
        ['Cultural events', 'Cultural events', 'hierarchy', 'parent=Arts & Culture - THEMATIC'],
        ['Cultural activities', 'Cultural activities', 'hierarchy', 'parent=Arts & Culture - THEMATIC'],
        ['Advertising', 'Advertising', 'hierarchy', 'parent=Cultural activities - THEMATIC'],
    ])

    # ========================================================================
    # THEME 9: COMMUNITY INSTITUTIONS
    # ========================================================================

    rows.extend([
        ['Community institutions', 'Community institutions', 'hierarchy', 'parent=(thematic grouping)'],
        ['Civic organizations', 'Civic organizations', 'hierarchy', 'parent=Community institutions - THEMATIC'],
        ['Civic buildings', 'Civic buildings', 'hierarchy', 'parent=Community institutions - THEMATIC'],
        ['Fraternal orders & lodges', 'Fraternal orders & lodges', 'hierarchy', 'parent=Community institutions - THEMATIC'],
        ['Cultural & recreational organizations', 'Cultural & recreational organizations', 'hierarchy', 'parent=Community institutions - THEMATIC'],
        ['Community buildings', 'Community buildings', 'hierarchy', 'parent=Community institutions - THEMATIC'],
    ])

    # ========================================================================
    # THEME 10: SOCIAL ISSUES
    # ========================================================================

    rows.extend([
        ['Social issues', 'Social issues', 'hierarchy', 'parent=(thematic grouping)'],
        ['Economic hardship', 'Economic hardship', 'hierarchy', 'parent=Social issues - THEMATIC'],
        ['Unemployment', 'Unemployment', 'hierarchy', 'parent=Economic hardship - THEMATIC'],
        ['Unemployment relief', 'Unemployment relief', 'hierarchy', 'parent=Economic hardship - THEMATIC'],
        ['Charity', 'Charity', 'hierarchy', 'parent=Economic hardship - THEMATIC'],
        ['Bankruptcy', 'Bankruptcy', 'hierarchy', 'parent=Economic hardship - THEMATIC'],
        ['Vulnerable populations', 'Vulnerable populations', 'hierarchy', 'parent=Social issues - THEMATIC'],
        ['Widows', 'Widows', 'hierarchy', 'parent=Vulnerable populations - THEMATIC'],
        ['Miners\' families', 'Miners\' families', 'hierarchy', 'parent=Vulnerable populations - THEMATIC'],
        ['Children', 'Children', 'hierarchy', 'parent=Vulnerable populations - THEMATIC'],
        ['Victims of crime & violence', 'Victims of crime & violence', 'hierarchy', 'parent=Social issues - THEMATIC (virtual grouping)'],
    ])

    # ========================================================================
    # THEME 11: RACE & ETHNICITY
    # ========================================================================

    rows.extend([
        ['Race & Ethnicity', 'Race & Ethnicity', 'hierarchy', 'parent=(thematic grouping)'],
        ['Marginalised groups', 'Marginalised groups', 'hierarchy', 'parent=Race & Ethnicity - THEMATIC'],
        ['Indigenous peoples', 'Indigenous peoples', 'hierarchy', 'parent=Marginalised groups - THEMATIC'],
        ['Aboriginal people', 'Aboriginal people', 'hierarchy', 'parent=Indigenous peoples - THEMATIC'],
        ['Corroboree', 'Corroboree', 'hierarchy', 'parent=Indigenous peoples - THEMATIC'],
        ['Aborigines\' Protection Board', 'Aborigines\' Protection Board', 'hierarchy', 'parent=Indigenous peoples - THEMATIC'],
        ['Chinese community', 'Chinese community', 'hierarchy', 'parent=Marginalised groups - THEMATIC'],
        ['Chinese people', 'Chinese people', 'hierarchy', 'parent=Chinese community - THEMATIC'],
        ['Racial stereotyping & performance', 'Racial stereotyping & performance', 'hierarchy', 'parent=Race & Ethnicity - THEMATIC'],
        ['Minstrel shows', 'Minstrel shows', 'hierarchy', 'parent=Racial stereotyping & performance - THEMATIC'],
        ['Katoomba Amateur Minstrels', 'Katoomba Amateur Minstrels', 'hierarchy', 'parent=Minstrel shows - THEMATIC'],
        ['Cultural identity & heritage', 'Cultural identity & heritage', 'hierarchy', 'parent=Race & Ethnicity - THEMATIC'],
        ['Reference to the Irish or Irish culture', 'Reference to the Irish or Irish culture', 'hierarchy', 'parent=Cultural identity & heritage - THEMATIC'],
    ])

    # ========================================================================
    # THEME 12: WOMEN & GENDER
    # ========================================================================

    rows.extend([
        ['Women & Gender', 'Women & Gender', 'hierarchy', 'parent=(thematic grouping)'],
        ['Women as demographic group', 'Women as demographic group', 'hierarchy', 'parent=Women & Gender - THEMATIC'],
        ['Women', 'Women', 'hierarchy', 'parent=Women as demographic group - THEMATIC'],
        ['Girls\' cricket', 'Girls\' cricket', 'hierarchy', 'parent=Women as demographic group - THEMATIC'],
        ['Gender-related vulnerabilities', 'Gender-related vulnerabilities', 'hierarchy', 'parent=Women & Gender - THEMATIC'],
        ['Widows', 'Widows', 'hierarchy', 'parent=Gender-related vulnerabilities - THEMATIC'],
        ['Sexual violence', 'Sexual violence', 'hierarchy', 'parent=Gender-related vulnerabilities - THEMATIC'],
        ['Rape', 'Rape', 'hierarchy', 'parent=Gender-related vulnerabilities - THEMATIC'],
    ])

    # ========================================================================
    # THEME 13: FAMILY & DOMESTIC LIFE
    # ========================================================================

    rows.extend([
        ['Family & Domestic Life', 'Family & Domestic Life', 'hierarchy', 'parent=(thematic grouping)'],
        ['Families', 'Families', 'hierarchy', 'parent=Family & Domestic Life - THEMATIC (all family tags)'],
        ['Miners\' families', 'Miners\' families', 'hierarchy', 'parent=Families - THEMATIC'],
        ['Family members by demographic', 'Family members by demographic', 'hierarchy', 'parent=Family & Domestic Life - THEMATIC'],
        ['Women', 'Women', 'hierarchy', 'parent=Family members by demographic - THEMATIC'],
        ['Men', 'Men', 'hierarchy', 'parent=Family members by demographic - THEMATIC'],
        ['Children', 'Children', 'hierarchy', 'parent=Family members by demographic - THEMATIC'],
        ['Widows', 'Widows', 'hierarchy', 'parent=Family members by demographic - THEMATIC'],
        ['Life events', 'Life events', 'hierarchy', 'parent=Family & Domestic Life - THEMATIC'],
        ['Domestic accommodation', 'Domestic accommodation', 'hierarchy', 'parent=Family & Domestic Life - THEMATIC'],
        ['Miners\' dwellings', 'Miners\' dwellings', 'hierarchy', 'parent=Domestic accommodation - THEMATIC'],
        ['Boarding houses', 'Boarding houses', 'hierarchy', 'parent=Domestic accommodation - THEMATIC'],
        ['Hotels', 'Hotels', 'hierarchy', 'parent=Domestic accommodation - THEMATIC (residential aspect)'],
    ])

    # ========================================================================
    # THEME 14: ECONOMY & LABOUR
    # ========================================================================

    rows.extend([
        ['Economy & Labour', 'Economy & Labour', 'hierarchy', 'parent=(thematic grouping)'],
        ['Industries', 'Industries', 'hierarchy', 'parent=Economy & Labour - THEMATIC'],
        ['Mining', 'Mining', 'hierarchy', 'parent=Industries - THEMATIC'],
        ['Tourism', 'Tourism', 'hierarchy', 'parent=Industries - THEMATIC'],
        ['Businesses', 'Businesses', 'hierarchy', 'parent=Economy & Labour - THEMATIC'],
        ['Commercial businesses', 'Commercial businesses', 'hierarchy', 'parent=Businesses - THEMATIC'],
        ['Labour relations', 'Labour relations', 'hierarchy', 'parent=Economy & Labour - THEMATIC'],
        ['Strike', 'Strike', 'hierarchy', 'parent=Labour relations - THEMATIC'],
        ['Unions', 'Unions', 'hierarchy', 'parent=Labour relations - THEMATIC'],
        ['Workforce', 'Workforce', 'hierarchy', 'parent=Economy & Labour - THEMATIC'],
        ['Miners', 'Miners', 'hierarchy', 'parent=Workforce - THEMATIC'],
        ['Economic distress', 'Economic distress', 'hierarchy', 'parent=Economy & Labour - THEMATIC'],
        ['Unemployment', 'Unemployment', 'hierarchy', 'parent=Economic distress - THEMATIC'],
        ['Unemployment relief', 'Unemployment relief', 'hierarchy', 'parent=Economic distress - THEMATIC'],
        ['Bankruptcy', 'Bankruptcy', 'hierarchy', 'parent=Economic distress - THEMATIC'],
    ])

    # ========================================================================
    # THEME 15: TRANSPORT & INFRASTRUCTURE
    # ========================================================================

    rows.extend([
        ['Transport & Infrastructure', 'Transport & Infrastructure', 'hierarchy', 'parent=(thematic grouping)'],
        ['Railway', 'Railway', 'hierarchy', 'parent=Transport & Infrastructure - THEMATIC'],
        ['Roads', 'Roads', 'hierarchy', 'parent=Transport & Infrastructure - THEMATIC'],
        ['Mining transport', 'Mining transport', 'hierarchy', 'parent=Transport & Infrastructure - THEMATIC'],
        ['Tramway', 'Tramway', 'hierarchy', 'parent=Mining transport - THEMATIC'],
        ['Commercial transport', 'Commercial transport', 'hierarchy', 'parent=Transport & Infrastructure - THEMATIC'],
        ['Trucking', 'Trucking', 'hierarchy', 'parent=Commercial transport - THEMATIC'],
        ['Utilities', 'Utilities', 'hierarchy', 'parent=Transport & Infrastructure - THEMATIC'],
    ])

    # ========================================================================
    # THEME 16: TOURISM & ACCOMMODATION
    # ========================================================================

    rows.extend([
        ['Tourism & Accommodation', 'Tourism & Accommodation', 'hierarchy', 'parent=(thematic grouping)'],
        ['Tourism activities', 'Tourism activities', 'hierarchy', 'parent=Tourism & Accommodation - THEMATIC'],
        ['Tourism', 'Tourism', 'hierarchy', 'parent=Tourism activities - THEMATIC'],
        ['Tourist trains', 'Tourist trains', 'hierarchy', 'parent=Tourism activities - THEMATIC'],
        ['Accommodation', 'Accommodation', 'hierarchy', 'parent=Tourism & Accommodation - THEMATIC'],
        ['Tourist attractions', 'Tourist attractions', 'hierarchy', 'parent=Tourism & Accommodation - THEMATIC'],
        ['Waterfalls', 'Waterfalls', 'hierarchy', 'parent=Tourist attractions - THEMATIC'],
        ['Jenolan Caves', 'Jenolan Caves', 'hierarchy', 'parent=Tourist attractions - THEMATIC'],
        ['Natural features', 'Natural features', 'hierarchy', 'parent=Tourist attractions - THEMATIC'],
    ])

    # ========================================================================
    # THEME 17: POLITICS & GOVERNANCE
    # ========================================================================

    rows.extend([
        ['Politics & Governance', 'Politics & Governance', 'hierarchy', 'parent=(thematic grouping)'],
        ['Government bodies', 'Government bodies', 'hierarchy', 'parent=Politics & Governance - THEMATIC'],
        ['Political events', 'Political events', 'hierarchy', 'parent=Politics & Governance - THEMATIC'],
        ['Public officials', 'Public officials', 'hierarchy', 'parent=Politics & Governance - THEMATIC'],
    ])

    # ========================================================================
    # THEME 18: MILITARY & WAR
    # ========================================================================

    rows.extend([
        ['Military & War', 'Military & War', 'hierarchy', 'parent=(thematic grouping)'],
        ['Military events', 'Military events', 'hierarchy', 'parent=Military & War - THEMATIC'],
        ['World War I', 'World War I', 'hierarchy', 'parent=Military events - THEMATIC'],
        ['Military personnel', 'Military personnel', 'hierarchy', 'parent=Military & War - THEMATIC'],
        ['Military organizations', 'Military organizations', 'hierarchy', 'parent=Military & War - THEMATIC'],
        ['Military', 'Military', 'hierarchy', 'parent=Military organizations - THEMATIC'],
    ])

    # ========================================================================
    # THEME 19: ENVIRONMENT & WEATHER
    # ========================================================================

    rows.extend([
        ['Environment & Weather', 'Environment & Weather', 'hierarchy', 'parent=(thematic grouping)'],
        ['Weather & climate', 'Weather & climate', 'hierarchy', 'parent=Environment & Weather - THEMATIC'],
        ['Weather', 'Weather', 'hierarchy', 'parent=Weather & climate - THEMATIC'],
        ['Natural features', 'Natural features', 'hierarchy', 'parent=Environment & Weather - THEMATIC'],
        ['Animals', 'Animals', 'hierarchy', 'parent=Environment & Weather - THEMATIC'],
        ['Natural resources', 'Natural resources', 'hierarchy', 'parent=Environment & Weather - THEMATIC'],
        ['Coal', 'Coal', 'hierarchy', 'parent=Natural resources - THEMATIC'],
        ['Shale mines', 'Shale mines', 'hierarchy', 'parent=Natural resources - THEMATIC'],
    ])

    # ========================================================================
    # THEME 20: COMMUNICATIONS & POSTAL SERVICES
    # ========================================================================

    rows.extend([
        ['Communications & Postal Services', 'Communications & Postal Services', 'hierarchy', 'parent=(thematic grouping)'],
        ['Postal services', 'Postal services', 'hierarchy', 'parent=Communications & Postal Services - THEMATIC'],
        ['Post office', 'Post office', 'hierarchy', 'parent=Postal services - THEMATIC'],
        ['Post', 'Post', 'hierarchy', 'parent=Postal services - THEMATIC'],
        ['Advertising', 'Advertising', 'hierarchy', 'parent=Communications & Postal Services - THEMATIC'],
        ['Information Forms', 'Information Forms', 'hierarchy', 'parent=Communications & Postal Services - THEMATIC'],
    ])

    return rows


def main():
    """Generate complete poly-hierarchical taxonomy CSV."""
    print("Generating comprehensive poly-hierarchical taxonomy...")
    print()

    # Generate primary facets
    print("Generating primary facet hierarchies...")
    primary_rows = generate_primary_facets()
    print(f"  Generated {len(primary_rows)} primary facet relationships")

    # Generate thematic groupings
    print("Generating thematic grouping hierarchies...")
    thematic_rows = generate_thematic_groupings()
    print(f"  Generated {len(thematic_rows)} thematic relationships")

    # Combine
    all_rows = primary_rows + thematic_rows
    print()
    print(f"TOTAL: {len(all_rows)} new hierarchy relationships")
    print()

    # Write to output file
    output_file = Path('data/poly_hierarchy_additions.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['old_tag', 'new_tag', 'action', 'notes'])
        writer.writerows(all_rows)

    print(f"Written to: {output_file}")
    print()
    print("Next steps:")
    print("1. Review generated CSV")
    print("2. Append to tag_consolidation_map.csv")
    print("3. Generate hierarchy visualization")
    print("4. Update folksonomy_logic.md")


if __name__ == '__main__':
    main()
