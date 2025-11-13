# Entity Tagging System

## Overview

Comprehensive system for analysing, classifying, and enriching subject tags in the Blue Mountains Historical Society Zotero library. Combines deterministic automated analysis with Claude Sonnet 4.5 natural language understanding to build a Getty AAT-aligned controlled vocabulary taxonomy.

**Current Phase:** Tag rationalization and dual-nature entity classification
**Future Vision:** Full entity recognition, relationship extraction, and automated tag enrichment from historical newspaper text

## System Purpose

### Phase 1: Tag Rationalization (Current)
Clean and consolidate existing folksonomy tags:
- Fix case sensitivity issues
- Map unqualified variants to qualified terms
- Classify dual-nature entities (hotels, churches, schools, halls)
- Eliminate data loss during taxonomy migration
- Achieve 100% mapping coverage

### Phase 2: Entity Classification (In Progress)
Determine appropriate facet assignments for ambiguous entities:
- Building/facility (Built Environment) vs Business/organisation (Agents)
- Apply polyhierarchical tagging where appropriate
- Use both regex-based and Claude NLU approaches
- Build audit trail for all classification decisions

### Phase 3: Tag Enrichment (Planned)
Extract additional entities and relationships from full text:
- Named entity recognition (people, places, organizations)
- Event extraction (meetings, accidents, court cases)
- Relationship detection (person-to-organization, event-to-location)
- Temporal information (dates, durations, sequences)
- Thematic classification (social issues, economic activities)

### Phase 4: Automated Tagging (Future)
Apply controlled vocabulary automatically to new items:
- Machine learning models trained on approved classifications
- Confidence scoring for automated suggestions
- Human-in-the-loop review for low-confidence tags
- Continuous improvement through feedback

## Directory Structure

```
entity-tagging-system/
├── README.md                    # This file - system overview and guide
├── workflows/                   # Step-by-step workflow guides
│   ├── 01-hotel-classification.md
│   ├── 02-church-classification.md
│   └── 03-entity-enrichment.md
├── outputs/                     # Generated classification reports
│   ├── hotels/
│   ├── churches/
│   └── schools/
└── scripts/                     # Workflow automation scripts
    ├── collect_entities.sh      # Wrapper for entity collection
    └── apply_classifications.py  # Apply approved classifications
```

## Core Components

### 1. Entity Classifier Skill
**Location:** `.claude/skills/entity-classifier/`

Claude Skill for classifying dual-nature entities using natural language understanding.

**Key files:**
- `SKILL.md` - Main skill definition with workflow
- `references/classification_heuristic.md` - Detailed decision framework
- `references/examples_comparison.md` - NLU vs regex comparison
- `scripts/collect_entity_mentions.py` - Automated collection from Zotero

**Usage:**
```bash
# Collect entity mentions
python .claude/skills/entity-classifier/scripts/collect_entity_mentions.py \
  --entity-type hotels --output entity-tagging-system/outputs/hotels/

# Invoke skill in Claude Code
/skill entity-classifier

# Paste generated prompt from outputs/
```

### 2. Classification Scripts
**Location:** `scripts/37_*.py` and `scripts/38_*.py`

Automated tools for entity analysis:

- **Script 37** (Regex-based): Deterministic pattern matching for classification
  - Fast processing of large batches
  - High confidence for clear patterns
  - Good for validation and cross-checking

- **Script 38** (Claude NLU): Natural language understanding classification
  - Superior context recognition
  - Handles metonymy and genre cues
  - Better for complex/ambiguous cases

**When to use which:**
- Use **Script 37** for initial bulk processing and clear cases
- Use **Script 38** for low-confidence cases and final review
- Compare results between approaches for quality assurance

### 3. Core Documentation
**Location:** `docs/`

Foundation documents for the tagging system:

- `entity-classification-heuristic.md` - Decision framework (also in skill references)
- `entity-classifier-skill-usage.md` - Skill usage guide
- `entity-classifier-quick-start.md` - Quick reference

### 4. Data Files
**Location:** `data/`

- `tag_map_consolidated.csv` - Master taxonomy mapping (single source of truth)
- `tag_application_mapping.csv` - Item-level tag applications
- `zotero_full_export.json` - Complete Zotero library export

## Current Workflows

### Workflow 1: Hotel Classification

**Goal:** Classify hotel mentions as building-only, business-only, or both

**Steps:**

1. **Collect mentions:**
   ```bash
   python .claude/skills/entity-classifier/scripts/collect_entity_mentions.py \
     --entity-type hotels \
     --output entity-tagging-system/outputs/hotels/
   ```

2. **Generate classifications:**
   ```bash
   # Option A: Regex-based (fast, deterministic)
   python scripts/37_classify_hotels_building_vs_business.py
   # Output: reports/hotel_classification_review.md

   # Option B: Claude NLU (contextual, nuanced)
   # In Claude Code:
   /skill entity-classifier
   # Paste: entity-tagging-system/outputs/hotels/hotels_classification_prompt.txt
   # Save output: entity-tagging-system/outputs/hotels/classifications.md
   ```

3. **Review and approve:**
   - Open classification report
   - Verify each classification
   - Modify `APPROVED_CLASSIFICATION` field if needed
   - Add `REVIEW_NOTES` for ambiguous cases

4. **Compare approaches (optional):**
   - Review discrepancies between regex and NLU
   - Choose best classification for each case
   - Document patterns for future reference

5. **Apply to taxonomy:**
   ```bash
   # Script to parse approved classifications and update taxonomy
   python entity-tagging-system/scripts/apply_classifications.py \
     --input entity-tagging-system/outputs/hotels/classifications.md \
     --update data/tag_map_consolidated.csv
   ```

### Workflow 2: Church Classification

**Coming Soon** - Follow same pattern as hotels, adapted for religious organisations

Key considerations:
- Worship events → building
- Denominational governance → organisation
- Mixed religious/administrative → both

### Workflow 3: Schools of Arts Classification

**Coming Soon** - Cultural society vs community venue

Key considerations:
- Event venue usage → building
- Committee decisions/programs → organisation
- Often polyhierarchical due to dual role

## Quality Assurance

### Validation Checks

Before finalizing any classifications:

1. **Coverage check:**
   ```bash
   python scripts/36_check_all_tag_mappings.py
   # Ensure 100% mapping coverage
   ```

2. **Consistency check:**
   - Compare classifications across similar entities
   - Verify polyhierarchical assignments are justified
   - Check for conflicting signals

3. **Evidence check:**
   - Every "both" classification has clear evidence for both aspects
   - Reasoning includes specific textual evidence
   - Confidence levels reflect actual ambiguity

4. **Audit trail:**
   - All decisions documented with reasoning
   - Original context preserved
   - Reviewer notes captured

### Decision Documentation

Maintain comprehensive audit trail in:
- `planning/consolidation-decisions.md` - Overall decision log
- Individual workflow outputs - Classification-specific reasoning
- REVIEW_NOTES fields - Ambiguous case explanations

## Future Extensions

### Phase 3: Entity Enrichment

**Vision:** Extract additional entities from full text that weren't manually tagged

**Planned capabilities:**
- Named entity recognition for people, places, organisations
- Event extraction (accidents, crimes, social events, business events)
- Relationship detection (person-occupation, person-organisation, event-location)
- Temporal tagging (precise dates, date ranges, temporal relationships)

**Workflow approach:**
1. Process full text through entity recognition
2. Generate candidate tags with confidence scores
3. Claude NLU reviews candidates in context
4. Human expert approves high-confidence suggestions
5. Low-confidence candidates flagged for manual review

### Phase 4: Automated Tagging Pipeline

**Vision:** Apply controlled vocabulary automatically to new items

**Components:**
- Training data from approved classifications
- Machine learning models for tag prediction
- Confidence thresholds for automation
- Human-in-the-loop review interface
- Continuous learning from corrections

## System Principles

### 1. Evidence-Based Classification
Every classification decision grounded in textual evidence. No speculation or external knowledge.

### 2. Audit Trail
Complete documentation of decisions, reasoning, and alternatives considered. Reproducible process.

### 3. Progressive Disclosure
Start simple (hotels), expand to similar entities (churches, halls), generalize to full entity recognition.

### 4. Hybrid Approach
Combine deterministic automation (regex, rules) with AI understanding (Claude NLU) and human expertise.

### 5. Quality Over Speed
Correct classifications more valuable than rapid processing. Build trust through careful review.

### 6. Getty AAT Alignment
Maintain compatibility with authoritative controlled vocabularies. Follow established cultural heritage standards.

## Getting Started

### For Hotel Classification (Current Task)

1. **Review the skill:**
   ```bash
   cat .claude/skills/entity-classifier/SKILL.md
   ```

2. **Collect hotel mentions:**
   ```bash
   python .claude/skills/entity-classifier/scripts/collect_entity_mentions.py \
     --entity-type hotels \
     --output entity-tagging-system/outputs/hotels/
   ```

3. **Generate classifications using Claude:**
   ```
   # In Claude Code
   /skill entity-classifier

   # Paste contents of:
   # entity-tagging-system/outputs/hotels/hotels_classification_prompt.txt
   ```

4. **Save and review output:**
   ```bash
   # Save Claude's output to:
   entity-tagging-system/outputs/hotels/classifications.md

   # Review each classification
   # Approve or modify as needed
   ```

5. **Compare with regex approach (optional):**
   ```bash
   diff entity-tagging-system/outputs/hotels/classifications.md \
        reports/hotel_classification_review.md
   ```

### For New Entity Types

1. Add entity names to `scripts/collect_entity_mentions.py`
2. Update entity-specific defaults in skill references
3. Run collection → classification → review workflow
4. Document patterns and edge cases
5. Apply approved classifications to taxonomy

## Related Documentation

- **Project overview:** `CLAUDE.md`
- **Taxonomy structure:** `docs/folksonomy_logic.md`
- **Decision log:** `planning/consolidation-decisions.md`
- **Validation scripts:** `scripts/36_*.py`
- **Classification heuristic:** `docs/entity-classification-heuristic.md`

## Support and Iteration

As you use this system:

1. **Document challenges** encountered during classification
2. **Note patterns** that emerge across entity types
3. **Suggest improvements** to heuristic or workflow
4. **Request new features** for Phase 3 entity enrichment

This system is designed to evolve. Feedback from real usage will shape future development.
