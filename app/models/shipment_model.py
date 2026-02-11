from sqlalchemy import Column, String, Integer
from app.db.base import Base

class Shipment(Base):
    __tablename__ = "SHIPMENT_TB"

    shipment_id = Column(String(10), primary_key=True)
    applicant_key = Column(String(50))                   
    user_id = Column(String(20))
    item_id = Column(String(20))
    item_name = Column(String(100))
    price = Column(Integer)