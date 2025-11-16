# Public Houses: Disambiguation Implementation Summary

**Date:** 2025-11-16
**Status:** ✅ COMPLETE - Ready for Zotero application

---

## Summary

Completed (building)/(business) disambiguation for Public houses, finalising the partial structure that existed. This strategic decision aligns Public houses with the established pattern for hotels, schools of arts, churches, and boarding houses.

---

## Classification Results

**Total items analysed:** 2 unique items (4 mentions due to duplicate tags)

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 0 | 0% |
| Business only | 0 | 0% |
| Both | 2 | 100% |

**Pattern:** Dual-nature dominant - strongest pattern among all entity types (100% both)

**Human review:** No corrections needed - both classifications confirmed

---

## Taxonomy Changes

### Removed (8 obsolete entries)

**Unqualified polyhierarchical structure:**

```csv
Public house,Public house,hierarchy,parent=Public houses
Public houses,Public houses,hierarchy,parent=Accommodation and hospitality venues
Public houses,Public houses,hierarchy,parent=Alcohol-related venues - THEMATIC
public houses,public houses,hierarchy,parent=Alcohol-related venues - THEMATIC
```

**Obsolete synonyms:**

```csv
Pub,public house,synonym,Colloquial term for public house
pub,public house,synonym,Short form (UK/Australian) - lowercase variant
Pubs,public houses,synonym,Colloquial short form - prefer full form public houses
```

### Added (13 new entries)

**Built Environment facet (completed):**

```csv
public houses (buildings),public houses (buildings),hierarchy,parent=accommodation buildings
# Note: public house (building) already existed under public houses (buildings)
```

**Agents facet (NEW):**

```csv
public houses (businesses),public houses (businesses),hierarchy,parent=hospitality businesses
public house (business),public house (business),hierarchy,parent=public houses (businesses)
```

**Thematic cross-references:**

```csv
public houses (buildings),public houses (buildings),hierarchy,parent=Accommodation and hospitality venues
public houses (businesses),public houses (businesses),hierarchy,parent=Alcohol-related venues - THEMATIC
```

**Synonyms to both aspects:**

```csv
Pub,public house (building),synonym,Colloquial term - maps to building aspect
Pub,public house (business),synonym,Colloquial term - maps to business aspect
pub,public house (building),synonym,Short form (UK/Australian) - maps to building aspect
pub,public house (business),synonym,Short form (UK/Australian) - maps to business aspect
Pubs,public houses (buildings),synonym,Colloquial plural - maps to building aspect
Pubs,public houses (businesses),synonym,Colloquial plural - maps to business aspect
pubs,public houses (buildings),synonym,Colloquial plural (lowercase) - maps to building aspect
pubs,public houses (businesses),synonym,Colloquial plural (lowercase) - maps to business aspect
```

**Net change:** +5 entries (8 removed, 13 added)
**Final taxonomy size:** 2,232 entries

---

## New Taxonomy Structure

```text
Built Environment > Accommodation buildings > public houses (buildings)
└── public house (building)

Agents > Businesses > Hospitality businesses > public houses (businesses)
└── public house (business)
```

**Thematic cross-references maintained:**

- Built Environment aspect also appears under "Accommodation and hospitality venues"
- Business aspect also appears under "Alcohol-related venues - THEMATIC"

---

## Specific Establishments Identified

**None at this stage** - Both items use generic "pub"/"public house" terminology without naming specific establishments.

**Note:** As additional items are found and tagged, specific named establishments can be added under both parent categories following the leaf-node pattern.

---

## Items Requiring Zotero Retagging

**Total:** 2 items (with duplicate tag cleanup)

**Breakdown:**

- Replace with both (building + business): 2 items
- Remove duplicate tags: 2 items (consolidate "Pub"/"pub" duplicates)

**Application CSV:** `entity-tagging-system/outputs/public-houses/item_tag_application.csv`

---

## Strategic Decision: Complete Disambiguation

**Rationale:**

1. **Empirical evidence confirms strong dual nature**
   - 100% of mentions reference both building and business aspects
   - Strongest dual-nature pattern among all entity types studied
   - Both spatial indicators (location, infrastructure) and agency indicators (operations, licensing)

2. **Partial structure already existed**
   - Building facet (`public house (building)`) was already implemented
   - Incomplete without corresponding business facet
   - Inconsistent with project pattern

3. **Getty AAT alignment**
   - Public houses are dual-faceted (built works + commercial entities)
   - Strong regulatory/licensing framework distinguishes premises from operations

4. **Consistency with project pattern**
   - Matches hotels (building/business)
   - Matches schools of arts (building/organisation)
   - Matches churches (building/organisation)
   - Matches boarding houses (building/business)

5. **Clarity improvement**
   - Previous polyhierarchy created ambiguity
   - Cannot distinguish: drinking *at* the premises vs business *operated by* the publican
   - Disambiguation makes facet assignment explicit

6. **Future-proofing**
   - As more items are found and tagged, structure is ready
   - Specific named establishments can be added as discovered
   - Consistent pattern for all hospitality venues

---

## Key Findings

### Pattern Comparison

| Entity Type | Building % | Business/Org % | Both % | Dominant Pattern |
|-------------|------------|----------------|--------|------------------|
| **Public Houses** | **0%** | **0%** | **100%** | **Dual-nature dominant** |
| Churches | 29% | 29% | 42% | Dual-nature dominant |
| Schools of Arts | 11.1% | 55.6% | 33.3% | Organisation-dominant |
| Hotels | 43% | 25% | 32% | Building-dominant |
| Educational Schools | 17.2% | 58.6% | 24.1% | Organisation-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | Business-dominant |

**Observation:** Public houses show the strongest dual-nature pattern, exceeding even churches. This reflects the inherent inseparability of licensed premises (physical location with infrastructure like bars) and commercial hospitality operations (service provision, regulatory compliance).

### Building Evidence

**Spatial indicators found:**

- Locational references ("The nearest pub")
- Movement to/arrival ("roll off our horses")
- Physical infrastructure ("behind the bar")
- Comparison with other built structures ("preferable to...shanties")

### Business Evidence

**Agency indicators found:**

- Licensing and regulation ("application for a public house," "Licensing Act")
- Police oversight ("watched by the police")
- Employment/staffing ("amiable old lady who presided behind the bar")
- Service provision (serving drinks, customer service)
- Commercial operations (hospitality transactions)
- Community approval processes (residents debating establishment)

---

## Data Quality Notes

### Tag Duplication

Both items have duplicate capitalisation variant tags:

- "Pub" and "pub" on same items
- Synonyms now correctly map both variants to qualified terms
- Retagging will consolidate to single preferred forms

### Sample Size

- Only 2 unique items currently tagged
- Limited statistical sample, but pattern is clear and consistent
- Aligns with domain knowledge (pubs inherently dual-nature)
- Structure ready for additional items as they're discovered and tagged

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/public-houses/public-houses_classification_results.md`
- **Item mentions:** `data/entity_classification/public-houses_mentions.json`
- **Classification prompt:** `data/entity_classification/public-houses_classification_prompt.txt`
- **Tag application CSV:** `entity-tagging-system/outputs/public-houses/item_tag_application.csv`
- **Taxonomy implementation script:** `scripts/45_implement_public_houses_taxonomy.py` (executed)
- **Backup:** `data/tag_map_consolidated.csv.backup-20251116-072808`

---

## Next Steps

1. **Apply Zotero tags** - Use item_tag_application.csv to retag 2 items
2. **Document decision** - Add to `planning/consolidation-decisions.md`
3. **Continue tagging enrichment** - As more pub references found, add specific establishments
4. **Consider medium-priority entities** - Banks, Stores/Retailers identified in audit

---

## Getty AAT Alignment

**Public houses (buildings):** Licensed drinking establishments, bars, accommodation buildings (Built Environment facet)

**Public houses (businesses):** Hospitality businesses, drinking establishments, licensed operations (Agents facet)

✅ Dual-faceted structure aligns with Getty AAT patterns for commercial hospitality venues

---

**Implementation completed:** 2025-11-16
**Taxonomy size:** 2,232 entries (+5 from Public houses implementation)
**Items awaiting Zotero application:** 2 (public houses) + 106 (from previous work) = 108 total
