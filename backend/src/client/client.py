from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src.priceList.priceList import PriceList
from sqlalchemy.orm import relationship
from base import Base
from dataclasses import dataclass

class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer,primary_key=True)
    name = Column(String)
    adress = Column(String)
    phone = Column(String)
    pricelist_id = Column(Integer, ForeignKey('price_lists.id'))
    pricelist = relationship('PriceList')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'adress': self.adress,
            'phone': self.phone,
            'pricelist_id': self.pricelist_id
        }

@dataclass
class ClientDTO:
    pricelist_id: int
    name: String
    phone: String
    adress: String
