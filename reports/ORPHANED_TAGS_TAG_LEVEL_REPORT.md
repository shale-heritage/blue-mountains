# Orphaned Tags - Tag-Level Mapping Report

**Date**: 2025-11-06
**Purpose**: Tag-level mapping decisions for 36 remaining orphaned tags
**Total applications**: 275

---

## Category 1: EXACT MATCHES FOUND (abbreviations/variations) - 14 tags, 119 items

These have clear matches in taxonomy and can be mapped immediately.

| Orphaned Tag | Items | Recommended Mapping | Confidence |
|--------------|-------|---------------------|------------|
| A.K.O. & M. Company | 42 | Australian Kerosene Oil and Mineral Company | ✅ High (abbreviation) |
| U.A.O.D. | 3 | United Ancient Order of Druids | ✅ High (abbreviation) |
| Oddfellows | 2 | Independent Order of Odd Fellows | ✅ High (variant spelling) |
| Waudby & Co. | 7 | Waudby and Company | ✅ High (abbreviation) |
| Peckman Bros | 3 | Peckman Brothers | ✅ High (abbreviation) |
| Douglas & Co. | 2 | Douglas and Company | ✅ High (abbreviation) |
| Tabrett and Co. | 1 | Tabrett and Company | ✅ High (exact match) |
| Mr Charles George Gordon | 11 | Major Sir Charles George Gordon | ✅ High (variant name) |
| Billiard | 3 | billiards | ✅ High (singular→plural) |
| Masons | 3 | Freemasons | ✅ High (short form) |
| Stores | 9 | retailers and stores | ✅ High (parent→child) |
| Middle camp | 2 | Middle Camp (settlement) | ✅ High (case variant) |
| Pub | 3 | public house | ⚠️ Medium (synonym) |
| Katoomba Coal and Shale Mines | 2 | Katoomba Coal and Shale Company | ⚠️ Medium (check context) |

**Subtotal**: 119 applications (43% of remaining orphaned)

---

## Category 2: MULTIPLE OPTIONS - CONTEXT NEEDED - 12 tags, 124 items

These have multiple potential matches in taxonomy. Need to review item contexts to choose correct option.

### 2.1 Geographic Tags (3 tags, 56 items)

| Orphaned Tag | Items | Options in Taxonomy | Decision Needed |
|--------------|-------|---------------------|-----------------|
| Nellie's Glen | 25 | • Nellie's Glen (settlement)<br>• Nellie's Glen Shale Mine (site)<br>• Nellie's Glen Road | Review contexts: settlement vs mine vs road |
| Hartley Vale | 20 | • Hartley Vale (settlement)<br>• Hartley Vale mines<br>• Hartley Vale Natives Football Club | Review contexts: settlement vs mines vs club |
| Ruined Castle | 11 | • Ruined Castle (settlement)<br>• Ruined Castle - rock formation<br>• Ruined Castle Shale Mine (site) | Review contexts: settlement vs rock vs mine |

**Strategy**: Most likely **settlement** for generic references, but check contexts.

---

### 2.2 Occupational/Organizational Tags (4 tags, 56 items)

| Orphaned Tag | Items | Options in Taxonomy | Decision Needed |
|--------------|-------|---------------------|-----------------|
| Police | 27 | • police officers (occupation)<br>• Police Court (institution)<br>• New South Wales Police (organization) | Review contexts: officers vs court vs force |
| Post | 9 | • postal services (service)<br>• postal facilities (building)<br>• postal employees (occupation) | Review contexts: service vs building vs people |
| Publican's License | 11 | • publican (occupation)<br>• publican's licensing (process)<br>• liquor licensing (process) | Likely **publican's licensing** but verify |
| Mining settlements | 7 | • mining (activity)<br>• settlement (place type)<br>• Use both? | Likely needs multi-tag: location + mining |

---

### 2.3 Activity/Event Tags (3 tags, 9 items)

| Orphaned Tag | Items | Options in Taxonomy | Decision Needed |
|--------------|-------|---------------------|-----------------|
| Trucking | 8 | • cattle trucking yards (facility)<br>• cattle trucking yard (singular)<br>• trucking (activity - check if exists) | Check if generic "trucking" exists, else specify |
| Rape | 5 | • sexual violence (generic)<br>• assault (generic)<br>• Create specific tag? | Likely **sexual violence** but verify terminology |
| Port Kembla disaster | 3 | • disaster (event type)<br>• Port Kembla (place)<br>• Use both? | Specific event - may need multi-tag or new entry |

---

### 2.4 Hotel Tags (2 tags, 3 items)

| Orphaned Tag | Items | Options in Taxonomy | Decision Needed |
|--------------|-------|---------------------|-----------------|
| Grand Hotel | 3 | • Grand Hotel (Sydney) (specific)<br>• hotel (generic)<br>• Check if local Grand Hotel exists | Review contexts: Sydney hotel vs local hotel |
| Mrs Long's Hotel | 5 | • Mrs Long (person)<br>• hotel (generic)<br>• Create "Mrs Long's Hotel" entry? | Check if specific hotel should be added |

---

## Category 3: LIKELY NEED NEW ENTRIES - 4 tags, 14 items

These appear to reference specific entities not yet in taxonomy.

| Orphaned Tag | Items | Recommendation | Rationale |
|--------------|-------|----------------|-----------|
| Allen's Hotel | 2 | Add as specific hotel name | Specific named hotel |
| Brown's Hotel | 2 | Add as specific hotel name | Specific named hotel |
| Nellie's Glen track | 3 | Add under paths/tracks | Specific path/track |
| New South Wales Shale and Oil Co. | 2 | Add as mining company | Specific company (not in taxonomy) |

**Note**: South Clifton Mine Co. not listed - need to check if this is an abbreviation of existing company.

---

## Category 4: ORGANIZATIONS - VERIFY - 2 tags, 19 items

| Orphaned Tag | Items | Recommendation | Notes |
|--------------|-------|----------------|-------|
| I.O.O.F. Hall | 17 | Independent Order of Odd Fellows \| hall | Multi-tag: organization + building type |
| Katoomba Tennis Club | 2 | Check if exists as "Katoomba Tennis Club" | May already exist in taxonomy |
| Rifle reserves | 2 | Mountain Rifle Reserves (exact match found) | Check if abbreviation |

---

## Summary by Action Required

### IMMEDIATE: Direct Mapping (14 tags, 93 items)

Can be mapped now without context review:

```csv
A.K.O. & M. Company,Australian Kerosene Oil and Mineral Company
U.A.O.D.,United Ancient Order of Druids
Oddfellows,Independent Order of Odd Fellows
Waudby & Co.,Waudby and Company
Peckman Bros,Peckman Brothers
Douglas & Co.,Douglas and Company
Tabrett and Co.,Tabrett and Company
Mr Charles George Gordon,Major Sir Charles George Gordon
Billiard,billiards
Masons,Freemasons
Stores,retailers and stores
Middle camp,Middle Camp (settlement)
Pub,public house
```

**Action**: Create mapping entries for these 14 tags (93 total applications)

---

### REVIEW CONTEXTS: Multiple Options (12 tags, 124 items)

Need to review item contexts to choose correct option:

**High Priority** (>10 items each):
1. Police (27) - officers vs court vs force
2. Nellie's Glen (25) - settlement vs mine vs road
3. Hartley Vale (20) - settlement vs mines vs club
4. Ruined Castle (11) - settlement vs rock vs mine
5. Publican's License (11) - publican's licensing vs liquor licensing

**Medium Priority** (5-10 items):
6. Trucking (8) - cattle trucking vs generic
7. Post (9) - services vs facilities vs employees
8. Mining settlements (7) - multi-tag needed
9. Mrs Long's Hotel (5) - person + hotel vs specific hotel
10. Rape (5) - sexual violence vs assault

**Low Priority** (<5 items):
11. Grand Hotel (3) - Sydney vs local
12. Port Kembla disaster (3) - specific event

---

### ADD TO TAXONOMY: New Entries Needed (4 tags, 14 items)

Specific named entities to add:
1. Allen's Hotel (2) - specific hotel
2. Brown's Hotel (2) - specific hotel
3. Nellie's Glen track (3) - specific path
4. New South Wales Shale and Oil Co. (2) - mining company

---

### VERIFY: Check Taxonomy (3 tags, 19 items)

Check if these already exist under different names:
1. I.O.O.F. Hall (17) - hall + organization
2. Katoomba Tennis Club (2) - may exist
3. Rifle reserves (2) - may be "Mountain Rifle Reserves"

---

## Recommended Workflow

### Phase 1: Apply Immediate Mappings (30 minutes)

Map 14 tags with confident matches (93 applications)

**Output**: 93 new mapping entries

---

### Phase 2: Context Review for High Priority (2-3 hours)

Review contexts for 5 high-priority tags (94 applications):
- Police (27)
- Nellie's Glen (25)
- Hartley Vale (20)
- Ruined Castle (11)
- Publican's License (11)

**Method**: Extract KWIC contexts, determine most common usage, create mappings

**Output**: ~90 mapping entries

---

### Phase 3: Quick Resolution of Medium/Low Priority (1-2 hours)

Review remaining 7 tags (30 applications)

**Output**: ~25 mapping entries

---

### Phase 4: Taxonomy Additions (1 hour)

Add 4 new specific entries to taxonomy, create mappings

**Output**: 4 taxonomy additions + ~10 mapping entries

---

## Total Remaining Work Estimate

| Phase | Tags | Applications | Effort |
|-------|------|--------------|--------|
| 1. Immediate mappings | 14 | 93 | 30 min |
| 2. High priority contexts | 5 | 94 | 2-3 hrs |
| 3. Medium/low priority | 7 | 30 | 1-2 hrs |
| 4. Taxonomy additions | 4 | 14 | 1 hr |
| **TOTAL** | **36** | **275** | **5-7 hrs** |

---

## Files for Next Steps

### For Immediate Mapping

Create: `reports/batch_mappings_immediate.csv`

Entries for 14 high-confidence abbreviation/variation mappings

---

### For Context Review

For each high-priority tag, need:
- Item titles and dates
- Short contexts from full text (if available)
- Current usage patterns

**Tool**: scripts/43_extract_tag_contexts.py (if exists) or manual review

---

## Questions for User

1. **Approve immediate mappings?** - 14 tags with clear abbreviation/variation matches

2. **Priority order?** - Start with high-priority context reviews (Police, Nellie's Glen, etc.) or do all immediate mappings first?

3. **Pub → public house?** - Confirm this UK/Australian synonym

4. **Sexual violence terminology?** - Confirm "Rape" → "sexual violence" is appropriate term

5. **Multi-tag strategy?** - For "I.O.O.F. Hall" → "Independent Order of Odd Fellows | hall" or create specific "I.O.O.F. Hall" entry?

---

