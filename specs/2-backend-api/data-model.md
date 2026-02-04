# Data Model: Tasks

## Entity: Task
- **Table**: `tasks`
- **Description**: Represents a todo item belonging to a specific user.

| Field | Type | Constraint | Description |
|-------|------|------------|-------------|
| id | UUID | Primary Key | Unique task identifier |
| title | String(255) | Not Null | Task title |
| description | Text | Nullable | Optional task details |
| is_completed | Boolean | Default False | Completion status |
| user\_id | UUID | Foreign Key (users.id) | Task owner |
| created\_at | DateTime | Not Null | Creation timestamp |
| updated\_at | DateTime | Not Null | Last update timestamp |

## State Transitions
1. **Pending**: `is_completed = false` (Default)
2. **Completed**: `is_completed = true`

## Relationships
- **Task belongs to User**: `tasks.user_id -> users.id` (Many-to-One)
