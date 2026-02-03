# test_db.py
from backend.db.session import db_session
from sqlalchemy import text

with db_session() as db:
    result = db.execute(text("SELECT 1")).scalar()
    print(result, "OK")
