from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import engine, SessionLocal
from app.batch.shipment_service import process_shipments

def run_job():
    session = SessionLocal()
    try:
        print("운송 배치 시작")
        process_shipments(session)
        print("운송 배치 완료")
    except Exception as e:
        print("배치 중 오류발생:", e)
        session.rollback()
    finally:
        session.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    run_job()
    scheduler.add_job(run_job, "interval", minutes=5)
    scheduler.start()