import os
import sys
import requests
from sqlalchemy import create_engine, text

API_URL = os.getenv("SMOKE_API_URL", "http://localhost:8000")

# For Windows host execution, DB is reachable via localhost:5432
DB_URL = os.getenv(
    "SMOKE_DATABASE_URL",
    os.getenv("DATABASE_URL", "postgresql+psycopg2://geoai:geoai@localhost:5432/geoai"),
)

def check_api() -> None:
    r = requests.get(f"{API_URL}/health", timeout=5)
    if r.status_code != 200:
        raise RuntimeError(f"API health failed: {r.status_code} {r.text}")

def check_db() -> None:
    engine = create_engine(DB_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1;"))

def main() -> int:
    check_api()
    check_db()
    print("Smoke test passed: API + DB OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
