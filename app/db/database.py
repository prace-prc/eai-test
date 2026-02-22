import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("ORDER_TB_USER")
DB_PASS = os.getenv("ORDER_TB_PASSWORD")
DB_HOST = os.getenv("ORDER_TB_HOST")
DB_PORT = os.getenv("ORDER_TB_PORT")
DB_SERVICE = os.getenv("ORDER_TB_SID")

dsn = f"{DB_HOST}:{DB_PORT}/?service_name={DB_SERVICE}"

engine = create_engine(
    f"oracle+oracledb://{DB_USER}:{DB_PASS}@{dsn}",
    pool_pre_ping=True
)
SessionLocal = sessionmaker(bind=engine)