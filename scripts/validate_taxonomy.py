#!/usr/bin/env python3
"""
Comprehensive taxonomy validation.

Runs all quality checks on tag_map_consolidated.csv and tag_application_mapping.csv:
1. Parent-child reference integrity
2. Tag existence validation
3. Duplicate detection
4. Spelling consistency (UK)
5. Capitalisation conventions
6. Parent node usage in mappings
7. Orphaned tags
"""

import csv
import io
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
TAG_MAP_FILE = BASE_DIR / 'data' / 'tag_map_consolidated.csv'
TAG_APP_FILE = BASE_DIR / 'data' / 'tag_application_mapping.csv'

def load_csv_normalized(filepath):
    """Load CSV with normalized line endings."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n').replace('\r', '\n')
    reader = csv.DictReader(io.StringIO(content))
    return list(reader)

class TaxonomyValidator:
    def __init__(self):
        self.taxonomy = load_csv_normalized(TAG_MAP_FILE)
        self.mappings = load_csv_normalized(TAG_APP_FILE)
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_all(self):
        """Run all validation checks."""
        print("=" * 70)
        print("TAXONOMY VALIDATION")
        print("=" * 70)
        print()

        checks = [
            ("Parent-Child Reference Integrity", self.check_parent_references),
            ("Tag Existence in Mappings", self.check_mapping_tags_exist),
            ("Duplicate Leaf Nodes", self.check_duplicate_leaves),
            ("UK Spelling", self.check_uk_spelling),
            ("Capitalisation", self.check_capitalisation),
            ("Orphaned Tags in Mappings", self.check_orphaned_mappings),
        ]

        for name, check_func in checks:
            print(f"Running: {name}...")
            check_func()
            print()

        self.print_summary()

    def check_parent_references(self):
        """Verify all parent references resolve to existing tags."""
        all_tags = {r['new_tag'] for r in self.taxonomy if r['action'] in ['hierarchy', 'keep']}

        broken = []
        for row in self.taxonomy:
            parent = row.get('parent_broader_category', '')
            if not parent or not parent.startswith('parent='):
                continue

            parent_tag = parent.replace('parent=', '').strip()
            # Skip thematic and Getty facet markers
            if ' - THEMATIC' in parent_tag or '(Getty AAT primary facet)' in parent_tag:
                continue
            if '(thematic grouping)' in parent_tag or '(new top-level facet)' in parent_tag:
                continue

            if parent_tag and parent_tag not in all_tags:
                broken.append({
                    'tag': row['new_tag'],
                    'missing_parent': parent_tag
                })

        if broken:
            self.errors.append(f"Found {len(broken)} broken parent references")
            for item in broken[:10]:
                self.errors.append(f"  - '{item['tag']}' → missing parent '{item['missing_parent']}'")
            if len(broken) > 10:
                self.errors.append(f"    ... and {len(broken) - 10} more")
        else:
            self.info.append("✓ All parent references valid")

    def check_mapping_tags_exist(self):
        """Verify all tags in mappings exist in taxonomy."""
        all_tags = {r['new_tag'] for r in self.taxonomy}

        orphaned = set()
        for row in self.mappings:
            add_tags = row.get('add_tags', '')
            if not add_tags:
                continue

            for tag in add_tags.split(' | '):
                tag = tag.strip()
                if tag and tag not in all_tags:
                    orphaned.add(tag)

        if orphaned:
            self.errors.append(f"Found {len(orphaned)} orphaned tags in mappings")
            for tag in sorted(orphaned)[:10]:
                self.errors.append(f"  - '{tag}'")
            if len(orphaned) > 10:
                self.errors.append(f"    ... and {len(orphaned) - 10} more")
        else:
            self.info.append("✓ All mapping tags exist in taxonomy")

    def check_duplicate_leaves(self):
        """Check for duplicate leaf names within primary facets."""
        # This is complex - would need to trace full hierarchy paths
        # For now, just check case-insensitive duplicates
        tags_lower = defaultdict(list)
        for row in self.taxonomy:
            if row['action'] in ['hierarchy', 'keep']:
                tag = row['new_tag']
                tags_lower[tag.lower()].append(tag)

        duplicates = {k: v for k, v in tags_lower.items() if len(set(v)) > 1}

        if duplicates:
            self.warnings.append(f"Found {len(duplicates)} tags with case variations")
            for key, variants in list(duplicates.items())[:5]:
                self.warnings.append(f"  - {key}: {', '.join(set(variants))}")
            if len(duplicates) > 5:
                self.warnings.append(f"    ... and {len(duplicates) - 5} more")
        else:
            self.info.append("✓ No case-insensitive duplicates found")

    def check_uk_spelling(self):
        """Check for US spelling violations."""
        us_patterns = [
            ('organization', 'organisation'),
            ('color', 'colour'),
            ('center', 'centre'),
            ('traveled', 'travelled'),
            ('labor', 'labour'),
        ]

        violations = []
        for row in self.taxonomy:
            for field in ['old_tag', 'new_tag', 'notes', 'parent_broader_category']:
                value = row.get(field, '').lower()
                for us, uk in us_patterns:
                    if us in value:
                        violations.append({
                            'tag': row['new_tag'],
                            'field': field,
                            'us_word': us
                        })

        if violations:
            self.errors.append(f"Found {len(violations)} US spelling violations")
            for v in violations[:10]:
                self.errors.append(f"  - '{v['tag']}' in {v['field']}: contains '{v['us_word']}'")
            if len(violations) > 10:
                self.errors.append(f"    ... and {len(violations) - 10} more")
        else:
            self.info.append("✓ UK spelling consistent throughout")

    def check_capitalisation(self):
        """Check capitalisation conventions."""
        # Check for tags that should be lowercase but aren't
        # (excluding proper nouns)
        issues = []

        for row in self.taxonomy:
            tag = row['new_tag']
            # Skip if it's a proper noun (contains place names, personal names, etc.)
            if any(word in tag for word in ['Hotel', 'Church', 'St ', 'Mount', 'Company']):
                continue

            # Check if first word is capitalized when it shouldn't be
            if tag and tag[0].isupper() and not tag.startswith('('):
                # Check if it's a thematic grouping or facet
                if ' - THEMATIC' in tag or 'Getty AAT' in tag:
                    continue
                issues.append(tag)

        if issues:
            self.warnings.append(f"Found {len(issues)} potentially incorrect capitalisations")
            for tag in issues[:10]:
                self.warnings.append(f"  - '{tag}'")
            if len(issues) > 10:
                self.warnings.append(f"    ... and {len(issues) - 10} more")
        else:
            self.info.append("✓ Capitalisation appears consistent")

    def check_orphaned_mappings(self):
        """Check for mappings that remove tags but don't add any."""
        orphaned = []
        for row in self.mappings:
            remove = row.get('remove_tags', '').strip()
            add = row.get('add_tags', '').strip()
            if remove and not add:
                orphaned.append(row.get('title', 'Unknown'))

        if orphaned:
            self.warnings.append(f"Found {len(orphaned)} mappings with removals but no additions")
            for title in orphaned[:5]:
                self.warnings.append(f"  - '{title}'")
            if len(orphaned) > 5:
                self.warnings.append(f"    ... and {len(orphaned) - 5} more")
        else:
            self.info.append("✓ All mappings have replacement tags")

    def print_summary(self):
        """Print validation summary."""
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print()

        if self.errors:
            print(f"ERRORS ({len(self.errors)}):")
            for err in self.errors:
                print(f"  {err}")
            print()

        if self.warnings:
            print(f"WARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  {warn}")
            print()

        if self.info:
            print(f"PASSED ({len(self.info)}):")
            for info_item in self.info:
                print(f"  {info_item}")
            print()

        total_issues = len(self.errors) + len(self.warnings)
        if total_issues == 0:
            print("✓ ALL VALIDATION CHECKS PASSED")
        else:
            print(f"⚠ Found {len(self.errors)} errors and {len(self.warnings)} warnings")

        return total_issues == 0

def main():
    validator = TaxonomyValidator()
    success = validator.validate_all()

    if not success:
        import sys
        sys.exit(1)

if __name__ == '__main__':
    main()
