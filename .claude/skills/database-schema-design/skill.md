---
name: database-schema-design
description: Design relational database schemas, create tables, and manage migrations safely. Use for backend and full-stack applications.
---

# Database Skill – Tables, Migrations & Schema Design

## Instructions

1. **Schema planning**
   - Identify entities and relationships
   - Define primary keys and foreign keys
   - Normalize data (avoid redundancy)

2. **Table creation**
   - Use appropriate data types
   - Apply constraints (NOT NULL, UNIQUE)
   - Add indexes for performance

3. **Migrations**
   - Create incremental migration files
   - Ensure migrations are reversible
   - Version-control schema changes

4. **Relationships**
   - One-to-One
   - One-to-Many
   - Many-to-Many (junction tables)

## Best Practices
- Use snake_case for table and column names
- Always include timestamps where relevant
- Avoid breaking changes in production databases
- Test migrations on staging before production
- Keep migrations small and atomic

## Example Structure
```sql
-- users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts table
CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
