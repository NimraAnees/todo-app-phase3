"""
Security utilities for password hashing and JWT token verification.

Provides:
- Password hashing with bcrypt (work factor 12)
- Password verification with constant-time comparison
- JWT token verification using python-jose
"""
import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Uses bcrypt with work factor 12 for strong password security.
    The resulting hash is 60 characters long and includes the salt.

    Args:
        password: Plain-text password to hash (minimum 8 characters enforced elsewhere)

    Returns:
        str: Bcrypt hash of the password (60 characters)

    Example:
        >>> hash_password("mypassword123")
        '$2b$12$KIXxCc8r9c4yN8fL5vXvRO7gH3sL9tXK8r4yN9fL6vXvRO8gH4sL9'

    Security Notes:
        - Never log the input password
        - Never store the plain-text password
        - Always validate password length before hashing
        - Bcrypt automatically generates and includes a random salt
    """
    # Generate salt with work factor 12
    salt = bcrypt.gensalt(rounds=12)
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.

    Uses constant-time comparison to prevent timing attacks.
    Returns False if the password doesn't match or if hash is invalid.

    Args:
        plain_password: Plain-text password provided by user
        hashed_password: Bcrypt hash from database (60 characters)

    Returns:
        bool: True if password matches hash, False otherwise

    Example:
        >>> stored_hash = "$2b$12$KIXxCc8r9c4yN8fL5vXvRO..."
        >>> verify_password("mypassword123", stored_hash)
        True
        >>> verify_password("wrongpassword", stored_hash)
        False

    Security Notes:
        - Use for sign-in authentication
        - Always call even if user doesn't exist (prevent timing attacks)
        - Never log the plain_password parameter
        - Comparison is constant-time (prevents timing side-channel attacks)
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def verify_token(token: str) -> dict:
    """
    Verify JWT token signature and extract claims.

    Validates token signature using BETTER_AUTH_SECRET and HS256 algorithm.
    Checks token expiration automatically (exp claim).
    Extracts user identity from 'sub' claim (user_id).

    Args:
        token: JWT token string (format: "header.payload.signature")

    Returns:
        dict: Decoded JWT claims containing:
            - sub: User ID (UUID as string)
            - email: User email address
            - iat: Issued at timestamp (Unix epoch)
            - exp: Expiration timestamp (Unix epoch)

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, or missing 'sub' claim

    Example:
        >>> token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        >>> claims = verify_token(token)
        >>> print(claims["sub"])  # User ID
        '550e8400-e29b-41d4-a716-446655440000'

    Security Notes:
        - Validates signature using shared BETTER_AUTH_SECRET
        - Automatically checks token expiration (exp claim)
        - Returns generic error message to prevent information leakage
        - Token must contain 'sub' claim (user ID) to be valid
    """
    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        # Extract user_id from 'sub' claim (JWT standard)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload

    except JWTError:
        # Generic error message to prevent information leakage
        # Same error for expired, invalid signature, or malformed tokens
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
