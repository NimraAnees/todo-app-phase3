from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.task import Task
from ..models.user import User
from ..utils.errors import NotFoundException, ValidationException
from ..utils.logging import log_error
from fastapi import HTTPException, status


class TaskService:
    """
    Service class for handling task-related operations.
    """

    @staticmethod
    def create_task(session: Session, user_id: uuid.UUID, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            user_id: ID of the user creating the task
            title: Title of the task
            description: Optional description of the task

        Returns:
            Created Task object
        """
        try:
            # Validate inputs
            if not title.strip():
                raise ValidationException(detail="Task title cannot be empty")

            # Create the task
            task = Task(
                user_id=user_id,
                title=title.strip(),
                description=description,
                status="pending"
            )
            session.add(task)
            session.commit()
            session.refresh(task)

            return task
        except Exception as e:
            log_error(e, "Creating task", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def get_user_tasks(session: Session, user_id: uuid.UUID, status_filter: Optional[str] = None) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by status.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            status_filter: Optional status to filter tasks by (pending, in_progress, completed)

        Returns:
            List of Task objects for the user
        """
        try:
            query = select(Task).where(Task.user_id == user_id)

            if status_filter:
                query = query.where(Task.status == status_filter)

            tasks = session.exec(query).all()
            return tasks
        except Exception as e:
            log_error(e, "Retrieving user tasks", str(user_id))
            raise

    @staticmethod
    def get_task_by_id(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Get a specific task by its ID for a user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user (to ensure access control)

        Returns:
            Task object if found and belongs to user, None otherwise
        """
        try:
            task = session.get(Task, task_id)

            # Ensure the task belongs to the user
            if task and task.user_id != user_id:
                return None

            return task
        except Exception as e:
            log_error(e, "Retrieving task by ID", str(user_id))
            raise

    @staticmethod
    def update_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID,
                    title: Optional[str] = None, description: Optional[str] = None,
                    status: Optional[str] = None) -> Optional[Task]:
        """
        Update a task for a user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user (to ensure access control)
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)

        Returns:
            Updated Task object if successful, None if not found or not owned by user
        """
        try:
            # Get the task
            task = session.get(Task, task_id)

            # Ensure the task exists and belongs to the user
            if not task or task.user_id != user_id:
                return None

            # Update fields if provided
            if title is not None:
                task.title = title.strip() if title.strip() else task.title
            if description is not None:
                task.description = description
            if status is not None:
                task.status = status
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return task
        except Exception as e:
            log_error(e, "Updating task", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        """
        Delete a task for a user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user (to ensure access control)

        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        try:
            # Get the task
            task = session.get(Task, task_id)

            # Ensure the task exists and belongs to the user
            if not task or task.user_id != user_id:
                return False

            session.delete(task)
            session.commit()

            return True
        except Exception as e:
            log_error(e, "Deleting task", str(user_id))
            session.rollback()
            raise

    @staticmethod
    def complete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
        """
        Mark a task as completed.

        Args:
            session: Database session
            task_id: ID of the task to complete
            user_id: ID of the user (to ensure access control)

        Returns:
            Updated Task object if successful, None if not found or not owned by user
        """
        try:
            # Get the task
            task = session.get(Task, task_id)

            # Ensure the task exists and belongs to the user
            if not task or task.user_id != user_id:
                return None

            # Update task status and completion timestamp
            task.status = "completed"
            task.completed_at = datetime.utcnow()
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return task
        except Exception as e:
            log_error(e, "Completing task", str(user_id))
            session.rollback()
            raise