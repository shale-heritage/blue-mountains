# Australian Gazetteer Comparison for Blue Mountains Project

**Date:** 2025-10-09
**Purpose:** Evaluate which Geoscience Australia gazetteer product best suits the Blue Mountains Shale Mining Communities project

---

## Executive Summary

**Recommendation:** Use the **Composite Gazetteer of Australia** as the primary gazetteer for this project.

**Reasons:**
1. More current data (2024-2025 vs 2012)
2. Modern, easy-to-query format (GeoPackage/SQLite)
3. Well-structured categorisation system
4. Better documentation through standardised Schema
5. Larger dataset with comprehensive coverage

**Supplementary Use:** Keep Gazetteer of Australia 2012 as a reference for historical place names or verification.

---

## Detailed Comparison

### 1. Composite Gazetteer of Australia

**Format:** GeoPackage (`.gpkg`) - SQLite-based spatial database

**File Location:** `gazetteers/composite-gazetteer/PlaceNames.gpkg`

**Metadata:**
- **Total Records:** 289,560 place names
- **Data Currency:** 2024-2025 (supply dates range from 2024-01-18 to 2025-05-13)
- **File Size:** ~57 MB (compressed, efficient)
- **Coordinate System:** WGS84 (EPSG:4326)

**Schema Structure:**
```text
Fields:
- id: Unique identifier (integer)
- geom: Point geometry (binary)
- NAT_ID: National identifier (e.g., "NSW_12345")
- AUTH_ID: Authority identifier
- NAME: Place name (up to 100 characters)
- FEATURE: Feature type (e.g., WATERCOURSE, LOCALITY, VALLEY)
- CATEGORY: Broader category (e.g., WATERWAY, ADMINISTRATIVE AREA, LANDFORM)
- GROUP: Highest-level group (e.g., HYDROLOGY, ADMINISTRATION, LANDFORM)
- LATITUDE: Decimal degrees (real)
- LONGITUDE: Decimal degrees (real)
- AUTHORITY: Supplying authority (e.g., NSW, VIC, SA)
- SUPPLY_DATE: Date data was supplied (datetime)
```

**Advantages:**
1. **Modern Format:** GeoPackage is an open OGC standard, widely supported by GIS software (QGIS, ArcGIS, Python libraries)
2. **Easy Querying:** SQLite backend allows direct SQL queries without specialised tools
3. **Hierarchical Organisation:** Three levels of classification (GROUP → CATEGORY → FEATURE)
4. **Provenance:** Supply dates track data currency
5. **Efficient Storage:** Spatial index (R-tree) for fast geographic queries
6. **Python Integration:** Can be queried directly using sqlite3, geopandas, or GDAL

**Relevant Blue Mountains Coverage (Sample):**
- Jamison Valley (VALLEY) - LANDFORM
- Jamison Creek (WATERCOURSE) - WATERWAY
- Katoomba (LOCALITY, POPULATION CENTRE) - Multiple entries
- Jamisons Lookout (LOOKOUT) - LANDMARK
- Multiple administrative parishes and survey markers

**Example Query:**
```python
import sqlite3
conn = sqlite3.connect('gazetteers/composite-gazetteer/PlaceNames.gpkg')
cursor = conn.cursor()
cursor.execute("""
    SELECT NAME, FEATURE, LATITUDE, LONGITUDE
    FROM PlaceNames
    WHERE NAME LIKE '%Jamison%'
""")
```

---

### 2. Gazetteer of Australia 2012

**Formats:** GML (Geography Markup Language), KML (Keyhole Markup Language), MDB (Microsoft Access Database)

**File Location:** `gazetteers/gazetter-of-australia/`

**Metadata:**
- **Data Vintage:** 2012 (12+ years old)
- **File Size:**
  - GML: ~10.8 million lines (very large XML file)
  - MDB: ~107 MB (Microsoft Access format)
  - KML: Available for Google Earth
- **Documentation:** PDF user guide included

**Schema Structure (from GML sample):**
```text
Fields:
- OBJECTID: Object identifier
- RECORD_ID: Record identifier (e.g., "NSW12345")
- NAME: Place name
- FEAT_CODE: Feature code (e.g., "PT" for point)
- CGDN: Commonwealth Gazetteer of Defence Names flag (Y/N)
- AUTHORITY_ID: Authority identifier
- CONCISE_GAZ: Concise Gazetteer flag (Y/N)
- LATITUDE: Decimal degrees
- lat_degrees/lat_minutes/lat_seconds: DMS components
- LONGITUDE: Decimal degrees
- long_degrees/long_minutes/long_seconds: DMS components
```

**Advantages:**
1. **Multiple Formats:** Choice of GML (interoperable), KML (Google Earth), MDB (legacy databases)
2. **DMS Coordinates:** Includes both decimal degrees and degrees-minutes-seconds
3. **Defence Names:** Flags Commonwealth Gazetteer of Defence Names entries
4. **Historical Reference:** Captures place names as of 2012

**Disadvantages:**
1. **Outdated:** 12+ year-old dataset, missing recent changes
2. **Format Challenges:**
   - GML: Extremely large XML file, slow to parse
   - MDB: Requires Microsoft Access or mdbtools, proprietary format
   - No native Python-friendly format
3. **Limited Categorisation:** Feature codes less descriptive than Composite Gazetteer
4. **No Supply Dates:** Cannot determine currency of individual records

**Relevant Blue Mountains Coverage (Sample):**
- RUINED CASTLE HILL
- RUINED CASTLE CREEK
- Ruined Castle Ridge
- Ruined Castle Gully
- Mount Jamison
- Katoomba (multiple entries)
- Megalong Public School
- Jamison Creek

---

## Comparison Matrix

| Criterion | Composite Gazetteer | Gazetteer 2012 | Winner |
|-----------|---------------------|----------------|--------|
| **Data Currency** | 2024-2025 | 2012 | Composite ✓ |
| **File Format** | GeoPackage (modern) | GML/KML/MDB (legacy) | Composite ✓ |
| **Ease of Query** | Direct SQL | XML parsing or MDB tools | Composite ✓ |
| **File Size** | 57 MB | 107+ MB | Composite ✓ |
| **Categorisation** | 3-level hierarchy | Feature codes | Composite ✓ |
| **Python Integration** | Excellent (sqlite3) | Complex (XML/MDB) | Composite ✓ |
| **Provenance** | Supply dates included | Not tracked | Composite ✓ |
| **DMS Coordinates** | Decimal only | Both decimal & DMS | Gazetteer 2012 |
| **Historical Coverage** | Current | 2012 snapshot | Depends on use case |
| **Project Coverage** | Comprehensive | Comprehensive | Tie |

**Overall Winner:** **Composite Gazetteer of Australia**

---

## Recommendation for Blue Mountains Project

### Primary Gazetteer: Composite Gazetteer of Australia

**Use for:**
1. **Location tagging** of newspaper articles and primary sources
2. **Coordinate lookup** for places mentioned in historical documents
3. **Hierarchical browsing** of geographic features (valleys, creeks, landmarks)
4. **Modern mapping** and visualisation of research data
5. **API integration** for automated place name resolution

**Implementation:**
```python
# Example: Resolve place name to coordinates
import sqlite3

def get_coordinates(place_name):
    """
    Look up coordinates for a place name in the Composite Gazetteer.

    Parameters:
        place_name (str): Name of place to look up

    Returns:
        list: List of matches with coordinates and feature types
    """
    conn = sqlite3.connect('gazetteers/composite-gazetteer/PlaceNames.gpkg')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT NAME, FEATURE, CATEGORY, LATITUDE, LONGITUDE, AUTHORITY
        FROM PlaceNames
        WHERE NAME = ? OR NAME LIKE ?
        ORDER BY
            CASE WHEN AUTHORITY = 'NSW' THEN 1 ELSE 2 END,
            CATEGORY
    """, (place_name, f"%{place_name}%"))

    results = cursor.fetchall()
    conn.close()

    return results

# Example usage:
locations = get_coordinates("Jamison Valley")
for name, feature, category, lat, lon, authority in locations:
    print(f"{name} ({feature}): {lat}, {lon} - {authority}")
```

### Secondary Reference: Gazetteer of Australia 2012

**Retain for:**
1. **Historical verification** - Some place names may have changed since 2012
2. **Cross-referencing** - Verify ambiguous or disputed locations
3. **Defence place names** - CGDN flag for Commonwealth Gazetteer of Defence Names
4. **Legacy compatibility** - If working with other 2012-era datasets

**Note:** The 2012 gazetteer contains some features not yet in the Composite Gazetteer, particularly for Ruined Castle-related features (RUINED CASTLE HILL, RUINED CASTLE CREEK, Ruined Castle Ridge, Ruined Castle Gully).

---

## Integration with Project Workflow

### Controlled Vocabulary Mapping

The Composite Gazetteer complements the existing vocabulary strategy:

1. **Getty TGN (Thesaurus of Geographic Names):** For international standard URIs
   - Example: Katoomba → `http://vocab.getty.edu/tgn/7001924`

2. **Composite Gazetteer:** For Australian-specific coordinates and local feature names
   - Example: Jamison Valley → `-33.7333, 150.3667` (VALLEY/LANDFORM)

3. **Cross-Referencing:** Use both for comprehensive geographic metadata
   ```yaml
   location:
     name: "Jamison Valley"
     tgn_uri: "http://vocab.getty.edu/tgn/[TO_BE_MAPPED]"
     gazetteer_id: "NSW_12345"
     coordinates: [-33.7333, 150.3667]
     feature_type: "VALLEY"
     authority: "NSW"
   ```

### Future Enhancements

1. **Custom Gazetteer Extension:** Add project-specific features not in either gazetteer
   - Shale mine sites (e.g., "Ruined Castle Shale Mine")
   - Historical settlement names from archival sources
   - Archaeological site locations (anonymised for protection)

2. **Temporal Gazetteer:** Track historical place name changes
   - Compare 2012 vs 2024 entries
   - Document name changes in historical period (1880-1914)

---

## Technical Specifications

### Accessing Composite Gazetteer in Python

```python
import sqlite3
import json

def query_gazetteer(bbox=None, feature_type=None, name_pattern=None):
    """
    Query the Composite Gazetteer with optional filters.

    Parameters:
        bbox (tuple): Bounding box (min_lon, min_lat, max_lon, max_lat)
        feature_type (str): Filter by FEATURE type
        name_pattern (str): SQL LIKE pattern for NAME field

    Returns:
        list: Matching records as dictionaries
    """
    conn = sqlite3.connect('gazetteers/composite-gazetteer/PlaceNames.gpkg')
    cursor = conn.cursor()

    query = "SELECT * FROM PlaceNames WHERE 1=1"
    params = []

    if bbox:
        min_lon, min_lat, max_lon, max_lat = bbox
        query += " AND LONGITUDE BETWEEN ? AND ? AND LATITUDE BETWEEN ? AND ?"
        params.extend([min_lon, max_lon, min_lat, max_lat])

    if feature_type:
        query += " AND FEATURE = ?"
        params.append(feature_type)

    if name_pattern:
        query += " AND NAME LIKE ?"
        params.append(name_pattern)

    cursor.execute(query, params)
    columns = [desc[0] for desc in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    conn.close()
    return results

# Example: Get all valleys in Blue Mountains region
blue_mountains_bbox = (150.0, -34.0, 151.0, -33.0)
valleys = query_gazetteer(
    bbox=blue_mountains_bbox,
    feature_type='VALLEY'
)
```

### GeoJSON Export

```python
def export_to_geojson(query_results, output_file):
    """
    Export gazetteer query results to GeoJSON format.

    Parameters:
        query_results (list): Results from query_gazetteer()
        output_file (str): Path to output GeoJSON file
    """
    features = []
    for record in query_results:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [record['LONGITUDE'], record['LATITUDE']]
            },
            "properties": {
                "name": record['NAME'],
                "feature": record['FEATURE'],
                "category": record['CATEGORY'],
                "authority": record['AUTHORITY'],
                "nat_id": record['NAT_ID']
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)
```

---

## Conclusion

The **Composite Gazetteer of Australia** is the recommended primary gazetteer for the Blue Mountains Shale Mining Communities project due to its:

- Modern, accessible format (GeoPackage)
- Current data (2024-2025)
- Excellent Python integration
- Comprehensive hierarchical organisation
- Efficient querying capabilities

The **Gazetteer of Australia 2012** should be retained as a supplementary reference for historical verification and cross-referencing, particularly for Ruined Castle-specific features.

This dual approach ensures both currency and historical depth in geographic metadata while maintaining technical accessibility for the project's digital humanities workflow.

---

## References

- **Composite Gazetteer of Australia:** Geoscience Australia, accessed October 2025
- **Gazetteer of Australia 2012:** Geoscience Australia, 2012 edition
- **OGC GeoPackage Specification:** https://www.geopackage.org/
- **Project Documentation:** `docs/vocabularies.md` for Getty TGN integration

---

*Prepared for the Blue Mountains Shale Mining Communities Digital Collection Project*
*ARC Linkage Project LP190100900*
