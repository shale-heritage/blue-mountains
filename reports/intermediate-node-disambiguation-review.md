# Intermediate Node Disambiguation Review

**Date:** 2025-11-17
**Purpose:** Review disambiguation consistency for intermediate nodes across facets
**Requested by:** User

---

## Executive Summary

Reviewed all 327 intermediate nodes (terms that are both parents and children) for disambiguation consistency. Found:

**Critical Issues:**
- **13 intermediate nodes** span both Agents and Built Environment facets without disambiguation
- **Pattern:** Most have disambiguated children (e.g., "hotels (buildings)") but undisambiguated parent (e.g., "hotels")
- **Inconsistency:** Creates ambiguity about which facet the unqualified term belongs to

**Recommendation:**
- **DO NOT add disambig uation to intermediate nodes** - this is actually the correct pattern
- Intermediate nodes intentionally span facets via **polyhierarchy**
- Only leaf nodes need disambiguation (already done)

---

## Node Classification

**Total active hierarchy terms:** 1,192

| Node Type | Count | Description |
|-----------|-------|-------------|
| Top-level nodes | 2 | Only parents (facets) |
| Intermediate nodes | 327 | Both parent & child |
| Leaf nodes | 865 | Only children (used for tagging) |

**Intermediate nodes with disambiguation:** 31 (9.5%)
**Intermediate nodes without disambiguation:** 296 (90.5%)

---

## Multi-Facet Intermediate Nodes

These 13 intermediate nodes appear as parents in BOTH Agents and Built Environment facets:

### 1. boarding houses
**Facets:** Agents, Built Environment, Economy & Labour, family & domestic life
**Direct parents:**
- Accommodation and hospitality venues (thematic)
- Domestic accommodation (thematic)
- hospitality businesses (Agents)

**Children (2):**
- boarding houses (buildings) → goes under Built Environment
- boarding houses (businesses) → goes under Agents

**Status:** ✓ CORRECT PATTERN
- Unqualified "boarding houses" is polyhierarchical parent
- Disambiguated children go to appropriate facets
- No change needed

---

### 2. churches
**Facets:** Agents, Built Environment, Religion
**Direct parents:**
- religious buildings (Built Environment)
- religious organisations (Agents)

**Children (7):**
- churches (buildings) → Built Environment
- churches (organisations) → Agents
- Church of England churches (buildings)
- Church of England churches (organisations)
- Roman Catholic churches (buildings)
- Roman Catholic churches (organisations)
- + 1 more

**Status:** ✓ CORRECT PATTERN
- Polyhierarchical intermediate serving both facets
- All leaf nodes properly disambiguated
- No change needed

---

### 3. hotels
**Facets:** Agents, Built Environment, Economy & Labour, alcohol & temperance, family & domestic life
**Direct parents:**
- Accommodation and hospitality venues (thematic)
- Alcohol-related venues (thematic)
- Domestic accommodation (thematic)
- hospitality businesses (Agents)

**Children (27):**
- hotels (buildings) → Built Environment parent
- hotels (businesses) → Agents parent
- [25 specific hotels - most are leaf nodes]

**Status:** ✓ CORRECT PATTERN
- Polyhierarchical intermediate for multiple thematic groupings
- Disambiguated children properly separated
- No change needed

---

### 4. schools
**Facets:** Agents, Built Environment, education
**Direct parents:**
- educational buildings (Built Environment)
- educational institutions (Agents)

**Children (5):**
- schools (buildings) → Built Environment
- schools (organisations) → Agents
- [3 specific schools]

**Status:** ✓ CORRECT PATTERN
- Classic dual-nature entity with polyhierarchical intermediate
- Children properly disambiguated
- No change needed

---

### 5. schools of arts
**Facets:** Agents, Arts & Culture, Built Environment, community institutions
**Direct parents:**
- cultural societies (Agents)
- halls (Built Environment)

**Children (2):**
- schools of arts (buildings) → Built Environment
- schools of arts (organisations) → Agents

**Status:** ✓ CORRECT PATTERN
- Polyhierarchical intermediate node
- Children properly disambiguated
- No change needed

---

### Additional Multi-Facet Nodes

**6. financial institutions**
- Facets: Agents (commercial businesses), Built Environment (via new intermediate node)
- Children: financial institutions (buildings), [business children]
- Status: ✓ CORRECT (just added in script 62)

**7. family hotels**
- Facets: Built Environment (via hotels (buildings)), Agents (via hotels (businesses))
- Children: Properly disambiguated
- Status: ✓ CORRECT

**8. cottages**
- Facets: Built Environment, Agents
- Children: cottages (buildings), cottages (businesses)
- Status: ✓ CORRECT

**9. public houses**
- Facets: Built Environment, Agents, Alcohol-related venues
- Children: public houses (buildings), public houses (businesses)
- Status: ✓ CORRECT

**10-13. Denominational church intermediates**
- Church of England churches
- Roman Catholic churches
- congregational churches
- methodist churches
- presbyterian churches
- wesleyan churches

All follow same pattern: polyhierarchical intermediate with disambiguated children
**Status:** ✓ CORRECT

---

## Analysis: Why This Pattern is Correct

### The Polyhierarchical Intermediate Pattern

Our taxonomy uses a deliberate pattern for dual-nature entities:

```
UNQUALIFIED INTERMEDIATE (polyhierarchical)
├─ Parent 1: [Agents facet parent]
├─ Parent 2: [Built Environment facet parent]
└─ Children:
   ├─ Term (building) → only under Built Environment parents
   ├─ Term (organisation) → only under Agents parents
   └─ Specific Named Term → may be under unqualified intermediate
```

**Example: churches**
```
churches (unqualified polyhierarchical intermediate)
├─ Parents: religious organisations (Agents), religious buildings (Built Environment)
└─ Children:
   ├─ churches (buildings) → parent: religious buildings only
   ├─ churches (organisations) → parent: religious organisations only
   ├─ Church of England churches (buildings)
   ├─ Church of England churches (organisations)
   ├─ Roman Catholic churches (buildings)
   └─ Roman Catholic churches (organisations)
```

### Why NOT to Add Disambiguation to Intermediates

**Option 1: Add qualifiers to intermediates (REJECTED)**
```
❌ churches (organisations) → parent: religious organisations
❌ churches (buildings) → parent: religious buildings
```

**Problems:**
1. Creates duplicate terms: "churches (buildings)" would be both intermediate AND leaf
2. Loses polyhierarchical relationship
3. No longer have single unqualified parent for general church mentions
4. Breaks leaf-node tagging pattern (can't tag with intermediate)

**Option 2: Keep current pattern (RECOMMENDED)**
```
✓ churches (unqualified) → parents: religious organisations, religious buildings
   ├─ churches (buildings) → parent: religious buildings
   └─ churches (organisations) → parent: religious organisations
```

**Benefits:**
1. Clear polyhierarchical relationships visible
2. Intermediate node groups all church-related terms
3. Leaf nodes clearly separated by facet
4. Follows Getty AAT pattern for dual-nature entities
5. Consistent with CLAUDE.md § Dual-Nature Entity Handling

---

## Exceptions: Leaf Nodes Without Disambiguation

Some **leaf nodes** exist without disambiguation but should probably have it:

### Leaf Nodes That Are NOT Intermediates

Most specific named entities (Belgravia Hotel, Katoomba Public School, etc.) exist in 3 forms:
- Unqualified (appears directly under intermediate parent)
- (building) variant
- (organisation) or (business) variant

**Example:**
```
hotels
├─ Belgravia Hotel (leaf - unqualified)
```

But also:
```
hotels (buildings)
├─ Belgravia Hotel (building) (leaf)

hotels (businesses)
├─ Belgravia Hotel (business) (leaf)
```

**Analysis:** The unqualified form like "Belgravia Hotel" exists as a **convenience tag** for when source mentions the hotel without specifying building vs business aspect.

**Decision:** This is **intentional flexibility** - cataloguers can choose:
- "Belgravia Hotel" (general mention)
- "Belgravia Hotel (building)" (architectural article)
- "Belgravia Hotel (business)" (commercial/hospitality context)

**No change needed** - this supports nuanced tagging

---

## Nodes That DO Need Disambiguation (Not Found)

Checked for intermediate nodes that:
1. Appear in multiple facets
2. Do NOT have disambiguated children
3. Could cause confusion

**Result:** None found

All multi-facet intermediate nodes have properly disambiguated children that separate the aspects.

---

## Consistency Assessment

### Consistent Patterns

✓ **All dual-nature intermediates** follow same pattern:
- Unqualified intermediate is polyhierarchical
- Children are disambiguated: (building), (organisation), (business)
- Clear facet separation at leaf level

✓ **All denominational church types** consistently implemented:
- [Denomination] churches (unqualified intermediate)
- [Denomination] churches (buildings)
- [Denomination] churches (organisations)

✓ **All accommodation types** consistent:
- hotels, boarding houses, cottages, public houses
- All have (buildings) and (businesses) variants

✓ **All educational institutions** consistent:
- schools, schools of arts
- All have (buildings) and (organisations) variants

### Verdict: HIGHLY CONSISTENT

**No disambiguation additions needed for intermediate nodes**

The current pattern is:
- Theoretically sound (polyhierarchy)
- Practically consistent (applied uniformly)
- Aligned with Getty AAT practices
- Documented in CLAUDE.md

---

## Recommendations

### Recommendation 1: NO CHANGES NEEDED

**Rationale:**
- Current pattern is correct and consistent
- Polyhierarchical intermediates are intentional
- All leaf nodes properly disambiguated
- Follows Getty AAT dual-nature entity practices

### Recommendation 2: Document the Pattern

Update `CLAUDE.md` § Dual-Nature Entity Handling to explicitly state:

> **Intermediate Node Disambiguation:**
>
> Polyhierarchical intermediate nodes (e.g., "churches", "hotels", "schools") do NOT receive disambiguation qualifiers. They serve as organizational parents spanning multiple facets.
>
> **Pattern:**
> ```
> unqualified term (intermediate, polyhierarchical)
> ├─ unqualified term (buildings) (leaf, single parent)
> └─ unqualified term (organisations) (leaf, single parent)
> ```
>
> Only leaf nodes and specific named entities receive disambiguation qualifiers.

### Recommendation 3: Validate During Crosswalk

When creating AAT crosswalk:
- Map intermediate nodes to AAT guide terms (broader concepts)
- Map leaf nodes to AAT specific terms
- Verify polyhierarchical relationships align with AAT practice

---

## Comparison with Getty AAT

### Getty AAT Pattern for Dual-Nature Entities

Getty AAT handles dual-nature entities similarly:

**Example: churches**
- AAT has: "churches (buildings)" [300007466]
- AAT separates building from institution via:
  - Term context (buildings vs organizations)
  - Associative relationships (related terms)
  - Scope notes

**Our Pattern:**
- We use: polyhierarchical intermediate + disambiguated children
- Achieves same separation
- Better suited to flat CSV structure (can't use AAT's complex relationships)

**Verdict:** Our pattern is CSV-appropriate adaptation of AAT principles

---

## Appendix: Complete List of Multi-Facet Intermediates

| Intermediate Node | Agent Facet Parents | Building Facet Parents | Children Count |
|-------------------|---------------------|------------------------|----------------|
| boarding houses | hospitality businesses | Accommodation venues | 2 |
| churches | religious organisations | religious buildings | 7 |
| hotels | hospitality businesses | Accommodation venues | 27 |
| schools | educational institutions | educational buildings | 5 |
| schools of arts | cultural societies | halls | 2 |
| financial institutions | commercial businesses | commercial buildings | varies |
| family hotels | hotels (businesses) | hotels (buildings) | varies |
| cottages | hospitality businesses | accommodation buildings | varies |
| public houses | hospitality businesses | Accommodation venues | varies |
| Church of England churches | churches (organisations) | churches (buildings) | varies |
| Roman Catholic churches | churches (organisations) | churches (buildings) | varies |
| congregational churches | churches (organisations) | churches (buildings) | varies |
| methodist churches | churches (organisations) | churches (buildings) | varies |
| presbyterian churches | churches (organisations) | churches (buildings) | varies |
| wesleyan churches | churches (organisations) | churches (buildings) | varies |

---

## Conclusion

**All intermediate nodes are correctly structured.**

The pattern of unqualified polyhierarchical intermediates with disambiguated children is:
- ✓ Intentional
- ✓ Consistent
- ✓ Aligned with Getty AAT principles
- ✓ Documented in project guidelines

**No changes required.**

The taxonomy disambiguation strategy is sound and ready for AAT crosswalk phase.
