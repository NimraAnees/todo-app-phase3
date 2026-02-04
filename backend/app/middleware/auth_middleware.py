"""
Authentication middleware for JWT token extraction and verification.

Provides middleware that:
- Extracts JWT from Authorization: Bearer header
- Verifies token signature and expiration
- Returns 401 Unauthorized for missing or invalid tokens
- Attaches user claims to request state for downstream handlers
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.security import verify_token


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to authenticate requests using JWT tokens.

    Extracts JWT token from Authorization: Bearer header on all requests.
    Verifies token signature and expiration using verify_token().
    Returns 401 Unauthorized if token is missing or invalid.

    Protected routes should use this middleware to enforce authentication.
    Public routes (e.g., /health, /docs) can bypass this middleware.

    Usage:
        app.add_middleware(AuthMiddleware)

    Request Flow:
        1. Extract Authorization header
        2. Verify Bearer token format
        3. Verify token signature and expiration
        4. Attach user claims to request.state.user
        5. Call next middleware/handler

    Error Responses:
        - 401: Missing Authorization header
        - 401: Invalid Bearer token format
        - 401: Expired or invalid token signature
    """

    async def dispatch(self, request: Request, call_next):
        """
        Process request and verify authentication token.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware or route handler

        Returns:
            Response from downstream handler or 401 error response

        Raises:
            HTTPException: 401 Unauthorized if token is missing or invalid
        """
        # Skip authentication for public endpoints
        public_paths = ["/health", "/docs", "/redoc", "/openapi.json"]
        if request.url.path in public_paths:
            return await call_next(request)

        # Extract Authorization header
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing authentication credentials"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify Bearer token format
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid authentication scheme"},
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except ValueError:
            # Authorization header doesn't contain two parts
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid authorization header format"},
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify token signature and expiration
        try:
            claims = verify_token(token)
            # Attach user claims to request state for downstream handlers
            request.state.user = claims
        except HTTPException as e:
            # Token verification failed (expired, invalid signature, etc.)
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
                headers=e.headers or {},
            )

        # Continue to next middleware or route handler
        response = await call_next(request)
        return response
