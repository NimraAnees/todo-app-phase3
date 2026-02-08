# Data Model: Frontend Application & Integration

## Overview
Data model representation for the frontend application, focusing on client-side state and API data structures that align with the backend API contracts.

## Frontend State Models

### Task State Model
Represents the client-side state for tasks in the frontend application.

- **id**: string - Unique identifier for the task (matches backend UUID)
- **title**: string - Task title (required, 1-255 characters)
- **description**: string | null - Optional task description
- **isCompleted**: boolean - Completion status (default: false)
- **userId**: string - Owner's user ID (from JWT token)
- **createdAt**: string - ISO timestamp when task was created
- **updatedAt**: string - ISO timestamp when task was last updated
- **isLoading**: boolean - Loading state for individual task operations

### User Session Model
Represents the authenticated user session state in the frontend.

- **userId**: string - User's unique identifier from JWT token
- **email**: string - User's email address
- **isLoggedIn**: boolean - Authentication status
- **jwtToken**: string - JWT token for API authentication
- **tokenExpiry**: number - Unix timestamp of token expiration

### API Response Models
Standard response structures for API interactions.

#### Task Response
- **success**: boolean - Whether the operation succeeded
- **data**: Task | Task[] | null - The task data or array of tasks
- **error**: string | null - Error message if operation failed
- **statusCode**: number - HTTP status code

#### Loading State Model
- **isLoading**: boolean - Global loading state
- **operation**: string - Current operation being performed
- **progress**: number | null - Progress percentage if applicable

## State Relationships
- Each Task belongs to one User Session (via userId)
- User Session manages multiple Tasks
- Loading states are tied to specific operations
- Error states are operation-specific

## Validation Rules
- Task titles must be 1-255 characters
- Task descriptions must be less than 1000 characters if provided
- User session must exist for task operations
- JWT token must be valid before API calls
- Loading states must be cleared after operations complete

## Client-Side State Transitions
1. **Initial State**: User not logged in, no tasks loaded
2. **Login State**: User authenticated, JWT token acquired
3. **Loading State**: Fetching tasks from API
4. **Loaded State**: Tasks displayed in UI
5. **Operation State**: Performing create/update/delete operations
6. **Error State**: Operation failed, error message displayed
7. **Logout State**: Session cleared, return to initial state

## API Integration Points
- GET /api/v1/tasks - Fetch user's tasks
- POST /api/v1/tasks - Create new task
- PATCH /api/v1/tasks/{id} - Update task
- DELETE /api/v1/tasks/{id} - Delete task
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/logout - User logout