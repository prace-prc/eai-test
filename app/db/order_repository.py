from sqlalchemy.orm import Session
from app.models.order_model import Order
from app.core.config import APPLICANT_KEY

def insert_orders(session: Session, orders: list):
    db_objects = []

    for o in orders:
        db_objects.append(
            Order(
                order_id=o["order_id"],
                applicant_key=APPLICANT_KEY,
                user_id=o["user_id"],
                name=o["name"],
                address=o["address"],
                status=o["status"],
                item_id=o["item_id"],
                item_name=o["item_name"],
                price=o["price"],
            )
        )

    session.add_all(db_objects)
    session.commit()