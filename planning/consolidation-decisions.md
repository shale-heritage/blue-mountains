# Tag Consolidation Decisions

**Purpose:** Document all tag consolidation and rationalisation decisions with evidence and rationale for audit trail and reproducibility.

## Format

Each decision should include:

- **Date:** Decision date
- **Tags affected:** Original tags and consolidated preferred term
- **Rationale:** Evidence-based reasoning
- **Evidence:** Primary source excerpts, context analysis, usage patterns
- **Impact:** Number of items affected
- **Getty AAT alignment:** Reference to relevant AAT terms

---

## Military Activity Terms Consolidation

**Date:** 2025-10-31

**Tags affected:**

- `Military` (activity sense) → `Military activities`
- `Military activity` → `Military activities`
- **Preferred term:** `Military activities`

**Rationale:**

The military-related tags in the Activities facet showed redundancy:

1. `Military activities` (plural) - Parent facet term, never directly applied
2. `Military activity` (singular) - Never used in collection
3. `Military` - Applied to 2 items, but ambiguous (could mean activity or organisation)

Analysis of the 2 items tagged with `Military` revealed:

- Both items about Major Sir Charles George Gordon (WWI)
- Usage contexts: "military work" (career/service) and "Military Sports" (recreation event)
- The ambiguity of `Military` requires users to infer whether it refers to activities, organisations, events, or personnel
- More specific tags provide better retrieval precision

**Evidence:**

Primary source excerpts from items tagged `Military`:

**Item 1: "Death of Major Gordon" (5 May 1915)**

> "...he left to follow up his **military** work. About eight years ago he accepted a commission as Lieutenant in the old N.S.W. Mounted Rifles..."

> "...the powerful assistance he rendered at the last **Military** Sports here..."

**Analysis:**

- First usage: refers to military service/career (better tagged as "Military personnel" or "Soldiers")
- Second usage: refers to organised sporting event (better tagged as "Military sports" under Recreation activities)
- Neither usage requires the ambiguous `Military` tag

**Impact:**

- `Military`: 2 items (both retagged with more specific terms)
- `Military activity`: 0 items (never used)
- `Military activities`: 0 items directly applied (retained as facet parent)

**Getty AAT alignment:**

Getty AAT uses "military activities" (plural) as the standard form for the activities facet. Examples:

- <http://vocab.getty.edu/page/aat/300069290> military operations
- Activities facet uses plural forms for consistency

**Resolution:**

1. **Consolidated preferred term:** `Military activities` (plural)
2. **Action on `Military` tag:** Mark as merge to `Military activities` for activity contexts; retain polyhierarchical placement under `Military organizations` for organisational contexts
3. **Action on `Military activity` tag:** Mark as merge to `Military activities` (redundant singular form)
4. **New specific tags created:**
   - `Military sports` (under Recreation activities) for sporting events with military themes
   - `Major Sir Charles George Gordon` (under Soldiers) for the individual
   - `N.S.W. Mounted Rifles` (under Military organizations) for the regiment

**Related taxonomy updates:**

The military consolidation prompted creation of missing hierarchy elements:

1. **Added `Military organizations` under Organizations facet**
   - Enables proper polyhierarchical structure
   - Separates organisational entities from activity concepts

2. **Added `N.S.W. Mounted Rifles`**
   - Specific military organisation from WWI
   - Parent: Military organizations
   - Evidence: "N.S.W. Mounted Rifles" appears in full text as formal organisation name

3. **Added `Military sports`**
   - Recreation activity with military theme/participation
   - Parent: Recreation activities (with polyhierarchical link to Sport & Recreation thematic)
   - Evidence: "Military Sports" in primary sources refers to organised athletic events

4. **Added `Major Sir Charles George Gordon`**
   - Named individual, military officer
   - Parents: Soldiers, Military personnel, People - THEMATIC
   - Evidence: Full name and title from primary sources
   - WWI casualty, officer in N.S.W. Mounted Rifles

**Tag application queue:**

Items added to `tag_application_mapping.csv` for retagging:

1. "Death of Major Gordon" (5 May 1915)
   - Remove: `Military`
   - Add: `Major Sir Charles George Gordon`, `Soldiers`, `N.S.W. Mounted Rifles`, `Military activities`, `Military sports`, `World War I`

2. "The Late Major Gordon" (6 October 1915)
   - Remove: `Military`
   - Add: `Major Sir Charles George Gordon`, `Soldiers`, `World War I`

---

## Horses Tag Reclassification

**Date:** 2025-10-31

**Tags affected:**

- `Horses` (under Recreation activities) → Removed (conceptually incorrect)
- `Horses` → Retained under Agents > Animals > Horses (correct placement)
- Items requiring additional tags:
  - `Horseback riding` (for recreational riding)
  - `Horseborne transportation` (for commercial/practical transport)

**Rationale:**

The "Horses" tag was incorrectly placed under Recreation activities facet. This represents a fundamental categorical error:

- **Horses are animals (agents), not activities**
- The **activity** is "Horseback riding" or "Horseborne transportation"
- Getty AAT structure clearly separates agents (animals) from activities (actions involving those animals)

**Evidence:**

Full text analysis of all 19 items tagged with "Horses" revealed:

1. **All 19 items (100%)** refer to horses as animals/agents
   - Transport animals (buggy horses, sulky horses, riding horses)
   - Commercial property (breeding ponies for market, wild horses shot for skins)
   - Straying animals (property disputes)

2. **15 items (79%)** describe commercial or practical horse transport
   - Postal delivery (mailman's horse, postman's horse)
   - Official business (constable's horse, riding home from posting registry)
   - Commercial carting (carter's horse and cart)
   - Tourism routes (Jenolan Caves access, Nellie's Glen track)
   - Urban traffic (horseman riding through town streets)

3. **1 item (5%)** describes recreational horseback riding
   - Horse racing at Medlow (sport/entertainment)

4. **3 items (16%)** mention horses only as animals
   - Straying animals court cases
   - Horses grazing on streets
   - Wild horses and pony breeding

**Impact:**

- `Horses` tag under Recreation activities: Remove from taxonomy (conceptual error)
- `Horses` tag under Agents > Animals: Retain for all 19 items
- Add `Horseborne transportation` to 15 items (commercial/practical transport)
- Add `Horseback riding` to 1 item (recreational horse racing)

**Getty AAT alignment:**

Getty AAT structure demonstrates proper separation:

- **Agents Facet:**
  - Animals > Horses (the biological agents)

- **Activities Facet:**
  - Recreation activities > Horseback riding (the recreational activity)
  - Economic activities > Transport > Horseborne transportation (the transport activity)

This polyhierarchical approach correctly separates:
- **What:** Horses (the animal agents involved)
- **How:** Horseborne transportation (the transport method used)
- **Why:** Horseback riding (the recreational purpose)

**Resolution:**

1. **Taxonomy changes:**
   - Line 277 in tag_map_consolidated.csv: Changed from `hierarchy,parent=Recreation activities` to `merge,Remove from Recreation activities - horses are animals (agents) not activities; use 'Horseback riding' for the activity`

2. **Tag applications queued:**
   - All 19 items added to tag_application_mapping.csv (lines 103-121)
   - Categorised by context:
     - 15 items: Add `Horseborne transportation` (commercial/practical transport)
     - 1 item: Add `Horseback riding` (recreational sport - horse racing)
     - 3 items: No additional tags (just animals as property)

3. **Review documentation:**
   - Created detailed review sheet: `reports/horses_tag_reclassification_review.md`
   - Includes primary source excerpts for each item
   - Provides approve/reject/change options for user review

**Key principle:**

This consolidation reinforces a critical taxonomic principle: **entities (agents) must be clearly separated from activities (processes)**. Confusing the two creates retrieval problems and violates Getty AAT structural logic.

---

## Horses Tag Getty AAT Alignment and Expansion

**Date:** 2025-10-31

**Tags added/modified:**

**NEW TAXONOMY STRUCTURE (Getty AAT-aligned):**

### Activities Facet

1. **Agriculture > Animal husbandry > Animal breeding**
   - Horse breeding
   - Pony breeding

2. **Hunting**
   - Wild horse culling (commercial skin harvesting)

3. **Societal activities > Law enforcement**
   - Policing

### Agents Facet

1. **Animals > Wild animals**
   - Wild horses (feral horses)

2. **People > Occupations > Agriculture workers**
   - Animal breeders > Horse breeder

3. **People > Occupations > Law enforcement personnel**
   - Police officers > Constable

4. **People - THEMATIC**
   - Mr Hardie Clydesdale (polyhierarchical: Horse breeder + Named individual)

### Events Facet

1. **Accidents**
   - Transport accidents
     - Animal-powered transport accidents
       - Horse accidents
         - Horse-drawn vehicle accidents
         - Horseback riding accidents
         - Runaway horse incidents
   - Agricultural accidents
     - Livestock accidents
       - Animal attacks
         - Goring

2. **Legal proceedings > Court cases**
   - Property offences
     - Stock trespass (Australian legal term)
       - Alternate terms: Animal trespass, Cattle straying, Horse straying

3. **Cultural events > Sporting events**
   - Equestrian events
     - Horse races

### Recreation Activities (polyhierarchical link)

- Sports > Equestrian sports
  - Horse racing (the activity/sport)
  - Horseback riding (recreational)

**Rationale:**

Following user review of primary source contexts, comprehensive Getty AAT-aligned taxonomy was required to accurately represent the diverse horse-related content in the collection:

1. **Conceptual Clarity:** Original "Horses" under Recreation activities confused agent (animal) with activity (riding/racing)

2. **Getty AAT Verification:**
   - Animal husbandry (AAT ID: 300254388) sits under Agriculture (discipline)
   - Getty AAT uses specific facets: Activities, Events, Agents, Associated Concepts
   - Events facet encompasses accidents, legal proceedings, and cultural events

3. **Australian Context:**
   - "Stock trespass" is the Australian legal term for animal straying
   - Wild horse culling reflects historical economic activity (shooting for skins)
   - Constable reflects UK/Commonwealth police rank structure (1890s Australia)

**Evidence:**

Full-text analysis of 19 items revealed:
- 100% refer to horses as animals/agents
- 79% involve commercial/practical horse transport
- Multiple distinct accident types requiring specific categorisation
- Mix of agricultural, legal, recreational, and commercial contexts

**Getty AAT Alignment:**

All new taxonomy entries follow Getty AAT structural principles:

1. **Facet-appropriate placement:**
   - **Activities:** Processes and functions (breeding, hunting, policing)
   - **Events:** Occurrences and incidents (accidents, races, court cases)
   - **Agents:** Entities (animals, people, occupations)

2. **Hierarchical specificity:**
   - Broader terms: Agriculture > Animal husbandry > Animal breeding
   - Narrower terms: Horse breeding, Pony breeding
   - Parallel structure: Horse-drawn vehicle accidents vs Horseback riding accidents

3. **Polyhierarchical relationships:**
   - Mr Hardie Clydesdale: Horse breeder (occupation) + Named individual (person)
   - Horse racing: Sporting events (event) + Equestrian sports (activity)

**Resolution:**

1. **Taxonomy changes:** 40 new entries added to tag_map_consolidated.csv
   - 11 activities terms
   - 16 events terms
   - 10 agents terms
   - 3 alternate/merge terms

2. **Tag applications:** All 19 items updated in tag_application_mapping.csv with Getty AAT-aligned tags

3. **Item-specific categorisation:**
   - Item #2: Animal husbandry context (breeding business + wild horse culling)
   - Items #5, 11, 12: Runaway horse incidents (horses bolting)
   - Items #5, 12, 15, 16: Horse-drawn vehicle accidents (carts, buggies, sulkies)
   - Items #14, 17, 18: Horseback riding accidents (riders falling/thrown)
   - Item #7: Stock trespass (legal proceeding)
   - Item #9: Horse races (sporting event, not recreational activity)
   - Item #10: Goring (livestock attack accident)
   - Items #3, 19: Postal services (commercial communication activity)
   - Item #13: Policing (law enforcement activity)
   - Items #8, 11: Recreational horseback riding

**Key Principles Reinforced:**

1. **Entities vs Activities:** Horses are agents (animals), not activities; riding/racing are activities
2. **Event specificity:** Accidents require detailed categorisation by type and context
3. **Occupational precision:** Named individuals should be polyhierarchical (role + person)
4. **Legal terminology:** Use formal legal terms (Stock trespass) over colloquial (straying)
5. **Getty AAT authority:** Verify controlled vocabulary terms against authoritative thesaurus

**Impact:**

- Horses tag: Retained under Agents > Animals (all 19 items)
- Horses tag: Removed from Recreation activities (conceptual error corrected)
- 40 new taxonomy terms: Enable accurate, granular tagging
- 19 items retagged: Getty AAT-aligned, context-appropriate tags applied

This consolidation demonstrates the importance of:
- Primary source analysis for accurate categorisation
- Getty AAT structural principles for taxonomy design
- Distinguishing between agent types, activity types, and event types
- Polyhierarchical relationships for complex entities

---

## Horses Taxonomy Refinements

**Date:** 2025-10-31 (Updated)

**Changes made:**

### 1. Pony Breeding Consolidated to Horse Breeding

**Original structure:**
```
Activities > Economic activities > Agriculture > Animal husbandry > Animal breeding
├── Horse breeding
└── Pony breeding
```

**Updated structure:**
```
Activities > Economic activities > Agriculture > Animal husbandry > Animal breeding
└── Horse breeding (with "Pony breeding" as alternate term)
```

**Rationale:**
- Ponies are simply small horses (horses under 14.2 hands/147cm)
- No semantic difference in the breeding activity
- Consolidation reduces redundancy while preserving terminology through alternate term
- Item #2 now tagged with "Horse breeding" (covers both horses and ponies)

**Action:**
- Line 1078 in tag_map_consolidated.csv: Changed from `hierarchy,parent=Animal breeding` to `merge,Alternate term for Horse breeding (ponies are small horses)`
- Item #2 in tag_application_mapping.csv: Removed "Pony breeding" tag (now covered by "Horse breeding")

### 2. Spectator Sports Added

**Context:**
Horse racing is a spectator sport (watching event), not participatory recreation. Other sports in collection (cricket, football, athletics) are also spectator events.

**New structure:**
```
Activities (primary facet)
└── Recreation activities
    ├── Spectator sports (NEW)
    └── Sports
        └── Equestrian sports
            └── Horse racing

Events (primary facet - existing)
└── Cultural events
    └── Sporting events
        └── Equestrian events
            └── Horse races
```

**Rationale:**
- Distinguishes between:
  - **Event:** Horse races (the occurrence/competition)
  - **Activity:** Spectator sports (the recreation of watching/attending)
- Aligns with other sporting events in collection (cricket matches, football games)
- Provides consistent tagging for sports that primarily involve spectators rather than participants

**Getty AAT Alignment:**
- Activities Facet: Recreation activities > Spectator sports (the act of watching)
- Events Facet: Sporting events > Equestrian events > Horse races (the competitive event)

**Action:**
- Lines 767-768 in tag_map_consolidated.csv: Added "Spectator sports" with polyhierarchical links to Recreation activities and Sport & Recreation thematic
- Item #9 in tag_application_mapping.csv: Added "Spectator sports" tag to horse race item

**Impact:**
- Enables accurate tagging of spectator-oriented sporting events
- Separates participatory recreation (playing sport) from spectator recreation (watching sport)
- Provides framework for future tagging of other spectator sports (cricket matches, football games, athletics meets)

---

## Sports Hierarchy Simplification

**Date:** 2025-10-31 (Updated)

**Tags affected:**

- `Sports` (under Recreation activities) → Removed from primary facet
- `Equestrian sports` → Removed from primary facet
- `Horse racing` (activity sense) → Removed from primary facet
- **Preferred approach:** Use `Spectator sports` for watching sporting events; use `Horse races` (Events facet) for the sporting event itself

**Rationale:**

The nested hierarchy `Recreation activities > Sports > Equestrian sports > Horse racing` created unnecessary complexity and conceptual confusion:

1. **Redundancy:** "Sports" as a generic container under Recreation activities duplicated the more specific "Spectator sports" and "Sporting events" categories
2. **Conceptual clarity:** The distinction between:
   - **Activity:** Spectator sports (the act of watching/attending sporting events)
   - **Event:** Horse races (the competitive event itself)
   - **Participatory activity:** Would be specific activities like "Playing cricket" or "Playing football" (not present in collection)
3. **Collection reality:** The Blue Mountains collection contains references to attending/watching sporting events, not participating in them
4. **Getty AAT alignment:** Activities facet should describe what people do (watching/spectating), not generic categories (sports)

**Evidence:**

Review of sporting content in collection shows:
- Horse racing references are about attending races as spectators (social/recreation activity)
- Cricket, football, athletics mentions are about matches/competitions (events) or club organizations (agents)
- No items describe participatory recreational sport activities (people playing sport for recreation)

**Getty AAT Alignment:**

Getty AAT structure maintains clear separation:
- **Activities Facet:** Specific actions (spectating, playing, coaching)
- **Events Facet:** Occurrences (matches, races, competitions)
- **Agents Facet:** Organizations (sports clubs, teams)

**Resolution:**

1. **Taxonomy changes:**
   - Line 765 in tag_map_consolidated.csv: Changed Sports from `hierarchy,parent=Recreation activities` to `merge,Remove from Recreation activities - use specific activity types (Spectator sports for watching events) or event types (Sporting events for the events themselves)`
   - Line 1103: Changed Equestrian sports to `merge,Remove from Recreation activities hierarchy - use Spectator sports for watching horse racing; use Horse races (Events facet) for the sporting event itself`
   - Line 1104: Changed Horse racing (activity) to `merge,Remove from Recreation activities - use Spectator sports for watching horse racing; use Horse races (Events facet) for the sporting event itself`

2. **Retained thematic links:**
   - Sports remains under Recreation themes (thematic grouping) for domain-based browsing
   - Horse racing remains under Sport & Recreation thematic for exhibition purposes

3. **Tag applications:**
   - No items currently tagged with "Sports", "Equestrian sports", or "Horse racing" in the activity sense
   - All horse racing references already tagged with "Spectator sports" (Item #9)

**Impact:**

- Simplified Recreation activities facet structure
- Eliminated redundant generic "Sports" container
- Reinforced clear conceptual distinction between activities (spectating) and events (races/matches)
- Maintained thematic groupings for domain-based browsing
- Zero items requiring retagging (no active usage of removed tags)

**Key Principle:**

This consolidation reinforces: **Use specific activity terms (Spectator sports) rather than generic category containers (Sports) in primary facets**. Generic categories may remain useful in thematic groupings for exhibition/browsing purposes, but the formal Getty AAT-aligned taxonomy should use precise, actionable terms.

---

## Licensing Taxonomy Rationalisation

**Date:** 2025-10-31

**Tags affected:**

- `Licensing Court` → Removed from Activities > Regulatory processes > Licensing
- `Licensing inspector` → Removed from Activities > Regulatory processes > Licensing
- `Licensing Act` → Moved from Activities > Regulatory processes > Licensing to Associated Concepts > Legal concepts > Laws
- **New tags created:**
  - `Laws` (parent category under Legal concepts)
  - `Licensing cases` (under Events > Legal proceedings)
  - `Liquor licensing applications` (under Licensing cases)
  - `Licensing offences` (under Licensing cases)

**Rationale:**

The licensing-related tags were incorrectly mixed under Activities > Regulatory processes > Licensing, confusing different conceptual categories:

1. **Licensing Court is an organisation (judicial institution), not an activity**
   - Evidence: "At the Katoomba Licensing Court, on Wednesday last..."
   - Evidence: "QUATERY MEETING of the Licensing Court... will be holden AT THE POLICE OFFICE, KATOOMBA"
   - The court **meets at different locations**, proving it's an institutional body, not a building or activity
   - **Correct placement:** Agents > Organizations > Government bodies > Courts

2. **Licensing inspector is an occupation, not an activity**
   - Evidence: "Mr. Gannon" appears as the licensing inspector - clearly a person with occupational role
   - **Correct placement:** Agents > People > Occupations > Public officials

3. **Licensing Act is legislation (a legal document), not an activity or process**
   - Evidence: "infringing Section 63 of the Licensing Act"
   - Evidence: "never was summoned under the Licensing Act before"
   - **Correct placement:** Associated Concepts > Legal concepts > Laws

4. **Items tagged with "Licensing Act" describe different event types**
   - Some are routine licence applications (administrative proceedings)
   - Others are prosecutions for violations (criminal/civil proceedings)
   - Both are **events**, not activities

**Evidence:**

Primary source excerpts from hotel licensing review (reports/hotel_licensing_review.md):

**Licensing Court (institutional body):**
> "Nepean Times (Penrith, NSW : 1882 - 1962), Saturday 26 March 1892, page 4
>
> GRANTED. - At the Katoomba **Licensing Court**, on Wednesday last, Rubina Fryer applied to have the License of the house known as "Fryer's Family Hotel" transferred..."

> "QUATERLY MEETING, **Licensing Court**, Katoomba. NOTICE is hereby given that the QUATERY MEETING of the **Licensing Court** for the Licensing distinct of Penrith will be holden AT THE POLICE OFFICE, KATOOMBA, at 11 o'clock..."

**Licensing Act (legislation):**
> "Richard Allen, **licensee of** the Centennial Hotel, Katoomba South, was charged with infringing Section 63 of the Licensing Act."

> "never was summoned under the **Licensing Act** before..."

**Licensing inspector (occupation):**
Context shows Mr. Gannon as the licensing inspector reviewing applications.

**Getty AAT Alignment:**

Getty AAT structure maintains clear separation:

- **Activities Facet:** Licensing (the regulatory process of issuing licences)
- **Agents Facet:**
  - Courts (judicial institutions, including Licensing Court)
  - Public officials (occupations, including Licensing inspector)
- **Events Facet:**
  - Legal proceedings > Licensing cases (specific legal events)
    - Liquor licensing applications (routine administrative proceedings)
    - Licensing offences (prosecutions for violations)
- **Associated Concepts Facet:**
  - Legal concepts > Laws (legislation, including Licensing Act)

**Resolution:**

1. **Taxonomy changes:**
   - Line 378 in tag_map_consolidated.csv: Removed `Licensing Court,Licensing Court,hierarchy,parent=Licensing`
   - Line 380 in tag_map_consolidated.csv: Removed `Licensing inspector,Licensing inspector,hierarchy,parent=Licensing`
   - Line 375: Changed `Licensing Act,Licensing Act,hierarchy,parent=Licensing` to `Licensing Act,Licensing Act,hierarchy,parent=Laws`
   - Line 951: Added Laws hierarchy:
     ```csv
     Laws,Laws,hierarchy,parent=Legal concepts
     ```
   - Lines 147-150: Added Licensing cases hierarchy:
     ```csv
     Licensing cases,Licensing cases,hierarchy,parent=Legal proceedings
     Licensing cases,Licensing cases,hierarchy,parent=Licensing & regulation - THEMATIC
     Liquor licensing applications,Liquor licensing applications,hierarchy,parent=Licensing cases
     Licensing offences,Licensing offences,hierarchy,parent=Licensing cases
     ```

2. **Retained correct placements:**
   - Licensing Court under Agents > Organizations > Courts (line 377)
   - Licensing inspector under Agents > People > Occupations > Public officials (line 380)
   - All retain thematic grouping links for domain-based browsing

3. **Updated hierarchy trees:**
   - Activities > Regulatory processes > Licensing now only contains activity-related terms (Hotel licensing, Liquor licensing, Publican's licensing)
   - Associated Concepts > Legal concepts > Laws > Licensing Act (new structure)
   - Events > Legal proceedings > Licensing cases (new structure)
   - Agents facets unchanged (already correct)

**Impact:**

- Simplified Activities > Regulatory processes > Licensing (removed non-activity terms)
- Created proper Legal concepts > Laws structure for legislation
- Created proper Events > Legal proceedings > Licensing cases structure for legal events
- Reinforced clear conceptual boundaries:
  - **What:** Licensing Act (the law)
  - **Who:** Licensing Court (judicial body), Licensing inspector (occupation)
  - **How:** Licensing (regulatory process/activity)
  - **When:** Licensing cases (legal events - applications or prosecutions)

**Key Principles:**

This consolidation reinforces critical taxonomic principles:

1. **Facet-appropriate placement:** Entities belong in Agents, activities in Activities, events in Events, abstract concepts in Associated Concepts
2. **Institutional vs spatial:** Courts are institutional bodies (organizations), not buildings (unless specifically referring to courthouse building)
3. **Legislation as concept:** Laws and acts are abstract concepts (legal frameworks), not activities or processes
4. **Event typing:** Legal proceedings should distinguish between administrative (applications) and adjudicative (prosecutions) events

**Tag Applications:**

No immediate tag applications required. The 4 items currently tagged with "Licensing Act" should be reviewed individually to add appropriate event tags:
- Routine applications → Add "Liquor licensing applications"
- Violation prosecutions → Add "Licensing offences"

---

## Drinking Tag Consolidation

**Date:** 2025-10-31

**Tags affected:**

- `Drinking` → Merged to `Drinking (alcohol)`
- **Preferred term:** `Drinking (alcohol)`

**Rationale:**

The collection contained two separate but semantically identical tags:
- `Drinking` (2 items)
- `Drinking (alcohol)` (0 items)

Analysis revealed both tagged items refer specifically to alcohol consumption:

1. **Drinking without qualification is ambiguous** in a general taxonomy (water? tea? alcohol?)
2. **Historical newspaper context** makes alcohol consumption the default meaning
3. **Existing rationalisation work** already established `Drinking (alcohol)` as the preferred term
4. **Both tagged items involve alcohol** consumption

**Evidence:**

Primary source analysis of 2 items tagged with "Drinking":

**Item 1: "Katoomba Municipal Elections." (5 July 1890)**
- Also tagged with "Drunkeness" and "Hotels"
- Full text excerpt: "a man, maddened by drink, rushed through the streets, kicking, tripping, and biting all in his way"
- Context: Article notes individual should "seek to avoid stimulants in the future"
- **Conclusion:** Clearly refers to alcohol consumption

**Item 2: "[untitled]" (29 June 1889)**
- Tagged with "Concerts", "Recreation for miners", "Reference to the Irish or Irish culture"
- No contradictory evidence (no mentions of water, tea, or non-alcoholic beverages)
- Collection context (Blue Mountains temperance-era newspapers, 1880s-1900s)
- **Conclusion:** Most likely refers to alcohol consumption

**Collection Context:**

Blue Mountains historical newspaper collection (1880s-1910s):
- Temperance movement highly active in this period
- Alcohol consumption was newsworthy; non-alcoholic beverage consumption was not
- When newspapers mention "drinking" as a social behaviour, they invariably mean alcohol
- Tea drinking, water drinking, etc. are not tagged as social behaviours in the collection

**Getty AAT Alignment:**

Getty AAT uses qualified terms for disambiguation:
- Generic "drinking" could mean any beverage consumption
- "Drinking (alcohol)" specifically identifies the activity
- Follows established pattern: "Drunkenness (intoxication)" vs "Drunkenness (crime)"

**Previous Rationalisation Work:**

The alcohol_rationalisation_report.md (existing project documentation) consistently uses "Drinking (alcohol)" as the preferred term for alcohol consumption activity:
- 10+ items analysed all use "Drinking (alcohol)" tag
- Report establishes clear hierarchy: Activities > Social behaviours > Drinking (alcohol)

**Resolution:**

1. **Taxonomy changes:**
   - Line 197 in tag_map_consolidated.csv: Changed from contradictory entries to:
     ```csv
     Drinking,Drinking,merge,Consolidate to Drinking (alcohol) - all instances in collection refer to alcohol consumption (Blue Mountains temperance-era newspapers)
     ```
   - Removed redundant/contradictory hierarchy entries for "Drinking"
   - Retained "Drinking (alcohol)" hierarchy:
     ```csv
     Drinking (alcohol),Drinking (alcohol),hierarchy,parent=Alcohol consumption & behaviour - THEMATIC
     Drinking (alcohol),Drinking (alcohol),hierarchy,parent=Social behaviours
     ```

2. **Tag applications:**
   - Lines 122-123 in tag_application_mapping.csv: Added 2 items for retagging:
     ```csv
     [untitled],29 June 1889,Katoomba Times,Drinking,Drinking (alcohol),drinking_consolidation,Consolidate Drinking to Drinking (alcohol)
     Katoomba Municipal Elections.,5 July 1890,Katoomba Times,Drinking,Drinking (alcohol),drinking_consolidation,Consolidate Drinking to Drinking (alcohol) - item mentions drunkenness
     ```

3. **Updated hierarchy trees:**
   - Activities > Social behaviours now shows only "Drinking (alcohol)" (line 44 in primary_activities.txt)
   - Removed ambiguous "Drinking" term

**Impact:**

- Simplified Social behaviours structure (removed redundant tag)
- Improved semantic clarity through disambiguation
- Aligned with existing alcohol rationalisation work
- Maintained consistency with other disambiguated terms in taxonomy

**Key Principle:**

This consolidation reinforces: **Use parenthetical qualifiers to disambiguate generic terms**. In historical collections with strong thematic focus (temperance-era newspapers), contextual defaults may apply, but explicit disambiguation improves cross-collection compatibility and semantic precision.

---

## Societal Activities Facet Restructure

**Date:** 2025-10-31

**Changes made:**

1. **Moved existing facets under Societal activities:**
   - `Regulatory processes` → Activities > Societal activities > Regulatory processes
   - `Military activities` → Activities > Societal activities > Military activities

2. **Removed individuals from Activities facet:**
   - Moved 7 named police officers from Activities > Law enforcement to Agents > People > Occupations
   - Created proper rank structure: Constable, Senior-Constable, Sergeant

3. **Fixed Police organisation placement:**
   - Moved `Police` from Activities > Law enforcement to Agents > Organizations > Government bodies
   - Removed Police court and Police station from incorrect "Police" parent

**Rationale:**

### Issue 1: Flat facet structure

The Activities facet had three sibling facets at the same level:
- Regulatory processes
- Military activities
- Societal activities > Law enforcement

This created inconsistent hierarchy depth and failed to reflect that regulatory and military functions are types of societal activities.

**Getty AAT structure** uses "societal activities" as a broader container for organized collective activities including:
- Military operations
- Law enforcement
- Government/regulatory functions
- Civic administration

### Issue 2: Named individuals in Activities facet

The taxonomy had fundamental categorical errors:

```
Activities > Societal activities > Law enforcement
├── Constable John Hamilton (PERSON, not activity)
├── Constable O'Reilly (PERSON, not activity)
├── Policing (ACTIVITY - correct)
```

**Problem:** People are agents, not activities. Mixing them violates Getty AAT facet principles.

**Evidence:** Primary facet definitions:
- **Activities Facet:** Actions, processes, functions (what people DO)
- **Agents Facet:** Entities (WHO does things) - people, organizations, groups

### Issue 3: Police organisation misplaced

"Police" was under Activities > Law enforcement, but Police is an **institution/organization** (agent), not an activity. The activity is "Policing".

Similarly, Police court and Police station were incorrectly parented under "Police" in the Activities facet, when they should only appear under their correct primary facets:
- **Police court:** Agents > Organizations > Courts (judicial institution)
- **Police station:** Built Environment > Civic buildings > Police facilities (building)

**Getty AAT Alignment:**

Correct facet structure:

**Activities Facet:**
```
Activities
└── Societal activities
    ├── Law enforcement
    │   └── Policing (the activity)
    ├── Military activities
    └── Regulatory processes
        └── Licensing
```

**Agents Facet:**
```
Agents
├── Organizations
│   └── Government bodies
│       └── Police (the institution)
└── People
    └── Occupations
        └── Law enforcement personnel
            └── Police officers
                ├── Constable (rank)
                │   ├── Constable John Hamilton
                │   ├── Constable O'Reilly
                │   ├── Constable Orr
                │   └── Constable White
                ├── Senior-Constable (rank)
                │   ├── Senior-Constable Illingworth
                │   └── Senior-Constable Thorncroft
                └── Sergeant (rank)
                    └── Sergeant Thorndyke
```

**Resolution:**

1. **Taxonomy changes (Activities facet):**
   - Line 422: Changed `Military activities,Military activities,hierarchy,parent=Activities` to `parent=Societal activities`
   - Line 688: Changed `Regulatory processes,Regulatory processes,hierarchy,parent=Activities` to `parent=Societal activities`
   - Lines 120-127: Changed all named constables from `parent=Law enforcement` and `parent=Police` to `parent=Constable` and `parent=People - THEMATIC`
   - Lines 730-735: Changed Senior-Constables and Sergeant from `parent=Law enforcement` and `parent=Police` to appropriate rank parents
   - Line 620: Changed `Police,Police,hierarchy,parent=Law enforcement` to `parent=Government bodies`

2. **Taxonomy additions (Agents facet):**
   - Lines 1116-1117: Added police rank structure:
     ```csv
     Senior-Constable,Senior-Constable,hierarchy,parent=Police officers
     Sergeant,Sergeant,hierarchy,parent=Police officers
     ```

3. **Removed incorrect hierarchies:**
   - Removed Police court from "Police" parent (line 622) - retained only under Courts
   - Removed Police station from "Police" parent (line 625) - retained only under Police facilities

4. **Updated hierarchy trees:**
   - Activities > Societal activities now contains: Law enforcement > Policing, Military activities, Regulatory processes
   - No named individuals remain in Activities facet
   - All police officers correctly placed in Agents > People > Occupations > Law enforcement personnel

**Impact:**

- **Improved structural consistency:** Societal activities now properly groups related governmental/civic functions
- **Fixed categorical errors:** Removed people from Activities facet
- **Proper agent/activity separation:** Police (organization) vs Policing (activity)
- **Better hierarchy depth:** Three-level structure (Activities > Societal activities > Law enforcement > Policing) provides appropriate granularity
- **Getty AAT compliance:** Facet-appropriate placement for all entities

**Key Principles:**

This restructure reinforces fundamental taxonomic principles:

1. **Facet integrity:** Activities contain only activities; Agents contain only agents
2. **Hierarchical grouping:** Related activities should be grouped under appropriate intermediate categories
3. **Entity distinction:** Organizations (Police) ≠ Activities (Policing) ≠ People (Police officers)
4. **Rank structure:** Occupational hierarchies should reflect organizational ranks (Constable < Senior-Constable < Sergeant)

---

## Domestic Animals Classification

**Date:** 2025-10-31

**Tags affected:**

- Created `Domestic animals` as new intermediate category under `Animals`
- Moved `Cattle` from direct child of `Animals` to child of `Domestic animals`
- Moved `Dogs` from direct child of `Animals` to child of `Domestic animals`
- Moved `Horses` from direct child of `Animals` to child of `Domestic animals`
- Retained `Animal` (singular generic) as direct child of `Animals`
- Retained `Wild animals` structure unchanged

**Rationale:**

The Animals hierarchy lacked parallel structure with asymmetric organization:

**Before:**
```
Animals
├── Animal (generic)
├── Cattle
├── Dogs
├── Horses
└── Wild animals
    └── Wild horses
```

Creating a `Domestic animals` category provides:

1. **Symmetry:** Domestic/Wild distinction creates clear organizing principle
2. **Getty AAT alignment:** AAT distinguishes between domestic and wild animals as fundamental characteristic
3. **Semantic clarity:** Makes the domestication status explicit for browsing users
4. **Logical grouping:** Cattle, dogs, and horses in 19th century Australian context are clearly domestic animals

**After:**
```
Animals
├── Animal (generic - for when domestic/wild not specified)
├── Domestic animals
│   ├── Cattle
│   ├── Dogs
│   └── Horses
└── Wild animals
    └── Wild horses
```

**Evidence:**

Historical context supports this classification:

- **Cattle:** Domestic livestock raised for agricultural purposes
- **Dogs:** Domestic companion/working animals
- **Horses:** Domestic animals used for transportation, work, and recreation
- **Wild horses:** Feral horses in Blue Mountains region (distinct from domestic horses)

The collection context shows these animals in clearly domestic roles:
- Cattle: Stock trespass cases (owned, managed animals)
- Dogs: Companion animals in domestic settings
- Horses: Transport, recreation, horse breeding businesses
- Wild horses: Pest management, culling operations

**Getty AAT alignment:**

Getty AAT makes the domestic/wild distinction fundamental to animal classification:

- **Domestic animals (AAT: 300265135):** "Animals adapted through breeding in captivity to a life intimately associated with and advantageous to humans"
- **Wild animals:** Animals not domesticated or under direct human control

**Impact:**

- **No retagging required:** This is purely hierarchical reorganization
- **Improved browsing:** Users can now filter by domestication status
- **Parallel structure:** Domestic animals / Wild animals creates symmetrical organization
- **Future-proofing:** Clear placement for additional domestic animal types (chickens, pigs, etc.)
- **Maintains generic term:** "Animal" remains available for contexts where domestic/wild is not specified

**Key Principles:**

This reorganization demonstrates:

1. **Parallel structure:** Creating symmetric hierarchies improves navigability
2. **Semantic transparency:** Making implicit distinctions (domestic/wild) explicit in hierarchy
3. **Getty AAT alignment:** Following authoritative vocabulary structure principles
4. **Flexibility:** Generic term "Animal" preserved for ambiguous cases

---

## Retailer and Store Tag Consolidation

**Date:** 2025-10-31

**Tags affected:**

Parent category consolidation:

- `Retailers & stores` → `Retailers and Stores` (standardised plural parent)
- `Retailers and stores` → `Retailers and Stores` (merged duplicate)
- **Preferred term:** `Retailers and Stores` (plural parent, never directly applied)

Generic leaf node (for unspecified retailer items):

- `Store` → `Retailer or Store` (singular generic leaf)
- `Stores` → `Retailer or Store` (singular generic leaf)
- `Retailers & store` → `Retailer or Store` (singular generic leaf)
- `Retailers and store` → `Retailer or Store` (singular generic leaf)
- **Preferred term:** `Retailer or Store` (singular, applied to generic items)

Business name standardisation:

- `Douglas & Co.` → `Douglas and Company` (with abbreviated form as synonym)
- `Peckman Bros` → `Peckman Brothers` (with abbreviated form as synonym)
- `Tabrett and Co.` → `Tabrett and Company` (with abbreviated form as synonym)
- `Nimmo's` → retained as is (already in full form)

**Rationale:**

Duplication issue identified in hierarchy visualisation where two parallel branches existed:

1. `Retailers & stores` (with ampersand)
2. `Retailers and stores` (with "and")

Both branches contained nearly identical children with minor naming variants, creating confusion and data quality issues. The consolidation addresses several problems:

1. **Eliminate redundancy:** Two identical parent categories with slightly different punctuation
2. **Standardise pattern:** Plural parent ("Retailers and Stores") + singular generic leaf ("Retailer or Store") matches established taxonomy pattern (e.g., Hotels > Hotel, Schools > School)
3. **Spell out abbreviations:** Full business names improve clarity and searchability
4. **Preserve alternates:** Abbreviated forms retained as synonyms for historical references

**Evidence:**

Hierarchy tree analysis showed duplicate branches:

```
│   │   ├── Retailers & stores
│   │   │   ├── Douglas & Co.
│   │   │   ├── Nimmo's
│   │   │   ├── Peckman Bros
│   │   │   ├── Retailers & store
│   │   │   ├── Stores
│   │   │   └── Tabrett and Co.
│   │   ├── Retailers and stores
│   │   │   ├── Douglas and Company
│   │   │   ├── Nimmo's
│   │   │   ├── Peckman Bros
│   │   │   ├── Retailers and store
│   │   │   ├── Store
│   │   │   └── Tabrett and Company
```

**Changes implemented:**

1. **Parent consolidation:**
   - Merged duplicate "Retailers & stores" and "Retailers and stores" entries
   - New preferred term: "Retailers and Stores" (plural parent, never directly applied)
   - Maintains parent: Commercial businesses
   - Follows standard pattern: plural parent for category

2. **Generic leaf node:**
   - Created: "Retailer or Store" (singular, for generic/unspecified retailer items)
   - Parent: Retailers and Stores
   - Consolidates: Store, Stores, Retailers & store, Retailers and store
   - Applied to items tagged generically without specific business name

3. **Business names - specific leaf nodes with full forms as preferred:**
   - Douglas and Company (primary) ← Douglas & Co. (synonym)
   - Peckman Brothers (primary) ← Peckman Bros (synonym)
   - Tabrett and Company (primary) ← Tabrett and Co. (synonym)
   - Nimmo's (unchanged)
   - All have parent: Retailers and Stores

**Impact:**

- **Hierarchy cleanup:** Single clean branch replaces two duplicate branches
- **Pattern consistency:** Follows established taxonomy pattern (plural parent + singular generic leaf + specific leaves)
- **Improved clarity:** Clear distinction between parent category, generic instances, and specific businesses
- **Better searchability:** Full business names more discoverable than abbreviations
- **Historical preservation:** Abbreviated forms retained as synonyms for archival references
- **Tagging precision:** Generic "Retailer or Store" available for unspecified businesses, specific names for identified ones

**Getty AAT alignment:**

- AAT uses "stores (built works)" for retail buildings
- AAT uses "retailers" for commercial entities/organisations
- Our "Retailer or Store" accommodates both senses with parent relationships:
  - Parent: Commercial businesses (Agents facet - organisational sense)
  - Can also relate to Built Environment facet where appropriate

**Key Principles:**

This consolidation demonstrates:

1. **Eliminate duplication:** Remove parallel redundant hierarchies
2. **Leaf-node tagging pattern:** Only leaf nodes (specific businesses and generic term) used for tagging; plural parent never directly applied
3. **Standardise naming:** Consistent use of spelled-out business names
4. **Preserve historical forms:** Abbreviations retained as synonyms
5. **Taxonomic consistency:** Matches established pattern across entire taxonomy (Hotels > Hotel, Schools > School, etc.)
6. **Quality control:** Regular hierarchy visualisation catches duplication issues

---

## Schools of Arts Tag Consolidation and Recursive Nesting Fix

**Date:** 2025-10-31

**Tags affected:**

Parent category issues:

- `Schools of Arts` (plural parent - had polyhierarchical parents)
- `School of Arts` (singular - was incorrectly acting as both parent AND leaf)

Generic leaf consolidation:

- `School of Arts` (singular generic leaf - proper role)
- `School of Art` → `School of Arts` (variant spelling without 's' on Art)

Plural variant consolidation:

- `Schools of Art` → `Schools of Arts` (variant spelling without 's' on Art)

Specific institution:

- `Katoomba School of Arts` (specific leaf - had multiple incorrect parents)

**Rationale:**

Hierarchy visualisation revealed severe structural problems in the Schools of Arts taxonomy:

1. **Recursive nesting:** "School of Arts" appeared as both a parent node AND a child node, creating infinite loops in the hierarchy
2. **Multiple incorrect parents:** "Katoomba School of Arts" had four parent relationships instead of one
3. **Ambiguous role:** "School of Arts" was simultaneously acting as:
   - A parent of other schools
   - A generic term for unspecified Schools of Arts
   - A child of "Schools of Arts"
   - A child of "Cultural societies", "Halls", and "School"
4. **Spelling variants:** "School of Art" and "Schools of Art" (without 's' on "Arts")

This violated the leaf-node tagging pattern and created navigational confusion.

**Evidence:**

Original problematic structure from hierarchy tree:

```
│   │   │   ├── Katoomba School of Arts
│   │   │   ├── School of Arts
│   │   │   │   ├── Katoomba School of Arts (duplicate!)
│   │   │   │   └── School of Art
│   │   │   └── Schools of Arts
│   │   │       ├── Katoomba School of Arts (duplicate!)
│   │   │       ├── School of Arts (recursive!)
│   │   │       │   ├── Katoomba School of Arts (duplicate!)
│   │   │       │   └── School of Art
│   │   │       └── Schools of Art
```

CSV showed:
- "School of Arts" had 4 parent relationships (Cultural societies, Halls, School, Schools of Arts)
- "Katoomba School of Arts" had 4 parent relationships (Cultural societies, Halls, School of Arts, Schools of Arts)
- "School of Arts" also had children (creating the recursive structure)

**Changes implemented:**

1. **Clarified parent node:**
   - **Schools of Arts** remains the plural parent
   - Maintains polyhierarchical relationships to: Cultural societies, Halls
   - Never directly applied to items

2. **Fixed generic leaf:**
   - **School of Arts** now ONLY a singular generic leaf under "Schools of Arts"
   - Removed incorrect parent relationships (Cultural societies, Halls, School)
   - Removed child relationships (no longer acts as parent)
   - Applied to items mentioning "a School of Arts" without specifying which one

3. **Consolidated spelling variants:**
   - "School of Art" (no 's' on Art) → synonym of "School of Arts"
   - "Schools of Art" (no 's' on Art) → synonym of "Schools of Arts"

4. **Fixed specific institution:**
   - **Katoomba School of Arts** now has single parent: Schools of Arts
   - Removed incorrect parent relationships (Cultural societies, Halls, School of Arts)
   - Appears exactly once in hierarchy as a leaf node

**Impact:**

- **Eliminated recursion:** "School of Arts" no longer creates circular parent-child relationships
- **Fixed duplication:** "Katoomba School of Arts" appears once instead of four times
- **Pattern compliance:** Now follows leaf-node tagging pattern (plural parent + singular generic + specific leaves)
- **Navigation clarity:** Users can now browse: Schools of Arts > School of Arts (generic) OR Schools of Arts > Katoomba School of Arts (specific)
- **Polyhierarchy preserved:** "Schools of Arts" maintains appropriate relationships to Cultural societies and Halls at parent level

**Getty AAT alignment:**

- AAT 300026030: "schools of arts" (community halls in Australian/New Zealand context)
- AAT structure: plural parent terms with specific instances as narrower terms
- Our structure now matches: Schools of Arts (parent) > specific institutions (narrower terms)

**Historical context:**

Schools of Arts in the Blue Mountains context were community institutions combining:
- Meeting halls (hence relationship to Halls)
- Cultural/educational societies (hence relationship to Cultural societies)
- NOT educational "schools" in the modern sense (removed incorrect "School" parent)

The dual polyhierarchical relationship to both "Cultural societies" and "Halls" is appropriate because these institutions functioned as both organisations AND buildings.

**Key Principles:**

This consolidation demonstrates:

1. **Prevent recursive structures:** A node cannot be both parent and child
2. **Single responsibility:** Each term has ONE clear role (parent, generic leaf, or specific leaf)
3. **Leaf-node tagging:** Only leaves are tagged; parents organise
4. **Polyhierarchy at parent level:** Multiple broader terms applied to parent node, not duplicated to all children
5. **Spelling standardisation:** "Arts" (with 's') is standard Australian terminology for these institutions
6. **Quality control:** Hierarchy visualisation essential for catching structural anomalies

---

## Bands Duplication Fix

**Date:** 2025-10-31

**Tags affected:**

- `Bands` (plural parent)
- `Band` (singular generic leaf)
- `Katoomba band` (specific leaf - had duplicate parent relationships)

**Rationale:**

Similar to the Schools of Arts issue, "Katoomba band" had two parent relationships:
1. Parent: Band (incorrect - creating nested structure)
2. Parent: Bands (correct - direct child of plural parent)

This caused "Katoomba band" to appear twice in the hierarchy.

**Evidence:**

Original problematic structure:
```
Bands
├── Band
│   └── Katoomba band (child of Band)
└── Katoomba band (child of Bands)
```

**Changes implemented:**

- Removed parent relationship: Katoomba band → Band
- Retained correct relationship: Katoomba band → Bands
- Result: Katoomba band appears once as a leaf node

**Corrected structure:**
```
Bands (plural parent)
├── Band (singular generic leaf)
└── Katoomba band (specific leaf)
```

**Impact:**

- **Eliminated duplication:** Specific band now appears once
- **Pattern compliance:** Follows leaf-node tagging pattern
- **Navigation clarity:** Clear hierarchy with no nested redundancy

**Key Principle:**

Specific named entities (like "Katoomba band") should be direct children of the plural parent, not children of the generic singular leaf. Both the generic leaf ("Band") and specific leaves ("Katoomba band") are peers at the same hierarchical level.

---

## Lodges Taxonomy Comprehensive Rationalisation

**Date:** 2025-10-31

**Context:**

Fraternal organizations (lodges) taxonomy had multiple structural problems that accumulated despite previous corrections in October 2025. This rationalisation addresses variant names still in hierarchy, duplicate placements, building/organization mixing, and terminology clarity issues.

**Tags affected:**

### Variant Names → Synonyms
- `Druids` → `United Ancient Order of Druids` (synonym: informal name)
- `U.A.O.D.` → `United Ancient Order of Druids` (synonym: acronym)
- `Masons` → `Freemasons` (synonym: informal name)
- `Oddfellows` → `Odd Fellows` (synonym: variant spelling)

### Duplicate Placements Fixed
- `Druid's Lodge` - removed 2 incorrect parents (Druids, Lodges), kept only under United Ancient Order of Druids
- `Mountaineer Lodge` - removed duplicate under Lodges, kept only under Unaffiliated lodges
- `Masonic Hall` - removed organizational parents (Lodges, Masons), kept only under Halls (Built Environment)
- `Odd Fellows' Hall` - removed organizational parents (Lodges, Odd Fellows), kept only under Halls (Built Environment)

### Terminology Clarification
- `Independent lodges` → `Unaffiliated lodges` (avoids confusion with "Independent Order of Odd Fellows")
- `Independent lodge` → `Unaffiliated lodge` (singular generic)

### Unnecessary Terms Removed
- `United Ancient Order of Druid` (singular generic) - not needed; use plural form only

**Rationale:**

### 1. Variant Names Still in Hierarchy
Despite October 2025 validation report stating variants should be synonyms, these terms were still appearing as hierarchy nodes:
- **Druids** and **U.A.O.D.** under Lodges (should be synonyms of United Ancient Order of Druids)
- **Masons** under Lodges (should be synonym of Freemasons)
- **Oddfellows** under Odd Fellows (should be synonym)

This violated the established pattern: "Synonyms and variant names are NOT represented as child tags in the hierarchy."

### 2. Triple Duplication of Druid's Lodge
`Druid's Lodge` appeared THREE times:
- As child of "Druids" (incorrect - Druids shouldn't exist as hierarchy node)
- As child of "Lodges" (incorrect - should only be under specific organization)
- As "Druid's Lodge (local lodge)" under "United Ancient Order of Druids" (✓ correct)

Only the qualified form under UAOD is correct - this represents a specific local chapter.

### 3. Building/Organization Confusion
**Masonic Hall** and **Odd Fellows' Hall** are BUILDINGS (Built Environment facet), not organizations (Agents facet).

Previous validation report (October 2025) established:
- Source text: "forming a Druid's Lodge" = organization
- Masonic Hall → Built Environment (BUILDING) ✅
- Odd Fellows' Hall → Built Environment (BUILDING) ✅

However, these buildings still had organizational parents creating polyhierarchical confusion.

### 4. Terminology Ambiguity: "Independent"
**Problem:** "Independent Order of Odd Fellows" (IOOF) is the official NAME of the organization - the word "Independent" is part of the proper name, NOT a description of affiliation status.

**Confusion:** "Independent lodges" category was meant for lodges unaffiliated with national/international bodies (e.g., Mountaineer Lodge), but this creates ambiguity:
- Is "Independent Order of Odd Fellows" an "independent lodge"? NO - it's a national organization.
- Is "Mountaineer Lodge" an "independent lodge"? YES - it's locally unaffiliated.

**Solution:** Rename to "Unaffiliated lodges" for clarity.

**Getty AAT Check:** Getty AAT has no specific guidance on fraternal lodge affiliation terminology. "Unaffiliated" is clearer and unambiguous.

### 5. Unnecessary Singular Generic
"United Ancient Order of Druid" (singular) serves no purpose - the organization has specific local chapters (like Druid's Lodge), but no generic usage requiring a singular form.

**Evidence:**

Original problematic structure from hierarchy tree:

```
Fraternal orders & lodges
└── Lodges
    ├── Druid's Lodge (duplicate #1)
    ├── Druids (should be synonym)
    │   ├── Druid (singular)
    │   ├── Druid's Lodge (duplicate #2)
    │   └── U.A.O.D. (should be synonym)
    ├── Freemasons
    ├── Independent Order of Odd Fellows
    ├── Independent lodges (ambiguous name)
    │   ├── Independent lodge (singular)
    │   └── Mountaineer Lodge
    ├── Lodge (generic)
    ├── Masonic Hall (BUILDING mixed with organizations!)
    ├── Masons (should be synonym)
    │   ├── Mason (singular)
    │   └── Masonic Hall (duplicate!)
    ├── Mountaineer Lodge (duplicate!)
    ├── Odd Fellows
    │   ├── Odd Fellow (singular)
    │   ├── Odd Fellows' Hall (BUILDING!)
    │   └── Oddfellows (should be synonym)
    ├── Odd Fellows' Hall (duplicate!)
    └── United Ancient Order of Druids
        ├── Druid's Lodge (local lodge) (✓ correct)
        └── United Ancient Order of Druid (unnecessary singular)
```

**Changes implemented:**

### 1. Converted Variants to Synonyms
```csv
United Ancient Order of Druids,Druids,synonym,Informal name for United Ancient Order of Druids
United Ancient Order of Druids,U.A.O.D.,synonym,Acronym for United Ancient Order of Druids
Freemasons,Masons,synonym,Informal name for Freemasons
Odd Fellows,Oddfellows,synonym,Variant spelling of Odd Fellows
```

### 2. Eliminated Duplicate Placements
**Druid's Lodge:**
- DELETED: parent=Druids
- DELETED: parent=Lodges
- KEPT: Druid's Lodge (local lodge), parent=United Ancient Order of Druids

**Mountaineer Lodge:**
- DELETED: parent=Lodges
- KEPT: parent=Unaffiliated lodges

**Masonic Hall (building separation):**
- DELETED: parent=Lodges
- DELETED: parent=Masons (which no longer exists as hierarchy node)
- KEPT: parent=Halls (Built Environment facet)

**Odd Fellows' Hall (building separation):**
- DELETED: parent=Lodges
- DELETED: parent=Odd Fellows
- KEPT: parent=Halls (Built Environment facet)

### 3. Renamed for Clarity
```csv
Independent lodges → Unaffiliated lodges
Independent lodge → Unaffiliated lodge (singular generic)
```
Updated Mountaineer Lodge parent accordingly.

### 4. Removed Unnecessary Terms
DELETED: United Ancient Order of Druid (singular generic not needed)

**Corrected structure:**

```
Fraternal orders & lodges
└── Lodges
    ├── Lodge (generic leaf)
    ├── Freemasons (specific organization leaf)
    ├── Odd Fellows (specific organization leaf)
    ├── United Ancient Order of Druids (specific organization)
    │   └── Druid's Lodge (local lodge) (local chapter leaf)
    └── Unaffiliated lodges
        ├── Unaffiliated lodge (generic leaf)
        └── Mountaineer Lodge (specific unaffiliated lodge leaf)
```

**Synonyms (not in hierarchy):**
- Masons → Freemasons
- Oddfellows → Odd Fellows
- Druids → United Ancient Order of Druids
- U.A.O.D. → United Ancient Order of Druids

**Buildings (separate Built Environment facet):**
- Masonic Hall (parent: Halls)
- Odd Fellows' Hall (parent: Halls)

**Impact:**

- **Eliminated all duplication:** Each entity appears exactly once in correct location
- **Separated building/organization facets:** Buildings in Built Environment, organizations in Agents
- **Variant consolidation:** All informal names, acronyms, and spellings are synonyms (will merge in Zotero retagging)
- **Terminology clarity:** "Unaffiliated lodges" unambiguous vs. "Independent Order of Odd Fellows"
- **Pattern compliance:** Follows leaf-node tagging pattern consistently
- **Zotero-ready:** Structure maps cleanly to tag application without confusion

**Zotero Application Implications:**

When these changes are applied to Zotero (Phase 1.4):

1. **Synonyms will consolidate:**
   - Items tagged "Masons" → retagged as "Freemasons"
   - Items tagged "Druids" or "U.A.O.D." → retagged as "United Ancient Order of Druids"
   - Items tagged "Oddfellows" → retagged as "Odd Fellows"

2. **Buildings separated from organizations:**
   - "Masonic Hall" and "Odd Fellows' Hall" remain valid tags in Built Environment
   - No conflation with organizational tags

3. **Clear tagging options:**
   - Generic: "Lodge", "Unaffiliated lodge"
   - Specific organizations: "Freemasons", "Odd Fellows", "United Ancient Order of Druids"
   - Local chapters: "Druid's Lodge (local lodge)"
   - Specific unaffiliated: "Mountaineer Lodge"

4. **Parent nodes not applied:**
   - "Lodges", "Unaffiliated lodges" are organizational only
   - Only leaf nodes become actual Zotero tags

**Getty AAT Alignment:**

- AAT 300025950: "associations (organizations)" - broad term for organized groups
- AAT has no specific "fraternal organizations" or "lodges" term
- Our structure: Lodges as organizational category under "Fraternal orders & lodges"
- Buildings (Halls) correctly placed in Objects/Built Environment facet per AAT pattern
- Separation of organization/building senses follows AAT disambiguation practices

**Historical Context:**

Blue Mountains fraternal organizations were significant social institutions:
- **Freemasons:** Met at Masonic Hall (building separate from organization)
- **Odd Fellows (IOOF):** Independent Order of Odd Fellows met at Odd Fellows' Hall
- **United Ancient Order of Druids:** Local chapter "Druid's Lodge" established 1892 (also known as Jersey Lodge U.A.O.D.)
- **Mountaineer Lodge:** Local unaffiliated lodge, not part of national fraternal order

**Key Principles:**

This comprehensive rationalisation demonstrates:

1. **Enforce synonym pattern:** Variants NEVER appear as hierarchy children
2. **Eliminate duplication:** Each entity in ONE correct location only
3. **Separate facets:** Buildings (Built Environment) vs. Organizations (Agents)
4. **Terminology precision:** Use unambiguous terms ("Unaffiliated" not "Independent")
5. **Remove unnecessary terms:** Singular generics only when actually needed for tagging
6. **Leaf-node compliance:** Only leaves are taggable; parents organize
7. **Zotero readiness:** Structure must map cleanly to actual tag application
8. **Quality control:** Regular hierarchy visualization catches accumulated problems

---

## Removal of Unnecessary Singular Generics (Organizational Authorities)

**Date:** 2025-10-31

**Tags affected:**

Removed unnecessary singular generic forms:
- `Postal authority` (singular generic under Postal authorities)
- `Railway authority` (singular generic under Railway authorities)

**Rationale:**

Not all plural parent categories require a singular generic leaf. Singular generics serve a specific purpose: to tag items where the source text mentions the category generically without naming the specific entity.

**When singular generics ARE needed:**
- "stayed at a hotel" (without naming which) → tag as "Hotel"
- "attended a school" (without naming which) → tag as "School"
- "a mountain feature" (without specifying) → tag as "Mountain feature"

**When singular generics are NOT needed:**
- Source text would never say "a postal authority" generically
- Source text would either:
  1. Name the specific authority: "Postal Department"
  2. Discuss postal services thematically
- These are organizational entities that are always named/specific, not generic categories

**Evidence:**

Examination of usage patterns shows:
- Postal authorities = specific government departments (e.g., "Postal Department")
- Railway authorities = specific government commissions (e.g., "Railway commission")
- No scenarios where you'd tag generically without knowing the specific entity name

**Comparison with other categories:**

**Keep singular generic (makes sense):**
- Hotels → Hotel (source: "stayed at a hotel")
- Schools → School (source: "attended a school")
- Postal facilities → Postal facility (source: "a postal facility" - could be any post office/mail depot)
- Public officials → Public official (source: "a public official" - unnamed official)

**Remove singular generic (doesn't make sense):**
- Postal authorities → ~~Postal authority~~ (would always be named: "Postal Department")
- Railway authorities → ~~Railway authority~~ (would always be named: "Railway commission")

**Corrected structure:**

```
Government bodies
├── Postal authorities
│   └── Postal Department (specific authority only)
└── Railway authorities
    └── Railway commission (specific authority only)
```

**Impact:**

- **Clearer tagging guidance:** No confusion about when to use authority tags
- **Pattern refinement:** Singular generics only where functionally needed
- **Taxonomy precision:** Distinguishes between generic-able categories (hotels, schools) vs. always-specific entities (government authorities)

**Key Principle:**

**Singular generic leaves should only exist when there are realistic scenarios where source text would mention the category generically without naming the specific entity.** Government authorities, regulatory bodies, and official organizational entities are always named/specific in historical sources and don't require generic forms.

This refinement clarifies the leaf-node tagging pattern: not every plural parent needs a singular generic - only those where generic tagging is semantically meaningful.

---

## Law Enforcement Facet Correction (Activity vs. Occupation)

**Date:** 2025-10-31

**Tags affected:**

Fixed incorrect facet placement:
- `Law enforcement` - removed incorrect `parent=Occupations` relationship

**Rationale:**

Confusion between two semantically distinct concepts with similar names:

1. **"Law enforcement" (ACTIVITY)** - The activity/function of enforcing laws
2. **"Law enforcement personnel" (AGENTS/OCCUPATIONS)** - The people who perform law enforcement

**Problem:** "Law enforcement" incorrectly had `parent=Occupations`, placing the ACTIVITY under the Agents facet.

**Correct structure:**

**Activities facet:**
```
Activities
└── Societal activities
    └── Law enforcement (the activity)
        └── Policing (the activity of police work)
```

**Agents facet:**
```
People
└── Occupations
    └── Law enforcement personnel (the occupation category)
        └── Police officers (the people)
            ├── Constable (rank/occupation)
            └── Senior-Constable (rank/occupation)
```

**Evidence:**

Hierarchy tree showed "Law enforcement" appearing under Agents > Occupations, which is semantically incorrect. Activities (what people DO) belong in the Activities facet, not the Agents facet (WHO does things).

**Comparison with similar facet distinctions:**

- **Mining** (activity - Activities facet) vs. **Miners** (people - Agents facet)
- **Teaching** (activity - Activities facet) vs. **Teachers** (people - Agents facet)
- **Law enforcement** (activity - Activities facet) vs. **Law enforcement personnel** (people - Agents facet)

**Changes implemented:**

DELETED: `Law enforcement,Law enforcement,hierarchy,parent=Occupations`

KEPT:
- `Law enforcement,hierarchy,parent=Justice & Crime - THEMATIC` (thematic grouping)
- `Law enforcement,hierarchy,parent=Societal activities` (correct facet - Activities)
- `Law enforcement personnel,hierarchy,parent=Occupations` (people - correct facet - Agents)

**Impact:**

- **Facet purity:** Activities facet contains only activities; Agents facet contains only agents
- **Semantic clarity:** Clear distinction between actions and actors
- **Getty AAT alignment:** Follows AAT pattern of separating activities from agents
- **Navigation improvement:** Users browsing "what people did" vs. "who did things" get correct results

**Getty AAT Alignment:**

AAT maintains strict separation between:
- **Activities Facet** (300264087) - actions, processes, functions
- **Agents Facet** (300264090) - people, organizations, groups

Our correction aligns with this fundamental AAT principle.

**Key Principle:**

**Activities (what is DONE) vs. Agents (WHO does it):** Maintain strict facet separation. When terms are semantically similar (e.g., "law enforcement" vs. "law enforcement personnel"), ensure correct facet placement based on the fundamental distinction between actions and actors.

---

## Coroners Hierarchy Duplication and Nesting Fix

**Date:** 2025-10-31

**Tags affected:**

Fixed duplicate placements and recursive nesting:
- `Coroner` - removed incorrect `parent=Legal officials`
- `Coroner Lethbridge` - removed incorrect parents (`parent=Coroner`, `parent=Legal officials`)

**Rationale:**

Same pattern of problems seen throughout taxonomy rationalisation:

1. **Quadruple duplication of Coroner Lethbridge** - appeared 4 times due to 3 parent relationships
2. **Duplicate branch for Coroner** - appeared as both child of "Coroners" and "Legal officials"
3. **Recursive nesting** - Coroner Lethbridge nested under Coroner under Coroners (violates leaf-node pattern)

**Evidence:**

Original problematic structure from hierarchy tree:

```
Legal officials
├── Coroner
│   └── Coroner Lethbridge (duplicate #1)
├── Coroner Lethbridge (duplicate #2)
├── Coroners
│   ├── Coroner (recursive!)
│   │   └── Coroner Lethbridge (duplicate #3)
│   └── Coroner Lethbridge (duplicate #4)
└── Legal official
```

CSV showed:
- `Coroner` had 2 parent relationships: Coroners, Legal officials
- `Coroner Lethbridge` had 3 parent relationships: Coroner, Coroners, Legal officials

**Changes implemented:**

DELETED:
- `Coroner,hierarchy,parent=Legal officials` (creates duplicate branch)
- `Coroner Lethbridge,hierarchy,parent=Coroner` (creates recursive nesting)
- `Coroner Lethbridge,hierarchy,parent=Legal officials` (should only be under Coroners)

KEPT:
- `Coroners,hierarchy,parent=Legal officials` (category parent)
- `Coroner,hierarchy,parent=Coroners` (singular generic leaf)
- `Coroner Lethbridge,hierarchy,parent=Coroners` (specific person leaf)

**Corrected structure:**

```
Legal officials
├── Coroners (plural parent - category for coroners)
│   ├── Coroner (singular generic leaf)
│   └── Coroner Lethbridge (specific person leaf)
└── Legal official (singular generic for unspecified legal official)
```

**Impact:**

- **Eliminated quadruple duplication:** Coroner Lethbridge appears once
- **Removed recursive nesting:** Singular generic and specific leaves are peers, not nested
- **Pattern compliance:** Follows leaf-node tagging pattern consistently
- **Clear structure:** Coroners as intermediate category under Legal officials

**Key Principle:**

This fix demonstrates the same principles applied throughout today's rationalisation session:
1. Specific named entities (Coroner Lethbridge) are direct children of plural parent (Coroners)
2. Generic singular (Coroner) and specific leaves are peers at same hierarchical level
3. Each entity appears exactly once in correct location
4. No recursive nesting of singular generic → specific pattern

---

## Military Personnel Duplication Fix

**Date:** 2025-10-31

**Tags affected:**

Fixed duplicate placement:
- `Major Sir Charles George Gordon` - removed incorrect `parent=Military personnel`

**Rationale:**

Same duplication pattern - specific person appearing both as direct child of category parent AND as child of intermediate category.

**Evidence:**

Original structure:
```
Military personnel
├── Major Sir Charles George Gordon (duplicate #1)
└── Soldiers
    └── Major Sir Charles George Gordon (duplicate #2)
```

**Changes implemented:**

DELETED: `Major Sir Charles George Gordon,hierarchy,parent=Military personnel`

KEPT: `Major Sir Charles George Gordon,hierarchy,parent=Soldiers`

**Corrected structure:**

```
Military personnel (occupation category)
└── Soldiers (specific military occupation)
    └── Major Sir Charles George Gordon (specific person)
```

**Impact:**

- **Eliminated duplication:** Specific person appears once in correct location
- **Clear hierarchy:** Person under specific occupation (Soldiers) rather than generic category (Military personnel)
- **Pattern compliance:** Follows established hierarchy pattern

---

## Unemployment vs. Unemployment Relief Facet Correction

**Date:** 2025-10-31

**Tags affected:**

Fixed incorrect hierarchical relationship:
- `Unemployment relief` - removed incorrect `parent=Unemployment`

**Rationale:**

Semantically incorrect parent-child relationship causing tagging problems.

**Problem:**
1. "Unemployment" couldn't be tagged (was a parent node with "Unemployment relief" as child)
2. Semantically wrong relationship - unemployment relief is NOT a "type of" unemployment

**Semantic distinction:**
- **Unemployment** = CONCEPT/CONDITION (the state of being without work) → Associated Concepts facet
- **Unemployment relief** = ACTIVITY (charitable/welfare efforts to help the unemployed) → Activities facet

**Evidence:**

Original problematic structure:
```
Associated Concepts
└── Social & economic concepts
    └── Unemployment (parent - can't be tagged!)
        └── Unemployment relief (child)
```

This created two problems:
1. "Unemployment" was untaggable due to having a child
2. The relationship implies "unemployment relief" is a subcategory of "unemployment" (semantically incorrect)

**Correct relationship:**

These concepts are **related but not hierarchical**:
- Both relate to **economic distress/hardship** (thematic grouping)
- But they belong in **different primary facets** (Associated Concepts vs. Activities)
- The relationship is: unemployment relief is a **response TO** unemployment, not a **type OF** unemployment

**Changes implemented:**

DELETED: `Unemployment relief,hierarchy,parent=Unemployment`

KEPT:
- **Unemployment** maintains parents:
  - `parent=Social & economic concepts` (Associated Concepts facet)
  - `parent=Economic distress - THEMATIC`
  - `parent=Economic hardship - THEMATIC`

- **Unemployment relief** maintains parents:
  - `parent=Charitable and welfare activities` (Activities facet)
  - `parent=Economic distress - THEMATIC`
  - `parent=Economic hardship - THEMATIC`

**Corrected structure:**

**Associated Concepts facet:**
```
Social & economic concepts
└── Unemployment (leaf - now taggable)
```

**Activities facet:**
```
Charitable and welfare activities
└── Unemployment relief (leaf - taggable)
```

**Thematic groupings (maintain relationship without hierarchy):**
```
Economic distress - THEMATIC
├── Unemployment
└── Unemployment relief

Economic hardship - THEMATIC
├── Unemployment
└── Unemployment relief
```

**Impact:**

- **Both concepts now taggable:** As independent leaf nodes in appropriate facets
- **Correct semantic relationships:** Related through thematic groupings, not parent-child
- **Facet purity:** Concepts in Associated Concepts, activities in Activities
- **Improved precision:** Can tag unemployment (the condition) separately from unemployment relief (the response)

**Key Principle:**

**Not all semantic relationships should be expressed as parent-child hierarchies.** When concepts are related but belong to different facets (e.g., a condition and a response to that condition), maintain the relationship through **thematic groupings** rather than creating inappropriate hierarchical dependencies that prevent both concepts from being taggable.

This aligns with Getty AAT practice of using polyhierarchical relationships and associative relationships rather than forcing all related concepts into strict parent-child hierarchies.

---

## Unemployment Insurance - Financial Services Activity (2025-10-31)

**Decision:** Add "Unemployment insurance" as a new leaf node under a new Financial services hierarchy in the Activities facet, with polyhierarchical relationships to thematic groupings.

**Context:**

User requested addition of "Unemployment insurance" to distinguish it from "Unemployment relief" already in the taxonomy. Research into late 19th/early 20th century Australian social welfare context revealed important distinctions.

**Historical Context (Late 19th - Early 20th Century Australia):**

- **Private/mutual aid provision:** Unemployment insurance was provided primarily by friendly societies (Oddfellows, Druids, etc.) and trade unions through voluntary, contributory schemes
- **No government programme:** State unemployment benefits did not exist in Australia until 1945
- **Commercial/mutual nature:** Members paid premiums into schemes that provided benefits during unemployment
- **Distinct from relief:** Government "unemployment relief" (sustenance programmes from 1930s) was charitable/welfare assistance, while unemployment insurance was a financial service/mutual aid arrangement

**Getty AAT Alignment:**

- AAT includes "insurance" (AAT:300055719) under economic concepts with scope note: "Coverage by contract whereby for a stipulated consideration one party undertakes to indemnify or guarantee another against loss by a specified contingency or peril"
- Insurance provision (the activity) belongs in Activities facet, while insurance (the concept) belongs in Associated Concepts facet
- This follows AAT pattern of distinguishing concepts from activities

**Rationale:**

Three related but distinct concepts now exist:

1. **Unemployment** (Associated Concepts facet) - the social/economic condition of being unemployed
2. **Unemployment relief** (Activities facet > Charitable and welfare activities) - government or charitable assistance provided to the unemployed
3. **Unemployment insurance** (Activities facet > Economic activities > Financial services) - commercial/mutual aid insurance coverage for unemployment

**Structure Added:**

**Activities facet:**
```
Activities
└── Economic activities
    └── Financial services (new parent)
        └── Insurance provision (new parent)
            └── Unemployment insurance (new leaf - taggable)
```

**Polyhierarchical relationships maintained via thematic groupings:**
```
Economic distress - THEMATIC
├── Unemployment
├── Unemployment relief
└── Unemployment insurance (NEW)

Economic hardship - THEMATIC
├── Unemployment
├── Unemployment relief
└── Unemployment insurance (NEW)
```

**CSV Entries Added:**

Lines 210-214 in tag_map_consolidated.csv:
```csv
Financial services,Financial services,hierarchy,parent=Economic activities
Insurance provision,Insurance provision,hierarchy,parent=Financial services
Unemployment insurance,Unemployment insurance,hierarchy,parent=Insurance provision
Unemployment insurance,Unemployment insurance,hierarchy,parent=Economic distress - THEMATIC
Unemployment insurance,Unemployment insurance,hierarchy,parent=Economic hardship - THEMATIC
```

**Impact:**

- **Three-way distinction:** Clear separation between condition, charitable response, and commercial/mutual aid response
- **Accurate historical representation:** Reflects the actual nature of unemployment insurance in the Blue Mountains period (1890s-1930s)
- **Extensible structure:** Financial services > Insurance provision hierarchy can accommodate future insurance-related tags (life insurance, fire insurance, etc.)
- **Facet purity:** Economic activities in Activities facet, concepts in Associated Concepts facet
- **Getty AAT alignment:** Follows AAT pattern for distinguishing concepts from activities

**Key Principle:**

**Financial services and insurance provision are economic activities, not charitable activities.** Even when serving social welfare functions (as friendly societies did), insurance operates on commercial/mutual aid principles (premiums, contracts, coverage) rather than charitable principles (donations, need-based assistance). This distinction is critical for accurate historical representation and aligns with Getty AAT structure.

---

## Hunting - Corrected Facet Placement (2025-10-31)

**Decision:** Move "Hunting" from erroneous top-level facet to Activities facet under Economic activities.

**Issue:**

An erroneous top-level facet "Hunting" was created (visualizations/hierarchy_trees/primary_hunting.txt) containing only "Wild horse culling". This violated the taxonomy structure which should have seven primary facets aligned with Getty AAT.

**Context:**

- "Wild horse culling" was tagged with `parent=Hunting`
- However, "Hunting" was not defined in tag_map_consolidated.csv with its own parent
- This created an orphaned parent node that generated a spurious top-level facet
- Hunting is an activity, not a facet

**Resolution:**

Added Hunting as a parent under Economic activities (alongside Agriculture, Mining, Tourism, etc.):

```csv
Hunting,Hunting,hierarchy,parent=Economic activities
Wild horse culling,Wild horse culling,hierarchy,parent=Hunting
```

**Structure:**

```
Activities (facet)
└── Economic activities
    ├── Agriculture
    │   └── Animal husbandry
    │       └── Animal breeding
    │           └── Horse breeding
    └── Hunting (NEW parent)
        └── Wild horse culling (existing leaf)
```

**Rationale:**

- **Economic activity classification:** Hunting (including culling for pest control/management) is an economic activity, similar to agriculture and mining
- **Resource management:** Wild horse culling is a land/resource management activity, making it appropriate under Economic activities
- **Getty AAT alignment:** Hunting in the AAT is classified under Activities, not as a top-level facet
- **Facet integrity:** Maintains the seven primary facets without spurious additions

**Files Updated:**

- `data/tag_map_consolidated.csv:1059` - Added Hunting parent definition
- Removed `visualizations/hierarchy_trees/primary_hunting.txt` - Erroneous file deleted

**Note on Classification:**

Hunting could alternatively fit under Recreation activities if the collection contained sport hunting references. However, given the specific context of "wild horse culling" (pest control/land management), Economic activities is more appropriate. Future hunting-related tags should be evaluated based on their specific context (sport/recreation vs. commercial/management).

---

## Settlements - Removed Duplicate Entry (2025-10-31)

**Decision:** Remove duplicate "Mining settlements" entry that incorrectly referenced undefined "Settlements" parent, eliminating spurious top-level facet.

**Issue:**

An erroneous top-level facet "Settlements" was created (visualizations/hierarchy_trees/primary_settlements.txt) due to a duplicate CSV entry. "Mining settlements" had two parent definitions:
- Line 454: Correct entry with `parent=Places (existing facet)`
- Line 1039: Duplicate entry with `parent=Settlements` (undefined parent)

The undefined "Settlements" parent created an orphaned node that generated a spurious eighth facet.

**Context:**

Mining settlements was correctly positioned under Places facet (alongside Mining districts, Natural features, Reserves, and Towns), but the duplicate entry with the undefined parent caused the visualization script to generate an extra facet file.

**Resolution:**

Removed the duplicate entry at line 1039:
```csv
Mining settlements,Mining settlements,hierarchy,parent=Settlements   # REMOVED
```

Retained the correct entries:
```csv
Mining settlements,Mining settlements,hierarchy,parent=Mining & Industry - THEMATIC  (line 453)
Mining settlements,Mining settlements,hierarchy,parent=Places (existing facet)        (line 454)
```

**Correct Structure:**

```
Places (facet)
├── Mining districts
│   ├── Mining district
│   ├── Nellie's Glen
│   ├── Ruined Castle
│   └── South Clifton
├── Mining settlements
│   ├── Mining settlement
│   ├── Middle camp
│   ├── Nellie's Glen (poly-hierarchy)
│   └── Ruined Castle (poly-hierarchy)
├── Natural features
├── Reserves
└── Towns
```

**Polyhierarchical Relationships:**

- **Mining settlements** has two valid parents:
  - `parent=Places (existing facet)` - Primary facet placement
  - `parent=Mining & Industry - THEMATIC` - Thematic grouping
- Individual settlements like Nellie's Glen and Ruined Castle appear in both Mining districts and Mining settlements (poly-hierarchy representing dual nature as geographic areas and settlement locations)

**Rationale:**

- **Facet integrity:** Settlements is not a Getty AAT primary facet; it belongs under Places
- **Duplicate removal:** Only one hierarchical parent definition should exist (line 454); thematic relationships are maintained separately (line 453)
- **Getty AAT alignment:** Places facet encompasses all geographic locations including settlements, districts, natural features, and towns

**Files Updated:**

- `data/tag_map_consolidated.csv:1039` - Removed duplicate entry
- Removed `visualizations/hierarchy_trees/primary_settlements.txt` - Erroneous file deleted

**Impact:**

- Maintains seven primary facets aligned with Getty AAT structure
- Preserves correct polyhierarchical relationships for mining settlements
- Mining settlements remains correctly positioned under Places facet

---

## Built Environment - Accommodation Consolidation (2025-10-31)

**Decision:** Consolidate "Accommodation and hospitality venues" and "Hospitality venues" into "Accommodation buildings" for consistency with Built Environment taxonomy.

**Issue:**

Built Environment facet had redundant and inconsistent parent nodes:
- "Accommodation and hospitality venues" (with 6 children: Boarding houses, Cottages, Dwellings, Hotels, Public houses, Stables)
- "Accommodation buildings" (with 3 duplicate children: Boarding houses, Dwellings, Hotels)
- "Hospitality venues" (with 1 child: Pubs)

This created duplication in the hierarchy visualizations and violated the naming consistency pattern.

**Context:**

Analysis of all Built Environment children revealed a clear pattern:
- Civic **buildings**
- Commercial **buildings**
- Community **buildings**
- Educational **buildings**
- Industrial **buildings**
- Religious **buildings**
- Infrastructure (different category)

Only the accommodation-related categories used "venues" terminology, breaking the consistent "buildings" pattern used for 7 out of 10 direct children of Built Environment.

**Getty AAT Alignment:**

Getty AAT classifies accommodation structures as building types (e.g., "single dwellings" AAT:300005424, "hotels" AAT:300007166) under the Objects facet, emphasising their physical/architectural nature rather than functional "venue" designation.

**Resolution:**

1. **Removed parent nodes:**
   - Line 17: `Accommodation and hospitality venues,hierarchy,parent=Built Environment` (REMOVED)
   - Line 284: `Hospitality venues,hierarchy,parent=Built Environment` (REMOVED)

2. **Retained and consolidated under:**
   - `Accommodation buildings,hierarchy,parent=Built Environment`

3. **Updated all children** to use `parent=Accommodation buildings`:
   - Boarding houses
   - Cottages
   - Dwellings
   - Hotels
   - Public houses
   - Pubs
   - Stables

4. **Removed duplicate entries** where children had both parents listed

**Final Structure:**

```
Built Environment (facet)
└── Accommodation buildings
    ├── Boarding houses
    │   ├── Boarding house
    │   └── Orama Boarding House
    ├── Cottages
    │   └── Cottage
    ├── Dwellings
    │   ├── Dwelling
    │   └── Miners' dwellings
    ├── Hotels
    │   ├── Hotel (generic)
    │   └── [30+ specific hotels]
    ├── Public houses
    │   └── Public house
    ├── Pubs
    │   └── Pub
    └── Stables
        └── Stable
```

**Rationale:**

- **Internal consistency:** Matches the "buildings" suffix used by all other Built Environment categories
- **Simplicity:** Single clear parent instead of three overlapping categories
- **Getty AAT alignment:** Emphasises physical/architectural classification appropriate for Built Environment facet
- **Eliminates duplication:** One parent definition per child, with polyhierarchical relationships maintained through thematic groupings (e.g., Alcohol-related venues, Hospitality businesses)
- **Semantic clarity:** "Accommodation buildings" clearly indicates these are architectural structures

**Polyhierarchical Relationships Preserved:**

Children maintain appropriate thematic relationships:
- Hotels → Alcohol-related venues - THEMATIC
- Hotels → Hospitality businesses
- Boarding houses → Hospitality businesses
- Public houses → Alcohol-related venues - THEMATIC
- Pubs → Alcohol-related venues - THEMATIC

**Impact:**

- **Consistency:** All Built Environment categories now follow "buildings" naming convention (except Infrastructure)
- **Deduplication:** Removed 2 redundant parent nodes and multiple duplicate child entries
- **Clarity:** Single unambiguous parent for all accommodation structures
- **Maintainability:** Simpler hierarchy easier to visualise and maintain

**Key Principle:**

**Within a facet, maintain consistent terminology patterns.** When most categories use a specific suffix ("buildings"), outliers using different terminology ("venues") should be evaluated for consolidation unless there is a compelling semantic distinction. The Built Environment facet represents physical structures, making "buildings" more appropriate than "venues" (which emphasises function over form).

---

## Civic Buildings - Remove Unused Generics (2025-10-31)

**Decision:** Remove unused generic terms and redundant "Council buildings" intermediate parent, simplifying to direct "Civic buildings > Council Chambers" relationship.

**Issue:**

Civic buildings had confusing duplication and unused generic terms:
- Council Chambers appeared twice (direct child of Civic buildings AND child of Council buildings)
- "Council buildings" intermediate parent with only one used child
- Two unused generic singular terms: "Civic building" and "Council building"

**Evidence from Collection:**

Tag frequency analysis revealed:
- ✅ "Council Chambers" - 7 items tagged (USED)
- ❌ "Civic building" - 0 items tagged (UNUSED)
- ❌ "Council building" - 0 items tagged (UNUSED)
- Note: "Councils" (27 items) exists but in Agents facet as organizations, not buildings

**Previous Structure:**
```
Civic buildings
├── Civic building (singular generic - UNUSED)
├── Council Chambers (direct child)
└── Council buildings (intermediate parent)
    ├── Council building (singular generic - UNUSED)
    └── Council Chambers (duplicate!)
```

**Simplified Structure:**
```
Civic buildings
├── Council Chambers (specific building - USED)
├── Court buildings
│   └── Court building (generic - KEPT as used)
├── Police facilities
└── Postal facilities
```

**Changes Made:**

1. **Removed entries:**
   - Line 135: `Council Chambers,hierarchy,parent=Council buildings` (duplicate removed)
   - Line 136: `Council buildings,hierarchy,parent=Civic buildings` (unused parent removed)
   - Line 943: `Civic building,hierarchy,parent=Civic buildings (singular generic term)` (unused generic removed)
   - Line 946: `Council building,hierarchy,parent=Council buildings (singular generic term)` (unused generic removed)

2. **Retained:**
   - Line 134: `Council Chambers,hierarchy,parent=Civic buildings` (direct, simple relationship)

**Rationale:**

- **Evidence-based pruning:** Only keep terms that are actually used in the collection
- **Simplicity:** Avoid creating unnecessary intermediate parents when there's only one child
- **YAGNI principle:** Don't create generic placeholders until collection evidence shows they're needed
- **Clarity:** Direct parent-child relationships are easier to understand and maintain

**Note on Court buildings:**

"Court buildings" intermediate parent was KEPT because:
- Multiple children exist (Court building, Courthouse, Katoomba Court)
- "Court building" generic is likely used (pending frequency verification if needed)
- Represents a genuine subcategory of civic buildings

**Impact:**

- Removed duplication of Council Chambers
- Removed 2 unused parent nodes
- Removed 2 unused generic singular terms
- Cleaner, simpler hierarchy based on actual collection usage
- Maintains appropriate structure for categories with multiple children (Court buildings, Police facilities, Postal facilities)

**Key Principle:**

**Don't create generic placeholders or intermediate parents without evidence from the collection.** The taxonomy should reflect actual tagging needs, not theoretical completeness. When only one specific instance exists (Council Chambers), use a direct relationship rather than creating an unused intermediate parent and generic term.

**Follow-up (same session):** Removed additional unused generic leaf nodes:
- "Court building" (0 items) - removed from Court buildings parent
- "Police facility" (0 items) - removed from Police facilities parent
- "Postal facility" (0 items) - removed from Postal facilities parent

Kept only used terms: Courthouse (8 items), Katoomba Court (8 items), Police station (4 items), Post office (23 items).

**Final Civic buildings structure:**
```
Civic buildings
├── Council Chambers
├── Court buildings
│   ├── Courthouse
│   └── Katoomba Court
├── Police facilities
│   └── Police station
└── Postal facilities
    └── Post office
```

Intermediate parents (Court buildings, Police facilities, Postal facilities) were retained as organizational nodes despite having few children, pending further review of whether they should be flattened.

---

## Schools of Arts - Dual-Nature Verification (2025-10-31)

**Decision:** VERIFIED - Current polyhierarchical structure correctly represents dual nature of Schools of Arts entities.

**Issue Raised:**

User questioned whether "Schools of Arts" appearing under "Halls" in Built Environment was correct, or if it should be:
1. Renamed to "Schools of Arts hall" to clarify it's the building, OR
2. Moved to be a higher-level category under Community buildings, OR
3. Kept as an organization-only term in Agents facet

**Context Review:**

Schools of Arts were historical community institutions (similar to Mechanics' Institutes or Literary Institutes) that operated cultural/educational programmes AND maintained physical hall buildings. This is a **known dual-nature entity** documented in:
- `reports/schools_of_arts_analysis.md` (town-specific investigation)
- `reports/dual_nature_analysis_churches_councils.md` (organizational vs. venue usage)

**Current Structure:**

The CSV correctly implements polyhierarchical relationships:

Line 709: `Schools of Arts,hierarchy,parent=Cultural societies` (Agents facet - organization)
Line 710: `Schools of Arts,hierarchy,parent=Halls` (Built Environment facet - building)

**How It Appears in Visualizations:**

**Agents facet:**
```
Cultural societies
└── Schools of Arts (the institution/organization)
    ├── Katoomba School of Arts
    └── School of Arts (generic)
```

**Built Environment facet:**
```
Community buildings
└── Halls
    └── Schools of Arts (the hall/building)
        ├── Katoomba School of Arts
        └── School of Arts (generic)
```

**Verification:**

This is the **CORRECT implementation** of dual-nature tagging. The tag "Schools of Arts" can be applied to items discussing:
- The cultural/educational organization (appears under Cultural societies in Agents)
- The physical hall building (appears under Halls in Built Environment)

**Why Not Rename to "Schools of Arts hall"?**

The polyhierarchical approach is superior to renaming because:
1. **Historical accuracy:** Sources refer to them as "School of Arts", not "School of Arts hall"
2. **Single tag for dual contexts:** Cataloguers apply one tag, hierarchy shows both aspects
3. **Getty AAT pattern:** Dual-nature entities maintain same term in multiple facets
4. **Established pattern:** Already used for Churches, Councils (building vs. organization)

**Why Not Make Schools of Arts a Top-Level Category?**

Schools of Arts are not numerous enough to warrant their own category under Community buildings. They are a specific type of community hall, appropriately categorized under "Halls" alongside Masonic Hall, Oddfellows' Hall, etc.

**Rationale:**

- **Dual-nature correctly modelled:** Polyhierarchical structure allows same tag to represent both aspects
- **Context-appropriate classification:** Organization under Cultural societies, building under Halls
- **User experience:** Tag once, appears in both facets appropriately
- **Maintains historical terminology:** Uses "School of Arts" as sources do

**Status:** Structure verified as correct. No changes needed.

**Key Principle:**

**Dual-nature entities use polyhierarchical relationships, not disambiguation suffixes.** When an entity has both organizational and physical aspects (Schools of Arts, Churches), use the same term in multiple facets rather than creating separate "X (organization)" and "X (building)" variants. This matches source terminology and provides better user experience.

---

## Decision 2025-10-31: Schools of Arts (venues) Parent Node Qualifier

**Date:** 2025-10-31
**Issue:** Dual-nature entity visualization clarity
**Tags Affected:** Schools of Arts hierarchy in Built Environment facet
**Decision:** Add parenthetical qualifier to parent node (not leaf nodes)

**Context:**

User requested clarification in visualization to distinguish the physical venue aspect of Schools of Arts from the organizational aspect. Initial request suggested adding "(venue)" to leaf nodes, but analysis revealed this would conflict with the polyhierarchical approach already established.

**Investigation:**

1. **Current structure is correct:** Schools of Arts already polyhierarchical
   - Line 709: parent=Cultural societies (organizational aspect)
   - Line 710: parent=Halls (physical building aspect)

2. **Alcohol tag pattern examined:** Found "Drunkenness (crime)" vs "Drunkenness (intoxication)" are SEPARATE tags (disambiguation), NOT polyhierarchical - different pattern

3. **Trade-off identified:** Two competing approaches:
   - **Polyhierarchy:** Same tag in multiple facets (current approach)
   - **Disambiguation:** Separate tags with parentheticals (alcohol model)

**Attempted Solution (FAILED):**

Attempted to add qualifier to PARENT node in Built Environment facet only:

**CSV Change Attempted (line 710):**
```csv
# Attempted change:
Schools of Arts (venues),Schools of Arts,hierarchy,parent=Halls
```

**Why This Failed:**

The CSV structure doesn't support different display names for the same tag in different facets. The visualization script uses `new_tag` as the node name, so:

1. **Renaming problem:** Changing `new_tag` to "Schools of Arts (venues)" actually RENAMES the tag
2. **Broken relationships:** Child nodes (`Katoomba School of Arts`, `School of Arts`) reference `parent=Schools of Arts`, not `parent=Schools of Arts (venues)`
3. **Cross-facet impact:** The rename would affect ALL facets, not just Built Environment
4. **Missing children:** The renamed parent node appeared without children in visualization

**Solution: Reverted Changes**

Reverted to original polyhierarchical structure without display qualifiers:
```csv
# Line 710 (reverted):
Schools of Arts,Schools of Arts,hierarchy,parent=Halls

# Line 340 (reverted):
Katoomba School of Arts,Katoomba School of Arts,hierarchy,parent=Schools of Arts

# Line 707 (reverted):
School of Arts,School of Arts,hierarchy,parent=Schools of Arts
```

**Lessons Learned:**

1. **CSV structure limitation:** Cannot have facet-specific display names with current data model
2. **Reinforces disambiguation approach:** This limitation supports the user's intuition that separate tags with parenthetical qualifiers (e.g., "Schools of Arts (organization)" vs "Schools of Arts (venue)") may be necessary
3. **Polyhierarchy vs disambiguation:** The current polyhierarchical approach works but lacks visualization clarity that disambiguation would provide

**Strategic Decision Deferred:**

User identified fundamental tension between polyhierarchy vs disambiguation approaches. Added comprehensive review item to planning/TODO.md (lines 42-140) documenting:
- Trade-offs between approaches
- Entities affected (~15-20)
- Research needed (Getty AAT practice investigation)
- Decision criteria (prioritizing Getty AAT alignment)
- **New evidence:** CSV structure limitation makes disambiguation approach more attractive

**Files Modified:**
- planning/TODO.md (new section lines 42-140) - strategic review item
- CLAUDE.md (interim guidance removed - not technically feasible)
- visualizations/hierarchy_trees/ (regenerated with original structure)

**Status:** No changes implemented. Polyhierarchical structure maintained without qualifiers. Strategic review pending Getty AAT research in Phase 1.3.

---

## Decision 2025-10-31: Educational Buildings Hierarchy Correction

**Date:** 2025-10-31
**Issue:** Duplicate school names in Educational buildings visualization
**Tags Affected:** Katoomba Public School, Katoomba Superior Public School, Megalong Valley School, Mount Victoria School, Sunday school
**Decision:** Remove incorrect `parent=School` relationships for named schools

**Problem Identified:**

User reported duplication in Educational buildings hierarchy:
```
├── Educational buildings
│   └── Schools
│       ├── Katoomba Public School        ← direct child of Schools
│       ├── Katoomba Superior Public School
│       ├── Megalong Valley School
│       ├── Mount Victoria School
│       └── School                        ← generic leaf node
│           ├── Katoomba Public School    ← DUPLICATE
│           ├── Katoomba Superior Public School
│           ├── Megalong Valley School
│           ├── Mount Victoria School
│           └── Sunday school             ← incorrect placement
```

**Root Cause:**

Each named school had TWO parent relationships in the CSV:
1. `parent=Schools` (plural - correct parent category)
2. `parent=School` (singular - incorrect, treating generic leaf as intermediate parent)

This violated the leaf-node tagging pattern where "School" (singular) should be a generic leaf node alongside named schools, NOT a parent of named schools.

**CSV Changes:**

Removed 5 incorrect `parent=School` relationships:

```csv
# Line 334 REMOVED:
Katoomba Public School,Katoomba Public School,hierarchy,parent=School

# Line 342 REMOVED:
Katoomba Superior Public School,Katoomba Superior Public School,hierarchy,parent=School

# Line 399 REMOVED:
Megalong Valley School,Megalong Valley School,hierarchy,parent=School

# Line 463 REMOVED:
Mount Victoria School,Mount Victoria School,hierarchy,parent=School

# Line 757 REMOVED:
Sunday school,Sunday school,hierarchy,parent=School
```

**Correct Structure After Fix:**

```
├── Educational buildings
│   └── Schools
│       ├── Katoomba Public School
│       ├── Katoomba Superior Public School
│       ├── Megalong Valley School
│       ├── Mount Victoria School
│       └── School                        ← generic leaf only
```

Sunday school correctly remains under Religious education (Agents facet):
```
Agents > Religious organizations > Religious education > Sunday school
```

**Rationale:**

1. **Follows leaf-node pattern:** "School" is a generic leaf for unspecified schools, not a category parent
2. **Eliminates duplication:** Named schools appear once under "Schools" parent
3. **Correct Sunday school placement:** Religious education activity, not secular educational building
4. **Matches other patterns:** Same structure as Hotels > Hotel, Retailers and Stores > Retailer or Store

**Files Modified:**
- data/tag_map_consolidated.csv (removed 5 lines)
- visualizations/hierarchy_trees/primary_built_environment.txt (regenerated clean)
- visualizations/hierarchy_trees/primary_agents.txt (regenerated, Sunday school correctly placed)

**Status:** Fix implemented and verified.

---

## Decision 2025-10-31: Religious Buildings Hierarchy Correction

**Date:** 2025-10-31
**Issue:** Duplicate church names in Religious buildings visualization
**Tags Affected:** Church (generic), Methodist Church, Roman Catholic Church, St Hilda's Church, Katoomba Congregational Church
**Decision:** Remove incorrect `parent=Religious buildings` relationships for churches

**Problem Identified:**

User reported duplication in Religious buildings hierarchy:
```
└── Religious buildings
    ├── Church                           ← generic, direct child
    ├── Churches
    │   ├── Church                       ← DUPLICATE generic
    │   ├── Congregational Church
    │   │   └── Katoomba Congregational Church
    │   ├── Methodist Church
    │   ├── Roman Catholic Church
    │   ├── St Hilda's Church
    │   └── Wesleyan Church
    ├── Katoomba Congregational Church   ← DUPLICATE
    ├── Methodist Church                 ← DUPLICATE
    ├── Religious building
    ├── Roman Catholic Church            ← DUPLICATE
    └── St Hilda's Church                ← DUPLICATE
```

**Root Cause:**

Same issue as Educational buildings - named churches and the generic "Church" had TWO parent relationships:
1. `parent=Churches` (correct - the plural parent category)
2. `parent=Religious buildings` (incorrect - bypassing the intermediate parent)

**CSV Changes:**

Removed 5 incorrect `parent=Religious buildings` relationships:

```csv
# Line 89 REMOVED:
Church,Church,hierarchy,parent=Religious buildings

# Line 322 REMOVED:
Katoomba Congregational Church,Katoomba Congregational Church,hierarchy,parent=Religious buildings

# Line 402 REMOVED:
Methodist Church,Methodist Church,hierarchy,parent=Religious buildings

# Line 692 REMOVED:
Roman Catholic Church,Roman Catholic Church,hierarchy,parent=Religious buildings

# Line 744 REMOVED:
St Hilda's Church,St Hilda's Church,hierarchy,parent=Religious buildings
```

**Correct Structure After Fix:**

```
└── Religious buildings
    ├── Churches
    │   ├── Church                       ← generic leaf only
    │   ├── Congregational Church
    │   │   └── Katoomba Congregational Church
    │   ├── Methodist Church
    │   ├── Roman Catholic Church
    │   ├── St Hilda's Church
    │   └── Wesleyan Church
    └── Religious building               ← generic for non-church buildings
```

**Rationale:**

1. **Follows leaf-node pattern:** Named churches are children of "Churches" parent, not direct children of "Religious buildings"
2. **Eliminates duplication:** Each church appears once in correct location
3. **Proper nesting:** "Churches" is the intermediate parent between "Religious buildings" and specific churches
4. **Consistent with other categories:** Matches pattern used for Schools, Hotels, etc.
5. **Preserves dual-nature polyhierarchy:** Churches also appear in Agents facet under Religious organizations

**Note on Dual-Nature:**

These churches are polyhierarchical entities appearing in both:
- Built Environment > Religious buildings > Churches (physical buildings)
- Agents > Religious organizations > Churches (organizational entities)

This fix only corrected the Built Environment facet structure - the polyhierarchical relationships across facets remain intact.

**Files Modified:**
- data/tag_map_consolidated.csv (removed 5 lines)
- visualizations/hierarchy_trees/primary_built_environment.txt (regenerated clean)

**Status:** Fix implemented and verified.

---

## Decision 2025-10-31: Remove Unused "Religious building" Generic

**Date:** 2025-10-31
**Issue:** Unnecessary generic "Religious building" with zero usage
**Tags Affected:** Religious building
**Decision:** Remove unused generic term

**Context:**

After fixing Religious buildings hierarchy duplication, user noted that "Religious building" generic is unnecessary since "Church" already serves as the generic leaf node.

**Evidence:**

Tag frequency check:
- `Church`: 34 items (actively used)
- `Religious building`: 0 items (never used)

**Rationale:**

1. **YAGNI principle:** "You Aren't Gonna Need It" - don't create structure until data shows need
2. **Church is sufficient:** All religious buildings in the collection are churches
3. **Zero usage:** No items tagged with "Religious building" in 304+ tagged sources
4. **Simplification:** Reduces unnecessary choice for cataloguers
5. **Future expansion:** If non-church religious buildings appear (e.g., synagogue, mosque), can add then

**CSV Change:**

```csv
# Line 978 REMOVED:
Religious building,Religious building,hierarchy,parent=Religious buildings (singular generic term)
```

**Structure After Removal:**

```
└── Religious buildings
    └── Churches
        ├── Church                    ← generic covers all unspecified churches
        ├── Congregational Church
        │   └── Katoomba Congregational Church
        ├── Methodist Church
        ├── Roman Catholic Church
        ├── St Hilda's Church
        └── Wesleyan Church
```

**Files Modified:**
- data/tag_map_consolidated.csv (removed 1 line)
- visualizations/hierarchy_trees/primary_built_environment.txt (regenerated)

**Status:** Implemented and verified.

---

## Decision 2025-10-31: Merge "Rape" into "Sexual violence"

**Date:** 2025-10-31
**Issue:** Two closely related tags with low usage
**Tags Affected:** Rape (5 items), Sexual violence (1 item)
**Decision:** Merge "Rape" → "Sexual violence", retain "Rape" as synonym

**Evidence:**

Tag frequency:
- `Rape`: 5 items (0.13%)
- `Sexual violence`: 1 item (0.03%)
- **Total**: 6 items

Both tags had identical parent relationships:
- Events > Criminal events
- Gender-related vulnerabilities - THEMATIC
- Violent crimes - THEMATIC

**Rationale:**

1. **Broader, more inclusive term:** "Sexual violence" is the umbrella category; rape is a specific type
2. **Low usage:** Only 6 items total across both tags
3. **Semantic relationship:** Rape is a subset of sexual violence
4. **Modern terminology:** "Sexual violence" is more commonly used in contemporary research and cataloguing
5. **Maintains searchability:** "Rape" retained as synonym for discoverability

**CSV Changes:**

```csv
# Lines 652-653 (replaced 3 hierarchy lines):
Sexual violence,Rape,merge,Specific term merged into broader category (rape is a type of sexual violence)
Sexual violence,Rape,synonym,Specific type of sexual violence - retained as synonym for search/discovery

# REMOVED:
Rape,Rape,hierarchy,parent=Criminal events
Rape,Rape,hierarchy,parent=Gender-related vulnerabilities - THEMATIC
Rape,Rape,hierarchy,parent=Violent crimes - THEMATIC
```

**Result:**

All 6 items will be tagged with "Sexual violence". Users searching for "Rape" will find these items via the synonym relationship.

**Structure:**
```
Events > Criminal events > Sexual violence
  (synonym: Rape)
```

**Files Modified:**
- data/tag_map_consolidated.csv (3 hierarchy lines removed, 2 lines added: merge + synonym)

**Status:** Implemented, pending regeneration of hierarchy trees.

---

## Decision 2025-10-31: Consolidate Accidents and Disasters Structure

**Date:** 2025-10-31
**Issue:** Duplicate accident/disaster categories in Events facet
**Tags Affected:** Disasters & accidents (parent), Port Kembla disaster, Accident, Fire, Disaster (new)
**Decision:** Merge "Disasters & accidents" → "Accidents", consolidate disaster references

**Problem Identified:**

Events facet had two separate top-level categories for similar concepts:
1. "Accidents" (parent with Agricultural accidents, Transport accidents)
2. "Disasters & accidents" (separate parent with Accident, Fire, Port Kembla disaster)

Additionally, "Port Kembla disaster" was a historical misnomer for "Mount Kembla Disaster" (1902 mining disaster).

**Evidence:**

Tag frequency:
- `Disasters & accidents`: 0 items (parent node only)
- `Port Kembla disaster`: Part of existing Mount Kembla Disaster synonym chain

**Rationale:**

1. **Eliminate redundancy:** "Disasters & accidents" duplicates "Accidents" functionality
2. **Simplify structure:** Single "Accidents" parent clearer for users
3. **Correct historical error:** Port Kembla disaster is actually Mount Kembla (different location)
4. **Add clarity:** Provide both "Accident" and "Disaster" as generic catch-all terms
5. **Consistent categorisation:** All accidents and disasters under single parent

**CSV Changes:**

```csv
# REMOVED (line 174):
Disasters & accidents,Disasters & accidents,hierarchy,parent=Events

# REMOVED (line 608):
Port Kembla disaster,Port Kembla disaster,hierarchy,parent=Disasters & accidents

# REMOVED (line 940):
Disasters & accident,Disasters & accident,hierarchy,parent=Disasters & accidents (singular generic term)

# UPDATED (line 13):
Accident,Accident,hierarchy,parent=Accidents  # was parent=Disasters & accidents

# UPDATED (line 230):
Fire,Fire,hierarchy,parent=Accidents  # was parent=Disasters & accidents

# ADDED (line 16):
Disaster,Disaster,hierarchy,parent=Accidents  # new generic catch-all
```

**Result:**

Consolidated structure:
```
Events > Accidents
├── Accident                    ← generic for unspecified accidents
├── Disaster                    ← generic for unspecified disasters
├── Fire                        ← can be accident or disaster
├── Agricultural accidents
├── Transport accidents
└── Mining accidents
    ├── Mining accident
    └── Mount Kembla Disaster   ← (synonyms: Port Kembla disaster, Mount Kembla Colliery Disaster)
```

**Note on Port Kembla vs Mount Kembla:**

The Mount Kembla Disaster (1902) is one of Australia's worst mining disasters. "Port Kembla disaster" is a historical misnomer - the disaster occurred at Mount Kembla, not Port Kembla (two different locations in the Illawarra region). The synonym chain already correctly identifies this:
- Preferred: "Mount Kembla Disaster"
- Synonyms: "Port Kembla disaster", "Mount Kembla Colliery Disaster"

**Files Modified:**
- data/tag_map_consolidated.csv (3 lines removed, 1 line added, 2 lines updated)

**Status:** Implemented, pending regeneration of hierarchy trees.

---

## Decision 2025-10-31: Remove Redundant "Mining events" Category

**Date:** 2025-10-31
**Issue:** Duplicate categorization in Events facet
**Tags Affected:** Mining events (parent), Mining accidents, Mine closure
**Decision:** Remove "Mining events" category - children already exist elsewhere

**Problem Identified:**

"Mining events" existed as a parent under Events with two children:
- Mine closure (already under Economic events)
- Mining accidents (already under Accidents)

Both children were duplicated, making the "Mining events" parent redundant.

**Evidence:**

All children have primary locations elsewhere:
- `Mine closure`: Events > Economic events > Mine closure
- `Mining accidents`: Events > Accidents > Mining accidents

**Rationale:**

1. **Eliminate duplication:** Both children already properly categorized
2. **Simplify structure:** No need for separate mining-specific events category
3. **Consistent with domain organization:** Mining activities/companies in other facets, events distributed by type

**CSV Changes:**

```csv
# REMOVED (line 1017):
Mining events,Mining events,hierarchy,parent=Events

# REMOVED (line 1018):
Mining accidents,Mining accidents,hierarchy,parent=Mining events

# REMOVED (line 1021):
Mine closure,Mine closure,hierarchy,parent=Mining events
```

**Result:**

Children remain in their primary locations:
- Economic events > Mine closure
- Accidents > Mining accidents > Mining accident, Mount Kembla Disaster

**Files Modified:**
- data/tag_map_consolidated.csv (3 lines removed)

**Status:** Implemented, pending regeneration of hierarchy trees.

---

### Decision 2025-11-01-H: Social Events Singular Standardisation

**Date:** 2025-11-01
**Type:** Naming Convention / Standardisation

**Issue:**
Under Social events, leaf tags showed inconsistent plural/singular forms:
- Plural: "Concerts" (29 items), "Dances" (26 items)
- Singular: "Ball" (4 items), "Flower show" (2 items)

**Analysis:**
This violated the consistent singular naming pattern used for leaf nodes throughout the taxonomy. Following the leaf-node tagging pattern documented in CLAUDE.md, leaf tags should use singular forms (e.g., "Hotel" not "Hotels", "School" not "Schools").

**Decision:**
Standardise all Social events leaf tags to singular:
- Concerts (29 items) → **Concert** (merge plural into singular)
- Dances (26 items) → **Dance** (merge plural into singular)
- Ball (4 items) → unchanged (already singular)
- Flower show (2 items) → unchanged (already singular)

**Rationale:**
1. **Internal consistency:** Matches pattern used across entire taxonomy (Hotels > Hotel, Schools > School)
2. **Leaf-node pattern compliance:** Singular generics and named entities are the standard
3. **Getty AAT alignment:** AAT uses singular forms for event types
4. **User clarity:** Consistent pattern makes tagging rules easier to follow

**Hierarchy Result:**
```
Social events
├── Ball
├── Concert (was Concerts)
├── Dance (was Dances)
├── Flower show
└── Social event
```

**Polyhierarchy Notes:**
Concert also appears under Cultural events (dual classification preserved after merge).

**Impact:**
- 29 items previously tagged "Concerts" → "Concert"
- 26 items previously tagged "Dances" → "Dance"
- Total affected: 55 items

**Files Modified:**
- data/tag_map_consolidated.csv (lines 114-117, 161-162)
  - Added merge entries for Concerts → Concert, Dances → Dance
  - Updated hierarchy relationships to use singular forms

**Status:** Implemented and verified in hierarchy visualizations.

---

## Sporting Events Reclassification: Cricket

**Date:** 2025-11-02

**Tags affected:**

- `Cricket` - Enhanced with thematic tag and Built Environment additions
- NEW: `Cricket grounds` (plural parent)
- NEW: `Cricket ground` (singular generic)
- NEW: `Recreation buildings` (Built Environment parent)
- NEW: `Sports facilities` (under Recreation buildings)
- NEW: `Women's sports` (thematic tag)
- NEW: `Youth sports` (thematic tag)
- NEW: `Childhood & adolescence` (thematic tag)
- `Girls' cricket` - Enhanced with Women's sports thematic

**Rationale:**

Following systematic review of sporting events (see reports/sporting_events_reclassification_review.md), Cricket emerged as a well-documented sporting activity requiring:

1. **Primary event hierarchy:** Cricket already correctly placed under Events > Sporting events
2. **Built Environment support:** Cricket grounds are significant cultural heritage sites in the Blue Mountains requiring dedicated Built Environment hierarchy
3. **Thematic enrichment:** Women's participation in cricket (Girls' cricket tag) warranted dedicated Women's sports thematic grouping
4. **Structural consistency:** Recreation buildings parent provides logical home for all sports facilities

**Evidence:**

Analysis revealed:
- Cricket clubs: Katoomba Cricket Club, Megalong Cricket Club (well-established organisations)
- Girls' cricket: Multiple references to women's cricket matches and participation
- Cricket grounds: Physical venues requiring Built Environment classification

**Hierarchy Result:**

```
Events > Sporting events
├── Cricket
│   ├── Cricket clubs (polyhierarchy with Sports clubs)
│   └── Girls' cricket (polyhierarchy with Women's sports - THEMATIC)

Built Environment
├── Recreation buildings (NEW)
│   └── Sports facilities (NEW)
│       ├── Cricket grounds (NEW plural parent)
│       │   └── Cricket ground (NEW singular generic)
│       └── Rifle ranges (added in Shooting review)

Sport & Recreation - THEMATIC
├── Cricket
├── Women's sports (NEW)
│   └── Girls' cricket
└── Youth sports (NEW)

Family & Domestic Life - THEMATIC
└── Childhood & adolescence (NEW)
```

**Impact:**

- Enhanced Cricket classification with thematic tag
- New Built Environment infrastructure for sports facilities
- Girls' cricket now discoverable via Women's sports thematic
- Foundation laid for other sports facilities (rifle ranges, etc.)

**Getty AAT Alignment:**

- Sports facilities: Aligns with AAT 300343232 "sports facilities"
- Recreation buildings: Follows AAT pattern for functional building classification
- Women's sports: Cultural heritage significance of women's participation in sports

**Files Modified:**

- data/tag_map_consolidated.csv
  - Lines 147-150: Enhanced Cricket with thematic tag
  - Lines 217-223: Added Recreation buildings > Sports facilities > Cricket grounds hierarchy
  - Lines 230: Added Childhood & adolescence thematic
  - Lines 256-258: Enhanced Girls' cricket with Women's sports thematic
  - Lines 738-739: Added Women's sports and Youth sports thematics

**Status:** Implemented 2025-11-02

---

## Sporting Events Reclassification: Shooting

**Date:** 2025-11-02

**Tags affected:**

- `Shooting` - MOVED from Events > Sporting events to Activities > Recreation activities
- NEW: `Shooting matches` (Events > Sporting events)
- NEW: `Shooting match` (singular generic)
- SYNONYM: `Shooting competition` (synonym for Shooting match)
- NEW: `Rifle ranges` (Built Environment > Sports facilities)
- NEW: `Rifle range` (singular generic)
- NEW: `Katoomba Shooting Fishing and Excursion Club` (specific club)
- NEW: `Western Rifle Association` (specific club)
- `Katoomba Rifle Reserves` - ADDED as club (dual-nature with existing place)
- NEW: `Mountain Rifle Reserves` (specific club)
- `Hunting` - ENHANCED with Recreation activities polyhierarchy
- NEW: `Recreational hunting` (distinct from economic hunting)

**Rationale:**

Context analysis of 13 items tagged "Shooting" revealed semantic complexity requiring nuanced classification:

1. **Activity vs Event distinction:** Shooting functions as both:
   - **Activity:** General recreational shooting practice, training, club activities (NOT team sport)
   - **Event:** Specific competitions, matches, tournaments

2. **NOT a team sport:** Unlike cricket/football, shooting encompasses:
   - Solo target practice
   - Group recreational shooting
   - Competitive team matches
   - Individual competition

   **Decision:** Place Shooting under Recreation activities (NOT under Team sports)

3. **Hunting distinction:** Item-by-item analysis revealed:
   - **Shooting sports:** Target practice, rifle clubs, competitions
   - **Recreational hunting:** Sport/recreational hunting of game (Item 11)
   - **Economic hunting:** Wild horse culling for commercial purposes (Items 8, 10)

4. **Specific clubs identified:**
   - Katoomba Shooting, Fishing, and Excursion Club (Item 2)
   - Western Rifle Association (Item 4)
   - Katoomba Rifle Reserves (Items 5, 7) - dual-nature: place AND club
   - Mountain Rifle Reserves (Item 12)

5. **Built Environment requirements:**
   - Rifle ranges are physical sporting facilities (Item 9)
   - Require Built Environment classification alongside Cricket grounds

**Evidence:**

**Item-by-item review findings:**

- **Item 1:** "Lithgow reserves good fine-weather shooters" → Activity (recreational shooting)
- **Item 2:** "Katoomba Shooting, Fishing, and Excursion Club will hold their half-yearly meeting" → Specific club organisation
- **Item 3:** "Improvement is shown in the shooting all round" → Activity (practice/training)
- **Item 4:** "Western Rifle Association" → Specific club organisation
- **Item 5:** "Katoomba Rifle Reserves were put through the musketry course" → Club + Activity (training)
- **Item 6:** "best shooters averaging 50... shoot the first stage of the ladies' £40 trophy" → Event (competition) + Women's sports thematic
- **Item 7:** "Katoomba Rifle Reserves musketry shooting this week" → Club + Event (organised shooting)
- **Item 8:** "destroy yelping mongrels... keep the canine 3s" → NOT shooting sports (dog control regulation) - REMOVE Shooting tag
- **Item 9:** "Preparations are being made at Blackheath for active work at the rifle range" → Built Environment (facility)
- **Item 10:** "Men were employed shooting [wild horses] for the skins" → Economic hunting (already appropriately tagged) - REMOVE Shooting tag
- **Item 11:** "dissecting every animal he shoots" → Recreational hunting (distinct from shooting sports)
- **Item 12:** "Mountain Rifle Reserves at the Association meeting at Sydney have won prizes" → Specific club + Event (competition)
- **Item 13:** "Triangular rifle match at Katoomba" → Event (shooting match) ✓ APPROVED

**Hierarchy Result:**

```
Activities
├── Recreation activities
│   ├── Shooting (MOVED from Events, NOT under Team sports)
│   └── Hunting (ENHANCED polyhierarchy)
│       └── Recreational hunting (NEW - distinct from shooting sports)
├── Economic activities
│   └── Hunting
│       └── Wild horse culling

Events > Sporting events
├── Cricket
└── Shooting matches (NEW)
    └── Shooting match (NEW singular generic, "Shooting competition" as synonym)

Built Environment > Recreation buildings > Sports facilities
├── Cricket grounds
│   └── Cricket ground
└── Rifle ranges (NEW)
    └── Rifle range (NEW singular generic)

Agents > Organisations > Sports clubs
├── Cricket clubs
├── Rifle clubs
│   ├── Rifle club (singular generic)
│   ├── Western Rifle Association (NEW)
│   ├── Katoomba Rifle Reserves (NEW - dual-nature with Place)
│   └── Mountain Rifle Reserves (NEW)
└── Katoomba Shooting Fishing and Excursion Club (NEW - multi-purpose club)

Places
└── Reserves
    └── Rifle reserves
        └── Katoomba Rifle Reserves (dual-nature with club)
```

**Dual-Nature Entity:**

`Katoomba Rifle Reserves` exhibits dual-nature (place AND organisation):
- **Place facet:** Physical reserve location for rifle practice
- **Agents facet:** Organised club/unit using the reserve

This polyhierarchical relationship preserves both aspects without disambiguation.

**Impact:**

- Shooting activity correctly classified under Recreation activities (NOT team sport)
- Shooting competitions properly distinguished as Events
- 4 specific rifle clubs/associations now individually tagged
- Rifle ranges added to Built Environment sports facilities
- Recreational hunting distinguished from shooting sports and economic hunting
- 2 items (8, 10) appropriately de-tagged from Shooting (dog control and economic horse culling)

**Getty AAT Alignment:**

- Shooting (activity): AAT 300239470 "shooting (attacking)"
- Rifle ranges: AAT 300007594 "shooting ranges"
- Hunting: AAT 300239666 "hunting (function)"
- Recreation activities: AAT 300054592 "recreational activities"

**Files Modified:**

- data/tag_map_consolidated.csv
  - Lines 222-223: Added Rifle ranges > Rifle range hierarchy
  - Lines 693-698: Added specific rifle clubs and association
  - Lines 724-729: Restructured Shooting (activity) and added Shooting competitions (events)
  - Lines 1046-1049: Enhanced Hunting with Recreation activities polyhierarchy and Recreational hunting

**Tagging Guidance:**

- Use `Shooting` (activity) for: practice, training, recreational shooting, club activities
- Use `Shooting match` for: organised competitions, tournaments, matches (synonym: "Shooting competition")
- Use `Recreational hunting` for: sport/recreational hunting of game animals
- Use `Hunting` (under Economic activities) for: commercial hunting operations
- Use `Wild horse culling` for: specific culling activities (economic or management)
- Use specific club names when identifiable: Katoomba Rifle Reserves, Western Rifle Association, etc.
- Use `Rifle range` (Built Environment) for: physical facilities/venues

**Status:** Implemented 2025-11-02

---

## Sporting Events Reclassification: Football

**Date:** 2025-11-02

**Tags affected:**

- `Football` - MOVED from Events > Sporting events to Activities > Recreation activities > Team sports
- NEW: `Team sports` (under Recreation activities)
- NEW: `Football matches` (Events > Sporting events)
- NEW: `Football match` (singular generic)
- NEW: `Hartley Vale Natives Football Club` (specific club)
- SYNONYM: `Hartley Vale Football Club` (shortened synonym for Hartley Vale Natives Football Club)
- NEW: `Lithgow Rovers` (specific club)
- NEW: `Nepean Football Club` (specific club)
- NEW: `Ovals` (Built Environment > Sports facilities)
- NEW: `Oval` (singular generic)
- NEW: `Eskbank Oval` (specific venue)
- `Cricket` - MOVED to Team sports (from Sporting events directly)

**Rationale:**

Context analysis of 6 items tagged "Football" revealed that Football is fundamentally different from Shooting:

1. **Team sport classification:** Unlike Shooting (which can be solo, group, or team), Football is inherently a team sport:
   - Always requires two teams
   - Organised club structure
   - Competitive matches between clubs

   **Decision:** Place Football under Activities > Recreation activities > Team sports

2. **Activity vs Event distinction:** Football functions as both:
   - **Activity:** The sport itself, team practice, club activities
   - **Event:** Specific matches and competitions

3. **Specific clubs identified:**
   - Katoomba Football Club (Item 2 - already existed)
   - Hartley Vale Natives Football Club (Items 3, 6 - "Hartley Vale Football Club" as synonym)
   - Lithgow Rovers (Item 4)
   - Nepean Football Club (Item 5)

4. **Built Environment requirements:**
   - Ovals are important sporting venues distinct from cricket grounds and rifle ranges
   - Eskbank Oval specifically mentioned (Item 4)

5. **Mining recreation thematic:**
   - Multiple items reference miners playing football (Items 1, 2, 4)
   - Links to existing "Recreation for miners" thematic tag

**Evidence:**

**Item-by-item review findings:**

- **Item 1:** "A FOOTBALL match came off here... between Katoomba miners and Hartley Vale miners" → Event (match) + Recreation for miners
- **Item 2:** "Katoomba Football Club and the Miner's Club" → Specific club + Event (match) + Recreation for miners
- **Item 3:** "Hartley Vale Natives Football Club brought a successful season to a close" → Specific club + Activity
- **Item 4:** "match was played... between Lithgow Rovers... on Eskbank oval" → Specific club (Lithgow Rovers) + Event (match) + Built Environment (Eskbank Oval)
- **Item 5:** "The Nepean Football Club has been formed at Penrith" → Specific club
- **Item 6:** "The Hartley Vale Football Club held a very successful social" → Specific club

**Hierarchy Result:**

```
Activities > Recreation activities
├── Team sports (NEW - distinct from solo/flexible sports)
│   ├── Cricket (MOVED from Sporting events)
│   └── Football (MOVED from Sporting events)
│       └── Football clubs (polyhierarchy with Sports clubs)
└── Shooting (NOT under Team sports - flexible participation)

Events > Sporting events
├── Cricket matches (existing)
├── Football matches (NEW)
│   └── Football match (NEW singular generic)
└── Shooting matches (existing)

Built Environment > Recreation buildings > Sports facilities
├── Cricket grounds
│   └── Cricket ground
├── Rifle ranges
│   └── Rifle range
└── Ovals (NEW)
    ├── Oval (NEW singular generic)
    └── Eskbank Oval (NEW specific venue)

Agents > Organisations > Sports clubs
├── Cricket clubs
├── Football clubs
│   ├── Football club (singular generic)
│   ├── Katoomba Football Club (existing)
│   ├── Hartley Vale Natives Football Club (NEW, "Hartley Vale Football Club" as synonym)
│   ├── Lithgow Rovers (NEW)
│   └── Nepean Football Club (NEW)
└── Rifle clubs
```

**Team Sports Distinction:**

This review establishes clear criteria for Team sports classification:

- **Team sports (inherently team-based):** Cricket, Football
  - Always require two teams
  - Cannot be played solo
  - Organised club structure essential

- **NOT team sports (flexible participation):** Shooting, individual athletics
  - Can be solo, group, or team
  - Club membership optional
  - Competition can be individual or team

**Impact:**

- Football correctly classified as team sport (activity)
- Football matches distinguished as events
- 3 new football clubs individually tagged (Hartley Vale Natives FC, Lithgow Rovers, Nepean FC)
- Hartley Vale Football Club established as synonym for full name
- Ovals added to Built Environment sports facilities
- Cricket also moved to Team sports for consistency
- Recreation for miners thematic connections preserved

**Getty AAT Alignment:**

- Team sports: Follows AAT pattern for collective sport classification
- Football: AAT 300222921 "football (action)"
- Ovals: AAT 300007601 "ovals (stadium spaces)"
- Sports facilities: AAT 300343232 "sports facilities"

**Files Modified:**

- data/tag_map_consolidated.csv
  - Line 147: Cricket moved to Team sports
  - Lines 224-226: Added Ovals > Oval > Eskbank Oval hierarchy
  - Lines 242-249: Restructured Football (activity) and added Football matches (events)
  - Lines 347-350: Added 3 specific football clubs (Hartley Vale Natives FC with synonym, Lithgow Rovers, Nepean FC)
  - Line 664: Added Team sports under Recreation activities

**Tagging Guidance:**

- Use `Football` (activity) for: the sport, team practice, club activities, general references
- Use `Football match` for: specific matches, competitions, tournaments
- Use `Cricket` (activity) for: the sport, team practice, club activities, general references
- Use specific club names when identifiable: Katoomba Football Club, Lithgow Rovers, etc.
- Use `Oval` (Built Environment) for: physical sporting venues
- Use `Recreation for miners` thematic when miners are participants

**Status:** Implemented 2025-11-02

---

## Sporting Events Reclassification: Billiards

**Date:** 2025-11-02

**Tags affected:**

- `Billiard` - MERGED into Billiards
- `Billiards` - MOVED from Events > Sporting events to Activities > Recreation activities
- NEW: `Billiard License` (under Legal concepts > Licenses)

**Rationale:**

Context analysis of 3 items tagged "Billiard" or "Billiards" revealed:

1. **Activity not event:** Billiards is an indoor game played continuously, not as discrete competitive events:
   - Item 1: Licensing context (Billiard License for hotel)
   - Item 2: "playing a game of billiards" (recreational activity)
   - Item 3: "billiard-room" (venue/facility reference)
   - No evidence of competitive matches or tournaments

2. **NOT a team sport:** Unlike Cricket/Football, billiards:
   - Can be played solo (practice)
   - Typically 1v1 (two individuals, not teams)
   - Rarely organised as team competitions
   - Similar participation flexibility to Shooting

   **Decision:** Place under Recreation activities (NOT Team sports)

3. **Singular/plural consolidation:**
   - Both "Billiard" and "Billiards" existed
   - Usage contexts show "billiards" (plural) as standard form
   - "billiard" appears only as modifier (e.g., "billiard-room", "Billiard License")

   **Decision:** Merge to "Billiards" (plural form as single preferred term)

4. **Licensing context:**
   - Item 1 references "Billiard License" for hotels
   - Distinct from Publican's License (alcohol sales)
   - Historical regulatory requirement for billiard tables in hotels

**Evidence:**

**Item-by-item review findings:**

- **Item 1:** "The Billiard License for the same hotel, as also transferred" → Licensing (regulatory)
- **Item 2:** "while playing a game of billiards... at the Carrington hotel" → Activity (recreational) + Recreation for miners
- **Item 3:** "from Jim Nelson's billiard-room to the Mines" → Venue reference + mentions Katoomba Rifle Reserves (club already correctly tagged)

**Hierarchy Result:**

```
Activities > Recreation activities
├── Team sports
│   ├── Cricket
│   └── Football
├── Billiards (NEW - NOT team sport, flexible participation)
└── Shooting (NOT team sport, flexible participation)

Legal concepts > Licenses
├── Billiard License (NEW)
└── Publican's License (existing)
```

**Recreation Activities Classification Criteria:**

This review clarifies criteria for Recreation activities structure:

**Team sports (inherently team-based):**
- Cricket, Football
- Always require two teams
- Cannot be played solo

**Flexible participation activities (NOT team sports):**
- Billiards, Shooting
- Can be solo, 1v1, or group
- Individual or paired participation typical

**Impact:**

- Billiards correctly classified under Recreation activities (NOT Team sport)
- "Billiard" merged into "Billiards" (single preferred term)
- Billiard License added to Legal concepts for historical licensing contexts
- Recreation for miners thematic connection maintained (Item 2)
- Katoomba Rifle Reserves club reference (Item 3) already correctly tagged as dual-nature entity

**Getty AAT Alignment:**

- Billiards: AAT 300222757 "billiards (game)"
- Recreation activities: AAT 300054592 "recreational activities"
- Licenses: AAT 300027834 "licenses (permissions)"

**Files Modified:**

- data/tag_map_consolidated.csv
  - Lines 59-61: Merged Billiard → Billiards, moved to Recreation activities with thematic tag
  - Line 952: Added Billiard License under Legal concepts > Licenses

**Tagging Guidance:**

- Use `Billiards` for: playing billiards, billiard rooms/facilities, general references to the game
- Use `Billiard License` for: licensing contexts, regulatory documents for billiard tables in hotels
- Use `Recreation for miners` thematic when miners are participants

**Status:** Implemented 2025-11-02

---

## Post-Taxonomy Application Notes: Zotero Item Tag Review

**Date:** 2025-11-02

**Context:** During sporting events review, identified items where club/organisation tags may have been misapplied as event tags.

**Example: Katoomba Football Club**

The taxonomy correctly places "Katoomba Football Club" under:
- Football (activity)
- Football clubs (organisation)

However, specific Zotero items require review to ensure appropriate tagging:

**Items requiring tag review:**
1. **Mountain Mixtures (1893-06-02):** "Dr. Prangley president of Katoomba football club"
   - Context: Club administration/organisation
   - Recommendation: Club tag appropriate, no event tag needed

2. **Football (1904-04-22):** "football match... between Katoomba Football Club and the Miner's Club"
   - Context: Specific match mentioned
   - Recommendation: Keep club tag + add "Football match" event tag

3. **Mountain Mixtures (1893-06-30):** "Katoomba Football Club is evidently one of those little arrangements"
   - Context: General club commentary
   - Recommendation: Club tag appropriate, no event tag needed

**Tagging Principle:**

- **Organisation/club references:** Use club tag only (e.g., "Katoomba Football Club")
- **Specific events/matches:** Use event tag (e.g., "Football match") + club tags for participants
- **Activity references:** Use activity tag (e.g., "Football")

**Status:** Noted for future Zotero tag application review (post-taxonomy implementation)

---

## Sporting Events Comprehensive Review and Rationalisation

**Date:** 2025-11-02

**Context:** Systematic review of all sporting-related tags to determine whether they represent specific events (Events facet), ongoing activities (Activities facet), or organisations (Agents facet). Generated detailed context analysis report using script 31_analyse_sporting_events.py with item-by-item recommendations.

### Key Decisions

#### 1. Events vs Activities Distinction

**Principle established:** Distinguish between:
- **Events facet:** Discrete occurrences (matches, competitions, meetings)
- **Activities facet:** The sport/activity itself (cricket, football, tennis)
- **Agents facet:** Clubs and organisations

**Event naming convention:** Use specific event type names (e.g., "Cricket match", "Football match") rather than generic sport names in Events facet.

#### 2. Gender-Neutral Events + Thematic Tags

**Decision:** Do NOT create gender-specific event terms (e.g., "Girls' cricket match").

**Rationale:**
- Getty AAT uses gender-neutral base terms
- Gender treated as ATTRIBUTE (modifier/thematic tag), not separate hierarchy
- Avoids term proliferation (Girls' cricket match, Boys' cricket match, Women's cricket match, etc.)
- Better searchability and aggregation

**Implementation:**
- REMOVED: `Girls' cricket` as separate event term
- USE: `Cricket match` (gender-neutral) + thematic tags `Women's sports` and/or `Youth sports`
- Historical article titles preserve original phrasing; controlled vocabulary remains neutral

**Thematic tags for demographic context:**
- `Women's sports` (Sport & Recreation + Women & Gender themes)
- `Youth sports` (Sport & Recreation + Childhood & adolescence themes)

#### 3. Club Name Consolidation

**Katoomba Lawn Tennis Club:**
- **Evidence:** 1893 formed as "Katoomba Tennis Club"; 1903 referenced as "Katoomba Lawn Tennis Club"
- **Decision:** Use "Katoomba Lawn Tennis Club" as preferred term (later, more specific form)
- **Synonym:** "Katoomba Tennis Club" → "Katoomba Lawn Tennis Club"

#### 4. Tag Misapplication Identified

**"At Katoomba (1893-11-10)" - Cricket Match Item:**

**Current tags (INCORRECT):**
- `Katoomba Cricket Club` ❌ (not mentioned)
- `Megalong Cricket Club` ❌ (not mentioned)
- `Cricket clubs` ❌ (not mentioned)

**Full text analysis revealed:**
- Single cricket reference: "promised cricket match - town v. mines - was damped down"
- Match cancelled due to rain
- Teams named ("town" vs "mines") but NO club organisations mentioned
- Primary article content: Wesleyan Flower Show and Bazaar at Odd Fellows' Hall

**Corrected tags:**
- REMOVE: Katoomba Cricket Club, Megalong Cricket Club, Cricket clubs, generic Cricket/Sports tags
- ADD: Cricket match (planned event, though cancelled)
- ADD: Flower show, Bazaar (Events > Social events - NEW event types)
- ADD: Odd Fellows' Hall (Built Environment)
- ADD: Wesleyans (religious organisation)

**Lesson:** Club tags were applied based on keyword "cricket" without verifying clubs actually mentioned. Demonstrates importance of full-text context analysis.

#### 5. New Event Types Added

**Social Events:**
- `Flower show` (Events > Social events)
- `Bazaar` (Events > Social events)

**Sporting Events:**
- `Cricket matches` (parent) with `Cricket match` (singular generic)
- `Rugby matches` (parent) with `Rugby match` (singular generic)
- `Coursing` (hare coursing competitions/meetings)

**Note:** Football matches/Football match already existed in taxonomy.

#### 6. New Organisations Added

**Rugby clubs:**
- `Rugby clubs` (parent under Sports clubs)
- `Rugby club` (singular generic)
- `Penrith Rugby Club` (specific club)

**Coursing clubs:**
- `Coursing clubs` (parent under Sports clubs)
- `Coursing club` (singular generic)
- `Wallerawang Coursing Club` (specific club)

**Background:** Coursing is competitive canine sport where greyhounds chase hares by sight (not scent). Popular "gentlemanly sport" in 19th century, now illegal in many countries. Clubs held meetings/competitions requiring live hares.

#### 7. Activities Reclassification

**Moved from Events > Sporting events to Activities > Recreation activities:**

- **Athletics** → Activities > Recreation activities (general sport/fitness activity)
- **Tennis** → Activities > Recreation activities (not team sport - individual or doubles)

**Moved from Events > Sporting events to Activities > Recreation activities > Team sports:**

- **Rugby** → Team sports (alongside Cricket and Football)

**Already correctly placed:**
- Cricket → Team sports ✓
- Football → Team sports ✓
- Billiards → Recreation activities ✓
- Shooting → Recreation activities ✓

**Team Sports Criteria:**
- Inherently team-based (always require two teams)
- Cannot be played solo
- Examples: Cricket, Football, Rugby

**Flexible Participation Activities (NOT team sports):**
- Can be solo, 1v1, or group
- Individual or paired participation typical
- Examples: Billiards, Shooting, Tennis, Athletics

### Files Modified

**data/tag_map_consolidated.csv:**
- Removed: Girls' cricket (lines 266-268)
- Moved: Athletics from Sporting events to Recreation activities
- Moved: Tennis from Sporting events to Recreation activities
- Moved: Rugby from Sporting events to Team sports
- Updated: Katoomba Tennis Club → Katoomba Lawn Tennis Club with synonym
- Added: Cricket matches, Cricket match (lines 1101-1103)
- Added: Rugby matches, Rugby match (lines 1104-1106)
- Added: Coursing (lines 1107-1108)
- Added: Rugby clubs structure with Penrith Rugby Club (lines 1109-1111)
- Added: Coursing clubs structure with Wallerawang Coursing Club (lines 1112-1114)
- Added: Flower show, Bazaar (lines 1115-1116)

**visualizations/hierarchy_trees/:**
- Regenerated all 30 hierarchy trees (7 primary facets + 22 thematic groupings + overview)

**scripts/:**
- Created: 31_analyse_sporting_events.py (context analysis script)
- Created: check_cricket_item.py (full text verification script)

**reports/:**
- Generated: sporting_events_reclassification_review.md (item-by-item analysis)

### Tagging Guidance

**For sporting content:**

1. **Specific matches/competitions:** Use event tag (Cricket match, Football match, Rugby match, Shooting match, Coursing)
2. **General sport/activity references:** Use activity tag (Cricket, Football, Rugby, Tennis, Shooting, Billiards, Athletics)
3. **Clubs/organisations:** Use agent tag (Katoomba Cricket Club, Penrith Rugby Club, etc.)
4. **Gender/demographic context:** Add thematic tags (Women's sports, Youth sports, Recreation for miners)

**Common scenarios:**

- "Football match between Katoomba Football Club and Miner's Club" → Football match (event) + club tags (agents)
- "Girls playing cricket" → Cricket (activity) + Women's sports + Youth sports (thematics)
- "Coursing club meeting cancelled due to lack of hares" → Coursing (event) + club tag (agent)
- "Tennis club fencing being erected" → Club tag only (organisational infrastructure, not event/activity)

### Getty AAT Alignment

- Events as discrete occurrences vs activities as ongoing practices aligns with AAT facet structure
- Gender-neutral terminology matches AAT approach (gender as attribute, not embedded in term)
- Sport/activity terms: AAT 300054592 "recreational activities"
- Individual sport references align with AAT specific game terms

### Outstanding Issues

**For future Zotero tag application:**

Many items currently tagged with club names may actually be about matches/events rather than club organisations. Full-text context analysis recommended before applying tags, particularly:

- Items tagged "Katoomba Football Club" - may need Football match event tag
- Items tagged cricket club names - verify club actually mentioned vs match between teams
- Tennis club tags - distinguish club administration content from matches/facilities

**Status:** Implemented 2025-11-02

---
