"""
User database model for authentication.

Defines the User entity with SQLModel ORM mapping to the 'users' table.
"""
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional


class User(SQLModel, table=True):
    """
    User entity for authentication and user management.

    Maps to the 'users' table in PostgreSQL database.
    Stores user credentials and metadata for authentication.

    Attributes:
        id: Unique user identifier (UUID, primary key, auto-generated)
        email: User's email address (unique, used for sign-in)
        password_hash: Bcrypt hash of user's password (60 characters)
        created_at: Timestamp when user account was created
        updated_at: Timestamp when user account was last modified

    Database Constraints:
        - id: PRIMARY KEY
        - email: UNIQUE (prevents duplicate registrations)
        - All fields: NOT NULL

    Security Notes:
        - password_hash stores bcrypt hash, never plain-text password
        - Email uniqueness enforced at database level
        - UUID prevents user enumeration attacks (vs sequential integers)
        - created_at/updated_at provide audit trail

    Example:
        # Create new user
        user = User(
            email="user@example.com",
            password_hash=hash_password("securepass123")
        )
        db.add(user)
        db.commit()

        # Query user by email
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()
    """

    __tablename__ = "users"

    # Primary key: UUID for security (prevents enumeration)
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique user identifier (UUID)",
    )

    # Email: unique identifier for authentication
    email: str = Field(
        sa_column_kwargs={"unique": True},
        max_length=255,
        nullable=False,
        index=True,  # Index for fast lookups during sign-in
        description="User's email address (unique, used for authentication)",
    )

    # Password hash: bcrypt output (60 characters)
    # VARCHAR(255) allows future algorithm upgrades (e.g., argon2)
    password_hash: str = Field(
        max_length=255,
        nullable=False,
        description="Bcrypt hash of user's password (never store plain-text)",
    )

    # Audit timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was created",
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was last updated",
    )

    class Config:
        """SQLModel configuration for OpenAPI documentation."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "password_hash": "$2b$12$KIXxCc8r9c4yN8fL5vXvRO7gH3sL9tXK8r4yN9fL6vXvRO8gH4sL9",
                "created_at": "2026-01-11T12:00:00Z",
                "updated_at": "2026-01-11T12:00:00Z",
            }
        }
