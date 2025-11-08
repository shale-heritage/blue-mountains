# Orphaned Tags - Final Report

**Date**: 2025-11-04
**Starting orphans**: 162
**Current orphans**: 123
**Resolved**: 39 tags

## Changes Completed

### ✓ Name Synonyms Added (2)
- Mr Charles George Gordon → Major Sir Charles George Gordon
- Mr David Brown → Mr D Brown

### ✓ Family Names Added (16)
All added to `people > families`:
- Austin family
- Brydon family
- Davey family
- Eaton family
- Evans family
- Flynn family
- Gordon family
- Goyder family (with child: Goyder brothers)
- Hartman family
- Husband family
- Meredith family
- Peckman family
- Penman family
- Tabrett family
- Watkins family

### ✓ Place Names Added (12)
All added to `Places > towns`:
- Bathurst
- Burragorang
- Capertee
- Lawson
- Newcastle
- Oberon
- Parramatta
- Penrith
- Port Kembla
- Rockley
- Springwood
- Sunny Corner

**Note**: Katoomba Street flagged for individual review (not automatically added to towns).

### ✓ Company Synonyms Added (5)
- A.K.O. & M. Company → Australian Kerosene Oil and Mineral Company
- Australian Kerosene Shale and Oil Company → Australian Kerosene Oil and Mineral Company
- New South Wales Shale and Oil Co. → New South Wales Shale and Oil Company
- South Clifton Mine Co. → South Clifton Mine Company
- Waudby & Co. → Waudby and Company

### ✓ New Companies Added (2)
- Gladstone Coal Company (parent: mining companies)
- Sunny Corner Mining Company (parent: mining companies)

### ✓ Other Mappings Added (2)
- suicide → life events > death > suicide
- Publican's License (US spelling) → publican's licence (UK spelling)

## Remaining Orphans (123 tags)

### 1. Person Names (111 tags - EXPECTED)

These are individual person names not currently in the taxonomy. This is expected behaviour - they will be preserved during tag rewrite.

**Status**: No action needed. These tags will remain on items during rewrite.

<details>
<summary>View all 111 person names</summary>

- Miss Bradley
- Miss Edwards
- Miss Eva Peckman
- Miss Levina Kitch
- Miss Nellie North
- Mr A J Parcell
- Mr A Thorneycroft
- Mr A W Stephen
- Mr Ah Narm
- Mr Allan West
- Mr Arthur L Morris
- Mr Arthur Wright
- Mr Banfield
- Mr C J Ellis
- Mr C W Craig
- Mr Charles E Hoffman
- Mr Charles Pratt
- Mr Charles Wooller
- Mr Christopher Webb
- Mr Clydesdale
- Mr D J Dunbar
- Mr D Morsby
- Mr D O'Keefe
- Mr Dalwood
- Mr David Hamilton
- Mr Douglass
- Mr E E Medlicott
- Mr E Jordan
- Mr Edward J Delaney
- Mr Edward Pearson
- Mr Frederick Charles Goyder
- Mr G Donald
- Mr G Griffiths
- Mr G R Dibbs
- Mr G W Spring
- Mr Gannon
- Mr George Bremmer Dunn
- Mr George Frederick Goyder
- Mr George H Cooper
- Mr George Susans
- Mr H Roberts
- Mr J Annesley
- Mr J B North
- Mr J H Humbley
- Mr J K Cleeve
- Mr J R Nash
- Mr John Duff
- Mr John Fitzpatrick
- Mr John Geggie
- Mr John Henry Mitchell
- Mr John Hurley
- Mr John Norton
- Mr John Still O'Hara
- Mr John W Fletcher
- Mr Jones
- Mr Joseph Cook
- Mr Joseph Edwards
- Mr Joseph Nimmo
- Mr Kitch
- Mr L H Howell
- Mr Lewis Duff
- Mr Louis Cohen
- Mr Mark Foy
- Mr Messitter
- Mr Neate
- Mr Nick Zimmo
- Mr O Purslow
- Mr O'Hare
- Mr O'Sullivan
- Mr Owen Owens
- Mr P McAviney
- Mr P Mullany
- Mr Parker
- Mr Penrose
- Mr Percy Hammond
- Mr Peter O'Donnell
- Mr Preston
- Mr R J Bronger
- Mr Ralph Hartman
- Mr Robert Brydon
- Mr Robert H Esgate
- Mr Robert Russell
- Mr Rodrigeuz
- Mr Rubina Fryer
- Mr S E Hewett
- Mr Samuel Austin
- Mr Sheard
- Mr Stanley Gayfer
- Mr T J Cale
- Mr T Tiernan
- Mr Thomas Austin
- Mr Thomas Cook
- Mr Thomas Hollins
- Mr W Hocking
- Mr W J Hart
- Mr W McMillan
- Mr Wilfred Moss
- Mr Wrench
- Mr Zack Nimmo
- Mrs Christina Brydon
- Mrs Elizabeth Nimmo
- Mrs Ellen Hoffman (nee Gavin)
- Mrs Emma Matilda Waudby (nee Phair)
- Mrs Evelyn Gordon (nee Günther)
- Mrs Grace Richmond Battram (nee Jones)
- Mrs Isabella Long (nee Clune)
- Mrs Mary Duff (nee Evans)
- Mrs Percy Fowles (nee Nimmo)
- Mrs Rose Anna (Fanny) Lynch (nee Fisher)
- Mrs S Hindman
- Ms May Porter

</details>

### 2. Tags Requiring Decisions (12 tags)

| Tag | Issue | Recommendation |
|-----|-------|---------------|
| **Primary source** | Metadata tag | User confirmed: preserve separately during rewrite |
| **Alcohol** | Very broad category | User confirmed: already dealt with (consolidated to alcoholic beverages) |
| **Carrington** | Ambiguous reference | Investigate: Place? Person? Hotel variant? |
| **Colliery** | Mining term | Map as synonym to "coal mine"? |
| **Druid's Lodge** | Lodge name variant | Map as synonym to "Druid's Lodge (local lodge)"? |
| **Girls' cricket** | Gender-specific sport | Add as subcategory under cricket, or preserve as-is? |
| **Katoomba Coal and Shale Mines** | Facility name variant | Research: same as "Katoomba Coal Mines" or different? |
| **Katoomba South mines** | New mine facility | Add to Built Environment > mines > coal mines? |
| **Katoomba Street** | Street name | Flagged for review - add to Places with appropriate parent? |
| **Maps** | Document type | Add to Associated Concepts as document type? |
| **Mining settlements** | Settlement category | Add to Places > towns or as separate category? |
| **Rifle reserves** | Military unit variant | Map as synonym to "volunteer rifle reserves"? |

## Summary

**What was accomplished:**
- Added 39 missing mappings
- 2 new company names added to taxonomy
- 16 family names added
- 12 town names added
- No regressions detected

**What remains:**
- 111 person names (expected - will be preserved)
- 12 tags needing decisions

**Quality assurance results:**
- ✓ No spurious primary facets
- ✓ All families correctly placed in Agents > people > families
- ✓ All towns correctly placed in Places > towns
- ✓ Suicide correctly placed in Events > life events > death
- ✓ All company synonyms mapping correctly

## Recommendations

1. **For the 12 undecided tags**: Review each individually and decide whether to:
   - Map to existing terms
   - Add as new terms
   - Document as intentionally excluded

2. **For person names**: Document strategy in folksonomy_logic.md:
   - Keep unmapped person names as folksonomy tags
   - OR map all to occupational categories
   - OR preserve only "significant" individuals per Getty ULAN practice

3. **Next step**: Proceed with tag rewrite process once decisions made on remaining 12 tags.
