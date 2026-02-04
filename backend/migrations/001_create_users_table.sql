-- Migration: Create users table
-- Date: 2026-01-11
-- Feature: Authentication & Security Layer (1-auth-security)
-- Description: Creates users table with UUID primary key, unique email, password hash, and timestamps

-- Enable UUID generation extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create index on email column for fast lookups during sign-in
-- Rationale: Email lookups occur on every authentication, index improves query performance (O(log n) vs O(n))
CREATE INDEX idx_users_email ON users(email);

-- Create trigger function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update updated_at before any UPDATE on users table
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Verification queries (run after migration to validate)
-- SELECT COUNT(*) FROM users; -- Should return 0 (empty table)
-- \d users; -- Describe table structure
-- SELECT indexname, indexdef FROM pg_indexes WHERE tablename = 'users'; -- Verify index exists
