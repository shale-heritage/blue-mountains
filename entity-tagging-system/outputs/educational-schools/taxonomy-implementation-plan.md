# Educational Schools Taxonomy Implementation Plan

**Date:** 2025-11-14
**Entity Type:** Educational schools (public schools)
**Strategy:** Disambiguation with parenthetical qualifiers (following hotel/church model)

---

## Current Taxonomy Issues

1. **No dual-nature structure**: Schools currently only appear in Built Environment facet
2. **Case-variant duplication**: "School"/"school" and "Schools"/"schools" duplicates
3. **No disambiguation**: Generic "School" doesn't distinguish building vs organisation usage
4. **Specific schools lack qualifiers**: Named schools (Katoomba Public School, etc.) lack building/organisation distinction

---

## Classification Results Summary

**Total unique mentions:** 23
- Building only: 4 (17.4%)
- Organisation only: 15 (65.2%)
- Both: 4 (17.4%)

**Entity breakdown:**
- Katoomba Public School: 5 mentions (1 building, 2 organisation, 2 both)
- Katoomba Superior Public School: 6 mentions (1 building, 4 organisation, 1 both)
- Megalong Valley School: 0 mentions (tagged but no text extracted)
- Mount Victoria School: 0 mentions (tagged but no text extracted)
- Generic "School": 12 mentions (2 building, 9 organisation, 1 both)

---

## Proposed Taxonomy Structure

### Facet: Built Environment > Educational buildings

```text
educational buildings (parent)
├── schools (buildings) (intermediate parent - NEW)
    ├── School (building) (singular generic leaf - NEW)
    ├── Katoomba Public School (building) (specific leaf - NEW)
    ├── Katoomba Superior Public School (building) (specific leaf - NEW)
    ├── Megalong Valley School (building) (specific leaf - NEW)
    └── Mount Victoria School (building) (specific leaf - NEW)
```

### Facet: Agents > Organisations > Educational institutions

```text
organisations (parent)
├── educational institutions (intermediate parent - EXISTS)
    ├── schools (organisations) (intermediate parent - NEW)
        ├── School (organisation) (singular generic leaf - NEW)
        ├── Katoomba Public School (organisation) (specific leaf - NEW)
        ├── Katoomba Superior Public School (organisation) (specific leaf - NEW)
        ├── Megalong Valley School (organisation) (specific leaf - NEW)
        └── Mount Victoria School (organisation) (specific leaf - NEW)
```

---

## CSV Changes Required

### Remove (obsolete unqualified entries)

```csv
School,School,hierarchy,parent=Schools
school,school,hierarchy,parent=schools
Katoomba Public School,Katoomba Public School,hierarchy,parent=schools
Katoomba Public School,Katoomba Public School,hierarchy,parent=Schools
Katoomba Superior Public School,Katoomba Superior Public School,hierarchy,parent=schools
Katoomba Superior Public School,Katoomba Superior Public School,hierarchy,parent=Schools
Megalong Valley School,Megalong Valley School,hierarchy,parent=schools
Megalong Valley School,Megalong Valley School,hierarchy,parent=Schools
Mount Victoria School,Mount Victoria School,hierarchy,parent=schools
Mount Victoria School,Mount Victoria School,hierarchy,parent=Schools
Schools,Schools,hierarchy,parent=Educational buildings
schools,schools,hierarchy,parent=educational buildings
```

### Add (new disambiguated structure)

**Intermediate parents:**
```csv
schools (buildings),schools (buildings),hierarchy,parent=educational buildings
schools (organisations),schools (organisations),hierarchy,parent=educational institutions
```

**Plural parent category (organisational only - retaining polyhierarchy for browsing):**
```csv
Schools,Schools,hierarchy,parent=Educational institutions
Schools,Schools,hierarchy,parent=Educational buildings
```

**Synonym mappings for unqualified generic terms:**
```csv
School,School (organisation),synonym,Unqualified variant - most usage is organisational (65.2%)
school,school (organisation),synonym,Lowercase variant - maps to organisation as primary
```

**Singular generic leaves:**
```csv
School (building),School (building),hierarchy,parent=schools (buildings)
School (organisation),School (organisation),hierarchy,parent=schools (organisations)
school (building),school (building),hierarchy,parent=schools (buildings)
school (organisation),school (organisation),hierarchy,parent=schools (organisations)
```

**Specific named entities with disambiguation:**
```csv
Katoomba Public School (building),Katoomba Public School (building),hierarchy,parent=schools (buildings)
Katoomba Public School (organisation),Katoomba Public School (organisation),hierarchy,parent=schools (organisations)
Katoomba Superior Public School (building),Katoomba Superior Public School (building),hierarchy,parent=schools (buildings)
Katoomba Superior Public School (organisation),Katoomba Superior Public School (organisation),hierarchy,parent=schools (organisations)
Megalong Valley School (building),Megalong Valley School (building),hierarchy,parent=schools (buildings)
Megalong Valley School (organisation),Megalong Valley School (organisation),hierarchy,parent=schools (organisations)
Mount Victoria School (building),Mount Victoria School (building),hierarchy,parent=schools (buildings)
Mount Victoria School (organisation),Mount Victoria School (organisation),hierarchy,parent=schools (organisations)
```

**Unqualified name synonyms (to be determined based on evidence):**
```csv
Katoomba Public School,Katoomba Public School (organisation),synonym,Unqualified variant - to be applied based on context
Katoomba Superior Public School,Katoomba Superior Public School (organisation),synonym,Unqualified variant - to be applied based on context
Megalong Valley School,Megalong Valley School (organisation),synonym,Unqualified variant - to be applied based on context (no data to classify)
Mount Victoria School,Mount Victoria School (organisation),synonym,Unqualified variant - to be applied based on context (no data to classify)
```

---

## Rationale for Decisions

### Why "organisation" as default for unqualified "School"?

Classification data shows 65.2% of generic "School" mentions are organisational only, compared to 17.4% building only. When context is ambiguous, organisational interpretation is statistically more likely.

### Why keep "Schools" as polyhierarchical parent?

Following the pattern established for other dual-nature entities, the plural parent "Schools" appears in both facets to allow hierarchical browsing. The leaf-node tagging pattern means this is never directly applied to items.

### Why synonym mapping for unqualified specific names?

Similar to hotels approach: unqualified "Katoomba Public School" maps to the more common aspect (organisation) as default, but cataloguers can override with explicit `(building)` qualifier when context clearly indicates physical structure.

---

## Item Retagging Strategy

### Phase 1: Replace unqualified generic tags

All items currently tagged with "School" or "school" (without qualifiers):
- Apply classification from analysis
- 12 unique mentions to retag based on classification results

### Phase 2: Replace specific school tags

All items currently tagged with specific school names:
- Katoomba Public School: 6 items (5 mentions classified)
- Katoomba Superior Public School: 8 items (6 mentions classified)
- Megalong Valley School: 6 items (no mentions in extraction - needs manual review)
- Mount Victoria School: 1 item (no mentions in extraction - needs manual review)

### Phase 3: Fix School of Arts misclassifications

3 items incorrectly tagged as "School" should be retagged to "School of Arts":
- Item: Mountain Mixtures (1892-11-25) - Katoomba School of Arts Flower Show
- Item: Town Talk (1903-03-13) - School of Arts committee meeting
- Item: Town Talk (1904-05-13) - School of Arts membership canvass

---

## Data Quality Issues to Address

### Duplicate Tag Applications (12 duplicates)

Items are tagged with both "School" AND "school" (case variants) - consolidate to single qualified tag

### Missing Context for Some Tagged Items

- Megalong Valley School: 6 items tagged, but no mention text extracted
- Mount Victoria School: 1 item tagged, but no mention text extracted

These require manual review or re-extraction to determine building vs organisation classification.

---

## Implementation Steps

1. ✅ Update classification results with user corrections (Mention 22: building → both)
2. 🔄 **Create backup of tag_map_consolidated.csv**
3. ⏳ Apply taxonomy structure changes to CSV
4. ⏳ Generate item_tag_application.csv with all retagging instructions
5. ⏳ Document decisions in planning/consolidation-decisions.md
6. ⏳ Apply tags to Zotero library (separate step after validation)

---

## Files Generated

- `data/entity_classification/educational-schools_mentions.json` - Raw mention extractions
- `data/entity_classification/educational-schools_classification_prompt.txt` - Classification prompt
- `data/entity_classification/educational-schools_classification_results.md` - Full classification with user corrections
- `entity-tagging-system/outputs/educational-schools/taxonomy-implementation-plan.md` - This file
- (Pending) `entity-tagging-system/outputs/educational-schools/item_tag_application.csv` - Retagging instructions

---

**Status:** Ready for taxonomy CSV implementation
**Next Action:** Create backup and apply CSV changes
