# Coverage Verification Report

**Generated:** 2025-11-17
**Source:** `data/tag_map_consolidated.csv`

---

## Summary

- **Total entries:** 1,844
- **Active entries:** 1,797 (97.5%)
- **Unique original tags:** 1,299
- **Unique controlled terms:** 1,221
- **Coverage ratio:** 94.0%

---

## Mapping Breakdown

### By Action

- **hierarchy:** 1,447 (78.5%)
- **synonym:** 264 (14.3%)
- **keep:** 96 (5.2%)
- **merge:** 34 (1.8%)
- **broader:** 2 (0.1%)
- **exclude:** 1 (0.1%)

### By Status

- **active:** 1,797 (97.5%)
- **merged:** 34 (1.8%)
- **removed:** 13 (0.7%)

### Mapping Types

- **Self-mapped** (old_tag == new_tag): 1,204
- **Redirected** (old_tag → new_tag): 181

---

## Sample Redirections (First 20)

Examples of folksonomy tags mapped to controlled vocabulary:

- `A.K.O. & M. Company` → `Australian Kerosene Oil and Mineral Company` (synonym)
- `Alcohol` → `alcohol consumption & behaviour` (synonym)
- `Allen's Hotel` → `hotel` (merge)
- `Anglican` → `Church of England` (synonym)
- `Anglican Church Katoomba` → `Church of England Katoomba` (synonym)
- `Assault` → `assault` (synonym)
- `Australian Kerosene Shale and Oil Company` → `Australian Kerosene Oil and Mineral Company` (synonym)
- `Ball` → `ball` (synonym)
- `Belgravia Hotel` → `Belgravia Hotel (building)` (synonym)
- `Belgravia Hotel` → `Belgravia Hotel (business)` (synonym)
- `Bigamy` → `bigamy` (synonym)
- `Blackheath Catholic Church` → `Roman Catholic Church Blackheath` (synonym)
- `Brown's Hotel` → `hotel` (merge)
- `Carrington Hotel` → `Carrington Hotel (building)` (synonym)
- `Carrington Hotel` → `Carrington Hotel (business)` (synonym)
- `Centennial Hotel` → `Centennial Hotel (building)` (synonym)
- `Centennial Hotel` → `Centennial Hotel (business)` (synonym)
- `Chess and Draughts Club` → `chess and draughts club` (synonym)
- `Coal` → `coal` (synonym)
- `Colliery` → `coal mine (facility)` (synonym)

... and 161 more redirections

---

## Orphaned Tags

✓ **No orphaned tags found.**

All original folksonomy tags have been successfully mapped to the controlled vocabulary.

---

## Methodology

**Coverage verification checks:**

1. All `old_tag` values have corresponding `new_tag` mappings
2. Mappings are marked as `active` status
3. Appropriate `action` field values (hierarchy, synonym, merge, keep)
4. No gaps in folksonomy → controlled vocabulary transformation

**Interpretation:**

- **Self-mapped:** Original tag kept as-is in controlled vocabulary
- **Redirected:** Original tag normalized/consolidated to preferred term
- **Coverage ratio:** Proportion of controlled terms vs original tags

