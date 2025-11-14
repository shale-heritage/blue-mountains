# Entity Classification Heuristic: Building vs Business/Organisation

## Purpose

Determine whether entities (hotels, churches, schools of arts, halls, etc.) should be classified as:
- **(a) Building only** - Physical structure facet only (Built Environment)
- **(b) Business/Organisation only** - Agent facet only (Agents > Organisations)
- **(c) Both (polyhierarchical)** - Appears in both facets

## Core Principle

The classification depends on **how the entity is represented in the source text**, not our external knowledge. We're tagging what the text *is about*, not what we know the entity to be.

## Decision Framework

### (a) Building Only - Spatial/Physical Indicators

**Strong indicators:**
- **Locational prepositions**: at, in, within, inside, outside, on, near, opposite, adjacent to
- **Movement verbs**: going to, coming from, arriving at, leaving, departing, walking to, travelling to
- **Events occurring**: meeting held at, concert at, ball at, dinner at, auction at, court session at
- **Physical descriptions**: the building, the structure, the premises, the rooms, the veranda
- **Construction/modification**: built, erected, demolished, burned down, renovated (as passive subject)
- **Physical features**: "the hotel's bar room", "the church's vestry", "the hall's stage"
- **Occupancy**: staying at, lodging at, residing at, accommodated at

**Example contexts:**
- "A meeting was held at the Carrington Hotel last evening"
- "The concert took place in the School of Arts"
- "Fire destroyed the Imperial Hotel building"
- "Guests staying at the hotel witnessed the incident"

### (b) Business/Organisation Only - Agency Indicators

**Strong indicators:**
- **Agency verbs**: expanding, refurbishing, opening, closing, advertising, announcing, deciding
- **Ownership/management**: proprietor, lessee, owner, manager, keeper, committee (as subject)
- **Business operations**: licensed, opened for season, closed for repairs, commenced trading
- **Financial actions**: selling, purchasing, paying rent, generating revenue, offering discounts
- **Employment**: hiring, dismissing, employing staff, seeking workers
- **Services**: offering, providing, catering, serving, hosting (as active agent)
- **Competition**: competing with, attracting customers, undercutting prices
- **Legal status**: applying for licence, losing licence, being prosecuted (as corporate entity)

**Example contexts:**
- "The Carrington Hotel has announced extensive renovations"
- "The Methodist Church appointed a new minister"
- "The School of Arts committee voted to extend opening hours"
- "The hotel proprietor was fined for breaching licensing conditions"

### (c) Both (Polyhierarchical) - Dual Nature Indicators

**Strong indicators:**
- **Mixed spatial and agency cues** in same text
- **Metonymic usage** where entity name stands for both place and organisation
- **Parallel constructions** treating entity as both space and actor

**Example contexts:**
- "The Carrington Hotel [building] hosted a ball last night, with the hotel [business] providing refreshments" (Both)
- "Fire destroyed the church [building], but the congregation [organisation] plans to rebuild" (Both entities, separate tags)
- "The School of Arts [building] was packed, with the School of Arts [organisation] reporting record attendance" (Both)

## Special Cases

### Metonymy
When entity name is used as shorthand:
- "The hotel denies the accusation" → Business (hotel = proprietor/management)
- "The church condemns the proposal" → Organisation (church = congregation/leadership)
- **Rule**: Treat as the intended referent, not the literal term

### Passive Agency
When entity undergoes changes:
- "The hotel was refurbished" → Building (passive recipient of work)
- "The hotel refurbished its premises" → Business (active agent performing work)
- **Rule**: Who initiates the action determines classification

### Events vs Services
Distinction between hosting and operating:
- "Concert at the hotel" → Building (venue for third-party event)
- "Hotel concert series" → Business (hotel-operated service)
- **Rule**: If entity is merely location, classify as building; if entity organises, classify as business

## Application Workflow

1. **Read full context** (2-4 sentences around mention)
2. **Identify grammatical role** (subject, object, locative complement)
3. **Note prepositions/verbs** surrounding entity mention
4. **Check for agency** (is entity acting, or being acted upon/in?)
5. **Classify using indicators** above
6. **Document reasoning** for review

## Confidence Levels

- **High confidence**: Text strongly indicates one aspect only
- **Medium confidence**: Text leans toward one but could support both
- **Low confidence/Ambiguous**: Text genuinely unclear; default to building for spatial, business for agency verbs

## Edge Cases Requiring Human Review

- Unclear grammatical structure
- Insufficient context (isolated mentions)
- Novel usage patterns not covered by heuristic
- Contradictory signals within same passage

## Notes on Reuse

This heuristic applies to:
- Hotels, inns, public houses
- Churches, chapels, places of worship
- Schools of Arts, Mechanics' Institutes, community halls
- Fraternal lodge halls (Masonic Hall, Oddfellows' Hall)
- Any dual-nature entity that can be both place and organisation
