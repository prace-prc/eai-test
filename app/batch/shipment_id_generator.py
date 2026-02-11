from sqlalchemy import text

PREFIX = "A"
_counter = None


def get_next_shipment_id(session):
    global _counter

    # 최초 1회만 DB에서 마지막 번호 조회
    if _counter is None:
        row = session.execute(text(f"""
            SELECT NVL(MAX(TO_NUMBER(SUBSTR(SHIPMENT_ID, 2, 3))), 0)
            FROM SHIPMENT_TB
            WHERE SHIPMENT_ID LIKE '{PREFIX}%'
        """)).scalar()

        _counter = int(row)

    # 증가
    _counter += 1

    # 3자리 포맷
    if _counter > 999:
        raise Exception("SHIPMENT_ID 3자리 초과. 규칙 변경 필요")

    return f"{PREFIX}{_counter:03d}"