# Blue Mountains Project - To-Do List

**Last Updated:** 2025-10-19
**Current Phase:** Phase 1.2 - Tag Schema Rationalisation

---

## ✅ COMPLETED

### Phase 1.1: Folksonomy Analysis & Documentation
- ✅ Extract all tags from Zotero (Script 01)
- ✅ Analyse tag patterns, frequencies, overlaps (Script 02)
- ✅ Generate comprehensive analysis reports
- ✅ Document folksonomy logic (`docs/folksonomy_logic.md` - 1,336 lines)
- ✅ FAIR4RS documentation complete (Phases A-E)
- ✅ Technical documentation complete (~16,200 lines)

### Phase 1.2.1: Tag Consolidation (Current)
- ✅ **ALL 421 pairs processed** (100% complete)
  - ✅ 2 MERGE decisions (naming variants)
  - ✅ 218 HIERARCHY decisions (parent-child relationships)
  - ✅ 218 KEEP_SEPARATE decisions (distinct concepts)
  - ✅ 0 FLAGGED (all triaged with evidence-based decisions)

### Recent Dual-Nature Analysis (Oct 19, 2025)
- ✅ Churches analysed (7 churches, 4 dual-nature, pattern recognition methodology)
- ✅ Councils analysed (already correctly separated - NOT dual-nature)
- ✅ Schools of Arts town-specific investigation (kept generic tag only)
- ✅ Civic buildings category created
- ✅ Religious organisations + Religious buildings subcategories created
- ✅ 18 new CSV rows added to taxonomy

### Scripts Created (21 total)
- ✅ Scripts 01-15: Core analysis and consolidation tools
- ✅ Scripts 16-18: Church and council dual-nature analysis
- ✅ Scripts 19-21: Schools of Arts town-specific investigation

---

## 🔄 IN PROGRESS

### Phase 1.2.2: Tag Definitions & Scope Notes
**Status:** Not started
**Priority:** HIGH

**Tasks:**
- [ ] Document definitions for all 481 unique tags
- [ ] Create scope notes explaining when to use each tag
- [ ] Clarify boundaries between similar concepts
- [ ] Document naming conventions applied
- [ ] Create controlled vocabulary documentation

**Dependencies:** Phase 1.2.1 complete ✅

**Deliverable:** `docs/tag-definitions.md` or similar

---

## 📋 PLANNED - PHASE 1

### Phase 1.3: Vocabulary Mapping & Publication
**Status:** Not started
**Priority:** HIGH (after Phase 1.2.2)

**Tasks:**
- [ ] Map rationalised tags → Getty Art & Architecture Thesaurus (AAT)
- [ ] Map geographic tags → Getty Thesaurus of Geographic Names (TGN)
- [ ] Create local gazetteer for places not in Getty TGN:
  - Ruined Castle (mining district)
  - Nellie's Glen (mining district)
  - Other local Blue Mountains place names
- [ ] Prepare SKOS-formatted vocabulary
- [ ] Publish controlled vocabulary to Research Vocabularies Australia (RVA)
- [ ] Document all mappings for interoperability

**Resources Available:**
- `docs/vocabularies.md` - Getty AAT, TGN, and RVA standards
- `docs/gazetteer-comparison.md` - Geographic vocabulary options

**Dependencies:** Phase 1.2.2 complete

**Deliverable:** Published vocabulary on RVA + mapping documentation

---

### Phase 1.4: Batch Update Zotero
**Status:** Not started
**Priority:** HIGH (after Phase 1.3)

**Tasks:**
- [ ] **CRITICAL:** Backup existing Zotero data before any updates
- [ ] Apply rationalised tags to existing 336 tagged items via Zotero API:
  - [ ] Apply merges (2 pairs)
  - [ ] Apply hierarchies (218 parent-child relationships)
  - [ ] Apply dual-nature multi-tagging (8 entities)
- [ ] Preserve original tags as backup:
  - Separate Zotero collection OR
  - CSV export of original state
- [ ] Validate all updates
- [ ] Generate update report showing changes made

**Resources Available:**
- `docs/api-integration.md` - Zotero API patterns and best practices
- `data/tag_consolidation_map.csv` - 438 rows of transformation rules

**Dependencies:** Phase 1.3 complete

**Deliverable:** Updated Zotero library + validation report

---

## 📋 PLANNED - PHASE 2

### Phase 2.1: Named Entity Recognition (NER)
**Status:** Not started
**Priority:** MEDIUM (after Phase 1 complete)

**Tasks:**
- [ ] Extract full text from 304 tagged primary source PDFs
- [ ] Run NER to extract:
  - [ ] Person names (all individuals, not just protagonists)
  - [ ] Place names (all geographic references)
  - [ ] Organisation names (companies, institutions)
  - [ ] Dates and temporal expressions
- [ ] Create comprehensive registers:
  - [ ] Person register with biographical links (ADB, genealogical databases)
  - [ ] Place name register with geospatial coordinates
  - [ ] Organisation/institution register
- [ ] Apply disambiguation approach for ambiguous person names
- [ ] Validate and enrich existing tags:
  - [ ] Compare NER results with current tags
  - [ ] Identify missing tags
  - [ ] Identify tag errors or inconsistencies
  - [ ] Expand abbreviated names using context

**Implementation Options:**
- **Option A:** Interactive analysis with Claude Code (human-in-the-loop)
- **Option B:** Automated batch processing with local LLM (up to 120B parameters)
- **Option C:** Hybrid approach (recommended) - automated batch + selective review

**Dependencies:** Phase 1.4 complete (rationalised tags applied)

---

### Phase 2.2: Tag Untagged Items
**Status:** Not started
**Priority:** MEDIUM

**Tasks:**
- [ ] Tag 853 currently untagged items using:
  - Rationalised controlled vocabulary from Phase 1
  - NER results from Phase 2.1
  - Human review for quality control

**Dependencies:** Phases 1.4 and 2.1 complete

---

## 📋 PLANNED - PHASE 3

### Phase 3.1: Archaeological & Artefact Tag Integration
**Status:** Not started
**Priority:** MEDIUM (after historical tags finalised)

**Tasks:**
- [ ] Align archaeological feature tags with rationalised historical vocabulary
- [ ] Verify artefact tags with artefact specialist (Penny Crook) for EAMC schema compliance
- [ ] Enrich archaeological and artefact tags with social theme associations
- [ ] Ensure cross-domain consistency while respecting specialist needs
- [ ] Map ~256 archaeological features from FAIMS Mobile to historical context

**Dependencies:** Phase 1.4 complete

---

### Phase 3.2: Australian Dictionary of Biography (ADB) Linking
**Status:** Not started
**Priority:** LOW

**Tasks:**
- [ ] Extract all person names from tags
- [ ] Search ADB online database for matches
- [ ] Record ADB persistent URLs for matched entries
- [ ] Add ADB links as metadata in Zotero person records

**Known ADB Entries:**
- North, John Britty (1831-1917) - Edgar 1974, ADB Volume 5
- [Additional entries to be identified]

**Dependencies:** Phase 2.1 complete (person register)

---

## 📋 FUTURE PHASES (Not Yet Scheduled)

### Phase 4: Omeka Classic Publication
- Migrate Zotero items → Omeka Classic via API
- Create collections and exhibits
- Configure CurateScape for mobile tours
- Deploy to shaleheritage.au

### Phase 5: Public Engagement
- Launch public digital collection
- Develop educational resources
- Engage local historical societies

---

## 🎯 IMMEDIATE NEXT STEPS

Based on project documents, the **most urgent tasks** are:

### 1. Phase 1.2.2: Tag Definitions (HIGH PRIORITY)
**Why:** Complete documentation of the rationalised vocabulary before mapping to external standards

**Estimated Effort:** Medium (2-3 weeks with domain expert consultation)

**Deliverable:** Comprehensive tag definitions document

---

### 2. Phase 1.3: Getty Mapping (HIGH PRIORITY)
**Why:** Required for interoperability and publication to Research Vocabularies Australia

**Estimated Effort:** Medium-High (3-4 weeks, requires research into Getty vocabularies)

**Deliverable:** Vocabulary mappings + local gazetteer

---

### 3. Phase 1.4: Apply to Zotero (HIGH PRIORITY)
**Why:** Changes documented in CSV need to be applied to actual library

**Estimated Effort:** Low-Medium (1-2 weeks, largely automated but requires careful validation)

**Critical Note:** ⚠️ **BACKUP REQUIRED** before any batch updates

**Deliverable:** Updated Zotero library with rationalised tags

---

## 📊 Current Statistics

**Consolidation Decisions:**
- Total pairs reviewed: 421 (was 332 + 89 new from taxonomy work)
- Merges: 2
- Hierarchies: 218
- Keep separate: 218
- Flagged: 0 ✅

**Tags:**
- Unique tags: 481
- Tagged items: 336 (304 primary sources + 32 other)
- Untagged items: 853
- Average tags per item: 11.24

**Documentation:**
- Scripts: 21 analysis tools
- Documentation files: 29 markdown files (~16,200 lines)
- Documentation-to-code ratio: 16:1

**Archaeological Data:**
- Features documented: ~256 (FAIMS Mobile)
- Integration: Pending Phase 3.1

---

## 🎓 Methodological Innovations Developed

### Pattern Recognition Training (Oct 19, 2025)
- User trains AI on 10 examples
- AI extracts classification pattern
- AI applies to remaining contexts
- User validates results
- **Success:** Achieved 100% accuracy on church dual-nature analysis

### Evidence-Based Disambiguation
- Primary: Explicit text evidence
- Secondary: Pattern-based classification
- Tertiary: Historical verification
- Lowest: Location tag inference
- **Principle:** "Tag what's in the source, not what might historically be true"

### Dual-Nature Entity Recognition
- **8 entities identified:** School of Arts, Katoomba School of Arts, Odd Fellows' Hall, Masonic Hall, Church (generic), Methodist Church, Katoomba Congregational Church, St Hilda's Church
- **Pattern:** Some entities function as BOTH organisation AND venue
- **Implementation:** Multi-tagging under relevant parent categories

---

## 📝 Documentation Files

**Planning:**
- `planning/TODO.md` ← This file
- `planning/project-plan.md` - Overall project workflow
- `planning/phase1.2.1-instructions.md` - Tag consolidation methodology
- `planning/phase1.2.1-consolidation-decisions.md` - All 421 decisions
- `planning/taxonomy_implementation_phase1.md` - Religion & Community institutions
- `planning/session_summary_2025-10-19.md` - First session achievements
- `planning/session_summary_2025-10-19-continued.md` - Second session achievements

**Core Documentation:**
- `docs/folksonomy_logic.md` - Complete tagging logic (1,336 lines)
- `docs/vocabularies.md` - Getty AAT, TGN, RVA standards
- `docs/gazetteer-comparison.md` - Geographic vocabulary options
- `docs/api-integration.md` - Zotero API patterns

**Reports:**
- `reports/tag_summary.md` - Overview statistics
- `reports/tag_analysis.md` - Detailed pattern analysis
- `reports/dual_nature_analysis_churches_councils.md` - Church & council analysis
- `reports/schools_of_arts_analysis.md` - Town-specific investigation
- `reports/taxonomy_implementation_churches_councils.md` - Implementation summary

**Data:**
- `data/tag_consolidation_map.csv` - 438 transformation rules (READY TO APPLY)
- `data/similar_tags.csv` - Original 332 similar pairs
- `data/tag_hierarchy.csv` - Detected parent-child relationships
- `data/tag_cooccurrence.csv` - Network relationships

---

## 💡 Key Principles Guiding This Project

1. **"Err on the side of maintaining existing granularity"** - Don't collapse prematurely
2. **"Tag what's in the source, not what might historically be true"** - Evidence-based only
3. **"Be liberal with tags; simplification later is straightforward"** - Preserve information
4. **Dual-nature entities deserve multi-tagging** - Don't force single classification
5. **Pattern recognition through training** - Efficient human-AI collaboration
