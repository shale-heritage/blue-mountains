#!/usr/bin/env python3
"""
Generate item tag application CSV for educational schools based on classification results.

This script reads the classification results and generates a CSV with instructions for:
1. Removing old unqualified tags
2. Adding new qualified tags based on building/organisation/both classifications
3. Fixing School of Arts misclassifications

Date: 2025-11-14
"""

import json
import csv
from pathlib import Path
from typing import List, Dict

# Paths
DATA_DIR = Path(__file__).parent.parent / "data"
ENTITY_DIR = DATA_DIR / "entity_classification"
OUTPUT_DIR = Path(__file__).parent.parent / "entity-tagging-system" / "outputs" / "educational-schools"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Classification decisions from analysis + user correction
CLASSIFICATIONS = {
    # Mention number: classification
    1: "building",
    2: "organisation",
    3: "building",
    4: "organisation",
    5: "both",
    6: "building",
    7: "both",
    8: "organisation",
    9: "organisation",
    10: "organisation",
    11: "organisation",
    12: "organisation",
    13: "organisation",
    14: "organisation",
    15: "school_of_arts",  # Misclassification
    16: "building",
    17: "both",
    18: "organisation",
    19: "organisation",
    20: "school_of_arts",  # Misclassification
    21: "school_of_arts",  # Misclassification
    22: "both",  # User correction: was "building"
    23: "both",
    # 24-35 are duplicates of 12-23 (case variants)
    24: "organisation",  # = 12
    25: "organisation",  # = 13
    26: "organisation",  # = 14
    27: "school_of_arts",  # = 15
    28: "building",  # = 16
    29: "both",  # = 17
    30: "organisation",  # = 18
    31: "organisation",  # = 19
    32: "school_of_arts",  # = 20
    33: "school_of_arts",  # = 21
    34: "both",  # = 22 (with correction)
    35: "both",  # = 23
}

def load_mentions() -> List[Dict]:
    """Load mentions from JSON file."""
    mentions_file = ENTITY_DIR / "educational-schools_mentions.json"
    with open(mentions_file) as f:
        return json.load(f)

def generate_tag_applications(mentions: List[Dict]) -> List[Dict]:
    """Generate tag application instructions based on classifications."""
    applications = []

    for i, mention in enumerate(mentions, 1):
        classification = CLASSIFICATIONS[i]
        entity_name = mention["entity_name"]
        item_title = mention["item_title"]
        url = mention["url"]
        context_snippet = mention["context"][:200].replace("\n", " ").strip() + "..."

        # Determine old and new tags
        old_tag = entity_name
        new_tags = []

        if classification == "school_of_arts":
            # This is a misclassification - should be School of Arts
            new_tags = ["School of Arts"]  # Or could be more specific if known
            action = "RETAG_SCHOOL_OF_ARTS"
        elif classification == "building":
            new_tags = [f"{entity_name} (building)"]
            action = "REPLACE"
        elif classification == "organisation":
            new_tags = [f"{entity_name} (organisation)"]
            action = "REPLACE"
        elif classification == "both":
            new_tags = [f"{entity_name} (building)", f"{entity_name} (organisation)"]
            action = "REPLACE_WITH_BOTH"

        applications.append({
            "mention_id": i,
            "item_title": item_title,
            "item_url": url,
            "action": action,
            "old_tag": old_tag,
            "new_tags": " | ".join(new_tags),
            "classification": classification,
            "context_snippet": context_snippet,
            "notes": f"Mention {i}: {entity_name}"
        })

    return applications

def remove_duplicates(applications: List[Dict]) -> List[Dict]:
    """
    Remove duplicate tag applications for the same item.

    Some items are tagged with both "School" and "school" (case variants).
    Keep only unique item_title + action combinations.
    """
    seen = set()
    unique = []

    for app in applications:
        # Create unique key: item title + old tag + new tags
        key = (app["item_title"], app["old_tag"].lower(), app["new_tags"].lower())

        if key not in seen:
            seen.add(key)
            unique.append(app)
        else:
            # Mark as duplicate in notes
            app["notes"] += " [DUPLICATE - case variant]"

    removed = len(applications) - len(unique)
    print(f"✓ Removed {removed} duplicate applications (case-variant tags)")

    return unique

def write_csv(filepath: Path, applications: List[Dict]) -> None:
    """Write applications to CSV file."""
    fieldnames = [
        "mention_id",
        "item_title",
        "item_url",
        "action",
        "old_tag",
        "new_tags",
        "classification",
        "context_snippet",
        "notes"
    ]

    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(applications)

def main():
    """Main execution."""
    print("Educational Schools Tag Application Generator")
    print("=" * 60)

    # Load mentions
    print("\n1. Loading mentions...")
    mentions = load_mentions()
    print(f"   Loaded {len(mentions)} mentions")

    # Generate applications
    print("\n2. Generating tag applications...")
    applications = generate_tag_applications(mentions)
    print(f"   Generated {len(applications)} initial applications")

    # Remove duplicates
    print("\n3. Removing duplicate applications...")
    applications = remove_duplicates(applications)
    print(f"   Final count: {len(applications)} unique applications")

    # Summary statistics
    action_counts = {}
    for app in applications:
        action = app["action"]
        action_counts[action] = action_counts.get(action, 0) + 1

    print("\n4. Summary by action:")
    for action, count in sorted(action_counts.items()):
        print(f"   {action}: {count}")

    # Write to CSV
    output_file = OUTPUT_DIR / "item_tag_application.csv"
    print(f"\n5. Writing to: {output_file}")
    write_csv(output_file, applications)

    print("\n✅ Tag application CSV generated!")
    print(f"\nTotal applications: {len(applications)}")
    print(f"Output file: {output_file}")

    print("\nNext steps:")
    print("  1. Review CSV for accuracy")
    print("  2. Apply tags to Zotero library")
    print("  3. Update consolidation decisions log")

if __name__ == "__main__":
    main()
