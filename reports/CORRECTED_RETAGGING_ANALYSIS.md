# Corrected Retagging Analysis - Final Scope

**Date**: 2025-11-06
**Purpose**: Corrected orphaned tags analysis with proper case-insensitive matching
**Previous Error**: Original analysis was case-sensitive, incorrectly flagged 102 tags as "orphaned"

---

## Executive Summary - CORRECTED

**Actual Situation** (much better than originally reported):

```
Total Zotero tags: 481
├── Perfect matches (no mapping needed): 335 (70%) ✅
├── Simple mappings needed: 104 (22%)
│   ├── Capitalization + leaf node correction: 102 tags
│   └── Plural → Singular: 2 tags
└── Truly orphaned (need investigation): 42 (8%)
    ├── Metadata tags: 1 tag (304 applications)
    ├── Named entities: 15 tags (106 applications)
    ├── Synonym candidates: 4 tags (22 applications)
    └── May need taxonomy addition: 22 tags (169 applications)
```

**Key Finding**: **70% of tags already match perfectly** - no mapping needed!

**Effort Estimate**:
- High-confidence mappings: **776 entries ready** (2-3 hours to review and apply)
- Remaining investigation: **42 tags** (4-6 hours)
- **Total: 6-9 hours** (down from originally estimated 22-32 hours)

---

## What Went Wrong in Original Analysis

### Error: Case-Sensitive Matching

**Original script logic**:
```python
orphaned = [tag for tag in zotero_tags if tag not in taxonomy_tags]
```

**Problem**: "Recreation for miners" (Zotero) ≠ "recreation for miners" (taxonomy)

**Result**: 102 tags incorrectly flagged as "orphaned" when they actually exist in taxonomy with different capitalization.

---

## Corrected High-Confidence Mappings (✅ READY)

### File Generated: `reports/batch_mappings_CORRECTED.csv`

**Total entries**: 776 mapping entries
**Coverage**: ~50% of all tag applications (776 of ~1,544)

### Key Mappings (following user guidance):

| Zotero Tag | Target Tag | Items | Strategy |
|------------|-----------|-------|----------|
| Hotels | hotel | 62 | Generic singular leaf (not plural parent) |
| Death | death | 53 | Case correction |
| Weather | weather | 49 | Case correction |
| Shale mines | shale mine | 48 | Already correct form |
| Recreation for miners | recreation for miners | 46 | Case correction |
| Court cases | court cases | 45 | Case correction |
| Court | court | 45 | Case correction |
| Sports | recreation activity | 39 | Map to generic recreation activity |
| Church | church | 34 | Generic leaf |
| Railway | railway | 33 | Case correction |
| Mining | mining | 32 | Case correction |
| Miners | miner | 32 | Plural → singular |
| Concerts | concert | 29 | Plural → singular |
| Councils | council | 27 | Plural → singular |
| Dances | dance | 26 | Plural → singular |

**Full list**: 27 distinct tags mapped to correct taxonomy forms

**User Guidance Applied**:
- ✅ Map generic tags (Hotels, Sport, Church) to generic singular leaves
- ✅ Don't try to resolve specific entities now (named entity recognition deferred)
- ✅ All target tags verified to exist in taxonomy
- ✅ Follows leaf-node tagging pattern

---

## Remaining Work: Truly Orphaned Tags (42 tags, 601 applications)

### Category 1: Metadata Tags (1 tag, 304 applications) - NO ACTION

| Tag | Items | Decision |
|-----|-------|----------|
| Primary source | 304 | Preserve as metadata tag (not subject tag) |

**Action**: None - preserve alongside new taxonomy tags

---

### Category 2: Already Mapped (4 tags, 22 applications) - NO ACTION

| Tag | Items | Status |
|-----|-------|--------|
| Alcohol | 12 | ✅ Already in alcohol_rationalisation report |
| Colliery | 4 | ✅ In batch_mappings_CORRECTED.csv (→ coal mine) |
| Druid's Lodge | 4 | ✅ In batch_mappings_CORRECTED.csv (→ Druid's Lodge (local lodge)) |
| Girls' cricket | 2 | ✅ In batch_mappings_CORRECTED.csv (→ cricket \| women \| adolescents) |

**Action**: None - already handled

---

### Category 3: Named Entities (15 tags, 106 applications) - NEEDS VERIFICATION

Organizations, people, and specific places that should exist in taxonomy:

**High Priority** (>10 items):
- A.K.O. & M. Company (42) - Mining company, likely exists as "Australian Kerosene Oil and Mineral Company"
- I.O.O.F. Hall (17) - Independent Order of Odd Fellows hall
- Mr Charles George Gordon (11) - Person name

**Medium Priority** (3-10 items):
- Waudby & Co. (7) - Business
- Mrs Long's Hotel (5) - Specific hotel
- Mr David Brown (4) - Person name
- Australian Kerosene Shale and Oil Company (3) - Mining company variant
- South Clifton Mine Co. (3) - Mining company
- Grand Hotel (3) - Specific hotel (may already exist in taxonomy)
- Masons (3) - Likely "Freemasons"
- U.A.O.D. (3) - United Ancient Order of Druids (abbreviation)
- Pub (3) - Likely synonym for "public house"

**Low Priority** (<3 items):
- Various company names, hotels, person names

**Action**:
1. Check if these entities exist in taxonomy under slightly different names
2. Add missing specific named entities to taxonomy
3. Create mapping entries

**Estimated effort**: 2-3 hours

---

### Category 4: Geographic/Location Tags (22 tags, 169 applications) - MIXED

Places and concepts that may need taxonomy addition or mapping:

**Likely Already Exist** (check taxonomy):
- Nellie's Glen (25) - Known location, likely exists
- Hartley Vale (20) - Known location, likely exists
- Ruined Castle (11) - Known landmark, likely exists
- Nellie's Glen track (3) - Path/track, likely exists
- Middle camp (2) - Mining camp location

**Likely Synonyms or Variants**:
- Police (27) - Check: "police" vs "police force" vs "NSW Police"
- Publican's License (11) - Likely variant of "publican's licensing"
- Stores (9) - Check if synonym for "retailer or store"
- Katoomba South mines (8) - Already in batch (→ Katoomba South \| coal mine)
- Mining settlements (7) - Check if exists
- Oddfellows (2) - Variant of "Odd Fellows"
- Rifle reserves (2) - May already be mapped

**May Need Addition**:
- Trucking (8) - Transport activity
- Rape (5) - Criminal event (sexual assault)
- Billiard (3) - Recreation activity variant
- Peckman Bros (3) - Business name
- Port Kembla disaster (3) - Specific event
- Katoomba Tennis Club (2) - Specific organization
- Post (9) - Unclear (postal service? position?)

**Action**:
1. Search taxonomy for each tag (case-insensitive, variant spellings)
2. Create synonym mappings for found tags
3. Flag for taxonomy addition if genuinely missing
4. Review contexts for ambiguous tags

**Estimated effort**: 2-3 hours

---

## Implementation Plan

### Step 1: Apply High-Confidence Batch (✅ READY NOW)

**File**: `reports/batch_mappings_CORRECTED.csv`
**Entries**: 776
**Effort**: 1-2 hours (review + merge into tag_application_mapping.csv)

**Actions**:
1. Review batch file for any obvious errors
2. Append to `data/tag_application_mapping.csv`
3. Validate no duplicate entries
4. Update git

**Expected outcome**: Coverage increases from 24% to ~60% of library

---

### Step 2: Verify Named Entities (15 tags, 106 applications)

**Effort**: 2-3 hours

**Actions**:
1. Search taxonomy for each named entity
2. Check for variant spellings/abbreviations
3. Create mapping entries for found entities
4. Document missing entities for taxonomy addition

**Output**: Mapping entries for ~10-15 named entities

---

### Step 3: Resolve Geographic/Location Tags (22 tags, 169 applications)

**Effort**: 2-3 hours

**Actions**:
1. Search taxonomy for each location/concept
2. Create synonym mappings
3. Flag genuinely missing terms

**Output**: Mapping entries + list of taxonomy gaps

---

### Step 4: Validate and Deploy

**Effort**: 1 hour

**Actions**:
1. Run validation script (check all add_tags exist)
2. Verify leaf node uniqueness (CRITICAL for query expansion)
3. Generate coverage statistics
4. Update documentation

---

## Revised Statistics

### Before This Work

```
Mapped items: 102 (24% of 417 items)
Mapped entries: 133
```

### After Step 1 (Apply Batch)

```
Mapped entries: 133 + 776 = 909
Estimated unique items: ~220-250 (53-60% of library)
```

### After Steps 2-3 (Complete Investigation)

```
Estimated additional entries: ~150-200
Estimated total coverage: ~70-80% of library
Remaining: Named entity recognition, tag enrichment (future work)
```

---

## Files Generated This Session

### Batch Mapping Files
1. ✅ **`reports/batch_mappings_CORRECTED.csv`** - 776 entries (READY TO APPLY)
2. ~~`reports/batch_mappings_cat1-4.csv`~~ - Superseded by corrected version
3. ~~`reports/batch_mappings_cat2.csv`~~ - Superseded by corrected version

### Analysis Reports
1. **`reports/CORRECTED_RETAGGING_ANALYSIS.md`** - This file (corrected scope)
2. ~~`reports/ORPHANED_FOLKSONOMY_TAGS.md`~~ - Original (incorrect) analysis
3. ~~`reports/RETAGGING_MAPPING_WORK_LIST.md`~~ - Based on incorrect analysis
4. **`reports/PHASE_2_PROGRESS_REPORT.md`** - Progress summary (needs update)

---

## Key Takeaways

### What We Learned

1. **70% of tags already match** - Original "109 orphaned tags" was due to case-sensitive matching error

2. **776 high-confidence mappings ready** - Following user guidance on generic singular leaves

3. **Only 42 truly orphaned tags remain** - Down from originally reported 109

4. **Effort reduced by 75%** - From 22-32 hours to 6-9 hours total

### User Guidance Applied

✅ **Generic tags → generic singular leaves**
- Hotels → hotel (not plural parent)
- Sport/Sports → recreation activity
- Church → church

✅ **Defer named entity resolution**
- Don't try to identify specific hotels/entities from titles alone
- Named entity recognition is future work
- Accept some loss of specificity for efficiency

✅ **Focus on leaf-node pattern**
- All mappings target leaf nodes
- No parent nodes in add_tags
- Supports query expansion implementation

---

## Next Steps - User Decision Point

### Option A: Apply Batch Now (Recommended)

**Immediate action**: Apply 776 entries from batch_mappings_CORRECTED.csv

**Pros**:
- Immediate 24% → 60% coverage improvement
- Validates mapping process
- Enables early testing
- High confidence (all targets verified)

**Cons**: None significant

**Time**: 1-2 hours

---

### Option B: Complete Investigation First

**Immediate action**: Resolve 42 orphaned tags before applying batch

**Pros**:
- One comprehensive application
- Complete picture of taxonomy gaps

**Cons**:
- Delays validation of 776 ready entries
- Additional 4-6 hours before any application

**Time**: 6-8 hours total

---

### Option C: Hybrid (Recommended)

**Immediate action**:
1. Apply 776 batch entries now (1-2 hours)
2. Continue investigation of 42 orphaned tags (4-6 hours)
3. Apply second batch when ready

**Pros**:
- Progressive deployment
- Early validation
- Flexibility to adjust based on findings

**Time**: Same total, but staged

---

## Recommendation

**Apply batch_mappings_CORRECTED.csv immediately**, then continue with investigation.

**Rationale**:
- 776 entries are high confidence (all targets verified)
- Represents ~50% of all tag applications
- Following user's guidance on generic mapping strategy
- Allows early validation of approach
- Remaining 42 tags require more investigation anyway

---

