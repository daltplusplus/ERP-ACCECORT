from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from base import Base
from src.client import client
from src.product import product
from src.priceList import priceList
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TicketState(Enum):
    ISSUED = "ISSUED"
    PAID = "PAID"
    CANCELED = "CANCELED"

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer,primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client')
    items = relationship('ItemTicket', back_populates='ticket' )
    total = Column(Float)
    discount = Column(Float)
    subtotal = Column(Float)
    date = Column(DateTime)
    state = Column(SQLAlchemyEnum(TicketState), default=TicketState.ISSUED)

    def __init__(self, client):
        self.client = client

    def to_dict(self, include_items=True, include_client= False):
        data = {
            "id": self.id,
            "client_id": self.client_id,
            "total": self.total,
            "discount": self.discount,
            "subtotal": self.subtotal,
            "date": self.date.strftime("%d/%m/%Y") if self.date else None,
            "state": str(self.state.name)
        }

        if include_items:
            data["items"] = [item.to_dict() for item in self.items]
        if include_client:
            data["client_name"] = self.client.name

        return data

@dataclass
class TicketDTO:
    discount: float
    total: float
    subtotal: float
    state: String


class ItemTicket(Base):
    __tablename__ = 'items_ticket'

    id = Column(Integer,primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    ticket = relationship('Ticket', back_populates='items')
    name = Column(String)
    unitPrice = Column(Float)
    amount = Column(Integer)
    subtotal = Column(Float)
    itemPriceList_id = Column(Integer, ForeignKey('items_price_list.id'))
    itemPriceList = relationship('ItemPriceList')

    def __init__(self, ticket, itemPriceListId, amount, unitPrice, subtotal):
        self.ticket = ticket
        self.itemPriceList_id = itemPriceListId
        self.amount = amount
        self.unitPrice = unitPrice
        self.subtotal = subtotal

    def to_dict(self):
        return {
            "id": self.id,
            "ticket_id": self.ticket_id,
            "unit_price": self.unitPrice,
            "amount": self.amount,
            "subtotal": self.subtotal,
            "name": self.name,
            "item_price_list_id": self.itemPriceList_id
        }

@dataclass
class ItemTicketDTO:
    unitPrice: float
    amount: int
    itemPriceListId: int
    subtotal: float
    name: String