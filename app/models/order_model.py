from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Order(Base):
    __tablename__ = "ORDER_TB"

    order_id = Column(String(10), primary_key=True)
    applicant_key = Column(String(50))
    user_id = Column(String(20))
    name = Column(String(50))
    address = Column(String(200))
    status = Column(String(1))
    item_id = Column(String(20))
    item_name = Column(String(100))
    price = Column(Integer)