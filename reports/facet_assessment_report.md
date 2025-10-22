# Facet Assessment Report - Tag Cleaning Issues

**Generated:** 2025-10-20
**Purpose:** Systematic assessment of remaining primary facets for cleaning

---

## Summary Statistics

- **Total tags analyzed:** 401
- **Similar tag pairs found:** 32
- **Singular/plural inconsistencies:** 7
- **Parents with many children (>10):** 2
- **Potential building tags:** 8
- **Company name issues:** 0

---

## 1. Similar Tags (Potential Synonyms/Variants)

**Issue:** Tags with similar names may be variants, abbreviations, or synonyms.

**Action needed:** Review each pair to determine if MERGE or KEEP SEPARATE.

| Tag 1 | Tag 2 | Similarity | Notes |
|-------|-------|------------|-------|
| Transport & Infrastructure | Transport infrastructure | 0.96 | |
| Rifle club | Rifle clubs | 0.95 | |
| Coroner | Coroners | 0.93 | |
| School | Schools | 0.92 | |
| Choir | Choirs | 0.91 | |
| Court | Courts | 0.91 | |
| Alcohol & Temperance | Temperance | 0.90 | |
| Communications & Postal Services | Post | 0.90 | |
| Environment & Weather | Weather | 0.90 | |
| Great Western Railway | Railway | 0.90 | |
| Katoomba Public School | Pub | 0.90 | |
| Katoomba Public School | School | 0.90 | |
| Katoomba Rifle Reserves | Reserves | 0.90 | |
| Katoomba School of Arts | School | 0.90 | |
| Katoomba School of Arts | School of Arts | 0.90 | |
| Katoomba Superior Public School | Pub | 0.90 | |
| Katoomba Superior Public School | School | 0.90 | |
| Katoomba Tennis Club | Tennis | 0.90 | |
| Lawn Tennis Club | Tennis | 0.90 | |
| Megalong Valley School | School | 0.90 | |
| Mount Victoria School | School | 0.90 | |
| Band | Bands | 0.89 | |
| Mount Victoria Hotel | Mount Victoria School | 0.88 | |
| Mining accidents | Mining incidents | 0.88 | |
| Mount Victoria Hall | Mount Victoria Hotel | 0.87 | |
| Cultural events | Cultural venues | 0.87 | |
| Nellie's Glen Road | Nellie's Glen track | 0.86 | |
| Church | Churches | 0.86 | |
| Licensing Act | Licensing Court | 0.86 | |
| Pub | Pubs | 0.86 | |

*...and 2 more pairs*

---

## 2. Singular/Plural Inconsistencies

**Issue:** Tags have both singular and plural forms.

**Action needed:** Determine if these should be merged or kept separate based on usage.

| Singular | Plural | Parent Context |
|----------|--------|----------------|
| Band | Bands | S: Bands<br>P: Performance groups |
| Choir | Choirs | S: Choirs<br>P: Performance groups |
| Coroner | Coroners | S: Coroners<br>P: Legal officials (intermediate facet |
| Court | Courts | S: Courts<br>P: Justice & Crime - THEMATIC |
| Pub | Pubs | S: Pubs<br>P: Alcohol-related venues - THEMATIC |
| Rifle club | Rifle clubs | S: Rifle clubs<br>P: Sports clubs |
| School | Schools | S: Schools<br>P: Educational buildings |

---

## 3. Potential Missing Intermediate Facets

**Issue:** Parents with >10 direct children may need intermediate facets.

**Action needed:** Review to determine if intermediate categorisation is needed.

| Parent Tag | # Children | Sample Children (first 5) |
|------------|------------|---------------------------|
| (thematic grouping | 20 | Health & Medicine, Education, Religion, Justice & Crime, Mining & Industry, ...and 15 more |
| Hotels | 18 | Megalong Hotel, Mount Victoria Hotel, Mrs Long's Hotel, Family Hotel, Belgravia Hotel, ...and 13 more |

---

## 4. Potential Buildings Miscategorized as Organizations

**Issue:** Tags ending in building-related terms may be physical structures.

**Action needed:** Verify if these should be in Built Environment facet.

| Tag | Indicator | Current Parent | Notes |
|-----|-----------|----------------|-------|
| Hoffman's House | House | Hotels | |
| Montrose House | House | Hotels | |
| Masonic Hall | Hall | Halls | |
| Odd Fellows' Hall | Hall | Halls | |
| Council Chambers | Chambers | Council buildings | |
| Mount Victoria Hall | Hall | Halls | |
| Waudby's Hall | Hall | Halls | |
| Clarke's Hall | Hall | Halls | |

---

## 5. Company Name Standardization Issues

**Issue:** Company names need standardization (spell out Co./&, drop Ltd.).

**Action needed:** Apply standardization pattern established in Phase 1.

✅ No company name issues found.

---

## Priority Recommendations

### HIGH Priority

- **Review 7 singular/plural pairs** (may indicate inconsistency)

### MEDIUM Priority

- **Review 8 potential building tags** (verify categorization)
- **Review 2 parents with many children** (consider intermediate facets)

### LOW Priority

- **Review 32 similar tag pairs** (may be legitimate distinct tags)

---

## Next Steps

1. Manual spot-check flagged tags with primary sources (scripts 24-27 pattern)
2. Apply batch corrections to `scripts/22_generate_poly_hierarchy.py`
3. Create variant merge CSVs for any new synonyms
4. Regenerate poly-hierarchy CSV and visualizations
5. Validate all corrections with validation report

---

**Assessment completed by:** Claude Code  
**Date:** 2025-10-20
