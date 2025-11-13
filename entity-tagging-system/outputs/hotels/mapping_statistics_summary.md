# Hotel Item-Level Mapping Statistics

**Date:** 2025-11-13
**Phase:** Phase 2 - Mapping statistics and analysis
**Source:** Item-by-item mapping proposal

---

## Overall Statistics

**Total Items:** 43
**Total Unique Entities:** 14

**Classification Distribution:**
- Building only: 18 items (41.9%)
- Business only: 17 items (39.5%)
- Both (polyhierarchical): 8 items (18.6%)

**Confidence Distribution:**
- High confidence: 40 items (93.0%)
- Medium confidence: 3 items (7.0%)
- Low confidence: 0 items (0.0%)

---

## Entity-Level Statistics

| Entity | Total Mentions | Building | Business | Both | Dominant Pattern |
|--------|----------------|----------|----------|------|------------------|
| Belgravia Hotel | 2 | 1 | 1 | 0 | Mixed |
| Carrington Hotel | 4 | 2 | 1 | 1 | Mixed |
| Centennial Hotel | 5 | 1 | 2 | 2 | Business-dominant |
| Family hotel | 3 | 0 | 2 | 1 | Business-dominant |
| Grand Hotel | 1 | 1 | 0 | 0 | Building-only |
| Imperial Hotel | 3 | 2 | 1 | 0 | Building-dominant |
| Katoomba Family Hotel | 1 | 0 | 1 | 0 | Business-only |
| Katoomba Hotel | 3 | 3 | 0 | 0 | Building-only |
| Megalong Hotel | 8 | 2 | 3 | 3 | Business-dominant |
| Montrose House | 4 | 4 | 0 | 0 | Building-only |
| Mount Victoria Hotel | 2 | 0 | 2 | 0 | Business-only |
| Railway Hotel | 2 | 2 | 0 | 0 | Building-only |
| Wentworth Falls Hotel | 2 | 0 | 2 | 0 | Business-only |
| family hotel | 3 | 0 | 2 | 1 | Business-dominant |

---

## Tag Application Summary

This shows how many times each tag will be applied to Zotero items:

### Building Tags

| Tag | Applications |
|-----|--------------|
| Belgravia Hotel (building) | 1 |
| Carrington Hotel (building) | 3 |
| Centennial Hotel (building) | 3 |
| Grand Hotel (building) | 1 |
| Imperial Hotel (building) | 2 |
| Katoomba Family Hotel (building) | 1 |
| Katoomba Hotel (building) | 3 |
| Megalong Hotel (building) | 5 |
| Montrose House (building) | 4 |
| Railway Hotel (building) | 2 |
| family hotel (building) | 1 |

### Business Tags

| Tag | Applications |
|-----|--------------|
| Belgravia Hotel (business) | 1 |
| Carrington Hotel (business) | 2 |
| Centennial Hotel (business) | 4 |
| Imperial Hotel (business) | 1 |
| Katoomba Family Hotel (business) | 4 |
| Megalong Hotel (business) | 6 |
| Mount Victoria Hotel (business) | 2 |
| Wentworth Falls Hotel (business) | 2 |
| family hotel (business) | 3 |

### Total Tag Applications

- Total building tag applications: 11
- Total business tag applications: 9
- Total distinct tags to be applied: 20
- Total tag application operations: 51

---

## Entity Classification Patterns

Grouped by classification behaviour:

**Building-only entities (4):**
- Grand Hotel (1 mentions)
- Katoomba Hotel (3 mentions)
- Montrose House (4 mentions)
- Railway Hotel (2 mentions)

**Business-only entities (3):**
- Katoomba Family Hotel (1 mentions)
- Mount Victoria Hotel (2 mentions)
- Wentworth Falls Hotel (2 mentions)

**Mixed/polyhierarchical entities (5):**
- Belgravia Hotel (2 mentions: 1 building, 1 business, 0 both)
- Carrington Hotel (4 mentions: 2 building, 1 business, 1 both)
- Centennial Hotel (5 mentions: 1 building, 2 business, 2 both)
- Imperial Hotel (3 mentions: 2 building, 1 business, 0 both)
- Megalong Hotel (8 mentions: 2 building, 3 business, 3 both)

---

## Capitalization Variant Handling

Analysis of how capitalization affects tag mapping:

**'Family hotel' (capitalized):** 3 mentions
- Maps to: Katoomba Family Hotel (building) and/or (business)
- Classifications: Counter({'business': 2, 'both': 1})

**'family hotel' (lowercase):** 3 mentions
- Maps to: family hotel (building) and/or (business) [generic]
- Classifications: Counter({'business': 2, 'both': 1})

**Rationale:** Capitalization signals proper noun (specific establishment) vs common noun (generic term) following UK/Australian journalistic conventions.

---

## Comparison with Existing Taxonomy

**Entities in dataset:** 14

**Entities requiring business tags:** 10
- Belgravia Hotel: Belgravia Hotel (business)
- Carrington Hotel: Carrington Hotel (business)
- Centennial Hotel: Centennial Hotel (business)
- Family hotel: Katoomba Family Hotel (business)
- Imperial Hotel: Imperial Hotel (business)
- Katoomba Family Hotel: Katoomba Family Hotel (business)
- Megalong Hotel: Megalong Hotel (business)
- Mount Victoria Hotel: Mount Victoria Hotel (business)
- Wentworth Falls Hotel: Wentworth Falls Hotel (business)
- family hotel: family hotel (business)

**Status:** All business tags have been created in taxonomy restructuring (Phase 1). No taxonomy gaps identified.

---

## Validation Readiness

**High confidence items:** 40/43 (93.0%)
**Medium confidence items:** 3/43 (7.0%)

**Review priority:**
1. **High priority (medium confidence):** 3 items
   - Carrington Hotel illustration (minimal context)
   - Grand Hotel future reference (not yet established)
   - Wentworth Falls Hotel advertisement (brief mention)
2. **Low priority (high confidence):** 40 items with clear indicators

**Recommendation:** All mappings ready for user review. Focus manual verification on 3 medium-confidence items.

---

## Next Steps

1. ✓ **Phase 1 Complete:** Taxonomy restructuring (business tags created)
2. ✓ **Phase 2 Complete:** Item-by-item mapping proposal generated
3. **Phase 3 Pending:** Identify taxonomy gaps (if any)
4. **Phase 4 Required:** User review and approval of mappings
5. **Phases 5-8 Waiting:** Apply mappings after user approval

---

**Generated:** 2025-11-13
**Status:** Ready for Phase 4 user review
