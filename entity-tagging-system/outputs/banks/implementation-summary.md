# Banks: Disambiguation Implementation Summary

**Date:** 2025-11-16
**Status:** ✅ COMPLETE - Ready for Zotero application

---

## Summary

Implemented (building)/(business) disambiguation for Banks, replacing unqualified polyhierarchical structure. This strategic decision aligns Banks with the established pattern for hotels, public houses, schools of arts, churches, and boarding houses.

**Important caveat:** Implementation based on domain knowledge and project consistency due to very small sample size (1 valid bank reference, 1 false match removed).

---

## Classification Results

**Total items analysed:** 2 items
- **Valid bank references:** 1 item
- **False matches:** 1 item (removed)

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 0 | 0% |
| Business only | 0 | 0% |
| Both | 1 | 100% |

**Pattern:** Dual-nature (100% both) - based on single valid item

**Critical issue identified:** 50% false positive rate due to "bankrupt" substring match

**Human review:** No corrections needed for valid classification

---

## Taxonomy Changes

### Removed (5 obsolete entries)

**Unqualified polyhierarchical structure:**

```csv
Bank,Bank,hierarchy,parent=Financial institutions
Bank,Bank,hierarchy,parent=Commercial buildings
bank,bank,hierarchy,parent=commercial buildings
bank,bank,hierarchy,parent=financial institutions
Bank,bank,synonym,Capitalized variant from original Zotero tags
```

### Added (10 new entries)

**Built Environment facet:**

```csv
banks (buildings),banks (buildings),hierarchy,parent=commercial buildings
bank (building),bank (building),hierarchy,parent=banks (buildings)
Commercial Bank of Australia (building),Commercial Bank of Australia (building),hierarchy,parent=banks (buildings)
```

**Agents facet:**

```csv
banks (businesses),banks (businesses),hierarchy,parent=financial institutions
bank (business),bank (business),hierarchy,parent=banks (businesses)
Commercial Bank of Australia (business),Commercial Bank of Australia (business),hierarchy,parent=banks (businesses)
```

**Synonyms to both aspects:**

```csv
Bank,bank (building),synonym,Capitalized variant - maps to building aspect
Bank,bank (business),synonym,Capitalized variant - maps to business aspect
Commercial Bank,Commercial Bank of Australia (building),synonym,Short form - maps to building aspect
Commercial Bank,Commercial Bank of Australia (business),synonym,Short form - maps to business aspect
```

**Net change:** +5 entries (5 removed, 10 added)
**Final taxonomy size:** 2,237 entries

---

## New Taxonomy Structure

```text
Built Environment > Commercial buildings > banks (buildings)
├── bank (building)
└── Commercial Bank of Australia (building)

Agents > Businesses > Financial institutions > banks (businesses)
├── bank (business)
└── Commercial Bank of Australia (business)
```

**Leaf-node pattern:**
- Plural parent: banks (buildings) / banks (businesses)
- Generic singular: bank (building) / bank (business)
- Specific establishments: Commercial Bank of Australia (building/business)

---

## Specific Establishments Identified

**From this analysis:**
1. **Commercial Bank of Australia** - 1 mention (branch opening in Katoomba, 1903)

**Potential additional establishments** (not yet tagged):
- Bank of New South Wales (major historical Australian bank)
- Savings Bank of New South Wales
- Other commercial banks operating in Blue Mountains region

**Note:** As tagging enrichment continues, additional specific establishments can be added following the same (building)/(business) pattern.

---

## Items Requiring Zotero Retagging

**Total:** 2 items

**Breakdown:**
- Replace with both (building + business) + add specific establishment: 1 item
- Remove false match tags: 1 item
- Consolidate duplicate tags (Bank/bank): 1 item

**Application CSV:** `entity-tagging-system/outputs/banks/item_tag_application.csv`

---

## Strategic Decision: Implement Disambiguation Despite Small Sample

**Rationale:**

1. **Domain knowledge strongly supports dual nature**
   - Bank branches inherently combine physical premises and institutional operations
   - Historical banking involved both building infrastructure and financial services
   - "Branch office" explicitly indicates both location (building) and operations (business)

2. **Single valid item shows clear dual-nature pattern**
   - Building: "branch office in Katoomba" (physical premises)
   - Business: "Commercial Bank of Australia opened" (institutional operations)
   - Cannot separate branch location from banking operations

3. **Consistency with project pattern**
   - Matches hotels (building/business) - commercial accommodation
   - Matches public houses (building/business) - commercial hospitality
   - Banks are commercial financial services - same dual-nature logic applies

4. **Getty AAT alignment**
   - Banks are dual-faceted (built works + financial organisations)
   - Branch banks particularly clear: premises + institutional presence

5. **Future-proofing**
   - Structure ready as more bank items discovered
   - Specific establishments can be added systematically
   - Consistent pattern across all commercial entity types

6. **Small sample size acknowledged**
   - Only 1 valid reference insufficient for statistical confidence
   - Decision relies on domain knowledge + project consistency
   - Structure anticipates future tagging enrichment

---

## Key Findings

### Pattern Comparison

| Entity Type | Building % | Business/Org % | Both % | Sample Size | Dominant Pattern |
|-------------|------------|----------------|--------|-------------|------------------|
| **Banks** | **0%** | **0%** | **100%** | **1** | **Dual-nature** |
| Public Houses | 0% | 0% | 100% | 2 | Dual-nature dominant |
| Churches | 29% | 29% | 42% | 83 | Dual-nature dominant |
| Hotels | 43% | 25% | 32% | 43 | Building-dominant |
| Schools of Arts | 11.1% | 55.6% | 33.3% | 18 | Organisation-dominant |
| Educational Schools | 17.2% | 58.6% | 24.1% | 29 | Organisation-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | 8 | Business-dominant |

**Observation:** Banks show dual-nature pattern consistent with other commercial entities (public houses, hotels), though sample size (N=1) prevents statistical confidence.

### Building Evidence

**Spatial indicators found:**
- Branch office establishment ("opened a branch office in Katoomba")
- Geographic location (physical presence in specific town)
- Premises reference ("office" implies physical space)

### Business Evidence

**Agency indicators found:**
- Corporate entity ("Commercial Bank of Australia")
- Business operations (opening a branch = expansion, business activity)
- Organisational action (corporate decision-making and execution)
- Financial services (implied banking operations)

---

## Data Quality Issues

### False Match Problem

**Issue:** "Bankruptcy" creates substring collision with "Bank"

**Impact:**
- 50% false positive rate (1 of 2 items incorrect)
- Item incorrectly tagged "Bank" when discussing personal bankruptcy
- Pollutes Zotero tags

**Resolution:**
- Item tag application CSV includes removal action
- Taxonomy already has safeguard: `bank,bank,keep,Substring coincidence`
- Future consideration: enhance script 38 to filter "bankrupt" vs "bank"

### Tag Duplication

Valid bank item has both "Bank" and "bank" tags (capitalisation variants) - addressed in retagging.

### Sample Size Limitation

**Critical limitation:** Only 1 valid bank reference found

**Implications:**
- Cannot reliably generalise pattern from single item
- Pattern percentages (100% both) not statistically meaningful
- Implementation relies on domain knowledge, not empirical validation

**Mitigation:**
- Acknowledge limitation in documentation
- Rely on domain knowledge (banks inherently dual-nature)
- Maintain consistency with project pattern
- Structure ready for additional items as discovered

---

## Recommendations for Future Work

### Expand Bank Tagging

**Search strategies:**
1. **Full-text search for specific banks:**
   - "Commercial Bank of Australia"
   - "Bank of New South Wales"
   - "Savings Bank"
   - "English, Scottish and Australian Bank"
   - "Union Bank of Australia"

2. **Review items tagged with financial/economic terms:**
   - Items about finance, commerce, business
   - Economic crisis/depression items (bank failures)
   - Business establishment/closure items

3. **Check historical Blue Mountains business directories:**
   - Identify which banks operated in the region
   - Search for those specific institutions

### Improve False Match Detection

**Script 38 enhancement:**
- Add word boundary detection to prevent "bankrupt" matching "bank"
- Check for other potential substring issues:
  - "embankment" (geographical feature)
  - "riverbank" (geographical feature)
  - "banksia" (plant species)

### Document Specific Establishments

As additional bank references found:
- Add specific establishments to taxonomy (building/business pairs)
- Document which banks operated in Blue Mountains
- Track temporal patterns (when banks established/closed)

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/banks/banks_classification_results.md`
- **Item mentions:** `data/entity_classification/banks_mentions.json`
- **Classification prompt:** `data/entity_classification/banks_classification_prompt.txt`
- **Tag application CSV:** `entity-tagging-system/outputs/banks/item_tag_application.csv`
- **Taxonomy implementation script:** `scripts/46_implement_banks_taxonomy.py` (executed)
- **Backup:** `data/tag_map_consolidated.csv.backup-20251116-075341`

---

## Next Steps

1. **Apply Zotero tags** - Use item_tag_application.csv to:
   - Retag 1 valid bank item with qualified tags + specific establishment
   - Remove false match tags from bankruptcy item
   - Consolidate duplicate Bank/bank tags

2. **Document decision** - Add to `planning/consolidation-decisions.md`
   - Note small sample size and reliance on domain knowledge
   - Explain consistency rationale

3. **Expand search** - Consider full-text search for specific bank names

4. **Continue to retailers** - Next medium-priority entity type

---

## Getty AAT Alignment

**Banks (buildings):** Bank buildings, branch offices, financial institution premises (Built Environment facet)

**Banks (businesses):** Financial institutions, banking operations, commercial banks (Agents facet)

✅ Dual-faceted structure aligns with Getty AAT patterns for commercial financial institutions

---

**Implementation completed:** 2025-11-16
**Taxonomy size:** 2,237 entries (+5 from Banks implementation)
**Items awaiting Zotero application:** 110 total (108 previous + 1 bank + 1 removal)
