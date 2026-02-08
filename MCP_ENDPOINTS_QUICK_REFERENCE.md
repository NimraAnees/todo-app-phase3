# MCP Endpoints - Quick Reference Guide

## 🎯 All Operations Use POST Method

**Base URL**: `http://localhost:8000`

**Authentication**: JWT token in `Authorization: Bearer {token}` header

---

## 📋 List Tasks

```bash
POST /mcp/list_tasks
```

**Request**:
```json
{
  "status": null  // Optional: "pending", "in_progress", "completed"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Retrieved 5 tasks",
  "data": {
    "tasks": [/* Task objects */],
    "count": 5
  }
}
```

**Frontend Usage**:
```typescript
const response = await apiClient.post('/mcp/list_tasks', { status: null });
const tasks = response.data.tasks;
```

---

## ➕ Add Task

```bash
POST /mcp/add_task
```

**Request**:
```json
{
  "title": "Task title",
  "description": "Optional description"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully created task 'Task title'",
  "data": {
    "task_id": "uuid",
    "title": "Task title",
    "status": "pending",
    "created_at": "2026-02-08T07:10:19"
  }
}
```

---

## ✏️ Update Task

```bash
POST /mcp/update_task
```

**Request**:
```json
{
  "task_id": "uuid",
  "title": "New title",          // Optional
  "description": "New desc",      // Optional
  "status": "in_progress"         // Optional: "pending", "in_progress", "completed"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully updated task",
  "data": {
    "task_id": "uuid",
    "title": "New title",
    "status": "in_progress",
    "updated_at": "2026-02-08T07:10:23"
  }
}
```

---

## ✅ Complete Task

```bash
POST /mcp/complete_task
```

**Request**:
```json
{
  "task_id": "uuid"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully completed task",
  "data": {
    "task_id": "uuid",
    "title": "Task title",
    "status": "completed",
    "completed_at": "2026-02-08T07:10:25"
  }
}
```

---

## 🗑️ Delete Task

```bash
POST /mcp/delete_task
```

**Request**:
```json
{
  "task_id": "uuid"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Successfully deleted task",
  "data": {
    "task_id": "uuid"
  }
}
```

---

## 🔐 Authentication Endpoints

### Register

```bash
POST /auth/register
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Sign In

```bash
POST /auth/signin
```

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Get Current User

```bash
GET /auth/me
Headers: Authorization: Bearer {token}
```

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2026-02-08T07:00:00"
}
```

---

## 📊 Task Object Schema

```typescript
interface Task {
  id: string;                    // UUID
  title: string;                 // Task title
  description: string;           // Task description
  status: string;                // "pending" | "in_progress" | "completed"
  created_at: string;            // ISO datetime
  updated_at: string;            // ISO datetime
  completed_at: string | null;  // ISO datetime or null
}
```

---

## 🔑 Key Differences from REST

| Aspect | Traditional REST | MCP Endpoints |
|--------|-----------------|---------------|
| HTTP Method | GET, POST, PUT, DELETE | **POST only** |
| Endpoint | `/api/v1/tasks/{id}` | `/mcp/{tool_name}` |
| ID Location | URL path | **Request body** |
| Response | Direct data | **Wrapped in MCPResponse** |
| Task Status | `is_completed: boolean` | **status: string** |

---

## ⚡ Quick Examples

### Create and List Tasks

```bash
# 1. Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123"}'

# Response: { "access_token": "..." }

# 2. Create Task
curl -X POST http://localhost:8000/mcp/add_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"My Task","description":"Do something"}'

# 3. List Tasks
curl -X POST http://localhost:8000/mcp/list_tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"status":null}'
```

### Update and Complete

```bash
# 4. Update Task
curl -X POST http://localhost:8000/mcp/update_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"task_id":"TASK_UUID","title":"Updated Title"}'

# 5. Complete Task
curl -X POST http://localhost:8000/mcp/complete_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"task_id":"TASK_UUID"}'

# 6. Delete Task
curl -X POST http://localhost:8000/mcp/delete_task \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"task_id":"TASK_UUID"}'
```

---

## 🛠️ Testing

### Run Complete Test

```bash
./test_mcp_endpoints.sh
```

### Access Swagger Docs

http://localhost:8000/docs

### Frontend URLs

- Frontend: http://localhost:3001
- Tasks Page: http://localhost:3001/tasks

---

## ❌ Common Mistakes

1. ❌ Using GET instead of POST
   ```bash
   GET /mcp/list_tasks  # WRONG
   ```
   ✅ Always use POST:
   ```bash
   POST /mcp/list_tasks  # CORRECT
   ```

2. ❌ Sending task_id in URL
   ```bash
   POST /mcp/update_task/123  # WRONG
   ```
   ✅ Send in request body:
   ```json
   { "task_id": "123" }  // CORRECT
   ```

3. ❌ Using is_completed boolean
   ```json
   { "is_completed": true }  // WRONG
   ```
   ✅ Use status string:
   ```json
   { "status": "completed" }  // CORRECT
   ```

4. ❌ Accessing response data directly
   ```typescript
   const tasks = response;  // WRONG
   ```
   ✅ Extract from data property:
   ```typescript
   const tasks = response.data.tasks;  // CORRECT
   ```

---

## 📞 Support

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Test Script**: `./test_mcp_endpoints.sh`
- **Documentation**: `FRONTEND_MCP_FIX_COMPLETE.md`
