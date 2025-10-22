# Session Handover - Tag Consolidation Phase 1.2.1

**Date:** 2025-10-19
**Status:** In progress - Naming variants review

---

## CRITICAL: Family Name Protection Applied

**URGENT FIX COMPLETED:** Removed Peckman/Penman family merge
- **NO family or person names are merged without checking primary sources**
- Peckman vs Penman could be different families entirely
- All family names now require historian review with primary source verification

---

## Current Status Summary

### Completed (235 of 332 pairs - 70.8%)

| Category | Count | Status |
|----------|-------|--------|
| MERGE | 0 | **No merges without primary source verification** |
| HIERARCHY | 139 | ✅ Completed (105 initial + 34 automated) |
| KEEP_SEPARATE | 96 | ✅ Completed (83 person names + 13 false positives) |

### Remaining (98 pairs - 29.5%)

1. **CRITICAL: Peckman/Penman family** (1 pair) - Requires primary source check
2. **Naming Variants** (6 pairs) - Ready for review (report created)
3. **Family Name Relationships** (8 pairs) - Require historian judgment
4. **Mining Domain** (16 pairs) - Require domain expertise
5. **Contextual** (67 pairs) - Require Zotero item examination

---

## Files Updated This Session

### Core Decision Files
- `planning/phase1.2.1-consolidation-decisions.md` - Updated (0 merges, 139 hierarchies, 96 keep-separate, 98 flagged)
- `data/tag_consolidation_map.csv` - Updated (Peckman/Penman merge removed)

### Reports Created/Updated
- `reports/review_summary.md` - **Current state documented** with critical principle
- `reports/triage_report.md` - Automated triage of 144→98 flagged pairs
- `reports/naming_variants_review.md` - **NEW: Detailed analysis of 6 naming variants**
- `reports/consolidation_preview.md` - Updated previews

### Scripts Created
- `scripts/05_triage_flagged_pairs.py` - Pattern-based categorisation
- `scripts/06_apply_automated_decisions.py` - Applied 47 automated decisions
- `scripts/07_review_naming_variants.py` - Naming variant analysis (created but needs Zotero data structure adjustment)

---

## Automated Decisions Applied (47 pairs)

### False Positives → KEEP_SEPARATE (13)
Substring coincidences: Pub/Public meeting, Band/Husband family, Death/Debating, etc.

### Generic→Specific Hierarchies (34)
- **Hotels** (18): Hotels → Imperial Hotel, Carrington Hotel, etc.
- **Coal/Mining** (4): Coal → Gladstone Coal Company, etc.
- **Sports** (4): Cricket/Football/Tennis → specific clubs
- **Infrastructure** (4): Councils, Reserves, Roads → specific instances
- **Shale mines** (3): Shale mines → specific mine names
- **Other** (1): Accident → Mining accidents, Mining → Sunny Corner Mining Company

---

## Naming Variants Review - Ready for Decision

**Report location:** `reports/naming_variants_review.md`

### High Confidence ✅
**Druid's Lodge / Lodges → HIERARCHY (Lodges parent)**
- Can implement immediately

### Medium Confidence ⚠️
**Katoomba South / South Katoomba → MERGE to "South Katoomba"**
- Recommend spot-checking 1-2 items to confirm same location

**Coal/Mining hierarchies:**
- Katoomba Coal and Shale **Company** → **Mines** (HIERARCHY)
- Katoomba **coal mines** (generic) → **Coal and Shale Company** (specific) (HIERARCHY)

### Low Confidence ❓
**Katoomba Superior Public School / Katoomba Public School**
- Need to check dates on items (same school over time vs concurrent institutions)
- May require NSW education records

---

## Next Session Priority Tasks

### 1. Complete Naming Variants Review (5-10 mins)
- User to approve/modify 6 naming variant decisions from report
- Implement approved decisions

### 2. Review All 139 Hierarchies (User Requested)
Check hierarchies for usefulness and completeness - user specifically requested this

### 3. Family Name Relationships (10-15 mins)
Review 8 family name pairs:
- Default to KEEP_SEPARATE unless evidence of same family unit
- Pairs: Gordon/Brydon, Austin/Watkins, Evans/Eaton, etc.

### 4. Mining Domain Review (15-20 mins)
16 pairs requiring domain expertise:
- Miners vs Miners' families/dwellings
- Miners vs specific mines (9 pairs)
- Mine naming relationships

### 5. Contextual Review (25-35 mins)
67 remaining pairs requiring Zotero item examination

---

## Key Principles Established

### 1. Person/Family Name Protection
**NEVER merge without primary sources:**
- Person names: Different people (Mr D McKillop vs Mr G McKillop)
- Family names: Different family lines (Peckman vs Penman)
- Requires birth/death records, census data, or primary historical documents

### 2. Hierarchy Multi-Tagging
Items receive BOTH parent and child tags:
- Court → Police court (item gets both "Court" and "Police court")
- Hotels → Imperial Hotel (item gets both "Hotels" and "Imperial Hotel")

### 3. Conservative Approach
When uncertain → FLAG_REVIEW rather than guess

### 4. 80% Solution Goal
"Finished and consistent" over "perfect" - iterate later

---

## Project Context

**Goal:** Rationalise 332 similar tag pairs from Blue Mountains shale mining communities digital collection

**Approach:** Semi-automated with pattern matching + manual review for ambiguous cases

**Current Phase:** Phase 1.2.1 - Tag consolidation decision-making

**Next Phase:** Phase 1.4 - Apply consolidation to Zotero (optional, after decisions finalised)

---

## Technical Notes

### Environment Setup
- Automated setup: `./setup.sh` (creates venv, installs dependencies)
- Script wrapper: `./run.sh <script>` (auto-activates venv)
- Requires: `python3.12-venv` package on Ubuntu

### Data Files
- Raw tags: `data/raw_tags.json` (481 tags from 336 items)
- Similar pairs: `data/similar_tags.csv` (332 pairs)
- Consolidation map: `data/tag_consolidation_map.csv` (transformation rules)

### Linting
- All markdown/Python files must pass linting
- UK/Australian spelling required (CLAUDE.md project standards)
- MD022, MD031, MD032, MD040 rules enforced

---

## Quick Reference Commands

```bash
# Review current status
cat reports/review_summary.md

# Check naming variants analysis
cat reports/naming_variants_review.md

# View current decisions
cat planning/phase1.2.1-consolidation-decisions.md

# Count remaining work
grep "FLAGGED FOR REVIEW" planning/phase1.2.1-consolidation-decisions.md -A5
```

---

## Session End State

**Where we left off:** Just completed naming variants analysis report. User ready to review and make decisions on the 6 naming variant pairs.

**Immediate next step:** User to review `reports/naming_variants_review.md` and approve/modify proposed decisions for naming variants.

**Blocked items:** None - all automated work complete, waiting for historian decisions

**Time estimate for completion:** 55-80 minutes of manual review (excluding Peckman/Penman primary source research)
