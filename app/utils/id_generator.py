from sqlalchemy import text

def generate_order_id(session):
    result = session.execute(text(
        "SELECT NVL(MAX(ORDER_ID), 'A000') FROM ORDER_TB"
    )).scalar()

    prefix = result[0]
    number = int(result[1:])
    return prefix, number