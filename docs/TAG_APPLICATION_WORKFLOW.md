# Tag Application Workflow

**Status:** Mapping file complete, ready for API application  
**Last Updated:** 2025-10-30  
**Total Items:** 97 items ready to retag in Zotero

---

## Overview

This document describes the tag application workflow - how we track tag changes and apply them to the Zotero library via API.

### The Problem We Solved

Previously, we created analysis reports and decision documents for tag changes, but we **didn't have a machine-readable mapping** of which Zotero items needed which tag changes.

### The Solution

We now have a **comprehensive tag application mapping file** (`data/tag_application_mapping.csv`) with 97 items ready to retag.

---

## Mapping File Structure

**File:** `data/tag_application_mapping.csv`

**Columns:**
- `title`: Article title
- `date`: Publication date
- `publication`: Publication name
- `remove_tags`: Tags to remove (pipe-separated)
- `add_tags`: Tags to add (pipe-separated)
- `source`: Origin decision document
- `notes`: Additional context

---

## Source Documents

1. **Hotel Licensing** (13 items) - `reports/hotel_licensing_action_plan.md`
2. **Alcohol** (12 items) - `reports/alcohol_rationalisation_report.md`
3. **Accommodation** (63 items, 32 modified) - `reports/ACCOMMODATION_TAGS_APPROVAL.md`
4. **Post Tags** (9 items) - `reports/post_tag_action_plan.md`

---

## Next Steps

1. ✅ Parse all decision documents
2. ✅ Create mapping file (97 items)
3. ✅ Review cc-interactions logs
4. ⏳ Create API application script
5. ⏳ Execute changes in Zotero

