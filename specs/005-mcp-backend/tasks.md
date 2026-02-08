---
description: "Task list for MCP Backend & Task Tools implementation"
---

# Tasks: MCP Backend & Task Tools

**Input**: Design documents from `/specs/005-mcp-backend/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅

**Tests**: Not explicitly requested in specification - optional test tasks are marked for reference.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- Paths shown below follow the structure defined in plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: MCP SDK installation and project structure preparation

- [ ] T001 Install Official MCP SDK for Python in backend/requirements.txt
- [ ] T002 [P] Create MCP server module directory structure in backend/src/mcp/
- [ ] T003 [P] Create MCP test directory structure in backend/tests/mcp/
- [ ] T004 [P] Update backend/src/config/settings.py with MCP server configuration settings

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core MCP infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create MCP server initialization module in backend/src/mcp/server.py
- [ ] T006 [P] Implement stdio transport layer in backend/src/mcp/transport.py
- [ ] T007 [P] Implement JWT authentication middleware for MCP requests in backend/src/mcp/auth_middleware.py
- [ ] T008 [P] Create tool adapter base class in backend/src/mcp/tool_adapter.py
- [ ] T009 Integrate MCP server startup into FastAPI lifecycle in backend/src/main.py
- [ ] T010 [P] Add per-request database session management for MCP tools in backend/src/mcp/session_manager.py
- [ ] T011 [P] Update ToolCall model with MCP-specific fields in backend/src/models/tool_call.py
- [ ] T012 Create database migration for Task model enhancements in backend/migrations/003_add_task_due_date.sql

**Checkpoint**: MCP foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Stateless Task Creation via MCP Tool (Priority: P1) 🎯 MVP

**Goal**: Enable AI agents to create tasks through the `add_task` MCP tool with JWT authentication and database persistence

**Independent Test**: Call `add_task` MCP tool with valid JWT, verify task persists to database with correct user_id, restart server (cold-start test), verify task remains retrievable

### Tests for User Story 1 (OPTIONAL - for MCP protocol validation) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T013 [P] [US1] Contract test for add_task tool schema validation in backend/tests/mcp/test_add_task_contract.py
- [ ] T014 [P] [US1] Integration test for add_task with JWT authentication in backend/tests/mcp/test_add_task_integration.py
- [ ] T015 [P] [US1] Cold-start test for add_task persistence in backend/tests/mcp/test_cold_start.py

### Implementation for User Story 1

- [ ] T016 [US1] Validate existing Task model matches Spec-5 requirements in backend/src/models/task.py
- [ ] T017 [US1] Create Pydantic schema for add_task input parameters in backend/src/mcp/schemas/add_task_schema.py
- [ ] T018 [US1] Create Pydantic schema for add_task output response in backend/src/mcp/schemas/add_task_schema.py
- [ ] T019 [US1] Implement add_task MCP tool wrapper using decorator-based registration in backend/src/mcp/tools/add_task.py
- [ ] T020 [US1] Implement JWT token extraction and validation in add_task tool handler
- [ ] T021 [US1] Implement per-request database session management in add_task tool
- [ ] T022 [US1] Implement task creation logic with user_id from JWT in add_task tool
- [ ] T023 [US1] Implement error handling for authentication failures (HTTP 401) in add_task tool
- [ ] T024 [US1] Implement error handling for validation failures (HTTP 400) in add_task tool
- [ ] T025 [US1] Add audit logging to ToolCall model for add_task invocations
- [ ] T026 [US1] Register add_task tool with MCP server in backend/src/mcp/server.py

**Checkpoint**: At this point, User Story 1 should be fully functional - AI agents can create tasks via MCP protocol

---

## Phase 4: User Story 2 - Task Retrieval with User Isolation (Priority: P2)

**Goal**: Enable AI agents to retrieve tasks through the `list_tasks` MCP tool with strict user data isolation

**Independent Test**: Create tasks for multiple users, call `list_tasks` with different JWT tokens, verify each user only sees their own tasks and no cross-user data leakage occurs

### Tests for User Story 2 (OPTIONAL - for user isolation validation) ⚠️

- [ ] T027 [P] [US2] Contract test for list_tasks tool schema validation in backend/tests/mcp/test_list_tasks_contract.py
- [ ] T028 [P] [US2] Integration test for list_tasks with user isolation in backend/tests/mcp/test_list_tasks_isolation.py
- [ ] T029 [P] [US2] Performance test for list_tasks with 100 tasks in backend/tests/mcp/test_list_tasks_performance.py

### Implementation for User Story 2

- [ ] T030 [US2] Create Pydantic schema for list_tasks input parameters (filters, pagination) in backend/src/mcp/schemas/list_tasks_schema.py
- [ ] T031 [US2] Create Pydantic schema for list_tasks output response in backend/src/mcp/schemas/list_tasks_schema.py
- [ ] T032 [US2] Implement list_tasks MCP tool wrapper with decorator registration in backend/src/mcp/tools/list_tasks.py
- [ ] T033 [US2] Implement JWT token validation and user_id extraction in list_tasks tool
- [ ] T034 [US2] Implement database query with user_id filtering for task retrieval
- [ ] T035 [US2] Implement optional status filtering in list_tasks query
- [ ] T036 [US2] Implement pagination support (limit/offset) in list_tasks query
- [ ] T037 [US2] Implement error handling for empty result sets (return empty array, not error)
- [ ] T038 [US2] Add audit logging to ToolCall model for list_tasks invocations
- [ ] T039 [US2] Register list_tasks tool with MCP server in backend/src/mcp/server.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - tasks can be created and retrieved with user isolation

---

## Phase 5: User Story 3 - Task State Management via MCP Tools (Priority: P3)

**Goal**: Enable AI agents to update, complete, and delete tasks through MCP tools with ownership verification

**Independent Test**: Create task via add_task, modify with update_task, complete with complete_task, delete with delete_task; verify ownership enforcement (403 error when accessing other user's tasks)

### Tests for User Story 3 (OPTIONAL - for mutation validation) ⚠️

- [ ] T040 [P] [US3] Contract test for update_task tool schema validation in backend/tests/mcp/test_update_task_contract.py
- [ ] T041 [P] [US3] Contract test for complete_task tool schema validation in backend/tests/mcp/test_complete_task_contract.py
- [ ] T042 [P] [US3] Contract test for delete_task tool schema validation in backend/tests/mcp/test_delete_task_contract.py
- [ ] T043 [P] [US3] Integration test for ownership verification across all mutation tools in backend/tests/mcp/test_ownership_enforcement.py

### Implementation for User Story 3

#### update_task Implementation

- [ ] T044 [P] [US3] Create Pydantic schema for update_task input parameters in backend/src/mcp/schemas/update_task_schema.py
- [ ] T045 [P] [US3] Create Pydantic schema for update_task output response in backend/src/mcp/schemas/update_task_schema.py
- [ ] T046 [US3] Implement update_task MCP tool wrapper in backend/src/mcp/tools/update_task.py
- [ ] T047 [US3] Implement JWT validation and user_id extraction in update_task tool
- [ ] T048 [US3] Implement ownership verification (task.user_id == auth user_id) in update_task tool
- [ ] T049 [US3] Implement task update logic with field validation in update_task tool
- [ ] T050 [US3] Implement error handling for 403 Forbidden and 404 Not Found in update_task tool
- [ ] T051 [US3] Add audit logging for update_task invocations
- [ ] T052 [US3] Register update_task tool with MCP server

#### complete_task Implementation

- [ ] T053 [P] [US3] Create Pydantic schema for complete_task input parameters in backend/src/mcp/schemas/complete_task_schema.py
- [ ] T054 [P] [US3] Create Pydantic schema for complete_task output response in backend/src/mcp/schemas/complete_task_schema.py
- [ ] T055 [US3] Implement complete_task MCP tool wrapper in backend/src/mcp/tools/complete_task.py
- [ ] T056 [US3] Implement JWT validation and ownership verification in complete_task tool
- [ ] T057 [US3] Implement task completion logic (set completed=true, completed_at=now) in complete_task tool
- [ ] T058 [US3] Implement error handling for 403/404 in complete_task tool
- [ ] T059 [US3] Add audit logging for complete_task invocations
- [ ] T060 [US3] Register complete_task tool with MCP server

#### delete_task Implementation

- [ ] T061 [P] [US3] Create Pydantic schema for delete_task input parameters in backend/src/mcp/schemas/delete_task_schema.py
- [ ] T062 [P] [US3] Create Pydantic schema for delete_task output response in backend/src/mcp/schemas/delete_task_schema.py
- [ ] T063 [US3] Implement delete_task MCP tool wrapper in backend/src/mcp/tools/delete_task.py
- [ ] T064 [US3] Implement JWT validation and ownership verification in delete_task tool
- [ ] T065 [US3] Implement task deletion logic with atomic transaction in delete_task tool
- [ ] T066 [US3] Implement idempotent delete (204 No Content if already deleted)
- [ ] T067 [US3] Implement error handling for 403/404 in delete_task tool
- [ ] T068 [US3] Add audit logging for delete_task invocations
- [ ] T069 [US3] Register delete_task tool with MCP server

**Checkpoint**: All user stories should now be independently functional - complete task lifecycle supported

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final integration

- [ ] T070 [P] Create MCP tool contract documentation in specs/005-mcp-backend/contracts/mcp-tools.yaml
- [ ] T071 [P] Update Spec-4 AI agent to use MCP client in backend/src/agents/todo_agent.py
- [ ] T072 Add MCP client initialization in AI agent with error handling
- [ ] T073 [P] Implement fallback mechanism (MCP client → direct tool calls) during migration
- [ ] T074 Run cold-start validation test (create task, restart server, retrieve task)
- [ ] T075 Run performance validation test (100 concurrent requests, verify < 1 second response)
- [ ] T076 [P] Create quickstart guide for MCP server setup in specs/005-mcp-backend/quickstart.md
- [ ] T077 [P] Update README with MCP server documentation
- [ ] T078 Remove fallback mechanism and enforce MCP-only tool access
- [ ] T079 Final integration test with Spec-4 AI agent end-to-end flow
- [ ] T080 [P] Code cleanup and refactoring for production readiness

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 (can run in parallel)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1 and US2 (can run in parallel)

**Note**: All three user stories are independent after foundational infrastructure is complete. They can be implemented in parallel by different team members.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Schemas before tool implementations
- Tool implementations before tool registration
- Audit logging with tool implementation
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all three user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Schemas within a story marked [P] can run in parallel
- Within US3, the three mutation tools (update, complete, delete) can be implemented in parallel after their schemas are created

---

## Parallel Example: User Story 1

```bash
# Launch all schema tasks for US1 together:
Task: "Create Pydantic schema for add_task input in backend/src/mcp/schemas/add_task_schema.py"
Task: "Create Pydantic schema for add_task output in backend/src/mcp/schemas/add_task_schema.py"

# These can run after schemas complete:
Task: "Implement add_task MCP tool wrapper in backend/src/mcp/tools/add_task.py"
Task: "Add audit logging to ToolCall model for add_task"
```

---

## Parallel Example: User Story 3

```bash
# All six schema tasks can run in parallel:
Task: "Create Pydantic schema for update_task input..."
Task: "Create Pydantic schema for update_task output..."
Task: "Create Pydantic schema for complete_task input..."
Task: "Create Pydantic schema for complete_task output..."
Task: "Create Pydantic schema for delete_task input..."
Task: "Create Pydantic schema for delete_task output..."

# After schemas done, three tool implementations can run in parallel:
Task: "Implement update_task MCP tool wrapper..."
Task: "Implement complete_task MCP tool wrapper..."
Task: "Implement delete_task MCP tool wrapper..."
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (add_task tool)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Cold-start test: Create task, restart server, verify persistence
   - Authentication test: Invalid JWT returns 401
   - Performance test: add_task completes in < 500ms
5. Deploy/demo if ready

**MVP Deliverable**: AI agents can create tasks through MCP protocol with JWT authentication

### Incremental Delivery

1. Complete Setup + Foundational → MCP foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (add task retrieval)
4. Add User Story 3 → Test independently → Deploy/Demo (full CRUD lifecycle)
5. Each story adds value without breaking previous stories

**Incremental Value**:
- After US1: Task creation works
- After US2: Task creation + retrieval works
- After US3: Full task lifecycle management works

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (add_task)
   - Developer B: User Story 2 (list_tasks)
   - Developer C: User Story 3 (update, complete, delete tasks)
3. Stories complete and integrate independently

**Note**: All three user stories are independent - no cross-story dependencies

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 80 |
| **Setup Tasks** | 4 |
| **Foundational Tasks** | 8 |
| **User Story 1 Tasks** | 14 (3 tests + 11 implementation) |
| **User Story 2 Tasks** | 13 (3 tests + 10 implementation) |
| **User Story 3 Tasks** | 30 (4 tests + 26 implementation) |
| **Polish Tasks** | 11 |
| **Parallel Opportunities** | ~40 tasks marked [P] |
| **Estimated Timeline** | 2 weeks (per plan.md) |
| **MVP Scope** | Phase 1 + Phase 2 + Phase 3 (US1) = 26 tasks |

## Independent Test Criteria

| User Story | Test Criteria | Validates |
|------------|---------------|-----------|
| US1 (add_task) | Call add_task with JWT → verify task in DB → restart server → verify task persists | Stateless task creation, JWT auth, cold-start resilience |
| US2 (list_tasks) | Create tasks for User A and User B → call list_tasks with each JWT → verify isolation | User data isolation, no cross-user leakage |
| US3 (mutations) | Create task → update → complete → delete → verify 403 on wrong user access | Full CRUD lifecycle, ownership enforcement |
