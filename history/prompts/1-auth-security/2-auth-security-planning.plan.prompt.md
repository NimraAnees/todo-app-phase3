---
id: 2
title: Auth Security Implementation Plan
stage: plan
date: 2026-01-11
surface: agent
model: claude-sonnet-4-5
feature: 1-auth-security
branch: 1-auth-security
user: system
command: /sp.plan
labels: ["authentication", "security", "jwt", "planning", "architecture", "better-auth", "fastapi"]
links:
  spec: specs/1-auth-security/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-auth-security/plan.md
  - specs/1-auth-security/research.md
  - specs/1-auth-security/data-model.md
  - specs/1-auth-security/contracts/auth-api.yaml
  - specs/1-auth-security/contracts/jwt-schema.json
  - specs/1-auth-security/quickstart.md
tests:
  - Constitution Check validation (15/15 items passed)
  - Phase 0: Research completed (10 decisions documented)
  - Phase 1: Design artifacts generated (data model, API contracts, quickstart)
---

## Prompt

Authentication & Security Layer Execution Plan

Objective:
Implement a secure, stateless authentication system connecting the Next.js frontend and FastAPI backend using JWT.

Steps:
- Configure Better Auth in the Next.js application
- Enable JWT plugin and define token expiry
- Set `BETTER_AUTH_SECRET` in frontend and backend environments
- Implement JWT extraction and verification middleware in FastAPI
- Reject unauthorized requests with proper HTTP status codes
- Validate decoded user identity from JWT

Deliverables:
- Working signup/signin flow
- JWT issued on login
- Backend successfully validates tokens
- Unauthorized access is blocked

## Response snapshot

Created comprehensive implementation plan with complete architecture design for authentication system:

**Plan Structure**:
1. Summary and technical approach
2. Technical Context (languages, dependencies, storage, testing, performance goals)
3. Constitution Check (15/15 gates passed - full compliance)
4. Project Structure (frontend + backend separation)
5. Phase 0: Research & Resolution (10 technical decisions documented)
6. Phase 1: Design & Contracts (4 artifacts generated)
7. Phase 2: Ready for `/sp.tasks` command

**Constitution Check Results**: ✅ 15/15 PASSED
- Security by Default ✅
- User Data Isolation ✅
- Spec-Driven Development ✅
- Separation of Concerns ✅
- Simplicity ✅
- Determinism ✅
- Production Readiness ✅
- Technology Standards ✅
- Security Constraints (8 rules) ✅
- Architecture Constraints (6 rules) ✅

**Phase 0: Research Decisions**:
1. Better Auth integration with Next.js 16+ App Router
2. FastAPI JWT verification with python-jose (HS256)
3. Password hashing with bcrypt (work factor 12)
4. JWT token claims: sub, email, iat, exp (minimal)
5. Authorization: Bearer header for token transport
6. Generic error messages for user enumeration prevention
7. Token expiration handling (redirect to /signin on 401)
8. Database schema with UUID, minimal fields
9. Shared BETTER_AUTH_SECRET across frontend/backend
10. CORS configuration with credentials-enabled

**Phase 1: Design Artifacts**:
1. **data-model.md**: User entity with SQLModel/Pydantic schemas
   - User table: id (UUID), email (UNIQUE), password_hash, created_at, updated_at
   - Request schemas: UserCreate, UserLogin
   - Response schemas: UserResponse, TokenResponse
   - Migration scripts with rollback

2. **contracts/auth-api.yaml**: OpenAPI 3.0.3 specification
   - POST /api/v1/auth/register (registration endpoint)
   - POST /api/v1/auth/signin (sign-in endpoint)
   - POST /api/v1/auth/signout (sign-out endpoint, protected)
   - GET /api/v1/auth/me (current user endpoint, protected)
   - Full request/response schemas with examples
   - Error response schemas (401, 403, 422, 500)

3. **contracts/jwt-schema.json**: JSON Schema for JWT claims
   - Required claims: sub (UUID), email, iat, exp
   - Optional claim: iss (issuer)
   - Signing: HS256 with BETTER_AUTH_SECRET
   - Expiration: 3600 seconds (1 hour)
   - Validation rules and security notes

4. **quickstart.md**: Complete local development guide
   - Prerequisites and quick start (5 minutes)
   - Environment variable setup (frontend + backend)
   - Database setup (Neon or local PostgreSQL)
   - Testing authentication flow (curl examples)
   - Manual testing via frontend (step-by-step)
   - API documentation links (Swagger, ReDoc)
   - Troubleshooting common issues
   - Development workflow and testing checklist

**Architecture Highlights**:
- **Stateless Authentication**: JWT carries all state, no server sessions
- **Security-First**: httpOnly cookies, Secure flag, SameSite=Strict
- **User Enumeration Prevention**: Generic error messages, constant-time operations
- **Token Verification**: HMAC-SHA256 signature with shared secret
- **Password Security**: Bcrypt hashing with work factor 12
- **CORS Configuration**: Credentials-enabled with specific origins

**Project Structure**:
- Backend: FastAPI with routers, models, schemas, middleware, core (security, config)
- Frontend: Next.js App Router with (auth) routes, components, lib (auth config, API client)
- Separate deployment support with independent testing

**Files Created**:
1. `specs/1-auth-security/plan.md` - Implementation plan
2. `specs/1-auth-security/research.md` - Research findings (10 decisions)
3. `specs/1-auth-security/data-model.md` - User entity schema
4. `specs/1-auth-security/contracts/auth-api.yaml` - OpenAPI spec
5. `specs/1-auth-security/contracts/jwt-schema.json` - JWT claims schema
6. `specs/1-auth-security/quickstart.md` - Development guide

**Next Phase**: Run `/sp.tasks` to generate implementation tasks organized by user story (P1/P2/P3 priority)

## Outcome

- ✅ Impact: Complete architecture plan with 6 design artifacts covering research, data model, API contracts, JWT schema, and quickstart guide
- 🧪 Tests: Constitution Check passed 15/15 gates - full compliance with security, architecture, and technology standards
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, 2 contracts, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable implementation tasks organized by user story priorities
- 🧠 Reflection: This planning phase demonstrates comprehensive architecture design following spec-driven development. All technical decisions are documented with rationale, alternatives considered, and security implications. The plan fully complies with the constitution's security-by-default and production-readiness principles.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all constitution gates passed
- Graders run and results (PASS/FAIL): Constitution Check PASS (15/15 gates), Phase 0 research PASS (10 decisions documented), Phase 1 design PASS (4 artifacts generated)
- Prompt variant (if applicable): Standard /sp.plan workflow with comprehensive research and design phases
- Next experiment (smallest change to try): Proceed to /sp.tasks phase to validate how well the architecture plan translates into actionable tasks. Monitor if any planning gaps emerge during task generation.
