# Mining Taxonomy Reorganization Summary

**Date:** 2025-10-30
**Script:** `scripts/44_reorganize_mining_taxonomy.py`

---

## Overview

Comprehensive reorganization of mining-related tags to align with Getty AAT principles, ensuring clear separation of activities, physical structures, places, agents, and events.

---

## Key Changes

### 1. **Merged Commercial Activities into Economic Activities** ✓

**Before:**
```
Activities
├── Commercial activities
│   └── Liquor trade
└── Economic activities
    ├── Mining
    ├── Tourism
    └── Transport
```

**After:**
```
Activities
└── Economic activities
    ├── Liquor trade
    ├── Mining
    ├── Tourism
    └── Transport
```

**Rationale:** Only one activity (Liquor trade) was under Commercial activities. Economic activities is the more standard, broader term.

---

### 2. **Added Coal and Shale to Materials Facet** ✓

**New Structure:**
```
Materials
├── Coal (NEW)
├── Consumable materials
│   └── Alcoholic beverages
└── Shale (NEW)
```

**Rationale:** Coal and Shale are materials, not activities. They were incorrectly placed under Coal mining activity.

---

### 3. **Created Mines Category in Built Environment** ✓

**New Structure:**
```
Built Environment
└── Industrial buildings (NEW)
    └── Mines (NEW)
        ├── Mine (singular generic)
        ├── Coal mines
        │   ├── Coal mine (singular generic)
        │   ├── Katoomba coal mines
        │   └── South Clifton Tunnel Mine
        └── Shale mines
            ├── Shale mine (singular generic)
            ├── Katoomba Shale Mine
            ├── Megalong Shale Mines
            ├── Nellie's Glen Shale Mine
            └── Ruined Castle Shale Mine
```

**Rationale:** Mines are physical built structures, not activities. Following the pattern: Industrial buildings > Mines > [type] mines > specific named mines.

---

### 4. **Created Mining Districts and Settlements in Places** ✓

**New Structure:**
```
Places
├── Mining districts (NEW)
│   ├── Mining district (singular generic)
│   ├── Nellie's Glen
│   ├── Ruined Castle
│   └── South Clifton
└── Mining settlements (under Settlements)
    ├── Mining settlement (singular generic)
    ├── Middle camp
    ├── Nellie's Glen (poly-hierarchy)
    └── Ruined Castle (poly-hierarchy)
```

**Rationale:**
- Mining districts are geographic areas
- Mining settlements are inhabited places
- Nellie's Glen and Ruined Castle function as both districts and settlements (poly-hierarchy)

---

### 5. **Standardized Mining Company Names in Agents** ✓

**Merges Performed:**

| Old Name (Deleted) | New Name (Primary) |
|-------------------|-------------------|
| A.K.O. & M. Company | Australian Kerosene Oil and Mineral Company |
| Australian Kerosene Shale and Oil Company | Australian Kerosene Oil and Mineral Company |
| Katoomba Coal and Shale Mines | Katoomba Coal and Shale Company |
| New South Wales Shale and Oil Co. | New South Wales Shale and Oil Company |
| South Clifton Mine Co. | South Clifton Mine Company |
| Waudby & Co. | Waudby and Company |

**Final Structure:**
```
Agents > Organizations > Commercial businesses > Mining companies
├── Mining company (singular generic)
├── Australian Kerosene Oil and Mineral Company
├── Gladstone Coal Company
├── Katoomba Coal and Shale Company
├── New South Wales Shale and Oil Company
├── South Clifton Mine Company
├── Sunny Corner Mining Company
└── Waudby and Company
```

**Rationale:**
- Spell out abbreviated names (Co. → Company, & → and)
- Use official registered company names
- Historical research confirmed some variants were same entity

---

### 6. **Created Mining Events in Events Facet** ✓

**New Structure:**
```
Events
└── Mining events (NEW)
    ├── Mine closure
    └── Mining accidents
        ├── Mining accident (singular generic)
        └── Mount Kembla Disaster
```

**Rationale:** Mining accidents and mine closures are events, not activities. Moved from Economic activities > Mining to Events > Mining events.

---

### 7. **Simplified Economic Activities > Mining** ✓

**Before:**
```
Economic activities > Mining
├── Coal mining
│   ├── Coal (intermediate tag)
│   │   ├── Coal mine (building)
│   │   ├── Companies mixed in
│   │   └── Katoomba coal mines (building)
│   ├── Coal mine (duplicate)
│   └── Coal mines (duplicate)
├── Gold mining
├── Mining accidents (should be Events)
├── Mining settlements (should be Places)
└── Shale mining
    └── Shale mines (buildings mixed in)
```

**After:**
```
Economic activities > Mining (ACTIVITIES ONLY)
├── Coal mining
├── Gold mining
└── Shale mining
```

**Rationale:** Keep only mining ACTIVITIES. Removed buildings, companies, settlements, and events to appropriate facets.

---

### 8. **Removed Colliery Tag** ✓

**Action:** Deleted standalone "Colliery" tag

**Thesaurus Entry:** "Colliery" becomes synonym for "Coal mine"

**Retagging Required:**
- Items tagged with "Colliery" need to be retagged to "Coal mine"
- Company names containing "Colliery" (e.g., "Katoomba Colliery") may need individual assessment

---

## Statistics

**CSV Changes:**
- Original rows: 1,066
- Deleted rows: 27
- Added rows: 35
- Final rows: 1,067
- Net change: +1

**Changes by Category:**
- Company merges: 6
- Mines moved: 13 (to Built Environment)
- Settlements/districts moved: 10 (to Places)
- Events moved: 5 (to Events facet)
- Materials added: 2 (Coal, Shale)
- Commercial activities merged: 2

---

## Getty AAT Alignment

These changes align with Getty AAT principles:

1. **Facet Separation:** Clear distinction between:
   - Activities (what people do)
   - Built Environment (physical structures)
   - Agents (people and organizations)
   - Events (occurrences)
   - Materials (substances)
   - Places (geographic locations)

2. **Hierarchical Clarity:** Follows pattern of plural category > singular generic > named instances

3. **Poly-Hierarchy:** Nellie's Glen and Ruined Castle appear in both districts and settlements, reflecting their dual nature

---

## Backup

Original CSV backed up to: `data/tag_map_consolidated.csv.backup-before-mining-reorg`

---

## Next Steps

1. **Create thesaurus entries:**
   - Colliery → Coal mine (synonym)
   - A.K.O. & M. Company → Australian Kerosene Oil and Mineral Company (variant)
   - Etc. for all merged company names

2. **Retag Zotero items:**
   - Items tagged "Colliery" → retag to "Coal mine"
   - Items with old company names → retag to standardized names

3. **Update documentation:**
   - Update folksonomy_logic.md
   - Update thesaurus_structure.md

---

## Files Modified

- `data/tag_map_consolidated.csv` - Main taxonomy (1,066 → 1,067 rows)
- `scripts/44_reorganize_mining_taxonomy.py` - Reorganization script (NEW)
- `visualizations/hierarchy_trees/*.txt` - All visualizations regenerated

---

## Historical Context from Research

### Australian Kerosene Oil and Mineral Company
- Established 1878
- Operated at Joadja (main site), Airly, and near Katoomba
- Later known as "A.K.O." or "Australian Kerosene Oil Company" (from 1891)
- Wound up in 1906

### Katoomba Coal and Shale Company
- Formed 1885 by John Britty North
- Operated coal mines at Orphan Rock and shale mines at Ruined Castle
- Famous for "Flying Fox" tramway disaster
- Went into liquidation in 1892
- Operations leased by Australian Kerosene Oil and Mineral Company in 1891

### South Clifton
- Coal mining operation near Wollongong
- South Clifton Mine Company (the company)
- South Clifton Tunnel Mine (the physical mine)

---

*Generated with Claude Code - 2025-10-30*
