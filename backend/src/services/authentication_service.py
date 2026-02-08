from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
import uuid
from ..models.user import User
from ..auth.auth import auth_service
from ..utils.errors import ValidationException, UnauthorizedException
from ..utils.logging import log_error


class AuthenticationService:
    """
    Service class for handling authentication-related operations.
    """

    @staticmethod
    def register_user(session: Session, email: str, password: str) -> User:
        """
        Register a new user with email and password.

        Args:
            session: Database session
            email: User's email address
            password: User's password (will be hashed)

        Returns:
            Created User object
        """
        try:
            # Validate inputs
            if not email or '@' not in email:
                raise ValidationException(detail="Invalid email address")

            if len(password) < 6:
                raise ValidationException(detail="Password must be at least 6 characters long")

            # Check if user already exists
            existing_user = session.exec(select(User).where(User.email == email)).first()
            if existing_user:
                raise ValidationException(detail="User with this email already exists")

            # Hash the password
            hashed_password = auth_service.hash_password(password)

            # Create the user
            user = User(
                email=email,
                hashed_password=hashed_password,  # Set the hashed password
                is_active=True
            )
            user.id = uuid.uuid4()  # Explicitly assign UUID

            session.add(user)
            session.commit()
            session.refresh(user)

            return user
        except ValidationException:
            raise
        except Exception as e:
            log_error(e, "Registering user", email)
            session.rollback()
            raise

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[dict]:
        """
        Authenticate a user with email and password.

        Args:
            session: Database session
            email: User's email address
            password: User's password

        Returns:
            Dictionary with user info and access token if authentication is successful,
            None otherwise
        """
        try:
            # Find the user by email
            user = session.exec(select(User).where(User.email == email)).first()

            # Check if user exists and is active
            if not user or not user.is_active:
                return None

            # Verify the password
            if not auth_service.verify_password(password, user.hashed_password):
                return None

            # Create access token
            token_data = {
                "user_id": str(user.id),
                "email": user.email
            }
            access_token = auth_service.create_access_token(
                data=token_data,
                expires_delta=timedelta(seconds=3600)  # Use default expiry
            )

            return {
                "user_id": user.id,
                "email": user.email,
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception as e:
            log_error(e, "Authenticating user", email)
            raise

    @staticmethod
    def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
        """
        Get a user by their ID.

        Args:
            session: Database session
            user_id: ID of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            user = session.get(User, user_id)
            return user if user and user.is_active else None
        except Exception as e:
            log_error(e, "Getting user by ID", str(user_id))
            raise

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Get a user by their email address.

        Args:
            session: Database session
            email: Email address of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            user = session.exec(select(User).where((User.email == email) & (User.is_active == True))).first()
            return user
        except Exception as e:
            log_error(e, "Getting user by email", email)
            raise