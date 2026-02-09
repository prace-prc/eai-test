from app.db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1 FROM DUAL"))
    print("Oracle 연결 성공 ✅", result.scalar())