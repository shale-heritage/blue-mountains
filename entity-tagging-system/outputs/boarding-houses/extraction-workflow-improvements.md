# Boarding Houses: Extraction Workflow Improvements

**Date:** 2025-11-14
**Issue:** Script 38 failed to extract 6 of 8 boarding house items due to variant terminology
**Status:** Workflow recommendations documented

---

## Problem Analysis

### Root Cause

Script `38_classify_entities_with_claude.py` searches for exact tag name matches in full text:

```python
pattern = re.compile(re.escape(entity_name).replace(r"\'", r"'?"), re.IGNORECASE)
```

This pattern:
- ✅ Handles apostrophe variants (e.g., "School of Arts" vs "School of Arts")
- ❌ Doesn't handle hyphen vs space variants (e.g., "boarding-house" vs "boarding house")
- ❌ Doesn't handle singular vs plural variants (e.g., "boarding house" vs "boarding houses")

### Observed Variants in Corpus

From 8 tagged items:
- **"boarding-house"** (singular, hyphenated): 5 occurrences
- **"boarding houses"** (plural, two words): 1 occurrence
- **"boarding-houses"** (plural, hyphenated): 2 occurrences

Tag name used: "boarding houses" (plural, two words)

**Result:** Only 1 of 8 items matched the exact tag name pattern

---

## Proposed Solutions

### Option 1: Flexible Regex Pattern (Recommended)

Modify `extract_context()` function to handle common morphological variants:

```python
def extract_context(text: str, entity_name: str, context_chars: int = 400) -> str:
    """
    Extract context around first mention of entity.

    Handles variants:
    - Hyphen vs space (e.g., "boarding-house" vs "boarding house")
    - Singular vs plural (e.g., "house" vs "houses")
    - Apostrophe variants (existing)
    """
    import re

    # Normalise entity name for flexible matching
    # Convert spaces/hyphens to flexible pattern
    pattern_base = re.escape(entity_name).replace(r"\'", r"'?")
    pattern_base = pattern_base.replace(r"\ ", r"[\s-]")  # space or hyphen
    pattern_base = pattern_base.replace(r"\-", r"[\s-]")  # hyphen or space

    # Handle plural variants (optional 's' at word boundaries)
    # e.g., "boarding house" also matches "boarding houses"
    # But also "boarding-house" matches "boarding-houses"
    pattern_base = re.sub(r'(s\\b|s\$)', r's?', pattern_base)

    pattern = re.compile(pattern_base, re.IGNORECASE)
    match = pattern.search(text)

    if not match:
        return None

    # ... rest of function unchanged
```

**Advantages:**
- Handles orthographic variants automatically
- No need to manually list all variants
- Catches unexpected variant forms
- Minimal code change

**Disadvantages:**
- More complex regex (may match false positives in rare cases)
- Needs testing across entity types

### Option 2: Expanded Entity Name Lists

Add all known variants to `entity_names` dictionary in script 38:

```python
'boarding-houses': [
    'Orama Boarding House',
    'boarding house',      # singular, two words
    'Boarding house',      # capitalised
    'boarding houses',     # plural, two words
    'Boarding houses',     # capitalised
    'boarding-house',      # singular, hyphenated
    'Boarding-house',      # capitalised
    'boarding-houses',     # plural, hyphenated
    'Boarding-houses',     # capitalised
],
```

**Advantages:**
- Explicit control over what matches
- No regex complexity
- Easy to understand and maintain

**Disadvantages:**
- Must manually identify all variants for each entity type
- Verbose entity lists
- May still miss unexpected variants
- Duplicate work (case variants already handled by case-insensitive search)

### Option 3: Natural Language Extraction (Advanced)

Use Claude's NLU capabilities to extract relevant contexts without exact pattern matching:

```python
def extract_context_with_nlp(text: str, entity_type: str, context_chars: int = 400) -> list:
    """
    Use Claude to identify mentions of entity type in text.

    Returns list of (mention_text, context) tuples.
    """
    # Prompt Claude to:
    # 1. Identify all mentions of entity_type in text
    # 2. Extract context around each mention
    # 3. Return structured data

    # This would handle:
    # - All orthographic variants
    # - Metonymic references (e.g., "the establishment" referring to boarding house)
    # - Implied mentions (e.g., "Mrs. Gillen's place")
```

**Advantages:**
- Most flexible and robust
- Handles semantic understanding (metonymy, coreference)
- Language-agnostic (works across entity types)
- Catches all relevant mentions regardless of form

**Disadvantages:**
- Requires API calls (slower, costs)
- More complex implementation
- May be overkill for simple orthographic variants
- Harder to debug/validate

---

## Recommendation

**Use Option 1 (Flexible Regex)** as primary solution:

1. **Immediate benefit:** Handles hyphen/space and plural variants automatically
2. **Low complexity:** Single regex modification, well-tested pattern
3. **Good balance:** More robust than exact matching, simpler than NLU

**Fallback to Option 3 (NLU) for complex cases:**
- When entity has many synonyms (e.g., "School of Arts" = "Athenaeum" = "Literary Institute")
- When metonymy is common (e.g., "the church" meaning the religious organisation)
- When manual variant listing becomes unwieldy

---

## Implementation

### Modified `extract_context()` Function

```python
def extract_context(text: str, entity_name: str, context_chars: int = 400) -> str:
    """
    Extract context around first mention of entity.

    Handles common morphological variants:
    - Hyphen vs space: "boarding-house" matches "boarding house"
    - Singular vs plural: "boarding house" matches "boarding houses"
    - Apostrophe variants: "School of Arts" matches "School of Arts"

    Returns:
        Context string, or None if entity not found
    """
    import re

    # Build flexible pattern
    pattern_str = re.escape(entity_name)

    # Handle apostrophe variants (existing)
    pattern_str = pattern_str.replace(r"\'", r"'?")

    # Handle hyphen/space variants (NEW)
    pattern_str = pattern_str.replace(r"\ ", r"[\s-]")  # space → space or hyphen
    pattern_str = pattern_str.replace(r"\-", r"[\s-]")  # hyphen → hyphen or space

    # Handle plural variants (NEW)
    # Make trailing 's' optional at word boundaries
    pattern_str = re.sub(r's(\\b|$)', r's?\\1', pattern_str)

    pattern = re.compile(pattern_str, re.IGNORECASE)
    match = pattern.search(text)

    if not match:
        return None

    start, end = match.span()

    # Extract surrounding text
    context_start = max(0, start - context_chars)
    context_end = min(len(text), end + context_chars)

    context = text[context_start:context_end]

    # Try to clip at sentence boundaries
    if context_start > 0:
        first_period = context.find('. ')
        if 0 < first_period < 50:
            context = context[first_period + 2:]

    last_period = context.rfind('. ')
    if last_period > len(context) - 50:
        context = context[:last_period + 1]

    return context.strip()
```

### Testing Strategy

1. **Test with boarding houses corpus:**
   - Should now match all 7 valid items (excluding mis-tagged item)
   - Verify no false positives

2. **Test with educational schools corpus:**
   - Should still match all previously matched items
   - Verify plural handling doesn't break existing functionality

3. **Test with hotels corpus:**
   - Verify existing matches still work
   - Check for any false positives from flexible pattern

---

## Validation Results (To Be Completed)

After implementing changes, document:

```text
Entity Type: boarding-houses
Items tagged: 8
Items with text: 8 (1 mis-tagged, no mention)
Items matched before: 2/7 valid items (28.6%)
Items matched after: _/7 valid items (___%)

False positives: _ (list any)
False negatives: _ (list any)
```

---

## Lessons Learned

### For Future Entity Extraction

1. **Check orthographic variants early:** Before running extraction, search for common variants:
   - Hyphenated vs two-word forms
   - Singular vs plural
   - Alternative spellings (UK/US, historical variations)

2. **Validate extraction coverage:** After running script 38, check:
   - What percentage of tagged items were extracted?
   - If <80%, investigate why (variants? no text? mis-tagged?)

3. **Preview full text samples:** Manually check 2-3 items to see actual terminology used in corpus

4. **Use NLU for ambiguous cases:** When variants are semantic (synonyms, metonymy), regex won't suffice

### For Tagging Consistency

1. **Standardise tag forms:** Use consistent capitalisation and hyphenation in tags
2. **Document variant forms:** Note in taxonomy which morphological variants exist
3. **Consider lemmatisation:** Generic tags should be lemma form (e.g., "boarding house" not "boarding houses")

---

## Related Issues

- Educational schools had similar issue with annotations vs notes (resolved via manual review)
- Hotels may have similar variant issues not yet discovered
- Churches likely have variant forms ("Church of England" vs "C of E", etc.)

**Recommendation:** Apply flexible regex pattern globally across all entity types in script 38

---

**Status:** Recommendations documented, awaiting implementation approval
