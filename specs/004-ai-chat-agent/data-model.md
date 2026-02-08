# Data Model: AI Chat Agent & Conversation System

**Feature**: AI Chat Agent & Conversation System
**Date**: 2026-02-06
**Status**: Completed

## Entity Definitions

### User
**Description**: Represents an authenticated user in the system
**Fields**:
- id (UUID): Unique identifier for the user
- email (String): User's email address (unique)
- created_at (DateTime): Timestamp when user account was created
- updated_at (DateTime): Timestamp when user account was last updated
- is_active (Boolean): Whether the user account is active

**Validation**: Email must be valid email format, unique across all users

### Task
**Description**: A todo item that can be managed through the AI agent's natural language interface
**Fields**:
- id (UUID): Unique identifier for the task
- user_id (UUID): Reference to the user who owns this task
- title (String): Title/description of the task
- description (String): Detailed description of the task (optional)
- status (String): Current status of the task (pending, in_progress, completed)
- created_at (DateTime): Timestamp when task was created
- updated_at (DateTime): Timestamp when task was last updated
- completed_at (DateTime): Timestamp when task was marked as completed (nullable)

**Validation**: Title is required, status must be one of the allowed values, user_id must reference valid user

### Conversation
**Description**: Represents a user's ongoing dialogue with the AI agent
**Fields**:
- id (UUID): Unique identifier for the conversation
- user_id (UUID): Reference to the user who owns this conversation
- title (String): Auto-generated title for the conversation
- started_at (DateTime): Timestamp when conversation was started
- last_message_at (DateTime): Timestamp of the most recent message
- status (String): Current status of the conversation (active, archived)

**Validation**: user_id must reference valid user, status must be one of allowed values

### Message
**Description**: An individual exchange in the conversation
**Fields**:
- id (UUID): Unique identifier for the message
- conversation_id (UUID): Reference to the conversation this message belongs to
- user_id (UUID): Reference to the user who sent this message
- role (String): Role of the message sender (user, assistant)
- content (Text): Content of the message
- timestamp (DateTime): When the message was sent
- metadata (JSON): Additional information about the message (tool calls, context, etc.)

**Validation**: conversation_id must reference valid conversation, role must be either 'user' or 'assistant'

### ToolCall
**Description**: Records tool invocations made by the AI agent during conversations
**Fields**:
- id (UUID): Unique identifier for the tool call
- conversation_id (UUID): Reference to the conversation where tool was called
- message_id (UUID): Reference to the message that triggered this tool call
- user_id (UUID): Reference to the user who initiated the action
- tool_name (String): Name of the MCP tool that was called
- parameters (JSON): Parameters passed to the tool
- result (JSON): Result returned by the tool
- timestamp (DateTime): When the tool was called

**Validation**: conversation_id and message_id must reference valid records, tool_name must be one of allowed MCP tools

## Relationships

### User → Task
- One-to-Many relationship
- A user can have multiple tasks
- Tasks are isolated per user for security

### User → Conversation
- One-to-Many relationship
- A user can have multiple conversations
- Conversations are isolated per user for security

### Conversation → Message
- One-to-Many relationship
- A conversation can have multiple messages
- Messages belong to exactly one conversation

### Conversation → ToolCall
- One-to-Many relationship
- A conversation can have multiple tool calls
- Tool calls belong to exactly one conversation

### Message → ToolCall
- One-to-Many relationship (optional)
- A message can trigger zero or more tool calls
- Tool calls reference the message that initiated them

## Validation Rules

1. **User Isolation**: All queries must filter by user_id to prevent cross-user data access
2. **Task Ownership**: Tasks can only be modified by their owning user
3. **Conversation Access**: Users can only access their own conversations
4. **Message Integrity**: Messages cannot be modified after creation (append-only)
5. **Status Constraints**: Enumerated status fields must have valid values
6. **Required Fields**: Critical fields like title for tasks and user_id for all entities must be present

## Indexes for Performance

1. **Task indexes**:
   - Index on user_id for user isolation queries
   - Index on status for filtering tasks by status
   - Composite index on (user_id, status) for common user-task-status queries

2. **Conversation indexes**:
   - Index on user_id for user isolation queries
   - Index on last_message_at for chronological ordering

3. **Message indexes**:
   - Index on conversation_id for conversation message retrieval
   - Index on timestamp for chronological ordering
   - Composite index on (conversation_id, timestamp) for conversation history

4. **ToolCall indexes**:
   - Index on user_id for user isolation
   - Index on conversation_id for conversation-specific tool calls
   - Index on tool_name for tool usage analytics