#!/usr/bin/env python3
"""
Analyse the Blue Mountains Railway Tourist Guide PDF.

Extracts:
1. Description of contents
2. All text content
3. List of place names mentioned
4. Any tables or structured data
"""

import re
from pathlib import Path

import pdfplumber

PDF_PATH = Path("data/pdfs/blue-mountains-railway-guide-1894.pdf")
OUTPUT_DIR = Path("reports")


def extract_place_names(text):
    """
    Extract potential place names from text.
    Looks for capitalized words and common place name patterns.
    """
    # Common place name patterns in Blue Mountains region
    place_patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Falls|Valley|Creek|Pass|Station|Point|Lookout|Hotel|Mine|Plateau|Ridge))\b',
        r'\b(?:Mount|Mt|Mount Victoria|Katoomba|Leura|Wentworth|Blackheath|Megalong|Hartley|Lithgow)\b(?:\s+[A-Z][a-z]+)*',
    ]

    places = set()
    for pattern in place_patterns:
        matches = re.findall(pattern, text)
        places.update(matches)

    return sorted(places)


def analyse_pdf():
    """Main analysis function."""
    print("="*80)
    print("BLUE MOUNTAINS RAILWAY TOURIST GUIDE - ANALYSIS")
    print("="*80)
    print()

    if not PDF_PATH.exists():
        print(f"Error: PDF not found at {PDF_PATH}")
        return

    print(f"Analysing: {PDF_PATH}")
    print(f"File size: {PDF_PATH.stat().st_size:,} bytes")
    print()

    # Open PDF
    with pdfplumber.open(PDF_PATH) as pdf:
        num_pages = len(pdf.pages)
        print(f"Total pages: {num_pages}")
        print()

        # Extract text from all pages
        print("Extracting text from all pages...")
        all_text = ""
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                all_text += f"\n--- Page {i} ---\n{text}\n"

            # Show progress
            if i % 5 == 0 or i == num_pages:
                print(f"  Processed {i}/{num_pages} pages")

        print()

        # Get first page for description
        first_page = pdf.pages[0]
        first_page_text = first_page.extract_text() or ""

        # Try to extract image info
        print("Document structure:")
        print(f"  First page dimensions: {first_page.width:.1f} x {first_page.height:.1f} pts")

        # Check for images
        has_images = False
        for page in pdf.pages[:3]:  # Check first 3 pages
            if page.images:
                has_images = True
                break

        if has_images:
            print(f"  Contains images: Yes")
        else:
            print(f"  Contains images: Checking...")

        print()

        # Extract place names
        print("Extracting place names...")
        places = extract_place_names(all_text)
        print(f"Found {len(places)} potential place names")
        print()

        # Check for tables
        print("Checking for tables...")
        tables_found = 0
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                tables_found += len(tables)

        print(f"Found {tables_found} tables")
        print()

        # Save outputs
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # Save full text
        text_output = OUTPUT_DIR / "railway-guide-1894-full-text.txt"
        with open(text_output, 'w', encoding='utf-8') as f:
            f.write("BLUE MOUNTAINS RAILWAY TOURIST GUIDE (1894)\n")
            f.write("="*80 + "\n\n")
            f.write(f"Total pages: {num_pages}\n")
            f.write(f"Extracted: {len(all_text)} characters\n\n")
            f.write(all_text)

        print(f"✓ Saved full text: {text_output}")

        # Save place names
        places_output = OUTPUT_DIR / "railway-guide-1894-place-names.txt"
        with open(places_output, 'w', encoding='utf-8') as f:
            f.write("PLACE NAMES IN BLUE MOUNTAINS RAILWAY TOURIST GUIDE (1894)\n")
            f.write("="*80 + "\n\n")
            f.write(f"Total unique places found: {len(places)}\n\n")
            for i, place in enumerate(places, 1):
                f.write(f"{i:3d}. {place}\n")

        print(f"✓ Saved place names: {places_output}")

        # Create summary report
        summary_output = OUTPUT_DIR / "railway-guide-1894-summary.md"
        with open(summary_output, 'w', encoding='utf-8') as f:
            f.write("# Blue Mountains Railway Tourist Guide (1894) - Analysis Summary\n\n")

            f.write("## Document Description\n\n")
            f.write(f"**Format:** PDF with {num_pages} pages\n\n")
            f.write(f"**File Size:** {PDF_PATH.stat().st_size:,} bytes ({PDF_PATH.stat().st_size/1024/1024:.1f} MB)\n\n")
            f.write(f"**Content Type:** {'Text and images' if has_images else 'Primarily text'}\n\n")

            if first_page_text:
                f.write("**First Page Content:**\n\n")
                # Get first 500 chars
                excerpt = first_page_text[:500].strip()
                f.write(f"```\n{excerpt}\n[...]\n```\n\n")

            f.write(f"## Contents\n\n")
            f.write(f"- **Total pages:** {num_pages}\n")
            f.write(f"- **Tables found:** {tables_found}\n")
            f.write(f"- **Text extracted:** {len(all_text):,} characters\n")
            f.write(f"- **Place names identified:** {len(places)}\n\n")

            f.write("## Place Names\n\n")
            if places:
                f.write("The following locations are mentioned in the guide:\n\n")
                # Show first 50 places in summary
                for place in places[:50]:
                    f.write(f"- {place}\n")
                if len(places) > 50:
                    f.write(f"\n... and {len(places) - 50} more (see full list in railway-guide-1894-place-names.txt)\n")
            else:
                f.write("No place names automatically extracted (may require manual review of full text)\n")

            f.write("\n## Files Generated\n\n")
            f.write(f"- `{text_output.name}` - Complete text extraction\n")
            f.write(f"- `{places_output.name}` - List of all place names\n")
            f.write(f"- `{summary_output.name}` - This summary\n")

        print(f"✓ Saved summary: {summary_output}")
        print()

        print("="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print()
        print("Key findings:")
        print(f"  - {num_pages} page document")
        print(f"  - {len(places)} place names identified")
        print(f"  - {tables_found} tables found")
        print(f"  - {len(all_text):,} characters of text extracted")
        print()
        print(f"Review the full outputs in {OUTPUT_DIR}/")


if __name__ == "__main__":
    analyse_pdf()
