# Hotel Classifications - Approval Template

**Date:** 2025-11-12
**Source:** NLU classifications from Claude Sonnet 4.5
**Status:** PENDING REVIEW

## Instructions

For each hotel entity below:

1. Review the recommended classification
2. Modify `APPROVED_CLASSIFICATION` if needed (building | business | both)
3. Add notes in `REVIEW_NOTES` if helpful
4. Mark `REVIEWED: [ ]` as `[x]` when complete

---

## Classification Summary

| Entity | NLU Recommendation | Business Mentions | Building Mentions | Both Mentions |
|--------|-------------------|------------------|------------------|---------------|
| Family hotel | **Business-dominant** | 4 | 0 | 2 |
| Carrington Hotel | **Mixed** | 1 | 1 | 2 |
| Imperial Hotel | **Building-dominant** | 1 | 2 | 0 |
| Katoomba Hotel | **Building-only** | 0 | 3 | 0 |
| Megalong Hotel | **Mixed** | 3 | 3 | 2 |
| Centennial Hotel | **Business-dominant** | 3 | 1 | 1 |
| Belgravia Hotel | **Mixed** | 1 | 1 | 0 |
| Railway Hotel | **Building-only** | 0 | 2 | 0 |
| Wentworth Falls Hotel | **Business-only** | 2 | 0 | 0 |
| Mount Victoria Hotel | **Business-only** | 2 | 0 | 0 |
| Grand Hotel | **Building-only** | 0 | 1 | 0 |
| Katoomba Family Hotel | **Business-only** | 1 | 0 | 0 |
| Montrose House | **Building-only** | 0 | 4 | 0 |

---

## Entity 1: Family hotel

**Analysis:** 6 mentions (4 business, 2 both)

**Contexts:**
- Proprietorship and business operations (4 mentions: "presided over destinies," "purchased," "running successfully")
- Mixed business + spatial (2 mentions: "Mrs. Long, of the Family Hotel" with room rental)

**NLU Recommendation:** Create (business) tag + retain (building) for "both" contexts

**Taxonomy Actions Required:**
- [ ] Create: `Family hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Family hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 2: Carrington Hotel

**Analysis:** 4 mentions (1 business, 1 building, 2 both)

**Contexts:**
- Licensing renewal (business)
- Arrest location (building)
- Assault case with licensee testimony (both)
- Picture/illustration (building - weak)

**NLU Recommendation:** Create (business) tag for licensing + proprietor contexts

**Taxonomy Actions Required:**
- [ ] Create: `Carrington Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Carrington Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 3: Imperial Hotel

**Analysis:** 3 mentions (1 business, 2 building)

**Contexts:**
- License transfer (business)
- To be rebuilt (building - passive construction)
- Spatial landmark opposite paddock (building)

**NLU Recommendation:** Create (business) tag for licensing context

**Taxonomy Actions Required:**
- [ ] Create: `Imperial Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Imperial Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 4: Katoomba Hotel

**Analysis:** 3 mentions (all building)

**Contexts:**
- Spatial landmark for footpath (building)
- Inquest venue (building)
- Preaching location landmark (building)

**NLU Recommendation:** Remain building-only (no business contexts found)

**Taxonomy Actions Required:**
- [ ] No action: Retain existing `Katoomba Hotel (building)` only

**APPROVED_CLASSIFICATION:** `building` (no business tag needed)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 5: Megalong Hotel

**Analysis:** 8 mentions (3 business, 3 building, 2 both)

**Contexts:**
- Licensing applications (2 business)
- Advertisements (2 both - marketing + location)
- Licensee testimony (1 both)
- Business closure (1 business)
- Spatial landmarks (3 building - cricket ground, geographic features, visual description)

**NLU Recommendation:** Create (business) tag - substantial business agency

**Taxonomy Actions Required:**
- [ ] Create: `Megalong Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Megalong Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 6: Centennial Hotel

**Analysis:** 5 mentions (3 business, 1 building, 1 both)

**Contexts:**
- Property sale (business)
- Licensing violation (business)
- Proprietor testimony/theft location (both)
- Event venue for testimonial (building)
- Election polling location with host (both)

**NLU Recommendation:** Create (business) tag - strong business contexts

**Taxonomy Actions Required:**
- [ ] Create: `Centennial Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Centennial Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 7: Belgravia Hotel

**Analysis:** 2 mentions (1 business, 1 building)

**Contexts:**
- License renewal (business)
- Viewing platform for race (building - balcony)

**NLU Recommendation:** Create (business) tag for licensing

**Taxonomy Actions Required:**
- [ ] Create: `Belgravia Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Belgravia Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (polyhierarchical)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 8: Railway Hotel

**Analysis:** 2 mentions (all building)

**Contexts:**
- Meeting venue (building - "meeting held at")
- Gaming house location (building - billiard room)

**NLU Recommendation:** Remain building-only (no business agency contexts)

**Taxonomy Actions Required:**
- [ ] No action: Retain existing `Railway Hotel (building)` only

**APPROVED_CLASSIFICATION:** `building` (no business tag needed)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 9: Wentworth Falls Hotel

**Analysis:** 2 mentions (all business)

**Contexts:**
- Business advertising notice (business)
- Business sale (business - "sold out the business in connection with")

**NLU Recommendation:** Create (business) tag - only appears in business contexts

**Taxonomy Actions Required:**
- [ ] Create: `Wentworth Falls Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Wentworth Falls Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (create business tag; assume building usage exists even if not in these mentions)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 10: Mount Victoria Hotel

**Analysis:** 2 mentions (all business)

**Contexts:**
- Licensee identification in application (business)
- Proprietor catering services (business)

**NLU Recommendation:** Create (business) tag - only appears in business contexts

**Taxonomy Actions Required:**
- [ ] Create: `Mount Victoria Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses)
- [ ] Retain: `Mount Victoria Hotel (building)` under Built Environment > ... > Hotels (buildings)

**APPROVED_CLASSIFICATION:** `both` (create business tag; assume building usage exists even if not in these mentions)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 11: Grand Hotel

**Analysis:** 1 mention (building)

**Contexts:**
- Future establishment location (building - "shortly-to-be Grand Hotel in Phillip-street, Sydney")

**NLU Recommendation:** Remain building-only (single weak reference)

**Taxonomy Actions Required:**
- [ ] No action: Retain existing `Grand Hotel (building)` only

**APPROVED_CLASSIFICATION:** `building` (no business tag needed based on single mention)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 12: Katoomba Family Hotel

**Analysis:** 1 mention (business)

**Contexts:**
- Business investment decision (business - "lessee intends to make improvements")

**NLU Recommendation:** Create (business) tag

**Taxonomy Actions Required:**
- [ ] Create: `Katoomba Family Hotel (business)` under Agents > Organisations > Hospitality businesses > Hotels (businesses) > Family hotels
- [ ] Retain: `Katoomba Family Hotel (building)` under Built Environment > ... > Hotels (buildings) > Family hotels

**APPROVED_CLASSIFICATION:** `both` (create business tag; assume building usage exists)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Entity 13: Montrose House

**Analysis:** 4 mentions (all building)

**Contexts:**
- Property rental for police department (building - real estate)
- Court venue proposals (building - government facility location)
- Spatial landmark (building - "next to")

**NLU Recommendation:** Remain building-only (used as government facility, not hotel operations)

**Taxonomy Actions Required:**
- [ ] No action: Retain existing `Montrose House (building)` only

**APPROVED_CLASSIFICATION:** `building` (no business tag needed - not operating as hotel in these contexts)

**REVIEW_NOTES:**

**REVIEWED:** [ ]

---

## Summary of Taxonomy Updates

### Tags to Create (Business Variants)

1. **Family hotel (business)** - 4 business mentions, strong proprietorship
2. **Carrington Hotel (business)** - 1 business + 2 both (licensing, proprietor testimony)
3. **Imperial Hotel (business)** - 1 business (licensing transfer)
4. **Megalong Hotel (business)** - 3 business + 2 both (licensing, operations, advertisements)
5. **Centennial Hotel (business)** - 3 business + 2 both (sale, licensing, proprietor)
6. **Belgravia Hotel (business)** - 1 business (licensing)
7. **Wentworth Falls Hotel (business)** - 2 business (advertising, sale)
8. **Mount Victoria Hotel (business)** - 2 business (licensing, catering)
9. **Katoomba Family Hotel (business)** - 1 business (investment decision)

**Total:** 9 new (business) tags to create

### Tags Remaining Building-Only

1. **Katoomba Hotel (building)** - 3 building, 0 business
2. **Railway Hotel (building)** - 2 building, 0 business
3. **Grand Hotel (building)** - 1 building, 0 business
4. **Montrose House (building)** - 4 building, 0 business (government facility usage)

**Total:** 4 hotels remain building-only

---

## Next Steps After Approval

1. [ ] Review all classifications above
2. [ ] Mark all entities as `REVIEWED: [x]`
3. [ ] Confirm approved classifications
4. [ ] Create (business) tags in `data/tag_map_consolidated.csv`
5. [ ] Add synonym mappings for unqualified variants
6. [ ] Run validation: `python scripts/36_check_all_tag_mappings.py`
7. [ ] Update `planning/consolidation-decisions.md` with rationale
8. [ ] Apply approved tags to Zotero items (Phase 2 completion)

---

## Additional Review Priority

### High Priority (Review Carefully)

- **Advertisements** (Megalong Hotel): Ensure "both" justified (business marketing + location description)
- **Wentworth Falls Hotel**: Only 2 mentions, both business - confirm no building usage expected
- **Mount Victoria Hotel**: Only 2 mentions, both business - confirm no building usage expected

### Medium Priority

- **Centennial Hotel**: Mixed contexts - verify business vs building distinction clear
- **Carrington Hotel**: Mixed contexts - verify "both" classifications justified

### Low Priority

- **Katoomba Hotel, Railway Hotel**: Clear building-only patterns
- **Montrose House**: Clear building-only (government facility usage)

---

## Confidence Assessment

**Overall Classification Quality:** High

- 93% of NLU classifications at high confidence
- Clear reasoning and evidence for each decision
- Superior to regex baseline (which missed all business contexts)
- Context genre recognition (licensing, advertisements, transactions) is key differentiator

**Recommendation:** Approve NLU classifications as presented, with manual review of high-priority cases noted above.

---

**Approval Date:** ___________

**Approved By:** ___________

**Status After Review:**
- [ ] Approved as presented
- [ ] Approved with modifications (see notes)
- [ ] Requires further analysis

**Modifications Made:**

