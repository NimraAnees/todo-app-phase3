# Todo App - Backend API

FastAPI-based authentication and todo management API.

## Setup

### 1. Create virtual environment
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your database URL and generate BETTER_AUTH_SECRET
```

### 4. Generate secret
```bash
openssl rand -base64 48
```

### 5. Run database migrations

#### Option A: Using psql CLI (Recommended)
```bash
# Set your DATABASE_URL from .env file
export DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f2-)

# Run migration
psql $DATABASE_URL -f migrations/001_create_users_table.sql

# Verify migration
psql $DATABASE_URL -c "\d users"
```

#### Option B: Using Neon SQL Editor
1. Copy contents of `migrations/001_create_users_table.sql`
2. Navigate to Neon dashboard > SQL Editor
3. Paste and execute SQL
4. Verify with: `SELECT * FROM users LIMIT 1;`

#### Option C: Using Python
```bash
python3 -c "
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = conn.cursor()

with open('migrations/001_create_users_table.sql', 'r') as f:
    cursor.execute(f.read())

conn.commit()
cursor.close()
conn.close()
print('Migration completed successfully')
"
```

For detailed migration documentation, see [migrations/README.md](./migrations/README.md)

### 6. Start development server
```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database connection
│   ├── dependencies.py      # FastAPI dependencies
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   └── security.py     # JWT & password utilities
│   ├── middleware/
│   │   └── auth_middleware.py  # JWT verification
│   ├── models/
│   │   └── user.py         # User SQLModel
│   ├── schemas/
│   │   ├── auth.py         # Auth request/response schemas
│   │   └── user.py         # User schemas
│   └── routers/
│       └── auth.py         # Authentication endpoints
├── migrations/
│   ├── README.md            # Migration documentation
│   ├── 001_create_users_table.sql  # Users table migration
│   └── 001_rollback.sql     # Rollback for users table
└── tests/                   # Test suite
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (min 32 chars)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
