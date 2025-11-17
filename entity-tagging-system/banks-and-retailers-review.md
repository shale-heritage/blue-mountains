# Banks and Retailers/Stores: Taxonomy Review

**Date:** 2025-11-16
**Status:** Medium-priority dual-nature entities requiring disambiguation decision

---

## Current Taxonomy State

### Banks

**Polyhierarchical structure (unqualified):**

```text
Commercial buildings > Bank (capitalized)
Commercial buildings > bank (lowercase)

Financial institutions > Bank (capitalized)
Financial institutions > bank (lowercase)
```

**Current entries:**
```csv
Bank,Bank,hierarchy,parent=Financial institutions
Bank,Bank,hierarchy,parent=Commercial buildings
bank,bank,hierarchy,parent=commercial buildings
bank,bank,hierarchy,parent=financial institutions
Bank,bank,synonym,Capitalized variant from original Zotero tags
```

**Issues:**
- Polyhierarchical without qualifiers (appears in both facets)
- Capitalization inconsistency (Bank vs bank both exist as separate entries)
- No generic plural parent ("banks" or "Banks")
- No specific named establishments (e.g., "Commercial Bank", "Savings Bank")
- Inconsistent with project's leaf-node pattern (missing plural parent)

---

### Retailers and Stores

**Polyhierarchical structure (mixed qualifiers):**

```text
Commercial buildings > Store (capitalized) - polyhierarchical
commercial buildings > store (lowercase via synonym)

Commercial businesses > Retailers and stores (capitalized)
  ├── Douglas and Company (polyhierarchical)
  ├── Nimmo's (polyhierarchical)
  ├── P. Mullany and Company
  ├── Peckman Bros/Brothers (polyhierarchical)
  ├── Tabrett and Company (polyhierarchical)
  ├── Store (polyhierarchical)
  └── retailer or store (generic singular)

commercial businesses > retailers and stores (lowercase)
  ├── Douglas and Company (polyhierarchical)
  ├── Nimmo's (polyhierarchical)
  ├── Peckman Brothers
  ├── Tabrett and Company (polyhierarchical)
  └── retailer or store
```

**Current entries (sample):**
```csv
Retailers and stores,Retailers and stores,hierarchy,parent=Commercial businesses
retailers and stores,retailers and stores,hierarchy,parent=commercial businesses

Store,Store,hierarchy,parent=commercial buildings
Store,Store,hierarchy,parent=Retailers and stores
Store,Store,hierarchy,parent=Commercial buildings

retailer or store,retailer or store,hierarchy,parent=retailers and stores

Douglas and Company,Douglas and Company,hierarchy,parent=retailers and stores
Douglas and Company,Douglas and Company,hierarchy,parent=Retailers and stores
```

**Issues:**
- Mixed approach: Some entries polyhierarchical, some only in one facet
- Capitalization inconsistency throughout
- "Store" appears in Commercial buildings without (building) qualifier
- Specific establishments (Douglas and Company, etc.) are polyhierarchical
- Violates leaf-node pattern: "Store" appears both as leaf and potentially used directly
- Missing disambiguation between shop premises and retail business operations

---

## Pattern Analysis

### Banks

**Expected dual-nature characteristics:**

**Building indicators:**
- Physical bank premises/branches
- Architectural features (bank buildings)
- Spatial references ("at the bank", "bank premises")

**Business/Organisation indicators:**
- Financial institution operations
- Banking services (deposits, loans, transactions)
- Corporate entity (governance, ownership)
- Business failures/mergers

**Domain knowledge:**
- Historical banks were both physical premises and financial institutions
- Banking crises involved both building closures and business failures
- Strong dual-nature expected (like hotels, public houses)

---

### Retailers and Stores

**Expected dual-nature characteristics:**

**Building indicators:**
- Shop premises, storefronts
- Commercial buildings for retail
- Spatial references ("at the store")
- Physical infrastructure

**Business indicators:**
- Retail operations (buying/selling)
- Business ownership (proprietors)
- Commercial transactions
- Business establishment/closure
- Inventory and stock

**Domain knowledge:**
- Retail establishments inherently dual-nature
- Historical newspaper mentions could reference premises OR business operations
- Similar pattern to hotels/public houses expected

---

## Comparison with Completed Entity Types

| Entity Type | Building % | Business/Org % | Both % | Current Structure |
|-------------|------------|----------------|--------|-------------------|
| Public Houses | 0% | 0% | 100% | ✅ Disambiguated |
| Churches | 29% | 29% | 42% | ✅ Disambiguated |
| Hotels | 43% | 25% | 32% | ✅ Disambiguated |
| Schools of Arts | 11.1% | 55.6% | 33.3% | ✅ Disambiguated |
| Boarding Houses | 12.5% | 50% | 37.5% | ✅ Disambiguated |
| Educational Schools | 17.2% | 58.6% | 24.1% | ✅ Disambiguated |
| **Banks** | **Unknown** | **Unknown** | **Unknown** | ⚠️ Polyhierarchical |
| **Retailers/Stores** | **Unknown** | **Unknown** | **Unknown** | ⚠️ Mixed approach |

---

## Issues Summary

### Banks

1. **Polyhierarchy without qualifiers** - Inconsistent with all completed entity types
2. **No plural parent** - Violates leaf-node pattern (should have "Banks" or "banks" parent)
3. **Capitalization duplication** - "Bank" and "bank" exist separately
4. **No specific establishments** - Generic only (no "Commercial Bank", "Savings Bank", etc.)
5. **No empirical classification** - Unknown distribution of building/business/both

### Retailers and Stores

1. **Mixed qualification approach** - Some polyhierarchical, some single-facet
2. **Capitalization chaos** - "Retailers and stores" vs "retailers and stores" both exist
3. **Specific establishments polyhierarchical** - Douglas and Company, Nimmo's, Peckman Bros, Tabrett and Company all appear in both facets without qualifiers
4. **"Store" polyhierarchical in buildings** - Appears in "commercial buildings" without qualifier
5. **Inconsistent leaf-node pattern** - Generic "Store" vs "retailer or store" both exist
6. **No empirical classification** - Unknown distribution of building/business/both

---

## Questions for User

### Strategic Questions

1. **Approach:** Should we apply the same NLU classification workflow to Banks and Retailers/Stores?
   - Extract mentions from Zotero
   - Classify with entity-classifier skill
   - Analyse pattern distribution
   - Make evidence-based disambiguation decision

2. **Scope:** Should we tackle both entity types together or separately?
   - Together: Efficient, can compare patterns
   - Separately: More thorough, clearer focus

3. **Specific establishments:** Should we search for specific named banks/retailers?
   - Examples: "Commercial Bank", "Savings Bank", "Bank of New South Wales"
   - Examples: Named retail businesses beyond those already tagged

### Technical Questions

4. **Search strategy for Banks:** What tags should we search?
   - "Bank" (capitalized)
   - "bank" (lowercase)
   - Should we search for specific bank names in full text?

5. **Search strategy for Retailers:** What tags should we search?
   - "Store" (capitalized)
   - "Retailers and stores"
   - "retailer or store"
   - Specific establishments (Douglas and Company, Nimmo's, Peckman Bros, Tabrett and Company)
   - All of the above?

6. **Expected pattern:** Based on your domain knowledge, do you expect:
   - Banks: Building-dominant, business-dominant, or dual-nature dominant?
   - Retailers: Building-dominant, business-dominant, or dual-nature dominant?

---

## Recommended Approach

### Option A: Full NLU Classification (Thorough)

1. **Extract mentions** for both entity types using script 38 (needs enhancement)
2. **Classify separately** using entity-classifier skill
3. **Analyse patterns** to determine building/business/both distribution
4. **Make evidence-based decision** on disambiguation
5. **Implement taxonomy changes** following established pattern
6. **Document specific establishments** found during analysis

**Pros:**
- Empirical evidence-based decision
- Follows proven methodology
- High confidence in results
- Discovers specific establishments

**Cons:**
- More time-intensive
- Requires sample size sufficient for pattern analysis
- May find very few items currently tagged

---

### Option B: Quick Review and Assume Disambiguation (Pragmatic)

1. **Assume dual-nature** based on domain knowledge
2. **Implement disambiguation immediately** without classification
3. **Structure:**
   - Banks: banks (buildings) / banks (businesses)
   - Retailers: retailers and stores (buildings) / retailers and stores (businesses)
4. **Clean up capitalization** inconsistencies
5. **Apply leaf-node pattern** consistently

**Pros:**
- Faster implementation
- Domain knowledge strongly suggests dual-nature
- Consistent with all other commercial entities

**Cons:**
- No empirical validation
- May miss nuances in how these entities are referenced
- Less rigorous audit trail

---

## Preliminary Recommendations

Based on established patterns, I recommend:

### For Banks:

**Proposed structure:**
```text
Built Environment > Commercial buildings > banks (buildings)
└── bank (building)

Agents > Businesses > Financial institutions > banks (businesses)
└── bank (business)
```

**Rationale:**
- Banks inherently dual-nature (physical branches + financial institutions)
- Consistent with hotels, public houses (commercial dual-nature entities)
- Clean leaf-node pattern with plural parent

---

### For Retailers and Stores:

**Proposed structure:**
```text
Built Environment > Commercial buildings > retailers and stores (buildings)
├── retailer or store (building)
├── Douglas and Company (building)
├── Nimmo's (building)
├── P. Mullany and Company (building)
├── Peckman Brothers (building)
└── Tabrett and Company (building)

Agents > Businesses > Commercial businesses > retailers and stores (businesses)
├── retailer or store (business)
├── Douglas and Company (business)
├── Nimmo's (business)
├── P. Mullany and Company (business)
├── Peckman Brothers (business)
└── Tabrett and Company (business)
```

**Rationale:**
- Retail establishments inherently dual-nature (shop premises + business operations)
- Specific establishments need both building and business qualifiers
- Consistent with hotels (specific establishments in both facets)
- Clean leaf-node pattern with singular generic leaf

---

## Next Steps (Awaiting User Decision)

**If Option A (Full NLU Classification):**
1. Enhance script 38 to support "banks" and "retailers" entity types
2. Extract mentions from Zotero
3. Run entity-classifier skill on both entity types
4. Generate classification reports
5. Implement taxonomy based on empirical findings

**If Option B (Assume Disambiguation):**
1. Create taxonomy implementation scripts for both entity types
2. Remove polyhierarchical entries
3. Add disambiguated (building)/(business) entries
4. Clean up capitalization inconsistencies
5. Document decision rationale

**Questions to resolve:**
- Which approach do you prefer (A or B)?
- Should we tackle both together or separately?
- Any specific bank or retailer names to search for?

---

**Review prepared:** 2025-11-16
**Awaiting user guidance**
