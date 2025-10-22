# Tag Consolidation Review Summary

**Generated:** 2025-10-19
**Last updated:** 2025-10-19 (post family name merge reversal)

---

## CRITICAL PRINCIPLE

**NO family or person names are merged without checking primary sources.**

This principle is strictly enforced throughout the consolidation process. Family names that appear similar (e.g., Peckman vs Penman) could represent different families (brothers, father-son, cousins, distinct family lines). All such cases require historian review with reference to original documents.

---

## Progress Overview

### Completed Automated Decisions ✅

**Total pairs processed:** 235 of 332 (70.8%)

| Category | Count | Status |
|----------|-------|--------|
| MERGE | 0 | **No merges without primary source verification** |
| HIERARCHY | 139 | Completed (105 initial + 34 automated) |
| KEEP_SEPARATE | 96 | Completed (83 person names + 13 false positives) |

### Remaining for Manual Review

**Total pairs requiring review:** 98 (29.5%)

Categorized as follows:

1. **CRITICAL: Family Names** (1 pair) - Requires primary source verification
2. **Naming Variants** (6 pairs) - May be same entity with different names
3. **Family Name Relationships** (8 pairs) - Require historian review
4. **Mining Domain** (16 pairs) - Requires mining industry domain expertise
5. **Contextual** (67 pairs) - Requires examining actual Zotero items

---

## Automated Decisions Applied (47 pairs)

### False Positives → KEEP_SEPARATE (13 pairs)

These were substring coincidences with no semantic relationship:

- `Pub` vs `Public meeting` / `Publican`
- `Bank` vs `Greenbank family` (surname contains "bank")
- `Band` vs `Husband family` / `Mr William Husband` / `Mr Robert J Husband`
- `Football` vs `Ball` (different concepts)
- `Mining` vs `Drinking`
- `Horses` vs `Boarding houses`
- `Death` vs `Debating`
- `Theft` vs `Athletics`
- `Weather` vs `Death`
- `Dogs` vs `Gas`
- `Blackheath` vs `Death`

### Generic → Specific Hierarchies (34 pairs)

These follow established patterns (e.g., Church → Methodist Church):

**Hotels** (18 hierarchies):
- Hotels → Megalong Hotel, Mount Victoria Hotel, Mrs Long's Hotel, Family Hotel,
  Belgravia Hotel, Railway Hotel, Grand Hotel, Allen's Hotel, Centennial Hotel,
  Brown's Hotel, Katoomba Hotel, Wentworth Falls Hotel, Imperial Hotel,
  Katoomba Family Hotel, Delaney's Hotel

**Coal/Mining** (4 hierarchies):
- Coal → Gladstone Coal Company, Katoomba Coal and Shale Mines, Katoomba coal mines,
  Katoomba Coal and Shale Company

**Sports** (4 hierarchies):
- Cricket → Katoomba Cricket Club, Megalong Cricket Club
- Football → Katoomba Football Club
- Tennis → Katoomba Tennis Club

**Infrastructure** (4 hierarchies):
- Councils → Lithgow Council, Katoomba Council
- Reserves → South Katoomba Reserve, Leura Reserve
- Roads → Nellie's Glen Road, Jenolan Caves road

**Shale mines** (3 hierarchies):
- Shale mines → Nellie's Glen Shale Mine, Ruined Castle Shale Mine, Katoomba Shale Mine

**Other** (1 hierarchy):
- Accident → Mining accidents
- Mining → Sunny Corner Mining Company

---

## Remaining 98 Pairs - Grouped for Review

### Category A: CRITICAL - Family Name Verification (1 pair)

**PRIORITY:** Requires checking primary sources before any decision

| Tag 1 | Tag 2 | Count 1 | Count 2 | Critical Issue |
|-------|-------|---------|---------|----------------|
| Peckman family | Penman family | 8 | 1 | Could be different families (distinct family lines, different spellings of unrelated families). Must verify against birth/death records, census data, or other primary sources before considering merge. |

**DO NOT MERGE without verification.** These could be:
- Completely different families with similar names
- Related families that should remain distinct
- Same family with variant spellings (only merge if verified in sources)

---

### Category B: Naming Variants (6 pairs)

**Requires investigation:** Check if same entity with different naming conventions

| Priority | Tag 1 | Tag 2 | Count 1 | Count 2 | Question |
|----------|-------|-------|---------|---------|----------|
| HIGH | Katoomba South | South Katoomba | 9 | 10 | Same location, different name order? |
| HIGH | Katoomba Superior Public School | Katoomba Public School | 8 | 6 | Same school renamed/reclassified? |
| MEDIUM | Katoomba Coal and Shale Mines | Katoomba Coal and Shale Company | 2 | 7 | Same company, different official names? |
| MEDIUM | Katoomba coal mines | Katoomba Coal and Shale Company | 9 | 7 | Same company (informal vs formal name)? |
| MEDIUM | Katoomba Coal and Shale Mines | Katoomba coal mines | 2 | 9 | Same mines (formal vs informal)? |
| LOW | Druid's Lodge | Lodges | 4 | 1 | Specific instance or false positive? |

**Recommendation:** Start with these 6 pairs - highest impact for effort

---

### Category C: Family Name Relationships (8 pairs)

**Requires historian review:** Determine if families are related or distinct

| Tag 1 | Tag 2 | Count 1 | Count 2 | Question |
|-------|-------|---------|---------|----------|
| Greenbank family | Penman family | 4 | 1 | Are these related families or distinct? |
| Gordon family | Brydon family | 14 | 9 | Are these related families or distinct? |
| Austin family | Watkins family | 12 | 6 | Are these related families or distinct? |
| Austin family | Eaton family | 12 | 3 | Are these related families or distinct? |
| Eaton family | Penman family | 3 | 1 | Are these related families or distinct? |
| Evans family | Eaton family | 8 | 3 | Are these related families or distinct? |
| Evans family | Penman family | 8 | 1 | Are these related families or distinct? |
| Husband family | Band | 10 | 8 | Substring coincidence (surname contains "band") - likely KEEP_SEPARATE |

**Note:** Even if families are historically related, they should typically remain as separate tags to preserve genealogical granularity unless there's clear evidence they're the same family unit.

---

### Category D: Mining Domain (16 pairs)

**Requires domain expertise:** Mining industry structure, miners vs mines relationships

#### Miners/Families/Dwellings:
- Miners vs Miners' families (32 vs 7) - Related but distinct concept?
- Miners' dwellings vs Miners (14 vs 32) - Subset or separate topic?

#### Miners vs Specific Mines:
- Miners vs Katoomba coal mines (32 vs 9)
- Miners vs Katoomba South mines (32 vs 8)
- Miners vs Hartley Vale mines (32 vs 2)
- Miners vs Katoomba Coal and Shale Mines (32 vs 2)
- Miners vs Coal mine (32 vs 7)
- Miners vs Katoomba Shale Mine (32 vs 4)
- Megalong Shale Mines vs Miners (9 vs 32)
- Shale mines vs Miners (48 vs 32)

#### Mines vs Minister/Coal:
- Miners vs Minister for Mines (32 vs 1) - Different concepts?
- Katoomba coal mines vs Coal mine (9 vs 7) - Specific vs generic?

#### Mine Relationships:
- Katoomba South mines vs Katoomba Shale Mine (8 vs 4)
- Katoomba Shale Mine vs Katoomba coal mines (4 vs 9)
- Katoomba South mines vs Katoomba coal mines (8 vs 9)
- Shale mines vs Hartley Vale mines (48 vs 2)

**Pattern to decide:** Are "Miners" (people) distinct from mines (places)? Hierarchy or separate?

---

### Category E: Contextual Review (67 pairs)

**Requires examining Zotero items** to understand relationships

#### High-Priority Patterns (clear decision likely):

**Generic → Specific Patterns (may be hierarchies):**
- Progress committees → Megalong/Mount Victoria Progress Committee (22 vs 1/2)
- Cricket clubs → Katoomba/Megalong Cricket Club (15 vs 2)
- Football clubs → Katoomba Football Club (clubs vs specific club)
- Publican's License → Publican / Pub (11 vs 1/3)
- Masonic Hall → Masons (11 vs 3)
- Odd Fellows' Hall → Oddfellows (24 vs 2)

**Geographic Hierarchies (may extend existing patterns):**
- Katoomba → South Katoomba Reserve (123 vs 1)
- Katoomba School of Arts → School (13 vs 12)
- Council Chambers → Councils (7 vs 27)
- Megalong Valley → Megalong Shale Mines (29 vs 9)

**Activity → Instance:**
- Tourism → Tourist trains (20 vs 5)
- Lawn Tennis Club → Tennis (2 vs 3)
- Katoomba Athletic Club → Athletics (2 vs 2)

**Lodges:**
- Mountaineer Lodge → Lodges (3 vs 1)
- Druid's Lodge → Lodges (4 vs 1) [also in naming variants]

#### Likely False Positives (substring coincidence):

**Person Names vs Concepts:**
- Mr Thomas Greenbank vs Bank (5 vs 2)
- Band vs Husband family (10 vs 8)
- Husband family already handled above

**Unrelated Concepts:**
- Constable O'Reilly vs Constable Orr (2 vs 5) - Different people?
- Sunny Corner vs Coroner (3 vs 1) - No relationship
- Mount Victoria School vs Mount Victoria Hotel (1 vs 2) - Both under Mt Victoria
- Disease vs Port Kembla disaster (8 vs 3) - Related or coincidence?
- Miners' dwellings vs Gas (14 vs 2) - No relationship
- Theft vs Katoomba Athletic Club (11 vs 2) - No relationship
- Tennis vs Centennial Hotel (3 vs 5) - No relationship
- Stores vs Katoomba Amateur Minstrels (9 vs 2) - No relationship

#### Special Cases:

**Nimmo Family:**
- Nimmo's vs Mr Zack Nimmo / Mr Robert Nimmo / Mr Joseph Nimmo / Mrs Elizabeth Nimmo
- Pattern: "Nimmo's" (business/property) vs individual Nimmos

**Family Names:** See Category C above for all family name relationships

**Katoomba Location Variants:**
- Katoomba South mines vs South Katoomba (8 vs 10) [cross-ref with naming variants]
- Katoomba Court vs Katoomba South/Katoomba Council/Katoomba South mines
- Katoomba Street vs South Katoomba Reserve/Katoomba station/Katoomba Athletic Club
- Katoomba Falls vs Katoomba Family Hotel (8 vs 2)
- Katoomba Hotel vs Katoomba Family Hotel (5 vs 2)

**Place-to-Place:**
- Wentworth Falls Hotel vs Allen's Hotel (3 vs 2) - Different hotels
- Family Hotel vs Railway Hotel / Belgravia Hotel (3 vs 3) - Different hotels
- Nellie's Glen track vs Nellie's Glen Road (3 vs 3) - Same or different?
- Wentworth Falls Reserves vs Wentworth Falls Progress Association (2 vs 2)
- Wentworth Falls Hotel vs Wentworth Falls Progress Association/Reserves (3 vs 2)

**Legal/Licensing:**
- Licensing Court vs Licensing Act (12 vs 4) - Related concepts?
- Bankruptcy vs Bank (4 vs 2) - Different concepts

**Elections:**
- Mr John Waudby's selection (Top Camp) vs Election (12 vs 17) - "selection" = election?

**Misc Pairings:**
- Ball vs Katoomba Football Club / Football clubs (4 vs 3/2) - Social event vs sport?
- Carrington Hotel vs Hotels (12 vs 62) - Should be hierarchy like others?

---

## Recommended Review Order

### Phase 0: CRITICAL - Family Name (1 pair, requires primary sources)

**Peckman family vs Penman family** - Do NOT proceed without checking birth/death records, census data, or other primary historical documents

### Phase 1: Quick Wins (6 pairs, ~5-10 minutes)

Review **Naming Variants** - highest value, clear yes/no decisions

### Phase 2: Family Name Relationships (8 pairs, ~10-15 minutes)

Review **Family Name Relationships** - determine if distinct families or related

- Default to KEEP_SEPARATE unless clear evidence of same family unit
- Consider historical context (intermarriage, geographic proximity)

### Phase 3: Domain Expertise (16 pairs, ~15-20 minutes)

Review **Mining Domain** - requires understanding of miners vs mines

### Phase 4: Contextual (67 pairs, ~25-35 minutes)

Work through contextual pairs by pattern:

1. Generic→Specific hierarchies (extend existing patterns)
2. False positives (substring coincidence)
3. Special cases (Nimmo's, Katoomba locations)

**Estimated total review time:** 55-80 minutes (excluding primary source research for Peckman/Penman)

---

## After Manual Review

Once decisions are made:

1. Update consolidation decisions file
2. Regenerate consolidation map CSV
3. **Review all 139 hierarchies for usefulness** (as requested)
4. Apply consolidation to Zotero (Phase 1.4 - optional)
