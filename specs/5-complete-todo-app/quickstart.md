# Quickstart Guide: Complete Todo Application

**Feature**: Complete Todo Application with full CRUD functionality
**Version**: 1.0
**Created**: 2026-02-01

## Overview

This quickstart guide provides step-by-step instructions to set up and run the complete todo application with full CRUD functionality, authentication, and responsive UI.

## Prerequisites

- Node.js 18+ installed
- Python 3.9+ installed
- PostgreSQL database (Neon Serverless recommended)
- Git installed
- npm or yarn package manager

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Set Up Backend (Python/FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Backend Environment

Create `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
JWT_SECRET=another-super-secret-key-for-jwt-tokens
CORS_ORIGINS=http://localhost:3000
```

### 4. Set Up Frontend (Next.js)

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
```

### 5. Configure Frontend Environment

Create `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

### 6. Database Setup

Run the database migrations to create the required tables:

```bash
# From backend directory
cd backend

# Make sure your virtual environment is activated
# Run database migrations manually or via your migration tool
# For this setup, you may need to run the SQL files in backend/migrations/ manually
psql -d postgresql://username:password@localhost:5432/todo_app -f migrations/001_create_users_table.sql
psql -d postgresql://username:password@localhost:5432/todo_app -f migrations/002_create_tasks_table.sql
```

### 7. Start the Applications

#### Start Backend Server:

```bash
# From backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Start Frontend Server:

```bash
# From frontend directory
cd frontend

# Start the Next.js development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## API Endpoints

### Authentication Endpoints
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - User logout

### Task Endpoints
- `GET /api/v1/tasks` - Get user's tasks
- `POST /api/v1/tasks` - Create new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

## Usage Instructions

### 1. Register a New User
1. Navigate to `http://localhost:3000/signup`
2. Enter a valid email and password (8+ characters)
3. Click "Sign Up"
4. You'll be automatically logged in and redirected to the dashboard

### 2. Log In
1. Navigate to `http://localhost:3000/login`
2. Enter your registered email and password
3. Click "Sign In"
4. You'll be redirected to your dashboard

### 3. Manage Tasks
1. Once logged in, go to the tasks page
2. Click "Add Task" to create a new task
3. Fill in the task details and save
4. Use checkboxes to mark tasks as complete/incomplete
5. Click the delete icon to remove tasks

### 4. Log Out
1. Click the "Sign Out" button in the navigation
2. You'll be logged out and redirected to the login page

## Testing

### Backend Tests
```bash
# From backend directory
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
# From frontend directory
cd frontend
npm test
```

## Troubleshooting

### Common Issues

**Issue**: Database connection errors
**Solution**: Verify DATABASE_URL in backend `.env` file is correct

**Issue**: Authentication not working
**Solution**: Ensure BETTER_AUTH_SECRET is the same in both backend and frontend `.env` files

**Issue**: Frontend can't connect to backend API
**Solution**: Verify NEXT_PUBLIC_API_URL in frontend `.env.local` points to your backend server

**Issue**: Migrations not applied
**Solution**: Manually run the SQL files in the migrations directory against your database

### Environment Variables

Make sure all required environment variables are set correctly in both:
- `backend/.env`
- `frontend/.env.local`

## Production Deployment

### Backend Deployment
1. Use a WSGI server like Gunicorn instead of uvicorn for production
2. Set `DEBUG=False` in environment
3. Use a production-ready database
4. Configure proper logging

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve the built application with a web server like nginx
3. Set production environment variables
4. Configure proper caching headers

## Next Steps

1. Explore the complete API documentation at `/docs` on your backend server
2. Customize the UI themes in the frontend
3. Add additional features like task categories or due dates
4. Set up monitoring and logging for production use