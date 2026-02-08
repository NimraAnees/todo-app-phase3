# FastAPI Backend - API Endpoints Documentation

This document provides comprehensive information about the available API endpoints in the FastAPI backend.

## Base URL

```
http://localhost:8000
```

## Table of Contents

1. [Authentication Endpoints](#authentication-endpoints)
2. [MCP Tool Endpoints](#mcp-tool-endpoints)
3. [Chat Endpoint](#chat-endpoint)
4. [Error Responses](#error-responses)

---

## Authentication Endpoints

All authentication endpoints are prefixed with `/auth`.

### 1. Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account with email and password. Returns a JWT access token upon successful registration.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid email or weak password
- `409 Conflict`: User with this email already exists
- `500 Internal Server Error`: Registration failed

**Password Requirements:**
- Minimum 6 characters

**Email Requirements:**
- Valid email format with '@' symbol

---

### 2. Sign In User

**Endpoint:** `POST /auth/signin`

**Description:** Authenticate an existing user with email and password. Returns a JWT access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid email or password
- `500 Internal Server Error`: Authentication failed

---

### 3. Get Current User

**Endpoint:** `GET /auth/me`

**Description:** Get the currently authenticated user's information. Requires JWT authentication.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "is_active": true
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User not found
- `500 Internal Server Error`: Failed to retrieve user information

---

## MCP Tool Endpoints

All MCP tool endpoints are prefixed with `/mcp` and require JWT authentication.

**Authentication Required:** All endpoints require the `Authorization: Bearer <token>` header.

### 1. Add Task

**Endpoint:** `POST /mcp/add_task`

**Description:** Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the new API endpoints"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Successfully created task 'Complete project documentation'",
  "data": {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Complete project documentation",
    "status": "pending",
    "created_at": "2026-02-07T10:30:00"
  },
  "error": null
}
```

**Error Responses:**
- `400 Bad Request`: Title is empty or invalid
- `401 Unauthorized`: Invalid or missing token
- `500 Internal Server Error`: Task creation failed

---

### 2. List Tasks

**Endpoint:** `POST /mcp/list_tasks`

**Description:** List all tasks for the authenticated user, optionally filtered by status.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "status": "pending"  // Optional: "pending", "in_progress", or "completed"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Retrieved 3 tasks",
  "data": {
    "tasks": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Complete project documentation",
        "description": "Write comprehensive docs",
        "status": "pending",
        "created_at": "2026-02-07T10:30:00",
        "updated_at": "2026-02-07T10:30:00",
        "completed_at": null
      }
    ],
    "count": 3,
    "status_filter": "pending"
  },
  "error": null
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `500 Internal Server Error`: Task retrieval failed

---

### 3. Update Task

**Endpoint:** `POST /mcp/update_task`

**Description:** Update an existing task for the authenticated user. Only the owner can update their tasks.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Complete project documentation (UPDATED)",
  "description": "Write comprehensive docs with examples",
  "status": "in_progress"
}
```

**Note:** All fields except `task_id` are optional. Only provide fields you want to update.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully updated task",
  "data": {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Complete project documentation (UPDATED)",
    "status": "in_progress",
    "updated_at": "2026-02-07T11:00:00"
  },
  "error": null
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Task belongs to a different user
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Task update failed

---

### 4. Complete Task

**Endpoint:** `POST /mcp/complete_task`

**Description:** Mark a task as completed. Only the owner can complete their tasks.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully completed task",
  "data": {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed",
    "completed_at": "2026-02-07T11:30:00"
  },
  "error": null
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Task belongs to a different user
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Task completion failed

---

### 5. Delete Task

**Endpoint:** `POST /mcp/delete_task`

**Description:** Delete a task. Only the owner can delete their tasks.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully deleted task",
  "data": {
    "task_id": "123e4567-e89b-12d3-a456-426614174000"
  },
  "error": null
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Task belongs to a different user
- `404 Not Found`: Task not found
- `500 Internal Server Error`: Task deletion failed

---

## Chat Endpoint

### Chat with AI Agent

**Endpoint:** `POST /api/{user_id}/chat`

**Description:** Send a message to the AI chat agent. (Existing endpoint - documented for completeness)

**Path Parameters:**
- `user_id`: UUID of the user

**Request Body:**
```json
{
  "message": "Add a task to write documentation"
}
```

**Response (200 OK):**
```json
{
  "response": "I've added a task to write documentation.",
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

---

## Error Responses

All error responses follow a consistent format:

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data or validation error
- `401 Unauthorized`: Authentication required or token invalid
- `403 Forbidden`: Access denied (e.g., trying to access another user's resource)
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists (e.g., duplicate email)
- `500 Internal Server Error`: Server-side error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

For MCP tool endpoints, errors also include:

```json
{
  "success": false,
  "message": "Failed to create task",
  "data": null,
  "error": "Detailed error message"
}
```

---

## Authentication Flow

1. **Register or Sign In**: Call `/auth/register` or `/auth/signin` to get a JWT token
2. **Store Token**: Save the `access_token` from the response
3. **Make Authenticated Requests**: Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <access_token>
   ```
4. **Token Expiration**: Tokens expire after 1 hour (3600 seconds). Sign in again to get a new token.

---

## Security Considerations

1. **Token Storage**: Store JWT tokens securely (e.g., httpOnly cookies or secure storage)
2. **HTTPS**: Always use HTTPS in production to protect tokens in transit
3. **Password Security**: Passwords are hashed using bcrypt before storage
4. **User Isolation**: All MCP endpoints enforce user data isolation - users can only access their own tasks
5. **Input Validation**: All inputs are validated using Pydantic models

---

## Testing

A test script is provided at `backend/test_new_endpoints.py` that demonstrates all endpoints:

```bash
# Make sure the backend server is running
cd backend
python test_new_endpoints.py
```

---

## API Documentation (Swagger UI)

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

Alternative documentation (ReDoc):

```
http://localhost:8000/redoc
```

---

## Example: Complete Workflow

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword123"}'

# Response: {"access_token": "eyJhbGc...", "token_type": "bearer"}

# 2. Get current user info
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer eyJhbGc..."

# 3. Add a task
curl -X POST http://localhost:8000/mcp/add_task \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete documentation", "description": "Write API docs"}'

# 4. List tasks
curl -X POST http://localhost:8000/mcp/list_tasks \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"status": null}'

# 5. Update task
curl -X POST http://localhost:8000/mcp/update_task \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"task_id": "123e4567-...", "status": "in_progress"}'

# 6. Complete task
curl -X POST http://localhost:8000/mcp/complete_task \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"task_id": "123e4567-..."}'

# 7. Delete task
curl -X POST http://localhost:8000/mcp/delete_task \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"task_id": "123e4567-..."}'
```

---

## Notes

- All timestamps are in ISO 8601 format (e.g., `2026-02-07T10:30:00`)
- UUIDs are in standard UUID4 format
- The backend uses Neon Serverless PostgreSQL for data persistence
- User data is strictly isolated - users can only access their own resources
