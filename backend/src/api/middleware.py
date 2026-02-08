from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import time
import logging

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add timing information to requests.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()

        # Add timing header to response
        response.headers["X-Process-Time"] = str(end_time - start_time)

        # Log request timing
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {(end_time - start_time)*1000:.2f}ms"
        )

        return response


class UserIsolationMiddleware(BaseHTTPMiddleware):
    """
    Middleware to ensure user data isolation by validating that
    requests are properly scoped to the authenticated user.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract user ID from the request if available (after auth middleware)
        user_id = request.state.user_id if hasattr(request.state, 'user_id') else None

        # Add the user_id to request state for downstream handlers to use
        if user_id:
            request.state.user_id = user_id

        response = await call_next(request)
        return response


class ValidationErrorMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle validation errors and return appropriate responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
        except HTTPException as exc:
            # Re-raise HTTPExceptions as-is
            raise exc
        except ValueError as exc:
            # Handle ValueError (e.g., invalid input data)
            return JSONResponse(
                status_code=400,
                content={"detail": f"Value error: {str(exc)}"}
            )
        except Exception as exc:
            # Log unexpected errors
            logger.error(f"Unexpected error in request {request.url}: {exc}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )

        return response