import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('ORDER_TB_HOST'),
        port=11527,
        user=os.getenv('ORDER_TB_USER'),
        password=os.getenv('ORDER_TB_PASSWORD'),
        database=os.getenv('ORDER_TB_TABLENAME'),
        connect_timeout=10,
        ssl={}
    )
    print("직접 연결 성공 ✅")
    conn.close()
except Exception as e:
    print("직접 연결 실패 ❌", e)