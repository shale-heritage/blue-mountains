# CSV Hierarchy Fixes Summary

**Date:** 2025-10-30
**Script:** `scripts/40_fix_csv_hierarchy_issues.py`

---

## Changes Applied

### CSV Modifications
- **Original rows:** 1,005
- **Deleted rows:** 18
- **Final rows:** 987
- **Backup created:** `data/tag_map_consolidated.csv.backup-hierarchy-fixes`

---

## Issues Fixed

### 1. ✓ Agents Facet - Getty AAT Alignment

**Problem:** Demographic groups and Occupations appeared twice in the Agents tree - once as direct children of Agents, and again under People.

**Root Cause:** Incorrect poly-hierarchy within primary facet
```csv
Demographic groups -> parent=Agents ❌ (REMOVED)
Demographic groups -> parent=People ✓ (KEPT)
Occupations -> parent=Agents ❌ (REMOVED)
Occupations -> parent=People ✓ (KEPT)
```

**Getty AAT Structure:**
```
Agents
├── Animals
├── Organizations
└── People
    ├── Demographic groups ✓
    └── Occupations ✓
```

**Relationships Deleted:** 2

---

### 2. ✓ Duplicate Police Entry

**Problem:** Police appeared 3 times in Law enforcement due to duplicate CSV rows with different annotations.

**Root Cause:** Same relationship defined twice with different note fields
```csv
Police -> parent=Law enforcement ✓ (KEPT)
Police -> parent=Law enforcement (intermediate facet) ❌ (REMOVED)
```

**Relationships Deleted:** 1

---

### 3. ✓ Court/Courts Confusion

**Problem:** "Court" appeared as both a category and generic term, causing massive duplication:
```
Courts
├── Court (as child category)
│   ├── Katoomba Court
│   ├── Licensing Court
│   └── Supreme Court
├── Katoomba Court (duplicate)
├── Licensing Court (duplicate)
└── Supreme Court (duplicate)
```

**Root Cause:** Generic term "Court" incorrectly used as intermediate category

**Fix:** Removed "Court" as a category entirely
```csv
Court -> parent=Courts ❌ (REMOVED)
Katoomba Court -> parent=Court ❌ (REMOVED, has parent=Courts)
Licensing Court -> parent=Court ❌ (REMOVED, has parent=Courts)
Police court -> parent=Court ❌ (REMOVED, has parent=Courts)
Supreme Court -> parent=Court ❌ (REMOVED, has parent=Courts)
Court cases -> parent=Court ❌ (REMOVED, has parent=Legal events)
Courthouse -> parent=Court ❌ (REMOVED, has parent=Court buildings)
```

**Corrected Structure:**
```
Courts (under Government bodies)
├── Katoomba Court ✓
├── Licensing Court ✓
├── Police court ✓
└── Supreme Court ✓
```

**Relationships Deleted:** 6

---

### 4. ✓ Church/Churches Confusion

**Problem:** Same pattern as Court - "Church" used as both category and generic term

**Root Cause:** Generic term "Church" incorrectly used as intermediate category

**Fix:** Removed "Church" as a category
```csv
Church -> parent=Churches ❌ (REMOVED)
Congregational Church -> parent=Church ❌ (REMOVED, has parent=Churches)
Methodist Church -> parent=Church ❌ (REMOVED, has parent=Churches)
Roman Catholic Church -> parent=Church ❌ (REMOVED, has parent=Churches)
St Hilda's Church -> parent=Church ❌ (REMOVED, has parent=Churches)
Wesleyan Church -> parent=Church ❌ (REMOVED, has parent=Churches)
Katoomba Congregational Church -> parent=Church ❌ (REMOVED, has parent=Congregational Church)
```

**Relationships Deleted:** 7

---

### 5. ✓ Specific Church Duplication

**Problem:** Katoomba Congregational Church appeared twice:
```
Churches
├── Congregational Church
│   └── Katoomba Congregational Church
└── Katoomba Congregational Church (duplicate)
```

**Root Cause:** Specific church had parent relationships to both denomination AND Churches category

**Fix:**
```csv
Katoomba Congregational Church -> parent=Churches ❌ (REMOVED)
Katoomba Congregational Church -> parent=Congregational Church ✓ (KEPT)
Katoomba Congregational Church -> parent=Religious buildings ✓ (KEPT - poly-hierarchy)
```

**Corrected Structure:**
```
Churches (under Religious organizations)
├── Congregational Church
│   └── Katoomba Congregational Church ✓
├── Methodist Church
├── Roman Catholic Church
├── St Hilda's Church
└── Wesleyan Church
```

**Relationships Deleted:** 1

---

## Impact on Hierarchy Statistics

### Before Fixes:
- Primary facets: 7 (+ spurious "Court" facet = 8)
- Total primary relationships: 588
- Duplications visible in multiple trees

### After Fixes:
- Primary facets: 7 ✓ (correct Getty AAT structure)
- Total primary relationships: 570 (18 removed)
- Total hierarchy relationships: 836
- No duplications in primary facets ✓
- All thematic trees show full depth ✓

---

## Files Modified

1. **scripts/40_fix_csv_hierarchy_issues.py** (NEW)
   - Automated fix script for systematic removal of problematic relationships
   - Creates backup before modifications
   - Comprehensive logging of all deletions

2. **data/tag_map_consolidated.csv**
   - 18 duplicate/incorrect relationships removed
   - Reduced from 1,005 to 987 rows
   - Backup: `data/tag_map_consolidated.csv.backup-hierarchy-fixes`

3. **scripts/23_visualise_poly_hierarchy.py** (UPDATED)
   - Added deduplication of children lists
   - Added combined hierarchy for mixed traversal
   - Thematic trees now use combined hierarchy

4. **visualizations/hierarchy_trees/** (30 files regenerated)
   - All primary facet trees
   - All thematic grouping trees
   - Overview document

---

## Validation Checks Performed

✓ Agents facet follows Getty AAT structure (Animals, Organizations, People)
✓ No duplicate entries in Courts structure
✓ No duplicate entries in Churches structure
✓ No orphaned "Court" or "Church" facets
✓ Demographic groups and Occupations only under People
✓ Police appears only once under Law enforcement
✓ Specific churches only under their denomination
✓ All 7 primary facets align with Getty AAT
✓ All 22 thematic groupings show full depth

---

## Principles Applied

### 1. Getty AAT Alignment
Primary facets structured to match Getty AAT hierarchy patterns

### 2. No Generic Term Categories
Generic terms (Court, Church) should NOT be intermediate categories - only specific types or instances

### 3. Denominations vs Instances
- Denominations (Methodist Church, Roman Catholic Church) → direct children of Churches ✓
- Specific churches (Katoomba Congregational Church) → children of denomination ✓

### 4. Poly-Hierarchy Boundaries
- Within primary facet: Avoid duplication (Demographic groups under People only)
- Across facets: Intentional poly-hierarchy OK (Church as organization AND building)

### 5. Single Canonical Parent
Each tag should have ONE primary parent in its facet, with additional poly-hierarchy relationships for thematic groupings or cross-facet connections

---

## Next Steps

1. ✅ CSV fixes complete
2. ✅ Visualizations regenerated
3. ⏳ Continue with other tag corrections as needed
4. ⏳ Create API script for Zotero tag application
