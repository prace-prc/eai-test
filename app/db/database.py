import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

ORDER_TB_URL = f"mysql+pymysql://{os.getenv('ORDER_TB_USER')}:{os.getenv('ORDER_TB_PASSWORD')}@" \
               f"{os.getenv('ORDER_TB_HOST')}:{os.getenv('ORDER_TB_PORT')}/{os.getenv('ORDER_TB_TABLENAME')}?charset=utf8mb4"

print(ORDER_TB_URL)

engine = create_engine(
    ORDER_TB_URL,
    pool_pre_ping=True,  # 죽은 커넥션 자동 체크
    connect_args={
        "ssl": {}
    }
)