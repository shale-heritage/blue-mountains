# Boarding Houses: Taxonomy Additions Needed

**Date:** 2025-11-14
**Status:** Ready for implementation

---

## Summary

Two new specific boarding house establishments need to be added to the taxonomy:
1. **Mrs. Gillen's boarding-house** (building only)
2. **Miss Kelly's boarding house** (both building and business)

---

## Current Taxonomy Structure

Boarding houses already has complete dual-nature structure:

```text
Built Environment > Accommodation buildings > boarding houses (buildings)
├── boarding house (building)
└── Orama Boarding House (building)

Agents > Hospitality businesses > boarding houses (businesses)
├── boarding house (business)
└── Orama Boarding House (business)
```

---

## Additions Required

### 1. Mrs. Gillen's boarding-house

**Evidence:** Megalong Valley (1893-06-16)
- Classification: building only
- Context: Spatial movement reference ("crossing from Mrs. Gillen's boarding-house")

**Taxonomy entries to add:**

```csv
Mrs. Gillen's boarding-house (building),Mrs. Gillen's boarding-house (building),hierarchy,parent=boarding houses (buildings)
```

**Note:** Only building variant needed - no business context found in corpus

---

### 2. Miss Kelly's boarding house

**Evidence:** Mountain Mixtures (1891-11-20)
- Classification: both
- Context: Construction completion + owner-operator setup

**Taxonomy entries to add:**

```csv
Miss Kelly's boarding house (building),Miss Kelly's boarding house (building),hierarchy,parent=boarding houses (buildings)
Miss Kelly's boarding house (business),Miss Kelly's boarding house (business),hierarchy,parent=boarding houses (businesses)
```

**Note:** Both variants needed - construction (building) and operations (business)

---

## Implementation Script

```python
#!/usr/bin/env python3
"""
Add Mrs. Gillen's and Miss Kelly's boarding houses to taxonomy.
"""

import csv
from pathlib import Path
from datetime import datetime

# Paths
DATA_DIR = Path('data')
TAXONOMY_FILE = DATA_DIR / 'tag_map_consolidated.csv'
BACKUP_DIR = DATA_DIR

def add_boarding_house_establishments():
    """Add specific boarding house establishments to taxonomy."""

    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_file = BACKUP_DIR / f'tag_map_consolidated.csv.backup-{timestamp}'

    print(f"Creating backup: {backup_file}")
    with open(TAXONOMY_FILE, 'r') as src, open(backup_file, 'w') as dst:
        dst.write(src.read())

    # Read existing taxonomy
    with open(TAXONOMY_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    print(f"Current taxonomy size: {len(rows)} entries")

    # New entries
    new_entries = [
        ("Mrs. Gillen's boarding-house (building)",
         "Mrs. Gillen's boarding-house (building)",
         "hierarchy",
         "parent=boarding houses (buildings)"),
        ("Miss Kelly's boarding house (building)",
         "Miss Kelly's boarding house (building)",
         "hierarchy",
         "parent=boarding houses (buildings)"),
        ("Miss Kelly's boarding house (business)",
         "Miss Kelly's boarding house (business)",
         "hierarchy",
         "parent=boarding houses (businesses)"),
    ]

    # Check for duplicates
    existing_tags = {row[0] for row in rows}
    to_add = []

    for entry in new_entries:
        if entry[0] in existing_tags:
            print(f"⚠ Already exists: {entry[0]}")
        else:
            to_add.append(entry)
            print(f"✓ Will add: {entry[0]}")

    if not to_add:
        print("\nNo new entries to add (all already exist)")
        return

    # Add new entries
    rows.extend(to_add)

    # Write updated taxonomy
    with open(TAXONOMY_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\n✓ Added {len(to_add)} new entries")
    print(f"Final taxonomy size: {len(rows)} entries")
    print(f"Backup saved to: {backup_file}")

if __name__ == '__main__':
    add_boarding_house_establishments()
```

---

## Verification Checklist

After running script:

- [ ] Mrs. Gillen's boarding-house (building) appears under boarding houses (buildings)
- [ ] Miss Kelly's boarding house (building) appears under boarding houses (buildings)
- [ ] Miss Kelly's boarding house (business) appears under boarding houses (businesses)
- [ ] No duplicate entries created
- [ ] Backup file created successfully
- [ ] Taxonomy size increased by 3 entries

---

## Alternative: Manual Addition

If script not used, manually add these 3 lines to `data/tag_map_consolidated.csv`:

```csv
Mrs. Gillen's boarding-house (building),Mrs. Gillen's boarding-house (building),hierarchy,parent=boarding houses (buildings)
Miss Kelly's boarding house (building),Miss Kelly's boarding house (building),hierarchy,parent=boarding houses (buildings)
Miss Kelly's boarding house (business),Miss Kelly's boarding house (business),hierarchy,parent=boarding houses (businesses)
```

---

**Status:** Ready for implementation
**Impact:** +3 taxonomy entries
**Applications affected:** 2 items (Megalong Valley, Mountain Mixtures 1891-11-20)
