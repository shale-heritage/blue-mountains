# Schools of Arts: Disambiguation Implementation Summary

**Date:** 2025-11-15
**Status:** ✅ COMPLETE - Ready for Zotero application

---

## Summary

Implemented (building)/(organisation) disambiguation for Schools of Arts, replacing polyhierarchical structure. This strategic decision aligns Schools of Arts with the established pattern for educational schools, churches, hotels, and boarding houses.

---

## Classification Results

**Total items analysed:** 18

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 2 | 11.1% |
| Organisation only | 10 | 55.6% |
| Both | 6 | 33.3% |

**Pattern:** Organisation-dominant (similar to educational schools at 58.6%)

**Human review correction:** 1 item (Mention 18) corrected from "organisation" to "both" after identifying elliptical spatial reference ("at the room")

---

## Taxonomy Changes

### Removed (13 obsolete entries)

**Unqualified polyhierarchical structure:**
```csv
Schools of Arts,Schools of Arts,hierarchy,parent=Cultural societies
Schools of Arts,Schools of Arts,hierarchy,parent=Halls
schools of arts,schools of arts,hierarchy,parent=cultural societies
schools of arts,schools of arts,hierarchy,parent=halls
School of Arts,School of Arts,hierarchy,parent=Schools of Arts
school of arts,school of arts,hierarchy,parent=schools of arts
Katoomba School of Arts,Katoomba School of Arts,hierarchy,parent=schools of arts
Katoomba School of Arts,Katoomba School of Arts,hierarchy,parent=Schools of Arts
```

**Obsolete synonyms:**
```csv
School of Arts,school of arts,synonym
school of art,school of arts,synonym
schools of art,schools of arts,synonym
```

### Added (14 new entries)

**Built Environment facet:**
```csv
schools of arts (buildings),schools of arts (buildings),hierarchy,parent=halls
school of arts (building),school of arts (building),hierarchy,parent=schools of arts (buildings)
Katoomba School of Arts (building),Katoomba School of Arts (building),hierarchy,parent=schools of arts (buildings)
Mines School of Arts (building),Mines School of Arts (building),hierarchy,parent=schools of arts (buildings)
```

**Agents facet:**
```csv
schools of arts (organisations),schools of arts (organisations),hierarchy,parent=cultural societies
school of arts (organisation),school of arts (organisation),hierarchy,parent=schools of arts (organisations)
Katoomba School of Arts (organisation),Katoomba School of Arts (organisation),hierarchy,parent=schools of arts (organisations)
Mines School of Arts (organisation),Mines School of Arts (organisation),hierarchy,parent=schools of arts (organisations)
```

**Synonyms to both aspects:**
```csv
School of Arts,school of arts (building),synonym
School of Arts,school of arts (organisation),synonym
school of art,school of arts (building),synonym
school of art,school of arts (organisation),synonym
schools of art,schools of arts (buildings),synonym
schools of art,schools of arts (organisations),synonym
```

**Net change:** +1 entry (13 removed, 14 added)
**Final taxonomy size:** 2,227 entries

---

## New Taxonomy Structure

```text
Built Environment > Community buildings > Halls
└── schools of arts (buildings)
    ├── school of arts (building)
    ├── Katoomba School of Arts (building)
    └── Mines School of Arts (building)

Agents > Organisations > Cultural societies
└── schools of arts (organisations)
    ├── school of arts (organisation)
    ├── Katoomba School of Arts (organisation)
    └── Mines School of Arts (organisation)
```

---

## Specific Establishments Identified

1. **Katoomba School of Arts** (9 items)
   - Building: 1 mention
   - Organisation: 5 mentions
   - Both: 3 mentions

2. **Mines School of Arts** (2 items)
   - Organisation: 2 mentions
   - Note: Mentioned in items with generic "School of Arts" tags

3. **Generic "School of Arts"** (7 items)
   - Building: 1 mention
   - Organisation: 4 mentions
   - Both: 2 mentions

---

## Items Requiring Zotero Retagging

**Total:** 18 items

**Breakdown:**
- Replace with building only: 2 items
- Replace with organisation only: 10 items
- Replace with both: 6 items
- Add specific establishment tags: 2 items (Mines School of Arts)

**Application CSV:** `entity-tagging-system/outputs/schools-of-arts/item_tag_application.csv`

---

## Strategic Decision: Polyhierarchy → Disambiguation

**Rationale:**

1. **Empirical evidence confirms dual nature**
   - 44.4% of mentions reference building aspects (2 building-only + 6 both)
   - 88.9% of mentions reference organisational aspects (10 organisation-only + 6 both)
   - Clear context-dependent usage

2. **Dedicated buildings confirmed**
   - Explicit mention of "new School of Arts building"
   - Permanent reading room infrastructure
   - Fixed recreational facilities (billiard table)

3. **Getty AAT alignment**
   - Schools of Arts dual-faceted like churches
   - Requires disambiguation for clarity

4. **Consistency with project pattern**
   - Matches educational schools (building/organisation)
   - Matches churches (building/organisation)
   - Matches hotels (building/business)
   - Matches boarding houses (building/business)

5. **Clarity improvement**
   - Current polyhierarchy creates ambiguity
   - Cannot distinguish: events *at* the building vs events *organised by* the society
   - Disambiguation makes facet assignment explicit

---

## Key Findings

### Pattern Comparison

| Entity Type | Building % | Business/Org % | Both % | Dominant Pattern |
|-------------|------------|----------------|--------|------------------|
| **Schools of Arts** | **11.1%** | **55.6%** | **33.3%** | **Organisation-dominant** |
| Educational Schools | 17.2% | 58.6% | 24.1% | Organisation-dominant |
| Churches | 29% | 29% | 42% | Dual-nature dominant |
| Hotels | 43% | 25% | 32% | Building-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | Business-dominant |

**Observation:** Schools of Arts pattern closest to educational schools - both are organisation-dominant cultural/educational institutions.

### Building Evidence

**Spatial indicators found:**
- Physical library space ("fossicking about the books at")
- New building construction ("new School of Arts building")
- Reading room facilities (tables, periodicals)
- Fixed infrastructure (billiard table)
- Elliptical spatial references ("at the room")

### Organisation Evidence

**Agency indicators found:**
- Committee meetings and governance
- Membership and subscriptions (21 shillings fee mentioned)
- Financial operations (debt management, revenue)
- Event organisation (flower shows, tournaments)
- Staffing and employment (librarian)
- Institutional management

---

## Methodology Improvement

**Human review identified issue:** Elliptical spatial reference missed ("at the room")

**Skill enhancement implemented:** Added explicit guidance for elliptical/implied spatial references to entity-classifier skill

**Impact:** Should reduce similar misses in future classifications while maintaining conservative approach to avoid false positives

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/schools-of-arts/schools-of-arts_classification_results.md`
- **Item mentions:** `data/entity_classification/schools_mentions.json`
- **Classification prompt:** `data/entity_classification/schools_classification_prompt.txt`
- **Tag application CSV:** `entity-tagging-system/outputs/schools-of-arts/item_tag_application.csv`
- **Taxonomy implementation script:** `scripts/44_implement_schools_of_arts_taxonomy.py` (executed)
- **Backup:** `data/tag_map_consolidated.csv.backup-20251115-090402`

---

## Next Steps

1. **Apply Zotero tags** - Use item_tag_application.csv to retag 18 items
2. **Document decision** - Add to planning/consolidation-decisions.md
3. **Update TODO.md** - Remove Schools of Arts from pending strategic decisions (lines 42-140)
4. **Consider next entity type** - Public Houses (pubs) identified as high-priority dual-nature entity

---

## Getty AAT Alignment

**Schools of Arts (buildings):** Community halls, reading rooms, libraries (Built Environment facet)

**Schools of Arts (organisations):** Cultural societies, membership organisations, adult education institutions (Agents facet)

✅ Dual-faceted structure aligns with Getty AAT patterns

---

**Implementation completed:** 2025-11-15
**Taxonomy size:** 2,227 entries (+1 from Schools of Arts implementation)
