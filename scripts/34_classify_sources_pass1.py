#!/usr/bin/env python3
"""
Pass 1: Metadata-Based Source Classification

This script analyses Zotero library items and classifies them as primary or
secondary sources based on bibliographic metadata with high confidence.
Items that cannot be confidently classified from metadata alone are flagged
for Pass 2 (content analysis or manual review).

Classification Rules:

PRIMARY SOURCE (High Confidence):
- newspaperArticle (contemporary newspaper articles)
- map (historical maps from the period)
- letter (historical correspondence)
- archivalDocument (archival materials)
- Items with dates 1850-1930 AND item types suggesting contemporary records

SECONDARY SOURCE (High Confidence):
- dictionaryEntry (reference works)
- encyclopediaArticle (reference works)
- thesis (modern scholarly research)
- Items with dates post-1950 AND scholarly item types (journalArticle, book)

UNCERTAIN (Needs Pass 2):
- Items where metadata is ambiguous
- Historical books/reports that could be primary or secondary
- Journal articles without clear date indicators
- Items missing critical metadata

Output:
- reports/pass1_classification_report.md - Detailed classification report
- data/pass1_classifications.json - Machine-readable classifications

Author: Claude Code
Date: 2025-10-29
"""

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# Input and output files
INPUT_FILE = Path("data/zotero_full_export.json")
OUTPUT_REPORT = Path("reports/pass1_classification_report.md")
OUTPUT_DATA = Path("data/pass1_classifications.json")


def parse_year(date_str: str) -> int | None:
    """
    Extract year from a date string.

    Args:
        date_str: Date string from Zotero (various formats)

    Returns:
        Year as integer, or None if unable to parse
    """
    if not date_str:
        return None

    # Try to extract 4-digit year
    match = re.search(r'\b(1[789]\d{2}|20\d{2})\b', date_str)
    if match:
        return int(match.group(1))

    return None


def classify_item(item: Dict) -> Tuple[str, str, str]:
    """
    Classify a Zotero item as primary, secondary, or uncertain.

    Args:
        item: Item data from Zotero export

    Returns:
        Tuple of (classification, confidence, rationale)
        - classification: "primary", "secondary", or "uncertain"
        - confidence: "high", "medium", or "low"
        - rationale: Human-readable explanation
    """
    item_type = item.get("itemType", "")
    title = item.get("title", "")
    date = item.get("date", "")
    pub_title = item.get("publicationTitle", "")
    creators = item.get("creators", [])
    tags = item.get("tags", [])
    year = parse_year(date)

    # Check if already tagged
    has_primary_tag = "Primary source" in tags or "primary source" in tags
    has_secondary_tag = "Secondary source" in tags or "secondary source" in tags

    if has_primary_tag:
        return ("primary", "high", "Already tagged as 'Primary source'")
    if has_secondary_tag:
        return ("secondary", "high", "Already tagged as 'Secondary source'")

    # PRIMARY SOURCE classifications (high confidence)

    # Newspaper articles (contemporary reporting)
    if item_type == "newspaperArticle":
        # Additional check: if published in known primary source publications
        primary_publications = [
            "Lithgow Mercury",
            "Blue Mountains Echo",
            "Nepean Times",
            "Evening News",
            "Sydney Morning Herald",
            "Cumberland Argus"
        ]
        if any(pub in pub_title for pub in primary_publications):
            return ("primary", "high",
                    f"Contemporary newspaper article from {pub_title}")
        else:
            return ("primary", "high",
                    "Contemporary newspaper article (item type: newspaperArticle)")

    # Historical maps from the period
    if item_type == "map":
        if year and 1850 <= year <= 1930:
            return ("primary", "high",
                    f"Historical map from {year} (within study period)")
        else:
            return ("uncertain", "medium",
                    "Map with unclear date - needs review")

    # Letters (historical correspondence)
    if item_type == "letter":
        if year and 1850 <= year <= 1930:
            return ("primary", "high",
                    f"Historical letter from {year} (within study period)")
        else:
            return ("primary", "medium",
                    "Letter (likely primary source but date unclear)")

    # Archival documents
    if item_type == "archivalDocument":
        return ("primary", "high",
                "Archival document (item type indicates primary source)")

    # SECONDARY SOURCE classifications (high confidence)

    # Reference works
    if item_type in ["dictionaryEntry", "encyclopediaArticle"]:
        return ("secondary", "high",
                f"Reference work (item type: {item_type})")

    # Modern scholarly research
    if item_type == "thesis":
        return ("secondary", "high",
                "Academic thesis (modern scholarly research)")

    # Blog posts and web pages (modern content)
    if item_type in ["blogPost", "webpage"]:
        if year and year >= 1990:
            return ("secondary", "high",
                    f"Modern web content from {year}")
        else:
            return ("secondary", "medium",
                    "Web content (likely secondary source)")

    # Conference papers (modern scholarship)
    if item_type == "conferencePaper":
        return ("secondary", "high",
                "Conference paper (modern scholarly work)")

    # CONDITIONAL classifications based on date and type

    # Journal articles - date dependent
    if item_type == "journalArticle":
        if year:
            if 1850 <= year <= 1930:
                return ("primary", "medium",
                        f"Historical journal article from {year} (may be contemporary account)")
            elif year >= 1950:
                return ("secondary", "high",
                        f"Modern journal article from {year} (scholarly research)")
            else:
                return ("uncertain", "medium",
                        f"Journal article from {year} - ambiguous period")
        else:
            return ("uncertain", "low",
                    "Journal article with no date information")

    # Books - date and content dependent
    if item_type in ["book", "bookSection"]:
        if year:
            if 1850 <= year <= 1930:
                # Historical books from the period - could be primary accounts
                # or contemporary secondary works
                return ("uncertain", "medium",
                        f"Historical {item_type} from {year} - "
                        f"needs content analysis (could be contemporary account "
                        f"or reference work)")
            elif year >= 1950:
                return ("secondary", "high",
                        f"Modern {item_type} from {year} (retrospective analysis)")
            else:
                return ("uncertain", "medium",
                        f"{item_type} from {year} - ambiguous period")
        else:
            return ("uncertain", "low",
                    f"{item_type} with no date information")

    # Reports - context dependent
    if item_type == "report":
        if year:
            if 1850 <= year <= 1930:
                return ("primary", "medium",
                        f"Historical report from {year} (likely contemporary record)")
            elif year >= 1950:
                return ("secondary", "medium",
                        f"Modern report from {year} (likely research/analysis)")
            else:
                return ("uncertain", "medium",
                        f"Report from {year} - needs review")
        else:
            return ("uncertain", "low",
                    "Report with no date information")

    # Default: uncertain
    return ("uncertain", "low",
            f"Item type '{item_type}' requires content analysis or manual review")


def main():
    """Main execution function."""
    print("=" * 70)
    print("Pass 1: Metadata-Based Source Classification")
    print("=" * 70)
    print()

    # Load exported data
    print(f"Loading data from {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        export_data = json.load(f)

    items = export_data.get("items", [])
    print(f"Loaded {len(items)} items")
    print()

    # Classify all items
    print("Classifying items based on metadata...")
    classifications = {
        "primary_high": [],
        "primary_medium": [],
        "secondary_high": [],
        "secondary_medium": [],
        "uncertain_medium": [],
        "uncertain_low": []
    }

    stats = defaultdict(int)

    for item in items:
        classification, confidence, rationale = classify_item(item)

        # Create classification record
        record = {
            "key": item["key"],
            "itemType": item["itemType"],
            "title": item["title"],
            "date": item["date"],
            "publicationTitle": item["publicationTitle"],
            "currentTags": item["tags"],
            "classification": classification,
            "confidence": confidence,
            "rationale": rationale,
            "numAttachments": item["numAttachments"],
            "numNotes": item["numNotes"]
        }

        # Group by classification and confidence
        key = f"{classification}_{confidence}"
        if key in classifications:
            classifications[key].append(record)

        # Update statistics
        stats[classification] += 1
        stats[f"{classification}_{confidence}"] += 1

    print("Classification complete")
    print()

    # Generate report
    print(f"Generating report: {OUTPUT_REPORT}...")
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("# Pass 1 Source Classification Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Total items analysed:** {len(items)}\n\n")

        # Summary statistics
        f.write("## Summary Statistics\n\n")
        f.write(f"- **Primary sources (high confidence):** {stats['primary_high']}\n")
        f.write(f"- **Primary sources (medium confidence):** {stats['primary_medium']}\n")
        f.write(f"- **Secondary sources (high confidence):** {stats['secondary_high']}\n")
        f.write(f"- **Secondary sources (medium confidence):** {stats['secondary_medium']}\n")
        f.write(f"- **Uncertain (needs Pass 2):** "
                f"{stats['uncertain_medium'] + stats['uncertain_low']}\n\n")

        total_classified = stats['primary_high'] + stats['primary_medium'] + \
                          stats['secondary_high'] + stats['secondary_medium']
        total_uncertain = stats['uncertain_medium'] + stats['uncertain_low']

        f.write(f"**Classification coverage:** {total_classified}/{len(items)} "
                f"({100 * total_classified / len(items):.1f}%)\n\n")
        f.write(f"**Requiring Pass 2:** {total_uncertain}/{len(items)} "
                f"({100 * total_uncertain / len(items):.1f}%)\n\n")

        # Primary sources (high confidence)
        f.write("## Primary Sources (High Confidence)\n\n")
        f.write(f"**Count:** {stats['primary_high']}\n\n")
        f.write("These items can be confidently classified as primary sources "
                "based on metadata alone.\n\n")

        if classifications["primary_high"]:
            # Group by item type
            by_type = defaultdict(list)
            for item in classifications["primary_high"]:
                by_type[item["itemType"]].append(item)

            for item_type in sorted(by_type.keys()):
                items_list = by_type[item_type]
                f.write(f"### {item_type} ({len(items_list)} items)\n\n")

                for item in items_list[:10]:  # Show first 10 of each type
                    f.write(f"- **{item['title']}** ({item['date']})\n")
                    f.write(f"  - Rationale: {item['rationale']}\n")
                    if item['currentTags']:
                        f.write(f"  - Current tags: {', '.join(item['currentTags'][:5])}"
                                f"{'...' if len(item['currentTags']) > 5 else ''}\n")
                    f.write("\n")

                if len(items_list) > 10:
                    f.write(f"*...and {len(items_list) - 10} more items*\n\n")

        f.write("\n")

        # Secondary sources (high confidence)
        f.write("## Secondary Sources (High Confidence)\n\n")
        f.write(f"**Count:** {stats['secondary_high']}\n\n")
        f.write("These items can be confidently classified as secondary sources "
                "based on metadata alone.\n\n")

        if classifications["secondary_high"]:
            # Group by item type
            by_type = defaultdict(list)
            for item in classifications["secondary_high"]:
                by_type[item["itemType"]].append(item)

            for item_type in sorted(by_type.keys()):
                items_list = by_type[item_type]
                f.write(f"### {item_type} ({len(items_list)} items)\n\n")

                for item in items_list[:10]:  # Show first 10 of each type
                    f.write(f"- **{item['title']}** ({item['date']})\n")
                    f.write(f"  - Rationale: {item['rationale']}\n")
                    if item['currentTags']:
                        f.write(f"  - Current tags: {', '.join(item['currentTags'][:5])}"
                                f"{'...' if len(item['currentTags']) > 5 else ''}\n")
                    f.write("\n")

                if len(items_list) > 10:
                    f.write(f"*...and {len(items_list) - 10} more items*\n\n")

        f.write("\n")

        # Uncertain items (need Pass 2)
        f.write("## Uncertain Items (Require Pass 2 Analysis)\n\n")
        f.write(f"**Count:** {total_uncertain}\n\n")
        f.write("These items cannot be confidently classified from metadata alone. "
                "They require content analysis (if transcriptions available) or "
                "manual review.\n\n")

        # Combine uncertain items
        uncertain_items = (classifications["uncertain_medium"] +
                          classifications["uncertain_low"])

        if uncertain_items:
            # Group by item type
            by_type = defaultdict(list)
            for item in uncertain_items:
                by_type[item["itemType"]].append(item)

            for item_type in sorted(by_type.keys()):
                items_list = by_type[item_type]
                f.write(f"### {item_type} ({len(items_list)} items)\n\n")

                # Count how many have notes (for content analysis)
                with_notes = sum(1 for i in items_list if i["numNotes"] > 0)
                f.write(f"*{with_notes} items have notes available for content analysis*\n\n")

                for item in items_list[:5]:  # Show first 5 of each type
                    f.write(f"- **{item['title']}** ({item['date']})\n")
                    f.write(f"  - Rationale: {item['rationale']}\n")
                    f.write(f"  - Attachments: {item['numAttachments']}, "
                            f"Notes: {item['numNotes']}\n")
                    if item['currentTags']:
                        f.write(f"  - Current tags: {', '.join(item['currentTags'][:3])}"
                                f"{'...' if len(item['currentTags']) > 3 else ''}\n")
                    f.write("\n")

                if len(items_list) > 5:
                    f.write(f"*...and {len(items_list) - 5} more items*\n\n")

        f.write("\n")

        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("1. **Review and approve high-confidence classifications** "
                f"({total_classified} items)\n")
        f.write("   - If approved, these can be immediately tagged\n\n")
        f.write("2. **Proceed to Pass 2 analysis** "
                f"({total_uncertain} items)\n")
        f.write("   - Items with notes: Perform content analysis\n")
        f.write("   - Items without notes: Manual review or user judgement\n\n")

    print(f"Report saved: {OUTPUT_REPORT}")

    # Save machine-readable data
    print(f"Saving classifications to {OUTPUT_DATA}...")
    OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)

    output = {
        "generated": datetime.now().isoformat(),
        "totalItems": len(items),
        "statistics": dict(stats),
        "classifications": {
            "primary_high": classifications["primary_high"],
            "primary_medium": classifications["primary_medium"],
            "secondary_high": classifications["secondary_high"],
            "secondary_medium": classifications["secondary_medium"],
            "uncertain": uncertain_items
        }
    }

    with open(OUTPUT_DATA, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Data saved: {OUTPUT_DATA}")
    print()

    # Print summary
    print("=" * 70)
    print("Classification Summary")
    print("=" * 70)
    print(f"Total items: {len(items)}")
    print()
    print(f"Primary sources (high confidence):     {stats['primary_high']:3d}")
    print(f"Primary sources (medium confidence):   {stats['primary_medium']:3d}")
    print(f"Secondary sources (high confidence):   {stats['secondary_high']:3d}")
    print(f"Secondary sources (medium confidence): {stats['secondary_medium']:3d}")
    print(f"Uncertain (needs Pass 2):              {total_uncertain:3d}")
    print()
    print(f"Classification coverage: {total_classified}/{len(items)} "
          f"({100 * total_classified / len(items):.1f}%)")
    print()
    print("✓ Classification complete")
    print()
    print(f"Next steps:")
    print(f"1. Review the report: {OUTPUT_REPORT}")
    print(f"2. Approve or modify classifications")
    print(f"3. Proceed to Pass 2 for uncertain items")


if __name__ == "__main__":
    main()
