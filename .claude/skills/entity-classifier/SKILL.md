---
name: entity-classifier
description: Classify dual-nature entities (hotels, churches, schools of arts, halls, lodges) in historical newspaper text as building-only, business/organisation-only, or both (polyhierarchical) based on contextual linguistic analysis. Use when analysing entity mentions from the Blue Mountains Historical Society Zotero library to determine appropriate Getty AAT facet assignments (Built Environment vs Agents).
---

# Entity Classifier

## Overview

Classify mentions of dual-nature entities in 19th-century Australian newspaper text to determine whether each entity should be tagged as a physical building/facility (Built Environment facet), a business/organisation (Agents facet), or both (polyhierarchical).

Uses natural language understanding to apply a linguistic heuristic framework, analysing spatial indicators (locational prepositions, events occurring, physical features) versus agency indicators (ownership, business operations, services provided).

## When to Use This Skill

Invoke this skill when:
- Classifying hotel mentions as buildings versus businesses
- Determining church classification (building versus religious organisation)
- Analysing schools of arts (venue versus cultural society)
- Reviewing any entity that can be both physical structure and organisational agent
- Validating or improving automated classifications from regex-based scripts
- Batch processing entity mentions collected from the Zotero library

## Workflow

### Step 1: Receive Entity Mentions

Accept formatted input containing:
- Entity name (e.g., "Carrington Hotel")
- Item title (newspaper article)
- Context (2-4 sentences surrounding the entity mention)
- Trove URL (optional, for verification)

Input may come from:
- **Automated collection**: Script 38 (`scripts/38_classify_entities_with_claude.py`) extracts mentions from Zotero and generates formatted prompts
- **Manual submission**: User provides individual entity mentions for classification
- **Batch review**: Multiple mentions in a single session

### Step 2: Apply Classification Heuristic

For each mention, analyse the context using the decision framework documented in `references/classification_heuristic.md`:

**Building/Facility indicators:**
- Locational prepositions: "at [entity]", "in [entity]", "near [entity]"
- Movement to/from location: "going to", "arriving at", "leaving"
- Events occurring: "meeting held at", "concert at", "staying at"
- Physical features: "[entity]'s rooms", "[entity] building"
- Construction/damage: "was built", "fire destroyed"

**Business/Organisation indicators:**
- Agency verbs: "[entity] announced", "[entity] is expanding"
- Ownership/management: "proprietor of [entity]", "[entity] owner"
- Business operations: "[entity] licensed", "[entity] trading"
- Services provided: "[entity] offers", "[entity] provides"
- Financial actions: "[entity] purchased", "[entity] revenue"
- Legal agency: "[entity] applied for licence", "[entity] was fined"

**Both (Polyhierarchical) indicators:**
- Mixed signals: Context contains both spatial AND agency indicators
- Metonymic usage: Entity name refers to both structure and organisation
- Parallel constructions: Text treats entity as both place and actor

**Context Genre Recognition:**
- **Advertisements** = business agency (entity promoting itself)
- **Licensing applications** = business operations (entity as legal applicant)
- **Court testimony** = usually spatial (entity as location of events)
- **News reports** = depends on narrative focus

**Metonymy Handling:**
- "The hotel denies..." = business (hotel = management/proprietor)
- "Meeting at the hotel" = building (hotel = physical venue)
- Passive voice ("was refurbished") = building (recipient of action)
- Active voice ("[entity] refurbished") = business (agent of action)

### Step 3: Determine Classification

Based on indicator analysis, assign classification:
- **building** - Only spatial/locational indicators present; entity functions as location
- **business** or **organisation** - Only agency/operational indicators present; entity acts as agent
- **both** - Both spatial and agency indicators present; requires polyhierarchical tags

Assess confidence level:
- **high** - Multiple strong indicators present; classification unambiguous
- **medium** - Some indicators present but context could support alternative
- **low** - Minimal indicators; relying on defaults or general patterns

**Default Guidance When Indicators Are Weak:**
- Hotels/inns → default to building (most newspaper mentions are locational)
- Churches → consider denomination and context (worship = building, governance = organisation)
- Schools of Arts → consider activity (event venue = building, committee = organisation)
- Halls → usually building unless committee/management explicitly mentioned

### Step 4: Provide Structured Output

For each entity mention, return structured classification:

```
### Entity: [Entity Name]
**Item:** [Article Title] ([Date if available])
**Classification:** building | business | organisation | both
**Confidence:** high | medium | low

**Reasoning:**
[2-3 sentences explaining classification, referencing specific textual evidence and matched indicators]

**Indicators Found:**
- Building: [list matched indicators, or "none"]
- Business/Organisation: [list matched indicators, or "none"]

**Context:**
> [The relevant excerpt with entity mention and surrounding text]
```

## Quality Standards

Adhere to these standards when classifying:

- **Evidence-based**: Ground every classification in textual evidence from context
- **Audit trail**: Provide reasoning clear enough for human reviewer to verify
- **Conservative**: When genuinely ambiguous, apply established defaults rather than speculate
- **Independent analysis**: Process each mention independently; avoid letting previous classifications bias current analysis
- **UK/Australian spelling**: Use behaviour, organisation, licence (noun), etc.

## Resources

### references/classification_heuristic.md
Complete decision framework with detailed indicator definitions, edge case guidance, and extended examples showing building-only, business-only, both, and metonymy cases.

### references/examples_comparison.md
Side-by-side comparison of Claude NLU approach versus regex-based classification, demonstrating where natural language understanding provides superior results (context genre recognition, metonymy handling, confidence calibration).

### scripts/collect_entity_mentions.py
Python script to automate collection of entity mentions from Zotero library. Fetches items by tag, extracts full text from notes, finds context around mentions, and generates formatted prompts for classification.

## Integration with Project Workflow

This skill supports the Blue Mountains folksonomy rationalisation project:

1. **Collection** (Script 38 or manual): Gather entity mentions with context from Zotero
2. **Classification** (This skill): Analyse and classify using NLU approach
3. **Review** (Human expert): Verify classifications, especially "both" cases
4. **Application** (Script 39): Parse approved classifications, update `data/tag_map_consolidated.csv`
5. **Validation** (Scripts 36+): Check for data loss, verify consistency

## Extending to Other Entity Types

This skill applies to any dual-nature entity. Adjust defaults as needed:

- **Hotels, inns, public houses**: Accommodation versus hospitality business
- **Churches, chapels**: Worship building versus religious organisation
- **Schools of Arts, Mechanics' Institutes**: Community hall versus cultural society
- **Fraternal lodge halls**: Lodge building versus fraternal order organisation
- **Schools**: Educational facility versus educational institution

When processing new entity types, update default guidance in references and document any entity-specific patterns encountered.
