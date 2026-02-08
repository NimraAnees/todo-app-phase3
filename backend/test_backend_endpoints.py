import requests
import json
from uuid import UUID

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("SUCCESS: Health check passed")

def test_authentication():
    """Test user registration and login."""
    # Clean up any existing test user
    print("\n--- Testing Authentication ---")

    # Register a new user
    import time
    timestamp = int(time.time())
    register_data = {
        "email": f"backend-test-{timestamp}@example.com",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=register_data)
    print(f"Registration: {response.status_code}")
    print(f"Registration response: {response.json()}")

    if response.status_code == 201:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"SUCCESS: Registration successful, got token: {access_token[:20]}...")
    else:
        # If user already exists, try to login
        login_data = {
            "email": "backend-test@example.com",
            "password": "testpassword123"
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"SUCCESS: Login successful, got token: {access_token[:20]}...")
        else:
            print(f"ERROR: Login failed: {response.status_code}, {response.text}")
            return None

    # Test getting user profile
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
    print(f"Get user profile: {response.status_code}")
    if response.status_code == 200:
        user_data = response.json()
        print(f"SUCCESS: Got user profile: {user_data['email']}")
    else:
        print(f"ERROR: Get user profile failed: {response.text}")

    return access_token

def test_task_crud_operations(access_token):
    """Test all task CRUD operations."""
    print("\n--- Testing Task CRUD Operations ---")

    headers = {"Authorization": f"Bearer {access_token}"}

    # 1. Create a new task
    task_data = {
        "title": "Test Task from API Test",
        "description": "This task was created via the API test"
    }

    response = requests.post(f"{BASE_URL}/api/v1/tasks/", json=task_data, headers=headers)
    print(f"Create task: {response.status_code}")
    if response.status_code == 201:
        created_task = response.json()
        task_id = created_task["id"]
        print(f"SUCCESS: Created task with ID: {task_id}")
    else:
        print(f"ERROR: Create task failed: {response.status_code}, {response.text}")
        return

    # 2. Get all tasks
    response = requests.get(f"{BASE_URL}/api/v1/tasks/", headers=headers)
    print(f"Get all tasks: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"SUCCESS: Retrieved {len(tasks)} tasks")
        print(f"  First task: {tasks[0]['title']} (completed: {tasks[0]['is_completed']})")
    else:
        print(f"ERROR: Get all tasks failed: {response.text}")

    # 3. Get specific task
    response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}", headers=headers)
    print(f"Get specific task: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        print(f"SUCCESS: Retrieved task: {task['title']}")
    else:
        print(f"ERROR: Get specific task failed: {response.text}")

    # 4. Update the task
    update_data = {
        "title": "Updated Test Task",
        "description": "This task was updated via the API test",
        "is_completed": True
    }

    response = requests.put(f"{BASE_URL}/api/v1/tasks/{task_id}", json=update_data, headers=headers)
    print(f"Update task: {response.status_code}")
    if response.status_code == 200:
        updated_task = response.json()
        print(f"SUCCESS: Updated task: {updated_task['title']} (completed: {updated_task['is_completed']})")
    else:
        print(f"ERROR: Update task failed: {response.status_code}, {response.text}")

    # 5. Delete the task
    response = requests.delete(f"{BASE_URL}/api/v1/tasks/{task_id}", headers=headers)
    print(f"Delete task: {response.status_code}")
    if response.status_code == 204:
        print(f"SUCCESS: Deleted task successfully")
    else:
        print(f"ERROR: Delete task failed: {response.status_code}, {response.text}")

def main():
    """Run all backend API tests."""
    print("Starting Backend API Endpoint Tests...\n")

    # Test health check
    test_api_health()

    # Test authentication
    access_token = test_authentication()

    if access_token:
        # Test task CRUD operations
        test_task_crud_operations(access_token)

    print("\n--- Backend API Tests Complete ---")

if __name__ == "__main__":
    main()