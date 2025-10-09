# Project Standards

## Spelling and Localisation

- Always use UK/Australian English spelling (colour, behaviour, organisation, centre, analyse, optimise, etc.)
- Apply UK/Australian spelling to all documentation, code comments, and file names
- Convert US spellings to UK/Australian equivalents when editing existing files

## Code Standards

- All code (e.g., python) and documentation (e.g., markdown) files must pass linting validation
- Before committing  files, check for linting issues using the IDE diagnostics
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

## Git Commit Messages

- Use UK/Australian spelling in commit messages
- Include informative brief and detailed commit messages with context
- Always include the Claude Code co-authorship footer
