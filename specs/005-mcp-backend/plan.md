# Implementation Plan: MCP Backend & Task Tools

**Branch**: `005-mcp-backend` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-mcp-backend/spec.md`

**Note**: This plan transforms existing custom tool implementations into a proper MCP server architecture using the Official MCP SDK.

## Summary

Implement a stateless MCP backend that exposes five task operation tools (add_task, list_tasks, update_task, complete_task, delete_task) using the Official MCP SDK for Python. The implementation will wrap existing tool functionality with MCP protocol layer (JSON-RPC 2.0), integrate stdio transport for local communication between the AI agent and MCP tools, and maintain strict JWT authentication and user data isolation. All tools will persist data to Neon PostgreSQL via SQLModel, return deterministic structured responses, and support cold-start resilience with zero state loss.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI 0.109.0, Official MCP SDK (Python), SQLModel 0.0.14, Neon PostgreSQL (psycopg2-binary), Pydantic 2.5.3
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM; Task and ToolCall models
**Testing**: pytest for unit/integration tests; cold-start validation for statelessness
**Target Platform**: Linux server environment (existing FastAPI deployment)
**Project Type**: Web application backend (integrates MCP server as FastAPI module)
**Performance Goals**: < 1 second response time for tool operations; < 500ms for add_task; handle 100 concurrent requests
**Constraints**: Fully stateless (no in-memory session state); JWT authentication required on every MCP tool invocation; user data isolation enforced at query level
**Scale/Scope**: 5 MCP tools; supports multiple concurrent users; integrates with existing Spec-4 AI agent

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Stateless Backend by Default** | ✅ PASS | MCP tools receive all authentication context (JWT token) with each request; no in-memory session state; database session created and closed per request |
| **Tool-Driven AI Operations** | ✅ PASS | All task operations go through MCP tools; AI agent (Spec-4) uses MCP client to invoke tools; direct database access by agent eliminated |
| **MCP Server Integration** | ✅ PASS | Official MCP SDK integrated; JSON-RPC 2.0 protocol implemented; tools registered with MCP server; authentication context passed through protocol layer |
| **AI Agent Determinism** | ✅ PASS | MCP tools return structured, deterministic JSON responses; same input produces same output; all operations logged in ToolCall audit model |
| **Conversation History Persistence** | ✅ PASS | Not directly in scope; handled by Spec-4; MCP tools focus on task data persistence only |
| **Security by Default** | ✅ PASS | JWT validation on every MCP tool invocation; user_id extracted from token; unauthorized requests return HTTP 401/403 |
| **User Data Isolation** | ✅ PASS | All database queries filtered by authenticated user_id; cross-user access prevented; authorization checked before mutations |
| **Spec-Driven Development** | ✅ PASS | Following SDD workflow: spec → plan → tasks → implement; all decisions documented |
| **Separation of Concerns** | ✅ PASS | MCP layer (tool protocol) separate from business logic (services) separate from data layer (models); AI agent (Spec-4) decoupled from tool implementation |

**Gate Status**: ✅ **PASSED** - All constitution principles satisfied; ready to proceed.

## Project Structure

### Documentation (this feature)

```text
specs/005-mcp-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - MCP SDK integration patterns
├── data-model.md        # Phase 1 output - database schema and tool contracts
├── quickstart.md        # Phase 1 output - setup and deployment guide
├── contracts/           # Phase 1 output - MCP tool specifications
│   └── mcp-tools.yaml   # Tool contract definitions (JSON Schema)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── mcp/                         # NEW: MCP server module
│   │   ├── __init__.py
│   │   ├── server.py                # MCP server initialization with Official SDK
│   │   ├── transport.py             # Stdio transport layer for MCP protocol
│   │   ├── tool_adapter.py          # Adapts existing tools to MCP SDK interface
│   │   └── auth_middleware.py       # JWT validation for MCP requests
│   ├── tools/                       # EXISTING: Task operation tools
│   │   ├── __init__.py              # MODIFY: Export MCP-adapted tools
│   │   ├── base.py                  # MODIFY: Adapt BaseMCPTool to SDK interface
│   │   ├── add_task_tool.py         # MINIMAL CHANGES: Add MCP decorators
│   │   ├── list_tasks_tool.py       # MINIMAL CHANGES: Add MCP decorators
│   │   ├── update_task_tool.py      # MINIMAL CHANGES: Add MCP decorators
│   │   ├── complete_task_tool.py    # MINIMAL CHANGES: Add MCP decorators
│   │   └── delete_task_tool.py      # MINIMAL CHANGES: Add MCP decorators
│   ├── agents/                      # EXISTING: AI agent
│   │   ├── __init__.py
│   │   └── todo_agent.py            # MODIFY: Use MCP client for tool invocation
│   ├── models/                      # EXISTING: SQLModel entities
│   │   ├── __init__.py
│   │   ├── task.py                  # VALIDATE: Ensure schema matches requirements
│   │   ├── user.py                  # EXISTING: No changes needed
│   │   ├── tool_call.py             # MODIFY: Add MCP-specific fields (protocol version)
│   │   └── conversation.py          # EXISTING: No changes needed
│   ├── services/                    # EXISTING: Business logic
│   │   ├── __init__.py
│   │   ├── task_service.py          # EXISTING: No changes needed
│   │   └── authentication_service.py # EXISTING: Used by MCP auth middleware
│   ├── api/                         # EXISTING: FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── chat_endpoint.py         # MINIMAL CHANGES: Agent now uses MCP client
│   │   └── middleware.py            # EXISTING: No changes needed
│   ├── auth/                        # EXISTING: Authentication
│   │   └── auth.py                  # EXISTING: JWT validation reused by MCP
│   ├── config/                      # EXISTING: Configuration
│   │   └── settings.py              # ADD: MCP server settings
│   ├── database.py                  # EXISTING: SQLModel engine and sessions
│   └── main.py                      # MODIFY: Initialize MCP server on startup
├── tests/
│   ├── mcp/                         # NEW: MCP-specific tests
│   │   ├── test_tool_adapter.py
│   │   ├── test_auth_middleware.py
│   │   └── test_mcp_integration.py
│   ├── tools/                       # EXISTING: Tool tests (validate still pass)
│   └── integration/                 # EXISTING: End-to-end tests
└── requirements.txt                 # MODIFY: Add Official MCP SDK dependency
```

**Structure Decision**: Integrate MCP server as a new module (`backend/src/mcp/`) within the existing FastAPI application. This maintains a single deployment unit, minimizes migration complexity, and allows gradual transition from direct tool invocation to MCP client-based invocation. The existing tool implementations remain largely unchanged; MCP layer wraps them with protocol handling.

## Complexity Tracking

> No violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Architecture Decision Records

### ADR-001: MCP Server Integration Pattern

**Status**: Accepted

**Context**: Need to transform existing custom tool pattern into Official MCP SDK architecture while minimizing disruption to Spec-4 AI agent functionality.

**Decision**: Implement MCP server as a FastAPI-integrated module using **stdio transport** for local communication between AI agent and MCP tools.

**Options Considered**:
1. **Stdio Transport (Local Process)** - ✅ Selected
   - Pros: Single process; low latency; simple auth token passing; no network overhead
   - Cons: Agent and tools in same process (but already deployed together)

2. **HTTP Transport (Remote Service)**
   - Pros: Independent deployment; could scale MCP server separately
   - Cons: Added network latency; complex auth for inter-service calls; deployment complexity
   - Rejected: Over-engineered for current architecture; premature scaling concern

3. **Custom MCP-Like Protocol (No SDK)**
   - Pros: Full control over protocol
   - Cons: Spec requires Official MCP SDK; loses standard tooling and compatibility
   - Rejected: Violates specification requirement for Official MCP SDK

**Consequences**:
- AI agent and MCP tools run in same FastAPI process
- Tool invocations use stdio pipes (in-memory communication)
- JWT token passed as part of MCP request context
- Database sessions created per MCP request (stateless)
- Existing `/api/{user_id}/chat` endpoint unchanged; internal implementation switches to MCP client

**Rationale**: Stdio transport maintains deployment simplicity while achieving all technical requirements (statelessness, JWT auth, protocol compliance). Migration path is clearer with minimal infrastructure changes.

---

### ADR-002: Database Session Lifecycle in MCP Tools

**Status**: Accepted

**Context**: MCP tools must be fully stateless; database sessions cannot be maintained between requests.

**Decision**: Create database session at the start of each MCP tool invocation; close session after tool completes (within the same request context).

**Options Considered**:
1. **Per-Request Session (Database Context Manager)** - ✅ Selected
   - Pros: True statelessness; connection pooling handles efficiency; no leaked connections
   - Cons: Slightly higher overhead per request (minimal with pooling)

2. **Long-Lived Session Pool**
   - Pros: Potential performance optimization
   - Cons: Violates stateless principle; complex lifecycle management; risk of state leakage
   - Rejected: Conflicts with constitution's stateless backend requirement

3. **Session Passed from Caller (Agent)**
   - Pros: Caller controls session lifecycle
   - Cons: MCP protocol doesn't support passing session objects; breaks MCP abstraction
   - Rejected: Not compatible with MCP SDK patterns

**Consequences**:
- Each MCP tool receives JWT token in request context
- Tool validates token, creates database session, performs operation, commits/rolls back, closes session
- No session state persists between tool invocations
- Database connection pooling ensures efficiency despite per-request sessions

**Rationale**: Per-request sessions align with stateless architecture, ensure no leaked connections, and leverage existing database connection pooling for performance.

---

### ADR-003: Tool Contract Formalization

**Status**: Accepted

**Context**: Need to define strict input/output schemas for five MCP tools to ensure deterministic, auditable behavior.

**Decision**: Define tool contracts in `contracts/mcp-tools.yaml` using JSON Schema; enforce validation with Pydantic models at MCP layer.

**Options Considered**:
1. **YAML with JSON Schema** - ✅ Selected
   - Pros: Human-readable; JSON Schema is MCP standard; Pydantic can validate
   - Cons: Requires separate contract file

2. **Python Type Hints Only**
   - Pros: Code and schema in same place
   - Cons: Less portable; harder to share with non-Python clients; no formal contract doc
   - Rejected: Need formal contract documentation for Spec-4 integration

3. **OpenAPI/Swagger Specification**
   - Pros: Well-known standard; good tooling
   - Cons: Doesn't align with MCP protocol conventions; HTTP-centric
   - Rejected: MCP uses JSON Schema, not OpenAPI

**Consequences**:
- Tool contracts maintained in `contracts/mcp-tools.yaml`
- Pydantic models generated from contracts or hand-written to match
- Contract serves as API documentation for Spec-4 AI agent developers
- Schema validation happens at MCP layer before tool invocation

**Rationale**: Formal contract documentation ensures Spec-4 and Spec-5 integration is clear, testable, and maintainable. JSON Schema aligns with MCP standards.

---

## Phase Breakdown

### Phase 0: Research & Technology Selection (research.md output)

**Objective**: Investigate Official MCP SDK patterns, transport options, and authentication strategies.

**Key Questions**:
- How does Official MCP SDK for Python structure tool registration?
- What authentication patterns are supported by MCP protocol?
- How to pass JWT tokens through stdio transport?
- What are performance implications of per-request database sessions?
- How to maintain backward compatibility with existing Spec-4 agent?

**Deliverables**:
- research.md with MCP SDK integration patterns
- Transport layer comparison (stdio vs HTTP)
- Authentication context passing mechanisms
- Database session lifecycle recommendations

---

### Phase 1: Design & Contracts (data-model.md, quickstart.md, contracts/ output)

**Objective**: Design MCP server architecture, define tool contracts, document database schema.

**Key Activities**:
- Validate existing Task model matches specification requirements
- Define ToolCall audit model enhancements for MCP metadata
- Create `contracts/mcp-tools.yaml` with five tool schemas
- Document MCP server setup and configuration
- Plan database migration (if Task schema changes needed)

**Deliverables**:
- data-model.md with database schema and migration plan
- quickstart.md with MCP server setup instructions
- contracts/mcp-tools.yaml with tool input/output schemas

---

### Phase 2: Task Breakdown (/sp.tasks command - separate workflow)

**Objective**: Break down implementation into granular, testable tasks.

**Note**: This phase is handled by `/sp.tasks` command after planning is complete.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **MCP SDK API Changes** | Medium | High | Pin SDK version in requirements.txt; monitor SDK releases; abstract MCP-specific code behind adapter layer |
| **Performance Degradation** | Low | Medium | Per-request sessions may add 10-50ms overhead; connection pooling mitigates this; benchmark early and optimize if needed |
| **Spec-4 Integration Breakage** | Low | High | Implement MCP client in agent gradually; keep existing tool invocation as fallback during migration; comprehensive integration tests |
| **JWT Token Passing Complexity** | Low | Medium | Stdio transport supports custom context; document JWT format clearly; validate with integration tests |
| **Cold-Start Test Failure** | Low | High | Design with statelessness from the start; no caching or in-memory state; validate with automated cold-start tests |

## Implementation Approach

### Incremental Migration Strategy

1. **Phase A: Add MCP Server Module** (without changing existing tools)
   - Install Official MCP SDK
   - Create `backend/src/mcp/` module with server initialization
   - Implement stdio transport layer
   - Register empty MCP server in FastAPI startup

2. **Phase B: Wrap Existing Tools with MCP Adapters**
   - Create `tool_adapter.py` to bridge existing tools to MCP SDK interface
   - Add MCP tool registration for each of the five tools
   - Keep existing tool classes unchanged
   - Test MCP tools in isolation (bypass AI agent)

3. **Phase C: Integrate MCP Client in AI Agent**
   - Modify `todo_agent.py` to use MCP client instead of direct tool calls
   - Pass JWT token through MCP request context
   - Maintain fallback to direct calls during transition
   - Validate with integration tests

4. **Phase D: Remove Fallback and Finalize**
   - Remove direct tool invocation code path
   - Enforce MCP-only tool access
   - Complete audit logging with ToolCall model updates
   - Run cold-start validation tests

### Testing Strategy

1. **Unit Tests** (tools/)
   - Each tool tested with valid/invalid inputs
   - JWT validation tested with mock tokens
   - Database operations tested with test database

2. **Integration Tests** (mcp/)
   - MCP server startup and tool registration
   - End-to-end MCP protocol flow (request → tool → response)
   - JWT authentication through MCP context

3. **Contract Tests** (tests/contract/)
   - Tool input/output schemas validated against `mcp-tools.yaml`
   - Error response formats verified

4. **Cold-Start Tests**
   - Create tasks via MCP tools
   - Restart backend server (simulate cold start)
   - Verify tasks persist and are retrievable

5. **Performance Tests**
   - Tool response time under load (100 concurrent requests)
   - Validate < 1 second response time
   - Database connection pool efficiency

### Definition of Done

- ✅ All five MCP tools (add, list, update, complete, delete) registered and callable
- ✅ Official MCP SDK integrated with stdio transport
- ✅ JWT authentication enforced on every tool invocation
- ✅ User data isolation verified (cross-user access returns 403)
- ✅ Database sessions created/closed per request (no state leakage)
- ✅ Tool contracts documented in `contracts/mcp-tools.yaml`
- ✅ Cold-start test passes (server restart with zero data loss)
- ✅ Performance test passes (< 1 second response time)
- ✅ Integration with Spec-4 AI agent validated
- ✅ All tests pass (unit, integration, contract, cold-start, performance)
- ✅ Quickstart guide allows new developers to run MCP server locally

---

## Success Validation

This implementation will be considered successful when:

1. **Functional Completeness**: All five MCP tools callable independently and returning correct results
2. **Statelessness**: Cold-start test passes; server restart causes zero data loss
3. **Security**: JWT validation blocks unauthorized requests; user isolation prevents cross-user access
4. **Performance**: Tool operations complete within 1 second; 100 concurrent requests handled
5. **Integration**: Spec-4 AI agent successfully uses MCP client to invoke tools
6. **Auditability**: All tool invocations logged in ToolCall model with MCP metadata
7. **Contract Compliance**: Tool input/output matches `mcp-tools.yaml` specifications
8. **Documentation**: Quickstart guide enables setup in < 30 minutes

---

**Planning Complete**: Ready to proceed to research phase and detailed design.
