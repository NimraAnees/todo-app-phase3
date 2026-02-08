---
id: 001
title: Amend Constitution Phase III
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: claude
command: sp.constitution "Project: Phase III – AI-Powered Todo Chatbot"
labels: [constitution, ai, mcp, phase-3]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

Project: Phase III – AI-Powered Todo Chatbot

Phase III extends the authenticated Todo application (Phase II) by introducing a
natural-language chatbot powered by AI agents and MCP tools. Users manage tasks
conversationally while the backend remains fully stateless and secure.

## Core Principles
- Stateless backend (no in-memory session state)
- Tool-driven AI (all task actions via MCP tools)
- JWT-based authentication and strict user isolation
- Persistent conversation history in the database
- Deterministic, auditable agent behavior

## Architecture Standards
- Frontend: OpenAI ChatKit
- Backend: FastAPI
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth (JWT)

## Constraints
- MCP tools must be stateless
- Agents must not access the database directly
- All chat and tool requests require valid JWT
- Conversation context must be reconstructed per request
- Follow Agentic Dev Stack workflow (spec → plan → tasks → implement)

## Success Criteria
- Users manage todos via natural language
- AI agents correctly invoke MCP tools
- Conversations persist across requests and restarts
- Task ownership is enforced for every operation
- All Phase 3 specs (backend + frontend) are fully implemented and integrated

## Response snapshot

Updated the project constitution to version 3.0.0 to reflect Phase III requirements for the AI-powered Todo Chatbot. Key changes include:

- Added new principles: "Stateless Backend by Default", "Tool-Driven AI Operations", "MCP Server Integration", "AI Agent Determinism", and "Conversation History Persistence"
- Updated existing principles to include AI/MCP considerations
- Modified Technology Standards to include AI Framework and MCP Server
- Expanded Security Constraints to cover AI agents and MCP tools
- Updated Architecture Constraints for stateless AI architecture
- Enhanced Code Standards to include AI/MCP patterns
- Updated Success Criteria to reflect Phase III deliverables

## Outcome

- ✅ Impact: Major version update (2.0.0 → 3.0.0) to reflect significant architectural expansion to AI-powered chatbot
- 🧪 Tests: null
- 📁 Files: Updated .specify/memory/constitution.md with new Phase III principles
- 🔁 Next prompts: Plan implementation of AI-powered chatbot with MCP integration
- 🧠 Reflection: Constitution successfully updated to guide Phase III development

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Begin Phase III implementation following new constitutional guidelines