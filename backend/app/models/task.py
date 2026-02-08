"""
Task database model for the todo application.
Defines the Task entity with SQLModel ORM mapping to the 'tasks' table.
"""
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.
    """
    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique task identifier",
    )
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to User
    # user: Optional["User"] = Relationship(back_populates="tasks")
