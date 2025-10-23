# Taxonomy Fixes - 2025-10-23

**Purpose:** Systematic corrections to taxonomy structure for consistency and clarity

---

## Summary of Changes

**6 taxonomy fixes applied:**
1. Merged Postboy under Mailmen (mail delivery occupations grouped together)
2. Fixed Postal services pattern (plural → singular)
3. Updated Transport leaf nodes (Horses → Horseborne transportation)
4. Clarified Drunkenness (crime) vs (intoxication) distinction
5. Moved Middle camp from Mining settlements to Mining districts
6. Merged Hospitality venues into Accommodation buildings

**Total hierarchy relationships:** 679 (was 680)

---

## 1. Postal Employees - Mailmen Consolidation

**Change:** Merged Postboy under Mailmen category (both are mail delivery occupations)

**Before:**
```
Postal employees
  ├─ Postmasters > Postmaster > [specific people]
  ├─ Postboys > Postboy
  └─ Mailmen > Mailman
```

**After:**
```
Postal employees
  ├─ Postmasters > Postmaster > [specific people]
  └─ Mailmen (mail delivery occupations)
      ├─ Mailman (generic mail carrier)
      └─ Postboy (junior mail carrier/assistant)
```

**Thesaurus Addition:**
- `Postman` → synonym for `Mailman`

**Rationale:** Both Mailman and Postboy are mail delivery roles (vs. Postmaster which is administrative). Grouping them together under Mailmen provides better organizational clarity.

---

## 2. Postal Services Pattern Fix

**Change:** Applied Pattern A structure to Postal services

**Before:**
```
Activities > Communication activities
  └─ Postal services
      └─ Post
```

**After:**
```
Activities > Communication activities
  └─ Postal services (plural, organizational)
      └─ Postal service (singular, taggable)
```

**Thesaurus Addition:**
- `Post` → synonym for `Postal service` (marked as deprecated - use specific tags)

**Rationale:** Follows Pattern A (leaf nodes only) - plural organizational category with singular taggable term. Consistent with Hotels > Hotel, Churches > Church, etc.

---

## 3. Transport Leaf Nodes Clarification

**Change:** Updated Transport activity terms for clarity

**Before:**
```
Activities > Economic activities > Transport
  ├─ Trucking
  └─ Horses
```

**After:**
```
Activities > Economic activities > Transport
  ├─ Trucking
  └─ Horseborne transportation
```

**Rationale:** "Horseborne transportation" is more descriptive as an economic activity than just "Horses" (which exists separately under Agents > Animals). The term clearly indicates horses used for transport purposes.

**Note:** "Horses" still exists under Agents > Animals > Horses for references to horses as living organisms.

---

## 4. Drunkenness Disambiguation

**Change:** Clarified distinction between drunkenness as crime vs. health condition

**Before:**
```
Events > Criminal events > Alcohol-related
  └─ Drunkenness

Associated Concepts > Physical and health conditions
  └─ Drunkenness (intoxication)
```

**After:**
```
Events > Criminal events > Alcohol-related
  └─ Drunkenness (crime)

Associated Concepts > Physical and health conditions
  └─ Drunkenness (intoxication)
```

**Rationale:** Adding "(crime)" qualifier makes the leaf node self-documenting. Users can determine meaning from the tag name alone without needing to see full hierarchy path. Distinguishes:
- **Drunkenness (crime):** Court cases, charges, fines for public drunkenness
- **Drunkenness (intoxication):** State of being drunk, testimony about intoxication

**Also updated in thematic groupings:**
- Alcohol & Temperance > Alcohol consumption & behaviour > Drunkenness (crime)
- Justice & Crime > Crimes > Social order offences > Drunkenness (crime)

---

## 5. Middle Camp - Mining Districts Consolidation

**Change:** Moved Middle camp from deprecated Mining settlements to Mining districts

**Source Context:**
- **Item:** "Megalong Valley" (18 August 1893, Katoomba Times, Key: 2TRIXS5G)
- **Context:** "...increased the number of boarders at Mrs. Brydon's, Middle Camp, who appears to be a very hardworking woman striving to support herself and family..."

**Before:**
```
Places
  └─ Mining settlements
      └─ Middle camp
  └─ Towns > Megalong
      └─ Middle camp
```

**After:**
```
Places
  └─ Mining districts
      └─ Middle camp
  └─ Towns > Megalong
      └─ Middle camp (also appears under Mining districts)
```

**Rationale:**
- Middle camp is a specific mining camp location in Megalong Valley
- Mining settlements category deprecated - all items should use Mining districts
- Maintains poly-hierarchy: appears under both Mining districts (primary mining context) and Megalong (geographic locality)
- Mrs. Brydon's boarding house serviced miners at this camp location

**Action Required:** 2 items tagged "Middle camp" need verification, potentially retag any other "Mining settlements" items to specific mining districts.

---

## 6. Accommodation and Hospitality Venues Merger

**Change:** Merged separate Accommodation buildings and Hospitality venues into unified category

**Before:**
```
Built Environment
  ├─ Accommodation buildings
  │   ├─ Hotels > Hotel > [specific hotels]
  │   ├─ Boarding houses > Boarding house
  │   ├─ Cottages > Cottage
  │   ├─ Stables > Stable
  │   └─ Dwellings > Miners' dwellings
  └─ Hospitality venues
      ├─ Public house
      ├─ Pub (synonym)
      └─ Pubs (separate category!)
```

**After:**
```
Built Environment
  └─ Accommodation and hospitality venues
      ├─ Hotels > Hotel > [specific hotels]
      ├─ Boarding houses > Boarding house
      ├─ Cottages > Cottage
      ├─ Stables > Stable
      ├─ Dwellings > Miners' dwellings
      └─ Public houses (Pattern A)
          └─ Public house
```

**Thesaurus:**
- `Pub` → synonym for `Public house` (not separate taxonomy entry)

**Rationale:**
- Hotels and pubs overlap significantly in sources (both serve alcohol, both provide accommodation)
- "Hospitality venues" was redundant with "Accommodation buildings"
- Unified category better reflects historical reality of Blue Mountains venues
- Pattern A applied to Public houses: Public houses (plural) > Public house (singular, taggable)
- Removed confusing "Pubs" separate entry - Pub is now purely a synonym

**Also updated in thematic groupings:**
- Alcohol & Temperance > Alcohol-related venues > Public houses (was "Pubs")

---

## Pattern A Compliance Summary

All fixes maintain **Pattern A (leaf nodes only)** structure:
- **Plural Category** (organizational, NO TAG)
- **Singular Generic** (TAG when unnamed)
- **Specific Instances** (TAG when named)

**Examples from these fixes:**
- Mailmen > Mailman / Postboy ✓
- Postal services > Postal service ✓
- Public houses > Public house ✓

---

## Actions Required

1. **Middle camp items (2):** Verify tagging, ensure Mining districts used
2. **Mining settlements tag:** Audit all uses, migrate to specific Mining districts
3. **Drunkenness items (16):** Already split in previous work, verify applied
4. **Horses tag:** Review items to determine if referring to animals or transportation activity
5. **Pubs tag:** Audit all uses, retag as "Public house" following Pattern A

---

## Hierarchy Statistics

**Before fixes:** 680 relationships
**After fixes:** 679 relationships
**Change:** -1 (consolidated Postboys into Mailmen)

**Facet breakdown:**
- Agents: ~356 relationships
- Places: ~76 relationships
- Built Environment: ~73 relationships
- Activities & Events: ~176 relationships
- Concepts & Themes: ~32 relationships
- Materials: ~11 relationships
- Thematic groupings: 202 relationships

---

## Next Steps

1. Regenerate hierarchy visualizations with updated structure
2. Update TAGGING_GUIDELINES.md with examples from these fixes
3. Create migration scripts for deprecated tags:
   - Mining settlements → Mining districts
   - Pubs → Public house
   - Horses (transport) → Horseborne transportation
4. Apply Post tag changes to Zotero (9 items ready)
5. Apply alcohol + licensing changes (25 items ready)
6. Review accommodation report (64 items ready)

---

## Commit Reference

These changes implemented in commit [to be added]

All fixes maintain UK/Australian spelling and follow Pattern A (leaf nodes only) structure.
