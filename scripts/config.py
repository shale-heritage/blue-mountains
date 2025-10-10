"""
Configuration Management for Blue Mountains Digital Collection Software

Purpose:
Centralised configuration management for all scripts in the project. This module
loads Application Programming Interface (API) credentials, defines project paths,
and ensures required directories exist. All other scripts import this module to
access configuration constants.

Security Model:
API credentials are stored in a .env file (NEVER committed to Git) and loaded via
the python-dotenv library. This prevents accidental exposure of secret keys in
version control. The .env file is listed in .gitignore to enforce this security
boundary.

API Key Strategy - Principle of Least Privilege:
Following security best practice, we use separate API keys for different access levels:
- Read-only key: For scripts that only extract/analyse data (01-03)
- Read-write key: For future scripts that modify Zotero library (vocabulary publishing)

Using read-only keys for extraction scripts means that if a key is compromised or a
script has bugs, it cannot accidentally modify or delete library data. This implements
the "principle of least privilege" - grant only the permissions actually needed.

To generate separate API keys:
1. Visit https://www.zotero.org/settings/keys
2. Create read-only key:
   - Name: "Blue Mountains - Read Only"
   - Permissions: "Allow library access" → Read Only
   - Select group library: Blue Mountains (2258643)
   - Copy generated key to .env as ZOTERO_API_KEY_READONLY
3. Create read-write key:
   - Name: "Blue Mountains - Read Write"
   - Permissions: "Allow library access" → Read/Write
   - Select group library: Blue Mountains (2258643)
   - Copy generated key to .env as ZOTERO_API_KEY_READWRITE

Backward Compatibility:
For convenience, the legacy ZOTERO_API_KEY variable is still supported. If present
and no specific key is requested, it will be used as a fallback.

Design Decision - Centralised Configuration:
Rather than having each script load its own .env file, we centralise configuration
here. Benefits:
1. Single source of truth for all credentials and paths
2. Consistent validation (all scripts fail early if credentials missing)
3. Easier maintenance (change paths in one place)
4. Testability (can override config in tests)
5. Clear documentation of which scripts need which permissions

Path Management:
We define all project directories as Path objects (pathlib) rather than strings.
Benefits:
- Platform-independent path separators (works on Windows/macOS/Linux)
- Path manipulation methods (.parent, .mkdir(), etc.)
- Type safety (Integrated Development Environment (IDE) autocomplete)

Directory Auto-Creation:
This module creates required directories when imported (at script startup) using
mkdir() with parents=True and exist_ok=True. This ensures scripts can immediately
write outputs without checking if directories exist. We use exist_ok=True to avoid
errors when directories already exist from previous runs.

Adding New Configuration:
1. Add environment variable to .env.example with documentation
2. Load it here with os.getenv('VARIABLE_NAME')
3. Add validation if required (see Zotero validation example)
4. Document the variable in this docstring
5. Document which scripts use it and why

Usage:
    # Import at top of every script
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    import config

    # Access credentials (read-only scripts)
    from pyzotero import zotero
    zot = zotero.Zotero(config.ZOTERO_GROUP_ID,
                       config.ZOTERO_LIBRARY_TYPE,
                       config.ZOTERO_API_KEY_READONLY)

    # Access credentials (read-write scripts - future)
    zot = zotero.Zotero(config.ZOTERO_GROUP_ID,
                       config.ZOTERO_LIBRARY_TYPE,
                       config.ZOTERO_API_KEY_READWRITE)

    # Access paths
    output_file = config.DATA_DIR / 'output.json'
    report_file = config.REPORTS_DIR / 'report.md'

Dependencies:
- python-dotenv: Loads .env file variables into os.environ
- pathlib: Modern path manipulation (Python 3.4+)

Security Notes:
- Never print API keys in logs or console output
- Validate that .env is in .gitignore before committing
- Regenerate API keys if accidentally committed
- Use read-only keys for extraction scripts (01-03)
- Use read-write keys only for scripts that need to modify library

Author: Shawn Ross
Project: Australian Research Council (ARC) Linkage Project LP190100900
         Blue Mountains Shale Mining Communities
Last Updated: 2025-10-09
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# ==========================================
# The .env file should be in the project root (parent of scripts/ directory)
# We use __file__ to get this config.py file's location, then navigate up:
# __file__ = /path/to/blue-mountains/scripts/config.py
# __file__.parent = /path/to/blue-mountains/scripts/
# __file__.parent.parent = /path/to/blue-mountains/ (project root)
env_path = Path(__file__).parent.parent / '.env'

# load_dotenv() reads the .env file and adds variables to os.environ
# This makes them accessible via os.getenv() throughout this module
# dotenv_path parameter specifies exact file location (not just filename)
load_dotenv(dotenv_path=env_path)

# Zotero Configuration
# ====================
# Zotero is a reference management system with a Web API for programmatic access
# This project uses a Zotero group library (shared collaborative collection)
# All newspaper articles and sources are stored there with tags and metadata

# Group library ID (numeric identifier for Blue Mountains project)
# This is publicly visible - it's not a secret, just an identifier
# Find it in the URL: https://www.zotero.org/groups/2258643/...
ZOTERO_GROUP_ID = os.getenv('ZOTERO_GROUP_ID')

# API keys for different access levels (principle of least privilege)
# Read-only key: Used by extraction/analysis scripts (01-03)
# These scripts only retrieve data, never modify the library
ZOTERO_API_KEY_READONLY = os.getenv('ZOTERO_API_KEY_READONLY')

# Read-write key: Used by future vocabulary publishing scripts
# These scripts will write controlled vocabulary tags back to Zotero
ZOTERO_API_KEY_READWRITE = os.getenv('ZOTERO_API_KEY_READWRITE')

# Legacy API key for backward compatibility
# If specific keys aren't set, fall back to this general key
# This allows existing .env files to work without modification
ZOTERO_API_KEY = os.getenv('ZOTERO_API_KEY')

# Library type: 'group' (shared) or 'user' (personal)
# This project uses a group library for collaborative research
# Default to 'group' if not specified in .env
ZOTERO_LIBRARY_TYPE = os.getenv('ZOTERO_LIBRARY_TYPE', 'group')

# Omeka Configuration (for future implementation)
# ===============================================
# Omeka Classic is a digital collections publishing platform
# Phase 4 of this project will publish items from Zotero to Omeka
# These variables are placeholders - not yet used by any scripts

# Omeka API endpoint URL (e.g., https://bluemountains.omeka.net/api)
OMEKA_API_URL = os.getenv('OMEKA_API_URL')

# Omeka API key for authentication
# Generated in Omeka admin panel under API Keys
OMEKA_API_KEY = os.getenv('OMEKA_API_KEY')

# Project Paths
# =============
# All paths are defined as pathlib.Path objects for platform independence
# These paths are relative to PROJECT_ROOT (the repository root directory)

# PROJECT_ROOT is the parent directory of scripts/ (i.e., repository root)
# We use __file__ to get this config.py file's location, then navigate up
# This works regardless of where Python is run from (cwd independence)
PROJECT_ROOT = Path(__file__).parent.parent

# data/ - Machine-readable outputs (JSON, CSV)
# Generated by scripts, used as inputs to other scripts
# Not committed to Git (in .gitignore) - regenerated from Zotero
# Examples: raw_tags.json, tag_frequency.csv, similar_tags.csv
DATA_DIR = PROJECT_ROOT / 'data'

# reports/ - Human-readable reports (Markdown)
# Generated by scripts, intended for project team review
# Not committed to Git (in .gitignore) - regenerated from Zotero
# Examples: tag_summary.md, tag_analysis.md, data_quality_issues.md
REPORTS_DIR = PROJECT_ROOT / 'reports'

# backups/ - Timestamped backups of important data
# Used before major changes (e.g., before tag consolidation in Zotero)
# Not committed to Git (in .gitignore) - local safety net only
# Manually copy important files here before irreversible operations
BACKUPS_DIR = PROJECT_ROOT / 'backups'

# logs/ - Script execution logs for debugging
# Not currently used but prepared for future logging implementation
# Not committed to Git (in .gitignore) - local debugging only
# Future enhancement: Add logging.basicConfig() to write execution logs
LOGS_DIR = PROJECT_ROOT / 'logs'

# visualisations/ - Generated charts and network graphs
# (Portable Network Graphics (PNG), Scalable Vector Graphics (SVG))
# Created by analysis scripts, embedded in reports
# Not committed to Git (in .gitignore) - regenerated from data
# Examples: tag_cooccurrence.png, tag_network.png
VISUALIZATIONS_DIR = PROJECT_ROOT / 'visualizations'

# Ensure all required directories exist
# ======================================
# We create directories when this config module is imported (at script startup)
# This guarantees that scripts can immediately write files without error checking
#
# mkdir() parameters:
#   parents=True:  Create parent directories if needed (like 'mkdir -p' in Unix)
#   exist_ok=True: Don't raise error if directory already exists
#
# This approach uses "ask forgiveness not permission" (AFNP) Python philosophy:
# Rather than checking if directory exists then creating (LBYL - look before you leap),
# we just create and ignore the error if it exists. More concise and thread-safe.
for directory in [DATA_DIR, REPORTS_DIR, BACKUPS_DIR, LOGS_DIR, VISUALIZATIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Validation
# ==========
# We validate critical configuration before any scripts run
# This provides clear error messages at startup rather than cryptic failures later

# Zotero Group ID is REQUIRED for all scripts
# Without this, we don't know which library to access
if not ZOTERO_GROUP_ID:
    raise ValueError(
        "ZOTERO_GROUP_ID not found in .env file\n"
        "Required: ZOTERO_GROUP_ID=2258643\n"
        "See .env.example for setup instructions"
    )

# At least one Zotero API key must be present
# Check for specific keys first, then fall back to legacy key
# This allows flexible configuration while maintaining security
if not ZOTERO_API_KEY_READONLY and not ZOTERO_API_KEY_READWRITE and not ZOTERO_API_KEY:
    raise ValueError(
        "No Zotero API key found in .env file\n"
        "Required: At least one of:\n"
        "  ZOTERO_API_KEY_READONLY (for extraction scripts 01-03)\n"
        "  ZOTERO_API_KEY_READWRITE (for future publishing scripts)\n"
        "  ZOTERO_API_KEY (legacy, works for all scripts)\n"
        "See .env.example for setup instructions\n"
        "Generate keys at: https://www.zotero.org/settings/keys"
    )

# Success confirmation
# Print to console so users know configuration loaded correctly
# We deliberately don't print API keys (security risk - might be logged or screenshotted)
# We also don't print full key even partially (first/last chars) to avoid accidental exposure
print("✓ Configuration loaded successfully")
print(f"  Zotero Group ID: {ZOTERO_GROUP_ID}")
print(f"  Library Type: {ZOTERO_LIBRARY_TYPE}")

# Indicate which API keys are available (without revealing the keys themselves)
if ZOTERO_API_KEY_READONLY:
    print("  Read-only API key: Available")
if ZOTERO_API_KEY_READWRITE:
    print("  Read-write API key: Available")
if ZOTERO_API_KEY and not ZOTERO_API_KEY_READONLY and not ZOTERO_API_KEY_READWRITE:
    print("  Legacy API key: Available (consider splitting into read-only/read-write)")

# Testing This Configuration
# ===========================
# To verify configuration is correct, run this file directly:
#   python scripts/config.py
#
# Expected output:
#   ✓ Configuration loaded successfully
#   Zotero Group ID: 2258643
#   Library Type: group
#   Read-only API key: Available
#   Read-write API key: Available (or Legacy API key message)
#
# If you see ValueError, check your .env file:
#   1. Does .env exist in project root? (not in scripts/ directory)
#   2. Does it contain ZOTERO_GROUP_ID=2258643?
#   3. Does it contain at least one API key variable?
#   4. Is python-dotenv installed? (pip install python-dotenv)
#   5. Are there any typos in variable names? (case-sensitive)
#
# Common issues:
#   - .env in wrong location (should be in project root, not scripts/)
#   - Extra spaces around = sign (should be KEY=value not KEY = value)
#   - Quotes around values (not needed: KEY=abc123 not KEY="abc123")
#   - Missing .env file entirely (copy from .env.example)
