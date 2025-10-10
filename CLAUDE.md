# Project Standards

## Spelling and Localisation

- Always use UK/Australian English spelling (colour, behaviour, organisation, centre, analyse, optimise, etc.)
- Apply UK/Australian spelling to all documentation, code comments, and file names
- Convert US spellings to UK/Australian equivalents when editing existing files

## Code Standards

- All code (e.g., python) and documentation (e.g., markdown) files must pass linting validation
- Before committing files, check for linting issues using the IDE diagnostics
- Common markdown rules to follow:
  - MD022: Blank lines around headings
  - MD031: Blank lines around fenced code blocks
  - MD032: Blank lines around lists
  - MD040: Language specifiers for code blocks (use ```text for plain text)
  - Other markdown rules that might compromise readability can be disabled, but check with me first.
- Fix all linting warnings before committing
- Always include verbose code comments sufficient that someone unfamiliar with the code can understand it
  - Scripts should be well described in a header comment block
  - Functions should have docstrings describing their purpose, parameters, and return values
  - Inline comments should explain non-obvious code sections

## Documentation Standards

- **Expand acronyms on first usage** in each file (module docstrings, markdown documents)
  - Example: "Getty Art & Architecture Thesaurus (AAT)" not just "Getty AAT"
  - Example: "Research Vocabularies Australia (RVA)" not just "RVA"
  - Subsequent uses in the same file can use the acronym alone
  - Common acronyms in this project:
    - AAT: Art & Architecture Thesaurus (Getty vocabulary)
    - TGN: Thesaurus of Geographic Names (Getty vocabulary)
    - RVA: Research Vocabularies Australia
    - SKOS: Simple Knowledge Organisation System
    - FAIR: Findable, Accessible, Interoperable, Reusable
    - FAIR4RS: FAIR Principles for Research Software
    - API: Application Programming Interface
    - CSV: Comma-Separated Values
    - JSON: JavaScript Object Notation
    - PDF: Portable Document Format
- Use clear, accessible language appropriate for digital humanities researchers
- Provide context and rationale for technical decisions
- Include examples where they aid understanding

## Git Commit Messages

- Use UK/Australian spelling in commit messages
- Include informative brief and detailed commit messages with context
- Always include the Claude Code co-authorship footer
