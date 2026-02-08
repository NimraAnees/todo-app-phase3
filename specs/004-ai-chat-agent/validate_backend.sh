#!/bin/bash
# Backend Validation Script for AI Chat Agent & Conversation System
# Run this script to validate the backend implementation

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================="
echo "AI Chat Agent Backend Validation"
echo -e "==========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}1. Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
    echo -e "${GREEN}✓ Python $PYTHON_VERSION (meets requirement: 3.11+)${NC}"
else
    echo -e "${RED}✗ Python $PYTHON_VERSION (requires 3.11+)${NC}"
    exit 1
fi
echo ""

# Check if backend directory exists
echo -e "${YELLOW}2. Checking backend directory structure...${NC}"
if [ -d "backend/src" ]; then
    echo -e "${GREEN}✓ Backend directory structure exists${NC}"
else
    echo -e "${RED}✗ Backend directory not found${NC}"
    exit 1
fi
echo ""

# Check if requirements.txt exists
echo -e "${YELLOW}3. Checking requirements.txt...${NC}"
if [ -f "backend/requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt found${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi
echo ""

# Check if key source files exist
echo -e "${YELLOW}4. Checking implementation files...${NC}"

FILES=(
    "backend/src/main.py"
    "backend/src/database.py"
    "backend/src/models/user.py"
    "backend/src/models/task.py"
    "backend/src/models/conversation.py"
    "backend/src/models/message.py"
    "backend/src/models/tool_call.py"
    "backend/src/services/task_service.py"
    "backend/src/services/conversation_service.py"
    "backend/src/services/authentication_service.py"
    "backend/src/tools/add_task_tool.py"
    "backend/src/tools/list_tasks_tool.py"
    "backend/src/tools/update_task_tool.py"
    "backend/src/tools/complete_task_tool.py"
    "backend/src/tools/delete_task_tool.py"
    "backend/src/api/chat_endpoint.py"
    "backend/src/agents/todo_agent.py"
    "backend/src/config/settings.py"
)

MISSING_FILES=0
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✓ $file${NC}"
    else
        echo -e "${RED}  ✗ $file (missing)${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -eq 0 ]; then
    echo -e "${GREEN}✓ All implementation files present (${#FILES[@]}/${#FILES[@]})${NC}"
else
    echo -e "${RED}✗ Missing $MISSING_FILES files${NC}"
    exit 1
fi
echo ""

# Check Python syntax
echo -e "${YELLOW}5. Checking Python syntax...${NC}"
SYNTAX_ERRORS=0
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            : # Success, do nothing
        else
            echo -e "${RED}  ✗ Syntax error in $file${NC}"
            SYNTAX_ERRORS=$((SYNTAX_ERRORS + 1))
        fi
    fi
done

if [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ No syntax errors detected${NC}"
else
    echo -e "${RED}✗ Found $SYNTAX_ERRORS files with syntax errors${NC}"
    exit 1
fi
echo ""

# Check if .env exists or .env.example
echo -e "${YELLOW}6. Checking environment configuration...${NC}"
if [ -f "backend/.env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
elif [ -f "backend/.env.example" ]; then
    echo -e "${YELLOW}⚠ .env.example exists but .env is missing${NC}"
    echo -e "${YELLOW}  Copy .env.example to .env and fill in values${NC}"
else
    echo -e "${YELLOW}⚠ No .env file found${NC}"
    echo -e "${YELLOW}  You'll need to create one before running the server${NC}"
fi
echo ""

# Check if dependencies are installed
echo -e "${YELLOW}7. Checking installed dependencies...${NC}"
cd backend

DEPS=("fastapi" "uvicorn" "sqlmodel" "openai" "pydantic")
MISSING_DEPS=0

for dep in "${DEPS[@]}"; do
    if python3 -c "import $dep" 2>/dev/null; then
        echo -e "${GREEN}  ✓ $dep installed${NC}"
    else
        echo -e "${RED}  ✗ $dep not installed${NC}"
        MISSING_DEPS=$((MISSING_DEPS + 1))
    fi
done

if [ $MISSING_DEPS -gt 0 ]; then
    echo -e "${YELLOW}⚠ $MISSING_DEPS dependencies missing${NC}"
    echo -e "${YELLOW}  Run: pip install -r requirements.txt${NC}"
else
    echo -e "${GREEN}✓ All key dependencies installed${NC}"
fi

cd ..
echo ""

# Try to import main module
echo -e "${YELLOW}8. Testing module imports...${NC}"
cd backend
if python3 -c "from src.main import create_application" 2>/dev/null; then
    echo -e "${GREEN}✓ Main application module imports successfully${NC}"
else
    echo -e "${RED}✗ Failed to import main application${NC}"
    echo -e "${YELLOW}  This may be due to missing dependencies or environment variables${NC}"
fi
cd ..
echo ""

# Summary
echo -e "${BLUE}=========================================="
echo "Validation Summary"
echo -e "==========================================${NC}"
echo ""

if [ $MISSING_FILES -eq 0 ] && [ $SYNTAX_ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ Backend implementation is COMPLETE${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Set up environment variables in backend/.env"
    echo "2. Configure Neon PostgreSQL database"
    echo "3. Add OpenAI API key to .env"
    echo "4. Install dependencies: cd backend && pip install -r requirements.txt"
    echo "5. Start server: uvicorn src.main:app --reload"
    echo "6. Test endpoint: curl http://localhost:8000/"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "- Setup guide: specs/004-ai-chat-agent/quickstart.md"
    echo "- Validation report: specs/004-ai-chat-agent/VALIDATION_REPORT.md"
    echo "- API contract: specs/004-ai-chat-agent/contracts/chat-api.yaml"
else
    echo -e "${RED}❌ Validation failed - please fix the issues above${NC}"
    exit 1
fi

echo ""
