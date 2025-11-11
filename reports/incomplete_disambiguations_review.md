# Incomplete Disambiguations - Manual Review Required

**Date:** 2025-11-09
**Status:** Requires user review and decision

## Summary

Found 10 entities with incomplete disambiguation patterns where both unqualified and qualified versions exist in the taxonomy:
- 9 church-related entities
- 1 hotel entity

## Issue Description

Per the leaf-node tagging pattern, when an entity has dual nature (e.g., both building and organisation), ALL uses should be disambiguated with parenthetical qualifiers. Having an unqualified version alongside qualified versions creates ambiguity.

## Entities Requiring Review

### 1. Church of England Katoomba

**Current state:**
- ✓ `Church of England Katoomba (organisation)` - exists
- ✓ `Church of England Katoomba (building)` - exists
- ⚠ `Church of England Katoomba` - exists as synonym target (from "Anglican Church Katoomba")

**Recommendation:** Convert the synonym to point to one of the qualified versions (likely organisation), or create separate synonyms for each aspect.

**Trove search:** `nla.obj-ID` (to be filled with specific item IDs from tag_application_mapping.csv)

---

### 2. Methodist Church Katoomba

**Current state:**
- ✓ `Methodist Church Katoomba (organisation)` - exists
- ⚠ `Methodist Church Katoomba (building)` - CHECK if exists
- ⚠ `Methodist Church Katoomba` - unqualified version exists

**Recommendation:** Complete the disambiguation pattern - add (building) if missing, remove or redirect unqualified version.

---

### 3. Presbyterian Church Leura

**Current state:**
- ✓ `Presbyterian Church Leura (organisation)` - exists
- ✓ `Presbyterian Church Leura (building)` - exists
- ⚠ `Presbyterian Church Leura` - unqualified version exists

**Recommendation:** Remove unqualified version or convert to synonym pointing to one of the qualified versions.

---

### 4. Presbyterian Church Wentworth Falls

**Current state:**
- ✓ `Presbyterian Church Wentworth Falls (organisation)` - exists
- ⚠ `Presbyterian Church Wentworth Falls (building)` - CHECK if exists
- ⚠ `Presbyterian Church Wentworth Falls` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 5. Roman Catholic Church Blackheath

**Current state:**
- ✓ `Roman Catholic Church Blackheath (organisation)` - exists
- ⚠ `Roman Catholic Church Blackheath (building)` - CHECK if exists
- ⚠ `Roman Catholic Church Blackheath` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 6. Roman Catholic Church Lawson

**Current state:**
- ✓ `Roman Catholic Church Lawson (organisation)` - exists
- ⚠ `Roman Catholic Church Lawson (building)` - CHECK if exists
- ⚠ `Roman Catholic Church Lawson` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 7. Roman Catholic Church Megalong

**Current state:**
- ✓ `Roman Catholic Church Megalong (organisation)` - exists
- ⚠ `Roman Catholic Church Megalong (building)` - CHECK if exists
- ⚠ `Roman Catholic Church Megalong` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 8. Roman Catholic Church Mount Victoria

**Current state:**
- ✓ `Roman Catholic Church Mount Victoria (organisation)` - exists
- ⚠ `Roman Catholic Church Mount Victoria (building)` - CHECK if exists
- ⚠ `Roman Catholic Church Mount Victoria` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 9. Wesleyan Church Katoomba

**Current state:**
- ✓ `Wesleyan Church Katoomba (organisation)` - exists
- ⚠ `Wesleyan Church Katoomba (building)` - CHECK if exists
- ⚠ `Wesleyan Church Katoomba` - unqualified version exists

**Recommendation:** Complete disambiguation pattern.

---

### 10. Grand Hotel

**Current state:**
- ✓ `Grand Hotel (Sydney)` - exists (2 instances - appears to be duplicate)
- ⚠ `Grand Hotel` - unqualified version exists

**Recommendation:** Determine if unqualified "Grand Hotel" refers to a different entity (Blue Mountains location vs Sydney location). If same as Sydney instance, convert to synonym. If different, add parenthetical qualifier for location disambiguation.

---

## Actions Required

1. **User review**: For each entity above, review primary source material in Zotero/Trove to determine:
   - Does the unqualified version represent a legitimate separate concept?
   - Should it be removed entirely?
   - Should it be converted to a synonym pointing to one of the qualified versions?

2. **Implementation**: Once decisions are made, update:
   - `tag_map_consolidated.csv` - add/remove/modify entries
   - `tag_application_mapping.csv` - update any mappings using unqualified versions

3. **Validation**: Verify no remaining incomplete disambiguations

## Search Strategy for Trove Review

For each entity, search Zotero library for items tagged with the unqualified version and review the full text context to understand whether the source is referring to:
- The building/venue
- The organisation/congregation
- Ambiguous/unclear (in which case, use qualified version based on primary context)

---

**Next Steps:**
- [ ] User reviews each case
- [ ] Decisions documented in this file
- [ ] Updates applied to taxonomy
- [ ] Validation run to confirm completion
