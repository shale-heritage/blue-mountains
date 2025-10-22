# Intermediate Facets Consistency Analysis

**Date:** 2025-10-20
**Purpose:** Systematically address inconsistencies in intermediate facet usage

---

## Issue 1: Coroner/Coroner Lethbridge Pattern

### Current (Incorrect)
```
Legal officials
├── Coroner (generic - 1 item)
└── Coroner Lethbridge (individual - 2 items)
```

### Should Be (Following Clergy Pattern)
```
Legal officials
└── Coroners (intermediate category - PLURAL)
    ├── Coroner (generic/unidentified coroner - 1 item)
    └── Coroner Lethbridge (identified individual - 2 items)
```

**Justification:** Follows clergy pattern consistently

---

## Issue 2: Generic Singular Tags (Band, Choir, Court, Church, Rifle club)

### Analysis

These ARE actual tags used when specific entity not named:

| Tag | Item Count | Usage |
|-----|-----------|-------|
| Court | 45 items | Generic court (not Supreme/Police/Licensing Court) |
| Church | 34 items | Generic church (not Methodist/Catholic/etc.) |
| Band | 8 items | Generic band (not Katoomba band) |
| Choir | 1 item | Generic choir |
| Rifle club | 1 item | Generic rifle club |
| Coroner | 1 item | Generic coroner (not Coroner Lethbridge) |

### Decision: KEEP Generic Tags

**Rationale:**
- These represent REAL tagging usage
- Used when source mentions "the court" or "the church" without specifying which one
- NOT structural placeholders

### Current Pattern (INCONSISTENT)

**Pattern A: Generic as sibling (INCORRECT)**
```
Bands (category)
├── Band (generic) ← sibling to specific bands
└── Katoomba band (specific)
```

**Pattern B: No generic (ACCEPTABLE when count is low)**
```
Cricket clubs (category)
├── Katoomba Cricket Club
└── Megalong Cricket Club
(No generic "Cricket club" tag exists)
```

### Correct Pattern: Generic UNDER Intermediate

When generic tag exists (>0 items), treat it like named entities:

```
Performance groups
└── Bands (intermediate category - PLURAL)
    ├── Band (generic - 8 items)
    └── Katoomba band (specific - N items)
```

```
Choirs (intermediate category - PLURAL)
└── Choir (generic - 1 item)
(No specific named choirs exist)
```

```
Rifle clubs (intermediate category - PLURAL)
└── Rifle club (generic - 1 item)
(No specific named rifle clubs exist)
```

**Key Principle:** Generic singular tag is treated like any other tag under the plural intermediate category.

---

## Issue 3: Courts/Court and Churches/Church

### Courts

**Tag frequency:**
- Court: 45 items (generic)
- Katoomba Court: N items
- Supreme Court: N items
- Police court: N items
- Licensing Court: N items

**Current structure:**
```
Courts (category)
├── Court (generic) ← SHOULD BE UNDER intermediate
├── Katoomba Court
├── Supreme Court
├── Police court
└── Licensing Court
```

**Correct structure:**
```
Government bodies
└── Courts (intermediate category - PLURAL)
    ├── Court (generic court references - 45 items)
    ├── Katoomba Court (specific court)
    ├── Licensing Court (specific court)
    ├── Police court (specific court)
    └── Supreme Court (specific court)
```

### Churches

**Tag frequency:**
- Church: 34 items (generic)
- Methodist Church: N items
- Wesleyan Church: N items
- etc.

**Correct structure:**
```
Religious organizations
└── Churches (intermediate category - PLURAL)
    ├── Church (generic church references - 34 items)
    ├── Congregational Church (denominational)
    ├── Katoomba Congregational Church (specific)
    ├── Methodist Church (denominational)
    ├── Roman Catholic Church (denominational)
    ├── St Hilda's Church (specific)
    └── Wesleyan Church (denominational)
```

---

## Issue 4: Halls vs Organizations (Masonic, Odd Fellows, Druids)

### Evidence from Primary Sources

**Masonic Hall:**
- "auction sale of furniture **in** the Masonic Hall"
- "dance was held **at** the Masonic Hall"
- "commences **in** the Masonic Hall"
- **CONCLUSION:** BUILDING (use locational prepositions)

**Odd Fellows' Hall:**
- Similar pattern expected
- **CONCLUSION:** BUILDING

**Druid's Lodge:**
- "forming a Druid's Lodge" (organization)
- Could refer to meeting place (building)
- **CONCLUSION:** AMBIGUOUS - could be both

### Correct Classification

**Buildings → Built Environment:**
```
Built Environment
└── Community buildings
    └── Halls
        ├── Masonic Hall (building)
        ├── Odd Fellows' Hall (building)
        └── [other halls]
```

**Organizations → Agents:**
```
Organizations
└── Fraternal orders & lodges
    └── Lodges
        ├── Druids
        │   ├── United Ancient Order of Druids (U.A.O.D.) (organization - preferred term)
        │   └── Druid's Lodge (local lodge OR building - needs disambiguation)
        ├── Masons (organization)
        ├── Odd Fellows (organization - Oddfellows variant)
        └── [other lodges]
```

**Problem:** Current hierarchy has "Masonic Hall" under Organizations/Lodges/Masons (INCORRECT)

---

## Issue 5: Fraternal Organization Names

### Current Tags (from tag_frequency.csv)
- U.A.O.D.: 3 items
- Druid's Lodge: 4 items
- Masons: 3 items
- Oddfellows: 2 items
- Odd Fellows' Hall: 24 items

### Evidence from Primary Sources

**U.A.O.D.:**
- Full name: "United Ancient Order of Druids"
- "Jersey Lodge U.A.O.D." (local lodge)
- "officers of the Jersey Lodge U.A.O.D."

**Druid's Lodge:**
- "forming a Druid's Lodge"
- Could mean local Druids lodge OR the building

### Standardized Names (Following Company Name Pattern)

| Current Tag | Preferred Term | Notes |
|-------------|----------------|-------|
| U.A.O.D. | United Ancient Order of Druids | Spell out acronym |
| Druid's Lodge | Druid's Lodge | Keep as-is (local lodge name) OR disambiguate building vs org |
| Masons | Freemasons | Use proper name |
| Oddfellows | Independent Order of Odd Fellows | Use proper name if confirmed |
| Masonic Hall | Masonic Hall | BUILDING - move to Built Environment |
| Odd Fellows' Hall | Odd Fellows' Hall | BUILDING - move to Built Environment |

### Recommended Hierarchy

```
Fraternal orders & lodges
└── Lodges
    ├── Freemasons
    │   └── (No specific lodge names - just "Masons" tag)
    ├── Independent Order of Odd Fellows
    │   └── (Oddfellows variant name)
    └── United Ancient Order of Druids
        └── Druid's Lodge (if organization - check context)
```

**Buildings moved to:**
```
Built Environment > Community buildings > Halls
├── Masonic Hall
└── Odd Fellows' Hall
```

---

## Summary of Required Corrections

### 1. Add Intermediate Facets

- [ ] Coroners (plural) with Coroner + Coroner Lethbridge under it
- [ ] Courts (already exists, move Court under it)
- [ ] Churches (already exists, move Church under it)
- [ ] Bands (already exists, ensure Band is under it properly)
- [ ] Choirs (ensure Choir is under it properly)
- [ ] Rifle clubs (ensure Rifle club is under it properly)

### 2. Move Buildings from Organizations to Built Environment

- [ ] Masonic Hall: FROM Organizations/Lodges → TO Built Environment/Halls
- [ ] Odd Fellows' Hall: FROM Organizations/Lodges → TO Built Environment/Halls

### 3. Standardize Fraternal Organization Names

- [ ] U.A.O.D. → United Ancient Order of Druids (preferred term, add U.A.O.D. to thesaurus)
- [ ] Masons → Freemasons (if appropriate)
- [ ] Oddfellows → Independent Order of Odd Fellows (if confirmed)

### 4. Disambiguate Druid's Lodge

- [ ] Check primary sources: building OR organization?
- [ ] If building: move to Built Environment/Halls
- [ ] If organization: keep under Lodges/United Ancient Order of Druids
- [ ] If both: create two separate tags with (building) and (organization) suffixes

### 5. Systematic Pattern Enforcement

**Rule:** When a generic singular tag exists (Court, Church, Band, Choir, Coroner, etc.):
- Create plural intermediate category (Courts, Churches, Bands, Choirs, Coroners)
- Place generic AND specific tags under it
- Treat generic tag like any other tag (not as special structural element)

**When NO generic tag exists:**
- Can have intermediate category without generic (e.g., Cricket clubs → [specific clubs only])

---

## Implementation Checklist

- [ ] Update script 22 with all corrections
- [ ] Move Masonic Hall and Odd Fellows' Hall to Built Environment
- [ ] Add Coroners intermediate facet
- [ ] Ensure all generic tags properly nested under intermediates
- [ ] Standardize fraternal organization names
- [ ] Add variants to thesaurus (U.A.O.D., etc.)
- [ ] Check Druid's Lodge context and classify appropriately
- [ ] Regenerate CSV and visualizations
- [ ] Validate all changes

---

**Analysis by:** Claude Code
**Date:** 2025-10-20
**Status:** Ready for user approval before implementation
