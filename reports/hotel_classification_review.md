# Hotel Classification Review: Building vs Business

Classification of hotel mentions using linguistic heuristic from `docs/entity-classification-heuristic.md`

## Instructions

For each hotel mention below:

1. Read the context and my recommendation
2. Modify the `APPROVED_CLASSIFICATION` if needed
3. Valid values: `building`, `business`, `both`
4. Add notes in `REVIEW_NOTES` if helpful

## Classification Key

- **building**: Tag as `[Hotel Name] (building)` in Built Environment only
- **business**: Tag as `[Hotel Name] (business)` in Agents > Organisations only
- **both**: Create polyhierarchical tags appearing in both facets

## Decision Heuristic Summary

**Building indicators:**
- Locational: at/in/near the hotel
- Movement: going to/from, arriving at
- Events: meeting held at, concert at
- Accommodation: staying at, lodging at

**Business indicators:**
- Agency: hotel expanding, refurbishing, opening
- Ownership: hotel proprietor, owner, manager
- Operations: licensed, trading, providing services
- Financial: selling, purchasing, revenue

---

## Megalong Hotel

**Total mentions analysed:** 8

### Entry 1

**Item:** The Megalong Hotel (1894-09-21) (21 September 1894)

**Context:**

> Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 21 September 1894, page 1

The Megalong Hotel About 3 ?/3 miles from Katoomba. This Hotel is very favourably situated at the foot of the far-famed Nellie's Glen, and will be found highly convenient to visitors there, and also to those intending to explore the Kanimbla Valley or to journey to th

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <https://trove.nla.gov.au/newspaper/article/194836241?searchTerm=megalong%20hotel%201894#>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 2

**Item:** Notice of Application for a Conditional Publican's Licence (1893-06-09) (9 June 1893)

**Context:**

> authorising the issue of a Conditional Publican's License for a House, situate on land known as Mr. J. Waudby's selection, Megalong, in the Licensing District of Penrith, and marked in red in ink on plans lodged, and to be known by the sign of the "Megalong Hotel," con-taining six rooms exclusive of those required for the use of the family, as per plan lodged with the Licensing Court at Katoomba. 
I am a married man having a wife and nine children. I am at present the lincesee of the Mount Victoria Hotel, si

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <https://trove.nla.gov.au/newspaper/article/194112699>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 3

**Item:** Advertising (1895-02-08) (8 February 1895)

**Context:**

> ES to thank his customers for past support, and will do his best to please all Best Beef and Mutton on the Mountains. Families attended to punctually. Small Goods equal to the metropolis. Tripe, &c. Picnic Parties supplied with all necessaries. 
The Megalong Hotel About 3 1/2 Miles from Katoomba. This Hotel is very favourably situated at the foot of the far-famed Nellie's Glen, and will be found highly convenient to visitors there, and also to those intending to explore the Kanimbla Valley or to journey to th

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194839926>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 4

**Item:** Katoomba Police Court (1895-12-13) (13 December 1895)

**Context:**

> d not speak to the accused.
By the Defendant: Did not notice Lennox holding my horse and cap. Accused did say after the handcuffs were on the prisoner "go with the constable now; he has got the best end of the stick."
Edward Delaney, licensee of the Megalong Hotel, on oath, deposed: Remember Constable White being at my hotel about the middle of the day on the 1st instant. Saw Constable White arrest Adams and saw Lennox there. The prisoner resisted, and I was called to assist.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194839890>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 5

**Item:** Notice of Application for a Publican's Licence (1896-06-19) (19 June 1896)

**Context:**

> 14. The premises for which this license is applied for are the same for which a Publican's license was granted by the Penrith Licensing Court at Katoomba on the 11th April, 1894, then known by the sign of the Megalong Hotel plans of which have been lodged. 
In conjuction with the above application I hereby give notice of my intention of applying to the above Licensing Court for a reduction of the license fee under section 11 of Act 46 Vic, no 24.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194842204>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 6

**Item:** Narrow Neck (1901-12-27) (27 December 1901)

**Context:**

> Later on this stream flows over the edge of the "Neck" and forms a beautiful fall, bell shape, and about 30 feet in height. 
The stream can then be traced in a series of cascades right to its junction with the Nelly's Glen creek in the front of the Megalong hotel, which makes a very pretty picture as it lies nestled close in to the cliffs and surrounded by a waving crop of wheat. 
Taking a more expansive view the stream may be seen wending its way like a silver thread far out into the valley, where it is los

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <https://trove.nla.gov.au/newspaper/article/190710317?browse=ndp%3Abrowse%2Ftitle%2FM%2Ftitle%2F907%2F1901%2F12%2F27%2Fpage%2F21393095%2Farticle%2F190710317>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 7

**Item:** Megalong Matters (1896-06-05) (5 June 1896)

**Context:**

> traffic nor by the suitability of the place, as the approach via Nellie's Glen is not suitable for travelling stock. Such requests as these do more harm than good and are pronounced by the officials who read them as instances of "darned cheek." 
The Megalong Hotel, for some reason best known to those concerned, remains closed. 
A cricket match between Ruined Castle miners and Megalong took place on Saturday creek resulting in a win for Ruined Castle. The return match at Burrugorang was played on Queen's birth

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <https://trove.nla.gov.au/newspaper/article/194841544>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 8

**Item:** The Rockley Game (1896-02-07) (7 February 1896)

**Context:**

> .
The much talked of and long expected match at Rockley Game between the young ladies of the district of Megalong and a team from the Katoomba Club came off on Saturday last on the new cricket ground specially prepared for the occasion, close to the Megalong hotel. The local team, fourteen in all, chaperoned by Mrs Peckman and accompanied by the founder and patron of the game (Mr J. Still O'Hara) were driven to the top of Nellie's Glen a little after 9 a.m. in two conveyances by Messrs Peckman Bros, and reach

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194838040>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Centennial Hotel

**Total mentions analysed:** 5

### Entry 9

**Item:** Katoomba (1903-04-21) (21 April 1903)

**Context:**

> uffered most through being lost in the mine a few days ago, are slowly recovering from the effects of exposure. Work has not yet been resumed at the Ruined Castle beyond trucking the shale away.
Tabrett and Co. report the sale of the freehold of the Centennial hotel, South Katoomba, at a satisfactory figure. I understand that it is the intention of the purchaser to thoroughly renovate the property and make it attractive to the many visitors to the Katoomba Falls.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article221489774>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 10

**Item:** Katoomba Court (1893-03-17) (17 March 1893)

**Context:**

> ven him (Saunders) a bottle of grog; he said, "That is false;" then locked him up. He then corroborated previous witness' evidence as to what took place at the backup.
By Prentice: You did not tell me you went to Hoffman's.
Richard Allen, proprietor Centennial Hotel, South Katoomba, deposed: The three men in the dock were in my house the night the grog were stolen; left the bar for a little while that night; I fancy I must have dozed off; the men mentioned left before I went into the little room; was in the roo

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194114685>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 11

**Item:** Katoomba Municipal Elections (1890-07-05) (5 July 1890)

**Context:**

> n, the the north side, and to the Mines, from the opening till the close of the poll, and opponents were generously given a drive through the ever falling rain. At the Mines the electors were seated now and then in a snug room by Host Edwards of the Centennial Hotel, a comfort that the scrutineers were not slow at times to avail themselves of. Inside the polling booths, the various officials worked most agreeably, and were anxious to assist each other. They had two luncheons, which, with the assistance of "the

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194116221>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 12

**Item:** Testimonial to a Mine Manager (1890-08-09) (9 August 1890)

**Context:**

> Katoomba Times (NSW : 1889 - 1894), Saturday 9 August 1890, page 2

TESTIMONIAL TO A MINE MANAGER.
FRIDAY evening, at Alderman Edwards' Centennial Hotel, the Mayor (Mr. A. A. Smith) being in the chair, the following address was presented to Mr. Joseph Edwards: —
"Coal and Shale Mines Katoomba."To Mr. Joseph Edwards, Manager. "Dear Sir. — The miners and other workmen employed at the above Colliery, h

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194111613>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 13

**Item:** Katoomba Court (1893-06-16) (16 June 1893)

**Context:**

> . Verdict for plaintiff.
POLICE
Before Messrs. A. W. Stephen, F. C. Goyder, and J. W. Fletcher, Js.P.
William and Arthur Wright were charged with taking sand form the Great Western-road.
Discharged on payment of costs.
Richard Allen, licensee of the Centennial Hotel, Katoomba South, was charged with infringing Section 63 of the Licensing Act.
Mr. Montagu appeared in support of complainant. Mr. Gannon for defendant.
Sergeant Thorndike, Licensing Inspector, proved formalities.
John Johnson miner, deposed: Live th

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194113779>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Carrington Hotel

**Total mentions analysed:** 4

### Entry 14

**Item:** Local and General (1893-07-08) (8 July 1893)

**Context:**

> 1893, page 4

Local and General.
…
KATOOMBA LICENSING COURT. - The Quarterly Licensing Court was held on Wednesday morning, Mr. J K. Cleeve, P.M., and Mr. A. Stephen, J.P., being on the Bench. A renewal of license was granted to F. C. Goyder for the Carrington Hotel. A conditional license for an hotel to be built at Leura was granted, and a license for an hotel at Megalong was refused, owing to the plans being imperfectly drawn.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article101080283>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 15

**Item:** Local Jottings (1889-09-21) (21 September 1889)

**Context:**

> ; Thomas Fernie, of Vale of Clwydd; and Thomas Mayne, of Clarence Siding, will explain to their creditors in Lithgow Court House on 7th proximo.
Tenders are advertised for a daily mail between Bell and Mount Wilson.
Have you seen that picture of the Carrington Hotel in the Sydney illustrated! A local artist is sharpening his tomahawk to cut a better view.
The bankrupt estate of Thomas Lovelle, store-keeper, of Katoomba, shows an equalising dividend of 3.s 4 7-10d.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194115775>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 16

**Item:** Katoomba Police Court (1894-09-21) (21 September 1894)

**Context:**

> id defendant did unlawfully assault the complainant on his licensed premises, on the 8th inst. The following evidence was taken: -
Ralph Taylor, complainant, deposed that he was a miner living at Megalong. On the 8th inst. about 7 p.m. he was at the Carrington hotel, and while playing a game of billiards the defendant came into the room and wanted to know what I was making such a noise for, saying he would not have such a noise in his house. Witness said he was not making a row, but defendant said he would put

**Recommended classification:** `building` (confidence: 2/3)

**Reasoning:** Spatial/locational indicators: locational_prep

**Matched patterns:** locational_prep

**Trove source:** <http://nla.gov.au/nla.news-article194836227>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 17

**Item:** A Charge of Rape (1890-09-06) (6 September 1890)

**Context:**

> was between 9 and 10 o'clock, she refused to be examined; I went in search of Fanny Lynch's husband but I failed to find him; Constable Illingworth then arrived at Katoomba, we went and searched for Lynch but could not find him; we then went to the Carrington Hotel; I called accused and said to him "We are going to arrest you;" I further said "I charge you with committing a rape on Mrs. William Lynch sometime this morning at her residence Katoomba; he replied "Who, me, alright it is one thing.

**Recommended classification:** `building` (confidence: 2/3)

**Reasoning:** Spatial/locational indicators: movement_to

**Matched patterns:** movement_to

**Trove source:** <http://nla.gov.au/nla.news-article101009812>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Montrose House

**Total mentions analysed:** 4

### Entry 18

**Item:** Mountain Mixtures (1893-05-05) (5 May 1893)

**Context:**

> re now?" Witness: "At present, your worship, I'm in Katoomba." * * * Mr. William Davis has commenced business at Katoomba as a wholesale and retail butcher. His advertisement appears in another column. Directory notice next week. * * * The owners of Montrose House, Katoomba, require from the police department a rental of £156 per annum for that house for five years, and the department will have to expend fully £50 on it before it can be made suitable. * * * If Katoomba Council declines to go on with the long

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194112641>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 19

**Item:** Mountain Mixtures (1893-08-25) (25 August 1893)

**Context:**

> The last two words of the previous sentence mean the exaggeration gained in the travel of the news. Like a scavenger's cart - the more it travels the more it gathers. 
Department of Justice contemplate forsaking the I.O.O.F. Hall at Katoomba for Montrose House. This item of startling news we published nearly six months ago, and the I.O.O.F. Hall is still the court, although all the time officers are getting and making reports on the matter. 
Newest designs in Invite, Wedding, Menu, and Mourning Cards at T

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194114976>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 20

**Item:** Moutains Mixtures (1893-11-17) (17 November 1893)

**Context:**

> R. W. Orton preaches at the Katoomba Wesleyan Church on Sunday next. See advt.
Messrs. Wyatt and Shuttleworth have dissolved partnership. Mr. Wyatt continues the business.
Shortly the Katoomba police office and court-house will be established at "Montrose House."
A Blackheath drunk, disorderly and obscene language man, paid over 17s. 6d. at Katoomba court on Wednesday.
The Katoomba mines are just working sufficiently to keep the rope rollers from rusting. Only about 50 men are at Megalong now.
Heavy hailst

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194110192>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 21

**Item:** Jottings (1891-05-23) (23 May 1891)

**Context:**

> - The Railway Quadrille Club hold dances at the Odd Fellows' Hall, Katoomba every Wednesday night.
A few weeks ago we mentioned that there was a good opening for a watchmaker in Katoomba. This week one has commenced business next to Montrose House.
A foreigner - well, he is not an Australian - undermined a Katoombaite last week and secured his situation at a trifle less salary. We detest wire-pullers, jeremydiddlers, and never-pay-ups, and will deal warmly with such trash.
Mr. S. E.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194112487>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Imperial Hotel

**Total mentions analysed:** 3

### Entry 22

**Item:** The Rockley Game (1898-03-18) (18 March 1898)

**Context:**

> Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 18 March 1898, page 2

The Rockley Game.
Last Saturday afternoon Beaumont's paddock opposite the Grand and Imperial Hotels presented a very pretty sight dotted all over with the bright and active figures of over a score of merry young people who, gaily attired, and distinguished by cream and red sashes, represented the Katoomba and Combined (Hartley, Hartley Vale and B

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194839495>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 23

**Item:** Mountain Mixtures (1893-06-23) (23 June 1893)

**Context:**

> 894), Friday 23 June 1893, page 2

Mountain Mixtures. "A chiel's amang ye takin' notes, an faith we'll prent 'em
Very cold weather.
No court at Katoomba this week.
Tenders called for crematory work.
A.J.S. Bank reconstructed. Opened last Monday.
The Imperial Hotel at Mount Victoria to be re-built.
I.O.R. concert at Katoomba on the 3rd next month. See advt.
Katoomba Council threaten law to all ratepayers not settling up before the 14th July, 1893.
Katoomba Quadrille Club meets every Tuesday evening at 8 in the

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194113438>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 24

**Item:** Local Jottings (1890-07-19) (19 July 1890)

**Context:**

> s Day.
The Assembly agreed by 51 votes to 9 to the third reading of the Marrickville to Burwood road Railway Bill.
The Byron Bay Breakwater Bill passed its third reading in the Assembly on division by 49 votes to 25.
A transfer of the license of the Imperial Hotel, Mount Victoria, has been granted from P. G. Whittal to Mrs. Margaret Coles, late of Melbourne.
The Legislative Council passed the Nyngan to Cobar Railway Bill through its final stages.
The Typographical Association of Sydney voted on Saturday 2 eac

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194114141>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Katoomba Hotel

**Total mentions analysed:** 3

### Entry 25

**Item:** Mountain Mixtures (1892-12-02) (2 December 1892)

**Context:**

> The breakage caused a delay to the traffic and the mail train did not arrive at Katoomba till a late hour.
The Katoomba Council would confer a great boon upon suffering humanity if they would make the footpath near that covetted corner, opposite the Katoomba Hotel, a little bit like a footpath. In wet weather at this spot one sinks to the ankles in slush and in dry weather one is almost blinded by the dust arising from the staff blocking the water-course.
Strikes us very forcibly that the tightness of money m

**Recommended classification:** `building` (confidence: 2/3)

**Reasoning:** Spatial/locational indicators: locational_prep

**Matched patterns:** locational_prep

**Trove source:** <http://nla.gov.au/nla.news-article194113022>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 26

**Item:** The Inquest (1896-07-03) (3 July 1896)

**Context:**

> Mountaineer (Katoomba, NSW : 1894 - 1908), Friday 3 July 1896, page 2

THE INQUEST.
Mr Lethbridge held an inquest at the Katoomba Hotel on Thursday afternoon the jury consisting of the following: - Messrs John West (foreman), and Louis Menser, William Thomson, Thomas Christie, Samuel Herring, Herman Westphal, James Ford, Frederick McKay, John Edwards and William Thomas.
Thomas Barri

**Recommended classification:** `building` (confidence: 2/3)

**Reasoning:** Spatial/locational indicators: locational_prep

**Matched patterns:** locational_prep

**Trove source:** <http://nla.gov.au/nla.news-article194839540>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 27

**Item:** Local Jottings (1890-04-26) (26 April 1890)

**Context:**

> They have enough pound pots of paint to do all the houses in Lawson.
Mr. Dalwood and another gentleman were preaching in the streets of Katoomba last Saturday evening.
A painter poetically gave his views on "Hell fire" in front of a Katoomba Hotel on Wednesday. Large concourse of hearers.
Mr. [?] plays the horn very proficiently, and is thinking of getting up a band.
When you advertise, remember it is more profitable to pay for a business notice in a well-circulated paper.
Mr.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194118062>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Belgravia Hotel

**Total mentions analysed:** 2

### Entry 28

**Item:** Mountain Mixtures (1892-04-29) (29 April 1892)

**Context:**

> chool of Arts library are a great acquisition to the institution.
Our Lithgow contemporary couldn't manage to report the matter of a goods engine tender running off the line under half a column.
Mr. Ellis was granted a renewal of the license for the Belgravia Hotel, Medlow, at the Licensing Court, held at Katoomba, last Wednesday.
Events to come. - Skating carnival at Katoomba on 18th May, and £10 Skating Handicap at the Mount commencing on 21st May. See ads.
Mr. A. L.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194118683>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 29

**Item:** Mountain Mixtures (1891-11-20) (20 November 1891)

**Context:**

> A great deal of interest was taken in the race, the betting on Friday night being even money, but on Saturday five to one was laid on the [?]. The course is a very good one, and the race could be viewed from the balcony of the Belgravia Hotel, which was packed with onlookers.
BY TELEGRAPH. - Mr. Albert Wilson, of [?] Water Supply, Blackheath, died early this morning from painful illness. He was the oldest resident and greatly respected, and his loss regretted.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194115968>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Railway Hotel

**Total mentions analysed:** 2

### Entry 30

**Item:** Mountain Mixtures (1893-06-02) (2 June 1893)

**Context:**

> ason why the walls of the late building should be suffered to remain until an accident occurs. It is not safe to walk on the footpath near the walls, and it is about time the authorities saw that they were pulled down. 
A meeting was held at Nimmo's Railway Hotel on Friday night last for the purpose of forming a football club, Mr. Wolfenden in the chair. Dr. Prangley was elected president; Messrs. Moss and Minno, vice-presidents; Mr. H. Brandon, captain; Mr. M. Dolan, vice-captain; Mr. J.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194113004>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 31

**Item:** Katoomba Police Court (1905-12-01) (1 December 1905)

**Context:**

> 1st, 1905.
Before the P.M. and Mr Hicks, J.P.
David Brown was charged with "being a person acting in a certain manner, to wit, as banker in conducting a common gaming house, to wit, the billiard-room of the Railway Hotel, at Katoomba, the said room, having been entered under the authority of a special warrant, as provided by section 4 of the Games, Wagers and Betting House Act of 1901." 
Accused pleaded not guilty, and asked for a remand. 
Mr R. M.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article190711256>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Wentworth Falls Hotel

**Total mentions analysed:** 2

### Entry 32

**Item:** Mountain Mixtures (1892-01-22) (22 January 1892)

**Context:**

> he is a candidate for municipal honors.
'Tis now said that as yet only 100 men have been discharged by the Sunny Corner Mining Company.
Inspector Kevin examined Katoomba Public School this week.
New business notices for THE TIMES. — Mr. N. Delaney's Wentworth Falls Hotel, and Mr. Thomas Cale's coach and buggy business. See the ads.
A Lithgow man last week sued his wife because she threatened to knock his brains out and because he was in terror of grievous bodily injury at her hands.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194117043>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 33

**Item:** Mountain Mixtures (1892-09-09) (9 September 1892)

**Context:**

> Stale news this. He went away two or three weeks ago.
Trade is so brisk at the new mining township, Nelly's Glen, that another butcher is talking of opening there.
Mr. Wilson has sold out the business in connection with Wentworth Falls Hotel. Wentworth Falls, to Mr. Manuel, late of Hatley Vale.
The report of the banquet tendered to Mr. Atkinson, postmaster, Lawson, reached us to late for insertion last issue. It appears on our fourth page.
The concert given by Katoomba Amateur Minstrels

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194117633>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Mount Victoria Hotel

**Total mentions analysed:** 2

### Entry 34

**Item:** Notice of Application for a Conditional Publican's Licence (1893-06-09) (9 June 1893)

**Context:**

> n of the "Megalong Hotel," con-taining six rooms exclusive of those required for the use of the family, as per plan lodged with the Licensing Court at Katoomba. 
I am a married man having a wife and nine children. I am at present the lincesee of the Mount Victoria Hotel, situate at Little Hartley, in the Licensing District of Lithgow, but I intend to religuish the License of the said Hotel before this application will be heard. 
Dated at Katoomba this seventh day of June, 1893.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <https://trove.nla.gov.au/newspaper/article/194112699>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

### Entry 35

**Item:** Opening of the Gladstone Coal-Mine, Katoomba (1885-07-13) (13 July 1885)

**Context:**

> ch, which had been prepared for several hundred people in a large marquee, adorned with mountain gigantic ferns, and pitched so as to afford a bird's-eye vista of the timber clearing along which the route to the mine runs. Mr. P. G. Whittall, of the Mount Victoria Hotel, and host elect of the shorty-to-be Grand Hotel in Phillip-street, Sydney, catered, and supplied full and plenty of the best. In deference to those destined after lunch to undertake a stiff mountaineering climb to the mine, toastmaking was made extr

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article13592813>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Katoomba Family Hotel

**Total mentions analysed:** 1

### Entry 36

**Item:** Mountain Mixtures (1892-04-29) (29 April 1892)

**Context:**

> d dispensers of alcoholic stimulants are coming down to the "thripenny" beers. We predict, that there will be nearly double the amount of drunkenness at the black-diamond fields in consequence.
The lessee (whom believe is shortly to be the owner) of Katoomba Family Hotel intends to make great improvements to the building. With the old bar and billiard saloon away, the building would have a much nicer appearance.
Will Katoomba Council be able to finance a lighting scheme during the depression now existing throughout

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article194118683>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

## Grand Hotel

**Total mentions analysed:** 1

### Entry 37

**Item:** Opening of the Gladstone Coal-Mine, Katoomba (1885-07-13) (13 July 1885)

**Context:**

> a large marquee, adorned with mountain gigantic ferns, and pitched so as to afford a bird's-eye vista of the timber clearing along which the route to the mine runs. Mr. P. G. Whittall, of the Mount Victoria Hotel, and host elect of the shorty-to-be Grand Hotel in Phillip-street, Sydney, catered, and supplied full and plenty of the best. In deference to those destined after lunch to undertake a stiff mountaineering climb to the mine, toastmaking was made extremely short and practical.

**Recommended classification:** `building` (confidence: 1/3)

**Reasoning:** No strong indicators detected; defaulting to building (typical usage)

**Trove source:** <http://nla.gov.au/nla.news-article13592813>

**APPROVED_CLASSIFICATION:** `building`

**REVIEW_NOTES:**

---

