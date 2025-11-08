# Orphaned Tags Analysis

**Date**: 2025-11-04
**Total orphaned tags**: 162
**Capitalization-only differences**: 103 (will be auto-corrected)

## Summary by Category

### 1. Person Names (109 tags)

Individual person names with no mapping. These may be intentionally excluded from the taxonomy if the project uses a "People - THEMATIC" grouping rather than individual names.

<details>
<summary>View all person names (click to expand)</summary>

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
- Mr Charles George Gordon
- Mr Charles Pratt
- Mr Charles Wooller
- Mr Christopher Webb
- Mr Clydesdale
- Mr D J Dunbar
- Mr D Morsby
- Mr D O'Keefe
- Mr Dalwood
- Mr David Brown
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

**Recommendation**: Check if these should be:
- Mapped to generic occupational categories
- Preserved as named individuals (per Getty AAT ULAN practice)
- Removed as overly granular folksonomy

### 2. Family Names (12 tags)

- Austin family
- Brydon family
- Davey family
- Eaton family
- Evans family
- Flynn family
- Gordon family
- Goyder family (note: "Goyder brothers" also orphaned)
- Hartman family
- Husband family
- Meredith family
- Peckman family
- Penman family
- Tabrett family
- Watkins family

**Current mapping**: Has "families" category with "Delaney family" and "Greenbank family"

**Recommendation**: Add these to the families category if validated in sources.

### 3. Place Names (13 tags)

Towns/localities not currently mapped:

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
- Katoomba Street (specific street vs. town)

**Recommendation**: Add to Places facet > towns (except Katoomba Street which needs specific handling).

### 4. Mining Companies (6 tags)

**Issues with company names**:

| Current tag (orphaned) | Likely target | Issue |
|------------------------|---------------|-------|
| A.K.O. & M. Company | Australian Kerosene Oil and Mineral Company | Abbreviated form |
| Australian Kerosene Shale and Oil Company | Australian Kerosene Oil and Mineral Company? | Variant name or different company? |
| Gladstone Coal Company | (not mapped) | Missing |
| New South Wales Shale and Oil Co. | New South Wales Shale and Oil Company | Abbreviated form |
| South Clifton Mine Co. | South Clifton Mine Company | Abbreviated form |
| Sunny Corner Mining Company | (not mapped) | Missing |
| Waudby & Co. | Waudby and Company | Abbreviated form |

**Recommendation**:
- Add synonym mappings for abbreviated forms
- Research and add missing companies if validated

### 5. Mining Locations (3 tags)

- Katoomba Coal and Shale Mines (vs. "Katoomba Coal Mines" which is mapped)
- Katoomba South mines (not mapped)
- Mining settlements (generic category?)

**Recommendation**:
- Clarify relationship between "Katoomba Coal and Shale Mines" and company/mine distinction
- Add "Katoomba South mines" if validated
- Determine if "Mining settlements" should be a category in Places or Built Environment

### 6. Variant Spellings/Punctuation (2 tags)

- Publican's License → should map to "Publican's Licence" (UK spelling)
- Druid's Lodge → should map to "Druid's Lodge (local lodge)"?

**Recommendation**: Add synonym mappings.

### 7. Potentially Intentionally Removed (4 tags)

- **Primary source**: Metadata tag, not subject tag. Decision needed.
- **Maps**: Material type or document type? Not in current Materials facet.
- **Alcohol**: Very broad category - may have been intentionally consolidated into "alcoholic beverages"
- **Carrington**: Unclear - place name, hotel name, or person name? "Carrington Hotel" is mapped.

**Recommendation**: Document decision if intentionally removed, or add mapping if overlooked.

### 8. Potentially Missing Categories (4 tags)

- **Colliery**: Synonym for "mine" or "coal mine"?
- **Girls' cricket**: Specific sport subcategory not in current taxonomy
- **Rifle reserves**: Military/volunteer units - variant of "volunteer rifle reserves"?
- **Suicide**: Death-related event type not currently mapped

**Recommendation**:
- Add "colliery" as synonym for coal mine
- Evaluate if gender-specific sports need subcategories
- Check "rifle reserves" vs "volunteer rifle reserves" relationship
- Add "suicide" to life events if appropriate

## Actions Required

1. **Places** (13 tags): Add missing town names to Places facet
2. **Families** (15 tags): Add family names to families category
3. **Company synonyms** (4 tags): Add abbreviated forms as synonyms
4. **Missing companies** (2 tags): Research and add if validated
5. **Variant spellings** (2 tags): Add as synonyms
6. **Person names** (109 tags): Strategic decision needed on granularity
7. **Special cases** (8 tags): Individual review required

## Questions for User

1. **Person names**: Should individual person names be preserved as tags, or consolidated into occupational/demographic categories?

2. **Primary source**: Is this a metadata tag that should be kept outside the taxonomy, or mapped/removed?

3. **Alcohol** vs **alcoholic beverages**: Was this consolidation intentional?

4. **Carrington**: What is this tag referring to?

5. **Families**: Should all family names be added, or only specific significant families?
