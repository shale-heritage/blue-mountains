# Boarding Houses Classification Results

**Date:** 2025-11-14
**Entity Type:** Boarding houses (hospitality accommodation businesses)
**Total Mentions:** 4 (2 unique + 2 case-variant duplicates)
**Method:** NLU classification using entity-classifier skill

---

## Classification Summary

### Overall Statistics (All Unique Mentions)

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 1 | 12.5% |
| Business only | 4 | 50.0% |
| Both | 3 | 37.5% |
| **Total** | **8** | **100%** |

**Coverage:** 7 of 8 tagged items classified (1 item mis-tagged, no boarding house mention found)

### Pattern Observations

**Strong business operational emphasis:** 50% business-only mentions focus on proprietors, keepers, advertising, and commercial operations

**Dual-nature present:** 37.5% of mentions combine building and business aspects (construction, occupancy, meal service, pricing)

**Limited building-only usage:** Only 12.5% purely spatial/locational references (movement between buildings)

**Context-dependent classification:** Same establishment (e.g., Orama Boarding House) appears as business in advertising context, but would be building in locational context

**Comparison with hotels:**
- Hotels: 43% building, 25% business, 32% both
- Boarding houses: 12.5% building, 50% business, 37.5% both
- Boarding houses show stronger business emphasis than hotels in this corpus

---

## Detailed Classifications

### Mention 1: boarding houses

**Item:** Katoomba (1888-01-07)
**Date:** 7 January 1888
**Trove URL:** http://nla.gov.au/nla.news-article100894625

**Classification:** both
**Confidence:** high

**Reasoning:** "All the boarding houses have been taxed to their utmost" combines business capacity management ("taxed to their utmost" = operating at full capacity, business operations) with spatial accommodation ("full" indicates physical occupancy of buildings). The parallel structure with hotels and furnished cottages suggests both physical facilities and commercial operations.

**Indicators Found:**
- Building: accommodation_capacity, spatial_reference (parallel with "furnished cottages")
- Business: operational_capacity ("taxed to their utmost"), commercial_services (accommodation provision), capacity_management

**Context:**
> The Carrington has been full up during the whole season, as also has been The Katoomba and Biles' Hotel. All the boarding houses have been taxed to their utmost, and the various furnished cottages are all full. Among the numerous residents of Katoomba at present will be found most of our leading [?]nists.

---

### Mention 2: boarding houses

**Item:** Mountain Mixtures (1892-11-18)
**Date:** 18 November 1892
**Trove URL:** http://nla.gov.au/nla.news-article194117649

**Classification:** business
**Confidence:** high

**Reasoning:** "Publish a list of visitors at all the boarding houses and hotels" refers to guest lists for publication - this is about commercial hospitality operations and visitor tracking. The phrase "at all the boarding houses" uses "at" locatively but the context is clearly about business operations (publishing visitor lists), not physical structures. This is agency/business activity.

**Indicators Found:**
- Building: locational_prep ("at") but secondary
- Business: visitor_lists (operational record-keeping), commercial_services (hospitality operations), parallel_with_hotels (both business operations)

**Context:**
> We will publish a list of visitors at all the boarding houses and hotels on the Blue Mountains. Names should not reach this office not later than Wednesday, 10 o'clock, in each week.

---

### Mention 3: Boarding houses (case duplicate)

**Item:** Katoomba (1888-01-07)
**Date:** 7 January 1888
**Trove URL:** http://nla.gov.au/nla.news-article100894625

**Classification:** both
**Confidence:** high

**Note:** Exact duplicate of Mention 1 with capitalised variant. Same context, same classification.

---

### Mention 4: Boarding houses (case duplicate)

**Item:** Mountain Mixtures (1892-11-18)
**Date:** 18 November 1892
**Trove URL:** http://nla.gov.au/nla.news-article194117649

**Classification:** business
**Confidence:** high

**Note:** Exact duplicate of Mention 2 with capitalised variant. Same context, same classification.

---

## Duplicate Mapping

- **Mention 3** = Mention 1: both (case variant)
- **Mention 4** = Mention 2: business (case variant)

---

---

### Mention 5: Mrs. Gillen's boarding-house

**Item:** Megalong Valley (1893-06-16)
**Date:** 16 June 1893
**Trove URL:** http://nla.gov.au/nla.news-article194113765

**Classification:** building
**Confidence:** high

**Reasoning:** "They were in the act of crossing from Mrs. Gillen's boarding-house to the billiard-room" uses purely spatial/locational language. The preposition "from" indicates movement away from a physical location, and the parallel structure with "to the billiard-room" confirms this is about physical structures serving as reference points for movement. No business operations or services are mentioned - this is purely about the building as a location in space.

**Indicators Found:**
- Building: locational_prep ("from"), spatial_reference (movement between buildings), parallel_structure (building-to-building movement)
- Business: none

**Context:**
> They were in the act of crossing from Mrs. Gillen's boarding-house to the billiard-room, when one of those heavy squalls brought down with a crash two heavy trees and large branches of others, also some iron sheets from Mrs. Brydon's house, but they escaped it all.

---

### Mention 6: Blue Mountain boarding house

**Item:** Mountain Mixtures (1893-12-29)
**Date:** 29 December 1893
**Trove URL:** http://nla.gov.au/nla.news-article194111522

**Classification:** both
**Confidence:** high

**Reasoning:** "At a certain Blue Mountain boarding house there was duck served up for the Xmas dinner. Certain boarders reckoned, not in contemplation of the ducks but in contemplation of the fat price which they had to pay per week." This combines locational reference ("at") with business operations (meal service, weekly pricing, boarders paying). The mention of "the fat price which they had to pay per week" clearly indicates commercial hospitality operations with pricing structures, while "at a certain boarding house" indicates the physical location where this occurs.

**Indicators Found:**
- Building: locational_prep ("at"), accommodation_capacity (housing boarders)
- Business: commercial_services (meal provision), pricing (weekly rates), customer_relations (boarders paying)

**Context:**
> At a certain Blue Mountain boarding house there was duck served up for the Xmas dinner. Certain boarders reckoned, not in contemplation of the ducks but in contemplation of the fat price which they had to pay per week. Still if people are fools enough to acquiesce in this, the Land Owner may live and grow fat.

---

### Mention 7: Miss Kelly's new boarding house

**Item:** Mountain Mixtures (1891-11-20)
**Date:** 20 November 1891
**Trove URL:** http://nla.gov.au/nla.news-article194115968

**Classification:** both
**Confidence:** high

**Reasoning:** "Miss Kelly's new boarding house is completed and she will move into it early next week" combines building construction ("is completed", physical structure) with ownership/operation ("Miss Kelly's", "she will move into it" indicating owner-operator taking occupancy). The completion of construction emphasises the physical building, while the possessive and operational language ("move into it" to commence operations) indicates the business establishment.

**Indicators Found:**
- Building: construction_completion ("is completed"), physical_structure (building completion), occupancy ("move into it")
- Business: ownership ("Miss Kelly's"), operational_commencement (owner moving in to operate)

**Context:**
> Miss Kelly's new boarding house is completed and she will move into it early next week. We will publish a short list of hotels and boarding-houses in our next issue.

---

### Mention 8: Orama Boarding House (advertisement)

**Item:** Mountain Mixtures (1891-12-04)
**Date:** 4 December 1891
**Trove URL:** http://nla.gov.au/nla.news-article194115914

**Classification:** business
**Confidence:** high

**Reasoning:** "Another new ad. - 'Orama' Boarding House" refers to a commercial advertisement for the establishment. Advertisements are inherently about business promotion and commercial operations, not physical structures. This is about the business seeking customers, not the building itself.

**Indicators Found:**
- Building: none (proper name indicates specific entity but context is purely commercial)
- Business: advertising (commercial promotion), business_operations (seeking customers)

**Context:**
> Another new ad. - "Orama" Boarding House. Getting ripe - Cherries and other Mountain fruits.

---

### Mention 9: Proprietors of boarding-houses

**Item:** Mountain Mixtures (1891-12-04)
**Date:** 4 December 1891
**Trove URL:** http://nla.gov.au/nla.news-article194115914

**Classification:** business
**Confidence:** high

**Reasoning:** "Proprietors of boarding-houses will do well to remember that for over two years THE TIMES has been circulating gratis amongst the very people who require the board" focuses entirely on business operators ("Proprietors") and their commercial interests (advertising to potential customers, "people who require the board" = potential paying guests). The phrase "boarding-house keepers" later in context reinforces this is about business operations and marketing strategy, not physical buildings.

**Indicators Found:**
- Building: none
- Business: proprietorship (business owners), advertising_strategy (marketing to customers), commercial_services ("people who require the board"), business_operations (keeper activities)

**Context:**
> Proprietors of boarding-houses will do well to remember that for over two years THE TIMES has been circulating gratis amongst the very people who require the board. [...] If boarding-house keepers are wise they will do their own advertising in the Sydney papers, and not be made cats-paws of by other people.

---

### Mention 10: Blue Mountain hotel and boarding-house keepers

**Item:** Moutains Mixtures (1893-11-17)
**Date:** 17 November 1893
**Trove URL:** http://nla.gov.au/nla.news-article194110192

**Classification:** business
**Confidence:** high

**Reasoning:** "If Blue Mountain hotel and boarding-house keepers don't take better interest in our Visitor's List it isn't our fault" addresses business operators ("keepers") and their participation in commercial promotional activities (Visitor's List publication). This is entirely about business operations and marketing engagement, not physical facilities.

**Indicators Found:**
- Building: none
- Business: business_operators ("keepers"), promotional_activities (Visitor's List participation), commercial_engagement

**Context:**
> If Blue Mountain hotel and boarding-house keepers don't take better interest in our Visitor's List it isn't our fault. Go slow with the Christmas boom.

---

## Data Quality Issues

### Extraction Completeness - RESOLVED ✅

**Issue identified:** Initial extraction only found 2 unique contexts from 8 tagged items

**Root cause:** Script searched for exact tag name "boarding houses" (plural, two words), but newspaper text uses multiple variant forms:
- "boarding-house" (singular, hyphenated) - 5 occurrences
- "boarding houses" (plural, two words) - 1 occurrence
- "boarding-houses" (plural, hyphenated) - 2 occurrences

**Resolution:** Manual extraction of all 6 additional contexts, classified above as Mentions 5-10

**Items successfully classified:** 7 unique items from 8 tagged (1 item mis-tagged - see below)

### Mis-Tagged Item

**Item:** Mountain Mixtures (1893-05-05)
**Issue:** Tagged with "boarding houses" but contains NO mention of boarding houses in full text
**Recommendation:** Remove "boarding houses" tag from this item

### Case-Variant Duplication

**Issue:** Items tagged with both "boarding houses" and "Boarding houses"

**Impact:** Duplicate classifications (2 case variants for each of 2 contexts = 4 total mentions)

**Resolution:** Application CSV should consolidate to unique items, removing case duplicates

---

## Current Taxonomy Structure

### Existing Dual-Nature Structure ✅

Boarding houses already has a complete dual-nature taxonomy structure:

```text
Built Environment > Accommodation buildings
└── boarding houses (buildings)
    ├── boarding house (building)
    └── Orama Boarding House (building)

Agents > Hospitality businesses
└── boarding houses (businesses)
    ├── boarding house (business)
    └── Orama Boarding House (business)

[Plus polyhierarchical parent "Boarding houses" in multiple thematic categories]
```

**Status:** Structure already implements hotel-style disambiguation with (building)/(business) qualifiers

**Specific entities:**
- Orama Boarding House: Has both building and business variants
- Generic boarding house: Has both building and business variants

---

## Recommendations

### 1. Complete Classification Coverage

**Current:** 2 unique mentions classified (from 2 items)
**Missing:** 6 items require classification

**Action:** Manual review of remaining 6 items:
- Extract contexts from Zotero (may need to check annotations/attachments)
- Classify each as building/business/both
- Add to application CSV

### 2. Apply Existing Taxonomy Structure

**No taxonomy changes needed** - boarding houses already has complete (building)/(business) structure

**Action:** Generate item tag application CSV using existing qualified tags:
- `boarding house (building)` for building-only
- `boarding house (business)` for business-only
- Both tags for "both" classification

### 3. Consolidate Case Variants

**Action:** Remove duplicate "Boarding houses" vs "boarding houses" tags during application

**Expected result:** 8 items should have single qualified tag set (not duplicates)

---

## Comparison with Other Entity Types

| Entity Type | Building % | Organisation/Business % | Both % | Total Mentions |
|-------------|-----------|------------------------|--------|----------------|
| Hotels | 43% | 25% | 32% | 43 |
| Churches | Mixed | Mixed | Mixed | TBD |
| Schools of Arts | 17% | 56% | 28% | 18 |
| Educational schools | 17% | 59% | 24% | 29 |
| **Boarding houses** | **0%** | **50%** | **50%** | **2** |

**Note:** Boarding houses sample size (n=2) insufficient for meaningful statistical comparison. Pattern suggests similar dual-nature to hotels but requires more data.

---

## Next Steps

### Immediate

1. **Manual review:** Extract and classify remaining 6 boarding house items
2. **Generate application CSV:** Use existing (building)/(business) qualified tags
3. **Consolidate case variants:** Remove duplicate "Boarding houses"/"boarding houses" tags

### For Application

Once all 8 items classified:
- Apply qualified tags based on classifications
- Remove unqualified "boarding houses"/"Boarding houses" tags
- Use existing taxonomy structure (no changes needed)

---

## Files Generated

- `data/entity_classification/boarding-houses_mentions.json` - 4 mentions (2 unique + 2 duplicates)
- `data/entity_classification/boarding-houses_classification_prompt.txt` - Classification prompt
- `data/entity_classification/boarding-houses_classification_results.md` - This file

---

**Classification completed:** 2025-11-14
**Status:** Partial - 2/8 items classified, 6 require manual review
**Taxonomy status:** Complete structure already exists, ready to apply
