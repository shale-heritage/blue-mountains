# Contributing to Blue Mountains Digital Collection Software

Thank you for considering contributing to this research software project!

This document provides guidelines for contributing code, documentation, and other improvements to the Blue Mountains Shale Mining Communities Digital Collection Software.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Code Standards](#code-standards)
- [Documentation Standards](#documentation-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Questions and Support](#questions-and-support)

---

## Code of Conduct

This project is part of an academic research initiative. All contributors are expected to:

- Be respectful and professional in all interactions
- Provide constructive feedback
- Focus on what is best for the project and research community
- Show empathy towards other community members
- Accept constructive criticism gracefully

**Unacceptable behaviour** includes harassment, discriminatory language, personal attacks, trolling, or unprofessional conduct.

**Enforcement:** Violations should be reported to <shawn@faims.edu.au>. The project team will review and respond to all complaints.

---

## Getting Started

### Prerequisites

- **Python 3.12 or higher**
- **Git** for version control
- **Zotero API credentials** (for testing tag extraction)
- Familiarity with Python, pandas, and JSON data formats
- Understanding of digital humanities workflows (helpful but not required)

### Installation

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/blue-mountains.git
   cd blue-mountains
   ```

3. Add upstream remote:
   ```bash
   git remote add upstream <https://github.com/shale-heritage/blue-mountains>.git
   ```

4. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

7. Verify installation:
   ```bash
   python scripts/config.py
   ```

---

## Development Environment

### Recommended Tools

- **IDE/Editor:** VS Code, PyCharm, or vim with Python extensions
- **Linting:** flake8 or pylint for Python, markdownlint for Markdown
- **Testing:** pytest (when tests are added)
- **JSON Tools:** jq for JSON validation and query
- **Git Client:** Command-line git or GitHub Desktop

### VS Code Extensions

If using VS Code, install these extensions:

- Python (Microsoft)
- Pylance (Microsoft)
- markdownlint (David Anson)
- Python Docstring Generator
- GitLens

### Project Structure

```text
blue-mountains/
├── scripts/              # Python scripts for data processing
│   ├── config.py        # Configuration management
│   ├── 01_extract_tags.py
│   ├── 02_analyze_tags.py
│   └── 03_inspect_multiple_attachments.py
├── data/                # Generated data files (gitignored)
├── reports/             # Generated reports (gitignored)
├── docs/                # Documentation
├── planning/            # Project planning documents
├── visualisations/      # Generated charts (gitignored)
├── gazetteers/          # Gazetteer data files
├── references/          # BibTeX citations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── CITATION.cff         # Software citation metadata
├── codemeta.json        # Software metadata
├── CHANGELOG.md         # Version history
└── README.md            # Project overview
```

---

## Code Standards

### Spelling and Localisation

**CRITICAL: Always use UK/Australian English spelling in all code, comments, and documentation.**

**Common conversions:**

| US English | UK/Australian English |
|------------|----------------------|
| color | colour |
| behavior | behaviour |
| organization | organisation |
| center | centre |
| analyze | analyse |
| optimize | optimise |
| license (noun) | licence (noun) |
| license (verb) | license (verb) |
| fulfill | fulfil |
| traveled | travelled |

**Tools:**

- Use spellchecker with UK English dictionary
- VS Code: Set `"cSpell.language": "en-GB"`
- Configure IDE to highlight US spellings

**Rationale:** This project is based in Australia and follows Australian academic standards. Consistency in spelling is essential for professionalism and FAIR principles.

---

### Python Code Style

Follow **PEP 8** with these project-specific guidelines:

#### General Guidelines

- **Line Length:** 100 characters maximum (slightly longer than PEP 8's 79 for readability)
- **Indentation:** 4 spaces (no tabs)
- **Encoding:** UTF-8 for all Python files
- **Imports:** Standard library, third-party, local (separated by blank lines)
- **Naming Conventions:**
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

#### Import Order

```python
# Standard library
import json
import sys
from pathlib import Path
from datetime import datetime

# Third-party packages
import pandas as pd
from pyzotero import zotero

# Local modules
import config
```

#### Documentation Requirements

**All functions must have detailed docstrings** using this format:

```python
def analyse_tag_similarity(tags_dict, threshold=80):
    """
    Identify similar tags using fuzzy string matching for consolidation.

    This function uses the Levenshtein Distance algorithm (via fuzzywuzzy
    library) to calculate similarity scores between all tag pairs. Pairs
    exceeding the threshold are flagged as potential duplicates requiring
    manual review for consolidation.

    The algorithm compares tags pairwise, which has O(n²) complexity.
    For large tag sets (>1000), this may take several minutes. Progress
    is displayed for long-running operations.

    Parameters:
        tags_dict (dict): Dictionary of tags from raw_tags.json format,
                         where keys are tag names and values are dicts
                         containing 'count', 'items', and 'item_titles'.
                         Example: {'Mining': {'count': 32, 'items': [...]}}
        threshold (int): Minimum similarity score (0-100) to flag a pair
                        as similar. Default is 80. Higher values (90+)
                        reduce false positives but may miss variants.
                        Lower values (70-79) catch more variants but
                        require more manual review.

    Returns:
        list: List of dictionaries, each containing:
              - 'tag1' (str): First tag in pair
              - 'tag2' (str): Second tag in pair
              - 'similarity' (float): Similarity score (0-100)
              - 'count1' (int): Usage count of tag1
              - 'count2' (int): Usage count of tag2
              - 'suggested_merge' (str): Recommended target tag (higher count)

    Raises:
        ValueError: If tags_dict is empty or malformed
        TypeError: If threshold is not an integer

    Example:
        >>> tags = {'Mining': {'count': 32}, 'Mine': {'count': 8}}
        >>> results = analyse_tag_similarity(tags, threshold=80)
        >>> print(results[0])
        {'tag1': 'Mine', 'tag2': 'Mining', 'similarity': 83.3,
         'count1': 8, 'count2': 32, 'suggested_merge': 'Mining'}

    See Also:
        - fuzzywuzzy.fuzz.ratio: Underlying similarity algorithm
        - 02_analyze_tags.py: Full implementation context

    Note:
        This function uses python-Levenshtein for performance (100x speedup
        vs pure Python). Ensure it's installed: pip install python-Levenshtein
    """
    # Validate input
    if not tags_dict:
        raise ValueError("tags_dict cannot be empty")

    if not isinstance(threshold, int) or not 0 <= threshold <= 100:
        raise TypeError("threshold must be an integer between 0 and 100")

    # Implementation...
```

**Docstring sections (in order):**

1. **Brief summary** (one line)
2. **Detailed description** (2-4 paragraphs explaining context and approach)
3. **Parameters:** Type, description, example values, constraints
4. **Returns:** Type, structure, example
5. **Raises:** Exceptions and when they occur
6. **Example:** Working code snippet showing usage
7. **See Also:** (optional) Related functions, documentation
8. **Note:** (optional) Performance tips, caveats, dependencies

#### Inline Comments

**Comment the "why," not the "what".**

**Good examples:**

```python
# Use defaultdict to avoid KeyError when counting co-occurrences
# This is more Pythonic than checking if key exists before incrementing
co_occurrence_counts = defaultdict(int)

# Zotero API limits responses to 100 items, so we paginate
# Larger batches cause timeouts; smaller batches are inefficient
batch_size = 100
```

**Bad examples:**

```python
# Increment counter
count += 1  # DON'T: States the obvious

# Loop through items
for item in items:  # DON'T: Restates code
```

**When to comment:**

- Non-obvious algorithms or logic
- Performance optimisations
- Workarounds for bugs or limitations
- Complex data transformations
- API-specific requirements (e.g., Zotero pagination)
- Technical terms or domain-specific concepts

---

### Code Quality and Linting

**Before committing code, ensure it passes linting.**

#### Python Linting

```bash
# Install linters (optional, not in requirements.txt by default)
pip install flake8 pylint

# Run flake8
flake8 scripts/*.py --max-line-length=100

# Run pylint
pylint scripts/*.py
```

**Linting Rules:**

- Fix all errors
- Address warnings where reasonable
- Disable specific rules with inline comments only when justified:
  ```python
  # pylint: disable=line-too-long
  long_string = "This is an exceptionally long string that cannot be reasonably broken across lines without harming readability..."
  # pylint: enable=line-too-long
  ```

#### Markdown Linting

**All Markdown files must pass linting** (rules from CLAUDE.md):

- **MD022:** Blank lines around headings
- **MD031:** Blank lines around fenced code blocks
- **MD032:** Blank lines around lists
- **MD040:** Language specifiers for code blocks

**Installation:**

```bash
# Install markdownlint (requires Node.js/npm)
npm install -g markdownlint-cli

# Or use VS Code extension: "markdownlint" by David Anson
```

**Run linter:**

```bash
markdownlint '**/*.md' --ignore node_modules --ignore venv
```

**Fix common issues:**

````markdown
<!-- WRONG: No blank lines around heading -->
Some text
## Heading
More text

<!-- CORRECT: Blank lines around heading -->
Some text

## Heading

More text

<!-- WRONG: No language specified -->
```
code here
```

<!-- CORRECT: Language specified -->
```python
code here
```
````

---

## Documentation Standards

### README Files

- Each major directory should have a README.md explaining its contents
- Use clear section headings (##)
- Include examples where helpful
- Keep language accessible to digital humanities researchers

### Code Comments

- **Header comments** for all scripts explaining purpose, inputs, outputs
- **Function docstrings** (see Python Code Style above)
- **Inline comments** for complex logic (see Python Code Style above)

### Spelling

- **All documentation uses UK/Australian English** (same as code)
- Exceptions: Quoted text, proper nouns, code identifiers

---

## Commit Message Guidelines

### Format

```text
Brief summary of changes in imperative mood (50 chars max)

Optional detailed explanation of what and why (not how).
Wrap at 72 characters. Separate from summary with blank line.

- Use bullet points for multiple changes
- Reference issue numbers: Fixes #42, Relates to #37
- Explain breaking changes clearly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Summary Line Rules

- **Imperative mood:** "Add feature" (not "Added feature" or "Adds feature")
- **No period** at end
- **50 characters maximum**
- **UK/Australian spelling**
- **Capitalise** first word

**Examples:**

```text
✓ Add Getty AAT vocabulary mapping to analyse script
✓ Fix Unicode encoding error in tag export
✓ Update gazetteer comparison with Composite Gazetteer recommendation
✗ Fixed a bug (too vague, past tense)
✗ updated the readme file (not capitalised, past tense)
```

### Commit Body

- Explain **what** changed and **why** (not how - that's in the code)
- Wrap lines at 72 characters
- Use UK/Australian spelling
- Reference related issues/PRs with `#number`

**Example commit:**

```text
Add hierarchical tag relationship detection

Extends the tag analysis script to identify parent-child relationships
between tags using substring matching and co-occurrence patterns. This
helps build the hierarchical vocabulary structure needed for SKOS
export to Research Vocabularies Australia.

Algorithm detects:
- Exact substring matches (e.g., "Mining" contains "Mine")
- High co-occurrence rates (>80% of child's items also have parent)

Outputs written to data/tag_hierarchies.csv for manual review.

Relates to #12 (RVA vocabulary publishing)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Pull Request Process

### Before Submitting

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following code standards above

4. **Test your changes:**
   ```bash
   # Run the modified script
   python scripts/your_script.py

   # Verify outputs
   ls -l data/

   # Check for errors
   cat logs/your_script.log
   ```

5. **Lint your code:**
   ```bash
   flake8 scripts/your_script.py --max-line-length=100
   markdownlint '**/*.md' --ignore node_modules --ignore venv
   ```

6. **Update documentation:**
   - Add docstrings to new functions
   - Update README.md if adding features
   - Update CHANGELOG.md under [Unreleased]
   - Update relevant docs/ files

7. **Commit your changes** (see Commit Message Guidelines above)

8. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting the PR

1. Go to <https://github.com/shale-heritage/blue-mountains>
2. Click "Pull Requests" → "New Pull Request"
3. Select your fork and feature branch
4. Fill in the PR template:

```markdown
## Description

Brief summary of changes (1-2 sentences)

## Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Motivation and Context

Why is this change needed? What problem does it solve?
If it fixes an open issue, link to the issue here.

## Testing

How did you test these changes? Provide specific steps:

1. Run script X with input Y
2. Verify output Z matches expected result
3. Check log files for errors

## Checklist

- [ ] Code follows project style guidelines (PEP 8, UK spelling)
- [ ] All functions have comprehensive docstrings
- [ ] Code passes linting (flake8, markdownlint)
- [ ] Documentation updated (README, CHANGELOG, docs/)
- [ ] Tested on Python 3.12
- [ ] Commit messages follow guidelines
- [ ] No merge conflicts with main branch

## Screenshots (if applicable)

Include screenshots of visualisations, reports, or output files
```

1. Submit the PR

### PR Review Process

- **Maintainers will review** within 1-2 weeks
- **Be responsive** to feedback and requested changes
- **Discussion is encouraged** – PRs are a learning opportunity
- **CI/CD checks** must pass (when implemented)
- **At least one approval** required before merging

---

## Reporting Issues

### Before Creating an Issue

1. **Search existing issues:** Your issue may already be reported
2. **Try latest version:** Update dependencies and retry
3. **Check documentation:** Review README and docs/ folder
4. **Verify environment:** Ensure Python 3.12+, correct API keys

### Issue Template

```markdown
## Description

Clear and concise description of the issue.

## Steps to Reproduce

1. Run script '...'
2. With input '...'
3. See error '...'

## Expected Behaviour

What you expected to happen.

## Actual Behaviour

What actually happened. Include error messages and logs.

## Environment

- OS: [e.g., Ubuntu 22.04, macOS 14.0, Windows 11]
- Python version: [e.g., 3.12.1]
- Dependencies: [output of `pip freeze`]
- Script: [which script failed]

## Additional Context

Screenshots, log files, data samples (anonymised if necessary)
```

### Issue Labels

Maintainers will add labels:

- `bug` – Something isn't working
- `enhancement` – New feature or improvement
- `documentation` – Documentation improvements
- `good first issue` – Suitable for newcomers
- `help wanted` – Extra attention needed
- `question` – Further information requested

---

## Questions and Support

**For project-specific questions:**

- **Email:** <shawn@faims.edu.au>
- **GitHub Discussions:** (when enabled)

**For general support:**

- **Zotero API:** <https://www.zotero.org/support/dev/web_api/v3/start>
- **Python:** <https://docs.python.org/3/>
- **pandas:** <https://pandas.pydata.org/docs/>
- **FAIR4RS:** <https://www.rd-alliance.org/groups/fair-4-research-software-fair4rs-wg>

---

## Licence

By contributing to this project, you agree that your contributions will be licensed under:

- **Code:** Apache License 2.0 (same as project)
- **Documentation:** Creative Commons Attribution 4.0 International (CC-BY-4.0)

See [LICENSE](LICENSE) (code) and [LICENSE-docs](LICENSE-docs) (documentation) for details.

---

## Acknowledgements

Thank you for contributing to research software and helping advance digital humanities scholarship!

This project is supported by the Australian Research Council Linkage Project scheme (grant LP190100900).

---

Last updated: 2025-10-09
