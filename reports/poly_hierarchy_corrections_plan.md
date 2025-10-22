# Poly-Hierarchy Corrections Implementation Plan

**Date:** 2025-10-20
**Status:** Ready to implement

---

## Summary of Corrections

1. ✅ Add intermediate facets consistently (Priority: HIGH)
2. ✅ Standardize company names to official registered names
3. ✅ Spell out "Co." as "Company" consistently
4. ✅ Add "(company)" suffix where name is ambiguous
5. ✅ Move mine sites to correct location (Places > Mining districts)
6. ✅ Handle "Colliery" tag appropriately

---

## 1. Intermediate Facets - Systematic Fixes

### Current Inconsistencies

**CORRECT pattern (Clergy):**
```
Occupations > Clergy > [individual clergy members]
```

**INCORRECT pattern (Law enforcement):**
```
Occupations > Law enforcement > Police (should be intermediate)
                              > [individual officers - should be under Police]
```

### Fix Required

**Law enforcement - ADD "Police" intermediate:**
```
Occupations
└── Law enforcement
    └── Police (INTERMEDIATE FACET)
        ├── Constable John Hamilton
        ├── Constable O'Reilly
        ├── Constable Orr
        ├── Constable White
        ├── Senior-Constable Illingworth
        ├── Senior-Constable Thorncroft
        └── Sergeant Thorndyke
```

**Legal officials - NO CHANGE NEEDED:**
```
Occupations
└── Legal officials
    ├── Coroner (generic/unidentified - 1 item only)
    └── Coroner Lethbridge (specific individual)
```
*Pattern is acceptable because "Coroner" is generic usage, not an individual*

### Systematic Review Needed

Check ALL organization subcategories for consistent intermediate facet usage:
- [ ] Sports clubs → [Sport type] clubs → [specific clubs] ✅ (already correct)
- [ ] Performance groups → [Performance type] → [specific groups] ✅ (already correct)
- [ ] Mining companies → [specific companies] ✅ (no intermediate needed - all are companies)
- [ ] Hotels → [specific hotels] ✅ (no intermediate needed - all are hotels)
- [ ] Lodges → [Lodge type] → [specific lodges] ✅ (already correct: Odd Fellows, Masons, Druids, Independent lodges)

**CONCLUSION:** Only Law enforcement needs fixing. Others are already consistent.

---

## 2. Mining Company Name Standardization

### Research Findings

| Current Tag Name | Official Registered Name | Action Required |
|------------------|-------------------------|-----------------|
| A.K.O. & M. Company | Australian Kerosene Oil and Mineral Company Limited | RENAME + spell out |
| Australian Kerosene Shale and Oil Company | Australian Kerosene Oil and Mineral Company Limited | MERGE with above OR verify if different entity |
| Katoomba Coal and Shale Company | Katoomba Coal and Shale Company Limited | ADD "Limited" |
| Katoomba Coal and Shale Mines | Katoomba Coal and Shale Company Limited (company name) | MERGE OR add "(company)" suffix |
| South Clifton Mine Co. | South Clifton Mine Company | Spell out "Co." |
| New South Wales Shale and Oil Co. | New South Wales Shale and Oil Company | Spell out "Co." |
| Waudby & Co. | Waudby and Company | Spell out "Co." AND "&" |

### Specific Actions

**A. MERGE:** "A.K.O. & M. Company" → "Australian Kerosene Oil and Mineral Company"
- Full official name: "Australian Kerosene Oil and Mineral Company Limited"
- For tag: Use "Australian Kerosene Oil and Mineral Company" (drop "Limited" for brevity)
- Add scope note: "Abbreviated as A.K.O. & M. Company or A.K.O."

**B. CHECK:** "Australian Kerosene Shale and Oil Company" vs "Australian Kerosene Oil and Mineral Company"
- Are these the SAME company with name variants?
- OR different entities?
- Web search suggests "Australian Kerosene Oil and Mineral Company" is correct
- "Australian Kerosene Shale and Oil Company" might be informal variant
- **ACTION:** Merge into "Australian Kerosene Oil and Mineral Company" unless evidence of distinct entity

**C. MERGE:** "Katoomba Coal and Shale Mines" → "Katoomba Coal and Shale Company"
- Official name: "Katoomba Coal and Shale Company Limited" (est. 1885/1887)
- "Katoomba Coal and Shale Mines" refers to the same company (based on context analysis)
- **ACTION:** Merge both tags into "Katoomba Coal and Shale Company"

**D. SPELL OUT:** All "Co." → "Company", all "&" → "and"
- South Clifton Mine Co. → South Clifton Mine Company
- New South Wales Shale and Oil Co. → New South Wales Shale and Oil Company
- Waudby & Co. → Waudby and Company

---

## 3. "Colliery" Tag Handling

### All 4 Items Tagged "Colliery"

| Item | Date | Context | Action |
|------|------|---------|--------|
| 1. Local Jottings | 19 July 1890 | "Katoomba Colliery changed hands" | Replace with "Katoomba Coal and Shale Company" |
| 2. The Collieries and Big-Head Mines of NSW | 1887 | Article title (no context in notes) | KEEP tag OR use generic "Coal mining" theme tag |
| 3. NSW Railway Enquiry | 13 Dec 1905 | "lessee of the Katoomba colliery" | Replace with "Katoomba Coal and Shale Company" |
| 4. Mountain Industries | 7 April 1903 | "Operations at the various collieries" | KEEP tag OR use generic "Coal mining" theme tag |

### Decision

**Items 1 & 3:** "Katoomba Colliery" = shorthand for "Katoomba Coal and Shale Company"
- **ACTION:** Replace "Colliery" tag with "Katoomba Coal and Shale Company" tag

**Items 2 & 4:** Generic/multiple collieries
- **OPTION A:** Keep "Colliery" tag for generic usage
- **OPTION B:** Replace with thematic tag like "Coal mining" or "Mining industry"
- **RECOMMENDATION:** Option B - use "Coal mining" tag instead (more specific and avoids ambiguity)

**Final action:** DELETE "Colliery" from taxonomy, re-tag all 4 items appropriately

---

## 4. Mine Sites vs Companies

### Consistent Pattern

**COMPANIES (Organizations):** Organizations > Commercial businesses > Mining companies
- All entities with "Company"/"Co." in name
- Katoomba Coal and Shale Company (even though it operated mines)

**MINE SITES (Places):** Places > Mining districts > [District] > [Mine name]
- Ruined Castle Shale Mine ✅ (already correct)
- Nellie's Glen Shale Mine ✅ (already correct)
- South Clifton Tunnel Mine ❌ (needs to move here)

**MINE INFRASTRUCTURE (Built Environment):** Built Environment > Infrastructure > Mining infrastructure
- Tramway ✅
- Colliery ❌ (being deleted)

### Action Required

**MOVE:** South Clifton Tunnel Mine
- FROM: Organizations > Commercial businesses > Mining companies
- TO: Places > Mining districts > South Clifton > South Clifton Tunnel Mine

**CREATE:** New intermediate category "South Clifton" under Mining districts (if not already exists)

---

## 5. Complete List of CSV Changes

### A. Delete Rows

```csv
# DELETE - ambiguous/being merged
old_tag,new_tag,action,notes
Colliery,Colliery,hierarchy,parent=Mining companies
Colliery,Colliery,hierarchy,parent=Mining infrastructure
```

### B. Merge Tags (via tag_consolidation_map.csv)

```csv
# MERGE - name variants of same company
old_tag,new_tag,action,notes
A.K.O. & M. Company,Australian Kerosene Oil and Mineral Company,merge,Abbreviated name - merge to official registered name
Australian Kerosene Shale and Oil Company,Australian Kerosene Oil and Mineral Company,merge,Name variant - verify if same entity first
Katoomba Coal and Shale Mines,Katoomba Coal and Shale Company,merge,Company name variant - both refer to same company entity
```

### C. Rename Tags (spell out abbreviations)

```csv
# RENAME - spell out Co. as Company
old_tag,new_tag,action,notes
South Clifton Mine Co.,South Clifton Mine Company,rename,Spell out Co. as Company for consistency
New South Wales Shale and Oil Co.,New South Wales Shale and Oil Company,rename,Spell out Co. as Company
Waudby & Co.,Waudby and Company,rename,Spell out Co. and & for consistency
```

### D. Move Tags (correct placement)

```csv
# DELETE old placement
South Clifton Tunnel Mine,South Clifton Tunnel Mine,hierarchy,parent=Mining companies

# ADD new placement
South Clifton,South Clifton,hierarchy,parent=Mining districts
South Clifton Tunnel Mine,South Clifton Tunnel Mine,hierarchy,parent=South Clifton
```

### E. Add Intermediate Facets

```csv
# MODIFY - move individuals under Police intermediate
# DELETE these rows:
Senior-Constable Illingworth,Senior-Constable Illingworth,hierarchy,parent=Law enforcement
Senior-Constable Thorncroft,Senior-Constable Thorncroft,hierarchy,parent=Law enforcement
Constable Orr,Constable Orr,hierarchy,parent=Law enforcement
Constable John Hamilton,Constable John Hamilton,hierarchy,parent=Law enforcement
Constable O'Reilly,Constable O'Reilly,hierarchy,parent=Law enforcement
Constable White,Constable White,hierarchy,parent=Law enforcement
Sergeant Thorndyke,Sergeant Thorndyke,hierarchy,parent=Law enforcement

# MODIFY Police from sibling to intermediate:
# DELETE:
Police,Police,hierarchy,parent=Law enforcement

# ADD BACK as intermediate with children:
Police,Police,hierarchy,parent=Law enforcement (intermediate facet for constables/sergeants)
Senior-Constable Illingworth,Senior-Constable Illingworth,hierarchy,parent=Police
Senior-Constable Thorncroft,Senior-Constable Thorncroft,hierarchy,parent=Police
Constable Orr,Constable Orr,hierarchy,parent=Police
Constable John Hamilton,Constable John Hamilton,hierarchy,parent=Police
Constable O'Reilly,Constable O'Reilly,hierarchy,parent=Police
Constable White,Constable White,hierarchy,parent=Police
Sergeant Thorndyke,Sergeant Thorndyke,hierarchy,parent=Police
```

---

## 6. Implementation Steps

1. [ ] Update `scripts/22_generate_poly_hierarchy.py` with corrections
2. [ ] Regenerate `data/poly_hierarchy_additions.csv`
3. [ ] Review generated CSV for accuracy
4. [ ] Run `scripts/23_visualise_poly_hierarchy.py` to regenerate trees
5. [ ] Review tree visualizations for correctness
6. [ ] Update Zotero items:
   - Re-tag 2 items from "Colliery" to "Katoomba Coal and Shale Company"
   - Re-tag 2 items from "Colliery" to "Coal mining" (generic usage)
7. [ ] Update `docs/folksonomy_logic.md` with final structure

---

## 7. Questions Needing User Confirmation

**Q1:** Should we verify "Australian Kerosene Shale and Oil Company" vs "Australian Kerosene Oil and Mineral Company" are the same entity before merging?
- **Web search suggests:** Same company, name variant
- **Recommendation:** MERGE

**Q2:** For items #2 and #4 tagged "Colliery" (generic usage), replace with "Coal mining" thematic tag?
- **Recommendation:** YES - more specific than deleting

**Q3:** Should "Limited" / "Ltd." be included in company names or dropped for brevity?
- **Current practice:** Drop "Limited" for tag names, note in scope notes
- **Recommendation:** Continue this practice for consistency

---

**Ready to implement?** Please confirm and I'll proceed with updating the scripts and regenerating all files.
