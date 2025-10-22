#!/usr/bin/env python3
"""
Script 15: Search for Other Dual-Nature Entities

Identify tags that might represent both organisations AND physical locations.

Pattern: Entity used as both:
1. Organisation/society/group (committee, members, secretary)
2. Physical venue/building (held at, meeting at, building)

Candidates to check:
- Churches (denomination + building)
- Hotels (business + building)
- Progress associations (org + meeting place?)
- Sports clubs (team/club + grounds?)
- Councils (government body + chambers?)
"""

import sys
import re
from pathlib import Path
from collections import Counter

sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def analyse_tag_candidates():
    """Identify potential dual-nature entities from existing tags."""

    # Load tag frequency
    import pandas as pd
    tags_df = pd.read_csv(config.DATA_DIR / 'tag_frequency.csv')

    print("="*70)
    print("POTENTIAL DUAL-NATURE ENTITY CANDIDATES")
    print("="*70)
    print()

    # Categories to check
    categories = {
        'Churches': r'church',
        'Hotels': r'hotel',
        'Progress groups': r'progress',
        'Sports clubs': r'cricket|football|tennis|athletic',
        'Councils': r'council',
        'Reserves': r'reserve',
        'Bands': r'band',
        'Other halls': r'hall'
    }

    for category, pattern in categories.items():
        print(f"\n{category}:")
        print("-" * 50)

        matches = tags_df[tags_df['tag'].str.contains(pattern, case=False, na=False)]

        if len(matches) > 0:
            for _, row in matches.head(10).iterrows():
                print(f"  - {row['tag']} ({row['count']} items)")
        else:
            print("  (none found)")

    print("\n" + "="*70)
    print("RECOMMENDATIONS FOR CONTEXTUAL ANALYSIS")
    print("="*70)
    print()

    print("""
Based on the pattern we discovered (organisations that also have buildings),
here are likely dual-nature candidates to investigate:

HIGH PRIORITY (likely dual-nature):
1. **Churches** - Denomination/organisation + physical building
   - Example: "Methodist Church" = both the Methodist denomination AND the church building
   - Check: Do articles distinguish "at the Methodist Church" (building)
     vs "the Methodist Church" (denomination/congregation)?

2. **Councils** - Governing body + council chambers
   - Example: "Katoomba Council" = both the municipal government AND the chambers
   - Check: References to meetings "at the Council" vs decisions by "the Council"

MEDIUM PRIORITY (possibly dual-nature):
3. **Progress Associations** - Organisation + regular meeting place?
   - May just be organisations that meet at various halls
   - Check: Do they have dedicated premises?

4. **Reserves** - Land designation + committee managing it?
   - Example: "Rifle Reserves" might be both land AND the club/organisation
   - Check: References to "Reserves committee" vs "on the Reserves"

LOW PRIORITY (likely single-nature):
5. **Hotels** - Probably just buildings/businesses (not dual-nature)
   - Physical venue with commercial function, not separate organisation

6. **Sports clubs** - Probably organisations only (grounds separately named)
   - Cricket Club = organisation
   - Cricket Ground = venue (if mentioned)
   - Check: Are grounds separately tagged?

RECOMMENDATION:
Run contextual analysis on Churches and Councils first, as these are most likely
to show dual-nature patterns similar to Schools of Arts and Lodge Halls.
    """)


def main():
    """Main execution."""
    try:
        analyse_tag_candidates()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
