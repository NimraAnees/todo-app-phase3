#!/bin/bash
# Test script for Phase-3 backend endpoints

echo "=========================================="
echo "Phase-3 Backend Endpoint Testing"
echo "=========================================="
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo "1. Testing Health Endpoint..."
curl -s "$BASE_URL/health" | jq '.'
echo ""

# Test 2: Register User
echo "2. Testing Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"demo$(date +%s)@example.com\",\"password\":\"SecurePass123\"}")
echo "$REGISTER_RESPONSE" | jq '.'

# Extract token
TOKEN=$(echo "$REGISTER_RESPONSE" | jq -r '.access_token')
echo "Token obtained: ${TOKEN:0:20}..."
echo ""

# Test 3: Get Current User
echo "3. Testing /auth/me..."
curl -s "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" | jq '.'
echo ""

# Test 4: Add Task via MCP
echo "4. Testing /mcp/add_task..."
ADD_TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/mcp/add_task" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Buy groceries\",\"description\":\"Milk, eggs, bread\"}")
echo "$ADD_TASK_RESPONSE" | jq '.'

# Extract task ID
TASK_ID=$(echo "$ADD_TASK_RESPONSE" | jq -r '.data.id // empty')
echo "Task ID: $TASK_ID"
echo ""

# Test 5: List Tasks via MCP
echo "5. Testing /mcp/list_tasks..."
curl -s -X POST "$BASE_URL/mcp/list_tasks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{}" | jq '.'
echo ""

# Test 6: Update Task via MCP
if [ -n "$TASK_ID" ]; then
  echo "6. Testing /mcp/update_task..."
  curl -s -X POST "$BASE_URL/mcp/update_task" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\":\"$TASK_ID\",\"title\":\"Buy groceries UPDATED\"}" | jq '.'
  echo ""
fi

# Test 7: Complete Task via MCP
if [ -n "$TASK_ID" ]; then
  echo "7. Testing /mcp/complete_task..."
  curl -s -X POST "$BASE_URL/mcp/complete_task" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\":\"$TASK_ID\"}" | jq '.'
  echo ""
fi

# Test 8: Delete Task via MCP
if [ -n "$TASK_ID" ]; then
  echo "8. Testing /mcp/delete_task..."
  curl -s -X POST "$BASE_URL/mcp/delete_task" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\":\"$TASK_ID\"}" | jq '.'
  echo ""
fi

echo "=========================================="
echo "All Tests Complete!"
echo "=========================================="
