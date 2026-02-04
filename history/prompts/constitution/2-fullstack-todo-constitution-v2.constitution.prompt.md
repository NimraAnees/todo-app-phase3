---
id: 2
title: Full-Stack Todo Constitution v2.0.0
stage: constitution
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: system
command: /sp.constitution
labels: ["constitution", "security", "architecture", "full-stack", "authentication"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitution update)
---

## Prompt

Project: Full-Stack Todo Web Application (Spec-Driven, Authenticated, Production-Ready)

Core principles:
- **Security by default** – Authentication and authorization are mandatory across the system
- **User data isolation** – Users can only access and modify their own tasks
- **Spec-driven development** – All implementation must strictly follow defined specifications
- **Separation of concerns** – Frontend, backend, and authentication layers remain cleanly decoupled
- **Production readiness** – Code and architecture must be deployable and maintainable

Key standards:
- All REST APIs must follow RESTful design conventions
- Every protected endpoint must require a valid JWT
- JWTs must be verified server-side using a shared secret
- Backend must never trust client-provided user identifiers without token verification
- Database queries must always be scoped to the authenticated user
- Proper HTTP status codes must be returned (401, 403, 404, 500)
- API request and response schemas must be explicit and consistent
- Sensitive data must never be exposed in logs or responses

Technology standards:
- Frontend: Next.js 16+ (App Router)
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT-based)
- Spec tooling: Claude Code + Spec-Kit Plus

Security constraints:
- JWT signing and verification must use a shared secret via `BETTER_AUTH_SECRET`
- Tokens must have an explicit expiration policy
- Requests without valid JWT must return `401 Unauthorized`
- Cross-user data access must be impossible by design
- Authorization checks must be enforced at the API and database layers

Architecture constraints:
- Authentication must be stateless on the backend
- Backend must not depend on frontend session storage
- Frontend must attach JWT tokens to every API request
- Business logic must remain independent of UI logic
- Each spec must remain independently testable

Success criteria:
- All task CRUD operations work only for authenticated users
- Users cannot read or modify tasks belonging to other users
- All 5 Basic Level features are implemented end-to-end
- All three specs (backend, frontend, and authentication) are fully implemented and integrated
- Frontend, backend, and database integrate seamlessly
- API behavior strictly matches the defined specs
- The application is secure, stable, and spec-compliant

## Response snapshot

Constitution successfully updated from version 1.0.0 to 2.0.0 (MAJOR version bump).

**Key Changes:**
- Transformed from "Phase I: In-Memory Console First" to "Full-Stack Todo Web Application"
- Removed console-app specific principles (Phase-First Focus, In-Memory Constraint, Evolvability)
- Added security-first principles: Security by Default, User Data Isolation
- Added production-ready principles: Spec-Driven Development, Production Readiness
- Kept and expanded: Simplicity, Determinism, Separation of Concerns

**New Sections:**
- Technology Standards (explicit tech stack mandate)
- Security Constraints (8 non-negotiable security rules)
- Architecture Constraints (6 architectural requirements)
- Success Criteria (15-point feature checklist)
- Enhanced Governance with spec-compliance requirements

**Security Highlights:**
- JWT-based authentication with Better Auth
- Stateless backend authentication
- User data isolation at API and database layers
- No cross-user data access possible by design
- All secrets externalized via environment variables

**Template Impact:**
- plan-template.md: Constitution Check will now validate security and architecture principles
- spec-template.md: Requirements must include authentication and data isolation
- tasks-template.md: Tasks must enforce security and multi-user considerations

**Files Modified:**
- `.specify/memory/constitution.md` (complete rewrite)

The constitution now governs a production-ready, multi-user web application with security-first principles and explicit technology constraints.

## Outcome

- ✅ Impact: MAJOR constitutional change (v1.0.0 → v2.0.0) - Transformed from console app to full-stack web application
- 🧪 Tests: No tests required (governance document update)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Create feature specifications following new constitution principles, begin implementing authentication, backend API, and frontend features
- 🧠 Reflection: This is a foundational governance update that establishes security-first, production-ready principles for the entire project. All future specifications and implementations must comply with these principles.

## Evaluation notes (flywheel)

- Failure modes observed: None (successful constitution update)
- Graders run and results (PASS/FAIL): Manual validation PASS - All placeholders filled, no unresolved tokens, semantic versioning correctly applied
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): Apply constitution principles to first feature specification (authentication spec)
