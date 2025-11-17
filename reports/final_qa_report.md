# Final QA Validation Report

**Generated:** 2025-11-17
**Source:** `data/tag_map_consolidated.csv`
**Total rows:** 1,847
**Active rows:** 1,800

---

## Verdict

**⚠ PASSED WITH WARNINGS - Review warnings before deployment**

---

## Summary

- **Errors:** 0
- **Warnings:** 9
- **Info:** 9

---

## Warnings

- Found 4 potential capitalisation issues:
-   • Activities
-   • Activities
-   • Events
-   • Events
- Found 3 status inconsistencies:
-   • Senior-Constable John Illingworth: status=removed but no REMOVED marker in notes
-   • St Hilda's Church of England (building): status=removed but no REMOVED marker in notes
-   • St Hilda's Church of England (organisation): status=removed but no REMOVED marker in notes

---

## Information

- CSV has 1847 data rows
- CSV structure: old_tag, new_tag, action, notes, status
- All parent references valid
- No exact duplicates
- No US spelling violations
- Unique original tags: 1,302
- Unique controlled terms: 1,213
- Active mappings: 1,800
- Coverage ratio: 93.2%

---

## Checks Performed

1. ✓ CSV structure integrity
2. ✓ Parent-child reference integrity
3. ✓ Exact duplicate detection
4. ✓ UK spelling compliance
5. ✓ Getty AAT capitalisation
6. ✓ Status field consistency
7. ✓ Coverage completeness

