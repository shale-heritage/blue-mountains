# Phantom Facets Cleanup Report

**Date:** 2025-11-17
**Issue:** Extraneous primary facets appearing in hierarchy visualizations
**Scripts:** 65, 66
**Result:** ✓ RESOLVED - Clean 8 primary facets confirmed

---

## Problem Identified

User reported seeing extraneous primary facets in visualizations:
- Cottages
- Law enforcement (intermediate facet)
- Legal officials (intermediate facet)
- Public houses
- Transport
- Transport & logistics businesses

Expected: Only 8 primary facets (Activities, Agents, Associated Concepts, Built Environment, Events, Information Forms, Materials, Places)

---

## Root Cause Analysis

### Issue 1: Audit Trail Entries (status=removed)

13 entries with `status=removed` were retained as audit trail documentation but contained parent references to phantom nodes:

**Examples:**
```csv
trucking,trucking,hierarchy,parent=Transport - REMOVED by script 48 (regression),removed
Cottage,Cottage,hierarchy,parent=Cottages - REMOVED by script 52 (obsolete unqualified form),removed
public house,public house,hierarchy,parent=Public houses - REMOVED by script 52 (obsolete unqualified form),removed
```

**Problem:** The visualization script extracts ALL parent names from the CSV, including these phantom "REMOVED by script XX" references, treating them as top-level facets.

**Affected entries:**
- 5× trucking (referencing phantom Transport, Commercial transport parents)
- 3× bankruptcy (referencing phantom Economic distress, Legal outcomes parents)
- 2× Cottage, public house (referencing phantom Cottages, Public houses parents)
- 3× synonym corrections (Constable, St Hilda's Church variants)

**Total:** 13 removed entries

### Issue 2: Phantom Intermediate Facet References

2 entries referenced non-existent intermediate facet parents:

```csv
Police,Police,hierarchy,parent=law enforcement (intermediate facet),active
coroners,coroners,hierarchy,parent=legal officials (intermediate facet),active
```

**Problem:** The actual intermediate nodes are named "law enforcement" and "legal officials" (without the "(intermediate facet)" annotation). These phantom parent names caused the visualization to create false top-level facets.

**Note:** coroners also had a correct duplicate entry with `parent=legal officials` (line 1487).

---

## Solution Implemented

### Script 65: Remove Audit Trail Entries

**Purpose:** Delete all entries with `status=removed` - they served their audit purpose but now cause confusion.

**Changes:**
- Removed 13 audit trail entries
- Total entries: 1,846 → 1,833
- Verified no phantom "REMOVED" parent references remain

**Backup:** `data/tag_map_consolidated.20251117_160343.bak`

### Script 66: Fix Phantom Intermediate Facet References

**Purpose:** Correct parent references and remove duplicate entries.

**Changes:**
1. Fixed Police parent: `law enforcement (intermediate facet)` → `law enforcement`
2. Removed duplicate coroners entry with phantom parent (kept correct entry at line 1487)

**Statistics:**
- Fixed: 1 parent reference
- Removed: 1 duplicate entry
- Total entries: 1,833 → 1,832

**Backup:** `data/tag_map_consolidated.20251117_160448.bak`

---

## Verification

### Before Cleanup
```
Identified 18 top-level primary facets:
  - Activities
  - Agents
  - Associated Concepts
  - Built Environment
  - Cottages - REMOVED by script 52 (obsolete unqualified form)  ← PHANTOM
  - Events
  - Information Forms
  - Law enforcement (intermediate facet)  ← PHANTOM
  - Legal officials (intermediate facet)  ← PHANTOM
  - Materials
  - Places
  - Public houses - REMOVED by script 52 (obsolete unqualified form)  ← PHANTOM
  - Transport & logistics businesses - REMOVED by script 48 (regression)  ← PHANTOM
  - Transport - REMOVED by script 48 (regression)  ← PHANTOM
  - ... (capitalization variants)
```

### After Cleanup
```
Identified 8 top-level primary facets:
  - Activities
  - Agents
  - Associated Concepts
  - Built Environment
  - Events
  - Information Forms
  - Materials
  - Places
```

✓ **PERFECT** - Exactly 8 primary facets as designed

---

## Final State

**CSV Structure:**
- Total entries: 1,832
- Active entries: 1,832 (100%)
- Removed entries: 0 (audit trail cleaned)
- Primary facets: 8 (correct)
- Thematic groupings: 29

**Hierarchy Visualizations:**
- 8 primary facet trees
- 29 thematic grouping trees
- 1 overview document
- **Total: 38 files** (previously 70 with phantoms)

---

## Quality Impact

### Before
- ❌ 18 "primary facets" (10 phantoms)
- ❌ 51+ "thematic groupings" (capitalization duplicates)
- ❌ 70 visualization files
- ❌ Confusing audit trail entries mixed with active taxonomy

### After
- ✓ 8 primary facets (correct)
- ✓ 29 thematic groupings (clean)
- ✓ 38 visualization files
- ✓ Clean active taxonomy only
- ✓ Audit trail preserved in backups

---

## Lessons Learned

1. **Audit trail entries should be fully removed** after their documentation purpose is served (not kept with status=removed)

2. **Parent references must exactly match existing node names** - annotations like "(intermediate facet)" create phantom nodes

3. **Visualization scripts should filter by status=active** to avoid processing removed entries

4. **Regular validation of top-level facet count** catches structural issues early

---

## Documentation Updates Required

- [x] Create cleanup report (this document)
- [ ] Update docs/taxonomy-csv-structure.md with new entry counts
- [ ] Update reports/ontologist-review.md with corrected facet count
- [ ] Update reports/final_qa_report.md if needed

---

## Next Steps

1. ✓ Phantom facets removed
2. ✓ Visualizations regenerated (38 clean files)
3. → Update documentation with new counts
4. → Proceed with Getty AAT crosswalk mapping

---

**Conclusion:** Taxonomy structure is now clean with exactly 8 primary facets and 29 thematic groupings. Ready for deployment and AAT crosswalk.
