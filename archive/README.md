# Archive

This directory contains superseded files kept for reference and audit trail purposes.

## Structure

### csv-files/

Superseded CSV files from tag consolidation work:

- `tag_consolidation_map.csv` - Original consolidation map (replaced by `tag_map_consolidated.csv`)
- `poly_hierarchy_additions.csv` - Poly-hierarchy additions (merged into `tag_map_consolidated.csv`)
- `*.backup*` - Timestamped backups with MD5 checksums
- `*.md5` - MD5 checksum files for data integrity verification

**Note:** These files were merged on 2025-10-24 to create the single source of truth:
`data/tag_map_consolidated.csv`

### cc-interactions/

Claude Code interaction logs and session handover documents (Oct 2025):

- `2025-10-09-*.txt` through `2025-10-27-*.txt` - Complete interaction logs
- `SESSION_HANDOVER.md` - Session transition documentation
- `SESSION_HANDOVER_2025-10-20.md` - Previous session handover

These logs provide complete audit trail of:
- Decision-making rationale for tag consolidations
- Context analysis methodology discussions
- Taxonomy design choices
- Getty AAT (Art & Architecture Thesaurus) alignment considerations
- Implementation challenges and solutions

### planning/

Completed planning documents from Phase 1.2 tag consolidation work:

**Phase 1.2.1 (Oct 19, 2025):**
- `phase1.2.1-consolidation-decisions.md` - Tag consolidation decision log
- `phase1.2.1-instructions.md` - Detailed consolidation workflow instructions
- `session_summary_2025-10-19.md` - Session work summary
- `taxonomy_implementation_phase1.md` - Implementation roadmap

**CSV Merge and Primary Facet Cleanup (Oct 24, 2025):**
- `CSV_MERGE_PLAN.md` - Plan for merging CSV files (completed in commit e5e9312)
- `PRIMARY_FACET_CLEANUP_PLAN.md` - Plan for Getty AAT facet alignment (completed in commit 9706f16)

**Taxonomy Proposals (Oct 19, 2025):**
- `community_institutions_proposal.md` - Community institutions hierarchy proposal
- `community_institutions_taxonomy.md` - Detailed community taxonomy structure
- `religion_hierarchy_proposal.md` - Religious organisations hierarchy proposal
- All proposals implemented in `data/tag_map_consolidated.csv`

These documents are preserved for:

- Audit trail of decision-making process
- Methodology documentation
- Historical reference
- Understanding rationale for taxonomy choices

### reports/

Interim analysis reports from tag consolidation work:

- `consolidation_preview.md` - Preview of tag consolidations (completed Oct 19, 2025)
- `triage_report.md` - Ambiguous tag pair triage (all 421 pairs processed)
- `session_summary_2025-10-19-continued.md` - Session continuation summary

## Archive Policy

Files are moved to the archive when they are:

- Completed planning documents (plans that have been successfully executed)
- Superseded interim reports (analysis reports replaced by implementation)
- Historical session documentation (logs and summaries from completed work)
- Obsolete data files (replaced by consolidated or updated versions)

## Active Files

Current active files are in their respective directories:

- **Data:** `data/tag_map_consolidated.csv` (single source of truth)
- **Planning:** `planning/TODO.md`, active project plans
- **Documentation:** `docs/` directory
- **Reports:** `reports/` directory (current analysis and validation reports)
- **Scripts:** `scripts/` directory (reusable analysis and processing scripts)
