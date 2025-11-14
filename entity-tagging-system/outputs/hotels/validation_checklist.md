# Hotel Item-Level Mapping Validation Checklist

**Date:** 2025-11-13
**Phase:** Phase 4 - User review and approval
**Status:** PENDING USER REVIEW

---

## Overview

This checklist guides review and approval of 43 proposed hotel item-tag mappings before application to `data/tag_application_mapping.csv`.

**Total Items:** 43
**Entities:** 14
**Confidence:** 93% high, 7% medium

---

## Quick Reference

### Proposed Mapping Summary

| Classification | Count | Percentage | Review Priority |
|----------------|-------|------------|-----------------|
| Building only | 18 | 41.9% | Low (if high confidence) |
| Business only | 17 | 39.5% | Low (if high confidence) |
| Both (polyhierarchical) | 8 | 18.6% | Medium (verify dual indicators) |

### Entity Patterns

**Building-only (4 entities):**

- Grand Hotel (1 mention) **NOTE: User changed to BOTH - see modifications section**
- Katoomba Hotel (3 mentions)
- Montrose House (4 mentions)
- Railway Hotel (2 mentions)

**Business-only (2 entities):**

- Mount Victoria Hotel (2 mentions)
- Wentworth Falls Hotel (2 mentions)

**Mixed/Polyhierarchical (8 entities):**

- Belgravia Hotel (2 mentions: 1 building, 1 business)
- Carrington Hotel (4 mentions: 1 building, 1 business, 2 both)
- Centennial Hotel (5 mentions: 1 building, 3 business, 1 both)
- Family hotel (3 mentions: 2 business, 1 both)
- family hotel (3 mentions: 2 business, 1 both)
- Imperial Hotel (3 mentions: 2 building, 1 business)
- Katoomba Family Hotel (1 mention: 1 business)
- Megalong Hotel (8 mentions: 3 building, 3 business, 2 both)

---

## Review Priority

### High Priority: Medium Confidence Items (3 items)

These require careful manual verification:

#### 1. Carrington Hotel - Local Jottings (1889-09-21)

- **Proposed:** `Carrington Hotel (building)`
- **Context:** "Picture of the Carrington Hotel in the Sydney illustrated"
- **Issue:** Minimal context; illustrations typically depict buildings
- **Verify:** Is building classification appropriate for visual representation?
- **USER RESPONSE:** Building only classification is correct. ✓

#### 2. Grand Hotel - Opening of Gladstone Coal-Mine (1885-07-13)

- **Proposed:** `Grand Hotel (building)`
- **Context:** "Shortly-to-be Grand Hotel in Phillip-street, Sydney"
- **Issue:** Future establishment, not yet operating
- **Verify:** Building classification appropriate for planned/future hotel?
- **USER RESPONSE:** BOTH building and business; tag as 'Grand Hotel (Sydney)' (building and business). **MODIFICATION REQUIRED** ⚠

#### 3. Wentworth Falls Hotel - Mountain Mixtures (1892-01-22)

- **Proposed:** `Wentworth Falls Hotel (business)`
- **Context:** "Mr. N. Delaney's Wentworth Falls Hotel" in business notices section
- **Issue:** Brief mention in advertising context
- **Verify:** Business classification justified by advertising/proprietor identification?
- **USER RESPONSE:** Business only is correct. ✓

### Medium Priority: "Both" Classifications (8 items)

Verify that dual indicators genuinely present:

1. **Family hotel** - Katoomba (1905-08-04)
   - Both: Proprietor identification + room rental
2. **family hotel** - Katoomba (1905-08-04)
   - Both: Same context (case variant)
3. **Carrington Hotel** - Katoomba Police Court (1894-09-21)
   - Both: Licensee testimony + spatial location
4. **Carrington Hotel** - A Charge of Rape (1890-09-06)
   - Wait, this is classified as "building" not "both" in the proposal
5. **Megalong Hotel** - The Megalong Hotel (1894-09-21)
   - Both: Advertisement (marketing + location)
6. **Megalong Hotel** - Advertising (1895-02-08)
   - Both: Advertisement (duplicate of above)
7. **Megalong Hotel** - Katoomba Police Court (1895-12-13)
   - Both: Licensee testimony + "at my hotel"
8. **Centennial Hotel** - Katoomba Court (1893-03-17)
   - Both: Proprietor identified + spatial theft location
9. **Centennial Hotel** - Katoomba Municipal Elections (1890-07-05)
   - Both: "Host Edwards" + room accommodation

**USER RESPONSE:** All appear correct ('both' EXCEPT for item 4, which is correctly 'building' only). ✓

### Low Priority: High Confidence Items (40 items)

Clear indicators support classifications. Spot-check recommended.

---

## Systematic Review Process

### Step 1: Review Medium Confidence Items

- [X] Verify Carrington Hotel illustration (building appropriate?)
- [X] Verify Grand Hotel future reference (BOTH?)
- [X] Verify Wentworth Falls Hotel business notice (business justified?)

### Step 2: Review "Both" Classifications

- [X] Verify all 8 "both" items have genuine dual indicators
- [X] Check proprietor+location pattern is consistently applied
- [X] Check advertisement pattern is consistently applied

### Step 3: Review Capitalization Handling

- [X] Verify "Family hotel" (capital) → Katoomba Family Hotel (3 items)
- [X] Verify "family hotel" (lowercase) → generic family hotel (3 items)
- [ ] Confirm capitalization rule correctly applied in all 7 cases (see detailed_review_report.md)

### Step 4: Spot-Check High Confidence Items

- [ ] Sample 5 "building" classifications (spatial/locational indicators)
- [ ] Sample 5 "business" classifications (licensing/operations indicators)
- [ ] Verify consistency with NLU reasoning
- [ ] Review 10 spot-check items in detailed_review_report.md

### Step 5: Cross-Reference with Taxonomy

- [ ] Verify all proposed tags exist in `data/tag_map_consolidated.csv`
- [ ] Confirm building tags present for all entities
- [ ] Confirm business tags present for all 9 polyhierarchical entities
- [ ] Check no orphaned tags will be created

### Step 6: Validate Mapping Proposal Document

- [ ] Open `entity-tagging-system/outputs/hotels/item_tag_mapping_proposal.md`
- [ ] Verify all 43 items present
- [ ] Check entity grouping is logical
- [ ] Confirm proposed tags match NLU classifications

---

## Common Issues to Watch For

### 1. Metonymy Confusion

**Problem:** Hotel mentioned but unclear if building or business intended

**How to identify:**

- Generic mentions ("a hotel," "the hotel")
- Passive constructions ("hotel was built," "hotel remains closed")
- Spatial vs operational verbs

**USER CLARIFICATION:** Items like 'hotel remains closed' or 'hotel opening soon' should be *business* unless it also involves the building explicitly, as in the Grand Hotel (Sydney) above which is both being built (a building) and will open soon (a business).

**What to check:**

- "Hotel remains closed" → business (operational status)
- "Hotel to be rebuilt" → building (construction passive)
- "Went to the hotel" → building (movement/location)

**USER RESPONSE:** Yes, agree. ✓

### 2. Proprietor Identification Alone

**Problem:** Proprietor mentioned but no clear business context

**How to identify:**

- "Mr. X of the Hotel" without business indicators
- Proprietor mentioned for location identification only

**What to check:**

- If proprietor + spatial context → "both"
- If proprietor + business operations → "business"
- If proprietor only identifies location → "building"

**USER RESPONSE:** Agree. ✓

### 3. Court/Legal Contexts

**Problem:** Legal proceedings could involve building location OR business entity

**How to identify:**

- Licensing violations → business
- Crimes at location → building (or "both" if proprietor testifies)
- Testimony by licensee → "both" (business operator + spatial location)

**USER RESPONSE:** Agree. ✓

### 4. Advertisements

**Problem:** Inherently dual-nature (marketing business + describing location)

**What to check:**

- All advertisements should be "both" unless purely spatial description
- Marketing language ("convenient to visitors") = business indicator
- Geographic descriptors ("at the foot of") = building indicator

**USER RESPONSE:** Agree. ✓

---

## Validation Questions

For each item, ask:

1. **Does the classification match the NLU reasoning?**
   - Check reasoning text in proposal document
   - Verify indicators align with classification

2. **Are proposed tags correct for the classification?**
   - building → (building) tag only
   - business → (business) tag only
   - both → both (building) AND (business) tags

3. **Is capitalization handling correct?**
   - "Family Hotel" → Katoomba Family Hotel?
   - "family hotel" → generic family hotel?

4. **Do the proposed tags exist in taxonomy?**
   - All tags created in Phase 1 restructuring
   - Check if uncertain

5. **Is this mapping consistent with similar items?**
   - Same context type should yield same classification
   - Same entity should follow consistent patterns

---

## Approval Sign-Off

### Review Completion Checklist

- [X] All 3 medium-confidence items reviewed and approved/modified
- [X] All 8 "both" classifications verified
- [ ] Capitalization handling verified (6 Family/family hotel items)
- [ ] Spot-checked 10+ high-confidence items
- [ ] Cross-referenced proposed tags with taxonomy
- [ ] Reviewed full mapping proposal document
- [ ] No inconsistencies or errors identified

### Modifications Made

#### 1. Grand Hotel (Sydney) - Opening of Gladstone Coal-Mine (1885-07-13)

- **Original classification:** `building`
- **Modified classification:** `both` (building + business)
- **Rationale:** Hotel is being built (building aspect) AND will open soon as business (business aspect)
- **Tags required:**
  - `Grand Hotel (Sydney) (building)` ✓ exists
  - `Grand Hotel (Sydney) (business)` ⚠ **TAXONOMY GAP - needs creation**
- **Action:** Create business tag before applying mappings

### Final Approval

**Status:**

- [ ] Approved as presented (no modifications)
- [ ] Approved with modifications (see above)
- [ ] Requires further analysis (specify items)

**Approved by:** ___________

**Date:** ___________

---

## Next Steps After Approval

Once approved:

1. **Phase 3:** Check for taxonomy gaps (expect: none identified)
2. **Phase 5:** Prepare item-level mapping application
3. **Phase 6:** Apply mappings to `data/tag_application_mapping.csv`
4. **Phase 7:** Validate applied mappings
5. **Phase 8:** Generate final documentation

**DO NOT PROCEED** to application phases until this checklist is completed and signed off.

---

**Generated:** 2025-11-13
**Awaiting user approval to proceed**
