from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.chat_endpoint import router as chat_router
from .api.auth_routes import router as auth_router
from .api.mcp_routes import router as mcp_router
from .database import create_db_and_tables
from .config.settings import settings
from .api.middleware import TimingMiddleware, UserIsolationMiddleware


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="AI Chat Agent API",
        description="API for the AI Chat Agent & Conversation System",
        version="1.0.0",
        debug=settings.debug
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Additional security: expose only necessary headers
        # expose_headers=["Access-Control-Allow-Origin"]
    )

    # Add custom middleware
    app.add_middleware(TimingMiddleware)
    app.add_middleware(UserIsolationMiddleware)

    # Include API routers
    app.include_router(auth_router)
    app.include_router(mcp_router)
    app.include_router(chat_router)

    @app.on_event("startup")
    def startup_event():
        """Initialize database tables on startup."""
        print("Initializing database tables...")
        create_db_and_tables()
        print("Database tables initialized.")

    @app.get("/")
    def read_root():
        """Root endpoint for health check."""
        return {"message": "AI Chat Agent API is running", "version": "1.0.0"}

    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": "1.0.0"}

    return app


# Create the main application instance
app = create_application()


# Additional utility functions for testing and development
def run_development_server():
    """
    Utility function to run the development server.
    This is mainly for local development and testing.
    """
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
        log_level="info"
    )


if __name__ == "__main__":
    # This allows running the file directly for development
    run_development_server()