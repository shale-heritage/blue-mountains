# Naming Variants Review

**Generated:** 2025-10-19

This document reviews 6 naming variant pairs to determine if they represent the same entity or are distinct.

---

## Review Approach

For each pair, we need to determine:

1. **Same entity?** → MERGE (consolidate to one canonical form)
2. **Related but distinct?** → HIERARCHY (parent-child relationship)
3. **Completely different?** → KEEP_SEPARATE

**Key principle:** When uncertain, default to KEEP_SEPARATE and flag for future review.

---

## Pair 1: "Katoomba South" vs "South Katoomba"

**Usage:** Katoomba South (9 items) vs South Katoomba (10 items)

**Analysis:**
- Very similar usage counts (9 vs 10)
- Same words in different order
- Could be:
  - **Same location** with naming inconsistency (user tagging variation)
  - **Different areas** (e.g., "Katoomba South" as district vs "South Katoomba" as geographic descriptor)

**Historical Context Question:**
- In 19th/early 20th century Blue Mountains, was there an official locality called "South Katoomba"?
- Or is this simply "the southern part of Katoomba"?

**Proposed Decision:** **MERGE** → South Katoomba (more natural phrasing)

**Rationale:** Likely the same geographic area with user tagging inconsistency. "South Katoomba" is more natural Australian English phrasing. However, **recommend checking 1-2 items from each tag** to confirm they refer to the same area.

**Alternative:** If they prove to be distinct areas, KEEP_SEPARATE.

---

## Pair 2: "Katoomba Superior Public School" vs "Katoomba Public School"

**Usage:** Katoomba Superior Public School (8 items) vs Katoomba Public School (6 items)

**Analysis:**
- "Superior Public School" was a specific classification in NSW education system
- Superior schools provided education beyond primary level (roughly equivalent to early high school)
- Could be:
  - **Same school** that was reclassified (e.g., became "Superior" in later period)
  - **Different institutions** operating concurrently
  - **Same school** where taggers used shortened name inconsistently

**Historical Context Question:**
- Did Katoomba have one school that was upgraded to "Superior" status?
- Or did it have both a Public School AND a Superior Public School simultaneously?
- What years do the items span?

**Proposed Decision:** **FLAG FOR INVESTIGATION** → Need to check dates of items

**Rationale:** Schools were often upgraded in status. If items span different time periods, they may be the same institution at different points. If items are from the same era, they could be different schools. **Requires checking dates on tagged items.**

**Alternative if same school:** MERGE or HIERARCHY (with temporal note)

---

## Pair 3: "Katoomba Coal and Shale Mines" vs "Katoomba Coal and Shale Company"

**Usage:** Katoomba Coal and Shale Mines (2 items) vs Katoomba Coal and Shale Company (7 items)

**Analysis:**
- "Mines" (physical locations) vs "Company" (business entity)
- Could be:
  - **Same entity** - formal company name vs physical mine reference
  - **Related** - Company owns/operates the Mines (hierarchy)
  - **Same with user inconsistency** - taggers using names interchangeably

**Historical Context:**
- Mining companies often had similar names to their mines
- "Company" is more formal/corporate
- "Mines" is more geographic/operational

**Proposed Decision:** **HIERARCHY** → Katoomba Coal and Shale Company (parent) → Katoomba Coal and Shale Mines (child)

**Rationale:** The Company (business entity) operated the Mines (physical locations). Items tagged with company name should also get the mines tag when relevant, but not vice versa. This preserves distinction between corporate/business context vs on-site/mining context.

**Alternative:** MERGE if they're used completely interchangeably in sources.

---

## Pair 4: "Katoomba coal mines" (informal) vs "Katoomba Coal and Shale Company" (formal)

**Usage:** Katoomba coal mines (9 items) vs Katoomba Coal and Shale Company (7 items)

**Analysis:**
- Lowercase "coal mines" suggests generic/informal reference
- Could be:
  - **Generic term** vs **specific company**  (HIERARCHY or KEEP_SEPARATE)
  - **Informal** vs **formal** names for same entity (MERGE)
  - **Different:** "coal mines" could refer to multiple mines, company is specific

**Historical Context Question:**
- Does "Katoomba coal mines" refer to all coal mining operations in Katoomba?
- Or is it specifically the Katoomba Coal and Shale Company's operations?

**Proposed Decision:** **HIERARCHY** → "Katoomba coal mines" (parent, generic) → "Katoomba Coal and Shale Company" (child, specific)

**Rationale:** The generic term "Katoomba coal mines" likely encompasses all coal mining in Katoomba, while the Company is a specific operator. Items about the company should also be tagged with the generic category.

**Alternative:** KEEP_SEPARATE if "coal mines" is distinct from "Coal and Shale" operations.

---

## Pair 5: "Katoomba Coal and Shale Mines" vs "Katoomba coal mines"

**Usage:** Katoomba Coal and Shale Mines (2 items) vs Katoomba coal mines (9 items)

**Analysis:**
- This is the relationship between pairs 3 and 4
- "Coal and Shale Mines" (formal, specific) vs "coal mines" (informal, generic)
- Low usage of formal name (2) vs higher usage of generic (9)

**Note:** This pair is redundant with pairs 3 and 4 above. Once we resolve those relationships, this one is automatically resolved.

**Proposed Decision:** **Depends on resolution of Pairs 3 & 4**

If we establish:
- Company → Coal and Shale Mines (hierarchy from Pair 3)
- coal mines → Company (hierarchy from Pair 4)

Then: "Coal and Shale Mines" and "coal mines" would be related through the Company hierarchy.

**Recommendation:** Resolve Pairs 3 & 4 first, then this relationship becomes clear.

---

## Pair 6: "Druid's Lodge" vs "Lodges"

**Usage:** Druid's Lodge (4 items) vs Lodges (1 item)

**Analysis:**
- "Druid's Lodge" is specific (a particular friendly society lodge)
- "Lodges" is generic (fraternal organisations generally)
- Could be:
  - **HIERARCHY:** Lodges (parent) → Druid's Lodge (specific instance)
  - **FALSE POSITIVE:** Substring match with unrelated generic tag

**Historical Context:**
- Druids were a specific friendly society (Ancient Order of Druids)
- "Lodges" as a generic term could refer to Freemasons, Oddfellows, Druids, etc.

**Proposed Decision:** **HIERARCHY** → Lodges (parent) → Druid's Lodge (child)

**Rationale:** This follows the same pattern as our established hierarchies (Church → Methodist Church). Druid's Lodge is a specific instance of the broader category "Lodges". Items about Druid's Lodge should be tagged with both.

---

## Summary Table

| Tag 1 | Tag 2 | Count 1 | Count 2 | Proposed Decision | Confidence |
|-------|-------|---------|---------|-------------------|------------|
| Katoomba South | South Katoomba | 9 | 10 | MERGE → South Katoomba | Medium - needs item check |
| Katoomba Superior Public School | Katoomba Public School | 8 | 6 | INVESTIGATE (check dates) | Low - needs temporal data |
| Katoomba Coal and Shale Mines | Katoomba Coal and Shale Company | 2 | 7 | HIERARCHY (Company → Mines) | Medium-High |
| Katoomba coal mines | Katoomba Coal and Shale Company | 9 | 7 | HIERARCHY (coal mines → Company) | Medium |
| Katoomba Coal and Shale Mines | Katoomba coal mines | 2 | 9 | [Resolves from pairs 3&4] | Depends |
| Druid's Lodge | Lodges | 4 | 1 | HIERARCHY (Lodges → Druid's Lodge) | High |

---

## Recommended Actions

### High Confidence (Can proceed)

**Pair 6: Druid's Lodge / Lodges → HIERARCHY**
- Clear generic → specific pattern
- Matches established hierarchy patterns

### Medium Confidence (Quick check recommended)

**Pair 1: Katoomba South / South Katoomba → MERGE**
- Spot-check 1-2 items from each to confirm same location

**Pairs 3 & 4: Coal/Company relationships → HIERARCHIES**
- Logical corporate/geographic distinctions
- Allows for nuanced searching

### Low Confidence (Requires investigation)

**Pair 2: School names → FLAG FOR REVIEW**
- Need to check dates to determine if same school over time or concurrent institutions
- May require consulting NSW education records

---

## Decision Framework

### If MERGE:
- Choose canonical form (more common or more formal)
- Document variant in notes

### If HIERARCHY:
- Determine parent (more generic) and child (more specific)
- Apply multi-tagging (items get both tags)

### If KEEP_SEPARATE:
- Document rationale
- Consider adding notes to distinguish usage

