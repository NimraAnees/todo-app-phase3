"""
FastAPI main application for Todo App authentication API.

This module initializes the FastAPI application, configures CORS middleware,
and mounts the authentication router.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


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
from app.routers import auth

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
