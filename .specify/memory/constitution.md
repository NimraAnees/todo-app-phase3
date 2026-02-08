<!--
SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0 (MAJOR)
Modified principles:
  - Modified: "Security by Default" (expanded for AI agents and JWT usage in tool requests)
  - Modified: "User Data Isolation" (expanded for conversation history and AI tools)
  - Modified: "Separation of Concerns" (expanded for MCP server and AI agents)
  - Modified: "Architecture Constraints" (expanded for stateless AI agents)
  - Modified: "Success Criteria" (updated for Phase III features)
  - Added: "Stateless Backend by Default" (no in-memory session state for AI agents)
  - Added: "Tool-Driven AI Operations" (AI agents must use MCP tools for all actions)
  - Added: "MCP Server Integration" (mandates MCP server for all task operations)
  - Added: "AI Agent Determinism" (ensures consistent, auditable behavior)
  - Added: "Conversation History Persistence" (mandates persistent conversation storage)
Modified sections:
  - Technology Standards: Updated to include AI Framework and MCP Server
  - Code Standards: Expanded to include AI/MCP server patterns
  - Success Criteria: Updated for Phase III deliverables
Templates requiring updates:
  - ✅ plan-template.md: Constitution Check section updated to validate new AI/MCP principles
  - ✅ spec-template.md: Requirements must include AI/MCP integration
  - ✅ tasks-template.md: Tasks must enforce AI/MCP and stateless considerations
  - ℹ️ adr-template.md: No changes needed (generic structure)
  - ℹ️ checklist-template.md: No changes needed (generic structure)
  - ℹ️ phr-template.md: No changes needed (generic structure)
  - ℹ️ agent-file-template.md: No changes needed (generic structure)
Follow-up TODOs:
  - Consider updating README.md to reflect AI-powered chatbot architecture
  - Update CLAUDE.md if constitution principles reference changes
Ratification Date: 2026-01-11 (initial adoption of Phase I principles)
Last Amended Date: 2026-02-06 (expanded to AI-powered chatbot with MCP tools)
-->

# AI-Powered Todo Chatbot Constitution

**Version**: 3.0.0
**Ratified**: 2026-01-11
**Last Amended**: 2026-02-06
**Status**: Active

This constitution governs all architectural, security, and development decisions for the AI-Powered Todo Chatbot project. All implementation must comply with these principles.

---

## Core Principles

### Stateless Backend by Default

The backend system MUST be stateless with no in-memory session state. AI agents and MCP tools MUST NOT rely on server-side session storage or cached conversation context. Every request MUST contain all necessary information to process the operation. Conversation history MUST be retrieved from the database for each interaction. No session state MAY be maintained in memory between requests.

**Rationale**: Statelessness ensures scalability, reliability, and deterministic behavior in AI-powered systems. Memory-based session state creates bottlenecks and failure points that impede horizontal scaling and system resilience.

### Tool-Driven AI Operations

All task operations within the AI system MUST be executed through MCP tools. AI agents MUST NOT directly access the database or perform operations outside the established MCP tool framework. Every task creation, modification, deletion, and retrieval MUST occur via MCP tool invocation. This constraint ensures all operations are logged, auditable, and consistent with system security policies.

**Rationale**: Tool-driven operations provide centralized control, audit trails, and security enforcement. Direct database access by AI agents creates security vulnerabilities and bypasses authentication/authorization controls.

### MCP Server Integration

MCP server integration is mandatory across the entire AI system. All AI agents MUST interact with the system exclusively through officially defined MCP tools. The MCP server MUST handle authentication, authorization, and business logic enforcement. MCP tools MUST be stateless and carry all necessary authentication context with each invocation.

**Rationale**: MCP server integration centralizes access control, provides consistent tool interfaces, and ensures all operations follow established protocols. This creates a deterministic, auditable system architecture.

### AI Agent Determinism

AI agent behavior MUST be predictable and auditable. All agent operations MUST produce consistent results given the same inputs and authentication context. Agent responses MUST be logged with structured metadata. Error handling within AI agents MUST be consistent and follow explicit contracts. Agent behavior MUST be reproducible for debugging and compliance purposes.

**Rationale**: Deterministic AI agents are essential for security, reliability, and user trust. Non-deterministic behavior creates unpredictable failures, security vulnerabilities, and compliance risks.

### Conversation History Persistence

All conversation history MUST be stored persistently in the database. Each conversation turn MUST be recorded with timestamp, user ID, agent response, and any invoked tool calls. Conversation context MUST be reconstructible from database records for continuity across requests and system restarts. Historical conversations MUST be retrievable by authenticated users.

**Rationale**: Persistent conversation history enables continuity, provides audit trails, and supports user review of AI interactions. Without persistence, users lose context and cannot review previous interactions.

### Security by Default

Authentication and authorization are mandatory across the entire system. Every protected API endpoint, chat endpoint, and MCP tool invocation MUST require a valid JWT token. Backend services MUST verify tokens server-side using a shared secret and MUST filter all database queries by authenticated user ID. Users can only access and modify their own data. Cross-user data access is impossible by design. All AI agent operations MUST validate JWT tokens and enforce user isolation.

**Rationale**: Multi-user applications require robust security to protect user data and prevent unauthorized access. Security cannot be retrofitted—it must be embedded from the start.

### User Data Isolation

Users MUST only be able to access and modify their own tasks and conversations. Database queries MUST always be scoped to the authenticated user. Backend services MUST never trust client-provided user identifiers without token verification. Authorization checks MUST be enforced at the API layer, MCP tool layer, and database layer. Conversation histories MUST be isolated by user ID.

**Rationale**: Data privacy and tenant isolation are non-negotiable in multi-user systems. Breaches can result in legal, reputational, and operational damage.

### Spec-Driven Development

All implementation MUST strictly follow defined specifications (spec.md, plan.md, tasks.md). No code may be written without a corresponding specification. All features MUST proceed through the workflow: specification → planning → task breakdown → implementation. Specifications are the authoritative source of requirements and behavior.

**Rationale**: Spec-driven development ensures alignment between stakeholders, eliminates ambiguity, and creates auditable decision records. It enables parallel work, independent testing, and incremental delivery.

### Separation of Concerns

Frontend, backend, authentication, and AI agent layers MUST remain cleanly decoupled. Business logic MUST be independent of UI logic. Database models MUST be independent of API contracts and MCP tool interfaces. Authentication MUST be stateless on the backend. MCP servers MUST be independent of AI agent implementations. Each layer MUST communicate through well-defined interfaces.

**Rationale**: Clean architecture enables independent testing, parallel development, technology swaps, and long-term maintainability. Coupling creates brittle systems that resist change.

### Simplicity

Prefer clear, minimal designs over complex abstractions. Solutions MUST be understandable and maintainable. Avoid unnecessary complexity that impedes testing, deployment, or comprehension. Use the simplest solution that meets requirements. Do not over-engineer for hypothetical future needs.

**Rationale**: Simplicity reduces cognitive load, accelerates development, minimizes bugs, and lowers maintenance costs. Complexity should be justified by concrete requirements, not speculation.

### Production Readiness

Code and architecture MUST be deployable and maintainable. All secrets MUST be externalized via environment variables. Error messages MUST be user-friendly. Logs MUST NOT expose sensitive data. HTTP status codes MUST be semantically correct (401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error). API documentation MUST be accurate and complete. AI agent responses MUST be sanitized before presentation to users.

**Rationale**: Production-ready systems minimize operational burden, reduce downtime, and provide a professional user experience. Shortcuts in production readiness create technical debt.

---

## Technology Standards

The following technology stack is mandatory for this project:

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | OpenAI ChatKit | Natural language conversation interface |
| **Backend** | Python FastAPI | RESTful API endpoints with async support |
| **AI Framework** | OpenAI Agents SDK | AI agent orchestration and management |
| **MCP Server** | Official MCP SDK | Tool invocation and external system integration |
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
   - All MCP tool invocations MUST validate JWT tokens before execution.

2. **Authorization Enforcement**
   - Every protected API endpoint, chat endpoint, and MCP tool MUST validate the JWT token before processing the request.
   - Requests without a valid JWT MUST return `401 Unauthorized`.
   - The user ID embedded in the JWT MUST match the user ID in the request URL, body, or MCP tool context.
   - Attempts to access other users' data via AI agents or MCP tools MUST return `403 Forbidden`.

3. **Database Query Scoping**
   - All database queries MUST filter by `user_id` from the authenticated JWT token.
   - Backend services and MCP tools MUST never accept `user_id` directly from client input without token verification.
   - Cross-user data leakage MUST be architecturally impossible (enforced via query filters and foreign key constraints).
   - Conversation history queries MUST be scoped to authenticated user ID.

4. **AI Agent Security**
   - AI agents MUST NOT store user data or tokens in their internal memory between requests.
   - All tool inputs MUST be validated and sanitized before MCP tool invocation.
   - AI agents MUST NOT have direct database access - all operations MUST go through MCP tools.
   - Tool responses MUST be filtered to prevent cross-user data exposure.

5. **Password Security**
   - Passwords MUST be hashed using bcrypt or argon2 before storage.
   - Plain-text passwords MUST never be stored or logged.
   - Password validation MUST enforce minimum requirements (e.g., 8+ characters, complexity).

6. **Token Storage**
   - Tokens MUST be stored in secure, httpOnly cookies (never localStorage or sessionStorage).
   - Cookies MUST have `Secure` and `SameSite` attributes set appropriately.
   - Token secrets MUST never be hardcoded in source code.
   - MCP tools MUST receive tokens securely through proper authentication flows.

7. **Input Validation**
   - All API inputs MUST be validated using Pydantic models.
   - SQL injection MUST be prevented via ORM parameterized queries.
   - XSS attacks MUST be prevented via proper output encoding.
   - Natural language inputs to AI agents MUST be sanitized to prevent prompt injection.
   - Rate limiting MUST be implemented to prevent abuse.

8. **Secrets Management**
   - All secrets MUST be stored in `.env` file (NEVER committed to git).
   - Required environment variables: `DATABASE_URL`, `JWT_SECRET`, `BETTER_AUTH_SECRET`, `OPENAI_API_KEY`, `MCP_SECRET`.
   - Different secrets MUST be used for development and production environments.

9. **Sensitive Data Exposure**
   - Passwords, tokens, and secrets MUST never appear in logs, API responses, or AI agent outputs.
   - Error messages MUST be generic to external users (detailed errors logged internally only).
   - Stack traces MUST never be exposed to clients in production.
   - AI agent responses MUST not leak internal system information or sensitive data.

---

## Architecture Constraints

1. **Stateless Authentication**
   - Backend authentication MUST be stateless (no server-side session storage).
   - All authentication state MUST be carried in the JWT token.
   - Token verification MUST be performed on every protected request and MCP tool invocation.

2. **No Frontend Session Dependency**
   - Backend MUST NOT depend on frontend session storage mechanisms.
   - Backend MUST authenticate requests solely via JWT tokens.
   - AI agents MUST NOT rely on frontend-stored conversation state.

3. **API Request Contract**
   - Frontend MUST attach JWT tokens to every API request via `Authorization: Bearer <token>` header.
   - API responses MUST follow consistent JSON schemas defined in specifications.
   - MCP tool responses MUST follow consistent formats and include authentication context.

4. **Business Logic Independence**
   - Business logic MUST remain independent of UI logic (no frontend code in backend services).
   - Backend services MUST be testable without a frontend (via contract and integration tests).
   - MCP tools MUST encapsulate business logic and enforce security policies.

5. **Independent Testability**
   - Each specification (authentication, backend API, frontend UI, AI agents) MUST be independently testable.
   - Tests MUST NOT require the entire system to run (unit and integration tests for each layer).
   - MCP tool tests MUST be isolated and repeatable.

6. **RESTful and Tool Design**
   - All APIs MUST follow RESTful conventions:
     - GET for retrieval (idempotent, no side effects)
     - POST for creation (non-idempotent)
     - PUT/PATCH for updates (idempotent)
     - DELETE for removal (idempotent)
   - MCP tools MUST follow consistent patterns with proper error handling.
   - Resource URLs MUST be noun-based (e.g., `/api/v1/users/{user_id}/todos`, not `/api/v1/getTodos`).
   - HTTP status codes MUST be semantically correct.

7. **Stateless AI Architecture**
   - AI agents MUST NOT maintain in-memory session state between requests.
   - All conversation context MUST be reconstructed from persistent storage for each interaction.
   - MCP tools MUST be stateless and process each invocation independently.
   - System restarts MUST NOT lose conversation history or context.

---

## Code Standards

### Backend (FastAPI + SQLModel)

- Use FastAPI dependency injection for database sessions, authentication, and MCP services.
- Define Pydantic models for all request and response schemas.
- Use SQLModel for database models with explicit type hints.
- Implement authentication middleware for protected routes.
- Handle errors gracefully with custom exception handlers.
- Validate all inputs using Pydantic validation.
- Log all errors with structured logging (no sensitive data).
- Document APIs using OpenAPI/Swagger annotations.
- Implement proper JWT token validation in all endpoints.

### Frontend (OpenAI ChatKit)

- Use OpenAI ChatKit for conversation interface.
- Implement proper authentication flow before initializing chat.
- Store JWT tokens in httpOnly cookies (never localStorage).
- Attach tokens to API requests via `Authorization` header.
- Handle loading states and error boundaries appropriately.
- Implement responsive design (mobile, tablet, desktop).
- Sanitize AI agent responses before displaying to users.

### AI Framework (OpenAI Agents SDK)

- Use OpenAI Agents SDK for agent orchestration.
- Implement proper authentication and authorization before agent execution.
- Configure agents to use MCP tools for all task operations.
- Store conversation history in database with proper user isolation.
- Log all agent interactions and tool calls for audit purposes.
- Implement error handling for agent failures and tool invocations.

### MCP Server (MCP SDK)

- Implement MCP tools following official specifications.
- Ensure all MCP tools validate JWT tokens and enforce user isolation.
- MCP tools MUST be stateless and process requests independently.
- MCP tools MUST encapsulate business logic and database operations.
- Implement proper error handling and response formatting for MCP tools.

### Database (Neon PostgreSQL + SQLModel)

- Define schemas with proper constraints (NOT NULL, UNIQUE, CHECK).
- Use foreign keys to enforce referential integrity.
- Add indexes on frequently queried columns (e.g., user_id, created_at, conversation_id).
- Use migrations for schema changes (version-controlled).
- Filter all queries by `user_id` to enforce data isolation.
- Use connection pooling for scalability.
- Design schemas to support conversation history persistence.

### General

- Write clear, maintainable code with descriptive variable names.
- Follow single responsibility principle for functions and classes.
- Prefer composition over inheritance.
- Avoid global mutable state.
- Use explicit error handling (no silent failures).
- Write tests for critical paths (authentication, authorization, CRUD, AI interactions).
- Commit frequently with descriptive messages.
- No hardcoded secrets or credentials.
- Ensure AI agents do not retain user data in memory between requests.

---

## Success Criteria

The project is considered successful when ALL of the following criteria are met:

- [ ] **Authentication**: Users can sign up and sign in with email/password.
- [ ] **JWT Tokens**: Better Auth issues JWT tokens upon successful login.
- [ ] **Protected Endpoints**: All chat and todo CRUD endpoints require valid JWT tokens.
- [ ] **Authorization**: Users can only read/modify their own todos and conversations (cross-user access blocked).
- [ ] **CRUD Operations**: Users can create, read, update, and delete todos via AI chat.
- [ ] **Data Persistence**: All todos and conversations are stored in Neon PostgreSQL database.
- [ ] **User Isolation**: Database queries filter by authenticated user ID for all operations.
- [ ] **RESTful API**: API follows RESTful conventions with proper status codes.
- [ ] **AI Agent Integration**: AI agents correctly invoke MCP tools for all operations.
- [ ] **MCP Tool Implementation**: MCP tools handle all task operations with proper authentication.
- [ ] **Conversation Persistence**: All conversation history persists across requests and restarts.
- [ ] **Stateless Architecture**: Backend maintains no in-memory session state.
- [ ] **Chat Interface**: Users can manage todos via natural language chat.
- [ ] **Responsive UI**: Frontend works on mobile, tablet, and desktop.
- [ ] **Security**: No security vulnerabilities (SQL injection, XSS, CSRF, token leakage, prompt injection).
- [ ] **Spec Compliance**: All specs (backend, frontend, authentication, AI agents) fully implemented.
- [ ] **Integration**: Frontend, backend, AI agents, and MCP tools integrate seamlessly.
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