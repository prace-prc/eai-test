from sqlalchemy import text

from app.core.config import APPLICANT_KEY
from app.batch.shipment_id_generator import get_next_shipment_id

def log_sql(query, params):
    print("\n 실행 SQL -------------------------")
    print(query.strip())
    print(" PARAMS:", params)
    print("-------------------------------------")

def process_shipments(session):
    rows = session.execute(text("""
        SELECT * FROM ORDER_TB
        WHERE APPLICANT_KEY = :key
        AND STATUS = 'N'
    """), {"key": APPLICANT_KEY}).mappings().all()

    if not rows:
        return

    prefix = "A"
    num = 100

    for o in rows:
        shipment_id = get_next_shipment_id(session)

        orders = session.execute(text("""
        SELECT ORDER_ID,
               USER_ID,
               ITEM_ID,
               ADDRESS,
               APPLICANT_KEY
                FROM ORDER_TB
                WHERE STATUS = 'N'
            """)).fetchall()

        if not orders:
            print("운송할 주문 없음")
            return

        print(f"{len(orders)}건 처리 시작")

        insert_sql = """
            INSERT INTO SHIPMENT_TB
            (SHIPMENT_ID, APPLICANT_KEY, ORDER_ID, ITEM_ID, ADDRESS)
            VALUES (:sid, :aid, :oid, :iid, :addr)
        """
        insert_params = {
            "sid": shipment_id,
            "aid": o["applicant_key"],
            "oid": o["order_id"],
            "iid": o["item_id"],
            "addr": o["address"]
        }
        log_sql(insert_sql, insert_params)
        session.execute(text(insert_sql), insert_params)

        session.execute(text("""
            UPDATE ORDER_TB SET STATUS='Y'
            WHERE ORDER_ID=:oid
        """), {"oid": o["order_id"]})

    session.commit()