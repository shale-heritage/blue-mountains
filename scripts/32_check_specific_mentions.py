#!/usr/bin/env python3
"""Check for specific alcohol mentions in items 1, 7, 9."""

import sys
from pathlib import Path
from html.parser import HTMLParser
import re

sys.path.append(str(Path(__file__).parent))
import config

from pyzotero import zotero

class MLStripper(HTMLParser):
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
    stripper = MLStripper()
    stripper.feed(html)
    return stripper.get_data()

zot = zotero.Zotero(config.ZOTERO_GROUP_ID, config.ZOTERO_LIBRARY_TYPE, config.ZOTERO_API_KEY_READONLY)

items = zot.items(tag='Alcohol')

for idx, item in enumerate(items, 1):
    title = item['data'].get('title', '[No Title]')

    # Get full text
    children = zot.children(item['key'])
    notes = [child for child in children if child['data'].get('itemType') == 'note']
    full_text = ''
    for note in notes:
        note_content = note['data'].get('note', '')
        full_text += strip_html(note_content) + '\n'

    text_lower = full_text.lower()

    # Check for specific terms
    if idx == 1:  # Rape case
        print(f"{idx}. {title[:40]}")
        print(f"  - grog mentioned: {'grog' in text_lower}")
        if 'grog' in text_lower:
            matches = re.finditer(r'.{0,40}grog.{0,40}', text_lower, re.IGNORECASE)
            for m in list(matches)[:2]:
                print(f"    Context: {m.group()}")
        print()
    elif idx == 7:  # Katoomba Court Oct 1892
        print(f"{idx}. {title[:40]}")
        print(f"  - whisky mentioned: {'whisk' in text_lower}")
        if 'whisk' in text_lower:
            matches = re.finditer(r'.{0,40}whisk[ye]y.{0,40}', text_lower, re.IGNORECASE)
            for m in list(matches)[:3]:
                print(f"    Context: {m.group()}")
        print()
    elif idx == 9:  # Katoomba Court March 1893
        print(f"{idx}. {title[:40]}")
        print(f"  - whisky mentioned: {'whisk' in text_lower}")
        print(f"  - gin mentioned: {'gin' in text_lower}")
        if 'whisk' in text_lower:
            matches = re.finditer(r'.{0,40}whisk[ye]y.{0,40}', text_lower, re.IGNORECASE)
            for m in list(matches)[:2]:
                print(f"    Whisky: {m.group()}")
        if 'gin' in text_lower:
            matches = re.finditer(r'.{0,40}\bgin\b.{0,40}', text_lower, re.IGNORECASE)
            for m in list(matches)[:2]:
                print(f"    Gin: {m.group()}")
        print()
