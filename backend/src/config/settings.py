from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    database_url: str

    # Authentication
    jwt_secret: str
    better_auth_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_seconds: int = 3600

    # AI/ML
    openai_api_key: str

    # Application
    app_name: str = "AI Chat Agent API"
    debug: bool = False
    cors_origins: str = "http://localhost:3000,http://localhost:3001"  # Comma-separated string

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert the comma-separated string to a list of origins."""
        if not self.cors_origins:
            return []
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()