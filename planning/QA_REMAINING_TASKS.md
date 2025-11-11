# QA Remaining Tasks - To Resume After Restart

**Date Created:** 2025-11-09
**Session:** Post-QA Integrity Check
**Priority:** Complete before Zotero retagging

---

## Quick Status Summary

✅ **Phase 1 Complete:** Critical data quality issues fixed (US spelling, case variations, capitalisation)

⚠️ **Remaining Work:** 3 categories of issues requiring completion

---

## Task 1: Fix Remaining 28 Orphaned Tags in Mappings ✅ COMPLETE

**Priority:** HIGH (blocks retagging)
**Estimated Time:** 30-45 minutes (ACTUAL: 45 minutes)
**File:** `data/tag_application_mapping.csv`
**Completed:** 2025-11-11

### What Was Done
Fixed all 28 orphaned tags through comprehensive script that handled:
- Spelling corrections (organization → organisation)
- Case corrections (Whisky → whisky)
- Context-specific building tag replacements
- Person name consolidations
- New taxonomy additions (sanatorium hierarchy, Courts of Petty Sessions, inquests)
- Synonym mappings for all variants

**Result:** ✓ All mapping tags now exist in taxonomy (validation passed)

### Orphaned Tags List (with usage counts)

```text
5x  building          → Should be "buildings" or specific type
4x  Whisky            → Should be lowercase "whisky"
4x  Police Court      → Needs adding to taxonomy OR map to existing
4x  St Hilda's Church of England (organization) → Fix to (organisation)
2x  Constable John Illingworth → Needs adding to taxonomy as agent
2x  Katoomba Congregational Church (organization) → Fix to (organisation)
2x  Methodist Church (organization) → Fix to (organisation)
2x  church (organization) → Fix to (organisation)
1x  sexual assault    → Check if exists, may need lowercase
1x  inquest           → Check if exists (vs "inquests")
1x  Mr J. Hudson      → Needs adding to taxonomy as agent
1x  Joseph Nimmo      → Needs adding to taxonomy as agent
1x  Hotel licensing Please → Remove (malformed)
1x  [name of hotellier] → Remove (placeholder)
1x  Hotel (not only here but in all instances) → Remove (malformed)
1x  Mt Victoria Hotel → Check if exists or map to existing
1x  N.S.W. Mounted Rifles → Needs adding to taxonomy
1x  Senior-constable Tomkins → Needs adding to taxonomy as agent
1x  Ruined Castle     → Check vs "Ruined Castle mining district"
1x  Waverley Friary (organization) → Fix to (organisation)
1x  St Canice's Catholic Church Katoomba (organization) → Fix to (organisation)
1x  Roman Catholic Church Mount Victoria (organization) → Fix to (organisation)
1x  Roman Catholic Church (organization) → Fix to (organisation)
1x  Presbyterian church (organization) → Fix to (organisation)
1x  St Clement's Church of England Yass (organization) → Fix to (organisation)
1x  St Mark's Church of England Darling Point (organization) → Fix to (organisation)
1x  St Andrew's Cathedral Church of England Sydney (organization) → Fix to (organisation)
1x  Wesleyan Church (organization) → Fix to (organisation)
```

### Action Required

**Option A - Claude Code can do this:**
Run automated fix script to:
- Replace all (organization) → (organisation) in mappings
- Fix Whisky → whisky
- Fix building → buildings
- Remove malformed/placeholder entries
- Flag remaining person names/entities for manual addition to taxonomy

**Option B - Manual:**
Edit `data/tag_application_mapping.csv` directly with find-replace

### Command to Resume
```bash
# Claude Code: create and run script to fix remaining orphaned tags
# Focus on bulk spelling fixes, flag entities needing taxonomy additions
```

---

## Task 2: Review 10 Incomplete Disambiguations

**Priority:** MEDIUM (decision required)
**Estimated Time:** 1-2 hours
**File:** `reports/incomplete_disambiguations_review.md` (review guide created)

### What's Wrong
Some entities have both qualified and unqualified versions:
- `Church of England Katoomba` (unqualified)
- `Church of England Katoomba (organisation)` (qualified)
- `Church of England Katoomba (building)` (qualified)

This creates ambiguity - which should users apply?

### 10 Cases Requiring Review

1. Church of England Katoomba
2. Methodist Church Katoomba
3. Presbyterian Church Leura
4. Presbyterian Church Wentworth Falls
5. Roman Catholic Church Blackheath
6. Roman Catholic Church Lawson
7. Roman Catholic Church Megalong
8. Roman Catholic Church Mount Victoria
9. Wesleyan Church Katoomba
10. Grand Hotel (vs Grand Hotel (Sydney))

### Decision Needed for Each

For each entity, review Zotero/Trove source context and decide:

- **Remove unqualified** - Force users to choose (building) or (organisation)
- **Convert to synonym** - Make unqualified point to most common qualified version
- **Keep as ambiguous** - Allow unqualified for cases where distinction unclear

### How to Review

1. Open `reports/incomplete_disambiguations_review.md`
2. For each entity, search Zotero for items tagged with unqualified version
3. Review full text to understand context (building vs organisation)
4. Document decision in the report
5. Apply changes to `data/tag_map_consolidated.csv` and `data/tag_application_mapping.csv`

### Command to Resume
```bash
# Open review report
cat reports/incomplete_disambiguations_review.md

# For each case, tell Claude Code your decision:
# "For Church of England Katoomba, convert unqualified to synonym pointing to (organisation)"
```

---

## Task 3: Resolve Parent-Leaf Pattern Violations

**Priority:** LOW (strategic decision, may defer)
**Estimated Time:** 2-4 hours if restructuring
**File:** Analysis in `reports/QA_SESSION_SUMMARY.md`

### What's Wrong

Some tags act as BOTH:
- Valid leaf nodes (used in tagging - correct)
- Parent nodes (have children - violates strict leaf-node pattern)

### Example: "death"

**Current structure:**
```
death (both tag AND parent)
├── death notice
└── suicide
```

**Strict leaf-node pattern would be:**
```
deaths (plural parent - never tagged)
├── death (singular generic - CAN be tagged)
├── death notice
└── suicide
```

### Affected Tags
- death
- hotel licensing
- liquor trade
- court cases
- railway
- mining
- Others...

### Decision Required

**Option A:** Restructure hierarchies
- Create plural parents above current parent-leaves
- Time-consuming but enforces pattern consistency
- May require updating many parent references

**Option B:** Accept current pattern
- Acknowledge these are valid polyhierarchical cases
- Document as acceptable exception to pattern
- No changes needed

**Option C:** Defer
- Mark as "future refactoring" task
- Doesn't block current retagging work
- Can revisit during Phase 1.3 (dual-nature entity handling)

### Recommendation
**DEFER** - This doesn't block retagging and relates to larger dual-nature entity strategy documented in `planning/TODO.md` lines 42-140.

### Command to Resume
```bash
# If choosing to restructure:
# "Claude Code: implement parent-leaf restructuring for tag 'death'"

# If accepting current pattern:
# "Claude Code: document parent-leaf violations as acceptable in taxonomy design docs"

# If deferring:
# "Claude Code: add parent-leaf restructuring to planning/TODO.md as future task"
```

---

## Task 4: Fix 2 Mappings with Data Loss Risk

**Priority:** LOW
**Estimated Time:** 15 minutes
**File:** `data/tag_application_mapping.csv`

### What's Wrong
5 mappings remove tags but don't add replacements (potential data loss).

### Affected Items
1. Blue Mountains Railway Tourist Guide
2. A Public Meeting.
3. Licensing.
4. Megalong Valley.
5. Megalong Matters.

### Action Required
Review each item and determine:
- Is removal intentional (tag was incorrect)?
- Should replacement tags be added?

### Command to Resume
```bash
# Tell Claude Code to:
# "Review the 5 mappings with removals but no additions and show me the context"
```

---

## Task 5: Re-run Validation

**Priority:** HIGH (after Tasks 1-2 complete)
**Estimated Time:** 5 minutes
**File:** `scripts/validate_taxonomy.py`

### Action Required
After completing Tasks 1 and 2, run validation to confirm all critical issues resolved.

### Command to Resume
```bash
python3 scripts/validate_taxonomy.py
```

### Success Criteria
- Zero orphaned tags in mappings
- Zero US spelling violations in data (notes OK)
- All parent references valid
- No unexpected errors

---

## Task 6: Regenerate Hierarchy Visualisations (Optional)

**Priority:** LOW
**Estimated Time:** 5-10 minutes

### Action Required
If any structural changes made to taxonomy, regenerate hierarchy visualisation files.

### Command to Resume
```bash
# Claude Code: identify and run hierarchy visualisation generation script
# Should update all 61 files in visualizations/hierarchy_trees/
```

---

## Task 7: Final Commit and Push

**Priority:** HIGH (after all tasks)
**Estimated Time:** 5 minutes

### Action Required
Commit all QA work with comprehensive message.

### Command to Resume
```bash
# Tell Claude Code:
# "Commit all QA work with descriptive message documenting fixes and remaining manual tasks"
```

---

## Recommended Order of Execution

### Session 1 (Quick wins - 30-45 min)
1. ✅ Task 1: Fix remaining orphaned tags (automated)
2. ✅ Task 4: Review 5 data loss mappings (quick check)
3. ✅ Task 5: Re-run validation
4. ✅ Task 7: Commit and push

### Session 2 (Manual review - 1-2 hours)
5. ⏸️ Task 2: Review 10 incomplete disambiguations (requires Trove context)
6. ⏸️ Task 5: Re-run validation again
7. ⏸️ Task 7: Commit disambiguation decisions

### Session 3 (Strategic decision - defer if needed)
8. ⏸️ Task 3: Decide on parent-leaf violations (or defer to Phase 1.3)

---

## Files to Reference

### Reports
- `reports/QA_SESSION_SUMMARY.md` - Complete session overview
- `reports/incomplete_disambiguations_review.md` - Disambiguation review guide
- `planning/QA_INTEGRITY_CHECKLIST.md` - Detailed progress checklist

### Scripts
- `scripts/validate_taxonomy.py` - Validation runner
- `scripts/temp_fix_orphaned_mapping_tags.py` - Partial orphan fix (can extend)

### Data (with backups)
- `data/tag_map_consolidated.csv` (1,463 rows, 5 backup versions)
- `data/tag_application_mapping.csv` (1,241 rows, 1 backup version)

---

## Quick Start Command for Next Session

```bash
# Review this file
cat planning/QA_REMAINING_TASKS.md

# Tell Claude Code:
"Let's resume the QA remaining tasks. Start with Task 1: fix the remaining 28 orphaned tags in mappings."
```

---

**Last Updated:** 2025-11-09
**Status:** Ready for resumption
