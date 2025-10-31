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
