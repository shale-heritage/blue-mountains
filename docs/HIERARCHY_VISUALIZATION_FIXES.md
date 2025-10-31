# Hierarchy Visualization Fixes

**Date:** 2025-10-30
**Script:** `scripts/23_visualise_poly_hierarchy.py`

---

## Issues Identified

### 1. Duplicate Relationships (FIXED ✓)
**Problem:** CSV contained duplicate parent-child relationships with different note annotations:
```csv
Police,Police,hierarchy,parent=Law enforcement
Police,Police,hierarchy,parent=Law enforcement (intermediate facet)
```

**Impact:** Police appeared 3 times in the Agents tree

**Fix:** Added deduplication to `build_hierarchy_tree()` function:
```python
# Deduplicate children lists (handles duplicate CSV rows with different annotations)
for parent in primary:
    primary[parent] = list(dict.fromkeys(primary[parent]))  # Preserves order
```

**Result:** Police now appears only once ✓

---

### 2. Thematic Trees Too Shallow (FIXED ✓)
**Problem:** Thematic groupings showed only top-level nodes without children

Example - Community institutions showed:
```
Community institutions
├── Civic buildings (no children shown)
├── Community buildings (no children shown)
└── ...
```

**Root Cause:** Children had PRIMARY relationships (`parent=Civic buildings`) but parents had THEMATIC relationships (`parent=Community institutions - THEMATIC`). The visualization script only traversed within the same hierarchy type.

**Fix:**
1. Added `combined` hierarchy that merges both primary and thematic relationships
2. Use `combined` hierarchy when generating thematic trees for mixed traversal

**Result:** Community institutions now shows full depth (89 nodes instead of 6) ✓

---

### 3. Nested Poly-Hierarchies in Primary Facets (CSV DESIGN ISSUE)
**Problem:** Agents facet has nested duplicate structures:

```
Agents
├── Demographic groups (direct child)
│   ├── Families
│   └── ...
├── Occupations (direct child)
│   └── ...
└── People (also direct child)
    ├── Demographic groups (duplicate here)
    │   ├── Families (duplicate)
    │   └── ...
    └── Occupations (duplicate here)
```

**Root Cause:** CSV defines multiple parent relationships:
- `Demographic groups -> parent=Agents`
- `Demographic groups -> parent=People`
- `People -> parent=Agents`

This creates a poly-hierarchy WITHIN the same primary facet.

**Current Status:** Correctly visualized, but may be confusing
**Action Needed:** Review with user to determine if this is intentional design

---

### 4. Additional Poly-Hierarchy Duplicates (CSV DESIGN ISSUE)

**Court:** Appears multiple times in Government bodies > Courts
```
Courts
├── Court (parent)
│   ├── Court cases
│   ├── Courthouse
│   ├── Katoomba Court
│   ├── Licensing Court
│   ├── Police court
│   └── Supreme Court
├── Katoomba Court (duplicate)
├── Licensing Court (duplicate)
├── Police court (duplicate)
└── Supreme Court (duplicate)
```

**Churches:** Similar pattern in Religious organizations
```
Churches
├── Church (parent)
│   ├── Congregational Church
│   │   └── Katoomba Congregational Church
│   ├── Katoomba Congregational Church (duplicate)
│   ├── Methodist Church
│   ├── Roman Catholic Church
│   ├── St Hilda's Church
│   └── Wesleyan Church
├── Congregational Church (duplicate)
│   └── Katoomba Congregational Church (triplicate)
├── Katoomba Congregational Church (duplicate)
├── Methodist Church (duplicate)
├── Roman Catholic Church (duplicate)
├── St Hilda's Church (duplicate)
└── Wesleyan Church (duplicate)
```

**Root Cause:** Tags have multiple parents within the same hierarchy
**Action Needed:** Review CSV data to determine correct parent relationships

---

## Script Changes Made

### Modified Function: `build_hierarchy_tree()`

**Before:**
```python
def build_hierarchy_tree(csv_path: Path) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    primary = defaultdict(list)
    thematic = defaultdict(list)
    # ... build hierarchies ...
    return primary, thematic
```

**After:**
```python
def build_hierarchy_tree(csv_path: Path) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, List[str]]]:
    primary = defaultdict(list)
    thematic = defaultdict(list)
    combined = defaultdict(list)

    # ... build hierarchies ...

    # Deduplicate children lists
    for parent in primary:
        primary[parent] = list(dict.fromkeys(primary[parent]))
    for parent in thematic:
        thematic[parent] = list(dict.fromkeys(thematic[parent]))
    for parent in combined:
        combined[parent] = list(dict.fromkeys(combined[parent]))

    return primary, thematic, combined
```

### Modified: Thematic Tree Generation

**Before:**
```python
tree = generate_facet_tree(theme, thematic)
```

**After:**
```python
# Use combined hierarchy to traverse both thematic AND primary relationships
tree = generate_facet_tree(theme, combined)
```

---

## Remaining CSV Data Structure Issues

### Priority 1: Review Nested Poly-Hierarchies
- **Agents > People > Demographic groups/Occupations** duplication
- Determine if intentional or should be consolidated

### Priority 2: Fix Court/Church Duplicates
- **Courts** - multiple Court/Katoomba Court/etc. entries
- **Churches** - multiple Church/Congregational Church/etc. entries
- Need to identify correct parent-child relationships

### Priority 3: Other Potential Issues
- **Schools of Arts** appears multiple times in Community institutions tree
- **Band/Katoomba band** - similar duplication pattern
- Review all poly-hierarchy instances for correctness

---

## Next Steps

1. ✅ Regenerate visualizations with fixed script
2. ⏳ Review CSV data structure issues together
3. ⏳ Clean up unintentional poly-hierarchies
4. ⏳ Validate all parent-child relationships
5. ⏳ Final visualization regeneration

---

## Test Results

**Before fixes:**
- Community institutions: 6 nodes (only top level)
- Police duplicates: 3 occurrences
- Law enforcement duplicates: 2 relationships

**After fixes:**
- Community institutions: 89 nodes (full depth) ✓
- Police duplicates: 1 occurrence ✓
- All duplicates from CSV annotations removed ✓
- Nested poly-hierarchies preserved (awaiting user review)
