# Taxonomy CSV Structure

**File:** `data/tag_map_consolidated.csv`
**Purpose:** Master mapping from original folksonomy tags to controlled vocabulary
**Last updated:** 2025-11-16

---

## CSV Schema

```csv
old_tag,new_tag,action,notes,status
```

### Field Definitions

#### 1. old_tag
**Type:** String
**Description:** Original tag from Zotero folksonomy or variant form
**Examples:** `Trucking`, `Anglican`, `Allen's Hotel`

#### 2. new_tag
**Type:** String
**Description:** Preferred term in controlled vocabulary
**Examples:** `truck system`, `Church of England`, `hotel`

#### 3. action
**Type:** Enum
**Description:** What transformation was applied to the old tag

**Values:**
- `hierarchy` - Active term in taxonomy structure (1,859 entries)
- `synonym` - Old tag redirects to preferred term (270 entries)
- `merge` - Multiple old tags consolidated into one (34 entries)
- `keep` - Explicitly preserved as-is (95 entries)
- `exclude` - Excluded from taxonomy (rare)
- `broader` - Replaced with broader term (rare)

**Note:** This field captures **what happened** to transform folksonomy to controlled vocabulary.

#### 4. notes
**Type:** String
**Description:** Rationale, evidence, or explanation for the mapping decision

**Best practices:**
- UK/Australian spelling
- Concise (1-2 sentences)
- Include evidence from sources when relevant
- Document reasoning for non-obvious decisions

**Examples:**
- `Capitalized variant from original Zotero tags`
- `UK/Australian terminology preference - use Church of England`
- `Historical term for the truck system - 19th century exploitative labour practice`

#### 5. status
**Type:** Enum
**Description:** Current lifecycle state of the entry (added 2025-11-16)

**Values:**
- `active` - Currently used in taxonomy (2,213 entries, 98%)
- `merged` - Consolidated into another entry (34 entries, 1.5%)
- `removed` - No longer valid, kept for audit trail only (13 entries, 0.6%)
- `deprecated` - Marked for future removal but still valid (not yet used)
- `historical` - Preserved for research but not for tagging (not yet used)

**Note:** This field captures **lifecycle state** (orthogonal to action field).

---

## Field Comparison: action vs status

These fields serve different purposes:

| Field | Purpose | Question Answered | Examples |
|-------|---------|-------------------|----------|
| **action** | Transformation type | "What happened to this tag?" | synonym, merge, hierarchy |
| **status** | Lifecycle state | "Is this entry currently valid?" | active, removed, deprecated |

**Example:**
```csv
old_tag,new_tag,action,notes,status
Anglican,Church of England,synonym,UK/Australian terminology preference,active
Trucking,Trucking,hierarchy,parent=Transport - REMOVED by script 48,removed
```

- First entry: **action=synonym** (redirects to preferred term), **status=active** (valid mapping)
- Second entry: **action=hierarchy** (was in structure), **status=removed** (no longer valid)

---

## Status Field Use Cases

### active
Normal entries in current use. Includes:
- All hierarchy entries for current taxonomy structure
- All synonym mappings from old folksonomy to new terms
- All keep entries for preserved tags

### removed
Entries that are no longer valid but preserved for audit trail:
- Incorrect entries created by scripts then deleted (10 entries from scripts 48, 51, 52)
- Tags incorrectly auto-classified then corrected
- Duplicate entries that were consolidated

**Important:** These entries document **mistakes that were corrected**, not valid folksonomy tags.

### merged
Entries where multiple old tags were consolidated:
- Plural → singular forms (`Concerts` → `concert`)
- Owner-specific → generic (`Allen's Hotel` → `hotel`)
- Variant names → standard form (`Grand Hotel` → `Grand Hotel (Sydney)`)

Automatically set when `action=merge`.

### deprecated (not yet used)
Future use: Tags marked for removal but still temporarily valid during transition period.

### historical (not yet used)
Future use: Archaic terms preserved for research but not recommended for new tagging.

---

## Entry Counts

**Total lines:** 1,848 (including header)
**Data rows:** 1,847

### By Action
- hierarchy: 1,863 (82.2%)
- synonym: 270 (11.9%)
- keep: 96 (4.2%)
- merge: 34 (1.5%)
- broader: 2 (0.1%)
- exclude: 1 (0.04%)

### By Status
- active: 1,800 (97.5%)
- merged: 34 (1.8%)
- removed: 13 (0.7%)
- deprecated: 0
- historical: 0

---

## Validation Rules

1. **Required fields:** All 5 fields must be present
2. **action field:** Must be one of: hierarchy, synonym, merge, keep, exclude, broader
3. **status field:** Must be one of: active, merged, removed, deprecated, historical
4. **Consistency:** If `action=merge`, then `status` should be `merged`
5. **Parent references:** If `action=hierarchy`, notes should contain `parent=...`
6. **UK spelling:** notes field must use UK/Australian spelling (organisation, labour, colour)

---

## Change History

| Date | Change | Script | Description |
|------|--------|--------|-------------|
| 2025-11-17 | Added banks intermediate | 63 | Added missing 'banks' polyhierarchical intermediate for 3-tier pattern consistency |
| 2025-11-17 | Getty AAT alignment (Tier 1) | 62 | Added 2 intermediate nodes for AAT alignment: financial institutions (buildings), public accommodations |
| 2025-11-17 | Final QA validation | 61 | Comprehensive validation passed with 0 errors, 9 warnings |
| 2025-11-17 | Coverage verification | 60 | Verified 100% coverage of 1,299 original tags → 1,210 controlled terms |
| 2025-11-17 | Removed exact duplicates | 59 | Removed 422 exact duplicate rows (411 patterns) |
| 2025-11-17 | Getty AAT capitalisation | 57 | Applied lowercase for 303 generic terms (864 updates) with 24 exceptions preserved |
| 2025-11-16 | Church disambiguations | 56 | Added 4 missing (building) entries, removed 1 Grand Hotel conflict |
| 2025-11-16 | Added status field | 54 | Added 5th column for lifecycle tracking |
| 2025-11-16 | Added removed entries | 55 | Added 10 audit trail entries for deleted tags |
| 2025-11-16 | Fixed US spelling | 53 | Corrected 41 organization → organisation |
| 2025-11-16 | Fixed orphaned tags | 52 | Added 8 cottage/public house synonyms |
| 2025-11-16 | Fixed bankruptcy | 51 | Removed 3 incorrect capitalized hierarchies |
| 2025-11-16 | Deduplicated | 50 | Removed 17 exact duplicates |
| 2025-11-16 | Banks disambiguation | 46 | Implemented (building)/(business) split |

See `data/*.bak` files for timestamped backups of all changes.

---

## Related Documentation

- **style-guide.md** - Capitalisation, spelling, punctuation conventions
- **CLAUDE.md** - Project instructions and workflow
- **planning/consolidation-decisions.md** - Decision audit trail
- **reports/QA_SESSION_SUMMARY.md** - Quality assurance findings
