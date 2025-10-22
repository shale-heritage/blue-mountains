# Intermediate Facets Corrections - Validation Report

**Date:** 2025-10-20
**Status:** ✅ ALL CORRECTIONS VALIDATED

---

## Corrections Implemented

### ✅ 1. Coroners Intermediate Facet Added

**Before:**
```
Legal officials
├── Coroner (generic - 1 item)
└── Coroner Lethbridge (individual - 2 items)
```

**After:**
```
Legal officials
└── Coroners (intermediate facet - PLURAL)
    ├── Coroner (generic - 1 item)
    └── Coroner Lethbridge (individual - 2 items)
```

**Validation:** ✅ Confirmed in `primary_agents.txt`

---

### ✅ 2. Courts - Generic Tag Properly Nested

**Structure:**
```
Government bodies
└── Courts (intermediate - PLURAL)
    ├── Court (generic - 45 items)
    ├── Katoomba Court
    ├── Licensing Court
    ├── Police court
    └── Supreme Court
```

**Validation:** ✅ Confirmed - Court appears under Courts, not as sibling

---

### ✅ 3. Churches - Generic Tag Properly Nested

**Structure:**
```
Religious organizations
└── Churches (intermediate - PLURAL)
    ├── Church (generic - 34 items)
    ├── Congregational Church
    ├── Katoomba Congregational Church
    ├── Methodist Church
    ├── Roman Catholic Church
    ├── St Hilda's Church
    └── Wesleyan Church
```

**Validation:** ✅ Confirmed - Church appears under Churches

---

### ✅ 4. Performance Groups - Bands and Choirs

**Structure:**
```
Performance groups
├── Bands (intermediate - PLURAL)
│   ├── Band (generic - 8 items)
│   └── Katoomba band
├── Choirs (intermediate - PLURAL)
│   └── Choir (generic - 1 item)
└── Minstrel troupes
    └── Katoomba Amateur Minstrels
```

**Validation:** ✅ Confirmed - Band and Choir under plural intermediates

---

### ✅ 5. Rifle Clubs

**Structure:**
```
Sports clubs
└── Rifle clubs (intermediate - PLURAL)
    └── Rifle club (generic - 1 item)
```

**Validation:** ✅ Confirmed - Rifle club under Rifle clubs

---

### ✅ 6. Halls Moved from Organizations to Built Environment

**Before (INCORRECT):**
```
Organizations
└── Fraternal orders & lodges
    └── Lodges
        ├── Masons
        │   └── Masonic Hall ❌ (building, not organization)
        └── Odd Fellows
            └── Odd Fellows' Hall ❌ (building, not organization)
```

**After (CORRECT):**
```
Organizations
└── Fraternal orders & lodges
    └── Lodges
        ├── Freemasons
        │   └── Masons
        └── Independent Order of Odd Fellows
            └── Oddfellows
        (No halls - moved to Built Environment)

Built Environment
└── Community buildings
    └── Halls
        ├── Masonic Hall ✅
        ├── Odd Fellows' Hall ✅
        └── [other halls]
```

**Validation:** ✅ Confirmed - Halls in Built Environment only, NOT in Organizations

---

### ✅ 7. Fraternal Organizations - Standardized Names

**Before:**
```
Lodges
├── Odd Fellows
│   ├── Oddfellows
│   └── Odd Fellows' Hall (building)
├── Masons
│   └── Masonic Hall (building)
└── Druids
    ├── U.A.O.D.
    └── Druid's Lodge
```

**After:**
```
Lodges
├── Independent Order of Odd Fellows (preferred term)
│   └── Oddfellows (variant name)
├── Freemasons (preferred term)
│   └── Masons (variant name)
└── United Ancient Order of Druids (preferred term)
    ├── U.A.O.D. (acronym variant)
    └── Druid's Lodge (local lodge name)
```

**Validation:** ✅ Confirmed - Full names used, variants nested under them

---

## Systematic Pattern Consistency Verified

### Rule: Generic Singular Tags

**When a generic singular tag exists (Court, Church, Band, etc.):**
- ✅ Create plural intermediate category
- ✅ Place generic tag UNDER the intermediate (like any other tag)
- ✅ Place specific tags also under the intermediate

**Applied consistently to:**
- ✅ Coroners > Coroner, Coroner Lethbridge
- ✅ Courts > Court, [specific courts]
- ✅ Churches > Church, [specific churches]
- ✅ Bands > Band, [specific bands]
- ✅ Choirs > Choir
- ✅ Rifle clubs > Rifle club

---

## Buildings vs Organizations Distinction

**Rule:** Entities ending in "Hall" are BUILDINGS

**Applied:**
- ✅ Masonic Hall → Built Environment > Halls
- ✅ Odd Fellows' Hall → Built Environment > Halls
- ✅ Clarke's Hall → Built Environment > Halls
- ✅ Waudby's Hall → Built Environment > Halls
- ✅ Mount Victoria Hall → Built Environment > Halls

**Organizations remain in Organizations facet:**
- ✅ Freemasons (organization)
- ✅ Independent Order of Odd Fellows (organization)
- ✅ United Ancient Order of Druids (organization)

**Consistent with earlier pattern:**
- Companies (organizations) vs Mine sites (places)
- Hotels (organizations AND buildings via poly-hierarchy)
- Churches (organizations AND buildings via poly-hierarchy)

---

## Summary Statistics

### Changes Made
- Added intermediate facets: 1 (Coroners)
- Moved entities: 2 (Masonic Hall, Odd Fellows' Hall)
- Renamed/standardized: 3 fraternal organizations
- Fixed nesting: 6 generic tags already correct
- Total hierarchy rows: 532 (unchanged - additions balanced by removals)

### Validation Checks Performed
- [x] Coroners intermediate facet present
- [x] Court under Courts (not sibling)
- [x] Church under Churches (not sibling)
- [x] Band under Bands (not sibling)
- [x] Choir under Choirs (not sibling)
- [x] Rifle club under Rifle clubs (not sibling)
- [x] Masonic Hall ONLY in Built Environment (not in Organizations)
- [x] Odd Fellows' Hall ONLY in Built Environment (not in Organizations)
- [x] Fraternal organizations use full names with variants nested
- [x] All generic tags treated consistently

---

## Files Modified

1. ✅ `scripts/22_generate_poly_hierarchy.py` - all corrections applied
2. ✅ `data/poly_hierarchy_additions.csv` - regenerated (532 rows)
3. ✅ `visualizations/hierarchy_trees/*.txt` - all 87 trees regenerated

---

## Thesaurus Entries Required (Phase 1.2.2)

Add to `docs/tag_definitions.md`:

### United Ancient Order of Druids
**Preferred term:** United Ancient Order of Druids
**Variants:**
- U.A.O.D. (acronym)
- Druids (informal)

**Scope note:** Fraternal organization. "Jersey Lodge U.A.O.D." was the Katoomba local lodge established 1892.

### Independent Order of Odd Fellows
**Preferred term:** Independent Order of Odd Fellows
**Variants:**
- Oddfellows (variant spelling)
- Odd Fellows (abbreviated)

**Scope note:** Fraternal organization. Use "Odd Fellows' Hall" for the building.

### Freemasons
**Preferred term:** Freemasons
**Variants:**
- Masons (informal)

**Scope note:** Fraternal organization. Use "Masonic Hall" for the building.

---

## Next Steps

1. ✅ **COMPLETE:** All intermediate facet corrections applied
2. ✅ **COMPLETE:** Buildings vs organizations distinction enforced
3. ✅ **COMPLETE:** Fraternal organization names standardized
4. **PENDING:** Create scope notes in tag_definitions.md (Phase 1.2.2)
5. **PENDING:** Add variant mappings to tag_consolidation_map.csv
6. **PENDING:** Apply changes to Zotero (Phase 1.4)

---

## Conclusion

✅ **All corrections successfully implemented and validated**

The poly-hierarchical taxonomy now has:
- **Consistent intermediate facet usage** throughout
- **Generic tags properly nested** under plural intermediates
- **Buildings correctly classified** in Built Environment (not Organizations)
- **Standardized organization names** with variants documented
- **532 well-structured hierarchy relationships**

**Pattern established:**
> When a generic singular tag exists, create a plural intermediate category and place the generic tag under it like any other tag.

**Ready for:**
- Phase 1.2.2 (Tag definitions & scope notes)
- Phase 1.3 (Getty AAT mapping)
- Phase 1.4 (Apply to Zotero)

---

**Validation completed by:** Claude Code
**Date:** 2025-10-20
**Status:** ✅ APPROVED FOR NEXT PHASE
