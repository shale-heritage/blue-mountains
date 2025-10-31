# Horses Tag Context Analysis

**Date:** 2025-10-31

**Purpose:** Determine whether items tagged with "Horses" should be:
1. Moved to Agents > Animals > Horses (horses as animals/agents)
2. Tagged with Recreation activities > Horseback riding (the activity)
3. Both

---

## Summary

**Total items analysed:** 19 items tagged with "Horses"

**Findings:**

- **All items** refer to horses as animals/agents (transport, property, wild animals)
- **9 items** (47%) specifically describe horseback riding as an activity
- **1 item** has false positive ("22-horse power" refers to motor car, not horses)

**Recommendation:**

1. **Remove "Horses" from Recreation activities facet** - This is conceptually confused (horses are animals, not activities)
2. **All items keep:** Agents > Animals > Horses
3. **Add "Horseback riding" tag to items** where riding activity is explicitly described

---

## Item-by-Item Analysis

### Items referring to HORSES AS ANIMALS ONLY

**Item 2: "Megalong Matters" (26 Aug 1892)**
- Context: Wild horses shot for skins, breeding ponies for Sydney market
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 5: "Mountain Mixtures" (4 Dec 1891)**
- Context: "pair of horses attached to a buggy bolted"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 6: "Mountain Mixtures" (23 Jun 1893)**
- Context: "took a spring cart and horse to carry their packs"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 7: "Town Talk" (30 Oct 1903)**
- Context: "cattle and horse straying cases" (animal property dispute)
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses
- **Note:** Also contains "making rapid strides" (idiom, not about horses)

**Item 10: "Mountain Mixtures" (29 Apr 1892)**
- Context: "horses and cattle turned upon Katoomba streets", "stuck her horns into the sides of Bowker's horse"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 12: "Local and General" (7 Jul 1905)**
- Context: "horse attached to Mr Jones' sulky bolted" (runaway horse incident)
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 13: "Katoomba Police Court" (13 Dec 1895)**
- Context: "holding the Constable's horse and cap"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 15: "Mountain Mixtures" (3 Nov 1893)**
- Context: Cart overturned, "felling the horse"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

**Item 16: "Mountain Mixtures" (25 Nov 1892)**
- Context: "backed his employer's horse and cart over the embankment"
- **Current tags:** Horses
- **Recommendation:** Keep Agents > Animals > Horses

---

### Items referring to HORSEBACK RIDING ACTIVITY

**Item 1: "Mountain Mixtures" (21 Oct 1892)**
- Context: "knocked down by a horseman on the main street, Katoomba"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 4: "Town Talk" (13 Mar 1903)**
- Context: "traffic down Nellie's Glen has been done either on horseback"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 8: "Local Jottings" (25 May 1889)**
- Context: "17st horsewoman rode up Long Swamp", "16 miles on horseback"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 9: "Mountain Mixtures" (20 Nov 1891)**
- Context: "horse race took place at Medlow", "experienced rider on the chestnut"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**
  - **Note:** This is actually horse racing (sport), but we don't have a specific "Horse racing" tag

**Item 11: [untitled] (29 Jun 1889)**
- Context: "ride on the neck of a horse", "goes out in a new riding habit"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 14: "Megalong Valley" (15 Sep 1893)**
- Context: "riding a pony and leading another", "pulled the rider out of the saddle"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 17: "Accident in Nellie's Glen" (27 Jul 1889)**
- Context: "riding home", "riding his grey mare", "spilling over her rider"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 18: "Megalong Matters" (10 Jan 1896)**
- Context: "Horsemen returning to the valley via Nellie's Glen"
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

**Item 19: "Megalong Valley" (23 Jun 1893)**
- Context: "to give the horse a rest for awhile", "shank's pony" (idiom for walking)
- **Current tags:** Horses
- **Recommendation:**
  - Keep: Agents > Animals > Horses
  - **Add: Recreation activities > Horseback riding**

---

### Items with FALSE POSITIVES

**Item 3: "Town Talk" (13 May 1904)**
- Context: "22-horse power" (motor car specification, NOT actual horses)
- **Current tags:** Horses
- **Recommendation:** **REMOVE "Horses" tag entirely** - this is about motor cars, not horses
- **Also mentions:** "his grey neddy" (postman's horse as transport animal)
- **Revised recommendation:** Keep Agents > Animals > Horses (for the neddy reference)

---

## Taxonomy Updates Needed

### 1. Remove "Horses" from Recreation activities facet

**Current (incorrect):**
```
Recreation activities
├── Horseback riding
├── Horses  ← REMOVE THIS
```

**Corrected:**
```
Recreation activities
├── Horseback riding
```

### 2. Confirm "Horses" remains in Agents facet

**Confirmed (correct):**
```
Agents
└── Animals
    └── Horses
```

### 3. Update tag_map_consolidated.csv

**Entry to modify:**
```csv
Horses,Horses,hierarchy,parent=Recreation activities
```

**Change to:**
```csv
Horses,Horses,merge,Move all instances to Agents > Animals > Horses (horses are animals not activities)
```

**Entry to keep:**
```csv
Horses,Horses,hierarchy,parent=Animals
```

---

## Tag Application Queue

Add to `tag_application_mapping.csv`:

| Title | Date | Remove | Add | Notes |
|-------|------|--------|-----|-------|
| Mountain Mixtures | 21 Oct 1892 | | Horseback riding | Item #1 - horseman mentioned |
| Town Talk | 13 Mar 1903 | | Horseback riding | Item #4 - travel on horseback |
| Local Jottings | 25 May 1889 | | Horseback riding | Item #8 - horsewoman, on horseback |
| Mountain Mixtures | 20 Nov 1891 | | Horseback riding | Item #9 - horse race, rider |
| [untitled] | 29 Jun 1889 | | Horseback riding | Item #11 - riding, riding habit |
| Megalong Valley | 15 Sep 1893 | | Horseback riding | Item #14 - riding a pony, rider |
| Accident in Nellie's Glen | 27 Jul 1889 | | Horseback riding | Item #17 - riding home, rider |
| Megalong Matters | 10 Jan 1896 | | Horseback riding | Item #18 - horsemen returning |
| Megalong Valley | 23 Jun 1893 | | Horseback riding | Item #19 - give horse a rest (implies riding) |

---

## Conclusion

The current placement of "Horses" under Recreation activities is conceptually incorrect:
- **Horses are animals (agents), not activities**
- The **activity** is "Horseback riding"

All 19 items correctly refer to horses as animals and should remain tagged with Agents > Animals > Horses.

Additionally, 9 items (47%) specifically describe the activity of horseback riding and should receive the additional tag "Recreation activities > Horseback riding".

This polyhierarchical approach correctly separates:
- **What:** Horses (the animal agents)
- **Action:** Horseback riding (the recreation activity)
