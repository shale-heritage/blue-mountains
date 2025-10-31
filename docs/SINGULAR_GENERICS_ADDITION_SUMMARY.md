# Singular Generics Addition Summary

**Date:** 2025-10-30
**Scripts:** `scripts/41_add_singular_generics.py`, `scripts/42_fix_awkward_singulars.py`

---

## Overview

Added singular generic terms to all plural categories that have specific named instances as direct children. This follows the established pattern:

```
Plural Category
├── Singular Generic (sibling to instances)
├── Specific Instance 1
├── Specific Instance 2
└── ...
```

**Example:**
```
Hotels
├── Hotel (generic term)
├── Carrington Hotel
├── Katoomba Hotel
└── ...
```

---

## Changes Summary

### Phase 1: Add Singular Generics
- **Started with:** 987 rows
- **Added:** 87 singular generic terms
- **Result:** 1,074 rows

### Phase 2: Fix Awkward Forms
- **Deleted:** 4 duplicate awkward forms
- **Renamed:** 1 awkward form
- **Final:** 1,070 rows

---

## Net Changes

**Original rows:** 987
**Final rows:** 1,070
**Net additions:** +83 singular generic terms

**Backups created:**
- `data/tag_map_consolidated.csv.backup-before-singular-generics`
- `data/tag_map_consolidated.csv.backup-before-awkward-fix`

---

## Categories Modified

### Built Environment (Examples)
- ✓ Halls → Hall
- ✓ Churches → Church
- ✓ Courts → Court
- ✓ Civic buildings → Civic building
- ✓ Commercial buildings → Commercial building
- ✓ Court buildings → Court building
- ✓ Religious buildings → Religious building
- ✓ Dwellings → Dwelling

### Places (Examples)
- ✓ Towns → Town
- ✓ Valleys → Valley
- ✓ Waterfalls → Waterfall
- ✓ Roads → Road
- ✓ Reserves → Reserve
- ✓ Mountain features → Mountain feature

### Agents (Examples)
- ✓ Animals → Animal
- ✓ Councils → Council
- ✓ Families → Family
- ✓ Hospitality workers → Hospitality worker
- ✓ Medical professionals → Medical professional
- ✓ Demographic groups → Demographic group
- ✓ Progress committees → Progress committee

### Events (Examples)
- ✓ Criminal events → Criminal event
- ✓ Cultural events → Cultural event
- ✓ Political events → Political event
- ✓ Social events → Social event
- ✓ Sporting events → Sporting event
- ✓ Life events → Life event

### Organizations (Examples)
- ✓ Athletic clubs → Athletic club
- ✓ Cricket clubs → Cricket club
- ✓ Football clubs → Football club
- ✓ Tennis clubs → Tennis club
- ✓ Lodges → Lodge
- ✓ Mining companies → Mining company

### Materials (Examples)
- ✓ Alcoholic beverages → Alcoholic beverage
- ✓ Spirits → Spirit

---

## Awkward Forms Fixed

### Deleted (Proper Form Already Existed)
1. **Boarding hous** → Deleted (kept: "Boarding house")
2. **Public hous** → Deleted (kept: "Public house")
3. **Tenni** → Deleted (kept: "Tennis")
4. **Coach and buggy busines** → Deleted (kept: "Coach and buggy business")

### Renamed
1. **Licens** → Renamed to: "License"

---

## Validation

### Pattern Verification

**Churches** (in Agents > Organizations > Religious organizations):
```
Churches
├── Church (singular generic) ✓
├── Congregational Church
│   └── Katoomba Congregational Church
├── Methodist Church
├── Roman Catholic Church
├── St Hilda's Church
└── Wesleyan Church
```

**Courts** (in Agents > Organizations > Government bodies):
```
Courts
├── Court (singular generic) ✓
├── Katoomba Court
├── Licensing Court
├── Police court
└── Supreme Court
```

**Halls** (in Built Environment > Community buildings):
```
Halls
├── Hall (singular generic) ✓
├── Clarke's Hall
├── Katoomba School of Arts
├── Masonic Hall
├── Mount Victoria Hall
└── Odd Fellows' Hall
```

**Towns** (in Places):
```
Towns
├── Blackheath
├── Clarence
├── Hartley Vale
├── Katoomba
├── Leura
├── Lithgow
├── Medlow
├── Megalong
├── Mount Victoria
├── Sydney
└── Town (singular generic) ✓
```

---

## Hierarchy Statistics

### Before Singular Generic Additions:
- Primary relationships: 570
- Total nodes: 487
- Leaf nodes: 315

### After All Changes:
- Primary relationships: 653
- Total nodes: 569
- Leaf nodes: 397
- **Total hierarchy relationships: 919**

---

## Categories Already Correct (Before This Work)

These 12 categories already followed the pattern:
1. Hotels → Hotel ✓
2. Bands → Band ✓
3. Choirs → Choir ✓
4. Coroners → Coroner ✓
5. Cottages → Cottage ✓
6. Hotelliers → Hotellier ✓
7. Postal services → Postal service ✓
8. Postmasters → Postmaster ✓
9. Pubs → Pub ✓
10. Rifle clubs → Rifle club ✓
11. Schools → School ✓
12. Stables → Stable ✓

---

## Pattern Rule Applied

**Only add singular generic when:**
1. Parent category is plural (ends in 's')
2. Parent has specific named instances as **direct children** (leaf nodes)
3. Singular generic doesn't already exist

**Do NOT add for:**
- Intermediate categories (no direct leaf children)
- Categories where plural doesn't clearly indicate multiple instances
- Cases where proper singular form already exists as a leaf

---

## Benefits

1. **Consistency:** All plural-with-instances categories now follow same pattern
2. **Findability:** Users can tag with generic term (e.g., "Hotel") when specific instance unknown
3. **Getty AAT Alignment:** Matches AAT practice of providing generic terms
4. **Query Flexibility:** Enables searching for "any hotel" vs "specific hotels"
5. **Documentation:** Makes taxonomy structure clearer and more predictable

---

## Scripts Created

### scripts/41_add_singular_generics.py
- Identifies plural categories with leaf children
- Calculates singular form
- Adds singular generic as sibling to instances
- Creates backup before modifications

### scripts/42_fix_awkward_singulars.py
- Removes duplicate awkward forms
- Renames remaining awkward forms
- Creates backup before modifications

Both scripts include:
- Comprehensive logging
- Backup creation
- Summary statistics
- Error handling

---

## Next Steps

1. ✅ Singular generics added (83 net)
2. ✅ Awkward forms fixed
3. ✅ Visualizations regenerated
4. ⏳ Continue with other tag corrections as needed
5. ⏳ Create API script for Zotero tag application
