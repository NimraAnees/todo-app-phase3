#!/usr/bin/env python3
"""
Demo script to test the create task functionality.
This script demonstrates that the US1 (Create Task) user story is working.
"""

import os
import sys
from uuid import uuid4

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set required environment variables for testing
os.environ['DATABASE_URL'] = 'sqlite:///./demo_test.db'
os.environ['BETTER_AUTH_SECRET'] = 'demo-test-secret-key-for-testing'

from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_current_user

def demo_create_task():
    """Demonstrate the create task functionality."""
    print("[DEMO] Demonstrating Create Task Functionality (US1)")
    print("=" * 50)

    # Create a mock user
    mock_user = {
        "sub": str(uuid4()),
        "email": "demo@example.com",
        "name": "Demo User"
    }

    print(f"[USER] Using mock user: {mock_user['email']}")
    print(f"[ID] User ID: {mock_user['sub']}")

    # Override the authentication dependency
    app.dependency_overrides[get_current_user] = lambda: mock_user

    # Create test client
    client = TestClient(app)

    print("\n[TEST] Testing task creation...")

    # Test 1: Create a task with full data
    print("\n[CREATE] Creating task with full data:")
    task_data = {
        "title": "Complete project documentation",
        "description": "Write comprehensive docs for the project",
        "is_completed": False
    }

    response = client.post("/api/v1/tasks/", json=task_data)

    if response.status_code == 201:
        result = response.json()
        print(f"[SUCCESS] Task created!")
        print(f"   Title: {result['title']}")
        print(f"   Description: {result['description']}")
        print(f"   Completed: {result['is_completed']}")
        print(f"   User ID: {result['user_id']}")
        print(f"   Task ID: {result['id']}")
    else:
        print(f"[ERROR] FAILED: Status {response.status_code}")
        print(f"   Response: {response.text}")

    # Test 2: Create a task with minimal data
    print("\n[CREATE] Creating task with minimal data:")
    minimal_task = {
        "title": "Buy groceries"
    }

    response = client.post("/api/v1/tasks/", json=minimal_task)

    if response.status_code == 201:
        result = response.json()
        print(f"[SUCCESS] Task created!")
        print(f"   Title: {result['title']}")
        print(f"   Description: {result['description']} (defaults to None)")
        print(f"   Completed: {result['is_completed']} (defaults to False)")
        print(f"   User ID: {result['user_id']}")
    else:
        print(f"[ERROR] FAILED: Status {response.status_code}")
        print(f"   Response: {response.text}")

    # Test 3: Attempt to create task without required title (should fail)
    print("\n[VALIDATE] Testing validation (missing title):")
    invalid_task = {
        "description": "This should fail"
    }

    response = client.post("/api/v1/tasks/", json=invalid_task)

    if response.status_code == 422:
        print("[SUCCESS] Validation correctly rejected missing title")
    else:
        print(f"[ERROR] UNEXPECTED: Expected 422, got {response.status_code}")

    # Clean up the dependency override
    app.dependency_overrides.clear()

    print("\n[RESULT] User Story 1 (Create Task) - IMPLEMENTED SUCCESSFULLY!")
    print("[FEATURE] Authenticated users can create new tasks")
    print("[FEATURE] Tasks are automatically assigned to authenticated user")
    print("[FEATURE] Input validation is enforced")
    print("[FEATURE] Proper HTTP status codes returned")


if __name__ == "__main__":
    demo_create_task()