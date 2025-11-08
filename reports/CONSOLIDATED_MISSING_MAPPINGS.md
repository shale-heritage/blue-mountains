# Consolidated Missing Retagging Mappings

**Date**: 2025-11-06
**Purpose**: Comprehensive list of all items requiring retagging map entries before deployment

---

## Executive Summary

**Current Status:**
- Total Zotero items: **417**
- Items with mapping entries: **102** (24%)
- Items needing mapping: **315** (76%)
- Unique tags in use: **481**

**Critical Finding:**
Major parent node tags are being used directly on items, violating leaf-node-only pattern:
- **Accommodation**: 64 items
- **Hotels**: 62 items
- **Mining**: 32 items

**Total missing mappings**: Estimated **350-400 entries** needed

---

## Category 1: Parent Node → Leaf Node Transformations (HIGH PRIORITY)

These items currently have parent node tags that MUST be replaced with leaf nodes.

### 1.1 Accommodation Tag (64 items)

**Issue**: "Accommodation" is a parent node, not a leaf. Items need specific accommodation type.

**Already mapped**: 63/64 (from accommodation_approval report)

**Still missing**: 1 item marked "TBD - needs content extraction"

**Mapping strategy**: Each item needs specific leaf like:
- `Hotel` (generic) OR specific hotel name
- `Boarding house` OR specific boarding house name
- `Cottage`
- `Dwellings`

**Source**: reports/ACCOMMODATION_TAGS_APPROVAL.md

---

### 1.2 Hotels Tag (62 items)

**Issue**: "Hotels" is a plural parent node. Per leaf-node pattern, should be:
- `Hotel` (singular generic leaf) for unspecified hotels
- OR specific hotel name (e.g., `Grand Hotel`, `Imperial Hotel`)

**Currently mapped**: 0/62

**Mapping strategy**:
- Review each item's context
- If specific hotel named → use that hotel's leaf tag
- If generic reference "a hotel", "the hotel" → use `Hotel` (singular)

**Action required**: Create 62 mapping entries

**Estimated effort**: 4-6 hours (need context review for each)

---

### 1.3 Mining Tag (32 items)

**Issue**: "Mining" could refer to:
- Mining (activity) - already correct if leaf node in Activities facet
- Mines (places) - parent node, needs specific mine name or `mine` (generic)
- Mining companies - needs company name
- Miners (people) - correct if under Agents

**Currently mapped**: Unknown - needs investigation

**Action required**: Review all 32 items to determine correct facet and leaf node

**Estimated effort**: 3-4 hours

---

## Category 2: Report-Based Retagging Decisions (MEDIUM PRIORITY)

Items with explicit retagging decisions in reports but not yet in mapping CSV.

### 2.1 Undecided Orphaned Tags

| Tag | Items | Mapped | Missing |
|-----|-------|--------|---------|
| Carrington | 4 | 0 | 4 |
| Colliery | 4 | 0 | 4 |
| Druid's Lodge | 4 | 0 | 4 |
| Girls' cricket | 2 | 0 | 2 |
| Katoomba South mines | 8 | 0 | 8 |
| Katoomba Street | 4 | 0 | 4 |
| **Subtotal** | **26** | **0** | **26** |

**Mapping decisions already made in taxonomy** - just need mapping entries created.

**Estimated effort**: 2-3 hours

---

### 2.2 Family Hotels (5 items - analysis only)

**Status**: reports/family_hotels_analysis.md contains recommendations but not formal retagging decisions

**Items**:
1. Girls Cricket Match at Katoomba (26 April 1895) - Already has accommodation mapping
2. Granted (26 March 1892) - No mapping
3. Katoomba Progress Association (4 August 1905) - No mapping
4. Death of Mrs. Nimmo (3 December 1926) - Mapped ✓
5. Notice of Application Publican's Licence (19 June 1896) - No mapping
6. Mountain Mixtures (11 March 1892) - No mapping

**Missing**: 4 items

**Action**: Convert analysis recommendations to formal mapping entries

**Estimated effort**: 1 hour

---

## Category 3: Consolidation Decision Implications (PHASE 2.2)

Items affected by taxonomy consolidation decisions that may need retagging.

### 3.1 Known Consolidations Requiring Item Updates

From planning/consolidation-decisions.md (24 sections):

**Examples needing investigation:**
1. "Drinking" → "Drinking (alcohol)" - Check if old tag still on items
2. Lodges terminology changes - Check for variant names
3. Schools of Arts consolidation - Check for recursive nesting
4. Military terminology - Check for variants
5. Sports hierarchy changes - Check for category tags
6. Hotels/Public houses disambiguation - Check usage
7. Singular generic removals - Check if items tagged with removed nodes

**Action required**: Systematic review of all 24 consolidation sections

**Estimated items affected**: 50-100 (unknown until audit complete)

**Estimated effort**: 6-8 hours

---

## Category 4: Pattern-Based Transformations (PHASE 3.2)

### 4.1 All Plural Parent Tags

**Pattern**: Any current Zotero tag matching a plural parent node name needs mapping to singular leaf

**Known examples**:
- Hotels → Hotel
- Schools → School
- Churches → Church
- Retailers and Stores → Retailer or Store
- Mining companies → mining company (generic) OR specific company name

**Action required**: Generate comprehensive list of all parent nodes from taxonomy, cross-reference against current Zotero tags

**Estimated items**: 100-150

**Estimated effort**: 2-3 hours (mostly automated once pattern identified)

---

## Category 5: Synonym Consolidations (PHASE 3.1)

### 5.1 Variant Tags to Preferred Terms

Tags in current Zotero that are marked as synonyms or merges in taxonomy need mapping entries.

**Examples**:
- "Colliery" → "coal mine"
- "Pubs" → "Public houses"
- Various spelling/capitalization variants

**Action required**: Extract all synonym/merge entries from taxonomy, check which are in current Zotero tags

**Estimated items**: 50-80

**Estimated effort**: 2-3 hours

---

## Consolidated Priority List

### CRITICAL (Must Complete Before Deployment)

1. **Hotels parent tag** (62 items) - 4-6 hours
2. **Mining parent tag** (32 items) - 3-4 hours
3. **Accommodation remaining** (1 item) - 15 minutes
4. **Pattern-based plural parents** (100-150 items) - 2-3 hours

**Critical subtotal**: ~200 items, ~10-14 hours

---

### HIGH (Should Complete for Quality)

1. **Undecided orphaned tags** (26 items) - 2-3 hours
2. **Consolidation implications** (50-100 items) - 6-8 hours
3. **Family hotels** (4 items) - 1 hour

**High subtotal**: ~80-130 items, ~9-12 hours

---

### MEDIUM (Nice to Have)

1. **Synonym consolidations** (50-80 items) - 2-3 hours
2. **Additional report-based decisions** - TBD after audit

**Medium subtotal**: ~50-80 items, ~2-3 hours

---

## Total Estimate

**Items needing mapping**: 330-410 (matches 315 unmapped items found + some already mapped items may need updates)

**Total effort**: 21-29 hours of work

---

## Recommended Approach

### Phase 2A: Complete Critical Parent Node Mappings

**Focus**: Hotels, Mining, pattern-based plurals

**Why first**: These violate core leaf-node pattern, highest risk of query expansion failure

**Output**: ~200 mapping entries

---

### Phase 2B: Complete High Priority Mappings

**Focus**: Orphaned tags, consolidation implications, family hotels

**Why second**: Known decisions, just need entry creation

**Output**: ~80-130 mapping entries

---

### Phase 2C: Build Validation Scripts (Phase 5)

**Before continuing with medium priority**: Build dry run and validation scripts to:
1. Auto-detect remaining parent node usage
2. Auto-generate pattern-based mappings where possible
3. Validate no tags will be lost

**Why pause here**: Validation scripts will catch anything we missed and auto-generate many entries

---

### Phase 2D: Complete Medium Priority + Refinement

**Focus**: Synonym consolidations, validation findings, iterative refinement

**Output**: Final ~50-80 entries + any validation discoveries

---

## Next Steps (Immediate)

### Step 1: Extract All Parent Nodes from Taxonomy

Create script to:
- Parse tag_map_consolidated.csv
- Identify all nodes with children (parent nodes)
- Cross-reference against current Zotero tags
- Generate list of items using parent nodes

**Output**: parent_node_violations.csv

---

### Step 2: Hotels Mapping Strategy Decision

**Question for user**: For the 62 items tagged "Hotels", what's the strategy?

**Option A**: Manual context review (slow but accurate)
- Review each item's full text
- Identify if specific hotel named
- Create specific mapping entry

**Option B**: Default to generic (fast but less precise)
- All "Hotels" → "Hotel" (generic leaf)
- Accept loss of specificity for items that mention specific hotels

**Option C**: Hybrid
- Quick scan for obvious hotel names in titles/snippets
- Default to generic for unclear cases

---

### Step 3: Create Batch Mapping Templates

For patterns like:
- Druid's Lodge (4 items): template ready
- Colliery (4 items): template ready
- Girls' cricket (2 items): template ready

Create CSV templates that can be filled in quickly.

---

## Files Generated This Session

1. ✅ reports/alcohol_reconciliation_analysis.md - Alcohol decisions reconciled
2. ✅ reports/undecided_tags_status.md - Orphaned tags status
3. ✅ reports/CONSOLIDATED_MISSING_MAPPINGS.md - This file

---

## Questions for User

1. **Hotels strategy**: Manual review, default to generic, or hybrid?

2. **Priority order**: Start with critical parent nodes, or do all orphaned tags first?

3. **Automation tolerance**: Comfortable with automated pattern-based mappings for clear cases (plural→singular)?

4. **Effort threshold**: How many hours should we invest in manual context review vs accepting some loss of specificity?

5. **Validation timing**: Build validation scripts now (Phase 5) before completing all mappings, or after?

---

