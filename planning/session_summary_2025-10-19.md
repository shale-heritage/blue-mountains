# Session Summary: Tag Consolidation - Contextual Analysis & Taxonomy Development

**Date:** 2025-10-19
**Focus:** Evidence-based disambiguation using full text analysis

---

## Major Accomplishments

### 1. Discovered Full Text Availability ✓

**Finding:** All Zotero items have full newspaper article text in notes
- Text stored as HTML (easily stripped for analysis)
- Substantive content (860-12,300 characters per article)
- Enables KWIC (Key Word In Context) analysis for disambiguation

**Created Tools:**
- Script 08: Check full text availability
- Script 09: Analyse naming variants using KWIC
- Script 12: Check School of Arts usage
- Script 13: Analyse lodge vs hall usage
- Script 14: Compare School of Arts tags
- Script 15: Find dual-nature entities

---

### 2. Evidence-Based Decisions Implemented ✓

#### **Decision 1: Katoomba South → South Katoomba (MERGE)**

**Evidence from full text:**
- "On the spot known as **South Katoomba** a little village sprang up"
- "Returning Officer for **South Katoomba**" (separate voting district)
- "25 miners have freeholds in **South Katoomba**"
- Consistently capitalised as proper noun = named place

**Action:** MERGE Katoomba South → South Katoomba
- Already in hierarchy under Katoomba (parent)

#### **Decision 2: I.O.O.F. Hall → Odd Fellows' Hall (MERGE)**

**Evidence:**
- IOOF = Independent Order of Odd Fellows
- Same physical building, different naming conventions
- 17 items vs 24 items

**Action:** MERGE I.O.O.F. Hall → Odd Fellows' Hall

---

### 3. Discovered Dual-Nature Entity Pattern ✓

**Key Insight:** Some entities function as BOTH organisation AND venue

**Pattern identified:**
- Organisation usage: committee, members, subscribers, secretary, institution
- Venue usage: held at, meeting at, building, hall, room

**Entities with dual nature:**

1. **School of Arts institutions**
   - Organisation: subscribers, committee, institution
   - Venue: reading room, building, hall
   - Multi-tag: Cultural societies + Halls

2. **Odd Fellows' Hall**
   - Organisation: lodge, members, "Oddfellows' Lodge"
   - Venue: "social at the Oddfellows' Hall"
   - Multi-tag: Lodges + Halls

3. **Masonic Hall**
   - Organisation: "Mount Masonic Lodge"
   - Venue: "dance at the Masonic Hall"
   - Multi-tag: Lodges + Halls

**Implementation:** Multi-tagging in both relevant parent categories

---

### 4. Created Two Major Taxonomy Hierarchies ✓

#### **A. Religion Hierarchy (NEW)**

```
Religion (NEW master parent)
├── Church (modified from top-level to child)
│   ├── Wesleyan Church
│   ├── St Hilda's Church
│   ├── Congregational Church
│   ├── Katoomba Congregational Church
│   ├── Roman Catholic Church
│   └── Methodist Church
└── Sunday school (MOVED from School parent)
```

**Rationale:** Sunday school is religious education, not educational school

#### **B. Community Institutions Hierarchy (NEW)**

```
Community institutions (NEW master parent)
│
├── Lodges (friendly societies)
│   ├── Druid's Lodge
│   ├── Mountaineer Lodge
│   ├── Odd Fellows' Hall (also under Halls)
│   └── Masonic Hall (also under Halls)
│
├── Halls (physical venues)
│   ├── School of Arts (also under Cultural societies)
│   ├── Katoomba School of Arts (also under Cultural societies)
│   ├── Odd Fellows' Hall (also under Lodges)
│   ├── Masonic Hall (also under Lodges)
│   ├── Clarke's Hall
│   ├── Waudby's Hall
│   └── Mount Victoria Hall
│
├── Civic organisations
│   ├── Progress committees
│   ├── Katoomba Progress Association
│   ├── Leura Progress Association
│   ├── Wentworth Falls Progress Association
│   ├── Mount Victoria Progress Committee
│   └── Megalong Progress Committee
│
└── Cultural societies
    ├── School of Arts (also under Halls)
    ├── Katoomba School of Arts (also under Halls)
    ├── Horticulture society
    ├── Katoomba Amateur Dramatic Club
    └── Chess and Draughts Club
```

**Additional hierarchy:**
```
School of Arts (generic parent)
└── Katoomba School of Arts (specific child)
```

**Rationale:**
- "School of Arts" is generic (used for multiple towns)
- "Katoomba School of Arts" is specific instance

---

### 5. Current Consolidation Status ✓

**Total decisions:** 421 pairs

- **MERGE:** 2 pairs
  - Katoomba South → South Katoomba
  - I.O.O.F. Hall → Odd Fellows' Hall

- **HIERARCHY:** 201 pairs (increased from 174)
  - Added 27 new hierarchies for Religion and Community Institutions

- **KEEP_SEPARATE:** 218 pairs

- **FLAGGED:** 0 pairs (all triaged!)

---

## Future Work Identified

### Phase 2: Town-Specific Schools of Arts

**Principle:** Create specific entries for each town's School of Arts

**Evidence:** Generic "School of Arts" tag includes references to:
- Blackheath (2 items)
- Leura (2 items)
- Mount Victoria (2 items)
- Megalong (2 items)
- Katoomba (4 items)

**Action needed:**
1. Web search to verify historical existence of each town's School of Arts
2. Create specific tags: Blackheath School of Arts, Leura School of Arts, etc.
3. Apply dual-nature classification to each (organisation + venue)
4. Establish hierarchy: School of Arts (parent) → [Town] School of Arts (children)

---

### Phase 3: Other Dual-Nature Entity Candidates

**HIGH PRIORITY:**

1. **Churches** - Likely dual-nature (denomination + building)
   - Methodist Church = denomination/congregation AND physical church building
   - Check full text: "at the Methodist Church" (venue) vs "the Methodist Church decided" (org)

2. **Councils** - Likely dual-nature (government body + chambers)
   - Katoomba Council = municipal government AND council chambers
   - Evidence: Separate "Council Chambers" tag exists (7 items)
   - Check: "the Council decided" (org) vs "meeting at the Council" (venue)

**MEDIUM PRIORITY:**

3. **Reserves** - Possibly dual-nature (land + managing committee)
   - Check: "Rifle Reserves committee" vs "on the Rifle Reserves" (land)

4. **Progress Associations** - Check if they had dedicated premises

**LOW PRIORITY:**

5. **Hotels** - Likely single-nature (just buildings/businesses)
6. **Sports clubs** - Likely single-nature (just organisations; grounds separately named)

---

## Tools Created

All scripts with full contextual analysis capability:

1. `scripts/08_check_full_text_availability.py` - Verify notes contain full text
2. `scripts/09_analyse_variants_in_context.py` - KWIC analysis of naming variants
3. `scripts/10_check_company_tag.py` - Check specific tag items
4. `scripts/11_regenerate_reports.py` - Regenerate markdown reports from CSV
5. `scripts/12_check_school_of_arts.py` - Analyse School of Arts usage patterns
6. `scripts/13_check_lodge_usage.py` - Distinguish lodge organisation vs hall building
7. `scripts/14_compare_school_of_arts.py` - Compare generic vs specific tags
8. `scripts/15_find_dual_nature_entities.py` - Identify potential dual-nature candidates

---

## Key Principles Established

### 1. Liberal Tagging Philosophy ✓

**Principle:** Be liberal with tags; simplification later is easier than recovery
- Multi-tag entities that have dual nature
- Create hierarchies rather than merging when uncertain
- Preserve information, don't collapse prematurely

### 2. Evidence-Based Decisions ✓

**Method:** Use full text context to disambiguate
- KWIC analysis shows actual usage in newspaper sources
- Keyword analysis (organisation vs venue language)
- Geographic context from co-occurring location tags

### 3. Dual-Nature Recognition ✓

**Pattern:** Entity = organisation + venue → Multi-tag both aspects
- Cultural societies + Halls (School of Arts)
- Lodges + Halls (Odd Fellows, Masons)
- Future: Churches?, Councils?

### 4. Generic vs Specific Hierarchies ✓

**Pattern:** Generic parent → Town-specific children
- School of Arts (generic) → Katoomba School of Arts (specific)
- Future: Create for all towns with Schools of Arts

---

## Statistics

**Scripts created:** 8 new analysis tools
**Hierarchies added:** 27 new parent-child relationships
**Merges completed:** 2 naming variants
**New taxonomy categories:** 2 master parents (Religion, Community institutions)
**Dual-nature entities identified:** 4 (School of Arts, Katoomba School of Arts, Odd Fellows' Hall, Masonic Hall)
**Future dual-nature candidates:** 4 high/medium priority

**Total consolidation decisions:** 421 pairs (up from 393)

---

## Next Session Priorities

1. **Churches analysis** - Check for dual-nature (high priority)
2. **Councils analysis** - Check for dual-nature (high priority)
3. **Town-specific Schools of Arts** - Create dedicated tags
4. **Review remaining 218 keep-separate decisions** - Any consolidation opportunities?
5. **Begin broader taxonomy development** - Now that existing tags are rationalized

