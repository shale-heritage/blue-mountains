# Mining Entities Classification Analysis

**Date:** 2025-10-20
**Purpose:** Determine correct classification of mining-related tags

---

## Key Findings from Primary Source Context

### 1. "Colliery" ❌ NEEDS CORRECTION
**Current placement:** Under mining companies

**Evidence:**
- Context 1: "Katoomba Colliery changed hands this week" (1890)
- Context 2: "lessee of the Katoomba colliery" (1905)
- Context 3: "Operations at the various collieries throughout the valley" (1903) - generic plural

**Analysis:**
"Colliery" appears to be:
- A shortened reference to "Katoomba Colliery" (specific company)
- OR a generic term for coal mining operations

**Recommendation:**
- **REMOVE** "Colliery" as separate tag (too ambiguous/generic)
- OR **RENAME** to "Katoomba Colliery" if that's a distinct entity
- Check if "Katoomba Coal and Shale Company" is the same as "Katoomba Colliery"

---

### 2. "Katoomba Coal and Shale Mines" ✅ CORRECTLY PLACED
**Current placement:** Under mining companies

**Evidence:**
- "The Katoomba Coal and Shale Mines are in full swing, and the Company require 500 men" (1891)

**Analysis:**
Despite having "Mines" (plural) in the name, this refers to the **COMPANY**, not the physical mines.
The phrase "and the Company require" confirms this is the corporate entity.

**Recommendation:**
- **KEEP** under Organizations > Commercial businesses > Mining companies
- This is the company name, even though it sounds like it refers to mines

---

### 3. "South Clifton Tunnel Mine" ❌ NEEDS CORRECTION
**Current placement:** Under mining companies

**Evidence:**
- "death of John Meredith, a wheeler, who was killed the previous day by a fall of stone in the South Clifton Tunnel Mine" (1910)

**Analysis:**
This clearly refers to the **PHYSICAL MINE SITE**, not a company.
"in the South Clifton Tunnel Mine" - locational usage.

**Recommendation:**
- **MOVE** from Organizations > Mining companies
- **TO:** Places > Mining districts > South Clifton > South Clifton Tunnel Mine
- OR: Built Environment > Mining infrastructure > Mines > South Clifton Tunnel Mine

---

### 4. "South Clifton Mine Co." ✅ PROBABLY CORRECT
**Current placement:** Under mining companies

**Evidence:** Not checked yet, but has "Co." in name

**Recommendation:**
- **KEEP** under mining companies (name indicates company)
- NOTE: This would be the COMPANY that operates "South Clifton Tunnel Mine" (the physical site)
- Dual classification appropriate:
  - Company: Organizations > Mining companies > South Clifton Mine Co.
  - Mine site: Places > Mining districts > South Clifton > South Clifton Tunnel Mine

---

### 5. "New South Wales Shale and Oil Co." ✅ CORRECTLY PLACED
**Current placement:** Under mining companies

**Evidence:**
- "one belonging to the New South Wales Shale and Oil Co." (1892)
- Has "Co." in name

**Recommendation:**
- **KEEP** under mining companies

---

### 6. "A.K.O. & M. Company" ✅ CORRECTLY PLACED
**Current placement:** Under mining companies

**Evidence:**
- Full name is "Australian Kerosene Oil and Shale Company"
- Multiple contexts refer to "the Australian Kerosene Oil and Shale Company"

**Recommendation:**
- **KEEP** under mining companies
- Consider adding scope note that this is abbreviation of "Australian Kerosene Shale and Oil Company"

---

## Complete List of Entities Under "Mining companies"

From poly_hierarchy_additions.csv:

1. ✅ A.K.O. & M. Company - COMPANY (has "Company" in name)
2. ✅ Australian Kerosene Shale and Oil Company - COMPANY (has "Company" in name)
3. ✅ Katoomba Coal and Shale Company - COMPANY (has "Company" in name)
4. ✅ Katoomba Coal and Shale Mines - COMPANY (despite "Mines", context shows it's company)
5. ✅ Gladstone Coal Company - COMPANY (has "Company" in name)
6. ✅ Sunny Corner Mining Company - COMPANY (has "Company" in name)
7. ✅ South Clifton Mine Co. - COMPANY (has "Co." in name)
8. ❌ South Clifton Tunnel Mine - **MINE SITE** (physical location, not company)
9. ✅ New South Wales Shale and Oil Co. - COMPANY (has "Co." in name)
10. ✅ Waudby & Co. - COMPANY (has "& Co." in name)
11. ❌ Colliery - **AMBIGUOUS/GENERIC** (should be removed or renamed to "Katoomba Colliery")

---

## Recommended Actions

### 1. Remove "Colliery" ❌
**Reason:** Too generic/ambiguous

**Action:** Delete row from tag_consolidation_map.csv

**Alternative:** Rename to "Katoomba Colliery" if it's a distinct entity

---

### 2. Move "South Clifton Tunnel Mine" ❌ → ✅
**FROM:** Organizations > Commercial businesses > Mining companies
**TO:** Places > Mining districts > South Clifton > South Clifton Tunnel Mine

**Rationale:** This is a physical mine site, not a corporate entity

**CSV change:**
```csv
OLD: South Clifton Tunnel Mine,South Clifton Tunnel Mine,hierarchy,parent=Mining companies
NEW: South Clifton Tunnel Mine,South Clifton Tunnel Mine,hierarchy,parent=South Clifton
     South Clifton,South Clifton,hierarchy,parent=Mining districts
```

---

### 3. Check for Other Mine Sites

Tags that might be physical sites (not companies):

- "Ruined Castle Shale Mine" - Currently under Places > Mining districts > Ruined Castle ✅
- "Nellie's Glen Shale Mine" - Currently under Places > Mining districts > Nellie's Glen ✅
- "Shale mines" (generic) - Currently under Activities > Economic activities > Mining > Shale mining ✅
- "Coal mine" (generic) - Currently under Activities > Economic activities > Mining > Coal mining ✅

**All correctly placed!**

---

## Relationship Between Companies and Mine Sites

Several entities have both a **company** (organization) and **mine site** (place):

| Company (Organization) | Mine Site (Place) |
|------------------------|-------------------|
| South Clifton Mine Co. | South Clifton Tunnel Mine |
| Australian Kerosene Shale and Oil Company | Ruined Castle Shale Mine? Nellie's Glen Shale Mine? |
| Katoomba Coal and Shale Company | Katoomba Colliery? |

**Note:** These relationships should be documented in scope notes for clarity.

---

## Summary of Changes Needed

1. ❌ **DELETE:** "Colliery" row from mining companies
2. ❌→✅ **MOVE:** "South Clifton Tunnel Mine" from mining companies to Places > Mining districts
3. ✅ **KEEP ALL OTHERS** under mining companies

---

## Next Steps

1. Check if "Katoomba Coal and Shale Company" and "Katoomba Coal and Shale Mines" are the same entity
2. Verify whether "Colliery" should be merged with one of these
3. Update poly_hierarchy_additions.csv
4. Regenerate visualizations

---

**Analysis completed by:** Claude Code
**Date:** 2025-10-20
**Source data:** Zotero primary source notes
