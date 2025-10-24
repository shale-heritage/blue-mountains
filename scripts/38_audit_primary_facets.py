#!/usr/bin/env python3
"""
Script 38: Audit Primary Facet Structure

Analyses the current primary facet hierarchy and generates a comprehensive
audit report identifying issues and proposing corrections to align with
Getty AAT 7-facet structure.

PROBLEM:
- 82 separate root-level "primary" trees (should be 7 Getty AAT facets)
- 697 intermediate facets appearing as roots due to missing Getty parent connections
- All tags should be in primary hierarchy, with thematic providing alternative views

SOLUTION:
- Add 7 Getty AAT root entries
- Connect orphaned intermediate facets to proper Getty parents
- Maintain poly-hierarchy (keep thematic parents alongside new primary parents)

TARGET STRUCTURE (7 Getty AAT Primary Facets):
1. Agents (People, Organizations, Animals)
2. Places (Towns, Natural features, Mining districts)
3. Built Environment (Buildings, Infrastructure)
4. Activities (Sports, Work, Cultural activities)
5. Events (Sporting events, Historical events, Legal events)
6. Associated Concepts (Social behaviours, Cultural concepts, Legal concepts)
7. Materials (Consumable materials, Construction materials)

Author: Claude Code
Date: 2025-10-24
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


# Getty AAT 7 Primary Facets
GETTY_FACETS = [
    'Agents',
    'Places',
    'Built Environment',
    'Activities',
    'Events',
    'Associated Concepts',
    'Materials',
]


def load_csv_data(csv_path: Path) -> List[Dict]:
    """Load consolidated CSV into list of dicts."""
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_parent(notes: str) -> Tuple[str, bool]:
    """
    Extract parent name from notes field.

    Returns:
        (parent_name, is_thematic)
    """
    if not notes or 'parent=' not in notes:
        return None, False

    # Special markers for roots
    if 'parent=(thematic grouping)' in notes:
        return None, True
    if 'parent=(Getty AAT primary facet)' in notes:
        return None, False

    # Extract parent name
    parent = notes.replace('parent=', '').split(' -')[0].split(' (')[0].strip()
    is_thematic = '- THEMATIC' in notes or 'thematic grouping' in notes.lower()

    return parent, is_thematic


def build_hierarchy_maps(rows: List[Dict]) -> Tuple[Dict, Dict, Set, Set]:
    """
    Build parent-child mappings and identify roots.

    Returns:
        (primary_children, thematic_children, primary_roots, all_tags)
    """
    primary_children = defaultdict(set)
    thematic_children = defaultdict(set)
    all_tags = set()
    thematic_markers = set()

    for row in rows:
        if row['action'] == 'hierarchy':
            tag = row['old_tag']
            all_tags.add(tag)
            parent, is_thematic = parse_parent(row['notes'])

            if parent:
                if is_thematic:
                    thematic_children[parent].add(tag)
                    thematic_markers.add(tag)
                else:
                    primary_children[parent].add(tag)

    # Identify primary roots (parents that are not children in primary hierarchy)
    all_primary_parents = set(primary_children.keys())
    primary_roots = all_primary_parents - all_tags

    # Also include tags that ARE in all_tags but only appear as thematic children
    # (These are tags with ONLY primary parents pointing to them, making them intermediate roots)
    for tag in all_tags:
        # If tag is a parent in primary hierarchy but not a child in primary hierarchy
        if tag in primary_children and tag not in {child for children in primary_children.values() for child in children}:
            # Unless it's a Getty facet marker
            if not any(marker in str(tag) for marker in ['(new top-level facet)', '(conceptual facet)', '(existing facet)']):
                primary_roots.add(tag)

    return primary_children, thematic_children, primary_roots, all_tags


def categorise_by_getty_facet(tag: str, primary_children: Dict, all_tags: Set) -> Tuple[str, str, str]:
    """
    Suggest which Getty facet this orphaned root should belong to.

    Returns:
        (getty_facet, intermediate_parent, confidence)
    """
    tag_lower = tag.lower()

    # AGENTS patterns
    if any(word in tag_lower for word in ['club', 'society', 'association', 'committee', 'organization', 'organisation', 'company', 'council', 'lodge', 'band', 'choir', 'group']):
        return 'Agents', 'Organizations', 'HIGH'
    if any(word in tag_lower for word in ['occupation', 'worker', 'employee', 'professional', 'official', 'merchant', 'hotellier', 'publican', 'clergyman', 'police', 'coroner']):
        return 'Agents', 'People > Occupations', 'HIGH'
    if any(word in tag_lower for word in ['people', 'demographic', 'ethnic', 'racial', 'women', 'men', 'children', 'families']):
        return 'Agents', 'People > Demographic groups', 'HIGH'
    if 'animal' in tag_lower:
        return 'Agents', 'Animals', 'HIGH'

    # PLACES patterns
    if any(word in tag_lower for word in ['town', 'village', 'suburb', 'locality', 'carrington', 'katoomba', 'megalong', 'leura', 'mount victoria', 'wentworth falls', 'hartley', 'lithgow']):
        return 'Places', 'Towns', 'HIGH'
    if any(word in tag_lower for word in ['valley', 'gully', 'gulley', 'mountain', 'falls', 'creek', 'river', 'cave', 'feature']):
        return 'Places', 'Natural features', 'HIGH'
    if any(word in tag_lower for word in ['mining district', 'mining settlement', 'reserve']):
        return 'Places', 'Places', 'MEDIUM'

    # BUILT ENVIRONMENT patterns
    if any(word in tag_lower for word in ['building', 'hall', 'church', 'chapel', 'temple', 'hotel', 'house', 'cottage', 'dwelling', 'stable']):
        return 'Built Environment', 'Built Environment', 'HIGH'
    if any(word in tag_lower for word in ['court', 'council building', 'police station', 'post office', 'government building']):
        return 'Built Environment', 'Government buildings', 'HIGH'
    if any(word in tag_lower for word in ['railway', 'railroad', 'station', 'track', 'infrastructure']):
        return 'Built Environment', 'Transport infrastructure', 'HIGH'
    if any(word in tag_lower for word in ['school', 'education']):
        return 'Built Environment', 'Educational buildings', 'MEDIUM'

    # ACTIVITIES patterns
    if any(word in tag_lower for word in ['sport', 'cricket', 'football', 'tennis', 'athletics', 'riding', 'racing']):
        return 'Activities', 'Sports', 'HIGH'
    if any(word in tag_lower for word in ['mining', 'work', 'labour', 'trade', 'commerce']):
        return 'Activities', 'Economic activities', 'MEDIUM'
    if 'activity' in tag_lower or 'activities' in tag_lower:
        return 'Activities', 'Activities', 'MEDIUM'

    # EVENTS patterns
    if any(word in tag_lower for word in ['event', 'accident', 'disaster', 'ceremony', 'celebration']):
        return 'Events', 'Events', 'HIGH'
    if 'historical period' in tag_lower or 'world war' in tag_lower:
        return 'Events', 'Historical events', 'HIGH'

    # ASSOCIATED CONCEPTS patterns
    if any(word in tag_lower for word in ['alcohol', 'drinking', 'temperance', 'consumption', 'behaviour', 'behavior']):
        return 'Associated Concepts', 'Social behaviours', 'HIGH'
    if any(word in tag_lower for word in ['crime', 'offence', 'offense', 'legal', 'law', 'justice']):
        return 'Associated Concepts', 'Legal concepts', 'HIGH'
    if any(word in tag_lower for word in ['health', 'disease', 'illness', 'injury', 'medical', 'condition']):
        return 'Associated Concepts', 'Health concepts', 'HIGH'
    if any(word in tag_lower for word in ['cultural', 'identity', 'heritage', 'ethnic']):
        return 'Associated Concepts', 'Cultural concepts', 'HIGH'
    if any(word in tag_lower for word in ['environment', 'weather', 'climate']):
        return 'Associated Concepts', 'Environmental concepts', 'HIGH'
    if 'concept' in tag_lower or 'associated' in tag_lower:
        return 'Associated Concepts', 'Associated Concepts', 'MEDIUM'

    # MATERIALS patterns
    if any(word in tag_lower for word in ['material', 'beverage', 'food', 'drink', 'spirit', 'beer', 'wine', 'alcohol']):
        return 'Materials', 'Consumable materials', 'HIGH'
    if any(word in tag_lower for word in ['coal', 'shale', 'timber', 'stone', 'metal']):
        return 'Materials', 'Construction materials', 'MEDIUM'

    # Default to Associated Concepts with LOW confidence
    return 'Associated Concepts', 'Associated Concepts', 'LOW'


def generate_audit_report(csv_path: Path, output_path: Path):
    """Generate comprehensive audit report."""

    print("=" * 80)
    print("PRIMARY FACET STRUCTURE AUDIT")
    print("=" * 80)
    print()

    # Load data
    print("Loading data from tag_map_consolidated.csv...")
    rows = load_csv_data(csv_path)
    print(f"  Loaded {len(rows)} rows")
    print()

    # Build hierarchy maps
    print("Building hierarchy maps...")
    primary_children, thematic_children, primary_roots, all_tags = build_hierarchy_maps(rows)
    print(f"  Primary parents: {len(primary_children)}")
    print(f"  Thematic parents: {len(thematic_children)}")
    print(f"  Primary roots (orphaned): {len(primary_roots)}")
    print(f"  Total unique tags: {len(all_tags)}")
    print()

    # Categorize orphaned roots
    print("Categorising orphaned roots by Getty facet...")
    categorised = defaultdict(list)
    for root in sorted(primary_roots):
        # Skip special markers
        if root in ['(conceptual facet)', '(new top-level facet)', '(place type)', '(thematic facet)']:
            continue
        # Skip Getty facets themselves
        if root in GETTY_FACETS:
            continue
        # Skip if already has Getty parent marker
        # Check if this root has a parent entry
        has_getty_parent = False
        for row in rows:
            if row['old_tag'] == root and '(Getty AAT primary facet)' in row['notes']:
                has_getty_parent = True
                break
        if has_getty_parent:
            continue

        getty_facet, intermediate, confidence = categorise_by_getty_facet(root, primary_children, all_tags)
        categorised[getty_facet].append((root, intermediate, confidence))

    print(f"  Categorised {sum(len(v) for v in categorised.values())} orphaned roots")
    print()

    # Write report
    print(f"Writing audit report to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Primary Facet Structure Audit Report\n\n")
        f.write(f"**Generated:** 2025-10-24\n")
        f.write(f"**Source:** {csv_path}\n\n")

        f.write("## Problem Summary\n\n")
        f.write(f"- **Current primary root trees:** {len(primary_roots)} (including special markers)\n")
        f.write(f"- **Target primary root trees:** 7 (Getty AAT facets)\n")
        f.write(f"- **Orphaned roots requiring Getty parent:** {sum(len(v) for v in categorised.values())}\n\n")

        f.write("## Section A: Add 7 Getty AAT Root Entries\n\n")
        f.write("These entries create the top-level Getty AAT primary facets.\n\n")
        f.write("```csv\n")
        for facet in GETTY_FACETS:
            f.write(f"{facet},{facet},hierarchy,parent=(Getty AAT primary facet)\n")
        f.write("```\n\n")
        f.write("**USER ACTION:** [APPROVE / REJECT]\n\n")
        f.write("---\n\n")

        f.write("## Section B: Connect Orphaned Roots to Getty Facets\n\n")
        f.write("Each orphaned root needs a parent connection to one of the 7 Getty facets.\n")
        f.write("Entries are grouped by Getty facet with confidence levels.\n\n")

        for getty_facet in GETTY_FACETS:
            if getty_facet not in categorised or len(categorised[getty_facet]) == 0:
                continue

            f.write(f"### {getty_facet}\n\n")

            # Group by confidence
            high_conf = [r for r in categorised[getty_facet] if r[2] == 'HIGH']
            medium_conf = [r for r in categorised[getty_facet] if r[2] == 'MEDIUM']
            low_conf = [r for r in categorised[getty_facet] if r[2] == 'LOW']

            for conf_level, conf_list in [('HIGH', high_conf), ('MEDIUM', medium_conf), ('LOW', low_conf)]:
                if not conf_list:
                    continue

                f.write(f"#### Confidence: {conf_level} ({len(conf_list)} tags)\n\n")

                for root, intermediate, confidence in sorted(conf_list):
                    f.write(f"**Tag:** `{root}`\n")
                    f.write(f"**Suggested parent path:** `{getty_facet} > {intermediate}`\n")

                    # Show current children if any
                    if root in primary_children:
                        children_count = len(primary_children[root])
                        sample_children = list(sorted(primary_children[root]))[:3]
                        f.write(f"**Current children:** {children_count} ")
                        f.write(f"(e.g., {', '.join(sample_children)})\n")

                    f.write(f"**USER ACTION:** [APPROVE / REJECT / EDIT: _______________]\n\n")

            f.write("---\n\n")

        f.write("## Section C: Review Statistics\n\n")
        f.write(f"- **Getty AAT roots to add:** 7\n")
        f.write(f"- **Orphaned roots to connect:** {sum(len(v) for v in categorised.values())}\n")
        f.write(f"- **Tags by confidence level:**\n")
        all_entries = [(r, c) for entries in categorised.values() for r, i, c in entries]
        high_count = len([e for e in all_entries if e[1] == 'HIGH'])
        medium_count = len([e for e in all_entries if e[1] == 'MEDIUM'])
        low_count = len([e for e in all_entries if e[1] == 'LOW'])
        f.write(f"  - HIGH: {high_count}\n")
        f.write(f"  - MEDIUM: {medium_count}\n")
        f.write(f"  - LOW: {low_count}\n\n")

        f.write("## Instructions\n\n")
        f.write("1. Review Section A and mark [APPROVE / REJECT]\n")
        f.write("2. Review each entry in Section B:\n")
        f.write("   - Mark [APPROVE] if suggested parent is correct\n")
        f.write("   - Mark [REJECT] if tag should not be connected\n")
        f.write("   - Mark [EDIT: new_parent_path] to specify different parent\n")
        f.write("3. Save this file with your annotations\n")
        f.write("4. Run script 39 to apply approved changes\n\n")

    print("✓ Audit report generated")
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print(f"1. Review the audit report: {output_path}")
    print(f"2. Mark each entry with [APPROVE / REJECT / EDIT: ...]")
    print(f"3. Save the annotated report")
    print(f"4. Run script 39 to apply approved changes")
    print()


def main():
    """Main execution."""
    csv_path = Path('data/tag_map_consolidated.csv')
    output_path = Path('reports/primary_facets_audit.md')

    if not csv_path.exists():
        print(f"ERROR: {csv_path} not found")
        return 1

    # Create reports directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_audit_report(csv_path, output_path)

    return 0


if __name__ == '__main__':
    main()
