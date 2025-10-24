# Primary Facet Structure Audit Report

**Generated:** 2025-10-24
**Source:** data/tag_map_consolidated.csv

## Problem Summary

- **Current primary root trees:** 31 (including special markers)
- **Target primary root trees:** 7 (Getty AAT facets)
- **Orphaned roots requiring Getty parent:** 25

## Section A: Add 7 Getty AAT Root Entries

These entries create the top-level Getty AAT primary facets.

```csv
Agents,Agents,hierarchy,parent=(Getty AAT primary facet)
Places,Places,hierarchy,parent=(Getty AAT primary facet)
Built Environment,Built Environment,hierarchy,parent=(Getty AAT primary facet)
Activities,Activities,hierarchy,parent=(Getty AAT primary facet)
Events,Events,hierarchy,parent=(Getty AAT primary facet)
Associated Concepts,Associated Concepts,hierarchy,parent=(Getty AAT primary facet)
Materials,Materials,hierarchy,parent=(Getty AAT primary facet)
```

**USER ACTION:** [APPROVE]

---

## Section B: Connect Orphaned Roots to Getty Facets

Each orphaned root needs a parent connection to one of the 7 Getty facets.
Entries are grouped by Getty facet with confidence levels.

### Agents

#### Confidence: HIGH (3 tags)

**Tag:** `Environment & Weather`
**Suggested parent path:** `Agents > People > Demographic groups`
**Current children:** 2 (e.g., Natural resources, Weather & climate)
**USER ACTION:** [EDIT: Associated Concepts > Physical phenomena > Climate & weather [for weather related tags; replaced current 'weather'] OR Associated Concepts > Physical phenomena > Environment > Natural resources (for natural resources tag) ]

**Tag:** `Race & Ethnicity`
**Suggested parent path:** `Agents > People > Demographic groups`
**Current children:** 3 (e.g., Cultural identity & heritage, Marginalised groups, Racial stereotyping & performance)
**USER ACTION:** [EDIT: Race & Ethnicity should be a top-level thematic facet. We need to look at current children and place those tags under 'Agents > People > Demographic groups' ]

**Tag:** `Women & Gender`
**Suggested parent path:** `Agents > People > Demographic groups`
**Current children:** 2 (e.g., Gender-related vulnerabilities, Women as demographic group)
**USER ACTION:** [EDIT: as above, 'Women & Gender' needs to be a top-level thematic facet, and we need to look at current children and place those tags in a primary hierarchy, such as: Agents > People > Demographic groups > Women plus Agents > People > Demographic groups > Gender-related vulnerabilities ]

---

### Places

#### Confidence: HIGH (5 tags)

**Tag:** `Katoomba`
**Suggested parent path:** `Places > Towns`
**Current children:** 28 (e.g., Carrington, Katoomba Amateur Dramatic Club, Katoomba Amateur Minstrels)
**USER ACTION:** [EDIT: in the 'Places > Towns' primary facet, Katoomba should have NO children EXCEPT locales or places like 'South Katoomba' and 'Carrington'. All other children should appear elsewhere in primary facets (built  environment, agents > organisations, etc). PLUS there should be a thematic hierarchy of 'Towns > Katoomba > [all 28 children but classified by type, e.g., 'hotels', etc.'] ]

**Tag:** `Leura`
**Suggested parent path:** `Places > Towns`
**Current children:** 3 (e.g., Leura Falls, Leura Progress Association, Leura Reserve)
**USER ACTION:** [EDIT: Follows pattern described above for Katoomba: 'Places > Towns' primary facet with only place / locale children plus thematic facet. ]

**Tag:** `Megalong`
**Suggested parent path:** `Places > Towns`
**Current children:** 7 (e.g., Megalong Cricket Club, Megalong Hotel, Megalong Progress Committee)
**USER ACTION:** [EDIT: Follows pattern described above for Katoomba: 'Places > Towns' primary facet with only place / locale children plus thematic facet. ]

**Tag:** `Mount Victoria`
**Suggested parent path:** `Places > Towns`
**Current children:** 4 (e.g., Mount Victoria Hall, Mount Victoria Hotel, Mount Victoria Progress Committee)
**USER ACTION:** [EDIT: Follows pattern described above for Katoomba: 'Places > Towns' primary facet with only place / locale children plus thematic facet. ]

**Tag:** `Wentworth Falls`
**Suggested parent path:** `Places > Towns`
**Current children:** 3 (e.g., Wentworth Falls Hotel, Wentworth Falls Progress Association, Wentworth Falls Reserves)
**USER ACTION:** [EDIT: Follows pattern described above for Katoomba: 'Places > Towns' primary facet with only place / locale children plus thematic facet. ]

---

### Built Environment

#### Confidence: HIGH (1 tags)

**Tag:** `Transport & Infrastructure`
**Suggested parent path:** `Built Environment > Transport infrastructure`
**Current children:** 2 (e.g., Commercial transport, Mining transport)
**USER ACTION:** [REJECT: It is not clear to me whether these tags apply to 'built environment > Infrastructure' or under 'Activities > Transport', I need to see a source excerpt for each tagged item.]

---

### Activities

#### Confidence: HIGH (1 tags)

**Tag:** `Sport & Recreation`
**Suggested parent path:** `Activities > Sports`
**Current children:** 1 (e.g., Recreation themes)
**USER ACTION:** [REJECT: Too vague to be useful, will need to review source for each tag to assign a sport or activity]

#### Confidence: MEDIUM (2 tags)

**Tag:** `Economy & Labour`
**Suggested parent path:** `Activities > Economic activities`
**Current children:** 5 (e.g., Businesses, Economic distress, Industries)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Mining & Industry`
**Suggested parent path:** `Activities > Economic activities`
**Current children:** 4 (e.g., Mines & mining districts, Mining activities, Mining incidents)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

---

### Associated Concepts

#### Confidence: HIGH (3 tags)

**Tag:** `Alcohol & Temperance`
**Suggested parent path:** `Associated Concepts > Social behaviours`
**Current children:** 4 (e.g., Alcohol consumption & behaviour, Alcohol-related venues, Licensing & regulation)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Health & Medicine`
**Suggested parent path:** `Associated Concepts > Health concepts`
**Current children:** 2 (e.g., Health conditions, Health-related events)
**USER ACTION:** [APPRREJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Justice & Crime`
**Suggested parent path:** `Associated Concepts > Legal concepts`
**Current children:** 2 (e.g., Crimes, Legal outcomes)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

#### Confidence: LOW (10 tags)

**Tag:** `Arts & Culture`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 2 (e.g., Cultural activities, Cultural venues)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Communications & Postal Services`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 1 (e.g., Postal services)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Community institutions`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 5 (e.g., Civic buildings, Civic organisations, Cultural societies)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Family & Domestic Life`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 2 (e.g., Domestic accommodation, Family members by demographic)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Military & War`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 2 (e.g., Military events, Military organizations)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Parent Tag`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 1 (e.g., Child Tag)
**USER ACTION:** [DELETE - why is this needed?]

**Tag:** `Port Kembla`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 1 (e.g., Port Kembla disaster)
**USER ACTION:** [EDIT: Places > Towns (with Port Kembla disaster removed as child, it correctly appears under 'Events > Disasters & accidents') PLUS thematic facet under 'Towns', i.e., 'Towns > Port Kembla > Port Kembla disaster']

**Tag:** `Religion`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 4 (e.g., Church, Religious buildings, Religious organisations)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

**Tag:** `Sunny Corner`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 1 (e.g., Sunny Corner Mining Company)
**USER ACTION:** [REJECT: I need to see the source to catagorise this]

**Tag:** `Tourism & Accommodation`
**Suggested parent path:** `Associated Concepts > Associated Concepts`
**Current children:** 2 (e.g., Tourism activities, Tourist attractions)
**USER ACTION:** [REJECT: This is a thematic tag, we need to look at sub-tags and assign those to primary hierarchies]

---

## Section C: Review Statistics

- **Getty AAT roots to add:** 7
- **Orphaned roots to connect:** 25
- **Tags by confidence level:**
  - HIGH: 13
  - MEDIUM: 2
  - LOW: 10

## Instructions

1. Review Section A and mark [APPROVE / REJECT]
2. Review each entry in Section B:
   - Mark [APPROVE] if suggested parent is correct
   - Mark [REJECT] if tag should not be connected
   - Mark [EDIT: new_parent_path] to specify different parent
3. Save this file with your annotations
4. Run script 39 to apply approved changes

