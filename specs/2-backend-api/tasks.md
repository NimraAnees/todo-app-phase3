# Tasks: Backend API & Data Layer

**Input**: Design documents from `/specs/2-backend-api/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Verify backend project structure and environment variables in `.env`
- [ ] T002 Update `backend/requirements.txt` with `sqlmodel` and `python-jose` if missing

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T003 Create Task database model in `backend/app/models/task.py`
- [ ] T004 Create database migration for tasks table in `backend/migrations/002_create_tasks_table.sql`
- [ ] T005 Run migration `002_create_tasks_table.sql` against Neon PostgreSQL
- [ ] T006 [P] Define Task Pydantic schemas in `backend/app/schemas/task.py`
- [ ] T007 [P] Create empty tasks router in `backend/app/routers/tasks.py`
- [ ] T008 Register tasks router in `backend/app/main.py`

## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Authenticated user can create a new task.
**Independent Test**: Use curl to POST to `/api/v1/tasks` with valid JWT and verify 201 Created.

- [ ] T009 [US1] Implement POST `/api/v1/tasks` endpoint in `backend/app/routers/tasks.py`
- [ ] T010 [US1] Ensure task is saved with current user ID from `get_current_user` dependency

## Phase 4: User Story 2 - View My Tasks (Priority: P1)

**Goal**: Authenticated user can see a list of their own tasks.
**Independent Test**: GET `/api/v1/tasks` and verify it returns tasks belonging ONLY to the user.

- [ ] T011 [US2] Implement GET `/api/v1/tasks` endpoint in `backend/app/routers/tasks.py`
- [ ] T012 [US2] Add mandatory `.where(Task.user_id == user_id)` filter to the GET query

## Phase 5: User Story 3 - Update Task (Priority: P1)

**Goal**: Authenticated user can update task details or completion status.
**Independent Test**: PATCH `/api/v1/tasks/{id}` and verify changes. Verify 404 for other user's tasks.

- [ ] T013 [US3] Implement PATCH `/api/v1/tasks/{id}` endpoint in `backend/app/routers/tasks.py`
- [ ] T014 [US3] Implement ownership check (404 if user\_id mismatch) in PATCH handler

## Phase 6: User Story 4 - Delete Task (Priority: P2)

**Goal**: Authenticated user can delete a task.
**Independent Test**: DELETE `/api/v1/tasks/{id}` and verify 204. Verify 404 for other user's tasks.

- [ ] T015 [US4] Implement DELETE `/api/v1/tasks/{id}` endpoint in `backend/app/routers/tasks.py`
- [ ] T016 [US4] Implement ownership check (404 if user\_id mismatch) in DELETE handler

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T017 [P] Update REST API documentation in `backend/README.md`
- [ ] T018 Run final validation of all endpoints against success criteria in spec.md

## Dependencies & Execution Order

- **Foundational (Phase 2)**: MUST complete before any User Story.
- **User Stories (Phase 3-6)**: Can be implemented sequentially or in parallel once Phase 2 is done.
- **Task IDs T001-T018** represent the recommended execution path.
