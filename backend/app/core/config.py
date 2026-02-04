"""
Configuration management for the Todo App backend.

Loads environment variables and provides application settings using pydantic-settings.
All sensitive configuration values (secrets, database URLs) are loaded from .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Required environment variables:
    - DATABASE_URL: PostgreSQL connection string (format: postgresql://user:pass@host:port/dbname)
    - BETTER_AUTH_SECRET: JWT signing secret (64+ characters, shared with frontend)
    - CORS_ORIGINS: Comma-separated list of allowed CORS origins

    Optional environment variables:
    - APP_NAME: Application name for documentation (default: "Todo App API")
    - DEBUG: Enable debug mode (default: False)
    """

    # Database configuration
    DATABASE_URL: str

    # Authentication configuration
    BETTER_AUTH_SECRET: str

    # CORS configuration
    CORS_ORIGINS: str = "http://localhost:3000"

    # Application settings
    APP_NAME: str = "Todo App API"
    DEBUG: bool = False

    # JWT configuration
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600  # 1 hour

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into a list of origins.

        Example:
            CORS_ORIGINS="http://localhost:3000,https://app.example.com"
            -> ["http://localhost:3000", "https://app.example.com"]

        Returns:
            List of allowed CORS origin URLs
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
# Import this instance throughout the application to access configuration
settings = Settings()
