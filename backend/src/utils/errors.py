from fastapi import HTTPException, status
from typing import Optional


class BaseCustomException(HTTPException):
    """Base exception class for custom exceptions."""

    def __init__(self, detail: str = None, headers: Optional[dict] = None):
        super().__init__(status_code=self.status_code, detail=detail, headers=headers)


class UnauthorizedException(BaseCustomException):
    """Raised when user is not authorized to access a resource."""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Unauthorized"


class ForbiddenException(BaseCustomException):
    """Raised when user doesn't have permission to perform an action."""
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Forbidden"


class NotFoundException(BaseCustomException):
    """Raised when a requested resource is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found"


class ValidationException(BaseCustomException):
    """Raised when request validation fails."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation error"


def handle_error(error_type: str, detail: str = None):
    """
    Helper function to raise appropriate exceptions based on error type.

    Args:
        error_type: Type of error ('unauthorized', 'forbidden', 'not_found', 'validation')
        detail: Optional error message
    """
    error_map = {
        'unauthorized': UnauthorizedException,
        'forbidden': ForbiddenException,
        'not_found': NotFoundException,
        'validation': ValidationException,
    }

    error_class = error_map.get(error_type.lower())
    if error_class:
        raise error_class(detail=detail)
    else:
        raise ValueError(f"Unknown error type: {error_type}")