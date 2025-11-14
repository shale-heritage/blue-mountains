# Cottages: Dual-Nature Taxonomy Implementation

**Date:** 2025-11-14
**Status:** ✅ COMPLETE

---

## Summary

Implemented dual-nature taxonomy structure for cottages following the boarding houses/hotels disambiguation pattern.

**Change:** Replaced obsolete polyhierarchical structure with disambiguated (building)/(business) qualifiers

---

## Taxonomy Changes

### Removed (4 obsolete entries):
```csv
Cottage,Cottage,hierarchy,parent=Cottages
Cottages,Cottages,hierarchy,parent=Accommodation and hospitality venues
cottage,cottage,hierarchy,parent=cottages
cottages,cottages,hierarchy,parent=accommodation buildings
```

### Added (4 new entries):
```csv
cottages (buildings),cottages (buildings),hierarchy,parent=accommodation buildings
cottage (building),cottage (building),hierarchy,parent=cottages (buildings)
cottages (businesses),cottages (businesses),hierarchy,parent=hospitality businesses
cottage (business),cottage (business),hierarchy,parent=cottages (businesses)
```

**Net change:** 0 entries (4 removed, 4 added)

---

## New Taxonomy Structure

```text
Built Environment > Accommodation buildings
└── cottages (buildings)
    └── cottage (building)

Agents > Hospitality businesses
└── cottages (businesses)
    └── cottage (business)
```

---

## Items Requiring Tags

### From Boarding Houses Analysis

**Item:** Katoomba (1888-01-07)
- **Trove URL:** http://nla.gov.au/nla.news-article100894625
- **Context:** "the various furnished cottages are all full"
- **Tags to add:**
  - cottage (building)
  - cottage (business)
- **Classification:** both - physical occupancy ("all full") indicates building capacity + rental operations indicate business

---

## Files

**Script:** `scripts/43_implement_cottages_taxonomy.py` (executed)
**Backup:** `data/tag_map_consolidated.csv.backup-20251114-222725`

---

## Getty AAT Alignment

**Cottages (buildings):** http://vocab.getty.edu/page/aat/300000339 (cottages - buildings)
**Cottages (businesses):** Hospitality rental operations

✅ Follows AAT dual-faceted pattern

---

## Next Steps

1. Apply cottage tags to Katoomba (1888-01-07) item in Zotero
2. Check if other items in library mention cottages and need tagging

---

**Implementation completed:** 2025-11-14
**Taxonomy size:** 2,226 entries (unchanged)
