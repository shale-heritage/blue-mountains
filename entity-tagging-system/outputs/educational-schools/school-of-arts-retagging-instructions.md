# School of Arts Retagging Instructions

**Date:** 2025-11-14
**Issue:** 3 items incorrectly tagged as "School" (educational schools) should be "School of Arts" (cultural societies)

---

## Summary

During educational schools classification, 3 items were found to be incorrectly tagged with the generic "School" tag when they actually refer to "School of Arts" (cultural societies/community halls), not educational institutions.

These require retagging from the educational schools facet to the Schools of Arts facet.

---

## Items to Retag

### Item 1: Mountain Mixtures (1892-11-25)

**Trove URL:** http://nla.gov.au/nla.news-article194115505

**Current (incorrect) tag:** `School`

**Correct tag:** `School of Arts` (or `Katoomba School of Arts` if context allows specificity)

**Context:**
> Katoomba School of Arts Flower Show on [?] and 17th December.

**Reasoning:** This clearly refers to the Katoomba School of Arts (cultural society) organising a Flower Show event, not an educational school.

**Action:**
1. Remove tag: `School`
2. Add tag: `Katoomba School of Arts`

---

### Item 2: Town Talk (1903-03-13)

**Trove URL:** http://nla.gov.au/nla.news-article188871927

**Current (incorrect) tag:** `School`

**Correct tag:** `School of Arts`

**Context:**
> A meeting of the committee of the local School of Arts was to have been held at the room on Tuesday evening.

**Reasoning:** Committee meeting refers to organisational governance of School of Arts (cultural society), not educational school.

**Action:**
1. Remove tag: `School`
2. Add tag: `School of Arts` (generic, as specific location not clearly stated but "local" suggests Katoomba)

---

### Item 3: Town Talk (1904-05-13)

**Trove URL:** http://nla.gov.au/nla.news-article188871519

**Current (incorrect) tag:** `School`

**Correct tag:** `School of Arts`

**Context:**
> A canvass of the town is to be made for an increase in the membership of the School of Arts.

**Reasoning:** Membership canvass refers to organisational membership drive for School of Arts (cultural society), not educational school.

**Action:**
1. Remove tag: `School`
2. Add tag: `School of Arts` (generic, as specific location not clearly stated)

---

## Implementation Notes

### Zotero Retagging Process

1. **Search for items by URL** or title in Zotero library
2. **Remove the incorrect "School" tag** from each item
3. **Add the correct "School of Arts" tag** (or specific variant if identifiable)
4. **Verify no other tags need adjustment**

### Data Quality Improvement

This retagging will:
- Remove 3 items from the educational schools category (where they don't belong)
- Add 3 items to the Schools of Arts category (where they do belong)
- Improve precision of both categories
- Reduce false positives in educational schools searches

### Future Prevention

**Root cause:** The generic "School" tag is ambiguous and can refer to:
1. Educational schools (public schools)
2. Schools of Arts (cultural societies/community halls)

**Solution implemented:**
- Educational schools now use disambiguation: `School (building)` / `School (organisation)`
- Schools of Arts retain unqualified form as they have distinct terminology
- Generic "School" now maps to `School (organisation)` via synonym, with note about educational context

**Recommendation:** When cataloguing, always use the most specific term available:
- For educational institutions: `[Name] Public School (building)` or `(organisation)`
- For cultural societies: `[Name] School of Arts`
- Avoid unqualified "School" unless context is unambiguous

---

## Verification

After retagging, verify:

```bash
# Check these items no longer tagged with School
# (Search by Trove URL in Zotero)
```

Expected result:
- Mountain Mixtures (1892-11-25): Tagged `Katoomba School of Arts`, not `School`
- Town Talk (1903-03-13): Tagged `School of Arts`, not `School`
- Town Talk (1904-05-13): Tagged `School of Arts`, not `School`

---

## Related Documentation

- Educational schools classification: `data/entity_classification/educational-schools_classification_results.md`
- Schools of Arts classification: `data/entity_classification/schools_classification_prompt.txt`
- Taxonomy implementation: `entity-tagging-system/outputs/educational-schools/taxonomy-implementation-plan.md`

---

**Status:** Ready for implementation in Zotero
**Priority:** Medium (improves data quality but doesn't block other work)
