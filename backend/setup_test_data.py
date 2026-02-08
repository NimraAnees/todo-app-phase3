import asyncio
import os
from datetime import datetime, timedelta
from uuid import UUID
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.task import Task
from app.core.security import hash_password

def create_test_data():
    """Create test user and tasks for verification."""

    # Create a test user
    test_email = "test@example.com"
    test_password = "testpassword123"

    with Session(engine) as session:
        # Check if test user already exists
        existing_user = session.exec(select(User).where(User.email == test_email)).first()

        if existing_user:
            print(f"Test user {test_email} already exists with ID: {existing_user.id}")
            user = existing_user
        else:
            # Create new test user
            user = User(
                email=test_email,
                password_hash=hash_password(test_password)
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"Created test user: {user.email} with ID: {user.id}")

        # Create some test tasks for this user
        test_tasks = [
            Task(title="Test Task 1", description="This is the first test task", user_id=user.id),
            Task(title="Test Task 2", description="This is the second test task", user_id=user.id),
            Task(title="Test Task 3", is_completed=True, user_id=user.id),  # Completed task
        ]

        for task in test_tasks:
            existing_task = session.exec(
                select(Task).where(Task.title == task.title, Task.user_id == user.id)
            ).first()

            if not existing_task:
                session.add(task)
                print(f"Created task: {task.title}")

        session.commit()
        print("Test data setup complete!")

if __name__ == "__main__":
    print("Setting up test data for backend API...")
    create_test_data()
    print("Test data created successfully!")