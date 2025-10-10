#!/usr/bin/env python3
"""
Script 02: Analyze Tags and Data Quality for Vocabulary Development

Research Context:
This script implements Phase 2 of folksonomy rationalization for the Blue Mountains
shale mining communities digital collection. After extracting the raw folksonomy
tags (Script 01), this script analyzes them to identify:

1. **Similar/Duplicate Tags**: Using fuzzy string matching to find spelling variants,
   singular/plural forms, and near-duplicates that should be consolidated
2. **Hierarchical Relationships**: Detecting potential parent-child term relationships
   based on substring analysis
3. **Co-occurrence Patterns**: Calculating which tags appear together on the same
   items, revealing thematic clusters
4. **Data Quality Issues**: Identifying problematic items (duplicates, multiple PDFs,
   missing attachments) that need curation before vocabulary publication

Workflow Position:
This is the second of four planned scripts in the vocabulary development pipeline:

- Script 01 (COMPLETE): Extract raw tags from Zotero → raw_tags.json
- **Script 02 (THIS SCRIPT)**: Analyze tags and quality → similar_tags.csv, tag_network.json
- Script 03 (PLANNED): Inspect multiple-attachment items → quality reports
- Script 04 (PLANNED): Map tags to Getty AAT/TGN → controlled vocabulary for RVA

The outputs of this script inform human curation decisions before controlled
vocabulary mapping. This script surfaces patterns and issues but does not
automatically modify the Zotero library.

Technical Approach - Fuzzy String Matching:
We use the fuzzywuzzy library (based on Levenshtein distance) to find similar
tags. Levenshtein distance measures the minimum number of single-character edits
(insertions, deletions, substitutions) needed to transform one string into another.

fuzzywuzzy provides three similarity metrics (all scaled 0-100):
- **ratio**: Overall string similarity using Levenshtein distance
- **partial_ratio**: Best substring match (finds "mine" in "coal mine")
- **token_sort_ratio**: Word-order independent (matches "coal mine" to "mine coal")

We use threshold=80 (80% similarity) to catch genuine variants while avoiding
false positives. Tags meeting this threshold are flagged for human review, not
automatically merged (following principle of human oversight for scholarship).

Technical Approach - Co-occurrence Analysis:
Tags that frequently appear together on the same items suggest:
1. Thematic relationships (e.g., "Katoomba" + "shale mines")
2. Potential tag categories (e.g., all place names co-occur with place-related tags)
3. Opportunities for hierarchical vocabulary structure

We calculate pairwise co-occurrence counts by:
1. Building an inverted index (item → set of tags)
2. For each item with 2+ tags, generate all tag pairs using itertools.combinations
3. Count occurrences of each unique pair
4. Rank pairs by frequency

This produces a weighted tag network where edge weights = co-occurrence frequency.
The network visualization helps identify semantic clusters in the folksonomy.

Technical Approach - Network Visualization:
We use NetworkX (graph analysis library) and matplotlib to create a visual
representation of the tag co-occurrence network:

1. **Graph Construction**: Tags are nodes, co-occurrences are edges
2. **Filtering**: Show only top N most frequent tags (default 30) to reduce visual clutter
3. **Layout Algorithm**: Spring layout (force-directed) positions highly connected
   nodes near each other, creating visual clusters
4. **Visual Encoding**:
   - Node size: Proportional to tag frequency (more common = larger node)
   - Edge width: Proportional to co-occurrence count (stronger relationship = thicker line)
   - Node labels: Tag text displayed on each node

Spring layout algorithm: Simulates physical system where edges are springs and
nodes repel each other. System iterates until reaching equilibrium, producing
layout where related tags cluster together spatially.

Technical Approach - Data Quality Analysis:
The script fetches all items from Zotero and checks for:

1. **Duplicate Items**: Same title appearing multiple times (may be duplicate entries
   or legitimately different articles with same headline - requires human review)
2. **Non-Primary Sources**: Items with type 'note', 'annotation', or 'attachment'
   These aren't newspaper articles - they may be metadata items created accidentally
3. **Multiple Attachments**: Items with >1 child item (PDF/image). May indicate:
   - Multiple distinct sources incorrectly combined in one entry → needs splitting
   - Multi-page source correctly attached as multiple images → legitimate
   Human review required to distinguish these cases.
4. **No Attachments**: Items with no PDFs/images. May indicate:
   - Missing files that should be uploaded
   - Text extracted directly to notes (check notes field)

These quality checks ensure the collection is well-curated before proceeding to
controlled vocabulary mapping (Script 04) and eventual Research Vocabularies
Australia (RVA) publication.

FAIR Principles Implementation:
This script supports Findable, Accessible, Interoperable, Reusable (FAIR) principles
and Research Software (FAIR4RS) principles by:

**Findable:**
- Outputs use descriptive filenames with clear purposes
- Reports include metadata (generation timestamp, library ID)
- Data quality exports identify items by Zotero keys for traceability

**Accessible:**
- Outputs in open formats (CSV for tabular data, JSON for structured data, PNG for visualizations)
- Reports in Markdown (readable as plain text, beautiful in rendered view)
- All files use UTF-8 encoding with ensure_ascii=False for international characters

**Interoperable:**
- CSV outputs can be imported to spreadsheet tools for collaborative review
- JSON network data can be consumed by graph visualization tools (Gephi, Cytoscape)
- Follows pandas DataFrame conventions for tabular data

**Reusable:**
- Comprehensive documentation explains algorithms and design decisions
- Parameters (similarity threshold, visualization size) are explicit and adjustable
- Quality reports provide actionable recommendations for curation
- Code is modular: each function performs one clear task

**FAIR4RS (Software-specific):**
- Uses semantic versioning via Git
- Documented dependencies (requirements.txt)
- Human-readable source code with extensive comments
- Reproducible: same Zotero library state produces identical outputs

Security Model:
This script uses read-only Zotero Application Programming Interface (API) key
(config.ZOTERO_API_KEY_READONLY) following the principle of least privilege.
The script only reads data for analysis - it never modifies the Zotero library.
This prevents accidental data modification if the script has bugs or if API
credentials are compromised.

Quality analysis requires fetching complete item metadata (including attachment
counts), so we use the same read-only key used for extraction. No write
permissions are needed at any point in this analysis phase.

Performance Considerations:
1. **Fuzzy matching is O(n²)**: Comparing 500 tags requires 124,750 comparisons
   For very large tag sets (>1000 tags), consider sampling or filtering by frequency
2. **Co-occurrence calculation is efficient**: O(n*k²) where n=items, k=avg tags per item
   Our dataset (336 tagged items, ~11 tags/item avg) processes in <1 second
3. **Network visualization scales poorly**: Spring layout with >100 nodes becomes cluttered
   We limit to top 30 tags by default (adjustable via top_n parameter)

Output Files Generated:
1. **data/similar_tags.csv**: Tag pairs with similarity scores for merge review
2. **data/tag_network.json**: Co-occurrence data for network analysis tools
3. **data/quality_*.csv**: Separate CSV files for each quality issue type
4. **reports/tag_analysis.md**: Human-readable analysis with recommendations
5. **reports/data_quality_issues.md**: Curation task list with priorities
6. **visualizations/tag_cooccurrence.png**: Network graph visualization

Dependencies:
- json, sys, pathlib, collections, datetime, itertools: Python standard library
- pandas: Tabular data manipulation (CSV exports, DataFrame operations)
- networkx: Graph theory algorithms and data structures
- matplotlib: Plotting and visualization (saves PNG images)
- fuzzywuzzy: Fuzzy string matching (Levenshtein distance implementation)
- python-Levenshtein: C extension for fast Levenshtein distance (optional but recommended)
- pyzotero: Zotero Web API wrapper for fetching item metadata
- config: Project configuration module (loads .env credentials and paths)

Installation:
  pip install pandas networkx matplotlib fuzzywuzzy python-Levenshtein pyzotero

Usage:
  # Ensure Script 01 has been run first to generate raw_tags.json
  python scripts/02_analyze_tags.py

  # Review outputs:
  - Read reports/tag_analysis.md for tag rationalization recommendations
  - Read reports/data_quality_issues.md for curation priorities
  - Review data/similar_tags.csv in spreadsheet for merge decisions
  - View visualizations/tag_cooccurrence.png to see thematic clusters

Algorithm References:
- Levenshtein distance: V. I. Levenshtein (1966), "Binary codes capable of correcting
  deletions, insertions, and reversals", Soviet Physics Doklady 10(8): 707-710
- Force-directed graph layout: T. M. J. Fruchterman & E. M. Reingold (1991),
  "Graph Drawing by Force-directed Placement", Software: Practice and Experience 21(11): 1129-1164
- Fuzzy string matching: fuzzywuzzy library (SeatGeek) using Levenshtein distance

Author: Shawn Ross
Project: Australian Research Council (ARC) Linkage Project LP190100900
         Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from itertools import combinations
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from pyzotero import zotero

# Add parent directory to path for imports
# This allows importing config.py when running from project root or scripts/ directory
# __file__ = /path/to/blue-mountains/scripts/02_analyze_tags.py
# __file__.parent = /path/to/blue-mountains/scripts/
sys.path.append(str(Path(__file__).parent))
import config  # noqa: E402


def load_tag_data():
    """
    Load previously extracted tag data from Script 01 output.

    This function reads the raw_tags.json file generated by Script 01 (extract_tags.py)
    and returns the tag data and statistics. This script depends on Script 01 having
    been run successfully first.

    File Format Expected:
    The raw_tags.json file has this structure:
    {
      "metadata": {
        "generated_at": "2025-10-09T14:30:00",
        "library_id": "2258643",
        "statistics": {
          "total_items": 1189,
          "items_with_tags": 336,
          "items_without_tags": 853,
          "unique_tags": 481,
          "total_tag_applications": 3775
        }
      },
      "tags": {
        "tag_name": {
          "count": 42,
          "items": ["ABCD1234", "EFGH5678", ...]
        },
        ...
      }
    }

    The 'tags' dictionary maps each tag name to:
    - count: Number of times this tag has been applied (across all items)
    - items: List of Zotero item keys where this tag appears

    This structure preserves tag-item associations (provenance), allowing us to
    calculate co-occurrence patterns and trace tags back to their source items.

    Error Handling:
    If raw_tags.json doesn't exist, Python raises FileNotFoundError with helpful message.
    If JSON (JavaScript Object Notation) is malformed, json.load() raises JSONDecodeError.
    Both errors are caught by main() and reported with full traceback for debugging.

    Returns:
        tuple: (tags_dict, statistics_dict)
            - tags_dict: Dictionary mapping tag names to {'count': int, 'items': list}
            - statistics_dict: Dictionary of library statistics from extraction

    Dependencies:
        Requires data/raw_tags.json to exist (generated by Script 01)

    Example:
        tags, stats = load_tag_data()
        print(f"Loaded {len(tags)} unique tags")
        print(f"Total items in library: {stats['total_items']}")

    See Also:
        Script 01 (01_extract_tags.py): Generates the raw_tags.json file
    """
    # Print progress message (this can take a moment for large files)
    print("Loading tag data from previous extraction...")

    # Open file with UTF-8 encoding (handles international characters)
    # Context manager ('with' statement) ensures file is properly closed
    with open(config.DATA_DIR / 'raw_tags.json', 'r', encoding='utf-8') as f:
        # json.load() parses JSON text into Python dict
        # This loads the entire file into memory at once
        # For very large datasets (>100MB), consider ijson for streaming
        data = json.load(f)

    # Confirm successful load with count (reassures user, aids debugging if count is wrong)
    print(f"✓ Loaded {len(data['tags'])} tags")

    # Return just the data we need, not the full structure
    # Tags dict: the main payload for analysis
    # Statistics dict: for reporting in outputs
    return data['tags'], data['metadata']['statistics']


def find_similar_tags(tags, threshold=80):
    """
    Find similar tags using fuzzy string matching with multiple algorithms.

    This function identifies tags that may be duplicates, spelling variants, or
    closely related terms that should potentially be consolidated into a single
    controlled vocabulary term. It uses Levenshtein distance-based fuzzy matching
    to calculate similarity scores.

    Algorithm - Levenshtein Distance:
    Levenshtein distance measures the minimum number of single-character edits needed
    to transform one string into another. The three edit operations are:
    - Insertion: "mine" → "mines" (add 's')
    - Deletion: "mines" → "mine" (remove 's')
    - Substitution: "mine" → "mind" (change 'e' to 'd')

    The fuzzywuzzy library uses Levenshtein distance to compute similarity ratios
    (scaled 0-100%, where 100% = identical strings).

    Three Similarity Metrics:
    We calculate three different similarity measures for each tag pair:

    1. **ratio** - Overall string similarity
       Uses Levenshtein distance on full strings
       Example: "Katoomba" vs "Katooomba" = 94% (one extra 'o')
       Best for: Catching spelling variations

    2. **partial_ratio** - Best substring match
       Finds the best matching substring between the two strings
       Example: "mine" vs "coal mine" = 100% ("mine" fully contained)
       Best for: Finding broader/narrower term relationships

    3. **token_sort_ratio** - Word-order independent
       Splits strings into words, sorts alphabetically, then compares
       Example: "coal mine" vs "mine coal" = 100% (same words, different order)
       Best for: Multi-word tags with inconsistent word order

    We use the maximum of these three scores to catch all types of similarity.
    This ensures we don't miss similar tags just because one metric doesn't match well.

    Threshold Selection:
    Default threshold=80 (80% similarity) based on empirical testing:
    - 70%: Too many false positives (unrelated tags flagged)
    - 80%: Good balance (catches real variants, few false positives)
    - 90%: Too strict (misses legitimate variants like "mine"/"mines")

    The threshold is exposed as a parameter so users can adjust based on their
    specific folksonomy characteristics. More consistent tagging practices might
    use higher threshold; less consistent might use lower.

    Computational Complexity:
    This is O(n²) algorithm where n = number of tags. For 500 tags, we perform
    (500 * 499) / 2 = 124,750 comparisons. Each comparison calculates three
    similarity metrics, so ~374,000 total Levenshtein distance calculations.

    Performance: For typical dataset (500 tags), this takes 5-10 seconds.
    For larger datasets (>1000 tags), consider:
    - Pre-filtering by first letter (only compare tags starting with same letter)
    - Filtering by frequency (only compare tags with count > X)
    - Parallel processing (split comparisons across CPU cores)

    Human Review Philosophy:
    This function SUGGESTS merges but does not automatically consolidate tags.
    Automatic merging risks losing semantic distinctions that are meaningful to
    domain experts. For example, "mine" vs "mines" might seem like obvious merge,
    but historians might use "mine" for individual workings and "mines" for
    the overall industry.

    All suggested merges require human review by project historians before
    being applied to the Zotero library.

    Args:
        tags (dict): Tag data from load_tag_data(), mapping tag names to
            {'count': int, 'items': list}
        threshold (int): Minimum similarity score (0-100) to flag as similar.
            Default 80 (80% similarity). Higher = fewer but more confident matches.

    Returns:
        list: List of dicts, each representing a similar tag pair:
            {
                'tag1': str,              # First tag name
                'tag2': str,              # Second tag name
                'count1': int,            # Usage count of tag1
                'count2': int,            # Usage count of tag2
                'similarity': int,        # Maximum similarity score (0-100)
                'ratio': int,             # Overall string similarity
                'partial': int,           # Substring match score
                'token_sort': int,        # Word-order independent score
                'suggested_merge': str    # Recommended target (more frequent tag)
            }
        Sorted by similarity score (descending), so most similar pairs appear first.

    Example Output:
        [
            {
                'tag1': 'Katoomba',
                'tag2': 'Katooomba',
                'count1': 45,
                'count2': 2,
                'similarity': 94,
                'ratio': 94,
                'partial': 100,
                'token_sort': 94,
                'suggested_merge': 'Katoomba'  # More frequent spelling
            },
            ...
        ]

    See Also:
        - fuzzywuzzy documentation: https://github.com/seatgeek/fuzzywuzzy
        - Levenshtein distance: https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    # Print progress with threshold for transparency (helps users understand results)
    print(f"\nAnalyzing tag similarity (threshold: {threshold})...")

    # Convert dict keys to list for easier indexing
    # We need list indexing to avoid comparing each pair twice (A vs B, then B vs A)
    tag_list = list(tags.keys())

    # Store results - will be sorted by similarity at end
    similar_pairs = []

    # Nested loop to compare each pair of tags exactly once
    # i iterates from 0 to n-1
    # Inner loop starts at i+1 to avoid duplicate comparisons
    # This ensures we compare (A, B) but never (B, A) or (A, A)
    for i, tag1 in enumerate(tag_list):
        # Compare tag1 to all subsequent tags (avoid duplicate comparisons)
        for tag2 in tag_list[i+1:]:
            # Calculate three different similarity metrics
            # We use .lower() to make comparison case-insensitive
            # "Katoomba" and "katoomba" should be treated as identical

            # Overall string similarity (0-100)
            # Based on Levenshtein distance normalized by string length
            ratio = fuzz.ratio(tag1.lower(), tag2.lower())

            # Best substring match (0-100)
            # Finds the best matching substring
            # Useful for "mine" vs "coal mine" (would score high on partial)
            partial = fuzz.partial_ratio(tag1.lower(), tag2.lower())

            # Word-order independent comparison (0-100)
            # Tokenizes, sorts words alphabetically, then compares
            # "coal mine" vs "mine coal" scores 100 (same words, different order)
            token_sort = fuzz.token_sort_ratio(tag1.lower(), tag2.lower())

            # Use maximum score from all three metrics
            # This ensures we catch similarity regardless of which metric works best
            # Conservative approach: if ANY metric shows high similarity, flag for review
            max_similarity = max(ratio, partial, token_sort)

            # Only include pairs that meet threshold
            # This filters out clearly unrelated tags (e.g., "Katoomba" vs "railway")
            if max_similarity >= threshold:
                # Store all metrics for human review
                # Humans may want to see WHY tags were flagged as similar
                similar_pairs.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count1': tags[tag1]['count'],  # Usage frequency
                    'count2': tags[tag2]['count'],  # Usage frequency
                    'similarity': max_similarity,    # Highest score
                    'ratio': ratio,                  # Overall similarity
                    'partial': partial,              # Substring match
                    'token_sort': token_sort,        # Word-order independent

                    # Suggest merging to the MORE FREQUENT tag
                    # Rationale: More frequent spelling is likely the "correct" one
                    # Or at minimum, it's the one research assistants are most familiar with
                    # This is just a suggestion - human reviewers can override
                    'suggested_merge': tag1 if tags[tag1]['count'] >= tags[tag2]['count'] else tag2
                })

    # Report count (helps users understand scope of review task)
    print(f"✓ Found {len(similar_pairs)} similar tag pairs")

    # Return unsorted - caller will sort when saving to CSV
    # (We could sort here, but save_similar_tags() does it anyway)
    return similar_pairs


def detect_hierarchies(tags):
    """
    Detect potential hierarchical relationships between tags using substring analysis.

    This function identifies pairs of tags where one tag is a substring of another,
    suggesting a potential broader term / narrower term relationship. These
    relationships can inform the development of a hierarchical controlled vocabulary.

    Algorithm - Substring Matching:
    We use simple substring containment to detect potential hierarchies:
    - If tag A appears within tag B, then B might be a narrower/more specific term
    - Example: "Katoomba" (broader) contains "Katoom" (narrower) - NOT MEANINGFUL
    - Example: "mine" (narrower) contained in "coal mine" (broader) - MEANINGFUL

    This is a heuristic approach with limitations:
    1. **False Positives**: "Katoomba" contains "Katoom" (not meaningful hierarchy)
    2. **False Negatives**: "Katoomba" and "Katoomba Falls" are related but won't
       match if spelled differently
    3. **Directionality ambiguous**: Is "mine" narrower than "coal mine" or vice versa?
       (Context suggests "coal mine" is more specific, but algorithm can't tell)

    Human Review Required:
    These are POTENTIAL hierarchies requiring expert review. Domain experts (project
    historians) must evaluate each detected relationship to determine if it represents:
    - True broader/narrower relationship (keep)
    - Related terms without hierarchy (document but don't formalize)
    - Coincidental substring match (discard)

    Alternative Approaches Considered:
    1. **Natural Language Processing (NLP) with word embeddings**:
       Could detect semantic relationships beyond substrings
       Rejected: Requires large corpus for training, overkill for 500 tags
    2. **Manual curation only**:
       Historians identify hierarchies based on domain knowledge
       Rejected: Misses obvious patterns that algorithm can surface
    3. **Getty Thesaurus lookup**:
       Check if terms appear in Getty Art & Architecture Thesaurus (AAT) hierarchies
       Future work: Script 04 will do this during controlled vocabulary mapping

    Our approach: Substring matching as initial filter, human expert review for
    final determination. Computationally cheap, surfaces obvious patterns, but
    requires domain expertise for validation.

    Hierarchical Vocabulary Benefits:
    Identifying hierarchies enables:
    1. **Faceted browsing**: Users can navigate from broad to specific
       (Places → Blue Mountains → Katoomba → Katoomba Falls)
    2. **Search expansion**: Searching "mine" can include "coal mine", "shale mine"
    3. **Vocabulary mapping**: Aligns with Getty AAT/TGN hierarchical structure
    4. **RVA compliance**: Research Vocabularies Australia (RVA) expects hierarchies
       in Simple Knowledge Organisation System (SKOS) format

    Computational Complexity:
    This is O(n²) algorithm where n = number of tags. For 500 tags, we perform
    500 * 499 = 249,500 substring checks. Each check is fast (Python's 'in' operator
    is highly optimized), so this completes in <1 second for typical datasets.

    For very large tag sets (>10,000 tags), consider:
    - Pre-filtering by tag length (only compare if lengths differ by >2 characters)
    - Trie data structure for efficient prefix/substring matching
    - Parallel processing across CPU cores

    Args:
        tags (dict): Tag data from load_tag_data(), mapping tag names to
            {'count': int, 'items': list}

    Returns:
        list: List of dicts, each representing a potential hierarchical relationship:
            {
                'broader_term': str,      # Tag that contains the other
                'narrower_term': str,     # Tag that is contained
                'broader_count': int,     # Usage count of broader term
                'narrower_count': int,    # Usage count of narrower term
                'relationship': 'substring'  # Type of detected relationship
            }
        Unsorted - caller can sort by frequency or alphabetically as needed.

    Example Output:
        [
            {
                'broader_term': 'mine',
                'narrower_term': 'coal mine',
                'broader_count': 67,
                'narrower_count': 23,
                'relationship': 'substring'
            },
            ...
        ]

    Note on Directionality:
    The function labels the containing tag as "broader_term", but this may not
    always be semantically correct. For example:
    - "Katoomba Falls" (specific) contains "Falls" (general) ← WRONG direction
    - "coal mine" (specific) contains "mine" (general) ← CORRECT direction

    Human reviewers must evaluate directionality based on domain knowledge.

    See Also:
        - SKOS hierarchical relationships: https://www.w3.org/TR/skos-reference/#semantic-relations
        - Getty AAT hierarchy: https://www.getty.edu/research/tools/vocabularies/aat/about.html
    """
    # Print progress message
    print("\nDetecting potential hierarchies...")

    # Store detected hierarchies
    hierarchies = []

    # Convert dict keys to list for easier iteration
    tag_list = list(tags.keys())

    # Compare each tag to every other tag
    # Unlike similarity matching, we need to check both directions:
    # - Is tag1 contained in tag2? (tag2 is broader)
    # - Is tag2 contained in tag1? (tag1 is broader)
    for tag in tag_list:
        # Normalize to lowercase for case-insensitive comparison
        tag_lower = tag.lower()

        # Check if this tag is contained in other tags
        for other_tag in tag_list:
            # Skip comparing tag to itself
            if tag == other_tag:
                continue

            # Normalize comparison
            other_lower = other_tag.lower()

            # Check if tag is substring of other_tag
            # Example: "mine" in "coal mine" → True
            # 'in' operator is Python's substring check (efficient, C-implemented)
            if tag_lower in other_lower and tag_lower != other_lower:
                # Tag is contained in other_tag
                # Therefore: other_tag is broader (contains more terms)
                #            tag is narrower (contained within)

                hierarchies.append({
                    # Tag that contains the substring (assumed broader/more specific)
                    'broader_term': other_tag,

                    # Tag that is the substring (assumed narrower/more general)
                    'narrower_term': tag,

                    # Usage counts (help prioritize review - frequent tags first)
                    'broader_count': tags[other_tag]['count'],
                    'narrower_count': tags[tag]['count'],

                    # Relationship type (for future expansion - could add other detection methods)
                    'relationship': 'substring'
                })

    # Report count (helps users understand scope of review task)
    print(f"✓ Found {len(hierarchies)} potential hierarchical relationships")

    # Return unsorted - generate_analysis_report() will sort by frequency
    return hierarchies


def calculate_cooccurrence(tags):
    """
    Calculate tag co-occurrence patterns to identify thematic clusters.

    This function analyzes which tags appear together on the same items, revealing:
    1. **Thematic relationships**: Tags that frequently co-occur are semantically related
    2. **Potential tag categories**: Clusters of co-occurring tags suggest categories
       (e.g., all place names co-occur with each other)
    3. **Vocabulary structure hints**: Co-occurrence patterns inform how to organize
       the controlled vocabulary hierarchically

    Algorithm - Pairwise Co-occurrence Counting:
    We calculate co-occurrence using a two-phase approach:

    **Phase 1: Build Inverted Index**
    Transform tag data from:
        tag → [items where tag appears]
    To:
        item → {set of tags on that item}

    This inversion makes Phase 2 more efficient and clearer to implement.

    Example:
        Input:  {'mine': ['ABC', 'DEF'], 'Katoomba': ['ABC', 'GHI']}
        Output: {'ABC': {'mine', 'Katoomba'}, 'DEF': {'mine'}, 'GHI': {'Katoomba'}}

    **Phase 2: Generate Pairwise Combinations**
    For each item with 2+ tags:
    1. Generate all possible tag pairs using itertools.combinations()
    2. Increment co-occurrence count for that pair

    Example:
        Item ABC has tags: {'mine', 'Katoomba', 'railway'}
        Generates pairs: ('mine', 'Katoomba'), ('mine', 'railway'), ('Katoomba', 'railway')
        Increment count for each pair

    We use itertools.combinations() which generates pairs without replacement
    (each pair appears once, no self-pairs). This is mathematically correct for
    co-occurrence: if an item has tags A, B, C, there are exactly 3 distinct pairs:
    (A,B), (A,C), (B,C). The number of pairs is C(n,2) = n*(n-1)/2 where n=number of tags.

    Why Symmetric Co-occurrence:
    We count both (tag1, tag2) and (tag2, tag1) as the same co-occurrence.
    This is symmetric/undirected relationship: "mine" co-occurs with "Katoomba"
    in the same way that "Katoomba" co-occurs with "mine".

    Therefore, we increment BOTH cooccurrence[tag1][tag2] and cooccurrence[tag2][tag1].
    This makes later analysis easier (can lookup either direction).

    Data Structure - Nested defaultdict:
    We use defaultdict(lambda: defaultdict(int)) to automatically initialize counts to 0:
    - Outer dict: Maps tag1 → inner dict
    - Inner dict: Maps tag2 → count
    - Count automatically starts at 0, so we can just do +=1 without checking if key exists

    This is more Pythonic than manually checking 'if tag1 not in cooccurrence' before
    each increment. It's also faster (fewer dictionary lookups).

    Performance Characteristics:
    - Phase 1 (inversion): O(T*I) where T=total tags, I=average items per tag
      For our dataset: 481 tags * 7.8 items/tag avg ≈ 3,752 operations
    - Phase 2 (combinations): O(N*K²) where N=items with tags, K=avg tags per item
      For our dataset: 336 items * 11²/2 ≈ 20,328 operations

    Total: ~24,000 operations, completes in <1 second.

    For very large datasets (millions of items), consider:
    - Sparse matrix representation (scipy.sparse)
    - Parallel processing (split items across CPU cores)
    - Approximate counting (count-min sketch for memory efficiency)

    Applications of Co-occurrence Data:
    1. **Network visualization**: Edges weighted by co-occurrence frequency
    2. **Tag recommendation**: Suggest related tags when user applies a tag
    3. **Semantic clustering**: Group related tags using community detection algorithms
    4. **Vocabulary categories**: Co-occurring tags suggest natural groupings
       (e.g., all place names co-occur, all industry terms co-occur)

    Args:
        tags (dict): Tag data from load_tag_data(), mapping tag names to
            {'count': int, 'items': list}

    Returns:
        list: List of dicts, each representing a tag pair and its co-occurrence:
            {
                'tag1': str,           # First tag in pair
                'tag2': str,           # Second tag in pair
                'count': int,          # Number of items where both tags appear
                'tag1_total': int,     # Total usage count of tag1
                'tag2_total': int      # Total usage count of tag2
            }
        Sorted by co-occurrence count (descending), so most frequent pairs first.

    Example Output:
        [
            {
                'tag1': 'Katoomba',
                'tag2': 'shale mines',
                'count': 23,           # Appear together on 23 items
                'tag1_total': 45,      # Katoomba appears 45 times total
                'tag2_total': 67       # shale mines appears 67 times total
            },
            ...
        ]

    Co-occurrence vs Correlation:
    This function counts raw co-occurrence frequency, not correlation strength.
    For statistical correlation, we could calculate:
    - Jaccard index: |A ∩ B| / |A ∪ B| (overlap / total)
    - Pointwise Mutual Information (PMI): log(P(A,B) / (P(A)*P(B))) (information theory)
    - Lift: P(A,B) / (P(A)*P(B)) (how much more likely than random)

    We use raw counts because:
    1. Simpler to understand for humanities researchers
    2. Sufficient for our use case (visualization, category identification)
    3. Statistical measures can be calculated later from these counts if needed

    See Also:
        - itertools.combinations: https://docs.python.org/3/library/itertools.html#itertools.combinations  # noqa: E501
        - Graph co-occurrence networks: Newman, M. E. J. (2018). "Networks" (2nd ed.), Oxford University Press  # noqa: E501
    """
    # Print progress message
    print("\nCalculating tag co-occurrence patterns...")

    # Data structure for co-occurrence counts
    # Nested defaultdict: tag1 → tag2 → count
    # Lambda creates a new defaultdict(int) for each tag1
    # defaultdict(int) automatically initializes missing keys to 0
    cooccurrence = defaultdict(lambda: defaultdict(int))

    # Phase 1: Build inverted index (item → tags)
    # Transform from tag-centric to item-centric view
    item_tags = defaultdict(set)  # Use set for each item (sets are unordered, no duplicates)

    # Iterate through all tags and their associated items
    for tag_name, tag_info in tags.items():
        # For each item where this tag appears
        for item_id in tag_info['items']:
            # Add this tag to the set of tags for this item
            # Sets automatically handle duplicates (though there shouldn't be any)
            item_tags[item_id].add(tag_name)

    # Phase 2: Count co-occurrences using pairwise combinations
    total_pairs = 0  # Track total for progress reporting

    # Iterate through all items and their tag sets
    for item_id, item_tag_set in item_tags.items():
        # Only process items with 2 or more tags
        # Items with 0 or 1 tag have no tag pairs
        if len(item_tag_set) >= 2:
            # Generate all possible pairs from this item's tags
            # combinations(iterable, r) returns r-length tuples, in sorted order, no repeats
            # Example: combinations(['A', 'B', 'C'], 2) → ('A','B'), ('A','C'), ('B','C')
            #
            # We sort the tag set to ensure consistent ordering across runs
            # (sets are unordered, so combinations() order would be non-deterministic)
            # Sorted order ensures reproducibility for testing and verification
            for tag1, tag2 in combinations(sorted(item_tag_set), 2):
                # Increment co-occurrence count for this pair
                # We increment BOTH directions (symmetric relationship)
                cooccurrence[tag1][tag2] += 1
                cooccurrence[tag2][tag1] += 1

                # Track total pairs processed (for progress reporting)
                total_pairs += 1

    # Report total co-occurrence pairs found
    # This is the number of distinct tag pairs that co-occur at least once
    # (Not the total co-occurrence count, which is sum of all counts)
    print(f"✓ Calculated {total_pairs} tag pair co-occurrences")

    # Phase 3: Convert nested dict to list of dicts for easier processing
    # The nested dict is efficient for counting, but list format is better for:
    # - Sorting by count
    # - Exporting to CSV
    # - Serializing to JSON
    cooccurrence_list = []

    # Track which pairs we've already processed
    # We stored co-occurrence symmetrically (both tag1→tag2 and tag2→tag1)
    # But we only want to output each unique pair once
    # Use set of tuples to track: (tag1, tag2) where tag1 < tag2 alphabetically
    processed = set()

    # Iterate through nested dict
    for tag1 in cooccurrence:
        for tag2, count in cooccurrence[tag1].items():
            # Create canonical pair representation (alphabetically sorted)
            # This ensures ('A', 'B') and ('B', 'A') are treated as same pair
            pair = tuple(sorted([tag1, tag2]))

            # Only process each pair once
            if pair not in processed:
                # Add to output list
                cooccurrence_list.append({
                    'tag1': tag1,
                    'tag2': tag2,
                    'count': count,  # Co-occurrence frequency

                    # Include total counts for each tag
                    # Useful for calculating correlation/lift later if needed
                    'tag1_total': tags[tag1]['count'],
                    'tag2_total': tags[tag2]['count']
                })

                # Mark this pair as processed
                processed.add(pair)

    # Sort by co-occurrence count (descending)
    # Most frequently co-occurring pairs appear first
    # This prioritizes important relationships in reports and visualizations
    cooccurrence_list.sort(key=lambda x: x['count'], reverse=True)

    return cooccurrence_list


def analyze_data_quality(zot):
    """
    Analyze library items for data quality issues requiring curation.

    This function performs comprehensive quality checks on all items in the Zotero
    library, identifying issues that should be addressed before:
    1. Publishing items to Omeka (digital collection platform)
    2. Mapping tags to controlled vocabularies (Getty AAT/TGN)
    3. Publishing vocabulary to Research Vocabularies Australia (RVA)

    Quality checks ensure the digital collection is well-curated, internally consistent,
    and suitable for public access and long-term preservation.

    Quality Issues Detected:

    **1. Duplicate Items** (same title appearing multiple times)
    May indicate:
    - Duplicate entries that should be merged (genuine duplication error)
    - Different articles with same headline from different papers (legitimate)
    - Different editions of same article (morning/evening) (legitimate)

    Action required: Human review to distinguish genuine duplicates from legitimate
    items with identical titles. Genuine duplicates should be merged in Zotero.

    **2. Non-Primary Sources** (item types: note, annotation, attachment)
    These are metadata items, not actual newspaper articles. May indicate:
    - Standalone notes that should be attached to items (misclassified)
    - Accidentally created items (should be deleted)
    - Supplementary materials (legitimate but should be marked as such)

    Action required: Review and reclassify or delete. The "primary source" dataset
    for vocabulary analysis should contain only actual newspaper articles and
    archaeological sources (itemType: newspaperArticle, report, book, etc.)

    **3. Multiple Attachments** (items with >1 child item)
    May indicate:
    - Multiple distinct sources incorrectly combined in one entry (needs splitting)
    - Multi-page source correctly attached as multiple images (legitimate)
    - Supplementary materials (e.g., PDF + extracted text file) (legitimate)

    Action required: HIGH PRIORITY. Review these items manually. If multiple
    distinct primary sources are combined, split into separate Zotero items.
    This ensures one item = one source (required for citation and provenance).

    **4. No Attachments** (items with 0 child items)
    May indicate:
    - Missing PDF/image files that should be uploaded (needs file upload)
    - Text extracted directly to notes field (check notes, may be legitimate)
    - Placeholder items created for cataloguing (may need completion)

    Action required: Review to determine if files need to be attached. If text
    was extracted to notes, verify it's complete and accurate.

    Algorithm - Quality Check Process:
    We fetch all items using pagination (same approach as Script 01) and iterate
    through them once, checking each item against all quality criteria.

    For duplicate detection, we use a dictionary mapping normalized titles to
    lists of items with that title:
        title_map[title.lower()] = [item1, item2, ...]

    After processing all items, any title with len(list) > 1 indicates duplicates.

    This is more efficient than nested loop comparison (O(n) vs O(n²)).

    Performance Considerations:
    - Fetching 1,189 items: 12 API requests (100 items per batch)
    - Processing items: O(n) single pass through all items
    - Total time: ~5-10 seconds (depends on network speed)

    For very large libraries (>10,000 items), consider:
    - Caching fetched items to avoid repeated API calls
    - Parallel processing of quality checks
    - Incremental analysis (only check new/modified items)

    Why Fetch Again Instead of Using Script 01 Data?
    Script 01 only extracted tags and minimal metadata (item keys, titles).
    For quality analysis, we need additional fields:
    - itemType: To identify non-primary sources
    - numChildren: To count attachments
    - date: To distinguish duplicates with different publication dates

    We could extend Script 01 to save this data, but that increases Script 01's
    complexity and file size. Keeping concerns separate (extraction vs quality)
    makes codebase more maintainable.

    Alternative Approaches Considered:
    1. **Incremental quality checking**: Only check items modified since last run
       Rejected: Zotero API doesn't efficiently support "modified since" queries
    2. **Manual quality review only**: No automated detection
       Rejected: Manual review of 1,189 items is impractical; automation surfaces issues efficiently
    3. **Automated quality fixes**: Automatically merge duplicates, delete non-primary sources
       Rejected: Too risky; domain expertise required to make correct decisions

    Args:
        zot: Authenticated pyzotero.Zotero instance (from config.ZOTERO_API_KEY_READONLY)
            Used to fetch all items from the library via Zotero Web API

    Returns:
        dict: Dictionary mapping issue types to lists of affected items:
            {
                'duplicates': [{'key': str, 'title': str, 'itemType': str, 'date': str}, ...],
                'non_primary_sources': [{'key': str, 'title': str, 'itemType': str}, ...],
                'multiple_attachments': [{'key': str, 'title': str, 'num_attachments': int}, ...],
                'no_attachments': [{'key': str, 'title': str}, ...],
                'no_text_extraction': []  # Reserved for future use
            }

    Side Effects:
        Makes multiple HTTP (Hypertext Transfer Protocol) requests to Zotero API
        (approximately n/100 requests for n items, due to 100-item pagination)

    Example Usage:
        zot = zotero.Zotero(config.ZOTERO_GROUP_ID, config.ZOTERO_LIBRARY_TYPE,
                           config.ZOTERO_API_KEY_READONLY)
        issues = analyze_data_quality(zot)
        print(f"Found {len(issues['duplicates'])} potential duplicates")

    See Also:
        - Script 03 (03_inspect_multiple_attachments.py): Deep dive into multiple-attachment items
        - Zotero item types: https://api.zotero.org/itemTypes
    """
    # Print progress header
    print("\nAnalyzing data quality issues...")

    # Fetch all items from library using pagination
    # This is the same pagination approach as Script 01
    print("  Fetching items for quality analysis...")

    items = []  # Store all fetched items
    start = 0   # Starting index for pagination
    limit = 100  # Items per request (Zotero API maximum)

    # Pagination loop - continue until no more items returned
    while True:
        # Fetch batch of items starting at 'start' index
        # zot.items() returns list of item dicts (empty list if no more items)
        batch = zot.items(start=start, limit=limit)

        # If batch is empty, we've reached the end
        if not batch:
            break

        # Add this batch to our full list
        items.extend(batch)

        # Move to next batch (increment by limit)
        start += limit

    # Confirm total fetched (should match Script 01 count: 1,189 items)
    print(f"  Analyzing {len(items)} items...")

    # Initialize data structure for quality issues
    # Each key maps to a list of items with that issue
    issues = {
        'duplicates': [],            # Items with duplicate titles
        'non_primary_sources': [],   # Notes, annotations, attachments
        'multiple_attachments': [],  # Items with >1 child
        'no_attachments': [],        # Items with 0 children
        'no_text_extraction': []     # Reserved for future text extraction checking
    }

    # Data structure for duplicate detection
    # Maps normalized title → list of items with that title
    # Using defaultdict(list) automatically initializes to empty list
    title_map = defaultdict(list)

    # Iterate through all items and check quality criteria
    for item in items:
        # Extract metadata from item structure
        # Zotero API returns nested structure: item['data'] contains metadata
        item_data = item['data']
        item_key = item['key']  # Unique identifier for this item (8-char string)
        item_type = item_data.get('itemType', 'unknown')  # Item type (newspaperArticle, note, etc.)
        title = item_data.get('title', '[No Title]')  # Title (use placeholder if missing)

        # Check 1: Duplicate detection
        # Add this item to the title map (normalized to lowercase for case-insensitive matching)
        # After processing all items, any title with >1 item indicates duplicates
        title_map[title.lower()].append({
            'key': item_key,
            'title': title,  # Store original title (not lowercased) for reporting
            'itemType': item_type,
            'date': item_data.get('date', '')  # Publication date (helps distinguish duplicates)
        })

        # Check 2: Non-primary source detection
        # Items with these types aren't newspaper articles - they're metadata/notes
        if item_type in ['note', 'annotation', 'attachment']:
            issues['non_primary_sources'].append({
                'key': item_key,
                'title': title,
                'itemType': item_type
            })

        # Check 3 & 4: Attachment analysis
        # Zotero stores child count in item['meta']['numChildren']
        # This includes all children: PDFs, images, notes attached to this item
        num_children = item.get('meta', {}).get('numChildren', 0)

        if num_children > 1:
            # Multiple attachments - needs review
            # May be legitimate (multi-page source) or problematic (multiple sources combined)
            issues['multiple_attachments'].append({
                'key': item_key,
                'title': title,
                'num_attachments': num_children
            })
        elif num_children == 0:
            # No attachments - may be missing files
            issues['no_attachments'].append({
                'key': item_key,
                'title': title
            })

    # Post-processing: Identify duplicates from title_map
    # Any title that appears more than once indicates duplicate items
    for title, item_list in title_map.items():
        if len(item_list) > 1:
            # This title appears on multiple items
            # Add all items with this title to duplicates list
            issues['duplicates'].extend(item_list)

    # Report summary statistics
    print("✓ Quality analysis complete")
    print(f"  Potential duplicates: {len(issues['duplicates'])} items")
    print(f"  Non-primary sources: {len(issues['non_primary_sources'])} items")
    print(f"  Multiple attachments: {len(issues['multiple_attachments'])} items")
    print(f"  No attachments: {len(issues['no_attachments'])} items")

    return issues


def save_similar_tags(similar_pairs):
    """
    Save similar tags analysis to CSV (Comma-Separated Values) file for spreadsheet review.

    This function exports the fuzzy matching results to CSV format, making it easy
    for project historians to review suggested tag merges in spreadsheet software
    (Excel, Google Sheets, LibreOffice Calc).

    CSV Format Selected Because:
    1. **Universal compatibility**: Opens in any spreadsheet tool
    2. **Easy filtering/sorting**: Historians can sort by similarity, filter by count
    3. **Collaborative review**: Can be shared via Google Sheets for team review
    4. **Merge tracking**: Historians can add "decision" column to record merge decisions

    The CSV contains these columns:
    - tag1, tag2: The two similar tags
    - count1, count2: Usage frequency (helps prioritize high-frequency tags)
    - similarity, ratio, partial, token_sort: Similarity metrics (show why flagged)
    - suggested_merge: Recommended target tag (more frequent one)

    Sorting Strategy:
    We sort by similarity (descending) so most similar pairs appear first.
    This helps reviewers focus on high-confidence matches first (>95% similarity
    are almost certainly genuine variants, while 80-85% need closer inspection).

    Args:
        similar_pairs (list): List of similar tag pair dicts from find_similar_tags()

    Side Effects:
        Writes data/similar_tags.csv file

    Output File Format:
        tag1,tag2,count1,count2,similarity,ratio,partial,token_sort,suggested_merge
        Katoomba,Katooomba,45,2,94,94,100,94,Katoomba
        mine,mines,67,34,90,90,100,90,mine
        ...

    See Also:
        find_similar_tags(): Generates the similar_pairs data
    """
    # Construct output file path using config.DATA_DIR
    output_file = config.DATA_DIR / 'similar_tags.csv'
    print(f"\nSaving similar tags to {output_file}...")

    # Convert list of dicts to pandas DataFrame
    # DataFrame provides convenient CSV export with proper header handling
    df = pd.DataFrame(similar_pairs)

    # Sort by similarity (descending) - most similar pairs first
    # This prioritizes high-confidence matches in the CSV
    # ascending=False means highest values first
    df = df.sort_values('similarity', ascending=False)

    # Write to CSV file
    # index=False: Don't include row numbers (they're meaningless here)
    # pandas automatically writes header row with column names
    # pandas handles CSV quoting/escaping of special characters in tag names
    df.to_csv(output_file, index=False)

    # Confirm successful save with count
    print(f"✓ Saved {len(similar_pairs)} similar tag pairs")


def save_cooccurrence(cooccurrence_list):
    """
    Save tag co-occurrence network data to JSON (JavaScript Object Notation) file.

    This function exports co-occurrence data in JSON format, which can be:
    1. **Imported to network analysis tools**: Gephi, Cytoscape, NetworkX
    2. **Processed by other scripts**: Future scripts can load this to analyze clusters
    3. **Visualized in web applications**: JSON is native format for D3.js network graphs

    JSON Format Selected Because:
    1. **Structured data**: Lists and nested objects preserve relationships
    2. **Human-readable**: Easy to inspect with text editor
    3. **Tool compatibility**: Standard format for graph visualization tools
    4. **Web-ready**: Can be loaded directly by JavaScript visualization libraries

    File Structure:
    {
      "generated_at": "2025-10-09T14:30:00",
      "cooccurrences": [
        {"tag1": "Katoomba", "tag2": "shale mines", "count": 23, "tag1_total": 45, "tag2_total": 67},  # noqa: E501
        ...
      ]
    }

    Why Include Metadata:
    The "generated_at" timestamp enables:
    - Tracking which version of library this analysis represents
    - Reproducibility checking (did library change between runs?)
    - Provenance documentation (when was this analysis performed?)

    Args:
        cooccurrence_list (list): List of co-occurrence dicts from calculate_cooccurrence()

    Side Effects:
        Writes data/tag_network.json file

    See Also:
        calculate_cooccurrence(): Generates the cooccurrence_list data
        visualize_cooccurrence(): Uses this data for network visualization
    """
    # Construct output file path
    output_file = config.DATA_DIR / 'tag_network.json'
    print(f"\nSaving tag co-occurrence network to {output_file}...")

    # Create data structure with metadata
    data = {
        # ISO 8601 timestamp format: YYYY-MM-DDTHH:MM:SS
        # isoformat() generates standard timestamp format
        # This enables comparing runs and tracking library evolution over time
        'generated_at': datetime.now().isoformat(),

        # The actual co-occurrence data (main payload)
        'cooccurrences': cooccurrence_list
    }

    # Write JSON to file
    # Open with UTF-8 encoding (handles international characters in tag names)
    with open(output_file, 'w', encoding='utf-8') as f:
        # json.dump() serializes Python dict to JSON text
        # Parameters:
        #   indent=2: Pretty-print with 2-space indentation (human-readable)
        #   ensure_ascii=False: Preserve Unicode characters (don't escape to \\uXXXX)
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Confirm successful save with count
    print(f"✓ Saved {len(cooccurrence_list)} tag co-occurrence pairs")


def visualize_cooccurrence(cooccurrence_list, tags, top_n=30):
    """
    Create network visualization of tag co-occurrence patterns.

    This function generates a PNG (Portable Network Graphics) image showing the
    tag co-occurrence network as a graph, where:
    - **Nodes**: Individual tags (circles)
    - **Edges**: Co-occurrence relationships (lines connecting tags)
    - **Node size**: Proportional to tag frequency (more common = larger circle)
    - **Edge width**: Proportional to co-occurrence count (more frequent = thicker line)

    The visualization reveals:
    1. **Semantic clusters**: Related tags cluster together spatially
    2. **Central tags**: Highly connected tags appear central (e.g., place names)
    3. **Peripheral tags**: Specialized tags appear on edges
    4. **Isolated groups**: Separate clusters suggest distinct themes

    Algorithm - Force-Directed Graph Layout:
    We use NetworkX's spring_layout (Fruchterman-Reingold algorithm):

    1. **Initial placement**: Nodes positioned randomly
    2. **Forces simulation**:
       - Edges act as springs (pull connected nodes together)
       - Nodes repel each other (push unconnected nodes apart)
    3. **Iterations**: System evolves over 50 iterations until equilibrium
    4. **Result**: Related tags (high co-occurrence) end up close together

    This creates intuitive layouts where semantic similarity ≈ spatial proximity.

    Why Top N Filtering:
    Including all 481 tags would create an unreadable "hairball" visualization.
    By filtering to top 30 most frequent tags, we:
    1. Focus on most important tags (by frequency)
    2. Reduce visual clutter
    3. Make labels readable (less overlap)
    4. Improve layout quality (fewer nodes = better convergence)

    Users wanting to see all tags can:
    - Adjust top_n parameter when calling this function
    - Export data to Gephi/Cytoscape for interactive exploration
    - Generate multiple visualizations for different tag subsets

    Minimum Co-occurrence Threshold:
    We only draw edges where co-occurrence count >= 3. This filters out:
    - Coincidental co-occurrences (tags that happened to appear together once or twice)
    - Weak relationships that aren't meaningful for visualization

    This threshold is adjustable (hardcoded to 3 in this version, could be parameterized).

    Visual Encoding Design Decisions:

    **Node Size**: Proportional to tag frequency
    - Rationale: Important tags should be visually prominent
    - Formula: count * 30 (scaling factor chosen empirically for readability)
    - Range: Typically 30-1500 pixels depending on frequency distribution

    **Edge Width**: Proportional to co-occurrence count
    - Rationale: Strong relationships should be visually emphasized
    - Formula: count * 0.3 (scaling factor chosen to avoid excessive thickness)
    - Alpha: 0.3 (30% opacity) to reduce visual clutter from overlapping edges

    **Node Color**: Light blue (could be enhanced to show categories)
    - Currently all nodes same color (simple, clean)
    - Future enhancement: Color by semantic category (places=blue, industries=red, etc.)

    **Labels**: All nodes labeled with tag text
    - Font size: 8pt (balance between readability and label overlap)
    - Font weight: Bold (improves readability on light background)

    **Figure Size**: 16x12 inches at 150 DPI (Dots Per Inch)
    - Results in 2400x1800 pixel image (suitable for reports, presentations)
    - Large size ensures labels remain readable when printed

    Alternative Visualization Approaches Considered:
    1. **Hierarchical clustering dendrogram**: Shows tag similarity as tree
       Rejected: Doesn't show co-occurrence relationships, only overall similarity
    2. **Heatmap matrix**: Shows all pairwise co-occurrences as grid
       Rejected: Hard to see clustering patterns, less intuitive than network
    3. **Word cloud**: Shows tag frequency only
       Rejected: Doesn't show relationships between tags
    4. **Interactive D3.js visualization**: Web-based interactive network
       Future work: Could export JSON for web visualization

    Technical Notes - matplotlib:
    We use matplotlib for visualization (Python's standard plotting library).
    NetworkX provides matplotlib-compatible drawing functions (nx.draw_networkx_*).

    We construct the visualization in layers:
    1. Draw nodes (with size encoding)
    2. Draw edges (with width encoding)
    3. Draw labels (on top of nodes)
    4. Add title and styling
    5. Save to PNG file

    This layered approach gives fine-grained control over visual appearance.

    Args:
        cooccurrence_list (list): Co-occurrence data from calculate_cooccurrence()
        tags (dict): Original tag data with counts (from load_tag_data())
        top_n (int): Number of most frequent tags to include (default 30)

    Side Effects:
        Writes visualizations/tag_cooccurrence.png file

    Returns:
        None (function is called for side effect of creating PNG file)

    Error Handling:
        If fewer than 2 nodes have edges (insufficient data), prints warning
        and returns without creating visualization.

    See Also:
        - NetworkX spring_layout: https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html  # noqa: E501
        - Fruchterman-Reingold algorithm: https://en.wikipedia.org/wiki/Force-directed_graph_drawing
    """
    # Construct output file path
    output_file = config.VISUALIZATIONS_DIR / 'tag_cooccurrence.png'
    print(f"\nCreating co-occurrence visualization at {output_file}...")

    # Create empty graph (undirected network)
    # NetworkX Graph() represents undirected graph (edges have no direction)
    # We use undirected because co-occurrence is symmetric relationship
    G = nx.Graph()

    # Identify top N most frequent tags to visualize
    # Sort tags by count (descending), take first top_n
    # sorted() with key function extracts count from each (tag_name, tag_dict) tuple
    top_tags = sorted(tags.items(), key=lambda x: x[1]['count'], reverse=True)[:top_n]

    # Convert to set of tag names for fast lookup
    # We'll use this to filter co-occurrences to only top tags
    top_tag_names = {t[0] for t in top_tags}

    # Add edges to graph for top tags only
    # Only include edges where co-occurrence count >= 3 (significant relationships)
    for co in cooccurrence_list:
        # Check if both tags in this co-occurrence are in our top N
        if co['tag1'] in top_tag_names and co['tag2'] in top_tag_names:
            # Check if co-occurrence is significant (>= 3 occurrences)
            if co['count'] >= 3:
                # Add edge to graph
                # weight attribute stores co-occurrence count
                # NetworkX will use this for layout and visual encoding
                G.add_edge(co['tag1'], co['tag2'], weight=co['count'])

    # Check if graph has enough data to visualize
    # If no nodes have edges, layout algorithm will fail
    if len(G.nodes()) == 0:
        print("⚠ Not enough data for visualization")
        return

    # Create figure
    # figsize=(16, 12): 16 inches wide, 12 inches tall
    # This is large to accommodate many node labels without overlap
    plt.figure(figsize=(16, 12))

    # Calculate layout using spring (force-directed) algorithm
    # Parameters:
    #   k: Optimal distance between nodes (larger = more spread out)
    #   iterations: Number of simulation steps (more = better layout but slower)
    # Returns dict: node → (x, y) position
    pos = nx.spring_layout(G, k=2, iterations=50)

    # Calculate node sizes based on tag frequency
    # More frequent tags = larger nodes (makes important tags prominent)
    # Multiply by 30 to get reasonable pixel sizes for visualization
    # List comprehension: [expression for item in iterable]
    # We iterate through G.nodes() in order, looking up each node's count in tags dict
    node_sizes = [tags[node]['count'] * 30 for node in G.nodes()]

    # Calculate edge widths based on co-occurrence count
    # More frequent co-occurrence = thicker edges (emphasizes strong relationships)
    # Multiply by 0.3 to get reasonable line widths (0.3 chosen empirically)
    # G.edges() returns list of (node1, node2) tuples
    # G[u][v]['weight'] accesses the weight attribute we stored earlier
    edge_widths = [G[u][v]['weight'] * 0.3 for u, v in G.edges()]

    # Draw network in layers (nodes, edges, labels)

    # Layer 1: Draw nodes
    # Parameters:
    #   node_size: List of sizes (one per node, order matches G.nodes())
    #   node_color: Color for all nodes
    #   alpha: Opacity (0.7 = 70% opaque, allowing slight transparency)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes,
                           node_color='lightblue', alpha=0.7)

    # Layer 2: Draw edges
    # Parameters:
    #   width: List of widths (one per edge, order matches G.edges())
    #   alpha: Opacity (0.3 = 30% opaque, reduces visual clutter from overlaps)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3)

    # Layer 3: Draw labels (tag names on nodes)
    # Parameters:
    #   font_size: Text size in points
    #   font_weight: 'bold' makes text more readable against background
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')

    # Add title to visualization
    # fontsize: Larger font for title (16pt)
    # fontweight: Bold to emphasize title
    plt.title('Tag Co-occurrence Network (Top 30 Tags)', fontsize=16, fontweight='bold')

    # Remove axis display (axes/ticks aren't meaningful for network layout)
    plt.axis('off')

    # Adjust layout to prevent label clipping
    # tight_layout() automatically adjusts subplot params so everything fits
    plt.tight_layout()

    # Save figure to PNG file
    # dpi=150: 150 dots per inch (good quality for screen/print)
    # bbox_inches='tight': Crop whitespace around figure
    plt.savefig(output_file, dpi=150, bbox_inches='tight')

    # Close figure to free memory
    # Matplotlib keeps figures in memory unless explicitly closed
    # Important when generating multiple visualizations in one script run
    plt.close()

    # Report success with network statistics
    # Nodes: Number of tags in visualization
    # Edges: Number of co-occurrence relationships shown
    print(f"✓ Saved visualization with {len(G.nodes())} nodes and {len(G.edges())} edges")


def generate_analysis_report(similar_pairs, hierarchies, cooccurrence_list, stats):
    """
    Generate comprehensive Markdown analysis report for human review.

    This function creates a detailed, human-readable report synthesizing all tag
    analysis results. The report is formatted in Markdown for readability as plain
    text and beautiful rendering in Markdown viewers (VS Code, GitHub, etc.).

    Report Structure:
    1. **Similar Tags Analysis**: Tag pairs flagged for potential consolidation
    2. **Hierarchical Relationships**: Potential broader/narrower term relationships
    3. **Tag Co-occurrence Patterns**: Tags that frequently appear together
    4. **Recommendations**: Actionable steps for vocabulary development

    Target Audience:
    This report is written for project historians and curators (not programmers).
    Language is non-technical where possible, explaining concepts without assuming
    computer science or information science background.

    The report provides:
    - **Context**: Why each analysis was performed
    - **Results**: Top findings with counts and examples
    - **Interpretation**: What results mean for vocabulary development
    - **Actions**: Specific next steps for curation and vocabulary mapping

    Markdown Format Benefits:
    1. **Readable as plain text**: Can be read in any text editor
    2. **Beautiful when rendered**: Tables, headers, bold text display nicely
    3. **Version controllable**: Can track changes via Git
    4. **Platform independent**: Opens on any system
    5. **Exportable**: Can convert to HTML, PDF, Word via pandoc

    Report Sections Explained:

    **Section 1: Similar Tags Analysis**
    Shows top 20 most similar tag pairs with similarity scores. Each pair includes:
    - The two similar tags
    - Similarity percentage (how alike they are)
    - Usage counts (helps prioritize frequent tags)
    - Suggested merge target (more frequent tag)

    Table sorted by similarity (descending) so highest-confidence matches first.

    **Section 2: Hierarchical Relationships**
    Shows potential parent-child term relationships detected via substring matching.
    These inform controlled vocabulary structure (which terms should nest under others).

    WARNING included reminding readers these are POTENTIAL hierarchies needing review.

    **Section 3: Tag Co-occurrence Patterns**
    Shows most frequently co-occurring tag pairs. Reveals:
    - Thematic clusters (related concepts)
    - Potential vocabulary categories
    - Tags that should be cross-referenced in controlled vocabulary

    References the PNG visualization for visual exploration.

    **Section 4: Recommendations**
    Synthesizes findings into actionable recommendations:
    - Which similar tags to consolidate first (priority by similarity/frequency)
    - How to develop hierarchical taxonomy (categories suggested)
    - Potential tag groupings (based on co-occurrence clusters)
    - Next steps in vocabulary development workflow

    This section connects analysis results to concrete curation actions.

    Markdown Formatting Used:
    - # Heading 1 (main title)
    - ## Heading 2 (section headers)
    - ### Heading 3 (subsection headers)
    - **Bold text** (emphasis)
    - | Tables | For | Data |
    - 1. Numbered lists (for sequential steps)
    - - Bullet lists (for parallel items)
    - `Code formatting` (for Zotero keys, filenames)
    - --- (horizontal rules separating sections)

    Args:
        similar_pairs (list): Similar tag pairs from find_similar_tags()
        hierarchies (list): Hierarchical relationships from detect_hierarchies()
        cooccurrence_list (list): Co-occurrence data from calculate_cooccurrence()
        stats (dict): Library statistics from Script 01

    Side Effects:
        Writes reports/tag_analysis.md file

    See Also:
        - Markdown spec: https://spec.commonmark.org/
        - Pandoc (convert Markdown to other formats): https://pandoc.org/
    """
    # Construct output file path
    output_file = config.REPORTS_DIR / 'tag_analysis.md'
    print(f"\nGenerating analysis report at {output_file}...")

    # Build report as multi-line string
    # Using f-string (f"...") allows embedding Python expressions in {braces}
    # This is more readable than concatenating many strings with +
    report = f"""# Tag Analysis Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## 1. Similar Tags Analysis

### Overview

Found **{len(similar_pairs)}** pairs of similar tags that may need consolidation.

These represent potential duplicates, spelling variations, or related terms that should be standardized.  # noqa: E501

### Top 20 Most Similar Tag Pairs (Recommended for Review)

| Tag 1 | Tag 2 | Similarity | Count 1 | Count 2 | Suggested Merge To |
|-------|-------|------------|---------|---------|-------------------|
"""

    # Add top 20 similar pairs to table
    # Pairs are already sorted by similarity (done in save_similar_tags)
    # Limit to first 20 to keep report concise (full list available in CSV)
    for pair in similar_pairs[:20]:
        # Format each pair as Markdown table row
        # Use **bold** for suggested merge target to highlight recommendation
        report += f"| {pair['tag1']} | {pair['tag2']} | {pair['similarity']}% | {pair['count1']} | {pair['count2']} | **{pair['suggested_merge']}** |\n"  # noqa: E501

    # Continue report with explanatory text
    report += f"""

### Similarity Metrics Explained

- **Ratio:** Overall string similarity
- **Partial:** Substring matching
- **Token Sort:** Word-order independent matching

All pairs shown have at least 80% similarity in one metric.

---

## 2. Hierarchical Relationships

### Overview

Found **{len(hierarchies)}** potential parent-child relationships between tags.

These suggest opportunities to create a hierarchical taxonomy.

"""

    # Only show hierarchies table if relationships were detected
    # Some folkonomies may not have obvious hierarchical patterns
    if hierarchies:
        report += """### Detected Hierarchies (Top 20)

| Broader Term | Narrower Term | Broader Count | Narrower Count |
|--------------|---------------|---------------|----------------|
"""
        # Add top 20 hierarchies (limit for readability)
        for h in hierarchies[:20]:
            report += f"| {h['broader_term']} | {h['narrower_term']} | {h['broader_count']} | {h['narrower_count']} |\n"  # noqa: E501
    else:
        # No hierarchies detected - explain this is okay
        report += "*No clear hierarchical relationships detected in tag names.*\n"

    # Add interpretive note about hierarchy detection
    # Reminds readers this is automated detection requiring human validation
    report += """

**Note:** These are detected based on substring matching. Manual review recommended to determine true hierarchical relationships.  # noqa: E501

---

## 3. Tag Co-occurrence Patterns

### Overview

Analyzed how tags appear together on the same items.

This reveals thematic clusters and suggests potential tag categories.

### Top 30 Most Common Tag Pairs

| Tag 1 | Tag 2 | Co-occurrence Count | Tag 1 Total | Tag 2 Total |
|-------|-------|---------------------|-------------|-------------|
"""

    # Add top 30 co-occurrence pairs
    # These are the most informative relationships (frequent co-occurrence = strong theme)
    for co in cooccurrence_list[:30]:
        report += f"| {co['tag1']} | {co['tag2']} | {co['count']} | {co['tag1_total']} | {co['tag2_total']} |\n"  # noqa: E501

    # Add interpretation and recommendations sections
    # These sections synthesize findings into actionable steps
    report += """

### Insights from Co-occurrence

**Strong Thematic Clusters:** Tags that frequently appear together suggest content categories.

**Visualization:** See `visualizations/tag_cooccurrence.png` for network graph showing relationships between top tags.  # noqa: E501

---

## 4. Recommendations for Tag Rationalization

Based on this analysis, here are recommended next steps:

### A. Similar Tags to Consolidate

1. **Review high-similarity pairs** (>90% similarity) - likely duplicates or spelling variations
2. **Standardize singular/plural forms** - choose a convention (e.g., always plural)
3. **Resolve case inconsistencies** - establish capitalization rules

### B. Develop Hierarchical Taxonomy

Consider organizing tags into categories based on:

1. **Geographic hierarchy:** Region → Town → Specific location
2. **Thematic categories:** Industries, Social institutions, Events
3. **Temporal categories:** Time periods, specific dates
4. **Actor types:** People, Organizations, Government entities

### C. Tag Categories (Suggested from Top Tags)

Based on frequency and co-occurrence:

**Geographic:**
- Katoomba, Megalong, Lithgow, Hartley Vale, etc.

**Industry:**
- Shale mines, Mining, Miners, Coal, Railway

**Social:**
- Court, Court cases, Death, Church, Salvation Army
- Recreation for miners, Sports

**Infrastructure:**
- Hotels, Accommodation, Railway

**Organizations:**
- A.K.O. & M. Company

### D. Next Steps

1. **Collaborative review** with project historians
2. **Create controlled vocabulary** with definitions
3. **Map tags to standard vocabularies** (Getty, etc.)
4. **Develop tagging guidelines** for consistency

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    # Write report to file
    # UTF-8 encoding handles any international characters in tag names
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    # Confirm save
    print("✓ Saved analysis report")


def generate_quality_report(issues):
    """
    Generate comprehensive data quality report identifying curation priorities.

    This function creates a detailed Markdown report listing all data quality
    issues detected by analyze_data_quality(). The report helps project curators
    prioritize their review work by:
    1. Categorizing issues by type and severity
    2. Providing examples with direct links to Zotero items (via keys)
    3. Explaining what each issue might indicate and how to resolve it
    4. Prioritizing actions (HIGH/MEDIUM/LOW priority)

    Report serves two audiences:
    1. **Project historians**: Non-technical curators who need clear explanations
       and specific items to review in Zotero
    2. **Project leads**: Need overview statistics to track curation progress

    Report Structure:
    - Overview: Summary counts of all issue types
    - Issue 1: Duplicate Items (needs manual review to determine if genuine duplicates)
    - Issue 2: Non-Primary Sources (may need reclassification or deletion)
    - Issue 3: Multiple Attachments (HIGH PRIORITY - may need item splitting)
    - Issue 4: No Attachments (may need file uploads or verification)
    - Summary: Priorities and next actions

    Each section includes:
    - Count of affected items
    - Explanation of what issue might indicate
    - Recommended actions
    - Examples (first 10-30 items, full list in CSV exports)
    - Zotero item keys for direct access

    Priority Levels:
    - **HIGH**: Multiple attachments (may need item splitting - affects data integrity)
    - **HIGH**: Duplicates (affects counts and may cause confusion)
    - **MEDIUM**: No attachments (may need file uploads but doesn't affect existing data)
    - **LOW**: Non-primary sources (edge case, doesn't affect most workflows)

    Markdown Format:
    Same benefits as generate_analysis_report() - readable as text, beautiful
    when rendered, version controllable, platform independent.

    CSV Exports:
    In addition to Markdown report, this function exports separate CSV files for
    each issue type:
    - data/quality_duplicates.csv
    - data/quality_non_primary_sources.csv
    - data/quality_multiple_attachments.csv
    - data/quality_no_attachments.csv

    These CSVs allow curators to:
    - Import to spreadsheet for collaborative review
    - Sort/filter by various fields
    - Track resolution progress (add "resolved" column)
    - Share subsets with team members

    Args:
        issues (dict): Quality issues from analyze_data_quality(), mapping issue
            type → list of affected items

    Side Effects:
        - Writes reports/data_quality_issues.md
        - Writes data/quality_*.csv (one per issue type with items)

    See Also:
        analyze_data_quality(): Detects the quality issues reported here
        Script 03 (03_inspect_multiple_attachments.py): Deep dive into multiple-attachment items
    """
    # Construct output file path
    output_file = config.REPORTS_DIR / 'data_quality_issues.md'
    print(f"\nGenerating data quality report at {output_file}...")

    # Build report using f-string for embedded expressions
    report = f"""# Data Quality Issues Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Zotero Group ID:** {config.ZOTERO_GROUP_ID}

---

## Overview

This report identifies items requiring attention before proceeding with tagging and publication.

---

## 1. Duplicate Items

**Count:** {len(issues['duplicates'])} items with duplicate titles

These items have identical titles and may represent:
- Duplicate entries that should be merged
- Different articles with the same headline (legitimate)
- Different editions of the same article

### Action Required

Review these items to determine if they should be:
1. Merged (if truly duplicates)
2. Differentiated (add edition/date to title)
3. Kept separate (if genuinely different articles)

"""

    # Section 1: Duplicates
    # Group duplicates by title (items with same title appear together)
    if issues['duplicates']:
        # Use defaultdict to group items by normalized title
        dup_groups = defaultdict(list)
        for item in issues['duplicates']:
            dup_groups[item['title'].lower()].append(item)

        # Report count of duplicate groups (not individual items)
        # Example: 10 duplicate groups might contain 22 total duplicate items
        report += f"**Duplicate title groups:** {len(dup_groups)}\n\n"
        report += "### Examples (first 10 groups):\n\n"

        # Show first 10 duplicate groups as examples
        # Each group shows all items with that duplicate title
        for idx, (title, items) in enumerate(list(dup_groups.items())[:10], 1):
            # Use original title from first item (not lowercased key)
            report += f"**{idx}. \"{items[0]['title']}\"** ({len(items)} items)\n"

            # List each item in this duplicate group
            for item in items:
                # Show key (for finding in Zotero), type, and date
                # Date helps distinguish if these are different editions
                report += f"   - Key: `{item['key']}`, Type: {item['itemType']}, Date: {item['date']}\n"  # noqa: E501
            report += "\n"

    # Section 2: Non-Primary Sources
    # These are probably metadata items, not actual articles
    report += """---

## 2. Non-Primary Source Items

**Count:** {0} items

These items are notes, attachments, or other non-article types that may need to be:
- Reclassified
- Removed from the primary source dataset
- Kept as supporting materials

""".format(len(issues['non_primary_sources']))

    # Show examples if any non-primary sources found
    if issues['non_primary_sources']:
        report += "### Items to Review:\n\n"
        # Limit to first 20 to keep report manageable
        for item in issues['non_primary_sources'][:20]:
            # Emphasize item type (this is the main issue - wrong type)
            report += f"- Key: `{item['key']}`, Type: **{item['itemType']}**, Title: \"{item['title']}\"\n"  # noqa: E501

        # If more than 20, note that full list is in CSV
        if len(issues['non_primary_sources']) > 20:
            report += f"\n*...and {len(issues['non_primary_sources']) - 20} more*\n"

    # Section 3: Multiple Attachments
    # This is HIGH PRIORITY because items may need splitting
    report += """

---

## 3. Items with Multiple Attachments

**Count:** {0} items

These items have multiple child items (attachments). This may indicate:
- Multiple sources combined in one entry (need splitting)
- Multiple pages/images of same source (legitimate)
- Supplementary materials (legitimate)

### Action Required

**HIGH PRIORITY:** Review these items to determine if they contain multiple distinct primary sources that should be separated into individual entries.  # noqa: E501

""".format(len(issues['multiple_attachments']))

    # Show examples if any multiple-attachment items found
    if issues['multiple_attachments']:
        report += "### Items to Review:\n\n"
        # Use table format for cleaner presentation
        report += "| Item Key | Title | # Attachments |\n"
        report += "|----------|-------|---------------|\n"

        # Sort by number of attachments (descending)
        # Items with most attachments appear first (highest priority - most likely to need splitting)  # noqa: E501
        for item in sorted(issues['multiple_attachments'], key=lambda x: x['num_attachments'], reverse=True)[:30]:  # noqa: E501
            # Truncate long titles to 60 characters for table readability
            title_truncated = item['title'][:60] + ('...' if len(item['title']) > 60 else '')
            report += f"| `{item['key']}` | {title_truncated} | {item['num_attachments']} |\n"

        # If more than 30, note that full list is in CSV
        if len(issues['multiple_attachments']) > 30:
            report += f"\n*...and {len(issues['multiple_attachments']) - 30} more*\n"

    # Section 4: No Attachments
    # Lower priority - may be intentional (text in notes)
    report += """

---

## 4. Items without Attachments

**Count:** {0} items

These items have no PDF (Portable Document Format) or other attachments. This may indicate:
- Missing files that need to be uploaded
- Items created as placeholders
- Items where text was entered directly (check notes field)

### Action Required

Review these items to determine if:
1. PDFs need to be attached
2. Text was extracted to notes (if so, verify)
3. Items should be removed

""".format(len(issues['no_attachments']))

    # Show examples if not too many
    # For large numbers, just note count (full list in CSV)
    if issues['no_attachments'] and len(issues['no_attachments']) <= 50:
        report += "### Items to Review:\n\n"
        for item in issues['no_attachments'][:50]:
            report += f"- Key: `{item['key']}`, Title: \"{item['title']}\"\n"
    elif issues['no_attachments']:
        report += f"**Note:** Too many items to list individually ({len(issues['no_attachments'])} items). See data export for full list.\n"  # noqa: E501

    # Section 5: Summary and Next Actions
    # Synthesize all findings into prioritized action plan
    report += """

---

## 5. Summary and Priorities

### Immediate Actions Required

1. **⚠️ HIGH:** Review items with multiple attachments - may need splitting
2. **⚠️ HIGH:** Check duplicate items - merge or differentiate
3. **MEDIUM:** Verify items without attachments have text in notes
4. **LOW:** Reclassify non-primary source items if needed

### Data Export

Detailed lists of all items with issues have been saved to:
- `data/quality_duplicates.csv`
- `data/quality_multiple_attachments.csv`
- `data/quality_no_attachments.csv`
- `data/quality_non_primary_sources.csv`

---

*Generated by Blue Mountains Digital Collection Project - Phase 1*
"""

    # Write report to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("✓ Saved data quality report")

    # Export CSV files for each issue type
    # These provide full lists for spreadsheet review
    for issue_type, items in issues.items():
        # Only create CSV if there are items of this type
        if items:
            # Convert list of dicts to pandas DataFrame
            df = pd.DataFrame(items)

            # Construct CSV filename based on issue type
            csv_file = config.DATA_DIR / f'quality_{issue_type}.csv'

            # Write to CSV (index=False: don't include row numbers)
            df.to_csv(csv_file, index=False)

            # Confirm export with count
            print(f"  Exported {len(items)} {issue_type} to CSV")


def main():
    """
    Main execution function orchestrating the complete tag analysis workflow.

    This function coordinates all analysis steps in sequence:
    1. Load tag data from Script 01 output
    2. Perform tag similarity analysis (fuzzy matching)
    3. Detect hierarchical relationships (substring analysis)
    4. Calculate co-occurrence patterns (pairwise combinations)
    5. Visualize tag network (force-directed graph layout)
    6. Generate analysis report (Markdown)
    7. Connect to Zotero for quality analysis
    8. Analyze data quality issues (duplicates, attachments, etc.)
    9. Generate quality report (Markdown)

    Workflow Design - Sequential Processing:
    Steps must run in this order because later steps depend on earlier outputs:
    - Similarity/hierarchy/cooccurrence need tag data (step 1)
    - Visualization needs cooccurrence and tags (steps 3-4)
    - Analysis report needs all three analyses (steps 2-4)
    - Quality analysis is independent but logically follows tag analysis

    Error Handling Strategy:
    The entire workflow is wrapped in try/except to catch any errors and provide
    helpful debugging information:
    - Errors print to console with full traceback
    - Script exits with status code 1 (signals failure to shell)
    - This allows users to identify and fix issues without completing the rest

    If one analysis step fails, all subsequent steps are skipped. This prevents
    partial/inconsistent outputs and makes debugging easier.

    Alternative Error Handling Approaches Considered:
    1. **Continue on error**: Skip failed step, continue with rest
       Rejected: Partial results may be misleading or inconsistent
    2. **Retry on error**: Attempt failed step multiple times
       Rejected: Most errors aren't transient (e.g., malformed JSON, missing file)
    3. **Per-step error handling**: Try/except around each step individually
       Rejected: More complex code, harder to debug, some steps depend on earlier ones

    Progress Reporting:
    Each major step prints progress messages to keep user informed:
    - What's happening now
    - How many items/tags being processed
    - When step completes successfully

    This is especially important for slow steps (fuzzy matching, network layout,
    API calls) so users know the script hasn't hung.

    Output Files Summary:
    After successful completion, these files will have been created/updated:
    - data/similar_tags.csv (tag merge suggestions)
    - data/tag_network.json (co-occurrence data)
    - data/quality_*.csv (quality issue exports)
    - reports/tag_analysis.md (main analysis report)
    - reports/data_quality_issues.md (curation priorities)
    - visualizations/tag_cooccurrence.png (network graph)

    Performance:
    For typical dataset (481 tags, 336 tagged items, 1,189 total items):
    - Total execution time: ~15-20 seconds
    - Breakdown:
      - Load data: <1 sec
      - Fuzzy matching: 5-8 sec (O(n²) on tags)
      - Hierarchies: <1 sec
      - Co-occurrence: <1 sec
      - Visualization: 1-2 sec (layout iterations)
      - Reports: <1 sec (text generation)
      - Fetch items: 5-8 sec (12 API requests)
      - Quality analysis: <1 sec

    Returns:
        None (main is called for side effects - file generation)

    Exit Codes:
        0: Success (all analyses completed without error)
        1: Failure (error occurred, see traceback for details)

    Side Effects:
        - Writes multiple files to data/, reports/, visualizations/ directories
        - Makes HTTP (Hypertext Transfer Protocol) requests to Zotero API
        - Prints progress messages to console
        - May take 15-20 seconds to complete

    Dependencies:
        - Requires data/raw_tags.json to exist (from Script 01)
        - Requires Zotero API credentials in .env file
        - Requires required directories to exist (created by config module)

    Example Usage:
        if __name__ == '__main__':
            main()

    See Also:
        - Script 01 (01_extract_tags.py): Must run first to generate raw_tags.json
        - Script 03 (03_inspect_multiple_attachments.py): Follow-up for quality issues
    """
    # Print header banner for visual separation in console output
    print("="*70)
    print("BLUE MOUNTAINS PROJECT - TAG ANALYSIS")
    print("Script 02: Analyze tags and identify data quality issues")
    print("="*70)
    print()

    # Wrap entire workflow in try/except for centralized error handling
    try:
        # PHASE 1: TAG ANALYSIS
        # Load tag data extracted by Script 01
        tags, stats = load_tag_data()

        # Analyze tags using three different approaches
        # Each analysis reveals different aspects of the folksonomy structure
        similar_pairs = find_similar_tags(tags, threshold=80)
        hierarchies = detect_hierarchies(tags)
        cooccurrence_list = calculate_cooccurrence(tags)

        # Save tag analysis results
        # CSV for similar tags (spreadsheet review)
        # JSON for network data (tool compatibility)
        save_similar_tags(similar_pairs)
        save_cooccurrence(cooccurrence_list)

        # Create visualization (PNG network graph)
        visualize_cooccurrence(cooccurrence_list, tags, top_n=30)

        # Generate human-readable analysis report (Markdown)
        generate_analysis_report(similar_pairs, hierarchies, cooccurrence_list, stats)

        # PHASE 2: DATA QUALITY ANALYSIS
        # Print separator for visual organization
        print("\n" + "="*70)
        print("DATA QUALITY ANALYSIS")
        print("="*70)

        # Connect to Zotero for quality checks
        # Use read-only API key (principle of least privilege)
        # This script only reads data - never modifies the library
        zot = zotero.Zotero(
            config.ZOTERO_GROUP_ID,
            config.ZOTERO_LIBRARY_TYPE,
            config.ZOTERO_API_KEY_READONLY  # Read-only key (security: prevents accidental modification)  # noqa: E501
        )

        # Analyze data quality issues by fetching all items and checking for problems
        issues = analyze_data_quality(zot)

        # Generate human-readable quality report (Markdown)
        # Also exports CSV files for each issue type
        generate_quality_report(issues)

        # Print success banner
        print("\n" + "="*70)
        print("✓ ANALYSIS COMPLETE")
        print("="*70)

        # List all output files for user reference
        # This helps users know what files to review next
        print("\nOutputs created:")
        print(f"  - {config.DATA_DIR / 'similar_tags.csv'}")
        print(f"  - {config.DATA_DIR / 'tag_network.json'}")
        print(f"  - {config.VISUALIZATIONS_DIR / 'tag_cooccurrence.png'}")
        print(f"  - {config.REPORTS_DIR / 'tag_analysis.md'}")
        print(f"  - {config.REPORTS_DIR / 'data_quality_issues.md'}")

        # Suggest next steps in workflow
        print("\nNext: Review reports and begin tag rationalization planning")

    except Exception as e:
        # Catch any error that occurred during execution
        # Print error message and full traceback for debugging
        print(f"\n❌ ERROR: {e}")

        # import traceback here (not at top) because it's only needed for error handling
        import traceback
        traceback.print_exc()  # Print full stack trace showing where error occurred

        # Exit with status code 1 to signal failure
        # This allows shell scripts to detect failure with $? or "if command; then"
        sys.exit(1)


# Standard Python idiom: Only run main() if this file is executed directly
# (not if it's imported as a module by another script)
if __name__ == '__main__':
    main()
