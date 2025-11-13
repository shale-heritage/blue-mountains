# Existing Hotel Taxonomy Inventory

**Date:** 2025-11-13
**Source:** `data/tag_map_consolidated.csv`
**Purpose:** Phase 1 - Inventory existing hotel tags before proposing new ones

---

## Executive Summary

**Key Findings:**
1. ✅ Parent categories exist: `hotels (buildings)` and `hotels (businesses)`
2. ✅ All 13 specific hotel (building) tags exist for entities in our analysis
3. ❌ **NO specific hotel (business) tags exist yet** - only the parent category
4. ✅ Singular generic terms exist: `hotel (building)` and `family hotel (building)`
5. ✅ Standardisation exists: "Family Hotel" → "Katoomba Family Hotel" (synonym)

**Implication:** The 9 proposed hotel (business) tags from NLU analysis are genuinely needed - none exist yet.

---

## Taxonomy Structure

### Parent Categories (Organisational Nodes)

#### Built Environment Facet

```
accommodation buildings
└── hotels (buildings)
    └── family hotels
```

**Notes:**
- `hotels (buildings)` - Line 501: Parent for all hotel building entities
- `family hotels` - Line 376: Parent for family hotel buildings (sub-category of hotels)
- These are polyhierarchical: also appear under thematic categories:
  - `hotels` → `Alcohol-related venues - THEMATIC` (Line 498)
  - `hotels` → `Domestic accommodation - THEMATIC` (Line 499)

#### Agents Facet

```
commercial businesses
└── hospitality businesses
    ├── hotels (businesses)
    └── boarding houses (businesses)
```

**Notes:**
- `hotels (businesses)` - Line 502: Parent for hotel business entities
- Currently has **NO children** - no specific hotel business tags exist yet

---

## Singular Generic Terms (Leaf Nodes)

### Building Terms

1. **`hotel (building)`** - Line 492
   - Parent: `hotels (buildings)`
   - Also: Parent: `accommodation buildings` (Line 493)
   - Purpose: Singular generic term for unspecified hotel buildings
   - Status: ✅ EXISTS

2. **`family hotel (building)`** - Line 375
   - Parent: `family hotels`
   - Purpose: Singular generic term for unspecified family hotels
   - Status: ✅ EXISTS

### Business Terms

**Status:** ❌ NO singular generic business term exists yet
**Needed:** `hotel (business)` - singular generic for unspecified hotel businesses

---

## Specific Named Hotel (Building) Tags

All specific hotel buildings from our NLU analysis **already exist**:

| Tag | Line | Parent | Synonym Mapping |
|-----|------|--------|-----------------|
| Belgravia Hotel (building) | 95 | hotels (buildings) | "Belgravia Hotel" → qualified (Line 94) |
| Carrington Hotel (building) | 135 | hotels (buildings) | "Carrington Hotel" → qualified (Line 134) |
| Centennial Hotel (building) | 142 | hotels (buildings) | "Centennial Hotel" → qualified (Line 141) |
| Comet Hotel (building) | 191 | hotels (buildings) | - |
| Falls Hotel (building) | 368 | hotels (buildings) | - |
| Grand Hotel (Sydney) (building) | 435 | hotels (buildings) | "Grand Hotel" → Sydney variant (Lines 433-434) |
| Great Western Hotel (building) | 437 | hotels (buildings) | - |
| Hotel Wentworth (building) | 495 | hotels (buildings) | - |
| Imperial Hotel (building) | 511 | hotels (buildings) | "Imperial Hotel" → qualified (Line 510) |
| Katoomba Hotel (building) | 569 | hotels (buildings) | "Katoomba Hotel" → qualified (Line 568) |
| Megalong Hotel (building) | 681 | hotels (buildings) | "Megalong Hotel" → qualified (Line 680) |
| Mount Victoria Hotel (building) | 803 | hotels (buildings) | "Mount Victoria Hotel" → qualified (Line 802) |
| Railway Hotel (building) | 1251 | hotels (buildings) | "Railway Hotel" → qualified (Line 1250) |
| Wentworth Falls Hotel (building) | 1570 | hotels (buildings) | "Wentworth Falls Hotel" → qualified (Line 1569) |

**Family Hotels (Sub-category):**

| Tag | Line | Parent | Notes |
|-----|------|--------|-------|
| Katoomba Family Hotel (building) | 566 | family hotels | Preferred term (Line 565) |
| Delaney's Family Hotel (building) | 298 | family hotels | - |
| Fryer's Family Hotel (building) | 405 | family hotels | Historical ownership period |

**Accommodation Houses:**

| Tag | Line | Parent | Notes |
|-----|------|--------|-------|
| Hoffman's House (building) | 469 | hotels (buildings) | - |
| Montrose House (building) | 794 | hotels (buildings) | - |

---

## Specific Named Hotel (Business) Tags

**Status:** ❌ **NONE EXIST**

The following specific hotel (business) tags are **missing** and correspond to the 9 hotels identified in NLU analysis as having business contexts:

1. **Belgravia Hotel (business)** - Not found
2. **Carrington Hotel (business)** - Not found
3. **Centennial Hotel (business)** - Not found
4. **Imperial Hotel (business)** - Not found
5. **Katoomba Family Hotel (business)** - Not found
6. **Megalong Hotel (business)** - Not found
7. **Mount Victoria Hotel (business)** - Not found
8. **Wentworth Falls Hotel (business)** - Not found
9. **Family hotel (business)** - Not found (generic singular term)

---

## Synonym and Merge Relationships

### Standardisation: Family Hotel Variants

**Primary finding:** "Family Hotel" is standardised to "Katoomba Family Hotel"

1. **Line 374:** `Family Hotel` → `Katoomba Family Hotel` (synonym)
   - Rationale: "Case variant - standardise to lowercase 'family hotel' or use specific 'Katoomba Family Hotel'"

2. **Line 373:** `family hotel` → merge
   - Rationale: "Colloquial/generic reference to Katoomba family hotel - all instances in collection refer to this specific establishment in Katoomba"

3. **Line 403:** `Fryer's Family Hotel` → merge (use Katoomba Family Hotel)
   - Rationale: "Owner-specific name for Katoomba family hotel during Fryer family ownership (1892)"

4. **Line 404:** `Fryer's Family Hotel` → `Katoomba Family Hotel` (synonym)
   - Rationale: "Historical name used during Fryer family ownership period (pre-March 1892)"

**Implication:** When creating business variant, should we create:
- `Katoomba Family Hotel (business)` (following standardisation), OR
- `family hotel (business)` (generic singular term)?

**Recommendation:** Create BOTH:
- `family hotel (business)` - singular generic for unspecified family hotel businesses
- `Katoomba Family Hotel (business)` - specific named entity
- Map "Family Hotel" → "Katoomba Family Hotel (business)" as synonym

---

### Unqualified Variants → Qualified (Building) Forms

All unqualified hotel names map to qualified (building) variants:

| Unqualified | Maps To | Relationship |
|-------------|---------|--------------|
| Belgravia Hotel | Belgravia Hotel (building) | synonym |
| Carrington Hotel | Carrington Hotel (building) | synonym |
| Centennial Hotel | Centennial Hotel (building) | synonym |
| Imperial Hotel | Imperial Hotel (building) | synonym |
| Katoomba Hotel | Katoomba Hotel (building) | synonym |
| Katoomba Family Hotel | Katoomba Family Hotel (building) | synonym |
| Megalong Hotel | Megalong Hotel (building) | synonym |
| Mount Victoria Hotel | Mount Victoria Hotel (building) | synonym |
| Railway Hotel | Railway Hotel (building) | synonym |
| Wentworth Falls Hotel | Wentworth Falls Hotel (building) | synonym |

**Implication:** When we create (business) variants, should unqualified forms map to:
- (building) only (current state), OR
- Both (building) AND (business)?

**Recommendation:** Depends on usage context analysis. If most mentions are ambiguous (could be either), unqualified should map to BOTH. If building-dominant, keep current mapping.

---

### Possessive Forms → Hotel + Hotellier

Several possessive forms are merged to generic "hotel" + specific hotellier:

| Possessive Form | Maps To | Relationship | Line |
|----------------|---------|--------------|------|
| Allen's Hotel | hotel | merge | 43 |
| Brown's Hotel | hotel | merge | 122 |
| Mrs Long's Hotel | hotel | merge | 1086 |

**Rationale:** "Possessive form referring to hotel run by [name] (hotellier) - tag as Hotel + [name]"

**Implication:** These should be tagged with:
- `hotel (building)` or `hotel (business)` (depending on context)
- Plus the specific hotellier name (e.g., "Mrs Long")

---

## Hotelliers (Hotel Proprietors)

A comprehensive list of hotelliers exists (parent: `hotelliers`, line 497):

**Examples:**
- Allen (Line 42)
- Bashford (Line 89)
- Biles (Line 101)
- Brown (Line 121)
- F C Goyder / F. C. Goyder (Lines 366-367)
- Isabellea J Long / Isabellea J. Long (Lines 529-530)
- Mrs Long (Line 1085)
- Richard Allen (Line 1306)
- Rubina Fryer (Line 1330)
- And many more...

**Implication:** When hotel business contexts mention proprietors, we should tag with:
- The specific hotel (business) tag
- The specific hotellier tag (if identified)

---

## Licensing Category

**Line 494:** `hotel licensing` exists
- Parent: `licensing`
- Purpose: For licensing-specific contexts (applications, renewals, violations)

**Implication:** Licensing contexts in our NLU analysis should be tagged with:
- The specific hotel (business) tag (the entity being licensed)
- `hotel licensing` (the activity/process)

---

## Geographic Disambiguation

**Grand Hotel:** All instances disambiguated to Sydney location
- **Line 433:** `Grand Hotel` → `Grand Hotel (Sydney)` (synonym)
- **Line 434:** `Grand Hotel` → `Grand Hotel (Sydney)` (merge)
- **Rationale:** "Primary source evidence shows Grand Hotel refers to Phillip Street Sydney hotel"

**Note:** In our NLU analysis, "Grand Hotel" had only 1 mention (building-only). This is the Sydney hotel, not a Blue Mountains hotel.

---

## Missing Tags: Taxonomy Gaps

Based on inventory, the following tags need to be created:

### 1. Singular Generic Business Term

**Tag:** `hotel (business)`
- **Parent:** `hotels (businesses)`
- **Purpose:** Singular generic term for unspecified hotel businesses
- **Justification:** Matches pattern of `hotel (building)` for building facet
- **Priority:** HIGH - needed for consistent taxonomy structure

**Tag:** `family hotel (business)`
- **Parent:** `hotels (businesses)` (or create `family hotels (businesses)` sub-category?)
- **Purpose:** Singular generic term for unspecified family hotel businesses
- **Justification:** Matches pattern of `family hotel (building)`
- **Priority:** MEDIUM - needed if family hotel business contexts are generic

---

### 2. Specific Named Hotel (Business) Tags

Based on NLU analysis, the following 9 specific hotel (business) tags are needed:

#### High Priority (Multiple Business/Both Mentions)

1. **`Megalong Hotel (business)`**
   - NLU: 8 mentions (3 business, 3 building, 2 both)
   - Contexts: Licensing (2), advertisements (2), licensee testimony (1), business closure (1)
   - Justification: Substantial business agency and operations

2. **`Katoomba Family Hotel (business)`**
   - NLU: 6 mentions as "Family hotel" (4 business, 2 both)
   - Contexts: Proprietorship (4), room rental (2)
   - Justification: Strong business operations, follows standardisation to "Katoomba Family Hotel"
   - **Note:** Need to decide: Create as "Katoomba Family Hotel (business)" or "family hotel (business)"?

3. **`Centennial Hotel (business)`**
   - NLU: 5 mentions (3 business, 1 building, 1 both)
   - Contexts: Property sale (1), licensing violation (1), proprietor testimony (2), polling location (1)
   - Justification: Strong business contexts

4. **`Carrington Hotel (business)`**
   - NLU: 4 mentions (1 business, 1 building, 2 both)
   - Contexts: Licensing renewal (1), assault with proprietor (2)
   - Justification: Licensing + proprietor involvement

#### Medium Priority (2-3 Business Mentions)

5. **`Imperial Hotel (business)`**
   - NLU: 3 mentions (1 business, 2 building)
   - Contexts: License transfer (1)
   - Justification: Business asset transfer

6. **`Wentworth Falls Hotel (business)`**
   - NLU: 2 mentions (2 business)
   - Contexts: Business advertising (1), business sale (1)
   - Justification: Only appears in business contexts

7. **`Mount Victoria Hotel (business)`**
   - NLU: 2 mentions (2 business)
   - Contexts: Licensee identification (1), proprietor catering (1)
   - Justification: Only appears in business contexts

8. **`Belgravia Hotel (business)`**
   - NLU: 2 mentions (1 business, 1 building)
   - Contexts: License renewal (1)
   - Justification: Licensing context

#### Lower Priority (1 Business Mention)

9. **`Katoomba Family Hotel (business)`**
   - NLU: 1 mention (1 business)
   - Contexts: Business investment decision (1)
   - Justification: Business agency (lessee making improvements)
   - **Note:** This is distinct from generic "family hotel" mentions above if those refer to Katoomba Family Hotel specifically

---

## Entities Remaining Building-Only

The following hotels from our NLU analysis do **NOT** need (business) variants:

1. **Katoomba Hotel (building)** - 3 mentions (all building)
   - Contexts: Spatial landmarks, inquest venue, preaching location
   - Status: ✅ EXISTS (Line 569)

2. **Railway Hotel (building)** - 2 mentions (all building)
   - Contexts: Meeting venue, gaming house location
   - Status: ✅ EXISTS (Line 1251)

3. **Grand Hotel (Sydney) (building)** - 1 mention (building)
   - Context: Future establishment location reference
   - Status: ✅ EXISTS (Line 435)

4. **Montrose House (building)** - 4 mentions (all building)
   - Contexts: Police department rental, court venue, spatial landmark
   - Status: ✅ EXISTS (Line 794)
   - Note: Used as government facility, not hotel operations

---

## Questions for User Review

### 1. Family Hotel Standardisation

Our NLU analysis found 6 mentions of generic "Family hotel" (lowercase, unspecified). Per lines 373-374, these should map to "Katoomba Family Hotel" as the standardised term.

**Question:** Should we create:
- **Option A:** `family hotel (business)` (generic singular term, parallel to `family hotel (building)`)
- **Option B:** `Katoomba Family Hotel (business)` (specific entity, following standardisation)
- **Option C:** Both (generic + specific)

**Recommendation:** Option C - Create both:
- `family hotel (business)` for generic/unspecified contexts
- `Katoomba Family Hotel (business)` for specific contexts
- Map "Family Hotel" → "Katoomba Family Hotel (business)" as synonym

---

### 2. Unqualified Variant Mapping

Currently, unqualified forms (e.g., "Carrington Hotel") map ONLY to (building) variants.

**Question:** When we create (business) variants, should unqualified forms:
- **Option A:** Continue mapping only to (building) - forces explicit disambiguation
- **Option B:** Map to BOTH (building) AND (business) - allows polyhierarchical tagging
- **Option C:** Depend on context analysis (if building-dominant, keep building-only)

**Recommendation:** Option C - Analyse actual usage in Zotero collection:
- If mostly ambiguous/mixed → map to both
- If clearly building-dominant → keep building-only
- Phase 2 (item-by-item analysis) will inform this decision

---

### 3. Family Hotels Sub-Category

Currently `family hotels` exists as a sub-category under `hotels (buildings)`.

**Question:** Should we create a parallel sub-category for business facet?
- **Option A:** Create `family hotels (businesses)` under `hotels (businesses)`
- **Option B:** Place family hotel businesses directly under `hotels (businesses)`

**Recommendation:** Option A for consistency - mirror the structure:
```
hotels (businesses)
└── family hotels (businesses)
    ├── family hotel (business)
    ├── Katoomba Family Hotel (business)
    ├── Delaney's Family Hotel (business)
    └── Fryer's Family Hotel (business)
```

---

### 4. Possessive Forms with Business Contexts

Lines 43, 122, 1086 show possessive forms (Allen's Hotel, Brown's Hotel, Mrs Long's Hotel) merge to generic "hotel" + hotellier name.

**Question:** If these possessive forms appear in business contexts, should they map to:
- **Option A:** `hotel (business)` + hotellier name
- **Option B:** Create specific tags (e.g., "Allen's Hotel (business)")
- **Option C:** Depends on whether these were distinct businesses vs. informal references

**Recommendation:** Option A - maintain merge pattern, tag with:
- `hotel (business)` or `hotel (building)` (depending on context)
- Plus specific hotellier tag (e.g., "Allen", "Mrs Long")

---

## Summary Statistics

### Existing Tags

| Category | Count | Status |
|----------|-------|--------|
| Parent categories (building) | 2 | ✅ Complete |
| Parent categories (business) | 1 | ✅ Complete (no children yet) |
| Singular generic (building) | 2 | ✅ Complete |
| Singular generic (business) | 0 | ❌ Missing |
| Specific hotels (building) | 17 | ✅ Complete (all needed entities exist) |
| Specific hotels (business) | 0 | ❌ Missing (9 needed) |
| Hotelliers | 30+ | ✅ Complete |
| Synonym mappings | 15+ | ✅ Extensive |

### Tags to Create

| Category | Count | Priority |
|----------|-------|----------|
| Singular generic business terms | 2 | HIGH (hotel, family hotel) |
| Specific hotel (business) tags | 9 | HIGH (based on NLU evidence) |
| Family hotels (businesses) sub-category | 1 | MEDIUM (structural consistency) |
| **Total new tags** | **12** | |

---

## Next Steps

1. **User Review:**
   - Approve/modify proposed new tags (9 specific + 2 generic + 1 sub-category)
   - Answer questions about family hotel standardisation
   - Decide on unqualified variant mapping strategy
   - Confirm sub-category structure for family hotels

2. **Phase 2:**
   - Create item-by-item tag mapping proposal
   - Show which Zotero items get which tags (building/business/both)
   - Provide evidence from context excerpts

3. **Phase 3:**
   - Generate final taxonomy gaps analysis
   - Format new tag entries for CSV insertion
   - Prepare validation workflow

---

## Validation

**Data Integrity Checks:**
- ✅ All 13 specific hotel buildings from NLU analysis exist in taxonomy
- ✅ Parent categories exist for both building and business facets
- ✅ Singular generic building terms exist
- ✅ Synonym mappings are comprehensive
- ✅ No unexpected hotel business tags found (confirms gap analysis)

**Cross-Reference:**
- Source: `data/tag_map_consolidated.csv`
- Lines referenced: 42-1570 (hotel-related entries)
- Total hotel-related lines: ~90 entries
- Grep pattern: `(?i)hotel` matched 88 lines

---

**Phase 1 Status:** ✅ COMPLETE

**Ready for Phase 2:** Yes - proceed to item-by-item tag mapping proposal
