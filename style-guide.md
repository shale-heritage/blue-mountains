# Blue Mountains Taxonomy Style Guide

**Version:** 1.0
**Date:** 2025-11-16
**Status:** Official taxonomy style standard

---

## Purpose

This guide defines the capitalisation, spelling, punctuation, and formatting conventions for the Blue Mountains Historical Society controlled vocabulary taxonomy. All taxonomy entries in `data/tag_map_consolidated.csv` must conform to these standards.

---

## 1. Capitalisation Rules

### 1.1 Primary Facets (Getty AAT Alignment)

**Rule:** Title Case

**Examples:**
- Built Environment
- Agents
- Activities
- Events
- Associated Concepts
- Materials
- Places
- Information Forms

**Rationale:** Aligns with Getty AAT facet naming conventions.

---

### 1.2 Generic Terms (Common Nouns)

**Rule:** Lowercase

**Applies to:**
- Generic singular leaf nodes (e.g., `hotel`, `church`, `school`)
- Generic plural parents (e.g., `hotels`, `churches`, `schools`)
- Occupation terms (e.g., `hotelier`, `clergyman`, `teacher`)
- Material terms (e.g., `beer`, `wine`, `whisky`, `timber`)
- Activity terms (e.g., `drinking`, `gambling`, `advertising`)
- Abstract concepts (e.g., `death`, `bankruptcy`, `marriage`)

**Examples:**
```
hotels (plural parent - organisational)
├── hotel (singular generic leaf - taggable)
├── Grand Hotel (specific named instance)
└── Carrington Hotel (specific named instance)
```

**Exception:** When a common noun is part of a proper noun, capitalise it:
- `Railway Hotel Katoomba` (proper noun)
- `Commercial Bank of Australia` (proper noun)

---

### 1.3 Proper Nouns (Named Entities)

**Rule:** Title Case for each significant word

**Applies to:**
- Named establishments: `Grand Hotel`, `St Hilda's Church`, `Katoomba School of Arts`
- Geographic locations: `Katoomba`, `Mount Victoria`, `Nellie's Glen`
- Person names: `Mr Joseph Nimmo`, `Dr Prangley`, `Reverend Smith`
- Organisation names: `Commercial Bank of Australia`, `Postal Department`
- Event names: `Great War`, `Federation`

**Articles, prepositions, conjunctions:** Lowercase unless first word
- `Church of England Katoomba` (not "Church Of England Katoomba")
- `School of Arts` (not "School Of Arts")

---

### 1.4 Intermediate Categories and Facet Children

**Rule:** Lowercase

**Examples:**
- `accommodation and hospitality venues`
- `commercial buildings`
- `financial institutions`
- `cultural societies`
- `economic activities`

**Exception:** Thematic groupings use Title Case + marker:
- `Tourism & Accommodation - THEMATIC`
- `Alcohol & Temperance - THEMATIC`
- `Economy & Labour - THEMATIC`

---

### 1.5 Disambiguation Qualifiers

**Rule:** Lowercase in parentheses

**Standard qualifiers:**
- `(building)` - physical structure aspect
- `(business)` - commercial operation aspect
- `(organisation)` - institutional/corporate entity aspect
- `(venue)` - event/activity location aspect

**Examples:**
- `hotel (building)` - physical premises
- `hotel (business)` - hospitality operation
- `School of Arts (organisation)` - cultural society
- `School of Arts (venue)` - hall/meeting space

**Spelling:** Use UK spelling: `(organisation)` not `(organization)`

---

### 1.6 Honorifics and Titles

**Rule:** Title Case, abbreviated where conventional

**Standard forms:**
- `Mr` (not `Mister`)
- `Mrs`, `Miss`, `Ms`
- `Dr` (not `Doctor`)
- `Reverend` (full form), `Rev` (abbreviated - use full)
- `Major`, `Captain`, `Colonel` (military ranks)
- `Sir`, `Dame` (knighthood)

**Examples:**
- `Mr Joseph Nimmo`
- `Dr Prangley`
- `Reverend Smith`
- `Major Sir John Jamison`

---

### 1.7 Acronyms and Initialisms

**Rule:** All capitals, without periods (if usage includes instances with periods, include that form as synonym)

**With periods (historical conventional):**
- `AKO & M Company` (Australian Kerosene Oil and Mineral Company)

**Without periods (modern conventional):**
- `NSW` (New South Wales)
- `ANZAC` (Australian and New Zealand Army Corps)

**Preference:** Use expanded form as preferred term, acronym as synonym:
```csv
Australian Kerosene Oil and Mineral Company,Australian Kerosene Oil and Mineral Company,hierarchy,parent=...
A.K.O. & M. Company,Australian Kerosene Oil and Mineral Company,synonym,Historical abbreviated form
```

---

## 2. Spelling Conventions

### 2.1 UK/Australian Spelling Standard

**Rule:** Use UK/Australian spelling throughout

**Common differences:**

| ❌ US Spelling | ✅ UK/Australian Spelling |
|---------------|-------------------------|
| color | colour |
| behavior | behaviour |
| organization | organisation |
| analyze | analyse |
| optimize | optimise |
| labor | labour |
| center | centre |
| theater | theatre |
| defense | defence |
| license (noun) | licence (noun) |
| license (verb) | license (verb) |
| practice (noun) | practice (noun) |
| practice (verb) | practise (verb) |

**Key terms in taxonomy:**
- `organisation` (not organization)
- `labour` (not labor)
- `colour` (not color)
- `behaviour` (not behavior)
- `licence` (noun - publican's licence)
- `license` (verb - to license a hotel)

---

### 2.2 Australian Terminology

**Prefer Australian terms where they differ from British:**

| British | Australian (Preferred) |
|---------|----------------------|
| pub | public house |
| shop | store (when referring to retail premises) |
| lorry | truck (but see 2.3 below) |

---

### 2.3 Historical Terminology Preservation

**Rule:** Preserve historical terms as used in sources, even if archaic

**Examples:**
- `truck system` - 19th century exploitative labour practice (not modern trucking)
- `temperance` - historical abstinence movement
- `draper` - historical textile merchant (not "fabric store")
- `cordial` - Australian term for non-alcoholic fruit drink

**Approach:** Historical term as preferred, modern equivalent as synonym if needed.

---

## 3. Punctuation Conventions

### 3.1 Minimal Punctuation

**Rule:** Use minimal punctuation in tag names

**Avoid:**
- Periods at end of tags
- Quotation marks (unless part of proper noun)
- Commas (except in inverted names or lists)

**Examples:**
✅ `Mr Joseph Nimmo`
❌ `Mr. Joseph Nimmo.`

✅ `School of Arts`
❌ `"School of Arts"`

---

### 3.2 Apostrophes in Proper Nouns

**Rule:** Preserve apostrophes in proper nouns where they appear in sources

**Examples:**
- `St Hilda's Church` (possessive)
- `Odd Fellows' Hall` (plural possessive)
- `Nellie's Glen` (possessive)
- `Allen's Hotel` (possessive)

**BUT:** When possessive form refers to generic entity, map to non-possessive:
```csv
Allen's Hotel,hotel,merge,Possessive form - Allen is hotelier (person tag), hotel is establishment
```

---

### 3.3 Ampersands vs "and"

**Rule:** Context-dependent

**Use ampersand (&):**
- In official organisation names: `Commercial Bank of Australia & New Zealand`
- In company names where conventional: `AKO & M Company`

**Use "and":**
- In descriptive phrases: `accommodation and hospitality venues`
- In generic terms: `hotels and boarding houses`
- In thematic facet names: `Tourism and Accommodation - THEMATIC`


---

### 3.4 Hyphens in Compound Terms

**Rule:** Hyphenate compound modifiers before nouns

**Examples:**
✅ `alcohol-related venues`
❌ `alcohol related venues`

✅ `dual-nature entities`
❌ `dual nature entities`

✅ `full-text search`
❌ `full text search`

**BUT:** No hyphen when not modifying:
✅ `the venue is alcohol related`
✅ `entities with dual nature`

---

### 3.5 Parenthetical Qualifiers

**Rule:** Lowercase qualifier in parentheses, no space before opening parenthesis

**Format:** `term (qualifier)`

**Examples:**
- `hotel (building)`
- `hotel (business)`
- `School of Arts (organisation)`
- `School of Arts (venue)`

**NOT:**
- `hotel(building)` - missing space
- `hotel (Building)` - incorrect capitalisation
- `hotel [building]` - wrong brackets

---

## 4. Formatting Conventions

### 4.1 Date Formatting

**Rule:** Context-dependent formatting

**Machine-readable contexts (CSV files, metadata, timestamps, filenames):**
- Use ISO format: `YYYY-MM-DD`
- Examples: `1893-06-02`, `2025-11-16`
- Rationale: Sortable, unambiguous, interoperable with Zotero and database systems

**Human-readable prose (notes field, documentation, markdown reports):**
- Use Day Month Year format: no leading zeros, no commas
- Examples: `2 June 1893`, `15 October 1889`
- NOT: `June 2, 1893` (US format)
- NOT: `02 June 1893` (leading zero)

**Filenames and backups:**
- Always ISO: `backup_20251116.csv`, `report_2025-11-16.md`
- Ensures correct chronological sorting

---

### 4.2 Geographic Qualifiers

**Rule:** Use when disambiguation necessary, format: `Name, Location`

**Examples:**
- `Railway Hotel Katoomba` (location as part of proper noun)
- `Post Office, Katoomba` (when multiple Post Offices exist)

**Avoid:** Redundant geographic qualifiers when name is unique:
✅ `Grand Hotel` (if only one in collection)
❌ `Grand Hotel, Katoomba` (unless disambiguation needed)

---

### 4.3 Inverted Names (Person Names)

**Rule:** Natural order (Given Family), not inverted

**Examples:**
✅ `Mr Joseph Nimmo`
❌ `Nimmo, Joseph Mr`

**Exception:** When source uses inverted form historically, preserve in notes but use natural order as preferred term.

---

## 5. Leaf-Node Pattern Conventions

### 5.1 Standard Structure

```
Plural Parent (organisational - never tagged)
├── singular generic (taggable - for unspecified items)
├── Specific Named Instance 1 (taggable)
├── Specific Named Instance 2 (taggable)
└── Specific Named Instance N (taggable)
```

**Capitalisation in this pattern:**
- Plural parent: lowercase (`hotels`, `churches`, `schools`)
- Singular generic: lowercase (`hotel`, `church`, `school`)
- Specific named: Title Case (`Grand Hotel`, `St Hilda's Church`, `Katoomba School of Arts`)

---

### 5.2 Exception: No Singular Generic When Unnecessary

**Do NOT create singular generics when:**
- Entities are always named/specific in sources
- Example: Government authorities, regulatory bodies

**Example:**
```
postal authorities (parent)
└── Postal Department (specific - no generic "postal authority")
```

---

## 6. Synonym Conventions

### 6.1 Synonym Notes Format

**Rule:** Concise explanation of relationship

**Template:** `[Variant type] - [explanation]`

**Examples:**
- `Capitalized variant - maps to building aspect`
- `Abbreviated form - use full Peckman Brothers`
- `Possessive form - refers to hotel run by Allen`
- `Historical term for the truck system - 19th century exploitative labour practice`

---

### 6.2 Capitalisation Synonyms

**Rule:** Capitalised variants point to lowercase preferred term (for generic terms)

**Example:**
```csv
bank,bank,hierarchy,parent=...
Bank,bank (building),synonym,Capitalized variant - maps to building aspect
Bank,bank (business),synonym,Capitalized variant - maps to business aspect
```

---

## 7. Disambiguation Conventions

### 7.1 When to Disambiguate

**Use (building)/(business)/(organisation) qualifiers when:**
- Entity has dual-nature (both physical and organisational aspects)
- Entity appears in multiple facets (polyhierarchical)
- Aligns with project pattern (hotels, churches, schools, banks)

**Examples requiring disambiguation:**
- Hotels: physical premises + hospitality business
- Banks: building + financial institution
- Churches: building + religious organisation
- Schools of Arts: hall/venue + cultural society
- Public houses: licensed premises + alcohol business

---

### 7.2 Disambiguation Qualifier Selection

**Use (building) when:**
- Refers to physical structure, premises, architecture
- Spatial/location context ("at the hotel", "in the church")
- Building features mentioned (rooms, architecture)

**Use (business) when:**
- Refers to commercial operations
- Services provided, trade conducted
- Business establishment, closure, management

**Use (organisation) when:**
- Refers to institutional entity, corporate body
- Membership, governance, activities
- Non-commercial associations (churches, societies)

**Use (venue) when:**
- Emphasizes function as event/activity location
- Meeting place, performance space
- Typically subordinate to (building) - use sparingly

---

## 8. Thematic Facet Conventions

### 8.1 Thematic Marker Format

**Rule:** Title Case + ` - THEMATIC` suffix

**Examples:**
- `Tourism & Accommodation - THEMATIC`
- `Alcohol & Temperance - THEMATIC`
- `Justice & Crime - THEMATIC (virtual grouping)`

**Purpose:** Distinguishes thematic cross-cutting groupings from primary Getty AAT facets

---

### 8.2 When to Use Thematic Facets

**Use for:**
- Domain-based groupings (tourism, alcohol, mining)
- Cross-facet collections for exhibitions/research
- Thematic browsing (not structural hierarchy)

**Do not use for:**
- Primary facet structure (use Getty AAT facets)
- Replacing proper hierarchical relationships

---

## 9. Notes Field Conventions

### 9.1 Notes Field Purpose

**Use for:**
- Rationale for mapping decisions
- Evidence from sources (brief quotes)
- Cross-references to documentation
- Disambiguation reasoning

**Keep concise:** 1-2 sentences maximum

---

### 9.2 Notes Field Spelling

**Rule:** UK/Australian spelling applies to notes field

**Examples:**
✅ `Historical term for organisation - 19th century labour practice`
❌ `Historical term for organization - 19th century labor practice`

---

## 10. Special Cases

### 10.1 Truck vs Trucking

**Truck system:**
- Historical exploitative labour practice
- Tag: `truck system`
- Synonym: `trucking` → `truck system`

**NOT commercial trucking/logistics** (removed from taxonomy)

---

### 10.2 Bankruptcy vs Bank

**Separate unrelated concepts:**
- `bank` (financial institution)
- `bankruptcy` (legal/economic status)
- Marked as: `bank,bank,keep,Substring coincidence - semantically unrelated concepts`

**Prevent:** Substring false matches in search/tagging

---

### 10.3 Dual-Nature Entities

**Current strategic approach:**
- Use (building)/(business)/(organisation) disambiguation
- Create separate qualified tags for each facet
- Aligns with hotels, public houses, schools of arts, churches, banks pattern

**Under review:**
- Getty AAT alignment (Phase 1.3)
- May affect future dual-nature handling
- See CLAUDE.md lines 42-140 for detailed analysis

---

## 11. Validation Checklist

Before committing taxonomy changes, verify:

- [ ] All generic terms lowercase
- [ ] All proper nouns Title Case
- [ ] UK/Australian spelling throughout (including notes)
- [ ] Disambiguation qualifiers lowercase in parentheses
- [ ] No trailing punctuation
- [ ] Apostrophes preserved in proper nouns
- [ ] Hyphens in compound modifiers
- [ ] Date format: ISO YYYY-MM-DD for CSV/metadata, Day Month Year for prose
- [ ] Thematic facets have ` - THEMATIC` marker
- [ ] Synonym notes concise and clear
- [ ] Leaf-node pattern followed (where applicable)

---

## 12. References

- **Getty AAT:** https://vocab.getty.edu/
- **CLAUDE.md:** Project-specific instructions (lines 1-431)
- **TAGGING_GUIDELINES.md:** Leaf-node pattern and classification heuristics
- **Macquarie Dictionary:** Australian spelling authority
- **Oxford English Dictionary:** UK spelling authority

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-16 | Initial style guide creation | Claude Code |

---

**Questions or edge cases:** Document in `planning/consolidation-decisions.md` and update this guide as needed.
