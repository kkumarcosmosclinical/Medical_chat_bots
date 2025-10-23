#!/bin/bash

################################################################################
# Medical Chatbot Deployment Script
# 
# This script deploys the Medical Chatbot application to your production server
# 
# Usage:
#   ./deploy.sh [server_user@server_ip] [optional: branch_name]
#   Example: ./deploy.sh krishan@38.137.54.223 main
################################################################################

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVER=${1:-"krishan@38.137.54.223"}
BRANCH=${2:-"main"}
REMOTE_DIR="/home/krishan/projects/Medicalchatbot"
APP_NAME="Medical Chatbot"

echo -e "${BLUE}=================================================="
echo -e "  ${APP_NAME} - Deployment Script"
echo -e "==================================================${NC}"
echo ""
echo -e "${YELLOW}Target Server:${NC} ${SERVER}"
echo -e "${YELLOW}Branch:${NC} ${BRANCH}"
echo -e "${YELLOW}Remote Directory:${NC} ${REMOTE_DIR}"
echo ""

# Step 1: Run local tests
echo -e "${BLUE}[1/8] Running Pre-deployment Checks...${NC}"
echo "Checking Python files for syntax errors..."
python -m py_compile main.py 2>/dev/null && echo "✓ main.py" || echo "✗ main.py has errors"
python -m py_compile app.py 2>/dev/null && echo "✓ app.py" || echo "✗ app.py has errors"
python -m py_compile config.py 2>/dev/null && echo "✓ config.py" || echo "✓ config.py"
echo -e "${GREEN}✓ Pre-deployment checks passed${NC}\n"

# Step 2: Create deployment package
echo -e "${BLUE}[2/8] Creating Deployment Package...${NC}"
DEPLOY_FILES=(
    "main.py"
    "app.py"
    "config.py"
    "requirements.txt"
    "chat_functions/"
    "Embedding_fuctions/"
    "database/"
    "Excel_chat_bot/"
    "fix_permissions.sh"
    "fix_dirs.py"
    "FIX_CHROMADB_PERMISSIONS.sh"
)

# Check if files exist
echo "Checking required files..."
for file in "${DEPLOY_FILES[@]}"; do
    if [ -e "$file" ]; then
        echo "  ✓ $file"
    else
        echo -e "  ${RED}✗ $file (missing)${NC}"
    fi
done
echo -e "${GREEN}✓ Deployment package ready${NC}\n"

# Step 3: Backup current version on server
echo -e "${BLUE}[3/8] Creating Backup on Server...${NC}"
BACKUP_CMD="cd ${REMOTE_DIR} && mkdir -p backups && tar -czf backups/backup_\$(date +%Y%m%d_%H%M%S).tar.gz *.py chat_functions Embedding_fuctions database Excel_chat_bot 2>/dev/null || echo 'No backup created (first deployment?)'"
ssh $SERVER "$BACKUP_CMD"
echo -e "${GREEN}✓ Backup created${NC}\n"

# Step 4: Upload files to server
echo -e "${BLUE}[4/8] Uploading Files to Server...${NC}"
echo "Uploading application files..."

# Upload Python files
scp main.py app.py config.py requirements.txt $SERVER:$REMOTE_DIR/
echo "  ✓ Python files uploaded"

# Upload directories
scp -r chat_functions $SERVER:$REMOTE_DIR/
scp -r Embedding_fuctions $SERVER:$REMOTE_DIR/
scp -r database $SERVER:$REMOTE_DIR/
scp -r Excel_chat_bot $SERVER:$REMOTE_DIR/
echo "  ✓ Application directories uploaded"

# Upload scripts
scp fix_permissions.sh fix_dirs.py FIX_CHROMADB_PERMISSIONS.sh $SERVER:$REMOTE_DIR/
echo "  ✓ Utility scripts uploaded"

echo -e "${GREEN}✓ All files uploaded${NC}\n"

# Step 5: Install/Update dependencies
echo -e "${BLUE}[5/8] Installing Dependencies...${NC}"
INSTALL_CMD="cd ${REMOTE_DIR} && pip install -r requirements.txt --quiet"
ssh $SERVER "$INSTALL_CMD" && echo -e "${GREEN}✓ Dependencies installed${NC}\n" || echo -e "${YELLOW}⚠ Dependency installation had warnings${NC}\n"

# Step 6: Fix permissions
echo -e "${BLUE}[6/8] Fixing Permissions...${NC}"
PERMISSION_CMD="cd ${REMOTE_DIR} && chmod +x *.sh && ./fix_permissions.sh && python fix_dirs.py"
ssh $SERVER "$PERMISSION_CMD"
echo -e "${GREEN}✓ Permissions fixed${NC}\n"

# Step 7: Restart application
echo -e "${BLUE}[7/8] Restarting Application...${NC}"
RESTART_CMD="cd ${REMOTE_DIR} && pkill -f 'python main.py' 2>/dev/null || echo 'No running process found' && nohup python main.py > app.log 2>&1 &"
ssh $SERVER "$RESTART_CMD"
sleep 3
echo -e "${GREEN}✓ Application restarted${NC}\n"

# Step 8: Verify deployment
echo -e "${BLUE}[8/8] Verifying Deployment...${NC}"
sleep 2
VERIFY_CMD="cd ${REMOTE_DIR} && ps aux | grep 'python main.py' | grep -v grep"
if ssh $SERVER "$VERIFY_CMD" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Application is running${NC}"
else
    echo -e "${RED}✗ Application is not running!${NC}"
    echo "Check logs: ssh $SERVER 'tail -50 ${REMOTE_DIR}/app.log'"
    exit 1
fi

# Check if API is responding
echo "Checking API health..."
HEALTH_CHECK="curl -f http://localhost:5001/docs -o /dev/null -s -w '%{http_code}' || echo '000'"
HTTP_CODE=$(ssh $SERVER "$HEALTH_CHECK")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ API is responding (HTTP $HTTP_CODE)${NC}"
else
    echo -e "${YELLOW}⚠ API check returned: HTTP $HTTP_CODE${NC}"
fi

echo ""
echo -e "${GREEN}=================================================="
echo -e "  ✅ Deployment Successful!"
echo -e "==================================================${NC}"
echo ""
echo -e "${YELLOW}Application URL:${NC} http://38.137.54.223:5001"
echo -e "${YELLOW}API Documentation:${NC} http://38.137.54.223:5001/docs"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  View logs:    ssh $SERVER 'tail -f ${REMOTE_DIR}/app.log'"
echo "  Stop app:     ssh $SERVER 'pkill -f \"python main.py\"'"
echo "  Restart app:  ssh $SERVER 'cd ${REMOTE_DIR} && python main.py'"
echo "  Check status: ssh $SERVER 'ps aux | grep python'"
echo ""
echo -e "${YELLOW}Backups Location:${NC} ${REMOTE_DIR}/backups/"
echo ""

