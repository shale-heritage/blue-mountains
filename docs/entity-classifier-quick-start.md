# Entity Classifier - Quick Start Guide

## What is this?

A Claude Skill that uses natural language understanding to classify dual-nature entities (hotels, churches, schools, halls) as building-only, business/organisation-only, or both.

## Why use it?

**Better than regex because:**
- Understands context genre (advertisements, licenses, court cases)
- Handles metonymy and implied reference
- Explains reasoning for decisions
- Adapts to novel patterns
- Provides genuine confidence scoring

## Quick Start: 3 Steps

### Step 1: Collect Entity Mentions

```bash
cd ~/Code/blue-mountains
source venv/bin/activate

# Generate prompt for hotels
python scripts/38_classify_entities_with_claude.py --entity-type hotels --interactive

# Or for churches
python scripts/38_classify_entities_with_claude.py --entity-type churches --interactive
```

This creates:
- `data/entity_classification/hotels_mentions.json` - Raw data
- `data/entity_classification/hotels_classification_prompt.txt` - Formatted prompt

### Step 2: Copy the Skill to User Skills Directory

```bash
# If not already done
cp -r ~/.claude/skills/entity-classifier ~/.claude/skills/
```

Or manually create:
- `~/.claude/skills/entity-classifier/SKILL.md`
- `~/.claude/skills/entity-classifier/skill.md`

(Files are already at these locations based on earlier setup)

### Step 3: Classify with Claude

**Option A: In Claude Code CLI**
```
# Invoke the skill
/skill entity-classifier

# Paste contents of: data/entity_classification/hotels_classification_prompt.txt
```

**Option B: Manually with the prompt**

Just read the skill prompt (`~/.claude/skills/entity-classifier/skill.md`) and apply the heuristic to each mention.

Example:
```
I need you to classify this hotel mention:

Entity: Carrington Hotel
Context: "A concert was held at the Carrington Hotel last evening. The large dining room was filled to capacity."

Apply the entity classification heuristic.
```

Claude responds with:
```
### Entity: Carrington Hotel
**Classification:** building
**Confidence:** high

**Reasoning:**
Strong spatial indicators: event occurring "at the Carrington Hotel"
and reference to physical features ("large dining room"). No business
agency present.

**Indicators Found:**
- Building: locational_prep (at), events_at (concert held at),
  physical_features (dining room)
- Business: none
```

## Output Format

Claude provides structured output for each mention:

```
### Entity: [Name]
**Item:** [Article Title]
**Classification:** building | business | both
**Confidence:** high | medium | low

**Reasoning:**
[Explanation referencing specific textual evidence]

**Indicators Found:**
- Building: [list indicators or "none"]
- Business: [list indicators or "none"]

**Context:**
> [The relevant excerpt]
```

## What to do with the output

1. **Save it**: Copy to `reports/claude_entity_classification_hotels.md`

2. **Review it**: Check classifications, especially "both" cases

3. **Compare it**: Against regex-based report if you generated one

4. **Apply it**: Use approved classifications to update taxonomy

## Examples of Each Classification Type

### Building Only
```
Context: "A meeting was held at the Imperial Hotel on Tuesday evening."
→ Classification: building (venue for event)
```

### Business Only
```
Context: "The Carrington Hotel announced it will close for renovations."
→ Classification: business (hotel acting as agent)
```

### Both (Polyhierarchical)
```
Context: "The Megalong Hotel is conveniently situated near Nellie's Glen
and offers special rates for visitors."
→ Classification: both (location + commercial services)
```

## Troubleshooting

**Q: Skill not found when I type `/skill entity-classifier`**

A: The skill files need to be in `~/.claude/skills/entity-classifier/`. Check:
```bash
ls -la ~/.claude/skills/entity-classifier/
# Should show: SKILL.md and skill.md
```

**Q: How many mentions can I process at once?**

A: Recommend batches of 20-30 mentions per session. Larger batches can be split.

**Q: What if I disagree with Claude's classification?**

A: Review the reasoning, check the context, and override the classification. The skill provides recommendations, not mandates.

**Q: How do I extend this to churches or other entities?**

A: Use the same process:
```bash
python scripts/38_classify_entities_with_claude.py --entity-type churches --interactive
```

The skill automatically adapts to different entity types.

## Files Reference

- **Skill definition**: `~/.claude/skills/entity-classifier/skill.md`
- **Collection script**: `scripts/38_classify_entities_with_claude.py`
- **Decision heuristic**: `docs/entity-classification-heuristic.md`
- **Usage guide**: `docs/entity-classifier-skill-usage.md`
- **Demo examples**: `reports/claude_entity_classification_hotels_demo.md`

## Next: Extend to Other Entities

Once you're comfortable with hotels:

1. **Churches**: Building (worship venue) vs Organisation (congregation/denomination)
2. **Schools of Arts**: Building (community hall) vs Organisation (cultural society)
3. **Fraternal Halls**: Building (lodge meeting place) vs Organisation (fraternal order)

Same skill, same process, just change `--entity-type`.
