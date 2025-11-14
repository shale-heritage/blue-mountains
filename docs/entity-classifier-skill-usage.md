# Entity Classifier Skill - Usage Guide

## Overview

The **entity-classifier** skill uses Claude Sonnet 4.5's natural language understanding to classify dual-nature entities (hotels, churches, schools, halls) based on contextual analysis rather than deterministic regex patterns.

## Skill Location

```
~/.claude/skills/entity-classifier/
├── SKILL.md       # Metadata
└── skill.md       # Main prompt and instructions
```

## Two Approaches to Using the Skill

### Approach 1: Automated Collection + Manual Classification

**Best for:** Batch processing entities with human review

**Workflow:**

1. **Collect mentions from Zotero:**
   ```bash
   python scripts/38_classify_entities_with_claude.py --entity-type hotels --interactive
   ```

   This script:
   - Fetches items from Zotero tagged with specific hotel names
   - Extracts full text from notes
   - Finds context around hotel mentions
   - Generates a formatted prompt
   - Saves prompt to `data/entity_classification/hotels_classification_prompt.txt`

2. **Invoke the skill in Claude Code:**
   ```
   /skill entity-classifier
   ```

3. **Paste the generated prompt:**
   - Open `data/entity_classification/hotels_classification_prompt.txt`
   - Copy entire contents
   - Paste into Claude Code session

4. **Review Claude's structured output:**
   - Claude will analyse each mention
   - Provide classification (building/business/both)
   - Give reasoning and confidence level
   - List matched indicators

5. **Save the output:**
   - Copy Claude's output to `reports/claude_entity_classification_hotels.md`
   - Review and modify classifications as needed

### Approach 2: Direct Interactive Use

**Best for:** Individual entity classification, exploratory analysis

**Workflow:**

1. **Invoke the skill:**
   ```
   /skill entity-classifier
   ```

2. **Provide entity mention directly:**
   ```
   Classify this hotel mention:

   Entity: Carrington Hotel
   Context: "A concert was held at the Carrington Hotel last evening,
   attended by many prominent citizens. The hotel's large dining room
   was filled to capacity."
   ```

3. **Get immediate classification:**
   - Claude analyses the context
   - Applies heuristic framework
   - Returns structured classification

## Example Classification Session

### Input:
```
I need you to classify 2 mentions of hotels in historical newspaper text.

## Mention 1

**Entity:** Carrington Hotel
**Item:** Local and General (1893-07-08)
**Trove URL:** https://trove.nla.gov.au/newspaper/article/89522551

**Context:**
> The Nepean Times: Katoomba. Local and General. A very enjoyable concert
> was held at the Carrington Hotel on Wednesday evening last. The large
> dining room was crowded with visitors and residents who were treated to
> an excellent program of music and recitations.

---

## Mention 2

**Entity:** Imperial Hotel
**Item:** The Rockley Game (1898-03-18)
**Trove URL:** https://trove.nla.gov.au/newspaper/article/89530844

**Context:**
> After the match, the teams gathered at the Imperial Hotel, where the
> proprietor, Mr. J. Smith, provided refreshments. The Imperial Hotel has
> recently expanded its dining facilities to better serve visiting sporting
> teams and offers special rates for group bookings.
```

### Output:
```
### Entity: Carrington Hotel
**Item:** Local and General (1893-07-08)
**Classification:** building
**Confidence:** high

**Reasoning:**
Strong spatial indicators present: event occurring "at the Carrington Hotel"
and use of physical features ("large dining room"). The hotel functions purely
as a venue for the concert with no agency or business operation signals. This
is a clear building-only usage.

**Indicators Found:**
- Building: locational_prep (at), events_at (concert held at), physical_features (dining room)
- Business: none

**Context:**
> The Nepean Times: Katoomba. Local and General. A very enjoyable concert
> was held at the Carrington Hotel on Wednesday evening last. The large
> dining room was crowded with visitors and residents who were treated to
> an excellent program of music and recitations.

---

### Entity: Imperial Hotel
**Item:** The Rockley Game (1898-03-18)
**Classification:** both
**Confidence:** high

**Reasoning:**
Mixed indicators present. First sentence shows spatial usage (teams gathered
"at the Imperial Hotel"). However, second sentence demonstrates clear business
agency: proprietor named as active agent, hotel "has expanded" (active voice),
hotel "offers" services. Both building and business aspects evident in same
context.

**Indicators Found:**
- Building: locational_prep (at)
- Business: proprietor_subject (proprietor provided), agency_verbs (expanded),
  services (offers)

**Context:**
> After the match, the teams gathered at the Imperial Hotel, where the
> proprietor, Mr. J. Smith, provided refreshments. The Imperial Hotel has
> recently expanded its dining facilities to better serve visiting sporting
> teams and offers special rates for group bookings.
```

## Advantages Over Regex Approach

1. **Nuanced understanding**: Handles metonymy, implied agency, contextual disambiguation
2. **Robust to variation**: Doesn't require exhaustive pattern catalogues
3. **Confidence scoring**: Provides genuine assessment of classification certainty
4. **Reasoning transparency**: Explains decisions for human review
5. **Handles edge cases**: Can reason about novel patterns not in regex library
6. **Reusable**: Same skill applies to hotels, churches, schools, halls without modification

## Integration with Workflow

1. **Collection** (Script 38): Gather entity mentions from Zotero
2. **Classification** (entity-classifier skill): Claude analyses and classifies
3. **Review** (Human): Expert reviews structured output, modifies as needed
4. **Application** (Script 39): Parse approved classifications, update taxonomy
5. **Validation** (Scripts 36+): Verify no data loss, check consistency

## When to Use Which Approach

**Use Regex Approach (Script 37)** when:
- Processing large volumes (1000+ mentions)
- Patterns are very regular and well-defined
- Speed is critical
- No budget constraints for compute

**Use Claude Skill Approach (Script 38)** when:
- Contexts are complex and varied
- Edge cases are common
- Human review time is more valuable than compute cost
- Want explanations for classifications
- Building audit trail for decisions

## Skill Customisation

The skill can be adapted for other entity types by:

1. **Adjusting defaults** in skill.md:
   - Change default classifications for entity types
   - Add entity-specific indicators

2. **Adding examples** specific to domain:
   - More church-specific examples
   - School of arts patterns
   - Fraternal lodge contexts

3. **Refining confidence guidance**:
   - Entity-specific confidence heuristics
   - Domain knowledge about typical patterns

## Related Documentation

- `docs/entity-classification-heuristic.md` - Full decision framework
- `scripts/37_classify_hotels_building_vs_business.py` - Regex-based alternative
- `CLAUDE.md` - Project taxonomy principles
- `planning/TODO.md` - Lines 42-140 on polyhierarchy decisions
