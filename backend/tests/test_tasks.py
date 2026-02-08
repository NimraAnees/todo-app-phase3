import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from uuid import uuid4
from unittest.mock import AsyncMock

# Set required environment variables for testing
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'  # Use SQLite for testing
os.environ['BETTER_AUTH_SECRET'] = 'test-secret-key-for-testing-purposes-only'

from app.main import app
from app.models.task import Task
from app.models.user import User
from app.dependencies import get_current_user


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    # Create a mock user for authentication
    mock_user = {
        "sub": str(uuid4()),  # user_id as string UUID
        "email": "test@example.com",
        "name": "Test User"
    }

    # Override the get_current_user dependency
    app.dependency_overrides[get_current_user] = lambda: mock_user

    with TestClient(app) as test_client:
        yield test_client

    # Clean up the dependency override after the test
    app.dependency_overrides.clear()


def test_create_task_success(client):
    """Test successful task creation."""
    # Test data
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "is_completed": False
    }

    # Make request
    response = client.post("/api/v1/tasks/", json=task_data)

    # Assertions
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == "Test Task"
    assert response_data["description"] == "This is a test task"
    assert response_data["is_completed"] is False
    assert "id" in response_data
    assert "user_id" in response_data
    assert "created_at" in response_data
    assert "updated_at" in response_data


def test_create_task_minimal_data(client):
    """Test task creation with minimal required data."""
    # Test data with only required fields
    task_data = {
        "title": "Minimal Task"
    }

    # Make request
    response = client.post("/api/v1/tasks/", json=task_data)

    # Assertions
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == "Minimal Task"
    assert response_data["description"] is None
    assert response_data["is_completed"] is False
    assert "user_id" in response_data


def test_create_task_missing_title(client):
    """Test task creation with missing title (should fail validation)."""
    # Test data with missing required title
    task_data = {
        "description": "Task without title"
    }

    # Make request
    response = client.post("/api/v1/tasks/", json=task_data)

    # Should return validation error
    assert response.status_code == 422


def test_create_task_empty_title(client):
    """Test task creation with empty title (should fail validation)."""
    # Test data with empty title
    task_data = {
        "title": ""
    }

    # Make request
    response = client.post("/api/v1/tasks/", json=task_data)

    # Should return validation error
    assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__])