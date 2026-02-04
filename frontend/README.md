# Todo App - Frontend

Next.js 15+ application with Better Auth authentication.

## Setup

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Configure environment
```bash
cp .env.local.example .env.local
# Edit .env.local with your API URL and BETTER_AUTH_SECRET
```

### 3. Start development server
```bash
npm run dev
```

Open http://localhost:3000

## Project Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signup/
│   │   │   └── page.tsx    # Registration page
│   │   └── signin/
│   │       └── page.tsx    # Sign-in page
│   ├── dashboard/
│   │   └── page.tsx        # Protected dashboard
│   ├── layout.tsx          # Root layout
│   └── page.tsx            # Landing page
├── components/
│   ├── auth/
│   │   ├── SignupForm.tsx  # Registration form
│   │   ├── SigninForm.tsx  # Sign-in form
│   │   └── SignoutButton.tsx  # Sign-out button
│   └── ui/
│       ├── Button.tsx      # Reusable button
│       └── Input.tsx       # Reusable input
└── lib/
    ├── auth.ts             # Better Auth configuration
    └── api-client.ts       # API client with JWT
```

## Environment Variables

- `NEXT_PUBLIC_API_URL`: Backend API base URL
- `BETTER_AUTH_SECRET`: JWT secret (must match backend)
- `DATABASE_URL`: PostgreSQL connection (for Better Auth)

## Authentication Flow

1. User registers → Backend creates account → JWT issued
2. User signs in → Backend validates → JWT issued
3. Frontend stores JWT in httpOnly cookie
4. Protected routes check JWT → Redirect to signin if missing
5. API requests include Authorization header with JWT
