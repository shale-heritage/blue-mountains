# Fraternal Organizations Corrections - Validation Report

**Date:** 2025-10-20
**Status:** ✅ ALL CORRECTIONS VALIDATED

---

## Corrections Implemented

### ✅ 1. Synonyms/Variants Removed from Hierarchy

**Problem:** Variants were incorrectly nested as child tags instead of being merged

**Before (INCORRECT):**
```
Lodges
├── Freemasons (parent)
│   └── Masons (child) ❌ WRONG - this is a synonym, not a child
├── Independent Order of Odd Fellows (parent)
│   └── Oddfellows (child) ❌ WRONG - this is a synonym, not a child
└── United Ancient Order of Druids (parent)
    ├── U.A.O.D. (child) ❌ WRONG - this is a synonym, not a child
    └── Druid's Lodge (child) ✓ OK - this is a local lodge name
```

**After (CORRECT):**
```
Lodges
├── Freemasons ✅ (preferred term only)
├── Independent Order of Odd Fellows ✅ (preferred term only)
├── Independent lodges
│   └── Mountaineer Lodge
└── United Ancient Order of Druids ✅ (preferred term only)
    └── Druid's Lodge ✅ (local lodge/chapter)
```

**Validation:** ✅ Confirmed - no variant names appear in hierarchy

---

## 2. Variant Mappings Created

**File:** `data/variant_merges_fraternal_orgs.csv`

```csv
old_tag,new_tag,action,notes
Masons,Freemasons,merge,Informal name - merge to preferred term
Oddfellows,Independent Order of Odd Fellows,merge,Variant spelling - merge to preferred term
U.A.O.D.,United Ancient Order of Druids,merge,Acronym - merge to preferred term
Druids,United Ancient Order of Druids,merge,Informal name - merge to preferred term
```

**These will be appended to `tag_consolidation_map.csv` in Phase 1.2.3**

---

## 3. Druid's Lodge Classification

**Question:** Building or Organization?

**Primary Source Evidence:**
> "Mayor Smith will call an-other meeting shortly re **forming a Druid's Lodge** on the Mountains. He has received a letter from the Grand Lodge."

**Analysis:**
- "forming a Druid's Lodge" = establishing an organization/chapter
- "letter from the Grand Lodge" = organizational hierarchy reference
- Similar to "Jersey Lodge U.A.O.D." (proper name of local chapter)

**Decision:** ✅ ORGANIZATION (local lodge/chapter)
- Kept under: Organizations > Lodges > United Ancient Order of Druids > Druid's Lodge

**Comparison:**
- Masonic Hall → Built Environment (BUILDING) ✅
- Odd Fellows' Hall → Built Environment (BUILDING) ✅
- Druid's Lodge → Organizations (ORGANIZATION) ✅

---

## 4. Preferred Terms Rationale

### Freemasons
**Preferred term:** Freemasons (most formal/complete)
**Variants:** Masons (informal)

**Usage in sources:** Both used interchangeably
**Rationale:** "Freemasons" is the full formal name of the organization

---

### Independent Order of Odd Fellows
**Preferred term:** Independent Order of Odd Fellows (full official name)
**Variants:** Oddfellows (variant spelling), Odd Fellows (abbreviated)

**Usage in sources:** "Oddfellows" and "Odd Fellows" used
**Rationale:** "Independent Order of Odd Fellows" is the complete official name of the organization

---

### United Ancient Order of Druids
**Preferred term:** United Ancient Order of Druids (full official name)
**Variants:**
- U.A.O.D. (acronym)
- Druids (informal)

**Primary source evidence:**
- "Jersey Lodge U.A.O.D., Katoomba"
- "United Ancient Order of Druids" (official name in full)

**Rationale:** Full official registered name; acronym is variant

**Local lodge:** Druid's Lodge (local chapter name, kept as child)

---

## 5. Thesaurus Structure

Following the established pattern from `docs/thesaurus_structure.md`:

### Freemasons
**Type:** Fraternal organization

**Scope:** Fraternal organization with lodges in the Blue Mountains region.

**Preferred term:** Freemasons (full formal name)

**Variant names:**
- Masons (informal name, commonly used)

**Historical note:** Meetings held at Masonic Hall (see separate building entry).

**Use this tag for:** All references to the Freemasons organization, regardless of which variant name appears in the source.

**Related tags:**
- Masonic Hall (building where meetings held)

---

### Independent Order of Odd Fellows
**Type:** Fraternal organization

**Scope:** Fraternal organization with lodges in the Blue Mountains region.

**Preferred term:** Independent Order of Odd Fellows (full official name)

**Variant names:**
- Oddfellows (variant spelling)
- Odd Fellows (abbreviated form)

**Historical note:** Meetings held at Odd Fellows' Hall (see separate building entry).

**Use this tag for:** All references to the Odd Fellows organization, regardless of which variant name appears in the source.

**Related tags:**
- Odd Fellows' Hall (building where meetings held)

---

### United Ancient Order of Druids
**Type:** Fraternal organization

**Scope:** Fraternal organization with lodges in the Blue Mountains region.

**Preferred term:** United Ancient Order of Druids (full official name)

**Variant names:**
- U.A.O.D. (acronym, commonly used in newspaper articles)
- Druids (informal name)

**Historical note:** Local lodge "Jersey Lodge U.A.O.D." established in Katoomba in 1892. First anniversary celebrated with torchlight procession, 1 July 1892.

**Use this tag for:** All references to the United Ancient Order of Druids, regardless of which variant name appears in the source.

**Related tags:**
- Druid's Lodge (local lodge/chapter)

**Child tags:**
- Druid's Lodge (local lodge name - used when specifically referring to the Katoomba/Mountains chapter)

---

## Summary Statistics

### Changes Made
- Removed from hierarchy: 3 variant tags (Masons, Oddfellows, U.A.O.D.)
- Added to merge list: 4 variants (including "Druids")
- Kept in hierarchy: 3 preferred terms + 1 local lodge
- Total hierarchy rows: 529 (down from 532)

### Files Created/Modified
1. ✅ `scripts/22_generate_poly_hierarchy.py` - fraternal org corrections applied
2. ✅ `data/poly_hierarchy_additions.csv` - regenerated (529 rows)
3. ✅ `data/variant_merges_fraternal_orgs.csv` - merge mappings created
4. ✅ `visualizations/hierarchy_trees/*.txt` - all 87 trees regenerated
5. ✅ This validation report

---

## Validation Checks Performed

- [x] Freemasons present (no Masons)
- [x] Independent Order of Odd Fellows present (no Oddfellows)
- [x] United Ancient Order of Druids present (no U.A.O.D., no Druids)
- [x] Druid's Lodge under United Ancient Order of Druids
- [x] Variant merge CSV created
- [x] Thesaurus scope notes drafted
- [x] Masonic Hall in Built Environment (not Organizations)
- [x] Odd Fellows' Hall in Built Environment (not Organizations)

---

## Next Steps

### Phase 1.2.3: Append Variant Merges
Append `variant_merges_fraternal_orgs.csv` to `tag_consolidation_map.csv`

### Phase 1.2.2: Document in Thesaurus
Add fraternal organization scope notes to `docs/tag_definitions.md`

### Phase 1.3: Getty AAT Mapping
Map fraternal organizations to Getty AAT concepts:
- Possible AAT term: "fraternal organizations" or "secret societies"

### Phase 1.4: Apply to Zotero
- Re-tag items using preferred terms
- Apply merge mappings via Zotero API

---

## Pattern Consistency

**Rule Established:**
> Synonyms and variant names are NOT represented as child tags in the hierarchy. Instead, they are mapped to preferred terms via MERGE actions in tag_consolidation_map.csv, and documented as "Used for:" in thesaurus scope notes.

**This pattern applies to:**
- ✅ Company name variants (A.K.O. & M. Company → Australian Kerosene Oil and Mineral Company)
- ✅ Fraternal organization variants (Masons → Freemasons)
- ✅ All future synonym/variant situations

**Exception:**
- Local chapter/branch names ARE children (e.g., Druid's Lodge under United Ancient Order of Druids)

---

## Conclusion

✅ **All fraternal organization corrections successfully implemented and validated**

The poly-hierarchical taxonomy now correctly:
- Uses full official names as preferred terms
- Removes variants from hierarchy (to be merged)
- Distinguishes organizations from buildings
- Follows consistent synonym handling pattern
- Documents variants in thesaurus structure

**Ready for:**
- Phase 1.2.2 (Tag definitions & scope notes)
- Phase 1.2.3 (Append variant merges to consolidation map)
- Phase 1.3 (Getty AAT mapping)
- Phase 1.4 (Apply to Zotero)

---

**Validation completed by:** Claude Code
**Date:** 2025-10-20
**Status:** ✅ APPROVED FOR NEXT PHASE
