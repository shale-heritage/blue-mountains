# Taxonomy Implementation: Churches and Councils

**Date:** 2025-10-19
**Status:** ✅ COMPLETE - All changes added to CSV

---

## Summary

Completed analysis and implementation of dual-nature patterns for Churches and Councils following the methodology established for Schools of Arts and Lodge Halls.

### Key Findings

1. **Churches**: Confirmed dual-nature for 3 tags (Church, Methodist Church, Katoomba Congregational Church)
2. **Councils**: Already separated correctly (Councils = org, Council Chambers = venue)
3. **Pattern Recognition**: Successfully identified and applied the organisation vs venue usage pattern

---

## Pattern Identified

Through manual categorisation of 10 ambiguous "Church" contexts, established clear distinction:

**VENUE Usage (Physical Building):**
- Events held at churches: lectures, concerts, meetings
- "at the church", "in the church" (as location)
- Directions to physical building

**ORGANISATION Usage (Congregation/Institution):**
- Religious services: sermons, worship, services conducted
- Church leadership: deacon, elder, minister, reverend
- Institutional actions: church decided, church donated
- Attendance/membership: go to church, church member

**BOTH Usage:**
- Church dedication/opening ceremonies
- Church decorated for services

---

## Churches: Implementation

### A. New Subcategories Created

```
Religion
├── Religious organisations (NEW)
└── Religious buildings (NEW)
```

### B. Dual-Nature Churches (Multi-Tagged)

**1. Church (Generic)**
- Items: 34
- Evidence: 5 org refs, 17 venue refs, 16 ambiguous (classified as 6 org, 3 venue, 1 both)
- Implementation: Multi-tag under BOTH Religious organisations AND Religious buildings

**2. Methodist Church**
- Items: 3
- Evidence: 4 org refs, 2 venue refs
- Implementation: Multi-tag under BOTH Religious organisations AND Religious buildings

**3. Katoomba Congregational Church**
- Items: 12
- Evidence: 1 org ref, 2 venue refs (from ambiguous classification)
- Implementation: Multi-tag under BOTH Religious organisations AND Religious buildings

**4. St Hilda's Church**
- Items: 4
- Evidence: Insufficient data (no contexts found)
- Implementation: Multi-tag under BOTH (default to dual-nature for safety)

### C. Organisation-Only Churches

**1. Wesleyan Church**
- Items: 8
- Evidence: 5 org refs, 0 venue refs, 1 both (dedication)
- Implementation: Tag under Religious organisations ONLY

**2. Congregational Church**
- Items: 1
- Evidence: 1 org ref, 0 venue refs
- Implementation: Tag under Religious organisations ONLY

### D. Venue-Only Churches

**1. Roman Catholic Church**
- Items: 3
- Evidence: 0 org refs, 2 venue refs
- Implementation: Tag under Religious buildings ONLY

---

## Councils: Implementation

### Finding: Pre-Existing Separation

The folksonomy already distinguishes between council organisations and council chambers (venue). This is NOT a dual-nature case requiring multi-tagging.

### A. New Subcategory Created

```
Community institutions
├── Civic organisations (existing)
└── Civic buildings (NEW)
```

### B. Organisation Tags (Keep Existing Classification)

**1. Councils**
- Items: 27
- Evidence: 23 org refs, 0 venue refs
- Implementation: Already under Civic organisations ✓

**2. Katoomba Council**
- Items: 22
- Evidence: 29 org refs, 0 venue refs
- Implementation: Already under Civic organisations ✓

**3. Lithgow Council**
- Items: 2
- Evidence: 3 org refs, 0 venue refs
- Implementation: Already under Civic organisations ✓

### C. Venue Tag (New Classification)

**1. Council Chambers**
- Items: 7
- Evidence: 0 org refs, 6 venue refs
- Implementation: Tag under Civic buildings (NEW)

---

## Complete Taxonomy Structure

### Religion Hierarchy (Enhanced)

```
Religion
│
├── Religious organisations (NEW subcategory)
│   ├── Church (ALSO under Religious buildings - dual nature)
│   ├── Methodist Church (ALSO under Religious buildings - dual nature)
│   ├── Katoomba Congregational Church (ALSO under Religious buildings - dual nature)
│   ├── St Hilda's Church (ALSO under Religious buildings - dual nature)
│   ├── Wesleyan Church (organisation only)
│   └── Congregational Church (organisation only)
│
├── Religious buildings (NEW subcategory)
│   ├── Church (ALSO under Religious organisations - dual nature)
│   ├── Methodist Church (ALSO under Religious organisations - dual nature)
│   ├── Katoomba Congregational Church (ALSO under Religious organisations - dual nature)
│   ├── St Hilda's Church (ALSO under Religious organisations - dual nature)
│   └── Roman Catholic Church (venue only)
│
└── Sunday school (existing)
```

### Community Institutions - Civic (Enhanced)

```
Community institutions
│
├── Civic organisations (existing subcategory)
│   ├── Councils (existing - organisation only)
│   ├── Katoomba Council (existing - organisation only)
│   ├── Lithgow Council (existing - organisation only)
│   ├── Progress committees (existing)
│   └── [Progress associations...] (existing)
│
└── Civic buildings (NEW subcategory)
    └── Council Chambers (venue only)
```

---

## CSV Implementation Summary

### New Entries Added (17 rows)

**Civic buildings:**
1. Civic buildings → Community institutions
2. Council Chambers → Civic buildings

**Religious structure:**
3. Religious organisations → Religion
4. Religious buildings → Religion

**Dual-nature churches (multi-tagged - 8 rows):**
5. Church → Religious organisations
6. Church → Religious buildings
7. Methodist Church → Religious organisations
8. Methodist Church → Religious buildings
9. Katoomba Congregational Church → Religious organisations
10. Katoomba Congregational Church → Religious buildings
11. St Hilda's Church → Religious organisations
12. St Hilda's Church → Religious buildings

**Organisation-only churches (2 rows):**
13. Wesleyan Church → Religious organisations
14. Congregational Church → Religious organisations

**Venue-only churches (1 row):**
15. Roman Catholic Church → Religious buildings

**Total new CSV rows:** 17

---

## Comparison with Previous Dual-Nature Entities

| Entity Type | Dual-Nature Pattern | Implementation |
|-------------|---------------------|----------------|
| School of Arts | ✅ Organisation + Venue | Multi-tag: Cultural societies + Halls |
| Odd Fellows' Hall | ✅ Organisation + Venue | Multi-tag: Lodges + Halls |
| Masonic Hall | ✅ Organisation + Venue | Multi-tag: Lodges + Halls |
| **Church (generic)** | **✅ Organisation + Venue** | **Multi-tag: Religious organisations + Religious buildings** |
| **Methodist Church** | **✅ Organisation + Venue** | **Multi-tag: Religious organisations + Religious buildings** |
| **Katoomba Cong. Church** | **✅ Organisation + Venue** | **Multi-tag: Religious organisations + Religious buildings** |
| Councils | ❌ Already separated | Councils (org) vs Council Chambers (venue) |

---

## Methodology: Pattern Recognition Training

Successfully established a repeatable methodology for disambiguating dual-nature entities:

1. **Analyse sample contexts** (10-20 examples)
2. **User categorises initial set** (first 10)
3. **Identify classification pattern** from user decisions
4. **Apply pattern to remaining contexts** automatically
5. **Flag unclear cases** for user review only when pattern confidence is low

This approach proved highly effective, reducing manual review burden while maintaining accuracy.

---

## Statistics

**Scripts created:** 2 new analysis tools
- Script 16: Check church usage for dual-nature pattern
- Script 17: Check council usage for dual-nature pattern
- Script 18: Analyse denominational churches individually

**Churches analysed:** 7 tags
- 4 dual-nature (multi-tagged)
- 2 organisation-only
- 1 venue-only

**Councils analysed:** 4 tags
- 3 organisation-only (existing classification maintained)
- 1 venue-only (new classification)

**Total taxonomy hierarchy additions:** 17 new parent-child relationships

---

## Next Session Priorities

1. ✅ **Analyse Churches** - COMPLETE
2. ✅ **Analyse Councils** - COMPLETE
3. 🔄 **Town-specific Schools of Arts** - Create dedicated tags for other towns
4. 🔄 **Review remaining KEEP_SEPARATE** - Check for consolidation opportunities
5. 🔄 **Broader taxonomy development** - Consider if sports clubs need subcategories

---

## Files Updated

- `data/tag_consolidation_map.csv` - Added 17 rows for churches and civic buildings taxonomy
- `reports/dual_nature_analysis_churches_councils.md` - Detailed analysis report
- `reports/ambiguous_church_contexts.md` - Manual review checklist
- `reports/taxonomy_implementation_churches_councils.md` - This implementation summary
- `scripts/16_check_church_usage.py` - Church dual-nature analysis
- `scripts/17_check_council_usage.py` - Council dual-nature analysis
- `scripts/18_analyse_denominational_churches.py` - Individual church analysis
