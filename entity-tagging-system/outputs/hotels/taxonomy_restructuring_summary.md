# Hotel Taxonomy Restructuring - Summary

**Date:** 2025-11-13
**Status:** COMPLETE ✓

---

## What Was Accomplished

### 1. Removed Extraneous 'hotels' Primary Facet ✓

**Problem:** The `hotels` tag appeared as a standalone primary facet containing only family hotels, creating a phantom hierarchy visible in visualizations.

**Solution:** Deleted lines 498-499 from `data/tag_map_consolidated.csv`:
```csv
hotels,hotels,hierarchy,parent=Alcohol-related venues - THEMATIC,
hotels,hotels,hierarchy,parent=Domestic accommodation - THEMATIC (residential aspect),
```

**Result:** Family hotels now correctly appear only under `Built Environment > accommodation buildings > hotels (buildings) > family hotels`

---

### 2. Created Parallel Hotels (Businesses) Structure ✓

**Problem:** No hotel business tags existed despite 69% of hotels in collection showing business agency contexts.

**Solution:** Added complete business hierarchy mirroring building structure:

```
hotels (businesses)
├── hotel (business) [singular generic]
├── Belgravia Hotel (business)
├── Carrington Hotel (business)
├── Centennial Hotel (business)
├── Imperial Hotel (business)
├── Megalong Hotel (business)
├── Mount Victoria Hotel (business)
└── Wentworth Falls Hotel (business)
```

**Total added:** 8 new business tags (1 generic + 7 specific named hotels)

---

### 3. Created Family Hotels (Businesses) Sub-Category ✓

**Problem:** Family hotels are a distinct business model requiring separate classification.

**Solution:** Added sub-category mirroring building structure:

```
family hotels (businesses)
├── family hotel (business) [singular generic]
├── Delaney's Family Hotel (business)
├── Fryer's Family Hotel (business)
└── Katoomba Family Hotel (business)
```

**Total added:** 5 new tags (1 sub-category + 1 generic + 3 specific)

---

### 4. Updated Unqualified Variants to Map to BOTH Building and Business ✓

**Problem:** Unqualified hotel names (e.g., "Carrington Hotel") mapped only to building variants, preventing polyhierarchical tagging.

**Solution:** Added business synonym mappings for 8 hotels:

1. Belgravia Hotel → Belgravia Hotel (business)
2. Carrington Hotel → Carrington Hotel (business)
3. Centennial Hotel → Centennial Hotel (business)
4. Imperial Hotel → Imperial Hotel (business)
5. Katoomba Family Hotel → Katoomba Family Hotel (business)
6. Megalong Hotel → Megalong Hotel (business)
7. Mount Victoria Hotel → Mount Victoria Hotel (business)
8. Wentworth Falls Hotel → Wentworth Falls Hotel (business)

**Result:** Each unqualified name now maps to BOTH (building) and (business) variants, enabling accurate polyhierarchical tagging.

**Hotels excluded:** Katoomba Hotel, Railway Hotel, Grand Hotel (Sydney), Montrose House remain building-only (no business contexts found in NLU analysis).

---

### 5. Updated Family Hotel Capitalization Mapping Rules ✓

**Problem:** Capitalized "Family Hotel" and lowercase "family hotel" both mapped to "Katoomba Family Hotel" without distinguishing generic vs specific usage.

**Solution:** Implemented capitalization-sensitive mapping rules:

**Lowercase "family hotel" (generic):**
```csv
family hotel → family hotel (building)
family hotel → family hotel (business)
```

**Capitalized "Family Hotel" (specific - Katoomba establishment):**
```csv
Family Hotel → Katoomba Family Hotel (building)
Family Hotel → Katoomba Family Hotel (business)
```

**Rationale:** Follows UK/Australian journalistic conventions where capitalization signals proper nouns (specific entities) vs common nouns (generic terms).

---

## Summary Statistics

**Total changes to taxonomy:**
- **Deleted:** 2 lines (extraneous hotels facet)
- **Added:** 22 new lines (13 business hierarchy + 4 sub-category + 8 synonym mappings)
- **Modified:** 10 lines (unqualified mappings + Family Hotel rules)
- **Total impact:** 34 line changes

**New taggable entities:**
- 9 hotel (business) tags for specific named hotels
- 2 generic singular terms: `hotel (business)`, `family hotel (business)`
- 1 organizational sub-category: `family hotels (businesses)`

**Hotels with polyhierarchical classification (9):**
1. Megalong Hotel - building + business
2. Katoomba Family Hotel - building + business
3. Centennial Hotel - building + business
4. Carrington Hotel - building + business
5. Imperial Hotel - building + business
6. Wentworth Falls Hotel - building + business
7. Mount Victoria Hotel - building + business
8. Belgravia Hotel - building + business
9. Family hotel (generic) - building + business

**Hotels remaining building-only (4):**
1. Katoomba Hotel
2. Railway Hotel
3. Grand Hotel (Sydney)
4. Montrose House

---

## Evidence Base

**Source:** Entity Tagging System NLU analysis (Claude Sonnet 4.5)
**Dataset:** 43 hotel mentions from Zotero library
**Confidence:** 93% high confidence classifications

**Key findings:**
- 46.5% building-only contexts
- 34.9% business-only contexts
- 18.6% both contexts

**Genre patterns identified:**
- Licensing contexts → 100% business (7 mentions)
- Property transactions → 100% business (4 mentions)
- Advertisements → 100% both (2 mentions)
- Court testimony with proprietor → 100% both (4 mentions)
- Event venues → 100% building (5 mentions)
- Spatial landmarks → 100% building (8 mentions)

---

## Validation Results

**Taxonomy integrity:** ✓ PASS
- All parent references valid
- All mapping tags exist in taxonomy
- No case-insensitive duplicates
- No orphaned tags

**Scripts executed:**
1. `scripts/validate_taxonomy.py` - Passed all critical tests
2. `scripts/40_check_orphaned_tags.py` - No orphaned tags found
3. `scripts/22_generate_poly_hierarchy.py` - Regenerated relationships (572 new, 100 duplicates removed)

---

## Documentation

**Master taxonomy:**
- `data/tag_map_consolidated.csv` - All changes applied and validated

**Consolidation decisions:**
- `planning/consolidation-decisions.md` - Full rationale and evidence documented

**Analysis reports:**
- `entity-tagging-system/outputs/hotels/existing_taxonomy_inventory.md` - Pre-change state
- `entity-tagging-system/outputs/hotels/claude_classifications.md` - Full NLU analysis
- `entity-tagging-system/outputs/hotels/comparison_report.md` - Regex vs NLU comparison
- `entity-tagging-system/outputs/hotels/statistics_summary.md` - Genre pattern analysis

---

## Next Steps for Item-Level Tagging

**Now ready for Phase 2-8:**
1. Phase 2: Create item-by-item tag mapping proposal
2. Phase 3: Identify any remaining taxonomy gaps
3. Phase 4: User review and approval checkpoint
4. Phase 5: Update taxonomy with any approved additions
5. Phase 6: Prepare item-level mapping application
6. Phase 7: Apply mappings to `data/tag_application_mapping.csv`
7. Phase 8: Final validation and documentation

**Status:** Ready to proceed when you approve the taxonomy structure.

---

## Applicability to Other Entity Types

This restructuring establishes precedent for:
- **Churches:** Unqualified variants should map to both building and organisation
- **Schools of Arts:** Review unqualified variant mappings
- **Halls:** Analyse if organizational variants needed
- **Lodges:** Review mapping consistency with hotel precedent

---

**Completed:** 2025-11-13
**All tasks completed successfully** ✓
