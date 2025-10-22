# Taxonomy Implementation - Phase 1

**Date:** 2025-10-19
**Status:** Ready to implement

---

## Changes to Implement Now

### 1. Religion Hierarchy (NEW)

**Create master parent:** Religion

**Structure:**
```
Religion (NEW parent)
├── Church (modify: was top-level, now child of Religion)
│   ├── Wesleyan Church
│   ├── St Hilda's Church
│   ├── Congregational Church
│   ├── Katoomba Congregational Church
│   ├── Roman Catholic Church
│   └── Methodist Church
└── Sunday school (MOVE from parent=School to parent=Religion)
```

**Actions:**
- Create new parent tag: Religion
- Modify: Church (change from top-level to child of Religion)
- Move: Sunday school (from School → Religion)

---

### 2. Community Institutions Hierarchy (NEW)

**Create master parent:** Community institutions

**Structure with dual-nature multi-tagging:**
```
Community institutions (NEW parent)
│
├── Lodges (friendly societies - nest existing parent under Community institutions)
│   ├── Druid's Lodge
│   ├── Mountaineer Lodge
│   ├── Odd Fellows' Hall (MULTI-TAG: also under Halls)
│   └── Masonic Hall (MULTI-TAG: also under Halls)
│
├── Halls (physical venues - NEW subcategory)
│   ├── School of Arts (MULTI-TAG: also under Cultural societies - generic parent)
│   ├── Katoomba School of Arts (MULTI-TAG: also under Cultural societies - specific instance)
│   ├── Odd Fellows' Hall (MULTI-TAG: also under Lodges)
│   ├── Masonic Hall (MULTI-TAG: also under Lodges)
│   ├── Clarke's Hall
│   ├── Waudby's Hall
│   └── Mount Victoria Hall
│
├── Civic organisations (NEW subcategory)
│   ├── Progress committees
│   ├── Katoomba Progress Association
│   ├── Leura Progress Association
│   ├── Wentworth Falls Progress Association
│   ├── Mount Victoria Progress Committee
│   └── Megalong Progress Committee
│
└── Cultural societies (NEW subcategory)
    ├── School of Arts (MULTI-TAG: also under Halls - generic parent)
    ├── Katoomba School of Arts (MULTI-TAG: also under Halls - specific instance)
    ├── Horticulture society
    ├── Katoomba Amateur Dramatic Club
    └── Chess and Draughts Club
```

**Additional Hierarchy:**
```
School of Arts (generic - modify to be parent)
└── Katoomba School of Arts (child of generic School of Arts)
```

**Actions:**
- Create: Community institutions (new master parent)
- Create: Lodges, Halls, Civic organisations, Cultural societies (subcategories)
- Move: Lodges parent (from top-level → under Community institutions)
- Move: School of Arts tags (from School → Community institutions)
- Add multi-tagging for dual-nature entities:
  - Odd Fellows' Hall: Lodges + Halls
  - Masonic Hall: Lodges + Halls
  - School of Arts: Cultural societies + Halls
  - Katoomba School of Arts: Cultural societies + Halls
- Create hierarchy: School of Arts (parent) → Katoomba School of Arts (child)

---

### 3. Merges

**I.O.O.F. Hall → Odd Fellows' Hall**
- Rationale: Same organisation/building (IOOF = Independent Order of Odd Fellows)
- Evidence: 17 items vs 24 items, same physical location
- New canonical form: "Odd Fellows' Hall"

**Katoomba South → South Katoomba** (ALREADY IMPLEMENTED)
- Rationale: Naming variant, contextual evidence shows "South Katoomba" in sources
- Status: ✓ Complete

---

### 4. Moves (from incorrect parents)

| Tag | Current Parent | New Parent | Reason |
|-----|----------------|------------|--------|
| Sunday school | School | Religion | Religious education, not educational school |
| School of Arts | School | Cultural societies + Halls | Community cultural centre, not educational school |
| Katoomba School of Arts | School of Arts | Cultural societies + Halls | Community cultural centre, not educational school |

---

## Implementation in CSV Format

### New parent relationships to add:

```csv
old_tag,new_tag,action,notes
# Religion hierarchy
Church,Church,hierarchy,parent=Religion
Sunday school,Sunday school,hierarchy,parent=Religion

# Community institutions - Lodges subcategory
Lodges,Lodges,hierarchy,parent=Community institutions
Druid's Lodge,Druid's Lodge,hierarchy,parent=Lodges
Mountaineer Lodge,Mountaineer Lodge,hierarchy,parent=Lodges
Odd Fellows' Hall,Odd Fellows' Hall,hierarchy,"parent=Lodges; parent=Halls (dual nature)"
Masonic Hall,Masonic Hall,hierarchy,"parent=Lodges; parent=Halls (dual nature)"

# Community institutions - Halls subcategory
Halls,Halls,hierarchy,parent=Community institutions
School of Arts,School of Arts,hierarchy,"parent=Halls; parent=Cultural societies (dual nature)"
Katoomba School of Arts,Katoomba School of Arts,hierarchy,"parent=Halls; parent=Cultural societies (dual nature); parent=School of Arts (specific instance)"
Odd Fellows' Hall,Odd Fellows' Hall,hierarchy,"parent=Halls; parent=Lodges (dual nature)"
Masonic Hall,Masonic Hall,hierarchy,"parent=Halls; parent=Lodges (dual nature)"
Clarke's Hall,Clarke's Hall,hierarchy,parent=Halls
Waudby's Hall,Waudby's Hall,hierarchy,parent=Halls
Mount Victoria Hall,Mount Victoria Hall,hierarchy,parent=Halls

# Community institutions - Civic organisations
Civic organisations,Civic organisations,hierarchy,parent=Community institutions
Progress committees,Progress committees,hierarchy,parent=Civic organisations
Katoomba Progress Association,Katoomba Progress Association,hierarchy,parent=Civic organisations
Leura Progress Association,Leura Progress Association,hierarchy,parent=Civic organisations
Wentworth Falls Progress Association,Wentworth Falls Progress Association,hierarchy,parent=Civic organisations
Mount Victoria Progress Committee,Mount Victoria Progress Committee,hierarchy,parent=Civic organisations
Megalong Progress Committee,Megalong Progress Committee,hierarchy,parent=Civic organisations

# Community institutions - Cultural societies
Cultural societies,Cultural societies,hierarchy,parent=Community institutions
School of Arts,School of Arts,hierarchy,"parent=Cultural societies; parent=Halls (dual nature)"
Katoomba School of Arts,Katoomba School of Arts,hierarchy,"parent=Cultural societies; parent=Halls (dual nature)"
Horticulture society,Horticulture society,hierarchy,parent=Cultural societies
Katoomba Amateur Dramatic Club,Katoomba Amateur Dramatic Club,hierarchy,parent=Cultural societies
Chess and Draughts Club,Chess and Draughts Club,hierarchy,parent=Cultural societies

# Merge
I.O.O.F. Hall,Odd Fellows' Hall,merge,Same building - IOOF = Independent Order of Odd Fellows
```

---

## Future Work (Phase 2)

### Town-Specific Schools of Arts

**Principle:** Consistently create specific entries for each town's School of Arts when evidence exists.

**Process:**
1. Review items tagged "School of Arts" (generic) for town-specific mentions
2. Web search to verify historical existence (e.g., "Blackheath School of Arts 1890s")
3. Create specific tags if confirmed:
   - Blackheath School of Arts
   - Leura School of Arts
   - Megalong School of Arts
   - Mount Victoria School of Arts
4. Apply dual-nature classification (organisation + venue) to each
5. Establish hierarchy: School of Arts (parent) → [Town] School of Arts (children)

**Research needed:**
- Check historical records for Schools of Arts in:
  - Blackheath
  - Leura
  - Mount Victoria
  - Megalong
  - Hartley
  - Lithgow
  - Wentworth Falls

**Tagging consistency:**
- Each town's School of Arts should have BOTH:
  - Organisation aspect: under Cultural societies
  - Venue aspect: under Halls

---

## Dual-Nature Entity Pattern (Generalizable)

**Pattern discovered:** Some entities have both organisational and physical aspects.

**Classification rule:**
- If entity is both organisation AND building → Multi-tag under both relevant parents
- Organisation parent options: Lodges, Cultural societies, Civic organisations
- Venue parent: Halls

**Examples found:**
- ✓ School of Arts institutions (organisation + venue)
- ✓ Friendly society lodges (organisation + hall building)

**Apply to other candidates:**
- Churches? (denomination/organisation + building)
- Cricket/Football clubs? (organisation + ground/facility)
- Hotels? (business + building) - probably not dual-nature, just buildings

**Future:** Review all institutional tags for dual-nature potential.

