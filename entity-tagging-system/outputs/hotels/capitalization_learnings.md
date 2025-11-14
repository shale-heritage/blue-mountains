# Hotel Classification Capitalisation Handling - Learnings

**Date:** 2025-11-13
**Phase:** Phase 4 User Review
**Issue:** Zotero tag capitalisation variants vs original source text capitalisation

---

## Problem Identified

During Phase 4 user review, a systematic misclassification was discovered affecting 4 items tagged with lowercase "family hotel" in Zotero.

### The Issue

**Zotero Tags (user-generated):**
- `Family hotel` (capitalised)
- `family hotel` (lowercase)

**Original Newspaper Text (all instances):**
- "Family Hotel" (always capitalised)

**Incorrect Assumption:**
The NLU classification system assumed that:
- Capitalised Zotero tag → Specific entity (Katoomba Family Hotel)
- Lowercase Zotero tag → Generic family hotel

**Reality:**
ALL instances in the original source text used capitalised "Family Hotel", referring to the specific Katoomba establishment, regardless of how the tag was stored in Zotero.

---

## Root Cause

The Zotero tag capitalisation variants resulted from:

1. **User tagging inconsistency** - Same entity tagged with different capitalisation on different items
2. **Zotero's case-sensitive tag system** - Treats "Family hotel" and "family hotel" as distinct tags
3. **NLU over-reliance on tag capitalisation** - Used Zotero tag capitalisation as classification signal without verifying against source text

---

## Items Affected

### Item 4: Death of Mrs. Nimmo (1926-12-03)

**Zotero tag:** `family hotel` (lowercase)
**Source text:** "Family Hotel" (capitalised)
**Original classification:** `family hotel (business)` ❌
**Corrected classification:** `Katoomba Family Hotel (business)` ✓

### Item 5: The Passing of a Mountaineer (1917-03-23)

**Zotero tag:** `family hotel` (lowercase)
**Source text:** "Family Hotel" (capitalised)
**Original classification:** `family hotel (business)` ❌
**Corrected classification:** `Katoomba Family Hotel (business)` ✓

### Item 6: Katoomba (1905-08-04)

**Zotero tag:** `family hotel` (lowercase)
**Source text:** "Family Hotel" (capitalised)
**Original classification:** `family hotel (building)` + `family hotel (business)` ❌
**Corrected classification:** `Katoomba Family Hotel (building)` + `Katoomba Family Hotel (business)` ✓

### Item 39: Mountain Mixtures (1892-04-29)

**Zotero tag:** `Katoomba Family Hotel` (proper name)
**Source text:** "Katoomba Family Hotel" (capitalised)
**Original classification:** `Katoomba Family Hotel (business)` ✓ (correct, but listed here for context)

---

## Impact

**Classification errors:** 4 items (9.3% of 43 total hotel items)

**Nature of errors:**
- All errors were **false negatives** for the specific named entity
- Generic tags applied when specific tags should have been used
- Did not create incorrect polyhierarchy assignments
- Did not misclassify building vs business aspects (those were correct)

**Severity:** Moderate
- Errors would result in items being tagged with generic rather than specific entity tags
- Would reduce precision of search/filtering for Katoomba Family Hotel specifically
- However, building/business facet assignments were correct

---

## Corrective Actions Taken

### 1. Source Text Verification (Manual)

User reviewed original newspaper text snippets for all 7 family hotel items and confirmed:
- ALL instances use capitalised "Family Hotel" in source text
- ALL refer to the specific Katoomba establishment

### 2. Classification Corrections

Updated item_tag_mapping_proposal.md:
- Items 4, 5, 6: Changed from `family hotel` to `Katoomba Family Hotel`
- Updated summary statistics (14 business-only → 12 both tags increased)

### 3. Taxonomy Verification

No taxonomy changes required:
- `Katoomba Family Hotel (building)` already exists
- `Katoomba Family Hotel (business)` already exists
- Generic `family hotel` tags exist for future use if genuine generic mentions found

---

## Lessons Learned

### For Future Entity Classification Work

1. **Do not trust Zotero tag capitalisation as authoritative**
   - Zotero tags are user-generated and inconsistent
   - Always verify capitalisation against source text when ambiguous

2. **Capitalisation as disambiguating signal is unreliable**
   - Cannot use tag capitalisation alone to distinguish generic vs specific entities
   - Must consult original source text context

3. **Need source text verification step for proper names**
   - For entities where generic/specific distinction matters (family hotels, boarding houses, etc.)
   - Add source text verification to classification workflow BEFORE NLU classification

4. **Case-sensitive Zotero tags create duplicates**
   - Same real-world entity can have multiple tag variants
   - Need deduplication strategy that checks source text, not just tag strings

### For NLU Classification Approach

1. **Strengthen entity resolution logic**
   - Add step: "Check if capitalised form exists in source text"
   - If source text is capitalised but Zotero tag is lowercase → flag for review

2. **Context window should include original text**
   - Current approach includes excerpts, but may need full-text access for capitalisation checking
   - Or: Extract entity mentions with surrounding context that preserves capitalisation

3. **Add confidence flags for capitalisation mismatches**
   - When Zotero tag case doesn't match source text case → lower confidence
   - Flag these items for human review in Phase 4

---

## Recommendations for Other Entity Types

### High-Risk Categories (check these for similar issues)

1. **Boarding houses** - May have generic "boarding house" vs specific "Smith's Boarding House"
2. **Shops/stores** - "Store" vs "Peckman Brothers' Store"
3. **Hotels** - Already addressed, but verify other hotels don't have same issue
4. **Churches** - Generic "church" vs specific "St Hilda's Church"

### Low-Risk Categories

1. **People names** - Usually properly capitalised
2. **Place names** - Usually properly capitalised
3. **Organisations** - Usually properly capitalised
4. **Events** - Usually properly capitalised

### Mitigation Strategy

For high-risk categories:
1. Export all Zotero tags with case variants (grep for duplicates ignoring case)
2. Sample check source text capitalisation for variant pairs
3. Apply corrections before Phase 2 NLU classification
4. Document entity resolution decisions in consolidation log

---

## Process Improvement

### Add to Classification Workflow (before NLU)

**New Step 1.5: Entity Normalisation**

After extracting entity mentions (Step 1) and before NLU classification (Step 2):

1. Identify Zotero tag case variants (e.g., "Family hotel" vs "family hotel")
2. For each variant pair:
   - Extract sample source text contexts
   - Check capitalisation in original source
   - Determine if generic or specific entity
   - Create normalisation mapping
3. Apply normalisation before NLU classification
4. Document in entity resolution log

**Estimated time:** 30-60 minutes per entity type (one-time cost)

**Benefit:** Eliminates entire category of classification errors

---

## Verification Checklist

For future entity classification projects:

- [ ] Check for Zotero tag case variants (`grep -i` duplicates)
- [ ] For case variants, verify source text capitalisation
- [ ] Create entity normalisation mapping if needed
- [ ] Document ambiguous cases (when source text has mixed capitalisation)
- [ ] Flag for manual review if source text is inconsistent
- [ ] Test sample after normalisation to verify corrections

---

## Files Modified

1. **entity-tagging-system/outputs/hotels/item_tag_mapping_proposal.md**
   - Updated Items 4, 5, 6, 21, 38 with corrected classifications
   - Added "MODIFIED" flags and user correction rationale
   - Updated summary statistics

2. **data/tag_map_consolidated.csv**
   - Added `Grand Hotel (Sydney) (business)` taxonomy entry
   - No other changes required (Katoomba Family Hotel tags already existed)

3. **entity-tagging-system/outputs/hotels/detailed_review_report.md**
   - User feedback documented with corrections

4. **entity-tagging-system/outputs/hotels/validation_checklist.md**
   - User responses recorded
   - Modifications section updated

---

## Conclusion

This capitalisation issue highlights the importance of **source text fidelity** over user-generated metadata capitalisation. While Zotero tags are valuable starting points, they should not be treated as authoritative for entity resolution, particularly when distinguishing generic from specific named entities.

The correction process was straightforward once identified, affecting only 4 items. However, the lesson is significant: **always verify ambiguous cases against source text**, not just metadata.

For the hotel classification project, this represents a 9.3% error rate that was caught during Phase 4 user review - exactly the validation step designed to catch such issues. The process worked as intended.

---

**Generated:** 2025-11-13
**Reviewed by:** User
**Status:** Corrections applied, learnings documented
