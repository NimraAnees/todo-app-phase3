"""
Pydantic schemas for user-related API responses.

Defines response models that exclude sensitive information (password_hash).
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.

    Excludes password_hash and other sensitive fields.
    Used in authentication responses and user profile endpoints.

    Attributes:
        id: User's unique identifier (UUID)
        email: User's email address
        created_at: Timestamp when account was created

    Security Notes:
        - NEVER include password_hash in API responses
        - NEVER include password field (even hashed)
        - Only expose non-sensitive user information

    Usage:
        # In TokenResponse
        {
            "access_token": "...",
            "token_type": "bearer",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-11T12:00:00Z"
            }
        }

        # In GET /api/v1/auth/me
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "created_at": "2026-01-11T12:00:00Z"
        }

    Example Response:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "user@example.com",
            "created_at": "2026-01-11T12:00:00Z"
        }
    """

    id: UUID = Field(
        ...,
        description="User's unique identifier (UUID)",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"],
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when user account was created",
        examples=["2026-01-11T12:00:00Z"],
    )

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLModel conversion
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-11T12:00:00Z",
            }
        },
    )
