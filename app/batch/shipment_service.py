from sqlalchemy import text

from app.core.config import APPLICANT_KEY
from app.batch.shipment_id_generator import get_next_shipment_id

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

        session.execute(text("""
            INSERT INTO SHIPMENT_TB
            (SHIPMENT_ID, APPLICANT_KEY, USER_ID, ITEM_ID, ITEM_NAME, PRICE)
            VALUES (:sid, :aid, :uid, :iid, :iname, :price)
        """), {
            "sid": shipment_id,
            "aid": o["APPLICANT_KEY"],
            "uid": o["USER_ID"],
            "iid": o["ITEM_ID"],
            "iname": o["ITEM_NAME"],
            "price": o["PRICE"]
        })

        session.execute(text("""
            UPDATE ORDER_TB SET STATUS='Y'
            WHERE ORDER_ID=:oid
        """), {"oid": o["ORDER_ID"]})

    session.commit()