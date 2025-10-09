# Vocabulary Standards and Mappings

**Project:** Blue Mountains Shale Mining Communities Digital Collection Software
**Purpose:** Documentation of controlled vocabularies and semantic mappings
**Standards:** Getty Vocabularies (AAT, TGN), Gazetteer of Australia, Research Vocabularies Australia (RVA), SKOS, Dublin Core

---

## Overview

This project uses controlled vocabularies following FAIR principles for research data. Tags extracted from the Zotero library will be mapped to international and Australian standards to enable interoperability, discovery, and semantic web integration.

**Vocabulary Strategy:**

1. **Tag Rationalisation:** Clean and consolidate folksonomy tags from Zotero
2. **Hierarchical Structure:** Develop broader/narrower term relationships
3. **International Mapping:** Link to Getty Vocabularies (AAT, TGN)
4. **Australian Mapping:** Link to Gazetteer of Australia for place names
5. **Publishing:** Publish project vocabulary to Research Vocabularies Australia
6. **Metadata:** Apply Dublin Core terms for Omeka Classic publication

---

## Vocabulary Ecosystem

```text
┌─────────────────────────────────────────────────────────────┐
│                    Blue Mountains Project                    │
│                   Folksonomy Tags (481)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├──► Getty AAT (Concepts, Activities, Materials)
                 │    http://vocab.getty.edu/aat/
                 │
                 ├──► Getty TGN (Places, Historic Sites)
                 │    http://vocab.getty.edu/tgn/
                 │
                 ├──► Gazetteer of Australia (Australian Places)
                 │    Composite Gazetteer (GeoPackage)
                 │
                 └──► Research Vocabularies Australia (RVA)
                      https://vocabs.ardc.edu.au/
                      (Project-specific controlled vocabulary)
```

---

## 1. Getty Vocabularies

### Art & Architecture Thesaurus (AAT)

**Purpose:** Standardised concepts for art, architecture, decorative arts, archival materials, and material culture

**URL:** http://vocab.getty.edu/aat/

**Scope for This Project:**
- Activities (e.g., mining, labour, transport)
- Materials (e.g., shale, kerosene, oil)
- Object types (e.g., tools, dwellings, machinery)
- Styles and periods
- Processes and techniques

**Example Mappings:**

| Local Tag | AAT Concept | AAT ID | URI | Relationship |
|-----------|-------------|--------|-----|--------------|
| Mining | mining (extracting) | 300053857 | http://vocab.getty.edu/aat/300053857 | exactMatch |
| Shale | shale (rock) | 300011791 | http://vocab.getty.edu/aat/300011791 | exactMatch |
| Kerosene | kerosene | 300014880 | http://vocab.getty.edu/aat/300014880 | exactMatch |
| Dwelling | dwellings | 300004037 | http://vocab.getty.edu/aat/300004037 | broadMatch |
| Miners | miners (people) | 300025334 | http://vocab.getty.edu/aat/300025334 | exactMatch |
| Labour | labor (work) | 300069214 | http://vocab.getty.edu/aat/300069214 | exactMatch |
| Accident | accidents | 300054559 | http://vocab.getty.edu/aat/300054559 | exactMatch |
| Court | courts (institutions) | 300025987 | http://vocab.getty.edu/aat/300025987 | closeMatch |

**Access Methods:**

1. **Web Interface:** Browse and search at http://www.getty.edu/research/tools/vocabularies/aat/
2. **SPARQL Endpoint:** http://vocab.getty.edu/sparql
3. **Linked Open Data:** Dereferenceable URIs (content negotiation)

**Query Example (SPARQL):**

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gvp: <http://vocab.getty.edu/ontology#>

SELECT ?concept ?prefLabel ?scopeNote WHERE {
  ?concept skos:inScheme aat: ;
           luc:term "mining" ;
           skos:prefLabel ?prefLabel ;
           skos:scopeNote ?scopeNote .
  FILTER (lang(?prefLabel) = "en")
}
LIMIT 10
```

**Python Integration:**

```python
from SPARQLWrapper import SPARQLWrapper, JSON

def query_aat(search_term):
    """
    Query Getty AAT for concepts matching search term.

    Parameters:
        search_term (str): Term to search for

    Returns:
        list: Matching concepts with URIs and labels
    """
    sparql = SPARQLWrapper("http://vocab.getty.edu/sparql")

    query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX luc: <http://www.ontotext.com/owlim/lucene#>
    PREFIX aat: <http://vocab.getty.edu/aat/>

    SELECT ?concept ?label ?id WHERE {{
      ?concept luc:term "{search_term}" ;
               skos:inScheme aat: ;
               skos:prefLabel ?label ;
               gvp:prefLabelGVP [xl:literalForm ?label] ;
               dcterms:identifier ?id .
      FILTER (lang(?label) = "en")
    }}
    LIMIT 10
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results["results"]["bindings"]
```

---

### Thesaurus of Geographic Names (TGN)

**Purpose:** Hierarchical vocabulary of geographic places, both current and historical

**URL:** http://vocab.getty.edu/tgn/

**Scope for This Project:**
- Australian place names
- New South Wales localities
- Blue Mountains region
- Historic mining settlements
- Geographic features (valleys, ridges, creeks)

**Example Mappings:**

| Local Tag | TGN Place Name | TGN ID | URI | Coordinates |
|-----------|----------------|--------|-----|-------------|
| Blue Mountains | Blue Mountains (region) | 7001926 | http://vocab.getty.edu/tgn/7001926 | -33.7°, 150.3° |
| Katoomba | Katoomba (inhabited place) | 7001924 | http://vocab.getty.edu/tgn/7001924 | -33.7127°, 150.3119° |
| Jamison Valley | [To be mapped] | TBD | TBD | -33.733°, 150.367° |
| New South Wales | New South Wales (state) | 7001594 | http://vocab.getty.edu/tgn/7001594 | -32.0°, 147.0° |
| Sydney | Sydney (inhabited place) | 7004934 | http://vocab.getty.edu/tgn/7004934 | -33.8688°, 151.2093° |

**Hierarchical Structure Example:**

```text
World (facet)
└── Australia (nation)
    └── New South Wales (state)
        └── Blue Mountains (region)
            └── Katoomba (inhabited place)
```

**Query Example:**

```sparql
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX gvp: <http://vocab.getty.edu/ontology#>
PREFIX wgs84: <http://www.w3.org/2003/01/geo/wgs84_pos#>

SELECT ?place ?label ?lat ?long WHERE {
  ?place skos:inScheme tgn: ;
         skos:prefLabel ?label ;
         wgs84:lat ?lat ;
         wgs84:long ?long ;
         gvp:broaderExtended <http://vocab.getty.edu/tgn/7001594> .  # NSW
  FILTER (lang(?label) = "en")
  FILTER (regex(?label, "Blue Mountains", "i"))
}
```

**Integration Note:**

TGN is complementary to the Gazetteer of Australia. Use TGN for internationally recognised URIs and semantic web integration; use Gazetteer of Australia for detailed Australian place name data and coordinates.

---

## 2. Gazetteer of Australia

### Composite Gazetteer of Australia (Recommended)

**Purpose:** Authoritative Australian place names with coordinates and feature classification

**Provider:** Geoscience Australia

**Format:** GeoPackage (SQLite-based spatial database)

**File:** `gazetteers/composite-gazetteer/PlaceNames.gpkg`

**Records:** 289,560 place names (as of 2024-2025)

**Schema:**

```text
Fields:
- NAT_ID: National identifier (e.g., "NSW_12345")
- NAME: Place name
- FEATURE: Feature type (e.g., VALLEY, WATERCOURSE, LOCALITY)
- CATEGORY: Broader category (e.g., LANDFORM, WATERWAY, ADMINISTRATIVE AREA)
- GROUP: Highest-level group (e.g., LANDFORM, HYDROLOGY, ADMINISTRATION)
- LATITUDE: Decimal degrees (WGS84)
- LONGITUDE: Decimal degrees (WGS84)
- AUTHORITY: Supplying jurisdiction (e.g., NSW, VIC, SA)
- SUPPLY_DATE: Data currency (YYYY-MM-DD)
```

**Blue Mountains Coverage:**

| Name | Feature | Category | Group | Lat | Long |
|------|---------|----------|-------|-----|------|
| Jamison Valley | VALLEY | LANDFORM | LANDFORM | -33.7333 | 150.3667 |
| Jamison Creek | WATERCOURSE | WATERWAY | HYDROLOGY | -33.7183 | 150.3581 |
| Katoomba | LOCALITY | ADMINISTRATIVE AREA | ADMINISTRATION | -33.7127 | 150.3119 |
| Katoomba | POPULATION CENTRE | POPULATED PLACE | POPULATED PLACE | -33.7127 | 150.3119 |
| Jamisons Lookout | LOOKOUT | LANDMARK | LANDMARK | -33.7169 | 150.3783 |

**Usage Example:**

```python
import sqlite3

def lookup_gazetteer(place_name, feature_type=None):
    """
    Look up place name in Composite Gazetteer.

    Parameters:
        place_name (str): Name to search for
        feature_type (str): Optional filter by FEATURE type

    Returns:
        list: Matching records with coordinates
    """
    conn = sqlite3.connect('gazetteers/composite-gazetteer/PlaceNames.gpkg')
    cursor = conn.cursor()

    query = """
        SELECT NAME, FEATURE, CATEGORY, LATITUDE, LONGITUDE,
               NAT_ID, AUTHORITY, SUPPLY_DATE
        FROM PlaceNames
        WHERE NAME = ? OR NAME LIKE ?
    """
    params = [place_name, f"%{place_name}%"]

    if feature_type:
        query += " AND FEATURE = ?"
        params.append(feature_type)

    query += " ORDER BY AUTHORITY='NSW' DESC, CATEGORY"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results

# Example
locations = lookup_gazetteer("Jamison Valley")
for name, feature, category, lat, lon, nat_id, authority, date in locations:
    print(f"{name} ({feature}): {lat}, {lon} [{nat_id}]")
```

**Integration with Metadata:**

```json
{
  "location": {
    "name": "Jamison Valley",
    "tgn_uri": "http://vocab.getty.edu/tgn/[TBD]",
    "gazetteer_id": "NSW_12345",
    "coordinates": {
      "latitude": -33.7333,
      "longitude": 150.3667,
      "datum": "WGS84"
    },
    "feature": {
      "type": "VALLEY",
      "category": "LANDFORM",
      "group": "LANDFORM"
    },
    "authority": "NSW",
    "updated": "2024-01-18"
  }
}
```

**Export to GeoJSON:**

```python
import json

def export_locations_geojson(place_names, output_file):
    """
    Export gazetteer matches to GeoJSON for mapping.

    Parameters:
        place_names (list): List of place names to include
        output_file (str): Path to output GeoJSON file
    """
    features = []

    for place_name in place_names:
        results = lookup_gazetteer(place_name)
        for name, feature, category, lat, lon, nat_id, authority, date in results:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]  # GeoJSON: lon, lat order
                },
                "properties": {
                    "name": name,
                    "feature_type": feature,
                    "category": category,
                    "nat_id": nat_id,
                    "authority": authority,
                    "source": "Composite Gazetteer of Australia"
                }
            })

    geojson = {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}
        },
        "features": features
    }

    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)

# Example: Export Blue Mountains locations
places = ["Jamison Valley", "Katoomba", "Ruined Castle Creek"]
export_locations_geojson(places, "data/blue_mountains_locations.geojson")
```

**See Also:** `docs/gazetteer-comparison.md` for detailed comparison with Gazetteer of Australia 2012

---

## 3. Research Vocabularies Australia (RVA)

**Purpose:** Australian platform for publishing, discovering, and reusing research vocabularies

**Provider:** Australian Research Data Commons (ARDC)

**URL:** https://vocabs.ardc.edu.au/

**Project Status:** Planned for Phase 6 (Vocabulary Publishing)

**Publication Format:** SKOS (Simple Knowledge Organisation System) in RDF/XML or Turtle

### Blue Mountains Controlled Vocabulary Structure

**Concept Scheme:**

```turtle
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix bluemtn: <http://bluemountains.example.org/vocab/> .

bluemtn:conceptScheme
  a skos:ConceptScheme ;
  dcterms:title "Blue Mountains Shale Mining Communities Vocabulary"@en ;
  dcterms:description "Controlled vocabulary for historical sources related to Blue Mountains shale mining settlements (1880-1914)"@en ;
  dcterms:creator "Blue Mountains Shale Mining Communities Project" ;
  dcterms:created "2025-10-09"^^xsd:date ;
  dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
  skos:hasTopConcept bluemtn:mining, bluemtn:places, bluemtn:people, bluemtn:events .
```

**Example Concept (Mining):**

```turtle
bluemtn:mining
  a skos:Concept ;
  skos:inScheme bluemtn:conceptScheme ;
  skos:prefLabel "Mining"@en ;
  skos:altLabel "Mine"@en, "Shale mining"@en ;
  skos:definition "Activities related to extracting shale ore from the earth in the Jamison Valley region, 1880-1914"@en ;
  skos:scopeNote "Use for articles discussing mining operations, techniques, labour, and production. See also 'Miners' for people and 'Shale' for the material."@en ;
  skos:broader bluemtn:industry ;
  skos:narrower bluemtn:shale-extraction, bluemtn:kerosene-production ;
  skos:related bluemtn:miners, bluemtn:labour, bluemtn:accidents ;
  skos:exactMatch <http://vocab.getty.edu/aat/300053857> ;
  dcterms:created "2025-10-09"^^xsd:date .
```

**Hierarchical Relationships:**

```text
Top Concepts:
├── Mining
│   ├── Shale extraction
│   ├── Kerosene production
│   └── Mine closures
├── Places
│   ├── Blue Mountains
│   ├── Katoomba
│   ├── Jamison Valley
│   └── Ruined Castle
├── People
│   ├── Miners
│   ├── Families
│   ├── Women
│   └── Children
└── Events
    ├── Accidents
    ├── Court cases
    ├── Strikes
    └── Community gatherings
```

**Mapping Relationships (SKOS):**

| Relationship | Usage | Example |
|--------------|-------|---------|
| `skos:exactMatch` | Identical concepts | `bluemtn:mining` → `aat:300053857` |
| `skos:closeMatch` | Very similar concepts | `bluemtn:court-case` → `aat:300417384` |
| `skos:broadMatch` | Broader concept | `bluemtn:dwelling` → `aat:300004037` |
| `skos:narrowMatch` | Narrower concept | `bluemtn:shale` → `aat:300011791` |
| `skos:relatedMatch` | Related but not hierarchical | `bluemtn:mining` → `bluemtn:miners` |

**Publication Workflow:**

1. **Export from Zotero:** Extract rationalised tags
2. **Build Hierarchy:** Define broader/narrower relationships
3. **Map to Standards:** Link to Getty AAT/TGN URIs
4. **Encode in SKOS:** Generate RDF/XML or Turtle file
5. **Validate:** Use SKOS validator (http://labs.sparna.fr/skos-testing-tool/)
6. **Publish to RVA:** Submit via RVA platform
7. **Assign PID:** Receive persistent identifier (Handle or DOI)

**Python Tools:**

```python
from rdflib import Graph, Namespace, Literal, URF
from rdflib.namespace import SKOS, DCTERMS, XSD

def create_skos_concept(uri, pref_label, definition, broader=None, aat_match=None):
    """
    Create a SKOS concept for the Blue Mountains vocabulary.

    Parameters:
        uri (str): Concept URI
        pref_label (str): Preferred label (English)
        definition (str): Concept definition
        broader (str): URI of broader concept (optional)
        aat_match (str): Getty AAT URI for exact match (optional)

    Returns:
        rdflib.Graph: RDF graph with concept
    """
    g = Graph()
    BLUEMTN = Namespace("http://bluemountains.example.org/vocab/")

    concept = URIRef(uri)
    g.add((concept, RDF.type, SKOS.Concept))
    g.add((concept, SKOS.prefLabel, Literal(pref_label, lang="en")))
    g.add((concept, SKOS.definition, Literal(definition, lang="en")))
    g.add((concept, SKOS.inScheme, BLUEMTN.conceptScheme))

    if broader:
        g.add((concept, SKOS.broader, URIRef(broader)))

    if aat_match:
        g.add((concept, SKOS.exactMatch, URIRef(aat_match)))

    return g

# Example usage
mining_concept = create_skos_concept(
    uri="http://bluemountains.example.org/vocab/mining",
    pref_label="Mining",
    definition="Activities related to extracting shale ore",
    broader="http://bluemountains.example.org/vocab/industry",
    aat_match="http://vocab.getty.edu/aat/300053857"
)

# Serialise to Turtle
print(mining_concept.serialize(format="turtle"))
```

---

## 4. Dublin Core Metadata

**Purpose:** Item-level metadata for Omeka Classic publications

**Namespace:** http://purl.org/dc/terms/

**Specification:** Dublin Core Metadata Initiative (DCMI)

**Application:** Phase 4 (Omeka Classic Publication)

### Dublin Core Elements Used

| Element | Usage | Example |
|---------|-------|---------|
| `dcterms:title` | Item title (article headline) | "The Ruined Castle Mines" |
| `dcterms:creator` | Author or publisher | "Sydney Morning Herald" |
| `dcterms:date` | Publication date (ISO 8601) | "1895-06-12" |
| `dcterms:description` | Abstract or summary | "Report on mining operations..." |
| `dcterms:subject` | Tags (controlled vocabulary) | "Mining", "Katoomba" |
| `dcterms:spatial` | Geographic coverage | "Jamison Valley, NSW" |
| `dcterms:temporal` | Time period covered | "1880-1914" |
| `dcterms:type` | Resource type | "Text", "Image" |
| `dcterms:format` | File format | "application/pdf", "image/jpeg" |
| `dcterms:identifier` | Unique identifier | "Zotero:ABC123XY" |
| `dcterms:source` | Original source publication | "Sydney Morning Herald, p. 5" |
| `dcterms:rights` | Rights statement | "Public Domain" or license URI |
| `dcterms:isPartOf` | Collection membership | "Blue Mountains Collection" |

### Omeka Metadata Example

```xml
<dublin_core>
  <dcterms:title>Accident at the Ruined Castle Mine</dcterms:title>
  <dcterms:creator>Sydney Morning Herald</dcterms:creator>
  <dcterms:date>1895-06-12</dcterms:date>
  <dcterms:description>Newspaper report of a mining accident at the Ruined Castle shale mine in which two miners were injured.</dcterms:description>
  <dcterms:subject>Mining</dcterms:subject>
  <dcterms:subject>Accident</dcterms:subject>
  <dcterms:subject>Ruined Castle</dcterms:subject>
  <dcterms:spatial>
    <location>
      <name>Jamison Valley</name>
      <coordinates>-33.7333, 150.3667</coordinates>
      <gazetteer_id>NSW_12345</gazetteer_id>
    </location>
  </dcterms:spatial>
  <dcterms:temporal>1895</dcterms:temporal>
  <dcterms:type>Text</dcterms:type>
  <dcterms:format>application/pdf</dcterms:format>
  <dcterms:identifier>urn:zotero:2258643:ABC123XY</dcterms:identifier>
  <dcterms:source>Sydney Morning Herald, 12 June 1895, p. 5</dcterms:source>
  <dcterms:rights>http://rightsstatements.org/vocab/NoC-US/1.0/</dcterms:rights>
  <dcterms:isPartOf>Blue Mountains Shale Mining Communities Collection</dcterms:isPartOf>
</dublin_core>
```

**Integration with Vocabularies:**

- `dcterms:subject` values drawn from Blue Mountains controlled vocabulary (published to RVA)
- `dcterms:spatial` linked to Gazetteer of Australia NAT_ID
- Geographic coordinates in WGS84 decimal degrees
- `dcterms:subject` URIs point to SKOS concepts when available

---

## 5. Vocabulary Maintenance

### Versioning

All vocabularies are versioned using semantic versioning:

- **MAJOR:** Breaking changes (concept removal, URI changes)
- **MINOR:** Non-breaking additions (new concepts, mappings)
- **PATCH:** Corrections (typos, definition clarifications)

**Current Version:** 0.1.0 (initial draft)

### Change Log

Vocabulary changes documented in `CHANGELOG.md` under "Vocabulary" section

**Example Entry:**

```markdown
## [0.2.0] - 2025-11-15

### Vocabulary Changes

#### Added
- 15 new concepts for labour relations
- Getty AAT mappings for 42 concepts
- Hierarchical relationships for place names

#### Changed
- Refined definition of "Mining" concept
- Updated "Court" to "Court cases" (preferred label)

#### Deprecated
- "Mine" merged into "Mining" (use skos:altLabel)
```

### Quality Assurance

**Validation Tools:**

1. **SKOS Validator:** http://labs.sparna.fr/skos-testing-tool/
2. **RDF Validator:** https://www.w3.org/RDF/Validator/
3. **Local Testing:** `rdflib` (Python), `rapper` (command-line)

**Quality Checks:**

- No orphan concepts (all have broader or topConcept)
- Unique prefLabels within scheme
- All concepts have definitions
- External mappings resolve (HTTP 200)
- Consistent language tags (@en)
- Valid URIs (no broken links)

---

## 6. Future Enhancements

**Phase 2-6 Planned Additions:**

1. **Temporal Concepts:** Decades, periods, historical events
2. **Materials:** Extended material culture vocabulary
3. **Archaeological Features:** Site types, feature classifications
4. **Social Relations:** Family, community, migration
5. **Economic Activities:** Beyond mining (farming, forestry, tourism)

**Integration with External Vocabularies:**

- **Library of Congress Subject Headings (LCSH):** For library cataloguing
- **Australian Pictorial Thesaurus (APT):** For visual materials
- **Heritage Collections Council Thesaurus:** For heritage objects

---

## References

- **Getty Vocabularies:** http://www.getty.edu/research/tools/vocabularies/
- **SKOS Specification:** https://www.w3.org/TR/skos-reference/
- **Research Vocabularies Australia:** https://vocabs.ardc.edu.au/
- **Gazetteer of Australia:** https://www.ga.gov.au/scientific-topics/geographic-information/placenames
- **Dublin Core:** https://www.dublincore.org/specifications/dublin-core/
- **RightsStatements.org:** https://rightsstatements.org/

---

*Blue Mountains Shale Mining Communities Digital Collection Software*
*ARC Linkage Project LP190100900*
