from dataclasses import dataclass
import os

@dataclass(frozen=True)
class DatabaseSettings:
    url: str

def load_database_settings() -> DatabaseSettings:
    # Example: postgresql+psycopg2://geoai:geoai@db:5432/geoai
    url = os.getenv("DATABASE_URL", "postgresql+psycopg2://geoai:geoai@localhost:5432/geoai")
    return DatabaseSettings(url=url)
