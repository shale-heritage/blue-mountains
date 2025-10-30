# Tag Consolidation Triage Report

**Generated:** 2025-10-19 13:45:38
**Total flagged pairs reviewed:** 144

---

## Executive Summary

This report categorizes the 144 flagged pairs from automated analysis into decision groups for efficient batch review.

### Decision Statistics

- **Automated decisions proposed:** 47 pairs (32.6%)
  - False positives (keep separate): 13
  - Hierarchies (multi-tag): 34

- **Manual review required:** 97 pairs (67.4%)
  - Naming variants (investigate): 6
  - Mining domain (domain expertise): 16
  - Contextual review: 75

---

## Category 1: False Positives (KEEP_SEPARATE)

**Count:** 13 pairs
**Proposed action:** Mark as KEEP_SEPARATE (distinct concepts)

These pairs matched due to substring coincidence but are semantically unrelated.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Rationale |
|-------|-------|---------|---------|-----------|
| Pub | Public meeting | 3 | 1 | Substring coincidence - semantically unrelated concepts |
| Pub | Publican | 3 | 1 | Substring coincidence - semantically unrelated concepts |
| Bank | Greenbank family | 2 | 4 | Substring coincidence - semantically unrelated concepts |
| Band | Mr William Husband | 8 | 2 | Substring coincidence - semantically unrelated concepts |
| Band | Mr Robert J Husband | 8 | 4 | Substring coincidence - semantically unrelated concepts |
| Football | Ball | 6 | 4 | Substring coincidence - semantically unrelated concepts |
| Mining | Drinking | 32 | 2 | Substring coincidence - semantically unrelated concepts |
| Horses | Boarding houses | 19 | 8 | Substring coincidence - semantically unrelated concepts |
| Death | Debating | 53 | 2 | Substring coincidence - semantically unrelated concepts |
| Theft | Athletics | 11 | 2 | Substring coincidence - semantically unrelated concepts |
| Weather | Death | 49 | 53 | Substring coincidence - semantically unrelated concepts |
| Dogs | Gas | 8 | 2 | Substring coincidence - semantically unrelated concepts |
| Blackheath | Death | 22 | 53 | Substring coincidence - semantically unrelated concepts |

---

## Category 2: Generic → Specific Hierarchies (HIERARCHY)

**Count:** 34 pairs
**Proposed action:** Establish parent-child hierarchy with multi-tagging

These follow the same pattern as the 104 hierarchies already approved (e.g., Church → Methodist Church).

| Parent Tag | Child Tag | Count 1 | Count 2 | Rationale |
|------------|-----------|---------|---------|-----------|
| **Coal** | Gladstone Coal Company | 18 | 2 | Generic resource 'Coal' → specific instance 'Gladstone Coal Company' |
| **Coal** | Katoomba Coal and Shale Mines | 18 | 2 | Generic resource 'Coal' → specific instance 'Katoomba Coal and Shale Mines' |
| **Coal** | Katoomba coal mines | 18 | 9 | Generic resource 'Coal' → specific instance 'Katoomba coal mines' |
| **Coal** | Katoomba Coal and Shale Company | 18 | 7 | Generic resource 'Coal' → specific instance 'Katoomba Coal and Shale Company' |
| **Cricket** | Katoomba Cricket Club | 14 | 2 | Generic activity 'Cricket' → specific instance 'Katoomba Cricket Club' |
| **Cricket** | Megalong Cricket Club | 14 | 2 | Generic activity 'Cricket' → specific instance 'Megalong Cricket Club' |
| **Football** | Katoomba Football Club | 6 | 3 | Generic activity 'Football' → specific instance 'Katoomba Football Club' |
| **Accident** | Mining accidents | 16 | 16 | Generic concept 'Accident' → specific type 'Mining accidents' |
| **Tennis** | Katoomba Tennis Club | 3 | 2 | Generic activity 'Tennis' → specific instance 'Katoomba Tennis Club' |
| **Mining** | Sunny Corner Mining Company | 32 | 2 | Generic activity 'Mining' → specific instance 'Sunny Corner Mining Company' |
| **Shale mines** | Nellie's Glen Shale Mine | 48 | 6 | Generic type 'Shale mines' → specific instance 'Nellie's Glen Shale Mine' |
| **Shale mines** | Ruined Castle Shale Mine | 48 | 26 | Generic type 'Shale mines' → specific instance 'Ruined Castle Shale Mine' |
| **Shale mines** | Katoomba Shale Mine | 48 | 4 | Generic type 'Shale mines' → specific instance 'Katoomba Shale Mine' |
| **Reserves** | South Katoomba Reserve | 11 | 1 | Generic type 'Reserves' → specific instance 'South Katoomba Reserve' |
| **Reserves** | Leura Reserve | 11 | 2 | Generic type 'Reserves' → specific instance 'Leura Reserve' |
| **Councils** | Lithgow Council | 27 | 2 | Generic type 'Councils' → specific instance 'Lithgow Council' |
| **Councils** | Katoomba Council | 27 | 22 | Generic type 'Councils' → specific instance 'Katoomba Council' |
| **Hotels** | Megalong Hotel | 62 | 9 | Generic type 'Hotels' → specific instance 'Megalong Hotel' |
| **Hotels** | Mount Victoria Hotel | 62 | 2 | Generic type 'Hotels' → specific instance 'Mount Victoria Hotel' |
| **Hotels** | Mrs Long's Hotel | 62 | 5 | Generic type 'Hotels' → specific instance 'Mrs Long's Hotel' |
| **Hotels** | Family Hotel | 62 | 3 | Generic type 'Hotels' → specific instance 'Family Hotel' |
| **Hotels** | Belgravia Hotel | 62 | 3 | Generic type 'Hotels' → specific instance 'Belgravia Hotel' |
| **Hotels** | Railway Hotel | 62 | 3 | Generic type 'Hotels' → specific instance 'Railway Hotel' |
| **Hotels** | Grand Hotel | 62 | 3 | Generic type 'Hotels' → specific instance 'Grand Hotel' |
| **Hotels** | Allen's Hotel | 62 | 2 | Generic type 'Hotels' → specific instance 'Allen's Hotel' |
| **Hotels** | Centennial Hotel | 62 | 5 | Generic type 'Hotels' → specific instance 'Centennial Hotel' |
| **Hotels** | Brown's Hotel | 62 | 2 | Generic type 'Hotels' → specific instance 'Brown's Hotel' |
| **Hotels** | Katoomba Hotel | 62 | 5 | Generic type 'Hotels' → specific instance 'Katoomba Hotel' |
| **Hotels** | Wentworth Falls Hotel | 62 | 3 | Generic type 'Hotels' → specific instance 'Wentworth Falls Hotel' |
| **Hotels** | Imperial Hotel | 62 | 5 | Generic type 'Hotels' → specific instance 'Imperial Hotel' |
| **Hotels** | Katoomba Family Hotel | 62 | 2 | Generic type 'Hotels' → specific instance 'Katoomba Family Hotel' |
| **Hotels** | Delaney's Hotel | 62 | 5 | Generic type 'Hotels' → specific instance 'Delaney's Hotel' |
| **Roads** | Nellie's Glen Road | 15 | 3 | Generic type 'Roads' → specific instance 'Nellie's Glen Road' |
| **Roads** | Jenolan Caves road | 15 | 2 | Generic type 'Roads' → specific instance 'Jenolan Caves road' |

---

## Category 3: Naming Variants (INVESTIGATE)

**Count:** 6 pairs
**Proposed action:** Examine actual Zotero items to determine if same entity

These pairs may represent the same entity with different naming conventions. Requires checking bibliographic items.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Question to Answer |
|-------|-------|---------|---------|-------------------|
| Katoomba South | South Katoomba | 9 | 10 | Same location, different naming convention? |
| Druid's Lodge | Lodges | 4 | 1 | Are these the same entity? |
| Katoomba Coal and Shale Mines | Katoomba Coal and Shale Company | 2 | 7 | Same company/mine (different official names)? |
| Katoomba coal mines | Katoomba Coal and Shale Company | 9 | 7 | Same company/mine (different official names)? |
| Katoomba Coal and Shale Mines | Katoomba coal mines | 2 | 9 | Same company/mine (different official names)? |
| Katoomba Superior Public School | Katoomba Public School | 8 | 6 | Same school (renamed/reclassified)? |

---

## Category 4: Mining Domain Relationships (REVIEW)

**Count:** 16 pairs
**Proposed action:** Apply domain expertise for miners/mines/dwellings relationships

These involve complex relationships between miners, mines, mine infrastructure, and related concepts.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Domain Consideration |
|-------|-------|---------|---------|---------------------|
| Miners | Miners' families | 32 | 7 | Are miners' families a related but distinct concept? |
| Miners' dwellings | Miners | 14 | 32 | Are miners' dwellings a subset/aspect of miners generally? |
| Katoomba coal mines | Coal mine | 9 | 7 | Relationship between concept and instance? |
| Shale mines | Miners | 48 | 32 | Relationship between concept and instance? |
| Miners | Katoomba coal mines | 32 | 9 | Relationship between concept and instance? |
| Miners | Katoomba South mines | 32 | 8 | Relationship between concept and instance? |
| Miners | Hartley Vale mines | 32 | 2 | Relationship between concept and instance? |
| Miners | Katoomba Coal and Shale Mines | 32 | 2 | Relationship between concept and instance? |
| Megalong Shale Mines | Miners | 9 | 32 | Relationship between concept and instance? |
| Katoomba South mines | Katoomba Shale Mine | 8 | 4 | Relationship between concept and instance? |
| Katoomba Shale Mine | Katoomba coal mines | 4 | 9 | Relationship between concept and instance? |
| Miners | Minister for Mines | 32 | 1 | Relationship between concept and instance? |
| Katoomba South mines | Katoomba coal mines | 8 | 9 | Relationship between concept and instance? |
| Shale mines | Hartley Vale mines | 48 | 2 | Relationship between concept and instance? |
| Miners | Coal mine | 32 | 7 | Relationship between concept and instance? |
| Miners | Katoomba Shale Mine | 32 | 4 | Relationship between concept and instance? |

---

## Category 5: Contextual Review Required (REVIEW)

**Count:** 75 pairs
**Proposed action:** Examine Zotero items to understand semantic relationship

These pairs require looking at actual bibliographic context to determine appropriate action.

| Tag 1 | Tag 2 | Count 1 | Count 2 | Similarity |
|-------|-------|---------|---------|-----------|
| Lawn Tennis Club | Tennis | 2 | 3 | 100.0% |
| Bankruptcy | Bank | 4 | 2 | 100.0% |
| Husband family | Band | 10 | 8 | 100.0% |
| Katoomba | South Katoomba Reserve | 123 | 1 | 100.0% |
| Katoomba Superior Public School | Pub | 8 | 3 | 100.0% |
| Katoomba School of Arts | School | 13 | 12 | 100.0% |
| Publican's License | Publican | 11 | 1 | 100.0% |
| Publican's License | Pub | 11 | 3 | 100.0% |
| Katoomba Public School | Pub | 6 | 3 | 100.0% |
| Ball | Katoomba Football Club | 4 | 3 | 100.0% |
| Ball | Football clubs | 4 | 2 | 100.0% |
| Mr Thomas Greenbank | Bank | 5 | 2 | 100.0% |
| Mr John Waudby’s selection (Top Camp) | Election | 12 | 17 | 100.0% |
| Progress committees | Megalong Progress Committee | 22 | 1 | 97.0% |
| Progress committees | Mount Victoria Progress Committee | 22 | 2 | 97.0% |
| Cricket clubs | Megalong Cricket Club | 15 | 2 | 96.0% |
| Cricket clubs | Katoomba Cricket Club | 15 | 2 | 96.0% |
| Katoomba Football Club | Football clubs | 3 | 2 | 96.0% |
| Constable O'Reilly | Constable Orr | 2 | 5 | 92.0% |
| Sunny Corner | Coroner | 3 | 1 | 92.0% |
| Mountaineer Lodge | Lodges | 3 | 1 | 91.0% |
| Carrington Hotel | Hotels | 12 | 62 | 91.0% |
| Odd Fellows' Hall | Oddfellows | 24 | 2 | 90.0% |
| Nellie's Glen track | Nellie's Glen Road | 3 | 3 | 89.0% |
| Katoomba Athletic Club | Athletics | 2 | 2 | 89.0% |
| Council Chambers | Councils | 7 | 27 | 88.0% |
| Mount Victoria School | Mount Victoria Hotel | 1 | 2 | 88.0% |
| Mount Victoria Hall | Mount Victoria Hotel | 2 | 2 | 87.0% |
| Wentworth Falls Hotel | Allen's Hotel | 3 | 2 | 87.0% |
| Licensing Court | Licensing Act | 12 | 4 | 86.0% |
| Sunny Corner Mining Company | Coroner | 2 | 1 | 86.0% |
| Katoomba Court | Katoomba South mines | 8 | 8 | 86.0% |
| Katoomba Court | Katoomba South | 8 | 9 | 86.0% |
| Katoomba Congregational Church | Katoomba Court | 12 | 8 | 86.0% |
| Disease | Port Kembla disaster | 8 | 3 | 86.0% |
| Tourism | Tourist trains | 20 | 5 | 86.0% |
| Katoomba Falls | Katoomba Family Hotel | 8 | 2 | 86.0% |
| Katoomba Court | Katoomba Council | 8 | 22 | 86.0% |
| Wentworth Falls Progress Association | Leura Progress Association | 2 | 2 | 85.0% |
| Greenbank family | Penman family | 4 | 1 | 85.0% |
| Katoomba Progress Association | Leura Progress Association | 8 | 2 | 85.0% |
| Senior-Constable Thorncroft | Constable Orr | 1 | 5 | 85.0% |
| Gordon family | Brydon family | 14 | 9 | 85.0% |
| Mount Victoria Hall | Mount Victoria School | 2 | 1 | 85.0% |
| Constable John Hamilton | Constable Orr | 5 | 5 | 85.0% |
| Austin family | Watkins family | 12 | 6 | 85.0% |
| Eaton family | Penman family | 3 | 1 | 83.0% |
| Nimmo's | Mr Zack Nimmo | 3 | 3 | 83.0% |
| Mr Joseph Nimmo | Nimmo's | 14 | 3 | 83.0% |
| Family Hotel | Railway Hotel | 3 | 3 | 83.0% |
| Nimmo's | Mr Robert Nimmo | 3 | 2 | 83.0% |
| Masonic Hall | Masons | 11 | 3 | 83.0% |
| Wentworth Falls Reserves | Wentworth Falls Progress Association | 2 | 2 | 83.0% |
| Evans family | Eaton family | 8 | 3 | 83.0% |
| Evans family | Penman family | 8 | 1 | 83.0% |
| Tennis | Centennial Hotel | 3 | 5 | 83.0% |
| Stores | Katoomba Amateur Minstrels | 9 | 2 | 83.0% |
| Nimmo's | Mrs Elizabeth Nimmo | 3 | 1 | 83.0% |
| Belgravia Hotel | Railway Hotel | 3 | 3 | 83.0% |
| Nellie's Glen Road | Nellie's Glen Shale Mine | 3 | 6 | 83.0% |
| Katoomba South mines | South Katoomba | 8 | 10 | 82.0% |
| Katoomba Tennis Club | Katoomba Athletic Club | 2 | 2 | 81.0% |
| Lawn Tennis Club | Katoomba Tennis Club | 2 | 2 | 81.0% |
| Katoomba South mines | South Katoomba Reserve | 8 | 1 | 81.0% |
| Wentworth Falls Hotel | Wentworth Falls Progress Association | 3 | 2 | 81.0% |
| Wentworth Falls Hotel | Wentworth Falls Reserves | 3 | 2 | 81.0% |
| Miners' dwellings | Gas | 14 | 2 | 80.0% |
| Mount Victoria Progress Committee | Mount Victoria Hotel | 2 | 2 | 80.0% |
| Theft | Katoomba Athletic Club | 11 | 2 | 80.0% |
| Katoomba Street | South Katoomba Reserve | 4 | 1 | 80.0% |
| Katoomba Street | Katoomba station | 4 | 5 | 80.0% |
| Katoomba Street | Katoomba Athletic Club | 4 | 2 | 80.0% |
| Austin family | Eaton family | 12 | 3 | 80.0% |
| Megalong Valley | Megalong Shale Mines | 29 | 9 | 80.0% |
| Katoomba Hotel | Katoomba Family Hotel | 5 | 2 | 80.0% |

---

## Recommended Next Steps

### Immediate Batch Decisions (Can approve without further review)

1. **Accept all 13 FALSE_POSITIVE pairs** → Mark as KEEP_SEPARATE
2. **Accept all 34 HIERARCHY pairs** → Establish parent-child relationships

This resolves 47 of 144 pairs (32.6%) with high confidence.

### Requires Investigation (6 pairs)

For naming variants, check Zotero items to determine:
- Are they the same entity? → MERGE (with canonical form decision)
- Are they related but distinct? → HIERARCHY or KEEP_SEPARATE

### Requires Domain Expertise (91 pairs)

The mining domain relationships and contextual pairs require historian review:
- Understanding of historical mining industry structure
- Knowledge of local institutions and relationships
- Examination of actual bibliographic context

---

## Approval Workflow

**Option A (Fast):** Approve Categories 1-2 as batch, review Categories 3-5 individually

**Option B (Careful):** Review sample from each category before batch approval

**Recommended:** Option A - batch approve obvious patterns, focus time on genuinely ambiguous cases

