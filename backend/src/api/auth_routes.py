from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
import uuid

from ..database import get_session
from ..auth import schemas
from ..auth.auth import get_current_user
from ..services.authentication_service import AuthenticationService
from ..utils.errors import ValidationException, UnauthorizedException


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: schemas.UserCreate,
    session: Session = Depends(get_session)
) -> Dict[str, str]:
    """
    Register a new user account.

    Creates a new user with email and password, then returns a JWT access token.

    Args:
        user_data: User registration data (email and password)
        session: Database session (injected)

    Returns:
        JWT access token and token type

    Raises:
        HTTPException 400: If validation fails (invalid email, weak password)
        HTTPException 409: If user with email already exists
        HTTPException 500: If registration fails due to server error
    """
    try:
        # Register the user
        user = AuthenticationService.register_user(
            session=session,
            email=user_data.email,
            password=user_data.password
        )

        # Authenticate the newly registered user to get token
        auth_result = AuthenticationService.authenticate_user(
            session=session,
            email=user_data.email,
            password=user_data.password
        )

        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to authenticate after registration"
            )

        return {
            "access_token": auth_result["access_token"],
            "token_type": auth_result["token_type"]
        }

    except ValidationException as e:
        # Handle validation errors (invalid email, weak password, duplicate user)
        if "already exists" in str(e.detail):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e.detail)
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.detail)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/signin", response_model=schemas.Token)
def signin_user(
    user_data: schemas.UserLogin,
    session: Session = Depends(get_session)
) -> Dict[str, str]:
    """
    Sign in an existing user.

    Authenticates user with email and password, returns JWT access token.

    Args:
        user_data: User login credentials (email and password)
        session: Database session (injected)

    Returns:
        JWT access token and token type

    Raises:
        HTTPException 401: If credentials are invalid or user not found
        HTTPException 500: If authentication fails due to server error
    """
    try:
        # Authenticate the user
        auth_result = AuthenticationService.authenticate_user(
            session=session,
            email=user_data.email,
            password=user_data.password
        )

        if not auth_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {
            "access_token": auth_result["access_token"],
            "token_type": auth_result["token_type"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )


@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(
    current_user: Dict = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> schemas.UserResponse:
    """
    Get the currently authenticated user's information.

    Requires valid JWT token in Authorization header.

    Args:
        current_user: Current authenticated user data (injected from JWT token)
        session: Database session (injected)

    Returns:
        User information (id, email, is_active)

    Raises:
        HTTPException 401: If token is invalid or missing
        HTTPException 404: If user not found in database
        HTTPException 500: If retrieval fails due to server error
    """
    try:
        # Extract user_id from token payload
        user_id_str = current_user.get("user_id")
        if not user_id_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        # Convert string to UUID
        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: malformed user_id"
            )

        # Retrieve user from database
        user = AuthenticationService.get_user_by_id(
            session=session,
            user_id=user_id
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return schemas.UserResponse(
            id=user.id,
            email=user.email,
            is_active=user.is_active
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user information: {str(e)}"
        )
