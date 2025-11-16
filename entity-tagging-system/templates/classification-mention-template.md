# Classification Mention Entry Template

**Purpose:** Standard format for each entity mention in classification results, with human review section.

---

## Template Structure

```markdown
### Mention {N}: {DESCRIPTIVE_TITLE}

**Entity:** {entity_name}
**Item:** {item_title} ({item_date})
**Trove URL:** {trove_url}

**Context:**
> {extracted_context}

**Classification:** {building|organisation|both}

**Reasoning:** {2-3 sentences explaining classification with specific indicators}

---

**HUMAN REVIEW:**

- [ ] Confirm classification
- [ ] Change to: [ ] building  [ ] organisation  [ ] both

**Notes:**
{Space for reviewer comments, corrections, alternative tags}

**Additional/Alternative Tags:**
{Space for additional tags if needed, e.g., specific establishment names, mis-tagging corrections}

---
```

---

## Usage Notes

**Checkboxes:**
- Use `[ ]` for unchecked, `[x]` for checked
- "Confirm classification" - check if AI classification is correct
- "Change to" options - check appropriate box if correction needed
- Only one "Change to" box should be checked (mutually exclusive)

**Notes field:**
- Free-form text for human reviewer
- May include:
  - Reasoning for disagreement
  - Context Claude missed
  - Ambiguity notes
  - Cross-references

**Additional/Alternative Tags field:**
- Specific establishment names not captured
- Tags for mis-tagged items (when entity shouldn't be tagged at all)
- Related tags that should be added
- Format: One tag per line or comma-separated

---

## Design Rationale

**"Confirm" vs separate checkboxes:**
- **Chosen:** Confirm/Change model
- **Rationale:** Faster for reviewer - single checkbox for majority (correct) cases
- **Alternative considered:** Three separate checkboxes (building/organisation/both)
  - Would require checking one box for every entry (more work)
  - Confirm model assumes AI is usually correct (empirically true: 94-98% accuracy)

**Unambiguous for Claude:**
- Empty checkboxes = not yet reviewed
- [x] Confirm = AI correct
- [x] Change to + checked box = AI incorrect, use checked classification
- Can parse mechanically: `if 'x] Confirm'` vs `if 'x] Change to'` + which box checked

**Generic across entity types:**
- No entity-specific fields
- Works for hotels, churches, schools, any dual-nature entity
- Consistent review experience

---

## Example (Completed)

```markdown
### Mention 18: Committee meeting about new building

**Entity:** School of Arts
**Item:** Town Talk (1903-03-13)
**Trove URL:** http://nla.gov.au/nla.news-article188871927

**Context:**
> A mooting of the committee of the local School of Arts was to have been held at the room on Tuesday evening. The night was somewhat damp and no quorum turned up. The interest shown by some of the committee seems very slight, especially as important business in connection with new building, &c., had to be discussed.

**Classification:** organisation

**Reasoning:** Organisational decision-making about building project (agency indicators: committee governance, capital project planning)

---

**HUMAN REVIEW:**

- [ ] Confirm classification
- [x] Change to: [ ] building  [x] organisation  [x] both

**Notes:**
Meeting was held "at the room" (elliptical reference to School of Arts building - spatial indicator). Discussion topic includes "new building" (physical infrastructure). Should be BOTH.

**Additional/Alternative Tags:**
{None needed}

---
```

---

## Version History

- **v1.0** (2025-11-15): Initial template creation
  - Confirm/Change checkbox model
  - Notes and additional tags fields
  - Generic design for all entity types
