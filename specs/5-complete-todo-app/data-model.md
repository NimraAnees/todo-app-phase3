# Data Model: Complete Todo Application

**Feature**: Complete Todo Application with full CRUD functionality
**Version**: 1.0
**Created**: 2026-02-01
**Author**: Claude Code

## Overview

This document defines the data model for the complete todo application, including user management and task management entities with their relationships, constraints, and validation rules. The data model ensures proper data integrity, user isolation, and scalability.

## Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐
│     Users       │    │     Tasks       │
│─────────────────│    │─────────────────│
│ id (UUID) PK    │────│ user_id (UUID)  │
│ email (VARCHAR) │    │ id (UUID) PK    │
│ password_hash   │    │ title (VARCHAR) │
│ (VARCHAR)       │    │ description     │
│ created_at      │    │ (TEXT)          │
│ (TIMESTAMP)     │    │ completed       │
│ updated_at      │    │ (BOOLEAN)       │
│ (TIMESTAMP)     │    │ created_at      │
└─────────────────┘    │ (TIMESTAMP)     │
                       │ updated_at      │
                       │ (TIMESTAMP)     │
                       └─────────────────┘
```

## Entity Definitions

### Users Entity

**Description**: Stores user account information for authentication and authorization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address for login |
| password_hash | VARCHAR(255) | NOT NULL | BCrypt hashed password |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When the user account was created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When the user record was last updated |

**Indexes**:
- `idx_users_email`: Index on email field for fast lookup during authentication

**Constraints**:
- Email uniqueness constraint to prevent duplicate accounts
- Password hash required for all users
- Automatic timestamp updates

### Tasks Entity

**Description**: Stores individual tasks associated with users, supporting CRUD operations.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for the task |
| title | VARCHAR(255) | NOT NULL | Task title/description |
| description | TEXT | | Optional detailed description of the task |
| completed | BOOLEAN | DEFAULT FALSE | Whether the task is marked as completed |
| user_id | UUID | FOREIGN KEY(users.id) ON DELETE CASCADE | Reference to the owning user |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When the task was created |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT CURRENT_TIMESTAMP | When the task was last updated |

**Indexes**:
- `idx_tasks_user_id`: Index on user_id for efficient user-specific queries
- `idx_tasks_completed`: Index on completed field for filtering by status

**Constraints**:
- Foreign key relationship to users table with cascade delete
- Title required for all tasks
- Automatic timestamp updates
- Completed status defaults to false

## Relationships

### Users → Tasks (One-to-Many)
- One user can have many tasks
- Implemented via foreign key `tasks.user_id` → `users.id`
- Cascade delete: when user is deleted, all their tasks are automatically deleted
- This ensures data isolation and cleanup

## Data Integrity Rules

### Referential Integrity
- All tasks must have a valid user_id that references an existing user
- Attempts to create tasks with invalid user_id will fail
- When users are deleted, their tasks are automatically removed

### Business Rules
- Users must have unique email addresses
- Tasks cannot exist without an associated user
- Users can only access tasks they own
- Passwords must be hashed before storage

## Validation Rules

### Users Validation
- Email: Must conform to RFC 5322 standard format
- Email: Maximum length of 255 characters
- Password: Stored as bcrypt hash, minimum 60 characters when hashed
- Timestamps: Automatically managed by database triggers

### Tasks Validation
- Title: Required, 1-255 characters
- Description: Optional, up to 1000 characters
- Completed: Boolean value (true/false)
- User association: Required foreign key reference

## Performance Considerations

### Indexing Strategy
- Primary keys are automatically indexed
- Foreign key fields are indexed for join performance
- Frequently queried fields (user_id, completed) have dedicated indexes
- Email field is indexed for authentication lookups

### Partitioning Strategy
- Not initially required but could be implemented by user_id range if scale demands
- Time-based partitioning could be applied to created_at field for historical data

## Security Considerations

### Data Protection
- Passwords are never stored in plain text
- User emails are encrypted in transit and at rest
- Task titles and descriptions are user-generated content

### Access Control
- Database-level row-level security through user_id foreign keys
- Application-level validation ensures users can only access their own data
- No direct database access for end users

## Migration Strategy

### Initial Schema Creation
1. Create users table with all fields and constraints
2. Create tasks table with all fields and constraints
3. Create indexes for performance optimization
4. Set up automatic timestamp updates

### Future Schema Changes
- Use migration files to track schema evolution
- Maintain backward compatibility where possible
- Plan downtime windows for breaking changes
- Always backup before schema modifications

## Sample Data

### Users Sample
```sql
INSERT INTO users (id, email, password_hash, created_at, updated_at)
VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'john@example.com', '$2b$12$...', '2026-01-01 10:00:00+00', '2026-01-01 10:00:00+00'),
('f0e9d8c7-b6a5-4321-fedc-ba9876543210', 'jane@example.com', '$2b$12$...', '2026-01-01 11:00:00+00', '2026-01-01 11:00:00+00');
```

### Tasks Sample
```sql
INSERT INTO tasks (id, title, description, completed, user_id, created_at, updated_at)
VALUES
('z9y8x7w6-v5u4-3210-pqrs-tuvwxyz12345', 'Buy groceries', 'Milk, bread, eggs', false, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', '2026-01-01 12:00:00+00', '2026-01-01 12:00:00+00'),
('t9s8r7q6-p5o4-3210-nmlk-jihgfedcba98', 'Finish report', 'Complete quarterly report for review', true, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', '2026-01-01 13:00:00+00', '2026-01-01 14:00:00+00');
```

## Query Examples

### Find all tasks for a specific user
```sql
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;
```

### Count completed tasks for a user
```sql
SELECT COUNT(*) FROM tasks
WHERE user_id = $1 AND completed = true;
```

### Update task completion status
```sql
UPDATE tasks
SET completed = $2, updated_at = CURRENT_TIMESTAMP
WHERE id = $1 AND user_id = $3;
```

## Monitoring and Maintenance

### Performance Monitoring
- Monitor query execution times for slow operations
- Track index usage and effectiveness
- Watch for deadlocks or locking issues

### Data Maintenance
- Regular backup schedules
- Archive old data if retention policies require
- Cleanup orphaned records (though foreign keys prevent most cases)