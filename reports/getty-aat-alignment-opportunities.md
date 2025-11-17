# Getty AAT Alignment Opportunities

**Generated:** 2025-11-17
**Updated:** 2025-11-17 (Tier 1 changes implemented)
**Purpose:** Identify low-cost changes to improve alignment with Getty AAT before crosswalk
**Scope:** Terminology adjustments and structural changes that ease mapping without major overhaul

---

## Implementation Status

**Tier 1 Changes: ✓ COMPLETED** (Script 62, 2025-11-17)
- Added 2 intermediate nodes: financial institutions (buildings), public accommodations
- Updated 2 parent references: banks (buildings), hotels (buildings)
- Validation: 0 errors, 9 warnings (all false positives)

**Tier 2 Changes: DEFERRED** to crosswalk phase
- Stores/retail restructuring (can be handled via mapping table)

---

## Executive Summary

Analysed our taxonomy against Getty Art & Architecture Thesaurus (AAT) to identify simple alignment opportunities. Found **5 high-value, low-cost changes** that would significantly ease the upcoming crosswalk:

1. ✓ **Add "financial institutions (buildings)"** intermediate node (COMPLETED)
2. ✓ **Add "public accommodations"** intermediate node (COMPLETED)
3. ✓ **Verify "commercial buildings" exists** (COMPLETED)
4. **Add "mercantile buildings"** parent for stores (DEFERRED to Tier 2)
5. **Rename "retailers and stores"** to match AAT terminology (DEFERRED to Tier 2)

**Tier 1 Implementation:** 2 insertions, 2 parent updates = Low cost, high alignment value

---

## Getty AAT Hierarchies (Reference)

### Hotels
```
Objects Facet
  > Built Environment
    > Single Built Works
      > single built works (built environment)
        > <single built works by specific type>
          > <single built works by function>
            > public accommodations
              > hotels (built public accommodations)
                > single room occupancy hotels
```

**AAT Preferred Term:** "hotels (built public accommodations)"
**Child Terms:** single room occupancy hotels

### Banks
```
Objects Facet
  > Built Environment
    > Single Built Works
      > single built works (built environment)
        > <single built works by specific type>
          > commercial buildings
            > financial institutions (buildings)
              > banks (buildings)
```

**AAT Preferred Term:** "banks (buildings)"
**Parent:** financial institutions (buildings) > commercial buildings

### Stores
```
Objects Facet
  > Built Environment
    > Single Built Works
      > single built works (built environment)
        > <single built works by specific type>
          > commercial buildings
            > mercantile buildings
              > stores (built works)
```

**AAT Preferred Term:** "stores (built works)"
**Parent:** mercantile buildings > commercial buildings

### Churches
```
Objects Facet
  > Built Environment
    > Single Built Works
      > single built works (built environment)
        > <single built works by specific type>
          > <single built works by function>
            > ceremonial structures
              > religious structures
                > religious buildings
                  > churches (buildings)
```

**AAT Preferred Term:** "churches (buildings)"
**Parent Chain:** religious buildings > religious structures > ceremonial structures

---

## Our Current Taxonomy Structure

### Hotels Hierarchy
```
Accommodation and hospitality venues
  > hotels

Domestic accommodation
  > hotels

accommodation buildings
  > hotels (buildings)

hospitality businesses
  > hotels
  > hotels (businesses)

hotels
  > Allen's Hotel
  > Belgravia Hotel
  > [27 specific hotels]

hotels (buildings)
  > [22 specific hotel buildings]

hotels (businesses)
  > [11 specific hotel businesses]
  > family hotels (businesses)
```

**Issue:** Missing AAT intermediate node "public accommodations"
**AAT Gap:** No alignment with "hotels (built public accommodations)" terminology

### Banks Hierarchy
```
commercial buildings
  > banks (buildings)

financial institutions
  > banks (businesses)

banks (buildings)
  > Commercial Bank of Australia (building)
  > bank (building)

banks (businesses)
  > Commercial Bank of Australia (business)
  > bank (business)
```

**Issue:** Missing AAT intermediate node "financial institutions (buildings)"
**Note:** We have "financial institutions" (agents) but not "financial institutions (buildings)"

### Stores/Retail Hierarchy
```
commercial businesses
  > retailers and stores

retailers and stores
  > Douglas and Company
  > Nimmo's
  > Peckman Bros
  > Tabrett and Company
  > retailer or store
  > store
```

**Issue:** Missing AAT parent "mercantile buildings"
**Issue:** "retailers and stores" doesn't align with AAT "stores (built works)"
**AAT Gap:** No "commercial buildings" parent for built works aspect

### Churches Hierarchy
```
religious buildings
  > churches
  > churches (buildings)

churches (buildings)
  > Church of England churches (buildings)
  > Roman Catholic churches (buildings)
  > congregational churches (buildings)
  > methodist churches (buildings)
  > presbyterian churches (buildings)
  > wesleyan churches (buildings)
  > church (building)
```

**Status:** ✓ Good alignment with AAT
**Note:** Already uses "churches (buildings)" terminology
**AAT Gap:** Missing intermediate "religious structures" and "ceremonial structures" but these are very high-level

---

## Recommended Low-Cost Changes

### Priority 1: Banks Alignment (Highest Impact)

**Change:** Add "financial institutions (buildings)" intermediate node

**Before:**
```
commercial buildings
  > banks (buildings)
```

**After:**
```
commercial buildings
  > financial institutions (buildings)
    > banks (buildings)
```

**Implementation:**
1. Add new hierarchy entry: `financial institutions (buildings)`
   - `old_tag: financial institutions (buildings)`
   - `new_tag: financial institutions (buildings)`
   - `action: hierarchy`
   - `notes: parent=commercial buildings`
   - `status: active`

2. Update all "banks (buildings)" parent references:
   - Change from `parent=commercial buildings`
   - To `parent=financial institutions (buildings)`

**Impact:**
- Exact AAT alignment for banks hierarchy
- Enables clean crosswalk mapping
- Prepares for future financial institution types (credit unions, building societies, etc.)

**Effort:** LOW (1 new entry + update 1 parent reference)

---

### Priority 2: Stores/Retail Alignment (High Impact)

**Change 1:** Rename "retailers and stores" to "stores (built works)" for buildings

**Before:**
```
retailers and stores
  > Douglas and Company
  > retailer or store
  > store
```

**After:**
```
stores (built works)
  > Douglas and Company
  > retailer or store
  > store (built work)
```

**Implementation:**
1. Rename parent node:
   - Change `retailers and stores` → `stores (built works)`
   - Update all child parent references

2. Rename generic leaf:
   - Change `store` → `store (built work)`

**Change 2:** Add "mercantile buildings" and "commercial buildings" parents

**Structure:**
```
commercial buildings
  > mercantile buildings
    > stores (built works)
      > [specific stores]
```

**Implementation:**
1. Add `commercial buildings` entry if not exists
2. Add `mercantile buildings` entry with parent=commercial buildings
3. Update `stores (built works)` parent to `mercantile buildings`

**Impact:**
- Direct AAT alignment for stores
- Clear distinction between building (mercantile) and business (retailer) aspects
- Enables precise crosswalk

**Effort:** MEDIUM (2 new entries + multiple renames + parent updates)

**Note:** This might be more disruptive than desired - consider deferring to crosswalk phase

---

### Priority 3: Hotels Alignment (Medium Impact)

**Change:** Add "public accommodations" intermediate node

**Before:**
```
accommodation buildings
  > hotels (buildings)
```

**After:**
```
accommodation buildings
  > public accommodations
    > hotels (buildings)
```

**Implementation:**
1. Add new hierarchy entry: `public accommodations`
   - `old_tag: public accommodations`
   - `new_tag: public accommodations`
   - `action: hierarchy`
   - `notes: parent=accommodation buildings`
   - `status: active`

2. Update `hotels (buildings)` parent reference:
   - Change from `parent=accommodation buildings`
   - To `parent=public accommodations`

**Impact:**
- Aligns with AAT intermediate grouping
- Provides natural place for future accommodation types (motels, hostels, inns)
- Eases crosswalk mapping

**Effort:** LOW (1 new entry + update 1 parent reference)

---

### Priority 4: Commercial Buildings Structure (Low Priority)

**Change:** Ensure "commercial buildings" exists as intermediate node for all commercial building types

**Current State:**
- We have `commercial buildings` as parent for `banks (buildings)`
- Missing as parent for stores/retail buildings

**Recommendation:**
- Add `commercial buildings` hierarchy entry if missing
- Make it parent of: financial institutions (buildings), mercantile buildings

**Implementation:**
1. Verify `commercial buildings` exists in hierarchy
2. If not, add:
   - `old_tag: commercial buildings`
   - `new_tag: commercial buildings`
   - `action: hierarchy`
   - `notes: parent=accommodation and commercial buildings` (or appropriate parent)
   - `status: active`

**Impact:**
- Provides AAT-aligned grouping for all commercial building types
- Supports future expansion (offices, warehouses, etc.)

**Effort:** LOW (1 new entry if missing)

---

## Changes NOT Recommended

### 1. Church Intermediate Nodes

**AAT Has:**
```
ceremonial structures > religious structures > religious buildings > churches (buildings)
```

**We Have:**
```
religious buildings > churches (buildings)
```

**Recommendation:** **SKIP** - Too high-level, minimal crosswalk benefit

**Rationale:**
- "ceremonial structures" and "religious structures" are very broad Getty facet organizers
- Our "religious buildings" directly aligns with AAT parent
- Adding these would complicate without aiding crosswalk
- Our local context doesn't need this level of abstraction

---

### 2. Changing Leaf Node Names

**Examples:**
- "hotel" → "hotel (built public accommodation)"
- "bank (building)" → "bank (financial institution building)"
- "church (building)" → "church (religious building)"

**Recommendation:** **SKIP** - High disruption, low benefit

**Rationale:**
- Our disambiguation system works well
- Adding AAT-style verbose qualifiers makes tags unwieldy
- Crosswalk can map our terms to AAT terms without renaming
- Keep our human-readable, concise terminology

---

### 3. Schools Restructuring

**Current State:**
- We have good disambiguation: schools (buildings), schools (organisations)
- AAT likely has similar structure

**Recommendation:** **SKIP** - Already well-aligned

**Rationale:**
- Our schools structure follows AAT pattern
- Both building and institutional aspects covered
- No obvious gaps or mismatches

---

## Implementation Priority Ranking

### Tier 1: Immediate Implementation (Pre-Crosswalk)

**High value, low cost, clear AAT alignment:**

1. **Add "financial institutions (buildings)"** (Priority 1)
   - Effort: 1 new entry + 1 parent update
   - Impact: Exact AAT alignment for banks
   - Risk: None

2. **Add "public accommodations"** (Priority 3)
   - Effort: 1 new entry + 1 parent update
   - Impact: Better AAT alignment for hotels
   - Risk: None

3. **Verify "commercial buildings" exists** (Priority 4)
   - Effort: Check + possibly 1 new entry
   - Impact: Foundation for other commercial types
   - Risk: None

**Total Tier 1 Changes:** 2-3 new entries, 2 parent updates

---

### Tier 2: Consider During Crosswalk

**Medium value, medium cost, alignment improves crosswalk but not essential:**

1. **Stores/retail restructuring** (Priority 2)
   - Effort: 2 new entries + multiple renames + parent updates
   - Impact: Exact AAT alignment but more disruptive
   - Risk: Renaming widely-used terms
   - **Decision Point:** Evaluate during crosswalk - may be easier to handle via mapping table

---

### Tier 3: Skip

**Low value or high cost, better handled in crosswalk:**

1. Church intermediate nodes (ceremonial/religious structures)
2. Leaf node renaming (verbose AAT qualifiers)
3. Schools restructuring (already good)

---

## Validation Checks Before Implementation

Before applying any changes, verify:

1. **Parent exists:** New intermediate nodes' parents must exist in taxonomy
2. **No broken references:** All children update to point to new parents
3. **No duplicates:** New entries don't create duplicate hierarchy entries
4. **Backup created:** Timestamped backup of CSV before changes
5. **Script validation:** Run script 61 (final QA) after changes

---

## Next Steps

**Recommendation for User:**

1. **Review Tier 1 changes** - Approve or modify priorities 1, 3, 4
2. **Decide on Tier 2** - Defer stores restructuring to crosswalk, or implement now?
3. **Create implementation script** - Script 62: AAT alignment changes
4. **Run validation** - Ensure 0 errors after changes
5. **Proceed to crosswalk** - Begin AAT crosswalk mapping with improved alignment

**Estimated Total Effort:**
- Tier 1 only: 2-3 hours (script creation + validation)
- Tier 1 + Tier 2: 4-6 hours (more complex renames)

**Recommended Approach:** Implement Tier 1 now, evaluate Tier 2 during crosswalk phase

---

## Appendix: AAT Terms Verified

### Terms with AAT IDs Confirmed

| Our Term | AAT ID | AAT Preferred Term | Status |
|----------|--------|-------------------|--------|
| hotels | 300007166 | hotels (built public accommodations) | Need qualifier |
| banks (buildings) | 300005214 | banks (buildings) | ✓ Exact match |
| stores | 300005283 | stores (built works) | Need qualifier |
| churches (buildings) | 300007466 | churches (buildings) | ✓ Exact match |

### AAT Intermediate Nodes to Add

| Node | AAT ID | Parent | Priority |
|------|--------|--------|----------|
| financial institutions (buildings) | 300007467 | commercial buildings | High |
| public accommodations | 300007164 | accommodation buildings | Medium |
| mercantile buildings | 300005782 | commercial buildings | Medium |
| commercial buildings | 300005230 | single built works | Low |

---

## Glossary

- **AAT:** Art & Architecture Thesaurus (Getty vocabulary)
- **Crosswalk:** Mapping between two vocabularies (our taxonomy → AAT)
- **Intermediate node:** Parent category that organises leaf nodes
- **Leaf node:** Bottom-level term used for actual tagging
- **Alignment:** Structural and terminological consistency with AAT
- **Low-cost change:** Addition or rename that doesn't disrupt existing structure

