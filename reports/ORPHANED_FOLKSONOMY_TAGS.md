# Orphaned Folksonomy Tags - Complete Analysis

**Date**: 2025-11-06
**Critical Finding**: 109 folksonomy tags in current Zotero items DO NOT EXIST in the new taxonomy

---

## Executive Summary

**The Real Scope:**
- Total tags in Zotero: **481**
- Tags that exist in new taxonomy: **372** (77%)
- **Tags that DON'T exist in new taxonomy: 109 (23%)**
- **Total orphaned tag applications: 1,544**

This means ~23% of the current folksonomy tags are completely unmapped and will be LOST unless we create mapping entries.

---

## Top 50 Orphaned Tags (By Usage)

| Rank | Tag | Items | Status | Mapping Strategy |
|------|-----|-------|--------|------------------|
| 1 | Primary source | 304 | ✅ Metadata | Preserve separately (not subject tag) |
| 2 | **Hotels** | 62 | ⚠️ UNMAPPED | Parent/folksonomy → Hotel (generic) OR specific hotel names |
| 3 | Death | 53 | ⚠️ UNMAPPED | Should map to "death" in taxonomy (check capitalization) |
| 4 | Weather | 49 | ⚠️ UNMAPPED | Should exist in taxonomy - check if capitalization issue |
| 5 | Shale mines | 48 | ⚠️ UNMAPPED | Plural → "shale mine" (singular) OR specific mine names |
| 6 | Recreation for miners | 46 | ⚠️ UNMAPPED | Thematic concept - map to appropriate activities |
| 7 | Court | 45 | ⚠️ UNMAPPED | Generic → "court" OR specific courts |
| 8 | Court cases | 45 | ⚠️ UNMAPPED | Event type - should be in taxonomy |
| 9 | Sports | 39 | ⚠️ UNMAPPED | Parent/plural → specific sports OR "sport" (generic) |
| 10 | Church | 34 | ⚠️ UNMAPPED | Singular generic vs. "Churches" parent? |
| 11 | Railway | 33 | ⚠️ UNMAPPED | Should be "railway" OR "railways" in taxonomy |
| 12 | **Mining** | 32 | ⚠️ UNMAPPED | Activity, place, or industry? Needs facet determination |
| 13 | Miners | 32 | ⚠️ UNMAPPED | Plural → "miner" (singular) |
| 14 | Councils | 27 | ⚠️ UNMAPPED | Plural → specific council names OR "council" |
| 15 | Post office | 23 | ⚠️ UNMAPPED | Should be in taxonomy (postal services) |
| 16 | Progress committees | 22 | ⚠️ UNMAPPED | Organizational type |
| 17 | Tourism | 20 | ⚠️ UNMAPPED | Activity/industry |
| 18 | Unemployment | 19 | ⚠️ UNMAPPED | Economic concept |
| 19 | Licensing | 19 | ⚠️ UNMAPPED | Regulatory process |
| 20 | Horses | 19 | ✅ MAPPED | Already in horses_reclassification report |
| 21 | Charity | 18 | ⚠️ UNMAPPED | Activity type |
| 22 | Coal | 18 | ⚠️ UNMAPPED | Material |
| 23 | Election | 17 | ⚠️ UNMAPPED | Event type |
| 24 | Injury | 17 | ⚠️ UNMAPPED | Physical condition |
| 25 | Illness | 16 | ⚠️ UNMAPPED | Physical condition (some mapped already) |
| 26 | Accident | 16 | ⚠️ UNMAPPED | Event type |
| 27 | Mining accidents | 16 | ⚠️ UNMAPPED | Specific event type |
| 28 | Roads | 15 | ⚠️ UNMAPPED | Plural → "road" OR specific road names |
| 29 | Cricket clubs | 15 | ⚠️ UNMAPPED | Organizational type |
| 30 | Miners' dwellings | 14 | ✅ EXISTS | Check capitalization |
| 31 | Cricket | 14 | ⚠️ UNMAPPED | Sport - should be in taxonomy |
| 32 | Strike | 14 | ⚠️ UNMAPPED | Event/activity type |
| 33 | Tramway | 14 | ⚠️ UNMAPPED | Infrastructure |
| 34 | Shooting | 13 | ⚠️ UNMAPPED | Activity |
| 35 | Marriage | 13 | ⚠️ UNMAPPED | Event type |
| 36 | Alcohol | 12 | ✅ MAPPED | All 12 items mapped in alcohol_rationalisation |
| 37 | School | 12 | ⚠️ UNMAPPED | Singular vs. "Schools" parent |
| 38 | Funeral | 12 | ⚠️ UNMAPPED | Event type |
| 39 | Reserves | 11 | ⚠️ UNMAPPED | Place type - plural |
| 40 | Theft | 11 | ⚠️ UNMAPPED | Criminal event |
| 41 | Gold mining | 10 | ⚠️ UNMAPPED | Activity type |
| 42 | Stores | 9 | ⚠️ UNMAPPED | Plural → "store" OR specific names |
| 43 | School of Arts | 9 | ⚠️ UNMAPPED | Specific building type |
| 44 | Katoomba coal mines | 9 | ⚠️ UNMAPPED | Location + facility |
| 45 | Fire | 8 | ⚠️ UNMAPPED | Event/disaster type |
| 46 | Dogs | 8 | ⚠️ UNMAPPED | Animal - should be in taxonomy |
| 47 | Gambling | 8 | ⚠️ UNMAPPED | Activity |
| 48 | Horticulture society | 8 | ⚠️ UNMAPPED | Organization type |
| 49 | Disease | 8 | ⚠️ UNMAPPED | Physical condition |
| 50 | Railway commission | 8 | ⚠️ UNMAPPED | Government body |

---

## Analysis by Category

### Category A: Capitalization/Spelling Issues (CHECK FIRST)

These tags might exist in taxonomy with different capitalization:
- Death vs. death
- Weather vs. weather
- Church vs. church OR Churches
- Court vs. court
- Sports vs. sport OR Sports
- School vs. school OR Schools
- Reserves vs. reserves

**Action**: Case-insensitive taxonomy lookup

---

### Category B: Plural → Singular Transformations

These are plural folksonomy tags that need singular leaf forms:
- Hotels → Hotel (62 items)
- Shale mines → shale mine (48 items)
- Miners → miner (32 items)
- Councils → council (27 items)
- Roads → road (15 items)
- Cricket clubs → cricket club (15 items)
- Stores → store (9 items)
- Reserves → reserve (11 items)

**Action**: Pattern-based mapping (plural → singular generic leaf)

**Estimated**: ~200+ tag applications

---

### Category C: Event/Activity Types Needing Taxonomy Addition

These are legitimate event/activity concepts that should exist:
- Court cases (45 items)
- Election (17 items)
- Accident (16 items)
- Mining accidents (16 items)
- Strike (14 items)
- Marriage (13 items)
- Funeral (12 items)
- Theft (11 items)
- Fire (8 items)

**Action**: Check if exists with different names, or add to taxonomy

**Estimated**: ~140 tag applications

---

### Category D: Requires Facet Determination

These need analysis to determine correct facet/hierarchy:
- Mining (32 items) - Activity? Place? Industry?
- Tourism (20 items) - Activity? Economic sector?
- Licensing (19 items) - Process? Event?
- Charity (18 items) - Activity? Organization type?
- Coal (18 items) - Material? Industry?
- Railway (33 items) - Infrastructure? Organization?

**Action**: Context review to determine appropriate taxonomy placement

**Estimated**: ~150 tag applications

---

### Category E: Already Mapped or Metadata

- Primary source (304) - Metadata, preserve separately ✅
- Alcohol (12) - Already mapped ✅
- Horses (19) - Already mapped ✅
- Illness (some) - Partially mapped

**Action**: No action needed

---

### Category F: Complex Consolidations

These require detailed decisions:
- Recreation for miners (46 items) - Thematic concept
- Progress committees (22 items) - Organization type
- School of Arts (9 items) - Dual nature (building + organization)
- Katoomba coal mines (9 items) - Location + facility
- Horticulture society (8 items) - Organization type

**Action**: Case-by-case analysis and mapping

**Estimated**: ~100 tag applications

---

## Revised Scope Estimate

### Total Orphaned Tags: 109 tags
### Total Applications: 1,544

**Breakdown by action required:**
| Category | Tags | Applications | Effort |
|----------|------|--------------|---------|
| Metadata (skip) | 1 | 304 | 0 hrs |
| Already mapped | 3 | 43 | 0 hrs |
| Capitalization check | 10 | ~150 | 1 hr |
| Plural → Singular | 10+ | ~200 | 2-3 hrs |
| Events/Activities | 10+ | ~140 | 3-4 hrs |
| Facet determination | 8 | ~150 | 4-6 hrs |
| Complex consolidations | 10+ | ~100 | 4-6 hrs |
| **Remaining unmapped** | ~55 | ~450 | 8-12 hrs |

**Total estimated effort**: 22-32 hours

---

## CRITICAL INSIGHT

**The current mapping CSV has only 102 unique items mapped (24% of library).**

**The real retagging scope is:**
- ~1,200 orphaned tag applications (excluding metadata)
- Affecting unknown number of items (many items have multiple orphaned tags)
- Requiring systematic transformation of folksonomy → controlled vocabulary

**This is NOT just about creating mapping entries - it's about completing the vocabulary rationalization project.**

---

## Recommended Immediate Actions

### 1. Case-Insensitive Taxonomy Lookup
Many "orphaned" tags may exist with different capitalization. Quick script can resolve.

**Output**: Reduced orphaned list

---

### 2. Pattern-Based Automated Mappings
For clear cases (plurals, known variants), generate mappings automatically.

**Output**: ~200 mapping entries auto-generated

---

### 3. Build Dry Run Script (Phase 5) NOW
Before continuing manual mappings, build validation to:
- Show what would happen to every item
- Auto-detect patterns
- Flag truly problematic cases

**Rationale**: Avoid manual work that could be automated

---

### 4. Prioritize by Impact
Focus on high-usage tags first:
- Hotels (62)
- Death (53)
- Weather (49)
- Shale mines (48)
- Recreation for miners (46)

**These 5 tags alone = 258 applications (17% of orphaned tags)**

---

## Questions for User

1. **Scope confirmation**: Are you aware this is ~1,200 orphaned tag applications, not just the 100-200 we initially thought?

2. **Effort tolerance**: 22-32 hours of manual mapping work - proceed or seek automation first?

3. **Strategy preference**:
   - Option A: Build automation scripts first (Phase 5), then handle exceptions
   - Option B: Continue systematic manual mapping
   - Option C: Hybrid - automate obvious patterns, manually handle complex cases

4. **Metadata handling**: Confirm Primary/Secondary source tags should be preserved alongside new taxonomy tags?

---

