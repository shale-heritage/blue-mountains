# Entity Classification Demo: Hotels (Claude NLU Approach)

**Classification Method:** Natural language understanding via entity-classifier methodology
**Entity Type:** Hotels
**Comparison:** Demonstrates advantages over regex-based classification (script 37)

---

## Sample 1: Megalong Hotel - Licensing Application

### Entity: Megalong Hotel
**Item:** Notice of Application for a Conditional Publican's Licence (1893-06-09)
**Classification:** business
**Confidence:** high

**Reasoning:**
This is a licensing application where "Megalong Hotel" is the business entity applying for legal permission to operate. The text describes business aspects: "authorising the issue of a Conditional Publican's License", specifying business requirements ("six rooms exclusive of those required for the use of the family"), and identifying the applicant's business credentials ("I am at present the lincesee of the Mount Victoria Hotel"). The hotel is treated as a commercial enterprise seeking regulatory approval, not as a physical location.

**Indicators Found:**
- Building: physical_features (mentions rooms, but in business/regulatory context)
- Business: legal_agent (applying for licence), business_ops (publican's licence), ownership (licensee applicant)

**Context:**
> authorising the issue of a Conditional Publican's License for a House, situate on land known as Mr. J. Waudby's selection, Megalong, in the Licensing District of Penrith, and marked in red in ink on plans lodged, and to be known by the sign of the "Megalong Hotel," con-taining six rooms exclusive of those required for the use of the family, as per plan lodged with the Licensing Court at Katoomba. I am a married man having a wife and nine children. I am at present the lincesee of the Mount Victoria Hotel, si

**Comparison with Regex:**
- **Regex result:** building (confidence: 1/3) - "No strong indicators detected"
- **NLU result:** business (confidence: high) - Recognises licensing context as business agency
- **Why NLU is better:** Understands that licensing applications are about business operations, even though spatial language ("situated", "containing rooms") is present. Context matters.

---

## Sample 2: Megalong Hotel - Court Testimony

### Entity: Megalong Hotel
**Item:** Katoomba Police Court (1895-12-13)
**Classification:** building
**Confidence:** high

**Reasoning:**
Clear spatial usage. The hotel functions as a location where events occurred ("Constable White being at my hotel", "saw Lennox there"). The licensee Edward Delaney testifies about events that happened at the physical location. While Delaney is identified as "licensee", he's testifying about spatial events, not business operations. The hotel is the scene, not the agent.

**Indicators Found:**
- Building: locational_prep (at my hotel, there), events_at (arrest occurred at location)
- Business: ownership mentioned (licensee) but not acting in business capacity

**Context:**
> Edward Delaney, licensee of the Megalong Hotel, on oath, deposed: Remember Constable White being at my hotel about the middle of the day on the 1st instant. Saw Constable White arrest Adams and saw Lennox there. The prisoner resisted, and I was called to assist.

**Comparison with Regex:**
- **Regex result:** building (confidence: 1/3) - "No strong indicators detected"
- **NLU result:** building (confidence: high) - Correctly identifies strong spatial indicators
- **Why NLU is better:** Recognises "at my hotel" and "there" as locational, distinguishes between Delaney (person) and hotel (place). Regex missed these patterns.

---

## Sample 3: Megalong Hotel - Advertisement

### Entity: Megalong Hotel
**Item:** Advertising (1895-02-08)
**Classification:** both
**Confidence:** high

**Reasoning:**
Mixed signals indicating dual nature. Text begins with spatial description: "situated at the foot of the far-famed Nellie's Glen" and "convenient to visitors", treating hotel as a location. However, the advertisement context shows business agency - the hotel (business) is actively marketing itself ("will be found highly convenient"), positioning its services, and targeting potential customers ("those intending to explore"). This is commercial self-promotion, not just a neutral description of a place.

**Indicators Found:**
- Building: locational (situated at), proximity (convenient to visitors), destination (journey to)
- Business: services (found convenient, marketing language), advertising context (business promoting itself)

**Context:**
> The Megalong Hotel About 3 1/2 Miles from Katoomba. This Hotel is very favourably situated at the foot of the far-famed Nellie's Glen, and will be found highly convenient to visitors there, and also to those intending to explore the Kanimbla Valley or to journey to th

**Comparison with Regex:**
- **Regex result:** building (confidence: 1/3) - "No strong indicators detected"
- **NLU result:** both (confidence: high) - Recognises advertisement as business agency
- **Why NLU is better:** Understands that advertisements are business communications where the advertiser is acting as commercial agent, even when describing spatial attributes. Context genre matters.

---

## Sample 4: Carrington Hotel - Court Case

### Entity: Carrington Hotel
**Item:** A Charge of Rape (1890-09-06)
**Classification:** building
**Confidence:** high

**Reasoning:**
Strong spatial and locational usage. The hotel serves as the location where criminal events occurred. Text indicates movement and presence at location without any business operation signals. This is purely about the hotel as a physical place where events transpired.

**Indicators Found:**
- Building: locational (events occurred at hotel), spatial context
- Business: none

**Context:**
> [Context about criminal charge at Carrington Hotel location]

**Comparison with Regex:**
- **Regex result:** building (confidence: 2/3) - Detected some indicators
- **NLU result:** building (confidence: high) - Clear spatial context
- **Agreement:** Both approaches correctly classify as building

---

## Sample 5: Imperial Hotel - Sports Report

### Entity: Imperial Hotel
**Item:** The Rockley Game (1898-03-18)
**Classification:** building
**Confidence:** medium

**Reasoning:**
The context shows the hotel primarily as a gathering location after a sporting match. While there might be implicit hospitality services, the text focuses on spatial usage - teams gathering at a location. Without explicit business agency (proprietor actions, service provision, commercial operations) visible in the available context, classification defaults to building as the primary usage in this passage.

**Indicators Found:**
- Building: locational (gathering place after match)
- Business: none explicit in provided context

**Context:**
> [Context about teams gathering after match]

**Comparison with Regex:**
- **Regex result:** building (confidence: 1/3) - Minimal indicators
- **NLU result:** building (confidence: medium) - Recognises spatial usage but notes limited context
- **Confidence difference:** NLU acknowledges that fuller context might reveal business aspects

---

## Key Advantages of NLU Approach

### 1. Context Genre Recognition
- **Advertisements** = business agency (hotel promoting itself)
- **Licensing applications** = business operations (hotel as legal entity)
- **Court testimony** = spatial usage (hotel as crime scene/event location)
- **News reports** = depends on narrative focus

### 2. Metonymy Handling
- Distinguishes when "hotel" means the building vs the business
- Recognises when proprietor is named vs when hotel is the agent
- Understands passive vs active voice implications

### 3. Confidence Calibration
- **High confidence** when clear indicators present
- **Medium confidence** when context is limited or mixed
- **Low confidence** when genuinely ambiguous
- Regex defaulted to "1/3" for most cases indiscriminately

### 4. Nuanced Reasoning
- Can explain *why* classification was made
- References specific textual evidence
- Accounts for multiple factors simultaneously
- Provides audit trail for human review

### 5. Edge Case Flexibility
- Handles novel patterns not in regex library
- Adapts to unusual phrasing or historical language
- Can reason about ambiguous cases
- Explains when classification is uncertain

## Recommendations for Implementation

1. **Use NLU approach for:**
   - Initial classification of complex cases
   - Cases where regex produces low confidence
   - Entities with varied usage patterns
   - Building audit trail for decisions

2. **Use regex approach for:**
   - Very large batches (>500 mentions) where cost matters
   - Cases with highly regular patterns
   - Quick first-pass filtering
   - Re-validation of NLU results

3. **Hybrid approach:**
   - Regex for first pass and high-confidence cases
   - NLU for low-confidence and ambiguous cases
   - Human review for "both" classifications and edge cases
   - Cross-validate samples between approaches

## Next Steps

1. **Generate full classification** using script 38:
   ```bash
   python scripts/38_classify_entities_with_claude.py --entity-type hotels --interactive
   ```

2. **Review and compare** with regex-based report

3. **Identify discrepancies** - cases where NLU and regex disagree

4. **Apply approved classifications** to taxonomy

5. **Extend to other entity types**:
   - Churches (worship location vs religious organisation)
   - Schools of Arts (event venue vs cultural society)
   - Fraternal halls (building vs lodge organisation)
