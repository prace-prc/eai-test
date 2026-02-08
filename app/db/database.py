import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

ORDER_TB_URL = f"mysql+pymysql://{os.getenv('ORDER_TB_USER')}:{os.getenv('ORDER_TB_PASS')}@" \
               f"{os.getenv('ORDER_TB_HOST')}:{os.getenv('ORDER_TB_PORT')}/{os.getenv('ORDER_TB_NAME')}"

engine = create_engine(ORDER_TB_URL, echo=True)