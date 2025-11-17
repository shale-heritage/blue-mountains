# Banks Classification Results

**Date:** 2025-11-16
**Entity Type:** Banks (financial institutions)
**Method:** Natural Language Understanding via entity-classifier skill
**Total Mentions:** 4 (2 unique items, each tagged with both "Bank" and "bank")

---

## Classification Summary

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 0 | 0% |
| Business only | 0 | 0% |
| Both | 1 | 100% |
| **FALSE MATCH** | 1 | N/A |

**Pattern:** Single valid mention shows dual-nature (both building and business aspects)

**Critical Issue:** 1 of 2 unique items is a false match ("bankrupt" not "bank")

---

## Detailed Analysis

### Mention 1 ✓ VALID

**Entity:** Bank
**Item:** Town Talk (1903-10-02)
**Date:** 2 October 1903
**Trove URL:** http://nla.gov.au/nla.news-article188872658

**Context:**
> The Commercial Bank of Australia opened a branch office in Katoomba during the week.

**Classification:** **BOTH**

**Building/Facility Indicators:**
- "Branch office" - physical premises/location
- "Opened...in Katoomba" - establishment of physical presence in specific location
- Spatial reference: office exists in geographic location

**Business/Organisation Indicators:**
- "Commercial Bank of Australia" - corporate entity/financial institution
- "Opened a branch" - business expansion/operations
- Corporate action (organisational decision to establish presence)
- Financial institution operations

**Reasoning:** This mention describes the establishment of a bank branch, which inherently involves both physical premises (the branch office building/space) and organisational operations (the financial institution extending its business to Katoomba). The "branch office" indicates both a physical location where banking occurs AND the institutional presence of the Commercial Bank of Australia as a business entity.

**Confidence:** High

**HUMAN REVIEW:**

- [X] Confirm classification
- [ ] Change to: [ ] building  [ ] business  [ ] both

**Notes:**


**Additional/Alternative Tags:**
- Consider adding specific establishment: "Commercial Bank of Australia"

---

### Mention 2 ✗ FALSE MATCH

**Entity:** Bank (tagged)
**Item:** Local Jottings (1889-09-21)
**Date:** 21 September 1889
**Trove URL:** http://nla.gov.au/nla.news-article194115775

**Context:**
> William Payne, formerly of Orange, is bankrupt. His creditors will feel pain.

**Classification:** **FALSE MATCH - NOT A BANK**

**Issue:** The word "bank" appears as substring of "**bankrupt**" (legal status/financial insolvency), not as reference to a financial institution or bank building.

**Reasoning:** This is a false positive from substring matching. The item discusses personal bankruptcy, not banking institutions. The context is about legal/economic status, not financial services or bank premises.

**Action Required:**
- Remove "Bank"/"bank" tags from this item
- Verify item has appropriate "Bankruptcy" tag (already exists in taxonomy)
- Update taxonomy to prevent future false matches

**Confidence:** Certain (obvious false match)

**HUMAN REVIEW:**

- [x] **REMOVE TAG** - False match on "bankrupt" substring

**Notes:**
Item should be tagged with "Bankruptcy" instead (legal outcome, not banking)

**Additional/Alternative Tags:**
- Bankruptcy (correct tag)
- Remove: Bank, bank (false matches)

*please note that 'bankruptcy' exists already under 'events':

├── legal events
│   ├── bankruptcy

---

### Mention 3 ✓ VALID (Duplicate)

**Entity:** bank (lowercase variant)
**Item:** Town Talk (1903-10-02)
**Date:** 2 October 1903
**Trove URL:** http://nla.gov.au/nla.news-article188872658

**Context:**
> The Commercial Bank of Australia opened a branch office in Katoomba during the week.

**Classification:** **BOTH**

**Note:** Duplicate of Mention 1 (same item, different tag capitalisation)

**Reasoning:** Identical context to Mention 1 - same classification applies.

**Confidence:** High

---

### Mention 4 ✗ FALSE MATCH (Duplicate)

**Entity:** bank (lowercase variant)
**Item:** Local Jottings (1889-09-21)
**Date:** 21 September 1889
**Trove URL:** http://nla.gov.au/nla.news-article194115775

**Context:**
> William Payne, formerly of Orange, is bankrupt. His creditors will feel pain.

**Classification:** **FALSE MATCH - NOT A BANK**

**Note:** Duplicate of Mention 2 (same item, different tag capitalisation)

**Reasoning:** Same false match issue - "bankrupt" not "bank"

**Action Required:** Remove tags

---

## Pattern Analysis

### Overall Distribution (Valid Items Only)

- **Building only:** 0 items (0%)
- **Business only:** 0 items (0%)
- **Both:** 1 item (100%)
- **False matches:** 1 item (removed from analysis)

### Spatial Indicators Found

- **Branch office establishment:** "Opened a branch office in Katoomba"
- **Geographic location:** Physical presence in specific town
- **Premises reference:** "Office" implies physical space

### Agency Indicators Found

- **Corporate entity:** "Commercial Bank of Australia" (financial institution)
- **Business operations:** Opening a branch (expansion, business activity)
- **Organisational action:** Corporate decision-making and execution
- **Financial services:** Implied banking operations

### Key Observations

1. **Single valid item limitation:** Only 1 genuine bank reference found (2 items total, 1 false match)
2. **False match issue:** "Bankruptcy" creates substring collision with "Bank"
3. **Strong dual-nature evidence:** The single valid mention clearly shows both building and business aspects
4. **Specific establishment identified:** Commercial Bank of Australia (could be added to taxonomy)
5. **Branch banking context:** Historical branch establishment (common pattern in Australian banking history)

---

## Data Quality Issues

### False Match Problem

**Root cause:** Substring matching of "bank" within "bankrupt"

**Impact:**
- 50% false positive rate (1 of 2 items incorrect)
- Wastes classification effort
- Pollutes Zotero tags with incorrect "Bank" tags

**Solution required:**
1. **Immediate:** Remove "Bank"/"bank" tags from bankruptcy item
2. **Taxonomy:** Verify "bank" and "bankruptcy" are properly distinguished (already exists: `bank,bank,keep,Substring coincidence`)
3. **Script enhancement:** Improve context extraction to detect "bankrupt" as separate term
4. **Validation:** Check other potential substring collisions (embankment, riverbank, etc.)

### Tag Duplication

Item has both "Bank" and "bank" tags (capitalisation variants) - same issue as public houses.

---

## Taxonomy Implications

### Current Taxonomy State

**Existing structure (polyhierarchical without qualifiers):**

```text
Commercial buildings > Bank (capitalized)
Commercial buildings > bank (lowercase)

Financial institutions > Bank (capitalized)
Financial institutions > bank (lowercase)
```

**Issues:**
- No plural parent (violates leaf-node pattern)
- Capitalisation duplication
- Polyhierarchical without qualifiers
- No specific establishments (Commercial Bank of Australia exists but not tagged)

### Recommended Taxonomy Structure

**Complete disambiguation following project pattern:**

```text
Built Environment > Commercial buildings > banks (buildings)
├── bank (building)
└── Commercial Bank of Australia (building)

Agents > Businesses > Financial institutions > banks (businesses)
├── bank (business)
└── Commercial Bank of Australia (business)
```

### Rationale for Full Disambiguation

1. **Empirical evidence (limited):** 100% of valid mentions show dual nature (1 of 1)
2. **Domain knowledge:** Banks inherently dual-nature (branches are both premises and institutional presence)
3. **Consistency:** Aligns with hotels, public houses, schools of arts
4. **Getty AAT alignment:** Banks are dual-faceted (built works + financial organisations)
5. **Specific establishments:** Commercial Bank of Australia identified, more likely exist
6. **Future-proofing:** As tagging continues, structure ready for additional items

### Sample Size Limitation

**Critical note:** Only 1 valid bank reference is insufficient for confident pattern generalisation.

**Recommendation:**
- Implement disambiguation based on domain knowledge + consistency with project pattern
- **BUT** acknowledge low empirical confidence
- Consider expanded search for bank mentions:
  - Search full text for "Commercial Bank", "Savings Bank", "Bank of New South Wales"
  - Check items tagged with financial/economic terms
  - Review items about business establishment/closures

---

## Comparison with Other Entity Types

| Entity Type | Building % | Business/Org % | Both % | Sample Size | Dominant Pattern |
|-------------|------------|----------------|--------|-------------|------------------|
| **Banks** | **0%** | **0%** | **100%** | **1** | **Dual-nature** |
| Public Houses | 0% | 0% | 100% | 2 | Dual-nature dominant |
| Churches | 29% | 29% | 42% | 83 | Dual-nature dominant |
| Hotels | 43% | 25% | 32% | 43 | Building-dominant |
| Schools of Arts | 11.1% | 55.6% | 33.3% | 18 | Organisation-dominant |
| Educational Schools | 17.2% | 58.6% | 24.1% | 29 | Organisation-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | 8 | Business-dominant |

**Observations:**
- Banks show dual-nature pattern (100% both) but sample size critically small (N=1)
- Pattern aligns with public houses (commercial dual-nature entities)
- Insufficient data for statistical confidence

---

## Specific Establishments Identified

**From this analysis:**
1. **Commercial Bank of Australia** - 1 mention (branch opening in Katoomba, 1903)

**Recommendation:** Add to taxonomy as specific establishment under both building and business facets.

**Potential additional establishments** (not found in current search):
- Bank of New South Wales (major historical Australian bank)
- Savings Bank
- Other commercial banks operating in Blue Mountains region

---

## Next Steps

### Immediate Actions

1. **Remove false match tags** - Delete "Bank"/"bank" from bankruptcy item
2. **Verify bankruptcy tagging** - Ensure item properly tagged with "Bankruptcy"
3. **Human review** - Validate the single genuine bank classification

### Taxonomy Implementation

**Two options:**

**Option A: Implement with caveat (recommended)**
- Proceed with (building)/(business) disambiguation
- Base decision on domain knowledge + project consistency
- Acknowledge low sample size in documentation
- Structure ready as more items discovered

**Option B: Expand search first**
- Search full text for specific bank names
- Find more bank references before implementing taxonomy
- Higher empirical confidence
- More time-intensive

**Recommendation:** Option A - implement disambiguation now, expand tagging later. Banks are inherently dual-nature (domain knowledge certain), and structure should be consistent with project pattern.

### Future Work

1. **Expand bank tagging:**
   - Search full text for "Commercial Bank", "Savings Bank", "Bank of NSW"
   - Review financial/economic items for bank references
   - Add specific establishments as discovered

2. **Fix substring collision:**
   - Enhance script 38 to detect "bankrupt" vs "bank"
   - Check for other substring issues (embankment, riverbank)

3. **Document decision:**
   - Add to `planning/consolidation-decisions.md`
   - Note low sample size and decision rationale

---

## Methodology Notes

### Classification Approach

- Natural Language Understanding via entity-classifier skill
- Applied linguistic heuristic framework
- Context-aware analysis
- False match detection and filtering

### Limitations

- **Sample size:** Only 1 valid bank reference (critically small)
- **False positives:** 50% false match rate highlights need for better filtering
- **Pattern confidence:** Cannot reliably generalise from single item
- **Coverage:** Current tagging may miss many bank references

### Strengths

- False match identified and documented
- Clear dual-nature evidence in valid mention
- Specific establishment identified
- Aligns with domain knowledge of banking

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/banks/banks_classification_results.md` (this file)
- **Item mentions:** `data/entity_classification/banks_mentions.json`
- **Classification prompt:** `data/entity_classification/banks_classification_prompt.txt`

---

**Classification completed:** 2025-11-16
**Analyst:** Claude (entity-classifier skill)
**Confidence:** Low (N=1 valid sample) - relying on domain knowledge for taxonomy decision
**Action required:** Remove false match tags, implement disambiguation, expand search
