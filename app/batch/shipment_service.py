import os
import uuid
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import APPLICANT_KEY
from app.batch.shipment_id_generator import get_next_shipment_id

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log_sql(query, params):
    print("\n 실행 SQL -------------------------")
    print(query.strip())
    print(" PARAMS:", params)
    print("-------------------------------------")

def _log(run_id: str, step: str, status: str, message: str = ""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{now}] [shipment] [{run_id}] [{step}] [{status}] {message}\n"
    logfile = os.path.join(LOG_DIR, f"shipment_{datetime.now().strftime('%Y%m%d')}.log")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(line)

def process_shipments(session):
    run_id = str(uuid.uuid4())

    _log(run_id, "SELECT_ORDER_TB", "INFO", f"key={APPLICANT_KEY}")

    rows = session.execute(text("""
        SELECT * FROM ORDER_TB
        WHERE APPLICANT_KEY = :key
        AND STATUS = 'N'
    """), {"key": APPLICANT_KEY}).mappings().all()

    _log(run_id, "SELECT_ORDER_TB", "SUCCESS", f"count={len(rows)}")

    if not rows:
        _log(run_id, "END", "SUCCESS", "대상 없음")
        return

    prefix = "A"
    num = 100

    for o in rows:
        shipment_id = get_next_shipment_id(session)

        _log(
            run_id,
            "ROW_START",
            "INFO",
            f"order_id={o.get('order_id')}, shipment_id={shipment_id}"
        )

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
            _log(run_id, "END", "SUCCESS", "운송할 주문 없음")
            return

        print(f"{len(orders)}건 처리 시작")
        _log(run_id, "PROCESS_COUNT", "INFO", f"count={len(orders)}")

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
        _log(run_id, "INSERT_SHIPMENT_TB", "INFO", f"params={insert_params}")
        log_sql(insert_sql, insert_params)

        session.execute(text(insert_sql), insert_params)
        _log(run_id, "INSERT_SHIPMENT_TB", "SUCCESS", f"order_id={o.get('order_id')}")

        session.execute(text("""
            UPDATE ORDER_TB SET STATUS='Y'
            WHERE ORDER_ID=:oid
        """), {"oid": o["order_id"]})

        _log(run_id, "UPDATE_ORDER_TB", "SUCCESS", f"order_id={o.get('order_id')}")

    session.commit()
    _log(run_id, "COMMIT", "SUCCESS", "커밋 완료")
    _log(run_id, "END", "SUCCESS", "운송 배치 종료")