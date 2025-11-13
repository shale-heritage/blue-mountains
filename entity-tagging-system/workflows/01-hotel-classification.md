# Workflow 1: Hotel Classification

## Goal

Classify all hotel mentions in the Zotero library as:
- **building** - Physical structure only (Built Environment facet)
- **business** - Hospitality business only (Agents facet)
- **both** - Polyhierarchical (appears in both facets)

## Prerequisites

- Zotero library export up to date (`data/zotero_full_export.json`)
- Virtual environment activated (`source venv/bin/activate`)
- Entity classifier skill installed (`.claude/skills/entity-classifier/`)

## Step 1: Collect Hotel Mentions

Extract hotel mentions with surrounding context from Zotero:

```bash
cd ~/Code/blue-mountains
source venv/bin/activate

python .claude/skills/entity-classifier/scripts/collect_entity_mentions.py \
  --entity-type hotels \
  --output entity-tagging-system/outputs/hotels/
```

**Output files:**
- `entity-tagging-system/outputs/hotels/hotels_mentions.json` - Raw data
- `entity-tagging-system/outputs/hotels/hotels_classification_prompt.txt` - Formatted prompt

**Review:** Check that expected hotels were found and contexts look reasonable.

## Step 2A: Generate Classifications (Regex Approach)

Generate automated classifications using pattern matching:

```bash
python scripts/37_classify_hotels_building_vs_business.py
```

**Output:** `reports/hotel_classification_review.md`

**Characteristics:**
- Fast processing (processes all 37 mentions in seconds)
- Deterministic pattern matching
- Lower confidence for many cases (89% at 1/3 confidence)
- Good as baseline or for cross-validation

## Step 2B: Generate Classifications (Claude NLU Approach)

Generate classifications using natural language understanding.

In Claude Code terminal, invoke the entity-classifier skill:

```
/skill entity-classifier
```

Then paste the contents of:
```
entity-tagging-system/outputs/hotels/hotels_classification_prompt.txt
```

Claude will analyse each mention and provide structured output.

**Save output to:**
```
entity-tagging-system/outputs/hotels/claude_classifications.md
```

**Characteristics:**
- Context-aware (recognises advertisements, licensing, court testimony)
- Handles metonymy ("hotel denies" = business, "at hotel" = building)
- Genuine confidence scoring
- Superior for complex cases

## Step 3: Review Classifications

### Option A: Review Regex Output Only

Open `reports/hotel_classification_review.md` and for each entry:

1. Read the context
2. Check the recommended classification
3. Modify `APPROVED_CLASSIFICATION` if needed
4. Add `REVIEW_NOTES` for ambiguous cases

### Option B: Review Claude NLU Output Only

Open `entity-tagging-system/outputs/hotels/claude_classifications.md` and:

1. Review each structured classification
2. Verify reasoning matches context
3. Note any disagreements with Claude's assessment
4. Modify classifications as needed

### Option C: Compare Both Approaches (Recommended)

Compare regex and Claude NLU results to identify:
- Cases where they agree (high confidence)
- Cases where they disagree (needs human decision)
- Patterns that one approach handles better

**Create comparison document:**
```bash
# Open both files side by side
code reports/hotel_classification_review.md \
     entity-tagging-system/outputs/hotels/claude_classifications.md
```

**Document discrepancies:**
- Where does Claude see business agency that regex missed?
- Where does regex over-classify based on weak signals?
- Which approach better handles advertisements, licensing, court testimony?

## Step 4: Approve Final Classifications

Create final approved classification file:

```
entity-tagging-system/outputs/hotels/approved_classifications.md
```

Format (one entry per hotel mention):
```markdown
### Carrington Hotel - A Charge of Rape (1890-09-06)
**Classification:** building
**Confidence:** high
**Source:** Claude NLU
**Reasoning:** Strong spatial indicators; hotel as location of criminal event
**Review Notes:** Both approaches agreed. Clear building usage.

### Megalong Hotel - Licensing Application (1893-06-09)
**Classification:** business
**Confidence:** high
**Source:** Claude NLU (regex: building)
**Reasoning:** Licensing application context; hotel as legal business entity
**Review Notes:** Claude correctly identified business context; regex missed licensing genre signal.
```

## Step 5: Update Taxonomy

### For "building" classifications:
Confirm existing `[Hotel Name] (building)` tags remain as-is in Built Environment.

### For "business" classifications:
Create new `[Hotel Name] (business)` tags under Agents > Organisations > Hospitality businesses.

Update `data/tag_map_consolidated.csv`:
```csv
[Hotel Name] (business),[Hotel Name] (business),hierarchy,parent=hotels (businesses),
```

### For "both" classifications:
Create polyhierarchical tags in both facets.

1. Keep existing: `[Hotel Name] (building)` → Built Environment
2. Add new: `[Hotel Name] (business)` → Agents > Organisations

Update synonym mappings for unqualified variants:
```csv
[Hotel Name],[Hotel Name] (building),synonym,Primary spatial usage,
[Hotel Name],[Hotel Name] (business),synonym,Business operations context,
```

**Note:** Items will need manual review to determine which facet applies per mention.

## Step 6: Validation

Verify no data loss:

```bash
# Check all tags still mapped
python scripts/36_check_all_tag_mappings.py

# Verify hotel hierarchy
grep -i "hotel" data/tag_map_consolidated.csv | grep hierarchy
```

Check for:
- All specific hotels accounted for
- Both (building) and (business) variants created where needed
- Synonym mappings point to correct facet
- No orphaned tags

## Expected Results

**From current batch (37 hotel mentions analysed):**

**Regex approach:**
- 100% classified as "building"
- 89% low confidence (1/3)
- 11% medium confidence (2/3)
- 0% high confidence

**Claude NLU approach (sample):**
- ~70-80% "building" (expected)
- ~10-20% "business" (licensing, advertisements)
- ~5-10% "both" (mixed contexts)
- Higher confidence scores overall

**Final approved (estimated):**
- Majority "building" (spatial usage most common)
- Some "business" (licensing applications, proprietor agency, advertisements)
- Few "both" (advertisements describing location while marketing services)

## Quality Checklist

Before finalizing:

- [ ] All 37 mentions reviewed
- [ ] Each "both" classification justified with evidence for both aspects
- [ ] Discrepancies between regex and NLU resolved
- [ ] Confidence levels reflect actual ambiguity
- [ ] Review notes explain non-obvious decisions
- [ ] Taxonomy updated with new tags where needed
- [ ] Validation scripts pass (100% mapping coverage)
- [ ] Decision log updated in `planning/consolidation-decisions.md`

## Patterns to Document

As you review, note patterns for future entity types:

**Context genres requiring special handling:**
- Advertisements → often "both" (location description + business marketing)
- Licensing applications → usually "business" (legal/regulatory context)
- Court testimony → usually "building" (location where events occurred)
- News reports → depends on focus (events vs operations)

**Metonymy patterns:**
- "Hotel denies..." → business
- "At the hotel..." → building
- "Proprietor of hotel..." → person related to business

**Indicators that matter most:**
- Strong: Licensing, proprietor agency, "offers/provides", "at/in [entity]"
- Weak: Generic mentions without clear spatial or agency cues

## Next Steps

After completing hotel classification:

1. Apply workflow to **churches** (worship location vs religious organisation)
2. Then **schools of arts** (community venue vs cultural society)
3. Generalize to **all dual-nature entities**
4. Begin **Phase 3** entity enrichment planning
