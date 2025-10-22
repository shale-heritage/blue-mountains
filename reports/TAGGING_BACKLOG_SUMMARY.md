# Tagging Backlog Summary

**Purpose:** Track all pending tag consolidation and application work
**Last Updated:** 2025-10-22
**Status:** 89+ items ready for manual application in Zotero

---

## Quick Stats

| Category | Items | Status |
|----------|-------|--------|
| **Ready to apply** | **25** | Reviewed & approved |
| **Awaiting review** | **64** | Report generated |
| **Hierarchy issues** | **2** | User identified |
| **Deferred tags** | **1** | Analysis needed |
| **Total items affected** | **89+** | Manual work required |

---

## Section 1: Ready to Apply in Zotero (25 items)

These items have been reviewed and approved. Apply changes manually using the action plans.

### A. Hotel Licensing Tags (13 items)

**Report:** `reports/hotel_licensing_action_plan.md`
**Status:** ✅ User reviewed and approved all decisions

**Items to tag:**
- 6 items → Add 'Hotel licensing' only
- 7 items → Add 'Publican's licensing' only
- 3 items → Add BOTH tags

**Quick reference:**

| Item # | Title | Date | Hotel Licensing | Publican's Licensing |
|--------|-------|------|-----------------|---------------------|
| 4 | Mountain Mixtures | 7 July 1893 | ✓ | ✓ |
| 13 | Megalong Valley | 6 October 1893 | | ✓ |
| 14 | Katoomba Police Court | 21 September 1894 | | ✓ |
| 15 | Granted | 26 March 1892 | ✓ | |
| 22 | Mountain Mixtures | 29 April 1892 | ✓ | |
| 37 | Notice of Application... | 19 June 1896 | | ✓ |
| 41 | Mountain Mixtures | 14 July 1893 | | ✓ |
| 42 | Licensing | 7 July 1893 | | ✓ |
| 43 | Local and General | 8 July 1893 | ✓ | ✓ |
| 44 | Katoomba Court | 16 June 1893 | ✓ | ✓ |
| 48 | Licensing | 1 October 1892 | | ✓ |
| 61 | Megalong Valley | 27 October 1893 | ✓ | |
| 63 | Notice of Application... | 9 June 1893 | | ✓ |

**Application workflow:**
1. Open each item in Zotero
2. Add specified tag(s) - both hierarchies already exist in `poly_hierarchy_additions.csv`
3. Check off in action plan when complete

**Estimated time:** ~30 minutes (2-3 minutes per item)

---

### B. Alcohol Tags (12 items)

**Report:** `reports/alcohol_rationalisation_report.md`
**Status:** ✅ User reviewed and approved all 12 items

**Changes approved:**
- Remove generic "Alcohol" tag from all 12 items
- Add specific tags based on context:
  - Activities: Drinking (alcohol), Liquor trade, Liquor licensing
  - Materials: Beer, Wine, Spirits (Whisky, Rum, Brandy, Gin), Grog
  - Events: Drunkenness (criminal), Unlicensed sales, Serving alcohol to minors
  - Agents: Publicans, Liquor merchants, Hotelliers, Shipwright
  - Associated Concepts: Drunkenness (intoxication) - physical condition

**Sample items:**

| # | Title | Date | Remove | Add |
|---|-------|------|--------|-----|
| 1 | A Charge of Rape | 6 Sept 1890 | Alcohol | Drinking (alcohol), Rum, Grog, Sexual assault, Carrington Hotel |
| 2 | Mountain Mixtures | 29 April 1892 | Alcohol | Drunkenness (both types), Beer, Liquor trade, Lithgow |
| 7 | Katoomba Court | 14 Oct 1892 | Alcohol | Liquor licensing, Unlicensed sales, Whisky, Nellie's Glen |
| 8 | Katoomba Police Court | 21 March 1891 | Alcohol | Liquor licensing, Serving alcohol to minors, Whisky, Adolescents |
| 11 | Megalong Valley | 18 Aug 1893 | Alcohol | Liquor trade, Mr Wilkinson, Megalong Valley |

**Note:** All 12 items detailed in full report with exact tags and rationale

**Application workflow:**
1. Open report: `reports/alcohol_rationalisation_report.md`
2. For each item:
   - Locate in Zotero by title and date
   - Remove "Alcohol" tag
   - Add all specified new tags (listed in "Proposed Tags" for each item)
3. Track progress in report

**Estimated time:** ~1-2 hours (5-10 minutes per item, some have 6-8 new tags)

---

## Section 2: Awaiting User Review (64 items)

Report generated but needs user approval before application.

### C. Accommodation Tag Rationalisation (64 items)

**Report:** `reports/accommodation_rationalization_report.md`
**Status:** ⏳ Report generated, awaiting user review

**Issue:** Generic "Accommodation" tag applied to 64 items needs replacement with specific tags

**Proposed changes:**
- Replace "Accommodation" with specific tags based on context:
  - **Occupations:** Hotelliers, Publicans, Boarding house keepers
  - **Buildings:** Hotels, Boarding houses, Cottages, Stables
  - **Specific establishments:** Carrington Hotel, Megalong Hotel, etc.
  - **Commercial activities:** Liquor trade, Coach and buggy business

**Breakdown:**
- Hotels/Hotelliers: ~40 items
- Boarding houses: ~5 items
- Stables/Cottages: ~3 items
- Occupations only: ~16 items

**Special cases:**
- Item #24: Blue Mountains Railway Tourist Guide - needs full-text review
- Item #30: A Public Meeting - needs full-text review
- Item #48: Testimonial to a Mine Manager - needs full-text review

**Next steps:**
1. Read report: `reports/accommodation_rationalization_report.md`
2. Review each item's proposed tags
3. Approve or modify recommendations
4. Apply changes manually in Zotero

**Estimated review time:** 2-3 hours
**Estimated application time:** 2-3 hours
**Total:** ~4-6 hours

---

## Section 3: Taxonomy Issues to Fix (2 issues)

User-identified problems in current hierarchy structure.

### D. Merge "Mining settlements" → "Mining districts"

**Issue:** Two similar categories exist
**Action:** Consolidate into single category
**Affected tags:** Unknown (need to grep CSV files)
**Priority:** Medium
**Status:** Not started

**Steps:**
1. Search `poly_hierarchy_additions.csv` for both terms
2. Decide preferred term (likely "Mining districts" - more generic)
3. Update `scripts/22_generate_poly_hierarchy.py`
4. Regenerate CSV
5. Update any affected items in Zotero

---

### E. Merge/Rename "Hospitality venues"

**Issue:** Naming inconsistency with "Accommodation buildings"
**Proposed solution:** Merge or rename to "Accommodation and Hospitality buildings"?
**Affected tags:** Hotels, Boarding houses, Pubs, etc.
**Priority:** Medium
**Status:** Not started

**Discussion needed:**
- "Hospitality venues" = modern term (hotels, restaurants, pubs)
- "Accommodation buildings" = broader term (includes cottages, boarding houses)
- Should they be merged or kept separate?
- If merged, what should the combined term be?

**Steps:**
1. Decide on terminology
2. Review all children of both categories
3. Update `scripts/22_generate_poly_hierarchy.py`
4. Regenerate CSV
5. Update visualisations

---

## Section 4: Deferred Analysis (1 tag)

Tags that need analysis reports before application.

### F. Post Tag Disambiguation (9 items)

**Issue:** "Post" tag is ambiguous
- Could mean: Post office (building)
- Could mean: Postal services (activity)
- Could mean: Both

**Status:** Deferred - needs context analysis
**Priority:** Low-Medium

**Next steps:**
1. Create script `scripts/35_analyse_post_tag.py` (similar to alcohol/accommodation analyses)
2. Generate report with KWIC snippets
3. User reviews and approves classifications
4. Apply changes manually

**Estimated analysis time:** 1 hour
**Estimated review time:** 30 minutes
**Estimated application time:** 30 minutes

---

## Section 5: Phase 2 Work (Future)

Larger structural improvements deferred to later phase.

### G. Pattern A Standardisation

**Issue:** Inconsistent hierarchy patterns
- **Pattern A (correct):** Hotels > Hotel > Carrington Hotel (Plural > Singular > Specific)
- **Pattern B (current):** Clergy > Cardinal Moran (Plural > Specific - missing intermediate)

**Affected categories:**
- Clergy → need to add "Clergyman" intermediate
- Medical professionals → need to add "Medical professional" intermediate
- Law enforcement → need to add "Police officer" intermediate
- Possibly 3-6 more categories

**Estimated scope:** ~200+ tags affected
**Priority:** Medium (improves consistency, not urgent)
**Status:** Deferred to Phase 2

**Benefits:**
- Consistent structure across all facets
- Better browsing in Zotero
- Clearer semantic relationships
- Easier to maintain

**Steps:**
1. Audit all plural parent categories across 7 primary facets
2. Identify Pattern B categories
3. Add singular intermediates to `scripts/22_generate_poly_hierarchy.py`
4. Regenerate `poly_hierarchy_additions.csv`
5. Regenerate visualisations
6. Test and validate
7. Apply to Zotero (if using manual workflow)

---

## Section 6: Infrastructure Work (Critical)

Foundational tasks that support all other work.

### H. Merge CSV Files ⚠️

**Issue:** Two CSV files exist with overlapping but different content
- `tag_consolidation_map.csv` (996 lines) - legacy file
- `poly_hierarchy_additions.csv` (667 lines) - current active file

**Status:** NOT MERGED - critical blocker
**Priority:** **HIGH** ⚠️

**Problems this creates:**
- Confusion about which file is authoritative
- Risk of losing work from legacy file
- Can't create single source of truth
- Harder to apply changes to Zotero

**Steps:**
1. **Assess overlap:**
   ```bash
   # Find tags in both files
   cut -d',' -f1 data/tag_consolidation_map.csv | sort > /tmp/old.txt
   cut -d',' -f1 data/poly_hierarchy_additions.csv | sort > /tmp/new.txt
   comm -12 /tmp/old.txt /tmp/new.txt  # Common to both
   comm -23 /tmp/old.txt /tmp/new.txt  # Only in old
   comm -13 /tmp/old.txt /tmp/new.txt  # Only in new
   ```

2. **Identify conflicts:**
   - Same tag with different parents in each file
   - Same tag with different actions (hierarchy vs synonym)
   - Decide which to keep

3. **Merge strategy:**
   - Use `poly_hierarchy_additions.csv` as base (has facet structure)
   - Add missing entries from `tag_consolidation_map.csv`
   - Resolve conflicts (prefer newer poly_hierarchy decisions)
   - Rename old file to `tag_consolidation_map.csv.deprecated`

4. **Validate merge:**
   - Check all tags from old file are represented
   - No duplicate rows
   - All parent references valid
   - Regenerate visualisations to confirm

**Estimated time:** 2-3 hours

---

### I. Create Application Automation (Optional)

**Issue:** All changes must be applied manually (time-consuming, error-prone)
**Solution:** Develop read-write scripts to automate application
**Priority:** Medium (saves time, but requires development)
**Status:** Not started (Phase 4)

**Requirements:**
1. Read-write Zotero API key
2. New script: `scripts/34_apply_tag_changes.py`
3. Testing framework (don't break the library!)
4. Rollback mechanism
5. Progress tracking (resume if interrupted)
6. Dry-run mode (preview before applying)

**Benefits:**
- Apply 100+ tag changes in minutes instead of hours
- Consistent application (no manual errors)
- Repeatable (can re-run if needed)
- Faster iteration on taxonomy design

**Risks:**
- Accidental damage to Zotero library
- Hard to reverse bulk changes
- API rate limiting issues
- Bugs in application logic

**Estimated development time:** 8-12 hours
**Recommended?** Yes, if more bulk changes expected

---

## Prioritised Action Plan

### Phase 1: Critical Infrastructure (Week 1)

1. ⚠️ **Merge CSV files** (HIGH PRIORITY)
   - Time: 2-3 hours
   - Deliverable: Single `tag_consolidation_map.csv` file

2. **Fix taxonomy issues**
   - Mining settlements → Mining districts merge (1 hour)
   - Hospitality venues decision (1 hour discussion + 1 hour implementation)

### Phase 2: Apply Ready Items (Week 2)

3. **Apply hotel licensing tags** (25 items)
   - Time: 30 minutes
   - Use: `reports/hotel_licensing_action_plan.md`

4. **Apply alcohol tags** (12 items)
   - Time: 1-2 hours
   - Use: `reports/alcohol_rationalisation_report.md`

### Phase 3: Complete Pending Analyses (Week 3)

5. **Review accommodation report** (64 items)
   - Review time: 2-3 hours
   - Application time: 2-3 hours
   - Use: `reports/accommodation_rationalization_report.md`

6. **Post tag analysis** (9 items)
   - Analysis: 1 hour
   - Review: 30 minutes
   - Application: 30 minutes

### Phase 4: Automation & Pattern A (Future)

7. **Optional: Develop application automation**
   - Time: 8-12 hours development
   - Benefit: Saves time on future bulk changes

8. **Optional: Pattern A standardisation**
   - Time: 4-6 hours
   - Benefit: Improved consistency

---

## Total Time Estimates

**Minimum (infrastructure + ready items):**
- Infrastructure: 4-5 hours
- Ready items application: 1.5-2.5 hours
- **Total: 5.5-7.5 hours**

**Medium (add pending analyses):**
- Above + accommodation + post analysis
- Additional: 5-7 hours
- **Total: 10.5-14.5 hours**

**Maximum (complete all work):**
- Above + automation + Pattern A
- Additional: 12-18 hours
- **Total: 22.5-32.5 hours**

---

## Recommended Approach

**Option A: Minimum Viable (Quick Wins)**
1. Merge CSV files (critical)
2. Apply ready items (37 items)
3. Stop here, assess

**Option B: Comprehensive (Complete Phase 1.2)**
1. All of Option A
2. Fix taxonomy issues
3. Review and apply accommodation tags
4. Analyse and apply post tags
5. Complete Phase 1.2 work

**Option C: Full Automation (Best for long-term)**
1. All of Option B
2. Develop application automation
3. Use automation for Pattern A standardisation
4. Use automation for future bulk changes

**Recommendation:** Start with Option A (7-8 hours work), assess results, then decide whether to continue with Option B or C.

---

## Questions?

- **What should I work on first?** Merge CSV files (Section 6H) - critical blocker
- **How much manual work is there?** 89+ items need manual review/application
- **Can this be automated?** Yes, but requires development (Section 6I)
- **What's the quickest win?** Apply 25 ready items (Sections 1A & 1B) - 1.5-2.5 hours

---

## See Also

- **docs/TAG_APPLICATION_WORKFLOW.md:** Complete explanation of how changes are tracked and applied
- **docs/api-integration.md:** Zotero API and automation possibilities
- **reports/hotel_licensing_action_plan.md:** Ready-to-apply example
- **SESSION_HANDOVER.md:** Latest session status and context
