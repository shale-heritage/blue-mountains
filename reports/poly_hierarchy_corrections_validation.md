# Poly-Hierarchy Corrections Validation Report

**Date:** 2025-10-20
**Status:** ✅ ALL CORRECTIONS VALIDATED

---

## Corrections Implemented

### ✅ 1. Intermediate Facet Added - Law Enforcement

**Issue:** Police appeared at same level as individual constables/sergeants

**Fix Applied:**
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

**Validation:** ✅ Confirmed in `primary_agents.txt` lines 22-30

---

### ✅ 2. Company Names Standardised

**Issue:** Inconsistent abbreviations ("Co.", "&") in company names

**Fixes Applied:**
- Spelled out "Co." as "Company" throughout
- Spelled out "&" as "and" throughout
- Dropped "Limited"/"Ltd." for brevity

**Before → After:**
- `A.K.O. & M. Company` → `Australian Kerosene Oil and Mineral Company`
- `South Clifton Mine Co.` → `South Clifton Mine Company`
- `New South Wales Shale and Oil Co.` → `New South Wales Shale and Oil Company`
- `Waudby & Co.` → `Waudby and Company`
- `Douglas & Co.` → `Douglas and Company`
- `Tabrett and Co.` → `Tabrett and Company`
- `Retailers & stores` → `Retailers and stores`

**Validation:** ✅ Confirmed in `primary_agents.txt` lines 98-111

---

### ✅ 3. Preferred Terms Used

**Issue:** Multiple name variants for same company

**Fix Applied:** Used official registered names as preferred terms
- `A.K.O. & M. Company` merged into `Australian Kerosene Oil and Mineral Company`
- `Katoomba Coal and Shale Mines` merged into `Katoomba Coal and Shale Company`

**Note:** Variant mappings documented in `docs/thesaurus_structure.md`

**Validation:** ✅ Only preferred terms appear in hierarchy

---

### ✅ 4. "Colliery" Tag Removed

**Issue:** "Colliery" was ambiguous/generic

**Fix Applied:**
- Removed from Organizations > Mining companies
- Removed from Built Environment > Mining infrastructure

**Items tagged "Colliery" (4 total):**
- Items 1 & 3: Replace with `Katoomba Coal and Shale Company` (Phase 1.4)
- Items 2 & 4: Replace with `Coal mining` tag (Phase 1.4)

**Validation:** ✅ Confirmed absent from both `primary_agents.txt` and `primary_built_environment.txt`

---

### ✅ 5. Mine Site Moved to Correct Location

**Issue:** "South Clifton Tunnel Mine" incorrectly placed under mining companies (it's a physical site, not a company)

**Fix Applied:**
- Removed from Organizations > Commercial businesses > Mining companies
- Added to Places > Mining districts > South Clifton > South Clifton Tunnel Mine
- Created new intermediate: "South Clifton" mining district

**Validation:** ✅ Confirmed in `primary_places.txt` lines 12-13

---

## Summary Statistics

### Before Corrections
- Total hierarchy relationships: 558
- Mining companies: 11 (including Colliery and South Clifton Tunnel Mine)
- Law enforcement: 8 entities at same level

### After Corrections
- Total hierarchy relationships: 555 (−3)
- Mining companies: 7 (all valid companies with standardised names)
- Law enforcement: 1 intermediate (Police) + 7 individuals under it
- Mining districts: Added South Clifton with South Clifton Tunnel Mine

---

## Files Modified

1. ✅ `scripts/22_generate_poly_hierarchy.py` - corrected version with documentation
2. ✅ `data/poly_hierarchy_additions.csv` - regenerated with 555 rows
3. ✅ `visualizations/hierarchy_trees/*.txt` - all 87 tree files regenerated

---

## New Documentation Created

1. ✅ `docs/thesaurus_structure.md` - comprehensive guide for handling name changes
2. ✅ `reports/mining_entities_classification.md` - analysis of company vs mine site
3. ✅ `reports/mining_entity_context_analysis.txt` - primary source evidence
4. ✅ `reports/poly_hierarchy_corrections_plan.md` - detailed implementation plan
5. ✅ This validation report

---

## Validation Checks Performed

### Law Enforcement Intermediate Facet
- [x] "Police" appears as child of "Law enforcement"
- [x] All 7 constables/sergeants appear as children of "Police"
- [x] No individuals directly under "Law enforcement"

### Mining Companies
- [x] Only 7 valid company entries
- [x] All names spelled out (no "Co." or "&")
- [x] "Colliery" absent
- [x] "South Clifton Tunnel Mine" absent
- [x] "Australian Kerosene Oil and Mineral Company" present (preferred term)

### Places > Mining Districts
- [x] "South Clifton" present as mining district
- [x] "South Clifton Tunnel Mine" present as child of South Clifton
- [x] Pattern matches Ruined Castle and Nellie's Glen

### Retailers and Stores
- [x] Category renamed to "Retailers and stores" (no "&")
- [x] All company names spelled out

---

## Systematic Pattern Consistency Check

### ✅ Intermediate Facets Pattern
All occupational categories follow consistent pattern:

| Category | Intermediate? | Pattern |
|----------|---------------|---------|
| Medical professionals | No | All are individual doctors (no intermediate needed) |
| Clergy | No | All are individual clergy (no intermediate needed) |
| **Law enforcement** | **Yes ✅** | **Police → [individuals]** |
| Legal officials | No | 1 generic + 1 named individual (acceptable) |
| Public officials | No | Diverse roles (no intermediate needed) |
| Hospitality workers | No | Only 1 tag |
| Military personnel | No | Only 1 tag |

**Result:** ✅ Consistent across all categories

### ✅ Organizations Pattern
All organisation subcategories follow consistent pattern:

| Category | Intermediate? | Pattern |
|----------|---------------|---------|
| Sports clubs | Yes ✅ | [Sport type] clubs → [specific clubs] |
| Performance groups | Yes ✅ | [Performance type] → [specific groups] |
| Lodges | Yes ✅ | [Lodge type] → [specific lodges] |
| Mining companies | No | All are companies (no intermediate needed) |
| Hotels | No | All are hotels (no intermediate needed) |

**Result:** ✅ Consistent across all categories

---

## Next Steps

### Phase 1.2.2: Tag Definitions & Scope Notes
Create `docs/tag_definitions.md` with:
- [ ] Scope note for "Australian Kerosene Oil and Mineral Company" (include all variants)
- [ ] Scope note for "Katoomba Coal and Shale Company" (include all variants)
- [ ] Scope notes for all mining companies explaining company vs mine site distinction
- [ ] Scope notes for all 481 tags

### Phase 1.2.3: Variant Mappings
Update `data/tag_consolidation_map.csv` with MERGE actions:
- [ ] `A.K.O. & M. Company` → `Australian Kerosene Oil and Mineral Company`
- [ ] `Australian Kerosene Shale and Oil Company` → `Australian Kerosene Oil and Mineral Company`
- [ ] `Katoomba Coal and Shale Mines` → `Katoomba Coal and Shale Company`
- [ ] `South Clifton Mine Co.` → `South Clifton Mine Company`
- [ ] `New South Wales Shale and Oil Co.` → `New South Wales Shale and Oil Company`
- [ ] `Waudby & Co.` → `Waudby and Company`
- [ ] `Tabrett and Co.` → `Tabrett and Company`
- [ ] `Douglas & Co.` → `Douglas and Company`

### Phase 1.4: Apply to Zotero
- [ ] ⚠️ **BACKUP** Zotero library before any changes
- [ ] Re-tag 2 items from "Colliery" to "Katoomba Coal and Shale Company"
- [ ] Re-tag 2 items from "Colliery" to "Coal mining"
- [ ] Apply all variant merges via Zotero API
- [ ] Validate changes

---

## Conclusion

✅ **All corrections successfully implemented and validated**

The poly-hierarchical taxonomy now has:
- Consistent intermediate facet usage
- Standardised company names (spelled out, preferred terms)
- Correct placement of mine sites vs companies
- Removed ambiguous tags
- 555 well-structured hierarchy relationships

**Ready for:**
- Phase 1.2.2 (Tag definitions & scope notes)
- Phase 1.3 (Getty AAT mapping)
- Phase 1.4 (Apply to Zotero)

---

**Validation completed by:** Claude Code
**Date:** 2025-10-20
**Status:** ✅ APPROVED FOR NEXT PHASE
