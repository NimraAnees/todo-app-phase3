# Feature Specification: Backend API & Data Layer

**Feature Branch**: `2-backend-api`
**Created**: 2026-01-12
**Status**: Draft
**Input**: User description: "Backend API & Data Layer..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Task (Priority: P1)

As an authenticated user, I want to create a new task so that I can track what I need to do.

**Why this priority**: Creating tasks is the fundamental entry point for value generation in a todo app. Without this, there is no data to manage.

**Independent Test**: Can be independently tested by sending a POST request with valid JWT and task details, verifying 201 Created response and data persistence in the database scoped to that user.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a valid JWT, **When** they send a POST request to `/api/v1/tasks` with a valid title, **Then** the task is created, assigned to their user ID, and returned with a 201 status and UUID.
2. **Given** an unauthenticated request (no/invalid JWT), **When** attempting to create a task, **Then** the system returns 401 Unauthorized and does not create the task.
3. **Given** an authenticated user, **When** they attempt to create a task without a title (empty/null), **Then** the system returns 422 Unprocessable Entity with a validation error.

---

### User Story 2 - View My Tasks (Priority: P1)

As an authenticated user, I want to see a list of my own tasks so that I can know what is pending.

**Why this priority**: Users need to retrieve their data to get value from the application. Privacy/isolation is critical here.

**Independent Test**: Can be tested by creating tasks for User A and User B, then requesting User A's task list and verifying it contains ONLY User A's tasks.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they request `GET /api/v1/tasks`, **Then** they receive a list of tasks belonging ONLY to them (scoped by user_id).
2. **Given** an authenticated user with no tasks, **When** they request `GET /api/v1/tasks`, **Then** they receive an empty list with 200 OK status.
3. **Given** an unauthenticated request, **When** attempting to list tasks, **Then** the system returns 401 Unauthorized.

---

### User Story 3 - Update Task Status & Details (Priority: P1)

As an authenticated user, I want to update a task's title or mark it as complete so that I can keep my list current.

**Why this priority**: Task lifecycle management (completion) is core utility.

**Independent Test**: Create a task, then send a PATCH request to update its status, verifying the change persists. attempt to update another user's task and verify 404/403.

**Acceptance Scenarios**:

1. **Given** an authenticated user who owns a specific task, **When** they send a PATCH request to `/api/v1/tasks/{id}` with `is_completed=true`, **Then** the task status updates and the updated object is returned.
2. **Given** an authenticated user who owns a task, **When** they send a PATCH request to update the title, **Then** the title is updated successfully.
3. **Given** an authenticated user, **When** they attempt to update a task ID that belongs to another user, **Then** the system returns 404 Not Found (to prevent ID enumeration/probing).

---

### User Story 4 - Delete Task (Priority: P2)

As an authenticated user, I want to remove a task permanently so I can declutter my list.

**Why this priority**: Important for list maintenance but less critical than creating/completing tasks for MVP usage.

**Independent Test**: Create a task, send DELETE request, verify it's no longer retrievable by GET request.

**Acceptance Scenarios**:

1. **Given** an authenticated user who owns a specific task, **When** they send a DELETE request to `/api/v1/tasks/{id}`, **Then** the task IS permanently removed and 204 No Content is returned.
2. **Given** an authenticated user, **When** they attempt to delete a task ID that belongs to another user, **Then** the system returns 404 Not Found.
3. **Given** an authenticated user, **When** they attempt to delete a non-existent task ID, **Then** the system returns 404 Not Found.

### Edge Cases

- What happens when a user sends a task title that exceeds database limits? (Should return 422)
- How does the system handle database connection failures? (Should return 500)
- What happens if the JWT expires during a request? (Should return 401)
- Are there limits on how many tasks a user can create? (Not specified, assumed unbounded for now)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `POST /api/v1/tasks` endpoint that accepts `title` (required) and `description` (optional).
- **FR-002**: System MUST automatically assign a unique UUID and the authenticated user's ID to every new task.
- **FR-003**: System MUST provided a `GET /api/v1/tasks` endpoint that returns a JSON array of tasks.
- **FR-004**: System MUST ensure `GET /api/v1/tasks` NEVER returns tasks belonging to other users (strict data isolation).
- **FR-005**: System MUST provide a `PATCH /api/v1/tasks/{id}` endpoint allowing updates to `title`, `description`, and `is_completed` fields.
- **FR-006**: System MUST provide a `DELETE /api/v1/tasks/{id}` endpoint to permanently remove a task.
- **FR-007**: System MUST return 404 Not Found if a user attempts to access (GET/PATCH/DELETE) a task ID belonging to another user.
- **FR-008**: System MUST validate that `title` is not empty and does not exceed reasonable length limits (e.g., 255 chars).
- **FR-009**: All API responses MUST use standard HTTP status codes (200, 201, 204, 400, 401, 403, 404, 422, 500).

### Key Entities

- **Task**: Represents a todo item
  - **id**: UUID, primary key
  - **title**: String, required content
  - **description**: String, optional detail
  - **is_completed**: Boolean, default false
  - **user_id**: UUID, foreign key to User (owner)
  - **created_at**: Timestamp
  - **updated_at**: Timestamp

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of API endpoints (Create, Read, Update, Delete) are successfully implemented and pass functional tests.
- **SC-002**: 100% of requests to these endpoints require a valid JWT; unauthenticated requests are rejected with 401.
- **SC-003**: Cross-user access attempts (User A accessing User B's task) result in 404 Not Found 100% of the time (verified by test).
- **SC-004**: Endpoints return correct HTTP status codes (201 for create, 204 for delete, 200 for OK) in 100% of test cases.
