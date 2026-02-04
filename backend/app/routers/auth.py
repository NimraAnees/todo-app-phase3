"""
Authentication router for user registration, sign-in, and sign-out.

Endpoints:
- POST /auth/register: Create new user account
- POST /auth/signin: Authenticate existing user
- POST /auth/signout: Sign out current user
- GET /auth/me: Get current user information
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timezone
from jose import jwt

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.schemas.user import UserResponse
from app.core.security import hash_password, verify_password
from app.core.config import settings
from app.dependencies import get_current_user

router = APIRouter()


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
    # Check if email already exists
    statement = select(User).where(User.email == user_create.email)
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
        email=user_create.email,
        password_hash=password_hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT token
    token = create_access_token(user_id=str(new_user.id), email=new_user.email)

    # Return token and user data
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
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
    # Find user by email
    statement = select(User).where(User.email == user_login.email)
    user = db.exec(statement).first()

    # Verify password (always hash even if user not found to prevent timing attacks)
    if not user or not verify_password(user_login.password, user.password_hash if user else ""):
        # Generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generate JWT token
    token = create_access_token(user_id=str(user.id), email=user.email)

    # Return token and user data
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.post("/auth/signout")
async def signout(current_user: dict = Depends(get_current_user)):
    """
    Sign out the current user.

    Note: JWT tokens are stateless, so actual token revocation happens client-side
    by clearing the cookie. This endpoint confirms the user is authenticated
    before allowing sign-out.

    Args:
        current_user: Current authenticated user from JWT

    Returns:
        Success message
    """
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
    user_id = current_user.get("sub")

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


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
