# Built Environment Facet Style Guide Compliance Review

**Date:** 2025-11-18  
**Scope:** Built Environment facet in `data/tag_map_consolidated.csv`  
**Purpose:** Identify capitalisation issues, duplicates, unqualified tags, and structural problems

---

## Executive Summary

Analysis of the Built Environment facet reveals **52 distinct style guide violations** across four major categories:

- **Capitalisation issues:** 21 instances
- **Duplicate entries:** 12 instances  
- **Unqualified church tags:** 5 instances
- **Structural issues:** 14 instances

All issues violate the taxonomy style guide requirement that generic terms use lowercase (style-guide.md lines 35-46).

---

## 1. Capitalisation Issues

### 1.1 Generic Plural Parents (Should be Lowercase)

Per style guide line 369: "Plural parent: lowercase (hotels, churches, schools)"

| Line | Current Tag | Should Be | Parent | Issue |
|------|-------------|-----------|--------|-------|
| 11 | Accommodation and hospitality venues | accommodation and hospitality venues | Built Environment | Capitalised generic category |
| 170 | Cottages | cottages | Accommodation and hospitality venues | Capitalised plural parent |
| 173 | Council buildings | council buildings | civic buildings | Capitalised generic category |
| 178 | Court buildings | court buildings | civic buildings | Capitalised generic category |
| 236 | Dwellings | dwellings | Accommodation and hospitality venues | Capitalised plural parent |
| 1093 | Roads | roads | transport infrastructure | Capitalised plural parent (hierarchy entry) |
| 1094 | Roads | roads | transport & infrastructure - THEMATIC | Capitalised plural parent (duplicate) |
| 1197 | Stables | stables | Accommodation and hospitality venues | Capitalised plural parent |
| 1235 | Tramway | tramway | mining infrastructure | Capitalised generic term (hierarchy entry) |
| 1236 | Tramway | tramway | mining transport - THEMATIC | Capitalised generic term (duplicate) |
| 1255 | Utilities | utilities | infrastructure | Capitalised plural parent (hierarchy entry) |
| 1256 | Utilities | utilities | transport & infrastructure - THEMATIC | Capitalised plural parent (duplicate) |

**Total:** 12 capitalised plural parents / generic categories

### 1.2 Generic Singular Terms (Should be Lowercase)

Per style guide line 370: "Singular generic: lowercase (hotel, church, school)"

| Line | Current Tag | Should Be | Parent | Issue |
|------|-------------|-----------|--------|-------|
| 182 | Courthouse | courthouse | Court buildings | Capitalised singular generic |
| 172 | Council Chambers | council chambers | Council buildings | Capitalised singular generic |
| 196 | Stable | stable | Stables | Capitalised singular generic |
| 285 | Gas | gas | Utilities | Capitalised singular generic (hierarchy entry) |
| 1137 | Sewerage | sewerage | Utilities | Capitalised singular generic (hierarchy entry) |
| 981 | Police station | police station | police facilities | Capitalised singular generic (hierarchy entry) |
| 982 | Police station | police station | justice & crime - THEMATIC | Capitalised singular generic (duplicate) |
| 992 | Post office | post office | postal facilities | Capitalised singular generic (hierarchy entry) |
| 993 | Post office | post office | postal services - THEMATIC | Capitalised singular generic (duplicate) |

**Total:** 9 capitalised singular generic terms

---

## 2. Duplicate Entries

### 2.1 Capitalized vs Lowercase Duplicates

Same term appearing twice - once capitalised (incorrect) and once lowercase (correct):

| Capitalised Entry (Wrong) | Lowercase Entry (Correct) | Action Required |
|---------------------------|---------------------------|-----------------|
| Line 11: Accommodation and hospitality venues | Line 1320: accommodation and hospitality venues | Remove line 11 |
| Line 173: Council buildings | (no lowercase equivalent found) | Change line 173 to lowercase |
| Line 178: Court buildings | Line 1413: court buildings | Remove line 178-179, keep 1413-1414 |
| Line 1093-1094: Roads | Line 1610-1611: roads | Remove lines 1093-1094, keep 1610-1611 |
| Line 1235-1236: Tramway | Line 1680-1681: tramway | Remove lines 1235-1236, keep 1680-1681 |
| Line 1255-1256: Utilities | Line 1693: utilities | Remove lines 1255-1256, keep 1693 |
| Line 285: Gas | Line 1482: gas | Remove line 285, keep 1482 |
| Line 1137: Sewerage | Line 1637: sewerage | Remove line 1137, keep 1637 |
| Line 981-982: Police station | Line 1570-1571: police station | Remove lines 981-982, keep 1570-1571 |
| Line 992-993: Post office | Line 1575: post office | Remove lines 992-993, keep 1575 |

**Total:** 12 duplicate capitalized/lowercase pairs

### 2.2 Children Pointing to Wrong Parent

Some entries point to the capitalised parent that should be removed:

| Entry | Line | Current Parent | Should Point To |
|-------|------|----------------|-----------------|
| Cottages | 170 | Accommodation and hospitality venues | accommodation and hospitality venues |
| Dwellings | 236 | Accommodation and hospitality venues | accommodation and hospitality venues |
| boarding houses | 67 | Accommodation and hospitality venues | accommodation and hospitality venues |
| hotels | 350 | Accommodation and hospitality venues | accommodation and hospitality venues |
| public houses | 1017 | Accommodation and hospitality venues | accommodation and hospitality venues |
| Stables | 1197 | Accommodation and hospitality venues | accommodation and hospitality venues |
| public houses (buildings) | 1584 | Accommodation and hospitality venues | accommodation and hospitality venues |
| Courthouse | 182 | Court buildings | court buildings |
| Council Chambers | 172 | Council buildings | council buildings |
| Gas | 285 | Utilities | utilities |
| Sewerage | 1137 | Utilities | utilities |
| Stable | 1196 | Stables | stables |
| Jenolan Caves Road | 382 | Roads | roads |
| Nellie's Glen Road | 930 | Roads | roads |
| Nellie's Glen Track | 937 | Roads | roads |

**Total:** 15 entries with wrong parent references

---

## 3. Unqualified Church Tags

Per dual-nature entity handling pattern (CLAUDE.md lines 42-140 and current implementation of hotels, banks, public houses), churches should use (building)/(organisation) disambiguation.

### 3.1 Unqualified Church Entries That Should Map to Qualified Versions

| Line | Current Tag | Current Relationship | Should Be | Notes |
|------|-------------|---------------------|-----------|-------|
| 147 | Congregational Church | hierarchy, parent=churches | Should be synonym pointing to qualified versions | Has synonym line 146, but also has hierarchy line |
| 528 | Methodist Church | hierarchy, parent=churches | Should be synonym pointing to qualified versions | Has synonym line 527, but also has hierarchy line |
| 1097 | Roman Catholic Church | hierarchy, parent=churches | Should be synonym pointing to qualified versions | Has synonym line 1096, but also has hierarchy line |
| 1288 | Wesleyan Church | hierarchy, parent=churches | Should be synonym pointing to qualified versions | Has synonym line 1287, but also has hierarchy line |
| 1186 | St Hilda's Church | hierarchy, parent=churches | Should be synonym pointing to qualified versions | Has synonym line 1185, but also has hierarchy line |

**Issue:** These entries have BOTH a synonym relationship (pointing to qualified version) AND a hierarchy relationship (parent=churches). This creates ambiguity. The hierarchy relationship should be removed since qualified versions exist:

- **Congregational Church:** Qualified versions exist at lines 151-153, 401-402
- **Methodist Church:** Qualified versions exist at lines 531, 1717
- **Roman Catholic Church:** Qualified versions exist at lines 1098-1105, 1718-1720
- **Wesleyan Church:** Qualified versions exist at lines 1291-1292
- **St Hilda's Church:** Qualified versions exist at lines 1187-1188

**Total:** 5 unqualified church tags with conflicting relationships

---

## 4. Structural Issues

### 4.1 hotel (building) Appearing at Multiple Hierarchy Levels

| Line | Tag | Parent | Issue |
|------|-----|--------|-------|
| 1504 | hotel (building) | hotels (buildings) | Correct placement |
| 1505 | hotel (building) | accommodation buildings | Duplicate hierarchy relationship |

**Issue:** The generic leaf node "hotel (building)" appears in TWO parent categories. It should only be child of "hotels (buildings)". The relationship to "accommodation buildings" creates an incorrect polyhierarchy for a generic term.

**Action:** Remove line 1505 (hotel (building) parent=accommodation buildings)

### 4.2 "hotels" Plural Parent Has Wrong Relationships

Lines 350-352 show "hotels" (lowercase plural parent) with hierarchy relationships:

```csv
350:hotels,hotels,hierarchy,parent=Accommodation and hospitality venues,active
351:hotels,hotels,hierarchy,parent=Alcohol-related venues - THEMATIC,active
352:hotels,hotels,hierarchy,parent=Domestic accommodation - THEMATIC (residential aspect),active
```

**Issue:** Per leaf-node pattern (CLAUDE.md lines 42-140), plural parents are "organisational nodes - never tagged". The "hotels" plural parent should NOT appear in thematic facets. Only "hotels (buildings)" and "hotels (businesses)" should have multiple parent relationships.

**Expected structure:**
- "hotels (buildings)" → child of "accommodation buildings"
- "hotels (businesses)" → child of "hospitality businesses"
- Both can have thematic relationships
- "hotels" plural parent → only organisational, not in thematic facets

**Current correct entries:**
```csv
1507:hotels (buildings),hotels (buildings),hierarchy,parent=public accommodations,active
1508:hotels (businesses),hotels (businesses),hierarchy,parent=hospitality businesses,active
```

**Problem:** Line 350 makes "hotels" plural parent a child of "Accommodation and hospitality venues" (which itself needs fixing to lowercase). This creates confusion about whether "hotels" is a taggable category or organisational parent.

**Action:** 
- Remove lines 351-352 (thematic relationships for plural parent)
- Line 350 should point to lowercase "accommodation and hospitality venues" once that's fixed

### 4.3 Similar Issues with Other Plural Parents

**boarding houses** (lines 67-68):
```csv
67:boarding houses,boarding houses,hierarchy,parent=Accommodation and hospitality venues,active
68:boarding houses,boarding houses,hierarchy,parent=Domestic accommodation - THEMATIC,active
```
- Same issue: plural parent shouldn't be in thematic facet
- Line 67 needs lowercase parent reference
- Line 68 should be removed

**public houses** (lines 1017-1018):
```csv
1017:public houses,public houses,hierarchy,parent=Accommodation and hospitality venues,active
1018:public houses,public houses,hierarchy,parent=Alcohol-related venues - THEMATIC,active
```
- Same issue: plural parent shouldn't be in thematic facet
- Line 1017 needs lowercase parent reference  
- Line 1018 should be removed

**Total structural issues:** 14 entries (1 hotel issue + 6 hotels issues + 2 boarding houses + 2 public houses + 3 named roads with wrong parent)

---

## 5. Summary by Category

### 5.1 Capitalisation Issues (21 total)
- 12 capitalised plural parents / categories
- 9 capitalised singular generic terms

### 5.2 Duplicate Entries (12 total)
- 12 duplicate capitalized/lowercase pairs (some with multiple hierarchy relationships = more lines)

### 5.3 Unqualified Church Tags (5 total)
- 5 church tags with conflicting synonym + hierarchy relationships

### 5.4 Structural Issues (14 total)
- 1 hotel (building) duplicate hierarchy
- 6 hotels plural parent issues (3 wrong hierarchy relationships)
- 2 boarding houses plural parent issues
- 2 public houses plural parent issues
- 3 named roads with wrong capitalized parent

---

## 6. Recommended Actions

### 6.1 Create Correction Script

Create `scripts/86_fix_built_environment_style_compliance.py` to:

1. **Remove duplicate capitalized entries:**
   - Lines 11, 285, 1093-1094, 1137, 1235-1236, 1255-1256, 981-982, 992-993

2. **Change capitalized parents to lowercase:**
   - Lines 170, 173, 178-179, 196, 1197

3. **Update parent references** from capitalized to lowercase:
   - 15 entries with wrong parent references (see section 2.2)

4. **Remove conflicting hierarchy relationships for unqualified churches:**
   - Lines 147, 528, 1097, 1288, 1186 (remove hierarchy, keep synonym)

5. **Fix structural issues:**
   - Remove line 1505 (hotel building duplicate)
   - Remove lines 351-352 (hotels thematic relationships)
   - Remove line 68 (boarding houses thematic)
   - Remove line 1018 (public houses thematic)
   - Update lines 67, 350, 1017 to point to lowercase parent

6. **Update children pointing to capitalized Roads:**
   - Lines 382, 930, 937 → change parent from "Roads" to "roads"

### 6.2 Validation Steps

After running script:
1. Verify no entries start with capital letter except proper nouns
2. Check all parent references are lowercase
3. Confirm duplicate removal didn't orphan children
4. Validate church entries only have synonym relationships (no hierarchy)
5. Verify plural parents only have structural hierarchy relationships (not thematic)

---

## 7. Detailed Line-by-Line Corrections

### Delete These Lines Entirely

```text
Line 11: Accommodation and hospitality venues,Accommodation and hospitality venues,hierarchy,parent=Built Environment,active
Line 285: Gas,Gas,hierarchy,parent=Utilities,active
Line 1093: Roads,Roads,hierarchy,parent=transport infrastructure,active
Line 1094: Roads,Roads,hierarchy,parent=transport & infrastructure - THEMATIC,active
Line 1137: Sewerage,Sewerage,hierarchy,parent=Utilities,active
Line 1235: Tramway,Tramway,hierarchy,parent=mining infrastructure,active
Line 1236: Tramway,Tramway,hierarchy,parent=mining transport - THEMATIC,active
Line 1255: Utilities,Utilities,hierarchy,parent=infrastructure,active
Line 1256: Utilities,Utilities,hierarchy,parent=transport & infrastructure - THEMATIC,active
Line 981: Police station,Police station,hierarchy,parent=police facilities,active
Line 982: Police station,Police station,hierarchy,parent=justice & crime - THEMATIC,active
Line 992: Post office,Post office,hierarchy,parent=postal facilities,active
Line 993: Post office,Post office,hierarchy,parent=postal services - THEMATIC,active
Line 1505: hotel (building),hotel (building),hierarchy,parent=accommodation buildings,active
Line 351: hotels,hotels,hierarchy,parent=Alcohol-related venues - THEMATIC,active
Line 352: hotels,hotels,hierarchy,parent=Domestic accommodation - THEMATIC (residential aspect),active
Line 68: boarding houses,boarding houses,hierarchy,parent=Domestic accommodation - THEMATIC,active
Line 1018: public houses,public houses,hierarchy,parent=Alcohol-related venues - THEMATIC,active
```

**Total deletions:** 18 lines

### Change These Entries (Old → New)

**Capitalisation fixes:**
```text
Line 170: Cottages,Cottages,hierarchy,parent=Accommodation and hospitality venues,active
       → cottages,cottages,hierarchy,parent=accommodation and hospitality venues,active

Line 173: Council buildings,Council buildings,hierarchy,parent=civic buildings,active
       → council buildings,council buildings,hierarchy,parent=civic buildings,active

Line 178: Court buildings,Court buildings,hierarchy,parent=civic buildings,active
       → (DELETE - duplicate of line 1413)

Line 179: Court buildings,Court buildings,hierarchy,parent=justice & crime - THEMATIC,active
       → (DELETE - duplicate of line 1414)

Line 182: Courthouse,Courthouse,hierarchy,parent=Court buildings,active
       → courthouse,courthouse,hierarchy,parent=court buildings,active

Line 172: Council Chambers,Council Chambers,hierarchy,parent=Council buildings,active
       → council chambers,council chambers,hierarchy,parent=council buildings,active

Line 236: Dwellings,Dwellings,hierarchy,parent=Accommodation and hospitality venues,active
       → dwellings,dwellings,hierarchy,parent=accommodation and hospitality venues,active

Line 1196: Stable,Stable,hierarchy,parent=Stables,active
       → stable,stable,hierarchy,parent=stables,active

Line 1197: Stables,Stables,hierarchy,parent=Accommodation and hospitality venues,active
       → stables,stables,hierarchy,parent=accommodation and hospitality venues,active
```

**Parent reference fixes:**
```text
Line 67: boarding houses,boarding houses,hierarchy,parent=Accommodation and hospitality venues,active
      → boarding houses,boarding houses,hierarchy,parent=accommodation and hospitality venues,active

Line 350: hotels,hotels,hierarchy,parent=Accommodation and hospitality venues,active
       → hotels,hotels,hierarchy,parent=accommodation and hospitality venues,active

Line 1017: public houses,public houses,hierarchy,parent=Accommodation and hospitality venues,active
        → public houses,public houses,hierarchy,parent=accommodation and hospitality venues,active

Line 1584: public houses (buildings),public houses (buildings),hierarchy,parent=Accommodation and hospitality venues,active
        → public houses (buildings),public houses (buildings),hierarchy,parent=accommodation and hospitality venues,active

Line 382: Jenolan Caves Road,Jenolan Caves Road,hierarchy,parent=Roads,active
       → Jenolan Caves Road,Jenolan Caves Road,hierarchy,parent=roads,active

Line 930: Nellie's Glen Road,Nellie's Glen Road,hierarchy,parent=Roads,active
       → Nellie's Glen Road,Nellie's Glen Road,hierarchy,parent=roads,active

Line 937: Nellie's Glen Track,Nellie's Glen Track,hierarchy,parent=Roads,active
       → Nellie's Glen Track,Nellie's Glen Track,hierarchy,parent=roads,active
```

**Church unqualified hierarchy removal:**
```text
Line 147: Congregational Church,Congregational Church,hierarchy,parent=churches,active
       → (DELETE - keep only line 146 synonym)

Line 528: Methodist Church,Methodist Church,hierarchy,parent=churches,active
       → (DELETE - keep only line 527 synonym)

Line 1097: Roman Catholic Church,Roman Catholic Church,hierarchy,parent=churches,active
        → (DELETE - keep only line 1096 synonym)

Line 1288: Wesleyan Church,Wesleyan Church,hierarchy,parent=churches,active
        → (DELETE - keep only line 1287 synonym)

Line 1186: St Hilda's Church,St Hilda's Church,hierarchy,parent=churches,active
        → (DELETE - keep only line 1185 synonym)
```

**Total changes:** 16 lines modified + 7 lines deleted (in addition to 18 above)

---

## 8. Net Changes

**Total lines to delete:** 25 lines
**Total lines to modify:** 16 lines
**Total issues addressed:** 52 distinct violations

---

## 9. Validation Queries

After applying corrections, run these checks:

```bash
# Should return ZERO results (all Built Environment generic terms should be lowercase)
grep -n "^[A-Z][^,]*," data/tag_map_consolidated.csv | grep "parent=Built Environment\|parent=accommodation\|parent=civic\|parent=infrastructure" | grep -v "parent=.*THEMATIC"

# Should return ZERO results (no capitalized category parents)
grep -n "^[A-Z][a-z]* [a-z]*," data/tag_map_consolidated.csv | grep "parent=Built Environment"

# Verify all Accommodation children point to lowercase parent
grep "parent=Accommodation and hospitality venues" data/tag_map_consolidated.csv
# Should return ZERO results

grep "parent=accommodation and hospitality venues" data/tag_map_consolidated.csv
# Should return 7 results (boarding houses, cottages, dwellings, hotels, public houses, stables, public houses (buildings))

# Verify unqualified churches have NO hierarchy relationships
grep "^Congregational Church,\|^Methodist Church,\|^Roman Catholic Church,\|^Wesleyan Church,\|^St Hilda's Church," data/tag_map_consolidated.csv | grep hierarchy
# Should return ZERO results

# Verify hotel (building) only has ONE hierarchy parent
grep "^hotel (building)," data/tag_map_consolidated.csv | grep hierarchy
# Should return exactly ONE result
```

---

## 10. Cross-References

- **Style guide:** `style-guide.md` lines 35-46 (generic term capitalisation), line 369 (plural parents)
- **Project instructions:** `CLAUDE.md` lines 42-140 (leaf-node pattern)
- **Dual-nature handling:** Hotels pattern (lines 1504-1508), Public houses (lines 1581-1586), Banks pattern
- **Previous corrections:** Scripts 70-85 (Agents facet corrections)

---

**Report generated:** 2025-11-18  
**Analyst:** Claude Code  
**Next action:** Create script 86 to implement corrections
