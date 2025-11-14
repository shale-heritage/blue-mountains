# Session Handover: Entity Classification Workflow - Schools of Arts Complete

**Date:** 2025-11-13
**Session:** Dual-nature entity classification for full library tagging preparation
**Status:** Schools of Arts classification complete (18 items), ready to continue with boarding houses

---

## What We Accomplished

### 1. Entity Classification Audit ✓

Created comprehensive audit of all dual-nature entities in taxonomy (`entity-tagging-system/dual-nature-entity-audit.md`):

**Complete with validation:**
- ✅ **Churches** (17 entities) - Manual classification done, uses (building)/(organisation) qualifiers
- ✅ **Hotels** (8 entities) - Phase 6 complete, 49 tag applications ready for 37 items
- ✅ **Schools of Arts** (2 entities) - NLU classification complete (18 mentions classified)

**Taxonomy exists, needs validation:**
- **Boarding houses** - Structure exists with (building)/(business) qualifiers, needs NLU workflow
- **Educational schools** - Not yet investigated

**Clarified approach:**
- **Halls/Lodges** - Intentionally separate (halls = buildings, lodges = organisations), use intrinsic naming distinction

### 2. Taxonomy Naming Guideline Added ✓

Updated entity-classifier skill (`~/.claude/skills/entity-classifier/skill.md`) with principle:

**Use intrinsic naming distinction when possible:**
- "Halls" (buildings) vs "Lodges" (organisations) - Different words distinguish concepts
- Only use parenthetical qualifiers when same name needs disambiguation (e.g., "Methodist Church (building)" vs "Methodist Church (organisation)")

### 3. Schools of Arts Classification Complete ✓

**Method:** NLU classification with entity-classifier skill
**Results:** 18 mentions classified across Katoomba School of Arts and generic School of Arts

**Initial classification:**
- Building only: 5 mentions
- Organisation only: 10 mentions
- Both: 3 mentions

**After user corrections:**
- Building only: 3 mentions (16.7%)
- Organisation only: 10 mentions (55.6%)
- Both: 5 mentions (27.8%)

**Accuracy:** 17/18 (94.4%) - 1 error corrected, 2 judgement call refinements

**User feedback applied:**
1. ✅ **Mention 4** (billiard table revenue): `building` → `both` - Financial returns = agency
2. ✅ **Mention 6** (reading-room literature): `building` → `both` - Collection management = organisational
3. ✅ **Mention 13** (meeting at residence): `both` → `organisation` - ERROR: Meeting not held AT School of Arts

**Key learning:** Always verify locative phrases ("at", "in") actually refer to the entity being classified, not other locations.

---

## Current State

### Files Created/Modified

**New files:**
- `entity-tagging-system/dual-nature-entity-audit.md` - Complete audit of dual-nature entities
- `data/entity_classification/schools_mentions.json` - 18 Schools of Arts mentions with context
- `data/entity_classification/schools_classification_prompt.txt` - Classification prompt used

**Modified files:**
- `~/.claude/skills/entity-classifier/skill.md` - Added intrinsic vs parenthetical disambiguation guideline

**Hotels (already complete):**
- `entity-tagging-system/outputs/hotels/item_tag_application.csv` - 49 applications ready
- All Phase 1-6 documentation complete

### Entity Classification Status

| Entity Type | Mentions | Classification Status | Next Step |
|-------------|----------|----------------------|-----------|
| Hotels | 43 items | ✅ Phase 6 complete | Ready to apply |
| Churches | TBD | ✅ Manual complete | 5-item spot-check |
| Schools of Arts | 18 | ✅ NLU complete | Generate application CSV |
| Halls/Lodges | TBD | ✅ Intentionally separate | 5-item spot-check |
| Boarding houses | TBD | ⏳ Next: Extract mentions | Run NLU workflow |
| Educational schools | TBD | ⏳ Not yet searched | Search then classify if needed |

---

## Next Steps (Priority Order)

### Immediate: Continue Entity Classification

**1. Boarding Houses (next in queue)**
```bash
source venv/bin/activate
python scripts/38_classify_entities_with_claude.py --entity-type "boarding-houses" --interactive
```
Expected: Similar to hotels workflow (accommodation + business aspects)

**2. Educational Schools**
- Search taxonomy for school-related tags
- If found without dual-nature structure, run NLU workflow
- May need to add entity type to script 38

**3. Generate Application CSVs**
- Schools of Arts: Create item_tag_application.csv (like hotels Phase 6)
- Boarding houses: After classification complete
- Combine all entity types for full library tagging

**4. Spot-Check Validations (5 items each)**
- Churches: Verify manual classifications
- Halls/Lodges: Confirm separation approach is working

### Before Full Library Tagging

From `planning/TODO.md` and analysis:

**Required:**
- ✅ Hotels classification (DONE)
- ✅ Churches classification (DONE - manual)
- ✅ Schools of Arts classification (DONE - NLU)
- ⏳ Boarding houses classification (IN PROGRESS)
- ⏳ Educational schools classification (TBD)
- ⏳ Spot-checks for churches, halls (5 each)
- ❌ Dual-nature entity strategy decision (DEFERRED - TODO.md:42-140)
- ❌ Phase 1.2.2: Tag definitions/scope notes (NOT STARTED - 2-3 weeks)
- ❌ Phase 1.3: Getty AAT mapping (NOT STARTED - 3-4 weeks)
- ❌ Phase 1.4 prep: Backup strategy (NOT STARTED - 2 hours)

**Strategic decision needed:** Polyhierarchy (current) vs disambiguation approach
- Schools of Arts currently use polyhierarchy (same tag in both facets)
- Churches/hotels use disambiguation qualifiers
- Decision affects all future entity work

**Timeline estimates:**
- Complete entity classification: 1-2 weeks
- Full Phase 1 completion for library tagging: 6-8 weeks
- OR incremental application: Apply entities as completed (2-3 weeks to first batch)

---

## Key Decisions Made

1. **Halls vs Lodges separation confirmed** - Intrinsic naming distinction, not dual-nature with qualifiers
2. **Spot-check quantity: 5 items** - Sufficient for validation given strong hotels performance
3. **Priority order: Schools of Arts → Boarding houses → Educational schools** - Logical sequence
4. **Naming guideline formalized** - Prefer intrinsic distinction, fall back to parenthetical qualifiers

---

## Entity Classification Learnings

### Indicators to Strengthen

**Financial returns from physical assets = both tags:**
- "Revenue from billiard table" = agency (earning income) + building (physical asset)
- Strengthen `financial_returns` as organisation indicator

**Collection management = organisational activity:**
- "Literature on reading-room table" = organisational curation, even via physical space
- Add `collection_management` as organisation indicator

### Critical Error to Avoid

**Locative phrase verification:**
- ❌ "Meeting held at Mr Edwards' residence" ≠ meeting held AT School of Arts
- ✅ Always verify "at/in/near [X]" actually refers to the entity being classified
- Add explicit check: "Does this locative phrase refer to the entity or another location?"

### Classification Patterns Observed

**Schools of Arts usage:**
- Predominantly organisational (55.6%) - committees, subscriptions, management
- Building references via physical spaces - reading room, library, billiard room
- Mixed contexts (27.8%) - committee meetings held in the reading room

**Comparable to hotels:**
- Hotels: More building-heavy (many locational references)
- Schools of Arts: More organisation-heavy (membership societies)
- Both: "Both" classification increased after user corrections (nuanced cases)

---

## Quality Metrics

### Schools of Arts Classification

**Accuracy:** 94.4% (17/18 mentions)
- 1 clear error (locative phrase misread)
- 2 judgement call refinements (defensible either way)
- 15 correct on first pass

**User feedback:** "Your tagging was quite good, with one error and two judgement call differences"

**Improvement from hotels:** Applied hotels learnings, maintained high accuracy

---

## Commands Reference

### Extract Entity Mentions
```bash
source venv/bin/activate
python scripts/38_classify_entities_with_claude.py --entity-type <type> --interactive
# Supported: hotels, churches, schools, halls
```

### Review Taxonomy Structure
```bash
grep "School of Arts\|Schools of Arts" data/tag_map_consolidated.csv
grep "Boarding house\|boarding house" data/tag_map_consolidated.csv
```

### Current Taxonomy Stats
- Total rows: 1,391 unique tags
- Churches: 83 unique tags (24 building, 24 organisation, 17 entities with both)
- Hotels: 19 unique tags (10 building, 9 business, 8 entities with both)
- Schools of Arts: Uses polyhierarchy (same tag in Cultural societies + Halls facets)

---

## For Next Session

**Immediate action:** Continue with boarding houses classification

**Script ready:** `scripts/38_classify_entities_with_claude.py`

**Expected entities:** Check what boarding house names are in taxonomy:
- Orama Boarding House (has both building + business tags)
- Generic "Boarding house" (has both variants)
- Others TBD from Zotero extraction

**Apply learnings:**
1. Verify all locative phrases refer to the entity being classified
2. Financial returns from assets = both tags
3. Collection/facility management = organisational activity

**Note:** Script 38 may need boarding house entity names added to `entity_names` dict if "boarding-houses" isn't already configured.

---

## Session Context

**User goal:** Complete dual-nature entity classification for ALL entity types before applying tags to full Zotero library.

**Progress:** 3 of ~6-7 entity types complete (hotels, churches, Schools of Arts)

**Next:** Boarding houses, educational schools, spot-checks, then generate combined application CSVs

**Decision pending:** Polyhierarchy vs disambiguation strategy (affects all future work)

---

**Session completed:** 2025-11-13
**Next session start point:** Boarding houses extraction and classification
**Status:** On track, high classification quality maintained
