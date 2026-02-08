from fastapi import APIRouter, Body, HTTPException
from lxml import etree
from app.mapper.order_mapper import parse_orders

router = APIRouter()

@router.post("/orders", summary="주문 생성 API (XML 수신)")
async def create_order(xml_data: str = Body(..., media_type="application/xml")):
    try:
        xml_root = etree.fromstring(xml_data.encode())
        orders = parse_orders(xml_root)

        if not orders:
            raise ValueError("주문 데이터 없음")

        return {
            "status": "SUCCESS",
            "order_count": len(orders),
            "orders": orders
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))