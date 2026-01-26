from sqlalchemy import create_engine, text
from core.config.settings import load_database_settings

def check_db() -> bool:
    settings = load_database_settings()
    engine = create_engine(settings.url, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1;"))
    return True
