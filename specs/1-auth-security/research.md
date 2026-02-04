# Research: Authentication & Security Layer

**Date**: 2026-01-11
**Feature**: Authentication & Security Layer (JWT-based)
**Purpose**: Resolve technical unknowns and document architecture decisions

---

## Research Questions & Findings

### 1. Better Auth Integration with Next.js 16+ App Router

**Question**: How does Better Auth integrate with Next.js 16+ using the App Router paradigm?

**Decision**: Use Better Auth's Next.js adapter with App Router support

**Rationale**:
- Better Auth v1.x provides native Next.js 13+ support with App Router compatibility
- Integrates with React Server Components and Client Components
- Handles JWT token generation automatically
- Provides hooks for authentication state management (`useSession`, `useUser`)
- Supports httpOnly cookies out of the box

**Implementation Pattern**:
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next"

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL
  },
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8
  },
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET,
    expiresIn: "1h" // 3600 seconds
  },
  cookies: {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "strict"
  }
})

export const { GET, POST } = auth.handler()
```

**Alternatives Considered**:
- NextAuth.js (formerly Auth.js): More mature but heavier, includes OAuth complexity not needed
- Custom JWT implementation: More control but higher security risk, more maintenance
- **Why Better Auth chosen**: Simpler API, focused on email/password, built-in JWT support, modern architecture

---

### 2. FastAPI JWT Verification with Shared Secret

**Question**: What's the best practice for verifying JWT tokens issued by Better Auth in FastAPI?

**Decision**: Use `python-jose` library with HS256 algorithm and shared `BETTER_AUTH_SECRET`

**Rationale**:
- `python-jose` is the standard JWT library for Python (used in FastAPI docs)
- Better Auth uses HS256 (HMAC-SHA256) for symmetric signing
- Shared secret approach is simple and suitable for single-tenant applications
- No need for public/private key pair (RS256) in this architecture

**Implementation Pattern**:
```python
# core/security.py
from jose import JWTError, jwt
from fastapi import HTTPException, status
from core.config import settings

def verify_token(token: str) -> dict:
    """Verify JWT token and return decoded claims."""
    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")  # subject = user_id
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

**Alternatives Considered**:
- PyJWT: Similar functionality, but python-jose is more feature-rich
- Custom JWT parsing: Security risk, not recommended
- **Why python-jose chosen**: Industry standard, FastAPI documentation uses it, well-tested

---

### 3. Password Hashing Strategy

**Question**: Should we use bcrypt or argon2 for password hashing?

**Decision**: Use **bcrypt** with work factor 12

**Rationale**:
- Bcrypt is battle-tested (20+ years) and widely trusted
- Work factor 12 provides strong security in 2026 (2^12 = 4096 iterations)
- `passlib` library provides easy bcrypt integration with FastAPI
- Better Auth supports bcrypt natively
- Argon2 is newer but bcrypt is sufficient for this use case

**Implementation Pattern**:
```python
# core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

**Alternatives Considered**:
- Argon2: Winner of Password Hashing Competition (2015), but bcrypt is proven
- PBKDF2: Older standard, slower without hardware acceleration
- **Why bcrypt chosen**: Industry standard, battle-tested, Better Auth native support, sufficient security

---

### 4. JWT Token Claims Structure

**Question**: What claims should be included in the JWT token?

**Decision**: Minimal claims following JWT best practices

**Claims Structure**:
```json
{
  "sub": "user_id_uuid",           // Subject: unique user identifier
  "email": "user@example.com",     // User email (for display, not auth)
  "iat": 1704931200,               // Issued at: Unix timestamp
  "exp": 1704934800,               // Expiration: iat + 3600 seconds
  "iss": "todo-app"                // Issuer: application identifier (optional)
}
```

**Rationale**:
- `sub` (subject): Standard claim for user identity, used for DB query filtering
- `email`: Convenience for displaying user info without DB lookup
- `iat` (issued at): Required for token freshness validation
- `exp` (expiration): Required for automatic expiration enforcement
- `iss` (issuer): Optional but useful for multi-app environments

**Why minimal**: Reduces token size, faster transmission, less data leakage if token intercepted

**Alternatives Considered**:
- Including user roles/permissions: Not needed (no RBAC in Phase 2)
- Including more user data: Security risk, increases token size
- **Why minimal chosen**: Follows JWT best practices, sufficient for authentication

---

### 5. Frontend-Backend Communication Pattern

**Question**: How should the frontend pass JWT tokens to the backend?

**Decision**: Use `Authorization: Bearer <token>` header (industry standard)

**Rationale**:
- RESTful API convention for stateless authentication
- Supported by all HTTP clients (fetch, axios, httpx)
- FastAPI's `OAuth2PasswordBearer` dependency extracts token automatically
- Allows CORS configuration without cookie complications

**Implementation Pattern (Frontend)**:
```typescript
// lib/api-client.ts
export async function apiCall(endpoint: string, options: RequestInit = {}) {
  const token = await getTokenFromCookie() // Extract from httpOnly cookie

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      ...options.headers
    },
    credentials: 'include' // Send cookies
  })

  if (response.status === 401) {
    // Token expired, redirect to sign-in
    window.location.href = '/signin'
  }

  return response
}
```

**Implementation Pattern (Backend)**:
```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from core.security import verify_token

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> dict:
    """Extract and verify JWT token, return user claims."""
    token = credentials.credentials
    return verify_token(token)
```

**Alternatives Considered**:
- Cookie-based authentication on backend: Complicates CORS, harder to test
- Custom header (X-Auth-Token): Non-standard, less tooling support
- **Why Authorization Bearer chosen**: Industry standard, best tooling support, RESTful

---

### 6. Error Handling & User Enumeration Prevention

**Question**: How do we prevent user enumeration attacks while providing useful feedback?

**Decision**: Generic error messages for authentication failures

**Rationale**:
- User enumeration attack: attacker tries emails to discover valid accounts
- Solution: return same error for "email not found" and "wrong password"
- Error message: "Invalid credentials" (generic)
- Status code: `401 Unauthorized` (authentication failed)

**Implementation Patterns**:

**Registration (email already exists)**:
```python
# Return generic error without revealing email exists
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Unable to create account. Please try a different email."
)
```

**Sign-in (wrong email or password)**:
```python
# Same error for both cases
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials"
)
```

**Timing Attack Prevention**:
- Always hash password attempt even if email not found (prevents timing attacks)
- Use constant-time comparison for password verification

**Alternatives Considered**:
- Specific errors: "Email not found", "Wrong password" - Enables user enumeration
- CAPTCHA: Adds friction, not needed for Phase 2
- **Why generic errors chosen**: Best practice for security, simple to implement

---

### 7. Token Expiration Handling on Frontend

**Question**: How should the frontend handle expired JWT tokens?

**Decision**: Detect expiration and redirect to sign-in page

**Rationale**:
- Backend returns `401 Unauthorized` for expired tokens
- Frontend intercepts 401 responses and redirects to `/signin`
- Clear expired cookie to prevent stale token reuse
- Display user-friendly message: "Session expired. Please sign in again."

**Implementation Pattern**:
```typescript
// lib/api-client.ts
export async function apiCall(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(/* ... */)

  if (response.status === 401) {
    // Clear expired token cookie
    document.cookie = 'auth_token=; Max-Age=0; path=/;'

    // Redirect to sign-in with message
    const message = encodeURIComponent('Session expired. Please sign in again.')
    window.location.href = `/signin?message=${message}`

    throw new Error('Authentication required')
  }

  return response
}
```

**Alternatives Considered**:
- Silent token refresh: Requires refresh tokens (out of scope for Phase 2)
- Modal dialog: Less clear UX than redirect
- **Why redirect chosen**: Simple, clear UX, aligns with stateless auth model

---

### 8. Database Schema for Users

**Question**: What's the minimal schema for the `users` table?

**Decision**: Simple schema with essential fields only

**Schema**:
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

**Rationale**:
- UUID for `id`: Universal unique identifier, avoids enumeration attacks
- `email` UNIQUE: Prevents duplicate registrations
- `password_hash`: Stores bcrypt hash (60 characters, but 255 for future algorithms)
- `created_at`/`updated_at`: Audit timestamps
- Index on `email`: Fast lookups during sign-in

**Why minimal**: Follows "simplicity" principle, sufficient for Phase 2, easy to extend

**Alternatives Considered**:
- Integer `id`: Less secure (enumerable), but simpler
- Additional fields (name, phone): Not required for Phase 2
- **Why UUID + minimal chosen**: Security best practice, sufficient for authentication

---

### 9. Environment Variable Management

**Question**: How do we manage `BETTER_AUTH_SECRET` across frontend and backend?

**Decision**: Separate `.env` files for frontend and backend with shared secret

**Frontend (`.env.local`)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<64-character-random-string>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

**Backend (`.env`)**:
```bash
BETTER_AUTH_SECRET=<same-64-character-random-string>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ORIGINS=http://localhost:3000,https://yourapp.com
```

**Secret Generation**:
```bash
# Generate secure random secret (64 characters)
openssl rand -base64 48
```

**Rationale**:
- Same `BETTER_AUTH_SECRET` required for both to sign/verify tokens
- Frontend needs secret to configure Better Auth
- Backend needs secret to verify JWT signatures
- Never commit `.env` files (use `.env.example` templates)

**Alternatives Considered**:
- Environment-specific secrets: More secure but complex for Phase 2
- Single `.env` file: Doesn't work with separate deployments
- **Why separate files chosen**: Standard practice, supports independent deployment

---

### 10. CORS Configuration for Cookie-Based Auth

**Question**: What CORS settings are required for httpOnly cookies between frontend and backend?

**Decision**: Configure CORS with credentials support

**Backend CORS Configuration (FastAPI)**:
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://yourapp.com"     # Production
    ],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Frontend Fetch Configuration**:
```typescript
fetch(url, {
  credentials: 'include',  // Send cookies with request
  // ...
})
```

**Rationale**:
- `allow_credentials=True` required for httpOnly cookies
- Specific origins (not `*`) required when using credentials
- Frontend must send `credentials: 'include'` to attach cookies

**Alternatives Considered**:
- Same-origin deployment: Simpler but limits deployment flexibility
- Token in localStorage: Vulnerable to XSS attacks
- **Why CORS + cookies chosen**: Secure, flexible deployment, standard practice

---

## Technology Decisions Summary

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| **Frontend Auth Library** | Better Auth v1.x | Simple API, JWT support, Next.js App Router compatible |
| **Backend JWT Library** | python-jose | FastAPI standard, HS256 support, well-documented |
| **Password Hashing** | bcrypt (work factor 12) | Battle-tested, Better Auth native, sufficient security |
| **Token Claims** | Minimal (sub, email, iat, exp) | Follows JWT best practices, reduces token size |
| **Token Transport** | Authorization: Bearer header | RESTful standard, best tooling support |
| **Error Messages** | Generic ("Invalid credentials") | Prevents user enumeration attacks |
| **Token Expiration** | Redirect to /signin on 401 | Clear UX, aligns with stateless model |
| **Database Schema** | UUID id, minimal fields | Security best practice, sufficient for Phase 2 |
| **Environment Secrets** | Separate .env files, shared secret | Standard practice, independent deployment |
| **CORS Configuration** | Credentials-enabled, specific origins | Secure cookie transport across origins |

---

## Implementation Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Shared secret leakage** | High - All tokens can be forged | Store in `.env`, add to `.gitignore`, rotate regularly |
| **Weak BETTER_AUTH_SECRET** | High - Brute-force attacks possible | Generate 64+ character random string (384+ bits entropy) |
| **CORS misconfiguration** | Medium - Cookies not sent, auth breaks | Test with actual frontend domain, document CORS setup |
| **Token expiration too long** | Medium - Stolen tokens valid longer | Use 1-hour expiration (spec requirement) |
| **User enumeration via timing** | Low - Email discovery attacks | Hash password even if email not found (constant-time) |
| **XSS token theft** | High (if localStorage used) | Use httpOnly cookies (prevents JavaScript access) |
| **CSRF attacks** | Medium - Forged requests | Use SameSite=Strict cookies (prevents cross-site requests) |

---

## Next Steps

1. ✅ Phase 0 Complete: All technical unknowns resolved
2. → Phase 1: Create `data-model.md` with User entity schema
3. → Phase 1: Generate API contracts in `/contracts/` directory
4. → Phase 1: Write `quickstart.md` for local development setup
5. → Phase 2: Generate `tasks.md` with implementation tasks (via `/sp.tasks`)

---

**Research Completed**: 2026-01-11
**All unknowns resolved**: ✅ Ready for Phase 1 (Design & Contracts)
