# Phase 1.2.1: Consolidate Similar Tags - Detailed Instructions

**Document Version:** 1.0
**Date:** 2025-10-12
**Status:** Ready to begin
**Phase:** Tag Schema Rationalisation (Phase 1.2, Sub-task 1.2.1)

---

## Overview

**Goal**: Review 332 similar tag pairs and make systematic decisions about which to merge, which to keep separate, and how to establish hierarchical relationships.

**Your primary resources**:
- `data/similar_tags.csv` (332 pairs requiring decisions)
- `docs/folksonomy_logic.md` (decision-making framework already documented)

**Key principle** (from folksonomy_logic.md:614):
**"Err on the side of maintaining existing granularity."** It's easier to collapse tags later than to re-expand them.

---

## The Decision Framework

For each of the 332 tag pairs, you need to make **one of four decisions**:

### Decision 1: **MERGE** (Consolidate to single tag)

**When to merge**:
- True spelling variants (e.g., "Arefact" → "Artefact")
- Capitalisation inconsistencies (e.g., "Bottle" vs "bottle")
- Singular/plural forms **where meaning is identical** (e.g., "Hotel" vs "Hotels")
- Hyphenation differences (e.g., "Building-material" vs "Building material")

**How to decide which form to keep**:
- Use most frequent form as canonical
- Follow naming conventions (to be documented in Phase 1.2.2)
- Prefer full words over abbreviations

**Example from similar_tags.csv line 107**:

```csv
tag1,tag2,count1,count2,similarity,ratio,partial,token_sort,suggested_merge
Bottle,Bootle,60,2,100,56,100,56,Bottle
```

**Decision**: MERGE "Bootle" → "Bottle" (typo, keep more frequent form)

---

### Decision 2: **HIERARCHY** (Parent-child relationship)

**When to create hierarchy**:
- One tag is a **broader category**, the other is a **specific instance**
- Geographic relationships (Katoomba → Katoomba Hotel)
- Institution types (Court → Katoomba Court, Supreme Court, Licensing Court)
- Thematic relationships (Mining → Mining accidents)

**Important**: Both tags are **preserved** - this is NOT a merge. Items get **both** tags applied.

**Example from similar_tags.csv lines 2-7**:

```csv
Court,Court cases,45,45,100,62,100,62,Court
Court,Supreme Court,45,4,100,56,100,56,Court
Court,Katoomba Court,45,8,100,53,100,53,Court
Court,Police court,45,5,100,59,100,59,Court
Court,Courthouse,45,8,100,67,100,67,Court
Court,Licensing Court,45,12,100,50,100,50,Court
```

**Decision**: HIERARCHY (already decided in folksonomy_logic.md:453-475)

```text
Court (PARENT - institution type)
├── Court cases (sub-tag: events/proceedings)
├── Courthouse (sub-tag: building type)
├── Supreme Court (sub-tag: court level)
├── Police court (sub-tag: proceeding type)
├── Licensing Court (sub-tag: proceeding type)
└── Katoomba Court (sub-tag: specific building + also tagged "Katoomba")
```

---

### Decision 3: **KEEP SEPARATE** (Distinct concepts)

**When to keep separate**:
- Different people with similar names (Mr Wilson vs Mrs Wilson vs Mr W Wilson)
- Different places (Katoomba vs South Katoomba)
- Related but distinct concepts (Pub vs Publican vs Public meeting)
- Legitimately different entities detected by similarity algorithm

**Example from similar_tags.csv line 23**:

```csv
Pub,Public meeting,3,1,100,35,100,35,Pub
```

**Decision**: KEEP SEPARATE (completely different concepts - similarity algorithm false positive)

**Example from similar_tags.csv line 148**:

```csv
Mr Wilson,Mrs Wilson,5,2,95,95,89,95,Mr Wilson
```

**Decision**: KEEP SEPARATE (different people - likely husband and wife)

---

### Decision 4: **UNCERTAIN - FLAG FOR HISTORIAN REVIEW**

**When to flag**:
- Domain expertise needed (e.g., "Are Katoomba South and South Katoomba the same place?")
- Ambiguous relationships (e.g., "Should 'Recreation for miners' be merged with 'Miners'?")
- Potential false positives requiring source checking

**Example from similar_tags.csv line 30**:

```csv
Katoomba South,South Katoomba,9,10,100,57,73,100,South Katoomba
```

**Decision**: FLAG FOR REVIEW (Are these the same place or different places? Need historian confirmation)

---

## Workflow: Processing the 332 Pairs

### Step 1: Create Working Document

Create `planning/phase1.2.1-consolidation-decisions.md` to record your decisions as you work through the pairs.

**Format**:

```markdown
# Phase 1.2.1: Tag Consolidation Decisions

**Date started**: 2025-10-12
**Status**: In progress (X/332 pairs reviewed)

## Decisions by Category

### MERGE (Spelling/Capitalisation/Typos)

| Old Tag | New Tag | Count | Rationale |
|---------|---------|-------|-----------|
| Bootle | Bottle | 2→60 | Typo |
| Arefact | Artefact | 1→151 | Typo |

### HIERARCHY (Parent-Child Relationships)

| Parent Tag | Child Tag | Count | Rationale |
|------------|-----------|-------|-----------|
| Court | Court cases | 45, 45 | Institution type → event type |
| Court | Supreme Court | 45, 4 | Institution type → specific court level |

### KEEP SEPARATE (Distinct Concepts)

| Tag 1 | Tag 2 | Count | Rationale |
|-------|-------|-------|-----------|
| Mr Wilson | Mrs Wilson | 5, 2 | Different people (likely husband/wife) |
| Pub | Public meeting | 3, 1 | Unrelated concepts (false positive) |

### FLAG FOR REVIEW (Requires Historian Input)

| Tag 1 | Tag 2 | Count | Question |
|-------|-------|-------|----------|
| Katoomba South | South Katoomba | 9, 10 | Same place or different places? |
```

---

### Step 2: Work Systematically Through Categories

The 332 pairs fall into **natural groupings**. Process them in this order for efficiency:

#### **Category A: Geographic Tags** (lines 8-19, 30, 46-52, 66, etc.)

**Pattern**: Place name + Specific institution/feature within that place

**Strategy**: Apply **multi-tagging principle** from folksonomy_logic.md:438-451
- Keep geographic tag (e.g., "Katoomba")
- Keep institution type (e.g., "Hotel", "Court", "School")
- Keep specific named institution (e.g., "Katoomba Hotel", "Katoomba Court")
- **Decision**: HIERARCHY for all

**Examples**:
- Line 8: Katoomba → Katoomba Hotel (HIERARCHY)
- Line 48: Nellie's Glen → Nellie's Glen Shale Mine (HIERARCHY)
- Line 51: Megalong Valley → Megalong Valley School (HIERARCHY)

---

#### **Category B: Institution Type + Named Institution** (lines 90-95, 160-184, etc.)

**Pattern**: Generic institution → Specific named instance

**Strategy**: Same as geographic - establish parent-child hierarchy

**Examples**:
- Lines 90-95: Church → St Hilda's Church, Congregational Church, etc. (HIERARCHY for all)
- Lines 160-184: Hotels → Mount Victoria Hotel, Allen's Hotel, etc. (HIERARCHY for all)

---

#### **Category C: Person Names** (lines 148-332, approximately)

**Pattern**: Similar names (Mr Wilson, Mrs Wilson, Mr W Wilson, etc.)

**Strategy**: **KEEP SEPARATE unless you have definitive evidence they're the same person**

**Critical guidance from folksonomy_logic.md:517-522**:
> "Preserve all individual person tags - DO NOT merge similar names without verification. Many detected 'similar' names are actually different people."

**Examples**:
- Line 148: Mr Wilson vs Mrs Wilson (KEEP SEPARATE - different people)
- Line 186: Mr W Wilson vs Mr Wilson (KEEP SEPARATE - could be same person or different, needs verification)
- Line 193: Mr Thomas Meredith vs Mr Evan Thomas Meredith (KEEP SEPARATE - different people from Meredith family)

---

#### **Category D: Spelling/Typo Variants** (scattered throughout)

**Pattern**: Obvious misspellings

**Strategy**: MERGE to correct form

**Examples**:
- "Bootle" → "Bottle"
- "Arefact" → "Artefact"
- "Depresson" → "Depression"
- "Buidling material" → "Building material"

**Note**: These are also present in archaeological data (see docs/folksonomy_logic.md:1098-1123 for archaeological typos)

---

#### **Category E: Thematic Relationships** (lines 34-46, 76-78, 102, etc.)

**Pattern**: Broad theme + Specific manifestation

**Strategy**: Establish HIERARCHY (parent-child)

**Examples**:
- Line 34: Cricket → Megalong Cricket Club (HIERARCHY)
- Line 42: Football → Football clubs (HIERARCHY)
- Lines 77-78: Mining → Mining settlements, Mining accidents (HIERARCHY)

---

#### **Category F: Ambiguous/Uncertain** (case-by-case)

**Strategy**: FLAG FOR REVIEW when uncertain

**Examples**:
- Line 23: Pub vs Public meeting (KEEP SEPARATE - false positive)
- Line 101: Recreation for miners vs Miners (FLAG - is recreation a sub-category or separate theme?)
- Line 237: Mining vs Drinking (KEEP SEPARATE - unrelated, false positive)

---

### Step 3: Generate Consolidation Map

Once decisions are made, create `data/tag_consolidation_map.csv`:

**Format**:

```csv
old_tag,new_tag,action,notes
Bootle,Bottle,merge,typo
Arefact,Artefact,merge,typo
Court cases,Court,hierarchy,parent=Court
Supreme Court,Court,hierarchy,parent=Court
Katoomba Hotel,Katoomba,hierarchy,parent=Katoomba (also parent=Hotel)
Mr Wilson,Mr Wilson,keep,distinct from Mrs Wilson and Mr W Wilson
```

**Column definitions**:
- **old_tag**: Original tag from Zotero
- **new_tag**: Canonical form (for merges) or parent tag (for hierarchies)
- **action**: One of: merge, hierarchy, keep, review
- **notes**: Brief rationale or additional context

---

### Step 4: Preview Changes

Before applying, generate `reports/consolidation_preview.md` showing:
- How many tags will be affected
- How many items will be retagged
- Examples of before/after for spot-checking

---

## Practical Approach: Recommended Order

Work through this **incrementally**:

1. **Start with Category D (Spelling/Typos)** - Quickest wins, clearest decisions
2. **Move to Category A (Geographic)** - Apply consistent hierarchy pattern
3. **Then Category B (Institutions)** - Similar hierarchy pattern
4. **Review Category E (Thematic)** - Some judgement calls
5. **Flag Category F (Ambiguous)** - Set aside for historian review
6. **Save Category C (Person Names) for last** - Most complex, requires careful review

---

## Key Reference Documents

### Primary Resources

- **data/similar_tags.csv** - The 332 pairs to review (lines 1-333, including header)
- **docs/folksonomy_logic.md** - Your decision-making framework and tagging philosophy
  - Section 2: Historical Document Tagging System
  - Section 5.2: Geographic Tag Proliferation (lines 422-451)
  - Section 5.3: Court Tag Consolidation (lines 453-486)
  - Section 5.4: People and Family Name Variations (lines 488-534)
  - Section 7.1: Priority Actions (lines 610-687)

### Phase 1 Planning

- **planning/phase1-detailed.md** - Complete Phase 1 roadmap
  - Section 1.2.1: Consolidate Similar Tags (lines 93-111)

---

## Important Reminders

### From folksonomy_logic.md

**Rationalisation Principle (line 614)**:
> "Err on the side of maintaining existing granularity. It's easier to collapse tags later than to re-expand them. Temporary redundancy is acceptable during Phase 1.2."

**Multi-tagging for Geographic + Institution (lines 438-451)**:

> "Apply multiple tags: Geographic + Institution type + Named institution
> Example: Item about Katoomba Court → Tags: 'Katoomba', 'Court', 'Katoomba Court'
> Benefits: Enables searching by location alone, by institution type alone, or specific named institution"

**Person Names - DO NOT MERGE (lines 517-522)**:

> "Preserve all individual person tags - DO NOT merge similar names without verification. Many detected 'similar' names are actually different people."

**Court Tag Hierarchy - ALREADY DECIDED (lines 453-475)**:

The Court tag hierarchy has been decided and documented:
- Court (PARENT CATEGORY - institution type)
- Court cases, Courthouse, Supreme Court, Police court, Licensing Court, Katoomba Court (all SUB-TAGS)

---

## Outputs from Phase 1.2.1

**Required deliverables**:

1. **planning/phase1.2.1-consolidation-decisions.md** - Decision log with rationale
2. **data/tag_consolidation_map.csv** - Machine-readable transformation rules
3. **reports/consolidation_preview.md** - Before/after comparison for validation

**Optional but recommended**:

4. **planning/phase1.2.1-flagged-for-review.md** - Questions requiring historian input
5. **data/tags_deduplicated.json** - Preview of consolidated tag list (before applying to Zotero)

---

## Next Steps After 1.2.1

Once similar tags are consolidated, you will proceed to:

- **Phase 1.2.2**: Standardise Terminology (naming conventions, preferred terms)
- **Phase 1.2.3**: Create Hierarchical Structure (build complete taxonomy)
- **Phase 1.2.4**: Document Definitions (scope notes, usage guidelines)

Then:

- **Phase 1.3**: Vocabulary Mapping & Publication (Getty AAT/TGN, RVA)
- **Phase 1.4**: Batch Update Zotero (apply rationalised tags via API)

---

## Getting Started

**First session tasks**:

1. Read this instruction document thoroughly
2. Review `data/similar_tags.csv` (first 50 lines to get a sense of the data)
3. Review relevant sections of `docs/folksonomy_logic.md`
4. Create `planning/phase1.2.1-consolidation-decisions.md` using template above
5. Begin with Category D (Spelling/Typos) - scan through similar_tags.csv and identify obvious typos
6. Document first 10-20 decisions to establish workflow rhythm
7. Continue systematically through categories

**Estimated time**: 1-2 weeks part-time (depends on how many require historian consultation)

---

## Questions or Uncertainties?

When you're unsure about a decision:

1. Check `docs/folksonomy_logic.md` for relevant guidance
2. Flag the pair for historian review in your decisions document
3. Document your uncertainty and specific questions
4. Continue with other clear-cut decisions
5. Batch review all flagged items with historian later

**Remember**: It's better to flag for review than to make incorrect consolidations. The principle of maintaining granularity means you can always collapse later, but you cannot re-expand lost information.

---

## End of Instructions

**Status**: Ready to begin Phase 1.2.1
**Next action**: Create `planning/phase1.2.1-consolidation-decisions.md` and start with Category D (Spelling/Typos)

Good luck with the tag consolidation work!
