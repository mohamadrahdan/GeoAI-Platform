import os

REQUIRED_VARS = [
    "DATABASE_URL",
    "POSTGRES_USER",
    "POSTGRES_DB",
]

def validate_env() -> None:
    missing = [v for v in REQUIRED_VARS if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
