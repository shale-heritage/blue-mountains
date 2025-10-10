# Blue Mountains Planning Directory

This directory contains project planning documents that guide software development, FAIR4RS compliance implementation, and research workflows.

## Purpose

Planning documents serve multiple functions:

1. **Project roadmap:** Break down complex work into phases and tasks
2. **Decision documentation:** Record rationale for technical and methodological choices
3. **Knowledge transfer:** Enable new team members to understand project evolution
4. **FAIR compliance:** Document software development process (Reusable principle)

---

## Document Index

### Project Planning

| Document | Purpose | Status | Last Updated |
|----------|---------|--------|--------------|
| `project-plan.md` | Overall 6-phase project plan | Active | 2025-10-09 |
| `phase1-detailed.md` | Tag rationalisation phase breakdown | Active | 2025-10-09 |

### FAIR4RS Implementation Plans

| Document | Purpose | Status | Last Updated |
|----------|---------|--------|--------------|
| `FAIR4RS-documentation-plan.md` | Master FAIR4RS compliance plan (Phases A-E) | Active | 2025-10-09 |
| `FAIR4RS-phase-a-detailed.md` | Phase A: Metadata and compliance files | Completed | 2025-10-09 |
| `FAIR4RS-phase-b-detailed.md` | Phase B: Enhanced code documentation | Completed | 2025-10-09 |
| `FAIR4RS-phase-c-detailed.md` | Phase C: Folder-specific READMEs | Completed | 2025-10-10 |

### Future Planning Documents

As the project progresses, additional planning documents may be added:

- `phase2-ai-tagging-plan.md` - LLM-assisted tagging implementation
- `phase3-location-data-plan.md` - Gazetteer integration approach
- `phase4-omeka-publication-plan.md` - Omeka Classic workflow
- `vocabulary-development-plan.md` - Controlled vocabulary structure decisions
- `data-quality-log.md` - Record of curation decisions and merges

---

## Document Purposes

### project-plan.md

**High-level overview of the 6-phase project:**

1. Tag Rationalisation & Vocabulary Publishing
2. AI-Assisted Tagging
3. Location Data Enhancement
4. Omeka Classic Publication
5. CurateScape Mobile Tours
6. Archaeological Integration

Provides strategic context for all technical decisions.

### phase1-detailed.md

**Operational breakdown of Phase 1 (current focus):**

- Tag extraction workflow
- Analysis procedures
- Quality assurance steps
- Vocabulary development approach
- RVA publishing preparation

### FAIR4RS-documentation-plan.md

**Master plan for achieving FAIR4RS compliance:**

Maps FAIR principles (Findable, Accessible, Interoperable, Reusable) to concrete implementation tasks across 5 phases:

- Phase A: Metadata files (CITATION.cff, codemeta.json, enhanced README)
- Phase B: Code documentation (docstrings, comments, educational explanations)
- Phase C: Folder READMEs (this phase)
- Phase D: API documentation and testing
- Phase E: Quality assurance and final validation

### FAIR4RS Phase Detail Plans

**Implementation guides for each FAIR4RS phase:**

Each phase detail plan includes:

- Overview and rationale
- Task breakdowns with deliverables
- File locations and content specifications
- Quality assurance procedures
- Acceptance criteria
- Estimated time and dependencies

These plans guide Claude Code-assisted implementation while documenting the development process for reproducibility.

---

## How Planning Documents Relate to Implementation

### Planning → Code

1. **Planning documents** (this directory) describe **what** to build and **why**
2. **Scripts** (scripts/ directory) implement the planned functionality
3. **Documentation** (README.md, docs/, CONTRIBUTING.md) explain **how** to use and maintain

### Iterative Refinement

Planning is not linear:

- Initial plans are detailed but may evolve as implementation reveals new insights
- Completed phases inform future phase planning
- Decision logs capture changes and rationale

### Version Control

All planning documents are tracked in Git to preserve project history:

```bash
# View planning document history
git log --follow planning/FAIR4RS-documentation-plan.md

# Compare versions
git diff HEAD~5 HEAD planning/project-plan.md
```

---

## Project Evolution

### Timeline

**October 2025:** FAIR4RS compliance implementation

- ✅ Phase A: Metadata files and main README (Oct 9)
- ✅ Phase B: Enhanced code documentation (Oct 10)
- ✅ Phase C: Folder-specific READMEs (Oct 10)
- 📅 Phase D: API documentation (planned)
- 📅 Phase E: Quality assurance (planned)

### Major Decisions

Key methodological and technical decisions are documented in planning files:

1. **Folksonomy → Controlled Vocabulary approach** (project-plan.md)
   - Rationale: Leverage team's informal tagging work rather than starting from scratch
   - Method: Fuzzy matching, hierarchy detection, manual curation

2. **Separate API keys for read-only vs read-write** (FAIR4RS-phase-b-detailed.md)
   - Rationale: Principle of least privilege for security
   - Implementation: config.py supports dual-key strategy

3. **UK/Australian spelling throughout** (FAIR4RS-phase-b-detailed.md, CLAUDE.md)
   - Rationale: Project based in Australia, aligns with funding body and partner expectations
   - Implementation: Comprehensive spelling audit, custom aspell dictionary

4. **Three-tier README architecture** (FAIR4RS-phase-c-detailed.md)
   - Rationale: Balance discoverability (main README), technical depth (docs/), and contextual guidance (folder READMEs)
   - Implementation: Main README complete, docs/ complete, folder READMEs complete

---

## Contributing to Planning

Planning documents are living resources. To propose changes:

1. **Open an issue:** Describe what aspect of planning needs revision and why
2. **Submit PR:** Modify planning document with clear rationale
3. **Discuss with team:** Major strategic changes require PI approval
4. **Update related docs:** Keep implementation docs in sync with planning

---

## See Also

- **Main README:** Project overview and getting started
- **CONTRIBUTING.md:** Code standards and contribution process
- **docs/:** Technical specifications (data formats, vocabularies)
- **scripts/README.md:** Script execution guide

---

## Questions?

- **Planning unclear:** Open GitHub issue for discussion
- **Want to contribute:** See CONTRIBUTING.md for process
- **Historical context:** Check git log for document evolution
