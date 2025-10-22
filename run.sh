#!/usr/bin/env bash
# ==============================================================================
# Blue Mountains Project - Script Runner
# ==============================================================================
#
# Purpose:
#   Convenience wrapper that automatically activates the virtual environment
#   before running Python scripts. Ensures scripts always run in the correct
#   environment without requiring manual activation.
#
# Usage:
#   ./run.sh <script_name> [script arguments]
#
# Examples:
#   ./run.sh 01_extract_tags.py
#   ./run.sh 02_analyze_tags.py
#   ./run.sh scripts/01_extract_tags.py
#   ./run.sh config.py
#
# Why use this wrapper:
#   - No need to remember 'source venv/bin/activate'
#   - Prevents accidentally running scripts with wrong Python version
#   - Works consistently across different terminal sessions
#   - Safer for beginners and collaborators
#
# Alternative (if you prefer manual activation):
#   source venv/bin/activate
#   python scripts/01_extract_tags.py
#
# Author: Shawn Ross
# Project: ARC Linkage Project LP190100900
# Last Updated: 2025-10-19
# ==============================================================================

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colours for output
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# ==============================================================================
# Validation
# ==============================================================================

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}✗ Virtual environment not found${NC}"
    echo ""
    echo "Please run setup first:"
    echo "  ${GREEN}./setup.sh${NC}"
    echo ""
    exit 1
fi

# Check if virtual environment is complete
if [ ! -f "venv/bin/activate" ]; then
    echo -e "${RED}✗ Virtual environment is incomplete${NC}"
    echo ""
    echo "Please run setup to recreate it:"
    echo "  ${GREEN}rm -rf venv${NC}"
    echo "  ${GREEN}./setup.sh${NC}"
    echo ""
    exit 1
fi

# Check if script argument provided
if [ $# -eq 0 ]; then
    echo -e "${RED}✗ No script specified${NC}"
    echo ""
    echo "Usage: ./run.sh <script_name> [arguments]"
    echo ""
    echo "Examples:"
    echo "  ${GREEN}./run.sh 01_extract_tags.py${NC}"
    echo "  ${GREEN}./run.sh 02_analyze_tags.py${NC}"
    echo "  ${GREEN}./run.sh 03_inspect_multiple_attachments.py${NC}"
    echo "  ${GREEN}./run.sh config.py${NC}"
    echo ""
    echo "Or with full path:"
    echo "  ${GREEN}./run.sh scripts/01_extract_tags.py${NC}"
    echo ""
    exit 1
fi

# ==============================================================================
# Script Execution
# ==============================================================================

# Get script name from first argument
SCRIPT_NAME="$1"
shift  # Remove first argument, leaving any additional arguments

# Determine full script path
# If script name doesn't include path, assume it's in scripts/ directory
if [[ "$SCRIPT_NAME" != *"/"* ]]; then
    SCRIPT_PATH="scripts/$SCRIPT_NAME"
else
    SCRIPT_PATH="$SCRIPT_NAME"
fi

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}✗ Script not found: $SCRIPT_PATH${NC}"
    echo ""
    echo "Available scripts in scripts/ directory:"
    ls -1 scripts/*.py 2>/dev/null || echo "  (no Python scripts found)"
    echo ""
    exit 1
fi

# Show what we're running
echo -e "${GREEN}➜ Running: $SCRIPT_PATH${NC}"
echo ""

# Activate virtual environment and run script
# shellcheck disable=SC1091
source venv/bin/activate

# Run the Python script with any additional arguments
# Use exec to replace shell with Python process (cleaner exit)
exec python "$SCRIPT_PATH" "$@"
