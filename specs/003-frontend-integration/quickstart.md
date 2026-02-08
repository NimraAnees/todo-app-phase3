# Quickstart: Frontend Application & Integration

## Overview
Quickstart guide for setting up and running the frontend application that integrates with the backend API for task management.

## Prerequisites
- Node.js 18+ with npm/yarn/pnpm
- Backend API running and accessible
- JWT token from authentication service
- Environment variables configured

## Setup Instructions

### 1. Clone and Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.local.example .env.local
```

Update the `.env.local` file with your backend API configuration:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

### 3. Run Development Server
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Key Integration Points

### Authentication Flow
1. User visits `/signup` or `/login` page
2. Credentials sent to backend via Better Auth
3. JWT token received and stored securely
4. Token automatically attached to subsequent API requests

### Task Management Flow
1. Tasks fetched from `/api/v1/tasks` endpoint
2. JWT token automatically included in Authorization header
3. Only user's tasks are returned by backend
4. Create/update/delete operations follow same pattern

### Error Handling
- Network errors caught and displayed to user
- Authentication errors redirect to login
- Validation errors shown inline in forms

## API Integration Details

### Headers
All API requests include:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

### Endpoints Used
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/tasks` - Fetch user's tasks
- `POST /api/v1/tasks` - Create new task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

## Testing the Integration

### Manual Testing
1. Navigate to signup page and create an account
2. Verify you can create tasks
3. Verify you can update and delete tasks
4. Verify other users' tasks are not accessible
5. Test error handling scenarios

### Development Commands
```bash
npm run dev        # Start development server
npm run build      # Build for production
npm run start      # Start production server
npm run lint       # Check code quality
npm run test       # Run tests (if configured)
```

## Troubleshooting

### Common Issues
- **401 Unauthorized**: JWT token expired or invalid - re-authenticate
- **403 Forbidden**: Attempting to access another user's data - verify backend filtering
- **Network Error**: Backend API not accessible - check API_BASE_URL
- **CORS Error**: Backend not configured for frontend origin - check backend CORS settings

### Debugging Tips
- Check browser developer tools for network requests
- Verify JWT token is being sent in Authorization header
- Confirm backend API endpoints are accessible
- Review environment variables for correct configuration