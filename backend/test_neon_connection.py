#!/usr/bin/env python3
"""
Test script to verify database connection and table creation in Neon PostgreSQL.
"""

import os
import sys
import asyncio

# Set required environment variables for testing
# These should match your actual Neon database connection string
os.environ.setdefault('DATABASE_URL', 'postgresql://neondb_owner:npg_1CBphnFPQZm6@ep-polished-term-ahceomx7-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
os.environ.setdefault('BETTER_AUTH_SECRET', 'BhU26MUjPil2fVEG9Ae91R7gVbFrD7DxKZTNhtE6ykM3n7GB3Xnc2b0rhPlYmqs/')

def test_database_connection():
    """Test the database connection and table creation."""
    # Import after setting environment variables
    from sqlmodel import select, Session
    from app.database import engine, create_db_and_tables
    from app.models.user import User
    from app.models.task import Task
    from app.core.config import settings

    print("[TEST] Testing Database Connection to Neon PostgreSQL")
    print("=" * 50)
    print(f"Database URL: {settings.DATABASE_URL.replace('://', '://***:***@') if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    print(f"Debug mode: {settings.DEBUG}")

    try:
        print("\n[CREATE] Creating database tables...")
        create_db_and_tables()
        print("[SUCCESS] Tables created successfully!")

        print("\n[CHECK] Checking existing tables...")
        # Reflect the database to see what tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables found: {tables}")

        # Check if our tables exist
        expected_tables = ['users', 'tasks']
        for table in expected_tables:
            if table in tables:
                print(f"[FOUND] '{table}' table exists")
            else:
                print(f"[MISSING] '{table}' table missing")

        # Test creating a session and querying
        print("\n[SESSION] Testing database session...")
        with Session(engine) as session:
            # Count existing users
            user_count = session.exec(select(User)).all()
            print(f"[CONNECTED] Connected to database, found {len(user_count)} existing users")

            # Count existing tasks
            task_count = session.exec(select(Task)).all()
            print(f"[DATA] Found {len(task_count)} existing tasks")

        print("\n[COMPLETE] Database connection and table creation test completed successfully!")
        print("[INFO] The tables should now be visible in your Neon dashboard.")

    except Exception as e:
        print(f"\n[ERROR] Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_database_connection()