#!/usr/bin/env python3
"""
Update AMBIGUOUS_TAGS_DECISION_REPORT.md with Trove links for 16 items.
"""

from pathlib import Path
import re

# Trove links mapped to item IDs
TROVE_LINKS = {
    "2.2": "http://nla.gov.au/nla.news-article194117633",
    "2.3": "http://nla.gov.au/nla.news-article188871927",
    "2.9": "http://nla.gov.au/nla.news-article190711837",
    "2.10": "http://nla.gov.au/nla.news-article190711596",
    "2.11": "http://nla.gov.au/nla.news-article188869963",
    "2.12": "http://nla.gov.au/nla.news-article188870884",
    "2.13": "https://trove.nla.gov.au/newspaper/article/190710317",
    "2.14": "http://nla.gov.au/nla.news-article114079710",
    "2.18": "https://trove.nla.gov.au/newspaper/article/194112664",
    "2.23": "http://nla.gov.au/nla.news-article194116072",
    "3.1": "http://nla.gov.au/nla.news-article188871519",
    "3.9": "http://nla.gov.au/nla.news-article194111925",
    "3.16": "http://nla.gov.au/nla.news-article194115698",
    "3.17": "http://nla.gov.au/nla.news-article194118172",
    "3.19": "http://nla.gov.au/nla.news-article218623042",
    "4.11": "http://nla.gov.au/nla.news-article194114685",
}

def main():
    report_path = Path('reports/AMBIGUOUS_TAGS_DECISION_REPORT.md')

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # For each item, find the "need link to trove" pattern and replace with actual link
    for item_id, url in TROVE_LINKS.items():
        # Pattern 1: need link to trove
        pattern1 = rf'(#### Item {item_id}.*?)\*\*DECISION\*\*: _____ \(A-[A-Z]\) (I can\'t tell: provide link to primary source in Trove|need link to trove|need link to Trove|I need the trove link for review|need link to trove source|I need the link to Trove, insufficient context here)'
        replacement1 = rf'\1**Trove**: {url}\n\n**DECISION**: (Pending - see Trove source)'

        content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

        # Pattern 2: For items that already have some context but say "need link"
        pattern2 = rf'(#### Item {item_id}.*?)_Article title:.*?_\n\n\*\*DECISION\*\*: _____ \(A-[A-Z]\) need link to trove'
        replacement2 = rf'\1**Trove**: {url}\n\n**DECISION**: (Pending - see Trove source)'

        content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)

    # Write updated content
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated decision report with {len(TROVE_LINKS)} Trove links")
    print(f"✓ Report path: {report_path}")

if __name__ == '__main__':
    main()
