# Quickstart Guide: Authentication & Security Layer

**Date**: 2026-01-11
**Feature**: Authentication & Security Layer (JWT-based)
**Purpose**: Set up and test authentication locally

---

## Prerequisites

- Node.js 20+ and npm (for Next.js frontend)
- Python 3.11+ and pip (for FastAPI backend)
- PostgreSQL database (Neon or local)
- Git (for version control)

---

## Quick Start (5 Minutes)

###1. Clone and Navigate

```bash
git clone <repository-url>
cd todo-app
git checkout 1-auth-security
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart

# Create .env file
cat > .env <<EOF
DATABASE_URL=postgresql://user:password@localhost:5432/todoapp
BETTER_AUTH_SECRET=$(openssl rand -base64 48)
CORS_ORIGINS=http://localhost:3000
EOF

# Run database migrations (if using Alembic)
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**Backend will be running at**: http://localhost:8000

### 3. Set Up Frontend (in a new terminal)

```bash
cd frontend

# Install dependencies
npm install next@latest react@latest react-dom@latest better-auth

# Create .env.local file (use the SAME secret from backend/.env)
cat > .env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<paste-secret-from-backend-env>
DATABASE_URL=<same-as-backend>
EOF

# Start frontend development server
npm run dev
```

**Frontend will be running at**: http://localhost:3000

---

## Environment Variables

### Backend (`.env`)

```bash
# Database connection string (Neon PostgreSQL or local)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# JWT signing secret (MUST be same as frontend)
# Generate with: openssl rand -base64 48
BETTER_AUTH_SECRET=<64-character-random-string>

# Allowed CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://yourapp.com
```

### Frontend (`.env.local`)

```bash
# Backend API base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# JWT signing secret (MUST be same as backend)
BETTER_AUTH_SECRET=<same-64-character-string-as-backend>

# Database URL (for Better Auth)
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

**⚠️ CRITICAL**: `BETTER_AUTH_SECRET` must be identical in both files. Tokens signed by frontend with one secret cannot be verified by backend with a different secret.

---

## Database Setup

### Option 1: Neon Serverless PostgreSQL (Recommended)

1. Create account at https://neon.tech
2. Create new project "todo-app"
3. Copy connection string from dashboard
4. Use connection string in both `.env` files

### Option 2: Local PostgreSQL

```bash
# Install PostgreSQL (macOS with Homebrew)
brew install postgresql
brew services start postgresql

# Create database
createdb todoapp

# Connection string
DATABASE_URL=postgresql://localhost:5432/todoapp
```

### Run Migrations

```bash
cd backend

# Option A: Using Alembic (recommended)
alembic revision --autogenerate -m "Create users table"
alembic upgrade head

# Option B: Using SQLModel directly (quick start)
python -c "from app.database import create_db_and_tables; create_db_and_tables()"
```

---

## Testing Authentication Flow

### 1. Test Registration

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'

# Expected response (201 Created)
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "created_at": "2026-01-11T12:00:00Z"
  }
}
```

### 2. Test Sign-In

```bash
curl -X POST http://localhost:8000/api/v1/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'

# Expected response (200 OK) - same structure as registration
```

### 3. Test Protected Endpoint

```bash
# Extract token from registration/signin response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Expected response (200 OK)
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com",
  "created_at": "2026-01-11T12:00:00Z"
}
```

### 4. Test Invalid Token

```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer invalid_token"

# Expected response (401 Unauthorized)
{
  "detail": "Could not validate credentials"
}
```

### 5. Test No Token

```bash
curl -X GET http://localhost:8000/api/v1/auth/me

# Expected response (401 Unauthorized)
{
  "detail": "Not authenticated"
}
```

---

## Manual Testing via Frontend

### 1. Test Registration Flow

1. Navigate to http://localhost:3000/signup
2. Enter email: `test@example.com`
3. Enter password: `testpassword123` (minimum 8 characters)
4. Click "Sign Up"
5. **Expected**: Redirected to dashboard with user info displayed

### 2. Test Sign-In Flow

1. Navigate to http://localhost:3000/signin
2. Enter registered email and password
3. Click "Sign In"
4. **Expected**: Redirected to dashboard

### 3. Test Protected Route

1. Sign in (step 2)
2. Navigate to http://localhost:3000/dashboard
3. **Expected**: Dashboard loads with user info
4. Sign out
5. Try accessing http://localhost:3000/dashboard again
6. **Expected**: Redirected to sign-in page

### 4. Test Token Expiration

1. Sign in
2. Wait 1 hour (or modify JWT expiration to 1 minute for testing)
3. Try accessing protected route
4. **Expected**: Redirected to sign-in with message "Session expired"

---

## API Documentation

Once backend is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Common Issues & Troubleshooting

### Issue: "Invalid authentication credentials"

**Cause**: `BETTER_AUTH_SECRET` mismatch between frontend and backend

**Solution**:
1. Verify secrets are identical in both `.env` files
2. Restart both frontend and backend servers
3. Clear browser cookies and try again

### Issue: "Connection refused" or "CORS error"

**Cause**: Backend not running or CORS misconfiguration

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/docs`
2. Check `CORS_ORIGINS` includes `http://localhost:3000`
3. Restart backend after `.env` changes

### Issue: "Database connection error"

**Cause**: Invalid `DATABASE_URL` or database not running

**Solution**:
1. Test connection: `psql $DATABASE_URL`
2. Verify Neon project is active (check dashboard)
3. Check database credentials are correct

### Issue: "Email already registered" on first registration

**Cause**: User already exists in database from previous test

**Solution**:
```bash
# Delete test user from database
psql $DATABASE_URL -c "DELETE FROM users WHERE email = 'test@example.com';"
```

### Issue: Token works in Postman but not in browser

**Cause**: httpOnly cookies not being sent

**Solution**:
1. Verify `credentials: 'include'` in fetch calls
2. Check browser DevTools → Application → Cookies
3. Ensure `Secure` flag is false for http://localhost (dev only)

---

## Development Workflow

### 1. Start Development Environment

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Database (if local PostgreSQL)
brew services start postgresql
```

### 2. Make Changes

- Backend: Edit files in `backend/app/`, auto-reload enabled
- Frontend: Edit files in `frontend/app/`, hot module replacement enabled

### 3. Test Changes

- Backend: Run `pytest` in backend directory
- Frontend: Run `npm test` in frontend directory
- Integration: Manual testing via browser or curl

### 4. Commit Changes

```bash
git add .
git commit -m "feat(auth): implement JWT token verification"
git push origin 1-auth-security
```

---

## Testing Checklist

- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Database connection successful
- [ ] User registration works (returns 201 with token)
- [ ] Sign-in works (returns 200 with token)
- [ ] Protected endpoint requires token (returns 401 without token)
- [ ] Protected endpoint works with valid token (returns 200)
- [ ] Invalid token returns 401
- [ ] Expired token returns 401 (test after 1 hour or modify expiration)
- [ ] Sign-out clears token (subsequent requests return 401)
- [ ] Frontend registration form works
- [ ] Frontend sign-in form works
- [ ] Frontend redirects to dashboard after auth
- [ ] Frontend redirects to sign-in when accessing protected route without auth
- [ ] Error messages are generic (no user enumeration)

---

## Next Steps

After authentication is working:

1. Run `/sp.tasks` to generate implementation tasks
2. Implement auth middleware for FastAPI
3. Implement Better Auth configuration in Next.js
4. Create sign-up and sign-in UI components
5. Add protected route middleware in Next.js
6. Write integration tests
7. Deploy to staging environment

---

## Useful Commands

```bash
# Generate secure secret
openssl rand -base64 48

# Test JWT token decoding (Python)
python -c "from jose import jwt; print(jwt.decode('TOKEN', 'SECRET', algorithms=['HS256']))"

# Check database for users
psql $DATABASE_URL -c "SELECT id, email, created_at FROM users;"

# Delete all test users
psql $DATABASE_URL -c "DELETE FROM users WHERE email LIKE '%test%';"

# View backend logs
tail -f backend/logs/app.log

# View frontend build logs
cd frontend && npm run build

# Run tests
cd backend && pytest
cd frontend && npm test
```

---

## Resources

- **Better Auth Docs**: https://better-auth.com/docs
- **FastAPI JWT Tutorial**: https://fastapi.tiangolo.com/tutorial/security/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Neon PostgreSQL**: https://neon.tech/docs
- **JWT.io Debugger**: https://jwt.io/

---

**Quickstart Guide Completed**: 2026-01-11
**Next**: Run `/sp.tasks` to generate implementation tasks
