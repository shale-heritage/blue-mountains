# Dual-Nature Entity Classification Audit

**Date:** 2025-11-13
**Purpose:** Assess which entity types need classification workflow (like hotels) vs spot-check validation

---

## Methodology

Review taxonomy (`data/tag_map_consolidated.csv`) to identify:
1. Entities already disambiguated with (building)/(organisation) or (building)/(business) qualifiers
2. Entities using polyhierarchy without disambiguation
3. Entities that may need classification but aren't yet structured

---

## CATEGORY 1: Entities with Disambiguation Qualifiers (COMPLETE)

### 1.1 Churches - WELL STRUCTURED ✓

**Status:** Manual classification already complete

**Structure:** Uses (building) and (organisation) disambiguation qualifiers

**Statistics:**
- Total unique church tags: 83
- Building tags: 24
- Organisation tags: 24
- Entities with both aspects: 17
- Unqualified tags: 35 (hierarchy parents and synonyms)

**Examples of entities with both aspects:**
- Church of England Katoomba (building) + (organisation)
- Methodist Church (building) + (organisation)
- St Hilda's Church of England (building) + (organisation)
- Congregational Church (building) + (organisation)
- Roman Catholic Church (building) + (organisation)
- Presbyterian Church Leura (building) + (organisation)

**Hierarchy structure:**
```
Built Environment > Churches (buildings) > [denomination] churches (buildings)
Agents > Organisations > Religious organisations > Churches (organisations) > [denomination] churches (organisations)
```

**Validation needed:** SPOT-CHECK only (manual work already done)

---

### 1.2 Hotels - STRUCTURED AND VALIDATED ✓

**Status:** Phase 6 complete (NLU classification + user review)

**Structure:** Uses (building) and (business) disambiguation qualifiers

**Statistics:**
- Total unique hotel tags: 19
- Building tags: 10
- Business tags: 9
- Entities with both aspects: 8
- Application CSV: 49 tag applications for 37 items ready

**Examples:**
- Megalong Hotel (building) + (business)
- Carrington Hotel (building) + (business)
- Katoomba Family Hotel (building) + (business)

**Hierarchy structure:**
```
Built Environment > Accommodation buildings > hotels (buildings)
Agents > Organisations > Hospitality businesses > hotels (businesses)
```

**Validation needed:** COMPLETE

---

### 1.3 Boarding Houses - STRUCTURED, NOT VALIDATED

**Status:** Taxonomy structure exists, but NO item-level classification done

**Structure:** Uses (building) and (business) disambiguation qualifiers

**Statistics from taxonomy:**
- Generic tags exist:
  - boarding house (building) → parent: boarding houses (buildings)
  - boarding house (business) → parent: boarding houses (businesses)
- Specific entities:
  - Orama Boarding House (building)
  - Orama Boarding House (business)
- Hierarchy parents:
  - boarding houses (buildings) → parent: accommodation buildings
  - boarding houses (businesses) → parent: hospitality businesses

**Validation needed:** HOTELS-STYLE NLU WORKFLOW
- Extract boarding house mentions from Zotero items
- Classify each mention as building/business/both
- User review and validation
- Generate application CSV

---

## CATEGORY 2: Entities Using Polyhierarchy WITHOUT Disambiguation

### 2.1 Halls and Fraternal Lodges - POLYHIERARCHICAL

**Status:** Structured using polyhierarchy, but NO disambiguation qualifiers

**Current approach:** Same tag name appears under multiple hierarchy parents

**Examples:**
- `Masonic Hall` appears under:
  - Built Environment > Community buildings > halls
  - (No organisation parent currently visible)
- `Odd Fellows' Hall` appears under:
  - Built Environment > Community buildings > halls
- `Independent Order of Odd Fellows` appears under:
  - Agents > Organisations > Lodges

**Key observation:**
The BUILDINGS (halls) and ORGANISATIONS (lodges/fraternal orders) are currently SEPARATE entities in the taxonomy:
- **Halls** = Physical buildings (Masonic Hall, Odd Fellows' Hall, Clarke's Hall, etc.)
- **Lodges** = Organisations (Independent Order of Odd Fellows, United Ancient Order of Druids)

**Validation needed:** SPOT-CHECK
- Check if this separation is historically accurate
- Verify that "Masonic Hall" refers to building only, not organisation
- Verify that "Independent Order of Odd Fellows" refers to organisation only
- Check if any contexts show dual-nature usage

---

### 2.2 Schools of Arts - POLYHIERARCHICAL

**Status:** Uses polyhierarchy WITHOUT disambiguation qualifiers

**Current structure:**
- `School of Arts` appears under:
  - Agents > Organisations > Cultural societies > Schools of Arts
  - Built Environment > Community buildings > Halls > Schools of Arts
- `Katoomba School of Arts` appears under:
  - Agents > Organisations > Cultural societies > Schools of Arts
  - Built Environment > Community buildings > Halls > Schools of Arts

**Key observation:**
This follows the "polyhierarchy" approach where the SAME TAG NAME appears in multiple facets without qualifiers like (building) or (organisation).

**Validation needed:** HOTELS-STYLE NLU WORKFLOW
- Extract Schools of Arts mentions
- Classify building vs organisation vs both
- Determine if polyhierarchy is appropriate or if disambiguation needed
- Inform dual-nature strategy decision (TODO.md lines 42-140)

---

## CATEGORY 3: Entities Needing Classification (Not Yet Structured)

### 3.1 Schools (Educational Institutions)

**Status:** NOT FOUND IN TAXONOMY with building/organisation disambiguation

**Search results:** No tags found matching "School (building)" or "School (organisation)"

**Hypothesis:** Educational schools may not yet be classified as dual-nature entities

**Validation needed:**
1. Search for school-related tags in taxonomy
2. Extract school mentions from Zotero
3. Determine if building/organisation distinction needed
4. Run HOTELS-STYLE NLU WORKFLOW if needed

---

### 3.2 Other Potential Dual-Nature Entities

**To investigate:**
- Public houses/pubs (building vs business)
- Shops/stores (building vs business)
- Banks (building vs organisation)
- Post offices (building vs organisation)
- Courthouses (building vs organisation)
- Libraries (building vs organisation)
- Fire stations (building vs organisation)

---

## Summary Table

| Entity Type | Structure | Status | Validation Needed |
|-------------|-----------|--------|-------------------|
| **Churches** | (building)/(organisation) qualifiers | ✓ Manual complete | Spot-check only |
| **Hotels** | (building)/(business) qualifiers | ✓ NLU Phase 6 complete | COMPLETE |
| **Boarding Houses** | (building)/(business) qualifiers | Structure exists | Hotels-style NLU workflow |
| **Halls/Lodges** | Polyhierarchy OR separate entities | Unclear | Spot-check to clarify approach |
| **Schools of Arts** | Polyhierarchy (no qualifiers) | Structure exists | Hotels-style NLU workflow |
| **Schools (educational)** | Unknown | Not found | Search + hotels-style NLU if needed |
| **Public houses** | Unknown | Not checked | TBD |
| **Shops/Stores** | Unknown | Not checked | TBD |

---

## Recommended Next Steps

### Priority 1: Clarify Halls/Lodges Structure

**Question:** Are halls and lodges already correctly separated (buildings separate from organisations), or do they need dual-nature classification?

**Method:** Spot-check sample of contexts

**Examples to check:**
- "Meeting held at Masonic Hall" → building
- "Masonic Hall announced new members" → organisation (?)
- "Odd Fellows' Hall" → building or organisation?

### Priority 2: Schools of Arts Classification

**Action:** Run hotels-style NLU workflow
- Extract mentions
- Classify building vs organisation vs both
- Determine if polyhierarchy is working or if disambiguation needed

**Strategic importance:** This will inform the dual-nature entity strategy decision (TODO.md)

### Priority 3: Boarding Houses Classification

**Action:** Run hotels-style NLU workflow
- Similar to hotels (accommodation + business)
- Should be straightforward with hotels template

### Priority 4: Educational Schools

**Action:**
1. Search taxonomy for school-related tags
2. If found without dual-nature structure, run NLU workflow
3. If not found, determine if schools need to be added

---

## Questions for User

1. **Halls vs Lodges:** Did you manually separate building entities (halls) from organisation entities (lodges/fraternal orders), or should they be dual-nature with both aspects?

2. **Schools of Arts:** Should we validate the polyhierarchy approach (same tag in multiple facets) or move to disambiguation qualifiers like churches?

3. **Priority order:** Which entity types should we tackle first after this audit?

---

**Generated:** 2025-11-13
**Next action:** Present to user for clarification on halls/lodges and priority order
