# Retailers Misclassification Correction Report

**Date:** 2025-11-16
**Purpose:** Document misclassified businesses and propose corrective retagging

---

## Executive Summary

**Finding:** All items currently tagged under "Retailers and stores" for Nimmo's and Peckman Bros are misclassified.

**Businesses affected:**
- **Nimmo's** → Actually a hotel (Nimmo's Railway Hotel)
- **Peckman Bros** → Actually a coach/transportation service

**Action required:** Remove from "Retailers and stores", retag under correct categories

---

## Nimmo's: Hotel Misclassified as Retailer

### Evidence Summary

**3 unique items, 6 total mentions** (duplicate "Nimmo's" tags on each item)

| Item | Date | Explicit Evidence | Business Type |
|------|------|-------------------|---------------|
| Mountain Mixtures (1893-06-02) | 2 June 1893 | "meeting held at **Nimmo's Railway Hotel**" | Hotel (explicit) |
| [untitled] (1889-06-29) | 29 June 1889 | "**Nimmo's smoking-room**", "in **the bar**" | Hotel/Public house |
| Local Jottings (1889-09-21) | 21 September 1889 | "solicitor, **at Nimmo's** every Saturday" | Hotel (meeting venue) |

**Conclusion:** Nimmo's is definitively a hotel, specifically **Nimmo's Railway Hotel**.

### Current Tags (Incorrect)

```
Nimmo's (under "Retailers and stores")
```

### Proposed Corrections

**Remove:**
- "Nimmo's" tag (incorrectly placed under retailers)

**Add:**
- "Nimmo's Railway Hotel (building)"
- "Nimmo's Railway Hotel (business)"

**Alternative (if "Nimmo's Railway Hotel" too long):**
- "Nimmo's Hotel (building)"
- "Nimmo's Hotel (business)"

### Taxonomy Implications

**Check if already exists:**
- Nimmo's may already have hotel tags on these items
- If so, just remove incorrect retailer tag
- If not, add hotel tags as above

**Taxonomy entry needed:**
```csv
Nimmo's Railway Hotel (building),Nimmo's Railway Hotel (building),hierarchy,parent=hotels (buildings)
Nimmo's Railway Hotel (business),Nimmo's Railway Hotel (business),hierarchy,parent=hotels (businesses)
Nimmo's,Nimmo's Railway Hotel (building),synonym,Short form - maps to building aspect
Nimmo's,Nimmo's Railway Hotel (business),synonym,Short form - maps to business aspect
```

### Items Requiring Retagging

**Item 1:**
- **Title:** Mountain Mixtures (1893-06-02)
- **Date:** 2 June 1893
- **Trove URL:** http://nla.gov.au/nla.news-article194113004
- **Current tags:** Nimmo's (retailers)
- **Remove:** Nimmo's (from retailers and stores)
- **Add:** Railway Hotel Katoomba (building)
- **Context snippet:** "A meeting was held at Nimmo's Railway Hotel..."
- **Rationale:** Building-only tag appropriate for venue context (meeting location)

**Item 2:**
- **Title:** [untitled] (1889-06-29)
- **Date:** 29 June 1889
- **Trove URL:** (not provided in extraction)
- **Current tags:** Nimmo's (retailers)
- **Remove:** Nimmo's (from retailers and stores)
- **Add:** Railway Hotel Katoomba (business)
- **Context snippet:** "from Nimmo's smoking-room...in the bar on Tuesday"
- **Rationale:** Business tag appropriate for operational context (bar service)

**Item 3:**
- **Title:** Local Jottings (1889-09-21)
- **Date:** 21 September 1889
- **Trove URL:** http://nla.gov.au/nla.news-article194115775
- **Current tags:** Nimmo's (retailers)
- **Remove:** Nimmo's (from retailers and stores)
- **Add:** Railway Hotel Katoomba (building)
- **Context snippet:** "Mr. Hewitt, solicitor, at Nimmo's every Saturday"
- **Rationale:** Building-only tag appropriate for venue context (professional services location)

---

## Peckman Bros: Transportation Service Misclassified as Retailer

### Evidence Summary

**3 unique items, 3 mentions**

| Item | Date | Explicit Evidence | Business Type |
|------|------|-------------------|---------------|
| Mountain Mixtures (1892-01-22) | 22 January 1892 | "left Katoomba **per Peckman Bros.' coach**" | Coach service |
| The Rockley Game (1896-02-07) | 7 February 1896 | "driven...in two **conveyances** by Messrs **Peckman Bros**" | Coach service |
| Girls Cricket Match (1895-04-26) | 26 April 1895 | "conveyed...in **four-horse drags** by **Peckman Bros**" | Coach service |

**Conclusion:** Peckman Bros operates coach/transportation services (passenger transport by horse-drawn vehicles).

### Current Tags (Incorrect)

```
Peckman Bros (under "Retailers and stores")
```

**Note:** Taxonomy also has "Peckman Brothers" variant.

### Proposed Corrections

**Remove:**
- "Peckman Bros" tag (incorrectly placed under retailers)
- "Peckman Brothers" tag (if exists, also incorrectly placed under retailers)

**Add:**
- Tags under appropriate transportation category (see taxonomy question below)

### Taxonomy Question: Where Should Coach Services Go?

**Option A: Create new Transportation Services category**

Structure:
```
Agents > Businesses > Transportation services
└── Coach services
    ├── coach service (generic singular)
    ├── Peckman Bros (business)
    └── Peckman Brothers (business - synonym of Peckman Bros)
```

**Option B: Place under existing category**

Check if transportation-related categories already exist:
- Transport services?
- Coach operators?
- Travel services?
- Commercial transport?

**Option C: Dual-nature (building + business)?**

Coach services likely have:
- **Building aspect:** Coach houses, stables, depots (physical infrastructure)
- **Business aspect:** Transportation operations, service provision

If dual-nature, should follow pattern:
```
Built Environment > Transportation buildings > coach services (buildings)
└── Peckman Bros (building)

Agents > Businesses > Transportation services > coach services (businesses)
└── Peckman Bros (business)
```

**Question for user:** How should transportation/coach services be structured in taxonomy?

### Items Requiring Retagging

**Item 1:**
- **Title:** Mountain Mixtures (1892-01-22)
- **Date:** 22 January 1892
- **Trove URL:** http://nla.gov.au/nla.news-article194117043
- **Current tags:** Peckman Bros (retailers)
- **Remove:** Peckman Bros (from retailers and stores)
- **Add:** Peckman Brothers (business)
- **Context snippet:** "left Katoomba per Peckman Bros.' coach for Jenolan Caves"
- **Rationale:** Business tag appropriate for service provision context (coach transportation)

**Item 2:**
- **Title:** The Rockley Game (1896-02-07)
- **Date:** 7 February 1896
- **Trove URL:** http://nla.gov.au/nla.news-article194838040
- **Current tags:** Peckman Bros (retailers)
- **Remove:** Peckman Bros (from retailers and stores)
- **Add:** Peckman Brothers (business)
- **Context snippet:** "driven...in two conveyances by Messrs Peckman Bros"
- **Rationale:** Business tag appropriate for service provision context (coach transportation)

**Item 3:**
- **Title:** Girls Cricket Match at Katoomba (1895-04-26)
- **Date:** 26 April 1895
- **Trove URL:** http://nla.gov.au/nla.news-article194840456
- **Current tags:** Peckman Bros (retailers)
- **Remove:** Peckman Bros (from retailers and stores)
- **Add:** Peckman Brothers (business)
- **Context snippet:** "conveyed...in four-horse drags by Peckman Bros free of charge"
- **Rationale:** Business tag appropriate for service provision context (coach transportation)

---

## Additional "Retailers" Requiring Investigation

### Businesses Not Found in Current Search

The following are tagged as "Retailers and stores" but were **not found** when searching:
1. **Douglas and Company**
2. **P. Mullany and Company**
3. **Tabrett and Company**

**Issue:** Cannot verify if these are genuine retailers or also misclassified.

**Recommendation:** Search Zotero for each to verify actual business type before proceeding.

---

## Questions for User Decision

### 1. Nimmo's Railway Hotel Naming

**Question:** Should we use full name "Nimmo's Railway Hotel" or shorter "Nimmo's Hotel"?

**Considerations:**
- Full name is more precise (distinguishes from other potential Nimmo establishments)
- Shorter name matches common usage ("at Nimmo's")
- Synonym mapping can handle both

**Recommendation:** Use full "Nimmo's Railway Hotel" with "Nimmo's" as synonym

---

### 2. Peckman Bros Transportation Category

**Question:** How should coach/transportation services be structured in taxonomy?

**Options:**
A. Single-facet under Agents > Transportation services (business only)
B. Dual-facet with building + business aspects
C. Different existing category (if transportation already exists)

**Context from mentions:**
- All mentions focus on service provision (transportation operations)
- No explicit mention of coach houses, stables, or physical infrastructure
- May still have building aspects (businesses need premises)

**Recommendation:** Check if transportation category exists first, then decide single vs dual-facet

---

### 3. Investigate Remaining "Retailers"?

**Question:** Should we investigate Douglas and Company, P. Mullany and Company, and Tabrett and Company now?

**Options:**
A. Yes - investigate now to complete retailer audit
B. No - defer investigation, focus on correcting known misclassifications first
C. Partial - quick search to see if findable, deep dive later

**Recommendation:** Quick search at minimum to determine if they exist and basic business type

---

### 4. Generic "Store" / "Retailer" Tags

**Question:** Search found zero items tagged with generic "Store", "store", "Retailers and stores", "retailer or store". Should we:

A. Search full text for retail-related terms ("shop", "merchant", "goods", "merchandise")?
B. Accept that retail stores may not be significant in corpus?
C. Defer retailers disambiguation entirely until genuine retailers found?

**Recommendation:** Option C - defer until we know genuine retailers exist

---

## Proposed Implementation Plan

### Phase 1: Correct Known Misclassifications

1. **Nimmo's (3 items):**
   - Remove from "Retailers and stores"
   - Add "Nimmo's Railway Hotel (building/business)"
   - Update taxonomy with new hotel entry

2. **Peckman Bros (3 items):**
   - Remove from "Retailers and stores"
   - Determine transportation category structure
   - Add appropriate transportation tags
   - Create taxonomy entries as needed

### Phase 2: Investigate Unknown "Retailers"

3. **Search for remaining businesses:**
   - Douglas and Company
   - P. Mullany and Company
   - Tabrett and Company
   - Determine actual business types

### Phase 3: Taxonomy Cleanup

4. **Clean up "Retailers and stores" category:**
   - Remove misclassified entries from taxonomy
   - Assess if any genuine retailers remain
   - Decide whether to proceed with retailers disambiguation

---

## Taxonomy Changes Required

### Remove from Retailers and Stores

```csv
# Remove these entries (misclassified)
Nimmo's,Nimmo's,hierarchy,parent=retailers and stores
Nimmo's,Nimmo's,hierarchy,parent=Retailers and stores
Peckman Bros,Peckman Bros,hierarchy,parent=Retailers and stores
Peckman Brothers,Peckman Brothers,hierarchy,parent=retailers and stores
```

### Add to Hotels

```csv
# Add Nimmo's Railway Hotel
Nimmo's Railway Hotel (building),Nimmo's Railway Hotel (building),hierarchy,parent=hotels (buildings)
Nimmo's Railway Hotel (business),Nimmo's Railway Hotel (business),hierarchy,parent=hotels (businesses)
Nimmo's,Nimmo's Railway Hotel (building),synonym,Short form - maps to building aspect
Nimmo's,Nimmo's Railway Hotel (business),synonym,Short form - maps to business aspect
Nimmo's Railway Hotel,Nimmo's Railway Hotel (building),synonym,Full form - maps to building aspect
Nimmo's Railway Hotel,Nimmo's Railway Hotel (business),synonym,Full form - maps to business aspect
```

### Add Transportation Category (pending user decision on structure)

```csv
# Option A: Business-only
transportation services,transportation services,hierarchy,parent=businesses
coach services,coach services,hierarchy,parent=transportation services
Peckman Bros,Peckman Bros,hierarchy,parent=coach services
Peckman Brothers,Peckman Bros,synonym,Variant spelling

# Option B: Dual-nature
coach services (buildings),coach services (buildings),hierarchy,parent=transportation buildings
Peckman Bros (building),Peckman Bros (building),hierarchy,parent=coach services (buildings)

coach services (businesses),coach services (businesses),hierarchy,parent=transportation services
Peckman Bros (business),Peckman Bros (business),hierarchy,parent=coach services (businesses)

Peckman Brothers,Peckman Bros (building),synonym,Variant spelling - maps to building
Peckman Brothers,Peckman Bros (business),synonym,Variant spelling - maps to business
```

---

## Item Tag Application CSV (Pending User Decisions)

Will create after user confirms:
1. Nimmo's naming convention
2. Peckman Bros category structure
3. Whether to investigate other "retailers" now

---

## Summary

**Total items affected:** 6 items
- Nimmo's: 3 items to retag (hotel)
- Peckman Bros: 3 items to retag (transportation)

**Total taxonomy changes:** TBD (pending decisions)

**Priority:** High - these are fundamental misclassifications affecting data quality

**Next steps:** User decisions on questions 1-4 above

---

**Report prepared:** 2025-11-16
**Awaiting user decisions to proceed with corrections**
