# Tasks: Authentication & Security Layer

**Input**: Design documents from `/specs/1-auth-security/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec - focusing on implementation tasks only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Path Conventions

- **Web app**: `backend/app/`, `frontend/app/`
- Backend paths: `backend/app/{routers,models,schemas,middleware,core}/`
- Frontend paths: `frontend/app/`, `frontend/components/`, `frontend/lib/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (app/, tests/, .env.example, requirements.txt, README.md)
- [x] T002 Create frontend directory structure (app/, components/, lib/, public/, .env.local.example, package.json)
- [x] T003 [P] Initialize backend Python virtual environment and install core dependencies (fastapi, uvicorn, sqlmodel, psycopg2-binary)
- [x] T004 [P] Initialize frontend Next.js project and install core dependencies (next@16+, react@19+, typescript)
- [x] T005 [P] Create backend .env.example with required variables (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS)
- [x] T006 [P] Create frontend .env.local.example with required variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, DATABASE_URL)
- [x] T007 [P] Add .gitignore entries for both backend and frontend (.env, venv/, node_modules/, .next/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create backend database connection module in backend/app/database.py (SQLModel engine, session maker, get_db dependency)
- [x] T009 Create backend configuration module in backend/app/core/config.py (load environment variables, settings class)
- [x] T010 [P] Install backend authentication dependencies (python-jose[cryptography], passlib[bcrypt], python-multipart)
- [x] T011 [P] Install frontend authentication dependencies (better-auth@1.x)
- [x] T012 Create backend security utilities in backend/app/core/security.py (password hashing, JWT token verification functions)
- [x] T013 Create backend authentication middleware in backend/app/middleware/auth_middleware.py (extract and verify JWT from Authorization header)
- [x] T014 Create backend authentication dependencies in backend/app/dependencies.py (get_current_user dependency using security module)
- [ ] T015 Create frontend Better Auth configuration in frontend/lib/auth.ts (configure JWT plugin, database, cookies, expiration)
- [x] T016 Create frontend API client utility in frontend/lib/api-client.ts (fetch wrapper with Authorization header, error handling for 401)
- [x] T017 Create database migration for users table (CREATE TABLE users with id, email, password_hash, created_at, updated_at, indexes)
- [ ] T018 Run database migration to create users table in Neon PostgreSQL
- [x] T019 Create backend FastAPI main application in backend/app/main.py (FastAPI app, CORS middleware, health check endpoint)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts with secure password hashing and database storage

**Independent Test**: Submit registration form with valid email/password, verify user created in database with hashed password, receive JWT token

### Implementation for User Story 1

- [x] T020 [P] [US1] Create User SQLModel entity in backend/app/models/user.py (id UUID, email unique, password_hash, timestamps)
- [x] T021 [P] [US1] Create UserCreate Pydantic schema in backend/app/schemas/auth.py (email EmailStr, password min_length=8)
- [x] T022 [P] [US1] Create UserResponse Pydantic schema in backend/app/schemas/user.py (id, email, created_at - excludes password_hash)
- [x] T023 [P] [US1] Create TokenResponse Pydantic schema in backend/app/schemas/auth.py (access_token, token_type, user)
- [x] T024 [US1] Implement user registration endpoint POST /api/v1/auth/register in backend/app/routers/auth.py (validate email unique, hash password, create user, return JWT)
- [x] T025 [US1] Add validation for duplicate email in registration endpoint (return 400 with generic error message to prevent user enumeration)
- [x] T026 [US1] Add password validation (minimum 8 characters) in registration endpoint using Pydantic Field validator
- [x] T027 [US1] Integrate Better Auth JWT token issuance in registration endpoint (sign token with BETTER_AUTH_SECRET, set 1-hour expiration)
- [x] T028 [P] [US1] Create registration page in frontend/app/(auth)/signup/page.tsx (Server Component with metadata)
- [x] T029 [P] [US1] Create SignupForm component in frontend/components/auth/SignupForm.tsx (Client Component with form validation, API call)
- [x] T030 [US1] Implement registration form validation in SignupForm (email format RFC 5322, password min 8 characters, display errors)
- [x] T031 [US1] Implement registration API call in SignupForm (POST to /api/v1/auth/register, handle success/error, store JWT in cookie)
- [x] T032 [US1] Add redirect to dashboard after successful registration in SignupForm
- [x] T033 [US1] Mount auth router in backend/app/main.py (app.include_router with /api/v1 prefix)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Sign-In (Priority: P1)

**Goal**: Enable registered users to authenticate with email/password and receive JWT token

**Independent Test**: Submit valid credentials, verify JWT token returned with correct user claims, stored in httpOnly cookie

### Implementation for User Story 2

- [ ] T034 [P] [US2] Create UserLogin Pydantic schema in backend/app/schemas/auth.py (email EmailStr, password string)
- [ ] T035 [US2] Implement user sign-in endpoint POST /api/v1/auth/signin in backend/app/routers/auth.py (verify email exists, verify password hash, return JWT)
- [ ] T036 [US2] Add password verification logic in sign-in endpoint (use passlib bcrypt verify, constant-time comparison)
- [ ] T037 [US2] Add generic error message for invalid credentials in sign-in endpoint (same error for email not found and wrong password)
- [ ] T038 [US2] Integrate Better Auth JWT token issuance in sign-in endpoint (include user_id, email, iat, exp claims)
- [ ] T039 [P] [US2] Create sign-in page in frontend/app/(auth)/signin/page.tsx (Server Component with metadata)
- [ ] T040 [P] [US2] Create SigninForm component in frontend/components/auth/SigninForm.tsx (Client Component with form, API call)
- [ ] T041 [US2] Implement sign-in form validation in SigninForm (email format, required fields, display errors)
- [ ] T042 [US2] Implement sign-in API call in SigninForm (POST to /api/v1/auth/signin, handle success/error, store JWT)
- [ ] T043 [US2] Add redirect to dashboard after successful sign-in in SigninForm

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Protected API Access (Priority: P1)

**Goal**: Enforce JWT authentication on protected endpoints and extract user identity for authorization

**Independent Test**: Make API request with valid JWT, verify user ID extracted correctly; make request without JWT, verify 401 Unauthorized returned

### Implementation for User Story 3

- [ ] T044 [US3] Implement GET /api/v1/auth/me endpoint in backend/app/routers/auth.py (protected, returns current user from JWT claims)
- [ ] T045 [US3] Add Depends(get_current_user) to /auth/me endpoint to enforce JWT verification
- [ ] T046 [US3] Test JWT verification middleware with invalid token (should return 401 with "Could not validate credentials")
- [ ] T047 [US3] Test JWT verification middleware with missing token (should return 401 with "Not authenticated")
- [ ] T048 [US3] Test JWT verification middleware with expired token (should return 401 with "Token expired")
- [ ] T049 [P] [US3] Create protected dashboard page in frontend/app/dashboard/page.tsx (Server Component that fetches /api/v1/auth/me)
- [ ] T050 [P] [US3] Create route middleware in frontend/app/middleware.ts to check JWT before accessing /dashboard routes
- [ ] T051 [US3] Implement automatic redirect to /signin when 401 is returned from protected endpoints in frontend API client
- [ ] T052 [US3] Test that unauthorized access to /dashboard redirects to /signin page
- [ ] T053 [US3] Add user info display in dashboard (email, created date) fetched from /api/v1/auth/me

**Checkpoint**: All P1 user stories (registration, sign-in, protected access) should now be independently functional

---

## Phase 6: User Story 4 - Token Expiration & Re-authentication (Priority: P2)

**Goal**: Enforce JWT token expiration (1 hour) and require re-authentication for expired tokens

**Independent Test**: Wait 1 hour (or manipulate exp claim in tests), make API request with expired token, verify 401 returned and user redirected to sign-in

### Implementation for User Story 4

- [ ] T054 [US4] Verify JWT expiration claim (exp) is set correctly in token issuance (iat + 3600 seconds)
- [ ] T055 [US4] Implement expiration check in backend JWT verification (jose.jwt.decode validates exp automatically)
- [ ] T056 [US4] Add specific error message "Token expired. Please sign in again." for expired tokens in backend
- [ ] T057 [US4] Implement frontend token expiration detection in API client (intercept 401, check for expiration message)
- [ ] T058 [US4] Clear JWT cookie on frontend when token expires (document.cookie with Max-Age=0)
- [ ] T059 [US4] Display user-friendly message on sign-in page after token expiration ("Session expired. Please sign in again.")

**Checkpoint**: Token expiration security feature is now functional

---

## Phase 7: User Story 5 - Sign-Out (Priority: P3)

**Goal**: Allow users to explicitly end their session by clearing the JWT token

**Independent Test**: Sign in, click sign-out, verify token cleared and subsequent API requests return 401

### Implementation for User Story 5

- [ ] T060 [US5] Implement POST /api/v1/auth/signout endpoint in backend/app/routers/auth.py (protected, returns success message)
- [ ] T061 [US5] Add Depends(get_current_user) to /auth/signout to require authentication before sign-out
- [ ] T062 [P] [US5] Create SignoutButton component in frontend/components/auth/SignoutButton.tsx (Client Component with API call)
- [ ] T063 [US5] Implement sign-out API call in SignoutButton (POST to /api/v1/auth/signout, clear JWT cookie)
- [ ] T064 [US5] Clear JWT token cookie on frontend in SignoutButton (set Max-Age=0)
- [ ] T065 [US5] Redirect to /signin page after successful sign-out in SignoutButton
- [ ] T066 [US5] Add SignoutButton to dashboard page navigation in frontend/app/dashboard/page.tsx

**Checkpoint**: All user stories (P1, P2, P3) should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T067 [P] Add CORS configuration to FastAPI main.py (allow frontend origin, credentials=True, specific methods/headers)
- [ ] T068 [P] Create reusable UI components in frontend/components/ui/ (Button.tsx, Input.tsx for forms)
- [ ] T069 [P] Add error handling to all API endpoints (catch exceptions, return 500 with generic message, log details)
- [ ] T070 [P] Add request/response logging to backend (structured logging, no sensitive data like passwords or tokens)
- [ ] T071 [P] Create backend README.md with setup instructions, environment variables, API documentation links
- [ ] T072 [P] Create frontend README.md with setup instructions, environment variables, development workflow
- [ ] T073 [P] Add OpenAPI documentation to FastAPI (auto-generated at /docs and /redoc)
- [ ] T074 [P] Create .env.example templates with placeholder values and comments for both frontend and backend
- [ ] T075 [P] Add rate limiting middleware to authentication endpoints (5 attempts per email per 15 minutes - optional but recommended)
- [ ] T076 Validate all authentication flows end-to-end (registration → sign-in → protected access → token expiration → sign-out)
- [ ] T077 Run quickstart.md validation (follow setup guide, verify all steps work, update if needed)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Independent of US1 (but typically implemented after for logical flow)
- **User Story 3 (P1)**: Requires US1 and US2 to be testable (needs users in database), but technically independent
- **User Story 4 (P2)**: Can start after Foundational - Enhances US2/US3 security
- **User Story 5 (P3)**: Requires US2 (sign-in) to be complete - Adds sign-out to existing auth flow

### Within Each User Story

- Models and schemas (Pydantic/SQLModel) can be created in parallel
- Backend endpoints depend on models/schemas being complete
- Frontend components can be created in parallel
- Frontend API integration depends on backend endpoints being complete
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, multiple user stories can be worked on in parallel by different developers
- Within each user story:
  - Models/schemas marked [P] can run in parallel
  - Frontend components marked [P] can run in parallel
  - Backend endpoints and frontend pages can be developed in parallel (using API contracts)

---

## Parallel Example: User Story 1 (Registration)

```bash
# Launch models and schemas in parallel:
Task: "Create User SQLModel entity in backend/app/models/user.py"
Task: "Create UserCreate Pydantic schema in backend/app/schemas/auth.py"
Task: "Create UserResponse Pydantic schema in backend/app/schemas/user.py"
Task: "Create TokenResponse Pydantic schema in backend/app/schemas/auth.py"

# After schemas complete, launch frontend components in parallel:
Task: "Create registration page in frontend/app/(auth)/signup/page.tsx"
Task: "Create SignupForm component in frontend/components/auth/SignupForm.tsx"

# Backend endpoint and frontend integration happen sequentially:
Task: "Implement user registration endpoint POST /api/v1/auth/register"
Then: "Implement registration API call in SignupForm"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Registration)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Registration) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Sign-In) → Test independently → Deploy/Demo
4. Add User Story 3 (Protected Access) → Test independently → Deploy/Demo
5. Add User Story 4 (Token Expiration) → Test independently → Deploy/Demo
6. Add User Story 5 (Sign-Out) → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Registration)
   - Developer B: User Story 2 (Sign-In)
   - Developer C: User Story 3 (Protected Access)
3. User Story 4 and 5 can be added by any developer after their dependencies complete
4. Stories complete and integrate independently

---

## Task Summary

**Total Tasks**: 77
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 12 tasks (BLOCKING)
- Phase 3 (US1 - Registration): 14 tasks
- Phase 4 (US2 - Sign-In): 10 tasks
- Phase 5 (US3 - Protected Access): 10 tasks
- Phase 6 (US4 - Token Expiration): 6 tasks
- Phase 7 (US5 - Sign-Out): 7 tasks
- Phase 8 (Polish): 11 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**User Story Distribution**:
- US1: 14 tasks (18% of total)
- US2: 10 tasks (13% of total)
- US3: 10 tasks (13% of total)
- US4: 6 tasks (8% of total)
- US5: 7 tasks (9% of total)
- Infrastructure: 30 tasks (39% of total)

**Critical Path**: Setup → Foundational → US1 → US2 → US3 → US4 → US5 → Polish

**Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1) = 33 tasks = Minimum viable authentication system

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

**Tasks Generated**: 2026-01-11
**Ready for Implementation**: ✅ All user stories have clear, actionable tasks with exact file paths
**Next Step**: Begin Phase 1 (Setup) tasks
