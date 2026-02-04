"""
Pydantic schemas for authentication requests and responses.

Defines request/response models for:
- User registration (UserCreate)
- User sign-in (UserLogin)
- Authentication token response (TokenResponse)
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Used by POST /api/v1/auth/register endpoint.
    Validates email format and password length at API boundary.

    Attributes:
        email: User's email address (validated by EmailStr)
        password: Plain-text password (minimum 8 characters)

    Validation Rules:
        - email: Must be valid RFC 5322 email format
        - password: Minimum 8 characters (no maximum, bcrypt handles up to 72 bytes)

    Security Notes:
        - Password validated for length only (complexity optional in Phase 2)
        - Password hashed before storage (never store plain-text)
        - Email uniqueness checked against database

    Example Request:
        POST /api/v1/auth/register
        {
            "email": "newuser@example.com",
            "password": "securepassword123"
        }
    """

    email: EmailStr = Field(
        ...,
        description="User's email address (must be unique)",
        examples=["newuser@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User's password (minimum 8 characters)",
        examples=["securepassword123"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "newuser@example.com",
                "password": "securepassword123",
            }
        }
    )


class UserLogin(BaseModel):
    """
    Schema for user sign-in request.

    Used by POST /api/v1/auth/signin endpoint.
    Validates email format at API boundary.

    Attributes:
        email: User's email address
        password: Plain-text password

    Validation Rules:
        - email: Must be valid RFC 5322 email format
        - password: No validation (checked against hash in database)

    Security Notes:
        - Generic error for wrong email or password (prevent enumeration)
        - Always hash password attempt even if email not found (prevent timing attacks)
        - Failed attempts should be rate-limited (5 per 15 minutes)

    Example Request:
        POST /api/v1/auth/signin
        {
            "email": "user@example.com",
            "password": "securepassword123"
        }
    """

    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        description="User's password",
        examples=["securepassword123"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
            }
        }
    )


class TokenResponse(BaseModel):
    """
    Schema for JWT token response after successful authentication.

    Returned by POST /api/v1/auth/register and POST /api/v1/auth/signin.
    Contains JWT access token and user information.

    Attributes:
        access_token: JWT token string (format: "header.payload.signature")
        token_type: Token type (always "bearer" for JWT)
        user: User information (UserResponse schema)

    Token Details:
        - Algorithm: HS256 (HMAC-SHA256)
        - Expiration: 1 hour (3600 seconds)
        - Claims: sub (user_id), email, iat, exp

    Usage:
        Frontend stores access_token in httpOnly cookie.
        Backend verifies token on protected endpoints.

    Example Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "created_at": "2026-01-11T12:00:00Z"
            }
        }
    """

    access_token: str = Field(
        ...,
        description="JWT access token (1 hour expiration)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always 'bearer' for JWT)",
        examples=["bearer"],
    )

    # Import UserResponse inline to avoid circular import
    # Defined in schemas/user.py
    user: "UserResponse" = Field(
        ...,
        description="User information (excludes password_hash)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "user@example.com",
                    "created_at": "2026-01-11T12:00:00Z",
                },
            }
        }
    )


# Import UserResponse for type checking
# Placed at end to avoid circular import issues
from app.schemas.user import UserResponse

# Update forward references
TokenResponse.model_rebuild()
