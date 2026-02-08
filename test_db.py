from app.db.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("DB 연결 성공 ✅", result.scalar())
except Exception as e:
    print("DB 연결 실패 ❌", e)