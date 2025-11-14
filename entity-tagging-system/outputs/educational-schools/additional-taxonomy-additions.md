# Additional Taxonomy Additions from Educational Schools Review

**Date:** 2025-11-14
**Source:** Manual review of Megalong Valley School and Mount Victoria School items
**Status:** Ready for implementation

---

## Overview

During manual review of 7 educational school items, two additional taxonomy needs were identified:

1. **School teachers** hierarchy under Agents > People > Occupations
2. **University of Sydney (institution)** - Already exists in taxonomy ✓

---

## 1. School Teachers Hierarchy

### Current State

The taxonomy has an `Occupations` hierarchy under `People` with various professional categories:
- Clergy
- Hospitality workers
- Law enforcement
- Medical professionals
- Miners
- etc.

**Missing:** Educational occupations category and school teachers

### Proposed Addition

Add educational occupations hierarchy following the leaf-node tagging pattern:

```text
Agents > People > Occupations
└── Educational occupations (NEW - intermediate parent)
    ├── School teachers (NEW - intermediate parent)
        ├── School teacher (NEW - singular generic leaf)
        └── [Specific named teachers] (NEW - specific leaves as identified)
```

### CSV Entries to Add

```csv
Educational occupations,Educational occupations,hierarchy,parent=Occupations
educational occupations,educational occupations,hierarchy,parent=occupations
School teachers,School teachers,hierarchy,parent=Educational occupations
school teachers,school teachers,hierarchy,parent=educational occupations
School teacher,School teacher,hierarchy,parent=School teachers
school teacher,school teacher,hierarchy,parent=school teachers
```

### Rationale

**Why this structure:**
1. **Educational occupations** as intermediate parent allows for future expansion (e.g., university lecturers, headmasters, inspectors)
2. **School teachers** (plural) as organisational parent following standard pattern
3. **School teacher** (singular) as generic leaf for unspecified teachers
4. Matches pattern used for other occupational categories (e.g., hospitality workers > hoteliers)

**Evidence from sources:**
- Item: Megalong Matters (1892-09-09) mentions "school teacher" in context of local news
- Pattern shows teachers referenced both generically ("the school teacher") and by name ("Mr W Chapman")

### Getty AAT Alignment

- Teachers: http://vocab.getty.edu/page/aat/300025529
- School teachers: http://vocab.getty.edu/page/aat/300266227 (educational institution personnel)
- Follows AAT pattern of professional occupations under People/Agents facet

---

## 2. Specific Person: Mr W Chapman

### Context

Item: Megalong Matters (1892-09-09)
- Mentions "school teacher" in local news context
- Based on user note, the teacher is identified as "Mr W Chapman"

### Proposed Addition

Once school teachers hierarchy is implemented, add:

```csv
Mr W Chapman,Mr W Chapman,hierarchy,parent=School teachers
```

**Note:** This follows the pattern of adding specific named individuals under their occupational category.

**Alternative consideration:** Depending on how people are typically structured in your taxonomy, this might need:
- Full name expansion if known (e.g., "William Chapman")
- Disambiguation if multiple people with same name
- Cross-reference to other roles if applicable

### Action Required

**Before adding Mr W Chapman:**
1. Check if there's a separate "People by name" hierarchy
2. Verify full name and biographical details if available
3. Determine if polyhierarchical relationships needed (e.g., person appears in multiple occupational contexts)

---

## 3. University of Sydney (institution)

### Current State

✅ **Already exists in taxonomy:**

```csv
University of Sydney (institution),University of Sydney (institution),hierarchy,parent=universities
```

**Location:** Agents > Organisations > Educational institutions > universities > University of Sydney (institution)

### Action Required

**Item needing this tag:**
- Mountain Mixtures (1892-11-25)
- Currently tagged: Mount Victoria School
- Should also be tagged: University of Sydney (institution)

**Reason:** Based on user note, this item mentions University of Sydney in context (likely Junior University Exam or similar)

**No taxonomy changes needed** - just apply existing tag to item.

---

## Implementation Plan

### Phase 1: Add School Teachers Hierarchy ✅ COMPLETE

**Implemented:** 2025-11-14

```bash
python scripts/41_add_educational_occupations_taxonomy.py
```

**Result:** 7 new CSV entries added (6 hierarchy + 1 specific person)
- Educational occupations (intermediate parent)
- School teachers (intermediate parent)
- School teacher (singular generic leaf)
- Mr W Chapman (specific person)

**Taxonomy updated:** 2,223 entries (was 2,216)

### Phase 2: Add Mr W Chapman ✅ COMPLETE

**Decision made:** Include Mr W Chapman as specific named person under School teachers

**Rationale:** User specified to "identify people explicitly and specifically where we can"

**Implementation:**
- Added to taxonomy: `Mr W Chapman → School teachers`
- Added to application CSV: Megalong Matters (1892-09-09)
- Action: REPLACE "Megalong Valley School" with "Mr W Chapman"

### Phase 3: Apply University of Sydney Tag (Ready)

**Action:** Simply add existing "University of Sydney (institution)" tag to:
- Item: Mountain Mixtures (1892-11-25)
- URL: http://nla.gov.au/nla.news-article194115505

---

## Item Retagging Summary

### Items Requiring Additional Tags

| Item Title | Current Tags | Add Tags | Action |
|------------|--------------|----------|--------|
| Megalong Matters (1892-09-09) | Megalong Valley School | School teacher (or Mr W Chapman) | Replace school tag with occupation tag |
| Mountain Mixtures (1892-11-25) | Mount Victoria School (organisation) | University of Sydney (institution) | Add additional tag (keep school tag) |

---

## Updated Statistics

### Educational Schools Tag Applications (After Manual Review)

**Total applications:** 29 (was 23)
- REPLACE: 18 (single building or organisation tag)
- REPLACE_WITH_BOTH: 8 (both building and organisation tags)
- RETAG_SCHOOL_OF_ARTS: 3 (School of Arts corrections)

**Coverage:**
- Katoomba Public School: 5 items (from automated classification)
- Katoomba Superior Public School: 6 items (from automated classification)
- Generic "School": 12 items (from automated classification)
- Megalong Valley School: 5 items (from manual review - Item 3 excluded as it's actually about school teacher)
- Mount Victoria School: 1 item (from manual review)

**Total items with school tags:** 29 items with educational school classification

**Additional items needing non-school tags:** 1 (Megalong Item 3 - school teacher occupation)

---

## Validation Checklist

Before implementation:

- [ ] Review existing People/Occupations structure for consistency
- [ ] Confirm educational occupations as appropriate intermediate category
- [ ] Verify Mr W Chapman name spelling and biographical details
- [ ] Check if University of Sydney tag already applied to Mountain Mixtures (1892-11-25)
- [ ] Confirm whether to create individual person entries or use generic occupational tags

---

## Files Referenced

- **Tag applications CSV:** `entity-tagging-system/outputs/educational-schools/item_tag_application.csv` (updated with 6 manual items)
- **Manual review report:** `entity-tagging-system/outputs/educational-schools/manual-review-report.md` (with user classifications)
- **Master taxonomy:** `data/tag_map_consolidated.csv`

---

## Next Steps

1. ✅ School teachers hierarchy - Ready to implement (6 CSV entries)
2. ⏳ Mr W Chapman - Requires name verification and decision on person vs occupation tagging approach
3. ✅ University of Sydney - Already exists, just apply to Mountain Mixtures item
4. ⏳ Update implementation summary with complete 29-item coverage

---

**Prepared:** 2025-11-14
**Status:** School teachers hierarchy ready; Mr W Chapman requires research
