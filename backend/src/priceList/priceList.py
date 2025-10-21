from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm.exc import DetachedInstanceError
from base import Base
from src.client import client
from src.product import product
from dataclasses import dataclass


class PriceList(Base):
    __tablename__ = 'price_lists'

    id = Column(Integer,primary_key=True)
    #client_id = Column(Integer, ForeignKey('clients.id'))
    #client = relationship('Client')
    items = relationship('ItemPriceList', back_populates='list')
    name = Column(String)


    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

@dataclass
class PriceListDTO:
    name : String


class ItemPriceList(Base):
    __tablename__ = 'items_price_list'

    id = Column(Integer,primary_key=True)
    list_id = Column(Integer, ForeignKey('price_lists.id'))
    list = relationship('PriceList', back_populates='items')
    price = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    product = relationship('Product')

    def __init__(self, list, price, product):
        self.list = list
        self.price = price
        self.product = product

    from sqlalchemy.orm.exc import DetachedInstanceError

    def to_dict(self):
        try:
            product_name = self.product.name if self.product else None
        except DetachedInstanceError:
            product_name = None

        return {
            'id': self.id,
            'price': self.price,
            'product': product_name
        }


@dataclass
class ItemPriceListDTO:
    list_id: int
    price: float
    product_id: int