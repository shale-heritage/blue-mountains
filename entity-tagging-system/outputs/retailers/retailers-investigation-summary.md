# Retailers Investigation Summary

**Date:** 2025-11-16

**Purpose:** Investigate all businesses tagged under "Retailers and stores" to verify classification accuracy

---

## Key Findings

### 1. Misclassifications Corrected (6 items)

**Nimmo's** (3 items)
- **Actual business type:** Hotel (Railway Hotel Katoomba)
- **Operator:** Mr Joseph Nimmo
- **Action taken:** Removed from retailers, added to Hotels (building/business)
- **Script:** 47_implement_retailers_misclassification_corrections.py

**Peckman Bros** (3 items)
- **Actual business type:** Coach service (transportation)
- **Action taken:** Removed from retailers, added to Transport & logistics businesses > Coach services
- **Script:** 47_implement_retailers_misclassification_corrections.py

### 2. "Phantom" Retailer Entries (0 items tagged)

The following businesses exist in the taxonomy under "Retailers and stores" but have **zero items** tagged with them in Zotero:

1. **Douglas and Company**
   - Listed in: `data/tag_map_consolidated.csv`
   - Tag frequency: 0 items
   - Status: Phantom entry (exists in taxonomy but never used)

2. **P. Mullany and Company**
   - Listed in: `data/tag_map_consolidated.csv`
   - Tag frequency: 0 items
   - Note: "Mr P Mullany" as a person has 12 items, but the company has 0
   - Status: Phantom entry

3. **Tabrett and Company**
   - Listed in: `data/tag_map_consolidated.csv`
   - Tag frequency: 0 items
   - Note: "Tabrett family" exists with items, but the company has 0
   - Status: Phantom entry

---

## Current State of "Retailers and Stores" Category

### Items Actually Tagged
- **Before corrections:** 6 items total (all misclassified)
  - Nimmo's: 3 items → moved to Hotels
  - Peckman Bros: 3 items → moved to Transport & logistics
- **After corrections:** 0 items tagged as retailers

### Taxonomy Entries Remaining
After script 47 corrections, the following entries remain in taxonomy:
- Generic terms: "Retailers and stores" (parent category)
- Generic terms: "Retailer or store" (singular generic)
- Phantom businesses: Douglas and Company (0 items)
- Phantom businesses: P. Mullany and Company (0 items)
- Phantom businesses: Tabrett and Company (0 items)

---

## Analysis

### Why Are There Phantom Entries?

Possible explanations:
1. **Anticipatory tagging:** Entries created during taxonomy development but never applied to items
2. **Historical migrations:** Tags that existed in earlier Zotero versions but items were retagged
3. **Planned but unexecuted:** Businesses identified for tagging but work not completed
4. **Alternative tag usage:** Items may use person tags (e.g., "Mr P Mullany") instead of business tags

### Evidence from Tag Frequency Data

```text
Tag Name                          Items  Percentage
Mr P Mullany                      12     0.32%
Tabrett family                    ?      ?
Douglas and Company               0      0.00%
P. Mullany and Company           0      0.00%
Tabrett and Company              0      0.00%
```

The fact that personal/family tags exist with items suggests these may have been businesses operated by these people, but they were tagged with person/family names rather than business names.

---

## Implications

### No Genuine Retailers Found

**Critical finding:** After investigating all entries under "Retailers and stores":
- All 6 items with business tags were misclassifications
- 3 phantom business entries have zero items
- Generic "Retailer or store" tag has zero items

**Conclusion:** The Blue Mountains Historical Society Zotero library may contain **no items specifically about retail stores** as a primary subject.

### Why Retailers May Be Absent

Possible reasons:
1. **Collection focus:** Library focuses on institutions, infrastructure, community organizations rather than commercial retail
2. **Tagging granularity:** Retail activity tagged by specific business types (grocers, drapers, etc.) rather than generic "retailer"
3. **Incidental mentions:** Retailers mentioned in passing but not tagged as subjects
4. **Person-centric tagging:** Business owners tagged (Mr P Mullany) but not their businesses

---

## Recommendations

### Option A: Remove Phantom Entries (Recommended)

**Rationale:** If entries have never been used, they create taxonomy bloat and confusion

**Action:**
1. Remove Douglas and Company from taxonomy
2. Remove P. Mullany and Company from taxonomy
3. Remove Tabrett and Company from taxonomy
4. Keep generic "Retailers and stores" / "Retailer or store" structure in case future items need it

### Option B: Investigate Person Tags for Business Context

**Rationale:** Business activity may be tagged via person names

**Action:**
1. Search "Mr P Mullany" contexts to determine if retail activity mentioned
2. Search "Tabrett family" contexts to determine business type
3. If retail businesses identified, decide whether to retag with business names or keep person tags

### Option C: Accept Minimal Retail Coverage

**Rationale:** Collection genuinely doesn't focus on retail commerce

**Action:**
1. Document that retail is not a significant subject in this collection
2. Keep taxonomy structure for completeness
3. Remove phantom entries that were never used

---

## Next Steps

### Immediate Actions Completed

✓ Corrected Nimmo's misclassification (3 items)
✓ Corrected Peckman Bros misclassification (3 items)
✓ Verified phantom entries have zero items

### Awaiting Decision

Choose one of the options above (A, B, or C) for handling phantom entries.

**Questions for user:**
1. Should we remove phantom retailer entries from taxonomy?
2. Should we investigate Mr P Mullany and Tabrett family contexts to identify business types?
3. Should we search full text for retail-related terms (shop, store, merchant) to identify untagged retailers?

---

## Files Generated

- `misclassification-correction-report.md` - Detailed analysis of misclassifications
- `item_tag_application.csv` - Retagging instructions for 6 items
- `retailers-investigation-summary.md` - This document
- Script: `47_implement_retailers_misclassification_corrections.py`

## Taxonomy Changes

**Net change:** -4 entries (removed 4 misclassified, added 10 correct entries elsewhere)

**Changes to tag_map_consolidated.csv:**

Removed:
- Nimmo's → Nimmo's (parent=retailers and stores) [2 variants]
- Peckman Bros → Peckman Bros (parent=Retailers and stores)
- Peckman Brothers → Peckman Brothers (parent=retailers and stores)

Added to Hotels:
- Railway Hotel Katoomba (building) + synonyms
- Railway Hotel Katoomba (business) + synonyms

Added to Transport & logistics:
- Coach services (parent category)
- Coach service (singular generic)
- Peckman Brothers (business) + synonyms

---

**Report completed:** 2025-11-16
**Status:** Awaiting user decision on phantom entries (Douglas, Mullany, Tabrett)
