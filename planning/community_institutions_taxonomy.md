# Community Institutions Taxonomy - REVISED

## Key Principle: Organisation vs Building

**Critical distinction:**
- **Organisation tags** = the society/club/group (e.g., "Druid's Lodge" organisation)
- **Building/venue tags** = the physical hall (e.g., "Odd Fellows' Hall" building)

---

## Proposed Hierarchy

```
Community institutions (NEW PARENT)
├── Friendly societies & lodges (organisations)
│   ├── Lodges (generic parent - KEEP EXISTING)
│   │   ├── Druid's Lodge
│   │   └── Mountaineer Lodge
│   ├── Odd Fellows (organisation) - NEW if needed
│   └── Freemasons (organisation) - NEW if needed
│
├── Halls & meeting places (buildings/venues)
│   ├── School of Arts (MOVED from parent=School)
│   ├── Katoomba School of Arts (MOVED from parent=School of Arts)
│   ├── Odd Fellows' Hall (building owned by Odd Fellows lodge)
│   ├── I.O.O.F. Hall (same as above - IOOF = Odd Fellows)
│   ├── Masonic Hall (building owned by Freemasons lodge)
│   ├── Clarke's Hall
│   ├── Waudby's Hall
│   └── Mount Victoria Hall
│
├── Civic organisations
│   ├── Progress committees (generic)
│   ├── Katoomba Progress Association
│   ├── Leura Progress Association
│   ├── Wentworth Falls Progress Association
│   ├── Mount Victoria Progress Committee
│   └── Megalong Progress Committee
│
└── Cultural & recreational societies
    ├── Horticulture society
    ├── Katoomba Amateur Dramatic Club
    └── Chess and Draughts Club
```

---

## Definitions (for consistent application)

### Friendly Societies & Lodges
**What:** Mutual aid organisations providing insurance, healthcare, social support
**Examples:** Odd Fellows (IOOF), Freemasons, Druids, Foresters
**Tag rule:**
- Organisation name (e.g., "Druid's Lodge") goes under "Lodges"
- Physical building (e.g., "Odd Fellows' Hall") goes under "Halls & meeting places"

### Halls & Meeting Places
**What:** Physical buildings/venues used for community gatherings, meetings, entertainment
**Includes:**
- Purpose-built community halls
- Lodge halls (buildings owned by friendly societies)
- Schools of Arts (library/reading room/cultural centres)
**Tag rule:** If tag includes "Hall" or refers to a building/venue, it goes here

### Civic Organisations
**What:** Advocacy and improvement groups for local government/community development
**Examples:** Progress associations/committees
**Tag rule:** Groups focused on municipal improvement, infrastructure advocacy

### Cultural & Recreational Societies
**What:** Social clubs for hobbies, culture, arts (non-sports)
**Includes:** Drama clubs, horticultural societies, chess clubs
**Tag rule:** Non-athletic recreational pursuits, cultural activities
**Excludes:** Sports clubs (Cricket, Football, Tennis, Athletic clubs)

---

## Questions to Check Current Tags

**Question 1:** Do we have any tags for lodge ORGANISATIONS (not halls)?
- Check: "Odd Fellows", "Freemasons", "Druids" (without "Lodge" or "Hall")
- Current: Only "Druid's Lodge" and "Mountaineer Lodge" found

**Question 2:** Is "I.O.O.F. Hall" a duplicate of "Odd Fellows' Hall"?
- IOOF = Independent Order of Odd Fellows
- Likely the same building, different naming conventions
- **Decision needed:** MERGE these two tags?

**Question 3:** Should "Lodges" remain as intermediate category?
```
Option A (RECOMMENDED):
Community institutions → Friendly societies & lodges → Lodges → [specific lodges]

Option B (SIMPLER):
Community institutions → Lodges → [specific lodges]
```

---

## Implementation Notes

### Tags to Move
1. **From "School" to "Community institutions → Halls & meeting places":**
   - School of Arts
   - Katoomba School of Arts

2. **From "School" to "Religion":**
   - Sunday school

3. **New parent relationships to create:**
   - All halls → Community institutions → Halls & meeting places
   - All progress orgs → Community institutions → Civic organisations
   - Cultural societies → Community institutions → Cultural & recreational societies
   - Lodges → Community institutions → Friendly societies & lodges (OR directly under Community institutions)

---

## Recommendation

**Simplified structure (easier to implement):**

```
Community institutions
├── Lodges
│   ├── Druid's Lodge
│   └── Mountaineer Lodge
├── Halls
│   ├── School of Arts (MOVED)
│   ├── Katoomba School of Arts (MOVED)
│   ├── Odd Fellows' Hall
│   ├── I.O.O.F. Hall (consider merging with above?)
│   ├── Masonic Hall
│   ├── Clarke's Hall
│   ├── Waudby's Hall
│   └── Mount Victoria Hall
├── Civic organisations
│   └── [all progress associations]
└── Cultural societies
    └── [drama, horticulture, chess clubs]
```

**Clearer semantics, easier tagging rules, less nesting complexity.**

Do you prefer this simplified version?

