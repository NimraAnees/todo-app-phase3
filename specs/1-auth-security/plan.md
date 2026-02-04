# Implementation Plan: Authentication & Security Layer

**Branch**: `1-auth-security` | **Date**: 2026-01-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-auth-security/spec.md`

---

## Summary

Implement a secure, stateless authentication system that connects the Next.js frontend and FastAPI backend using JWT tokens issued by Better Auth. The system enables user registration, sign-in, protected API access, token expiration handling, and sign-out functionality. All authentication flows enforce user data isolation through JWT-based identity verification, ensuring users can only access their own resources.

**Technical Approach**: Better Auth library on the frontend issues JWT tokens upon successful authentication. Tokens are stored in httpOnly, Secure, SameSite=Strict cookies to prevent XSS and CSRF attacks. FastAPI backend verifies JWT signatures using a shared `BETTER_AUTH_SECRET` and extracts user identity (`user_id`) from token claims. All protected endpoints require valid JWT tokens and filter database queries by authenticated user ID.

---

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16+ (App Router)
- Backend: Python 3.11+ with FastAPI

**Primary Dependencies**:
- Frontend: Better Auth (v1.x), next (16+), react (19+)
- Backend: FastAPI, python-jose (JWT), passlib (bcrypt), pydantic, sqlmodel

**Storage**: Neon Serverless PostgreSQL with `users` table (id, email, password_hash, created_at, updated_at)

**Testing**:
- Frontend: Jest + React Testing Library for component tests
- Backend: pytest + httpx for API tests
- Contract tests: OpenAPI schema validation

**Target Platform**:
- Frontend: Next.js App Router (deployed to Vercel or similar)
- Backend: FastAPI (deployed to Fly.io, Railway, or AWS Lambda)

**Project Type**: Web application (frontend + backend separation)

**Performance Goals**:
- Token verification overhead: <50ms per request
- Authentication API response time: <2 seconds (p95)
- Registration/sign-in form submission: <1 minute user completion time

**Constraints**:
- Stateless authentication only (no server-side sessions)
- JWT expiration: 1 hour (3600 seconds)
- Password hashing: bcrypt (work factor 12) or argon2
- No refresh token rotation in Phase 2
- No OAuth/social logins in Phase 2
- No password reset flow in Phase 2

**Scale/Scope**:
- Hackathon Phase 2 deliverable
- Target: 100-1000 concurrent users
- Database: Single Neon PostgreSQL instance
- Deployment: Single region (US or EU)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Security by Default
- **Requirement**: Authentication and authorization mandatory across the system
- **Compliance**: JWT tokens required for all protected endpoints. Backend verifies signatures using `BETTER_AUTH_SECRET`. User data queries filtered by authenticated `user_id`.
- **Status**: ✅ PASS

### ✅ User Data Isolation
- **Requirement**: Users can only access/modify their own data
- **Compliance**: JWT claims contain `user_id`. Backend extracts user ID from verified token and filters all queries. Cross-user access returns `403 Forbidden`.
- **Status**: ✅ PASS

### ✅ Spec-Driven Development
- **Requirement**: Implementation follows specifications strictly
- **Compliance**: This plan is derived from `spec.md`. All user stories, functional requirements, and acceptance scenarios guide design decisions.
- **Status**: ✅ PASS

### ✅ Separation of Concerns
- **Requirement**: Frontend, backend, and authentication layers cleanly decoupled
- **Compliance**:
  - Frontend: Better Auth handles token issuance, stored in cookies
  - Backend: JWT verification middleware decouples auth from business logic
  - Database: User model independent of authentication mechanism
- **Status**: ✅ PASS

### ✅ Simplicity
- **Requirement**: Clear, minimal designs over complex abstractions
- **Compliance**:
  - Simple JWT-based stateless authentication (no session management complexity)
  - Standard bcrypt password hashing (no custom crypto)
  - httpOnly cookies for token storage (standard browser security)
  - RESTful API design (standard patterns)
- **Status**: ✅ PASS

### ✅ Determinism
- **Requirement**: Predictable, repeatable application behavior
- **Compliance**:
  - Same credentials always produce same authentication result
  - Token verification is deterministic (valid signature → authenticated, invalid → rejected)
  - Error responses are consistent (`401` for missing/invalid tokens, `403` for unauthorized access)
- **Status**: ✅ PASS

### ✅ Production Readiness
- **Requirement**: Deployable, maintainable, secure
- **Compliance**:
  - Secrets externalized via `.env` (`BETTER_AUTH_SECRET`, `DATABASE_URL`)
  - User-friendly error messages ("Invalid credentials", "Authentication required")
  - No sensitive data in logs (passwords never logged, tokens not logged)
  - Correct HTTP status codes (`401`, `403`, `500`)
- **Status**: ✅ PASS

### ✅ Technology Standards
- **Requirement**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth
- **Compliance**: All required technologies used as specified
- **Status**: ✅ PASS

### ✅ Security Constraints (8 non-negotiable rules)
1. **JWT Signing**: ✅ Signed with `BETTER_AUTH_SECRET`, 1-hour expiration
2. **Authorization Enforcement**: ✅ All protected endpoints validate JWT
3. **Database Query Scoping**: ✅ Queries filtered by `user_id` from token
4. **Password Security**: ✅ Bcrypt hashing, 8+ character minimum
5. **Token Storage**: ✅ httpOnly, Secure, SameSite=Strict cookies
6. **Input Validation**: ✅ Pydantic models for all API inputs
7. **Secrets Management**: ✅ `.env` file, not committed to git
8. **Sensitive Data Exposure**: ✅ Generic error messages, no token/password logging

### ✅ Architecture Constraints (6 requirements)
1. **Stateless Authentication**: ✅ JWT carries all state, no server sessions
2. **No Frontend Session Dependency**: ✅ Backend authenticates via JWT only
3. **API Request Contract**: ✅ `Authorization: Bearer <token>` header
4. **Business Logic Independence**: ✅ Auth middleware separate from routes
5. **Independent Testability**: ✅ Frontend/backend testable separately
6. **RESTful Design**: ✅ POST `/api/auth/register`, POST `/api/auth/signin`, POST `/api/auth/signout`

**Constitution Check Result**: ✅ **ALL GATES PASSED**

---

## Project Structure

### Documentation (this feature)

```text
specs/1-auth-security/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Better Auth + JWT integration research)
├── data-model.md        # Phase 1 output (User entity schema)
├── quickstart.md        # Phase 1 output (Setup and testing guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── auth-api.yaml   # OpenAPI spec for auth endpoints
│   └── jwt-schema.json # JWT token claims schema
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (frontend + backend)

backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── models/
│   │   └── user.py             # SQLModel User entity
│   ├── schemas/
│   │   ├── auth.py             # Pydantic request/response models
│   │   └── user.py             # User response models
│   ├── routers/
│   │   └── auth.py             # Authentication endpoints
│   ├── middleware/
│   │   └── auth_middleware.py  # JWT verification middleware
│   ├── core/
│   │   ├── security.py         # Password hashing, JWT verification
│   │   └── config.py           # Environment variables
│   ├── database.py             # SQLModel database connection
│   └── dependencies.py         # FastAPI dependencies (DB session, current user)
├── tests/
│   ├── contract/
│   │   └── test_auth_contract.py  # OpenAPI contract tests
│   ├── integration/
│   │   └── test_auth_flow.py      # End-to-end auth flow tests
│   └── unit/
│       ├── test_security.py       # Password hashing, JWT tests
│       └── test_auth_endpoints.py # Auth router tests
├── .env.example
├── requirements.txt
└── README.md

frontend/
├── app/
│   ├── (auth)/
│   │   ├── signup/
│   │   │   └── page.tsx        # Registration page
│   │   └── signin/
│   │       └── page.tsx        # Sign-in page
│   ├── dashboard/
│   │   └── page.tsx            # Protected dashboard (requires auth)
│   ├── layout.tsx              # Root layout
│   └── page.tsx                # Landing page
├── components/
│   ├── auth/
│   │   ├── SignupForm.tsx      # Registration form component
│   │   ├── SigninForm.tsx      # Sign-in form component
│   │   └── SignoutButton.tsx   # Sign-out button component
│   └── ui/
│       ├── Button.tsx          # Reusable button component
│       └── Input.tsx           # Reusable input component
├── lib/
│   ├── auth.ts                 # Better Auth configuration
│   ├── api-client.ts           # API client with JWT token handling
│   └── utils.ts                # Utility functions
├── public/
├── .env.local.example
├── package.json
├── tsconfig.json
└── next.config.js
```

**Structure Decision**: Web application structure with separate frontend and backend directories. Frontend uses Next.js App Router conventions (app/ directory). Backend uses FastAPI layered architecture (routers, models, schemas, middleware, core). This structure supports independent deployment, testing, and development.

---

## Complexity Tracking

> **No violations detected** - All constitution requirements are met without needing justifications.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

---


## Phase 0: Research & Resolution ✅

**Status**: ✅ COMPLETE
**Artifact**: [research.md](./research.md)

All technical unknowns have been resolved through comprehensive research:

1. ✅ Better Auth integration with Next.js 16+ App Router
2. ✅ FastAPI JWT verification with python-jose library
3. ✅ Password hashing strategy (bcrypt with work factor 12)
4. ✅ JWT token claims structure (sub, email, iat, exp)
5. ✅ Frontend-backend communication pattern (Authorization: Bearer)
6. ✅ Error handling and user enumeration prevention
7. ✅ Token expiration handling on frontend
8. ✅ Database schema for users table (UUID, minimal fields)
9. ✅ Environment variable management (shared BETTER_AUTH_SECRET)
10. ✅ CORS configuration for cookie-based auth

**Key Decisions**:
- Better Auth for frontend (simpler than NextAuth, JWT-focused)
- python-jose for backend JWT verification (FastAPI standard)
- bcrypt for password hashing (battle-tested, sufficient security)
- Authorization: Bearer header for token transport (RESTful standard)
- Generic error messages to prevent user enumeration attacks

---

## Phase 1: Design & Contracts ✅

**Status**: ✅ COMPLETE
**Artifacts**:
- [data-model.md](./data-model.md) - User entity schema
- [contracts/auth-api.yaml](./contracts/auth-api.yaml) - OpenAPI specification
- [contracts/jwt-schema.json](./contracts/jwt-schema.json) - JWT token claims schema
- [quickstart.md](./quickstart.md) - Local development setup guide

**Data Model**: User entity with UUID id, unique email, password_hash (bcrypt), created_at, updated_at

**API Endpoints**:
1. `POST /api/v1/auth/register` - User registration
2. `POST /api/v1/auth/signin` - User sign-in
3. `POST /api/v1/auth/signout` - User sign-out (protected)
4. `GET /api/v1/auth/me` - Get current user (protected)

**JWT Claims**: sub (user_id), email, iat (issued at), exp (expiration)

**Quickstart**: Complete setup guide with environment variables, database migrations, testing commands

---

## Phase 2: Task Generation → `/sp.tasks`

**Next Command**: `/sp.tasks`

This command will generate `tasks.md` with implementation tasks organized by user story:
- Setup tasks (project initialization)
- Foundational tasks (database, authentication middleware)
- User Story 1: Registration (P1)
- User Story 2: Sign-In (P1)
- User Story 3: Protected API Access (P1)
- User Story 4: Token Expiration (P2)
- User Story 5: Sign-Out (P3)

---

**Implementation Plan Completed**: 2026-01-11
**Status**: ✅ Ready for `/sp.tasks` command
