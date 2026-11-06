"""
Configuration management for the Enterprise Deal & Revenue Intelligence Platform.
Loads environment variables and provides typed configuration.
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Enterprise Deal & Revenue Intelligence Platform"
    app_version: str = "1.0.0"
    debug: str = "false"
    environment: str = "development"

    @property
    def is_debug(self) -> bool:
        """Parse debug from string to boolean."""
        return self.debug.lower() in ("true", "1", "yes", "on")

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "hindsight"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Groq API
    groq_api_key: Optional[str] = None
    groq_model: str = "qwen/qwen3-32b"

    # Hindsight API
    hindsight_api_url: str = "https://api.hindsight.vectorize.io"
    hindsight_api_key: Optional[str] = None

    # CORS
    cors_origins: list[str] = ["*"]

    # API
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()