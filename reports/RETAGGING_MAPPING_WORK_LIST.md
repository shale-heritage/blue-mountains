# Retagging Mapping Work List - Complete Action Plan

**Date**: 2025-11-06
**Purpose**: Comprehensive list of all mapping entries that need to be created or reviewed
**Scope**: 109 orphaned tags = 1,544 applications

---

## Executive Summary

Based on systematic analysis of all orphaned folksonomy tags, here is the complete work breakdown:

| Category | Tags | Applications | Effort | Status |
|----------|------|--------------|--------|--------|
| 1. Capitalization synonyms | 14 | 314 | 30 min | Ready to automate |
| 2. Plural → Singular | 8 | 219 | 1-2 hrs | Ready (needs review) |
| 3. Simple synonyms | 3 | 12 | 30 min | Ready |
| 4. Multi-tag replacements | 2 | 10 | 30 min | Ready |
| 5. Context-dependent (exist in taxonomy) | 11 | 260 | 3-4 hrs | Needs disambiguation |
| 6. Event types | 8 | 140 | 2-3 hrs | Needs review |
| 7. Already mapped | 4 | 359 | 0 hrs | Complete ✅ |
| 8. Complex/remaining | ~58 | ~230 | 8-12 hrs | Needs investigation |
| **TOTAL** | **109** | **1,544** | **16-25 hrs** | **In progress** |

---

## CATEGORY 1: Capitalization Synonyms (AUTOMATED)

**Tags**: 14
**Applications**: 314
**Effort**: 30 minutes
**Action**: Create automated synonym mappings (OLD_TAG → lowercase)

### Mappings to Create

| Old Tag (Zotero) | New Tag (Taxonomy) | Items | Notes |
|------------------|-------------------|-------|-------|
| Death | death | 53 | Case variant |
| Weather | weather | 49 | Case variant |
| Court | court | 45 | Case variant |
| Sports | sports | 39 | Case variant |
| Church | church | 34 | Case variant |
| Cricket | cricket | 14 | Case variant |
| Marriage | marriage | 13 | Case variant |
| School | school | 12 | Case variant |
| Funeral | funeral | 12 | Case variant |
| Reserves | reserves | 11 | Case variant (note: different from "reserve" singular) |
| Fire | fire | 8 | Case variant |
| Dogs | dogs | 8 | Case variant |
| Gambling | gambling | 8 | Case variant |
| Disease | disease | 8 | Case variant |

**Implementation**: Can be automated with pattern-based script or batch CSV creation.

---

## CATEGORY 2: Plural → Singular Transformations

**Tags**: 8
**Applications**: 219
**Effort**: 1-2 hours (requires item-by-item review for specific named entities)
**Action**: Map to singular generic leaf, OR identify specific named entity

### Mappings to Create

| Old Tag (Zotero) | Default New Tag | Items | Review Strategy |
|------------------|-----------------|-------|-----------------|
| Hotels | hotel | 62 | ⚠️ Check if specific hotel named (e.g., Grand Hotel, Imperial Hotel) |
| Shale mines | shale mine | 48 | ⚠️ Check if specific mine named |
| Miners | miner | 32 | ⚠️ Check context: generic miner vs specific person name |
| Councils | council | 27 | ⚠️ Check if specific council named (e.g., Katoomba Council) |
| Roads | road | 15 | ⚠️ Check if specific road named |
| Cricket clubs | cricket club | 15 | ⚠️ Check if specific club named |
| Reserves | reserve | 11 | Direct mapping (generic) |
| Stores | retailer or store | 9 | ⚠️ Check if specific business named |

**Implementation Strategy**:

1. **Quick scan approach** (1 hour):
   - Review item titles for obvious named entities
   - Default to generic for unclear cases
   - Accept some loss of specificity

2. **Detailed review approach** (2 hours):
   - Review full item contexts
   - Identify all specific named entities
   - Create specific mappings for each

**Examples**:

```csv
# Generic mapping
"Mountain Mixtures (1892)","Hotels","hotel","Generic reference to hotels"

# Specific mapping
"Grand Hotel Opening (1891)","Hotels","Grand Hotel","Specific hotel named in text"
```

---

## CATEGORY 3: Simple Synonyms & Consolidations

**Tags**: 3
**Applications**: 12
**Effort**: 30 minutes
**Action**: Create direct synonym mappings (decisions already documented in taxonomy)

### Mappings to Create

| Old Tag (Zotero) | New Tag (Taxonomy) | Items | Notes |
|------------------|-------------------|-------|-------|
| Colliery | coal mine | 4 | UK/Australian synonym for coal mine |
| Druid's Lodge | Druid's Lodge (local lodge) | 4 | Disambiguated form exists in taxonomy |
| Katoomba Street | Katoomba Street | 4 | Already correct - verify no other changes needed |

**Implementation**: Create 4 mapping entries (3 actual changes + 1 verification).

**Note**: Colliery items from undecided_tags_status.md:
1. Local Jottings (19 July 1890)
2. The Collieries and Big-Head Mines of New South Wales (1887)
3. New South Wales Railway Enquiry (13 December 1905)
4. (1 more)

---

## CATEGORY 4: Multi-Tag Replacements

**Tags**: 2
**Applications**: 10
**Effort**: 30 minutes
**Action**: Replace single folksonomy tag with multiple controlled vocabulary tags

### Mappings to Create

| Old Tag (Zotero) | Remove | Add Tags | Items | Notes |
|------------------|--------|----------|-------|-------|
| Girls' cricket | Girls' cricket | cricket \| women \| adolescents | 2 | Merge decision: sport + demographic |
| Katoomba South mines | Katoomba South mines | Katoomba South \| coal mine | 8 | Geographic folksonomy: location + facility |

**Implementation**: Create mapping entries with pipe-delimited add_tags.

**Girls' cricket items**:
1. Girls Cricket Match at Katoomba (26 April 1895)
2. The Rockley Game (7 February 1896)

**Katoomba South mines items**: 8 items from undecided_tags_status.md

---

## CATEGORY 5: Context-Dependent Mappings (All Exist in Taxonomy)

**Tags**: 11
**Applications**: 260
**Effort**: 3-4 hours
**Action**: Review item contexts to determine correct taxonomy tag (all target tags verified to exist)

### 5.1 Mining (32 items) - FACET DISAMBIGUATION

**Challenge**: "Mining" folksonomy tag could map to multiple taxonomy facets:

| Possible Mapping | Facet | When to Use |
|------------------|-------|-------------|
| mining | Activities | Mining as an activity/industry |
| mine | Built Environment | Mining as a place/location |
| miner | Agents | Mining as a person/occupation |
| mining company | Agents | Mining as an organization |

**Strategy**: Review contexts to determine which facet each item refers to.

**Estimated breakdown**:
- mining (activity): ~15 items
- mine (place): ~10 items
- miner (person): ~5 items
- mining company: ~2 items

**Effort**: 1-1.5 hours

---

### 5.2 Direct Mappings (10 tags = 228 items)

These tags exist in taxonomy and likely just need direct carryover:

| Old Tag | New Tag (Verified) | Items | Notes |
|---------|-------------------|-------|-------|
| Court cases | court cases | 45 | Direct match - verify correct |
| Recreation for miners | recreation for miners | 46 | Thematic concept - verify exists |
| Railway | railway | 33 | Likely infrastructure sense |
| Licensing | liquor licensing OR publican's licensing | 19 | Determine which |
| Post office | post office | 23 | Direct match |
| Progress committees | progress committee | 22 | Singular form exists |
| Tourism | tourism | 20 | Direct match |
| Unemployment | unemployment | 19 | Direct match |
| Charity | charity | 18 | Direct match |
| Coal | coal | 18 | Direct match |

**Estimated Effort**: 1.5-2 hours (verify each mapping is semantically correct)

**Implementation**: Create direct mappings, flag any that seem incorrect for manual review.

---

## CATEGORY 6: Event Types Needing Verification

**Tags**: 8
**Applications**: 140
**Effort**: 2-3 hours
**Action**: Verify these event/activity types exist in taxonomy, create mappings

| Old Tag | Expected New Tag | Items | Notes |
|---------|------------------|-------|-------|
| Election | election | 17 | Event type - verify exists |
| Accident | accident | 16 | Event type - verify exists |
| Mining accidents | mining accidents | 16 | Specific event type - verify exists |
| Strike | strike | 14 | Event/activity - verify exists |
| Theft | theft | 11 | Criminal event - verify exists |
| Injury | injury | 17 | Physical condition - verify exists |
| Illness | illness | 16 | Physical condition (some mapped already) |
| Tramway | tramway | 14 | Infrastructure type - verify exists |

**Strategy**:
1. Check taxonomy for each term
2. Create direct mappings if found
3. Document if not found (need taxonomy additions)

---

## CATEGORY 7: Already Mapped or Metadata

**Tags**: 4
**Applications**: 359
**Effort**: 0 hours ✅
**Status**: Complete - no action needed

| Tag | Items | Status | Notes |
|-----|-------|--------|-------|
| Primary source | 304 | Metadata | Preserve separately (not subject tag) |
| Alcohol | 12 | Mapped | All 12 items in alcohol_rationalisation report |
| Horses | 19 | Mapped | Covered in horses_reclassification report |
| Illness | (partial) | Partially mapped | Some items already have mappings |

**Action**: None - these are complete.

---

## CATEGORY 8: Complex & Remaining Tags

**Tags**: ~58
**Applications**: ~230
**Effort**: 8-12 hours
**Action**: Requires detailed investigation, context review, and/or taxonomy additions

This category includes tags that need more detailed analysis:

- Geographic place names that may not exist in taxonomy
- Organization names requiring verification
- Specific events that may need new taxonomy entries
- Ambiguous terms requiring facet determination
- Low-usage tags (1-5 items each)

**Strategy**: Defer to Phase 4.1 (Archive Review) and Phase 6 (Iterative Refinement)

**Examples** (partial list):
- School of Arts (9 items) - dual nature entity
- Katoomba coal mines (9 items) - location + facility
- Horticulture society (8 items) - organization type
- Railway commission (8 items) - government body
- Various low-usage tags

---

## Implementation Priorities

### IMMEDIATE (Categories 1-4): 553 applications, 2.5-3.5 hours

These can be completed quickly with high confidence:

1. ✅ **Capitalization synonyms** (314 applications) - Automate
2. ✅ **Simple synonyms** (12 applications) - Manual entry
3. ✅ **Multi-tag replacements** (10 applications) - Manual entry
4. ⚠️ **Plural → Singular** (219 applications) - Needs item review

**Deliverable**: ~350 new mapping entries

---

### HIGH PRIORITY (Category 5-6): 400 applications, 5-7 hours

Complete these before dry run:

1. **Mining disambiguation** (32 applications) - Context review
2. **Direct mappings verification** (228 applications) - Verify + create
3. **Event types** (140 applications) - Verify taxonomy + create

**Deliverable**: ~260 new mapping entries

---

### MEDIUM PRIORITY (Category 8): 230 applications, 8-12 hours

Defer to later phases:

1. Complex consolidations
2. Low-usage tags
3. Taxonomy gap discoveries

**Deliverable**: Remaining ~150-200 mapping entries

---

## Validation Requirements

Before deployment, verify:

1. ✅ All `add_tags` values exist in `data/tag_map_consolidated.csv`
2. ✅ All mapping entries use correct CSV format
3. ✅ No duplicate mappings for same item
4. ✅ All leaf nodes are unique (CRITICAL for query expansion)
5. ✅ No tags lost (every current Zotero tag either mapped or explicitly flagged for removal)

---

## Next Steps

### Step 1: Complete Immediate Priority Mappings

**Categories 1-4** (553 applications, 2.5-3.5 hours)

Create CSV batch for:
- 14 capitalization synonyms
- 3 simple synonyms
- 2 multi-tag replacements
- Review Hotels (62 items) for specific names

---

### Step 2: Complete High Priority Mappings

**Categories 5-6** (400 applications, 5-7 hours)

Verify taxonomy and create mappings for:
- Mining facet disambiguation
- Direct carryover tags
- Event types

---

### Step 3: Build Dry Run & Validation Scripts (Phase 5)

**Before continuing with Category 8**:
- Build scripts/50_retagging_dry_run.py
- Build scripts/51_validate_retagging.py
- Run validation to catch any remaining gaps

---

### Step 4: Iterative Refinement (Phase 6)

**Category 8 + validation discoveries**:
- Address complex cases
- Handle validation findings
- Complete remaining ~200 mappings

---

## Files Referenced

- `data/tag_map_consolidated.csv` - Source of truth for taxonomy
- `data/zotero_full_export.json` - Current Zotero tags
- `data/tag_application_mapping.csv` - Master retagging decisions
- `reports/ORPHANED_FOLKSONOMY_TAGS.md` - Original analysis
- `reports/undecided_tags_status.md` - Undecided orphaned tags
- `reports/alcohol_reconciliation_analysis.md` - Alcohol decisions

---

