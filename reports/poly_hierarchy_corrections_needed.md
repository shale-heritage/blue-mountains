# Poly-Hierarchy Corrections Needed

**Date:** 2025-10-20
**Status:** Issues identified, corrections pending

---

## Issue 1: Inconsistent Intermediate Facets

### Problem
Under "Occupations", intermediate facets are inconsistent:

**CORRECT pattern (Clergy):**
```
Occupations
└── Clergy (occupational category)
    ├── Cardinal Moran (individual)
    ├── Reverend F V Pratt (individual)
    └── ... (other individuals)
```

**INCORRECT pattern (Law enforcement):**
```
Occupations
└── Law enforcement (occupational category)
    ├── Police (role/type) ← SHOULD BE INTERMEDIATE
    ├── Senior-Constable Illingworth (individual) ← SHOULD BE UNDER Police
    ├── Constable Orr (individual) ← SHOULD BE UNDER Police
    └── ... (other individuals)
```

### Solution
Add "Police" as intermediate facet, move named individuals under it:

**CORRECTED pattern:**
```
Occupations
└── Law enforcement (occupational category)
    └── Police (role/type - INTERMEDIATE FACET)
        ├── Senior-Constable Illingworth (individual)
        ├── Senior-Constable Thorncroft (individual)
        ├── Constable Orr (individual)
        ├── Constable John Hamilton (individual)
        ├── Constable O'Reilly (individual)
        ├── Constable White (individual)
        └── Sergeant Thorndyke (individual)
```

---

## Issue 2: Should Law Enforcement and Legal Officials Be Combined?

### Current Structure
```
Occupations
├── Law enforcement
│   └── Police → [7 constables/sergeants]
└── Legal officials
    ├── Coroner
    └── Coroner Lethbridge
```

### Analysis
- **Law enforcement**: 1 subcategory (Police)
- **Legal officials**: 1 subcategory (Coroner)

### Getty AAT Considerations
Let me check Getty AAT structure for guidance...

**Getty AAT structure for legal professions:**
- "law enforcement agents" (category)
  - police officers
  - constables
  - sergeants
- "legal professionals" (category)
  - lawyers
  - judges
  - coroners

**Recommendation:** **KEEP SEPARATE** for Getty AAT mapping compatibility.
- Coroners are legal/judicial officials, not law enforcement
- Getty AAT distinguishes between law enforcement and legal professionals
- Future tags might include: lawyers, magistrates, judges (legal professionals) vs sheriffs, bailiffs (law enforcement)

---

## Issue 3: "Colliery" Placement and Classification

### Current Status
- Tag: "Colliery" (4 items)
- Placement: Mining companies AND Mining infrastructure (dual classification)

### Evidence from Primary Sources

**Context 1 (1890):** "Katoomba Colliery changed hands this week"
**Context 2 (1905):** "lessee of the Katoomba colliery"
**Context 3 (1903):** "Operations at the various collieries throughout the valley" (generic plural)

### Analysis
"Colliery" appears to be:
1. A shortened reference to "Katoomba Colliery" (specific entity)
2. Sometimes used generically for coal mining operations

### Related Tags
- "Katoomba coal mines" (9 items) - generic reference to mines in Katoomba
- "Katoomba Coal and Shale Company" (7 items) - company name
- "Katoomba Coal and Shale Mines" (2 items) - company name (based on context analysis)
- "Katoomba Shale Mine" - specific mine site

### Recommendation
**Option A:** MERGE "Colliery" → "Katoomba Coal and Shale Company" (if they're the same entity)
**Option B:** RENAME "Colliery" → "Katoomba Colliery" (make explicit)
**Option C:** DELETE "Colliery" (too ambiguous - retain only specific company/mine names)

**PREFERRED:** **Option C - DELETE** (too generic/ambiguous)
- Reviewers can use more specific tags: "Katoomba Coal and Shale Company", "Katoomba coal mines", etc.
- Avoids ambiguity

---

## Issue 4: Mining Companies vs Mine Sites

### Problem
Some entities under "Mining companies" are actually physical mine sites, not companies.

### Entities Currently Under "Mining companies"

| Entity | Type | Evidence | Correct? |
|--------|------|----------|----------|
| A.K.O. & M. Company | Company | Has "Company" in name | ✅ YES |
| Australian Kerosene Shale and Oil Company | Company | Has "Company" in name | ✅ YES |
| Katoomba Coal and Shale Company | Company | Has "Company" in name | ✅ YES |
| Katoomba Coal and Shale Mines | Company | "the Company require 500 men" | ✅ YES |
| Gladstone Coal Company | Company | Has "Company" in name | ✅ YES |
| Sunny Corner Mining Company | Company | Has "Company" in name | ✅ YES |
| South Clifton Mine Co. | Company | Has "Co." in name | ✅ YES |
| South Clifton Tunnel Mine | **MINE SITE** | "killed... in the South Clifton Tunnel Mine" | ❌ NO - MOVE |
| New South Wales Shale and Oil Co. | Company | Has "Co." in name | ✅ YES |
| Waudby & Co. | Company | Has "& Co." in name | ✅ YES |
| Colliery | Ambiguous | See Issue 3 | ❌ NO - DELETE |

### Corrections Needed

**1. MOVE "South Clifton Tunnel Mine"**
- FROM: Organizations > Commercial businesses > Mining companies
- TO: Places > Mining districts > South Clifton > South Clifton Tunnel Mine

**2. DELETE "Colliery"**
- FROM: Organizations > Commercial businesses > Mining companies
- AND: Built Environment > Mining infrastructure
- REASON: Too ambiguous/generic

---

## Issue 5: Other Inconsistent Intermediate Facets

### Areas to Check
Need to systematically review ALL occupational categories for consistent intermediate facet usage:

1. ✅ **Medical professionals** - NO INTERMEDIATE NEEDED (all are individual doctors)
2. ✅ **Clergy** - NO INTERMEDIATE NEEDED (all are individual clergy)
3. ❌ **Law enforcement** - NEEDS "Police" intermediate (see Issue 1)
4. **Legal officials** - Check if "Coroner" should be intermediate or if both tags refer to same person
5. ✅ **Public officials** - NO INTERMEDIATE NEEDED (diverse roles: Aldermen, Licensing inspector, Stationmaster, Minister)
6. ✅ **Hospitality workers** - Only 1 tag (Publican)
7. ✅ **Military personnel** - Only 1 tag (Soldiers)

### Legal Officials: Coroner Pattern

**Current:**
```
Legal officials
├── Coroner (generic role)
└── Coroner Lethbridge (specific individual)
```

**Question:** Is "Coroner" a role or a specific person?

Let me check frequency:
- "Coroner" - needs context check
- "Coroner Lethbridge" - clearly an individual

**Recommendation:** Follow clergy pattern:
```
Legal officials
└── Coroners (occupational category - PLURAL)
    ├── Coroner Lethbridge (individual)
    └── Coroner (generic/unidentified coroner)
```

OR if "Coroner" refers to generic usage (e.g., "the coroner ruled"):
```
Legal officials
├── Coroner (generic role - when specific individual not named)
└── Coroner Lethbridge (specific individual)
```

**Need to check primary source context for "Coroner" tag.**

---

## Summary of All Corrections Needed

### 1. Add Intermediate Facets
- [ ] Law enforcement > Police > [move all constables/sergeants here]
- [ ] Check Legal officials > Coroner pattern

### 2. Delete Tags
- [ ] Delete "Colliery" (ambiguous/generic)

### 3. Move Tags
- [ ] Move "South Clifton Tunnel Mine" from mining companies to Places > Mining districts

### 4. Create New Parent Categories
- [ ] "South Clifton" under Mining districts (if doesn't exist)
- [ ] "Coroners" (plural) under Legal officials (if pattern matches clergy)

### 5. Systematic Review
- [ ] Review ALL occupational categories for consistent intermediate facet usage
- [ ] Review all organization subcategories for consistent patterns

---

## Next Steps

1. Check "Coroner" tag context in primary sources
2. Systematically review all occupational categories
3. Create corrected version of scripts/22_generate_poly_hierarchy.py
4. Regenerate data/poly_hierarchy_additions.csv
5. Regenerate all visualizations
6. Validate corrections

---

**Analysis by:** Claude Code
**Date:** 2025-10-20
**Status:** Awaiting user approval before implementing fixes
