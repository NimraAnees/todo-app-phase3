"""
Authentication router for user registration, sign-in, and sign-out.

Endpoints:
- POST /auth/register: Create new user account
- POST /auth/signin: Authenticate existing user
- POST /auth/signout: Sign out current user
- GET /auth/me: Get current user information
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from datetime import datetime, timezone
from jose import jwt
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.schemas.user import UserResponse
from app.core.security import hash_password, verify_password
from app.core.config import settings
from app.dependencies import get_current_user

router = APIRouter()


def create_access_token(user_id: str, email: str) -> str:
    """
    Create a JWT access token.

    Token contains:
    - sub: user_id (subject)
    - email: user's email
    - iat: issued at timestamp
    - exp: expiration timestamp (iat + 3600 seconds)

    Args:
        user_id: User's UUID as string
        email: User's email address

    Returns:
        JWT token string (format: "header.payload.signature")
    """
    now = datetime.now(timezone.utc)
    iat = int(now.timestamp())
    exp = iat + settings.JWT_EXPIRATION_SECONDS

    payload = {
        "sub": user_id,  # Subject: user identifier
        "email": email,
        "iat": iat,  # Issued at
        "exp": exp,  # Expiration
    }

    token = jwt.encode(
        payload,
        settings.BETTER_AUTH_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.

    Creates a new user with hashed password and issues JWT token.

    Args:
        user_create: UserCreate schema with email and password
        db: Database session dependency

    Returns:
        TokenResponse with JWT access token and user information

    Raises:
        HTTPException 400: Email already registered (generic error to prevent enumeration)
        HTTPException 422: Validation error (email format, password length)
    """
    logger.info(f"Register called with: name={user_create.name}, email={user_create.email}")
    # Check if email already exists (case-insensitive)
    statement = select(User).where(User.email.ilike(user_create.email))
    existing_user = db.exec(statement).first()

    if existing_user:
        # Generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create account. Please try a different email."
        )

    # Hash password before storage
    password_hash = hash_password(user_create.password)

    # Create new user
    new_user = User(
        name=user_create.name,
        email=user_create.email.lower(),  # Normalize email to lowercase
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = create_access_token(user_id=str(new_user.id), email=new_user.email)

    logger.info(f"User registered successfully: {new_user.id}")

    # Return token and user data
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            created_at=new_user.created_at
        )
    )


@router.post("/auth/signin", response_model=TokenResponse)
async def signin(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Sign in an existing user.

    Validates credentials and issues JWT token.

    Args:
        user_login: UserLogin schema with email and password
        db: Database session dependency

    Returns:
        TokenResponse with JWT access token and user information

    Raises:
        HTTPException 401: Invalid credentials (generic error for email or password)
    """
    # Find user by email (case-insensitive lookup)
    statement = select(User).where(User.email.ilike(user_login.email.lower()))
    user = db.exec(statement).first()

    logger.info(f"Signin attempt for email: {user_login.email}, found user: {user is not None}")

    # Verify password only if user exists
    if not user or not verify_password(user_login.password, user.password_hash):
        # Generic error message to prevent user enumeration
        logger.warning(f"Invalid credentials for email: {user_login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate JWT token
    token = create_access_token(user_id=str(user.id), email=user.email)

    logger.info(f"User signed in successfully: {user.id}")

    # Return token and user data
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.post("/auth/signout")
async def signout(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Sign out the current user.

    Note: JWT tokens are stateless, so actual token revocation happens client-side
    by clearing the cookie. This endpoint confirms the user is authenticated
    before allowing sign-out.

    Args:
        request: FastAPI request object
        current_user: Current authenticated user from JWT

    Returns:
        Success message
    """
    user_id = current_user.get("sub")
    logger.info(f"Signout called for user: {user_id}")

    # For JWT, we can't actually revoke the token server-side
    # The client should remove the token from storage
    return {"message": "Successfully signed out"}


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information.

    Protected endpoint that requires valid JWT token.

    Args:
        current_user: Current authenticated user from JWT (user_id extracted)
        db: Database session dependency

    Returns:
        UserResponse with user information

    Raises:
        HTTPException 404: User not found (shouldn't happen with valid JWT)
    """
    # Extract user_id from JWT claims
    user_id_str = current_user.get("sub")
    logger.info(f"Getting user info for: {user_id_str}")

    # Convert string user_id to UUID for comparison with User.id
    from uuid import UUID
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        logger.error(f"Invalid user_id format in token: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()

    if not user:
        logger.error(f"User not found in database: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        created_at=user.created_at
    )
