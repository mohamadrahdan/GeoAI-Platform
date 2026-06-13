import os
from dataclasses import dataclass
from pathlib import Path


class BaseConfig:
    "Base configuration shared across all environments."

    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development").lower()
        self.APP_NAME = os.getenv("APP_NAME", "GeoAI-Platform")
        self.APP_DEBUG = True
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # Database Configuration
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "geoai")
        # SECURITY FIX: Ensure password is provided for non-dev environments
        # or at least not empty if explicitly set
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

        # FAIL-FAST VALIDATION
        if not self.POSTGRES_PASSWORD:
            if self.APP_ENV in ["production", "prod"]:
                raise ValueError(
                    "CRITICAL ERROR: POSTGRES_PASSWORD must be set in production!"
                )
            else:
                self.POSTGRES_PASSWORD = "geoai"

        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "geoai")
        self.DATA_ROOT_RAW = os.getenv("DATA_ROOT", str(Path.cwd() / "data"))

    @property
    def DATABASE_URL(self) -> str:
        override = os.getenv("DATABASE_URL")
        if override:
            return override
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class DevelopmentConfig(BaseConfig):
    "Development-specific overrides."

    def __init__(self):
        super().__init__()
        self.APP_DEBUG = True


class ProductionConfig(BaseConfig):
    "Production-specific overrides."

    def __init__(self):
        super().__init__()
        self.APP_DEBUG = False
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING")  # Stricter logging in prod


class TestingConfig(BaseConfig):
    "Testing-specific overrides."

    def __init__(self):
        super().__init__()
        self.APP_DEBUG = True
        self.POSTGRES_DB = os.getenv("POSTGRES_DB_TEST", "geoai_test")


def get_settings() -> BaseConfig:
    "Factory function to instantiate the correct config profile based on APP_ENV."
    env_state = os.getenv("APP_ENV", "development").lower()
    if env_state in ["production", "prod"]:
        return ProductionConfig()
    elif env_state in ["testing", "test"]:
        return TestingConfig()
    return DevelopmentConfig()


# Global settings object
settings = get_settings()


# Maintained for backward compatibility with backend/db/session.py
# and backend/db/health.py
@dataclass(frozen=True)
class DatabaseSettings:
    url: str


def load_database_settings() -> DatabaseSettings:
    return DatabaseSettings(url=settings.DATABASE_URL)
