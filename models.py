from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    seller = Column(String(100))
    buyer = Column(String(100))
    sold_price = Column(Integer) 
    closing_date = Column(DateTime, default=datetime.utcnow)
    Type = Column(String(50))                    
    status = Column(String(50))
    address = Column(String(50)) 

    def __init__(self, seller=None, buyer=None, sold_price=None, closing_date=None, Type=None,
                status=None, address=None):
        self.seller = seller
        self.buyer = buyer
        self.sold_price = sold_price
        self.closing_date = closing_date
        self.Type = Type
        self.status = status 
        self.address = address 

    def __repr__(self):
        return '<Sales %r>' % (self.seller)