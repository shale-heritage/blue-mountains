# {ENTITY_TYPE} Classification Results

**Date:** {DATE}
**Entity Type:** {ENTITY_TYPE_FORMAL}
**Classification Method:** NLU (Natural Language Understanding) via entity-classifier skill
**Total Items Analysed:** {TOTAL_COUNT}

---

## Classification Summary

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | {BUILDING_COUNT} | {BUILDING_PCT}% |
| Business/Organisation only | {BUSINESS_COUNT} | {BUSINESS_PCT}% |
| Both | {BOTH_COUNT} | {BOTH_PCT}% |
| **Total** | **{TOTAL_COUNT}** | **100%** |

---

## Detailed Analysis

**Note:** Each mention includes human review section. See `classification-mention-template.md` for format specification.

{MENTION_ANALYSES}

**Format for each mention:**
```
### Mention N: Descriptive Title
[Entity details, context, classification, reasoning]

---

**HUMAN REVIEW:**
- [ ] Confirm classification
- [ ] Change to: [ ] building  [ ] organisation  [ ] both

**Notes:**


**Additional/Alternative Tags:**


---
```

---

## Pattern Analysis

### Building Indicators

{BUILDING_PATTERNS}

### Business/Organisation Indicators

{BUSINESS_PATTERNS}

### Dual-Nature Indicators (Both)

{BOTH_PATTERNS}

---

## Taxonomy Implications

### Current Taxonomy Structure

```
{CURRENT_TAXONOMY}
```

### Recommended Structure

```
{RECOMMENDED_TAXONOMY}
```

### Required Changes

{TAXONOMY_CHANGES}

---

## Specific Establishments Identified

{SPECIFIC_ESTABLISHMENTS}

---

## Item Tag Application

**Action Required:** Update {TAG_APPLICATION_COUNT} Zotero items with qualified tags

**Application CSV:** `entity-tagging-system/outputs/{entity-type}/item_tag_application.csv`

**Summary:**
- Replace generic tags: {REPLACE_COUNT}
- Add specific establishments: {ADD_SPECIFIC_COUNT}
- Remove mis-tagged items: {REMOVE_COUNT}

---

## Comparison with Other Entity Types

| Entity Type | Building % | Business/Org % | Both % | Dominant Pattern |
|-------------|------------|----------------|--------|------------------|
| {ENTITY_TYPE} | {BUILDING_PCT}% | {BUSINESS_PCT}% | {BOTH_PCT}% | {DOMINANT_PATTERN} |
| Hotels | 43% | 25% | 32% | Building-dominant |
| Educational Schools | 17.2% | 58.6% | 24.1% | Organisation-dominant |
| Boarding Houses | 12.5% | 50% | 37.5% | Business-dominant |
| Churches | 29% | 29% | 42% | Dual-nature dominant |

---

## Methodology Notes

**Linguistic Heuristic Framework:**

- **Spatial indicators** → Building classification
  - Locative prepositions (at, in, near)
  - Events occurring at location
  - Physical descriptions
  - Construction/renovation references

- **Agency indicators** → Business/Organisation classification
  - Ownership and management
  - Financial operations
  - Service provision
  - Membership and subscriptions
  - Committee meetings and governance

- **Both** → When single mention contains both spatial and agency indicators

**Confidence:** {CONFIDENCE_LEVEL}

---

## Next Steps

1. **Review classifications** - Verify accuracy of analysis
2. **Implement taxonomy** - Run script to update tag_map_consolidated.csv
3. **Apply Zotero tags** - Use item_tag_application.csv to retag items
4. **Document decision** - Add to planning/consolidation-decisions.md

---

## Files Generated

- **Classification results:** `entity-tagging-system/outputs/{entity-type}/{entity-type}_classification_results.md`
- **Item mentions:** `data/entity_classification/{entity-type}_mentions.json`
- **Classification prompt:** `data/entity_classification/{entity-type}_classification_prompt.txt`
- **Tag application CSV:** `entity-tagging-system/outputs/{entity-type}/item_tag_application.csv`
- **Taxonomy implementation script:** `scripts/{SCRIPT_NUMBER}_implement_{entity-type}_taxonomy.py`

---

## Version History

- **{DATE}**: Initial classification completed using entity-classifier skill v1.0
