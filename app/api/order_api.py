import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import sessionmaker
from lxml import etree

from app.db.database import engine
from app.db.order_repository import insert_orders
from app.mapper.order_mapper import parse_orders
from app.utils.file_writer import save_orders_to_file
from app.utils.decoder import decode_base64_euckr
from app.utils.sftp_client import upload_file_sftp

load_dotenv()

APPLICANT_NAME=os.getenv("APPLICANT_NAME")
APPLICANT_KEY=os.getenv("APPLICANT_KEY")
SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT"))
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASSWORD = os.getenv("SFTP_PASSWORD")
SFTP_FILE_PATH = os.getenv("SFTP_FILE_PATH")

#로그 남기기
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

router = APIRouter()
SessionLocal = sessionmaker(bind=engine)

def _log(request_id: str, step: str, status: str, message: str = "") -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] [{request_id}] [{step}] [{status}] {message}\n"
    logfile = os.path.join(LOG_DIR, f"scenario1_{datetime.now().strftime('%Y%m%d')}.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line)

@router.post("/orders", summary="주문 수신 API")
async def create_order(data: str = Body(..., media_type="text/plain")):
    request_id = str(uuid.uuid4())
    session = SessionLocal()
    
    try:
        xml_string = decode_base64_euckr(data)
        # 1) XML Parse
        try:
            wrapped_xml = f"<ROOT>{xml_string}</ROOT>" 
            xml_root = etree.fromstring(wrapped_xml.encode())
            _log(request_id, "XML_PARSE", "SUCCESS")
        except Exception as e:
            _log(request_id, "XML_PARSE", "FAIL", str(e))
            raise HTTPException(status_code=400, detail=f"XML 파싱 실패: {e}")

        # 2) Mapping/Validation
        try:
            orders = parse_orders(xml_root, session)
            if not orders:
                raise ValueError("주문 데이터 없음")
            _log(request_id, "VALIDATION", "SUCCESS", f"{len(orders)}건")
        except Exception as e:
            _log(request_id, "VALIDATION", "FAIL", str(e))
            raise HTTPException(status_code=400, detail=f"유효성 검증 실패: {e}")

        # 3) DB Insert
        try:
            insert_orders(session, orders)   # insert_orders 내부 commit 금지(중요)
            session.flush()                  # DB 반영은 하되, 최종 확정은 commit에서
            _log(request_id, "DB_INSERT", "SUCCESS", f"{len(orders)}건")
        except SQLAlchemyError as e:
            session.rollback()
            _log(request_id, "DB_INSERT", "FAIL", str(e))
            raise HTTPException(status_code=500, detail=f"DB 저장 실패: {e}")
        except Exception as e:
            session.rollback()
            _log(request_id, "DB_INSERT", "FAIL", str(e))
            raise HTTPException(status_code=500, detail=f"DB 처리 실패: {e}")

        # 4) File Create
        try:
            file_path = save_orders_to_file(orders, APPLICANT_NAME, APPLICANT_KEY)
            _log(request_id, "FILE_CREATE", "SUCCESS", file_path)
        except OSError as e:
            session.rollback()
            _log(request_id, "FILE_CREATE", "FAIL", str(e))
            raise HTTPException(status_code=500, detail=f"파일 생성 실패: {e}")
        except Exception as e:
            session.rollback()
            _log(request_id, "FILE_CREATE", "FAIL", str(e))
            raise HTTPException(status_code=500, detail=f"파일 처리 실패: {e}")

        # 5) SFTP Upload
        try:
            upload_file_sftp(
                file_path,
                SFTP_HOST,
                SFTP_PORT,
                SFTP_USER,
                SFTP_PASSWORD,
                SFTP_FILE_PATH
            )
            _log(request_id, "SFTP_SEND", "SUCCESS", file_path)
        except Exception as e:
            # SFTP 실패하면 DB도 확정(commit)하지 않도록 rollback
            session.rollback()
            _log(request_id, "SFTP_SEND", "FAIL", str(e))
            raise HTTPException(status_code=502, detail=f"SFTP 전송 실패: {e}")

        # 여기까지 왔으면 DB + 파일 + SFTP 모두 성공 → 최종 커밋
        session.commit()
        _log(request_id, "END", "SUCCESS", "전체 처리 완료")

        return {
            "request_id": request_id,
            "status": "SUCCESS",
            "saved_file": file_path,
            "order_count": len(orders),
        }

    except HTTPException:
        raise

    except Exception as e:
        # 예상 못한 에러
        session.rollback()
        _log(request_id, "UNEXPECTED", "FAIL", str(e))
        raise HTTPException(status_code=500, detail=f"예상치 못한 오류: {e}")

    finally:
        session.close()