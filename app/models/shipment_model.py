from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Shipment(Base):
    __tablename__ = "SHIPMENT_TB"

    shipment_id = Column(String(10), primary_key=True)
    applicant_key = Column(String(50))
    order_id = Column(String(10), primary_key=True)                   
    item_id = Column(String(20))
    address = Column(String(100))