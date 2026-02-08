from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import schemas
from ..config.settings import settings
import uuid


class AuthService:
    """
    Service class for handling authentication operations.
    """

    def __init__(self):
        # Configure bcrypt with explicit settings for compatibility with bcrypt 5.0+
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__default_rounds=12,
            bcrypt__default_ident="2b"
        )
        self.algorithm = settings.jwt_algorithm
        self.secret_key = settings.jwt_secret

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if passwords match, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password.

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password
        """
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.

        Args:
            data: Data to encode in the token
            expires_delta: Optional expiration time delta (uses default if not provided)

        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(seconds=settings.jwt_expiration_seconds)
        )
        to_encode.update({"exp": expire, "sub": str(data.get("user_id", ""))})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decode a JWT token and return the payload.

        Args:
            token: JWT token to decode

        Returns:
            Token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None


# Global instance
auth_service = AuthService()

# Security scheme for FastAPI
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency function to get the current authenticated user from the JWT token.

    Args:
        credentials: HTTP authorization credentials from the request

    Returns:
        User information from the token

    Raises:
        HTTPException: If the token is invalid or expired
    """
    token = credentials.credentials
    payload = auth_service.decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user_id": user_id,
        "email": payload.get("email"),
        "expires_at": payload.get("exp")
    }


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from a JWT token.

    Args:
        token: JWT token to extract user_id from

    Returns:
        User ID if token is valid, None otherwise
    """
    payload = auth_service.decode_token(token)
    if payload:
        return payload.get("sub")
    return None