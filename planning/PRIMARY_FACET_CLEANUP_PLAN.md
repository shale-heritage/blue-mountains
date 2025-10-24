# Primary Facet Cleanup Plan

**Date:** 2025-10-24
**Status:** Analysis Complete - Ready for Execution
**Goal:** Reduce 82 primary visualization trees → 7 Getty AAT-aligned primary facets

---

## Problem Statement

Currently have 82 separate primary root-level trees instead of 7 Getty AAT facets due to:
- Missing Getty AAT root entries
- Orphaned primary hierarchies not connected to Getty roots
- Some thematic groupings incorrectly in primary hierarchy

**Target Structure:** 7 Getty AAT Primary Facets
1. Agents
2. Places
3. Built Environment
4. Activities
5. Events
6. Associated Concepts
7. Materials

---

## Current State (Analysis Complete)

### Analysis Results from Script 40

**File:** `reports/primary_structure_analysis.md`

**Summary Statistics:**
- Current Getty roots: 0 (need to add 7)
- Getty-connected primary parents: 171 (KEEP these)
- Orphaned primary roots: 60 (REMOVE these)
- Missing from archive: 4 relationships (Katoomba, Leura, Megalong, Mount Victoria → parent=Towns)
- Added in current: 288 relationships (valuable new content)
- Unassigned tags: 110 (need Getty facet assignment)

**Decision:** FIX CURRENT (don't revert to archive)

### Key Findings

1. **171 Getty-connected hierarchies are correct** - these properly chain to Agents, Places, Built Environment, Activities, Events, Associated Concepts, or Materials

2. **60 Orphaned primary roots to remove** - these are disconnected hierarchies:
   - Special markers: `(conceptual facet)`, `(new top-level facet)`, `(place type)`, `(thematic facet)`
   - Thematic groupings: Alcohol & Temperance, Arts & Culture, Communications & Postal Services, Community institutions, Economy & Labour, Environment & Weather, Family & Domestic Life, Health & Medicine, Justice & Crime, Military & War, Politics & Governance, Race & Ethnicity, Religion, Social issues, Sport & Recreation, Tourism & Accommodation, Transport & Infrastructure, Women & Gender
   - Location-specific: Carrington, Port Kembla, Sunny Corner
   - Concept groups: Crimes, Cultural identity & heritage, etc.

3. **4 Missing relationships from archive** - all are town → parent=Towns connections:
   - Katoomba → parent=Towns
   - Leura → parent=Towns
   - Megalong → parent=Towns
   - Mount Victoria → parent=Towns

4. **110 Unassigned tags** need Getty facet assignment

---

## Execution Plan

### Phase 1: Add Getty AAT Root Entries (7 entries)

Add to CSV:
```csv
Agents,Agents,hierarchy,parent=(Getty AAT primary facet)
Places,Places,hierarchy,parent=(Getty AAT primary facet)
Built Environment,Built Environment,hierarchy,parent=(Getty AAT primary facet)
Activities,Activities,hierarchy,parent=(Getty AAT primary facet)
Events,Events,hierarchy,parent=(Getty AAT primary facet)
Associated Concepts,Associated Concepts,hierarchy,parent=(Getty AAT primary facet)
Materials,Materials,hierarchy,parent=(Getty AAT primary facet)
```

### Phase 2: Remove Orphaned Primary Hierarchies

For each of the 60 orphaned roots, remove PRIMARY parent relationships while preserving:
- Thematic parent relationships (keep all "- THEMATIC" connections)
- The tags themselves (only remove the parent relationship)

**Special handling:**
- Location tags (Carrington, Port Kembla, Sunny Corner): Keep if under Places hierarchy, otherwise remove primary parent
- Town thematic hierarchies: PRESERVE Towns > [Town] > [intermediates] > [entities]

**Tools needed:**
- Script to identify and remove orphaned primary parent relationships
- Validation to ensure thematic parents preserved

### Phase 3: Restore Missing Archive Relationships

Add back 4 missing relationships:
```csv
Katoomba,Katoomba,hierarchy,parent=Towns
Leura,Leura,hierarchy,parent=Towns
Megalong,Megalong,hierarchy,parent=Towns
Mount Victoria,Mount Victoria,hierarchy,parent=Towns
```

**Note:** These are PRIMARY hierarchy entries. The THEMATIC hierarchy (Towns > Katoomba - THEMATIC) already exists and should be preserved.

### Phase 4: Assign Unassigned Tags

For 110 unassigned tags, manually assign to appropriate Getty facet paths.

**Process:**
1. Review tag name
2. Check thematic parent context
3. Fetch Zotero source excerpt if needed
4. Assign to Getty facet path

**Common patterns:**
- Thematic grouping names (Arts & Culture, Religion, etc.) → Stay thematic-only, no primary parent
- Activity names → Activities
- Event names → Events
- Organization names → Agents > Organizations
- Building names → Built Environment
- Place names → Places
- Concepts → Associated Concepts

### Phase 5: Towns Hierarchy Special Handling

**Current issue:** Towns have children mixing:
- Locations/places (Carrington, South Katoomba) - KEEP in primary Places
- Buildings (Katoomba Hotel, Megalong Hotel) - MOVE to Built Environment in primary
- Organizations (Katoomba Cricket Club) - MOVE to Agents > Organizations in primary
- Etc.

**Target structure:**

**Primary:**
```text
Places > Towns > Katoomba
             └── Carrington (locale only)
             └── South Katoomba (locale only)
```

**Thematic (PRESERVE):**
```text
Towns > Katoomba
    ├── Hotels > Katoomba Hotel, Katoomba Family Hotel
    ├── Churches > Katoomba Congregational Church
    ├── Organizations > Katoomba Cricket Club, Katoomba Progress Association
    └── [all other Katoomba-related entities organized by type]
```

**Implementation:**
- Don't change thematic Towns hierarchy (already correct)
- For primary, remove non-place children from town entries
- Those entities already exist in proper primary facets (hotels under Built Environment, etc.)

---

## Scripts Created

1. **`scripts/38_audit_primary_facets.py`** - Initial audit (superseded by script 40)
   - Generated `reports/primary_facets_audit.md`
   - User reviewed with annotations

2. **`scripts/40_analyze_primary_structure.py`** ✓ COMPLETE
   - Comprehensive analysis vs archive
   - Generated `reports/primary_structure_analysis.md`
   - Identified 171 correct, 60 orphaned, 4 missing, 110 unassigned

3. **`scripts/41_fix_primary_structure.py`** - TODO: Create
   - Add 7 Getty roots
   - Remove orphaned primary parents
   - Restore 4 missing relationships
   - Provide unassigned tags list for manual assignment

4. **`scripts/42_assign_unassigned_tags.py`** - TODO: Create
   - Interactive tool to assign 110 unassigned tags
   - Fetch Zotero excerpts for context
   - Generate assignment CSV for review/approval

---

## Next Session Tasks

1. **Create script 41** - Automated fixes:
   - Add 7 Getty AAT root entries
   - Remove 60 orphaned primary parent relationships
   - Restore 4 missing Town → parent=Towns relationships
   - Validate thematic hierarchies preserved

2. **Run script 41** - Apply automated fixes

3. **Review 110 unassigned tags** - Either:
   - Option A: Create interactive script 42 with Zotero context
   - Option B: Manual review of list with thematic context

4. **Regenerate visualizations** - Run script 23

5. **Verify result** - Should have ~7-10 primary trees (7 Getty + maybe a few edge cases)

6. **Commit** - All changes with comprehensive commit message

---

## Key Preservation Rules

1. **Preserve all thematic hierarchies** - Don't touch "- THEMATIC" relationships
2. **Preserve Towns thematic structure** - Towns > [Town] > [intermediates] > [entities]
3. **Only remove PRIMARY parents** - Never remove tags themselves
4. **Keep Getty-connected hierarchies** - 171 already correct paths

---

## Expected Outcome

**Before:**
- 82 primary visualization trees
- Cluttered, confusing structure
- Mix of Getty-aligned and thematic-only roots

**After:**
- 7 Getty AAT primary trees (Agents, Places, Built Environment, Activities, Events, Associated Concepts, Materials)
- All tags accessible via primary (form-based) hierarchy
- Thematic hierarchies provide alternative exhibition views
- Clean, professional, Getty AAT-compatible structure

---

## Files Reference

**Analysis Reports:**
- `reports/primary_facets_audit.md` - Initial audit with user annotations
- `reports/primary_structure_analysis.md` - Comprehensive analysis vs archive

**Scripts:**
- `scripts/38_audit_primary_facets.py` - Initial audit generator
- `scripts/40_analyze_primary_structure.py` - Comprehensive analyzer
- `scripts/41_fix_primary_structure.py` - TODO: Automated fixer
- `scripts/42_assign_unassigned_tags.py` - TODO: Interactive assigner

**Data:**
- `data/tag_map_consolidated.csv` - Current (1071 rows)
- `archive/csv-files/poly_hierarchy_additions.csv` - Archive (679 rows)

**Visualizations:**
- `visualizations/hierarchy_trees/primary_*.txt` - Currently 82 trees, target 7
- `visualizations/hierarchy_trees/theme_*.txt` - 21 thematic trees (preserve)
