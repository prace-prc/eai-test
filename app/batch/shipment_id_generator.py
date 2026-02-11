from sqlalchemy import text

def get_next_shipment_id(session):
    result = session.execute(text("""
        SELECT MAX(SHIPMENT_ID) FROM SHIPMENT_TB
    """)).scalar()

    # 테이블이 비어있는 경우
    if not result:
        return "A001"

    prefix = result[0]          # 알파벳
    number = int(result[1:])    # 숫자 부분

    next_number = number + 1
    return f"{prefix}{next_number:03d}"