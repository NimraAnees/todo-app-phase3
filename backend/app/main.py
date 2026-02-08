"""
FastAPI main application for Todo App authentication API.

This module initializes the FastAPI application, configures CORS middleware,
and mounts the authentication router.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database import create_db_and_tables
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Authentication API for Todo App with JWT-based security",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,  # Required for httpOnly cookies and Authorization header
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type", "Access-Control-Allow-Origin"],
    # Allow credentials to be sent with cross-origin requests
    # This is essential for sending JWT tokens in Authorization header
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Log validation errors for debugging."""
    body = await request.body()
    logger.error(f"Validation error on {request.url}")
    logger.error(f"Request body: {body.decode()}")
    logger.error(f"Validation errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


@app.on_event("startup")
async def on_startup():
    """
    Application startup event handler.

    Creates all database tables if they don't exist.
    This ensures the database schema is initialized when the application starts.
    """
    create_db_and_tables()


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message indicating API is operational
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME
    }


# Import and mount routers
# Note: Import here to avoid circular dependencies
from app.routers import auth, tasks

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/v1", tags=["Tasks"])
