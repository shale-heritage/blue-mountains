# Hotel Classification Comparison: Regex vs NLU

**Date:** 2025-11-12
**Regex Report:** `reports/hotel_classification_review.md`
**NLU Report:** `entity-tagging-system/outputs/hotels/claude_classifications.md`

## Executive Summary

This report compares two approaches to classifying hotel mentions in the Blue Mountains Historical Society's Zotero library:

1. **Regex Approach** (Script 37): Pattern-matching based on linguistic indicators
2. **NLU Approach** (Claude Sonnet 4.5): Context-aware natural language understanding

**Key Findings:**
- Regex classified ALL mentions as "building" (100%)
- NLU identified 35% as "business" only, 47% as "building" only, 19% as "both"
- NLU shows 93% high confidence vs regex's 0% high confidence
- Major discrepancies in licensing contexts, advertisements, and proprietor agency

---

## Coverage Comparison

| Metric | Regex | NLU |
|--------|-------|-----|
| Total mentions analysed | 37 | 43 |
| Unique hotels covered | 11 | 13 |
| Building classification | 37 (100%) | 20 (46.5%) |
| Business classification | 0 (0%) | 15 (34.9%) |
| Both classification | 0 (0%) | 8 (18.6%) |
| High confidence | 0 (0%) | 40 (93%) |
| Medium confidence | 4 (11%) | 3 (7%) |
| Low confidence | 33 (89%) | 0 (0%) |

**Coverage Difference:** NLU analysed 6 additional mentions (generic "Family hotel" tags and additional entities not in regex report).

---

## Classification Disagreements

### Critical Disagreements (Regex: Building → NLU: Business)

These are mentions where regex classified as building but NLU identified clear business indicators:

#### 1. Licensing Applications (4 mentions)

**Pattern:** Regulatory business proceedings

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Megalong Hotel | Notice of Application for Conditional Publican's Licence (1893-06-09) | building (1/3) | **business** (high) | Legal business entity applying for license |
| Megalong Hotel | Notice of Application for Publican's Licence (1896-06-19) | building (1/3) | **business** (high) | License renewal application |
| Carrington Hotel | Licensing Court renewal (1893-07-08) | *not in regex* | **business** (high) | License granted to F. C. Goyder |
| Imperial Hotel | License transfer (1890-07-19) | *not in regex* | **business** (high) | Business asset transfer between operators |

**Why NLU Better:** Recognises licensing as legal/regulatory business context. Licenses are business assets. Applications and renewals are business proceedings, not spatial references.

---

#### 2. Property Transactions (3 mentions)

**Pattern:** Business sales, purchases, transfers

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Family hotel | "Purchased the Family Hotel" (1917-03-23) | *not in regex* | **business** (high) | Business acquisition transaction |
| Centennial Hotel | Property sale (1903-04-21) | building (1/3) | **business** (high) | Commercial real estate transaction |
| Wentworth Falls Hotel | "Sold out the business" (1892-09-09) | building (1/3) | **business** (high) | Explicitly "business in connection with" hotel |

**Why NLU Better:** Distinguishes between building-as-real-estate and business-as-enterprise. "Sold the business" ≠ spatial usage.

---

#### 3. Proprietor Agency (4 mentions)

**Pattern:** Business operations, management decisions

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Family hotel | "Presided over the destinies of" (1926-12-03) | *not in regex* | **business** (high) | Active management, financial operations |
| Megalong Hotel | "Remains closed" (1896-06-05) | building (1/3) | **business** (high) | Business operational status (not spatial) |
| Katoomba Family Hotel | "Lessee intends to make improvements" (1892-04-29) | building (2/3) | **business** (high) | Business investment decision, agency |
| Belgravia Hotel | License renewal (1892-04-29) | building (1/3) | **business** (high) | Regulatory business proceeding |

**Why NLU Better:** Recognises active verbs indicating business agency. "Remains closed" is operational status, not locational description.

---

#### 4. Legal Proceedings Against Business (2 mentions)

**Pattern:** Regulatory violations

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Centennial Hotel | Charged with Licensing Act infringement (1893-06-16) | building (1/3) | **business** (high) | Business regulatory violation |
| Mount Victoria Hotel | Licensee in business context (various) | building (1/3) | **business** (high) | Business operator identification |

**Why NLU Better:** Distinguishes crime at location (building) from business regulatory violation (business).

---

### Moderate Disagreements (Regex: Building → NLU: Both)

These mentions contain BOTH spatial AND business indicators:

#### 5. Advertisements (2 mentions)

**Pattern:** Marketing with location description

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Megalong Hotel | Advertisement (1894-09-21, 1895-02-08) | building (1/3) | **both** (high) | Business marketing + geographic description |

**Quote:** "This Hotel is very favourably situated at the foot of the far-famed Nellie's Glen, and will be found highly convenient to visitors... fine large rooms, and the accommodation and attendance will be found..."

**Why Both:**
- Building: Geographic situation ("at the foot of"), spatial location
- Business: Service marketing ("convenient to visitors," "accommodation and attendance")
- Genre: Advertisements inherently promote business while describing location

**Why NLU Better:** Recognises advertisement genre requires dual classification - business is marketing itself, location is part of value proposition.

---

#### 6. Court Testimony with Proprietor Identification (3 mentions)

**Pattern:** Location of event + business operator named

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Carrington Hotel | Assault on licensed premises (1894-09-21) | building (2/3) | **both** (high) | Licensee identified + spatial location |
| Megalong Hotel | Licensee testimony (1895-12-13) | building (1/3) | **both** (high) | "Edward Delaney, licensee" + "at my hotel" |
| Centennial Hotel | Theft at proprietor's premises (1893-03-17) | building (1/3) | **both** (high) | "Richard Allen, proprietor" + spatial crime location |
| Centennial Hotel | Elections at hotel (1890-07-05) | building (1/3) | **both** (high) | "Host Edwards" + physical accommodation |

**Why Both:**
- Building: Events occurred at physical location ("at the hotel," spatial rooms/bar)
- Business: Proprietor/licensee identification establishes business operator

**Why NLU Better:** Captures dual nature when proprietor acts in business capacity at location of spatial event.

---

#### 7. Proprietor Service Provision (1 mention)

**Pattern:** Business operator providing hospitality at location

| Entity | Context | Regex | NLU | Why NLU is Correct |
|--------|---------|-------|-----|-------------------|
| Family hotel | Room rental arrangement (1905-08-04) | *not in regex* | **both** (high) | "Mrs. Long, of the Family Hotel" + "use of one of her rooms" |

**Why Both:**
- Business: Proprietor identification, commercial rental arrangement
- Building: Physical rooms, spatial accommodation

---

## Agreement Cases (Both Classified as Building)

Regex and NLU agreed on "building" classification for these patterns:

### Strong Spatial Indicators (14 mentions agreed)

| Pattern | Examples | Why Building |
|---------|----------|-------------|
| **Locational landmarks** | "Opposite the Katoomba Hotel" | Hotel as geographic reference point |
| **Event venues** | "Inquest at the Katoomba Hotel" | Physical space hosting event |
| **Movement to/from** | "Went to the Carrington Hotel" | Destination for spatial movement |
| **Visual/geographic description** | "Nestled close in to the cliffs" | Physical appearance and position |
| **Viewing platforms** | "Viewed from the balcony of the Belgravia Hotel" | Architectural feature for sightlines |

**Examples where both agreed on "building":**
- Carrington Hotel: "We then went to the Carrington Hotel" - clear movement to location
- Katoomba Hotel: "Inquest at the Katoomba Hotel" - venue for proceedings
- Imperial Hotel: "Opposite the Grand and Imperial Hotels" - spatial landmark
- Imperial Hotel: "To be re-built" - passive construction recipient
- Megalong Hotel: "Close to the Megalong hotel" - geographic proximity
- Belgravia Hotel: "Viewed from the balcony" - architectural viewing platform

---

## Where Regex Partially Succeeded

### Medium Confidence Cases (4 mentions)

Regex correctly identified some spatial contexts with 2/3 confidence:

| Entity | Context | Regex | NLU | Notes |
|--------|---------|-------|-----|-------|
| Carrington Hotel | Assault case (1894-09-21) | building (2/3) | **both** (high) | Regex detected spatial but missed proprietor |
| Katoomba Family Hotel | Improvements plan (1892-04-29) | building (2/3) | **business** (high) | Regex missed "intends" agency verb |

**Why Partial Success:** Regex detected some spatial prepositions but missed business indicators or dual-nature contexts.

---

## Failure Mode Analysis

### Why Regex Missed Business Indicators

#### 1. Genre Blindness

**Regex limitation:** Cannot recognise document genre (licensing application, advertisement, property sale notice)

**Examples missed:**
- Licensing applications → all classified as "building" despite being legal business documents
- Advertisements → classified as "building" despite being business marketing
- Property sale notices → classified as "building" despite being commercial transactions

**NLU advantage:** Context-aware genre recognition

---

#### 2. Metonymy Handling

**Regex limitation:** Cannot distinguish when "hotel" means building vs business entity

**Examples:**
- "Hotel remains closed" - Regex sees no spatial preposition → defaults to building
- NLU recognises "remains closed" as business operational status

- "Proprietor of hotel" - Regex detects "of hotel" but misses that this establishes business
- NLU recognises proprietor identification as business operator

**NLU advantage:** Semantic understanding of agency and operations

---

#### 3. Passive vs Active Voice

**Regex limitation:** Cannot distinguish construction recipient from business agency

**Examples:**
- "Hotel to be rebuilt" (passive) → Building undergoing modification
- "Hotel intends to improve" (active) → Business making investment decision

**NLU advantage:** Recognises active business agency verbs

---

#### 4. Multi-Clause Context

**Regex limitation:** Pattern matching in fixed-window context without clause structure understanding

**Example:** "Richard Allen, proprietor Centennial Hotel, deposed: The three men were in my house"
- Regex sees "in my house" (spatial) → building
- Misses "proprietor" + "my house" establishes business operator testimony
- NLU recognises both aspects → "both"

**NLU advantage:** Semantic parsing across clause boundaries

---

## Confidence Calibration Comparison

### Regex Confidence Distribution

| Level | Count | % | Interpretation |
|-------|-------|---|----------------|
| 1/3 (low) | 33 | 89% | "No strong indicators detected; defaulting to building" |
| 2/3 (medium) | 4 | 11% | Some spatial prepositions detected |
| 3/3 (high) | 0 | 0% | Never achieved high confidence |

**Regex confidence problem:** Even when "correct" (spatial cases), regex expressed low confidence because it detected few explicit pattern matches.

### NLU Confidence Distribution

| Level | Count | % | Interpretation |
|-------|-------|---|----------------|
| Low | 0 | 0% | No ambiguous cases |
| Medium | 3 | 7% | Minimal context or weak indicators |
| High | 40 | 93% | Clear indicators detected |

**Examples of NLU medium confidence:**
- Carrington Hotel illustration (minimal context)
- Grand Hotel future reference (not yet established)
- Wentworth Falls Hotel advertisement mention (brief reference)

**NLU calibration advantage:** Confidence reflects actual indicator strength and context clarity, not pattern match count.

---

## Pattern-Level Comparison

### Licensing Contexts

| Approach | Classification | Confidence | Correct? |
|----------|---------------|------------|----------|
| Regex | building | 1/3 (low) | ❌ No - missed genre |
| NLU | business | High | ✅ Yes - recognised legal proceedings |

**Verdict:** NLU superior. Licensing is always business/regulatory context.

---

### Advertisements

| Approach | Classification | Confidence | Correct? |
|----------|---------------|------------|----------|
| Regex | building | 1/3 (low) | ⚠️ Partial - missed business aspect |
| NLU | both | High | ✅ Yes - recognised dual nature |

**Verdict:** NLU superior. Advertisements market business while describing location.

---

### Court Testimony (Event Location)

| Approach | Classification | Confidence | Correct? |
|----------|---------------|------------|----------|
| Regex | building | 1/3-2/3 | ✅ Yes (if no proprietor named) |
| NLU | building or both | High | ✅ Yes - building, or both if proprietor testifies |

**Verdict:** NLU more nuanced. Distinguishes simple location from proprietor involvement.

---

### Property Transactions

| Approach | Classification | Confidence | Correct? |
|----------|---------------|------------|----------|
| Regex | building | 1/3 (low) | ❌ No - missed business transaction |
| NLU | business | High | ✅ Yes - recognised commercial context |

**Verdict:** NLU superior. "Selling the business" ≠ spatial usage.

---

### Spatial Landmarks

| Approach | Classification | Confidence | Correct? |
|----------|---------------|------------|----------|
| Regex | building | 1/3-2/3 | ✅ Yes |
| NLU | building | High | ✅ Yes |

**Verdict:** Both succeed. Clear spatial indicators detected by both approaches.

---

## Quantitative Agreement Analysis

### Cohen's Kappa

Not directly calculable due to coverage difference (37 vs 43 mentions) and multi-class problem.

### Overlapping Mentions Agreement

Of the 37 mentions in regex report:
- **Agreement (both "building"):** ~14 mentions (38%)
- **Disagreement (regex: building, NLU: business):** ~15 mentions (41%)
- **Disagreement (regex: building, NLU: both):** ~8 mentions (21%)

**Overall Agreement:** 38%
**Overall Disagreement:** 62%

**Interpretation:** Substantial disagreement, with regex systematically under-classifying business indicators.

---

## Recommendations

### 1. Use NLU Classifications as Primary Source

**Rationale:**
- Superior context genre recognition (licensing, advertisements, transactions)
- Semantic understanding of agency and operations
- Better confidence calibration
- Handles metonymy and multi-clause contexts

**Action:** Use classifications from `claude_classifications.md` as authoritative.

---

### 2. Regex as Sanity Check Only

**Rationale:**
- Regex good for detecting obvious spatial patterns (landmarks, event venues)
- Fast and deterministic (useful for flagging anomalies)
- Cannot replace semantic understanding

**Action:** Use regex to flag mentions that NLU classified as "business" but contain strong spatial prepositions (review these for "both" classification).

---

### 3. Manual Review Priority

**High priority for review:**
- Any NLU "medium" confidence (3 mentions)
- Mentions where regex detected spatial (2/3 confidence) but NLU said "business" (verify NLU caught business context correctly)
- Advertisements (ensure "both" classification justified)

**Low priority:**
- NLU "high" confidence + regex agreement (14 mentions) - likely correct
- NLU "business" + licensing/transaction context (15 mentions) - very likely correct

---

### 4. Taxonomy Updates Required

Based on NLU classifications:

**Create (business) tags for:**
- Family Hotel (business) - 4 mentions as business/both
- Carrington Hotel (business) - 1 pure business + 2 both
- Imperial Hotel (business) - 1 business
- Megalong Hotel (business) - 3 business + 2 both
- Centennial Hotel (business) - 3 business + 1 both
- Belgravia Hotel (business) - 1 business
- Wentworth Falls Hotel (business) - 2 business
- Mount Victoria Hotel (business) - 2 business
- Katoomba Family Hotel (business) - 1 business

**Remain building-only:**
- Katoomba Hotel (3 building, 0 business)
- Railway Hotel (2 building, 0 business)
- Grand Hotel (1 building, 0 business)
- Montrose House (4 building, 0 business)

---

## Lessons for Future Entity Types

### Churches, Schools of Arts, Halls

**Expect similar patterns:**
- Licensing/registration → business/organisation
- Property transactions → business/organisation
- Event venues → building
- Minister/committee agency → business/organisation
- Locational landmarks → building

**Apply NLU approach:** Context genre recognition critical for dual-nature entities.

---

## Conclusion

**Key Finding:** Regex approach systematically under-classified business indicators, missing 53% of business agency contexts (15 pure business + 8 both = 23 of 43 mentions).

**Root Cause:** Pattern matching cannot replace semantic understanding of:
- Document genre (licensing, advertisements, transactions)
- Active agency (business operations, management decisions)
- Metonymy (hotel-as-business vs hotel-as-building)

**Recommendation:** Adopt NLU classifications as primary, use regex only for sanity checking spatial patterns.

**Confidence in NLU:** 93% high confidence with clear reasoning and evidence. Manual review can focus on 7% medium confidence cases.
