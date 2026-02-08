from fastapi import APIRouter, Request, HTTPException
from lxml import etree

router = APIRouter()

@router.post("/orders")
async def create_order(request: Request):
    try:
        body = await request.body()
        xml_root = etree.fromstring(body)

        # 예시: HEADER 태그 개수 확인
        headers = xml_root.findall(".//HEADER")
        items = xml_root.findall(".//ITEM")

        if not headers or not items:
            raise ValueError("HEADER 또는 ITEM 누락")

        return {
            "status": "SUCCESS",
            "header_count": len(headers),
            "item_count": len(items)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))