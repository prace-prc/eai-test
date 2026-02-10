from sqlalchemy.exc import SQLAlchemyError
from app.db.database import engine
from app.db.base import Base
from app.models.order_model import Order

def create_tables():
    try:
        print("테이블 생성 시도 중...")
        Base.metadata.create_all(bind=engine)
        print("테이블 생성 완료")

    except SQLAlchemyError as e:
        print("DB 작업 중 오류 발생")
        print("에러 타입:", type(e).__name__)
        print("에러 내용:", e)

    except Exception as e:
        print("예상치 못한 오류")
        print(type(e).__name__, e)


if __name__ == "__main__":
    create_tables()