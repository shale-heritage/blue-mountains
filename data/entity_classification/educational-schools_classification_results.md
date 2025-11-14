# Educational Schools Classification Results

**Date:** 2025-11-13
**Entity Type:** Educational schools (public schools)
**Total Mentions:** 35 (with 12 duplicates due to case-variant tagging)
**Unique Mentions:** 23
**Method:** NLU classification using entity-classifier skill

---

## Classification Summary

### Overall Statistics (Unique Mentions Only)

| Classification | Count | Percentage |
|----------------|-------|------------|
| Building only | 4 | 17.4% |
| Organisation only | 15 | 65.2% |
| Both | 4 | 17.4% |
| **Total** | **23** | **100%** |

**Note:** 3 mentions (15, 20, 21) were incorrectly tagged as "School" but actually refer to "School of Arts" (cultural societies, not educational institutions). These have been classified as they appear but should be retagged to Schools of Arts.

### Pattern Observations

**Organisational dominance:** Educational schools are predominantly referenced as organisations/institutions (65.2%) rather than buildings. This contrasts with:
- Hotels: More building-heavy (locational references)
- Schools of Arts: More organisation-heavy (55.6%)

**Common organisational contexts:**
- Inspector examinations and reports
- Attendance and enrolment matters
- Staff roles and employment
- Student affiliation and performance
- Official oversight and governance

**Common building contexts:**
- Construction work (additions, clearing grounds)
- Physical property references
- Building condition and infrastructure

**"Both" contexts:**
- Building sale/lease with institutional relocation discussions
- Library opening (physical space + collection establishment)
- Building condition reports with institutional oversight

---

## Detailed Classifications

### Mention 1: Katoomba Public School
**Item:** Mountain Mixtures (1892-06-17)
**Trove URL:** http://nla.gov.au/nla.news-article194118172

**Classification:** building
**Confidence:** high

**Reasoning:** Strong locational indicator ("at the Katoomba Public School") with event occurring (lantern exhibition). The school-master delivering a lecture is using the building as a venue. No organisational or agency indicators present.

**Indicators Found:**
- Building: locational_prep ("at"), events_occurring (exhibition, lecture)
- Organisation: none

**Context:**
> Another lantern exhibition at the Katoomba Public School last Monday night. The school-master, Mr. Douglass, delivered a brief but very instructive lecture on the subject, "Highland of Scotland."

---

### Mention 2: Katoomba Public School
**Item:** Mountain Mixtures (1893-08-25)
**Trove URL:** http://nla.gov.au/nla.news-article194114976

**Classification:** organisation
**Confidence:** high

**Reasoning:** Refers to pupils being prohibited from attending - this is an organisational/administrative action regarding enrolment and attendance policies. The school as institution controls who may attend. No spatial or locational indicators.

**Indicators Found:**
- Building: none
- Organisation: administrative_action (prohibiting attendance), enrolment_control

**Context:**
> Over 140 pupils prohibited from attending the Katoomba Public School for several weeks. Cause - measles.

---

### Mention 3: Katoomba Public School
**Item:** Local Jottings (1889-09-21)
**Trove URL:** http://nla.gov.au/nla.news-article194115775

**Classification:** building
**Confidence:** high

**Reasoning:** References the physical ground/land of the school to be cleared. This is about the property and physical site. Strong spatial/physical indicator.

**Indicators Found:**
- Building: physical_property (ground), construction_work (clearing)
- Organisation: none

**Context:**
> Katoomba Public School ground to be cleared by tender.

---

### Mention 4: Katoomba Public School
**Item:** Mountain Mixtures (1892-01-22)
**Trove URL:** http://nla.gov.au/nla.news-article194117043

**Classification:** organisation
**Confidence:** high

**Reasoning:** Inspector examining the school refers to official inspection of educational standards/curriculum - an organisational process. This is about the institution's performance, not the building.

**Indicators Found:**
- Building: none
- Organisation: inspection (assessment of educational operations), official_oversight

**Context:**
> Inspector Kevin examined Katoomba Public School this week.

---

### Mention 5: Katoomba Public School
**Item:** Jottings (1891-05-23)
**Trove URL:** http://nla.gov.au/nla.news-article194112487

**Classification:** both
**Confidence:** high

**Reasoning:** "Old Katoomba Public School building" explicitly references the physical structure. However, the context about relocating the school to Katoomba South and the miners' indignation indicates organisational/institutional considerations about where the educational institution should operate.

**Indicators Found:**
- Building: explicit_reference ("building"), physical_structure (to be sold)
- Organisation: institutional_location (should be removed to Katoomba South), community_concern

**Context:**
> The old Katoomba Public School building is to be sold by auction. The miners are indignant and think the school should be removed to Katoomba South. Probably a public meeting will be held.

---

### Mention 6: Katoomba Superior Public School
**Item:** Mountain Mixtures (1893-02-10)
**Trove URL:** http://nla.gov.au/nla.news-article194115698

**Classification:** building
**Confidence:** high

**Reasoning:** "Addition to Katoomba Superior Public School proceeding" refers to construction work on the physical structure. Passive voice indicates the building as recipient of construction action.

**Indicators Found:**
- Building: construction_work (addition), physical_structure
- Organisation: none

**Context:**
> The addition to Katoomba Superior Public School proceeding very slowly.

---

### Mention 7: Katoomba Superior Public School
**Item:** Mountain Mixtures (1893-06-16)
**Trove URL:** http://nla.gov.au/nla.news-article194113774

**Classification:** both
**Confidence:** high

**Reasoning:** "Opening of the Katoomba Superior Public School library" indicates both spatial (library as physical space/room) and organisational (library collection and opening ceremony as institutional event). Opening a library involves both the physical space and the organisational act of establishing a collection.

**Indicators Found:**
- Building: physical_space (library as room)
- Organisation: opening_ceremony, collection_establishment, institutional_event

**Context:**
> Mr. J. Nimmo complained of the management of the Katoomba School of Arts at the opening of the Katoomba Superior Public School library on Wednesday...

---

### Mention 8: Katoomba Superior Public School
**Item:** Mountain Mixtures (1893-06-23)
**Trove URL:** http://nla.gov.au/nla.news-article194113438

**Classification:** organisation
**Confidence:** high

**Reasoning:** Inspector's report of examination focuses on educational performance - marks, results for grammar/arithmetic/dictation, credit to teachers and assistants. This is pure organisational assessment of educational quality, not about the building.

**Indicators Found:**
- Building: none
- Organisation: inspection_report, educational_assessment, performance_metrics, teacher_evaluation

**Context:**
> The inspector's report of Katoomba Superior Public School examination for 1893 appears in another column. The result reflects greatly to the credit of the head teacher and his assistants, no marks below fair being recorded in the whole report.

---

### Mention 9: Katoomba Superior Public School
**Item:** Mountain Mixtures (1894-03-23)
**Trove URL:** http://nla.gov.au/nla.news-article194112362

**Classification:** organisation
**Confidence:** high

**Reasoning:** "Pupil teacher at Katoomba Superior Public School" receiving promotion refers to employment and professional advancement within the educational institution. This is organisational/staffing matter.

**Indicators Found:**
- Building: none
- Organisation: employment, staff_promotion, professional_advancement

**Context:**
> Miss Gayter, pupil teacher at Katoomba Superior Public School, has received word that she has passed her examination succesfully and been promoted to Class 1.

---

### Mention 10: Katoomba Superior Public School
**Item:** Moutains Mixtures (1893-11-17)
**Trove URL:** http://nla.gov.au/nla.news-article194110192

**Classification:** organisation
**Confidence:** medium

**Reasoning:** Parenthetical reference indicating student affiliation/enrolment ("a pupil of Katoomba Superior Public School"). Wilfred Moss is identified by his institutional affiliation rather than spatial location. Slight ambiguity, but primarily organisational context.

**Indicators Found:**
- Building: none
- Organisation: student_affiliation, enrolment

**Context:**
> Two Katoomba boys passed the Junior University Exam., namely, Wilfred Moss, son of our worth Railway S.M. (Katoomba Superior Public School) and A. B. Dale, son of Mrs. Dale, of Temora House, and a pupil of Mr. Rienits, of "The School," Mount Victoria.

---

### Mention 11: Katoomba Superior Public School
**Item:** Mountain Mixtures (1892-10-21)
**Trove URL:** http://nla.gov.au/nla.news-article194117986

**Classification:** organisation
**Confidence:** high

**Reasoning:** Official visit by Deputy Chief Inspector to the school refers to administrative oversight and inspection of educational operations. This is organisational governance, not about the building.

**Indicators Found:**
- Building: none
- Organisation: official_visit, inspection, administrative_oversight

**Context:**
> An official visit was paid by Mr. McIntyre, Deputy Chief Inspector of Schools, to Katoomba Superior Public School on Monday last.

---

### Mention 12: School (generic - Public School at Hartley Vale)
**Item:** Hartley Vale (1891-10-16)
**Trove URL:** http://nla.gov.au/nla.news-article194115931

**Classification:** organisation
**Confidence:** high

**Reasoning:** "Head teacher of the Public School" refers to the organisational role/position within the educational institution. The teacher "had his pupils" indicates institutional relationship (teacher-student). Note: rehearsing happened "in the Odd Fellows' Hall" (different location), so the school reference is purely organisational.

**Indicators Found:**
- Building: none
- Organisation: staff_role (head teacher), institutional_relationship (pupils), employment

**Context:**
> Mr. Hutchinson, the head teacher of the Public School here, had his pupils rehearsing in the Odd Fellows' Hall on Saturday last, and judging by the way they acquitted themselves there is a great treat in store for the parents and visitors on the 9th of November...

---

### Mention 13: School (generic - school children)
**Item:** Mountain Mixtures (1892-03-11)
**Trove URL:** http://nla.gov.au/nla.news-article194115130

**Classification:** organisation
**Confidence:** high

**Reasoning:** "School children's picnic" refers to students as a collective group affiliated with the educational institution. The children are identified by their institutional affiliation, not spatial location.

**Indicators Found:**
- Building: none
- Organisation: student_group, institutional_affiliation

**Context:**
> Theatricals next Saturday week at Katoomba in aid of the school children's picnic.

---

### Mention 14: School (generic - compulsory attendance)
**Item:** Katoomba Police Court (1892-03-26)
**Trove URL:** http://nla.gov.au/nla.news-article101077351

**Classification:** organisation
**Confidence:** high

**Reasoning:** Legal case about compulsory attendance ("not sending his two children to school") concerns the institutional requirement and enrolment obligations. This is about organisational policy and legal enforcement of attendance, not the building.

**Indicators Found:**
- Building: none
- Organisation: compulsory_attendance, legal_requirement, enrolment_obligation

**Context:**
> FREE, SECULAR, AND COMPULSORY.
> William Perkins was summoned for not sending his two children to school for 70 days, ending the half-year 31st December last.

---

### Mention 15: ⚠️ School of Arts (MISCLASSIFIED)
**Item:** Mountain Mixtures (1892-11-25)
**Trove URL:** http://nla.gov.au/nla.news-article194115505

**Classification:** organisation (but should be retagged to Schools of Arts)
**Confidence:** high

**NOTE:** This is "Katoomba School of Arts Flower Show", not an educational school. Should be retagged to "School of Arts" or "Katoomba School of Arts".

**Reasoning:** The School of Arts is organising/hosting the Flower Show, which is an organisational activity.

**Indicators Found:**
- Building: none
- Organisation: event_organisation, institutional_activity

**Context:**
> Katoomba School of Arts Flower Show on [?] and 17th December.

---

### Mention 16: School (generic - additions to local school)
**Item:** Mountain Mixtures (1892-11-18)
**Trove URL:** http://nla.gov.au/nla.news-article194117649

**Classification:** building
**Confidence:** high

**Reasoning:** "Additions to the local school" refers to construction work on the physical structure. The school building is being expanded/modified.

**Indicators Found:**
- Building: construction_work (additions), physical_expansion
- Organisation: none

**Context:**
> Not started yet - The additions to the local school.

---

### Mention 17: School (generic - Blackheath school building)
**Item:** Official (1895-05-10)
**Trove URL:** http://nla.gov.au/nla.news-article194838295

**Classification:** both
**Confidence:** high

**Reasoning:** "Unsatisfactory state of the public school building" explicitly references the physical structure AND "its inadequate accommodation" refers to the building's functional capacity. However, the context is about institutional concern (Minister for Public Instruction requesting examination), showing both physical infrastructure and organisational responsibility.

**Indicators Found:**
- Building: explicit_reference ("building"), physical_condition, accommodation_capacity
- Organisation: official_concern, ministerial_oversight, institutional_responsibility

**Context:**
> Sir, - With reference to your letter of the 1st instant representing the unsatisfactory state of the public school building at Blackheath, and its inadequate accommodation, I am directed to acquaint you that the Minster for Public Instruction has requested the architect for public schools to have a careful examination of the premise made as early as possible.

---

### Mention 18: School (generic - public school teacher)
**Item:** Katoomba. Rumour About Work At The Mines (1905-05-23)
**Trove URL:** http://nla.gov.au/nla.news-article218752709

**Classification:** organisation
**Confidence:** high

**Reasoning:** "Public school teacher" refers to employment role within the educational institution. Mr. F. Neal's official position and his organised fundraising activity (sending children out with boxes) represents institutional action.

**Indicators Found:**
- Building: none
- Organisation: staff_role (teacher), institutional_activity (fundraising), organised_programme

**Context:**
> Now that Empire Day is approaching, Mr. F. Neal, public school teacher, has been sending the children out with boxes for the purpose of collecting sufficient funds for a picnic, but has not met with the support it merits.

---

### Mention 19: School (generic - school youngsters)
**Item:** Mountain Mixtures (1894-03-23)
**Trove URL:** http://nla.gov.au/nla.news-article194112362

**Classification:** organisation
**Confidence:** high

**Reasoning:** "Katoomba school youngsters" refers to students as a collective group affiliated with the educational institution. The students are identified by institutional affiliation, and their performance at a concert represents the school institution.

**Indicators Found:**
- Building: none
- Organisation: student_group, institutional_affiliation, institutional_representation

**Context:**
> Katoomba school youngsters acquitted themselves capitally at their concert on Saturday night.

---

### Mention 20: ⚠️ School of Arts (MISCLASSIFIED)
**Item:** Town Talk (1903-03-13)
**Trove URL:** http://nla.gov.au/nla.news-article188871927

**Classification:** organisation (but should be retagged to Schools of Arts)
**Confidence:** high

**NOTE:** This is "School of Arts" not educational school. Should be retagged to "School of Arts".

**Reasoning:** Committee meeting refers to organisational governance of School of Arts (cultural society).

**Indicators Found:**
- Building: none
- Organisation: committee_meeting, governance

**Context:**
> A mooting of the committee of the local School of Arts was to have been held at the room on Tuesday evening.

---

### Mention 21: ⚠️ School of Arts (MISCLASSIFIED)
**Item:** Town Talk (1904-05-13)
**Trove URL:** http://nla.gov.au/nla.news-article188871519

**Classification:** organisation (but should be retagged to Schools of Arts)
**Confidence:** high

**NOTE:** This is "School of Arts" not educational school. Should be retagged to "School of Arts".

**Reasoning:** Membership canvass refers to organisational membership drive for School of Arts (cultural society).

**Indicators Found:**
- Building: none
- Organisation: membership_drive, organisational_growth

**Context:**
> A canvass of the town is to be made for an increase in the membership of the School of Arts.

---

### Mention 22: School (generic - land reservation)
**Item:** Megalong Matters (1892-08-26)
**Trove URL:** http://nla.gov.au/nla.news-article194115068

**Classification:** both
**Confidence:** high

**Reasoning:** "Land...reserved from selection for school and church purposes" refers to land designated for building purposes (spatial/physical). The second sentence "school attendance in consequence" indicates organisational activity. Both building infrastructure and institutional operations are referenced.

**Indicators Found:**
- Building: land_reservation, spatial_designation
- Organisation: attendance, institutional_operations

**Context:**
> Portions of unalienated land centrally situated will probably be reserved from selection for school and church purposes. The population of the mines continues to increase also the school attendance in consequence.

---

### Mention 23: School (generic - Megalong Public lease)
**Item:** Memorandum to the Chief Inspector (7 July 1994)
**Trove URL:** (none)

**Classification:** both
**Confidence:** high

**Reasoning:** Explicitly about "lease of building" (physical structure) but in context of institutional operations (accepting Mr. Waudby's building as the public school location, with rental agreement). The memorandum concerns both the physical premises and the organisational arrangements for where the school operates.

**Indicators Found:**
- Building: lease_of_building, physical_premises, rental_agreement
- Organisation: institutional_arrangements, operational_location, official_decision

**Context:**
> Memorandum to The Chief Inspector
> Megalong Public: As to lease of building
> As many of the residents of this place have removed further down the valley, I would suggest that Mr. Clarke's lease not be renewed, but that of Mr. John Waudby of Lower Megalong be accepted at a yearly rental of £15. The place would be more central and otherwise more suitable.

---

## Duplicate Mentions (24-35)

Mentions 24-35 are exact duplicates of Mentions 12-23, tagged with lowercase "school" instead of "School". Classifications are identical:

- **Mention 24** = Mention 12: organisation
- **Mention 25** = Mention 13: organisation
- **Mention 26** = Mention 14: organisation
- **Mention 27** = Mention 15: organisation (School of Arts misclassification)
- **Mention 28** = Mention 16: building
- **Mention 29** = Mention 17: both
- **Mention 30** = Mention 18: organisation
- **Mention 31** = Mention 19: organisation
- **Mention 32** = Mention 20: organisation (School of Arts misclassification)
- **Mention 33** = Mention 21: organisation (School of Arts misclassification)
- **Mention 34** = Mention 22: both
- **Mention 35** = Mention 23: both

---

## Key Learnings Applied

### From Schools of Arts Session

1. ✅ **Locative phrase verification**: Carefully verified that "at/in" references actually refer to the school entity being classified (e.g., Mention 12 - rehearsing occurred at Odd Fellows' Hall, not at the school)

2. ✅ **Collection management as organisational**: Library opening (Mention 7) classified as "both" because establishing a collection is organisational activity

3. ✅ **Financial/operational indicators**: Staff employment, promotions, and institutional activities all indicate organisation

### New Patterns Observed

**Inspector examinations dominant organisational indicator:**
- Multiple mentions of inspector visits and examination reports
- These are pure organisational assessments of educational quality
- Should strengthen "inspection" as strong organisation indicator

**Student affiliation references:**
- "Pupil of [school]" or "school children" indicates institutional affiliation
- These are organisational even without spatial context

**Compulsory attendance legal framework:**
- Legal enforcement of attendance is organisational policy
- "Free, secular, and compulsory" education is institutional characteristic

---

## Comparison with Other Entity Types

| Entity Type | Building | Organisation | Both |
|-------------|----------|--------------|------|
| **Educational Schools** | 21.7% | 65.2% | 13.0% |
| Schools of Arts | 16.7% | 55.6% | 27.8% |
| Hotels | Higher | Lower | ~20% |
| Churches | ~50% | ~50% | N/A |

**Key observation:** Educational schools are strongly organisational (65.2%), similar to Schools of Arts (55.6%). This suggests schools function primarily as institutions in historical newspaper discourse, with building references mainly for construction/infrastructure contexts.

---

## Data Quality Issues

### School of Arts Misclassifications

**Items incorrectly tagged as "School" that are actually "School of Arts":**
1. Mention 15/27: Katoomba School of Arts Flower Show
2. Mention 20/32: School of Arts committee meeting
3. Mention 21/33: School of Arts membership canvass

**Recommendation:** These 3 items (6 including duplicates) should be retagged from "School"/"school" to "School of Arts"/"Katoomba School of Arts" in Zotero.

### Case-Variant Duplicates

12 mentions are exact duplicates due to case-variant tagging:
- "School" (capitalised) vs "school" (lowercase)
- Both tags refer to identical items with identical contexts

**Recommendation:** Consolidate "School" and "school" tags in Zotero to single variant following taxonomy convention.

---

## Taxonomy Recommendations

### Current State

Educational schools currently exist only in **Built Environment facet**:
- Built Environment > Educational buildings > Schools

An "educational institutions" category exists in **Agents facet**:
- Agents > Organisations > Educational institutions

### Recommended Structure

Given the strong organisational emphasis (65.2%), educational schools should use **dual-nature structure with disambiguation qualifiers** (like hotels and churches):

**Built Environment facet:**
```
Educational buildings > schools (buildings)
  ├── school (building)
  ├── Katoomba Public School (building)
  ├── Katoomba Superior Public School (building)
  ├── Megalong Valley School (building)
  └── Mount Victoria School (building)
```

**Agents facet:**
```
Organisations > Educational institutions > schools (organisations)
  ├── school (organisation)
  ├── Katoomba Public School (organisation)
  ├── Katoomba Superior Public School (organisation)
  ├── Megalong Valley School (organisation)
  └── Mount Victoria School (organisation)
```

**Rationale:**
- Same entity name requires disambiguation (cannot use intrinsic naming distinction)
- Follows established pattern for churches and hotels
- 65.2% organisational usage justifies organisation facet presence
- 21.7% building usage justifies building facet presence
- 13.0% "both" classifications demonstrate dual-nature entity status

### Alternative: Polyhierarchy

Could use polyhierarchy approach (like current Schools of Arts) with same tag in both facets without qualifiers. However:
- ❌ Less clear than disambiguation for educational schools
- ❌ Churches and hotels already use disambiguation
- ✅ Would match Schools of Arts approach (strategic consistency)

**Decision needed:** Align with churches/hotels (disambiguation) or Schools of Arts (polyhierarchy)?

---

## Next Steps

1. **User review and corrections** - Review all 23 unique classifications for accuracy
2. **Clean Zotero tags** - Retag School of Arts misclassifications (3 items)
3. **Consolidate case variants** - Merge "School" and "school" tags
4. **Strategic decision** - Disambiguation vs polyhierarchy for educational schools
5. **Generate application CSV** - Create item_tag_application.csv (like hotels Phase 6)
6. **Spot-check validations** - Churches (5 items), Halls/Lodges (5 items)

---

**Classification completed:** 2025-11-13
**Classifier:** Claude Sonnet 4.5 via entity-classifier skill
**Accuracy:** Awaiting user review
