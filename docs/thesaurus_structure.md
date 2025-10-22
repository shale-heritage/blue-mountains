# Thesaurus Structure for Blue Mountains Folksonomy

**Date:** 2025-10-20
**Status:** Draft framework

---

## Overview

This document defines how the Blue Mountains folksonomy handles:
- **Preferred terms** (main entries used for tagging)
- **Non-preferred terms** (variants that point to preferred terms)
- **Historical name changes** (entities with multiple official names over time)
- **Scope notes** (contextual information)

---

## 1. How Major Thesauri Handle Name Changes

### Getty Art & Architecture Thesaurus (AAT)

**Structure:**
```
PREFERRED TERM (descriptor)
├── Used for: [non-preferred terms]
├── Scope note: [contextual information]
└── Historical note: [name changes, dates]
```

**Example:**
```
Australian Kerosene Oil and Mineral Company
├── Used for: Australian Kerosene Oil Company
├── Used for: A.K.O. & M. Company
├── Used for: A.K.O.
├── Scope note: Australian mining company that extracted and processed oil shale
└── Historical note: Known as "Australian Kerosene Oil and Mineral Company"
    through 1896; renamed "Australian Kerosene Oil Company" after 1896,
    though old name continued in use.
```

### Library of Congress Subject Headings (LCSH)

**Structure:**
```
Non-preferred term
    USE Preferred term
```

**Example:**
```
Australian Kerosene Oil Company
    USE Australian Kerosene Oil and Mineral Company

A.K.O. & M. Company
    USE Australian Kerosene Oil and Mineral Company
```

### SKOS (Simple Knowledge Organisation System)

**Structure (RDF/XML):**
```xml
<skos:Concept rdf:about="australian_kerosene_oil_and_mineral_company">
  <skos:prefLabel xml:lang="en">Australian Kerosene Oil and Mineral Company</skos:prefLabel>
  <skos:altLabel xml:lang="en">Australian Kerosene Oil Company</skos:altLabel>
  <skos:altLabel xml:lang="en">A.K.O. &amp; M. Company</skos:altLabel>
  <skos:altLabel xml:lang="en">A.K.O.</skos:altLabel>
  <skos:scopeNote xml:lang="en">Mining company operating in Blue Mountains region of New South Wales, Australia. Known as "Australian Kerosene Oil and Mineral Company" through 1896; renamed "Australian Kerosene Oil Company" after 1896, though earlier name continued in use.</skos:scopeNote>
  <skos:historyNote xml:lang="en">Established 1878. Name changed 1896.</skos:historyNote>
</skos:Concept>
```

---

## 2. Recommended Approach for Blue Mountains Folksonomy

### Preferred Term Selection Principles

When choosing between multiple historical names:

**PRINCIPLE 1: Longest official name**
- Use the most complete official name as preferred term
- Rationale: Most precise, avoids ambiguity

**PRINCIPLE 2: Earlier name for historical entities**
- For defunct entities, use the name from their most significant period
- Rationale: Preserves historical context

**PRINCIPLE 3: Name with clearest meaning**
- If equally valid, choose the name that best describes the entity
- Rationale: Supports discovery and comprehension

**EXAMPLE:** "Australian Kerosene Oil and Mineral Company" (preferred)
- ✅ Longest official name
- ✅ Earlier name (1878-1896, company's establishment period)
- ✅ Clearer meaning (specifies both oil AND mineral)

---

## 3. Implementation in Zotero Tags

### Tagging Protocol

**ALWAYS use the preferred term for tagging**, regardless of what name appears in the source document.

**Example:**
- Source says: "The A.K.O. Company announced..."
- Tag to use: "Australian Kerosene Oil and Mineral Company"

**Rationale:**
- Ensures consistent retrieval across all sources
- Collocates all items about the same entity under one tag
- Supports faceted browsing and filtering

---

## 4. Scope Note Requirements

For entities with name changes or variants, scope notes MUST include:

### Minimum Required Elements

1. **Entity type** (company, organization, person, place, etc.)
2. **Preferred term explanation** (why this term was chosen)
3. **Variant names** (all known alternatives)
4. **Historical context** (name changes with dates)
5. **Usage guidance** (when to apply this tag)

### Template

```markdown
**[Preferred Term]**

**Type:** [Organization/Company/Person/Place]

**Scope:** [1-2 sentence description of entity]

**Preferred term:** [Explanation of why this is the preferred term]

**Variant names:**
- [Variant 1] (dates if applicable)
- [Variant 2] (dates if applicable)
- [Abbreviation]

**Historical note:** [Name changes, significant events, dates]

**Use this tag for:** [Guidance on when to apply]

**Related tags:** [See also references]
```

---

## 5. Example Scope Notes

### Example 1: Australian Kerosene Oil and Mineral Company

**Australian Kerosene Oil and Mineral Company**

**Type:** Commercial business (mining company)

**Scope:** Australian mining company that extracted and processed oil shale in the Blue Mountains region of New South Wales, producing kerosene, paraffin wax, lubricating oil, and other petroleum products.

**Preferred term:** "Australian Kerosene Oil and Mineral Company" is the preferred term as it was the company's official registered name from establishment (1878) through 1896, encompassing the company's most significant period of operations in the Blue Mountains.

**Variant names:**
- Australian Kerosene Oil Company (1896-closure, official name after reorganisation)
- Australian Kerosene Oil and Mineral Company Limited (full legal name with "Limited")
- A.K.O. & M. Company (abbreviation, commonly used in newspapers)
- A.K.O. (short abbreviation)
- AKO (abbreviation without punctuation)

**Historical note:** Established 1878 as "Australian Kerosene Oil and Mineral Company Limited." Company was reorganised in 1896 and renamed "Australian Kerosene Oil Company," though the earlier name continued to be used in some contexts. The company operated mines at Ruined Castle and Nellie's Glen in the Katoomba area. Ceased operations [date TBD - needs research].

**Use this tag for:** Articles mentioning this company regardless of which name variant appears in the source. Includes references to the company as an organisation, its management, operations, employees, or financial affairs.

**Do not use this tag for:** Physical mine sites operated by the company (use specific mine site tags: "Ruined Castle Shale Mine," "Nellie's Glen Shale Mine"). For articles discussing mining activities without explicitly naming the company, use thematic tags like "Shale mining" or "Mining industry."

**Related tags:**
- Ruined Castle Shale Mine (mine site operated by this company)
- Nellie's Glen Shale Mine (mine site operated by this company)
- Shale mining (thematic tag for mining activity)
- Mining companies (parent category)

---

### Example 2: Katoomba Coal and Shale Company

**Katoomba Coal and Shale Company**

**Type:** Commercial business (mining company)

**Scope:** Coal and oil shale mining company operating in Katoomba, New South Wales. One of the earliest mining enterprises in the Blue Mountains region.

**Preferred term:** "Katoomba Coal and Shale Company" is the preferred term as it was the official registered name.

**Variant names:**
- Katoomba Coal and Shale Company Limited (full legal name with "Limited")
- Katoomba Coal & Shale Co. Ltd. (abbreviated form)
- KC&S Co., Ltd. (abbreviation)
- Katoomba Coal and Shale Mines (company name as it appeared in some newspaper articles)
- Katoomba Colliery (informal reference to the company in newspaper articles)

**Historical note:** Established 3 February 1887 (some sources say January 1885) by John Britty North. Company went into liquidation in 1892. Operations were subsequently taken over by the Australian Kerosene Oil and Mineral Company.

**Use this tag for:** Articles mentioning this company by any of its name variants. Includes references to the company's establishment, operations, management, employees, or liquidation.

**Do not use this tag for:** Generic references to coal mining in Katoomba without naming this specific company (use "Coal mining" or "Katoomba coal mines" instead). Physical infrastructure of the mine (use "Katoomba coal mines" for the physical mine site).

**Related tags:**
- Katoomba coal mines (generic tag for coal mines in Katoomba area, may include this company's mines)
- Australian Kerosene Oil and Mineral Company (successor company)
- Mining companies (parent category)

---

## 6. CSV Structure for Variant Mappings

### In tag_consolidation_map.csv

All variants map to the preferred term via MERGE action:

```csv
old_tag,new_tag,action,notes
Australian Kerosene Oil Company,Australian Kerosene Oil and Mineral Company,merge,Name variant (1896-closure) - merge to preferred term (earlier name)
A.K.O. & M. Company,Australian Kerosene Oil and Mineral Company,merge,Abbreviation - merge to preferred term
A.K.O.,Australian Kerosene Oil and Mineral Company,merge,Short abbreviation - merge to preferred term
AKO,Australian Kerosene Oil and Mineral Company,merge,Abbreviation without punctuation - merge to preferred term
Australian Kerosene Shale and Oil Company,Australian Kerosene Oil and Mineral Company,merge,Name variant found in sources - merge to preferred term
```

---

## 7. SKOS Export Structure

For Phase 1.3 (Vocabulary Publication to Research Vocabularies Australia):

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix bmf: <http://bluemountains.example.org/folksonomy/> .

bmf:australian_kerosene_oil_and_mineral_company
    a skos:Concept ;
    skos:prefLabel "Australian Kerosene Oil and Mineral Company"@en ;
    skos:altLabel "Australian Kerosene Oil Company"@en ;
    skos:altLabel "A.K.O. & M. Company"@en ;
    skos:altLabel "A.K.O."@en ;
    skos:altLabel "AKO"@en ;
    skos:hiddenLabel "Australian Kerosene Shale and Oil Company"@en ;
    skos:definition "Australian mining company that extracted and processed oil shale in the Blue Mountains region of New South Wales."@en ;
    skos:scopeNote "Use this term for all references regardless of name variant in source."@en ;
    skos:historyNote "Established 1878. Renamed 'Australian Kerosene Oil Company' in 1896."@en ;
    skos:broader bmf:mining_companies ;
    skos:related bmf:ruined_castle_shale_mine ;
    skos:related bmf:nellies_glen_shale_mine ;
    dct:created "1878"^^xsd:gYear ;
    dct:modified "1896"^^xsd:gYear .
```

---

## 8. Workflow for Handling Name Changes

### Step 1: Research
- Identify all known name variants from sources
- Determine official registered names
- Establish chronology of name changes
- Note context (mergers, reorganizations, etc.)

### Step 2: Select Preferred Term
- Apply principles (see Section 2)
- Document rationale

### Step 3: Create Mapping
- Add MERGE rows to tag_consolidation_map.csv
- Map all variants → preferred term

### Step 4: Write Scope Note
- Follow template (see Section 4)
- Include all required elements
- Cross-reference related tags

### Step 5: Apply to Zotero
- Re-tag items using preferred term
- Update tag_consolidation_map.csv
- Apply batch updates via Zotero API (Phase 1.4)

---

## 9. Phase 1.2.2 Deliverable

**File:** `docs/tag_definitions.md` (to be created)

**Structure:**
```markdown
# Tag Definitions and Scope Notes

## Organizations

### Mining Companies

#### Australian Kerosene Oil and Mineral Company
[Full scope note as per template]

#### Katoomba Coal and Shale Company
[Full scope note as per template]

[... all other tags with scope notes ...]
```

---

## 10. Implementation Checklist

For each entity with name variants:

- [ ] Research all known names and dates
- [ ] Select preferred term (document rationale)
- [ ] Create variant mappings in CSV
- [ ] Write scope note following template
- [ ] Add to tag_definitions.md (Phase 1.2.2)
- [ ] Export to SKOS format (Phase 1.3)
- [ ] Apply to Zotero items (Phase 1.4)

---

## References

- Getty AAT: https://www.getty.edu/research/tools/vocabularies/aat/
- LCSH: https://www.loc.gov/aba/publications/FreeLCSH/freelcsh.html
- SKOS Primer: https://www.w3.org/TR/skos-primer/
- ANSI/NISO Z39.19-2005: Guidelines for the Construction, Format, and Management of Monolingual Controlled Vocabularies

---

**Document status:** Draft framework
**Next steps:** Populate tag_definitions.md with scope notes (Phase 1.2.2)
