# Feature Specification: MCP Backend & Task Tools

**Feature Branch**: `005-mcp-backend`
**Created**: 2026-02-07
**Status**: Draft
**Input**: User description: "Spec-5: MCP Backend & Task Tools - Build a stateless MCP backend that exposes task operations as tools. Implement MCP tools for todo management: add_task, list_tasks, update_task, complete_task, delete_task. Persist all task data in Neon PostgreSQL using SQLModel. Enforce strict user isolation via JWT-authenticated requests. Provide a stable, auditable tool contract for AI agents."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Stateless Task Creation via MCP Tool (Priority: P1) 🎯 MVP

An AI agent needs to create a new task on behalf of an authenticated user. The agent calls the `add_task` MCP tool with task details, which persists the task to the database and returns a confirmation. The operation must be completely stateless, with all context derived from the authenticated JWT token.

**Why this priority**: This is the foundational operation that enables the entire todo system. Without the ability to create tasks through the MCP interface, no other operations can be demonstrated. It establishes the core pattern of JWT-authenticated, stateless tool invocation that all other tools will follow.

**Independent Test**: Can be fully tested by invoking the `add_task` MCP tool with valid authentication, verifying the task is persisted to the database with correct user ownership, and confirming the tool returns structured, deterministic output. The server can be restarted (cold-start test) and the task will remain in the database.

**Acceptance Scenarios**:

1. **Given** an authenticated user with a valid JWT token, **When** the AI agent calls `add_task` with task title "Buy groceries", **Then** the task is created in the database with the authenticated user's ID, a unique task ID is returned, and the operation completes in under 500ms.

2. **Given** an authenticated user, **When** the AI agent calls `add_task` with task details including title, description, and optional due date, **Then** all provided fields are stored correctly, default values are applied for optional fields not provided, and the complete task object is returned.

3. **Given** an unauthenticated request (no JWT token), **When** the AI agent attempts to call `add_task`, **Then** the tool returns an authentication error with HTTP 401 status and does not create any task in the database.

4. **Given** a request with an invalid or expired JWT token, **When** the AI agent calls `add_task`, **Then** the tool rejects the request with an authorization error and does not persist any data.

---

### User Story 2 - Task Retrieval with User Isolation (Priority: P2)

An AI agent needs to retrieve all tasks for an authenticated user to display or process them. The agent calls the `list_tasks` MCP tool, which queries the database and returns only the tasks owned by the authenticated user, enforcing strict data isolation.

**Why this priority**: This enables the AI agent to provide context-aware responses about existing tasks. It's essential for the agent to understand what tasks a user already has before suggesting new actions or modifications. User data isolation is critical for security and privacy.

**Independent Test**: Can be tested by creating tasks for multiple users, then calling `list_tasks` with different JWT tokens and verifying that each user only sees their own tasks. The tool should return an empty array for users with no tasks and a properly structured array for users with existing tasks.

**Acceptance Scenarios**:

1. **Given** a user with 5 existing tasks in the database, **When** the AI agent calls `list_tasks` with that user's JWT token, **Then** exactly 5 tasks are returned, all with matching user_id, and no tasks from other users are included.

2. **Given** a new user with no tasks, **When** the AI agent calls `list_tasks`, **Then** an empty array is returned with HTTP 200 status and appropriate metadata indicating zero tasks found.

3. **Given** multiple users with overlapping task titles, **When** each user's AI agent calls `list_tasks`, **Then** each agent receives only the tasks belonging to their authenticated user, demonstrating complete data isolation.

4. **Given** a database with 100 tasks across 10 users, **When** any user calls `list_tasks`, **Then** the response is returned in under 1 second and contains only their tasks, with proper pagination support if the user has more than 50 tasks.

---

### User Story 3 - Task State Management via MCP Tools (Priority: P3)

An AI agent needs to modify existing tasks (update details or mark as complete) or remove tasks that are no longer needed. The agent uses `update_task`, `complete_task`, and `delete_task` MCP tools to perform these operations, with each tool enforcing user ownership verification before allowing the operation.

**Why this priority**: These operations complete the full CRUD lifecycle for task management. While less critical than creation and retrieval for an MVP, they're essential for a production-ready system. They demonstrate the stateless pattern for mutations and ensure users can fully manage their task lifecycle.

**Independent Test**: Can be tested by creating a task via `add_task`, then calling `update_task` to modify it, `complete_task` to mark it done, and finally `delete_task` to remove it. Each operation should verify ownership, persist changes atomically, and return appropriate confirmation. Attempting these operations on another user's tasks should fail with authorization errors.

**Acceptance Scenarios**:

1. **Given** a user owns task ID 123, **When** the AI agent calls `update_task` with new title and description, **Then** the task is updated in the database with the new values, the updated_at timestamp is refreshed, and the complete updated task object is returned.

2. **Given** a user owns an incomplete task, **When** the AI agent calls `complete_task` with the task ID, **Then** the task's completed status is set to true, completed_at timestamp is recorded, and a success confirmation is returned.

3. **Given** a user attempts to update or delete a task they don't own, **When** the AI agent makes the call with their JWT token, **Then** the tool returns HTTP 403 Forbidden error and the task remains unchanged in the database.

4. **Given** a task that doesn't exist, **When** the AI agent calls any mutation tool (update, complete, delete), **Then** the tool returns HTTP 404 Not Found error with a clear message indicating the task was not found.

---

### Edge Cases

- What happens when an MCP tool is called with a malformed JWT token that can't be decoded?
- How does the system handle concurrent modifications to the same task from different AI agent instances?
- What occurs when the database connection is temporarily unavailable during a tool invocation?
- How does the system behave when a task deletion is attempted on an already-deleted task (idempotency)?
- What happens if an MCP tool receives invalid input data types (e.g., string instead of integer for task ID)?
- How does the system handle extremely large batch operations if `list_tasks` needs to return hundreds of tasks?
- What occurs when the MCP server restarts mid-operation (cold-start resilience test)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement five MCP tools following the Official MCP SDK specification: add_task, list_tasks, update_task, complete_task, delete_task
- **FR-002**: System MUST validate JWT tokens on every MCP tool invocation and extract the authenticated user_id from the token payload
- **FR-003**: System MUST enforce user data isolation by filtering all database queries with the authenticated user_id
- **FR-004**: System MUST persist all task data to Neon PostgreSQL database using SQLModel ORM
- **FR-005**: System MUST maintain zero in-memory state across MCP tool invocations (fully stateless operation)
- **FR-006**: System MUST return structured, deterministic JSON responses from all MCP tools with consistent schema
- **FR-007**: System MUST handle authentication failures by returning HTTP 401 Unauthorized without exposing sensitive error details
- **FR-008**: System MUST handle authorization failures (wrong user accessing another's task) by returning HTTP 403 Forbidden
- **FR-009**: System MUST handle resource not found scenarios by returning HTTP 404 with clear error messages
- **FR-010**: System MUST validate all input parameters to MCP tools using Pydantic schemas before database operations
- **FR-011**: System MUST perform database operations atomically to prevent partial updates in case of failures
- **FR-012**: System MUST log all MCP tool invocations with user_id, tool name, and outcome for audit trail
- **FR-013**: System MUST prevent AI agents from directly accessing the database (all access through MCP tools only)
- **FR-014**: System MUST integrate MCP tools with the existing FastAPI backend without disrupting current endpoints
- **FR-015**: System MUST handle database connection failures gracefully by returning HTTP 503 Service Unavailable
- **FR-016**: System MUST support task metadata including: id, user_id, title, description, completed status, created_at, updated_at, completed_at timestamps
- **FR-017**: System MUST assign unique task IDs (UUID recommended) upon task creation
- **FR-018**: System MUST automatically timestamp task creation, updates, and completion events
- **FR-019**: System MUST return appropriate HTTP status codes (200, 201, 400, 401, 403, 404, 500, 503) based on operation outcome
- **FR-020**: System MUST document each MCP tool's input schema, output schema, and error responses in a contract specification

### Non-Functional Requirements

- **NFR-001**: MCP tool responses MUST complete within 1 second for single-task operations under normal load
- **NFR-002**: System MUST pass cold-start test: server restart results in zero data loss (all data persisted)
- **NFR-003**: MCP tools MUST be callable independently without requiring previous tool invocations (true statelessness)
- **NFR-004**: System MUST handle at least 100 concurrent MCP tool requests without degradation
- **NFR-005**: Database schema MUST support future extensions without breaking existing MCP tool contracts

### Key Entities

- **Task**: Represents a todo item with ownership, completion status, and timestamps
  - Attributes: id (UUID), user_id (UUID, foreign key), title (string, required), description (string, optional), completed (boolean, default false), created_at (timestamp), updated_at (timestamp), completed_at (timestamp, nullable)
  - Relationships: Belongs to one User
  - Constraints: user_id must reference valid user, title cannot be empty, completed_at only set when completed is true

- **User**: Represents an authenticated user who owns tasks
  - Attributes: id (UUID), email (string), authentication details (handled by existing Spec-4 auth system)
  - Relationships: Has many Tasks
  - Note: User management is handled by existing authentication system (Spec-4), this spec only references user_id from JWT tokens

- **Tool Invocation Log** (audit trail): Records MCP tool usage
  - Attributes: id (UUID), user_id (UUID), tool_name (string), parameters (JSON), response_code (integer), timestamp (datetime), execution_time_ms (integer)
  - Purpose: Audit trail for debugging and security monitoring

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All five MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) are callable and return valid responses within 1 second
- **SC-002**: Cold-start test passes: Backend server restart with zero data loss; all tasks remain in database and are retrievable post-restart
- **SC-003**: User data isolation is enforced: Users can only access their own tasks through MCP tools; attempting to access another user's task returns HTTP 403
- **SC-004**: Stateless validation passes: Multiple sequential MCP tool calls from different users execute correctly without any in-memory state dependency
- **SC-005**: Authentication verification succeeds: Invalid or missing JWT tokens result in HTTP 401 errors; expired tokens are rejected
- **SC-006**: Database operations are atomic: Partial failures during task operations result in rollback; database integrity is maintained
- **SC-007**: Tool responses are deterministic: Same input parameters to the same MCP tool produce identical output structure and status codes
- **SC-008**: AI agents can perform complete task lifecycle: Create task via add_task, retrieve via list_tasks, modify via update_task, complete via complete_task, and remove via delete_task without database access
- **SC-009**: Error handling is comprehensive: All edge cases (invalid input, auth failure, resource not found, database error) return appropriate HTTP status codes with clear error messages
- **SC-010**: Integration with Spec-4 is seamless: MCP tools coexist with existing FastAPI endpoints; no breaking changes to current AI Chat Agent functionality

## Assumptions

1. **JWT Token Structure**: JWT tokens contain user_id in the payload and are signed with a secret key accessible to the MCP backend
2. **Database Availability**: Neon PostgreSQL database from existing implementation is available and accessible with valid connection credentials
3. **SQLModel ORM**: Existing SQLModel models and database connection setup from Spec-4 can be reused or extended
4. **FastAPI Integration**: MCP server will be integrated as a module or middleware within the existing FastAPI backend rather than as a separate service
5. **Authentication System**: User authentication and JWT token generation are handled by existing Better Auth integration (Spec-4) and are not in scope for this feature
6. **MCP SDK Version**: Official MCP SDK (Python) is available and compatible with FastAPI/SQLModel tech stack
7. **Tool Invocation Pattern**: AI agents will call MCP tools via HTTP requests (REST-like) or through an MCP client library that handles protocol details
8. **Error Response Format**: Standard HTTP status codes with JSON error messages are acceptable for error handling (no custom error protocol required)
9. **Performance Baseline**: Target of 1-second response time assumes standard database query performance; no complex aggregations or joins required for basic CRUD operations
10. **Concurrency Model**: Standard FastAPI async handling is sufficient; no special distributed locking or coordination required for MVP

## Out of Scope

- AI agent logic, natural language processing, or prompt design (handled in Spec-4)
- User authentication system, JWT token generation, or user management APIs (handled by existing auth system)
- Frontend UI, ChatKit integration, or user-facing web pages
- Conversation history or message persistence (handled in Spec-4)
- Advanced task features (subtasks, categories, tags, priorities, recurring tasks, attachments)
- Task sharing, collaboration, or multi-user access to same task
- Real-time synchronization or WebSocket notifications
- Task search, filtering, or sorting capabilities beyond basic list retrieval
- Task analytics, reporting, or dashboards
- Automated task scheduling or reminders
- Import/export functionality for tasks
- Mobile app or native client integration
- Rate limiting or advanced security features beyond JWT authentication
- Performance optimization beyond basic indexed queries

## Dependencies

- **Spec-4 (AI Chat Agent)**: This feature provides MCP tools that Spec-4's AI agent will consume. The AI agent is the primary client for these tools.
- **Existing Authentication System**: Relies on JWT tokens generated by the Better Auth integration to authenticate MCP tool requests.
- **Neon PostgreSQL Database**: Requires access to the existing Neon Serverless PostgreSQL instance with valid connection credentials.
- **SQLModel ORM**: Builds upon existing SQLModel models and database session management from previous implementations.
- **FastAPI Backend**: MCP tools will be integrated into the existing FastAPI application as additional endpoints or middleware.
- **Official MCP SDK**: Requires the Official MCP SDK (Python) to be installable and compatible with the tech stack.

## Relationship to Other Specifications

### Spec-4: AI Chat Agent & Conversation System

- **Spec-4 consumes Spec-5**: The AI agent in Spec-4 uses the MCP tools defined in this specification to perform task operations. The AI agent translates natural language user commands into MCP tool invocations.
- **No circular dependency**: Spec-5 provides a stable, versioned API contract that Spec-4 depends on. Spec-5 does not depend on Spec-4 implementation details.
- **Clear boundary**: Spec-4 handles user interaction and natural language understanding; Spec-5 handles data persistence and task CRUD operations.
- **Integration point**: The AI agent (Spec-4) will authenticate requests with JWT tokens and call MCP tools (Spec-5) over HTTP or via MCP client library.

### Future Specifications

- This specification establishes the MCP tool pattern that can be extended for other entity types (e.g., user preferences, notifications, categories).
- The stateless, JWT-authenticated design serves as a template for additional backend services.
