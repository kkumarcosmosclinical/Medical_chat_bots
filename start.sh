#!/bin/bash

################################################################################
# Medical Chatbot Startup Script
# 
# This script starts the Medical Chatbot application using conda base environment
################################################################################

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=================================================="
echo "  Medical Chatbot - Starting Application"
echo -e "==================================================${NC}"

# Initialize conda
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    conda activate base
    echo -e "${GREEN}✓ Conda base environment activated${NC}"
else
    echo -e "${YELLOW}⚠ Conda not found, using system Python${NC}"
fi

# Check if all requirements are installed
echo "Checking dependencies..."
pip install -r requirements.txt --quiet

# Fix permissions
if [ -f "fix_permissions.sh" ]; then
    chmod +x fix_permissions.sh
    ./fix_permissions.sh > /dev/null 2>&1
fi

if [ -f "fix_dirs.py" ]; then
    python fix_dirs.py
fi

# Start the application
echo ""
echo -e "${GREEN}Starting application...${NC}"
python main.py

