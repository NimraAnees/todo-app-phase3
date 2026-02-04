# Database Migrations

This directory contains SQL migration scripts for the todo-app PostgreSQL database.

## Migration Naming Convention

`{version}_{description}.sql` - Forward migration
`{version}_rollback.sql` - Rollback migration

Example:
- `001_create_users_table.sql` - Creates users table
- `001_rollback.sql` - Drops users table

## Prerequisites

1. PostgreSQL database provisioned (Neon Serverless recommended)
2. Database connection credentials configured in `.env`
3. `psql` CLI tool installed (part of PostgreSQL client)

## Running Migrations

### Method 1: Using psql CLI (Recommended)

```bash
# Set database connection string from .env
export DATABASE_URL="postgresql://user:password@host:5432/database?sslmode=require"

# Run forward migration
psql $DATABASE_URL -f migrations/001_create_users_table.sql

# Verify migration
psql $DATABASE_URL -c "\d users"
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

### Method 2: Using Neon SQL Editor

1. Navigate to your Neon project dashboard
2. Open SQL Editor
3. Copy contents of migration file (e.g., `001_create_users_table.sql`)
4. Paste and execute in SQL Editor
5. Verify by running: `SELECT * FROM users LIMIT 1;`

### Method 3: Using Python Script

```bash
# From backend directory
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

## Rolling Back Migrations

```bash
# Run rollback migration
psql $DATABASE_URL -f migrations/001_rollback.sql

# Verify rollback
psql $DATABASE_URL -c "\dt users"  # Should show "Did not find any relation named 'users'"
```

## Migration History

| Version | Description | Date | Status |
|---------|-------------|------|--------|
| 001 | Create users table with UUID, email, password_hash, timestamps, index, trigger | 2026-01-11 | ✅ Ready |

## Verification Checklist

After running `001_create_users_table.sql`, verify:

- [ ] Table `users` exists
- [ ] Column `id` is UUID type with PRIMARY KEY constraint
- [ ] Column `email` has UNIQUE and NOT NULL constraints
- [ ] Column `password_hash` is VARCHAR(255) NOT NULL
- [ ] Columns `created_at` and `updated_at` are TIMESTAMP WITH TIME ZONE NOT NULL with DEFAULT NOW()
- [ ] Index `idx_users_email` exists on `email` column
- [ ] Trigger `update_users_updated_at` exists
- [ ] Function `update_updated_at_column()` exists

### Verification SQL Commands

```sql
-- Check table structure
\d users

-- Check constraints
SELECT conname, contype, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'users'::regclass;

-- Check indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';

-- Check triggers
SELECT tgname, pg_get_triggerdef(oid)
FROM pg_trigger
WHERE tgrelid = 'users'::regclass;

-- Test trigger (insert and update to verify updated_at changes)
INSERT INTO users (email, password_hash)
VALUES ('test@example.com', 'dummy_hash')
RETURNING id, email, created_at, updated_at;

-- Wait 1 second, then update
SELECT pg_sleep(1);

UPDATE users
SET email = 'test2@example.com'
WHERE email = 'test@example.com'
RETURNING id, email, created_at, updated_at;

-- Verify updated_at changed (should be > created_at)
SELECT id, email, created_at, updated_at,
       (updated_at > created_at) as trigger_worked
FROM users
WHERE email = 'test2@example.com';

-- Clean up test data
DELETE FROM users WHERE email = 'test2@example.com';
```

## Troubleshooting

### Error: "extension 'uuid-ossp' does not exist"

**Solution**: Neon PostgreSQL includes this extension by default. If using another PostgreSQL provider:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Error: "relation 'users' already exists"

**Solution**: Table already created. To recreate:
```bash
psql $DATABASE_URL -f migrations/001_rollback.sql
psql $DATABASE_URL -f migrations/001_create_users_table.sql
```

### Error: "permission denied to create extension"

**Solution**: Ensure database user has SUPERUSER privileges or extension is pre-installed.

### Connection Issues

**Solution**: Verify DATABASE_URL format:
```
postgresql://user:password@host:5432/database?sslmode=require
```

For Neon, get connection string from Neon dashboard (Settings → Connection String).

## Best Practices

1. **Always test migrations in a development database first** (use Neon branching feature)
2. **Never modify executed migrations** - create a new migration to alter schema
3. **Always create rollback migrations** for production deployments
4. **Verify migrations** using the verification checklist above
5. **Backup production database** before running migrations
6. **Use transactions** for complex migrations (wrap in BEGIN; ... COMMIT;)

## Neon-Specific Features

### Using Neon Database Branching for Safe Migrations

```bash
# Create a development branch from main database
neon branches create --name migration-test

# Get branch connection string
neon connection-string migration-test

# Run migration on branch
psql "postgresql://..." -f migrations/001_create_users_table.sql

# Test application with branch
export DATABASE_URL="postgresql://...branch..."

# If successful, run on main database
neon connection-string main
psql "postgresql://..." -f migrations/001_create_users_table.sql

# Delete test branch
neon branches delete migration-test
```

## Future Migrations

For subsequent migrations, use incremental versioning:
- `002_add_todos_table.sql` / `002_rollback.sql`
- `003_add_sessions_table.sql` / `003_rollback.sql`

Always document:
- What changed
- Why it changed
- How to verify
- How to rollback
