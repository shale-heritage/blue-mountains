# Getty AAT-Aligned Taxonomy Proposals for Horses Review

**Date:** 2025-10-31
**Purpose:** Propose Getty AAT-aligned taxonomy terms for user approval before implementation

---

## Research Summary

**Getty AAT Verified:**
- **Animal husbandry (discipline)** - Getty AAT ID: 300254388
  - Broader term: Agriculture (discipline)
  - Scope: "Science and discipline of breeding, raising, feeding, and tending animals, especially but not exclusively domestic farm animals"

**Getty AAT Principles Applied:**
- Activities Facet: For processes, functions, and disciplinary activities
- Events Facet: For occurrences, incidents, and temporal happenings
- Agents Facet: For people, organisations, animals, and biological entities
- Associated Concepts Facet: For abstract ideas and conditions

---

## PROPOSAL 1: Animal Husbandry and Breeding Activities

### Context
Item #2: Megalong Matters (26 Aug 1892) - Wild horse hunting and pony breeding

### User Request
```
Activities > Economic activities > Animal husbandry > Horse breeding (Thesaurus: Pony breeding)
Activities > Economic activities > Hunting > Wild horse hunting (Thesaurus: Wild pony hunting)
Agents > Animals > Wildlife > Wild horses
Agents > People > Occupations > Farming and animal husbandry > Horse breeder > Mr Hardie Clydesdale
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Activities (primary facet)
└── Economic activities
    ├── Agriculture
    │   └── Animal husbandry
    │       ├── Animal breeding
    │       │   ├── Horse breeding
    │       │   └── Pony breeding (alternate term for Horse breeding)
    │       └── Livestock management
    └── Hunting
        ├── Wild horse culling (preferred over "hunting" for commercial skin harvesting)
        └── Wild horse hunting (alternate term)

Agents (primary facet)
├── Animals
│   ├── Domestic animals
│   │   └── Horses (livestock/working animals)
│   └── Wild animals
│       └── Wild horses (feral horses)
└── People
    └── Occupations
        ├── Agriculture workers
        │   ├── Animal breeders
        │   │   ├── Horse breeder
        │   │   └── Livestock breeder
        │   └── Farmers
        └── Named individuals
            └── Mr Hardie Clydesdale (polyhierarchical: Horse breeder, People)
```

**RATIONALE:**
- Getty AAT places animal husbandry under Agriculture, not standalone under Economic activities
- "Culling" is more accurate than "hunting" for commercial skin harvesting (industrial-scale activity)
- "Feral horses" is the zoologically correct term for wild horses (descended from domestic stock)
- Individual names (Mr Hardie Clydesdale) should be polyhierarchical under both occupation and named people

**RECOMMENDATION:**
✓ **APPROVE** this structure with the following hierarchy:
- `Activities > Economic activities > Agriculture > Animal husbandry > Animal breeding > Horse breeding`
- `Activities > Economic activities > Hunting > Wild horse culling`
- `Agents > Animals > Domestic animals > Horses`
- `Agents > Animals > Wild animals > Wild horses`
- `Agents > People > Occupations > Agriculture workers > Animal breeders > Horse breeder`
- `Agents > People > Named individuals > Mr Hardie Clydesdale`

---

## PROPOSAL 2: Transportation Accidents

### Context
Items #5, 11, 12, 14, 15, 16, 17, 18: Various horse and cart accidents

### User Request
```
Disasters and Accidents > Accident > Transportation accident > Horse accident
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Events (primary facet)
└── Accidents (unintended harmful events)
    ├── Transportation accidents
    │   ├── Horse-drawn vehicle accidents
    │   │   ├── Buggy accidents
    │   │   ├── Cart accidents
    │   │   └── Sulky accidents
    │   ├── Horseback riding accidents
    │   └── Runaway horse incidents
    └── Work accidents (polyhierarchical for occupational accidents)
```

**ALTERNATIVE STRUCTURE (more specific):**

```
Events
└── Accidents
    └── Transport accidents
        ├── Animal-powered transport accidents
        │   ├── Horse accidents (generic term)
        │   ├── Horse-drawn vehicle accidents (carts, buggies, sulkies)
        │   └── Horseback riding accidents (rider falls, thrown from horse)
        └── Runaway animal incidents
```

**RATIONALE:**
- Getty AAT uses "Events" facet for occurrences/incidents, not "Disasters and Accidents" as top level
- Distinguish between:
  - **Horse-drawn vehicle accidents** (horses pulling carts/buggies that crash)
  - **Horseback riding accidents** (riders falling from horses)
  - **Runaway horse incidents** (horses bolting uncontrolled)
- "Accidents" is preferred Getty term over "mishaps" or "disasters"

**RECOMMENDATION:**
✓ **APPROVE** this structure:
- `Events > Accidents > Transport accidents > Animal-powered transport accidents > Horse accidents`
- With narrower terms:
  - `Horse-drawn vehicle accidents` (for Items #5, 12, 15, 16)
  - `Horseback riding accidents` (for Items #14, 17, 18)
  - `Runaway horse incidents` (for Items #11, 12)

**SPECIFIC ITEM TAGGING:**
- Item #5: Horse-drawn vehicle accidents | Runaway horse incidents (buggy bolted)
- Item #11: Runaway horse incidents (barber's horse bolting)
- Item #12: Horse-drawn vehicle accidents | Runaway horse incidents (sulky bolted)
- Item #14: Horseback riding accidents (rider pulled from saddle)
- Item #15: Horse-drawn vehicle accidents (cart overturned)
- Item #16: Horse-drawn vehicle accidents (cart over embankment)
- Item #17: Horseback riding accidents (rider fell 80 feet)
- Item #18: Horseback riding accidents (horsemen encountering fallen tree)

---

## PROPOSAL 3: Animal Straying / Property Offences

### Context
Item #7: Town Talk (30 Oct 1903) - Cattle and horse straying court cases

### User Request
```
Event > Criminal event > Animal straying (thesaurus: Cattle straying; Horse straying)
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Events (primary facet)
└── Legal proceedings
    └── Court cases
        ├── Property offences
        │   ├── Animal trespass
        │   │   ├── Cattle straying
        │   │   └── Horse straying
        │   └── Stock trespass
        └── Regulatory offences
```

**ALTERNATIVE (if treating as criminal matter):**

```
Associated Concepts (primary facet)
└── Legal concepts
    └── Offences
        ├── Property offences
        │   ├── Animal trespass
        │   └── Stock trespass
        └── Regulatory offences
```

**RATIONALE:**
- "Animal straying" is typically a **civil/regulatory offence**, not a criminal event
- Getty AAT distinguishes between:
  - **Events** (court proceedings, trials)
  - **Associated Concepts** (legal concepts, types of offences)
- "Trespass" is the legal term for animals straying onto another's property
- "Stock trespass" is the Australian legal term for livestock straying

**RECOMMENDATION:**
✓ **APPROVE** hybrid approach:
- Primary: `Events > Legal proceedings > Court cases > Property offences > Stock trespass`
- Thesaurus:
  - `Animal trespass` (alternate term)
  - `Cattle straying` (use-for term)
  - `Horse straying` (use-for term)

This accurately reflects that the **event** is a court case about stock trespass, while "straying" is the colloquial description.

---

## PROPOSAL 4: Horse Racing (Sporting Events)

### Context
Item #9: Mountain Mixtures (20 Nov 1891) - Horse race at Medlow

### User Request
```
Events > Sporting event > Horse race
(not recreational activity as the riding isn't being done for recreation, but instead it's a spectator sport event watching the horse race)
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Events (primary facet)
└── Cultural events
    └── Sporting events
        ├── Equestrian events
        │   ├── Horse races
        │   │   ├── Flat racing
        │   │   ├── Harness racing
        │   │   └── Steeplechase
        │   ├── Show jumping
        │   └── Dressage
        ├── Athletic competitions
        └── Recreational sports

Activities (polyhierarchical link)
└── Recreation activities
    └── Sports
        └── Equestrian sports
            └── Horse racing (the activity of participating)
```

**RATIONALE:**
- Getty AAT distinguishes between:
  - **Events > Sporting events** (the organised occasion/competition)
  - **Activities > Sports** (the practice/discipline itself)
- "Horse race" (singular) for the specific event
- "Horse racing" (gerund) for the sport/activity
- Polyhierarchical relationship captures both aspects

**RECOMMENDATION:**
✓ **APPROVE** this structure:
- Primary: `Events > Cultural events > Sporting events > Equestrian events > Horse races`
- Polyhierarchical: `Activities > Recreation activities > Sports > Equestrian sports > Horse racing`

For Item #9, tag as: `Events > Sporting events > Horse races` (the event that occurred)

---

## PROPOSAL 5: Goring Accidents (Animal Attacks)

### Context
Item #10: Mountain Mixtures (29 Apr 1892) - Cow gored horse

### User Request
```
Agents > Animals > Cattle
Disasters and Accidents > Accident > Farming and animal husbandry accident > Goring
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Agents (primary facet)
└── Animals
    └── Domestic animals
        ├── Cattle (already exists)
        └── Horses (already exists)

Events (primary facet)
└── Accidents
    ├── Agricultural accidents
    │   ├── Livestock accidents
    │   │   ├── Animal attacks
    │   │   │   ├── Goring
    │   │   │   ├── Kicking
    │   │   │   └── Trampling
    │   │   └── Stock handling injuries
    │   └── Farm machinery accidents
    └── Animal-related injuries
```

**RATIONALE:**
- "Goring" is a specific type of injury caused by horned animals
- Occurs in both agricultural and non-agricultural contexts
- Getty AAT structure: Events > Accidents > [context] > [specific type]
- "Animal attacks" encompasses goring, kicking, biting, etc.

**RECOMMENDATION:**
✓ **APPROVE** this structure:
- `Agents > Animals > Domestic animals > Cattle` (already exists, confirm tag applied)
- `Events > Accidents > Agricultural accidents > Livestock accidents > Animal attacks > Goring`

Alternative narrower path if non-agricultural:
- `Events > Accidents > Animal-related injuries > Animal attacks > Goring`

---

## PROPOSAL 6: Postal Services Activities

### Context
Items #3, #19: Postman's horse for mail delivery

### User Request
```
Activities > Communication activities > Postal services
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Activities (primary facet)
└── Communication activities
    ├── Postal services
    │   ├── Mail collection
    │   ├── Mail delivery
    │   ├── Mail sorting
    │   └── Mail transport
    ├── Telecommunications
    └── Publishing

Agents (polyhierarchical)
└── People
    └── Occupations
        └── Communication workers
            ├── Postal workers
            │   ├── Postman (historical term)
            │   ├── Postmaster
            │   └── Postal carrier (modern term)
            └── Mail carriers
```

**RATIONALE:**
- Getty AAT has "Postal services" under Communication activities
- Can be made more specific: "Mail delivery" as narrower term
- Person conducting the activity: "Postman" or "Postal worker"

**RECOMMENDATION:**
✓ **APPROVE** this structure:
- `Activities > Communication activities > Postal services` (generic term)
- Optionally more specific: `Activities > Communication activities > Postal services > Mail delivery`
- For person: `Agents > People > Occupations > Communication workers > Postal workers > Postman`

---

## PROPOSAL 7: Law Enforcement Activities

### Context
Item #13: Katoomba Police Court (13 Dec 1895) - Constable's horse

### User Request
```
Activities > Policing
Agents > People > Occupations > Law enforcement > Constable
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Activities (primary facet)
└── Societal activities (or Functions)
    └── Law enforcement
        ├── Policing
        │   ├── Patrol
        │   ├── Investigation
        │   ├── Arrest
        │   └── Traffic control
        ├── Judicial activities
        └── Corrections

Agents (primary facet)
└── People
    └── Occupations
        └── Law enforcement personnel
            ├── Police officers
            │   ├── Constable (historical UK/Commonwealth rank)
            │   ├── Sergeant
            │   └── Inspector
            ├── Sheriffs
            └── Magistrates (judicial)
```

**RATIONALE:**
- Getty AAT treats law enforcement as societal function or activity
- "Policing" is the general activity; "Patrol," "Investigation" are specific functions
- "Constable" is a specific rank within police hierarchy (UK/Commonwealth usage)
- In 1890s Australia, "Constable" was the standard police officer rank

**RECOMMENDATION:**
✓ **APPROVE** this structure:
- `Activities > Societal activities > Law enforcement > Policing`
- `Agents > People > Occupations > Law enforcement personnel > Police officers > Constable`

**NOTE:** The item is about a court case (legal proceeding), not the policing activity itself. Consider also tagging:
- `Events > Legal proceedings > Court cases`

---

## PROPOSAL 8: Recreational Horseback Riding

### Context
Items #8, #11: Horsewoman riding, riding habit

### User Request
```
Add recreational horseback riding
```

### Getty AAT-Aligned Proposal

**PROPOSED TAXONOMY:**

```
Activities (primary facet)
└── Recreation activities
    └── Sports
        ├── Equestrian sports
        │   ├── Horseback riding (recreational)
        │   ├── Horse racing (competitive)
        │   └── Show jumping
        └── Outdoor recreation
            └── Trail riding
```

**RATIONALE:**
- Distinguish between:
  - **Recreational horseback riding** (leisure riding for pleasure)
  - **Horse racing** (competitive sport)
  - **Horseborne transportation** (practical transport)
- "Horsewoman" suggests social/recreational context (Item #8: "17st horsewoman rode up Long Swamp")
- "Riding habit" is clothing for recreational/social riding (Item #11)

**RECOMMENDATION:**
✓ **APPROVE** this addition:
- `Activities > Recreation activities > Sports > Equestrian sports > Horseback riding`
- Apply to Items #8 and #11 where context suggests leisure/social riding

---

## SUMMARY OF RECOMMENDATIONS

| Proposal | Concept | Recommended Taxonomy | Status |
|----------|---------|---------------------|--------|
| 1 | Animal husbandry & breeding | `Activities > Economic activities > Agriculture > Animal husbandry > Animal breeding > Horse breeding` | **APPROVE?** |
| 1 | Wild horse culling | `Activities > Economic activities > Hunting > Wild horse culling` | **APPROVE?** |
| 1 | Wild horses (animals) | `Agents > Animals > Wild animals > Wild horses` | **APPROVE?** |
| 1 | Horse breeder (person) | `Agents > People > Occupations > Agriculture workers > Animal breeders > Horse breeder` | **APPROVE?** |
| 2 | Horse accidents | `Events > Accidents > Transport accidents > Animal-powered transport accidents` with narrower terms | **APPROVE?** |
| 3 | Animal straying | `Events > Legal proceedings > Court cases > Property offences > Stock trespass` | **APPROVE?** |
| 4 | Horse racing | `Events > Cultural events > Sporting events > Equestrian events > Horse races` | **APPROVE?** |
| 5 | Goring accidents | `Events > Accidents > Agricultural accidents > Livestock accidents > Animal attacks > Goring` | **APPROVE?** |
| 6 | Postal services | `Activities > Communication activities > Postal services` | **APPROVE?** |
| 7 | Policing | `Activities > Societal activities > Law enforcement > Policing` | **APPROVE?** |
| 7 | Constable | `Agents > People > Occupations > Law enforcement personnel > Police officers > Constable` | **APPROVE?** |
| 8 | Recreational riding | `Activities > Recreation activities > Sports > Equestrian sports > Horseback riding` | **APPROVE?** |

---

## NEXT STEPS

Please review each proposal and indicate:
1. **APPROVE** - Accept as proposed
2. **CHANGE** - Modify (specify changes)
3. **REJECT** - Do not implement

Once approved, I will:
1. Update `tag_map_consolidated.csv` with new hierarchy entries
2. Revise `tag_application_mapping.csv` with correct tags for all 19 items
3. Document decisions in `planning/consolidation-decisions.md`
4. Regenerate hierarchy trees to show new structure

---

**Prepared by:** Claude Code
**Date:** 2025-10-31
**Awaiting approval to proceed with implementation**
