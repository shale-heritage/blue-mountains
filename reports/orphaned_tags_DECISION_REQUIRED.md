# Orphaned Tags - Decision Required

**Date**: 2025-11-04
**Reviewers**: User review and approval needed
**Status**: PENDING APPROVAL

This report presents the final 3 orphaned tags requiring manual review and decision. Each section includes:
- Tag analysis from primary sources
- Recommended new tag mapping
- Approval options
- Confirmation of retagability

---

## Tag 1: Alcohol

### Summary
- **Current tag**: Alcohol
- **Items affected**: 12 items (0.32% of collection)
- **Date range**: 1890-1893
- **Publications**: Mostly Katoomba Times, Nepean Times

### Context from Primary Sources

The 12 items tagged with "Alcohol" include:

1. **Court cases** (items #1, #7, #8, #9): Alcohol-related court proceedings
   - Often co-tagged with "Court", "Court cases", "Drunkeness"
   - Example: "Katoomba Court" (14 Oct 1892) - co-tags include "Constable John Hamilton", "Drunkeness"

2. **Social issues** (items #2, #3, #4, #6): Community news mentioning alcohol
   - "Mountain Mixtures" columns with diverse content
   - Co-tagged with social events, accidents, community activities

3. **Death/tragedy** (item #5): "Found dead" (28 Jan 1893)
   - Co-tags: "Death", "Miners", mining company names
   - Likely alcohol-involved fatality

4. **Valley life** (items #10, #11, #12): Megalong Valley community
   - Co-tagged with "Megalong Valley", "Mining settlements", "Licensing"
   - General references to alcohol in mining communities

### Pattern Analysis

**Common co-tags suggest:**
- 9/12 items involve legal/court matters (Court, Court cases, Drunkeness, Licensing)
- 5/12 items relate to accommodation venues (Hotels, specific hotel names)
- 3/12 items are pure social/community references

The tag appears to have been used inconsistently as a catch-all for any alcohol mention, regardless of whether the item focuses on alcohol-related issues or merely mentions alcohol in passing.

### Recommended Mapping

**ACTION**: Add synonym mapping with merge guidance

```csv
alcoholic beverages,Alcohol,synonym,Broad folksonomy term - review items and retag with specific terms: alcoholic beverages (substances), drunkenness (intoxication/crime), alcohol-related (criminal events), publican's licence (licensing), or Hotels/public houses (venues)
```

### Retagging Strategy

For the 12 items, recommend manual review to apply more specific tags:

| Context | Replace with |
|---------|-------------|
| Court cases about drunkenness | drunkenness (crime) |
| Intoxication incidents | drunkenness (intoxication) |
| Alcohol-related criminal events | alcohol-related (under criminal events) |
| Licensing matters | publican's licence, licensing cases |
| Hotel/pub venues | Hotels, public houses, specific venue names |
| Alcoholic beverages mentioned | alcoholic beverages (+ specific type if known: beer, spirits, wine) |

**Sufficient info to retag?** ✓ YES - Co-tags provide clear context clues for correct categorisation

---

## Tag 2: Mining settlements

### Summary
- **Current tag**: Mining settlements
- **Items affected**: 7 items (0.19% of collection)
- **Date range**: 1885-1893
- **Publications**: Katoomba Times, Evening News

### Context from Primary Sources

The 7 items tagged with "Mining settlements" include:

1. **Megalong/Nellie's Glen area** (items #2, #3, #5):
   - "Unionism of To-day" (1 Sep 1893) - co-tags: Megalong, Miners' dwellings, Unions
   - "Megalong Mines" (1 Sep 1893) - co-tags: Megalong, Miners' dwellings, Top Camp, Nellie's Glen
   - "Megalong Valley" (18 Aug 1893) - co-tags: Megalong Valley, Middle camp

2. **Wentworth Falls** (item #4):
   - "Great Wentworth Falls Coal and Shale Mining Company" (31 Aug 1885)
   - Co-tags: Jamieson Valley, Shale mines, Wentworth Falls

3. **Hartley Vale** (item #6):
   - "Notice of Application for a Conditional Publican's Licence" (9 Jun 1893)
   - Co-tags: Hartley Vale, Megalong Hotel, Licensing

4. **Top Camp map** (item #7):
   - "Map of Top Camp" (29 Aug 1892)
   - Co-tags: Maps, Miners' dwellings, Mr John Waudby's selection (Top Camp)

5. **General community** (item #1):
   - "Mountain Mixtures" (9 Sep 1892) - multi-topic column

### Pattern Analysis

**Specific settlements identifiable:**
- **Middle camp** (appears in existing tags - specific settlement name)
- **Top Camp** (Mr John Waudby's selection - specific settlement name)
- **Hartley Vale** (already in taxonomy as town)
- **Nellie's Glen** (already in taxonomy as mining district with settlement)
- **Ruined Castle** (already in taxonomy as mining district with settlement)
- **Hartley Vale (settlement)** (already in taxonomy under Hartley Vale mining district)

**Current taxonomy already has:**
```
Places > mining districts > Hartley Vale mining district > Hartley Vale (settlement)
Places > mining districts > Nellie's Glen mining district > Nellie's Glen (settlement)
Places > mining districts > Ruined Castle mining district > Ruined Castle (settlement)
```

### Recommended Mapping

**OPTION A** (Recommended): Add generic term + retag with specific settlements

Add generic category term:
```csv
mining settlement,mining settlement,hierarchy,parent=mining districts (generic term for unspecified mining settlements)
```

Then retag the 7 items with specific settlements:
- Items #2, #3, #5, #7 → Middle camp (settlement) [NOTE: needs to be added under Greater Megalong]
- Item #4 → Possibly "Wentworth Falls" (town) or needs new "Jamieson Valley mining settlement"
- Item #6 → Hartley Vale (settlement) - already exists
- Item #1 → Review content to determine specific settlement

**OPTION B** (Alternative): Just merge to existing specific settlements

```csv
mining settlement,Mining settlements,merge,Folksonomy tag for various mining camp settlements - retag with specific settlement names: Hartley Vale (settlement), Nellie's Glen (settlement), Ruined Castle (settlement), Middle camp (settlement), or generic 'mining settlement' if unspecified
```

**My recommendation**: OPTION A - provides generic term for cases where specific settlement is unknown, while encouraging specific tagging where possible.

### Retagging Strategy

| Item | Recommended tags |
|------|-----------------|
| #1 | Review content → likely specific mining district |
| #2, #3 | Megalong + Middle camp (NEEDS ADDING) + Nellie's Glen mining district |
| #4 | Wentworth Falls + Jamieson Valley (OR add "Wentworth Falls mining settlement" if distinct) |
| #5 | Megalong Valley + Middle camp |
| #6 | Hartley Vale (settlement) - already exists |
| #7 | Middle camp + Top Camp (verify if these are same or different) |

**Sufficient info to retag?** ⚠ MOSTLY - Need to:
1. Add "Middle camp" as settlement (similar to existing "Middle camp (settlement)" under Greater Megalong)
2. Verify Top Camp = Middle camp or is separate settlement
3. Review item #1 and #4 for specific settlement references

---

## Tag 3: Rifle reserves

### Summary
- **Current tag**: Rifle reserves
- **Items affected**: 2 items (0.05% of collection)
- **Date range**: 1892, 1904
- **Publications**: Katoomba Times, Blue Mountain Gazette

### Context from Primary Sources

The 2 items tagged with "Rifle reserves":

1. **"Mountain Mixtures"** (21 Oct 1892, Katoomba Times)
   - Co-tags include: Druid's Lodge, Court, Church, Gold mining, Hotels
   - Multi-topic community news column

2. **"Town Talk"** (13 May 1904, Blue Mountain Gazette)
   - Co-tags include: Blackheath, Church, Dances, Death, Election, Katoomba
   - Multi-topic community news column

### Pattern Analysis

Both items are "Mixtures" / "Talk" columns covering multiple community topics. The "Rifle reserves" tag likely refers to:
- **Volunteer rifle reserves** - military/defence organisations
- **Rifle ranges** - recreational/training facilities

Based on existing taxonomy:
- **volunteer rifle reserves** exists under Agents > organisations > military organisations
  - Children: Katoomba Rifle Reserves, Mountain Rifle Reserves
- **rifle ranges** exists under Built Environment > recreation buildings > sports facilities
  - Child: rifle range (generic)

### Recommended Mapping

**ACTION**: Add synonym mapping to volunteer rifle reserves

```csv
volunteer rifle reserves,Rifle reserves,synonym,Short form - use full term 'volunteer rifle reserves' (military organisations)
```

**Alternative consideration**: These items might reference rifle range facilities rather than the military units. However, given the 1890s-1900s timeframe and co-occurrence with community/church/court topics, more likely references to the volunteer rifle reserve units participating in community life.

### Retagging Strategy

| Item | Action |
|------|--------|
| Both items | Replace "Rifle reserves" with "volunteer rifle reserves" |
| If facility mentioned | Also add "rifle range" (Built Environment) |

**Sufficient info to retag?** ✓ YES - Clear synonym relationship, though might benefit from content review to distinguish between:
- Organisation (volunteer rifle reserves)
- Facility (rifle ranges)

---

## Summary and Confirmation

### Retagging Completeness Check

**Can all affected items be retagged?**

| Tag | Items | Retaggable | Notes |
|-----|-------|------------|-------|
| Alcohol | 12 | ✓ YES | Co-tags provide clear context for specific categorisation |
| Mining settlements | 7 | ⚠ MOSTLY | Needs "Middle camp" added; 2 items need content review |
| Rifle reserves | 2 | ✓ YES | Direct synonym replacement |

### Action Items Before Proceeding

**Required:**
1. Add "Middle camp" settlement to taxonomy under Places > towns > Greater Megalong
2. Verify "Top Camp" vs "Middle camp" relationship (same place with two names, or distinct?)

**Recommended:**
3. Manual review of "Alcohol" items to apply specific tags (drunkenness, licensing, venues, beverages)
4. Content review of Mining settlements items #1 and #4 for specific settlement identification

### Approve / Reject / Change

Please review each tag and indicate your decision:

**Tag 1: Alcohol**
- [ ] APPROVE: Add synonym with merge guidance as recommended
- [ ] REJECT: Different approach needed
- [ ] CHANGE: (Please specify alternative mapping)

**Tag 2: Mining settlements**
- [ ] APPROVE OPTION A: Add generic term + specific retagging
- [ ] APPROVE OPTION B: Just merge with guidance
- [ ] REJECT: Different approach needed
- [ ] CHANGE: (Please specify alternative mapping)

**Tag 3: Rifle reserves**
- [ ] APPROVE: Add synonym to volunteer rifle reserves
- [ ] REJECT: Different approach needed
- [ ] CHANGE: (Please specify alternative mapping)

---

**CONFIRMATION**: With the addition of "Middle camp" settlement and the synonym mappings above, all 21 items (12 + 7 + 2) can be successfully retagged using the new taxonomy.

The existing co-tags on these items provide sufficient context clues to apply appropriate specific tags during the retagging process.
