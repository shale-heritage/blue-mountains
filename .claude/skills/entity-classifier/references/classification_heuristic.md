# Entity Classification Heuristic: Detailed Decision Framework

## Purpose

Comprehensive decision framework for classifying dual-nature entities (hotels, churches, schools of arts, halls, lodges, etc.) as:
- **(a) Building/Facility only** - Physical structure in Built Environment facet
- **(b) Business/Organisation only** - Agent in Agents > Organisations facet
- **(c) Both (Polyhierarchical)** - Appears in both facets

## Core Principle

Classification depends on **how the entity is represented in the source text**, not external knowledge. Tag what the text *is about*, not what is known about the entity.

## Detailed Indicator Patterns

### Building/Facility Indicators

#### 1. Locational Prepositions
Entity functions as a location or spatial reference point.

**Patterns:**
- at [entity], in [entity], within [entity], inside [entity]
- outside [entity], near [entity], opposite [entity], adjacent to [entity]
- on [entity], by [entity], around [entity]

**Examples:**
- "A meeting was held **at the Carrington Hotel**"
- "Concert **in the School of Arts**"
- "Fire brigade stationed **near the hotel**"

#### 2. Movement To/From
Entity serves as destination or origin of movement.

**Patterns:**
- going to, coming from, arriving at, leaving, departing
- walking to, travelling to, proceeded to, repaired to

**Examples:**
- "Guests **arriving at the Imperial Hotel**"
- "After the match, teams **went to the hotel**"
- "Travellers **leaving the Megalong Hotel**"

#### 3. Events Occurring
Entity hosts events organised by others (not the entity itself).

**Patterns:**
- meeting held at, concert at, ball at, dinner at
- auction at, court session at, gathering at, function at
- picnic at, race meeting at, entertainment at

**Examples:**
- "Ball **held at the hotel** last evening"
- "Church choir concert **in the hall**"
- "Licensing court **at the courthouse**"

**Note:** If entity organises/sponsors event (not just hosting), this is business agency.

#### 4. Accommodation/Occupancy
Entity provides space where people stay or reside.

**Patterns:**
- staying at, lodging at, residing at, accommodated at
- stopping at, quartered at, housed at

**Examples:**
- "Visitors **staying at the Falls Hotel**"
- "Family **lodging at the boarding house**"

#### 5. Physical Features
References to structural or spatial attributes.

**Patterns:**
- [entity]'s building, structure, premises, rooms, bar
- [entity]'s verandah, dining room, bedroom, parlour, stable
- [entity]'s yard, grounds, paddock, garden

**Examples:**
- "**The hotel's large dining room** was filled"
- "Fire destroyed **the church building**"
- "**School premises** underwent repairs"

#### 6. Construction/Physical Change
Passive recipient of construction or destruction.

**Patterns:**
- was built, being erected, demolished, burned down
- destroyed, damaged, renovated (passive voice)

**Examples:**
- "**The hotel was built** in 1885"
- "**Church destroyed** by fire"
- "**Hall damaged** in storm"

**Critical:** Passive voice indicates building. Active voice ("hotel renovated its premises") indicates business.

### Business/Organisation Indicators

#### 1. Agency Verbs
Entity actively performs actions or makes decisions.

**Patterns:**
- [entity] announced, expanded, refurbished, opened, closed
- [entity] advertised, commenced, decided, voted

**Examples:**
- "**Hotel announced** extensive renovations"
- "**School of Arts committee voted** to extend hours"
- "**Church appointed** new minister"

#### 2. Ownership/Management
Entity identified through its operators (who can act as agents).

**Patterns:**
- [entity] proprietor, owner, manager, keeper, lessee
- proprietor of [entity], owner of [entity]
- [entity] management, [entity] committee

**Examples:**
- "**Imperial Hotel proprietor** was fined"
- "**Licensee of the Megalong Hotel** testified"
- "**School of Arts committee** met yesterday"

**Note:** When proprietor/owner is named as individual person, this can still indicate business if they're acting in business capacity.

#### 3. Business Operations
Entity operates commercially or provides services.

**Patterns:**
- [entity] licensed, trading, operating, conducting business
- [entity] opened for season, closed for repairs
- [entity] commenced operations

**Examples:**
- "**Hotel licensed** to sell alcohol"
- "**Business trading** as Carrington Hotel"
- "**School of Arts opened** for evening classes"

#### 4. Services Provided
Entity actively offers, provides, or markets services.

**Patterns:**
- [entity] offers, provides, caters, serves, supplies
- [entity] can accommodate, will host, features

**Examples:**
- "**Hotel offers** special rates for groups"
- "**School of Arts provides** library services"
- "**Church operates** Sunday school"

#### 5. Financial Actions
Entity engages in financial transactions or business decisions.

**Patterns:**
- [entity] purchased, selling, bought, sold
- [entity] revenue, profit, rent, fees
- [entity] paying, charging, billing

**Examples:**
- "**Hotel purchased** adjacent land"
- "**School of Arts** increased membership fees"
- "**Church** raised funds for organ"

#### 6. Legal Agency
Entity acts as legal person in proceedings or applications.

**Patterns:**
- [entity] applied for licence, fined, prosecuted, charged
- [entity] sued, summoned, appealed, contested

**Examples:**
- "**Megalong Hotel applied** for publican's licence"
- "**Church was fined** for building violations"
- "**School committee** appealed decision"

#### 7. Competition/Marketing
Entity competes commercially or promotes itself.

**Patterns:**
- [entity] competing with, attracting customers
- [entity] advertising, promoting, marketing

**Examples:**
- "**Hotel competing** for tourist trade"
- "**School of Arts** advertised new programs"

### Both (Polyhierarchical) Indicators

#### When to Use "Both"

**Mixed Signals:**
Context contains substantial indicators for both building AND business/organisation.

**Example:**
> "The Megalong Hotel is conveniently situated near Nellie's Glen [building: spatial] and offers special rates for visitors [business: services]. Guests staying at the hotel [building: accommodation] praised the proprietor's hospitality [business: ownership]."

**Metonymic Usage:**
Entity name shifts meaning within same context, referring to both structure and organisation.

**Example:**
> "Fire damaged the church [building: structure] last night, but the church [organisation: congregation] vows to rebuild."

**Parallel Constructions:**
Text explicitly treats entity as both place and actor in parallel.

**Example:**
> "Concert at the School of Arts [building: venue] was organised by the School of Arts committee [organisation: agent]."

## Special Cases and Edge Cases

### Metonymy: Entity Name as Shorthand

When entity name stands for different referents, classify by intended meaning:

**"Hotel" = Management/Proprietor (Business):**
- "The hotel denies the accusation"
- "Hotel claims no responsibility"
- "Hotel refuses to comment"

**"Hotel" = Physical Structure (Building):**
- "The hotel is located on Main Street"
- "Fire threatened the hotel"
- "Hotel underwent repairs"

**"Church" = Congregation/Leadership (Organisation):**
- "The church condemns the proposal"
- "Church welcomes new minister"
- "Church voted to support mission"

**"Church" = Worship Building (Building):**
- "Service at the church on Sunday"
- "Church seats 200 people"
- "Lightning struck the church"

### Passive Agency: Who Initiates Action?

**Passive Voice = Building (Recipient):**
- "The hotel **was refurbished**" (someone refurbished it)
- "Church **was consecrated**" (bishop consecrated it)
- "Hall **was decorated**" (committee decorated it)

**Active Voice = Business (Agent):**
- "The hotel **refurbished** its premises" (hotel as agent)
- "Church **appointed** new clergy" (church as agent)
- "Hall committee **decorated** the venue" (committee as agent)

### Events vs Services: Hosting vs Operating

**Hosting Third-Party Events = Building:**
- "Concert **at** the hotel" (hotel is venue)
- "Meeting **held in** the hall" (hall is space)
- "Service **at** the church" (church is location)

**Operating Own Events/Services = Business:**
- "Hotel concert series" (hotel-organised)
- "School of Arts lecture program" (school-operated)
- "Church Sunday school" (church-operated service)

### Advertisements and Genre Context

**Advertisements = Business Agency:**
Even when using spatial language, advertisements show business promoting itself.

**Example:**
> "The Carrington Hotel [advertisement context] is favourably situated [spatial language] and offers excellent accommodation [service provision]."

**Classification:** both - Advertisement (business) describing location (building)

**Licensing Applications = Business:**
Applications are business/legal documents even when describing physical premises.

**Example:**
> "Application for licence for premises known as Megalong Hotel, containing six rooms [physical description] as per plans lodged [legal process]."

**Classification:** business - Legal/business document about operating licence

### Court Testimony: Scene vs Agent

**Entity as Crime Scene = Building:**
- "Arrest occurred **at the hotel**"
- "Witness saw accused **near the church**"
- "Fight broke out **in the hall**"

**Entity as Business Defendant = Business:**
- "Hotel **was prosecuted** for licensing breach"
- "Proprietor of hotel **appeared in court**"
- "Church **appealed** the fine"

## Confidence Calibration

### High Confidence
- Multiple strong indicators present (3+)
- Clear unambiguous context
- No contradictory signals
- Genre context reinforces classification

### Medium Confidence
- Some indicators present (1-2 strong, or several weak)
- Context could support alternative reading
- Mixed signals but one clearly dominant
- Limited context available

### Low Confidence
- Minimal or no strong indicators
- Genuinely ambiguous context
- Relying on defaults
- Insufficient context to determine

## Default Guidance by Entity Type

When indicators are weak or absent, apply these defaults:

### Hotels, Inns, Public Houses
**Default:** building

**Rationale:** Most newspaper mentions use hotels as locations (events occurring, people staying, incidents happening). Business operations less frequently mentioned.

**Override when:** Explicit business operations, proprietor agency, licensing, services marketed.

### Churches, Chapels
**Default:** Consider denomination and context

- **Worship events, services** → building
- **Governance, appointments, denominational actions** → organisation
- **Mixed religious and administrative** → both

### Schools of Arts, Mechanics' Institutes
**Default:** Depends on activity

- **Events, concerts, meetings** → building (venue usage)
- **Committee decisions, membership, programs** → organisation
- **Event announcements by committee** → both

### Fraternal Lodge Halls
**Default:** building

**Rationale:** Usually references to meeting location unless explicitly about lodge organisation/membership.

**Override when:** Lodge governance, membership actions, fraternal order business.

### Schools (Educational)
**Default:** Requires careful analysis

- **Students attending, classes occurring** → building (facility)
- **School policy, hiring, governance** → organisation (institution)
- **Often both** → School as institution AND physical campus

## Quality Checklist

Before finalising classification, verify:

- [ ] Read full context carefully (not just entity mention)
- [ ] Identified grammatical role (subject, object, locative)
- [ ] Noted prepositions and verbs surrounding mention
- [ ] Checked for agency (is entity acting or being acted upon?)
- [ ] Considered context genre (advertisement, legal, news, etc.)
- [ ] Applied metonymy test (what does entity name refer to?)
- [ ] Assessed voice (passive recipient vs active agent)
- [ ] Recorded specific evidence for classification
- [ ] Assigned appropriate confidence level
- [ ] Flagged for human review if genuinely ambiguous
