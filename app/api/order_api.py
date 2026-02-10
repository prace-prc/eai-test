from fastapi import APIRouter, Body, HTTPException
from lxml import etree
from app.mapper.order_mapper import parse_orders
from app.utils.file_writer import save_orders_to_file

router = APIRouter()

@router.post("/orders", summary="주문 생성 API (XML 수신)")
async def create_order(xml_data: str = Body(..., media_type="application/xml")):
    try:
        wrapped_xml = f"<ROOT>{xml_data}</ROOT>" # XML에 ROOT 태그 추가하여 오류 방지
        xml_root = etree.fromstring(wrapped_xml.encode())
        orders = parse_orders(xml_root)

        if not orders:
            raise ValueError("주문 데이터 없음")
        
        file_path = save_orders_to_file(orders)

        return {
            "status": "SUCCESS",
            "saved_file": file_path,
            "order_count": len(orders),
            #"orders": orders 
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))