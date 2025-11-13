# Entity Tagging System - Quick Navigation

## Getting Started

→ **Start here:** [README.md](README.md) - Complete system overview
→ **Setup summary:** [SETUP.md](SETUP.md) - What's been created and why

## Workflows

→ **Hotel classification:** [workflows/01-hotel-classification.md](workflows/01-hotel-classification.md)
→ **Church classification:** workflows/02-church-classification.md (coming soon)
→ **Schools of Arts:** workflows/03-schools-classification.md (coming soon)

## Core Skill

→ **Entity Classifier Skill:** [../.claude/skills/entity-classifier/SKILL.md](../.claude/skills/entity-classifier/SKILL.md)
→ **Classification Heuristic:** [../.claude/skills/entity-classifier/references/classification_heuristic.md](../.claude/skills/entity-classifier/references/classification_heuristic.md)
→ **NLU vs Regex Comparison:** [../.claude/skills/entity-classifier/references/examples_comparison.md](../.claude/skills/entity-classifier/references/examples_comparison.md)

## Collection Script

→ **Automated collection:** [../.claude/skills/entity-classifier/scripts/collect_entity_mentions.py](../.claude/skills/entity-classifier/scripts/collect_entity_mentions.py)

## Outputs (Generated)

→ **Hotels:** [outputs/hotels/](outputs/hotels/)
→ **Churches:** [outputs/churches/](outputs/churches/)
→ **Schools:** [outputs/schools/](outputs/schools/)

Note: Generated files are not committed to git

## Related Documentation

→ **Project overview:** [../CLAUDE.md](../CLAUDE.md)
→ **Original heuristic:** [../docs/entity-classification-heuristic.md](../docs/entity-classification-heuristic.md)
→ **Taxonomy principles:** [../docs/folksonomy_logic.md](../docs/folksonomy_logic.md)
→ **Decision log:** [../planning/consolidation-decisions.md](../planning/consolidation-decisions.md)

## Quick Commands

```bash
# Activate environment
cd ~/Code/blue-mountains
source venv/bin/activate

# Collect hotel mentions
python .claude/skills/entity-classifier/scripts/collect_entity_mentions.py \
  --entity-type hotels \
  --output entity-tagging-system/outputs/hotels/

# Validate skill
python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py \
  .claude/skills/entity-classifier

# Check mapping coverage
python scripts/36_check_all_tag_mappings.py
```

## System Vision

**Phase 1 (Current):** Tag rationalization and dual-nature entity classification
**Phase 2 (In Progress):** Building vs business/organisation classification
**Phase 3 (Planned):** Entity enrichment from full text
**Phase 4 (Future):** Automated tagging pipeline

See [README.md](README.md) for complete vision and roadmap.
