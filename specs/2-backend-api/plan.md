# Implementation Plan: Backend API & Data Layer

**Branch**: `2-backend-api` | **Date**: 2026-01-13 | **Spec**: [specs/2-backend-api/spec.md](specs/2-backend-api/spec.md)
**Input**: Feature specification from `/specs/2-backend-api/spec.md`

## Summary

Build a secure, user-isolated backend API for task management using FastAPI, SQLModel, and Neon PostgreSQL. The system will provide RESTful CRUD endpoints for tasks, enforced by JWT-based authentication where every database query is strictly scoped to the authenticated user ID to ensure complete data isolation.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: FastAPI, SQLModel, pydantic, alembic, psycopg2-binary, python-jose, passlib  
**Storage**: Neon Serverless PostgreSQL  
**Testing**: pytest  
**Target Platform**: Linux/WSL (Development), Production server  
**Project Type**: Web application (Backend API)  
**Performance Goals**: < 200ms API response time (p95)  
**Constraints**: Stateless JWT auth, Mandatory user\_id filtering  
**Scale/Scope**: MVP for task management  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Security by Default**: Every task endpoint MUST require GET_CURRENT_USER dependency. [PASS]
- **User Data Isolation**: Every SQLModel query MUST include `.where(Task.user_id == user_id)`. [PASS]
- **Spec-Driven Development**: Following SDD workflow from spec.md to tasks.md. [PASS]
- **Separation of Concerns**: Decouple database models from API schemas where necessary. [PASS]
- **Simplicity**: Use standard FastAPI/SQLModel patterns without over-engineering. [PASS]
- **Determinism**: Consistent HTTP status codes (201, 204, 404). [PASS]
- **Production Readiness**: Environment variables for DB\_URL and secrets. [PASS]

## Project Structure

### Documentation (this feature)

```text
specs/2-backend-api/
├── plan.md              # This file
├── research.md          # Implementation decisions
├── data-model.md        # Database schema
├── quickstart.md        # Development setup
├── contracts/           # API contract definitions
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── database.py          # SQLModel engine and session
│   ├── dependencies.py      # Auth and session dependencies
│   ├── core/
│   │   ├── config.py        # Settings and env vars
│   │   └── security.py      # JWT logic
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── models/
│   │   ├── task.py          # NEW: Task model
│   │   └── user.py          # Existing: User model
│   ├── schemas/
│   │   ├── task.py          # NEW: Pydantic schemas for Tasks
│   │   └── user.py
│   └── routers/
│       ├── auth.py          # Existing: Auth routes
│       └── tasks.py         # NEW: Task CRUD routes
├── migrations/              # Alembic/SQL migrations
└── tests/
    ├── conftest.py          # Test fixtures
    └── test_tasks.py        # NEW: Task API tests
```

**Structure Decision**: Using the existing FastAPI structure in the `backend/` directory, extending it with Task-specific models, schemas, and routers.
