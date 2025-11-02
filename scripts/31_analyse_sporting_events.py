#!/usr/bin/env python3
"""
Sporting Events Context Analysis and Reclassification Review
==============================================================

Extracts text contexts for sporting-related tags to determine whether they
represent:
- Specific events (stays in Events facet)
- Ongoing activities/sports (→ Activities > Recreation activities)
- Organisations (→ Agents > Organizations > Sports clubs)

Generates a human-readable review report with recommendations.

Author: Claude Code
Date: 2025-11-01
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402

from pyzotero import zotero


class MLStripper(HTMLParser):
    """Simple HTML tag stripper."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_data(self):
        return ''.join(self.text)


def strip_html(html):
    """Remove HTML tags from text."""
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()


def connect_to_zotero():
    """Connect to Zotero."""
    zot = zotero.Zotero(
        config.ZOTERO_GROUP_ID,
        config.ZOTERO_LIBRARY_TYPE,
        config.ZOTERO_API_KEY_READONLY
    )
    return zot


def extract_sport_context(text, sport_keywords):
    """
    Extract context around sporting keywords.

    Returns first 300 chars or context around first match.
    """
    if not text.strip():
        return '[No text content available]'

    # Try to find sport-specific keywords
    for keyword in sport_keywords:
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\w*', re.IGNORECASE)
        match = pattern.search(text)

        if match:
            start = match.start()
            end = match.end()

            # Extract 150 chars before and after
            context_start = max(0, start - 150)
            context_end = min(len(text), end + 150)

            before = text[context_start:start]
            term = text[start:end]
            after = text[end:context_end]

            # Clean whitespace
            before = ' '.join(before.split())
            after = ' '.join(after.split())

            return f"...{before} **{term}** {after}..."

    # No keyword match, just return first 300 chars
    excerpt = text[:300].strip()
    if len(text) > 300:
        excerpt += '...'

    return excerpt if excerpt else '[No text content available]'


def get_sport_keywords(tag):
    """Get relevant keywords for each sport tag."""
    tag_lower = tag.lower()

    keywords = []

    if 'cricket' in tag_lower:
        keywords = ['cricket', 'wicket', 'bat', 'bowl', 'innings', 'match', 'game']
    elif 'football' in tag_lower:
        keywords = ['football', 'goal', 'match', 'game', 'team', 'play']
    elif 'rugby' in tag_lower:
        keywords = ['rugby', 'try', 'scrum', 'match', 'game']
    elif 'tennis' in tag_lower:
        keywords = ['tennis', 'court', 'match', 'game', 'set']
    elif 'shooting' in tag_lower or 'rifle' in tag_lower:
        keywords = ['shoot', 'rifle', 'target', 'competition', 'match', 'score']
    elif 'billiard' in tag_lower:
        keywords = ['billiard', 'table', 'game', 'play']
    elif 'athletic' in tag_lower:
        keywords = ['athletic', 'sport', 'race', 'competition', 'carnival']
    elif 'horse race' in tag_lower or 'equestrian' in tag_lower:
        keywords = ['race', 'horse', 'racing', 'meeting', 'course']
    else:
        keywords = ['sport', 'game', 'match', 'play', 'competition']

    return keywords


def get_item_recommendation(tag, item):
    """
    Generate item-specific recommendation based on title and excerpt.

    Returns: String describing recommended action and tags
    """
    title = item['title'].lower()
    excerpt = item['excerpt'].lower()
    combined = (title + ' ' + excerpt).lower()

    # Check for club/organisation indicators
    club_indicators = ['club', 'meeting', 'formed', 'association', 'society', 'committee']
    is_club = any(indicator in combined for indicator in club_indicators)

    # Check for event indicators
    event_indicators = ['match', 'game', 'played', 'competition', 'carnival', 'tournament', 'contest', 'versus', ' v ', ' vs ']
    is_event = any(indicator in combined for indicator in event_indicators)

    # Check for activity/general indicators
    activity_indicators = ['playing', 'ready for play', 'practice', 'season', 'sport']
    is_activity = any(indicator in combined for indicator in activity_indicators)

    # Check for miner involvement
    has_miners = any(word in combined for word in ['miner', 'mines', 'mining', 'shale', 'coal'])

    # Sport-specific analysis
    sport_name = tag.replace(' club', '').replace('Katoomba ', '').replace('Megalong ', '')

    recommendations = []

    # Clubs are organisations
    if 'club' in tag.lower():
        recommendations.append(f"REMOVE from Events > Sporting events")
        recommendations.append(f"Already in Agents > Organizations > Sports clubs")
        return ' | '.join(recommendations)

    # Mixed club + event content
    if is_club and is_event:
        sport_base = sport_name.title()
        recommendations.append(f"MULTIPLE TAGS NEEDED:")
        recommendations.append(f"Agents > Organizations > Sports clubs > {sport_base} clubs > {sport_base} club")
        recommendations.append(f"Events > Sporting events > {sport_base} match")
        if has_miners:
            recommendations.append(f"| ALSO thematic: Recreation for miners")
        return ' '.join(recommendations)

    # Pure club/organisation content
    if is_club and not is_event:
        sport_base = sport_name.title()
        recommendations.append(f"MOVE to: Agents > Organizations > Sports clubs > {sport_base} clubs > {sport_base} club")
        if has_miners:
            recommendations.append(f"| ALSO thematic: Recreation for miners")
        return ' '.join(recommendations)

    # Pure event content
    if is_event and not is_activity:
        sport_base = sport_name.title()
        recommendations.append(f"RENAME to: Events > Sporting events > {sport_base} match")
        if has_miners:
            recommendations.append(f"| ALSO thematic: Recreation for miners")
        return ' '.join(recommendations)

    # General activity/sport
    if is_activity or (not is_event and not is_club):
        sport_base = sport_name.title()
        recommendations.append(f"MOVE to: Activities > Recreation activities > Team sports > {sport_base}")
        if has_miners:
            recommendations.append(f"| ALSO thematic: Recreation for miners")
        return ' '.join(recommendations)

    # Default
    return "REVIEW: Unclear from context, manual review needed"


def get_recommendation(tag, contexts):
    """
    Determine recommendation based on tag and contexts.

    Returns: (category, full_taxonomy_path, rationale)
    """
    tag_lower = tag.lower()

    # Clubs are always organisations
    if 'club' in tag_lower:
        if 'cricket' in tag_lower:
            path = 'Agents > Organizations > Sports clubs > Cricket clubs'
            if tag == 'Cricket club':
                path += ' > Cricket club'
            else:
                path += f' > {tag}'
        elif 'football' in tag_lower:
            path = 'Agents > Organizations > Sports clubs > Football clubs'
            if tag == 'Football club':
                path += ' > Football club'
            else:
                path += f' > {tag}'
        elif 'tennis' in tag_lower:
            path = 'Agents > Organizations > Sports clubs > Tennis clubs > ' + tag
        else:
            path = 'Agents > Organizations > Sports clubs > ' + tag

        return ('REMOVE', path, 'Sports club = organisation, not event. Already correctly classified in Agents facet.')

    # Horse races are specific events
    if tag == 'Horse races':
        return ('KEEP', 'Events > Sporting events > Equestrian events > Horse races',
                'Horse races are specific race meetings (discrete events).')

    if tag == 'Equestrian events':
        return ('KEEP', 'Events > Sporting events > Equestrian events',
                'Parent category for horse-related sporting events.')

    # Billiards likely activity (indoor game)
    if tag in ['Billiard', 'Billiards']:
        return ('MOVE', 'Activities > Recreation activities > Billiards',
                'Indoor game played continuously, not discrete events. Merge Billiard → Billiards.')

    # Analyse contexts to determine event vs activity
    event_indicators = ['match', 'game', 'competition', 'carnival', 'meeting', 'contest', 'tournament']
    activity_indicators = ['playing', 'practice', 'club', 'season', 'general']

    event_count = 0
    activity_count = 0

    for item in contexts:
        excerpt_lower = item['excerpt'].lower()
        for indicator in event_indicators:
            if indicator in excerpt_lower:
                event_count += 1
                break
        for indicator in activity_indicators:
            if indicator in excerpt_lower:
                activity_count += 1
                break

    # Check if tag name itself suggests event
    title_suggests_event = any(title.lower() for title in [item['title'] for item in contexts]
                               if 'match' in title.lower() or 'game' in title.lower() or
                               'carnival' in title.lower() or 'sports' in title.lower())

    # Girls' cricket - special case
    if tag == "Girls' cricket":
        if title_suggests_event:
            return ('KEEP', "Events > Sporting events > Cricket > Girls' cricket",
                    'Item titles suggest specific girls\' cricket matches/events.')
        else:
            return ('MOVE', "Activities > Recreation activities > Cricket > Girls' cricket",
                    'Could be specific matches or general girls playing cricket. Review contexts.')

    # Default: most general sport tags refer to ongoing activities
    if tag in ['Cricket', 'Football', 'Rugby', 'Tennis', 'Shooting', 'Athletics']:
        if title_suggests_event or event_count > activity_count:
            return ('REVIEW', f'Events > Sporting events > {tag}',
                    'Contexts suggest possible specific events. Review carefully to determine if event or activity.')
        else:
            return ('MOVE', f'Activities > Recreation activities > {tag}',
                    'Likely general sport/activity rather than specific events. May need to split if some items are events.')

    # Default
    return ('REVIEW', 'Events > Sporting events > ' + tag,
            'Insufficient information. Review contexts to determine event vs activity.')


def generate_review_report(items_by_tag, output_path):
    """Generate human-readable markdown review report."""

    print(f"\nGenerating review report: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("""# Sporting Events Context Analysis and Reclassification Review

**Date:** 2025-11-01
**Purpose:** Determine which sporting tags represent specific events vs ongoing activities vs organisations

## Instructions

This report requires **ITEM-BY-ITEM review** for proper retagging.

For each tag section:
1. Review the RECOMMENDATION as a general guide
2. For EACH ITEM listed, review the title and text excerpt
3. For EACH ITEM, mark your decision:
   - `[X] Keep as '[tag]'` - Item correctly tagged with current tag
   - `[X] Move to: [new tag path]` - Specify the correct tag (e.g., "Cricket match", "Recreation activities > Cricket")
   - `[X] Remove tag` - Tag doesn't apply to this item

**Key Principle:**
- Events should be named to indicate discrete occurrences: "Cricket match", "Football game", "Shooting competition"
- Activities are ongoing/general: "Cricket" (the sport), "Shooting" (the practice)
- If items under one tag are mixed, they need to be split and retagged appropriately

## Summary Statistics

""")

        # Calculate totals
        total_tags = len(items_by_tag)
        total_items = sum(len(items) for items in items_by_tag.values())

        f.write(f"- Total tags analysed: {total_tags}\n")
        f.write(f"- Total item instances: {total_items}\n\n")

        f.write("| Tag | Items | Current Location | Recommendation |\n")
        f.write("|-----|-------|------------------|----------------|\n")

        for tag in sorted(items_by_tag.keys()):
            count = len(items_by_tag[tag])
            rec_type, rec_path, _ = get_recommendation(tag, items_by_tag[tag])
            current_loc = 'Events > Sporting events'
            if 'club' in tag.lower():
                current_loc += ' (+ Agents > Sports clubs)'

            f.write(f"| {tag} | {count} | {current_loc} | {rec_type} |\n")

        f.write("\n---\n\n")

        # Write detailed analysis for each tag
        f.write("## Detailed Analysis\n\n")

        for tag in sorted(items_by_tag.keys(), key=lambda t: len(items_by_tag[t]), reverse=True):
            f.write(f"### {tag}\n\n")

            count = len(items_by_tag[tag])
            f.write(f"**Items tagged:** {count}  \n")

            rec_type, rec_path, rationale = get_recommendation(tag, items_by_tag[tag])

            f.write(f"**Current classification:** Events > Sporting events")
            if 'club' in tag.lower():
                f.write(" (also in Agents > Sports clubs)")
            f.write("  \n")

            f.write(f"**Recommendation:** **{rec_type}**  \n")
            f.write(f"**Proposed taxonomy:** `{rec_path}`  \n")
            f.write(f"**Rationale:** {rationale}\n\n")

            # Show ALL contexts for item-by-item review with specific recommendations
            f.write("**All items (item-by-item review):**\n\n")
            for i, item in enumerate(items_by_tag[tag], 1):
                f.write(f"{i}. **{item['title']}** ({item['date']})\n")
                f.write(f"   > {item['excerpt']}\n\n")

                # Generate item-specific recommendation
                item_rec = get_item_recommendation(tag, item)
                f.write(f"   **Recommendation:** {item_rec}\n\n")

                f.write(f"   **Your decision:**\n")
                f.write(f"   - [ ] APPROVE recommendation\n")
                f.write(f"   - [ ] MODIFY: ___________________________________________\n")
                f.write(f"   - [ ] REMOVE tag\n\n")

            f.write("---\n\n")

        # Footer
        f.write("""
## Review Complete

Once reviewed, return this report to Claude Code for implementation of approved changes.

**Generated by:** scripts/31_analyse_sporting_events.py
**Source data:** Zotero API (full text from item attachments)
""")

    print(f"✓ Review report generated: {output_path}")


def main():
    """Main execution."""
    print("=" * 80)
    print("SPORTING EVENTS CONTEXT ANALYSIS")
    print("=" * 80)
    print()

    # Define sporting tags to analyse
    sporting_tags = [
        'Athletics', 'Billiard', 'Billiards', 'Cricket', "Girls' cricket",
        'Cricket club', 'Katoomba Cricket Club', 'Megalong Cricket Club',
        'Football', 'Football club', 'Katoomba Football Club',
        'Rugby', 'Shooting', 'Tennis', 'Katoomba Tennis Club',
        'Horse races', 'Equestrian events'
    ]

    # Connect to Zotero
    print("Connecting to Zotero API...")
    zot = connect_to_zotero()

    # Collect items for each tag
    items_by_tag = {}

    for tag in sporting_tags:
        print(f"\nFetching items tagged '{tag}'...")
        items = zot.items(tag=tag)

        if not items:
            print(f"  No items found")
            continue

        print(f"  Found {len(items)} items, extracting contexts...")

        tag_items = []

        for item in items:
            title = item['data'].get('title', 'Untitled')
            date = item['data'].get('date', 'No date')

            # Get full text from children (notes/attachments)
            children = zot.children(item['key'])
            notes = [child for child in children if child['data'].get('itemType') == 'note']

            full_text = ''
            for note in notes:
                note_content = note['data'].get('note', '')
                full_text += strip_html(note_content) + '\n'

            # Extract relevant context
            keywords = get_sport_keywords(tag)
            excerpt = extract_sport_context(full_text, keywords)

            tag_items.append({
                'title': title,
                'date': date,
                'excerpt': excerpt,
                'full_text': full_text
            })

        items_by_tag[tag] = tag_items
        print(f"  ✓ Processed {len(tag_items)} items")

    # Generate review report
    output_path = Path('reports/sporting_events_reclassification_review.md')
    generate_review_report(items_by_tag, output_path)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"\nReview report: {output_path}")
    print("\nNext steps:")
    print("1. Review the report and mark your decisions")
    print("2. Return the reviewed report to Claude Code")
    print("3. Approved changes will be implemented in tag_map_consolidated.csv")


if __name__ == '__main__':
    main()
