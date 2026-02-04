"""
FastAPI dependencies for authentication and database access.

Provides reusable dependency functions for:
- Current user extraction from JWT token
- Database session management
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlmodel import Session
from typing import Dict
from app.core.security import verify_token
from app.database import get_db


# HTTP Bearer security scheme for OpenAPI documentation
# Adds "Authorize" button in Swagger UI for JWT token input
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security)
) -> Dict[str, str]:
    """
    FastAPI dependency to extract and verify current user from JWT token.

    Extracts JWT token from Authorization: Bearer header.
    Verifies token signature and expiration using security.verify_token().
    Returns decoded JWT claims containing user identity.

    Args:
        credentials: HTTP Bearer credentials extracted from Authorization header

    Returns:
        dict: JWT claims containing:
            - sub: User ID (UUID as string)
            - email: User email address
            - iat: Issued at timestamp
            - exp: Expiration timestamp

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or expired

    Usage:
        @app.get("/api/v1/protected")
        async def protected_route(current_user: dict = Depends(get_current_user)):
            user_id = current_user["sub"]
            return {"message": f"Hello user {user_id}"}

    Example:
        # In a route handler
        @app.get("/api/v1/todos")
        async def get_todos(
            current_user: dict = Depends(get_current_user),
            db: Session = Depends(get_db)
        ):
            user_id = current_user["sub"]
            # Query todos filtered by user_id
            todos = db.exec(
                select(Todo).where(Todo.user_id == user_id)
            ).all()
            return todos

    Security Notes:
        - Always filter database queries by user_id from JWT claims
        - Never trust user_id from request body or query parameters
        - JWT signature ensures user_id cannot be forged
        - Token expiration is enforced automatically (1 hour)
    """
    token = credentials.credentials
    return verify_token(token)


# Export get_db for convenience
# Usage: db: Session = Depends(get_db)
__all__ = ["get_current_user", "get_db"]
