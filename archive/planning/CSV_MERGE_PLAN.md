# CSV Merge Plan: Creating Single Source of Truth

**Date:** 2025-10-24
**Status:** Awaiting approval
**Files:** `tag_consolidation_map.csv` + `poly_hierarchy_additions.csv` → `tag_consolidation_map.csv` (merged)

## Executive Summary

We need to merge two CSV files that contain overlapping but complementary taxonomy data. The merge is complex because:

1. **Poly-hierarchy support**: Same tag can have multiple parents (e.g., "Katoomba Hotel" appears under both "Hotels" (form-based) and "Katoomba" (location-based))
2. **Data quality issues**: tag_consolidation_map has 126 exact duplicate rows
3. **Correction conflicts**: poly_hierarchy_additions has corrected intermediate facets
4. **Complementary content**: Each file has unique thematic groupings

## Current State Analysis

### File: `tag_consolidation_map.csv` (996 lines)

**Content:**

- 996 total lines (including header)
- 126 exact duplicate rows (data quality issue)
- ~870 unique rows after deduplication
- 113 THEMATIC grouping markers
- 196 poly-hierarchical tags (multiple parents per tag)
- 37 town-based thematic groupings (parent=Katoomba, parent=Blackheath, etc.)

**Issues:**

- **OUTDATED primary facets**: Missing intermediate facets
  - Example: "Senior-Constable Illingworth" → parent=Law enforcement (should be parent=Police)
  - Example: "Demographic groups" → parent=Agents (should be parent=People)
- **Exact duplicates**: Hotels appear 4x each (Allen's Hotel, Brown's Hotel, Belgravia Hotel, Carrington Hotel)
- **Substring triage duplicates**: Many "keep" action rows duplicated

**Unique value:**

- Contains **town-based thematic groupings** (37 entries) NOT in poly file
- Example: Katoomba > Katoomba Hotel, Katoomba Congregational Church, Katoomba School of Arts, etc.

### File: `poly_hierarchy_additions.csv` (680 lines)

**Content:**

- 680 total lines (including header)
- 2 exact duplicate rows (minimal data quality issues)
- ~678 unique rows after deduplication
- 183 THEMATIC grouping markers (MORE than map file)
- 119 poly-hierarchical tags (multiple parents per tag)

**Strengths:**

- **CORRECTED primary facets**: Has proper intermediate facets
  - Example: Law enforcement > Police > [individual officers]
  - Example: Agents > People > Demographic groups
- **Clean data**: Only 2 duplicates
- **More thematic groupings overall**: 183 vs 113 THEMATIC markers

**Missing:**

- **No town-based thematic groupings**: Doesn't have parent=Katoomba, parent=Blackheath entries

## Taxonomy Structure Review

### Primary Facets (Form-Based, Getty AAT Compatible)

These answer **"WHAT type of thing?"**

```text
Agents (top-level facet)
├── People
│   ├── Demographic groups
│   │   ├── Women
│   │   └── Men
│   └── Occupations
│       └── Hotelliers
│           └── [individual hotelliers as leaf nodes]
├── Organizations
│   └── [various org types]
└── [other agent types]

Built Environment (top-level facet)
├── Accommodation
│   └── Hotels (generic type, plural organizational - NO TAG per guidelines)
│       └── Hotel (singular generic - TAG for unnamed hotels)
│           └── [Named hotels as leaf nodes: Katoomba Hotel, Carrington Hotel, etc.]
└── [other building types]

Places (top-level facet)
└── Blue Mountains
    ├── Katoomba (place/town)
    ├── Blackheath (place/town)
    └── [other towns/places]
```

**Key principle:** Places hierarchy says WHERE, Built Environment says WHAT. Hotels do NOT appear under Katoomba in primary facets.

### Thematic Groupings (Domain-Based, Exhibition/Tour Optimized)

These answer **"Show me everything related to X"**

```text
Towns (thematic grouping) - TOWN-BASED
├── Katoomba (thematic)
│   ├── Hotels
│   │   ├── Katoomba Hotel
│   │   ├── Carrington Hotel
│   │   └── Katoomba Family Hotel
│   ├── Churches
│   │   └── Katoomba Congregational Church
│   ├── Organizations
│   │   ├── Katoomba School of Arts
│   │   └── Katoomba Cricket Club
│   └── [all entities associated with Katoomba]
└── [other towns]

Health & Medicine (thematic grouping) - DOMAIN-BASED
├── Medical professionals - THEMATIC
├── Health conditions - THEMATIC
│   ├── Illness - THEMATIC
│   ├── Disease - THEMATIC
│   └── Death - THEMATIC
└── Health-related events - THEMATIC
    └── Accident - THEMATIC
```

**Key principle:** Thematic groupings enable browsing by location OR domain. Same entity appears in BOTH primary facet (form) and thematic grouping (domain/location).

## Merge Strategy

### Phase 1: Data Cleaning

1. **Remove exact duplicates from BOTH files**
   - tag_consolidation_map: 126 duplicates → keep 1 of each
   - poly_hierarchy_additions: 2 duplicates → keep 1 of each
   - Result: ~870 unique from map, ~678 unique from poly

### Phase 2: Identify Relationship Types

For each row, categorise the parent relationship:

**A. Primary Facet Relationships** (form-based hierarchy)

- Pattern: `parent=<form-based category>`
- Examples: parent=Police, parent=Hotels, parent=Demographic groups
- NO " - THEMATIC" suffix

**B. Thematic Groupings** (domain-based or location-based)

- Pattern: `parent=<category> - THEMATIC` or `parent=<town name>`
- Examples: parent=Health & Medicine - THEMATIC, parent=Katoomba
- May have " - THEMATIC" suffix OR be a town name

### Phase 3: Conflict Resolution Rules

**Rule 1: Exact matches (same old_tag + same notes)**
→ Keep only ONE copy (already handled in Phase 1)

**Rule 2: Poly-hierarchy (same old_tag, different parent types)**
→ Keep BOTH rows (this is intentional poly-hierarchy)

Example:

```csv
Katoomba Hotel,Katoomba Hotel,hierarchy,parent=Hotels        # Primary facet (WHAT)
Katoomba Hotel,Katoomba Hotel,hierarchy,parent=Katoomba      # Thematic grouping (WHERE)
```

Action: Keep BOTH

**Rule 3: Primary facet conflicts (same old_tag, both primary facets, different parents)**
→ Prefer poly_hierarchy_additions version (has corrections)

Example:

```csv
# map version (OLD):
Senior-Constable Illingworth,Senior-Constable Illingworth,hierarchy,parent=Law enforcement

# poly version (CORRECTED):
Senior-Constable Illingworth,Senior-Constable Illingworth,hierarchy,parent=Police
```

Action: Keep poly version, discard map version

**Rule 4: Unique to map (not in poly at all)**
→ Keep map version

Example: Town-based thematic groupings

```csv
Katoomba Hotel,Katoomba Hotel,hierarchy,parent=Katoomba
```

Action: Keep (only exists in map)

**Rule 5: Unique to poly (not in map at all)**
→ Keep poly version

Example: New thematic groupings

```csv
Alcoholic beverages,Alcoholic beverages,hierarchy,parent=Alcohol consumption & behaviour - THEMATIC
```

Action: Keep (only exists in poly)

### Phase 4: Merge Algorithm

```text
1. Load both files
2. Remove exact duplicates within each file
3. Create relationship sets:
   - map_relations = {(old_tag, notes): {new_tag, action}}
   - poly_relations = {(old_tag, notes): {new_tag, action}}

4. For each unique (old_tag, notes) pair:
   a. If exists in poly → use poly version (prefer corrected data)
   b. If NOT in poly but in map → use map version (unique content)

5. Result: Union of all relationships, with poly taking precedence for conflicts
```

### Phase 5: Validation

1. **Line count check:**

   - Expected: ~(870 unique map + poly additions) rows
   - Should be LESS than 996 + 678 = 1674 (due to deduplication and conflict resolution)
   - Should be MORE than 678 (due to unique map content)
   - Estimate: ~1100-1200 lines

2. **Poly-hierarchy preservation:**

   - Check sample tags have multiple parents (e.g., "Katoomba Hotel" has both parent=Hotels and parent=Katoomba)

3. **Primary facet corrections:**

   - Verify police officers have parent=Police (not parent=Law enforcement)
   - Verify Demographic groups has parent=People (not parent=Agents)

4. **Town groupings preserved:**

   - Verify all 37 town-based thematic groupings exist (parent=Katoomba, etc.)

5. **THEMATIC markers:**

   - Count should be >= 183 (from poly, plus any unique from map)

## Implementation Plan

### Script Requirements

```python
#!/usr/bin/env python3
"""
Script 37: Merge Tag Consolidation CSV Files

Merge strategy:
1. Remove exact duplicates from each file
2. Create relationship index: (old_tag, notes) → row data
3. Merge with precedence: poly > map (prefer corrected data)
4. Output: Unified CSV with all unique relationships
"""

def merge_csvs(map_file, poly_file, output_file):
    # Phase 1: Load and deduplicate
    map_data = load_and_dedupe(map_file)
    poly_data = load_and_dedupe(poly_file)

    # Phase 2: Merge with precedence
    # Start with map data (all unique relationships)
    merged = map_data.copy()

    # Update/add from poly data (overwrites conflicts with corrected versions)
    merged.update(poly_data)

    # Phase 3: Write output
    write_csv(merged, output_file)

    return validation_stats
```

### Output File

**Filename:** `tag_map_consolidated.csv` (new unified file)
**Backups:** Existing backups with MD5 checksums preserved
**Archive:** Old CSV files moved to archive subfolder

## Post-Merge Actions

1. **Update script 22** (`scripts/22_generate_poly_hierarchy.py`):

   - Change output mode from "generate new CSV" to "update existing CSV"
   - Future additions append to tag_map_consolidated.csv directly
   - No more separate poly_hierarchy_additions.csv

2. **Archive superseded files**:

   - Move old CSV files to `archive/csv-files/` subfolder
   - Move completed planning documents to `archive/planning/` subfolder
   - Keep for reference but no longer active data sources

3. **Update documentation**:

   - Single source of truth: `tag_map_consolidated.csv`
   - All future hierarchy additions go directly into this file

## Questions for Approval

**APPROVED 2025-10-24:**

1. **Conflict resolution**: ✓ YES - Poly version takes precedence for primary facet conflicts

2. **Town groupings**: ✓ YES - Preserve ALL 37 town-based thematic groupings from map file

3. **Duplicate removal**: ✓ YES - Remove 126 exact duplicates from map file

4. **Output filename**: ✓ CHANGED - Output to new file `tag_map_consolidated.csv`

5. **Script 22 updates**: ✓ YES - Append to merged file to maintain single source of truth

## Risk Assessment

**Low Risk:**

- Backups exist with MD5 checksums (2025-10-23-230752)
- Output to new file (no overwriting)
- Merge is additive (no data loss, only deduplication)

**Medium Risk:**

- Complex conflict resolution rules could miss edge cases
- Recommend manual validation of sample entries post-merge

**Mitigation:**

- Generate detailed statistics and validation checks
- User review before committing to git
- Original files preserved in archive

## Success Criteria

- ✅ All 37 town-based thematic groupings preserved
- ✅ All poly-hierarchical relationships preserved (tags with multiple parents)
- ✅ Primary facets use corrected intermediate facets (from poly file)
- ✅ No exact duplicates in output
- ✅ Line count in expected range (1100-1200)
- ✅ All THEMATIC groupings preserved (>=183 markers)
- ✅ Single source of truth established

---

**Next Step:** User review and approval of this plan before implementation.
