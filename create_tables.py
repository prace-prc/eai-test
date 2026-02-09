from sqlalchemy import text
from app.db.database import engine

query = """
SELECT table_name 
FROM user_tables 
WHERE table_name = 'ORDER_TB'
"""

with engine.connect() as conn:
    result = conn.execute(text(query)).fetchall()

    if result:
        print("ORDER_TB 테이블 존재함 ✅")
    else:
        print("ORDER_TB 테이블 없음 ❌")