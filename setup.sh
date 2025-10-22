#!/usr/bin/env bash
# ==============================================================================
# Blue Mountains Project - Setup Script
# ==============================================================================
#
# Purpose:
#   Automated setup for Blue Mountains Shale Mining Communities software.
#   Creates Python virtual environment, installs dependencies, and verifies
#   configuration. Designed for reproducible setup across different computers.
#
# Usage:
#   ./setup.sh
#
# What this script does:
#   1. Checks for Python 3.12+ installation
#   2. Checks for python3-venv package (Debian/Ubuntu systems)
#   3. Creates virtual environment in venv/ directory
#   4. Installs all dependencies from requirements.txt
#   5. Verifies Zotero API configuration (.env file)
#   6. Tests that all imports work correctly
#
# Prerequisites:
#   - Python 3.12 or higher
#   - python3-venv package (on Debian/Ubuntu: sudo apt install python3.12-venv)
#   - Internet connection (for pip package downloads)
#
# FAIR4RS Compliance:
#   - Reusable: Works across different computers and operating systems
#   - Accessible: Clear error messages guide users through issues
#   - Documented: Comprehensive comments explain each step
#
# Author: Shawn Ross
# Project: ARC Linkage Project LP190100900
# Last Updated: 2025-10-19
# ==============================================================================

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Colours for output (only if terminal supports it)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Colour
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# ==============================================================================
# Utility Functions
# ==============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}======================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ==============================================================================
# Prerequisite Checks
# ==============================================================================

check_python_version() {
    print_header "Checking Python Installation"

    # Check if python3 is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo "Please install Python 3.12 or higher:"
        echo "  Ubuntu/Debian: sudo apt install python3.12"
        echo "  macOS: brew install python@3.12"
        echo "  Windows: Download from https://www.python.org/downloads/"
        exit 1
    fi

    # Get Python version
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

    print_success "Found Python $PYTHON_VERSION"

    # Check minimum version (3.12)
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 12 ]); then
        print_error "Python 3.12 or higher is required"
        echo "Current version: $PYTHON_VERSION"
        echo "Please upgrade Python"
        exit 1
    fi

    print_success "Python version is compatible (>= 3.12)"
}

check_venv_package() {
    print_header "Checking Virtual Environment Support"

    # Create a test venv to check if ensurepip is available
    # This is more reliable than just checking if venv module exists
    TEST_VENV_DIR=".test_venv_$$"

    if python3 -m venv "$TEST_VENV_DIR" &> /dev/null; then
        # Success - clean up test venv
        rm -rf "$TEST_VENV_DIR"
        print_success "python3-venv package is installed and working"
        return 0
    else
        # Failed - clean up any partial test venv
        rm -rf "$TEST_VENV_DIR"

        print_error "python3-venv package is not properly installed"
        echo ""
        echo "The venv module exists but ensurepip is missing."
        echo "This is a common issue on Debian/Ubuntu systems."
        echo ""
        echo "To fix, install the full python3-venv package:"
        echo "  ${GREEN}sudo apt install python3.12-venv${NC}"
        echo ""
        echo "On other systems:"
        echo "  Fedora/RHEL: sudo dnf install python3-virtualenv"
        echo "  macOS: Should be included with Python installation"
        echo "  Windows: Should be included with Python installation"
        echo ""
        print_info "After installing, re-run this script: ./setup.sh"
        exit 1
    fi
}

# ==============================================================================
# Virtual Environment Setup
# ==============================================================================

create_virtual_environment() {
    print_header "Creating Virtual Environment"

    # Remove existing incomplete venv if it exists
    if [ -d "venv" ]; then
        # Check if it's a complete venv (has bin/activate)
        if [ ! -f "venv/bin/activate" ]; then
            print_warning "Removing incomplete virtual environment"
            rm -rf venv
        else
            print_info "Virtual environment already exists"
            print_info "To recreate, delete venv/ directory first: rm -rf venv"
            return 0
        fi
    fi

    # Create new virtual environment
    print_info "Creating venv/ directory..."
    python3 -m venv venv

    print_success "Virtual environment created in venv/"
}

install_dependencies() {
    print_header "Installing Python Dependencies"

    # Activate virtual environment
    # shellcheck disable=SC1091
    source venv/bin/activate

    # Upgrade pip to latest version (avoids warnings)
    print_info "Upgrading pip to latest version..."
    pip install --upgrade pip --quiet

    # Install dependencies from requirements.txt
    print_info "Installing dependencies from requirements.txt..."
    print_info "(This may take 1-3 minutes)"

    # Install with progress bar (remove --quiet for verbose output)
    if pip install -r requirements.txt --quiet; then
        print_success "All dependencies installed successfully"
    else
        print_error "Failed to install dependencies"
        echo "Try running manually: source venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi

    # Show installed packages
    echo ""
    print_info "Installed packages:"
    pip list | grep -E "pyzotero|pandas|fuzzywuzzy|networkx|matplotlib|seaborn|python-dotenv|python-Levenshtein" || true
}

# ==============================================================================
# Configuration Verification
# ==============================================================================

check_environment_file() {
    print_header "Checking Configuration"

    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        echo ""
        echo "Configuration file .env is required for Zotero API access."
        echo ""
        echo "To create it:"
        echo "  1. Copy the example: ${GREEN}cp .env.example .env${NC}"
        echo "  2. Edit .env and add your Zotero credentials"
        echo "  3. Get API key from: https://www.zotero.org/settings/keys"
        echo ""
        print_info "Creating .env from .env.example..."

        if [ -f ".env.example" ]; then
            cp .env.example .env
            print_success "Created .env file"
            echo ""
            print_warning "ACTION REQUIRED: Edit .env and add your Zotero API credentials"
            echo "  ${GREEN}nano .env${NC}  (or use your preferred editor)"
            echo ""
        else
            print_error ".env.example not found - cannot create .env"
            exit 1
        fi
    else
        print_success ".env file exists"
    fi

    # Verify .env has required variables (basic check)
    if grep -q "ZOTERO_GROUP_ID" .env && grep -q "ZOTERO_API_KEY" .env; then
        print_success ".env contains required Zotero configuration"
    else
        print_warning ".env may be missing required variables"
        echo "Ensure .env contains:"
        echo "  - ZOTERO_GROUP_ID"
        echo "  - ZOTERO_API_KEY_READONLY or ZOTERO_API_KEY"
    fi
}

verify_installation() {
    print_header "Verifying Installation"

    # Activate virtual environment
    # shellcheck disable=SC1091
    source venv/bin/activate

    # Test configuration loading
    print_info "Testing configuration loading..."
    if python scripts/config.py; then
        print_success "Configuration loads successfully"
    else
        print_error "Configuration test failed"
        echo "Check your .env file and ensure Zotero credentials are set"
        exit 1
    fi

    echo ""
    print_info "Testing package imports..."

    # Test critical imports
    if python3 -c "
import pyzotero
import pandas
import fuzzywuzzy
import networkx
import matplotlib
import seaborn
from dotenv import load_dotenv
print('✓ All required packages import successfully')
" 2>&1; then
        print_success "All package imports work correctly"
    else
        print_error "Package import test failed"
        exit 1
    fi
}

# ==============================================================================
# Setup Summary and Next Steps
# ==============================================================================

print_summary() {
    print_header "Setup Complete!"

    echo -e "${GREEN}Virtual environment is ready to use.${NC}"
    echo ""
    echo "To activate the virtual environment:"
    echo "  ${GREEN}source venv/bin/activate${NC}"
    echo ""
    echo "To run the tag extraction workflow:"
    echo "  ${GREEN}./run.sh 01_extract_tags.py${NC}"
    echo "  ${GREEN}./run.sh 02_analyze_tags.py${NC}"
    echo "  ${GREEN}./run.sh 03_inspect_multiple_attachments.py${NC}"
    echo ""
    echo "Or activate manually and run scripts directly:"
    echo "  ${GREEN}source venv/bin/activate${NC}"
    echo "  ${GREEN}python scripts/01_extract_tags.py${NC}"
    echo ""
    echo "To deactivate when done:"
    echo "  ${GREEN}deactivate${NC}"
    echo ""
    print_info "For full documentation, see README.md"
    echo ""
}

# ==============================================================================
# Main Execution
# ==============================================================================

main() {
    echo ""
    echo -e "${BLUE}======================================================================${NC}"
    echo -e "${BLUE}Blue Mountains Shale Mining Communities${NC}"
    echo -e "${BLUE}Automated Setup Script${NC}"
    echo -e "${BLUE}======================================================================${NC}"
    echo ""

    # Run all setup steps
    check_python_version
    check_venv_package
    create_virtual_environment
    install_dependencies
    check_environment_file
    verify_installation
    print_summary

    exit 0
}

# Run main function
main
