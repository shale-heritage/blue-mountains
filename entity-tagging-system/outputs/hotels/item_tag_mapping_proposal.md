# Hotel Item-by-Item Tag Mapping Proposal

**Date:** 2025-11-13
**Phase:** Phase 2 - Item-level mapping proposal
**Status:** PENDING USER REVIEW

---

## Instructions

For each item below, review:

1. The proposed tag(s) to be applied
2. The NLU classification and confidence level
3. The context excerpt and reasoning
4. Modify proposed tags if needed
5. Mark `APPROVED: [ ]` as `[x]` when verified

**IMPORTANT:** Do not proceed to Phase 5 (application) until ALL items are reviewed and approved.

---

## Summary Statistics

**Total Items:** 43
**Total Unique Entities:** 14

**Proposed Tag Distribution:**
- Building tag only: 17 items (REVISED from 18)
- Business tag only: 14 items (REVISED from 17)
- Both tags (polyhierarchical): 12 items (REVISED from 8)

**User Modifications:** 5 items modified during Phase 4 review (see MODIFIED tags)

---

## Entity Summary Table

| Entity | Items | Building Only | Business Only | Both | Proposed Tags |
|--------|-------|---------------|---------------|------|---------------|
| Belgravia Hotel | 2 | 1 | 1 | 0 | Belgravia Hotel (building), Belgravia Hotel (business) |
| Carrington Hotel | 4 | 2 | 1 | 1 | Carrington Hotel (building), Carrington Hotel (business) |
| Centennial Hotel | 5 | 1 | 2 | 2 | Centennial Hotel (building), Centennial Hotel (business) |
| Family hotel | 3 | 0 | 2 | 1 | Katoomba Family Hotel (building), Katoomba Family Hotel (business) |
| Grand Hotel | 1 | 0 | 0 | 1 | Grand Hotel (Sydney) (building), Grand Hotel (Sydney) (business) **MODIFIED** |
| Imperial Hotel | 3 | 2 | 1 | 0 | Imperial Hotel (building), Imperial Hotel (business) |
| Katoomba Family Hotel | 1 | 0 | 1 | 0 | Katoomba Family Hotel (business) |
| Katoomba Hotel | 3 | 3 | 0 | 0 | Katoomba Hotel (building) |
| Megalong Hotel | 8 | 2 | 2 | 4 | Megalong Hotel (building), Megalong Hotel (business) **MODIFIED** |
| Montrose House | 4 | 4 | 0 | 0 | Montrose House (building) |
| Mount Victoria Hotel | 2 | 0 | 2 | 0 | Mount Victoria Hotel (business) |
| Railway Hotel | 2 | 2 | 0 | 0 | Railway Hotel (building) |
| Wentworth Falls Hotel | 2 | 0 | 2 | 0 | Wentworth Falls Hotel (business) |
| family hotel | 3 | 0 | 0 | 3 | Katoomba Family Hotel (building), Katoomba Family Hotel (business) **MODIFIED** |

---

## Detailed Item-by-Item Mappings

## Entity: Belgravia Hotel

**Total Items:** 2

### Item 30: Mountain Mixtures (1892-04-29)

**Date:** 29 April 1892
**Trove URL:** http://nla.gov.au/nla.news-article194118683

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Belgravia Hotel (business)`

**Context Excerpt:**
```text
Mr. L. T. Lloyd, official asignee.
The majority of the new books added to the Katoomba School of Arts library are a great acquisition to the institution.
Our Lithgow contemporary couldn't manage to report the matter of a goods engine tender running off the line under half a column.
Mr. Ellis was granted a renewal of the license for the Belgravia Ho...
```

**Reasoning:** Licensing renewal - "Mr. Ellis was granted a renewal of the license for the Belgravia Hotel." Legal/regulatory business proceeding. License renewal is business regulatory approval.

**APPROVED:** [ ]

---

### Item 31: Mountain Mixtures (1891-11-20)

**Date:** 20 November 1891
**Trove URL:** http://nla.gov.au/nla.news-article194115968

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Belgravia Hotel (building)`

**Context Excerpt:**
```text
half the distance, and then the great experienced rider on the chestnut forged ahead and kept that position to the finish. A great deal of interest was taken in the race, the betting on Friday night being even money, but on Saturday five to one was laid on the [?]. The course is a very good one, and the race could be viewed from the balcony of the ...
```

**Reasoning:** Strong spatial/visual reference - "the race could be viewed from the balcony of the Belgravia Hotel, which was packed with onlookers." Hotel serves as viewing platform (physical structure with balcony). Spatial relationship to race course. Physical architectural feature (balcony) emphasized.

**APPROVED:** [ ]

---

## Entity: Carrington Hotel

**Total Items:** 4

### Item 7: Local and General (1893-07-08)

**Date:** 8 July 1893
**Trove URL:** http://nla.gov.au/nla.news-article101080283

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Carrington Hotel (business)`

**Context Excerpt:**
```text
Nepean Times (Penrith, NSW : 1882 - 1962), Saturday 8 July 1893, page 4

Local and General.
…
KATOOMBA LICENSING COURT. - The Quarterly Licensing Court was held on Wednesday morning, Mr. J K. Cleeve, P.M., and Mr. A. Stephen, J.P., being on the Bench. A renewal of license was granted to F. C. Goyder for the Carrington Hotel. A conditional license f...
```

**Reasoning:** Licensing context - "renewal of license was granted to F. C. Goyder for the Carrington Hotel." This is a legal/regulatory proceeding concerning the business entity's right to trade. Licensee is named (F. C. Goyder), establishing business ownership. No spatial or locational usage.

**APPROVED:** [ ]

---

### Item 8: Local Jottings (1889-09-21)

**Date:** 21 September 1889
**Trove URL:** http://nla.gov.au/nla.news-article194115775

**NLU Classification:** building
**Confidence:** medium

**Proposed Tags:**
- `Carrington Hotel (building)`

**Context Excerpt:**
```text
rson.
Lithgow has sent nearly £40 to the London dock laborers.
Charles Wm. Cox, engineer, of Lithgow; Thomas Fernie, of Vale of Clwydd; and Thomas Mayne, of Clarence Siding, will explain to their creditors in Lithgow Court House on 7th proximo.
Tenders are advertised for a daily mail between Bell and Mount Wilson.
Have you seen that picture of the ...
```

**Reasoning:** Visual representation context - "picture of the Carrington Hotel in the Sydney illustrated" refers to depiction of the physical structure. Weak indicator overall (no clear spatial usage or events), but the context of illustrations typically depicting buildings (not businesses as abstract entities) suggests building classification.

**APPROVED:** [ ]

---

### Item 9: Katoomba Police Court (1894-09-21)

**Date:** 21 September 1894
**Trove URL:** http://nla.gov.au/nla.news-article194836227

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Carrington Hotel (building)`
- `Carrington Hotel (business)`

**Context Excerpt:**
```text
C. Goyder, licensee of the Car-rington Hotel, upon an information, that the said defendant did unlawfully assault the complainant on his licensed premises, on the 8th inst. The following evidence was taken: -
Ralph Taylor, complainant, deposed that he was a miner living at Megalong. On the 8th inst. about 7 p.m. he was at the Carrington hotel, and ...
```

**Reasoning:** Mixed indicators. Business: "F. C. Goyder, licensee of the Carrington Hotel" - proprietor/business operator. "Licensed premises" - regulatory business designation. Building: "was at the Carrington hotel" (locational preposition), "came into the room," "in his house" - clear spatial usage indicating building as location where assault occurred.

**APPROVED:** [ ]

---

### Item 10: A Charge of Rape (1890-09-06)

**Date:** 6 September 1890
**Trove URL:** http://nla.gov.au/nla.news-article101009812

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Carrington Hotel (building)`

**Context Excerpt:**
```text
rom Fanny Lynch yesterday morning between 3 and 4 o'clock, I took her to Dr. Spark at Katoomba, this was between 9 and 10 o'clock, she refused to be examined; I went in search of Fanny Lynch's husband but I failed to find him; Constable Illingworth then arrived at Katoomba, we went and searched for Lynch but could not find him; we then went to the ...
```

**Reasoning:** Strong locational indicator - "we then went to the Carrington Hotel" shows movement to location. Criminal investigation context uses hotel as spatial reference point where accused was located and arrested. No business operations or agency mentioned.

**APPROVED:** [ ]

---

## Entity: Centennial Hotel

**Total Items:** 5

### Item 25: Katoomba (1903-04-21)

**Date:** 21 April 1903
**Trove URL:** http://nla.gov.au/nla.news-article221489774

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Centennial Hotel (business)`

**Context Excerpt:**
```text
last year; Leura, 471; Wentworth Falls, 750; Lawson, 323.
The two men, Morsby and Thornicroft, who suffered most through being lost in the mine a few days ago, are slowly recovering from the effects of exposure. Work has not yet been resumed at the Ruined Castle beyond trucking the shale away.
Tabrett and Co. report the sale of the freehold of the ...
```

**Reasoning:** Property transaction - "Tabrett and Co. report the sale of the freehold of the Centennial hotel." Business asset sale. "Intention of the purchaser to thoroughly renovate the property" - business investment and operations planning. Financial transaction dominates context.

**APPROVED:** [ ]

---

### Item 26: Katoomba Court (1893-03-17)

**Date:** 17 March 1893
**Trove URL:** http://nla.gov.au/nla.news-article194114685

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Centennial Hotel (building)`
- `Centennial Hotel (business)`

**Context Excerpt:**
```text
th instant in the company of Brown, Saunders, and Daniel Gallagher; told him Saunders said he had given him (Saunders) a bottle of grog; he said, "That is false;" then locked him up. He then corroborated previous witness' evidence as to what took place at the backup.
By Prentice: You did not tell me you went to Hoffman's.
Richard Allen, proprietor ...
```

**Reasoning:** Mixed indicators. Business: "Richard Allen, proprietor Centennial Hotel" - business owner identification. "In my house" (from proprietor) - business premises ownership. Building: "The three men in the dock were in my house" - spatial location where theft occurred, "left the bar," "get behind the bar" - physical spatial references to rooms/areas within structure.

**APPROVED:** [ ]

---

### Item 27: Katoomba Municipal Elections (1890-07-05)

**Date:** 5 July 1890
**Trove URL:** http://nla.gov.au/nla.news-article194116221

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Centennial Hotel (building)`
- `Centennial Hotel (business)`

**Context Excerpt:**
```text
Cabs placarded with well-printed notices of "Vote for North and Nimmo" plied around the town, the the north side, and to the Mines, from the opening till the close of the poll, and opponents were generously given a drive through the ever falling rain. At the Mines the electors were seated now and then in a snug room by Host Edwards of the Centennia...
```

**Reasoning:** Mixed indicators. Business: "Host Edwards of the Centennial Hotel" - proprietor identification (host = hotelier). Building: "At the Mines the electors were seated now and then in a snug room" - spatial accommodation, physical room provision. Social/hospitality function provided by business at physical location.

**APPROVED:** [ ]

---

### Item 28: Testimonial to a Mine Manager (1890-08-09)

**Date:** 9 August 1890
**Trove URL:** http://nla.gov.au/nla.news-article194111613

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Centennial Hotel (building)`

**Context Excerpt:**
```text
Katoomba Times (NSW : 1889 - 1894), Saturday 9 August 1890, page 2

TESTIMONIAL TO A MINE MANAGER.
FRIDAY evening, at Alderman Edwards' Centennial Hotel, the Mayor (Mr. A. A. Smith) being in the chair, the following address was presented to Mr. Joseph Edwards: —
"Coal and Shale Mines Katoomba."To Mr. Joseph Edwards, Manager. "Dear Sir. — The miners...
```

**Reasoning:** Event location - "at Alderman Edwards' Centennial Hotel" establishes hotel as venue where testimonial presentation occurred. Locational preposition "at" indicates spatial usage. Proprietor mentioned but in context of location identification, not business operations.

**APPROVED:** [ ]

---

### Item 29: Katoomba Court (1893-06-16)

**Date:** 16 June 1893
**Trove URL:** http://nla.gov.au/nla.news-article194113779

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Centennial Hotel (business)`

**Context Excerpt:**
```text
plaintiff.
Verdict for plaintiff and one witness 10s.
R. Seaman v. P. H. Roberts. Claim, £3 16s. 3d. Verdict for plaintiff.
POLICE
Before Messrs. A. W. Stephen, F. C. Goyder, and J. W. Fletcher, Js.P.
William and Arthur Wright were charged with taking sand form the Great Western-road.
Discharged on payment of costs.
Richard Allen, licensee of the C...
```

**Reasoning:** Legal proceedings against business operator - "Richard Allen, licensee of the Centennial Hotel, Katoomba South, was charged with infringing Section 63 of the Licensing Act." Business entity facing regulatory violation. Licensing Act infringement is business/regulatory matter.

**APPROVED:** [ ]

---

## Entity: Family hotel

**Total Items:** 3

### Item 1: Death of Mrs. Nimmo (1926-12-03)

**Date:** 3 December 1926
**Trove URL:** http://nla.gov.au/nla.news-article108957001

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
Blue Mountain Echo (NSW : 1909 - 1928), Friday 3 December 1926, page 4

Death of Mrs. Nimmo
BURIED AT BOWENFELS.
Back in the early days of Katoomba, Mr. and Mrs. Joe Nimmo were prominent personalities in the community of Katoomba. For years they presided over the destinies of the Family Hotel, where they made money quickly and spent it with the fre...
```

**Reasoning:** Strong business agency indicators - "presided over the destinies of" indicates active management and proprietorship. "Made money quickly" references financial operations. No spatial/locational language - the hotel is referenced as a business enterprise run by the Nimmos.

**APPROVED:** [ ]

---

### Item 2: The Passing of a Mountaineer. Vale! Joseph Nimmo (1917-03-23)

**Date:** 23 March 1917
**Trove URL:** http://nla.gov.au/nla.news-article108247332

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
years; when, with two others, he started sawmills at Clarence. Disposing of his interest there, he left Lithgow for Hartley Vale, where he took over the Comet Hotel, the present brick building, which was sold the other day for a record decline price, being specially built for him. In '87, Mr. and Mrs. Nimmo came to Katoomba, where he purchased the ...
```

**Reasoning:** Clear business transaction language - "purchased the Family Hotel" indicates property/business acquisition. "Running them successfully for nearly ten years" demonstrates active business operations. No locational or spatial usage.

**APPROVED:** [ ]

---

### Item 3: Katoomba (1905-08-04)

**Date:** 4 August 1905
**Trove URL:** http://nla.gov.au/nla.news-article218749071

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (building)`
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
ggestion, and at a later date appoint delegates, as much good was likely to result from exchange of views. From the Katoomba Council, granting use of the chambers on payment of the usual fee of 2s 6d. After discussion it was decided to decline the offer at present, but it was stated that favourable arrangements had been made with Mrs. Long, of the ...
```

**Reasoning:** Dual-nature mention. Business aspect: "Mrs. Long, of the Family Hotel" - proprietor identification linking person to business entity. Building aspect: "use of one of her rooms" - spatial reference to physical accommodation within the structure. The arrangement is for room rental (business transaction) at a specific location (building).

**APPROVED:** [ ]

---

## Entity: Grand Hotel

**Total Items:** 1

### Item 38: Opening of the Gladstone Coal-Mine, Katoomba (1885-07-13)

**Date:** 13 July 1885
**Trove URL:** http://nla.gov.au/nla.news-article13592813

**NLU Classification:** both
**Confidence:** medium

**Proposed Tags:**
- `Grand Hotel (Sydney) (building)`
- `Grand Hotel (Sydney) (business)`

**Context Excerpt:**
```text
, an immediate adjournment was made for lunch, which had been prepared for several hundred people in a large marquee, adorned with mountain gigantic ferns, and pitched so as to afford a bird's-eye vista of the timber clearing along which the route to the mine runs. Mr. P. G. Whittall, of the Mount Victoria Hotel, and host elect of the shorty-to-be ...
```

**Reasoning:** Mixed indicators. Building: "shortly-to-be Grand Hotel in Phillip-street, Sydney" - future construction, geographic location. Business: "host elect" - future business proprietor/operator role. USER CORRECTION: Hotel is being built (building aspect) AND will open soon as business (business aspect). Note: Correct tag is "Grand Hotel (Sydney)" to distinguish from other Grand Hotels.

**APPROVED:** [X] MODIFIED

---

## Entity: Imperial Hotel

**Total Items:** 3

### Item 11: The Rockley Game (1898-03-18)

**Date:** 18 March 1898
**Trove URL:** http://nla.gov.au/nla.news-article194839495

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Imperial Hotel (building)`

**Context Excerpt:**
```text
Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 18 March 1898, page 2

The Rockley Game.
Last Saturday afternoon Beaumont's paddock opposite the Grand and Imperial Hotels presented a very pretty sight dotted all over with the bright and active figures of over a score of merry young people who, gaily attired, and distinguished by cream and red sas...
```

**Reasoning:** Clear spatial reference - "Beaumont's paddock opposite the Grand and Imperial Hotels." The hotels serve as geographical landmarks for locating the event venue. Strong locational preposition "opposite" establishes spatial relationship.

**APPROVED:** [ ]

---

### Item 12: Mountain Mixtures (1893-06-23)

**Date:** 23 June 1893
**Trove URL:** http://nla.gov.au/nla.news-article194113438

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Imperial Hotel (building)`

**Context Excerpt:**
```text
Katoomba Times (NSW : 1889 - 1894), Friday 23 June 1893, page 2

Mountain Mixtures. "A chiel's amang ye takin' notes, an faith we'll prent 'em
Very cold weather.
No court at Katoomba this week.
Tenders called for crematory work.
A.J.S. Bank reconstructed. Opened last Monday.
The Imperial Hotel at Mount Victoria to be re-built.
I.O.R. concert at Kat...
```

**Reasoning:** Passive construction - "The Imperial Hotel at Mount Victoria to be re-built." The hotel is recipient of construction action (passive voice), indicating building/structure undergoing physical modification. No active business agency.

**APPROVED:** [ ]

---

### Item 13: Local Jottings (1890-07-19)

**Date:** 19 July 1890
**Trove URL:** http://nla.gov.au/nla.news-article194114141

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Imperial Hotel (business)`

**Context Excerpt:**
```text
l has given notice of his intention to amend the Act Preventing Abuses and Profanations of the Lord's Day.
The Assembly agreed by 51 votes to 9 to the third reading of the Marrickville to Burwood road Railway Bill.
The Byron Bay Breakwater Bill passed its third reading in the Assembly on division by 49 votes to 25.
A transfer of the license of the ...
```

**Reasoning:** Licensing transfer context - "transfer of the license of the Imperial Hotel, Mount Victoria, has been granted from P. G. Whittal to Mrs. Margaret Coles." Clear business transaction involving legal business entity. License is business asset being transferred between proprietors.

**APPROVED:** [ ]

---

## Entity: Katoomba Family Hotel

**Total Items:** 1

### Item 39: Mountain Mixtures (1892-04-29)

**Date:** 29 April 1892
**Trove URL:** http://nla.gov.au/nla.news-article194118683

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
he appeal court is to be held at the local courthouse on the 11th May.
Gradually the Lithgow licensed dispensers of alcoholic stimulants are coming down to the "thripenny" beers. We predict, that there will be nearly double the amount of drunkenness at the black-diamond fields in consequence.
The lessee (whom believe is shortly to be the owner) of ...
```

**Reasoning:** Business operations and property transaction - "The lessee (whom believe is shortly to be the owner) of Katoomba Family Hotel intends to make great improvements to the building." Lessee/owner business relationship. "Intends to make improvements" - business investment decision and agency. Future business planning.

**APPROVED:** [ ]

---

## Entity: Katoomba Hotel

**Total Items:** 3

### Item 14: Mountain Mixtures (1892-12-02)

**Date:** 2 December 1892
**Trove URL:** http://nla.gov.au/nla.news-article194113022

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Katoomba Hotel (building)`

**Context Excerpt:**
```text
The trucks were laden with bullocks, and several beasts were killed. The breakage caused a delay to the traffic and the mail train did not arrive at Katoomba till a late hour.
The Katoomba Council would confer a great boon upon suffering humanity if they would make the footpath near that covetted corner, opposite the Katoomba Hotel, a little bit li...
```

**Reasoning:** Strong spatial reference - "footpath near that covetted corner, opposite the Katoomba Hotel." Hotel serves as geographical landmark. Locational preposition "opposite" establishes spatial relationship to infrastructure (footpath).

**APPROVED:** [ ]

---

### Item 15: The Inquest (1896-07-03)

**Date:** 3 July 1896
**Trove URL:** http://nla.gov.au/nla.news-article194839540

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Katoomba Hotel (building)`

**Context Excerpt:**
```text
Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 3 July 1896, page 2

THE INQUEST.
Mr Lethbridge held an inquest at the Katoomba Hotel on Thursday afternoon the jury consisting of the following: - Messrs John West (foreman), and Louis Menser, William Thomson, Thomas Christie, Samuel Herring, Herman Westphal, James Ford, Frederick McKay, John Edwar...
```

**Reasoning:** Clear locational usage - "inquest at the Katoomba Hotel." The hotel provides the physical venue for the judicial proceeding. Strong locational preposition "at" establishes hotel as location where event occurred.

**APPROVED:** [ ]

---

### Item 16: Local Jottings (1890-04-26)

**Date:** 26 April 1890
**Trove URL:** http://nla.gov.au/nla.news-article194118062

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Katoomba Hotel (building)`

**Context Excerpt:**
```text
The postmaster and boy at Lawson are painting the post office. Government supplying the paint and brushes. They have enough pound pots of paint to do all the houses in Lawson.
Mr. Dalwood and another gentleman were preaching in the streets of Katoomba last Saturday evening.
A painter poetically gave his views on "Hell fire" in front of a Katoomba H...
```

**Reasoning:** Spatial reference - "in front of a Katoomba Hotel." Locational preposition "in front of" establishes hotel as spatial landmark for street preaching event. Note indefinite article "a" suggests generic hotel building reference.

**APPROVED:** [ ]

---

## Entity: Megalong Hotel

**Total Items:** 8

### Item 17: The Megalong Hotel (1894-09-21)

**Date:** 21 September 1894
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194836241?searchTerm=megalong%20hotel%201894#

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (building)`
- `Megalong Hotel (business)`

**Context Excerpt:**
```text
Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 21 September 1894, page 1

The Megalong Hotel About 3 ?/3 miles from Katoomba. This Hotel is very favourably situated at the foot of the far-famed Nellie's Glen, and will be found highly convenient to visitors there, and also to those intending to explore the Kanimbla Valley or to journey to the Jen...
```

**Reasoning:** Advertisement context. Building: "very favourably situated," "at the foot of," geographic location - spatial/geographic descriptors. Business: "will be found highly convenient to visitors," "accommodation and attendance will be found..." - service provision and marketing language. Advertisements inherently promote business while describing physical location.

**APPROVED:** [ ]

---

### Item 18: Notice of Application for a Conditional Publican's Licence (1893-06-09)

**Date:** 9 June 1893
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194112699

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (business)`

**Context Excerpt:**
```text
ng Court, to be holden at Katoomba, on WEDNESDAY, the 5th day of July, 1893, apply for a Certificate authorising the issue of a Conditional Publican's License for a House, situate on land known as Mr. J. Waudby's selection, Megalong, in the Licensing District of Penrith, and marked in red in ink on plans lodged, and to be known by the sign of the "...
```

**Reasoning:** Licensing application - clear legal/regulatory business context. "Apply for a Certificate authorising the issue of a Conditional Publican's License" is regulatory approval for business operations. Plans lodged, applicant identified, business entity to be established. No spatial usage.

**APPROVED:** [ ]

---

### Item 19: Advertising (1895-02-08)

**Date:** 8 February 1895
**Trove URL:** http://nla.gov.au/nla.news-article194839926

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (building)`
- `Megalong Hotel (business)`

**Context Excerpt:**
```text
T. WATSON, Family Butcher, BENT-ST., KATOOMBA. WISHES to thank his customers for past support, and will do his best to please all Best Beef and Mutton on the Mountains. Families attended to punctually. Small Goods equal to the metropolis. Tripe, &c. Picnic Parties supplied with all necessaries. 
The Megalong Hotel About 3 1/2 Miles from Katoomba. T...
```

**Reasoning:** Advertisement (duplicate of Mention 17, slightly different text). Building: Geographic descriptors ("very favourably situated," spatial location). Business: Service provision ("accommodation and attendance"), marketing to visitors, advertisement genre.

**APPROVED:** [ ]

---

### Item 20: Katoomba Police Court (1895-12-13)

**Date:** 13 December 1895
**Trove URL:** http://nla.gov.au/nla.news-article194839890

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (building)`
- `Megalong Hotel (business)`

**Context Excerpt:**
```text
Was on duty at the time wearing uniform.
By the Bench: Did not speak to the accused.
By the Defendant: Did not notice Lennox holding my horse and cap. Accused did say after the handcuffs were on the prisoner "go with the constable now; he has got the best end of the stick."
Edward Delaney, licensee of the Megalong Hotel, on oath, deposed: Remember ...
```

**Reasoning:** Mixed indicators. Business: "Edward Delaney, licensee of the Megalong Hotel" - proprietor identification, business operator. Building: "at my hotel" - locational preposition indicating physical premises where arrest occurred, spatial context for legal proceedings.

**APPROVED:** [ ]

---

### Item 21: Notice of Application for a Publican's Licence (1896-06-19)

**Date:** 19 June 1896
**Trove URL:** http://nla.gov.au/nla.news-article194842204

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (business)`
- `Megalong Hotel (building)`

**Context Excerpt:**
```text
The accomodation in the premises for which the License is desired is in conformity with the provisions of section 30 of Act 45, Vic No. 14. The premises for which this license is applied for are the same for which a Publican's license was granted by the Penrith Licensing Court at Katoomba on the 11th April, 1894, then known by the sign of the Megal...
```

**Reasoning:** Mixed indicators. Business: "License is applied for," reference to previous license grant, reduction of license fee - legal/regulatory business context. Building: "plans of which have been lodged" - reference to architectural plans suggests physical building structure. USER CORRECTION: Plans mentioned indicate building aspect alongside licensing (business aspect).

**APPROVED:** [X] MODIFIED

---

### Item 22: Narrow Neck (1901-12-27)

**Date:** 27 December 1901
**Trove URL:** https://trove.nla.gov.au/newspaper/article/190710317?browse=ndp%3Abrowse%2Ftitle%2FM%2Ftitle%2F907%2F1901%2F12%2F27%2Fpage%2F21393095%2Farticle%2F190710317

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (building)`

**Context Excerpt:**
```text
its onward course the stream passes over a soft meadow covered with a series of beautiful cascades. 
Later on this stream flows over the edge of the "Neck" and forms a beautiful fall, bell shape, and about 30 feet in height. 
The stream can then be traced in a series of cascades right to its junction with the Nelly's Glen creek in the front of the ...
```

**Reasoning:** Strong spatial/visual description - "in the front of the Megalong hotel" locates stream junction relative to hotel as geographic landmark. "Lies nestled close in to the cliffs" - physical position and visual appearance. "Makes a very pretty picture" - aesthetic/visual observation of building in landscape.

**APPROVED:** [ ]

---

### Item 23: Megalong Matters (1896-06-05)

**Date:** 5 June 1896
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194841544

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (business)`

**Context Excerpt:**
```text
This is a request warranted neither by the amount of the stock traffic nor by the suitability of the place, as the approach via Nellie's Glen is not suitable for travelling stock. Such requests as these do more harm than good and are pronounced by the officials who read them as instances of "darned cheek." 
The Megalong Hotel, for some reason best ...
```

**Reasoning:** Business operations status - "The Megalong Hotel, for some reason best known to those concerned, remains closed." Active verb "remains" indicates business operational state (not open for trading). Business cessation/closure is business agency matter.

**APPROVED:** [ ]

---

### Item 24: The Rockley Game (1896-02-07)

**Date:** 7 February 1896
**Trove URL:** http://nla.gov.au/nla.news-article194838040

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Megalong Hotel (building)`

**Context Excerpt:**
```text
a, NSW : 1894 - 1908), Friday 7 February 1896, page 3

The Rockley Game. 
- o -
KATOOMBA V. MEGALONG.
The much talked of and long expected match at Rockley Game between the young ladies of the district of Megalong and a team from the Katoomba Club came off on Saturday last on the new cricket ground specially prepared for the occasion, close to the ...
```

**Reasoning:** Strong spatial references - "close to the Megalong hotel" locates cricket ground. "Reached the hotel on foot," "met... at the hotel" - movement to and gathering at physical location. Hotel serves as venue/meeting point for social event.

**APPROVED:** [ ]

---

## Entity: Montrose House

**Total Items:** 4

### Item 40: Mountain Mixtures (1893-05-05)

**Date:** 5 May 1893
**Trove URL:** http://nla.gov.au/nla.news-article194112641

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Montrose House (building)`

**Context Excerpt:**
```text
* * *At Katoomba Court. — Witness: "I resided for awhile in Haselbrook." The P.M. : "Where now?" Witness: "At present, your worship, I'm in Katoomba." * * * Mr. William Davis has commenced business at Katoomba as a wholesale and retail butcher. His advertisement appears in another column. Directory notice next week. * * * The owners of Montrose Hou...
```

**Reasoning:** Property rental negotiation - "The owners of Montrose House, Katoomba, require from the police department a rental of £156 per annum for that house for five years." While owners are mentioned (business aspect), dominant context is property as physical asset for rental. "The department will have to expend fully £50 on it" - physical modifications required. Building as real estate.

**APPROVED:** [ ]

---

### Item 41: Mountain Mixtures (1893-08-25)

**Date:** 25 August 1893
**Trove URL:** http://nla.gov.au/nla.news-article194114976

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Montrose House (building)`

**Context Excerpt:**
```text
Whisky at Megalong breeds imitation funerals, hangings, and what not. The last two words of the previous sentence mean the exaggeration gained in the travel of the news. Like a scavenger's cart - the more it travels the more it gathers. 
Department of Justice contemplate forsaking the I.O.O.F. Hall at Katoomba for Montrose House. This item of start...
```

**Reasoning:** Venue change for court - "Department of Justice contemplate forsaking the I.O.O.F. Hall at Katoomba for Montrose House." Montrose House serves as potential alternative venue for court sessions. Building usage as government facility location. Spatial/accommodation function.

**APPROVED:** [ ]

---

### Item 42: Moutains Mixtures (1893-11-17)

**Date:** 17 November 1893
**Trove URL:** http://nla.gov.au/nla.news-article194110192

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Montrose House (building)`

**Context Excerpt:**
```text
t far behind.
The Katoomba salvationists now hold forth in the Oddfellows' Hall every Sunday.
The Rev. R. W. Orton preaches at the Katoomba Wesleyan Church on Sunday next. See advt.
Messrs. Wyatt and Shuttleworth have dissolved partnership. Mr. Wyatt continues the business.
Shortly the Katoomba police office and court-house will be established at "...
```

**Reasoning:** Venue establishment - "Shortly the Katoomba police office and court-house will be established at 'Montrose House.'" Strong locational preposition "at" indicates building will house government facilities. Physical venue providing accommodation for official functions.

**APPROVED:** [ ]

---

### Item 43: Jottings (1891-05-23)

**Date:** 23 May 1891
**Trove URL:** http://nla.gov.au/nla.news-article194112487

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Montrose House (building)`

**Context Excerpt:**
```text
We believe that it has been secured by the present occupied for a term of five years.
Something new. - The Railway Quadrille Club hold dances at the Odd Fellows' Hall, Katoomba every Wednesday night.
A few weeks ago we mentioned that there was a good opening for a watchmaker in Katoomba. This week one has commenced business next to Montrose House.
...
```

**Reasoning:** Spatial landmark - "commenced business next to Montrose House." Montrose House serves as geographic reference point for locating new watchmaker business. Locational preposition "next to" establishes spatial relationship.

**APPROVED:** [ ]

---

## Entity: Mount Victoria Hotel

**Total Items:** 2

### Item 36: Notice of Application for a Conditional Publican's Licence (1893-06-09)

**Date:** 9 June 1893
**Trove URL:** https://trove.nla.gov.au/newspaper/article/194112699

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Mount Victoria Hotel (business)`

**Context Excerpt:**
```text
Licensing District of Penrith, and marked in red in ink on plans lodged, and to be known by the sign of the "Megalong Hotel," con-taining six rooms exclusive of those required for the use of the family, as per plan lodged with the Licensing Court at Katoomba. 
I am a married man having a wife and nine children. I am at present the lincesee of the M...
```

**Reasoning:** Licensing context - "I am at present the licensee of the Mount Victoria Hotel." License holder identification in regulatory application. "I intend to relinquish the License" - business regulatory asset transfer. No spatial usage.

**APPROVED:** [ ]

---

### Item 37: Opening of the Gladstone Coal-Mine, Katoomba (1885-07-13)

**Date:** 13 July 1885
**Trove URL:** http://nla.gov.au/nla.news-article13592813

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Mount Victoria Hotel (business)`

**Context Excerpt:**
```text
the Lithgow mines, 98 miles away.
On reaching the ground, an immediate adjournment was made for lunch, which had been prepared for several hundred people in a large marquee, adorned with mountain gigantic ferns, and pitched so as to afford a bird's-eye vista of the timber clearing along which the route to the mine runs. Mr. P. G. Whittall, of the M...
```

**Reasoning:** Business proprietor identification - "Mr. P. G. Whittall, of the Mount Victoria Hotel." Proprietor named in context of business capacity (catering provision for event). "Catered, and supplied full and plenty of the best" - business service provision. Hospitality business operations.

**APPROVED:** [ ]

---

## Entity: Railway Hotel

**Total Items:** 2

### Item 32: Mountain Mixtures (1893-06-02)

**Date:** 2 June 1893
**Trove URL:** http://nla.gov.au/nla.news-article194113004

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Railway Hotel (building)`

**Context Excerpt:**
```text
, of The Grand, long since secured the greater part of the trade at the Mount. Anyhow, this is no reason why the walls of the late building should be suffered to remain until an accident occurs. It is not safe to walk on the footpath near the walls, and it is about time the authorities saw that they were pulled down. 
A meeting was held at Nimmo's ...
```

**Reasoning:** Event location - "meeting was held at Nimmo's Railway Hotel." Strong locational preposition "at" indicates venue. Hotel provides physical space for football club formation meeting. Proprietor mentioned for location identification.

**APPROVED:** [ ]

---

### Item 33: Katoomba Police Court (1905-12-01)

**Date:** 1 December 1905
**Trove URL:** http://nla.gov.au/nla.news-article190711256

**NLU Classification:** building
**Confidence:** high

**Proposed Tags:**
- `Railway Hotel (building)`

**Context Excerpt:**
```text
Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 1 December 1905, page 3

Katoomba Police Court.
Friday (to-day), Dec. 1st, 1905.
Before the P.M. and Mr Hicks, J.P.
David Brown was charged with "being a person acting in a certain manner, to wit, as banker in conducting a common gaming house, to wit, the billiard-room of the Railway Hotel, at Katoo...
```

**Reasoning:** Location of illegal activity - "billiard-room of the Railway Hotel, at Katoomba" identifies specific room within building where alleged gaming occurred. Strong locational preposition "at" plus specific internal space reference. Building serves as location for criminal proceedings.

**APPROVED:** [ ]

---

## Entity: Wentworth Falls Hotel

**Total Items:** 2

### Item 34: Mountain Mixtures (1892-01-22)

**Date:** 22 January 1892
**Trove URL:** http://nla.gov.au/nla.news-article194117043

**NLU Classification:** business
**Confidence:** medium

**Proposed Tags:**
- `Wentworth Falls Hotel (business)`

**Context Excerpt:**
```text
or, who is well known to almost everyone in the district, announces in our advertising columns that he is a candidate for municipal honors.
'Tis now said that as yet only 100 men have been discharged by the Sunny Corner Mining Company.
Inspector Kevin examined Katoomba Public School this week.
New business notices for THE TIMES. — Mr. N. Delaney's ...
```

**Reasoning:** Business advertising notice - "Mr. N. Delaney's Wentworth Falls Hotel" in context of "New business notices for THE TIMES." Proprietor identification linked to advertising/marketing. Proprietor's name possessive suggests business ownership. Context is commercial promotion.

**APPROVED:** [ ]

---

### Item 35: Mountain Mixtures (1892-09-09)

**Date:** 9 September 1892
**Trove URL:** http://nla.gov.au/nla.news-article194117633

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Wentworth Falls Hotel (business)`

**Context Excerpt:**
```text
eorge Palmer, last postmaster at Katoomba, took unto himself a wife last week.
Mr. A. J. Robertson, solicitor, has left Katoomba. Stale news this. He went away two or three weeks ago.
Trade is so brisk at the new mining township, Nelly's Glen, that another butcher is talking of opening there.
Mr. Wilson has sold out the business in connection with ...
```

**Reasoning:** Business sale transaction - "Mr. Wilson has sold out the business in connection with Wentworth Falls Hotel." Clear business asset transfer. "Business in connection with" explicitly identifies business entity separate from (but related to) physical property.

**APPROVED:** [ ]

---

## Entity: family hotel

**Total Items:** 3

### Item 4: Death of Mrs. Nimmo (1926-12-03)

**Date:** 3 December 1926
**Trove URL:** http://nla.gov.au/nla.news-article108957001

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
Blue Mountain Echo (NSW : 1909 - 1928), Friday 3 December 1926, page 4

Death of Mrs. Nimmo
BURIED AT BOWENFELS.
Back in the early days of Katoomba, Mr. and Mrs. Joe Nimmo were prominent personalities in the community of Katoomba. For years they presided over the destinies of the Family Hotel, where they made money quickly and spent it with the fre...
```

**Reasoning:** Duplicate of Mention 1 (case variation only). Same context, same indicators. USER CORRECTION: Original text uses capitalized "Family Hotel" - refers to specific Katoomba Family Hotel, not generic family hotel.

**APPROVED:** [X] MODIFIED

---

### Item 5: The Passing of a Mountaineer. Vale! Joseph Nimmo (1917-03-23)

**Date:** 23 March 1917
**Trove URL:** http://nla.gov.au/nla.news-article108247332

**NLU Classification:** business
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
years; when, with two others, he started sawmills at Clarence. Disposing of his interest there, he left Lithgow for Hartley Vale, where he took over the Comet Hotel, the present brick building, which was sold the other day for a record decline price, being specially built for him. In '87, Mr. and Mrs. Nimmo came to Katoomba, where he purchased the ...
```

**Reasoning:** Duplicate of Mention 2 (case variation only). Same context, same indicators. USER CORRECTION: Original text uses capitalized "Family Hotel" - refers to specific Katoomba Family Hotel, not generic family hotel.

**APPROVED:** [X] MODIFIED

---

### Item 6: Katoomba (1905-08-04)

**Date:** 4 August 1905
**Trove URL:** http://nla.gov.au/nla.news-article218749071

**NLU Classification:** both
**Confidence:** high

**Proposed Tags:**
- `Katoomba Family Hotel (building)`
- `Katoomba Family Hotel (business)`

**Context Excerpt:**
```text
ggestion, and at a later date appoint delegates, as much good was likely to result from exchange of views. From the Katoomba Council, granting use of the chambers on payment of the usual fee of 2s 6d. After discussion it was decided to decline the offer at present, but it was stated that favourable arrangements had been made with Mrs. Long, of the ...
```

**Reasoning:** Duplicate of Mention 3 (case variation only). Same context, same indicators. USER CORRECTION: Original text uses capitalized "Family Hotel" - refers to specific Katoomba Family Hotel, not generic family hotel.

**APPROVED:** [X] MODIFIED

---

## Next Steps After Approval

1. [ ] User reviews all 43 item mappings
2. [ ] User marks all items as APPROVED or modifies proposed tags
3. [ ] User confirms readiness to proceed to Phase 3 (Taxonomy Gaps)
4. [ ] User approves final mapping before Phase 7 application

---

**Generated:** 2025-11-13
**Ready for Phase 4 User Review**
