from sqlalchemy import text

def generate_order_id(session):
    query = text("""
        SELECT NVL(MAX(ORDER_ID), 'A000') FROM ORDER_TB
    """)

    last_id = session.execute(query).scalar()

    prefix = last_id[0]
    number = int(last_id[1:])

    number += 1

    if number > 999:
        prefix = chr(ord(prefix) + 1)
        number = 1

    return f"{prefix}{number:03d}"