"""
Configuration file for Blue Mountains project.
Loads API credentials and settings from environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Zotero Configuration
ZOTERO_GROUP_ID = os.getenv('ZOTERO_GROUP_ID')
ZOTERO_API_KEY = os.getenv('ZOTERO_API_KEY')
ZOTERO_LIBRARY_TYPE = os.getenv('ZOTERO_LIBRARY_TYPE', 'group')

# Omeka Configuration (to be added later)
OMEKA_API_URL = os.getenv('OMEKA_API_URL')
OMEKA_API_KEY = os.getenv('OMEKA_API_KEY')

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
REPORTS_DIR = PROJECT_ROOT / 'reports'
BACKUPS_DIR = PROJECT_ROOT / 'backups'
LOGS_DIR = PROJECT_ROOT / 'logs'
VISUALIZATIONS_DIR = PROJECT_ROOT / 'visualizations'

# Ensure directories exist
for directory in [DATA_DIR, REPORTS_DIR, BACKUPS_DIR, LOGS_DIR, VISUALIZATIONS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Validation
if not ZOTERO_GROUP_ID or not ZOTERO_API_KEY:
    raise ValueError("Zotero credentials not found in .env file")

print(f"✓ Configuration loaded successfully")
print(f"  Zotero Group ID: {ZOTERO_GROUP_ID}")
print(f"  Library Type: {ZOTERO_LIBRARY_TYPE}")
