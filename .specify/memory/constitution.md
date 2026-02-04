<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0 (MAJOR)
Modified principles:
  - Removed: "Phase-First Focus" (console-specific)
  - Removed: "In-Memory Constraint (Phase I)" (console-specific)
  - Removed: "Evolvability" (multi-phase evolution no longer applies)
  - Added: "Security by Default" (authentication/authorization mandatory)
  - Added: "User Data Isolation" (multi-user data privacy)
  - Added: "Spec-Driven Development" (formalized workflow)
  - Added: "Production Readiness" (deployment and maintainability)
  - Kept: "Simplicity" (expanded for web context)
  - Kept: "Determinism" (expanded for API context)
  - Kept: "Separation of Concerns" (expanded for full-stack context)
Added sections:
  - Technology Standards (explicit tech stack)
  - Security Constraints (JWT, tokens, authorization)
  - Architecture Constraints (stateless auth, API design)
  - Success Criteria (complete feature checklist)
Removed sections:
  - Phase I Constraints (console app specific)
Modified sections:
  - Code Standards: Transformed from console-focused to full-stack web standards
  - Governance: Enhanced with spec-compliance requirements
Templates requiring updates:
  - ✅ plan-template.md: Constitution Check section will validate new security and architecture principles
  - ✅ spec-template.md: Requirements must include authentication and data isolation
  - ✅ tasks-template.md: Tasks must enforce security and multi-user considerations
  - ℹ️ adr-template.md: No changes needed (generic structure)
  - ℹ️ checklist-template.md: No changes needed (generic structure)
  - ℹ️ phr-template.md: No changes needed (generic structure)
  - ℹ️ agent-file-template.md: No changes needed (generic structure)
Follow-up TODOs:
  - Consider updating README.md to reflect full-stack architecture
  - Update CLAUDE.md if constitution principles reference changes
Ratification Date: 2026-01-11 (initial adoption of Phase I principles)
Last Amended Date: 2026-01-11 (transformed to full-stack web application)
-->

# Full-Stack Todo Web Application Constitution

**Version**: 2.0.0
**Ratified**: 2026-01-11
**Last Amended**: 2026-01-11
**Status**: Active

This constitution governs all architectural, security, and development decisions for the Full-Stack Todo Web Application project. All implementation must comply with these principles.

---

## Core Principles

### Security by Default

Authentication and authorization are mandatory across the entire system. Every protected API endpoint MUST require a valid JWT token. Backend services MUST verify tokens server-side using a shared secret and MUST filter all database queries by authenticated user ID. Users can only access and modify their own data. Cross-user data access is impossible by design.

**Rationale**: Multi-user applications require robust security to protect user data and prevent unauthorized access. Security cannot be retrofitted—it must be embedded from the start.

### User Data Isolation

Users MUST only be able to access and modify their own tasks. Database queries MUST always be scoped to the authenticated user. Backend services MUST never trust client-provided user identifiers without token verification. Authorization checks MUST be enforced at both the API layer and database layer.

**Rationale**: Data privacy and tenant isolation are non-negotiable in multi-user systems. Breaches can result in legal, reputational, and operational damage.

### Spec-Driven Development

All implementation MUST strictly follow defined specifications (spec.md, plan.md, tasks.md). No code may be written without a corresponding specification. All features MUST proceed through the workflow: specification → planning → task breakdown → implementation. Specifications are the authoritative source of requirements and behavior.

**Rationale**: Spec-driven development ensures alignment between stakeholders, eliminates ambiguity, and creates auditable decision records. It enables parallel work, independent testing, and incremental delivery.

### Separation of Concerns

Frontend, backend, and authentication layers MUST remain cleanly decoupled. Business logic MUST be independent of UI logic. Database models MUST be independent of API contracts. Authentication MUST be stateless on the backend. Each layer MUST communicate through well-defined interfaces.

**Rationale**: Clean architecture enables independent testing, parallel development, technology swaps, and long-term maintainability. Coupling creates brittle systems that resist change.

### Simplicity

Prefer clear, minimal designs over complex abstractions. Solutions MUST be understandable and maintainable. Avoid unnecessary complexity that impedes testing, deployment, or comprehension. Use the simplest solution that meets requirements. Do not over-engineer for hypothetical future needs.

**Rationale**: Simplicity reduces cognitive load, accelerates development, minimizes bugs, and lowers maintenance costs. Complexity should be justified by concrete requirements, not speculation.

### Determinism

Application behavior MUST be predictable and repeatable. All API operations MUST produce consistent results given the same inputs and authentication context. Responses MUST follow explicit contracts. Error handling MUST be consistent across all endpoints.

**Rationale**: Deterministic systems are testable, debuggable, and reliable. Non-determinism creates unpredictable failures and erodes user trust.

### Production Readiness

Code and architecture MUST be deployable and maintainable. All secrets MUST be externalized via environment variables. Error messages MUST be user-friendly. Logs MUST NOT expose sensitive data. HTTP status codes MUST be semantically correct (401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error). API documentation MUST be accurate and complete.

**Rationale**: Production-ready systems minimize operational burden, reduce downtime, and provide a professional user experience. Shortcuts in production readiness create technical debt.

---

## Technology Standards

The following technology stack is mandatory for this project:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 16+ (App Router) | React-based UI with server/client components |
| **Backend** | Python FastAPI | RESTful API endpoints with async support |
| **ORM** | SQLModel | Type-safe database operations with Pydantic integration |
| **Database** | Neon Serverless PostgreSQL | Cloud-native persistent storage with autoscaling |
| **Authentication** | Better Auth (JWT-based) | User signup/signin with token issuance |
| **Spec Tooling** | Claude Code + Spec-Kit Plus | Agentic spec-driven workflow automation |

**Technology Change Policy**: Deviations from this stack require explicit architectural review and documented justification via ADR (Architecture Decision Record).

---

## Security Constraints

These security constraints are **non-negotiable**:

1. **JWT Signing and Verification**
   - JWTs MUST be signed and verified using a shared secret stored in `BETTER_AUTH_SECRET` environment variable.
   - Tokens MUST have an explicit expiration policy (e.g., 1 hour access tokens, 7-day refresh tokens).
   - Expired tokens MUST be rejected with `401 Unauthorized`.

2. **Authorization Enforcement**
   - Every protected API endpoint MUST validate the JWT token before processing the request.
   - Requests without a valid JWT MUST return `401 Unauthorized`.
   - The user ID embedded in the JWT MUST match the user ID in the request URL or body.
   - Attempts to access other users' data MUST return `403 Forbidden`.

3. **Database Query Scoping**
   - All database queries MUST filter by `user_id` from the authenticated JWT token.
   - Backend services MUST never accept `user_id` directly from client input without token verification.
   - Cross-user data leakage MUST be architecturally impossible (enforced via query filters and foreign key constraints).

4. **Password Security**
   - Passwords MUST be hashed using bcrypt or argon2 before storage.
   - Plain-text passwords MUST never be stored or logged.
   - Password validation MUST enforce minimum requirements (e.g., 8+ characters, complexity).

5. **Token Storage**
   - Tokens MUST be stored in secure, httpOnly cookies (never localStorage or sessionStorage).
   - Cookies MUST have `Secure` and `SameSite` attributes set appropriately.
   - Token secrets MUST never be hardcoded in source code.

6. **Input Validation**
   - All API inputs MUST be validated using Pydantic models.
   - SQL injection MUST be prevented via ORM parameterized queries.
   - XSS attacks MUST be prevented via proper output encoding.
   - Rate limiting MUST be implemented to prevent abuse.

7. **Secrets Management**
   - All secrets MUST be stored in `.env` file (NEVER committed to git).
   - Required environment variables: `DATABASE_URL`, `JWT_SECRET`, `BETTER_AUTH_SECRET`.
   - Different secrets MUST be used for development and production environments.

8. **Sensitive Data Exposure**
   - Passwords, tokens, and secrets MUST never appear in logs or API responses.
   - Error messages MUST be generic to external users (detailed errors logged internally only).
   - Stack traces MUST never be exposed to clients in production.

---

## Architecture Constraints

1. **Stateless Authentication**
   - Backend authentication MUST be stateless (no server-side session storage).
   - All authentication state MUST be carried in the JWT token.
   - Token verification MUST be performed on every protected request.

2. **No Frontend Session Dependency**
   - Backend MUST NOT depend on frontend session storage mechanisms.
   - Backend MUST authenticate requests solely via JWT tokens.

3. **API Request Contract**
   - Frontend MUST attach JWT tokens to every API request via `Authorization: Bearer <token>` header.
   - API responses MUST follow consistent JSON schemas defined in specifications.

4. **Business Logic Independence**
   - Business logic MUST remain independent of UI logic (no frontend code in backend services).
   - Backend services MUST be testable without a frontend (via contract and integration tests).

5. **Independent Testability**
   - Each specification (authentication, backend API, frontend UI) MUST be independently testable.
   - Tests MUST NOT require the entire system to run (unit and integration tests for each layer).

6. **RESTful Design**
   - All APIs MUST follow RESTful conventions:
     - GET for retrieval (idempotent, no side effects)
     - POST for creation (non-idempotent)
     - PUT/PATCH for updates (idempotent)
     - DELETE for removal (idempotent)
   - Resource URLs MUST be noun-based (e.g., `/api/v1/users/{user_id}/todos`, not `/api/v1/getTodos`).
   - HTTP status codes MUST be semantically correct.

---

## Code Standards

### Backend (FastAPI + SQLModel)

- Use FastAPI dependency injection for database sessions and authentication.
- Define Pydantic models for all request and response schemas.
- Use SQLModel for database models with explicit type hints.
- Implement authentication middleware for protected routes.
- Handle errors gracefully with custom exception handlers.
- Validate all inputs using Pydantic validation.
- Log all errors with structured logging (no sensitive data).
- Document APIs using OpenAPI/Swagger annotations.

### Frontend (Next.js 16+)

- Use App Router conventions (app/ directory structure).
- Separate Server Components (data fetching) from Client Components (interactivity).
- Store JWT tokens in httpOnly cookies (never localStorage).
- Attach tokens to API requests via `Authorization` header.
- Handle loading states (loading.tsx) and error boundaries (error.tsx).
- Implement responsive design (mobile, tablet, desktop).
- Use TypeScript for type safety.
- Validate forms client-side before submission.

### Database (Neon PostgreSQL + SQLModel)

- Define schemas with proper constraints (NOT NULL, UNIQUE, CHECK).
- Use foreign keys to enforce referential integrity.
- Add indexes on frequently queried columns (e.g., user_id, created_at).
- Use migrations for schema changes (version-controlled).
- Filter all queries by `user_id` to enforce data isolation.
- Use connection pooling for scalability.

### General

- Write clear, maintainable code with descriptive variable names.
- Follow single responsibility principle for functions and classes.
- Prefer composition over inheritance.
- Avoid global mutable state.
- Use explicit error handling (no silent failures).
- Write tests for critical paths (authentication, authorization, CRUD).
- Commit frequently with descriptive messages.
- No hardcoded secrets or credentials.

---

## Success Criteria

The project is considered successful when ALL of the following criteria are met:

- [ ] **Authentication**: Users can sign up and sign in with email/password.
- [ ] **JWT Tokens**: Better Auth issues JWT tokens upon successful login.
- [ ] **Protected Endpoints**: All todo CRUD endpoints require valid JWT tokens.
- [ ] **Authorization**: Users can only read/modify their own todos (cross-user access blocked).
- [ ] **CRUD Operations**: Users can create, read, update, and delete todos.
- [ ] **Data Persistence**: All todos are stored in Neon PostgreSQL database.
- [ ] **User Isolation**: Database queries filter by authenticated user ID.
- [ ] **RESTful API**: API follows RESTful conventions with proper status codes.
- [ ] **Responsive UI**: Frontend works on mobile, tablet, and desktop.
- [ ] **Security**: No security vulnerabilities (SQL injection, XSS, CSRF, token leakage).
- [ ] **Spec Compliance**: All three specs (backend, frontend, authentication) fully implemented.
- [ ] **Integration**: Frontend, backend, and database integrate seamlessly.
- [ ] **Error Handling**: User-friendly error messages, no sensitive data leakage.
- [ ] **Environment Config**: All secrets externalized via `.env` file.
- [ ] **Documentation**: API endpoints documented, setup instructions clear.

---

## Governance

### Amendment Process

1. Proposed amendments MUST be documented with rationale.
2. Amendments MUST be reviewed for impact on existing specifications and code.
3. Breaking changes (MAJOR version bumps) require explicit approval.
4. Approved amendments trigger:
   - Version increment (semantic versioning: MAJOR.MINOR.PATCH)
   - Update of `LAST_AMENDED_DATE`
   - Sync Impact Report prepended to this file
   - Updates to dependent templates and specifications
   - Creation of ADRs for significant architectural changes

### Versioning Policy

- **MAJOR (X.0.0)**: Backward-incompatible governance changes, principle removals, or redefinitions.
- **MINOR (X.Y.0)**: New principles added or materially expanded guidance.
- **PATCH (X.Y.Z)**: Clarifications, wording improvements, typo fixes.

### Compliance Review

- All specifications (spec.md, plan.md, tasks.md) MUST reference this constitution.
- Plan templates MUST include a "Constitution Check" section validating compliance.
- Code reviews MUST verify adherence to principles and standards.
- Violations MUST be documented and justified via ADRs or corrected.

### Conflict Resolution

- This constitution is the authoritative source for project decisions.
- In case of conflict between specifications and constitution, constitution takes precedence.
- Unresolved conflicts MUST be escalated for architectural review.

---

**End of Constitution**
