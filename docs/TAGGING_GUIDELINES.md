# Tagging Guidelines

**Purpose:** Establish consistent rules for applying controlled vocabulary tags to Zotero items
**Last Updated:** 2025-10-22
**Status:** Authoritative - all tagging must follow these guidelines

---

## Core Principle: Leaf Nodes Only

**Rule:** Only tag with **leaf nodes** (terminal/taggable terms), never with organizational/intermediate category terms.

**Rationale:**
- Organizational terms (plural categories) exist only to structure the vocabulary
- They are not meant to be applied to items
- Tagging with leaf nodes maintains specificity and prevents redundancy
- The hierarchy automatically provides broader context without redundant tagging

**Aligned with:** Getty Art & Architecture Thesaurus (AAT) approach using guide terms vs. descriptors

---

## Hierarchy Structure

Our vocabulary uses a three-level pattern for most hierarchies:

```
Level 1: Plural Category (ORGANIZATIONAL - DO NOT TAG)
├─ Level 2: Singular Generic (TAGGABLE - use when unnamed/generic)
├─ Level 3a: Specific Instance 1 (TAGGABLE)
├─ Level 3b: Specific Instance 2 (TAGGABLE)
└─ Level 3c: Specific Instance 3 (TAGGABLE)
```

### Example: Hotels

```
Hotels ← ORGANIZATIONAL CATEGORY (DO NOT TAG)
├─ Hotel ← TAG when "a hotel" mentioned but not named
├─ Carrington Hotel ← TAG when this specific hotel named
├─ Megalong Hotel ← TAG when this specific hotel named
├─ Belgravia Hotel ← TAG when this specific hotel named
└─ ... (25+ specific hotels)
```

### Usage in Practice

**Article text:** "The hotel keeper applied for a license..."
- ✗ Do NOT tag: `Hotels` (organizational category)
- ✓ DO tag: `Hotel` (generic hotel)
- ✓ Also tag: `Hotellier` (occupation mentioned)

**Article text:** "The Carrington Hotel opened today..."
- ✗ Do NOT tag: `Hotels` (organizational category)
- ✓ DO tag: `Carrington Hotel` (specific hotel named)

**Article text:** "Hotels in the mountains are busy this season..."
- ✗ Do NOT tag: `Hotels` (organizational category)
- ✓ DO tag: `Hotel` (generic hotels, plural in text but use singular tag)

**Article text:** "The Carrington Hotel and Megalong Hotel both reported..."
- ✗ Do NOT tag: `Hotels` (organizational category)
- ✓ DO tag: `Carrington Hotel` + `Megalong Hotel` (both specific hotels)

---

## Tagging Decision Tree

When tagging an item, follow this decision process:

### Step 1: Identify the Concept

What is mentioned in the text?
- A general/unnamed instance? → Use singular generic term
- A specific named instance? → Use the specific term
- Multiple instances? → Use multiple specific terms
- Category/class discussion? → Use singular generic term

### Step 2: Locate in Hierarchy

Find the term in `data/poly_hierarchy_additions.csv`:
- Check if it's a plural category (organizational only)
- Confirm it's a leaf node (taggable)

### Step 3: Apply Tag

- Use the most specific applicable term
- Never use plural organizational categories
- Tag with multiple terms if multiple concepts mentioned
- Use singular generic when specific instance not identified

---

## Common Patterns and Examples

### Pattern 1: Buildings and Structures

**Hierarchy:**
```
Hotels (organizational)
├─ Hotel (generic)
└─ [Specific hotels]

Churches (organizational)
├─ Church (generic)
└─ [Specific churches]

Boarding houses (organizational)
├─ Boarding house (generic)
└─ [Specific boarding houses]

Cottages (organizational)
└─ Cottage (generic - no specific ones named yet)

Stables (organizational)
└─ Stable (generic - no specific ones named yet)
```

**Examples:**
- "A church was built" → Tag: `Church`
- "St Hilda's Church was consecrated" → Tag: `St Hilda's Church`
- "The hotel and boarding house were full" → Tag: `Hotel` + `Boarding house`
- "Carrington Hotel's stables" → Tag: `Carrington Hotel` + `Stable`

### Pattern 2: Occupations and People

**Hierarchy:**
```
Hotelliers (organizational)
├─ Hotellier (generic)
├─ Mrs Long
├─ F. C. Goyder
└─ [28 more specific people]

Clergy (organizational)
├─ Clergyman (generic - TO BE ADDED)
├─ Cardinal Moran
├─ Reverend M S Fletcher
└─ [Other specific clergy]

Medical professionals (organizational)
├─ Medical professional (generic - TO BE ADDED)
├─ Dr Spark
├─ Dr Prangley
└─ [Other specific doctors]
```

**Examples:**
- "A hotellier applied for a license" → Tag: `Hotellier`
- "Mrs Long, the hotellier, attended" → Tag: `Mrs Long`
- "F. C. Goyder and Mrs Long both spoke" → Tag: `F. C. Goyder` + `Mrs Long`
- "A clergyman performed the service" → Tag: `Clergyman` (when implemented)
- "Reverend Fletcher officiated" → Tag: `Reverend M S Fletcher`

### Pattern 3: Materials and Substances

**Hierarchy:**
```
Alcoholic beverages (organizational)
├─ Beer (generic beverage type)
├─ Wine (generic beverage type)
├─ Spirits (organizational subcategory)
│   ├─ Whisky (specific spirit type)
│   ├─ Rum (specific spirit type)
│   ├─ Brandy (specific spirit type)
│   └─ Gin (specific spirit type)
└─ Mixed alcoholic beverages (organizational subcategory)
    └─ Grog (specific mixed beverage)
```

**Examples:**
- "They drank alcohol" → Tag: `Beer` or `Wine` or `Spirits` (based on context, or all if general)
- "Beer and wine were served" → Tag: `Beer` + `Wine`
- "A bottle of whisky" → Tag: `Whisky`
- "Rum and gin" → Tag: `Rum` + `Gin`
- "Grog was consumed" → Tag: `Grog`

**Note:** For materials, the intermediate level (Beer, Wine, Spirits) ARE taggable because they represent actual substance types, not just organizational categories.

### Pattern 4: Activities

**Hierarchy:**
```
Commercial activities (organizational)
├─ Liquor trade (specific activity)
└─ ... (other activities)

Social behaviours (organizational)
├─ Drinking (alcohol) (specific behaviour)
├─ Gambling (specific behaviour)
└─ ... (other behaviours)

Regulatory processes (organizational)
└─ Licensing (organizational subcategory)
    ├─ Liquor licensing (specific regulatory process)
    ├─ Hotel licensing (specific regulatory process)
    └─ Publican's licensing (specific regulatory process)
```

**Examples:**
- "He engaged in liquor trade" → Tag: `Liquor trade`
- "Drinking and gambling occurred" → Tag: `Drinking (alcohol)` + `Gambling`
- "Hotel licensing application submitted" → Tag: `Hotel licensing`

### Pattern 5: Geographic Places

**Hierarchy:**
```
Towns (organizational)
├─ Katoomba (specific town)
├─ Leura (specific town)
├─ Megalong (specific town - or valley?)
└─ ... (other towns)

Valleys (organizational)
└─ Megalong Valley (specific valley)
```

**Examples:**
- "In a Blue Mountains town" → Tag: Identify specific town if mentioned, or use most appropriate broader geographic tag
- "At Katoomba" → Tag: `Katoomba`
- "Leura and Katoomba" → Tag: `Leura` + `Katoomba`
- "Megalong Valley" → Tag: `Megalong Valley`

**Note:** For places, we typically don't have a generic "Town" tag because places are inherently specific.

---

## Special Cases and Exceptions

### Exception 1: When Generic Tag Doesn't Exist

Some organizational categories may not have a singular generic tag yet.

**What to do:**
1. If text clearly identifies a generic instance needing a tag
2. Add the singular generic to the hierarchy
3. Use it for tagging

**Example:** If we discover articles about "a council" but no specific council named, and we don't have a "Council" (singular) tag:
1. Add `Council,Council,hierarchy,parent=Councils` to the vocabulary
2. Tag the item with `Council`

### Exception 2: Multiple Levels of Organization

Some hierarchies have multiple organizational levels:

```
Criminal events (organizational)
└─ Alcohol-related (organizational subcategory)
    ├─ Drunkenness (taggable)
    ├─ Unlicensed sales (taggable)
    └─ Serving alcohol to minors (taggable)
```

**Rule:** Still only tag with leaf nodes
- ✗ Do NOT tag: `Criminal events` or `Alcohol-related`
- ✓ DO tag: `Drunkenness`, `Unlicensed sales`, or `Serving alcohol to minors`

### Exception 3: Poly-hierarchical Terms

Some terms appear in multiple hierarchies (poly-hierarchy):

```
Hotels appears in THREE hierarchies:
1. Built Environment > Accommodation buildings > Hotels (primary)
2. Agents > Organizations > Hospitality businesses > Hotels (secondary)
3. Thematic grouping > Alcohol-related venues > Hotels (thematic)
```

**Rule:** The poly-hierarchy exists to show relationships, but you still tag with the SAME leaf node tag (`Hotel` or specific hotel name)
- The tag automatically inherits all hierarchical relationships
- No need to tag differently based on which hierarchy perspective

---

## When to Tag with Multiple Terms

### Tag Multiple Terms When:

1. **Multiple distinct concepts mentioned:**
   - "The Carrington Hotel's hotellier, Mrs Long" → Tag: `Carrington Hotel` + `Mrs Long`

2. **Multiple instances of same type:**
   - "Carrington Hotel and Megalong Hotel" → Tag: `Carrington Hotel` + `Megalong Hotel`

3. **Related but distinct concepts:**
   - "Hotel licensing and publican's licensing" → Tag: `Hotel licensing` + `Publican's licensing`

4. **Activities and participants:**
   - "Liquor trade by Mr Wilkinson" → Tag: `Liquor trade` + `Mr Wilkinson`

5. **Materials and activities:**
   - "Drinking whisky" → Tag: `Drinking (alcohol)` + `Whisky`

### Do NOT Tag Redundantly:

1. **Parent and child together:**
   - ✗ `Hotels` + `Carrington Hotel` (redundant - hierarchy provides parent)
   - ✓ `Carrington Hotel` (only)

2. **Generic and specific together:**
   - ✗ `Hotel` + `Carrington Hotel` (redundant - Carrington Hotel is a hotel)
   - ✓ `Carrington Hotel` (only)

3. **Organizational category and leaf:**
   - ✗ `Alcoholic beverages` + `Beer` (wrong - alcoholic beverages is organizational)
   - ✓ `Beer` (only)

---

## Verification Checklist

Before applying a tag, verify:

- [ ] Is this a leaf node (taggable term)?
- [ ] Is it the most specific term applicable?
- [ ] Have I avoided plural organizational categories?
- [ ] If generic/unnamed, am I using the singular generic tag?
- [ ] If specific/named, am I using the specific tag?
- [ ] Have I tagged all relevant concepts mentioned?
- [ ] Have I avoided redundant parent-child tagging?

---

## Implementation Notes

### In Zotero

When tagging items in Zotero:
1. Type the tag name - Zotero will autocomplete from existing tags
2. If tag doesn't exist yet, Zotero will create it
3. Ensure spelling matches the controlled vocabulary exactly

### In Automated Tagging Scripts (Future)

When developing automated tagging scripts:
1. Load `data/poly_hierarchy_additions.csv`
2. Filter for `action=hierarchy` (exclude synonyms, broader terms)
3. Build a list of taggable leaf nodes by excluding plural organizational terms
4. Apply pattern matching:
   - If specific name detected → use specific tag
   - If generic mention detected → use singular generic tag
   - Never apply plural category tags

**Detection pattern for organizational terms:**
- Terms that end in 's' AND have a singular version as immediate child → organizational
- Terms marked with special notation in future vocabulary versions

---

## Common Mistakes to Avoid

### Mistake 1: Tagging with Plural Categories

❌ **Wrong:** Article about hotel licensing gets tagged with `Hotels`
✓ **Correct:** Gets tagged with `Hotel` (if generic) or specific hotel name

### Mistake 2: Over-specific When Generic

❌ **Wrong:** Article says "a hotel" and you guess it might be Carrington Hotel, so you tag `Carrington Hotel`
✓ **Correct:** If hotel not named, tag with `Hotel` (generic)

### Mistake 3: Redundant Hierarchy Tagging

❌ **Wrong:** Tag with `Hotels` + `Hotel` + `Carrington Hotel`
✓ **Correct:** Tag with `Carrington Hotel` only (hierarchy provides the rest)

### Mistake 4: Missing Generic Tag

❌ **Wrong:** Article says "a hotel" but since no specific hotel named, don't tag at all
✓ **Correct:** Tag with `Hotel` (singular generic)

### Mistake 5: Confusing Singular Generic with Organizational

❌ **Wrong:** Think `Hotel` is organizational and don't use it
✓ **Correct:** `Hotel` (singular) is TAGGABLE, `Hotels` (plural) is organizational

---

## Reference Summary Table

| Hierarchy Level | Example | Taggable? | When to Use |
|----------------|---------|-----------|-------------|
| **Plural Category** | Hotels, Churches, Clergy | ✗ NO | Never - organizational only |
| **Singular Generic** | Hotel, Church, Clergyman | ✓ YES | When unnamed/generic instance mentioned |
| **Specific Instance** | Carrington Hotel, St Hilda's Church, Cardinal Moran | ✓ YES | When specific entity named |

---

## Getty AAT Alignment

Our approach aligns with Getty AAT principles:

**AAT uses:**
- Guide terms `<in angle brackets>` - organizational only (equivalent to our plural categories)
- Descriptors - taggable terms (equivalent to our singular generic + specific instances)

**Differences:**
- AAT often makes plural terms taggable descriptors (e.g., "churches")
- We reserve plural forms for organizational structure only
- Our singular generic terms serve the function AAT assigns to plural descriptors
- This provides clearer distinction for cataloguers

**Similarity:**
- Both approaches emphasize specificity
- Both use hierarchies to provide context without redundant tagging
- Both distinguish organizational structure from taggable vocabulary

---

## Updates and Revisions

### Version History

- **2025-10-22:** Initial version establishing leaf nodes only rule
- Future updates will be tracked here

### Proposing Changes

If you encounter cases that don't fit these guidelines:
1. Document the specific case
2. Propose how the guidelines should be modified
3. Update this document after decision
4. Regenerate affected CSV files and reports

---

## See Also

- **data/poly_hierarchy_additions.csv:** Complete vocabulary hierarchy
- **docs/folksonomy_logic.md:** Rationale for vocabulary structure
- **docs/thesaurus_structure.md:** Vocabulary organization principles
- **docs/TAG_APPLICATION_WORKFLOW.md:** How to apply tags to Zotero
- **Getty AAT About:** https://www.getty.edu/research/tools/vocabularies/aat/about.html

---

## Quick Reference Card

**One Rule to Remember:**

> **Tag with leaf nodes only**
> Never use plural organizational categories.
> Use singular generic for unnamed instances.
> Use specific names when entities are identified.

**Example:**
- Text: "A hotel opened" → Tag: `Hotel`
- Text: "Carrington Hotel opened" → Tag: `Carrington Hotel`
- Text: "Hotels were busy" → Tag: `Hotel` (generic plural becomes singular tag)
- Never tag: `Hotels` (plural category)
