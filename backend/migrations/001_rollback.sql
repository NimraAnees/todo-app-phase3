-- Rollback Migration: Drop users table
-- Date: 2026-01-11
-- Feature: Authentication & Security Layer (1-auth-security)
-- Description: Reverts 001_create_users_table.sql by dropping all created objects

-- Drop trigger first (depends on function and table)
DROP TRIGGER IF EXISTS update_users_updated_at ON users;

-- Drop trigger function
DROP FUNCTION IF EXISTS update_updated_at_column();

-- Drop index (will be dropped with table, but explicit for clarity)
DROP INDEX IF EXISTS idx_users_email;

-- Drop users table (CASCADE removes dependent objects)
DROP TABLE IF EXISTS users CASCADE;

-- Note: We intentionally keep uuid-ossp extension as other features may use it
-- To remove extension (use with caution): DROP EXTENSION IF EXISTS "uuid-ossp";
