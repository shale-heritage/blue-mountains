# Public Houses Classification Results

**Date:** 2025-11-16
**Entity Type:** Public houses (pubs)
**Method:** Natural Language Understanding via entity-classifier skill
**Total Mentions:** 4 (2 unique items, each tagged with both "Pub" and "pub")

---

## Classification Summary

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 0 | 0% |
| Business only | 0 | 0% |
| Both | 2 | 100% |

**Pattern:** Dual-nature dominant - all mentions reference both physical and business aspects

**Note:** 4 mentions represent 2 unique items (each item has duplicate tags "Pub" and "pub")

---

## Detailed Analysis

### Mention 1

**Entity:** Pub
**Item:** Megalong Valley (1893-06-23)
**Date:** 23 June 1893
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194113432/21705257

**Context:**
> Re the application for a public house, many of the residents are against the project. [We should think a hotel would be preferable to the sly-grog and gambling shanties which are said to exist at the Mines at present. We take a public house to be the lesser of the two evils. A public house is watched by the police, and the Licensing Act is strict enough to keep even the most

**Classification:** **BOTH**

**Building/Facility Indicators:**
- Physical alternative to "sly-grog and gambling shanties" (implies physical premises)
- Comparison with "hotel" suggests similar built infrastructure
- Contrasted with unlicensed premises that "exist at the Mines"

**Business/Organisation Indicators:**
- "Application for a public house" - licensing/regulatory process (business establishment)
- "Watched by the police" - operational oversight of business activity
- "Licensing Act" - legal framework governing business operations
- Community debate about approving the business ("residents are against the project")

**Reasoning:** This mention discusses the proposal to establish a licensed public house. The context emphasises both the regulatory/business aspects (licensing application, police oversight, Licensing Act compliance) and the physical presence (as an alternative to existing shanties, comparison with hotels). The "application" refers to obtaining a licence to operate the business, while the discussion of it being "preferable" to shanties and watched by police indicates both built premises and commercial operations.

**Confidence:** High

---

### Mention 2

**Entity:** Pub
**Item:** Rich Mineral Deposits (1889-10-29)
**Date:** 29 October 1889
**Trove URL:** http://nla.gov.au/nla.news-article227569730

**Context:**
> The nearest "pub." had a fascination for us. We allowed ourselves to roll off our horses, and the amiable old lady who presided behind the bar soon comforted our weary spirits (we had spirits) with something enervating.

**Classification:** **BOTH**

**Building/Facility Indicators:**
- "The nearest pub" - spatial reference indicating physical location
- "Roll off our horses" - movement to/arrival at physical premises
- "Behind the bar" - physical infrastructure/fixture within building

**Business/Organisation Indicators:**
- "Amiable old lady who presided behind the bar" - staffing/employment (business operations)
- Service provision - "comforted our weary spirits" with drinks (commercial transaction)
- Bar service - professional hospitality operation

**Reasoning:** This vivid description captures both the pub as a physical destination ("nearest," riders arriving) and as an operating business (proprietor serving drinks behind the bar, commercial hospitality service). The mention of specific infrastructure (the bar) and service personnel indicates both built environment and business activity.

**Confidence:** High

---

### Mention 3

**Entity:** pub (lowercase variant)
**Item:** Megalong Valley (1893-06-23)
**Date:** 23 June 1893
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194113432/21705257

**Context:**
> Re the application for a public house, many of the residents are against the project. [We should think a hotel would be preferable to the sly-grog and gambling shanties which are said to exist at the Mines at present. We take a public house to be the lesser of the two evils. A public house is watched by the police, and the Licensing Act is strict enough to keep even the most

**Classification:** **BOTH**

**Note:** Duplicate of Mention 1 (same item, different tag capitalization)

**Reasoning:** Identical context to Mention 1 - same classification applies.

**Confidence:** High

---

### Mention 4

**Entity:** pub (lowercase variant)
**Item:** Rich Mineral Deposits (1889-10-29)
**Date:** 29 October 1889
**Trove URL:** http://nla.gov.au/nla.news-article227569730

**Context:**
> The nearest "pub." had a fascination for us. We allowed ourselves to roll off our horses, and the amiable old lady who presided behind the bar soon comforted our weary spirits (we had spirits) with something enervating.

**Classification:** **BOTH**

**Note:** Duplicate of Mention 2 (same item, different tag capitalization)

**Reasoning:** Identical context to Mention 2 - same classification applies.

**Confidence:** High

---

## Pattern Analysis

### Overall Distribution (Unique Items)

- **Building only:** 0 items (0%)
- **Business only:** 0 items (0%)
- **Both:** 2 items (100%)

### Spatial Indicators Found

- **Locational references:** "The nearest pub" (explicit spatial reference)
- **Movement to/arrival:** "Roll off our horses" (traveling to premises)
- **Physical infrastructure:** "Behind the bar" (built fixture)
- **Comparative location:** Contrasted with "shanties which exist at the Mines"

### Agency Indicators Found

- **Licensing/regulation:** "Application for a public house," "Licensing Act," "watched by the police"
- **Employment/staffing:** "Amiable old lady who presided behind the bar"
- **Service provision:** Serving drinks, "comforted our weary spirits"
- **Commercial operations:** Bar service, hospitality transactions
- **Community oversight:** Residents debating approval of business establishment

### Key Observations

1. **Strong dual-nature pattern:** Both items reference physical premises AND business operations equally
2. **Regulatory framework prominent:** Licensing, police oversight, community approval processes
3. **Hospitality services explicit:** Service personnel, drink provision, customer interaction
4. **Physical infrastructure clear:** Bar fixtures, built premises as alternatives to shanties
5. **Sample size limitation:** Only 2 unique items (4 mentions due to duplicate tags)

---

## Taxonomy Implications

### Current Taxonomy State

**Existing structure (partial disambiguation):**
```
Built Environment > accommodation buildings > public houses (buildings)
  └── public house (building)

Alcohol-related venues - THEMATIC > Public houses (polyhierarchical)
  └── Public house (polyhierarchical)
```

**Issues identified:**
1. **Incomplete disambiguation:** Building facet exists, but no Agents/business facet
2. **Mixed approach:** Some qualified (building), some unqualified (polyhierarchical)
3. **Inconsistent with project pattern:** Hotels, schools, churches all use full (building)/(business/organisation) disambiguation

### Recommended Taxonomy Structure

**Complete disambiguation following project pattern:**

```
Built Environment > accommodation buildings > public houses (buildings)
  └── public house (building)

Agents > Businesses > Hospitality businesses > public houses (businesses)
  └── public house (business)
```

**Alternative placement for Agents facet:**
```
Agents > Businesses > Drinking establishments > public houses (businesses)
  └── public house (business)
```

### Rationale for Full Disambiguation

1. **Empirical evidence:** 100% of mentions show dual nature (both building and business)
2. **Consistency:** Aligns with hotels (building/business), schools (building/organisation), churches (building/organisation)
3. **Clarity:** Eliminates ambiguity between physical premises and business operations
4. **Getty AAT alignment:** Public houses are dual-faceted (built works + commercial entities)
5. **Regulatory context:** Licensing framework distinguishes premises (where) from operations (business activity)

---

## Comparison with Other Entity Types

| Entity Type | Building % | Business/Org % | Both % | Dominant Pattern |
|-------------|------------|----------------|--------|------------------|
| **Public Houses** | **0%** | **0%** | **100%** | **Dual-nature dominant** |
| Churches | 29% | 29% | 42% | Dual-nature dominant |
| Hotels | 43% | 25% | 32% | Building-dominant |
| Schools of Arts | 11.1% | 55.6% | 33.3% | Organisation-dominant |
| Educational Schools | 17.2% | 58.6% | 24.1% | Organisation-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | Business-dominant |

**Observations:**
- Public houses show strongest dual-nature pattern (100% both)
- Similar to churches (42% both) but even more pronounced
- Unlike hotels (building-dominant) or schools (organisation-dominant)
- Small sample size (2 items) limits statistical confidence

---

## Specific Establishments Identified

**None identified** - Both items use generic "pub"/"public house" terminology without naming specific establishments.

**Implication:** Current taxonomy only needs:
- Generic: public house (building) / public house (business)
- No specific named establishments to add at this stage

---

## Data Quality Notes

### Tag Duplication Issue

Both items are tagged with duplicate capitalisation variants:
- Item 1: Tagged with both "Pub" and "pub"
- Item 2: Tagged with both "Pub" and "pub"

**Recommendation:** Consolidate to single preferred form during retagging phase. Taxonomy already maps "Pub" → "public house" and "pub" → "public house" as synonyms.

### Sample Size Limitation

- Only 2 unique items found (4 mentions due to duplicate tags)
- Limited statistical confidence for pattern generalisation
- However, both items show consistent dual-nature classification
- Pattern aligns with domain knowledge (pubs are inherently both premises and businesses)

---

## Methodology Notes

### Classification Approach

- Natural Language Understanding via entity-classifier skill
- Applied linguistic heuristic framework (spatial vs agency indicators)
- Context-aware analysis of each mention
- Duplicate mentions identified and noted

### Human Review

**HUMAN REVIEW:**

**Mention 1:**
- [ ] Confirm classification
- [ ] Change to: [ ] building  [ ] business  [ ] both

**Notes:**


**Additional/Alternative Tags:**


---

**Mention 2:**
- [ ] Confirm classification
- [ ] Change to: [ ] building  [ ] business  [ ] both

**Notes:**


**Additional/Alternative Tags:**


---

## Next Steps

1. **Human review** - Validate classifications (2 unique items)
2. **Implement taxonomy changes** - Complete disambiguation structure (add business facet)
3. **Create item tag application CSV** - Retag 2 items with qualified tags
4. **Address tag duplication** - Consolidate "Pub"/"pub" duplicate tags
5. **Document decision** - Add to `planning/consolidation-decisions.md`
6. **Consider expanded search** - Check for named pubs (e.g., "Commercial Hotel's public bar" might be tagged differently)

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/public-houses/public-houses_classification_results.md` (this file)
- **Item mentions:** `data/entity_classification/public-houses_mentions.json`
- **Classification prompt:** `data/entity_classification/public-houses_classification_prompt.txt`

---

**Classification completed:** 2025-11-16
**Analyst:** Claude (entity-classifier skill)
**Confidence:** High (despite small sample size, pattern is clear and consistent)
