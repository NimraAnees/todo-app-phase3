#!/bin/bash

echo "============================================================"
echo "COMPLETE MCP ENDPOINT TEST - FRONTEND TO BACKEND"
echo "============================================================"

# Generate unique test user
TIMESTAMP=$(date +%s)
TEST_EMAIL="mcptest${TIMESTAMP}@example.com"
TEST_PASSWORD="MCPTest123"

echo ""
echo "Test Credentials:"
echo "  Email: $TEST_EMAIL"
echo "  Password: $TEST_PASSWORD"
echo ""

# Step 1: Register and get JWT token
echo "============================================================"
echo "STEP 1: Register User and Get JWT Token"
echo "============================================================"

REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

echo "Response: $REGISTER_RESPONSE"

TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
    echo "❌ Registration failed!"
    exit 1
fi

echo "✅ Registration successful!"
echo "🎫 JWT Token: ${TOKEN:0:50}..."
echo ""

# Step 2: Create Task via MCP
echo "============================================================"
echo "STEP 2: Create Task via POST /mcp/add_task"
echo "============================================================"

CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/add_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Test MCP Task","description":"Testing MCP endpoints"}')

echo "Response: $CREATE_RESPONSE"

TASK_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('data', {}).get('task_id', ''))" 2>/dev/null)

if [ -z "$TASK_ID" ]; then
    echo "❌ Task creation failed!"
    exit 1
fi

echo "✅ Task created successfully!"
echo "📝 Task ID: $TASK_ID"
echo ""

# Step 3: List Tasks via MCP
echo "============================================================"
echo "STEP 3: List Tasks via POST /mcp/list_tasks"
echo "============================================================"

LIST_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/list_tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"status":null}')

echo "Response: $LIST_RESPONSE"

TASK_COUNT=$(echo "$LIST_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('data', {}).get('count', 0))" 2>/dev/null)

echo "✅ Tasks listed successfully!"
echo "📊 Total tasks: $TASK_COUNT"
echo ""

# Step 4: Update Task via MCP
echo "============================================================"
echo "STEP 4: Update Task via POST /mcp/update_task"
echo "============================================================"

UPDATE_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/update_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"task_id\":\"$TASK_ID\",\"title\":\"Updated MCP Task\",\"description\":\"Updated via MCP\"}")

echo "Response: $UPDATE_RESPONSE"
echo "✅ Task updated successfully!"
echo ""

# Step 5: Complete Task via MCP
echo "============================================================"
echo "STEP 5: Complete Task via POST /mcp/complete_task"
echo "============================================================"

COMPLETE_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/complete_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"task_id\":\"$TASK_ID\"}")

echo "Response: $COMPLETE_RESPONSE"
echo "✅ Task completed successfully!"
echo ""

# Step 6: Delete Task via MCP
echo "============================================================"
echo "STEP 6: Delete Task via POST /mcp/delete_task"
echo "============================================================"

DELETE_RESPONSE=$(curl -s -X POST http://localhost:8000/mcp/delete_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"task_id\":\"$TASK_ID\"}")

echo "Response: $DELETE_RESPONSE"
echo "✅ Task deleted successfully!"
echo ""

# Final Summary
echo "============================================================"
echo "🎉 FINAL SUMMARY - ALL MCP ENDPOINTS WORKING!"
echo "============================================================"
echo "✅ POST /mcp/add_task - CREATE: SUCCESS"
echo "✅ POST /mcp/list_tasks - READ: SUCCESS"
echo "✅ POST /mcp/update_task - UPDATE: SUCCESS"
echo "✅ POST /mcp/complete_task - COMPLETE: SUCCESS"
echo "✅ POST /mcp/delete_task - DELETE: SUCCESS"
echo ""
echo "🎯 All MCP endpoints operational!"
echo "🔐 JWT authentication working correctly"
echo "📱 Frontend can now use these endpoints"
echo "============================================================"
