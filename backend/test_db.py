from sqlalchemy import text

from app.database import engine

with engine.connect() as conn:
    print("DB connected, SELECT 1 ->", conn.execute(text("SELECT 1")).scalar())