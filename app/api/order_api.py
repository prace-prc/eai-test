import os
from dotenv import load_dotenv
from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.orm import sessionmaker
from lxml import etree

from app.db.database import engine
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

router = APIRouter()
SessionLocal = sessionmaker(bind=engine)

@router.post("/orders", summary="주문 수신 API")
async def create_order(data: str = Body(..., media_type="text/plain")):
    session = SessionLocal()
    
    try:
        xml_string = decode_base64_euckr(data)
        wrapped_xml = f"<ROOT>{xml_string}</ROOT>" # XML에 ROOT 태그 추가하여 오류 방지
        xml_root = etree.fromstring(wrapped_xml.encode())
        orders = parse_orders(xml_root, session)

        if not orders:
            raise ValueError("주문 데이터 없음")
        
        file_path = save_orders_to_file(orders, APPLICANT_NAME, APPLICANT_KEY)

        upload_file_sftp(
            file_path,
            SFTP_HOST,
            SFTP_PORT,
            SFTP_USER,
            SFTP_PASSWORD,
            SFTP_FILE_PATH
        )

        return {
            "status": "SUCCESS",
            "saved_file": file_path,
            "order_count": len(orders),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        session.close()