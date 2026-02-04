# Research: Backend API & Data Layer

## Decision 1: Task Ownership Enforcement
- **Chosen**: Mandatory filtering in every query via `get_current_user` user\_id.
- **Rationale**: Direct filtering is the most robust way to ensure data isolation. It is simple to implement and review.
- **Alternatives considered**: Row Level Security (RLS) in Postgres. Rejected for now to keep the application logic central in Python and avoid complexity in migration management.

## Decision 2: UUID vs Sequential IDs
- **Chosen**: UUID v4 for both Users and Tasks.
- **Rationale**: Prevents ID enumeration attacks and makes it difficult for users to guess other user's task IDs (though auth check is still primary).
- **Alternatives considered**: Sequential Integers. Rejected due to security risks in multi-user environments.

## Decision 3: SQLModel Schemas (SQLModel + Pydantic)
- **Chosen**: Separate Pydantic schemas for TaskCreate, TaskUpdate, and TaskRead.
- **Rationale**: Avoids exposing internal fields (like `user_id` during creation) and ensures strict validation of inputs.
- **Alternatives considered**: Using the SQLModel entity directly for all operations. Rejected because it often leaks database structure to the client.

## Decision 4: Neon Connection Pooling
- **Chosen**: Using `psycopg2` with standard engine pooling in SQLModel.
- **Rationale**: Neon supports standard pooling. Will monitor for latency and shift to Neon-specific proxy if high volume is expected.
