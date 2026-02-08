"""
Test script for the new authentication and MCP tool HTTP endpoints.

This script demonstrates how to use the newly created endpoints:
1. Register a new user
2. Sign in to get JWT token
3. Get current user info
4. Use MCP tool endpoints (add, list, update, complete, delete tasks)

Usage:
    python test_new_endpoints.py
"""

import requests
import json
from typing import Optional

# Base URL for the FastAPI backend
BASE_URL = "http://localhost:8000"

# Store the JWT token globally
auth_token: Optional[str] = None


def print_response(response, title: str):
    """Helper function to print formatted response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body:")
    print(json.dumps(response.json(), indent=2))


def register_user(email: str, password: str):
    """Register a new user."""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    print_response(response, "1. REGISTER USER")

    if response.status_code == 201:
        global auth_token
        auth_token = response.json()["access_token"]
        print(f"\n✓ Registration successful! Token obtained.")
    else:
        print(f"\n✗ Registration failed.")

    return response


def signin_user(email: str, password: str):
    """Sign in an existing user."""
    url = f"{BASE_URL}/auth/signin"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    print_response(response, "2. SIGN IN USER")

    if response.status_code == 200:
        global auth_token
        auth_token = response.json()["access_token"]
        print(f"\n✓ Sign in successful! Token obtained.")
    else:
        print(f"\n✗ Sign in failed.")

    return response


def get_current_user():
    """Get current authenticated user info."""
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)
    print_response(response, "3. GET CURRENT USER INFO")

    if response.status_code == 200:
        print(f"\n✓ User info retrieved successfully.")
    else:
        print(f"\n✗ Failed to retrieve user info.")

    return response


def add_task(title: str, description: str = ""):
    """Add a new task using MCP tool endpoint."""
    url = f"{BASE_URL}/mcp/add_task"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "title": title,
        "description": description
    }
    response = requests.post(url, json=payload, headers=headers)
    print_response(response, f"4. ADD TASK: {title}")

    if response.status_code == 201:
        print(f"\n✓ Task created successfully.")
        return response.json().get("data", {}).get("task_id")
    else:
        print(f"\n✗ Failed to create task.")
        return None


def list_tasks(status: Optional[str] = None):
    """List tasks using MCP tool endpoint."""
    url = f"{BASE_URL}/mcp/list_tasks"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {"status": status}
    response = requests.post(url, json=payload, headers=headers)
    print_response(response, "5. LIST TASKS")

    if response.status_code == 200:
        print(f"\n✓ Tasks retrieved successfully.")
    else:
        print(f"\n✗ Failed to retrieve tasks.")

    return response


def update_task(task_id: str, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None):
    """Update a task using MCP tool endpoint."""
    url = f"{BASE_URL}/mcp/update_task"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "status": status
    }
    response = requests.post(url, json=payload, headers=headers)
    print_response(response, "6. UPDATE TASK")

    if response.status_code == 200:
        print(f"\n✓ Task updated successfully.")
    else:
        print(f"\n✗ Failed to update task.")

    return response


def complete_task(task_id: str):
    """Complete a task using MCP tool endpoint."""
    url = f"{BASE_URL}/mcp/complete_task"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "task_id": task_id
    }
    response = requests.post(url, json=payload, headers=headers)
    print_response(response, "7. COMPLETE TASK")

    if response.status_code == 200:
        print(f"\n✓ Task completed successfully.")
    else:
        print(f"\n✗ Failed to complete task.")

    return response


def delete_task(task_id: str):
    """Delete a task using MCP tool endpoint."""
    url = f"{BASE_URL}/mcp/delete_task"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    payload = {
        "task_id": task_id
    }
    response = requests.post(url, json=payload, headers=headers)
    print_response(response, "8. DELETE TASK")

    if response.status_code == 200:
        print(f"\n✓ Task deleted successfully.")
    else:
        print(f"\n✗ Failed to delete task.")

    return response


def main():
    """Main test flow."""
    print("\n" + "="*60)
    print("TESTING NEW AUTHENTICATION AND MCP TOOL ENDPOINTS")
    print("="*60)

    # Test user credentials
    test_email = "testuser@example.com"
    test_password = "securepassword123"

    # Step 1: Register a new user (or sign in if already exists)
    print("\n\nAttempting to register new user...")
    register_response = register_user(test_email, test_password)

    if register_response.status_code == 409:
        # User already exists, sign in instead
        print("\nUser already exists, signing in...")
        signin_user(test_email, test_password)

    if not auth_token:
        print("\n✗ Failed to obtain authentication token. Exiting.")
        return

    # Step 2: Get current user info
    get_current_user()

    # Step 3: Add some tasks
    task1_id = add_task("Complete project documentation", "Write comprehensive docs for the new API endpoints")
    task2_id = add_task("Review pull request", "Review and merge the authentication PR")
    task3_id = add_task("Fix bug in task service", "Address the issue with task filtering")

    # Step 4: List all tasks
    list_tasks()

    # Step 5: Update a task
    if task1_id:
        update_task(task1_id, title="Complete project documentation (UPDATED)", status="in_progress")

    # Step 6: Complete a task
    if task2_id:
        complete_task(task2_id)

    # Step 7: List tasks again to see changes
    list_tasks()

    # Step 8: Delete a task
    if task3_id:
        delete_task(task3_id)

    # Step 9: List tasks one final time
    list_tasks()

    print("\n\n" + "="*60)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to the backend server.")
        print("Make sure the FastAPI server is running at http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
